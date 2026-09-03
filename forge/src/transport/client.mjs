// The tRPC client. Groups calls into homogeneous batches (queries GET, mutations POST),
// issues them through the Session, decodes per index. No retry logic lives here: a fetch that
// throws is reported as NETWORK, and it is the caller's job to treat that as AMBIGUOUS for a
// mutation (the request may or may not have left the device).

import { buildRequest, decodeResponse, TransportError } from "./envelope.mjs";
import { procedure } from "./procedures.mjs";
import { Session, SessionRefused } from "./session.mjs";

// A fetch that threw. phase "connect": nothing may have left, or it may have (a timeout after
// the request was written is indistinguishable) -> ambiguous for a mutation. phase "body": the
// status arrived, so the request DID reach the server -> the mutation applied or was refused.
export class NetworkError extends Error {
  constructor(cause, info = {}) {
    const name = cause && cause.name ? cause.name + ": " : "";
    super("network: " + name + (cause && cause.message ? cause.message : String(cause)));
    this.name = "NetworkError";
    this.causeName = cause && cause.name ? String(cause.name) : null; // strings only; the journal serialises this
    Object.assign(this, { phase: "connect", httpStatus: null, received: false, results: null }, info);
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
    if (!Number.isInteger(maxBatch) || maxBatch < 1) throw new TransportError("maxBatch must be an integer >= 1");
    if (!Number.isInteger(maxUrlLength) || maxUrlLength < 64) throw new TransportError("maxUrlLength must be an integer >= 64");
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
   *
   * The server runs the elements of one request CONCURRENTLY; never batch calls that depend on
   * each other. The runner sends mutations one per request for exactly that reason.
   *
   * If a later chunk throws, the error carries `results` (what earlier chunks decoded) and
   * `failedIndices`, so a caller never loses ids the server already minted.
   */
  async batch(calls) {
    if (!calls.length) return [];
    const kinds = new Set(calls.map((c) => procedure(c.path).kind));
    if (kinds.size !== 1) throw new TransportError("a batch must be all queries or all mutations");
    const kind = [...kinds][0];
    const out = new Array(calls.length);
    for (const chunk of this._chunks(calls, kind)) {
      let results;
      try { results = await this._send(chunk.map((c) => c.call), kind); }
      catch (e) { e.results = out.slice(); e.failedIndices = chunk.map((c) => c.index); throw e; }
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
      if (tooLong && cur.length === 1) throw new TransportError(`single call to ${c.call.path} exceeds maxUrlLength ${this.maxUrlLength}`, { paths: [c.call.path], sent: false });
      if ((tooMany || tooLong) && cur.length > 1) { cur.pop(); yield cur; cur = [c]; }
    }
    if (cur.length) yield cur;
  }

  async _send(calls, kind) {
    const req = buildRequest(calls, kind, { endpoint: this.endpoint });
    const paths = calls.map((c) => c.path);
    let res;
    try {
      res = await this.session.fetch(req.url, { method: req.method, headers: req.headers, body: req.body });
    } catch (e) {
      this._observe({ kind, paths, status: null, error: String(e && e.message) });
      if (e instanceof SessionRefused) throw new TransportError("not sent: " + e.message, { paths, kind, sent: false });
      throw new NetworkError(e, { paths, kind, phase: "connect" });
    }
    let text;
    try { text = await res.text(); }
    catch (e) {
      this._observe({ kind, paths, status: res.status, error: "body: " + String(e && e.message) });
      throw new NetworkError(e, { paths, kind, phase: "body", httpStatus: res.status, received: true });
    }
    let decoded;
    try { decoded = decodeResponse(res.status, text, calls.length); }
    catch (e) {
      // a response arrived but is not the audited shape: an HTML login/challenge page, a proxy
      // 502, a truncated body. For a mutation this is AMBIGUOUS (the request reached something).
      const ct = res.headers && res.headers.get ? res.headers.get("content-type") : null;
      Object.assign(e, { paths, kind, received: true, httpStatus: res.status, redirected: !!res.redirected, url: res.url ?? null, contentType: ct,
                         looksLikeLogin: !!(ct && /text\/html/i.test(ct)) });
      this._observe({ kind, paths, status: res.status, error: e.message, contentType: ct, redirected: !!res.redirected });
      throw e;
    }
    this._observe({ kind, paths, status: res.status, outcomes: decoded.map((d) => (d.ok ? "ok" : d.error.code)) });
    return decoded;
  }

  _observe(rec) { if (this.onExchange) { try { this.onExchange(rec); } catch { /* observer must never break transport */ } } }
}
