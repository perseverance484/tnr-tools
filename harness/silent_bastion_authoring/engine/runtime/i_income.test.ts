/**
 * Gate I — recovery-battle income (RUL-2026-10-16-005, option O2) on the COMPILED candidate quest.
 *
 * The eight recovery battles carry `scaleGains: 0`; every other battle leaves it unset. Per division
 * this walks the real routers: lose regular 1, win recovery_first, win regular 2, lose regular 3,
 * win recovery_later. A recovery win must still count as a win (the graph advances exactly as the
 * C99 contract says) while the battle's `rewardScaling` is 0 and the settlement pays no money or
 * experience; a first-pass win in the same run must pay.
 * Paid amounts vary with the engine's random settlement, so they go to i_income.timings.json. Runs only with TNR_COMPILED_QUEST set.
 */
import { beforeEach, it, vi } from "bun:test";
import { Pusher } from "@/libs/pusher";
import { describeWithDatabase } from "../setup/testDatabase";
import { choose, currentBattle, engineView, hero, refresh, resetWorld, settle, HERO } from "./lib/driver";
import { loadGraph } from "./lib/graph";
import { Evidence, requireClean } from "./lib/report";
import { Runner } from "./lib/run99";

const ev = new Evidence("i_income");
const COMPILED = !!process.env.TNR_COMPILED_QUEST;
const sym = new Map(loadGraph().nodes.map((n) => [n.id, n]));
const node = (id: string) => sym.get(id)!;
const pools = { health: 800, chakra: 900, stamina: 700 };

/** Single-path dialog → its target (regular-fight dialogs and loss dialogs have one option). */
const fwd = (id: string) => node(id).next ?? node(id).choices![0]!.to;

const gains = async () => {
  const h = await hero();
  return { money: Number(h?.money ?? 0), experience: Number(h?.experience ?? 0) };
};

/** Start the battle reached from dialog `at`, settle it, and return what the settlement paid. */
const fightFrom = async (tag: string, at: string, battleId: string, win: boolean) => {
  const res = await choose(fwd(at));
  ev.check(`${tag}: ${at} -> ${battleId} accepted`, res.success && fwd(at) === battleId, { to: fwd(at), msg: res.message });
  const snap = await currentBattle();
  ev.check(`${tag}: ${battleId} is the live battle`, snap?.extraState.questBattleSource?.objectiveId === battleId, snap?.extraState.questBattleSource ?? null);
  const scaling = Number(snap?.rewardScaling);
  const before = await gains();
  const result = await settle(win, win ? pools : { health: 0, chakra: 100, stamina: 100 });
  await refresh();
  const after = await gains();
  return { scaling, result, paid: { money: after.money - before.money, experience: after.experience - before.experience } };
};

/** Follow a won battle's onWin through an optional confirmation dialog and reset; return the landing. */
const settleWin = async (battleId: string) => {
  let t = node(battleId).onWin!;
  if (node(t).kind === "dialog" && t.endsWith(".recovered")) {
    ev.check(`${battleId}: win opens ${t} (counts as a win)`, (await engineView()).active === t);
    const r = await choose(node(t).next!);
    ev.check(`${t} confirmed`, r.success, r.message);
    t = node(t).next!;
  }
  if (node(t).kind === "reset") { await refresh(); t = node(t).resetTarget!; }
  return t;
};

describeWithDatabase("I: recovery battles pay no settlement, first-pass battles do", () => {
  beforeEach(() => { vi.spyOn(Pusher.prototype, "trigger").mockResolvedValue(undefined); });
  for (const d of [2, 3, 4, 5]) {
    it(`I${d}: division ${d - 1}`, async () => {
      ev.check("runs on the compiled candidate quest (TNR_COMPILED_QUEST)", COMPILED);
      if (!COMPILED) return;
      await resetWorld();
      const r = new Runner(ev, { name: `I${d}`, divisions: [], expect: "complete" });
      await r.start();
      for (let e = 2; e < d; e++) await r.division(e, [{ route: "clean" }]);
      const tag = `I${d}`;
      ev.check(`${tag}: at d${d}.n.f1`, (await engineView()).active === `d${d}.n.f1`);

      // Regular 1 lost → recovery_first won.
      await fightFrom(tag, `d${d}.n.f1`, `b${d}.n.f1`, false);
      ev.check(`${tag}: loss leads to d${d}.lost_first`, (await engineView()).active === `d${d}.lost_first`);
      const rf = await fightFrom(tag, `d${d}.lost_first`, `b${d}.recovery_first`, true);
      ev.check(`${tag}: recovery_first battle rewardScaling is 0`, rf.scaling === 0, rf.scaling);
      ev.check(`${tag}: recovery_first settlement pays no money or experience`,
        rf.result.money === 0 && rf.result.experience === 0 && rf.result.earnedExperience === 0 && rf.paid.money === 0 && rf.paid.experience === 0,
        { result: { money: rf.result.money, experience: rf.result.experience, earned: rf.result.earnedExperience }, paid: rf.paid });
      const afterRf = await settleWin(`b${d}.recovery_first`);
      ev.check(`${tag}: recovery_first win advances to ${afterRf}`, (await engineView()).active === afterRf && afterRf === `d${d}.n.f2` && (await currentBattle()) === null);

      // Regular 2 won (first pass, scaleGains unset) → pays.
      const f2 = await fightFrom(tag, `d${d}.n.f2`, `b${d}.n.f2`, true);
      ev.check(`${tag}: first-pass battle rewardScaling is the engine default (scaleGains 1 × 2 combatants / 2 = 1)`, f2.scaling === 1, f2.scaling);
      ev.check(`${tag}: first-pass win pays experience`, f2.result.experience > 0 && f2.paid.experience > 0,
        { result: { money: f2.result.money, experience: f2.result.experience }, paid: f2.paid });
      const at3 = node(`b${d}.n.f2`).onWin!;
      ev.check(`${tag}: first-pass win advances to ${at3}`, (await engineView()).active === at3);

      // Regular 3 lost → recovery_later won (C1-safe confirmation dialog, then reset to regular 2).
      await fightFrom(tag, at3, `b${d}.n.f3`, false);
      if (node(node(`b${d}.n.f3`).onLoss!).kind === "reset") await refresh();
      ev.check(`${tag}: loss leads to d${d}.lost_later`, (await engineView()).active === `d${d}.lost_later`);
      const rl = await fightFrom(tag, `d${d}.lost_later`, `b${d}.recovery_later`, true);
      ev.check(`${tag}: recovery_later battle rewardScaling is 0`, rl.scaling === 0, rl.scaling);
      ev.check(`${tag}: recovery_later settlement pays no money or experience`,
        rl.result.money === 0 && rl.result.experience === 0 && rl.result.earnedExperience === 0 && rl.paid.money === 0 && rl.paid.experience === 0,
        { result: { money: rl.result.money, experience: rl.result.experience, earned: rl.result.earnedExperience }, paid: rl.paid });
      const afterRl = await settleWin(`b${d}.recovery_later`);
      ev.check(`${tag}: recovery_later win advances to ${afterRl}`, (await engineView()).active === afterRl && afterRl === `d${d}.n.f2` && (await currentBattle()) === null);
      const h = await hero();
      ev.check(`${tag}: still in the run between floors`, h?.status === "BATTLE" && h.battleId === null && h.userId === HERO);
      ev.put(`${tag}.income`, { recoveryFirst: { scaling: rf.scaling, paid: rf.paid }, firstPassF2: { scaling: f2.scaling, paysExperience: f2.paid.experience > 0 }, recoveryLater: { scaling: rl.scaling, paid: rl.paid } });
      ev.timing(`${tag}.firstPassF2.paid`, f2.paid);
    });
  }
  requireClean(ev);
});
