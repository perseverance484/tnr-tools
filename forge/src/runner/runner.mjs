// The runner (spec sections 4, 5, 8). Executes a job item by item with write-ahead state
// transitions, two-phase creates, and read-back on asserted keys only. Never retries.
//
// Item lifecycle, per phase, every SENT flushed before its request leaves:
//   create:  PLANNED -SENT(phase create)-> CONFIRMED{entityId, phase update}
//   update:  CONFIRMED/PLANNED -SENT(phase update)-> CONFIRMED{phase rules|verify}
//   rules:   (ai with rules, aiProfile) CONFIRMED -SENT(phase rules-toggle|rules)-> CONFIRMED{phase verify}
//   verify:  CONFIRMED{phase verify} -> VERIFIED when the asserted keys read back equal; else
//            stays CONFIRMED{phase verify} with item.diffs recorded (drift is visible, not hidden).
//
// The phase written on CONFIRMED is the NEXT thing to do. Once a send has succeeded the item is
// at phase "verify" (or "rules"), never back at "update", so a resume after a read-back 429 can
// only read, never re-send (adversarial review L4, R1-R4).
//
// Anything thrown INSIDE a withSent thunk (NetworkError, TransportError, or a bug) leaves the
// item SENT: the request may have left. The job pauses; resume goes through reconciliation.
// A transport failure on a READ (outside withSent) pauses the job too, leaving the item where
// it was. A server refusal (success:false) or a validation error is FAILED, never retried.
// TOO_MANY_REQUESTS from a read pauses the job with the path and countdown (budget layer).

import { readCreate, readMutation, classifyError } from "../transport/outcome.mjs";
import { AuthUnavailable, AuthRefused } from "../transport/auth.mjs";
import { isProtected } from "../transport/procedures.mjs";
import { NetworkError } from "../transport/client.mjs";
import { TransportError } from "../transport/envelope.mjs";
import { RateLimited } from "../budget/bucket.mjs";
import { readIdmap, writeIdmap } from "../storage/compat.mjs";
import { readAssetUploads, recordAssetUpload } from "../storage/assets.mjs";
import { toHex } from "./imgpack.mjs";
import { snapshotKey, tierCeiling } from "../storage/captures.mjs";
import { projectBody, capturePolicy } from "../research/registry.mjs";
import { TERMINAL_ITEM_STATES, jobOutcome } from "../storage/journal.mjs";
import { recipe, mergeForUpdate } from "./recipes.mjs";
import { resolveRefs, collectRefs } from "./refs.mjs";
import { diffAsserted, deepEqualPayload } from "./validate.mjs";
import { parseManifest, planOrder, toJournalSpecs } from "./manifest.mjs";

// One tab drives a job at a time. Two runners over one localStorage would each read PLANNED and
// both send (adversarial L1/L3: the whole-record journal write cannot detect it). The lease is a
// key per job with the driving tab's id and a heartbeat; another tab refuses to run or resume
// while the heartbeat is fresh. A crashed tab's lease expires by itself.
export const LEASE_PREFIX = "tnr_forge_lease_v1:";
export const LEASE_TTL_MS = 30_000;
export class LeaseHeld extends Error {
  constructor(jobId, lease) { super(`job ${jobId} is being driven by another tab (heartbeat ${Math.round((Date.now() - lease.at) / 1000)}s ago); wait ${Math.ceil(LEASE_TTL_MS / 1000)}s or close it`); this.name = "LeaseHeld"; this.lease = lease; }
}
const randomTab = () => Math.random().toString(36).slice(2, 10) + Math.random().toString(36).slice(2, 6);

export class Paused extends Error {
  constructor(reason, info = {}) { super(`paused: ${reason}`); this.name = "Paused"; this.reason = reason; Object.assign(this, info); }
}
const isTransport = (e) => e instanceof NetworkError || e instanceof TransportError;

/**
 * Every protected procedure a planned job would touch. The UI asks this before offering to run a
 * manifest, and run()/resume() ask it before the first request, so "this manifest needs a session
 * you do not have" is answered once, in one place, from the audited procedure table rather than
 * from a guess about what a manifest looks like.
 */
export function protectedPathsFor(order, manifest) {
  const paths = new Set();
  const captures = manifest && manifest.capture ? [...(manifest.capture.before || []), ...(manifest.capture.after || [])] : [];
  for (const c of captures) {
    const path = c.proc || c.procedure;
    if (path && isProtected(path)) paths.add(path);
  }
  for (const planned of order || []) {
    const rc = recipe(planned.entity);
    for (const path of [rc.create && rc.create.path, rc.get, rc.update, rc.names, rc.profileToggle, rc.profileUpdate]) {
      if (path && isProtected(path)) paths.add(path);
    }
  }
  return [...paths];
}

export class Runner {
  /**
   * @param {object} d  dependencies
   * @param {import("../storage/journal.mjs").Journal} d.journal
   * @param {import("../transport/client.mjs").TrpcClient} d.client
   * @param {import("../budget/reader.mjs").CachedReader} d.reader
   * @param {import("../storage/captures.mjs").CaptureCache} d.cache
   * @param {import("./validate.mjs").Validator} d.validator
   * @param {object} [d.uploader]      {upload(file) -> {ufsUrl}}
   * @param {(bytes: ArrayBuffer) => Promise<ArrayBuffer>} [d.digest]  SHA-256, for re-verifying a
   *   pack-backed image immediately before its upload. Absent, a pack-backed upload fails closed.
   * @param {object} [d.reconciler]    {beforeCreate(job, item, entity), resolveSent(job, item, ctx)}
   * @param {Storage} d.storage        for the retained idmap
   * @param {object} [d.auth]          {assert(path), state} - the auth gate. Optional so a
   *   harness can leave it out; when it is absent nothing is gated, exactly as before it existed.
   * @param {(msg: string, item?: object) => void} [d.log]
   */
  constructor(d) {
    for (const k of ["journal", "client", "reader", "cache", "validator", "storage"]) if (!d[k]) throw new Error("Runner needs " + k);
    Object.assign(this, d);
    this.log = d.log ?? (() => {});
    this.files = new Map(); // name -> File, from the UI picker OR a repo-backed image pack
    // name -> {sha256, path, ref, bytes, at} for the images a repo-backed pack supplied. Only a
    // VERIFIED fetch writes here (core/imagepack.mjs), so its presence is the runner's own evidence
    // that these bytes are the ones the manifest named - which is why the upload path below trusts
    // content identity for a pack-backed image and the name-keyed idmap only for a picked one.
    this.imgProvenance = new Map();
    this.manifests = new Map(); // jobId -> parsed manifest (data lives here, not in the journal)
    this.pauseRequested = false;
    this.tabId = d.tabId ?? randomTab();
    this.clock = d.clock ?? (() => Date.now());
    this._subs = new Set();
  }

  // ------------------------------------------------------------------ progress events (advisory)
  /**
   * Subscribe to structured progress events. ADVISORY ONLY, and the word is load-bearing:
   *
   *   - _emit writes nothing to the journal and performs no state transition;
   *   - it is synchronous and never awaited, so a subscriber cannot delay, reorder or interleave a
   *     request. Every emit sits between awaits that already existed, so the send sequence is
   *     byte-for-byte what it was before this hook existed;
   *   - every subscriber runs inside try/catch. A throwing subscriber is swallowed here rather
   *     than unwinding the run, because a UI progress listener must never be able to fail a job
   *     that is mid-mutation.
   *
   * Phase 0 adds this so the extracted core can drive a progress view without the view reaching
   * into runner internals or polling. Nothing in execution reads it back.
   *
   * @param {(event: {type: string, at: number, jobId: string|null, [k: string]: any}) => void} fn
   * @returns {() => void} unsubscribe
   */
  on(fn) {
    if (typeof fn !== "function") throw new TypeError("Runner.on needs a function");
    this._subs.add(fn);
    return () => this._subs.delete(fn);
  }

  _emit(type, payload = {}) {
    if (!this._subs.size) return;
    const event = { type, at: this.clock(), ...payload };
    for (const fn of [...this._subs]) {
      try { fn(event); } catch { /* advisory: a listener must never affect the run */ }
    }
  }

  // ------------------------------------------------------------------ auth gate
  /**
   * Refuse a protected call while the game session is not established, BEFORE anything is
   * journaled or sent (brief sections D and E). Two properties matter and both come from where
   * this is called rather than from what it does:
   *
   *   - it runs before withSent(), so a refusal leaves the item in the state it was already in.
   *     Nothing is marked SENT, so nothing enters reconciliation, and the mutation provably never
   *     left the device. SENT semantics for real transport ambiguity are untouched;
   *   - it keys off the procedure, not the job, so a public read still runs signed out. A
   *     capture-only manifest over gameAsset.get is unaffected by a missing session, which is
   *     what the procedure guards themselves already allow.
   */
  _requireAuth(path, idx = null) {
    if (!this.auth || typeof this.auth.assert !== "function") return;
    try { this.auth.assert(path); }
    catch (e) {
      if (!(e instanceof AuthUnavailable)) throw e;
      throw new Paused("SESSION", { idx, path, detail: e.message, authState: e.state });
    }
  }

  /** Every protected path a job would touch, so the gate can refuse before the first request. */
  _protectedPaths(order, manifest) { return protectedPathsFor(order, manifest); }

  /**
   * The server just proved this session is not authenticated. Invalidate the shared auth state
   * BEFORE pausing, so that everything downstream - the banner, the Resume button, the next
   * job's preflight - reads the server's answer rather than the last successful probe
   * (independent review FPA-2). Returns the Paused the caller should throw, so that recording the
   * refusal and stopping are one statement and cannot drift apart.
   */
  _authRefused(error, info = {}) {
    const detail = error && error.message ? String(error.message) : "UNAUTHORIZED";
    if (this.auth && typeof this.auth.refuse === "function") {
      this.auth.refuse(`${info.path ? info.path + ": " : ""}${error && error.code ? error.code : "UNAUTHORIZED"}`);
    }
    this.log(`the game refused ${info.path || "a protected procedure"} as unauthenticated; auth state invalidated`);
    return new Paused("SESSION", { detail, authState: "signed_out", ...info });
  }

  // ------------------------------------------------------------------ lease
  _leaseKey(jobId) { return LEASE_PREFIX + jobId; }
  _readLease(jobId) { try { return JSON.parse(this.storage.getItem(this._leaseKey(jobId)) || "null"); } catch { return null; } }
  /** Take or refresh the lease for this tab; throws LeaseHeld if another tab's heartbeat is fresh. */
  _lease(jobId) {
    const cur = this._readLease(jobId);
    const now = this.clock();
    if (cur && cur.tab !== this.tabId && typeof cur.at === "number" && now - cur.at < LEASE_TTL_MS) throw new LeaseHeld(jobId, cur);
    this.storage.setItem(this._leaseKey(jobId), JSON.stringify({ tab: this.tabId, at: now }));
  }
  _releaseLease(jobId) {
    const cur = this._readLease(jobId);
    if (cur && cur.tab === this.tabId) this.storage.removeItem(this._leaseKey(jobId));
  }

  // ------------------------------------------------------------------ lifecycle
  /** Plan a manifest and open a job. Returns the journal job. Does not send anything. */
  plan(manifestSource, { jobId, manifestPath = null, manifestNumber = null } = {}) {
    const manifest = parseManifest(manifestSource);
    const order = planOrder(manifest, readIdmap(this.storage));
    const captureOnly = order.length === 0 && manifest.capture.before.length + manifest.capture.after.length > 0;
    const job = this.journal.open({ jobId, manifestPath, manifestNumber, manifestHash: manifest.hash, items: toJournalSpecs(order), allowEmpty: captureOnly });
    this.manifests.set(jobId, { manifest, order });
    return job;
  }

  /** Attach the parsed manifest to an existing (resumed) job. */
  attach(jobId, manifestSource) {
    const manifest = parseManifest(manifestSource);
    const job = this.journal.get(jobId);
    if (!job) throw new Error("no such job " + jobId);
    if (job.manifestHash && manifest.hash !== job.manifestHash) {
      // One specific mismatch is not an edited file. A job opened by a bundle that hashed bodies
      // alone recorded the pre-policy identity; this file still matches that, but its execution
      // policy (dedupNames / readBack / skipPreflight / imgSizes) was never part of what the job
      // recorded, so there is nothing to compare it against and resuming would be exactly the
      // unsafe equivalence that let manifest 51 be mistaken for job 50. Refuse - and say which of
      // the two things happened, because the operator's next move differs.
      if (manifest.bodyHash === job.manifestHash) {
        throw new Error(`job ${jobId} was opened before manifest identity covered execution policy (journal hash ${job.manifestHash} is this file's body hash). Its policy - dedupNames/readBack/skipPreflight/imgSizes - was never recorded, so it cannot be resumed safely under this bundle. Export the job for evidence and start a fresh one from the manifest.`);
      }
      throw new Error(`manifest changed under job ${jobId}: journal hash ${job.manifestHash}, file hash ${manifest.hash}`);
    }
    const order = planOrder(manifest, readIdmap(this.storage));
    if (order.length !== job.items.length) throw new Error("manifest item count differs from the journal");
    this.manifests.set(jobId, { manifest, order });
  }

  /** Ask the loop to stop after the current item. */
  requestPause() { this.pauseRequested = true; }

  /** Run every non-terminal item in order. Returns a summary. */
  async run(jobId) {
    const { manifest, order } = this._m(jobId);
    let job = this.journal.get(jobId);
    if (job.state === "DONE" || job.state === "ABORTED") return this.summary(jobId);
    if (job.state === "PAUSED" || job.state === "INCOMPLETE") {
      const t = this.budget && this.budget.log && this.budget.log.tripped();
      if (t) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: t.path, until: t.until });
      job = this.journal.setJobState(jobId, "RUNNING");
    }
    if (job.items.some((it) => it.state === "SENT")) {
      throw new Error("job has SENT items; call resume() so they are reconciled before anything else is sent");
    }
    // Pre-flight: refuse the whole job at the door when it needs a session it does not have, so a
    // signed-out operator gets one clear auth message instead of the first item discovering it.
    // Only paths this job would actually use are checked, so a public capture-only job is not
    // caught by a manifest it has nothing to do with.
    for (const path of this._protectedPaths(order, manifest)) {
      try { this._requireAuth(path); }
      catch (e) { if (e instanceof Paused) return this._pause(jobId, e.reason, e); throw e; }
    }
    this._lease(jobId);
    this._syncIdmapFromJob(job);
    this.pauseRequested = false;
    this._emit("job:start", { jobId, items: job.items.length, mode: "run" });
    try {
      if (manifest.capture.before.length && !job.capturesBefore) await this._captures(jobId, manifest.capture.before, "before");
      if (manifest.dedupNames) await this._dedupNames(jobId, order);
      for (let i = 0; i < job.items.length; i++) {
        this._lease(jobId); // heartbeat
        job = this.journal.get(jobId);
        const item = job.items[i];
        if (["VERIFIED", "FAILED", "SKIPPED"].includes(item.state)) continue;
        // an orphan is a pending decision (adopt or skip); nothing after it may be sent until
        // the user makes it, because later items may reference the id it is waiting on
        if (item.state === "ORPHANED") throw new Paused("ORPHANED", { idx: i, detail: item.error ?? null });
        if (this.pauseRequested) throw new Paused("USER", { idx: i });
        this._emit("item:start", { jobId, idx: i, name: item.name ?? null, entity: item.entity ?? null, phase: item.phase ?? null });
        await this._runItem(jobId, item, order[i], manifest);
        this._emit("item:end", { jobId, idx: i, state: this.journal.get(jobId).items[i]?.state ?? null });
      }
      if (manifest.capture.after.length && !job.capturesAfter) await this._captures(jobId, manifest.capture.after, "after");
    } catch (e) {
      if (e instanceof Paused) return this._pause(jobId, e.reason, e);
      if (e instanceof AuthRefused) { const p = this._authRefused(e.error, { path: e.path }); return this._pause(jobId, p.reason, p); }
      // raised by the capture passes (item reads pause inside _runItem): never escape as a crash
      if (e instanceof RateLimited) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: e.path, until: e.until });
      if (isTransport(e)) return this._pause(jobId, "NETWORK", { detail: String(e && e.message), httpStatus: e.httpStatus ?? null });
      this._releaseLease(jobId);
      throw e;
    }
    // DONE is only for a job whose every item reached a terminal state. An item still CONFIRMED at
    // phase "verify" is a write whose read-back was unread or drifted: execution has nothing left to
    // send, but the job is not verified, so it finishes INCOMPLETE and stays resumable for a re-read.
    const finished = this.journal.get(jobId);
    const unresolved = finished.items.filter((it) => !TERMINAL_ITEM_STATES.includes(it.state));
    this.journal.setJobState(jobId, unresolved.length ? "INCOMPLETE" : "DONE");
    this._releaseLease(jobId);
    if (this.reconciler && typeof this.reconciler.forget === "function" && !unresolved.length) this.reconciler.forget(jobId);
    const summary = this.summary(jobId);
    this._emit("job:end", { jobId, state: summary.state ?? null });
    return summary;
  }

  /** Reconcile SENT items through the reconciler, then run. */
  async resume(jobId) {
    if (!this.reconciler) throw new Error("resume needs a reconciler");
    const { manifest, order } = this._m(jobId);
    const job = this.journal.get(jobId);
    // Reconciliation answers "did this SENT request land" by READING. Against a dead session
    // every one of those reads fails, and the reconciler's honest answer to an unreadable record
    // is to ORPHAN it - which would turn a five-minute sign-in into a pile of adopt-or-skip
    // decisions about writes that are perfectly fine. Gate before the first read instead.
    for (const path of this._protectedPaths(order, manifest)) {
      try { this._requireAuth(path); }
      catch (e) { if (e instanceof Paused) return this._pause(jobId, e.reason, e); throw e; }
    }
    this._lease(jobId);
    this._syncIdmapFromJob(job);
    try {
      for (const item of job.items) {
        if (item.state !== "SENT") continue;
        const planned = order[item.idx];
        const r = await this.reconciler.resolveSent(this.journal.get(jobId), item, { planned, lookup: this._lookup(this.journal.get(jobId)) });
        if (r.action === "confirm") {
          // landed:true means the sent request is proven to have applied; the runner never re-sends
          // it. The next step is verify, except that a landed UPDATE on an ai with rules still owes
          // its rules step (adversarial L3-5: otherwise the profile is never written).
          const owesRules = item.phase === "update" && item.entity === "ai" && Array.isArray(planned?.data?.rules);
          const phase = r.landed ? (owesRules ? "rules" : "verify") : (r.phase ?? item.phase);
          this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: r.entityId ?? item.entityId, phase, reconciled: r.note ?? "confirmed by reconciliation" });
          if (r.entityId && item.srcId) this._remember(item.srcId, r.entityId);
        } else if (r.action === "orphan") {
          this.journal.transition(jobId, item.idx, "ORPHANED", { error: r.note ?? "ambiguous after crash", candidates: r.candidates ?? [] });
        } else {
          throw new Error("reconciler returned unknown action " + r.action);
        }
      }
    } catch (e) {
      // reconciliation only reads; a limited or failed read pauses with the reason recorded and
      // the SENT items untouched, so the next resume reconciles them again (adversarial L3-5)
      //
      // The session can expire between resume()'s preflight gate and these reads. The reconciler
      // raises that distinctly rather than answering ORPHANED, so the answer here is the same as
      // for any other failed reconciliation read - pause, touch nothing - plus invalidating the
      // auth state so the banner, the gate and Resume all agree (independent review round 2,
      // surviving path B). Every SENT item stays SENT and is reconciled again after sign-in.
      if (e instanceof AuthRefused) { const p = this._authRefused(e.error, { path: e.path }); return this._pause(jobId, p.reason, p); }
      if (e instanceof RateLimited) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: e.path, until: e.until });
      if (isTransport(e)) return this._pause(jobId, "NETWORK", { detail: String(e && e.message), httpStatus: e.httpStatus ?? null });
      this._releaseLease(jobId);
      throw e;
    }
    return this.run(jobId);
  }

  /**
   * User decision on an ORPHANED item: adopt an id. A phase-create orphan continues at update;
   * an orphan that already had an id keeps its phase (the user is choosing to re-send THAT
   * step, and the UI says so). Refuses ids already held by another item.
   */
  adopt(jobId, idx, entityId) {
    const job = this.journal.get(jobId);
    const item = job.items[idx];
    if (!item) throw new Error("no such item " + idx);
    if (item.state !== "ORPHANED") throw new Error(`adopt needs an ORPHANED item; ${item.idx} is ${item.state}`);
    if (!entityId) throw new Error("adopt needs an id");
    // journal-global, not job-local: an id another JOB holds is the same overwrite hazard, and the
    // orphan UI accepts a pasted id when there are no candidates (adversarial review F2)
    const holder = this.journal.findHolder(item.entity, entityId, { exceptJobId: jobId, exceptIdx: idx });
    if (holder) throw new Error(`${entityId} is already held by job ${holder.jobId} item ${holder.idx} (${holder.name}) in state ${holder.state}`);
    const phase = item.phase === "create" || !item.entityId ? "update" : item.phase;
    this.journal.transition(jobId, idx, "CONFIRMED", { entityId, phase, adopted: true, error: null });
    if (item.srcId) this._remember(item.srcId, entityId);
  }
  skip(jobId, idx) { this.journal.transition(jobId, idx, "SKIPPED"); }

  summary(jobId) {
    const job = this.journal.get(jobId);
    const counts = {};
    for (const it of job.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
    // `state` says whether execution finished; `outcome` says whether it is good news. Only
    // "success" may ever be presented as one (jobOutcome in journal.mjs).
    const verify = { match: 0, drift: 0, unread: 0 };
    for (const it of job.items) if (it.verify && verify[it.verify] !== undefined) verify[it.verify]++;
    return { jobId, state: job.state, outcome: jobOutcome(job), pause: job.pause, counts, verify, items: job.items.map((it) => ({ idx: it.idx, name: it.name, entity: it.entity, state: it.state, phase: it.phase, entityId: it.entityId, error: it.error ?? null, diffs: it.diffs ?? null, verify: it.verify ?? null })) };
  }

  // ------------------------------------------------------------------ items
  async _runItem(jobId, item, planned, manifest) {
    const ent = item.entity;
    try {
      if (item.state === "CONFIRMED" && item.phase === "verify") return await this._verifyOrSkip(jobId, item, planned, manifest);
      if (item.state === "CONFIRMED" && (item.phase === "rules" || item.phase === "rules-toggle")) {
        // the update landed (reconciled or normal); only the rules step remains
        await this._rules(jobId, item, planned, item.entityId ?? item.targetId);
        item = this.journal.get(jobId).items[item.idx];
        if (item.state === "CONFIRMED") await this._verifyOrSkip(jobId, item, planned, manifest);
        return;
      }
      if (item.op === "create" && item.state === "PLANNED") {
        // everything that can fail locally fails BEFORE a placeholder is created (L4 review)
        await this._preflight(item, planned);
        await this._create(jobId, item, planned);
        item = this.journal.get(jobId).items[item.idx];
        if (item.state !== "CONFIRMED") return; // FAILED
      }
      if (ent === "aiProfile") {
        await this._rules(jobId, item, planned, item.targetId);
      } else {
        await this._fill(jobId, item, planned);
        item = this.journal.get(jobId).items[item.idx];
        if (item.state !== "CONFIRMED") return;
        if (ent === "ai" && Array.isArray(planned.data.rules)) await this._rules(jobId, item, planned, item.entityId);
      }
      item = this.journal.get(jobId).items[item.idx];
      if (item.state === "CONFIRMED") await this._verifyOrSkip(jobId, item, planned, manifest);
    } catch (e) {
      if (e instanceof Paused) throw e;
      // A read refused as unauthenticated, raised from somewhere that has no auth dependency of
      // its own (today: the reconciler's pre-create snapshot). It can only come from a READ, so
      // the item is never SENT because of it and the ambiguity handling below does not apply.
      if (e instanceof AuthRefused) throw this._authRefused(e.error, { idx: item.idx, path: e.path });
      if (e instanceof RateLimited) throw new Paused("TOO_MANY_REQUESTS", { path: e.path, until: e.until, idx: item.idx });
      const cur = this.journal.get(jobId).items[item.idx];
      if (cur.state === "SENT") {
        // thrown inside a withSent thunk: the request may have left. Leave SENT, pause.
        throw new Paused(e instanceof NetworkError ? "NETWORK" : e instanceof TransportError ? "UNDECODABLE_RESPONSE" : "AMBIGUOUS",
          { idx: item.idx, detail: String(e && e.message), httpStatus: e.httpStatus ?? null, received: e.received ?? null });
      }
      if (isTransport(e)) {
        // a read failed on the wire; nothing was sent for this item. Pause, keep the item.
        throw new Paused("NETWORK", { idx: item.idx, detail: String(e && e.message), httpStatus: e.httpStatus ?? null });
      }
      // an ordinary failure before or after a send: this item fails, the job continues
      this.journal.transition(jobId, item.idx, "FAILED", { error: String(e && e.message ? e.message : e) });
      this.log(`item ${item.idx} failed: ${e && e.message}`, item);
    }
  }

  /** Local checks before a create: refs resolvable, files picked, keys known. No request. */
  async _preflight(item, planned) {
    const refs = collectRefs(planned.data);
    for (const r of refs) {
      if (r.pfx === "DOUBLED") throw new Error(`doubled ref prefix at ${r.path}: ${r.key}`);
      if (r.pfx === "img") { this._imgPreflight(r.key); continue; }
      if (!this._lookup(this.journal.get(this._jobOf(item)))(r.pfx, r.key)) throw new Error(`@${r.pfx}:${r.key} is not resolvable yet (at ${r.path})`);
    }
    const problems = this.validator.problems(item.entity, planned.data, null, { preCreate: true });
    if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
  }

  /**
   * One `@img` ref, before anything is sent. A pack-backed image is satisfied ONLY by its verified
   * bytes or by an upload of exactly those bytes; the name-keyed idmap is deliberately not consulted
   * for it, because `tnr_bk_idmap_v1` maps a FILENAME to a URL and two different files have carried
   * the same logical name across manifests. Reusing that URL would ship the previous image behind
   * the new manifest's provenance, which is the one outcome a content-bound pack must make
   * impossible. A picked (unbound) image keeps the historical behaviour exactly.
   */
  _imgPreflight(name) {
    const prov = this.imgProvenance.get(name);
    if (prov) {
      // A recorded upload of this exact content needs no local file at all.
      if (readAssetUploads(this.storage)[prov.sha256]) return;
      const file = this.files.get(name);
      if (!file) throw new Error(`@img:${name} is bound to ${prov.path} but its verified bytes are not loaded`);
      // Identity, not size. See _imgBytes() for why a size check is not enough.
      if (file !== prov.file) throw new Error(`@img:${name} is not holding the exact file that was verified against ${prov.sha256.slice(0, 12)}; nothing was sent`);
      return;
    }
    if (!this.files.has(name) && !readIdmap(this.storage)[name]) throw new Error(`@img:${name} has no file picked`);
  }

  /**
   * The bytes of a pack-backed image, re-verified at the moment of upload. This is the LAST barrier
   * and the only one every item passes: `_preflight` runs for creates only, so the five Marrow avatar
   * EDITS that push/53 exists to replay reach the uploader through here and nowhere else.
   *
   * Two checks, and neither is redundant (independent review F1):
   *
   *   identity  the File must be the object `commitImagePack` installed. The gate used to compare
   *             provenance metadata and the file's SIZE, so a different file of identical length
   *             swapped into `files` after verification was uploaded AND recorded in the
   *             content-keyed upload ledger under the correct digest - poisoning every later job
   *             for those bytes with the wrong URL.
   *   digest    re-hashed anyway, immediately before the bytes leave. Identity alone is sound for a
   *             real immutable File/Blob; this does not depend on that being true of whatever
   *             file-like object a host or a future caller supplies. Hashing at most 512 KB (every
   *             upload slug's ceiling) on the item's own send path is not a cost worth trading for
   *             an assumption.
   *
   * Fails closed with no digest wired: repo-backed bytes are never uploaded unverified.
   */
  async _imgBytes(name, prov) {
    const file = this.files.get(name);
    if (!file) throw new Error(`@img:${name} is bound to ${prov.path} but its verified bytes are not loaded`);
    if (file !== prov.file) throw new Error(`@img:${name} is not holding the exact file that was verified against ${prov.sha256.slice(0, 12)}; nothing was uploaded`);
    if (typeof this.digest !== "function") throw new Error(`@img:${name} is repo-backed but no digest is wired, so its bytes cannot be re-verified; nothing was uploaded`);
    const hex = toHex(await this.digest(await file.arrayBuffer()));
    if (hex !== prov.sha256) throw new Error(`@img:${name} hashes to ${hex} at the moment of upload; the pack says ${prov.sha256}. Nothing was uploaded.`);
    return file;
  }

  async _create(jobId, item, planned) {
    const rc = recipe(item.entity);
    if (this.reconciler) {
      const key = await this.reconciler.beforeCreate(this.journal.get(jobId), item, item.entity);
      if (key) this.journal.annotate(jobId, item.idx, { snapshotKey: key });
    }
    const input = rc.create.input(planned.data);
    this._requireAuth(rc.create.path, item.idx);
    const decoded = await this.journal.withSent(jobId, item.idx, { phase: "create" }, () => this.client.call(rc.create.path, input));
    const o = readCreate(decoded);
    if (o.kind === "ok") {
      this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: o.id, phase: "update" });
      this._remember(item.srcId, o.id);
      await this.cache.invalidateEntity(rc.cacheEntity);
      this.log(`created ${item.entity} ${o.id} (placeholder)`, item);
      return;
    }
    this._failFromOutcome(jobId, item, o, "create");
  }

  async _fill(jobId, item, planned) {
    const rc = recipe(item.entity);
    const id = item.entityId ?? item.targetId;
    if (!id) throw new Error("no id to fill");
    const data = await this._resolved(planned.data, jobId);
    this._requireAuth(rc.get, item.idx);
    const live = await this.reader.get(rc.get, id, { fresh: true });
    if (!live.ok) {
      const cls = classifyError(live.error);
      if (cls === "SESSION") throw this._authRefused(live.error, { path: rc.get, idx: item.idx });
      throw new Error(`${rc.get} failed: ${live.error.code} ${live.error.message}`);
    }
    if (live.data == null) throw new Error(`${rc.get} returned no record for ${id}`);
    const problems = this.validator.problems(item.entity, data, live.data);
    if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
    const payload = mergeForUpdate(item.entity, live.data, data, this.validator.knownFields(item.entity));
    this._requireAuth(rc.update, item.idx);
    const decoded = await this.journal.withSent(jobId, item.idx, { phase: "update" }, () => this.client.call(rc.update, { id, data: payload }));
    const o = readMutation(decoded);
    await this.cache.invalidateRecord(rc.cacheEntity, id);
    if (o.kind === "ok") {
      const next = item.entity === "ai" && Array.isArray(planned.data.rules) ? "rules" : "verify";
      this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: id, phase: next, asserted: Object.keys(data) });
      return;
    }
    this._failFromOutcome(jobId, item, o, "update");
  }

  async _rules(jobId, item, planned, userId) {
    const rc = recipe("aiProfile");
    const rules = planned.data.rules ?? [];
    const includeDefaultRules = planned.data.includeDefaultRules !== false;
    if (item.entity === "aiProfile") {
      const problems = this.validator.problems("aiProfile", planned.data, null);
      if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
    }
    this._requireAuth(rc.get, item.idx);
    let live = await this.reader.get(rc.get, userId, { fresh: true });
    // profile.getAi is protectedProcedure. A session that expired since the gate makes this read
    // UNAUTHORIZED, and the generic Error below would turn a sign-in problem into a terminal
    // content failure with the auth state still claiming READY (independent review round 2,
    // surviving path A). Pausing instead leaves the item exactly where it is, which for AI work
    // is CONFIRMED and resumable.
    if (!live.ok && classifyError(live.error) === "SESSION") throw this._authRefused(live.error, { idx: item.idx, path: rc.get });
    if (!live.ok || !live.data) throw new Error(`profile.getAi failed for ${userId}`);
    let apid = live.data.aiProfileId;
    if (!apid) {
      this._requireAuth(rc.profileToggle, item.idx);
      const decoded = await this.journal.withSent(jobId, item.idx, { phase: "rules-toggle", entityId: userId }, () => this.client.call(rc.profileToggle, { aiId: userId }));
      const o = readMutation(decoded);
      if (o.kind !== "ok") { this._failFromOutcome(jobId, item, o, "toggle"); return; }
      this.journal.transition(jobId, item.idx, "CONFIRMED", { phase: "rules" });
      // The worst place to lose the session: the toggle mutation has LANDED, the profile row
      // exists, and only the rules write is left. Failing the item here would strand a
      // half-configured AI that resume() then skips as terminal. The item is already CONFIRMED at
      // phase "rules", so pausing preserves exactly the state a post-sign-in resume needs.
      live = await this.reader.get(rc.get, userId, { fresh: true });
      if (!live.ok && classifyError(live.error) === "SESSION") throw this._authRefused(live.error, { idx: item.idx, path: rc.get });
      apid = live.ok && live.data ? live.data.aiProfileId : null;
      if (!apid) throw new Error("no aiProfileId after toggle");
    }
    this._requireAuth(rc.profileUpdate, item.idx);
    const decoded = await this.journal.withSent(jobId, item.idx, { phase: "rules", entityId: userId, aiProfileId: apid }, () => this.client.call(rc.profileUpdate, { id: apid, rules, includeDefaultRules }));
    const o = readMutation(decoded);
    await this.cache.invalidateEntity("ai");
    if (o.kind === "ok") { this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: userId, phase: "verify", aiProfileId: apid, assertedRules: true }); return; }
    this._failFromOutcome(jobId, item, o, "rules");
  }

  async _verifyOrSkip(jobId, item, planned, manifest) {
    // A written item is ALWAYS read back. readBack:false cannot reach here - parseManifest refuses
    // it on any manifest carrying items - and it used to mark the item VERIFIED{skipped}, which let
    // a manifest opt out of verification and still be counted as verified. Defence in depth: if one
    // ever does reach here, that is a bug, not a licence to call an unread write good.
    if (!manifest.readBack) throw new Error("readBack:false reached item " + item.idx + "; a written item must be read back");
    await this._verify(jobId, item, planned);
  }

  async _verify(jobId, item, planned) {
    const rc = recipe(item.entity);
    const data = await this._resolved(planned.data, jobId);
    const diffs = [];
    if (item.entity !== "aiProfile") {
      this._requireAuth(rc.get, item.idx);
      const live = await this.reader.get(rc.get, item.entityId, { fresh: true });
      // An expired session must not be recorded as "we read it back and could not see it". The
      // write is real and unverified either way, but the operator is told which problem it is.
      if (!live.ok && classifyError(live.error) === "SESSION") throw this._authRefused(live.error, { idx: item.idx, path: rc.get });
      if (!live.ok || !live.data) { this.journal.annotate(jobId, item.idx, { verify: "unread", phase: "verify" }); return; }
      diffs.push(...diffAsserted(item.entity, data, live.data));
    }
    if ((item.entity === "ai" && Array.isArray(planned.data.rules)) || item.entity === "aiProfile") {
      if (!item.aiProfileId) { this.journal.annotate(jobId, item.idx, { verify: "unread", phase: "verify" }); return; }
      this._requireAuth("ai.getAiProfile", item.idx);
      const pr = await this.reader.get("ai.getAiProfile", item.aiProfileId, { fresh: true });
      if (!pr.ok && classifyError(pr.error) === "SESSION") throw this._authRefused(pr.error, { idx: item.idx, path: "ai.getAiProfile" });
      if (pr.ok && pr.data) {
        // Structural, not textual. The server re-emits the rules in schema key order, so a
        // stringify comparison here reported every landed Godstorm AI-profile write as drift
        // while the two payloads were the same document (deepEqualPayload, validate.mjs).
        if (!deepEqualPayload(planned.data.rules ?? [], pr.data.rules ?? [])) diffs.push({ key: "rules", sent: planned.data.rules, live: pr.data.rules });
        if (planned.data.includeDefaultRules !== undefined && pr.data.includeDefaultRules !== planned.data.includeDefaultRules) diffs.push({ key: "includeDefaultRules", sent: planned.data.includeDefaultRules, live: pr.data.includeDefaultRules });
      } else { this.journal.annotate(jobId, item.idx, { verify: "unread", phase: "verify" }); return; }
    }
    if (diffs.length) this.journal.annotate(jobId, item.idx, { diffs, verify: "drift", phase: "verify" });
    else this.journal.transition(jobId, item.idx, "VERIFIED", { diffs: [], verify: "match" });
  }

  /**
   * dedupNames: refuse to create a row whose name is already live (readiness brief 5b).
   *
   * Runs BEFORE the first create of the job, through the cache-first reader under the budget, so
   * a collision fails while the only cost is a read. Only PLANNED creates are checked: an item
   * this job already created owns its live name, and re-checking it would collide with itself.
   * Only creates at all - an edit that re-asserts its own name would always match the live list,
   * which is why the old builder's version could not be run over an edit manifest.
   *
   * A limited or failed read is NOT silently skipped the way the builder skipped it: RateLimited
   * and transport errors propagate to run(), which pauses the job with the path and countdown, so
   * the check is either performed or the job stops. A collision fails that item only; the rest of
   * the manifest still runs, and the job's outcome reports the failure.
   */
  async _dedupNames(jobId, order) {
    const byEntity = new Map();
    for (const it of this.journal.get(jobId).items) {
      if (it.op !== "create" || it.state !== "PLANNED") continue;
      const rc = recipe(it.entity);
      if (!rc.names) continue;
      const planned = order[it.idx];
      const name = planned && planned.data ? planned.data[rc.nameKey] ?? it.name : it.name;
      if (typeof name !== "string" || !name.trim()) continue;
      if (!byEntity.has(it.entity)) byEntity.set(it.entity, []);
      byEntity.get(it.entity).push({ idx: it.idx, name: name.trim() });
    }
    for (const [entity, entries] of byEntity) {
      const rc = recipe(entity);
      const r = await this.reader.list(rc.names, { fresh: true });
      if (!r.ok) {
        const cls = classifyError(r.error);
        if (cls === "SESSION") throw this._authRefused(r.error, { path: rc.names });
        throw new Paused("NETWORK", { detail: `dedupNames: ${rc.names} failed: ${r.error.code} ${r.error.message}` });
      }
      const rows = Array.isArray(r.data) ? r.data : (r.data && Array.isArray(r.data.data) ? r.data.data : []);
      const live = new Set();
      for (const row of rows) {
        const v = row && (row[rc.nameKey] ?? row.name ?? row.username);
        if (typeof v === "string") live.add(v.trim().toLowerCase());
      }
      for (const e of entries) {
        if (!live.has(e.name.toLowerCase())) continue;
        this.journal.transition(jobId, e.idx, "FAILED", { error: `dedupNames: LIVE NAME COLLISION "${e.name}" already exists as a ${entity}; rename before pushing` });
        this.log(`item ${e.idx} failed: live name collision "${e.name}"`);
      }
    }
  }

  /**
   * One capture pass. Reads are already incremental: the loop starts at out.length, and each
   * answer is journaled before the next read, so a pause after N captures resumes at N+1 and
   * never re-reads what is done. That is unchanged by persistence — `persist: "full"` adds no
   * second read, it only decides how durably the body that read already produced is kept.
   *
   * The journal entry stays COMPACT whatever the mode: the body goes to IndexedDB and the journal
   * carries only the persistence request, the immutable snapshot key that finds that body, and
   * whether it was actually stored. The exporter materializes from that key
   * (App.resolveCaptures); nothing here puts a body in localStorage.
   */
  async _captures(jobId, list, phase) {
    const key = phase === "before" ? "capturesBefore" : "capturesAfter";
    const job = this.journal.get(jobId);
    const out = Array.isArray(job[key + "Partial"]) ? job[key + "Partial"] : [];
    for (let i = out.length; i < list.length; i++) {
      const c = list[i];
      const path = c.proc || c.procedure;
      const id = c.id ?? (c.input && (c.input.id ?? c.input.userId));
      this._requireAuth(path, null);
      // The read mode is the registry's, decided at parse: a point read of one record, an
      // input-free name list, or a filtered/paged query. RateLimited/Network propagate to run().
      let r;
      try {
        r = c.mode === "query"
          ? await this.reader.query(path, c.input, { fresh: true, pages: c.pages })
          : c.mode === "point"
            ? await this.reader.get(path, id, { fresh: true })
            : await this.reader.list(path, { fresh: true });
      } catch (e) {
        // A rate limit or a transport failure pauses the job, and the pass will resume AT THIS
        // capture and read it again. The attempt that was abandoned still happened, so its per-page
        // evidence is journaled first, appended to a list that is never rewritten - a resumed
        // attempt is a new record beside it, not an overwrite of it (independent review FN5).
        if (Array.isArray(e.pages) && e.pages.length) this._journalAttempt(jobId, key, c, phase, i, e);
        throw e;
      }
      // THE OBSERVED DEFECT (harvests/inbox/tnr_results_17890671*.json): five protected reads
      // came back UNAUTHORIZED, each was journaled as an ordinary failed read, the pass ran to
      // the end and the job reported "0/5 full bodies persisted · read failed". That reads as a
      // capture problem. It is an authentication problem, and it stops the pass here so the
      // remaining reads are not spent proving the same thing four more times.
      if (!r.ok && classifyError(r.error) === "SESSION") throw this._authRefused(r.error, { path, phase, ordinal: i });
      // `input` is the CANONICAL input — the exact object that went on the wire, not the shape the
      // manifest happened to write it in (requirement 7.4). For a paged walk the per-page inputs are
      // journaled too, so "what was asked for" is recoverable page by page.
      // The policy that admitted this read is stamped on EVERY research record, before the entry
      // splits into a summary, a persisted or an abandoned one. Stamping it only where a body was
      // kept left ordinary summary captures unable to name the contract they ran under, which
      // brief section 6 requires of every research capture (re-review FN4-R2).
      const entry = { phase, proc: path, policy: capturePolicy(path), input: c.input ?? null, ok: r.ok, rows: Array.isArray(r.data) ? r.data.length : r.data ? 1 : 0, error: r.ok ? null : r.error.code };
      if (c.mode === "query") {
        entry.pages = r.pages;
        // A walk that stopped on its page bound with a full page in hand has more data behind it.
        // Saying so here is what keeps a bounded read from being read later as a whole answer.
        entry.complete = r.complete;
        entry.rows = r.rowCount ?? entry.rows;
        if (r.bounded) entry.bounded = r.bounded;
      }
      if (c.tier) Object.assign(entry, await this._persist(jobId, phase, i, c, path, id, r));
      out.push(entry);
      this.journal.annotateJob(jobId, { [key + "Partial"]: out }); // persisted incrementally
    }
    this.journal.annotateJob(jobId, { [key]: out, [key + "Partial"]: null });
    return out;
  }

  /**
   * Commit ONE capture's body to the immutable snapshot store at its declared TIER, and return the
   * compact verdict fields the journal keeps.
   *
   * The body written is `r.data` — the value this very read returned — so the snapshot cannot be
   * anything other than the body of the read it belongs to. It is deliberately NOT fetched back out
   * of the read cache: that slot is overwritten by the next read of the same key and dropped by a
   * write to its entity, which is exactly how a capture.before body could be replaced by the after
   * body before export (independent review FFC-1).
   *
   * The tier is written ONTO the snapshot rather than re-derived at export. A body that was read
   * under local-only stays local-only for its whole life, whatever a later registry edit says, and
   * the exporter never has to ask a second authority what it is allowed to do with what it holds.
   *
   * Writing here rather than at export also means every check happens at read time — the byte
   * ceiling, the projection, a storage refusal — so a failure shows on the run screen instead of
   * surprising the exporter. A failed read stores nothing and fabricates nothing.
   */
  async _persist(jobId, phase, ordinal, c, path, id, r) {
    const tier = c.tier;
    // The policy that admitted this read, stamped at the moment it is taken: the source pin the row
    // was audited at and the immutable content identity of the registry that admitted it. Recorded
    // here rather than derived at export, so an old capture materialized under a newer build keeps
    // the provenance it was actually taken under (brief section 6, independent review FN4).
    const policy = capturePolicy(path);
    const fields = { persist: c.persist, tier, policy, snapshotKey: snapshotKey(jobId, phase, ordinal), persistOk: false, persistError: null };
    if (tier === "projected") fields.projection = c.projection;
    if (!r.ok) { fields.persistError = "read failed; there is no body to persist"; return fields; }
    // A bounded or partial walk is not a body: persisting it would present part of an answer under
    // a verdict that says the capture succeeded. It is recorded as the non-success it is.
    if (c.mode === "query" && r.complete === false) {
      fields.persistError = `the paged walk did not complete (${r.bounded || "a page was not read"}), so this is a partial result and is NOT persisted as a whole body`;
      return fields;
    }
    const bytes = JSON.stringify(r.data ?? null).length;
    fields.bytes = bytes;
    const ceiling = tierCeiling(tier);
    // Over the ceiling is an explicit failure, and nothing is stored. Truncating and still calling
    // it a persisted body is the one thing this must never do, so there is no shortening path here.
    if (bytes > ceiling) {
      fields.persistError = `body is ${bytes} bytes, over the ${ceiling}-byte ${tier} capture ceiling; it is NOT truncated and NOT persisted`;
      return fields;
    }
    // The projection is computed with the body in hand so a missing declared path is reported by
    // the run that read it, not discovered at export. The RAW body is what gets stored — projection
    // is applied again at export from the same declaration, so there is exactly one projected value
    // and it is derived, never a second copy that could drift from the evidence it came from.
    if (tier === "projected") {
      const pr = projectBody(r.data, c.projection);
      fields.projectOk = pr.ok;
      if (!pr.ok) {
        fields.projectMissing = pr.missing;
        fields.persistError = `projection failed: ${pr.missing.join(", ")} ${pr.missing.length === 1 ? "is" : "are"} absent from the body. The full body is NOT substituted and NOT exported`;
        // The raw body is still retained locally: it is the evidence that the declared projection
        // was wrong, and it is local-only by tier, so retaining it exports nothing.
      }
    }
    try {
      await this.cache.putSnapshot({
        key: fields.snapshotKey, jobId, phase, ordinal, path, id,
        input: c.input ?? null, data: r.data, tier, policy,
        projection: c.projection, page: c.mode === "query" ? { pages: r.pages, complete: r.complete } : null,
      });
    } catch (e) {
      fields.persistError = "capture snapshot write failed: " + (e && e.message ? e.message : String(e));
      return fields;
    }
    // A projection failure is a persistence failure even though the write succeeded: the capture did
    // not produce the evidence the manifest asked for, and no later step may upgrade it.
    fields.persistOk = fields.persistError == null;
    return fields;
  }

  /**
   * Record ONE abandoned capture attempt. Appended to `<phase>Attempts`, which is append-only: a
   * capture that is paused and later resumed leaves both records, so "what was asked for and what
   * came back" survives for the attempt that did not finish. It is deliberately NOT written into
   * the phase's completed list, because that list is the resume cursor and adding to it would skip
   * the capture on resume.
   */
  _journalAttempt(jobId, key, c, phase, ordinal, e) {
    const job = this.journal.get(jobId);
    const prior = Array.isArray(job[key + "Attempts"]) ? job[key + "Attempts"] : [];
    this.journal.annotateJob(jobId, {
      [key + "Attempts"]: [...prior, {
        phase, ordinal, proc: c.proc, policy: capturePolicy(c.proc),
        input: c.input ?? null, persist: c.persist, tier: c.tier,
        abandoned: true, ok: false, complete: false,
        rows: typeof e.rowCount === "number" ? e.rowCount : 0,
        error: e.name === "RateLimited" ? "TOO_MANY_REQUESTS" : e.name || "ERROR",
        pages: e.pages,
        persistOk: false,
        persistError: `the walk stopped on ${e.name === "RateLimited" ? "a rate limit" : "a transport failure"} after ${e.pages.length} page(s); this attempt is incomplete and no body was persisted from it`,
      }],
    });
  }

  // ------------------------------------------------------------------ helpers
  _m(jobId) { const m = this.manifests.get(jobId); if (!m) throw new Error("no manifest attached for job " + jobId + "; call plan() or attach()"); return m; }
  _jobOf(item) { for (const [jobId, m] of this.manifests) if (m.order.some((o) => o === item || (o.idx === item.idx && this.journal.get(jobId)?.items[item.idx]?.srcId === item.srcId))) return jobId; return null; }

  _pause(jobId, reason, info) {
    this._emit("job:paused", { jobId, reason, path: info.path ?? null, idx: info.idx ?? null });
    this.journal.setJobState(jobId, "PAUSED", { pause: { reason, path: info.path ?? null, until: info.until ?? null, idx: info.idx ?? null, detail: info.detail ?? null, httpStatus: info.httpStatus ?? null, authState: info.authState ?? null, authRefused: info.authRefused ?? false } });
    this._releaseLease(jobId);
    this.log(`paused: ${reason}${info.path ? " on " + info.path : ""}`);
    return this.summary(jobId);
  }

  _failFromOutcome(jobId, item, o, step) {
    if (o.kind === "refused") { this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} refused: ${o.message}` }); return; }
    const cls = classifyError(o.error);
    if (cls === "SESSION") {
      // The server DECODED this element and refused it. That is a clean, complete answer: the
      // resolver never ran, so nothing was written, and leaving the item SENT would hand a
      // definite refusal to reconciliation as if the write might exist (brief section E). The
      // item fails here, with the reason named as authentication, and then the job pauses so
      // nothing after it is attempted against the same dead session.
      this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} SESSION: ${o.error.message}`, authRefused: true });
      this.log(`item ${item.idx} refused by the game as unauthenticated on ${step}`, item);
      throw this._authRefused(o.error, { idx: item.idx, authRefused: true });
    }
    const issues = o.error.zodError ? " " + o.error.zodError.map((z) => `${(z.path || []).join(".")}: ${z.message}`).join("; ") : "";
    this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} ${cls}: ${o.error.message}${issues}`, zodError: o.error.zodError ?? null });
  }

  _remember(srcId, id) {
    if (!srcId || !id) return;
    const map = readIdmap(this.storage); map[srcId] = id; writeIdmap(this.storage, map);
  }

  /** Re-derive idmap entries from the job's own items, so a crash between CONFIRMED and the idmap write cannot strand a @ref. */
  _syncIdmapFromJob(job) {
    let map = null;
    for (const it of job.items) if (it.srcId && it.entityId) { map = map ?? readIdmap(this.storage); if (map[it.srcId] !== it.entityId) map[it.srcId] = it.entityId; }
    if (map) writeIdmap(this.storage, map);
  }

  /** Ref lookup: idmap first, then this job's own items by srcId. */
  _lookup(job) {
    const map = readIdmap(this.storage);
    return (pfx, key) => map[key] ?? (job ? job.items.find((it) => it.srcId === key && it.entityId)?.entityId : undefined);
  }

  async _resolved(data, jobId) {
    // upload any @img refs first
    const refs = collectRefs(data).filter((r) => r.pfx === "img");
    for (const r of refs) {
      const prov = this.imgProvenance.get(r.key) ?? null;
      const map = readIdmap(this.storage);
      let file;
      if (prov) {
        // Reuse is decided by CONTENT, not by filename: a recorded upload of this exact digest is
        // the same image, and nothing else is. The idmap is still written so resolveRefs() can
        // substitute the URL, but it is never read as permission to skip the upload.
        const known = readAssetUploads(this.storage)[prov.sha256];
        if (known && known.url) {
          if (map[r.key] !== known.url) { map[r.key] = known.url; writeIdmap(this.storage, map); }
          continue;
        }
        // Re-verified here, not trusted from the preparation that ran before the operator tapped.
        file = await this._imgBytes(r.key, prov);
      } else {
        if (map[r.key]) continue;
        file = this.files.get(r.key);
        if (!file) throw new Error(`@img:${r.key} has no file picked`);
      }
      if (!this.uploader) throw new Error("no uploader configured for @img refs");
      const up = await this.uploader.upload(file);
      map[r.key] = up.ufsUrl; writeIdmap(this.storage, map);
      if (prov) recordAssetUpload(this.storage, prov.sha256, up.ufsUrl, { path: prov.path, ref: prov.ref, at: this.clock() });
    }
    const job = jobId ? this.journal.get(jobId) : null;
    const { value, unresolved } = resolveRefs(data, this._lookup(job));
    if (unresolved.length) throw new Error("unresolved refs: " + unresolved.map((u) => `@${u.pfx}:${u.key} at ${u.path}`).join(", "));
    return value;
  }
}
