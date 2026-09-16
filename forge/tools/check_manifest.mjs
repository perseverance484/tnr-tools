// Offline Forge compatibility gate for a committed manifest.
//
// A repository manifest is handed off long before anyone selects it in Forge, and the only
// thing that decides whether Forge will open a job for it is Forge's own parser. push/47
// reached a frozen, independently reviewed handoff carrying two standalone `aiProfile` create
// items: green under the repository's Python validator, and refused by Forge 0.4.1 at parse
// time with "aiProfile cannot be created directly; create an ai with rules". This tool runs
// the real thing - parseManifest, planOrder and the pinned pre-send Validator - against a file
// on disk, so that answer is available from the container instead of from a live selection.
//
// It NEVER opens a socket, mints an id or sends anything: parse, plan and validate are pure.
//
// CLI:
//   node tools/check_manifest.mjs ../push/47_one_perfect_crop_core_manifest.json
// exits 0 when the manifest is Forge-runnable, 1 with the problems on stderr otherwise.

import { readFileSync } from "node:fs";
import { basename } from "node:path";
import { parseManifest, planOrder } from "../src/runner/manifest.mjs";
import { Validator } from "../src/runner/validate.mjs";

const FIELDS = JSON.parse(readFileSync(new URL("../src/runner/fields.json", import.meta.url), "utf8"));
const NESTED = JSON.parse(readFileSync(new URL("../src/runner/nested.json", import.meta.url), "utf8"));

/**
 * Parse, plan and pre-send-validate one manifest exactly as the runner would.
 *
 * @param {string} path  manifest file to check
 * @returns {{path: string, hash: string, plan: Array, problems: string[], warnings: string[]}}
 *   `plan` is one entry per planned item: {idx, entity, op, srcId, targetId, name, phase},
 *   where `phase` is the runner's post-fill route for that item - "rules" for an ai create
 *   carrying data.rules (runner.mjs _fill -> _rules -> ai.updateAiProfile), else "verify".
 * @throws {ManifestError} when Forge would refuse the manifest before a job exists
 */
export function checkManifest(path) {
  const manifest = parseManifest(readFileSync(path, "utf8"));
  const order = planOrder(manifest);
  const v = new Validator(FIELDS, NESTED);
  const problems = [];
  for (const it of order) {
    for (const p of v.problems(it.entity, it.data, null, { preCreate: it.op === "create" })) {
      problems.push(`item ${it.idx} (${it.name}): ${p}`);
    }
  }
  return {
    path: basename(path),
    hash: manifest.hash,
    warnings: manifest.warnings,
    problems,
    plan: order.map((it) => ({
      idx: it.idx, entity: it.entity, op: it.op, name: it.name,
      srcId: it.srcId, targetId: it.targetId,
      // recipes.mjs AI_OMIT keeps rules/includeDefaultRules out of profile.updateAi; the
      // runner routes them to its rules phase instead. This mirrors runner.mjs _fill.
      phase: it.entity === "ai" && Array.isArray(it.data.rules) ? "rules" : "verify",
    })),
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const path = process.argv[2];
  if (!path) { console.error("usage: node tools/check_manifest.mjs <manifest.json>"); process.exit(2); }
  let report;
  try {
    report = checkManifest(path);
  } catch (e) {
    console.error(`REFUSED by Forge ${e.name}: ${e.message}`);
    process.exit(1);
  }
  for (const w of report.warnings) console.log("warn   " + w);
  for (const p of report.problems) console.error("ERROR  " + p);
  console.log(`${report.path}: ${report.plan.length} planned item(s), manifest hash ${report.hash}`);
  for (const it of report.plan) {
    console.log(`  ${it.idx}. ${it.entity} ${it.op} ${it.srcId ?? it.targetId ?? ""} -> ${it.phase} phase`);
  }
  console.log(`\n${report.problems.length} pre-send problem(s)`);
  process.exit(report.problems.length ? 1 : 0);
}
