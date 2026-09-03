// The budget (spec section 6). Mirrors the server's limiter locally so the client never
// trips it, because a trip is a penalty, not a retry signal.
//
// Server facts, from app/src/server/api/trpc.ts at 345d18ac:
//   Ratelimit.slidingWindow(60, "60 s")             (:123)
//   identifier = `${path}-${context.userId ?? context.userIp}`   (:148)
//   on trip: movedTooFastCount + 1, money * 0.99, bank * 0.99, throw TOO_MANY_REQUESTS (:166-179)
//   applied to publicProcedure only (:211); protectedProcedure carries none (:230)
//
// Two things the local mirror cannot see, which is why it runs at a MARGIN below 60:
//   1. The window is per (path, user), shared with every other tab the user has open on the
//      game. The game's own pages call the same publicProcedure reads on mount.
//   2. Upstash slidingWindow is an approximation (weighted previous window); a strict local
//      count can disagree with it by a few requests near the boundary.
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
  _prune(arr, windowMs, now) { return arr.filter((t) => now - t < windowMs); }

  /** Timestamps in the window for a path, oldest first. */
  inWindow(path, windowMs) {
    const now = this.clock();
    return this._prune(this._load()[path] || [], windowMs, now).sort((a, b) => a - b);
  }

  /** Append n sends for path, prune, flush synchronously. Returns the count in window after. */
  record(path, n, windowMs) {
    const now = this.clock();
    const log = this._load();
    const arr = this._prune(log[path] || [], windowMs, now);
    for (let i = 0; i < n; i++) arr.push(now);
    log[path] = arr;
    this._save(log);
    return arr.length;
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

  /** How many more sends on path fit right now without waiting. */
  available(path) {
    if (!this.isLimited(path)) return Infinity;
    return Math.max(0, this.allowance - this.log.inWindow(path, this.windowMs).length);
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
    for (;;) {
      const inWin = this.log.inWindow(path, this.windowMs);
      if (inWin.length + n <= this.allowance) break;
      // wait for enough of the oldest timestamps to age out
      const need = inWin.length + n - this.allowance;
      const wakeAt = inWin[need - 1] + this.windowMs;
      this.waits++;
      await this.sleep(Math.max(1, wakeAt - this.clock()));
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
        const until = this.clock() + this.windowMs;
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
      out[path] = {
        used: inWin.length, allowance: this.allowance, serverLimit: this.limit,
        resetInMs: inWin.length ? Math.max(0, inWin[0] + this.windowMs - now) : 0,
      };
    }
    return { paths: out, tripped: this.log.tripped(), waits: this.waits, margin: this.margin };
  }
}
