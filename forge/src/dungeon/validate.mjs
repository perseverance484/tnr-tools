import CONTRACT from "./contract.json" with { type: "json" };
// a function import across the runner/validate <-> dungeon/validate cycle: hoisted, resolved at call time
import { deepEqualPayload } from "../runner/validate.mjs";
export { CONTRACT };

// Pre-send validation for dungeon definitions (state/prompt_forge_dungeon_recipe.md).
//
// The manifest's `data` is the dungeon's `content` object: coop.dungeon.save takes {id?, content} and
// replaces the whole content, so an edit is checked against live content merged with the
// asserted keys, exactly what the runner will send. Every rule here mirrors one in the pinned
// source (dungeonContentSchema and its superRefine, dungeonDropSchema, encounterWaveSchema,
// mapLocationFields, dungeonRewardError); bounds and defaults come from contract.json, derived
// from the pin by tools/derive_dungeon.mjs, never typed in by hand.
//
// A live definition is the getAll row {id, content, updatedAt} exactly as the server returns it:
// the row's id and timestamp are never mixed into the content (review F3).
//
// Checked at save by the server and NOT here, because they need live rows: that each AI, item,
// jutsu and package exists; that a cache drop is a weighted cache; that the entrance asset
// exists; package contents' share of the reward bounds.

export const isDungeonEntity = (e) => e === "dungeon";
export const dungeonFields = () => new Set(CONTRACT.contentFields);

const B = CONTRACT.bounds;
const D = CONTRACT.defaults;
const obj = (v) => v && typeof v === "object" && !Array.isArray(v);
const str = (v) => typeof v === "string";
const num = (v) => typeof v === "number" && Number.isFinite(v);
const int = (v, min, max) => Number.isSafeInteger(v) && v >= min && v <= max;
const isRef = (v) => str(v) && v.startsWith("@");
// An instant both this browser and the server read the same way: a date-only value (UTC midnight
// in every JS engine) or a date-time carrying its own offset. Without one, "2027-01-01T00:00"
// would be read in the browser's zone here and in the server's zone at save.
const ISO_INSTANT = /^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[+-]\d{2}:\d{2}))?$/;
const validDate = (v) => v instanceof Date ? !Number.isNaN(v.getTime()) : str(v) && ISO_INSTANT.test(v) && !Number.isNaN(Date.parse(v));

/** Which ref prefixes a literal-or-ref id may carry in each position. */
const REF_FOR_DROP = Object.freeze({ item: ["item"], cache: ["item"], jutsu: ["jutsu"], package: [] });

function idProblem(v, allowed, where) {
  if (!str(v) || !v.trim()) return `${where} must be a non-empty id`;
  if (!isRef(v)) return null;
  const m = v.match(/^@(\w+):(.+)$/);
  if (!m || !allowed.includes(m[1])) {
    return allowed.length
      ? `${where}: ${v} is not a ${allowed.map((p) => `@${p}:`).join(" or ")} ref`
      : `${where}: ${v} must be a literal id (no ref type exists for it)`;
  }
  return null;
}

function unknownKeys(o, allowed, where, out, why = "the server's validator would drop it silently") {
  for (const k of Object.keys(o)) if (!allowed.includes(k)) out.push(`${where}: unknown key "${k}" (${why})`);
}

/**
 * Unknown keys anywhere in a LIVE definition. The save re-parses the whole content and zod drops
 * what the pinned schema does not know, so editing such a definition would delete those keys and
 * still read back as a match on every asserted key. Refuse instead: the contract is behind the game.
 */
export function liveDrift(content) {
  if (!obj(content)) return ["live dungeon row has no content object; refusing to edit it"];
  const out = [];
  const why = "schema drift: the pinned contract does not know it and a save would delete it; re-derive src/dungeon/contract.json first";
  unknownKeys(content, CONTRACT.contentFields, "live content", out, why);
  if (Array.isArray(content.tiers)) content.tiers.forEach((tier, ti) => Array.isArray(tier) && tier.forEach((f, fi) => {
    if (!obj(f)) return;
    unknownKeys(f, CONTRACT.floorFields, `live tiers[${ti}][${fi}]`, out, why);
    if (Array.isArray(f.waves)) f.waves.forEach((w, wi) => obj(w) && unknownKeys(w, CONTRACT.waveFields, `live tiers[${ti}][${fi}].waves[${wi}]`, out, why));
  }));
  if (obj(content.rewards)) {
    unknownKeys(content.rewards, CONTRACT.rewardFields, "live rewards", out, why);
    if (Array.isArray(content.rewards.drops)) content.rewards.drops.forEach((d, i) => obj(d) && unknownKeys(d, CONTRACT.dropFields, `live rewards.drops[${i}]`, out, why));
  }
  return out;
}

/** The ids of the package drops in a content's rewards (each one is re-copied from the catalog on save). */
export function packageDrops(content) {
  const drops = obj(content) && obj(content.rewards) && Array.isArray(content.rewards.drops) ? content.rewards.drops : [];
  return drops.filter((d) => obj(d) && d.type === "package").map((d) => d.id);
}

/**
 * Problems with one dungeon content payload.
 * @param {object} data      asserted content keys (refs may be unresolved: offline checks)
 * @param {object|null} live live getAll row {id, content, updatedAt} (edits only)
 * @param {{preCreate?: boolean, refreshPackages?: boolean}} [opts] preCreate: no live row; `data`
 *   is the whole content. refreshPackages: the entry accepts that this save re-copies every
 *   package snapshot from the current catalog.
 * @returns {string[]}
 */
export function dungeonProblems(data, live = null, { preCreate = false, refreshPackages = false } = {}) {
  if (!obj(data)) return ["data must be the dungeon content object"];
  const out = [];
  unknownKeys(data, CONTRACT.contentFields, "content", out);
  if (preCreate && data.hidden !== true) out.push("a dungeon create must carry hidden:true (everything ships hidden; publishing is a separate step)");
  if (!preCreate && !live) return out; // keys only until the live content is known
  if (!preCreate) {
    // the original live content, before anything is merged or filtered (review F3)
    const drift = liveDrift(live.content);
    if (drift.length) return [...out, ...drift];
  }
  const d = { ...(preCreate ? {} : live.content), ...data };
  const check = (ok, message) => { if (!ok) out.push(message); };

  check(str(d.name) && d.name.trim().length >= 1 && d.name.trim().length <= B.nameMax, `name must contain 1..${B.nameMax} characters`);
  check(!str(d.name) || d.name === d.name.trim(), "name must not start or end with whitespace (the server trims it)");
  check(d.description === undefined || (str(d.description) && d.description.length <= B.descriptionMax), `description must be text of at most ${B.descriptionMax} characters`);
  check(d.structureAssetId === undefined || (str(d.structureAssetId) && d.structureAssetId.length <= B.structureAssetIdMax && !isRef(d.structureAssetId)),
    "structureAssetId must be a literal map-structure asset id (a mapAsset row, not a gameAsset; no ref type exists for it) or empty");
  check(d.structureScale === undefined || (num(d.structureScale) && d.structureScale >= B.structureScale.min && d.structureScale <= B.structureScale.max),
    `structureScale must be ${B.structureScale.min}..${B.structureScale.max}`);
  check(int(d.sector, B.sector.min, B.sector.max), `sector must be an integer ${B.sector.min}..${B.sector.max}`);
  check(int(d.longitude, B.longitude.min, B.longitude.max), `longitude must be an integer ${B.longitude.min}..${B.longitude.max}`);
  check(int(d.latitude, B.latitude.min, B.latitude.max), `latitude must be an integer ${B.latitude.min}..${B.latitude.max}`);
  check("expiresAt" in d && (d.expiresAt === null || validDate(d.expiresAt)),
    "expiresAt is required: null, YYYY-MM-DD, or a date-time with Z or an offset");
  check(d.hidden === undefined || typeof d.hidden === "boolean", "hidden must be boolean");
  check(d.background === undefined || CONTRACT.biomes.includes(d.background), `background must be one of ${CONTRACT.biomes.join(", ")}`);

  tierProblems(d.tiers, out);
  // A package snapshot the manifest wrote is refused; one inherited from the live row is the
  // server's own copy and is not the client's to author (review F4).
  rewardProblems(d.rewards, out, preCreate || "rewards" in data);
  const packages = packageDrops(d);
  if (!preCreate && packages.length && !refreshPackages) {
    out.push(`rewards: package drop(s) ${packages.join(", ")}: coop.dungeon.save re-copies every package snapshot from the CURRENT catalog, which Forge cannot read, so stored package rewards may change. Set "refreshPackages": true to accept that`);
  }
  return out;
}

function tierProblems(tiers, out) {
  if (!Array.isArray(tiers) || tiers.length < 1 || tiers.length > B.maxTiers) {
    out.push(`tiers must hold 1..${B.maxTiers} tiers`);
    return;
  }
  tiers.forEach((tier, ti) => {
    if (!Array.isArray(tier) || tier.length !== B.floorsPerTier) {
      out.push(`tiers[${ti}] must hold exactly ${B.floorsPerTier} floors`);
      return;
    }
    tier.forEach((floor, fi) => {
      const where = `tiers[${ti}][${fi}]`;
      if (!obj(floor)) { out.push(`${where} must be an object`); return; }
      unknownKeys(floor, CONTRACT.floorFields, where, out);
      const last = ti === tiers.length - 1 && fi === B.floorsPerTier - 1;
      const expected = last ? "boss" : fi === B.floorsPerTier - 1 ? "mini-boss" : "floor";
      if (!CONTRACT.floorKinds.includes(floor.kind)) out.push(`${where}.kind must be one of ${CONTRACT.floorKinds.join(", ")}`);
      else if (floor.kind !== expected) out.push(`${where}.kind must be "${expected}" (each non-final tier ends on a mini-boss, the last floor is the boss)`);
      const waves = floor.waves;
      if (!Array.isArray(waves) || waves.length < 1 || waves.length > B.maxWaves) {
        out.push(`${where}.waves must hold 1..${B.maxWaves} waves`);
        return;
      }
      waves.forEach((wave, wi) => {
        const w = `${where}.waves[${wi}]`;
        if (!obj(wave)) { out.push(`${w} must be an object`); return; }
        unknownKeys(wave, CONTRACT.waveFields, w, out);
        if (!Array.isArray(wave.aiIds) || wave.aiIds.length < 1 || wave.aiIds.length > B.maxMobs) out.push(`${w}.aiIds must hold 1..${B.maxMobs} enemies`);
        else wave.aiIds.forEach((id, ai) => { const p = idProblem(id, ["ai"], `${w}.aiIds[${ai}]`); if (p) out.push(p); });
        // zod's prefault fills undefined only: an explicit null is refused (review F6)
        const delay = wave.delayRounds === undefined ? D.wave.delayRounds : wave.delayRounds;
        if (!int(delay, 0, B.maxWaveDelayRounds)) out.push(`${w}.delayRounds must be an integer 0..${B.maxWaveDelayRounds} (null is not accepted)`);
        else if (wi === 0 && delay !== 0) out.push(`${w}.delayRounds must be 0: the first wave starts immediately`);
      });
    });
  });
}

function rewardProblems(rewards, out, authored) {
  if (!obj(rewards)) { out.push("rewards must be an object {money, experience, tokens, prestige, drops}"); return; }
  unknownKeys(rewards, CONTRACT.rewardFields, "rewards", out);
  for (const k of ["money", "experience"]) {
    const v = rewards[k];
    if (v !== undefined && !(num(v) && v >= 0 && v <= B.maxRewardAmount)) out.push(`rewards.${k} must be 0..${B.maxRewardAmount}`);
  }
  for (const k of ["tokens", "prestige"]) {
    const v = rewards[k];
    if (v !== undefined && !int(v, 0, B.maxRewardAmount)) out.push(`rewards.${k} must be an integer 0..${B.maxRewardAmount}`);
  }
  const drops = rewards.drops === undefined ? [] : rewards.drops;
  if (!Array.isArray(drops) || drops.length > B.maxDrops) { out.push(`rewards.drops must be a list of at most ${B.maxDrops} drops (null is not accepted)`); return; }
  let items = 0;
  drops.forEach((drop, i) => {
    const where = `rewards.drops[${i}]`;
    if (!obj(drop)) { out.push(`${where} must be an object`); return; }
    unknownKeys(drop, CONTRACT.dropFields, where, out);
    if ("package" in drop && authored) out.push(`${where}.package: the server copies the catalog snapshot at save and ignores a sent payload; omit it`);
    if (!CONTRACT.dropTypes.includes(drop.type)) { out.push(`${where}.type must be one of ${CONTRACT.dropTypes.join(", ")}`); return; }
    const p = idProblem(drop.id, REF_FOR_DROP[drop.type], `${where}.id`);
    if (p) out.push(p);
    if (!(num(drop.chance) && drop.chance >= B.chance.min && drop.chance <= B.chance.max)) out.push(`${where}.chance must be ${B.chance.min}..${B.chance.max}`);
    const quantity = drop.quantity === undefined ? D.drop.quantity : drop.quantity;
    if (!int(quantity, 1, B.maxRewardQuantity)) out.push(`${where}.quantity must be an integer 1..${B.maxRewardQuantity} (null is not accepted)`);
    else if (drop.type === "jutsu" && quantity !== 1) out.push(`${where}.quantity must be 1: jutsu rewards can only be learned once`);
    else if (drop.type === "item" || drop.type === "cache") items += quantity;
  });
  // dungeonRewardError: every drop assumed to succeed. Package contents count too, but only the
  // server holds their snapshot, so this is a lower bound and the save still checks the rest.
  if (items > B.maxGrantedItems) out.push(`rewards: up to ${items} items per player exceeds ${B.maxGrantedItems} (dungeonRewardError)`);
}

/**
 * The content the save sends for an edit: the live content with the asserted keys over it, every
 * key kept (liveDrift has already refused any the contract does not know). Inherited package
 * snapshots are left out: the server ignores a sent one and re-copies the catalog's, which is
 * exactly why such an edit needs refreshPackages.
 */
export function mergeDungeon(live, data) {
  const out = { ...(obj(live) && obj(live.content) ? live.content : {}), ...data };
  if (obj(out.rewards) && Array.isArray(out.rewards.drops)) {
    out.rewards = { ...out.rewards, drops: out.rewards.drops.map((d) => (obj(d) && "package" in d ? (({ package: _p, ...rest }) => rest)(d) : d)) };
  }
  return out;
}

/**
 * Content as the server stores it, so a sent value and its read-back compare by meaning: zod's
 * defaults filled for undefined members (never for null), the name trimmed, an expiry reduced to
 * its ISO instant (the column is JSON, so a Date reads back as a string), and package snapshots
 * set aside (server-owned). Anything malformed is left as it is and so compares unequal.
 */
export function normalizeDungeon(c) {
  if (!obj(c)) return c;
  const fill = (defaults, o) => {
    const r = { ...o };
    for (const [k, v] of Object.entries(defaults)) if (r[k] === undefined) r[k] = structuredClone(v);
    return r;
  };
  const n = fill(D.content, c);
  if (str(n.name)) n.name = n.name.trim();
  if (n.expiresAt !== null && validDate(n.expiresAt)) n.expiresAt = new Date(n.expiresAt).toISOString();
  if (Array.isArray(n.tiers)) {
    n.tiers = n.tiers.map((t) => (Array.isArray(t) ? t.map((f) => (obj(f) && Array.isArray(f.waves) ? { ...f, waves: f.waves.map((w) => (obj(w) ? fill(D.wave, w) : w)) } : f)) : t));
  }
  if (obj(n.rewards)) {
    n.rewards = fill(D.rewards, n.rewards);
    if (Array.isArray(n.rewards.drops)) n.rewards.drops = n.rewards.drops.map((d) => (obj(d) ? fill(D.drop, (({ package: _p, ...rest }) => rest)(d)) : d));
  }
  return n;
}

/** Read-back diff for the asserted keys of a dungeon edit or create, by normalized meaning. */
export function dungeonDiffs(asserted, liveContent) {
  const a = normalizeDungeon(asserted), l = normalizeDungeon(obj(liveContent) ? liveContent : {});
  const diffs = [];
  for (const k of Object.keys(asserted)) if (!deepEqualPayload(a[k], l[k])) diffs.push({ key: k, sent: asserted[k], live: obj(liveContent) ? liveContent[k] : undefined });
  return diffs;
}

/** Every content field a create would store that this row stores differently (defaults applied). */
export function contentDiffKeys(planned, liveContent) {
  const a = normalizeDungeon(planned), l = normalizeDungeon(obj(liveContent) ? liveContent : {});
  const keys = new Set([...Object.keys(a), ...Object.keys(l)]);
  return [...keys].filter((k) => !deepEqualPayload(a[k], l[k]));
}

/** The dungeon name of a getAll row. */
export const dungeonName = (row) => (obj(row) && obj(row.content) ? row.content.name : undefined);
