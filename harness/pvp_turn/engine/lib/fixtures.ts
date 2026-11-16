/**
 * Ghost Ship / Skyglass Stage 2 harness — committed-record fixture loader.
 *
 * Every combat record used by the harness is read from committed TNR captures by
 * JSON pointer (paths/pointers come from the accepted kit packet, the legacy
 * conversion packet and the Sealwright rule contract). Nothing here fetches from
 * the network or the game. Records are deep-cloned and never normalised.
 *
 * Synthetic values are confined to the `carrier`/`policy` helpers at the bottom,
 * each labelled with its provenance so reports can disclose them.
 */
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";

export const REPO = process.env.TNR_REPO ?? "";
if (!REPO) throw new Error("TNR_REPO must point at the tnr-tools checkout");

const cache = new Map<string, any>();
export const loadJson = (rel: string): any => {
  if (!cache.has(rel)) {
    const raw = readFileSync(join(REPO, rel));
    cache.set(rel, { doc: JSON.parse(raw.toString("utf8")), sha256: sha256(raw) });
  }
  return cache.get(rel).doc;
};
export const fileSha256 = (rel: string): string => {
  loadJson(rel);
  return cache.get(rel).sha256;
};
const sha256 = (b: Buffer | string) => createHash("sha256").update(b).digest("hex");

export const ptr = (doc: any, pointer: string): any => {
  let cur = doc;
  for (const raw of pointer.replace(/^\//, "").split("/")) {
    const t = raw.replace(/~1/g, "/").replace(/~0/g, "~");
    cur = Array.isArray(cur) ? cur[Number(t)] : cur[t];
    if (cur === undefined) throw new Error(`Pointer ${pointer} unresolved at ${t}`);
  }
  return cur;
};
export const clone = <T>(x: T): T => structuredClone(x);

export const KIT_PATH = "state/ghost_ship_hybrid_kit_proposal.json";
export const LEGACY_PATH = "state/ghost_ship_legacy_jutsu_conversion.json";
export const CONTRACT_PATH = "state/ghost_ship_skyglass_sealwright_rule_contract.json";

export const kit = () => loadJson(KIT_PATH);
export const legacy = () => loadJson(LEGACY_PATH);
export const contract = () => loadJson(CONTRACT_PATH);
const aiDoc = () => loadJson(kit().sourceFiles.ai);
const profDoc = () => loadJson(kit().sourceFiles.profiles);
export const poolDoc = () => loadJson(kit().sourceFiles.poolRecords);

export type Provenance = { file: string; pointer: string; note?: string };

/** Full shared-pool jutsu record by kit code or by ID (October 9 pool capture). */
export const poolJutsuById = (id: string): { record: any; prov: Provenance } => {
  const caps = poolDoc().captures as any[];
  const idx = caps.findIndex((c) => c?.data?.id === id);
  if (idx < 0) throw new Error(`Pool jutsu ${id} not captured`);
  return {
    record: clone(caps[idx].data),
    prov: { file: kit().sourceFiles.poolRecords, pointer: `/captures/${idx}/data` },
  };
};
export const poolJutsuByCode = (code: string) => {
  const ref = kit().sharedReferences[code];
  if (!ref) throw new Error(`Unknown shared code ${code}`);
  return {
    record: clone(ptr(poolDoc(), ref.sourcePointer)),
    prov: { file: kit().sourceFiles.poolRecords, pointer: ref.sourcePointer },
  };
};
/** Retained legacy jutsu (first captured copy; M0 proves repeated copies identical). */
export const legacyJutsu = (id: string) => {
  const conv = (legacy().conversions as any[]).find((c) => c.targetId === id);
  if (!conv) throw new Error(`Legacy ${id} not in conversion packet`);
  return {
    record: clone(ptr(aiDoc(), conv.sourcePointers[0])),
    prov: { file: kit().sourceFiles.ai, pointer: conv.sourcePointers[0] },
    conversion: conv,
  };
};

export const entityByName = (name: string) => {
  const e = (kit().entities as any[]).find((x) => x.name === name);
  if (!e) throw new Error(`No entity ${name}`);
  return e;
};
export const entities = (): any[] => kit().entities;

export const capturedAi = (entity: any) => ({
  record: clone(ptr(aiDoc(), entity.aiSourcePointer)),
  prov: { file: kit().sourceFiles.ai, pointer: entity.aiSourcePointer },
});
export const capturedProfile = (entity: any) => ({
  record: clone(ptr(profDoc(), entity.profileSourcePointer)),
  prov: { file: kit().sourceFiles.profiles, pointer: entity.profileSourcePointer },
});

/** Generic committed-capture record by file + pointer. */
export const captured = (file: string, pointer: string) => ({
  record: clone(ptr(loadJson(file), pointer)),
  prov: { file, pointer },
});

/** Resolve one accepted kit member to its full record. */
export const resolveMember = (member: string) =>
  member.startsWith("legacy:")
    ? legacyJutsu(member.slice("legacy:".length))
    : poolJutsuByCode(member);

/** Map from captured jutsu ID to accepted kit member ID for one entity. */
export const memberIdMap = (entity: any): Record<string, string> => {
  const out: Record<string, string> = {};
  for (const m of entity.mapping) out[m.fromId] = resolveMember(m.to).record.id;
  return out;
};

const userJutsu = (userId: string, rec: any, level: number, idx: number) => ({
  id: `uj-${userId.slice(0, 6)}-${idx}-${rec.id}`,
  userId,
  jutsuId: rec.id,
  level,
  experience: 0,
  equipped: true,
  finishTraining: null,
  reskinId: null,
  jutsu: rec,
});

/** Battle-assembly fields the DB query supplies alongside the userData row. */
const queryShell = (aiProfile: any) => ({
  aiProfile,
  village: null,
  bloodline: null,
  sageMode: null,
  anbuSquad: null,
  clan: null,
  loadout: null,
  userSkills: [],
  bloodright: [],
  userQuests: [],
  completedQuests: [],
  questData: [],
  bounties: [],
  bountySignups: [],
});

/**
 * The October 1 AI capture predates upstream migration
 * `app/drizzle/migrations/0056_unified_combat_stats_masteries.sql` (commit 46f62cd9,
 * 2026-10-08), so captured rows carry per-type offence/defence columns and lack
 * the `offence`/`defence`/`*Mastery` columns the pinned engine fights with. This
 * applies that migration's own AI/summon branch, verbatim:
 *   offence = GREATEST(nin/gen/tai/bukiOffence), defence = GREATEST(...Defence),
 *   xMastery = GREATEST(xOffence, xDefence), bloodline/sage mastery = 10.
 * Captured per-type columns are left in place (unused by the pinned engine).
 * A fresh post-migration operator capture must confirm the live values.
 */
export const MIGRATION_0056 = "app/drizzle/migrations/0056_unified_combat_stats_masteries.sql (AI branch)";
export const migrate0056Ai = (row: any) => {
  if ("offence" in row && "defence" in row) return { row, applied: false };
  if (!(row.isAi || row.isSummon)) throw new Error("migrate0056Ai: only AI/summon rows");
  const t = ["ninjutsu", "genjutsu", "taijutsu", "bukijutsu"];
  row.offence = Math.max(...t.map((x) => row[`${x}Offence`]));
  row.defence = Math.max(...t.map((x) => row[`${x}Defence`]));
  for (const x of t) row[`${x}Mastery`] = Math.max(row[`${x}Offence`], row[`${x}Defence`]);
  row.bloodlineMastery = 10;
  row.sageMastery = 10;
  return { row, applied: true };
};

export type KitVariant = "captured" | "accepted";

/**
 * CombatQueryUser for one Ghost Ship AI. `captured` keeps the October 1 jutsu
 * list; `accepted` swaps in the RUL-2026-10-11-003 membership. Every other field
 * — numeric profile, innate effects (duplicates kept), items with their
 * equipped state and drop chances — is the captured record, unchanged.
 */
export const aiQueryUser = (entity: any, variant: KitVariant, profile: any) => {
  const { record: ai } = capturedAi(entity);
  migrate0056Ai(ai);
  const items = (ai.items ?? []).map((ui: any) => ({ ...ui, imbuements: [] }));
  let jutsus = ai.jutsus;
  if (variant === "accepted") {
    jutsus = entity.proposedKit.map((m: string, i: number) => {
      // Level: the captured level of any jutsu mapped onto this member (all
      // captured Ghost Ship AI jutsu are level 1; M0 reports this).
      const from = entity.mapping.filter((x: any) => x.to === m);
      const levels = from.map(
        (x: any) => ai.jutsus.find((uj: any) => uj.jutsuId === x.fromId)?.level ?? 1,
      );
      return userJutsu(ai.userId, resolveMember(m).record, Math.max(1, ...levels), i);
    });
  }
  return { ...ai, ...queryShell(profile), items, jutsus };
};

/* ----------------------------------------------------------------------------
 * Profiles
 * ------------------------------------------------------------------------- */

/** Captured profile unchanged (rules may reference jutsu no longer equipped). */
export const capturedRules = (entity: any) => capturedProfile(entity).record;

/**
 * Candidate rebuilt rules: the captured profile with every jutsu reference
 * remapped through the accepted mapping (fromId → accepted member). Combos that
 * collapse onto duplicates keep their order with consecutive duplicates removed.
 * includeDefaultRules is preserved. This is a RULE CHANGE proposal, reported
 * separately from the kit change.
 */
export const remappedRules = (entity: any) => {
  const p = capturedProfile(entity).record;
  const map = memberIdMap(entity);
  const changes: string[] = [];
  for (const [i, rule] of p.rules.entries()) {
    const a = rule.action;
    if (a.jutsuId && map[a.jutsuId] && map[a.jutsuId] !== a.jutsuId) {
      changes.push(`rule ${i}: jutsuId ${a.jutsuId} -> ${map[a.jutsuId]}`);
      a.jutsuId = map[a.jutsuId];
    }
    if (Array.isArray(a.comboIds)) {
      const before = [...a.comboIds];
      const mapped = a.comboIds.map((id: string) => map[id] ?? id);
      a.comboIds = mapped.filter((id: string, k: number) => k === 0 || id !== mapped[k - 1]);
      if (JSON.stringify(before) !== JSON.stringify(a.comboIds))
        changes.push(`rule ${i}: combo ${before.join(",")} -> ${a.comboIds.join(",")}`);
    }
  }
  return { profile: { ...p, id: `${p.id}::remapped` }, changes };
};

/** Sealwright candidate profiles from the rule contract (variants for A2). */
export const sealwrightProfile = (variant: "contract" | "noClosing" | "lateClosing") => {
  const plan = clone(contract().aiProfile.priorityOrderedRulePlan) as any[];
  const rules = plan.map((r) => ({ conditions: r.conditions, action: r.action }));
  const closingIdx = plan.findIndex((r) => r.role === "position for S31 shorter r3 Clear");
  if (variant !== "contract") {
    const [closing] = rules.splice(closingIdx, 1);
    if (variant === "lateClosing") rules.splice(rules.length - 1, 0, closing);
  }
  return {
    id: `sealwright::${variant}`,
    userId: "sealwright",
    name: `Sealwright ${variant}`,
    includeDefaultRules: contract().aiProfile.includeDefaultRules,
    rules,
  };
};

/**
 * Sealwright query user. Numeric profile carrier: the captured regular Captain
 * (level/rank/experience/raw stats/pools/regeneration/multipliers, which the
 * contract names as the starting candidate). Explicitly NOT copied: innate
 * effects (set to []), items (contract equipment []), jutsu (contract seven).
 * Stat/general preferences and elements are an open contract gate; the Captain's
 * are used as a labelled carrier.
 */
export const sealwrightQueryUser = (profile: any) => {
  const capt = migrate0056Ai(capturedAi(entityByName("The Captain")).record).row;
  const jutsus = (contract().jutsus as any[]).map((j, i) =>
    userJutsu("sealwright", poolJutsuById(j.liveJutsuId).record, 1, i),
  );
  return {
    ...capt,
    userId: "sealwright",
    username: "Sealwright",
    aiProfileId: profile.id,
    effects: [],
    items: [],
    jutsus,
    ...queryShell(profile),
  };
};

/* ----------------------------------------------------------------------------
 * Player fixtures (test carriers, not recommendations)
 * ------------------------------------------------------------------------- */

/**
 * Player kit members are captured shared-pool records referenced by ID. All are
 * non-elemental: the pinned engine filters elemental jutsu for players whose
 * elements do not match (AI users bypass that check), and fixtures carry none.
 */
export const PLAYER_KITS: Record<string, { ids: string[]; note: string }> = {
  buffer: {
    ids: [
      "yDznlfsnPaOSFtdjfCyTZ", // Sovereign Ascendance: IDG 60 + IDG 60 (SELF) + DDT 60, 3r
      "w4F7-w5ubgKsqYPBPvRuV", // Apex Hunger: IDG 60 / 99r + increasestat
      "I66lzvVHf8v4thxR6tEJn", // Cataclysm Fist: damage 70
      "ZvPl6uyJfwF5EjmLHouQR", // Annihilating Wave: damage 70 ALL
      "05rH3kZNXbtFq9a9iRl-W", // Light Barrier: shield
    ],
    note: "IDG-stacking buffer; exercises B32 threshold and both Clears",
  },
  striker: {
    ids: [
      "I66lzvVHf8v4thxR6tEJn", // Cataclysm Fist 70
      "ZvPl6uyJfwF5EjmLHouQR", // Annihilating Wave 70
      "b7ZOgdZmhZiUbCVrmQiwH", // Sundering Blow 50
      "Vo8N1luCT0p48y7JzKe84", // Heavy Cut 45
    ],
    note: "damage-only; no positive effects for Clear to remove",
  },
  moderate: {
    ids: [
      "taxbZNdm1Q7YL5AxaRssW", // Warrior's Poise IDG 30 / DDT 30
      "_9k7kSYUgMtB-AEFgRly5", // Windlash Focus IDG 20
      "I66lzvVHf8v4thxR6tEJn", // Cataclysm Fist 70
      "b7ZOgdZmhZiUbCVrmQiwH", // Sundering Blow 50
      "05rH3kZNXbtFq9a9iRl-W", // Light Barrier
    ],
    note: "moderate buffs that stay below the B32 threshold unless stacked",
  },
};

export type PlayerStatBand = "jonin-cap" | "jonin-cap-durable" | "jonin-half" | "upstream-helper";

/**
 * Player CombatQueryUser. Shape comes from the captured regular Captain row
 * (field set only); identity, AI flags, stats, pools, effects, items and jutsu
 * are overwritten. Stat bands:
 *  - jonin-cap: engine USER_CAPS JONIN stats/gens caps, calcHP/SP/CP(100) pools;
 *  - jonin-cap-durable: jonin-cap stats with pools × 2.5 (the Ghost Ship AIs'
 *    poolsMultiplier) so fights last long enough to measure control/uptime;
 *  - jonin-half: 50% of those caps, same pools;
 *  - upstream-helper: app/tests/libs/combat/helpers/battleScenario.ts defaults
 *    (stats 450000, generals 100000, pools 5000).
 */
export const playerQueryUser = (
  id: string,
  band: PlayerStatBand,
  kitName: keyof typeof PLAYER_KITS,
  profile: any,
  caps: { stats: number; gens: number; hp: number; sp: number; cp: number; masteryEach: number },
) => {
  const capt = capturedAi(entityByName("The Captain")).record;
  const capped = band === "jonin-cap" || band === "jonin-cap-durable";
  const stat = capped ? caps.stats : band === "jonin-half" ? caps.stats / 2 : 450_000;
  const gen = capped ? caps.gens : band === "jonin-half" ? caps.gens / 2 : 100_000;
  const pm = band === "jonin-cap-durable" ? 2.5 : 1;
  const pools =
    band === "upstream-helper"
      ? { hp: 5000, sp: 5000, cp: 5000 }
      : { hp: caps.hp * pm, sp: caps.sp * pm, cp: caps.cp * pm };
  // Post-0056 schema: one offence and one defence stat; masteries gate jutsu use
  // only (pool records require none), set to an even split of TOTAL_MASTERY_CAP
  // across the four combat arts for the capped bands.
  const mastery = band === "upstream-helper" ? 450_000 : capped ? caps.masteryEach : caps.masteryEach / 2;
  const u: any = {
    ...capt,
    userId: id,
    username: id,
    isAi: false,
    isSummon: false,
    isEvent: false,
    villageId: "village-player",
    aiProfileId: profile.id,
    statsMultiplier: 1,
    poolsMultiplier: 1,
    customTitle: null,
    effects: [],
    items: [],
    jutsus: PLAYER_KITS[kitName].ids.map((jid, i) =>
      userJutsu(id, poolJutsuById(jid).record, 1, i),
    ),
    curHealth: pools.hp, maxHealth: pools.hp,
    curChakra: pools.cp, maxChakra: pools.cp,
    curStamina: pools.sp, maxStamina: pools.sp,
    strength: gen, intelligence: gen, willpower: gen, speed: gen,
    preferredStat: null, preferredGeneral1: null, preferredGeneral2: null,
    offence: stat, defence: stat,
    ninjutsuMastery: mastery, genjutsuMastery: mastery, taijutsuMastery: mastery,
    bukijutsuMastery: mastery, bloodlineMastery: 10, sageMastery: 10,
    ...queryShell(profile),
  };
  // Pre-0056 per-type columns from the shape donor are not used by the pinned engine.
  for (const t of ["ninjutsu", "genjutsu", "taijutsu", "bukijutsu"])
    for (const s of ["Offence", "Defence"]) delete u[`${t}${s}`];
  return u;
};

/** Player auto-combat policies (declared test inputs, engine-executed). */
export const playerPolicy = (id: string, kitName: keyof typeof PLAYER_KITS) => {
  const use = (jutsuId: string, target: string, conditions: any[] = []) => ({
    conditions,
    action: { type: "use_specific_jutsu", jutsuId, target, description: "" },
  });
  const notHas = (effectType: string, threshold: number) => ({
    // "has_effect" with threshold acts as "at least"; we invert by ordering rules
    type: "has_effect", effectType, threshold, description: "",
  });
  const near = (v: number) => ({ type: "distance_lower_than", value: v, target: "CLOSEST_OPPONENT", description: "" });
  const far = (v: number) => ({ type: "distance_higher_than", value: v, target: "CLOSEST_OPPONENT", description: "" });
  const move = { conditions: [far(6)], action: { type: "move_towards_opponent", target: "CLOSEST_OPPONENT", description: "" } };
  const hp = { conditions: [], action: { type: "use_highest_power_action", effect: "damage", target: "CLOSEST_OPPONENT", description: "" } };
  const k = PLAYER_KITS[kitName].ids;
  let rules: any[] = [];
  if (kitName === "buffer") {
    rules = [
      use(k[0], "SELF"), // Sovereign Ascendance whenever ready
      use(k[1], "SELF"), // Apex Hunger whenever ready
      use(k[4], "SELF"), // Light Barrier whenever ready
      move,
      use(k[0 + 2], "CLOSEST_OPPONENT", [near(6)]),
      use(k[3], "CLOSEST_OPPONENT", [near(6)]),
      hp,
    ];
  } else if (kitName === "striker") {
    rules = [move, ...k.map((j) => use(j, "CLOSEST_OPPONENT", [near(6)])), hp];
  } else {
    rules = [
      use(k[0], "SELF"),
      use(k[1], "SELF"),
      use(k[4], "SELF"),
      move,
      use(k[2], "CLOSEST_OPPONENT", [near(6)]),
      use(k[3], "CLOSEST_OPPONENT", [near(6)]),
      hp,
    ];
  }
  void notHas;
  return { id: `policy::${id}::${kitName}`, userId: id, includeDefaultRules: false, rules };
};
