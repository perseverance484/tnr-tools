// tRPC 11 fetch-adapter wire format, with superjson. Every shape in this file was DERIVED by
// running the real @trpc/client 11.18.0 against the real @trpc/server 11.18.0 fetch adapter
// (tools/derive_envelope.mjs); the recorded exchanges are test/fixtures/envelope/*.json and the
// tests assert this module against them. Nothing here comes from builder_bundle.js.
//
// Request
//   query     GET  /api/trpc/<p0>,<p1>?batch=1&input=<urlencoded {"0":<sj>,"1":<sj>}>
//   mutation  POST /api/trpc/<p0>,<p1>?batch=1   body {"0":<sj>,"1":<sj>}  content-type: application/json
//   where <sj> is superjson.serialize(input): {json, meta?}. An undefined input serialises as
//   {"json":null,"meta":{"values":["undefined"],"v":1}}.
// Response: always a JSON array, one element per batch index, even for a single call.
//   ok    {"result":{"data":{json, meta?}}}
//   error {"error":{json:{message, code:<jsonrpc int>, data:{code, httpStatus, stack?, zodError}}, meta?}}
//   HTTP status rule, observed: a single-element batch carries that element's status (200, 400,
//   405, 429); a multi-element batch with any mix of outcomes is 207. So a 207 can hide a 429
//   at one index while another index succeeded (query_batched_one_limited_one_ok.json). Outcome
//   is therefore read per index and the status is never consulted for a verdict.

import superjson from "superjson";

export const ENDPOINT = "/api/trpc";

export class TransportError extends Error {
  constructor(message, info = {}) { super(message); this.name = "TransportError"; Object.assign(this, info); }
}

/** superjson-encode one input. Returns the {json, meta?} object the adapter puts at each index. */
export function encodeInput(input) {
  const { json, meta } = superjson.serialize(input);
  return meta ? { json, meta } : { json };
}

/**
 * Build one HTTP request for a homogeneous batch.
 * @param {Array<{path: string, input: any}>} calls
 * @param {"query"|"mutation"} kind
 */
export function buildRequest(calls, kind, { endpoint = ENDPOINT } = {}) {
  if (!Array.isArray(calls) || calls.length === 0) throw new TransportError("empty batch");
  const paths = calls.map((c) => c.path).join(",");
  const envelope = {};
  calls.forEach((c, i) => { envelope[String(i)] = encodeInput(c.input); });
  if (kind === "query") {
    const input = encodeURIComponent(JSON.stringify(envelope));
    return { method: "GET", url: `${endpoint}/${paths}?batch=1&input=${input}`, headers: {}, body: null };
  }
  if (kind === "mutation") {
    return {
      method: "POST", url: `${endpoint}/${paths}?batch=1`,
      headers: { "content-type": "application/json" }, body: JSON.stringify(envelope),
    };
  }
  throw new TransportError("unknown kind: " + kind);
}

/**
 * Decode a response body into per-index outcomes.
 * @returns {Array<{ok: true, data: any} | {ok: false, error: DecodedError}>}
 * DecodedError = { code: string, httpStatus: number|null, message: string, path: string|null, zodError: array|null, raw: object }
 */
export function decodeResponse(status, text, expectedCount) {
  let body;
  try { body = JSON.parse(text); } catch (e) {
    throw new TransportError("response is not JSON", { httpStatus: status, snippet: String(text).slice(0, 200) });
  }
  if (!Array.isArray(body)) {
    // A non-batched shape would mean the server is not the one we audited, or an intermediary
    // answered. Surface loudly; never guess.
    throw new TransportError("response is not a batch array", { httpStatus: status, snippet: String(text).slice(0, 200) });
  }
  if (expectedCount != null && body.length !== expectedCount) {
    throw new TransportError(`batch length mismatch: expected ${expectedCount}, got ${body.length}`, { httpStatus: status });
  }
  return body.map((el, i) => decodeElement(el, i, status));
}

function decodeElement(el, i, status) {
  if (el && el.result && el.result.data !== undefined) {
    const { json, meta } = el.result.data;
    return { ok: true, data: superjson.deserialize({ json, meta }) };
  }
  if (el && el.error) {
    const err = el.error.json !== undefined ? superjson.deserialize({ json: el.error.json, meta: el.error.meta }) : el.error;
    const data = (err && err.data) || {};
    return {
      ok: false,
      error: {
        code: data.code ?? "UNKNOWN",
        httpStatus: data.httpStatus ?? null,
        message: (err && err.message) ?? "",
        path: data.path ?? null,
        zodError: Array.isArray(data.zodError) ? data.zodError : null,
        raw: err,
      },
    };
  }
  throw new TransportError(`batch element ${i} is neither result nor error`, { httpStatus: status, element: el });
}
