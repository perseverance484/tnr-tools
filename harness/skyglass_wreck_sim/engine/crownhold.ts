/**
 * Crownhold's division commanders (SKYGLASS_BOSS_FIGHTS.md section 7) and the isolated-pyramid chain.
 *
 *   D2.BOSS Crown Armsmaster  -GKFYAZUg1eF-3VnZhDjx  Racks Fall (Omen: Scatter A/B + shared scatter blast);
 *                                                    later Whirlwind (Omen: Ring + shared ring blast). No window.
 *   D3.BOSS Replicant Zero    vjEFUJ9mb1zNTuQf4lfXv  Jar Seals (Omen: Seal Lines + shared violet blast), from round 6;
 *                                                    the design's clones-on-the-lines is not buildable (report L5). No window.
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
import { auditEnemy, unmarkedReport } from "./fallback";
import { assertSpecRuleCap, overCapReport } from "./rulecap";
import { gateReport } from "./gates";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { loadJson } from "./model";
import {
  afterMark, allCapturedRecords, args, buildLibraryRecords, C, crownholdRow, dmg, type Fight, type FightConfig, IN, idgRowTags, LIB,
  LIB_POWERS, MARKER_TYPES as M, median, opt, PET_ON, R, r1, runFight, SIZE, STAT_PER_MULT, STATS, summarise, validator, type PlayerStart,
} from "./cclib";
import { ccFightConfig, ccParams, ccValidate } from "./crowned_captain";

/* ------------------------------------------------------------------ parameters */
export const CMD_DEFAULTS = {
  name: "chain_tuned", // RUL-2026-10-28-013: tuned for the pyramid chain (pools carried), not standalone
  // alarmStrike: a kit jutsu cast first while the player carries Alarm Raised (rounds 1-2), "he was expecting you";
  // alarmTarget SELF for a guard-up buff. opening (D2 only): Sovereign Fetters then Racks Fall in round 1, the
  // combination the War Rite's stun immunity answers.
  // (Tested and not shipped: alarm strikes made the alert route cheaper, because they delay each boss's real threat.)
  D2: { poolsMultiplier: 1.25, idgRows: -0.5, alarmStrike: null as string | null, alarmTarget: "CLOSEST_OPPONENT", opening: true }, // push/272: 2.5, no rows
  D3: { poolsMultiplier: 1.25, idgRows: -0.9, alarmStrike: null as string | null, alarmTarget: "CLOSEST_OPPONENT", opening: false }, // push/272: 3, no rows
  D4: { poolsMultiplier: 2, idgRows: -0.15, alarmStrike: null as string | null, alarmTarget: "CLOSEST_OPPONENT", opening: false }, // push/272: 3, no rows
  cc: {} as Record<string, unknown>, // Crowned Captain overrides; default = crowned_captain.ts CC_DEFAULTS (chain-tuned)
  /** Regular overrides. D3.REG1 Crown Archivist is shared with the hunts harness, which tuned it (pools 2, 2 damage
   * rows, coordinator 2026-10-28); Crownhold takes those stats as fixed input and does not retune it. */
  regs: { "D3.REG1": { poolsMultiplier: 2, idgRows: 2 } } as Record<string, { poolsMultiplier?: number; idgRows?: number }>,
  /** Route quest effects (push/273 values by default): Alarm Raised on the player, and the War Rite per division. */
  quest: {
    alarm: { type: "increasedamagetaken", power: 10, rounds: 2 },
    war: {
      D2: { type: "stunprevent", power: 100, rounds: 2, calculation: "percentage" },
      D3: { type: "increasedamagegiven", power: 25, rounds: 3, calculation: "percentage" },
      D4: { type: "sealprevent", power: 100, rounds: 2, calculation: "static" },
      D5: { type: "debuffprevent", power: 100, rounds: 3, calculation: "static" },
    } as Record<string, { type: string; power: number; rounds: number; calculation: string }>,
    /** Proposal knob (not push/273): extra War Rite rows added in every division. */
    warExtra: [] as { type: string; power: number; rounds: number; calculation?: string }[],
    /**
     * RUL-2026-10-28-026 item 1: the Crowned Captain fight opens with a route heal (applyBuffs heal, percentage of max
     * HP), added to the carried HP and capped at max; it never lowers it. Healing Rite: full. War Rite: +20% and the
     * division's War Rite buff for the whole fight. Chakra and stamina still carry. `null` = the pre-ruling chain.
     */
    ccTopUp: { healing: 100, clean: 35, war: 20, alert: 15, warWholeFight: true } as null | { healing: number; clean: number; war: number; alert: number; warWholeFight: boolean },
    /**
     * RUL-2026-10-30-060 item 3: the War route also gets its +20% heal top-up at D4 and D5. Modelled as a heal of that
     * % of max HP on entering the division (before its regulars, where the final pass lost its War runs), added to the
     * carried HP and capped at max; the Crowned Captain's own top-up (ccTopUp.war) still applies. `null` = final pass.
     */
    warDivTopUp: null as null | Record<string, number>,
  },
};
type CmdParams = typeof CMD_DEFAULTS;
const loadParams = (): CmdParams => {
  const o = opt("params") ? loadJson(resolve(opt("params")!)) : {};
  return { ...CMD_DEFAULTS, ...o, D2: { ...CMD_DEFAULTS.D2, ...(o.D2 ?? {}) },
    D3: { ...CMD_DEFAULTS.D3, ...(o.D3 ?? {}) }, D4: { ...CMD_DEFAULTS.D4, ...(o.D4 ?? {}) }, regs: { ...CMD_DEFAULTS.regs, ...(o.regs ?? {}) },
    quest: { alarm: { ...CMD_DEFAULTS.quest.alarm, ...(o.quest?.alarm ?? {}) }, warExtra: o.quest?.warExtra ?? [],
      ccTopUp: o.quest?.ccTopUp === null ? null : { ...CMD_DEFAULTS.quest.ccTopUp!, ...(o.quest?.ccTopUp ?? {}) },
      warDivTopUp: o.quest?.warDivTopUp ?? null,
      war: Object.fromEntries(Object.entries(CMD_DEFAULTS.quest.war).map(([d, w]) => [d, { ...w, ...(o.quest?.war?.[d] ?? {}) }])) } };
};

/** The chain/table player reads each new telegraph with this probability (--read, default 1 = every one). */
const READ = Number(opt("read", "1"));
const K = { // live ids used in the added rules
  splitImage: "LQ26G2ANWkbTRL7Ry__F0", undertow: "nOYLPmN3TXj6wEe_oE6HQ",
};
const PLAYER = "CLOSEST_OPPONENT";
const FETTERS_ID = (IN.ais["D2.BOSS"].data.jutsus as string[]).find((id) => (IN.jutsu[id]?.record ?? IN.oldKit[id]?.record)?.name === "Sovereign Fetters")!;
type Commander = {
  slot: "D2" | "D3" | "D4"; flavour: string; library: string[]; sets: FightConfig["sets"]; setNames: string[];
  special: Record<string, string>; rules: (base: any[], p: any) => any[];
};
const J2 = { backlashPalm: "ElSK-RCrLjddEUm76FZrs", shurikenStorm: "Nrxc8m9utE9qaD_gWpLgf", fetters: FETTERS_ID };
const J3 = { devouringWave: "-45phqE2baTGC--lNSEx9", mirrorEdge: "AEeRf7i9215twJ_iEugZT" };
const J4 = { piercingJudgment: "OyswJoalfNpmz7FsA8Hd8", explosiveTag: "o-4SCAhJ4LHdCwcBDgJrV" };
export const COMMANDERS: Commander[] = [
  {
    slot: "D2", flavour: "\"Every weapon the Project ever tested. Mind your footing.\"",
    library: [LIB.mark.scatterA, LIB.mark.scatterB, LIB.blast.scatterA, LIB.blast.scatterB, LIB.mark.ring, LIB.blast.ring],
    sets: { [LIB.mark.scatterA]: ["racksFall", "mark"], [LIB.mark.scatterB]: ["racksFall", "mark"], [LIB.blast.scatterA]: ["racksFall", "land"], [LIB.blast.scatterB]: ["racksFall", "land"], [LIB.mark.ring]: ["whirlwind", "mark"], [LIB.blast.ring]: ["whirlwind", "land"] },
    setNames: ["racksFall", "whirlwind"], special: {},
    // Racks Fall (Scatter) after his set-up and heavy moves; Whirlwind (Ring) under 50% when the player hugs him.
    rules: (b, p) => [
      R.jutsu(LIB.blast.ring, "SELF", [C.has(M.ring)]),
      R.jutsu(LIB.blast.scatterB, "SELF", [C.has(M.scatterB)]),
      R.jutsu(LIB.blast.scatterA, "SELF", [C.has(M.scatterA)]),
      ...(["ring", "scatterA", "scatterB"] as const).flatMap((k) => afterMark(k, [R.jutsu(J2.backlashPalm, PLAYER, [C.near(5)]), R.jutsu(J2.shurikenStorm, PLAYER, [C.near(5)])])),
      // Opening (round 1): Sovereign Fetters (60 AP), then Racks Fall's mark (40 AP) on the stunned player.
      ...(p.opening ? [R.jutsu(J2.fetters, PLAYER, [C.round(2), C.near(6)]), R.jutsu(LIB.mark.scatterA, "SELF", [C.round(2)])] : []),
      ...b.slice(0, 2),
      R.jutsu(LIB.mark.ring, "SELF", [C.hb(50), C.near(2)]),
      ...b.slice(2, 7),
      R.jutsu(LIB.mark.scatterA, "SELF", []),
      R.jutsu(LIB.mark.scatterB, "SELF", []),
      ...b.slice(7),
    ],
  },
  {
    slot: "D3", flavour: "\"I would like a copy.\"",
    library: [LIB.mark.sealLines, LIB.blast.sealLines],
    sets: { [LIB.mark.sealLines]: ["jarSeals", "mark"], [LIB.blast.sealLines]: ["jarSeals", "land"] },
    setNames: ["jarSeals"], special: { splitImage: K.splitImage },
    // Jar Seals after his openers.
    rules: (b, p) => [
      R.jutsu(LIB.blast.sealLines, "SELF", [C.has(M.sealLines)]),
      // No Split Image here: a clone runs his rules, lays its own Seal Lines and blasts them; when he stands in its
      // cross, the blast's elementalseal lands on him, which is his own Seal Lines marker type, and he then blasts
      // every turn without a mark (library defect, see the report). His live round-2 Split Image stays.
      ...afterMark("sealLines", [R.jutsu(J3.devouringWave, PLAYER, [C.near(5)]), R.jutsu(J3.mirrorEdge, PLAYER, [C.near(5)])]),
      ...b.slice(0, 3),
      // From round 6: his round-2 Split Image (3 rounds) is gone, so no clone can blast him into a loop.
      R.jutsu(LIB.mark.sealLines, "SELF", [{ type: "round_greater_than", value: 5, description: "Current round is greater than specified value" }]),
      ...b.slice(3),
    ],
  },
  {
    slot: "D4", flavour: "\"I questioned his orders for thirty years.\" (belongs on the window; the shared Lowered Guard carries a neutral line)",
    library: [LIB.mark.rowsA, LIB.mark.rowsB, LIB.blast.rowsA, LIB.blast.rowsB, LIB.loweredGuard],
    sets: { [LIB.mark.rowsA]: ["orderOfBattle", "mark"], [LIB.mark.rowsB]: ["orderOfBattle", "mark"], [LIB.blast.rowsA]: ["orderOfBattle", "land"], [LIB.blast.rowsB]: ["orderOfBattle", "land"] },
    setNames: ["orderOfBattle"], special: { undertow: K.undertow, loweredGuard: LIB.loweredGuard },
    // Order of Battle: the Rows mark (40 AP), then his live Sovereign Undertow (60 AP) drags the player in the same turn;
    // the rows blast fires next turn. Under 30%, once: Lowered Guard.
    rules: (b, p) => [
      R.jutsu(LIB.blast.rowsB, "SELF", [C.has(M.rowsB)]),
      R.jutsu(LIB.blast.rowsA, "SELF", [C.has(M.rowsA)]),
      ...(["rowsA", "rowsB"] as const).flatMap((k) => afterMark(k, [R.jutsu(K.undertow, PLAYER, [C.near(5)]), R.jutsu(J4.piercingJudgment, PLAYER, [C.near(5)]), R.jutsu(J4.explosiveTag, PLAYER, [C.near(5)])])),
      R.jutsu(LIB.loweredGuard, "SELF", [C.hb(30)]),
      ...b.slice(0, 2),
      R.jutsu(LIB.mark.rowsA, "SELF", []),
      R.jutsu(LIB.mark.rowsB, "SELF", []),
      ...b.slice(2),
    ],
  },
];

/** The alarm strike goes right after the blast rules (a blast owed to a mark still fires first). */
export const ALARM_CONDS = [C.tHas("increasedamagetaken", 10), C.round(3)];
const withAlarmStrike = (rules: any[], jutsuId: string | null, target = PLAYER) => {
  if (!jutsuId) return rules;
  const firstNonBlast = rules.findIndex((r) => !(r.conditions?.[0]?.type === "has_effect" && String(r.action?.jutsuId ?? "").startsWith("lib-blast")));
  return [...rules.slice(0, firstNonBlast), R.jutsu(jutsuId, target, target === "SELF" ? ALARM_CONDS : [...ALARM_CONDS, C.near(6)]), ...rules.slice(firstNonBlast)];
};
const cmdRecord = (c: Commander, P: CmdParams) => {
  const a = IN.ais[`${c.slot}.BOSS`];
  const p = P[c.slot];
  const d = a.data;
  return {
    ...d, username: a.liveUsername, poolsMultiplier: p.poolsMultiplier,
    ...((p as any).statsMultiplier !== undefined ? { statsMultiplier: (p as any).statsMultiplier, ...Object.fromEntries(STATS.map((s) => [s, Math.round(STAT_PER_MULT * (p as any).statsMultiplier * 100) / 100])) } : {}),
    jutsus: [...d.jutsus, ...c.library], effects: [...d.effects, ...idgRowTags(p.idgRows)], rules: withAlarmStrike(c.rules(d.rules, p), p.alarmStrike, p.alarmTarget),
  };
};
const records = (_P: CmdParams) => ({ ...allCapturedRecords(), ...buildLibraryRecords() });
export const cmdFightConfig = (c: Commander, P: CmdParams): FightConfig => {
  const recs = records(P);
  const rec = cmdRecord(c, P);
  const row = crownholdRow(`${c.slot}.BOSS`, recs, { data: rec, rules: rec.rules, effects: rec.effects });
  return { bossId: IN.ais[`${c.slot}.BOSS`].id, rows: { [row.userId]: row }, recs, sets: c.sets, setNames: c.setNames, phases: [60, 30], special: c.special };
};
const regFightConfig = (slot: string, P: CmdParams): FightConfig => {
  const recs = records(P);
  const o = P.regs[slot];
  const a = IN.ais[slot];
  const row = o ? crownholdRow(slot, recs, { data: { poolsMultiplier: o.poolsMultiplier ?? a.data.poolsMultiplier }, effects: [...a.data.effects, ...idgRowTags(o.idgRows ?? 0)] }) : crownholdRow(slot, recs);
  return { bossId: row.userId, rows: { [row.userId]: row }, recs, sets: {}, setNames: [], phases: [50] };
};

/* ------------------------------------------------------------------ the pyramid route */
const questTag = (t: { type: string; power: number; rounds: number; calculation?: string }, description: string) => ({
  type: t.type, power: t.power, rounds: t.rounds, target: "INHERIT", direction: "offence", calculation: t.calculation ?? "percentage",
  powerPerLevel: 0, description, appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "",
});
/** Quest starting effects for a boss fight on a route (push/273 Alarm Raised / War Rite, values from P.quest). */
const routeEffects = (P: CmdParams, variant: string, div: string) =>
  variant === "alarm" ? [questTag(P.quest.alarm, "Alarm Raised")]
    : variant === "war" && P.quest.war[div] ? [questTag(P.quest.war[div]!, "War Rite"), ...(P.quest.warExtra ?? []).map((t: any) => questTag(t, "War Rite"))]
    : undefined;
type Policy = "clean" | "alert" | "healing" | "war";
const runChain = async (P: CmdParams, policy: Policy, seed: number) => {
  const bosses: Record<string, FightConfig> = Object.fromEntries(COMMANDERS.map((c) => [c.slot, cmdFightConfig(c, P)]));
  bosses.D5 = ccFightConfig(ccParams(P.cc));
  const out: any = { seed, policy, fights: [] as any[], reached: "D2", outcome: "won" };
  let pools = { hp: 1, cp: 1, sp: 1 };
  let s = seed * 100;
  for (const div of ["D2", "D3", "D4", "D5"]) {
    const regs = policy === "healing" || policy === "war" ? [1, 2, 3, 4] : [1, 2, 3];
    const divTop = policy === "war" ? P.quest.warDivTopUp?.[div] : undefined;
    if (divTop) pools = { ...pools, hp: Math.min(1, pools.hp + divTop / 100) };
    for (const r of regs) {
      const f = await runFight(regFightConfig(`${div}.REG${r}`, P), s++, READ, { hpFrac: pools.hp, cpFrac: pools.cp, spFrac: pools.sp });
      out.fights.push({ fight: `${div}.REG${r}`, outcome: f.outcome, rounds: f.rounds, startHp: Math.round(100 * pools.hp), endHp: f.playerHpPct });
      if (f.outcome !== "won") { out.outcome = `lost ${div}.REG${r}`; out.reached = div; return out; }
      pools = { hp: f.endHpFrac, cp: f.endCpFrac, sp: f.endSpFrac };
    }
    const top = div === "D5" ? P.quest.ccTopUp : null;
    // Healing Rite: every commander and the Crowned Captain are entered full (push/273; the ruled top-up is "full").
    const carriedHp = pools.hp;
    const hpAtEntry = policy === "healing" ? 1 : top ? Math.min(1, carriedHp + (top[policy] ?? 0) / 100) : carriedHp;
    const start: PlayerStart = policy === "healing" ? {} : { hpFrac: hpAtEntry, cpFrac: pools.cp, spFrac: pools.sp };
    let fx = routeEffects(P, policy === "alert" ? "alarm" : policy, div);
    if (fx && top && policy === "war" && top.warWholeFight) fx = fx.map((e: any) => ({ ...e, rounds: 99 }));
    if (fx) start.startingEffects = fx;
    const f = await runFight(bosses[div]!, s++, READ, start);
    out.fights.push({ fight: `${div}.BOSS`, outcome: f.outcome, rounds: f.rounds, startHp: Math.round(100 * hpAtEntry), carriedHp: Math.round(100 * carriedHp), endHp: f.playerHpPct });
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
const cmdSpec = (P: CmdParams, issues: string[]) => ({
  _note: "Crownhold division commanders build spec (SKYGLASS_BOSS_FIGHTS.md section 7). Generated by engine/crownhold.ts --write-spec; offline engine-tested, not pushed. Each keeps its push/272 kit and rules and gains library records (library_spec.json, lib-* placeholder ids, referenced not copied) and rules; no new jutsu of their own. The Crowned Captain is in crowned_captain_spec.json.",
  params: P,
  librarySource: "library_spec.json (fable/skyglass-wreck-sim 5f6c3edb)", libraryPowers: LIB_POWERS, markerTypes: M,
  commanders: Object.fromEntries(COMMANDERS.map((c) => {
    const a = IN.ais[`${c.slot}.BOSS`];
    const rec = cmdRecord(c, P);
    return [`${c.slot}.BOSS`, { id: a.id, liveUsername: a.liveUsername, flavour: c.flavour, libraryAdded: c.library, setPieces: c.setNames, record: rec,
      changedFromPush272: { poolsMultiplier: [a.data.poolsMultiplier, rec.poolsMultiplier], addedEffects: idgRowTags(P[c.slot].idgRows), addedJutsu: c.library, rules: [a.data.rules.length, rec.rules.length] } }];
  })),
  crownedCaptain: "crowned_captain_spec.json",
  tunedFor: "RUL-2026-10-28-013: the pyramid chain with pools carried between fights (no refill); never fought alone",
  fixedInputs: { regulars: P.regs, note: "D3.REG1 Crown Archivist uses the hunts harness tuning (pools 2, 2 damage rows) as fixed input; Crownhold did not retune it" },
  routeQuestEffects: { ...P.quest, note: "push/273 values unless a proposal file overrides them; the shipped spec does not change quest data" },
  notUsed: { wardOfCommand: "lib-ward-of-command is not used by any Crownhold fight, so the hunts INHERIT fix does not apply here" },
  validation: issues.length ? issues : "valid",
});

/* ------------------------------------------------------------------ main */
const main = async () => {
  const P = loadParams();
  const v = validator();
  const lib = buildLibraryRecords();
  for (const c of COMMANDERS) for (const id of c.library) v.jutsu(lib[id]);
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
    const spec = cmdSpec(P, issues);
    assertSpecRuleCap("crownhold_spec", spec);
    writeFileSync(resolve(specPath), `${JSON.stringify(spec, null, 1)}\n`);
    console.log(`wrote ${specPath}`);
  }
  const auditPath = opt("audit-fallback");
  if (auditPath) {
    // RUL-2026-10-29-046 audit: every Crownhold record as the harness fights it (commanders with their library rules,
    // the Crowned Captain, all regulars at their push/272 rules).
    const rows: any[] = [];
    const add = (cfg: FightConfig) => {
      for (const r of Object.values<any>(cfg.rows)) rows.push(auditEnemy("crownhold", r.userId, r.username, r.aiProfile ?? { rules: [], includeDefaultRules: false }, r.jutsus.map((uj: any) => uj.jutsuId)));
    };
    for (const c of COMMANDERS) add(cmdFightConfig(c, P));
    add(ccFightConfig(ccParams(P.cc)));
    for (const slot of Object.keys(IN.ais)) if (!slot.endsWith("BOSS")) add(regFightConfig(slot, P));
    mkdirSync(dirname(resolve(auditPath)), { recursive: true });
    writeFileSync(resolve(auditPath), `${JSON.stringify(rows, null, 1)}\n`);
    console.log(`wrote ${auditPath}`);
    return;
  }
  const results: any = { generatedBy: "engine/crownhold.ts", params: P, ccParams: ccParams(P.cc), dmgConfig: dmg.name, grid: SIZE, player: { telegraphReadP: READ, pet: PET_ON ? "one modelled mid-rank companion (model.ts petFor)" : false }, solo: {}, chain: {} };
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
  // --table: each fight at a grid of carried start HP fractions (chakra and stamina carried at the same fraction), for
  // composing route chains offline (tools/compose_chain.py). --table D2.REG1,D2.BOSS,... or "all"; --hps 1,0.7,0.4;
  // --variants none,alarm,war (boss fights only); --shard i/n splits the work across processes.
  const table = opt("table");
  if (table) {
    const seeds = Number(opt("seeds", "8"));
    const hps = opt("hps", "1,0.8,0.6,0.4,0.25")!.split(",").map(Number);
    const variants = opt("variants", "none")!.split(",");
    const all = ["D2", "D3", "D4", "D5"].flatMap((d) => [1, 2, 3, 4].map((r) => `${d}.REG${r}`).concat(`${d}.BOSS`));
    const fights = table === "all" ? all : table.split(",");
    const [si, sn] = (opt("shard", "0/1")!).split("/").map(Number);
    const jobs: [string, number, string][] = [];
    for (const fn of fights) for (const hp of hps) for (const vr of fn.endsWith("BOSS") ? variants : ["none"]) jobs.push([fn, hp, vr]);
    results.table = [];
    let ji = 0;
    for (const [fn, hp, vr] of jobs) {
      if (ji++ % sn! !== si) continue;
      const div = fn.slice(0, 2);
      const cfg = fn === "D5.BOSS" ? ccFightConfig(ccParams(P.cc)) : fn.endsWith("BOSS") ? cmdFightConfig(COMMANDERS.find((c) => c.slot === div)!, P) : regFightConfig(fn, P);
      const start: PlayerStart = hp >= 1 ? {} : { hpFrac: hp, cpFrac: hp, spFrac: hp };
      const fx = routeEffects(P, vr, div);
      if (fx) start.startingEffects = fx;
      const fs: Fight[] = [];
      for (let i = 0; i < seeds; i++) fs.push(await runFight(cfg, 1000 + i, READ, start));
      const row = { fight: fn, hp, variant: vr, runs: fs.map((f) => ({ seed: f.seed, outcome: f.outcome, rounds: f.rounds, endHp: r1(100 * f.endHpFrac), endCp: r1(100 * f.endCpFrac), endSp: r1(100 * f.endSpFrac), phaseRounds: f.phaseRounds, petAlive: (f.petEndHpPct ?? 0) > 0, petShare: f.bossDmgTotal ? r1((100 * f.petBossDmg) / f.bossDmgTotal) : null, sets: Object.fromEntries(Object.entries(f.sets).map(([k, v]) => [k, [v.mark, v.land, v.hit]])), dmg: Object.fromEntries(Object.entries(f.dmgBySource).sort((x, y) => y[1] - x[1]).slice(0, 5).map(([k, v]) => [k, Math.round(v)])) })) };
      results.table.push(row);
      const w = fs.filter((f) => f.outcome === "won");
      console.log(`T ${fn} hp${hp} ${vr}: win ${w.length}/${fs.length} endHp ${median(w.map((f) => r1(100 * f.endHpFrac)!))} cost ${median(w.map((f) => r1(100 * ((hp >= 1 ? 1 : hp) - f.endHpFrac))!))} rounds ${median(fs.map((f) => f.rounds))} cp ${median(w.map((f) => r1(100 * f.endCpFrac)!))} sp ${median(w.map((f) => r1(100 * f.endSpFrac)!))}`);
    }
  }
  const chain = Number(opt("chain", "0"));
  if (chain > 0) for (const policy of opt("policies", "clean,alert,healing,war")!.split(",") as Policy[]) {
    const cs = [];
    for (let i = 0; i < chain; i++) {
      cs.push(await runChain(P, policy, 1 + i));
      // Checkpoint after every chain (long runs on a shared machine can be killed).
      const op = opt("out");
      if (op) {
        results.chain[policy] = { summary: summariseChains(cs), chains: cs, partial: i + 1 < chain };
        mkdirSync(dirname(resolve(op)), { recursive: true });
        writeFileSync(resolve(op), `${JSON.stringify(results, null, 1)}\n`);
      }
    }
    const s = summariseChains(cs);
    results.chain[policy] = { summary: s, chains: cs };
    console.log(`== chain ${policy}: ${JSON.stringify(s)}`);
  }
  results.fallbackGuard = unmarkedReport();
  results.ruleCap = overCapReport();
  results.gates = gateReport();
  console.log("fallback guard:", JSON.stringify(results.fallbackGuard));
  const outPath = opt("out");
  if (outPath) {
    mkdirSync(dirname(resolve(outPath)), { recursive: true });
    writeFileSync(resolve(outPath), `${JSON.stringify(results, null, 1)}\n`);
    console.log(`wrote ${outPath}`);
  }
};
if (import.meta.main) await main();
