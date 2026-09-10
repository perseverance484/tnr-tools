// A forge results bundle must be readable by the repository's own ingestion path, and must not be
// able to report a bad run as a good one there (readiness brief section 9).
//
// These tests run a job through the shipped composition against the fake game, export the bundle
// the app would commit to harvests/inbox/, and then run the REAL
// skills/building-tnr-content/scripts/harvest.py over it, asserting the verdicts it prints and the
// exit code it returns. No network, no live game: harvest.py reads a local file.

import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, writeFileSync, readFileSync, rmSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { App } from "../src/ui/app.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const HARVEST = join(HERE, "..", "..", "skills", "building-tnr-content", "scripts", "harvest.py");

function python() {
  for (const bin of ["python3", "python"]) {
    try { execFileSync(bin, ["-c", "print(1)"], { stdio: "pipe" }); return bin; }
    catch { /* try the next one */ }
  }
  return null;
}

/** Run one harvest.py subcommand over a bundle. Returns {code, out}. */
function harvest(bin, cmd, file, args = []) {
  try { return { code: 0, out: execFileSync(bin, [HARVEST, cmd, file, ...args], { encoding: "utf8" }) }; }
  catch (e) { return { code: e.status ?? -1, out: (e.stdout ?? "") + (e.stderr ?? "") }; }
}

const jutsu = (name, extra = {}) => ({ entity: "jutsu", slot: "create", name, srcId: name.toLowerCase(), data: { name, description: "d", hidden: true, ...extra } });

/**
 * One job carrying every outcome a bundle has to be able to express: a clean write, a write whose
 * read-back disagreed, a write whose read-back could not be read, and a refusal.
 */
async function bundleWithEveryOutcome() {
  const game = new FakeGame();
  const storage = new MemoryStorage();
  const d = composeForTest({ game, storage });
  const marks = { drift: null, unread: null };
  const orig = game.handle.bind(game);
  game.handle = (p, i) => {
    if (p === "jutsu.update" && i?.data?.name === "B") marks.drift = i.id;
    if (p === "jutsu.update" && i?.data?.name === "C") marks.unread = i.id;
    const r = orig(p, i);
    if (p === "jutsu.get" && marks.unread && i?.id === marks.unread) return { ok: true, data: null };
    if (p === "jutsu.get" && marks.drift && i?.id === marks.drift && r && r.data) r.data = { ...r.data, name: "Someone renamed it" };
    return r;
  };
  const manifest = {
    capture: { before: [{ proc: "jutsu.getAllNames" }], after: [{ proc: "jutsu.getAllNames" }] },
    items: [jutsu("A"), jutsu("B"), jutsu("C"), jutsu("D", { nmae: "typo" })],
  };
  d.runner.plan(manifest, { jobId: "hv", manifestPath: "push/99_harvest.json", manifestNumber: 99 });
  const summary = await d.runner.run("hv");

  const app = new App({ version: "forge 0.3.0", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
  let text = null;
  app.showExport = (t) => { text = t; };
  await app.exportJob("hv");
  return { summary, bundle: JSON.parse(text), text, game };
}

test("a forge bundle expresses match, drift, unread and failure distinctly", async () => {
  const { summary, bundle } = await bundleWithEveryOutcome();
  assert.equal(summary.state, "INCOMPLETE");
  assert.equal(summary.outcome, "failed", "one item was refused");
  const by = Object.fromEntries(bundle.entries.map((e) => [e.name, e]));
  assert.equal(by.A.state, "ok"); assert.equal(by.A.verdict, "match"); assert.deepEqual(by.A.asserted.fail, []);
  assert.equal(by.B.state, "ok"); assert.equal(by.B.verdict, "drift"); assert.equal(by.B.asserted.fail[0].k, "name");
  assert.equal(by.C.state, "ok"); assert.equal(by.C.verdict, "unread");
  assert.equal(by.D.state, "error"); assert.match(by.D.detail, /unknown key "nmae"/);
  // the journal's own vocabulary rides along, so nothing is lost in the translation
  assert.deepEqual(bundle.entries.map((e) => e.forgeState), ["VERIFIED", "CONFIRMED", "CONFIRMED", "FAILED"]);
  assert.equal(bundle.outcome, "failed");
  assert.equal(bundle.postflight.match, 1);
  assert.equal(bundle.postflight.diff, 1);
  assert.equal(bundle.postflight.unverified, 1);
  assert.equal(bundle.postflight.failed, 1);
  assert.equal(bundle.captures.length, 2);
});

test("harvest.py verify reads a forge bundle and refuses to call that run verified", async (t) => {
  const bin = python();
  if (!bin) return t.skip("no python3 on PATH");
  assert.ok(existsSync(HARVEST), "harvest.py is where this test expects it");
  const { text } = await bundleWithEveryOutcome();
  const dir = mkdtempSync(join(tmpdir(), "forge-harvest-"));
  const file = join(dir, `tnr_results_${Date.now()}.json`);
  writeFileSync(file, text);
  try {
    const v = harvest(bin, "verify", file);
    assert.match(v.out, /^OK\s+A ->/m, v.out);
    assert.match(v.out, /^FAIL\s+B ->.*asserted field/m, v.out);
    assert.match(v.out, /^UNVERIFIED\s+C ->.*live=NONE/m, v.out);
    assert.match(v.out, /^ERROR\s+D ->.*push failed/m, v.out);
    assert.match(v.out, /VERIFY FAILED/, v.out);
    assert.equal(v.code, 1, "a run with a drift, an unread and a refusal must not exit 0");

    // the capture calls survive normalisation and are reported with their inputs
    const idx = harvest(bin, "index", file);
    assert.equal(idx.code, 0, idx.out);
    assert.match(idx.out, /jutsu\.getAllNames/, idx.out);

    // diff is honest about what a forge bundle does not carry rather than inventing it
    const df = harvest(bin, "diff", file);
    assert.equal(df.code, 0, df.out);
    assert.match(df.out, /no read-back|no pushed payload/, df.out);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test("harvest.py verify agrees with forge on capture-only outcomes", async (t) => {
  const bin = python();
  if (!bin) return t.skip("no python3 on PATH");

  async function make(fail) {
    const game = new FakeGame();
    if (fail) {
      const handle = game.handle.bind(game);
      game.handle = (path, input) => path === "jutsu.getAllNames"
        ? { ok: false, error: { code: "NOT_FOUND", httpStatus: 404, message: "capture failed", path } }
        : handle(path, input);
    }
    const storage = new MemoryStorage();
    const d = composeForTest({ game, storage });
    d.runner.plan({ items: [], capture: { after: [{ proc: "jutsu.getAllNames", input: {} }] } },
      { jobId: fail ? "capture-bad" : "capture-good", manifestPath: "push/00_forge_readonly_smoke.json" });
    const summary = await d.runner.run(fail ? "capture-bad" : "capture-good");
    return { summary, ...(await exportOf(d, fail ? "capture-bad" : "capture-good")) };
  }

  const dir = mkdtempSync(join(tmpdir(), "forge-harvest-capture-"));
  try {
    const good = await make(false);
    assert.equal(good.summary.outcome, "success");
    const goodFile = join(dir, "good.json");
    writeFileSync(goodFile, good.text);
    const goodVerify = harvest(bin, "verify", goodFile);
    assert.equal(goodVerify.code, 0, goodVerify.out);
    assert.match(goodVerify.out, /capture-only bundle/);

    const bad = await make(true);
    assert.equal(bad.summary.outcome, "failed");
    assert.equal(bad.bundle.captures[0].ok, false);
    const badFile = join(dir, "bad.json");
    writeFileSync(badFile, bad.text);
    const badVerify = harvest(bin, "verify", badFile);
    assert.equal(badVerify.code, 1, badVerify.out);
    assert.match(badVerify.out, /UNVERIFIED\s+capture-only forge bundle/);
    assert.match(badVerify.out, /1 failed capture/);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test("harvest.py verify passes a clean forge bundle, and only a clean one", async (t) => {
  const bin = python();
  if (!bin) return t.skip("no python3 on PATH");
  const game = new FakeGame();
  const storage = new MemoryStorage();
  const d = composeForTest({ game, storage });
  d.runner.plan({ items: [jutsu("A"), jutsu("B")] }, { jobId: "clean", manifestPath: "push/98_clean.json" });
  const s = await d.runner.run("clean");
  assert.equal(s.state, "DONE"); assert.equal(s.outcome, "success");
  const app = new App({ version: "forge 0.3.0", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
  let text = null; app.showExport = (t2) => { text = t2; };
  await app.exportJob("clean");
  const dir = mkdtempSync(join(tmpdir(), "forge-harvest-"));
  const file = join(dir, "tnr_results_clean.json");
  writeFileSync(file, text);
  try {
    const v = harvest(bin, "verify", file);
    assert.equal(v.code, 0, v.out);
    assert.match(v.out, /2 ok, 0 fail, 0 unverified/, v.out);
    assert.match(v.out, /->\s+verified/, v.out);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

/**
 * An ambiguous create the operator resolved by SKIPPING it: two placeholder rows appeared while one
 * create was in flight, so reconciliation refuses to guess and the item is ORPHANED. Skipping it is
 * a decision to leave whatever the server holds alone - deliberately unverified, and the row may be
 * live. Produced through the real reconcile/skip path, not by hand-editing the journal.
 */
async function skippedOrphanBundle() {
  const game = new FakeGame();
  const storage = new MemoryStorage();
  const d = composeForTest({ game, storage });
  const manifest = { items: [
    { entity: "asset", slot: "create", name: "Orphan", srcId: "o", data: { name: "Orphan", hidden: true, type: "STATIC", url: "u" } },
    jutsu("After"),
  ] };
  d.runner.plan(manifest, { jobId: "sk", manifestPath: "push/97_skip.json" });
  const key = await d.reconciler.beforeCreate(d.journal.get("sk"), d.journal.get("sk").items[0], "asset");
  d.journal.annotate("sk", 0, { snapshotKey: key });
  await d.journal.withSent("sk", 0, { phase: "create" }, async () => { game.handle("gameAsset.create"); game.handle("gameAsset.create"); });
  const d2 = composeForTest({ game, storage: storage.crash(), idb: d.idb });
  d2.runner.attach("sk", manifest);
  const paused = await d2.runner.resume("sk");
  assert.equal(paused.items[0].state, "ORPHANED");
  d2.runner.skip("sk", 0);                       // the real decision path
  const summary = await d2.runner.run("sk");
  return { summary, ...(await exportOf(d2, "sk")), game };
}

/** A job that stopped with a write still in flight: the create left, the response never came. */
async function pendingWriteBundle() {
  const game = new FakeGame({ crashAt: 2 });     // 1 = the pre-create snapshot, 2 = jutsu.create
  const storage = new MemoryStorage();
  const d = composeForTest({ game, storage });
  d.runner.plan({ items: [jutsu("Pending")] }, { jobId: "pw", manifestPath: "push/96_pending.json" });
  const summary = await d.runner.run("pw");
  assert.equal(summary.state, "PAUSED");
  assert.equal(summary.items[0].state, "SENT", "the write is in flight, not resolved");
  return { summary, ...(await exportOf(d, "pw")), game };
}

/** The bundle the app would commit for a job, through the real export path. */
async function exportOf(d, jobId) {
  const app = new App({ version: "forge 0.3.0", storage: d.storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
  let text = null;
  app.showExport = (t) => { text = t; };
  await app.exportJob(jobId);
  return { text, bundle: JSON.parse(text) };
}

test("a skipped orphan cannot pass repository verification (review of c388ea6, finding 1)", async (t) => {
  const bin = python();
  if (!bin) return t.skip("no python3 on PATH");
  const { summary, bundle, text, game } = await skippedOrphanBundle();
  // forge's own semantics were already right, and stay right
  assert.equal(summary.state, "DONE", "execution has nothing left to do");
  assert.equal(summary.outcome, "unverified", "but a skipped orphan is not a verified success");
  assert.equal(bundle.entries[0].state, "skipped");
  assert.equal(bundle.entries[0].forgeState, "SKIPPED");
  assert.equal(bundle.outcome, "unverified");
  assert.ok(game.count("asset") >= 1, "the server row the skip walked away from is still there");
  // ...and the repository gate must agree. Against c388ea6 this printed SKIP and exited 0.
  const dir = mkdtempSync(join(tmpdir(), "forge-harvest-"));
  const file = join(dir, "tnr_results_skipped.json");
  writeFileSync(file, text);
  try {
    const v = harvest(bin, "verify", file);
    assert.match(v.out, /^UNVERIFIED\s+Orphan/m, v.out);
    assert.match(v.out, /VERIFY FAILED/, v.out);
    assert.equal(v.code, 1, "a bundle holding a skipped orphan must never verify green");
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test("a bundle exported with a write still pending cannot pass verification either", async (t) => {
  const bin = python();
  if (!bin) return t.skip("no python3 on PATH");
  const { bundle, text } = await pendingWriteBundle();
  assert.equal(bundle.entries[0].state, "pending");
  assert.equal(bundle.entries[0].forgeState, "SENT");
  assert.equal(bundle.outcome, "open", "the job is paused: the question is not answered yet");
  const dir = mkdtempSync(join(tmpdir(), "forge-harvest-"));
  const file = join(dir, "tnr_results_pending.json");
  writeFileSync(file, text);
  try {
    const v = harvest(bin, "verify", file);
    assert.match(v.out, /^UNVERIFIED\s+Pending/m, v.out);
    assert.notEqual(v.code, 0, "an in-flight write is the definition of unverified");
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test("a legacy builder bundle keeps its own semantics", async (t) => {
  const bin = python();
  if (!bin) return t.skip("no python3 on PATH");
  // no cfg:"forge", no forgeState: the pre-forge shape, where a non-ok row is the builder's own
  // "not pushed" and the gate has always read it as a skip rather than a failure
  const legacy = {
    builder: "v4.29", at: new Date(0).toISOString(), cfg: "45c",
    postflight: { match: 1, diff: 0, unverified: 0 },
    entries: [
      { name: "A", entity: "jutsu", slot: "create", state: "ok", verdict: "match", asserted: { ok: 3, fail: [] }, id: "id-a" },
      { name: "B", entity: "jutsu", slot: "edit", state: "pending", detail: "not attempted", id: "id-b" },
    ],
    captures: [], idmap: {},
  };
  const dir = mkdtempSync(join(tmpdir(), "forge-harvest-"));
  const file = join(dir, "tnr_results_legacy.json");
  writeFileSync(file, JSON.stringify(legacy, null, 1));
  try {
    const v = harvest(bin, "verify", file);
    assert.equal(v.code, 0, v.out);
    assert.match(v.out, /1 ok, 0 fail, 0 unverified, 1 skipped/, v.out);
    // but the same shape marked as forge fails closed, even with no outcome recorded: a forge
    // bundle that cannot state its own verdict is not evidence of success
    const asForge = { ...legacy, cfg: "forge", entries: legacy.entries.map((e) => ({ ...e, forgeState: e.state === "ok" ? "VERIFIED" : "PLANNED" })) };
    const f2 = join(dir, "tnr_results_forge_no_outcome.json");
    writeFileSync(f2, JSON.stringify(asForge, null, 1));
    const v2 = harvest(bin, "verify", f2);
    assert.equal(v2.code, 1, v2.out);
    assert.match(v2.out, /job outcome=None/, v2.out);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test("harvest.py reads a full capture body, and still refuses a bundle whose body is missing", async (t) => {
  const bin = python();
  if (!bin) return t.skip("no python3 on PATH");
  const ASSET = { id: "XsLLy8awDAtaE6hXVIi_0", name: "Chase Alley Plate", type: "STATIC", image: "https://utfs.io/f/chase-alley.webp", folder: "scene", hidden: false };

  async function run(dropBody) {
    const game = new FakeGame();
    const storage = new MemoryStorage();
    game.seed("asset", { ...ASSET });
    const d = composeForTest({ game, storage });
    d.runner.plan({ items: [], capture: { after: [{ proc: "gameAsset.get", input: { id: ASSET.id }, persist: "full" }] } },
      { jobId: dropBody ? "probe-gone" : "probe", manifestPath: "push/02_one_perfect_crop_asset_probe.json", manifestNumber: 2 });
    await d.runner.run(dropBody ? "probe-gone" : "probe");
    if (dropBody) await d.cache.delete("gameAsset.get", ASSET.id);
    const app = new App({ version: "forge 0.3.0", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
    let text = null;
    app.showExport = (t2) => { text = t2; };
    await app.exportJob(dropBody ? "probe-gone" : "probe");
    return text;
  }

  const dir = mkdtempSync(join(tmpdir(), "forge-harvest-full-"));
  try {
    const good = join(dir, "tnr_results_full_ok.json");
    writeFileSync(good, await run(false));
    // the repository's own ingestion path sees the record, not just a row count
    const idx = harvest(bin, "index", good);
    assert.equal(idx.code, 0, idx.out);
    assert.match(idx.out, /gameAsset\.get/, idx.out);
    // `get` extracts the RECORD, which is the whole point of full persistence: before this
    // contract a capture-only bundle could only tell harvest.py how many rows came back
    const out = join(dir, "asset.json");
    const got = harvest(bin, "get", good, ["--proc", "gameAsset.get", "--out", out]);
    assert.equal(got.code, 0, got.out);
    assert.match(got.out, /name='Chase Alley Plate'/, got.out);
    assert.deepEqual(JSON.parse(readFileSync(out, "utf8")), ASSET, "the exact record, straight out of the bundle");
    assert.equal(JSON.parse(readFileSync(good, "utf8")).captures[0].data.image, ASSET.image);
    const v = harvest(bin, "verify", good);
    assert.equal(v.code, 0, v.out);
    assert.match(v.out, /capture-only bundle/, v.out);

    const bad = join(dir, "tnr_results_full_missing.json");
    writeFileSync(bad, await run(true));
    const parsed = JSON.parse(readFileSync(bad, "utf8"));
    assert.equal(parsed.captures[0].persistOk, false);
    assert.ok(!("data" in parsed.captures[0]));
    const v2 = harvest(bin, "verify", bad);
    assert.equal(v2.code, 1, "a bundle that owes a body it does not carry must not verify: " + v2.out);
    assert.match(v2.out, /UNVERIFIED\s+capture-only forge bundle/, v2.out);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
