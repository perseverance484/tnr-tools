// Regressions for the re-review of the dungeon corrections (verdict REJECT on a9af6fcd: R1, R2,
// N1). Each case runs another tab's action INSIDE a budget wait: the clock's tick (the harness's
// sleep) is hooked once, so the action happens while this tab is held for a coop.dungeon.save token.
// Socket-free; the extractor cases read a copy of the pinned game source and never run it.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, readFileSync, cpSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { IDBFactory } from "fake-indexeddb";
import { CONTRACT } from "../src/dungeon/validate.mjs";
import { SENDLOG_KEY } from "../src/budget/bucket.mjs";
import { LEASE_PREFIX, LeaseHeld, StaleItem } from "../src/runner/runner.mjs";
import { derive } from "../tools/derive_dungeon.mjs";
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
const PACKAGES = { "pk-1": { name: "Wreck Haul", description: "Salvage", rewards: { reward_money: 100, reward_items: [] } },
  "pk-2": { name: "Captain's Chest", description: "Gold", rewards: { reward_money: 700, reward_items: [] } } };
const saves = (game) => game.calls.filter((c) => c.path === "coop.dungeon.save");
const edit = (targetId, data, extra = {}) => ({ items: [{ entity: "dungeon", slot: "edit", name: `edit ${targetId}`, targetId, data, ...extra }] });

/** A fake clock whose next sleep first advances time, then runs `fn` (another tab acting during the wait). */
function hookedClock() {
  const c = fakeClock(), advance = c.tick;
  let hook = null;
  c.onNextSleep = (fn) => { hook = fn; };
  c.tick = async (ms) => { const t = advance(ms); const fn = hook; hook = null; if (fn) await fn(); return t; };
  return c;
}

/** A game holding 30 dungeons plus `dun-x`, and a tab that has just spent coop.dungeon.save's whole allowance. */
async function exhausted({ target = content(), clock = hookedClock(), storage = new MemoryStorage(), idb = new IDBFactory(), game = new FakeGame() } = {}) {
  game.packages = new Map(Object.entries(structuredClone(PACKAGES)));
  for (let i = 0; i < 30; i++) game.seed("dungeon", { id: `dun-${i}`, content: content({ name: `Dungeon ${i}` }), updatedAt: new Date(0) });
  game.seed("dungeon", { id: "dun-x", content: target, updatedAt: new Date(0) });
  const h = composeForTest({ game, clock, storage, idb, tabId: "tab-1" });
  h.runner.plan({ items: Array.from({ length: 30 }, (_, i) => ({ entity: "dungeon", slot: "edit", name: `fill ${i}`, targetId: `dun-${i}`, data: { name: `Filled ${i}` } })) }, { jobId: "exhaust" });
  assert.equal((await h.runner.run("exhaust")).counts.VERIFIED, 30);
  assert.equal(h.budget.available("coop.dungeon.save"), 0);
  return h;
}

/** Plan an edit of dun-x, let `during` act while it waits for its token, then run it. */
async function waitingEdit(h, data, extra, during) {
  let ran = false;
  h.clock.onNextSleep(async () => { ran = true; await during(); });
  h.runner.plan(edit("dun-x", data, extra), { jobId: "w" });
  const out = await h.runner.run("w").then((s) => ({ s }), (error) => ({ error }));
  assert.ok(ran, "the edit really waited for a token");
  return out;
}
const liveX = (h) => h.game.tables.dungeon.get("dun-x");

// ------------------------------------------------------------------ R1 trip guard
test("R1 A: a trip another tab persists while this tab waits for a token stops this tab's send", async () => {
  const h = await exhausted();
  const other = composeForTest({ game: h.game, clock: h.clock, storage: h.storage, idb: h.idb, tabId: "tab-2" });
  const { s } = await waitingEdit(h, { name: "Waiting" }, {}, async () => {
    h.game.limitPath = "coop.dungeon.save";
    other.runner.plan(edit("dun-0", { name: "Other tab" }), { jobId: "other" });
    assert.equal((await other.runner.run("other")).pause.reason, "TOO_MANY_REQUESTS");
    h.game.limitPath = null;
  });
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "TOO_MANY_REQUESTS");
  assert.equal(h.journal.get("w").items[0].state, "PLANNED", "a local refusal leaves the item unsent, not ambiguous");
  assert.equal(saves(h.game).length, 31, "the 30 that fit and the other tab's refused one; nothing from the waiting tab");
  assert.equal(other.journal.get("other").items[0].state, "FAILED", "the decoded 429 stays a definite failure");

  // the same holds after a restart, and the waiting edit goes once the trip expires
  const trip = JSON.parse(h.storage.getItem(SENDLOG_KEY)).__tripped;
  const h2 = composeForTest({ game: h.game, clock: h.clock, storage: h.storage.crash(), idb: h.idb, tabId: "tab-3" });
  h2.runner.attach("w", edit("dun-x", { name: "Waiting" }));
  assert.equal((await h2.runner.run("w")).pause.reason, "TOO_MANY_REQUESTS");
  assert.equal(saves(h.game).length, 31);
  h.clock.set(trip.until);
  assert.equal((await h2.runner.run("w")).counts.VERIFIED, 1);
  assert.equal(other.journal.get("other").items[0].state, "FAILED", "and the refused save was never resent");
});

const AI = (userId, aiProfileId) => ({ userId, username: `Bandit ${userId}`, isAi: true, level: 10, rank: "GENIN", aiProfileId, jutsus: [], items: [] });
const rules = (userId, name) => ({ items: [{ entity: "aiProfile", slot: "edit", targetId: userId, name, data: { rules: [{ conditions: [], action: { type: "end_turn" } }], includeDefaultRules: false } }] });

test("R1 B: after a 429 on the unmetered ai.updateAiProfile, no fresh job sends a mutation until the trip expires", async () => {
  const game = new FakeGame({ limitPath: "ai.updateAiProfile" });
  for (const [u, p] of [["a1", "p1"], ["a2", "p2"]]) { game.seed("ai", AI(u, p)); game.tables.aiProfile.set(p, { id: p, userId: u, rules: [], includeDefaultRules: true }); }
  const updates = () => game.calls.filter((c) => c.path === "ai.updateAiProfile").length;
  const h = composeForTest({ game });
  h.runner.plan(rules("a1", "first"), { jobId: "first" });
  assert.equal((await h.runner.run("first")).pause.reason, "TOO_MANY_REQUESTS");
  assert.equal(h.journal.get("first").items[0].state, "FAILED");
  game.limitPath = null;

  // a fresh job: its protected reads are unmetered, so only the global guard stands in the way
  h.runner.plan(rules("a2", "second"), { jobId: "second" });
  const s = await h.runner.run("second");
  assert.equal(s.pause.reason, "TOO_MANY_REQUESTS");
  assert.equal(h.journal.get("second").items[0].state, "PLANNED");
  assert.equal(updates(), 1);

  const h2 = composeForTest({ game, clock: h.clock, storage: h.storage.crash(), idb: h.idb, tabId: "tab-2" });
  h2.runner.plan(rules("a2", "third"), { jobId: "third" });
  assert.equal((await h2.runner.run("third")).pause.reason, "TOO_MANY_REQUESTS", "a restarted tab honours it too");
  assert.equal(updates(), 1);
  h.clock.set(JSON.parse(h.storage.getItem(SENDLOG_KEY)).__tripped.until);
  assert.equal((await h2.runner.run("third")).state, "DONE");
  assert.equal(updates(), 2);
  const log = JSON.parse(h2.storage.getItem(SENDLOG_KEY));
  assert.equal(log["ai.updateAiProfile"], undefined, "an unmetered path still spends no token");
});

// ------------------------------------------------------------------ R2 fresh payload after the wait
test("R2: a known field another operator changes during the wait is preserved; one token per save", async () => {
  const h = await exhausted();
  const { s } = await waitingEdit(h, { name: "Renamed" }, {}, async () => { liveX(h).content.description = "Changed by another operator"; });
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.equal(liveX(h).content.description, "Changed by another operator", "the concurrent change survives");
  assert.equal(liveX(h).content.name, "Renamed");
  assert.equal(saves(h.game).at(-1).input.content.description, "Changed by another operator", "the payload was built after the wait");
  assert.equal(JSON.parse(h.storage.getItem(SENDLOG_KEY))["coop.dungeon.save"].length, saves(h.game).length, "exactly one token per save");
});

test("R2: an unknown content key that appears during the wait is refused as schema drift, not deleted", async () => {
  const h = await exhausted();
  const { s } = await waitingEdit(h, { name: "Renamed" }, {}, async () => { liveX(h).content.minLevel = 40; });
  assert.equal(s.counts.FAILED, 1);
  assert.match(h.journal.get("w").items[0].error, /schema drift/);
  assert.equal(saves(h.game).length, 30);
  assert.equal(liveX(h).content.minLevel, 40);
});

test("R2: a package drop that appears during the wait needs refreshPackages; nothing is sent", async () => {
  const h = await exhausted();
  const { s } = await waitingEdit(h, { name: "Renamed" }, {}, async () => {
    liveX(h).content.rewards.drops.push({ type: "package", id: "pk-1", chance: 5, quantity: 1, package: PACKAGES["pk-1"] });
  });
  assert.equal(s.counts.FAILED, 1);
  assert.match(h.journal.get("w").items[0].error, /refreshPackages/);
  assert.equal(saves(h.game).length, 30);
});

test("R2: a package drop changed during the wait is the one refreshed and recorded", async () => {
  const withPk1 = content({ rewards: { money: 0, experience: 0, tokens: 0, prestige: 0, drops: [{ type: "package", id: "pk-1", chance: 5, quantity: 1, package: PACKAGES["pk-1"] }] } });
  const h = await exhausted({ target: withPk1 });
  const { s } = await waitingEdit(h, { name: "Renamed" }, { refreshPackages: true }, async () => {
    Object.assign(liveX(h).content.rewards.drops[0], { id: "pk-2", package: PACKAGES["pk-2"] });
  });
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.deepEqual(h.journal.get("w").items[0].packagesRefreshed, ["pk-2"]);
  assert.deepEqual(liveX(h).content.rewards.drops[0].package, PACKAGES["pk-2"]);
});

test("R2: a lease another tab takes during the wait stops this tab before it reads or sends", async () => {
  const h = await exhausted();
  const reads = () => h.game.calls.filter((c) => c.path === "coop.dungeon.getAll").length;
  let before = 0;
  const { error } = await waitingEdit(h, { name: "Renamed" }, {}, async () => {
    before = reads();
    h.storage.setItem(LEASE_PREFIX + "w", JSON.stringify({ tab: "tab-9", at: h.clock() }));
  });
  assert.ok(error instanceof LeaseHeld, String(error));
  assert.equal(reads(), before, "no read after losing the lease");
  assert.equal(saves(h.game).length, 30);
  assert.equal(h.journal.get("w").items[0].state, "PLANNED");
});

test("R2: an item another tab resolves during the wait is never sent", async () => {
  const h = await exhausted();
  const { error } = await waitingEdit(h, { name: "Renamed" }, {}, async () => { h.journal.transition("w", 0, "SKIPPED"); });
  assert.ok(error instanceof StaleItem, String(error));
  assert.equal(saves(h.game).length, 30);
  assert.equal(h.journal.get("w").items[0].state, "SKIPPED", "the other tab's decision stands");
  assert.equal(liveX(h).content.name, "Skyglass Wreck");
});

test("R2: a dungeon create waits before its snapshot and payload, and still sends once", async () => {
  const h = await exhausted();
  let snapshotsDuringWait = -1;
  h.clock.onNextSleep(async () => { snapshotsDuringWait = h.game.calls.filter((c) => c.path === "coop.dungeon.getAll").length; });
  const before = h.game.calls.filter((c) => c.path === "coop.dungeon.getAll").length;
  h.runner.plan({ items: [{ entity: "dungeon", slot: "create", name: "New Wreck", srcId: "new", data: content({ name: "New Wreck" }) }] }, { jobId: "c" });
  assert.equal((await h.runner.run("c")).counts.VERIFIED, 1);
  assert.equal(snapshotsDuringWait, before, "the pre-create snapshot is taken after the wait");
  assert.equal(saves(h.game).length, 31);
});

// ------------------------------------------------------------------ N1 extractor indentation
const GAME = process.env.TNR_GAME_CHECKOUT;
test("N1: members at any other indentation are refused, not skipped", { skip: !GAME && "set TNR_GAME_CHECKOUT to a checkout at the pin" }, () => {
  const sources = Object.keys(CONTRACT._meta.sources);
  const anchor = "    hidden: z.boolean().prefault(true),\n";
  const cases = {
    "spread at 2": "  ...extraFields,\n",
    "computed at 2": "  [\"newField\"]: z.number(),\n",
    "shorthand at 2": "  extraField,\n",
    "ordinary member at 2": "  newField: z.number(),\n",
    "spread at 0": "...extraFields,\n",
    "ordinary member at 6": "      newField: z.number(),\n",
  };
  for (const [label, line] of Object.entries(cases)) {
    const dir = mkdtempSync(join(tmpdir(), "dungeon-n1-"));
    for (const p of sources) cpSync(join(GAME, p), join(dir, p));
    const p = join(dir, sources[0]), s = readFileSync(p, "utf8");
    assert.ok(s.includes(anchor));
    writeFileSync(p, s.replace(anchor, anchor + line));
    assert.throws(() => derive(dir), /dungeonContentSchema/, label);
  }
});
