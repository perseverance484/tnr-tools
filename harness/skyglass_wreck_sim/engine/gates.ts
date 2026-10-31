/**
 * Law 40 distance gates (director, 2026-10-31, with RUL-2026-10-31-066): every `distance_lower_than` condition on a rule
 * that casts a shared-pool jutsu is set to exactly the jutsu's range + 1 (the pool file's `gate`), as Forge's
 * `kitProblems` (forge/src/runner/pool.mjs) requires: it refuses any other value on any `distance_lower_than` condition of
 * such a rule. The harness had gated at the range itself, which forfeits the outermost band (rule distance is the A* path
 * length including both endpoints, docs/ENGINE_LAWS.md law 40).
 *
 * Source of ranges and gates: the repository's generated `32b_DATA_pool.json` (the same file Forge bundles). Non-pool
 * jutsu (library set pieces, dungeon-new records, live records outside the pool) are left as they are, as Forge does.
 *
 * Applied to every enemy, ally and summon-template row in `assembleFloor` (sim.ts), and by the spec writers, so the specs
 * carry exactly what was simulated. `--old-gates` (any runner) keeps the previous gates (the pre-change measurements).
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";

export const LAW40_GATES = !process.argv.includes("--old-gates");
const REPO = process.env.TNR_REPO ?? join(import.meta.dir, "../../..");
const POOL: Record<string, { name: string; id: string; range: number | null; gate: number | null }> = JSON.parse(readFileSync(join(REPO, "32b_DATA_pool.json"), "utf8")).records;
export const POOL_GATE: Record<string, { name: string; range: number | null; gate: number | null }> = Object.fromEntries(
  Object.values(POOL).map((r) => [r.id, { name: r.name, range: r.range, gate: r.gate }]),
);

const CHANGES: Record<string, number> = {};

/** Returns the rules with law-40 gates (new objects only where a value changes) and counts changes per jutsu. */
export const gateRules = (rules: any[]) => {
  if (!LAW40_GATES || !Array.isArray(rules)) return rules;
  return rules.map((r) => {
    const rec = r?.action?.jutsuId ? POOL_GATE[r.action.jutsuId] : undefined;
    if (!rec || rec.gate == null || !Array.isArray(r.conditions)) return r;
    let changed = false;
    const conditions = r.conditions.map((c: any) => {
      if (c?.type !== "distance_lower_than" || c.value === rec.gate) return c;
      changed = true;
      const k = `${rec.name}: ${c.value} -> ${rec.gate}`;
      CHANGES[k] = (CHANGES[k] ?? 0) + 1;
      return { ...c, value: rec.gate };
    });
    return changed ? { ...r, conditions } : r;
  });
};

/** In place, on a profile object (`rules` replaced). */
export const gateProfile = (profile: any) => {
  if (profile && Array.isArray(profile.rules)) profile.rules = gateRules(profile.rules);
  return profile;
};

/** A spec's rule list: engine rules ({conditions, action}) or the spec writers' summaries ({when, do, note}). */
export const isRuleList = (v: any) => Array.isArray(v) && v.length > 0 && !!v[0] && typeof v[0] === "object" && ("action" in v[0] || "conditions" in v[0] || ("when" in v[0] && "do" in v[0]));
/** In place, on every AI-rule list in a spec / override object (the same walk as assertSpecRuleCap). */
export const gateSpec = (spec: any) => {
  const walk = (o: any) => {
    if (Array.isArray(o)) return o.forEach(walk);
    if (!o || typeof o !== "object") return;
    for (const [k, v] of Object.entries(o)) {
      if (k === "rules" && isRuleList(v)) {
        (o as any)[k] = "when" in (v as any[])[0]
          ? gateRules((v as any[]).map((r) => ({ conditions: r.when, action: r.do }))).map((g, i) => ({ ...(v as any[])[i], when: g.conditions }))
          : gateRules(v as any[]);
      } else walk(v);
    }
  };
  walk(spec);
  return spec;
};

/** Every rule in the rows that would fail Forge's gate check (after gating this must be empty). */
export const gateProblems = (rules: any[]) =>
  (rules ?? []).flatMap((r: any, i: number) => {
    const rec = r?.action?.jutsuId ? POOL_GATE[r.action.jutsuId] : undefined;
    if (!rec || rec.gate == null) return [];
    return (r.conditions ?? []).filter((c: any) => c?.type === "distance_lower_than" && c.value !== rec.gate).map((c: any) => `rules[${i}]: ${rec.name} gate ${c.value}, law 40 wants ${rec.gate}`);
  });

export const gateReport = () => ({ law40: LAW40_GATES, changedConditions: { ...CHANGES } });
