/**
 * The game server's AI rule cap (RUL-2026-10-31-066 item 1).
 *
 * Source (theninjarpg@3314d122, unchanged from the harness engine pin c86f43f4):
 * - `app/drizzle/constants.ts:1933`: `export const AI_PROFILE_MAX_RULES = 20;`
 * - `app/src/server/api/routers/ai.ts:87` (`updateAiProfile`): `if (input.rules.length > AI_PROFILE_MAX_RULES) return
 *   errorResponse("Maximum of 20 rules allowed")`. This is the route both builders use to push behaviour
 *   (`builder_bundle.js` aiProfPush, Forge `profileUpdate`). The cap counts the authored `rules` array only: the engine's
 *   backup rules (`includeDefaultRules`) and its appended end-turn rule are added at battle time and do not count.
 * - `app/src/validators/pets.ts:141`: the same cap on pet instructions (`.max(AI_PROFILE_MAX_RULES)`).
 * (`createAiProfile` has no cap, but it only creates an empty profile; rules always arrive through `updateAiProfile`.)
 *
 * Every runner builds its AI rows through `assembleFloor` (sim.ts), which calls `assertRuleCap` on every enemy, ally and
 * summon-template row, so a profile over the cap fails the run instead of being simulated. `--allow-over-cap` (any
 * runner) downgrades the failure to a recorded warning, only to reproduce pre-trim measurements.
 */
import { gateSpec, isRuleList } from "./gates";

export const AI_PROFILE_MAX_RULES = 20;
export const ALLOW_OVER_CAP = process.argv.includes("--allow-over-cap");

const OVER: Record<string, number> = {};

export const ruleCount = (profile: any) => (Array.isArray(profile?.rules) ? profile.rules.length : 0);

/** Throws (or records, under --allow-over-cap) when a profile has more authored rules than the server accepts. */
export const checkRuleCap = (label: string, profile: any) => {
  const n = ruleCount(profile);
  if (n <= AI_PROFILE_MAX_RULES) return n;
  OVER[label] = n;
  const msg = `HARNESS: AI rule cap: ${label} has ${n} rules; the server rejects more than ${AI_PROFILE_MAX_RULES} (AI_PROFILE_MAX_RULES, ai.updateAiProfile)`;
  if (!ALLOW_OVER_CAP) throw new Error(msg);
  return n;
};

/** Every AI row a battle is assembled from (enemies, quest allies, summon templates). */
export const assertRuleCap = (rows: Record<string, any>) => {
  for (const [id, row] of Object.entries(rows ?? {})) {
    if (!row || String(row.userId ?? id).includes("user_")) continue; // harness players drive auto-combat profiles
    if (row.aiProfile) checkRuleCap(`${row.username ?? id} (${id})`, row.aiProfile);
  }
};

/**
 * Spec writers call this before writing: applies the law-40 gates (gates.ts) to every `rules` list of AI rules in place,
 * so the spec carries what was simulated, then checks each list against the cap.
 */
export const assertSpecRuleCap = (label: string, spec: any) => {
  gateSpec(spec);
  const found: { path: string; n: number }[] = [];
  const walk = (o: any, path: string) => {
    if (Array.isArray(o)) return o.forEach((v, i) => walk(v, `${path}/${i}`));
    if (!o || typeof o !== "object") return;
    for (const [k, v] of Object.entries(o)) {
      if (k === "rules" && isRuleList(v)) {
        found.push({ path: `${path}/${k}`, n: v.length });
        checkRuleCap(`${label}${path}`, { rules: v });
      }
      walk(v, `${path}/${k}`);
    }
  };
  walk(spec, "");
  return found;
};

export const overCapReport = () => ({ cap: AI_PROFILE_MAX_RULES, allowOverCap: ALLOW_OVER_CAP, overCap: { ...OVER } });
