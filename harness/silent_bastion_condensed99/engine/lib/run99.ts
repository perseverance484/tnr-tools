/**
 * Condensed four-division runner: walks any condensed-99-shaped symbolic graph (the candidate or a
 * derived remediation option) through the real routers (lib/driver.ts), choosing dialog options and
 * battle outcomes only, and checks every battle start and every loss/recovery/reset transition
 * against the brief's contract. The path is read from the graph, not hard-coded, so dialog gates
 * folded by an option are followed automatically.
 */
import { MAX, HERO, beacons, choose, currentBattle, engineView, hero, payouts, refresh, settle, api, db, tracker } from "./driver";
import { aiIdForSlot, loadGraph, PLACEHOLDER_EFFECTS, QUEST_ID, type SymNode } from "./graph";
import type { Evidence } from "./report";

export type Route = "clean" | "alert" | "medical" | "combat";
export type Point = "f1" | "f2" | "f3" | "f4" | "boss";
/**
 * One pass through a division from its current checkpoint (d.n.f1 on entry, d.n.f2 after a
 * recovery win). `lossAt` loses that battle; `recoveryLosses` recovery fights are then lost before
 * the recovery fight is won. Without `lossAt` the pass ends with the commander beaten.
 */
export type Seg = { route: Route; lossAt?: Point; wrong?: "wrong_a" | "wrong_b"; recoveryLosses?: number; stopAfterLoss?: boolean };
export type Plan = { name: string; divisions: Seg[][]; expect: "complete" | "fail" };

export const DIVS = [2, 3, 4, 5] as const;
const graph = loadGraph();
const sym = new Map(graph.nodes.map((n) => [n.id, n]));
export const ROOT = (graph.root ?? graph.entry) as string;
const node = (id: string) => {
  const n = sym.get(id);
  if (!n) throw new Error(`unknown node ${id}`);
  return n;
};
export const pointOf = (battleId: string): Point | "recovery" => {
  const s = battleId.split(".").slice(1).join(".");
  if (s.startsWith("recovery")) return "recovery";
  if (s.startsWith("n.boss")) return "boss";
  return s.slice(2) as Point;
};
const divOf = (id: string) => Number(id.match(/^[dbr](\d)/)?.[1] ?? 0);

/** Dialog option the plan selects at dialog `n`. */
const optionFor = (n: SymNode, seg: Seg): string => {
  if (n.next) return n.next;
  const ch = n.choices ?? [];
  if (n.id.endsWith(".terminal")) {
    const wantPuzzle = seg.route === "clean" || seg.route === "alert";
    return ch.find((c) => (wantPuzzle ? c.to.endsWith(".puzzle") : /\.f4$/.test(c.to)))!.to;
  }
  if (n.id.endsWith(".puzzle")) {
    const label = seg.route === "clean" ? "correct" : (seg.wrong ?? "wrong_a");
    return ch.find((c) => c.label === label)!.to;
  }
  if (n.id.endsWith(".protocol")) return ch.find((c) => c.to.endsWith(`.boss.${seg.route}`))!.to;
  throw new Error(`no plan rule for dialog ${n.id}`);
};

type Pools = { health: number; chakra: number; stamina: number };
const pct = (v: number, m: number) => Math.round((v / m) * 10000) / 100;
const lossesOf = (d: number) => ({ first: `d${d}.lost_first`, later: `d${d}.lost_later` });

export class Runner {
  carry: Pools = { health: MAX.health, chakra: MAX.chakra, stamina: MAX.stamina };
  battles = 0;
  trace: Record<string, unknown>[] = [];
  beaconsBefore = 0;
  commanderWins: Record<number, number> = {};
  private lastStart: Pools = { ...this.carry };
  constructor(readonly ev: Evidence, readonly plan: Plan) {}
  c(name: string, pass: boolean, detail?: unknown) {
    return this.ev.check(`${this.plan.name}: ${name}`, pass, detail);
  }

  async start() {
    // A later attempt carries whatever the previous one left (no refill on a new attempt).
    const h0 = await hero();
    if (h0) this.carry = { health: h0.curHealth, chakra: h0.curChakra, stamina: h0.curStamina };
    this.beaconsBefore = await beacons();
    const r = await (await api()).quests.startQuest({ questId: QUEST_ID, userSector: 0 });
    this.c("startQuest succeeds", r.success, r.message);
    const h = await hero();
    this.c("run starts isolated between floors (BATTLE, no battle)", h?.status === "BATTLE" && h.battleId === null);
    this.c("exactly one Beacon charged by the start (pin behaviour, dc07be41)", (await beacons()) === this.beaconsBefore - 1, { before: this.beaconsBefore, now: await beacons() });
    this.c(`engine active objective is the single root ${ROOT}`, (await engineView()).active === ROOT);
  }

  /** Done objective ids of divisions before `d` — must survive every later loss and reset. */
  private async earlierDone(d: number) {
    return ((await tracker())?.goals ?? []).filter((g) => g.done && divOf(g.id) > 0 && divOf(g.id) < d).map((g) => g.id).sort();
  }

  /** Choose the option at dialog `id`; returns the chosen target. */
  private async step(id: string, seg: Seg) {
    const view = await engineView();
    this.c(`${id} is the engine's active objective before choosing`, view.active === id, view);
    const to = optionFor(node(id), seg);
    const res = await choose(to);
    this.c(`${id} -> ${to} accepted`, res.success, res.message);
    return to;
  }

  /** Play one division according to its segments. Returns "won" or "failed" (Arakane). */
  async division(d: number, segs: Seg[]): Promise<"won" | "failed"> {
    const kept = await this.earlierDone(d);
    let at = `d${d}.n.f1`;
    for (let s = 0; s < segs.length; s++) {
      const seg = segs[s]!;
      const out = await this.pass(d, at, seg);
      if (out === "stopped") throw new Error("stopAfterLoss is for single passes only");
      const still = await this.earlierDone(d);
      this.c(`D${d} seg ${s + 1}: earlier divisions untouched (${kept.length} done objectives kept)`, kept.every((k) => still.includes(k)), { missing: kept.filter((k) => !still.includes(k)) });
      if (out === "failed") return "failed";
      if (out === "won") {
        this.c(`D${d}: commander beaten on the last planned segment`, s === segs.length - 1, { seg: s, of: segs.length });
        this.commanderWins[d] = (this.commanderWins[d] ?? 0) + 1;
        return "won";
      }
      at = `d${d}.n.f2`;
      this.c(`D${d} seg ${s + 1}: plan has a following segment after the recovery`, s < segs.length - 1);
    }
    throw new Error(`plan for D${d} ended without beating the commander`);
  }

  /**
   * Walk from dialog `at`; returns "won" (commander beaten), "recovered" (back at d.n.f2),
   * "failed" (Arakane) or "stopped" (loss with `stopAfterLoss`, left at the loss dialog).
   */
  async pass(d: number, at: string, seg: Seg): Promise<"won" | "recovered" | "failed" | "stopped"> {
    let id = at;
    for (;;) {
      const n = node(id);
      if (n.kind !== "dialog") throw new Error(`walker expected a dialog at ${id}`);
      const to = await this.step(id, seg);
      const next = node(to);
      if (next.kind === "dialog") {
        this.c(`${id}: no battle starts on a dialog-to-dialog step`, (await currentBattle()) === null);
        id = to;
        continue;
      }
      if (next.kind !== "battle") throw new Error(`unexpected ${next.kind} after ${id}`);
      const p = pointOf(to) as Point;
      const lose = seg.lossAt === p;
      await this.fight(to);
      const out = await this.afterBattle(to, !lose);
      if (out === "failed") return "failed";
      if (out === "lost" && seg.stopAfterLoss) return "stopped";
      if (out === "lost") return this.recover(d, p === "f1" ? "first" : "later", seg.recoveryLosses ?? 0);
      if (p === "boss") return "won";
      id = next.onWin!;
    }
  }

  /** After a loss: dialog → 50% recovery fight, `losses` times lost, then won. */
  private async recover(d: number, kind: "first" | "later", losses: number): Promise<"recovered"> {
    const dialog = lossesOf(d)[kind];
    const battle = `b${d}.recovery_${kind}`;
    for (let i = 0; i <= losses; i++) {
      const win = i === losses;
      await this.step(dialog, { route: "clean" });
      await this.fight(battle);
      await this.afterBattle(battle, win, dialog);
    }
    return "recovered";
  }

  async fight(id: string) {
    const n = node(id);
    const snap = await currentBattle();
    this.c(`${id}: exactly this battle started`, !!snap && snap.extraState.questBattleSource?.objectiveId === id, snap?.extraState.questBattleSource ?? null);
    if (!snap) throw new Error(`${this.plan.name}: ${id} did not start`);
    const live = (await (await db()).query.battle.findMany()).length;
    this.c(`${id}: one live battle`, live === 1, live);
    const p = snap.usersState.find((u) => u.userId === HERO)!;
    const foes = snap.usersState.filter((u) => u.isAi).map((u) => u.controllerId);
    this.c(`${id}: opponent is slot ${n.encounterSlot} only`, foes.length === 1 && foes[0] === aiIdForSlot(n.encounterSlot!), foes);
    const got = { health: p.curHealth, chakra: p.curChakra, stamina: p.curStamina };
    const max = { health: p.maxHealth, chakra: p.maxChakra, stamina: p.maxStamina };
    const sp = n.startPoolsPercent;
    const want = sp !== undefined ? { health: (max.health * sp) / 100, chakra: (max.chakra * sp) / 100, stamina: (max.stamina * sp) / 100 } : this.carry;
    const ok = Math.abs(got.health - want.health) < 1e-6 && Math.abs(got.chakra - want.chakra) < 1e-6 && Math.abs(got.stamina - want.stamina) < 1e-6;
    this.c(`${id}: start pools ${sp !== undefined ? `set to ${sp}%` : "carried unchanged"}`, ok, { got, want, max });
    const questFx = (snap.usersEffects ?? []).filter((e) => e.fromType === "quest");
    const expectFx = n.startEffect ? [PLACEHOLDER_EFFECTS[n.startEffect]!.tag.type] : [];
    const fxOk = questFx.map((e) => e.type).sort().join() === expectFx.join() && questFx.every((e) => e.targetId === HERO);
    this.c(`${id}: quest starting effects ${expectFx.join() || "none"} on the player only`, fxOk, questFx.map((e) => ({ type: e.type, target: e.targetId })));
    this.c(`${id}: still exactly one Beacon charged this attempt`, (await beacons()) === this.beaconsBefore - 1);
    this.battles++;
    this.trace.push({ battle: id, slot: n.encounterSlot, carriedHpPct: pct(this.carry.health, MAX.health),
      startPct: { h: pct(got.health, max.health), c: pct(got.chakra, max.chakra), s: pct(got.stamina, max.stamina) }, effects: questFx.map((e) => e.type) });
    this.lastStart = got;
  }

  /**
   * Settle the live battle and check the transition. `lossDialog` is set for recovery fights
   * (where a loss must rewind to that dialog via reset_quest).
   */
  async afterBattle(id: string, win: boolean, lossDialog?: string): Promise<"won" | "lost" | "failed"> {
    const n = node(id);
    const d = divOf(id);
    // Deterministic attrition from the battle's own start pools, so carried vs set-to is visible.
    const pools = { health: Math.round(this.lastStart.health * 0.97), chakra: Math.round(this.lastStart.chakra * 0.97), stamina: Math.round(this.lastStart.stamina * 0.97) };
    await settle(win, pools);
    this.trace[this.trace.length - 1]!.outcome = win ? "Won" : "Lost";
    this.c(`${id}: no quest reward before completion`, (await payouts()) === 0);
    const h = await hero();
    if (win) {
      this.carry = pools;
      this.c(`${id}: win keeps the run between floors with the fight's end pools`, h?.status === "BATTLE" && h.battleId === null && h.curHealth === pools.health && h.curChakra === pools.chakra && h.curStamina === pools.stamina,
        { status: h?.status, hp: h?.curHealth, pools });
      await refresh();
      let target = n.onWin!;
      // Remediation options: a dialog confirms the recovery before the reset rewinds to regular 2.
      if (node(target).kind === "dialog" && target.endsWith(".recovered")) {
        const v = await engineView();
        this.c(`${id}: recovery win opens ${target} (reset not yet fired)`, v.active === target && (await currentBattle()) === null, v);
        await this.step(target, { route: "clean" });
        target = node(target).next!;
      }
      if (node(target).kind === "reset") {
        await refresh();
        target = node(target).resetTarget!;
      }
      const view = await engineView();
      this.c(`${id}: after the win the active objective is ${target}, nothing auto-fires`, (await currentBattle()) === null && view.active === target && view.open.length === 1, view);
      const h2 = await hero();
      this.c(`${id}: end pools still carried after the transition`, h2?.curHealth === pools.health && h2.curChakra === pools.chakra && h2.curStamina === pools.stamina, { hp: h2?.curHealth });
      return "won";
    }
    this.c(`${id}: defeat keeps the player in the run at 1 HP`, h?.curHealth === 1 && h.battleId === null, { hp: h?.curHealth, status: h?.status });
    const retry = await (await api()).quests.retryBattle({ questId: QUEST_ID });
    this.c(`${id}: no in-place Retry Battle is offered`, !retry.success, retry.message);
    this.carry = { health: 1, chakra: pools.chakra, stamina: pools.stamina };
    await refresh();
    if (n.onLoss === "f.arakane") return "failed";
    const target = lossDialog ?? (pointOf(id) === "f1" ? lossesOf(d).first : lossesOf(d).later);
    if (node(n.onLoss!).kind === "reset") await refresh();
    const view = await engineView();
    this.c(`${id}: loss leads to ${target} (same division checkpoint)`, view.active === target && view.open.length === 1, view);
    this.c(`${id}: no battle auto-fires after a loss`, (await currentBattle()) === null);
    return "lost";
  }

  async run() {
    await this.start();
    for (let i = 0; i < DIVS.length; i++) {
      const d = DIVS[i]!;
      const out = await this.division(d, this.plan.divisions[i]!);
      if (out === "failed") return this.finishFail(d);
    }
    return this.finishWin();
  }

  private async finishWin() {
    const view = await engineView();
    this.c("after Arakane: aftermath dialog is active, no reward yet", view.active === "d.aftermath" && (await payouts()) === 0, view);
    this.c("one commander victory in each of the four divisions", DIVS.every((d) => this.commanderWins[d] === 1), this.commanderWins);
    const res = await choose("w.complete");
    this.c("aftermath -> win resolves the quest", res.success && (res as { resolved?: boolean }).resolved === true, res.message);
    const h = await hero();
    const hist = await (await db()).query.questHistory.findMany();
    this.c("completion pays the quest reward exactly once", (await payouts()) === 1, await payouts());
    this.c("completion releases isolation (AWAKE)", h?.status === "AWAKE" && h.battleId === null, h?.status);
    this.c("history: one attempt, completed", hist.length === 1 && hist[0]!.completed === 1 && !!hist[0]!.endAt);
    const again = await choose("w.complete");
    this.c("replaying the final claim pays nothing more", (await payouts()) === 1, again.message);
    this.c("plan expected completion", this.plan.expect === "complete");
    this.c("pools are not restored by completion", h?.curHealth === this.carry.health, { hp: h?.curHealth, carry: this.carry.health });
    await this.newAttemptAfterEnd();
    return "complete" as const;
  }

  private async finishFail(d: number) {
    const h = await hero();
    const hist = await (await db()).query.questHistory.findMany();
    this.c("Arakane defeat ends the attempt", d === 5 && hist.length === 1 && hist[0]!.completed === 0 && !!hist[0]!.endAt);
    this.c("failed attempt releases isolation (AWAKE)", h?.status === "AWAKE" && h.battleId === null, h?.status);
    this.c("failed attempt pays no quest reward", (await payouts()) === 0);
    this.c("failed attempt refunds no Beacon", (await beacons()) === this.beaconsBefore - 1);
    this.c("failed attempt restores no pools (1 HP kept)", h?.curHealth === 1, h?.curHealth);
    this.c("plan expected failure", this.plan.expect === "fail");
    await this.newAttemptAfterEnd();
    return "fail" as const;
  }

  /** A closed attempt cannot continue; a new attempt restarts at the root and pays a new Beacon. */
  private async newAttemptAfterEnd() {
    const firstBattle = node(ROOT).next!;
    const stale = await choose(firstBattle);
    this.c("closed attempt: no further progress or battle", !stale.success || (await currentBattle()) === null, stale.message);
    const before = await beacons();
    const hpBefore = (await hero())?.curHealth;
    const r = await (await api()).quests.startQuest({ questId: QUEST_ID, userSector: 0 });
    this.c("new attempt can start", r.success, r.message);
    const view = await engineView();
    this.c(`new attempt restarts fresh at ${ROOT} (no stale tracker)`, view.active === ROOT && view.open.length === 1, view);
    this.c("new attempt charges a new Beacon once", (await beacons()) === before - 1, { before, now: await beacons() });
    const c = await choose(firstBattle);
    const snap = await currentBattle();
    const p = snap?.usersState.find((u) => u.userId === HERO);
    this.c("new attempt's first battle starts without refilled pools", c.success && !!p && p.curHealth === hpBefore, { battleHp: p?.curHealth, hpBefore });
  }
}
