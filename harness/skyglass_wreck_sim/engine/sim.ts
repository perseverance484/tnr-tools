/**
 * Skyglass Wreck harness: in-memory dungeon floor battles driven by the engine.
 *
 * Assembly follows `initiateBattle` for a dungeon floor (routers/dungeon.ts "start" ->
 * initiateBattle(QUEST, coop.kind "dungeon", forceKeepPools, waves)):
 *   clone users -> capUserStats(rank) for every participant -> processUsersForBattle(opening
 *   slice: 3 players + wave 1) -> prepareEncounterWaves(remaining waves, leftSideUserCount 0) ->
 *   extraState.encounter / extraState.dungeon -> pool-effect base adjust -> refreshMasteries ->
 *   aggressor -> initial random ground barriers -> first actor = the initiating player.
 * The turn loop mirrors the inner loop of `combat.performAction`:
 *   advanceEncounterWave -> alignBattle (+sage transition) -> performAIaction(actor) ->
 *   dungeon lastActionRound -> alignBattle (+sage transition) -> advanceEncounterWave ->
 *   dungeonBattleOutcome.
 * Players are driven by the engine's auto-combat path (isAutoCombat + their AI profile).
 */
import { performAIaction } from "@/libs/combat/ai_v2";
import { stillInBattle } from "@/libs/combat/actions";
import { advanceEncounterWave, prepareEncounterWaves } from "@/libs/combat/encounters";
import { getBattleSpawnLocations } from "@/libs/combat/participants";
import { applySageModeAfterRoundTransition } from "@/libs/combat/process";
import type { CompleteBattle } from "@/libs/combat/types";
import {
  alignBattle,
  applyPoolAdjustmentsToBase,
  getBattleGrid,
  getDefaultBattleSizes,
  isEffectActive,
  refreshMasteries,
} from "@/libs/combat/util";
import { dungeonBattleOutcome } from "@/libs/dungeon";
import { capUserStats } from "@/libs/profile";
import { SAGE_MODE_ACTIVATION_JUTSU } from "@/libs/sageMode";
import { getBackupRules } from "@/validators/ai";
import { BarrierTag } from "@/validators/combat";
import { SAGE_MODE_ACTIVATION_JUTSU_ID } from "@/drizzle/constants";
import { processUsersForBattle } from "@/server/api/routers/combat";
import type { FloorDef } from "./model";

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

/** Read-only client: any property access means assembly needed the DB (it must not). */
const noDbClient = new Proxy(
  {},
  {
    get(_t, prop) {
      throw new Error(`HARNESS: battle assembly attempted DB access (${String(prop)})`);
    },
  },
) as never;

/** Stand-in for the DB "Default" AI profile; only used by users without their own profile. */
const defaultProfile = { id: "Default", userId: "Default", includeDefaultRules: true, rules: getBackupRules() };

export type Probe = { userId: string; ruleIndex: number; actionId: string; ruleType: string; totalRules: number };

export type StepRec = {
  round: number;
  wave: number;
  actor: string; // controllerId (AI template id or player id)
  actorUid: string;
  human: boolean;
  actionId: string | null;
  ruleIndex: number | null;
  authoredRules: number;
  hp: Record<string, number>; // per battle userId, HP change over the step (incl. ticks)
  dealt: number; // engine damageDealt delta of the actor
  dealtBy: Record<string, number>; // damageDealt delta per userId over the step
  effects: { type: string; target: string; creator: string }[]; // new user effects this step
  ground: { type: string; creator: string; x?: number; y?: number; rounds?: number }[];
  /** Positions (debug/probe use): actor before and after the step. */
  actorFrom?: [number, number];
  actorTo?: [number, number];
  /** Units that entered usersState during the step (summons, clones, waves). */
  newUnits?: { uid: string; name: string; controllerId: string; isSummon: boolean; x: number; y: number; hp: number }[];
  /** Effects on the actor when its step began (probe use). */
  actorEffects?: { type: string; power?: number; rounds?: number; creator: string }[];
  /** Ground effects on the field after the step. */
  groundAfter?: { type: string; creator: string; x: number; y: number; rounds?: number; power?: number }[];
};

export type FloorResult = {
  outcome: "won" | "wipe" | "ended" | "stalled";
  failedReason?: string;
  rounds: number;
  waves: {
    wave: number;
    startRound: number;
    endRound: number | null;
    enemies: { uid: string; aiId: string; name: string; maxHealth: number; diedRound: number | null }[];
    humanTurns: number;
    aiTurns: number;
    partyHpLost: number;
    partyHpMax: number;
    poolsAtEnd: Record<string, { hp: number; cp: number; sp: number; alive: boolean }> | null;
  }[];
  steps: StepRec[];
  players: Record<string, { name: string; maxHealth: number; minHealth: number; downs: number }>;
  final: Record<string, { hp: number; maxHp: number; cp: number; maxCp: number; sp: number; maxSp: number }>;
  humanTurns: number;
  aiTurns: number;
};

/** Assemble one dungeon floor exactly as initiateBattle does (minus I/O). */
export const assembleFloor = async (opts: {
  players: any[];
  enemyRows: Record<string, any>; // aiId -> CombatQueryUser
  floor: FloorDef;
  rand: () => number;
  initialBarriers: boolean;
  /** Damage formula settings; the engine reads battle.extraState.dmgConfig ?? code defaults. */
  dmgConfig?: Record<string, number>;
  /** "dungeon" (default): coop dungeon floor. "quest": a plain QUEST battle (no waves/dungeon state). */
  mode?: "dungeon" | "quest";
}): Promise<CompleteBattle> => {
  const quest = opts.mode === "quest";
  const battleType = "QUEST" as never;
  const playerIds = opts.players.map((p) => p.userId);
  const targetIds = opts.floor.waves.flatMap((w) => w.aiIds);
  // initiateBattle: users = [...userIds, ...targetIds] each structuredCloned; then per-user loop caps stats.
  const users = [...opts.players, ...targetIds.map((id) => opts.enemyRows[id])].map((u) => structuredClone(u));
  for (const u of users) capUserStats(u, u.rank);
  // Summon templates: initiateBattle reads them from the DB into a shared summonTemplateCache.
  // Pre-seed that same cache with the captured AI rows (keyed by AI id), so the engine's own
  // summon preparation runs without a database; a summon of an uncaptured AI fails loudly.
  const summonIds = new Set<string>();
  for (const u of users)
    for (const uj of u.jutsus ?? [])
      for (const e of uj.jutsu.effects) if (e.type === "summon" && e.aiId) summonIds.add(e.aiId);
  const summonTemplateCache = new Map<string, Promise<any[]>>();
  for (const id of summonIds) {
    const row = opts.enemyRows[id];
    if (!row) throw new Error(`HARNESS: summon template ${id} is not a captured AI`);
    summonTemplateCache.set(id, Promise.resolve([structuredClone(row)]));
  }
  const size = getDefaultBattleSizes(battleType, users[0]?.level ?? 0)!;
  const { width, height } = size;
  const common = {
    settings: [], relations: [], wars: [], villages: [], defaultProfile: defaultProfile as never,
    battleType, width, height, hide: false, isSummon: false, summonTemplateCache,
  };
  const firstCount = quest ? users.length : playerIds.length + (opts.floor.waves[0]?.aiIds.length ?? 0);
  const processed = await processUsersForBattle(noDbClient, {
    ...common,
    users: users.slice(0, firstCount),
    leftSideUserIds: playerIds,
    leftSideUserCount: playerIds.length,
  } as never);
  const { userEffects, usersState, extraState } = processed;
  const groundEffects = [...(processed.groundEffects ?? [])];
  // Spawn cells: the engine draws them with node:crypto (unseedable). Redraw the opening
  // placement uniformly over the same engine spawn list with the run's seeded generator.
  const taken: { x: number; y: number }[] = [];
  for (const u of usersState) {
    if (u.isSummon) continue;
    const free = getBattleSpawnLocations(width, height, u.direction).filter(
      (l) => !taken.some((t) => t.x === l.x && t.y === l.y),
    );
    const loc = free[Math.floor(opts.rand() * free.length)]!;
    taken.push(loc);
    u.longitude = loc.x;
    u.latitude = loc.y;
  }
  let offset = firstCount;
  if (!quest) {
  const encounter = await prepareEncounterWaves(
    opts.floor.waves as never,
    { usersState, userEffects, extraState },
    async (wave: any) => {
      const prepared = await processUsersForBattle(noDbClient, {
        ...common,
        users: users.slice(offset, offset + wave.aiIds.length),
        leftSideUserCount: 0,
      } as never);
      offset += wave.aiIds.length;
      return prepared;
    },
  );
  extraState.encounter = encounter;
  extraState.dungeon = {
    runId: "harness-run",
    runVersion: 1,
    runState: {} as never,
    totalFloors: 5,
    roomKind: opts.floor.kind,
    expiresAt: Date.now() + 1e12, // wall-clock deadline is modelled outside the battle
    lastActionRound: Object.fromEntries(playerIds.map((id) => [id, 0])),
  };
  }
  // Players drive their own turns live; here the engine's auto-combat path stands in.
  for (const u of usersState) if (!u.isAi && !u.isSummon) u.isAutoCombat = true;
  for (const u of usersState) {
    const hasPoolEffects = userEffects.some(
      (e) => e.targetId === u.userId && (e.type === "increasemaxpools" || e.type === "decreasemaxpools") && isEffectActive(e),
    );
    if (hasPoolEffects) applyPoolAdjustmentsToBase(u, userEffects);
  }
  refreshMasteries(usersState, userEffects);
  if (usersState[0]) usersState[0].isAggressor = true;
  // initiateBattle: 10% of unoccupied cells get a power-2 barrier from a battlefield asset.
  if (opts.initialBarriers) {
    for (let col = 0; col < width; col++)
      for (let row = 0; row < height; row++) {
        if (usersState.find((u) => u.longitude === col && u.latitude === row)) continue;
        if (Math.random() < 0.1) {
          groundEffects.push({
            ...BarrierTag.parse({ power: 2, staticAssetPath: "harness-asset" }),
            id: `initial-${col}-${row}`, creatorId: "ground", actionId: "initial", createdRound: 0,
            level: 0, longitude: col, latitude: row, isNew: false, barrierAbsorb: 0, castThisRound: false,
          } as never);
        }
      }
  }
  usersState.sort((a, b) => b.initiative - a.initiative);
  const now = new Date();
  return {
    id: "harness-battle",
    battleType,
    background: "default",
    usersState,
    usersEffects: userEffects,
    groundEffects,
    width,
    height,
    extraState: {
      ...extraState,
      jutsus: { ...extraState.jutsus, [SAGE_MODE_ACTIVATION_JUTSU_ID]: SAGE_MODE_ACTIVATION_JUTSU },
      settings: [],
      ...(opts.dmgConfig ? { dmgConfig: opts.dmgConfig } : {}),
    },
    rewardScaling: 1,
    createdAt: now,
    updatedAt: now,
    roundStartAt: now,
    activeUserId: playerIds[0],
    forceKeepPools: !quest,
    round: 1,
    version: 1,
  } as unknown as CompleteBattle;
};

/** Run one floor battle to its dungeon outcome. */
export const runFloor = (battle: CompleteBattle, opts: { playerIds: string[]; maxRounds: number; detail?: boolean }): FloorResult => {
  let b = battle;
  const suid = opts.playerIds[0]!;
  const grid = getBattleGrid(1, b);
  const actionRounds: number[] = [];
  const steps: StepRec[] = [];
  const g = globalThis as { __TNR_RULE_PROBE__?: (p: Probe) => void };
  let probe: Probe | null = null;
  g.__TNR_RULE_PROBE__ = (p) => {
    probe = p;
  };
  const enc = () => b.extraState.encounter ?? { wave: 1 };
  /** Dungeon outcome, or for a plain battle: one side has nobody left standing. */
  const outcomeOf = () => {
    if (b.extraState.dungeon) return dungeonBattleOutcome(b);
    const side = (dir: string) => b.usersState.some((u) => u.direction === dir && !u.isSummon && stillInBattle(u, b.usersEffects));
    if (!side("left")) return "wipe" as const;
    if (!side("right")) return "won" as const;
    return null;
  };
  const humans = () => b.usersState.filter((u) => !u.isAi && !u.isSummon);
  const authoredCount = (u: any) => {
    const p = (b.extraState.aiProfiles as any)?.[u.aiProfileId];
    return p ? p.rules.length : 0;
  };
  const players: FloorResult["players"] = {};
  for (const u of humans()) players[u.userId] = { name: u.username, maxHealth: u.maxHealth, minHealth: u.curHealth, downs: 0 };
  const waves: FloorResult["waves"] = [];
  const seen = new Set<string>();
  const registerWave = () => {
    const fresh = b.usersState.filter((u) => u.isAi && !u.isSummon && u.direction === "right" && !seen.has(u.userId) && stillInBattle(u, b.usersEffects));
    if (!fresh.length) return;
    fresh.forEach((u) => seen.add(u.userId));
    const partyMax = humans().reduce((s, u) => s + u.maxHealth, 0);
    waves.push({
      wave: enc().wave, startRound: b.round, endRound: null,
      enemies: fresh.map((u) => ({ uid: u.userId, aiId: u.controllerId, name: u.username, maxHealth: u.maxHealth, diedRound: null })),
      humanTurns: 0, aiTurns: 0, partyHpLost: 0, partyHpMax: partyMax, poolsAtEnd: null,
    });
  };
  const curWave = () => waves[waves.length - 1]!;
  const closeWaveIfCleared = () => {
    const w = waves[waves.length - 1];
    if (!w || w.endRound !== null) return;
    for (const e of w.enemies) {
      const u = b.usersState.find((x) => x.userId === e.uid);
      if (e.diedRound === null && (!u || !stillInBattle(u, b.usersEffects))) e.diedRound = b.round;
    }
    if (w.enemies.every((e) => e.diedRound !== null)) {
      w.endRound = b.round;
      w.poolsAtEnd = Object.fromEntries(
        humans().map((u) => [u.userId, { hp: u.curHealth / u.maxHealth, cp: u.curChakra / u.maxChakra, sp: u.curStamina / u.maxStamina, alive: stillInBattle(u, b.usersEffects) }]),
      );
    }
  };
  let humanTurns = 0;
  let aiTurns = 0;
  const turnKey = new Set<string>();
  let outcome: FloorResult["outcome"] = "stalled";
  advanceEncounterWave(b, !!outcomeOf());
  registerWave();
  const maxSteps = opts.maxRounds * 40;
  for (let step = 0; step < maxSteps; step++) {
    const pre = alignBattle(b, actionRounds, suid);
    if (pre.progressRound) applySageModeAfterRoundTransition(b);
    if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
    if (b.round > opts.maxRounds) break;
    const actor = pre.actor;
    const isHuman = !actor.isAi && !actor.isSummon;
    const k = `${b.round}:${actor.userId}`;
    if (!turnKey.has(k)) {
      turnKey.add(k);
      if (isHuman) {
        humanTurns++;
        curWave().humanTurns++;
      } else {
        aiTurns++;
        curWave().aiTurns++;
      }
    }
    const hpBefore = new Map(b.usersState.map((u) => [u.userId, u.curHealth]));
    const ddBefore = new Map(b.usersState.map((u) => [u.userId, u.damageDealt ?? 0]));
    const effBefore = new Set(b.usersEffects.map((e) => e.id));
    const gBefore = new Set(b.groundEffects.map((e) => e.id));
    const uBefore = new Set(b.usersState.map((u) => u.userId));
    const actorFrom: [number, number] = [actor.longitude, actor.latitude];
    const actorEffects = opts.detail
      ? b.usersEffects.filter((e) => e.targetId === actor.userId).map((e: any) => ({ type: e.type, power: e.power, rounds: e.rounds, creator: e.creatorId }))
      : undefined;
    const waveAtStep = curWave().wave;
    probe = null;
    const res = performAIaction(b, grid, actor.userId);
    b = res.nextBattle;
    const fired = probe as Probe | null;
    // performAction: an explicit player action stamps the dungeon inactivity tracker.
    if (res.nextActionId && b.extraState.dungeon && isHuman)
      b.extraState.dungeon.lastActionRound[actor.userId] = pre.actionRound;
    const post = alignBattle(b, actionRounds, suid);
    if (post.progressRound) applySageModeAfterRoundTransition(b);
    if (!actionRounds.includes(post.actionRound)) actionRounds.push(post.actionRound);
    if (!res.nextActionId && actor.isAutoCombat) {
      // Live, the round clock passes an idle turn on; never observed with the default profiles.
      b.roundStartAt = new Date(Date.now() - 61_000);
    }
    const hp: Record<string, number> = {};
    const dealtBy: Record<string, number> = {};
    for (const u of b.usersState) {
      const d = u.curHealth - (hpBefore.get(u.userId) ?? u.curHealth);
      if (d) hp[u.userId] = d;
      const dd = (u.damageDealt ?? 0) - (ddBefore.get(u.userId) ?? 0);
      if (dd) dealtBy[u.userId] = dd;
    }
    for (const u of humans()) {
      const pl = players[u.userId]!;
      const before = hpBefore.get(u.userId) ?? u.curHealth;
      pl.minHealth = Math.min(pl.minHealth, u.curHealth);
      if (before > 0 && u.curHealth <= 0) pl.downs++;
      if (u.curHealth < before) curWave().partyHpLost += before - u.curHealth;
    }
    steps.push({
      round: pre.actionRound, wave: waveAtStep, actor: actor.controllerId, actorUid: actor.userId, human: isHuman,
      actionId: res.nextActionId ?? null,
      ruleIndex: fired && fired.userId === actor.userId ? fired.ruleIndex : null,
      authoredRules: authoredCount(actor),
      hp, dealt: dealtBy[actor.userId] ?? 0, dealtBy,
      effects: b.usersEffects.filter((e) => !effBefore.has(e.id)).map((e) => ({ type: e.type, target: e.targetId, creator: e.creatorId })),
      ground: b.groundEffects.filter((e) => !gBefore.has(e.id)).map((e) => ({ type: e.type, creator: e.creatorId, ...(opts.detail ? { x: e.longitude, y: e.latitude, rounds: e.rounds } : {}) })),
      ...(opts.detail
        ? {
            actorFrom,
            actorEffects,
            actorTo: ((u) => (u ? [u.longitude, u.latitude] : actorFrom))(b.usersState.find((u) => u.userId === actor.userId)) as [number, number],
            newUnits: b.usersState.filter((u) => !uBefore.has(u.userId)).map((u) => ({ uid: u.userId, name: u.username, controllerId: u.controllerId, isSummon: !!u.isSummon, x: u.longitude, y: u.latitude, hp: u.curHealth })),
            groundAfter: b.groundEffects.filter((e) => e.creatorId !== "ground").map((e: any) => ({ type: e.type, creator: e.creatorId, x: e.longitude, y: e.latitude, rounds: e.rounds, power: e.power, staticAnimation: e.staticAnimation || undefined })),
          }
        : {}),
    });
    closeWaveIfCleared();
    if (advanceEncounterWave(b, !!outcomeOf())) registerWave();
    const out = outcomeOf();
    if (out) {
      outcome = out;
      closeWaveIfCleared();
      break;
    }
  }
  g.__TNR_RULE_PROBE__ = undefined;
  const final: FloorResult["final"] = {};
  for (const u of b.usersState)
    if (!u.isSummon) final[u.userId] = { hp: u.curHealth, maxHp: u.maxHealth, cp: u.curChakra, maxCp: u.maxChakra, sp: u.curStamina, maxSp: u.maxStamina };
  return {
    outcome, failedReason: b.extraState.dungeon?.failedReason, rounds: b.round,
    waves, steps, players, final, humanTurns, aiTurns,
  };
};
