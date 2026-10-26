// Regressions for the final-boundary review of the dungeon corrections (verdict REJECT on
// 0bbc664f: R1, R2). Another tab acts at the two moments a mutation is most exposed: inside the
// journal's write-ahead yield (SENT is on disk, the request has not left) and inside a budget
// wait long enough for this tab's lease to expire. Socket-free: FakeGame, shared MemoryStorage.
import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { SENDLOG_KEY } from "../src/budget/bucket.mjs";
import { LEASE_PREFIX, LeaseHeld, StaleItem } from "../src/runner/runner.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const floor = (kind, ...aiIds) => ({ kind, waves: [{ aiIds }] });
const content = (over = {}) => ({
  name: "Skyglass Wreck", description: "A downed warship on the tideline.",
  sector: 222, longitude: 12, latitude: 7, expiresAt: null, hidden: true, background: "ocean",
  tiers: [
    [floor("floor", "ai-1"), floor("floor", "ai-2"), floor("floor", "ai-3"), floor("floor", "ai-4"), floor("mini-boss", "ai-5")],
    [floor("floor", "ai-6"), floor("floor", "ai-7"), floor("floor", "ai-8"), floor("floor", "ai-9"), floor("boss", "ai-10")],
  ],
  rewards: { money: 5000, experience: 2000, drops: [{ type: "item", id: "chest-1", chance: 100, quantity: 1 }] },
  ...over,
});
const dungeonEdit = (id, name) => ({ items: [{ entity: "dungeon", slot: "edit", name: `edit ${id}`, targetId: id, data: { name } }] });
const jutsuEdit = (id, description) => ({ items: [{ entity: "jutsu", slot: "edit", name: `edit ${id}`, targetId: id, data: { description } }] });
const calls = (game, path) => game.calls.filter((c) => c.path === path).length;

/** Two tabs over one storage, clock and IndexedDB. */
function twoTabs(game, clock = fakeClock()) {
  const storage = new MemoryStorage(), idb = new IDBFactory();
  return [composeForTest({ game, clock, storage, idb, tabId: "tab-a" }), composeForTest({ game, clock, storage, idb, tabId: "tab-b" })];
}
/** Run `fn` once, inside this tab's next write-ahead yield (SENT flushed, request not yet sent). */
function duringYield(h, fn) {
  const real = h.journal.yieldTask;
  h.journal.yieldTask = async () => { h.journal.yieldTask = real; await real(); await fn(); };
}

// ------------------------------------------------------------------ R1 trip during the write-ahead yield
for (const [label, path, seed, edit] of [
  ["metered dungeon.save", "dungeon.save", (g) => { for (const id of ["d-a", "d-b"]) g.seed("dungeon", { id, content: content({ name: id }), updatedAt: new Date(0) }); }, (id, v) => dungeonEdit(id === "a" ? "d-a" : "d-b", v)],
  ["unmetered jutsu.update", "jutsu.update", (g) => { for (const id of ["j-a", "j-b"]) g.seed("jutsu", { id, name: id }); }, (id, v) => jutsuEdit(id === "a" ? "j-a" : "j-b", v)],
]) {
  test(`R1 (${label}): a trip another tab records during the write-ahead yield stops the pending send, which is withdrawn, not ambiguous`, async () => {
    const game = new FakeGame(); seed(game);
    const [a, b] = twoTabs(game);
    duringYield(a, async () => {
      game.limitPath = path;
      b.runner.plan(edit("b", "from tab b"), { jobId: "b" });
      assert.equal((await b.runner.run("b")).pause.reason, "TOO_MANY_REQUESTS");
      game.limitPath = null;
    });
    a.runner.plan(edit("a", "from tab a"), { jobId: "a" });
    const s = await a.runner.run("a");
    assert.equal(s.pause.reason, "TOO_MANY_REQUESTS");
    assert.equal(calls(game, path), 1, "only tab b's refused request reached the game");
    const item = a.journal.get("a").items[0];
    assert.equal(item.state, "PLANNED", "the write-ahead SENT was withdrawn: the request provably never left");
    assert.match(item.withdrawn.reason, /limiter tripped/);
    assert.equal(b.journal.get("b").items[0].state, "FAILED", "tab b's decoded 429 stays a definite failure");

    // a restart honours the trip; after expiry the edit goes exactly once
    const trip = JSON.parse(a.storage.getItem(SENDLOG_KEY)).__tripped;
    const r = composeForTest({ game, clock: a.clock, storage: a.storage.crash(), idb: a.idb, tabId: "tab-r" });
    r.runner.attach("a", edit("a", "from tab a"));
    assert.equal((await r.runner.resume("a")).pause.reason, "TOO_MANY_REQUESTS");
    assert.equal(calls(game, path), 1);
    a.clock.set(trip.until);
    assert.equal((await r.runner.run("a")).counts.VERIFIED, 1);
    assert.equal((await r.runner.run("a")).state, "DONE");
    assert.equal(calls(game, path), 2, "sent once after expiry, and never again");
  });
}

test("R1: a lease lost during the write-ahead yield stops the send and withdraws the SENT", async () => {
  const game = new FakeGame();
  game.seed("dungeon", { id: "d-a", content: content(), updatedAt: new Date(0) });
  const [a] = twoTabs(game);
  duringYield(a, () => { a.storage.setItem(LEASE_PREFIX + "a", JSON.stringify({ tab: "tab-z", at: a.clock() })); });
  a.runner.plan(dungeonEdit("d-a", "renamed"), { jobId: "a" });
  await assert.rejects(() => a.runner.run("a"), LeaseHeld);
  assert.equal(calls(game, "dungeon.save"), 0);
  const item = a.journal.get("a").items[0];
  assert.equal(item.state, "PLANNED");
  assert.match(item.withdrawn.reason, /another tab/);
});

test("R1: a request that may have left is still SENT and reconciled, never withdrawn", async () => {
  const game = new FakeGame({ crashAt: 2 }); // getAll (1), the save applies and the tab dies (2)
  game.seed("dungeon", { id: "d-a", content: content(), updatedAt: new Date(0) });
  const [a] = twoTabs(game);
  a.runner.plan(dungeonEdit("d-a", "renamed"), { jobId: "a" });
  assert.equal((await a.runner.run("a")).pause.reason, "AMBIGUOUS");
  const item = a.journal.get("a").items[0];
  assert.equal(item.state, "SENT"); assert.equal(item.withdrawn, undefined);
});

// ------------------------------------------------------------------ R2 same-job takeover during a budget wait
test("R2: a stale tab that loses its job during a budget wait preserves the other tab's CONFIRMED/verify and INCOMPLETE state", async () => {
  const game = new FakeGame();
  for (let i = 0; i < 30; i++) game.seed("dungeon", { id: `dun-${i}`, content: content({ name: `Dungeon ${i}` }), updatedAt: new Date(0) });
  game.seed("dungeon", { id: "dun-x", content: content(), updatedAt: new Date(0) });
  // the row becomes unreadable right after it is saved, until visibility returns
  let unreadable = false;
  const handle = game.handle.bind(game);
  game.handle = (path, input) => {
    if (unreadable && path === "dungeon.getAll") return { ok: false, error: { code: "INTERNAL_SERVER_ERROR", httpStatus: 500, message: "read unavailable", path, zodError: null } };
    const r = handle(path, input);
    if (path === "dungeon.save" && input.id === "dun-x") unreadable = true;
    return r;
  };
  const clock = fakeClock(), advance = clock.tick;
  const [a, b] = twoTabs(game, clock);
  a.runner.plan({ items: Array.from({ length: 30 }, (_, i) => ({ entity: "dungeon", slot: "edit", name: `fill ${i}`, targetId: `dun-${i}`, data: { name: `Filled ${i}` } })) }, { jobId: "exhaust" });
  assert.equal((await a.runner.run("exhaust")).counts.VERIFIED, 30);

  // tab a waits for a token; meanwhile its lease expires and tab b runs the SAME job
  let tookOver = null;
  clock.tick = async (ms) => {
    clock.tick = advance;
    const t = advance(ms);
    b.runner.attach("w", dungeonEdit("dun-x", "Renamed"));
    tookOver = await b.runner.run("w");
    return t;
  };
  a.runner.plan(dungeonEdit("dun-x", "Renamed"), { jobId: "w" });
  await assert.rejects(() => a.runner.run("w"), StaleItem);
  assert.equal(tookOver.state, "INCOMPLETE", JSON.stringify(tookOver));
  assert.equal(calls(game, "dungeon.save"), 31, "tab b's one save; tab a sent nothing");
  const job = a.journal.get("w"), item = job.items[0];
  assert.equal(job.state, "INCOMPLETE", "tab a did not finish the job over tab b's state");
  assert.equal(item.state, "CONFIRMED"); assert.equal(item.phase, "verify"); assert.equal(item.verify, "unread");

  // once the row is visible again, resuming only verifies
  unreadable = false;
  const s = await a.runner.run("w");
  assert.equal(s.state, "DONE"); assert.equal(s.counts.VERIFIED, 1);
  assert.equal(calls(game, "dungeon.save"), 31, "no second save");
});
