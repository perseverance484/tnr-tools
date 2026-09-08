// The budget (spec section 6). Mirrors the server's limiter locally so the client never
// trips it, because a trip is a penalty, not a retry signal.
//
// Server facts, from app/src/server/api/trpc.ts at 345d18ac:
//   Ratelimit.slidingWindow(60, "60 s")             (:123)
//   identifier = `${path}-${context.userId ?? context.userIp}`   (:148)
//   on trip: movedTooFastCount + 1, money * 0.99, bank * 0.99, throw TOO_MANY_REQUESTS (:166-179)
//   applied to publicProcedure only (:211); protectedProcedure carries none (:230)
//
// The local mirror computes the SAME estimate the server does. @upstash/ratelimit 2.0.8
// (the game's pin) slidingWindowLimitScript: buckets are floor(now / window); at a request,
//   prev = floor((1 - (now % window) / window) * count(previous bucket))
//   reject if prev + count(current bucket) >= limit
// A strict 60 s window is NOT this: it lets a client that sent 30 early in one bucket send 30
// more early in the next, which the server weights to ~59 (adversarial L3). So acquire() holds a
// request until BOTH the strict window and the weighted estimate fit under the allowance; the
// strict check is kept because the estimate depends on the client and server clocks agreeing on
// the bucket boundary (NTP keeps that within a second; a skewed clock is the residual risk).
//
// Why a MARGIN below 60 at all: the window is per (path, user), shared with every other tab the
// user has open on the game, whose pages call the same publicProcedure reads on mount. The
// client cannot see that traffic; half the window is left for it.
// The send log is written to localStorage BEFORE a request leaves (write-ahead, same reason
// as the journal): an in-memory bucket resets on tab eviction and would overspend the same
// server window on restart.

import { LIMITED_PATHS } from "../transport/procedures.mjs";

export const SENDLOG_KEY = "tnr_forge_sendlog_v1";
export const SERVER_LIMIT = 60;
export const SERVER_WINDOW_MS = 60_000;
export const DEFAULT_MARGIN = 0.5; // allowance = floor(60 * 0.5) = 30 per path per minute

export class RateLimited extends Error {
  constructor({ path, until, index = null, message }) {
    super(message || `TOO_MANY_REQUESTS on ${path}`);
    this.name = "RateLimited"; this.path = path; this.until = until; this.index = index;
  }
}

export class SendLog {
  constructor(storage, clock) { this.storage = storage; this.clock = clock; }
  _load() {
    try { return JSON.parse(this.storage.getItem(SENDLOG_KEY) || "{}") || {}; } catch { return {}; }
  }
  _save(log) { this.storage.setItem(SENDLOG_KEY, JSON.stringify(log)); }
  // timestamps are kept for two windows: the previous bucket still weighs on the estimate
  _prune(arr, windowMs, now) { return arr.filter((t) => now - t < 2 * windowMs); }

  /** Timestamps within the strict window for a path, oldest first. */
  inWindow(path, windowMs) {
    const now = this.clock();
    return this._prune(this._load()[path] || [], windowMs, now).filter((t) => now - t < windowMs).sort((a, b) => a - b);
  }

  /** All retained timestamps (two windows) for a path. */
  recent(path, windowMs) {
    const now = this.clock();
    return this._prune(this._load()[path] || [], windowMs, now);
  }

  /** Append n sends for path, prune, flush synchronously. Returns the count in the strict window after. */
  record(path, n, windowMs) {
    const now = this.clock();
    const log = this._load();
    const arr = this._prune(log[path] || [], windowMs, now);
    for (let i = 0; i < n; i++) arr.push(now);
    log[path] = arr;
    this._save(log);
    return arr.filter((t) => now - t < windowMs).length;
  }

  /** Persisted trip marker so a restart within the window still shows the countdown. */
  trip(path, until) {
    const log = this._load();
    log.__tripped = { path, until };
    this._save(log);
  }
  tripped() {
    const t = this._load().__tripped;
    if (!t) return null;
    if (this.clock() >= t.until) return null;
    return t;
  }
  clearTrip() { const log = this._load(); delete log.__tripped; this._save(log); }
}

export class Budget {
  /**
   * @param {object} o
   * @param {Storage} o.storage
   * @param {() => number} [o.clock]
   * @param {(ms: number) => Promise<void>} [o.sleep]
   * @param {number} [o.margin]  fraction of the server limit to allow locally (0 < margin <= 1)
   * @param {string[]} [o.limitedPaths]
   */
  constructor({ storage, clock = () => Date.now(), sleep = (ms) => new Promise((r) => setTimeout(r, ms)),
                limit = SERVER_LIMIT, windowMs = SERVER_WINDOW_MS, margin = DEFAULT_MARGIN,
                limitedPaths = LIMITED_PATHS } = {}) {
    if (!(margin > 0 && margin <= 1)) throw new Error("margin must be in (0, 1]");
    this.log = new SendLog(storage, clock);
    this.clock = clock; this.sleep = sleep;
    this.limit = limit; this.windowMs = windowMs; this.margin = margin;
    this.limited = new Set(limitedPaths);
    this.waits = 0; // observability: how often the throttle held a request
  }

  get allowance() { return Math.max(1, Math.floor(this.limit * this.margin)); }
  isLimited(path) { return this.limited.has(path); }

  /**
   * The server's own estimate for path at `now`, computed the way slidingWindowLimitScript does,
   * from this client's sends alone. {prev, cur, weighted, strict, bucketStart}
   */
  estimate(path, now = this.clock()) {
    const w = this.windowMs;
    const bucket = Math.floor(now / w);
    let prev = 0, cur = 0, strict = 0;
    for (const t of this.log.recent(path, w)) {
      const b = Math.floor(t / w);
      if (b === bucket) cur++; else if (b === bucket - 1) prev++;
      if (now - t < w) strict++;
    }
    const frac = (now % w) / w;
    const weighted = Math.floor((1 - frac) * prev) + cur;
    return { prev, cur, weighted, strict, bucketStart: bucket * w, used: Math.max(weighted, strict) };
  }

  /** How many more sends on path fit right now without waiting. */
  available(path) {
    if (!this.isLimited(path)) return Infinity;
    return Math.max(0, this.allowance - this.estimate(path).used);
  }

  /** Earliest time at which n more sends fit under BOTH checks, assuming no other sends. */
  _wakeAt(path, n, now) {
    const w = this.windowMs, a = this.allowance;
    const est = this.estimate(path, now);
    if (est.used + n <= a) return now;
    // strict: enough of the oldest in-window timestamps must age out
    let strictWake = now;
    const inWin = this.log.inWindow(path, w);
    if (inWin.length + n > a) strictWake = inWin[inWin.length + n - a - 1] + w;
    // weighted: within this bucket the previous bucket's weight decays; failing that, the next
    // bucket, where the current count becomes the (decaying) previous one
    let weightedWake = now;
    if (est.weighted + n > a) {
      const need = a - n; // floor((1-f)*prev) + cur must be <= need
      let inThis = Infinity;
      if (est.cur <= need && est.prev > 0) {
        // floor((1-f)*prev) <= need - cur  <=>  (1-f)*prev < need - cur + 1
        const f = 1 - (need - est.cur + 1) / est.prev;
        inThis = est.bucketStart + Math.ceil(f * w) + 1;
      }
      const nextStart = est.bucketStart + w;
      let inNext = nextStart + 1;
      if (est.cur > need) { const f = 1 - (need + 1) / est.cur; inNext = nextStart + Math.ceil(f * w) + 1; }
      weightedWake = inThis > now && inThis < nextStart ? inThis : inNext;
    }
    return Math.max(strictWake, weightedWake, now + 1);
  }

  /**
   * Acquire n tokens for path. Waits (never fails) until the local window has room, then records
   * the sends WRITE-AHEAD and resolves. Unlimited paths resolve immediately and record nothing.
   * A persisted trip (server 429 within the window) refuses with RateLimited: the caller must
   * not send at all until `until`.
   */
  async acquire(path, n = 1) {
    if (!this.isLimited(path)) return;
    if (n > this.allowance) throw new Error(`cannot acquire ${n} > allowance ${this.allowance} on ${path}; chunk smaller`);
    const t = this.log.tripped();
    if (t) throw new RateLimited({ path: t.path, until: t.until, message: `limiter tripped on ${t.path}; wait until ${new Date(t.until).toISOString()}` });
    for (let guard = 0; guard < 1000; guard++) {
      const now = this.clock();
      const wakeAt = this._wakeAt(path, n, now);
      if (wakeAt <= now) break;
      this.waits++;
      await this.sleep(Math.max(1, wakeAt - now));
    }
    this.log.record(path, n, this.windowMs);
  }

  /**
   * Inspect decoded batch results. If ANY index is TOO_MANY_REQUESTS, persist the trip and
   * throw RateLimited for that index. Never retries. Call this AFTER caching any ok results,
   * so the successful indices are not wasted.
   */
  observe(results, paths) {
    for (let i = 0; i < results.length; i++) {
      const r = results[i];
      if (r && r.ok === false && r.error && r.error.code === "TOO_MANY_REQUESTS") {
        const path = r.error.path || paths[i];
        // the server keeps counting this bucket at full weight until it ends, then decays it over
        // the next one; the count from this client is provably clear at the end of the NEXT bucket
        const until = (Math.floor(this.clock() / this.windowMs) + 2) * this.windowMs;
        this.log.trip(path, until);
        throw new RateLimited({ path, until, index: i, message: r.error.message });
      }
    }
  }

  /** Live view for the Run screen. */
  status() {
    const now = this.clock();
    const out = {};
    for (const path of this.limited) {
      const inWin = this.log.inWindow(path, this.windowMs);
      const est = this.estimate(path, now);
      out[path] = {
        used: est.used, strict: inWin.length, weighted: est.weighted, allowance: this.allowance, serverLimit: this.limit,
        resetInMs: inWin.length ? Math.max(0, inWin[0] + this.windowMs - now) : 0,
        bucketEndsInMs: est.bucketStart + this.windowMs - now,
      };
    }
    return { paths: out, tripped: this.log.tripped(), waits: this.waits, margin: this.margin };
  }
}
