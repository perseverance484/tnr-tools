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

/** --skip clearTide,cleanse,stance,bw1,deep: answers this player never gives (one-miss ablations). */
const HAS = (k: string) => (opt("harass") ?? "").split(",").includes(k);
const SKIP = new Set((opt("skip") ?? "").split(",").filter(Boolean));
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
  // Silt Cloud: the brace before a big hit (director 2026-11-19 17:06Z: one stronger DR, 40% for 1 round, cast in
  // anticipation of a big hit). siltDdg is the old -% damage given on the player; 0 drops it.
  braceDr: 25, braceRounds: 2, braceCd: 10 as number | undefined, siltDdg: 50, braceHigh: false,
  anchorPower: 110,
  anchorWound: 4,
  // extras
  bitePct: 30, // below 50%, once: +% damage given for the rest of the fight (Clearable)
  armHp: 4000, armPower: 60, armRounds: 30, armCooldown: 5, lashPower: 70,
  churnAp: 10, beatAp: 60, reactAp: 60, sideAp: 30,
  deepAp: 70, // The Deep's sink leaves 20 AP, so no Silt Cloud (30) rides along: the break round is never smoked
  // v5 (director 2026-11-19 19:28Z: Strict budget, base DR as an AI tag, one clear window per answer)
  baseDr: 30, // permanent damage taken reduction, an AI tag (realised as fromType bloodline: the player's Clear can't take it)
  brandBeat: 150, // Brine Brand alone (the Cleanse window): +% damage taken on the player for the Undertow
  undertowPower: 400,
  reactions: false, gearIdg: 80, // live marks clearIdg/smokeIdg are what goes on the live rule
  brandHealPrevent: 0, // rounds of healprevent on the player from Brine Brand (Cleanse removes it with the brand)
  borePower: 900, // Tidal Bore (the Smoke window)
  boreAt: 55,
  deepDr: 80, // The Deep: % DR on itself for the break round (pierce ignores it: the Pierce window)
  deepAt: 35,
  // the player
  lifesteal: true, // Eclipse Drain (35% lifesteal + 30% damage given, 2 rounds, cd 7, 40 AP) cast whenever it is ready
  playerDg: 120, // gear stand-in damage given %: reproduces dauntless's live 12-round v3 kill (iso_cal.ts)
  // v7 probe (director 2026-11-19 23:47Z: a player's move-prevent must not throw off the fight)
  undertowMark: 100, undertowThreshold: 1, // A: Brine Brand's own moveprevent power and the Undertow rule threshold
  undertowKey: "moveprevent", harpoonThreshold: 1, undertowOnBrand: false, // A': key type (elementalseal keeps its power; prevent tags are reset to 100 on landing); C: key on the Brand itself
  undertowCd: 2, undertowLow: false, // B: Undertow cooldown, and its rule moved down to just above Barnacle Hide
  sealMark: 100, sealThreshold: 1, // the same key for Black Water I (its omen's seal marker)
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
  brandBeat: "iso-brine-brand", undertow: "iso-undertow", boreMark: "iso-the-swell", boreRise: "iso-the-swell-rises", boreLand: "iso-tidal-bore",
};
/** Chain markers. Negative polarity (a player's Clear leaves them), no gameplay on this boss: it has no cooldown
 * actions listed, never flees, has no elements, heals or bloodline. */
export const MK = {
  tide: "fleeprevent", breaker: "increasecooldown", harpoon: "elementalseal", swell: "healprevent", bw1: "seal", bw2: "disarm", // decreaseheal is stored negative (tags.ts decreaseHealGiven), so has_effect never sees it
  react: "decreasecooldown", // positive on purpose: its own Cleanse must not strip it mid-turn
  brand: "healprevent", undertow: "moveprevent", bore: "increasepoolcost", // v5 (swell retired)
  boreB: "robprevent", // inert in combat and laid by no other move
  // shared-cooldown tags (increasepoolcost, moveprevent, seal, pierce, clear...) lock other actions with the same tag:
  // each of these markers is laid by one jutsu only.
};
export const ANIM = { red: "tg_heavy", safe: "tg_safe", bodyWater: "anim_isonade_body_water_v1", hit: "anim_isonade_slam_v1", surge: "anim_isonade_surge_v1", eye: "anim_isonade_eye_v1", bite: "anim_isonade_bite_v1", armBurst: "anim_isonade_arm_burst_v1", armLash: "anim_isonade_arm_lash_v1" };
const marker = (type: string, rounds = 2, power = 100) => tag(type, {
  power: ["increasecooldown", "decreasecooldown"].includes(type) ? 1 : power, rounds, target: "SELF",
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
    target: "SELF", method: "SINGLE", range: 0, cooldown: 3, actionCostPerc: P.beatAp,
    effects: [tag("shield", { power: 100, health: P.hideShield, rounds: P.hideRounds, target: "SELF", description: "Barnacle Hide" }),
      ...(P.hideDr ? [T.pct("decreasedamagetaken", P.hideDr, 2, { target: "SELF", ...statsAll, description: "Barnacle Hide" })] : []), marker(MK.tide)] }));
  // v5: one tell per answer. Tide (Clear it), Brine Brand (Cleanse it), The Swell (Smoke the Tidal Bore).
  add(jutsu(J4.tide, { name: "The Tide Draws Back", description: "The water pulls away from the shore and gathers into it. Its next hit, the Breaker, is huge. Clear it now.",
    battleDescription: "The water pulls away from the shore and gathers around %user.", target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: P.beatAp,
    effects: [T.pct("increasedamagegiven", P.tideBuff, 1, { target: "SELF", ...statsAll, description: "The tide gathers" }), marker(MK.breaker)] }));
  add(jutsu(J4.brandBeat, { name: "Brine Brand", description: "It brands you with brine. Its next hit, the Undertow, will crush you. Cleanse it now.",
    battleDescription: "Brine burns into %target.", ...onPlayer, cooldown: 99, actionCostPerc: P.beatAp,
    effects: [T.pct("increasedamagetaken", P.brandBeat, 1, { friendlyFire: "ENEMIES", ...statsAll, description: "Brine Brand" }), ...(P.brandHealPrevent ? [tag("healprevent", { power: 100, rounds: P.brandHealPrevent, friendlyFire: "ENEMIES", description: "Brine Brand: no healing or lifesteal until cleansed" })] : []), marker(P.undertowKey, 2, P.undertowMark)] }));
  add(jutsu(J4.undertow, { name: "Undertow", description: "It drags you under.", battleDescription: "The undertow drags %target under.", ...onPlayer, cooldown: P.undertowCd, actionCostPerc: P.beatAp,
    effects: [hit(P.undertowPower, { appearAnimation: ANIM.surge }), T.pct("wound", P.breakerWound, 2, { friendlyFire: "ENEMIES", description: "Undertow wound" })] }));
  add(jutsu(J4.boreMark, { name: "The Swell", description: "The sea rears up behind it. In two turns the Tidal Bore crashes over you: Smoke it now, or brace.",
    battleDescription: "The sea rears up behind %user.", target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: P.beatAp, effects: [marker(MK.bore, 3)] }));
  add(jutsu(J4.boreRise, { name: "The Swell Rises", description: "The wave stands over the hold. It breaks next turn.",
    battleDescription: "The wave stands over the hold.", target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: P.beatAp, effects: [marker(MK.boreB, 2)] }));
  add(jutsu(J4.boreLand, { name: "Tidal Bore", description: "The wave breaks over everything.", battleDescription: "The Tidal Bore breaks over %target.", ...onPlayer, cooldown: 99, actionCostPerc: P.beatAp,
    effects: [hit(P.borePower, { appearAnimation: ANIM.surge })] })); // no self-cleanse: it would strip the player's Smoke
  add(jutsu(J4.breaker, { name: "Breaker", description: "The wave breaks over you. Then it hangs exposed for a round.", battleDescription: "The wave breaks over %target.", ...onPlayer,
    cooldown: 2, actionCostPerc: P.beatAp,
    effects: [hit(P.breakerPower, { appearAnimation: ANIM.surge }), T.pct("wound", P.breakerWound, 2, { friendlyFire: "ENEMIES", description: "Breaker wound" }),
      tag("weakness", { target: "SELF", rounds: 1, dmgModifier: P.breakerWindow, ...statsAll, power: 100, staticAnimation: ANIM.eye, description: "Spent: takes extra damage" }), marker(MK.harpoon)] }));
  add(jutsu(J4.harpoon, { name: "Harpoon Line", description: "It spits the old harpoon back through you. Goes through damage reduction and shields.", battleDescription: "%user spits a rusted harpoon through %target.",
    ...onPlayer, cooldown: 2, actionCostPerc: P.beatAp, effects: [T.pierce(P.harpoonPower, { ...statsAll }), marker(MK.brand)] }));
  // --- Black Water I: the crates
  add(jutsu(J4.bw1Mark, { name: "Black Water", description: "Everything but the floating crates is marked red. Black water fills the room next turn.", battleDescription: "The water goes still and black. Only the floating crates stay pale.",
    target: "GROUND", method: "COORDINATES", range: 0, cooldown: 99, actionCostPerc: P.beatAp, coordinateTargeting: field(P.crates, "EXCLUDE"),
    effects: [T.visual(ANIM.red, 1), T.visual(ANIM.safe, 1, { target: "COORDINATES", coordinateTargeting: field(P.crates) }), marker(MK.bw1, 2, P.sealMark)] }));
  add(jutsu(J4.bw1Land, { name: "Black Water", description: "Black water fills every hex but the crates; then it surfaces to feed.", battleDescription: "Black water crashes down. %user surfaces to feed.",
    target: "CHARACTER", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: P.beatAp, coordinateTargeting: field(notCrates),
    effects: [hit(P.bw1Power, { appearAnimation: ANIM.surge }), tag("weakness", { target: "SELF", rounds: 1, dmgModifier: P.bw1Feed, ...statsAll, power: 100, staticAnimation: ANIM.eye, description: "Feeding: takes extra damage" })] }));
  // --- Black Water II: The Deep (break the shield or eat the crash)
  add(jutsu(J4.bw2Mark, { name: "The Deep", description: "It sinks under black water behind a heavy shield. Break the shield before its next turn, or the whole room floods.",
    battleDescription: "%user sinks out of sight. The whole hold goes black.", target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: P.deepAp,
    effects: [tag("shield", { power: 100, health: P.bw2Shield, rounds: 1, target: "SELF", description: "The Deep" }),
      ...(P.deepDr ? [T.pct("decreasedamagetaken", P.deepDr, 1, { target: "SELF", ...statsAll, description: "The Deep" })] : []), marker(MK.bw2)] }));
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
  add(jutsu(J4.smoke, { name: "Silt Cloud", description: P.siltDdg ? "It churns up silt: your damage next round is cut hard, and it takes less." : "It churns up silt and braces: it takes far less damage next round.", battleDescription: "%user thrashes and braces. Silt clouds the hold.", ...onPlayer,
    cooldown: P.braceCd ?? P.reactCd, actionCostPerc: P.sideAp, effects: [
      ...(P.siltDdg ? [T.pct("decreasedamagegiven", P.siltDdg, 1, { friendlyFire: "ENEMIES", ...statsAll, description: "Silt Cloud" })] : []),
      T.pct("decreasedamagetaken", P.braceDr, P.braceRounds, { target: "SELF", ...statsAll, description: "Silt Cloud" })] }));
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
const utCond = (P: V4) => P.undertowOnBrand ? [C.tHas("increasedamagetaken", P.brandBeat)] : [C.has(P.undertowKey, P.undertowThreshold)];
export const isoRules = (P: V4) => [
  R.jutsu(J4.churn, "SELF", []), // 10 AP; also prunes markers two rounds old before anything reads them
  // Set pieces can't be interrupted.
  R.jutsu(J4.bw2Crash, "SELF", [C.has(MK.bw2), C.has("shield", 1)]),
  R.jutsu(J4.bw2Surface, "SELF", [C.has(MK.bw2)]),
  R.jutsu(J4.bw1Land, "SELF", [C.has(MK.bw1, P.sealThreshold)]),
  R.jutsu(J4.boreLand, "SELF", [C.has(MK.bore), C.has(MK.boreB)]),
  R.jutsu(J4.boreRise, "SELF", [C.has(MK.bore)]),
  // v6 (deepFirst): The Deep's omen right after the set-piece lands, ahead of the reactions and the chain, so crossing
  // 35% always calls it. Placed after the crash rule, so the crash can't fire the same turn (conditions see this turn's
  // effects); at 70 AP nothing else (Silt 30, Hide 60) rides along on the omen turn, so the pierce window stays clean.
  ...(P.deepFirst ? [R.jutsu(J4.bw2Mark, "SELF", [C.hb(P.deepAt)])] : []),
  // Reactions (no tell): strip a big damage stack (Eclipse Drain's lifesteal goes with it), or brace for it.
  // Scour/Silt reactions are optional (P.reactions). target_has_effect sums every effect of the type, gear and
  // bloodline passives included (a geared player carries ~80 damage given from round 1). The sim player has no gear
  // passives, so a live mark of M is simulated as M - P.gearIdg.
  ...(P.reactions ? [R.jutsu(J4.clear, "SELF", [C.tHas("increasedamagegiven", P.clearIdg - P.gearIdg)]),
    R.jutsu(J4.smoke, "SELF", [C.tHas("increasedamagegiven", P.smokeIdg - P.gearIdg)])] : []),
  // The opening chain, once each: Hide, Tide (Clear), Breaker, Harpoon, Brine Brand (Cleanse), Undertow.
  ...(P.undertowLow ? [] : [R.jutsu(J4.undertow, "SELF", utCond(P))]),
  R.jutsu(J4.brandBeat, "SELF", [C.has(MK.brand)]),
  R.jutsu(J4.harpoon, "SELF", [C.has(MK.harpoon, P.harpoonThreshold)]),
  R.jutsu(J4.breaker, "SELF", [C.has(MK.breaker)]),
  R.jutsu(J4.tide, "SELF", [C.has(MK.tide)]),
  // Then the set pieces in order, each once, the first free round after its health line: crates, Tidal Bore (Smoke),
  // The Deep (Pierce).
  R.jutsu(J4.bw1Mark, "SELF", [C.hb(P.bw1At)]),
  R.jutsu(J4.boreMark, "SELF", [C.hb(P.boreAt)]),
  ...(P.deepFirst ? [] : [R.jutsu(J4.bw2Mark, "SELF", [C.hb(P.deepAt)])]),
  ...(P.undertowLow ? [R.jutsu(J4.undertow, "SELF", utCond(P))] : []),
  R.jutsu(J4.hide, "SELF", []),
  R.jutsu(J4.harpoon, "SELF", []),
  R.jutsu(J4.arm, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [C.noSummon()]),
  R.end([]),
];
export const armRules = () => [R.jutsu(J4.lash, "SELF", []), R.end([])];
export const isoKit = (P: V4) => [J4.churn, J4.hide, J4.tide, J4.breaker, J4.harpoon, J4.brandBeat, J4.undertow, J4.bw1Mark, J4.bw1Land, J4.boreMark, J4.boreRise, J4.boreLand, J4.bw2Mark, J4.bw2Crash, J4.bw2Surface, ...(P.reactions ? [J4.clear, J4.smoke] : []), J4.arm];
export const STUN_PREVENT = { type: "stunprevent", power: 100, rounds: 99, target: "INHERIT", appearSfx: "", direction: "offence", calculation: "percentage", description: "Prevents being stunned", disappearSfx: "", powerPerLevel: 0, appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "" };
export const BASE_DR = (power: number) => T.pct("decreasedamagetaken", power, 99, { target: "INHERIT", ...statsAll, description: "Old hull: takes less damage" });
export const isoAiRecord = (P: V4) => ({
  ...IN.boss.data, username: "Isonade", poolsMultiplier: P.poolsMultiplier, statsMultiplier: P.statsMultiplier,
  ...Object.fromEntries(STATS.map((s) => [s, Math.round(STAT_PER_MULT * P.statsMultiplier * 100) / 100])),
  jutsus: isoKit(P), effects: [STUN_PREVENT, ...(P.baseDr ? [BASE_DR(P.baseDr)] : [])], includeDefaultRules: false, rules: isoRules(P), avatarFacing: "left",
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
  [J4.smoke]: "Silt", [J4.bite]: "Bite", [J4.arm]: "Arm", [J4.churn]: "churn", [J4.brandBeat]: "Brand", [J4.undertow]: "Undertow", [J4.boreMark]: "Swell", [J4.boreRise]: "Swell rises", [J4.boreLand]: "Tidal Bore",
};
type Fight = {
  seed: number; read: number; outcome: string; rounds: number; playerHpPct: number; bossHpPct: number; minHpPct: number;
  bossActs: Record<string, number>; dmgBySource: Record<string, number>; breakers: { r: number; dmg: number; answered: string[] }[];
  deep: { r: number; broke: boolean; dmg: number }[]; bore: { r: number; dmg: number }[]; bw1: { r: number; dmg: number }[]; playerAnswers: Record<string, number>; misreads: number;
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
    // The two answers the stand-in kit lacks: Eclipse Drain (dauntless's lifesteal) and an Elite Smoke Bomb stand-in.
    const SIM_ECLIPSE = "sim-eclipse-drain", SIM_SMOKE = "sim-elite-smoke";
    (t0.jutsu as any)[SIM_ECLIPSE] = jutsu(SIM_ECLIPSE, { name: "Eclipse Drain", description: "sim stand-in", battleDescription: "%user drains.", target: "SELF", method: "SINGLE", range: 0, cooldown: 7, actionCostPerc: 40,
      effects: [T.pct("lifesteal", 35, 2, { target: "SELF", ...statsAll }), T.pct("increasedamagegiven", 30, 2, { target: "SELF", ...statsAll })] });
    (t0.jutsu as any)[SIM_SMOKE] = jutsu(SIM_SMOKE, { name: "Elite Smoke Bomb", description: "sim stand-in", battleDescription: "%user throws smoke.", target: "OPPONENT", method: "SINGLE", range: 5, cooldown: 10, actionCostPerc: 20,
      effects: [T.pct("decreasedamagegiven", 70, 1, { friendlyFire: "ENEMIES", ...statsAll }), T.pct("decreasedamagegiven", 70, 1, { target: "SELF", ...statsAll }), T.pct("decreasedamagetaken", 25, 2, { target: "SELF", ...statsAll })] });
    const SIM_ROOT = "sim-root", SIM_SEAL = "sim-seal";
    (t0.jutsu as any)[SIM_ROOT] = jutsu(SIM_ROOT, { name: "Root (Dragon's Tomb stand-in)", description: "sim stand-in", battleDescription: "%user roots %target.", target: "OPPONENT", method: "SINGLE", range: 5, cooldown: Number(opt("rootCd", "4")), actionCostPerc: 30,
      effects: [tag("moveprevent", { power: 100, rounds: 1, target: "INHERIT", description: "root" })] });
    (t0.jutsu as any)[SIM_SEAL] = jutsu(SIM_SEAL, { name: "Seal stand-in", description: "sim stand-in", battleDescription: "%user seals %target.", target: "OPPONENT", method: "SINGLE", range: 5, cooldown: Number(opt("sealCd", "4")), actionCostPerc: 30,
      effects: [tag("seal", { power: 100, rounds: 2, target: "INHERIT", description: "seal" })] });
    for (const id of [SIM_ECLIPSE, SIM_SMOKE, SIM_ROOT, SIM_SEAL]) recs[id] = (t0.jutsu as any)[id];
    const HARASS = [...(HAS("root") ? [SIM_ROOT] : []), ...(HAS("seal") ? [SIM_SEAL] : [])];
    // A strong player focuses the boss, not the add that rises beside them: aim every rule at the biggest enemy.
    const focus = (rs: any[]) => JSON.parse(JSON.stringify(rs).replaceAll('"CLOSEST_OPPONENT"', '"HIGHEST_MAX_HEALTH_OPPONENT"'));
    const v = { ...PLAYER_VARIANTS.average!, jutsuIds: [...kit, SIM_ECLIPSE, SIM_SMOKE, ...HARASS], damageGivenPct: P.playerDg, rules: focus(playerRules(kit, t0.jutsu)) };
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
    const f: Fight = { seed, read: readP, outcome: "stalled", rounds: 0, playerHpPct: 0, bossHpPct: 0, minHpPct: 100, bossActs: {}, dmgBySource: {}, breakers: [], deep: [], bore: [], bw1: [], playerAnswers: {}, misreads: 0, beatLog: [], bossDmgTotal: 0, ...(trace ? { trace: [] } : {}) };
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
      if (!readMemo.has(k)) { const ok = !SKIP.has(sit) && (readP >= 1 || readRand() < readP); readMemo.set(k, ok); if (!ok) f.misreads++; }
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
      // Clear window: the Tide's buff is on it and the Breaker lands this round. Clear is instant.
      const bossIdg = sum(fx(bossUid, "increasedamagegiven", true));
      if (fx(bossUid, MK.breaker).length && bossIdg >= P.tideBuff && ready("clear") && dist(here, bp) <= 4 && reads("clearTide")) { if (tryAction("clear", bp)) { answered.push("Clear"); return "Clear its Tide buffs"; } }
      // Cleanse window: Brine Brand is on me and the Undertow lands this round.
      const brand = sum(fx(puid, "increasedamagetaken", true));
      if (sum(fx(bossUid, P.undertowKey)) >= P.undertowThreshold && brand >= P.brandBeat && ready("cleanse") && reads("cleanse")) { if (tryAction("cleanse", here)) { answered.push("Cleanse"); return "Cleanse the Brand"; } }
      // Smoke window: The Swell went up last round; the Tidal Bore lands next round, so the smoke must go out now.
      const boreStage = fx(bossUid, MK.bore).length ? (fx(bossUid, MK.boreB).length ? 100 : 50) : 0;
      if (boreStage >= 50 && boreStage < 100 && ready(SIM_SMOKE) && reads("smoke")) { if (tryAction(SIM_SMOKE, bp)) { answered.push("Smoke"); return "Smoke the Tidal Bore"; } }
      // Defend a round ahead: a big hit lands next round (Tide or Brand due now, or The Swell up).
      const bigNext = fx(bossUid, MK.tide).length > 0 || fx(bossUid, MK.brand).length > 0 || (boreStage >= 50 && boreStage < 100);
      const stanced = fx(puid, "decreasedamagetaken").length > 0;
      if (bigNext && !stanced && ready("defensiveStance") && reads("stance")) { if (tryAction("defensiveStance", here)) return "Defensive Stance ahead of a big hit"; }
      // v7 probe: a player who roots or seals the boss whenever the move is ready (not to game it; it is just in their kit).
      for (const h of HARASS) if (ready(h) && dist(here, bp) <= 5 && tryAction(h, bp)) { (f as any).harass = ((f as any).harass ?? 0) + 1; return h === SIM_ROOT ? "root the boss" : "seal the boss"; }
      // Greedy lifesteal: Eclipse Drain whenever it is ready.
      if (P.lifesteal && ready(SIM_ECLIPSE)) { if (tryAction(SIM_ECLIPSE, here)) return "Eclipse Drain"; }
      // Low: heal.
      if (pu().curHealth < 0.45 * maxHp && ready("basicHeal")) { if (tryAction("basicHeal", here)) return "Basic Heal"; }
      return null;
    };
    const actionRounds: number[] = [];
    let origRules: any[] | null = null;
    let deepSeen = false;
    const PIERCE_IDS = Object.values(b.extraState.jutsus as any).filter((j: any) => j.effects?.some((e: any) => e.type === "pierce") && !String(j.id).startsWith("iso-")).map((j: any) => j.id);
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
      if (human) {
        // Hold the pierce for The Deep: a reading player doesn't spend it in the last stretch before the Deep line.
        const prof = (b.extraState as any).aiProfiles?.[(pu() as any).aiProfileId];
        if (prof) {
          if (!origRules) origRules = structuredClone(prof.rules);
          const deepSoon = /* a player who has read the fight saves its pierce for The Deep */ !deepSeen && !SKIP.has("deep") && !fx(bossUid, MK.bw2).length;
          prof.rules = deepSoon ? origRules.filter((r: any) => !PIERCE_IDS.includes(r.action?.jutsuId ?? r.jutsuId)) : structuredClone(origRules);
        }
        why = smartStep();
      }
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
      if (human) (f as any).leech = ((f as any).leech ?? 0) + Math.max(0, pu().curHealth - (hpBefore.get(puid) ?? 0));
      if (human && pLoss > 0) f.dmgBySource["ticks on own turn (wounds)"] = (f.dmgBySource["ticks on own turn (wounds)"] ?? 0) + pLoss;
      if (isBoss && actionId === J4.breaker) { lastBreaker = { r: pre.actionRound, dmg: pLoss, answered: [...answered], ...bkState } as any; f.breakers.push(lastBreaker!); }
      if (isBoss && actionId === J4.bw1Land) f.bw1.push({ r: pre.actionRound, dmg: pLoss });
      if (isBoss && actionId === J4.boreLand) f.bore.push({ r: pre.actionRound, dmg: pLoss });
      if (isBoss && actionId === J4.brandBeat) (f as any).brandR = pre.actionRound;
      if (isBoss && actionId === J4.bw1Mark) (f as any).bw1MarkR = pre.actionRound;
      if (isBoss && actionId === J4.undertow) { const br = (f as any).brandR; const legit = br !== undefined && pre.actionRound - br <= 3 && !(f as any).brandUsed; if (legit) (f as any).brandUsed = true; (f as any).undertow = [...((f as any).undertow ?? []), { r: pre.actionRound, dmg: pLoss, legit }]; }
      if (isBoss && actionId === J4.bw1Land) { const mr = (f as any).bw1MarkR; (f as any).floods = [...((f as any).floods ?? []), { r: pre.actionRound, dmg: pLoss, legit: mr !== undefined && pre.actionRound - mr <= 2 }]; }
      if (isBoss && actionId === J4.bw2Mark) deepSeen = true;
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
    boreDmgMedian: Math.round(median(fs.flatMap((f) => f.bore.map((x: any) => x.dmg))) ?? 0), borePerFight: r1(fs.reduce((s, f) => s + f.bore.length, 0) / fs.length),
    undertowDmgMedian: Math.round(median(fs.flatMap((f) => ((f as any).undertow ?? []).map((x: any) => x.dmg))) ?? 0),
    ownTurnHealPerFight: Math.round(fs.reduce((s, f) => s + ((f as any).leech ?? 0), 0) / fs.length),
    bw1DmgMedian: Math.round(median(fs.flatMap((f) => f.bw1.map((x: any) => x.dmg))) ?? 0), bw1PerFight: r1(fs.reduce((s, f) => s + f.bw1.length, 0) / fs.length),
    bossActsPerFight: Object.fromEntries(Object.entries(acts).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, r1(v / fs.length)])),
    playerAnswersPerFight: Object.fromEntries(Object.entries(ans).map(([k, v]) => [k, r1(v / fs.length)])),
    damageToPlayerPerFight: Object.fromEntries(Object.entries(src).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, Math.round(v / fs.length)])),
    misreadsPerFight: r1(fs.reduce((s, f) => s + f.misreads, 0) / fs.length),
    harassPerFight: r1(fs.reduce((s, f) => s + ((f as any).harass ?? 0), 0) / fs.length),
    undertow: (() => { const u = fs.flatMap((f) => (f as any).undertow ?? []); const lg = u.filter((x: any) => x.legit), st = u.filter((x: any) => !x.legit);
      return { perFight: r1(u.length / fs.length), legitPerFight: r1(lg.length / fs.length), strayPerFight: r1(st.length / fs.length), strayDmgMedian: Math.round(median(st.map((x: any) => x.dmg)) ?? 0), legitDmgMedian: Math.round(median(lg.map((x: any) => x.dmg)) ?? 0),
        brandNoUndertow: fs.filter((f) => (f as any).brandR !== undefined && !((f as any).undertow ?? []).some((x: any) => x.legit)).length }; })(),
    floods: (() => { const u = fs.flatMap((f) => (f as any).floods ?? []); return { perFight: r1(u.length / fs.length), strayPerFight: r1(u.filter((x: any) => !x.legit).length / fs.length), strayDmgMedian: Math.round(median(u.filter((x: any) => !x.legit).map((x: any) => x.dmg)) ?? 0) }; })(),
  };
};

const main = async () => {
  const P = v4(opt("params") ? loadJson(resolve(opt("params")!)) : {});
  if (opt("dg")) P.playerDg = Number(opt("dg"));
  const issues = isoValidate(P);
  console.log(issues.length ? `VALIDATION ISSUES:\n  ${issues.join("\n  ")}` : `valid (Isonade ${isoRules(P).length} rules, arm ${armRules().length})`);
  if (opt("write-spec")) {
    const spec = { _note: "Isonade v5 build spec. Generated by isonade_v5.ts --write-spec; offline engine-tested, NOT pushed. Ids are placeholders (iso-*).", params: P, ais: { [BOSS_ID]: isoAiRecord(P), [ARM_ID]: armAiRecord() }, newJutsu: buildRecords(P), markers: MK, validation: issues.length ? issues : "valid" };
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
  const out: any = { generatedBy: "isonade_v7.ts", harass: opt("harass") ?? "", params: P, dmgConfig: dmg.name, seeds, reads: {} };
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
