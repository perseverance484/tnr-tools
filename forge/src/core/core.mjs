// ForgeCore — the headless orchestration layer.
//
// It owns Forge's machine state and every action that changes it: picker loading, manifest
// selection, the auth gates, starting and resuming jobs, driving a run, materializing captures and
// exporting the results bundle. It has NO dependency on the DOM, `window`, userscript takeover or
// any presentation class, and it must not acquire one — a second shell, or a headless host with no
// DOM at all, drives a complete Forge lifecycle through exactly this surface.
//
// Everything the operator needs to be *told* leaves through notify() as a fact — a level, a
// message, sometimes a payload — never as markup. The view decides what a toast looks like. This
// is what keeps "the run finished with drift" a single sentence of domain reasoning instead of one
// copy per shell.

import { parseManifest, planOrder, ManifestError } from "../runner/manifest.mjs";
import { collectRefs } from "../runner/refs.mjs";
import { manifestNumber, manifestSummary, GH } from "../github.mjs";
import { JournalError } from "../storage/journal.mjs";
import { blockedPaths, resumeBlockedReason, runHeadline } from "./facts.mjs";
import { resolveCaptures, buildBundle, repoSyncReady, inboxPath } from "./results.mjs";

export class ForgeCore {
  /**
   * @param {object} d { version, storage, journal, cache, budget, reader, client, session, auth,
   *                     runner, reconciler, github, validator, now }
   */
  constructor(d) {
    Object.assign(this, d);
    this.now = d.now ?? (() => Date.now());
    this.authBusy = false;
    this.state = { screen: "jobs", jobId: null, picker: null, selected: null, running: null, persisted: null };
    this._listeners = new Set();
  }

  // ------------------------------------------------------------------ notifications
  /** @param {(n: {type: string, [k: string]: any}) => void} fn @returns {() => void} */
  subscribe(fn) {
    if (typeof fn !== "function") throw new TypeError("ForgeCore.subscribe needs a function");
    this._listeners.add(fn);
    return () => this._listeners.delete(fn);
  }

  notify(note) {
    for (const fn of [...this._listeners]) {
      try { fn(note); } catch { /* a view must never be able to fail an action */ }
    }
  }

  /** Something went wrong in a named context. Returns the message so callers can also log it. */
  fail(context, e) {
    const msg = e instanceof JournalError ? `journal: ${e.message}` : (e && e.message) || String(e);
    this.notify({ type: "error", context, text: `${context}: ${msg}`, level: "bad", ms: 9000 });
    return msg;
  }

  say(text, level = "info", ms = 4000) { this.notify({ type: "message", text, level, ms }); }

  /** Ask the view to re-render. The core never renders; it only says that something moved. */
  changed() { this.notify({ type: "changed" }); }

  // ------------------------------------------------------------------ auth
  async establishAuth() { return this._auth(() => this.auth.establish()); }
  async recheckAuth() { return this._auth(() => this.auth.probe()); }

  async _auth(fn) {
    if (!this.auth || this.authBusy) return this.auth ? this.auth.state : null;
    this.authBusy = true;
    this.changed();
    try { return await fn(); }
    finally { this.authBusy = false; this.changed(); }
  }

  resumeBlockedReason(job) { return resumeBlockedReason(job, this.auth); }
  blockedPaths(plan, manifest) { return blockedPaths(this.auth, plan, manifest); }

  // ------------------------------------------------------------------ picker
  async loadPicker(force) {
    if (this.state.picker && !force) return;
    this.state.pickerError = null;
    try {
      const entries = (await this.github.list(GH.pushDir)).filter((e) => e.type === "file" && /\.json$/i.test(e.name))
        .map((e) => ({ ...e, number: manifestNumber(e.name), summary: null, loading: true }));
      entries.sort((a, b) => (b.number ?? -1) - (a.number ?? -1) || a.name.localeCompare(b.name));
      this.state.picker = entries; this.state.pickerAt = new Date(this.now()).toISOString();
      this.notify({ type: "picker" });
      await Promise.all(entries.map(async (e) => {
        try {
          const key = `gh:${e.path}@${e.sha}`;
          const hit = await this.cache.get("github.contents", key);
          const text = hit ? hit.data : await this.github.text(e.path);
          if (!hit) await this.cache.put({ path: "github.contents", id: key, data: text });
          e.text = text; e.summary = manifestSummary(text);
        } catch (err) { e.error = err.message; }
        e.loading = false;
        this.notify({ type: "picker" });
      }));
    } catch (e) {
      this.state.picker = this.state.picker || [];
      this.state.pickerError = e.message;
      this.notify({ type: "picker" });
    }
  }

  async selectManifest(entry) {
    try {
      const text = entry.text ?? await this.github.text(entry.path);
      const manifest = parseManifest(text);
      const problems = [];
      let plan = [];
      try { plan = planOrder(manifest, JSON.parse(this.storage.getItem("tnr_bk_idmap_v1") || "{}")); } catch (e) { problems.push(e.message); }
      for (const it of plan) {
        const p = it.entity === "ai" || it.entity === "aiProfile" ? [] : this.validator.problems(it.entity, it.data, null);
        for (const x of p) problems.push(`item ${it.idx} (${it.name}): ${x}`);
      }
      const images = [...new Set(plan.flatMap((it) => collectRefs(it.data).filter((r) => r.pfx === "img").map((r) => r.key)))];
      this.state.selected = { entry, text, manifest, plan, problems, images };
      this.state.selected.blocked = this.blockedPaths(plan, manifest);
      this.changed();
    } catch (e) { this.fail("select manifest", e instanceof ManifestError ? e : e); }
  }

  // ------------------------------------------------------------------ jobs
  async startJob() {
    const s = this.state.selected; if (!s) return;
    // Re-read the gate at the moment of the tap, not at selection time: the operator may have been
    // sitting on this screen while the session expired.
    const blocked = this.blockedPaths(s.plan, s.manifest);
    if (blocked.length) {
      this.say(`TNR authentication is unavailable; ${blocked.join(", ")} ${blocked.length === 1 ? "is a protected procedure" : "are protected procedures"} and nothing was sent`, "bad", 9000);
      this.state.selected.blocked = blocked;
      return this.changed();
    }
    const jobId = `${s.entry.number ?? "m"}-${Date.now().toString(36)}`;
    try {
      this.runner.plan(s.text, { jobId, manifestPath: s.entry.path, manifestNumber: s.entry.number });
    } catch (e) { return this.fail("plan", e); }
    this.state.selected = null;
    this.go("run", { jobId });
    await this.drive(jobId, () => this.runner.run(jobId));
  }

  async resumeJob(jobId) {
    const job = this.journal.get(jobId);
    // Re-read at the moment of the tap: the state may have changed since the screen rendered.
    const blocked = this.resumeBlockedReason(job);
    if (blocked) { this.say(blocked, "bad", 9000); return this.changed(); }
    if (!this.runner.manifests.has(jobId)) {
      try {
        const text = job.manifestPath ? await this.github.text(job.manifestPath) : null;
        if (!text) throw new Error("no manifest path recorded; cannot resume");
        this.runner.attach(jobId, text);
      } catch (e) { return this.fail("resume: fetch manifest", e); }
    }
    this.go("run", { jobId });
    const hasSent = job.items.some((i) => i.state === "SENT");
    await this.drive(jobId, () => (hasSent ? this.runner.resume(jobId) : this.runner.run(jobId)));
  }

  go(screen, patch = {}) { Object.assign(this.state, patch, { screen }); this.changed(); }

  async drive(jobId, fn) {
    if (this.state.running) return this.say("a job is already running", "warn");
    this.state.running = jobId; this.state.runningNote = "";
    this.changed();
    this.notify({ type: "driving", jobId });
    try {
      const s = await fn();
      // Re-check every requested full body against the capture cache BEFORE the headline, so it
      // can never be greener than the evidence: a body that vanished between the read and here (an
      // entity invalidation, an evicted store) changes the job's own outcome. A capture cache that
      // cannot even be opened must not swallow the run: the job still finished, and its bundle is
      // still exported below with whatever the journal already recorded.
      if (s.state === "DONE" || s.state === "INCOMPLETE") {
        try { await resolveCaptures(this, jobId); } catch (e) { this.fail("resolve full captures", e); }
      }
      const job = this.journal.get(jobId);
      const head = runHeadline(job, s);
      this.say(head.text, head.kind, head.ms);
      if (s.state === "DONE" || s.state === "INCOMPLETE") await this.exportJob(jobId, { auto: true });
    } catch (e) { this.fail("run", e); }
    finally {
      this.state.running = null;
      this.notify({ type: "idle", jobId });
      this.changed();
    }
  }

  requestPause() { this.runner.requestPause(); this.say("pausing after the current item finishes", "warn"); }
  adopt(jobId, idx, id) { try { this.runner.adopt(jobId, idx, id); this.changed(); } catch (e) { this.fail("adopt", e); } }
  skip(jobId, idx) { try { this.runner.skip(jobId, idx); this.changed(); } catch (e) { this.fail("skip", e); } }

  resolveCaptures(jobId) { return resolveCaptures(this, jobId); }

  /** Results bundle, committed via GitHub when Sync is on, otherwise handed to the view. */
  async exportJob(jobId, { auto = false } = {}) {
    let captures;
    try { captures = await resolveCaptures(this, jobId); }
    catch (e) {
      // A broken capture cache must not stop the bundle from being written: the bundle is the
      // evidence. It goes out with whatever the journal already recorded, which for an
      // unresolvable full capture is persistOk:false, so nothing claims a body it does not carry.
      this.fail("resolve full captures", e);
      const j = this.journal.get(jobId);
      captures = [...(j.capturesBefore || []), ...(j.capturesAfter || [])];
    }
    const job = this.journal.get(jobId); // read AFTER resolveCaptures so the embedded journal agrees
    const bundle = buildBundle(this, job, captures);
    const name = `tnr_results_${Date.now()}.json`;
    const text = JSON.stringify(bundle, null, 1);
    const synced = repoSyncReady(this.storage);
    if (synced) {
      try {
        const r = await this.github.put(inboxPath(name), text, `results: ${name} (forge)`);
        this.say(`committed ${name}${r.sha ? " @" + r.sha.slice(0, 7) : ""}`, "ok");
        return;
      } catch (e) { this.fail("commit results", e); }
    }
    if (!auto || !synced) this.notify({ type: "export", text, name });
  }
}
