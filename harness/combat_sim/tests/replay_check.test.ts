/**
 * Regression tests for the replay's exactness predicate (review item 1): each known false positive must be judged
 * not exact. The baseline is the logged Isonade battle replayed against itself, which must be judged exact.
 *
 *   bun test harness/combat_sim/tests/replay_check.test.ts     (pure: no engine, no network)
 */
import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { judgeSeed, logToEntries } from "../engine/replay_check";

const H = join(import.meta.dir, "..");
const sc = JSON.parse(readFileSync(join(H, "scenarios/isonade_replay.json"), "utf8"));
const raw = JSON.parse(readFileSync(join(H, `data/live/2026-11-18/battles/${sc.battleId}.entries.json`), "utf8")).data;
const log = logToEntries(raw);
const PLAYER = sc.playerUserId as string;
const NAME = sc.player.name as string;

// A run whose steps reproduce the log exactly (AI ids renamed, as the sim's are).
const rename = (id: string) => (id === PLAYER ? id : `sim-${id.slice(-6)}`);
const exactRun = () => ({
  rounds: sc.expected.round as number,
  participants: { [NAME]: { outcome: sc.expected.outcome as string, settledRound: sc.expected.round as number } },
  steps: log.map((e) => ({
    round: e.round, wave: 0, actor: "", aiId: "", userId: rename(e.userId), human: e.userId === PLAYER, actionId: e.actionId,
    action: null, at: null, description: e.description, texts: [...e.effects], actionTexts: [...e.effects], hp: {},
  })) as any[],
});
const opts = { playerUserId: PLAYER, playerName: NAME, expected: sc.expected, unconsumed: 0, unforcedIdles: 0 };
const judge = (run: any, o: Partial<typeof opts> = {}) => judgeSeed(log, run, { ...opts, ...o });
const firstAi = (run: any, pred: (s: any) => boolean = () => true) => run.steps.findIndex((s: any) => !s.human && pred(s));
const dmg = /takes [\d.]+ (?:[a-z]+ )?damage/;

describe("replay exactness predicate", () => {
  test("the log against itself is exact", () => {
    const v = judge(exactRun());
    expect(v.mismatches).toBe(0);
    expect(v.exact).toBe(true);
  });

  test("altered damage (one cent) is not exact", () => {
    const run = exactRun();
    const i = firstAi(run, (s) => s.texts.some((t: string) => dmg.test(t)));
    expect(i).toBeGreaterThanOrEqual(0);
    const k = run.steps[i].texts.findIndex((t: string) => dmg.test(t));
    run.steps[i].texts[k] = run.steps[i].texts[k].replace(/takes ([\d.]+)/, (_: string, n: string) => `takes ${(Number(n) + 0.01).toFixed(2)}`);
    const v = judge(run);
    expect(v.exact).toBe(false);
    expect(v.firstDivergence?.index).toBe(i);
  });

  test("a deleted AI damage line is not exact", () => {
    const run = exactRun();
    const i = firstAi(run, (s) => s.texts.some((t: string) => dmg.test(t)));
    run.steps[i].texts = run.steps[i].texts.filter((t: string) => !dmg.test(t));
    expect(judge(run).exact).toBe(false);
  });

  test("an extra AI action is not exact", () => {
    const run = exactRun();
    const i = firstAi(run);
    run.steps.splice(i + 1, 0, { ...run.steps[i], texts: [...run.steps[i].texts] });
    expect(judge(run).exact).toBe(false);
  });

  test("a missing player wait is not exact", () => {
    const run = exactRun();
    const i = run.steps.findIndex((s: any) => s.human && s.actionId === "wait");
    expect(i).toBeGreaterThanOrEqual(0);
    run.steps.splice(i, 1);
    expect(judge(run).exact).toBe(false);
  });

  test("a trailing extra entry is not exact", () => {
    const run = exactRun();
    run.steps.push({ ...run.steps.at(-1) });
    expect(judge(run).historyEntries.sim).toBe(log.length + 1);
    expect(judge(run).exact).toBe(false);
  });

  test("a round-99 loss with an identical history is not exact", () => {
    const run = exactRun();
    run.rounds = 99;
    run.participants[NAME] = { outcome: "Lost", settledRound: 99 };
    const v = judge(run);
    expect(v.checks.historyIdentical).toBe(true);
    expect(v.exact).toBe(false);
  });

  test("the right history with the wrong outcome or round is not exact", () => {
    const a = exactRun();
    a.participants[NAME]!.outcome = "Draw";
    expect(judge(a).exact).toBe(false);
    const b = exactRun();
    b.rounds = sc.expected.round + 1;
    expect(judge(b).exact).toBe(false);
  });

  test("swapped actors are not exact", () => {
    const run = exactRun();
    const ai = [...new Set(run.steps.filter((s: any) => !s.human).map((s: any) => s.userId))];
    expect(ai.length).toBeGreaterThanOrEqual(2);
    const i = run.steps.findIndex((s: any) => s.userId === ai[1]);
    run.steps[i].userId = ai[0];
    expect(judge(run).exact).toBe(false);
  });

  test("unconsumed player actions, refused actions or unforced idle turns are not exact", () => {
    expect(judge(exactRun(), { unconsumed: 1 }).exact).toBe(false);
    expect(judge(exactRun(), { unforcedIdles: 1 }).exact).toBe(false);
    const run = exactRun();
    run.steps[0].issue = "refused";
    expect(judge(run).exact).toBe(false);
  });
});
