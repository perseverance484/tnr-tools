/**
 * Combat sim input model: live read-only records -> DB-shaped `CombatQueryUser` rows.
 *
 * Records come from `data/live/<date>/` (written by tools/pull_live.py from connector answers) or from any
 * folder with the same layout (a manifest's records can be dropped in as extra folders). Combat itself is
 * entirely the engine's: this file only builds the rows the battle query would have loaded.
 */
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { calcLevel, calcLevelRequirements, scaleUserStats } from "@/libs/profile";
import { scaleEditedAi } from "@/server/api/routers/profile";

export const loadJson = (p: string) => JSON.parse(readFileSync(p, "utf8"));

const DATE_KEY = /(At|Until)$/;
const ISO = /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z$/;
/** DB rows carry Date objects; connector answers serialise them as ISO strings. */
export const revive = (x: any): any => {
  if (Array.isArray(x)) return x.map(revive);
  if (x instanceof Date) return new Date(x.getTime());
  if (x && typeof x === "object") {
    const o: any = {};
    for (const [k, v] of Object.entries(x)) o[k] = typeof v === "string" && DATE_KEY.test(k) && ISO.test(v) ? new Date(v) : revive(v);
    return o;
  }
  return x;
};

export type Library = {
  ai: Record<string, any>;
  profiles: Record<string, any>;
  jutsu: Record<string, any>;
  items: Record<string, any>;
  userItems: Record<string, any>;
  bloodlines: Record<string, any>;
  /** pets.getPet answers: {pet (with species), abilities: {jutsus, skills}}. */
  pets: Record<string, any>;
  battles: Record<string, any[]>;
  runtime: { dmgConfig?: Record<string, number>; sharedCooldowns?: Record<string, number> };
  /** "<kind>/<id>" -> where and when the record was read. */
  sources: Record<string, { endpoint: string; readAt: string | null; dir: string }>;
};

const KINDS: [keyof Library, string][] = [
  ["ai", "ai"], ["profiles", "profiles"], ["jutsu", "jutsu"], ["items", "items"],
  ["userItems", "user_items"], ["bloodlines", "bloodlines"], ["pets", "pets"],
];

/** Merge record folders in order (later folders win). Each file is {_source, data}. */
export const loadLibrary = (dirs: string[]): Library => {
  const lib: Library = { ai: {}, profiles: {}, jutsu: {}, items: {}, userItems: {}, bloodlines: {}, pets: {}, battles: {}, runtime: {}, sources: {} };
  for (const dir of dirs) {
    if (!existsSync(dir)) throw new Error(`record folder ${dir} does not exist`);
    for (const [key, sub] of KINDS) {
      const d = join(dir, sub);
      if (!existsSync(d)) continue;
      for (const f of readdirSync(d).filter((x) => x.endsWith(".json")).sort()) {
        const doc = loadJson(join(d, f));
        const id = f.slice(0, -5);
        (lib[key] as Record<string, any>)[id] = doc.data;
        lib.sources[`${sub}/${id}`] = { endpoint: doc._source?.endpoint, readAt: doc._source?.readAt ?? null, dir };
      }
    }
    const bd = join(dir, "battles");
    if (existsSync(bd))
      for (const f of readdirSync(bd).filter((x) => x.endsWith(".entries.json"))) lib.battles[f.replace(".entries.json", "")] = loadJson(join(bd, f)).data;
    const dmg = join(dir, "runtime/dmg_config.json");
    if (existsSync(dmg)) lib.runtime.dmgConfig = loadJson(dmg).data;
    const cd = join(dir, "runtime/shared_cooldowns.json");
    if (existsSync(cd)) {
      // misc.getSharedCooldowns answers [{tag, rounds}]; the battle stores Record<tag, rounds> (combat.ts initiateBattle)
      const rows = loadJson(cd).data as { tag: string; rounds: number }[];
      lib.runtime.sharedCooldowns = Object.fromEntries(rows.map((r) => [r.tag, r.rounds]));
    }
  }
  return lib;
};

/** Relations the combat query supplies alongside a userData row. */
export const queryShell = (aiProfile: any) => ({
  aiProfile,
  titles: [],
  raidBuffs: [],
  cookingJobs: [],
  village: null,
  bloodline: null,
  sageMode: null,
  anbuSquad: null,
  clan: null,
  loadout: null,
  userSkills: [],
  userQuests: [],
  completedQuests: [],
  bounties: [],
  bountySignups: [],
  queue: [],
});

/* ------------------------------------------------------------------------ */
/* Enemies                                                                  */
/* ------------------------------------------------------------------------ */

/** Design knobs on an enemy, all optional. `aiEdit`/`level` go through the server's own scaleEditedAi. */
export type EnemyOverride = {
  aiEdit?: Record<string, unknown>;
  level?: number;
  rules?: unknown[];
  includeDefaultRules?: boolean;
  /** Replace a jutsu record in this enemy's kit (same id), e.g. a manifest's pending edit. */
  jutsu?: Record<string, any>;
};

/** An AI row as the battle query loads it: equipped jutsu, equipped in-stock items, its AI profile. */
export const enemyRow = (lib: Library, aiId: string, ov: EnemyOverride = {}) => {
  const stored = lib.ai[aiId];
  if (!stored) throw new Error(`AI ${aiId} has no live record (profile.getAi) in the library`);
  let row = revive(structuredClone(stored));
  if (ov.level !== undefined || ov.aiEdit) {
    const edited = { ...structuredClone(row), ...(ov.aiEdit ?? {}), ...(ov.level !== undefined ? { level: ov.level } : {}) };
    scaleEditedAi(row, edited);
    row = edited;
  }
  const profile = structuredClone(lib.profiles[row.aiProfileId]);
  if (!profile) throw new Error(`AI ${row.username} (${aiId}): profile ${row.aiProfileId} not in the library (ai.getAiProfile)`);
  if (ov.rules) profile.rules = structuredClone(ov.rules);
  if (ov.includeDefaultRules !== undefined) profile.includeDefaultRules = ov.includeDefaultRules;
  row.jutsus = row.jutsus
    .filter((uj: any) => uj.equipped)
    .map((uj: any) => ({ activeReskin: null, ...uj, jutsu: ov.jutsu?.[uj.jutsuId] ? revive(structuredClone(ov.jutsu[uj.jutsuId])) : uj.jutsu }));
  row.items = (row.items ?? [])
    .filter((ui: any) => ui.equipped !== "NONE" && ui.quantity > 0 && !ui.isInAuction)
    .map((ui: any) => ({ imbuements: [], ...ui }));
  return { ...row, ...queryShell(profile) };
};

/** Every AI id a set of rows can summon (summon effects), so assembly can pre-seed the summon cache. */
export const summonIds = (rows: any[]) => {
  const ids = new Set<string>();
  for (const u of rows) for (const uj of u.jutsus ?? []) for (const e of uj.jutsu?.effects ?? []) if (e.type === "summon" && e.aiId) ids.add(e.aiId);
  return [...ids];
};

/* ------------------------------------------------------------------------ */
/* Players                                                                  */
/* ------------------------------------------------------------------------ */

export type PlayerSpec = {
  name: string;
  level: number;
  rank: "STUDENT" | "GENIN" | "CHUNIN" | "JONIN" | "ELITE JONIN";
  /** Explicit combat stats. Without them: the level's stat budget (scaleUserStats "player") times statBudget, spread evenly. */
  stats?: { offence: number; defence: number; strength: number; intelligence: number; willpower: number; speed: number };
  statBudget?: number;
  /** Explicit pool maxima. Without them: calcHP/CP/SP(level). */
  pools?: { health: number; chakra: number; stamina: number };
  masteries?: Partial<Record<"ninjutsuMastery" | "genjutsuMastery" | "taijutsuMastery" | "bukijutsuMastery" | "bloodlineMastery" | "sageMastery", number>>;
  elements?: string[];
  preferredGenerals?: [string, string];
  bloodlineId?: string;
  jutsu: { id: string; level: number }[];
  /** Worn gear and carried items: a live user item (its level) or an item record, in a slot. */
  items?: { userItemId?: string; itemId?: string; slot: string; level?: number; quantity?: number }[];
  /** Auto-combat rules; without them the default rotation (rotationRules) is used. */
  rules?: unknown[];
  /** Companion pets (live pets.getPet records). One = the active pet; two = a solo dungeon's chosen pair. */
  pets?: string[];
};

const COMBAT_STATS = ["offence", "defence", "strength", "intelligence", "willpower", "speed"] as const;

const userJutsu = (userId: string, rec: any, level: number, idx: number) => ({
  id: `uj-${userId.slice(0, 12)}-${idx}`, userId, jutsuId: rec.id, level, experience: 0, equipped: true,
  trainingStartedAt: null, finishTraining: null, reskinId: null, createdAt: new Date(0), updatedAt: new Date(0),
  jutsu: rec, activeReskin: null,
});

/**
 * Default player rotation (a stand-in for a person; declared test input, executed by the engine's AI selector):
 * self buffs whenever ready; each attack jutsu whenever ready and the closest enemy is in its range (gate = range + 1,
 * because rule distance counts both end hexes, ENGINE_LAWS law 40); close in; basic attack; end turn.
 */
export const rotationRules = (kit: any[]) => {
  const rules: any[] = [];
  const heal = (j: any) => j.effects.some((e: any) => e.type === "heal");
  for (const j of kit.filter((j) => j.target === "SELF"))
    rules.push({
      conditions: heal(j) ? [{ type: "health_below", value: 50, description: "" }] : [],
      action: { type: "use_specific_jutsu", jutsuId: j.id, target: "SELF", description: `self: ${j.name}` },
    });
  for (const j of kit.filter((j) => j.target !== "SELF"))
    rules.push({
      conditions: [{ type: "distance_lower_than", value: (j.range ?? 1) + 1, target: "CLOSEST_OPPONENT", description: "" }],
      action: { type: "use_specific_jutsu", jutsuId: j.id, target: "CLOSEST_OPPONENT", description: `attack: ${j.name}` },
    });
  rules.push({
    conditions: [{ type: "distance_higher_than", value: 1, target: "CLOSEST_OPPONENT", description: "" }],
    action: { type: "move_towards_opponent", target: "CLOSEST_OPPONENT", description: "close in" },
  });
  rules.push({ conditions: [], action: { type: "use_specific_jutsu", jutsuId: "basicAttack", target: "CLOSEST_OPPONENT", description: "basic attack" } });
  rules.push({ conditions: [], action: { type: "end_turn", description: "end turn" } });
  return rules;
};

/** A player row built on a donor userData row (any live AI row: same table, same columns). */
export const playerRow = (lib: Library, spec: PlayerSpec, idx: number, donor: any, userIdOverride?: string) => {
  const userId = userIdOverride ?? `user_sim_p${idx + 1}`; // ai_v2 treats ids containing "user_" as players
  const s: any = {
    level: spec.level, experience: 0, statsMultiplier: 1, poolsMultiplier: 1,
    curHealth: 0, maxHealth: 0, curStamina: 0, maxStamina: 0, curChakra: 0, maxChakra: 0,
    offence: 10, defence: 10, strength: 10, intelligence: 10, willpower: 10, speed: 10,
    ninjutsuMastery: 10, genjutsuMastery: 10, taijutsuMastery: 10, bukijutsuMastery: 10, bloodlineMastery: 10, sageMastery: 10,
  };
  scaleUserStats(s, "player");
  const frac = spec.statBudget ?? 1;
  for (const k of COMBAT_STATS) s[k] = 10 + (s[k] - 10) * frac;
  if (spec.stats) for (const k of COMBAT_STATS) s[k] = spec.stats[k];
  const pools = spec.pools ?? { health: s.maxHealth, chakra: s.maxChakra, stamina: s.maxStamina };
  // experience consistent with the level (the engine reads calcLevel(experience) in places)
  let exp = calcLevelRequirements(spec.level - 1);
  while (calcLevel(exp) < spec.level) exp += 100;
  const kit = spec.jutsu.map((j) => {
    const rec = lib.jutsu[j.id];
    if (!rec) throw new Error(`player ${spec.name}: jutsu ${j.id} not in the library (jutsu.get)`);
    return revive(structuredClone(rec));
  });
  const rules = spec.rules ?? rotationRules(kit);
  const profile = { id: `profile-${userId}`, userId, name: spec.name, includeDefaultRules: false, rules };
  const items = (spec.items ?? []).map((it, i) => {
    const owned = it.userItemId ? lib.userItems[it.userItemId] : undefined;
    if (it.userItemId && !owned) throw new Error(`player ${spec.name}: user item ${it.userItemId} not in the library (item.getUserItem)`);
    const rec = owned?.item ?? (it.itemId ? lib.items[it.itemId] : undefined);
    if (!rec) throw new Error(`player ${spec.name}: item ${it.itemId ?? it.userItemId} not in the library`);
    return revive({
      id: `ui-${userId}-${i}`, userId, itemId: rec.id, quantity: it.quantity ?? owned?.quantity ?? 1,
      level: it.level ?? owned?.level ?? 1, experience: 0, equipped: it.slot, durability: owned?.durability ?? rec.maxDurability ?? 100,
      storedAtHome: false, isInAuction: false, activeVariantId: null, dropChancePerc: 0, craftingFinishedAt: null,
      createdAt: new Date(0).toISOString(), updatedAt: new Date(0).toISOString(), imbuements: [], item: structuredClone(rec),
    });
  });
  const simPets = (spec.pets ?? []).map((id) => {
    const doc = lib.pets[id];
    if (!doc?.pet) throw new Error(`player ${spec.name}: pet ${id} not in the library (pets.getPet)`);
    return { pet: { ...revive(structuredClone(doc.pet)), userId }, jutsus: revive(structuredClone(doc.abilities?.jutsus ?? [])), skills: [] };
  });
  const bloodline = spec.bloodlineId ? lib.bloodlines[spec.bloodlineId] : null;
  if (spec.bloodlineId && !bloodline) throw new Error(`player ${spec.name}: bloodline ${spec.bloodlineId} not in the library`);
  const m = spec.masteries ?? {};
  return {
    ...revive(structuredClone(donor)),
    userId, username: spec.name, isAi: false, isSummon: false, isEvent: false, aiProfileId: profile.id,
    villageId: "village-sim-party", sector: 1, rank: spec.rank, level: spec.level, experience: exp,
    statsMultiplier: 1, poolsMultiplier: 1,
    curHealth: pools.health, maxHealth: pools.health, curChakra: pools.chakra, maxChakra: pools.chakra,
    curStamina: pools.stamina, maxStamina: pools.stamina,
    offence: s.offence, defence: s.defence, strength: s.strength, intelligence: s.intelligence, willpower: s.willpower, speed: s.speed,
    ninjutsuMastery: m.ninjutsuMastery ?? 10, genjutsuMastery: m.genjutsuMastery ?? 10, taijutsuMastery: m.taijutsuMastery ?? 10,
    bukijutsuMastery: m.bukijutsuMastery ?? 10, bloodlineMastery: m.bloodlineMastery ?? 10, sageMastery: m.sageMastery ?? 10,
    preferredGeneral1: spec.preferredGenerals?.[0] ?? null, preferredGeneral2: spec.preferredGenerals?.[1] ?? null,
    primaryElement: spec.elements?.[0] ?? null, secondaryElement: spec.elements?.[1] ?? null,
    preferredDamageElement: null, elementalMastery: {}, activeTrainedElement: null,
    bloodlineId: bloodline?.id ?? null, bloodlineReskinId: null, sageModeId: null, activePetId: simPets[0]?.pet.id ?? null, petTask: null,
    effects: [], items, pvpStreak: 0, isBanned: false, status: "AWAKE", defaultAutoCombat: false,
    jutsus: kit.map((rec, i) => userJutsu(userId, rec, spec.jutsu[i]!.level, i)),
    ...queryShell(profile),
    bloodline: bloodline ? revive(structuredClone(bloodline)) : null,
    _simPets: simPets,
  };
};

export const describeRow = (u: any) => ({
  name: u.username, level: u.level, rank: u.rank, hp: u.maxHealth, cp: u.maxChakra, sp: u.maxStamina,
  offence: u.offence, defence: u.defence, generals: [u.strength, u.intelligence, u.willpower, u.speed],
  jutsu: u.jutsus.map((j: any) => `${j.jutsu.name}@${j.level}`),
  items: (u.items ?? []).map((i: any) => `${i.equipped}:${i.item.name}@${i.level}`),
  bloodline: u.bloodline?.name ?? null, elements: [u.primaryElement, u.secondaryElement].filter(Boolean),
});
