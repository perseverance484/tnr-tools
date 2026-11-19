/**
 * Validation replay: force a logged player's actions, in order and at the logged tiles, through the engine's human
 * action path, let the AI side act through the engine's AI, and compare the sim's battle history with the log.
 *
 *   run.sh replay.ts --scenario scenarios/isonade_replay.json [--out results/replay.json] [--expect-exact N]
 *
 * A seed is EXACT only when all of these hold (one predicate, used for the count, the gate and the example):
 *   - the sim's history has exactly as many entries as the log, and entry k matches log entry k on round, actor,
 *     actionId, description text and the complete ordered list of applied-effect lines (HTML stripped);
 *   - actors match one-to-one: each logged userId maps to one sim userId and back (the player's id is the logged id);
 *   - every damage line ("X takes N ... damage") pairs one-to-one with the log at integer-cent precision;
 *   - every logged player action was consumed, none was refused, and no player turn timed out unforced;
 *   - the sim ends with the scenario's expected outcome (calcBattleResult) in the expected round.
 * --expect-exact N exits 1 unless at least N seeds are exact (a minimum, not a claim about the exact count).
 */
import { writeFileSync } from "node:fs";
import { isAbsolute, join } from "node:path";
import { enemyRow, loadJson, loadLibrary, playerRow, type PlayerSpec } from "./model";
import { judgeSeed, logToEntries, plain } from "./replay_check";
import { assemble, parseTile, runFight, seedRun, type Forced } from "./sim";

const arg = (k: string) => {
  const i = process.argv.indexOf(k);
  return i > 0 ? process.argv[i + 1] : undefined;
};
const sc = loadJson(arg("--scenario")!);
const H = process.env.TNR_HARNESS!;
const lib = loadLibrary(sc.library.map((d: string) => (isAbsolute(d) ? d : join(H, d))));
const log = [...lib.battles[sc.battleId]!].sort((a, b) => a.battleVersion - b.battleVersion);
if (!sc.expected?.outcome || !sc.expected?.round) throw new Error("scenario needs expected.outcome and expected.round (the logged result)");
const tileOf = (e: any) => plain(e.description).match(/ on ([A-Z]\d+)/)?.[1] ?? null;
const logEntries = logToEntries(log);

// Logged player actions, in order.
const playerLog = log.filter((e) => e.userId === sc.playerUserId).map((e) => {
  const at = tileOf(e);
  if (!at) throw new Error(`no tile in log line ${e.battleVersion}`);
  return { round: e.battleRound as number, actionId: e.actionId as string, at };
});

const spec = sc.player as PlayerSpec;
const rows = Object.fromEntries(Object.keys(lib.ai).map((id) => [id, enemyRow(lib, id)]));
const perSeed: any[] = [];
const runsBySeed: any[] = [];
for (let seed = 1; seed <= (sc.seeds ?? 10); seed++) {
  seedRun(seed);
  const p = playerRow(lib, spec, 0, lib.ai[sc.enemies[0]], sc.playerUserId); // logged id, so log lines match
  const queue = [...playerLog];
  const battle = await assemble({
    players: [p], enemyRows: rows, waves: [{ aiIds: sc.enemies, delayRounds: 0 }], mode: sc.mode, runtime: lib.runtime,
    placements: sc.placements.map(parseTile), barriers: false, manualPlayers: true,
  });
  let unforcedIdles = 0;
  const driver = (b: any): Forced => {
    const next = queue[0];
    if (next && next.round === b.round) {
      queue.shift();
      return { actionId: next.actionId, ...parseTile(next.at) };
    }
    unforcedIdles++; // the log has no player action for this turn
    return "idle";
  };
  const run = runFight(battle, { maxRounds: sc.maxRounds ?? 30, driver });
  const verdict = judgeSeed(logEntries, run, {
    playerUserId: sc.playerUserId, playerName: spec.name, expected: sc.expected, unconsumed: queue.length, unforcedIdles,
  });
  perSeed.push({ seed, opening: run.opening, initiativeOrder: Object.keys(run.opening), ...verdict });
  runsBySeed.push(run);
}

const allPairs = perSeed.length;
const summary = {
  battleId: sc.battleId,
  enginePin: process.env.TNR_ENGINE_PIN,
  seeds: allPairs,
  expected: sc.expected,
  exactSeeds: perSeed.filter((p) => p.exact).length,
  exactSeedList: perSeed.filter((p) => p.exact).map((p) => p.seed),
  predicate: "history identical entry by entry (round, actor 1:1, actionId, description, every effect line, damage to the cent), every player action consumed and accepted, no unforced idle turn, expected settlement and round",
  settlements: Object.fromEntries([...new Set(perSeed.map((p) => String(p.settlement)))].map((o) => [o, perSeed.filter((p) => String(p.settlement) === o).length])),
  firstDivergenceFields: Object.fromEntries(
    [...new Set(perSeed.filter((p) => p.firstDivergence).map((p) => p.firstDivergence.field))].map((f) => [f, perSeed.filter((p) => p.firstDivergence?.field === f).length]),
  ),
};
console.log(JSON.stringify({ ...summary, perSeed: perSeed.map((p) => ({ seed: p.seed, exact: p.exact, mismatches: p.mismatches, first: p.firstDivergence ? `#${p.firstDivergence.index} ${p.firstDivergence.field}` : null })) }, null, 1));
const out = arg("--out");
const exampleIdx = perSeed.findIndex((p) => p.exact);
if (out)
  writeFileSync(out, JSON.stringify({
    invocation: { script: "replay.ts", args: process.argv.slice(2).map((a) => a.replace(/^.*\/harness\/combat_sim\//, "")) },
    harnessCode: process.env.TNR_HARNESS_CODE ?? null,
    summary, perSeed,
    exampleExactRun: exampleIdx >= 0 ? { seed: perSeed[exampleIdx].seed, steps: runsBySeed[exampleIdx].steps } : null,
  }, null, 1));
const need = Number(arg("--expect-exact") ?? 0);
if (summary.exactSeeds < need) {
  console.error(`replay gate: ${summary.exactSeeds} exact seeds, expected at least ${need}`);
  process.exit(1);
}
