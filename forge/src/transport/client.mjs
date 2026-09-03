// The tRPC client. Groups calls into homogeneous batches (queries GET, mutations POST),
// issues them through the Session, decodes per index. No retry logic lives here: a fetch that
// throws is reported as NETWORK, and it is the caller's job to treat that as AMBIGUOUS for a
// mutation (the request may or may not have left the device).

import { buildRequest, decodeResponse, TransportError } from "./envelope.mjs";
import { procedure } from "./procedures.mjs";
import { Session } from "./session.mjs";

export class NetworkError extends Error {
  constructor(cause, info = {}) {
    super("network: " + (cause && cause.message ? cause.message : String(cause)));
    this.name = "NetworkError"; this.cause = cause; Object.assign(this, info);
  }
}

export class TrpcClient {
  /**
   * @param {Session} session
   * @param {object} [opts]
   * @param {number} [opts.maxBatch=20]   items per HTTP request. The route handler has
   *   maxDuration = 90 s per request; batching shares one request scope server-side, but every
   *   procedure still pays its own limiter token, so batching is for latency, not budget.
   * @param {number} [opts.maxUrlLength=8000]  GET batches longer than this are split.
   * @param {(rec: object) => void} [opts.onExchange]  observer for the UI/journal (no secrets).
   */
  constructor(session, { maxBatch = 20, maxUrlLength = 8000, onExchange = null, endpoint } = {}) {
    if (!(session instanceof Session)) throw new TransportError("TrpcClient needs a Session");
    this.session = session;
    this.maxBatch = maxBatch;
    this.maxUrlLength = maxUrlLength;
    this.onExchange = onExchange;
    this.endpoint = endpoint;
  }

  /** One call. Resolves to a decoded element {ok, data} | {ok:false, error}; rejects NetworkError. */
  async call(path, input) {
    const [r] = await this.batch([{ path, input }]);
    return r;
  }

  /**
   * Many calls. All must be the same kind (the adapter cannot mix GET and POST in one request).
   * Returns decoded elements in input order. Splits by maxBatch and by URL length.
   */
  async batch(calls) {
    if (!calls.length) return [];
    const kinds = new Set(calls.map((c) => procedure(c.path).kind));
    if (kinds.size !== 1) throw new TransportError("a batch must be all queries or all mutations");
    const kind = [...kinds][0];
    const out = new Array(calls.length);
    for (const chunk of this._chunks(calls, kind)) {
      const results = await this._send(chunk.map((c) => c.call), kind);
      chunk.forEach((c, j) => { out[c.index] = results[j]; });
    }
    return out;
  }

  *_chunks(calls, kind) {
    const indexed = calls.map((call, index) => ({ call, index }));
    let cur = [];
    for (const c of indexed) {
      cur.push(c);
      const tooMany = cur.length > this.maxBatch;
      const tooLong = kind === "query" && buildRequest(cur.map((x) => x.call), kind, { endpoint: this.endpoint }).url.length > this.maxUrlLength;
      if ((tooMany || tooLong) && cur.length > 1) { cur.pop(); yield cur; cur = [c]; }
    }
    if (cur.length) yield cur;
  }

  async _send(calls, kind) {
    const req = buildRequest(calls, kind, { endpoint: this.endpoint });
    let res, text;
    try {
      res = await this.session.fetch(req.url, { method: req.method, headers: req.headers, body: req.body });
      text = await res.text();
    } catch (e) {
      this._observe({ kind, paths: calls.map((c) => c.path), status: null, error: String(e && e.message) });
      throw new NetworkError(e, { paths: calls.map((c) => c.path), kind });
    }
    const decoded = decodeResponse(res.status, text, calls.length);
    this._observe({ kind, paths: calls.map((c) => c.path), status: res.status,
                    outcomes: decoded.map((d) => (d.ok ? "ok" : d.error.code)) });
    return decoded;
  }

  _observe(rec) { if (this.onExchange) { try { this.onExchange(rec); } catch { /* observer must never break transport */ } } }
}
