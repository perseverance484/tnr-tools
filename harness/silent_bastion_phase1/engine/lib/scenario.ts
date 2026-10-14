/**
 * Scenario runner: walks the compiled fixture through the real routers (lib/driver.ts),
 * choosing dialog options and battle outcomes, and checks every battle start against the
 * approved design. It records a deterministic trace for the evidence file.
 */
import { battle } from "@/drizzle/schema";
import { MAX, HERO, beacons, choose, currentBattle, engineView, hero, payouts, refresh, settle, api, db } from "./driver";
import { aiIdForSlot, loadGraph, PLACEHOLDER_EFFECTS, QUEST_ID } from "./graph";
import type { Evidence } from "./report";

export type Route = "clean" | "alert" | "medical" | "combat";
export type Point = "f1" | "f2" | "f3" | "f4" | "boss";
export type Seg = { route: Route; lossAt?: Point; wrong?: "wrong_a" | "wrong_b" };
export type Plan = { name: string; divisions: Seg[][]; expect: "complete" | "fail" };

const graph = loadGraph();
const sym = new Map(graph.nodes.map((n) => [n.id, n]));

/** Objective ids of one lane pass, in order, up to and including its commander battle. */
export const lanePath = (d: number, lane: "n" | "r", seg: Seg) => {
  const p = (s: string) => `d${d}.${lane}.${s}`;
  const b = (s: string) => `b${d}.${lane}.${s}`;
  const ids = [p("f1"), b("f1"), p("f2"), b("f2"), p("f3"), b("f3"), p("terminal")];
  if (seg.route === "clean" || seg.route === "alert") ids.push(p("puzzle"), p(`boss.${seg.route}`), b(`boss.${seg.route}`));
  // r2: one fourth fight; the protocol dialog after it routes straight to the commander battle.
  else ids.push(p("f4"), b("f4"), p("protocol"), b(`boss.${seg.route}`));
  return ids;
};
const pointOf = (battleId: string): Point => {
  const s = battleId.split(".").slice(2).join(".");
  return s.startsWith("boss") ? "boss" : s.startsWith("f4") ? "f4" : (s as Point);
};
/** Dialog option the driver selects to move from dialog `id` to `to`. */
const optionFor = (id: string, to: string, seg: Seg) => {
  const n = sym.get(id)!;
  if (n.next) return n.next;
  if (id.endsWith(".puzzle")) {
    const label = seg.route === "clean" ? "correct" : (seg.wrong ?? "wrong_a");
    return n.choices!.find((c) => c.label === label)!.to;
  }
  return n.choices!.find((c) => c.to === to)!.to;
};

type Pools = { health: number; chakra: number; stamina: number };
const pct = (v: number, m: number) => Math.round((v / m) * 10000) / 100;

export class Runner {
  carry: Pools = { health: MAX.health, chakra: MAX.chakra, stamina: MAX.stamina };
  battles = 0;
  trace: unknown[] = [];
  beaconsAtStart = 0;
  constructor(readonly ev: Evidence, readonly plan: Plan) {}
  private c(name: string, pass: boolean, detail?: unknown) {
    return this.ev.check(`${this.plan.name}: ${name}`, pass, detail);
  }
  nextWinPools(): Pools {
    // Deterministic attrition (3% per win) so carry is distinguishable from the 50%/100% set-to values.
    return { health: Math.round(this.carry.health * 0.97), chakra: Math.round(this.carry.chakra * 0.97), stamina: Math.round(this.carry.stamina * 0.97) };
  }

  async start() {
    this.beaconsAtStart = await beacons();
    const r = await (await api()).quests.startQuest({ questId: QUEST_ID, userSector: 0 });
    this.c("startQuest succeeds", r.success, r.message);
    const h = await hero();
    this.c("run starts isolated between floors (BATTLE, no battle)", h?.status === "BATTLE" && h.battleId === null);
    this.c("starting the run does not consume the Beacon", (await beacons()) === this.beaconsAtStart);
    this.c("engine active objective is the single root d1.n.f1", (await engineView()).active === "d1.n.f1");
  }

  /** Walk one lane pass. Returns "won" (commander beaten), "lost", or "failed" (Arakane). */
  async lane(d: number, lane: "n" | "r", seg: Seg): Promise<"won" | "lost" | "failed"> {
    const path = lanePath(d, lane, seg);
    for (let i = 0; i < path.length; i++) {
      const id = path[i]!;
      const node = sym.get(id)!;
      if (node.kind === "dialog") {
        const view = await engineView();
        this.c(`${id} is the engine's active objective before choosing`, view.active === id, view);
        const option = optionFor(id, path[i + 1]!, seg);
        const res = await choose(option);
        this.c(`${id} -> ${option} accepted`, res.success, res.message);
        const next = sym.get(option)!;
        if (next.kind === "battle") await this.fight(option, d, lane, seg);
        else this.c(`${id}: no battle starts on a dialog-to-dialog step`, (await currentBattle()) === null);
        if (next.kind === "battle") {
          const out = await this.afterBattle(option, d, lane, seg);
          // A loss/failure ends the pass; a commander win ends the division.
          if (out !== "won" || pointOf(option) === "boss") return out;
          i++; // battle consumed
        }
      }
    }
    return "won";
  }

  private async fight(id: string, d: number, lane: string, seg: Seg) {
    const node = sym.get(id)!;
    const snap = await currentBattle();
    this.c(`${id}: exactly this battle started`, !!snap && snap.extraState.questBattleSource?.objectiveId === id, snap?.extraState.questBattleSource);
    if (!snap) return;
    const live = (await (await db()).query.battle.findMany()).length;
    this.c(`${id}: one live battle`, live === 1, live);
    const p = snap.usersState.find((u) => u.userId === HERO)!;
    const foes = snap.usersState.filter((u) => u.isAi).map((u) => u.controllerId);
    this.c(`${id}: opponent is slot ${node.encounterSlot} only`, foes.length === 1 && foes[0] === aiIdForSlot(node.encounterSlot!), foes);
    const got = { health: p.curHealth, chakra: p.curChakra, stamina: p.curStamina };
    const max = { health: p.maxHealth, chakra: p.maxChakra, stamina: p.maxStamina };
    const want = node.startPoolsPercent !== undefined
      ? { health: (max.health * node.startPoolsPercent) / 100, chakra: (max.chakra * node.startPoolsPercent) / 100, stamina: (max.stamina * node.startPoolsPercent) / 100 }
      : this.carry;
    const poolsOk = Math.abs(got.health - want.health) < 1e-6 && Math.abs(got.chakra - want.chakra) < 1e-6 && Math.abs(got.stamina - want.stamina) < 1e-6;
    this.c(`${id}: start pools ${node.startPoolsPercent !== undefined ? `set to ${node.startPoolsPercent}%` : "carried unchanged"}`, poolsOk, { got, want, max });
    const questFx = (snap.usersEffects ?? []).filter((e) => e.fromType === "quest");
    const expectFx = node.startEffect ? [PLACEHOLDER_EFFECTS[node.startEffect]!.tag.type] : [];
    const fxOk = questFx.map((e) => e.type).sort().join() === expectFx.join() && questFx.every((e) => e.targetId === HERO);
    this.c(`${id}: quest starting effects ${expectFx.join() || "none"} on the player only`, fxOk, questFx.map((e) => ({ type: e.type, target: e.targetId, rounds: e.rounds, power: e.power })));
    this.c(`${id}: Beacon charged exactly once per attempt`, (await beacons()) === this.beaconsAtStart - 1, { now: await beacons(), atStart: this.beaconsAtStart });
    this.battles++;
    const carriedPct = pct(this.carry.health, MAX.health);
    this.trace.push({ battle: id, slot: node.encounterSlot, carriedHpPct: carriedPct, startPct: { h: pct(got.health, max.health), c: pct(got.chakra, max.chakra), s: pct(got.stamina, max.stamina) }, effects: questFx.map((e) => e.type) });
  }

  private async afterBattle(id: string, d: number, lane: string, seg: Seg): Promise<"won" | "lost" | "failed"> {
    const loses = seg.lossAt !== undefined && pointOf(id) === seg.lossAt;
    const pools = this.nextWinPools();
    await settle(!loses, pools);
    (this.trace[this.trace.length - 1] as Record<string, unknown>).outcome = loses ? "Lost" : "Won";
    const node = sym.get(id)!;
    const h = await hero();
    this.c(`${id}: no quest reward before completion`, (await payouts()) === 0);
    if (!loses) {
      this.carry = pools;
      this.c(`${id}: win keeps the run between floors with settled pools`, h?.status === "BATTLE" && h.battleId === null && h.curHealth === pools.health && h.curChakra === pools.chakra && h.curStamina === pools.stamina,
        { status: h?.status, hp: h?.curHealth, cp: h?.curChakra, sp: h?.curStamina, pools });
      await refresh();
      const view = await engineView();
      this.c(`${id}: no adjacent battle auto-fires after a win`, (await currentBattle()) === null && view.active === node.onWin, view);
      return "won";
    }
    // Loss
    this.c(`${id}: defeat keeps the player in the run at 1 HP`, h?.curHealth === 1 && h.battleId === null, { hp: h?.curHealth, status: h?.status });
    const retry = await (await api()).quests.retryBattle({ questId: QUEST_ID });
    this.c(`${id}: no in-place Retry Battle is offered`, !retry.success, retry.message);
    await refresh();
    if (node.onLoss === "f.arakane") return "failed";
    const view = await engineView();
    const target = `d${d}.r.f1`;
    this.c(`${id}: loss routes to ${target} (same division retry entry)`, view.active === target && view.open.length === 1, view);
    this.c(`${id}: no battle auto-fires after a loss`, (await currentBattle()) === null);
    return "lost";
  }

  async run() {
    await this.start();
    for (let d = 1; d <= 5; d++) {
      const segs = this.plan.divisions[d - 1]!;
      let lane: "n" | "r" = "n";
      for (let s = 0; s < segs.length; s++) {
        const out = await this.lane(d, lane, segs[s]!);
        if (out === "failed") return this.finishFail(d, lane);
        if (out === "won") {
          this.c(`D${d}: commander win joins the next division's ordinary lane`, s === segs.length - 1, { seg: s, of: segs.length });
          break;
        }
        lane = "r";
      }
    }
    return this.finishWin();
  }

  private async finishWin() {
    const view = await engineView();
    this.c("after Arakane: aftermath dialog is active, no reward yet", view.active === "d.aftermath" && (await payouts()) === 0, view);
    const res = await choose("w.complete");
    this.c("aftermath -> win resolves the quest", res.success && (res as { resolved?: boolean }).resolved === true, res);
    const h = await hero();
    const hist = (await (await db()).query.questHistory.findMany());
    this.c("completion pays the quest reward exactly once", (await payouts()) === 1, await payouts());
    this.c("completion releases isolation (AWAKE)", h?.status === "AWAKE" && h.battleId === null, h?.status);
    this.c("history: one attempt, completed", hist.length === 1 && hist[0]!.completed === 1 && !!hist[0]!.endAt, hist.map((r) => ({ completed: r.completed, endAt: !!r.endAt })));
    const again = await choose("w.complete");
    this.c("replaying the final claim pays nothing more", (await payouts()) === 1, { success: again.success, message: again.message });
    this.c("plan expected completion", this.plan.expect === "complete");
    this.c("pools are not restored by completion", h?.curHealth === this.carry.health, { hp: h?.curHealth, carry: this.carry.health });
    await this.newAttemptAfterEnd();
    return "complete" as const;
  }

  /** A closed attempt cannot continue; a new attempt restarts at the root and needs a new Beacon. */
  private async newAttemptAfterEnd() {
    const stale = await choose("b1.n.f1");
    this.c("closed attempt: no further progress or battle", !stale.success || (await currentBattle()) === null, stale.message);
    const before = await beacons();
    const r = await (await api()).quests.startQuest({ questId: QUEST_ID, userSector: 0 });
    this.c("new attempt can start", r.success, r.message);
    const view = await engineView();
    this.c("new attempt restarts fresh at d1.n.f1 (no stale tracker)", view.active === "d1.n.f1" && view.open.length === 1, view);
    const c = await choose("b1.n.f1");
    this.c("new attempt's first battle starts", c.success && (await currentBattle()) !== null, c.message);
    this.c("new attempt charges a new Beacon once", (await beacons()) === before - 1, { before, now: await beacons() });
    const snap = await currentBattle();
    const p = snap?.usersState.find((u) => u.userId === HERO);
    this.c("new attempt does not refill pools", !!p && p.curHealth === (await hero())?.curHealth, { battleHp: p?.curHealth });
  }

  private async finishFail(d: number, lane: string) {
    const h = await hero();
    const hist = await (await db()).query.questHistory.findMany();
    this.c(`Arakane defeat on lane ${lane} ends the attempt`, d === 5 && hist.length === 1 && hist[0]!.completed === 0 && !!hist[0]!.endAt, hist.map((r) => ({ completed: r.completed, endAt: !!r.endAt })));
    this.c("failed attempt releases isolation (AWAKE)", h?.status === "AWAKE" && h.battleId === null, h?.status);
    this.c("failed attempt pays no quest reward", (await payouts()) === 0);
    this.c("failed attempt refunds no Beacon", (await beacons()) === this.beaconsAtStart - 1);
    this.c("failed attempt restores no pools (1 HP kept)", h?.curHealth === 1, h?.curHealth);
    this.c("plan expected failure", this.plan.expect === "fail");
    await this.newAttemptAfterEnd();
    return "fail" as const;
  }
}
