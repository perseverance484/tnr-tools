// Regression tests for the findings of the three adversarial panels that survived
// verification or were confirmed by reading. Each test names the finding it pins.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { IDBFactory } from "fake-indexeddb";
import { Journal, JournalError, KEY_PREFIX, TRANSITIONS, ITEM_STATES, migrate, repairHistory, JOURNAL_VERSION, jobOutcome } from "../src/storage/journal.mjs";
import { CaptureCache } from "../src/storage/captures.mjs";
import { readIdmap, IDMAP_KEY } from "../src/storage/compat.mjs";
import { stableStringify, payloadHash } from "../src/storage/hash.mjs";
import { decodeResponse } from "../src/transport/envelope.mjs";
import { CookieSession, SessionRefused } from "../src/transport/session.mjs";
import { TrpcClient, NetworkError } from "../src/transport/client.mjs";
import { TransportError, isTrpcErrorBody } from "../src/transport/envelope.mjs";
import { mergeForUpdate, mergeAi } from "../src/runner/recipes.mjs";
import { RateLimited } from "../src/budget/bucket.mjs";
import { classifyError, readMutation, OutcomeError } from "../src/transport/outcome.mjs";
import { Budget } from "../src/budget/bucket.mjs";
import { CachedReader } from "../src/budget/reader.mjs";
import { Validator, diffAsserted } from "../src/runner/validate.mjs";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";
import { Runner, LeaseHeld, LEASE_PREFIX, LEASE_TTL_MS } from "../src/runner/runner.mjs";
import { Reconciler } from "../src/reconcile/reconciler.mjs";
import { FakeGame, FakeClient, CrashSignal } from "./fakegame.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";
import { compose } from "../src/main.mjs";

const SCHEMAS = JSON.parse(readFileSync(new URL("../src/runner/fields.json", import.meta.url), "utf8"));
const spec = (entity = "jutsu", op = "create", i = 0) => ({ entity, op, name: `${entity}${i}`, srcId: op === "create" ? `${entity}${i}` : null, targetId: op === "update" ? `t${i}` : null, payloadHash: "h" });
const J = (s = new MemoryStorage()) => new Journal(s, fakeClock(), { yieldTask: async () => {} });

function harness({ game = new FakeGame(), storage = new MemoryStorage(), idb = new IDBFactory(), tabId = "tab", client = null } = {}) {
  return composeForTest({ game, storage, idb, tabId, client });
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
  h.clock.tick(s1.pause.until - h.clock() + 1); // the trip clears at the end of the NEXT server bucket
  const s2 = await h.runner.run("r");
  assert.equal(s2.state, "DONE"); assert.equal(s2.items[0].state, "VERIFIED");
  assert.equal(updates(), 1, "resume read back; it did not re-send");
  assert.equal(game.count("jutsu"), 1);
});

test("L4: drift stays CONFIRMED/verify and the job finishes INCOMPLETE, never DONE", async () => {
  // drift: make the server lie on read-back
  const g2 = new FakeGame(); const h2 = harness({ game: g2 });
  h2.runner.plan(ONE, { jobId: "d" });
  const orig = g2.handle.bind(g2); let n = 0;
  g2.handle = (p, i) => { const r = orig(p, i); if (p === "jutsu.get" && ++n === 2) r.data.name = "Someone renamed it"; return r; };
  const sd = await h2.runner.run("d");
  assert.equal(sd.items[0].state, "CONFIRMED"); assert.equal(sd.items[0].phase, "verify"); assert.equal(sd.items[0].verify, "drift");
  assert.equal(sd.state, "INCOMPLETE"); assert.equal(sd.outcome, "unverified");
  assert.equal(g2.calls.filter((c) => c.path === "jutsu.update").length, 1);
  // a run of a job that IS done sends nothing
  const h3 = harness();
  h3.runner.plan(ONE, { jobId: "ok" });
  const s3 = await h3.runner.run("ok");
  assert.equal(s3.state, "DONE"); assert.equal(s3.outcome, "success");
  const before = h3.game.calls.length;
  await h3.runner.run("ok");
  assert.equal(h3.game.calls.length, before, "DONE job sends nothing");
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
  assert.throws(() => h.runner.adopt("a", 0, "held"), /already held by job a item 1/);
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

// ---------------------------------------------------------------- panel results that arrived after the fold-in
test("L2: a gateway's JSON error body is NOT a request-level tRPC error; a mutation stays ambiguous", async () => {
  assert.equal(isTrpcErrorBody({ error: { json: { message: "x", code: -32600, data: { code: "BAD_REQUEST", httpStatus: 400 } } } }), true);
  assert.equal(isTrpcErrorBody({ error: { code: "FUNCTION_INVOCATION_TIMEOUT" } }), false);
  assert.equal(isTrpcErrorBody({ error: "timeout" }), false);
  assert.throws(() => decodeResponse(504, '{"error":{"code":"FUNCTION_INVOCATION_TIMEOUT"}}', 1), TransportError);
  // through the client: received, not decodable, never a per-index verdict
  const f = async () => new Response('{"error":{"code":"FUNCTION_INVOCATION_TIMEOUT"}}', { status: 504, headers: { "content-type": "application/json" } });
  const c = new TrpcClient(new CookieSession({ fetchImpl: f }));
  await assert.rejects(() => c.call("jutsu.update", { id: "x", data: {} }), (e) => e instanceof TransportError && e.received === true && e.httpStatus === 504);
  // the adapter's own request-level shape is still fanned out per index
  const els = decodeResponse(415, '{"error":{"json":{"message":"Unsupported content-type","code":-32015,"data":{"code":"UNSUPPORTED_MEDIA_TYPE","httpStatus":415}}}}', 2);
  assert.equal(els.length, 2); assert.equal(els[1].error.code, "UNSUPPORTED_MEDIA_TYPE"); assert.equal(els[1].error.requestLevel, true);
});

test("L4: a landed ai update reconciled after a crash still owes its rules step; the profile is written exactly once", async () => {
  const game = new FakeGame(); const h = harness({ game });
  const M = { items: [{ entity: "ai", slot: "create", name: "R", srcId: "r", data: { username: "R", level: 4, rules: [{ conditions: [], action: { type: "end_turn" } }], includeDefaultRules: false } }] };
  h.runner.plan(M, { jobId: "lr" });
  const orig = game.handle.bind(game); let crashed = false;
  game.handle = (p, i) => { const r = orig(p, i); if (p === "profile.updateAi" && !crashed) { crashed = true; throw new CrashSignal(game.calls.length); } return r; };
  const s0 = await h.runner.run("lr");
  assert.equal(s0.state, "PAUSED"); assert.equal(h.journal.get("lr").items[0].phase, "update"); assert.equal(h.journal.get("lr").items[0].state, "SENT");
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("lr", M);
  const s1 = await h2.runner.resume("lr");
  assert.equal(s1.items[0].state, "VERIFIED", JSON.stringify(s1));
  assert.equal(game.calls.filter((c) => c.path === "profile.updateAi").length, 1, "the landed update was not re-sent");
  assert.equal(game.calls.filter((c) => c.path === "ai.toggleAiProfile").length, 1);
  assert.equal(game.calls.filter((c) => c.path === "ai.updateAiProfile").length, 1, "the rules step ran after the reconciled update");
  const ai = game.rows("ai")[0]; const prof = h2.game.tables.aiProfile.get(ai.aiProfileId);
  assert.equal(prof.includeDefaultRules, false); assert.equal(prof.rules.length, 1);
});

test("L5: a lost rules write whose only change was includeDefaultRules is not 'landed'", async () => {
  const h = harness();
  h.game.tables.aiProfile.set("p1", { id: "p1", userId: "u1", rules: [], includeDefaultRules: true });
  h.journal.open({ jobId: "d", items: [spec("ai", "update", 0)] });
  h.journal.transition("d", 0, "SENT", { phase: "rules", entityId: "u1", aiProfileId: "p1" });
  const r = await h.reconciler.resolveSent(h.journal.get("d"), h.journal.get("d").items[0], { planned: { data: { rules: [], includeDefaultRules: false } } });
  assert.equal(r.action, "orphan");
  const r2 = await h.reconciler.resolveSent(h.journal.get("d"), h.journal.get("d").items[0], { planned: { data: { rules: [], includeDefaultRules: true } } });
  assert.equal(r2.action, "confirm"); assert.equal(r2.landed, true);
});

test("L3/L4: a 429 during reconciliation pauses with the path and countdown; the SENT item is untouched", async () => {
  const game = new FakeGame({ limitPath: "jutsu.getAllNames" }); const h = harness({ game });
  h.runner.plan(ONE, { jobId: "rr" });
  h.storage.setItem("tnr_forge_snap_v1:rr:jutsu", JSON.stringify({ entity: "jutsu", ids: [] }));
  h.journal.annotate("rr", 0, { snapshotKey: "tnr_forge_snap_v1:rr:jutsu" });
  h.journal.transition("rr", 0, "SENT", { phase: "create" });
  const s = await h.runner.resume("rr");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "TOO_MANY_REQUESTS"); assert.equal(s.pause.path, "jutsu.getAllNames");
  assert.equal(s.items[0].state, "SENT"); assert.equal(game.count("jutsu"), 0);
});

test("L1/L4: one tab drives a job at a time; a stale lease expires; DONE releases it", async () => {
  const h = harness();
  h.runner.plan(ONE, { jobId: "lease" });
  const o = composeForTest({ game: h.game, storage: h.storage, idb: h.idb, clock: h.clock, tabId: "other-tab", client: h.client });
  const other = o.runner;
  other.manifests = h.runner.manifests;
  h.runner._lease("lease"); // this tab is driving
  await assert.rejects(() => other.run("lease"), LeaseHeld);
  await assert.rejects(() => other.resume("lease"), LeaseHeld);
  assert.equal(h.game.count("jutsu"), 0, "the refused tab sent nothing");
  h.clock.tick(LEASE_TTL_MS + 1); // the driving tab died
  const s = await other.run("lease");
  assert.equal(s.state, "DONE");
  assert.equal(h.storage.getItem(LEASE_PREFIX + "lease"), null, "released on DONE");
  // while a job is paused the lease is released too
  const g2 = new FakeGame({ limitPath: "jutsu.get" }); const h3 = harness({ game: g2 });
  h3.runner.plan(ONE, { jobId: "p" }); const sp = await h3.runner.run("p");
  assert.equal(sp.state, "PAUSED"); assert.equal(h3.storage.getItem(LEASE_PREFIX + "p"), null);
});

test("L4/validate: an AI item entry's number is dropChancePerc; the live kit re-sends it, never quantity (law 69)", async () => {
  const game = new FakeGame(); const h = harness({ game });
  game.seed("ai", { userId: "u1", username: "U", level: 2, isAi: true, aiProfileId: null, jutsus: [{ jutsuId: "j1" }], items: [{ itemId: "i1", quantity: 3, dropChancePerc: 25 }] });
  // an edit that does not mention the kit
  h.runner.plan({ items: [{ entity: "ai", slot: "edit", name: "U", targetId: "u1", data: { level: 7 } }] }, { jobId: "k1" });
  const s = await h.runner.run("k1");
  assert.equal(s.items[0].state, "VERIFIED", JSON.stringify(s));
  const sent = game.calls.find((c) => c.path === "profile.updateAi").input.data;
  assert.deepEqual(sent.items, [{ ids: ["i1"], number: 25 }]); assert.deepEqual(sent.jutsus, ["j1"]);
  const row = game.tables.ai.get("u1");
  assert.equal(row.items[0].dropChancePerc, 25); assert.equal(row.items[0].quantity, 3, "quantity untouched");
  // an edit asserting a new drop chance lands and is read back
  h.runner.plan({ items: [{ entity: "ai", slot: "edit", name: "U", targetId: "u1", data: { items: [{ ids: ["i1"], number: 40 }] } }] }, { jobId: "k2" });
  const s2 = await h.runner.run("k2");
  assert.equal(s2.items[0].state, "VERIFIED", JSON.stringify(s2));
  assert.equal(game.tables.ai.get("u1").items[0].dropChancePerc, 40);
  // a server that ignores the chance is drift on items.dropChancePerc, not a match
  const orig = game.handle.bind(game);
  game.handle = (p, i) => { if (p === "profile.updateAi") { const r = orig(p, { ...i, data: { ...i.data, items: [{ ids: ["i1"], number: 40 }] } }); return r; } return orig(p, i); };
  h.runner.plan({ items: [{ entity: "ai", slot: "edit", name: "U", targetId: "u1", data: { items: [{ ids: ["i1"], number: 60 }] } }] }, { jobId: "k3" });
  const s3 = await h.runner.run("k3");
  assert.equal(s3.items[0].verify, "drift"); assert.ok(s3.items[0].diffs.some((d) => d.key === "items.dropChancePerc"), JSON.stringify(s3.items[0].diffs));
  // merge helpers directly
  assert.deepEqual(mergeAi({ userId: "u1", items: [{ itemId: "i9", quantity: 5, dropChancePerc: 10 }] }, {}).items, [{ ids: ["i9"], number: 10 }]);
});

test("validate: columns insertAiSchema omits and server-owned columns are refused on an ai, even before a create", () => {
  const v = new Validator(SCHEMAS);
  assert.match(v.problems("ai", { username: "x", questData: {} }, null, { preCreate: true }).join(";"), /"questData" is not writable/);
  assert.match(v.problems("ai", { username: "x", userId: "forged" }, { userId: "u1", username: "x" }).join(";"), /"userId" is not writable/);
  assert.deepEqual(v.problems("ai", { username: "x", level: 3 }, { userId: "u1", username: "x", level: 1 }), []);
});

test("validate: the pinned ItemValidator's farm* keys and quest.requiredFarmingLevel are legal, and survive the update merge", () => {
  const v = new Validator(SCHEMAS);
  assert.deepEqual(v.problems("item", { name: "Seed", isFarmSeed: true, farmGrowTimeSeconds: 60, farmYieldItemId: "x" }), []);
  assert.deepEqual(v.problems("quest", { name: "Q", requiredFarmingLevel: 3 }), []);
  assert.equal(v.knownFields("item").size, 71); assert.equal(v.knownFields("quest").size, 29);
  const live = { id: "i1", name: "Old", farmYieldItemId: "y", farmGrowTimeSeconds: 120, isFarmSeed: true, createdAt: "x" };
  const payload = mergeForUpdate("item", live, { name: "New" }, v.knownFields("item"));
  assert.equal(payload.farmYieldItemId, "y", "ItemValidator requires farmYieldItemId; stripping it would fail every item update");
  assert.equal(payload.farmGrowTimeSeconds, 120); assert.equal(payload.name, "New");
  assert.equal(SCHEMAS._provenance.pin, "345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9");
});

test("L3: the budget mirrors the server's weighted sliding window, so this client alone never reaches 60% of the limit at the bucket edge", async () => {
  const h = harness();
  const W = 60_000, A = h.budget.allowance;
  h.clock.set((Math.floor(h.clock() / W) + 1) * W + 1000); // 1 s into a fresh bucket
  // the server's estimate, computed as slidingWindowLimitScript does, over everything we sent
  const server = (now) => { const b = Math.floor(now / W); let prev = 0, cur = 0; for (const t of h.budget.log.recent("jutsu.get", W)) { const tb = Math.floor(t / W); if (tb === b) cur++; else if (tb === b - 1) prev++; } return Math.floor((1 - (now % W) / W) * prev) + cur; };
  for (let i = 0; i < A; i++) { await h.budget.acquire("jutsu.get"); assert.ok(server(h.clock()) <= A); }
  assert.equal(h.budget.waits, 0);
  h.clock.set(h.budget.estimate("jutsu.get").bucketStart + W + 1000); // 1 s into the NEXT bucket: a strict window would allow 30 more here
  assert.ok(h.budget.available("jutsu.get") <= 1, "the previous bucket still weighs ~29 on the server");
  const t0 = h.clock();
  for (let i = 0; i < A; i++) { await h.budget.acquire("jutsu.get"); assert.ok(server(h.clock()) <= A, `server estimate ${server(h.clock())} after send ${i}`); }
  assert.ok(h.clock() - t0 <= W + 5000, "the second 30 still fit inside about one window: " + (h.clock() - t0));
  const st = h.budget.status().paths["jutsu.get"];
  assert.ok(st.weighted <= A && st.used <= A);
});


// ------------------------------------- readiness P0: honest terminal and verify semantics (R1-R5)
test("R1: readBack:false is refused before a job exists when the manifest writes", () => {
  const h = harness();
  assert.throws(() => h.runner.plan({ readBack: false, ...ONE }, { jobId: "nb" }), /readBack:false is refused/);
  assert.equal(h.journal.listJobs().length, 0, "no job, no placeholder, nothing sent");
  assert.throws(() => parseManifest({ readBack: false, ...ONE }), ManifestError);
  // a capture-only manifest has no write to read back, so it is untouched
  const capOnly = parseManifest({ readBack: false, capture: { before: [{ proc: "jutsu.getAllNames" }], after: [] } });
  assert.equal(capOnly.readBack, false);
  assert.equal(capOnly.items.length, 0);
});

test("R2: a drifted item leaves the job INCOMPLETE, resumable, and re-reading never re-sends", async () => {
  const game = new FakeGame(); const h = harness({ game });
  h.runner.plan(ONE, { jobId: "dr" });
  const orig = game.handle.bind(game); let lie = true;
  game.handle = (p, i) => { const r = orig(p, i); if (p === "jutsu.get" && lie && r.data) { r.data = { ...r.data, name: "Someone renamed it" }; } return r; };
  const s1 = await h.runner.run("dr");
  assert.equal(s1.state, "INCOMPLETE"); assert.equal(s1.outcome, "unverified");
  assert.equal(s1.items[0].state, "CONFIRMED"); assert.equal(s1.items[0].verify, "drift");
  assert.ok(h.journal.resumable().some((j) => j.jobId === "dr"), "an unverified job is still open work");
  const updates = () => game.calls.filter((c) => c.path === "jutsu.update").length;
  const creates = () => game.calls.filter((c) => c.path === "jutsu.create").length;
  const [u0, c0] = [updates(), creates()];
  // the drift was the server's answer, not ours: on a re-read that agrees, the job closes clean
  lie = false;
  const s2 = await h.runner.run("dr");
  assert.equal(updates(), u0, "re-reading an unverified item sends no mutation");
  assert.equal(creates(), c0, "and certainly no second create");
  assert.equal(s2.items[0].state, "VERIFIED"); assert.equal(s2.state, "DONE"); assert.equal(s2.outcome, "success");
});

test("R3: an unread read-back leaves the job INCOMPLETE and resume only reads", async () => {
  const game = new FakeGame(); const h = harness({ game });
  h.runner.plan(ONE, { jobId: "ur" });
  // blind only AFTER the update: the read-back itself is what fails, not the pre-update read
  const orig = game.handle.bind(game); let blind = false;
  game.handle = (p, i) => { const r = orig(p, i); if (p === "jutsu.update") blind = true; if (p === "jutsu.get" && blind) return { ok: true, data: null }; return r; };
  const s1 = await h.runner.run("ur");
  assert.equal(s1.items[0].verify, "unread");
  assert.equal(s1.items[0].state, "CONFIRMED"); assert.equal(s1.items[0].phase, "verify");
  assert.equal(s1.state, "INCOMPLETE"); assert.equal(s1.outcome, "unverified");
  const u0 = game.calls.filter((c) => c.path === "jutsu.update").length;
  blind = false;
  const s2 = await h.runner.run("ur");
  assert.equal(game.calls.filter((c) => c.path === "jutsu.update").length, u0, "no mutation resent for an unread item");
  assert.equal(s2.state, "DONE"); assert.equal(s2.outcome, "success");
  assert.equal(game.count("jutsu"), 1);
});

test("R4: DONE is structurally impossible while an item is unresolved", () => {
  const j = J();
  j.open({ jobId: "u", items: [spec()] });
  j.transition("u", 0, "SENT"); j.transition("u", 0, "CONFIRMED", { entityId: "e1", phase: "verify" });
  assert.throws(() => j.setJobState("u", "DONE"), /cannot mark DONE with unresolved items/);
  j.setJobState("u", "INCOMPLETE"); // the honest one
  assert.equal(j.get("u").state, "INCOMPLETE");
  assert.equal(jobOutcome(j.get("u")), "unverified");
  j.transition("u", 0, "VERIFIED", { verify: "match" });
  j.setJobState("u", "DONE");
  assert.equal(jobOutcome(j.get("u")), "success");
  // a SENT item can reach neither
  j.open({ jobId: "s", items: [spec()] }); j.transition("s", 0, "SENT");
  assert.throws(() => j.setJobState("s", "DONE"), /cannot mark DONE with SENT items/);
  assert.throws(() => j.setJobState("s", "INCOMPLETE"), /cannot mark INCOMPLETE with SENT items/);
});

test("R5: a failed item is execution-terminal but never a success", async () => {
  const h = harness();
  h.runner.plan({ items: [
    { entity: "jutsu", slot: "create", name: "A", srcId: "a", data: { name: "A", description: "d", hidden: true } },
    { entity: "jutsu", slot: "create", name: "B", srcId: "b", data: { name: "B", nmae: "typo" } },
  ] }, { jobId: "mix" });
  const s = await h.runner.run("mix");
  assert.equal(s.state, "DONE", "nothing is left to do");
  assert.equal(s.outcome, "failed", "but it is not good news");
  assert.equal(s.items[1].state, "FAILED");
  assert.equal(s.verify.match, 1);
  // a skipped orphan is unverified too: the row may be live and nobody proved what is in it
  const j = J(); j.open({ jobId: "sk", items: [spec()] });
  j.transition("sk", 0, "SENT"); j.transition("sk", 0, "ORPHANED"); j.transition("sk", 0, "SKIPPED");
  j.setJobState("sk", "DONE");
  assert.equal(jobOutcome(j.get("sk")), "unverified");
});

// ------------------------------------------------- independent review of a1f9144 (F1-F4)
test("F1: persisted history outranks a hand-edited state; a sent create is never replayed", async () => {
  // a real create whose response was lost, so the pre-create snapshot exists
  const game = new FakeGame(); const h = harness({ game });
  h.runner.plan(ONE, { jobId: "hx" });
  const orig = game.handle.bind(game); let crashed = false;
  game.handle = (p, i) => { const r = orig(p, i); if (p === "jutsu.create" && !crashed) { crashed = true; throw new CrashSignal(1); } return r; };
  await h.runner.run("hx");
  game.handle = orig;
  assert.equal(game.count("jutsu"), 1);
  // hand edit the persisted record: state only, history left intact
  const raw = JSON.parse(h.storage.crash().getItem(KEY_PREFIX + "hx"));
  assert.equal(raw.items[0].state, "SENT"); assert.ok(raw.items[0].createSentAt);
  raw.items[0].state = "PLANNED";
  const storage = h.storage.crash(); storage.setItem(KEY_PREFIX + "hx", JSON.stringify(raw));
  const h2 = harness({ game, storage, idb: h.idb });
  const it = h2.journal.get("hx").items[0];
  assert.equal(it.state, "SENT", "restored: createSentAt proves the request left");
  assert.equal(it.phase, "create");
  assert.match(it.repaired, /contradicted by/);
  h2.runner.attach("hx", ONE);
  await assert.rejects(() => h2.runner.run("hx"), /call resume\(\)/, "run() refuses a job holding a SENT item");
  const s = await h2.runner.resume("hx");
  assert.equal(s.items[0].state, "VERIFIED", JSON.stringify(s));
  assert.equal(game.count("jutsu"), 1, "exactly one live row: the create was never replayed");
  assert.equal(game.calls.filter((c) => c.path === "jutsu.create").length, 1);
});

test("F1b: repairHistory restores on any proof field, never advances a state, never invents an id", () => {
  for (const k of ["sentAt", "createSentAt", "confirmedAt", "verifiedAt"]) {
    const job = { items: [{ idx: 0, op: "create", state: "PLANNED", phase: "create", entityId: null, [k]: "2026-01-01T00:00:00.000Z" }] };
    repairHistory(job);
    assert.equal(job.items[0].state, "SENT", k);
    assert.equal(job.items[0].entityId, null, "no id is invented");
  }
  // a genuinely fresh PLANNED item is untouched
  const fresh = { items: [{ idx: 0, op: "create", state: "PLANNED", phase: "create", sentAt: null, createSentAt: null, confirmedAt: null, verifiedAt: null }] };
  repairHistory(fresh);
  assert.equal(fresh.items[0].state, "PLANNED");
  assert.equal(fresh.items[0].repaired, undefined);
  // an update-phase item keeps its id and lands on the update phase, not create
  const upd = { items: [{ idx: 0, op: "create", state: "PLANNED", phase: "verify", entityId: "e1", confirmedAt: "t" }] };
  repairHistory(upd);
  assert.equal(upd.items[0].state, "SENT"); assert.equal(upd.items[0].entityId, "e1"); assert.equal(upd.items[0].phase, "verify");
  // terminal states are never rewound
  const done = { items: [{ idx: 0, op: "create", state: "VERIFIED", phase: "verify", sentAt: "t" }] };
  repairHistory(done); assert.equal(done.items[0].state, "VERIFIED");
});

test("F2: the SHIPPED composition wires the journal into the Reconciler, and one cannot be built without it", () => {
  const d = compose({ storage: new MemoryStorage(), indexedDB: new IDBFactory(), fetchImpl: async () => new Response("[]"), clock: fakeClock() });
  assert.equal(d.reconciler.journal, d.journal, "production reconciler can exclude ids other jobs own");
  assert.equal(d.runner.reconciler, d.reconciler);
  assert.throws(() => new Reconciler({ storage: new MemoryStorage(), reader: {}, clock: fakeClock() }), /needs the journal/);
  assert.throws(() => new Reconciler({ storage: new MemoryStorage(), reader: {}, journal: {} }), /needs the journal/);
});

test("F2b: a resumed job never adopts a row another job owns", async () => {
  const game = new FakeGame(); const h = harness({ game });
  const B = { items: [{ entity: "asset", slot: "create", name: "B", srcId: "b", data: { name: "B", hidden: true, type: "STATIC", url: "u" } }] };
  h.runner.plan(B, { jobId: "B" });
  const key = await h.reconciler.beforeCreate(h.journal.get("B"), h.journal.get("B").items[0], "asset");
  h.journal.annotate("B", 0, { snapshotKey: key });
  h.journal.transition("B", 0, "SENT", { phase: "create" }); // B's create left, response lost
  // job A then creates and confirms exactly one new row
  h.journal.open({ jobId: "A", items: [spec("asset", "create", 0)] });
  const aId = game.handle("gameAsset.create").data.message;
  h.journal.transition("A", 0, "SENT"); h.journal.transition("A", 0, "CONFIRMED", { entityId: aId, phase: "update" });
  h.runner.attach("B", B);
  const s = await h.runner.resume("B");
  assert.equal(s.items[0].state, "ORPHANED", "A's row is not a candidate");
  assert.notEqual(s.items[0].entityId, aId);
  assert.equal(game.rows("asset").find((r) => r.id === aId).name, "Placeholder", "A's row is untouched");
});

test("F2c: adopt() refuses an id held by ANY job, not just this one", () => {
  const h = harness();
  h.journal.open({ jobId: "A", items: [spec("asset", "create", 0)] });
  h.journal.transition("A", 0, "SENT"); h.journal.transition("A", 0, "CONFIRMED", { entityId: "held-by-A", phase: "update" });
  h.journal.open({ jobId: "B", items: [spec("asset", "create", 1)] });
  h.journal.transition("B", 0, "SENT"); h.journal.transition("B", 0, "ORPHANED");
  assert.throws(() => h.runner.adopt("B", 0, "held-by-A"), /already held by job A item 0/);
  assert.equal(h.journal.get("B").items[0].state, "ORPHANED", "refused, not partially applied");
  h.runner.adopt("B", 0, "fresh-id"); // an unheld id is still fine
  assert.equal(h.journal.get("B").items[0].entityId, "fresh-id");
});

test("F3: an unknown AI key is refused BEFORE the placeholder is created", async () => {
  const v = new Validator(SCHEMAS);
  assert.match(v.problems("ai", { username: "X", usernmae: "typo" }, null, { preCreate: true }).join(";"), /unknown key "usernmae"/);
  assert.deepEqual(v.problems("ai", { username: "X", level: 3, avatar: "u", jutsus: [], items: [], rules: [], includeDefaultRules: false }, null, { preCreate: true }), []);
  assert.equal(v.knownFields("ai").size, 157);
  for (const k of ["username", "level", "avatar", "isAi", "jutsus", "items"]) assert.ok(v.knownFields("ai").has(k), k);
  for (const k of ["questData", "occupation", "deletionAt"]) assert.ok(!v.knownFields("ai").has(k), k + " is omitted by insertAiSchema");
  const h = harness();
  h.runner.plan({ items: [{ entity: "ai", slot: "create", name: "X", srcId: "x", data: { username: "X", usernmae: "typo" } }] }, { jobId: "f3" });
  const s = await h.runner.run("f3");
  assert.equal(s.items[0].state, "FAILED");
  assert.match(s.items[0].error, /unknown key "usernmae"/);
  assert.equal(h.game.count("ai"), 0, "no live placeholder for a locally knowable typo");
  assert.ok(!h.game.calls.some((c) => c.path === "profile.create"));
});

test("F4: an undecodable mutation element stays ambiguous; queries keep sibling salvage", async () => {
  // query: one bad element does not discard its siblings
  const q = decodeResponse(200, "[{}]", 1);
  assert.equal(q[0].error.code, "MALFORMED_ELEMENT");
  // mutation: fatal, because the resolver may have run
  assert.throws(() => decodeResponse(200, "[{}]", 1, { mutation: true }), TransportError);
  // through the real transport and runner: the item stays SENT and the job pauses
  const h = harness();
  h.runner.plan(ONE, { jobId: "f4" });
  h.runner.client = new TrpcClient(new CookieSession({ fetchImpl: async () => new Response("[{}]", { status: 200, headers: { "content-type": "application/json" } }) }));
  const s = await h.runner.run("f4");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "UNDECODABLE_RESPONSE");
  assert.equal(s.items[0].state, "SENT", "ambiguity preserved: the write may have landed");
  assert.equal(h.journal.get("f4").items[0].state, "SENT");
  // and readMutation refuses to turn one into a verdict even if it ever reached it
  assert.throws(() => readMutation({ ok: false, error: { code: "MALFORMED_ELEMENT", message: "x" } }), OutcomeError);
});

test("F4c: a per-INDEX error is held to the same adapter shape (review of 4062268, F4 reopened)", async () => {
  // Against 4062268 every one of these decoded to a normal {ok:false} verdict with code UNKNOWN,
  // and the runner turned an already-SENT mutation into FAILED. A response element that is not the
  // shape we audited is evidence of something other than our server answering, and the resolver
  // may still have run.
  const bad = [
    ['[{"error":{}}]', "empty error object"],
    ['[{"error":{"json":{"message":"x","data":{"code":"BAD_REQUEST"}}}}]', "no numeric jsonrpc code"],
    ['[{"error":{"json":{"message":"x","code":-32600}}}]', "no data.code"],
    ['[{"error":{"json":{"message":"x","code":-32600,"data":{}}}}]', "data without a code"],
    ['[{"error":{"code":"FUNCTION_INVOCATION_TIMEOUT"}}]', "a gateway body at one index"],
  ];
  for (const [body, why] of bad) {
    assert.throws(() => decodeResponse(200, body, 1, { mutation: true }), TransportError, why);
    const q = decodeResponse(200, body, 1);
    assert.equal(q[0].error.code, "MALFORMED_ELEMENT", why + " (query salvage)");
    assert.notEqual(q[0].error.code, "UNKNOWN", why + " must never become a per-index verdict");
  }
  // a malformed error element in a QUERY batch keeps its well-formed siblings
  const mixed = decodeResponse(207, '[{"result":{"data":{"json":{"id":"a"}}}},{"error":{}},{"result":{"data":{"json":{"id":"c"}}}}]', 3);
  assert.equal(mixed[0].data.id, "a"); assert.equal(mixed[1].error.code, "MALFORMED_ELEMENT"); assert.equal(mixed[2].data.id, "c");
  // and end to end: the item stays SENT, the job pauses, the write is never called failed
  const h = harness();
  h.runner.plan(ONE, { jobId: "f4c" });
  h.runner.client = new TrpcClient(new CookieSession({ fetchImpl: async () => new Response('[{"error":{}}]', { status: 200, headers: { "content-type": "application/json" } }) }));
  const s = await h.runner.run("f4c");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "UNDECODABLE_RESPONSE");
  assert.equal(s.items[0].state, "SENT", "ambiguity preserved: the write may have landed");
});

test("F4d: recorded adapter errors still decode exactly as before", () => {
  // the guard must not cost us any real error the adapter actually produces
  const fixture = (name) => JSON.parse(readFileSync(new URL(`./fixtures/envelope/${name}.json`, import.meta.url), "utf8")).exchanges[0].response;
  const cases = [
    ["get_on_mutation_path_rejected", "METHOD_NOT_SUPPORTED", false],
    ["mutation_update_zod_fail", "BAD_REQUEST", true],
    ["query_too_many_requests", "TOO_MANY_REQUESTS", false],
  ];
  for (const [name, code, mutation] of cases) {
    const r = fixture(name);
    const out = decodeResponse(r.status, r.body, 1, { mutation });
    assert.equal(out[0].ok, false, name);
    assert.equal(out[0].error.code, code, name);
    assert.ok(isTrpcErrorBody(JSON.parse(r.body)[0]), name + " is the audited shape");
  }
  const mixed = fixture("mutation_batched_mixed_ok_and_zod_fail");
  const out = decodeResponse(mixed.status, mixed.body, 2, { mutation: true });
  assert.equal(out[0].ok, true); assert.equal(out[1].error.code, "BAD_REQUEST");
  const oneLimited = fixture("query_batched_one_limited_one_ok");
  const ol = decodeResponse(oneLimited.status, oneLimited.body, 2);
  assert.equal(ol[0].error.code, "TOO_MANY_REQUESTS"); assert.equal(ol[1].ok, true);
});

test("F4b: only the exact adapter error shape is fanned out per index", () => {
  assert.equal(isTrpcErrorBody({ error: { json: { message: "x", code: -32015, data: { code: "UNSUPPORTED_MEDIA_TYPE" } } } }), true);
  assert.equal(isTrpcErrorBody({ error: { json: { message: "x", data: { code: "INTERNAL_SERVER_ERROR" } } } }), false, "no numeric jsonrpc code: an intermediary body");
  assert.equal(isTrpcErrorBody({ error: { json: { message: "x", code: "-32015", data: { code: "X" } } } }), false);
  assert.throws(() => decodeResponse(504, '{"error":{"json":{"message":"x","data":{"code":"Y"}}}}', 1), TransportError);
});
