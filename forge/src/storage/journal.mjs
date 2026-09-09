// The journal. localStorage, synchronous, write-ahead.
//
// Why localStorage and not IndexedDB (spec section 3): setItem is synchronous, so a record
// committed before a fetch is on disk before the request leaves. IndexedDB commits
// asynchronously and can lose the write in exactly the eviction window that matters.
//
// One key per job. The job list is derived by scanning keys with the prefix, so there is no
// separate index that can disagree with the jobs themselves.
//
// The single invariant this file exists to hold: an item in SENT is never returned to
// PLANNED. A SENT item may only become CONFIRMED (the response arrived, or reconciliation
// adopted an orphan), ORPHANED (reconciliation found no match), or FAILED. Retrying a SENT
// create would double-create. Two guards make this structural: SENT -> PLANNED is absent
// from TRANSITIONS, and annotate() refuses to touch state or the timestamps.
//
// Honesty note (adversarial review L1): on Firefox, setItem is synchronous in the content
// process; the disk write is an IPC to the parent that follows shortly after. withSent()
// yields one macrotask between the flush and the request so that IPC is queued before the
// fetch is issued. This narrows the window; it does not make the flush a fsync.

export const JOURNAL_VERSION = 1;
export const KEY_PREFIX = "tnr_forge_job_v1:";
export const MAX_TEXT = 512; // cap on error strings so one long message cannot blow the record

export const ITEM_STATES = Object.freeze([
  "PLANNED", "SENT", "CONFIRMED", "VERIFIED", "FAILED", "ORPHANED", "SKIPPED",
]);
export const TERMINAL_ITEM_STATES = Object.freeze(["VERIFIED", "FAILED", "SKIPPED"]);
// INCOMPLETE: execution finished, but at least one item is not terminal - a read-back that could
// not be read (verify "unread") or came back different (verify "drift") leaves its item CONFIRMED
// at phase "verify". Such a job is NOT a success and is still resumable, and resuming it can only
// re-read: the phase recorded on CONFIRMED is "verify", so no mutation can be sent again. Keeping
// it out of DONE is what stops "the job finished" from being read as "the writes are verified".
export const JOB_STATES = Object.freeze(["RUNNING", "PAUSED", "DONE", "INCOMPLETE", "ABORTED"]);
export const OPS = Object.freeze(["create", "update"]);

// Legal item transitions. Anything not listed throws. SENT -> PLANNED is deliberately
// absent; that absence is the write-ahead guarantee made structural.
export const TRANSITIONS = Object.freeze({
  PLANNED:   ["SENT", "FAILED", "SKIPPED"],
  SENT:      ["CONFIRMED", "ORPHANED", "FAILED"],
  CONFIRMED: ["SENT", "VERIFIED", "FAILED"], // SENT again only for a later phase of the same item
  VERIFIED:  [],
  FAILED:    [],
  ORPHANED:  ["CONFIRMED", "FAILED", "SKIPPED"], // CONFIRMED = adopted by the user
  SKIPPED:   [],
});
// Keys only transition() may write. annotate() refuses them.
const RESERVED = Object.freeze(["state", "idx", "sentAt", "confirmedAt", "verifiedAt", "createSentAt"]);

/**
 * What a job actually achieved, for the UI, the summary and the exported bundle. The job STATE
 * says whether execution is finished; the outcome says whether it is good news. They are separate
 * because "the run stopped" and "every write is verified against the server" are separate claims,
 * and the second one is the only one that may ever be shown as success (TNR doctrine: a push echo
 * is not a read-back).
 *
 *   success      every item VERIFIED with its asserted keys read back equal
 *   failed       at least one item FAILED (execution-terminal, but not good news)
 *   unverified   nothing failed, but at least one write is unproven: drift, unread, a skipped
 *                orphan, or an item execution never resolved
 *   open         still running or paused; the question is not answered yet
 */
export function jobOutcome(job) {
  if (!job || !Array.isArray(job.items)) return "open";
  if (job.state === "RUNNING" || job.state === "PAUSED") return "open";
  if (!job.items.length) {
    const captures = [...(job.capturesBefore || []), ...(job.capturesAfter || [])];
    if (!captures.length) return "unverified";
    return captures.every((capture) => capture && capture.ok === true) ? "success" : "failed";
  }
  if (job.items.some((it) => it.state === "FAILED")) return "failed";
  if (job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state) || it.state === "SKIPPED" || (it.verify && it.verify !== "match"))) return "unverified";
  return "success";
}

export class JournalError extends Error {
  constructor(message, info) { super(message); this.name = "JournalError"; this.info = info; }
}

function nowIso(clock) { return new Date(clock()).toISOString(); }
function capText(v) { return typeof v === "string" && v.length > MAX_TEXT ? v.slice(0, MAX_TEXT - 1) + "…" : v; }
function capPatch(patch) {
  const out = {};
  for (const [k, v] of Object.entries(patch || {})) out[k] = capText(v);
  return out;
}

export function newItem(idx, spec) {
  if (!spec || typeof spec !== "object") throw new JournalError("item spec must be an object", { idx });
  if (!OPS.includes(spec.op)) throw new JournalError(`item ${idx}: op must be create or update, got ${spec.op}`, { idx });
  if (typeof spec.entity !== "string" || !spec.entity) throw new JournalError(`item ${idx}: entity required`, { idx });
  return {
    idx,
    entity: spec.entity,
    op: spec.op,
    name: spec.name ?? null,
    srcId: spec.srcId ?? null,
    targetId: spec.targetId ?? null,
    payloadHash: spec.payloadHash ?? null,
    state: "PLANNED",
    phase: spec.op === "create" ? "create" : "update",
    entityId: spec.targetId ?? null,
    snapshotKey: null,
    sentAt: null,        // the LAST send of this item
    createSentAt: null,  // the create-phase send, never overwritten
    confirmedAt: null,
    verifiedAt: null,
    error: null,
  };
}

/**
 * Persisted history outranks a persisted state label. A record can be hand-edited, truncated by
 * a partial flush, or written by a future bundle; shape validation alone cannot see that an item
 * labelled PLANNED already carries proof that its request left (sentAt / createSentAt /
 * confirmedAt / verifiedAt). Replaying such an item would mint a SECOND live row, because every
 * create at the pin generates a fresh nanoid (jutsu.ts:391, item.ts:235, bloodline.ts:144,
 * asset.ts:194, quests.ts:866, profile.ts:1138). Restore it to SENT, which is the only state that
 * routes through reconciliation, and record why. Never the reverse: this function never advances
 * an item towards a terminal state and never invents an entityId.
 */
export function repairHistory(job) {
  if (!job || !Array.isArray(job.items)) return job;
  for (const it of job.items) {
    if (!it || typeof it !== "object" || it.state !== "PLANNED") continue;
    const proof = ["sentAt", "createSentAt", "confirmedAt", "verifiedAt"].filter((k) => it[k]);
    if (!proof.length) continue;
    it.state = "SENT";
    if (it.createSentAt && !it.entityId) it.phase = "create";
    else if (!it.phase || it.phase === "create") it.phase = it.entityId ? "update" : "create";
    it.sentAt = it.sentAt || it.createSentAt || it.confirmedAt || it.verifiedAt;
    it.repaired = `state PLANNED contradicted by ${proof.join(", ")}; restored to SENT for reconciliation`;
  }
  return job;
}

export function validateJobShape(job) {
  if (!job || typeof job !== "object" || Array.isArray(job)) throw new JournalError("journal record is not an object");
  if (typeof job.jobId !== "string" || !job.jobId) throw new JournalError("journal record has no jobId");
  if (!Array.isArray(job.items)) throw new JournalError("journal record has no items array", { jobId: job.jobId });
  if (!JOB_STATES.includes(job.state)) throw new JournalError("journal record has unknown job state " + job.state, { jobId: job.jobId });
  job.items.forEach((it, i) => {
    if (!it || typeof it !== "object") throw new JournalError(`item ${i} is not an object`, { jobId: job.jobId });
    if (!ITEM_STATES.includes(it.state)) throw new JournalError(`item ${i} has unknown state ${it.state}`, { jobId: job.jobId });
    if (it.idx !== i) throw new JournalError(`item ${i} has idx ${it.idx}`, { jobId: job.jobId });
  });
  return job;
}

export class Journal {
  /**
   * @param {Storage} storage  a localStorage-compatible object
   * @param {() => number} clock  epoch ms; injectable so tests are deterministic
   * @param {object} [opts]
   * @param {() => Promise<void>} [opts.yieldTask]  awaited between the SENT flush and the request
   */
  constructor(storage, clock = () => Date.now(), { yieldTask = () => new Promise((r) => setTimeout(r, 0)) } = {}) {
    if (!storage || typeof storage.setItem !== "function") {
      throw new JournalError("Journal needs a Storage-like object");
    }
    this.storage = storage;
    this.clock = clock;
    this.yieldTask = yieldTask;
  }

  // ------------------------------------------------------------------ persistence
  _key(jobId) { return KEY_PREFIX + jobId; }

  _write(job) {
    job.v = JOURNAL_VERSION;
    job.updatedAt = nowIso(this.clock);
    const text = JSON.stringify(job);
    try {
      this.storage.setItem(this._key(job.jobId), text);
    } catch (e) {
      // QuotaExceededError or a storage that is read-only. Surface it; never swallow, because
      // a swallowed failure here is exactly a lost write-ahead record.
      throw new JournalError("journal write failed: " + (e && e.message ? e.message : String(e)), {
        jobId: job.jobId, bytes: text.length, cause: e,
      });
    }
    return job;
  }

  _read(jobId) {
    const text = this.storage.getItem(this._key(jobId));
    if (text == null) return null;
    let job;
    try { job = JSON.parse(text); } catch (e) {
      throw new JournalError("journal record is not JSON: " + jobId, { jobId, cause: e, raw: text });
    }
    return validateJobShape(migrate(job));
  }

  // ------------------------------------------------------------------ jobs
  listJobIds() {
    const ids = [];
    for (let i = 0; i < this.storage.length; i++) {
      const k = this.storage.key(i);
      if (k && k.startsWith(KEY_PREFIX) && k.length > KEY_PREFIX.length) ids.push(k.slice(KEY_PREFIX.length));
    }
    return ids;
  }

  /**
   * Readable jobs, newest first. A corrupt record never blocks the others: it is collected in
   * this.broken (jobId, error, raw) so the UI can show it and the user can export it.
   */
  listJobs() {
    const jobs = [];
    this.broken = [];
    for (const id of this.listJobIds()) {
      try { const j = this._read(id); if (j) jobs.push(j); }
      catch (e) { this.broken.push({ jobId: id, error: e.message, raw: this.storage.getItem(this._key(id)) }); }
    }
    return jobs.sort((a, b) => String(b.startedAt).localeCompare(String(a.startedAt)) || a.jobId.localeCompare(b.jobId));
  }

  get(jobId) { return this._read(jobId); }

  /**
   * Open a new job. items are specs: {entity, op, name, srcId, targetId, payloadHash}.
   * Refuses when a non-terminal job with the same manifestHash already exists: resume it.
   */
  open({ jobId, manifestPath, manifestNumber, manifestHash, items, allowEmpty = false }) {
    if (!jobId) throw new JournalError("jobId required");
    if (!Array.isArray(items) || (!items.length && !allowEmpty)) throw new JournalError("a job needs at least one item unless it is an explicit capture-only job");
    if (this._read(jobId)) throw new JournalError("job already exists: " + jobId, { jobId });
    if (manifestHash) {
      const dup = this.resumable().find((j) => j.manifestHash === manifestHash);
      if (dup) throw new JournalError(`an open job for this manifest already exists (${dup.jobId}); resume it instead`, { jobId: dup.jobId });
    }
    const job = {
      v: JOURNAL_VERSION,
      jobId,
      manifestPath: manifestPath ?? null,
      manifestNumber: manifestNumber ?? null,
      manifestHash: manifestHash ?? null,
      startedAt: nowIso(this.clock),
      updatedAt: null,
      state: "RUNNING",
      pause: null,
      items: items.map((spec, i) => newItem(i, spec)),
    };
    return this._write(job);
  }

  setJobState(jobId, state, extra = {}) {
    if (!JOB_STATES.includes(state)) throw new JournalError("bad job state: " + state);
    const job = this._mustRead(jobId);
    if ((state === "DONE" || state === "INCOMPLETE") && job.items.some((it) => it.state === "SENT")) throw new JournalError(`cannot mark ${state} with SENT items`, { jobId });
    if (state === "DONE" && job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state))) {
      // DONE is the green terminal state and nothing else may reach it: an item still at
      // CONFIRMED owes a read-back, and a job that finished with one is INCOMPLETE.
      throw new JournalError("cannot mark DONE with unresolved items; use INCOMPLETE", { jobId });
    }
    job.state = state;
    job.pause = state === "PAUSED" ? (extra.pause ?? job.pause ?? { reason: "unspecified" }) : null;
    return this._write(job);
  }

  /** Delete a job record. Refused while any item is SENT (the record that a request left). */
  remove(jobId, { force = false } = {}) {
    const job = this._read(jobId);
    if (job && !force && job.items.some((it) => it.state === "SENT")) {
      throw new JournalError("refusing to delete a job with SENT items; reconcile it first", { jobId });
    }
    this.storage.removeItem(this._key(jobId));
  }

  _mustRead(jobId) {
    const job = this._read(jobId);
    if (!job) throw new JournalError("no such job: " + jobId, { jobId });
    return job;
  }

  // ------------------------------------------------------------------ items
  /**
   * Transition one item. Validates against TRANSITIONS, applies patch, flushes synchronously.
   * Returns the updated job. Throws JournalError on an illegal transition.
   */
  transition(jobId, idx, to, patch = {}) {
    const job = this._mustRead(jobId);
    const item = job.items[idx];
    if (!item) throw new JournalError("no such item: " + idx, { jobId, idx });
    const from = item.state;
    if (!TRANSITIONS[from] || !TRANSITIONS[from].includes(to)) {
      throw new JournalError(`illegal transition ${from} -> ${to}`, { jobId, idx, from, to });
    }
    const p = capPatch(patch);
    for (const k of RESERVED) if (k in p) throw new JournalError(`transition patch may not set ${k}`, { jobId, idx });
    // A second SENT on the same item is only for a later phase: the create must have yielded an id.
    if (from === "CONFIRMED" && to === "SENT") {
      const entityId = p.entityId ?? item.entityId;
      const phase = p.phase ?? item.phase;
      if (!entityId) throw new JournalError("CONFIRMED -> SENT needs an entityId (phase 2 of a create)", { jobId, idx });
      if (phase === "create") throw new JournalError("CONFIRMED -> SENT may not re-enter the create phase", { jobId, idx });
    }
    if (to === "SENT" && job.state !== "RUNNING") throw new JournalError(`cannot send while job is ${job.state}`, { jobId, idx });
    Object.assign(item, p);
    item.state = to;
    const at = nowIso(this.clock);
    if (to === "SENT") { item.sentAt = at; if (item.phase === "create" && !item.createSentAt) item.createSentAt = at; }
    if (to === "CONFIRMED") item.confirmedAt = at;
    if (to === "VERIFIED") item.verifiedAt = at;
    return this._write(job);
  }

  /**
   * The write-ahead primitive. Flush SENT to disk, yield one task so the storage IPC is
   * queued, THEN run the thunk that issues the request. If the flush throws, the thunk never
   * runs and nothing left the device.
   *
   * @returns {Promise<any>} whatever the thunk resolves to
   */
  async withSent(jobId, idx, patch, thunk) {
    if (typeof patch === "function") { thunk = patch; patch = {}; }
    this.transition(jobId, idx, "SENT", patch); // synchronous flush
    await this.yieldTask();
    return await thunk();
  }

  /** Set non-reserved fields on an item without a state change. Still flushes. */
  annotate(jobId, idx, patch) {
    const job = this._mustRead(jobId);
    const item = job.items[idx];
    if (!item) throw new JournalError("no such item: " + idx, { jobId, idx });
    const p = capPatch(patch);
    for (const k of RESERVED) if (k in p) throw new JournalError(`annotate may not set ${k}; use transition()`, { jobId, idx, key: k });
    Object.assign(item, p);
    return this._write(job);
  }

  /** Set job-level fields (captures, notes). Never items or state. */
  annotateJob(jobId, patch) {
    const job = this._mustRead(jobId);
    for (const k of ["items", "state", "jobId", "v"]) if (k in (patch || {})) throw new JournalError("annotateJob may not set " + k, { jobId });
    Object.assign(job, patch);
    return this._write(job);
  }

  // ------------------------------------------------------------------ resume
  /**
   * Jobs that still have work: PAUSED, INCOMPLETE (verification outstanding), or RUNNING with any
   * non-terminal item. DONE/ABORTED never. An INCOMPLETE job is resumable on purpose: re-reading a
   * drifted or unread item is the only way it can ever become DONE, and re-reading is all a resume
   * of it can do.
   */
  resumable() {
    return this.listJobs().filter((job) =>
      job.state === "PAUSED" || job.state === "INCOMPLETE"
      || (job.state === "RUNNING" && job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state))));
  }

  /** Items in SENT. These are ambiguous and must go through reconciliation, never retried. */
  ambiguous(jobId) {
    return this._mustRead(jobId).items.filter((it) => it.state === "SENT");
  }

  /** Every entityId any job in this journal has recorded (for cross-job orphan reconciliation). */
  /**
   * Which item, in ANY job, already holds this entityId. Excludes the caller's own item.
   * Adoption and reconciliation both consult it: two items pointing at one row means the second
   * one's update overwrites the first one's content, and the server keeps no job provenance.
   */
  findHolder(entity, entityId, { exceptJobId = null, exceptIdx = null } = {}) {
    if (!entityId) return null;
    for (const job of this.listJobs()) {
      for (const it of job.items) {
        if (job.jobId === exceptJobId && it.idx === exceptIdx) continue;
        if (it.entityId === entityId && (!entity || it.entity === entity)) return { jobId: job.jobId, idx: it.idx, name: it.name ?? null, state: it.state };
      }
    }
    return null;
  }

  knownEntityIds(entity = null) {
    const ids = new Set();
    for (const job of this.listJobs()) for (const it of job.items) if (it.entityId && (!entity || it.entity === entity)) ids.add(it.entityId);
    return ids;
  }

  // ------------------------------------------------------------------ export
  exportText() {
    const jobs = this.listJobs();
    return JSON.stringify({ exportedAt: nowIso(this.clock), version: JOURNAL_VERSION, jobs, broken: this.broken ?? [] }, null, 1);
  }
}

// ------------------------------------------------------------------ migrations
// Chain from job.v to JOURNAL_VERSION. Each step is (job) => job. When a v2 lands, add
// MIGRATIONS[1] = (job) => {...; job.v = 2; return job}.
const MIGRATIONS = {};

export function migrate(job) {
  if (!job || typeof job !== "object") throw new JournalError("journal record is not an object");
  let v = job.v ?? 1;
  if (!Number.isInteger(v) || v < 1) throw new JournalError("journal record has an invalid version: " + String(job.v));
  if (v > JOURNAL_VERSION) throw new JournalError(`journal v${v} is newer than this bundle (v${JOURNAL_VERSION}); update the app`, { v });
  while (v < JOURNAL_VERSION) {
    const step = MIGRATIONS[v];
    if (!step) throw new JournalError("no migration from journal v" + v);
    job = step(job);
    if (job.v !== v + 1) throw new JournalError("migration did not advance the version");
    v = job.v;
  }
  job.v = v;
  return repairHistory(job);
}
