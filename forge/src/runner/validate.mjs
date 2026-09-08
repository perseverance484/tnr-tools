// Pre-send validation (spec section 9, R3). Every content validator on the server is
// non-strict: an unknown or misspelled key is dropped at .input() parse time with no error
// and the mutation reports success. The only place that error can surface is here.
//
// Field sets come from src/runner/fields.json, derived from the PINNED validators by
// tools/derive_fields.mjs (jutsu, item, bloodline, quest, gameAsset, and ai). 45d_DATA_entity_schemas
// (generated 2026-08-26) is stale against 345d18ac: it lacks the twelve item farm* keys and
// quest.requiredFarmingLevel, and ItemValidator REQUIRES farmYieldItemId, so an item update
// picked by the 45d set would be refused by zod. Both files share one shape; the constructor
// accepts either. The AI record has no entity list (insertAiSchema is the whole userData
// table); its key surface is derived instead from createInsertSchema(userData).omit().extend()
// at drizzle/schema.ts:2577, so an AI create is validated BEFORE the placeholder is minted.
// Waiting for a live row to learn the key set (the earlier behaviour) meant a typed key cost a
// live row: profile.create mints the placeholder first, and only _fill could then reject it.
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

// `hidden` is not a userData column and insertAiSchema does not extend it, so the server strips
// it. The repository rule (validate.py check_entry, law 16b) is that EVERY create carries
// hidden:true, "where the column does not exist the key is stripped harmlessly" - so a Lane B
// manifest written for the current builder carries it on an ai create too. Refusing it as an
// unknown key would reject a manifest for obeying the repo's own rule, so it is accepted here,
// dropped by the pinned-field merge before the send, and excluded from the read-back diff.
export const AI_STRIPPED_OK = Object.freeze(["hidden"]);

// Keys the server owns. Sending them is harmless (stripped) but they are never "asserted".
export const SERVER_OWNED = Object.freeze(["id", "userId", "createdAt", "updatedAt", "aiProfileId"]);

// Columns insertAiSchema .omit()s (drizzle/schema.ts:2578-2592): the server strips them silently.
export const AI_OMITTED = Object.freeze([
  "trainingStartedAt", "occupationSignupAt", "currentlyTraining", "deletionAt", "travelFinishAt",
  "questData", "occupation", "stealthActivatedAt", "stealthCooldownAt", "lastSensoryAt",
  "covertTrainingType", "covertTrainingStartedAt", "covertTrainingMinutes",
]);

/** Which 45d entity backs a manifest entity. */
export const SCHEMA_ENTITY = Object.freeze({ jutsu: "jutsu", item: "item", bloodline: "bloodline", quest: "quest", asset: "gameAsset", ai: "ai" });

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
      const allowed = new Set([...AI_EXTRA_KEYS, ...AI_STRIPPED_OK]);
      if (entity === "ai") {
        const pinned = this.knownFields("ai"); // insertAiSchema at the pin: known without a live row
        if (!pinned) out.push("no pinned insertAiSchema field set: cannot validate ai keys");
        else for (const k of pinned) allowed.add(k);
      }
      if (live) for (const k of Object.keys(live)) allowed.add(k);
      for (const k of AI_OMITTED) allowed.delete(k);
      for (const k of SERVER_OWNED) allowed.delete(k);
      const check = entity === "aiProfile" ? new Set(["rules", "includeDefaultRules"]) : allowed;
      // omitted and server-owned columns are refused even before a create (no live row needed)
      for (const k of keys) if (AI_OMITTED.includes(k) || (entity === "ai" && SERVER_OWNED.includes(k))) out.push(`"${k}" is not writable on an ai (insertAiSchema omits it or the server owns it)`);
      // every unknown key is refused BEFORE the create, because the pinned set does not need a live row
      for (const k of keys) if (!check.has(k) && !AI_OMITTED.includes(k) && !SERVER_OWNED.includes(k)) out.push(`unknown key "${k}" for ${entity}`);
      if (entity === "ai" && Array.isArray(data.items)) for (const t of data.items) if (t && typeof t === "object" && !Array.isArray(t.ids) && t.itemId == null && t.id == null) out.push("items: each entry is {ids: [itemId], number: dropChancePerc} (law 69)");
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
    if (entity === "ai" && AI_STRIPPED_OK.includes(k)) continue; // never reaches the server; see AI_STRIPPED_OK
    if (entity === "ai" && k === "jutsus") { // live row carries relation rows; compare ids
      const l = Array.isArray(live?.jutsus) ? live.jutsus.map((r) => (typeof r === "string" ? r : r.jutsuId ?? r.id)) : [];
      const s = (asserted.jutsus ?? []).map((j) => (typeof j === "string" ? j : j?.jutsuId ?? j?.id));
      if (JSON.stringify([...s].sort()) !== JSON.stringify([...l].sort())) diffs.push({ key: k, sent: s, live: l });
      continue;
    }
    if (entity === "ai" && k === "items") {
      // ids AND drop chances: number is written to userItem.dropChancePerc (law 69)
      const lm = new Map(); if (Array.isArray(live?.items)) for (const r of live.items) { if (typeof r === "string") lm.set(r, null); else if (r) lm.set(r.itemId ?? r.id, r.dropChancePerc ?? null); }
      const sm = new Map(); for (const t of asserted.items ?? []) { if (typeof t === "string") sm.set(t, null); else if (t && Array.isArray(t.ids)) for (const id of t.ids) sm.set(id, t.number == null ? null : Number(t.number)); else if (t) sm.set(t.itemId ?? t.id, t.number == null ? null : Number(t.number)); }
      const l = [...lm.keys()].filter(Boolean), s = [...sm.keys()].filter(Boolean);
      const chanceDrift = s.some((id) => sm.get(id) != null && lm.has(id) && lm.get(id) != null && Number(lm.get(id)) !== sm.get(id));
      if (chanceDrift) diffs.push({ key: "items.dropChancePerc", sent: Object.fromEntries(sm), live: Object.fromEntries(lm) });
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
