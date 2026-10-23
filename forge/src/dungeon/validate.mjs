import CONTRACT from "./contract.json" with { type: "json" };
export { CONTRACT };

// Pre-send validation for dungeon definitions (state/prompt_forge_dungeon_recipe.md).
//
// The manifest's `data` is the dungeon's `content` object: dungeon.save takes {id?, content} and
// replaces the whole content, so an edit is checked against live content merged with the
// asserted keys, exactly what the runner will send. Every rule here mirrors one in the pinned
// source (dungeonContentSchema and its superRefine, dungeonDropSchema, encounterWaveSchema,
// mapLocationFields, dungeonRewardError); bounds come from contract.json, derived from the pin by
// tools/derive_dungeon.mjs, never typed in by hand.
//
// Checked at save by the server and NOT here, because they need live rows: that each AI, item,
// jutsu and package exists; that a cache drop is a weighted cache; that the entrance asset
// exists; package contents' share of the reward bounds.

export const isDungeonEntity = (e) => e === "dungeon";
export const dungeonFields = () => new Set(CONTRACT.contentFields);

const B = CONTRACT.bounds;
const obj = (v) => v && typeof v === "object" && !Array.isArray(v);
const str = (v) => typeof v === "string";
const num = (v) => typeof v === "number" && Number.isFinite(v);
const int = (v, min, max) => Number.isSafeInteger(v) && v >= min && v <= max;
const isRef = (v) => str(v) && v.startsWith("@");

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

function unknownKeys(o, allowed, where, out) {
  for (const k of Object.keys(o)) if (!allowed.includes(k)) out.push(`${where}: unknown key "${k}" (the server's validator would drop it silently)`);
}

/**
 * Problems with one dungeon content payload.
 * @param {object} data      asserted content keys (refs may be unresolved: offline checks)
 * @param {object|null} live live content, projected from dungeon.getAll (edits only)
 * @param {{preCreate?: boolean}} [opts] preCreate: no live row; `data` is the whole content
 * @returns {string[]}
 */
export function dungeonProblems(data, live = null, { preCreate = false } = {}) {
  if (!obj(data)) return ["data must be the dungeon content object"];
  const out = [];
  unknownKeys(data, CONTRACT.contentFields, "content", out);
  if (preCreate && data.hidden !== true) out.push("a dungeon create must carry hidden:true (everything ships hidden; publishing is a separate step)");
  if (!preCreate && !live) return out; // keys only until the live content is known
  const d = { ...(preCreate ? {} : pickContent(live)), ...data };
  const check = (ok, message) => { if (!ok) out.push(message); };

  check(str(d.name) && d.name.trim().length >= 1 && d.name.trim().length <= B.nameMax, `name must contain 1..${B.nameMax} characters`);
  check(d.description === undefined || (str(d.description) && d.description.length <= B.descriptionMax), `description must be text of at most ${B.descriptionMax} characters`);
  check(d.structureAssetId === undefined || (str(d.structureAssetId) && d.structureAssetId.length <= B.structureAssetIdMax && !isRef(d.structureAssetId)),
    "structureAssetId must be a literal map-structure asset id (a mapAsset row, not a gameAsset; no ref type exists for it) or empty");
  check(d.structureScale === undefined || (num(d.structureScale) && d.structureScale >= B.structureScale.min && d.structureScale <= B.structureScale.max),
    `structureScale must be ${B.structureScale.min}..${B.structureScale.max}`);
  check(int(d.sector, B.sector.min, B.sector.max), `sector must be an integer ${B.sector.min}..${B.sector.max}`);
  check(int(d.longitude, B.longitude.min, B.longitude.max), `longitude must be an integer ${B.longitude.min}..${B.longitude.max}`);
  check(int(d.latitude, B.latitude.min, B.latitude.max), `latitude must be an integer ${B.latitude.min}..${B.latitude.max}`);
  check("expiresAt" in d && (d.expiresAt === null || d.expiresAt instanceof Date || (str(d.expiresAt) && !Number.isNaN(Date.parse(d.expiresAt)))),
    "expiresAt is required: null for no expiry, or a date");
  check(d.hidden === undefined || typeof d.hidden === "boolean", "hidden must be boolean");
  check(d.background === undefined || CONTRACT.biomes.includes(d.background), `background must be one of ${CONTRACT.biomes.join(", ")}`);

  tierProblems(d.tiers, out);
  rewardProblems(d.rewards, out);
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
        const delay = wave.delayRounds ?? 0;
        if (!int(delay, 0, B.maxWaveDelayRounds)) out.push(`${w}.delayRounds must be an integer 0..${B.maxWaveDelayRounds}`);
        else if (wi === 0 && delay !== 0) out.push(`${w}.delayRounds must be 0: the first wave starts immediately`);
      });
    });
  });
}

function rewardProblems(rewards, out) {
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
  const drops = rewards.drops ?? [];
  if (!Array.isArray(drops) || drops.length > B.maxDrops) { out.push(`rewards.drops must hold at most ${B.maxDrops} drops`); return; }
  let items = 0;
  drops.forEach((drop, i) => {
    const where = `rewards.drops[${i}]`;
    if (!obj(drop)) { out.push(`${where} must be an object`); return; }
    unknownKeys(drop, CONTRACT.dropFields, where, out);
    if ("package" in drop) out.push(`${where}.package: the server copies the catalog snapshot at save and ignores a sent payload; omit it`);
    if (!CONTRACT.dropTypes.includes(drop.type)) { out.push(`${where}.type must be one of ${CONTRACT.dropTypes.join(", ")}`); return; }
    const p = idProblem(drop.id, REF_FOR_DROP[drop.type], `${where}.id`);
    if (p) out.push(p);
    if (!(num(drop.chance) && drop.chance >= B.chance.min && drop.chance <= B.chance.max)) out.push(`${where}.chance must be ${B.chance.min}..${B.chance.max}`);
    const quantity = drop.quantity ?? 1;
    if (!int(quantity, 1, B.maxRewardQuantity)) out.push(`${where}.quantity must be an integer 1..${B.maxRewardQuantity}`);
    else if (drop.type === "jutsu" && quantity !== 1) out.push(`${where}.quantity must be 1: jutsu rewards can only be learned once`);
    else if (drop.type === "item" || drop.type === "cache") items += quantity;
  });
  // dungeonRewardError: every drop assumed to succeed. Package contents count too, but only the
  // server holds their snapshot, so this is a lower bound and the save still checks the rest.
  if (items > B.maxGrantedItems) out.push(`rewards: up to ${items} items per player exceeds ${B.maxGrantedItems} (dungeonRewardError)`);
}

/** The content keys of a live projection, without the row's id and timestamps. */
export function pickContent(live) {
  const out = {};
  if (!obj(live)) return out;
  for (const k of CONTRACT.contentFields) if (live[k] !== undefined) out[k] = live[k];
  return out;
}

/**
 * A dungeon.getAll row as the runner reads it: the content's keys beside the row's id and
 * updatedAt. undefined stays undefined (no such definition), so "no record" still reads as one.
 */
export function dungeonRow(row) {
  if (!obj(row)) return row ?? undefined;
  return { ...(obj(row.content) ? row.content : {}), id: row.id, updatedAt: row.updatedAt };
}
