// Capture materialization and results-bundle assembly. Talks to the journal, the capture cache
// and the repository; never to the DOM.

import { tierCeiling, captureTier, isLegacyCapture, canPersistFull } from "../storage/captures.mjs";
import { TIERS, projectBody, validateProjection } from "../research/registry.mjs";
import { readGh } from "../storage/compat.mjs";
import { GH } from "../github.mjs";
import { jobOutcome } from "../storage/journal.mjs";
import { harvestEntry, postflight } from "./facts.mjs";

/**
 * Materialize every retained capture body out of the IndexedDB snapshot store AT ITS DECLARED TIER,
 * and write the VERDICT (not the body) back onto the job's own capture entries. Two things follow
 * from doing it this way:
 *
 *   - the export never issues a read. The body it ships is the immutable snapshot the capture pass
 *     committed from that read's own response; if it is not there, the export says so rather than
 *     going back to the game for it. It is NOT read out of the path+id read cache, which a later
 *     read or a write to the entity may legitimately have replaced or dropped (review FFC-1);
 *   - the journal stays compact and stays the record of truth. persistOk/persistError live on the
 *     journal entry, so jobOutcome(), the run screen and the bundle all read one answer, and the
 *     embedded `journal` in the bundle never duplicates the bodies beside it.
 *
 * Returns the export-ready capture list: summary entries exactly as journaled, and tiered entries
 * carrying `data` when and only when their tier allows a body into an export at all - the whole
 * body for repo-safe, the declared fields for projected, and nothing for local-only.
 */
export async function resolveCaptures({ journal, cache }, jobId) {
  const job = journal.get(jobId);
  const patch = {};
  const out = [];
  for (const key of ["capturesBefore", "capturesAfter"]) {
    if (!Array.isArray(job[key])) continue;
    const resolved = [];
    for (const capture of job[key]) resolved.push(await materialize(cache, capture));
    // Only a pass that actually re-checked something rewrites the journal: a job with no full
    // capture is untouched by exporting it, exactly as before this contract existed.
    if (job[key].some((capture) => captureTier(capture))) {
      patch[key] = resolved.map(({ data, ...rest }) => rest); // the journal keeps the verdict, never the body
    }
    out.push(...resolved);
  }
  // Abandoned attempts are evidence too: a walk that was rate-limited part way through really did
  // ask for those pages and really did get those answers. They are appended as recorded, never
  // materialized - there is no snapshot behind an attempt that never finished, and they carry their
  // own non-success verdict - so an exported bundle shows the paused attempt beside the completed
  // read rather than quietly omitting it (independent review FN5).
  for (const key of ["capturesBeforeAttempts", "capturesAfterAttempts"]) {
    if (Array.isArray(job[key])) out.push(...job[key]);
  }
  if (Object.keys(patch).length) journal.annotateJob(jobId, patch);
  return out;
}

/**
 * Turn ONE journaled capture into its export-ready form, at its declared tier.
 *
 * This is the leak boundary. There is exactly one statement in this function that can put a read's
 * bytes into an exported bundle, and it is reached only for a repo-safe snapshot; a projected
 * snapshot exports a freshly derived projection of the declared fields and nothing else; a
 * local-only snapshot exports a verdict and never a body, however green everything else looks.
 * There is no fallback path from a failed projection to the full body, and no re-read: a body that
 * is not there is reported missing, not fetched again to make the export greener.
 */
export async function materialize(cache, capture) {
  // captureTier() also recognises a Phase 0 `persist: "full"` record, which has no `tier` key. Asking
  // it rather than reading capture.tier is what stops an upgraded journal's existing full captures
  // from being mistaken for captures that asked for no body at all (independent review FN1).
  const asked = captureTier(capture);
  if (!asked) return capture;
  const c = { ...capture, tier: asked, persistOk: false, persistError: null };
  delete c.data;
  if (capture.ok !== true) { c.persistError = "read failed; there is no body to persist"; return c; }
  // A failure the capture pass already recorded stands. It was decided with the body in hand - over
  // the ceiling, a projection whose declared fields were absent, or IndexedDB refusing the write -
  // so it names the real reason, which is more specific than the "snapshot is gone" the lookup
  // below would infer from a snapshot that was deliberately never written. Export may downgrade a
  // success; it never overwrites a recorded reason, and it never upgrades a failure.
  if (capture.persistOk === false && capture.persistError) return { ...c, persistError: capture.persistError };
  // A pre-tier record can only be one thing: a full capture of a path that was on the audited
  // point-read allowlist at the time. If it names anything else it is not a record this code can
  // honestly interpret, and guessing is how a body ends up somewhere it was never approved for.
  if (isLegacyCapture(capture) && !canPersistFull(capture.proc)) {
    c.persistError = `this capture predates persistence tiers and names ${capture.proc}, which is not an approved repo-safe path; its body is not exported`;
    return c;
  }
  const key = capture.snapshotKey || null;
  if (!key) { c.persistError = "no capture snapshot key was journaled for this capture"; return c; }
  let rec = null;
  try { rec = await cache.getSnapshot(key); }
  catch (e) { c.persistError = "capture snapshot read failed: " + ((e && e.message) || String(e)); return c; }
  if (!rec) { c.persistError = `capture snapshot ${key} is gone, so the body cannot be exported without a second read; it was not re-read`; return c; }

  // The snapshot's own tier is authority, and where the two disagree the NARROWER one wins. A body
  // read under local-only stays local-only even if the journal entry beside it says otherwise,
  // which is what makes a tampered or stale journal entry unable to widen an export. A snapshot
  // written before tiers existed has no tier of its own: it is repo-safe only if its path is still
  // an approved repo-safe one, and otherwise falls to the narrowest tier rather than to trust.
  const recTier = typeof rec.tier === "string" && rec.tier ? rec.tier : (canPersistFull(rec.path) ? "repo-safe" : TIERS[0]);
  const tier = TIERS[Math.min(TIERS.indexOf(asked), TIERS.indexOf(recTier))] ?? TIERS[0];
  c.tier = tier;
  // Policy provenance travels with the BODY. A record that carries none predates the stamp and is
  // shown as carrying none: export never fabricates one from today's registry (review FN4).
  if (rec.policy) c.policy = rec.policy;
  const bytes = typeof rec.bytes === "number" ? rec.bytes : JSON.stringify(rec.data ?? null).length;
  c.bytes = bytes;
  if (bytes > tierCeiling(tier)) { c.persistError = `body is ${bytes} bytes, over the ${tierCeiling(tier)}-byte ${tier} capture ceiling; it is NOT truncated and NOT persisted`; return c; }
  c.at = rec.at ?? null; // when this exact body was read, so the bundle carries its own freshness

  if (tier === "local-only") {
    // Retained locally, exported never. persistOk is true because the capture DID do what it
    // promised: the exact body is in IndexedDB for the operator. The bundle says so and carries none
    // of it, which is the whole contract of this tier (RUL-2026-09-17-001).
    c.persistOk = true;
    c.localOnly = true;
    return c;
  }
  if (tier === "projected") {
    // THE RETAINED DECLARATION IS AUTHORITY. It was validated when the capture was taken and stored
    // beside the body; the journal entry is mutable state that a stale write, an edit or a resumed
    // job can change. Export used to prefer the journal's copy, which let a changed journal redirect
    // the projection at an undeclared field and ship it (independent review FN2). The journal may
    // now only AGREE; any difference is reported and nothing is exported.
    const retained = Array.isArray(rec.projection) ? rec.projection : null;
    if (!retained || !retained.length) {
      c.persistError = "no projection was retained with this capture's body, so nothing may be exported from it";
      return c;
    }
    const claimed = Array.isArray(capture.projection) ? capture.projection : null;
    if (claimed && (claimed.length !== retained.length || claimed.some((f, i) => f !== retained[i]))) {
      c.persistError = `the journal declares a projection (${claimed.join(", ")}) that differs from the one retained with the body (${retained.join(", ")}); the retained declaration is authority, so nothing is exported`;
      return c;
    }
    // Re-validated at the leak boundary, not merely trusted because it was validated once. A
    // declaration that is no longer admissible - a field the registry has since withdrawn, or a
    // malformed path in a hand-edited store - must fail the export rather than be applied, and it
    // must fail as a VERDICT rather than as an exception thrown into the export path.
    let fields;
    try { fields = validateProjection(rec.path, retained); }
    catch (e) { c.persistError = "the retained projection is not admissible: " + ((e && e.message) || String(e)); return c; }
    const pr = projectBody(rec.data, fields);
    if (!pr.ok) { c.persistError = `projection failed: ${pr.missing.join(", ")} ${pr.missing.length === 1 ? "is" : "are"} absent from the body or is not a declarable field. The full body is NOT substituted and NOT exported`; return c; }
    c.projection = [...fields];
    c.persistOk = true;
    c.data = pr.data;
    return c;
  }
  c.persistOk = true;
  c.data = rec.data;
  return c;
}

/** The results bundle, in the shape harvests/inbox/ already holds. */
export function buildBundle({ version, storage, now }, job, captures) {
  return {
    builder: version, at: new Date(now()).toISOString(), cfg: "forge", checks: null,
    // `outcome` is the honest headline: an exported bundle is evidence, not a claim of success.
    state: job.state, outcome: jobOutcome(job),
    postflight: postflight(job),
    entries: job.items.map((i) => harvestEntry(i)),
    captures,
    idmap: JSON.parse(storage.getItem("tnr_bk_idmap_v1") || "{}"),
    journal: job,
  };
}

export const bundleName = (now) => `tnr_results_${now()}.json`;

/** Is repository sync configured and switched on? */
export function repoSyncReady(storage) {
  const gh = readGh(storage);
  return Boolean(gh.on && gh.pat);
}

export const inboxPath = (name) => `${GH.inboxDir}/${name}`;
