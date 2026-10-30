/**
 * Skyglass charts (the map system, docs/design/SKYGLASS_LOOT_TABLES.md section 5; RUL-2026-10-28-009/-010/-013/-020/-022):
 * enemy records, twist hazards and the run sequences of the two common charts, the two rare charts, the two tainted
 * rares and the steeping fight. Solo player plus one companion pet.
 *
 * Built on the hunts (engine/hunts.ts): the same live crew records with their solo-tuned stats and shared kits, the
 * shared set-piece library (engine/library.ts), and the Crownhold records. Every record beyond those is a CHART-NEW
 * candidate listed in `newRecords` (placeholder ids `chart-*`):
 * - Lingering Echo (Sealed Reliquary twist, Boss Fights section 8): an immobile hazard AI holding fallen bosses'
 *   library mark + blast pairs; no new jutsu.
 * - Burning Deck (The Fall twist): an immobile hazard AI that lays `drain` ember ground in growing bands; 4 new jutsu
 *   (one per band: the engine has no growing pattern).
 * - Steeping Horror: the Core Horror copy for steeping (no Core Rot drop, RUL-2026-10-28-013).
 *
 * Scaling (`opponent_scaled_to_user`) is the engine's own: initiateBattle sets every target's level to the initiating
 * player's and runs scaleUserStats(target, "ai") before capUserStats (routers/combat.ts:3088-3091 at 2af4b320).
 */
import { scaleUserStats } from "@/libs/profile";
import { anim, cast, cond, endTurn, jutsu, rule, tag, T } from "./kitlib";
import { buildEndgame, buildHunts, CREW_TO_LIB, CROWN_SLOT, type HuntParams, LIVE, NAME } from "./hunts";
import { IDS } from "./kits";
import { LIB, MARKER_TYPES, type MarkKey } from "./library";

/* ------------------------------------------------------------------ */
/* Ids                                                                  */
/* ------------------------------------------------------------------ */
export const C = {
  oathkeeper: "0PZU_FvlbM3ErYGlD5r56", // live crew record (baseline), shared kit dg-oathkeeper
  replicant: "vjEFUJ9mb1zNTuQf4lfXv", // Crownhold D3.BOSS Replicant Zero (state/crownhold/ids.json)
  echo2: "chart-lingering-echo-2", echo3: "chart-lingering-echo-3", echo4: "chart-lingering-echo-4",
  deck: "chart-burning-deck",
  steep: "chart-steeping-horror",
} as const;
Object.assign(NAME, {
  [C.oathkeeper]: "Oathkeeper", [C.replicant]: "Replicant Zero", [C.echo2]: "Lingering Echo", [C.echo3]: "Lingering Echo",
  [C.echo4]: "Lingering Echo", [C.deck]: "Burning Deck", [C.steep]: "Steeping Horror",
});
// Replicant Zero comes from push/272 like the other Crownhold records (hunts.ts crownTemplates).
CROWN_SLOT[C.replicant] = "crownhold_d3.boss";

export const EMBER_ANIM = "tg_ember";
const W = 12;
const H = 10;

/* ------------------------------------------------------------------ */
/* Params                                                               */
/* ------------------------------------------------------------------ */
export type ChartParams = HuntParams & {
  /** Lingering Echo: pools, +100% rows, rounds it lingers (its rules end at this round, then it fades). */
  echo: { pools: number; rows: number; fade: number };
  /** Burning Deck: drain % of max HP per action on an ember; the round each band is laid. */
  ember: { power: number; rounds: number[]; pools: number };
  /** Steeping Horror (scaled to the player): pools and rows. */
  steep: { pools: number; rows: number };
  /** Tainted twists: entry pools %, elementalseal rounds, afterburn % and rounds. */
  tainted: { givePools: number; sealRounds: number; afterburn: number; afterburnRounds: number; echo?: "echo2" | "echo3" };
  /**
   * Common-chart crew copies (scaled to the player): statsMultiplier for all, and per live id pools / +100% rows.
   * The live crew records cannot serve: their statsMultiplier 5 gives a scaled copy 5 x half the level budget per stat
   * (2.5x a level-50 player's), and changing it on the live record rescales the hunts' stored stats (scaleEditedAi).
   */
  commons: {
    stats: number; rowsAdd?: number; poolsScale?: number;
    /** Softening rows (schema floor: statsMultiplier and poolsMultiplier >= 1): innate +damage-taken % rows and a -damage-given %. */
    taken?: number[]; givenDown?: number;
    byId: Record<string, { pools: number; rows: number; stats?: number; taken?: number[]; givenDown?: number }>;
  };
  /**
   * Rare-chart stat copies (unscaled, endgame), opt-in per live id: { pools, rows }. The hunt records are tuned as one
   * boss from full HP; a carried-HP gauntlet of four needs lighter copies. Ids not listed fight as the live record.
   */
  rares: { byId: Record<string, { pools: number; rows: number }> };
  /** Tainted-run stat copies (chart-t-*), opt-in per live id, for the pair fights; ids not listed use the rare copy / live. */
  taintedCopies: { byId: Record<string, { pools: number; rows: number }> };
};
export const DEFAULT_CHART_EXTRA = {
  echo: { pools: 2, rows: 1, fade: 10 },
  ember: { power: 5, rounds: [1, 4, 7], pools: 3 },
  steep: { pools: 2, rows: 2 },
  tainted: { givePools: 70, sealRounds: 2, afterburn: 30, afterburnRounds: 3 },
  commons: { stats: 2, byId: {} as Record<string, { pools: number; rows: number; stats?: number }> },
  rares: { byId: {} as Record<string, { pools: number; rows: number }> },
  taintedCopies: { byId: {} as Record<string, { pools: number; rows: number }> },
};
/** Rare-chart copy ids (placeholders), keyed by the live record they copy. */
export const COPY_R: Record<string, string> = {};
/** Common-chart crew copy ids (placeholders), keyed by the live record they copy. */
export const COPY: Record<string, string> = {};
export const COMMON_CREW = [LIVE.warden, LIVE.charge, LIVE.keeper, LIVE.sentinel, LIVE.wayfinder, LIVE.blade, C.oathkeeper];
for (const id of COMMON_CREW) {
  COPY[id] = `chart-c-${NAME[id]!.toLowerCase().replaceAll(" ", "-")}`;
  NAME[COPY[id]!] = NAME[id]!;
}

/* ------------------------------------------------------------------ */
/* Records                                                              */
/* ------------------------------------------------------------------ */
const idgRows = (n: number) => Array.from({ length: n }, () => tag("increasedamagegiven", { power: 100, rounds: 99, calculation: "percentage", description: "Increased damage given" }));
const primed = (k: MarkKey) => cond.marker(1, MARKER_TYPES[k]);
const specificRound = (v: number) => ({ type: "specific_round", value: v, description: "" });
const roundLt = (v: number) => ({ type: "round_lower_than", value: v, description: "" });

/** The ember bands: rows from the top edge down; the safe ground shrinks toward the bottom edge (the gangway). */
// drain is a SHARED_COOLDOWN_TAGS type (drizzle/constants.ts:265-286): one band locks the others for 3 rounds, so the
// bands are laid at least 3 rounds apart.
export const EMBER_BANDS = [[0, 1, 2], [3, 4], [5, 6]] as const;
const bandCells = (rows: readonly number[]) => {
  const out: { longitude: number; latitude: number }[] = [];
  for (let c = 0; c < W; c++) for (const r of rows) out.push({ longitude: c, latitude: r });
  return out;
};

/** Echo pairs per Reliquary fight (Boss Fights section 8): the Warden's Pour Line, the Sealwright's Script Lines, the Sentinel's Tide Line. */
export const ECHO_PAIRS: Record<string, MarkKey[]> = { [C.echo2]: ["lines"], [C.echo3]: ["lines", "sealLines"], [C.echo4]: ["lines", "sealLines", "rowsA"] };
const markId = (k: MarkKey) => LIB.mark[k];
const blastId = (k: MarkKey) => (LIB.blast as any)[k] as string;

/** Lingering Echo rules: each pair marks on its scheduled odd rounds and blasts the next turn; it fades at `fade`. */
export const echoRules = (pairs: MarkKey[], fade: number) => {
  const period = Math.max(4, 2 * pairs.length);
  const R: any[] = [];
  for (const k of pairs) R.push(cast(`${k}: the echo's blast`, blastId(k), "SELF", [primed(k)]));
  for (const k of pairs) R.push(endTurn(`${k}: hold after the mark`, [primed(k)]));
  pairs.forEach((k, i) => {
    for (let r = 1 + 2 * i; r < fade; r += period) R.push(cast(`${k}: the echo's mark (round ${r})`, markId(k), "SELF", [specificRound(r), roundLt(fade)]));
  });
  R.push(endTurn("linger (until it fades)", [roundLt(fade)]));
  // No rule matches from round `fade` on: the engine's give-up path removes it (ai_v2.ts "exhausted and has to give up").
  return R;
};

/** Burning Deck rules: one band per scheduled round, nothing else; it burns out after the last band. */
export const deckRules = (rounds: number[]) => [
  ...EMBER_BANDS.map((_, i) => cast(`Embers ${i + 1}`, `chart-embers-${i + 1}`, "SELF", [specificRound(rounds[i]!)])),
  endTurn("the deck burns", [roundLt(rounds[rounds.length - 1]! + 1)]),
];

export const buildCharts = (P: ChartParams, kitParams: any) => {
  const built = buildHunts(P, kitParams);
  const ov = built.override as any;
  const shared = (buildEndgame(kitParams, "endgame").override as any).newEnemies;
  const remap = (rules: any[]) => rules.map((r) => (r.action.jutsuId && CREW_TO_LIB[r.action.jutsuId] ? { ...r, action: { ...r.action, jutsuId: CREW_TO_LIB[r.action.jutsuId] } } : r));
  const kitOf = (rules: any[]) => [...new Set(rules.map((r) => r.action.jutsuId).filter(Boolean))] as string[];
  const newRecords: Record<string, any> = {};

  // Oathkeeper: live crew record with the shared kit (dg-oathkeeper), stats like the other solo crew.
  const oathRules = remap(structuredClone(shared[IDS.oath].rules));
  const os = P.stats[C.oathkeeper] ?? { pools: 1, rows: 0 };
  ov.enemies[C.oathkeeper] = { aiEdit: { poolsMultiplier: os.pools }, effects: idgRows(os.rows), jutsuIds: kitOf(oathRules), rules: oathRules, includeDefaultRules: false };
  ov.signatures[C.oathkeeper] = oathRules.map((r: any, i: number) => (r.action.description.startsWith("Oath of Stillness") ? i : -1)).filter((i: number) => i >= 0);

  // Common-chart crew copies: the same kit and rules as the live record (hunts / shared kits), their own stats.
  for (const id of COMMON_CREW) {
    const src = ov.enemies[id];
    const cs = P.commons.byId[id] ?? { pools: P.stats[id]?.pools ?? 1, rows: P.stats[id]?.rows ?? 0 };
    const stats = cs.stats ?? (id === LIVE.charge ? 1 : P.commons.stats);
    ov.newEnemies[COPY[id]!] = {
      base: NAME[id], username: NAME[id],
      aiEdit: { poolsMultiplier: id === LIVE.charge ? cs.pools : Math.round(cs.pools * (P.commons.poolsScale ?? 1) * 100) / 100, statsMultiplier: stats },
      effects: [
        ...idgRows(id === LIVE.charge ? cs.rows : cs.rows + (P.commons.rowsAdd ?? 0)),
        ...((cs as any).taken ?? P.commons.taken ?? []).map((pct: number) => tag("increasedamagetaken", { power: pct, rounds: 99, calculation: "percentage", description: "Increased damage taken" })),
        ...(((cs as any).givenDown ?? P.commons.givenDown) ? [tag("decreasedamagegiven", { power: (cs as any).givenDown ?? P.commons.givenDown, rounds: 99, calculation: "percentage", description: "Decreased damage given" })] : []),
      ],
      ...(src.jutsuIds ? { jutsuIds: src.jutsuIds, rules: src.rules, includeDefaultRules: false } : {}),
    };
    ov.signatures[COPY[id]!] = ov.signatures[id] ?? [];
    newRecords[COPY[id]!] = { kind: "AI (copy)", note: `common-chart copy of ${NAME[id]}: same kit and rules, statsMultiplier ${stats}, pools ${cs.pools}; opponent_scaled_to_user` };
  }

  // Rare-chart and tainted-run stat copies (opt-in): same kit and rules as the live record, their own pools and rows.
  for (const [prefix, byId] of [["chart-r-", P.rares.byId ?? {}], ["chart-t-", P.taintedCopies?.byId ?? {}]] as const)
  for (const [id, cs] of Object.entries(byId)) {
    if (!NAME[id]) throw new Error(`copies: unknown id ${id}`);
    const cid = `${prefix}${NAME[id]!.toLowerCase().replaceAll(" ", "-")}`;
    COPY_R[id] = cid;
    NAME[cid] = NAME[id]!;
    const src = ov.newEnemies[id] ?? ov.enemies[id];
    if (!src) throw new Error(`rares.byId: ${NAME[id]} has no hunt kit to copy`);
    const isNew = !!ov.newEnemies[id];
    ov.newEnemies[cid] = {
      base: isNew ? src.base : NAME[id], username: NAME[id], aiEdit: { ...(src.aiEdit ?? {}), poolsMultiplier: cs.pools }, effects: idgRows(cs.rows),
      ...(src.jutsuIds ? { jutsuIds: src.jutsuIds, rules: src.rules, includeDefaultRules: false } : {}),
    };
    ov.signatures[cid] = ov.signatures[id] ?? [];
    newRecords[cid] = { kind: "AI (copy)", note: `${prefix === "chart-r-" ? "rare-chart" : "tainted-run"} copy of ${NAME[id]}: same kit and rules, pools ${cs.pools}, ${cs.rows} damage rows (unscaled)` };
  }

  // Lingering Echoes (no new jutsu: library pairs only). Deck Warden statline (level 100, statsMultiplier 5).
  for (const id of [C.echo2, C.echo3, C.echo4]) {
    const pairs = ECHO_PAIRS[id]!;
    const rules = echoRules(pairs, P.echo.fade);
    ov.newEnemies[id] = { base: "Deck Warden", username: "Lingering Echo", aiEdit: { poolsMultiplier: P.echo.pools }, effects: idgRows(P.echo.rows), jutsuIds: kitOf(rules), rules, includeDefaultRules: false };
    ov.signatures[id] = rules.map((r: any, i: number) => (r.action.jutsuId ? i : -1)).filter((i: number) => i >= 0);
    newRecords[id] = { kind: "AI (hazard)", note: `Sealed Reliquary twist: immobile, casts ${pairs.join(" + ")} (library pairs), fades at round ${P.echo.fade}`, rules };
  }

  // Burning Deck: 4 ember bands (drain ground + tg_ember visual), immobile, Seal Charge statline.
  for (let i = 0; i < EMBER_BANDS.length; i++) {
    const id = `chart-embers-${i + 1}`;
    ov.jutsu[id] = jutsu(id, {
      name: `Spreading Fire ${["I", "II", "III"][i]}`,
      description: "The burning deck spreads: embers on these rows burn whoever acts on them.",
      battleDescription: ["Fire catches the far planks.", "The fire spreads down the deck.", "Only the gangway is clear."][i]!,
      target: "GROUND", method: "COORDINATES", range: 0, cooldown: 3, actionCostPerc: 40,
      coordinateTargeting: { origin: "BATTLEFIELD", selection: "ALL", coordinates: bandCells(EMBER_BANDS[i]!), randomCount: 1 },
      effects: [
        tag("drain", { power: P.ember.power, rounds: 10, calculation: "percentage", friendlyFire: "ENEMIES", poolsAffected: ["Health"] }),
        T.visual(anim(EMBER_ANIM), 10),
      ],
    });
    newRecords[id] = { kind: "jutsu", note: `ember band rows ${EMBER_BANDS[i]!.join(",")}: drain ${P.ember.power}% max HP per action, 10 rounds (the tag maximum)` };
  }
  const dRules = deckRules(P.ember.rounds);
  ov.newEnemies[C.deck] = { base: "Seal Charge", username: "Burning Deck", aiEdit: { poolsMultiplier: P.ember.pools, statsMultiplier: 1 }, effects: [], jutsuIds: kitOf(dRules), rules: dRules, includeDefaultRules: false };
  ov.signatures[C.deck] = dRules.map((r: any, i: number) => (r.action.jutsuId ? i : -1)).filter((i: number) => i >= 0);
  newRecords[C.deck] = { kind: "AI (hazard)", note: `The Fall twist: immobile, lays ember bands at rounds ${P.ember.rounds.join(",")}, burns out after the last`, rules: dRules };

  // Steeping Horror: the Core Horror's shared kit and rules on a copy (no Core Rot drop); scaled to the player in battle.
  const hr = ov.enemies[LIVE.horror];
  ov.newEnemies[C.steep] = { base: "Core Horror", username: "Steeping Horror", aiEdit: { poolsMultiplier: P.steep.pools }, effects: idgRows(P.steep.rows), jutsuIds: hr.jutsuIds, rules: hr.rules, includeDefaultRules: false };
  ov.signatures[C.steep] = ov.signatures[LIVE.horror];
  newRecords[C.steep] = { kind: "AI (copy)", note: "Core Horror copy for steeping: same shared kit and rules, no AI drop; opponent_scaled_to_user" };

  return { override: ov, newRecords, built };
};

/** initiateBattle target scaling (routers/combat.ts:3088): level := player level, scaleUserStats(target, "ai"). */
export const scaledRow = (row: any, level: number) => {
  const r = structuredClone(row);
  r.level = level;
  scaleUserStats(r, "ai");
  return r;
};

/* ------------------------------------------------------------------ */
/* Runs                                                                 */
/* ------------------------------------------------------------------ */
export type Fight = {
  label: string; ids: string[]; allies?: string[]; scaled?: boolean; givePools?: number; debuffs?: any[]; boss?: boolean;
  /** The press-on room: lost -> the run still pays its base ending (RUL-2026-10-28-022). */
  pressOn?: boolean;
};
export type Run = { chart: string; fights: Fight[]; note?: string };

const qfx = (t: string, power: number, rounds: number, desc: string, calc = "static") => ({
  type: t, power, rounds, target: "INHERIT", direction: "offence", calculation: calc, powerPerLevel: 0, description: desc,
  appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "",
});

/** All runs. `twist: false` drops the rare twists (hazards) to measure what they add. */
export const buildRuns = (P: ChartParams, twist = true): Record<string, Run> => {
  const R: Record<string, Run> = {};
  const f = (label: string, ids: string[], o: Partial<Fight> = {}): Fight => ({ label, ids, ...o });
  const tw = (ids: string[], hz: string[]) => (twist ? [...ids, ...hz] : ids);
  const r = (id: string) => (P.rares.byId?.[id] ? `chart-r-${NAME[id]!.toLowerCase().replaceAll(" ", "-")}` : id);
  const t = (id: string) => (P.taintedCopies?.byId?.[id] ? `chart-t-${NAME[id]!.toLowerCase().replaceAll(" ", "-")}` : r(id));
  /* Common charts: opponent_scaled_to_user, any level. */
  R.lowtide = {
    chart: "Tide Chart: The Low Tide Run",
    fights: [
      f("breach: Deck Warden + Seal Charge", [COPY[LIVE.warden]!, COPY[LIVE.charge]!], { scaled: true }),
      f("flooded hold: Arsenal Keeper", [COPY[LIVE.keeper]!], { scaled: true }),
      f("tide line: Skyglass Sentinel", [COPY[LIVE.sentinel]!], { scaled: true, boss: true }),
      f("PRESS ON (proposed): chart room, Wayfinder", [COPY[LIVE.wayfinder]!], { scaled: true, pressOn: true }),
    ],
  };
  R.nightwatch = {
    chart: "Watch Roster: The Night Watch",
    fights: [
      f("first watch: Deck Warden + Seal Charge", [COPY[LIVE.warden]!, COPY[LIVE.charge]!], { scaled: true }),
      f("middle watch: Oathkeeper", [COPY[C.oathkeeper]!], { scaled: true }),
      f("relief: Deck Warden + Oathkeeper", [COPY[LIVE.warden]!, COPY[C.oathkeeper]!], { scaled: true, boss: true }),
      f("PRESS ON: Second Watch, First Blade", [COPY[LIVE.blade]!], { scaled: true, pressOn: true }),
    ],
  };
  /* Rare charts: endgame (unscaled live records). */
  R.reliquary = {
    chart: "Reliquary Seal: The Sealed Reliquary",
    fights: [
      f("1st echo: Foundry Warden", [r(LIVE.foundry)], { boss: true }),
      f(`2nd echo: Sealwright${twist ? " + Lingering Echo (Pour Line)" : ""}`, tw([r(LIVE.sealwright)], [C.echo2]), { boss: true }),
      f(`3rd echo: Skyglass Sentinel${twist ? " + Lingering Echo (Pour + Script)" : ""}`, tw([r(LIVE.sentinel)], [C.echo3]), { boss: true }),
      f(`last echo: First Blade${twist ? " + Lingering Echo (Pour + Script + Tide)" : ""}`, tw([r(LIVE.blade)], [C.echo4]), { boss: true }),
      f("PRESS ON (proposed): the Oathkeeper", [r(C.oathkeeper)], { pressOn: true, boss: true }),
    ],
  };
  R.fall = {
    chart: "The Last Heading: The Fall",
    fights: [
      f(`burning deck: Deck Warden + Seal Charge${twist ? " + embers" : ""}`, tw([r(LIVE.warden), r(LIVE.charge)], [C.deck])),
      f(`gun deck: Arsenal Keeper + Deck Warden${twist ? " + embers" : ""}`, tw([r(LIVE.keeper), r(LIVE.warden)], [C.deck])),
      f(`the break: Core Horror${twist ? " + embers" : ""}`, tw([r(LIVE.horror)], [C.deck]), { boss: true }),
      f("PRESS ON (proposed): The Captain at the helm", [r(LIVE.captain)], { pressOn: true, boss: true }),
    ],
  };
  /* Tainted rares. */
  const seal = [qfx("elementalseal", 100, P.tainted.sealRounds, "The rot: your elemental jutsu are sealed")];
  const burn = [qfx("afterburn", P.tainted.afterburn, P.tainted.afterburnRounds, "The fire: you take extra burn damage", "percentage")];
  R.rotted = {
    chart: "Rotted Reliquary (tainted)",
    fights: [
      f("echoes rise in pairs: Foundry Warden + Sealwright", [t(LIVE.foundry), t(LIVE.sealwright)], { givePools: P.tainted.givePools, debuffs: seal, boss: true }),
      f(`last pair: Skyglass Sentinel + First Blade${twist ? ` + Lingering Echo (${P.tainted.echo === "echo3" ? "Pour + Script" : "Pour"})` : ""}`, tw([t(LIVE.sentinel), t(LIVE.blade)], [P.tainted.echo === "echo3" ? C.echo3 : C.echo2]), { debuffs: seal, boss: true }),
      f("PRESS ON: Replicant Zero", [t(C.replicant)], { debuffs: seal, pressOn: true, boss: true }),
    ],
  };
  R.burning = {
    chart: "Burning Heading (tainted)",
    fights: [
      f(`the break: Core Horror${twist ? " + embers" : ""}`, tw([(LIVE.horror)], [C.deck]), { givePools: P.tainted.givePools, debuffs: burn, boss: true }),
      f(`gun deck with the Captain: Arsenal Keeper + Deck Warden${twist ? " + embers" : ""}`, tw([(LIVE.keeper), (LIVE.warden)], [C.deck]), { allies: [LIVE.captain], debuffs: burn }),
      f("gangway duel (Captain beside you): Wayfinder", [(LIVE.wayfinder)], { allies: [LIVE.captain], debuffs: burn, boss: true }),
      f(`PRESS ON (proposed): First Blade on the burning deck${twist ? " + embers" : ""}`, tw([(LIVE.blade)], [C.deck]), { allies: [LIVE.captain], debuffs: burn, pressOn: true, boss: true }),
    ],
  };
  R.steeping = { chart: "Steeping (the Core)", fights: [f("steeping: Steeping Horror (scaled)", [C.steep], { scaled: true, boss: true })] };
  return R;
};
