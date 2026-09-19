// Pure domain reasoning. No DOM, no window, no presentation, no I/O.
//
// Everything here was previously a method on the UI App class. It is pure by construction: given
// the same facts it returns the same answer, which is what lets a second shell (or a headless
// host) ask the same questions without duplicating the reasoning or importing a view.

import { AUTH } from "../transport/auth.mjs";
import { SLUGS } from "../transport/upload.mjs";
import { protectedPathsFor } from "../runner/runner.mjs";
import { jobOutcome } from "../storage/journal.mjs";

// One results-bundle entry, in the shape harvests/inbox/ already holds, so the repository's
// harvest.py reads a forge bundle natively (readiness brief section 9). The mapping is deliberate:
//
//   state     harvest's vocabulary, not the journal's: "ok" once the write landed, "error" for a
//             refusal, "skipped" for a skipped orphan, "pending" for anything that never got that
//             far. The journal's own state rides along as `forgeState`, so nothing is lost.
//   verdict   match | drift | unread, which is exactly what harvest's verify already understands
//             (unread prints UNVERIFIED and exits 1: a write with no read-back is not success).
//   asserted  the v4.28 checklist harvest counts: how many asserted keys landed and which did not.
//             Built from the keys the runner asserted and the diffs it recorded, so a drift is a
//             per-field FAIL rather than a line of prose.
export function harvestEntry(i) {
  const diffs = i.diffs || [];
  const assertedKeys = Array.isArray(i.asserted) ? i.asserted.length : (i.assertedRules ? 1 : 0);
  const landed = i.state === "VERIFIED" || (i.entityId && i.phase === "verify");
  const state = i.state === "FAILED" ? "error" : i.state === "SKIPPED" ? "skipped" : landed ? "ok" : "pending";
  return {
    name: i.name, srcId: i.srcId, entity: i.entity,
    slot: i.op === "create" ? "create" : "edit", op: i.op,
    state, forgeState: i.state, phase: i.phase,
    detail: i.error || i.reconciled || "",
    verdict: i.verify || null,
    asserted: assertedKeys || diffs.length ? {
      ok: Math.max(0, assertedKeys - diffs.length),
      fail: diffs.map((d) => ({ k: d.key, c: "mismatch", d: [`sent ${JSON.stringify(d.sent)}  live ${JSON.stringify(d.live)}`] })),
    } : null,
    diffs,
    id: i.entityId || i.targetId || null,
  };
}

// ------------------------------------------------------------------ image picks
//
// THE OBSERVED DEFECT (harvests/inbox/tnr_results_1789829183863.json, items 3-7). The manifest
// asked for `ai_godstorm_marrow_starless_monk.webp`; the picker keys the chosen File by that
// expected name and showed a green "picked" pill; what the operator had actually selected was the
// unprocessed master `1000014259.png` at 1709179 bytes. All five avatar edits ran to their upload
// and only then failed on the 524288-byte ceiling - after the job had started, one item at a time.
// Nothing was corrupted, but the operator learned at the end of a live run what the picker could
// have told them at the moment they tapped.
//
// The ledger is what binds. `imgSizes` already exists for exactly this: L17 makes a byte entry
// mandatory for every @img ref BECAUSE "the Android picker matches a file by size when the name
// differs" (runner/lints.mjs). So an exact byte match against the ledger is the contract, and a
// differing physical filename is REPORTED rather than refused - refusing it would break the
// documented picker behaviour the ledger was introduced to survive. A reviewer who wants the name
// to bind as well should say so; it is one line here, and it costs the Android path.
const EXT_MIME = Object.freeze({
  webp: "image/webp", png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif", avif: "image/avif",
});
const extOf = (n) => { const m = /\.([A-Za-z0-9]+)$/.exec(String(n ?? "")); return m ? m[1].toLowerCase() : null; };

/**
 * Does this physical file satisfy the manifest's contract for this logical image?
 * Pure: takes the facts, returns the verdict. Knows nothing about pills or buttons.
 *
 * @param {string} name       the manifest's logical filename (the @img key)
 * @param {{name?: string, size?: number, type?: string}|null} file  the selected File, or null
 * @param {object} imgSizes   the manifest's byte ledger
 * @param {string} slug       upload slug whose ceiling applies
 * @returns {{name, ok, state: "missing"|"ready"|"refused", expectedBytes, ceiling,
 *            picked: {name, size, type}|null, renamed: boolean, problems: string[]}}
 */
export function imagePick(name, file, imgSizes = {}, slug = "imageUploader") {
  const ceiling = (SLUGS[slug] ?? SLUGS.imageUploader).maxBytes;
  const has = imgSizes && Object.prototype.hasOwnProperty.call(imgSizes, name);
  const expectedBytes = has ? Number(imgSizes[name]) : null;
  if (!file) return { name, ok: false, state: "missing", expectedBytes, ceiling, picked: null, renamed: false, problems: [] };
  const picked = { name: file.name ?? null, size: Number(file.size), type: file.type || null };
  const problems = [];
  // 1. the ledger. Fail closed when there is none: an unledgered image cannot be checked at all,
  //    and L17 already refuses that manifest, so reaching here means something else is wrong.
  if (expectedBytes == null || !Number.isFinite(expectedBytes)) {
    problems.push(`the manifest has no imgSizes entry for ${name}, so these bytes cannot be checked against it`);
  } else if (picked.size !== expectedBytes) {
    problems.push(`selected file is ${picked.size} bytes; the manifest ledger says ${name} is ${expectedBytes}`);
  }
  // 2. the uploader's own ceiling, checked here instead of mid-run. A ledger entry that is itself
  //    over the ceiling is caught by this too.
  if (Number.isFinite(picked.size) && picked.size > ceiling) {
    problems.push(`selected file is ${picked.size} bytes, over the ${slug} ceiling of ${ceiling}`);
  }
  // 3. a light type check, only when the browser told us a type. An empty type is common and is
  //    not evidence of anything.
  const wantMime = EXT_MIME[extOf(name)] ?? null;
  if (picked.type && !picked.type.startsWith("image/")) problems.push(`selected file is ${picked.type}, not an image`);
  else if (picked.type && wantMime && picked.type !== wantMime) problems.push(`selected file is ${picked.type}; ${name} is a ${extOf(name)}`);
  return {
    name, ok: !problems.length, state: problems.length ? "refused" : "ready",
    expectedBytes, ceiling, picked, renamed: !!(picked.name && picked.name !== name), problems,
  };
}

/** Every image a manifest needs, against what the operator has actually picked. */
export function imagePicks(names, files, imgSizes = {}, slug = "imageUploader") {
  const get = files && typeof files.get === "function" ? (n) => files.get(n) : () => null;
  return (names ?? []).map((n) => imagePick(n, get(n) ?? null, imgSizes, slug));
}

/** The picks that must stop a job from starting, with the reason already attached. */
export function unusablePicks(picks) { return (picks ?? []).filter((p) => !p.ok); }

/**
 * Why Resume is not offered on a SESSION-paused job. A job that stopped because the game refused
 * the session must not offer a green Resume that will immediately be refused again: the operator
 * has to sign in and re-check first (independent review FPA-2). Returns null when resuming is fine.
 */
export function resumeBlockedReason(job, auth) {
  if (!job || !job.pause || job.pause.reason !== "SESSION") return null;
  if (!auth || auth.ready) return null;
  return "TNR authentication is still unavailable. Sign in to the game and re-check the session; resuming now would send nothing.";
}

/** Protected procedures a selected manifest would need that the session cannot supply. */
export function blockedPaths(auth, plan, manifest) {
  if (!auth) return [];
  try { return protectedPathsFor(plan, manifest).filter((path) => !auth.allows(path)); }
  catch { return []; }
}

/**
 * The standing answer to "can Forge do protected work right now", as facts rather than markup.
 * The view turns this into a banner; nothing here knows what a banner is.
 */
export function authFacts(auth, busy) {
  if (!auth) return null;
  const state = auth.state;
  if (state === AUTH.READY) return { level: "ok", ready: true, probing: false, signedOut: false, detail: auth.detail ?? null };
  if (state === AUTH.PROBING || busy) return { level: "info", ready: false, probing: true, signedOut: false, detail: auth.detail ?? null };
  return { level: "bad", ready: false, probing: false, signedOut: state === AUTH.SIGNED_OUT, detail: auth.detail ?? null };
}

/**
 * The honest headline for a finished job. Only outcome "success" is green: a finished job holding
 * a drifted, unread or failed item is reported as what it is. An auth pause gets its own sentence,
 * because the generic line would read "0/5 full bodies persisted", which is true and useless — it
 * describes the symptom of a signed-out session as though the captures were the problem (brief D).
 */
export function runHeadline(job, summary) {
  const captures = [...(job.capturesBefore || []), ...(job.capturesAfter || [])];
  const outcome = jobOutcome(job);
  const full = captures.filter((capture) => capture.persist === "full");
  const detail = job.items.length
    ? `${Object.entries(summary.counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")} · ${summary.verify.match} verified, ${summary.verify.drift} drift, ${summary.verify.unread} unread`
    : `${captures.filter((capture) => capture.ok).length}/${captures.length} captures read ok${full.length ? ` · ${full.filter((capture) => capture.persistOk === true).length}/${full.length} full bodies persisted` : ""} · zero mutations`;
  const kind = outcome === "success" ? "ok" : outcome === "failed" ? "bad" : "warn";
  if (job.pause && job.pause.reason === "SESSION") {
    return {
      outcome, kind: "bad", ms: 12000, sessionPause: true,
      text: `job PAUSED: TNR authentication unavailable${job.pause.path ? ` on ${job.pause.path}` : ""}. Nothing further was sent. Sign in and resume.`,
    };
  }
  return { outcome, kind, ms: 8000, sessionPause: false, text: `job ${summary.state} (${outcome}): ${detail}` };
}

/** Postflight tallies for the exported bundle. */
export function postflight(job) {
  return {
    match: job.items.filter((i) => i.verify === "match").length,
    diff: job.items.filter((i) => i.verify === "drift").length,
    unverified: job.items.filter((i) => i.verify === "unread").length,
    failed: job.items.filter((i) => i.state === "FAILED").length,
    skipped: job.items.filter((i) => i.state === "SKIPPED").length,
    unresolved: job.items.filter((i) => !["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)).length,
  };
}
