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
import { blockedPaths, imagePicks, resumeBlockedReason, runHeadline, unusablePicks } from "./facts.mjs";
import { resolveCaptures, buildBundle, repoSyncReady, inboxPath } from "./results.mjs";
import { prepareImagePack, commitImagePack, packGateProblems } from "./imagepack.mjs";
import { packBinds } from "../runner/imgpack.mjs";

// The core's dependency contract, named rather than absorbed. `Object.assign(this, d)` used to
// take whatever the composition handed over, which meant the seam could widen silently: a second
// shell could pass a view helper and the core would keep it. Anything not on these lists is
// ignored, so widening the surface is now a deliberate edit of this file.
// `assetCache` and `digest` are REQUIRED, not optional. A repo-backed image pack whose digest
// cannot be computed must fail, not fall back to using the bytes unverified, and a consumer that
// forgets to wire them should learn that here rather than at the moment an operator taps Start.
export const REQUIRED_DEPS = ["version", "storage", "journal", "cache", "repoCache", "assetCache", "digest", "runner", "github", "validator"];
export const OPTIONAL_DEPS = ["budget", "reader", "client", "session", "auth", "reconciler", "uploader", "now"];

// The machine state the core owns. Presentation state (a search box's contents, a render callback,
// whether the browser granted persistent storage) belongs to whichever shell is drawing, and the
// golden test proves none of it lands here.
const STATE_KEYS = ["screen", "jobId", "picker", "pickerAt", "pickerError", "selected", "running", "runningNote"];

// The screens a shell may route to, and the ONLY keys go() will accept in a patch. go() used to be
// `Object.assign(this.state, patch, { screen })` with `patch` unconstrained, which meant any shell
// could mint a new key on core machine state through the public API and neither the snapshot
// golden (it copies a fixed key set) nor the render test (it exercises today's calls) would notice.
// Found by independent re-review. Widening either list is now a deliberate edit of this file.
export const SCREENS = ["jobs", "manifests", "run", "captures", "settings"];
export const GO_PATCH_KEYS = ["jobId"];

export class ForgeCore {
  /**
   * @param {object} d see REQUIRED_DEPS / OPTIONAL_DEPS. Unknown keys are ignored; a missing
   *   required dependency throws rather than degrading — `repoCache` in particular used to fall
   *   back to the game capture cache, which silently reversed the Phase 0 storage isolation.
   */
  constructor(d) {
    const missing = REQUIRED_DEPS.filter((k) => d[k] == null);
    if (missing.length) throw new Error(`ForgeCore is missing required dependencies: ${missing.join(", ")}`);
    for (const k of [...REQUIRED_DEPS, ...OPTIONAL_DEPS]) if (d[k] != null) this[k] = d[k];
    this.now = d.now ?? (() => Date.now());
    this.authBusy = false;
    this.state = { screen: "jobs", jobId: null, picker: null, pickerAt: null, pickerError: null, selected: null, running: null, runningNote: "" };
    this._listeners = new Set();
  }

  /** The public action surface. Pinned by the golden test so a shell cannot quietly grow one. */
  static get ACTIONS() {
    return [
      "adopt", "blockedPaths", "changed", "clearSelection", "drive", "establishAuth", "exportJob",
      "fail", "go", "loadPicker", "notify", "prepareImages", "recheckAuth", "requestPause",
      "resolveCaptures", "resumeBlockedReason", "resumeJob", "say", "selectManifest", "skip",
      "snapshot", "startJob", "subscribe",
    ];
  }

  /**
   * A serializable picture of machine state. This is what a shell renders from and what a headless
   * host inspects: JSON only, no functions, no nodes, no dependency handles. If rendering can add
   * a key here, the boundary has widened, which is exactly what the golden test watches for.
   */
  snapshot() {
    const out = {};
    for (const k of STATE_KEYS) out[k] = this.state[k] === undefined ? null : this.state[k];
    return JSON.parse(JSON.stringify(out));
  }

  /** Machine-state keys, so a shell can assert it is not writing outside them. */
  static get STATE_KEYS() { return [...STATE_KEYS]; }

  /** Drop the current manifest selection. A screen must not assign state.selected itself. */
  clearSelection() { this.state.selected = null; this.changed(); }

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
          // Repository text goes to the repository cache, never the game capture DB. There is no
          // fallback on purpose: a consumer that omits repoCache fails in the constructor rather
          // than quietly putting manifest text back into the capture store.
          const hit = await this.repoCache.get("github.contents", key);
          const text = hit ? hit.data : await this.github.text(e.path);
          if (!hit) await this.repoCache.put({ path: "github.contents", id: key, data: text });
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
      this.state.selected = { entry, text, manifest, plan, problems, images, pack: manifest.imagePack ?? null, packResult: null };
      this._scopePackProvenance(this.state.selected.pack);
      this.state.selected.blocked = this.blockedPaths(plan, manifest);
      this.changed();
      // The operator flow is "open the manifest, Forge fetches and verifies, then Start". Opening is
      // therefore where the fetch belongs - not Start, which must only ever GATE. A failure here is
      // reported and leaves Start refused; it never throws out of selection.
      if (this.state.selected.pack) await this.prepareImages();
    } catch (e) { this.fail("select manifest", e instanceof ManifestError ? e : e); }
  }

  /**
   * Fetch and verify every repo-backed image the selected manifest binds. Safe to call again: it
   * clears what it is about to replace first, so a re-fetch cannot leave a half-verified mixture.
   * @param {boolean} [force]  ignore the content cache and go to the repository
   */
  async prepareImages(force = false) {
    const s = this.state.selected;
    if (!s || !s.pack) return null;
    return this._queuePack(() => this._prepareImages(s, force));
  }

  /**
   * One preparation at a time. Two of them racing would both write `runner.files`, and the loser's
   * bytes could land under a name the winner had already verified. Queuing rather than dropping the
   * second call also means a re-tap of Re-fetch while one is in flight actually happens.
   */
  _queuePack(fn) {
    const next = () => fn();
    this._packChain = (this._packChain ?? Promise.resolve()).then(next, next);
    return this._packChain;
  }

  /**
   * The currency token a preparation commits against. Bumped by every act that changes which pack is
   * authoritative — selecting a manifest, resuming a job. A preparation captures it on entry and
   * installs nothing unless it is still the same number, which is what makes an in-flight pass for a
   * manifest the operator has already navigated away from harmless rather than merely discarded
   * (independent review F2).
   */
  _packEpoch = 0;

  /**
   * Provenance belongs to the manifest currently open. A name the new pack does not bind must lose
   * both its record AND the File that record vouched for: otherwise selecting manifest B after
   * preparing manifest A leaves A's digest recorded under a shared logical filename, and the
   * content-keyed upload reuse would hand B the URL of A's picture.
   */
  _scopePackProvenance(pack) {
    this._packEpoch += 1;
    for (const name of [...this.runner.imgProvenance.keys()]) {
      if (packBinds(pack, name)) continue;
      this.runner.imgProvenance.delete(name);
      this.runner.files.delete(name);
    }
    return this._packEpoch;
  }

  async _prepareImages(s, force) {
    if (this.state.selected !== s) return null;
    const epoch = this._packEpoch;
    this._preparing = true;
    this.changed();
    try {
      const result = await prepareImagePack(this, { pack: s.pack, names: s.images, force });
      // THE COMMIT POINT, and the only one. Nothing above this line has touched runner state, so a
      // pass that is no longer current installs nothing at all rather than writing first and being
      // discarded afterwards — the race review F2 reproduced by holding one manifest's fetch open
      // across a selection change.
      if (this.state.selected !== s || this._packEpoch !== epoch) {
        return { ref: result.ref, entries: result.entries, unbound: result.unbound, ok: false, stale: true };
      }
      commitImagePack(this.runner, { pack: s.pack, names: s.images, staged: result.staged });
      // `staged` carries File objects and never reaches machine state: state.selected is snapshotted
      // as JSON, and a dependency-shaped value there is exactly what the core golden watches for.
      s.packResult = { ref: result.ref, entries: result.entries, unbound: result.unbound, ok: result.ok };
      const bad = result.entries.filter((e) => e.state !== "ready");
      if (!bad.length) {
        this.say(`${result.entries.length} repo-backed image(s) verified against ${s.pack.ref.slice(0, 7)}`, "ok");
      } else {
        this.say(`${bad.length} of ${result.entries.length} repo-backed image(s) could not be verified: ${bad.map((e) => `${e.name}: ${e.error}`).join(" | ")}`, "bad", 12000);
      }
      return result;
    } catch (e) {
      // Fail closed and visibly. prepareImagePack() already reports per-image failures, so reaching
      // here means something structural; the gate in startJob() refuses the job either way.
      this.fail("prepare repo-backed images", e);
      if (this.state.selected === s) s.packResult = { ref: s.pack.ref, entries: [], unbound: [], ok: false, error: (e && e.message) || String(e) };
      return null;
    } finally {
      this._preparing = false;
      this.changed();
    }
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
    // The image ledger, re-read at the moment of the tap for the same reason the auth gate is:
    // the screen that disabled Start may have been drawn before the operator picked, replaced or
    // lost a file. A shell that never drew the picker at all is gated here too - the check belongs
    // to the machine, not to whoever is drawing it. This is the gate that would have stopped the
    // five Godstorm avatar edits before the job opened instead of at their uploads.
    const badImgs = unusablePicks(imagePicks(s.images, this.runner.files, s.manifest.imgSizes, "imageUploader"));
    if (badImgs.length) {
      this.say(`${badImgs.length} image selection(s) do not match the manifest: ${badImgs.map((p) => p.problems[0] ?? `${p.name} is not picked`).join("; ")}. Nothing was sent.`, "bad", 12000);
      return this.changed();
    }
    // The pack gate, IN ADDITION to the ledger gate above and never instead of it. The byte ledger
    // proves the file is the right SIZE; only this proves it is the right FILE. It is read from the
    // runner's own maps at the moment of the tap, not from what the preparation reported when the
    // screen was drawn, so a manifest re-selected under a new pack, a cleared cache or a preparation
    // that silently failed cannot ride an earlier green report into a live run.
    const packProblems = packGateProblems(s.pack, s.images, this.runner);
    if (packProblems.length) {
      this.say(`${packProblems.length} repo-backed image(s) are not verified: ${packProblems.join("; ")}. Nothing was sent.`, "bad", 12000);
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
    // A reload empties runner.files, so a resumed job that still owes an image upload used to be
    // unresumable without the operator finding the file again. A pack makes it deterministic: the
    // bytes are named, so fetch and verify them before the run touches an item. attach() has already
    // refused a manifest whose identity - pack included - differs from the one the job was opened on.
    try {
      const attached = this.runner.manifests.get(jobId);
      const pack = attached && attached.manifest ? attached.manifest.imagePack : null;
      const epoch = this._scopePackProvenance(pack);
      if (pack) {
        const names = [...new Set((attached.order || []).flatMap((it) => collectRefs(it.data).filter((r) => r.pfx === "img").map((r) => r.key)))];
        const result = await this._queuePack(async () => {
          const r = await prepareImagePack(this, { pack, names });
          // Same commit discipline as selection: a resume whose preparation outlived a newer
          // selection installs nothing, and the caller below refuses rather than running.
          if (this._packEpoch !== epoch) return { ...r, ok: false, stale: true, staged: [] };
          commitImagePack(this.runner, { pack, names, staged: r.staged });
          return r;
        });
        const bad = result.entries.filter((e) => e.state !== "ready");
        if (bad.length || result.stale) {
          const detail = result.stale
            ? "the selection changed while the images were being fetched, so nothing was installed"
            : bad.map((e) => `${e.name}: ${e.error}`).join(" | ");
          this.say(`resume refused: repo-backed image(s) could not be verified: ${detail}. Nothing was sent.`, "bad", 12000);
          return this.changed();
        }
      }
    } catch (e) { return this.fail("resume: prepare repo-backed images", e); }
    this.go("run", { jobId });
    const hasSent = job.items.some((i) => i.state === "SENT");
    await this.drive(jobId, () => (hasSent ? this.runner.resume(jobId) : this.runner.run(jobId)));
  }

  /**
   * Route to a screen, optionally carrying the job it is about. Fails closed on an unknown screen
   * or an unknown patch key rather than silently creating machine state.
   */
  go(screen, patch = {}) {
    if (!SCREENS.includes(screen)) throw new Error(`unknown screen ${JSON.stringify(screen)}`);
    if (patch === null || typeof patch !== "object" || Array.isArray(patch)) throw new TypeError("go() patch must be an object");
    const unknown = Object.keys(patch).filter((k) => !GO_PATCH_KEYS.includes(k));
    if (unknown.length) throw new Error(`go() refuses unknown state keys: ${unknown.join(", ")}; add a named action instead`);
    for (const k of GO_PATCH_KEYS) if (k in patch) this.state[k] = patch[k];
    this.state.screen = screen;
    this.changed();
  }

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
