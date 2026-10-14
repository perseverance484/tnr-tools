/**
 * Real-router driver for the offline Phase 1 fixture.
 *
 * Every step goes through pinned engine code against a throwaway local MySQL (unix socket, no
 * TCP, network namespace without interfaces):
 *   startQuest → checkRewards(dialog choice) → fetchUpdatedUser (quest consequences →
 *   initiateBattle) → battle settlement with the upstream test pattern
 *   (calcBattleResult + combat/database.updateUser, as tests/server/api/quests.persistentBattle)
 *   → fetchUpdatedUser (reset_quest / fail_quest consequences).
 * The driver chooses dialog options and battle outcomes; it never writes quest trackers.
 */
import { eq } from "drizzle-orm";
import { vi } from "bun:test";
import { aiProfile, battle, battleHistory, item, quest, questHistory, userData, userItem } from "@/drizzle/schema";
import { updateUser } from "@/libs/combat/database";
import { calcBattleResult } from "@/libs/combat/util";
import { getActiveObjective, isQuestObjectiveAvailable } from "@/libs/objectives";
import type { PusherClient } from "@/libs/pusher";
import { combatRouter, fetchBattle } from "@/server/api/routers/combat";
import { fetchUpdatedUser } from "@/server/api/routers/profile";
import { questsRouter } from "@/server/api/routers/quests";
import { createTRPCRouter } from "@/server/api/trpc";
import type { Quest } from "@/drizzle/schema";
import type { QuestTrackerType } from "@/validators/objectives";
import { insertItems, insertQuests, insertUserItems, insertUsers } from "../../setup/factories";
import { callerForDatabase, getTestDatabase, resetTables } from "../../setup/testDatabase";
import { aiIdForSlot, ENTRY_ITEM_ID, encounterSlots, QUEST_ID, questRecord, SENTINEL_ITEM_ID } from "./graph";

export const HERO = "sb-hero";
export const EDITOR = "sb-content-editor";
export const MAX = { health: 1000, chakra: 1200, stamina: 900 };
const router = createTRPCRouter({ quests: questsRouter, combat: combatRouter });
const pusher = { trigger: vi.fn(async () => {}) } as unknown as PusherClient;

export const db = () => getTestDatabase();
export const api = async () => callerForDatabase(router, HERO, await db());
export const hero = async () => (await db()).query.userData.findFirst({ where: eq(userData.userId, HERO) });
const heldQuantity = async (itemId: string) =>
  ((await (await db()).query.userItem.findMany({ where: eq(userItem.userId, HERO) }))
    .filter((r) => r.itemId === itemId).reduce((s, r) => s + r.quantity, 0));
export const beacons = () => heldQuantity(ENTRY_ITEM_ID);
/** Quest completion payouts received (sentinel reward item count). */
export const payouts = () => heldQuantity(SENTINEL_ITEM_ID);
export const history = async () => (await db()).query.questHistory.findMany({ where: eq(questHistory.userId, HERO) });
export const questRow = async () => (await db()).query.quest.findFirst({ where: eq(quest.id, QUEST_ID) }) as Promise<Quest>;
export const tracker = async (): Promise<QuestTrackerType | undefined> =>
  ((await hero())?.questData as QuestTrackerType[] | null)?.find((t) => t.id === QUEST_ID);

/** Fresh world: hero, 25 encounter AIs, Default AI profile, beacons, and the quest row. */
export const resetWorld = async (opts: { beaconCount?: number } = {}) => {
  await resetTables(battleHistory, battle, aiProfile, questHistory, quest, userItem, item, userData);
  await insertUsers([
    { userId: HERO, username: "sb-hero", status: "AWAKE", rank: "JONIN", level: 50, isOutlaw: true, regeneration: 10,
      money: 0, curEnergy: 10, curHealth: MAX.health, maxHealth: MAX.health, curChakra: MAX.chakra, maxChakra: MAX.chakra,
      curStamina: MAX.stamina, maxStamina: MAX.stamina, primaryElement: "Fire", secondaryElement: "Water", sector: 0 },
    { userId: EDITOR, username: "sb-editor", role: "CONTENT" },
    ...encounterSlots().map((slot) => ({ userId: aiIdForSlot(slot), username: aiIdForSlot(slot), isAi: true, level: 50 })),
  ]);
  await (await db()).insert(aiProfile).values({ id: "Default", userId: "sb-default-ai", rules: [] });
  await insertItems([
    { id: ENTRY_ITEM_ID, name: "Skyglass Signal Beacon [fixture]", itemType: "CONSUMABLE" },
    { id: SENTINEL_ITEM_ID, name: "Completion sentinel [fixture]", itemType: "MATERIAL" },
  ]);
  if ((opts.beaconCount ?? 3) > 0)
    await insertUserItems([{ id: "sb-beacon-stack", userId: HERO, itemId: ENTRY_ITEM_ID, quantity: opts.beaconCount ?? 3 }]);
  const { content, ...rest } = questRecord();
  await insertQuests([{ id: QUEST_ID, ...rest, content }]);
};

/** Engine's own view of the run: active objective and every available-but-open objective. */
export const engineView = async () => {
  const q = await questRow();
  const t = await tracker();
  if (!t) return { active: undefined as string | undefined, open: [] as string[] };
  const active = getActiveObjective(q, t)?.id;
  const open = q.content.objectives
    .map((o, i) => ({ o, i }))
    .filter(({ o, i }) => isQuestObjectiveAvailable(q, t, i) && !t.goals.find((g) => g.id === o.id)?.done)
    .map(({ o }) => o.id);
  return { active, open };
};

/** Page load: runs getNewTrackers("any") and its consequences, exactly like the client refresh. */
export const refresh = async () => fetchUpdatedUser({ client: await db(), userId: HERO });

export const choose = async (nextObjectiveId: string) =>
  (await api()).quests.checkRewards({ questId: QUEST_ID, nextObjectiveId });

export type Snapshot = NonNullable<Awaited<ReturnType<typeof fetchBattle>>>;
export const currentBattle = async (): Promise<Snapshot | null> => {
  const id = (await hero())?.battleId;
  return id ? (await fetchBattle(await db(), id)) ?? null : null;
};

/** Settle the live battle. Win leaves the given pools; loss sets HP 0 (engine keeps 1 HP). */
export const settle = async (won: boolean, pools: { health: number; chakra: number; stamina: number }) => {
  const snapshot = await currentBattle();
  if (!snapshot) throw new Error("No battle to settle");
  const player = snapshot.usersState.find((u) => u.userId === HERO)!;
  const opponents = snapshot.usersState.filter((u) => u.isAi);
  player.curHealth = won ? pools.health : 0;
  player.curChakra = pools.chakra;
  player.curStamina = pools.stamina;
  for (const o of opponents) o.curHealth = won ? 0 : o.maxHealth;
  const result = calcBattleResult(snapshot, HERO, snapshot.extraState.settings);
  if (!result) throw new Error("Battle did not finish");
  await updateUser(await db(), pusher, snapshot, result, HERO);
  await (await db()).delete(battle).where(eq(battle.id, snapshot.id));
  return result;
};
