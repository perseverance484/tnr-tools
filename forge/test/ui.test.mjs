import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
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
import { takeover, onHostPath, HOST_PATH } from "../src/ui/takeover.mjs";
import { FakeGame, FakeClient } from "./fakegame.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";

const SRC = join(dirname(fileURLToPath(import.meta.url)), "..", "src");
const SCHEMAS = JSON.parse(readFileSync(new URL("../../skills/building-tnr-content/data/45d_DATA_entity_schemas.json", import.meta.url), "utf8"));

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
  const clock = fakeClock();
  const journal = new Journal(storage, clock);
  const cache = new CaptureCache(new IDBFactory(), clock);
  const budget = new Budget({ storage, clock, sleep: async (ms) => clock.tick(ms) });
  const client = new FakeClient(game);
  const reader = new CachedReader({ client, cache, budget });
  const reconciler = new Reconciler({ storage, reader, clock });
  const validator = new Validator(SCHEMAS);
  const runner = new Runner({ journal, client, reader, cache, budget, validator, storage, reconciler });
  const session = new CookieSession({ fetchImpl: async () => new Response("[]") });
  const github = { list: async () => [{ name: "45_x.json", path: "push/45_x.json", sha: "s", size: 1, type: "file" }], text: async () => JSON.stringify({ items: [{ entity: "jutsu", slot: "create", name: "A", srcId: "a", data: { name: "A", hidden: true } }] }), put: async () => ({ sha: "abc" }) };
  const app = new App({ version: "test", storage, journal, cache, budget, reader, client, session, runner, reconciler, github, validator, now: clock });
  return { app, game, storage, journal, clock };
}

test("takeover: host path check and document replacement without innerHTML", () => {
  const win = dom();
  assert.equal(onHostPath(win.location), true);
  assert.equal(onHostPath({ pathname: "/" }), false);
  assert.equal(onHostPath({ pathname: "/forge/x" }), true);
  assert.equal(HOST_PATH, "/forge");
  win.stop = () => {};
  const { body, head } = takeover(win.document, win);
  assert.ok(head.querySelector("meta[name=viewport]"));
  assert.equal(win.document.body, body);
  assert.equal(win.document.title, "TNR forge");
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

test("a screen that throws is shown as an error banner, never a blank page", () => {
  const win = dom();
  const { app } = appWith();
  app.mount(win.document.body, win.document);
  app.journal.listJobs = () => { throw new Error("boom"); };
  app.go("jobs");
  assert.match(win.document.querySelector(".f-main").textContent, /failed to render.*boom/s);
});
