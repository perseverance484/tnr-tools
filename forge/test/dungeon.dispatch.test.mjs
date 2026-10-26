// Regressions for the dispatch-ownership review (verdict REJECT on ff4f1c73). A tab suspended in
// the journal's write-ahead yield (SENT flushed, request not yet sent) loses its lease; another tab
// resumes the SAME job through the public runner operations, resolves the item and finishes the
// job, releasing the lease. The first tab must then send nothing and overwrite nothing.
// Socket-free: FakeGame, shared MemoryStorage.
import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { Journal, StaleItem } from "../src/storage/journal.mjs";
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
const saves = (game) => game.calls.filter((c) => c.path === "dungeon.save").length;

function twoTabs(game) {
  const clock = fakeClock(), storage = new MemoryStorage(), idb = new IDBFactory();
  return [composeForTest({ game, clock, storage, idb, tabId: "tab-a" }), composeForTest({ game, clock, storage, idb, tabId: "tab-b" })];
}
/** Run `fn` once inside this tab's next write-ahead yield, after letting its lease expire. */
function takeoverDuringYield(a, fn) {
  const real = a.journal.yieldTask;
  a.journal.yieldTask = async () => { a.journal.yieldTask = real; await real(); a.clock.tick(31_000); await fn(); };
}

test("dispatch ownership: tab B reconciles, skips and finishes a create tab A has SENT; A sends nothing", async () => {
  const game = new FakeGame();
  const [a, b] = twoTabs(game);
  const manifest = { items: [{ entity: "dungeon", slot: "create", name: "Skyglass Wreck", srcId: "wreck", data: content() }] };
  takeoverDuringYield(a, async () => {
    b.runner.attach("c", manifest);
    const s = await b.runner.resume("c");
    assert.equal(s.pause.reason, "ORPHANED", "no row exists, so the SENT create is orphaned");
    b.runner.skip("c", 0);
    assert.equal((await b.runner.run("c")).state, "DONE");
  });
  a.runner.plan(manifest, { jobId: "c" });
  await assert.rejects(() => a.runner.run("c"), StaleItem);
  assert.equal(saves(game), 0, "no create left tab A");
  assert.equal(game.count("dungeon"), 0, "no untracked row");
  const job = a.journal.get("c"), item = job.items[0];
  assert.equal(job.state, "DONE"); assert.equal(item.state, "SKIPPED"); assert.equal(item.entityId ?? null, null);
  assert.equal(item.withdrawn, undefined, "the operator's decision was not overwritten by a withdrawal");
});

test("dispatch ownership: an update takeover — B skips, or B re-sends itself — never lets A's stale update out", async () => {
  for (const resolve of ["skip", "adopt"]) {
    const game = new FakeGame();
    game.seed("dungeon", { id: "dun-1", content: content(), updatedAt: new Date(0) });
    const [a, b] = twoTabs(game);
    const manifest = { items: [{ entity: "dungeon", slot: "edit", name: "W", targetId: "dun-1", data: { name: `Renamed (${resolve})` } }] };
    takeoverDuringYield(a, async () => {
      b.runner.attach("u", manifest);
      assert.equal((await b.runner.resume("u")).pause.reason, "ORPHANED", "the update did not land, so it is a decision");
      if (resolve === "skip") b.runner.skip("u", 0);
      else b.runner.adopt("u", 0, "dun-1"); // the operator chooses to re-send it from tab B
      assert.equal((await b.runner.run("u")).state, "DONE");
    });
    a.runner.plan(manifest, { jobId: "u" });
    await assert.rejects(() => a.runner.run("u"), StaleItem, resolve);
    const item = a.journal.get("u").items[0];
    if (resolve === "skip") {
      assert.equal(saves(game), 0); assert.equal(item.state, "SKIPPED");
      assert.equal(game.rows("dungeon")[0].content.name, "Skyglass Wreck");
    } else {
      assert.equal(saves(game), 1, "only tab B's own re-send"); assert.equal(item.state, "VERIFIED");
      assert.equal(item.attempt, 2, "tab B's attempt replaced tab A's");
    }
    assert.equal(a.journal.get("u").state, "DONE");
  }
});

// ------------------------------------------------------------------ journal-level attempt identity
function suspended() {
  const storage = new MemoryStorage(), clock = fakeClock();
  let release;
  const gate = new Promise((r) => { release = r; });
  const j = new Journal(storage, clock, { yieldTask: () => gate });
  const other = new Journal(storage, clock); // another tab over the same storage
  j.open({ jobId: "j", items: [{ entity: "dungeon", op: "update", name: "W", targetId: "dun-1", payloadHash: "h" }] });
  return { j, other, release };
}

test("attempt identity: a replaced SENT attempt is neither dispatched nor withdrawn by the old one", async () => {
  for (const withRefusal of [false, true]) {
    const { j, other, release } = suspended();
    let dispatched = 0;
    const pending = j.withSent("j", 0, { phase: "update" }, () => { dispatched++; }, withRefusal ? () => { throw new Error("trip"); } : null);
    // while A is suspended, tab B reconciles A's SENT and sends its own attempt
    other.transition("j", 0, "ORPHANED");
    other.transition("j", 0, "CONFIRMED", { entityId: "dun-1", phase: "update" });
    other.transition("j", 0, "SENT", { phase: "update", attempt: 2 });
    release();
    await assert.rejects(pending, StaleItem);
    assert.equal(dispatched, 0);
    const item = other.get("j").items[0];
    assert.equal(item.state, "SENT"); assert.equal(item.attempt, 2, "tab B's attempt is untouched");
    assert.equal(item.withdrawn, undefined);
  }
});

test("attempt identity: the item's own unchanged attempt is still withdrawn on a pre-dispatch refusal, and counts on", async () => {
  const { j, other, release } = suspended();
  const pending = j.withSent("j", 0, { phase: "update" }, () => assert.fail("dispatched"), () => { throw new Error("limiter tripped"); });
  release();
  await assert.rejects(pending, /limiter tripped/);
  const item = other.get("j").items[0];
  assert.equal(item.state, "PLANNED"); assert.match(item.withdrawn.reason, /limiter tripped/);
  assert.equal(item.attempt, 1, "a withdrawn attempt number is never reused");
  const next = new Journal(other.storage, fakeClock(), { yieldTask: async () => {} });
  let sent = 0;
  await next.withSent("j", 0, { phase: "update" }, () => { sent++; });
  assert.equal(sent, 1); assert.equal(next.get("j").items[0].attempt, 2);
});
