// Item variants (RUL-2026-10-29-047: Skyglass trophies are variant tokens), read at
// studie-tech/TheNinjaRPG@3314d122c93e036618483d18229a793ad7ad21fd.
//
//   routers/item.ts:1151-1275  getItemVariants {itemId} lists one item's variants by order;
//                              upsertItemVariant {itemId, variant: ItemVariantValidator} inserts when
//                              variant.id is absent and answers {success, message: "Variant saved"}
//                              with NO id, else replaces the whole record. Both protectedProcedure, no
//                              limiter; the body requires canChangeContent. Refused before any write:
//                              the item or a required unlock item missing, requiredItemId on a cost
//                              other than VARIANT_TOKEN, a required item with no unlockitemvariant
//                              whose variantId is null or this variant's id, furnitureData on a
//                              non-furniture item, MAX_ITEM_VARIANTS, an order another variant holds.
//   queries/item.ts:981-1060   the insert is INSERT ... SELECT WHERE the items exist ON DUPLICATE KEY
//                              UPDATE id = id, so a taken (itemId, order) writes nothing and is refused.
//   drizzle/schema.ts:1736-1766  ItemVariant: name varchar(191), image varchar(512), cost int, a
//                              unique (itemId, order) index, and no hidden column.
//   routers/item.ts:1458-1520  consumeVariantToken: the token's unlockitemvariant must have no variantId
//                              or this one; a variant with requiredItemId accepts only that item.
//
// Visibility: none. A variant shows in its base item's Variants list for every owner from the moment
// it exists (a token variant as "Need <token>"; any other cost can be bought at once). A create
// carries hidden:true for law 16b like every entity; it is stripped and never diffed.
//
// No point read and no id in the create answer: the id is found by (itemId, order), which the unique
// index makes one row, among the rows the pre-create read did not hold.

export const MAX_VARIANTS = 7; // MAX_ITEM_VARIANTS, drizzle/constants.ts:20 (checkout-gated test)
const INT_MAX = 2147483647;    // MySQL int
const url = (s) => { try { return /^https?:\/\/\S+$/.test(s) && !!new URL(s); } catch { return false; } };

/** The upsert input. `itemId` is the envelope key; hidden has no column. */
export function variantInput(d, id) {
  const { itemId, hidden: _h, ...v } = d;
  return { itemId, variant: id ? { ...v, id } : v };
}

/**
 * An edit replaces the whole record (the update sets every column), so the live row is re-sent for
 * every key the manifest leaves out. description/battleDescription are z.string().optional(): the
 * stored SQL NULL must be omitted, never sent as null.
 */
export function mergeVariant(live, data, fields) {
  const src = { ...(live ?? {}), ...data }, out = { itemId: src.itemId };
  for (const k of fields ?? []) if (src[k] !== undefined && !(src[k] === null && /escription$/.test(k))) out[k] = src[k];
  return out;
}

/** One variant from its item's list, as the runner reads any record: {ok, data|error}. */
export async function readVariant(reader, id, data) {
  if (!data || typeof data.itemId !== "string") return { ok: false, error: { code: "BAD_REQUEST", message: "a variant read needs its itemId" } };
  const r = await reader.list("item.getItemVariants", { fresh: true, input: { itemId: data.itemId } });
  if (!r.ok) return r;
  if (!Array.isArray(r.data)) throw new Error("item.getItemVariants did not return an array");
  return { ok: true, data: id == null ? r.data : r.data.find((v) => v && v.id === id) ?? null };
}

/** ItemVariantValidator bounds plus the column limits zod does not know. */
export function variantProblems(d, { preCreate = false } = {}) {
  const out = [], str = (v) => typeof v === "string";
  if (!str(d.itemId) || !d.itemId) out.push("itemId: every variant item names its base item (upsertItemVariant takes {itemId, variant})");
  if ("id" in d) out.push("id: the variant id is the item's targetId; do not send it in data");
  if ("hidden" in d && d.hidden !== true) out.push("hidden: a variant has no hidden column; send hidden:true (law 16b)");
  if (preCreate) for (const k of ["name", "image", "costType", "cost", "order"]) if (d[k] === undefined) out.push(`${k} is required on a variant create`);
  if ("name" in d && !(str(d.name) && d.name && d.name === d.name.trim() && d.name.length <= 191)) out.push("name: 1-191 characters, no leading or trailing whitespace");
  if ("image" in d && !(str(d.image) && (d.image.startsWith("@img:") || url(d.image) && d.image.length <= 512))) out.push("image: an @img ref or a URL of at most 512 characters");
  if ("costType" in d && !str(d.costType)) out.push("costType must be a string");
  if ("cost" in d && !(Number.isSafeInteger(d.cost) && d.cost >= 0 && d.cost <= INT_MAX)) out.push("cost: an integer 0.." + INT_MAX);
  if ("order" in d && !(Number.isSafeInteger(d.order) && d.order >= 1 && d.order <= MAX_VARIANTS)) out.push(`order: an integer 1..${MAX_VARIANTS} (unique per item)`);
  for (const k of ["description", "battleDescription"]) if (k in d && !str(d[k])) out.push(`${k}: a string; omit it to leave it empty (null is refused)`);
  if ("requiredItemId" in d && d.requiredItemId !== null) {
    if (!str(d.requiredItemId) || !d.requiredItemId.trim()) out.push("requiredItemId: an item id, an @item ref or null");
    else if ("costType" in d && d.costType !== "VARIANT_TOKEN") out.push("requiredItemId: only a VARIANT_TOKEN variant can require an unlock item");
  }
  if ("furnitureData" in d && d.furnitureData !== null && (typeof d.furnitureData !== "object" || Array.isArray(d.furnitureData))) out.push("furnitureData: an object or null");
  return out;
}

/**
 * The rows a create may have produced: not held before it (`before`, the pre-create read's ids) and
 * owned by no journal item. `matches` = at the planned order and holding the asserted keys.
 */
export function variantCandidates(rows, before, data, diff, owned = new Set()) {
  const seen = new Set(before ?? []);
  return rows.filter((v) => v && !seen.has(v.id) && !owned.has(v.id))
    .map((v) => ({ id: v.id, name: v.name ?? null, order: v.order, matches: v.order === data.order && !diff("itemVariant", data, v).length }));
}

/** Refusals the server makes from the item's current variants, checked before the create is sent. */
export function variantSlotProblem(rows, d) {
  if (rows.length >= MAX_VARIANTS) return `the item already has ${rows.length} variants (at most ${MAX_VARIANTS})`;
  const taken = rows.find((v) => v.order === d.order);
  return taken ? `order ${d.order} is already used by "${taken.name}" (${taken.id})` : null;
}
