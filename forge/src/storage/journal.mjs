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
// create would double-create.

export const JOURNAL_VERSION = 1;
export const KEY_PREFIX = "tnr_forge_job_v1:";

export const ITEM_STATES = Object.freeze([
  "PLANNED", "SENT", "CONFIRMED", "VERIFIED", "FAILED", "ORPHANED", "SKIPPED",
]);
export const TERMINAL_ITEM_STATES = Object.freeze(["VERIFIED", "FAILED", "SKIPPED"]);
export const JOB_STATES = Object.freeze(["RUNNING", "PAUSED", "DONE", "ABORTED"]);

// Legal item transitions. Anything not listed throws. SENT -> PLANNED is deliberately
// absent; that absence is the write-ahead guarantee made structural.
const TRANSITIONS = Object.freeze({
  PLANNED:   ["SENT", "FAILED", "SKIPPED"],
  SENT:      ["CONFIRMED", "ORPHANED", "FAILED"],
  CONFIRMED: ["SENT", "VERIFIED", "FAILED"], // SENT again only for phase 2 of a two-phase create
  VERIFIED:  [],
  FAILED:    [],
  ORPHANED:  ["CONFIRMED", "FAILED", "SKIPPED"], // CONFIRMED = adopted by the user
  SKIPPED:   [],
});

export class JournalError extends Error {
  constructor(message, info) { super(message); this.name = "JournalError"; this.info = info; }
}

function nowIso(clock) { return new Date(clock()).toISOString(); }

export function newItem(idx, spec) {
  return {
    idx,
    entity: spec.entity,
    op: spec.op,                   // "create" | "update"
    name: spec.name ?? null,       // display only
    srcId: spec.srcId ?? null,     // manifest key for @refs
    targetId: spec.targetId ?? null,
    payloadHash: spec.payloadHash,
    state: "PLANNED",
    phase: spec.op === "create" ? "create" : "update", // two-phase create: "create" then "update"
    entityId: spec.targetId ?? null,
    snapshotKey: null,
    sentAt: null,
    confirmedAt: null,
    verifiedAt: null,
    error: null,
  };
}

export class Journal {
  /**
   * @param {Storage} storage  a localStorage-compatible object
   * @param {() => number} clock  epoch ms; injectable so tests are deterministic
   */
  constructor(storage, clock = () => Date.now()) {
    if (!storage || typeof storage.setItem !== "function") {
      throw new JournalError("Journal needs a Storage-like object");
    }
    this.storage = storage;
    this.clock = clock;
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
      throw new JournalError("journal record is not JSON: " + jobId, { jobId, cause: e });
    }
    return migrate(job);
  }

  // ------------------------------------------------------------------ jobs
  listJobIds() {
    const ids = [];
    for (let i = 0; i < this.storage.length; i++) {
      const k = this.storage.key(i);
      if (k && k.startsWith(KEY_PREFIX)) ids.push(k.slice(KEY_PREFIX.length));
    }
    return ids;
  }

  listJobs() {
    return this.listJobIds().map((id) => this._read(id)).filter(Boolean)
      .sort((a, b) => (a.startedAt < b.startedAt ? 1 : -1));
  }

  get(jobId) { return this._read(jobId); }

  /**
   * Open a new job. items are specs: {entity, op, name, srcId, targetId, payloadHash}.
   */
  open({ jobId, manifestPath, manifestNumber, manifestHash, items }) {
    if (!jobId) throw new JournalError("jobId required");
    if (this._read(jobId)) throw new JournalError("job already exists: " + jobId, { jobId });
    const job = {
      v: JOURNAL_VERSION,
      jobId,
      manifestPath: manifestPath ?? null,
      manifestNumber: manifestNumber ?? null,
      manifestHash: manifestHash ?? null,
      startedAt: nowIso(this.clock),
      updatedAt: null,
      state: "RUNNING",
      pause: null, // { reason, path, until } when PAUSED
      items: items.map((spec, i) => newItem(i, spec)),
    };
    return this._write(job);
  }

  setJobState(jobId, state, extra = {}) {
    if (!JOB_STATES.includes(state)) throw new JournalError("bad job state: " + state);
    const job = this._mustRead(jobId);
    job.state = state;
    job.pause = state === "PAUSED" ? (extra.pause ?? job.pause ?? null) : null;
    return this._write(job);
  }

  remove(jobId) { this.storage.removeItem(this._key(jobId)); }

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
    Object.assign(item, patch);
    item.state = to;
    const at = nowIso(this.clock);
    if (to === "SENT") item.sentAt = at;
    if (to === "CONFIRMED") item.confirmedAt = at;
    if (to === "VERIFIED") item.verifiedAt = at;
    return this._write(job);
  }

  /**
   * The write-ahead primitive. Flush SENT to disk, THEN run the thunk that issues the request.
   * The thunk cannot run before the flush because it is only invoked after _write returns.
   * If the flush throws, the thunk never runs and nothing left the device.
   *
   * @returns {Promise<any>} whatever the thunk resolves to
   */
  async withSent(jobId, idx, patch, thunk) {
    if (typeof patch === "function") { thunk = patch; patch = {}; }
    this.transition(jobId, idx, "SENT", patch); // synchronous flush
    return await thunk();
  }

  /** Set a field on an item without a state change. Still flushes. */
  annotate(jobId, idx, patch) {
    const job = this._mustRead(jobId);
    const item = job.items[idx];
    if (!item) throw new JournalError("no such item: " + idx, { jobId, idx });
    Object.assign(item, patch);
    return this._write(job);
  }

  // ------------------------------------------------------------------ resume
  /** Jobs that have any item not in a terminal state, or that are PAUSED. */
  resumable() {
    return this.listJobs().filter((job) =>
      job.state === "PAUSED" || job.items.some((it) => !TERMINAL_ITEM_STATES.includes(it.state)));
  }

  /** Items in SENT. These are ambiguous and must go through reconciliation, never retried. */
  ambiguous(jobId) {
    return this._mustRead(jobId).items.filter((it) => it.state === "SENT");
  }

  // ------------------------------------------------------------------ export
  exportText() {
    return JSON.stringify({ exportedAt: nowIso(this.clock), version: JOURNAL_VERSION, jobs: this.listJobs() }, null, 1);
  }
}

// ------------------------------------------------------------------ migrations
// Chain from job.v to JOURNAL_VERSION. Each step is (job) => job. When a v2 lands, add
// MIGRATIONS[1] = (job) => {...; job.v = 2; return job}.
const MIGRATIONS = {};

export function migrate(job) {
  let v = job.v ?? 1;
  while (v < JOURNAL_VERSION) {
    const step = MIGRATIONS[v];
    if (!step) throw new JournalError("no migration from journal v" + v);
    job = step(job);
    v = job.v;
  }
  return job;
}
