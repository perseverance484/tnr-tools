/**
 * Ghost Ship / Skyglass Stage 2 harness — in-process battle assembly and loop.
 *
 * Assembly reproduces `initiateBattle`'s battle-start preprocessing around the
 * engine's own `processUsersForBattle`: each user is deep-cloned (captured records
 * stay untouched) and capped with `capUserStats` at its own rank (QUEST is not a
 * ranked battle; the captured Ghost Ship quest objectives carry no `scaleStats`,
 * so `scaleTarget` is false and no stat distribution applies); after assembly,
 * auto-combat flags, `applyPoolAdjustmentsToBase` for pool effects,
 * `refreshMasteries` and the aggressor flag are applied as initiateBattle does.
 * There is no database client: it is only touched for summon templates, and no
 * fixture here carries a summon effect (asserted). Not reproduced: random start
 * tiles and random initial ground barriers (fixed placements, clear ground).
 * The turn loop mirrors the inner loop of `combat.performAction`: alignBattle →
 * performAIaction for the active actor → alignBattle. Players are driven through
 * the engine's auto-combat path (`isAutoCombat`, as initiateBattle sets it for
 * QUEST battles), so both sides choose actions with the real AI selector.
 *
 * Determinism: `Math.random` is replaced by a seeded mulberry32 for the whole
 * fight (initiative rolls, RANDOM_* targets, prevent/stun rolls, etc.).
 */
import { getUserCaps, TOTAL_MASTERY_CAP } from "@/drizzle/constants";
import { performAIaction } from "@/libs/combat/ai_v2";
import { COMBAT_SECONDS } from "@/libs/combat/constants";
import {
  alignBattle,
  applyPoolAdjustmentsToBase,
  calcApReduction,
  getBattleGrid,
  getDefaultBattleSizes,
  isEffectActive,
  refreshMasteries,
} from "@/libs/combat/util";
import { stillInBattle } from "@/libs/combat/actions";
import { applySageModeAfterRoundTransition } from "@/libs/combat/process";
import { calcCP, calcHP, calcSP, capUserStats } from "@/libs/profile";
import { processUsersForBattle } from "@/server/api/routers/combat";
import { getBackupRules } from "@/validators/ai";
import type { CompleteBattle, UserEffect } from "@/libs/combat/types";

export const mulberry32 = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

export const withSeed = async <T>(seed: number, fn: () => Promise<T> | T): Promise<T> => {
  const orig = Math.random;
  Math.random = mulberry32(seed);
  try {
    return await fn();
  } finally {
    Math.random = orig;
  }
};

export const joninCaps = () => {
  const { stats_cap, gens_cap } = getUserCaps("JONIN");
  return {
    stats: stats_cap, gens: gens_cap, hp: calcHP(100), sp: calcSP(100), cp: calcCP(100),
    masteryEach: TOTAL_MASTERY_CAP / 4,
  };
};

/** Placeholder for the DB "Default" profile; only used by users without a profile. */
const defaultProfile = { id: "Default", userId: "Default", includeDefaultRules: true, rules: getBackupRules() };

/** Read-only client: any property access means the assembly needed the DB. */
const noDbClient = new Proxy(
  {},
  {
    get(_t, prop) {
      throw new Error(`HARNESS: battle assembly attempted DB access (${String(prop)})`);
    },
  },
) as never;

export type Placement = { userId: string; x: number; y: number };

/**
 * Assemble a QUEST battle from CombatQueryUsers. users[0] is the attacker (the
 * player, acting first as in initiateBattle for non-PvP types).
 */
export const assembleBattle = async (opts: {
  users: any[];
  placements: Placement[];
  autoCombatUserIds?: string[];
  /** Attacker side (initiateBattle passes the initiating userIds); default users[0]. */
  leftSideUserIds?: string[];
  battleType?: string;
  width?: number;
  height?: number;
}): Promise<CompleteBattle> => {
  const battleType = (opts.battleType ?? "QUEST") as never;
  const size = getDefaultBattleSizes(battleType, 100)!;
  const width = opts.width ?? size.width;
  const height = opts.height ?? size.height;
  // initiateBattle structuredClones each fetched user, then caps it at battle start.
  const users = opts.users.map((u) => structuredClone(u));
  for (const u of users) capUserStats(u, u.rank);
  for (const u of users) {
    const summon = [...(u.jutsus ?? []).flatMap((j: any) => j.jutsu.effects), ...(u.items ?? []).flatMap((i: any) => i.item.effects)]
      .some((e: any) => e.type === "summon");
    if (summon) throw new Error(`HARNESS: ${u.userId} carries a summon effect; needs DB templates`);
  }
  const { userEffects, usersState, extraState } = await processUsersForBattle(noDbClient, {
    users,
    settings: [],
    relations: [],
    wars: [],
    villages: [],
    defaultProfile: defaultProfile as never,
    battleType,
    hide: false,
    // As initiateBattle: the engine sets each side's `direction` (used by
    // friendlyFire ENEMIES/FRIENDLY checks) and assigns random start tiles.
    leftSideUserIds: opts.leftSideUserIds ?? [users[0].userId],
    isSummon: false,
    width,
    height,
  });
  for (const u of usersState) {
    if (!u.isAi && opts.autoCombatUserIds?.includes(u.controllerId)) u.isAutoCombat = true;
    // Fixed, declared start tiles replace the engine's random placement so that
    // distance-dependent tests are reproducible (same inputs for both bosses).
    const p = opts.placements.find((x) => x.userId === u.controllerId);
    if (p) {
      u.longitude = p.x;
      u.latitude = p.y;
    }
  }
  // initiateBattle, after processUsersForBattle: pool effects adjust base pools,
  // mastery tags apply from the first action, the attacker is the aggressor.
  for (const u of usersState) {
    const hasPoolEffects = userEffects.some((e) => e.targetId === u.userId && (e.type === "increasemaxpools" || e.type === "decreasemaxpools") && isEffectActive(e));
    if (hasPoolEffects) applyPoolAdjustmentsToBase(u, userEffects);
  }
  refreshMasteries(usersState, userEffects);
  if (usersState[0]) usersState[0].isAggressor = true;
  // initiateBattle: usersState sorted by initiative; attacker (users[0]) acts first.
  usersState.sort((a, b) => b.initiative - a.initiative);
  const attacker = usersState.find((u) => u.controllerId === users[0].userId)!;
  const now = new Date();
  return {
    id: "harness-battle",
    battleType,
    background: "",
    usersState,
    usersEffects: userEffects,
    groundEffects: [],
    width,
    height,
    extraState,
    rewardScaling: 1,
    createdAt: now,
    updatedAt: now,
    roundStartAt: now,
    activeUserId: attacker.userId,
    forceKeepPools: false,
    round: 1, // battle.round column default
    version: 1,
  } as unknown as CompleteBattle;
};

export type ActionRecord = {
  step: number;
  round: number;
  actor: string;
  actionId: string | null;
  actionName: string | null;
  apBefore: number;
  apAfter: number;
  /** HP change across performAIaction only. */
  hpDelta: Record<string, number>;
  /**
   * HP change across the whole step: from the end of the previous step, through
   * this step's turn/round alignment, the action and the post-action alignment.
   * Includes delayed effects (drain/poison ticks) that resolve outside the
   * actor's own action. Summed with FightResult.residualHpDelta it reconciles
   * exactly to final − initial HP.
   */
  hpDeltaStep: Record<string, number>;
  /** Positive, Clear-removable effects (by target controller) active before the action and gone/inactive after it. */
  removedPositive: { target: string; type: string }[];
  descriptions: string[];
  effectTexts: string[];
  idleTimeout?: boolean;
};

export type FightResult = {
  seed: number;
  winner: "player" | "boss" | "none";
  /** Round index in which the fight ended (maxRounds + 1 when it ran out). */
  rounds: number;
  /** Completed measurement interval: maxRounds when the cap was reached, else the round index in which it ended. */
  measuredRounds: number;
  initialHp: Record<string, number>;
  /** HP change not covered by any step record (alignment in the breaking iteration). */
  residualHpDelta: Record<string, number>;
  /** State at the end of the fight; perRound holds one round-start sample per distinct round. */
  terminal: RoundSample;
  steps: number;
  log: ActionRecord[];
  perRound: RoundSample[];
  bossExhausted: boolean;
  idleTimeouts: Record<string, number>;
  final: Record<string, { curHealth: number; maxHealth: number; curChakra: number; maxChakra: number; curStamina: number; maxStamina: number }>;
};

export type RoundSample = {
  round: number;
  users: Record<string, {
    hp: number; cp: number; sp: number;
    /** Action points held at the sample (round start) and the engine's stun AP reduction for this round. */
    ap: number; apReduction: number;
    stunned: boolean; sealed: boolean;
    idg: number; idgRemovable: number;
    shieldHp: number; absorb: boolean; ddt: boolean;
    positiveRemovable: number;
  }>;
};

const POSITIVE = new Set([
  "increasedamagegiven", "decreasedamagetaken", "increasestat", "shield", "absorb",
  "reflect", "heal", "increaseheal", "stealth", "debuffprevent", "clearprevent", "immunity",
]);
const PROTECTED = new Set(["bloodline", "armor", "accessory", "keystone", "skill", "ranked", "village", "sageMode", "sageModeAfter"]);

export const sampleRound = (b: CompleteBattle): RoundSample => {
  const users: RoundSample["users"] = {};
  for (const u of b.usersState) {
    const mine = b.usersEffects.filter((e) => e.targetId === u.userId && isEffectActive(e) && (e.rounds === undefined || e.rounds > 0));
    const idg = mine.filter((e) => e.type === "increasedamagegiven");
    users[u.controllerId] = {
      hp: u.curHealth, cp: u.curChakra, sp: u.curStamina,
      ap: u.actionPoints, apReduction: calcApReduction(b as never, u.userId),
      stunned: mine.some((e) => e.type === "stun"),
      sealed: mine.some((e) => e.type === "seal"),
      idg: idg.reduce((s, e) => s + (e.power ?? 0), 0),
      idgRemovable: idg.filter((e) => !PROTECTED.has(e.fromType as string)).reduce((s, e) => s + (e.power ?? 0), 0),
      shieldHp: mine.filter((e) => e.type === "shield").reduce((s, e: any) => s + (e.power ?? 0), 0),
      absorb: mine.some((e) => e.type === "absorb"),
      ddt: mine.some((e) => e.type === "decreasedamagetaken"),
      positiveRemovable: mine.filter((e) => POSITIVE.has(e.type) && !PROTECTED.has(e.fromType as string)).length,
    };
  }
  return { round: b.round, users };
};

const removablePositive = (b: CompleteBattle) =>
  b.usersEffects
    .filter((e) => POSITIVE.has(e.type) && !PROTECTED.has(e.fromType as string) && isEffectActive(e) && (e.rounds === undefined || e.rounds > 0))
    .map((e) => ({ id: e.id, targetId: e.targetId, type: e.type }));

const nameOf = (b: CompleteBattle, id?: string | null) => {
  if (!id) return null;
  const j = (b.extraState.jutsus as any)?.[id];
  if (j) return j.name;
  const it = (b.extraState.items as any)?.[id];
  if (it) return it.name;
  return id;
};

/**
 * Run a battle to completion or `maxRounds`. `playerIds` are controller IDs of
 * the player side (session user is the first). Returns a full action log and
 * per-round samples. An actor whose AI turn yields no action (auto-combat
 * humans never self-kill) is passed on by expiring the round timer, which is
 * what the live round clock would do; such events are counted.
 */
export const runFight = (battle: CompleteBattle, opts: { playerIds: string[]; bossIds: string[]; maxRounds: number; maxSteps?: number; seed: number }): FightResult => {
  let b = battle;
  const sessionUser = b.usersState.find((u) => u.controllerId === opts.playerIds[0])!.userId;
  const grid = getBattleGrid(1, b);
  const actionRounds: number[] = [];
  const log: ActionRecord[] = [];
  const perRound: RoundSample[] = [];
  const idleTimeouts: Record<string, number> = {};
  let bossExhausted = false;
  let lastSampled = -1;
  const hpNow = () => Object.fromEntries(b.usersState.map((u) => [u.controllerId, u.curHealth]));
  const diff = (from: Record<string, number>, to: Record<string, number>) => {
    const d: Record<string, number> = {};
    for (const [k, v] of Object.entries(to)) if (v !== (from[k] ?? v)) d[k] = v - (from[k] ?? v);
    return d;
  };
  const initialHp = hpNow();
  let lastHp = initialHp;
  const sideAlive = (ids: string[]) => b.usersState.some((u) => ids.includes(u.controllerId) && stillInBattle(u, b.usersEffects));
  const maxSteps = opts.maxSteps ?? opts.maxRounds * 12;
  let step = 0;
  for (; step < maxSteps; step++) {
    const pre = alignBattle(b, actionRounds, sessionUser);
    if (pre.progressRound) applySageModeAfterRoundTransition(b);
    if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
    // One round-start sample per distinct round inside the measured interval.
    if (b.round > opts.maxRounds) break;
    if (!sideAlive(opts.playerIds) || !sideAlive(opts.bossIds)) break;
    if (b.round !== lastSampled) {
      perRound.push(sampleRound(b));
      lastSampled = b.round;
    }
    const actor = pre.actor;
    const before = Object.fromEntries(b.usersState.map((u) => [u.controllerId, u.curHealth]));
    const apBefore = actor.actionPoints;
    const positiveBefore = removablePositive(b);
    const res = performAIaction(b, grid, actor.userId);
    b = res.nextBattle;
    const positiveAfter = new Set(removablePositive(b).map((e) => e.id));
    const cidOf = (uid: string) => b.usersState.find((u) => u.userId === uid)?.controllerId ?? uid;
    const removedPositive = positiveBefore.filter((e) => !positiveAfter.has(e.id)).map((e) => ({ target: cidOf(e.targetId), type: e.type }));
    const after = b.usersState.find((u) => u.userId === actor.userId);
    const hpDelta: Record<string, number> = {};
    for (const u of b.usersState) {
      const d = u.curHealth - (before[u.controllerId] ?? u.curHealth);
      if (d !== 0) hpDelta[u.controllerId] = d;
    }
    const rec: ActionRecord = {
      step, round: b.round, actor: actor.controllerId,
      actionId: res.nextActionId ?? null, actionName: nameOf(b, res.nextActionId),
      apBefore, apAfter: after?.actionPoints ?? 0, hpDelta, hpDeltaStep: {}, removedPositive,
      descriptions: res.aiDescriptions, effectTexts: res.nextActionEffects.map((e) => e.txt),
    };
    if (res.aiDescriptions.some((d) => d.includes("is exhausted and has to give up"))) {
      if (opts.bossIds.includes(actor.controllerId)) bossExhausted = true;
    }
    if (!res.nextActionId) {
      // Live round clock passes an idle auto-combat turn on.
      rec.idleTimeout = true;
      idleTimeouts[actor.controllerId] = (idleTimeouts[actor.controllerId] ?? 0) + 1;
      b.roundStartAt = new Date(Date.now() - (COMBAT_SECONDS + 1) * 1000);
    }
    log.push(rec);
    const post = alignBattle(b, actionRounds, sessionUser);
    if (post.progressRound) applySageModeAfterRoundTransition(b);
    const hpEnd = hpNow();
    rec.hpDeltaStep = diff(lastHp, hpEnd);
    lastHp = hpEnd;
    if (!sideAlive(opts.playerIds) || !sideAlive(opts.bossIds)) break;
  }
  const pAlive = sideAlive(opts.playerIds);
  const bAlive = sideAlive(opts.bossIds);
  const final: FightResult["final"] = {};
  for (const u of b.usersState) final[u.controllerId] = { curHealth: u.curHealth, maxHealth: u.maxHealth, curChakra: u.curChakra, maxChakra: u.maxChakra, curStamina: u.curStamina, maxStamina: u.maxStamina };
  return {
    seed: opts.seed,
    winner: pAlive && !bAlive ? "player" : bAlive && !pAlive ? "boss" : "none",
    rounds: b.round,
    measuredRounds: b.round > opts.maxRounds ? opts.maxRounds : b.round,
    initialHp, residualHpDelta: diff(lastHp, hpNow()), terminal: sampleRound(b),
    steps: step, log, perRound, bossExhausted, idleTimeouts, final,
  };
};

/** Effects realised onto a target, for direct selector tests. */
export const activeEffectsOf = (b: CompleteBattle, userId: string): UserEffect[] =>
  b.usersEffects.filter((e) => e.targetId === userId);
