/**
 * Kit-building helpers for dungeon-only jutsu and AI rules (harness design aid).
 *
 * New jutsu are built field-for-field on captured records (shape donors), then passed through the
 * live `JutsuValidator` and their rules through the live `AiRule` schema, so every record the
 * harness fights with is one the Forge would accept. Tag shapes come from captured tags of the same
 * type where one exists, otherwise from the tag's own zod schema defaults.
 */
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { AiRule } from "@/validators/ai";
import { AllTags, JutsuValidator } from "@/validators/combat";

const REPO = process.env.TNR_REPO!;
const cache = new Map<string, any>();
const doc = (f: string) => {
  if (!cache.has(f)) cache.set(f, JSON.parse(readFileSync(join(REPO, f), "utf8")));
  return cache.get(f);
};
const harvests = () => readdirSync(join(REPO, "harvests/inbox")).filter((f) => f.endsWith(".json")).map((f) => `harvests/inbox/${f}`);

/** Newest captured jutsu record with this id (by updatedAt) across the committed harvests. */
export const capturedJutsu = (id: string) => {
  let best: any = null;
  let src = "";
  const walk = (x: any, f: string) => {
    if (Array.isArray(x)) x.forEach((v) => walk(v, f));
    else if (x && typeof x === "object") {
      if (x.id === id && "jutsuType" in x && Array.isArray(x.effects) && (!best || (x.updatedAt ?? "") > (best.updatedAt ?? ""))) {
        best = x;
        src = f;
      }
      for (const v of Object.values(x)) walk(v, f);
    }
  };
  for (const f of harvests()) walk(doc(f), f);
  if (!best) throw new Error(`jutsu ${id} not captured`);
  return { record: structuredClone(best), source: src };
};

/** Shape donors (captured AI-type records unless noted). */
export const DONORS = {
  base: "3v9c1SHlD2GLPF2HW1_Sc", // Twin Kunai: plain AI single-target record
  ground: "VmZzkyfPswbJLXvuB-mcV", // Drowning Mire: GROUND AOE with damage + visual + IDT tags
  redirection: "nOYLPmN3TXj6wEe_oE6HQ", // Sovereign Undertow
  increasecooldown: "v6xrznZRrlpipX9azTJrt", // Hindering Strike
  stealth: "IBjVpLutojh3m9PRnIce-", // Veilstep
  clone: "LQ26G2ANWkbTRL7Ry__F0", // Split Image
  shield: "05rH3kZNXbtFq9a9iRl-W", // Light Barrier
  allyHeal: "xs-8r_KRJS8QQMpBDyhUv", // Demon Maiden's Howl (ALLY target, heal + shield)
  cleanse: "HcAs8gBtvopPZkjP8HCC2", // Purging Stance
  poison: "LiVOnYq6qHzjB0XkIIA2e", // Venom Strike
  barrier: "i4lGrYY5HNN2Q2GPToKUS", // Adamantine Fortress (AOE_LARGE_WALL_SHOOT barrier)
  core: "nCQETf-HNnbRec1OSY2-R", // Core Rupture (stun + pierce + onehitkill)
  pct: "Cw51Wm_Uy0GiIkiEjlQtn", // Opening Strike (increasedamagetaken percentage row)
  wound: "nS-iidYFYqWE9Z-UkC84y", // Scorching Sun Strike (wound)
  seal: "RPdeeWhFI5AIUUpJXwUlf", // Sovereign Fetters (stun + seal)
  dr: "6UE5jC71Y6nRjobkJ-UTV", // Folding Screen Guard (absorb + decreasedamagetaken)
  idg: "0Y10JpChssDwFUxNRk6p3", // Unbroken Command (increasedamagegiven + increasestat)
  heal: "STu1VHNcfgeC3x-UiQDgt", // Second Wind
} as const;

const tagDonor = (() => {
  const byType = new Map<string, any>();
  return (type: string, preferId?: string) => {
    const key = `${type}:${preferId ?? ""}`;
    if (!byType.has(key)) {
      const ids = [preferId, ...Object.values(DONORS)].filter(Boolean) as string[];
      let t: any = null;
      for (const id of ids) {
        t = capturedJutsu(id).record.effects.find((e: any) => e.type === type);
        if (t) break;
      }
      byType.set(key, t ? structuredClone(t) : null);
    }
    return structuredClone(byType.get(key));
  };
})();

const ANIM_FIELDS = { appearAnimation: "", staticAnimation: "", disappearAnimation: "", appearSfx: "", disappearSfx: "", staticAssetPath: "" };

/** A tag of `type`: captured donor shape (or schema defaults), then `over`. Validated by AllTags. */
export const tag = (type: string, over: Record<string, unknown> = {}) => {
  const donor = tagDonor(type) ?? {};
  const t = { ...ANIM_FIELDS, ...donor, type, powerPerLevel: 0, description: donor.description ?? "placeholder", ...over };
  const parsed = AllTags.safeParse(t);
  if (!parsed.success) throw new Error(`tag ${type}: ${parsed.error.message}`);
  return parsed.data as any;
};

/** Animation placeholder ids (docs/design/SKYGLASS_BOSS_ANIMATIONS.md and SKYGLASS_BOSS_FIGHTS.md). */
export const anim = (id: string) => id;

/* Common tags */
export const T = {
  damage: (power: number, o: Record<string, unknown> = {}) => tag("damage", { power, rounds: 0, friendlyFire: "ENEMIES", ...o }),
  pierce: (power: number, o: Record<string, unknown> = {}) => tag("pierce", { power, rounds: 0, friendlyFire: "ENEMIES", ...o }),
  /** Persistent ground damage: hits on landing, then each turn start a unit stands there. */
  pool: (power: number, rounds: number, o: Record<string, unknown> = {}) => tag("damage", { power, rounds, friendlyFire: "ENEMIES", ...o }),
  visual: (animation: string, rounds: number, o: Record<string, unknown> = {}) => tag("visual", { rounds, staticAnimation: animation, ...o }),
  /**
   * Self "primed" marker: increasecooldown with no actionsAffected (no gameplay effect). Not a
   * SHARED_COOLDOWN_TAGS type, so it does not put the boss's other marker jutsu on the 3-round
   * global cooldown (increasepoolcost does). 1 round: applied castThisRound, so it is present on
   * the caster's next turn and gone the turn after.
   */
  marker: (power: number, rounds = 1) => tag("increasecooldown", { power, rounds, target: "SELF", calculation: "static", actionsAffected: [] }),
  /** Second marker family (increaserange, no actionsAffected): the phase-1 "recover" beat. */
  beat: (power = 1, rounds = 1) => tag("increaserange", { power, rounds, target: "SELF", calculation: "static", actionsAffected: [] }),
  pct: (type: string, power: number, rounds: number, o: Record<string, unknown> = {}) => tag(type, { power, rounds, calculation: "percentage", ...o }),
  stun: (rounds: number, o: Record<string, unknown> = {}) => tag("stun", { power: 100, rounds, ...o }),
  seal: (rounds: number, o: Record<string, unknown> = {}) => tag("seal", { power: 100, rounds, ...o }),
  root: (rounds: number, o: Record<string, unknown> = {}) => tag("moveprevent", { power: 100, rounds, ...o }),
  pull: (power: number, o: Record<string, unknown> = {}) => tag("redirection", { power, rounds: 0, direction: "pull", ...o }),
  push: (power: number, o: Record<string, unknown> = {}) => tag("redirection", { power, rounds: 0, direction: "push", ...o }),
  cleanseSelf: () => tag("cleanse", { power: 100, rounds: 0, target: "SELF" }),
  cleanse: (o: Record<string, unknown> = {}) => tag("cleanse", { power: 100, rounds: 0, ...o }),
  heal: (power: number, o: Record<string, unknown> = {}) => tag("heal", { power, rounds: 0, calculation: "percentage", poolsAffected: ["Health"], ...o }),
};

/** Base record for a new dungeon-only jutsu (Twin Kunai shape), validated by the live JutsuValidator. */
export const jutsu = (id: string, f: {
  name: string; description: string; battleDescription: string; target: string; method: string; range: number;
  cooldown: number; actionCostPerc: number; effects: any[]; coordinateTargeting?: any; donor?: string;
}) => {
  const base = capturedJutsu(f.donor ?? DONORS.base).record;
  const rec = {
    ...base, id, name: f.name, description: f.description, battleDescription: f.battleDescription,
    target: f.target, method: f.method, range: f.range, cooldown: f.cooldown, actionCostPerc: f.actionCostPerc,
    effects: f.effects, coordinateTargeting: f.coordinateTargeting ?? null, methodSize: null,
    jutsuType: "AI", battleUsageType: "BOTH", elementClassification: "None", statClassification: base.statClassification ?? "None",
    requiredLevel: 1, requiredRank: "STUDENT", hidden: true, villageId: "", bloodlineId: "", requiredBloodlineItemId: null,
    reskinParentJutsuId: null, bloodlineReskinId: null, parentJutsuId: null,
  };
  const parsed = JutsuValidator.safeParse(rec);
  if (!parsed.success) throw new Error(`jutsu ${f.name}: ${JSON.stringify(parsed.error.issues.slice(0, 4))}`);
  return { ...rec, ...parsed.data, id, createdAt: base.createdAt, updatedAt: base.updatedAt } as any;
};

/** A dungeon copy of a captured jutsu: same record, new id/name/text/cooldown. */
export const copyJutsu = (srcId: string, id: string, over: Record<string, unknown>, catalog?: Record<string, any>) => {
  const src = structuredClone(catalog?.[srcId] ?? capturedJutsu(srcId).record);
  const rec = { ...src, id, hidden: true, ...over };
  const parsed = JutsuValidator.safeParse(rec);
  if (!parsed.success) throw new Error(`copy ${srcId} -> ${id}: ${JSON.stringify(parsed.error.issues.slice(0, 4))}`);
  return { ...rec, ...parsed.data, id } as any;
};

/* Rules */
const C = {
  hp: (v: number) => ({ type: "health_below", value: v, description: "" }),
  far: (v: number, target = "CLOSEST_OPPONENT") => ({ type: "distance_higher_than", value: v, target, description: "" }),
  near: (v: number, target = "CLOSEST_OPPONENT") => ({ type: "distance_lower_than", value: v, target, description: "" }),
  within: (minRange: number, maxRange: number) => ({ type: "player_within_range", minRange, maxRange, description: "" }),
  roundGt: (v: number) => ({ type: "round_greater_than", value: v, description: "" }),
  marker: (threshold: number, effectType = "increasecooldown") => ({ type: "has_effect", effectType, threshold, description: "" }),
  targetHas: (target: string, threshold: number, effectType = "increasepoolcost") => ({ type: "target_has_effect", effectType, target, threshold, description: "" }),
  noSummon: () => ({ type: "does_not_have_summon", description: "" }),
};
export const cond = C;
export const rule = (note: string, conditions: any[], action: any) => {
  const r = { conditions, action: { description: note, ...action } };
  const parsed = AiRule.safeParse(r);
  if (!parsed.success) throw new Error(`rule "${note}": ${parsed.error.message}`);
  return parsed.data as any;
};
export const cast = (note: string, jutsuId: string, target: string, conditions: any[] = []) =>
  rule(note, conditions, { type: "use_specific_jutsu", jutsuId, target });
export const moveTo = (note: string, target: string, conditions: any[] = []) => rule(note, conditions, { type: "move_towards_opponent", target });
export const endTurn = (note = "end turn", conditions: any[] = []) => rule(note, conditions, { type: "end_turn" });
export const highest = (note: string, target: string, conditions: any[] = []) => rule(note, conditions, { type: "use_highest_power_action", effect: "damage", target });
