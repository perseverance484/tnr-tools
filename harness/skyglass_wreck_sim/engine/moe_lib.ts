/**
 * The Mother of Echoes (RUL-2026-11-01-093..096): records, AI rows, player models and the three-act fight runner.
 * Offline harness only: every record is built here on captured shape donors (kitlib) and validated by the live
 * JutsuValidator / AiRule / insertAiSchema; ids are placeholders (moe-*). Nothing here is pushed.
 *
 * Engine facts this file relies on are proven by engine/moe_probe.ts (REPORT_mother_of_echoes.md section 2):
 *   P1 Recast order: use_combo_action replays an authored sequence from the AI's own usedActions (repeats allowed);
 *   P2 Cradle: the feeler casts it on HIGHEST_MAX_HEALTH_ALLY (Sayo carries the highest max HP of her side);
 *   P3 healprevent vs sustain; P4 Hush pools (GROUND healprevent + drain / damage ground); P5 partner death via
 *   target_has_effect on the extreme-max-health ally carrying the survivor's own innate token.
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { nanoid } from "nanoid";
import { performAIaction } from "@/libs/combat/ai_v2";
import { availableUserActions, actionPointsAfterAction, performBattleAction, stillInBattle } from "@/libs/combat/actions";
import { applySageModeAfterRoundTransition } from "@/libs/combat/process";
import { alignBattle, getBattleGrid, getEffectiveMaxPool } from "@/libs/combat/util";
import { StatTypes } from "@/drizzle/constants";
import { AiRule } from "@/validators/ai";
import { insertAiSchema } from "@/validators/aiInput";
import { capturedJutsu, jutsu, tag, T } from "./kitlib";
import { aiRow, ALL, C, type Cell, color, dist, DONOR_SUMMON, IN, key, R, STAT_PER_MULT, t0 } from "./cclib";
import { enemyQueryUser, KITSUNE_SET, petFor, PLAYER_VARIANTS, playerQueryUser, type PlayerVariant } from "./model";
import { assembleFloor, mulberry32, seedEntropy, tickClock } from "./sim";
import { PATTERNS as LIBP } from "./library";

export const W = 12;
export const H = 10;
type XY = { longitude: number; latitude: number };
const xy = (c: Cell): XY => ({ longitude: c[0], latitude: c[1] });
const field = (cells: Cell[], selection: "ALL" | "EXCLUDE" | "RANDOM" = "ALL", origin = "BATTLEFIELD", randomCount = 1) =>
  ({ origin, selection, coordinates: cells.map(xy), randomCount });
const cellsWhere = (pred: (c: number, r: number) => boolean): Cell[] => {
  const out: Cell[] = [];
  for (let c = 0; c < W; c++) for (let r = 0; r < H; r++) if (pred(c, r)) out.push([c, r]);
  return out;
};
const span = (r: number, c0: number, c1: number): Cell[] => Array.from({ length: c1 - c0 + 1 }, (_, i) => [c0 + i, r] as Cell);

/* ------------------------------------------------------------------ patterns */
export const STARS: Cell[] = LIBP.stars.map((s) => [s.longitude, s.latitude] as Cell); // Where the Three Refused
const isStar = (c: number, r: number) => STARS.some((s) => s[0] === c && s[1] === r);
export const PAT = {
  /** Refraction: three lines, alternately from the west and east walls (9 hexes each). */
  refractA: [...span(1, 0, 8), ...span(4, 3, 11), ...span(7, 0, 8)],
  /** The point mirror of A (Facet's "mirrored" pattern); also Refraction's second set. */
  refractB: [...span(8, 3, 11), ...span(5, 0, 8), ...span(2, 3, 11)],
  /** Act II etchings (memory game). */
  etch: {
    A: cellsWhere((_c, r) => r <= 2), // the north band
    B: cellsWhere((_c, r) => r >= 7), // the south band
    C: cellsWhere((c) => c <= 3), // the west band
    D: cellsWhere((c, r) => c >= 4 && c <= 8 && r >= 3 && r <= 6), // the heart of the hall
    E: cellsWhere((c, r) => color([c, r]) === 0), // one hex in three, every way
  } as Record<string, Cell[]>,
  /** Glassfall: the three hex colours (every hex has neighbours of the other two). */
  glass: [0, 1, 2].map((k) => cellsWhere((c, r) => color([c, r]) === k)),
  flood: cellsWhere((c, r) => !isStar(c, r)),
  hushField: cellsWhere((c) => c <= 9), // where the Hush may seed (never under the Silence)
};
export const FAN_OFFSETS = LIBP.lines; // Shatterfall: the library's west fan, caster-anchored

/* ------------------------------------------------------------------ parameters */
export const MOE_DEFAULTS = {
  name: "v1",
  // Pools: maxHealth = 5050 x poolsMultiplier; insertAiSchema caps the multiplier at 12 at level 100 (65,535 pool ceiling).
  pools: { sayo1: 12, silence: 9, sayo2: 12, saint: 12 },
  statsMultiplier: 5.83, // JONIN cap reached; inert above
  /** +damage-given rows (each +100% max) per boss: "HIGH normal damage". */
  idg: { sayo1: 5.75, silence: 5.75, sayo2: 5.75, saint: 6, summons: 4.75 },
  /** Innate decreasedamagetaken % on top of AI Heavy Armor (tankiness without HP above the stored cap). */
  dr: { sayo1: 30, silence: 50, sayo2: 30, saint: 40 },
  pw: {
    lancet: 70, thorns: 80, refract: 300, facet: 340, likenessHit: 90, stillness: 110, grasp: 30, graspDrain: 4,
    hushDrain: 4, hushDmg: 25, detonate: 360, quiet: 60, quietIdt: 15, shatter: 300, flood: 420, glass: 260, recastIII: 380,
    enrage: 600, porter: 80, hana: 8, tomo: 60, cradleDR: 90,
  },
  hushCount: [4, 8, 12], // pools per Hush I / II / III
  hushUnbridledCount: 3, // pools per Unbridled Hush (every turn)
  hushRounds: 8,
  hushBands: [8, 16], // Hush II from round > 8, III from round > 16
  feeler: { hp: 2500, power: 40, rounds: 8, listeningCd: 4 },
  likeness: { hp: 6000, power: 80, rounds: 3 },
  worn: { hp: 5000, power: 60, rounds: 8 },
  enrage: { act1: 25, act3: 30 },
  refractCd: 4,
  quietRounds: 6,
  starHush: { cd: 3, rounds: 3 },
  floodCd: 3,
  m2HealBlockRounds: 20,
  sayo2Stunprevent: true,
};
export type MoeParams = typeof MOE_DEFAULTS;
export const moeParams = (over: any = {}): MoeParams => {
  const P = structuredClone(MOE_DEFAULTS) as any;
  const merge = (a: any, b: any) => { for (const [k, v] of Object.entries(b ?? {})) a[k] = v && typeof v === "object" && !Array.isArray(v) && a[k] && typeof a[k] === "object" ? merge(a[k], v) : v; return a; };
  return merge(P, over);
};

/* ------------------------------------------------------------------ ids */
export const AI = {
  sayo1: "moe-ai-sayo", silence: "moe-ai-silence", feeler: "moe-ai-feeler", likeness: "moe-ai-likeness",
  sayo2: "moe-ai-sayo-stilling", porter: "moe-ai-worn-porter", hana: "moe-ai-worn-hana", tomo: "moe-ai-worn-tomo",
  saint: "moe-ai-saint",
};
export const JID = {
  lancet: "moe-glass-lancet", refractA: "moe-refraction", refractB: "moe-refraction-ii", blastA: "moe-refraction-blast",
  blastB: "moe-refraction-blast-ii", facet: "moe-facet", facetBlast: "moe-facet-blast", lucidBlast: "moe-lucid-refraction",
  likeness: "moe-your-likeness", likenessStrike: "moe-likeness-strike", likenessCopy: "moe-likeness-copy",
  hush: ["moe-hush", "moe-hush-ii", "moe-hush-iii"], hushUnbridled: "moe-hush-unbridled", listening: "moe-listening",
  listeningUnbridled: "moe-listening-unbridled", stillness: "moe-stillness", cradle: "moe-cradle", grasp: "moe-feeler-grasp",
  enrage: "moe-the-glass-remembers",
  etch: Object.fromEntries("ABCDE".split("").map((k) => [k, `moe-etching-${k.toLowerCase()}`])) as Record<string, string>,
  det: Object.fromEntries("ABCDE".split("").map((k) => [k, `moe-recast-${k.toLowerCase()}`])) as Record<string, string>,
  quietFall: "moe-the-glass-falls-quiet", thorns: "moe-glass-thorns",
  porter: "moe-worn-cleave", hana: "moe-worn-mending", tomo: "moe-worn-tether",
  summonPorter: "moe-raise-gate-porter", summonHana: "moe-raise-sister-hana", summonTomo: "moe-raise-cadet-tomo",
  quiet: "moe-the-quiet", shatterMark: "moe-shatterfall", shatterBlast: "moe-shatterfall-blast",
  floodMark: "moe-every-name-in-the-glass", floodBlast: "moe-every-name-blast", m2Entry: "moe-no-one-is-mended",
  pull: "moe-breathless-pull", starHush: "moe-hush-on-the-refused", longHush: "moe-the-long-hush",
  glass: ["moe-glassfall-a", "moe-glassfall-b", "moe-glassfall-c"], glassFirstB: "moe-glassfall-b-first", glassRecast: "moe-glassfall-recast",
};

/** Marker / token types (harmless on these AIs; distinct per record). */
export const MK = {
  // Act I
  refractA: "increaserange", refractB: "fleeprevent", facet: "robprevent",
  sayoToken: "onehitkillprevent", silenceToken: "sealprevent",
  // Act II
  done: "fleeprevent", counter: "increasecooldown", // counter: power 1 per cycle, no probability roll (prevent types roll power/100)
  // Act III
  shatter: "increaserange", flood: "fleeprevent", gA: "robprevent", gB: "onehitkillprevent", gC: "disarm", gCs: "elementalseal",
  firstPass: "decreasecooldown",
};
const marker = (type: string, rounds = 1, power?: number) => tag(type, {
  power: power ?? (["increasecooldown", "decreasecooldown", "increaserange"].includes(type) ? 1 : 100), rounds, target: "SELF",
  ...(["increasecooldown", "decreasecooldown", "increaserange"].includes(type) ? { actionsAffected: [], calculation: "static" } : {}),
});
const token = (type: string) => marker(type, 100);
const vis = (anim: string, rounds: number) => T.visual(anim, rounds);
const ALLSTATS = ["None", "Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"];
const ALLGEN = ["Highest", "Strength", "Intelligence", "Willpower", "Speed"];
const weaknessSelf = (mult: number, anim = "moe_guard_open") =>
  tag("weakness", { target: "SELF", rounds: 1, dmgModifier: mult, statTypes: ALLSTATS, generalTypes: ALLGEN, power: 100, staticAnimation: anim });
const heavy = (power: number, anim = "dt_heavy") => T.damage(power, { appearAnimation: anim });

/* ------------------------------------------------------------------ records */
export const buildRecords = (P: MoeParams) => {
  const J: Record<string, any> = {};
  const add = (id: string, f: Parameters<typeof jutsu>[1]) => { J[id] = jutsu(id, f); return id; };
  const p = P.pw;
  /* ---- shared ---- */
  add(JID.lancet, { name: "Glass Lancet", description: "A needle of skyglass, thrown hard.", battleDescription: "%user flicks a lancet of glass at %target.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 1, actionCostPerc: 60, effects: [heavy(p.lancet, "moe_lancet")] });
  add(JID.enrage, { name: "The Glass Remembers", description: "Enrage: every surface of the hall answers at once.", battleDescription: "Every pane in the hall turns toward you at once.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: field(cellsWhere(() => true)), effects: [heavy(p.enrage, "moe_enrage")] });
  /* ---- Act I: Sayo ---- */
  const mark = (id: string, name: string, cells: Cell[], mk: string, line: string, cost = 40, cd = P.refractCd) =>
    add(id, { name, description: "Refraction: lines of light from the walls; they shatter on her next turn.", battleDescription: line, target: "GROUND", method: "COORDINATES", range: 0, cooldown: cd, actionCostPerc: cost, coordinateTargeting: field(cells), effects: [vis("tg_heavy", 1), marker(mk)] });
  mark(JID.refractA, "Refraction", PAT.refractA, MK.refractA, "%user draws three lines of light from the walls.");
  mark(JID.refractB, "Refraction", PAT.refractB, MK.refractB, "%user draws three lines of light from the walls.");
  add(JID.facet, { name: "Facet", description: "Below 60%: her pattern also appears, mirrored.", battleDescription: "The lines split. Their mirror image glows on the far side of the hall.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 60, coordinateTargeting: field([...PAT.refractA, ...PAT.refractB]), effects: [vis("tg_heavy", 1), marker(MK.facet)] });
  const blast = (id: string, name: string, cells: Cell[], power: number, line: string, extra: any[] = []) =>
    add(id, { name, description: "The marked lines shatter.", battleDescription: line, target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: field(cells), effects: [heavy(power, "moe_refraction"), ...extra] });
  blast(JID.blastA, "Refraction", PAT.refractA, p.refract, "The lines shatter.");
  blast(JID.blastB, "Refraction", PAT.refractB, p.refract, "The lines shatter.");
  blast(JID.facetBlast, "Facet", [...PAT.refractA, ...PAT.refractB], p.facet, "Both images shatter at once.");
  // Lucid (the Silence fell first): the blast also draws the second set, so Refraction fires twice.
  add(JID.lucidBlast, { name: "Lucid Refraction", description: "Lucid: the lines shatter and are drawn again at once.", battleDescription: "\"I can hear myself again.\" The lines shatter, and new ones are already drawn.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: field(PAT.refractA),
    effects: [heavy(p.refract, "moe_refraction"), T.visual("tg_heavy", 1, { target: "COORDINATES", coordinateTargeting: field(PAT.refractB) }), marker(MK.refractB)] });
  add(JID.likeness, { name: "Your Likeness", description: "Below 40%: she casts your impression from the glass for three rounds.", battleDescription: "\"Hold still. There. That is you.\" Your likeness steps out of the glass.", target: "EMPTY_GROUND", method: "SINGLE", range: 5, cooldown: 99, actionCostPerc: 60, donor: IN.donors.summon,
    effects: [tag("summon", { aiId: AI.likeness, aiHp: P.likeness.hp, power: P.likeness.power, rounds: P.likeness.rounds, appearAnimation: "moe_likeness" })] });
  add(JID.likenessStrike, { name: "Your Own Strike", description: "Your likeness strikes with your habits.", battleDescription: "%user strikes the way you would.", target: "OTHER_USER", method: "SINGLE", range: 4, cooldown: 0, actionCostPerc: 60, effects: [heavy(p.likenessHit)] });
  add(JID.likenessCopy, { name: "A Good Copy", description: "Your likeness takes your strengths for itself.", battleDescription: "%user wears your strength like its own.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 99, actionCostPerc: 40, effects: [tag("copy", { power: 100, rounds: 3, calculation: "percentage" })] });
  /* ---- Act I: the Silence ---- */
  const hushRec = (id: string, name: string, n: number, line: string, withDrain: boolean, cd: number) =>
    add(id, { name, description: "The Hush: stilled pools seep up through the floor; standing in one drains you and nothing heals you.", battleDescription: line, target: "GROUND", method: "COORDINATES", range: 0, cooldown: cd, actionCostPerc: 40, coordinateTargeting: field(PAT.hushField, "RANDOM", "BATTLEFIELD", n),
      effects: [
        tag("healprevent", { power: 100, rounds: P.hushRounds, friendlyFire: "ENEMIES" }),
        withDrain ? tag("drain", { power: p.hushDrain, rounds: P.hushRounds, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"] })
          : T.pool(p.hushDmg, P.hushRounds, { appearAnimation: "moe_hush" }),
        vis("tg_linger", P.hushRounds),
      ] });
  // drain is a shared-cooldown tag: the three Hush records lock each other for 3 rounds (every third turn).
  hushRec(JID.hush[0], "The Hush", P.hushCount[0], "The floor goes quiet in patches.", true, 3);
  hushRec(JID.hush[1], "The Hush", P.hushCount[1], "The quiet spreads.", true, 3);
  hushRec(JID.hush[2], "The Hush", P.hushCount[2], "Most of the floor has stopped making any sound at all.", true, 3);
  hushRec(JID.hushUnbridled, "The Hush, Unbridled", P.hushUnbridledCount, "Unbridled, the quiet pours up out of the floor.", false, 1);
  const listen = (id: string, name: string, cd: number, line: string) =>
    add(id, { name, description: "The Listening: a feeler of the deep rises and listens for movement.", battleDescription: line, target: "EMPTY_GROUND", method: "SINGLE", range: 5, cooldown: cd, actionCostPerc: 40, donor: IN.donors.summon,
      effects: [tag("summon", { aiId: AI.feeler, aiHp: P.feeler.hp, power: P.feeler.power, rounds: P.feeler.rounds, appearAnimation: "moe_feeler" })] });
  listen(JID.listening, "The Listening", P.feeler.listeningCd, "Something under the floor turns toward the sound of you.");
  listen(JID.listeningUnbridled, "The Listening, Unbridled", 1, "It does not wait any more. Another feeler rises.");
  add(JID.stillness, { name: "Stillness", description: "A crushing weight on the closest thing that moves; it cannot move for a round.", battleDescription: "The deep presses down on %target. \"Be still.\"", target: "OTHER_USER", method: "SINGLE", range: 3, cooldown: 2, actionCostPerc: 60, effects: [heavy(p.stillness, "moe_stillness"), T.root(1)] });
  /* ---- the feeler ---- */
  add(JID.cradle, { name: "Cradle", description: "While a feeler lives, the Silence holds Sayo: 90% less damage taken, and the hold cannot be cleared.", battleDescription: "The Silence cradles %target. Blows slide off the glass.", target: "ALLY", method: "SINGLE", range: 5, cooldown: 1, actionCostPerc: 40, donor: "xs-8r_KRJS8QQMpBDyhUv",
    effects: [T.pct("decreasedamagetaken", p.cradleDR, 1, { target: "INHERIT", friendlyFire: "FRIENDLY", staticAnimation: "moe_cradle" }), tag("clearprevent", { power: 100, rounds: 1, target: "INHERIT", friendlyFire: "FRIENDLY" })] });
  add(JID.grasp, { name: "Grasp", description: "The feeler takes hold of whatever is nearest: rooted, and drained.", battleDescription: "%user closes around %target.", target: "OTHER_USER", method: "SINGLE", range: 2, cooldown: 0, actionCostPerc: 60,
    effects: [heavy(p.grasp), T.root(1), tag("drain", { power: p.graspDrain, rounds: 2, calculation: "percentage", poolsAffected: ["Health"] })] });
  /* ---- Act II: Sayo (the Stilling) ---- */
  for (const k of Object.keys(PAT.etch)) {
    add(JID.etch[k]!, { name: "Etching", description: "She etches a pattern into the glass. It will remember.", battleDescription: "%user traces a pattern into the glass. It glows, then fades.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 40, coordinateTargeting: field(PAT.etch[k]!), effects: [vis("tg_etch", 1)] });
    add(JID.det[k]!, { name: "Recast", description: "The glass remembers an etching and detonates it, unmarked. While she recasts, her guard is open (x3 damage taken).", battleDescription: "The glass remembers.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: field(PAT.etch[k]!), effects: [heavy(p.detonate, "moe_recast"), weaknessSelf(3)] });
  }
  // Etching turns: Etching (40 AP) + Glass Thorns (60 AP) = exactly 100 AP. Any leftover AP ends in the engine's
  // appended end turn, whose "wait" enters usedActions and breaks the combo (moe_probe P1b, first build).
  add(JID.thorns, { name: "Glass Thorns", description: "Thorns of glass burst from the floor around her while she etches.", battleDescription: "Glass thorns burst up around %user.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 60, coordinateTargeting: { origin: "CASTER", selection: "ALL", coordinates: LIBP.bindingRing, randomCount: 1 }, effects: [heavy(p.thorns, "moe_thorns")] });
  add(JID.quietFall, { name: "The Glass Falls Quiet", description: "The cycle ends; a Worn afterimage is raised in the lull.", battleDescription: "The glass falls quiet. Something worn steps out of it.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 20, coordinateTargeting: field(STARS), effects: [vis("moe_lull", 1), marker(MK.done, 2), marker(MK.counter, 99, 1)] });
  const raise = (id: string, name: string, ai: string, line: string) =>
    add(id, { name, description: `Raises one of the Worn: ${name.replace("Raise ", "")}.`, battleDescription: line, target: "EMPTY_GROUND", method: "SINGLE", range: 4, cooldown: 0, actionCostPerc: 60, donor: IN.donors.summon,
      effects: [tag("summon", { aiId: ai, aiHp: P.worn.hp, power: P.worn.power, rounds: P.worn.rounds, appearAnimation: "moe_worn" })] });
  raise(JID.summonPorter, "Raise the Gate Porter", AI.porter, "A gate porter steps out of the glass, still holding the door.");
  raise(JID.summonHana, "Raise Sister Hana", AI.hana, "Sister Hana steps out of the glass, hands already busy.");
  raise(JID.summonTomo, "Raise Cadet Tomo", AI.tomo, "Cadet Tomo steps out of the glass, rope in hand.");
  add(JID.porter, { name: "Doorward Sweep", description: "The porter sweeps the threshold: damage and a shove.", battleDescription: "%user sweeps the threshold clear.", target: "OTHER_USER", method: "SINGLE", range: 1, cooldown: 1, actionCostPerc: 60, effects: [heavy(p.porter), T.push(2)] });
  add(JID.hana, { name: "Worn Mending", description: "Sister Hana tends Sayo, as she tended everyone.", battleDescription: "%user tends to %target.", target: "ALLY", method: "SINGLE", range: 5, cooldown: 0, actionCostPerc: 60, donor: "xs-8r_KRJS8QQMpBDyhUv", effects: [T.heal(p.hana, { friendlyFire: "FRIENDLY" })] });
  add(JID.tomo, { name: "Cadet's Tether", description: "Tomo throws a line and hauls: pulled 3 hexes.", battleDescription: "%user hauls %target in.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 1, actionCostPerc: 60, effects: [heavy(p.tomo), T.pull(3)] });
  /* ---- Act III: Sayo, Saint of Stillness ---- */
  add(JID.quiet, { name: "The Quiet", description: "She channels: you take more damage and heal less, stacking; while she channels it cannot be cleansed.", battleDescription: "%user closes her eyes. The hall goes very quiet.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 2, actionCostPerc: 60,
    effects: [heavy(p.quiet, "moe_quiet"), T.pct("increasedamagetaken", p.quietIdt, P.quietRounds), tag("decreaseheal", { power: p.quietIdt, rounds: P.quietRounds, calculation: "percentage" }), tag("cleanseprevent", { power: 100, rounds: 1 })] });
  add(JID.shatterMark, { name: "Shatterfall", description: "A fan of cracks runs out from her; it falls on her next turn.", battleDescription: "Cracks fan out from %user's feet.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 3, actionCostPerc: 40, coordinateTargeting: { origin: "CASTER", selection: "ALL", coordinates: FAN_OFFSETS, randomCount: 1 }, effects: [vis("tg_heavy", 1), marker(MK.shatter)] });
  add(JID.shatterBlast, { name: "Shatterfall", description: "The fan falls.", battleDescription: "The fan of glass falls.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: { origin: "CASTER", selection: "ALL", coordinates: FAN_OFFSETS, randomCount: 1 }, effects: [heavy(p.shatter, "moe_shatterfall")] });
  add(JID.floodMark, { name: "Every Name in the Glass", description: "Every stilled name rises to the floor; only where the three refused stays dry.", battleDescription: "Every name in the glass rises at once. Three places stay dry: where the three refused.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: P.floodCd, actionCostPerc: 40, coordinateTargeting: field(PAT.flood),
    effects: [vis("tg_heavy", 1), T.visual("tg_safe", 1, { target: "COORDINATES", coordinateTargeting: field(STARS) }), marker(MK.flood)] });
  add(JID.floodBlast, { name: "Every Name in the Glass", description: "The flood of names.", battleDescription: "The names flood the hall.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: field(PAT.flood), effects: [heavy(p.flood, "moe_flood")] });
  add(JID.m2Entry, { name: "No One Is Mended", description: "For the whole of Every Name in the Glass, nothing heals you.", battleDescription: "\"Nothing mends here. Nothing needs to.\"", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 99, actionCostPerc: 20,
    effects: [tag("healprevent", { power: 100, rounds: P.m2HealBlockRounds })] });
  add(JID.pull, { name: "Breathless Pull", description: "She draws you in, three hexes, the turn before the flood.", battleDescription: "%user breathes in, and %target is drawn toward her.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 0, actionCostPerc: 60, effects: [T.pull(3)] });
  add(JID.starHush, { name: "The Hush", description: "The Hush seeps into one of the three dry places.", battleDescription: "The quiet seeps into one of the dry places.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: P.starHush.cd, actionCostPerc: 40, coordinateTargeting: field(STARS, "RANDOM", "BATTLEFIELD", 1),
    effects: [tag("healprevent", { power: 100, rounds: P.starHush.rounds, friendlyFire: "ENEMIES" }), tag("drain", { power: p.hushDrain, rounds: P.starHush.rounds, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"] }), vis("tg_linger", P.starHush.rounds)] });
  add(JID.longHush, { name: "The Long Hush", description: "Below 25%: she cannot fall for 6 rounds; the glass begins to fall.", battleDescription: "\"Not yet. You are almost a good impression.\" The ceiling begins to fall.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 99, actionCostPerc: 40, coordinateTargeting: field(PAT.glass[0]!),
    effects: [tag("finalstand", { power: 100, rounds: 6, target: "SELF" }), vis("tg_heavy", 1), marker(MK.gA), marker(MK.firstPass, 3)] });
  const gfMk = [MK.gA, MK.gB, MK.gC];
  const gf = (id: string, k: number, nextMk: string, extra: Cell[] = [], line = "Glass falls.") =>
    add(id, { name: "Glassfall", description: "The marked third of the hall is crushed; the next third is marked.", battleDescription: line, target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: field([...PAT.glass[k]!, ...extra.filter((c) => !PAT.glass[k]!.some((g) => key(g) === key(c)))]),
      effects: [heavy(extra.length ? Math.max(p.glass, p.recastIII) : p.glass, "moe_glassfall"), T.visual("tg_heavy", 1, { target: "COORDINATES", coordinateTargeting: field(PAT.glass[(k + 1) % 3]!) }), marker(nextMk)] });
  gf(JID.glass[0]!, 0, gfMk[1]!);
  gf(JID.glass[1]!, 1, gfMk[2]!);
  gf(JID.glass[2]!, 2, gfMk[0]!);
  gf(JID.glassFirstB, 1, MK.gCs);
  // Round 4 of the Long Hush: the C third falls and, unmarked, one Act II etching (the heart of the hall) is recast.
  gf(JID.glassRecast, 2, gfMk[0]!, PAT.etch.D!, "Glass falls, and the glass remembers one more etching.");
  return J;
};

/* ------------------------------------------------------------------ rules */
const tHas = (target: string, effectType: string) => ({ type: "target_has_effect", effectType, threshold: 1, target, description: "Target has effect" });
export const COND = {
  sayoAlive: tHas("HIGHEST_MAX_HEALTH_ALLY", MK.sayoToken), // feeler: Sayo is its side's highest max HP
  unbridled: tHas("HIGHEST_MAX_HEALTH_ALLY", MK.silenceToken), // Silence: Sayo gone, so the highest is the Silence itself
  lucid: tHas("LOWEST_MAX_HEALTH_ALLY", MK.sayoToken), // Sayo: Silence gone (and no feeler), so the lowest is Sayo herself
  rg: (v: number) => ({ type: "round_greater_than", value: v, description: "Current round is higher than specified value" }),
  combo: (ids: string[], target = "SELF") => ({ conditions: [] as any[], action: { type: "use_combo_action", comboIds: ids, target, description: "Use combo" } }),
};
const PL = "CLOSEST_OPPONENT";
const basic = (conds: any[] = []) => R.jutsu("basicAttack", PL, conds);
const withCond = (r: any, conds: any[]) => ({ ...r, conditions: [...conds, ...r.conditions] });

export const sayo1Rules = (P: MoeParams) => [
  R.jutsu(JID.enrage, "SELF", [COND.rg(P.enrage.act1)]),
  R.jutsu(JID.facetBlast, "SELF", [C.has(MK.facet)]),
  R.jutsu(JID.lucidBlast, "SELF", [COND.lucid, C.has(MK.refractA)]),
  R.jutsu(JID.blastA, "SELF", [C.has(MK.refractA)]),
  R.jutsu(JID.blastB, "SELF", [C.has(MK.refractB)]),
  R.jutsu(JID.likeness, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [C.hb(40), C.noSummon()]),
  // After a mark (its marker is on her the same turn): Facet below 60%, else a lancet, then end turn (never two marks).
  R.jutsu(JID.facet, "SELF", [C.hb(60), C.has(MK.refractA)]),
  R.jutsu(JID.facet, "SELF", [C.hb(60), C.has(MK.refractB)]),
  R.jutsu(JID.lancet, PL, [C.has(MK.refractA), C.near(5)]),
  R.jutsu(JID.lancet, PL, [C.has(MK.refractB), C.near(5)]),
  R.end([C.has(MK.refractA)]),
  R.end([C.has(MK.refractB)]),
  R.jutsu(JID.refractA, "SELF", []),
  R.jutsu(JID.refractB, "SELF", []),
  R.jutsu(JID.lancet, PL, [C.near(5)]),
  { conditions: [C.far(6)], action: { type: "move_towards_opponent", target: PL, description: "Keep 5 hexes" } },
  basic([C.near(1)]),
  R.end(),
];
export const silenceRules = (P: MoeParams) => [
  R.jutsu(JID.enrage, "SELF", [COND.rg(P.enrage.act1)]),
  // Unbridled (Sayo fell first): a feeler every turn one is missing, the Hush every turn instead of every third.
  R.jutsu(JID.listeningUnbridled, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [COND.unbridled, C.noSummon()]),
  R.jutsu(JID.hushUnbridled, "SELF", [COND.unbridled]),
  R.jutsu(JID.stillness, PL, [COND.unbridled, C.near(3)]),
  R.end([COND.unbridled]),
  R.jutsu(JID.hush[2]!, "SELF", [COND.rg(P.hushBands[1]!)]),
  R.jutsu(JID.hush[1]!, "SELF", [COND.rg(P.hushBands[0]!)]),
  R.jutsu(JID.hush[0]!, "SELF", []),
  R.jutsu(JID.listening, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [C.noSummon()]),
  R.jutsu(JID.stillness, PL, [C.near(3)]),
  basic([C.near(1)]),
  R.end(),
];
export const feelerRules = () => [
  R.jutsu(JID.cradle, "HIGHEST_MAX_HEALTH_ALLY", [COND.sayoAlive]),
  R.jutsu(JID.grasp, PL, [C.near(2)]),
  R.end(),
];
export const likenessRules = () => [R.jutsu(JID.likenessCopy, PL, [C.near(5)]), R.jutsu(JID.likenessStrike, PL, [C.near(4)]), { conditions: [], action: { type: "move_towards_opponent", target: PL, description: "Close in" } }];

/** Act II etching cycles (3 / 4 / 5 / 5; cycles 3 and 4 repeat an etching out of order). */
export const CYCLES: string[][] = [["A", "B", "C"], ["D", "A", "C", "B"], ["C", "A", "E", "A", "B"], ["E", "B", "D", "B", "C"]];
export const cycleCombo = (seq: string[]) => [...seq.flatMap((k) => [JID.etch[k]!, JID.thorns]), ...seq.map((k) => JID.det[k]!), JID.quietFall];
const cnt = (n: number) => C.has(MK.counter, n);
export const sayo2Rules = (_P: MoeParams) => [
  R.jutsu(JID.enrage, "SELF", [cnt(4)]),
  R.jutsu(JID.summonTomo, "EMPTY_GROUND_CLOSEST_TO_SELF", [C.has(MK.done), cnt(3), C.noSummon()]),
  R.jutsu(JID.summonHana, "EMPTY_GROUND_CLOSEST_TO_SELF", [C.has(MK.done), cnt(2), C.noSummon()]),
  R.jutsu(JID.summonPorter, "EMPTY_GROUND_CLOSEST_TO_SELF", [C.has(MK.done), C.noSummon()]),
  R.jutsu(JID.lancet, PL, [C.has(MK.done), C.near(5)]),
  R.end([C.has(MK.done)]),
  withCond(COND.combo(cycleCombo(CYCLES[3]!)), [cnt(3)]),
  withCond(COND.combo(cycleCombo(CYCLES[2]!)), [cnt(2)]),
  withCond(COND.combo(cycleCombo(CYCLES[1]!)), [cnt(1)]),
  COND.combo(cycleCombo(CYCLES[0]!)),
  R.end(),
];
export const wornRules = (jid: string, target = PL) => [
  R.jutsu(jid, target, target === PL ? [C.near(jid === JID.porter ? 1 : 5)] : [COND.sayoAlive]),
  ...(target === PL ? [{ conditions: [], action: { type: "move_towards_opponent", target: PL, description: "Close in" } }] : []),
  R.end(),
];
export const saintRules = (P: MoeParams) => [
  R.jutsu(JID.enrage, "SELF", [COND.rg(P.enrage.act3)]),
  R.jutsu(JID.longHush, "SELF", [C.hb(25)]),
  R.jutsu(JID.glassRecast, "SELF", [C.has(MK.gCs)]),
  R.jutsu(JID.glassFirstB, "SELF", [C.has(MK.firstPass), C.has(MK.gB)]),
  R.jutsu(JID.glass[0]!, "SELF", [C.has(MK.gA)]),
  R.jutsu(JID.glass[1]!, "SELF", [C.has(MK.gB)]),
  R.jutsu(JID.glass[2]!, "SELF", [C.has(MK.gC)]),
  R.end([C.hb(25)]),
  R.jutsu(JID.floodBlast, "SELF", [C.has(MK.flood)]),
  R.jutsu(JID.m2Entry, PL, [C.hb(60), C.near(5)]),
  R.jutsu(JID.floodMark, "SELF", [C.hb(60)]),
  R.jutsu(JID.pull, PL, [C.has(MK.flood), C.near(5)]),
  R.jutsu(JID.starHush, "SELF", [C.hb(60)]),
  R.jutsu(JID.shatterBlast, "SELF", [C.has(MK.shatter)]),
  R.jutsu(JID.quiet, PL, [C.near(5)]),
  R.jutsu(JID.shatterMark, "SELF", []),
  R.jutsu(JID.lancet, PL, [C.near(5)]),
  // Shatterfall is caster-anchored: never move between its mark and its fall.
  R.end([C.has(MK.shatter)]),
  { conditions: [C.far(5)], action: { type: "move_towards_opponent", target: PL, description: "Close in" } },
  R.end(),
];

/* ------------------------------------------------------------------ AI rows */
const capturedItem = (id: string, files: string[]) => {
  let best: any = null;
  const walk = (x: any) => {
    if (Array.isArray(x)) x.forEach(walk);
    else if (x && typeof x === "object") {
      if (x.id === id && "itemType" in x && Array.isArray(x.effects) && (!best || (x.updatedAt ?? "") > (best.updatedAt ?? ""))) best = x;
      Object.values(x).forEach(walk);
    }
  };
  for (const f of files) walk(JSON.parse(readFileSync(join(process.env.TNR_REPO!, f), "utf8")));
  if (!best) throw new Error(`item ${id} not captured`);
  return structuredClone(best);
};
export const HEAVY_ARMOR_ID = "h-V9uiuxbL7lAWkO6nZWt";
export const HEAVY_ARMOR_SRC = "harvests/inbox/tnr_results_1792552825510.json";
export const HEAVY_ARMOR = capturedItem(HEAVY_ARMOR_ID, [HEAVY_ARMOR_SRC]);
const donorRow = enemyQueryUser(t0.enemies["texZaFi42S3EvJZBwQ8cd"]!);
const armorDonor = donorRow.items.find((ui: any) => ui.item?.itemType === "ARMOR");
const heavyArmorRow = (userId: string) => ({ ...structuredClone(armorDonor), id: `moe-ha-${userId}`, userId, itemId: HEAVY_ARMOR_ID, equipped: HEAVY_ARMOR.slot, quantity: 1, isInAuction: false, durability: 100, imbuements: [], item: structuredClone(HEAVY_ARMOR) });

const idgTags = (rows: number) => [
  ...Array.from({ length: Math.floor(rows) }, () => tag("increasedamagegiven", { power: 100, rounds: 100, calculation: "percentage", description: "Increased damage given" })),
  ...(rows % 1 ? [tag("increasedamagegiven", { power: Math.round((rows % 1) * 100), rounds: 100, calculation: "percentage", description: "Increased damage given" })] : []),
];
const drTag = (pct: number) => (pct > 0 ? [tag("decreasedamagetaken", { power: pct, rounds: 100, calculation: "percentage", description: "Decreased damage taken" })] : []);

export type AiRec = { id: string; username: string; poolsMultiplier: number; jutsus: string[]; effects: any[]; rules: any[]; heavyArmor: boolean; summon?: boolean };
export const aiRecords = (P: MoeParams): AiRec[] => {
  const boss = (id: string, username: string, pools: number, idg: number, dr: number, jutsus: string[], rules: any[], extra: any[] = []) =>
    ({ id, username, poolsMultiplier: pools, jutsus, effects: [...idgTags(idg), ...drTag(dr), ...extra], rules, heavyArmor: true });
  const summon = (id: string, username: string, jutsus: string[], rules: any[], effects: any[] = []) => ({ id, username, poolsMultiplier: 1, jutsus, effects: [...idgTags(P.idg.summons), ...effects], rules, heavyArmor: false, summon: true });
  const etchIds = Object.values(JID.etch), detIds = Object.values(JID.det);
  return [
    boss(AI.sayo1, "Sayo, Mother of Echoes", P.pools.sayo1, P.idg.sayo1, P.dr.sayo1,
      [JID.lancet, JID.enrage, JID.refractA, JID.refractB, JID.blastA, JID.blastB, JID.facet, JID.facetBlast, JID.lucidBlast, JID.likeness], sayo1Rules(P), [token(MK.sayoToken)]),
    boss(AI.silence, "The Silence", P.pools.silence, P.idg.silence, P.dr.silence,
      [JID.enrage, ...JID.hush, JID.hushUnbridled, JID.listening, JID.listeningUnbridled, JID.stillness], silenceRules(P), [token(MK.silenceToken)]),
    summon(AI.feeler, "A Feeler of the Deep", [JID.cradle, JID.grasp], feelerRules()),
    summon(AI.likeness, "Your Likeness", [JID.likenessStrike, JID.likenessCopy], likenessRules()),
    boss(AI.sayo2, "Sayo, Mother of Echoes", P.pools.sayo2, P.idg.sayo2, P.dr.sayo2,
      [JID.lancet, JID.enrage, ...etchIds, ...detIds, JID.thorns, JID.quietFall, JID.summonPorter, JID.summonHana, JID.summonTomo], sayo2Rules(P),
      [...(P.sayo2Stunprevent ? [tag("stunprevent", { power: 100, rounds: 100 })] : []), token(MK.sayoToken)]),
    summon(AI.porter, "The Gate Porter (Worn)", [JID.porter], wornRules(JID.porter)),
    summon(AI.hana, "Sister Hana (Worn)", [JID.hana], wornRules(JID.hana, "HIGHEST_MAX_HEALTH_ALLY")),
    summon(AI.tomo, "Cadet Tomo (Worn)", [JID.tomo], wornRules(JID.tomo)),
    boss(AI.saint, "Sayo, Saint of Stillness", P.pools.saint, P.idg.saint, P.dr.saint,
      [JID.lancet, JID.enrage, JID.quiet, JID.shatterMark, JID.shatterBlast, JID.floodMark, JID.floodBlast, JID.m2Entry, JID.pull, JID.starHush, JID.longHush, ...JID.glass, JID.glassFirstB, JID.glassRecast], saintRules(P)),
  ];
};
export const rowOf = (a: AiRec, recs: Record<string, any>, P: MoeParams) => {
  const d = { ...IN.boss.data, username: a.username, poolsMultiplier: a.poolsMultiplier, statsMultiplier: P.statsMultiplier, jutsus: a.jutsus, includeDefaultRules: false };
  const row: any = aiRow(a.id, d, Math.round(STAT_PER_MULT * P.statsMultiplier * 100) / 100, recs, a.rules, a.effects, []);
  if (a.heavyArmor) row.items = [heavyArmorRow(a.id)];
  if (a.summon) row.isSummon = false; // templates are plain AI rows; the engine marks the summoned unit
  return row;
};
/** Static validation of every record and rule (live JutsuValidator ran in kitlib.jutsu; here AiRule + insertAiSchema). */
export const validateAll = (P: MoeParams) => {
  const issues: string[] = [];
  for (const a of aiRecords(P)) {
    for (const r of a.rules) {
      const res = AiRule.safeParse(r);
      if (!res.success) issues.push(`${a.username} rule ${JSON.stringify(r.action).slice(0, 80)}: ${res.error.issues.map((i: any) => i.message).join("; ")}`);
    }
    if (a.rules.length > 20) issues.push(`${a.username}: ${a.rules.length} rules (cap 20)`);
    const last = a.rules[a.rules.length - 1];
    if (last.conditions.length) issues.push(`${a.username}: last rule is conditional (law 41)`);
    const d = { ...IN.boss.data, username: a.username, poolsMultiplier: a.poolsMultiplier, statsMultiplier: P.statsMultiplier, effects: a.effects, includeDefaultRules: false };
    const { rules: _r, jutsus: _j, items: _i, ...fields } = d;
    const res = insertAiSchema.safeParse({ ...fields, userId: a.id, jutsus: a.jutsus, items: a.heavyArmor ? [{ ids: [HEAVY_ARMOR_ID], number: 0 }] : [], isAi: true });
    if (!res.success) issues.push(`${a.username} record: ${res.error.issues.map((i: any) => `${i.path.join(".")}: ${i.message}`).join("; ")}`);
  }
  return issues;
};

/* ------------------------------------------------------------------ players */
/** The geared level-100 model's kit (all captured player records; 9 = the JONIN equip limit). */
let GEAR_OVERRIDE: any = null;
export const setGearOverride = (g: any) => { GEAR_OVERRIDE = g; };
export const ELITE_KIT = [
  "e2eC-x4UXc5m6QexNbx8w", // Chakra Overflow: self IDG
  "ou7VyChQ-SFCm8T8yGS7I", // Eclipse Drain: self lifesteal 35% + IDG 30
  "J2KOpNHk5LJthnzb27H1h", // Stormguard Aura: self DDT 30 + shield
  "kUcL8K94TW3iCkRcoik_7", // Inner Flame: self absorb 20% + shield
  "c-yTyBUJil8MzlAIHApUG", // Black Crow: damage 35 + vamp 40 (Earth)
  "mYCbcdDwDzJBul52HiwhC", // Burning Coil: damage 40 + IDT 30 (Fire)
  "nS-iidYFYqWE9Z-UkC84y", // Scorching Sun Strike: damage 40 + wound (Fire)
  "V_VY284CMTuqYqOOX5sa7", // Phoenix Flame Strike: damage 35 + IDG 30 (Fire)
  "VT7oxj_fObWuQa3Rq_BbI", // Stunning Jab: damage 35 + stun
];
export const playerJutsuCatalog = () => {
  const j: Record<string, any> = { ...t0.jutsu };
  for (const id of ELITE_KIT) if (!j[id]) j[id] = capturedJutsu(id).record;
  return j;
};
export type PlayerModel = { variant: PlayerVariant; pets: number; immune: boolean; idgRows?: number; sustain: { lifestealGear: number; siphonInnate: number } };
/**
 * The geared level-100 stand-in. The harness's old `elite` tier carried one +400% gear row, but the engine realises a
 * tag row at power <= 100, so it hit for less than the Kitsune-geared `average`. Here: the real Kitsune set, one
 * decreasedamagetaken row, and `idgRows` +100% increasedamagegiven gear rows (gear rows fold additively into the
 * pre-battle increase pool, process.ts computeDamagePacket), sized so that the kit's typical hit on an AI wearing only
 * AI Heavy Armor is 5-8k (the director's logs). Pools x6 (30,300 HP).
 */
export const ELITE_GEAR = { damageTakenReductionPct: 75, poolsMultiplier: 6, idgRows: 20 };
export const playerModel = (name: string, over: any = {}): PlayerModel => {
  if (name.startsWith("elite") && over.gear === undefined && GEAR_OVERRIDE) over = { ...over, gear: GEAR_OVERRIDE };
  if (name === "average") return { variant: { ...PLAYER_VARIANTS.average! }, pets: 1, immune: false, sustain: { lifestealGear: 0, siphonInnate: 0 } };
  const g = { ...ELITE_GEAR, ...(over.gear ?? {}) };
  const v: PlayerVariant = {
    name: "elite", note: "geared level-100 model (elite gear stand-in + sustain kit)", statBudget: 1,
    stats: { offence: 1_300_000, defence: 1_300_000, generals: 400_000 }, poolsMultiplier: g.poolsMultiplier,
    damageGivenPct: 0, damageTakenReductionPct: g.damageTakenReductionPct, gearItemIds: KITSUNE_SET,
    elements: ["Fire", "Earth"], jutsuIds: ELITE_KIT, jutsuLevel: 25,
  };
  return { variant: v, pets: over.pets ?? 2, immune: name === "elite_imm", idgRows: g.idgRows, sustain: { lifestealGear: over.lifesteal ?? 25, siphonInnate: over.siphon ?? 25 } };
};
/** Player row: the model's variant plus sustain rows (gear lifesteal on the armour row, siphon innate) and the immunity rows. */
export const buildPlayer = (m: PlayerModel, catalog: Record<string, any>) => {
  const u: any = playerQueryUser(0, m.variant, t0.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, catalog);
  const gear = u.items.find((ui: any) => ui.item?.id === "harness-gear-armor");
  if (gear && m.idgRows) for (let i = 0; i < m.idgRows; i++) gear.item.effects.push({ ...structuredClone(gear.item.effects[0]), type: "increasedamagegiven", power: 100, direction: "offence", rounds: 100, description: "harness gear stand-in increasedamagegiven 100%" });
  if (gear && m.sustain.lifestealGear) gear.item.effects.push({ ...structuredClone(gear.item.effects[0]), type: "lifesteal", power: m.sustain.lifestealGear, rounds: 100, description: "harness gear stand-in lifesteal" });
  const innate = (type: string, power: number, extra: any = {}) => ({ ...structuredClone(tag(type, { power, rounds: 100, ...extra })), target: "INHERIT" });
  if (m.sustain.siphonInnate) u.effects.push(innate("siphon", m.sustain.siphonInnate, { calculation: "percentage" }));
  if (m.immune) u.effects.push(innate("stunprevent", 100), innate("sealprevent", 100));
  return u;
};

/* ------------------------------------------------------------------ the fight runner */
export type Policy = "play" | "ignore";
export type ActCfg = {
  act: 1 | 2 | 3;
  bossIds: string[]; // AI ids placed as targets
  rows: Record<string, any>; // bosses + summon templates
  recs: Record<string, any>;
  positions?: Record<string, Cell>; // forced cells by AI id
  maxRounds: number;
  killOrder?: "sayo" | "silence";
};
export type FightOpts = { seed: number; policy: Policy; model: PlayerModel; start?: { hp?: number; cp?: number; sp?: number }; trace?: boolean; catalog: Record<string, any> };
export type SetStat = { mark: number; land: number; hit: number; dmg: number; unmarked: number };
export type ActResult = {
  act: number; seed: number; outcome: "won" | "lost" | "stalled"; rounds: number; endHp: number; endCp: number; endSp: number;
  bossHpPct: Record<string, number>; deathCause: string | null; maxHit: { dmg: number; by: string };
  sets: Record<string, SetStat>; unmarkedTotal: number; specials: Record<string, number>; bossTurns: Record<string, number>; bossIdle: Record<string, number>;
  killFirst: string | null; dmgBySource: Record<string, number>; healed: number; dodges: number; cleanses: number; trace?: string[];
};
/** Set-piece bookkeeping: action id -> [set name, role, telegraph id(s)]. */
export const SETS: Record<string, [string, "mark" | "land", string[]?]> = {
  [JID.refractA]: ["Refraction", "mark"], [JID.refractB]: ["Refraction", "mark"],
  [JID.blastA]: ["Refraction", "land", [JID.refractA]], [JID.blastB]: ["Refraction", "land", [JID.refractB, JID.lucidBlast]],
  [JID.facet]: ["Facet", "mark"], [JID.facetBlast]: ["Facet", "land", [JID.facet]],
  [JID.lucidBlast]: ["Refraction", "land", [JID.refractA]],
  [JID.shatterMark]: ["Shatterfall", "mark"], [JID.shatterBlast]: ["Shatterfall", "land", [JID.shatterMark]],
  [JID.floodMark]: ["Every Name", "mark"], [JID.floodBlast]: ["Every Name", "land", [JID.floodMark]],
  [JID.longHush]: ["Glassfall", "mark"],
  [JID.glass[0]!]: ["Glassfall", "land", [JID.longHush, JID.glass[2]!, JID.glassRecast]],
  [JID.glass[1]!]: ["Glassfall", "land", [JID.glass[0]!]], [JID.glassFirstB]: ["Glassfall", "land", [JID.glass[0]!]],
  [JID.glass[2]!]: ["Glassfall", "land", [JID.glass[1]!]], [JID.glassRecast]: ["Glassfall", "land", [JID.glassFirstB]],
};
for (const k of Object.keys(PAT.etch)) { SETS[JID.etch[k]!] = ["Recast", "mark"]; SETS[JID.det[k]!] = ["Recast", "land"]; }
const SPECIAL_IDS: Record<string, string> = {
  [JID.lucidBlast]: "Lucid", [JID.hushUnbridled]: "Unbridled Hush", [JID.listeningUnbridled]: "Unbridled Listening", [JID.cradle]: "Cradle",
  [JID.listening]: "Listening", [JID.likeness]: "Your Likeness", [JID.enrage]: "Enrage", [JID.quiet]: "The Quiet", [JID.pull]: "Breathless Pull",
  [JID.starHush]: "Hush on a safe tile", [JID.m2Entry]: "No One Is Mended", [JID.quietFall]: "Cycle end", [JID.summonPorter]: "Worn: Porter",
  [JID.summonHana]: "Worn: Hana", [JID.summonTomo]: "Worn: Tomo", [JID.glassRecast]: "Long Hush recast", [JID.hush[0]!]: "Hush", [JID.hush[1]!]: "Hush", [JID.hush[2]!]: "Hush",
};
/** Cells a pattern record covers when cast by `caster` (BATTLEFIELD or CASTER origin). */
export const recCells = (rec: any, caster: Cell): Set<string> => {
  const ct = rec?.coordinateTargeting;
  if (!ct) return new Set();
  const cs = ct.coordinates.map((c: XY) => (ct.origin === "CASTER" ? [caster[0] + c.longitude, caster[1] + c.latitude] : [c.longitude, c.latitude]) as Cell);
  return new Set(cs.filter((c: Cell) => c[0] >= 0 && c[1] >= 0 && c[0] < W && c[1] < H).map(key));
};

export const runAct = async (cfg: ActCfg, o: FightOpts): Promise<ActResult> => {
  const rand = mulberry32(o.seed * 7919 + cfg.act);
  const orig = Math.random;
  Math.random = rand;
  seedEntropy(o.seed * 7919 + cfg.act);
  try {
    const player = buildPlayer(o.model, o.catalog);
    const pets = o.model.pets > 0 ? [petFor(player)] : undefined;
    if (pets) player.activePetId = pets[0]!.id;
    let b: any = await assembleFloor({ players: [player], enemyRows: cfg.rows, floor: { kind: "boss", waves: [{ aiIds: cfg.bossIds, delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmgCfg(), mode: "quest", ...(pets ? { pets } : {}) });
    for (const [id, r] of Object.entries(cfg.recs)) if (!b.extraState.jutsus[id]) b.extraState.jutsus[id] = r;
    if (o.model.pets > 1) addClonePet(b, player.userId);
    const puid = player.userId;
    const pu = () => b.usersState.find((u: any) => u.userId === puid)!;
    const bossU = (aid: string) => b.usersState.find((u: any) => u.controllerId === aid && !u.isSummon);
    for (const [aid, c] of Object.entries(cfg.positions ?? {})) { const u = bossU(aid); if (u) [u.longitude, u.latitude] = c; }
    // Player side spawns on the west edge (column 0-1), facing the bosses.
    {
      const p0 = pu();
      const free = (c: Cell) => !b.usersState.some((u: any) => u !== p0 && u.longitude === c[0] && u.latitude === c[1]);
      // Seeded west-edge spawn (columns 0-1, rows 2-7): the run's only positional variance besides the random Hush seeds.
      const cands: Cell[] = [];
      for (const col of [0, 1]) for (let row = 2; row <= 7; row++) cands.push([col, row]);
      const open = cands.filter(free);
      const c = open[Math.floor(rand() * open.length)]!;
      [p0.longitude, p0.latitude] = c;
      for (const pet of b.usersState.filter((u: any) => u.petId)) { const f = ALL.filter((x) => x[0] <= 2 && free(x)).sort((a, b) => dist(a, c) - dist(b, c))[0]!; [pet.longitude, pet.latitude] = f; }
    }
    const maxHp = getEffectiveMaxPool(pu(), b.usersEffects, "Health");
    const maxCp = getEffectiveMaxPool(pu(), b.usersEffects, "Chakra");
    const maxSp = getEffectiveMaxPool(pu(), b.usersEffects, "Stamina");
    if (o.start?.hp !== undefined) pu().curHealth = Math.max(1, Math.round(maxHp * o.start.hp));
    if (o.start?.cp !== undefined) pu().curChakra = Math.round(maxCp * o.start.cp);
    if (o.start?.sp !== undefined) pu().curStamina = Math.round(maxSp * o.start.sp);
    const grid = getBattleGrid(1, b);
    const res: ActResult = {
      act: cfg.act, seed: o.seed, outcome: "stalled", rounds: 0, endHp: 0, endCp: 0, endSp: 0, bossHpPct: {}, deathCause: null, maxHit: { dmg: 0, by: "" },
      sets: {}, unmarkedTotal: 0, specials: {}, bossTurns: {}, bossIdle: {}, killFirst: null, dmgBySource: {}, healed: 0, dodges: 0, cleanses: 0, ...(o.trace ? { trace: [] } : {}),
    };
    const set = (k: string) => (res.sets[k] ??= { mark: 0, land: 0, hit: 0, dmg: 0, unmarked: 0 });
    const actionRounds: number[] = [];
    const turnActs = new Map<string, string[]>();
    const lastBossAct = new Map<string, { id: string; round: number }[]>(); // per boss uid: its actions
    const cycleEtched = new Set<string>(); // etchings laid in the current Act II cycle (pattern keys, multiset as counts)
    const etchCount: Record<string, number> = {};
    const markPos = new Map<string, string>(); // caster-anchored marks: where the caster stood
    const name = (id?: string) => (id ? (b.extraState.jutsus[id]?.name ?? id) : "none");
    const alive = (u: any) => u && stillInBattle(u, b.usersEffects);
    const tryAction = (actionId: string, c: Cell, actor = puid) => {
      const u = b.usersState.find((x: any) => x.userId === actor)!;
      const action = availableUserActions(b, actor, true, true).find((a: any) => a.id === actionId);
      if (!action || !actionPointsAfterAction(u, b, action).canAct) return false;
      try { b = performBattleAction({ battle: structuredClone(b), action, grid, contextUserId: actor, actorId: actor, longitude: c[0], latitude: c[1] }).newBattle; return true; } catch { return false; }
    };
    /* ---- what a player who plays the mechanics avoids ---- */
    const enemySide = () => new Set(b.usersState.filter((u: any) => u.direction === "right").map((u: any) => u.userId));
    const dangerCells = () => {
      const es = enemySide();
      const danger = new Set<string>();
      const safe = new Set<string>();
      const linger = new Set<string>();
      for (const g of b.groundEffects as any[]) {
        if (!es.has(g.creatorId)) continue;
        if ((g.rounds ?? 0) <= 0 && !g.castThisRound) continue;
        const k = `${g.longitude},${g.latitude}`;
        if (g.type === "visual" && (g.staticAnimation === "tg_heavy" || g.staticAnimation === "tg_control")) danger.add(k);
        if (g.type === "visual" && g.staticAnimation === "tg_safe") safe.add(k);
        if (g.type === "visual" && g.staticAnimation === "tg_linger") linger.add(k);
      }
      // Memory: the next Recast detonation (Act II) and the Long Hush recast (Act III).
      const s2 = bossU(AI.sayo2);
      if (s2 && alive(s2)) {
        const nxt = nextComboAction(b, s2);
        if (nxt && Object.values(JID.det).includes(nxt)) for (const k of recCells(cfg.recs[nxt], [s2.longitude, s2.latitude])) danger.add(k);
      }
      const st = bossU(AI.saint);
      if (st && alive(st) && b.usersEffects.some((e: any) => e.targetId === st.userId && e.type === MK.gCs)) for (const k of recCells(cfg.recs[JID.glassRecast], [st.longitude, st.latitude])) danger.add(k);
      if (safe.size) for (const c of ALL) if (!safe.has(key(c))) danger.add(key(c));
      // The Silence never moves: a player who plays it keeps out of Stillness reach unless the Silence is the target.
      const si = bossU(AI.silence);
      if (si && alive(si) && currentTarget && !currentTarget.isSummon && currentTarget.controllerId !== AI.silence) for (const c of ALL) if (dist(c, [si.longitude, si.latitude]) <= 3) linger.add(key(c));
      // Glass Thorns (Act II): she bursts thorns within 2 of herself on every etching turn; keep 3 hexes away.
      const s2b = bossU(AI.sayo2);
      if (s2b && alive(s2b)) for (const c of ALL) if (dist(c, [s2b.longitude, s2b.latitude]) <= 2) linger.add(key(c));
      return { danger, linger, safe };
    };
    const free = (c: Cell) => !b.usersState.some((u: any) => u.longitude === c[0] && u.latitude === c[1] && alive(u));
    const dodgeStep = (): boolean => {
      const here: Cell = [pu().longitude, pu().latitude];
      const { danger, linger } = dangerCells();
      const bad = (k: string) => danger.has(k) || linger.has(k);
      if (!bad(key(here))) return false;
      const acts = availableUserActions(b, puid, true, true);
      if (!acts.some((a: any) => a.id === "move")) { if (tryAction("cleanse", here)) { res.cleanses++; return true; } return false; }
      const prev = new Map<string, string | null>([[key(here), null]]);
      const depth = new Map<string, number>([[key(here), 0]]);
      const q: Cell[] = [here];
      const found: { c: Cell; d: number; lingerOnly: boolean }[] = [];
      while (q.length) {
        const c = q.shift()!;
        const d = depth.get(key(c))!;
        if (d > 0 && !bad(key(c))) found.push({ c, d, lingerOnly: false });
        if (d >= 8) continue;
        for (const n of ALL) if (!prev.has(key(n)) && dist(c, n) === 1 && free(n)) { prev.set(key(n), key(c)); depth.set(key(n), d + 1); q.push(n); }
      }
      // If no clean cell exists, accept a linger (Hush) cell outside the blast.
      if (!found.length && danger.has(key(here))) for (const [k, d] of depth) if (d > 0 && !danger.has(k)) found.push({ c: k.split(",").map(Number) as Cell, d, lingerOnly: true });
      if (!found.length) return false;
      found.sort((a, c) => a.d - c.d);
      const t = found[0]!;
      if (t.d >= 2 && dist(here, t.c) <= 5 && tryAction("replacementTechnique", t.c)) return true;
      let step = key(t.c);
      while (prev.get(step) !== key(here)) step = prev.get(step)!;
      return tryAction("move", step.split(",").map(Number) as Cell);
    };
    /* ---- the player's target (play: feelers first, then the kill order; Hana before Sayo; ignore: closest) ---- */
    const chooseTarget = () => {
      const es = b.usersState.filter((u: any) => u.direction === "right" && alive(u));
      if (!es.length) return null;
      const by = (aid: string) => es.find((u: any) => u.controllerId === aid || (u.isSummon && u.username?.startsWith(cfg.rows[aid]?.username ?? "@@")));
      const sayoUp = alive(bossU(AI.sayo1));
      // Feelers matter only while Sayo lives (Cradle); after her, an Unbridled feeler a turn would only stall the player.
      const order = cfg.act === 1 ? [...(sayoUp ? [AI.feeler] : []), AI.likeness, cfg.killOrder === "silence" ? AI.silence : AI.sayo1, AI.sayo1, AI.silence]
        : cfg.act === 2 ? [AI.hana, AI.tomo, AI.sayo2, AI.porter] : [AI.saint];
      for (const aid of order) { const u = by(aid); if (u) return u; }
      return es[0];
    };
    let currentTarget: any = null;
    const setPlayerTarget = (target: any | null) => {
      currentTarget = target;
      const prof = b.extraState.aiProfiles[pu().aiProfileId];
      prof.__orig ??= structuredClone(prof.rules);
      prof.rules = structuredClone(prof.__orig);
      if (!target) return;
      for (const r of prof.rules) {
        const re = (x: any) => { if (x.target === PL) { x.target = "COORDINATE"; x.coordinates = { longitude: target.longitude, latitude: target.latitude }; } };
        re(r.action);
        r.conditions.forEach(re);
      }
    };
    const maxRounds = cfg.maxRounds;
    let prevBossAlive = Object.fromEntries(cfg.bossIds.map((a) => [a, true]));
    for (let step = 0; step < maxRounds * 60; step++) {
      const pre = alignBattle(b, actionRounds, puid);
      if (pre.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
      if (b.round > maxRounds) break;
      const actor = pre.actor;
      const human = actor.userId === puid;
      tickClock(1000);
      const tk = `${b.round}:${actor.userId}`;
      if (!turnActs.has(tk)) turnActs.set(tk, []);
      const hpBefore = new Map(b.usersState.map((u: any) => [u.userId, u.curHealth]));
      const pPos: Cell = [pu().longitude, pu().latitude];
      const aPos: Cell = [actor.longitude, actor.latitude];
      let actionId: string | undefined;
      if (human && o.policy === "play" && dodgeStep()) { actionId = "dodge"; res.dodges++; }
      else if (human && o.policy === "play" && wantsCleanse(b, puid) && tryAction("cleanse", pPos)) { actionId = "cleanse"; res.cleanses++; }
      else {
        if (human) setPlayerTarget(o.policy === "play" ? chooseTarget() : null);
        const r = performAIaction(b, grid, actor.userId);
        actionId = r.nextActionId;
        if (human && o.policy === "play" && (actionId === "move" || actionId === "replacementTechnique")) {
          const after = r.nextBattle.usersState.find((u: any) => u.userId === puid)!;
          const { danger, linger } = dangerCells();
          const k = `${after.longitude},${after.latitude}`;
          if (danger.has(k) || linger.has(k)) { actionId = tryAction("wait", pPos) ? "wait" : undefined; if (!actionId) b = r.nextBattle; }
          else b = r.nextBattle;
        } else b = r.nextBattle;
      }
      const post = alignBattle(b, actionRounds, puid);
      if (post.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(post.actionRound)) actionRounds.push(post.actionRound);
      if (!actionId && actor.isAutoCombat) b.roundStartAt = new Date(Date.now() - 61_000);
      turnActs.get(tk)!.push(actionId ?? "none");
      const pAfter = pu();
      const pLoss = Math.max(0, (hpBefore.get(puid) ?? 0) - pAfter.curHealth);
      const pGain = Math.max(0, pAfter.curHealth - (hpBefore.get(puid) ?? 0));
      if (pGain > 0) res.healed += pGain;
      const isEnemy = actor.direction === "right";
      const src = human ? "own turn (pools/drain)" : isEnemy ? (SETS[actionId ?? ""]?.[0] ?? name(actionId)) : "own side";
      if (pLoss > 0) {
        const label = isEnemy ? `${actor.isSummon ? actor.username : (actor.username ?? "")}: ${src}` : src;
        res.dmgBySource[label] = (res.dmgBySource[label] ?? 0) + pLoss;
        if (pLoss > res.maxHit.dmg) res.maxHit = { dmg: Math.round(pLoss), by: label };
        if (pAfter.curHealth <= 0 && !res.deathCause) res.deathCause = label;
      }
      if (isEnemy && !actor.isSummon && actionId) {
        const hist = lastBossAct.get(actor.userId) ?? [];
        const sp = SETS[actionId];
        if (sp) {
          const s = set(sp[0]);
          if (sp[1] === "mark") {
            s.mark++;
            markPos.set(actionId, key(aPos));
            if (sp[0] === "Recast") { const k = Object.entries(JID.etch).find(([, v]) => v === actionId)![0]; etchCount[k] = (etchCount[k] ?? 0) + 1; }
          } else {
            s.land++;
            const cells = recCells(cfg.recs[actionId], aPos);
            if (cells.has(key(pPos)) || pLoss > 0) { s.hit += cells.has(key(pPos)) ? 1 : 0; s.dmg += pLoss; }
            let ok: boolean;
            if (sp[0] === "Recast") {
              const k = Object.entries(JID.det).find(([, v]) => v === actionId)![0];
              ok = (etchCount[k] ?? 0) > 0;
              if (ok) etchCount[k]!--;
            } else {
              const prevTurn = hist.filter((h) => h.round === pre.actionRound - 1).map((h) => h.id);
              const thisTurn = hist.filter((h) => h.round === pre.actionRound).map((h) => h.id);
              ok = (sp[2] ?? []).some((t) => prevTurn.includes(t) || thisTurn.includes(t));
              const anchored = cfg.recs[actionId]?.coordinateTargeting?.origin === "CASTER";
              if (ok && anchored && (sp[2] ?? []).some((t) => markPos.has(t)) && !(sp[2] ?? []).some((t) => markPos.get(t) === key(aPos))) ok = false;
            }
            if (!ok) { s.unmarked++; res.unmarkedTotal++; }
          }
        }
        if (actionId === JID.quietFall) for (const k of Object.keys(etchCount)) etchCount[k] = 0;
        hist.push({ id: actionId, round: pre.actionRound });
        lastBossAct.set(actor.userId, hist);
      }
      if (isEnemy && actionId && SPECIAL_IDS[actionId]) res.specials[SPECIAL_IDS[actionId]!] = (res.specials[SPECIAL_IDS[actionId]!] ?? 0) + 1;
      for (const aid of cfg.bossIds) {
        const u = bossU(aid);
        const a = alive(u);
        if (prevBossAlive[aid] && !a && !res.killFirst) res.killFirst = aid;
        prevBossAlive[aid] = a;
      }
      if (o.trace) {
        const bossTxt = cfg.bossIds.map((aid) => { const u = bossU(aid); return u ? `${aid.replace("moe-ai-", "")} ${(100 * Math.max(0, u.curHealth) / u.maxHealth).toFixed(0)}%` : ""; }).join(" ");
        res.trace!.push(`r${pre.actionRound} ${(human ? `PLAYER>${(currentTarget?.username ?? "-").slice(0, 8)}` : actor.username ?? "?").slice(0, 22).padEnd(22)} ${String(actionId === "dodge" ? "DODGE" : name(actionId)).slice(0, 28).padEnd(28)} p@${pPos} hp ${Math.round(pAfter.curHealth)} (${pLoss ? "-" + Math.round(pLoss) : pGain ? "+" + Math.round(pGain) : "0"}) | ${bossTxt}`);
      }
      const side = (dir: string) => b.usersState.some((u: any) => u.direction === dir && !u.isSummon && alive(u));
      if (!alive(pu())) { res.outcome = "lost"; break; }
      if (!side("right")) { res.outcome = "won"; break; }
    }
    for (const [k, acts] of turnActs) {
      const uid = k.split(":")[1]!;
      const u = b.usersState.find((x: any) => x.userId === uid);
      if (!u || u.direction !== "right" || u.isSummon) continue;
      res.bossTurns[u.controllerId] = (res.bossTurns[u.controllerId] ?? 0) + 1;
      if (acts.every((a) => a === "wait" || a === "none")) res.bossIdle[u.controllerId] = (res.bossIdle[u.controllerId] ?? 0) + 1;
    }
    res.rounds = b.round;
    res.endHp = Math.max(0, pu().curHealth) / maxHp;
    res.endCp = Math.max(0, pu().curChakra) / maxCp;
    res.endSp = Math.max(0, pu().curStamina) / maxSp;
    for (const aid of cfg.bossIds) { const u = bossU(aid); if (u) res.bossHpPct[aid] = Math.round(1000 * Math.max(0, u.curHealth) / u.maxHealth) / 10; }
    return res;
  } finally {
    Math.random = orig;
  }
};
/** Cleanse when carrying 2+ stacks of the Quiet (or any root while a mark is up is handled by the dodge). */
const wantsCleanse = (b: any, puid: string) => b.usersEffects.filter((e: any) => e.targetId === puid && e.type === "increasedamagetaken" && (e.rounds ?? 0) > 0).length >= 2;
/** The next id of whichever use_combo_action rule of this AI would continue (harness memory of the etch order). */
export const nextComboAction = (b: any, u: any): string | null => {
  const prof = b.extraState.aiProfiles[u.aiProfileId];
  if (!prof) return null;
  const hist = (u.usedActions ?? []).map((a: any) => a.id);
  let best: { k: number; next: string } | null = null;
  for (const r of prof.rules) {
    if (r.action.type !== "use_combo_action") continue;
    const ids = r.action.comboIds as string[];
    const passes = r.conditions.every((c: any) => c.type !== "has_effect" || b.usersEffects.filter((e: any) => e.targetId === u.userId && e.type === c.effectType).reduce((s: number, e: any) => s + e.power, 0) >= c.threshold);
    if (!passes) continue;
    let K = 0;
    for (let k = Math.min(ids.length, hist.length); k >= 1; k--) { let m = true; for (let i = 0; i < k; i++) if (hist[hist.length - k + i] !== ids[i]) { m = false; break; } if (m) { K = k; break; } }
    const next = K > 0 && K < ids.length ? ids[K]! : ids[0]!;
    if (!best || K > best.k) best = { k: K, next };
    break; // the first passing combo rule is the one the AI evaluates
  }
  return best?.next ?? null;
};
let DMG: any;
export const setDmgConfig = (c: any) => { DMG = c; };
const dmgCfg = () => DMG;
export const addClonePet = (battle: any, ownerId: string) => {
  const pet = battle.usersState.find((u: any) => u.petId && u.controllerId === ownerId);
  if (!pet) return;
  const c = structuredClone(pet);
  c.userId = nanoid();
  c.petId = `${pet.petId}-harness2`;
  c.username = `${pet.username} (2)`;
  battle.usersState.push(c);
  battle.usersState.sort((a: any, b: any) => b.initiative - a.initiative);
};
export const StatTypesAll = StatTypes;
