// Every assertion here is against test/fixtures/envelope/*.json, which were produced by running
// the real @trpc/client 11.18.0 against the real @trpc/server 11.18.0 fetch adapter with
// superjson 2.2.6 (tools/derive_envelope.mjs). If buildRequest does not reproduce the recorded
// request byte for byte, this module is wrong, not the fixture.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { buildRequest, decodeResponse, encodeInput, TransportError } from "../src/transport/envelope.mjs";
import { readMutation, readCreate, classifyError, NANOID_RE, OutcomeError } from "../src/transport/outcome.mjs";

const DIR = join(dirname(fileURLToPath(import.meta.url)), "fixtures", "envelope");
const fx = (name) => JSON.parse(readFileSync(join(DIR, name + ".json"), "utf8"));
const pathAndQuery = (u) => u.replace(/^https?:\/\/[^/]+/, "");
const tagDates = (v) => v instanceof Date ? { __date: v.toISOString() }
  : Array.isArray(v) ? v.map(tagDates)
  : v && typeof v === "object" ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, tagDates(x)])) : v;

// The inputs each scenario was recorded with. Kept here, not in the fixture, so the test is an
// independent re-derivation rather than a copy.
const INPUTS = {
  query_single_get: { kind: "query", calls: [{ path: "jutsu.get", input: { id: "abc" } }] },
  query_batched_two: { kind: "query", calls: [{ path: "jutsu.get", input: { id: "a1" } }, { path: "jutsu.getAllNames", input: undefined }] },
  mutation_create_ok: { kind: "mutation", calls: [{ path: "jutsu.create", input: undefined }] },
  mutation_create_role_miss: { kind: "mutation", calls: [{ path: "jutsu.createRoleMiss", input: undefined }] },
  mutation_update_ok: { kind: "mutation", calls: [{ path: "jutsu.update", input: { id: "abc", data: { name: "Renamed", power: 150 } } }] },
  mutation_update_zod_fail: { kind: "mutation", calls: [{ path: "jutsu.update", input: { id: "abc", data: { name: "x", power: -1 } } }] },
  mutation_batched_create_and_update: { kind: "mutation", calls: [{ path: "jutsu.create", input: undefined }, { path: "jutsu.update", input: { id: "zz", data: { name: "N", power: 1 } } }] },
  mutation_batched_mixed_ok_and_zod_fail: { kind: "mutation", calls: [{ path: "jutsu.update", input: { id: "ok1", data: { name: "N", power: 1 } } }, { path: "jutsu.update", input: { id: "bad", data: { name: "x", power: -1 } } }] },
  query_too_many_requests: { kind: "query", calls: [{ path: "jutsu.limited", input: undefined }] },
  query_batched_one_limited_one_ok: { kind: "query", calls: [{ path: "jutsu.limited", input: undefined }, { path: "jutsu.get", input: { id: "fine" } }] },
};

test("fixture set is complete", () => {
  const names = readdirSync(DIR).filter((f) => f.endsWith(".json")).map((f) => f.slice(0, -5));
  for (const n of Object.keys(INPUTS)) assert.ok(names.includes(n), "missing fixture " + n);
});

for (const [name, spec] of Object.entries(INPUTS)) {
  test(`buildRequest reproduces the real client's request byte for byte: ${name}`, () => {
    const f = fx(name);
    const rec = f.exchanges[0].request;
    const mine = buildRequest(spec.calls, spec.kind);
    assert.equal(mine.method, rec.method);
    assert.equal(mine.url, pathAndQuery(rec.url));
    if (spec.kind === "mutation") {
      assert.equal(mine.body, rec.body);
      const ct = rec.headers["content-type"];
      if (ct) assert.equal(mine.headers["content-type"], ct);
    } else {
      assert.equal(mine.body, null);
    }
  });

  test(`decodeResponse matches what the real client decoded: ${name}`, () => {
    const f = fx(name);
    const res = f.exchanges[0].response;
    const out = decodeResponse(res.status, res.body, spec.calls.length);
    assert.equal(out.length, spec.calls.length);
    if (f.error) {
      // single call that threw client-side: our element must be an error with the same code
      assert.equal(out[0].ok, false);
      assert.equal(out[0].error.code, f.error.code);
      assert.equal(out[0].error.httpStatus, f.error.httpStatus);
      assert.deepEqual(out[0].error.zodError, f.error.zodError);
    } else if (spec.calls.length === 1) {
      assert.equal(out[0].ok, true);
      assert.deepEqual(tagDates(out[0].data), f.decoded);
    } else if (name.includes("mixed") || name.includes("one_limited")) {
      // Promise.allSettled shape in the fixture: [{status, value|reason}]
      f.decoded.forEach((settled, i) => {
        if (settled.status === "fulfilled") { assert.equal(out[i].ok, true); assert.deepEqual(tagDates(out[i].data), settled.value); }
        else { assert.equal(out[i].ok, false); }
      });
    } else {
      out.forEach((el, i) => { assert.equal(el.ok, true); assert.deepEqual(tagDates(el.data), f.decoded[i]); });
    }
  });
}

test("undefined input serialises exactly as the adapter does", () => {
  assert.deepEqual(encodeInput(undefined), { json: null, meta: { values: ["undefined"], v: 1 } });
  assert.deepEqual(encodeInput({ id: "x" }), { json: { id: "x" } });
});

test("Dates come back as Date instances, nulls stay null (the superjson round-trip)", () => {
  const f = fx("query_single_get");
  const [el] = decodeResponse(200, f.exchanges[0].response.body, 1);
  assert.ok(el.data.createdAt instanceof Date);
  assert.equal(el.data.createdAt.toISOString(), "2026-09-01T04:02:38.440Z");
  assert.equal(el.data.bloodlineId, null);
  assert.equal(el.data.effects[0].power, 150);
});

test("mixed batch is 207 and the verdict is per index, never the status", () => {
  const f = fx("mutation_batched_mixed_ok_and_zod_fail");
  const res = f.exchanges[0].response;
  assert.equal(res.status, 207);
  const [a, b] = decodeResponse(res.status, res.body, 2);
  assert.equal(a.ok, true); assert.equal(a.data.success, true);
  assert.equal(b.ok, false); assert.equal(b.error.code, "BAD_REQUEST"); assert.equal(b.error.httpStatus, 400);
  assert.ok(Array.isArray(b.error.zodError) && b.error.zodError.length === 1);
  assert.deepEqual(b.error.zodError[0].path, ["data", "power"]);
  assert.equal(b.error.path, "jutsu.update");
});

test("a 429 hides inside a 207: one limited element, one fine", () => {
  const f = fx("query_batched_one_limited_one_ok");
  const res = f.exchanges[0].response;
  assert.equal(res.status, 207);
  const [lim, ok] = decodeResponse(res.status, res.body, 2);
  assert.equal(lim.ok, false); assert.equal(lim.error.code, "TOO_MANY_REQUESTS"); assert.equal(lim.error.httpStatus, 429);
  assert.equal(lim.error.path, "jutsu.limited");
  assert.equal(classifyError(lim.error), "RATE_LIMITED");
  assert.equal(ok.ok, true); assert.equal(ok.data.id, "fine");
});

test("GET on a mutation path is refused by the adapter before any resolver runs", () => {
  const f = fx("get_on_mutation_path_rejected");
  const res = f.exchanges[0].response;
  assert.equal(res.status, 405);
  const [el] = decodeResponse(res.status, res.body, 1);
  assert.equal(el.error.code, "METHOD_NOT_SUPPORTED");
  assert.equal(classifyError(el.error), "CLIENT_BUG");
});

test("decodeResponse refuses non-JSON, non-array, and length mismatch loudly", () => {
  assert.throws(() => decodeResponse(200, "<html>", 1), TransportError);
  assert.throws(() => decodeResponse(200, '{"result":{}}', 1), TransportError);
  assert.throws(() => decodeResponse(200, "[]", 1), /length mismatch/);
  assert.throws(() => decodeResponse(200, "[{}]", 1), /neither result nor error/);
});

test("outcome: success:true with an id, success:false as refused, error element as error", () => {
  const ok = readMutation(decodeResponse(200, fx("mutation_create_ok").exchanges[0].response.body, 1)[0]);
  assert.equal(ok.kind, "ok"); assert.equal(ok.id, "N3wId0000000000000000"); assert.ok(NANOID_RE.test(ok.id));
  const refused = readMutation(decodeResponse(200, fx("mutation_create_role_miss").exchanges[0].response.body, 1)[0]);
  assert.equal(refused.kind, "refused"); assert.match(refused.message, /Not allowed/);
  const err = readMutation(decodeResponse(400, fx("mutation_update_zod_fail").exchanges[0].response.body, 1)[0]);
  assert.equal(err.kind, "error"); assert.equal(classifyError(err.error), "VALIDATION");
});

test("readCreate: success:true whose message is not an id is a contract break, not a success", () => {
  const upd = decodeResponse(200, fx("mutation_update_ok").exchanges[0].response.body, 1)[0]; // message "Updated abc"
  assert.throws(() => readCreate(upd), OutcomeError);
  assert.equal(readMutation(upd).kind, "ok"); // as an update it is fine
  assert.equal(readMutation(upd).id, undefined);
});

test("readMutation refuses a query-shaped body as a mutation outcome", () => {
  const q = decodeResponse(200, fx("query_single_get").exchanges[0].response.body, 1)[0];
  assert.throws(() => readMutation(q), OutcomeError);
});
