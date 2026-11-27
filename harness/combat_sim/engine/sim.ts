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
 * Each step is recorded as the router records a history entry: [effects expired before the action, the action's effects,
 *   effects expired after it, "<summon> vanishes without its summoner!" notices], with the router's description text.
 * Results come from the engine's own settlement: calcBattleResult per human participant after every step, as the
 *   router and each participant's poll call it; the fight is over when every human has a result.
 *
 * Determinism: Math.random is the run's seeded generator, crypto.getRandomValues is seeded separately (ids minted
 * mid-battle), the clock is virtual, and the router's node:crypto randomInt (opening spawn cells) is pointed at a
 * seeded source by entropy_plugin.ts, so the engine places fighters, pets and pet passives itself. Fixed opening
 * cells (a log replay) are chosen by feeding that source the index of the wanted cell in the engine's own spawn list.
 */
import { randomInt as seededRandomInt, setRandomIntSource } from "./entropy";
import { nanoid } from "nanoid";
import { availableUserActions, performBattleAction } from "@/libs/combat/actions";
import { performAIaction } from "@/libs/combat/ai_v2";
import { advanceEncounterWave, prepareEncounterWaves } from "@/libs/combat/encounters";
import { stillInBattle } from "@/libs/combat/inBattle";
import { rollStartingGroundEffects } from "@/libs/combat/initiation";
import { refreshMasteries } from "@/libs/combat/mastery";
import { getBattleSpawnLocations } from "@/libs/combat/participants";
import { calcBattleResult } from "@/libs/combat/settlement";
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

let defaultSpawnSource: ((span: number) => number) | null = null;

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
  // the router's node:crypto randomInt (opening spawn cells) gets its own seeded stream
  const spawn = mulberry32((seed ^ 0x59a7) >>> 0);
  defaultSpawnSource = (span) => Math.floor(spawn() * span);
  setRandomIntSource(defaultSpawnSource);
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
  /** Random barrier rocks as initiateBattle rolls them (10% of free cells). Default true. */
  barriers?: boolean;
  /** Fixed opening cells by row order (players first, then wave-1 enemies); null or absent = the engine's seeded draw. */
  placements?: ({ x: number; y: number } | null)[];
  /** Players act through a driver (human action path) instead of auto combat: isAutoCombat false, as in a logged fight. */
  manualPlayers?: boolean;
  totalFloors?: number;
  roomKind?: string;
};

/** The engine's draw order for opening cells (combat.ts processUsersForBattle): input order, per side, minus taken cells. */
const spawnPlan = (users: any[], leftCount: number, placements: ({ x: number; y: number } | null)[], width: number, height: number) => {
  const taken: { x: number; y: number }[] = [];
  return users.map((u, i) => {
    const direction = i < leftCount ? "left" : "right";
    const free = getBattleSpawnLocations(width, height, direction as never).filter((l) => !taken.some((t) => t.x === l.x && t.y === l.y));
    const want = placements[i];
    const index = want ? free.findIndex((l) => l.x === want.x && l.y === want.y) : defaultSpawnSource!(free.length);
    if (index < 0) throw new Error(`SIM: ${u.username} placement ${tile(want!.x, want!.y)} is not a free ${direction} spawn cell`);
    taken.push(free[index]!);
    return { index, of: free.length, cell: free[index]! };
  });
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
  void seededRandomInt; // entropy.ts must be loaded (and shared with the router) before assembly
  const common = {
    settings: [], relations: [], wars: [], villages: [], defaultProfile: defaultProfile as never,
    battleType, width, height, hide: false, isSummon: false, summonTemplateCache,
  };
  const firstCount = playerIds.length + (waves[0]?.aiIds.length ?? 0);
  // Fixed cells: give the router's spawn draw the index of each wanted cell in the list it draws from.
  const plan = o.placements?.some(Boolean) ? spawnPlan(users.slice(0, firstCount), playerIds.length, o.placements, width, height) : null;
  if (plan) {
    const queue = plan.map((p) => p.index);
    const lengths = plan.map((p) => p.of);
    setRandomIntSource((span) => {
      const k = queue.shift();
      const want = lengths.shift();
      if (k === undefined) return defaultSpawnSource!(span);
      if (span !== want) throw new Error(`SIM: spawn draw over ${span} cells, planned ${want}`);
      return k;
    });
  }
  let processed: Awaited<ReturnType<typeof processUsersForBattle>>;
  try {
    processed = await processUsersForBattle(noDbClient, {
      ...common, users: users.slice(0, firstCount), leftSideUserIds: playerIds, leftSideUserCount: playerIds.length, petPreload,
    } as never);
  } finally {
    setRandomIntSource(defaultSpawnSource);
  }
  const { userEffects, usersState, extraState } = processed;
  const groundEffects = [...(processed.groundEffects ?? [])];
  if (plan) {
    const opening = usersState.filter((u) => !u.isSummon);
    plan.forEach((p, i) => {
      const u = opening[i];
      if (!u || u.longitude !== p.cell.x || u.latitude !== p.cell.y)
        throw new Error(`SIM: ${u?.username ?? `fighter ${i}`} opened at ${u ? tile(u.longitude, u.latitude) : "-"}, planned ${tile(p.cell.x, p.cell.y)}`);
    });
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
  for (const u of usersState) if (!u.isAi && !u.isSummon) u.isAutoCombat = !o.manualPlayers;
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
  actor: string; // display name (Name#n when a name repeats)
  aiId: string; // controllerId (AI template id, or player id)
  /** The battle userId the router records for this entry (performedByUserId ?? actor.userId). */
  userId: string;
  human: boolean;
  actionId: string | null; // the router records "unknown" when nothing was performed
  action: string | null; // action name
  at: string | null; // forced target tile, e.g. "I2" (column letter, row number) as battle logs print it
  /** The router's history description for this entry, "It is now X's turn." included; null when it records no entry. */
  description: string | null;
  /** The history entry's applied effects in the router's order: pre-action expiry, action, post-action expiry, orphans. */
  texts: string[];
  /** Only the action's own effect lines (what the actor's action processing emitted). */
  actionTexts: string[];
  hp: Record<string, number>; // HP change per display name over the step, expiry included
  dodge?: boolean;
  forced?: boolean;
  /** The human turn timed out with nothing performed (no history entry). */
  idle?: boolean;
  issue?: string;
};

export type ParticipantResult = { outcome: string; settledRound: number };

export type FightResult = {
  /** won: some human participant's settlement says Won. lost: every human settled without a win. stalled: round cap. */
  outcome: "won" | "lost" | "stalled";
  rounds: number;
  steps: Step[];
  /** calcBattleResult per human participant (display name), from the pinned settlement code. */
  participants: Record<string, ParticipantResult>;
  final: Record<string, { hp: number; maxHp: number; cp: number; maxCp: number; sp: number; maxSp: number; alive: boolean }>;
  enemyDeaths: Record<string, number | null>; // display name -> round
  /** Opening cells per display name, as the engine placed them (pets included). */
  opening: Record<string, string>;
  /** Why the dungeon ended the floor early (inactivity, deadline), if it did. */
  failedReason?: string;
};

/** A forced action for a human turn: an action id and a target tile. "auto": the profile rules act. "idle": let the turn time out. */
export type Forced = { actionId: string; x: number; y: number } | "auto" | "idle";
export type Driver = (b: CompleteBattle, actor: any) => Forced;

export const tile = (x: number, y: number) => `${String.fromCharCode(65 + x)}${y + 1}`;
export const parseTile = (t: string) => ({ x: t.charCodeAt(0) - 65, y: Number(t.slice(1)) - 1 });

export type Policy = {
  /** Step out of enemy telegraphs: a player standing on an enemy ground mark walks to the nearest unmarked hex first. */
  dodge?: boolean;
  /** staticAnimation ids that count as a telegraph; empty or absent = any enemy ground effect with a staticAnimation. */
  dangerAnimations?: string[];
};

const ROUND_TIMEOUT_MS = 61_000;

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
  const opening: Record<string, string> = {};
  for (const u of battle.usersState)
    if (!u.isSummon || u.petId) opening[nameOf(u)] = tile(u.longitude, u.latitude);
  const enemyDeaths: Record<string, number | null> = {};
  const participants: Record<string, ParticipantResult> = {};
  /** The router's settlement, per human, as performAction (acting user) and each participant's poll call it. */
  const settle = (round: number) => {
    for (const u of humans()) {
      const k = nameOf(u);
      if (participants[k]) continue;
      const r = calcBattleResult(b, u.userId, b.extraState.settings);
      if (r) participants[k] = { outcome: r.outcome, settledRound: round };
    }
    const hs = humans().map(nameOf);
    if (!hs.every((k) => participants[k])) return null;
    return hs.some((k) => participants[k]!.outcome === "Won") ? ("won" as const) : ("lost" as const);
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
  advanceEncounterWave(b, !!dungeonBattleOutcome(b));
  const maxSteps = opts.maxRounds * 60;
  for (let n = 0; n < maxSteps; n++) {
    // combat.performAction inner loop: alignBattle (it runs the round transition, sage exhaustion included)
    const pre = alignBattle(b, actionRounds, suid);
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
    let performedActionId: string | null = null;
    let actionTexts: string[] = [];
    const descriptions: string[] = [];
    let at: string | null = null;
    let dodged = false;
    let issue: string | undefined;
    let actionPerformed = false;
    let idle = false;
    if (forced === "idle") {
      // a manual turn with nothing to do: the round timer runs out (no history entry)
      b.roundStartAt = new Date(Date.now() - ROUND_TIMEOUT_MS);
      idle = true;
    } else if (forced !== "auto") {
      // the router's human action path
      const action = availableUserActions(b as never, actor.userId, true, true).find((a: any) => a.id === forced.actionId);
      try {
        if (!action) throw new Error("action not available");
        const res = performBattleAction({ battle: b, action, grid, actorId: actor.userId, longitude: forced.x, latitude: forced.y });
        b = res.newBattle;
        actionPerformed = true;
        performedActionId = action.id;
        at = tile(forced.x, forced.y);
        actionTexts = res.actionEffects.map((e: any) => e.txt);
        descriptions.push(action.battleDescription);
      } catch (err) {
        issue = `${forced.actionId} at ${tile(forced.x, forced.y)}: ${(err as Error).message}`.slice(0, 200);
        // the router answers with a notification and changes nothing; let the turn time out
        b.roundStartAt = new Date(Date.now() - ROUND_TIMEOUT_MS);
        idle = true;
      }
    } else {
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
      // the router's AI path (AI, summons, and humans on auto combat)
      const res = performAIaction(b, grid, actor.userId);
      b = res.nextBattle;
      restore?.();
      actionPerformed = true;
      performedActionId = res.nextActionId ?? null;
      actionTexts = res.nextActionEffects.map((e: any) => e.txt);
      descriptions.push(...(res.aiDescriptions ?? []));
      if (!res.nextActionId && actor.isAutoCombat) b.roundStartAt = new Date(Date.now() - ROUND_TIMEOUT_MS); // idle auto turn times out
    }
    if (performedActionId && b.extraState.dungeon && isHuman) b.extraState.dungeon.lastActionRound[actor.userId] = pre.actionRound;
    const post = alignBattle(b, actionRounds, suid);
    if (!actionRounds.includes(post.actionRound)) actionRounds.push(post.actionRound);
    // history entry as performAction builds it
    let description = descriptions.join(". ");
    const texts = [
      ...pre.expiredEffects.map((e: any) => e.txt),
      ...actionTexts,
      ...post.expiredEffects.map((e: any) => e.txt),
      ...post.orphanedSummons.map((u: string) => `${u} vanishes without its summoner!`),
    ];
    if (actionPerformed && post.progressRound) {
      const dot = description.endsWith(".");
      description += `${dot ? "" : ". "} It is now ${post.actor.username}'s turn.`;
    }
    const recorded = !!(description || texts.length);
    const hp: Record<string, number> = {};
    for (const u of b.usersState) {
      const d = Math.round((u.curHealth - (hpBefore.get(u.userId) ?? u.curHealth)) * 100) / 100;
      if (d) hp[nameOf(u)] = d;
    }
    const jName = performedActionId ? ((b.extraState.jutsus as any)?.[performedActionId]?.name ?? performedActionId) : null;
    steps.push({
      round: pre.actionRound, wave: waveAtStep, actor: nameOf(actor), aiId: actor.controllerId, userId: actor.userId, human: isHuman,
      actionId: recorded ? (performedActionId ?? "unknown") : null, action: jName, at,
      description: recorded ? description || "Battlefield effects expire." : null, texts, actionTexts, hp,
      ...(dodged ? { dodge: true } : {}), ...(opts.driver && isHuman && forced !== "auto" && !idle ? { forced: true } : {}),
      ...(idle ? { idle: true } : {}), ...(issue ? { issue } : {}),
    });
    for (const u of b.usersState)
      if (u.isAi && !u.isSummon && u.direction === "right") {
        const k = nameOf(u);
        if (!(k in enemyDeaths)) enemyDeaths[k] = null;
        if (enemyDeaths[k] === null && !stillInBattle(u, b.usersEffects)) enemyDeaths[k] = pre.actionRound;
      }
    const spawnedWave = advanceEncounterWave(b, !!dungeonBattleOutcome(b));
    // a transformation is its own history entry in the router
    const form = spawnedWave ? b.usersState.find((u: any) => u.transformation && !u.leftBattle && stillInBattle(u)) : undefined;
    if (form)
      steps.push({
        round: pre.actionRound, wave: wave(), actor: nameOf(form), aiId: form.controllerId, userId: form.userId, human: false,
        actionId: "unknown", action: null, at: null, description: (form as any).transformation?.log ?? "", texts: [], actionTexts: [], hp: {},
      });
    const out = settle(pre.actionRound);
    if (out) {
      outcome = out;
      break;
    }
  }
  const final: FightResult["final"] = {};
  for (const u of b.usersState)
    if (!u.isSummon) final[nameOf(u)] = { hp: u.curHealth, maxHp: u.maxHealth, cp: u.curChakra, maxCp: u.maxChakra, sp: u.curStamina, maxSp: u.maxStamina, alive: stillInBattle(u, b.usersEffects) };
  const failedReason = b.extraState.dungeon && dungeonBattleOutcome(b) === "ended" ? (b.extraState.dungeon.failedReason ?? "ended") : undefined;
  return { outcome, rounds: b.round, steps, participants, final, enemyDeaths, opening, ...(failedReason ? { failedReason } : {}) };
};

export { isEffectActive };
