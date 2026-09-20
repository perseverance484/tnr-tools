// One entry point: spec file in, dossier plus lint out.
//
// Kept separate from dossier.mjs so the library stays free of filesystem assumptions - the
// extractors take parsed records, and only this file and evidence.mjs know where a repository is.

import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { parseSpec } from "./spec.mjs";
import { parseEvidence, loadEvidence } from "./evidence.mjs";
import { buildDossier } from "./dossier.mjs";
import { lintPresentation } from "./lint.mjs";
import { cadenceText } from "./structure.mjs";
import { PresentationError } from "./errors.mjs";
import { gitBlobReader } from "./gitblob.mjs";

const readJson = (path, what) => {
  let text;
  try {
    text = readFileSync(path, "utf8");
  } catch (e) {
    throw new PresentationError(`${what} could not be read at ${path} (${(e && e.code) || e})`);
  }
  try {
    return JSON.parse(text);
  } catch (e) {
    throw new PresentationError(`${what} at ${path} is not JSON (${(e && e.message) || e})`);
  }
};

/**
 * Build a dossier and lint it from a spec file on disk.
 *
 * @param {string} specPath  absolute path to a presentation spec
 * @param {object} o
 * @param {string} o.root    repository root; every evidence path resolves under it
 * @param {string} [o.gitRoot]  where the commit a pack names can be read from; defaults to root,
 *   and differs only when a fixture presents a working tree outside the repository
 * @param {boolean} [o.requireExactBytes]
 * @param {function} [o.blobAtRef]  override the git-backed blob reader (fixtures)
 */
export function buildFromSpecFile(specPath, { root, gitRoot = root, requireExactBytes = false, blobAtRef } = {}) {
  const spec = parseSpec(readJson(specPath, "presentation spec"));
  // The spec names its evidence package relative to itself: the two travel together, and a spec
  // that could point at an arbitrary repository path would be a way to smuggle a source in.
  const evidencePath = join(dirname(specPath), spec.evidence);
  const pkg = parseEvidence(readJson(evidencePath, "evidence package"));
  const loaded = loadEvidence(pkg, { root });
  const dossier = buildDossier(loaded, spec, { root, blobAtRef: blobAtRef ?? gitBlobReader(gitRoot) });
  const lint = lintPresentation(dossier, spec, { requireExactBytes });
  return { spec, dossier, lint };
}

/** A compact human summary of a built dossier - what a handoff or a CLI run should print. */
export function summarize(dossier) {
  const lines = [];
  lines.push(`${dossier.subject.title} (${dossier.subject.type}) - dossier ${dossier.hash.slice(0, 12)}`);
  lines.push(`  components: ${dossier.subject.components.join(", ")}`);
  for (const e of dossier.encounters) {
    lines.push(`  ${e.name}: ${e.battles} battles, ${e.keepers} keepers - ${cadenceText(e.cadence)}`);
  }
  lines.push(`  totals: ${dossier.totals.battles} battles, ${dossier.totals.keepers} keepers, ${dossier.totals.distinctAi} distinct AI`);
  for (const [questId, r] of Object.entries(dossier.rewards)) {
    const name = dossier.structure[questId].name;
    const fc = r.fullClear ? Object.entries(r.fullClear.reward).map(([k, v]) => `${v} ${k}`).join(" / ") : "none";
    lines.push(`  ${name} full clear (${r.fullClear ? r.fullClear.objectiveId : "-"}): ${fc}; ${r.intermediateCashOuts.length} intermediate cash-out(s), ${r.rewardItems.length} reward item(s)`);
  }
  const c = dossier.assets.coverage;
  lines.push(`  art: ${c.exactBytes} exact-with-bytes, ${c.exactRemote} exact-remote, ${c.historical} historical, ${c.missing} missing, ${c.mismatch} mismatched, of ${c.total}`);
  lines.push(`  locations: ${dossier.locations.map((l) => l.name).join(", ")} (${dossier.sceneAssets.length} scene asset(s), not locations)`);
  for (const b of dossier.narrative) lines.push(`  narrative ${b.key}: ${b.sourceObjectives.length} anchor(s) in ${b.component}`);
  return lines.join("\n");
}
