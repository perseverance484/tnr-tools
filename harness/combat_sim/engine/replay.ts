/**
 * Validation replay: force a logged player's actions, in order and at the logged tiles, through the engine's human
 * action path, let the AI side act through the engine's AI, and compare the result with the battle log.
 *
 *   run.sh replay.ts --scenario scenarios/isonade_replay.json [--out results/replay.json] [--expect-exact N]
 * --expect-exact N exits 1 unless at least N seeds reproduce the log exactly (a regression gate).
 */
import { writeFileSync } from "node:fs";
import { isAbsolute, join } from "node:path";
import { enemyRow, loadJson, loadLibrary, playerRow, type PlayerSpec } from "./model";
import { assemble, parseTile, runFight, seedRun, tile, type Forced } from "./sim";

const arg = (k: string) => {
  const i = process.argv.indexOf(k);
  return i > 0 ? process.argv[i + 1] : undefined;
};
const sc = loadJson(arg("--scenario")!);
const H = process.env.TNR_HARNESS!;
const lib = loadLibrary(sc.library.map((d: string) => (isAbsolute(d) ? d : join(H, d))));
const log = [...lib.battles[sc.battleId]!].sort((a, b) => a.battleVersion - b.battleVersion);
const plain = (s: string) => s.replace(/<[^>]+>/g, "");
const tileOf = (e: any) => plain(e.description).match(/ on ([A-Z]\d+)/)?.[1] ?? null;
const dmgNums = (texts: string[]) =>
  texts.flatMap((t) => [...t.matchAll(/^(.+?) takes ([\d.]+) (damage|afterburn damage|wound damage|reflect damage|recoil damage)/g)].map((m) => ({ who: m[1]!, n: Number(m[2]), kind: m[3]! })));

// Logged player actions per round, in order.
const playerLog = log.filter((e) => e.userId === sc.playerUserId);
const queue = new Map<number, { actionId: string; at: string }[]>();
for (const e of playerLog) {
  const at = tileOf(e);
  if (!at) throw new Error(`no tile in log line ${e.battleVersion}`);
  if (!queue.has(e.battleRound)) queue.set(e.battleRound, []);
  queue.get(e.battleRound)!.push({ actionId: e.actionId, at });
}
const lastRound = Math.max(...log.map((e) => e.battleRound));

const spec = sc.player as PlayerSpec;
const rows = Object.fromEntries(Object.keys(lib.ai).map((id) => [id, enemyRow(lib, id)]));
const runs: any[] = [];
for (let seed = 1; seed <= (sc.seeds ?? 10); seed++) {
  const rand = seedRun(seed);
  const p = playerRow(lib, spec, 0, lib.ai[sc.enemies[0]], sc.playerUserId); // logged id, so log lines match
  const q = new Map([...queue].map(([r, xs]) => [r, [...xs]]));
  const battle = await assemble({
    players: [p], enemyRows: rows, waves: [{ aiIds: sc.enemies, delayRounds: 0 }], mode: sc.mode, runtime: lib.runtime, rand,
    placements: sc.placements.map(parseTile), barriers: false,
  });
  const driver = (b: any, actor: any): Forced => {
    const next = q.get(b.round)?.shift();
    if (next) return { actionId: next.actionId, ...parseTile(next.at) };
    return { actionId: "wait", x: actor.longitude, y: actor.latitude };
  };
  runs.push(runFight(battle, { maxRounds: sc.maxRounds ?? 30, driver }));
}

// Compare.
const logAi = (r: number) => log.filter((e) => e.battleRound === r && e.userId !== sc.playerUserId && e.actionId !== "wait").map((e) => e.actionId);
const simAi = (run: any, r: number) => run.steps.filter((s: any) => s.round === r && !s.human && s.actionId && s.actionId !== "wait").map((s: any) => s.actionId);
const logHits = playerLog.map((e) => ({ round: e.battleRound, actionId: e.actionId, hits: dmgNums(e.appliedEffects.map((x: any) => x.txt)) }));
const perRun = runs.map((run) => {
  const forced = run.steps.filter((s: any) => s.human);
  let i = 0;
  const pairs: { round: number; actionId: string; log: number; sim: number | null }[] = [];
  for (const lh of logHits) {
    const st = forced.find((s: any, k: number) => k >= i && s.round === lh.round && s.actionId === lh.actionId);
    if (st) i = forced.indexOf(st) + 1;
    const sh = st ? dmgNums(st.texts) : [];
    for (const h of lh.hits.filter((h) => h.kind === "damage" && h.who !== "Little Horror")) {
      const m = sh.find((x) => x.who === h.who && x.kind === "damage");
      pairs.push({ round: lh.round, actionId: lh.actionId, log: h.n, sim: m ? m.n : null, who: h.who } as any);
    }
  }
  let aiMatch = 0, aiTotal = 0;
  for (let r = 1; r <= lastRound; r++) {
    const a = logAi(r), b = simAi(run, r);
    aiTotal += a.length;
    a.forEach((x, k) => (aiMatch += b[k] === x ? 1 : 0));
  }
  return { outcome: run.outcome, rounds: run.rounds, pairs, aiMatch, aiTotal, issues: run.steps.filter((s: any) => s.issue).map((s: any) => `r${s.round} ${s.issue}`) };
});
const r0 = perRun[0]!;
const ratios = perRun.flatMap((p) => p.pairs.filter((x) => x.sim !== null).map((x) => x.sim! / x.log));
const sorted = [...ratios].sort((a, b) => a - b);
const pct = (q: number) => sorted[Math.floor(q * (sorted.length - 1))];
const summary = {
  battleId: sc.battleId,
  enginePin: process.env.TNR_ENGINE_PIN,
  seeds: runs.length,
  logged: { outcome: "won", rounds: lastRound },
  outcomes: Object.fromEntries(["won", "lost", "stalled"].map((o) => [o, perRun.filter((p) => p.outcome === o).length])),
  roundsEnded: perRun.map((p) => p.rounds),
  damageRatio: { n: ratios.length, median: pct(0.5), p10: pct(0.1), p90: pct(0.9), within5pct: ratios.filter((x) => Math.abs(x - 1) <= 0.05).length / (ratios.length || 1) },
  /** Seeds where every forced action landed, every logged hit matched to 0.5% and every AI action matched in order. */
  exactSeeds: perRun.filter((p) => !p.issues.length && p.aiMatch === p.aiTotal && p.pairs.every((x) => x.sim !== null && Math.abs(x.sim / x.log - 1) <= 0.005)).length,
  seedsWithBlockedForcedActions: perRun.filter((p) => p.issues.length).length,
  aiActionsMatched: `${perRun.reduce((s, p) => s + p.aiMatch, 0)}/${perRun.reduce((s, p) => s + p.aiTotal, 0)}`,
  firstSeed: { pairs: r0.pairs, issues: r0.issues },
  firstSeedAiByRound: Array.from({ length: lastRound }, (_, k) => ({ round: k + 1, log: logAi(k + 1), sim: simAi(runs[0], k + 1) })),
  firstSeedPlayerHp: runs[0].steps.filter((s: any) => s.hp.dauntless).map((s: any) => `r${s.round} ${s.actor} ${s.action}: ${s.hp.dauntless}`),
};
console.log(JSON.stringify(summary, null, 1));
const out = arg("--out");
const exactIdx = perRun.findIndex((p) => !p.issues.length && p.aiMatch === p.aiTotal);
if (out) writeFileSync(out, JSON.stringify({ summary, exampleExactRun: exactIdx >= 0 ? { seed: exactIdx + 1, ...runs[exactIdx] } : null }, null, 1));
const need = Number(arg("--expect-exact") ?? 0);
if (summary.exactSeeds < need) {
  console.error(`replay gate: ${summary.exactSeeds} exact seeds, expected at least ${need}`);
  process.exit(1);
}
