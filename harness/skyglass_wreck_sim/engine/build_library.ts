/**
 * Write the shared set-piece library to library_spec.json (all records NEW, full fields).
 *   TNR_SCRIPT=build_library.ts run.sh [--out library_spec.json]
 */
import { writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { JutsuValidator } from "@/validators/combat";
import { ANSWERS, buildLibrary, LIB, LIB_POWERS, LIVE_COPY_SOURCE, MARKER_TYPES, PATTERNS } from "./library";

const args = process.argv.slice(2);
const out = resolve(args.includes("--out") ? args[args.indexOf("--out") + 1]! : join(process.env.TNR_HARNESS!, "library_spec.json"));
const J = buildLibrary();
const FIELDS = [
  "name", "description", "battleDescription", "jutsuType", "jutsuRank", "requiredRank", "requiredLevel", "jutsuWeapon",
  "target", "method", "range", "coordinateTargeting", "methodSize", "cooldown", "actionCostPerc", "healthCost", "chakraCost",
  "staminaCost", "healthCostReducePerLvl", "chakraCostReducePerLvl", "staminaCostReducePerLvl", "battleUsageType",
  "elementClassification", "statClassification", "hidden", "extraBaseCost", "image", "effects",
];
const ANIM = /^(tg|dt|ch|cp|cc|fw|lg)_[a-z_]+$|^(mark-sigil|chain-hook-hit|skyglass-pane)$/;
const group = (id: string) =>
  Object.values(LIB.mark).includes(id) ? "mark" : Object.values(LIB.blast).includes(id) ? "shared blast" : Object.values(LIB.sig).includes(id) ? "signature" : id === LIB.loweredGuard ? "lowered guard" : Object.values(LIB.liveCopy).includes(id) ? "Skyglass-only copy of a live jutsu" : "crew addition";
const markOf = Object.fromEntries(Object.entries(LIB.mark).map(([k, id]) => [id, k]));
const records = Object.entries<any>(J).map(([id, rec]) => {
  const v = JutsuValidator.safeParse(rec);
  const anims = new Set<string>();
  for (const e of rec.effects) for (const k of ["appearAnimation", "staticAnimation"]) if (ANIM.test(e[k] ?? "")) anims.add(e[k]);
  return {
    id, status: "NEW", group: group(id),
    ...(markOf[id] ? { primedMarker: { type: MARKER_TYPES[markOf[id] as keyof typeof MARKER_TYPES], rounds: 1, rule: `has_effect ${MARKER_TYPES[markOf[id] as keyof typeof MARKER_TYPES]} >= 1` } } : {}),
    ...(ANSWERS[id] ? { answersMark: LIB.mark[ANSWERS[id]!], fireRule: `use_specific_jutsu ${id} target SELF when has_effect ${MARKER_TYPES[ANSWERS[id]!]} >= 1` } : {}),
    ...(LIVE_COPY_SOURCE[id] ? { copyOf: LIVE_COPY_SOURCE[id] } : {}),
    record: Object.fromEntries(FIELDS.map((k) => [k, rec[k]])),
    animationPlaceholders: [...anims],
    validator: v.success ? "JutsuValidator: ok" : v.error.issues.map((i) => i.message).join("; "),
  };
});
const spec = {
  _about: "Skyglass set-piece library (docs/design/SKYGLASS_BOSS_FIGHTS.md 5a). Every record is NEW; lib-* ids are placeholders the builder replaces, and every rule referencing them must be remapped. Built by harness/skyglass_wreck_sim/engine/library.ts on captured shape donors; each record passes the live JutsuValidator (engine pin c86f43f4). Images are placeholders from the shape donors.",
  recipe: [
    "A set piece is a mark then a blast. Mark: 40 AP, GROUND, lays a 1-round visual on its pattern and a 1-round primed marker on the caster. Blast: 100 AP, cast with rule target SELF on the caster's next turn by a rule `has_effect <marker type> >= 1` placed above the boss's other rules.",
    "Each mark has its own marker type, so different marks never satisfy each other's blast rule and any two can coexist on one boss. Marker types are outside SHARED_COOLDOWN_TAGS, so a mark never locks another mark.",
    "A boss must not lay two marks in one turn (40 + 40 AP fits, but only one blast can follow): after its mark rules, give it rules `has_effect <its marker> -> plain attack` and `-> end turn` ahead of the other marks.",
    "The 60 AP left after a mark can carry a 60 AP follow-up such as a live pull (the two-marker chain).",
    "Once marked, every blast goes off, even if everyone stepped off. Pure-damage blasts (Ring, Rows, Scatter, Lines, Crownfall, Broadside, Splash, Short Line) are GROUND: ground damage resolves as an instant hit on occupants (enemies only), so they erupt on empty tiles too. Note: GROUND damage also strikes any barrier standing on an empty marked tile, including the caster's own. Blasts with stun, lock or push rows (Seal Lines, Ship's Bell, Maw of the Deep, Quench, Command Absolute) stay CHARACTER, because GROUND lands only damage. A CHARACTER cast is valid only with a character on its pattern, so Seal Lines and Ship's Bell include the caster's own hex, and the Last Light signatures cover the whole field but the stars. Scatter blasts also leave a 2-round pool (ground damage + tg_linger).",
    "Minor marks (Splash, Short Line) are caster-anchored. A target-anchored pattern cannot hold its tiles: the blast is a new cast on the next turn, and the AI aims it at the target's current hex.",
    "Caster-relative patterns (Ring, Binding Ring, Lines, Seal Lines) need the boss to stay where it marked; marks and blasts cost all its AP across two turns, so it does.",
  ],
  markerTypes: MARKER_TYPES,
  patterns: { ...PATTERNS, ring: "AOE_SPIRAL_SHOOT range 2 around the caster (disc minus the caster)" },
  powers: LIB_POWERS,
  counts: { marks: Object.keys(LIB.mark).length, sharedBlasts: Object.keys(LIB.blast).length, signatures: Object.keys(LIB.sig).length, loweredGuard: 1, crewAdditions: Object.keys(LIB.crew).length, liveCopies: Object.keys(LIB.liveCopy).length, total: records.length },
  records,
};
writeFileSync(out, `${JSON.stringify(spec, null, 1)}\n`);
console.log(`wrote ${out}: ${records.length} NEW records; validator ok: ${records.filter((r) => r.validator.endsWith("ok")).length}`);
