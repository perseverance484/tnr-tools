/**
 * The Crowned Captain (Crownhold D5.BOSS, live id 7QofodAiUwIoM-voiA2p6): solo boss fight, offline.
 * Set pieces from the shared library (engine/library.ts, library_spec.json; SKYGLASS_BOSS_FIGHTS.md 5a):
 *   Crownfall        = Omen: Lines + Crownfall (library signature)
 *   Command Absolute = Omen: Last Light, Binding + Command Absolute "Kneel." (library signature)
 *   Shardstorm       = Omen: Scatter A / B + the shared scatter blast (his line rides on the Last Directive)
 * His own new records: The Crown's Will and Recall only.
 *
 *   TNR_SCRIPT=crowned_captain.ts run.sh [--params /abs/p.json] [--seeds 60] [--seed 1] [--dodge both|on|off]
 *        [--start full|0.7] [--out results.json] [--write-spec /abs/spec.json] [--trace SEED] [--debugfx]
 *        [--probe-inject [--probe-out f.json]]
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { performAIaction } from "@/libs/combat/ai_v2";
import { availableUserActions, performBattleAction } from "@/libs/combat/actions";
import { alignBattle, getBattleGrid } from "@/libs/combat/util";
import { PLAYER_VARIANTS, loadJson, playerQueryUser } from "./model";
import { assembleFloor, mulberry32 } from "./sim";
import {
  args, C, type Cell, coords, DONOR_SUMMON, dmg, IMG, IN, idgRowTags, J, jutsuRecord, LIB, LIB_POWERS, MARKER_TYPES, PATTERNS,
  opt, R, runFight, SIZE, STAT_PER_MULT, STATS, summarise, t0, tagBase, userJutsu, validator, aiRow, buildLibraryRecords, uniq, lineCells, key,
  allCapturedRecords, afterMark, type FightConfig, type PlayerStart,
} from "./cclib";

/* ------------------------------------------------------------------ parameters */
export const CC_DEFAULTS = {
  name: "chain_tuned", // RUL-2026-10-28-013: tuned for the Crownhold chain (pools carried), report 4
  poolsMultiplier: 3, // report 2: 5 (director's doubled HP); 3 keeps the fight inside 20 rounds (Kitsune bonus)
  statsMultiplier: 5.83, // inert in battle (JONIN stat cap)
  idgRows: 0.25, // one +25% row
  throne: [9, 4] as [number, number],
  echoHp: 2500, echoPower: 70, echoRounds: 3, recallCd: 8,
  recallTarget: "EMPTY_GROUND_CLOSEST_TO_SELF" as string,
  phase3Extermination: false, // true: Extermination Order in phase 3 as well (report 2: 80% wins, 8.7% HP)
  // The innate sealprevent row collides with the library's Last Light, Binding marker (sealprevent): has_effect would
  // always be true and Command Absolute would fire every turn. The boss has no bloodline, so the row does nothing.
  dropInnateSealprevent: true,
  /** The plain attack after a mark (and after a refused CHARACTER blast): "basic" = basic attack (adjacent only),
   * "kit" = Devouring Grasp / Scorching Rend. */
  afterMarkAttack: "basic" as "basic" | "kit",
  /** Analysis only: override library powers (LIB_POWERS keys) to measure what the library owner would need to
   * change. Empty in the shipped tuning; the spec never carries copies of library records. */
  libPowers: {} as Record<string, number>,
  /** Analysis only (report 3, pre-5f6c3edb): replace the library's Lines pattern by report 1's five-ray fan. */
  libLinesFan: false,
  /** A kit jutsu cast first while the player carries Alarm Raised (rounds 1-2): Crownhold's alert route. */
  alarmStrike: null as string | null,
  /** The Crown's Will (his own record, a copy of Oni's Hunger): damage-given power and rounds. Live Oni's Hunger is
   * +60% for 99 rounds; a short, stronger Will makes phase 1 (the duel) the dangerous stretch. */
  crownsWillPower: 50,
  crownsWillRounds: 7,
  /** Extra +100% damage-given rows on The Crown's Will (each multiplies; the engine caps one row at +100%). */
  crownsWillExtraRows: 2,
  /** Phase 2 fillers: Scorching Rend / Devouring Grasp between the design's phase-2 moves (Recall, Command
   * Absolute, Stolen Form, Extermination Order). false = the design's list only. */
  phase2Fillers: false,
  /** Phase 2 also lays Omen: Lines (Crownfall) after Recall, ahead of Stolen Form and Extermination Order. */
  phase2Lines: true,
};
export type CCParams = typeof CC_DEFAULTS;
export const ccParams = (over: any = {}): CCParams => ({ ...CC_DEFAULTS, ...over });

export const ID = {
  oniHunger: "w4F7-w5ubgKsqYPBPvRuV", stolenForm: "VuFuBtE7h5B1nnA2J1lFZ", purging: "HcAs8gBtvopPZkjP8HCC2",
  veilstep: "IBjVpLutojh3m9PRnIce-", windSpear: "A5HrHSzx4J3WM4Fln8Lbf", hexweave: "_JRHgRL8pfUvt_-q1Xa3H",
  extermination: "EqZsaqser8c2-KpVCaXk_", scorchingRend: "Uou0sCjZ1rwiMJZ-JWEI_", devouringGrasp: "lft52q7DE_JjhR7PKXimB",
  lastDirective: "GHFMU_DDKvBBp5BEuTeah", finalCommand: "X2P22h8ApDmTZHjWpNO87", keelbind: "PdD44PGaNv4MN5fOALhAF",
  ruinRefrain: "EQ93LX8wvuIAd5u75q_i1",
  countermand: "W3lOjQhhIPUYPkIZmiNum", solarBow: "ALqXVSL58QMfJ4DgoJ5Il",
  // His own new records (placeholder ids until created); Crownfall and Command Absolute are library signatures
  crownsWill: "cc-crowns-will", recall: "cc-recall", crownfall: LIB.sig.crownfall, command: LIB.sig.commandAbsolute,
};
export const BOSS_ID = IN.boss.id as string;
const LIB_POWERS_SHIPPED = { ...LIB_POWERS };
const LINES_SHIPPED = PATTERNS.lines;
/** Five true hex rays west from an odd-column caster on the FLAT battle grid (report 1's Crownfall fan), as offsets. */
const FAN = (() => {
  const o: Cell = [9, 4];
  const cells = uniq([[0, 0], [0, 2], [0, 4], [0, 7], [0, 9]].flatMap((t) => lineCells(o, t as Cell))).filter((c) => key(c) !== key(o));
  return cells.map((c) => ({ longitude: c[0] - o[0], latitude: c[1] - o[1] }));
})();
export const ECHO_ID = IN.echo.id as string;

export const buildBespoke = (P: CCParams) => {
  const oni = J(ID.oniHunger);
  return [
    jutsuRecord(ID.crownsWill, {
      name: "The Crown's Will", target: "SELF", method: "SINGLE", range: 0, cooldown: oni.cooldown, actionCostPerc: oni.actionCostPerc,
      description: "The Command Crown answers its wearer. Its frost points glint, and every echo in the hall stands straighter.",
      battleDescription: "%user does not rise. \"Another echo come home.\"",
      effects: [
        ...oni.effects.map((e: any, i: number) => ({
          ...e, rounds: P.crownsWillRounds, ...(e.type === "increasedamagegiven" ? { power: P.crownsWillPower } : {}),
          ...(i === 0 ? { staticAnimation: "cc_crown_aura" } : {}),
        })),
        ...Array.from({ length: P.crownsWillExtraRows }, () => ({
          ...oni.effects.find((e: any) => e.type === "increasedamagegiven"), power: 100, rounds: P.crownsWillRounds,
        })),
      ],
    }),
    jutsuRecord(ID.recall, {
      ...structuredClone(DONOR_SUMMON), id: ID.recall, name: "Recall", image: IMG, jutsuType: "AI", jutsuRank: "S",
      hidden: true, injectableInBattle: false, battleUsageType: "BOTH", requiredRank: "STUDENT", requiredLevel: 1,
      bloodlineId: null, villageId: null, chakraCost: 0, staminaCost: 0, healthCost: 0,
      target: "EMPTY_GROUND", method: "SINGLE", range: 5, cooldown: P.recallCd, actionCostPerc: 60,
      description: "The crown calls an officer of Crownhold back out of chakra haze. It stands for as long as he commands.",
      battleDescription: "\"Stand, soldier.\" An echo rises at his word.",
      effects: DONOR_SUMMON.effects.filter((e: any) => e.type === "summon").map((e: any) => ({
        ...e, aiId: ECHO_ID, aiHp: P.echoHp, power: P.echoPower, powerPerLevel: 0, rounds: P.echoRounds, appearAnimation: "cc_recall",
      })),
    }),
  ];
};
/** The Last Directive: cosmetic edit only (design log line, carrying Shardstorm's image; animations). */
export const editedLastDirective = () => {
  const ld = { ...jutsuRecord(ID.lastDirective, {}), ...J(ID.lastDirective), id: ID.lastDirective };
  ld.battleDescription = "\"Preserve command.\" The crown blazes, and its points crack loose above him.";
  ld.effects = ld.effects.map((e: any) => (e.type === "finalstand" ? { ...e, staticAnimation: "cc_last_directive", appearAnimation: "cc_phase_shift" } : e));
  return ld;
};
export const ccRecords = (P: CCParams) => {
  Object.assign(LIB_POWERS, LIB_POWERS_SHIPPED, P.libPowers ?? {});
  PATTERNS.lines = P.libLinesFan ? FAN : LINES_SHIPPED;
  const recs: Record<string, any> = { ...allCapturedRecords() };
  recs[ID.extermination] = { ...jutsuRecord(ID.extermination, {}), ...J(ID.extermination), id: ID.extermination };
  recs[ID.lastDirective] = editedLastDirective();
  for (const r of buildBespoke(P)) recs[r.id] = r;
  Object.assign(recs, buildLibraryRecords());
  return recs;
};

const PLAYER = "CLOSEST_OPPONENT";
const M = MARKER_TYPES;
export const ccRules = (P: CCParams) => [
  // Blasts first: the marker left by last turn's mark.
  R.jutsu(LIB.blast.scatterB, "SELF", [C.has(M.scatterB)]),
  R.jutsu(LIB.blast.scatterA, "SELF", [C.has(M.scatterA)]),
  R.jutsu(ID.command, "SELF", [C.has(M.lastLightBinding)]),
  R.jutsu(ID.crownfall, "SELF", [C.has(M.lines)]),
  ...(P.alarmStrike ? [R.jutsu(P.alarmStrike, PLAYER, [C.tHas("increasedamagetaken", 10), C.round(3), C.near(5)])] : []),
  // The throne (a no-op once there; before any mark, so Lines are laid from it).
  R.moveTo(P.throne),
  // After a mark: one plain attack with the 60 AP left, then end turn (never two marks in a turn).
  ...(["scatterA", "scatterB", "lastLightBinding", "lines"] as const).flatMap((k) => afterMark(k, P.afterMarkAttack === "kit"
    ? [R.jutsu(ID.devouringGrasp, PLAYER, [C.near(5)]), R.jutsu(ID.scorchingRend, PLAYER, [C.near(5)])]
    : [R.jutsu("basicAttack", PLAYER, [C.near(1)])])),
  // Phase 3 (under 30%): the Last Directive; Purging Stance (Final Stand does not floor DoT ticks); Shardstorm marks
  // (A, then B while A cools down).
  R.jutsu(ID.lastDirective, "SELF", [C.hb(30)]),
  R.jutsu(ID.purging, "SELF", [C.hb(30), C.has("afterburn")]),
  R.jutsu(ID.purging, "SELF", [C.hb(30), C.has("poison")]),
  R.jutsu(LIB.mark.scatterA, "SELF", [C.hb(30)]),
  R.jutsu(LIB.mark.scatterB, "SELF", [C.hb(30)]),
  ...(P.phase3Extermination ? [R.jutsu(ID.extermination, PLAYER, [C.hb(30), C.near(5)])] : []),
  R.end([C.hb(30)]),
  // Phase 2 (60-30%)
  R.jutsu(LIB.mark.lastLightBinding, "SELF", [C.hb(60)]),
  R.jutsu(ID.recall, P.recallTarget, [C.hb(60), C.noSummon()]),
  ...(P.phase2Lines ? [R.jutsu(LIB.mark.lines, "SELF", [C.hb(60)])] : []),
  R.jutsu(ID.stolenForm, PLAYER, [C.hb(60), C.tHas("increasedamagegiven", 50), C.near(4)]),
  R.jutsu(ID.extermination, PLAYER, [C.hb(60), C.near(5)]),
  ...(P.phase2Fillers ? [R.jutsu(ID.scorchingRend, PLAYER, [C.hb(60), C.near(5)]), R.jutsu(ID.devouringGrasp, PLAYER, [C.hb(60), C.near(5)])] : []),
  R.item(ID.countermand, PLAYER, [C.hb(60), C.near(5)]),
  R.end([C.hb(60)]),
  // Phase 1 (100-60%): the duelist.
  R.jutsu(ID.crownsWill, "SELF", [C.round(2)]),
  R.jutsu(ID.veilstep, "SELF", [C.round(5), C.far(7)]),
  R.item(ID.countermand, PLAYER, [C.has("stealth"), C.near(5)]),
  R.jutsu(ID.purging, "SELF", [C.has("afterburn")]),
  R.jutsu(ID.windSpear, PLAYER, [C.tHas("shield", 1), C.near(5)]),
  R.jutsu(LIB.mark.lines, "SELF", []),
  R.jutsu(ID.hexweave, PLAYER, [C.near(4)]),
  R.jutsu(ID.finalCommand, PLAYER, [C.near(4)]),
  R.jutsu(ID.keelbind, PLAYER, [C.near(5)]),
  R.jutsu(ID.ruinRefrain, PLAYER, [C.near(5)]),
  R.jutsu(ID.scorchingRend, PLAYER, [C.near(5)]),
  R.jutsu(ID.devouringGrasp, PLAYER, [C.near(5)]),
  R.item(ID.solarBow, PLAYER, [C.near(5)]),
  R.end(),
];
export const CC_LIBRARY_USED = [LIB.mark.lines, LIB.sig.crownfall, LIB.mark.lastLightBinding, LIB.sig.commandAbsolute, LIB.mark.scatterA, LIB.mark.scatterB, LIB.blast.scatterA, LIB.blast.scatterB];
export const ccKit = () => [
  ID.crownsWill, ID.stolenForm, ID.purging, ID.veilstep, ID.windSpear, ID.hexweave, ID.extermination, ID.scorchingRend,
  ID.devouringGrasp, ID.lastDirective, ID.finalCommand, ID.keelbind, ID.ruinRefrain, ID.recall,
  ...CC_LIBRARY_USED,
];
export const ccAiRecord = (P: CCParams) => ({
  ...IN.boss.data, username: "The Crowned Captain", poolsMultiplier: P.poolsMultiplier, statsMultiplier: P.statsMultiplier,
  ...Object.fromEntries(STATS.map((s) => [s, Math.round(STAT_PER_MULT * P.statsMultiplier * 100) / 100])),
  jutsus: ccKit(), effects: [...IN.boss.data.effects.filter((e: any) => !(P.dropInnateSealprevent && e.type === "sealprevent")), ...idgRowTags(P.idgRows)],
  includeDefaultRules: false, rules: ccRules(P),
});
export const CC_SETS = {
  [LIB.mark.lines]: ["crownfall", "mark"], [ID.crownfall]: ["crownfall", "land"],
  [LIB.mark.lastLightBinding]: ["command", "mark"], [ID.command]: ["command", "land"],
  [LIB.mark.scatterA]: ["shardstorm", "mark"], [LIB.mark.scatterB]: ["shardstorm", "mark"],
  [LIB.blast.scatterA]: ["shardstorm", "land"], [LIB.blast.scatterB]: ["shardstorm", "land"],
} as FightConfig["sets"];
export const ccFightConfig = (P: CCParams): FightConfig => {
  const recs = ccRecords(P);
  const rec = ccAiRecord(P);
  const boss = aiRow(BOSS_ID, rec, rec.offence, recs, rec.rules, rec.effects, IN.boss.data.items.flatMap((it: any) => it.ids));
  const e = IN.echo.data;
  const echo = aiRow(ECHO_ID, e, IN.echo.liveStats.offence, recs, e.rules, e.effects, []);
  return {
    bossId: BOSS_ID, rows: { [BOSS_ID]: boss, [ECHO_ID]: echo }, recs, sets: CC_SETS, setNames: ["crownfall", "command", "shardstorm"],
    phases: [60, 30], anchor: P.throne, special: { recall: ID.recall, lastDirective: ID.lastDirective, extermination: ID.extermination },
  };
};
export const ccValidate = (P: CCParams) => {
  const v = validator();
  for (const j of buildBespoke(P)) v.jutsu(j);
  const lib = buildLibraryRecords();
  for (const id of CC_LIBRARY_USED) v.jutsu(lib[id]);
  v.jutsu(editedLastDirective());
  for (const r of ccRules(P)) v.rule(r);
  const rec = ccAiRecord(P);
  v.ai(BOSS_ID, { ...rec, items: IN.boss.data.items });
  return v.issues;
};
export const ccSpec = (P: CCParams, issues: string[]) => ({
  _note: "The Crowned Captain build spec (Crownhold D5.BOSS). Generated by harness/skyglass_wreck_sim/engine/crowned_captain.ts --write-spec; offline engine-tested, not pushed. His set pieces are library records (library_spec.json, ids lib-*), referenced by id and not copied here; his own new records are cc-* (The Crown's Will, Recall). All are placeholder ids to replace with created ids (law 17: literal ids in the AI's jutsus and rules).",
  params: P,
  ai: { id: BOSS_ID, srcId: IN.boss.srcId, record: ccAiRecord(P) },
  newJutsu: buildBespoke(P),
  libraryUsed: { ids: CC_LIBRARY_USED, source: "library_spec.json (fable/skyglass-wreck-sim 5f6c3edb)", powers: { crownfall: LIB_POWERS.crownfall, commandAbsolute: LIB_POWERS.commandAbsolute, blastScatter: LIB_POWERS.blastScatter, scatterPool: LIB_POWERS.scatterPool } },
  editedJutsu: { [ID.lastDirective]: { note: "existing push/271 record: cosmetic edit only (battleDescription carries the design's line and Shardstorm's image; finalstand row animations)", battleDescription: editedLastDirective().battleDescription, effects: editedLastDirective().effects } },
  editedRecord: { innateSealprevent: P.dropInnateSealprevent ? "removed: it collides with the Last Light, Binding marker (sealprevent); the boss has no bloodline, so the row did nothing" : "kept" },
  setPieces: {
    Crownfall: { mark: LIB.mark.lines, blast: ID.crownfall },
    "Command Absolute": { mark: LIB.mark.lastLightBinding, blast: ID.command, stars: PATTERNS.stars },
    Shardstorm: { marks: [LIB.mark.scatterA, LIB.mark.scatterB], blasts: [LIB.blast.scatterA, LIB.blast.scatterB] },
  },
  kitRemoved: { Braced_Strike: "WvLCyGsPCKSDYl6-e_D9o", Surging_Overflow: "AicYoMMpZmHAykb_5hYtY", Rapid_Fire_live_Shuriken_Storm: "Nrxc8m9utE9qaD_gWpLgf", Worldbreaker_Chorus_live_Great_Bell_Toll: "LisNuMJ2gncEByAxG6QPI", Apex_Hunger_live_Onis_Hunger: `${ID.oniHunger} (replaced by its Crownhold-only copy The Crown's Will)` },
  kitAdded: { "Final Command": ID.finalCommand, Keelbind: ID.keelbind, "Ruin Refrain": ID.ruinRefrain },
  recallEcho: { id: ECHO_ID, name: IN.echo.data.username, source: IN.echo.source, note: "he never uses Omen: Last Light (red), whose summonprevent marker would block Recall" },
  arena: { grid: SIZE, orientation: "FLAT, odd columns offset (getBattleGrid)", throne: P.throne },
  animations: { cc_recall: ID.recall, cc_crown_aura: ID.crownsWill, cc_last_directive: ID.lastDirective, cc_phase_shift: `${ID.lastDirective} (30%)`, library: "the library records carry tg_*, dt_*, cc_crownfall and cc_command_absolute" },
  validation: issues.length ? issues : "valid",
});

/* ------------------------------------------------------------------ main */
const main = async () => {
  const P = ccParams(opt("params") ? loadJson(resolve(opt("params")!)) : {});
  const issues = ccValidate(P);
  console.log(issues.length ? `SPEC VALIDATION ISSUES:\n  ${issues.join("\n  ")}` : "spec valid against JutsuValidator / AiRule / insertAiSchema");
  const specPath = opt("write-spec");
  if (specPath) {
    mkdirSync(dirname(resolve(specPath)), { recursive: true });
    writeFileSync(resolve(specPath), `${JSON.stringify(ccSpec(P, issues), null, 1)}\n`);
    console.log(`wrote ${specPath}`);
  }
  const cfg = ccFightConfig(P);
  const startArg = opt("start", "full");
  const start: PlayerStart = startArg === "full" ? {} : { hpFrac: Number(startArg), cpFrac: Number(startArg), spFrac: Number(startArg) };
  const traceSeed = opt("trace");
  if (traceSeed) for (const dodge of [true, false]) {
    const f = await runFight(cfg, Number(traceSeed), dodge, start, true, args.includes("--debugfx"));
    console.log(`--- trace seed ${traceSeed} dodge ${dodge}: ${f.outcome} in ${f.rounds} rounds, player ${f.playerHpPct}%, boss ${f.bossHpPct}%`);
    for (const l of f.trace!) console.log("  " + l);
  }
  const seeds = Number(opt("seeds", traceSeed ? "0" : "40"));
  const seed0 = Number(opt("seed", "1"));
  const modes = opt("dodge", "both") === "both" ? [true, false] : [opt("dodge") === "on"];
  const results: any = { generatedBy: "engine/crowned_captain.ts", params: P, dmgConfig: dmg.name, grid: SIZE, seeds, seed0, start: startArg, modes: {} };
  if (seeds > 0) for (const dodge of modes) {
    const fs = [];
    for (let i = 0; i < seeds; i++) fs.push(await runFight(cfg, seed0 + i, dodge, start));
    const s = summarise(fs, cfg.setNames);
    results.modes[dodge ? "dodge_on" : "dodge_off"] = { summary: s, fights: fs };
    console.log(`\n== ${P.name} dodge ${dodge ? "ON " : "OFF"}: ${JSON.stringify(s)}`);
  }
  const outPath = opt("out");
  if (outPath) {
    mkdirSync(dirname(resolve(outPath)), { recursive: true });
    writeFileSync(resolve(outPath), `${JSON.stringify(results, null, 1)}\n`);
    console.log(`wrote ${outPath}`);
  }
  if (args.includes("--probe-inject")) await probeInject();
};

/* ------------------------------------------------------------------ probe: ground injectjutsus (kept from report 1) */
const probeInject = async () => {
  const P = ccParams();
  const log: Record<string, string[]> = {};
  for (const variant of ["inject", "inject_all", "damage_taken_tile", "inject_direct"] as const) {
    const rand = mulberry32(1);
    const orig = Math.random;
    Math.random = rand;
    const lines: string[] = [];
    try {
      const cfg = ccFightConfig(P);
      const boss = cfg.rows[BOSS_ID];
      const granted = jutsuRecord("cc-probe-granted", { ...J("Sic286tbCpCjwaic0EX5q"), id: "cc-probe-granted", name: "Probe: granted bolt", jutsuType: "SPECIAL", injectableInBattle: true, cooldown: 20, requiredRank: "STUDENT", requiredLevel: 1, elementClassification: "None", battleUsageType: "BOTH" });
      const tile: Cell = [6, 4];
      const eff = variant === "damage_taken_tile"
        ? tagBase("increasedamagetaken", { power: 20, rounds: 3, calculation: "percentage", friendlyFire: "ENEMIES", description: "probe" })
        : tagBase("injectjutsus", { jutsuIds: [granted.id], power: 25, rounds: 3, ...(variant === "inject" ? { friendlyFire: "ENEMIES" } : {}), description: "Grants a jutsu" });
      const castJ = variant === "inject_direct"
        ? jutsuRecord("cc-probe-direct", { name: "Probe: grant on the player", target: "OTHER_USER", method: "SINGLE", range: 5, cooldown: 99, actionCostPerc: 100, effects: [eff], description: "probe", battleDescription: "probe" })
        : jutsuRecord("cc-probe-tile", { name: "Probe: grant tile", target: "GROUND", method: "COORDINATES", coordinateTargeting: coords([tile]), range: 0, cooldown: 99, actionCostPerc: 100, effects: [eff], description: "probe", battleDescription: "probe" });
      const row = { ...boss, jutsus: [...boss.jutsus, userJutsu(BOSS_ID, castJ, 99)] };
      row.aiProfile = { ...row.aiProfile, rules: [R.jutsu(castJ.id, variant === "inject_direct" ? "CLOSEST_OPPONENT" : "SELF", [C.round(2)]), R.end()] };
      const player = playerQueryUser(0, { ...PLAYER_VARIANTS.average!, rules: [R.jutsu(granted.id, "CLOSEST_OPPONENT", []), R.end()] } as never, t0.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, t0.jutsu);
      let b = await assembleFloor({ players: [player], enemyRows: { ...cfg.rows, [BOSS_ID]: row }, floor: { kind: "boss", waves: [{ aiIds: [BOSS_ID], delayRounds: 0 }] }, rand, initialBarriers: false, dmgConfig: dmg.config, mode: "quest" });
      (b.extraState.jutsus as any)[granted.id] = granted; // initiateBattle preloads every injectableInBattle jutsu
      for (const [id, r] of Object.entries(cfg.recs)) if (!(b.extraState.jutsus as any)[id]) (b.extraState.jutsus as any)[id] = r;
      const puid = player.userId;
      const pu = () => b.usersState.find((u) => u.userId === puid)!;
      const bu = b.usersState.find((u) => u.controllerId === BOSS_ID)!;
      [pu().longitude, pu().latitude] = [5, 4];
      [bu.longitude, bu.latitude] = P.throne;
      const grid = getBattleGrid(1, b);
      const actionRounds: number[] = [];
      const has = () => availableUserActions(b, puid, true, true).some((a) => a.id === granted.id);
      const fxOn = () => b.usersEffects.filter((e: any) => e.targetId === puid && e.creatorId === bu.userId).map((e: any) => `${e.type} r${e.rounds}`);
      let moved = false;
      for (let step = 0; step < 80 && b.round <= 6; step++) {
        const pre = alignBattle(b, actionRounds, puid);
        if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
        const actor = pre.actor;
        if (variant !== "inject_direct" && actor.userId === puid && !moved && b.groundEffects.some((g: any) => g.creatorId === bu.userId && g.type !== "visual")) {
          const mv = availableUserActions(b, puid, true, true).find((a) => a.id === "move")!;
          b = performBattleAction({ battle: structuredClone(b), action: mv, grid, contextUserId: puid, actorId: puid, longitude: tile[0], latitude: tile[1] }).newBattle;
          moved = true;
          lines.push(`r${b.round} player MOVES onto the tile ${tile}: effects ${JSON.stringify(fxOn())}, granted jutsu available: ${has()}`);
          continue;
        }
        const res = performAIaction(b, grid, actor.userId);
        b = res.nextBattle;
        alignBattle(b, actionRounds, puid);
        const nm = res.nextActionId === granted.id ? "GRANTED JUTSU" : (b.extraState.jutsus as any)[res.nextActionId ?? ""]?.name ?? res.nextActionId;
        lines.push(`r${pre.actionRound} ${actor.userId === puid ? "player" : "boss"} ${nm} | effects ${JSON.stringify(fxOn())} granted available: ${has()}`);
      }
    } finally {
      Math.random = orig;
    }
    log[variant] = lines;
    console.log(`\n### probe: ground tile ${variant}`);
    for (const l of lines) console.log("  " + l);
  }
  const out = opt("probe-out");
  if (out) writeFileSync(resolve(out), `${JSON.stringify({ generatedBy: "engine/crowned_captain.ts --probe-inject", log }, null, 1)}\n`);
};

if (import.meta.main) await main();
