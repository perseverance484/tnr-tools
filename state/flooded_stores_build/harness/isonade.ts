/**
 * Isonade (The Flooded Stores, The Stores Below): records, AI rows and a solo fight runner. Offline only; zero live
 * requests. Runs inside the Skyglass Wreck harness (fable/mother-of-echoes-act3 harness/skyglass_wreck_sim), whose
 * cclib / kitlib / model / sim modules it imports unchanged. Every record is validated by the live JutsuValidator,
 * AiRule and insertAiSchema. Ids are placeholders (iso-*) to replace with created ids (law 17).
 *
 *   TNR_SCRIPT=isonade.ts run.sh [--params /abs/p.json] [--seeds 40] [--read 1,0.85] [--trace SEED]
 *        [--write-spec /abs/spec.json] [--out /abs/results.json] [--start full|0.7]
 *
 * Design (approved Nov 18, "Stolen Stores: full update design"):
 *   - never moves (no move rule, includeDefaultRules off); body water on the 6 hexes around it from round 1
 *   - Slam: a 40 AP mark lays the red heavy-hit mark on two rows; next turn the 100 AP blast lands, floods those rows
 *     with brine pools (drain tiles, 3 rounds) and leaves a token so the next mark takes the next row pair (A -> B -> C)
 *   - Grasping Arm: one summon at a time, regrows on its jutsu cooldown; it lashes the hexes around it each turn
 *   - Undertow: when the player is 5+ hexes away, the west half of the room is pulled 3 hexes toward it
 *   - Black Water at 75/50/25%: everything but the floating crates goes red; next turn black water hits every hex but
 *     the crates, and Isonade surfaces to feed (x3 damage taken for 1 round)
 *   - Bite of the ship at 50% (once): a 100-round token; from then Slams cost 60 AP (mark + land in one turn, so
 *     they come a turn sooner) and pools last 4 rounds
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { performAIaction } from "@/libs/combat/ai_v2";
import { availableUserActions, actionPointsAfterAction, performBattleAction, stillInBattle } from "@/libs/combat/actions";
import { applySageModeAfterRoundTransition } from "@/libs/combat/process";
import { getTargetTiles } from "@/libs/combat/targeting";
import { alignBattle, getBattleGrid, getEffectiveMaxPool } from "@/libs/combat/util";
import { jutsu, T, tag } from "./kitlib";
import {
  aiRow, ALL, args, C, type Cell, DONOR_SUMMON, dist, dmg, idgRowTags, IN, IMG, jutsuRecord, key, median, opt, quantile, R, r1, SIZE, STAT_PER_MULT, STATS,
  t0, validator, allCapturedRecords,
} from "./cclib";
import { loadJson, petFor, PLAYER_VARIANTS, playerQueryUser, playerRules } from "./model";
import { assembleFloor, mulberry32, seedEntropy, tickClock } from "./sim";
import { assertSpecRuleCap, AI_PROFILE_MAX_RULES } from "./rulecap";

const W = SIZE.width;
const H = SIZE.height;
type XY = { longitude: number; latitude: number };
const xy = (c: Cell): XY => ({ longitude: c[0], latitude: c[1] });
const cellsWhere = (pred: (c: number, r: number) => boolean): Cell[] => {
  const out: Cell[] = [];
  for (let c = 0; c < W; c++) for (let r = 0; r < H; r++) if (pred(c, r)) out.push([c, r]);
  return out;
};
const field = (cells: Cell[], selection: "ALL" | "EXCLUDE" = "ALL") => ({ origin: "BATTLEFIELD", selection, coordinates: cells.map(xy), randomCount: 1 });

/* ------------------------------------------------------------------ parameters */
export const ISO_DEFAULTS = {
  name: "isonade_v1",
  poolsMultiplier: 5.6,
  statsMultiplier: 5.83,
  idgRows: 0, // extra +100% damage-given rows (a negative value is one decreasedamagegiven row)
  slamPower: 140,
  blackWaterPower: 170,
  feedMult: 3,
  poolPct: 8, // brine pool: % of max HP drained each action begun on it
  poolRounds: 3,
  poolRoundsBitten: 4,
  poolKind: "drain" as "drain" | "damage", // "damage": lingering ground damage instead of brine drain (live drain shares a 4-round lock)
  poolPower: 0, // poolKind "damage": formula power of each pool hit; the land's own hit is slamPower - poolPower, so a land still totals slamPower
  armHp: 4000,
  armPower: 60, // summon stat scale (% of Isonade's)
  armRounds: 30, // lifetime: it stays until cut
  armCooldown: 5,
  lashPower: 70,
  undertowPower: 30,
  undertowPull: 3,
  undertowFrom: 5, // player at least this far
  undertowCooldown: 3,
  bodyWaterRounds: 1, // re-laid every turn by the churn
  churnAp: 10, // the validator floor
  landAp: 90,
  bwLandAp: 90, // Black Water land (was landAp)
  bittenChainEnds: false, // the bitten slam on the last rows (C) lays no next mark: the chain runs A, B, C, then a free turn
  bw3At: 25, // health below which the third Black Water is marked
  stunPrevent: false, // innate stunprevent on Isonade (a stun cuts its AP so a marked land cannot be paid for)
  rows: { A: [2, 6], B: [3, 7], C: [4, 8] } as Record<"A" | "B" | "C", number[]>,
  crates: [[6, 1], [4, 5], [6, 9]] as Cell[],
  undertowCols: 4, // columns 0..N are pulled
  markAp: 46, // slam mark: + arm or undertow fits, two marks never do, nor a mark + a bitten slam
  bwMarkAp: 40, // Black Water mark: fits after the churn + a bitten slam
  sideAp: 40, // arm, undertow
  bittenLandAp: 50, // bitten slam (also lays the next mark): + arm fits, two never do
  playerPoolPolicy: "soft" as "soft" | "strict" | "good",
};
export type IsoParams = typeof ISO_DEFAULTS;
const isoParams = (over: any = {}): IsoParams => ({ ...ISO_DEFAULTS, ...over });

/* ------------------------------------------------------------------ ids, markers, animations */
export const BOSS_ID = "iso-isonade";
export const ARM_ID = "iso-grasping-arm";
export const JID = {
  bodyWater: "iso-it-rises",
  mark: { A: "iso-slam-mark-a", B: "iso-slam-mark-b", C: "iso-slam-mark-c" },
  slam: { A: "iso-slam-a", B: "iso-slam-b", C: "iso-slam-c" },
  slamBit: { A: "iso-slam-a-bitten", B: "iso-slam-b-bitten", C: "iso-slam-c-bitten" },
  bwMark: ["iso-black-water-mark-75", "iso-black-water-mark-50", "iso-black-water-mark-25"],
  blackWater: "iso-black-water",
  bite: "iso-bite-of-the-ship",
  arm: "iso-grasping-arm-rises",
  lash: "iso-arm-lash",
  undertow: "iso-undertow",
};
/** Marker / token effect types: each changes nothing for this boss (cooldown and range types list no actions; it
 * never flees or robs; it carries no weapon; its kit is non-elemental). summonprevent is NOT used (it would block the
 * arm), nor onehitkillprevent / sealprevent (real effects on the boss). */
export const MK = {
  A: "increasecooldown", B: "decreasecooldown", C: "increaserange", // slam marks (1 round)
  bw: "fleeprevent", // Black Water mark (1 round)
  tokA: "robprevent", tokB: "disarm", // "rows A / B just landed" (1 round): the next mark takes the next pair
  bite: "elementalseal", // bitten (100 rounds)
  chain: "increaseheal", // a bitten slam landed (1 round): it already laid the next mark, so no other mark this turn
};
export const ANIM = {
  red: "tg_heavy", safe: "tg_safe", bodyWater: "anim_isonade_body_water_v1", slamHit: "anim_isonade_slam_v1", brine: "anim_isonade_brine_v1",
  armBurst: "anim_isonade_arm_burst_v1", armLash: "anim_isonade_arm_lash_v1", blackWater: "anim_isonade_surge_v1", eye: "anim_isonade_eye_v1", bite: "anim_isonade_bite_v1",
  biteDrip: "anim_isonade_rot_drip_v1", undertow: "anim_fx_undertow_v1",
};
const PRIMED = "Primed: the set piece lands next turn";
const marker = (type: string, rounds = 1) => type === "increaseheal"
  ? tag(type, { power: 1, rounds, target: "SELF", calculation: "percentage", description: PRIMED })
  :   tag(type, {
    power: ["increasecooldown", "decreasecooldown", "increaserange"].includes(type) ? 1 : 100, rounds, target: "SELF",
    ...(["increasecooldown", "decreasecooldown", "increaserange"].includes(type) ? { actionsAffected: [], calculation: "static" } : {}),
    description: PRIMED,
  });
const ALL_STATS = ["None", "Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"];
const ALL_GENERALS = ["Highest", "Strength", "Intelligence", "Willpower", "Speed"];

/* ------------------------------------------------------------------ patterns */
const rowsCells = (rows: number[]) => cellsWhere((_c, r) => rows.includes(r));
export const patterns = (P: IsoParams) => ({
  A: rowsCells(P.rows.A), B: rowsCells(P.rows.B), C: rowsCells(P.rows.C),
  crates: P.crates,
  flood: cellsWhere((c, r) => !P.crates.some((x) => x[0] === c && x[1] === r)),
  undertow: cellsWhere((c) => c <= P.undertowCols),
});

/* ------------------------------------------------------------------ records */
export const buildRecords = (P: IsoParams) => {
  const pat = patterns(P);
  const J: Record<string, any> = {};
  const add = (j: any) => (J[j.id] = j);
  const heavy = (power: number, anim: string) => T.damage(power, { appearAnimation: anim });
  add(jutsu(JID.bodyWater, {
    name: "It Rises", description: "Black water churns around Isonade every turn: its body, wedged in the hull breach. Harmless.",
    battleDescription: "Black water churns around %user.",
    target: "GROUND", method: "AOE_SPIRAL_SHOOT", range: 1, cooldown: 1, actionCostPerc: P.churnAp,
    effects: [T.visual(ANIM.bodyWater, P.bodyWaterRounds)],
  }));
  const LINES: Record<string, string> = { A: "Two great arms rise out of the water.", B: "The arms rise again, further along the hold.", C: "The arms lift high over the stores." };
  for (const k of ["A", "B", "C"] as const) {
    add(jutsu(JID.mark[k], {
      name: "Slam", description: "Two arms rise; two rows of the room are marked red. They slam down next turn.",
      battleDescription: LINES[k]!, target: "GROUND", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: P.markAp,
      coordinateTargeting: field(pat[k]), effects: [T.visual(ANIM.red, 1), marker(MK[k])],
    }));
    const next = ({ A: "B", B: "C", C: "A" } as const)[k];
    const slamEffects = (rounds: number, bitten: boolean) => [
      ...(P.poolKind === "damage"
        ? [heavy(P.slamPower - P.poolPower, ANIM.slamHit), T.pool(P.poolPower, rounds, { description: "Brine pool: hits anyone standing in it with every action" })]
        : [heavy(P.slamPower, ANIM.slamHit),
           tag("drain", { power: P.poolPct, rounds, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"], description: "Brine pool: drains health with every action begun on it" })]),
      T.visual(ANIM.brine, rounds),
      ...(bitten && k === "C" && P.bittenChainEnds
        ? []
        : bitten
        ? [T.visual(ANIM.red, 1, { target: "COORDINATES", coordinateTargeting: field(pat[next]) }), marker(MK[next]), marker(MK.chain)]
        : k === "A" ? [marker(MK.tokA)] : k === "B" ? [marker(MK.tokB)] : []),
    ];
    add(jutsu(JID.slam[k], {
      name: "Slam", description: `The arms slam down on the marked rows and flood them with brine for ${P.poolRounds} rounds.`,
      battleDescription: "The arms crash down. Brine wells up through the boards.", target: "GROUND", method: "COORDINATES", range: 0,
      cooldown: 0, actionCostPerc: P.landAp, coordinateTargeting: field(pat[k]), effects: slamEffects(P.poolRounds, false),
    }));
    add(jutsu(JID.slamBit[k], {
      name: "Slam", description: P.bittenChainEnds && k === "C" ? `After the bite: the third slam in a row. The arms come down and stay down, and the brine lasts ${P.poolRoundsBitten} rounds.` : `After the bite: the arms slam and rise again at once (the next rows go red), and the brine lasts ${P.poolRoundsBitten} rounds.`,
      battleDescription: "The arms crash down and rise again at once, dripping rot.", target: "GROUND", method: "COORDINATES", range: 0,
      cooldown: 0, actionCostPerc: P.bittenLandAp, coordinateTargeting: field(pat[k]), effects: slamEffects(P.poolRoundsBitten, true),
    }));
  }
  const BW_LINES = ["The water goes still and black. Only the floating crates stay pale.", "The hold darkens again. The crates bob on black water.", "Everything goes black but the crates."];
  JID.bwMark.forEach((id, i) => add(jutsu(id, {
    name: "Black Water", description: "Everything but the floating crates is marked red. Black water fills the room next turn.",
    battleDescription: BW_LINES[i]!, target: "GROUND", method: "COORDINATES", range: 0, cooldown: 99, actionCostPerc: P.bwMarkAp,
    coordinateTargeting: field(pat.crates, "EXCLUDE"),
    effects: [T.visual(ANIM.red, 1), T.visual(ANIM.safe, 1, { target: "COORDINATES", coordinateTargeting: field(pat.crates) }), marker(MK.bw)],
  })));
  add(jutsu(JID.blackWater, {
    name: "Black Water", description: `Black water fills every hex but the crates; then Isonade surfaces to feed and takes x${P.feedMult} damage for 1 round.`,
    battleDescription: "Black water rises to head height and crashes down. %user surfaces to feed, its great eye open.",
    target: "CHARACTER", method: "COORDINATES", range: 0, cooldown: 1, actionCostPerc: P.bwLandAp, coordinateTargeting: field(pat.crates, "EXCLUDE"),
    effects: [
      heavy(P.blackWaterPower, ANIM.blackWater),
      tag("weakness", { target: "SELF", rounds: 1, dmgModifier: P.feedMult, statTypes: ALL_STATS, generalTypes: ALL_GENERALS, power: 100, staticAnimation: ANIM.eye, description: "Surfaces to feed: takes extra damage" }),
    ],
  }));
  add(jutsu(JID.bite, {
    name: "Bite of the Ship", description: P.bittenChainEnds ? "Once, at half health: Isonade tears off a piece of the hull. From now on it slams three turns running." : "Once, at half health: Isonade tears off a piece of the hull. From now on it slams faster and its brine lasts longer.",
    battleDescription: "%user tears a piece out of the hull. Planks rip inward and vanish into the water.",
    target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: 20,
    effects: [{ ...marker(MK.bite, 100), appearAnimation: ANIM.bite, staticAnimation: ANIM.biteDrip, description: "Bitten: it slams faster" }],
  }));
  add(jutsuRecord(JID.arm, {
    ...structuredClone(DONOR_SUMMON), id: JID.arm, name: "Grasping Arm", image: IMG, jutsuType: "AI", jutsuRank: "S",
    hidden: true, injectableInBattle: false, battleUsageType: "BOTH", requiredRank: "STUDENT", requiredLevel: 1,
    bloodlineId: null, villageId: null, chakraCost: 0, staminaCost: 0, healthCost: 0,
    target: "EMPTY_GROUND", method: "SINGLE", range: 5, cooldown: P.armCooldown, actionCostPerc: P.sideAp,
    description: "An arm bursts up through the deck and lashes everything around it. Cut it, and another grows.",
    battleDescription: "The deck bursts upward. A wet black arm rises out of it.",
    effects: DONOR_SUMMON.effects.filter((e: any) => e.type === "summon").map((e: any) => ({
      ...e, aiId: ARM_ID, aiHp: P.armHp, power: P.armPower, powerPerLevel: 0, rounds: P.armRounds, appearAnimation: ANIM.armBurst, appearSfx: "",
    })),
  }));
  add(jutsu(JID.lash, {
    name: "Arm Lash", description: "The arm sweeps every hex around it.", battleDescription: "The arm lashes across the planks.",
    target: "GROUND", method: "AOE_SPIRAL_SHOOT", range: 1, cooldown: 1, actionCostPerc: 100,
    effects: [heavy(P.lashPower, ANIM.armLash)],
  }));
  add(jutsu(JID.undertow, {
    name: "Undertow", description: `When nobody is in its reach, the water drags the far side of the room ${P.undertowPull} hexes toward Isonade.`,
    battleDescription: "The water pulls hard toward %user.", target: "CHARACTER", method: "COORDINATES", range: 0,
    cooldown: P.undertowCooldown, actionCostPerc: P.sideAp, coordinateTargeting: field(pat.undertow),
    effects: [heavy(P.undertowPower, ANIM.undertow), T.pull(P.undertowPull, { friendlyFire: "ENEMIES" })],
  }));
  return J;
};

/* ------------------------------------------------------------------ rules */
const toPlayer = (type: "distance_lower_than" | "distance_higher_than", value: number) =>
  ({ type, value, target: "HIGHEST_MAX_HEALTH_OPPONENT", description: type === "distance_lower_than" ? "Distance lower than or equal given value" : "Distance higher than or equal given value" });
/** Rule order. Engine facts it rests on (engine 3314d122):
 *  - pin 3314d122 shares a 3-round lock only when the cast action has cooldown > 0, but the LIVE game reads a
 *    per-tag table (misc.getSharedCooldowns; drain 4 rounds) and locks every other action sharing a tag whatever
 *    the cast's cooldown. Run against engwork_live (patched applyActionCooldowns) to model it. Brine (drain)
 *    therefore locks the next slam; poolKind "damage" pools are not in the table. Slam lands carry cooldown 0
 *    and are gated by their marks;
 *  - an AI re-reads its rules from the top after every action and a marker laid this turn already counts,
 *    so action costs keep a mark and its slam out of one turn (churn 10 + mark 46 + slam 90 or bitten slam 50 > 100),
 *    keep two marks and two slams out of one turn, and leave room for the arm or undertow beside either.
 *  - after the bite each slam lays the next mark itself (red rows + marker), so slams land every turn. */
export const isoRules = (P: IsoParams) => [
  // Every turn opens with the churn (10 AP). Besides keeping the body water up, its action clears any marker left
  // over from two turns ago, which the engine otherwise keeps until the round's first action: without it a slam
  // could land a second time, unmarked, when Isonade acts first in a round.
  R.jutsu(JID.bodyWater, "SELF", []),
  // Black Water marked last turn lands first.
  R.jutsu(JID.blackWater, "SELF", [C.has(MK.bw)]),
  // Slams marked last turn land (after the bite: the faster slam, which also marks the next rows).
  ...(["A", "B", "C"] as const).map((k) => R.jutsu(JID.slamBit[k], "SELF", [C.has(MK[k]), C.has(MK.bite)])),
  ...(["A", "B", "C"] as const).map((k) => R.jutsu(JID.slam[k], "SELF", [C.has(MK[k])])),
  // Half health, once.
  R.jutsu(JID.bite, "SELF", [C.hb(50)]),
  // Black Water marks (each once); nothing else is marked that turn.
  R.jutsu(JID.bwMark[2]!, "SELF", [C.hb(P.bw3At)]),
  R.jutsu(JID.bwMark[1]!, "SELF", [C.hb(50)]),
  R.jutsu(JID.bwMark[0]!, "SELF", [C.hb(75)]),
  R.end([C.has(MK.bw)]),
  // Beside a mark or a bitten slam: a cut arm regrows, or the undertow.
  R.jutsu(JID.arm, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [C.noSummon()]),
  R.jutsu(JID.undertow, "SELF", [toPlayer("distance_higher_than", P.undertowFrom)]),
  // A bitten slam already marked the next rows.
  R.end([C.has(MK.chain)]),
  // Slam marks, in turn: after A lands B, after B lands C, else A.
  R.jutsu(JID.mark.B, "SELF", [C.has(MK.tokA)]),
  R.jutsu(JID.mark.C, "SELF", [C.has(MK.tokB)]),
  R.jutsu(JID.mark.A, "SELF", []),
  // Law 41 tail (includeDefaultRules false): an explicit unconditional end. Reached only when Mark A cannot be paid for.
  R.end([]),
];
export const armRules = () => [R.jutsu(JID.lash, "SELF", []), R.end([])];

/* ------------------------------------------------------------------ AI records and rows */
export const isoKit = () => [JID.bodyWater, ...Object.values(JID.mark), ...Object.values(JID.slam), ...Object.values(JID.slamBit), ...JID.bwMark, JID.blackWater, JID.bite, JID.arm, JID.undertow];
export const STUN_PREVENT = {
  type: "stunprevent", power: 100, rounds: 99, target: "INHERIT", appearSfx: "", direction: "offence", calculation: "percentage",
  description: "Prevents being stunned", disappearSfx: "", powerPerLevel: 0, appearAnimation: "", staticAnimation: "",
  staticAssetPath: "", disappearAnimation: "",
};
export const isoAiRecord = (P: IsoParams) => ({
  ...IN.boss.data, username: "Isonade", poolsMultiplier: P.poolsMultiplier, statsMultiplier: P.statsMultiplier,
  ...Object.fromEntries(STATS.map((s) => [s, Math.round(STAT_PER_MULT * P.statsMultiplier * 100) / 100])),
  jutsus: isoKit(), effects: [...idgRowTags(P.idgRows), ...(P.stunPrevent ? [STUN_PREVENT] : [])], includeDefaultRules: false, rules: isoRules(P), avatarFacing: "left",
});
export const armAiRecord = () => ({
  ...IN.echo.data, username: "Grasping Arm", isSummon: true, jutsus: [JID.lash], effects: [], items: [], includeDefaultRules: false, rules: armRules(),
});
export const isoValidate = (P: IsoParams) => {
  const v = validator();
  for (const j of Object.values(buildRecords(P))) v.jutsu(j);
  for (const r of [...isoRules(P), ...armRules()]) v.rule(r);
  const rec = isoAiRecord(P);
  v.ai(BOSS_ID, { ...rec, items: IN.boss.data.items });
  v.ai(ARM_ID, armAiRecord());
  if (rec.rules.length > AI_PROFILE_MAX_RULES) v.issues.push(`Isonade has ${rec.rules.length} rules (cap ${AI_PROFILE_MAX_RULES})`);
  return v.issues;
};
export const fightRows = (P: IsoParams) => {
  const recs: Record<string, any> = { ...allCapturedRecords(), ...buildRecords(P) };
  const rec = isoAiRecord(P);
  const boss = aiRow(BOSS_ID, rec, rec.offence, recs, rec.rules, rec.effects, IN.boss.data.items.flatMap((it: any) => it.ids));
  const a = armAiRecord();
  const arm = aiRow(ARM_ID, a, IN.echo.liveStats.offence, recs, a.rules, [], []);
  return { recs, rows: { [BOSS_ID]: boss, [ARM_ID]: arm } };
};

/* ------------------------------------------------------------------ the fight */
const SETS: Record<string, [string, "mark" | "land"]> = {
  ...Object.fromEntries(Object.values(JID.mark).map((id) => [id, ["Slam", "mark"]])),
  ...Object.fromEntries([...Object.values(JID.slam), ...Object.values(JID.slamBit)].map((id) => [id, ["Slam", "land"]])),
  ...Object.fromEntries(JID.bwMark.map((id) => [id, ["Black Water", "mark"]])),
  [JID.blackWater]: ["Black Water", "land"],
};
type Fight = {
  seed: number; read: number; outcome: string; rounds: number; playerHpPct: number; bossHpPct: number;
  sets: Record<string, { mark: number; land: number; hit: number; dmg: number }>;
  untelegraphedLands: number; dmgBySource: Record<string, number>; poolActions: number; poolDmg: number; maxPoolRows: number; maxPoolHexes: number;
  armCasts: number[]; armDeaths: number[]; regrowGaps: number[]; bodyWaterLastRound: number | null; bodyWaterHexesEnd: number;
  feedWindows: number; feedDmg: number; feedPlayerHits: number; bite: number | null; undertow: number; undertowRounds: number[];
  bwRounds: number[]; phaseRounds: Record<string, number | null>; bossIdleTurns: number; bossTurns: number; dodges: number; misreads: number;
  petBossDmg: number; bossDmgTotal: number; minHpPct: number; ruleCount: number; trace?: string[];
  markLog: { r: number; sp: string }[]; landLog: { r: number; sp: string }[]; lapsed: number; overlaps: number;
};

export const runFight = async (P: IsoParams, seed: number, readP: number, start: { hpFrac?: number } = {}, trace = false): Promise<Fight> => {
  const rand = mulberry32(seed);
  const orig = Math.random;
  Math.random = rand;
  seedEntropy(seed);
  try {
    const { recs, rows } = fightRows(P);
    const kit = PLAYER_VARIANTS.average!.jutsuIds;
    const v = { ...PLAYER_VARIANTS.average!, rules: playerRules(kit, t0.jutsu) };
    const player = playerQueryUser(0, v as never, t0.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, t0.jutsu);
    const pets = [petFor(player)];
    (player as any).activePetId = pets[0]!.id;
    let b = await assembleFloor({ players: [player], enemyRows: rows, floor: { kind: "boss", waves: [{ aiIds: [BOSS_ID], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest", pets });
    for (const [id, r] of Object.entries(recs)) if (!(b.extraState.jutsus as any)[id]) (b.extraState.jutsus as any)[id] = r;
    const grid = getBattleGrid(1, b);
    const puid = player.userId;
    const pu = () => b.usersState.find((u) => u.userId === puid)!;
    const maxHp = getEffectiveMaxPool(pu() as never, b.usersEffects as never, "Health");
    if (start.hpFrac !== undefined) pu().curHealth = Math.max(1, Math.round(maxHp * start.hpFrac));
    if (opt("farStart")) { const [x, y] = String(opt("farStart")).split(",").map(Number); pu().longitude = x!; pu().latitude = y!; }
    const bossU = () => b.usersState.find((u) => u.controllerId === BOSS_ID && !u.isSummon)!;
    const bossUid = bossU().userId;
    const bossPos0: Cell = [bossU().longitude, bossU().latitude];
    const f: Fight = {
      seed, read: readP, outcome: "stalled", rounds: 0, playerHpPct: 0, bossHpPct: 0, sets: { Slam: { mark: 0, land: 0, hit: 0, dmg: 0 }, "Black Water": { mark: 0, land: 0, hit: 0, dmg: 0 } },
      untelegraphedLands: 0, dmgBySource: {}, poolActions: 0, poolDmg: 0, maxPoolRows: 0, maxPoolHexes: 0, armCasts: [], armDeaths: [], regrowGaps: [], bodyWaterLastRound: null, bodyWaterHexesEnd: 0,
      feedWindows: 0, feedDmg: 0, feedPlayerHits: 0, bite: null, undertow: 0, undertowRounds: [], bwRounds: [], phaseRounds: { "75": null, "50": null, "25": null }, bossIdleTurns: 0, bossTurns: 0,
      dodges: 0, misreads: 0, petBossDmg: 0, bossDmgTotal: 0, minHpPct: 100, ruleCount: isoRules(P).length, markLog: [], landLog: [], lapsed: 0, overlaps: 0, ...(trace ? { trace: [] } : {}),
    };
    const actionRounds: number[] = [];
    const turnActs = new Map<string, string[]>();
    const lastMark: Record<string, number> = {};
    const enemyIds = () => new Set(b.usersState.filter((u) => u.direction !== pu().direction).map((u) => u.userId));
    const groundOf = (pred: (g: any) => boolean) => new Set((b.groundEffects as any[]).filter((g) => enemyIds().has(g.creatorId) && pred(g) && ((g.rounds ?? 1) > 0 || g.castThisRound)).map((g) => `${g.longitude},${g.latitude}`));
    const danger = () => {
      const red = groundOf((g) => g.type === "visual" && g.staticAnimation === ANIM.red);
      const safe = groundOf((g) => g.type === "visual" && g.staticAnimation === ANIM.safe);
      if (safe.size) for (const c of ALL) if (!safe.has(key(c))) red.add(key(c));
      return { red, pools: groundOf((g) => g.type === "drain" || (g.type === "damage" && (g.rounds ?? 0) > 0)) };
    };
    const free = (c: Cell) => !b.usersState.some((u) => u.longitude === c[0] && u.latitude === c[1] && stillInBattle(u, b.usersEffects)) && !(b.groundEffects as any[]).some((g) => g.type === "barrier" && g.longitude === c[0] && g.latitude === c[1]);
    const tryAction = (actionId: string, c: Cell) => {
      const action = availableUserActions(b, puid, true, true).find((a) => a.id === actionId);
      if (!action || !actionPointsAfterAction(pu(), b, action).canAct) return false;
      try { b = performBattleAction({ battle: structuredClone(b), action, grid, contextUserId: puid, actorId: puid, longitude: c[0], latitude: c[1] }).newBattle; return true; } catch { return false; }
    };
    const readRand = mulberry32((seed ^ 0x2ead1) >>> 0);
    let lastSig = "";
    let reading = readP >= 1;
    const reads = (red: Set<string>) => {
      if (!red.size) return readP > 0;
      const sig = [...red].sort().join(";");
      if (sig !== lastSig) { lastSig = sig; reading = readP >= 1 ? true : readP <= 0 ? false : readRand() < readP; if (!reading) f.misreads++; }
      return reading;
    };
    /** A good player steps off red, and out of brine pools (each action begun on one drains). Never walks through a pool. */
    const dodgeStep = () => {
      const here: Cell = [pu().longitude, pu().latitude];
      const { red, pools } = danger();
      const readsNow = reads(red);
      const bp0: Cell = [bossU().longitude, bossU().latitude];
      const strict = P.playerPoolPolicy === "strict";
      const inRed = readsNow && red.has(key(here));
      if (!inRed && !pools.has(key(here))) return false;
      if (!inRed && !strict) {
        // In a pool only: step to a clean neighbour no farther from Isonade, else stay and fight.
        const step = ALL.filter((c) => dist(c, here) === 1 && free(c) && !pools.has(key(c)) && !red.has(key(c)) && dist(c, bp0) <= dist(here, bp0))
          .sort((a, c) => dist(a, bp0) - dist(c, bp0))[0];
        if (step) return tryAction("move", step);
        if (P.playerPoolPolicy !== "good") return false;
        // A good player walks up to two hexes to a clean one that still keeps Isonade within 2.
        const reach = Math.max(2, dist(here, bp0));
        for (const n of ALL.filter((c) => dist(c, here) === 1 && free(c) && !red.has(key(c)))) {
          if (ALL.some((c) => dist(c, n) === 1 && free(c) && !pools.has(key(c)) && !red.has(key(c)) && dist(c, bp0) <= reach)) return tryAction("move", n);
        }
        return false;
      }
      const bad = (k: string) => (readsNow && red.has(k)) || (strict && pools.has(k));
      if (!availableUserActions(b, puid, true, true).some((a) => a.id === "move")) return false;
      const prev = new Map<string, string | null>([[key(here), null]]);
      const depth = new Map<string, number>([[key(here), 0]]);
      const q: Cell[] = [here];
      const found: { c: Cell; d: number }[] = [];
      while (q.length) {
        const c = q.shift()!;
        const d = depth.get(key(c))!;
        if (d > 0 && !bad(key(c))) found.push({ c, d });
        if (d >= 10) continue;
        for (const n of ALL) if (!prev.has(key(n)) && dist(c, n) === 1 && free(n) && !(strict && pools.has(key(n)) && d > 0)) { prev.set(key(n), key(c)); depth.set(key(n), d + 1); q.push(n); }
      }
      // Replacement Technique reaches any clean free hex within 5.
      const jump = ALL.filter((c) => free(c) && !bad(key(c)) && dist(c, here) <= 5);
      const bp: Cell = [bossU().longitude, bossU().latitude];
      found.sort((a, c) => a.d - c.d || (pools.has(key(a.c)) ? 1 : 0) - (pools.has(key(c.c)) ? 1 : 0) || dist(a.c, bp) - dist(c.c, bp));
      const target = found[0];
      if ((!target || target.d >= 2) && jump.length) {
        jump.sort((a, c) => dist(a, here) - dist(c, here) || dist(a, bp) - dist(c, bp));
        if (tryAction("replacementTechnique", jump[0]!)) return true;
      }
      if (!target) return false;
      let step = key(target.c);
      while (prev.get(step) !== key(here)) step = prev.get(step)!;
      return tryAction("move", step.split(",").map(Number) as Cell);
    };
    const patCells = (rec: any, from: Cell) => {
      const a = grid.getHex({ col: from[0], row: from[1] });
      return new Set(getTargetTiles({ a, b: a, action: rec, grid } as never).map((h: any) => `${h.col},${h.row}`));
    };
    let armUid: string | null = null;
    const maxRounds = 50;
    for (let step = 0; step < maxRounds * 40; step++) {
      const pre = alignBattle(b, actionRounds, puid);
      if (pre.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
      if (b.round > maxRounds) break;
      const actor = pre.actor;
      const human = actor.userId === puid;
      tickClock(1000);
      const tk = `${b.round}:${actor.userId}`;
      if (!turnActs.has(tk)) {
        turnActs.set(tk, []);
        if (actor.userId === bossUid) {
          // Player effects on Isonade, re-applied each of its turns (not cast this round, so they count now).
          const inj = (type: string, over: Record<string, unknown>) => (b.usersEffects as any[]).push({
            ...tag(type, { rounds: 1, power: 100, ...over }), id: `inj-${type}-${b.round}`, targetId: bossUid, creatorId: puid,
            castThisRound: false, isNew: false, createdRound: b.round, longitude: bossU().longitude, latitude: bossU().latitude,
          });
          const stunAp = Number(opt("stun", "0"));
          const stunEvery = Number(opt("stunEvery", "1"));
          if (stunAp > 0 && !P.stunPrevent && b.round % stunEvery === 0) inj("stun", { apReduction: stunAp });
          if (opt("tc")) inj("timecompression", {});
        }
      }
      const hpBefore = new Map(b.usersState.map((u) => [u.userId, u.curHealth]));
      const pPos: Cell = [pu().longitude, pu().latitude];
      const bPos: Cell = [bossU().longitude, bossU().latitude];
      const poolsBefore = danger().pools;
      const weakBefore = b.usersEffects.some((e: any) => e.targetId === bossUid && e.type === "weakness" && !e.castThisRound);
      let actionId: string | undefined;
      if (trace && actor.userId === bossUid && opt("debug")) {
        const av = availableUserActions(b, bossUid, true, true).filter((x: any) => String(x.id).startsWith("iso-")).map((x: any) => String(x.id).slice(4));
        const ju = (bossU() as any).jutsus.filter((j: any) => String(j.jutsuId).startsWith("iso-slam")).map((j: any) => `${String(j.jutsuId).slice(4)}@${j.lastUsedRound}`);
        f.trace!.push(`   DEBUG r${pre.actionRound} avail=${av.join(",")} used=${ju.join(",")}`);
      }
      if (human && dodgeStep()) { actionId = "dodge"; f.dodges++; }
      else {
        const res = performAIaction(b, grid, actor.userId);
        actionId = res.nextActionId;
        if (human && (actionId === "move" || actionId === "replacementTechnique")) {
          const after = res.nextBattle.usersState.find((u) => u.userId === puid)!;
          const k = `${after.longitude},${after.latitude}`;
          const d = danger();
          if ((reading && d.red.has(k)) || (P.playerPoolPolicy === "strict" && d.pools.has(k))) actionId = tryAction("wait", pPos) ? "wait" : (b = res.nextBattle, actionId);
          else b = res.nextBattle;
        } else b = res.nextBattle;
      }
      const post = alignBattle(b, actionRounds, puid);
      if (post.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(post.actionRound)) actionRounds.push(post.actionRound);
      if (!actionId && actor.isAutoCombat) b.roundStartAt = new Date(Date.now() - 61_000);
      turnActs.get(tk)!.push(actionId ?? "none");
      const pLoss = Math.max(0, (hpBefore.get(puid) ?? 0) - pu().curHealth);
      const bl = Math.max(0, (hpBefore.get(bossUid) ?? 0) - bossU().curHealth);
      f.bossDmgTotal += bl;
      if ((actor as any).petId) f.petBossDmg += bl;
      if (weakBefore && bl > 0) { f.feedDmg += bl; if (human) f.feedPlayerHits++; }
      if (human && poolsBefore.has(key(pPos)) && actionId && actionId !== "none") { f.poolActions++; f.poolDmg += pLoss; }
      const isBoss = actor.userId === bossUid;
      if (!human && pLoss > 0) {
        const src = (actor as any).summonSourceId === ARM_ID ? "Grasping Arm" : isBoss ? (SETS[actionId ?? ""]?.[0] ?? (b.extraState.jutsus as any)[actionId ?? ""]?.name ?? actionId ?? "?") : actor.username;
        f.dmgBySource[src] = (f.dmgBySource[src] ?? 0) + pLoss;
      }
      if (human && pLoss > 0 && poolsBefore.has(key(pPos))) f.dmgBySource["Brine pool"] = (f.dmgBySource["Brine pool"] ?? 0) + pLoss;
      if (isBoss && actionId && SETS[actionId]) {
        const [sp, kind] = SETS[actionId]!;
        const s = f.sets[sp]!;
        const slamKey = (id: string) => (Object.entries(JID.mark).find(([, v]) => v === id) ?? Object.entries(JID.slam).find(([, v]) => v === id) ?? Object.entries(JID.slamBit).find(([, v]) => v === id))?.[0];
        if (kind === "mark") { s.mark++; lastMark[sp] = pre.actionRound; if (sp === "Black Water") f.bwRounds.push(pre.actionRound); f.markLog.push({ r: pre.actionRound, sp: sp === "Slam" ? `Slam ${slamKey(actionId)}` : sp }); }
        else {
          f.landLog.push({ r: pre.actionRound, sp: sp === "Slam" ? `Slam ${slamKey(actionId)}` : sp });
          s.land++;
          if (patCells(recs[actionId!], bPos).has(key(pPos))) { s.hit++; s.dmg += pLoss; }
          if (pre.actionRound - (lastMark[sp] ?? -9) > 1) f.untelegraphedLands++;
          if (sp === "Black Water") f.feedWindows++;
        }
        // A bitten slam also lays the next mark.
        if (Object.values(JID.slamBit).includes(actionId as never) && !(P.bittenChainEnds && actionId === JID.slamBit.C)) {
          s.mark++; lastMark[sp] = pre.actionRound;
          const k = Object.entries(JID.slamBit).find(([, v]) => v === actionId)![0];
          f.markLog.push({ r: pre.actionRound, sp: `Slam ${({ A: "B", B: "C", C: "A" } as any)[k]}` });
        }
      }
      if (isBoss && actionId === JID.bite) f.bite = pre.actionRound;
      if (isBoss && actionId === JID.undertow) { f.undertow++; f.undertowRounds.push(pre.actionRound); }
      if (isBoss && actionId === JID.arm) f.armCasts.push(pre.actionRound);
      // the arm: track its unit and when it is cut
      const armU = b.usersState.find((u: any) => u.isSummon && u.summonSourceId === ARM_ID && !u.isSummonTemplate && stillInBattle(u, b.usersEffects));
      if (armU && armU.userId !== armUid) armUid = armU.userId;
      if (!armU && armUid) { f.armDeaths.push(pre.actionRound); armUid = null; }
      // pools on the floor (by row)
      const poolNow = danger().pools;
      f.maxPoolHexes = Math.max(f.maxPoolHexes, poolNow.size);
      f.maxPoolRows = Math.max(f.maxPoolRows, new Set([...poolNow].map((k) => k.split(",")[1])).size);
      const bw = (b.groundEffects as any[]).filter((g) => g.type === "visual" && g.staticAnimation === ANIM.bodyWater);
      if (bw.length) f.bodyWaterLastRound = pre.actionRound;
      f.bodyWaterHexesEnd = new Set(bw.map((g) => `${g.longitude},${g.latitude}`)).size;
      (f as any).bodyWaterEffectsEnd = bw.length;
      const bu = bossU();
      const bhp = (100 * bu.curHealth) / bu.maxHealth;
      for (const t of ["75", "50", "25"]) if (bhp < Number(t) && f.phaseRounds[t] === null) f.phaseRounds[t] = pre.actionRound;
      f.minHpPct = Math.min(f.minHpPct, (100 * Math.max(0, pu().curHealth)) / maxHp);
      if (trace) {
        const nm = actionId === "dodge" ? "DODGE" : actionId?.startsWith("iso-") ? actionId.slice(4) : (b.extraState.jutsus as any)[actionId ?? ""]?.name ?? actionId;
        const who = human ? "player" : isBoss ? "Isonade" : (actor as any).petId ? "pet" : (actor as any).summonSourceId === ARM_ID ? "arm" : actor.username;
        f.trace!.push(`r${pre.actionRound} ${who.padEnd(7)} ${String(nm).padEnd(22)} p@${pPos} pHP ${Math.round(pu().curHealth)} (-${Math.round(pLoss)}) boss ${bhp.toFixed(1)}% @${bPos} pools ${poolNow.size}${armU ? ` arm@${armU.longitude},${armU.latitude}` : ""}${isBoss ? ` fx[${(b.usersEffects as any[]).filter((e) => e.targetId === bossUid && Object.values(MK).includes(e.type)).map((e) => `${e.type}:${e.rounds}${e.castThisRound ? "*" : ""}`).join(",")}]` : ""}`);
      }
      const side = (dir: string) => b.usersState.some((u) => u.direction === dir && !u.isSummon && stillInBattle(u, b.usersEffects));
      if (!side(pu().direction)) { f.outcome = "lost"; break; }
      if (!b.usersState.some((u) => u.controllerId === BOSS_ID && !u.isSummon && stillInBattle(u, b.usersEffects))) { f.outcome = "won"; break; }
    }
    for (const [k, acts] of turnActs) if (k.split(":")[1] === bossUid) { f.bossTurns++; if (acts.every((a) => a === "wait" || a === "none")) f.bossIdleTurns++; }
    // A warning lapses when its land does not follow next round (and the fight goes on); two warnings laid in one turn overlap.
    const endRound = f.landLog.length || f.markLog.length ? b.round : 0;
    for (const m of f.markLog) if (m.r + 1 < endRound && !f.landLog.some((l) => l.sp === m.sp && l.r === m.r + 1)) f.lapsed++;
    const byRound = new Map<number, number>();
    for (const m of f.markLog) byRound.set(m.r, (byRound.get(m.r) ?? 0) + 1);
    f.overlaps = [...byRound.values()].filter((n) => n > 1).length;
    for (const d of f.armDeaths) { const next = f.armCasts.find((c) => c > d); if (next !== undefined) f.regrowGaps.push(next - d); }
    const bu = bossU();
    f.rounds = b.round;
    f.playerHpPct = r1((100 * Math.max(0, pu().curHealth)) / maxHp)!;
    f.bossHpPct = r1((100 * Math.max(0, bu.curHealth)) / bu.maxHealth)!;
    f.minHpPct = r1(f.minHpPct)!;
    (f as any).bossMoved = bu.longitude !== bossPos0[0] || bu.latitude !== bossPos0[1];
    return f;
  } finally {
    Math.random = orig;
  }
};

const summarise = (fs: Fight[]) => {
  const wins = fs.filter((f) => f.outcome === "won");
  const src: Record<string, number> = {};
  for (const f of fs) for (const [k, v] of Object.entries(f.dmgBySource)) src[k] = (src[k] ?? 0) + v;
  const tot = Object.values(src).reduce((a, b) => a + b, 0) || 1;
  const per = (sp: string, fld: "mark" | "land" | "hit") => r1(fs.reduce((s, f) => s + f.sets[sp]![fld], 0) / fs.length);
  return {
    fights: fs.length, wins: wins.length, winPct: r1((100 * wins.length) / fs.length),
    roundsWinMedian: median(wins.map((f) => f.rounds)), roundsWinP10: quantile(wins.map((f) => f.rounds), 0.1), roundsWinP90: quantile(wins.map((f) => f.rounds), 0.9),
    hpLeftWinMedian: r1(median(wins.map((f) => f.playerHpPct))), minHpMedian: r1(median(fs.map((f) => f.minHpPct))),
    bossHpLeftLossMedian: r1(median(fs.filter((f) => f.outcome !== "won").map((f) => f.bossHpPct))),
    slam: { marks: per("Slam", "mark"), lands: per("Slam", "land"), hits: per("Slam", "hit") },
    blackWater: { marks: per("Black Water", "mark"), lands: per("Black Water", "land"), hits: per("Black Water", "hit"), roundsMedian: [0, 1, 2].map((i) => median(fs.flatMap((f) => (f.bwRounds[i] === undefined ? [] : [f.bwRounds[i]!])))) },
    untelegraphedLands: fs.reduce((s, f) => s + f.untelegraphedLands, 0),
    lapsedWarnings: fs.reduce((s, f) => s + f.lapsed, 0), overlappedWarnings: fs.reduce((s, f) => s + f.overlaps, 0),
    fightsWith3FeedWindowsPct: r1((100 * fs.filter((f) => f.feedWindows >= 3).length) / fs.length),
    feedWindowsInWinsMin: wins.length ? Math.min(...wins.map((f) => f.feedWindows)) : null,
    feed: { windowsPerFight: r1(fs.reduce((s, f) => s + f.feedWindows, 0) / fs.length), bossDmgSharePct: r1((100 * fs.reduce((s, f) => s + f.feedDmg, 0)) / Math.max(1, fs.reduce((s, f) => s + f.bossDmgTotal, 0))) },
    pools: { maxRowsEver: Math.max(...fs.map((f) => f.maxPoolRows)), maxHexesEver: Math.max(...fs.map((f) => f.maxPoolHexes)), actionsInPoolPerFight: r1(fs.reduce((s, f) => s + f.poolActions, 0) / fs.length) },
    arm: { castsPerFight: r1(fs.reduce((s, f) => s + f.armCasts.length, 0) / fs.length), cutPerFight: r1(fs.reduce((s, f) => s + f.armDeaths.length, 0) / fs.length), regrowGapMedian: median(fs.flatMap((f) => f.regrowGaps)), regrowGapMin: fs.some((f) => f.regrowGaps.length) ? Math.min(...fs.flatMap((f) => f.regrowGaps)) : null },
    undertowPerFight: r1(fs.reduce((s, f) => s + f.undertow, 0) / fs.length),
    biteRoundMedian: median(fs.flatMap((f) => (f.bite === null ? [] : [f.bite]))),
    bodyWater: { lastsWholeFightPct: r1((100 * fs.filter((f) => f.bodyWaterLastRound !== null && f.bodyWaterHexesEnd > 0).length) / fs.length), hexesAtEndMedian: median(fs.map((f) => f.bodyWaterHexesEnd)), groundEffectsAtEndMedian: median(fs.map((f: any) => f.bodyWaterEffectsEnd)) },
    phaseRoundMedian: Object.fromEntries(["75", "50", "25"].map((t) => [t, median(fs.flatMap((f) => (f.phaseRounds[t] === null ? [] : [f.phaseRounds[t]!])))])),
    bossMovedPct: r1((100 * fs.filter((f: any) => f.bossMoved).length) / fs.length),
    bossIdleTurnPct: r1((100 * fs.reduce((s, f) => s + f.bossIdleTurns, 0)) / Math.max(1, fs.reduce((s, f) => s + f.bossTurns, 0))),
    petBossDmgSharePct: r1((100 * fs.reduce((s, f) => s + f.petBossDmg, 0)) / Math.max(1, fs.reduce((s, f) => s + f.bossDmgTotal, 0))),
    misreadsPerFight: r1(fs.reduce((s, f) => s + f.misreads, 0) / fs.length),
    damageShareToPlayerPct: Object.fromEntries(Object.entries(src).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, r1((100 * v) / tot)])),
  };
};

export const isoSpec = (P: IsoParams, issues: string[]) => ({
  _note: "Isonade build spec (The Flooded Stores, The Stores Below; design approved Nov 18). Generated by isonade.ts --write-spec; offline engine-tested, NOT pushed. Ids are placeholders (iso-*) to replace with created ids (law 17). Animations anim_isonade_*_v1 are the new strips in tnr/art/isonade_anims (not uploaded; their game image names replace these); tg_heavy / tg_safe are the shared marks; anim_fx_undertow_v1 is the processed undertow streak.",
  params: P,
  ais: { [BOSS_ID]: isoAiRecord(P), [ARM_ID]: armAiRecord() },
  newJutsu: buildRecords(P),
  markerTypes: MK, animations: ANIM, patterns: patterns(P),
  validation: issues.length ? issues : "valid: JutsuValidator (every jutsu), AiRule (every rule), insertAiSchema (both AIs), rule cap",
});

/* ------------------------------------------------------------------ main */
const main = async () => {
  const P = isoParams(opt("params") ? loadJson(resolve(opt("params")!)) : {});
  const issues = isoValidate(P);
  console.log(issues.length ? `VALIDATION ISSUES:\n  ${issues.join("\n  ")}` : `valid (Isonade ${isoRules(P).length} rules, arm ${armRules().length})`);
  const specPath = opt("write-spec");
  if (specPath) {
    const spec = isoSpec(P, issues);
    assertSpecRuleCap("isonade_spec", { ai: { record: isoAiRecord(P) } });
    mkdirSync(dirname(resolve(specPath)), { recursive: true });
    writeFileSync(resolve(specPath), `${JSON.stringify(spec, null, 1)}\n`);
    console.log(`wrote ${specPath}`);
  }
  const startArg = opt("start", "full");
  const start = startArg === "full" ? {} : { hpFrac: Number(startArg) };
  const traceSeed = opt("trace");
  const readList = opt("read", "1,0.85")!.split(",").map(Number);
  if (traceSeed) {
    const f = await runFight(P, Number(traceSeed), readList[0]!, start, true);
    console.log(`--- trace seed ${traceSeed} read ${readList[0]}: ${f.outcome} in ${f.rounds} rounds, player ${f.playerHpPct}%, boss ${f.bossHpPct}%`);
    for (const l of f.trace!) console.log("  " + l);
  }
  const seeds = Number(opt("seeds", traceSeed ? "0" : "40"));
  const results: any = { generatedBy: "isonade.ts", params: P, dmgConfig: dmg.name, grid: SIZE, seeds, start: startArg, reads: {} };
  if (seeds > 0) for (const rp of readList) {
    const fs: Fight[] = [];
    for (let i = 0; i < seeds; i++) fs.push(await runFight(P, 1 + i, rp, start));
    const s = summarise(fs);
    results.reads[String(rp)] = { summary: s, fights: fs };
    console.log(`\n== ${P.name} read ${rp}: ${JSON.stringify(s)}`);
  }
  const outPath = opt("out");
  if (outPath) { mkdirSync(dirname(resolve(outPath)), { recursive: true }); writeFileSync(resolve(outPath), `${JSON.stringify(results, null, 1)}\n`); console.log(`wrote ${outPath}`); }
};
if (import.meta.main) await main();
