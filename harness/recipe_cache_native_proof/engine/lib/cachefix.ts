/**
 * Synthetic reward-choice + Weighted Cache fixture on the approved alt99_f4gate Pyramid.
 *
 * Everything here is SYNTHETIC: two cache items, six ordinary scratch ingredients, two recipe-shaped
 * bundles per cache, illustrative weights. None of it is a recipe shortlist, quantity, weight,
 * rarity or name proposal (RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_PROOF_BRIEF_20261016.md).
 */
import { eq } from "drizzle-orm";
import { item, quest, questHistory, userItem } from "@/drizzle/schema";
import { NonCombatConsumeRewardTag } from "@/validators/combat";
import { ObjectiveReward } from "@/validators/rewards";
import { insertItems } from "../../setup/factories";
import { db, HERO, questRow, resetWorld } from "./driver";
import { compileObjectives, QUEST_ID, questRecord } from "./graph";

export const ARSENAL = "rc-synthetic-arsenal-cache";
export const RESEARCH = "rc-synthetic-research-cache";
/** Scratch ordinary ingredients (visible, tradeable, no bloodline/reputation links). */
export const ING = {
  oreA: "rc-ing-ore-a", hideA: "rc-ing-hide-a", oreB: "rc-ing-ore-b",
  dustA: "rc-ing-dust-a", herbA: "rc-ing-herb-a", dustB: "rc-ing-dust-b",
} as const;

/** Two recipe-shaped bundles per cache; a tier picks one bundle uniformly. */
export const BUNDLES = {
  [ARSENAL]: {
    Epic: [[{ itemId: ING.oreA, quantity: 5 }, { itemId: ING.hideA, quantity: 3 }]],
    Legendary: [[{ itemId: ING.oreB, quantity: 2 }, { itemId: ING.hideA, quantity: 1 }, { itemId: ING.oreA, quantity: 1 }]],
  },
  [RESEARCH]: {
    Epic: [[{ itemId: ING.dustA, quantity: 4 }, { itemId: ING.herbA, quantity: 4 }], [{ itemId: ING.dustB, quantity: 3 }, { itemId: ING.herbA, quantity: 2 }]],
    Legendary: [[{ itemId: ING.dustB, quantity: 6 }, { itemId: ING.dustA, quantity: 2 }]],
  },
} as const;

export const cacheEffect = (cacheId: keyof typeof BUNDLES, over: { rolls?: { count: number; probability: number }[]; epic?: number } = {}) =>
  NonCombatConsumeRewardTag.parse({
    rewardMode: "weightedCache",
    weightedCache: {
      version: 1,
      displayName: cacheId === ARSENAL ? "Synthetic Arsenal Cache" : "Synthetic Research Cache",
      rolls: over.rolls ?? [{ count: 1, probability: 10_000 }],
      tiers: [
        { name: "Epic", probability: over.epic ?? 7_500, entries: BUNDLES[cacheId].Epic.map((b) => ({ items: b.map((x) => ({ ...x })) })) },
        { name: "Legendary", probability: 10_000 - (over.epic ?? 7_500), entries: BUNDLES[cacheId].Legendary.map((b) => ({ items: b.map((x) => ({ ...x })) })) },
      ],
    },
  });

export const cacheItemRow = (id: keyof typeof BUNDLES) => ({
  id, name: id === ARSENAL ? "Synthetic Arsenal Cache" : "Synthetic Research Cache",
  itemType: "CONSUMABLE" as const, rarity: "EPIC" as const, destroyOnUse: true, preventBattleUsage: true,
  canStack: true, stackSize: 10, effects: [cacheEffect(id)],
});

/** Quest-level one-of-two choice; nothing on w.complete. */
export const choiceReward = () => ObjectiveReward.parse({
  reward_items: [{ ids: [ARSENAL], number: 100, quantity: 1 }, { ids: [RESEARCH], number: 100, quantity: 1 }],
});
export const choiceRecord = () => {
  const rec = questRecord();
  return { ...rec, hidden: true, content: { ...rec.content, reward: choiceReward(), rewardMode: "choose" as const, rewardPickCount: 1 } };
};

/** Fresh world (driver.resetWorld) + synthetic items + the choice quest content in place. */
export const resetCacheWorld = async (opts: { beaconCount?: number; directOnWin?: boolean } = {}) => {
  await resetWorld({ beaconCount: opts.beaconCount });
  await insertItems([
    cacheItemRow(ARSENAL), cacheItemRow(RESEARCH),
    ...Object.values(ING).map((id) => ({ id, name: `Scratch ${id.slice(7)}`, itemType: "MATERIAL" as const, canStack: true, stackSize: 100 })),
  ] as never);
  const rec = choiceRecord();
  let content = { ...rec.content, objectives: compileObjectives() };
  if (opts.directOnWin) {
    // NEGATIVE CONTROL ONLY: caches on the win_quest objective instead of the quest-level choice.
    content = { ...content, rewardMode: "all" as never, reward: ObjectiveReward.parse({}),
      objectives: content.objectives.map((o) => (o.id === "w.complete" ? { ...o, reward_items: choiceReward().reward_items } : o)) as never };
  }
  // The fixture plays the quest unhidden; E-style save tests use the real editor procedure separately.
  await (await db()).update(quest).set({ content: content as never, hidden: false }).where(eq(quest.id, QUEST_ID));
};

export const held = async (itemId: string) =>
  (await (await db()).query.userItem.findMany({ where: eq(userItem.userId, HERO) })).filter((r) => r.itemId === itemId).reduce((s, r) => s + r.quantity, 0);
export const caches = async () => ({ arsenal: await held(ARSENAL), research: await held(RESEARCH) });
export const ingredients = async () => Object.fromEntries(await Promise.all(Object.values(ING).map(async (id) => [id, await held(id)])));
export const pendingOffer = async () =>
  (await (await db()).query.questHistory.findMany({ where: eq(questHistory.userId, HERO) })).map((h) => h.pendingRewardChoice).filter(Boolean);
export const itemExists = async (id: string) => !!(await (await db()).query.item.findFirst({ where: eq(item.id, id) }));
export { questRow };
