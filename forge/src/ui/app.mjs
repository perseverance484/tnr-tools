// The app shell: owns the layer instances, routes between the five screens, surfaces every
// error in the UI, and runs jobs. createElement + CSSOM only.
import { h, replace, installCss } from "./dom.mjs";
import { CSS } from "./styles.mjs";
import { JobsScreen, ManifestsScreen, RunScreen, CapturesScreen, SettingsScreen } from "./screens.mjs";
import { parseManifest, planOrder, ManifestError } from "../runner/manifest.mjs";
import { collectRefs } from "../runner/refs.mjs";
import { manifestNumber, manifestSummary, GH } from "../github.mjs";
import { readGh } from "../storage/compat.mjs";
import { JournalError } from "../storage/journal.mjs";

const SCREENS = { jobs: ["Jobs", JobsScreen], manifests: ["Manifests", ManifestsScreen], run: ["Run", RunScreen], captures: ["Captures", CapturesScreen], settings: ["Settings", SettingsScreen] };

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
      this.toast(`job ${s.state}: ${Object.entries(s.counts).map(([k, v]) => `${v} ${k.toLowerCase()}`).join(", ")}`, s.state === "DONE" ? "ok" : "warn", 8000);
      if (s.state === "DONE") await this.exportJob(jobId, { auto: true });
    } catch (e) { this.fail("run", e); }
    finally { clearInterval(tick); this.state.running = null; this.refresh(); }
  }

  requestPause() { this.runner.requestPause(); this.toast("pausing after the current item finishes", "warn"); }
  adopt(jobId, idx, id) { try { this.runner.adopt(jobId, idx, id); this.refresh(); } catch (e) { this.fail("adopt", e); } }
  skip(jobId, idx) { try { this.runner.skip(jobId, idx); this.refresh(); } catch (e) { this.fail("skip", e); } }

  /** Results bundle in the shape harvests/inbox/ already holds, committed via GitHub when Sync is on. */
  async exportJob(jobId, { auto = false } = {}) {
    const job = this.journal.get(jobId);
    const bundle = {
      builder: this.version, at: new Date(this.now()).toISOString(), cfg: "forge", checks: null,
      postflight: { match: job.items.filter((i) => i.verify === "match").length, diff: job.items.filter((i) => i.verify === "drift").length, unverified: job.items.filter((i) => i.verify === "unread").length },
      entries: job.items.map((i) => ({ name: i.name, srcId: i.srcId, entity: i.entity, slot: i.op, state: i.state, phase: i.phase, detail: i.error || i.reconciled || "", verdict: i.verify || null, diffs: i.diffs || [], id: i.entityId || i.targetId || null })),
      captures: [...(job.capturesBefore || []), ...(job.capturesAfter || [])],
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
