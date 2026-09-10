import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync, writeFileSync, mkdirSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { checkReleasePin } from "../tools/check_release_pin.mjs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { JSDOM } from "jsdom";
import { Journal } from "../src/storage/journal.mjs";
import { CaptureCache } from "../src/storage/captures.mjs";
import { Budget } from "../src/budget/bucket.mjs";
import { CachedReader } from "../src/budget/reader.mjs";
import { Validator } from "../src/runner/validate.mjs";
import { Runner } from "../src/runner/runner.mjs";
import { Reconciler } from "../src/reconcile/reconciler.mjs";
import { CookieSession } from "../src/transport/session.mjs";
import { App } from "../src/ui/app.mjs";
import { entryTakeover, mountHost, onEntryPath, ENTRY_PATH, CARRIER_PATH } from "../src/ui/takeover.mjs";
import { FakeGame, FakeClient } from "./fakegame.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const SRC = join(dirname(fileURLToPath(import.meta.url)), "..", "src");
const SCHEMAS = JSON.parse(readFileSync(new URL("../src/runner/fields.json", import.meta.url), "utf8"));

function walk(dir) { return readdirSync(dir, { withFileTypes: true }).flatMap((d) => d.isDirectory() ? walk(join(dir, d.name)) : [join(dir, d.name)]); }

test("repo law: no innerHTML / outerHTML / insertAdjacentHTML anywhere in src", () => {
  for (const f of walk(SRC)) {
    const t = readFileSync(f, "utf8").replace(/\/\/[^\n]*/g, "");
    assert.ok(!/innerHTML|outerHTML|insertAdjacentHTML|document\.write/.test(t), f + " uses an HTML string sink");
  }
});

function dom() {
  const d = new JSDOM("<!doctype html><html><head></head><body></body></html>", { url: "https://www.theninja-rpg.com/forge" });
  const win = d.window;
  // jsdom lacks these; the app treats them as optional
  win.confirm = () => true;
  win.navigator.clipboard = { writeText: async () => {} };
  // Node 22 defines some of these as read-only getters on globalThis; defineProperty replaces them
  for (const [k, v] of Object.entries({ document: win.document, window: win, navigator: win.navigator, location: win.location, confirm: win.confirm, MutationObserver: win.MutationObserver, CSSStyleSheet: win.CSSStyleSheet, HTMLElement: win.HTMLElement })) {
    Object.defineProperty(globalThis, k, { value: v, configurable: true, writable: true });
  }
  return win;
}

function appWith({ game = new FakeGame(), storage = new MemoryStorage() } = {}) {
  const d = composeForTest({ game, storage });
  d.github = { list: async () => [{ name: "45_x.json", path: "push/45_x.json", sha: "s", size: 1, type: "file" }], text: async () => JSON.stringify({ items: [{ entity: "jutsu", slot: "create", name: "A", srcId: "a", data: { name: "A", hidden: true } }] }), put: async () => ({ sha: "abc" }) };
  const app = new App({ version: "test", storage, now: d.clock, ...d });
  return { app, game, storage, journal: d.journal, clock: d.clock };
}

test("entry takeover: /forge is recognised and the providerless 404 is emptied without innerHTML", () => {
  const win = dom();
  assert.equal(onEntryPath(win.location), true);
  assert.equal(onEntryPath({ pathname: "/" }), false);
  assert.equal(onEntryPath({ pathname: "/forge/x" }), true);
  assert.equal(ENTRY_PATH, "/forge");
  assert.equal(CARRIER_PATH, "/");
  win.stop = () => {};
  const { body, head } = entryTakeover(win.document, win);
  assert.ok(head.querySelector("meta[name=viewport]"));
  assert.equal(win.document.body, body);
  assert.equal(win.document.title, "TNR forge");
});

test("carrier mount: the overlay is added and removed without disturbing the page under it", () => {
  const win = dom();
  const doc = win.document;
  const appRoot = doc.createElement("div");
  appRoot.id = "__next";
  doc.body.appendChild(appRoot);
  const host = mountHost(doc, win);
  assert.equal(doc.getElementById("__next"), appRoot, "the game's React root is untouched");
  assert.equal(doc.body.contains(host.body), true);
  assert.equal(doc.documentElement.style.overflow, "hidden");
  host.release();
  assert.equal(doc.body.contains(host.body), false);
  assert.equal(doc.getElementById("__next"), appRoot);
  assert.equal(doc.documentElement.style.overflow, "", "the carrier's scroll lock is handed back");
});

test("mount renders the five screens, no SENT job -> Jobs shows empty state", () => {
  const win = dom();
  const { app } = appWith();
  app.mount(win.document.body, win.document);
  const nav = [...win.document.querySelectorAll(".f-nav button")].map((b) => b.textContent);
  assert.deepEqual(nav, ["Jobs", "Manifests", "Run", "Captures", "Settings"]);
  assert.match(win.document.querySelector(".f-main").textContent, /No jobs yet/);
  for (const s of ["manifests", "run", "captures", "settings"]) { app.go(s); assert.ok(win.document.querySelector(".f-main").childElementCount >= 1, s); }
});

test("a job with a SENT item shows the resume banner with 'Reconcile & resume'", () => {
  const win = dom();
  const { app, journal } = appWith();
  journal.open({ jobId: "j", manifestPath: "push/45_x.json", items: [{ entity: "jutsu", op: "create", name: "A", srcId: "a", payloadHash: "h" }] });
  journal.transition("j", 0, "SENT", { phase: "create" });
  app.mount(win.document.body, win.document);
  const banner = win.document.querySelector(".f-banner.warn");
  assert.ok(banner); assert.match(banner.textContent, /Open job/);
  assert.ok([...banner.querySelectorAll("button")].some((b) => b.textContent === "Reconcile & resume"));
});

test("Run screen renders item pills, error text, drift details and budget", async () => {
  const win = dom();
  const { app, journal } = appWith();
  journal.open({ jobId: "r", manifestPath: "push/45_x.json", items: [{ entity: "jutsu", op: "create", name: "A", srcId: "a", payloadHash: "h" }, { entity: "quest", op: "update", name: "Q", targetId: "q", payloadHash: "h" }] });
  journal.transition("r", 0, "FAILED", { error: "create refused: Not allowed" });
  journal.transition("r", 1, "SENT"); journal.transition("r", 1, "CONFIRMED"); journal.annotate("r", 1, { diffs: [{ key: "name", sent: "x", live: "y" }], verify: "drift" });
  app.mount(win.document.body, win.document);
  app.go("run", { jobId: "r" });
  const main = win.document.querySelector(".f-main");
  assert.ok(main.querySelector(".f-pill.FAILED")); assert.ok(main.querySelector(".f-pill.CONFIRMED"));
  assert.match(main.textContent, /create refused: Not allowed/);
  assert.match(main.textContent, /drift on 1 key/);
  assert.match(main.textContent, /nothing spent/);
});

test("Settings saves the PAT under the retained key and the export shows a textarea", () => {
  const win = dom();
  const { app, storage } = appWith();
  app.mount(win.document.body, win.document);
  app.go("settings");
  const main = win.document.querySelector(".f-main");
  main.querySelector("input[type=password]").value = "github_pat_test";
  [...main.querySelectorAll("button")].find((b) => b.textContent === "Save").click();
  assert.equal(JSON.parse(storage.getItem("tnr_bk_gh_v1")).pat, "github_pat_test");
  [...win.document.querySelectorAll("button")].find((b) => b.textContent === "Export journal as text").click();
  assert.ok(win.document.querySelector("textarea"));
});

test("capture-only manifest is presented and completed as read-only", async () => {
  const win = dom();
  const { app, game } = appWith();
  app.github.text = async () => JSON.stringify({ items: [], capture: { after: [{ proc: "jutsu.getAllNames", input: {} }] } });
  app.mount(win.document.body, win.document);
  app.go("manifests");
  await app.loadPicker(true);
  await app.selectManifest(app.state.picker[0]);
  const main = win.document.querySelector(".f-main");
  assert.match(main.textContent, /Read-only capture job/);
  assert.match(main.textContent, /zero mutations/);
  const start = [...main.querySelectorAll("button")].find((button) => button.textContent === "Run captures");
  assert.ok(start && !start.disabled);
  let prompt = "";
  app.confirm = (message, run) => { prompt = message; run(); };
  start.click();
  await new Promise((resolve) => setTimeout(resolve, 20));
  assert.match(prompt, /No mutations will be sent/);
  assert.doesNotMatch(prompt, /writes to the game/i);
  assert.deepEqual(game.calls.map((call) => call.path), ["jutsu.getAllNames"]);
  const job = app.journal.listJobs()[0];
  assert.equal(job.state, "DONE");
  app.go("run", { jobId: job.jobId });
  assert.match(win.document.querySelector(".f-main").textContent, /Read-only capture complete/);
  assert.match(win.document.querySelector(".f-main").textContent, /zero mutations were sent/);
});

test("a full-capture manifest is labelled before the run and reported body-by-body after it", async () => {
  const win = dom();
  const ASSET = { id: "XsLLy8awDAtaE6hXVIi_0", name: "Chase Alley Plate", type: "STATIC", image: "https://utfs.io/f/chase-alley.webp", folder: "scene", hidden: false };
  const { app, game } = appWith();
  game.seed("asset", { ...ASSET });
  app.github.text = async () => JSON.stringify({ items: [], capture: { after: [{ proc: "gameAsset.get", input: { id: ASSET.id }, persist: "full" }] } });
  app.mount(win.document.body, win.document);
  app.go("manifests");
  await app.loadPicker(true);
  await app.selectManifest(app.state.picker[0]);
  const main = win.document.querySelector(".f-main");
  // BEFORE the run: "1 full capture" is visibly not "1 capture", and it says where the body goes
  assert.match(main.textContent, /1 full capture/);
  assert.match(main.textContent, /written into the results bundle/);
  assert.match(main.textContent, /zero mutations/);
  let prompt = "";
  app.confirm = (message, run) => { prompt = message; run(); };
  [...main.querySelectorAll("button")].find((b) => b.textContent === "Run captures").click();
  await new Promise((resolve) => setTimeout(resolve, 40));
  assert.match(prompt, /1 full capture/);
  assert.match(prompt, /No mutations will be sent/);
  assert.deepEqual(game.calls.map((c) => c.path), ["gameAsset.get"]);

  const job = app.journal.listJobs()[0];
  app.go("run", { jobId: job.jobId });
  let text = win.document.querySelector(".f-main").textContent;
  assert.match(text, /Read-only capture complete/);
  assert.match(text, /1\/1 full record body persisted into the bundle/);
  assert.match(text, /zero mutations were sent/);
  assert.match(text, /body persisted/);

  // and once the snapshot is gone, the same screen stops claiming the bundle carries it
  await app.cache.deleteSnapshot(`${job.jobId}::after::0`);
  await app.exportJob(job.jobId);
  app.refresh();
  text = win.document.querySelector(".f-main").textContent;
  assert.match(text, /Read-only capture incomplete/);
  assert.match(text, /could not be persisted/);
  assert.match(text, /capture snapshot .* is gone/);
  assert.match(text, /zero mutations were sent/);
  assert.doesNotMatch(text, /Read-only capture complete/);
  assert.equal(game.calls.length, 1, "nothing on this screen ever goes back to the game for a body");
});

test("Captures screen lists full-capture snapshots apart from the read cache", async () => {
  const win = dom();
  const ASSET = { id: "XsLLy8awDAtaE6hXVIi_0", name: "Chase Alley Plate", type: "STATIC", image: "https://utfs.io/f/chase-alley.webp", folder: "scene", hidden: false };
  const { app, game } = appWith();
  game.seed("asset", { ...ASSET });
  app.github.text = async () => JSON.stringify({ items: [], capture: { after: [{ proc: "gameAsset.get", input: { id: ASSET.id }, persist: "full" }] } });
  app.mount(win.document.body, win.document);
  app.go("manifests");
  await app.loadPicker(true);
  await app.selectManifest(app.state.picker[0]);
  app.confirm = (_m, run) => run();
  [...win.document.querySelector(".f-main").querySelectorAll("button")].find((b) => b.textContent === "Run captures").click();
  await new Promise((resolve) => setTimeout(resolve, 40));

  app.go("captures");
  await new Promise((resolve) => setTimeout(resolve, 20));
  const text = win.document.querySelector(".f-main").textContent;
  assert.match(text, /Full-capture snapshots/);
  assert.match(text, /1 snapshot/);
  assert.match(text, /never invalidated by a write/);
  assert.match(text, /::after::0/, "the snapshot is listed by its occurrence key, not by path:id");
  // clearing the READ CACHE is offered separately from deleting evidence, and does not delete it
  [...win.document.querySelectorAll("button")].find((b) => b.textContent === "Clear all").click();
  await new Promise((resolve) => setTimeout(resolve, 20));
  assert.equal((await app.cache.listSnapshots()).length, 1, "clearing the read cache leaves the snapshots");
  assert.deepEqual(await app.cache.list(), []);
});

test("Manifests: list, select, plan shown, Start job runs to DONE through the runner", async () => {
  const win = dom();
  const { app, game } = appWith();
  app.mount(win.document.body, win.document);
  app.go("manifests");
  await app.loadPicker(true);
  const row = win.document.querySelector(".f-main .f-row.f-tap");
  assert.ok(row); assert.match(row.textContent, /#45/);
  await app.selectManifest(app.state.picker[0]);
  assert.match(win.document.querySelector(".f-main").textContent, /1 items/);
  const start = [...win.document.querySelectorAll("button")].find((b) => b.textContent === "Start job");
  assert.ok(start && !start.disabled);
  await app.startJob();
  await new Promise((r) => setTimeout(r, 10));
  assert.equal(game.count("jutsu"), 1);
  const jobs = app.journal.listJobs();
  assert.equal(jobs.length, 1); assert.equal(jobs[0].state, "DONE"); assert.equal(jobs[0].items[0].state, "VERIFIED");
});


test("a finished-but-unverified job is never shown or exported as success", async () => {
  const win = dom();
  const game = new FakeGame();
  const { app } = appWith({ game });
  // the read-back disagrees with what was sent
  const orig = game.handle.bind(game);
  game.handle = (p, i) => { const r = orig(p, i); if (p === "jutsu.get" && r && r.data) r.data = { ...r.data, name: "Someone renamed it" }; return r; };
  app.mount(win.document.body, win.document);
  app.go("manifests");
  await app.loadPicker(true);
  await app.selectManifest(app.state.picker[0]);
  let exported = null;
  app.showExport = (text, name) => { exported = JSON.parse(text); };
  await app.startJob();
  await new Promise((r) => setTimeout(r, 10));
  const job = app.journal.listJobs()[0];
  assert.equal(job.state, "INCOMPLETE", "a drifted read-back is not DONE");
  assert.equal(job.items[0].verify, "drift");
  const main = win.document.querySelector(".f-main");
  assert.match(main.textContent, /Finished UNVERIFIED/);
  assert.match(main.textContent, /not proven/);
  assert.ok([...win.document.querySelectorAll("button")].some((b) => b.textContent === "Re-read unverified items"), "still resumable");
  assert.ok(!/^Verified\./m.test(main.textContent));
  // the bundle is still exported as evidence, and says what it is
  assert.ok(exported, "an incomplete job still exports its evidence");
  assert.equal(exported.outcome, "unverified");
  assert.equal(exported.state, "INCOMPLETE");
  assert.equal(exported.postflight.diff, 1);
  assert.equal(exported.postflight.match, 0);
  assert.equal(exported.postflight.unresolved, 1);
});


test("release pin: the forge loader cannot silently float on a branch", () => {
  const problems = checkReleasePin();
  const blockers = problems.filter((p) => p.level === "blocker");
  assert.deepEqual(blockers, [], blockers.map((b) => b.text).join("; "));
  // the one thing this branch cannot do for itself: installing a workflow needs dauntless (the PAT
  // cannot push .github/workflows/). It is reported, not hidden, and this assertion goes green by
  // itself once the staged copy is installed.
  for (const p of problems) assert.match(p.text, /^\.github\/workflows\/release_pin\.yml does not pin forge/, p.text);
});

test("release pin: pinning turns the branch URL into a commit URL and drops the marker", () => {
  // exercise the loader-rewrite the workflow performs, on a copy, so a regression in either the
  // loader's shape or the check's rules is caught here rather than after a release
  const root = mkdtempSync(join(tmpdir(), "forge-pin-"));
  mkdirSync(join(root, "forge"), { recursive: true });
  mkdirSync(join(root, "state", "staged_workflows"), { recursive: true });
  const repo = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
  const loader = readFileSync(join(repo, "forge_loader_user.js"), "utf8");
  const pkg = JSON.parse(readFileSync(join(repo, "forge", "package.json"), "utf8"));
  const sha = "a".repeat(40);
  // model the loader AS PROMOTED, exactly as .github/scripts/pin_release.py leaves it: the bundle
  // URL becomes the merge commit, BOTH staging markers are removed, and @version is synced from
  // forge/package.json. A branch that is staging the next release carries @x-release-pending and
  // is legitimately allowed to lag on @version, so a fixture that kept the marker would be
  // asserting against the staged state, not the released one.
  const pinned = loader
    .replace(/(\/\/ @require\s+)\S*forge_bundle\.js\S*/, `$1https://cdn.jsdelivr.net/gh/perseverance484/tnr-tools@${sha}/forge_bundle.js`)
    .replace(/^\/\/ @x-unpinned-until-release.*\n/m, "")
    .replace(/^\/\/ @x-release-pending.*\n/m, "")
    .replace(/(\/\/ @version\s+)\S+/, `$1${pkg.version}`);
  writeFileSync(join(root, "forge_loader_user.js"), pinned);
  writeFileSync(join(root, "forge", "package.json"), JSON.stringify(pkg));
  writeFileSync(join(root, "state", "staged_workflows", "release_pin.yml"), readFileSync(join(repo, "state", "staged_workflows", "release_pin.yml"), "utf8"));
  assert.deepEqual(checkReleasePin({ root }), [], "a pinned loader with the staged workflow is clean");
  // and the reverse: a floating URL with no marker is a blocker
  writeFileSync(join(root, "forge_loader_user.js"), pinned.replace(sha, "some-branch"));
  assert.match(checkReleasePin({ root }).map((p) => p.text).join(";"), /floats on "some-branch" with no @x-unpinned-until-release marker/);
  // and a version that did not rise with the bundle is a blocker
  writeFileSync(join(root, "forge_loader_user.js"), pinned.replace(/(\/\/ @version\s+)\S+/, "$10.0.1"));
  assert.match(checkReleasePin({ root }).map((p) => p.text).join(";"), /@version 0\.0\.1 != forge\/package\.json/);
  rmSync(root, { recursive: true, force: true });
});


test("no test can open a socket, and no source reaches a host it should not", () => {
  // The suite's whole premise is that nothing here can touch the live game. Two greps keep it
  // that way: no test may import a network module or call a global fetch (every request goes
  // through an injected fetchImpl), and src/ may name only the same-origin API paths and the two
  // hosts it is allowed to reach - jsDelivr is the loader's business, api.github.com is the
  // manifest picker's.
  const testDir = dirname(fileURLToPath(import.meta.url));
  const self = "ui.test.mjs"; // this file carries the patterns as literals; it would match itself
  for (const f of readdirSync(testDir).filter((n) => n.endsWith(".mjs") && n !== self)) {
    const t = readFileSync(join(testDir, f), "utf8").replace(/\/\/[^\n]*/g, "");
    assert.ok(!/from "node:(net|http|https|dns|tls)"|require\("node:(net|http|https)"\)|undici/.test(t), f + " imports a network module");
    assert.ok(!/(^|[^.\w])fetch\(/.test(t.replace(/fetchImpl/g, "")), f + " calls a global fetch");
  }
  for (const f of walk(SRC)) {
    const t = readFileSync(f, "utf8").replace(/\/\/[^\n]*/g, "");
    for (const host of [...t.matchAll(/https?:\/\/([A-Za-z0-9.-]+)/g)].map((m) => m[1])) {
      assert.ok(["api.github.com", "cdn.jsdelivr.net"].includes(host), `${f} names host ${host}`);
    }
  }
});

test("a screen that throws is shown as an error banner, never a blank page", () => {
  const win = dom();
  const { app } = appWith();
  app.mount(win.document.body, win.document);
  app.journal.listJobs = () => { throw new Error("boom"); };
  app.go("jobs");
  assert.match(win.document.querySelector(".f-main").textContent, /failed to render.*boom/s);
});
