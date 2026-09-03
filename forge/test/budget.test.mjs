import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { Budget, SendLog, RateLimited, SENDLOG_KEY } from "../src/budget/bucket.mjs";
import { CachedReader, readInput } from "../src/budget/reader.mjs";
import { CaptureCache } from "../src/storage/captures.mjs";
import { TrpcClient } from "../src/transport/client.mjs";
import { CookieSession } from "../src/transport/session.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";

/** sleep that advances the fake clock instead of waiting */
function fakeSleep(clock) { const calls = []; const s = async (ms) => { calls.push(ms); clock.tick(ms); }; s.calls = calls; return s; }
const okRow = (id) => `{"result":{"data":{"json":{"id":"${id}","name":"n"}}}}`;
const limitedEl = (path) => `{"error":{"json":{"message":"You are moving too fast! Incident logged for review","code":-32029,"data":{"code":"TOO_MANY_REQUESTS","httpStatus":429,"path":"${path}","zodError":null}}}}`;
function scripted(script) {
  const calls = [];
  const f = async (url, init) => { calls.push({ url, init }); const n = script.shift(); if (!n) throw new Error("script exhausted"); return new Response(n.body, { status: n.status, headers: { "content-type": "application/json" } }); };
  f.calls = calls; return f;
}
function mk({ margin = 0.5, script = [], limit = 60 } = {}) {
  const storage = new MemoryStorage(); const clock = fakeClock(); const sleep = fakeSleep(clock);
  const budget = new Budget({ storage, clock, sleep, margin, limit });
  const fetch = scripted(script);
  const client = new TrpcClient(new CookieSession({ fetchImpl: fetch }));
  const cache = new CaptureCache(new IDBFactory(), clock);
  const reader = new CachedReader({ client, cache, budget });
  return { storage, clock, sleep, budget, fetch, client, cache, reader };
}

test("allowance is floor(limit * margin); margin validated", () => {
  assert.equal(new Budget({ storage: new MemoryStorage(), margin: 0.5 }).allowance, 30);
  assert.equal(new Budget({ storage: new MemoryStorage(), margin: 1 }).allowance, 60);
  assert.throws(() => new Budget({ storage: new MemoryStorage(), margin: 0 }));
  assert.throws(() => new Budget({ storage: new MemoryStorage(), margin: 1.5 }));
});

test("unlimited path: acquire never waits and never records", async () => {
  const { budget, storage, sleep } = mk();
  await budget.acquire("profile.getAi", 5);
  await budget.acquire("jutsu.update", 1);
  assert.equal(storage.getItem(SENDLOG_KEY), null);
  assert.equal(sleep.calls.length, 0);
  assert.equal(budget.available("profile.getAi"), Infinity);
});

test("limited path: acquire records WRITE-AHEAD, before resolving", async () => {
  const { budget, storage } = mk();
  const p = budget.acquire("jutsu.get", 2);
  await p;
  const log = JSON.parse(storage.getItem(SENDLOG_KEY));
  assert.equal(log["jutsu.get"].length, 2);
  assert.equal(budget.available("jutsu.get"), 28);
});

test("the 31st send waits until the oldest ages out, then proceeds", async () => {
  const { budget, sleep, clock } = mk();
  for (let i = 0; i < 30; i++) { await budget.acquire("jutsu.get"); clock.tick(100); }
  assert.equal(budget.available("jutsu.get"), 0);
  await budget.acquire("jutsu.get"); // must wait ~57s for the first timestamp to age out
  assert.equal(sleep.calls.length, 1);
  assert.ok(sleep.calls[0] > 50_000 && sleep.calls[0] <= 60_000, "waited " + sleep.calls[0]);
  assert.equal(budget.waits, 1);
});

test("window survives eviction: a restarted Budget still sees the spent tokens", async () => {
  const { budget, storage, clock } = mk();
  for (let i = 0; i < 30; i++) await budget.acquire("jutsu.get");
  const after = storage.crash();
  const sleep2 = fakeSleep(clock);
  const b2 = new Budget({ storage: after, clock, sleep: sleep2 });
  assert.equal(b2.available("jutsu.get"), 0);
  await b2.acquire("jutsu.get");
  assert.equal(sleep2.calls.length, 1);
});

test("paths are independent buckets (the server key is path-userId)", async () => {
  const { budget } = mk();
  for (let i = 0; i < 30; i++) await budget.acquire("jutsu.get");
  assert.equal(budget.available("jutsu.get"), 0);
  assert.equal(budget.available("item.get"), 30);
});

test("acquire more than the allowance at once is refused, not deadlocked", async () => {
  const { budget } = mk();
  await assert.rejects(() => budget.acquire("jutsu.get", 31), /chunk smaller/);
});

test("observe: a 429 at any index persists the trip and throws RateLimited; nothing is retried", async () => {
  const { budget, storage, clock } = mk();
  const results = [{ ok: true, data: {} }, { ok: false, error: { code: "TOO_MANY_REQUESTS", path: "jutsu.get", message: "moving too fast" } }];
  assert.throws(() => budget.observe(results, ["jutsu.get", "jutsu.get"]), (e) => e instanceof RateLimited && e.path === "jutsu.get" && e.index === 1 && e.until === clock() + 60_000);
  const t = JSON.parse(storage.getItem(SENDLOG_KEY)).__tripped;
  assert.equal(t.path, "jutsu.get");
  // while tripped, acquire refuses outright
  await assert.rejects(() => budget.acquire("jutsu.get"), RateLimited);
  await assert.rejects(() => budget.acquire("item.get"), RateLimited); // any limited path: the account was penalised
  // after the window the trip clears itself
  clock.tick(60_001);
  await budget.acquire("jutsu.get");
});

test("readInput: profile.getAi takes userId, everything else id", () => {
  assert.deepEqual(readInput("profile.getAi", "u1"), { userId: "u1" });
  assert.deepEqual(readInput("jutsu.get", "j1"), { id: "j1" });
  assert.deepEqual(readInput("gameAsset.get", "a1"), { id: "a1" }); // no raw-string fallback (audit D5)
});

test("reader.get: miss fetches once and caches; hit fetches nothing and spends nothing", async () => {
  const { reader, fetch, budget } = mk({ script: [{ status: 200, body: `[${okRow("j1")}]` }] });
  const a = await reader.get("jutsu.get", "j1");
  assert.equal(a.ok, true); assert.equal(a.data.id, "j1"); assert.equal(fetch.calls.length, 1);
  assert.equal(budget.available("jutsu.get"), 29);
  const b = await reader.get("jutsu.get", "j1");
  assert.equal(b.cached, true); assert.equal(fetch.calls.length, 1); assert.equal(budget.available("jutsu.get"), 29);
  assert.deepEqual(reader.stats, { hits: 1, misses: 1, requests: 1 });
});

test("reader.getMany: cached ids are skipped, misses batched into one request, results in id order", async () => {
  const { reader, fetch, cache } = mk({ script: [{ status: 200, body: `[${okRow("b")},${okRow("d")},${okRow("e")}]` }] });
  await cache.put({ path: "jutsu.get", id: "a", data: { id: "a" } });
  await cache.put({ path: "jutsu.get", id: "c", data: { id: "c" } });
  const out = await reader.getMany("jutsu.get", ["a", "b", "c", "d", "e"]);
  assert.deepEqual(out.map((r) => r.data.id), ["a", "b", "c", "d", "e"]);
  assert.equal(fetch.calls.length, 1);
  assert.match(fetch.calls[0].url, /jutsu\.get,jutsu\.get,jutsu\.get\?batch=1/);
  assert.ok(await cache.get("jutsu.get", "e"));
});

test("reader.getMany over the allowance: chunks and waits between chunks, never trips", async () => {
  const two = (a, b) => `[${okRow(a)},${okRow(b)}]`;
  const { reader, fetch, sleep, budget } = mk({ margin: 2 / 60, script: [{ status: 200, body: two("1", "2") }, { status: 200, body: two("3", "4") }, { status: 200, body: `[${okRow("5")}]` }] });
  assert.equal(budget.allowance, 2);
  const out = await reader.getMany("jutsu.get", ["1", "2", "3", "4", "5"]);
  assert.deepEqual(out.map((r) => r.data.id), ["1", "2", "3", "4", "5"]);
  assert.equal(fetch.calls.length, 3);
  assert.equal(sleep.calls.length, 2); // waited before chunk 2 and chunk 3
});

test("reader: a 429 hidden in a 207 caches the ok index, then throws RateLimited, and is never retried", async () => {
  const { reader, fetch, cache } = mk({ script: [{ status: 207, body: `[${okRow("ok")},${limitedEl("jutsu.get")}]` }] });
  await assert.rejects(() => reader.getMany("jutsu.get", ["ok", "lim"]), (e) => e instanceof RateLimited && e.index === 1);
  assert.equal(fetch.calls.length, 1);
  assert.ok(await cache.get("jutsu.get", "ok"), "the successful index must be cached before the throw");
  assert.equal(await cache.get("jutsu.get", "lim"), null);
  // and a second attempt does not send while tripped
  await assert.rejects(() => reader.get("jutsu.get", "lim"), RateLimited);
  assert.equal(fetch.calls.length, 1);
});

test("reader.list caches under id '' and honours fresh", async () => {
  const body = `[{"result":{"data":{"json":[{"id":"a","name":"A"}]}}}]`;
  const { reader, fetch } = mk({ script: [{ status: 200, body }, { status: 200, body }] });
  const a = await reader.list("jutsu.getAllNames");
  assert.equal(a.data[0].id, "a"); assert.equal(fetch.calls.length, 1);
  const b = await reader.list("jutsu.getAllNames");
  assert.equal(b.cached, true); assert.equal(fetch.calls.length, 1);
  await reader.list("jutsu.getAllNames", { fresh: true });
  assert.equal(fetch.calls.length, 2);
});

test("status() reports per-path usage and the trip", async () => {
  const { budget, clock } = mk();
  await budget.acquire("quests.get", 3);
  const s = budget.status();
  assert.equal(s.paths["quests.get"].used, 3);
  assert.equal(s.paths["quests.get"].allowance, 30);
  assert.equal(s.paths["quests.get"].serverLimit, 60);
  assert.equal(s.paths["quests.get"].resetInMs, 60_000);
  assert.equal(s.tripped, null);
  assert.equal(s.margin, 0.5);
  clock.tick(10_000);
  assert.equal(budget.status().paths["quests.get"].resetInMs, 50_000);
});

test("SendLog tolerates a corrupt record by starting empty (never blocks a send on bad JSON)", () => {
  const s = new MemoryStorage(); s.setItem(SENDLOG_KEY, "{bad");
  const log = new SendLog(s, fakeClock());
  assert.deepEqual(log.inWindow("jutsu.get", 60_000), []);
});
