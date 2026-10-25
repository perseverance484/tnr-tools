// Scoped projection of the game's dungeon content contract (state/prompt_forge_dungeon_recipe.md).
// Deliberately does not refresh fields.json, nested.json or 45c-45g.
// Invoke with a checkout of the exact audited source pin; --check compares bytes.
//
// Every value is read mechanically from the pinned source and every pattern fails closed: a
// source change that moves a key, a bound or a procedure stops this tool instead of producing a
// contract that silently disagrees with the server.
import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

export const PIN = "107d7a86894f806a4c9cec89effef5992118a0ed";
const FILES = Object.freeze({
  validator: "app/src/validators/dungeon.ts",
  router: "app/src/server/api/routers/dungeon.ts",
  coop: "app/src/validators/coop.ts",
  mapLocation: "app/src/validators/mapLocation.ts",
  constants: "app/drizzle/constants.ts",
  rewards: "app/src/libs/dungeonRewards.ts",
});

const fail = (m) => { throw new Error(m); };
const block = (s, start, end) => {
  const a = s.indexOf(start);
  if (a < 0) fail(`missing ${start}`);
  if (s.indexOf(start, a + 1) >= 0) fail(`${start} appears more than once`);
  const b = s.indexOf(end, a + start.length);
  if (b < 0) fail(`missing end ${JSON.stringify(end)} after ${start}`);
  return s.slice(a, b);
};
const quoted = (s) => [...s.matchAll(/"([\w-]+)"/g)].map((m) => m[1]);
const one = (s, re, what) => { const m = s.match(re); if (!m) fail(`missing ${what}`); return m; };

/**
 * The members of one object literal whose keys sit at `indent` spaces, as {key: definition}, the
 * definition with all whitespace removed and its trailing comma dropped. FAILS CLOSED on anything
 * that is not a plain `key: value` member at that indent - a spread, a computed key, a shorthand
 * member - because each of those can add or rename a field this reader would not see.
 */
function members(body, indent, where) {
  const out = {};
  let cur = null;
  for (const line of body.split("\n")) {
    const lead = line.match(/^ */)[0].length;
    const text = line.trim();
    if (!text || lead < indent || text.startsWith("//") || text.startsWith("/*") || text.startsWith("*")) continue;
    // a closing line (`}),`) at the member indent belongs to the member it closes
    if (lead === indent && !/^[\])}]+[,;]?$/.test(text)) {
      const m = text.match(/^(\w+):(.*)$/);
      if (!m) fail(`${where}: unsupported member ${JSON.stringify(text)} (spread, computed or shorthand keys are not read)`);
      if (m[1] in out) fail(`${where}: duplicate key ${m[1]}`);
      cur = m[1];
      out[cur] = m[2];
    } else if (cur) out[cur] += text;
    else fail(`${where}: text before the first member: ${JSON.stringify(text)}`);
  }
  for (const k of Object.keys(out)) out[k] = out[k].replace(/\s+/g, "").replace(/,$/, "");
  return out;
}

/**
 * Match every member of `where` against the exact zod chain this contract understands. The member
 * set must equal the template set: a new, removed or renamed field fails, and so does any change
 * to a field's chain - a bound rebound from its constant to a literal, a dropped .int(), a changed
 * default - because the template no longer matches. Returns {key: regex match}.
 */
function shaped(defs, templates, where) {
  const got = Object.keys(defs), want = Object.keys(templates);
  if (got.join() !== want.join()) fail(`${where}: fields ${got.join(", ")} differ from the understood ${want.join(", ")}`);
  const out = {};
  for (const k of want) {
    const m = defs[k].match(templates[k]);
    if (!m) fail(`${where}.${k}: unrecognised definition ${defs[k]}`);
    out[k] = m;
  }
  return out;
}

const MSG = String.raw`(?:,"[^"]*")?`;
const T = {
  content: {
    name: new RegExp(String.raw`^z\.string\(\)\.trim\(\)\.min\(1${MSG}\)\.max\((\d+)\)$`),
    description: /^z\.string\(\)\.max\((\d+)\)\.prefault\(""\)$/,
    structureAssetId: /^mapLocationFields\.structureAssetId$/,
    structureScale: /^mapLocationFields\.structureScale$/,
    sector: /^z\.number\(\)\.int\(\)\.min\(MAP_SECTOR_ID_MIN\)\.max\(MAP_SECTOR_ID_MAX\)$/,
    longitude: /^z\.number\(\)\.int\(\)\.min\(0\)\.max\(SECTOR_WIDTH-1\)$/,
    latitude: /^z\.number\(\)\.int\(\)\.min\(0\)\.max\(SECTOR_HEIGHT-1\)$/,
    expiresAt: /^z\.coerce\.date\(\)\.nullable\(\)$/,
    hidden: /^z\.boolean\(\)\.prefault\((true|false)\)$/,
    background: /^z\.enum\(COMBAT_BIOMES\)\.prefault\("([\w-]+)"\)$/,
    tiers: /^z\.array\(z\.array\(dungeonFloorSchema\)\.length\(DUNGEON_FLOORS_PER_TIER\)\)\.min\(1\)\.max\(DUNGEON_MAX_TIERS\)$/,
    rewards: /^z\.object\(\{.*\}\)$/,
  },
  rewards: {
    money: /^z\.number\(\)\.min\(0\)\.max\(DUNGEON_MAX_REWARD_AMOUNT\)\.prefault\((\d+)\)$/,
    experience: /^z\.number\(\)\.min\(0\)\.max\(DUNGEON_MAX_REWARD_AMOUNT\)\.prefault\((\d+)\)$/,
    tokens: /^z\.number\(\)\.int\(\)\.min\(0\)\.max\(DUNGEON_MAX_REWARD_AMOUNT\)\.prefault\((\d+)\)$/,
    prestige: /^z\.number\(\)\.int\(\)\.min\(0\)\.max\(DUNGEON_MAX_REWARD_AMOUNT\)\.prefault\((\d+)\)$/,
    drops: /^z\.array\(dungeonDropSchema\)\.max\(DUNGEON_MAX_DROPS\)\.prefault\(\[\]\)$/,
  },
  drop: {
    type: /^z\.enum\(\[((?:"[\w-]+",?)+)\]\)$/,
    id: new RegExp(String.raw`^z\.string\(\)\.min\(1${MSG}\)$`),
    chance: /^z\.number\(\)\.min\((\d+)\)\.max\((\d+)\)$/,
    quantity: /^z\.number\(\)\.int\(\)\.min\(1\)\.max\(DUNGEON_MAX_REWARD_QUANTITY\)\.prefault\((\d+)\)$/,
    package: /^RewardPackageValidator\.optional\(\)$/,
  },
  floor: {
    kind: /^z\.enum\(\[((?:"[\w-]+",?)+)\]\)$/,
    waves: /^z\.array\(encounterWaveSchema\.extend\(\{aiIds:encounterWaveSchema\.shape\.aiIds\.max\(DUNGEON_MAX_MOBS\),?\}\),?\)\.min\(1\)\.max\(DUNGEON_MAX_WAVES\)$/,
  },
  wave: {
    aiIds: new RegExp(String.raw`^z\.array\(z\.string\(\)\.min\(1${MSG}\)\)\.min\(1\)$`),
    delayRounds: /^z\.number\(\)\.int\(\)\.min\(0\)\.max\(ENCOUNTER_MAX_WAVE_DELAY_ROUNDS\)\.prefault\((\d+)\)$/,
  },
  mapLocation: {
    structureAssetId: /^z\.string\(\)\.max\((\d+)\)\.prefault\(""\)$/,
    locationName: /^z\.string\(\)\.trim\(\)\.max\(\d+\)\.prefault\(""\)$/,
    locationDescription: /^z\.string\(\)\.trim\(\)\.max\(\d+\)\.prefault\(""\)$/,
    structureScale: /^z\.coerce\.number\(\)\.min\(([\d.]+)\)\.max\(([\d.]+)\)\.prefault\(([\d.]+)\)$/,
  },
  save: { id: /^z\.string\(\)\.optional\(\)$/, content: /^dungeonContentSchema$/ },
};

/**
 * Evaluate `export const NAME = <expr>;` from constants.ts. Only integer/float literals (with `_`
 * separators and exponents), other constants of the same file, + - * / and parentheses are
 * accepted; anything else fails closed rather than guessing.
 */
function constantEvaluator(src) {
  const memo = new Map();
  const value = (name, stack = []) => {
    if (memo.has(name)) return memo.get(name);
    if (stack.includes(name)) fail(`constant cycle ${[...stack, name].join(" -> ")}`);
    const m = src.match(new RegExp(`^export const ${name}(?::[^=]+)? = ([^;]+);`, "m"));
    if (!m) fail(`missing constant ${name}`);
    // Numeric separators first, so `2_000` is never read as an identifier `_000`.
    const expr = m[1].trim().replace(/(\d)_(?=\d)/g, "$1");
    if (!/^[\w\s+\-*/().]+$/.test(expr)) fail(`constant ${name} is not arithmetic: ${expr}`);
    // Identifiers are names that do not start a number literal (so the `e9` in `1e9` stays put).
    const js = expr.replace(/(?<![\d.])\b[A-Za-z_][A-Za-z0-9_]*/g, (id) => String(value(id, [...stack, name])));
    if (!/^[\d\s+\-*/().e]+$/.test(js)) fail(`constant ${name} did not reduce to arithmetic: ${js}`);
    const v = Function(`"use strict"; return (${js});`)();
    if (!Number.isFinite(v)) fail(`constant ${name} is not finite`);
    memo.set(name, v);
    return v;
  };
  return value;
}

/** Procedure facts for `dungeon.<name>`, from its router section. */
function procedureFacts(router, name) {
  const section = router.match(new RegExp(`^  ${name}: (public|protected)Procedure([\\s\\S]*?)(?=^  \\w+: (?:public|protected)Procedure|(?![\\s\\S]))`, "m"));
  if (!section) fail(`missing procedure dungeon.${name}`);
  const auth = section[1];
  const body = section[2];
  // The kind must be stated, once: a subscription (or anything else) is not a query by default.
  const kinds = [...body.matchAll(/^\s*\.(query|mutation|subscription)\(/gm)].map((m) => m[1]);
  if (kinds.length !== 1 || kinds[0] === "subscription") fail(`dungeon.${name}: expected exactly one .query( or .mutation(, found ${kinds.join(", ") || "none"}`);
  // `limited` means "carries ratelimitMiddleware": public procedures do by construction, and a
  // protected one does when it composes the middleware itself (dungeon.save does).
  const limited = auth === "public" || /^\s*\.use\(ratelimitMiddleware\)/m.test(body);
  return { kind: kinds[0], limited, mcp: /mcp:/.test(body), auth };
}

export function derive(root) {
  const read = (p) => readFileSync(`${root}/${p}`, "utf8");
  const validator = read(FILES.validator);
  const router = read(FILES.router);
  const coop = read(FILES.coop);
  const mapLocation = read(FILES.mapLocation);
  const constants = read(FILES.constants);
  const rewardsLib = read(FILES.rewards);
  const c = constantEvaluator(constants);

  const dropBlock = block(validator, "const dungeonDropSchema", "/** Enemy templates");
  const floorBlock = block(validator, "export const dungeonFloorSchema = z.object({", "\n});");
  const contentBlock = block(validator, "export const dungeonContentSchema", ".superRefine(");
  const contentBody = block(contentBlock, "  .object({", "\n  })\n");
  const rewardsBody = block(contentBody, "rewards: z.object({", "\n    }),");
  const waveBlock = block(coop, "export const encounterWaveSchema = z.object({", "\n});");
  const mapBlock = block(mapLocation, "export const mapLocationFields = {", "\n};");
  const saveBlock = block(validator, "export const saveDungeonSchema = z.object({", "\n});");

  // Each member is matched against its whole zod chain (T above), so the bounds below are the
  // constants the schema is bound to, not just constants that happen to exist.
  const content = shaped(members(contentBody, 4, "dungeonContentSchema"), T.content, "dungeonContentSchema");
  const rewards = shaped(members(rewardsBody.slice(rewardsBody.indexOf("\n")), 6, "rewards"), T.rewards, "rewards");
  // Only the object body: the refinement below it also has 4-space keys (path, message).
  const drop = shaped(members(block(dropBlock, ".object({", "  .refine("), 4, "dungeonDropSchema"), T.drop, "dungeonDropSchema");
  const floor = shaped(members(floorBlock, 2, "dungeonFloorSchema"), T.floor, "dungeonFloorSchema");
  const wave = shaped(members(waveBlock, 2, "encounterWaveSchema"), T.wave, "encounterWaveSchema");
  const map = shaped(members(mapBlock, 2, "mapLocationFields"), T.mapLocation, "mapLocationFields");
  shaped(members(saveBlock, 2, "saveDungeonSchema"), T.save, "saveDungeonSchema");
  one(router, /^  save: protectedProcedure\s*\.use\(ratelimitMiddleware\)\s*\.input\(saveDungeonSchema\)\s*\.mutation\(/m, "save input binding");

  const floorKinds = quoted(floor.kind[1]);
  const dropTypes = quoted(drop.type[1]);
  const biomes = quoted(block(constants, "export const COMBAT_BIOMES = [", "] as const"));
  const background = content.background[1];
  if (!biomes.includes(background)) fail(`background default ${background} is not a biome`);

  // Refinements the validator mirrors. Their presence is asserted so a removed rule is noticed.
  one(validator, /expected = last\s*\?\s*"boss"\s*:\s*fi === DUNGEON_FLOORS_PER_TIER - 1\s*\?\s*"mini-boss"\s*:\s*"floor"/, "floor-kind refinement");
  one(validator, /floor\.waves\[0\]\?\.delayRounds !== 0/, "first-wave refinement");
  one(dropBlock, /drop\.type !== "jutsu" \|\| drop\.quantity === 1/, "jutsu quantity refinement");
  one(rewardsLib, /export const dungeonRewardError/, "reward bound check");
  one(rewardsLib, /total > DUNGEON_MAX_GRANTED_ITEMS/, "granted-item bound binding");
  one(rewardsLib, /amounts\[field\] > DUNGEON_MAX_REWARD_AMOUNT/, "scalar reward bound binding");
  one(router, /effect\.rewardMode === "weightedCache"/, "cache drop rule");
  one(router, /mapAsset\.id, input\.content\.structureAssetId/, "entrance asset lookup (mapAsset)");
  one(router, /drops\.map\(\(\{ package: _snapshot, \.\.\.drop \}\)/, "server-side package snapshot copy");
  one(router, /return \{ success: true, message: "Dungeon saved\.", id \};/, "save response shape");

  const scale = map.structureScale;
  const bounds = {
    nameMax: Number(content.name[1]),
    descriptionMax: Number(content.description[1]),
    structureAssetIdMax: Number(map.structureAssetId[1]),
    structureScale: { min: Number(scale[1]), max: Number(scale[2]), default: Number(scale[3]) },
    sector: { min: c("MAP_SECTOR_ID_MIN"), max: c("MAP_SECTOR_ID_MAX") },
    longitude: { min: 0, max: c("SECTOR_WIDTH") - 1 },
    latitude: { min: 0, max: c("SECTOR_HEIGHT") - 1 },
    maxTiers: c("DUNGEON_MAX_TIERS"),
    floorsPerTier: c("DUNGEON_FLOORS_PER_TIER"),
    maxWaves: c("DUNGEON_MAX_WAVES"),
    maxMobs: c("DUNGEON_MAX_MOBS"),
    maxWaveDelayRounds: c("ENCOUNTER_MAX_WAVE_DELAY_ROUNDS"),
    maxDrops: c("DUNGEON_MAX_DROPS"),
    chance: { min: Number(drop.chance[1]), max: Number(drop.chance[2]) },
    maxRewardQuantity: c("DUNGEON_MAX_REWARD_QUANTITY"),
    maxRewardAmount: c("DUNGEON_MAX_REWARD_AMOUNT"),
    maxGrantedItems: c("DUNGEON_MAX_GRANTED_ITEMS"),
  };
  // What zod fills in for an absent (undefined, never null) member: the read-back comparison
  // normalises both sides with these, so an omitted key and its stored default compare equal.
  const defaults = {
    content: { description: "", structureAssetId: "", structureScale: bounds.structureScale.default, hidden: content.hidden[1] === "true", background },
    rewards: Object.fromEntries([...["money", "experience", "tokens", "prestige"].map((k) => [k, Number(rewards[k][1])]), ["drops", []]]),
    drop: { quantity: Number(drop.quantity[1]) },
    wave: { delayRounds: Number(wave.delayRounds[1]) },
  };
  const facts = {
    partySize: c("DUNGEON_PARTY_SIZE"),
    runSeconds: c("DUNGEON_RUN_SECONDS"),
    inactiveRounds: c("DUNGEON_INACTIVE_ROUNDS"),
  };

  const procedures = {};
  for (const name of ["getAll", "save"]) procedures[`dungeon.${name}`] = procedureFacts(router, name);

  const files = Object.values(FILES);
  return {
    _meta: {
      pin: PIN,
      scope: "Dungeon definitions only (dungeon.save / dungeon.getAll); lobby, run and claim procedures are out of scope",
      sources: Object.fromEntries(files.map((p) => [p, createHash("sha256").update(readFileSync(`${root}/${p}`)).digest("hex")])),
    },
    contentFields: Object.keys(content), rewardFields: Object.keys(rewards), dropFields: Object.keys(drop),
    floorFields: Object.keys(floor), waveFields: Object.keys(wave),
    floorKinds, dropTypes, biomes, bounds, defaults, facts, procedures,
  };
}

function main() {
  const root = process.argv[2];
  if (!root) fail("usage: node tools/derive_dungeon.mjs GAME_CHECKOUT [--check]");
  const actual = execFileSync("git", ["-C", root, "rev-parse", "HEAD"], { encoding: "utf8" }).trim();
  if (actual !== PIN) fail(`expected audited ${PIN}, got ${actual}`);
  for (const p of Object.values(FILES)) {
    const pinned = execFileSync("git", ["-C", root, "show", `${PIN}:${p}`]);
    if (!pinned.equals(readFileSync(`${root}/${p}`))) fail(`dirty source file: ${p}`);
  }
  const out = JSON.stringify(derive(root), null, 2) + "\n";
  const target = fileURLToPath(new URL("../src/dungeon/contract.json", import.meta.url));
  if (process.argv.includes("--check")) {
    const current = readFileSync(target, "utf8");
    if (current !== out) fail("src/dungeon/contract.json differs from a fresh derivation at the pin");
    process.stdout.write("dungeon contract current\n");
    return;
  }
  writeFileSync(target, out);
  process.stdout.write("wrote src/dungeon/contract.json\n");
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
