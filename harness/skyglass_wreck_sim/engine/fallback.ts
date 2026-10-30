/**
 * Library-wide fallback fix (RUL-2026-10-29-046 item 2): no enemy's fallback rule may fire a set piece or blast without
 * its mark; each enemy's last rule names the engine's basic attack instead of the highest-power action.
 *
 * - `SET_PIECE_MARK`: every jutsu that answers a mark (library blasts and signatures, plus records registered by the
 *   Crownhold builders), mapped to the marker effect type the caster carries while the mark is up.
 * - `fixFallback(profile, kitIds)`: the shared repair for profiles built from live rules (Haul guards, chart copies):
 *   every use_highest_power_action / use_highest_power_jutsu / use_random_jutsu / use_combo_action rule becomes the named
 *   basic attack (conditions kept), and `includeDefaultRules` is switched off with the engine's backup rules restated
 *   without their two highest-power rows (ai_v2.ts getBackupRules: three "move towards when farther than 2", "highest
 *   power within 2", "highest power at the barrier blocking the closest opponent").
 * - `auditEnemies(label, enemies)`: static audit, per enemy and per phase (the health bands its rules declare): the
 *   phase's terminal rule and every rule that could cast a set piece without its marker.
 * - Runtime guard (`noteAction`): sim.ts calls it around each AI action; a set piece cast while the caster did not
 *   carry its marker is recorded (`unmarkedReport()`), and every runner writes the report into its output.
 */
import { ANSWERS, MARKER_TYPES } from "./library";

export const BASIC_ATTACK = "basicAttack";
/** `--no-fallback-fix` (any runner) rebuilds the pre-fix rules, for the before/after audit and guard counts. */
export const FALLBACK_FIX = !process.argv.includes("--no-fallback-fix");
const FREE_PICK = new Set(["use_highest_power_action", "use_highest_power_jutsu", "use_random_jutsu", "use_combo_action"]);

/** Set-piece jutsu id -> marker effect type (the has_effect condition its rule must carry). */
export const SET_PIECE_MARK: Record<string, string> = Object.fromEntries(Object.entries(ANSWERS).map(([id, k]) => [id, MARKER_TYPES[k]]));
export const registerSetPiece = (id: string, markerType: string) => {
  SET_PIECE_MARK[id] = markerType;
};
const MARKER_SET = new Set(Object.values(MARKER_TYPES));

const ruleJutsu = (r: any) => r?.action?.jutsuId as string | undefined;
const markerCond = (r: any) => (r.conditions ?? []).find((c: any) => c.type === "has_effect" && MARKER_SET.has(c.effectType));

/** Any jutsu a rule fires only behind a marker condition, beyond the registered set (catches builder-local records). */
const inferSetPieces = (rules: any[]) => {
  for (const r of rules) {
    const id = ruleJutsu(r);
    const m = markerCond(r);
    if (id && m && r.action.type === "use_specific_jutsu" && !id.startsWith("lib-omen") && !SET_PIECE_MARK[id] && /blast|sig|crownfall|command|maw|quench|broadside|bell/i.test(id))
      SET_PIECE_MARK[id] = m.effectType;
  }
};

export const basicRule = (description: string, target = "CLOSEST_OPPONENT", conditions: any[] = []) => ({
  conditions, action: { type: "use_specific_jutsu", jutsuId: BASIC_ATTACK, target, description },
});

/** Repair a profile built from live rules; returns the new profile and what changed. */
export const fixFallback = (profile: any, kitIds: string[]) => {
  if (!FALLBACK_FIX) return { profile, changes: [] as string[] };
  const changes: string[] = [];
  const rules = (profile.rules ?? []).map((r: any) => {
    if (FREE_PICK.has(r.action?.type) && (r.action.effect ?? "damage") === "damage" && !String(r.action.target ?? "").includes("ALLY") && r.action.target !== "SELF") {
      changes.push(`${r.action.type} -> basic attack (${r.action.description || "fallback"})`);
      return { ...r, action: { type: "use_specific_jutsu", jutsuId: BASIC_ATTACK, target: r.action.target === "BARRIER_BLOCKING_CLOSEST_OPPONENT" ? "CLOSEST_OPPONENT" : (r.action.target ?? "CLOSEST_OPPONENT"), description: `basic attack (was ${r.action.type}${r.action.description ? `: ${r.action.description}` : ""})` } };
    }
    return r;
  });
  let includeDefaultRules = !!profile.includeDefaultRules;
  if (includeDefaultRules) {
    includeDefaultRules = false;
    rules.push(
      { conditions: [{ type: "distance_higher_than", value: 2, target: "CLOSEST_OPPONENT", description: "" }], action: { type: "move_towards_opponent", target: "CLOSEST_OPPONENT", description: "backup: close in (engine backup rule, restated)" } },
      basicRule("backup: basic attack (engine backup rule, restated without highest power)"),
    );
    changes.push("includeDefaultRules true -> false; engine backup rules restated (move towards, basic attack)");
  }
  void kitIds;
  return { profile: { ...profile, rules, includeDefaultRules }, changes };
};

/* ------------------------------------------------------------------ static audit */
export type AuditRow = {
  set: string; id: string; name: string; includeDefaultRules: boolean; setPiecesInKit: string[]; lastRule: string;
  phases: { band: string; terminal: string }[]; violations: string[];
};
const describe = (r: any) => {
  if (!r) return "(none)";
  const a = r.action;
  if (a.type === "use_specific_jutsu") return a.jutsuId === BASIC_ATTACK ? "basic attack" : `jutsu ${a.jutsuId}`;
  return a.type;
};
const hpBelow = (r: any) => (r.conditions ?? []).filter((c: any) => c.type === "health_below").map((c: any) => c.value as number);
export const auditEnemy = (set: string, id: string, name: string, profile: any, kitIds: string[]): AuditRow => {
  const rules: any[] = profile?.rules ?? [];
  inferSetPieces(rules);
  const kitSP = kitIds.filter((j) => SET_PIECE_MARK[j]);
  const violations: string[] = [];
  const idr = !!profile?.includeDefaultRules;
  if (idr && kitSP.length) violations.push("includeDefaultRules: the engine's backup highest-power rules can cast a set piece unmarked");
  rules.forEach((r, i) => {
    const t = r.action?.type;
    if (FREE_PICK.has(t) && kitSP.length && (r.action.effect ?? "damage") === "damage") violations.push(`rule ${i} ${t}: may pick ${kitSP.join("/")} unmarked`);
    const j = ruleJutsu(r);
    if (t === "use_specific_jutsu" && j && SET_PIECE_MARK[j]) {
      const m = markerCond(r);
      if (!m) violations.push(`rule ${i}: casts set piece ${j} with no marker condition`);
      else if (m.effectType !== SET_PIECE_MARK[j]) violations.push(`rule ${i}: set piece ${j} behind the wrong marker (${m.effectType}, wants ${SET_PIECE_MARK[j]})`);
    }
  });
  // Phases: the health bands the rules declare (health_below thresholds).
  const cuts = [...new Set(rules.flatMap(hpBelow))].sort((a, b) => b - a);
  const bounds = [100, ...cuts, 0];
  const phases = bounds.slice(0, -1).map((hi, k) => {
    const lo = bounds[k + 1]!;
    const active = rules.filter((r) => hpBelow(r).every((v) => v >= hi));
    // Terminal: the last active rule with no conditions beyond health (what fires when nothing else does).
    const uncond = active.filter((r) => (r.conditions ?? []).every((c: any) => c.type === "health_below"));
    const term = uncond[uncond.length - 1] ?? active[active.length - 1];
    return { band: `${hi}-${lo}%`, terminal: describe(term) };
  });
  return { set, id, name, includeDefaultRules: idr, setPiecesInKit: kitSP, lastRule: describe(rules[rules.length - 1]), phases, violations };
};
export const auditTemplates = (set: string, enemies: Record<string, { row: any; profile: any }>, only?: Set<string>) =>
  Object.entries(enemies)
    .filter(([id]) => !only || only.has(id))
    .map(([id, t]) => auditEnemy(set, id, t.row?.username ?? id, t.profile, (t.row?.jutsus ?? []).map((uj: any) => uj.jutsuId ?? uj.jutsu?.id)));

/* ------------------------------------------------------------------ runtime guard */
const UNMARKED: { actor: string; name: string; jutsu: string; round: number; marker: string }[] = [];
let SET_PIECE_CASTS = 0;
/** Before an AI action: the marker types the actor carries. */
export const markersOf = (battle: any, userId: string) =>
  new Set<string>((battle.usersEffects ?? []).filter((e: any) => e.targetId === userId && MARKER_SET.has(e.type)).map((e: any) => e.type));
/** After it: record a set piece cast without its marker. */
export const noteAction = (before: Set<string>, actor: any, actionId: string | null | undefined, round: number) => {
  if (!actionId) return;
  const m = SET_PIECE_MARK[actionId];
  if (!m) return;
  SET_PIECE_CASTS++;
  if (!before.has(m)) UNMARKED.push({ actor: actor.userId, name: actor.username, jutsu: actionId, round, marker: m });
};
export const unmarkedReport = () => {
  const byEnemyJutsu: Record<string, number> = {};
  for (const u of UNMARKED) byEnemyJutsu[`${u.name} / ${u.jutsu}`] = (byEnemyJutsu[`${u.name} / ${u.jutsu}`] ?? 0) + 1;
  return { setPieceCasts: SET_PIECE_CASTS, unmarkedCasts: UNMARKED.length, byEnemyJutsu, first: UNMARKED.slice(0, 10) };
};
