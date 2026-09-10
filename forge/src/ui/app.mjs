// The app shell: owns the layer instances, routes between the five screens, surfaces every
// error in the UI, and runs jobs. createElement + CSSOM only.
import { h, replace, installCss } from "./dom.mjs";
import { CSS } from "./styles.mjs";
import { JobsScreen, ManifestsScreen, RunScreen, CapturesScreen, SettingsScreen } from "./screens.mjs";
import { parseManifest, planOrder, ManifestError } from "../runner/manifest.mjs";
import { collectRefs } from "../runner/refs.mjs";
import { manifestNumber, manifestSummary, GH } from "../github.mjs";
import { readGh } from "../storage/compat.mjs";
import { JournalError, jobOutcome } from "../storage/journal.mjs";
import { MAX_FULL_CAPTURE_BYTES } from "../storage/captures.mjs";

const SCREENS = { jobs: ["Jobs", JobsScreen], manifests: ["Manifests", ManifestsScreen], run: ["Run", RunScreen], captures: ["Captures", CapturesScreen], settings: ["Settings", SettingsScreen] };


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

export class App {
  /**
   * @param {object} d  { version, storage, journal, cache, budget, reader, client, session, runner, reconciler, github, validator, now }
   */
  constructor(d) {
    Object.assign(this, d);
    this.now = d.now ?? (() => Date.now());
    this.state = { screen: "jobs", jobId: null, picker: null, selected: null, running: null, persisted: null };
    this.root = null;
  }

  mount(container, doc = document) {
    installCss(CSS, doc);
    this.root = h("div", { class: "f-app" });
    this.$top = h("div", { class: "f-top" }, h("span", { class: "f-title" }, "TNR forge"), h("span", { class: "f-ver" }, this.version));
    this.$nav = h("nav", { class: "f-nav" });
    this.$main = h("main", { class: "f-main" });
    this.$toast = h("div", { class: "f-toast" });
    this.root.append(this.$top, this.$nav, this.$main, this.$toast);
    container.appendChild(this.root);
    const open = this.journal.resumable();
    if (open.length) this.state.screen = "jobs";
    this.refresh();
    this._persist();
    return this.root;
  }

  go(screen, patch = {}) { Object.assign(this.state, patch, { screen }); this.refresh(); }

  refresh() {
    replace(this.$nav, Object.entries(SCREENS).map(([k, [label]]) => h("button", { "aria-current": this.state.screen === k ? "page" : null, onClick: () => this.go(k) }, label)));
    try {
      replace(this.$main, SCREENS[this.state.screen][1](this));
    } catch (e) {
      replace(this.$main, h("div", { class: "f-banner bad" }, h("b", {}, "This screen failed to render. "), h("div", { class: "f-err" }, String(e && e.stack || e))));
    }
  }

  toast(text, kind = "info", ms = 4000) {
    const el = h("div", { class: "f-banner " + kind }, text);
    this.$toast.appendChild(el);
    setTimeout(() => el.remove(), ms);
  }
  fail(context, e) {
    const msg = e instanceof JournalError ? `journal: ${e.message}` : (e && e.message) || String(e);
    this.toast(`${context}: ${msg}`, "bad", 9000);
    this.log(`${context}: ${msg}`);
  }
  log(msg) { (this.logs ??= []).push({ at: new Date(this.now()).toISOString(), msg }); }

  confirm(text, fn) {
    // window.confirm is synchronous and works in a userscript page; no custom modal needed.
    if (globalThis.confirm ? globalThis.confirm(text) : true) Promise.resolve().then(fn).catch((e) => this.fail("action", e));
  }

  showExport(text, title) {
    const ta = h("textarea", { readOnly: true, value: text });
    const card = h("div", { class: "f-card" }, h("h2", {}, title), ta, h("div", { class: "f-actions" },
      h("button", { onClick: async () => { try { await navigator.clipboard.writeText(text); this.toast("copied", "ok"); } catch { ta.focus(); ta.select(); this.toast("select-all and copy", "warn"); } } }, "Copy"),
      h("button", { onClick: () => card.remove() }, "Close")));
    this.$main.prepend(card);
  }

  // ------------------------------------------------------------------ picker
  async loadPicker(force) {
    if (this.state.picker && !force) return;
    this.state.pickerError = null;
    try {
      const entries = (await this.github.list(GH.pushDir)).filter((e) => e.type === "file" && /\.json$/i.test(e.name))
        .map((e) => ({ ...e, number: manifestNumber(e.name), summary: null, loading: true }));
      entries.sort((a, b) => (b.number ?? -1) - (a.number ?? -1) || a.name.localeCompare(b.name));
      this.state.picker = entries; this.state.pickerAt = new Date(this.now()).toISOString();
      this.state._renderPicker && this.state._renderPicker();
      await Promise.all(entries.map(async (e) => {
        try {
          const key = `gh:${e.path}@${e.sha}`;
          const hit = await this.cache.get("github.contents", key);
          const text = hit ? hit.data : await this.github.text(e.path);
          if (!hit) await this.cache.put({ path: "github.contents", id: key, data: text });
          e.text = text; e.summary = manifestSummary(text);
        } catch (err) { e.error = err.message; }
        e.loading = false;
        this.state._renderPicker && this.state._renderPicker();
      }));
    } catch (e) { this.state.picker = this.state.picker || []; this.state.pickerError = e.message; this.state._renderPicker && this.state._renderPicker(); }
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
      this.refresh();
    } catch (e) { this.fail("select manifest", e instanceof ManifestError ? e : e); }
  }

  // ------------------------------------------------------------------ jobs
  async startJob() {
    const s = this.state.selected; if (!s) return;
    const jobId = `${s.entry.number ?? "m"}-${Date.now().toString(36)}`;
    try {
      this.runner.plan(s.text, { jobId, manifestPath: s.entry.path, manifestNumber: s.entry.number });
    } catch (e) { return this.fail("plan", e); }
    this.state.selected = null;
    this.go("run", { jobId });
    await this._drive(jobId, () => this.runner.run(jobId));
  }

  async resumeJob(jobId) {
    const job = this.journal.get(jobId);
    if (!this.runner.manifests.has(jobId)) {
      try {
        const text = job.manifestPath ? await this.github.text(job.manifestPath) : null;
        if (!text) throw new Error("no manifest path recorded; cannot resume");
        this.runner.attach(jobId, text);
      } catch (e) { return this.fail("resume: fetch manifest", e); }
    }
    this.go("run", { jobId });
    const hasSent = job.items.some((i) => i.state === "SENT");
    await this._drive(jobId, () => (hasSent ? this.runner.resume(jobId) : this.runner.run(jobId)));
  }

  async _drive(jobId, fn) {
    if (this.state.running) return this.toast("a job is already running", "warn");
    this.state.running = jobId; this.state.runningNote = "";
    this.refresh();
    const tick = setInterval(() => { if (this.state.screen === "run") this.refresh(); }, 1500);
    try {
      const s = await fn();
      // Re-check every requested full body against the capture cache BEFORE the toast, so the
      // headline can never be greener than the evidence: a body that vanished between the read
      // and here (an entity invalidation, an evicted store) changes the job's own outcome. A
      // capture cache that cannot even be opened must not swallow the run: the job still finished,
      // and its bundle is still exported below with whatever the journal already recorded.
      if (s.state === "DONE" || s.state === "INCOMPLETE") {
        try { await this.resolveCaptures(jobId); } catch (e) { this.fail("resolve full captures", e); }
      }
      // Only outcome "success" is green. A finished job holding a drifted, unread or failed item is
      // reported as what it is; the bundle is still exported, because a failure is evidence too.
      const job = this.journal.get(jobId);
      const captures = [...(job.capturesBefore || []), ...(job.capturesAfter || [])];
      const outcome = jobOutcome(job);
      const full = captures.filter((capture) => capture.persist === "full");
      const detail = job.items.length
        ? `${Object.entries(s.counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")} · ${s.verify.match} verified, ${s.verify.drift} drift, ${s.verify.unread} unread`
        : `${captures.filter((capture) => capture.ok).length}/${captures.length} captures read ok${full.length ? ` · ${full.filter((capture) => capture.persistOk === true).length}/${full.length} full bodies persisted` : ""} · zero mutations`;
      const kind = outcome === "success" ? "ok" : outcome === "failed" ? "bad" : "warn";
      this.toast(`job ${s.state} (${outcome}): ${detail}`, kind, 8000);
      if (s.state === "DONE" || s.state === "INCOMPLETE") await this.exportJob(jobId, { auto: true });
    } catch (e) { this.fail("run", e); }
    finally { clearInterval(tick); this.state.running = null; this.refresh(); }
  }

  requestPause() { this.runner.requestPause(); this.toast("pausing after the current item finishes", "warn"); }
  adopt(jobId, idx, id) { try { this.runner.adopt(jobId, idx, id); this.refresh(); } catch (e) { this.fail("adopt", e); } }
  skip(jobId, idx) { try { this.runner.skip(jobId, idx); this.refresh(); } catch (e) { this.fail("skip", e); } }

  /**
   * Materialize every requested full capture body out of the IndexedDB capture cache, and write
   * the VERDICT (not the body) back onto the job's own capture entries. Two things follow from
   * doing it this way:
   *
   *   - the export never issues a read. The body it ships is the immutable snapshot the capture
   *     pass committed from that read's own response; if it is not there, the export says so
   *     rather than going back to the game for it. It is NOT read out of the path+id read cache,
   *     which a later read or a write to the entity may legitimately have replaced or dropped
   *     (independent review FFC-1);
   *   - the journal stays compact and stays the record of truth. persistOk/persistError live on
   *     the journal entry, so jobOutcome(), the run screen and the bundle all read one answer,
   *     and the embedded `journal` in the bundle never duplicates the bodies beside it.
   *
   * Returns the export-ready capture list: summary entries exactly as journaled, full entries
   * with `data` attached when, and only when, the body was materialized intact.
   */
  async resolveCaptures(jobId) {
    const job = this.journal.get(jobId);
    const patch = {};
    const out = [];
    for (const key of ["capturesBefore", "capturesAfter"]) {
      if (!Array.isArray(job[key])) continue;
      const resolved = [];
      for (const capture of job[key]) resolved.push(await this._materialize(capture));
      // Only a pass that actually re-checked something rewrites the journal: a job with no full
      // capture is untouched by exporting it, exactly as before this contract existed.
      if (job[key].some((capture) => capture && capture.persist === "full")) {
        patch[key] = resolved.map(({ data, ...rest }) => rest); // the journal keeps the verdict, never the body
      }
      out.push(...resolved);
    }
    if (Object.keys(patch).length) this.journal.annotateJob(jobId, patch);
    return out;
  }

  async _materialize(capture) {
    if (!capture || typeof capture !== "object" || capture.persist !== "full") return capture;
    const c = { ...capture, persistOk: false, persistError: null };
    delete c.data;
    if (capture.ok !== true) { c.persistError = "read failed; there is no body to persist"; return c; }
    // A failure the capture pass already recorded stands. It was decided with the body in hand -
    // over the ceiling, or IndexedDB refused the write - so it names the real reason, which is
    // more specific than the "snapshot is gone" the lookup below would infer from the snapshot
    // that was deliberately never written. Export may downgrade a success; it never overwrites a
    // recorded reason, and it never upgrades a failure.
    if (capture.persistOk === false && capture.persistError) return { ...c, persistError: capture.persistError };
    const key = capture.snapshotKey || null;
    if (!key) { c.persistError = "no capture snapshot key was journaled for this full capture"; return c; }
    let rec = null;
    try { rec = await this.cache.getSnapshot(key); }
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

  /** Results bundle in the shape harvests/inbox/ already holds, committed via GitHub when Sync is on. */
  async exportJob(jobId, { auto = false } = {}) {
    let captures;
    try { captures = await this.resolveCaptures(jobId); }
    catch (e) {
      // A broken capture cache must not stop the bundle from being written: the bundle is the
      // evidence. It goes out with whatever the journal already recorded, which for an
      // unresolvable full capture is persistOk:false, so nothing claims a body it does not carry.
      this.fail("resolve full captures", e);
      const j = this.journal.get(jobId);
      captures = [...(j.capturesBefore || []), ...(j.capturesAfter || [])];
    }
    const job = this.journal.get(jobId); // read AFTER resolveCaptures so the embedded journal agrees
    const bundle = {
      builder: this.version, at: new Date(this.now()).toISOString(), cfg: "forge", checks: null,
      // `outcome` is the honest headline: an exported bundle is evidence, not a claim of success.
      state: job.state, outcome: jobOutcome(job),
      postflight: {
        match: job.items.filter((i) => i.verify === "match").length,
        diff: job.items.filter((i) => i.verify === "drift").length,
        unverified: job.items.filter((i) => i.verify === "unread").length,
        failed: job.items.filter((i) => i.state === "FAILED").length,
        skipped: job.items.filter((i) => i.state === "SKIPPED").length,
        unresolved: job.items.filter((i) => !["VERIFIED", "FAILED", "SKIPPED"].includes(i.state)).length,
      },
      entries: job.items.map((i) => harvestEntry(i)),
      captures,
      idmap: JSON.parse(this.storage.getItem("tnr_bk_idmap_v1") || "{}"),
      journal: job,
    };
    const name = `tnr_results_${Date.now()}.json`;
    const text = JSON.stringify(bundle, null, 1);
    const gh = readGh(this.storage);
    if (gh.on && gh.pat) {
      try { const r = await this.github.put(`${GH.inboxDir}/${name}`, text, `results: ${name} (forge)`); this.toast(`committed ${name}${r.sha ? " @" + r.sha.slice(0, 7) : ""}`, "ok"); return; }
      catch (e) { this.fail("commit results", e); }
    }
    if (!auto || !(gh.on && gh.pat)) this.showExport(text, name);
  }

  async _persist() {
    try { if (navigator.storage && navigator.storage.persist) { this.state.persisted = await navigator.storage.persist(); const el = document.getElementById("f-persist"); if (el) el.textContent = String(this.state.persisted); } } catch { /* best effort */ }
  }
}
