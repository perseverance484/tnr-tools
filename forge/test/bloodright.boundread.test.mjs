// push/122 re-preview (2026-10-19): one bound-skill read answered an error page ("response is not
// JSON") and stopped a whole tree. Reads change nothing, so they are batched and retried.
import test from "node:test";
import assert from "node:assert/strict";
import { readBoundSkills, BOUND_READ_RETRY_MS } from "../src/bloodright/compiler.mjs";
import { TransportError } from "../src/transport/envelope.mjs";

const rec = (id) => ({ ok: true, data: { id, name: id } });

test("a read that hits an error page is retried after a pause, in one batch", async () => {
  const calls = [], slept = [];
  let first = true;
  const reader = { getMany: async (path, ids) => { calls.push(ids.length); if (first) { first = false; throw new TransportError("response is not JSON (HTTP 502)"); } return ids.map(rec); } };
  const found = await readBoundSkills(reader, ["a", "b", "c"], { sleep: async (ms) => slept.push(ms) });
  assert.deepEqual([...found.keys()], ["a", "b", "c"]);
  assert.deepEqual(calls, [3, 3]);
  assert.deepEqual(slept, [BOUND_READ_RETRY_MS[0]]);
});

test("only the records that failed are asked again", async () => {
  const calls = [];
  const reader = { getMany: async (path, ids) => { calls.push([...ids]); return ids.map((id) => (id === "b" && calls.length === 1 ? { ok: false, error: { message: "boom" } } : rec(id))); } };
  const found = await readBoundSkills(reader, ["a", "b"], { sleep: async () => {} });
  assert.equal(found.size, 2);
  assert.deepEqual(calls, [["a", "b"], ["b"]]);
});

test("a read that keeps failing is reported with its reason; a rate-limit trip is never retried", async () => {
  const always = { getMany: async () => { throw new TransportError("response is not JSON (HTTP 503)"); } };
  await assert.rejects(readBoundSkills(always, ["a"], { sleep: async () => {} }), /bound skill a is unreadable: response is not JSON \(HTTP 503\)/);
  const limited = { getMany: async () => { const e = new Error("TOO_MANY_REQUESTS"); e.name = "RateLimited"; throw e; } };
  let slept = 0;
  await assert.rejects(readBoundSkills(limited, ["a"], { sleep: async () => slept++ }), /TOO_MANY_REQUESTS/);
  assert.equal(slept, 0);
});
