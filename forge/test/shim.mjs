// Test doubles. No network anywhere in here.

/**
 * In-memory localStorage that records every write in order, so a test can prove that a
 * journal flush happened BEFORE a fetch was issued. Supports a byte quota to simulate
 * QuotaExceededError, and a crash() that freezes the store to whatever is on "disk".
 */
export class MemoryStorage {
  constructor({ quota = Infinity } = {}) {
    this._m = new Map();
    this.quota = quota;
    this.log = [];         // [{op, key, at}] in call order
    this._seq = 0;
  }
  get length() { return this._m.size; }
  key(i) { return Array.from(this._m.keys())[i] ?? null; }
  getItem(k) { return this._m.has(k) ? this._m.get(k) : null; }
  setItem(k, v) {
    v = String(v);
    const size = Array.from(this._m.entries()).reduce((a, [kk, vv]) => a + (kk === k ? 0 : vv.length), 0) + v.length;
    if (size > this.quota) {
      const e = new Error("QuotaExceededError"); e.name = "QuotaExceededError"; throw e;
    }
    this._m.set(k, v);
    this.log.push({ op: "set", key: k, seq: ++this._seq });
  }
  removeItem(k) { this._m.delete(k); this.log.push({ op: "remove", key: k, seq: ++this._seq }); }
  clear() { this._m.clear(); this.log.push({ op: "clear", seq: ++this._seq }); }
  /** Simulate eviction: return a fresh storage holding exactly what has been flushed. */
  crash() { const s = new MemoryStorage({ quota: this.quota }); s._m = new Map(this._m); return s; }
  snapshot() { return Object.fromEntries(this._m); }
}

/** A monotonic fake clock. */
export function fakeClock(start = 1_756_700_000_000) {
  let t = start;
  const clock = () => t;
  clock.tick = (ms = 1000) => { t += ms; return t; };
  clock.set = (ms) => { t = ms; };
  return clock;
}

/** An event recorder shared between storage and a fake transport, to prove ordering. */
export function orderLog() {
  const events = [];
  let seq = 0;
  return {
    events,
    mark(name, extra = {}) { events.push({ name, seq: ++seq, ...extra }); return seq; },
    seqOf(name) { const e = events.find((x) => x.name === name); return e ? e.seq : -1; },
  };
}
