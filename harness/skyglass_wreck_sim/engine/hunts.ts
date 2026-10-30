/**
 * Skyglass treasure hunts (solo): enemy records, kits and rules, and the four hunts' fight sequences.
 *
 * Sources (main): docs/design/SKYGLASS_BOSS_FIGHTS.md sections 4 (hunt bosses), 5/5a (sharing, the set-piece library),
 * 6 (engine recipe); SKYGLASS_WRECK_ENCOUNTERS.md (crew rules); push/skyglass_hunts.gen.py and
 * state/skyglass_hunts/hunts.py (fight sequences, TERM and ALARM debuffs); push/262 (Foundry Warden record).
 *
 * - Crew enemies use the shared endgame kit and rules exactly as engine/kits.ts builds them (read, not modified);
 *   only AI stats (pools, +100% damage rows) are tuned for solo.
 * - Hunt bosses add set pieces from the shared set-piece library (5a; engine/library.ts, library_spec.json, owned by
 *   the Wreck agent; read, not modified), used by id. The only record beyond the library is the Called to the Archive
 *   summon (budgeted in 5a, not built there yet). The six crew additions in the shared kits are remapped from their
 *   dg-* ids to the identical library records.
 * - Every jutsu passes the live JutsuValidator (kitlib.jutsu) and every rule the live AiRule (kitlib.rule).
 */
import { anim, capturedJutsu, cast, cond, endTurn, jutsu, moveTo, tag } from "./kitlib";
import { buildKits, IDS, type KitParams } from "./kits";

/**
 * Merge note (fable/skyglass-charts-sim, ad379117): the Wreck owner consolidated kits.ts on the library; buildEndgame and
 * DEFAULT_PARAMS are gone. The hunts take only the shared kits and rule lists from buildKits (rules depend only on
 * horrorPhase2); the stats below are placeholders that the hunts never read (their stats come from HuntParams).
 */
export const DEFAULT_PARAMS: KitParams = { crewPools: 1, crewRows: 0, horrorPools: 1, horrorRows: 0, captainPools: 1, captainRows: 0, sealPools: 1, sealRows: 0 };
export const buildEndgame = (P: Partial<KitParams>, version: "endgame" | "lvl50" = "endgame") => buildKits({ ...DEFAULT_PARAMS, ...P } as KitParams, version);
import { readFileSync } from "node:fs";
import { JutsuValidator } from "@/validators/combat";
import { join } from "node:path";
import { getUserCaps } from "@/drizzle/constants";
import { calcLevel, calcLevelRequirements } from "@/libs/profile";
import { scaleEditedAi } from "@/server/api/routers/profile";
import { buildLibrary, LIB, MARKER_TYPES, type MarkKey } from "./library";

/* ------------------------------------------------------------------ */
/* Live AI ids (push/skyglass_hunts.gen.py AI map)                     */
/* ------------------------------------------------------------------ */
export const LIVE = {
  horror: "AQi-bHJ-5tHXtxrnc0P9E", sentinel: "3V_gdHYaclMB1gTyOPAbV", charge: "wTgO-Q32caSSd0is1QIS7",
  sealwright: "RBW5KsIXmTGR710D2y2Y7", wayfinder: "v7T9_XdGMfP46em0dPuBc", blade: "d6g0mOM7RBSsYI1hrUVT9",
  captain: "QY69h271Nx9uHrBeR6jwW", warden: "texZaFi42S3EvJZBwQ8cd", canister: "frc9LTxqQlM7mncG4VZGK",
  keeper: "2OXJEXoktxJcjqMkE851g", foundry: "81lnIP-q97gItQYWl5vWD",
  // Crownhold AIs (state/crownhold/ids.json; push/272 creates, push/276 renames), RUL-2026-10-28-013:
  archivist: "LZiunyinw9ScK3mh9HiR2", // D3.REG1 Skyglass Archive Keeper -> Crown Archivist: the Archive alarm guard
  stonebound: "jqxu13kNHhfNY-NF68Ftb", // D3.REG4 Failed Reconstruction Prototype -> Crown Stonebound: the Sealwright's summon
} as const;
export const NAME: Record<string, string> = {
  [LIVE.horror]: "Core Horror", [LIVE.sentinel]: "Skyglass Sentinel", [LIVE.charge]: "Seal Charge", [LIVE.sealwright]: "Sealwright",
  [LIVE.wayfinder]: "Wayfinder", [LIVE.blade]: "First Blade", [LIVE.captain]: "The Captain", [LIVE.warden]: "Deck Warden",
  [LIVE.canister]: "Core Canister", [LIVE.keeper]: "Arsenal Keeper", [LIVE.foundry]: "Foundry Warden",
  [LIVE.archivist]: "Crown Archivist", [LIVE.stonebound]: "Crown Stonebound",
};
/** Crownhold records: manifest slot (push/272 srcId) for the hunt-used ones. */
export const CROWN_SLOT: Record<string, string> = { [LIVE.archivist]: "crownhold_d3.reg1", [LIVE.stonebound]: "crownhold_d3.reg4" };
/** Endgame dungeon copy whose kit and rules each live crew record takes (shared kit). */
const SHARED_FROM: Record<string, string> = {
  [LIVE.warden]: IDS.warden, [LIVE.charge]: IDS.charge, [LIVE.sentinel]: IDS.sentinel, [LIVE.blade]: IDS.blade,
  [LIVE.wayfinder]: IDS.wayfinder, [LIVE.horror]: IDS.horror, [LIVE.captain]: IDS.captain, [LIVE.sealwright]: IDS.sealwright,
};

/* ------------------------------------------------------------------ */
/* Quest debuffs (push/skyglass_hunts.gen.py ALARM / TERM, verbatim)    */
/* ------------------------------------------------------------------ */
const qfx = (t: string, power: number, rounds: number, desc: string, calc = "static") => ({
  type: t, power, rounds, target: "INHERIT", direction: "offence", calculation: calc, powerPerLevel: 0, description: desc,
  appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "",
});
export const ALARM = [qfx("increasedamagetaken", 20, 3, "The archive's alarm: you take 20% more damage for 3 rounds", "percentage")];
export const TERM: Record<number, any[]> = {
  1: [qfx("elementalseal", 100, 99, "The Oathkeeper's term: your elemental jutsu are sealed")],
  2: [qfx("disarm", 100, 99, "The Oathkeeper's term: you fight unarmed")],
  3: [qfx("healprevent", 100, 99, "The Oathkeeper's term: no healing at the Captain's helm")],
};

/* ------------------------------------------------------------------ */
/* Params                                                               */
/* ------------------------------------------------------------------ */
/** givenDown: one innate decreasedamagegiven % row (solo softening below the +100% rows, e.g. the Watch Captain). */
export type Stat = { pools: number; rows: number; stats?: number; givenDown?: number };
export type HuntParams = {
  /** Solo stats per live record (poolsMultiplier, number of +100% damage rows, optional statsMultiplier). */
  stats: Record<string, Stat>;
  /** Called to the Archive: summon HP and power % of the Crown Stonebound record (RUL-2026-10-28-013). */
  echoHp: number; echoPower: number;
  /** REFERENCE RUNS ONLY (not a design): shared-rule notes to drop, per live id, to measure what a kit decision would change. */
  refDropRules?: Record<string, string[]>;
  /** Composition overrides (live ids) for a fight label prefix, e.g. {"alarm": [sentinel]}; default: the generator's. */
  compose?: Record<string, string[]>;
};
/** The tuned solo values (same as overrides/hunts.params.json). */
export const DEFAULT_HUNT_PARAMS: HuntParams = {
  stats: {
    [LIVE.warden]: { pools: 1, rows: 0 }, [LIVE.charge]: { pools: 1, rows: 0, stats: 1 }, [LIVE.canister]: { pools: 1, rows: 0, stats: 5 },
    [LIVE.keeper]: { pools: 1, rows: 0 }, [LIVE.sentinel]: { pools: 3, rows: 3 }, [LIVE.horror]: { pools: 2, rows: 2 },
    [LIVE.sealwright]: { pools: 2.5, rows: 2 }, [LIVE.wayfinder]: { pools: 1.26, rows: 1 }, [LIVE.blade]: { pools: 1.5, rows: 2 },
    [LIVE.captain]: { pools: 2, rows: 4 }, [LIVE.foundry]: { pools: 2.5, rows: 1 },
    [LIVE.archivist]: { pools: 2, rows: 2 },
  },
  echoHp: 15000, echoPower: 60,
};

/* ------------------------------------------------------------------ */
/* Hunt kits                                                             */
/* ------------------------------------------------------------------ */
const idgRows = (n: number) => Array.from({ length: n }, () => ({
  type: "increasedamagegiven", power: 100, rounds: 99, target: "INHERIT", appearSfx: "", direction: "offence",
  calculation: "percentage", description: "Increased damage given", disappearSfx: "", powerPerLevel: 0,
  appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "",
}));
const LIVE_J = {
  quickStrike: "FeYnH7BBw_usnc1K-TM-J", heavyStrike: "pUrUJX8Jml7fUIBXKsPwv", snare: "1jXfTgrtGUaSfqTPSSa83",
  stoneward: "V3WrfQ3pB-eCq2hojsxWe", springguard: "mOA1hXNf4CcuwOhnnN7ZK", windlash: "_9k7kSYUgMtB-AEFgRly5",
  fortress: "i4lGrYY5HNN2Q2GPToKUS", coreRupture: "nCQETf-HNnbRec1OSY2-R", hellHound: "kP_KMs7H9wQJwRHeaTGCZ",
  twinKunai: "3v9c1SHlD2GLPF2HW1_Sc",
};
/** dg-* crew additions in the shared kits -> the identical library records. */
export const CREW_TO_LIB: Record<string, string> = {
  "dg-chain-hook": LIB.crew.chainHook, "dg-oath-of-stillness": LIB.crew.oath, "dg-chart-mark": LIB.crew.chartMark,
  "dg-skyglass-aegis": LIB.crew.aegis, "dg-mending-seal": LIB.crew.mending, "dg-ward-of-command": LIB.crew.ward,
};
/** Primed condition for a library mark (usage rule: has_effect <marker type> >= 1). */
const primed = (k: MarkKey) => cond.marker(1, MARKER_TYPES[k]);
/**
 * One library set piece as rules (coordinator usage rules): the blast on the marker goes on top (collected by the
 * caller); after the mark, `has_effect <marker>` -> plain attack -> end turn, ahead of other marks, so a boss never
 * lays two marks in one turn.
 */
const afterMark = (k: MarkKey, label: string, plain: { id: string; target: string; range: number }[], extra: any[] = []) => [
  ...extra,
  ...plain.map((p) => cast(`${label}: plain attack after the mark`, p.id, p.target, [primed(k), cond.near(p.range, p.target)])),
  endTurn(`${label}: end turn after the mark`, [primed(k)]),
];

export const buildHunts = (HP: HuntParams, kitParams: KitParams) => {
  const shared = buildEndgame(kitParams, "endgame").override as any;
  const lib = buildLibrary();
  const remap = (rules: any[]) => rules.map((r) => (r.action.jutsuId && CREW_TO_LIB[r.action.jutsuId] ? { ...r, action: { ...r.action, jutsuId: CREW_TO_LIB[r.action.jutsuId] } } : r));
  const J: Record<string, any> = { ...shared.jutsu, ...lib };
  // LIBRARY FIX (for the library owner to adopt): Ward of Command's decreasedamagetaken row inherits target SELF from
  // its shape donor (Folding Screen Guard), so the ward always lands on the caster, never on the ally the rule picks.
  // RUL-2026-10-28-013 wants it on the Stonebound, so the hunts use the same record with that row's target INHERIT.
  const ward = structuredClone(J[LIB.crew.ward]);
  ward.effects = ward.effects.map((e: any) => (e.type === "decreasedamagetaken" ? { ...e, target: "INHERIT" } : e));
  const wardOk = JutsuValidator.safeParse(ward);
  if (!wardOk.success) throw new Error(`ward fix: ${wardOk.error.message}`);
  J[LIB.crew.ward] = ward;
  const sharedRules = (liveId: string) => remap(structuredClone(shared.newEnemies[SHARED_FROM[liveId]!].rules) as any[]);
  // The one record beyond the library: the Sealwright's summon (5a budget: "Summons (Recall, Called to the Archive)").
  const echo = jutsu("hunt-called-to-the-archive", {
    name: "Called to the Archive", description: "The Stonebound, the one they kept, steps out of a frame (one at a time).",
    battleDescription: "%user touches an empty frame. The Stonebound steps out of it.", target: "EMPTY_GROUND", method: "SINGLE",
    range: 4, cooldown: 4, actionCostPerc: 40, donor: LIVE_J.hellHound,
    effects: [tag("summon", { aiId: LIVE.stonebound, aiHp: HP.echoHp, power: HP.echoPower, rounds: 3, calculation: "percentage", appearAnimation: anim("cc_recall") })],
  });
  J[echo.id] = echo;
  // Live records referenced by hunt rules that are not in the baseline catalog (used as they are).
  J[LIVE_J.fortress] = capturedJutsu(LIVE_J.fortress).record;

  const R: Record<string, { rules: any[]; signature: string[]; note: string }> = {};
  // Foundry Warden (4a): Pour Line = Omen: Lines + Eruption: Lines; Quench = Omen: Last Light + Quench (Cooling Shell
  // rides on it); Mould Cage = Chain Hook (library crew addition) drags the player beside him, by his Core Canister.
  // Overpour: under 50% Pour Line jumps ahead of Quench (no second channel pattern exists in the library).
  const fwPlain = [{ id: LIVE_J.heavyStrike, target: "CLOSEST_OPPONENT", range: 3 }, { id: LIVE_J.quickStrike, target: "CLOSEST_OPPONENT", range: 3 }, { id: LIB.crew.chainHook, target: "CLOSEST_OPPONENT", range: 5 }];
  R[LIVE.foundry] = {
    note: "Hunt boss (4a). Live kit (push/262: Quick Strike, Heavy Strike, Rigging Snare, Stoneward, Springguard, Windlash Focus) as plain moves, plus library set pieces and Chain Hook as Mould Cage; rules rewritten to the fight design.",
    signature: ["Quench", "Pour Line"],
    rules: [
      cast("Quench (Cooling Shell window)", LIB.sig.quench, "SELF", [primed("lastLight")]),
      cast("Pour Line: the channels run", LIB.blast.lines, "SELF", [primed("lines")]),
      // No Chain Hook in the Quench mark's turn: a root there makes the stars unreachable (a guaranteed hit).
      ...afterMark("lastLight", "Quench", fwPlain.slice(0, 2)),
      ...afterMark("lines", "Pour Line", fwPlain),
      cast("Windlash Focus (opener, once)", LIVE_J.windlash, "SELF", [{ type: "round_lower_than", value: 2, description: "" }]),
      cast("Overpour: Pour Line mark (under 50%)", LIB.mark.lines, "SELF", [cond.hp(50)]),
      cast("Quench mark (from round 3)", LIB.mark.lastLight, "SELF", [cond.roundGt(2)]),
      cast("Pour Line mark", LIB.mark.lines, "SELF", [cond.roundGt(1)]),
      moveTo("stay by the crucible (his Canister)", "LOWEST_MAX_HEALTH_ALLY", [cond.far(2, "LOWEST_MAX_HEALTH_ALLY")]),
      cast("Mould Cage (Chain Hook: drag beside the Canister)", LIB.crew.chainHook, "CLOSEST_OPPONENT", [cond.far(2)]),
      cast("Heavy Strike", LIVE_J.heavyStrike, "CLOSEST_OPPONENT", [cond.near(3)]),
      cast("Quick Strike", LIVE_J.quickStrike, "CLOSEST_OPPONENT", [cond.near(3)]),
      cast("Rigging Snare", LIVE_J.snare, "CLOSEST_OPPONENT", [cond.near(4)]),
      cast("Stoneward (player within 2)", LIVE_J.stoneward, "SELF", [cond.within(0, 2)]),
      cast("Springguard (player within 5)", LIVE_J.springguard, "SELF", [cond.within(0, 5)]),
      endTurn("stationary: hold the crucible"),
    ],
  };
  // Sealwright (4b): Script Lines = Omen: Seal Lines + Binding: Seal Lines; Archive Lock = Omen: Last Light, Binding +
  // Command Absolute (the library has no shared violet field blast; its line is the Crowned Captain's "Kneel.");
  // Called to the Archive (summon); Mending Seal (shared rule); He Lowers His Seals = Lowered Guard under 30% (once, cd 99).
  const swPlain = [{ id: "YiRdVytsdxFzZtqkEDs5Q", target: "CLOSEST_OPPONENT", range: 5 }];
  R[LIVE.sealwright] = {
    note: "Hunt boss (4b): set pieces above the shared Sealwright rules (kept intact).",
    signature: ["Archive Lock", "Script Lines"],
    rules: [
      cast("Archive Lock closes (Command Absolute)", LIB.sig.commandAbsolute, "SELF", [primed("lastLightBinding")]),
      cast("Script Lines close", LIB.blast.sealLines, "SELF", [primed("sealLines")]),
      ...afterMark("lastLightBinding", "Archive Lock", swPlain),
      ...afterMark("sealLines", "Script Lines", swPlain),
      cast("He Lowers His Seals (under 30%, once)", LIB.loweredGuard, "SELF", [cond.hp(30)]),
      cast("Called to the Archive (one Stonebound at a time)", echo.id, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [cond.roundGt(1), cond.noSummon()]),
      cast("Archive Lock mark (from round 3)", LIB.mark.lastLightBinding, "SELF", [cond.roundGt(2)]),
      cast("Script Lines mark", LIB.mark.sealLines, "SELF", [cond.roundGt(1)]),
      ...sharedRules(LIVE.sealwright),
    ],
  };
  // Skyglass Sentinel (4c): Tide Line = Omen: Rows + Eruption: Rows (the library rows blast has no push); Low Tide =
  // Lowered Guard in the mark's turn (the 100 AP blast leaves no AP for it, and Lowered Guard is once per fight);
  // Shell Wall = live Adamantine Fortress; Counter Stance is in the shared rules.
  const stPlain = [{ id: LIVE_J.twinKunai, target: "CLOSEST_OPPONENT", range: 5 }];
  R[LIVE.sentinel] = {
    note: "Hunt boss (4c) and Archive alarm guard: Tide Line above the shared Sentinel rules.",
    signature: ["Tide Line"],
    rules: [
      cast("Tide Line B: the surf hammers in", LIB.blast.rowsB, "SELF", [primed("rowsB")]),
      cast("Tide Line A: the surf hammers in", LIB.blast.rowsA, "SELF", [primed("rowsA")]),
      ...afterMark("rowsB", "Tide Line B", stPlain, [cast("Low Tide (the sand runs out, once)", LIB.loweredGuard, "SELF", [primed("rowsB")])]),
      ...afterMark("rowsA", "Tide Line A", stPlain, [cast("Low Tide (the sand runs out, once)", LIB.loweredGuard, "SELF", [primed("rowsA")])]),
      cast("Tide Line B mark (under 50%)", LIB.mark.rowsB, "SELF", [cond.hp(50)]),
      cast("Tide Line A mark", LIB.mark.rowsA, "SELF", [cond.roundGt(1)]),
      ...sharedRules(LIVE.sentinel).flatMap((r: any) => (r.action.description.startsWith("Skyglass Aegis") ? [r, cast("Shell Wall (live Adamantine Fortress)", LIVE_J.fortress, "EMPTY_GROUND_CLOSEST_TO_OPPONENT", [cond.within(0, 2)])] : [r])),
    ],
  };
  // Wayfinder (4d): the old coastline = Omen: Scatter + Eruption: Scatter (2-round pools). Chart Mark stays his opener.
  const wfPlain = [{ id: LIVE_J.twinKunai, target: "CLOSEST_OPPONENT", range: 5 }];
  const wfShared = sharedRules(LIVE.wayfinder);
  R[LIVE.wayfinder] = {
    note: "Watch duel (4d): coastline set piece above the shared Wayfinder rules (Chart Mark first).",
    signature: ["Coastline", "Chart Mark"],
    rules: [
      cast("Coastline B erupts", LIB.blast.scatterB, "SELF", [primed("scatterB")]),
      cast("Coastline A erupts", LIB.blast.scatterA, "SELF", [primed("scatterA")]),
      ...afterMark("scatterB", "Coastline B", wfPlain, [wfShared[0]]),
      ...afterMark("scatterA", "Coastline A", wfPlain, [wfShared[0]]),
      wfShared[0],
      cast("Coastline B mark (under 50%)", LIB.mark.scatterB, "SELF", [cond.hp(50)]),
      cast("Coastline A mark", LIB.mark.scatterA, "SELF", [cond.roundGt(1)]),
      ...wfShared.slice(1),
    ],
  };
  // First Blade (4d): ring = Omen: Ring + Eruption: Ring; "That was new." = Lowered Guard under 25% (once).
  const fbPlain = [{ id: "xGVqWSX93hXZgfmlKZODp", target: "LOWEST_HEALTH_OPPONENT", range: 5 }, { id: "m-ur3A8TS8r5jGb84L9x7", target: "LOWEST_HEALTH_OPPONENT", range: 5 }];
  R[LIVE.blade] = {
    note: "Watch duel (4d): ring set piece and window above the shared First Blade rules.",
    signature: ["Ring cut"],
    rules: [
      cast("Ring cut", LIB.blast.ring, "SELF", [primed("ring")]),
      ...afterMark("ring", "Ring", fbPlain),
      cast("That was new (under 25%, once)", LIB.loweredGuard, "SELF", [cond.hp(25)]),
      cast("Ring mark (a player within 2)", LIB.mark.ring, "SELF", [cond.within(0, 2)]),
      ...sharedRules(LIVE.blade),
      // Added (no shared rule removed): while Glassveil Step's stealth lasts he can use no jutsu or attack, and with no
      // matching rule the engine's give-up path sets his HP to 0 (ai_v2.ts "exhausted and has to give up").
      endTurn("hold while veiled (no valid action)"),
    ],
  };
  // The Captain (4d): exactly the shared dungeon kit (section 1); no Sealwright, so no Ward of Command.
  R[LIVE.captain] = { note: "Watch duel (4d): the shared Captain kit as is (engine/kits.ts; no Sealwright, so no Ward).", signature: ["Broadside"], rules: sharedRules(LIVE.captain) };
  R[LIVE.warden] = { note: "Crew: shared Deck Warden kit.", signature: ["Chain Hook"], rules: sharedRules(LIVE.warden) };
  R[LIVE.charge] = { note: "Crew hazard: shared Seal Charge kit (Core Rupture v2, live).", signature: ["Core Rupture"], rules: sharedRules(LIVE.charge) };
  R[LIVE.horror] = { note: "Archive descent: shared Core Horror kit (engine/kits.ts).", signature: ["Maw of the Deep"], rules: sharedRules(LIVE.horror) };
  // Not in the endgame dungeon, so no shared kit exists:
  R[LIVE.canister] = {
    note: "Crew hazard, not in the endgame dungeon: rules from SKYGLASS_WRECK_ENCOUNTERS.md (Core Canister row); fuse round 7 kept from the live rule.",
    signature: ["Core Rupture"],
    rules: [
      cast("Core Rupture: a player within 2", LIVE_J.coreRupture, "CLOSEST_OPPONENT", [cond.within(0, 2)]),
      cast("Core Rupture: fuse (from round 7, live)", LIVE_J.coreRupture, "CLOSEST_OPPONENT", [cond.roundGt(6)]),
      endTurn("stationary"),
    ],
  };

  const kitOf = (rules: any[], extra: string[] = []) => [...new Set([...rules.map((r) => r.action.jutsuId).filter((id: string) => id && id !== "basicAttack"), ...extra])];
  const enemies: Record<string, any> = {};
  const newEnemies: Record<string, any> = {};
  const signatures: Record<string, number[]> = {};
  const notes: Record<string, string> = {};
  for (const [id, r] of Object.entries(R)) {
    const drop = HP.refDropRules?.[id] ?? [];
    if (drop.length) r.rules = r.rules.filter((x: any) => !drop.some((d) => x.action.description.startsWith(d)));
    const s = HP.stats[id]!;
    const o = {
      aiEdit: { poolsMultiplier: s.pools, ...(s.stats ? { statsMultiplier: s.stats } : {}) },
      effects: [...idgRows(s.rows), ...(s.givenDown ? [tag("decreasedamagegiven", { power: s.givenDown, rounds: 99, calculation: "percentage", description: "Decreased damage given" })] : [])],
      jutsuIds: kitOf(r.rules, id === LIVE.foundry ? [LIVE_J.quickStrike, LIVE_J.heavyStrike, LIVE_J.snare, LIVE_J.stoneward, LIVE_J.springguard, LIVE_J.windlash] : []),
      rules: r.rules, includeDefaultRules: false,
    };
    if (id === LIVE.foundry) newEnemies[id] = { base: "Arsenal Keeper", username: "Foundry Warden", ...o };
    else if (id === LIVE.charge || id === LIVE.canister) enemies[id] = { ...o, aiEdit: s.stats ? { statsMultiplier: s.stats } : undefined }; // hazards: pools as live
    else enemies[id] = o;
    signatures[id] = r.rules.map((x: any, i: number) => (r.signature.some((sg) => x.action.description.startsWith(sg)) && x.action.jutsuId && !x.action.description.includes("plain attack") ? i : -1)).filter((i: number) => i >= 0);
    notes[id] = r.note;
  }
  // Arsenal Keeper: no shared endgame kit exists; live kit and live rules, stats only.
  const k = HP.stats[LIVE.keeper]!;
  enemies[LIVE.keeper] = { aiEdit: { poolsMultiplier: k.pools, ...(k.stats ? { statsMultiplier: k.stats } : {}) }, effects: idgRows(k.rows) };
  notes[LIVE.keeper] = "Crew, not in the endgame dungeon: no shared kit exists, so the live kit and live rules are kept; stats only.";
  return { override: { name: "hunts", jutsu: J, enemies, newEnemies, signatures }, rules: R, notes, echoId: echo.id, liveJ: LIVE_J };
};

export type Path = { hunt: string; fights: { ids: string[]; debuffs?: any[]; label: string; boss?: boolean }[] };
export const buildPaths = (compose: Record<string, string[]> = {}): Record<string, Path> => {
  const P: any = {};
  const f = (label: string, ids: string[], debuffs?: any[], boss = false) => ({ label, ids, debuffs, boss });
  P.foundry = { hunt: "Drowned Foundry", fights: [f("intake: Deck Warden + Core Canister", [LIVE.warden, LIVE.canister]), f("pour hall: Arsenal Keeper + Seal Charge x2", [LIVE.keeper, LIVE.charge, LIVE.charge]), f("crucible: Foundry Warden + Core Canister", [LIVE.foundry, LIVE.canister], undefined, true)] };
  // RUL-2026-10-28-013: the alarm guard is the Crown Archivist (its own record), still with the Seal Charge.
  const alarmIds = compose.alarm ?? [LIVE.archivist, LIVE.charge];
  const alarm = (n: number) => f(`alarm ${n}: ${alarmIds.map((i) => NAME[i]).join(" + ")} (alarm debuff)`, alarmIds, ALARM);
  const descent = f("descent: Core Horror", [LIVE.horror]);
  const keeper = f("archive: Sealwright", [LIVE.sealwright], undefined, true);
  P.archive_clean = { hunt: "Quarantined Archive", fights: [descent, keeper] };
  P.archive_alarm1 = { hunt: "Quarantined Archive", fights: [descent, alarm(1), keeper] };
  P.archive_alarm3 = { hunt: "Quarantined Archive", fights: [descent, alarm(1), alarm(2), alarm(3), keeper] };
  for (let m = 0; m < 8; m++) {
    const t = [1, 2, 3].map((n) => !!(m & (1 << (n - 1))));
    P[`watch_${t.map((x) => (x ? "1" : "0")).join("")}`] = {
      hunt: "Captain's Watch",
      fights: [
        f(`chart room: Wayfinder${t[0] ? " (term: elementalseal)" : ""}`, [LIVE.wayfinder], t[0] ? TERM[1] : undefined),
        f(`deck: First Blade${t[1] ? " (term: disarm)" : ""}`, [LIVE.blade], t[1] ? TERM[2] : undefined),
        f(`helm: The Captain${t[2] ? " (term: healprevent)" : ""}`, [LIVE.captain], t[2] ? TERM[3] : undefined, true),
      ],
    };
  }
  // Press-on probes (RUL-2026-10-29-057 item 6 asks whether the Archive and Watch keep press-on rooms): one extra room after
  // the boss, HP carried, built only from records these hunts already field. Not part of the hunts' design.
  P.archive_clean_press = { hunt: "Quarantined Archive", fights: [descent, keeper, f(`PRESS ON (probe): ${alarmIds.map((i) => NAME[i]).join(" + ")}`, alarmIds)] };
  P.watch_000_press = { hunt: "Captain's Watch", fights: [...P.watch_000.fights, f("PRESS ON (probe): Wayfinder + Deck Warden", [LIVE.wayfinder, LIVE.warden])] };
  P.cache_right = { hunt: "Buried Cache", fights: [f("dig: Skyglass Sentinel", [LIVE.sentinel], undefined, true)] };
  P.cache_wrong = { hunt: "Buried Cache", fights: [f("wrong cove: Deck Warden + Seal Charge", [LIVE.warden, LIVE.charge]), f("dig: Skyglass Sentinel", [LIVE.sentinel], undefined, true)] };
  return P;
};
export const PATHS = buildPaths();

export { DEFAULT_PARAMS as KIT_DEFAULTS };

/* ------------------------------------------------------------------ */
/* Crownhold records used by the hunts (RUL-2026-10-28-013)             */
/* ------------------------------------------------------------------ */
/**
 * Live jutsu edits the hunts model (director, 2026-10-28). Erupting Ground (`jBRyl7F4UjTyxG5nnzLqj`, the Crown
 * Stonebound's AOE) has no friendlyFire on its damage row, so it hit the Sealwright beside it: the row becomes
 * enemies-only. A live edit: law 18 (unequip from every holder, edit, re-equip); the holders are listed in the spec.
 */
export const LIVE_JUTSU_FIXES: Record<string, { note: string; apply: (rec: any) => any }> = {
  // Superseded by RUL-2026-10-28-026 item 2: the shared live Erupting Ground (89 holders) is NOT edited; the Crown
  // Stonebound holds its own copy (library LIB.liveCopy.stoneboundEruptingGround, damage enemies only): see SKYGLASS_COPY.
};
/** Live jutsu -> the Skyglass-only copy a Crownhold record holds instead (RUL-2026-10-28-026 item 2). */
export const SKYGLASS_COPY: Record<string, string> = { jBRyl7F4UjTyxG5nnzLqj: LIB.liveCopy.stoneboundEruptingGround };
export const useSkyglassCopies = (jutsuIds: string[], rules: any[]) => ({
  jutsuIds: jutsuIds.map((j) => SKYGLASS_COPY[j] ?? j),
  rules: rules.map((r) => (r.action?.jutsuId && SKYGLASS_COPY[r.action.jutsuId] ? { ...r, action: { ...r.action, jutsuId: SKYGLASS_COPY[r.action.jutsuId] } } : r)),
});
const repoDoc = (f: string) => JSON.parse(readFileSync(join(process.env.TNR_REPO!, f), "utf8"));
/**
 * Template rows for the Crown Archivist and Crown Stonebound: the push/272 create payload (kit, rules, pools, level),
 * with the combat stats from the live readback (tnr_results_1792984876132.json: the server stored 812,519.2 /
 * 926,605.8 instead of the sent 1,391,299.95). Jutsu records from the captures. The Archivist's solo stats are then
 * replayed through scaleEditedAi like a Forge edit; the Stonebound is used as stored (only summoned; its strength in
 * the hunt is set by the summon's aiHp and power %).
 */
export const crownTemplates = (donorRow: any, jutsuCatalog: Record<string, any>, HP: HuntParams) => {
  const m = repoDoc("archive/spent-manifests/push-2026-10-25/272_crownhold_ais.json");
  const res = repoDoc("harvests/inbox/tnr_results_1792984876132.json");
  const out: Record<string, { row: any; profile: any; notes: string[] }> = {};
  for (const [id, slot] of Object.entries(CROWN_SLOT)) {
    const item = m.items.find((i: any) => i.srcId === slot);
    const rb = res.entries.find((e: any) => e.id === id);
    const live: Record<string, number> = {};
    for (const f of rb?.asserted?.fail ?? []) {
      const mm = /live ([\d.]+)/.exec(f.d?.[0] ?? "");
      if (mm) live[f.k] = Number(mm[1]);
    }
    const d0 = item.data;
    const sw = useSkyglassCopies(d0.jutsus, d0.rules);
    const d = { ...d0, jutsus: sw.jutsuIds, rules: sw.rules };
    for (const jid of d.jutsus) {
      jutsuCatalog[jid] ??= buildLibrary()[jid];
      jutsuCatalog[jid] ??= capturedJutsu(jid).record;
      const fix = LIVE_JUTSU_FIXES[jid];
      if (fix && !jutsuCatalog[jid].__fixed) {
        const rec = fix.apply(structuredClone(jutsuCatalog[jid]));
        const ok = JutsuValidator.safeParse(rec);
        if (!ok.success) throw new Error(`live fix ${jid}: ${ok.error.message}`);
        jutsuCatalog[jid] = Object.defineProperty(rec, "__fixed", { value: true, enumerable: false });
      }
    }
    const hp = 5050 * d.poolsMultiplier;
    const stored: any = {
      ...structuredClone(donorRow), userId: id, username: NAME[id], level: d.level, rank: d.rank, regeneration: d.regeneration,
      poolsMultiplier: d.poolsMultiplier, statsMultiplier: d.statsMultiplier,
      maxHealth: hp, curHealth: hp, maxChakra: hp, curChakra: hp, maxStamina: hp, curStamina: hp,
      ninjutsuMastery: d.ninjutsuMastery, genjutsuMastery: d.genjutsuMastery, taijutsuMastery: d.taijutsuMastery, bukijutsuMastery: d.bukijutsuMastery,
      offence: live.offence ?? d.offence, defence: live.defence ?? d.defence, strength: live.strength ?? d.strength,
      intelligence: live.intelligence ?? d.intelligence, willpower: live.willpower ?? d.willpower, speed: live.speed ?? d.speed,
      preferredGeneral1: d.preferredGeneral1, preferredGeneral2: d.preferredGeneral2,
      effects: structuredClone(d.effects), items: [], aiProfileId: `profile-${id}`, isSummon: false,
      jutsus: d.jutsus.map((jid: string, i: number) => ({
        id: `crown-${slot}-${i}`, userId: id, jutsuId: jid, level: 1, experience: 0, equipped: true, finishTraining: null,
        reskinId: null, activeReskin: null, createdAt: new Date(0), updatedAt: new Date(0), jutsu: structuredClone(jutsuCatalog[jid]),
      })),
    };
    const notes = [`push/272 ${slot} with live readback stats (${Object.keys(live).length} fields)`];
    let row = stored;
    const s = HP.stats[id];
    if (s) {
      row = { ...structuredClone(stored), poolsMultiplier: s.pools, ...(s.stats ? { statsMultiplier: s.stats } : {}) };
      scaleEditedAi(stored, row);
      row.effects = idgRows(s.rows);
      notes.push(`solo edit poolsMultiplier ${s.pools}${s.stats ? `, statsMultiplier ${s.stats}` : ""}, ${s.rows} damage rows via scaleEditedAi -> maxHealth ${row.maxHealth}`);
    }
    const profile = { id: `profile-${id}`, userId: id, name: NAME[id], includeDefaultRules: d.includeDefaultRules, rules: structuredClone(d.rules) };
    out[id] = { row, profile, notes };
  }
  return out;
};

/* ------------------------------------------------------------------ */
/* Player companion pet (RUL-2026-10-28-013: pets join QUEST battles)    */
/* ------------------------------------------------------------------ */
/**
 * One modelled mid-rank companion per player (no pet record is captured). Same model as the Wreck harness's petFor
 * (fable/skyglass-wreck-sim working tree), restated here so the shared model.ts is not edited:
 * - rank: the middle of what a JONIN owner allows (max 7): rank 5 "Hunter", at its level cap 30;
 * - stats: half the stat caps of the pet rank's character rank (Hunter -> CHUNIN caps), evenly;
 * - species: COMMON ASSAULT, no passives, no PETS-type jutsu (none captured), the engine's default AI rules
 *   (close in, highest-power damage: its basic attack); spawn BEHIND the owner.
 * The engine builds the battle actor (addPetsToBattle): HP calcHP(30), a summon-like AI on the player's side, fresh in
 * every battle (pet HP does not carry between pyramid fights).
 */
export const petFor = (owner: any, statFraction = 0.5) => {
  const rank = 5;
  const levelCap = 30;
  const caps = getUserCaps("CHUNIN");
  const species = {
    id: "harness-species", name: "Harness Companion", description: "modelled mid-rank companion", artDirection: null, rankConcepts: [],
    rarity: "COMMON", role: "ASSAULT", preferredDamageElement: null, defaultJutsuIds: [], aiRules: [], includeDefaultRules: true,
    effects: [], skillTarget: "SELF", isActive: true, createdAt: new Date(0), updatedAt: new Date(0),
  };
  let experience = calcLevelRequirements(levelCap - 1);
  while (calcLevel(experience) < levelCap) experience += 1000;
  return {
    id: `pet-${owner.userId}`, userId: owner.userId, name: `${owner.username}'s companion`, speciesId: species.id, paletteIndex: 0,
    characteristicIndex: 0, auraIndex: 0, gender: null, rank, experience, storedExperience: 0, lastFedAt: null, jutsuIds: [], skillIds: [],
    offence: caps.stats_cap * statFraction, defence: caps.stats_cap * statFraction,
    strength: caps.gens_cap * statFraction, speed: caps.gens_cap * statFraction,
    intelligence: caps.gens_cap * statFraction, willpower: caps.gens_cap * statFraction,
    avatar: "harness-pet-avatar", avatarFacing: "left", battleEnabled: true, spawnPosition: "BEHIND", aiRules: [],
    includeDefaultRules: true, generationStatus: "READY", generationToken: null, generationStartedAt: null, generationAttempts: 0,
    artRank: rank, revision: 0, createdAt: new Date(0), updatedAt: new Date(0), species,
  };
};
