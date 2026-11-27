/**
 * The replay's exactness predicate, kept free of engine imports so it can be unit-tested on its own
 * (tests/replay_check.test.ts). replay.ts uses judgeSeed for the count, the gate and the example run alike.
 */
import type { FightResult, Step } from "./sim";

export const plain = (s: string) => s.replace(/<[^>]+>/g, "");

/** Every "X takes N <kind> damage" line, as {who, kind, cents} (integer cents). */
export const damageLines = (texts: string[]) =>
  texts.flatMap((t) => [...plain(t).matchAll(/^(.+?) takes ([\d.]+) ((?:[a-z]+ )?damage)/g)].map((m) => ({ who: m[1]!, kind: m[3]!, cents: Math.round(Number(m[2]) * 100) })));

export type Entry = { round: number; userId: string; actionId: string; description: string; effects: string[] };

export const logToEntries = (log: any[]): Entry[] =>
  [...log].sort((a, b) => a.battleVersion - b.battleVersion).map((e) => ({
    round: e.battleRound, userId: e.userId, actionId: e.actionId, description: plain(e.description), effects: (e.appliedEffects ?? []).map((x: any) => plain(x.txt)),
  }));

/** The sim's history entries: the steps the router would have recorded. */
export const simEntries = (steps: Step[]): Entry[] =>
  steps.filter((s) => s.description !== null).map((s) => ({ round: s.round, userId: s.userId, actionId: s.actionId!, description: plain(s.description!), effects: s.texts.map(plain) }));

export type Mismatch = { index: number; field: string; log: unknown; sim: unknown };

/** Compare two histories entry by entry; every mismatch is returned (empty = identical). fixedIds pins known ids. */
export const compareHistories = (want: Entry[], got: Entry[], fixedIds: Record<string, string>): Mismatch[] => {
  const problems: Mismatch[] = [];
  const l2s = new Map(Object.entries(fixedIds));
  const s2l = new Map(Object.entries(fixedIds).map(([a, b]) => [b, a]));
  const n = Math.max(want.length, got.length);
  for (let i = 0; i < n; i++) {
    const w = want[i], g = got[i];
    if (!w || !g) {
      problems.push({ index: i, field: w ? "missing in sim" : "extra in sim", log: w ?? null, sim: g ?? null });
      continue;
    }
    if (w.round !== g.round) problems.push({ index: i, field: "round", log: w.round, sim: g.round });
    const mapped = l2s.get(w.userId), back = s2l.get(g.userId);
    if (mapped === undefined && back === undefined) {
      l2s.set(w.userId, g.userId);
      s2l.set(g.userId, w.userId);
    } else if (mapped !== g.userId || back !== w.userId) problems.push({ index: i, field: "actor", log: w.userId, sim: g.userId });
    if (w.actionId !== g.actionId) problems.push({ index: i, field: "actionId", log: w.actionId, sim: g.actionId });
    if (w.description !== g.description) problems.push({ index: i, field: "description", log: w.description, sim: g.description });
    if (JSON.stringify(w.effects) !== JSON.stringify(g.effects)) problems.push({ index: i, field: "effects", log: w.effects, sim: g.effects });
    const wd = damageLines(w.effects), gd = damageLines(g.effects);
    if (JSON.stringify(wd) !== JSON.stringify(gd)) problems.push({ index: i, field: "damage", log: wd, sim: gd });
  }
  return problems;
};

export type JudgeOpts = {
  playerUserId: string;
  playerName: string;
  expected: { outcome: string; round: number };
  /** Logged player actions the driver never used. */
  unconsumed: number;
  /** Player turns the driver had nothing logged for. */
  unforcedIdles: number;
};

/** The one exactness predicate. */
export const judgeSeed = (logEntries: Entry[], run: Pick<FightResult, "steps" | "participants" | "rounds">, o: JudgeOpts) => {
  const sim = simEntries(run.steps);
  const problems = compareHistories(logEntries, sim, { [o.playerUserId]: o.playerUserId });
  const refused = run.steps.filter((s) => s.issue).map((s) => `r${s.round} ${s.issue}`);
  const settlement = run.participants[o.playerName]?.outcome ?? null;
  const checks = {
    historyIdentical: problems.length === 0,
    allPlayerActionsConsumed: o.unconsumed === 0,
    noRefusedActions: refused.length === 0,
    noUnforcedIdleTurns: o.unforcedIdles === 0,
    outcome: settlement === o.expected.outcome,
    round: run.rounds === o.expected.round,
  };
  return {
    exact: Object.values(checks).every(Boolean),
    checks,
    settlement,
    rounds: run.rounds,
    historyEntries: { log: logEntries.length, sim: sim.length },
    mismatches: problems.length,
    firstDivergence: problems[0] ?? null,
    unconsumedPlayerActions: o.unconsumed,
    refused,
    unforcedIdles: o.unforcedIdles,
  };
};
