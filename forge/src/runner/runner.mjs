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
import { NetworkError } from "../transport/client.mjs";
import { TransportError } from "../transport/envelope.mjs";
import { RateLimited } from "../budget/bucket.mjs";
import { readIdmap, writeIdmap } from "../storage/compat.mjs";
import { recipe, mergeForUpdate } from "./recipes.mjs";
import { resolveRefs, collectRefs } from "./refs.mjs";
import { diffAsserted } from "./validate.mjs";
import { parseManifest, planOrder, toJournalSpecs } from "./manifest.mjs";

export class Paused extends Error {
  constructor(reason, info = {}) { super(`paused: ${reason}`); this.name = "Paused"; this.reason = reason; Object.assign(this, info); }
}
const isTransport = (e) => e instanceof NetworkError || e instanceof TransportError;

export class Runner {
  /**
   * @param {object} d  dependencies
   * @param {import("../storage/journal.mjs").Journal} d.journal
   * @param {import("../transport/client.mjs").TrpcClient} d.client
   * @param {import("../budget/reader.mjs").CachedReader} d.reader
   * @param {import("../storage/captures.mjs").CaptureCache} d.cache
   * @param {import("./validate.mjs").Validator} d.validator
   * @param {object} [d.uploader]      {upload(file) -> {ufsUrl}}
   * @param {object} [d.reconciler]    {beforeCreate(job, item, entity), resolveSent(job, item, ctx)}
   * @param {Storage} d.storage        for the retained idmap
   * @param {(msg: string, item?: object) => void} [d.log]
   */
  constructor(d) {
    for (const k of ["journal", "client", "reader", "cache", "validator", "storage"]) if (!d[k]) throw new Error("Runner needs " + k);
    Object.assign(this, d);
    this.log = d.log ?? (() => {});
    this.files = new Map(); // name -> File, from the UI picker
    this.manifests = new Map(); // jobId -> parsed manifest (data lives here, not in the journal)
    this.pauseRequested = false;
  }

  // ------------------------------------------------------------------ lifecycle
  /** Plan a manifest and open a job. Returns the journal job. Does not send anything. */
  plan(manifestSource, { jobId, manifestPath = null, manifestNumber = null } = {}) {
    const manifest = parseManifest(manifestSource);
    const order = planOrder(manifest, readIdmap(this.storage));
    const job = this.journal.open({ jobId, manifestPath, manifestNumber, manifestHash: manifest.hash, items: toJournalSpecs(order) });
    this.manifests.set(jobId, { manifest, order });
    return job;
  }

  /** Attach the parsed manifest to an existing (resumed) job. */
  attach(jobId, manifestSource) {
    const manifest = parseManifest(manifestSource);
    const job = this.journal.get(jobId);
    if (!job) throw new Error("no such job " + jobId);
    if (job.manifestHash && manifest.hash !== job.manifestHash) {
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
    if (job.state === "PAUSED") {
      const t = this.budget && this.budget.log && this.budget.log.tripped();
      if (t) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: t.path, until: t.until });
      job = this.journal.setJobState(jobId, "RUNNING");
    }
    if (job.items.some((it) => it.state === "SENT")) {
      throw new Error("job has SENT items; call resume() so they are reconciled before anything else is sent");
    }
    this._syncIdmapFromJob(job);
    this.pauseRequested = false;
    try {
      if (manifest.capture.before.length && !job.capturesBefore) await this._captures(jobId, manifest.capture.before, "before");
      for (let i = 0; i < job.items.length; i++) {
        job = this.journal.get(jobId);
        const item = job.items[i];
        if (["VERIFIED", "FAILED", "SKIPPED"].includes(item.state)) continue;
        // an orphan is a pending decision (adopt or skip); nothing after it may be sent until
        // the user makes it, because later items may reference the id it is waiting on
        if (item.state === "ORPHANED") throw new Paused("ORPHANED", { idx: i, detail: item.error ?? null });
        if (this.pauseRequested) throw new Paused("USER", { idx: i });
        await this._runItem(jobId, item, order[i], manifest);
      }
      if (manifest.capture.after.length && !job.capturesAfter) await this._captures(jobId, manifest.capture.after, "after");
    } catch (e) {
      if (e instanceof Paused) return this._pause(jobId, e.reason, e);
      // raised by the capture passes (item reads pause inside _runItem): never escape as a crash
      if (e instanceof RateLimited) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: e.path, until: e.until });
      if (isTransport(e)) return this._pause(jobId, "NETWORK", { detail: String(e && e.message), httpStatus: e.httpStatus ?? null });
      throw e;
    }
    this.journal.setJobState(jobId, "DONE");
    if (this.reconciler && typeof this.reconciler.forget === "function") this.reconciler.forget(jobId);
    return this.summary(jobId);
  }

  /** Reconcile SENT items through the reconciler, then run. */
  async resume(jobId) {
    if (!this.reconciler) throw new Error("resume needs a reconciler");
    const { order } = this._m(jobId);
    const job = this.journal.get(jobId);
    this._syncIdmapFromJob(job);
    for (const item of job.items) {
      if (item.state !== "SENT") continue;
      const r = await this.reconciler.resolveSent(job, item, { planned: order[item.idx], lookup: this._lookup(job) });
      if (r.action === "confirm") {
        // landed:true means the sent request is proven to have applied; the runner then goes
        // straight to verify and never re-sends it.
        const phase = r.landed ? "verify" : (r.phase ?? item.phase);
        this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: r.entityId ?? item.entityId, phase, reconciled: r.note ?? "confirmed by reconciliation" });
        if (r.entityId && item.srcId) this._remember(item.srcId, r.entityId);
      } else if (r.action === "orphan") {
        this.journal.transition(jobId, item.idx, "ORPHANED", { error: r.note ?? "ambiguous after crash", candidates: r.candidates ?? [] });
      } else {
        throw new Error("reconciler returned unknown action " + r.action);
      }
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
    const holder = job.items.find((it) => it.idx !== idx && it.entityId === entityId);
    if (holder) throw new Error(`${entityId} is already held by item ${holder.idx} (${holder.name})`);
    const phase = item.phase === "create" || !item.entityId ? "update" : item.phase;
    this.journal.transition(jobId, idx, "CONFIRMED", { entityId, phase, adopted: true, error: null });
    if (item.srcId) this._remember(item.srcId, entityId);
  }
  skip(jobId, idx) { this.journal.transition(jobId, idx, "SKIPPED"); }

  summary(jobId) {
    const job = this.journal.get(jobId);
    const counts = {};
    for (const it of job.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
    return { jobId, state: job.state, pause: job.pause, counts, items: job.items.map((it) => ({ idx: it.idx, name: it.name, entity: it.entity, state: it.state, phase: it.phase, entityId: it.entityId, error: it.error ?? null, diffs: it.diffs ?? null, verify: it.verify ?? null })) };
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
      if (r.pfx === "img") { if (!this.files.has(r.key) && !readIdmap(this.storage)[r.key]) throw new Error(`@img:${r.key} has no file picked`); continue; }
      if (!this._lookup(this.journal.get(this._jobOf(item)))(r.pfx, r.key)) throw new Error(`@${r.pfx}:${r.key} is not resolvable yet (at ${r.path})`);
    }
    const problems = this.validator.problems(item.entity, planned.data, null, { preCreate: true });
    if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
  }

  async _create(jobId, item, planned) {
    const rc = recipe(item.entity);
    if (this.reconciler) {
      const key = await this.reconciler.beforeCreate(this.journal.get(jobId), item, item.entity);
      if (key) this.journal.annotate(jobId, item.idx, { snapshotKey: key });
    }
    const input = rc.create.input(planned.data);
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
    const live = await this.reader.get(rc.get, id, { fresh: true });
    if (!live.ok) {
      const cls = classifyError(live.error);
      if (cls === "SESSION") throw new Paused("SESSION", { detail: live.error.message });
      throw new Error(`${rc.get} failed: ${live.error.code} ${live.error.message}`);
    }
    if (live.data == null) throw new Error(`${rc.get} returned no record for ${id}`);
    const problems = this.validator.problems(item.entity, data, live.data);
    if (problems.length) throw new Error("pre-send validation: " + problems.join("; "));
    const payload = mergeForUpdate(item.entity, live.data, data, this.validator.knownFields(item.entity));
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
    let live = await this.reader.get(rc.get, userId, { fresh: true });
    if (!live.ok || !live.data) throw new Error(`profile.getAi failed for ${userId}`);
    let apid = live.data.aiProfileId;
    if (!apid) {
      const decoded = await this.journal.withSent(jobId, item.idx, { phase: "rules-toggle", entityId: userId }, () => this.client.call(rc.profileToggle, { aiId: userId }));
      const o = readMutation(decoded);
      if (o.kind !== "ok") { this._failFromOutcome(jobId, item, o, "toggle"); return; }
      this.journal.transition(jobId, item.idx, "CONFIRMED", { phase: "rules" });
      live = await this.reader.get(rc.get, userId, { fresh: true });
      apid = live.ok && live.data ? live.data.aiProfileId : null;
      if (!apid) throw new Error("no aiProfileId after toggle");
    }
    const decoded = await this.journal.withSent(jobId, item.idx, { phase: "rules", entityId: userId, aiProfileId: apid }, () => this.client.call(rc.profileUpdate, { id: apid, rules, includeDefaultRules }));
    const o = readMutation(decoded);
    await this.cache.invalidateEntity("ai");
    if (o.kind === "ok") { this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: userId, phase: "verify", aiProfileId: apid, assertedRules: true }); return; }
    this._failFromOutcome(jobId, item, o, "rules");
  }

  async _verifyOrSkip(jobId, item, planned, manifest) {
    if (!manifest.readBack) { this.journal.transition(jobId, item.idx, "VERIFIED", { verify: "skipped" }); return; }
    await this._verify(jobId, item, planned);
  }

  async _verify(jobId, item, planned) {
    const rc = recipe(item.entity);
    const data = await this._resolved(planned.data, jobId);
    const diffs = [];
    if (item.entity !== "aiProfile") {
      const live = await this.reader.get(rc.get, item.entityId, { fresh: true });
      if (!live.ok || !live.data) { this.journal.annotate(jobId, item.idx, { verify: "unread", phase: "verify" }); return; }
      diffs.push(...diffAsserted(item.entity, data, live.data));
    }
    if ((item.entity === "ai" && Array.isArray(planned.data.rules)) || item.entity === "aiProfile") {
      if (!item.aiProfileId) { this.journal.annotate(jobId, item.idx, { verify: "unread", phase: "verify" }); return; }
      const pr = await this.reader.get("ai.getAiProfile", item.aiProfileId, { fresh: true });
      if (pr.ok && pr.data) {
        if (JSON.stringify(pr.data.rules ?? []) !== JSON.stringify(planned.data.rules ?? [])) diffs.push({ key: "rules", sent: planned.data.rules, live: pr.data.rules });
        if (planned.data.includeDefaultRules !== undefined && pr.data.includeDefaultRules !== planned.data.includeDefaultRules) diffs.push({ key: "includeDefaultRules", sent: planned.data.includeDefaultRules, live: pr.data.includeDefaultRules });
      } else { this.journal.annotate(jobId, item.idx, { verify: "unread", phase: "verify" }); return; }
    }
    if (diffs.length) this.journal.annotate(jobId, item.idx, { diffs, verify: "drift", phase: "verify" });
    else this.journal.transition(jobId, item.idx, "VERIFIED", { diffs: [], verify: "match" });
  }

  async _captures(jobId, list, phase) {
    const key = phase === "before" ? "capturesBefore" : "capturesAfter";
    const job = this.journal.get(jobId);
    const out = Array.isArray(job[key + "Partial"]) ? job[key + "Partial"] : [];
    for (let i = out.length; i < list.length; i++) {
      const c = list[i];
      const path = c.proc || c.procedure;
      const id = c.input && (c.input.id ?? c.input.userId);
      const r = id != null ? await this.reader.get(path, id, { fresh: true }) : await this.reader.list(path, { fresh: true }); // RateLimited/Network propagate to run()
      out.push({ phase, proc: path, input: c.input ?? null, ok: r.ok, rows: Array.isArray(r.data) ? r.data.length : r.data ? 1 : 0, error: r.ok ? null : r.error.code });
      this.journal.annotateJob(jobId, { [key + "Partial"]: out }); // persisted incrementally
    }
    this.journal.annotateJob(jobId, { [key]: out, [key + "Partial"]: null });
    return out;
  }

  // ------------------------------------------------------------------ helpers
  _m(jobId) { const m = this.manifests.get(jobId); if (!m) throw new Error("no manifest attached for job " + jobId + "; call plan() or attach()"); return m; }
  _jobOf(item) { for (const [jobId, m] of this.manifests) if (m.order.some((o) => o === item || (o.idx === item.idx && this.journal.get(jobId)?.items[item.idx]?.srcId === item.srcId))) return jobId; return null; }

  _pause(jobId, reason, info) {
    this.journal.setJobState(jobId, "PAUSED", { pause: { reason, path: info.path ?? null, until: info.until ?? null, idx: info.idx ?? null, detail: info.detail ?? null, httpStatus: info.httpStatus ?? null } });
    this.log(`paused: ${reason}${info.path ? " on " + info.path : ""}`);
    return this.summary(jobId);
  }

  _failFromOutcome(jobId, item, o, step) {
    if (o.kind === "refused") { this.journal.transition(jobId, item.idx, "FAILED", { error: `${step} refused: ${o.message}` }); return; }
    const cls = classifyError(o.error);
    if (cls === "SESSION") throw new Paused("SESSION", { detail: o.error.message, idx: item.idx });
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
      const map = readIdmap(this.storage);
      if (map[r.key]) continue;
      const file = this.files.get(r.key);
      if (!file) throw new Error(`@img:${r.key} has no file picked`);
      if (!this.uploader) throw new Error("no uploader configured for @img refs");
      const up = await this.uploader.upload(file);
      map[r.key] = up.ufsUrl; writeIdmap(this.storage, map);
    }
    const job = jobId ? this.journal.get(jobId) : null;
    const { value, unresolved } = resolveRefs(data, this._lookup(job));
    if (unresolved.length) throw new Error("unresolved refs: " + unresolved.map((u) => `@${u.pfx}:${u.key} at ${u.path}`).join(", "));
    return value;
  }
}
