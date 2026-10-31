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
import { nanoid } from "nanoid";
import { performAIaction } from "@/libs/combat/ai_v2";
import { markersOf, noteAction } from "./fallback";
import { stillInBattle } from "@/libs/combat/actions";
import { advanceEncounterWave, prepareEncounterWaves } from "@/libs/combat/encounters";
import { assertRuleCap } from "./rulecap";
import { gateProfile } from "./gates";
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

/**
 * Seed the engine's id entropy. Unit ids minted mid-battle (clones, summons, effects) come from
 * nanoid, i.e. crypto.getRandomValues, which is unseeded; with a clone on the field the battle's
 * course can depend on those ids, so identical seeds diverged. This routes getRandomValues through
 * its own seeded generator (separate from Math.random, so the combat roll stream is unchanged) and
 * restarts nanoid's id pool.
 */
export const seedEntropy = (seed: number) => {
  const next = mulberry32((seed ^ 0x5eed1d) >>> 0);
  Object.defineProperty(globalThis.crypto, "getRandomValues", {
    configurable: true,
    writable: true,
    value: <T extends ArrayBufferView | null>(arr: T): T => {
      if (!arr) return arr;
      const bytes = new Uint8Array(arr.buffer, arr.byteOffset, arr.byteLength);
      for (let i = 0; i < bytes.length; i++) bytes[i] = Math.floor(next() * 256);
      return arr;
    },
  });
  // nanoid keeps a pool of up to 32,768 pre-drawn characters; one oversized draw empties it, so the
  // next id starts a fresh pool from the seeded source.
  nanoid(32_769);
  seedClock();
};

/**
 * Virtual clock. The engine reads the wall clock in a few places (the 60 s round timer in calcActiveUser,
 * roundStartAt, updatedAt stamps), so a slow or busy machine could change a battle's course. Each run gets a
 * fixed epoch, and the clock advances a fixed step per engine call (runFloor ticks it once per action), so
 * time-dependent paths see the same values on every machine.
 */
const RealDate = Date;
let virtualNow = 0;
export const tickClock = (ms: number) => {
  virtualNow += ms;
};
export const seedClock = () => {
  virtualNow = RealDate.UTC(2026, 9, 28, 0, 0, 0);
  if ((globalThis.Date as any).__harnessVirtual) return;
  class VirtualDate extends RealDate {
    constructor(...args: any[]) {
      if (args.length === 0) super(virtualNow);
      else super(...(args as [any]));
    }
    static now() {
      return virtualNow;
    }
  }
  (VirtualDate as any).__harnessVirtual = true;
  globalThis.Date = VirtualDate as unknown as DateConstructor;
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
  groundAfter?: { type: string; creator: string; x: number; y: number; rounds?: number; power?: number; curHealth?: number }[];
  /** Harness dodge pre-step (players only): this step was a dodge move. */
  dodge?: boolean;
};

/**
 * Harness auto-player dodge (a stand-in for a person reading the marks; not engine behaviour).
 * At a player's turn, if they stand on a hex marked by an enemy telegraph (tg_heavy / tg_control)
 * or a lingering pool (tg_linger), or an arena-wide mark is up (tg_safe stars exist) and they are
 * not on a star, they walk (engine basic Move, one hex per action) to the nearest acceptable free
 * hex within DODGE_STEPS. While any mark is up they also skip their "close the distance" move rule
 * for that turn, so they do not walk back in.
 */
export const DANGER_ANIMS = new Set(["tg_heavy", "tg_control", "tg_linger"]);
export const SAFE_ANIM = "tg_safe";
/**
 * Persistent hazard ground (The Fall's ember tiles: `drain` ground with a tg_ember visual). Not a one-turn mark: the
 * auto-player steps off an ember only when a clear hex within DODGE_STEPS still keeps the closest enemy within its
 * attack reach (else it fights on the embers), and its close-in step avoids embers when another step exists.
 */
export const EMBER_ANIM = "tg_ember";
export const DODGE_STEPS = 3;
export type DodgeStats = { threatened: number; dodged: number; failedRooted: number; failedNoPath: number; failedOther: number; stepsTaken: number };

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
  dodge: DodgeStats;
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
  /** Companion pets (UserPet rows with their species), one per owner; owners carry activePetId. */
  pets?: any[];
  /**
   * Quest NPC allies (objective `allyAIs` -> initiateBattle `allyAiIds`): AI ids placed after the players and before
   * the targets, all on the left side (leftSideUserCount = players + allies), exactly as initiateBattle orders them.
   */
  allyIds?: string[];
}): Promise<CompleteBattle> => {
  for (const [id, row] of Object.entries<any>(opts.enemyRows ?? {})) if (row?.aiProfile && !String(row.userId ?? id).includes("user_")) gateProfile(row.aiProfile);
  assertRuleCap(opts.enemyRows);
  const quest = opts.mode === "quest";
  const battleType = "QUEST" as never;
  const playerIds = opts.players.map((p) => p.userId);
  const targetIds = opts.floor.waves.flatMap((w) => w.aiIds);
  const allyIds = opts.allyIds ?? [];
  // initiateBattle: users = [...userIds, ...allyAiIds, ...targetIds] each structuredCloned; then per-user loop caps stats.
  const users = [...opts.players, ...allyIds.map((id) => opts.enemyRows[id]), ...targetIds.map((id) => opts.enemyRows[id])].map((u) => structuredClone(u));
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
  const firstCount = quest ? users.length : playerIds.length + allyIds.length + (opts.floor.waves[0]?.aiIds.length ?? 0);
  const petPreload = opts.pets?.length
    ? {
        pets: structuredClone(opts.pets),
        ownerRanks: Object.fromEntries(opts.players.map((p) => [p.userId, p.rank])),
        abilitiesByOwner: Object.fromEntries(opts.players.map((p) => [p.userId, { jutsus: [], skills: [] }])),
      }
    : undefined;
  const processed = await processUsersForBattle(noDbClient, {
    ...common,
    users: users.slice(0, firstCount),
    leftSideUserIds: playerIds,
    leftSideUserCount: playerIds.length + allyIds.length,
    ...(petPreload ? { petPreload } : {}),
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
  // Pets spawned beside their owner's engine-drawn cell; re-seat each beside the owner's redrawn cell
  // (the nearest free hex, the engine's own getPetSpawnLocation rule restated: owner's half, grid order on ties).
  // Clear every pet's engine-drawn cell first: those derive from the unseeded engine spawn draw, and a pet not yet
  // re-seated would otherwise block a cell for the others (same seed, different placement). (fable/skyglass-wreck-sim c301632b)
  const petsInBattle = usersState.filter((u: any) => u.petId);
  for (const pet of petsInBattle) {
    pet.longitude = -1;
    pet.latitude = -1;
  }
  for (const pet of petsInBattle) {
    const owner = usersState.find((u) => u.userId === pet.controllerId)!;
    const half = Math.floor(width / 2);
    const cells: { x: number; y: number; d: number }[] = [];
    for (let x = 0; x <= half; x++)
      for (let y = 0; y < height; y++) {
        if (usersState.some((u) => u !== pet && u.longitude === x && u.latitude === y)) continue;
        cells.push({ x, y, d: Math.abs(x - (owner.longitude - 1)) + Math.abs(y - owner.latitude) });
      }
    cells.sort((a, b) => a.d - b.d);
    if (cells[0]) {
      pet.longitude = cells[0].x;
      pet.latitude = cells[0].y;
    }
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
export const runFloor = (battle: CompleteBattle, opts: { playerIds: string[]; maxRounds: number; detail?: boolean; dodge?: boolean; onAiDecision?: (b: CompleteBattle, actorUid: string, grid: any) => void }): FloorResult => {
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
    // A player's battle ends when the player is out (calcBattleResult: !stillInBattle(user)), even while a quest NPC
    // ally fights on; pets are summons. Without allies this is the same test as side("left").
    if (!humans().some((u) => stillInBattle(u, b.usersEffects))) return "wipe" as const;
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
  const dodge: DodgeStats = { threatened: 0, dodged: 0, failedRooted: 0, failedNoPath: 0, failedOther: 0, stepsTaken: 0 };
  const playerSet = new Set(opts.playerIds);
  /** Marked hexes from enemy ground effects that are still live. */
  const marks = () => {
    const danger = new Set<string>();
    const safe = new Set<string>();
    const embers = new Set<string>();
    // Marks laid by the players' own side (players, pets, quest NPC allies) are not threats to them.
    const friendly = new Set(b.usersState.filter((u) => u.direction === "left").map((u) => u.userId));
    for (const e of b.groundEffects as any[]) {
      if (e.creatorId === "ground" || playerSet.has(e.creatorId) || friendly.has(e.creatorId)) continue;
      if ((e.rounds ?? 0) <= 0 && !e.castThisRound) continue;
      const k = `${e.longitude},${e.latitude}`;
      if (DANGER_ANIMS.has(e.staticAnimation)) danger.add(k);
      if (e.staticAnimation === SAFE_ANIM) safe.add(k);
      if (e.staticAnimation === EMBER_ANIM) embers.add(k);
    }
    return { danger, safe, embers };
  };
  /** One free, unmarked neighbouring hex that brings the player closer to the closest enemy. */
  const safeStep = (actor: any, danger: Set<string>): { x: number; y: number } | null => {
    const hexes = grid.toArray();
    const here = hexes.find((h: any) => h.col === actor.longitude && h.row === actor.latitude);
    if (!here) return null;
    const occupied = new Set<string>();
    for (const u of b.usersState) if (u.userId !== actor.userId && stillInBattle(u, b.usersEffects)) occupied.add(`${u.longitude},${u.latitude}`);
    for (const e of b.groundEffects as any[]) if (e.type === "barrier") occupied.add(`${e.longitude},${e.latitude}`);
    const foes = b.usersState.filter((u) => u.direction !== actor.direction && stillInBattle(u, b.usersEffects)).map((u) => hexes.find((x: any) => x.col === u.longitude && x.row === u.latitude)!).filter(Boolean);
    if (!foes.length) return null;
    const dFoe = (h: any) => Math.min(...foes.map((f: any) => grid.distance(h, f)));
    const cur = dFoe(here);
    const options = hexes.filter((n: any) => grid.distance(here, n) === 1 && !occupied.has(`${n.col},${n.row}`) && !danger.has(`${n.col},${n.row}`) && dFoe(n) < cur);
    options.sort((p: any, q: any) => dFoe(p) - dFoe(q) || p.col - q.col || p.row - q.row);
    return options[0] ? { x: options[0].col, y: options[0].row } : null;
  };
  /** Dodge state of the current human turn. */
  let dodgeTurn: { key: string; counted: boolean; steps: number; done: boolean; lastPos: string } | null = null;
  /** Longest range among the player's offensive jutsu (ember rule: stay within reach of the closest enemy). */
  const reachOf = (actor: any) =>
    Math.max(1, ...((actor.jutsus ?? []) as any[]).filter((uj) => uj.jutsu?.target !== "SELF").map((uj) => uj.jutsu?.range ?? 1));
  const planDodge = (actor: any): { x: number; y: number } | null | "ok" => {
    const { danger, safe, embers } = marks();
    const here = `${actor.longitude},${actor.latitude}`;
    const arena = safe.size > 0;
    const emberOnly = !danger.size && !arena;
    const ok = (k: string) => (arena ? safe.has(k) : !danger.has(k) && !(emberOnly && embers.has(k)));
    if (ok(here)) return "ok";
    const blocked = new Set<string>();
    for (const u of b.usersState) if (u.userId !== actor.userId && stillInBattle(u, b.usersEffects)) blocked.add(`${u.longitude},${u.latitude}`);
    for (const e of b.groundEffects as any[]) if (e.type === "barrier") blocked.add(`${e.longitude},${e.latitude}`);
    // BFS over the hex grid (honeycomb distance 1 neighbours).
    const hexes = grid.toArray();
    const start = hexes.find((h: any) => h.col === actor.longitude && h.row === actor.latitude);
    if (!start) return null;
    const dist = new Map<any, number>([[start, 0]]);
    const queue: any[] = [start];
    const found: any[] = [];
    while (queue.length) {
      const h = queue.shift();
      const d = dist.get(h)!;
      if (d > 0 && ok(`${h.col},${h.row}`)) found.push(h);
      if (d >= DODGE_STEPS) continue;
      for (const n of hexes) {
        if (dist.has(n) || grid.distance(h, n) !== 1 || blocked.has(`${n.col},${n.row}`)) continue;
        dist.set(n, d + 1);
        queue.push(n);
      }
    }
    const enemies = b.usersState.filter((u) => u.direction !== actor.direction && stillInBattle(u, b.usersEffects));
    const ed = (h: any) => Math.min(99, ...enemies.map((u) => grid.distance(h, hexes.find((x: any) => x.col === u.longitude && x.row === u.latitude)!)));
    if (emberOnly) {
      // Embers: leave only for a clear hex that keeps an enemy within reach; otherwise fight where you stand.
      const reach = reachOf(actor);
      const inReach = found.filter((h) => ed(h) <= reach);
      if (!inReach.length) return "ok";
      found.length = 0;
      found.push(...inReach);
    }
    if (!found.length) return null;
    const minD = Math.min(...found.map((h) => dist.get(h)!));
    const best = found.filter((h) => dist.get(h) === minD);
    // Tie-break: stay closest to the nearest enemy (keep fighting), then by position.
    best.sort((p, q) => ed(p) - ed(q) || p.col - q.col || p.row - q.row);
    return { x: best[0].col, y: best[0].row };
  };
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
    // Harness dodge pre-step (see DANGER_ANIMS).
    let restoreRules: (() => void) | null = null;
    let dodgeStep = false;
    if (isHuman && opts.dodge) {
      const tk = `${b.round}:${actor.userId}`;
      if (!dodgeTurn || dodgeTurn.key !== tk) dodgeTurn = { key: tk, counted: false, steps: 0, done: false, lastPos: "" };
      const profile = (b.extraState.aiProfiles as any)?.[actor.aiProfileId];
      const { danger, safe, embers } = marks();
      if (profile && (danger.size || safe.size || embers.size)) {
        const saved = profile.rules;
        const emberOnly = !danger.size && !safe.size;
        // While marks are up the player's own "close in" moves become one-hex steps that never enter a
        // marked hex (and never leave a safe star); an explicit end of turn keeps the engine's appended
        // backup rules (move towards a random opponent) from walking them into the marks.
        const step = safe.size ? null : safeStep(actor, emberOnly ? new Set([...danger, ...embers]) : danger);
        let rules = [
          ...saved.flatMap((r: any) =>
            r.action.type !== "move_towards_opponent"
              ? [r]
              : step
                ? [{ ...r, action: { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: step.x, latitude: step.y }, description: "harness: safe step" } }]
                : emberOnly
                  ? [r] // no clear step: walk in over the embers
                  : [],
          ),
          { conditions: [], action: { type: "end_turn", description: "harness: hold while marked" } },
        ];
        if (!dodgeTurn.done) {
          const plan = planDodge(actor);
          if (plan === "ok") dodgeTurn.done = true;
          else {
            if (!dodgeTurn.counted) {
              dodgeTurn.counted = true;
              dodge.threatened++;
            }
            const pos = `${actor.longitude},${actor.latitude}`;
            const rooted = b.usersEffects.some((e: any) => e.targetId === actor.userId && (e.type === "moveprevent" || e.type === "stun") && isEffectActive(e));
            if (plan === null) {
              dodge.failedNoPath++;
              dodgeTurn.done = true;
            } else if (dodgeTurn.steps >= DODGE_STEPS || (dodgeTurn.steps > 0 && pos === dodgeTurn.lastPos)) {
              if (rooted) dodge.failedRooted++;
              else dodge.failedOther++;
              dodgeTurn.done = true;
            } else {
              dodgeTurn.steps++;
              dodgeTurn.lastPos = pos;
              dodgeStep = true;
              rules = [{ conditions: [], action: { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: plan.x, latitude: plan.y }, description: "harness dodge" } }];
            }
          }
        }
        profile.rules = rules;
        const pid = actor.aiProfileId;
        restoreRules = () => {
          // performAIaction may return a cloned battle: restore on both.
          profile.rules = saved;
          const np = (b.extraState.aiProfiles as any)?.[pid];
          if (np) np.rules = saved;
        };
      }
    }
    tickClock(1000);
    // Read-only audit hook (audit_rules.ts): sees the battle as the AI is about to decide.
    if (opts.onAiDecision && !isHuman) opts.onAiDecision(b, actor.userId, grid);
    const markersBefore = isHuman ? null : markersOf(b, actor.userId);
    const res = performAIaction(b, grid, actor.userId);
    b = res.nextBattle;
    if (markersBefore) noteAction(markersBefore, actor, res.nextActionId, pre.actionRound);
    restoreRules?.();
    if (dodgeStep) {
      dodge.stepsTaken++;
      const me = b.usersState.find((u) => u.userId === actor.userId);
      const plan = me ? planDodge(me) : null;
      if (plan === "ok" && dodgeTurn) {
        dodge.dodged++;
        dodgeTurn.done = true;
      } else if (me && dodgeTurn && `${me.longitude},${me.latitude}` === dodgeTurn.lastPos) {
        const rooted = b.usersEffects.some((e: any) => e.targetId === actor.userId && (e.type === "moveprevent" || e.type === "stun") && isEffectActive(e));
        if (rooted) dodge.failedRooted++;
        else dodge.failedOther++;
        dodgeTurn.done = true;
      }
    }
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
      ruleIndex: dodgeStep ? null : fired && fired.userId === actor.userId ? fired.ruleIndex : null,
      ...(dodgeStep ? { dodge: true } : {}),
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
            groundAfter: b.groundEffects.filter((e) => e.creatorId !== "ground").map((e: any) => ({ type: e.type, creator: e.creatorId, x: e.longitude, y: e.latitude, rounds: e.rounds, power: e.power, staticAnimation: e.staticAnimation || undefined, curHealth: e.type === "barrier" ? e.curHealth : undefined })),
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
    waves, steps, players, final, humanTurns, aiTurns, dodge,
  };
};

/**
 * Phase lengths of one enemy in a finished fight, rebuilt from the step HP deltas (read-only): phase 2 starts at its first
 * own decision below `pct`% of max health (as audit_rules.ts --phase-hp) and ends at its death or the fight's end.
 * Rounds are inclusive. Used for the Captain's phase 2 in the Watch and the chart runs.
 */
export const phaseTrack = (battle: CompleteBattle, res: FloorResult, controllerId: string, pct = 50) => {
  const u0 = battle.usersState.find((u: any) => u.controllerId === controllerId && !u.isSummon) as any;
  if (!u0) return null;
  const uid = u0.userId;
  let hp = u0.curHealth;
  const max = u0.maxHealth;
  const first = res.steps.find((s) => s.actorUid === uid)?.round ?? null;
  let p2: number | null = null;
  let died: number | null = null;
  for (const s of res.steps) {
    if (s.actorUid === uid && p2 === null && hp < (max * pct) / 100) p2 = s.round;
    hp += s.hp[uid] ?? 0;
    if (hp <= 0 && died === null) died = s.round;
  }
  const end = died ?? res.rounds;
  return {
    reachedPhase2: p2 !== null, died: died !== null,
    phase1Rounds: first === null ? null : (p2 ?? end) - first + (p2 === null ? 1 : 0),
    phase2Rounds: p2 === null ? null : end - p2 + 1,
  };
};
