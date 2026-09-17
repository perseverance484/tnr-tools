// The app shell: the userscript-facing VIEW. It owns the DOM - mounting, routing between the five
// screens, banners, toasts and the export card - and nothing else.
//
// Every workflow decision now lives in ForgeCore (src/core/core.mjs): picker loading, manifest
// selection, the auth gates, starting/resuming/driving jobs, capture materialization and the
// results bundle. This class subscribes to the core's notifications and renders them. It forwards
// the actions the screens call, so screen code is unchanged, but it no longer DECIDES anything.
//
// That division is the point of Phase 0: a second shell, or a headless host with no DOM at all,
// drives the same lifecycle through ForgeCore without duplicating a line of this file.
//
// createElement + CSSOM only.
import { h, replace, installCss } from "./dom.mjs";
import { CSS } from "./styles.mjs";
import { JobsScreen, ManifestsScreen, RunScreen, CapturesScreen, SettingsScreen } from "./screens.mjs";
import { ForgeCore } from "../core/core.mjs";
import { authFacts } from "../core/facts.mjs";

const SCREENS = { jobs: ["Jobs", JobsScreen], manifests: ["Manifests", ManifestsScreen], run: ["Run", RunScreen], captures: ["Captures", CapturesScreen], settings: ["Settings", SettingsScreen] };

// Re-exported so existing importers keep working; it lives in the core now.
export { harvestEntry } from "../core/facts.mjs";

export class App {
  /**
   * @param {object} d  { version, storage, journal, cache, budget, reader, client, session, runner, reconciler, github, validator, now }
   */
  constructor(d) {
    Object.assign(this, d);
    this.now = d.now ?? (() => Date.now());
    this.exit = d.exit ?? null;   // set when Forge is an overlay over a carrier page
    this.core = d.core ?? new ForgeCore({ ...d, now: this.now });
    this.state = this.core.state;
    this.root = null;
    this._tick = null;
    this._unsubscribe = this.core.subscribe((n) => this._onCore(n));
  }

  get authBusy() { return this.core.authBusy; }
  set authBusy(v) { this.core.authBusy = v; }

  /** Turn a core notification into pixels. This is the only place that decision is made. */
  _onCore(n) {
    switch (n.type) {
      case "changed": return this.refresh();
      case "message": return this.toast(n.text, n.level, n.ms);
      case "error": { this.toast(n.text, n.level, n.ms); this.log(n.text); return; }
      case "picker": return void (this.state._renderPicker && this.state._renderPicker());
      case "export": return this.showExport(n.text, n.name);
      // While a job runs the Run screen shows elapsed time and progress that nothing else pushes,
      // so the view keeps its own repaint timer. It is presentation, which is why it lives here.
      case "driving": {
        if (this._tick) clearInterval(this._tick);
        this._tick = setInterval(() => { if (this.state.screen === "run") this.refresh(); }, 1500);
        return;
      }
      case "idle": {
        if (this._tick) { clearInterval(this._tick); this._tick = null; }
        return;
      }
      default: return;
    }
  }

  mount(container, doc = document) {
    installCss(CSS, doc);
    this.root = h("div", { class: "f-app" });
    this.$top = h("div", { class: "f-top" }, h("span", { class: "f-title" }, "TNR forge"), h("span", { class: "f-ver" }, this.version),
      this.exit ? h("button", { class: "f-exit", onClick: () => this.close() }, "Close") : null);
    this.$nav = h("nav", { class: "f-nav" });
    this.$auth = h("div", { class: "f-authbar" });
    this.$main = h("main", { class: "f-main" });
    this.$toast = h("div", { class: "f-toast" });
    this.root.append(this.$top, this.$nav, this.$auth, this.$main, this.$toast);
    if (this.auth && typeof this.auth.onChange === "function") this._unwatchAuth = this.auth.onChange(() => this.refresh());
    container.appendChild(this.root);
    const open = this.journal.resumable();
    if (open.length) this.state.screen = "jobs";
    this.refresh();
    this._persist();
    return this.root;
  }

  go(screen, patch = {}) { this.core.go(screen, patch); }

  refresh() {
    replace(this.$nav, Object.entries(SCREENS).map(([k, [label]]) => h("button", { "aria-current": this.state.screen === k ? "page" : null, onClick: () => this.go(k) }, label)));
    if (this.$auth) replace(this.$auth, this.authBanner());
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
  fail(context, e) { this.core.fail(context, e); }
  log(msg) { (this.logs ??= []).push({ at: new Date(this.now()).toISOString(), msg }); }

  // ------------------------------------------------------------------ auth health (brief D)
  /** Close the overlay and hand the carrier page back to the operator. */
  close() {
    if (!this.exit) return;
    if (this.state.running) return this.toast("a job is running; pause it before closing Forge", "warn");
    if (this._unwatchAuth) { this._unwatchAuth(); this._unwatchAuth = null; }
    if (this._tick) { clearInterval(this._tick); this._tick = null; }
    this.exit();
  }

  /** Wait for the page's auth runtime, then probe once. Called on mount. */
  establishAuth() { return this.core.establishAuth(); }
  /** Operator-driven re-check, from the auth banner. */
  recheckAuth() { return this.core.recheckAuth(); }

  /**
   * The standing answer to "can Forge do protected work right now", on every screen. It is a
   * separate line from job outcomes on purpose: "signed out" and "the read failed" are different
   * problems with different fixes, and 0.3.0 could only ever say the second one. The reasoning is
   * ForgeCore's (authFacts); only the markup is this function's.
   */
  authBanner() {
    const facts = authFacts(this.auth, this.authBusy);
    if (!facts) return null;
    const recheck = h("button", { disabled: this.authBusy, onClick: () => this.recheckAuth() }, this.authBusy ? "Checking\u2026" : "Re-check");
    if (facts.ready) {
      return h("div", { class: "f-banner ok" }, h("span", {}, "TNR session active. Protected reads and writes are available."), h("div", { class: "f-actions" }, recheck));
    }
    if (facts.probing) {
      return h("div", { class: "f-banner info" }, "Checking the TNR session\u2026");
    }
    return h("div", { class: "f-banner bad" },
      h("div", {}, h("b", {}, facts.signedOut ? "TNR authentication unavailable. " : "TNR authentication not confirmed. "),
        facts.signedOut
          ? "The game refused a protected procedure for this browser session. Protected reads and writes are blocked and nothing protected will be sent."
          : "Forge could not confirm a signed-in session, so protected reads and writes are blocked. This is not a read failure."),
      h("div", { class: "f-mute" }, "Sign in to The Ninja RPG in this browser (the page under Forge is the game itself \u2014 close Forge, sign in, reopen /forge), then re-check. Public capture-only manifests can still run."),
      facts.detail ? h("div", { class: "f-mute" }, facts.detail) : null,
      h("div", { class: "f-actions" }, recheck));
  }

  resumeBlockedReason(job) { return this.core.resumeBlockedReason(job); }
  blockedPaths(plan, manifest) { return this.core.blockedPaths(plan, manifest); }

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

  // ------------------------------------------------------------------ forwarded actions
  loadPicker(force) { return this.core.loadPicker(force); }
  selectManifest(entry) { return this.core.selectManifest(entry); }
  startJob() { return this.core.startJob(); }
  resumeJob(jobId) { return this.core.resumeJob(jobId); }
  requestPause() { return this.core.requestPause(); }
  adopt(jobId, idx, id) { return this.core.adopt(jobId, idx, id); }
  skip(jobId, idx) { return this.core.skip(jobId, idx); }
  resolveCaptures(jobId) { return this.core.resolveCaptures(jobId); }
  exportJob(jobId, opts) { return this.core.exportJob(jobId, opts); }

  async _persist() {
    try { if (navigator.storage && navigator.storage.persist) { this.state.persisted = await navigator.storage.persist(); const el = document.getElementById("f-persist"); if (el) el.textContent = String(this.state.persisted); } } catch { /* best effort */ }
  }
}
