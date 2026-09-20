// Presentation lint (plan §4.5).
//
// The dossier already refuses to invent facts and the spec already refuses to restate them. Lint
// is the layer that catches the ways a presentation can still be wrong while every individual
// piece is well-formed: a roster that claims to be complete and is not, a named character shown
// with pixels that are not its own, a scene asset promoted to a place, a summary whose dialogue
// moved under it.
//
// Every rule below traces to a real Godstorm delivery failure or to a reproduced bypass from the
// independent review. None of them is a style opinion.
//
// FATAL stops an export. WARN is reported and does not - and the split is deliberate: a warning is
// for something a human should look at (art that is current but not yet held as bytes, evidence
// from runs weeks apart), a fatal is for a presentation that would state something untrue OR for a
// claim nothing verified. "Unverified" sits with the fatals on purpose (review F1): a note that a
// binding could not be checked is not a check.

import { FATAL, WARN, finding } from "./errors.mjs";
import { STATUS, PRESENTABLE } from "./assets.mjs";

/**
 * @param {object} dossier
 * @param {object} spec       the parsed spec the dossier was built with
 * @param {object} [options]
 * @param {boolean} [options.requireExactBytes]  true when the caller intends a deterministic
 *   offline render, which only verified bytes support. P1 has no renderer, so the default is false
 *   and current-but-unheld art is a warning naming what P2 must do about it.
 * @returns {{findings: object[], fatal: object[], warnings: object[], ok: boolean}}
 */
export function lintPresentation(dossier, spec, { requireExactBytes = false } = {}) {
  const out = [];

  // ---- evidence ------------------------------------------------------------------------------
  if (!dossier.sources.records.length) out.push(finding(FATAL, "no-evidence", "the dossier binds no evidence records"));
  for (const p of dossier.problems) out.push(finding(FATAL, "extraction", p));
  for (const w of dossier.warnings) out.push(finding(WARN, "evidence", w));

  if (dossier.sources.draft) {
    out.push(finding(FATAL, "draft-evidence", "this dossier was built from a DRAFT evidence package: its sources are working-tree bytes with no commit behind them, so nothing it states is reproducible from the repository"));
  } else if (!dossier.sources.repoCommit) {
    out.push(finding(FATAL, "no-source-lock", "the dossier carries no source commit"));
  }

  const dates = dossier.sources.records.map((r) => r.capturedAt || r.bundleAt).filter(Boolean).sort();
  if (dates.length > 1) {
    const span = (new Date(dates[dates.length - 1]) - new Date(dates[0])) / 86400000;
    if (Number.isFinite(span) && span > 3) {
      out.push(finding(WARN, "evidence-spread", `selected evidence spans ${span.toFixed(1)} days (${dates[0]} to ${dates[dates.length - 1]}); confirm the older records are still current for what they supply`));
    }
  }

  // ---- structure -------------------------------------------------------------------------------
  for (const s of Object.values(dossier.structure)) {
    if (s.danglingLinks.length) {
      out.push(finding(WARN, "dangling-link", `${s.name}: ${s.danglingLinks.length} objective link(s) point at an id the record does not contain (${s.danglingLinks.slice(0, 3).join(", ")})`));
    }
    if (s.cycles.length) {
      out.push(finding(WARN, "objective-cycle", `${s.name}: the objective graph loops through ${s.cycles.join(", ")} once failure links are followed; the pinned flow validator rejects a cycle, so this record is malformed even though the route to completion is still well defined`));
    }
    if (s.orphanStarts.length) {
      out.push(finding(WARN, "orphan-objectives", `${s.name}: ${s.orphanStarts.length} objective(s) nothing points at and nothing reaches (${s.orphanStarts.join(", ")}); they are detached remnants, not part of this quest`));
    }
    if (!s.successPathLinear) {
      out.push(finding(WARN, "branching-route", `${s.name}: the route to completion branches at ${s.successPathBranchAt}, so it cannot be presented as one sequence`));
    }
    if (typeof s.hidden !== "boolean") {
      out.push(finding(FATAL, "unknown-publication-state", `${s.name}: the capture does not say whether it is hidden, so publication state is unknown and must not be presented either way`));
    }
  }

  // ---- roles and cadence ---------------------------------------------------------------------
  for (const e of dossier.roster.filter((x) => !x.role)) {
    out.push(finding(FATAL, "unannotated-role", `ai ${e.aiId} (${e.name ?? "unnamed"}) fights in ${e.appearances} battle(s) but the spec gives it no role, so it cannot be placed in an encounter cadence or a roster group`));
  }
  for (const e of dossier.encounters) {
    if (!e.cadence.exact) {
      out.push(finding(WARN, "no-cadence", `${e.name}: the ${e.battles} battles do not tile into a repeating unit, so the presentation must show the sequence rather than a cadence`));
    }
  }

  // ---- roster completeness -------------------------------------------------------------------
  if (spec.roster.coverage === "all") {
    for (const e of dossier.roster.filter((x) => !x.resolved)) {
      out.push(finding(FATAL, "roster-incomplete", `roster coverage is "all" but ai ${e.aiId} cannot be named from any admissible capture; a complete roster cannot be shown from this evidence`));
    }
    if (Array.isArray(spec.roster.entries) && spec.roster.entries.length) {
      const listed = new Set(spec.roster.entries);
      for (const e of dossier.roster) {
        if (!listed.has(e.aiId)) {
          out.push(finding(FATAL, "roster-omission", `roster coverage is "all" but the spec's entry list omits ai ${e.aiId} (${e.name ?? "unnamed"}), which fights in ${e.appearances} battle(s)`));
        }
      }
      for (const id of listed) {
        if (!dossier.roster.some((e) => e.aiId === id)) {
          out.push(finding(FATAL, "roster-stranger", `the spec's roster lists ai ${id}, which fights in no reachable battle of this subject`));
        }
      }
    }
  }

  // ---- rewards ---------------------------------------------------------------------------------
  for (const [questId, r] of Object.entries(dossier.rewards)) {
    const name = dossier.structure[questId]?.name ?? questId;
    if (r.fullClearAmbiguous) {
      out.push(finding(FATAL, "ambiguous-full-clear", `${name}: the route to completion branches, so there is no single full-clear reward to state; present the alternatives or nothing`));
    } else if (!r.fullClear) {
      out.push(finding(FATAL, "no-current-reward", `${name}: no reward sits on the path from the entry to a win, so a current-rewards section would have nothing to show`));
    }
    for (const node of r.intermediateCashOuts) {
      out.push(finding(WARN, "intermediate-cash-out", `${name}: objective ${node.objectiveId} pays out on the way to the clear; a "full clear reward" section must not fold it in`));
    }
    for (const node of r.optionalRewardNodes) {
      out.push(finding(WARN, "optional-reward", `${name}: objective ${node.objectiveId} pays a reward but cannot reach a win; it is an optional or exit payout and is not part of the full clear`));
    }
    for (const node of r.failurePathRewardNodes) {
      out.push(finding(WARN, "failure-reward", `${name}: objective ${node.objectiveId} pays a reward on the failure path; it must not be presented as a clear reward`));
    }
    for (const id of r.unreachableRewardNodes) {
      out.push(finding(WARN, "unreachable-reward", `${name}: objective ${id} still carries a reward but nothing reaches it; it is historical and must not be presented as current`));
    }
  }

  // ---- assets ----------------------------------------------------------------------------------
  for (const a of dossier.assets.entries) {
    const who = a.name ?? a.entity;
    if (a.status === STATUS.MISSING) {
      out.push(finding(FATAL, "asset-missing", `${who}: no exact or approved art resolves for this named entity${a.notes.length ? ` (${a.notes[0]})` : ""}`));
      continue;
    }
    if (a.status === STATUS.MISMATCH) {
      out.push(finding(FATAL, "asset-mismatch", `${who}: ${a.notes.join("; ")}`));
      continue;
    }
    if (a.status === STATUS.HISTORICAL) {
      out.push(finding(FATAL, "asset-historical", `${who}: ${a.notes.join("; ")}. Exact-current art is required for a named entity tile`));
      continue;
    }
    // F1: a binding whose bytes could not be verified must never pass as exact art. A status is
    // consumed by readiness counts and by the renderer, so "unverified" cannot live in a note.
    if (a.bytes.bound && !a.bytes.verified) {
      out.push(finding(FATAL, "asset-unverified", `${who}: the spec binds ${a.bytes.path}, but ${a.bytes.reason}. Unverified bytes are not exact art`));
      continue;
    }
    if (!PRESENTABLE.includes(a.status)) {
      out.push(finding(FATAL, "asset-not-presentable", `${who}: art status ${a.status} cannot back a factual tile`));
      continue;
    }
    if (requireExactBytes && !a.renderable) {
      out.push(finding(FATAL, "asset-not-materialised", `${who}: art is ${a.status} with no verified bytes; a deterministic render needs them, so it must be materialised into the content-addressed cache and hashed first`));
      continue;
    }
    if (!a.bytes.bound) {
      out.push(finding(WARN, "asset-remote", `${who}: current art is a remote URL with no repository bytes bound; a renderer must resolve it from a committed source archive or materialise and hash it before it can claim a deterministic build`));
    }
  }

  // ---- locations -------------------------------------------------------------------------------
  const locationKeys = new Set(dossier.locations.map((l) => l.key));
  const sceneKeys = new Map(dossier.sceneAssets.map((a) => [a.key, a]));
  const byName = new Map(dossier.locations.map((l) => [l.name, l]));
  for (const loc of spec.locations) {
    if (locationKeys.has(loc) || byName.has(loc)) continue;
    const scene = sceneKeys.get(loc) || sceneKeys.get(`asset:${loc}`);
    if (scene) {
      out.push(finding(FATAL, "scene-as-location", `spec.locations names ${JSON.stringify(loc)}, which is a ${scene.kind} used by ${scene.usedBy.length} objective(s) of ${scene.component}. A background is artwork, not a place; set sceneDetail to caption scene art instead`));
      continue;
    }
    out.push(finding(FATAL, "unknown-location", `spec.locations names ${JSON.stringify(loc)}, which is neither a component of this subject nor a scene asset it uses`));
  }

  if (spec.sceneDetail) {
    const registered = new Set(dossier.assets.entries.map((a) => a.entity));
    for (const a of dossier.sceneAssets) {
      if (!registered.has(a.key)) {
        out.push(finding(FATAL, "scene-art-unresolved", `sceneDetail is on, but ${a.key} (${a.kind} of ${a.component}) has no selected record describing its current image, so it cannot be captioned with exact art`));
      }
    }
  }

  // ---- narrative --------------------------------------------------------------------------------
  const anchored = new Set(dossier.narrative.map((b) => b.component));
  for (const s of Object.values(dossier.structure)) {
    if (!anchored.has(s.questId)) out.push(finding(WARN, "no-narrative", `${s.name}: no story block is anchored to this component`));
  }

  // ---- publication state --------------------------------------------------------------------
  for (const s of Object.values(dossier.structure)) {
    if (s.hidden === true) {
      out.push(finding(WARN, "hidden-subject", `${s.name} is hidden/unpublished in the current capture; that is provenance, and a player-facing artifact must not imply it is live`));
    }
  }

  const fatal = out.filter((f) => f.severity === FATAL);
  return { findings: out, fatal, warnings: out.filter((f) => f.severity === WARN), ok: fatal.length === 0 };
}

export { FATAL, WARN };
