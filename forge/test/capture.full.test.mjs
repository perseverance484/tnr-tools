// Full capture persistence (task brief state/prompt_forge_full_capture.md).
//
// The claim this file exists to hold: when a manifest asks for `persist: "full"`, the exported
// results bundle carries the EXACT decoded body of the read Forge already performed, with no
// second read, no body in the localStorage journal, no silent truncation, and no way for a
// missing body to be reported as a success.
//
// "the read Forge already performed" is the whole difficulty, and the FFC-1 section at the bottom
// is where it is actually held. The body comes out of an IMMUTABLE per-occurrence snapshot, not
// out of the path+id read cache, which the next read of that record replaces and a write to that
// entity deletes.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { App } from "../src/ui/app.mjs";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";
import { captureLabel } from "../src/ui/screens.mjs";
import { jobOutcome } from "../src/storage/journal.mjs";
import { MAX_FULL_CAPTURE_BYTES, FULL_PERSIST_PATHS, snapshotKey } from "../src/storage/captures.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";
import { IDBFactory } from "fake-indexeddb";

const PROBE = new URL("../../push/02_one_perfect_crop_asset_probe.json", import.meta.url);

// A plain asset row: no Date fields, so "the exported body is EXACTLY the decoded response" can be
// asserted as a deep equality against the row the game holds rather than against a serialization.
const ASSET = Object.freeze({
  id: "XsLLy8awDAtaE6hXVIi_0",
  name: "Chase Alley Plate",
  type: "STATIC",
  image: "https://utfs.io/f/chase-alley.webp",
  folder: "scene",
  hidden: false,
  frames: 1,
  speed: 1,
});
const ASSET2 = Object.freeze({ ...ASSET, id: "xsikTqetvzo5OXKdTicK6", name: "Rooftop Plate", hidden: true });

function harness({ game = new FakeGame(), storage = new MemoryStorage() } = {}) {
  const d = composeForTest({ game, storage });
  const app = new App({ version: "forge test", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
  let exported = null;
  app.showExport = (t) => { exported = t; };
  return { ...d, app, storage, game, bundle: async (jobId) => { exported = null; await app.exportJob(jobId); return JSON.parse(exported); } };
}

const fullCapture = (id, proc = "gameAsset.get") => ({ proc, input: { id }, persist: "full" });

// ---------------------------------------------------------------- 1, 2: backward compatibility
test("a legacy capture with no persist key parses, runs and exports exactly as before", async () => {
  const h = harness();
  const legacy = { items: [], capture: { after: [{ proc: "jutsu.getAllNames", input: {} }] } };
  const m = parseManifest(legacy);
  assert.equal(m.capture.after[0].persist, "summary", "omitted persist means the historical summary mode");
  assert.equal(m.fullCaptures, 0);

  h.runner.plan(legacy, { jobId: "legacy", manifestPath: "push/00_forge_readonly_smoke.json" });
  const s = await h.runner.run("legacy");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success");
  const bundle = await h.bundle("legacy");
  assert.deepEqual(Object.keys(bundle.captures[0]).sort(), ["error", "input", "ok", "phase", "proc", "rows"]);
  assert.ok(!("data" in bundle.captures[0]), "a summary capture never grows a body");
  assert.ok(!("persist" in bundle.captures[0]), "a summary capture is not annotated with a mode it did not ask for");
});

test('an explicit persist "summary" is exactly equivalent to omitting the key', async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  const manifest = { items: [], capture: { after: [{ proc: "gameAsset.get", input: { id: ASSET.id }, persist: "summary" }] } };
  h.runner.plan(manifest, { jobId: "sum" });
  const s = await h.runner.run("sum");
  assert.equal(s.outcome, "success");
  const bundle = await h.bundle("sum");
  assert.deepEqual(Object.keys(bundle.captures[0]).sort(), ["error", "input", "ok", "phase", "proc", "rows"]);
  assert.ok(!("data" in bundle.captures[0]));
  assert.ok(!("persistOk" in bundle.captures[0]));
});

// ---------------------------------------------------------------- 3, 4, 5: the full path itself
test("persist full exports the exact decoded body, from ONE read, out of IndexedDB", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  h.runner.plan({ items: [], capture: { after: [fullCapture(ASSET.id)] } }, { jobId: "full" });
  const s = await h.runner.run("full");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success");
  assert.deepEqual(h.game.calls.map((c) => c.path), ["gameAsset.get"], "one read, and it is the point read");

  const bundle = await h.bundle("full");
  const [capture] = bundle.captures;
  assert.equal(capture.proc, "gameAsset.get");
  assert.equal(capture.persist, "full");
  assert.equal(capture.persistOk, true);
  assert.equal(capture.persistError, null);
  assert.equal(capture.ok, true);
  assert.equal(capture.rows, 1);
  assert.deepEqual(capture.input, { id: ASSET.id });
  assert.deepEqual(capture.data, ASSET, "the exact decoded body, not a projection of it");
  // the compact fields a compatibility review actually reads off the record
  assert.equal(capture.data.image, ASSET.image);
  assert.equal(capture.data.hidden, false);

  assert.equal(h.game.calls.length, 1, "export must materialize from the cache, never re-read");
});

test("the full body is in IndexedDB and never in the localStorage journal", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  h.runner.plan({ items: [], capture: { after: [fullCapture(ASSET.id)] } }, { jobId: "where" });
  await h.runner.run("where");
  await h.bundle("where"); // export also writes the persistence verdict back to the journal

  const key = snapshotKey("where", "after", 0);
  const snap = await h.cache.getSnapshot(key);
  assert.deepEqual(snap.data, ASSET, "the immutable snapshot store holds the body");
  assert.equal(snap.path, "gameAsset.get");
  assert.equal(snap.id, ASSET.id);

  const localStorageText = JSON.stringify(h.storage.snapshot());
  assert.ok(!localStorageText.includes(ASSET.image), "no response body may reach the synchronous write-ahead journal");
  assert.ok(!localStorageText.includes(ASSET.name));
  assert.ok(localStorageText.includes(key), "the journal keeps the compact snapshot key instead");

  const journalled = h.journal.get("where").capturesAfter[0];
  assert.ok(!("data" in journalled));
  assert.equal(journalled.persist, "full");
  assert.equal(journalled.persistOk, true);
  assert.equal(journalled.snapshotKey, key);
});

// ---------------------------------------------------------------- 12: the embedded journal
test("the bundle's embedded journal stays compact and does not duplicate the body", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  h.runner.plan({ items: [], capture: { after: [fullCapture(ASSET.id)] } }, { jobId: "j" });
  await h.runner.run("j");
  const bundle = await h.bundle("j");
  assert.deepEqual(bundle.captures[0].data, ASSET);
  const embedded = bundle.journal.capturesAfter[0];
  assert.ok(!("data" in embedded), "the journal beside the captures must not carry a second copy");
  assert.equal(embedded.persistOk, true);
  assert.equal(JSON.stringify(bundle.journal).includes(ASSET.image), false);
});

// ---------------------------------------------------------------- 6: invalid persist values
test("an unknown persist value is a manifest error, before any job is opened", () => {
  const h = harness();
  const bad = (persist) => ({ items: [], capture: { after: [{ proc: "gameAsset.get", input: { id: ASSET.id }, persist }] } });
  for (const persist of ["fields", "FULL", "true", "", 1, true, ["full"], { mode: "full" }]) {
    assert.throws(() => parseManifest(bad(persist)), ManifestError, `persist ${JSON.stringify(persist)} must be refused`);
    assert.throws(() => parseManifest(bad(persist)), /persist must be "summary" or "full"/);
  }
  assert.throws(() => h.runner.plan(bad("fields"), { jobId: "never" }), ManifestError);
  assert.equal(h.journal.get("never"), null, "no job record may exist for a manifest that did not parse");
  assert.deepEqual(h.game.calls, []);
});

// ---------------------------------------------------------------- 7: the fail-closed allowlist
test("full persistence is refused for list, mutation, unknown and un-audited procedures", () => {
  const refuse = (proc, input = { id: "x" }) => {
    assert.throws(
      () => parseManifest({ items: [], capture: { after: [{ proc, input, persist: "full" }] } }),
      /persist "full" is only allowed for the audited content-record point reads/,
      `${proc} must not be persistable`);
  };
  for (const proc of ["jutsu.getAllNames", "gameAsset.getAllNames", "profile.getAllAiNames"]) refuse(proc);   // name lists
  for (const proc of ["jutsu.getAll", "item.getAll", "quests.getAll", "gameAsset.getAll"]) refuse(proc);      // list dumps
  for (const proc of ["jutsu.update", "gameAsset.create", "quests.delete", "profile.updateAi"]) refuse(proc); // mutations
  for (const proc of ["asset.get", "user.get", "profile.getUser", "auth.session", "nonsense"]) refuse(proc);  // unknown / not audited
  // and the same paths remain perfectly legal as SUMMARY captures: this gate is about durability
  assert.ok(parseManifest({ items: [], capture: { after: [{ proc: "jutsu.getAllNames" }] } }));
});

test('a full capture with no record id is refused: "full" is a point read or nothing', () => {
  for (const input of [undefined, {}, { limit: 10 }, { id: "" }, { id: 7 }]) {
    assert.throws(
      () => parseManifest({ items: [], capture: { after: [{ proc: "gameAsset.get", input, persist: "full" }] } }),
      /needs input\.id \(or input\.userId\)/);
  }
  // profile.getAi is keyed by userId at source, so it is accepted under that spelling
  const m = parseManifest({ items: [], capture: { after: [{ proc: "profile.getAi", input: { userId: "ai1" }, persist: "full" }] } });
  assert.equal(m.capture.after[0].id, "ai1");
});

test("the allowlist is exactly the audited content-record point reads and nothing else", () => {
  assert.deepEqual([...FULL_PERSIST_PATHS].sort(), [
    "ai.getAiProfile", "bloodline.get", "gameAsset.get", "item.get", "jutsu.get", "profile.getAi", "quests.get",
  ]);
});

// ---------------------------------------------------------------- hashing the contract
test("manifest hashing covers the persistence request", () => {
  const of = (persist) => parseManifest({ items: [], capture: { after: [{ proc: "gameAsset.get", input: { id: ASSET.id }, ...(persist ? { persist } : {}) }] } }).hash;
  assert.notEqual(of("full"), of("summary"), "a job opened as summary must not resume as full");
  assert.notEqual(of("full"), of(null), "nor may an omitted persist resume a full job");
  // a manifest written before this contract existed keeps the hash it already had, so an open job
  // in a browser survives the upgrade instead of refusing to resume
  const legacy = { items: [], capture: { after: [{ proc: "jutsu.getAllNames", input: {} }] } };
  assert.equal(parseManifest(legacy).hash, "c359fd86");
});

// ---------------------------------------------------------------- 8: incremental resume
test("a full capture pass that pauses does not re-read the captures it already finished", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  h.game.seed("asset", { ...ASSET2 });
  // the second read is answered with a limit, so the job pauses with one capture done
  h.game.limitPath = "gameAsset.get";
  let seen = 0;
  const orig = h.game.handle.bind(h.game);
  h.game.handle = (path, input) => {
    if (path === "gameAsset.get" && seen++ === 0) { h.game.limitPath = null; const r = orig(path, input); h.game.limitPath = "gameAsset.get"; return r; }
    return orig(path, input);
  };
  const manifest = { items: [], capture: { after: [fullCapture(ASSET.id), fullCapture(ASSET2.id)] } };
  h.runner.plan(manifest, { jobId: "part" });
  const paused = await h.runner.run("part");
  assert.equal(paused.state, "PAUSED");
  assert.equal(paused.outcome, "open");
  const partial = h.journal.get("part").capturesAfterPartial;
  assert.equal(partial.length, 1, "one capture finished and was journaled before the pause");
  assert.equal(partial[0].persistOk, true);
  const callsAfterPause = h.game.calls.length;

  // let the second read through and resume
  h.game.limitPath = null;
  h.budget.log.clearTrip();
  h.clock.tick(120_000);
  const done = await h.runner.run("part");
  assert.equal(done.state, "DONE");
  assert.equal(done.outcome, "success");
  const bodies = h.game.calls.filter((c) => c.path === "gameAsset.get" && c.input.id === ASSET.id).length;
  assert.equal(bodies, 1, "the completed capture is never read a second time");
  assert.equal(h.game.calls.length, callsAfterPause + 1, "resume issues exactly the one outstanding read");

  const bundle = await h.bundle("part");
  assert.deepEqual(bundle.captures.map((c) => c.data.id), [ASSET.id, ASSET2.id]);
});

// ---------------------------------------------------------------- 9: missing body at export
test("a full body missing from IndexedDB at export is an explicit non-success, never a green claim", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  h.runner.plan({ items: [], capture: { after: [fullCapture(ASSET.id)] } }, { jobId: "gone" });
  const s = await h.runner.run("gone");
  assert.equal(s.outcome, "success", "at read time the body was there");

  await h.cache.deleteSnapshot(snapshotKey("gone", "after", 0)); // e.g. an evicted store
  assert.ok(await h.cache.get("gameAsset.get", ASSET.id), "the ordinary read cache still holds a body");
  const bundle = await h.bundle("gone");
  const [capture] = bundle.captures;
  assert.equal(capture.ok, true, "the read itself still succeeded and is reported honestly");
  assert.equal(capture.persistOk, false);
  assert.match(capture.persistError, /capture snapshot .* is gone/);
  assert.ok(!("data" in capture), "and the read cache is NOT a fallback: a cache body is not this read's body");
  assert.equal(bundle.outcome, "failed", "a capture-only job that owes a body it cannot produce is not a success");
  assert.equal(jobOutcome(h.journal.get("gone")), "failed", "and the journal, not just the bundle, says so");
  assert.equal(h.game.calls.length, 1, "a missing body is reported, NOT re-read from the game");
});

test("a full capture whose body exceeds the ceiling fails explicitly and is never truncated", async () => {
  const h = harness();
  const huge = { ...ASSET, blob: "x".repeat(MAX_FULL_CAPTURE_BYTES + 1) };
  h.game.seed("asset", huge);
  h.runner.plan({ items: [], capture: { after: [fullCapture(ASSET.id)] } }, { jobId: "big" });
  const s = await h.runner.run("big");
  assert.equal(s.outcome, "failed");
  const bundle = await h.bundle("big");
  const [capture] = bundle.captures;
  assert.equal(capture.ok, true);
  assert.equal(capture.persistOk, false);
  assert.match(capture.persistError, /over the \d+-byte full-capture ceiling/, "export keeps the reason the capture pass recorded");
  assert.match(capture.persistError, /NOT truncated/);
  assert.ok(!("data" in capture), "an oversized body is withheld whole, never shortened and relabelled");
  assert.equal(await h.cache.getSnapshot(snapshotKey("big", "after", 0)), null, "and nothing oversized was stored at all");
});

// ---------------------------------------------------------------- 10: a failed read
test("a failed read fabricates no data and persists nothing", async () => {
  const h = harness(); // nothing seeded: gameAsset.get answers NOT_FOUND
  h.runner.plan({ items: [], capture: { after: [fullCapture("does-not-exist")] } }, { jobId: "miss" });
  const s = await h.runner.run("miss");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "failed");
  const bundle = await h.bundle("miss");
  const [capture] = bundle.captures;
  assert.equal(capture.ok, false);
  assert.equal(capture.error, "NOT_FOUND");
  assert.equal(capture.rows, 0);
  assert.equal(capture.persistOk, false);
  assert.match(capture.persistError, /no body to persist/);
  assert.ok(!("data" in capture));
});

// ---------------------------------------------------------------- 11: outcome and UI wording
test("a job that also writes degrades to unverified when a requested body is missing", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  const manifest = {
    capture: { before: [fullCapture(ASSET.id)] },
    items: [{ entity: "jutsu", slot: "create", name: "Ember Step", srcId: "ember", data: { name: "Ember Step", description: "d", hidden: true } }],
  };
  h.runner.plan(manifest, { jobId: "mixed" });
  const s = await h.runner.run("mixed");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success", "the write verified and the body was cached");

  await h.cache.deleteSnapshot(snapshotKey("mixed", "before", 0));
  const bundle = await h.bundle("mixed");
  assert.equal(bundle.outcome, "unverified", "no write is in doubt, but the promised evidence is not there");
  assert.equal(bundle.postflight.match, 1, "the write's own verdict is untouched");
  assert.equal(bundle.captures[0].persistOk, false);
});

test("the selected-manifest label distinguishes full captures from summary captures", () => {
  const cap = (persist) => ({ proc: "gameAsset.get", persist });
  assert.equal(captureLabel([]), "");
  assert.equal(captureLabel([cap("summary")]), "1 capture");
  assert.equal(captureLabel([cap("summary"), cap("summary")]), "2 captures");
  assert.equal(captureLabel([cap("full")]), "1 full capture");
  assert.equal(captureLabel(new Array(5).fill(cap("full"))), "5 full captures");
  assert.equal(captureLabel([cap("full"), cap("summary"), cap("full")]), "3 captures (2 full)");
});

// ---------------------------------------------------------------- 13: the first real consumer
test("push/02_one_perfect_crop_asset_probe.json parses under the contract and stays read-only", () => {
  const text = readFileSync(PROBE, "utf8");
  const raw = JSON.parse(text);
  const m = parseManifest(text);
  assert.equal(m.items.length, 0, "the probe writes nothing");
  assert.deepEqual(raw.items, [], "and says so in the file, not just after parsing");
  assert.equal(m.capture.before.length, 0);
  assert.equal(m.capture.after.length, 5);
  assert.equal(m.fullCaptures, 5);
  for (const c of m.capture.after) {
    assert.equal(c.proc, "gameAsset.get", "the canonical audited asset point read, not the asset.get spelling");
    assert.equal(c.persist, "full");
    assert.match(c.id, /^[\w-]{21}$/);
  }
  assert.equal(new Set(m.capture.after.map((c) => c.id)).size, 5, "five distinct reuse candidates");
  assert.match(m.note, /[Rr]ead-only/);
  assert.match(m.note, /[Zz]ero game mutations/);
  assert.ok(!/"asset\.get"/.test(text), "the un-audited alias is gone from the file");
});

// ================================================================ FFC-1
// A full capture must durably identify the body of THAT read. The path+id read cache cannot do
// that: the next read of the record replaces the slot, and a write to the entity deletes it. Each
// test below fails against a path+id-keyed implementation.

/** An asset edit the runner will actually send: renames the record, so before/after differ. */
const renameAsset = (id, name) => ({ entity: "asset", slot: "edit", name, targetId: id, data: { name } });

test("FFC-1: before/write/after on ONE record exports the before body and the after body", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  h.runner.plan({
    capture: { before: [fullCapture(ASSET.id)], after: [fullCapture(ASSET.id)] },
    items: [renameAsset(ASSET.id, "Chase Alley Plate v2")],
  }, { jobId: "ba" });
  const s = await h.runner.run("ba");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success");

  // the update deleted the read cache slot and the read-back refilled it with the NEW body, so
  // gameAsset.get:<id> now holds the after record. That is correct for a cache and fatal as an
  // identity for the before capture.
  assert.equal((await h.cache.get("gameAsset.get", ASSET.id)).data.name, "Chase Alley Plate v2");

  const callsBeforeExport = h.game.calls.length;
  const bundle = await h.bundle("ba");
  assert.equal(h.game.calls.length, callsBeforeExport, "export performs no read");

  const [before, after] = bundle.captures;
  assert.equal(before.phase, "before");
  assert.equal(after.phase, "after");
  assert.equal(before.persistOk, true);
  assert.equal(after.persistOk, true);
  assert.deepEqual(before.data, ASSET, "the BEFORE entry carries the body of the before read");
  assert.equal(after.data.name, "Chase Alley Plate v2", "and the after entry carries the after body");
  assert.notEqual(before.snapshotKey, after.snapshotKey, "two occurrences, two immutable snapshots");
  assert.equal(bundle.entries[0].verdict, "match", "the write itself still verified");

  // exactly one read per capture: the before pass, the after pass, and the item's own fill/verify
  // reads, but no capture read repeated
  const captureReads = h.game.calls.filter((c) => c.path === "gameAsset.get").length;
  assert.equal(captureReads, 4, "before capture, fill, read-back, after capture - and nothing else");
});

test("FFC-1: two full reads of the same path+id keep their own bodies, not the newest", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  let n = 0;
  const orig = h.game.handle.bind(h.game);
  h.game.handle = (path, input) => {
    // the record changes underneath us between the two capture reads, with no write from this job
    if (path === "gameAsset.get" && n++ === 1) h.game.tables.asset.get(ASSET.id).name = "Renamed By Someone Else";
    return orig(path, input);
  };
  h.runner.plan({ items: [], capture: { after: [fullCapture(ASSET.id), fullCapture(ASSET.id)] } }, { jobId: "twice" });
  const s = await h.runner.run("twice");
  assert.equal(s.outcome, "success");
  assert.equal(h.game.calls.filter((c) => c.path === "gameAsset.get").length, 2, "two reads, because both were requested fresh");

  const bundle = await h.bundle("twice");
  assert.equal(bundle.captures.length, 2);
  assert.equal(bundle.captures[0].data.name, "Chase Alley Plate", "the first capture kept the body IT read");
  assert.equal(bundle.captures[1].data.name, "Renamed By Someone Else");
  assert.deepEqual(bundle.captures.map((c) => c.snapshotKey), [snapshotKey("twice", "after", 0), snapshotKey("twice", "after", 1)]);
});

test("FFC-1: a before-only full capture survives the job's own write to that entity", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  h.runner.plan({
    capture: { before: [fullCapture(ASSET.id)] },
    items: [renameAsset(ASSET.id, "Renamed Plate")],
  }, { jobId: "beforeonly" });
  const s = await h.runner.run("beforeonly");
  assert.equal(s.outcome, "success");
  // invalidateRecord ran on the asset entity; the snapshot is in a different store and untouched
  const snap = await h.cache.getSnapshot(snapshotKey("beforeonly", "before", 0));
  assert.deepEqual(snap.data, ASSET);

  const bundle = await h.bundle("beforeonly");
  assert.equal(bundle.captures[0].persistOk, true);
  assert.deepEqual(bundle.captures[0].data, ASSET, "the pre-write state is still exportable after the write");
  assert.equal(h.game.rows("asset")[0].name, "Renamed Plate", "and the live record really did change");
});

test("FFC-1: snapshot bodies reach neither the localStorage journal nor the embedded journal", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  // the write changes `image` rather than `name`, so the after body's distinguishing value is one
  // that has no legitimate reason to be in the journal at all (an item's NAME does, and is)
  const NEW_IMAGE = "https://utfs.io/f/chase-alley-v2.webp";
  h.runner.plan({
    capture: { before: [fullCapture(ASSET.id)], after: [fullCapture(ASSET.id)] },
    items: [{ entity: "asset", slot: "edit", name: ASSET.name, targetId: ASSET.id, data: { image: NEW_IMAGE } }],
  }, { jobId: "compact" });
  await h.runner.run("compact");
  const bundle = await h.bundle("compact");
  assert.equal(bundle.captures[1].data.image, NEW_IMAGE, "the after body really did change");

  const localStorageText = JSON.stringify(h.storage.snapshot());
  for (const needle of [ASSET.image, ASSET.folder, NEW_IMAGE]) {
    assert.ok(!localStorageText.includes(needle), `localStorage must not carry ${needle}`);
  }
  const embedded = JSON.stringify(bundle.journal);
  assert.ok(!embedded.includes(ASSET.image), "the embedded journal must not duplicate a body");
  for (const entry of [...bundle.journal.capturesBefore, ...bundle.journal.capturesAfter]) {
    assert.ok(!("data" in entry));
    assert.match(entry.snapshotKey, /^compact::(before|after)::0$/);
  }
  assert.deepEqual(bundle.captures[0].data, ASSET, "while the bundle beside it does carry the bodies");
});

test("FFC-1: snapshots survive a restart and export from persisted state alone", async () => {
  const game = new FakeGame();
  const storage = new MemoryStorage();
  const idb = new IDBFactory();
  game.seed("asset", { ...ASSET });
  {
    // "the tab that ran the job", which then goes away entirely
    const first = composeForTest({ game, storage, idb });
    first.runner.plan({ items: [], capture: { after: [fullCapture(ASSET.id)] } }, { jobId: "restart", manifestPath: "push/02_one_perfect_crop_asset_probe.json" });
    assert.equal((await first.runner.run("restart")).state, "DONE");
    first.cache.close();
  }
  const callsAtRestart = game.calls.length;

  // a fresh composition over the SAME localStorage and the SAME IndexedDB: no runner state, no
  // parsed manifest, nothing in memory - only what was persisted
  const second = composeForTest({ game, storage: storage.crash(), idb });
  const app = new App({ version: "forge test", storage: second.storage, now: second.clock, ...second, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
  let exported = null;
  app.showExport = (t) => { exported = t; };
  await app.exportJob("restart");
  const bundle = JSON.parse(exported);
  assert.equal(bundle.captures[0].persistOk, true);
  assert.deepEqual(bundle.captures[0].data, ASSET, "the body came back out of persisted IndexedDB");
  assert.equal(game.calls.length, callsAtRestart, "and not out of the game");
});

test("FFC-1: a job's snapshots are deletable by job, and only that job's", async () => {
  const h = harness();
  h.game.seed("asset", { ...ASSET });
  h.game.seed("asset", { ...ASSET2 });
  h.runner.plan({ items: [], capture: { after: [fullCapture(ASSET.id)] } }, { jobId: "keep" });
  await h.runner.run("keep");
  h.runner.plan({ items: [], capture: { after: [fullCapture(ASSET2.id)] } }, { jobId: "drop" });
  await h.runner.run("drop");
  assert.equal((await h.cache.listSnapshots()).length, 2);

  assert.equal(await h.cache.deleteSnapshotsForJob("drop"), 1);
  const left = await h.cache.listSnapshots();
  assert.deepEqual(left.map((r) => r.jobId), ["keep"]);
  assert.deepEqual((await h.cache.getSnapshot(snapshotKey("keep", "after", 0))).data, ASSET);
  assert.equal(await h.cache.getSnapshot(snapshotKey("drop", "after", 0)), null);
});
