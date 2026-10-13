// node --test harness/crafting_recipe_census/census_script.test.mjs
// Socket-free: the census is handed an in-process fake fetch and a virtual clock.
import test from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { seedWorld, fakeFetch, fakeEnv, err } from "./fake_server.mjs";

const require = createRequire(import.meta.url);
const C = require("./crafting_recipe_census.console.js");
const OPTS = { limit: 3 };

async function fullRun(fetchOpts = {}, runOpts = OPTS) {
  const world = seedWorld();
  const ff = fakeFetch(world, fetchOpts);
  const fe = fakeEnv(ff.fetch);
  const census = C.create(fe.env);
  const summary = await census.run(runOpts);
  return { world, ff, fe, census, summary, state: await census.snapshot() };
}

const craftableIds = (world, hidden) =>
  world.items.filter((r) => r.canBeCrafted && r.hidden === hidden).map((r) => r.id).sort();
const passIds = (state, which, key) =>
  state.lists[which][key].pages.flatMap((p) => p.rows.map((r) => r.id)).sort();
const comparable = (s) => ({
  lists: Object.fromEntries(
    ["main", "confirm"].map((w) => [w, Object.fromEntries(
      Object.entries(s.lists[w]).map(([k, v]) => [k, v.pages.map((p) => ({ c: p.cursor, n: p.nextCursor, rows: p.rows }))]),
    )]),
  ),
  detailIds: s.detailIds,
  details: Object.fromEntries(Object.entries(s.details).map(([k, v]) => [k, { status: v.status, data: v.data }])),
});

test("complete run pages both hidden states to nextCursor null and reads every id", async () => {
  const { world, ff, state, summary } = await fullRun();
  assert.equal(summary.status, "complete");
  for (const [key, hidden] of [["hidden=false", false], ["hidden=true", true]]) {
    assert.deepEqual(passIds(state, "main", key), craftableIds(world, hidden));
    assert.deepEqual(passIds(state, "confirm", key), craftableIds(world, hidden));
    const pages = state.lists.main[key].pages;
    assert.deepEqual(pages.map((p) => p.cursor), pages.map((_, i) => i));
    assert.equal(pages.at(-1).nextCursor, null);
  }
  // 8 visible at limit 3 -> pages 3,3,2. 3 hidden -> 3 then an empty terminal page.
  assert.deepEqual(state.lists.main["hidden=false"].pages.map((p) => p.rows.length), [3, 3, 2]);
  assert.deepEqual(state.lists.main["hidden=true"].pages.map((p) => p.rows.length), [3, 0]);
  // the negative-cost craftable is only reachable because min*Cost is widened
  assert.ok(passIds(state, "main", "hidden=false").includes("c-neg"));
  const all = [...craftableIds(world, false), ...craftableIds(world, true)].sort();
  assert.deepEqual(state.detailIds, all);
  assert.deepEqual(Object.keys(state.details).sort(), all);
  assert.ok(Object.values(state.details).every((d) => d.status === "ok"));
  assert.equal(ff.calls.length, 5 + all.length + 5);
  assert.equal(state.seq, ff.calls.length);
});

test("every request is an anonymous same-origin GET to an allowed procedure", async () => {
  const { ff } = await fullRun();
  for (const { url, init } of ff.calls) {
    const u = new URL(url);
    assert.equal(u.origin, "https://www.theninja-rpg.com");
    assert.equal(init.method, "GET");
    assert.equal(init.credentials, "omit");
    assert.equal(init.body, undefined);
    assert.ok(!("cookie" in (init.headers || {})) && !("authorization" in (init.headers || {})));
    const proc = u.pathname.replace("/api/trpc/", "");
    assert.ok(C.ALLOWED_PROCS.includes(proc), proc);
    assert.ok(!proc.includes(","), "one procedure per request");
    const input = JSON.parse(u.searchParams.get("input"))["0"].json;
    if (proc === "item.getAll") {
      assert.equal(input.canBeCrafted, true);
      assert.equal(typeof input.hidden, "boolean");
      assert.equal(input.minCost, C.INT32_MIN);
    }
  }
});

test("throttle: consecutive requests are at least throttleMs apart", async () => {
  const { state } = await fullRun({}, { limit: 3, throttleMs: 1500 });
  const at = state.requestLog.map((r) => r.at);
  for (let i = 1; i < at.length; i++) assert.ok(at[i] - at[i - 1] >= 1500, `gap ${i}`);
});

test("rate limit halts at once, never retries, and resumes to an identical capture", async () => {
  const baseline = (await fullRun()).state;
  const world = seedWorld();
  const ff = fakeFetch(world, { faults: { 9: err("TOO_MANY_REQUESTS", 429, "You are acting too fast") } });
  const fe = fakeEnv(ff.fetch);
  const s1 = await C.create(fe.env).run(OPTS);
  assert.equal(s1.status, "halted");
  assert.equal(s1.lastHalt.reason, "RATE_LIMIT");
  assert.equal(ff.calls.length, 9, "no retry after 429");
  const haltedState = fe.mem.get(C.STATE_KEY);
  assert.ok(haltedState.notBefore >= fe.env.now() + 60000);

  // A fresh instance (page reload + re-paste) over the same store resumes.
  const s2 = await C.create(fe.env).run();
  assert.equal(s2.status, "complete");
  const resumed = fe.mem.get(C.STATE_KEY);
  assert.ok(resumed.requestLog[9].at >= haltedState.notBefore, "waited out the cooldown");
  assert.deepEqual(comparable(resumed), comparable(baseline));
  assert.equal(ff.calls.length, baseline.seq + 1, "only the rejected request was repeated");
});

test("auth and contract errors halt without retry", async () => {
  for (const [fault, reason] of [
    [err("UNAUTHORIZED", 401, "no"), "AUTH"],
    [err("FORBIDDEN", 403, "no"), "AUTH"],
    [err("BAD_REQUEST", 400, "bad input"), "CONTRACT"],
    [{ status: 429, body: "Too Many Requests" }, "RATE_LIMIT"],
  ]) {
    const { ff, summary } = await fullRun({ faults: { 2: fault } });
    assert.equal(summary.status, "halted");
    assert.equal(summary.lastHalt.reason, reason);
    assert.equal(ff.calls.length, 2);
  }
});

test("transient errors retry with backoff, then halt when exhausted", async () => {
  const flaky = await fullRun({ faults: { 3: err("INTERNAL_SERVER_ERROR", 500, "boom"), 4: "network" } });
  assert.equal(flaky.summary.status, "complete");
  const baseline = (await fullRun()).state;
  assert.deepEqual(comparable(flaky.state), comparable(baseline));

  const dead = await fullRun({ faults: { 3: "network", 4: "network", 5: "network", 6: "network" } });
  assert.equal(dead.summary.status, "halted");
  assert.equal(dead.summary.lastHalt.reason, "TRANSIENT_EXHAUSTED");
  assert.equal(dead.ff.calls.length, 6);
});

test("an item deleted between list and detail is recorded as not_found", async () => {
  const { state, summary } = await fullRun({
    onRequest: (n, world) => {
      if (n === 6) world.items = world.items.filter((r) => r.id !== "c-tonic");
    },
  });
  assert.equal(summary.status, "complete");
  assert.equal(state.details["c-tonic"].status, "not_found");
  assert.ok(!passIds(state, "confirm", "hidden=false").includes("c-tonic"));
});

test("stop() halts between requests and run() resumes", async () => {
  const world = seedWorld();
  const ff = fakeFetch(world);
  const fe = fakeEnv(ff.fetch);
  const census = C.create(fe.env);
  const origFetch = fe.env.fetch;
  fe.env.fetch = async (...a) => {
    if (ff.calls.length === 4) census.stop();
    return origFetch(...a);
  };
  const s1 = await census.run(OPTS);
  assert.equal(s1.status, "halted");
  assert.equal(s1.lastHalt.reason, "STOPPED");
  const s2 = await census.run();
  assert.equal(s2.status, "complete");
  assert.deepEqual(comparable(await census.snapshot()), comparable((await fullRun()).state));
});

test("guards: wrong host, throttle floor, limit range, unknown option, options on resume", async () => {
  const ff = fakeFetch(seedWorld());
  await assert.rejects(C.create(fakeEnv(ff.fetch, { hostname: "evil.example" }).env).run(), /theninja-rpg\.com/);
  await assert.rejects(C.create(fakeEnv(ff.fetch).env).run({ throttleMs: 500 }), /throttleMs/);
  await assert.rejects(C.create(fakeEnv(ff.fetch).env).run({ limit: 501 }), /limit/);
  await assert.rejects(C.create(fakeEnv(ff.fetch).env).run({ hidden: true }), /unknown option/);
  assert.equal(ff.calls.length, 0);
  const fe = fakeEnv(fakeFetch(seedWorld(), { faults: { 2: err("FORBIDDEN", 403, "x") } }).fetch);
  await C.create(fe.env).run(OPTS);
  await assert.rejects(C.create(fe.env).run({ limit: 5 }), /fresh census/);
});

test("download names the file by start time and status; reset clears state", async () => {
  const { census, fe } = await fullRun();
  const name = await census.download();
  assert.match(name, /^tnr_crafting_census_raw_\d+_complete\.json$/);
  const parsed = JSON.parse(fe.downloads[0].text);
  assert.equal(parsed.schema, C.SCHEMA);
  assert.equal(parsed.sourcePin, C.SOURCE_PIN);
  await census.reset();
  assert.equal(fe.mem.size, 0);
});

test("classify reads superjson batch success and error envelopes", () => {
  assert.deepEqual(C.classify(200, JSON.stringify([{ result: { data: { json: { a: 1 } } } }])), { data: { a: 1 } });
  assert.ok(C.classify(404, JSON.stringify([{ error: { json: { message: "Item not found", data: { code: "NOT_FOUND", httpStatus: 404 } } } }])).notFound);
  assert.ok(C.classify(502, "<html>").retry);
  assert.ok(C.classify(200, JSON.stringify([{}])).retry);
  assert.throws(() => C.classify(429, "slow down"), /RATE_LIMIT/);
});
