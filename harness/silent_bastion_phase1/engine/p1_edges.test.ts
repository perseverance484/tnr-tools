/**
 * Gate E — abandonment, premature/out-of-order input, entry-item edge cases, recovery freeze,
 * pause/version changes, the real content save procedure, and 178-objective (r2) performance.
 */
import { beforeEach, expect, it, vi } from "bun:test";
import { eq } from "drizzle-orm";
import { quest, userData, userItem } from "@/drizzle/schema";
import { getNewTrackers } from "@/libs/quest";
import { Pusher } from "@/libs/pusher";
import { questsRouter } from "@/server/api/routers/quests";
import { QuestValidator } from "@/validators/objectives";
import { callerFor, describeWithDatabase } from "../setup/testDatabase";
import {
  api, beacons, choose, currentBattle, db, EDITOR, engineView, hero, history, payouts,
  questRow, refresh, resetWorld, settle, tracker,
} from "./lib/driver";
import { QUEST_ID, questRecord } from "./lib/graph";
import { Evidence, requireClean } from "./lib/report";
import { Runner } from "./lib/scenario";

const ev = new Evidence("e_edges");
const c = (n: string, p: boolean, d?: unknown) => ev.check(n, p, d);
const start = async () => (await api()).quests.startQuest({ questId: QUEST_ID, userSector: 0 });
const pools = { health: 640, chakra: 700, stamina: 610 };

describeWithDatabase("E: edges", () => {
  beforeEach(() => { vi.spyOn(Pusher.prototype, "trigger").mockResolvedValue(undefined); });

  it("E1 abandonment between floors ends the attempt without refund, reward or recovery", async () => {
    await resetWorld();
    const r = new Runner(ev, { name: "E1", divisions: [], expect: "fail" });
    await r.start();
    await r.lane(1, "n", { route: "clean" });
    await choose("b2.n.f1");
    await settle(true, pools);
    const before = { beacons: await beacons(), hp: (await hero())!.curHealth };
    const res = await (await api()).quests.abandon({ id: QUEST_ID });
    const h = await hero();
    const hist = await history();
    c("E1 abandon succeeds between floors", res.success, res.message);
    c("E1 abandon releases isolation (AWAKE, no battle)", h?.status === "AWAKE" && h.battleId === null, h?.status);
    c("E1 attempt closed uncompleted", hist.length === 1 && hist[0]!.completed === 0 && !!hist[0]!.endAt);
    c("E1 Beacon not refunded", (await beacons()) === before.beacons && before.beacons === 2, before);
    c("E1 no quest reward", (await payouts()) === 0);
    c("E1 pools not restored by abandonment", h?.curHealth === before.hp && h.curHealth === pools.health, { hp: h?.curHealth });
    const late = await choose("b2.n.f2");
    c("E1 abandoned run cannot progress", !late.success || (await currentBattle()) === null, late.message);
    expect(res.success).toBe(true);
  }, 300_000);

  it("E2 abandonment is refused during a live battle", async () => {
    await resetWorld();
    await start();
    await choose("b1.n.f1");
    const res = await (await api()).quests.abandon({ id: QUEST_ID });
    c("E2 abandon refused mid-battle", !res.success, res.message);
    c("E2 battle and run intact", (await currentBattle()) !== null && (await history())[0]!.endAt === null);
  }, 120_000);

  it("E3 out-of-order and premature dialog choices are inert", async () => {
    await resetWorld();
    await start();
    const probes = ["b1.n.f2", "b1.n.boss.clean", "d1.n.boss.medical", "b5.n.f1", "b1.r.f1", "w.complete", "d2.n.f1"];
    for (const p of probes) {
      const res = await choose(p);
      const view = await engineView();
      c(`E3 choosing '${p}' at the root starts nothing and moves nothing`, (await currentBattle()) === null && view.active === "d1.n.f1" && (await payouts()) === 0, { success: res.success, view });
    }
    c("E3 Beacon untouched before the first battle", (await beacons()) === 3);
    await choose("b1.n.f1");
    const during = await choose("b1.n.f2");
    const t = await tracker();
    c("E3 continuing past a live battle is rejected", !during.success && !t?.goals.find((g) => g.id === "d1.n.f2")?.done, during.message);
    await settle(false, pools);
    await refresh();
    for (const p of ["b1.n.f2", "b1.n.boss.combat", "b2.n.f1"]) {
      await choose(p);
      const view = await engineView();
      c(`E3 after an initial loss, '${p}' does not resume the abandoned initial lane`, view.active === "d1.r.f1" && (await currentBattle()) === null, view);
    }
  }, 120_000);

  it("E4 missing Beacon: the first battle does not start (observed engine behaviour recorded)", async () => {
    await resetWorld({ beaconCount: 0 });
    const s = await start();
    ev.put("E4.startQuestWithoutBeacon", { success: s.success, message: s.message });
    ev.finding("F2", "startQuest admits an isolated entry-item Pyramid without the entry item; the Beacon is first checked at the first battle", s.success, s.message);
    const first = await choose("b1.n.f1");
    const noBattle = (await currentBattle()) === null;
    c("E4 first battle refused without a Beacon", noBattle, first);
    ev.put("E4.firstChoice", { success: first.success, notifications: (first as { notifications?: string[] }).notifications });
    const view1 = await engineView();
    ev.put("E4.viewAfterRefusedBattle", view1);
    // Probe: is the dialog after the un-fought battle reachable while that battle is open?
    const skip = await choose("b1.n.f2");
    const t = await tracker();
    const view2 = await engineView();
    const skipped = !!t?.goals.find((g) => g.id === "d1.n.f2")?.done;
    ev.put("E4.skipProbe", { success: skip.success, message: skip.message, d1n2Done: skipped, view: view2, battle: !!(await currentBattle()) });
    c("E4 no battle can start without a Beacon even via the skip probe", (await currentBattle()) === null);
    // Now supply a Beacon and refresh: which battle does the engine start?
    await (await db()).insert(userItem).values({ id: "late-beacon", userId: "sb-hero", itemId: "sb-skyglass-signal-beacon", quantity: 1 } as never);
    await refresh();
    const snap = await currentBattle();
    ev.put("E4.afterLateBeacon", { battleObjective: snap?.extraState.questBattleSource?.objectiveId ?? null, d1n2Done: skipped });
    if (snap) {
      await settle(true, pools);
      await refresh();
      const after = await currentBattle();
      ev.put("E4.afterWinningThatBattle", { autoStartedBattle: after?.extraState.questBattleSource?.objectiveId ?? null, view: await engineView() });
    }
  }, 120_000);

  it("E4b missing Beacon: how far dialogs can be pre-completed and whether battles then chain", async () => {
    await resetWorld({ beaconCount: 0 });
    await start();
    // Walk the whole Division I initial lane by dialog choices only (Combat route), then Division II.
    const walk = ["b1.n.f1", "b1.n.f2", "b1.n.f3", "d1.n.f4", "b1.n.f4", "b1.n.boss.combat", "b2.n.f1", "b2.n.f2"];
    const accepted: string[] = [];
    for (const step of walk) {
      const before = (await tracker())?.goals.filter((g) => g.done).length ?? 0;
      await choose(step);
      const after = (await tracker())?.goals.filter((g) => g.done).length ?? 0;
      if (after > before) accepted.push(step);
    }
    const doneDialogs = (await tracker())?.goals.filter((g) => g.done).map((g) => g.id) ?? [];
    ev.put("E4b.dialogStepsAcceptedWithoutAnyBattle", accepted);
    ev.put("E4b.doneObjectivesWithoutAnyBattle", doneDialogs);
    c("E4b no battle ran and no Beacon was charged", (await currentBattle()) === null && (await beacons()) === 0);
    await (await db()).insert(userItem).values({ id: "late-beacon", userId: "sb-hero", itemId: "sb-skyglass-signal-beacon", quantity: 1 } as never);
    const chain: (string | null)[] = [];
    for (let i = 0; i < 8; i++) {
      await refresh();
      const snap = await currentBattle();
      chain.push(snap?.extraState.questBattleSource?.objectiveId ?? null);
      if (!snap) break;
      await settle(true, pools);
    }
    ev.put("E4b.battlesStartedByPageRefreshAloneAfterBeacon", chain);
    ev.put("E4b.finalView", await engineView());
    const bossBeforeF4 = chain.indexOf("b1.n.boss.combat") >= 0 && chain.indexOf("b1.n.boss.combat") < chain.indexOf("b1.n.f4");
    c("E4b r2: in the missing-Beacon window the fourth fight still precedes the commander", !bossBeforeF4, chain);
    ev.finding("F1", "Missing-Beacon window: dialogs after an unstarted battle can be completed and battles later chain by page refresh without dialog gates",
      accepted.length > 1 && chain.filter(Boolean).length > 1, { dialogStepsAccepted: accepted.length, autoChained: chain.filter(Boolean), bossBeforeF4 });
  }, 300_000);

  it("E5 no automatic resource recovery between floors or while paused", async () => {
    await resetWorld();
    await start();
    await choose("b1.n.f1");
    await settle(true, pools);
    const old = new Date(Date.now() - 6 * 3600_000);
    await (await db()).update(userData).set({ regenAt: old }).where(eq(userData.userId, "sb-hero"));
    await refresh();
    const h = await hero();
    c("E5 six hours between floors: HP/CP/SP unchanged", h?.curHealth === pools.health && h.curChakra === pools.chakra && h.curStamina === pools.stamina, { hp: h?.curHealth, cp: h?.curChakra, sp: h?.curStamina });
    await choose("b1.n.f2");
    const p = (await currentBattle())?.usersState.find((u) => u.userId === "sb-hero");
    c("E5 next floor starts with the carried pools", p?.curHealth === pools.health && p.curChakra === pools.chakra && p.curStamina === pools.stamina, { hp: p?.curHealth });
  }, 120_000);

  it("E6 hidden pause and content-version change", async () => {
    await resetWorld();
    await start();
    await choose("b1.n.f1");
    await settle(true, pools);
    await (await db()).update(quest).set({ hidden: true }).where(eq(quest.id, QUEST_ID));
    const paused = await choose("b1.n.f2");
    c("E6 hidden quest pauses the run (continuation rejected)", !paused.success && (await currentBattle()) === null, paused.message);
    await refresh();
    c("E6 paused run keeps its checkpoint tracker", (await tracker())?.goals.find((g) => g.id === "b1.n.f1")?.done === true);
    await (await db()).update(quest).set({ hidden: false }).where(eq(quest.id, QUEST_ID));
    const resumed = await choose("b1.n.f2");
    c("E6 unhiding resumes at the same objective", resumed.success && (await currentBattle())?.extraState.questBattleSource?.objectiveId === "b1.n.f2", resumed.message);
    await settle(true, pools);
    const row = await questRow();
    await (await db()).update(quest).set({ updatedAt: new Date(row.updatedAt.getTime() + 5000) }).where(eq(quest.id, QUEST_ID));
    const changed = await choose("b1.n.f3");
    c("E6 edited content blocks the old run", !changed.success, changed.message);
    const ab = await (await api()).quests.abandon({ id: QUEST_ID });
    c("E6 edited run can be abandoned", ab.success && (await hero())?.status === "AWAKE", ab.message);
  }, 120_000);

  it("E7 the real content-editor save procedure accepts the 178-objective record (hidden)", async () => {
    await resetWorld();
    const rec = questRecord();
    const data = QuestValidator.parse({ ...rec, hidden: true });
    const editor = await callerFor(questsRouter, EDITOR);
    const t0 = performance.now();
    const res = await editor.update({ id: QUEST_ID, data });
    ev.timing("E7.updateMs", performance.now() - t0);
    c("E7 quests.update succeeds", res.success, res.message);
    const saved = await questRow();
    c("E7 saved record keeps 178 objectives in order", saved.content.objectives.length === 178 && saved.content.objectives.map((o) => o.id).join() === rec.content.objectives.map((o) => o.id).join());
    c("E7 saved record stays hidden", saved.hidden === true);
    ev.put("E7.savedContentBytes", JSON.stringify(saved.content).length);
    const visible = await editor.update({ id: QUEST_ID, data: QuestValidator.parse({ ...rec, hidden: false }) });
    ev.put("E7.visibleSaveWithoutSceneCharacters", { success: visible.success, message: visible.message });
  }, 120_000);

  it("E8 performance at the deepest pre-completion state", async () => {
    await resetWorld();
    const r = new Runner(ev, { name: "E8", divisions: [], expect: "complete" });
    const t0 = performance.now();
    await r.start();
    for (let d = 1; d <= 5; d++) await r.lane(d, "n", { route: "medical" });
    ev.timing("E8.fullMedicalRunMs", performance.now() - t0);
    // Timing below is at 178 objectives (r2).
    const { user } = await refresh();
    const N = 200;
    const t1 = performance.now();
    for (let i = 0; i < N; i++) getNewTrackers(structuredClone(user!), [{ task: "any" }]);
    ev.timing("E8.getNewTrackersMsPerCall", (performance.now() - t1) / N);
    const t2 = performance.now();
    for (let i = 0; i < 10; i++) await refresh();
    ev.timing("E8.fetchUpdatedUserMsPerCall", (performance.now() - t2) / 10);
    const t = await tracker();
    ev.put("E8.trackerGoalsAtDeepestPoint", t?.goals.length);
    ev.timing("E8.questDataBytes", JSON.stringify((await hero())!.questData).length);
    c("E8 deepest state reached (aftermath active)", (await engineView()).active === "d.aftermath");
    c("E8 25 battles on the full Medical route", r.battles === 25, r.battles);
    // Timing values live only in e_edges.timings.json so the evidence file stays deterministic.
    c("E8 getNewTrackers on 178 objectives under 50 ms/call", (ev.volatile["E8.getNewTrackersMsPerCall"] as number) < 50);
  }, 600_000);

  it("E9 retry loop: ordinary battle settlement income on repeated regular wins (economy observation)", async () => {
    await resetWorld();
    const r = new Runner(ev, { name: "E9", divisions: [], expect: "fail" });
    await r.start();
    await r.lane(1, "n", { route: "clean", lossAt: "f1" });
    const loops: { money: number; experience: number }[] = [];
    for (let i = 0; i < 3; i++) {
      const before = (await hero())!;
      await r.lane(1, "r", { route: "clean", lossAt: "boss" });
      const after = (await hero())!;
      loops.push({ money: after.money - before.money, experience: after.experience - before.experience });
    }
    // Engine battle ryo is randomised: raw amounts go to the volatile timings file only.
    ev.timing("E9.rawPerLoopDelta", loops);
    ev.put("E9.perLoop(3 regular wins + 1 commander loss)", loops.map((l) => ({ experienceGained: l.experience, ryoGained: l.money > 0 })));
    c("E9 still one Beacon charged after 3 deliberate loops", (await beacons()) === 2);
    c("E9 no quest reward from loops", (await payouts()) === 0);
    ev.finding("F3", "Deliberate Division I–IV commander losses re-run already-won regular fights; each win pays ordinary battle settlement income on one Beacon (economy decision, user-owned)",
      loops.every((l) => l.money > 0 || l.experience > 0), { loops: loops.length, everyLoopPaidIncome: true });
  }, 300_000);

  requireClean(ev);
});
