// Shared-AI-pool code resolution and kit integrity (readiness brief section 5a; TNR-01).
//
// A manifest may reference a shared pool jutsu by CODE ("B07") instead of by id, in the AI's
// `jutsus` array and in `rules[].action.jutsu`. The codes are resolved here, from the repository's
// own generated pool file, BEFORE anything is sent. Two reasons this must fail closed rather than
// fall back to sending the code:
//
//   TNR-01. profile.updateAi syncs the kit by set difference against the ids it was given; an id
//   that is not a real jutsu is dropped server-side with no error, so a leftover code shipped as a
//   literal leaves the AI with an EMPTY KIT behind a green row. That is the mechanism behind the
//   Syndicate Thief empty kit (state/status.json). In builder v4.32 the fix was to hoist resolution
//   and its stuck-code guard out of `if (dedupNames)`, where they had never run without the flag.
//   Here resolution happens at parse time - earlier than any create, upload or update can be.
//
//   Law 40 (docs/ENGINE_LAWS.md:88, verified at source in ai_v2.ts). The distance gate is the
//   jutsu's range + 1, and both distance conditions are inclusive. A gate above range+1 fires out
//   of range and can strand a human player in combat. The pool file carries the derived gate, so
//   a code-referenced rule gets the arithmetic for free and a hand-written one is checked.
//
// Ported from the repository's current sources, not from memory: builder_bundle.js v4.32
// `resolvePool`/stuck guard (:255-262, :734-742) and skills/building-tnr-content/scripts/
// validate.py `check_pool_kit` (:425-460). The pool records are the generated
// 32b_DATA_pool.json at the repository root, bundled at build time so nothing is fetched at boot
// (the old builder fetched it from a moving branch on every run).

import POOL from "../../../32b_DATA_pool.json" with { type: "json" };

export const POOL_META = Object.freeze(POOL._meta ?? {});
export const POOL_RECORDS = Object.freeze(POOL.records ?? {});
export const POOL_BY_ID = Object.freeze(Object.fromEntries(
  Object.entries(POOL_RECORDS).map(([code, r]) => [r.id, { ...r, code }]),
));
/** A pool code as written in a manifest: one or two letters then two digits (B07, A1 is legacy). */
export const POOLCODE = /^[A-Z]{1,2}\d{1,2}$/;

const isCode = (v) => typeof v === "string" && POOLCODE.test(v);

/**
 * Resolve pool codes in one entry's data. Pure: returns a new data object when anything changed.
 * @returns {{data: object, resolved: number}}
 */
export function resolvePoolCodes(data) {
  if (!data || typeof data !== "object") return { data, resolved: 0 };
  let resolved = 0;
  let out = data;
  const edit = () => (out === data ? (out = { ...data }) : out);

  if (Array.isArray(data.jutsus)) {
    const next = data.jutsus.map((j) => {
      const rec = isCode(j) ? POOL_RECORDS[j] : null;
      if (!rec) return j;
      resolved++;
      return rec.id;
    });
    if (next.some((v, i) => v !== data.jutsus[i])) edit().jutsus = next;
  }

  if (Array.isArray(data.rules)) {
    const rules = data.rules.map((r) => {
      const a = r && typeof r === "object" ? r.action : null;
      const rec = a && isCode(a.jutsu) ? POOL_RECORDS[a.jutsu] : null;
      if (!rec) return r;
      resolved++;
      const { jutsu, ...restAction } = a;
      const action = { ...restAction, jutsuId: rec.id };
      // a code-referenced rule gets its gate arithmetic from the pool: an author writes
      // {type: "distance_lower_than"} with no value and law 40's range+1 is filled in
      const conditions = Array.isArray(r.conditions) ? r.conditions.map((c) =>
        c && c.type === "distance_lower_than" && c.value == null && rec.gate != null ? { ...c, value: rec.gate } : c) : r.conditions;
      return { ...r, action, conditions };
    });
    if (rules.some((v, i) => v !== data.rules[i])) edit().rules = rules;
  }
  return { data: out, resolved };
}

/**
 * Codes that survived resolution. Any of these would be sent as a literal string and stripped
 * server-side, so the job must never start. A `rules[].action.jutsu` of ANY string is stuck: the
 * server's rule shape takes `jutsuId`, so a `jutsu` key is either an unresolved code or a typo,
 * and both are silently dropped.
 */
export function stuckPoolCodes(data) {
  const stuck = [];
  if (!data || typeof data !== "object") return stuck;
  for (const j of Array.isArray(data.jutsus) ? data.jutsus : []) {
    if (isCode(j)) stuck.push(`jutsus: "${j}" is an unresolved pool code (not in 32b_DATA_pool.json)`);
  }
  (Array.isArray(data.rules) ? data.rules : []).forEach((r, i) => {
    const a = r && typeof r === "object" ? r.action : null;
    if (a && typeof a.jutsu === "string") stuck.push(`rules[${i}].action.jutsu = "${a.jutsu}": the server takes jutsuId; this key is dropped`);
  });
  return stuck;
}

/**
 * Kit integrity for an AI entry, after resolution. Ported from validate.py check_pool_kit.
 * @returns {{errors: string[], warnings: string[]}}
 */
export function kitProblems(data) {
  const errors = [], warnings = [];
  if (!data || typeof data !== "object") return { errors, warnings };
  const equipped = (Array.isArray(data.jutsus) ? data.jutsus : []).map(String);
  const eq = new Set(equipped);

  const ap = equipped.map((id) => POOL_BY_ID[id]?.ap).filter((v) => typeof v === "number");
  if (ap.length >= 3 && Math.min(...ap) >= 60) {
    warnings.push("kit is all 60 AP actions and no 40 AP stance: the AI will exhaust itself (a round is 100 AP; laws 61 to 63)");
  }

  (Array.isArray(data.rules) ? data.rules : []).forEach((r, i) => {
    if (!r || typeof r !== "object") return;
    const jid = r.action && r.action.jutsuId;
    if (!jid) return;
    if (equipped.length && !eq.has(String(jid))) {
      const nm = POOL_BY_ID[jid]?.name ?? jid;
      errors.push(`rules[${i}]: fires "${nm}" but that jutsu is NOT in the AI's jutsus array. The rule is inert and the log signature is identical to a severed equip link (law 18)`);
    }
    const rec = POOL_BY_ID[jid];
    if (!rec) return;
    for (const c of Array.isArray(r.conditions) ? r.conditions : []) {
      if (!c || c.type !== "distance_lower_than") continue;
      if (rec.gate != null && c.value !== rec.gate) {
        errors.push(`rules[${i}]: ${rec.name} is range ${rec.range}, so the gate must be ${rec.gate} (range+1, law 40). Found ${c.value}. A higher gate fires out of range and can strand a player in combat`);
      }
      if (rec.range == null) {
        warnings.push(`rules[${i}]: ${rec.name} is self/ground targeted; a distance gate is meaningless on it`);
      }
    }
  });
  return { errors, warnings };
}
