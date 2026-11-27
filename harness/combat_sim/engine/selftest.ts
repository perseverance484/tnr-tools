/** Smoke + determinism check: one genin floor twice with the same seed must give identical step logs. */
import { join } from "node:path";
import { enemyRow, loadLibrary, playerRow } from "./model";
import { randomIntDraws } from "./entropy";
import { assemble, runFight, seedRun } from "./sim";

const lib = loadLibrary([join(process.env.TNR_HARNESS!, "data/live/2026-11-18")]);
const S = "pz4azy5M6ZYJiwURtKZjp";
const rows = Object.fromEntries(Object.keys(lib.ai).map((id) => [id, enemyRow(lib, id)]));
const once = async (seed: number) => {
  seedRun(seed);
  const p = playerRow(lib, { name: "Genin", level: 15, rank: "GENIN", elements: ["Lightning"], jutsu: [
    { id: "EOMOSOVn3za-UddIC2hY9", level: 8 }, { id: "xHZPm6r4dq9YhpsohKmtl", level: 8 }, { id: "clh4d6q1j0008tb0hzthddb6m", level: 8 }, { id: "9HwIfXZzkgenkpywlEuET", level: 8 },
  ] }, 0, lib.ai[S]);
  const b = await assemble({ players: [p], enemyRows: rows, waves: [{ aiIds: [S], delayRounds: 0 }], mode: "dungeon", runtime: lib.runtime });
  return runFight(b, { maxRounds: 40, policy: { dodge: true } });
};
const a = await once(7), b = await once(7), c = await once(8);
const sig = (r: any) => JSON.stringify([r.opening, r.steps.map((s: any) => [s.round, s.actor, s.actionId, s.description, s.texts, s.hp])]);
const ok = {
  fightRan: a.steps.length > 0 && a.outcome !== "stalled",
  sameSeedIdentical: sig(a) === sig(b),
  otherSeedDiffers: sig(a) !== sig(c),
  noForcedActionIssues: !a.steps.some((s) => s.issue),
  settledByEngine: Object.keys(a.participants).length === 1,
  spawnsFromSeededSource: randomIntDraws() >= 6, // two fighters per run, three runs: the router drew through entropy.ts
};
console.log(JSON.stringify({ outcome: a.outcome, settlement: a.participants, rounds: a.rounds, steps: a.steps.length, opening: a.opening, ...ok }));
if (!Object.values(ok).every(Boolean)) process.exit(1);
