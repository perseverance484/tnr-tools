/**
 * Skyglass Wreck dungeon copies on the shared set-piece library (docs/design/SKYGLASS_BOSS_FIGHTS.md 5, 5a, 6).
 *
 * One kit and one ordered rule list per enemy, shared by both Wreck versions (and meant for the hunts' live records):
 * only the AI records differ, and only in stats (level, multipliers, pools, damage rows). Jutsu are either
 * - LIBRARY: the shared marks, blasts, signatures, lowered guard and crew additions (engine/library.ts, all NEW);
 * - WRECK-NEW: Raise the Gunwale, the only new jutsu the Wreck adds outside the library;
 * - LIVE: captured live records used unchanged (the old Crowned Captain kit for the Captain, Unbroken Command and
 *   Battle Trance as Hold the Line and Last Stand, Springguard, Split Image, Sovereign Undertow, the crew's own moves,
 *   and Core Rupture as edited by push/316-317).
 */
import { capturedJutsu, cast, cond, endTurn, highest, jutsu, moveTo, tag } from "./kitlib";
import { ANSWERS, buildLibrary, LIB, MARKER_TYPES, type MarkKey } from "./library";

export type KitParams = {
  /** AI level of every copy (unset = captured level 100); the Seal Charge stays at most 70. */
  level?: number;
  /** AI statsMultiplier for the copies (replayed through scaleEditedAi; captured crew: 5). */
  statsMultiplier?: number;
  crewPools: number; crewRows: number;
  bladePools?: number;
  horrorPools: number; horrorRows: number;
  captainPools: number; captainRows: number;
  sealPools: number; sealRows: number;
  /** Innate +damage-taken % rows (each capped at 100, rows multiply): crew, and the boss wave + Core Horror. */
  crewTaken?: number[];
  bossTaken?: number[];
  /** Core Horror phase 2 (The Core Rebuilds, Rupture Field first) starts below this % health. */
  horrorPhase2?: number;
  gunwaleHP?: number;
};

export const IDS = {
  warden: "dg-deck-warden", charge: "dg-seal-charge", sentinel: "dg-skyglass-sentinel", blade: "dg-first-blade",
  oath: "dg-oathkeeper", wayfinder: "dg-wayfinder", horror: "dg-core-horror", captain: "dg-the-captain", sealwright: "dg-sealwright",
};
export const BASE: Record<string, string> = {
  [IDS.warden]: "Deck Warden", [IDS.charge]: "Seal Charge", [IDS.sentinel]: "Skyglass Sentinel", [IDS.blade]: "First Blade",
  [IDS.oath]: "Oathkeeper", [IDS.wayfinder]: "Wayfinder", [IDS.horror]: "Core Horror", [IDS.captain]: "The Captain", [IDS.sealwright]: "Sealwright",
};

/** Live records used as they are. */
export const LIVE = {
  coreRupture: "nCQETf-HNnbRec1OSY2-R",
  windlash: "_9k7kSYUgMtB-AEFgRly5", springguard: "mOA1hXNf4CcuwOhnnN7ZK", splitImage: "LQ26G2ANWkbTRL7Ry__F0",
  undertow: "nOYLPmN3TXj6wEe_oE6HQ", heavyStrike: "pUrUJX8Jml7fUIBXKsPwv", venomStrike: "LiVOnYq6qHzjB0XkIIA2e",
  twinKunai: "3v9c1SHlD2GLPF2HW1_Sc", tideBolt: "UnQKfwq_JoRVu10aTX6Uv", quickStrike: "FeYnH7BBw_usnc1K-TM-J",
  riggingSnare: "1jXfTgrtGUaSfqTPSSa83", raijin: "xGVqWSX93hXZgfmlKZODp", shuriken: "Nrxc8m9utE9qaD_gWpLgf",
  senbon: "m-ur3A8TS8r5jGb84L9x7", opening: "Cw51Wm_Uy0GiIkiEjlQtn", weakening: "YiRdVytsdxFzZtqkEDs5Q",
  fetters: "RPdeeWhFI5AIUUpJXwUlf", dispel: "JWZYiHKPNwYziWEFjw4Fn", secondWind: "STu1VHNcfgeC3x-UiQDgt",
  battleTrance: "MG9ZujAV8lK7--YxThVbQ",
  // The old Crowned Captain's kit (RUL-2026-10-28-006), unchanged.
  unbrokenCommand: "0Y10JpChssDwFUxNRk6p3", unraveling: "1OhP0StX4VTsosWtCxhsG", writ: "ddbIyVtoxdPQwLRXxSBq8",
  refrain: "EQ93LX8wvuIAd5u75q_i1", cataclysm: "o-4SCAhJ4LHdCwcBDgJrV", keelbind: "PdD44PGaNv4MN5fOALhAF",
  counter: "T3glZGcSd-jS8G-NB43GR", stolen: "VuFuBtE7h5B1nnA2J1lFZ", finalCommand: "X2P22h8ApDmTZHjWpNO87",
};
export const WRECK_NEW = { gunwale: "dg-raise-the-gunwale" };

const idgRow = () => ({
  type: "increasedamagegiven", power: 100, rounds: 99, target: "INHERIT", appearSfx: "", direction: "offence",
  calculation: "percentage", description: "Increased damage given", disappearSfx: "", powerPerLevel: 0,
  appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "",
});
const takenRow = (pct: number) => tag("increasedamagetaken", { power: pct, rounds: 99, calculation: "percentage", description: "Increased damage taken" });

/** The shared rule lists (independent of stats). */
export const sharedRules = (P: Pick<KitParams, "horrorPhase2">) => {
  const PH2 = P.horrorPhase2 ?? 70;
  const mk = (k: MarkKey) => MARKER_TYPES[k];
  const blastOf = (k: MarkKey, prefer?: string) => prefer ?? Object.keys(ANSWERS).find((id) => ANSWERS[id] === k && id.startsWith("lib-blast"))!;
  const blast = (note: string, k: MarkKey, id?: string) => cast(note, blastOf(k, id), "SELF", [cond.marker(1, mk(k))]);
  const mark = (note: string, k: MarkKey, conds: any[] = []) => cast(note, LIB.mark[k], "SELF", conds);
  /** After a mark (60 AP left): the plain attacks, then end the turn, so a boss never lays two marks in one turn. */
  const afterMark = (keys: MarkKey[], plain: [string, string, string, any[]][]) =>
    keys.flatMap((k) => [
      ...plain.map(([note, id, target, conds]) => cast(`after ${LIB.mark[k]}: ${note}`, id, target, [cond.marker(1, mk(k)), ...conds])),
      endTurn(`after ${LIB.mark[k]}: end turn`, [cond.marker(1, mk(k))]),
    ]);
  const focus = (jid: string) =>
    (["HIGHEST_ENMITY_OPPONENT", "CLOSEST_OPPONENT", "LOWEST_HEALTH_OPPONENT"] as const).map((t) =>
      cast(`focus the Chart Mark (${t})`, jid, t, [cond.targetHas(t, 5, "increasepoolcost"), cond.near(5, t)]));

  const horrorPlain: [string, string, string, any[]][] = [
    ["Splintered Grasp (live Heavy Strike)", LIVE.heavyStrike, "CLOSEST_OPPONENT", [cond.near(3)]],
    ["Bilge Spit (live Venom Strike)", LIVE.venomStrike, "CLOSEST_OPPONENT", [cond.near(5)]],
    ["Twin Kunai", LIVE.twinKunai, "CLOSEST_OPPONENT", [cond.near(5)]],
  ];
  const horror = [
    cast(`The Core Rebuilds (live Second Wind, under ${PH2}%)`, LIVE.secondWind, "SELF", [cond.hp(PH2)]),
    blast("Maw of the Deep (signature, Exposed Seam)", "lastLight", LIB.sig.maw),
    blast("Rupture Field A erupts (pools)", "scatterA"),
    blast("Rupture Field B erupts (pools)", "scatterB"),
    blast("Collapse (ring blast)", "ring"),
    // Two-marker chain: the 60 AP left after Omen: Ring drag a far player into the ring (live pull).
    cast("Undertow (live Sovereign Undertow, during a ring mark)", LIVE.undertow, "RANDOM_OPPONENT", [cond.marker(1, mk("ring")), cond.far(4, "RANDOM_OPPONENT")]),
    ...afterMark(["ring", "scatterA", "scatterB", "lastLight"], horrorPlain),
    // Phase 2 (director: earlier, so Rupture Field and its pools appear): Rupture Field A, then the Maw (from round 4;
    // its 6-round cooldown keeps it to about once a phase), then Rupture Field B.
    mark("Omen: Scatter A (phase 2)", "scatterA", [cond.hp(PH2)]),
    mark("Omen: Last Light (Maw of the Deep, from round 4)", "lastLight", [cond.roundGt(3)]),
    mark("Omen: Scatter B (phase 2)", "scatterB", [cond.hp(PH2)]),
    mark("Omen: Ring (Collapse, a player within 2)", "ring", [cond.within(0, 2)]),
    mark("Omen: Scatter A", "scatterA"),
    mark("Omen: Scatter B", "scatterB"),
    ...horrorPlain.map(([n, id, t, c]) => cast(n, id, t, c)),
    endTurn("stationary: hold"),
  ];

  const duel = (t = "HIGHEST_ENMITY_OPPONENT"): [string, string, string, any[]][] => [
    ["Final Command", LIVE.finalCommand, t, [cond.near(4, t)]],
    ["Keelbind", LIVE.keelbind, t, [cond.near(5, t)]],
  ];
  const captain = [
    cast("Hold the Line (live Unbroken Command; the wave opens far away)", LIVE.unbrokenCommand, "SELF", [cond.far(5)]),
    cast("Last Stand at the Helm (live Battle Trance, under 50%)", LIVE.battleTrance, "SELF", [cond.hp(50)]),
    blast("Broadside (signature, rows A)", "rowsA", LIB.sig.broadside),
    blast("Broadside, second volley (shared rows B blast)", "rowsB"),
    blast("Ship's Bell (signature)", "bindingRing", LIB.sig.shipsBell),
    ...afterMark(["rowsA", "rowsB", "bindingRing"], duel()),
    mark("Omen: Binding Ring (Ship's Bell, a player within 2)", "bindingRing", [cond.within(0, 2)]),
    mark("Omen: Rows A (Broadside)", "rowsA", [cond.roundGt(1)]),
    mark("Omen: Rows B (Broadside)", "rowsB", [cond.roundGt(1)]),
    cast("Raise the Gunwale", WRECK_NEW.gunwale, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [cond.roundGt(2)]),
    ...duel().map(([n, id, t, c]) => cast(n, id, t, c)),
    cast("Stolen Form (target buffed)", LIVE.stolen, "HIGHEST_ENMITY_OPPONENT", [cond.near(4, "HIGHEST_ENMITY_OPPONENT"), cond.targetHas("HIGHEST_ENMITY_OPPONENT", 25, "increasedamagegiven")]),
    cast("Suppression Writ", LIVE.writ, "HIGHEST_ENMITY_OPPONENT", [cond.near(4, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Second Wind (under 40%)", LIVE.secondWind, "SELF", [cond.hp(40)]),
    cast("Counter Stance (player adjacent)", LIVE.counter, "SELF", [cond.within(0, 1)]),
    cast("Ruin Refrain", LIVE.refrain, "CLOSEST_OPPONENT", [cond.near(5)]),
    cast("Unraveling Strike", LIVE.unraveling, "CLOSEST_OPPONENT", [cond.near(3)]),
    cast("Explosive Tag Cataclysm", LIVE.cataclysm, "CLOSEST_OPPONENT", [cond.near(5)]),
    cast("Windlash Focus", LIVE.windlash, "SELF", [cond.within(0, 4)]),
    moveTo("patrol: close in", "CLOSEST_OPPONENT", [cond.far(4)]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  const sealwright = [
    cast("Ward of Command on the Captain", LIB.crew.ward, "HIGHEST_MAX_HEALTH_ALLY"),
    cast("Mending Seal on the Captain", LIB.crew.mending, "HIGHEST_MAX_HEALTH_ALLY"),
    cast("Sovereign Fetters", LIVE.fetters, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Dispelling Wave (player buffed)", LIVE.dispel, "CLOSEST_OPPONENT", [cond.near(5), cond.targetHas("CLOSEST_OPPONENT", 25, "increasedamagegiven")]),
    cast("Weakening Strike", LIVE.weakening, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    moveTo("keep range: close only when out of reach", "CLOSEST_OPPONENT", [cond.far(6)]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  // Minor marks (RUL-2026-10-28-024): blast first when primed; mark when a player is within 3 (cooldown 3, so not every
  // turn); while primed the caster holds its hex (the patterns are caster-anchored), attacking but not moving.
  const minor = (k: "splash" | "shortLine") => ({
    blast: cast(`Eruption: ${k === "splash" ? "Splash" : "Short Line"} (primed)`, LIB.blast[k], "SELF", [cond.marker(1, MARKER_TYPES[k])]),
    mark: cast(`Omen: ${k === "splash" ? "Splash" : "Short Line"} (a player within 3)`, LIB.mark[k], "SELF", [cond.within(1, 3)]),
    hold: endTurn("hold position while the minor mark is up", [cond.marker(1, MARKER_TYPES[k])]),
  });
  const mS = minor("splash");
  const mL = minor("shortLine");
  const warden = [
    mS.blast,
    cast("Warden's Resolve (live Windlash Focus, opener)", LIVE.windlash, "SELF"),
    cast("Chain Hook (top threat 3+ hexes away)", LIB.crew.chainHook, "HIGHEST_ENMITY_OPPONENT", [cond.far(3, "HIGHEST_ENMITY_OPPONENT")]),
    mS.mark,
    ...focus(LIVE.tideBolt),
    cast("Quick Strike", LIVE.quickStrike, "HIGHEST_ENMITY_OPPONENT", [cond.near(3, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Tide Bolt", LIVE.tideBolt, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Tide Bolt (closest, top threat out of reach)", LIVE.tideBolt, "CLOSEST_OPPONENT", [cond.near(5)]),
    mS.hold,
    moveTo("move towards the top threat", "HIGHEST_ENMITY_OPPONENT", [cond.far(2, "HIGHEST_ENMITY_OPPONENT")]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  const charge = [
    cast("Core Rupture: a player adjacent", LIVE.coreRupture, "CLOSEST_OPPONENT", [cond.within(0, 1)]),
    cast("Core Rupture: fuse (from round 3)", LIVE.coreRupture, "CLOSEST_OPPONENT", [cond.roundGt(2)]),
    moveTo("walk at the closest player", "CLOSEST_OPPONENT", [cond.far(2)]),
    endTurn(),
  ];
  const sentinel = [
    mL.blast,
    cast("Skyglass Aegis on an ally", LIB.crew.aegis, "LOWEST_MAX_HEALTH_ALLY"),
    mL.mark,
    cast("Counter Stance (under 60%)", LIVE.counter, "SELF", [cond.hp(60)]),
    cast("Rigging Snare", LIVE.riggingSnare, "CLOSEST_OPPONENT", [cond.near(4)]),
    cast("Twin Kunai", LIVE.twinKunai, "CLOSEST_OPPONENT", [cond.near(5)]),
    mL.hold,
    moveTo("move towards", "CLOSEST_OPPONENT", [cond.far(2)]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  const blade = [
    // Defensive opener (director, retune): live Springguard. A live stealth opener was left out: stealth blocks the
    // user's own jutsu while it lasts, and cost the First Blade its signature turns.
    cast("Glassedge Guard (live Springguard, opener)", LIVE.springguard, "SELF"),
    cast("Raijin's Spear on the lowest-health player", LIVE.raijin, "LOWEST_HEALTH_OPPONENT", [cond.near(5, "LOWEST_HEALTH_OPPONENT")]),
    cast("Shuriken Storm on the lowest-health player", LIVE.shuriken, "LOWEST_HEALTH_OPPONENT", [cond.near(5, "LOWEST_HEALTH_OPPONENT")]),
    cast("Numbing Senbon on the lowest-health player", LIVE.senbon, "LOWEST_HEALTH_OPPONENT", [cond.near(5, "LOWEST_HEALTH_OPPONENT")]),
    cast("Opening Strike on the lowest-threat player", LIVE.opening, "LOWEST_ENMITY_OPPONENT", [cond.near(4, "LOWEST_ENMITY_OPPONENT")]),
    cast("Opening Strike (closest, while hunting)", LIVE.opening, "CLOSEST_OPPONENT", [cond.near(4)]),
    moveTo("hunt the lowest-health player", "LOWEST_HEALTH_OPPONENT", [cond.far(2, "LOWEST_HEALTH_OPPONENT")]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
    // Hunts harness (sharedKitFixes): an explicit end of turn, so a turn with nothing usable (e.g. under stealth)
    // never reaches the engine's give-up path.
    endTurn("end turn (never give up)"),
  ];
  const oath = [
    cast("Oath of Stillness on the top threat", LIB.crew.oath, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    ...focus(LIVE.weakening),
    cast("Weakening Strike on the top threat", LIVE.weakening, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Opening Strike", LIVE.opening, "CLOSEST_OPPONENT", [cond.near(4)]),
    moveTo("move towards the top threat", "HIGHEST_ENMITY_OPPONENT", [cond.far(2, "HIGHEST_ENMITY_OPPONENT")]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  const wayfinder = [
    mL.blast,
    cast("Chart Mark on the top threat", LIB.crew.chartMark, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Chart Mark on the closest (top threat out of reach)", LIB.crew.chartMark, "CLOSEST_OPPONENT", [cond.near(5)]),
    mL.mark,
    cast("Keelbind at range", LIVE.keelbind, "HIGHEST_ENMITY_OPPONENT", [cond.near(5, "HIGHEST_ENMITY_OPPONENT")]),
    cast("Afterimage Decoy (live Split Image, a player within 2)", LIVE.splitImage, "EMPTY_GROUND_CLOSEST_TO_SELF", [cond.within(0, 2)]),
    ...focus(LIVE.twinKunai),
    cast("Twin Kunai", LIVE.twinKunai, "CLOSEST_OPPONENT", [cond.near(5)]),
    mL.hold,
    moveTo("keep range: close only when out of reach", "CLOSEST_OPPONENT", [cond.far(6)]),
    highest("highest-power damage", "CLOSEST_OPPONENT"),
  ];
  return {
    [IDS.warden]: { rules: warden, signature: ["Chain Hook"] },
    [IDS.charge]: { rules: charge, signature: ["Core Rupture"] },
    [IDS.sentinel]: { rules: sentinel, signature: ["Skyglass Aegis"] },
    [IDS.blade]: { rules: blade, signature: ["Raijin's Spear", "Shuriken Storm", "Numbing Senbon"] },
    [IDS.oath]: { rules: oath, signature: ["Oath of Stillness"] },
    [IDS.wayfinder]: { rules: wayfinder, signature: ["Chart Mark"] },
    [IDS.horror]: { rules: horror, signature: ["Maw of the Deep", "Omen: Last Light"] },
    [IDS.captain]: { rules: captain, signature: ["Broadside", "Omen: Rows"] },
    [IDS.sealwright]: { rules: sealwright, signature: ["Ward of Command"] },
  } as Record<string, { rules: any[]; signature: string[] }>;
};

export const buildKits = (P: KitParams, version: "endgame" | "lvl50" = "endgame") => {
  const l50 = version === "lvl50";
  const aid = (id: string) => (l50 ? `${id}-l50` : id);
  const J: Record<string, any> = { ...buildLibrary() };
  J[WRECK_NEW.gunwale] = jutsu(WRECK_NEW.gunwale, {
    name: "Raise the Gunwale", description: "A barrier line of timber and seals; it has its own health.", battleDescription: "%user barks an order; the gunwale rises.",
    target: "EMPTY_GROUND", method: "AOE_WALL_SHOOT", range: 3, cooldown: 8, actionCostPerc: 60, donor: "i4lGrYY5HNN2Q2GPToKUS",
    effects: [tag("barrier", { power: 100, rounds: 3, curHealth: P.gunwaleHP ?? 3000, maxHealth: P.gunwaleHP ?? 3000, absorbPercentage: 50, staticAnimation: "cp_gunwale" })],
  });
  const shared = sharedRules(P);
  const liveIds = new Set<string>(Object.values(LIVE));
  for (const { rules } of Object.values(shared))
    for (const r of rules) {
      const id = r.action.jutsuId as string | undefined;
      if (id && liveIds.has(id) && !J[id] && id !== LIVE.coreRupture) {
        try {
          J[id] = capturedJutsu(id).record; // live record, unchanged (catalog ids resolve from the baseline anyway)
        } catch {
          /* resolved from data/baseline.json's catalog */
        }
      }
    }
  const kitOf = (rules: any[]) => [...new Set(rules.map((r) => r.action.jutsuId).filter(Boolean))] as string[];
  const enemy = (id: string, pools: number | null, rows: number) => {
    const { rules, signature } = shared[id]!;
    const boss = id === IDS.horror || id === IDS.captain || id === IDS.sealwright;
    const taken = (boss ? P.bossTaken : P.crewTaken) ?? [];
    const charge = id === IDS.charge;
    return {
      id: aid(id),
      o: {
        base: BASE[id], username: BASE[id],
        ...(P.level ? { level: charge ? Math.min(P.level, 70) : P.level } : {}),
        aiEdit: { ...(pools !== null ? { poolsMultiplier: pools } : {}), ...(P.statsMultiplier ? { statsMultiplier: P.statsMultiplier } : {}) },
        ...(charge ? {} : { effects: [...Array.from({ length: rows }, idgRow), ...taken.map(takenRow)] }),
        jutsuIds: kitOf(rules), rules, includeDefaultRules: false,
      },
      signature: rules.map((r, i) => (signature.some((s) => r.action.description.startsWith(s)) ? i : -1)).filter((i) => i >= 0),
    };
  };
  const E = [
    enemy(IDS.warden, P.crewPools, P.crewRows),
    enemy(IDS.charge, null, 0),
    enemy(IDS.sentinel, P.crewPools, P.crewRows),
    enemy(IDS.blade, P.bladePools ?? P.crewPools, P.crewRows),
    enemy(IDS.oath, P.crewPools, P.crewRows),
    enemy(IDS.wayfinder, P.crewPools, P.crewRows),
    enemy(IDS.horror, P.horrorPools, P.horrorRows),
    enemy(IDS.captain, P.captainPools, P.captainRows),
    ...(l50 ? [] : [enemy(IDS.sealwright, P.sealPools, P.sealRows)]),
  ];
  const A = Object.fromEntries(Object.entries(IDS).map(([k, v]) => [k, aid(v)])) as typeof IDS;
  const floors = l50
    ? [
        { kind: "floor", waves: [{ aiIds: [A.warden, A.charge], delayRounds: 0 }] },
        { kind: "floor", waves: [{ aiIds: [A.sentinel, A.blade], delayRounds: 0 }] },
        { kind: "floor", waves: [{ aiIds: [A.oath, A.wayfinder], delayRounds: 0 }] },
        { kind: "mini-boss", waves: [{ aiIds: [A.horror], delayRounds: 0 }] },
        { kind: "boss", waves: [{ aiIds: [A.warden, A.warden], delayRounds: 0 }, { aiIds: [A.captain], delayRounds: 0 }] },
      ]
    : [
        { kind: "floor", waves: [{ aiIds: [A.warden, A.warden, A.warden, A.charge], delayRounds: 0 }] },
        { kind: "floor", waves: [{ aiIds: [A.sentinel, A.blade, A.warden], delayRounds: 0 }] },
        { kind: "floor", waves: [{ aiIds: [A.oath, A.wayfinder, A.warden], delayRounds: 0 }] },
        { kind: "mini-boss", waves: [{ aiIds: [A.horror], delayRounds: 0 }] },
        { kind: "boss", waves: [{ aiIds: [A.warden, A.warden, A.warden], delayRounds: 0 }, { aiIds: [A.captain, A.sealwright], delayRounds: 0 }] },
      ];
  return {
    override: {
      name: `kits_${version}`,
      note: `Skyglass Wreck ${version}: the shared kits and rules on the set-piece library (SKYGLASS_BOSS_FIGHTS.md 5-6); only AI stats differ between versions. Built by engine/kits.ts.`,
      params: P,
      jutsu: J,
      newEnemies: Object.fromEntries(E.map((e) => [e.id, e.o])),
      floors,
      signatures: Object.fromEntries(E.map((e) => [e.id, e.signature])),
    },
    shared,
  };
};
