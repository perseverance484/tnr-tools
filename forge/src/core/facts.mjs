// Pure domain reasoning. No DOM, no window, no presentation, no I/O.
//
// Everything here was previously a method on the UI App class. It is pure by construction: given
// the same facts it returns the same answer, which is what lets a second shell (or a headless
// host) ask the same questions without duplicating the reasoning or importing a view.

import { AUTH } from "../transport/auth.mjs";
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
  // Every capture that asked for a body to be KEPT, at any tier. The headline counts them together
  // because the operator's question is the same one either way — did the evidence actually land —
  // and the tier breakdown belongs on the screen, not in a toast.
  const full = captures.filter((capture) => capture.tier);
  const partial = captures.filter((capture) => capture.complete === false).length;
  const detail = job.items.length
    ? `${Object.entries(summary.counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")} · ${summary.verify.match} verified, ${summary.verify.drift} drift, ${summary.verify.unread} unread`
    : `${captures.filter((capture) => capture.ok).length}/${captures.length} captures read ok${full.length ? ` · ${full.filter((capture) => capture.persistOk === true).length}/${full.length} ${full.every((capture) => capture.tier === "repo-safe") ? "full bodies persisted" : "bodies retained at their tier"}` : ""}${partial ? ` · ${partial} paged walk${partial === 1 ? "" : "s"} incomplete` : ""} · zero mutations`;
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
