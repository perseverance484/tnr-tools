/**
 * Isonade v4 (The Flooded Stores): a rotation boss that plays like an endgame PvP opponent, plus two different Black
 * Water set pieces. Offline only; zero live requests. Runs inside the Skyglass Wreck harness (fable/mother-of-echoes-act3
 * harness/skyglass_wreck_sim), importing its cclib / kitlib / model / sim modules unchanged.
 *
 *   TNR_SCRIPT=isonade_v4.ts run.sh [--params /abs/p.json] [--seeds 20] [--read 1,0.85,0.7] [--trace SEED] [--dg 120]
 *        [--write-spec /abs/spec.json] [--out /abs/results.json]
 *
 * Design (director, 2026-11-19): fixed four-beat rotation (Barnacle Hide, The Tide Draws Back, Breaker, Harpoon Line),
 * a Black Water slot after the first two rotations (I: the crates; II: The Deep, break its shield or eat the crash),
 * and PvP-style reactions with no warning: it Clears a big DR or damage stack, Cleanses debuffs off itself (60 AP, then
 * the Drowned Anchor with the other 30), and Smokes a damage stack when its Clear is down. It acts after the player
 * every round (player 2), so its reactions land the same round the player casts, before anything goes live.
 *
 * Chain flags: one-round-plus-one self markers of NEGATIVE polarity (the player's Clear can't break the chain; its
 * own Cleanse can, and then it restarts at Barnacle Hide). Markers last 2 rounds so a reaction turn delays the
 * rotation a round instead of breaking it; each beat has cooldown 2 so a stale marker can't repeat its beat.
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { performAIaction } from "@/libs/combat/ai_v2";
import { availableUserActions, actionPointsAfterAction, performBattleAction, stillInBattle } from "@/libs/combat/actions";
import { applySageModeAfterRoundTransition } from "@/libs/combat/process";
import { alignBattle, getBattleGrid, getEffectiveMaxPool } from "@/libs/combat/util";
import { jutsu, T, tag } from "./kitlib";
import {
  aiRow, ALL, C, type Cell, DONOR_SUMMON, dist, dmg, IN, IMG, jutsuRecord, key, median, opt, quantile, R, r1, SIZE, STAT_PER_MULT, STATS,
  t0, validator, allCapturedRecords,
} from "./cclib";
import { loadJson, petFor, PLAYER_VARIANTS, playerQueryUser, playerRules } from "./model";
import { assembleFloor, mulberry32, seedEntropy, tickClock } from "./sim";
import { AI_PROFILE_MAX_RULES } from "./rulecap";

const W = SIZE.width;
const H = SIZE.height;
const cellsWhere = (pred: (c: number, r: number) => boolean): Cell[] => {
  const out: Cell[] = [];
  for (let c = 0; c < W; c++) for (let r = 0; r < H; r++) if (pred(c, r)) out.push([c, r]);
  return out;
};
const field = (cells: Cell[], selection: "ALL" | "EXCLUDE" = "ALL") => ({ origin: "BATTLEFIELD", selection, coordinates: cells.map((c) => ({ longitude: c[0], latitude: c[1] })), randomCount: 1 });

export const V4_DEFAULTS = {
  name: "isonade_v4",
  poolsMultiplier: 6,
  statsMultiplier: 5.83,
  // rotation
  hideShield: 2500, // Barnacle Hide: instant self shield
  hideRounds: 2,
  hideDr: 0, // Barnacle Hide: % damage taken reduction on itself, 2 rounds (a buff: the player's Clear removes it)
  tideDr: 0, // The Tide Draws Back: % DR on itself, 2 rounds (Clearable)
  shedDr: 0, // Shed: % DR on itself, 2 rounds (Clearable)
  swellDr: 0, // The Swell Builds: another DR layer, 1 round (covers the Breaker round)
  tideBuff: 50, // each layer of the burst window: +% damage given on itself (Tide: 2 rounds, Swell: 1 round)
  brand: 30, // each Brine Brand layer on the player: +% damage taken. In-battle % modifiers multiply (damagePipeline), so 2+2 layers compound
  breakerPower: 400,
  breakerWound: 6, // % max HP per round, 2 rounds
  breakerWindow: 1.5, // self weakness the round after Breaker (damage taken multiplier)
  harpoonPower: 24, // pierce
  // Black Water I (the crates) and II (The Deep)
  bw1At: 75, // Black Water I when health first drops below this %
  bw2At: 40, // The Deep when health first drops below this %
  bw1Power: 220,
  bw1Feed: 1.5,
  bw2Shield: 6000,
  bw2Power: 260,
  bw2Feed: 2,
  crates: [[6, 1], [4, 5], [6, 9]] as Cell[],
  // reactions (no warning)
  clearAbsorb: 60, // player's absorb total that draws a Clear (gear absorb counts; DR is invisible to conditions, see below)
  clearShield: 100, // player's shield HP that draws a Clear
  clearIdg: 80, // player's increasedamagegiven total that draws a Clear
  cleanseWound: 5, // Isonade's own wound total that draws a Cleanse
  cleanseIdt: 40, // Isonade's own increasedamagetaken total that draws a Cleanse
  smokeIdg: 60, // player's increasedamagegiven total that draws Smoke (when Clear is down)
  reactCd: 10,
  anchorPower: 110,
  anchorWound: 4,
  // extras
  bitePct: 30, // below 50%, once: +% damage given for the rest of the fight (Clearable)
  armHp: 4000, armPower: 60, armRounds: 30, armCooldown: 5, lashPower: 70,
  churnAp: 10, beatAp: 60, reactAp: 60, sideAp: 30,
  deepAp: 70, // The Deep's sink leaves 20 AP, so no Silt Cloud (30) rides along: the break round is never smoked
  // the player
  playerDg: 120, // gear stand-in damage given %: reproduces dauntless's live 12-round v3 kill (iso_cal.ts)
};
export type V4 = typeof V4_DEFAULTS;
const v4 = (over: any = {}): V4 => ({ ...V4_DEFAULTS, ...over });

export const BOSS_ID = "iso-isonade";
export const ARM_ID = "iso-grasping-arm";
export const J4 = {
  churn: "iso-it-rises", hide: "iso-barnacle-hide", tide: "iso-tide-draws-back", breaker: "iso-breaker", harpoon: "iso-harpoon-line",
  bw1Mark: "iso-black-water-mark", bw1Land: "iso-black-water", bw2Mark: "iso-the-deep", bw2Crash: "iso-the-deep-crash", bw2Surface: "iso-the-deep-surface",
  swell: "iso-the-swell", clear: "iso-scour", cleanse: "iso-shed", smoke: "iso-silt-cloud", anchor: "iso-drowned-anchor", bite: "iso-bite-of-the-ship",
  arm: "iso-grasping-arm-rises", lash: "iso-arm-lash",
};
/** Chain markers. Negative polarity (a player's Clear leaves them), no gameplay on this boss: it has no cooldown
 * actions listed, never flees, has no elements, heals or bloodline. */
export const MK = {
  tide: "fleeprevent", breaker: "increasecooldown", harpoon: "elementalseal", swell: "healprevent", bw1: "seal", bw2: "disarm", // decreaseheal is stored negative (tags.ts decreaseHealGiven), so has_effect never sees it
  react: "decreasecooldown", // positive on purpose: its own Cleanse must not strip it mid-turn
};
export const ANIM = { red: "tg_heavy", safe: "tg_safe", bodyWater: "anim_isonade_body_water_v1", hit: "anim_isonade_slam_v1", surge: "anim_isonade_surge_v1", eye: "anim_isonade_eye_v1", bite: "anim_isonade_bite_v1", armBurst: "anim_isonade_arm_burst_v1", armLash: "anim_isonade_arm_lash_v1" };
const marker = (type: string, rounds = 2) => tag(type, {
  power: ["increasecooldown", "decreasecooldown"].includes(type) ? 1 : 100, rounds, target: "SELF",
  ...(["increasecooldown", "decreasecooldown"].includes(type) ? { actionsAffected: [], calculation: "static" } : {}),
  description: "Isonade's rotation",
});
const ALL_STATS = ["None", "Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"];
const ALL_GENERALS = ["Highest", "Strength", "Intelligence", "Willpower", "Speed"];
const statsAll = { statTypes: ALL_STATS, generalTypes: ALL_GENERALS };
const room = cellsWhere(() => true);
const hit = (power: number, o: Record<string, unknown> = {}) => T.damage(power, { appearAnimation: ANIM.hit, ...statsAll, ...o });

export const buildRecords = (P: V4) => {
  const J: Record<string, any> = {};
  const add = (j: any) => (J[j.id] = j);
  const onPlayer = { target: "CHARACTER", method: "COORDINATES", range: 0, coordinateTargeting: field(room) };
  const notCrates = cellsWhere((c, r) => !P.crates.some((x) => x[0] === c && x[1] === r));
  add(jutsu(J4.churn, { name: "It Rises", description: "Black water churns around Isonade every turn. Harmless.", battleDescription: "Black water churns around %user.",
    target: "GROUND", method: "AOE_SPIRAL_SHOOT", range: 1, cooldown: 1, actionCostPerc: P.churnAp, effects: [T.visual(ANIM.bodyWater, 1)] }));
  // --- the rotation
  add(jutsu(J4.hide, { name: "Barnacle Hide", description: "Barnacles close over its hide: a shield that soaks your hits.", battleDescription: "Barnacles grind shut over %user's hide.",
    target: "SELF", method: "SINGLE", range: 0, cooldown: 2, actionCostPerc: P.beatAp,
    effects: [tag("shield", { power: 100, health: P.hideShield, rounds: P.hideRounds, target: "SELF", description: "Barnacle Hide" }),
      ...(P.hideDr ? [T.pct("decreasedamagetaken", P.hideDr, 2, { target: "SELF", ...statsAll, description: "Barnacle Hide" })] : []), marker(MK.tide)] }));
  add(jutsu(J4.tide, { name: "The Tide Draws Back", description: "The water pulls away from the shore: it gathers itself and brands you. Its next hit is a big one.",
    battleDescription: "The water pulls away from the shore. Brine burns into %target.", ...onPlayer, cooldown: 2, actionCostPerc: P.beatAp,
    effects: [
      T.pct("increasedamagegiven", P.tideBuff, 2, { target: "SELF", ...statsAll, description: "The tide gathers" }),
      T.pct("increasedamagetaken", P.brand, 2, { friendlyFire: "ENEMIES", ...statsAll, description: "Brine Brand" }),
      ...(P.tideDr ? [T.pct("decreasedamagetaken", P.tideDr, 2, { target: "SELF", ...statsAll, description: "The tide gathers" })] : []),
      marker(MK.swell),
    ] }));
  add(jutsu(J4.swell, { name: "The Swell Builds", description: "The water stacks higher and the brand bites deeper. Its next hit is the big one.",
    battleDescription: "The sea rears up behind %user. The brand on %target burns deeper.", ...onPlayer, cooldown: 2, actionCostPerc: P.beatAp,
    effects: [
      T.pct("increasedamagegiven", P.tideBuff, 1, { target: "SELF", ...statsAll, description: "The swell builds" }),
      T.pct("increasedamagetaken", P.brand, 1, { friendlyFire: "ENEMIES", ...statsAll, description: "Brine Brand" }),
      ...(P.swellDr ? [T.pct("decreasedamagetaken", P.swellDr, 1, { target: "SELF", ...statsAll, description: "The swell builds" })] : []),
      marker(MK.breaker),
    ] }));
  add(jutsu(J4.breaker, { name: "Breaker", description: "The wave breaks over you. Then it hangs exposed for a round.", battleDescription: "The wave breaks over %target.", ...onPlayer,
    cooldown: 2, actionCostPerc: P.beatAp,
    effects: [hit(P.breakerPower, { appearAnimation: ANIM.surge }), T.pct("wound", P.breakerWound, 2, { friendlyFire: "ENEMIES", description: "Breaker wound" }),
      tag("weakness", { target: "SELF", rounds: 1, dmgModifier: P.breakerWindow, ...statsAll, power: 100, staticAnimation: ANIM.eye, description: "Spent: takes extra damage" }), marker(MK.harpoon)] }));
  add(jutsu(J4.harpoon, { name: "Harpoon Line", description: "It spits the old harpoon back through you. Goes through damage reduction and shields.", battleDescription: "%user spits a rusted harpoon through %target.",
    ...onPlayer, cooldown: 2, actionCostPerc: P.beatAp, effects: [T.pierce(P.harpoonPower, { ...statsAll })] }));
  // --- Black Water I: the crates
  add(jutsu(J4.bw1Mark, { name: "Black Water", description: "Everything but the floating crates is marked red. Black water fills the room next turn.", battleDescription: "The water goes still and black. Only the floating crates stay pale.",
    target: "GROUND", method: "COORDINATES", range: 0, cooldown: 99, actionCostPerc: P.beatAp, coordinateTargeting: field(P.crates, "EXCLUDE"),
    effects: [T.visual(ANIM.red, 1), T.visual(ANIM.safe, 1, { target: "COORDINATES", coordinateTargeting: field(P.crates) }), marker(MK.bw1)] }));
  add(jutsu(J4.bw1Land, { name: "Black Water", description: "Black water fills every hex but the crates; then it surfaces to feed.", battleDescription: "Black water crashes down. %user surfaces to feed.",
    target: "CHARACTER", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: P.beatAp, coordinateTargeting: field(notCrates),
    effects: [hit(P.bw1Power, { appearAnimation: ANIM.surge }), tag("weakness", { target: "SELF", rounds: 1, dmgModifier: P.bw1Feed, ...statsAll, power: 100, staticAnimation: ANIM.eye, description: "Feeding: takes extra damage" })] }));
  // --- Black Water II: The Deep (break the shield or eat the crash)
  add(jutsu(J4.bw2Mark, { name: "The Deep", description: "It sinks under black water behind a heavy shield. Break the shield before its next turn, or the whole room floods.",
    battleDescription: "%user sinks out of sight. The whole hold goes black.", target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: P.deepAp,
    effects: [tag("shield", { power: 100, health: P.bw2Shield, rounds: 1, target: "SELF", description: "The Deep" }), marker(MK.bw2)] }));
  add(jutsu(J4.bw2Crash, { name: "The Deep", description: "The shield held: the black water crashes over the whole room and washes Isonade clean.", battleDescription: "Black water rises to the ceiling and crashes down on %target.",
    ...onPlayer, cooldown: 2, actionCostPerc: P.beatAp, effects: [hit(P.bw2Power, { appearAnimation: ANIM.surge }), T.cleanseSelf()] })); // the cleanse clears its own Deep marker so it doesn't also surface
  add(jutsu(J4.bw2Surface, { name: "The Deep", description: "Its shield broken, it surfaces gasping and exposed.", battleDescription: "%user surfaces through its broken shell, gasping.",
    target: "SELF", method: "SINGLE", range: 0, cooldown: 2, actionCostPerc: P.beatAp,
    effects: [tag("weakness", { target: "SELF", rounds: 1, dmgModifier: P.bw2Feed, ...statsAll, power: 100, staticAnimation: ANIM.eye, description: "Exposed: takes extra damage" })] }));
  // --- reactions (no tell)
  add(jutsu(J4.clear, { name: "Scour", description: "The undertow tears your buffs away.", battleDescription: "The undertow tears through %target's guard.", ...onPlayer,
    cooldown: P.reactCd, actionCostPerc: P.reactAp, effects: [tag("clear", { power: 100, rounds: 0, friendlyFire: "ENEMIES" }), marker(MK.react, 1)] }));
  add(jutsu(J4.cleanse, { name: "Shed", description: "It sheds its outer skin and every debuff with it.", battleDescription: "%user sheds a skin of rotten barnacles.",
    target: "SELF", method: "SINGLE", range: 0, cooldown: P.reactCd, actionCostPerc: P.reactAp, effects: [T.cleanseSelf(), ...(P.shedDr ? [T.pct("decreasedamagetaken", P.shedDr, 2, { target: "SELF", ...statsAll, description: "Shed" })] : []), marker(MK.react, 1)] }));
  add(jutsu(J4.anchor, { name: "Drowned Anchor", description: "It swings the anchor chain it swallowed. Follows a Scour or a Shed.", battleDescription: "%user swings a drowned anchor into %target.", ...onPlayer,
    cooldown: 2, actionCostPerc: P.sideAp, effects: [hit(P.anchorPower), T.pct("wound", P.anchorWound, 2, { friendlyFire: "ENEMIES", description: "Anchor wound" })] }));
  add(jutsu(J4.smoke, { name: "Silt Cloud", description: "It churns up silt: your damage next round is cut hard, and it takes less.", battleDescription: "%user thrashes. Silt clouds the hold.", ...onPlayer,
    cooldown: P.reactCd, actionCostPerc: P.sideAp, effects: [T.pct("decreasedamagegiven", 50, 1, { friendlyFire: "ENEMIES", ...statsAll, description: "Silt Cloud" }), T.pct("decreasedamagetaken", 25, 2, { target: "SELF", ...statsAll, description: "Silt Cloud" })] }));
  add(jutsuRecord(J4.arm, {
    ...structuredClone(DONOR_SUMMON), id: J4.arm, name: "Grasping Arm", image: IMG, jutsuType: "AI", jutsuRank: "S", hidden: true, injectableInBattle: false, battleUsageType: "BOTH",
    requiredRank: "STUDENT", requiredLevel: 1, bloodlineId: null, villageId: null, chakraCost: 0, staminaCost: 0, healthCost: 0,
    target: "EMPTY_GROUND", method: "SINGLE", range: 5, cooldown: P.armCooldown, actionCostPerc: P.sideAp,
    description: "An arm bursts up through the deck and lashes everything around it. Cut it, and another grows.", battleDescription: "The deck bursts upward. A wet black arm rises out of it.",
    effects: DONOR_SUMMON.effects.filter((e: any) => e.type === "summon").map((e: any) => ({ ...e, aiId: ARM_ID, aiHp: P.armHp, power: P.armPower, powerPerLevel: 0, rounds: P.armRounds, appearAnimation: ANIM.armBurst, appearSfx: "" })),
  }));
  add(jutsu(J4.lash, { name: "Arm Lash", description: "The arm sweeps every hex around it.", battleDescription: "The arm lashes across the planks.", target: "GROUND", method: "AOE_SPIRAL_SHOOT", range: 1, cooldown: 1, actionCostPerc: 100, effects: [T.damage(P.lashPower, { appearAnimation: ANIM.armLash })] }));
  return J;
};

/** Rule order (P2: it acts after the player each round, so target_has_effect sees what the player cast this turn). */
export const isoRules = (P: V4) => [
  R.jutsu(J4.churn, "SELF", []), // 10 AP; also prunes markers two rounds old before anything reads them
  ...((P as any).probe ? [(P as any).probe.self ? R.jutsu(J4.clear, "SELF", [C.has((P as any).probe.type, (P as any).probe.th)]) : R.jutsu(J4.clear, "SELF", [C.tHas((P as any).probe.type, (P as any).probe.th)])] : []),
  // Set pieces can't be interrupted.
  R.jutsu(J4.bw2Crash, "SELF", [C.has(MK.bw2), C.has("shield", 1)]),
  R.jutsu(J4.bw2Surface, "SELF", [C.has(MK.bw2)]),
  R.jutsu(J4.bw1Land, "SELF", [C.has(MK.bw1)]),
  // Reactions: 60 AP, then the Drowned Anchor with the rest. They take this turn's beat; the rotation waits a round.
  // decreasedamagetaken / decreasedamagegiven are stored negative once applied (process.ts), so no condition can see
  // a DR or DDG stack. Absorb, shields and damage-given are positive and visible.
  ...((P as any).probe ? [] : [R.jutsu(J4.clear, "SELF", [C.tHas("absorb", P.clearAbsorb)])]),
  R.jutsu(J4.clear, "SELF", [C.tHas("shield", P.clearShield)]),
  R.jutsu(J4.clear, "SELF", [C.tHas("increasedamagegiven", P.clearIdg)]),
  R.jutsu(J4.anchor, "SELF", [C.has(MK.react)]),
  // The rotation: each beat needs the marker the previous beat laid.
  R.jutsu(J4.harpoon, "SELF", [C.has(MK.harpoon)]),
  R.jutsu(J4.breaker, "SELF", [C.has(MK.breaker)]),
  R.jutsu(J4.swell, "SELF", [C.has(MK.swell)]),
  R.jutsu(J4.tide, "SELF", [C.has(MK.tide)]),
  // Shed sits below the burst: it takes the Hide slot (cleanse + Anchor), so its cleanse never wipes a live chain marker.
  R.jutsu(J4.cleanse, "SELF", [C.has("wound", P.cleanseWound)]),
  R.jutsu(J4.cleanse, "SELF", [C.has("increasedamagetaken", P.cleanseIdt)]),
  // The two Black Water set pieces: each fires once, the first free round (the Hide slot) after its health first drops
  // past the line. Below the beats, so a set piece never eats a Breaker; HP-gated, so a burst player still sees both.
  R.jutsu(J4.bw1Mark, "SELF", [C.hb(P.bw1At)]),
  R.jutsu(J4.bw2Mark, "SELF", [C.hb(P.bw2At)]),
  R.jutsu(J4.hide, "SELF", []),
  // Extras with the last 30 AP.
  R.jutsu(J4.smoke, "SELF", [C.tHas("increasedamagegiven", P.smokeIdg)]),
  R.jutsu(J4.arm, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [C.noSummon()]),
  R.end([]),
];
export const armRules = () => [R.jutsu(J4.lash, "SELF", []), R.end([])];
export const isoKit = () => [J4.churn, J4.hide, J4.tide, J4.breaker, J4.harpoon, J4.bw1Mark, J4.bw1Land, J4.bw2Mark, J4.bw2Crash, J4.bw2Surface, J4.clear, J4.cleanse, J4.anchor, J4.smoke, J4.swell, J4.arm];
export const STUN_PREVENT = { type: "stunprevent", power: 100, rounds: 99, target: "INHERIT", appearSfx: "", direction: "offence", calculation: "percentage", description: "Prevents being stunned", disappearSfx: "", powerPerLevel: 0, appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "" };
export const isoAiRecord = (P: V4) => ({
  ...IN.boss.data, username: "Isonade", poolsMultiplier: P.poolsMultiplier, statsMultiplier: P.statsMultiplier,
  ...Object.fromEntries(STATS.map((s) => [s, Math.round(STAT_PER_MULT * P.statsMultiplier * 100) / 100])),
  jutsus: isoKit(), effects: [STUN_PREVENT], includeDefaultRules: false, rules: isoRules(P), avatarFacing: "left",
});
export const armAiRecord = () => ({ ...IN.echo.data, username: "Grasping Arm", isSummon: true, jutsus: [J4.lash], effects: [], items: [], includeDefaultRules: false, rules: armRules() });
export const isoValidate = (P: V4) => {
  const v = validator();
  for (const j of Object.values(buildRecords(P))) v.jutsu(j);
  for (const r of [...isoRules(P), ...armRules()]) v.rule(r);
  const rec = isoAiRecord(P);
  v.ai(BOSS_ID, { ...rec, items: IN.boss.data.items });
  v.ai(ARM_ID, armAiRecord());
  if (rec.rules.length > AI_PROFILE_MAX_RULES) v.issues.push(`Isonade has ${rec.rules.length} rules (cap ${AI_PROFILE_MAX_RULES})`);
  return v.issues;
};

/* ------------------------------------------------------------------ the fight */
const BEAT_NAMES: Record<string, string> = {
  [J4.hide]: "Hide", [J4.tide]: "Tide", [J4.breaker]: "Breaker", [J4.harpoon]: "Harpoon", [J4.bw1Mark]: "BW-I mark", [J4.bw1Land]: "BW-I land",
  [J4.bw2Mark]: "Deep sink", [J4.bw2Crash]: "Deep crash", [J4.bw2Surface]: "Deep surface", [J4.clear]: "Scour", [J4.cleanse]: "Shed", [J4.anchor]: "Anchor",
  [J4.smoke]: "Silt", [J4.bite]: "Bite", [J4.swell]: "Swell", [J4.arm]: "Arm", [J4.churn]: "churn",
};
type Fight = {
  seed: number; read: number; outcome: string; rounds: number; playerHpPct: number; bossHpPct: number; minHpPct: number;
  bossActs: Record<string, number>; dmgBySource: Record<string, number>; breakers: { r: number; dmg: number; answered: string[] }[];
  deep: { r: number; broke: boolean; dmg: number }[]; bw1: { r: number; dmg: number }[]; playerAnswers: Record<string, number>; misreads: number;
  beatLog: string[]; bossDmgTotal: number; trace?: string[];
};

export const runFight = async (P: V4, seed: number, readP: number, trace = false): Promise<Fight> => {
  const rand = mulberry32(seed);
  const orig = Math.random;
  Math.random = rand;
  seedEntropy(seed);
  try {
    const recs: Record<string, any> = { ...allCapturedRecords(), ...buildRecords(P) };
    const rec = isoAiRecord(P);
    const boss = aiRow(BOSS_ID, rec, rec.offence, recs, rec.rules, rec.effects, IN.boss.data.items.flatMap((it: any) => it.ids));
    const a = armAiRecord();
    const arm = aiRow(ARM_ID, a, IN.echo.liveStats.offence, recs, a.rules, [], []);
    const kit = PLAYER_VARIANTS.average!.jutsuIds;
    // A strong player focuses the boss, not the add that rises beside them: aim every rule at the biggest enemy.
    const focus = (rs: any[]) => JSON.parse(JSON.stringify(rs).replaceAll('"CLOSEST_OPPONENT"', '"HIGHEST_MAX_HEALTH_OPPONENT"'));
    const v = { ...PLAYER_VARIANTS.average!, damageGivenPct: P.playerDg, rules: focus(playerRules(kit, t0.jutsu)) };
    const player = playerQueryUser(0, v as never, t0.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, t0.jutsu);
    const pets = [petFor(player)];
    (player as any).activePetId = pets[0]!.id;
    let b = await assembleFloor({ players: [player], enemyRows: { [BOSS_ID]: boss, [ARM_ID]: arm }, floor: { kind: "boss", waves: [{ aiIds: [BOSS_ID], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest", pets });
    for (const [id, r] of Object.entries(recs)) if (!(b.extraState.jutsus as any)[id]) (b.extraState.jutsus as any)[id] = r;
    const grid = getBattleGrid(1, b);
    const puid = player.userId;
    const pu = () => b.usersState.find((u) => u.userId === puid)!;
    const maxHp = getEffectiveMaxPool(pu() as never, b.usersEffects as never, "Health");
    const bossU = () => b.usersState.find((u) => u.controllerId === BOSS_ID && !u.isSummon)!;
    const bossUid = bossU().userId;
    const f: Fight = { seed, read: readP, outcome: "stalled", rounds: 0, playerHpPct: 0, bossHpPct: 0, minHpPct: 100, bossActs: {}, dmgBySource: {}, breakers: [], deep: [], bw1: [], playerAnswers: {}, misreads: 0, beatLog: [], bossDmgTotal: 0, ...(trace ? { trace: [] } : {}) };
    const fx = (uid: string, type: string, live = false) => (b.usersEffects as any[]).filter((e) => e.targetId === uid && e.type === type && (e.rounds ?? 1) > 0 && (!live || !e.castThisRound));
    const sum = (es: any[]) => es.reduce((s, e) => s + (e.power ?? 0), 0);
    if (trace) f.trace!.push(`player start effects: ${(b.usersEffects as any[]).filter((e) => e.targetId === puid).map((e) => `${e.type} ${e.power} ${e.fromType ?? ""}`).join(", ")}; maxHp ${Math.round(maxHp)}`);
    const tryAction = (actionId: string, c: Cell) => {
      const action = availableUserActions(b, puid, true, true).find((x) => x.id === actionId);
      if (!action || !actionPointsAfterAction(pu(), b, action).canAct) return false;
      try { b = performBattleAction({ battle: structuredClone(b), action, grid, contextUserId: puid, actorId: puid, longitude: c[0], latitude: c[1] }).newBattle; return true; } catch { return false; }
    };
    const ready = (id: string) => availableUserActions(b, puid, true, true).some((x) => x.id === id && actionPointsAfterAction(pu(), b, x).canAct);
    const readRand = mulberry32((seed ^ 0x51ed) >>> 0);
    const readMemo = new Map<string, boolean>();
    /** A reading player gets each situation right with probability readP (one roll per situation per round). */
    const reads = (sit: string) => {
      const k = `${b.round}:${sit}`;
      if (!readMemo.has(k)) { const ok = readP >= 1 || readRand() < readP; readMemo.set(k, ok); if (!ok) f.misreads++; }
      return readMemo.get(k)!;
    };
    const free = (c: Cell) => !b.usersState.some((u) => u.longitude === c[0] && u.latitude === c[1] && stillInBattle(u, b.usersEffects));
    const redCells = () => new Set((b.groundEffects as any[]).filter((g) => g.type === "visual" && g.staticAnimation === ANIM.safe && ((g.rounds ?? 1) > 0 || g.castThisRound)).map((g) => `${g.longitude},${g.latitude}`));
    const answered: string[] = [];
    let answerRound = -1;
    /** The answers a strong player has without kit: Clear, Cleanse, Defensive Stance, Basic Heal, Replacement, plus the kit's pierce. */
    const smartStep = (): string | null => {
      if (answerRound !== b.round) { answered.length = 0; answerRound = b.round; }
      const here: Cell = [pu().longitude, pu().latitude];
      const bp: Cell = [bossU().longitude, bossU().latitude];
      // Black Water I marked: get onto a crate.
      const safe = redCells();
      if (safe.size && !safe.has(key(here)) && reads("bw1")) {
        const crates = ALL.filter((c) => safe.has(key(c)) && free(c)).sort((x, y) => dist(x, here) - dist(y, here));
        const c = crates[0];
        if (c && dist(c, here) <= 5 && tryAction("replacementTechnique", c)) return "crate (replacement)";
        if (c) { const step = ALL.filter((n) => dist(n, here) === 1 && free(n) && dist(n, c) < dist(here, c)).sort((x, y) => dist(x, c) - dist(y, c))[0]; if (step && tryAction("move", step)) return "crate (move)"; }
      }
      if (safe.size && safe.has(key(here))) return null; // on a crate: fight from it (no moving off)
      // The Deep: everything into the shield, pierce first.
      if (fx(bossUid, MK.bw2).length && sum(fx(bossUid, "shield")) > 0 && reads("deep")) {
        // Silt on me halves this turn's damage: Cleanse it first, or the shield holds.
        if (Math.abs(sum(fx(puid, "decreasedamagegiven", true))) >= 50 && ready("cleanse") && tryAction("cleanse", here)) { answered.push("Cleanse"); return "Cleanse the Silt before the Deep"; }
        const pierce = availableUserActions(b, puid, true, true).find((x: any) => x.effects?.some((e: any) => e.type === "pierce") && actionPointsAfterAction(pu(), b, x).canAct && dist(here, bp) <= (x.range ?? 1));
        if (pierce && tryAction(pierce.id, bp)) return `pierce the Deep shield (${pierce.name})`;
        return null; // every AP into the shield this turn: no Stance, no Cleanse
      }
      // Its Tide buffs are live: Clear them before the Breaker (instant).
      const bossIdg = sum(fx(bossUid, "increasedamagegiven", true));
      if (fx(bossUid, MK.breaker).length && bossIdg >= P.tideBuff && ready("clear") && dist(here, bp) <= 4 && reads("clearTide")) { if (tryAction("clear", bp)) { answered.push("Clear"); return "Clear its Tide buffs"; } }
      // Brand or Silt on me: Cleanse.
      const brand = sum(fx(puid, "increasedamagetaken", true));
      const silt = Math.abs(sum(fx(puid, "decreasedamagegiven", true)));
      // Save the Cleanse for the Brand; the Silt only when no Breaker is coming soon.
      const breakerSoon = fx(bossUid, MK.tide).length > 0 || fx(bossUid, MK.breaker).length > 0;
      if (((brand >= P.brand && fx(bossUid, MK.breaker).length > 0) || brand >= 2 * P.brand || (silt >= 50 && !breakerSoon)) && ready("cleanse") && reads("cleanse")) { if (tryAction("cleanse", here)) { answered.push("Cleanse"); return brand ? "Cleanse the Brand" : "Cleanse the Silt"; } }
      // Defend a round ahead: Tide is due this round (Hide laid its marker), so Defensive Stance goes live for the Breaker.
      const tideDue = fx(bossUid, MK.swell).length > 0;
      const stanced = fx(puid, "decreasedamagetaken").length > 0;
      if (tideDue && !stanced && ready("defensiveStance") && reads("stance")) { if (tryAction("defensiveStance", here)) return "Defensive Stance ahead of the Breaker"; }
      // Low: heal.
      if (pu().curHealth < 0.45 * maxHp && ready("basicHeal")) { if (tryAction("basicHeal", here)) return "Basic Heal"; }
      return null;
    };
    const actionRounds: number[] = [];
    let lastBreaker: { r: number; dmg: number; answered: string[] } | null = null;
    const maxRounds = 40;
    for (let step = 0; step < maxRounds * 40; step++) {
      const pre = alignBattle(b, actionRounds, puid);
      if (pre.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
      if (b.round > maxRounds) break;
      const actor = pre.actor;
      const human = actor.userId === puid;
      tickClock(1000);
      const hpBefore = new Map(b.usersState.map((u) => [u.userId, u.curHealth]));
      let actionId: string | undefined;
      let why: string | null = null;
      const bkState = { tide: sum(fx(bossUid, "increasedamagegiven", true)) > 0, stance: sum(fx(puid, "decreasedamagetaken", true)) < 0, brand: sum(fx(puid, "increasedamagetaken", true)) > 0 };
      if (trace && !human && actor.userId === bossUid) f.trace!.push(`  probe pre-boss: player DR ${(b.usersEffects as any[]).filter((e) => e.targetId === puid && e.type === "decreasedamagetaken").map((e) => `${e.power}${e.castThisRound ? "*" : ""}${e.fromType ? "/" + e.fromType : ""}`).join(" ")} | boss DDG ${(b.usersEffects as any[]).filter((e) => e.targetId === bossUid && e.type === "decreasedamagegiven").map((e) => `${e.power}${e.castThisRound ? "*" : ""}`).join(" ")}`);
      if (human) why = smartStep();
      if (why) { actionId = why; f.playerAnswers[why.split(" (")[0]!] = (f.playerAnswers[why.split(" (")[0]!] ?? 0) + 1; }
      else {
        const res = performAIaction(b, grid, actor.userId);
        actionId = res.nextActionId;
        // A reading player doesn't walk off a crate while Black Water is marked.
        if (human && (actionId === "move" || actionId === "replacementTechnique") && redCells().size && redCells().has(`${pu().longitude},${pu().latitude}`)) actionId = tryAction("wait", [pu().longitude, pu().latitude]) ? "wait" : (b = res.nextBattle, actionId);
        else b = res.nextBattle;
      }
      const post = alignBattle(b, actionRounds, puid);
      if (post.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(post.actionRound)) actionRounds.push(post.actionRound);
      if (!actionId && actor.isAutoCombat) b.roundStartAt = new Date(Date.now() - 61_000);
      const pLoss = Math.max(0, (hpBefore.get(puid) ?? 0) - pu().curHealth);
      const bl = Math.max(0, (hpBefore.get(bossUid) ?? 0) - bossU().curHealth);
      f.bossDmgTotal += bl;
      const isBoss = actor.userId === bossUid;
      const nm = isBoss ? BEAT_NAMES[actionId ?? ""] ?? actionId ?? "none" : actionId ?? "none";
      if (isBoss && actionId) f.bossActs[nm] = (f.bossActs[nm] ?? 0) + 1;
      if (!human && pLoss > 0) { const src = (actor as any).summonSourceId === ARM_ID ? "Grasping Arm" : isBoss ? nm : actor.username; f.dmgBySource[src] = (f.dmgBySource[src] ?? 0) + pLoss; }
      if (human && pLoss > 0) f.dmgBySource["ticks on own turn (wounds)"] = (f.dmgBySource["ticks on own turn (wounds)"] ?? 0) + pLoss;
      if (isBoss && actionId === J4.breaker) { lastBreaker = { r: pre.actionRound, dmg: pLoss, answered: [...answered], ...bkState } as any; f.breakers.push(lastBreaker!); }
      if (isBoss && actionId === J4.bw1Land) f.bw1.push({ r: pre.actionRound, dmg: pLoss });
      if (isBoss && (actionId === J4.bw2Crash || actionId === J4.bw2Surface)) f.deep.push({ r: pre.actionRound, broke: actionId === J4.bw2Surface, dmg: pLoss });
      if (isBoss && actionId && ![J4.churn].includes(actionId)) f.beatLog.push(`r${pre.actionRound}:${nm}`);
      f.minHpPct = Math.min(f.minHpPct, (100 * Math.max(0, pu().curHealth)) / maxHp);
      if (trace && actionId !== J4.churn) {
        const who = human ? "player" : isBoss ? "Isonade" : (actor as any).petId ? "pet" : (actor as any).summonSourceId === ARM_ID ? "arm" : actor.username;
        const pn = human && !why ? (b.extraState.jutsus as any)[actionId ?? ""]?.name ?? actionId : nm;
        const pIdg = sum(fx(puid, "increasedamagegiven")); const pDr = sum(fx(puid, "decreasedamagetaken"));
        const bIdg = sum(fx(bossUid, "increasedamagegiven")); const bSh = sum(fx(bossUid, "shield"));
        const armU = b.usersState.find((u: any) => u.controllerId === ARM_ID && stillInBattle(u, b.usersEffects));
        f.trace!.push(`r${pre.actionRound} ${who.padEnd(7)} @${pu().longitude},${pu().latitude} arm ${armU ? Math.round(armU.curHealth) + "@" + armU.longitude + "," + armU.latitude : "-"} AP ${Math.round((pu() as any).actionPoints ?? -1)} ${String(pn).padEnd(36)} pHP ${Math.round(pu().curHealth)} (-${Math.round(pLoss)}) boss ${(100 * bossU().curHealth / bossU().maxHealth).toFixed(1)}% (-${Math.round(bl)}) | p idg ${pIdg} dr ${pDr} | b idg ${bIdg} shield ${Math.round(bSh)} mk[${Object.entries(MK).filter(([, t]) => fx(bossUid, t).length).map(([k]) => k).join(",")}]`);
      }
      const side = (dir: string) => b.usersState.some((u) => u.direction === dir && !u.isSummon && stillInBattle(u, b.usersEffects));
      if (!side(pu().direction)) { f.outcome = "lost"; break; }
      if (!b.usersState.some((u) => u.controllerId === BOSS_ID && !u.isSummon && stillInBattle(u, b.usersEffects))) { f.outcome = "won"; break; }
    }
    f.rounds = b.round;
    f.playerHpPct = r1((100 * Math.max(0, pu().curHealth)) / maxHp)!;
    f.bossHpPct = r1((100 * Math.max(0, bossU().curHealth)) / bossU().maxHealth)!;
    f.minHpPct = r1(f.minHpPct)!;
    (f as any).bossMaxHp = bossU().maxHealth;
    (f as any).playerMaxHp = Math.round(maxHp);
    return f;
  } finally {
    Math.random = orig;
  }
};

const summarise = (fs: any[]) => {
  const wins = fs.filter((f) => f.outcome === "won");
  const src: Record<string, number> = {};
  for (const f of fs) for (const [k, v] of Object.entries<number>(f.dmgBySource)) src[k] = (src[k] ?? 0) + v;
  const acts: Record<string, number> = {};
  for (const f of fs) for (const [k, v] of Object.entries<number>(f.bossActs)) acts[k] = (acts[k] ?? 0) + v;
  const ans: Record<string, number> = {};
  for (const f of fs) for (const [k, v] of Object.entries<number>(f.playerAnswers)) ans[k] = (ans[k] ?? 0) + v;
  const brk = fs.flatMap((f) => f.breakers);
  const brkBy = (pred: (x: any) => boolean) => { const xs = brk.filter(pred).map((x: any) => x.dmg); return { n: xs.length, median: Math.round(median(xs) ?? 0) }; };
  const deep = fs.flatMap((f) => f.deep);
  return {
    fights: fs.length, winPct: r1((100 * wins.length) / fs.length),
    rounds: { median: median(wins.map((f) => f.rounds)), p10: quantile(wins.map((f) => f.rounds), 0.1), p90: quantile(wins.map((f) => f.rounds), 0.9) },
    hpLeftWin: { median: r1(median(wins.map((f) => f.playerHpPct))), p10: r1(quantile(wins.map((f) => f.playerHpPct), 0.1)), p90: r1(quantile(wins.map((f) => f.playerHpPct), 0.9)) },
    minHpMedian: r1(median(fs.map((f) => f.minHpPct))), bossHpLeftLossMedian: r1(median(fs.filter((f) => f.outcome !== "won").map((f) => f.bossHpPct))),
    bossMaxHp: fs[0]?.bossMaxHp, playerMaxHp: fs[0]?.playerMaxHp,
    breaker: { all: brkBy(() => true), clearedOrCleansed: brkBy((x) => x.answered.length > 0), unanswered: brkBy((x) => x.answered.length === 0),
      byState: Object.fromEntries([...new Set(brk.map((x: any) => `${x.tide ? "Tide" : "noTide"}/${x.brand ? "Brand" : "noBrand"}/${x.stance ? "Stance" : "noStance"}`))].map((k) => [k, brkBy((x: any) => `${x.tide ? "Tide" : "noTide"}/${x.brand ? "Brand" : "noBrand"}/${x.stance ? "Stance" : "noStance"}` === k)])) },
    deep: { n: deep.length, brokePct: r1((100 * deep.filter((d: any) => d.broke).length) / Math.max(1, deep.length)), crashDmgMedian: Math.round(median(deep.filter((d: any) => !d.broke).map((d: any) => d.dmg)) ?? 0) },
    bw1DmgMedian: Math.round(median(fs.flatMap((f) => f.bw1.map((x: any) => x.dmg))) ?? 0), bw1PerFight: r1(fs.reduce((s, f) => s + f.bw1.length, 0) / fs.length),
    bossActsPerFight: Object.fromEntries(Object.entries(acts).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, r1(v / fs.length)])),
    playerAnswersPerFight: Object.fromEntries(Object.entries(ans).map(([k, v]) => [k, r1(v / fs.length)])),
    damageToPlayerPerFight: Object.fromEntries(Object.entries(src).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, Math.round(v / fs.length)])),
    misreadsPerFight: r1(fs.reduce((s, f) => s + f.misreads, 0) / fs.length),
  };
};

const main = async () => {
  const P = v4(opt("params") ? loadJson(resolve(opt("params")!)) : {});
  if (opt("dg")) P.playerDg = Number(opt("dg"));
  const issues = isoValidate(P);
  console.log(issues.length ? `VALIDATION ISSUES:\n  ${issues.join("\n  ")}` : `valid (Isonade ${isoRules(P).length} rules, arm ${armRules().length})`);
  if (opt("write-spec")) {
    const spec = { _note: "Isonade v4 build spec. Generated by isonade_v4.ts --write-spec; offline engine-tested, NOT pushed. Ids are placeholders (iso-*).", params: P, ais: { [BOSS_ID]: isoAiRecord(P), [ARM_ID]: armAiRecord() }, newJutsu: buildRecords(P), markers: MK, validation: issues.length ? issues : "valid" };
    mkdirSync(dirname(resolve(opt("write-spec")!)), { recursive: true });
    writeFileSync(resolve(opt("write-spec")!), `${JSON.stringify(spec, null, 1)}\n`);
  }
  const reads = opt("read", "1,0.85,0.7")!.split(",").map(Number);
  if (opt("trace")) {
    const f = await runFight(P, Number(opt("trace")), reads[0]!, true);
    console.log(`--- trace seed ${opt("trace")} read ${reads[0]}: ${f.outcome} in ${f.rounds} rounds, player ${f.playerHpPct}%, boss ${f.bossHpPct}%`);
    for (const l of f.trace!) console.log("  " + l);
  }
  const seeds = Number(opt("seeds", opt("trace") ? "0" : "20"));
  const out: any = { generatedBy: "isonade_v4.ts", params: P, dmgConfig: dmg.name, seeds, reads: {} };
  if (seeds > 0) for (const rp of reads) {
    const fs: any[] = [];
    for (let i = 0; i < seeds; i++) fs.push(await runFight(P, 1 + i, rp));
    const s = summarise(fs);
    out.reads[String(rp)] = { summary: s, fights: fs };
    console.log(`\n== ${P.name} read ${rp}: ${JSON.stringify(s)}`);
  }
  if (opt("out")) { mkdirSync(dirname(resolve(opt("out")!)), { recursive: true }); writeFileSync(resolve(opt("out")!), `${JSON.stringify(out, null, 1)}\n`); console.log(`wrote ${opt("out")}`); }
};
if (import.meta.main) await main();
