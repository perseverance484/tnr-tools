// Runtime-equivalent Forge gate for push/90 (offline; never opens a socket).
//
// forge/tools/check_manifest.mjs validates every item with live = null, which is exact for a
// create (the runner's pre-create check) but not for an edit: at run time Forge's _fill validates
// an edit against the live row it has just read, so a post-0056 column such as `offence` is a
// known key there and an unknown one offline. This gate runs the same parseManifest / planOrder /
// Validator, and for each edit supplies the committed capture of that record as the live row:
//
//   ai edit      push/86 profile.getAi row (the Sealwright follow-up uses the regular Captain's
//                row as the shape proxy for the freshly created Sealwright row)
//   jutsu edit   the push/86 kit row of that jutsu
//   item edit    the October 1 item.get row when captured, else null (pinned field set only)
//   quest edit   the quest base the manifest was generated from
//   asset edit   null (no capture; gameAsset keys are all in the pinned set)
//
// It also replays mergeForUpdate for every AI edit against its push/86 row and asserts the
// payload re-sends a kit (law 70) and carries `items` as {ids, number}.
//
//   node push/90_ghost_ship_skyglass_release.check.mjs [--art-probe] [manifest] [quest-base]
//
// --art-probe adds dummy imgSizes IN MEMORY for unbound @img names so a draft can get past lint
// L17 and reach the pre-send validator. It never writes, and its result is labelled as a probe.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { parseManifest, planOrder } from "../forge/src/runner/manifest.mjs";
import { Validator } from "../forge/src/runner/validate.mjs";
import { mergeForUpdate } from "../forge/src/runner/recipes.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const rd = (rel) => JSON.parse(readFileSync(join(ROOT, rel), "utf8"));
const args = process.argv.slice(2);
const probe = args.includes("--art-probe");
const pos = args.filter((a) => !a.startsWith("--"));
const manifestPath = pos[0] ?? "push/90_ghost_ship_skyglass_release.json";
const report = rd("state/ghost_ship_skyglass_release_manifest_report.json");
const questBase = pos[1] ?? report.quests.base;

const FIELDS = rd("forge/src/runner/fields.json");
const NESTED = rd("forge/src/runner/nested.json");
const caps = (rel, proc) => (rd(rel).captures ?? []).filter((c) => c.proc === proc && c.data).map((c) => c.data);

const ais = new Map(caps("harvests/inbox/tnr_results_1791727613862.json", "profile.getAi").map((d) => [d.userId, d]));
const jutsus = new Map();
for (const a of ais.values()) for (const uj of a.jutsus) if (!jutsus.has(uj.jutsuId)) jutsus.set(uj.jutsuId, uj.jutsu);
const items = new Map(caps("harvests/inbox/tnr_results_1790826836406.json", "item.get").map((d) => [d.id, d]));
const quests = new Map(caps(questBase, "quests.get").map((d) => [d.id, d]));
const CAPTAIN = "QY69h271Nx9uHrBeR6jwW";

const raw = JSON.parse(readFileSync(join(ROOT, manifestPath), "utf8"));
if (probe) {
  const names = [...new Set([...JSON.stringify(raw.items).matchAll(/@img:([A-Za-z0-9_.\-]+)/g)].map((m) => m[1]))];
  raw.imgSizes = { ...(raw.imgSizes ?? {}) };
  for (const n of names) if (!(n in raw.imgSizes)) raw.imgSizes[n] = 1000;
}

let manifest;
try {
  manifest = parseManifest(raw);
} catch (e) {
  console.error(`REFUSED by Forge ${e.name}: ${e.message}`);
  process.exit(1);
}
const order = planOrder(manifest);
const v = new Validator(FIELDS, NESTED);
const problems = [];
const liveFor = (it) => {
  if (it.op === "create") return null;
  const t = it.targetId;
  if (it.entity === "ai") return ais.get(t) ?? (t === "@ai:sealwright" ? ais.get(CAPTAIN) : null);
  if (it.entity === "jutsu") return jutsus.get(t) ?? null;
  if (it.entity === "item") return items.get(t) ?? null;
  if (it.entity === "quest") return quests.get(t) ?? null;
  return null;
};
for (const it of order) {
  const live = liveFor(it);
  if (it.op === "update" && ["ai", "jutsu", "quest"].includes(it.entity) && !live) problems.push(`item ${it.idx} (${it.name}): no captured live row to validate against`);
  for (const p of v.problems(it.entity, it.data, live, { preCreate: it.op === "create" })) problems.push(`item ${it.idx} (${it.name}): ${p}`);
  if (it.entity === "ai" && it.op === "update" && live) {
    const payload = mergeForUpdate("ai", live, it.data, null);
    if (!Array.isArray(payload.jutsus)) problems.push(`item ${it.idx}: merged AI payload has no jutsus (law 70)`);
    if (!Array.isArray(payload.items) || payload.items.some((t) => !Array.isArray(t.ids) || typeof t.number !== "number")) problems.push(`item ${it.idx}: merged AI items are not {ids, number} (law 69)`);
  }
}
for (const w of manifest.warnings) console.log("warn   " + w);
for (const p of problems) console.error("ERROR  " + p);
console.log(`${manifestPath}: ${order.length} planned item(s), Forge manifest hash ${manifest.hash}${probe ? " [ART PROBE: dummy imgSizes in memory, not runnable]" : ""}`);
const phases = {};
for (const it of order) phases[it.phase ?? 5] = (phases[it.phase ?? 5] ?? 0) + 1;
console.log("planned phases " + JSON.stringify(phases));
console.log(`\n${problems.length} runtime-equivalent pre-send problem(s)`);
process.exit(problems.length ? 1 : 0);
