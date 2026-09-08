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
import { mkdtempSync, writeFileSync, rmSync, existsSync } from "node:fs";
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
function harvest(bin, cmd, file) {
  try { return { code: 0, out: execFileSync(bin, [HARVEST, cmd, file], { encoding: "utf8" }) }; }
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

  const app = new App({ version: "forge 0.2.0", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
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

test("harvest.py verify passes a clean forge bundle, and only a clean one", async (t) => {
  const bin = python();
  if (!bin) return t.skip("no python3 on PATH");
  const game = new FakeGame();
  const storage = new MemoryStorage();
  const d = composeForTest({ game, storage });
  d.runner.plan({ items: [jutsu("A"), jutsu("B")] }, { jobId: "clean", manifestPath: "push/98_clean.json" });
  const s = await d.runner.run("clean");
  assert.equal(s.state, "DONE"); assert.equal(s.outcome, "success");
  const app = new App({ version: "forge 0.2.0", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
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
