// Input-aware caching and bounded paged reads (state/prompt_forge_next_phase1.md §7).
//
// The claim this file exists to hold: the input is the identity. Two reads that sent different
// bytes never share a cache slot, the provenance a job records is the bytes that were actually
// sent, and a walk that did not reach the end of the data cannot be reported as though it had.

import { test } from "node:test";
import assert from "node:assert/strict";
import { App } from "../src/ui/app.mjs";
import { canonicalInput, canonicalKey } from "../src/research/registry.mjs";
import { queryCaptureKey, snapshotKey } from "../src/storage/captures.mjs";
import { jobOutcome } from "../src/storage/journal.mjs";
import { RateLimited } from "../src/budget/bucket.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

function harness({ game = new FakeGame(), storage = new MemoryStorage() } = {}) {
  const d = composeForTest({ game, storage });
  const app = new App({ version: "forge test", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
  let exported = null;
  app.showExport = (t) => { exported = t; };
  return { ...d, app, storage, game, bundle: async (jobId) => { exported = null; await app.exportJob(jobId); return JSON.parse(exported); } };
}

/** `n` action rows for one battle, already in the server's total order. */
function seedLog(game, battleId, n) {
  game.seedBattle(
    { battleId, battleType: "COMBAT", createdAt: "2026-09-10T00:00:00.000Z", attackedId: "a", defenderId: "d", attacker: {}, defender: {} },
    Array.from({ length: n }, (_, i) => ({ id: `${battleId}-${i}`, battleId, userId: i % 2 ? "me" : "them", battleRound: n - i, battleVersion: 1, seq: i })));
}

const sentInputs = (game, path) => game.calls.filter((c) => c.path === path).map((c) => c.input);

// ---------------------------------------------------------------- 1: identity is the input
test("different filters and different pages never alias in the cache", async () => {
  const h = harness();
  seedLog(h.game, "b1", 3);
  seedLog(h.game, "b2", 3);
  const reads = [
    { battleId: "b1" },
    { battleId: "b2" },
    { battleId: "b1", limit: 2 },
    { battleId: "b1", limit: 2, offset: 2 },
    { battleId: "b1", userFilter: "user" },
    { battleId: "b1", showBasicActions: false },
  ];
  for (const input of reads) await h.reader.query("combat.getBattleEntries", input);
  // every distinct request produced its own request AND its own cache row
  assert.equal(h.reader.stats.requests, reads.length, "no read was answered by another read's slot");
  const rows = (await h.cache.list()).filter((r) => r.path === "combat.getBattleEntries");
  assert.equal(rows.length, reads.length);
  assert.equal(new Set(rows.map((r) => r.key)).size, reads.length, "every key is distinct");
  for (const input of reads) {
    const key = queryCaptureKey("combat.getBattleEntries", canonicalKey(canonicalInput("combat.getBattleEntries", input)));
    assert.ok(rows.some((r) => r.key === key), `no cache row for ${JSON.stringify(input)}`);
  }
});

test("page 2 cannot be served by page 1's cache identity", async () => {
  const h = harness();
  seedLog(h.game, "b1", 6);
  const p1 = await h.reader.query("combat.getBattleEntries", { battleId: "b1", limit: 3 });
  assert.equal(p1.data.length, 3);
  const before = h.game.calls.length;
  const p2 = await h.reader.query("combat.getBattleEntries", { battleId: "b1", limit: 3, offset: 3 });
  assert.ok(h.game.calls.length > before, "page 2 went to the server; it was not answered from page 1");
  assert.notDeepEqual(p2.data, p1.data);
  assert.deepEqual(p2.data.map((r) => r.seq), [3, 4, 5]);
});

test("an equivalent canonical input reuses the intended cached result and nothing else", async () => {
  const h = harness();
  seedLog(h.game, "b1", 2);
  await h.reader.query("combat.getBattleEntries", { battleId: "b1", limit: 5, userFilter: "all" });
  const requests = h.reader.stats.requests;
  // the same request written in a different key order is the same request
  const again = await h.reader.query("combat.getBattleEntries", { userFilter: "all", limit: 5, battleId: "b1" });
  assert.equal(h.reader.stats.requests, requests, "an equivalent input must not spend a second request");
  assert.equal(h.reader.stats.hits, 1);
  assert.equal(again.pages[0].cached, true);
  // a DIFFERENT request must not be served by it, however similar
  await h.reader.query("combat.getBattleEntries", { battleId: "b1", limit: 5, userFilter: "user" });
  assert.equal(h.reader.stats.requests, requests + 1);
  // and `fresh` bypasses the slot entirely, as the capture pass always asks
  await h.reader.query("combat.getBattleEntries", { battleId: "b1", limit: 5, userFilter: "all" }, { fresh: true });
  assert.equal(h.reader.stats.requests, requests + 2);
});

test("the input journaled is byte-for-byte the input sent", async () => {
  const h = harness();
  seedLog(h.game, "b1", 2);
  // written in a deliberately awkward key order, with an optional the manifest does not set
  h.runner.plan({ items: [], capture: { after: [
    { proc: "combat.getBattleEntries", input: { showBasicActions: true, battleId: "b1", userFilter: "all", limit: 500 }, persist: "local-only" },
  ] } }, { jobId: "prov" });
  await h.runner.run("prov");
  const [sent] = sentInputs(h.game, "combat.getBattleEntries");
  const bundle = await h.bundle("prov");
  const [capture] = bundle.captures;
  assert.deepEqual(capture.input, sent, "the journal records the exact object that went on the wire");
  assert.deepEqual(capture.pages[0].input, sent, "and so does the per-page record");
  assert.equal(capture.pages[0].key, canonicalKey(sent), "and the cache identity is that same value");
  // the snapshot the body lives under carries it too, so evidence and request cannot separate
  const snap = await h.cache.getSnapshot(snapshotKey("prov", "after", 0));
  assert.deepEqual(snap.input, sent);
  assert.ok(!("offset" in sent) && !("refreshKey" in sent), "Forge sent no key the manifest did not ask for");
});

// ---------------------------------------------------------------- 2: bounded walks, honest verdicts
test("a bounded walk stops at its declared page count and says the answer is incomplete", async () => {
  const h = harness();
  seedLog(h.game, "b1", 100);
  h.runner.plan({ items: [], capture: { after: [
    { proc: "combat.getBattleEntries", input: { battleId: "b1", limit: 10 }, persist: "local-only", pages: 3 },
  ] } }, { jobId: "bounded" });
  const s = await h.runner.run("bounded");
  assert.equal(sentInputs(h.game, "combat.getBattleEntries").length, 3, "exactly the pages that were asked for; no crawl");
  assert.equal(jobOutcome(h.journal.get("bounded")), "failed", "a partial answer is never a green capture");
  const bundle = await h.bundle("bounded");
  const [capture] = bundle.captures;
  assert.equal(capture.complete, false);
  assert.equal(capture.rows, 30);
  assert.deepEqual(capture.pages.map((p) => p.input.offset), [undefined, 10, 20]);
  assert.equal(capture.persistOk, false);
  assert.match(capture.persistError, /paged walk did not complete/);
  assert.match(capture.persistError, /more rows exist/);
  assert.ok(!("data" in capture), "a partial walk is not persisted as a whole body");
});

test("a walk that reaches a short page IS complete, and the body is retained", async () => {
  const h = harness();
  seedLog(h.game, "b1", 25);
  h.runner.plan({ items: [], capture: { after: [
    { proc: "combat.getBattleEntries", input: { battleId: "b1", limit: 10 }, persist: "local-only", pages: 5 },
  ] } }, { jobId: "whole" });
  await h.runner.run("whole");
  assert.equal(sentInputs(h.game, "combat.getBattleEntries").length, 3, "it stopped at the short page, not at the page bound");
  assert.equal(jobOutcome(h.journal.get("whole")), "success");
  const bundle = await h.bundle("whole");
  const [capture] = bundle.captures;
  assert.equal(capture.complete, true);
  assert.equal(capture.rows, 25);
  assert.equal(capture.persistOk, true);
  const snap = await h.cache.getSnapshot(snapshotKey("whole", "after", 0));
  assert.equal(snap.data.length, 25, "the retained body is the whole walk, in order");
  assert.deepEqual(snap.data.map((r) => r.seq).slice(0, 3), [0, 1, 2]);
});

test("a failing page ends the walk with per-page evidence and no whole-answer verdict", async () => {
  const h = harness();
  seedLog(h.game, "b1", 40);
  h.runner.plan({ items: [], capture: { after: [
    { proc: "combat.getBattleEntries", input: { battleId: "b1", limit: 10 }, persist: "local-only", pages: 4 },
  ] } }, { jobId: "half" });
  // page 3 answers NOT_FOUND: the log disappears between requests
  let n = 0;
  const real = h.game.handle.bind(h.game);
  h.game.handle = (path, input) => {
    if (path === "combat.getBattleEntries" && ++n === 3) return { ok: false, error: { code: "NOT_FOUND", httpStatus: 404, message: "gone", path, zodError: null } };
    return real(path, input);
  };
  await h.runner.run("half");
  const bundle = await h.bundle("half");
  const [capture] = bundle.captures;
  assert.equal(capture.ok, false);
  assert.equal(capture.complete, false);
  assert.equal(capture.pages.length, 3, "it stopped at the failure rather than walking past it");
  assert.deepEqual(capture.pages.map((p) => p.ok), [true, true, false]);
  assert.equal(capture.pages[2].error, "NOT_FOUND");
  assert.deepEqual(capture.pages.map((p) => p.rows), [10, 10, 0]);
  assert.equal(capture.persistOk, false);
  assert.match(capture.persistError, /read failed; there is no body to persist/);
  assert.equal(jobOutcome(h.journal.get("half")), "failed");
});

test("a rate-limited page pauses the job; it never becomes a complete result", async () => {
  const h = harness({ game: new FakeGame({ limitPath: "combat.getBattleEntries" }) });
  seedLog(h.game, "b1", 10);
  h.runner.plan({ items: [], capture: { after: [
    { proc: "combat.getBattleEntries", input: { battleId: "b1", limit: 5 }, persist: "local-only", pages: 2 },
  ] } }, { jobId: "limited" });
  const s = await h.runner.run("limited");
  assert.equal(s.state, "PAUSED");
  assert.equal(h.journal.get("limited").pause.reason, "TOO_MANY_REQUESTS");
  const job = h.journal.get("limited");
  assert.ok(!Array.isArray(job.capturesAfter) || !job.capturesAfter.length,
    "a limited capture is not journaled as a finished capture at all; the pass resumes at it");
  assert.equal(jobOutcome(job), "open");
});

test("the bound cannot be talked past: MAX_PAGES and the audited maxLimit both hold", async () => {
  const h = harness();
  seedLog(h.game, "b1", 5);
  // reader.query clamps a caller asking for more pages than the registry ceiling
  const r = await h.reader.query("combat.getBattleEntries", { battleId: "b1", limit: 1 }, { pages: 1000 });
  assert.ok(r.pages.length <= 20, `walked ${r.pages.length} pages; the ceiling is 20`);
  assert.equal(r.pages.length, 5 + 1, "and it stopped at the short page well inside it");
  // a limit past what the row's contract was audited for is refused before any request
  const before = h.game.calls.length;
  await assert.rejects(() => h.reader.query("combat.getBattleEntries", { battleId: "b1", limit: 501 }),
    /limit 501 is over the audited maximum of 500/);
  assert.equal(h.game.calls.length, before, "and nothing was sent");
  // an unpaged procedure cannot be walked at all
  await assert.rejects(() => h.reader.query("combat.getBattleHistory", {}, { pages: 2 }), /is not paged at source/);
});

test("an unapproved path is refused by the reader before a request is shaped", async () => {
  const h = harness();
  const before = h.game.calls.length;
  await assert.rejects(() => h.reader.query("combat.getGraph", { userId: "u1" }), /not in the audited research-read registry/);
  await assert.rejects(() => h.reader.query("quests.getAll", { limit: 10 }), /not in the audited research-read registry/);
  assert.equal(h.game.calls.length, before, "fail closed means nothing left the machine");
});

// ---------------------------------------------------------------- 3: a write still invalidates
test("a write to an entity drops that entity's filtered query rows too", async () => {
  const h = harness();
  seedLog(h.game, "b1", 2);
  h.game.seed("quest", { id: "q1", name: "Old Ghost" });
  await h.reader.query("quests.get", { id: "q1" });
  const keep = await h.reader.query("combat.getBattleEntries", { battleId: "b1" });
  assert.equal(keep.ok, true);
  assert.equal((await h.cache.list()).filter((r) => r.path === "combat.getBattleEntries").length, 1);
  // a query row is shaped like a list row (id null), so entity invalidation reaches it
  await h.cache.invalidateRecord("combat", null);
  assert.equal((await h.cache.list()).filter((r) => r.path === "combat.getBattleEntries").length, 0,
    "a stale filtered read must not survive a write to its entity");
});
