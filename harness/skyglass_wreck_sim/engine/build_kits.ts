/**
 * Build the dungeon-copy kits and export them.
 *
 *   TNR_SCRIPT=build_kits.ts run.sh [--params params.json] [--override-out overrides/kits_endgame.json]
 *       [--spec-out build_spec.json]
 *
 * Writes the harness override (fought by main.ts) and the build spec section for the endgame
 * version: per AI the resolved stats, pools, level, multipliers, effect rows, jutsu list and ordered
 * rules; per new jutsu the full record with animation placeholder ids. Every new jutsu passed the
 * live JutsuValidator and every rule the live AiRule schema while being built (kitlib.ts).
 */
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { insertAiSchema } from "@/validators/aiInput";
import { JutsuValidator } from "@/validators/combat";
import { buildEndgame, DEFAULT_PARAMS, type KitParams } from "./kits";
import { buildTemplates, loadJson } from "./model";

const args = process.argv.slice(2);
const opt = (k: string) => {
  const i = args.indexOf(`--${k}`);
  return i >= 0 ? args[i + 1] : undefined;
};
const H = process.env.TNR_HARNESS!;
const baseline = loadJson(join(H, "data/baseline.json"));
const paramsPath = opt("params");
const params: KitParams = paramsPath ? { ...DEFAULT_PARAMS, ...loadJson(resolve(paramsPath)), pow: { ...DEFAULT_PARAMS.pow, ...(loadJson(resolve(paramsPath)).pow ?? {}) } } : DEFAULT_PARAMS;
const version = opt("version") ?? "endgame";

const { override } = buildEndgame(params);
// Core Rupture v2 (live record as edited by push/316-317; RUL-2026-10-28-001) from the tuned override.
const tuned = loadJson(join(H, "overrides/director_6wave_tuned.json"));
(override.jutsu as any)["nCQETf-HNnbRec1OSY2-R"] = tuned.jutsu["nCQETf-HNnbRec1OSY2-R"];
override.name = `kits_${version}`;

const ovOut = resolve(opt("override-out") ?? join(H, `overrides/kits_${version}.json`));
writeFileSync(ovOut, `${JSON.stringify(override, null, 1)}\n`);
console.log(`wrote ${ovOut}`);

/* ---------------- build spec ---------------- */
const t = buildTemplates(baseline, override as never);
const ANIM_IDS = /^(tg|dt|ch|cp|cc)_[a-z_]+$|^(mark-sigil|chain-hook-hit|skyglass-pane)$/;
const anims = (rec: any) => {
  const out = new Set<string>();
  for (const e of rec.effects) for (const k of ["appearAnimation", "staticAnimation", "disappearAnimation"]) if (typeof e[k] === "string" && ANIM_IDS.test(e[k])) out.add(e[k]);
  return [...out];
};
const RECORD_FIELDS = [
  "name", "description", "battleDescription", "jutsuType", "jutsuRank", "requiredRank", "requiredLevel", "jutsuWeapon",
  "target", "method", "range", "coordinateTargeting", "methodSize", "cooldown", "actionCostPerc", "healthCost", "chakraCost",
  "staminaCost", "healthCostReducePerLvl", "chakraCostReducePerLvl", "staminaCostReducePerLvl", "battleUsageType",
  "elementClassification", "statClassification", "hidden", "extraBaseCost", "image", "effects",
];
const newJutsu = Object.entries<any>(override.jutsu).map(([id, rec]) => {
  const parsed = JutsuValidator.safeParse(rec);
  const copyOf = id.startsWith("dg-") ? null : id;
  return {
    harnessId: id,
    liveRecord: copyOf ? `existing live record ${id} (referenced as-is; already edited by push/316-317)` : null,
    record: Object.fromEntries(RECORD_FIELDS.map((k) => [k, rec[k]])),
    animationPlaceholders: anims(rec),
    image: "placeholder: copied from the shape donor; art pass to replace",
    validator: parsed.success ? "JutsuValidator: ok" : `JutsuValidator: ${parsed.error.issues.map((i) => i.message).join("; ")}`,
  };
});
const capturedName = (id: string) => t.jutsu[id]?.name ?? id;
const ais = Object.entries<any>(override.newEnemies).map(([id, o]) => {
  const e = t.enemies[id]!;
  const row = e.row;
  const rules = e.profile.rules;
  // The Forge's AI insert/update schema: the captured row's own columns (relations dropped), jutsu as ids.
  const RELATIONS = new Set(["jutsus", "items", "aiProfile", "titles", "raidBuffs", "cookingJobs", "village", "bloodline", "sageMode", "anbuSquad", "clan", "loadout", "userSkills", "userQuests", "completedQuests", "bounties", "bountySignups", "queue"]);
  const aiInput = { ...Object.fromEntries(Object.entries(row).filter(([k]) => !RELATIONS.has(k))), jutsus: row.jutsus.map((uj: any) => uj.jutsuId) };
  const check = insertAiSchema.safeParse(aiInput);
  return {
    harnessId: id,
    copyOf: { liveAi: o.base, liveAiId: Object.keys(baseline.enemies).find((k) => baseline.enemies[k].user.username === o.base) },
    username: row.username, level: row.level, rank: row.rank,
    statsMultiplier: row.statsMultiplier, poolsMultiplier: row.poolsMultiplier,
    pools: { maxHealth: row.maxHealth, maxChakra: row.maxChakra, maxStamina: row.maxStamina },
    stats: { offence: row.offence, defence: row.defence, strength: row.strength, intelligence: row.intelligence, willpower: row.willpower, speed: row.speed },
    effects: row.effects,
    jutsu: row.jutsus.map((uj: any) => ({ id: uj.jutsuId, name: capturedName(uj.jutsuId), new: uj.jutsuId.startsWith("dg-") })),
    includeDefaultRules: e.profile.includeDefaultRules,
    rules: rules.map((r: any, i: number) => ({ index: i, note: r.action.description, conditions: r.conditions, action: r.action })),
    signatureRules: (override as any).signatures[id],
    scaleEditedAiNotes: e.notes,
    insertAiSchemaCheck: check.success ? "ok" : check.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).slice(0, 6),
  };
});

const specPath = resolve(opt("spec-out") ?? join(H, "build_spec.json"));
const spec = existsSync(specPath) ? JSON.parse(readFileSync(specPath, "utf8")) : {};
spec._about = "Skyglass Wreck build spec (harness output; not pushed). Per version: AI dungeon copies (stats, pools, level, multipliers, effect rows, jutsu, ordered rules) and the new dungeon-only jutsu (full records, animation placeholder ids from docs/design/SKYGLASS_BOSS_ANIMATIONS.md and SKYGLASS_BOSS_FIGHTS.md). Harness ids (dg-*) are placeholders: the builder mints real ids, and rule jutsuId references must be remapped to them. Generated by harness/skyglass_wreck_sim/engine/build_kits.ts.";
spec.schemas = "validated against the live validators at engine pin c86f43f4 (validators/combat.ts JutsuValidator, validators/ai.ts AiRule, validators/coordinateTargeting.ts via JutsuValidator)";
spec[version] = { params, floors: (override as any).floors, ais, newJutsu };
writeFileSync(specPath, `${JSON.stringify(spec, null, 1)}\n`);
console.log(`wrote ${specPath} [${version}]: ${ais.length} AIs, ${newJutsu.length} jutsu records`);
for (const a of ais) console.log(`  ${a.username.padEnd(18)} L${a.level} HP ${a.pools.maxHealth} rules ${a.rules.length} jutsu ${a.jutsu.length} insertAi ${JSON.stringify(a.insertAiSchemaCheck).slice(0, 80)}`);
for (const j of newJutsu) if (!j.validator.endsWith("ok")) console.log(`  ! ${j.record.name}: ${j.validator}`);
