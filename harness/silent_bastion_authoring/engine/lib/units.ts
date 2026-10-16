/**
 * Silent Bastion authoring — AI unit loader and router-faithful battle driver (pure, no DB).
 *
 * Loads state/silent_bastion_authoring/design/{commanders,regulars}.json and the captured jutsu
 * records in sources/source_records.json, compiles the rule DSL into the pinned engine's own AI
 * constructors (validators/ai.ts), and plays turns exactly the way routers/combat.ts does:
 * alignBattle → performAIaction → alignBattle … (no pruning step in between).
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { performAIaction } from "@/libs/combat/ai_v2";
import { alignBattle, getBattleGrid, isEffectActive } from "@/libs/combat/util";
import type { BattleUserState, CompleteBattle, UserEffect } from "@/libs/combat/types";
import {
  ActionEndTurn, ActionMoveTowardsOpponent, ActionUseSpecificItem, ActionUseSpecificJutsu, AiRule,
  ConditionDistanceHigherThan, ConditionDistanceLowerThan, ConditionHasEffect, ConditionHealthBelow,
  ConditionRoundGreaterThan, ConditionRoundLowerThan, ConditionSpecificRound, ConditionTargetHasEffect,
} from "@/validators/ai";
import { getTagSchema } from "@/validators/combat";
import { makeBattleUser, makeCompleteBattle } from "../../libs/combat/helpers/battleScenario";

export const REPO = process.env.TNR_REPO ?? join(import.meta.dir, "../../../../../../..");
const AUTH = join(REPO, "state/silent_bastion_authoring");
const load = (p: string) => JSON.parse(readFileSync(join(AUTH, p), "utf8"));

type Cond = (string | number)[];
export type DslRule = { if: Cond[]; do: string[]; src: string };
export type Unit = {
  key: string; slot: string; name: string; kit: string[]; items: string[]; rules: DslRule[];
  innate: { type: string; power: number; rounds: number }[];
  candidate: Record<string, unknown> & { level: number; rank: string; statsMultiplier: number; poolsMultiplier: number; regeneration: number };
};
export const commanders = load("design/commanders.json") as { units: Unit[]; exclusives: Record<string, { record: Record<string, unknown> & { effects: Record<string, unknown>[] } }> };
export const regulars = load("design/regulars.json") as { units: Unit[] };
export const sources = load("sources/source_records.json") as {
  jutsu: Record<string, { id: string; name: string; record: Record<string, unknown> & { effects: Record<string, unknown>[]; range: number; method: string; target: string; actionCostPerc: number; cooldown: number }; poolSummary?: Record<string, unknown> }>;
  seedItems: { records: Record<string, Record<string, unknown>> };
};
export const allUnits = () => [...commanders.units, ...regulars.units];

/** Exclusive / new candidate ids are local fixture ids, never live ids. */
export const exclusiveId = (key: string) => `sb-${key.slice(2).toLowerCase().replace(/_/g, "-")}`;
export const seedItemId = (name: string) => sources.seedItems.records[name]!.id as string;
export const jutsuId = (code: string) => (code.startsWith("X:") ? exclusiveId(code) : sources.jutsu[code]!.id);
export const itemId = (key: string) => (key.startsWith("X:") ? exclusiveId(key) : seedItemId(key.slice(5)));

/** Parse a candidate tag; a `calculation` the tag type does not support falls back to its schema default. */
const tag = (e: Record<string, unknown>) => {
  const schema = getTagSchema(e.type as never);
  const first = schema.safeParse({ target: "INHERIT", ...e });
  if (first.success) return first.data as Record<string, unknown>;
  const { calculation: _c, ...rest } = e;
  return schema.parse({ target: "INHERIT", ...rest }) as Record<string, unknown>;
};

/** Full jutsu record for a kit code: the captured record, or a candidate exclusive built on a captured template. */
export const jutsuRecord = (code: string) => {
  if (!code.startsWith("X:")) return structuredClone(sources.jutsu[code]!.record);
  const ex = commanders.exclusives[code]!.record;
  const template = structuredClone(sources.jutsu[ex.target === "SELF" ? "B10" : "S07"]!.record);
  return { ...template, ...ex, id: exclusiveId(code), jutsuType: "AI", hidden: true,
    effects: ex.effects.map(({ candidate: _c, ...e }) => tag({ ...e, target: ex.target === "SELF" ? "SELF" : "INHERIT" })) };
};

/** Full item record: candidate exclusive (Countermand) or the upstream seed row. */
export const itemRecord = (key: string) => {
  const base = {
    image: "/x.png", battleDescription: "%user uses %item", healthCost: 0, healthCostReducePerLvl: 0, chakraCost: 0,
    chakraCostReducePerLvl: 0, staminaCost: 0, staminaCostReducePerLvl: 0, maxDurability: 100, preventBattleUsage: false,
    battleUsageType: "BOTH", hidden: false,
  };
  if (key.startsWith("X:")) {
    const { effects, dropChancePerc: _d, ...ex } = commanders.exclusives[key]!.record as Record<string, unknown> & { effects: Record<string, unknown>[] };
    return { ...base, ...ex, id: exclusiveId(key), effects: effects.map(tag) };
  }
  const seed = structuredClone(sources.seedItems.records[key.slice(5)]!) as Record<string, unknown> & { effects: Record<string, unknown>[] };
  return { ...base, ...seed, effects: seed.effects.map(tag) };
};

/** DSL condition → engine condition object. */
const condition = (c: Cond) => {
  const [op, a, b] = c;
  const v = (x: unknown) => Number(x);
  switch (op) {
    case "hp<": return ConditionHealthBelow.parse({ value: v(a) });
    case "round<": return ConditionRoundLowerThan.parse({ value: v(a) });
    case "round>": return ConditionRoundGreaterThan.parse({ value: v(a) });
    case "round=": return ConditionSpecificRound.parse({ value: v(a) });
    case "dist<=": return ConditionDistanceLowerThan.parse({ value: v(a), target: "CLOSEST_OPPONENT" });
    case "dist>=": return ConditionDistanceHigherThan.parse({ value: v(a), target: "CLOSEST_OPPONENT" });
    case "self": return ConditionHasEffect.parse({ effectType: a, threshold: Number(b) });
    case "target": return ConditionTargetHasEffect.parse({ effectType: a, threshold: Number(b), target: "CLOSEST_OPPONENT" });
  }
  throw new Error(`unknown DSL condition ${op}`);
};
const action = (d: string[]) => {
  const [kind, ref, target] = d;
  if (kind === "jutsu") return ActionUseSpecificJutsu.parse({ jutsuId: jutsuId(ref!), target });
  if (kind === "item") return ActionUseSpecificItem.parse({ itemId: itemId(ref!), target });
  if (kind === "move") return ActionMoveTowardsOpponent.parse({ target: "CLOSEST_OPPONENT" });
  if (kind === "end") return ActionEndTurn.parse({});
  throw new Error(`unknown DSL action ${kind}`);
};
export const compileRules = (u: Unit) =>
  u.rules.map((r) => AiRule.parse({ conditions: r.if.map((c) => condition(c)), action: action(r.do) }));

// ---------------------------------------------------------------- battle driver
export const AI = "sb-ai";
export const HUMAN = "sb-player";
export const W = 13;
export const H = 9;
/** The router's own battle grid (routers/combat.ts: getBattleGrid(1, battle)): flat hexes, cost 1. */
export const newGrid = () => getBattleGrid(1, { width: W, height: H } as never);

export type Scene = {
  dist?: number; round?: number; hpPct?: number; cpPct?: number; aiEffects?: Partial<UserEffect>[];
  playerEffects?: Partial<UserEffect>[]; cooldowns?: Record<string, number>; humanHp?: number;
};

const effect = (e: Partial<UserEffect>, i: number, targetId: string, creatorId: string, round: number): UserEffect =>
  ({ id: `fx-${targetId}-${i}`, actionId: `fx-${i}`, level: 1, isNew: false, castThisRound: false, createdRound: round - 1,
     longitude: 0, latitude: 0, barrierAbsorb: 0, fromType: "jutsu", creatorId, targetId,
     ...getTagSchema(e.type as never).parse({ rounds: 3, power: 100, ...e }) }) as unknown as UserEffect;

/** Battle with the unit at column 2 and a passive player `dist` A* steps away (adjacent = 2). */
export const scene = (u: Unit, s: Scene = {}) => {
  const round = s.round ?? 3;
  const dist = s.dist ?? 2;
  const maxPool = 100_000;
  const hp = Math.round((maxPool * (s.hpPct ?? 100)) / 100);
  const jutsus = u.kit.map((code) => jutsuRecord(code));
  const items = u.items.map((k) => itemRecord(k));
  const ai = makeBattleUser(AI, {
    isAi: true, aiProfileId: `profile-${u.key}`, villageId: "bastion", direction: "right", longitude: 2, latitude: 4,
    curHealth: hp, maxHealth: maxPool, curChakra: (maxPool * (s.cpPct ?? 100)) / 100, maxChakra: maxPool, curStamina: maxPool, maxStamina: maxPool,
    level: 100, rank: "JONIN", round: round - 1,
    // Battle state carries each action's cooldown on the user entry (actions.ts userJutsuToAction: cooldown = originalCooldown).
    jutsus: u.kit.map((code, i) => ({ id: `uj-${code}`, jutsuId: jutsuId(code), equipped: true, level: 1, experience: 0,
      lastUsedRound: s.cooldowns?.[code] !== undefined ? round - s.cooldowns[code]! : -99, originalCooldown: Number(jutsus[i]!.cooldown), origin: "user" })),
    items: u.items.map((k, i) => ({ id: `ui-${i}`, itemId: itemId(k), quantity: 1, level: 1, experience: 0,
      equipped: k.startsWith("SEED:") ? (i === 1 ? "HAND_1" : "HAND_2") : "ITEM_1", durability: 100, dropChancePerc: 0,
      lastUsedRound: s.cooldowns?.[k] !== undefined ? round - s.cooldowns[k]! : -99, originalCooldown: Number(items[i]!.cooldown) })),
  });
  const human = makeBattleUser(HUMAN, {
    isAi: false, villageId: "player", direction: "left", longitude: 2 + (dist - 1), latitude: 4,
    curHealth: s.humanHp ?? 5_000_000, maxHealth: 5_000_000, level: 100, rank: "JONIN", round: round - 1, actionPoints: 0,
  });
  const battle = makeCompleteBattle({
    battleType: "QUEST", round, usersState: [ai, human], activeUserId: AI, roundStartAt: new Date(),
    createdAt: new Date(0), updatedAt: new Date(0), version: 1, background: "", width: W, height: H, rewardScaling: 1, forceKeepPools: false,
    usersEffects: [
      ...(u.innate.map((x, i) => effect({ type: x.type as never, power: x.power, rounds: x.rounds }, 100 + i, AI, AI, round))),
      ...(s.aiEffects ?? []).map((e, i) => effect(e, i, AI, AI, round)),
      ...(s.playerEffects ?? []).map((e, i) => effect(e, 50 + i, HUMAN, HUMAN, round)),
    ],
    extraState: {
      jutsus: Object.fromEntries(jutsus.map((j) => [j.id as string, j])), items: Object.fromEntries(items.map((i) => [i.id as string, i])),
      jutsuReskins: {}, bloodlines: {}, villages: {}, anbuSquads: {}, keystoneItems: {}, wars: {}, relations: {}, clans: {},
      userQuests: {}, completedQuests: {}, questData: {}, bounties: {}, bountySignups: {},
      aiProfiles: { [`profile-${u.key}`]: { id: `profile-${u.key}`, name: u.name, includeDefaultRules: false, rules: compileRules(u) } },
    } as never,
  });
  return battle as CompleteBattle;
};

export const codeOf = (u: Unit, id?: string) => {
  if (!id) return id;
  const j = u.kit.find((c) => jutsuId(c) === id);
  if (j) return j;
  const it = u.items.find((k) => itemId(k) === id);
  return it ?? id;
};

/** One AI turn on the current round: performAIaction until it passes, gives up or runs out of AP. */
export const aiTurn = (u: Unit, battle: CompleteBattle, grid = newGrid()) => {
  const acts: string[] = [];
  let b = battle;
  for (let i = 0; i < 6; i++) {
    const r = performAIaction(b, grid, AI);
    b = r.nextBattle;
    const me = b.usersState.find((x) => x.userId === AI);
    if (r.aiDescriptions.some((d) => d.includes("give up"))) { acts.push("GAVE_UP"); break; }
    if (!r.nextActionId) break;
    acts.push(codeOf(u, r.nextActionId)!);
    if (r.nextActionId === "wait" || !me || me.actionPoints <= 0) break;
  }
  return { battle: b, acts };
};

/**
 * Router-faithful multi-round loop: alignBattle before every decision (round progression lowers
 * effect rounds without pruning, exactly as routers/combat.ts), then performAIaction for whichever
 * AI-driven combatant is the actor (the unit, or its clone); the passive player's turn times out.
 * Every decision of the unit is logged with the Final Stand state it saw.
 */
export const playRounds = (u: Unit, battle: CompleteBattle, rounds: number) => {
  const grid = newGrid();
  let b = battle;
  const decisions: { round: number; act: string; finalStand: { present: boolean; active: boolean; rounds?: number } }[] = [];
  const others: { round: number; actor: string; act: string }[] = [];
  let guard = 0;
  while (b.round < battle.round + rounds && guard++ < rounds * 20) {
    const { actor } = alignBattle(b, [b.round]);
    if (actor.userId === HUMAN) {
      b.roundStartAt = new Date(Date.now() - 10 * 60_000); // passive player: turn times out
      continue;
    }
    const fs = b.usersEffects.find((e) => e.targetId === AI && e.type === "finalstand");
    const seen = { present: !!fs, active: !!fs && isEffectActive(fs), rounds: fs?.rounds };
    const r = performAIaction(b, grid, actor.userId);
    b = r.nextBattle;
    const act = r.aiDescriptions.some((d) => d.includes("give up")) ? "GAVE_UP" : r.nextActionId ? codeOf(u, r.nextActionId)! : "NONE";
    if (actor.userId === AI) decisions.push({ round: b.round, act, finalStand: seen });
    else others.push({ round: b.round, actor: actor.username, act });
    const me = b.usersState.find((x) => x.userId === AI) as BattleUserState | undefined;
    if (!me || me.curHealth <= 0) break;
    const cur = b.usersState.find((x) => x.userId === actor.userId);
    if (cur && (!r.nextActionId || r.nextActionId === "wait")) cur.actionPoints = 0;
  }
  const log: { round: number; acts: string[] }[] = [];
  for (const d of decisions) {
    const last = log[log.length - 1];
    if (last && last.round === d.round) last.acts.push(d.act);
    else log.push({ round: d.round, acts: [d.act] });
  }
  return { battle: b, log, decisions, others };
};
