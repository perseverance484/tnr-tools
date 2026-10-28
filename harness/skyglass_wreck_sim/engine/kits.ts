/**
 * Skyglass Wreck dungeon copies: kits, priority rules and dungeon-only jutsu (endgame set).
 *
 * Sources: docs/design/SKYGLASS_WRECK_ENCOUNTERS.md (roles, crew kits and rules, new jutsu),
 * docs/design/SKYGLASS_BOSS_FIGHTS.md sections 1-2 (The Captain, the Core Horror: named moves,
 * battle-log lines, set pieces), SKYGLASS_BOSS_ANIMATIONS.md (animation placeholder ids),
 * RUL-2026-10-28-001/-006/-007. Every jutsu is validated by the live JutsuValidator and every
 * rule by the live AiRule schema (kitlib).
 *
 * Engine facts this relies on (harness probes, results/probe_boss.json, probe_telegraph.json):
 * - Set pieces: a 100 AP telegraph lays visual marks (tg_*) and a self marker; the 100 AP
 *   detonation fires on the caster's next turn when its has_effect rule sees the marker.
 * - Markers are `increasecooldown` with no actionsAffected (no gameplay effect), 1 round. They are
 *   NOT `increasepoolcost`: that type is in SHARED_COOLDOWN_TAGS, so a jutsu carrying it puts every
 *   other increasepoolcost jutsu of the caster on the 3-round global cooldown (a second marker
 *   jutsu then never fires). A 1-round marker is present on the next turn only (no stale marker).
 * - Detonations that stun, push or root use target CHARACTER: on a GROUND jutsu only the damage
 *   lands; stun / push do not. CHARACTER + COORDINATES / AOE_SPIRAL_SHOOT with the rule target SELF
 *   hits the pattern, spares the caster (friendlyFire ENEMIES) and the safe hexes.
 * - Rings use AOE_SPIRAL_SHOOT (disc of radius `range` minus the caster): hex-correct, no row parity.
 *   Arena patterns use BATTLEFIELD coordinates: absolute, no parity. So no pattern here depends on
 *   row parity.
 */
import { anim, cast, cond, copyJutsu, endTurn, highest, jutsu, moveTo, rule, T, tag } from "./kitlib";

export type KitParams = {
  /** AI level of every dungeon copy except the Seal Charge (endgame: unset = captured level 100). */
  level?: number;
  /** AI statsMultiplier for those copies (replayed through scaleEditedAi; captured crew: 5). */
  statsMultiplier?: number;
  /**
   * Innate +damage-taken % rows on the crew (each row capped at 100 by the engine; rows multiply). The level 40-60 version
   * needs it: pools and stats multipliers cannot go below 1 (insertAiSchema), so a level-50 copy has at least
   * 2,550 HP, more than a level-50 party clears in the target time.
   */
  crewTaken?: number[];
  /** Same for the Core Horror and The Captain. */
  bossTaken?: number[];
  crewPools: number; crewRows: number;
  horrorPools: number; horrorRows: number;
  captainPools: number; captainRows: number;
  sealPools: number; sealRows: number;
  /** Damage powers of the new moves. */
  pow: Record<string, number>;
};

export const DEFAULT_PARAMS: KitParams = {
  crewPools: 1.0, crewRows: 2,
  horrorPools: 5, horrorRows: 2,
  captainPools: 2.5, captainRows: 3,
  sealPools: 2.0, sealRows: 3,
  pow: {
    chainHook: 45, oath: 35, collapse: 120, rupture: 100, rupturePool: 30, maw: 150, grasp: 80, bilge: 50,
    broadside: 110, bell: 50, wardDR: 60, aegisShield: 1500, mending: 20, rebuildHeal: 20, rebuildIDG: 50, gunwaleHP: 3000,
  },
};

const W = 12;
const H = 10;
const cells = (pred: (c: number, r: number) => boolean) => {
  const out: { longitude: number; latitude: number }[] = [];
  for (let c = 0; c < W; c++) for (let r = 0; r < H; r++) if (pred(c, r)) out.push({ longitude: c, latitude: r });
  return out;
};
const field = (selection: "ALL" | "EXCLUDE", coordinates: { longitude: number; latitude: number }[]) => ({ origin: "BATTLEFIELD", selection, coordinates, randomCount: 1 });
const at = (pts: [number, number][]) => pts.map(([longitude, latitude]) => ({ longitude, latitude }));

/** Rupture Field: three fixed scatter patterns (a third of the arena each, every marked hex has an unmarked neighbour). */
export const RUPTURE = [0, 1, 2].map((k) => cells((c, r) => ((c >> 1) + r) % 3 === k));
/** Maw of the Deep safe stars: phase 1 and phase 2 (columns <= 7, so never under the boss's spawn columns 8-9). */
export const MAW_STARS = [at([[6, 2], [5, 5], [6, 8]]), at([[4, 3], [7, 5], [4, 7]])];
/** Broadside: phase 1 two rows, phase 2 three rows; three rotating sets each. */
export const BROADSIDE = [
  [[2, 5], [3, 6], [1, 4]],
  [[1, 4, 7], [2, 5, 8], [3, 6, 0]],
].map((sets) => sets.map((rows) => cells((_c, r) => rows.includes(r))));

/** Innate +damage-taken row (built and validated like every tag; see KitParams.crewTaken). */
const takenRow = (pct: number) => tag("increasedamagetaken", { power: pct, rounds: 99, calculation: "percentage", description: "Increased damage taken" });
const idgRows = (n: number) =>
  Array.from({ length: n }, () => ({
    type: "increasedamagegiven", power: 100, rounds: 99, target: "INHERIT", appearSfx: "", direction: "offence",
    calculation: "percentage", description: "Increased damage given", disappearSfx: "", powerPerLevel: 0,
    appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "",
  }));

const ALL_STATS = ["None", "Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu"];
const ALL_GENERALS = ["Highest", "Strength", "Intelligence", "Willpower", "Speed"];

/** Dungeon AI ids (harness placeholders; the builder mints real ids on create). */
export const IDS = {
  warden: "dg-deck-warden", charge: "dg-seal-charge", sentinel: "dg-skyglass-sentinel", blade: "dg-first-blade",
  oath: "dg-oathkeeper", wayfinder: "dg-wayfinder", horror: "dg-core-horror", captain: "dg-the-captain", sealwright: "dg-sealwright",
};
const BASE: Record<string, string> = {
  [IDS.warden]: "Deck Warden", [IDS.charge]: "Seal Charge", [IDS.sentinel]: "Skyglass Sentinel", [IDS.blade]: "First Blade",
  [IDS.oath]: "Oathkeeper", [IDS.wayfinder]: "Wayfinder", [IDS.horror]: "Core Horror", [IDS.captain]: "The Captain", [IDS.sealwright]: "Sealwright",
};

/**
 * Level 40-60 version (SKYGLASS_WRECK_ENCOUNTERS.md "Level 40-60 version"): the same arcs with level-50 copies and
 * lighter kits. Rules whose notes start with these prefixes are left out of that version's copies.
 */
const LVL50_DROP: Record<string, string[]> = {
  [IDS.warden]: ["Quick Strike"],
  [IDS.sentinel]: ["Counter Stance", "Rigging Snare"],
  [IDS.blade]: ["Glassveil Step", "Shuriken Storm", "Numbing Senbon"],
  [IDS.oath]: ["Opening Strike"],
  [IDS.wayfinder]: ["Keelbind", "Afterimage Decoy"],
  // One phase of set pieces (no Undertow, no faster phase-2 cycle, no pools, no second Maw); The Core Rebuilds stays.
  [IDS.horror]: ["Undertow", "Maw of the Deep II", "Collapse mark (phase 2)", "Rupture Field A mark (phase 2)", "Rupture Field B mark (phase 2)", "Rupture Field C mark (phase 2)", "Rupture Field A (pools)", "Rupture Field B (pools)", "Rupture Field C (pools)"],
  // Two phases kept (Last Stand, faster Bell, three-row Broadside); no Sealwright, so no Gunwale; a short duel kit.
  [IDS.captain]: ["Raise the Gunwale", "Stolen Form", "Suppression Writ", "Counter Stance", "Ruin Refrain", "Unraveling Strike", "Explosive Tag Cataclysm", "Windlash Focus"],
};

export const buildEndgame = (P: KitParams = DEFAULT_PARAMS, version: "endgame" | "lvl50" = "endgame") => {
  const l50 = version === "lvl50";
  const aid = (id: string) => (l50 ? `${id}-l50` : id);
  const trim = (id: string, rules: any[]) => (l50 ? rules.filter((r) => !(LVL50_DROP[id] ?? []).some((d) => r.action.description.startsWith(d))) : rules);
  const J: Record<string, any> = {};
  const add = (j: any) => {
    J[j.id] = j;
    return j.id as string;
  };
  const p = P.pow;
  const tele = (id: string, name: string, line: string, method: string, range: number, marks: any[], markerPower: number, ct?: any, cooldown = 3) =>
    add(jutsu(id, { name, description: `Telegraph: ${name}.`, battleDescription: line, target: "GROUND", method, range, cooldown, actionCostPerc: 100, coordinateTargeting: ct, effects: [...marks, T.marker(markerPower)] }));

  /* ---------------- crew: dungeon-only jutsu ---------------- */
  const chainHook = add(jutsu("dg-chain-hook", {
    name: "Chain Hook", description: "A weighted chain hooks a target, drags them in and pins them.",
    battleDescription: "%user hurls a weighted chain and drags %target across the deck.",
    target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 3, actionCostPerc: 60,
    // Probe Q4: a same-cast root does not cancel the pull (either row order); no split needed.
    effects: [T.damage(p.chainHook!, { appearAnimation: anim("chain-hook-hit") }), T.pull(3), T.root(1)],
  }));
  const oath = add(jutsu("dg-oath-of-stillness", {
    name: "Oath of Stillness", description: "A binding oath that slows the target's footwork.",
    battleDescription: "%user speaks the oath; %target's footing turns to stone.",
    target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 4, actionCostPerc: 60,
    // increasecooldown only adjusts basic actions (actions.ts); it cannot touch jutsu cooldowns.
    effects: [T.damage(p.oath!), tag("increasecooldown", { power: 2, rounds: 2, actionsAffected: ["move", "replacementTechnique"] })],
  }));
  const chartMark = add(jutsu("dg-chart-mark", {
    name: "Chart Mark", description: "Marks a target on the chart; the crew converge on it.",
    battleDescription: "%user marks %target on the chart. \"There.\"",
    target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 4, actionCostPerc: 40,
    effects: [
      T.pct("increasedamagetaken", 40, 2, { staticAnimation: anim("mark-sigil") }),
      // RUL-2026-10-28-001 marker; poolsAffected [] so it changes no costs (a pure marker).
      tag("increasepoolcost", { power: 5, rounds: 2, calculation: "percentage", poolsAffected: [] }),
    ],
  }));
  const aegis = add(jutsu("dg-skyglass-aegis", {
    name: "Skyglass Aegis", description: "A pane of skyglass forms around an ally.",
    battleDescription: "%user raises a pane of skyglass around %target.",
    target: "ALLY", method: "SINGLE", range: 4, cooldown: 4, actionCostPerc: 40, donor: "xs-8r_KRJS8QQMpBDyhUv",
    effects: [tag("shield", { power: 100, health: p.aegisShield, rounds: 2, friendlyFire: "FRIENDLY", staticAnimation: anim("skyglass-pane") }), tag("absorb", { power: 20, rounds: 2, friendlyFire: "FRIENDLY", calculation: "percentage" })],
  }));
  const mending = add(jutsu("dg-mending-seal", {
    name: "Mending Seal", description: "A seal that knits wounds and lifts afflictions from an ally.",
    battleDescription: "%user presses a mending seal to %target.",
    target: "ALLY", method: "SINGLE", range: 5, cooldown: 4, actionCostPerc: 40, donor: "xs-8r_KRJS8QQMpBDyhUv",
    effects: [T.heal(p.mending!, { friendlyFire: "FRIENDLY" }), T.cleanse({ friendlyFire: "FRIENDLY" })],
  }));
  const ward = add(jutsu("dg-ward-of-command", {
    name: "Ward of Command", description: "The Sealwright's ward on the Captain: heavily reduced damage while she stands.",
    battleDescription: "%user binds the command ward to %target.",
    target: "ALLY", method: "SINGLE", range: 5, cooldown: 2, actionCostPerc: 40, donor: "xs-8r_KRJS8QQMpBDyhUv",
    effects: [T.pct("decreasedamagetaken", p.wardDR!, 2, { friendlyFire: "FRIENDLY", staticAnimation: anim("cp_command") })],
  }));
  const wardenOpener = add(copyJutsu("_9k7kSYUgMtB-AEFgRly5", "dg-warden-resolve", { name: "Warden's Resolve", cooldown: 99, battleDescription: "%user sets his feet on the deck." }));
  const vanish = add(copyJutsu("IBjVpLutojh3m9PRnIce-", "dg-first-blade-vanish", { name: "Glassveil Step", cooldown: 99, battleDescription: "%user steps behind a sheet of skyglass light and is gone." }));
  const decoy = add(copyJutsu("LQ26G2ANWkbTRL7Ry__F0", "dg-wayfinder-decoy", { name: "Afterimage Decoy", cooldown: 6, battleDescription: "%user leaves an afterimage on the chart lines." }));
  const wfKeel = add(copyJutsu("PdD44PGaNv4MN5fOALhAF", "dg-wayfinder-keelbind", { name: "Keelbind", battleDescription: "%user lashes %target to the keel." }));

  /* ---------------- Core Horror ---------------- */
  const H_M = { collapse: 1, undertow: 2, rupA: 10, rupB: 20, rupC: 30, rupA2: 15, rupB2: 25, rupC2: 35, maw1: 50, maw2: 60 };
  const grasp = add(jutsu("dg-splintered-grasp", { name: "Splintered Grasp", description: "Heavy melee and a bleeding wound.", battleDescription: "Timber and rope lash out from the mass.", target: "OTHER_USER", method: "SINGLE", range: 1, cooldown: 1, actionCostPerc: 60, effects: [T.damage(p.grasp!, { appearAnimation: anim("ch_claw") }), tag("wound", { power: 30, rounds: 2 })] }));
  const bilge = add(jutsu("dg-bilge-spit", { name: "Bilge Spit", description: "Range 5 (design: 4; widened so he always has a reply at range): damage and a poison.", battleDescription: "A glob of black bilge arcs across the hold.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 1, actionCostPerc: 60, effects: [T.damage(p.bilge!, { appearAnimation: anim("ch_bile_spit") }), tag("poison", { power: 20, rounds: 2 })] }));
  const collapseT = tele("dg-collapse-mark", "Collapse", "The planks around it groan and split.", "AOE_SPIRAL_SHOOT", 2, [T.visual(anim("tg_heavy"), 1)], H_M.collapse, undefined, 4);
  // Collapse costs 60 AP so the 40 AP Undertow can follow in the same turn (two-marker chain).
  J[collapseT]!.actionCostPerc = 60;
  const collapseD = add(jutsu("dg-collapse", { name: "Collapse", description: "The deck caves in around him.", battleDescription: "The deck caves in.", target: "CHARACTER", method: "AOE_SPIRAL_SHOOT", range: 2, cooldown: 2, actionCostPerc: 100, effects: [T.damage(p.collapse!, { appearAnimation: anim("ch_collapse") }), T.beat()] }));
  const undertow = add(jutsu("dg-undertow", { name: "Undertow", description: "During a Collapse mark: a player is dragged 3 hexes toward him, into the ring.", battleDescription: "Black water drags %target toward the breach.", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 4, actionCostPerc: 40, effects: [T.pull(3, { appearAnimation: anim("ch_undertow") }), T.marker(H_M.undertow)] }));
  const rupT = RUPTURE.map((pat, k) => tele(`dg-rupture-mark-${"abc"[k]}`, "Rupture Field", "Rot swells under the floorboards.", "COORDINATES", 0, [T.visual(anim("tg_heavy"), 1)], [H_M.rupA, H_M.rupB, H_M.rupC][k]!, field("ALL", pat), 9));
  const rupD = RUPTURE.map((pat, k) => add(jutsu(`dg-rupture-${"abc"[k]}`, { name: "Rupture Field", description: "The rot erupts.", battleDescription: "The rot erupts through the floor.", target: "CHARACTER", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: 100, coordinateTargeting: field("ALL", pat), effects: [T.damage(p.rupture!, { appearAnimation: anim("ch_rupture") }), T.beat()] })));
  const rupT2 = RUPTURE.map((pat, k) => tele(`dg-rupture2-mark-${"abc"[k]}`, "Rupture Field", "Rot swells under the floorboards.", "COORDINATES", 0, [T.visual(anim("tg_heavy"), 1)], [H_M.rupA2, H_M.rupB2, H_M.rupC2][k]!, field("ALL", pat), 6));
  // Phase 2: GROUND, so the eruption leaves a lingering pool (ground damage + tg_linger) where it lands.
  const rupD2 = RUPTURE.map((pat, k) => add(jutsu(`dg-rupture2-${"abc"[k]}`, { name: "Rupture Field", description: "The rot erupts and pools.", battleDescription: "The rot erupts and pools on the deck.", target: "GROUND", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: 100, coordinateTargeting: field("ALL", pat), effects: [T.damage(p.rupture!, { appearAnimation: anim("dt_linger") }), T.pool(p.rupturePool!, 2), T.visual(anim("tg_linger"), 2)] })));
  const mawT = MAW_STARS.map((stars, k) => tele(`dg-maw-mark-${k + 1}`, "Maw of the Deep", "The water in the hold goes still. Three points of skyglass light remain.", "COORDINATES", 0,
    [T.visual(anim("tg_heavy"), 1), T.visual(anim("tg_safe"), 1, { target: "COORDINATES", coordinateTargeting: field("ALL", stars) })], k ? H_M.maw2 : H_M.maw1, field("EXCLUDE", stars), 99));
  const weakness = tag("weakness", { target: "SELF", rounds: 1, dmgModifier: 3, statTypes: ALL_STATS, generalTypes: ALL_GENERALS, power: 100, staticAnimation: anim("ch_exposed") });
  const mawD = MAW_STARS.map((stars, k) => add(jutsu(`dg-maw-${k + 1}`, { name: "Maw of the Deep", description: "Black water and teeth rise everywhere but the stars; then the seam splits open (Exposed Seam: x3 damage taken for 1 round).", battleDescription: "Black water and teeth rise from every plank. The mass splits open along a glowing seam.", target: "CHARACTER", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: 100, coordinateTargeting: field("EXCLUDE", stars), effects: [T.damage(p.maw!, { appearAnimation: anim("ch_maw") }), T.stun(1), weakness, ...(k ? [] : [T.beat()])] })));
  const rebuild = add(jutsu("dg-core-rebuilds", { name: "The Core Rebuilds", description: "Under 50%: heals once and enrages.", battleDescription: "Skyglass light floods the mass. It knits itself back together, wrong.", target: "SELF", method: "SINGLE", range: 0, cooldown: 99, actionCostPerc: 60, effects: [T.heal(p.rebuildHeal!, { target: "SELF" }), T.pct("increasedamagegiven", p.rebuildIDG!, 99, { target: "SELF", staticAnimation: anim("ch_enrage") })] }));

  const horrorRules = [
    cast("The Core Rebuilds (under 50%, once)", rebuild, "SELF", [cond.hp(50)]),
    // Detonations, highest marker first (one telegraph per turn, markers last one round).
    cast("Maw of the Deep II detonates", mawD[1]!, "SELF", [cond.marker(H_M.maw2)]),
    cast("Maw of the Deep detonates", mawD[0]!, "SELF", [cond.marker(H_M.maw1)]),
    cast("Rupture Field C (pools) detonates", rupD2[2]!, "SELF", [cond.marker(H_M.rupC2)]),
    cast("Rupture Field C detonates", rupD[2]!, "SELF", [cond.marker(H_M.rupC)]),
    cast("Rupture Field B (pools) detonates", rupD2[1]!, "SELF", [cond.marker(H_M.rupB2)]),
    cast("Rupture Field B detonates", rupD[1]!, "SELF", [cond.marker(H_M.rupB)]),
    cast("Rupture Field A (pools) detonates", rupD2[0]!, "SELF", [cond.marker(H_M.rupA2)]),
    cast("Rupture Field A detonates", rupD[0]!, "SELF", [cond.marker(H_M.rupA)]),
    cast("Collapse detonates", collapseD, "SELF", [cond.marker(H_M.collapse)]),
    // Two-marker chain: in the Collapse mark's turn (40 AP left) drag a far player into the ring.
    cast("Undertow (during a Collapse mark)", undertow, "RANDOM_OPPONENT", [cond.marker(H_M.collapse), cond.far(4, "RANDOM_OPPONENT")]),
    // Phase 1 beat after a detonation: plain attacks only.
    cast("beat: Splintered Grasp", grasp, "CLOSEST_OPPONENT", [cond.marker(1, "increaserange"), cond.near(1)]),
    cast("beat: Bilge Spit", bilge, "CLOSEST_OPPONENT", [cond.marker(1, "increaserange"), cond.near(5)]),
    endTurn("beat: hold", [cond.marker(1, "increaserange")]),
    // Telegraphs. Phase 2 (under 50%): set pieces back to back.
    cast("Maw of the Deep II mark (phase 2, once)", mawT[1]!, "SELF", [cond.hp(50)]),
    cast("Collapse mark (phase 2)", collapseT, "SELF", [cond.hp(50), cond.within(0, 2)]),
    ...rupT2.map((id, k) => cast(`Rupture Field ${"ABC"[k]} mark (phase 2)`, id, "SELF", [cond.hp(50)])),
    // Level 40-60: the fight is shorter, so the signature opens it.
    l50 ? cast("Maw of the Deep mark (once, opener)", mawT[0]!, "SELF") : cast("Maw of the Deep mark (once, from round 3)", mawT[0]!, "SELF", [cond.roundGt(2)]),
    cast("Collapse mark", collapseT, "SELF", [cond.within(0, 2)]),
    ...rupT.map((id, k) => cast(`Rupture Field ${"ABC"[k]} mark`, id, "SELF")),
    cast("Splintered Grasp", grasp, "CLOSEST_OPPONENT", [cond.near(1)]),
    cast("Bilge Spit", bilge, "CLOSEST_OPPONENT", [cond.near(5)]),
    endTurn("stationary: hold"),
  ];

  /* ---------------- The Captain ---------------- */
  const C_M = { bell: 1, bA: 10, bB: 20, bC: 30, bA2: 40, bB2: 50, bC2: 60 };
  const holdLine = add(copyJutsu("0Y10JpChssDwFUxNRk6p3", "dg-hold-the-line", { name: "Hold the Line", cooldown: 99, battleDescription: "%user plants his blade on the deck. \"Hold the line.\"" }));
  const lastStand = add(copyJutsu("MG9ZujAV8lK7--YxThVbQ", "dg-last-stand-at-the-helm", { name: "Last Stand at the Helm", cooldown: 99, battleDescription: "\"I have held this deck through worse than you.\"" }));
  const finalCmd = add(copyJutsu("X2P22h8ApDmTZHjWpNO87", "dg-final-command", { name: "Final Command", battleDescription: "\"Stand down.\"" }));
  const keel = add(copyJutsu("PdD44PGaNv4MN5fOALhAF", "dg-captain-keelbind", { name: "Keelbind", battleDescription: "%user lashes %target to the keel." }));
  const kitCopies = Object.fromEntries(
    ([
      ["_9k7kSYUgMtB-AEFgRly5", "windlash", "Windlash Focus"], ["1OhP0StX4VTsosWtCxhsG", "unraveling", "Unraveling Strike"],
      ["ddbIyVtoxdPQwLRXxSBq8", "writ", "Suppression Writ"], ["EQ93LX8wvuIAd5u75q_i1", "refrain", "Ruin Refrain"],
      ["o-4SCAhJ4LHdCwcBDgJrV", "cataclysm", "Explosive Tag Cataclysm"], ["STu1VHNcfgeC3x-UiQDgt", "secondwind", "Second Wind"],
      ["T3glZGcSd-jS8G-NB43GR", "counter", "Counter Stance"], ["VuFuBtE7h5B1nnA2J1lFZ", "stolen", "Stolen Form"],
    ] as const).map(([src, k, name]) => [k, add(copyJutsu(src, `dg-captain-${k}`, { name }))]),
  ) as Record<string, string>;
  const bellT = tele("dg-ships-bell-mark", "Ship's Bell", "\"All hands.\"", "AOE_SPIRAL_SHOOT", 2, [T.visual(anim("tg_control"), 1)], C_M.bell, undefined, 5);
  const bellD = add(jutsu("dg-ships-bell", { name: "Ship's Bell", description: "The great bell tolls: push 3 and a 1-round stun inside the ring.", battleDescription: "\"All hands.\" The great bell answers.", target: "CHARACTER", method: "AOE_SPIRAL_SHOOT", range: 2, cooldown: 2, actionCostPerc: 100, effects: [T.damage(p.bell!, { appearAnimation: anim("cp_bell_toll") }), T.push(3), T.stun(1)] }));
  const bsT = BROADSIDE.flatMap((sets, ph) => sets.map((pat, k) => tele(`dg-broadside${ph ? "2" : ""}-mark-${"abc"[k]}`, "Broadside", "%user raises a hand. \"Run out the guns.\"", "COORDINATES", 0, [T.visual(anim("tg_heavy"), 1)], [[C_M.bA, C_M.bB, C_M.bC], [C_M.bA2, C_M.bB2, C_M.bC2]][ph]![k]!, field("ALL", pat), ph ? 6 : 9)));
  const bsD = BROADSIDE.flatMap((sets, ph) => sets.map((pat, k) => add(jutsu(`dg-broadside${ph ? "2" : ""}-${"abc"[k]}`, { name: "Broadside", description: "The ship's guns fire down the marked rows.", battleDescription: "\"Fire.\"", target: "CHARACTER", method: "COORDINATES", range: 0, cooldown: 2, actionCostPerc: 100, coordinateTargeting: field("ALL", pat), effects: [T.damage(p.broadside!, { appearAnimation: anim("cp_broadside") }), ...(ph ? [] : [T.beat()])] }))));
  const gunwale = add(jutsu("dg-raise-the-gunwale", { name: "Raise the Gunwale", description: "A barrier line of timber and seals; it has its own health.", battleDescription: "%user barks an order; the gunwale rises.", target: "EMPTY_GROUND", method: "AOE_WALL_SHOOT", range: 3, cooldown: 8, actionCostPerc: 60, donor: "i4lGrYY5HNN2Q2GPToKUS", effects: [tag("barrier", { power: 100, rounds: 3, curHealth: p.gunwaleHP, maxHealth: p.gunwaleHP, absorbPercentage: 50, staticAnimation: anim("cp_gunwale") })] }));

  const captainRules = [
    cast("Hold the Line (opener, once)", holdLine, "SELF"),
    cast("Last Stand at the Helm (under 50%, once)", lastStand, "SELF", [cond.hp(50)]),
    cast("Broadside C (3 rows) fires", bsD[5]!, "SELF", [cond.marker(C_M.bC2)]),
    cast("Broadside B (3 rows) fires", bsD[4]!, "SELF", [cond.marker(C_M.bB2)]),
    cast("Broadside A (3 rows) fires", bsD[3]!, "SELF", [cond.marker(C_M.bA2)]),
    cast("Broadside C fires", bsD[2]!, "SELF", [cond.marker(C_M.bC)]),
    cast("Broadside B fires", bsD[1]!, "SELF", [cond.marker(C_M.bB)]),
    cast("Broadside A fires", bsD[0]!, "SELF", [cond.marker(C_M.bA)]),
    cast("Ship's Bell tolls", bellD, "SELF", [cond.marker(C_M.bell)]),
    ...(l50 ? [] : [cast("Ship's Bell mark (phase 2)", bellT, "SELF", [cond.hp(50), cond.within(0, 2)])]),
    ...bsT.slice(3).map((id, k) => cast(`Broadside ${"ABC"[k]} mark (phase 2, 3 rows)`, id, "SELF", [cond.hp(50)])),
    ...(l50 ? [cast("Ship's Bell mark (phase 2)", bellT, "SELF", [cond.hp(50), cond.within(0, 2)])] : []),
    // Level 40-60: Broadside (his signature) ahead of the Bell, so the shorter fight shows it.
    ...(l50 ? [] : [cast("Ship's Bell mark", bellT, "SELF", [cond.within(0, 2)])]),
    ...bsT.slice(0, 3).map((id, k) => cast(`Broadside ${"ABC"[k]} mark`, id, "SELF", [cond.roundGt(1)])),
    ...(l50 ? [cast("Ship's Bell mark", bellT, "SELF", [cond.within(0, 2)])] : []),
    cast("Raise the Gunwale", gunwale, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [cond.roundGt(2)]),
    cast("Final Command", finalCmd, "HIGHEST_ENMITY_OPPONENT", [cond.near(4, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Keelbind", keel, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Stolen Form (target buffed)", kitCopies.stolen!, "HIGHEST_ENMITY_OPPONENT", [cond.near(4, "HIGHEST_ENMITY_OPPONENT"), cond.targetHas("HIGHEST_ENMITY_OPPONENT", 25, "increasedamagegiven")]),
    cast("Suppression Writ", kitCopies.writ!, "HIGHEST_ENMITY_OPPONENT", [cond.near(4, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Second Wind (under 40%)", kitCopies.secondwind!, "SELF", [cond.hp(40)]),
    cast("Counter Stance (player adjacent)", kitCopies.counter!, "SELF", [cond.within(0, 1)]),
    cast("Ruin Refrain", kitCopies.refrain!, "CLOSEST_OPPONENT", [cond.near(5)]),
    cast("Unraveling Strike", kitCopies.unraveling!, "CLOSEST_OPPONENT", [cond.near(3)]),
    cast("Explosive Tag Cataclysm", kitCopies.cataclysm!, "CLOSEST_OPPONENT", [cond.near(5)]),
    cast("Windlash Focus", kitCopies.windlash!, "SELF", [cond.within(0, 4)]),
    moveTo("patrol: close in", "CLOSEST_OPPONENT", [cond.far(4)]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];

  /* ---------------- Sealwright ---------------- */
  const sealRules = [
    cast("Ward of Command on the Captain", ward, "HIGHEST_MAX_HEALTH_ALLY"),
    cast("Mending Seal on the Captain", mending, "HIGHEST_MAX_HEALTH_ALLY"),
    cast("Sovereign Fetters", "RPdeeWhFI5AIUUpJXwUlf", "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Dispelling Wave (player buffed)", "JWZYiHKPNwYziWEFjw4Fn", "CLOSEST_OPPONENT", [cond.near(5), cond.targetHas("CLOSEST_OPPONENT", 25, "increasedamagegiven")]),
    cast("Weakening Strike", "YiRdVytsdxFzZtqkEDs5Q", "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    moveTo("keep range: close only when out of reach", "CLOSEST_OPPONENT", [cond.far(6)]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];

  /* ---------------- crew rules ---------------- */
  const focus = (jid: string) =>
    (["HIGHEST_ENMITY_OPPONENT", "CLOSEST_OPPONENT", "LOWEST_HEALTH_OPPONENT"] as const).map((t) =>
      cast(`focus the Chart Mark (${t})`, jid, t, [cond.targetHas(t, 5, "increasepoolcost"), cond.near(5, t)]));
  const wardenRules = [
    cast("Warden's Resolve (opener, once)", wardenOpener, "SELF"),
    cast("Chain Hook (top threat 3+ hexes away)", chainHook, "HIGHEST_ENMITY_OPPONENT", [cond.far(3, "HIGHEST_ENMITY_OPPONENT")]),
    ...focus("UnQKfwq_JoRVu10aTX6Uv"),
    cast("Quick Strike", "FeYnH7BBw_usnc1K-TM-J", "HIGHEST_ENMITY_OPPONENT", [cond.near(3, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Tide Bolt", "UnQKfwq_JoRVu10aTX6Uv", "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Tide Bolt (closest, top threat out of reach)", "UnQKfwq_JoRVu10aTX6Uv", "CLOSEST_OPPONENT", [cond.near(5)]),
    moveTo("move towards the top threat", "HIGHEST_ENMITY_OPPONENT", [cond.far(2, "HIGHEST_ENMITY_OPPONENT")]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  const chargeRules = [
    cast("Core Rupture: a player adjacent", "nCQETf-HNnbRec1OSY2-R", "CLOSEST_OPPONENT", [cond.within(0, 1)]),
    cast("Core Rupture: fuse (from round 3)", "nCQETf-HNnbRec1OSY2-R", "CLOSEST_OPPONENT", [cond.roundGt(2)]),
    moveTo("walk at the closest player", "CLOSEST_OPPONENT", [cond.far(2)]),
    endTurn(),
  ];
  const sentinelRules = [
    cast("Skyglass Aegis on an ally", aegis, "LOWEST_MAX_HEALTH_ALLY"),
    cast("Counter Stance (under 60%)", "T3glZGcSd-jS8G-NB43GR", "SELF", [cond.hp(60)]),
    cast("Rigging Snare", "1jXfTgrtGUaSfqTPSSa83", "CLOSEST_OPPONENT", [cond.near(4)]),
    cast("Twin Kunai", "3v9c1SHlD2GLPF2HW1_Sc", "CLOSEST_OPPONENT", [cond.near(5)]),
    moveTo("move towards", "CLOSEST_OPPONENT", [cond.far(2)]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  const bladeRules = [
    cast("Raijin's Spear on the lowest-health player", "xGVqWSX93hXZgfmlKZODp", "LOWEST_HEALTH_OPPONENT", [cond.near(5, "LOWEST_HEALTH_OPPONENT")]),
    cast("Shuriken Storm on the lowest-health player", "Nrxc8m9utE9qaD_gWpLgf", "LOWEST_HEALTH_OPPONENT", [cond.near(5, "LOWEST_HEALTH_OPPONENT")]),
    // Raijin's Spear and Shuriken Storm both carry pierce (a SHARED_COOLDOWN_TAGS type): one locks the other for 3 rounds.
    cast("Numbing Senbon on the lowest-health player", "m-ur3A8TS8r5jGb84L9x7", "LOWEST_HEALTH_OPPONENT", [cond.near(5, "LOWEST_HEALTH_OPPONENT")]),
    // Stealth blocks the user's own jutsu while it lasts, so it is the vanish when cornered, once.
    cast("Glassveil Step (cornered, once)", vanish, "SELF", [cond.within(0, 1)]),
    cast("Opening Strike on the lowest-threat player", "Cw51Wm_Uy0GiIkiEjlQtn", "LOWEST_ENMITY_OPPONENT", [cond.near(4, "LOWEST_ENMITY_OPPONENT")]),
    cast("Opening Strike (closest, while hunting)", "Cw51Wm_Uy0GiIkiEjlQtn", "CLOSEST_OPPONENT", [cond.near(4)]),
    moveTo("hunt the lowest-health player", "LOWEST_HEALTH_OPPONENT", [cond.far(2, "LOWEST_HEALTH_OPPONENT")]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  const oathRules = [
    cast("Oath of Stillness on the top threat", oath, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    ...focus("YiRdVytsdxFzZtqkEDs5Q"),
    cast("Weakening Strike on the top threat", "YiRdVytsdxFzZtqkEDs5Q", "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Opening Strike", "Cw51Wm_Uy0GiIkiEjlQtn", "CLOSEST_OPPONENT", [cond.near(4)]),
    moveTo("move towards the top threat", "HIGHEST_ENMITY_OPPONENT", [cond.far(2, "HIGHEST_ENMITY_OPPONENT")]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  const wayRules = [
    cast("Chart Mark on the top threat", chartMark, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    // Level 40-60: the crew live about 2 rounds, so the mark also goes on the closest player when the top threat is out of reach.
    ...(l50 ? [cast("Chart Mark on the closest (top threat out of reach)", chartMark, "CLOSEST_OPPONENT", [cond.near(5)])] : []),
    cast("Keelbind at range", wfKeel, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Afterimage Decoy (a player within 2)", decoy, "EMPTY_GROUND_CLOSEST_TO_SELF", [cond.within(0, 2)]),
    ...focus("3v9c1SHlD2GLPF2HW1_Sc"),
    cast("Twin Kunai", "3v9c1SHlD2GLPF2HW1_Sc", "CLOSEST_OPPONENT", [cond.near(5)]),
    moveTo("keep range: close only when out of reach", "CLOSEST_OPPONENT", [cond.far(6)]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];

  const kitOf = (rules: any[], extra: string[] = []) => [...new Set([...rules.map((r) => r.action.jutsuId).filter(Boolean), ...extra])];
  const enemy = (id: string, pools: number, rows: number, all: any[], signature: string[], extraKit: string[] = []) => {
    const rules = trim(id, all);
    const taken = (id === IDS.horror || id === IDS.captain ? P.bossTaken : P.crewTaken) ?? [];
    return {
      id: aid(id),
      o: { base: BASE[id], username: BASE[id], ...(P.level ? { level: P.level } : {}), aiEdit: { poolsMultiplier: pools, ...(P.statsMultiplier ? { statsMultiplier: P.statsMultiplier } : {}) }, effects: [...idgRows(rows), ...taken.map(takenRow)], jutsuIds: kitOf(rules, extraKit), rules, includeDefaultRules: false },
      signature: rules.map((r, i) => (signature.some((s) => r.action.description.startsWith(s)) ? i : -1)).filter((i) => i >= 0),
    };
  };
  const E = [
    enemy(IDS.warden, P.crewPools, P.crewRows, wardenRules, ["Chain Hook"]),
    { id: aid(IDS.charge), o: { base: BASE[IDS.charge], username: BASE[IDS.charge], ...(P.level ? { level: Math.min(P.level, 70) } : {}), ...(P.statsMultiplier ? { aiEdit: { statsMultiplier: P.statsMultiplier } } : {}), jutsuIds: ["nCQETf-HNnbRec1OSY2-R"], rules: chargeRules, includeDefaultRules: false }, signature: [0, 1] },
    enemy(IDS.sentinel, P.crewPools, P.crewRows, sentinelRules, ["Skyglass Aegis"]),
    enemy(IDS.blade, P.crewPools, P.crewRows, bladeRules, ["Raijin's Spear", "Shuriken Storm", "Numbing Senbon"]),
    enemy(IDS.oath, P.crewPools, P.crewRows, oathRules, ["Oath of Stillness"]),
    enemy(IDS.wayfinder, P.crewPools, P.crewRows, wayRules, ["Chart Mark"]),
    enemy(IDS.horror, P.horrorPools, P.horrorRows, horrorRules, ["Maw of the Deep"]),
    enemy(IDS.captain, P.captainPools, P.captainRows, captainRules, ["Broadside"]),
    ...(l50 ? [] : [enemy(IDS.sealwright, P.sealPools, P.sealRows, sealRules, ["Ward of Command"])]),
  ];
  const A = Object.fromEntries(Object.entries(IDS).map(([k, v]) => [k, aid(v)])) as typeof IDS;
  // Level 40-60: two enemies on floors 1-3, the Core Horror alone, the boss floor without the Sealwright.
  const floors = l50 ? [
    { kind: "floor", waves: [{ aiIds: [A.warden, A.charge], delayRounds: 0 }] },
    { kind: "floor", waves: [{ aiIds: [A.sentinel, A.blade], delayRounds: 0 }] },
    { kind: "floor", waves: [{ aiIds: [A.oath, A.wayfinder], delayRounds: 0 }] },
    { kind: "mini-boss", waves: [{ aiIds: [A.horror], delayRounds: 0 }] },
    { kind: "boss", waves: [{ aiIds: [A.warden, A.warden], delayRounds: 0 }, { aiIds: [A.captain], delayRounds: 0 }] },
  ] : [
    { kind: "floor", waves: [{ aiIds: [IDS.warden, IDS.warden, IDS.warden, IDS.charge], delayRounds: 0 }] },
    { kind: "floor", waves: [{ aiIds: [IDS.sentinel, IDS.blade, IDS.warden], delayRounds: 0 }] },
    { kind: "floor", waves: [{ aiIds: [IDS.oath, IDS.wayfinder, IDS.warden], delayRounds: 0 }] },
    { kind: "mini-boss", waves: [{ aiIds: [IDS.horror], delayRounds: 0 }] },
    { kind: "boss", waves: [{ aiIds: [IDS.warden, IDS.warden, IDS.warden], delayRounds: 0 }, { aiIds: [IDS.captain, IDS.sealwright], delayRounds: 0 }] },
  ];
  // Captured jutsu referenced by rules must be in the override jutsu map only if new; captured ids resolve from the catalog.
  return {
    override: {
      name: `kits_${version}`,
      note: l50 ? "Level 40-60 dungeon copies (level 50, lighter kits, two enemies a floor, no Sealwright), built and schema-validated by engine/kits.ts." : "Endgame dungeon copies with the designed kits and priority rules (SKYGLASS_WRECK_ENCOUNTERS.md, SKYGLASS_BOSS_FIGHTS.md 1-2), built and schema-validated by engine/kits.ts.",
      params: P,
      jutsu: J,
      newEnemies: Object.fromEntries(E.map((e) => [e.id, e.o])),
      floors,
      signatures: Object.fromEntries(E.map((e) => [e.id, e.signature])),
    },
  };
};
