// Runtime-equivalent Forge gate for push/93 (offline; never opens a socket).
//
// Same method as push/90_ghost_ship_skyglass_release.check.mjs. Each edit is validated against
// the live row Forge's _fill would read, which here is the push/90 after-capture
// (harvests/inbox/tnr_results_1791779642866.json): the half-applied Sentinel row and both quests
// as push/90 left them. It also replays mergeForUpdate for the AI edit (law 70 kit re-send, law 69 items).
//
//   node push/93_ghost_ship_guardian_repair.check.mjs [manifest]

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { parseManifest, planOrder } from "../forge/src/runner/manifest.mjs";
import { Validator } from "../forge/src/runner/validate.mjs";
import { mergeForUpdate } from "../forge/src/runner/recipes.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const rd = (rel) => JSON.parse(readFileSync(join(ROOT, rel), "utf8"));
const manifestPath = process.argv[2] ?? "push/93_ghost_ship_guardian_repair.json";
const after = (rd("harvests/inbox/tnr_results_1791779642866.json").captures ?? []).filter((c) => c.phase === "after" && c.data);
const ais = new Map(after.filter((c) => c.proc === "profile.getAi").map((c) => [c.data.userId, c.data]));
const quests = new Map(after.filter((c) => c.proc === "quests.get").map((c) => [c.data.id, c.data]));

let manifest;
try {
  manifest = parseManifest(rd(manifestPath));
} catch (e) {
  console.error(`REFUSED by Forge ${e.name}: ${e.message}`);
  process.exit(1);
}
const order = planOrder(manifest);
const v = new Validator(rd("forge/src/runner/fields.json"), rd("forge/src/runner/nested.json"));
const problems = [];
for (const it of order) {
  const live = it.entity === "ai" ? ais.get(it.targetId) : it.entity === "quest" ? quests.get(it.targetId) : null;
  if (it.op !== "update" || !live) { problems.push(`item ${it.idx} (${it.name}): expected an edit with a captured live row`); continue; }
  for (const p of v.problems(it.entity, it.data, live, { preCreate: false })) problems.push(`item ${it.idx} (${it.name}): ${p}`);
  if (it.entity === "ai") {
    const payload = mergeForUpdate("ai", live, it.data, null);
    if (!Array.isArray(payload.jutsus)) problems.push(`item ${it.idx}: merged AI payload has no jutsus (law 70)`);
    if (!Array.isArray(payload.items) || payload.items.some((t) => !Array.isArray(t.ids) || typeof t.number !== "number")) problems.push(`item ${it.idx}: merged AI items are not {ids, number} (law 69)`);
    if (payload.username !== "Guardian") problems.push(`item ${it.idx}: merged username ${payload.username}`);
  }
}
if (/"@(ai|item|scene|img):/.test(JSON.stringify(manifest.items))) problems.push("unresolved @ref left in a manifest with no creates or uploads");
for (const w of manifest.warnings) console.log("warn   " + w);
for (const p of problems) console.error("ERROR  " + p);
console.log(`${manifestPath}: ${order.length} planned item(s), Forge manifest hash ${manifest.hash}`);
console.log(`\n${problems.length} runtime-equivalent pre-send problem(s)`);
process.exit(problems.length ? 1 : 0);
