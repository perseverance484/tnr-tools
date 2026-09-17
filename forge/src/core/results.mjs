// Capture materialization and results-bundle assembly. Talks to the journal, the capture cache
// and the repository; never to the DOM.

import { MAX_FULL_CAPTURE_BYTES } from "../storage/captures.mjs";
import { readGh } from "../storage/compat.mjs";
import { GH } from "../github.mjs";
import { jobOutcome } from "../storage/journal.mjs";
import { harvestEntry, postflight } from "./facts.mjs";

/**
 * Materialize every requested full capture body out of the IndexedDB capture cache, and write the
 * VERDICT (not the body) back onto the job's own capture entries. Two things follow from doing it
 * this way:
 *
 *   - the export never issues a read. The body it ships is the immutable snapshot the capture pass
 *     committed from that read's own response; if it is not there, the export says so rather than
 *     going back to the game for it. It is NOT read out of the path+id read cache, which a later
 *     read or a write to the entity may legitimately have replaced or dropped (review FFC-1);
 *   - the journal stays compact and stays the record of truth. persistOk/persistError live on the
 *     journal entry, so jobOutcome(), the run screen and the bundle all read one answer, and the
 *     embedded `journal` in the bundle never duplicates the bodies beside it.
 *
 * Returns the export-ready capture list: summary entries exactly as journaled, full entries with
 * `data` attached when, and only when, the body was materialized intact.
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
    if (job[key].some((capture) => capture && capture.persist === "full")) {
      patch[key] = resolved.map(({ data, ...rest }) => rest); // the journal keeps the verdict, never the body
    }
    out.push(...resolved);
  }
  if (Object.keys(patch).length) journal.annotateJob(jobId, patch);
  return out;
}

export async function materialize(cache, capture) {
  if (!capture || typeof capture !== "object" || capture.persist !== "full") return capture;
  const c = { ...capture, persistOk: false, persistError: null };
  delete c.data;
  if (capture.ok !== true) { c.persistError = "read failed; there is no body to persist"; return c; }
  // A failure the capture pass already recorded stands. It was decided with the body in hand -
  // over the ceiling, or IndexedDB refused the write - so it names the real reason, which is more
  // specific than the "snapshot is gone" the lookup below would infer from the snapshot that was
  // deliberately never written. Export may downgrade a success; it never overwrites a recorded
  // reason, and it never upgrades a failure.
  if (capture.persistOk === false && capture.persistError) return { ...c, persistError: capture.persistError };
  const key = capture.snapshotKey || null;
  if (!key) { c.persistError = "no capture snapshot key was journaled for this full capture"; return c; }
  let rec = null;
  try { rec = await cache.getSnapshot(key); }
  catch (e) { c.persistError = "capture snapshot read failed: " + ((e && e.message) || String(e)); return c; }
  if (!rec) { c.persistError = `capture snapshot ${key} is gone, so the full body cannot be exported without a second read; it was not re-read`; return c; }
  const bytes = typeof rec.bytes === "number" ? rec.bytes : JSON.stringify(rec.data ?? null).length;
  c.bytes = bytes;
  if (bytes > MAX_FULL_CAPTURE_BYTES) { c.persistError = `body is ${bytes} bytes, over the ${MAX_FULL_CAPTURE_BYTES}-byte full-capture ceiling; it is NOT truncated and NOT persisted`; return c; }
  c.persistOk = true;
  c.at = rec.at ?? null; // when this exact body was read, so the bundle carries its own freshness
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
