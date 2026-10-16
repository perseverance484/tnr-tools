/**
 * Gate R — complete attempts on the real routers and a throwaway local MySQL, one fresh world per
 * plan. Every battle start, loss, recovery and reset is checked by lib/run99.ts.
 *
 * On the candidate graph, recovery_later is never LOST here: that transition is the defect C1,
 * reproduced in isolation by gate D. Everything else in the matrix runs identically on every variant.
 */
import { beforeEach, expect, it, vi } from "bun:test";
import { Pusher } from "@/libs/pusher";
import { describeWithDatabase } from "../setup/testDatabase";
import { resetWorld } from "./lib/driver";
import { Evidence, requireClean } from "./lib/report";
import { DIVS, type Plan, type Route, Runner, type Seg } from "./lib/run99";

const ev = new Evidence("r_runtime");
const CANDIDATE = (process.env.TNR_VARIANT ?? "candidate") === "candidate";
/** recovery_later losses requested by a plan (0 on the candidate; see header). */
const later = (n: number) => (CANDIDATE ? 0 : n);
const ROUTES: Route[] = ["clean", "alert", "medical", "combat"];
const rot = (i: number) => ROUTES[((i % 4) + 4) % 4]!;
const win = (route: Route, wrong?: Seg["wrong"]): Seg => ({ route, ...(wrong ? { wrong } : {}) });
const all = (f: (i: number, d: number) => Seg[]) => DIVS.map((d, i) => f(i, d));

const plans: Plan[] = [];
// S1–S4: clean victories; each division sees every route once across the four, both wrong answers used.
for (let j = 0; j < 4; j++)
  plans.push({ name: `S${j + 1} success`, expect: "complete", divisions: all((i) => [win(rot(i + j), (i + j) % 2 ? "wrong_b" : "wrong_a")]) });
// L1: REG1 loss, two consecutive recovery_first losses, recovery win, then the rest of the division.
plans.push({ name: "L1 REG1 loss + 2 recovery_first losses", expect: "complete",
  divisions: all((i) => [{ route: rot(i), lossAt: "f1", recoveryLosses: 2 }, win(rot(i + 1), "wrong_b")]) });
// L2: REG2 loss, recovery win -> reset to REG2.
plans.push({ name: "L2 REG2 loss + recovery win", expect: "complete",
  divisions: all((i) => [{ route: rot(i + 1), lossAt: "f2" }, win(rot(i + 2))]) });
// L3: REG3 loss, two consecutive recovery_later losses, then recovery win.
plans.push({ name: `L3 REG3 loss + ${later(2)} recovery_later losses`, expect: "complete",
  divisions: all((i) => [{ route: rot(i + 2), lossAt: "f3", recoveryLosses: later(2) }, win(rot(i + 3), "wrong_b")]) });
// L4: REG4 loss on the Medical route, recovery, then Combat.
plans.push({ name: "L4 REG4 loss + recovery", expect: "complete",
  divisions: all(() => [{ route: "medical", lossAt: "f4", recoveryLosses: later(1) }, win("combat")]) });
// B*: commander loss on each route in Divisions I–III (D2–D4), recovery, a different route wins; Arakane won.
for (const route of ROUTES)
  plans.push({ name: `B commander loss (${route})`, expect: "complete",
    divisions: [...[2, 3, 4].map((_, i) => [{ route, lossAt: "boss" as const, wrong: (i % 2 ? "wrong_b" : "wrong_a") as Seg["wrong"] }, win(route === "medical" ? "combat" : "medical")]), [win(route)]] });
// A*: Arakane defeat on each route hard-fails; one after a Division IV recovery.
for (const route of ROUTES)
  plans.push({ name: `A Arakane loss (${route})`, expect: "fail",
    divisions: [[win("clean")], [win("alert")], [win("medical")],
      route === "combat" ? [{ route: "clean", lossAt: "f2", recoveryLosses: later(1) }, { route, lossAt: "boss" }] : [{ route, lossAt: "boss" }]] });
// M1: repeated failures in one division, mixing both templates and every later loss point; Medical lost then Combat.
plans.push({ name: "M1 repeated failures", expect: "complete",
  divisions: [
    [{ route: "clean", lossAt: "f1", recoveryLosses: 1 }, { route: "alert", lossAt: "f3", recoveryLosses: later(1) },
      { route: "medical", lossAt: "boss" }, { route: "combat", lossAt: "f2", recoveryLosses: later(2) }, { route: "combat", lossAt: "f4" }, win("combat")],
    [win("clean")],
    [{ route: "medical", lossAt: "f4" }, { route: "alert", lossAt: "boss", wrong: "wrong_b" }, { route: "clean", lossAt: "boss" }, win("medical")],
    [{ route: "combat", lossAt: "f1" }, { route: "alert", lossAt: "f2", recoveryLosses: later(1) }, win("alert", "wrong_b")],
  ] });
// M2: recovery_first win then a later loss in the same division (cross-template), every division.
plans.push({ name: "M2 recovery_first then later loss", expect: "complete",
  divisions: all((i, d) => [{ route: rot(i), lossAt: "f1" }, { route: rot(i + 1), lossAt: i % 2 && d !== 5 ? "boss" : "f3", recoveryLosses: later(1) }, win(rot(i + 3), "wrong_b")]) });

describeWithDatabase("R: native runtime progression", () => {
  beforeEach(() => { vi.spyOn(Pusher.prototype, "trigger").mockResolvedValue(undefined); });
  const summary: { plan: string; outcome: string; battles: number; trace: Record<string, unknown>[] }[] = [];
  for (const plan of plans) {
    it(plan.name, async () => {
      await resetWorld();
      const t0 = performance.now();
      const r = new Runner(ev, plan);
      const outcome = await r.run();
      ev.timing(`${plan.name}.ms`, performance.now() - t0);
      ev.check(`${plan.name}: outcome ${plan.expect}`, outcome === plan.expect, outcome);
      if (plan.name.startsWith("S")) ev.check(`${plan.name}: 16-20 battles on a clean victory`, r.battles >= 16 && r.battles <= 20, r.battles);
      summary.push({ plan: plan.name, outcome, battles: r.battles, trace: r.trace });
      ev.put("runs", summary);
      expect(outcome).toBe(plan.expect);
    }, 600_000);
  }
  it("coverage across all attempts", () => {
    type T = { battle: string; carriedHpPct: number; startPct: { h: number }; outcome?: string };
    const t = summary.flatMap((r) => r.trace as T[]);
    const med = t.filter((x) => /boss\.medical$/.test(x.battle));
    ev.check("Medical: every Medical commander starts at 100%, including from a depleted carry", med.length > 0 && med.some((x) => x.carriedHpPct < 100) && med.every((x) => x.startPct.h === 100), { total: med.length });
    const rec = t.filter((x) => /recovery_/.test(x.battle));
    ev.check("every recovery fight starts at exactly 50%", rec.length > 0 && rec.every((x) => x.startPct.h === 50), { total: rec.length });
    const kinds = ["f1", "f2", "f3", "f4", "boss.clean", "boss.alert", "boss.medical", "boss.combat"];
    const lost = new Set(t.filter((x) => x.outcome === "Lost").map((x) => x.battle));
    const notLost = DIVS.flatMap((d) => kinds.map((k) => `b${d}.n.${k}`)).filter((b) => !lost.has(b));
    ev.check("a loss exercised at all 32 normal-lane battles (each REG and each commander variant, four divisions)", notLost.length === 0, notLost);
    const recWon = DIVS.flatMap((d) => [`b${d}.recovery_first`, `b${d}.recovery_later`]).filter((b) => !t.some((x) => x.battle === b && x.outcome === "Won"));
    ev.check("both recovery fights won in every division", recWon.length === 0, recWon);
    const recLost = DIVS.flatMap((d) => [`b${d}.recovery_first`, ...(CANDIDATE ? [] : [`b${d}.recovery_later`])]).filter((b) => !t.some((x) => x.battle === b && x.outcome === "Lost"));
    ev.check(CANDIDATE ? "recovery_first lost in every division (recovery_later loss: gate D)" : "both recovery fights lost in every division", recLost.length === 0, recLost);
    ev.put("totals", { attempts: summary.length, battles: t.length, losses: t.filter((x) => x.outcome === "Lost").length, recoveryStarts50: rec.length,
      cleanRunBattles: summary.filter((r) => r.plan.startsWith("S")).map((r) => r.battles) });
  });
  requireClean(ev);
});
