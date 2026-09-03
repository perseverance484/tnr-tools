// Pre-send validation (spec section 9, R3). Every content validator on the server is
// non-strict: an unknown or misspelled key is dropped at .input() parse time with no error
// and the mutation reports success. The only place that error can surface is here.
//
// Field sets come from 45d_DATA_entity_schemas.json (jutsu, item, bloodline, quest,
// gameAsset). The AI record has no 45d entity (insertAiSchema is the whole userData table),
// so AI keys are checked against the live record fetched before the write, plus the small
// extension set the schema adds.
//
// DELIBERATELY NOT WIRED: 45g.tag_power_max. Brief section 5: at source PowerAttributes.power
// is z.coerce.number().min(0) with no maximum, spread after BaseAttributes in all 61 tags that
// use it; 45g asserts a cap of 100 that the server does not impose, because schema_extract.py
// does not handle spread precedence. Wiring it would make this client reject payloads the
// server accepts. 45g is not loaded by this module at all. The bound is gated out until the
// generator is fixed; see docs/BUILDER_APP_NOTES.md.

export class ValidationError extends Error {
  constructor(message, problems) { super(message); this.name = "ValidationError"; this.problems = problems; }
}

// insertAiSchema extensions beyond the userData columns (drizzle/schema.ts:2593-2624) plus the
// rules envelope the runner routes to ai.updateAiProfile.
export const AI_EXTRA_KEYS = Object.freeze(["jutsus", "items", "primaryElement", "secondaryElement", "rules", "includeDefaultRules"]);

// Keys the server owns. Sending them is harmless (stripped) but they are never "asserted".
export const SERVER_OWNED = Object.freeze(["id", "userId", "createdAt", "updatedAt", "aiProfileId"]);

/** Which 45d entity backs a manifest entity. */
export const SCHEMA_ENTITY = Object.freeze({ jutsu: "jutsu", item: "item", bloodline: "bloodline", quest: "quest", asset: "gameAsset" });

export class Validator {
  /** @param {object} schemas  the parsed 45d file ({entities: {name: {fields: {...}}}}) or null */
  constructor(schemas) {
    this.fields = {};
    const ents = schemas && schemas.entities ? schemas.entities : {};
    for (const [name, e] of Object.entries(ents)) {
      if (e && e.fields && typeof e.fields === "object") this.fields[name] = new Set(Object.keys(e.fields));
    }
    this.schemaMissing = Object.keys(this.fields).length === 0;
  }

  knownFields(entity) {
    const s = SCHEMA_ENTITY[entity];
    return s ? this.fields[s] ?? null : null;
  }

  /**
   * Validate the ASSERTED keys of one item's data before merge and send.
   * @param {string} entity   manifest entity
   * @param {object} data     the manifest's data (refs already resolved)
   * @param {object|null} live  the live record when known (required for ai)
   * @returns {string[]} problems (empty = ok)
   */
  problems(entity, data, live = null, { preCreate = false } = {}) {
    const out = [];
    if (!data || typeof data !== "object") return ["data is not an object"];
    const keys = Object.keys(data);
    if (entity === "ai" || entity === "aiProfile") {
      const allowed = new Set(AI_EXTRA_KEYS);
      if (live) for (const k of Object.keys(live)) allowed.add(k);
      const check = entity === "aiProfile" ? new Set(["rules", "includeDefaultRules"]) : allowed;
      // before a create there is no live row to check AI keys against; structural checks only
      if (live || entity === "aiProfile") for (const k of keys) if (!check.has(k)) out.push(`unknown key "${k}" for ${entity}`);
      if (Array.isArray(data.rules)) out.push(...ruleProblems(data.rules));
    } else {
      const known = this.knownFields(entity);
      if (!known) out.push(`no field schema for entity ${entity}`);
      else for (const k of keys) if (!known.has(k) && !SERVER_OWNED.includes(k)) out.push(`unknown key "${k}" for ${entity} (would be silently dropped by the server)`);
    }
    // law 46 / empty_string_rule: '' becomes null on the write path; for image that 500s.
    if (data.image === "") out.push('image is an empty string: omit the key so fetch-merge keeps the current value');
    // law 45: doubled prefix
    for (const [k, v] of Object.entries(data)) if (typeof v === "string" && /^@\w+:@\w+:/.test(v)) out.push(`${k}: doubled ref prefix`);
    return out;
  }
}

function ruleProblems(rules) {
  const out = [];
  rules.forEach((r, i) => {
    if (!r || typeof r !== "object") { out.push(`rules[${i}] is not an object`); return; }
    if (!Array.isArray(r.conditions)) out.push(`rules[${i}].conditions must be an array`);
    if (!r.action || typeof r.action !== "object" || typeof r.action.type !== "string") out.push(`rules[${i}].action must be a tagged object with type`);
    for (const c of r.conditions || []) if (!c || typeof c.type !== "string") out.push(`rules[${i}] has a condition without type`);
    const extra = Object.keys(r).filter((k) => !["conditions", "action"].includes(k));
    if (extra.length) out.push(`rules[${i}] has keys outside {conditions, action}: ${extra.join(", ")} (law 16d: no flat triple)`);
  });
  return out;
}

/**
 * Diff only the keys the manifest asserted (spec section 8, R6). Returns [{key, sent, live}].
 * `''` sent vs null live is equal (server normalises empty strings to null on nullable columns).
 * Numbers within 0.5 are equal for ai (scaleUserStats re-normalises on every write, law 71).
 */
export function diffAsserted(entity, asserted, live) {
  const diffs = [];
  for (const k of Object.keys(asserted)) {
    if (SERVER_OWNED.includes(k)) continue;
    if (entity === "ai" && ["rules", "includeDefaultRules"].includes(k)) continue; // verified via the profile read
    if (entity === "ai" && k === "jutsus") { // live row carries relation rows; compare ids
      const l = Array.isArray(live?.jutsus) ? live.jutsus.map((r) => (typeof r === "string" ? r : r.jutsuId ?? r.id)) : [];
      const s = (asserted.jutsus ?? []).map((j) => (typeof j === "string" ? j : j?.jutsuId ?? j?.id));
      if (JSON.stringify([...s].sort()) !== JSON.stringify([...l].sort())) diffs.push({ key: k, sent: s, live: l });
      continue;
    }
    if (entity === "ai" && k === "items") {
      const l = Array.isArray(live?.items) ? live.items.map((r) => (typeof r === "string" ? r : r.itemId ?? r.id)).filter(Boolean) : [];
      const s = (asserted.items ?? []).flatMap((t) => (typeof t === "string" ? [t] : Array.isArray(t?.ids) ? t.ids : [t?.itemId ?? t?.id])).filter(Boolean);
      if (JSON.stringify([...s].sort()) !== JSON.stringify([...l].sort())) diffs.push({ key: k, sent: s, live: l });
      continue;
    }
    const s = asserted[k], l = live ? live[k] : undefined;
    if (!eqLoose(s, l, entity)) diffs.push({ key: k, sent: s, live: l });
  }
  return diffs;
}

function eqLoose(a, b, entity) {
  if (a === b) return true;
  if ((a === "" && b == null) || (a == null && b === "")) return true;
  if (a instanceof Date || b instanceof Date) return new Date(a).getTime() === new Date(b).getTime();
  if (typeof a === "number" && typeof b === "number") return entity === "ai" ? Math.abs(a - b) <= 0.5 : a === b;
  if (Array.isArray(a) && Array.isArray(b)) return a.length === b.length && a.every((x, i) => eqLoose(x, b[i], entity));
  if (a && b && typeof a === "object" && typeof b === "object") {
    const ka = Object.keys(a);
    return ka.every((k) => eqLoose(a[k], b[k], entity));
  }
  return false;
}
