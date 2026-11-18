/**
 * Combat sim core: assemble a battle the way `initiateBattle` does (minus I/O) and run it with the engine's own turn code.
 *
 * Assembly mirrors app/src/server/api/routers/combat.ts initiateBattle at the pinned commit (see ENGINE_PIN):
 *   clone users -> capUserStats(rank) -> processUsersForBattle(opening slice: players + wave 1, shared
 *   summonTemplateCache) -> prepareEncounterWaves(later waves, leftSideUserCount 0) -> extraState.encounter /
 *   extraState.dungeon -> isAutoCombat for players -> syncPoolAdjustments -> refreshMasteries -> aggressor ->
 *   rollStartingGroundEffects -> sort by initiative, first actor = the initiating player (non-PvP).
 *   The live dmgConfig and sharedCooldowns go into extraState, as insertBattleForCreateBattle stores them.
 * The turn loop mirrors combat.performAction: advanceEncounterWave -> alignBattle (+ sage transition) -> act ->
 *   dungeon lastActionRound -> alignBattle -> advanceEncounterWave -> outcome.
 * Players act through the engine's auto-combat path (their profile rules) unless a driver forces their actions
 * through availableUserActions -> performBattleAction (the human action path), as the log replay does.
 *
 * Determinism: Math.random is the run's seeded generator, crypto.getRandomValues is seeded separately (ids minted
 * mid-battle), the clock is virtual, and opening spawn cells are redrawn from the engine's spawn list with the seed.
 */
import { nanoid } from "nanoid";
import { availableUserActions, performBattleAction } from "@/libs/combat/actions";
import { performAIaction } from "@/libs/combat/ai_v2";
import { advanceEncounterWave, prepareEncounterWaves } from "@/libs/combat/encounters";
import { stillInBattle } from "@/libs/combat/inBattle";
import { rollStartingGroundEffects } from "@/libs/combat/initiation";
import { refreshMasteries } from "@/libs/combat/mastery";
import { getBattleSpawnLocations } from "@/libs/combat/participants";
import { getPetSpawnLocation } from "@/libs/combat/pets";
import { applySageModeAfterRoundTransition } from "@/libs/combat/process";
import { alignBattle } from "@/libs/combat/turn";
import type { CompleteBattle } from "@/libs/combat/types";
import { getBattleGrid, getBattleSize, isEffectActive, syncPoolAdjustments } from "@/libs/combat/util";
import { dungeonBattleOutcome } from "@/libs/dungeon";
import { capUserStats } from "@/libs/profile";
import { SAGE_MODE_ACTIVATION_JUTSU } from "@/libs/sageMode";
import { getBackupRules } from "@/validators/ai";
import { SAGE_MODE_ACTIVATION_JUTSU_ID } from "@/drizzle/constants";
import { processUsersForBattle } from "@/server/api/routers/combat";

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

const RealDate = Date;
let virtualNow = 0;
export const tickClock = (ms: number) => {
  virtualNow += ms;
};
const seedClock = () => {
  virtualNow = RealDate.UTC(2026, 10, 18, 0, 0, 0);
  if ((globalThis.Date as any).__simVirtual) return;
  class VirtualDate extends RealDate {
    constructor(...args: any[]) {
      if (args.length === 0) super(virtualNow);
      else super(...(args as [any]));
    }
    static now() {
      return virtualNow;
    }
  }
  (VirtualDate as any).__simVirtual = true;
  globalThis.Date = VirtualDate as unknown as DateConstructor;
};

/** Seed every random source the engine reads for one run; returns the seeded generator (also installed as Math.random). */
export const seedRun = (seed: number) => {
  const rand = mulberry32(seed);
  Math.random = rand;
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
  nanoid(32_769); // empty nanoid's pre-drawn pool so the next id comes from the seeded source
  seedClock();
  return rand;
};

/** Any DB access during assembly is a harness bug: everything must come from the records. */
const noDbClient = new Proxy({}, {
  get(_t, prop) {
    throw new Error(`SIM: battle assembly attempted DB access (${String(prop)})`);
  },
}) as never;

const defaultProfile = { id: "Default", userId: "Default", includeDefaultRules: true, rules: getBackupRules() };

export type WaveDef = { aiIds: string[]; delayRounds: number };

export type AssembleOpts = {
  players: any[];
  /** AI id -> row (model.enemyRow). Every wave entry and every summon target must be present. */
  enemyRows: Record<string, any>;
  waves: WaveDef[];
  /** "dungeon": dungeon floor (waves, forceKeepPools, dungeon outcome). "quest": one QUEST battle, all enemies at once. */
  mode: "dungeon" | "quest";
  runtime: { dmgConfig?: Record<string, number>; sharedCooldowns?: Record<string, number> };
  rand: () => number;
  /** Random barrier rocks as initiateBattle rolls them (10% of free cells). Default true. */
  barriers?: boolean;
  /** Fixed opening cells by row order (players first, then enemies in wave order); else seeded draw. */
  placements?: ({ x: number; y: number } | null)[];
  totalFloors?: number;
  roomKind?: string;
};

export const assemble = async (o: AssembleOpts): Promise<CompleteBattle> => {
  const battleType = "QUEST" as never;
  const playerIds = o.players.map((p) => p.userId);
  const waves = o.mode === "quest" ? [{ aiIds: o.waves.flatMap((w) => w.aiIds), delayRounds: 0 }] : o.waves;
  const targetIds = waves.flatMap((w) => w.aiIds);
  for (const id of targetIds) if (!o.enemyRows[id]) throw new Error(`SIM: no row for AI ${id}`);
  const users = [...o.players, ...targetIds.map((id) => o.enemyRows[id])].map((u) => structuredClone(u));
  // Companion pets ride on player rows (model.playerRow); hand them to the engine's pet preload as initiateBattle does.
  const simPets = users.flatMap((u) => u._simPets ?? []);
  for (const u of users) delete u._simPets;
  const petPreload = simPets.length
    ? {
        pets: simPets.map((p: any) => p.pet),
        ownerRanks: Object.fromEntries(o.players.map((p) => [p.userId, p.rank])),
        abilitiesByOwner: Object.fromEntries(o.players.map((p) => [p.userId, {
          jutsus: simPets.filter((x: any) => x.pet.userId === p.userId).flatMap((x: any) => x.jutsus), skills: [],
        }])),
        // a solo dungeon run brings its chosen pair (DUNGEON_SOLO_PETS); otherwise the active pet joins
        selectedPetIdsByOwner: o.mode === "dungeon" && playerIds.length === 1 && simPets.length > 1
          ? { [playerIds[0]!]: simPets.map((x: any) => x.pet.id) } : undefined,
      }
    : undefined;
  for (const u of users) capUserStats(u, u.rank);
  // initiateBattle reads summon templates from the DB into one shared cache; pre-seed it with the library rows.
  const summonTemplateCache = new Map<string, Promise<any[]>>();
  const need = new Set<string>();
  const scan = (rows: any[]) => {
    for (const u of rows) for (const uj of u.jutsus ?? []) for (const e of uj.jutsu?.effects ?? []) if (e.type === "summon" && e.aiId) need.add(e.aiId);
  };
  scan(users);
  for (let grew = true; grew; ) {
    grew = false;
    for (const id of [...need]) {
      if (summonTemplateCache.has(id)) continue;
      const row = o.enemyRows[id];
      if (!row) throw new Error(`SIM: summon template ${id} has no live record; read it with profile.getAi + ai.getAiProfile`);
      summonTemplateCache.set(id, Promise.resolve([structuredClone(row)]));
      const before = need.size;
      scan([row]);
      if (need.size > before) grew = true;
    }
  }
  const size = getBattleSize(battleType, users[0]?.level ?? 0, playerIds.length, Math.max(...waves.map((w) => w.aiIds.length)), true);
  if (!size) throw new Error("SIM: too many fighters for the battlefield");
  const { width, height } = size;
  const common = {
    settings: [], relations: [], wars: [], villages: [], defaultProfile: defaultProfile as never,
    battleType, width, height, hide: false, isSummon: false, summonTemplateCache,
  };
  const firstCount = playerIds.length + (waves[0]?.aiIds.length ?? 0);
  const processed = await processUsersForBattle(noDbClient, {
    ...common, users: users.slice(0, firstCount), leftSideUserIds: playerIds, leftSideUserCount: playerIds.length, petPreload,
  } as never);
  const { userEffects, usersState, extraState } = processed;
  const groundEffects = [...(processed.groundEffects ?? [])];
  // Spawn cells: the engine draws them with an unseedable source; redraw over the same spawn list with the seed.
  const taken: { x: number; y: number }[] = [];
  let slot = 0;
  for (const u of usersState) {
    if (u.isSummon) continue;
    const fixed = o.placements?.[slot++];
    const loc = fixed ?? (() => {
      const free = getBattleSpawnLocations(width, height, u.direction).filter((l) => !taken.some((t) => t.x === l.x && t.y === l.y));
      return free[Math.floor(o.rand() * free.length)]!;
    })();
    taken.push(loc);
    u.longitude = loc.x;
    u.latitude = loc.y;
  }
  // Pets were placed next to their owner's engine-drawn cell; put them back beside the redrawn one.
  for (const pet of usersState.filter((u: any) => u.petId)) {
    const owner = usersState.find((u) => u.userId === pet.controllerId)!;
    const spawn = simPets.find((x: any) => x.pet.id === (pet as any).petId)?.pet.spawnPosition;
    pet.longitude = -9;
    pet.latitude = -9;
    const loc = getPetSpawnLocation(owner, spawn, usersState, width, height);
    if (!loc) throw new Error(`SIM: no free cell for pet ${pet.username}`);
    pet.longitude = loc.x;
    pet.latitude = loc.y;
  }
  if (waves.length > 1) {
    let offset = firstCount;
    const encounter = await prepareEncounterWaves(waves as never, { usersState, userEffects, extraState }, async (wave: any) => {
      const prepared = await processUsersForBattle(noDbClient, {
        ...common, users: users.slice(offset, offset + wave.aiIds.length), leftSideUserCount: 0,
      } as never);
      offset += wave.aiIds.length;
      return prepared;
    });
    extraState.encounter = encounter;
  }
  if (o.mode === "dungeon") {
    extraState.dungeon = {
      runId: "sim-run", runVersion: 1, runState: {} as never, totalFloors: o.totalFloors ?? 1, roomKind: (o.roomKind ?? "floor") as never,
      expiresAt: Date.now() + 1e12, // the run's wall-clock deadline is outside the battle
      lastActionRound: Object.fromEntries(playerIds.map((id) => [id, 0])),
    };
  }
  for (const u of usersState) if (!u.isAi && !u.isSummon) u.isAutoCombat = true;
  syncPoolAdjustments(usersState, userEffects);
  refreshMasteries(usersState, userEffects);
  if (usersState[0]) usersState[0].isAggressor = true;
  if (o.barriers !== false) groundEffects.push(...rollStartingGroundEffects([{ id: "sim-rock", type: "STATIC" }], { width, height }, usersState));
  usersState.sort((a, b) => b.initiative - a.initiative);
  const now = new Date();
  return {
    id: "sim-battle", battleType, background: "default", usersState, usersEffects: userEffects, groundEffects, width, height,
    extraState: {
      ...extraState,
      jutsus: { ...extraState.jutsus, [SAGE_MODE_ACTIVATION_JUTSU_ID]: SAGE_MODE_ACTIVATION_JUTSU },
      settings: [],
      ...(o.runtime.dmgConfig ? { dmgConfig: o.runtime.dmgConfig } : {}),
      ...(o.runtime.sharedCooldowns ? { sharedCooldowns: o.runtime.sharedCooldowns } : {}),
    },
    rewardScaling: 1, createdAt: now, updatedAt: now, roundStartAt: now,
    activeUserId: playerIds[0], forceKeepPools: o.mode === "dungeon", round: 1, version: 1,
  } as unknown as CompleteBattle;
};

/* ------------------------------------------------------------------------ */
/* Turn loop                                                                */
/* ------------------------------------------------------------------------ */

export type Step = {
  round: number;
  wave: number;
  actor: string; // username
  aiId: string; // controllerId (AI template id, or player id)
  human: boolean;
  actionId: string | null;
  action: string | null; // action name
  at: string | null; // target tile, e.g. "I2" (column letter, row number) as battle logs print it
  texts: string[]; // the engine's action-effect lines, as the battle log shows them
  hp: Record<string, number>; // HP change per username over the step
  dodge?: boolean;
  forced?: boolean;
  issue?: string;
};

export type FightResult = {
  outcome: "won" | "lost" | "stalled";
  rounds: number;
  steps: Step[];
  final: Record<string, { hp: number; maxHp: number; cp: number; maxCp: number; sp: number; maxSp: number; alive: boolean }>;
  enemyDeaths: Record<string, number | null>; // username#n -> round
  /** Why the dungeon ended the floor early (inactivity, deadline), if it did. */
  failedReason?: string;
};

/** A forced action for a human turn: an action id and a target tile. "auto" lets the profile rules act. */
export type Forced = { actionId: string; x: number; y: number } | "auto";
export type Driver = (b: CompleteBattle, actor: any) => Forced;

export const tile = (x: number, y: number) => `${String.fromCharCode(65 + x)}${y + 1}`;
export const parseTile = (t: string) => ({ x: t.charCodeAt(0) - 65, y: Number(t.slice(1)) - 1 });

export type Policy = {
  /** Step out of enemy telegraphs: a player standing on an enemy ground mark walks to the nearest unmarked hex first. */
  dodge?: boolean;
  /** staticAnimation ids that count as a telegraph; empty or absent = any enemy ground effect with a staticAnimation. */
  dangerAnimations?: string[];
};

export const runFight = (battle: CompleteBattle, opts: { maxRounds: number; policy?: Policy; driver?: Driver }): FightResult => {
  let b = battle;
  const humans = () => b.usersState.filter((u) => !u.isAi && !u.isSummon);
  const suid = humans()[0]!.userId;
  const grid = getBattleGrid(1, b);
  const actionRounds: number[] = [];
  const steps: Step[] = [];
  const names = new Map<string, string>();
  const counts = new Map<string, number>();
  /** Stable display names: "Rogue Shinobi#2" when a name repeats (summon copies count separately, as "Name (summon)"). */
  const nameOf = (u: any) => {
    if (!names.has(u.userId)) {
      const base = u.isSummon && !u.petId ? `${u.username} (summon)` : u.username;
      const n = (counts.get(base) ?? 0) + 1;
      counts.set(base, n);
      const dupes = battle.usersState.filter((x) => x.username === u.username && !!x.isSummon === !!u.isSummon).length;
      names.set(u.userId, dupes > 1 || n > 1 || (u.isAi && !u.isSummon && !u.petId) ? `${base}#${n}` : base);
    }
    return names.get(u.userId)!;
  };
  for (const u of battle.usersState) if (!u.isSummon || u.petId) nameOf(u);
  const enemyDeaths: Record<string, number | null> = {};
  let failedReason: string | undefined;
  const outcomeOf = (): "won" | "lost" | null => {
    if (b.extraState.dungeon) {
      const d = dungeonBattleOutcome(b);
      if (d === "ended") failedReason = b.extraState.dungeon.failedReason ?? "ended";
      return d === "won" ? "won" : d ? "lost" : null;
    }
    if (!humans().some((u) => stillInBattle(u, b.usersEffects))) return "lost";
    if (!b.usersState.some((u) => u.direction === "right" && !u.isSummon && stillInBattle(u, b.usersEffects))) return "won";
    return null;
  };
  const wave = () => (b.extraState.encounter as any)?.wave ?? 1;
  const danger = new Set(opts.policy?.dangerAnimations ?? []);
  const marked = () => {
    const out = new Set<string>();
    const friendly = new Set(b.usersState.filter((u) => u.direction === "left").map((u) => u.userId));
    for (const e of b.groundEffects as any[]) {
      if (e.creatorId === "ground" || friendly.has(e.creatorId) || !e.staticAnimation) continue;
      if (danger.size && !danger.has(e.staticAnimation)) continue;
      if ((e.rounds ?? 0) <= 0 && !e.castThisRound) continue;
      out.add(`${e.longitude},${e.latitude}`);
    }
    return out;
  };
  /** Nearest free unmarked hex within 3 steps (BFS), ties broken towards the closest enemy. */
  const escape = (actor: any, marks: Set<string>) => {
    const hexes = grid.toArray();
    const at = (x: number, y: number) => hexes.find((h: any) => h.col === x && h.row === y);
    const start = at(actor.longitude, actor.latitude);
    if (!start) return null;
    const blocked = new Set<string>();
    for (const u of b.usersState) if (u.userId !== actor.userId && stillInBattle(u, b.usersEffects)) blocked.add(`${u.longitude},${u.latitude}`);
    for (const e of b.groundEffects as any[]) if (e.type === "barrier") blocked.add(`${e.longitude},${e.latitude}`);
    const foes = b.usersState.filter((u) => u.direction !== actor.direction && stillInBattle(u, b.usersEffects)).map((u) => at(u.longitude, u.latitude)).filter(Boolean);
    const dFoe = (h: any) => Math.min(99, ...foes.map((f: any) => grid.distance(h, f)));
    const dist = new Map<any, number>([[start, 0]]);
    const queue = [start];
    const found: any[] = [];
    while (queue.length) {
      const h = queue.shift();
      const d = dist.get(h)!;
      if (d > 0 && !marks.has(`${h.col},${h.row}`)) found.push(h);
      if (d >= 3) continue;
      for (const n of hexes) {
        if (dist.has(n) || grid.distance(h, n) !== 1 || blocked.has(`${n.col},${n.row}`)) continue;
        dist.set(n, d + 1);
        queue.push(n);
      }
    }
    if (!found.length) return null;
    const minD = Math.min(...found.map((h) => dist.get(h)!));
    const best = found.filter((h) => dist.get(h) === minD).sort((p, q) => dFoe(p) - dFoe(q) || p.col - q.col || p.row - q.row)[0];
    // first hop on the way there
    let hop = best;
    while (dist.get(hop)! > 1) hop = hexes.find((n: any) => grid.distance(n, hop) === 1 && dist.get(n) === dist.get(hop)! - 1);
    return hop;
  };

  let outcome: FightResult["outcome"] = "stalled";
  advanceEncounterWave(b, !!outcomeOf());
  const maxSteps = opts.maxRounds * 60;
  for (let n = 0; n < maxSteps; n++) {
    const pre = alignBattle(b, actionRounds, suid);
    if (pre.progressRound) applySageModeAfterRoundTransition(b);
    if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
    if (b.round > opts.maxRounds) break;
    const actor = pre.actor;
    const isHuman = !actor.isAi && !actor.isSummon;
    const hpBefore = new Map(b.usersState.map((u) => [u.userId, u.curHealth]));
    for (const u of b.usersState) nameOf(u);
    const waveAtStep = wave();
    tickClock(1000);
    let forced: Forced = "auto";
    if (isHuman && opts.driver) forced = opts.driver(b, actor);
    let actionId: string | null = null;
    let texts: string[] = [];
    let at: string | null = null;
    let dodged = false;
    let issue: string | undefined;
    if (forced !== "auto") {
      const action = availableUserActions(b as never, actor.userId, true, true).find((a: any) => a.id === forced.actionId);
      try {
        if (!action) throw new Error("action not available");
        const res = performBattleAction({ battle: b, action, grid, actorId: actor.userId, longitude: forced.x, latitude: forced.y });
        b = res.newBattle;
        actionId = action.id;
        at = tile(forced.x, forced.y);
        texts = res.actionEffects.map((e: any) => e.txt);
      } catch (err) {
        issue = `${forced.actionId} at ${tile(forced.x, forced.y)}: ${(err as Error).message}`.slice(0, 200);
        // keep the fight moving: fall back to the profile rules for this step
        forced = "auto";
      }
    }
    if (forced === "auto") {
      let restore: (() => void) | null = null;
      if (isHuman && opts.policy?.dodge) {
        const marks = marked();
        if (marks.has(`${actor.longitude},${actor.latitude}`)) {
          const hop = escape(actor, marks);
          const profile = (b.extraState.aiProfiles as any)?.[actor.aiProfileId];
          if (hop && profile) {
            const saved = profile.rules;
            profile.rules = [{ conditions: [], action: { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: hop.col, latitude: hop.row }, description: "sim: step out of a telegraph" } }];
            dodged = true;
            restore = () => {
              profile.rules = saved;
              const np = (b.extraState.aiProfiles as any)?.[actor.aiProfileId];
              if (np) np.rules = saved;
            };
          }
        }
      }
      const res = performAIaction(b, grid, actor.userId);
      b = res.nextBattle;
      restore?.();
      actionId = res.nextActionId ?? null;
      texts = res.nextActionEffects.map((e: any) => e.txt);
      if (!res.nextActionId && actor.isAutoCombat) b.roundStartAt = new Date(Date.now() - 61_000); // idle auto turn times out
    }
    if (actionId && b.extraState.dungeon && isHuman) b.extraState.dungeon.lastActionRound[actor.userId] = pre.actionRound;
    const post = alignBattle(b, actionRounds, suid);
    if (post.progressRound) applySageModeAfterRoundTransition(b);
    if (!actionRounds.includes(post.actionRound)) actionRounds.push(post.actionRound);
    const hp: Record<string, number> = {};
    for (const u of b.usersState) {
      const d = Math.round((u.curHealth - (hpBefore.get(u.userId) ?? u.curHealth)) * 100) / 100;
      if (d) hp[nameOf(u)] = d;
    }
    const jName = actionId ? ((b.extraState.jutsus as any)?.[actionId]?.name ?? actionId) : null;
    steps.push({
      round: pre.actionRound, wave: waveAtStep, actor: nameOf(actor), aiId: actor.controllerId, human: isHuman,
      actionId, action: jName, at, texts, hp,
      ...(dodged ? { dodge: true } : {}), ...(opts.driver && isHuman && !issue && forced !== "auto" ? { forced: true } : {}), ...(issue ? { issue } : {}),
    });
    for (const u of b.usersState)
      if (u.isAi && !u.isSummon && u.direction === "right") {
        const k = nameOf(u);
        if (!(k in enemyDeaths)) enemyDeaths[k] = null;
        if (enemyDeaths[k] === null && !stillInBattle(u, b.usersEffects)) enemyDeaths[k] = pre.actionRound;
      }
    advanceEncounterWave(b, !!outcomeOf());
    const out = outcomeOf();
    if (out) {
      outcome = out;
      break;
    }
  }
  const final: FightResult["final"] = {};
  for (const u of b.usersState)
    if (!u.isSummon) final[nameOf(u)] = { hp: u.curHealth, maxHp: u.maxHealth, cp: u.curChakra, maxCp: u.maxChakra, sp: u.curStamina, maxSp: u.maxStamina, alive: stillInBattle(u, b.usersEffects) };
  return { outcome, rounds: b.round, steps, final, enemyDeaths, ...(failedReason ? { failedReason } : {}) };
};

export { isEffectActive };
