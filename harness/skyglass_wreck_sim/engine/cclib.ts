/**
 * Crownhold boss fights: shared harness pieces (records, the set-piece library, AI rows, the solo fight
 * runner with the dodging auto-player, aggregation). Used by crowned_captain.ts and crownhold.ts.
 *
 * Fight model: one "average" endgame player (engine/model.ts) vs one Crownhold AI in a plain QUEST battle
 * (12 x 10), the engine's own turn loop (alignBattle -> performAIaction), live damage settings.
 * Dodge rule (declared test input, executed through the engine's Move / Replacement Technique / Cleanse):
 *   1. at each player action step, if they stand on a live danger mark (tg_heavy / tg_control ground
 *      visual laid by the boss), step to the nearest unmarked free hex (Replacement Technique when 2+ steps
 *      away, within 5 and ready; else one Move step); if rooted, the basic Cleanse first;
 *   2. never end a move on a marked hex (an auto-combat move onto one is replaced by ending the turn).
 */
import { join } from "node:path";
import { performAIaction } from "@/libs/combat/ai_v2";
import { availableUserActions, actionPointsAfterAction, performBattleAction, stillInBattle } from "@/libs/combat/actions";
import { applySageModeAfterRoundTransition } from "@/libs/combat/process";
import { addQuestStartingEffects } from "@/libs/combat/questEffects";
import { getTargetTiles } from "@/libs/combat/targeting";
import { alignBattle, getBattleGrid, getDefaultBattleSizes, getEffectiveMaxPool } from "@/libs/combat/util";
import { StatTypes } from "@/drizzle/constants";
import { AiRule } from "@/validators/ai";
import { insertAiSchema } from "@/validators/aiInput";
import { JutsuValidator } from "@/validators/combat";
import { buildTemplates, enemyQueryUser, loadDmgConfig, loadJson, PLAYER_VARIANTS, playerQueryUser, playerRules, queryShell } from "./model";
import { assembleFloor, mulberry32 } from "./sim";

export const args = process.argv.slice(2);
export const opt = (k: string, d?: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : d;
};
export const H = process.env.TNR_HARNESS!;
export const IN = loadJson(join(H, "data/crownhold_inputs.json"));
const baseline = loadJson(join(H, "data/baseline.json"));
export const dmg = loadDmgConfig(H, opt("dmg-config", "live"));

/* ------------------------------------------------------------------ geometry */
export const SIZE = getDefaultBattleSizes("QUEST" as never, 100)!;
export const GRID = getBattleGrid(1, { width: SIZE.width, height: SIZE.height } as never);
export type Cell = [number, number];
export const hexAt = (c: Cell) => GRID.getHex({ col: c[0], row: c[1] })!;
export const dist = (a: Cell, b: Cell) => GRID.distance(hexAt(a), hexAt(b));
export const ALL: Cell[] = GRID.toArray().map((h) => [h.col, h.row] as Cell);
export const key = (c: Cell) => `${c[0]},${c[1]}`;
/** Hex 3-colouring: each hex's six neighbours carry the other two colours. */
export const color = (c: Cell) => {
  const h = hexAt(c);
  return (((h.q - h.r) % 3) + 3) % 3;
};
/** Cube line between two hexes (axial lerp + round), excluding the start. */
export const lineCells = (a: Cell, b: Cell): Cell[] => {
  const A = hexAt(a);
  const B = hexAt(b);
  const n = GRID.distance(A, B);
  const out: Cell[] = [];
  for (let i = 1; i <= n; i++) {
    const t = i / n;
    const q = A.q + (B.q - A.q) * t + 1e-6;
    const r = A.r + (B.r - A.r) * t + 1e-6;
    const s = -q - r;
    let rq = Math.round(q), rr = Math.round(r);
    const rs = Math.round(s);
    const dq = Math.abs(rq - q), dr = Math.abs(rr - r), ds = Math.abs(rs - s);
    if (dq > dr && dq > ds) rq = -rr - rs;
    else if (dr > ds) rr = -rq - rs;
    const h = GRID.getHex({ q: rq, r: rr });
    if (h) out.push([h.col, h.row]);
  }
  return out;
};
export const uniq = (cs: Cell[]) => [...new Map(cs.map((c) => [key(c), c])).values()];

/* ------------------------------------------------------------------ records */
export const J = (id: string) => structuredClone(IN.jutsu[id]?.record ?? IN.oldKit[id]?.record);
const TEMPLATE = J("EQ93LX8wvuIAd5u75q_i1"); // Ruin Refrain: a complete captured AI jutsu row (field-set donor)
export const DONOR_SUMMON = J(IN.donors.summon);
export const IMG = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp";

export const tagBase = (type: string, over: Record<string, unknown> = {}) => ({
  type, power: 1, powerPerLevel: 0, rounds: 0, target: "INHERIT", direction: "offence", calculation: "static",
  description: "", appearSfx: "", disappearSfx: "", appearAnimation: "", staticAnimation: "", staticAssetPath: "",
  disappearAnimation: "", ...over,
});
export const coords = (cells: Cell[], selection: "ALL" | "EXCLUDE" = "ALL", origin: "BATTLEFIELD" | "CASTER" = "BATTLEFIELD") => ({
  origin, selection, coordinates: cells.map((c) => ({ longitude: c[0], latitude: c[1] })), randomCount: 1,
});
export const fx = {
  visual: (anim: string, rounds: number, ct?: ReturnType<typeof coords>) => tagBase("visual", {
    rounds, staticAnimation: anim, description: "A battlefield visual effect",
    ...(ct ? { target: "COORDINATES", coordinateTargeting: ct } : {}),
  }),
  /** Primed marker on the caster, 1 round; one harmless effect TYPE per library mark (MARKER). */
  marker: (type: string, anim = "") => tagBase(type, {
    power: ["increaseaggro", "decreaseaggro", "increasecooldown", "decreasecooldown", "increaserange"].includes(type) ? 1 : 100,
    rounds: 1, target: "SELF", appearAnimation: anim,
    ...(type.endsWith("aggro") ? { calculation: "percentage", aggroMode: "GENERATION" } : {}),
    ...(type.endsWith("cooldown") || type === "increaserange" ? { actionsAffected: [] } : {}),
    description: "Primed: the set piece lands next turn",
  }),
  damage: (power: number, anim: string) => tagBase("damage", {
    power, calculation: "formula", appearAnimation: anim, friendlyFire: "ENEMIES", description: "Deals damage",
    statTypes: ["None"], generalTypes: ["Highest"], elements: [], dmgModifier: 1, residualModifier: 1,
    allowBloodlineDamageDecrease: true, allowBloodlineDamageIncrease: true,
  }),
  stun: (ap: number, rounds: number) => tagBase("stun", { power: 100, rounds, apReduction: ap, friendlyFire: "ENEMIES", description: "Stuns the target" }),
  seal: (rounds: number) => tagBase("seal", { power: 100, rounds, friendlyFire: "ENEMIES", description: "Seals the target's bloodline effects" }),
  /** The 1-round x3 window: weakness on SELF to every stat type. */
  weakness: (mult: number, anim = "") => tagBase("weakness", {
    target: "SELF", rounds: 1, power: 100, statTypes: [...StatTypes], dmgModifier: mult, items: [], jutsus: [], elements: [], generalTypes: [],
    staticAnimation: anim, description: "Guard lowered: takes extra damage",
  }),
};
export const jutsuRecord = (id: string, over: Record<string, unknown>) => ({
  ...structuredClone(TEMPLATE), id, image: IMG, jutsuType: "AI", jutsuRank: "S", hidden: true, injectableInBattle: false,
  battleUsageType: "BOTH", chakraCost: 0, staminaCost: 0, healthCost: 0, chakraCostReducePerLvl: 0,
  staminaCostReducePerLvl: 0, healthCostReducePerLvl: 0, extraBaseCost: 0, requiredRank: "STUDENT", requiredLevel: 1,
  statClassification: "None", elementClassification: "None", jutsuWeapon: "NONE", bloodlineId: null, villageId: null,
  methodSize: null, coordinateTargeting: null, createdAt: "2026-10-28T00:00:00.000Z", updatedAt: "2026-10-28T00:00:00.000Z",
  ...over,
});

/* ------------------------------------------------------------------ the set-piece library */
/**
 * The shared library is engine/library.ts (library_spec.json, fable/skyglass-wreck-sim 4bd5356a); its records are
 * used as they are, never copied. Usage rules (coordinator, 2026-10-28): marks cost 40 AP, blasts 100 AP; the blast
 * rule `has_effect <marker> >= 1` goes above everything else; after a mark, `has_effect <that marker>` -> plain
 * attack -> end turn, ahead of other marks; a CHARACTER blast with nobody in its pattern is not cast.
 */
export { buildLibrary as buildLibraryRecords, LIB, LIB_POWERS, MARKER_TYPES, PATTERNS } from "./library";
import { MARKER_TYPES as MT } from "./library";
/** After a mark: the rest of the turn is a plain attack, then end turn (the marker blocks a second mark). */
export const afterMark = (markKey: keyof typeof MT, attacks: any[]) => [
  ...attacks.map((a) => ({ ...a, conditions: [{ type: "has_effect", effectType: MT[markKey], threshold: 1, description: "Has effect" }, ...a.conditions] })),
  { conditions: [{ type: "has_effect", effectType: MT[markKey], threshold: 1, description: "Has effect" }], action: { type: "end_turn", description: "End turn" } },
];

/* ------------------------------------------------------------------ rules */
export const R = {
  jutsu: (jutsuId: string, target: string, conditions: any[] = [], extra: Record<string, unknown> = {}) =>
    ({ conditions, action: { type: "use_specific_jutsu", jutsuId, target, description: "Select specific jutsu", ...extra } }),
  item: (itemId: string, target: string, conditions: any[] = []) =>
    ({ conditions, action: { type: "use_specific_item", itemId, target, description: "Select specific item" } }),
  end: (conditions: any[] = []) => ({ conditions, action: { type: "end_turn", description: "End turn" } }),
  moveTo: (c: Cell) => ({ conditions: [], action: { type: "move_towards_opponent", target: "COORDINATE", coordinates: { longitude: c[0], latitude: c[1] }, description: "Move to the post" } }),
};
export const C = {
  hb: (v: number) => ({ type: "health_below", value: v, description: "Health below given percentage" }),
  has: (effectType: string, threshold = 1) => ({ type: "has_effect", effectType, threshold, description: "Has effect" }),
  tHas: (effectType: string, threshold: number) => ({ type: "target_has_effect", effectType, threshold, target: "CLOSEST_OPPONENT", description: "Target has effect" }),
  near: (v: number) => ({ type: "distance_lower_than", value: v, target: "CLOSEST_OPPONENT", description: "Distance lower than or equal given value" }),
  far: (v: number) => ({ type: "distance_higher_than", value: v, target: "CLOSEST_OPPONENT", description: "Distance higher than or equal given value" }),
  round: (v: number) => ({ type: "round_lower_than", value: v, description: "Current round is lower than specified value" }),
  noSummon: () => ({ type: "does_not_have_summon", description: "Does not have a summon active" }),
};

/* ------------------------------------------------------------------ AI rows */
export const STAT_PER_MULT = 1622255.8 / 5.83; // push/272 readback: the server computes stats from statsMultiplier
export const STATS = ["offence", "defence", "strength", "intelligence", "willpower", "speed"] as const;
export const idgRowTags = (rows: number) => [
  ...Array.from({ length: Math.floor(rows) }, () => tagBase("increasedamagegiven", { power: 100, rounds: 99, calculation: "percentage", description: "Increased damage given" })),
  ...(rows % 1 ? [tagBase("increasedamagegiven", { power: Math.round((rows % 1) * 100), rounds: 99, calculation: "percentage", description: "Increased damage given" })] : []),
];
export const t0 = buildTemplates(baseline, {});
const donorRow = enemyQueryUser(t0.enemies["texZaFi42S3EvJZBwQ8cd"]!); // Deck Warden row: DB field-set donor
const armorDonor = donorRow.items.find((ui: any) => ui.item?.itemType === "ARMOR");
const itemRecord = (id: string) => ({ ...structuredClone(IN.items["ALqXVSL58QMfJ4DgoJ5Il"].record), ...structuredClone(IN.items[id].record), id });
const itemRow = (userId: string, id: string, i: number) => {
  const rec = itemRecord(id);
  return { ...structuredClone(armorDonor), id: `cc-item-${userId.slice(0, 5)}-${i}`, userId, itemId: id, equipped: rec.slot, quantity: 1, isInAuction: false, durability: 100, imbuements: [], item: rec };
};
export const userJutsu = (userId: string, rec: any, i: number) => ({
  id: `cc-uj-${userId.slice(0, 6)}-${i}`, userId, jutsuId: rec.id, level: 1, experience: 0, equipped: true, finishTraining: null,
  reskinId: null, activeReskin: null, createdAt: new Date(0), updatedAt: new Date(0), jutsu: rec,
});
export const statsFor = (slotData: any, liveStats?: Record<string, number>, statsMultiplier?: number) =>
  statsMultiplier !== undefined && statsMultiplier !== slotData.statsMultiplier
    ? Math.round(STAT_PER_MULT * statsMultiplier * 100) / 100
    : (liveStats?.offence ?? Math.round(STAT_PER_MULT * slotData.statsMultiplier * 100) / 100);
export const aiRow = (id: string, d: any, statsEach: number, recs: Record<string, any>, rules: any[], effects: any[], items: string[]) => {
  const profile = { id: `profile-${id}`, userId: id, name: d.username, includeDefaultRules: !!d.includeDefaultRules, rules };
  return {
    ...structuredClone(donorRow), userId: id, username: d.username, level: d.level, rank: d.rank,
    poolsMultiplier: d.poolsMultiplier, statsMultiplier: d.statsMultiplier, regeneration: d.regeneration,
    maxHealth: 5050 * d.poolsMultiplier, curHealth: 5050 * d.poolsMultiplier,
    maxChakra: 5050 * d.poolsMultiplier, curChakra: 5050 * d.poolsMultiplier, maxStamina: 5050 * d.poolsMultiplier, curStamina: 5050 * d.poolsMultiplier,
    ...Object.fromEntries(STATS.map((s) => [s, statsEach])),
    ninjutsuMastery: d.ninjutsuMastery, genjutsuMastery: d.genjutsuMastery, taijutsuMastery: d.taijutsuMastery, bukijutsuMastery: d.bukijutsuMastery,
    effects: structuredClone(effects), aiProfileId: profile.id,
    items: items.filter((iid) => IN.items[iid]).map((iid, i) => itemRow(id, iid, i)),
    jutsus: d.jutsus.map((jid: string, i: number) => {
      if (!recs[jid]) throw new Error(`no record for ${jid}`);
      return userJutsu(id, structuredClone(recs[jid]), i);
    }),
    ...queryShell(profile),
  };
};
/** A Crownhold AI as live (push/272 data, live username, server stats), optionally edited. */
export const crownholdRow = (slot: string, recs: Record<string, any>, edit: Partial<{ data: any; rules: any[]; effects: any[] }> = {}) => {
  const a = IN.ais[slot];
  const d = { ...a.data, username: a.liveUsername, ...(edit.data ?? {}) };
  return aiRow(a.id, d, statsFor(a.data, a.liveStats, edit.data?.statsMultiplier), recs, edit.rules ?? a.data.rules, edit.effects ?? a.data.effects,
    a.data.items.flatMap((it: any) => it.ids));
};
export const allCapturedRecords = () => Object.fromEntries([...Object.entries<any>(IN.jutsu), ...Object.entries<any>(IN.oldKit)].map(([id, j]) => [id, structuredClone(j.record)]));

/* ------------------------------------------------------------------ validation */
export const validator = () => {
  const issues: string[] = [];
  const check = (what: string, r: { success: boolean; error?: any }) => {
    if (!r.success) issues.push(`${what}: ${JSON.stringify(r.error.issues.map((i: any) => `${i.path.join(".")}: ${i.message}`))}`);
  };
  return {
    issues,
    jutsu: (j: any) => check(`jutsu ${j.name}`, JutsuValidator.safeParse(j)),
    rule: (r: any) => check(`rule ${JSON.stringify(r.action).slice(0, 60)}`, AiRule.safeParse(r)),
    ai: (id: string, rec: any) => {
      const { rules: _r, jutsus, items, ...aiFields } = rec;
      check(`ai record ${rec.username}`, insertAiSchema.safeParse({ ...aiFields, userId: id, jutsus, items, isAi: true }));
    },
  };
};

/* ------------------------------------------------------------------ the fight */
export type SetMap = Record<string, [string, "mark" | "land"]>; // action id -> [set piece, role]
export type PlayerStart = { hpFrac?: number; cpFrac?: number; spFrac?: number; startingEffects?: any[] };
export type FightConfig = {
  bossId: string;
  rows: Record<string, any>; // boss + any summon templates, keyed by AI id
  recs: Record<string, any>;
  sets: SetMap;
  setNames: string[];
  phases?: number[]; // boss HP % thresholds to time (default 60, 30)
  anchor?: Cell; // the boss's post, if any
  special?: Record<string, string>; // label -> action id, counted per fight (e.g. recall, lastDirective, window)
  maxRounds?: number;
};
export type Fight = {
  seed: number; dodge: boolean; outcome: string; rounds: number; playerHpPct: number; bossHpPct: number;
  endHpFrac: number; endCpFrac: number; endSpFrac: number;
  phaseRounds: (number | null)[]; anchorReached: boolean;
  sets: Record<string, { mark: number; land: number; hit: number; dmg: number }>;
  special: Record<string, number>; specialFirstRound: Record<string, number | null>;
  summonDamage: number; bossIdleTurns: number; bossTurns: number; playerIdleTurns: number; playerTurns: number;
  dodgeMoves: number; blockedMoves: number; cleanses: number; dmgBySource: Record<string, number>; untelegraphedLands: number;
  trace?: string[];
};
const DANGER_ANIMS = new Set(["tg_heavy", "tg_control"]);

/** Hexes a cast's parent pattern covers, cast by the boss from where it stands (engine targeting). */
const patternCells = (grid: any, rec: any, from: Cell) => {
  const a = grid.getHex({ col: from[0], row: from[1] });
  return new Set(getTargetTiles({ a, b: a, action: rec, grid }).map((h: any) => `${h.col},${h.row}`));
};

export const runFight = async (cfg: FightConfig, seed: number, dodge: boolean, start: PlayerStart = {}, trace = false, debugfx = false): Promise<Fight> => {
  const rand = mulberry32(seed);
  const orig = Math.random;
  Math.random = rand;
  try {
    const kit = PLAYER_VARIANTS.average!.jutsuIds;
    const v = { ...PLAYER_VARIANTS.average!, rules: playerRules(kit, t0.jutsu) };
    const player = playerQueryUser(0, v as never, t0.enemies["texZaFi42S3EvJZBwQ8cd"]!.row, t0.jutsu);
    let b = await assembleFloor({
      players: [player], enemyRows: cfg.rows, floor: { kind: "boss", waves: [{ aiIds: [cfg.bossId], delayRounds: 0 }] },
      rand, initialBarriers: true, dmgConfig: dmg.config, mode: "quest",
    });
    for (const [id, r] of Object.entries(cfg.recs)) if (!(b.extraState.jutsus as any)[id]) (b.extraState.jutsus as any)[id] = r;
    const grid = getBattleGrid(1, b);
    const puid = player.userId;
    const pu0 = b.usersState.find((u) => u.userId === puid)!;
    // Quest objective effects (Alarm Raised / War Rite), as initiateBattle adds them.
    if (start.startingEffects?.length) addQuestStartingEffects(pu0 as never, b.usersEffects as never, start.startingEffects as never, "quest-crownhold");
    const maxHp = getEffectiveMaxPool(pu0 as never, b.usersEffects as never, "Health");
    const maxCp = getEffectiveMaxPool(pu0 as never, b.usersEffects as never, "Chakra");
    const maxSp = getEffectiveMaxPool(pu0 as never, b.usersEffects as never, "Stamina");
    // Carried pools (isolated pyramid): the previous fight's end fraction of the effective maximum.
    if (start.hpFrac !== undefined) pu0.curHealth = Math.max(1, Math.round(maxHp * start.hpFrac));
    if (start.cpFrac !== undefined) pu0.curChakra = Math.round(maxCp * start.cpFrac);
    if (start.spFrac !== undefined) pu0.curStamina = Math.round(maxSp * start.spFrac);
    const bossU = () => b.usersState.find((u) => u.controllerId === cfg.bossId && !u.isSummon)!;
    const bossUid = bossU().userId;
    const phases = cfg.phases ?? [60, 30];
    const f: Fight = {
      seed, dodge, outcome: "stalled", rounds: 0, playerHpPct: 0, bossHpPct: 0, endHpFrac: 0, endCpFrac: 0, endSpFrac: 0,
      phaseRounds: phases.map(() => null), anchorReached: false,
      sets: Object.fromEntries(cfg.setNames.map((k) => [k, { mark: 0, land: 0, hit: 0, dmg: 0 }])),
      special: Object.fromEntries(Object.keys(cfg.special ?? {}).map((k) => [k, 0])),
      specialFirstRound: Object.fromEntries(Object.keys(cfg.special ?? {}).map((k) => [k, null])),
      summonDamage: 0, bossIdleTurns: 0, bossTurns: 0, playerIdleTurns: 0, playerTurns: 0, dodgeMoves: 0, blockedMoves: 0, cleanses: 0,
      dmgBySource: {}, untelegraphedLands: 0, ...(trace ? { trace: [] } : {}),
    };
    const actionRounds: number[] = [];
    const turnActs = new Map<string, string[]>();
    const lastMark: Record<string, number> = {};
    const marked = (bb: typeof b) =>
      new Set(bb.groundEffects.filter((g: any) => g.type === "visual" && g.creatorId === bossUid && DANGER_ANIMS.has(g.staticAnimation) && (g.rounds ?? 1) > 0).map((g: any) => `${g.longitude},${g.latitude}`));
    const free = (bb: typeof b, c: Cell) =>
      !bb.usersState.some((u) => u.longitude === c[0] && u.latitude === c[1] && stillInBattle(u, bb.usersEffects)) &&
      !bb.groundEffects.some((g: any) => g.type === "barrier" && g.longitude === c[0] && g.latitude === c[1]);
    const outcomeOf = () => {
      const side = (dir: string) => b.usersState.some((u) => u.direction === dir && !u.isSummon && stillInBattle(u, b.usersEffects));
      if (!side("left")) return "lost";
      if (!side("right")) return "won";
      return null;
    };
    const tryAction = (actionId: string, c: Cell) => {
      const pu = b.usersState.find((u) => u.userId === puid)!;
      const action = availableUserActions(b, puid, true, true).find((a) => a.id === actionId);
      if (!action || !actionPointsAfterAction(pu, b, action).canAct) return false;
      try {
        b = performBattleAction({ battle: structuredClone(b), action, grid, contextUserId: puid, actorId: puid, longitude: c[0], latitude: c[1] }).newBattle;
        return true;
      } catch {
        return false;
      }
    };
    const dodgeStep = () => {
      const pu = b.usersState.find((u) => u.userId === puid)!;
      const here: Cell = [pu.longitude, pu.latitude];
      const m = marked(b);
      if (!m.has(key(here))) return false;
      if (!availableUserActions(b, puid, true, true).some((a) => a.id === "move")) {
        if (tryAction("cleanse", here)) { f.cleanses++; return true; }
        return false;
      }
      const prev = new Map<string, string | null>([[key(here), null]]);
      const queue: Cell[] = [here];
      const found: { c: Cell; d: number }[] = [];
      const depth = new Map<string, number>([[key(here), 0]]);
      while (queue.length) {
        const c = queue.shift()!;
        const d = depth.get(key(c))!;
        if (d > 0 && !m.has(key(c))) found.push({ c, d });
        if (d >= 10) continue;
        for (const n of ALL) {
          if (prev.has(key(n)) || dist(c, n) !== 1 || !free(b, n)) continue;
          prev.set(key(n), key(c));
          depth.set(key(n), d + 1);
          queue.push(n);
        }
      }
      if (!found.length) return false;
      const bp: Cell = [bossU().longitude, bossU().latitude];
      found.sort((a, c) => a.d - c.d || dist(a.c, bp) - dist(c.c, bp));
      const target = found[0]!;
      if (target.d >= 2 && dist(here, target.c) <= 5 && tryAction("replacementTechnique", target.c)) return true;
      let step = key(target.c);
      while (prev.get(step) !== key(here)) step = prev.get(step)!;
      return tryAction("move", step.split(",").map(Number) as Cell);
    };
    const maxRounds = cfg.maxRounds ?? 60;
    for (let step = 0; step < maxRounds * 40; step++) {
      const pre = alignBattle(b, actionRounds, puid);
      if (pre.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(pre.actionRound)) actionRounds.push(pre.actionRound);
      if (b.round > maxRounds) break;
      const actor = pre.actor;
      const human = actor.userId === puid;
      const tk = `${b.round}:${actor.userId}`;
      if (!turnActs.has(tk)) turnActs.set(tk, []);
      const hpBefore = new Map(b.usersState.map((u) => [u.userId, u.curHealth]));
      const pBefore = b.usersState.find((u) => u.userId === puid)!;
      const pPos: Cell = [pBefore.longitude, pBefore.latitude];
      const bPos: Cell = [bossU().longitude, bossU().latitude];
      const markedBefore = trace ? marked(b).size : 0;
      if (debugfx) console.log(`FX r${b.round} ${actor.username}: boss ${b.usersEffects.filter((e: any) => e.targetId === bossUid).map((e: any) => `${e.type}:${e.power}:r${e.rounds}`).join(" ")} | player ${b.usersEffects.filter((e: any) => e.targetId === puid).map((e: any) => `${e.type}:${e.power}:r${e.rounds}`).join(" ")}`);
      let actionId: string | undefined;
      if (human && dodge && dodgeStep()) {
        actionId = "dodge";
        f.dodgeMoves++;
      } else {
        const res = performAIaction(b, grid, actor.userId);
        actionId = res.nextActionId;
        if (human && dodge && (actionId === "move" || actionId === "replacementTechnique")) {
          const after = res.nextBattle.usersState.find((u) => u.userId === puid)!;
          if (marked(res.nextBattle).has(`${after.longitude},${after.latitude}`)) {
            f.blockedMoves++;
            actionId = tryAction("wait", pPos) ? "wait" : undefined;
            if (!actionId) b = res.nextBattle;
          } else b = res.nextBattle;
        } else b = res.nextBattle;
      }
      const post = alignBattle(b, actionRounds, puid);
      if (post.progressRound) applySageModeAfterRoundTransition(b);
      if (!actionRounds.includes(post.actionRound)) actionRounds.push(post.actionRound);
      if (!actionId && actor.isAutoCombat) b.roundStartAt = new Date(Date.now() - 61_000);
      turnActs.get(tk)!.push(actionId ?? "none");
      const pAfter = b.usersState.find((u) => u.userId === puid)!;
      const pLoss = Math.max(0, (hpBefore.get(puid) ?? 0) - pAfter.curHealth);
      const isBoss = actor.userId === bossUid;
      const actorName = human ? "player" : isBoss ? "boss" : actor.isSummon ? "summon" : actor.username;
      if (!human && pLoss > 0) {
        const src = actor.isSummon ? "summon" : (cfg.sets[actionId ?? ""]?.[0] ?? (b.extraState.jutsus as any)[actionId ?? ""]?.name ?? (b.extraState.items as any)?.[actionId ?? ""]?.name ?? actionId ?? "tick");
        f.dmgBySource[src] = (f.dmgBySource[src] ?? 0) + pLoss;
        if (actor.isSummon) f.summonDamage += pLoss;
      }
      if (isBoss && actionId && cfg.sets[actionId]) {
        const [sp, kind] = cfg.sets[actionId]!;
        const s = f.sets[sp]!;
        if (kind === "mark") { s.mark++; lastMark[sp] = pre.actionRound; }
        else {
          s.land++;
          if (patternCells(grid, cfg.recs[actionId], bPos).has(key(pPos))) { s.hit++; s.dmg += pLoss; }
          if (pre.actionRound - (lastMark[sp] ?? -9) !== 1) f.untelegraphedLands++;
        }
      }
      if (isBoss && actionId) for (const [label, id] of Object.entries(cfg.special ?? {})) if (id === actionId) {
        f.special[label]!++;
        f.specialFirstRound[label] ??= pre.actionRound;
      }
      const bu = bossU();
      const bhp = (100 * bu.curHealth) / bu.maxHealth;
      phases.forEach((t, i) => { if (bhp < t && f.phaseRounds[i] === null) f.phaseRounds[i] = pre.actionRound; });
      if (cfg.anchor && bu.longitude === cfg.anchor[0] && bu.latitude === cfg.anchor[1]) f.anchorReached = true;
      if (trace) {
        const nm = actionId === "dodge" ? "DODGE" : (b.extraState.jutsus as any)[actionId ?? ""]?.name ?? (b.extraState.items as any)?.[actionId ?? ""]?.name ?? actionId;
        f.trace!.push(`r${pre.actionRound} ${actorName.padEnd(7)} ${String(nm).padEnd(30)} p@${pPos} pHP ${Math.round(pAfter.curHealth)} (-${Math.round(pLoss)}) boss ${bhp.toFixed(1)}% marks ${markedBefore}`);
      }
      const out = outcomeOf();
      if (out) { f.outcome = out; break; }
    }
    for (const [k, acts] of turnActs) {
      const uid = k.split(":")[1];
      if (uid === bossUid) { f.bossTurns++; if (acts.every((a) => a === "wait" || a === "none" || a === "move")) f.bossIdleTurns++; }
      if (uid === puid) { f.playerTurns++; if (acts.every((a) => a === "wait" || a === "none")) f.playerIdleTurns++; }
    }
    const pu = b.usersState.find((u) => u.userId === puid)!;
    const bu = bossU();
    f.rounds = b.round;
    f.endHpFrac = Math.max(0, pu.curHealth) / maxHp;
    f.endCpFrac = Math.max(0, pu.curChakra) / maxCp;
    f.endSpFrac = Math.max(0, pu.curStamina) / maxSp;
    f.playerHpPct = Math.round(1000 * f.endHpFrac) / 10;
    f.bossHpPct = Math.round((1000 * Math.max(0, bu.curHealth)) / bu.maxHealth) / 10;
    return f;
  } finally {
    Math.random = orig;
  }
};

/* ------------------------------------------------------------------ aggregation */
export const median = (xs: number[]) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m]! : (s[m - 1]! + s[m]!) / 2;
};
export const quantile = (xs: number[], p: number) => {
  if (!xs.length) return null;
  const s = [...xs].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.floor(p * (s.length - 1) + 0.5))]!;
};
export const r1 = (x: number | null) => (x === null ? null : Math.round(x * 10) / 10);
export const summarise = (fs: Fight[], setNames: string[]) => {
  const wins = fs.filter((f) => f.outcome === "won");
  const per = (k: string) => {
    const tot = (fld: "mark" | "land" | "hit" | "dmg") => fs.reduce((s, f) => s + f.sets[k]![fld], 0);
    return { marksPerFight: r1(tot("mark") / fs.length), landsPerFight: r1(tot("land") / fs.length), hitsPerFight: r1(tot("hit") / fs.length),
      hitRatePct: tot("land") ? r1((100 * tot("hit")) / tot("land")) : null, dmgPerHit: tot("hit") ? Math.round(tot("dmg") / tot("hit")) : null };
  };
  const src: Record<string, number> = {};
  for (const f of fs) for (const [k, v] of Object.entries(f.dmgBySource)) src[k] = (src[k] ?? 0) + v;
  const totSrc = Object.values(src).reduce((a, b) => a + b, 0) || 1;
  const nPh = fs[0]?.phaseRounds.length ?? 0;
  const lossPhase: Record<string, number> = {};
  for (const f of fs) if (f.outcome !== "won") {
    const ph = f.phaseRounds.filter((x) => x !== null).length + 1;
    lossPhase[`p${ph}`] = (lossPhase[`p${ph}`] ?? 0) + 1;
  }
  const specials = Object.keys(fs[0]?.special ?? {});
  return {
    fights: fs.length, wins: wins.length, winPct: r1((100 * wins.length) / fs.length),
    roundsWinMedian: median(wins.map((f) => f.rounds)), roundsWinP10: quantile(wins.map((f) => f.rounds), 0.1), roundsWinP90: quantile(wins.map((f) => f.rounds), 0.9),
    roundsAllMedian: median(fs.map((f) => f.rounds)),
    hpLeftWinMedian: r1(median(wins.map((f) => f.playerHpPct))), hpLeftWinP10: quantile(wins.map((f) => f.playerHpPct), 0.1),
    hpLeftAllMedian: r1(median(fs.map((f) => f.playerHpPct))),
    bossHpLeftLossMedian: r1(median(fs.filter((f) => f.outcome !== "won").map((f) => f.bossHpPct))),
    lossPhase,
    phaseStartRoundMedian: Array.from({ length: nPh }, (_, i) => median(fs.flatMap((f) => (f.phaseRounds[i] === null ? [] : [f.phaseRounds[i]!])))),
    anchorReachedPct: r1((100 * fs.filter((f) => f.anchorReached).length) / fs.length),
    setPieces: Object.fromEntries(setNames.map((k) => [k, per(k)])),
    special: Object.fromEntries(specials.map((k) => [k, { perFight: r1(fs.reduce((s, f) => s + f.special[k]!, 0) / fs.length), firstRoundMedian: median(fs.flatMap((f) => (f.specialFirstRound[k] === null ? [] : [f.specialFirstRound[k]!]))) }])),
    untelegraphedLands: fs.reduce((s, f) => s + f.untelegraphedLands, 0),
    summonDamageSharePct: r1((100 * fs.reduce((s, f) => s + f.summonDamage, 0)) / totSrc),
    bossIdleTurnPct: r1((100 * fs.reduce((s, f) => s + f.bossIdleTurns, 0)) / Math.max(1, fs.reduce((s, f) => s + f.bossTurns, 0))),
    playerIdleTurnPct: r1((100 * fs.reduce((s, f) => s + f.playerIdleTurns, 0)) / Math.max(1, fs.reduce((s, f) => s + f.playerTurns, 0))),
    dodgeMovesPerFight: r1(fs.reduce((s, f) => s + f.dodgeMoves, 0) / fs.length),
    cleansesPerFight: r1(fs.reduce((s, f) => s + f.cleanses, 0) / fs.length),
    blockedMovesPerFight: r1(fs.reduce((s, f) => s + f.blockedMoves, 0) / fs.length),
    damageShareToPlayerPct: Object.fromEntries(Object.entries(src).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, r1((100 * v) / totSrc)])),
  };
};
