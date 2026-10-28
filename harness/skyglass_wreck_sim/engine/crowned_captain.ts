/**
 * The Crowned Captain (Crownhold D5.BOSS, live id 7QofodAiUwIoM-voiA2p6): solo boss fight, offline.
 * Set pieces from the shared library (SKYGLASS_BOSS_FIGHTS.md 5a; engine/cclib.ts) plus his bespoke blasts:
 *   Crownfall        = Omen: Lines + Crownfall (bespoke)
 *   Command Absolute = Omen: Last Light, Binding + Command Absolute "Kneel." (bespoke)
 *   Shardstorm       = Omen: Scatter A / B + the shared scatter blasts (his line rides on the Last Directive)
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
  args, C, type Cell, coords, DONOR_SUMMON, dmg, fx, IMG, IN, idgRowTags, J, jutsuRecord, LIB, LIB_DEFAULTS, type LibParams, MARKER,
  opt, PATTERN, R, runFight, SIZE, STARS, STAT_PER_MULT, STATS, summarise, t0, tagBase, userJutsu, validator, aiRow, buildLibrary,
  allCapturedRecords, type FightConfig, type PlayerStart,
} from "./cclib";

/* ------------------------------------------------------------------ parameters */
export const CC_DEFAULTS = {
  name: "library_hp2x",
  poolsMultiplier: 5, // director 2026-10-28: HP doubled (25,250)
  statsMultiplier: 5.83, // inert in battle (JONIN stat cap)
  idgRows: 0.5,
  throne: [9, 4] as [number, number],
  crownfallPower: 180,
  commandPower: 130, commandStunAp: 60, commandStunRounds: 2, commandSealRounds: 2,
  echoHp: 2500, echoPower: 70, echoRounds: 3, recallCd: 8,
  recallTarget: "EMPTY_GROUND_CLOSEST_TO_SELF" as string,
X
  lib: { ...LIB_DEFAULTS } as LibParams, // shared blast power 180, Omen cd 3, Last Light cd 6
};
export type CCParams = typeof CC_DEFAULTS;
export const ccParams = (over: any = {}): CCParams => ({ ...CC_DEFAULTS, ...over, lib: { ...CC_DEFAULTS.lib, ...(over.lib ?? {}) } });

export const ID = {
  oniHunger: "w4F7-w5ubgKsqYPBPvRuV", stolenForm: "VuFuBtE7h5B1nnA2J1lFZ", purging: "HcAs8gBtvopPZkjP8HCC2",
  veilstep: "IBjVpLutojh3m9PRnIce-", windSpear: "A5HrHSzx4J3WM4Fln8Lbf", hexweave: "_JRHgRL8pfUvt_-q1Xa3H",
  extermination: "EqZsaqser8c2-KpVCaXk_", scorchingRend: "Uou0sCjZ1rwiMJZ-JWEI_", devouringGrasp: "lft52q7DE_JjhR7PKXimB",
  lastDirective: "GHFMU_DDKvBBp5BEuTeah", finalCommand: "X2P22h8ApDmTZHjWpNO87", keelbind: "PdD44PGaNv4MN5fOALhAF",
  ruinRefrain: "EQ93LX8wvuIAd5u75q_i1",
  countermand: "W3lOjQhhIPUYPkIZmiNum", solarBow: "ALqXVSL58QMfJ4DgoJ5Il",
  // Bespoke Crownhold-only records (placeholder ids until created)
  crownsWill: "cc-crowns-will", crownfall: "cc-crownfall", command: "cc-command-absolute", recall: "cc-recall",
};
export const BOSS_ID = IN.boss.id as string;
export const ECHO_ID = IN.echo.id as string;

export const buildBespoke = (P: CCParams) => {
  const oni = J(ID.oniHunger);
  return [
    jutsuRecord(ID.crownsWill, {
      name: "The Crown's Will", target: "SELF", method: "SINGLE", range: 0, cooldown: oni.cooldown, actionCostPerc: oni.actionCostPerc,
      description: "The Command Crown answers its wearer. Its frost points glint, and every echo in the hall stands straighter.",
      battleDescription: "%user does not rise. \"Another echo come home.\"",
      effects: oni.effects.map((e: any, i: number) => ({ ...e, ...(i === 0 ? { staticAnimation: "cc_crown_aura" } : {}) })),
    }),
    // Lands on Omen: Lines (same CASTER offsets, cast from the same throne hex).
    jutsuRecord(ID.crownfall, {
      name: "Crownfall", target: "GROUND", method: "COORDINATES", coordinateTargeting: coords(PATTERN.lines, "ALL", "CASTER"),
      range: 0, cooldown: 1, actionCostPerc: 100, effects: [fx.damage(P.crownfallPower, "cc_crownfall")],
      description: "Frost-pointed shards of the crown fall point-first along the marked lines.",
      battleDescription: "Shards of the crown fall point-first along the red lines.",
    }),
    // Lands on Omen: Last Light, Binding. Stun and seal must be user effects, so it targets units over the pattern.
    jutsuRecord(ID.command, {
      name: "Command Absolute", target: "OTHER_USER", method: "COORDINATES", coordinateTargeting: coords(STARS, "EXCLUDE"),
      range: 0, cooldown: 1, actionCostPerc: 100,
      effects: [fx.damage(P.commandPower, "cc_command_absolute"), { ...fx.stun(P.commandStunAp, P.commandStunRounds), appearAnimation: "dt_control" }, fx.seal(P.commandSealRounds)],
      description: "The crown's sigil stamps down. Every chain locks around whoever stands outside the stars.",
      battleDescription: "\"Kneel.\"",
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
  const recs: Record<string, any> = { ...allCapturedRecords() };
  recs[ID.extermination] = { ...jutsuRecord(ID.extermination, {}), ...J(ID.extermination), id: ID.extermination };
  recs[ID.lastDirective] = editedLastDirective();
  for (const r of buildBespoke(P)) recs[r.id] = r;
  Object.assign(recs, buildLibrary(P.lib));
  return recs;
};

const PLAYER = "CLOSEST_OPPONENT";
export const ccRules = (P: CCParams) => [
  R.moveTo(P.throne),
  // Blasts: the marker left by last turn's mark.
  R.jutsu(LIB.blastScatterB, "SELF", [C.has(MARKER.scatterB)]),
  R.jutsu(LIB.blastScatterA, "SELF", [C.has(MARKER.scatterA)]),
  R.jutsu(ID.command, "SELF", [C.has(MARKER.lastLightBinding)]),
  R.jutsu(ID.crownfall, "SELF", [C.has(MARKER.lines)]),
  // Phase 3 (under 30%): the Last Directive; Purging Stance (Final Stand does not floor DoT ticks); Shardstorm
  // marks (A then B by their cooldown); Extermination Order on the blast turns' 60 AP.
  R.jutsu(ID.lastDirective, "SELF", [C.hb(30)]),
  R.jutsu(ID.purging, "SELF", [C.hb(30), C.has("afterburn")]),
  R.jutsu(ID.purging, "SELF", [C.hb(30), C.has("poison")]),
  R.jutsu(LIB.omenScatterA, "SELF", [C.hb(30)]),
  R.jutsu(LIB.omenScatterB, "SELF", [C.hb(30)]),
  ...(P.phase3Extermination ? [R.jutsu(ID.extermination, PLAYER, [C.hb(30), C.near(5)])] : []),
  R.end([C.hb(30)]),
  // Phase 2 (60-30%)
  R.jutsu(LIB.omenLastLightBinding, "SELF", [C.hb(60)]),
  R.jutsu(ID.recall, P.recallTarget, [C.hb(60), C.noSummon()]),
  R.jutsu(ID.stolenForm, PLAYER, [C.hb(60), C.tHas("increasedamagegiven", 50), C.near(4)]),
  R.jutsu(ID.extermination, PLAYER, [C.hb(60), C.near(5)]),
  R.jutsu(ID.scorchingRend, PLAYER, [C.hb(60), C.near(5)]),
  R.jutsu(ID.devouringGrasp, PLAYER, [C.hb(60), C.near(5)]),
  R.item(ID.countermand, PLAYER, [C.hb(60), C.near(5)]),
  R.end([C.hb(60)]),
  // Phase 1 (100-60%): the duelist.
  R.jutsu(ID.crownsWill, "SELF", [C.round(2)]),
  R.jutsu(ID.veilstep, "SELF", [C.round(5), C.far(7)]),
  R.item(ID.countermand, PLAYER, [C.has("stealth"), C.near(5)]),
  R.jutsu(ID.purging, "SELF", [C.has("afterburn")]),
  R.jutsu(ID.windSpear, PLAYER, [C.tHas("shield", 1), C.near(5)]),
  R.jutsu(LIB.omenLines, "SELF", []),
  R.jutsu(ID.hexweave, PLAYER, [C.near(4)]),
  R.jutsu(ID.finalCommand, PLAYER, [C.near(4)]),
  R.jutsu(ID.keelbind, PLAYER, [C.near(5)]),
  R.jutsu(ID.ruinRefrain, PLAYER, [C.near(5)]),
  R.jutsu(ID.scorchingRend, PLAYER, [C.near(5)]),
  R.jutsu(ID.devouringGrasp, PLAYER, [C.near(5)]),
  R.item(ID.solarBow, PLAYER, [C.near(5)]),
  R.end(),
];
export const CC_LIBRARY_USED = [LIB.omenLines, LIB.omenLastLightBinding, LIB.omenScatterA, LIB.omenScatterB, LIB.blastScatterA, LIB.blastScatterB];
export const ccKit = () => [
  ID.crownsWill, ID.stolenForm, ID.purging, ID.veilstep, ID.windSpear, ID.hexweave, ID.extermination, ID.scorchingRend,
  ID.devouringGrasp, ID.lastDirective, ID.finalCommand, ID.keelbind, ID.ruinRefrain, ID.crownfall, ID.command, ID.recall,
  ...CC_LIBRARY_USED,
];
export const ccAiRecord = (P: CCParams) => ({
  ...IN.boss.data, username: "The Crowned Captain", poolsMultiplier: P.poolsMultiplier, statsMultiplier: P.statsMultiplier,
  ...Object.fromEntries(STATS.map((s) => [s, Math.round(STAT_PER_MULT * P.statsMultiplier * 100) / 100])),
  jutsus: ccKit(), effects: [...IN.boss.data.effects, ...idgRowTags(P.idgRows)], includeDefaultRules: false, rules: ccRules(P),
});
export const CC_SETS = {
  [LIB.omenLines]: ["crownfall", "mark"], [ID.crownfall]: ["crownfall", "land"],
  [LIB.omenLastLightBinding]: ["command", "mark"], [ID.command]: ["command", "land"],
  [LIB.omenScatterA]: ["shardstorm", "mark"], [LIB.omenScatterB]: ["shardstorm", "mark"],
  [LIB.blastScatterA]: ["shardstorm", "land"], [LIB.blastScatterB]: ["shardstorm", "land"],
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
  const lib = buildLibrary(P.lib);
  for (const id of CC_LIBRARY_USED) v.jutsu(lib[id]);
  v.jutsu(editedLastDirective());
  for (const r of ccRules(P)) v.rule(r);
  const rec = ccAiRecord(P);
  v.ai(BOSS_ID, { ...rec, items: IN.boss.data.items });
  return v.issues;
};
export const ccSpec = (P: CCParams, issues: string[]) => {
  const lib = buildLibrary(P.lib);
  return {
    _note: "The Crowned Captain build spec (Crownhold D5.BOSS). Generated by harness/skyglass_wreck_sim/engine/crowned_captain.ts --write-spec; offline engine-tested, not pushed. Placeholder ids: cc-* (his bespoke records) and lib-* (the shared set-piece library, SKYGLASS_BOSS_FIGHTS.md 5a; built here under the library names until harness/skyglass_wreck_sim/library_spec.json lands, then replace by its records/ids). Law 17: literal ids in the AI's jutsus and rules.",
    params: P,
    ai: { id: BOSS_ID, srcId: IN.boss.srcId, record: ccAiRecord(P) },
    bespokeJutsu: buildBespoke(P),
    libraryJutsu: CC_LIBRARY_USED.map((id) => lib[id]),
    editedJutsu: { [ID.lastDirective]: { note: "existing push/271 record: cosmetic edit only (battleDescription carries the design's line and Shardstorm's image; finalstand row animations)", battleDescription: editedLastDirective().battleDescription, effects: editedLastDirective().effects } },
    setPieces: {
      Crownfall: { mark: LIB.omenLines, blast: ID.crownfall, note: "CASTER offsets authored for an odd column (the throne is (9,4))" },
      "Command Absolute": { mark: LIB.omenLastLightBinding, blast: ID.command, note: "stars (7,1) (5,4) (8,8)" },
      Shardstorm: { marks: [LIB.omenScatterA, LIB.omenScatterB], blasts: [LIB.blastScatterA, LIB.blastScatterB], note: "two patterns, a third of the hall each (hex 3-colour classes 0 and 1); colour-2 hexes are never hit by Scatter" },
    },
    kitRemoved: { Braced_Strike: "WvLCyGsPCKSDYl6-e_D9o", Surging_Overflow: "AicYoMMpZmHAykb_5hYtY", Rapid_Fire_live_Shuriken_Storm: "Nrxc8m9utE9qaD_gWpLgf", Worldbreaker_Chorus_live_Great_Bell_Toll: "LisNuMJ2gncEByAxG6QPI", Apex_Hunger_live_Onis_Hunger: `${ID.oniHunger} (replaced by its Crownhold-only copy The Crown's Will)` },
    kitAdded: { "Final Command": ID.finalCommand, Keelbind: ID.keelbind, "Ruin Refrain": ID.ruinRefrain },
    recallEcho: { id: ECHO_ID, name: IN.echo.data.username, source: IN.echo.source },
    arena: { grid: SIZE, orientation: "FLAT, odd columns offset (getBattleGrid)", throne: P.throne, stars: STARS },
    animations: {
      cc_crownfall: ID.crownfall, cc_command_absolute: ID.command, cc_recall: ID.recall, cc_crown_aura: ID.crownsWill,
      cc_last_directive: ID.lastDirective, cc_phase_shift: `${ID.lastDirective} (30%); the 60% flourish rode on his own Command Absolute mark, which is now the shared Omen: Last Light, Binding`,
      tg_heavy: [LIB.omenLines, LIB.omenScatterA, LIB.omenScatterB], tg_control: LIB.omenLastLightBinding, tg_safe: LIB.omenLastLightBinding,
      dt_heavy: [LIB.blastScatterA, LIB.blastScatterB], dt_control: `${ID.command} (stun row)`,
      cc_shardstorm: "unused: Shardstorm now lands through the shared scatter blast (dt_heavy)",
    },
    validation: issues.length ? issues : "valid",
  };
};

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
