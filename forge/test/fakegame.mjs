// An in-memory game that answers like TrpcClient.batch() would (decoded elements), with the
// create/update/get/getAllNames semantics read at source: create inserts a placeholder and
// returns the id in message; update merges; get returns the row. Records every call, and can
// CRASH (throw) at a chosen call number to simulate tab eviction mid-flight: the call has
// been applied server-side (the request left) but the client never sees the response.
//
// This is what lets the runner tests assert "resume never double-creates" against actual
// server-side row counts, which is the point of the project.

import { Session } from "../src/transport/session.mjs";
import { TrpcClient } from "../src/transport/client.mjs";
import { isProtected } from "../src/transport/procedures.mjs";
import { NetworkError } from "../src/transport/client.mjs";

let seq = 0;
export const nanoidLike = () => ("fk" + String(++seq).padStart(19, "0")).slice(0, 21);

export class CrashSignal extends Error { constructor(n) { super("crash at call " + n); this.name = "CrashSignal"; } }

const PLACEHOLDER = {
  "jutsu.create": (id) => ({ id, name: `New Jutsu - ${id}`, description: "New jutsu description", hidden: true, effects: [], createdAt: new Date(0), updatedAt: new Date(0) }),
  "item.create": (id, input) => ({ id, name: `New Item - ${id}`, itemType: input?.type ?? "CONSUMABLE", hidden: true, effects: [], createdAt: new Date(0), updatedAt: new Date(0) }),
  "bloodline.create": (id) => ({ id, name: `New Bloodline - ${id}`, hidden: true, effects: [], createdAt: new Date(0), updatedAt: new Date(0) }),
  "gameAsset.create": (id) => ({ id, name: "Placeholder", type: "STATIC", image: "", url: "", hidden: true, createdAt: new Date(0), updatedAt: new Date(0) }),
  "quests.create": (id) => ({ id, name: `New Quest - ${id}`, hidden: true, content: { objectives: [], reward: {}, sceneBackground: "", sceneCharacters: [] }, createdAt: new Date(0), updatedAt: new Date(0) }),
  "profile.create": (id) => ({ userId: id, username: `New AI - ${id}`, isAi: true, level: 1, rank: "STUDENT", aiProfileId: null, jutsus: [], items: [], createdAt: new Date(0), updatedAt: new Date(0) }),
  // routers/badge.ts:124-138 and routers/title.ts:93-110 at 2af4b320
  "badge.create": (id) => ({ id, name: `New Badge - ${id}`, image: "https://utfs.io/f/default-avatar", description: "", createdAt: new Date(0), updatedAt: new Date(0) }),
  "title.create": (id) => ({ id, name: `New Title - ${id}`, description: "", effects: [], legacyOwnerId: null, archived: false, createdAt: new Date(0), updatedAt: new Date(0) }),
};
const TABLE = { jutsu: "jutsu", item: "item", bloodline: "bloodline", gameAsset: "asset", quests: "quest", profile: "ai", ai: "aiProfile", dungeon: "dungeon", petSpecies: "petSpecies", badge: "badge", title: "title" };
const ID_KEY = { ai: "userId" };

/**
 * Rebuild every object in a payload with its keys in a DIFFERENT order, the way zod re-emits a
 * validated document in schema order rather than the order the client sent. Semantically the same
 * document, structurally re-keyed - which is precisely what turned 18 landed Godstorm AI-profile
 * writes into reported "drift" against a JSON.stringify comparison
 * (harvests/inbox/tnr_results_1789829183863.json: every recorded rules diff parses equal).
 * Reversing is the cheapest re-keying that is deterministic and always different for >1 key.
 */
export const rekey = (v) => (Array.isArray(v) ? v.map(rekey)
  : v && typeof v === "object" && !(v instanceof Date)
    ? Object.fromEntries(Object.keys(v).reverse().map((k) => [k, rekey(v[k])]))
    : v);

export class FakeGame {
  constructor({ crashAt = Infinity, dropAt = Infinity, refuse = new Set(), limitPath = null, signedOut = false } = {}) {
    this.tables = { jutsu: new Map(), item: new Map(), bloodline: new Map(), asset: new Map(), quest: new Map(), ai: new Map(), aiProfile: new Map(), dungeon: new Map(), petSpecies: new Map(), badge: new Map(), title: new Map(), itemVariant: new Map() };
    this.calls = [];
    this.crashAt = crashAt;
    // the connection fails at this call BEFORE the server applies it: nothing is written
    this.dropAt = dropAt;
    this.refuse = refuse;        // set of paths that answer success:false
    this.limitPath = limitPath;  // a path that answers TOO_MANY_REQUESTS
    // No Clerk session: every protectedProcedure answers UNAUTHORIZED before its resolver runs,
    // which is what enforceUserIsAuthed does at source (trpc.ts:213-216) and what the two failed
    // Forge 0.3.0 runs saw five times each. Public procedures are unaffected, exactly as they are
    // live: that asymmetry is the thing the auth tests exist to pin down.
    this.signedOut = signedOut;
    this.armed = true;
  }
  signOut() { this.signedOut = true; return this; }
  signIn() { this.signedOut = false; return this; }
  count(entity) { return this.tables[entity].size; }
  rows(entity) { return [...this.tables[entity].values()]; }
  seed(entity, row) { const k = ID_KEY[entity] ?? "id"; this.tables[entity].set(row[k], row); return row; }

  /** Handle one procedure call; returns a decoded element. */
  handle(path, input) {
    const n = this.calls.push({ path, input });
    if (n === this.dropAt) throw new NetworkError("connection reset before the request was applied");
    // Nested routers: root.ts mounts coopRouter at `coop`, and coop.ts mounts dungeonRouter at
    // `dungeon`. A bare "dungeon.*" path does not exist on the server (NOT_FOUND, as live on 2026-10-25).
    const nested = path.startsWith("coop.dungeon.");
    const [router, proc] = nested ? ["dungeon", path.slice("coop.dungeon.".length)] : path.split(".");
    if (!nested && router === "dungeon") return { ok: false, error: { code: "NOT_FOUND", httpStatus: 404, message: `No procedure found on path "${path}"`, path, zodError: null } };
    const table = this.tables[TABLE[router]];
    const ok = (data) => ({ ok: true, data });
    const err = (code, message, httpStatus) => ({ ok: false, error: { code, httpStatus, message, path, zodError: null } });
    let result;
    if (this.limitPath === path) return err("TOO_MANY_REQUESTS", "You are moving too fast! Incident logged for review", 429);
    if (this.signedOut && isProtected(path)) return err("UNAUTHORIZED", `UNAUTHORIZED: Data: ${JSON.stringify(input ?? null)}`, 401);
    if (router === "dungeon") result = this.dungeon(proc, input, ok, err);
    else if (router === "petSpecies") result = this.petSpecies(proc, input, ok, err);
    else if (path === "item.getItemVariants" || path === "item.upsertItemVariant" || path === "item.getVariantNames") result = this.itemVariant(proc, input, ok, err);
    else if (PLACEHOLDER[path]) {
      if (this.refuse.has(path)) result = ok({ success: false, message: `Not allowed to create` });
      else { const id = nanoidLike(); const row = PLACEHOLDER[path](id, input); table.set(id, row); result = ok({ success: true, message: id }); }
    } else if (path === "title.getAll") {
      // routers/title.ts:30-38 at 2af4b320: every catalog title, archived too; legacy labels excluded
      result = ok(this.rows("title").filter((r) => !r.legacyOwnerId).map((r) => structuredClone(r)));
    } else if (proc === "get" || proc === "getAi") {
      const id = input.id ?? input.userId;
      // routers/title.ts:40-50: a per-player legacy label is not a catalog title, NOT_FOUND
      const row = path === "title.get" && table.get(id)?.legacyOwnerId ? null : table.get(id);
      result = row ? ok(structuredClone(row)) : (proc === "getAi" ? ok(null) : err("NOT_FOUND", `${router} not found`, 404));
    } else if (proc === "update" || proc === "updateAi") {
      const row = table.get(input.id);
      if (!row) result = ok({ success: false, message: `${router} not found` });
      else if (this.refuse.has(path)) result = ok({ success: false, message: "Not allowed" });
      // routers/jutsu.ts:1153-1157 at 2af4b320
      // routers/badge.ts:88-89: names are unique
      else if (router === "badge" && [...table.values()].some((r) => r.name === input.data.name && r.id !== input.id)) result = ok({ success: false, message: "Badge name already exists" });
      // server/utils/titleRewards.ts:9-37 (quests.ts:877, item.ts:682): reward_titles must name unarchived catalog titles
      else if ((router === "quests" || router === "item") && [...JSON.stringify(input.data).matchAll(/"reward_titles":\[([^\]]*)\]/g)].flatMap((m) => m[1].match(/[^",]+/g) ?? []).some((t) => !this.tables.title.get(t) || this.tables.title.get(t).archived)) result = ok({ success: false, message: "A reward title is missing, archived or private. Select an available title." });
      else if (router === "jutsu" && input.data.requiredPetSpeciesId && (input.data.jutsuType !== "PETS" || !this.tables.petSpecies.has(input.data.requiredPetSpeciesId))) result = ok({ success: false, message: "Select a valid companion species for a PETS jutsu" });
      else { const { jutsus, items, ...rest } = input.data; Object.assign(row, rest, { updatedAt: new Date(1) });
             if (router === "profile") { if (jutsus) row.jutsus = jutsus.map((j) => ({ jutsuId: j })); if (items) row.items = items.flatMap((t) => t.ids.map((i) => ({ itemId: i, quantity: (row.items ?? []).find((r) => r.itemId === i)?.quantity ?? 1, dropChancePerc: Number(t.number) }))); }
             result = ok({ success: true, message: `Updated ${input.id}` }); }
    } else if (proc === "getAllNames" || proc === "getAllAiNames") {
      // The name lists are NOT input-shape-equivalent. Only gameAsset.getAllNames declares an
      // .input(), z.object({type?, folderPrefix?}), and that object schema is not itself
      // .optional() (45f_DATA_procedures.json, routers/asset.getAllNames @ TheNinjaRPG bdec2883),
      // so an absent input fails zod before the resolver runs. That is the live BAD_REQUEST that
      // killed the three Godstorm Stormcourt asset creates at their pre-create snapshot; the
      // other lists declare no input and ignore whatever arrives.
      if (path === "gameAsset.getAllNames" && (input === null || typeof input !== "object" || Array.isArray(input))) {
        return err("BAD_REQUEST", "[{\"code\":\"invalid_type\",\"expected\":\"object\",\"received\":\"undefined\",\"path\":[],\"message\":\"Required\"}]", 400);
      }
      const k = ID_KEY[TABLE[router]] ?? "id", nk = TABLE[router] === "ai" ? "username" : "name";
      let rows = [...table.values()];
      if (path === "title.getAllNames") rows = rows.filter((r) => !r.archived && !r.legacyOwnerId); // routers/title.ts:23-28
      if (path === "gameAsset.getAllNames" && input.type) rows = rows.filter((r) => r.type === input.type);
      const name = (r) => (path === "gameAsset.getAllNames" && input.folderPrefix ? `${r.folder ?? ""}/${r[nk]}` : r[nk]);
      result = ok(rows.map((r) => ({ [k]: r[k], [nk]: name(r) })));
    } else if (path === "item.getItemWithCraftingRequirements") {
      result = this.itemWithCraftingRequirements(input, ok, err);
    } else if (path === "ai.getAiProfile") {
      const p = this.tables.aiProfile.get(input.id); result = p ? ok(structuredClone(p)) : err("NOT_FOUND", "profile not found", 404);
    } else if (path === "ai.toggleAiProfile") {
      const ai = this.tables.ai.get(input.aiId);
      if (!ai) result = ok({ success: false, message: "AI not found" });
      else if (ai.aiProfileId) { this.tables.aiProfile.delete(ai.aiProfileId); ai.aiProfileId = null; result = ok({ success: true, message: "Profile removed" }); }
      else { const pid = nanoidLike(); this.tables.aiProfile.set(pid, { id: pid, userId: input.aiId, rules: [], includeDefaultRules: true }); ai.aiProfileId = pid; result = ok({ success: true, message: "Profile created" }); }
    } else if (path === "ai.updateAiProfile") {
      const p = this.tables.aiProfile.get(input.id);
      if (!p) result = ok({ success: false, message: "profile not found" });
      // stored as the server stores it: same document, schema key order (see rekey above)
      else { p.rules = rekey(structuredClone(input.rules)); p.includeDefaultRules = input.includeDefaultRules; result = ok({ success: true, message: "Rules updated" }); }
    } else {
      result = err("NOT_FOUND", "unknown procedure " + path, 404);
    }
    // the request was applied server-side; now maybe the tab dies before the response is seen
    if (n >= this.crashAt && this.armed) { this.armed = false; throw new CrashSignal(n); }
    return result;
  }
}

/**
 * coop.dungeon.getAll / coop.dungeon.save as routers/dungeon.ts answers at the pin in src/dungeon/contract.json:
 * getAll returns whole rows {id, content, updatedAt} (an empty list for non-staff); save without
 * an id creates, with an id upserts the WHOLE content, and answers {success, message, id}.
 *
 * The save input is parsed the way saveDungeonSchema parses it, written out here independently of
 * Forge's validator: unknown keys are STRIPPED at every level (zod objects are not strict), the
 * name is trimmed, `.prefault()` defaults fill only undefined members (an explicit null is a
 * BAD_REQUEST), and expiresAt is z.coerce.date(). Then the resolver: every package drop's sent
 * payload is dropped and the CURRENT catalog row (`game.packages`) is copied in; a missing one is
 * refused. The row is stored through JSON (the content column is json), so a Date reads back as
 * its ISO string, in schema key order (rekey).
 */
const DUNGEON_KEYS = {
  content: ["name", "description", "structureAssetId", "structureScale", "sector", "longitude", "latitude", "expiresAt", "hidden", "background", "tiers", "rewards"],
  rewards: ["money", "experience", "tokens", "prestige", "drops"], drop: ["type", "id", "chance", "onlyOnce", "quantity", "package"],
  floor: ["kind", "waves"], wave: ["aiIds", "delayRounds"],
};
class ZodIssue extends Error { constructor(path, message) { super(message); this.path = path; } }
function parseDungeon(content) {
  const pick = (o, keys, where) => {
    if (!o || typeof o !== "object" || Array.isArray(o)) throw new ZodIssue(where, "Expected object");
    return Object.fromEntries(keys.filter((k) => o[k] !== undefined).map((k) => [k, o[k]]));
  };
  const prefault = (o, k, v, where) => { if (o[k] === null) throw new ZodIssue([...where, k], "Expected value, received null"); if (o[k] === undefined) o[k] = v; };
  const c = pick(content, DUNGEON_KEYS.content, ["content"]);
  if (typeof c.name !== "string" || !c.name.trim()) throw new ZodIssue(["content", "name"], "Enter a dungeon name.");
  c.name = c.name.trim();
  for (const [k, v] of [["description", ""], ["structureAssetId", ""], ["structureScale", 1], ["hidden", true], ["background", "default"]]) prefault(c, k, v, ["content"]);
  if (!("expiresAt" in c)) throw new ZodIssue(["content", "expiresAt"], "Required");
  if (c.expiresAt !== null) { const d = new Date(c.expiresAt); if (Number.isNaN(d.getTime())) throw new ZodIssue(["content", "expiresAt"], "Invalid date"); c.expiresAt = d; }
  c.tiers = (c.tiers ?? []).map((t, ti) => t.map((f, fi) => {
    const floor = pick(f, DUNGEON_KEYS.floor, ["content", "tiers", ti, fi]);
    floor.waves = floor.waves.map((w, wi) => { const wave = pick(w, DUNGEON_KEYS.wave, ["content", "tiers", ti, fi, "waves", wi]); prefault(wave, "delayRounds", 0, ["content", "tiers", ti, fi, "waves", wi]); return wave; });
    return floor;
  }));
  c.rewards = pick(c.rewards, DUNGEON_KEYS.rewards, ["content", "rewards"]);
  for (const k of ["money", "experience", "tokens", "prestige"]) prefault(c.rewards, k, 0, ["content", "rewards"]);
  prefault(c.rewards, "drops", [], ["content", "rewards"]);
  c.rewards.drops = c.rewards.drops.map((d, i) => { const drop = pick(d, DUNGEON_KEYS.drop, ["content", "rewards", "drops", i]); prefault(drop, "quantity", 1, ["content", "rewards", "drops", i]); return drop; });
  return c;
}

FakeGame.prototype.dungeon = function (proc, input, ok, err) {
  const table = this.tables.dungeon;
  if (proc === "getAll") return ok(this.notStaff ? [] : [...table.values()].map((r) => structuredClone(r)));
  if (proc !== "save") return err("NOT_FOUND", "unknown procedure dungeon." + proc, 404);
  let c;
  try { c = parseDungeon(input.content); } catch (e) {
    if (!(e instanceof ZodIssue)) throw e;
    return { ok: false, error: { code: "BAD_REQUEST", httpStatus: 400, message: e.message, path: "coop.dungeon.save", zodError: [{ path: e.path, message: e.message }] } };
  }
  if (this.notStaff) return ok({ success: false, message: "You cannot edit dungeons." });
  if (this.refuse.has("coop.dungeon.save")) return ok({ success: false, message: "An enemy or reward no longer exists." });
  const packages = this.packages ?? new Map();
  if (c.rewards.drops.some((d) => d.type === "package" && !packages.has(d.id))) return ok({ success: false, message: "An enemy or reward no longer exists." });
  c.rewards.drops = c.rewards.drops.map(({ package: _ignored, ...d }) => {
    const src = d.type === "package" ? packages.get(d.id) : null;
    return src ? { ...d, package: { name: src.name, description: src.description, rewards: structuredClone(src.rewards) } } : d;
  });
  const id = input.id ?? nanoidLike();
  table.set(id, { id, content: rekey(JSON.parse(JSON.stringify(c))), updatedAt: new Date(1) });
  return ok({ success: true, message: "Dungeon saved.", id });
};

/**
 * petSpecies.* as routers/petSpecies.ts answers at TheNinjaRPG@2af4b320, written out here independently
 * of Forge's pets.mjs: the input is parsed the way PetSpeciesValidator parses it (unknown keys
 * STRIPPED, defaults filled, name/description/rarity/isActive required, defaults unique and within
 * the rarity's slots); create refuses a taken name and any default that is not a published,
 * unlocked PETS jutsu and answers {success, message: <id>}; update {id, data} re-saves the whole
 * parsed record and accepts defaults locked to that species only; get {id}; getAll lists every row.
 */
const PET_KEYS = { name: undefined, description: undefined, artDirection: null, rankConcepts: [], rarity: undefined, role: "ASSAULT",
  preferredDamageElement: null, isActive: undefined, defaultJutsuIds: [], aiRules: [], includeDefaultRules: true, effects: [] };
const PET_SLOTS_AT_SOURCE = { COMMON: 2, UNCOMMON: 3, RARE: 4, EPIC: 5, LEGENDARY: 6 };
FakeGame.prototype.petSpecies = function (proc, input, ok, err) {
  const table = this.tables.petSpecies;
  if (proc === "getAll") return ok([...table.values()].map((r) => structuredClone(r)));
  if (proc === "get") { const r = table.get(input.id); return r ? ok(structuredClone(r)) : err("NOT_FOUND", "Companion species not found", 404); }
  if (proc !== "create" && proc !== "update") return err("NOT_FOUND", "unknown procedure petSpecies." + proc, 404);
  const raw = proc === "create" ? input : input.data;
  const d = {};
  for (const [k, dflt] of Object.entries(PET_KEYS)) {
    if (raw?.[k] !== undefined) d[k] = structuredClone(raw[k]);
    else if (dflt !== undefined) d[k] = structuredClone(dflt);
    else return { ok: false, error: { code: "BAD_REQUEST", httpStatus: 400, message: "Required", path: "petSpecies." + proc, zodError: [{ path: [k], message: "Required" }] } };
  }
  // the validator's transforms (validators/petSpecies.ts:22-48), as the stored row carries them
  for (const k of ["name", "description"]) d[k] = String(d[k]).trim();
  d.artDirection = typeof d.artDirection === "string" && d.artDirection.trim() ? d.artDirection.trim() : null;
  d.rankConcepts = d.rankConcepts.map((c) => (c == null ? "" : String(c).trim()));
  while (d.rankConcepts.length && !d.rankConcepts.at(-1)) d.rankConcepts.pop();
  if (new Set(d.defaultJutsuIds).size !== d.defaultJutsuIds.length || d.defaultJutsuIds.length > PET_SLOTS_AT_SOURCE[d.rarity]) {
    return { ok: false, error: { code: "BAD_REQUEST", httpStatus: 400, message: "defaults", path: "petSpecies." + proc, zodError: [{ path: ["defaultJutsuIds"], message: "defaults" }] } };
  }
  const id = proc === "create" ? null : input.id;
  const named = [...table.values()].find((r) => r.name === d.name);
  if (named && named.id !== id) return ok({ success: false, message: "Companion species name already exists" });
  if (id && !table.has(id)) return ok({ success: false, message: "Companion species not found" });
  const defaults = d.defaultJutsuIds.map((j) => this.tables.jutsu.get(j));
  if (defaults.some((j) => !j || j.hidden || j.jutsuType !== "PETS" || (j.requiredPetSpeciesId && j.requiredPetSpeciesId !== id))) {
    return ok({ success: false, message: "Choose published, compatible PETS jutsu for the default loadout." });
  }
  if (this.refuse.has("petSpecies." + proc)) return ok({ success: false, message: "Not allowed" });
  if (proc === "create") { const nid = nanoidLike(); table.set(nid, { id: nid, ...d, createdAt: new Date(0), updatedAt: new Date(0) }); return ok({ success: true, message: nid }); }
  Object.assign(table.get(id), d, { updatedAt: new Date(1) });
  return ok({ success: true, message: "Companion species updated." });
};

/** A Session-less TrpcClient stand-in with the same batch()/call() surface, backed by FakeGame. */
export class FakeClient {
  constructor(game) { this.game = game; }
  async call(path, input) { const [r] = await this.batch([{ path, input }]); return r; }
  async batch(calls) { return calls.map((c) => this.game.handle(c.path, c.input)); }
}

/**
 * item.getItemWithCraftingRequirements as routers/item.ts:400 answers at TheNinjaRPG@2af4b320:
 * fetchItemWithCraftingRequirements (item.ts:4094) is item.findFirst({with: {craftingRequirements:
 * {with: {requirementItem: true}}, requiredBloodline: true}}), and a missing item THROWS NOT_FOUND
 * ("Item not found") rather than answering null as item.get does. Recipe rows are seeded with
 * seedCraftingRequirement() and live beside the item table, as the CraftingRequirement table does.
 */
FakeGame.prototype.seedCraftingRequirement = function (row) {
  (this.craftingRequirements ??= []).push(row);
  return row;
};
FakeGame.prototype.itemWithCraftingRequirements = function (input, ok, err) {
  const row = this.tables.item.get(input?.id);
  if (!row) return err("NOT_FOUND", "Item not found", 404);
  const craftingRequirements = (this.craftingRequirements ?? [])
    .filter((r) => r.craftItemId === row.id)
    .map((r) => ({ ...structuredClone(r), requirementItem: structuredClone(this.tables.item.get(r.requirementItemId) ?? null) }));
  const requiredBloodline = row.bloodlineId ? structuredClone(this.tables.bloodline.get(row.bloodlineId) ?? null) : null;
  return ok({ ...structuredClone(row), craftingRequirements, requiredBloodline });
};

export { Session, TrpcClient };

/**
 * item.getItemVariants / item.upsertItemVariant (and item.getVariantNames, routers/item.ts:1150) as routers/item.ts:1151-1275 answers at
 * TheNinjaRPG@3314d122, written out here independently of src/runner/variants.mjs. getItemVariants
 * {itemId} lists that item's rows by order. upsertItemVariant {itemId, variant} parses
 * ItemVariantValidator (unknown keys stripped, name trimmed, requiredItemId/furnitureData prefault
 * null), refuses before writing (item / required item missing, a required item on a non-token cost,
 * a required item whose unlockitemvariant has a variantId other than this variant's, furniture data
 * on a non-furniture item, 7 variants, a taken order), then inserts with a fresh id - answering
 * "Variant saved" and NO id - or replaces every column of {id, itemId}. description is stored null
 * when absent.
 */
const VARIANT_COSTS = ["MONEY", "REPUTATION", "SEICHI_SILVER", "VILLAGE_PRESTIGE", "VARIANT_TOKEN"];
FakeGame.prototype.itemVariant = function (proc, input, ok, err) {
  const table = this.tables.itemVariant, items = this.tables.item;
  const listOf = (itemId) => [...table.values()].filter((v) => v.itemId === itemId).sort((a, b) => a.order - b.order);
  if (proc === "getItemVariants") return ok(listOf(input.itemId).map((v) => structuredClone(v)));
  // queries/item.ts:2350 listVariantNames: no input; {id, "<item>: <variant>"} for VARIANT_TOKEN
  // rows inner-joined to their item (a variant whose item is gone is not listed); no ORDER BY.
  if (proc === "getVariantNames") return ok([...table.values()].filter((v) => v.costType === "VARIANT_TOKEN" && items.has(v.itemId)).map((v) => ({ id: v.id, name: `${items.get(v.itemId).name}: ${v.name}` })));
  const bad = (path, message) => ({ ok: false, error: { code: "BAD_REQUEST", httpStatus: 400, message, path: "item.upsertItemVariant", zodError: [{ path: ["variant", path], message }] } });
  const v = input.variant ?? {};
  const name = typeof v.name === "string" ? v.name.trim() : null;
  if (!name) return bad("name", "Name required");
  if (typeof v.image !== "string" || !v.image) return bad("image", "Image required");
  const req = v.requiredItemId == null ? null : String(v.requiredItemId).trim();
  if (req === "") return bad("requiredItemId", "Too small");
  if (!VARIANT_COSTS.includes(v.costType)) return bad("costType", "Invalid option");
  const cost = Number(v.cost), order = Number(v.order);
  if (!Number.isInteger(cost) || cost < 0) return bad("cost", "Invalid cost");
  if (!Number.isInteger(order) || order < 1 || order > 7) return bad("order", "Invalid order");
  for (const k of ["description", "battleDescription"]) if (v[k] !== undefined && typeof v[k] !== "string") return bad(k, "Expected string");
  if (this.refuse.has("item.upsertItemVariant")) return ok({ success: false, message: "Not allowed" });
  const parent = items.get(input.itemId), required = req ? items.get(req) : undefined;
  const existing = listOf(input.itemId);
  if (!parent) return ok({ success: false, message: "Item not found" });
  if (req && !required) return ok({ success: false, message: "Required unlock item not found" });
  if (req && v.costType !== "VARIANT_TOKEN") return ok({ success: false, message: "Only token variants can require an unlock item" });
  if (required && !(required.effects ?? []).some((e) => e.type === "unlockitemvariant" && (!e.variantId || e.variantId === v.id))) return ok({ success: false, message: "Required unlock item cannot unlock this variant" });
  if (parent.itemType !== "FURNITURE" && v.furnitureData) return ok({ success: false, message: "Only furniture variants can define orientation images" });
  if (!v.id && existing.length >= 7) return ok({ success: false, message: "Items can have at most 7 variants" });
  const clash = existing.find((r) => r.order === order && r.id !== v.id);
  if (clash) return ok({ success: false, message: `Order ${order} is already used by "${clash.name}"` });
  const row = { itemId: input.itemId, name, image: v.image, requiredItemId: req, costType: v.costType, cost, order,
    description: v.description ?? null, battleDescription: v.battleDescription ?? null, furnitureData: v.furnitureData ?? null, updatedAt: new Date(1) };
  if (v.id) {
    const cur = table.get(v.id);
    if (!cur || cur.itemId !== input.itemId) return ok({ success: false, message: "Variant or required item changed — refresh and try again" });
    Object.assign(cur, row);
  } else {
    const id = nanoidLike();
    table.set(id, { id, ...row, createdAt: new Date(0) });
  }
  return ok({ success: true, message: "Variant saved" });
};
