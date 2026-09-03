// The runner (spec sections 4, 5, 8). Executes a job item by item with write-ahead state
// transitions, two-phase creates, and read-back on asserted keys only. Never retries.
//
// Item lifecycle, per phase, every SENT flushed before its request leaves:
//   create:  PLANNED -SENT(phase create)-> CONFIRMED{entityId, phase update}
//   update:  CONFIRMED/PLANNED -SENT(phase update)-> CONFIRMED
//   rules:   (ai with rules, aiProfile) CONFIRMED -SENT(phase rules-toggle|rules)-> CONFIRMED
//   verify:  CONFIRMED -> VERIFIED when the asserted keys read back equal; else stays CONFIRMED
//            with item.diffs recorded (a drift is visible, not hidden).
//
// Anything thrown INSIDE a withSent thunk (NetworkError, TransportError, or a bug) leaves the
// item SENT: the request may have left. The job pauses; resume goes through reconciliation.
// A server refusal (success:false) or a validation error is FAILED, never retried.
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

export class Runner {
  /**
   * @param {object} d  dependencies
   * @param {import("../storage/journal.mjs").Journal} d.journal
   * @param {import("../transport/client.mjs").TrpcClient} d.client
   * @param {import("../budget/reader.mjs").CachedReader} d.reader
   * @param {import("../storage/captures.mjs").CaptureCache} d.cache
   * @param {import("./validate.mjs").Validator} d.validator
   * @param {object} [d.uploader]      {upload(file) -> {ufsUrl}}
   * @param {object} [d.reconciler]    {beforeCreate(job, item, entity), resolveSent(job, item)}
   * @param {Storage} d.storage        for the retained idmap
   * @param {(msg: string, item?: object) => void} [d.log]
   */
  constructor(d) {
    for (const k of ["journal", "client", "reader", "cache", "validator", "storage"]) if (!d[k]) throw new Error("Runner needs " + k);
    Object.assign(this, d);
    this.log = d.log ?? (() => {});
    this.files = new Map(); // name -> File, from the UI picker
    this.manifests = new Map(); // jobId -> parsed manifest (data lives here, not in the journal)
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

  /** Run every non-terminal item in order. Returns a summary. */
  async run(jobId) {
    const { manifest, order } = this._m(jobId);
    let job = this.journal.get(jobId);
    if (job.state === "PAUSED") {
      const t = this.budget && this.budget.log && this.budget.log.tripped();
      if (t) return this._pause(jobId, "TOO_MANY_REQUESTS", { path: t.path, until: t.until });
      job = this.journal.setJobState(jobId, "RUNNING");
    }
    if (job.items.some((it) => it.state === "SENT")) {
      throw new Error("job has SENT items; call resume() so they are reconciled before anything else is sent");
    }
    if (manifest.capture.before.length && !job.capturesBefore) {
      await this._captures(jobId, manifest.capture.before, "before");
    }
    try {
      for (let i = 0; i < job.items.length; i++) {
        job = this.journal.get(jobId);
        const item = job.items[i];
        if (["VERIFIED", "FAILED", "SKIPPED", "ORPHANED"].includes(item.state)) continue;
        await this._runItem(jobId, item, order[i], manifest);
      }
      if (manifest.capture.after.length) await this._captures(jobId, manifest.capture.after, "after");
    } catch (e) {
      if (e instanceof Paused) return this._pause(jobId, e.reason, e);
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
    for (const item of job.items) {
      if (item.state !== "SENT") continue;
      const r = await this.reconciler.resolveSent(job, item, { planned: order[item.idx] });
      if (r.action === "confirm") {
        // landed:true means the sent request is proven to have applied; the runner then goes
        // straight to verify and never re-sends it.
        this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: r.entityId ?? item.entityId, phase: r.landed ? "verify" : (r.phase ?? item.phase), reconciled: r.note ?? "confirmed by reconciliation" });
        if (r.entityId && item.srcId) this._remember(item.srcId, r.entityId);
      } else if (r.action === "orphan") {
        this.journal.transition(jobId, item.idx, "ORPHANED", { error: r.note ?? "ambiguous after crash", candidates: r.candidates ?? [] });
      } else {
        throw new Error("reconciler returned unknown action " + r.action);
      }
    }
    return this.run(jobId);
  }

  /** User decision on an ORPHANED item: adopt an id (continue at update) or skip. */
  adopt(jobId, idx, entityId) {
    const item = this.journal.get(jobId).items[idx];
    this.journal.transition(jobId, idx, "CONFIRMED", { entityId, phase: item.op === "create" ? "update" : item.phase, adopted: true });
    if (item.srcId) this._remember(item.srcId, entityId);
  }
  skip(jobId, idx) { this.journal.transition(jobId, idx, "SKIPPED"); }

  summary(jobId) {
    const job = this.journal.get(jobId);
    const counts = {};
    for (const it of job.items) counts[it.state] = (counts[it.state] ?? 0) + 1;
    return { jobId, state: job.state, pause: job.pause, counts, items: job.items.map((it) => ({ idx: it.idx, name: it.name, entity: it.entity, state: it.state, phase: it.phase, entityId: it.entityId, error: it.error ?? null, diffs: it.diffs ?? null })) };
  }

  // ------------------------------------------------------------------ items
  async _runItem(jobId, item, planned, manifest) {
    const ent = item.entity;
    try {
      if (item.state === "CONFIRMED" && item.phase === "verify") {
        // reconciliation proved the last send landed; do not send anything, only read back
        if (manifest.readBack) await this._verify(jobId, item, planned);
        else this.journal.transition(jobId, item.idx, "VERIFIED", { verify: "skipped" });
        return;
      }
      if (item.op === "create" && item.state === "PLANNED") {
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
      if (item.state === "CONFIRMED" && manifest.readBack) await this._verify(jobId, item, planned);
    } catch (e) {
      if (e instanceof Paused) throw e;
      if (e instanceof RateLimited) throw new Paused("TOO_MANY_REQUESTS", { path: e.path, until: e.until, idx: item.idx });
      const cur = this.journal.get(jobId).items[item.idx];
      if (cur.state === "SENT") {
        // thrown inside a withSent thunk: the request may have left. Leave SENT, pause.
        throw new Paused(e instanceof NetworkError ? "NETWORK" : e instanceof TransportError ? "UNDECODABLE_RESPONSE" : "AMBIGUOUS", { idx: item.idx, detail: String(e && e.message) });
      }
      // an ordinary failure before or after a send: this item fails, the job continues
      this.journal.transition(jobId, item.idx, "FAILED", { error: String(e && e.message ? e.message : e) });
      this.log(`item ${item.idx} failed: ${e && e.message}`, item);
    }
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
    const data = await this._resolved(planned.data);
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
    if (o.kind === "ok") { this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: id, phase: "update", asserted: Object.keys(data) }); return; }
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
      const decoded = await this.journal.withSent(jobId, item.idx, { phase: "rules-toggle" }, () => this.client.call(rc.profileToggle, { aiId: userId }));
      const o = readMutation(decoded);
      if (o.kind !== "ok") { this._failFromOutcome(jobId, item, o, "toggle"); return; }
      this.journal.transition(jobId, item.idx, "CONFIRMED", { phase: "rules" });
      live = await this.reader.get(rc.get, userId, { fresh: true });
      apid = live.ok && live.data ? live.data.aiProfileId : null;
      if (!apid) throw new Error("no aiProfileId after toggle");
    }
    const decoded = await this.journal.withSent(jobId, item.idx, { phase: "rules", aiProfileId: apid }, () => this.client.call(rc.profileUpdate, { id: apid, rules, includeDefaultRules }));
    const o = readMutation(decoded);
    await this.cache.invalidateEntity("ai");
    if (o.kind === "ok") { this.journal.transition(jobId, item.idx, "CONFIRMED", { entityId: userId, phase: "rules", aiProfileId: apid, asserted: ["rules", "includeDefaultRules"] }); return; }
    this._failFromOutcome(jobId, item, o, "rules");
  }

  async _verify(jobId, item, planned) {
    const rc = recipe(item.entity);
    const data = await this._resolved(planned.data);
    const diffs = [];
    if (item.entity !== "aiProfile") {
      const live = await this.reader.get(rc.get, item.entityId, { fresh: true });
      if (!live.ok || !live.data) { this.journal.annotate(jobId, item.idx, { verify: "unread" }); return; }
      diffs.push(...diffAsserted(item.entity, data, live.data));
    }
    if ((item.entity === "ai" && Array.isArray(planned.data.rules)) || item.entity === "aiProfile") {
      const pr = await this.reader.get("ai.getAiProfile", item.aiProfileId, { fresh: true });
      if (pr.ok && pr.data) {
        if (JSON.stringify(pr.data.rules ?? []) !== JSON.stringify(planned.data.rules ?? [])) diffs.push({ key: "rules", sent: planned.data.rules, live: pr.data.rules });
        if (planned.data.includeDefaultRules !== undefined && pr.data.includeDefaultRules !== planned.data.includeDefaultRules) diffs.push({ key: "includeDefaultRules", sent: planned.data.includeDefaultRules, live: pr.data.includeDefaultRules });
      } else { this.journal.annotate(jobId, item.idx, { verify: "unread" }); return; }
    }
    if (diffs.length) this.journal.annotate(jobId, item.idx, { diffs, verify: "drift" });
    else this.journal.transition(jobId, item.idx, "VERIFIED", { diffs: [], verify: "match" });
  }

  async _captures(jobId, list, phase) {
    const out = [];
    for (const c of list) {
      const path = c.proc || c.procedure;
      try {
        const id = c.input && (c.input.id ?? c.input.userId);
        const r = id != null ? await this.reader.get(path, id, { fresh: true }) : await this.reader.list(path, { fresh: true });
        out.push({ phase, proc: path, input: c.input ?? null, ok: r.ok, rows: Array.isArray(r.data) ? r.data.length : r.data ? 1 : 0, error: r.ok ? null : r.error.code });
      } catch (e) {
        if (e instanceof RateLimited) throw new Paused("TOO_MANY_REQUESTS", { path: e.path, until: e.until });
        out.push({ phase, proc: path, input: c.input ?? null, ok: false, error: String(e && e.message) });
      }
    }
    const job = this.journal.get(jobId);
    const patch = phase === "before" ? { capturesBefore: out } : { capturesAfter: out };
    Object.assign(job, patch);
    this.journal._write(job);
    return out;
  }

  // ------------------------------------------------------------------ helpers
  _m(jobId) { const m = this.manifests.get(jobId); if (!m) throw new Error("no manifest attached for job " + jobId + "; call plan() or attach()"); return m; }

  _pause(jobId, reason, info) {
    this.journal.setJobState(jobId, "PAUSED", { pause: { reason, path: info.path ?? null, until: info.until ?? null, idx: info.idx ?? null, detail: info.detail ?? null } });
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

  async _resolved(data) {
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
    const map = readIdmap(this.storage);
    const { value, unresolved } = resolveRefs(data, (pfx, key) => map[key]);
    if (unresolved.length) throw new Error("unresolved refs: " + unresolved.map((u) => `@${u.pfx}:${u.key} at ${u.path}`).join(", "));
    return value;
  }
}
