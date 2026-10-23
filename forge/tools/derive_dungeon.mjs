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
  const b = s.indexOf(end, a + start.length);
  if (b < 0) fail(`missing end ${JSON.stringify(end)} after ${start}`);
  return s.slice(a, b);
};
const keys = (s, indent) => [...s.matchAll(new RegExp(`^ {${indent}}(\\w+):`, "gm"))].map((m) => m[1]);
const quoted = (s) => [...s.matchAll(/"([\w-]+)"/g)].map((m) => m[1]);
const one = (s, re, what) => { const m = s.match(re); if (!m) fail(`missing ${what}`); return m; };

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
  // `limited` means "carries ratelimitMiddleware": public procedures do by construction, and a
  // protected one does when it composes the middleware itself (dungeon.save does).
  const limited = auth === "public" || /^\s*\.use\(ratelimitMiddleware\)/m.test(body);
  return { kind: /\.mutation\(/.test(body) ? "mutation" : "query", limited, mcp: /mcp:/.test(body), auth };
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
  const floorBlock = block(validator, "export const dungeonFloorSchema", "/** Shared editor/server contract");
  const contentBlock = block(validator, "export const dungeonContentSchema", ".superRefine(");
  const rewardsBlock = block(contentBlock, "rewards: z.object({", "}),");
  const waveBlock = block(coop, "export const encounterWaveSchema", "});");

  // The content object's own keys are at four spaces; rewards' keys at six.
  const contentFields = keys(contentBlock, 4);
  const rewardFields = keys(rewardsBlock, 6);
  // Only the object body: the refinement below it also has 4-space keys (path, message).
  const dropFields = keys(block(dropBlock, ".object({", "  .refine("), 4);
  const floorFields = keys(floorBlock, 2);
  const waveFields = keys(waveBlock, 2);

  const floorKinds = quoted(one(floorBlock, /kind: z\.enum\(\[([^\]]+)\]\)/, "floor kind enum")[1]);
  const dropTypes = quoted(one(dropBlock, /type: z\.enum\(\[([^\]]+)\]\)/, "drop type enum")[1]);
  const biomes = quoted(block(constants, "export const COMBAT_BIOMES = [", "] as const"));

  const nameMax = Number(one(contentBlock, /name: z\.string\(\)\.trim\(\)\.min\(1[^)]*\)\.max\((\d+)\)/, "name bound")[1]);
  const descriptionMax = Number(one(contentBlock, /description: z\.string\(\)\.max\((\d+)\)/, "description bound")[1]);
  const scale = one(mapLocation, /structureScale: z\.coerce\.number\(\)\.min\(([\d.]+)\)\.max\(([\d.]+)\)\.prefault\(([\d.]+)\)/, "structureScale bounds");
  const assetMax = Number(one(mapLocation, /structureAssetId: z\.string\(\)\.max\((\d+)\)/, "structureAssetId bound")[1]);
  const chance = one(dropBlock, /chance: z\.number\(\)\.min\((\d+)\)\.max\((\d+)\)/, "chance bounds");

  // Refinements the validator mirrors. Their presence is asserted so a removed rule is noticed.
  one(validator, /expected = last\s*\?\s*"boss"\s*:\s*fi === DUNGEON_FLOORS_PER_TIER - 1\s*\?\s*"mini-boss"\s*:\s*"floor"/, "floor-kind refinement");
  one(validator, /floor\.waves\[0\]\?\.delayRounds !== 0/, "first-wave refinement");
  one(dropBlock, /drop\.type !== "jutsu" \|\| drop\.quantity === 1/, "jutsu quantity refinement");
  one(rewardsLib, /export const dungeonRewardError/, "reward bound check");
  one(router, /effect\.rewardMode === "weightedCache"/, "cache drop rule");
  one(router, /mapAsset\.id, input\.content\.structureAssetId/, "entrance asset lookup (mapAsset)");
  one(router, /return \{ success: true, message: "Dungeon saved\.", id \};/, "save response shape");

  const bounds = {
    nameMax, descriptionMax,
    structureAssetIdMax: assetMax,
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
    chance: { min: Number(chance[1]), max: Number(chance[2]) },
    maxRewardQuantity: c("DUNGEON_MAX_REWARD_QUANTITY"),
    maxRewardAmount: c("DUNGEON_MAX_REWARD_AMOUNT"),
    maxGrantedItems: c("DUNGEON_MAX_GRANTED_ITEMS"),
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
    contentFields, rewardFields, dropFields, floorFields, waveFields,
    floorKinds, dropTypes, biomes, bounds, facts, procedures,
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
