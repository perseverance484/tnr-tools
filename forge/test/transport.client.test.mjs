import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { CookieSession, Session } from "../src/transport/session.mjs";
import { TrpcClient, NetworkError } from "../src/transport/client.mjs";
import { TransportError } from "../src/transport/envelope.mjs";
import { PROCEDURES, LIMITED_PATHS, MUTATION_PATHS, procedure } from "../src/transport/procedures.mjs";

const DIR = join(dirname(fileURLToPath(import.meta.url)), "fixtures", "envelope");
const fx = (n) => JSON.parse(readFileSync(join(DIR, n + ".json"), "utf8"));

/** A scripted fetch: records calls, answers from a queue of {status, body} or throws. */
function scriptedFetch(script) {
  const calls = [];
  const f = async (url, init) => {
    calls.push({ url, init });
    const next = script.shift();
    if (!next) throw new Error("script exhausted");
    if (next.throw) throw next.throw;
    return new Response(next.body, { status: next.status, headers: { "content-type": "application/json" } });
  };
  f.calls = calls;
  return f;
}
const resOf = (name) => ({ status: fx(name).exchanges[0].response.status, body: fx(name).exchanges[0].response.body });

test("procedure table: 43 audited paths, limited set is exactly the publicProcedure reads", () => {
  assert.equal(Object.keys(PROCEDURES).length, 43);
  assert.equal(LIMITED_PATHS.length, 16);
  for (const p of LIMITED_PATHS) assert.equal(PROCEDURES[p].kind, "query", p + " limited but not a query");
  for (const p of MUTATION_PATHS) assert.equal(PROCEDURES[p].limited, false, p + " is a mutation and must not be limited");
  // verification F4 corrections applied
  assert.equal(PROCEDURES["item.get"].mcp, true);
  assert.equal(PROCEDURES["profile.create"].mcp, true);
  // the two protected reads are not limited
  assert.equal(PROCEDURES["profile.getAi"].limited, false);
  assert.equal(PROCEDURES["ai.getAiProfile"].limited, false);
  assert.throws(() => procedure("jutsu.nope"), /unknown procedure/);
});

test("CookieSession: same-origin credentials, never an Authorization header", async () => {
  const f = scriptedFetch([{ status: 200, body: "[]" }]);
  const s = new CookieSession({ fetchImpl: f });
  await s.fetch("/api/trpc/x?batch=1", { method: "GET" });
  assert.equal(f.calls[0].init.credentials, "same-origin");
  assert.equal(f.calls[0].url, "/api/trpc/x?batch=1");
  await assert.rejects(() => s.fetch("/api/trpc/x", { headers: { authorization: "Bearer nope" } }), /refuses header authorization/);
  await assert.rejects(() => s.fetch("/x", {}), /only issues same-origin/);
  assert.equal(f.calls.length, 1, "nothing refused ever reached fetch");
  assert.deepEqual(s.describe(), { kind: "cookie", origin: "(same-origin)" });
  assert.ok(s instanceof Session);
});

test("client.call: GET for a query, decoded per the fixture", async () => {
  const f = scriptedFetch([resOf("query_single_get")]);
  const c = new TrpcClient(new CookieSession({ fetchImpl: f }));
  const r = await c.call("jutsu.get", { id: "abc" });
  assert.equal(f.calls[0].init.method, "GET");
  assert.match(f.calls[0].url, /^\/api\/trpc\/jutsu\.get\?batch=1&input=/);
  assert.equal(r.ok, true); assert.ok(r.data.createdAt instanceof Date);
});

test("client.call: POST for a mutation with a JSON body", async () => {
  const f = scriptedFetch([resOf("mutation_create_ok")]);
  const c = new TrpcClient(new CookieSession({ fetchImpl: f }));
  const r = await c.call("jutsu.create", undefined);
  assert.equal(f.calls[0].init.method, "POST");
  assert.equal(f.calls[0].init.body, fx("mutation_create_ok").exchanges[0].request.body);
  assert.equal(r.data.message, "N3wId0000000000000000");
});

test("client.batch: refuses mixed kinds and unknown paths before any fetch", async () => {
  const f = scriptedFetch([]);
  const c = new TrpcClient(new CookieSession({ fetchImpl: f }));
  await assert.rejects(() => c.batch([{ path: "jutsu.get", input: { id: "a" } }, { path: "jutsu.create" }]), TransportError);
  await assert.rejects(() => c.batch([{ path: "nope.nope" }]), /unknown procedure/);
  assert.equal(f.calls.length, 0);
});

test("client.batch: splits by maxBatch and returns results in input order", async () => {
  const one = (id) => `[{"result":{"data":{"json":{"id":"${id}"}}}}]`;
  const two = (a, b) => `[{"result":{"data":{"json":{"id":"${a}"}}}},{"result":{"data":{"json":{"id":"${b}"}}}}]`;
  const f = scriptedFetch([{ status: 200, body: two("a", "b") }, { status: 200, body: two("c", "d") }, { status: 200, body: one("e") }]);
  const c = new TrpcClient(new CookieSession({ fetchImpl: f }), { maxBatch: 2 });
  const out = await c.batch(["a", "b", "c", "d", "e"].map((id) => ({ path: "jutsu.get", input: { id } })));
  assert.equal(f.calls.length, 3);
  assert.deepEqual(out.map((r) => r.data.id), ["a", "b", "c", "d", "e"]);
  assert.match(f.calls[0].url, /jutsu\.get,jutsu\.get\?batch=1/);
});

test("client.batch: splits a GET whose URL would exceed maxUrlLength", async () => {
  const one = (id) => `[{"result":{"data":{"json":{"id":"${id}"}}}}]`;
  const f = scriptedFetch([{ status: 200, body: one("x") }, { status: 200, body: one("y") }]);
  const c = new TrpcClient(new CookieSession({ fetchImpl: f }), { maxUrlLength: 120 });
  const out = await c.batch([{ path: "jutsu.get", input: { id: "x" } }, { path: "jutsu.get", input: { id: "y" } }]);
  assert.equal(f.calls.length, 2);
  assert.deepEqual(out.map((r) => r.data.id), ["x", "y"]);
});

test("client: a throwing fetch is a NetworkError carrying the paths, and nothing is retried", async () => {
  const f = scriptedFetch([{ throw: new TypeError("Failed to fetch") }]);
  const c = new TrpcClient(new CookieSession({ fetchImpl: f }));
  await assert.rejects(() => c.call("jutsu.create"), (e) => e instanceof NetworkError && e.paths[0] === "jutsu.create" && e.kind === "mutation");
  assert.equal(f.calls.length, 1);
});

test("client: mixed 207 batch decodes per index", async () => {
  const f = scriptedFetch([resOf("query_batched_one_limited_one_ok")]);
  const seen = [];
  const c = new TrpcClient(new CookieSession({ fetchImpl: f }), { onExchange: (r) => seen.push(r) });
  // jutsu.limited is not an audited procedure; use two audited query paths and the recorded body
  const [a, b] = await c.batch([{ path: "jutsu.getAllNames" }, { path: "jutsu.get", input: { id: "fine" } }]);
  assert.equal(a.ok, false); assert.equal(a.error.code, "TOO_MANY_REQUESTS");
  assert.equal(b.ok, true);
  assert.equal(seen.length, 1); assert.equal(seen[0].status, 207); assert.deepEqual(seen[0].outcomes, ["TOO_MANY_REQUESTS", "ok"]);
  assert.ok(!("body" in seen[0]));
});
