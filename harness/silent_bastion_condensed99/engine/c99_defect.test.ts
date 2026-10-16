/**
 * Gate D — the recovery_later reset timing, isolated per division (minimal reproduction).
 *
 * Each case completes the earlier divisions cleanly, loses one later battle of division N, then
 * starts the 50% recovery fight and LOSES it. The brief requires: the fight is the active
 * objective while it runs; the loss rewinds (reset_later_loss) to dN.lost_later; the next fight is
 * the recovery fight again at 50%. On the candidate the WIN-edge reset fires at battle start
 * instead (finding C1); on a remediation option it must not.
 */
import { beforeEach, expect, it, vi } from "bun:test";
import { Pusher } from "@/libs/pusher";
import { describeWithDatabase } from "../setup/testDatabase";
import { api, choose, currentBattle, engineView, hero, refresh, resetWorld, settle, tracker, HERO } from "./lib/driver";
import { QUEST_ID } from "./lib/graph";
import { Evidence, requireClean } from "./lib/report";
import { type Point, type Route, Runner } from "./lib/run99";

const ev = new Evidence("d_defect");
const VARIANT = process.env.TNR_VARIANT ?? "candidate";
const CANDIDATE = VARIANT === "candidate";
const cases: { d: number; route: Route; lossAt: Point }[] = [
  { d: 2, route: "clean", lossAt: "f2" },
  { d: 3, route: "combat", lossAt: "f4" },
  { d: 4, route: "alert", lossAt: "boss" },
  { d: 5, route: "medical", lossAt: "f3" },
];

describeWithDatabase("D: recovery_later reset timing", () => {
  beforeEach(() => { vi.spyOn(Pusher.prototype, "trigger").mockResolvedValue(undefined); });
  const observed: Record<string, unknown> = {};
  let reproduced = 0;
  for (const k of cases) {
    it(`D${k.d}: loss at ${k.lossAt}/${k.route}, then the recovery fight is lost`, async () => {
      await resetWorld();
      const r = new Runner(ev, { name: `D${k.d}`, divisions: [], expect: "fail" });
      await r.start();
      for (let d = 2; d < k.d; d++) await r.division(d, [{ route: "clean" }]);
      const stop = await r.pass(k.d, `d${k.d}.n.f1`, { route: k.route, lossAt: k.lossAt, stopAfterLoss: true });
      ev.check(`D${k.d}: the later loss reached d${k.d}.lost_later`, stop === "stopped" && (await engineView()).active === `d${k.d}.lost_later`);
      const rec = `b${k.d}.recovery_later`;
      const started = await choose(rec);
      const snap = await currentBattle();
      const t = await tracker();
      const during = {
        battle: snap?.extraState.questBattleSource?.objectiveId ?? null,
        startHpPct: snap ? (snap.usersState.find((u) => u.userId === HERO)!.curHealth / snap.usersState.find((u) => u.userId === HERO)!.maxHealth) * 100 : null,
        logbookActiveObjective: (await engineView()).active,
        recoveryGoalInTracker: !!t?.goals.find((g) => g.id === rec),
        lostLaterGoalInTracker: !!t?.goals.find((g) => g.id === `d${k.d}.lost_later`),
      };
      await settle(false, { health: 0, chakra: 100, stamina: 100 });
      await refresh();
      await refresh();
      const h = await hero();
      const afterLoss = { logbookActiveObjective: (await engineView()).active, open: (await engineView()).open, hp: h?.curHealth };
      // What the next accepted step starts.
      const next = afterLoss.logbookActiveObjective!;
      const res = await choose(next === `d${k.d}.lost_later` ? rec : `b${k.d}.n.f2`);
      const nb = await currentBattle();
      const p = nb?.usersState.find((u) => u.userId === HERO);
      const nextFight = { accepted: res.success, battle: nb?.extraState.questBattleSource?.objectiveId ?? null, startHp: p?.curHealth ?? null, startHpPct: p ? (p.curHealth / p.maxHealth) * 100 : null };
      const retry = await (await api()).quests.retryBattle({ questId: QUEST_ID });
      observed[`D${k.d}`] = { started: started.success, during, afterLoss, nextFight, retryOffered: retry.success };
      ev.put("observed", observed);

      ev.check(`D${k.d}: the recovery fight started at 50%`, during.battle === rec && during.startHpPct === 50, during);
      const bug = !during.recoveryGoalInTracker && during.logbookActiveObjective === `d${k.d}.n.f2` &&
        afterLoss.logbookActiveObjective === `d${k.d}.n.f2` && afterLoss.hp === 1 && nextFight.battle === `b${k.d}.n.f2` && nextFight.startHp === 1;
      if (bug) reproduced++;
      if (CANDIDATE) {
        ev.check(`D${k.d} [candidate]: C1 reproduced — reset fired at battle start, recovery loss continues to b${k.d}.n.f2 at 1 HP`, bug, { during, afterLoss, nextFight });
      } else {
        ev.check(`D${k.d}: recovery fight is the active objective while it runs`, during.logbookActiveObjective === rec && during.recoveryGoalInTracker, during);
        ev.check(`D${k.d}: recovery loss rewinds to d${k.d}.lost_later (reset_later_loss)`, afterLoss.logbookActiveObjective === `d${k.d}.lost_later` && afterLoss.open.length === 1, afterLoss);
        ev.check(`D${k.d}: next fight is the recovery fight again at 50%`, nextFight.battle === rec && nextFight.startHpPct === 50, nextFight);
      }
      ev.check(`D${k.d}: no in-place Retry Battle`, !retry.success);
      expect(true).toBe(true);
    }, 300_000);
  }
  it("finding C1", () => {
    ev.finding("C1", "recovery_later WIN edge -> reset_quest is pre-selected when the recovery fight starts: the reset to dN.n.f2 fires at battle start, the recovery outcome no longer matters, a recovery LOSS continues to REG2 at 1 HP, and reset_later_loss is unreachable",
      reproduced > 0, { divisionsReproduced: reproduced, of: cases.length, variant: VARIANT });
    ev.check(CANDIDATE ? "candidate: C1 reproduced in all four divisions" : "option: C1 absent in all four divisions", CANDIDATE ? reproduced === 4 : reproduced === 0, reproduced);
  });
  requireClean(ev);
});
