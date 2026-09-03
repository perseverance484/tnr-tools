// Manifest parsing and planning. Accepts the shapes committed under push/: a top-level
// `items` (legacy `jutsu`) array, optional `capture {before, after}`, `_note`, `skipPreflight`,
// `dedupNames`, `readBack`, `imgSizes`. Each item is {entity, slot, name, srcId?, targetId?,
// data, phase?}. slot "create" creates; "edit" and "convert" both update.
//
// Planning produces an ORDERED list of item specs for the journal. Order is manifest order,
// except that an item referencing @entity:key must come after the item whose srcId is key,
// so refs resolve from ids minted earlier in the same job (topological sort, stable).

import { payloadHash, stableStringify, fnv1a32 } from "../storage/hash.mjs";
import { collectRefs, REF_RE } from "./refs.mjs";

export const ENTITIES = Object.freeze(["jutsu", "item", "bloodline", "asset", "quest", "ai", "aiProfile"]);
const SLOT_TO_OP = Object.freeze({ create: "create", edit: "update", convert: "update" });

export class ManifestError extends Error {
  constructor(message, info = {}) { super(message); this.name = "ManifestError"; Object.assign(this, info); }
}

/** Parse text or object into a normalized manifest. Throws ManifestError on structural problems. */
export function parseManifest(source) {
  let m = source;
  if (typeof source === "string") {
    try { m = JSON.parse(source); } catch (e) { throw new ManifestError("manifest is not JSON: " + e.message); }
  }
  if (!m || typeof m !== "object" || Array.isArray(m)) throw new ManifestError("manifest must be an object");
  const raw = Array.isArray(m.items) ? m.items : Array.isArray(m.jutsu) ? m.jutsu : [];
  const capture = m.capture && typeof m.capture === "object"
    ? { before: Array.isArray(m.capture.before) ? m.capture.before : [], after: Array.isArray(m.capture.after) ? m.capture.after : [] }
    : { before: [], after: [] };
  for (const c of [...capture.before, ...capture.after]) {
    if (!c || typeof c !== "object" || !(c.proc || c.procedure)) throw new ManifestError("capture entry missing proc");
  }
  if (!raw.length && !capture.before.length && !capture.after.length) throw new ManifestError("manifest has no items and no captures");

  const items = raw.map((it, i) => normalizeItem(it, i));
  const problems = [];
  const srcIds = new Set();
  for (const it of items) {
    if (it.op === "create" && !it.srcId) problems.push(`item ${it.idx} (${it.name}): a create needs srcId`);
    if (it.op === "update" && !it.targetId) problems.push(`item ${it.idx} (${it.name}): an edit needs targetId`);
    if (it.srcId) { if (srcIds.has(it.srcId)) problems.push(`duplicate srcId ${it.srcId}`); srcIds.add(it.srcId); }
    if (it.entity === "aiProfile" && it.op === "create") problems.push(`item ${it.idx}: aiProfile cannot be created directly; create an ai with rules`);
  }
  if (problems.length) throw new ManifestError("manifest problems:\n" + problems.join("\n"), { problems });

  return {
    items, capture,
    note: typeof m._note === "string" ? m._note : null,
    skipPreflight: !!m.skipPreflight,
    dedupNames: !!m.dedupNames,
    readBack: m.readBack !== false,
    imgSizes: (m.imgSizes && typeof m.imgSizes === "object") ? m.imgSizes : {},
    hash: fnv1a32(stableStringify({ items: raw, capture })),
  };
}

function normalizeItem(it, idx) {
  if (!it || typeof it !== "object") throw new ManifestError(`item ${idx} is not an object`);
  const entity = it.entity || "jutsu";
  if (!ENTITIES.includes(entity)) throw new ManifestError(`item ${idx}: unknown entity "${entity}"`, { idx, entity });
  const slot = it.slot || (it.targetId ? "edit" : "create");
  const op = SLOT_TO_OP[slot];
  if (!op) throw new ManifestError(`item ${idx}: unknown slot "${slot}"`, { idx, slot });
  const data = it.data && typeof it.data === "object" ? it.data : {};
  if (typeof it.name === "string" && op === "create" && entity !== "aiProfile") {
    // Law 36: the entry-level name is metadata the server never sees. A create without the
    // name in data would land with the placeholder name, so mirror it down explicitly. The
    // AI record's name column is username (userData), every other entity's is name.
    const nameKey = entity === "ai" ? "username" : "name";
    if (data[nameKey] === undefined) data[nameKey] = it.name;
  }
  return {
    idx, entity, op, slot,
    name: typeof it.name === "string" ? it.name : (data.name ?? data.username ?? `item ${idx}`),
    srcId: typeof it.srcId === "string" && it.srcId ? it.srcId : null,
    targetId: typeof it.targetId === "string" && it.targetId ? it.targetId : null,
    phase: typeof it.phase === "number" ? it.phase : null,
    data,
  };
}

/**
 * Order items so every @ref resolves from an earlier item or the idmap. Returns the ordered
 * array of items with `deps` (srcIds referenced). Throws on an unknown ref or a cycle.
 * @param {object} manifest  from parseManifest
 * @param {object} idmap     already-known srcId -> id (compat idmap), consulted so refs to
 *                           earlier jobs' creates are not treated as unknown
 */
export function planOrder(manifest, idmap = {}) {
  const bySrc = new Map(manifest.items.filter((it) => it.srcId).map((it) => [it.srcId, it]));
  const nodes = manifest.items.map((it) => {
    const refs = collectRefs({ data: it.data, targetId: it.targetId });
    const deps = [];
    for (const r of refs) {
      if (r.pfx === "img") continue; // images are uploaded, not created as items
      if (idmap[r.key]) continue;
      const src = bySrc.get(r.key);
      if (!src) throw new ManifestError(`item ${it.idx} (${it.name}): @${r.pfx}:${r.key} is unknown (no srcId in this manifest, not in idmap)`, { idx: it.idx, ref: r });
      if (src.idx === it.idx) throw new ManifestError(`item ${it.idx} references itself`);
      deps.push(src.srcId);
    }
    return { it, deps };
  });
  // explicit numeric phases win, then manifest order; refs enforce a partial order on top
  const order = [];
  const state = new Map(); // srcId -> 'visiting' | 'done'
  const byIdx = new Map(nodes.map((n) => [n.it.idx, n]));
  const sorted = [...nodes].sort((a, b) => (a.it.phase ?? 5) - (b.it.phase ?? 5) || a.it.idx - b.it.idx);
  function visit(n, stack) {
    const key = n.it.srcId ?? `#${n.it.idx}`;
    if (state.get(key) === "done") return;
    if (state.get(key) === "visiting") throw new ManifestError("ref cycle: " + [...stack, key].join(" -> "));
    state.set(key, "visiting");
    for (const d of n.deps) visit(byIdx.get(bySrc.get(d).idx), [...stack, key]);
    state.set(key, "done");
    order.push({ ...n.it, deps: n.deps });
  }
  for (const n of sorted) visit(n, []);
  return order;
}

/** Journal item specs from an ordered plan. */
export function toJournalSpecs(order) {
  return order.map((it) => ({
    entity: it.entity, op: it.op, name: it.name, srcId: it.srcId, targetId: it.targetId,
    payloadHash: payloadHash({ data: it.data, targetId: it.targetId, entity: it.entity, op: it.op }),
  }));
}

export { REF_RE };
