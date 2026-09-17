// The Phase 0 acceptance test: a host with NO DOM drives a complete Forge lifecycle.
//
// This suite deliberately never imports jsdom and never touches globalThis.document. If ForgeCore
// reacquires a dependency on the DOM, window, userscript takeover or a presentation class, this
// file is where it fails — which is the whole reason the extraction was worth doing.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { ForgeCore } from "../src/core/core.mjs";
import { composeForTest } from "./compose.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { FakeGame } from "./fakegame.mjs";
import { writeGh } from "../src/storage/compat.mjs";

const SRC = join(dirname(fileURLToPath(import.meta.url)), "..", "src");
function walk(dir) { return readdirSync(dir, { withFileTypes: true }).flatMap((d) => d.isDirectory() ? walk(join(dir, d.name)) : [join(dir, d.name)]); }

const MANIFEST = JSON.stringify({
  items: [
    { entity: "jutsu", slot: "create", name: "Headless A", srcId: "hl-a", data: { name: "Headless A", hidden: true } },
    { entity: "jutsu", slot: "create", name: "Headless B", srcId: "hl-b", data: { name: "Headless B", hidden: true } },
  ],
});
const ENTRY = { name: "45_headless.json", path: "push/45_headless.json", sha: "hlsha", size: 64, type: "file" };

function headlessCore({ sync = true } = {}) {
  const storage = new MemoryStorage();
  const clock = fakeClock();
  // Repository sync on, so the export path under test is the one that commits the bundle rather
  // than the one that hands text back to a view.
  if (sync) writeGh(storage, { on: true, pat: "fake-pat" });
  const d = composeForTest({ game: new FakeGame(), storage, idb: new IDBFactory(), clock });
  const committed = [];
  d.github = {
    list: async () => [ENTRY],
    text: async () => MANIFEST,
    put: async (path, text) => { committed.push({ path, text }); return { sha: "committedsha" }; },
  };
  const notes = [];
  const core = new ForgeCore({ version: "headless", storage, now: clock, ...d });
  core.subscribe((n) => notes.push(n));
  return { core, notes, committed, storage, journal: d.journal };
}

test("ForgeCore carries no DOM, window, takeover or presentation dependency", () => {
  for (const f of walk(join(SRC, "core"))) {
    const text = readFileSync(f, "utf8").replace(/\/\/[^\n]*/g, "").replace(/\/\*[\s\S]*?\*\//g, "");
    for (const forbidden of ["document", "window.", "globalThis.document", "takeover", "f-banner", "createElement"]) {
      assert.ok(!text.includes(forbidden), `${f} reaches for ${forbidden}`);
    }
    assert.ok(!/from "\.\.\/ui\//.test(text), `${f} imports the view layer`);
    assert.ok(!/from "\.\.\/hosts\//.test(text), `${f} imports a host adapter`);
  }
});

test("a non-DOM host drives select -> start -> run -> resolve -> export end to end", async () => {
  assert.equal(typeof globalThis.document, "undefined", "this suite must run without a DOM");
  const { core, notes, committed, journal } = headlessCore();

  await core.loadPicker(true);
  assert.equal(core.state.picker.length, 1);
  assert.equal(core.state.picker[0].number, 45);

  await core.selectManifest({ ...ENTRY, number: 45, text: MANIFEST });
  assert.equal(core.state.selected.plan.length, 2);
  assert.deepEqual(core.state.selected.problems, []);
  assert.deepEqual(core.state.selected.blocked, []);

  await core.startJob();

  assert.equal(core.state.screen, "run");
  assert.equal(core.state.running, null, "the core returns to idle when the run finishes");
  const jobId = core.state.jobId;
  const job = journal.get(jobId);
  assert.equal(job.state, "DONE");
  assert.ok(job.items.every((i) => i.state === "VERIFIED"), "every item verified against the fake game");

  // the results bundle was committed to the repository inbox, in harvest's own shape
  assert.equal(committed.length, 1);
  assert.match(committed[0].path, /^harvests\/inbox\/tnr_results_\d+\.json$/);
  const bundle = JSON.parse(committed[0].text);
  assert.equal(bundle.outcome, "success");
  assert.equal(bundle.state, "DONE");
  assert.equal(bundle.entries.length, 2);
  assert.deepEqual(bundle.entries.map((e) => e.state), ["ok", "ok"]);
  assert.deepEqual(bundle.entries.map((e) => e.verdict), ["match", "match"]);
  assert.equal(bundle.postflight.match, 2);
  assert.equal(bundle.postflight.unresolved, 0);

  // and the host was told what happened, as facts rather than markup
  const kinds = notes.map((n) => n.type);
  assert.ok(kinds.includes("driving"), "a host can show progress");
  assert.ok(kinds.includes("idle"), "a host can stop showing progress");
  const headline = notes.filter((n) => n.type === "message").map((n) => n.text);
  assert.ok(headline.some((t) => /^job DONE \(success\)/.test(t)), "the run headline is a plain sentence");
  for (const n of notes) assert.ok(typeof n.type === "string" && !("element" in n), "notifications carry no nodes");
});

test("with repository sync off the bundle is handed to the host instead of committed", async () => {
  const { core, notes, committed } = headlessCore({ sync: false });
  await core.selectManifest({ ...ENTRY, number: 45, text: MANIFEST });
  await core.startJob();
  assert.equal(committed.length, 0, "nothing may be committed when sync is off");
  const exported = notes.find((n) => n.type === "export");
  assert.ok(exported, "the host is handed the bundle");
  assert.match(exported.name, /^tnr_results_\d+\.json$/);
  assert.equal(JSON.parse(exported.text).outcome, "success");
});

test("a host that throws on every notification cannot break a run", async () => {
  const { core, journal } = headlessCore();
  core.subscribe(() => { throw new Error("hostile host"); });
  await core.selectManifest({ ...ENTRY, number: 45, text: MANIFEST });
  await core.startJob();
  assert.equal(journal.get(core.state.jobId).state, "DONE");
});

test("the core refuses a second concurrent job and says so", async () => {
  const { core, notes } = headlessCore();
  core.state.running = "already";
  await core.drive("other", async () => { throw new Error("must not run"); });
  assert.ok(notes.some((n) => n.type === "message" && n.text === "a job is already running"));
});
