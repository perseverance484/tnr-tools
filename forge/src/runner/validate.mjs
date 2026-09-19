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

/**
 * Restore the per-discriminator key sets from nested.json's shared key-set table.
 *
 * The 165 allowed key sets at the pin are only 53 distinct arrays - every "absorb"-shaped effect
 * tag allows the same keys - so the file stores each one ONCE in `sets` and every section names it
 * by index. That is a storage encoding of the same contract, not a different contract: the
 * expansion below is asserted byte-for-byte against the pre-compaction content in
 * test/runner.test.mjs, which is the gate that keeps the two equivalent.
 *
 * FAILS CLOSED, and that matters more than the bytes it saves: an index this file does not define,
 * a missing table, a section that is neither an index nor a map of them - any of those returns
 * null, and a null nested surface makes the Validator refuse every nested writable structure
 * rather than send it unchecked. A half-expanded table would be worse than no table at all.
 *
 * @param {object|null} raw  the parsed src/runner/nested.json
 * @returns {object|null} {effects: {type: [keys]}, ...} or null when the table cannot be trusted
 */
export function expandNested(raw) {
  if (!raw || typeof raw !== "object" || !Array.isArray(raw.sets) || !raw.effects) return null;
  const at = (i) => (Number.isInteger(i) && i >= 0 && i < raw.sets.length && Array.isArray(raw.sets[i]) ? raw.sets[i] : null);
  const out = {};
  for (const [section, v] of Object.entries(raw)) {
    if (section === "_meta" || section === "sets") continue;
    if (typeof v === "number") {
      const set = at(v);
      if (!set) return null;
      out[section] = set;
      continue;
    }
    if (!v || typeof v !== "object" || Array.isArray(v)) return null;
    const byValue = {};
    for (const [discriminator, i] of Object.entries(v)) {
      const set = at(i);
      if (!set) return null;
      byValue[discriminator] = set;
    }
    out[section] = byValue;
  }
  return out.effects ? out : null;
}

export class Validator {
  /**
   * @param {object} schemas  the parsed field file ({entities: {name: {fields: {...}}}}) or null
   * @param {object} [nested] src/runner/nested.json: the nested key surface derived from the same
   *   pin by tools/derive_nested.mjs, in its shared key-set encoding. Without it, nested checking
   *   FAILS CLOSED: a manifest that carries any nested writable structure is refused rather than
   *   sent unchecked - and so does a table expandNested() cannot trust.
   */
  constructor(schemas, nested = null) {
    this.nested = expandNested(nested);
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
    out.push(...this.nestedProblems(entity, data));
    // law 46 / empty_string_rule: '' becomes null on the write path; for image that 500s.
    if (data.image === "") out.push('image is an empty string: omit the key so fetch-merge keeps the current value');
    // law 45: doubled prefix
    for (const [k, v] of Object.entries(data)) if (typeof v === "string" && /^@\w+:@\w+:/.test(v)) out.push(`${k}: doubled ref prefix`);
    return out;
  }

  /**
   * Unknown keys INSIDE the writable nested structures (readiness brief section 6).
   *
   * Every one of these is parsed by a zod object, and a zod object strips what it does not know,
   * so a misspelled key inside an effect tag, a quest objective or an AI rule is dropped silently
   * and the mutation still answers success. The allowed key sets come from src/runner/nested.json,
   * derived from the SAME pin as fields.json by tools/derive_nested.mjs.
   *
   * Keys only, never bounds: a bound the generator got wrong is the 45g.tag_power_max mistake, and
   * a client that rejects payloads the server accepts is worse than one that does not.
   *
   * Fail closed: with no nested.json, or for a discriminator value the pin does not define, the
   * structure is refused rather than sent unchecked.
   */
  nestedProblems(entity, data) {
    const out = [];
    if (!data || typeof data !== "object") return out;
    // an EMPTY nested structure carries nothing to check, so it is not a reason to fail closed
    const families = [];
    if (Array.isArray(data.effects) && data.effects.length) families.push("effects");
    if (entity === "quest" && data.content && typeof data.content === "object" && Object.keys(data.content).length) families.push("quest content");
    if ((entity === "ai" || entity === "aiProfile") && Array.isArray(data.rules) && data.rules.length) families.push("ai rules");
    if (!families.length) return out;
    if (!this.nested) return [`no derived nested key set: refusing to send ${families.join(", ")} unchecked`];

    const check = (obj, allowed, where) => {
      for (const k of Object.keys(obj)) {
        if (allowed.includes(k)) continue;
        out.push(`${where}: unknown key "${k}" (the server's validator would drop it silently)`);
      }
    };

    for (const [i, f] of (Array.isArray(data.effects) ? data.effects : []).entries()) {
      if (!f || typeof f !== "object") { out.push(`effects[${i}] is not an object`); continue; }
      const allowed = typeof f.type === "string" ? this.nested.effects[f.type] : null;
      if (!allowed) { out.push(`effects[${i}]: unknown effect type ${JSON.stringify(f.type)} at the pin`); continue; }
      check(f, allowed, `effects[${i}] (${f.type})`);
    }

    if (entity === "quest" && data.content && typeof data.content === "object") {
      check(data.content, this.nested.questContent, "content");
      if (data.content.reward && typeof data.content.reward === "object") {
        check(data.content.reward, this.nested.objectiveReward, "content.reward");
      }
      for (const [i, o] of (Array.isArray(data.content.objectives) ? data.content.objectives : []).entries()) {
        if (!o || typeof o !== "object") { out.push(`content.objectives[${i}] is not an object`); continue; }
        const allowed = typeof o.task === "string" ? this.nested.objectives[o.task] : null;
        if (!allowed) { out.push(`content.objectives[${i}]: unknown task ${JSON.stringify(o.task)} at the pin`); continue; }
        const where = `content.objectives[${i}] (${o.task})`;
        check(o, allowed, where);
        if (Array.isArray(o.nextObjectiveId)) {
          for (const [j, c] of o.nextObjectiveId.entries()) {
            if (c && typeof c === "object") check(c, this.nested.objectiveChoice, `${where}.nextObjectiveId[${j}]`);
          }
        }
        for (const key of ["opponentAIs", "attackers"]) {
          for (const [j, e] of (Array.isArray(o[key]) ? o[key] : []).entries()) {
            if (e && typeof e === "object") check(e, this.nested.idsWithNumber, `${where}.${key}[${j}]`);
          }
        }
      }
    }

    if ((entity === "ai" || entity === "aiProfile") && Array.isArray(data.rules)) {
      for (const [i, r] of data.rules.entries()) {
        if (!r || typeof r !== "object") continue; // shape is reported by ruleProblems()
        for (const [j, c] of (Array.isArray(r.conditions) ? r.conditions : []).entries()) {
          if (!c || typeof c !== "object") continue;
          const allowed = typeof c.type === "string" ? this.nested.aiConditions[c.type] : null;
          if (!allowed) { out.push(`rules[${i}].conditions[${j}]: unknown condition type ${JSON.stringify(c.type)} at the pin`); continue; }
          check(c, allowed, `rules[${i}].conditions[${j}] (${c.type})`);
        }
        const a = r.action;
        if (a && typeof a === "object") {
          const allowed = typeof a.type === "string" ? this.nested.aiActions[a.type] : null;
          if (!allowed) out.push(`rules[${i}].action: unknown action type ${JSON.stringify(a.type)} at the pin`);
          else check(a, allowed, `rules[${i}].action (${a.type})`);
        }
      }
    }
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
 * Deep equality for a payload the SERVER rebuilds before storing it.
 *
 * Two normalisations, and only two:
 *
 *   key order is not meaning.  A rules payload is validated by zod and re-emitted in SCHEMA key
 *     order, so a condition sent as {type, value, target, description} reads back as
 *     {type, description, value, target}. Comparing those with JSON.stringify calls a landed
 *     write drift; it did, for all 18 Godstorm AI-profile corrections, whose exported sent and
 *     live payloads parse to identical objects
 *     (harvests/inbox/tnr_results_1789829183863.json).
 *   a key carrying `undefined` is a key that is not there.  Neither survives the wire - superjson
 *     drops it, zod strips it - so asserting one against the other asserts against nothing.
 *
 * EVERYTHING ELSE STAYS STRICT, because that is where real drift lives:
 *   - array order is meaning: rule order decides which rule fires first, so a reordered rules
 *     array is drift;
 *   - a key present on one side with a real value and absent on the other is drift, in BOTH
 *     directions. `null` is a real value the server stores and is not the same as absent;
 *   - values are compared by type and value: 1 is not "1", 0 is not false.
 *
 * This is deliberately NOT eqLoose(): eqLoose compares an asserted field against a live DB ROW,
 * where the live side legitimately carries server-owned columns nobody asserted, and it applies
 * the ai numeric tolerance (law 71). A rules payload is a closed document that was sent whole
 * and read back whole, so nothing about it may be one-sided.
 */
export function deepEqualPayload(a, b) {
  if (a === b) return true;
  if (typeof a === "number" && typeof b === "number") return Number.isNaN(a) && Number.isNaN(b);
  if (a instanceof Date || b instanceof Date) {
    return a instanceof Date && b instanceof Date && a.getTime() === b.getTime();
  }
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    return a.every((x, i) => deepEqualPayload(x, b[i]));
  }
  if (a && b && typeof a === "object" && typeof b === "object") {
    const ka = definedKeys(a);
    if (ka.length !== definedKeys(b).length) return false;
    return ka.every((k) => b[k] !== undefined && deepEqualPayload(a[k], b[k]));
  }
  return false;
}
const definedKeys = (o) => Object.keys(o).filter((k) => o[k] !== undefined);

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
