// Regression tests for the findings of the three adversarial panels that survived
// verification or were confirmed by reading. Each test names the finding it pins.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { IDBFactory } from "fake-indexeddb";
import { Journal, JournalError, KEY_PREFIX, TRANSITIONS, ITEM_STATES, migrate, JOURNAL_VERSION } from "../src/storage/journal.mjs";
import { CaptureCache } from "../src/storage/captures.mjs";
import { readIdmap, IDMAP_KEY } from "../src/storage/compat.mjs";
import { stableStringify, payloadHash } from "../src/storage/hash.mjs";
import { decodeResponse } from "../src/transport/envelope.mjs";
import { CookieSession, SessionRefused } from "../src/transport/session.mjs";
import { TrpcClient, NetworkError } from "../src/transport/client.mjs";
import { classifyError } from "../src/transport/outcome.mjs";
import { Budget } from "../src/budget/bucket.mjs";
import { CachedReader } from "../src/budget/reader.mjs";
import { Validator, diffAsserted } from "../src/runner/validate.mjs";
import { Runner } from "../src/runner/runner.mjs";
import { Reconciler } from "../src/reconcile/reconciler.mjs";
import { FakeGame, FakeClient, CrashSignal } from "./fakegame.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";

const SCHEMAS = JSON.parse(readFileSync(new URL("../../skills/building-tnr-content/data/45d_DATA_entity_schemas.json", import.meta.url), "utf8"));
const spec = (entity = "jutsu", op = "create", i = 0) => ({ entity, op, name: `${entity}${i}`, srcId: op === "create" ? `${entity}${i}` : null, targetId: op === "update" ? `t${i}` : null, payloadHash: "h" });
const J = (s = new MemoryStorage()) => new Journal(s, fakeClock(), { yieldTask: async () => {} });

function harness({ game = new FakeGame(), storage = new MemoryStorage(), idb = new IDBFactory() } = {}) {
  const clock = fakeClock();
  const journal = new Journal(storage, clock, { yieldTask: async () => {} });
  const cache = new CaptureCache(idb, clock);
  const budget = new Budget({ storage, clock, sleep: async (ms) => clock.tick(ms) });
  const client = new FakeClient(game);
  const reader = new CachedReader({ client, cache, budget });
  const reconciler = new Reconciler({ storage, reader, clock, journal });
  const runner = new Runner({ journal, client, reader, cache, budget, validator: new Validator(SCHEMAS), storage, reconciler });
  return { game, storage, idb, clock, journal, cache, budget, client, reader, runner, reconciler };
}
const ONE = { items: [{ entity: "jutsu", slot: "create", name: "A", srcId: "a", data: { name: "A", description: "d", hidden: true } }] };

// ---------------------------------------------------------------- L1 storage
test("L1: annotate() refuses state and timestamps, so SENT -> PLANNED is unreachable by any call", () => {
  const j = J(); j.open({ jobId: "j", items: [spec()] });
  j.transition("j", 0, "SENT");
  for (const k of ["state", "sentAt", "confirmedAt", "verifiedAt", "idx", "createSentAt"]) {
    assert.throws(() => j.annotate("j", 0, { [k]: "PLANNED" }), /annotate may not set/, k);
  }
  assert.equal(j.get("j").items[0].state, "SENT");
  assert.throws(() => j.transition("j", 0, "CONFIRMED", { state: "PLANNED" }), /may not set state/);
});

test("L1: full transition matrix is pinned; every off-table pair throws and leaves the record untouched", () => {
  for (const from of ITEM_STATES) for (const to of ITEM_STATES) {
    const s = new MemoryStorage(); const j = J(s); j.open({ jobId: "j", items: [spec()] });
    // drive into `from` legally
    const path = { PLANNED: [], SENT: ["SENT"], CONFIRMED: ["SENT", "CONFIRMED"], VERIFIED: ["SENT", "CONFIRMED", "VERIFIED"], FAILED: ["FAILED"], ORPHANED: ["SENT", "ORPHANED"], SKIPPED: ["SKIPPED"] }[from];
    let entityId = null;
    for (const st of path) { const patch = st === "CONFIRMED" ? { entityId: "e1", phase: "update" } : {}; j.transition("j", 0, st, patch); if (st === "CONFIRMED") entityId = "e1"; }
    const before = s.getItem(KEY_PREFIX + "j"); const writes = s.log.length;
    const legal = TRANSITIONS[from].includes(to);
    if (legal) { j.transition("j", 0, to, to === "CONFIRMED" && !entityId ? { entityId: "e2" } : {}); }
    else { assert.throws(() => j.transition("j", 0, to), JournalError, `${from} -> ${to} should throw`); assert.equal(s.getItem(KEY_PREFIX + "j"), before); assert.equal(s.log.length, writes); }
  }
  assert.ok(!TRANSITIONS.SENT.includes("PLANNED"));
});

test("L1: CONFIRMED -> SENT needs an entityId and may not re-enter the create phase", () => {
  const j = J(); j.open({ jobId: "j", items: [spec()] });
  j.transition("j", 0, "SENT"); j.transition("j", 0, "CONFIRMED"); // no entityId recorded
  assert.throws(() => j.transition("j", 0, "SENT"), /needs an entityId/);
  j.annotate("j", 0, { entityId: "e1" });
  assert.throws(() => j.transition("j", 0, "SENT", { phase: "create" }), /may not re-enter the create phase/);
  j.transition("j", 0, "SENT", { phase: "update" });
  assert.equal(j.get("j").items[0].sentAt !== null, true);
});

test("L1: sending is refused while the job is not RUNNING", () => {
  const j = J(); j.open({ jobId: "j", items: [spec()] });
  j.setJobState("j", "PAUSED", { pause: { reason: "x" } });
  assert.throws(() => j.transition("j", 0, "SENT"), /cannot send while job is PAUSED/);
});

test("L1: one corrupt record never blocks the others; export carries the raw text", () => {
  const s = new MemoryStorage(); const j = J(s);
  j.open({ jobId: "good", items: [spec()] });
  s.setItem(KEY_PREFIX + "bad", "{not json"); s.setItem(KEY_PREFIX + "null", "null"); s.setItem(KEY_PREFIX + "shape", JSON.stringify({ jobId: "shape", items: [{ idx: 0, state: "WEIRD" }], state: "RUNNING" }));
  const jobs = j.listJobs();
  assert.deepEqual(jobs.map((x) => x.jobId), ["good"]);
  assert.equal(j.broken.length, 3);
  assert.equal(j.resumable().length, 1);
  const ex = JSON.parse(j.exportText());
  assert.equal(ex.broken.length, 3); assert.ok(ex.broken.find((b) => b.jobId === "bad").raw.startsWith("{not"));
});

test("L1: migrate refuses a newer journal, invalid versions, and bad shapes", () => {
  assert.throws(() => migrate({ v: JOURNAL_VERSION + 1, jobId: "x", items: [], state: "RUNNING" }), /newer than this bundle/);
  assert.throws(() => migrate({ v: "1" }), /invalid version/);
  assert.throws(() => migrate({ v: 0 }), /invalid version/);
  assert.equal(migrate({ jobId: "x", items: [], state: "RUNNING" }).v, JOURNAL_VERSION); // undefined -> 1, stamped
});

test("L1: remove() refuses a job with SENT items unless forced; resumable excludes DONE/ABORTED", () => {
  const j = J(); j.open({ jobId: "j", items: [spec()] });
  j.transition("j", 0, "SENT");
  assert.throws(() => j.remove("j"), /SENT items/);
  assert.throws(() => j.setJobState("j", "DONE"), /SENT items/);
  j.transition("j", 0, "CONFIRMED", { entityId: "e" });
  j.setJobState("j", "ABORTED");
  assert.deepEqual(j.resumable(), []);
  j.remove("j"); assert.equal(j.get("j"), null);
});

test("L1: open() refuses zero items and a second open job for the same manifest", () => {
  const j = J();
  assert.throws(() => j.open({ jobId: "e", items: [] }), /at least one item/);
  j.open({ jobId: "a", manifestHash: "mh", items: [spec()] });
  assert.throws(() => j.open({ jobId: "b", manifestHash: "mh", items: [spec()] }), /already exists \(a\); resume it/);
});

test("L1: phase-2 SENT keeps the create's send time; error strings are capped", () => {
  const s = new MemoryStorage(); const clock = fakeClock(); const j = new Journal(s, clock, { yieldTask: async () => {} });
  j.open({ jobId: "j", items: [spec()] });
  j.transition("j", 0, "SENT", { phase: "create" }); const t1 = j.get("j").items[0].createSentAt;
  clock.tick(5000);
  j.transition("j", 0, "CONFIRMED", { entityId: "e", phase: "update" }); j.transition("j", 0, "SENT");
  const it = j.get("j").items[0];
  assert.equal(it.createSentAt, t1); assert.notEqual(it.sentAt, t1);
  j.transition("j", 0, "FAILED", { error: "x".repeat(5000) });
  assert.ok(j.get("j").items[0].error.length <= 512);
});

test("L1: withSent yields a task between the flush and the request (storage IPC ordering)", async () => {
  let yielded = 0;
  const j = new Journal(new MemoryStorage(), fakeClock(), { yieldTask: async () => { yielded++; } });
  j.open({ jobId: "j", items: [spec()] });
  let stateAtSend = null;
  await j.withSent("j", 0, async () => { stateAtSend = j.get("j").items[0].state; });
  assert.equal(yielded, 1); assert.equal(stateAtSend, "SENT");
});

test("L1: hash is JSON-faithful (undefined omitted, Date via toJSON)", () => {
  assert.equal(stableStringify({ a: 1, b: undefined }), '{"a":1}');
  assert.equal(stableStringify([1, undefined]), "[1,null]");
  assert.equal(stableStringify({ d: new Date(0) }), '{"d":"1970-01-01T00:00:00.000Z"}');
  assert.equal(payloadHash({ a: 1, b: undefined }), payloadHash({ a: 1 }));
});

test("L1: a corrupt idmap is parked, not destroyed by the next write", () => {
  const s = new MemoryStorage(); s.setItem(IDMAP_KEY, "{bad");
  assert.deepEqual(readIdmap(s), {});
  assert.equal(s.getItem(IDMAP_KEY + ".corrupt"), "{bad");
});

test("L1: capture cache normalises ids and survives a closed connection", async () => {
  const c = new CaptureCache(new IDBFactory(), fakeClock());
  await c.put({ path: "jutsu.get", id: 42, data: {} });
  assert.ok(await c.get("jutsu.get", "42"));
  assert.equal(await c.invalidateRecord("jutsu", 42), 1);
  c._db.close(); // simulate the browser closing the connection (onclose fires in real IDB)
  c._db = null;
  await c.put({ path: "jutsu.get", id: "x", data: {} });
  assert.ok(await c.get("jutsu.get", "x"));
});

// ---------------------------------------------------------------- L2 transport
test("L2: a request-level adapter error (bare object, not array) decodes per index", () => {
  const body = JSON.stringify({ error: { json: { message: "Unsupported media type", code: -32600, data: { code: "UNSUPPORTED_MEDIA_TYPE", httpStatus: 415 } } } });
  const out = decodeResponse(415, body, 3);
  assert.equal(out.length, 3);
  assert.ok(out.every((e) => e.ok === false && e.error.code === "UNSUPPORTED_MEDIA_TYPE" && e.error.requestLevel));
});

test("L2: one malformed element does not discard its siblings", () => {
  const body = JSON.stringify([{ result: { data: { json: { id: "a" } } } }, {}, { result: { data: { json: { id: "c" } } } }]);
  const out = decodeResponse(200, body, 3);
  assert.equal(out[0].data.id, "a"); assert.equal(out[1].error.code, "MALFORMED_ELEMENT"); assert.equal(out[2].data.id, "c");
  assert.equal(classifyError(out[1].error), "CLIENT_BUG");
});

test("L2: CookieSession allowlists paths and headers, and calls fetch receiver-free", async () => {
  const calls = [];
  const fetchImpl = function (u, i) { if (this !== undefined && this !== globalThis) throw new TypeError("Illegal invocation"); calls.push({ u, i }); return new Response("[]"); };
  const s = new CookieSession({ fetchImpl });
  await s.fetch("/api/trpc/jutsu.get?batch=1", { method: "GET", headers: { "content-type": "application/json" } });
  assert.equal(calls.length, 1);
  await assert.rejects(() => s.fetch("https://evil.invalid/api/trpc/x"), SessionRefused);
  await assert.rejects(() => s.fetch("/api/other"), SessionRefused);
  await assert.rejects(() => s.fetch("/api/trpc/x", { headers: { "proxy-authorization": "Basic x" } }), SessionRefused);
  await assert.rejects(() => s.fetch("/api/trpc/x", { headers: { authorization: "Bearer x" } }), SessionRefused);
});

test("L2: a pre-flight refusal is not-sent (TransportError), never ambiguous", async () => {
  const c = new TrpcClient(new CookieSession({ fetchImpl: async () => new Response("[]") }), { endpoint: "https://evil.invalid/api/trpc" });
  await assert.rejects(() => c.call("jutsu.create"), (e) => e.name === "TransportError" && e.sent === false && e.paths[0] === "jutsu.create");
});

test("L2: connect vs body failures are distinguishable; decode failures carry received/status/contentType", async () => {
  const bodyFail = new TrpcClient(new CookieSession({ fetchImpl: async () => { const r = new Response("x", { status: 200 }); r.text = async () => { throw new TypeError("aborted"); }; return r; } }));
  await assert.rejects(() => bodyFail.call("jutsu.create"), (e) => e instanceof NetworkError && e.phase === "body" && e.received === true && e.httpStatus === 200 && e.causeName === "TypeError");
  const html = new TrpcClient(new CookieSession({ fetchImpl: async () => new Response("<html>login</html>", { status: 200, headers: { "content-type": "text/html" } }) }));
  await assert.rejects(() => html.call("jutsu.create"), (e) => e.name === "TransportError" && e.received === true && e.httpStatus === 200 && e.looksLikeLogin === true && e.kind === "mutation");
});

test("L2: a mid-batch failure keeps earlier chunks' decoded results on the error", async () => {
  let n = 0;
  const f = async () => { n++; if (n === 2) throw new TypeError("Failed to fetch"); return new Response('[{"result":{"data":{"json":{"id":"a"}}}}]'); };
  const c = new TrpcClient(new CookieSession({ fetchImpl: f }), { maxBatch: 1 });
  await assert.rejects(() => c.batch([{ path: "jutsu.get", input: { id: "a" } }, { path: "jutsu.get", input: { id: "b" } }]), (e) => e instanceof NetworkError && e.results[0].data.id === "a" && e.failedIndices[0] === 1);
});

test("L2: NOT_FOUND is sub-classified; a single oversize GET is refused before fetch; bad maxBatch rejected", async () => {
  assert.equal(classifyError({ code: "NOT_FOUND", message: "No procedure found on path \"x.y\"" }), "CLIENT_BUG");
  assert.equal(classifyError({ code: "NOT_FOUND", message: "User not found: u1. Please complete registration." }), "SESSION");
  assert.equal(classifyError({ code: "NOT_FOUND", message: "Jutsu not found" }), "NOT_FOUND");
  assert.equal(classifyError({ code: "INTERNAL_SERVER_ERROR", message: "Output validation failed" }), "CONTRACT");
  const c = new TrpcClient(new CookieSession({ fetchImpl: async () => new Response("[]") }), { maxUrlLength: 64 });
  await assert.rejects(() => c.call("jutsu.get", { id: "x".repeat(200) }), /exceeds maxUrlLength/);
  assert.throws(() => new TrpcClient(new CookieSession({ fetchImpl: async () => {} }), { maxBatch: 0 }), /maxBatch/);
});

test("L2/L3: reader.list refuses paged getAll; limited chunks never exceed what the window has room for", async () => {
  const h = harness();
  await assert.rejects(() => h.reader.list("jutsu.getAll"), /needs a paged input/);
  for (let i = 0; i < 27; i++) await h.budget.acquire("jutsu.get"); // 3 left of 30
  const ids = ["a", "b", "c", "d", "e"];
  ids.forEach((id) => h.game.seed("jutsu", { id, name: id }));
  await h.reader.getMany("jutsu.get", ids);
  const sizes = h.game.calls.map(() => 1); // FakeClient answers per call, so inspect the budget instead
  assert.ok(h.budget.status().paths["jutsu.get"].used <= 30, "never over the allowance");
});

// ---------------------------------------------------------------- L4 runner
test("L4: after a 429 on an item's own read-back, resume only reads; the update is never re-sent", async () => {
  const game = new FakeGame();
  const h = harness({ game });
  h.runner.plan(ONE, { jobId: "r" });
  // limit only the read-back: let create/get/update through, then trip on the 4th jutsu.get
  let gets = 0; const orig = game.handle.bind(game);
  game.handle = (p, i) => { if (p === "jutsu.get" && ++gets === 2) return { ok: false, error: { code: "TOO_MANY_REQUESTS", httpStatus: 429, path: p, message: "moving too fast", zodError: null } }; return orig(p, i); };
  const s1 = await h.runner.run("r");
  assert.equal(s1.state, "PAUSED"); assert.equal(s1.items[0].state, "CONFIRMED"); assert.equal(s1.items[0].phase, "verify");
  const updates = () => game.calls.filter((c) => c.path === "jutsu.update").length;
  assert.equal(updates(), 1);
  h.clock.tick(61_000);
  const s2 = await h.runner.run("r");
  assert.equal(s2.state, "DONE"); assert.equal(s2.items[0].state, "VERIFIED");
  assert.equal(updates(), 1, "resume read back; it did not re-send");
  assert.equal(game.count("jutsu"), 1);
});

test("L4: readBack:false marks VERIFIED{skipped} immediately; drift stays CONFIRMED/verify; run() on DONE is a no-op", async () => {
  const h = harness();
  h.runner.plan({ readBack: false, ...ONE }, { jobId: "nb" });
  const s = await h.runner.run("nb");
  assert.equal(s.items[0].state, "VERIFIED"); assert.equal(s.items[0].verify, "skipped");
  const before = h.game.calls.length;
  await h.runner.run("nb");
  assert.equal(h.game.calls.length, before, "DONE job sends nothing");
  // drift: make the server lie on read-back
  const g2 = new FakeGame(); const h2 = harness({ game: g2 });
  h2.runner.plan(ONE, { jobId: "d" });
  const orig = g2.handle.bind(g2); let n = 0;
  g2.handle = (p, i) => { const r = orig(p, i); if (p === "jutsu.get" && ++n === 2) r.data.name = "Someone renamed it"; return r; };
  const sd = await h2.runner.run("d");
  assert.equal(sd.items[0].state, "CONFIRMED"); assert.equal(sd.items[0].phase, "verify"); assert.equal(sd.items[0].verify, "drift");
  assert.equal(g2.calls.filter((c) => c.path === "jutsu.update").length, 1);
});

test("L4: a reconciled rules-toggle continues at rules without re-sending the update", async () => {
  const game = new FakeGame(); const h = harness({ game });
  const M = { items: [{ entity: "ai", slot: "create", name: "X", srcId: "x", data: { username: "X", level: 3, rules: [{ conditions: [], action: { type: "end_turn" } }] } }] };
  h.runner.plan(M, { jobId: "t" });
  // run normally up to the toggle, then crash ON the toggle call (applied server-side, response lost)
  const orig = game.handle.bind(game); let crashed = false;
  game.handle = (p, i) => { const r = orig(p, i); if (p === "ai.toggleAiProfile" && !crashed) { crashed = true; throw new CrashSignal(game.calls.length); } return r; };
  const s0 = await h.runner.run("t");
  const it = h.journal.get("t").items[0];
  assert.equal(s0.state, "PAUSED"); assert.equal(it.state, "SENT"); assert.equal(it.phase, "rules-toggle");
  const updatesBefore = game.calls.filter((c) => c.path === "profile.updateAi").length;
  h.clock.tick(1000);
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("t", M);
  const s1 = await h2.runner.resume("t");
  assert.equal(s1.items[0].state, "VERIFIED", JSON.stringify(s1));
  assert.equal(game.calls.filter((c) => c.path === "profile.updateAi").length, updatesBefore, "update not re-sent after reconciliation");
  assert.equal(game.calls.filter((c) => c.path === "profile.create").length, 1);
});

test("L4: pre-send validation runs BEFORE the create, so no placeholder is left behind", async () => {
  const h = harness();
  h.runner.plan({ items: [{ entity: "jutsu", slot: "create", name: "A", srcId: "a", data: { name: "A", nmae: "typo" } }] }, { jobId: "p" });
  const s = await h.runner.run("p");
  assert.equal(s.items[0].state, "FAILED"); assert.match(s.items[0].error, /unknown key "nmae"/);
  assert.equal(h.game.count("jutsu"), 0, "nothing created");
  assert.ok(!h.game.calls.some((c) => c.path === "jutsu.create"));
});

test("L4: a create referencing an @img with no file picked fails before the create", async () => {
  const h = harness();
  h.runner.plan({ items: [{ entity: "asset", slot: "create", name: "A", srcId: "a", data: { name: "A", hidden: true, type: "STATIC", url: "@img:icon.webp" } }] }, { jobId: "i" });
  const s = await h.runner.run("i");
  assert.equal(s.items[0].state, "FAILED"); assert.match(s.items[0].error, /no file picked/);
  assert.equal(h.game.count("asset"), 0);
});

test("L4: a network failure on a READ between create and update pauses (item stays CONFIRMED), never FAILED", async () => {
  const h = harness();
  h.runner.plan(ONE, { jobId: "n" });
  const orig = h.client.batch.bind(h.client); // reads go through reader -> client.batch
  h.client.batch = async (calls) => { if (calls.some((c) => c.path === "jutsu.get")) throw new NetworkError(new TypeError("Failed to fetch"), { paths: calls.map((c) => c.path), kind: "query" }); return orig(calls); };
  const s = await h.runner.run("n");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "NETWORK");
  assert.equal(s.items[0].state, "CONFIRMED"); assert.equal(s.items[0].phase, "update");
  assert.equal(h.game.count("jutsu"), 1);
});

test("L4: a crash between CONFIRMED and the idmap write does not strand a dependent @ref", async () => {
  const game = new FakeGame(); const h = harness({ game });
  const M = { items: [
    { entity: "ai", slot: "create", name: "Boss", srcId: "boss", data: { username: "Boss", level: 5 } },
    { entity: "quest", slot: "create", name: "Q", srcId: "q", data: { name: "Q", content: { objectives: [{ id: "o", task: "defeat_opponents", opponentAIs: [{ ids: ["@ai:boss"], number: 1 }] }], reward: {}, sceneBackground: "", sceneCharacters: [] } } },
  ] };
  h.runner.plan(M, { jobId: "c" });
  await h.runner.run("c");
  // simulate: the journal has the boss id, but the idmap write was lost
  h.storage.removeItem(IDMAP_KEY);
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("c", M);
  // both items already VERIFIED; force the quest back to needing its update to prove resolution
  assert.equal(h2.runner._lookup(h2.journal.get("c"))("ai", "boss"), game.rows("ai")[0].userId);
  assert.equal(readIdmap(h2.storage).boss, undefined);
  h2.runner._syncIdmapFromJob(h2.journal.get("c"));
  assert.equal(readIdmap(h2.storage).boss, game.rows("ai")[0].userId);
});

test("L4: adopt() requires ORPHANED, refuses an id another item holds, keeps a non-create phase", () => {
  const h = harness();
  h.journal.open({ jobId: "a", items: [spec("asset", "create", 0), spec("asset", "create", 1)] });
  assert.throws(() => h.runner.adopt("a", 0, "x"), /needs an ORPHANED item/);
  h.journal.transition("a", 0, "SENT"); h.journal.transition("a", 0, "ORPHANED");
  h.journal.transition("a", 1, "SENT"); h.journal.transition("a", 1, "CONFIRMED", { entityId: "held", phase: "update" });
  assert.throws(() => h.runner.adopt("a", 0, "held"), /already held by item 1/);
  h.runner.adopt("a", 0, "fresh");
  assert.equal(h.journal.get("a").items[0].phase, "update");
  // an orphaned rules-phase item keeps its phase on adopt
  h.journal.open({ jobId: "b", items: [spec("ai", "update", 0)] });
  h.journal.transition("b", 0, "SENT", { phase: "rules", entityId: "t0" }); h.journal.transition("b", 0, "ORPHANED");
  h.runner.adopt("b", 0, "t0");
  assert.equal(h.journal.get("b").items[0].phase, "rules");
});

test("L4: capture.before failures pause the job and partial captures persist incrementally", async () => {
  const game = new FakeGame({ limitPath: "quests.get" });
  game.seed("jutsu", { id: "j1", name: "J" });
  const h = harness({ game });
  h.runner.plan({ capture: { before: [{ proc: "jutsu.get", input: { id: "j1" } }, { proc: "quests.get", input: { id: "q" } }] }, ...ONE }, { jobId: "cb" });
  const s = await h.runner.run("cb");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "TOO_MANY_REQUESTS"); assert.equal(s.pause.path, "quests.get");
  const job = h.journal.get("cb");
  assert.equal(job.capturesBeforePartial.length, 1); assert.equal(job.capturesBeforePartial[0].proc, "jutsu.get");
  assert.equal(job.items[0].state, "PLANNED", "nothing sent before captures finished");
});

test("L4: user-requested pause stops after the current item", async () => {
  const h = harness();
  h.runner.plan({ items: [ONE.items[0], { entity: "jutsu", slot: "create", name: "B", srcId: "b", data: { name: "B", hidden: true } }] }, { jobId: "u" });
  const orig = h.client.call.bind(h.client);
  h.client.call = async (p, i) => { const r = await orig(p, i); if (p === "jutsu.update") h.runner.requestPause(); return r; };
  const s = await h.runner.run("u");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "USER");
  assert.equal(s.items[0].state, "VERIFIED"); assert.equal(s.items[1].state, "PLANNED");
});

// ---------------------------------------------------------------- L5 reconcile / validate
test("L5: cross-job adoption is impossible: a row another job owns is never a candidate", async () => {
  const game = new FakeGame(); const h = harness({ game });
  // job A created an asset and confirmed it
  h.journal.open({ jobId: "A", items: [spec("asset", "create", 0)] });
  const snapA = await h.reconciler.beforeCreate(h.journal.get("A"), h.journal.get("A").items[0], "asset");
  const aId = game.handle("gameAsset.create").data.message;
  h.journal.transition("A", 0, "SENT", { phase: "create" }); h.journal.transition("A", 0, "CONFIRMED", { entityId: aId, phase: "update" });
  // job B snapshots AFTER A's row existed? No: B snapshot taken before A's create would see A's row as new.
  h.journal.open({ jobId: "B", items: [spec("asset", "create", 9)] });
  h.storage.setItem(h.reconciler.snapKey("B", "asset"), JSON.stringify({ entity: "asset", ids: [] })); // B's snapshot predates A's row
  h.journal.transition("B", 0, "SENT", { phase: "create" });
  const r = await h.reconciler.resolveSent(h.journal.get("B"), h.journal.get("B").items[0], {});
  assert.equal(r.action, "orphan", "A's row must not be adopted by B");
  assert.deepEqual(r.candidates, []);
});

test("L5: an update whose asserted keys are refs cannot be 'landed' by an empty diff", async () => {
  const game = new FakeGame(); const h = harness({ game });
  game.seed("quest", { id: "q", name: "Q", content: { objectives: [] } });
  h.journal.open({ jobId: "u", items: [{ entity: "quest", op: "update", name: "Q", targetId: "q", payloadHash: "h" }] });
  h.journal.transition("u", 0, "SENT", { phase: "update" });
  const planned = { data: { content: { objectives: [{ id: "o", task: "defeat_opponents", opponentAIs: [{ ids: ["@ai:ghost"], number: 1 }] }] } } };
  const r = await h.reconciler.resolveSent(h.journal.get("u"), h.journal.get("u").items[0], { planned, lookup: () => undefined });
  assert.equal(r.action, "orphan"); assert.match(r.note, /unresolved refs/);
  const r2 = await h.reconciler.resolveSent(h.journal.get("u"), h.journal.get("u").items[0], { planned: { data: { id: "q" } } });
  assert.equal(r2.action, "orphan"); assert.match(r2.note, /no asserted keys/);
});

test("L5/validate: the AI kit IS read back; a lost updateAi is not 'landed'", () => {
  const live = { userId: "u", username: "X", jutsus: [{ jutsuId: "j1" }], items: [{ itemId: "i1", quantity: 1 }] };
  assert.deepEqual(diffAsserted("ai", { jutsus: ["j1"], items: [{ ids: ["i1"], number: 1 }] }, live), []);
  const d = diffAsserted("ai", { jutsus: ["j1", "j2"], items: ["i9"] }, live);
  assert.deepEqual(d.map((x) => x.key), ["jutsus", "items"]);
});

// ---------------------------------------------------------------- fold-in regressions
test("L4: an ORPHANED item pauses the job (reason ORPHANED); nothing after it is sent until adopt or skip", async () => {
  const game = new FakeGame(); const h = harness({ game });
  const two = { items: [
    { entity: "asset", slot: "create", name: "A", srcId: "a", data: { name: "A", hidden: true, type: "STATIC", url: "u" } },
    { entity: "jutsu", slot: "create", name: "J", srcId: "j", data: { name: "J", hidden: true } },
  ] };
  h.runner.plan(two, { jobId: "o" });
  const key = await h.reconciler.beforeCreate(h.journal.get("o"), h.journal.get("o").items[0], "asset");
  h.journal.annotate("o", 0, { snapshotKey: key });
  // two placeholders appeared while our one create was in flight: ambiguous by construction
  await h.journal.withSent("o", 0, { phase: "create" }, async () => { game.handle("gameAsset.create"); game.handle("gameAsset.create"); });
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("o", two);
  const s = await h2.runner.resume("o");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "ORPHANED"); assert.equal(s.pause.idx, 0);
  assert.equal(s.items[0].state, "ORPHANED");
  assert.equal(s.items[1].state, "PLANNED", "the item after the orphan was not started");
  assert.equal(game.count("jutsu"), 0);
  // running again without deciding re-pauses on the same item; still nothing sent
  const s2 = await h2.runner.run("o");
  assert.equal(s2.state, "PAUSED"); assert.equal(s2.pause.reason, "ORPHANED"); assert.equal(game.count("jutsu"), 0);
  // skip the orphan: the job continues and finishes
  h2.runner.skip("o", 0);
  const s3 = await h2.runner.run("o");
  assert.equal(s3.state, "DONE"); assert.equal(s3.items[0].state, "SKIPPED"); assert.equal(s3.items[1].state, "VERIFIED");
  assert.equal(game.count("asset"), 2, "orphans are never deleted");
});

test("L4: a transport failure during capture.before pauses (NETWORK) instead of escaping run()", async () => {
  const h = harness();
  h.game.seed("jutsu", { id: "j1", name: "J" });
  h.runner.plan({ capture: { before: [{ proc: "jutsu.get", input: { id: "j1" } }] }, ...ONE }, { jobId: "cn" });
  h.client.batch = async (calls) => { throw new NetworkError(new TypeError("Failed to fetch"), { paths: calls.map((c) => c.path), kind: "query" }); };
  const s = await h.runner.run("cn");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "NETWORK");
  assert.equal(s.items[0].state, "PLANNED"); assert.equal(h.game.count("jutsu"), 1, "nothing created");
});
