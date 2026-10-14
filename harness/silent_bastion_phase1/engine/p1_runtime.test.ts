/**
 * Gate R — native runtime proof on the real routers and a throwaway local MySQL.
 * Each plan starts from a fresh world (lib/driver.resetWorld) and runs one attempt.
 */
import { beforeEach, expect, it, vi } from "bun:test";
import { Pusher } from "@/libs/pusher";
import { describeWithDatabase } from "../setup/testDatabase";
import { resetWorld } from "./lib/driver";
import { Evidence, requireClean } from "./lib/report";
import { type Plan, type Point, type Route, Runner, type Seg } from "./lib/scenario";

const ev = new Evidence("r_runtime");
const ROUTES: Route[] = ["clean", "alert", "medical", "combat"];
const rot = (i: number) => ROUTES[((i % 4) + 4) % 4]!;
const win = (route: Route, wrong?: Seg["wrong"]): Seg => ({ route, ...(wrong ? { wrong } : {}) });

const plans: Plan[] = [];
// S1–S4: all-success attempts; every division sees every route once across the four, both wrong answers used.
for (let j = 0; j < 4; j++)
  plans.push({ name: `S${j + 1} success`, expect: "complete",
    divisions: [1, 2, 3, 4, 5].map((d) => [win(rot(j + d), (j + d) % 2 ? "wrong_b" : "wrong_a")]) });
// L1–L9: an initial-lane loss at the same point in every division, then the retry lane.
const lossPoints: { at: Point; route: Route | "rot" }[] = [
  { at: "f1", route: "rot" }, { at: "f2", route: "rot" }, { at: "f3", route: "rot" },
  { at: "f4", route: "medical" }, { at: "f4", route: "combat" },
  { at: "boss", route: "clean" }, { at: "boss", route: "alert" }, { at: "boss", route: "medical" }, { at: "boss", route: "combat" },
];
const retryPatterns: Seg[][] = [
  [{ route: "clean", lossAt: "f1" }, { route: "medical", lossAt: "f1" }],              // two consecutive retry-entry losses
  [{ route: "medical", lossAt: "boss" }],                                               // Medical boss lost, then a different route
  [{ route: "combat", lossAt: "f4" }, { route: "alert", lossAt: "boss" }],              // two different later retry losses
  [{ route: "alert", lossAt: "f3" }],
  [], [], [], [], [],
];
lossPoints.forEach((lp, k) => {
  plans.push({ name: `L${k + 1} initial loss at ${lp.at}${lp.route === "rot" ? "" : `/${lp.route}`}`,
    expect: lp.at === "boss" ? "fail" : "complete",
    divisions: [1, 2, 3, 4, 5].map((d) => [
      { route: lp.route === "rot" ? rot(d + k) : lp.route, lossAt: lp.at },
      // Commander losses on the retry lane in Division V would be Arakane (hard fail): covered by A1–A2.
      ...(d < 5 ? retryPatterns[k]! : retryPatterns[k]!.filter((x) => x.lossAt !== "boss")),
      win(rot(d + k + 1), "wrong_b"),
    ]) });
});
// A1–A2: Arakane defeat on the retry lane.
for (const route of ["medical", "clean"] as Route[])
  plans.push({ name: `A retry-lane Arakane loss (${route})`, expect: "fail",
    divisions: [[win("clean")], [win("alert")], [win("medical")], [win("combat")],
      [{ route: "combat", lossAt: "f1" }, { route, lossAt: "boss" }]] });
// X1: five consecutive retry losses in Division I, every loss point, then completion.
plans.push({ name: "X1 five consecutive retry losses", expect: "complete",
  divisions: [[{ route: "clean", lossAt: "f2" }, { route: "clean", lossAt: "f1" }, { route: "alert", lossAt: "f2" },
    { route: "medical", lossAt: "f3" }, { route: "medical", lossAt: "f4" }, { route: "combat", lossAt: "boss" }, win("clean")],
    [win("clean")], [win("clean")], [win("clean")], [win("clean")]] });

describeWithDatabase("R: native runtime progression", () => {
  beforeEach(() => { vi.spyOn(Pusher.prototype, "trigger").mockResolvedValue(undefined); });
  const summary: unknown[] = [];
  for (const plan of plans) {
    it(plan.name, async () => {
      await resetWorld();
      const t0 = performance.now();
      const r = new Runner(ev, plan);
      const outcome = await r.run();
      ev.timing(`${plan.name}.ms`, performance.now() - t0);
      ev.check(`${plan.name}: outcome ${plan.expect}`, outcome === plan.expect, outcome);
      summary.push({ plan: plan.name, outcome, battles: r.battles, trace: r.trace });
      ev.put("runs", summary);
      expect(outcome).toBe(plan.expect);
    }, 600_000);
  }
  it("coverage across all attempts", () => {
    type T = { battle: string; carriedHpPct: number; startPct: { h: number }; outcome?: string };
    const all = (summary as { trace: T[] }[]).flatMap((r) => r.trace);
    const med = all.filter((t) => /boss\.medical$/.test(t.battle));
    const lowered = med.filter((t) => t.carriedHpPct > 75 && !/\.r\./.test(t.battle)).length;
    const raised = med.filter((t) => t.carriedHpPct < 75).length;
    ev.check("Medical 75% observed lowering a higher carried pool and raising a lower one", lowered > 0 && raised > 0, { lowered, raised, total: med.length });
    const cov: Record<string, number> = {};
    for (const t of all) { const k = t.battle.replace(/^b\d/, "b*"); cov[k] = (cov[k] ?? 0) + 1; }
    const kinds = ["f1", "f2", "f3", "f4.medical", "f4.combat", "boss.clean", "boss.alert", "boss.medical", "boss.combat"];
    const missing = ["n", "r"].flatMap((l) => kinds.map((k) => `b*.${l}.${k}`)).filter((k) => !cov[k]);
    ev.check("every battle kind fought on both lanes", missing.length === 0, missing);
    const lostAt = new Set(all.filter((t) => t.outcome === "Lost").map((t) => t.battle));
    const notLost = [1, 2, 3, 4, 5].flatMap((d) => kinds.map((k) => `b${d}.n.${k}`)).filter((b) => !lostAt.has(b));
    ev.check("an initial-lane loss exercised at all 45 initial-lane battles", notLost.length === 0, notLost);
    ev.put("battleKindCoverage", cov);
    ev.put("totals", { attempts: summary.length, battles: all.length, losses: all.filter((t) => t.outcome === "Lost").length,
      retryEntries50: all.filter((t) => /\.r\.f1$/.test(t.battle)).length });
  });
  requireClean(ev);
});
