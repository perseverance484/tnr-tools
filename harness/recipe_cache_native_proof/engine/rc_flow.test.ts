/**
 * Gate F — the approved alt99_f4gate Battle Pyramid × quest-level one-of-two reward choice ×
 * Weighted Cache opening, through the real routers on a throwaway MySQL (no network).
 */
import { beforeEach, expect, it, vi } from "bun:test";
import { and, eq } from "drizzle-orm";
import { actionLog, item, userItem } from "@/drizzle/schema";
import { Pusher } from "@/libs/pusher";
import { fetchItemWithCraftingRequirements, itemRouter } from "@/server/api/routers/item";
import { ItemValidator } from "@/validators/combat";
import { questsRouter } from "@/server/api/routers/quests";
import type { DrizzleClient } from "@/server/db";
import { QuestValidator } from "@/validators/objectives";
import { callerFor, callerForDatabase, describeWithDatabase } from "../setup/testDatabase";
import { api, beacons, choose, currentBattle, db, EDITOR, engineView, hero, history, HERO, settle } from "./lib/driver";
import { compileObjectives, QUEST_ID } from "./lib/graph";
import { Evidence, requireClean } from "./lib/report";
import { DIVS, type Plan, Runner } from "./lib/run99";
import { ARSENAL, BUNDLES, cacheEffect, caches, choiceRecord, ING, ingredients, pendingOffer, RESEARCH, resetCacheWorld } from "./lib/cachefix";

const ev = new Evidence("f_flow");
const c = (n: string, p: boolean, d?: unknown) => ev.check(n, p, d);
const CARD = { [ARSENAL]: `reward_items:0:${ARSENAL}`, [RESEARCH]: `reward_items:1:${RESEARCH}` } as const;
const plan = (name: string): Plan => ({ name, divisions: [], expect: "complete" });

/** Win every division on the given routes (optionally with losses), stopping at d.aftermath. */
const playToAftermath = async (r: Runner, segs: Parameters<Runner["division"]>[1][] = DIVS.map(() => [{ route: "clean" as const }])) => {
  for (let i = 0; i < DIVS.length; i++) {
    await r.division(DIVS[i]!, segs[i]!);
    c(`${r.plan.name}: no offer and no cache after D${DIVS[i]}`, (await pendingOffer()).length === 0 && (await caches()).arsenal + (await caches()).research === 0);
  }
  c(`${r.plan.name}: aftermath active before the win objective`, (await engineView()).active === "d.aftermath");
};
const complete = async (name: string) => {
  const res = await choose("w.complete");
  c(`${name}: w.complete resolves the quest`, res.success && (res as { resolved?: boolean }).resolved === true, res.message);
  return res;
};
const quests = async () => (await api()).quests;
const claim = async (cardId: string) => {
  const offer = (await pendingOffer())[0] as { id: string } | undefined;
  return (await quests()).claimRewardChoice({ questId: QUEST_ID, choiceId: offer?.id ?? "none", cardIds: [cardId] });
};
const stackOf = async (itemId: string) =>
  (await (await db()).query.userItem.findFirst({ where: and(eq(userItem.userId, HERO), eq(userItem.itemId, itemId)) }))?.id;
const consume = async (userItemId: string, requestId: string, client?: DrizzleClient) =>
  callerForDatabase(itemRouter, HERO, client ?? (await db())).consume({ userItemId, requestId });
const bundleKeys = (id: keyof typeof BUNDLES) => [...BUNDLES[id].Epic, ...BUNDLES[id].Legendary].map((b) => JSON.stringify(Object.fromEntries([...b].map((x) => [x.itemId, x.quantity]).sort())));
const gained = (before: Record<string, number>, after: Record<string, number>) =>
  JSON.stringify(Object.fromEntries(Object.keys(after).filter((k) => after[k]! - before[k]! !== 0).map((k) => [k, after[k]! - before[k]!]).sort()));

describeWithDatabase("F: Pyramid reward choice and cache opening", () => {
  beforeEach(() => { vi.spyOn(Pusher.prototype, "trigger").mockResolvedValue(undefined); });

  it("F1 the real editor save accepts the 99-objective choose record (hidden)", async () => {
    await resetCacheWorld();
    const res = await (await callerFor(questsRouter, EDITOR)).update({ id: QUEST_ID, data: QuestValidator.parse(choiceRecord()) });
    c("F1 quests.update succeeds", res.success, res.message);
    const saved = await (await db()).query.quest.findFirst({ where: (q, { eq: e }) => e(q.id, QUEST_ID) });
    const content = saved!.content as unknown as Record<string, unknown> & { reward: { reward_items: { ids: string[] }[] }; objectives: { id: string }[] };
    c("F1 saved: hidden, choose, pick 1, two quest-level cache entries, 99 objectives", saved!.hidden && content.rewardMode === "choose" && content.rewardPickCount === 1 &&
      content.reward.reward_items.map((r) => r.ids.join()).join("|") === `${ARSENAL}|${RESEARCH}` && content.objectives.length === 99,
      { hidden: saved!.hidden, mode: content.rewardMode, pick: content.rewardPickCount });
    for (const id of [ARSENAL, RESEARCH]) {
      const row = await fetchItemWithCraftingRequirements(await db(), id);
      const parsed = ItemValidator.safeParse({ ...row, cost: 1, target: "SELF", method: "SINGLE" });
      c(`F1 ItemValidator accepts stored ${id} (CONSUMABLE, destroyOnUse, preventBattleUsage, weightedCache)`, parsed.success, parsed.success ? undefined : parsed.error.issues.slice(0, 4));
    }
  }, 120_000);

  it("F2 clean run: one frozen one-of-two offer after w.complete; Arsenal claimed once", async () => {
    await resetCacheWorld();
    const r = new Runner(ev, plan("F2"));
    await r.start();
    c("F2 Beacon charged once at start", (await beacons()) === 2);
    await playToAftermath(r);
    await complete("F2");
    const offers = await pendingOffer();
    const offer = offers[0] as { id: string; pickCount: number; cards: { id: string; contentId?: string; amount: number }[] } | undefined;
    ev.put("F2.offer", offer ? { pickCount: offer.pickCount, cards: offer.cards.map((x) => ({ id: x.id, contentId: x.contentId, amount: x.amount })) } : null);
    c("F2 exactly one stored offer: pick 1 of the two cache cards", offers.length === 1 && offer!.pickCount === 1 && offer!.cards.map((x) => x.id).sort().join() === [CARD[ARSENAL], CARD[RESEARCH]].sort().join());
    c("F2 no cache auto-granted at completion", (await caches()).arsenal === 0 && (await caches()).research === 0);
    const listed = await (await quests()).getPendingRewardChoices();
    ev.put("F2.apiView", listed.map((l) => ({ questName: l.questName, pickCount: l.pickCount, cards: l.cards.map((x) => ({ name: x.name, amount: x.amount, rarity: (x as { rarity?: string }).rarity })) })));
    c("F2 getPendingRewardChoices lists both cache names for the player UI", listed.length === 1 && listed[0]!.cards.map((x) => x.name).sort().join() === "Synthetic Arsenal Cache,Synthetic Research Cache");
    const two = await (await quests()).claimRewardChoice({ questId: QUEST_ID, choiceId: offer!.id, cardIds: [CARD[ARSENAL], CARD[RESEARCH]] });
    c("F2 picking both cards is rejected", !two.success && (await caches()).arsenal === 0, two.message);
    const ok = await claim(CARD[ARSENAL]);
    c("F2 claim Arsenal succeeds: 1 Arsenal, 0 Research, offer consumed", ok.success && (await caches()).arsenal === 1 && (await caches()).research === 0 && (await pendingOffer()).length === 0, ok.message);
    const again = await (await quests()).claimRewardChoice({ questId: QUEST_ID, choiceId: offer!.id, cardIds: [CARD[ARSENAL]] });
    const other = await (await quests()).claimRewardChoice({ questId: QUEST_ID, choiceId: offer!.id, cardIds: [CARD[RESEARCH]] });
    c("F2 replayed and switched claims rejected; totals unchanged", !again.success && !other.success && (await caches()).arsenal === 1 && (await caches()).research === 0);
    const h = await hero();
    c("F2 isolation released after completion", h?.status === "AWAKE");
  }, 600_000);

  it("F3 parallel claims on a fresh completion pay Research exactly once", async () => {
    await resetCacheWorld();
    const r = new Runner(ev, plan("F3"));
    await r.start(); await playToAftermath(r, DIVS.map((_, i) => [{ route: (["medical", "combat", "alert", "clean"] as const)[i]! }])); await complete("F3");
    const offer = (await pendingOffer())[0] as { id: string };
    const results = await Promise.all(Array.from({ length: 5 }, async () =>
      (await quests()).claimRewardChoice({ questId: QUEST_ID, choiceId: offer.id, cardIds: [CARD[RESEARCH]] })));
    c("F3 one of five parallel claims succeeds", results.filter((x) => x.success).length === 1, results.map((x) => x.success));
    c("F3 inverse grant: 0 Arsenal, 1 Research", (await caches()).arsenal === 0 && (await caches()).research === 1);
  }, 600_000);

  it("F4 opening: coherent bundle, receipt replay, concurrency, rollback, invalid config", async () => {
    await resetCacheWorld();
    const r = new Runner(ev, plan("F4"));
    await r.start(); await playToAftermath(r); await complete("F4");
    await claim(CARD[ARSENAL]);
    // Battle-usage and isolation: start a second attempt and try to open the cache inside it.
    const stack = (await stackOf(ARSENAL))!;
    const r2 = new Runner(ev, plan("F4-run2"));
    await r2.start();
    const between = await consume(stack, "open-during-isolated-run");
    await choose("b2.n.f1");
    const inBattle = await consume(stack, "open-during-pyramid-battle");
    c("F4 cache cannot be opened inside an isolated run (between floors or in battle)", !between.success && !inBattle.success && (await caches()).arsenal === 1,
      { between: between.message, inBattle: inBattle.message });
    await settle(true, { health: 900, chakra: 1000, stamina: 800 });
    await (await quests()).abandon({ id: QUEST_ID });
    c("F4 abandoned second attempt: no offer, no refund (2 Beacons spent of 3)", (await pendingOffer()).length === 0 && (await beacons()) === 1);
    // Normal opening with receipt.
    const before = await ingredients();
    const first = await consume(stack, "open-arsenal-request-0001");
    const after = await ingredients();
    c("F4 consume succeeds and destroys one cache", first.success && (await caches()).arsenal === 0, first.message);
    const g = gained(before, after);
    // The roll is random by design: the drawn bundle goes to the volatile file only.
    ev.timing("F4.grantedBundle", JSON.parse(g));
    c("F4 granted exactly one whole Arsenal bundle, nothing from Research", bundleKeys(ARSENAL).includes(g) && !bundleKeys(RESEARCH).includes(g), g);
    const replay = await consume(stack, "open-arsenal-request-0001");
    c("F4 replay with the same requestId returns the stored receipt, no second grant", JSON.stringify(replay) === JSON.stringify(first) && gained(after, await ingredients()) === "{}");
    const logs = (await (await db()).select().from(actionLog)).filter((l) => JSON.stringify(l.changes).includes("selections"));
    const sel = logs.map((l) => JSON.parse((l.changes as string[])[0]!).selections);
    ev.timing("F4.receiptSelections", sel);
    const one = sel[0]?.[0] as { rollCount?: number; selections?: { tierName: string; entryIndex: number; items: unknown[] }[] } | undefined;
    c("F4 receipt records one roll with its tier, entry index and the exact bundle granted", !!one && one.rollCount === 1 && one.selections?.length === 1 &&
      JSON.stringify(Object.fromEntries((one.selections[0]!.items as { itemId: string; quantity: number }[]).map((x) => [x.itemId, x.quantity]).sort())) === g, one);
    c("F4 one audit receipt recording tier and entry", logs.length === 1);
    const empty = await consume(stack, "open-arsenal-request-0002");
    c("F4 a new request on the emptied stack fails", !empty.success);
    // Concurrency on a single cache with distinct requests.
    await (await db()).insert(userItem).values({ id: "rc-two", userId: HERO, itemId: RESEARCH, quantity: 1 } as never);
    const b2 = await ingredients();
    const par = await Promise.all(["par-request-aaaa", "par-request-bbbb"].map((rid) => consume("rc-two", rid)));
    const g2 = gained(b2, await ingredients());
    c("F4 two distinct concurrent requests on one cache: one success, one bundle", par.filter((x) => x.success).length === 1 && bundleKeys(RESEARCH).includes(g2), { results: par.map((x) => x.success), g2 });
    // Rollback on an injected grant failure.
    await (await db()).insert(userItem).values({ id: "rc-three", userId: HERO, itemId: RESEARCH, quantity: 1 } as never);
    const d0 = await db();
    const failing = new Proxy(d0, { get(t, p, rcv) {
      if (p === "transaction") return (cb: (tx: DrizzleClient) => Promise<unknown>) => t.transaction(async (tx) => cb(new Proxy(tx, { get(x, k, rr) {
        if (k === "insert") return (table: typeof userItem) => { if (table === userItem) throw new Error("Injected grant failure"); return x.insert(table); };
        return Reflect.get(x, k, rr); } }) as unknown as DrizzleClient));
      return Reflect.get(t, p, rcv); } }) as DrizzleClient;
    const b3 = await ingredients();
    let threw = false;
    try { await consume("rc-three", "rollback-request-01", failing); } catch { threw = true; }
    c("F4 injected grant failure rolls back: cache kept, nothing granted", threw && (await caches()).research === 1 && gained(b3, await ingredients()) === "{}");
    const retry = await consume("rc-three", "rollback-request-01");
    c("F4 retry after rollback succeeds once", retry.success && (await caches()).research === 0);
    // Invalid stored configuration and missing reference are refused before consuming.
    await (await db()).insert(userItem).values({ id: "rc-four", userId: HERO, itemId: RESEARCH, quantity: 1 } as never);
    const bad = cacheEffect(RESEARCH); bad.weightedCache!.rolls[0]!.probability = 9_999;
    await (await db()).update(item).set({ effects: [bad] as never }).where(eq(item.id, RESEARCH));
    const invalid = await consume("rc-four", "invalid-config-req1");
    await (await db()).update(item).set({ effects: [cacheEffect(RESEARCH)] as never }).where(eq(item.id, RESEARCH));
    await (await db()).delete(item).where(eq(item.id, ING.dustB));
    const missing = await consume("rc-four", "missing-ref-req-01");
    c("F4 invalid roll sum and missing ingredient both refused, cache kept", !invalid.success && !missing.success && (await caches()).research === 1, { invalid: invalid.message, missing: missing.message });
  }, 900_000);

  it("F5 failed and abandoned attempts: no offer, no cache, no refund; recovery loops still pay once", async () => {
    await resetCacheWorld();
    const r = new Runner(ev, { name: "F5a", divisions: [], expect: "fail" });
    await r.start();
    for (const d of [2, 3, 4]) await r.division(d, [{ route: "clean" }]);
    const out = await r.division(5, [{ route: "medical", lossAt: "boss" }]);
    c("F5 Arakane loss ends the attempt with no offer and no cache", out === "failed" && (await pendingOffer()).length === 0 && (await caches()).arsenal + (await caches()).research === 0 && (await history())[0]!.completed === 0);
    c("F5 no Beacon refund after failure", (await beacons()) === 2);
    const r2 = new Runner(ev, plan("F5b"));
    await r2.start();
    await r2.division(2, [{ route: "clean" }]);
    const ab = await (await quests()).abandon({ id: QUEST_ID });
    c("F5 abandoned attempt: no offer, no cache, no refund", ab.success && (await pendingOffer()).length === 0 && (await caches()).arsenal + (await caches()).research === 0 && (await beacons()) === 1);
    const r3 = new Runner(ev, plan("F5c"));
    await r3.start();
    await playToAftermath(r3, [
      [{ route: "clean", lossAt: "f1", recoveryLosses: 1 }, { route: "alert", lossAt: "f3", recoveryLosses: 1 }, { route: "medical" }],
      [{ route: "combat", lossAt: "boss" }, { route: "clean" }],
      [{ route: "medical", lossAt: "f4" }, { route: "combat" }],
      [{ route: "alert", lossAt: "f2", recoveryLosses: 1 }, { route: "clean" }],
    ]);
    c("F5 recovery loops and resets create no offer before completion", (await pendingOffer()).length === 0);
    c("F5 three attempts used exactly three Beacons", (await beacons()) === 0);
    await complete("F5c");
    c("F5 one completion after many losses = one offer", (await pendingOffer()).length === 1 && (await caches()).arsenal + (await caches()).research === 0);
  }, 900_000);

  it("F6 an unclaimed offer blocks a second completion until it is claimed", async () => {
    await resetCacheWorld({ beaconCount: 3 });
    const r = new Runner(ev, plan("F6"));
    await r.start(); await playToAftermath(r); await complete("F6");
    const r2 = new Runner(ev, plan("F6-run2"));
    const s2 = await (await quests()).startQuest({ questId: QUEST_ID, userSector: 0 });
    ev.put("F6.startWithUnclaimedOffer", { success: s2.success, message: s2.message, beaconsAfter: await beacons() });
    let second: unknown = null;
    if (s2.success) {
      r2.beaconsBefore = (await beacons()) + 1;
      const h1 = (await hero())!;
      r2.carry = { health: h1.curHealth, chakra: h1.curChakra, stamina: h1.curStamina };
      for (const d of DIVS) await r2.division(d, [{ route: "clean" }]);
      const res = await choose("w.complete");
      second = { success: res.success, resolved: (res as { resolved?: boolean }).resolved ?? false, message: res.message, offers: (await pendingOffer()).length, view: await engineView() };
    }
    ev.put("F6.secondCompletionWhileUnclaimed", second);
    c("F6 never two offers or a silent second payout", (await pendingOffer()).length === 1 && (await caches()).arsenal + (await caches()).research === 0);
    ev.finding("RC1", "startQuest admits a new attempt (charging a Beacon) while the previous completion's cache choice is unclaimed; that attempt can never resolve (REWARD_CHOICE_PENDING_MESSAGE at w.complete) and the claim is refused while isolated, so the player must abandon it and lose that Beacon",
      !!second && !(second as { resolved: boolean }).resolved, second);
    const inRun = await claim(CARD[ARSENAL]);
    ev.put("F6.claimWhileSecondRunIsolated", { success: inRun.success, message: inRun.message, status: (await hero())?.status });
    if (s2.success && !inRun.success) {
      // Way out observed: abandon the stuck second run (its Beacon is not refunded), then claim.
      const ab = await (await quests()).abandon({ id: QUEST_ID });
      ev.put("F6.abandonStuckRun", { success: ab.success, message: ab.message });
    }
    const ok = inRun.success ? inRun : await claim(CARD[ARSENAL]);
    c("F6 the first offer can still be claimed exactly once", ok.success && (await caches()).arsenal === 1 && (await caches()).research === 0, ok.message);
    ev.put("F6.beaconsAtEnd", await beacons());
  }, 900_000);

  it("F7 NEGATIVE CONTROL: caches on w.complete bypass the choice and pay both", async () => {
    await resetCacheWorld({ directOnWin: true });
    const r = new Runner(ev, plan("F7"));
    await r.start(); await playToAftermath(r); await complete("F7");
    const got = await caches();
    ev.put("F7.directOnWin", { ...got, offers: (await pendingOffer()).length });
    c("F7 objective-level cache rewards grant both caches with no choice (why the brief forbids it)", got.arsenal === 1 && got.research === 1 && (await pendingOffer()).length === 0, got);
  }, 600_000);

  requireClean(ev);
});
