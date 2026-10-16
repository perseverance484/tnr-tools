/**
 * Gate E — entry item (F1/F2 recheck), abandonment, out-of-order input around recovery fights,
 * hidden pause and version change at recovery checkpoints, the real editor save, performance,
 * retry-loop income (F3) and dialog-text exposure (F4/F5) on the condensed graph.
 */
import { beforeEach, expect, it, vi } from "bun:test";
import { eq } from "drizzle-orm";
import { quest, userData } from "@/drizzle/schema";
import { getNewTrackers } from "@/libs/quest";
import { Pusher } from "@/libs/pusher";
import { questsRouter } from "@/server/api/routers/quests";
import { profileRouter } from "@/server/api/routers/profile";
import { QuestValidator } from "@/validators/objectives";
import { callerFor, describeWithDatabase } from "../setup/testDatabase";
import { api, beacons, choose, currentBattle, db, EDITOR, engineView, hero, history, HERO, payouts, questRow, refresh, resetWorld, settle, tracker } from "./lib/driver";
import { loadGraph, QUEST_ID, questRecord } from "./lib/graph";
import { Evidence, requireClean } from "./lib/report";
import { DIVS, ROOT, Runner } from "./lib/run99";

const ev = new Evidence("e_edges");
const c = (n: string, p: boolean, d?: unknown) => ev.check(n, p, d);
const start = async () => (await api()).quests.startQuest({ questId: QUEST_ID, userSector: 0 });
const N = loadGraph().nodes.length;
const CANDIDATE = (process.env.TNR_VARIANT ?? "candidate") === "candidate";

describeWithDatabase("E: edges", () => {
  beforeEach(() => { vi.spyOn(Pusher.prototype, "trigger").mockResolvedValue(undefined); });

  it("E1 no Beacon: the start is refused (F2 closed at the pin) and no dialog can be walked (F1 trigger closed)", async () => {
    await resetWorld({ beaconCount: 0 });
    const s = await start();
    const h = await hero();
    ev.put("E1.startWithoutBeacon", { success: s.success, message: s.message });
    c("E1 startQuest refused without the entry item", !s.success, s.message);
    c("E1 no isolation, no attempt row", h?.status === "AWAKE" && (await history()).length === 0, { status: h?.status });
    const walk = ["b2.n.f1", "b2.n.f2", "d2.n.terminal", "d.aftermath", "w.complete"];
    for (const t of walk) await choose(t);
    c("E1 crafted dialog choices without a run change nothing (no tracker, battle or reward)", !(await tracker()) && (await currentBattle()) === null && (await payouts()) === 0);
    ev.finding("F2", "startQuest admits an entry-item Pyramid without the entry item", s.success, s.message);
    ev.finding("F1", "Missing-Beacon window lets dialogs be pre-completed past an unstarted battle", s.success, "start refused, so the reachable trigger is gone at this pin");
  }, 120_000);

  it("E2 Beacon: charged once at the start, not refunded by abandoning before any fight", async () => {
    await resetWorld();
    await start();
    c("E2 one Beacon charged by startQuest, before any battle", (await beacons()) === 2 && (await currentBattle()) === null);
    const ab = await (await api()).quests.abandon({ id: QUEST_ID });
    c("E2 abandon before the first fight succeeds, no refund", ab.success && (await beacons()) === 2, ab.message);
    await start();
    c("E2 the next attempt charges a new Beacon", (await beacons()) === 1);
    ev.finding("B1", "Entry is charged by startQuest at this pin (upstream dc07be41), not at the first initiated battle as RUL-2026-10-15-001 / the brief state; still exactly once per attempt and never refunded",
      true, { beaconsAfterStartAndAbandon: 2 });
  }, 120_000);

  it("E3 abandonment at a recovery checkpoint and refusal mid-recovery-fight", async () => {
    await resetWorld();
    const r = new Runner(ev, { name: "E3", divisions: [], expect: "fail" });
    await r.start();
    await r.division(2, [{ route: "clean" }]);
    await r.pass(3, "d3.n.f1", { route: "clean", lossAt: "f2", stopAfterLoss: true });
    await choose("b3.recovery_later");
    const mid = await (await api()).quests.abandon({ id: QUEST_ID });
    c("E3 abandon refused during the live recovery fight", !mid.success && (await currentBattle()) !== null, mid.message);
    await settle(true, { health: 420, chakra: 500, stamina: 400 });
    await refresh();
    if (!CANDIDATE) await choose(loadGraph().nodes.find((n) => n.id === "d3.recovered")!.next!), await refresh();
    c("E3 after the recovery win the checkpoint is d3.n.f2", (await engineView()).active === "d3.n.f2", await engineView());
    const ab = await (await api()).quests.abandon({ id: QUEST_ID });
    const h = await hero();
    const hist = await history();
    c("E3 abandon at the post-recovery checkpoint closes the attempt", ab.success && h?.status === "AWAKE" && hist[0]!.completed === 0 && !!hist[0]!.endAt, ab.message);
    c("E3 no refund, no reward, pools kept", (await beacons()) === 2 && (await payouts()) === 0 && h?.curHealth === 420, { hp: h?.curHealth });
    const late = await choose("b3.n.f2");
    c("E3 abandoned run cannot progress", !late.success || (await currentBattle()) === null, late.message);
  }, 300_000);

  it("E4 out-of-order and premature choices around recovery fights are inert", async () => {
    await resetWorld();
    await start();
    for (const p of ["b2.n.f2", "b2.recovery_first", "b2.recovery_later", "d2.lost_later", "b3.n.f1", "w.complete", "d3.n.f1"]) {
      const res = await choose(p);
      const view = await engineView();
      c(`E4 at the root, '${p}' starts nothing and moves nothing`, (await currentBattle()) === null && view.active === ROOT, { success: res.success, view });
    }
    await choose("b2.n.f1");
    await settle(false, { health: 0, chakra: 300, stamina: 300 });
    await refresh();
    for (const p of ["b2.n.f2", "b2.recovery_later", "d2.n.terminal"]) {
      await choose(p);
      c(`E4 after a REG1 loss, '${p}' cannot skip the recovery`, (await engineView()).active === "d2.lost_first" && (await currentBattle()) === null, await engineView());
    }
    await choose("b2.recovery_first");
    const during = await choose("b2.n.f2");
    c("E4 continuing to REG2 during the live recovery fight is rejected", !during.success && !(await tracker())?.goals.find((g) => g.id === "d2.n.f2")?.done, during.message);
    ev.put("E4.logbookActiveDuringRecoveryFirst", (await engineView()).active);
    await settle(true, { health: 450, chakra: 560, stamina: 410 });
    await refresh();
    await choose("b2.n.f2");
    await settle(false, { health: 0, chakra: 100, stamina: 100 });
    await refresh();
    await choose("b2.recovery_later");
    const t = await tracker();
    const target = CANDIDATE ? "d2.n.f2" : "d2.recovered";
    const early = await choose(CANDIDATE ? "b2.n.f2" : "r2.reset_later_win");
    c(`E4 during the live recovery_later fight, '${target}' cannot be taken`, !early.success && (await currentBattle())?.extraState.questBattleSource?.objectiveId === "b2.recovery_later", early.message);
    ev.put("E4.recoveryLaterDuringFight", { logbookActive: (await engineView()).active, recoveryGoalPresent: !!t?.goals.find((g) => g.id === "b2.recovery_later") });
  }, 300_000);

  it("E5 hidden pause and version change at recovery checkpoints", async () => {
    await resetWorld();
    const r = new Runner(ev, { name: "E5", divisions: [], expect: "fail" });
    await r.start();
    await r.pass(2, "d2.n.f1", { route: "clean", lossAt: "f3", stopAfterLoss: true });
    await (await db()).update(quest).set({ hidden: true }).where(eq(quest.id, QUEST_ID));
    const paused = await choose("b2.recovery_later");
    c("E5 hidden quest pauses the run at d2.lost_later (recovery refused)", !paused.success && (await currentBattle()) === null, paused.message);
    await refresh();
    c("E5 paused run keeps the checkpoint", (await engineView()).active === "d2.lost_later");
    await (await db()).update(quest).set({ hidden: false }).where(eq(quest.id, QUEST_ID));
    const resumed = await choose("b2.recovery_later");
    const p = (await currentBattle())?.usersState.find((u) => u.userId === HERO);
    c("E5 unhiding resumes with the 50% recovery fight", resumed.success && !!p && p.curHealth / p.maxHealth === 0.5, resumed.message);
    await settle(true, { health: 470, chakra: 580, stamina: 430 });
    await refresh();
    if (!CANDIDATE) await choose("r2.reset_later_win"), await refresh();
    c("E5 recovery win lands on d2.n.f2", (await engineView()).active === "d2.n.f2");
    // Six hours idle at the checkpoint: no regeneration while isolated.
    await (await db()).update(userData).set({ regenAt: new Date(Date.now() - 6 * 3600_000) }).where(eq(userData.userId, HERO));
    await refresh();
    c("E5 no pool recovery while waiting at the checkpoint", (await hero())?.curHealth === 470);
    const row = await questRow();
    await (await db()).update(quest).set({ updatedAt: new Date(row.updatedAt.getTime() + 5000) }).where(eq(quest.id, QUEST_ID));
    const changed = await choose("b2.n.f2");
    c("E5 edited content blocks the old run after a reset", !changed.success && (await currentBattle()) === null, changed.message);
    const ab = await (await api()).quests.abandon({ id: QUEST_ID });
    c("E5 edited run can be abandoned", ab.success && (await hero())?.status === "AWAKE", ab.message);
  }, 300_000);

  it(`E6 the real content-editor save accepts the ${N}-objective record (hidden)`, async () => {
    await resetWorld();
    const rec = questRecord();
    const editor = await callerFor(questsRouter, EDITOR);
    const t0 = performance.now();
    const res = await editor.update({ id: QUEST_ID, data: QuestValidator.parse({ ...rec, hidden: true }) });
    ev.timing("E6.updateMs", performance.now() - t0);
    c("E6 quests.update succeeds", res.success, res.message);
    const saved = await questRow();
    c(`E6 saved record keeps ${N} objectives in order`, saved.content.objectives.length === N && saved.content.objectives.map((o) => o.id).join() === rec.content.objectives.map((o) => o.id).join());
    c("E6 saved record stays hidden", saved.hidden === true);
    ev.put("E6.savedContentBytes", JSON.stringify(saved.content).length);
  }, 120_000);

  it("E7 performance at the deepest pre-completion state", async () => {
    await resetWorld();
    const r = new Runner(ev, { name: "E7", divisions: [], expect: "complete" });
    const t0 = performance.now();
    await r.start();
    for (const d of DIVS) await r.division(d, [{ route: "medical" }]);
    ev.timing("E7.fullMedicalRunMs", performance.now() - t0);
    const { user } = await refresh();
    const t1 = performance.now();
    for (let i = 0; i < 200; i++) getNewTrackers(structuredClone(user!), [{ task: "any" }]);
    ev.timing("E7.getNewTrackersMsPerCall", (performance.now() - t1) / 200);
    ev.put("E7.trackerGoalsAtDeepestPoint", (await tracker())?.goals.length);
    ev.timing("E7.questDataBytes", JSON.stringify((await hero())!.questData).length);
    c("E7 deepest state reached (aftermath active)", (await engineView()).active === "d.aftermath");
    c("E7 20 battles on the all-Medical route", r.battles === 20, r.battles);
    c("E7 getNewTrackers under 50 ms/call", (ev.volatile["E7.getNewTrackersMsPerCall"] as number) < 50);
  }, 600_000);

  it("E8 retry loop income (F3): REG3 loss -> recovery win -> REG2 win -> REG3 loss, three times", async () => {
    await resetWorld();
    const r = new Runner(ev, { name: "E8", divisions: [], expect: "fail" });
    await r.start();
    await r.pass(2, "d2.n.f1", { route: "clean", lossAt: "f3" });
    const loops: { money: number; experience: number }[] = [];
    for (let i = 0; i < 3; i++) {
      const before = (await hero())!;
      await r.pass(2, "d2.n.f2", { route: "clean", lossAt: "f3" });
      const after = (await hero())!;
      loops.push({ money: after.money - before.money, experience: after.experience - before.experience });
    }
    ev.timing("E8.rawPerLoopDelta", loops);
    ev.put("E8.perLoop(REG2 win + REG3 loss + recovery win)", loops.map((l) => ({ experienceGained: l.experience, ryoGained: l.money > 0 })));
    c("E8 still one Beacon charged", (await beacons()) === 2);
    c("E8 no quest reward from loops", (await payouts()) === 0);
    ev.finding("F3", "Deliberate later losses re-run the 50% recovery fight and already-won regulars; every win pays ordinary battle settlement income on one Beacon (economy decision, user-owned)",
      loops.every((l) => l.money > 0 || l.experience > 0), { loops: loops.length });
  }, 300_000);

  it("E9 dialog text exposure (F4/F5 recheck at the pin)", async () => {
    await resetWorld();
    const text = (await questRow()).content.objectives.find((o) => o.id === "d.aftermath")!.description;
    const has = (r: { content: { objectives: { id: string; description: string }[] } } | null | undefined) => !!r?.content.objectives.find((o) => o.id === "d.aftermath" && o.description === text);
    const realFetch = globalThis.fetch;
    vi.spyOn(globalThis, "fetch").mockImplementation(async (input, init) => {
      if (typeof init?.body !== "string" || !init.body.includes("trpc-ratelimit")) return realFetch(input, init);
      const cmds = JSON.parse(init.body) as unknown[];
      const one = (cmd: unknown[]) => ({ result: cmd[0] === "evalsha" || cmd[0] === "eval" ? [59, 60] : 1 });
      return Response.json(Array.isArray(cmds[0]) ? cmds.map((x) => one(x as unknown[])) : one(cmds));
    });
    const anon = questsRouter.createCaller({ drizzle: await db(), userId: undefined, userIp: "127.0.0.1" } as never);
    const viaGet = has(await anon.get({ id: QUEST_ID }));
    await start();
    const me = await (await callerFor(profileRouter, HERO)).getUser();
    const u = (me as { userData?: { userQuests?: { quest?: { content?: { objectives?: { id: string; description: string }[] } } }[] } }).userData;
    const viaUser = !!u?.userQuests?.some((uq) => uq.quest?.content?.objectives?.some((o) => o.id === "d.aftermath" && o.description === text));
    await (await db()).update(quest).set({ hidden: true }).where(eq(quest.id, QUEST_ID));
    const hiddenViaGet = has(await anon.get({ id: QUEST_ID }));
    const listed = await anon.getAll({ limit: 500, hidden: true });
    const hiddenViaList = (listed.data as { id: string }[]).some((r) => r.id === QUEST_ID && has(r as never));
    ev.put("E9.exposure", { viaQuestsGetLoggedOut: viaGet, viaGetUserAtRunStart: viaUser, hiddenViaGet, hiddenViaList });
    ev.finding("F4", "Dialog text, including the final reveal, is readable via quests.get (logged out) or profile.getUser at run start", viaGet || viaUser, { viaGet, viaUser });
    ev.finding("F5", "hidden:true does not keep a staged quest's dialog text from logged-out callers", hiddenViaGet || hiddenViaList, { hiddenViaGet, hiddenViaList });
    expect(true).toBe(true);
  }, 120_000);

  requireClean(ev);
});
