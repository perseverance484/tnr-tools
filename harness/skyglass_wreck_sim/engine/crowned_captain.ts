/**
 * The Crowned Captain (Crownhold D5.BOSS, live id 7QofodAiUwIoM-voiA2p6): solo boss fight, offline.
 *
 * One "average" endgame player vs the boss in a plain QUEST battle (Crownhold is an isolated
 * battlepyramid quest; its start_battle objective calls initiateBattle(..., "QUEST"), so the grid is
 * getDefaultBattleSizes("QUEST", 100) = 12 x 10). The boss's record, kit, rules and every new jutsu are
 * built here from tuning parameters, validated against the live schemas, run through the engine, and
 * exported as a build spec.
 *
 *   TNR_SCRIPT=crowned_captain.ts run.sh [--params p.json] [--seeds 40] [--seed 1] [--dodge both|on|off]
 *        [--out results.json] [--write-spec spec.json] [--trace SEED] [--debug] [--debugfx] [--probe-inject]
 *
 * Player auto-combat: the harness rotation (engine/model.ts playerRules). Dodge rule (declared test
 * input, harness-side, executed through the engine's own move / Replacement Technique actions):
 *   1. at each of the player's action steps, if they stand on a hex marked by a live danger telegraph
 *      (tg_heavy / tg_control ground mark), step to the nearest unmarked free hex (Replacement
 *      Technique when it is 2+ steps away, within 5 and off cooldown; otherwise one Move step);
 *      if rooted (no Move available, e.g. Keelbind), use the basic Cleanse first when it is ready;
 *   2. never end an action on a marked hex: an auto-combat move onto one is replaced by ending the turn.
 *
 *   --probe-inject [--probe-out f.json]: toolkit probe, can a ground tile grant injectjutsus.
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { performAIaction } from "@/libs/combat/ai_v2";
import { availableUserActions, actionPointsAfterAction, performBattleAction, stillInBattle } from "@/libs/combat/actions";
import { applySageModeAfterRoundTransition } from "@/libs/combat/process";
import { alignBattle, getBattleGrid, getDefaultBattleSizes } from "@/libs/combat/util";
import { AiRule } from "@/validators/ai";
import { insertAiSchema } from "@/validators/aiInput";
import { ItemValidator, JutsuValidator } from "@/validators/combat";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, playerQueryUser, playerRules, queryShell } from "./model";
import { assembleFloor, mulberry32 } from "./sim";

const args = process.argv.slice(2);
const opt = (k: string, d?: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : d;
};
const H = process.env.TNR_HARNESS!;
const IN = loadJson(join(H, "data/crowned_captain_inputs.json"));
const baseline = loadJson(join(H, "data/baseline.json"));
const dmg = loadDmgConfig(H, opt("dmg-config", "live"));

/* ------------------------------------------------------------------ parameters */
export const DEFAULTS = {
  name: "tuned",
  // Record. HP = 5050 x poolsMultiplier. statsMultiplier: push/272 value; every JONIN-rank stat is capped
  // in battle (capUserStats: offence/defence 1.3M, generals 400k), so it changes nothing above ~4.7.
  poolsMultiplier: 2.5,
  statsMultiplier: 5.83,
  idgRows: 1.75, // innate increasedamagegiven rows: 1.75 = one +100% row and one +75% row (rows multiply: x3.5)
  // Arena (12 x 10, FLAT, odd columns offset)
  throne: [9, 4] as [number, number],
  safeStars: [[7, 1], [5, 4], [8, 8]] as [number, number][], // each 4 hexes from the throne: in jutsu range
  // Set pieces
  crownfallPower: 180, crownfallCd: 4,
  commandPower: 130, commandStunAp: 60, commandStunRounds: 2, commandSealRounds: 2, commandCd: 8,
  shardPower: 180,
  // Recall (echo: Sanctum Vanguard)
  echoHp: 2500, echoPower: 70, echoRounds: 3, recallCd: 8,
  recallTarget: "EMPTY_GROUND_CLOSEST_TO_SELF" as string,
  // Kit cooldown overrides (record id -> cooldown); empty = live values
  cooldowns: {} as Record<string, number>,
};
type Params = typeof DEFAULTS;
const P: Params = { ...DEFAULTS, ...(opt("params") ? loadJson(resolve(opt("params")!)) : {}) };

/* ------------------------------------------------------------------ geometry */
const SIZE = getDefaultBattleSizes("QUEST" as never, 100)!;
const GRID = getBattleGrid(1, { width: SIZE.width, height: SIZE.height } as never);
type Cell = [number, number];
const hexAt = (c: Cell) => GRID.getHex({ col: c[0], row: c[1] })!;
const dist = (a: Cell, b: Cell) => GRID.distance(hexAt(a), hexAt(b));
const ALL: Cell[] = GRID.toArray().map((h) => [h.col, h.row] as Cell);
const key = (c: Cell) => `${c[0]},${c[1]}`;
const color = (c: Cell) => {
  const h = hexAt(c);
  return (((h.q - h.r) % 3) + 3) % 3;
};
const T = P.throne;
// Cube line between two hexes (axial lerp + round), excluding the start.
const lineCells = (a: Cell, b: Cell): Cell[] => {
  const A = hexAt(a);
  const B = hexAt(b);
  const n = GRID.distance(A, B);
  const out: Cell[] = [];
  for (let i = 1; i <= n; i++) {
    const t = i / n;
    const q = A.q + (B.q - A.q) * t + 1e-6;
    const r = A.r + (B.r - A.r) * t + 1e-6;
    const s = -q - r;
    let rq = Math.round(q), rr = Math.round(r);
    const rs = Math.round(s);
    const dq = Math.abs(rq - q), dr = Math.abs(rr - r), ds = Math.abs(rs - s);
    if (dq > dr && dq > ds) rq = -rr - rs;
    else if (dr > ds) rr = -rq - rs;
    const h = GRID.getHex({ q: rq, r: rr });
    if (h) out.push([h.col, h.row]);
  }
  return out;
};
const uniq = (cs: Cell[]) => [...new Map(cs.map((c) => [key(c), c])).values()];
/** Crownfall: five rays west from the throne (a fan), the throne itself excluded. */
const CROWNFALL: Cell[] = uniq(
  [[0, 0], [0, 2], [0, T[1]], [0, 7], [0, 9]].flatMap((t) => lineCells(T, t as Cell)),
).filter((c) => key(c) !== key(T));
const STARS: Cell[] = P.safeStars;
const COMMAND: Cell[] = ALL.filter((c) => !STARS.some((s) => key(s) === key(c)));
/** Shardstorm pattern k: every hex of 3-colour k (a third of the hall; each hex's six neighbours carry
 * the other two colours, so a clear hex is always one step away). A third, not two thirds: when he acts
 * before the player in a round, last volley's 1-round mark is still on the floor beside the new one,
 * and with two-thirds patterns the two would cover every hex. The throne is never marked. */
const SHARD_DANGER = [0, 1, 2].map((k) => ALL.filter((c) => color(c) === k && key(c) !== key(T)));
const SHARD_SAFE = [0, 1, 2].map((k) => ALL.filter((c) => color(c) !== k));

/* ------------------------------------------------------------------ records */
const J = (id: string) => structuredClone(IN.jutsu[id]?.record ?? IN.oldKit[id]?.record);
const TEMPLATE = J("EQ93LX8wvuIAd5u75q_i1"); // Ruin Refrain: a complete captured AI jutsu row (field set donor)
const DONOR_GROUND = J(IN.donors.ground);
const DONOR_SUMMON = J(IN.donors.summon);
const ID = {
  oniHunger: "w4F7-w5ubgKsqYPBPvRuV", stolenForm: "VuFuBtE7h5B1nnA2J1lFZ", purging: "HcAs8gBtvopPZkjP8HCC2",
  veilstep: "IBjVpLutojh3m9PRnIce-", windSpear: "A5HrHSzx4J3WM4Fln8Lbf", hexweave: "_JRHgRL8pfUvt_-q1Xa3H",
  extermination: "EqZsaqser8c2-KpVCaXk_", scorchingRend: "Uou0sCjZ1rwiMJZ-JWEI_", devouringGrasp: "lft52q7DE_JjhR7PKXimB",
  lastDirective: "GHFMU_DDKvBBp5BEuTeah", finalCommand: "X2P22h8ApDmTZHjWpNO87", keelbind: "PdD44PGaNv4MN5fOALhAF",
  ruinRefrain: "EQ93LX8wvuIAd5u75q_i1",
  countermand: "W3lOjQhhIPUYPkIZmiNum", solarBow: "ALqXVSL58QMfJ4DgoJ5Il", crossbow: "LbccOnzfsADLgTBPSHjKK",
  // New Crownhold-only records (placeholder ids until created; the spec names them by srcId)
  crownsWill: "cc-crowns-will", crownfallMark: "cc-crownfall-mark", crownfall: "cc-crownfall",
  commandMark: "cc-command-absolute-mark", command: "cc-command-absolute", recall: "cc-recall",
  shardOpen: "cc-shardstorm-open", shardAB: "cc-shardstorm-ab", shardBC: "cc-shardstorm-bc", shardCA: "cc-shardstorm-ca",
};
const NEW_IDS = new Set(Object.entries(ID).filter(([, v]) => v.startsWith("cc-")).map(([, v]) => v));
const IMG = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp";

const tagBase = (type: string, over: Record<string, unknown> = {}) => ({
  type, power: 1, powerPerLevel: 0, rounds: 0, target: "INHERIT", direction: "offence", calculation: "static",
  description: "", appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "",
  disappearAnimation: "", ...over,
});
const coords = (cells: Cell[], selection: "ALL" | "EXCLUDE" = "ALL") => ({
  origin: "BATTLEFIELD", selection, coordinates: cells.map((c) => ({ longitude: c[0], latitude: c[1] })), randomCount: 1,
});
const fx = {
  visual: (anim: string, rounds: number, cells?: Cell[]) => tagBase("visual", {
    rounds, staticAnimation: anim, description: "A battlefield visual effect",
    ...(cells ? { target: "COORDINATES", coordinateTargeting: coords(cells) } : {}),
  }),
  /** Primed marker on the caster, 1 round, one harmless effect TYPE per set piece (see MARKERS). */
  marker: (type: string, anim = "") => tagBase(type, {
    power: type.endsWith("aggro") ? 1 : 100, rounds: 1, target: "SELF", appearAnimation: anim,
    ...(type.endsWith("aggro") ? { calculation: "percentage", aggroMode: "GENERATION" } : {}),
    description: "Primed: the set piece lands next turn",
  }),
  damage: (power: number, anim: string, cells?: Cell[]) => tagBase("damage", {
    power, calculation: "formula", appearAnimation: anim, friendlyFire: "ENEMIES", description: "Deals damage",
    statTypes: ["None"], generalTypes: ["Highest"], elements: [], dmgModifier: 1, residualModifier: 1,
    allowBloodlineDamageDecrease: true, allowBloodlineDamageIncrease: true,
    ...(cells ? { target: "COORDINATES", coordinateTargeting: coords(cells) } : {}),
  }),
  stun: (ap: number, rounds: number) => tagBase("stun", { power: 100, rounds, apReduction: ap, friendlyFire: "ENEMIES", description: "Stuns the target" }),
  seal: (rounds: number) => tagBase("seal", { power: 100, rounds, friendlyFire: "ENEMIES", description: "Seals the target's bloodline effects" }),
};
const jutsuRecord = (id: string, over: Record<string, unknown>) => ({
  ...structuredClone(TEMPLATE), id, image: IMG, jutsuType: "AI", jutsuRank: "S", hidden: true, injectableInBattle: false,
  battleUsageType: "BOTH", chakraCost: 0, staminaCost: 0, healthCost: 0, chakraCostReducePerLvl: 0,
  staminaCostReducePerLvl: 0, healthCostReducePerLvl: 0, extraBaseCost: 0, requiredRank: "STUDENT", requiredLevel: 1,
  statClassification: "None", elementClassification: "None", jutsuWeapon: "NONE", bloodlineId: null, villageId: null,
  methodSize: null, coordinateTargeting: null, createdAt: "2026-10-28T00:00:00.000Z", updatedAt: "2026-10-28T00:00:00.000Z",
  ...over,
});
/** A set-piece cast: method COORDINATES (BATTLEFIELD origin, so the pattern is the same wherever he stands). */
const setPiece = (id: string, name: string, o: { cells: Cell[]; selection?: "ALL" | "EXCLUDE"; cd: number; ap: number; effects: any[]; target?: string; description: string; battle: string }) =>
  jutsuRecord(id, {
    name, description: o.description, battleDescription: o.battle, target: o.target ?? "GROUND", method: "COORDINATES",
    coordinateTargeting: coords(o.cells, o.selection ?? "ALL"), range: 0, cooldown: o.cd, actionCostPerc: o.ap, effects: o.effects,
  });

/** Primed markers. increasepoolcost (the probe's marker) needs rounds >= 2 in the live schema, and a 2-round
 * marker overlaps the next one, so each set piece gets its own harmless self effect type, 1 round. */
const MK = { crownfall: "fleeprevent", command: "robprevent", A: "onehitkillprevent", B: "increaseaggro", C: "decreaseaggro" };
const shardDet = (from: number, to: number, id: string, name: string) =>
  setPiece(id, name, {
    // 60 AP: a volley also lays the next mark, so the fresh marker's own volley (60) cannot follow in the
    // same turn (40 AP left); the 40 AP that remain go to Purging Stance (Final Stand does not floor DoT).
    cells: SHARD_DANGER[from]!, cd: 0, ap: 60,
    effects: [fx.damage(P.shardPower, "cc_shardstorm"), fx.visual("tg_heavy", 1, SHARD_DANGER[to]!), fx.visual("tg_safe", 1, SHARD_SAFE[to]!), fx.marker([MK.A, MK.B, MK.C][to]!)],
    description: "The crown's shards keep falling. Each volley lands where the last warning stood, and the next is already marked.",
    battle: "Skyglass shards rain from the crown where the ground glowed red. %user turns his gaze, and new hexes begin to burn.",
  });

export const buildNewJutsu = () => {
  const oni = J(ID.oniHunger);
  const rows = [
    jutsuRecord(ID.crownsWill, {
      name: "The Crown's Will", target: "SELF", method: "SINGLE", range: 0, cooldown: oni.cooldown, actionCostPerc: oni.actionCostPerc,
      description: "The Command Crown answers its wearer. Its frost points glint, and every echo in the hall stands straighter.",
      battleDescription: "%user does not rise. \"Another echo come home.\"",
      effects: oni.effects.map((e: any, i: number) => ({ ...e, ...(i === 0 ? { staticAnimation: "cc_crown_aura" } : {}) })),
    }),
    setPiece(ID.crownfallMark, "Crownfall", {
      cells: CROWNFALL, cd: P.crownfallCd, ap: 100, effects: [fx.visual("tg_heavy", 1), fx.marker(MK.crownfall)],
      description: "Red lines fan out from the throne along the floor. Where they run, the crown's shards will fall.",
      battle: "%user lifts his chin. Red lines crack across the floor, fanning out from the throne.",
    }),
    setPiece(ID.crownfall, "Crownfall: the Fall", {
      cells: CROWNFALL, cd: 0, ap: 100, effects: [fx.damage(P.crownfallPower, "cc_crownfall")],
      description: "Frost-pointed shards of the crown fall point-first along the marked lines.",
      battle: "Shards of the crown fall point-first along the red lines.",
    }),
    jutsuRecord(ID.commandMark, {
      name: "Command Absolute", target: "GROUND", method: "COORDINATES", coordinateTargeting: coords(STARS, "EXCLUDE"),
      range: 0, cooldown: P.commandCd, actionCostPerc: 100,
      effects: [fx.visual("tg_control", 1), fx.visual("tg_safe", 1, STARS), fx.marker(MK.command, "cc_phase_shift")],
      description: "Violet chains coil across the whole hall. Three stars of skyglass stay clear.",
      battleDescription: "%user raises one hand. Violet chains coil across the floor; only three stars stay clear.",
    }),
    setPiece(ID.command, "Command Absolute: Kneel", {
      cells: STARS, selection: "EXCLUDE", cd: 0, ap: 100, target: "OTHER_USER",
      effects: [
        { ...fx.damage(P.commandPower, "cc_command_absolute"), target: "INHERIT" },
        { ...fx.stun(P.commandStunAp, P.commandStunRounds), appearAnimation: "dt_control" }, fx.seal(P.commandSealRounds),
      ],
      description: "The crown's sigil stamps down. Every chain locks around whoever stands outside the stars.",
      battle: "\"Kneel.\"",
    }),
    jutsuRecord(ID.recall, {
      ...structuredClone(DONOR_SUMMON), id: ID.recall, name: "Recall", image: IMG, jutsuType: "AI", jutsuRank: "S",
      hidden: true, injectableInBattle: false, battleUsageType: "BOTH", requiredRank: "STUDENT", requiredLevel: 1,
      bloodlineId: null, villageId: null, chakraCost: 0, staminaCost: 0, healthCost: 0,
      target: "EMPTY_GROUND", method: "SINGLE", range: 5, cooldown: P.recallCd, actionCostPerc: 60,
      description: "The crown calls an officer of Crownhold back out of chakra haze. It stands for as long as he commands.",
      battleDescription: "\"Stand, soldier.\" An echo rises at his word.",
      effects: DONOR_SUMMON.effects.filter((e: any) => e.type === "summon").map((e: any) => ({
        ...e, aiId: IN.echo.id, aiHp: P.echoHp, power: P.echoPower, powerPerLevel: 0, rounds: P.echoRounds, appearAnimation: "cc_recall",
      })),
    }),
    setPiece(ID.shardOpen, "Shardstorm", {
      cells: SHARD_DANGER[0]!, cd: 0, ap: 60, effects: [fx.visual("tg_heavy", 1), fx.visual("tg_safe", 1, SHARD_SAFE[0]!), fx.marker(MK.A)],
      description: "The crown begins to break apart above him. Its shards mark the floor where they will fall.",
      battle: "The crown's points crack loose and hang in the air. The floor glows red beneath them.",
    }),
    shardDet(0, 1, ID.shardAB, "Shardstorm: First Volley"),
    shardDet(1, 2, ID.shardBC, "Shardstorm: Second Volley"),
    shardDet(2, 0, ID.shardCA, "Shardstorm: Third Volley"),
  ];
  return rows;
};

/** Kit records (captured) with the Last Directive's cosmetic edit (animation + design log line). */
export const kitRecords = () => {
  const ld = { ...jutsuRecord(ID.lastDirective, {}), ...J(ID.lastDirective), id: ID.lastDirective };
  ld.battleDescription = "\"Preserve command.\" The crown blazes.";
  ld.effects = ld.effects.map((e: any) => (e.type === "finalstand" ? { ...e, staticAnimation: "cc_last_directive", appearAnimation: "cc_phase_shift" } : e));
  const eo = { ...jutsuRecord(ID.extermination, {}), ...J(ID.extermination), id: ID.extermination };
  const recs: Record<string, any> = { [ID.lastDirective]: ld, [ID.extermination]: eo };
  for (const k of ["stolenForm", "purging", "veilstep", "windSpear", "hexweave", "scorchingRend", "devouringGrasp", "finalCommand", "keelbind", "ruinRefrain"] as const)
    recs[ID[k]] = J(ID[k]);
  for (const [id, cd] of Object.entries(P.cooldowns)) if (recs[id]) recs[id] = { ...recs[id], cooldown: cd };
  return recs;
};

/* ------------------------------------------------------------------ rules */
const R = {
  jutsu: (jutsuId: string, target: string, conditions: any[] = [], extra: Record<string, unknown> = {}) =>
    ({ conditions, action: { type: "use_specific_jutsu", jutsuId, target, description: "Select specific jutsu", ...extra } }),
  item: (itemId: string, target: string, conditions: any[] = []) =>
    ({ conditions, action: { type: "use_specific_item", itemId, target, description: "Select specific item" } }),
  end: (conditions: any[] = []) => ({ conditions, action: { type: "end_turn", description: "End turn" } }),
  throne: () => ({ conditions: [], action: { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: T[0], latitude: T[1] }, description: "Move to the throne" } }),
};
const C = {
  hb: (v: number) => ({ type: "health_below", value: v, description: "Health below given percentage" }),
  has: (effectType: string, threshold: number) => ({ type: "has_effect", effectType, threshold, description: "Has effect" }),
  tHas: (effectType: string, threshold: number) => ({ type: "target_has_effect", effectType, threshold, target: "CLOSEST_OPPONENT", description: "Target has effect" }),
  near: (v: number) => ({ type: "distance_lower_than", value: v, target: "CLOSEST_OPPONENT", description: "Distance lower than or equal given value" }),
  far: (v: number) => ({ type: "distance_higher_than", value: v, target: "CLOSEST_OPPONENT", description: "Distance higher than or equal given value" }),
  round: (v: number) => ({ type: "round_lower_than", value: v, description: "Current round is lower than specified value" }),
  noSummon: () => ({ type: "does_not_have_summon", description: "Does not have a summon active" }),
};
const PLAYER = "CLOSEST_OPPONENT";
export const buildRules = () => [
  // The throne: he takes it on his first turn and never leaves (a no-op once there).
  R.throne(),
  // Detonations: the marker left by last turn's telegraph (descending marker power).
  R.jutsu(ID.shardCA, "SELF", [C.has(MK.C, 1)]),
  R.jutsu(ID.shardBC, "SELF", [C.has(MK.B, 1)]),
  R.jutsu(ID.shardAB, "SELF", [C.has(MK.A, 1)]),
  R.jutsu(ID.command, "SELF", [C.has(MK.command, 1)]),
  R.jutsu(ID.crownfall, "SELF", [C.has(MK.crownfall, 1)]),
  // Phase 3 (under 30%): the Last Directive, then Shardstorm every turn; nothing else but Extermination Order.
  R.jutsu(ID.lastDirective, "SELF", [C.hb(30)]),
  // Final Stand does not floor afterburn / poison / drain ticks (process.ts applies them outside
  // applyFinalStandDamage), so under the Directive he purges them first.
  R.jutsu(ID.purging, "SELF", [C.hb(30), C.has("afterburn", 1)]),
  R.jutsu(ID.purging, "SELF", [C.hb(30), C.has("poison", 1)]),
  R.jutsu(ID.shardOpen, "SELF", [C.hb(30)]),
  R.jutsu(ID.extermination, PLAYER, [C.hb(30), C.near(5)]),
  R.end([C.hb(30)]),
  // Phase 2 (60-30%): Command Absolute, Recall, Stolen Form, Extermination Order; duel fillers; then hold.
  R.jutsu(ID.commandMark, "SELF", [C.hb(60)]),
  R.jutsu(ID.recall, P.recallTarget, [C.hb(60), C.noSummon()]),
  R.jutsu(ID.stolenForm, PLAYER, [C.hb(60), C.tHas("increasedamagegiven", 50), C.near(4)]),
  R.jutsu(ID.extermination, PLAYER, [C.hb(60), C.near(5)]),
  R.jutsu(ID.scorchingRend, PLAYER, [C.hb(60), C.near(5)]),
  R.jutsu(ID.devouringGrasp, PLAYER, [C.hb(60), C.near(5)]),
  R.item(ID.countermand, PLAYER, [C.hb(60), C.near(5)]),
  R.end([C.hb(60)]),
  // Phase 1 (100-60%): the duelist.
  R.jutsu(ID.crownsWill, "SELF", [C.round(2)]),
  R.jutsu(ID.veilstep, "SELF", [C.round(5), C.far(7)]),
  R.item(ID.countermand, PLAYER, [C.has("stealth", 1), C.near(5)]),
  R.jutsu(ID.purging, "SELF", [C.has("afterburn", 1)]),
  R.jutsu(ID.windSpear, PLAYER, [C.tHas("shield", 1), C.near(5)]),
  R.jutsu(ID.crownfallMark, "SELF", []),
  R.jutsu(ID.hexweave, PLAYER, [C.near(4)]),
  R.jutsu(ID.finalCommand, PLAYER, [C.near(4)]),
  R.jutsu(ID.keelbind, PLAYER, [C.near(5)]),
  R.jutsu(ID.ruinRefrain, PLAYER, [C.near(5)]),
  R.jutsu(ID.scorchingRend, PLAYER, [C.near(5)]),
  R.jutsu(ID.devouringGrasp, PLAYER, [C.near(5)]),
  R.item(ID.solarBow, PLAYER, [C.near(5)]),
  R.end(),
];

/* ------------------------------------------------------------------ AI record */
const STAT_PER_MULT = 1622255.8 / 5.83; // push/272 readback: the server computes stats from statsMultiplier
const STATS = ["offence", "defence", "strength", "intelligence", "willpower", "speed"] as const;
export const bossEffects = () => [
  ...IN.boss.data.effects,
  ...Array.from({ length: Math.floor(P.idgRows) }, () => tagBase("increasedamagegiven", { power: 100, rounds: 99, calculation: "percentage", description: "Increased damage given" })),
  ...(P.idgRows % 1 ? [tagBase("increasedamagegiven", { power: Math.round((P.idgRows % 1) * 100), rounds: 99, calculation: "percentage", description: "Increased damage given" })] : []),
];
export const KIT = () => [
  ID.crownsWill, ID.stolenForm, ID.purging, ID.veilstep, ID.windSpear, ID.hexweave, ID.extermination, ID.scorchingRend,
  ID.devouringGrasp, ID.lastDirective, ID.finalCommand, ID.keelbind, ID.ruinRefrain,
  ID.crownfallMark, ID.crownfall, ID.commandMark, ID.command, ID.recall, ID.shardOpen, ID.shardAB, ID.shardBC, ID.shardCA,
];
export const aiRecord = () => {
  const d = IN.boss.data;
  return {
    ...d, username: "The Crowned Captain", poolsMultiplier: P.poolsMultiplier, statsMultiplier: P.statsMultiplier,
    ...Object.fromEntries(STATS.map((s) => [s, Math.round(STAT_PER_MULT * P.statsMultiplier * 100) / 100])),
    jutsus: KIT(), effects: bossEffects(), includeDefaultRules: false, rules: buildRules(),
  };
};

/* ------------------------------------------------------------------ battle rows */
const t0 = buildTemplates(baseline, {});
const donorRow = enemyQueryUser(t0.enemies["texZaFi42S3EvJZBwQ8cd"]!); // Deck Warden row: DB field-set donor
const armorDonor = donorRow.items.find((ui: any) => ui.item?.itemType === "ARMOR");
const itemRecord = (id: string) => ({ ...structuredClone(IN.items[ID.solarBow].record), ...structuredClone(IN.items[id].record), id });
const itemRow = (userId: string, id: string, i: number) => {
  const rec = itemRecord(id);
  return { ...structuredClone(armorDonor), id: `cc-item-${i}`, userId, itemId: id, equipped: rec.slot, quantity: 1, isInAuction: false, durability: 100, imbuements: [], item: rec };
};
const userJutsu = (userId: string, rec: any, i: number) => ({
  id: `cc-uj-${userId.slice(0, 6)}-${i}`, userId, jutsuId: rec.id, level: 1, experience: 0, equipped: true, finishTraining: null,
  reskinId: null, activeReskin: null, createdAt: new Date(0), updatedAt: new Date(0), jutsu: rec,
});
const aiRow = (id: string, d: any, statsEach: number, recs: Record<string, any>, rules: any[], effects: any[], items: string[]) => {
  const profile = { id: `profile-${id}`, userId: id, name: d.username, includeDefaultRules: false, rules };
  return {
    ...structuredClone(donorRow), userId: id, username: d.username, level: d.level, rank: d.rank,
    poolsMultiplier: d.poolsMultiplier, statsMultiplier: d.statsMultiplier, regeneration: d.regeneration,
    maxHealth: 5050 * d.poolsMultiplier, curHealth: 5050 * d.poolsMultiplier,
    maxChakra: 5050 * d.poolsMultiplier, curChakra: 5050 * d.poolsMultiplier, maxStamina: 5050 * d.poolsMultiplier, curStamina: 5050 * d.poolsMultiplier,
    ...Object.fromEntries(STATS.map((s) => [s, statsEach])),
    ninjutsuMastery: d.ninjutsuMastery, genjutsuMastery: d.genjutsuMastery, taijutsuMastery: d.taijutsuMastery, bukijutsuMastery: d.bukijutsuMastery,
    effects: structuredClone(effects), aiProfileId: profile.id,
    items: items.map((iid, i) => itemRow(id, iid, i)),
    jutsus: d.jutsus.map((jid: string, i: number) => {
      if (!recs[jid]) throw new Error(`no record for ${jid}`);
      return userJutsu(id, structuredClone(recs[jid]), i);
    }),
    ...queryShell(profile),
  };
};
const allRecords = () => {
  const recs: Record<string, any> = { ...kitRecords() };
  for (const r of buildNewJutsu()) recs[r.id] = r;
  for (const [id, j] of Object.entries<any>(IN.jutsu)) if (!recs[id]) recs[id] = j.record;
  return recs;
};
const BOSS_ID = IN.boss.id as string;
const ECHO_ID = IN.echo.id as string;
const buildRows = () => {
  const recs = allRecords();
  const rec = aiRecord();
  const boss = aiRow(BOSS_ID, rec, rec.offence, recs, rec.rules, rec.effects, IN.boss.data.items.flatMap((it: any) => it.ids));
  const e = IN.echo.data;
  const echo = aiRow(ECHO_ID, e, IN.echo.liveStats.offence, recs, e.rules, e.effects, []);
  return { boss, echo, recs };
};

/* ------------------------------------------------------------------ validation */
export const validateSpec = () => {
  const issues: string[] = [];
  const check = (what: string, r: { success: boolean; error?: any }) => {
    if (!r.success) issues.push(`${what}: ${JSON.stringify(r.error.issues.map((i: any) => `${i.path.join(".")}: ${i.message}`))}`);
  };
  for (const j of buildNewJutsu()) check(`jutsu ${j.name}`, JutsuValidator.safeParse(j));
  const kr = kitRecords();
  check("jutsu The Last Directive (edited)", JutsuValidator.safeParse(kr[ID.lastDirective]));
  for (const r of buildRules()) check(`rule ${JSON.stringify(r.action).slice(0, 60)}`, AiRule.safeParse(r));
  const rec = aiRecord();
  const { rules: _r, jutsus: _j, items: _i, ...aiFields } = rec;
  check("ai record", insertAiSchema.safeParse({ ...aiFields, userId: BOSS_ID, jutsus: rec.jutsus, items: IN.boss.data.items, isAi: true }));
  return issues;
};

/* ------------------------------------------------------------------ the fight */
const SET = {
  [ID.crownfallMark]: ["crownfall", "mark"], [ID.crownfall]: ["crownfall", "land"],
  [ID.commandMark]: ["command", "mark"], [ID.command]: ["command", "land"],
  [ID.shardOpen]: ["shardstorm", "mark"], [ID.shardAB]: ["shardstorm", "land"], [ID.shardBC]: ["shardstorm", "land"], [ID.shardCA]: ["shardstorm", "land"],
} as Record<string, [string, string]>;
const DANGER_CELLS: Record<string, Set<string>> = {
  [ID.crownfall]: new Set(CROWNFALL.map(key)), [ID.command]: new Set(COMMAND.map(key)),
  [ID.shardAB]: new Set(SHARD_DANGER[0]!.map(key)), [ID.shardBC]: new Set(SHARD_DANGER[1]!.map(key)), [ID.shardCA]: new Set(SHARD_DANGER[2]!.map(key)),
};
const DANGER_ANIMS = new Set(["tg_heavy", "tg_control"]);

type Fight = {
  seed: number; dodge: boolean; outcome: string; rounds: number; playerHpPct: number; bossHpPct: number;
  phase2Round: number | null; phase3Round: number | null; ldRound: number | null; throneReached: boolean;
  sets: Record<string, { mark: number; land: number; hit: number; dmg: number }>;
  recalls: number; echoDamage: number; bossIdleTurns: number; bossTurns: number; playerIdleTurns: number; playerTurns: number;
  dodgeMoves: number; blockedMoves: number; cleanses?: number; dmgBySource: Record<string, number>; untelegraphedLands: number;
  trace?: string[];
};

const runFight = async (seed: number, dodge: boolean, trace = false): Promise<Fight> => {
  const rand = mulberry32(seed);
  const orig = Math.random;
  Math.random = rand;
  try {
    const { boss, echo, recs } = buildRows();
    const kit = PLAYER_VARIANTS.average!.jutsuIds;
    const v = { ...PLAYER_VARIANTS.average!, rules: playerRules(kit, t0.jutsu) };
    const player = playerQueryUser(0, v as never, t0.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, t0.jutsu);
    let b = await assembleFloor({
      players: [player], enemyRows: { [BOSS_ID]: boss, [ECHO_ID]: echo }, floor: { kind: "boss", waves: [{ aiIds: [BOSS_ID], delayRounds: 0 }] },
      rand, initialBarriers: true, dmgConfig: dmg.config, mode: "quest",
    });
    // The battle catalog holds every equipped record (processUsersForBattle); make sure ours are there.
    for (const [id, r] of Object.entries(recs)) if (!(b.extraState.jutsus as any)[id]) (b.extraState.jutsus as any)[id] = r;
    const grid = getBattleGrid(1, b);
    const puid = player.userId;
    const pStartHp = b.usersState.find((u) => u.userId === puid)!.curHealth; // incl. the Kitsune set's +max HP
    const bossU = () => b.usersState.find((u) => u.controllerId === BOSS_ID && !u.isSummon)!;
    const bossUid = bossU().userId;
    const f: Fight = {
      seed, dodge, outcome: "stalled", rounds: 0, playerHpPct: 0, bossHpPct: 0, phase2Round: null, phase3Round: null, ldRound: null,
      throneReached: false, sets: Object.fromEntries(["crownfall", "command", "shardstorm"].map((k) => [k, { mark: 0, land: 0, hit: 0, dmg: 0 }])),
      recalls: 0, echoDamage: 0, bossIdleTurns: 0, bossTurns: 0, playerIdleTurns: 0, playerTurns: 0, dodgeMoves: 0, blockedMoves: 0,
      dmgBySource: {}, untelegraphedLands: 0, ...(trace ? { trace: [] } : {}),
    };
    const actionRounds: number[] = [];
    const turnActs = new Map<string, string[]>(); // `${round}:${uid}` -> action ids
    let lastMarkRound = -9;
    let cleanses = 0;
    const marked = (bb: typeof b) =>
      new Set(bb.groundEffects.filter((g: any) => g.type === "visual" && g.creatorId === bossUid && DANGER_ANIMS.has(g.staticAnimation) && (g.rounds ?? 1) > 0).map((g: any) => `${g.longitude},${g.latitude}`));
    const free = (bb: typeof b, c: Cell) =>
      !bb.usersState.some((u) => u.longitude === c[0] && u.latitude === c[1] && stillInBattle(u, bb.usersEffects)) &&
      !bb.groundEffects.some((g: any) => g.type === "barrier" && g.longitude === c[0] && g.latitude === c[1]);
    const outcomeOf = () => {
      const side = (dir: string) => b.usersState.some((u) => u.direction === dir && !u.isSummon && stillInBattle(u, b.usersEffects));
      if (!side("left")) return "lost";
      if (!side("right")) return "won";
      return null;
    };
    const tryAction = (actionId: string, c: Cell) => {
      const pu = b.usersState.find((u) => u.userId === puid)!;
      const action = availableUserActions(b, puid, true, true).find((a) => a.id === actionId);
      if (!action || !actionPointsAfterAction(pu, b, action).canAct) return false;
      const clone = structuredClone(b);
      try {
        const res = performBattleAction({ battle: clone, action, grid, contextUserId: puid, actorId: puid, longitude: c[0], latitude: c[1] });
        b = res.newBattle;
        return true;
      } catch {
        return false;
      }
    };
    /** Dodge step: off a marked hex towards the nearest unmarked free hex. */
    const dodgeStep = () => {
      const pu = b.usersState.find((u) => u.userId === puid)!;
      const here: Cell = [pu.longitude, pu.latitude];
      const m = marked(b);
      if (!m.has(key(here))) return false;
      // Rooted (Keelbind): a player who reads the mark cleanses the root first (basic Cleanse, 60 AP, cd 10).
      if (!availableUserActions(b, puid, true, true).some((a) => a.id === "move")) {
        if (tryAction("cleanse", here)) { cleanses++; return true; }
        return false;
      }
      // BFS over free hexes
      const prev = new Map<string, string | null>([[key(here), null]]);
      const q: Cell[] = [here];
      const found: { c: Cell; d: number }[] = [];
      const depth = new Map<string, number>([[key(here), 0]]);
      while (q.length) {
        const c = q.shift()!;
        const d = depth.get(key(c))!;
        if (d > 0 && !m.has(key(c))) found.push({ c, d });
        if (d >= 10) continue;
        for (const n of ALL) {
          if (prev.has(key(n)) || dist(c, n) !== 1 || !free(b, n)) continue;
          prev.set(key(n), key(c));
          depth.set(key(n), d + 1);
          q.push(n);
        }
      }
      if (!found.length) return false;
      const bp: Cell = [bossU().longitude, bossU().latitude];
      found.sort((a, c) => a.d - c.d || dist(a.c, bp) - dist(c.c, bp));
      const target = found[0]!;
      if (target.d >= 2 && dist(here, target.c) <= 5 && tryAction("replacementTechnique", target.c)) return true;
      let step = key(target.c);
      while (prev.get(step) !== key(here)) step = prev.get(step)!;
      const [sx, sy] = step.split(",").map(Number) as Cell;
      return tryAction("move", [sx, sy]);
    };
    const maxSteps = 60 * 40;
    for (let step = 0; step < maxSteps; step++) {
      const pre = alignBattle(b, actionRounds, puid);
      if (pre.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
      if (b.round > 60) break;
      const actor = pre.actor;
      const human = actor.userId === puid;
      const tk = `${b.round}:${actor.userId}`;
      if (!turnActs.has(tk)) turnActs.set(tk, []);
      const hpBefore = new Map(b.usersState.map((u) => [u.userId, u.curHealth]));
      const pBefore = b.usersState.find((u) => u.userId === puid)!;
      const pPos: Cell = [pBefore.longitude, pBefore.latitude];
      const markedBefore = trace ? marked(b).size : 0;
      if (trace && args.includes("--debugfx")) console.log(`FX r${b.round} ${actor.username}: boss ${b.usersEffects.filter((e: any) => e.targetId === bossUid).map((e: any) => `${e.type}:${e.power}:r${e.rounds}${e.castThisRound ? "*" : ""}`).join(" ")}`);
      if (trace && args.includes("--debug") && markedBefore > 50) {
        const m = marked(b);
        const vis = b.groundEffects.filter((g: any) => g.type === "visual" && g.creatorId === bossUid);
        console.log(`DEBUG r${b.round} ${actor.username} unmarked: ${ALL.filter((c) => !m.has(key(c))).map(key).join(" ")} | visual rounds: ${[...new Set(vis.map((g: any) => `${g.staticAnimation}:${g.rounds}:c${g.createdRound}`))].join(",")} | users: ${b.usersState.map((u) => `${u.username}@${u.longitude},${u.latitude}`).join(" ")}`);
      }
      let actionId: string | undefined;
      if (human && dodge && dodgeStep()) {
        actionId = "dodge";
        f.dodgeMoves++;
      } else {
        const res = performAIaction(b, grid, actor.userId);
        actionId = res.nextActionId;
        if (human && dodge && (actionId === "move" || actionId === "replacementTechnique")) {
          const after = res.nextBattle.usersState.find((u) => u.userId === puid)!;
          if (marked(res.nextBattle).has(`${after.longitude},${after.latitude}`)) {
            f.blockedMoves++;
            actionId = tryAction("wait", pPos) ? "wait" : undefined;
            if (!actionId) b = res.nextBattle;
          } else b = res.nextBattle;
        } else b = res.nextBattle;
      }
      const post = alignBattle(b, actionRounds, puid);
      if (post.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(post.actionRound)) actionRounds.push(post.actionRound);
      if (!actionId && actor.isAutoCombat) b.roundStartAt = new Date(Date.now() - 61_000);
      turnActs.get(tk)!.push(actionId ?? "none");
      // Telemetry
      const pAfter = b.usersState.find((u) => u.userId === puid)!;
      const pLoss = Math.max(0, (hpBefore.get(puid) ?? 0) - pAfter.curHealth);
      const actorName = human ? "player" : actor.userId === bossUid ? "boss" : actor.isSummon ? "echo" : actor.username;
      if (!human && pLoss > 0) {
        const src = actor.isSummon ? "echo" : (SET[actionId ?? ""]?.[0] ?? (b.extraState.jutsus as any)[actionId ?? ""]?.name ?? (b.extraState.items as any)?.[actionId ?? ""]?.name ?? actionId ?? "tick");
        f.dmgBySource[src] = (f.dmgBySource[src] ?? 0) + pLoss;
        if (actor.isSummon) f.echoDamage += pLoss;
      }
      if (actorName === "boss" && actionId && SET[actionId]) {
        const [sp, kind] = SET[actionId]!;
        const s = f.sets[sp]!;
        if (kind === "mark") { s.mark++; lastMarkRound = pre.actionRound; }
        else {
          s.land++;
          if (DANGER_CELLS[actionId]!.has(key(pPos))) { s.hit++; s.dmg += pLoss; }
          if (pre.actionRound - lastMarkRound !== 1) f.untelegraphedLands++;
          lastMarkRound = pre.actionRound;
          if (sp === "shardstorm") lastMarkRound = pre.actionRound; // a volley also marks the next pattern
        }
      }
      if (actorName === "boss" && actionId === ID.recall) f.recalls++;
      if (actorName === "boss" && actionId === ID.lastDirective) f.ldRound = pre.actionRound;
      const bu = bossU();
      const bhp = (100 * bu.curHealth) / bu.maxHealth;
      if (bhp < 60 && f.phase2Round === null) f.phase2Round = pre.actionRound;
      if (bhp < 30 && f.phase3Round === null) f.phase3Round = pre.actionRound;
      if (bu.longitude === T[0] && bu.latitude === T[1]) f.throneReached = true;
      if (trace) {
        const nm = actionId === "dodge" ? "DODGE" : (b.extraState.jutsus as any)[actionId ?? ""]?.name ?? (b.extraState.items as any)?.[actionId ?? ""]?.name ?? actionId;
        f.trace!.push(`r${pre.actionRound} ${actorName.padEnd(6)} ${String(nm).padEnd(30)} p@${pPos} pHP ${Math.round(pAfter.curHealth)} (-${Math.round(pLoss)}) boss ${bhp.toFixed(1)}% AP ${Math.round(actor.actionPoints)} marks ${markedBefore}`);
      }
      const out = outcomeOf();
      if (out) { f.outcome = out; break; }
    }
    // Turn accounting
    for (const [k, acts] of turnActs) {
      const uid = k.split(":")[1];
      const idle = acts.every((a) => a === "wait" || a === "none" || a === "move");
      if (uid === bossUid) { f.bossTurns++; if (idle) f.bossIdleTurns++; }
      if (uid === puid) { f.playerTurns++; if (acts.every((a) => a === "wait" || a === "none")) f.playerIdleTurns++; }
    }
    const pu = b.usersState.find((u) => u.userId === puid)!;
    const bu = bossU();
    f.rounds = b.round;
    f.cleanses = cleanses;
    f.playerHpPct = Math.round((1000 * Math.max(0, pu.curHealth)) / Math.max(pu.maxHealth, pStartHp)) / 10;
    f.bossHpPct = Math.round((1000 * Math.max(0, bu.curHealth)) / bu.maxHealth) / 10;
    return f;
  } finally {
    Math.random = orig;
  }
};

/* ------------------------------------------------------------------ aggregation */
const median = (xs: number[]) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m]! : (s[m - 1]! + s[m]!) / 2;
};
const q = (xs: number[], p: number) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.floor(p * (s.length - 1) + 0.5))]!;
};
const r1 = (x: number | null) => (x === null ? null : Math.round(x * 10) / 10);
const summarise = (fs: Fight[]) => {
  const wins = fs.filter((f) => f.outcome === "won");
  const per = (k: string) => {
    const tot = (fld: "mark" | "land" | "hit" | "dmg") => fs.reduce((s, f) => s + f.sets[k]![fld], 0);
    return { marksPerFight: r1(tot("mark") / fs.length), landsPerFight: r1(tot("land") / fs.length), hitsPerFight: r1(tot("hit") / fs.length),
      hitRatePct: tot("land") ? r1((100 * tot("hit")) / tot("land")) : null, dmgPerHit: tot("hit") ? Math.round(tot("dmg") / tot("hit")) : null,
      fightsWithLand: fs.filter((f) => f.sets[k]!.land > 0).length };
  };
  const src: Record<string, number> = {};
  for (const f of fs) for (const [k, v] of Object.entries(f.dmgBySource)) src[k] = (src[k] ?? 0) + v;
  const totSrc = Object.values(src).reduce((a, b) => a + b, 0);
  return {
    fights: fs.length, wins: wins.length, winPct: r1((100 * wins.length) / fs.length),
    roundsWinMedian: median(wins.map((f) => f.rounds)), roundsWinP10: q(wins.map((f) => f.rounds), 0.1), roundsWinP90: q(wins.map((f) => f.rounds), 0.9),
    roundsAllMedian: median(fs.map((f) => f.rounds)),
    hpLeftWinMedian: r1(median(wins.map((f) => f.playerHpPct))), hpLeftWinP10: q(wins.map((f) => f.playerHpPct), 0.1),
    bossHpLeftLossMedian: r1(median(fs.filter((f) => f.outcome !== "won").map((f) => f.bossHpPct))),
    lossPhase: { p1: fs.filter((f) => f.outcome !== "won" && f.phase2Round === null).length, p2: fs.filter((f) => f.outcome !== "won" && f.phase2Round !== null && f.phase3Round === null).length, p3: fs.filter((f) => f.outcome !== "won" && f.phase3Round !== null).length },
    phase2RoundMedian: median(fs.flatMap((f) => (f.phase2Round === null ? [] : [f.phase2Round]))),
    phase3RoundMedian: median(fs.flatMap((f) => (f.phase3Round === null ? [] : [f.phase3Round]))),
    ldCastPct: r1((100 * fs.filter((f) => f.ldRound !== null).length) / fs.length),
    throneReachedPct: r1((100 * fs.filter((f) => f.throneReached).length) / fs.length),
    setPieces: { crownfall: per("crownfall"), command: per("command"), shardstorm: per("shardstorm") },
    untelegraphedLands: fs.reduce((s, f) => s + f.untelegraphedLands, 0),
    recallsPerFight: r1(fs.reduce((s, f) => s + f.recalls, 0) / fs.length),
    bossIdleTurnPct: r1((100 * fs.reduce((s, f) => s + f.bossIdleTurns, 0)) / fs.reduce((s, f) => s + f.bossTurns, 0)),
    playerIdleTurnPct: r1((100 * fs.reduce((s, f) => s + f.playerIdleTurns, 0)) / fs.reduce((s, f) => s + f.playerTurns, 0)),
    dodgeMovesPerFight: r1(fs.reduce((s, f) => s + f.dodgeMoves, 0) / fs.length),
    cleansesPerFight: r1(fs.reduce((s, f) => s + (f.cleanses ?? 0), 0) / fs.length),
    blockedMovesPerFight: r1(fs.reduce((s, f) => s + f.blockedMoves, 0) / fs.length),
    damageShareToPlayerPct: Object.fromEntries(Object.entries(src).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, r1((100 * v) / totSrc)])),
  };
};

/* ------------------------------------------------------------------ main */
const issues = validateSpec();
if (issues.length) {
  console.log("SPEC VALIDATION ISSUES:");
  for (const i of issues) console.log("  " + i);
} else console.log("spec valid against JutsuValidator / AiRule / insertAiSchema");

const specPath = opt("write-spec");
if (specPath) {
  const rec = aiRecord();
  const kr = kitRecords();
  const spec = {
    _note: "The Crowned Captain build spec (Crownhold D5.BOSS). Generated by harness/skyglass_wreck_sim/engine/crowned_captain.ts --write-spec from the tuned parameters; offline engine-tested, not pushed. New jutsu carry placeholder ids (cc-*) to be replaced by the created ids (law 17: literal ids in the AI's jutsus and rules).",
    params: P,
    ai: { id: BOSS_ID, srcId: IN.boss.srcId, record: rec },
    newJutsu: buildNewJutsu(),
    editedJutsu: { [ID.lastDirective]: { note: "existing push/271 record: cosmetic edit only (battleDescription from the design's battle log; finalstand row animations)", battleDescription: kr[ID.lastDirective].battleDescription, effects: kr[ID.lastDirective].effects } },
    kitRemoved: { Braced_Strike: "WvLCyGsPCKSDYl6-e_D9o", Surging_Overflow: "AicYoMMpZmHAykb_5hYtY", Rapid_Fire_live_Shuriken_Storm: "Nrxc8m9utE9qaD_gWpLgf", Worldbreaker_Chorus_live_Great_Bell_Toll: "LisNuMJ2gncEByAxG6QPI", Apex_Hunger_live_Onis_Hunger: "w4F7-w5ubgKsqYPBPvRuV (replaced by its Crownhold-only copy The Crown's Will)" },
    kitAdded: { "Final Command": ID.finalCommand, Keelbind: ID.keelbind, "Ruin Refrain": ID.ruinRefrain },
    recallEcho: { id: ECHO_ID, name: IN.echo.data.username, source: IN.echo.source },
    arena: { grid: SIZE, orientation: "FLAT, odd columns offset (getBattleGrid)", throne: T, crownfall: CROWNFALL, commandStars: STARS, shardstormSafe: SHARD_SAFE, note: "All set-piece patterns are BATTLEFIELD-origin (absolute), so they line up wherever he stands; he moves to the throne on his first turn." },
    animations: { cc_crownfall: ID.crownfall, cc_command_absolute: ID.command, cc_shardstorm: [ID.shardAB, ID.shardBC, ID.shardCA], cc_recall: ID.recall, cc_crown_aura: ID.crownsWill, cc_last_directive: ID.lastDirective, cc_phase_shift: [ID.commandMark, ID.lastDirective], tg_heavy: [ID.crownfallMark, ID.shardOpen, ID.shardAB, ID.shardBC, ID.shardCA], tg_control: ID.commandMark, tg_safe: [ID.commandMark, ID.shardOpen, ID.shardAB, ID.shardBC, ID.shardCA], dt_control: `${ID.command} (the stun row: chains lock; cc_command_absolute is the damage row's sigil stamp)`, dt_heavy: "not used: every heavy detonation here has its boss-scale variant (cc_crownfall, cc_shardstorm), and a visual mark cannot play a disappearAnimation (process.ts expireGroundEffects drops expired visuals without it)" },
    validation: issues.length ? issues : "valid",
  };
  mkdirSync(dirname(resolve(specPath)), { recursive: true });
  writeFileSync(resolve(specPath), `${JSON.stringify(spec, null, 1)}\n`);
  console.log(`wrote ${specPath}`);
}

/* ------------------------------------------------------------------ probe: ground injectjutsus */
/** Toolkit question (director, for later heal / team-buff tiles): can a ground effect grant
 * injectjutsus to a unit that ends a move on it, is the injected jutsu usable (preloaded), is it one-use? */
const probeInject = async (variant: "inject" | "inject_all" | "damage_taken_tile" | "inject_direct") => {
  const rand = mulberry32(1);
  const orig = Math.random;
  Math.random = rand;
  try {
    const { boss, echo, recs } = buildRows();
    const granted = jutsuRecord("cc-probe-granted", {
      ...J("Sic286tbCpCjwaic0EX5q"), id: "cc-probe-granted", name: "Probe: granted bolt", jutsuType: "SPECIAL", injectableInBattle: true,
      cooldown: 20, requiredRank: "STUDENT", requiredLevel: 1, elementClassification: "None", battleUsageType: "BOTH",
    });
    const tile: Cell = [6, 4];
    const grant = setPiece("cc-probe-grant-tile", "Probe: grant tile", {
      cells: [tile], cd: 99, ap: 100, effects: [variant === "damage_taken_tile"
        ? tagBase("increasedamagetaken", { power: 20, rounds: 3, calculation: "percentage", friendlyFire: "ENEMIES", description: "probe" })
        : tagBase("injectjutsus", { jutsuIds: [granted.id], power: 25, rounds: 3, ...(variant === "inject" ? { friendlyFire: "ENEMIES" } : {}), staticAnimation: "tg_safe", description: "Grants a jutsu" })],
      description: "probe", battle: "probe",
    });
    const direct = { ...grant, id: "cc-probe-grant-direct", name: "Probe: grant on the player", target: "OTHER_USER", method: "SINGLE", coordinateTargeting: null, range: 5 };
    const castJ = variant === "inject_direct" ? direct : grant;
    const row = { ...boss, jutsus: [...boss.jutsus, userJutsu(BOSS_ID, castJ, 99)] };
    const profile = { ...row.aiProfile, rules: [R.jutsu(castJ.id, variant === "inject_direct" ? "CLOSEST_OPPONENT" : "SELF", [C.round(2)]), R.end()] };
    row.aiProfile = profile;
    const kit = PLAYER_VARIANTS.average!.jutsuIds;
    const rules = [R.jutsu(granted.id, "CLOSEST_OPPONENT", []), R.end()];
    const player = playerQueryUser(0, { ...PLAYER_VARIANTS.average!, rules } as never, t0.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, t0.jutsu);
    const b0 = await assembleFloor({ players: [player], enemyRows: { [BOSS_ID]: row, [ECHO_ID]: echo }, floor: { kind: "boss", waves: [{ aiIds: [BOSS_ID], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest" });
    let b = b0;
    // Live: initiateBattle preloads every injectableInBattle jutsu into extraState.jutsus (combat.ts ~2321).
    (b.extraState.jutsus as any)[granted.id] = granted;
    for (const [id, r] of Object.entries(recs)) if (!(b.extraState.jutsus as any)[id]) (b.extraState.jutsus as any)[id] = r;
    const puid = player.userId;
    const pu = () => b.usersState.find((u) => u.userId === puid)!;
    const bu = b.usersState.find((u) => u.controllerId === BOSS_ID)!;
    [pu().longitude, pu().latitude] = [5, 4];
    [bu.longitude, bu.latitude] = T;
    const grid = getBattleGrid(1, b);
    const log: string[] = [];
    const actionRounds: number[] = [];
    const has = () => availableUserActions(b, puid, true, true).some((a) => a.id === granted.id);
    const fxOn = () => b.usersEffects.filter((e: any) => e.targetId === puid && e.creatorId === bu.userId).map((e: any) => `${e.type} r${e.rounds}${e.fromGround ? " fromGround" : ""}`);
    let moved = false;
    for (let step = 0; step < 80 && b.round <= 6; step++) {
      const pre = alignBattle(b, actionRounds, puid);
      if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
      const actor = pre.actor;
      if (variant !== "inject_direct" && actor.userId === puid && !moved && b.groundEffects.some((g: any) => g.creatorId === bu.userId && g.type !== "visual")) {
        const mv = availableUserActions(b, puid, true, true).find((a) => a.id === "move")!;
        b = performBattleAction({ battle: structuredClone(b), action: mv, grid, contextUserId: puid, actorId: puid, longitude: tile[0], latitude: tile[1] }).newBattle;
        moved = true;
        log.push(`r${b.round} player MOVES onto the grant tile ${tile}: effects ${JSON.stringify(fxOn())}, granted jutsu available: ${has()}`);
        continue;
      }
      const res = performAIaction(b, grid, actor.userId);
      b = res.nextBattle;
      alignBattle(b, actionRounds, puid);
      const nm = res.nextActionId === granted.id ? "GRANTED JUTSU" : (b.extraState.jutsus as any)[res.nextActionId ?? ""]?.name ?? res.nextActionId;
      log.push(`r${pre.actionRound} ${actor.userId === puid ? "player" : "boss"} ${nm} | player at ${pu().longitude},${pu().latitude} effects ${JSON.stringify(fxOn())} granted available: ${has()} ground: ${b.groundEffects.filter((g: any) => g.creatorId === bu.userId).map((g: any) => `${g.longitude},${g.latitude}:r${g.rounds}`).join(" ") || "-"}`);
    }
    return log;
  } finally {
    Math.random = orig;
  }
};
if (args.includes("--probe-inject")) {
  const log: Record<string, string[]> = {};
  for (const v of ["inject", "inject_all", "damage_taken_tile", "inject_direct"] as const) {
    log[v] = await probeInject(v);
    console.log(`\n### probe: ground tile ${v}`);
    for (const l of log[v]!) console.log("  " + l);
  }
  const out = opt("probe-out");
  if (out) writeFileSync(resolve(out), `${JSON.stringify({ generatedBy: "engine/crowned_captain.ts --probe-inject", log }, null, 1)}\n`);
}

const traceSeed = opt("trace");
if (traceSeed) {
  for (const dodge of [true, false]) {
    const f = await runFight(Number(traceSeed), dodge, true);
    console.log(`--- trace seed ${traceSeed} dodge ${dodge}: ${f.outcome} in ${f.rounds} rounds, player ${f.playerHpPct}%, boss ${f.bossHpPct}%`);
    for (const l of f.trace!) console.log("  " + l);
  }
}

const seeds = Number(opt("seeds", traceSeed ? "0" : "40"));
const seed0 = Number(opt("seed", "1"));
const modes = opt("dodge", "both") === "both" ? [true, false] : [opt("dodge") === "on"];
const results: any = { generatedBy: "engine/crowned_captain.ts", params: P, dmgConfig: dmg.name, grid: SIZE, seeds, seed0, modes: {} };
if (seeds > 0) {
  for (const dodge of modes) {
    const fs: Fight[] = [];
    for (let i = 0; i < seeds; i++) fs.push(await runFight(seed0 + i, dodge));
    const s = summarise(fs);
    results.modes[dodge ? "dodge_on" : "dodge_off"] = { summary: s, fights: fs };
    console.log(`\n== ${P.name} dodge ${dodge ? "ON " : "OFF"}: ${JSON.stringify(s)}`);
  }
}
const outPath = opt("out");
if (outPath) {
  mkdirSync(dirname(resolve(outPath)), { recursive: true });
  writeFileSync(resolve(outPath), `${JSON.stringify(results, null, 1)}\n`);
  console.log(`wrote ${outPath}`);
}
