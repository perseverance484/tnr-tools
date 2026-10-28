/**
 * Crownhold's division commanders (SKYGLASS_BOSS_FIGHTS.md section 7) and the isolated-pyramid chain.
 *
 *   D2.BOSS Crown Armsmaster  -GKFYAZUg1eF-3VnZhDjx  Racks Fall (Omen: Scatter A/B + shared scatter blast);
 *                                                    later Whirlwind (Omen: Ring + shared ring blast). No window.
 *   D3.BOSS Replicant Zero    vjEFUJ9mb1zNTuQf4lfXv  Jar Seals (Omen: Seal Lines + shared violet blast); Split Image
 *                                                    clones on the lines with him. No window.
 *   D4.BOSS The Second        ZsfRoyJ55Zsay5bHNLMPv  Order of Battle (Omen: Rows A/B, then Sovereign Undertow pulls,
 *                                                    then the shared rows blast); under 30% once: Lowered Guard.
 * Each keeps its push/272 kit and rules; the library pieces are added. No new jutsu of their own.
 *
 *   TNR_SCRIPT=crownhold.ts run.sh [--params /abs/p.json] [--solo 40] [--chain 30] [--policies clean,alert,healing,war]
 *        [--out results.json] [--write-spec /abs/crownhold_spec.json] [--trace D2|D3|D4:SEED]
 *
 * --solo N: each commander solo, full pools, N seeds, dodging on and off.
 * --chain N: the whole pyramid (D2..D5 regulars and bosses, then the Crowned Captain) for each route policy, pools
 *   carried between fights as the fraction of the effective maximum (no regeneration between fights assumed),
 *   dodging on. Route per division: clean = 3 regulars, puzzle solved, boss; alert = 3 regulars, puzzle failed,
 *   boss with Alarm Raised (+10% damage taken, 2r); healing = 4 regulars, Healing Rite (enter full); war = 4
 *   regulars, War Rite (the division's buff). Quest data: push/273 (archive/spent-manifests/push-2026-10-28).
 */
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { loadJson } from "./model";
import {
  allCapturedRecords, args, buildLibrary, C, crownholdRow, dmg, type Fight, type FightConfig, IN, idgRowTags, LIB, LIB_DEFAULTS, type LibParams,
  MARKER, median, opt, quantile, R, r1, runFight, SIZE, STAT_PER_MULT, STATS, summarise, validator, type PlayerStart,
} from "./cclib";
import { ccFightConfig, ccParams, ccSpec, ccValidate, CC_DEFAULTS } from "./crowned_captain";

/* ------------------------------------------------------------------ parameters */
export const CMD_DEFAULTS = {
  name: "ramp",
  lib: { ...LIB_DEFAULTS } as LibParams, // shared with the Crowned Captain
  D2: { poolsMultiplier: 2.5, idgRows: 0 },
  D3: { poolsMultiplier: 3, idgRows: 0 },
  D4: { poolsMultiplier: 3, idgRows: 0 },
  cc: {} as Record<string, unknown>, // Crowned Captain overrides (chain); default = crowned_captain.ts CC_DEFAULTS
};
type CmdParams = typeof CMD_DEFAULTS;
const loadParams = (): CmdParams => {
  const o = opt("params") ? loadJson(resolve(opt("params")!)) : {};
  return { ...CMD_DEFAULTS, ...o, lib: { ...CMD_DEFAULTS.lib, ...(o.lib ?? {}) }, D2: { ...CMD_DEFAULTS.D2, ...(o.D2 ?? {}) },
    D3: { ...CMD_DEFAULTS.D3, ...(o.D3 ?? {}) }, D4: { ...CMD_DEFAULTS.D4, ...(o.D4 ?? {}) } };
};

const K = { // live ids used in the added rules
  splitImage: "LQ26G2ANWkbTRL7Ry__F0", undertow: "nOYLPmN3TXj6wEe_oE6HQ",
};
const PLAYER = "CLOSEST_OPPONENT";
type Commander = {
  slot: "D2" | "D3" | "D4"; flavour: string; library: string[]; sets: FightConfig["sets"]; setNames: string[];
  special: Record<string, string>; rules: (base: any[]) => any[];
};
export const COMMANDERS: Commander[] = [
  {
    slot: "D2", flavour: "\"Every weapon the Project ever tested. Mind your footing.\"",
    library: [LIB.omenScatterA, LIB.omenScatterB, LIB.blastScatterA, LIB.blastScatterB, LIB.omenRing, LIB.blastRing],
    sets: { [LIB.omenScatterA]: ["racksFall", "mark"], [LIB.omenScatterB]: ["racksFall", "mark"], [LIB.blastScatterA]: ["racksFall", "land"], [LIB.blastScatterB]: ["racksFall", "land"], [LIB.omenRing]: ["whirlwind", "mark"], [LIB.blastRing]: ["whirlwind", "land"] },
    setNames: ["racksFall", "whirlwind"], special: {},
    // Blasts first (before he moves); Racks Fall after his set-up and heavy moves; Whirlwind under 50% when the player hugs him.
    rules: (b) => [
      R.jutsu(LIB.blastRing, "SELF", [C.has(MARKER.ring)]),
      R.jutsu(LIB.blastScatterB, "SELF", [C.has(MARKER.scatterB)]),
      R.jutsu(LIB.blastScatterA, "SELF", [C.has(MARKER.scatterA)]),
      ...b.slice(0, 2),
      R.jutsu(LIB.omenRing, "SELF", [C.hb(50), C.near(2)]),
      ...b.slice(2, 7),
      R.jutsu(LIB.omenScatterA, "SELF", []),
      R.jutsu(LIB.omenScatterB, "SELF", []),
      ...b.slice(7),
    ],
  },
  {
    slot: "D3", flavour: "\"I would like a copy.\"",
    library: [LIB.omenSealLines, LIB.blastSealLines],
    sets: { [LIB.omenSealLines]: ["jarSeals", "mark"], [LIB.blastSealLines]: ["jarSeals", "land"] },
    setNames: ["jarSeals"], special: { splitImage: K.splitImage },
    // Jar Seals right after his openers; Split Image on cooldown after it, so the clones stand with him on the lines.
    rules: (b) => [
      R.jutsu(LIB.blastSealLines, "SELF", [C.has(MARKER.sealLines)]),
      ...b.slice(0, 3),
      R.jutsu(LIB.omenSealLines, "SELF", []),
      R.jutsu(K.splitImage, "EMPTY_GROUND_CLOSEST_TO_SELF", []),
      ...b.slice(3),
    ],
  },
  {
    slot: "D4", flavour: "\"I questioned his orders for thirty years.\" (the line belongs on the window; Lowered Guard is shared with a neutral line)",
    library: [LIB.omenRowsA, LIB.omenRowsB, LIB.blastRowsA, LIB.blastRowsB, LIB.loweredGuard],
    sets: { [LIB.omenRowsA]: ["orderOfBattle", "mark"], [LIB.omenRowsB]: ["orderOfBattle", "mark"], [LIB.blastRowsA]: ["orderOfBattle", "land"], [LIB.blastRowsB]: ["orderOfBattle", "land"] },
    setNames: ["orderOfBattle"], special: { undertow: K.undertow, loweredGuard: LIB.loweredGuard },
    // Next turn: Sovereign Undertow (60 AP) drags the player, then the rows blast (40 AP) fires. Window under 30%, once.
    rules: (b) => [
      R.jutsu(K.undertow, PLAYER, [C.has(MARKER.rowsA), C.near(5)]),
      R.jutsu(K.undertow, PLAYER, [C.has(MARKER.rowsB), C.near(5)]),
      R.jutsu(LIB.blastRowsB, "SELF", [C.has(MARKER.rowsB)]),
      R.jutsu(LIB.blastRowsA, "SELF", [C.has(MARKER.rowsA)]),
      R.jutsu(LIB.loweredGuard, "SELF", [C.hb(30)]),
      ...b.slice(0, 2),
      R.jutsu(LIB.omenRowsA, "SELF", []),
      R.jutsu(LIB.omenRowsB, "SELF", []),
      ...b.slice(2),
    ],
  },
];

const cmdRecord = (c: Commander, P: CmdParams) => {
  const a = IN.ais[`${c.slot}.BOSS`];
  const p = P[c.slot];
  const d = a.data;
  return {
    ...d, username: a.liveUsername, poolsMultiplier: p.poolsMultiplier,
    ...((p as any).statsMultiplier !== undefined ? { statsMultiplier: (p as any).statsMultiplier, ...Object.fromEntries(STATS.map((s) => [s, Math.round(STAT_PER_MULT * (p as any).statsMultiplier * 100) / 100])) } : {}),
    jutsus: [...d.jutsus, ...c.library], effects: [...d.effects, ...idgRowTags(p.idgRows)], rules: c.rules(d.rules),
  };
};
const records = (P: CmdParams) => ({ ...allCapturedRecords(), ...buildLibrary(P.lib) });
export const cmdFightConfig = (c: Commander, P: CmdParams): FightConfig => {
  const recs = records(P);
  const rec = cmdRecord(c, P);
  const row = crownholdRow(`${c.slot}.BOSS`, recs, { data: rec, rules: rec.rules, effects: rec.effects });
  return { bossId: IN.ais[`${c.slot}.BOSS`].id, rows: { [row.userId]: row }, recs, sets: c.sets, setNames: c.setNames, phases: [60, 30], special: c.special };
};
const regFightConfig = (slot: string, P: CmdParams): FightConfig => {
  const recs = records(P);
  const row = crownholdRow(slot, recs);
  return { bossId: row.userId, rows: { [row.userId]: row }, recs, sets: {}, setNames: [], phases: [50] };
};

/* ------------------------------------------------------------------ the pyramid route */
const WAR: Record<string, any[]> = { // push/273 War Rite starting effects per division
  D2: [{ type: "stunprevent", power: 100, rounds: 2, target: "INHERIT", direction: "offence", calculation: "percentage", powerPerLevel: 0, description: "War Rite", appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "" }],
  D3: [{ type: "increasedamagegiven", power: 25, rounds: 3, target: "INHERIT", direction: "offence", calculation: "percentage", powerPerLevel: 0, description: "War Rite", appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "" }],
  D4: [{ type: "sealprevent", power: 100, rounds: 2, target: "INHERIT", direction: "offence", calculation: "static", powerPerLevel: 0, description: "War Rite", appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "" }],
  D5: [{ type: "debuffprevent", power: 100, rounds: 3, target: "INHERIT", direction: "offence", calculation: "static", powerPerLevel: 0, description: "War Rite", appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "" }],
};
const ALARM = [{ type: "increasedamagetaken", power: 10, rounds: 2, target: "INHERIT", direction: "offence", calculation: "percentage", powerPerLevel: 0, description: "Alarm Raised", appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "" }];
type Policy = "clean" | "alert" | "healing" | "war";
const runChain = async (P: CmdParams, policy: Policy, seed: number) => {
  const bosses: Record<string, FightConfig> = Object.fromEntries(COMMANDERS.map((c) => [c.slot, cmdFightConfig(c, P)]));
  bosses.D5 = ccFightConfig(ccParams(P.cc));
  const out: any = { seed, policy, fights: [] as any[], reached: "D2", outcome: "won" };
  let pools = { hp: 1, cp: 1, sp: 1 };
  let s = seed * 100;
  for (const div of ["D2", "D3", "D4", "D5"]) {
    const regs = policy === "healing" || policy === "war" ? [1, 2, 3, 4] : [1, 2, 3];
    for (const r of regs) {
      const f = await runFight(regFightConfig(`${div}.REG${r}`, P), s++, true, { hpFrac: pools.hp, cpFrac: pools.cp, spFrac: pools.sp });
      out.fights.push({ fight: `${div}.REG${r}`, outcome: f.outcome, rounds: f.rounds, startHp: Math.round(100 * pools.hp), endHp: f.playerHpPct });
      if (f.outcome !== "won") { out.outcome = `lost ${div}.REG${r}`; out.reached = div; return out; }
      pools = { hp: f.endHpFrac, cp: f.endCpFrac, sp: f.endSpFrac };
    }
    const start: PlayerStart = policy === "healing" ? {} : { hpFrac: pools.hp, cpFrac: pools.cp, spFrac: pools.sp };
    if (policy === "alert") start.startingEffects = ALARM;
    if (policy === "war") start.startingEffects = WAR[div];
    const f = await runFight(bosses[div]!, s++, true, start);
    out.fights.push({ fight: `${div}.BOSS`, outcome: f.outcome, rounds: f.rounds, startHp: policy === "healing" ? 100 : Math.round(100 * pools.hp), endHp: f.playerHpPct });
    out.reached = div;
    if (f.outcome !== "won") { out.outcome = `lost ${div}.BOSS`; return out; }
    pools = { hp: f.endHpFrac, cp: f.endCpFrac, sp: f.endSpFrac };
  }
  return out;
};
const summariseChains = (chains: any[]) => {
  const n = chains.length;
  const stage = (name: string) => {
    const at = chains.map((c) => c.fights.find((f: any) => f.fight === name)).filter(Boolean);
    return { reachedPct: r1((100 * at.length) / n), winPctOfReached: at.length ? r1((100 * at.filter((f: any) => f.outcome === "won").length) / at.length) : null,
      startHpMedian: median(at.map((f: any) => f.startHp)), endHpWinMedian: median(at.filter((f: any) => f.outcome === "won").map((f: any) => f.endHp)),
      roundsMedian: median(at.map((f: any) => f.rounds)) };
  };
  const losses: Record<string, number> = {};
  for (const c of chains) if (c.outcome !== "won") losses[c.outcome.replace("lost ", "")] = (losses[c.outcome.replace("lost ", "")] ?? 0) + 1;
  return { chains: n, clearPct: r1((100 * chains.filter((c) => c.outcome === "won").length) / n), lossesAt: losses,
    bosses: Object.fromEntries(["D2.BOSS", "D3.BOSS", "D4.BOSS", "D5.BOSS"].map((b) => [b, stage(b)])) };
};

/* ------------------------------------------------------------------ spec */
const cmdSpec = (P: CmdParams, issues: string[]) => {
  const lib = buildLibrary(P.lib);
  return {
    _note: "Crownhold bosses build spec: the shared set-piece library pieces used in Crownhold, the three division commanders (section 7), and a pointer to the Crowned Captain (crowned_captain_spec.json). Generated by engine/crownhold.ts --write-spec; offline engine-tested, not pushed. lib-* are placeholder ids for the library (built here under the library names until harness/skyglass_wreck_sim/library_spec.json lands). Commanders add no jutsu of their own: their AI records gain library ids and rules only.",
    params: P,
    library: {
      note: "Marks: 100 AP, cooldown = the set piece's cadence floor (Omen 3, Last Light 6), a 1-round tg_* visual, one 1-round primed marker type each (none on SHARED_COOLDOWN_TAGS). Shared blasts: damage only on ground (the violet Seal Lines blast targets units, OTHER_USER, for its stun/seal), 40 AP, cooldown 1, neutral line, dt_heavy / dt_control. Lowered Guard: weakness x3 on SELF, 1 round, cooldown 99, 40 AP.",
      markerTypes: MARKER,
      jutsu: Object.values(lib),
    },
    commanders: Object.fromEntries(COMMANDERS.map((c) => {
      const a = IN.ais[`${c.slot}.BOSS`];
      const rec = cmdRecord(c, P);
      return [`${c.slot}.BOSS`, { id: a.id, liveUsername: a.liveUsername, flavour: c.flavour, libraryAdded: c.library, setPieces: c.setNames, record: rec,
        changedFromPush272: { poolsMultiplier: [a.data.poolsMultiplier, rec.poolsMultiplier], addedEffects: idgRowTags(P[c.slot].idgRows), addedJutsu: c.library, rulesNow: rec.rules.length, rulesBefore: a.data.rules.length } }];
    })),
    crownedCaptain: "crowned_captain_spec.json",
    validation: issues.length ? issues : "valid",
  };
};

/* ------------------------------------------------------------------ main */
const main = async () => {
  const P = loadParams();
  const v = validator();
  const lib = buildLibrary(P.lib);
  for (const j of Object.values(lib)) v.jutsu(j);
  for (const c of COMMANDERS) {
    const rec = cmdRecord(c, P);
    for (const r of rec.rules) v.rule(r);
    v.ai(IN.ais[`${c.slot}.BOSS`].id, rec);
  }
  const issues = [...v.issues, ...ccValidate(ccParams(P.cc))];
  console.log(issues.length ? `SPEC VALIDATION ISSUES:\n  ${issues.join("\n  ")}` : "spec valid against JutsuValidator / AiRule / insertAiSchema");
  const specPath = opt("write-spec");
  if (specPath) {
    mkdirSync(dirname(resolve(specPath)), { recursive: true });
    writeFileSync(resolve(specPath), `${JSON.stringify(cmdSpec(P, issues), null, 1)}\n`);
    console.log(`wrote ${specPath}`);
  }
  const results: any = { generatedBy: "engine/crownhold.ts", params: P, ccParams: ccParams(P.cc), dmgConfig: dmg.name, grid: SIZE, solo: {}, chain: {} };
  const tr = opt("trace");
  if (tr) {
    const [slot, sd] = tr.split(":");
    const c = COMMANDERS.find((x) => x.slot === slot)!;
    for (const dodge of [true, false]) {
      const f = await runFight(cmdFightConfig(c, P), Number(sd), dodge, {}, true, args.includes("--debugfx"));
      console.log(`--- ${slot} seed ${sd} dodge ${dodge}: ${f.outcome} in ${f.rounds}, player ${f.playerHpPct}%, boss ${f.bossHpPct}%`);
      for (const l of f.trace!) console.log("  " + l);
    }
  }
  const solo = Number(opt("solo", "0"));
  if (solo > 0) for (const c of COMMANDERS) {
    const cfg = cmdFightConfig(c, P);
    results.solo[c.slot] = {};
    for (const dodge of [true, false]) {
      const fs: Fight[] = [];
      for (let i = 0; i < solo; i++) fs.push(await runFight(cfg, 1 + i, dodge));
      const s = summarise(fs, cfg.setNames);
      results.solo[c.slot][dodge ? "dodge_on" : "dodge_off"] = { summary: s, fights: fs };
      console.log(`== ${c.slot} ${IN.ais[`${c.slot}.BOSS`].liveUsername} dodge ${dodge ? "ON " : "OFF"}: ${JSON.stringify(s)}`);
    }
  }
  const chain = Number(opt("chain", "0"));
  if (chain > 0) for (const policy of opt("policies", "clean,alert,healing,war")!.split(",") as Policy[]) {
    const cs = [];
    for (let i = 0; i < chain; i++) cs.push(await runChain(P, policy, 1 + i));
    const s = summariseChains(cs);
    results.chain[policy] = { summary: s, chains: cs };
    console.log(`== chain ${policy}: ${JSON.stringify(s)}`);
  }
  const outPath = opt("out");
  if (outPath) {
    mkdirSync(dirname(resolve(outPath)), { recursive: true });
    writeFileSync(resolve(outPath), `${JSON.stringify(results, null, 1)}\n`);
    console.log(`wrote ${outPath}`);
  }
};
if (import.meta.main) await main();
