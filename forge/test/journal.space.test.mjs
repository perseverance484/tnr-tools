// push/122 repair (2026-10-19): the journal filled browser storage at tree 12 of 15 and the run
// stopped. Finished jobs whose results already left the browser now make room.
import test from "node:test";
import assert from "node:assert/strict";
import { Journal, RECLAIM_AGE_MS } from "../src/storage/journal.mjs";

class QuotaStorage {
  constructor(limit) { this.m = new Map(); this.limit = limit; }
  get length() { return this.m.size; }
  key(i) { return [...this.m.keys()][i] ?? null; }
  getItem(k) { return this.m.has(k) ? this.m.get(k) : null; }
  removeItem(k) { this.m.delete(k); }
  setItem(k, v) {
    const used = [...this.m].reduce((n, [key, val]) => n + (key === k ? 0 : key.length + val.length), 0);
    if (used + k.length + String(v).length > this.limit) { const e = new Error("quota exceeded"); e.name = "QuotaExceededError"; throw e; }
    this.m.set(k, String(v));
  }
}

test("a full journal clears the oldest exported finished jobs, never open ones, and the write succeeds", () => {
  let now = Date.parse("2026-10-19T00:00:00Z");
  const storage = new QuotaStorage(60_000);
  const j = new Journal(storage, () => now);
  // Build jobs directly through the public shape the runner writes.
  const mk = (id, state, extra = {}) => j._write({ jobId: id, state, startedAt: new Date(now).toISOString(), items: Array.from({ length: 10 }, (_, i) => ({ idx: i, state: state === "DONE" ? "VERIFIED" : "PLANNED", name: "x".repeat(500) })), ...extra });
  mk("old-exported", "DONE", { exportedAt: "2026-10-18T00:00:00Z" }); now += 1000;
  mk("open", "PAUSED"); now += 1000;
  mk("recent-unexported", "DONE"); now += 1000;
  mk("old-unexported", "DONE"); now += RECLAIM_AGE_MS + 1;
  // Fill up with an open job until the next write cannot fit.
  let wrote = 0;
  for (let i = 0; i < 20; i++) { try { mk(`run-${i}`, "RUNNING"); wrote++; } catch { break; } }
  assert.ok(j.get("open"), "an open job is never cleared");
  assert.ok(!j.get("old-exported"), "the exported finished job made room");
  assert.ok(j.reclaimed?.length >= 1);
  assert.ok(wrote > 0);
});

test("with nothing reclaimable the write still fails loudly", () => {
  const storage = new QuotaStorage(2_000);
  const j = new Journal(storage, () => 0);
  assert.throws(() => j._write({ jobId: "big", state: "RUNNING", startedAt: "x", items: [{ idx: 0, state: "PLANNED", name: "y".repeat(5000) }] }), /journal write failed/);
});
