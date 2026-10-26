/**
 * Skyglass Wreck harness: input model (enemies, players, dungeon layout, overrides).
 *
 * Everything here builds DB-shaped `CombatQueryUser` rows. Combat itself is the engine's.
 * Baseline enemy rows come from data/baseline.json (committed captures + pushes 250-252);
 * push/252 pool edits are replayed through the server's own `scaleEditedAi`.
 */
import { readFileSync } from "node:fs";
import { getUserCaps, TOTAL_MASTERY_CAP } from "@/drizzle/constants";
import { calcLevel, calcLevelRequirements, scaleUserStats } from "@/libs/profile";
import { scaleEditedAi } from "@/server/api/routers/profile";

export type WaveDef = { aiIds: string[]; delayRounds: number };
export type FloorDef = { kind: "floor" | "mini-boss" | "boss"; waves: WaveDef[] };

/** Per-enemy override (all optional). Keys of `enemies` are AI ids or usernames. */
export type EnemyOverride = {
  username?: string;
  /** Replayed through scaleEditedAi exactly like a Forge AI edit. */
  aiEdit?: Record<string, unknown>;
  /** Post-assembly multiplier on max/current HP only (design knob; not an engine field). */
  hpScale?: number;
  /** Multiplier on offence/defence/generals before the battle cap (design knob). */
  statScale?: number;
  /** Replace the equipped kit with these jutsu ids (records from catalog or `jutsu`). */
  jutsuIds?: string[];
  /** Jutsu level for every equipped jutsu (captured AIs are level 1). */
  jutsuLevel?: number;
  /** Replace innate effects (the AI row `effects` column). */
  effects?: unknown[];
  rules?: unknown[];
  includeDefaultRules?: boolean;
  /** For new enemies: clone this AI id (then apply the fields above). */
  base?: string;
  /** Enemy level: replayed through scaleEditedAi as a Forge level edit (proportional
   * rescale of stats and pools to the new level; applied before aiEdit). */
  level?: number;
};

export type PlayerVariant = {
  name: string;
  note: string;
  /** Player level (default 100). Pools are calcHP/CP/SP(level); the stat budget is the level's. */
  level?: number;
  /** Player rank (default JONIN at level 100, CHUNIN below). Sets caps and the default kit. */
  rank?: "GENIN" | "CHUNIN" | "JONIN";
  /** Fraction of the player's level stat budget (scaleUserStats "player"), even spread. */
  statBudget: number;
  /** Explicit stats instead of the budget (then capped by capUserStats like every participant). */
  stats?: { offence: number; defence: number; generals: number };
  /** Pools multiplier on calcHP/CP/SP(level). */
  poolsMultiplier: number;
  /** Innate increasedamagegiven % (gear stand-in); 0 = none. */
  damageGivenPct: number;
  /** Innate decreasedamagetaken % (gear stand-in); 0 = none. */
  damageTakenReductionPct: number;
  jutsuIds: string[];
  jutsuLevel: number;
  /** Auto-combat profile rules (player side); undefined = default kit profile. */
  rules?: unknown[];
};

export type Override = {
  name?: string;
  note?: string;
  floors?: FloorDef[];
  enemies?: Record<string, EnemyOverride>;
  newEnemies?: Record<string, EnemyOverride>;
  jutsu?: Record<string, any>;
  players?: Record<string, Partial<PlayerVariant>>;
};

export const loadJson = (p: string) => JSON.parse(readFileSync(p, "utf8"));

const DATE_KEY = /(At|Until)$/;
const ISO = /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z$/;
/** DB rows carry Date objects; captures serialise them to ISO strings. */
export const revive = (x: any): any => {
  if (Array.isArray(x)) return x.map(revive);
  if (x && typeof x === "object") {
    const o: any = {};
    for (const [k, v] of Object.entries(x))
      o[k] = typeof v === "string" && DATE_KEY.test(k) && ISO.test(v) ? new Date(v) : revive(v);
    return o;
  }
  return x;
};

/** Relations the combat query supplies alongside a userData row (none apply to these units). */
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

const userJutsu = (userId: string, rec: any, level: number, idx: number) => ({
  id: `uj-${userId.slice(0, 8)}-${idx}`,
  userId,
  jutsuId: rec.id,
  level,
  experience: 0,
  equipped: true,
  finishTraining: null,
  reskinId: null,
  createdAt: new Date(0),
  updatedAt: new Date(0),
  jutsu: rec,
  activeReskin: null,
});

const COMBAT_STATS = ["offence", "defence", "strength", "intelligence", "willpower", "speed"] as const;

export type Templates = {
  enemies: Record<string, { row: any; profile: any; notes: string[] }>;
  floors: FloorDef[];
  jutsu: Record<string, any>;
  playerJutsu: Record<string, { label: string; record: any; source: string }>;
};

/** Resolve enemy templates (captured baseline + push/252 replay + overrides). */
export const buildTemplates = (baseline: any, ov: Override): Templates => {
  const jutsu: Record<string, any> = {};
  for (const [id, j] of Object.entries<any>(baseline.jutsuCatalog)) jutsu[id] = j.record;
  for (const [id, j] of Object.entries<any>(baseline.playerJutsu)) jutsu[id] = j.record;
  for (const [id, rec] of Object.entries<any>(ov.jutsu ?? {})) jutsu[id] = { ...rec, id };

  const enemies: Templates["enemies"] = {};
  for (const [aid, e] of Object.entries<any>(baseline.enemies)) {
    const stored = revive(structuredClone(e.user));
    let row = stored;
    const notes: string[] = [];
    if (e.pendingAiEdit) {
      row = { ...structuredClone(stored), ...e.pendingAiEdit.data };
      scaleEditedAi(stored, row);
      notes.push(`scaleEditedAi(${JSON.stringify(e.pendingAiEdit.data)}) -> maxHealth ${row.maxHealth}`);
    }
    enemies[aid] = { row, profile: structuredClone(e.profile), notes };
  }
  const byName = (k: string) =>
    enemies[k] ? k : Object.keys(enemies).find((id) => enemies[id]!.row.username === k);
  const apply = (id: string, o: EnemyOverride) => {
    const t = enemies[id]!;
    if (o.username) t.row.username = o.username;
    if (o.level !== undefined) {
      const stored = t.row;
      const edited = { ...structuredClone(stored), level: o.level };
      scaleEditedAi(stored, edited);
      t.row = edited;
      t.notes.push(`override level ${stored.level} -> ${o.level} via scaleEditedAi (HP ${stored.maxHealth} -> ${edited.maxHealth}, offence ${stored.offence} -> ${edited.offence})`);
    }
    if (o.aiEdit) {
      const stored = t.row;
      const edited = { ...structuredClone(stored), ...o.aiEdit };
      scaleEditedAi(stored, edited);
      t.row = edited;
      t.notes.push(`override aiEdit ${JSON.stringify(o.aiEdit)} via scaleEditedAi`);
    }
    if (o.statScale !== undefined) {
      for (const s of COMBAT_STATS) t.row[s] *= o.statScale;
      t.notes.push(`statScale ${o.statScale}`);
    }
    if (o.jutsuIds) {
      t.row.jutsus = o.jutsuIds.map((jid, i) => {
        if (!jutsu[jid]) throw new Error(`override: unknown jutsu ${jid}`);
        return userJutsu(t.row.userId, structuredClone(jutsu[jid]), 1, i);
      });
      t.notes.push(`kit -> ${o.jutsuIds.length} jutsu`);
    }
    if (o.jutsuLevel !== undefined) for (const uj of t.row.jutsus) uj.level = o.jutsuLevel;
    if (o.effects) t.row.effects = structuredClone(o.effects);
    if (o.rules) t.profile = { ...t.profile, rules: structuredClone(o.rules) };
    if (o.includeDefaultRules !== undefined) t.profile.includeDefaultRules = o.includeDefaultRules;
    if (o.hpScale !== undefined) (t as any).hpScale = o.hpScale;
  };
  for (const [nid, o] of Object.entries(ov.newEnemies ?? {})) {
    const baseId = o.base && byName(o.base);
    if (!baseId) throw new Error(`newEnemies.${nid}: base ${o.base} unknown`);
    const src = enemies[baseId]!;
    const row = structuredClone(src.row);
    row.userId = nid;
    row.username = o.username ?? nid;
    const profile = { ...structuredClone(src.profile), id: `profile-${nid}`, userId: nid };
    row.aiProfileId = profile.id;
    enemies[nid] = { row, profile, notes: [`new enemy cloned from ${src.row.username}`] };
    apply(nid, o);
  }
  for (const [k, o] of Object.entries(ov.enemies ?? {})) {
    const id = byName(k);
    if (!id) throw new Error(`override enemies.${k}: unknown AI`);
    apply(id, o);
  }
  const floors = structuredClone(ov.floors ?? baseline.dungeon.floors) as FloorDef[];
  for (const f of floors)
    for (const w of f.waves)
      w.aiIds = w.aiIds.map((k) => {
        const id = byName(k);
        if (!id) throw new Error(`floor wave references unknown AI ${k}`);
        return id;
      });
  return { enemies, floors, jutsu, playerJutsu: baseline.playerJutsu };
};

/** The battle query only loads equipped jutsu and equipped, in-stock items. */
export const enemyQueryUser = (t: Templates["enemies"][string]) => {
  const row = structuredClone(t.row);
  const hpScale = (t as any).hpScale as number | undefined;
  if (hpScale !== undefined) {
    // Design knob: battles hold pools in memory, so values above the stored column cap are possible.
    row.maxHealth = Math.round(row.maxHealth * hpScale);
    row.curHealth = row.maxHealth;
  }
  row.jutsus =row.jutsus.filter((uj: any) => uj.equipped).map((uj: any) => ({ activeReskin: null, ...uj }));
  row.items = (row.items ?? [])
    .filter((ui: any) => ui.equipped !== "NONE" && ui.quantity > 0 && !ui.isInAuction)
    .map((ui: any) => ({ imbuements: [], ...ui }));
  return { ...row, ...queryShell(t.profile) };
};

/* ------------------------------------------------------------------------ */
/* Players                                                                  */
/* ------------------------------------------------------------------------ */

export const DEFAULT_PLAYER_KIT = [
  "e2eC-x4UXc5m6QexNbx8w", // Chakra Overflow: self IDG 25+25
  "cUPCLvCCEO9MCSRtFsulW", // Aqua Barrier: self DDT 30 + IDG 30
  "fAKcf34Vlt_-utDdDdjxH", // Rejuvenating Chakra: self heal 40 (used below 50% HP)
  "4eDM_5VVZkasBjaW2fEmI", // Void Pulse Barrage: AOE pierce 46 + IDT 20
  "GiKpip6NxsC8QWlZi6l_R", // Shrapnel Clone Barrage: AOE damage 45 + wound
  "VT7oxj_fObWuQa3Rq_BbI", // Stunning Jab: damage 35 + stun
  "zCmYLVL4JYzfhjPXHi9rH", // Eight Fist Style: Lotus Dance: damage 35 + buffprevent
  "kbrQuf3nYNHoKEvusATTO", // Phantom Requiem: damage 30 + drain
];

/** Chunin-rank kit for the level 40-60 version (all CHUNIN rank, requiredLevel 1, PvE-usable). */
export const CHUNIN_PLAYER_KIT = [
  "C1SdH7N13naMHG3bKE07k", // Harden Fist: self IDG 20 + DDT 20
  "cUPCLvCCEO9MCSRtFsulW", // Aqua Barrier: self DDT 30 + IDG 30
  "fAKcf34Vlt_-utDdDdjxH", // Rejuvenating Chakra: self heal (below 50% HP)
  "VT7oxj_fObWuQa3Rq_BbI", // Stunning Jab: damage 35 + stun
  "uhEr3x6ucxHJbcjnTs7ps", // Shattering Strike: damage 30
  "5JCcW9EdcDy7a5-0SiH_W", // Chakra Palm: damage 28 + shield
  "kvuECU_A6qeZYsWwU_Zvq", // Resounding Crescendo: damage 28
  "Oi5pYxNaHa-5o737i5gAu", // Iron Fist: damage 20 + lifesteal
];
const RANK_ORDER = ["STUDENT", "GENIN", "CHUNIN", "JONIN"];
/** Kit appropriate to a level/rank: the rank's kit, minus anything its requirements block. */
export const kitFor = (level: number, rank: string, jutsu: Record<string, any>, ids?: string[]) =>
  (ids ?? (rank === "JONIN" ? DEFAULT_PLAYER_KIT : CHUNIN_PLAYER_KIT)).filter((id) => {
    const j = jutsu[id];
    return j && (j.requiredLevel ?? 1) <= level && RANK_ORDER.indexOf(j.requiredRank) <= RANK_ORDER.indexOf(rank);
  });

const CAPS = { offence: 1_300_000, defence: 1_300_000, generals: 400_000 }; // getUserCaps("JONIN")

/**
 * Player power ladder (all level-100 JONIN, same 8-jutsu kit at level 25 unless noted).
 * Gear, bloodline and items are not modelled record-by-record; tiers 2-4 stand them in as
 * innate battle tags (increasedamagegiven / decreasedamagetaken, as AI innate effects are)
 * plus a pools multiplier. Which tier is "average" is the director's call.
 */
export const PLAYER_VARIANTS: Record<string, PlayerVariant> = {
  baseline: {
    name: "baseline",
    note: "brief's suggested baseline: level-100 stat budget (scaleUserStats 'player') spread evenly (offence/defence 556,510; generals capped 400,000), calcHP/CP/SP(100) = 5,050 pools, no gear",
    statBudget: 1, poolsMultiplier: 1, damageGivenPct: 0, damageTakenReductionPct: 0,
    jutsuIds: DEFAULT_PLAYER_KIT, jutsuLevel: 25,
  },
  cap: {
    name: "cap",
    note: "fully trained Jonin: stats at the JONIN caps (1.3M/1.3M/400k), 5,050 pools, no gear",
    statBudget: 1, stats: CAPS, poolsMultiplier: 1, damageGivenPct: 0, damageTakenReductionPct: 0,
    jutsuIds: DEFAULT_PLAYER_KIT, jutsuLevel: 25,
  },
  geared: {
    name: "geared",
    note: "JONIN caps + gear stand-in: pools x2.5 (12,625 HP, parity with the crew AIs), damage taken -40%, damage given +100%",
    statBudget: 1, stats: CAPS, poolsMultiplier: 2.5, damageGivenPct: 100, damageTakenReductionPct: 40,
    jutsuIds: DEFAULT_PLAYER_KIT, jutsuLevel: 25,
  },
  strong: {
    name: "strong",
    note: "JONIN caps + heavy gear stand-in: pools x4 (20,200 HP), damage taken -60%, damage given +250%",
    statBudget: 1, stats: CAPS, poolsMultiplier: 4, damageGivenPct: 250, damageTakenReductionPct: 60,
    jutsuIds: DEFAULT_PLAYER_KIT, jutsuLevel: 25,
  },
  lvl50: {
    name: "lvl50", level: 50, rank: "CHUNIN",
    note: "easier-version average: level-50 CHUNIN, level-50 stat budget (scaleUserStats 'player') spread evenly, calcHP/CP/SP(50) = 2,550 pools, Chunin kit at jutsu level 15, no gear",
    statBudget: 1, poolsMultiplier: 1, damageGivenPct: 0, damageTakenReductionPct: 0,
    jutsuIds: CHUNIN_PLAYER_KIT, jutsuLevel: 15,
  },
  lvl40: {
    name: "lvl40", level: 40, rank: "CHUNIN",
    note: "easier-version lower bound: level 40, otherwise as lvl50 (jutsu level 12)",
    statBudget: 1, poolsMultiplier: 1, damageGivenPct: 0, damageTakenReductionPct: 0,
    jutsuIds: CHUNIN_PLAYER_KIT, jutsuLevel: 12,
  },
  lvl60: {
    name: "lvl60", level: 60, rank: "CHUNIN",
    note: "easier-version upper bound: level 60, otherwise as lvl50 (jutsu level 18)",
    statBudget: 1, poolsMultiplier: 1, damageGivenPct: 0, damageTakenReductionPct: 0,
    jutsuIds: CHUNIN_PLAYER_KIT, jutsuLevel: 18,
  },
  elite: {
    name: "elite",
    note: "JONIN caps + extreme gear stand-in: pools x6 (30,300 HP), damage taken -75%, damage given +400% (matches the crew's own innate +350-450%)",
    statBudget: 1, stats: CAPS, poolsMultiplier: 6, damageGivenPct: 400, damageTakenReductionPct: 75,
    jutsuIds: DEFAULT_PLAYER_KIT, jutsuLevel: 25,
  },
};

const tag = (type: string, power: number) => ({
  type, power, powerPerLevel: 0, rounds: 999, target: "INHERIT", calculation: "percentage",
  direction: type === "increasedamagegiven" ? "offence" : "defence",
  description: `harness gear stand-in ${type} ${power}%`, appearSfx: "", disappearSfx: "",
  appearAnimation: "", staticAnimation: "", staticAssetPath: "", disappearAnimation: "",
});

/**
 * Default player auto-combat profile (declared test input, executed by the engine's AI selector):
 * self-buff when ready; otherwise cast each attack jutsu whenever it is off cooldown and the
 * closest enemy is within its range; close the distance; basic attack as the fallback.
 * (The engine's use_highest_power_action ranks the basic attack above these jutsu, so a
 * "highest power only" profile would never cast them; this rotation is how a person plays.)
 */
export const playerRules = (kit: string[], jutsu: Record<string, any>) => {
  const rules: any[] = [];
  const isHeal = (j: any) => j.effects.some((e: any) => e.type === "heal");
  for (const id of kit) {
    const j = jutsu[id];
    if (j.target !== "SELF") continue;
    rules.push({
      conditions: isHeal(j) ? [{ type: "health_below", value: 50, description: "" }] : [],
      action: { type: "use_specific_jutsu", jutsuId: id, target: "SELF", description: "" },
    });
  }
  for (const id of kit) {
    const j = jutsu[id];
    if (j.target === "SELF") continue;
    rules.push({
      conditions: [{ type: "distance_lower_than", value: j.range, target: "CLOSEST_OPPONENT", description: "" }],
      action: { type: "use_specific_jutsu", jutsuId: id, target: "CLOSEST_OPPONENT", description: "" },
    });
  }
  rules.push({
    conditions: [{ type: "distance_higher_than", value: 2, target: "CLOSEST_OPPONENT", description: "" }],
    action: { type: "move_towards_opponent", target: "CLOSEST_OPPONENT", description: "" },
  });
  rules.push({ conditions: [], action: { type: "use_highest_power_action", effect: "damage", target: "CLOSEST_OPPONENT", description: "" } });
  return rules;
};

export const playerQueryUser = (idx: number, v: PlayerVariant, donor: any, jutsu: Record<string, any>) => {
  const userId = `user_wreck_p${idx + 1}`; // ai_v2 treats ids containing "user_" as players
  const level = v.level ?? 100;
  const rank = v.rank ?? (level >= 100 ? "JONIN" : "CHUNIN");
  const kit = kitFor(level, rank, jutsu, v.jutsuIds);
  // Level budget with an even spread: scaleUserStats(..., "player") from base stats.
  const s: any = {
    level, experience: 0, statsMultiplier: 1, poolsMultiplier: v.poolsMultiplier,
    curHealth: 0, maxHealth: 0, curStamina: 0, maxStamina: 0, curChakra: 0, maxChakra: 0,
    offence: 10, defence: 10, strength: 10, intelligence: 10, willpower: 10, speed: 10,
    ninjutsuMastery: 10, genjutsuMastery: 10, taijutsuMastery: 10, bukijutsuMastery: 10,
    bloodlineMastery: 10, sageMastery: 10,
  };
  scaleUserStats(s, "player");
  for (const k of COMBAT_STATS) s[k] = 10 + (s[k] - 10) * v.statBudget;
  if (v.stats) {
    s.offence = v.stats.offence;
    s.defence = v.stats.defence;
    for (const k of ["strength", "intelligence", "willpower", "speed"]) s[k] = v.stats.generals;
  }
  // Experience consistent with level 100 (getEffectiveLevel = calcLevel(experience)).
  let exp = calcLevelRequirements(level - 1);
  while (calcLevel(exp) < level) exp += 1000;
  if (calcLevel(exp) !== level) throw new Error(`player experience ${exp} -> level ${calcLevel(exp)}`);
  const m = TOTAL_MASTERY_CAP / 4; // masteries only gate jutsu use; even split of the shared cap
  const rules = v.rules ?? playerRules(kit, jutsu);
  const profile = { id: `profile-${userId}-${v.name}`, userId, name: v.name, includeDefaultRules: false, rules };
  const effects = [
    ...(v.damageGivenPct ? [tag("increasedamagegiven", v.damageGivenPct)] : []),
    ...(v.damageTakenReductionPct ? [tag("decreasedamagetaken", v.damageTakenReductionPct)] : []),
  ];
  const u: any = {
    ...structuredClone(donor),
    userId, username: `Player ${idx + 1}`, isAi: false, isSummon: false, isEvent: false,
    villageId: "village-wreck-party", sector: 210, aiProfileId: profile.id, rank,
    level, experience: exp, statsMultiplier: 1, poolsMultiplier: v.poolsMultiplier,
    curHealth: s.maxHealth, maxHealth: s.maxHealth, curChakra: s.maxChakra, maxChakra: s.maxChakra,
    curStamina: s.maxStamina, maxStamina: s.maxStamina,
    offence: s.offence, defence: s.defence, strength: s.strength, intelligence: s.intelligence,
    willpower: s.willpower, speed: s.speed,
    ninjutsuMastery: m, genjutsuMastery: m, taijutsuMastery: m, bukijutsuMastery: m,
    bloodlineMastery: 10, sageMastery: 10,
    primaryElement: null, secondaryElement: null, bloodlineId: null, sageModeId: null,
    effects, items: [], pvpStreak: 0, isBanned: false, status: "AWAKE", defaultAutoCombat: false,
    jutsus: kit.map((jid, i) => {
      if (!jutsu[jid]) throw new Error(`player jutsu ${jid} not in catalog`);
      return userJutsu(userId, structuredClone(jutsu[jid]), v.jutsuLevel, i);
    }),
    ...queryShell(profile),
  };
  return u;
};

export const describePlayer = (u: any) => ({
  userId: u.userId, level: u.level, rank: u.rank, offence: u.offence, defence: u.defence, generals: u.strength,
  hp: u.maxHealth, cp: u.maxChakra, sp: u.maxStamina, jutsu: u.jutsus.map((j: any) => `${j.jutsu.name}@${j.level}`),
  innateEffects: u.effects.map((e: any) => `${e.type} ${e.power}%`),
  rankCaps: getUserCaps(u.rank),
});
