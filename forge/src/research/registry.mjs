// The research-read registry (RUL-2026-09-17-001, RUL-2026-09-17-002).
//
// This module answers a different question from transport/procedures.mjs, and the separation is
// the point. procedures.mjs owns SOURCE facts — kind, auth, limiter — transcribed from the pinned
// game source. It says what the server is. It says nothing about whether Forge is willing to read
// a path for research, or where that read's body is allowed to end up.
//
// This registry owns PRODUCT and PRIVACY admission:
//
//   - a path is readable as a research capture only if it has a row here. `publicProcedure`, a
//     missing auth gate, a tidy endpoint name and mere discoverability at source admit nothing.
//     Admission is demand-driven: a row exists because a committed, reviewed manifest under push/
//     needs it, and the row names that manifest;
//   - a row declares the EXACT input contract Forge will send, so an input is validated and
//     canonicalized before transport rather than forwarded because it happened to parse;
//   - a row declares a persistence TIER, which is both the default and the ceiling for every
//     capture of that path. Widening one is an edit of this file, reviewed as a policy change.
//
// Tiers, narrow to wide (RUL-2026-09-17-001):
//
//   local-only   the exact body may be kept in local IndexedDB for operator/research use. It must
//                never reach a results bundle, a GitHub commit, an export/clipboard payload, a
//                diagnostic dump or an error object. This is the default for everything newly
//                admitted, and for every non-content row without exception.
//   projected    the raw body stays local; export carries ONLY the field paths a manifest declares
//                and this registry has audited, plus provenance/verdict metadata. No wildcard, no
//                object spread, no implicit nested passthrough, and no fallback to the full body
//                when a declared path is absent — that is a projection FAILURE.
//   repo-safe    the exact body may enter repository/export evidence. Carried over verbatim from
//                the Phase 0 content-record point reads that were already audited for it; nothing
//                has been added to this class.
//
// A row's tier is a CEILING as well as a default: a manifest may request the row's tier or any
// narrower one, never a wider one. Because the order below is narrow-to-wide, "narrower" is just
// a smaller index, and there is one comparison in the codebase rather than a table of special
// cases.

import { PROCEDURES } from "../transport/procedures.mjs";
import { stableStringify, fnv1a32 } from "../storage/hash.mjs";

// Narrow to wide. Index order is load-bearing: tierAtMost() is an index comparison.
export const TIERS = Object.freeze(["local-only", "projected", "repo-safe"]);
export const DEFAULT_RESEARCH_TIER = "local-only";

/** Is `tier` no wider than `ceiling`? Unknown names answer false rather than throwing: the caller
 *  that validates a manifest wants a refusal it can put in a message, not an exception. */
export function tierAtMost(tier, ceiling) {
  const a = TIERS.indexOf(tier), b = TIERS.indexOf(ceiling);
  return a >= 0 && b >= 0 && a <= b;
}

// The source pin every row below was audited against. It is the Forge generated-contract pin, and
// check_boundaries.mjs holds it equal to the one fields.json/nested.json carry, so a row can never
// claim provenance from a commit the rest of the contract does not come from.
export const REGISTRY_PIN = "345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9";

// ------------------------------------------------------------------ input contracts
// Deliberately tiny. These describe the handful of shapes the audited rows actually take, and a
// value that does not match is refused before transport. There is no "object" or "any" spec: an
// unconstrained value is how an unaudited field reaches the game.
const STR = Object.freeze({ t: "string" });
const NUM = Object.freeze({ t: "number" });
const BOOL = Object.freeze({ t: "boolean" });
const oneOf = (...values) => Object.freeze({ t: "enum", values: Object.freeze(values) });
const manyOf = (...values) => Object.freeze({ t: "enum[]", values: Object.freeze(values) });

// app/drizzle/constants.ts:539-557 at the pin. Byte-identical at upstream 1fd355ab.
const BATTLE_TYPES = [
  "ARENA", "COMBAT", "SPARRING", "KAGE_AI", "KAGE_PVP", "CLAN_CHALLENGE", "CLAN_BATTLE",
  "SHRINE_WAR", "TOURNAMENT", "QUEST", "RANDOM_ENCOUNTER", "VILLAGE_PROTECTOR", "TRAINING",
  "RANKED_PVP", "RANKED_SPARRING", "RAID", "OVERWORLD",
];

// app/drizzle/constants.ts:58-65 at the pin. Byte-identical at upstream b78eadb9.
const GAME_ASSET_TYPES = ["STATIC", "ANIMATION", "SCENE_BACKGROUND", "SCENE_CHARACTER", "SFX", "MUSIC"];

/**
 * Ceiling on how many pages one capture entry may walk. Requirement 7.6 is that bounds are
 * explicit and no read crawls without one; this is the outer bound a manifest cannot talk its way
 * past, on top of the per-row maxLimit. 20 pages of the only paged row's 500-row maximum is 10,000
 * rows, which is far above the 43-battle working set push/06 actually captures and still a number
 * an operator can reason about.
 */
export const MAX_PAGES = 20;

// A point read of one record by id; six of the seven repo-safe rows take exactly this.
const BY_ID = { required: { id: STR }, optional: {} };

const row = (r) => Object.freeze({
  tier: DEFAULT_RESEARCH_TIER,
  input: null,          // null means "this procedure takes no input"; undefined is sent
  page: null,           // null means "not paged at source"; do not invent one
  project: null,        // null means projection is not admitted for this path
  ...r,
  ...(r.input ? { input: Object.freeze({ required: Object.freeze(r.input.required || {}), optional: Object.freeze(r.input.optional || {}) }) } : {}),
});

/**
 * Every read Forge will issue as a research capture, and nothing else.
 *
 * The content rows are a transcription of what Phase 0 already admitted, not a widening: the seven
 * repo-safe point reads are exactly the old FULL_PERSIST_PATHS, and the name lists are the list
 * reads CachedReader.list() already allowed, now carrying the tier they always implicitly had
 * (their bodies were never persistable, which is local-only). The two combat rows are the only
 * genuinely new admissions, and each names the committed manifest that demanded it.
 */
export const RESEARCH_READS = Object.freeze({
  // ---- content record point reads: repo-safe, carried over verbatim (RUL-2026-09-17-001) -------
  "gameAsset.get": row({ tier: "repo-safe", input: BY_ID, source: "routers/gameAsset.ts get", demand: "push/02_one_perfect_crop_asset_probe.json" }),
  "jutsu.get": row({ tier: "repo-safe", input: BY_ID, source: "routers/jutsu.ts get", demand: "push/05_aerathiel_pvp_research_stage1.json" }),
  "item.get": row({ tier: "repo-safe", input: BY_ID, source: "routers/item.ts get", demand: "push/24_godstorm_tower_related_capture.json" }),
  "bloodline.get": row({ tier: "repo-safe", input: BY_ID, source: "routers/bloodline.ts get", demand: "push/21_night_parade_asset_followup.json" }),
  "quests.get": row({ tier: "repo-safe", input: BY_ID, source: "routers/quests.ts get", demand: "push/01_old_ghost_format_capture.json" }),
  // profile.getAi is the one point read keyed on userId, not id (routers/profile.ts:1121).
  "profile.getAi": row({ tier: "repo-safe", input: { required: { userId: STR }, optional: {} }, source: "routers/profile.ts:1121 getAi", demand: "push/04_one_perfect_crop_bandit_ai_probe.json" }),
  "ai.getAiProfile": row({ tier: "repo-safe", input: BY_ID, source: "routers/ai.ts getAiProfile", demand: "push/25_godstorm_tower_combat_closure.json" }),

  // ---- content name lists: local-only ---------------------------------------------------------
  // These were readable in Phase 0 and their bodies were never persistable, so local-only is the
  // tier they already had. Nothing here is widened; a row that should export needs a reviewed edit.
  //
  // Five declare no .input() at source, so `undefined` is the honest request and anything sent is
  // ignored. gameAsset.getAllNames is NOT one of them - see its row.
  "jutsu.getAllNames": row({ source: "routers/jutsu.ts getAllNames", demand: "push/00_forge_readonly_smoke.json" }),
  "quests.getAllNames": row({ source: "routers/quests.ts getAllNames", demand: "push/00_forge_readonly_smoke.json" }),
  "item.getAllNames": row({ source: "routers/item.ts getAllNames", demand: "builder dedupNames live-name check" }),
  "bloodline.getAllNames": row({ source: "routers/bloodline.ts getAllNames", demand: "builder dedupNames live-name check" }),
  "profile.getAllAiNames": row({ source: "routers/profile.ts getAllAiNames", demand: "builder dedupNames live-name check" }),
  // The one name list with an input contract: .input(z.object({ type: z.enum(GameAssetTypes)
  // .optional(), folderPrefix: z.boolean().optional() })) at asset.ts:50-57. BOTH MEMBERS are optional
  // but THE OBJECT IS NOT, so `undefined` fails zod before the resolver runs and the server answers
  // BAD_REQUEST - which is what killed the three Godstorm Stormcourt asset creates at their
  // pre-create name snapshot (harvests/inbox/tnr_results_1789829183863.json, items 0-2 and 27;
  // repaired on main at 74083c1). The Phase 1 registry first transcribed this row as input-free,
  // which would have reproduced that failure; the row now carries the audited contract, so the
  // canonical input for "no filter" is `{}` and a manifest filter is validated before transport.
  // `folderPrefix: true` returns "folder/Name" instead of the plain name, so the dedupNames and
  // reconciler callers deliberately send the unfiltered `{}` (budget/reader.mjs listInput).
  "gameAsset.getAllNames": row({
    input: { required: {}, optional: { type: oneOf(...GAME_ASSET_TYPES), folderPrefix: BOOL } },
    source: "app/src/server/api/routers/asset.ts:50-57 getAllNames",
    demand: "builder dedupNames live-name check; push/53 Godstorm repair",
    note: "object required at source: undefined is BAD_REQUEST, {} is the unfiltered list",
  }),

  // ---- non-content research reads: NEW, demand-driven, local-only -----------------------------
  // Both are protectedProcedure .query() with no ratelimitMiddleware composed at the call site,
  // audited at REGISTRY_PIN and re-checked byte-identical at upstream 1fd355ab.
  //
  // getBattleHistory returns battleHistory rows joined WITH attacker/defender objects carrying
  // username, userId and avatar (combat.ts:553-556). That is player data in a public repository if
  // it is ever exported, which is exactly why the tier is local-only and why `project` is null:
  // push/05 declares a `select` list, but admitting those fields for repository export is a
  // privacy/publishing decision this implementation does not get to take. A reviewed registry edit
  // adding `project` here is what turns push/05's select into an exportable projection.
  "combat.getBattleHistory": row({
    input: { required: {}, optional: { userId: STR, secondsBack: NUM, combatTypes: manyOf(...BATTLE_TYPES) } },
    source: "app/src/server/api/routers/combat.ts:530-560 getBattleHistory",
    demand: "push/05_aerathiel_pvp_research_stage1.json",
    note: "no pagination at source: filtered, ordered createdAt desc, returns every matching row",
  }),
  // getBattleEntries is the one paged row: limit/offset, server default limit 30 and offset 0,
  // ordered battleRound desc then battleVersion desc (combat.ts:396-421). The ordering is total and
  // server-side, which is what makes offset paging reproducible rather than a best effort.
  "combat.getBattleEntries": row({
    input: {
      required: { battleId: STR },
      optional: { limit: NUM, offset: NUM, userFilter: oneOf("all", "user", "opponents"), showBasicActions: BOOL, refreshKey: NUM, checkBattle: BOOL },
    },
    // maxLimit is Forge's bound, not the server's: source accepts any number. 500 is the value the
    // committed demand uses, so it is the measured working maximum rather than a round guess.
    page: Object.freeze({ mode: "offset", limitKey: "limit", offsetKey: "offset", defaultLimit: 30, maxLimit: 500 }),
    source: "app/src/server/api/routers/combat.ts:382-421 getBattleEntries",
    demand: "push/06_aerathiel_pvp_battle_logs.json",
  }),
});

export const RESEARCH_PATHS = Object.freeze(Object.keys(RESEARCH_READS));
/** The repo-safe class, derived rather than restated: storage/captures.mjs re-exports this. */
export const REPO_SAFE_PATHS = Object.freeze(RESEARCH_PATHS.filter((p) => RESEARCH_READS[p].tier === "repo-safe"));

export class ResearchError extends Error {
  constructor(message, info = {}) { super(message); this.name = "ResearchError"; Object.assign(this, info); }
}

/** The row for a path, or null. Never throws: callers that must fail closed use requireRow(). */
export function researchRow(path) { return RESEARCH_READS[path] || null; }
export function isResearchRead(path) { return Object.prototype.hasOwnProperty.call(RESEARCH_READS, path); }

/**
 * The row, or a refusal. This is the fail-closed gate RUL-2026-09-17-002 asks for, and it is
 * reached before any transport: a path the game would happily answer is still refused here when no
 * committed work package has demanded it and no reviewer has audited its contract.
 */
export function requireRow(path) {
  const r = RESEARCH_READS[path];
  if (!r) {
    throw new ResearchError(
      `${path} is not in the audited research-read registry, so Forge will not read it. Adding a row requires a committed manifest that needs it and a source audit at the declared pin.`,
      { path });
  }
  return r;
}

/** The tiers a manifest may request for a path: the row's tier and everything narrower. */
export function admissibleTiers(path) {
  const ceiling = requireRow(path).tier;
  return TIERS.slice(0, TIERS.indexOf(ceiling) + 1);
}

// ------------------------------------------------------------------ canonical input
const typeName = (v) => (Array.isArray(v) ? "array" : v === null ? "null" : typeof v);

function checkValue(where, spec, value) {
  switch (spec.t) {
    case "string":
      if (typeof value !== "string" || !value) throw new ResearchError(`${where} must be a non-empty string, got ${typeName(value)}`);
      return value;
    case "number":
      if (typeof value !== "number" || !Number.isFinite(value)) throw new ResearchError(`${where} must be a finite number, got ${typeName(value)}`);
      return value;
    case "boolean":
      if (typeof value !== "boolean") throw new ResearchError(`${where} must be a boolean, got ${typeName(value)}`);
      return value;
    case "enum":
      if (!spec.values.includes(value)) throw new ResearchError(`${where} must be one of ${spec.values.join(", ")}, got ${JSON.stringify(value)}`);
      return value;
    case "enum[]": {
      if (!Array.isArray(value) || !value.length) throw new ResearchError(`${where} must be a non-empty array`);
      for (const v of value) if (!spec.values.includes(v)) throw new ResearchError(`${where} contains ${JSON.stringify(v)}, which is not one of ${spec.values.join(", ")}`);
      return [...value]; // element ORDER is preserved: it is part of the exact input sent
    }
    /* c8 ignore next */
    default: throw new ResearchError(`${where} has an unknown spec`);
  }
}

/**
 * THE canonical representation of one read's input. Requirement 7.3 is that cache identity,
 * provenance and transport all derive from one representation, so this is the only function that
 * builds a research read's input and every one of those three uses its result.
 *
 * Key order is the registry's declaration order (required, then optional), not the manifest's, so
 * `{limit, battleId}` and `{battleId, limit}` serialize identically and share a cache entry — they
 * are the same request. An absent optional key is simply absent; it is never defaulted here, because
 * a default Forge invented would make the stored provenance differ from what the server was sent.
 *
 * @returns {object|null} a fresh plain object, or null for an input-free procedure (send undefined)
 */
export function canonicalInput(path, input) {
  const r = requireRow(path);
  const given = input == null ? {} : input;
  if (typeof given !== "object" || Array.isArray(given)) throw new ResearchError(`${path}: input must be an object`);
  if (!r.input) {
    const extra = Object.keys(given);
    if (extra.length) throw new ResearchError(`${path} takes no input; remove ${extra.join(", ")}`, { path });
    return null;
  }
  const { required, optional } = r.input;
  const known = new Set([...Object.keys(required), ...Object.keys(optional)]);
  const unknown = Object.keys(given).filter((k) => !known.has(k));
  if (unknown.length) {
    throw new ResearchError(`${path}: input key(s) ${unknown.join(", ")} are not in the audited contract (allowed: ${[...known].join(", ")})`, { path, unknown });
  }
  const out = {};
  for (const k of Object.keys(required)) {
    if (!(k in given)) throw new ResearchError(`${path}: input.${k} is required`, { path, key: k });
    out[k] = checkValue(`${path}: input.${k}`, required[k], given[k]);
  }
  for (const k of Object.keys(optional)) {
    if (!(k in given) || given[k] === undefined) continue;
    out[k] = checkValue(`${path}: input.${k}`, optional[k], given[k]);
  }
  return out;
}

/**
 * The cache identity of a canonical input, as a string. It is the serialization itself and NOT a
 * hash: a 32-bit digest of an unbounded input space can collide, and requirement 7.1 says two reads
 * with different transport inputs never alias. A key that cannot collide costs a few dozen bytes
 * per cache row and removes the question.
 */
export function canonicalKey(input) { return input === null ? "" : JSON.stringify(input); }

/**
 * How a row is read: a single-record point read, an input-free name list, or a filtered/paged query.
 * Derived from the row's own declared contract, so a registry edit that gives a path a filter or a
 * page contract moves it to the query path automatically instead of needing a second list updated.
 */
export function readMode(path) {
  const r = requireRow(path);
  if (!r.input) return "list";
  const req = Object.keys(r.input.required), opt = Object.keys(r.input.optional);
  return req.length === 1 && opt.length === 0 && !r.page ? "point" : "query";
}

/**
 * The canonical input for a POINT read of one record. Which key names the record (`id` for six of
 * the seven, `userId` for profile.getAi) is read off the row's own required contract rather than
 * from a second table that could disagree with it.
 */
export function pointInput(path, id) {
  const r = requireRow(path);
  const keys = r.input ? Object.keys(r.input.required) : [];
  if (keys.length !== 1) throw new ResearchError(`${path} is not a single-record point read`, { path });
  return canonicalInput(path, { [keys[0]]: id });
}

/** The audited page contract for a path, or null when the procedure is not paged at source. */
export function pageContract(path) { return requireRow(path).page; }

/**
 * The input for page `n` (0-based) of a paged read. Only the audited offset shape exists, and it is
 * built from the row's own key names — there is no generic pager that would hide the fact that a
 * different procedure pages differently.
 */
export function pageInput(path, canonical, n) {
  const p = requireRow(path).page;
  if (!p) throw new ResearchError(`${path} is not paged at source; it cannot be read by page`, { path });
  if (n === 0) return canonical;
  const limit = canonical[p.limitKey] ?? p.defaultLimit;
  return canonicalInput(path, { ...canonical, [p.offsetKey]: (canonical[p.offsetKey] ?? 0) + limit * n });
}

/** How many rows page `n` of this read may return; a short page means the walk is finished. */
export function pageSize(path, canonical) {
  const p = requireRow(path).page;
  return p ? (canonical[p.limitKey] ?? p.defaultLimit) : null;
}

// ------------------------------------------------------------------ projection
// A declared field path: dotted, alphanumeric segments only. This rejects "*", "a.*", "a[0]", "",
// "a..b" and anything with a space by construction, so there is no wildcard to interpret and no
// expression to evaluate. The prototype-pollution names are refused separately because they are
// perfectly ordinary identifiers that happen to be able to read across an object's own data.
const FIELD_RE = /^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*$/;
const FORBIDDEN_SEGMENTS = new Set(["__proto__", "prototype", "constructor"]);

/**
 * Validate a manifest's declared projection against the row.
 *
 * Which fields a row may project depends on which DIRECTION the projection moves in:
 *
 *   - on a **repo-safe** row the whole body is already admitted to repository evidence, so a
 *     projection can only ever narrow what is exported. Any well-formed declared path is accepted,
 *     because none of them can put into the repository something the row does not already allow;
 *   - on any narrower row a projection WIDENS what leaves the machine, so it is admitted only from
 *     the row's explicit `project` allowlist. No allowlist means no projection at all — which is
 *     where every non-content row stands today, and moving one is a reviewed registry edit.
 *
 * Well-formedness is fail-closed on every axis regardless: a wildcard, an index, an empty segment
 * and the prototype-walking names are refused before either rule above is reached.
 */
export function validateProjection(path, fields) {
  const r = requireRow(path);
  if (!Array.isArray(fields) || !fields.length) {
    throw new ResearchError(`${path}: tier "projected" needs a non-empty projection (declare it as "projection" or "select")`, { path });
  }
  const narrowing = r.tier === "repo-safe";
  if (!narrowing && !r.project) {
    throw new ResearchError(`${path}: the registry admits no projected fields for this path, so nothing may be exported from it; widening that is a reviewed registry edit, not a manifest key`, { path });
  }
  const out = [];
  for (const f of fields) {
    if (typeof f !== "string" || !FIELD_RE.test(f)) {
      throw new ResearchError(`${path}: ${JSON.stringify(f)} is not a declared field path; wildcards, indexes and spreads are not projections`, { path, field: f });
    }
    if (f.split(".").some((s) => FORBIDDEN_SEGMENTS.has(s))) throw new ResearchError(`${path}: ${f} is refused`, { path, field: f });
    if (!narrowing && !r.project.includes(f)) {
      throw new ResearchError(`${path}: ${f} is not in the registry's audited projectable fields (${r.project.join(", ")})`, { path, field: f });
    }
    if (!out.includes(f)) out.push(f);
  }
  // A declaration that is a strict PREFIX of another declaration cannot be satisfied: the shorter
  // path says "export this field", the longer says "descend into it", and a value cannot be both a
  // leaf and a structure. Accepting the pair let the leaf win and the deeper request disappear with
  // a green verdict - a declared field silently absent from the evidence (re-review FN3-R1). It is
  // refused here rather than resolved, because either resolution would quietly discard something the
  // manifest asked for.
  for (const a of out) {
    for (const b of out) {
      if (a !== b && b.startsWith(a + ".")) {
        throw new ResearchError(`${path}: ${a} and ${b} overlap - ${a} is declared as a field and also descended into by ${b}, and a value cannot be both. Declare the leaves you want.`, { path, field: b });
      }
    }
  }
  return out;
}

const own = (o, k) => o !== null && typeof o === "object" && Object.prototype.hasOwnProperty.call(o, k);
const isPlainObject = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
// What a declared path is allowed to END at. A projection exports the fields it names and nothing
// else, so a terminal must be a value that IS the field: a scalar, or a list of scalars. An object
// or a list of objects is a subtree, and exporting one would ship every field inside it - including
// fields added to the record after the projection was written, which nobody declared and nobody
// reviewed. RUL-2026-09-17-001 forbids exactly that as "implicit nested passthrough", so an
// unsupported terminal is a projection FAILURE naming the path, never a silent subtree.
const isScalar = (v) => v === null || v === undefined || ["string", "number", "boolean"].includes(typeof v);
const isScalarList = (v) => Array.isArray(v) && v.every(isScalar);

/**
 * Project one object against a set of declared paths, grouped by their first segment.
 *
 * Descending THROUGH an array is supported and is how a per-element field is declared:
 * `content.objectives.id` projects `{content: {objectives: [{id}, {id}]}}`, carrying the shape but
 * only the named leaf out of each element. Descending through a scalar, or stopping on a structure,
 * is a failure.
 */
function projectInto(value, paths, prefix, missing) {
  if (!isPlainObject(value)) { for (const segs of paths) missing.add([...prefix, ...segs].join(".")); return null; }
  const out = {};
  const groups = new Map();
  for (const segs of paths) {
    const [head, ...rest] = segs;
    if (!groups.has(head)) groups.set(head, []);
    groups.get(head).push(rest);
  }
  for (const [head, rests] of groups) {
    const here = [...prefix, head];
    if (!own(value, head)) { for (const rest of rests) missing.add([...here, ...rest].join(".")); continue; }
    const child = value[head];
    const terminal = rests.filter((r) => !r.length);
    const deeper = rests.filter((r) => r.length);
    if (terminal.length) {
      // Defence in depth for the overlap validateProjection now refuses: if a caller reaches here
      // with both a terminal and a descendant of it, the descendant is UNSATISFIED and is recorded,
      // never dropped. Taking the leaf and returning green is what made a declared field vanish from
      // the evidence (re-review FN3-R1).
      for (const rest of deeper) missing.add([...here, ...rest].join("."));
      if (isScalar(child)) { out[head] = child === undefined ? null : child; continue; }
      if (isScalarList(child)) { out[head] = [...child]; continue; }
      // a structure was named as a field; refuse rather than ship the subtree
      missing.add(here.join("."));
      continue;
    }
    if (Array.isArray(child)) { out[head] = child.map((el) => projectInto(el, deeper, here, missing)); continue; }
    if (isPlainObject(child)) { out[head] = projectInto(child, deeper, here, missing); continue; }
    for (const rest of deeper) missing.add([...here, ...rest].join("."));
  }
  return out;
}

/**
 * Apply a validated projection to a decoded body. An array body projects element-wise, which is the
 * shape every paged/filtered research read returns.
 *
 * There is no partial success and no fallback: one absent or unsupported declared path anywhere
 * makes the whole projection a failure carrying the field names responsible. Substituting the full
 * body, or quietly emitting a wider object than was declared, is the leak this exists to prevent.
 */
export function projectBody(body, fields) {
  const split = fields.map((f) => f.split("."));
  const missing = new Set();
  const data = Array.isArray(body)
    ? body.map((el) => projectInto(el, split, [], missing))
    : projectInto(body, split, [], missing);
  return missing.size ? { ok: false, missing: [...missing] } : { ok: true, data };
}

// ------------------------------------------------------------------ registry/source agreement
/**
 * Every research row must be a query that the audited source registry actually has, and no mutation
 * may ever appear here. Written as a function rather than inline assertions so the whole relation
 * can be checked in one place; test/research.registry.test.mjs holds it empty, which is what makes
 * a row that has drifted from the source facts a failing build rather than a comment nobody reread.
 */
export function registryProblems() {
  const problems = [];
  for (const path of RESEARCH_PATHS) {
    const p = PROCEDURES[path];
    if (!p) { problems.push(`${path}: no row in the audited source registry (transport/procedures.mjs)`); continue; }
    if (p.kind !== "query") problems.push(`${path}: kind is ${p.kind}; the research registry is reads only (RUL-2026-09-17-002)`);
    const r = RESEARCH_READS[path];
    if (!TIERS.includes(r.tier)) problems.push(`${path}: unknown tier ${JSON.stringify(r.tier)}`);
    if (r.project && r.tier === "local-only") problems.push(`${path}: declares projectable fields but its tier cannot export any`);
    if (r.page && r.page.mode !== "offset") problems.push(`${path}: unknown page mode ${JSON.stringify(r.page.mode)}`);
  }
  return problems;
}

/**
 * The immutable content identity of the admission policy itself, over every field that decides what
 * a read may do: the pin the rows were audited at, each row's tier, its projectable allowlist, its
 * input contract and its paging bound. Editing any of those changes this value, so a capture stamped
 * with it can be tied back to the exact policy that admitted it — which a version string cannot do,
 * because two builds of `forge 0.4.1` could carry different registries.
 *
 * Derived rather than hand-maintained, so it cannot be forgotten during a registry edit.
 */
/** One input spec as plain serializable data: its kind and, for an enum, its exact members. */
function specFacts(spec) {
  return spec.t === "enum" || spec.t === "enum[]" ? { t: spec.t, values: [...spec.values] } : { t: spec.t };
}

/**
 * EVERY fact that decides what a read may do, as plain data. This is the input the policy identity
 * is derived from, and it has to be complete: the first version keyed on input KEY NAMES, so
 * changing a field's type from number to boolean, or withdrawing an enum member, changed what Forge
 * would admit while leaving the identity untouched (re-review FN4-R1). It now carries the full input
 * specifications, the projectable allowlists, the per-row paging descriptors, and the global bounds
 * and tier ordering that apply to every row.
 *
 * Exported so the sensitivity of the identity can be tested directly: a test mutates a copy of these
 * facts and asserts the revision moves, which is the property that actually matters and which a
 * shape assertion on the digest cannot check.
 */
export function policyFacts() {
  return {
    pin: REGISTRY_PIN,
    // global policy: the tier lattice, the default tier and the ceiling on any walk
    tiers: [...TIERS],
    defaultTier: DEFAULT_RESEARCH_TIER,
    maxPages: MAX_PAGES,
    rows: RESEARCH_PATHS.map((path) => {
      const r = RESEARCH_READS[path];
      const specs = (m) => Object.fromEntries(Object.entries(m).map(([k, v]) => [k, specFacts(v)]));
      return {
        path, tier: r.tier,
        project: r.project ? [...r.project] : null,
        input: r.input ? { required: specs(r.input.required), optional: specs(r.input.optional) } : null,
        page: r.page ? { ...r.page } : null,
      };
    }),
  };
}

/** The identity of one set of policy facts. Stable under key order, sensitive to every value. */
export function revisionOf(facts) { return fnv1a32(stableStringify(facts)); }

export const REGISTRY_REVISION = revisionOf(policyFacts());

/**
 * The policy identity to stamp onto a capture at the moment it is taken (brief section 6: a capture
 * must retain provenance sufficient to identify its audited contract). It is recorded WITH the body
 * and never recomputed at export, so materializing an old job under a newer build cannot relabel
 * that old evidence with today's policy.
 */
export function capturePolicy(path) {
  const r = requireRow(path);
  return Object.freeze({ pin: REGISTRY_PIN, registry: REGISTRY_REVISION, tier: r.tier, source: r.source });
}
