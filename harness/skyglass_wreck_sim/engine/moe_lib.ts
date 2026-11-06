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
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { nanoid } from "nanoid";
import { performAIaction } from "@/libs/combat/ai_v2";
import { availableUserActions, actionPointsAfterAction, performBattleAction, stillInBattle } from "@/libs/combat/actions";
import { applySageModeAfterRoundTransition } from "@/libs/combat/process";
import { getBattleSpawnLocations } from "@/libs/combat/participants";
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
  risesField: cellsWhere((c, r) => !isStar(c, r)), // Act II pools: anywhere but the three
  stillReach: ALL.filter((c) => dist(c, [11, 4]) <= 3), // the Silence's post is [11, 4]
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
    pullDmg: 40, lancet: 70, refract: 300, facet: 340, likenessHit: 90, stillness: 110, grasp: 30, graspDrain: 4,
    hushDrain: 4, hushDmg: 25, detonate: 360, quiet: 60, quietIdt: 15, shatter: 300, flood: 420, glass: 260, recastIII: 380,
    enrage: 600, porter: 80, hana: 8, tomo: 60, cradleDR: 90,
  },
  /** Act I Hush (one record, pass 3 merge): pools per cast and % max HP drained per action; cast every third turn, its
   * 8-round pools pile up (about three casts live at once). */
  hushCount: 6, hushPoolDrain: 4,
  /** Act II, The Hush Rises (RUL-2026-11-02-097 item 1): one cast per etching turn, per cycle: pools and % max HP per action. */
  /** Act II, The Hush Rises (one record, pass 3 merge): cast on every etching turn, so a cycle of 3/4/5/5 etchings lays
   * 3/4/5/5 casts; the pools last `rounds` and pile up across cycles (the growing threat, moe_probe P4b). */
  rises: { count: 10, drain: 15, rounds: 10 },
  /** Telegraphed Stillness (RUL-2026-11-02-097 item 2): mark within 3 of the Silence, then damage + stun. */
  still: { cd: 3, stunAp: 100, stunRounds: 1 },
  /** Lucid (RUL-2026-11-02-097 item 4): +100% damage-given rows on Sayo when she wakes alone. */
  lucidIdg: 1,
  pullStunAp: 50, // Breathless Pull: AP the stun takes from the next turn
  /** Analysis only: false puts every telegraph back on a `visual` (pre-pass-3), to measure the server filter's effect. */
  telegraphCarrier: true,
  pullDist: 1, // Breathless Pull: hexes drawn toward her (the stun is the threat)
  pullCd: 4, // Breathless Pull mark cooldown (one flood cycle: mark, pull + flood mark, flood, one free turn)
  hushUnbridledCount: 3, // pools per Unbridled Hush (every turn)
  porterPush: 2, // Doorward Sweep shove (hexes); 0 = none
  /** Pass 6 ramp: each Glass Lancet stacks +pct% damage given on its caster for `rounds` (0 = off). */
  ramp: { pct: 0, rounds: 99 },
  /** Pass 6: multiplier on every boss-side formula hit (see buildRecords). */
  bossDmgScale: 1,
  /** Pass 6: the player-anchored mark (Act I: the Silence; Act II: Sayo on lull turns); % of max HP drained. */
  turnMark: { on: false, act1: 60, act2: 70, cd: 3 },
  /** Pass 6: Etching: Heart covers the east block too (columns 4-11, rows 3-6), closing Act II's 8 never-marked hexes. */
  etchDWide: false,
  /** Pass 6: cooldown of the Act I blasts (2 let a mark's blast slip a round when the blast was still cooling: an unmarked hit). */
  act1BlastCd: 2,
  /** Pass 6: the skilled player policy for every _real profile (see realRules). */
  skilledPolicy: false,
  /** Pass 6: cleansable debuff left by an eruption hit, per act ({dh, idt, rounds}); the cast becomes CHARACTER. */
  eruptDebuff: { on: false } as { on: boolean; act1?: any; act2?: any; act3?: any },
  /** Director 2026-11-05 proposal: per-boss SELF buffs (see buildRecords). */
  bossAura: { on: false } as any,
  /** Sim-only: visual "piece" tags on the signature moves (art pass identity check). */
  visualPieces: false,
  /** Director 2026-11-05 proposal: Grasp cooldown (0 = every turn; 2 = root every other round). */
  graspCd: 0,
  /** Policy (2026-11-05 pool audit): walk paths never cross pools, never step onto a pool to approach. */
  poolAware: false,
  /** Director 2026-11-05 (approved): Act I mark spacing (see buildRecords). */
  act1Spacing: false,
  /** Director 2026-11-05 (fight script): the Lancet ramp carries no clearprevent. */
  rampClearable: false,
  /** Director 2026-11-05: The Silence Turns from round 4, the first Listening from round 2. */
  act1Stagger: false,
  /** Director 2026-11-05: Sayo (Act I, II, III) carries innate stunprevent. */
  sayoStunImmune: false,
  /** Blasts with cooldown 0 so the shared pierce cooldown never delays a marked blast (see buildRecords). */
  gcdSafeBlasts: false,
  /** Telegraph art rounds for boss marks (see MARK_ART). */
  markArtRounds: 1,
  /** Policy fix: never step back onto a pool hex the player dodged off earlier in the same round. */
  noPoolReentry: false,
  /** Director 2026-11-05: the Silence steps toward the highest-HP opponent when it is out of the Silence Turns' reach. */
  silenceStalk: false,
  /** Director 2026-11-05: Stillness (mark and Nothing Moves) covers the hexes within 3 of the Silence wherever she stands. */
  stillAnchored: false,
  /** Pass 6 live calibration: Act II Recasts stay GROUND (debuff as a pool) instead of CHARACTER + Sayo's post. */
  recastGround: false,
  /** Pass 6 (director 2026-11-05 probe): Glass Lancet cooldown (1 = every turn it is free). */
  lancetCd: 1,
  /** Pass 6: extra multiplier on the summons' hits (Grasp, Your Own Strike, Doorward Sweep, Cadet's Tether). */
  summonDmgScale: 1,
  /** Pass 5 (RUL-2026-11-04-113): eruptions as a fixed share of an endgame max HP (elite model 31,500). */
  /** Pass 6 loop 11 (director 2026-11-05): `recast` is the Act II Recasts' own share (default: act2); Nothing Moves keeps act2's. */
  eruption: { on: false, hp: 31500, act1: 40, act2: 60, act3: 80 } as { on: boolean; hp: number; act1: number; act2: number; act3: number; recast?: number },
  /** Analysis only (pass 4): raise every cooldown below this to it (Forge L16 refuses jutsu cooldown < 3). 0 = off. */
  cooldownFloor: 0,
  hushRounds: 8,
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
  /** Act III redesign prototype (docs/design/MOTHER_OF_ECHOES_ACT3.md, 2026-11-05): see A3_DEFAULTS. */
  act3v2: { on: false } as any,
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
  likeness: "moe-your-likeness", likenessStrike: "moe-likeness-strike", likenessCopy: "VuFuBtE7h5B1nnA2J1lFZ" /* Stolen Form (live, reused) */,
  hush: ["moe-hush", "moe-hush", "moe-hush"], hushUnbridled: "moe-hush-unbridled", listening: "moe-listening",
  listeningUnbridled: "moe-listening-unbridled", stillness: "moe-stillness", cradle: "moe-cradle", grasp: "moe-feeler-grasp",
  enrage: "moe-the-glass-remembers", turnI: "moe-the-silence-turns", turnII: "moe-the-glass-turns",
  etch: Object.fromEntries("ABCDE".split("").map((k) => [k, `moe-etching-${k.toLowerCase()}`])) as Record<string, string>,
  det: Object.fromEntries("ABCDE".split("").map((k) => [k, `moe-recast-${k.toLowerCase()}`])) as Record<string, string>,
  // Pass 3 merge: one Hush record for Act I and one Hush Rises record for Act II (the arrays keep the cycle / band
  // indexing; every entry is the same id).
  quietFall: "moe-the-glass-falls-quiet", rises: ["moe-hush-rises", "moe-hush-rises", "moe-hush-rises", "moe-hush-rises"],
  stillnessBlast: "moe-stillness-blast", lucidWake: "moe-lucid", pullMark: "moe-breathless-pull-mark", m2EntryCast: "moe-probe-no-one-is-mended-cast",
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
  refractA: "increaserange", refractB: "fleeprevent", facet: "robprevent", still: "robprevent", // still: the Silence's own marker
  pull: "summonprevent", breath: "increasecooldown", // Saint: Breathless Pull mark / blast (she summons nothing)
  sayoToken: "onehitkillprevent", silenceToken: "sealprevent",
  // Act II
  done: "fleeprevent", counter: "increasecooldown", // counter: power 1 per cycle, no probability roll (prevent types roll power/100)
  // Act III
  shatter: "increaserange", flood: "fleeprevent", gA: "robprevent", gB: "onehitkillprevent", gC: "disarm", gCs: "elementalseal",
  firstPass: "decreasecooldown",
};
/**
 * Act III redesign (prototype; docs/design/MOTHER_OF_ECHOES_ACT3.md). The Saint uses Acts I-II's vocabulary, evolved:
 * Phase I "Lucid" (100-60%): Refraction every turn (break + redraw), Facet with a x3 open guard, Hold Still (the follow
 * ring), The Silence Holds Her (self-Cradle + Stillness: Clear is the answer), the Remainder Lancet (clearable ramp).
 * Phase II "Every Name, Remembered" (60-25%): a warned heal cut that spares the three stars; a 4-turn combo: Etching of
 * the Act II region holding one star (+ Hush Rises) -> Every Name (stars shown) -> The Names Flood In over everything
 * but the stars AND the remembered etching (x4 open guard) -> Hush on a star (+ Rises).
 * Phase III "A Good Impression" (<25%): a rolling clock: each turn a third of the hall falls together with one echo of
 * an earlier act (Act I lines, Act II Heart, Act II Seam), the next is marked, her guard is open x2, and Every Line
 * Through You (the follow mark multiplied: a cross through the player, lethal) lands on a step-off.
 * Engine rules this relies on: every eruption has cooldown 0 (pierce / drain / stun are shared-cooldown tags,
 * drizzle/constants.ts:261-282; applyActionCooldowns locks every other action sharing one for 3 rounds when the cast
 * has cooldown > 0, actions.ts:1461-1490); chain records cost 60 AP and extras 40 so no mark erupts in its own turn;
 * phase markers are negative types so a Clear (removeEffects, tags.ts:1179-1235) never cancels a lethal set piece, while
 * Stillness's marker is positive (robprevent) so a Clear cancels Nothing Moves, as in Act I.
 */
export const J3 = {
  opener: "moe-saint-refraction", lucid: "moe-saint-lucid-refraction", facet: "moe-saint-facet", facetBreak: "moe-saint-facet-breaks",
  holdStill: "moe-saint-hold-still", silenceHolds: "moe-saint-the-silence-holds-her", nothingMoves: "moe-saint-nothing-moves",
  lancet: "moe-saint-remainder-lancet", stir: "moe-saint-the-names-stir", mended: "moe-saint-no-one-is-mended",
  // Director 2026-11-05 (decision 8): Phase II reuses Act II's Etching records as they are (same pattern, AP, cooldown, art).
  etch: { A: "moe-etching-a", B: "moe-etching-b", D: "moe-etching-d" } as Record<string, string>,
  flood: { A: "moe-saint-flood-rime", B: "moe-saint-flood-ember", D: "moe-saint-flood-heart" } as Record<string, string>,
  everyName: "moe-saint-every-name", rises: "moe-saint-hush-rises", starHush: "moe-saint-hush-where-they-refused",
  impression: "moe-saint-a-good-impression", pane: ["moe-saint-echo-pane-a", "moe-saint-echo-pane-b", "moe-saint-echo-pane-c"], everyLine: "moe-saint-every-line",
};
export const MK3 = {
  a: "fleeprevent", b: "summonprevent", f: "elementalseal", still: "robprevent", phase: "increasecooldown",
  // decrease* tags are stored with negative power once cast, so a has_effect threshold never passes on them: no decrease*
  // markers. Player kits put increasedamagetaken (223 of 1,237 captured jutsu) and decreasedamagegiven (114) on the boss,
  // which would trip such a marker (first prototype run: 11 unmarked panes); fleeprevent, disarm and increasecooldown
  // appear on none, summonprevent and elementalseal on one each (harvests/inbox/tnr_results_1792732003454.json). Her
  // jutsu carry jutsuWeapon NONE, so disarm hides nothing. Reuse across phases is safe because every Phase III rule also
  // requires phase >= 2 and the Phase III entry phase >= 1.
  clean: "disarm", cycleEnd: "fleeprevent", gA: "disarm", gB: "summonprevent", gC: "fleeprevent",
};
export const A3_DEFAULTS = {
  on: false,
  holdStillPct: 50, everyLinePct: 100,
  cradleDR: 85, cradleAbsorb: 30, cradleRounds: 3, cradleCd: 6, cradleGate: 95,
  stillPierce: 2500, stillStunAp: 100,
  guardFacet: 3, guardFlood: 4, guardPane: 2,
  lancetCd: 2, lancetCost: 40, openerCd: 4,
  rises: { count: 6, drain: 8, rounds: 6 }, starHush: { drain: 3, rounds: 3 }, mendedRounds: 10,
  /** Phase II etching order (Act II regions; each holds one star: Rime the north, Ember the south, Heart the middle). */
  order: ["A", "B", "D"],
  /** Phase III echo per pane (Act I lines / Act II regions). */
  echoes: ["refractA", "D", "C"],
  /** Phase III line length (hexes north and south of the player). */
  lineArm: 4,
  /** Phase I Hold Still bar length (hexes north and south of the player; the player's own hex is never included). */
  barArm: 2,
  /** Phase I line-break pools (rounds). */
  linePoolRounds: 1,
  /** HP gates: the warning, Phase II, Phase III. */
  stirGate: 70, p2Gate: 60, p3Gate: 25,
  /** Sim policy: drink the Energy Potion once the heal cut is announced, below this HP %. 0 = never. */
  topUpBelow: 75,
  /** Sim policy: Clear the Saint for her Cradle, or for the ramp at this many live stacks. */
  clearRampStacks: 3,
};
export const a3 = (P: any) => ({ ...A3_DEFAULTS, ...(P.act3v2 ?? {}) }) as typeof A3_DEFAULTS;
const A3_ECHO = (k: string): Cell[] => (k === "refractA" ? PAT.refractA : k === "refractB" ? PAT.refractB : PAT.etch[k]!);
const unionCells = (...xs: Cell[][]) => [...new Map(xs.flat().map((c) => [key(c), c])).values()];
const A3_PANE = (A3: typeof A3_DEFAULTS, k: number) => unionCells(PAT.glass[k]!, A3_ECHO(A3.echoes[k]!));
/**
 * Every Line Through You: the column through the target hex, `arm` hexes either way (origin TARGET, libs/combat/targeting.ts
 * COORDINATES TARGET). A column, not a cross: a cross through a hex leaves only two of its six neighbours clear, and with
 * the falling third and its echo marked as well the first prototype trapped 4 of 20 perfect players; any side step clears
 * a column (four of six neighbours).
 */
// Ship pass (2026-11-05): the player's own hex is NOT in the pattern. A ground drain binds whoever stands on its hex when
// any action resolves (process.ts:396-412; live log 2 #64-#65, sim agent 3eb8abab), so a follow mark ON the player is on
// him from her cast and cannot be dodged (the same ring trap as Act I's Silence Turns). Without the centre the column
// only binds a player who steps onto it: step aside (or hold still), never along it.
const A3_CROSS = (arm: number) => [...Array.from({ length: arm }, (_, i) => i + 1).flatMap((d) => [
  { longitude: 0, latitude: d }, { longitude: 0, latitude: -d }])];
export const a3PhaseCombo = (A3: typeof A3_DEFAULTS) => A3.order.flatMap((k) => [J3.etch[k]!, J3.rises, J3.everyName, J3.flood[k]!, J3.starHush, J3.rises]);
const marker = (type: string, rounds = 1, power?: number) => tag(type, {
  power: power ?? (["increasecooldown", "decreasecooldown", "increaserange"].includes(type) ? 1 : 100), rounds, target: "SELF",
  ...(["increasecooldown", "decreasecooldown", "increaserange"].includes(type) ? { actionsAffected: [], calculation: "static" } : {}),
});
const token = (type: string) => marker(type, 100);
const vis = (anim: string, rounds: number) => T.visual(anim, rounds);
/**
 * Telegraph carrier (pass 3, combat.ts:857-859): the server drops every `visual` ground effect created before the round
 * a performAction request started in, so a visual mark vanishes after the player's first action of the next round.
 * Marks therefore ride a non-visual ground carrier holding the art: increaseregeneration, power 1 (the client hides
 * power <= 0), rounds `rounds`, friendlyFire FRIENDLY (only the caster's side would ever get +1% regeneration; no uber
 * rule or marker reads increaseregeneration). Battle log: "marked the ground with increaseregeneration".
 */
let CARRIER_ON = true;
// Telegraph art lifetime (pass 6, director 2026-11-05: the fight must always telegraph). A mark's SELF marker can
// outlive its 1-round art when the boss's next turn slips (AP drained/stunned, or turn order moves her to the front of the
// round): traced seed 18 Silence-first, Far Refraction Breaks landed with 0 of 27 hexes drawn. markArtRounds 2 keeps the
// art up as long as the marker can trigger the blast.
let MARK_ART = 1;
const carrier = (art: string, rounds = MARK_ART, ct?: any) => !CARRIER_ON ? T.visual(art, rounds, ct ? { target: "COORDINATES", coordinateTargeting: ct } : {}) : tag("increaseregeneration", {
  power: 1, rounds, calculation: "percentage", friendlyFire: "FRIENDLY", target: ct ? "COORDINATES" : "INHERIT", ...(ct ? { coordinateTargeting: ct } : {}),
  staticAssetPath: art, staticAnimation: art, appearAnimation: art, disappearAnimation: art, description: "Telegraph: the marked ground",
});
/** Lasting pool art rides the hurting effect itself (no disappear animation), so the pool stays drawn while it hurts. */
const poolArt = (art: string) => (CARRIER_ON ? { staticAssetPath: art, staticAnimation: art, appearAnimation: art } : {});
/** Analysis only (telegraphCarrier false): the pre-pass-3 pool art, a `visual` for the pool's whole life. */
const poolVis = (rounds: number) => (CARRIER_ON ? [] : [vis("tg_linger", rounds)]);
const ALLSTATS = ["None", "Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"];
const ALLGEN = ["Highest", "Strength", "Intelligence", "Willpower", "Speed"];
const weaknessSelf = (mult: number, anim = "moe_guard_open") =>
  tag("weakness", { target: "SELF", rounds: 1, dmgModifier: mult, statTypes: ALLSTATS, generalTypes: ALLGEN, power: 100, staticAnimation: anim });
const heavy = (power: number, anim = "dt_heavy") => T.damage(power, { appearAnimation: anim });
/**
 * Pass 5 (RUL-2026-11-04-113): a telegraphed eruption hits a player still standing in it for a fixed share of an
 * endgame player's max HP. `pierce` with calculation static: damageCalc returns the bare power for any non-formula
 * effect (theninjarpg@3314d122 libs/combat/tags.ts:1438-1497); pierce runs after every damage modifier
 * (process.ts:497-511, 741-756), so decreasedamagetaken and the boss's increasedamagegiven rows never touch it, and it
 * destroys shields instead of being absorbed (process.ts:842-877). dmgModifier is set to 1 because the PierceTag default
 * is 2 (damageCalc multiplies by it, tags.ts:1488-1490). Off = the pass-4 formula hit.
 */
let ERUPT: { on: boolean; hp: number; pct: Record<number, number>; recast?: number } = { on: false, hp: 31500, pct: { 1: 40, 2: 60, 3: 80 } };
const erupt = (act: number, power: number, anim: string, pct = ERUPT.pct[act]!) =>
  ERUPT.on ? T.pierce(Math.round((ERUPT.hp * pct) / 100), { calculation: "static", dmgModifier: 1, description: "Pierces target", appearAnimation: anim }) : heavy(power, anim);
/**
 * Pass 6 (director 2026-11-04): a hit also leaves a cleansable debuff. On a GROUND cast every tag becomes a ground effect
 * that only follows the player while he stands on the hex (process.ts:395-412: a 1-round copy per pass), so the debuff
 * rides a CHARACTER cast instead (actions.ts:1125-1158: user effects on the unit standing on each pattern hex, with the
 * tag's own rounds). decreaseheal runs after the damage passes and cuts heal / lifesteal / vamp / absorb
 * (process.ts:803; tags.ts:1100-1145); both tags are negative statuses (validators/combat.ts:1437-1475), so a Cleanse
 * removes them (tags.ts:1263-1271, removeEffects).
 */
let DEBUFF: { on: boolean; pct: Record<number, { dh: number; idt: number; rounds: number }> } = { on: false, pct: {} };
const eruptDebuff = (act: number) => {
  const d = DEBUFF.on ? DEBUFF.pct[act] : undefined;
  if (!d) return [];
  return [tag("decreaseheal", { power: d.dh, rounds: d.rounds, calculation: "percentage", friendlyFire: "ENEMIES", description: "The glass remembers you" }),
    T.pct("increasedamagetaken", d.idt, d.rounds, { friendlyFire: "ENEMIES", description: "The glass remembers you" })];
};

/* ------------------------------------------------------------------ records */
export const buildRecords = (P: MoeParams) => {
  CARRIER_ON = P.telegraphCarrier !== false;
  P_NO_REENTRY = !!P.noPoolReentry;
  RAMP_CLEARABLE = !!P.rampClearable;
  POOL_AWARE = !!P.poolAware;
  DEBUG_TRACE = !!(P as any).debugTrace;
  A3_ON = !!a3(P).on; A3_POLICY = a3(P);
  MARK_ART = P.markArtRounds ?? 1;
  SKILLED = !!P.skilledPolicy;
  DEBUFF = { on: !!P.eruptDebuff?.on, pct: { 1: P.eruptDebuff?.act1, 2: P.eruptDebuff?.act2, 3: P.eruptDebuff?.act3 } as any };
  ERUPT = { on: !!P.eruption?.on, hp: P.eruption?.hp ?? 31500, pct: { 1: P.eruption?.act1 ?? 40, 2: P.eruption?.act2 ?? 60, 3: P.eruption?.act3 ?? 80 }, recast: P.eruption?.recast };
  const J: Record<string, any> = {};
  const add = (id: string, f: Parameters<typeof jutsu>[1]) => { J[id] = jutsu(id, f); return id; };
  const p = P.pw;
  /* ---- shared ---- */
  add(JID.lancet, { name: "Glass Lancet", description: "A needle of skyglass, thrown hard.", battleDescription: "%user flicks a lancet of glass at %target.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: P.lancetCd ?? 1, actionCostPerc: 60, effects: [heavy(p.lancet, "moe_lancet"),
    // Pass 6 ramp (director 2026-11-04: a gradual clock instead of a wall): every Lancet also leaves her a lasting,
    // unclearable +ramp.pct% damage given. Each cast is a separate instance (BATTLE_TAG_STACKING, drizzle/constants.ts:1968;
    // util.ts:1352-1358) and in-battle increases multiply with no cap (process.ts:2225-2231), so her filler grows with
    // every Lancet she throws. Eruptions are pierce and ignore it (process.ts:497-511).
    // Director 2026-11-05 (fight script): the ramp is the act's "clear me" buff; rampClearable drops its clearprevent so a
    // Clear resets it (and her other clearable buffs).
    ...(P.ramp.pct ? [T.pct("increasedamagegiven", P.ramp.pct, P.ramp.rounds, { target: "SELF", description: "The glass hungers" }), ...(P.rampClearable ? [] : [tag("clearprevent", { power: 100, rounds: P.ramp.rounds, target: "SELF" })])] : [])] });
  add(JID.enrage, { name: "The Glass Remembers", description: "Enrage: every surface of the hall answers at once.", battleDescription: "Every pane in the hall turns toward you at once.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: field(cellsWhere(() => true)), effects: [heavy(p.enrage, "moe_enrage")] });
  /* ---- Act I: Sayo ---- */
  const mark = (id: string, name: string, cells: Cell[], mk: string, line: string, cost = 40, cd = P.refractCd) =>
    add(id, { name, description: "Refraction: lines of light from the walls; they shatter on her next turn.", battleDescription: line, target: "GROUND", method: "COORDINATES", range: 0, cooldown: cd, actionCostPerc: cost, coordinateTargeting: field(cells), effects: [carrier("tg_heavy"), marker(mk)] });
  mark(JID.refractA, "Refraction", PAT.refractA, MK.refractA, "%user draws three lines of light from the walls.");
  mark(JID.refractB, "Refraction", PAT.refractB, MK.refractB, "%user draws three lines of light from the walls.");
  add(JID.facet, { name: "Facet", description: "Below 60%: her Refraction is drawn with its mirror image (both line sets); they shatter on her next turn.", battleDescription: "The lines split. Their mirror image glows on the far side of the hall.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: P.refractCd, actionCostPerc: 40, coordinateTargeting: field([...PAT.refractA, ...PAT.refractB]), effects: [carrier("tg_heavy"), marker(MK.facet)] });
  const blast = (id: string, name: string, cells: Cell[], power: number, line: string, extra: any[] = []) =>
    add(id, { name, description: "The marked lines shatter.", battleDescription: line, target: "GROUND", method: "COORDINATES", range: 0, cooldown: P.act1BlastCd, actionCostPerc: 100, coordinateTargeting: field(cells), effects: [erupt(1, power, "moe_refraction"), ...extra] });
  blast(JID.blastA, "Refraction", PAT.refractA, p.refract, "The lines shatter.");
  blast(JID.blastB, "Refraction", PAT.refractB, p.refract, "The lines shatter.");
  blast(JID.facetBlast, "Facet", [...PAT.refractA, ...PAT.refractB], p.facet, "Both images shatter at once.");
  // Lucid (the Silence fell first): the blast also draws the second set, so Refraction fires twice.
  add(JID.lucidBlast, { name: "Lucid Refraction", description: "Lucid: the lines shatter and are drawn again at once.", battleDescription: "\"I can hear myself again.\" The lines shatter, and new ones are already drawn.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: P.act1BlastCd, actionCostPerc: 100, coordinateTargeting: field(PAT.refractA),
    effects: [erupt(1, p.refract, "moe_refraction"), carrier("tg_heavy", MARK_ART, field(PAT.refractB)), marker(MK.refractB)] });
  add(JID.lucidWake, { name: "Lucid", description: "With the Silence gone, Sayo hears herself again: her glass cuts deeper.", battleDescription: "\"I can hear myself again.\" Sayo straightens; every pane in the hall turns with her.", target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: 20, effects: idgTags(P.lucidIdg).map((e: any) => ({ ...e, rounds: 99, staticAnimation: "moe_lucid" })) });
  add(JID.likeness, { name: "Your Likeness", description: "Below 40%: she casts your impression from the glass for three rounds.", battleDescription: "\"Hold still. There. That is you.\" Your likeness steps out of the glass.", target: "EMPTY_GROUND", method: "SINGLE", range: 5, cooldown: 99, actionCostPerc: 60, donor: IN.donors.summon,
    effects: [tag("summon", { aiId: AI.likeness, aiHp: P.likeness.hp, power: P.likeness.power, rounds: P.likeness.rounds, appearAnimation: "moe_likeness" })] });
  add(JID.likenessStrike, { name: "Your Own Strike", description: "Your likeness strikes with your habits.", battleDescription: "%user strikes the way you would.", target: "OTHER_USER", method: "SINGLE", range: 4, cooldown: 0, actionCostPerc: 60, effects: [T.pierce(p.likenessHit)] });
  // Reused live record (pass 3 reuse audit): Stolen Form (copy 100, 3 rounds; range 4, 60 AP, cooldown 6), as-is.
  J[JID.likenessCopy] = { ...structuredClone(IN.jutsu[JID.likenessCopy]?.record ?? IN.oldKit[JID.likenessCopy]?.record), id: JID.likenessCopy };
  /* ---- Act I: the Silence ---- */
  const hushRec = (id: string, name: string, n: number, line: string, withDrain: boolean, cd: number, drainPct = p.hushDrain) =>
    add(id, { name, description: "The Hush: stilled pools seep up through the floor; standing in one drains you and nothing heals you.", battleDescription: line, target: "GROUND", method: "COORDINATES", range: 0, cooldown: cd, actionCostPerc: 40, coordinateTargeting: field(PAT.hushField, "RANDOM", "BATTLEFIELD", n),
      effects: [
        tag("healprevent", { power: 100, rounds: P.hushRounds, friendlyFire: "ENEMIES" }),
        withDrain ? tag("drain", { power: drainPct, rounds: P.hushRounds, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"], ...poolArt("tg_linger") })
          : T.pool(p.hushDmg, P.hushRounds, poolArt("tg_linger")),
        ...poolVis(P.hushRounds),
      ] });
  // drain is a shared-cooldown tag: the three Hush records lock each other for 3 rounds (every third turn).
  hushRec(JID.hush[0], "The Hush", P.hushCount, "Somewhere on the floor, sound stops.", true, 3, P.hushPoolDrain);
  hushRec(JID.hushUnbridled, "The Hush, Unbridled", P.hushUnbridledCount, "Unbridled, the quiet pours up out of the floor.", false, 1);
  const listen = (id: string, name: string, cd: number, line: string) =>
    add(id, { name, description: "The Listening: a feeler of the deep rises and listens for movement.", battleDescription: line, target: "EMPTY_GROUND", method: "SINGLE", range: 5, cooldown: cd, actionCostPerc: 40, donor: IN.donors.summon,
      effects: [tag("summon", { aiId: AI.feeler, aiHp: P.feeler.hp, power: P.feeler.power, rounds: P.feeler.rounds, appearAnimation: "moe_feeler" })] });
  listen(JID.listening, "The Listening", P.feeler.listeningCd, "Something under the floor turns toward the sound of you.");
  listen(JID.listeningUnbridled, "The Listening, Unbridled", 1, "It does not wait any more. Another feeler rises.");
  // Telegraphed Stillness: the Silence never moves, so its reach (every hex within 3 of its post) is a fixed pattern.
  // The blast is CHARACTER (it stuns) and its pattern holds the Silence's own hex, so it is always a valid cast.
  // Director 2026-11-05: Stillness is anchored to the Silence (she spawns at random and now moves): AOE_SPIRAL_SHOOT with
  // range 3 covers every hex within 3 of the caster, her own excluded (libs/combat/targeting.ts spiral around the caster).
  const stillGeo = P.stillAnchored ? { method: "AOE_SPIRAL_SHOOT", range: 3 } : { method: "COORDINATES", range: 0, coordinateTargeting: field(PAT.stillReach) };
  add(JID.stillness, { name: "Stillness", description: "The deep listens around the Silence: next turn, everything within 3 is crushed and stunned.", battleDescription: "The floor around the Silence goes still. Something is listening.", target: "GROUND", ...stillGeo, cooldown: P.still.cd, actionCostPerc: 40, effects: [carrier("tg_control"), marker(MK.still)] } as any);
  add(JID.stillnessBlast, { name: "Stillness", description: "Everything within 3 of the Silence is crushed and stunned.", battleDescription: "\"Be still.\"", target: "CHARACTER", ...stillGeo, cooldown: 2, actionCostPerc: 100,
    effects: [erupt(1, p.stillness, "moe_stillness"), tag("stun", { power: 100, rounds: P.still.stunRounds, apReduction: P.still.stunAp, friendlyFire: "ENEMIES" })] } as any);
  /* ---- the feeler ---- */
  add(JID.cradle, { name: "Cradle", description: "While a feeler lives, the Silence holds Sayo: 90% less damage taken, and the hold cannot be cleared.", battleDescription: "The Silence cradles %target. Blows slide off the glass.", target: "ALLY", method: "SINGLE", range: 5, cooldown: 1, actionCostPerc: 40, donor: "xs-8r_KRJS8QQMpBDyhUv",
    effects: [T.pct("decreasedamagetaken", p.cradleDR, 1, { target: "INHERIT", friendlyFire: "FRIENDLY", staticAnimation: "moe_cradle" }), tag("clearprevent", { power: 100, rounds: 1, target: "INHERIT", friendlyFire: "FRIENDLY" })] });
  add(JID.grasp, { name: "Grasp", description: "The feeler takes hold of whatever is nearest: rooted, and drained.", battleDescription: "%user closes around %target.", target: "OTHER_USER", method: "SINGLE", range: 2, cooldown: P.graspCd ?? 0, actionCostPerc: 60,
    effects: [T.pierce(p.grasp), T.root(1), tag("drain", { power: p.graspDrain, rounds: 2, calculation: "percentage", poolsAffected: ["Health"] })] });
  /* ---- Act II: Sayo (the Stilling) ---- */
  for (const k of Object.keys(PAT.etch)) {
    add(JID.etch[k]!, { name: "Etching", description: "She etches a pattern into the glass. It will remember.", battleDescription: "%user traces a pattern into the glass. It glows, then fades.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 40, coordinateTargeting: field(PAT.etch[k]!), effects: [carrier("tg_etch", 1)] }); // RUL-2026-11-02-101: readable for one full round
    add(JID.det[k]!, { name: "Recast", description: "The glass remembers an etching and detonates it, unmarked. While she recasts, her guard is open (x3 damage taken).", battleDescription: "The glass remembers.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: field(PAT.etch[k]!), effects: [erupt(2, p.detonate, "moe_recast", ERUPT.recast ?? ERUPT.pct[2]!), weaknessSelf(3)] });
  }
  // Etching turns: Etching (40 AP) + The Hush Rises (60 AP) = exactly 100 AP. Any leftover AP ends in the engine's
  // appended end turn, whose "wait" enters usedActions and breaks the combo (moe_probe P1b, first build). One record per
  // cycle: the Silence's pools grow in number and strength cycle by cycle, and each lasts 8 rounds, so they pile up.
  add(JID.rises[0]!, { name: "The Hush Rises", description: "While she etches, the Silence seeps up through the floor: stilled pools that drain and block healing, more of them every cycle.", battleDescription: "The floor stops making any sound in patches. The patches do not close.",
    target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 60, coordinateTargeting: field(PAT.risesField, "RANDOM", "BATTLEFIELD", P.rises.count),
    effects: [tag("healprevent", { power: 100, rounds: P.rises.rounds, friendlyFire: "ENEMIES" }), tag("drain", { power: P.rises.drain, rounds: P.rises.rounds, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"], ...poolArt("tg_linger") }), ...poolVis(P.rises.rounds)] });
  add(JID.quietFall, { name: "The Glass Falls Quiet", description: "The cycle ends; a Worn afterimage is raised in the lull.", battleDescription: "The glass falls quiet. Something worn steps out of it.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 20, coordinateTargeting: field(STARS), effects: [vis("moe_lull", 1), marker(MK.done, 2), marker(MK.counter, 99, 1)] });
  const raise = (id: string, name: string, ai: string, line: string) =>
    add(id, { name, description: `Raises one of the Worn: ${name.replace("Raise ", "")}.`, battleDescription: line, target: "EMPTY_GROUND", method: "SINGLE", range: 4, cooldown: 0, actionCostPerc: 60, donor: IN.donors.summon,
      effects: [tag("summon", { aiId: ai, aiHp: P.worn.hp, power: P.worn.power, rounds: P.worn.rounds, appearAnimation: "moe_worn" })] });
  raise(JID.summonPorter, "Raise the Gate Porter", AI.porter, "A gate porter steps out of the glass, still holding the door.");
  raise(JID.summonHana, "Raise Sister Hana", AI.hana, "Sister Hana steps out of the glass, hands already busy.");
  raise(JID.summonTomo, "Raise Cadet Tomo", AI.tomo, "Cadet Tomo steps out of the glass, rope in hand.");
  add(JID.porter, { name: "Doorward Sweep", description: "The porter sweeps the threshold: damage and a shove.", battleDescription: "%user sweeps the threshold clear.", target: "OTHER_USER", method: "SINGLE", range: 1, cooldown: 1, actionCostPerc: 60, effects: [T.pierce(p.porter), ...(P.porterPush ? [T.push(P.porterPush)] : [])] });
  add(JID.hana, { name: "Worn Mending", description: "Sister Hana tends Sayo, as she tended everyone.", battleDescription: "%user tends to %target.", target: "ALLY", method: "SINGLE", range: 5, cooldown: 0, actionCostPerc: 60, donor: "xs-8r_KRJS8QQMpBDyhUv", effects: [T.heal(p.hana, { friendlyFire: "FRIENDLY" })] });
  add(JID.tomo, { name: "Cadet's Tether", description: "Tomo throws a line and hauls: pulled 3 hexes.", battleDescription: "%user hauls %target in.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 1, actionCostPerc: 60, effects: [T.pierce(p.tomo), T.pull(3)] });
  /* ---- Act III: Sayo, Saint of Stillness ---- */
  add(JID.quiet, { name: "The Quiet", description: "She channels: you take more damage and heal less, stacking; while she channels it cannot be cleansed.", battleDescription: "%user closes her eyes. The hall goes very quiet.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 2, actionCostPerc: 60,
    effects: [heavy(p.quiet, "moe_quiet"), T.pct("increasedamagetaken", p.quietIdt, P.quietRounds), tag("decreaseheal", { power: p.quietIdt, rounds: P.quietRounds, calculation: "percentage" }), tag("cleanseprevent", { power: 100, rounds: 1 })] });
  // Shatterfall's mark stays NEW (pass 3: the live Omen: Fanned Lines carries its art on a visual, which the server drops
  // early; editing that shared record would ripple to its holders). Same 19-hex fan, with the carrier.
  add(JID.shatterMark, { name: "Shatterfall", description: "A fan of cracks runs out from her; it falls on her next turn.", battleDescription: "Cracks fan out from %user's feet.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 3, actionCostPerc: 40, coordinateTargeting: { origin: "CASTER", selection: "ALL", coordinates: FAN_OFFSETS, randomCount: 1 }, effects: [carrier("tg_heavy"), marker(MK.shatter)] });
  add(JID.shatterBlast, { name: "Shatterfall", description: "The fan falls.", battleDescription: "The fan of glass falls.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: 100, coordinateTargeting: { origin: "CASTER", selection: "ALL", coordinates: FAN_OFFSETS, randomCount: 1 }, effects: [erupt(3, p.shatter, "moe_shatterfall")] });
  add(JID.floodMark, { name: "Every Name in the Glass", description: "Every stilled name rises to the floor; only where the three refused stays dry.", battleDescription: "Every name in the glass rises at once. Three places stay dry: where the three refused.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: P.floodCd, actionCostPerc: 40, coordinateTargeting: field(PAT.flood),
    effects: [carrier("tg_heavy"), carrier("tg_safe", MARK_ART, field(STARS)), marker(MK.flood)] });
  add(JID.floodBlast, { name: "Every Name in the Glass", description: "The flood of names.", battleDescription: "The names flood the hall.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: 100, coordinateTargeting: field(PAT.flood), effects: [erupt(3, p.flood, "moe_flood")] });
  // RUL-2026-11-02-097 item 5 (addendum): healing REDUCTION, not healprevent. decreaseheal (percentage, power 100) cuts
  // heal_hp, lifesteal_hp, vampRatio and absorb_hp on the consequence whatever their source, gear lifesteal included
  // (tags.ts adjustHealGiven). It is laid as Hush ground over the whole floor, the three dry tiles included, so it
  // re-applies to whoever stands anywhere and a Cleanse only clears it until the next step (moe_probe P3b).
  add(JID.m2Entry, { name: "No One Is Mended", description: "For the whole of Every Name in the Glass, the Hush covers the floor: nothing mends.", battleDescription: "\"Nothing mends here. Nothing needs to.\" The quiet covers the whole floor.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 99, actionCostPerc: 20, coordinateTargeting: field(cellsWhere(() => true)),
    effects: [tag("decreaseheal", { power: 100, rounds: P.m2HealBlockRounds, calculation: "percentage", friendlyFire: "ENEMIES", ...poolArt("moe_hush_floor") }), tag("healprevent", { power: 100, rounds: P.m2HealBlockRounds, friendlyFire: "ENEMIES" })] });
  // Probe-only alternative (director's option b): the same rows cast on the player (target ALL), not ground.
  add(JID.m2EntryCast, { name: "No One Is Mended (cast)", description: "probe: option (b)", battleDescription: "probe", target: "CHARACTER", method: "ALL", range: 0, cooldown: 99, actionCostPerc: 20,
    effects: [tag("decreaseheal", { power: 100, rounds: P.m2HealBlockRounds, calculation: "percentage", friendlyFire: "ENEMIES" }), tag("healprevent", { power: 100, rounds: P.m2HealBlockRounds, friendlyFire: "ENEMIES" })] });
  // RUL-2026-11-02-099 item 2: Breathless Pull is a fixed, telegraphed stun. The mark (60 AP, so its blast cannot follow in
  // the same turn) covers every hex but the three dry tiles; on her next turn the pull and the stun land on everyone still
  // in it (stun power 100, only stunprevent resists), and the flood is marked in the same turn (gated on the blast's own
  // marker). A player who is not stun-immune must reach a dry tile a turn early; an immune one can keep fighting.
  add(JID.pullMark, { name: "Breathless Pull", description: "She breathes in. Next turn, everyone not standing where the three refused is drawn in and loses their breath.", battleDescription: "%user breathes in. The air leaves the hall, except where the three refused.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: P.pullCd, actionCostPerc: 60, coordinateTargeting: field(PAT.flood),
    effects: [carrier("tg_control"), carrier("tg_safe", MARK_ART, field(STARS)), marker(MK.pull)] });
  add(JID.pull, { name: "Breathless Pull", description: "The breath she took is spent: everyone off the dry tiles is drawn toward her and stunned.", battleDescription: "%user exhales. Everyone she can reach is drawn toward her, breathless.", target: "CHARACTER", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: 60, coordinateTargeting: field(PAT.flood),
    effects: [T.damage(P.pw.pullDmg, { appearAnimation: "moe_breathless" }), T.pull(P.pullDist), tag("stun", { power: 100, rounds: 1, apReduction: P.pullStunAp, friendlyFire: "ENEMIES" }), marker(MK.breath)] });
  add(JID.starHush, { name: "The Hush", description: "The Hush seeps into one of the three dry places.", battleDescription: "The quiet seeps into one of the dry places.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: P.starHush.cd, actionCostPerc: 40, coordinateTargeting: field(STARS, "RANDOM", "BATTLEFIELD", 1),
    effects: [tag("healprevent", { power: 100, rounds: P.starHush.rounds, friendlyFire: "ENEMIES" }), tag("drain", { power: p.hushDrain, rounds: P.starHush.rounds, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"], ...poolArt("tg_linger") }), ...poolVis(P.starHush.rounds)] });
  add(JID.longHush, { name: "The Long Hush", description: "Below 25%: she cannot fall for 6 rounds; the glass begins to fall.", battleDescription: "\"Not yet. You are almost a good impression.\" The ceiling begins to fall.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 99, actionCostPerc: 40, coordinateTargeting: field(PAT.glass[0]!),
    effects: [tag("finalstand", { power: 100, rounds: 6, target: "SELF" }), carrier("tg_heavy"), marker(MK.gA), marker(MK.firstPass, 3)] });
  const gfMk = [MK.gA, MK.gB, MK.gC];
  const gf = (id: string, k: number, nextMk: string, extra: Cell[] = [], line = "Glass falls.") =>
    add(id, { name: "Glassfall", description: "The marked third of the hall is crushed; the next third is marked.", battleDescription: line, target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 100, coordinateTargeting: field([...PAT.glass[k]!, ...extra.filter((c) => !PAT.glass[k]!.some((g) => key(g) === key(c)))]),
      effects: [erupt(3, extra.length ? Math.max(p.glass, p.recastIII) : p.glass, "moe_glassfall"), carrier("tg_heavy", MARK_ART, field(PAT.glass[(k + 1) % 3]!)), marker(nextMk)] });
  gf(JID.glass[0]!, 0, gfMk[1]!);
  gf(JID.glass[1]!, 1, gfMk[2]!);
  gf(JID.glass[2]!, 2, gfMk[0]!);
  gf(JID.glassFirstB, 1, MK.gCs);
  // Round 4 of the Long Hush: the C third falls and, unmarked, one Act II etching (the heart of the hall) is recast.
  gf(JID.glassRecast, 2, gfMk[0]!, PAT.etch.D!, "Glass falls, and the glass remembers one more etching.");
  for (const [id, t] of Object.entries(FINAL_TEXT)) if (J[id]) { J[id].battleDescription = t.line; if (t.name) J[id].name = t.name; }
  if (P.cooldownFloor) for (const r of Object.values(J)) if (r.cooldown < P.cooldownFloor) r.cooldown = P.cooldownFloor;
  // Pass 6 (5,050 HP players): scale every formula hit on the boss side (not the fixed eruptions, not the %-drains, not
  // Breathless Pull, which stays as is) by bossDmgScale, a multiplier on effect power (damage is linear in power:
  // tags.ts powerEffect epScale = power / ep_normalization).
  if (DEBUFF.on) {
    // Option 4 (director 2026-11-04). Act II: the five Recasts become CHARACTER casts with Sayo's own post (7,5) in the
    // pattern, so a cast is always valid (actions.ts refuses a CHARACTER cast with no unit on its hexes); the debuff lands on
    // the player with its own rounds. Her own hex is never hit (friendlyFire ENEMIES). Nothing Moves already holds the
    // Silence's hex. Acts I and III: the eruption stays GROUND and leaves a heal-block + damage-taken pool on its own
    // pattern hexes only (ground tags are placed on the cast's pattern, actions.ts:1063-1100), drawn as a lingering pool.
    const pool = (act: number) => {
      const d = DEBUFF.pct[act]; if (!d) return [];
      return [tag("decreaseheal", { power: d.dh, rounds: d.poolRounds ?? d.rounds, calculation: "percentage", friendlyFire: "ENEMIES", description: "The broken glass", ...poolArt("tg_linger") }),
        T.pct("increasedamagetaken", d.idt, d.poolRounds ?? d.rounds, { friendlyFire: "ENEMIES", description: "The broken glass" })];
    };
    const SAYO2_POST: Cell = [7, 5];
    // Live calibration (2026-11-05): the server seats Sayo II on a random cell of the right spawn block (x 8-9, y 1-7,
    // routers/combat.ts:3867-3880), never on (7,5), so a CHARACTER Recast with nobody on its hexes is refused
    // (actions.ts:1009-1021 -> ActionNotPossibleError, actions.ts:1421-1425) and her combo stalls on Etching (sim with
    // liveSpawn: 42 marks, 0 Recasts). recastGround keeps the Recasts GROUND on their etched pattern (always valid) and
    // lays the debuff as a pool on that pattern, like Acts I and III; at 6,500 a Recast is lethal, so the debuff only ever
    // met a dead player anyway.
    for (const id of Object.values(JID.det)) {
      const r = J[id]!;
      if (P.recastGround) { r.effects.push(...pool(2)); continue; }
      r.target = "CHARACTER";
      const cs = r.coordinateTargeting.coordinates;
      if (!cs.some((c: any) => c.longitude === SAYO2_POST[0] && c.latitude === SAYO2_POST[1])) cs.push({ longitude: SAYO2_POST[0], latitude: SAYO2_POST[1] });
      r.effects.push(...eruptDebuff(2));
    }
    J[JID.stillnessBlast]!.effects.push(...eruptDebuff(1));
    for (const id of [JID.blastA, JID.blastB, JID.facetBlast, JID.lucidBlast]) J[id]!.effects.push(...pool(1));
    for (const id of [JID.shatterBlast, JID.floodBlast, ...JID.glass, JID.glassFirstB, JID.glassRecast]) J[id]!.effects.push(...pool(3));
  }
  if (P.turnMark.on) {
    /**
     * Pass 6 player-anchored mark (director 2026-11-04 live feedback: a safe spot must not stay safe). A GROUND cast
     * centred on the tile the AI picks for CLOSEST_OPPONENT (AOE_CIRCLE_SPAWN: the target hex and its ring,
     * libs/combat/targeting.ts:33-35), drawn with the heavy tile, holding a Health drain as a % of max HP. The drain
     * does nothing on its cast round (tags.ts:2152-2156: !isNew && !castThisRound) and, as a ground effect, reaches a
     * unit only while it stands on the hex (process.ts:395-412) on that unit's own action: stay and it lands next turn,
     * step off and it misses. Telegraphed one turn ahead, follows the player, no new blast record needed.
     */
    const turn = (id: string, name: string, pct: number, line: string) => add(id, { name, description: "The floor under you goes still; it breaks next turn unless you move.", battleDescription: line, target: "GROUND", method: "AOE_CIRCLE_SPAWN", range: 5, cooldown: P.turnMark.cd, actionCostPerc: 40,
      effects: [carrier("tg_heavy", 1), tag("drain", { power: pct, rounds: 1, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"], description: "The floor breaks" })] });
    turn(JID.turnI, "The Silence Turns", P.turnMark.act1, "The floor under %target goes still. Something below has turned toward it.");
    turn(JID.turnII, "The Glass Turns", P.turnMark.act2, "The glass under %target remembers the weight of you.");
  }
  // Director 2026-11-05 (approved): Act I spacing. The marks (Refraction, Far Refraction, Facet) get cooldown 6 and a
  // SELF cleanseprevent, itself a shared-cooldown tag (drizzle/constants.ts:261-279), so casting one mark locks the other
  // marks for SHARED_COOLDOWN_ROUNDS = 3 (actions.ts:1461-1490). Marks therefore come at least 3 rounds apart and each
  // blast (1 round after its mark, cooldown kept) always falls after the previous blast's 3-round pierce lock: mark A,
  // blast A, rest, mark B, blast B, rest. Lucid Refraction no longer redraws the far set in the same action (its follow-up
  // blast would sit inside its own pierce lock); Lucid keeps its +20% and rest-free blasts.
  if (P.act1Spacing) {
    for (const id of [JID.refractA, JID.refractB, JID.facet]) { J[id]!.cooldown = 6; J[id]!.effects.push(tag("cleanseprevent", { power: 100, rounds: 1, target: "SELF", description: "The glass holds its breath" })); }
    J[JID.lucidBlast]!.effects = J[JID.lucidBlast]!.effects.filter((e: any) => !(e.type === "increaseregeneration" || e.type === MK.refractB));
  }
  // GCD fix (2026-11-05 trace, Silence-first seed 18): pierce is a shared-cooldown tag (drizzle/constants.ts:261-279;
  // applyActionCooldowns, actions.ts:1461-1490): casting any action with cooldown > 0 that carries pierce locks every
  // other pierce action of the caster for SHARED_COOLDOWN_ROUNDS = 3. Every eruption is pierce, so Refraction Breaks
  // (cooldown 2) locked Far Refraction Breaks: its mark expired unblasted, or it fell a turn late with no art up (traced:
  // 0 of 27 hexes drawn). With cooldown 0 a blast imposes no lock (applyGcd needs cooldown > 0); each blast stays gated
  // by its mark's marker.
  if (P.gcdSafeBlasts) for (const id of [JID.blastA, JID.blastB, JID.facetBlast, JID.lucidBlast, JID.stillnessBlast, JID.shatterBlast, JID.floodBlast]) J[id]!.cooldown = 0;
  if (P.etchDWide) J[JID.det.D!]!.coordinateTargeting = field(cellsWhere((c, r) => c >= 4 && r >= 3 && r <= 6));
  // Director 2026-11-05 (proposal, awaiting approval): a real, thematic SELF buff per boss, POSITIVE power only (the client
  // cannot draw negative-power tags), riding a move the boss opens the act with and repeats, so it is refreshed all act.
  // Each cast is a separate instance (BATTLE_TAG_STACKING, drizzle/constants.ts:1968); rounds are kept near the move's
  // repeat period so at most ~2 instances overlap. bossAura: { sayo1, silence, sayo2, saint }: { type, power | health, rounds }.
  if (P.bossAura?.on) {
    const aura = (a: any, desc: string) => a.type === "shield" ? tag("shield", { power: 100, health: a.health, rounds: a.rounds, target: "SELF", description: desc })
      : tag(a.type, { power: a.power, rounds: a.rounds, target: "SELF", calculation: "percentage", description: desc });
    const put = (ids: string[], a: any, desc: string) => { if (a) for (const id of new Set(ids)) J[id]!.effects.push(aura(a, desc)); };
    put([JID.refractA, JID.refractB, JID.facet], P.bossAura.sayo1, "Heartglass: every pane turns your light back at you");
    put([JID.hush[0]!, JID.hushUnbridled], P.bossAura.silence, "The deep drinks the sound of every blow");
    put(Object.values(JID.etch), P.bossAura.sayo2, "The Stilling: an etched pane holds in front of her");
    put([JID.shatterMark], P.bossAura.saint, "The Remainder: the black glass feeds on what it cuts");
  }
  // Art pass simulation (2026-11-05): visual-only "piece" tags on the signature moves (no gameplay handler); the
  // generator on main adds the real ones at build time. Sim-only switch for the fixed-seed identity check.
  const A3 = a3(P);
  if (A3.on) {
    // Phase I lines break every turn, so their pools last A3.linePoolRounds (1, like Act I's): 3-round pools on both line
    // sets carpeted the floor and a pool-aware player (sim agent 3eb8abab) could no longer walk to her (4 of 20 stalls).
    const pool3 = (rounds?: number) => {
      const d = DEBUFF.on ? DEBUFF.pct[3] as any : undefined;
      if (!d) return [];
      const r = rounds ?? d.poolRounds ?? d.rounds;
      return [tag("decreaseheal", { power: d.dh, rounds: r, calculation: "percentage", friendlyFire: "ENEMIES", description: "The broken glass", ...poolArt("tg_linger") }),
        T.pct("increasedamagetaken", d.idt, r, { friendlyFire: "ENEMIES", description: "The broken glass" })];
    };
    const ground = (id: string, name: string, line: string, desc: string, cells: Cell[], cost: number, cd: number, effects: any[]) =>
      add(id, { name, description: desc, battleDescription: line, target: "GROUND", method: "COORDINATES", range: 0, cooldown: cd, actionCostPerc: cost, coordinateTargeting: field(cells), effects });
    const facetCells = unionCells(PAT.refractA, PAT.refractB);
    const notStars = PAT.flood;
    /* Phase I: Lucid */
    ground(J3.opener, "Refraction", "\"Hold still. I want to see you in the light.\" Three lines of black glass run in from the walls.", "Three lines of glass; they break on her next turn, and she draws the next lines as they break.", PAT.refractA, 60, A3.openerCd, [carrier("tg_heavy", 1), marker(MK3.a)]);
    ground(J3.lucid, "Lucid Refraction", "The lines break, and three more are already drawn.", "The marked lines break; the far lines are drawn in the same breath.", PAT.refractA, 60, 0,
      [erupt(3, p.refract, "moe_shatterfall"), ...pool3(A3.linePoolRounds), carrier("tg_heavy", 1, field(PAT.refractB)), marker(MK3.b)]);
    ground(J3.facet, "Facet", "\"Every line has a reflection.\" The far lines break, and both images are drawn at once.", "The far lines break; both line sets and their mirror are drawn. Only the gaps are safe.", PAT.refractB, 60, 0,
      [erupt(3, p.refract, "moe_shatterfall"), ...pool3(A3.linePoolRounds), carrier("tg_heavy", 1, field(facetCells)), marker(MK3.f)]);
    ground(J3.facetBreak, "Facet Breaks", "Both images break at once, and for a moment her guard hangs open.", "Both images break. Her guard is open for a moment afterwards.", facetCells, 60, 0,
      [erupt(3, p.refract, "moe_shatterfall"), ...pool3(A3.linePoolRounds), weaknessSelf(A3.guardFacet), marker(MK3.clean)]);
    // A three-hex bar through the player (origin TARGET). Not Act I's radius-1 ring: a ground drain is copied onto whoever
    // ends an action on it and that copy lasts the round (process.ts:395-412), so walking out of a ring takes two actions
    // and two drains unless Replacement (cooldown 2) is up; the lines already spend Replacement. Any side step clears a bar.
    add(J3.holdStill, { name: "Hold Still", description: "The glass north and south of you goes still. Anyone who steps onto it there will wish they had held still.", battleDescription: "\"Hold still.\" The glass either side of %target goes quiet.", target: "GROUND", method: "COORDINATES", range: 5, cooldown: 0, actionCostPerc: 40,
      coordinateTargeting: { origin: "TARGET", selection: "ALL", coordinates: A3_CROSS(A3.barArm), randomCount: 1 },
      effects: [carrier("tg_heavy", 1), tag("drain", { power: A3.holdStillPct, rounds: 1, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"], description: "The floor breaks" })] });
    add(J3.silenceHolds, { name: "The Silence Holds Her", description: "The Silence folds around her: she takes far less damage and drinks what does land, and the floor within 3 of her goes still. There is no feeler to cut. The hold is hers, and a clean break would shatter it.", battleDescription: "The Silence folds around %user. The floor around her goes still.", target: "GROUND", method: "AOE_SPIRAL_SHOOT", range: 3, cooldown: A3.cradleCd, actionCostPerc: 40,
      effects: [carrier("tg_control", 1), marker(MK3.still), T.pct("decreasedamagetaken", A3.cradleDR, A3.cradleRounds, { target: "SELF", description: "The Silence holds her" }),
        tag("absorb", { power: A3.cradleAbsorb, rounds: A3.cradleRounds, target: "SELF", calculation: "percentage", description: "The deep drinks every blow", staticAnimation: "moe_cradle" })] } as any);
    add(J3.nothingMoves, { name: "Nothing Moves", description: "Everything within 3 of her is crushed and stunned.", battleDescription: "For a moment nothing near her moves. Nothing can.", target: "CHARACTER", method: "AOE_SPIRAL_SHOOT", range: 3, cooldown: 0, actionCostPerc: 40,
      effects: [T.pierce(A3.stillPierce, { calculation: "static", dmgModifier: 1, description: "Pierces target", appearAnimation: "moe_stillness" }), tag("stun", { power: 100, rounds: 1, apReduction: A3.stillStunAp, friendlyFire: "ENEMIES" })] } as any);
    add(J3.lancet, { name: "Remainder Lancet", description: "A needle of black glass. Each one steadies her hand; a clean break washes the steadiness away.", battleDescription: "%user flicks a lancet of black glass at %target.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: A3.lancetCd, actionCostPerc: A3.lancetCost,
      effects: [heavy(p.lancet, "moe_lancet"), ...(P.ramp.pct ? [T.pct("increasedamagegiven", P.ramp.pct, P.ramp.rounds, { target: "SELF", description: "The glass hungers" })] : [])] });
    /* Phase II: Every Name, Remembered */
    ground(J3.stir, "The Names Stir", "The names press up against the glass from below. \"Soon nothing here will mend. Except where the three refused.\"", "A warning: when she is pushed below 60%, nothing mends anywhere but the three dry places.", notStars, 20, 99, [carrier("moe_hush_floor", 1)]);
    ground(J3.mended, "No One Is Mended", "\"Nothing mends here. Nothing needs to.\" The quiet covers the floor, everywhere but where the three refused.", "Nothing mends anywhere but the three dry places.", notStars, 100, 99,
      [tag("decreaseheal", { power: 100, rounds: A3.mendedRounds, calculation: "percentage", friendlyFire: "ENEMIES" }), tag("healprevent", { power: 100, rounds: A3.mendedRounds, friendlyFire: "ENEMIES", ...poolArt("moe_hush_floor") }), marker(MK3.phase, 99, 1)]);
    const EN: Record<string, string> = { A: "Rime", B: "Ember", D: "Heart", C: "Seam" };
    for (const k of Object.keys(J3.etch)) {
      ground(J3.flood[k]!, `The Names Flood In: ${EN[k]}`, `Every name in the glass floods the hall, and the glass remembers the ${EN[k]!.toLowerCase()}. She has nothing left to breathe; her guard hangs open.`, "Everything but the three dry places floods, and so does the etching she drew two turns ago. Her guard is open afterwards.",
        unionCells(notStars, PAT.etch[k]!), 100, 0, [erupt(3, p.flood, "moe_flood"), weaknessSelf(A3.guardFlood)]);
    }
    ground(J3.everyName, "Every Name in the Glass", "\"Do you hear them? Every one of them stayed.\" The names rise. Three places stay dry: where the three refused.", "Every name rises; next turn they flood everything but the three dry places.", notStars, 100, 0,
      [carrier("tg_heavy", 1), carrier("tg_safe", 1, field(STARS))]);
    add(J3.rises, { name: "The Hush Rises", description: "Stilled pools seep up through the floor.", battleDescription: "The floor stops making any sound in patches.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 60, coordinateTargeting: field(PAT.risesField, "RANDOM", "BATTLEFIELD", A3.rises.count),
      effects: [tag("healprevent", { power: 100, rounds: A3.rises.rounds, friendlyFire: "ENEMIES" }), tag("drain", { power: A3.rises.drain, rounds: A3.rises.rounds, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"], ...poolArt("tg_linger") })] });
    add(J3.starHush, { name: "Hush Where They Refused", description: "The quiet seeps into one of the three dry places.", battleDescription: "The quiet finds one of the dry places where the three refused.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 0, actionCostPerc: 40, coordinateTargeting: field(STARS, "RANDOM", "BATTLEFIELD", 1),
      effects: [tag("healprevent", { power: 100, rounds: A3.starHush.rounds, friendlyFire: "ENEMIES" }), tag("drain", { power: A3.starHush.drain, rounds: A3.starHush.rounds, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"], ...poolArt("tg_linger") }), marker(MK3.cycleEnd)] });
    /* Phase III: A Good Impression */
    const gMk = [MK3.gA, MK3.gB, MK3.gC];
    const paneMk = (k: number) => marker(gMk[k]!);
    ground(J3.impression, "A Good Impression", "\"There. Hold still, and you will make a good impression.\" The ceiling cracks, and the glass begins to remember everything.", "Below 25%: every turn a third of the ceiling falls with an echo of the fight, and the next is marked. She holds nothing back, so her guard stays open.", A3_PANE(A3, 0), 60, 99,
      [carrier("tg_heavy", 1), paneMk(0), marker(MK3.phase, 99, 1)]);
    const echoName = (k: string) => (k === "refractA" ? "the first lines she ever drew" : k === "refractB" ? "the far lines" : `the ${EN[k]!.toLowerCase()}`);
    for (let k = 0; k < 3; k++) {
      const n = (k + 1) % 3;
      ground(J3.pane[k]!, `Glassfall: ${["First", "Second", "Last"][k]} Echo`, `A third of the ceiling falls, and with it ${echoName(A3.echoes[k]!)}. The next pane cracks.`, "The marked pane falls with its echo; the next is marked. Her guard is open.", A3_PANE(A3, k), 60, 0,
        [erupt(3, p.glass, "moe_glassfall"), ...pool3(), weaknessSelf(A3.guardPane), carrier("tg_heavy", 1, field(A3_PANE(A3, n))), paneMk(n)]);
    }
    add(J3.everyLine, { name: "Every Line Through You", description: "A line of glass runs north and south through where you stand. Step onto it and it takes you.", battleDescription: "\"Hold still.\" Every line in the hall runs through %target.", target: "GROUND", method: "COORDINATES", range: 5, cooldown: 0, actionCostPerc: 40,
      coordinateTargeting: { origin: "TARGET", selection: "ALL", coordinates: A3_CROSS(A3.lineArm), randomCount: 1 },
      effects: [carrier("tg_heavy", 1), tag("drain", { power: A3.everyLinePct, rounds: 1, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"], description: "The lines break" })] });
  }
  // Act III v2 text pass (push/mother_of_echoes_act3_text.json, pending director approval), keyed by spec id.
  if (A3.on) {
    const f = join(process.env.TNR_REPO!, "push/mother_of_echoes_act3_text.json");
    let A3_TEXT: Record<string, { name?: string; description?: string; battleDescription?: string }> = {};
    try { A3_TEXT = JSON.parse(readFileSync(f, "utf8")).jutsu ?? {}; } catch { A3_TEXT = {}; }
    for (const [id, t] of Object.entries(A3_TEXT)) if (J[id]) { if (t.name) J[id].name = t.name; if (t.description) J[id].description = t.description; if (t.battleDescription) J[id].battleDescription = t.battleDescription; }
  }
  if (P.visualPieces) for (const id of [JID.floodMark, JID.floodBlast, JID.shatterBlast, ...JID.glass, JID.glassFirstB, JID.glassRecast, JID.enrage, ...Object.values(JID.det)]) J[id]?.effects.push(vis("moe_piece", 1));
  const SUMMON_HITS = new Set([JID.grasp, JID.likenessStrike, JID.porter, JID.tomo]);
  for (const [id, r] of Object.entries<any>(J)) if (id !== JID.pull) for (const e of r.effects) if ((e.type === "damage" || e.type === "pierce") && e.calculation === "formula") {
    const k = P.bossDmgScale * (SUMMON_HITS.has(id) ? P.summonDmgScale : 1);
    if (k !== 1) e.power = Math.max(1, Math.round(e.power * k));
  }
  return J;
};

/** The live Omen: Fanned Lines (push/342 payload) as a full record. */
const fannedLines = () => {
  const doc = JSON.parse(readFileSync(join(process.env.TNR_HARNESS!, "data/fanned_lines_push342.json"), "utf8"));
  return { ...structuredClone(capturedJutsu("3v9c1SHlD2GLPF2HW1_Sc").record), ...structuredClone(doc.data), id: doc.id, reskinParentJutsuId: null, bloodlineReskinId: null, parentJutsuId: null, requiredBloodlineItemId: null };
};
/**
 * Final player-facing names and battle lines (pass 3, build-ready). Voices: Sayo is quiet and precise; the Silence has no
 * voice, so its lines narrate absence; the Worn speak in the habits of Crownhold. Applied over the records' working text.
 */
export const FINAL_TEXT: Record<string, { name?: string; line: string }> = {
  "moe-glass-lancet": { line: "%user lifts one finger. A lancet of glass leaves the wall and finds %target." },
  "moe-the-glass-remembers": { line: "Every pane in the hall turns toward you at once. The glass has remembered all of you." },
  "moe-refraction": { name: "Refraction", line: "\"Three lines. Mind them.\" Light runs in from the walls." },
  "moe-refraction-ii": { name: "Far Refraction", line: "\"Three more.\" Light runs in from the far walls." },
  "moe-refraction-blast": { name: "Refraction Breaks", line: "The lines of light shatter where they lie." },
  "moe-refraction-blast-ii": { name: "Far Refraction Breaks", line: "The far lines shatter where they lie." },
  "moe-facet": { name: "Facet", line: "\"Every line has a reflection.\" The lines are drawn again, mirrored across the hall." },
  "moe-facet-blast": { name: "Facet Breaks", line: "Both images shatter at once." },
  "moe-lucid-refraction": { line: "The lines shatter, and new ones are already drawn. \"I can see it clearly now.\"" },
  "moe-lucid": { line: "The hall is suddenly very loud. %user straightens. \"I can hear myself again.\"" },
  "moe-your-likeness": { line: "\"Hold still. There. That is you.\" Your likeness steps out of the glass." },
  "moe-likeness-strike": { line: "%user strikes exactly the way you would." },
  "moe-hush": { name: "The Hush", line: "Somewhere on the floor, sound stops. It does not come back." },
  "moe-hush-unbridled": { line: "Nothing holds the quiet back now. It pours up out of the floor." },
  "moe-listening": { line: "Something under the floor turns toward the sound of you." },
  "moe-listening-unbridled": { line: "It no longer waits to hear you. Another feeler rises." },
  "moe-stillness": { name: "Stillness", line: "The floor around the Silence goes still. Nothing there is moving, and soon nothing will." },
  "moe-stillness-blast": { name: "Nothing Moves", line: "For a moment nothing near the Silence moves. Nothing can." },
  "moe-cradle": { line: "The deep closes around %target. Blows slide off the glass." },
  "moe-feeler-grasp": { line: "%user closes around %target without a sound." },
  "moe-etching-a": { name: "Etching: Rime", line: "%user traces the north of the hall into the glass. It rimes over, then fades." },
  "moe-etching-b": { name: "Etching: Ember", line: "%user traces the south of the hall into the glass. It glows like an ember, then fades." },
  "moe-etching-c": { name: "Etching: Seam", line: "%user traces a seam down the west wall. It glows, then fades." },
  "moe-etching-d": { name: "Etching: Heart", line: "%user traces the heart of the hall into the glass. It beats once, then fades." },
  "moe-etching-e": { name: "Etching: Hail", line: "%user taps a scatter of points into the glass, like hail. They glow, then fade." },
  "moe-recast-a": { name: "Recast: Rime", line: "The glass remembers the rime, and the north of the hall breaks." },
  "moe-recast-b": { name: "Recast: Ember", line: "The glass remembers the ember, and the south of the hall breaks." },
  "moe-recast-c": { name: "Recast: Seam", line: "The glass remembers the seam, and the west wall breaks." },
  "moe-recast-d": { name: "Recast: Heart", line: "The glass remembers the heart, and the middle of the hall breaks." },
  "moe-recast-e": { name: "Recast: Hail", line: "The glass remembers the hail, and every point breaks at once." },
  "moe-hush-rises": { line: "The floor stops making any sound in patches. The patches do not close." },
  "moe-the-glass-falls-quiet": { line: "%user lowers her hand. \"Again.\" Something worn steps out of the glass." },
  "moe-raise-gate-porter": { line: "The gate porter steps out of the glass, still holding a door that is not there." },
  "moe-raise-sister-hana": { line: "Sister Hana steps out of the glass, hands already busy with someone else's wounds." },
  "moe-raise-cadet-tomo": { line: "Cadet Tomo steps out of the glass, rope in hand, waiting for an order." },
  "moe-worn-cleave": { line: "\"Gate's closed.\" %user sweeps the threshold clear." },
  "moe-worn-mending": { line: "\"Hold still, it's nearly done.\" %user tends to %target." },
  "moe-worn-tether": { line: "\"Line's secure!\" %user hauls %target in." },
  "moe-the-quiet": { line: "%user closes her eyes. The hall goes very quiet, and you go quiet with it." },
  "moe-shatterfall": { name: "Shatterfall", line: "Cracks fan out from %user's feet." },
  "moe-shatterfall-blast": { name: "Shatterfall Gives Way", line: "The fan of cracks gives way, and the glass beneath it falls." },
  "moe-every-name-in-the-glass": { name: "Every Name in the Glass", line: "\"Do you hear them? Every one of them stayed.\" The names rise. Three places stay dry: where the three refused." },
  "moe-every-name-blast": { name: "The Names Flood In", line: "Every name in the glass floods the hall." },
  "moe-no-one-is-mended": { line: "\"Nothing mends here. Nothing needs to.\" The quiet covers the whole floor." },
  "moe-breathless-pull-mark": { name: "The Held Breath", line: "%user breathes in. The air leaves the hall, except where the three refused." },
  "moe-breathless-pull": { name: "Breathless Pull", line: "%user breathes out, and everyone she can reach comes with it, breathless." },
  "moe-hush-on-the-refused": { name: "Hush Where They Refused", line: "The quiet finds one of the dry places where the three refused." },
  "moe-the-long-hush": { line: "\"Not yet. You are almost a good impression.\" The ceiling begins to fall." },
  "moe-glassfall-a": { name: "Glassfall: First Pane", line: "A third of the ceiling comes down, and the next pane cracks." },
  "moe-glassfall-b": { name: "Glassfall: Second Pane", line: "Another third of the ceiling comes down, and the next pane cracks." },
  "moe-glassfall-c": { name: "Glassfall: Last Pane", line: "The last third of the ceiling comes down, and the first pane cracks again." },
  "moe-glassfall-b-first": { name: "Glassfall: Opening Pane", line: "The second third of the ceiling comes down first, and the last pane cracks." },
  "moe-glassfall-recast": { name: "Glassfall: Heart Recast", line: "The ceiling comes down, and the glass remembers the heart once more." },
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
  R.jutsu(JID.lucidWake, "SELF", [COND.lucid]),
  R.jutsu(JID.facetBlast, "SELF", [C.has(MK.facet)]),
  R.jutsu(JID.lucidBlast, "SELF", [COND.lucid, C.has(MK.refractA)]),
  R.jutsu(JID.blastA, "SELF", [C.has(MK.refractA)]),
  R.jutsu(JID.blastB, "SELF", [C.has(MK.refractB)]),
  R.jutsu(JID.likeness, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [C.hb(40), C.noSummon()]),
  // After a mark (its marker is on her the same turn): a lancet, then end turn (never two marks, never two markers).
  R.jutsu(JID.lancet, PL, [C.has(MK.refractA), C.near(5)]),
  R.jutsu(JID.lancet, PL, [C.has(MK.refractB), C.near(5)]),
  R.jutsu(JID.lancet, PL, [C.has(MK.facet), C.near(5)]),
  R.end([C.has(MK.refractA)]),
  R.end([C.has(MK.refractB)]),
  R.end([C.has(MK.facet)]),
  // Below 60%, Facet takes the place of Refraction while it is ready (one marker at a time: moe_probe seed 23 showed a
  // second live marker outliving its visual when the first blast spent the next turn).
  R.jutsu(JID.facet, "SELF", [C.hb(60)]),
  R.jutsu(JID.refractA, "SELF", []),
  R.jutsu(JID.refractB, "SELF", P.act1Spacing ? [COND.rg(3)] : []),
  R.jutsu(JID.lancet, PL, [C.near(5)]),
  { conditions: [C.far(6)], action: { type: "move_towards_opponent", target: PL, description: "Keep 5 hexes" } },
  basic([C.near(1)]),
  R.end(),
];
export const silenceRules = (P: MoeParams) => [
  R.jutsu(JID.enrage, "SELF", [COND.rg(P.enrage.act1)]),
  R.jutsu(JID.stillnessBlast, "SELF", [C.has(MK.still)]),
  // Unbridled (Sayo fell first): a feeler every turn one is missing, the Hush every turn instead of every third.
  R.jutsu(JID.listeningUnbridled, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [COND.unbridled, C.noSummon()]),
  R.jutsu(JID.hushUnbridled, "SELF", [COND.unbridled]),
  R.jutsu(JID.stillness, "SELF", [COND.unbridled, C.near(3)]),
  R.end([COND.unbridled]),
  // Director 2026-11-05: stagger Act I: the follow-the-player ring no earlier than round 4, the first Feeler no earlier than 2.
  ...(P.turnMark.on ? [R.jutsu(JID.turnI, "HIGHEST_MAX_HEALTH_OPPONENT", P.act1Stagger ? [COND.rg(3)] : [])] : []),
  R.jutsu(JID.hush[0]!, "SELF", []),
  R.jutsu(JID.listening, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [C.noSummon(), ...(P.act1Stagger ? [COND.rg(1)] : [])]),
  R.jutsu(JID.stillness, "SELF", [C.near(3)]),
  basic([C.near(1)]),
  // Director 2026-11-05: the Silence stalks the player. When the highest-HP opponent (the Silence Turns' target) is out of
  // the Turns' reach (range 5 = path length 6, law 40 convention: ai_v2.ts getDistance is the A* path length, origin
  // included), she steps toward it (ai_v2.ts:482-491, one hex per move action); placed last so every cast rule above is
  // tried first. She never steps while Stillness is pending: the blast (rule 1) comes first on her next turn, and the mark
  // needs the player within 3, so no step can follow it in the same turn.
  ...(P.silenceStalk ? [{ conditions: [{ type: "distance_higher_than", value: 7, target: "HIGHEST_MAX_HEALTH_OPPONENT", description: "Out of reach" }], action: { type: "move_towards_opponent", target: "HIGHEST_MAX_HEALTH_OPPONENT", description: "The Silence drifts closer" } }] : []),
  R.end(),
];
export const feelerRules = () => [
  R.jutsu(JID.cradle, "HIGHEST_MAX_HEALTH_ALLY", [COND.sayoAlive]),
  R.jutsu(JID.grasp, PL, [C.near(3)]), // Grasp range 2 -> gate 3 (law 40)
  R.end(),
];
// Stolen Form is 60 AP and Your Own Strike 60 AP: one or the other per turn (copy first, while ready).
// Stolen Form and Your Own Strike are range 4 -> gate 5 (law 40; Forge refused the gate of 4 on Stolen Form).
export const likenessRules = () => [R.jutsu(JID.likenessCopy, PL, [C.near(5)]), R.jutsu(JID.likenessStrike, PL, [C.near(5)]), { conditions: [], action: { type: "move_towards_opponent", target: PL, description: "Close in" } }];

/** Act II etching cycles (3 / 4 / 5 / 5; cycles 3 and 4 repeat an etching out of order). */
export const CYCLES: string[][] = [["A", "B", "C"], ["D", "A", "C", "B"], ["C", "A", "E", "A", "B"], ["E", "B", "D", "B", "C"]];
export const cycleCombo = (seq: string[], cycle: number) => [...seq.flatMap((k) => [JID.etch[k]!, JID.rises[cycle]!]), ...seq.map((k) => JID.det[k]!), JID.quietFall];
const cnt = (n: number) => C.has(MK.counter, n);
export const sayo2Rules = (_P: MoeParams) => [
  R.jutsu(JID.enrage, "SELF", [cnt(4)]),
  R.jutsu(JID.summonTomo, "EMPTY_GROUND_CLOSEST_TO_SELF", [C.has(MK.done), cnt(3), C.noSummon()]),
  R.jutsu(JID.summonHana, "EMPTY_GROUND_CLOSEST_TO_SELF", [C.has(MK.done), cnt(2), C.noSummon()]),
  R.jutsu(JID.summonPorter, "EMPTY_GROUND_CLOSEST_TO_SELF", [C.has(MK.done), C.noSummon()]),
  ...(_P.turnMark.on ? [R.jutsu(JID.turnII, "HIGHEST_MAX_HEALTH_OPPONENT", [C.has(MK.done)])] : []),
  R.jutsu(JID.lancet, PL, [C.has(MK.done), C.near(5)]),
  R.end([C.has(MK.done)]),
  withCond(COND.combo(cycleCombo(CYCLES[3]!, 3)), [cnt(3)]),
  withCond(COND.combo(cycleCombo(CYCLES[2]!, 2)), [cnt(2)]),
  withCond(COND.combo(cycleCombo(CYCLES[1]!, 1)), [cnt(1)]),
  COND.combo(cycleCombo(CYCLES[0]!, 0)),
  R.end(),
];
export const wornRules = (jid: string, target = PL) => [
  // Gate = range + 1 (law 40): Doorward Sweep range 1 -> 2 (a gate of 1 never fires), Cadet's Tether range 5 -> 6.
  R.jutsu(jid, target, target === PL ? [C.near(jid === JID.porter ? 2 : 6)] : [COND.sayoAlive]),
  // The unconditional move is the last rule (law 41): an end_turn under it could never fire.
  ...(target === PL ? [{ conditions: [], action: { type: "move_towards_opponent", target: PL, description: "Close in" } }] : [R.end()]),
];
const A3_GATE = 4;
const toHigh = (v: number, type: "distance_lower_than" | "distance_higher_than" = "distance_lower_than") => ({ type, value: v, target: "HIGHEST_MAX_HEALTH_OPPONENT", description: "Distance to the player" });
/** Act III redesign rules (20; see J3). Phase III first, then the Phase II combo, then the Phase I chain and its extras. */
export const saintRulesV2 = (P: MoeParams) => {
  const A3 = a3(P);
  const ph = (n: number) => C.has(MK3.phase, n);
  return [
    R.jutsu(JID.enrage, "SELF", [COND.rg(P.enrage.act3)]),
    R.jutsu(J3.pane[0]!, "SELF", [C.has(MK3.gA), ph(2)]),
    R.jutsu(J3.pane[1]!, "SELF", [C.has(MK3.gB), ph(2)]),
    R.jutsu(J3.pane[2]!, "SELF", [C.has(MK3.gC), ph(2)]),
    R.jutsu(J3.everyLine, "HIGHEST_MAX_HEALTH_OPPONENT", [ph(2), toHigh(A3_GATE)]),
    // Phase III: she walks to the player (first prototype: she stood still, the player could not cross the marked floor to
    // reach her open guard, and 2 of 20 perfect runs stalled into the enrage). Beside the player the move fails and the
    // turn ends at the combo rule, whose first step needs AP she no longer has after a pane and Every Line.
    { conditions: [ph(2)], action: { type: "move_towards_opponent", target: "HIGHEST_MAX_HEALTH_OPPONENT", description: "She comes to you" } },
    R.jutsu(J3.impression, "SELF", [C.hb(A3.p3Gate), C.has(MK3.cycleEnd, 1), ph(1)]),
    withCond(COND.combo(a3PhaseCombo(A3)), [ph(1)]),
    R.jutsu(J3.facetBreak, "SELF", [C.has(MK3.f)]),
    R.jutsu(J3.facet, "SELF", [C.has(MK3.b)]),
    R.jutsu(J3.lucid, "SELF", [C.has(MK3.a)]),
    R.jutsu(J3.mended, "SELF", [C.hb(A3.p2Gate), C.has(MK3.clean)]),
    R.end([ph(1)]),
    R.jutsu(J3.nothingMoves, "SELF", [C.has(MK3.still)]),
    R.jutsu(J3.stir, "SELF", [C.hb(A3.stirGate)]),
    R.jutsu(J3.opener, "SELF", []),
    R.jutsu(J3.silenceHolds, "SELF", [C.hb(A3.cradleGate)]),
    R.jutsu(J3.lancet, PL, [C.near(5)]),
    // Hold Still and Every Line only within 3 hexes (path 4): farther out she walks in instead. With the full range-5 gate
    // she cast it every turn from 4-5 hexes and never closed, while a pool-aware player held his hex (3 of 20 stalls).
    R.jutsu(J3.holdStill, "HIGHEST_MAX_HEALTH_OPPONENT", [toHigh(A3_GATE)]),
    // Toward the player, not the closest opponent: a pet beside her held her in place while the player stood off.
    { conditions: [], action: { type: "move_towards_opponent", target: "HIGHEST_MAX_HEALTH_OPPONENT", description: "Close in" } },
  ];
};
export const saintRules = (P: MoeParams) => [
  R.jutsu(JID.enrage, "SELF", [COND.rg(P.enrage.act3)]),
  R.jutsu(JID.longHush, "SELF", [C.hb(25)]),
  R.jutsu(JID.glassRecast, "SELF", [C.has(MK.gCs)]),
  R.jutsu(JID.glassFirstB, "SELF", [C.has(MK.firstPass), C.has(MK.gB)]),
  R.jutsu(JID.glass[0]!, "SELF", [C.has(MK.gA)]),
  R.jutsu(JID.glass[1]!, "SELF", [C.has(MK.gB)]),
  R.jutsu(JID.glass[2]!, "SELF", [C.has(MK.gC)]),
  R.end([C.hb(25)]),
  // Every Name in the Glass: Breathless Pull mark -> pull + stun and the flood mark -> the flood.
  R.jutsu(JID.shatterBlast, "SELF", [C.has(MK.shatter)]),
  R.jutsu(JID.floodBlast, "SELF", [C.has(MK.flood)]),
  R.jutsu(JID.pull, "SELF", [C.has(MK.pull)]),
  R.jutsu(JID.floodMark, "SELF", [C.has(MK.breath)]),
  R.jutsu(JID.m2Entry, "SELF", [C.hb(60)]),
  R.jutsu(JID.pullMark, "SELF", [C.hb(60)]),
  R.jutsu(JID.starHush, "SELF", [C.hb(60)]),
  R.jutsu(JID.quiet, PL, [C.near(5)]),
  R.jutsu(JID.shatterMark, "SELF", []),
  R.jutsu(JID.lancet, PL, [C.near(5)]),
  // Shatterfall is caster-anchored: never move between its mark and its fall.
  R.end([C.has(MK.shatter)]),
  // Unconditional last rule (law 41): close in; beside the player it does nothing and the engine's end turn follows.
  { conditions: [], action: { type: "move_towards_opponent", target: PL, description: "Close in" } },
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
    ({ id, username, poolsMultiplier: pools, jutsus: [...new Set(jutsus)], effects: [...idgTags(idg), ...drTag(dr), ...(P.sayoStunImmune && [AI.sayo1, AI.sayo2, AI.saint].includes(id) ? stunImmune() : []), ...extra], rules, heavyArmor: true });
  // Director 2026-11-05: Sayo (all three forms) is stun immune: innate stunprevent 100 (positive power), checked by the
  // stun tag before it lands (theninjarpg@3314d122 libs/combat/tags.ts:2749; StunPreventTag validators/combat.ts:1041-1047).
  function stunImmune() { return [tag("stunprevent", { power: 100, rounds: 100, calculation: "percentage", description: "Nothing stills the Mother of Echoes" })]; }
  const summon = (id: string, username: string, jutsus: string[], rules: any[], effects: any[] = []) => ({ id, username, poolsMultiplier: 1, jutsus, effects: [...idgTags(P.idg.summons), ...effects], rules, heavyArmor: false, summon: true });
  const etchIds = Object.values(JID.etch), detIds = Object.values(JID.det);
  return [
    boss(AI.sayo1, "Sayo, Mother of Echoes", P.pools.sayo1, P.idg.sayo1, P.dr.sayo1,
      [JID.lancet, JID.enrage, JID.refractA, JID.refractB, JID.blastA, JID.blastB, JID.facet, JID.facetBlast, JID.lucidBlast, JID.lucidWake, JID.likeness], sayo1Rules(P), [token(MK.sayoToken)]),
    boss(AI.silence, "The Silence", P.pools.silence, P.idg.silence, P.dr.silence,
      [JID.enrage, ...JID.hush, JID.hushUnbridled, JID.listening, JID.listeningUnbridled, JID.stillness, JID.stillnessBlast, ...(P.turnMark.on ? [JID.turnI] : [])], silenceRules(P), [token(MK.silenceToken)]),
    summon(AI.feeler, "A Feeler of the Deep", [JID.cradle, JID.grasp], feelerRules()),
    summon(AI.likeness, "Your Likeness", [JID.likenessStrike, JID.likenessCopy], likenessRules()),
    boss(AI.sayo2, "Sayo, Glasswright of the Stilling", /* RUL-2026-11-02-105: unique AI usernames */ P.pools.sayo2, P.idg.sayo2, P.dr.sayo2,
      [JID.lancet, JID.enrage, ...etchIds, ...detIds, ...JID.rises, JID.quietFall, JID.summonPorter, JID.summonHana, JID.summonTomo, ...(P.turnMark.on ? [JID.turnII] : [])], sayo2Rules(P),
      [...(P.sayo2Stunprevent ? [tag("stunprevent", { power: 100, rounds: 100 })] : []), token(MK.sayoToken)]),
    summon(AI.porter, "The Gate Porter (Worn)", [JID.porter], wornRules(JID.porter)),
    summon(AI.hana, "Sister Hana (Worn)", [JID.hana], wornRules(JID.hana, "HIGHEST_MAX_HEALTH_ALLY")),
    summon(AI.tomo, "Cadet Tomo (Worn)", [JID.tomo], wornRules(JID.tomo)),
    a3(P).on ? boss(AI.saint, "Sayo, Saint of Stillness", P.pools.saint, P.idg.saint, P.dr.saint,
      [JID.enrage, J3.opener, J3.lucid, J3.facet, J3.facetBreak, J3.holdStill, J3.silenceHolds, J3.nothingMoves, J3.lancet, J3.stir, J3.mended, ...Object.values(J3.etch), ...Object.values(J3.flood), J3.everyName, J3.rises, J3.starHush, J3.impression, ...J3.pane, J3.everyLine], saintRulesV2(P)) :
    boss(AI.saint, "Sayo, Saint of Stillness", P.pools.saint, P.idg.saint, P.dr.saint,
      [JID.lancet, JID.enrage, JID.quiet, JID.shatterMark, JID.shatterBlast, JID.floodMark, JID.floodBlast, JID.m2Entry, JID.pullMark, JID.pull, JID.starHush, JID.longHush, ...JID.glass, JID.glassFirstB, JID.glassRecast], saintRules(P)),
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
let AVG_OVERRIDE: any = null;
export const setGearOverride = (g: any, avg?: any) => { GEAR_OVERRIDE = g; AVG_OVERRIDE = avg ?? null; };
/** Pass 6 live calibration: seat combatants like the server (random spawn blocks) instead of the fixed posts. */
let LIVE_SPAWN = false;
let P_NO_REENTRY = false;
let RAMP_CLEARABLE = false;
let POOL_AWARE = false;
let DEBUG_TRACE = false;
let A3_ON = false;
let A3_POLICY: any = null;
export const setLiveSpawn = (on: boolean) => { LIVE_SPAWN = on; };
/**
 * The average geared level-100 model (RUL-2026-11-02-097 item 3), built the same way as the elite one: the real Kitsune
 * set and the 9-jutsu Fire/Wind endgame kit, plus gear stand-in rows, with the +100% damage rows sized so that its
 * typical hit on an AI in AI Heavy Armor is about 45% of the elite model's (moe_probe P7). Gear assumption, documented
 * because no player log calibrates it: the elite model's kit (the same 9 jutsu: shields, lifesteal, vamp) with about half
 * its gear: 3 +100% gear damage rows (gear rows add to the engine's 60-point pre-battle increase pool, so hits scale with
 * 1.6 + rows: 3 rows hit ~43% as hard as the elite's 20, moe_probe P7), pools x4 (20,200 HP before Kitsune; two-thirds of the elite's),
 * 50% damage-taken reduction, 15% gear lifesteal and 15% siphon, one pet. (Pass 1 used the harness `average` tier: the
 * Fire/Wind endgame kit with no sustain, no gear rows, 6,250 HP; it died in round 2.)
 */
export const AVG_GEAR = { damageTakenReductionPct: 50, poolsMultiplier: 4, idgRows: 3, lifesteal: 15, siphon: 15, pets: 1, kit: "elite" as "elite" | "endgame" };
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
  for (const id of REAL_KIT) if (!j[id]) j[id] = id === "moe-harness-captains-decree" ? decreeEquivalent() : capturedJutsu(id).record;
  return j;
};
export type PlayerModel = { variant: PlayerVariant; pets: number; immune: boolean; idgRows?: number; sustain: { lifestealGear: number; siphonInnate: number };
  /** Real-player policy (RUL-2026-11-02-099 addendum): logged kit + items, reactive Clear/Cleanse, telegraph read rate. */
  real?: { readP: number; items: { id: string; qty: number }[] } };
/**
 * The geared level-100 stand-in. The harness's old `elite` tier carried one +400% gear row, but the engine realises a
 * tag row at power <= 100, so it hit for less than the Kitsune-geared `average`. Here: the real Kitsune set, one
 * decreasedamagetaken row, and `idgRows` +100% increasedamagegiven gear rows (gear rows fold additively into the
 * pre-battle increase pool, process.ts computeDamagePacket), sized so that the kit's typical hit on an AI wearing only
 * AI Heavy Armor is 5-8k (the director's logs). Pools x6 (30,300 HP).
 */
export const ELITE_GEAR = { damageTakenReductionPct: 75, poolsMultiplier: 6, idgRows: 20 };
export const playerModel = (name: string, over: any = {}): PlayerModel => {
  if (name.endsWith("_real")) return realModel(playerModel(name.slice(0, -5).replace("_perfect", ""), over), name);
  if (name.startsWith("elite") && over.gear === undefined && GEAR_OVERRIDE) over = { ...over, gear: GEAR_OVERRIDE };
  if (name === "average") {
    const g = { ...AVG_GEAR, ...(AVG_OVERRIDE ?? {}), ...(over.gear ?? {}) };
    const v: PlayerVariant = { ...PLAYER_VARIANTS.average!, name: "average", note: "average geared level-100 model (see AVG_GEAR)", poolsMultiplier: g.poolsMultiplier, damageGivenPct: 0, damageTakenReductionPct: g.damageTakenReductionPct,
      ...(g.kit === "elite" ? { jutsuIds: ELITE_KIT, elements: ["Fire", "Earth"] as [string, string] } : {}) };
    return { variant: v, pets: g.pets, immune: false, idgRows: g.idgRows, sustain: { lifestealGear: g.lifesteal, siphonInnate: g.siphon } };
  }
  const g = { ...ELITE_GEAR, ...(over.gear ?? {}) };
  const v: PlayerVariant = {
    name: "elite", note: "geared level-100 model (elite gear stand-in + sustain kit)", statBudget: 1,
    stats: { offence: 1_300_000, defence: 1_300_000, generals: 400_000 }, poolsMultiplier: g.poolsMultiplier,
    damageGivenPct: 0, damageTakenReductionPct: g.damageTakenReductionPct, gearItemIds: KITSUNE_SET,
    elements: ["Fire", "Earth"], jutsuIds: ELITE_KIT, jutsuLevel: 25,
  };
  return { variant: v, pets: over.pets ?? 2, immune: name.startsWith("elite_imm"), idgRows: g.idgRows, sustain: { lifestealGear: over.lifesteal ?? g.lifesteal ?? 25, siphonInnate: over.siphon ?? g.siphon ?? 25 } };
};
/**
 * The real-player model, from two logged fights of a strong stun/seal-immune player (loveispure vs The Captain,
 * 2026-11-01; scratchpad player_logs). What the logs show, and how it is modelled:
 * - Kit: the jutsu he cast, as captured (REAL_KIT). Not modelled: Chakra Invigoration (a move jutsu; the engine
 *   withholds move/summon jutsu from auto-combat humans, ai_v2.ts allActions filter) and Ancient Demon Roar (a bloodline
 *   jutsu). Captain's Decree is not captured: a harness equivalent built from the log lines (damage, +20% damage taken
 *   on the target, 40 AP, cooldown 7).
 * - Items, as captured: Ink of the Void (bow), Colored Jewel of the Dragon's Neck, Paper Bombs, Kunai, Chakra Pill,
 *   Stamina Pill, Energy Potion.
 * - Turn shape: 2 actions a turn, nearly always a 60 AP attack plus a 40 AP buff/debuff/weapon (or a 20 AP item); three
 *   buffs on round 1 (Wind Release, Chakra Overflow, the Jewel); End Turn once in ~29 turns; every jutsu at cooldown 7
 *   gives the logged cadence (each cast about every 7 rounds). Rules list 60 AP attacks first, then 40 AP, then 20 AP.
 * - Sustain: pills and the Energy Potion as HP falls (the logs show them at rounds 4-6 and 13-14).
 * - Clear: on the target right after it gains a clearable buff (2 per fight in the logs, after Unbroken Command and
 *   Counter Stance). Cleanse: when rooted or drained (2 per fight, after Keelbind / Sovereign Fetters).
 * - Movement: few steps; Replacement Technique to leave a mark (4 per fight).
 * - Two pets (Homura, Lorcan).
 * - Mistakes: he stood in 1 of the ~6 telegraphs in reach (Ship's Bell, in log 1). readP 0.85 for the elite; 0.7 for
 *   the average player (assumption). A learned player knows the etching order (the Recast memory is kept).
 */
export const REAL_KIT = [
  "rkFJGghHPLsaj9S_rVeoV", // Wind Release: Whirlwind Demise (self: +40% stat, +40% damage)
  "e2eC-x4UXc5m6QexNbx8w", // Chakra Overflow
  "_zNMEZqIzgjTqXoXQRWz0", // Earthen Bastion (self: DR 30, IDG 30)
  "ou7VyChQ-SFCm8T8yGS7I", // Eclipse Drain (self: lifesteal 35, IDG 30)
  "Ul83iTziN__Z0i_UOzZTK", // Tempest Cleave (AoE 45 + afterburn + IDT 35)
  "FytS2iqFInf1go6WhOvUU", // Dragon King's Impact (40 + IDG + afterburn + wound)
  "fCWC_ICdWT1bJDkDVq22e", // Wind Style: Sky Dragon (40 + wound)
  "PQdSt0IDdYFoR44tC3Hvo", // Typhon Burst (AoE 35 + IDG)
  "GiKpip6NxsC8QWlZi6l_R", // Shrapnel Clone Barrage (AoE 45 + wound)
  "QhEDzYwU0ucb0W7Ymib1T", // Multi-Layered Gale (35 + IDT 30)
  "FlQ0Mk8CB7afkYqxFempz", // Chakra Enfeeblement (IDT 40, DDG 30)
  "gkZYgOkTp8sQ_6qLR0uIy", // Heaven's Blessing (IDT 30 + afterburn)
  "moe-harness-captains-decree", // Captain's Decree (equivalent; not captured)
];
export const REAL_ITEMS = [
  { id: "wE1QeldWTjls2Cf43cFjf", qty: 1 }, // Ink of the Void (bow): 30 + vamp 25, 40 AP
  { id: "_8HEbybzN5QPX8vUG24Tk", qty: 1 }, // Colored Jewel of the Dragon's Neck: IDG 15, DR 10, 20 AP
  { id: "mlCQd6nbegRsYiO28cTPp", qty: 10 }, // Paper Bombs: afterburn 20, IDT 15, 20 AP
  { id: "u9mXSgVW_QjkRzCejGXZ1", qty: 20 }, // Kunai: 20, 20 AP
  { id: "tZTvqYWiAc_OrY64nDvIo", qty: 5 }, // Chakra Pill: IDG 15, lifesteal 20
  { id: "GNGrfEDnxbRBgOHHCjPX3", qty: 5 }, // Stamina Pill: DR 20, pool cost -30
  { id: "h-mvWaKK5vNNOwS5Y9KQj", qty: 5 }, // Energy Potion: heal 40%
];
let ITEM_CACHE: Record<string, any> | null = null;
export const capturedItems = () => {
  if (ITEM_CACHE) return ITEM_CACHE;
  const want = new Set(REAL_ITEMS.map((i) => i.id));
  const best: Record<string, any> = {};
  const walk = (x: any) => {
    if (Array.isArray(x)) x.forEach(walk);
    else if (x && typeof x === "object") {
      if (want.has(x.id) && "itemType" in x && Array.isArray(x.effects) && (!best[x.id] || (x.updatedAt ?? "") > (best[x.id].updatedAt ?? ""))) best[x.id] = x;
      Object.values(x).forEach(walk);
    }
  };
  for (const f of readdirSync(join(process.env.TNR_REPO!, "harvests/inbox")).filter((f) => f.endsWith(".json"))) walk(JSON.parse(readFileSync(join(process.env.TNR_REPO!, "harvests/inbox", f), "utf8")));
  for (const id of want) if (!best[id]) throw new Error(`item ${id} not captured`);
  return (ITEM_CACHE = structuredClone(best));
};
export const decreeEquivalent = () => jutsu("moe-harness-captains-decree", { name: "Captain's Decree (equivalent)", description: "Harness stand-in for the uncaptured Captain's Decree, built from its log lines.", battleDescription: "%user draws Captain's Decree.", target: "OPPONENT", method: "SINGLE", range: 4, cooldown: 7, actionCostPerc: 40, effects: [T.damage(40), T.pct("increasedamagetaken", 20, 2)] });
const realRules = (kit: string[], jutsu: Record<string, any>) => {
  const PLR = "CLOSEST_OPPONENT";
  const near = (r: number) => ({ type: "distance_lower_than", value: r, target: PLR, description: "" });
  const hb = (v: number) => ({ type: "health_below", value: v, description: "" });
  const r1 = { type: "round_lower_than", value: 2, description: "" };
  const J = (id: string, target: string, conditions: any[] = []) => ({ conditions, action: { type: "use_specific_jutsu", jutsuId: id, target, description: "" } });
  const I = (id: string, target: string, conditions: any[] = []) => ({ conditions, action: { type: "use_specific_item", itemId: id, target, description: "" } });
  const self = kit.filter((id) => jutsu[id]?.target === "SELF");
  const atk = (ap: number) => kit.filter((id) => jutsu[id] && jutsu[id].target !== "SELF" && jutsu[id].actionCostPerc === ap);
  if (SKILLED) {
    // Pass 6 skilled policy (director 2026-11-04 item 3), used by every _real profile:
    // - recovery is saved for real damage: the Energy Potion only below 50% HP (right after an eruption or a ramp
    //   hit), never topped up early; the Stamina Pill (DR 20) when hurt, the Chakra Pill (IDG 15, lifesteal 20) into an opening;
    // - defend when hurt: the self mitigation/sustain jutsu (shields, damage-taken cuts, lifesteal) go first below 65% HP;
    // - burst into openings: while the target carries weakness (Sayo's x3 guard-open after a Recast) or while its own
    //   lifesteal is up, the strongest available attack goes first (use_highest_power_action);
    // - otherwise the strongest affordable attack every action (no fixed 60/40/20 rotation), then buffs, then weapons.
    const tHasE = (t: string) => ({ type: "target_has_effect", effectType: t, threshold: 1, target: PLR, description: "" });
    const hasE = (t: string) => ({ type: "has_effect", effectType: t, threshold: 1, description: "" });
    const best = (c: any[] = []) => ({ conditions: c, action: { type: "use_highest_power_action", effect: "damage", target: PLR, description: "" } });
    return [
      I("h-mvWaKK5vNNOwS5Y9KQj", "SELF", [hb(50)]),
      J("rkFJGghHPLsaj9S_rVeoV", "SELF", [r1]), J("e2eC-x4UXc5m6QexNbx8w", "SELF", [r1]), I("_8HEbybzN5QPX8vUG24Tk", "SELF", [r1]),
      ...self.map((id) => J(id, "SELF", [hb(65)])),
      I("GNGrfEDnxbRBgOHHCjPX3", "SELF", [hb(65)]), // Stamina Pill: DR 20
      I("tZTvqYWiAc_OrY64nDvIo", "SELF", [tHasE("weakness")]), // Chakra Pill (IDG 15, lifesteal 20) into the guard-open window
      best([tHasE("weakness")]),
      best([hasE("lifesteal")]),
      best(),
      ...self.map((id) => J(id, "SELF")),
      I("wE1QeldWTjls2Cf43cFjf", PLR, [near(4)]),
      { conditions: [{ type: "distance_higher_than", value: 2, target: PLR, description: "" }], action: { type: "move_towards_opponent", target: PLR, description: "" } },
      best(),
    ];
  }
  return [
    I("h-mvWaKK5vNNOwS5Y9KQj", "SELF", [hb(45)]),
    I("GNGrfEDnxbRBgOHHCjPX3", "SELF", [hb(65)]),
    I("tZTvqYWiAc_OrY64nDvIo", "SELF", [hb(80)]),
    // Round 1: the setup turn (Wind Release, Chakra Overflow, the Jewel).
    J("rkFJGghHPLsaj9S_rVeoV", "SELF", [r1]), J("e2eC-x4UXc5m6QexNbx8w", "SELF", [r1]), I("_8HEbybzN5QPX8vUG24Tk", "SELF", [r1]),
    // Then: a 60 AP attack, then a 40 AP buff / debuff / weapon, then a 20 AP item.
    ...atk(60).map((id) => J(id, PLR, [near(jutsu[id].range)])),
    ...self.map((id) => J(id, "SELF")),
    ...atk(40).map((id) => J(id, PLR, [near(jutsu[id].range)])),
    I("wE1QeldWTjls2Cf43cFjf", PLR, [near(4)]),
    I("_8HEbybzN5QPX8vUG24Tk", "SELF"),
    I("mlCQd6nbegRsYiO28cTPp", PLR, [near(4)]),
    I("u9mXSgVW_QjkRzCejGXZ1", PLR, [near(4)]),
    { conditions: [{ type: "distance_higher_than", value: 2, target: PLR, description: "" }], action: { type: "move_towards_opponent", target: PLR, description: "" } },
    { conditions: [], action: { type: "use_highest_power_action", effect: "damage", target: PLR, description: "" } },
  ];
};
const realModel = (base: PlayerModel, name: string): PlayerModel => {
  const avg = name.startsWith("average");
  const variant = { ...base.variant, name: base.variant.name + "_real", jutsuIds: REAL_KIT, elements: ["Wind", "Fire"] as [string, string] };
  return { ...base, variant, idgRows: avg ? REAL_GEAR_ROWS.average : REAL_GEAR_ROWS.elite, pets: avg ? base.pets : 2, real: { readP: name.includes("perfect") ? 1 : avg ? REAL_READ.average : REAL_READ.elite, items: REAL_ITEMS } };
};
export const REAL_READ = { elite: 0.85, average: 0.7 };
let SKILLED = false;
export const setSkilled = (v: boolean) => { SKILLED = v; };
/** Gear damage rows for the real kit, calibrated like the elite model (moe_probe P11): 4 rows put its hits on an AI in
 * AI Heavy Armor at median 4,944 / p90 9,248 against the logs' 5,117 / 10,810. Average: 1 row (~46% of the elite's hits). */
export const REAL_GEAR_ROWS = { elite: 4, average: 1 };
/** Player row: the model's variant plus sustain rows (gear lifesteal on the armour row, siphon innate) and the immunity rows. */
export const buildPlayer = (m: PlayerModel, catalog: Record<string, any>) => {
  const variant = m.real ? { ...m.variant, rules: realRules(m.variant.jutsuIds, catalog) } : m.variant;
  const u: any = playerQueryUser(0, variant, t0.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, catalog);
  if (m.real) {
    const items = capturedItems();
    const donor = u.items[0] ?? null;
    for (const [i, it] of m.real.items.entries()) {
      const rec = structuredClone(items[it.id]);
      u.items.push({ ...(donor ? structuredClone(donor) : {}), id: `real-${i}-${it.id}`, userId: u.userId, itemId: it.id, equipped: rec.slot, quantity: it.qty, isInAuction: false, durability: 100, imbuements: [], level: 1, item: rec });
    }
  }
  const gear = u.items.find((ui: any) => ui.item?.id === "harness-gear-armor");
  if (gear && m.idgRows) for (let i = 0; i < m.idgRows; i++) gear.item.effects.push({ ...structuredClone(gear.item.effects[0]), type: "increasedamagegiven", power: 100, direction: "offence", rounds: 100, description: "harness gear stand-in increasedamagegiven 100%" });
  // Live calibration (director's log, 2026-11-05; harvests/battle_logs/moe_practice_dauntless_2026-11-05.txt on main):
  // gear.incTakenPct / avgGear.incTakenPct add an increasedamagetaken % row to the gear armor. Armor percentage rows are
  // consolidated into the pre-battle pools (process.ts:1752-1779): incPoints = 60 + this (process.ts:2218-2223), so the
  // player's formula damage taken is raised by (160 + X) / 160 before the DR pool, and the 5% floor rises with it.
  const incTaken = (m.variant.name.startsWith("average") ? AVG_OVERRIDE : GEAR_OVERRIDE)?.incTakenPct ?? 0;
  // One row per 100 points: a single row's power is clamped at 100 (observed: 300 / 358 / 420 all gave +100).
  for (let left = incTaken; gear && left > 0; left -= 100) gear.item.effects.push({ ...structuredClone(gear.item.effects[0]), type: "increasedamagetaken", power: Math.min(100, left), direction: "defence", rounds: 100, description: "live calibration: increasedamagetaken" });
  if (gear && m.sustain.lifestealGear) gear.item.effects.push({ ...structuredClone(gear.item.effects[0]), type: "lifesteal", power: m.sustain.lifestealGear, rounds: 100, description: "harness gear stand-in lifesteal" });
  const innate = (type: string, power: number, extra: any = {}) => ({ ...structuredClone(tag(type, { power, rounds: 100, ...extra })), target: "INHERIT" });
  if (m.sustain.siphonInnate) u.effects.push(innate("siphon", m.sustain.siphonInnate, { calculation: "percentage" }));
  if (m.immune) u.effects.push(innate("stunprevent", 100), innate("sealprevent", 100));
  return u;
};

/* ------------------------------------------------------------------ the fight runner */
export type Policy = "play" | "ignore" | "camp";
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
  misreads?: number; recastMisreads?: number; clears?: number; lancet?: { n: number; sum: number; max: number; pctOfMax: number[] };
  /** Solvability (director 2026-11-05): player turns checked; turns with no free hex within reach (5) clear of every live mark (+ pools). */
  solv?: { turns: number; noSafe: number; noSafeInclPools: number; noSafeRounds: number[] }; playerActs?: Record<string, number>; playerTurns?: number; playerEndTurns?: number; minHpFrac?: number;
  /** Act III review (2026-11-05): AP spent per player turn by category, and turns that ended with >= 20 AP unspent. */
  ap?: { turns: number; move: number; attack: number; buff: number; answer: number; other: number; unspent: number; turnsUnspent20: number };
};
/** Set-piece bookkeeping: action id -> [set name, role, telegraph id(s)]. */
export const SETS: Record<string, [string, "mark" | "land", string[]?]> = {
  [JID.refractA]: ["Refraction", "mark"], [JID.refractB]: ["Refraction", "mark"],
  [JID.blastA]: ["Refraction", "land", [JID.refractA]], [JID.blastB]: ["Refraction", "land", [JID.refractB, JID.lucidBlast]],
  [JID.facet]: ["Facet", "mark"], [JID.facetBlast]: ["Facet", "land", [JID.facet]],
  [JID.lucidBlast]: ["Refraction", "land", [JID.refractA]],
  [JID.stillness]: ["Stillness", "mark"], [JID.stillnessBlast]: ["Stillness", "land", [JID.stillness]],
  [JID.shatterMark]: ["Shatterfall", "mark"], [JID.shatterBlast]: ["Shatterfall", "land", [JID.shatterMark]],
  [JID.floodMark]: ["Every Name", "mark"], [JID.floodBlast]: ["Every Name", "land", [JID.floodMark]],
  [JID.pullMark]: ["Breathless Pull", "mark"], [JID.pull]: ["Breathless Pull", "land", [JID.pullMark]],
  [JID.longHush]: ["Glassfall", "mark"],
  [JID.glass[0]!]: ["Glassfall", "land", [JID.longHush, JID.glass[2]!, JID.glassRecast]],
  [JID.glass[1]!]: ["Glassfall", "land", [JID.glass[0]!]], [JID.glassFirstB]: ["Glassfall", "land", [JID.glass[0]!]],
  [JID.glass[2]!]: ["Glassfall", "land", [JID.glass[1]!]], [JID.glassRecast]: ["Glassfall", "land", [JID.glassFirstB]],
};
for (const k of Object.keys(PAT.etch)) { SETS[JID.etch[k]!] = ["Recast", "mark"]; SETS[JID.det[k]!] = ["Recast", "land"]; }
// Act III redesign bookkeeping (the role is the land unless noted; the marks ride the previous land).
Object.assign(SETS, {
  [J3.opener]: ["Refraction", "mark"], [J3.lucid]: ["Refraction", "land", [J3.opener]], [J3.facet]: ["Refraction", "land", [J3.lucid]],
  [J3.facetBreak]: ["Facet", "land", [J3.facet]], [J3.silenceHolds]: ["Stillness", "mark"], [J3.nothingMoves]: ["Stillness", "land", [J3.silenceHolds]],
  [J3.holdStill]: ["Hold Still", "mark"], [J3.everyLine]: ["Every Line", "mark"], [J3.everyName]: ["Every Name", "mark"],
  [J3.impression]: ["Glassfall", "mark"], [J3.pane[0]!]: ["Glassfall", "land", [J3.impression, J3.pane[2]!]], [J3.pane[1]!]: ["Glassfall", "land", [J3.impression, J3.pane[0]!]], [J3.pane[2]!]: ["Glassfall", "land", [J3.pane[1]!]],
});
for (const k of Object.keys(J3.etch)) { SETS[J3.flood[k]!] = ["Every Name", "land", [J3.everyName]]; }
const SPECIAL_IDS: Record<string, string> = {
  [J3.stir]: "The Names Stir (warning)", [J3.mended]: "No One Is Mended (v2)", [J3.starHush]: "Hush on a star", [J3.rises]: "Hush Rises (III)", [J3.lancet]: "Remainder Lancet",
  [JID.lucidBlast]: "Lucid", [JID.lucidWake]: "Lucid (wakes)", [JID.rises[0]!]: "Hush Rises", [JID.rises[1]!]: "Hush Rises", [JID.rises[2]!]: "Hush Rises", [JID.rises[3]!]: "Hush Rises", [JID.hushUnbridled]: "Unbridled Hush", [JID.listeningUnbridled]: "Unbridled Listening", [JID.cradle]: "Cradle",
  [JID.listening]: "Listening", [JID.likeness]: "Your Likeness", [JID.enrage]: "Enrage", [JID.quiet]: "The Quiet", [JID.pull]: "Breathless Pull",
  [JID.starHush]: "Hush on a safe tile", [JID.m2Entry]: "No One Is Mended", [JID.quietFall]: "Cycle end", [JID.summonPorter]: "Worn: Porter",
  [JID.summonHana]: "Worn: Hana", [JID.summonTomo]: "Worn: Tomo", [JID.glassRecast]: "Long Hush recast", [JID.hush[0]!]: "Hush", [JID.hush[1]!]: "Hush", [JID.hush[2]!]: "Hush",
};
/** Cells a pattern record covers when cast by `caster` (BATTLEFIELD or CASTER origin). */
export const recCells = (rec: any, caster: Cell): Set<string> => {
  // Caster-anchored spiral (anchored Stillness): every hex within range of the caster, its own excluded.
  if (rec?.method === "AOE_SPIRAL_SHOOT") return new Set(ALL.filter((c) => dist(c, caster) <= (rec.range ?? 0) && key(c) !== key(caster)).map(key));
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
    if (!LIVE_SPAWN) for (const [aid, c] of Object.entries(cfg.positions ?? {})) { const u = bossU(aid); if (u) [u.longitude, u.latitude] = c; }
    // Live spawn (director's log 2026-11-05: Sayo I5 = (8,4), the Silence J7 = (9,6)): the server seats every combatant
    // on a random cell of its side's spawn block (theninjarpg@3314d122 server/api/routers/combat.ts:3867-3880, unseeded
    // node:crypto; blocks from libs/combat/participants.ts:34-55 with COMBAT_BORDER_* = 2/2/2/0, libs/combat/constants.ts:23-26:
    // 12 x 10 field: right x 8-9, left x 3-4, y 1-7). The harness draws the same blocks with the run's seeded stream.
    if (LIVE_SPAWN) {
      const taken: string[] = [];
      const seat = (u: any, dir: "left" | "right") => {
        const open = getBattleSpawnLocations(W, H, dir).filter((l) => !taken.includes(`${l.x},${l.y}`));
        const l = open[Math.floor(rand() * open.length)]!;
        taken.push(`${l.x},${l.y}`); u.longitude = l.x; u.latitude = l.y;
      };
      for (const aid of cfg.bossIds) { const u = bossU(aid); if (u) seat(u, "right"); }
      seat(pu(), "left");
      for (const pet of b.usersState.filter((u: any) => u.petId || (u.isSummon && u.direction === "left"))) seat(pet, "left");
      if (o.policy === "camp") { const camp = ({ 1: [7, 3], 2: [10, 4], 3: [6, 2] } as Record<number, Cell>)[cfg.act]!; if (!b.usersState.some((u: any) => u.longitude === camp[0] && u.latitude === camp[1])) [pu().longitude, pu().latitude] = camp; }
    }
    // Player side spawns on the west edge (column 0-1), facing the bosses.
    if (!LIVE_SPAWN) {
      const p0 = pu();
      const free = (c: Cell) => !b.usersState.some((u: any) => u !== p0 && u.longitude === c[0] && u.latitude === c[1]);
      // Seeded west-edge spawn (columns 0-1, rows 2-7): the run's only positional variance besides the random Hush seeds.
      const cands: Cell[] = [];
      for (const col of [0, 1]) for (let row = 2; row <= 7; row++) cands.push([col, row]);
      const open = cands.filter(free);
      const c = open[Math.floor(rand() * open.length)]!;
      [p0.longitude, p0.latitude] = c;
      // camp profile: the act's best never-marked hex within reach of the bosses (pass 6 coverage audit)
      if (o.policy === "camp") { const camp = ({ 1: [7, 3], 2: [10, 4], 3: [6, 2] } as Record<number, Cell>)[cfg.act]!; if (free(camp)) [p0.longitude, p0.latitude] = camp; }
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
    (res as any).maxHp = maxHp;
    const set = (k: string) => (res.sets[k] ??= { mark: 0, land: 0, hit: 0, dmg: 0, unmarked: 0 });
    const actionRounds: number[] = [];
    const turnActs = new Map<string, string[]>();
    const apTurn: Record<string, number> = {};
    let topUpId = "";
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
      const recast = new Set<string>();
      for (const g of b.groundEffects as any[]) {
        if (!es.has(g.creatorId)) continue;
        if ((g.rounds ?? 0) <= 0 && !g.castThisRound) continue;
        const k = `${g.longitude},${g.latitude}`;
        // A stun-immune player ignores the stun-only telegraph (Breathless Pull), as the logged player stood in stuns; Stillness still crushes, so it is avoided.
        if (o.model.immune && g.actionId === JID.pullMark) continue;
        // Drawn art only: visual marks (while the server keeps them) and the non-visual carriers; pools draw on their effect.
        const drawn = g.type === "visual" || g.type === "increaseregeneration";
        if (drawn && (g.staticAnimation === "tg_heavy" || g.staticAnimation === "tg_control")) danger.add(k);
        if (drawn && g.staticAnimation === "tg_safe") safe.add(k);
        if (g.staticAnimation === "tg_linger") linger.add(k);
      }
      // Memory: the next Recast detonation (Act II) and the Long Hush recast (Act III).
      const s2 = bossU(AI.sayo2);
      if (s2 && alive(s2)) {
        const nxt = nextComboAction(b, s2);
        if (nxt && Object.values(JID.det).includes(nxt)) for (const k of recCells(cfg.recs[nxt], [s2.longitude, s2.latitude])) { danger.add(k); recast.add(k); }
      }
      const st = bossU(AI.saint);
      if (A3_ON && st && alive(st)) {
        // Memory (Act III Phase II): the flood that comes next also takes the region she etched two turns ago.
        const nxt = nextComboAction(b, st);
        if (nxt && Object.values(J3.flood).includes(nxt)) for (const k of recCells(cfg.recs[nxt], [st.longitude, st.latitude])) { danger.add(k); recast.add(k); }
      }
      if (!A3_ON && st && alive(st) && b.usersEffects.some((e: any) => e.targetId === st.userId && e.type === MK.gCs)) for (const k of recCells(cfg.recs[JID.glassRecast], [st.longitude, st.latitude])) danger.add(k);
      if (safe.size) for (const c of ALL) if (!safe.has(key(c))) danger.add(key(c));
      return { danger, linger, safe, recast };
    };
    // A player remembers, for the rest of its turn, the marks it saw at the start of the turn (the server may have dropped
    // their visuals by its second action).
    const turnSeen = new Map<string, { danger: Set<string>; linger: Set<string>; safe: Set<string>; recast: Set<string> }>();
    const seenCells = () => {
      const now = dangerCells();
      const k = `${b.round}`;
      const prev = turnSeen.get(k);
      if (!prev) { turnSeen.clear(); turnSeen.set(k, now); return now; }
      for (const x of now.danger) prev.danger.add(x);
      for (const x of now.linger) prev.linger.add(x);
      for (const x of now.safe) prev.safe.add(x);
      for (const x of now.recast) prev.recast.add(x);
      return prev;
    };
    const free = (c: Cell) => !b.usersState.some((u: any) => u.longitude === c[0] && u.latitude === c[1] && alive(u));
    // Telegraph reading (real-player policy): one roll per new danger pattern, on its own seeded stream.
    const readP = o.policy === "play" ? (o.model.real?.readP ?? 1) : 0;
    const readRand = mulberry32((o.seed * 7919 + cfg.act) ^ 0x2ead1);
    let lastSig = "", reading = true;
    const reads = (danger: Set<string>) => {
      if (readP >= 1) return true;
      const sig = [...danger].sort().join(";");
      if (sig && sig !== lastSig) { lastSig = sig; reading = readRand() < readP; if (!reading) res.misreads = (res.misreads ?? 0) + 1; }
      return sig ? reading : true;
    };
    // Loop 11 (director 2026-11-05): a misread Recast counts as standing in its pattern (only misreaders pay; readP 1 never
    // reaches this). While the misread pattern is live the player steps onto its nearest hex and holds it.
    let recastPin: Set<string> | null = null;
    let misstep = false;
    const dodgedFrom = new Set<string>(); let dodgedRound = -1;
    let sitPos = ""; let sitHp: number | null = null; let sitRun = 0;
    const pinnedStay = (to: string) => !!recastPin && recastPin.size > 0 && !recastPin.has(to) && recastPin.has(key([pu().longitude, pu().latitude]));
    const dodgeStep = (): boolean => {
      const here: Cell = [pu().longitude, pu().latitude];
      const { danger, linger, recast } = seenCells();
      if (!recast.size) recastPin = null;
      if (!reads(danger)) {
        if (!recast.size || recast.has(key(here))) { if (recast.size) recastPin = recast; return false; }
        if (recastPin !== recast) { recastPin = recast; res.recastMisreads = (res.recastMisreads ?? 0) + 1; }
        // nearest free pattern hex, walking; Replacement when 2+ away
        const prev = new Map<string, string | null>([[key(here), null]]);
        const q: Cell[] = [here];
        let goal: string | null = null;
        while (q.length && !goal) {
          const c = q.shift()!;
          for (const n of ALL) if (!prev.has(key(n)) && dist(c, n) === 1 && free(n)) { prev.set(key(n), key(c)); if (recast.has(key(n))) { goal = key(n); break; } q.push(n); }
        }
        if (!goal) return false;
        const gc = goal.split(",").map(Number) as Cell;
        misstep = true;
        if (dist(here, gc) >= 2 && dist(here, gc) <= 5 && tryAction("replacementTechnique", gc)) return true;
        let st = goal;
        while (prev.get(st) !== key(here)) st = prev.get(st)!;
        if (tryAction("move", st.split(",").map(Number) as Cell)) return true;
        misstep = false; return false;
      }
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
        // pool-aware (2026-11-05 audit): a walking path never crosses a pool hex (each action begun on one drains 15%);
        // Replacement still jumps to any clean hex within 5.
        for (const n of ALL) if (!prev.has(key(n)) && dist(c, n) === 1 && free(n) && !(POOL_AWARE && linger.has(key(n)))) { prev.set(key(n), key(c)); depth.set(key(n), d + 1); q.push(n); }
      }
      // pool-aware: no clean hex by a pool-free walk -> Replacement to the nearest clean hex within 5, before any pool.
      if (POOL_AWARE && !found.length) {
        const jump = ALL.filter((c) => free(c) && !bad(key(c)) && dist(here, c) >= 1 && dist(here, c) <= 5).sort((a, c) => dist(here, a) - dist(here, c))[0];
        if (jump && tryAction("replacementTechnique", jump)) return true;
        // still on a blast: walk the old way (pools allowed) rather than stand in it
        if (danger.has(key(here))) {
          const prev2 = new Map<string, string | null>([[key(here), null]]); const q2: Cell[] = [here]; let goal: string | null = null;
          while (q2.length && !goal) { const c = q2.shift()!; for (const n of ALL) if (!prev2.has(key(n)) && dist(c, n) === 1 && free(n)) { prev2.set(key(n), key(c)); if (!danger.has(key(n))) { goal = key(n); break; } q2.push(n); } }
          if (goal) { let st = goal; while (prev2.get(st) !== key(here)) st = prev2.get(st)!; return tryAction("move", st.split(",").map(Number) as Cell); }
        }
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
    let reqStartRound: number | null = null;
    let prevBossAlive = Object.fromEntries(cfg.bossIds.map((a) => [a, true]));
    for (let step = 0; step < maxRounds * 60; step++) {
      const pre = alignBattle(b, actionRounds, puid);
      if (pre.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
      if (b.round > maxRounds) break;
      const actor = pre.actor;
      const human = actor.userId === puid;
      // combat.ts:857-859: each performAction request (a human action plus the AI turns that follow it) ends by dropping
      // visual ground effects created before the round the request started in. A new request starts at every human action.
      if (human && !NO_VISUAL_FILTER) {
        if (reqStartRound !== null) b.groundEffects = b.groundEffects.filter((e: any) => e.type !== "visual" || e.createdRound >= reqStartRound!);
        reqStartRound = b.round;
      }
      tickClock(1000);
      const tk = `${b.round}:${actor.userId}`;
      if (!turnActs.has(tk)) turnActs.set(tk, []);
      const hpBefore = new Map(b.usersState.map((u: any) => [u.userId, u.curHealth]));
      // Telegraph audit: the drawn danger art (tg_heavy carriers / visuals) on the floor just before this action.
      const drawnBefore = new Set<string>((b.groundEffects as any[]).filter((g) => (g.type === "visual" || g.type === "increaseregeneration") && (g.staticAnimation === "tg_heavy" || g.staticAnimation === "tg_control") && ((g.rounds ?? 0) > 0 || g.castThisRound)).map((g) => `${g.longitude},${g.latitude}`));
      const pPos: Cell = [pu().longitude, pu().latitude];
      const aPos: Cell = [actor.longitude, actor.latitude];
      const apBefore = human ? (pu().actionPoints ?? 0) : 0;
      let actionId: string | undefined;
      // Solvability (director 2026-11-05): at the start of every player turn, is there a free hex within reach (Replacement
      // range 5, or the hex he stands on) that no live mark covers? Ground truth, independent of the player's read.
      if (human && turnActs.get(tk)!.length === 0) {
        // Safe-sit audit (director 2026-11-05): consecutive player turns begun on the same hex with no loss from the
        // boss side since the previous turn start.
        const hpNow = pu().curHealth;
        const sameHex = sitPos === key(pPos);
        const unhurt = sitHp !== null && hpNow >= sitHp;
        sitRun = sameHex && unhurt ? sitRun + 1 : 0;
        (res as any).maxSafeSit = Math.max((res as any).maxSafeSit ?? 0, sitRun);
        sitPos = key(pPos); sitHp = hpNow;
        const { danger, linger } = dangerCells();
        const sv = (res.solv ??= { turns: 0, noSafe: 0, noSafeInclPools: 0, noSafeRounds: [] });
        sv.turns++;
        if (danger.size) {
          const reach = ALL.filter((c) => (key(c) === key(pPos) || free(c)) && dist(c, pPos) <= 5).map(key);
          if (!reach.some((k) => !danger.has(k))) { sv.noSafe++; sv.noSafeRounds.push(pre.actionRound); }
          if (!reach.some((k) => !danger.has(k) && !linger.has(k))) sv.noSafeInclPools++;
        }
      }
      if (human && o.policy === "play" && (misstep = false, dodgeStep())) { if (misstep) actionId = "misstep"; else { actionId = "dodge"; res.dodges++; if (P_NO_REENTRY) { if (dodgedRound !== b.round) { dodgedFrom.clear(); dodgedRound = b.round; } dodgedFrom.add(key(pPos)); } } }
      else if (human && o.policy !== "ignore" && wantsCleanse(b, puid, !!o.model.real) && tryAction("cleanse", pPos)) { actionId = "cleanse"; res.cleanses++; }
      else if (human && o.policy === "play" && A3_ON && cfg.act === 3 && o.model.real && A3_POLICY.topUpBelow && (() => {
        // The heal cut was announced (The Names Stir) and has not landed: top up now (the read the warning asks for).
        const st = bossU(AI.saint);
        const stirred = st && (lastBossAct.get(st.userId) ?? []).some((h) => h.id === J3.stir) && !(lastBossAct.get(st.userId) ?? []).some((h) => h.id === J3.mended);
        if (!stirred || pu().curHealth / maxHp >= A3_POLICY.topUpBelow / 100) return false;
        // The real kit's HP sustain is lifesteal (Eclipse Drain, the Chakra Pill, gear); the Energy Potion restores chakra and stamina only.
        for (const id of ["ou7VyChQ-SFCm8T8yGS7I", "tZTvqYWiAc_OrY64nDvIo"]) if (!b.usersEffects.some((e: any) => e.targetId === puid && e.type === "lifesteal" && e.creatorId === puid && (e.rounds ?? 0) > 0 && (e.rounds ?? 0) < 100) && tryAction(id, pPos)) { topUpId = id; return true; }
        return false;
      })()) { actionId = topUpId; res.specials["Top-up after the warning"] = (res.specials["Top-up after the warning"] ?? 0) + 1; }
      else if (human && o.policy !== "ignore" && o.model.real && (() => { const t = chooseTarget(); return t && (A3_ON && cfg.act === 3 ? wantsClearA3(b, t) : wantsClear(b, t)) && dist(pPos, [t.longitude, t.latitude]) <= 4 && tryAction("clear", [t.longitude, t.latitude]); })()) { actionId = "clear"; res.clears = (res.clears ?? 0) + 1; }
      else {
        if (human) setPlayerTarget(o.policy !== "ignore" ? chooseTarget() : null);
        const r = performAIaction(b, grid, actor.userId);
        actionId = r.nextActionId;
        // While the caster carries a disarm marker (the live Omen: Fanned Lines' marker) the engine performs its next
        // action but returns no nextActionId (observed, cause not traced; moe_probe P12). Recover it from the log line.
        if (!actionId && r.aiDescriptions?.length) {
          const d = r.aiDescriptions[0]!;
          actionId = (cfg.rows[actor.controllerId]?.jutsus ?? []).map((uj: any) => uj.jutsuId).find((id: string) => { const rec = cfg.recs[id]; return rec && d.startsWith(`${rec.name}: ${String(rec.battleDescription).replace(/%user/g, actor.username).split("%")[0]}`.slice(0, 60)); });
          if (!actionId && o.trace) res.trace!.push(`   (unmatched log line: ${d.slice(0, 90)})`);
        }
        if (human && o.policy === "play" && (actionId === "move" || actionId === "replacementTechnique")) {
          const after = r.nextBattle.usersState.find((u: any) => u.userId === puid)!;
          const { danger, linger } = seenCells();
          const k = `${after.longitude},${after.latitude}`;
          // Pools are crossed to reach a target that is out of reach (a player walks through a pool rather than stall);
          // a step onto a pool is refused only when the target is already within attack range (4).
          const tgt = currentTarget ?? chooseTarget();
          const needApproach = !!tgt && dist([after.longitude, after.latitude], [tgt.longitude, tgt.latitude]) < dist(pPos, [tgt.longitude, tgt.latitude]) && dist(pPos, [tgt.longitude, tgt.latitude]) > 4;
          const reentry = P_NO_REENTRY && linger.has(k) && dodgedRound === b.round && dodgedFrom.has(k);
          if (pinnedStay(k) || (danger.has(k) && !recastPin?.has(k)) || (linger.has(k) && (POOL_AWARE || !needApproach || reentry))) { actionId = tryAction("wait", pPos) ? "wait" : undefined; if (!actionId) b = r.nextBattle; }
          else b = r.nextBattle;
        } else if (human && o.policy === "camp" && (actionId === "move" || actionId === "replacementTechnique")) {
          // camp: holds the act's best fixed hex (fewest marks in the coverage audit) and never moves
          actionId = tryAction("wait", pPos) ? "wait" : undefined; if (!actionId) b = r.nextBattle;
        } else b = r.nextBattle;
      }
      if (human) {
        // AP review: what this action cost and what kind of action it was (wait / none = unspent).
        const spent = Math.max(0, apBefore - (pu().actionPoints ?? 0));
        const a = (res.ap ??= { turns: 0, move: 0, attack: 0, buff: 0, answer: 0, other: 0, unspent: 0, turnsUnspent20: 0 });
        const tkAp = `${b.round}`;
        const id = actionId ?? "none";
        const rec = b.extraState.jutsus[id] ?? (o.model.real ? capturedItems()[id] : undefined);
        const hurts = (r: any) => !!r && r.target !== "SELF" && (r.effects ?? []).some((e: any) => ["damage", "pierce", "elementaldamage", "afterburn"].includes(e.type));
        const cat = ["dodge", "move", "replacementTechnique", "misstep"].includes(id) ? "move" : ["clear", "cleanse"].includes(id) ? "answer"
          : id === "basicAttack" || hurts(rec) ? "attack" : rec ? "buff" : ["wait", "none"].includes(id) ? "" : "other";
        if (cat) (a as any)[cat] += spent;
        (apTurn as any)[tkAp] = ((apTurn as any)[tkAp] ?? 0) + (cat ? spent : 0);
      }
      const post = alignBattle(b, actionRounds, puid);
      if (post.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(post.actionRound)) actionRounds.push(post.actionRound);
      if (!actionId && actor.isAutoCombat) b.roundStartAt = new Date(Date.now() - 61_000);
      turnActs.get(tk)!.push(actionId ?? "none");
      if (human) {
        const nm = actionId === "dodge" ? "dodge" : (b.extraState.jutsus[actionId ?? ""]?.name ?? b.extraState.items?.[actionId ?? ""]?.name ?? (o.model.real ? capturedItems()[actionId ?? ""]?.name : undefined) ?? actionId ?? "none");
        (res.playerActs ??= {})[nm] = (res.playerActs[nm] ?? 0) + 1;
        res.minHpFrac = Math.min(res.minHpFrac ?? 1, Math.max(0, pu().curHealth) / maxHp);
      }
      const pAfter = pu();
      const pLoss = Math.max(0, (hpBefore.get(puid) ?? 0) - pAfter.curHealth);
      const pGain = Math.max(0, pAfter.curHealth - (hpBefore.get(puid) ?? 0));
      if (pGain > 0) res.healed += pGain;
      const isEnemy = actor.direction === "right";
      const src = human ? "own turn (pools/drain)" : isEnemy ? (SETS[actionId ?? ""]?.[0] ?? name(actionId)) : "own side";
      if (pLoss > 0) {
        const label = isEnemy ? `${actor.isSummon ? actor.username : (actor.username ?? "")}: ${src}` : src;
        res.dmgBySource[label] = (res.dmgBySource[label] ?? 0) + pLoss;
        if (isEnemy && !actor.isSummon && actionId === JID.lancet) { const l = (res.lancet ??= { n: 0, sum: 0, max: 0, pctOfMax: [] }); l.n++; l.sum += pLoss; l.max = Math.max(l.max, pLoss); l.pctOfMax.push(Math.round(1000 * pLoss / maxHp) / 10); }
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
            if (!ok) {
              s.unmarked++; res.unmarkedTotal++;
              // Was the pattern still drawn when it landed (bookkeeping only), or did it land with no art up (a real unwarned hit)?
              const drawn = [...cells].filter((k) => drawnBefore.has(k)).length;
              if (drawn) (res as any).unmarkedButDrawn = ((res as any).unmarkedButDrawn ?? 0) + 1;
              else (res as any).unwarned = ((res as any).unwarned ?? 0) + 1;
              if (o.trace) res.trace!.push(`   UNMARKED ${name(actionId)}: ${drawn}/${cells.size} pattern hexes still drawn`);
            }
          }
        }
        if (actionId === JID.quietFall) for (const k of Object.keys(etchCount)) etchCount[k] = 0;
        hist.push({ id: actionId, round: pre.actionRound });
        lastBossAct.set(actor.userId, hist);
      }
      if (isEnemy && actionId && SPECIAL_IDS[actionId]) res.specials[SPECIAL_IDS[actionId]!] = (res.specials[SPECIAL_IDS[actionId]!] ?? 0) + 1;
      if (isEnemy && (actionId === J3.mended || actionId === J3.impression)) ((res as any).phaseAt ??= {})[actionId === J3.mended ? "II" : "III"] ??= pre.actionRound; if (isEnemy && (actionId === J3.mended || actionId === J3.impression)) ((res as any).phaseHp ??= {})[actionId === J3.mended ? "II" : "III"] ??= Math.round(100 * actor.curHealth / actor.maxHealth);
      for (const aid of cfg.bossIds) {
        const u = bossU(aid);
        const a = alive(u);
        if (prevBossAlive[aid] && !a && !res.killFirst) res.killFirst = aid;
        prevBossAlive[aid] = a;
      }
      if (o.trace) {
        const bossTxt = cfg.bossIds.map((aid) => { const u = bossU(aid); return u ? `${aid.replace("moe-ai-", "")} ${(100 * Math.max(0, u.curHealth) / u.maxHealth).toFixed(0)}%` : ""; }).join(" ");
        if (DEBUG_TRACE && !human && !actor.isSummon && actor.direction === "right") { const au = b.usersState.find((x: any) => x.userId === actor.userId); res.trace!.push(`   [dbg ${actor.username?.slice(0, 10)} ap ${au?.actionPoints} fx ${b.usersEffects.filter((e: any) => e.targetId === actor.userId && !(e.rounds >= 80)).map((e: any) => `${e.type}:${e.power}/${e.rounds}`).join(",")}]`); }
        res.trace!.push(`r${pre.actionRound} ${(human ? `PLAYER>${(currentTarget?.username ?? "-").slice(0, 8)}` : actor.username ?? "?").slice(0, 22).padEnd(22)} ${String(actionId === "dodge" ? "DODGE" : actionId === "misstep" ? "MISSTEP (misread Recast)" : name(actionId)).slice(0, 28).padEnd(28)} p@${pPos} hp ${Math.round(pAfter.curHealth)} (${pLoss ? "-" + Math.round(pLoss) : pGain ? "+" + Math.round(pGain) : "0"}) | ${bossTxt}`);
      }
      if (human && pLoss > 0) {
        // Own-turn loss by cause (pool-death audit, director 2026-11-05): the ground under the player when he acted, and
        // the drains on him.
        const here0 = `${pPos[0]},${pPos[1]}`;
        const gs = (b.groundEffects as any[]).filter((e) => `${e.longitude},${e.latitude}` === here0 && (e.rounds ?? 0) > 0).map((e) => String(e.actionId ?? ""));
        const onP = b.usersEffects.filter((e: any) => e.targetId === puid && e.type === "drain" && (e.rounds ?? 0) > 0 && !e.fromGround).map((e: any) => String(e.actionId ?? ""));
        const cause = gs.some((x) => x.includes("turns")) ? "follow-mark ring" : gs.some((x) => x.includes("hush") || x.includes("rises")) ? "Hush / Rises pool" : gs.some((x) => x.includes("refraction") || x.includes("facet") || x.includes("stillness") || x.includes("blast") || x.includes("shatter") || x.includes("glass")) ? "eruption pool" : onP.some((x) => x.includes("grasp")) ? "Grasp drain" : gs.length ? `other ground` : "recoil / reflect / other";
        const ob = ((res as any).ownTurnBy ??= {}); ob[cause] = (ob[cause] ?? 0) + pLoss;
        if (pAfter.curHealth <= 0) (res as any).ownTurnDeath = cause;
      }
      if (o.trace && human && pLoss > 0) {
        const here = `${pPos[0]},${pPos[1]}`;
        const g = (b.groundEffects as any[]).filter((e) => `${e.longitude},${e.latitude}` === here && (e.rounds ?? 0) > 0).map((e) => `${e.type}:${e.actionId ?? ""}`);
        const fx = b.usersEffects.filter((e: any) => e.targetId === puid && ["drain", "poison", "moveprevent", "stun", "healprevent", "decreaseheal"].includes(e.type) && (e.rounds ?? 0) > 0).map((e: any) => `${e.type}${e.fromGround ? "(ground)" : ""}:${e.actionId ?? ""}`);
        res.trace!.push(`   (own-turn loss ${Math.round(pLoss)} at ${here}; ground ${[...new Set(g)].join(",") || "-"}; on player ${[...new Set(fx)].join(",") || "-"})`);
      }
      if (o.trace && isEnemy && !actor.isSummon && (actionId === "wait" || !actionId)) res.trace!.push(`   (${actor.username?.slice(0, 12)} waits; effects: ${[...new Set(b.usersEffects.filter((e: any) => e.targetId === actor.userId && (e.rounds ?? 0) > 0).map((e: any) => e.type))].join(",")})`);
      const side = (dir: string) => b.usersState.some((u: any) => u.direction === dir && !u.isSummon && alive(u));
      if (!alive(pu())) { res.outcome = "lost"; break; }
      if (!side("right")) { res.outcome = "won"; break; }
    }
    for (const [k, acts] of turnActs) if (k.split(":")[1] === puid) { res.playerTurns = (res.playerTurns ?? 0) + 1; if (acts.every((x) => x === "wait" || x === "none")) res.playerEndTurns = (res.playerEndTurns ?? 0) + 1; }
    if (res.ap) { const ts = Object.values(apTurn); res.ap.turns = ts.length; res.ap.unspent = ts.reduce((s, v) => s + Math.max(0, 100 - v), 0); res.ap.turnsUnspent20 = ts.filter((v) => v <= 80).length; }
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
const wantsCleanse = (b: any, puid: string, real = false) =>
  b.usersEffects.filter((e: any) => e.targetId === puid && e.type === "increasedamagetaken" && (e.rounds ?? 0) > 0).length >= 2 ||
  // real player (logs): Cleanse right after a root or a drain from an enemy action (not ground pools, which re-apply)
  (real && b.usersEffects.some((e: any) => e.targetId === puid && !e.fromGround && (e.type === "moveprevent" || e.type === "drain") && (e.rounds ?? 0) > 0 && e.creatorId !== puid)) ||
  // skilled (pass 6): Cleanse the eruption debuff (Act II, Nothing Moves) when it is on and HP is below 70%
  (real && SKILLED && (() => { const u = b.usersState.find((x: any) => x.userId === puid); return u && u.curHealth / u.maxHealth < 0.7; })() &&
    b.usersEffects.some((e: any) => e.targetId === puid && !e.fromGround && e.type === "decreaseheal" && e.creatorId !== puid && (e.rounds ?? 0) > 0));
/** Real player (logs): Clear the target right after it gains a clearable combat buff (not innate rows; not clear-proof). */
/** Act III redesign: Clear her Cradle (jutsu decreasedamagetaken), or the ramp once it carries A3.clearRampStacks stacks. */
const wantsClearA3 = (b: any, t: any) => {
  const live = (type: string) => b.usersEffects.filter((e: any) => e.targetId === t.userId && e.type === type && e.fromType === "jutsu" && e.creatorId === t.userId && (e.rounds ?? 0) > 0 && (e.rounds ?? 0) < 100);
  if (b.usersEffects.some((e: any) => e.targetId === t.userId && e.type === "clearprevent" && (e.rounds ?? 0) > 0)) return false;
  return live("decreasedamagetaken").length > 0 || live("increasedamagegiven").length >= (A3_POLICY?.clearRampStacks ?? 3);
};
const wantsClear = (b: any, t: any) =>
  !b.usersEffects.some((e: any) => e.targetId === t.userId && e.type === "clearprevent" && (e.rounds ?? 0) > 0) &&
  // Ramp worth clearing: 3+ live Lancet stacks (about +22%); any other clearable buff (the Silence's absorb) as before.
  (!RAMP_CLEARABLE || b.usersEffects.filter((e: any) => e.targetId === t.userId && e.type === "increasedamagegiven" && e.creatorId === t.userId && e.fromType === "jutsu" && (e.rounds ?? 0) > 0 && (e.rounds ?? 0) < 100).length >= 3 ||
    b.usersEffects.some((e: any) => e.targetId === t.userId && e.type === "absorb" && (e.rounds ?? 0) > 0)) &&
  b.usersEffects.some((e: any) => e.targetId === t.userId && e.fromType === "jutsu" && e.creatorId === t.userId && (e.rounds ?? 0) > 0 && (e.rounds ?? 0) < 100 &&
    ["increasedamagegiven", "decreasedamagetaken", "absorb", "increasestat", "lifesteal"].includes(e.type));
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
let NO_VISUAL_FILTER = false;
/** Analysis only: switch the combat.ts:857-859 visual filter off (pass-2 behaviour) to measure what it alone changes. */
export const setNoVisualFilter = (v: boolean) => { NO_VISUAL_FILTER = v; };
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
