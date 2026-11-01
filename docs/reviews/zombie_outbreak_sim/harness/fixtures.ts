/**
 * Zombie Outbreak / Vanquish the Horde offline fight fixtures.
 * Every AI, jutsu, item and rule set is a committed live capture in tnr-tools; nothing is invented
 * except the player carriers (declared test inputs, see playerUser).
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { scaleUserStats } from "@/libs/profile";

export const REPO = process.env.TNR_REPO ?? "/home/claude/tnr-tools";
const load = (rel: string) => JSON.parse(readFileSync(join(REPO, rel), "utf8"));
const clone = <T>(x: T): T => structuredClone(x);

/** 2026-11-01 recapture (push/401): quests, Patient Zero + kit, wave AIs, all with nested jutsu/items. */
export const B_LIVE = "harvests/inbox/tnr_results_1793568292560.json";
/** 2026-10-30 capture (push/332): shared zombie AiProfile UXMYxPQd6aL8P1YAZayYU. */
export const B_ZPROFILE = "harvests/inbox/tnr_results_1793412740001.json";
/** 2026-10-21 shared-pool jutsu capture, source of the player kits. */
export const B_POOL = "harvests/inbox/tnr_results_1792983091495.json";
/** Patient Zero's rules as created and VERIFIED by push/336. */
export const M_PZ = "archive/spent-manifests/push-2026-10-30/336_patient_zero_and_pyramid.json";

const caps = (rel: string) => load(rel).captures as any[];
const pick = (rel: string, key: string) => {
  const c = caps(rel).find((x) => (x.input?.id ?? x.input?.userId) === key);
  if (!c?.data) throw new Error(`capture ${key} not in ${rel}`);
  return clone(c.data);
};

export const IDS = {
  voth: "0U8N6218b095-TQbWlCep",
  patientZero: "Pe5J6m1sc1IMpF2HF6Rby",
  protector: "uzlBfwiKdcH44ZZ0ZGw16",
  youngling: "TK7UuEQqnlJm0s1M66-EX",
  elite: "vxW8lqo2cZEhZpygev-Vs",
  villager: "nqL-uL-Z_7I0iuowlpBDx",
};

export const liveQuest = () => pick(B_LIVE, IDS.voth);

const queryShell = (aiProfile: any) => ({
  aiProfile, village: null, bloodline: null, sageMode: null, anbuSquad: null, clan: null,
  loadout: null, userSkills: [], bloodright: [], userQuests: [], completedQuests: [],
  questData: [], bounties: [], bountySignups: [],
});

export const zombieProfile = () => pick(B_ZPROFILE, "UXMYxPQd6aL8P1YAZayYU");
export const patientZeroProfile = () => {
  const m = load(M_PZ);
  const ai = m.items.find((e: any) => e.entity === "ai").data;
  return { id: "bdJbhPqB6sA9Mof_KmEGA", userId: IDS.patientZero, includeDefaultRules: ai.includeDefaultRules, rules: clone(ai.rules) };
};

/** One AI copy for battle, with a unique userId per copy (the router clones templates the same way). */
export const aiCopy = (templateId: string, n: number, profile: any, equipClaws = false) => {
  const ai = pick(B_LIVE, templateId);
  // What-if: equip Zombie Claws the way the Zombie Villager (nqL-) has them (equipped CHEST).
  if (equipClaws) for (const ui of ai.items ?? []) if (ui.itemId === "mMl6P4B7v6-_CyDo3HVG7") ui.equipped = "CHEST";
  // What-if (SIM_CLAW_FIX=1): Zombie Claws' damage made instant (rounds: 0) instead of a permanent stacking DoT.
  if (process.env.SIM_CLAW_FIX === "1") for (const ui of ai.items ?? []) for (const e of ui.item?.effects ?? []) if (e.type === "damage") e.rounds = 0;
  const uid = `${templateId}#${n}`;
  // What-if (SIM_PZ_MULT): Patient Zero's statsMultiplier; stored (unscaled) stats rescaled by the same ratio.
  if (templateId === IDS.patientZero && process.env.SIM_PZ_MULT) {
    const m = Number(process.env.SIM_PZ_MULT), r = m / (ai.statsMultiplier || 1);
    for (const k of ["offence", "defence", "strength", "intelligence", "willpower", "speed",
      "ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery"]) ai[k] = ai[k] * r;
    ai.statsMultiplier = m;
  }
  return {
    ...ai,
    userId: uid,
    username: `${ai.username} ${n}`,
    items: (ai.items ?? []).map((ui: any) => ({ ...ui, userId: uid, imbuements: [] })),
    jutsus: (ai.jutsus ?? []).map((uj: any) => ({ ...uj, userId: uid })),
    ...queryShell(profile),
  };
};

const poolRecord = (id: string) => {
  const c = caps(B_POOL).find((x) => x.proc === "jutsu.get" && x.data?.id === id);
  if (!c) throw new Error(`pool jutsu ${id} not captured`);
  return clone(c.data);
};

/** Player kits (declared carriers, built from captured shared-pool records; not recommendations). */
export const PLAYER_KITS = {
  // A mid-game kit: two 45-50 power strikes at range 5 and a damage/defence stance.
  basic: ["Vo8N1luCT0p48y7JzKe84", "b7ZOgdZmhZiUbCVrmQiwH", "taxbZNdm1Q7YL5AxaRssW"],
  // A stronger kit: a 70 power nuke, a 50 strike, the stance and a shield.
  strong: ["I66lzvVHf8v4thxR6tEJn", "b7ZOgdZmhZiUbCVrmQiwH", "taxbZNdm1Q7YL5AxaRssW", "05rH3kZNXbtFq9a9iRl-W"],
} as const;
export type KitName = keyof typeof PLAYER_KITS;

export const rankForLevel = (level: number) => (level <= 30 ? "GENIN" : level <= 50 ? "CHUNIN" : "JONIN");

/**
 * Player carrier. Stats: the engine's own "player" budget for the level (scaleUserStats over an even
 * spread, i.e. every experience point spent on combat stats), times `band` (1 = fully trained for the
 * level, 0.6 = under-trained). Pools from the level (calcHP/SP/CP). No armour, items, bloodline,
 * pets or jutsu levels: a deliberately plain baseline, so real geared players do better.
 */
export const playerUser = (level: number, band: number, kit: KitName, profile: any) => {
  const shape = pick(B_LIVE, IDS.protector);
  const id = "player";
  const u: any = {
    ...shape,
    userId: id, username: `Player L${level}`, isAi: false, isSummon: false, isEvent: false,
    villageId: "village-player", rank: rankForLevel(level), level, experience: 0,
    statsMultiplier: 1, poolsMultiplier: 1, regeneration: 60, customTitle: null, effects: [],
    items: [],
    offence: 100, defence: 100, strength: 100, intelligence: 100, willpower: 100, speed: 100,
    ninjutsuMastery: 100, genjutsuMastery: 100, taijutsuMastery: 100, bukijutsuMastery: 100,
    bloodlineMastery: 10, sageMastery: 10,
    preferredGeneral1: null, preferredGeneral2: null,
    aiProfileId: profile.id,
  };
  scaleUserStats(u, "player", { reweight: true });
  for (const k of ["offence", "defence", "strength", "intelligence", "willpower", "speed",
    "ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery"]) u[k] = 10 + (u[k] - 10) * band;
  u.jutsus = PLAYER_KITS[kit].map((jid, i) => ({
    id: `uj-player-${i}`, userId: id, jutsuId: jid, level: 1, experience: 0, equipped: true,
    finishTraining: null, reskinId: null, jutsu: poolRecord(jid),
  }));
  return { ...u, ...queryShell(profile) };
};

/** Player auto-combat policy: stance and shield when ready, then strikes in range, then close in. */
export const playerPolicy = (kit: KitName) => {
  const k = PLAYER_KITS[kit];
  const use = (jutsuId: string, target: string, conditions: any[] = []) => ({
    conditions, action: { type: "use_specific_jutsu", jutsuId, target, description: "" },
  });
  const near = (v: number) => ({ type: "distance_lower_than", value: v, target: "CLOSEST_OPPONENT", description: "" });
  const move = { conditions: [], action: { type: "move_towards_opponent", target: "CLOSEST_OPPONENT", description: "" } };
  const rules =
    kit === "basic"
      ? [use(k[2], "SELF"), use(k[1], "CLOSEST_OPPONENT", [near(6)]), use(k[0], "CLOSEST_OPPONENT", [near(6)]), move]
      : [use(k[2], "SELF"), use(k[3], "SELF"), use(k[0], "CLOSEST_OPPONENT", [near(6)]), use(k[1], "CLOSEST_OPPONENT", [near(6)]), move];
  return { id: `policy::player::${kit}`, userId: "player", includeDefaultRules: true, rules };
};
