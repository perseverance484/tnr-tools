// Presentation lint (plan §4.5).
//
// The dossier already refuses to invent facts and the spec already refuses to restate them. Lint
// is the layer that catches the ways a presentation can still be wrong while every individual
// piece is well-formed: a roster that claims to be complete and is not, a named character shown
// with pixels that are not its own, a scene asset promoted to a place, a summary anchored to an
// objective that no longer exists.
//
// Every rule below traces to a real Godstorm delivery failure. None of them is a style opinion.
//
// FATAL stops an export. WARN is reported and does not - and the split is deliberate: a warning is
// for something a human should look at (art that is current but not yet materialised, evidence
// from runs weeks apart), a fatal is for a presentation that would state something untrue.

import { FATAL, WARN, finding } from "./errors.mjs";
import { STATUS, RENDERABLE, CURRENT } from "./assets.mjs";

/**
 * @param {object} dossier
 * @param {object} spec       the parsed spec the dossier was built with
 * @param {object} [options]
 * @param {boolean} [options.requireExactBytes]  true when the caller intends a deterministic
 *   offline render, which only `exact-current-bytes` supports. P1 has no renderer, so the default
 *   is false and remote-but-current art is a warning naming what P2 must do about it.
 * @returns {{findings: object[], fatal: object[], warnings: object[], ok: boolean}}
 */
export function lintPresentation(dossier, spec, { requireExactBytes = false } = {}) {
  const out = [];

  // ---- evidence ------------------------------------------------------------------------------
  if (!dossier.sources.records.length) out.push(finding(FATAL, "no-evidence", "the dossier binds no evidence records"));
  for (const p of dossier.problems) out.push(finding(FATAL, "extraction", p));
  for (const w of dossier.warnings) out.push(finding(WARN, "evidence", w));

  const dates = dossier.sources.records.map((r) => r.capturedAt || r.bundleAt).filter(Boolean).sort();
  if (dates.length > 1) {
    const span = (new Date(dates[dates.length - 1]) - new Date(dates[0])) / 86400000;
    if (Number.isFinite(span) && span > 3) {
      out.push(finding(WARN, "evidence-spread", `selected evidence spans ${span.toFixed(1)} days (${dates[0]} to ${dates[dates.length - 1]}); confirm the older records are still current for what they supply`));
    }
  }

  // ---- roles and cadence ---------------------------------------------------------------------
  const unannotated = dossier.roster.filter((e) => !e.role);
  for (const e of unannotated) {
    out.push(finding(FATAL, "unannotated-role", `ai ${e.aiId} (${e.name ?? "unnamed"}) fights in ${e.appearances} battle(s) but the spec gives it no role, so it cannot be placed in an encounter cadence or a roster group`));
  }
  for (const e of dossier.encounters) {
    if (!e.cadence.exact) {
      out.push(finding(WARN, "no-cadence", `${e.name}: the ${e.battles} battles do not tile into a repeating unit, so the presentation must show the sequence rather than a cadence`));
    }
  }

  // ---- roster completeness -------------------------------------------------------------------
  if (spec.roster.coverage === "all") {
    const unresolved = dossier.roster.filter((e) => !e.resolved);
    for (const e of unresolved) {
      out.push(finding(FATAL, "roster-incomplete", `roster coverage is "all" but ai ${e.aiId} cannot be named from any selected record; a complete roster cannot be shown from this evidence`));
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
    if (!r.fullClear) {
      out.push(finding(FATAL, "no-current-reward", `${name}: no reachable objective grants a reward, so a rewards section would have nothing current to show`));
    }
    for (const node of r.intermediateCashOuts) {
      out.push(finding(WARN, "intermediate-cash-out", `${name}: objective ${node.objectiveId} is a reachable intermediate reward; a "full clear reward" section must not fold it in`));
    }
    for (const node of r.nodes.filter((n) => !n.reachable)) {
      out.push(finding(WARN, "unreachable-reward", `${name}: objective ${node.objectiveId} still carries a reward but nothing reaches it; it is historical and must not be presented as current`));
    }
  }

  // ---- assets ----------------------------------------------------------------------------------
  const byEntity = new Map(dossier.assets.entries.map((e) => [e.entity, e]));
  for (const e of dossier.roster) {
    const asset = byEntity.get(`ai:${e.aiId}`);
    if (!asset || asset.status === STATUS.MISSING) {
      out.push(finding(FATAL, "asset-missing", `${e.name ?? e.aiId}: no exact or approved art resolves for this named entity${asset && asset.notes.length ? ` (${asset.notes[0]})` : ""}`));
      continue;
    }
    if (asset.status === STATUS.MISMATCH) {
      out.push(finding(FATAL, "asset-mismatch", `${e.name ?? e.aiId}: ${asset.notes.join("; ")}`));
      continue;
    }
    if (asset.status === STATUS.HISTORICAL) {
      out.push(finding(FATAL, "asset-historical", `${e.name ?? e.aiId}: ${asset.notes.join("; ")}. Exact-current art is required for a named entity tile`));
      continue;
    }
    if (requireExactBytes && !RENDERABLE.includes(asset.status)) {
      out.push(finding(FATAL, "asset-not-materialised", `${e.name ?? e.aiId}: art is ${asset.status}; a deterministic render needs verified bytes, so it must be materialised into the content-addressed cache and hashed first`));
      continue;
    }
    if (asset.status === STATUS.EXACT_REMOTE) {
      out.push(finding(WARN, "asset-remote", `${e.name ?? e.aiId}: current art is a remote URL with no repository bytes bound; a renderer must materialise and hash it before it can claim a deterministic build`));
    }
  }
  for (const e of dossier.assets.entries) {
    if (!CURRENT.includes(e.status) && !dossier.roster.some((r) => `ai:${r.aiId}` === e.entity)) {
      out.push(finding(WARN, "asset-orphan", `${e.entity}: art status ${e.status} for an entity outside the roster`));
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
  if (!spec.sceneDetail && dossier.sceneAssets.length && spec.locations.length > dossier.locations.length) {
    out.push(finding(WARN, "location-count", `the spec names ${spec.locations.length} locations for a subject with ${dossier.locations.length} components`));
  }

  // ---- narrative --------------------------------------------------------------------------------
  const anchored = new Set(dossier.narrative.map((b) => b.component));
  for (const s of Object.values(dossier.structure)) {
    if (!anchored.has(s.questId)) {
      out.push(finding(WARN, "no-narrative", `${s.name}: no story block is anchored to this component`));
    }
  }

  // ---- publication state --------------------------------------------------------------------
  for (const s of Object.values(dossier.structure)) {
    if (s.hidden) {
      out.push(finding(WARN, "hidden-subject", `${s.name} is hidden/unpublished in the current capture; that is provenance, and a player-facing artifact must not imply it is live`));
    }
  }

  const fatal = out.filter((f) => f.severity === FATAL);
  return { findings: out, fatal, warnings: out.filter((f) => f.severity === WARN), ok: fatal.length === 0 };
}

export { FATAL, WARN };
