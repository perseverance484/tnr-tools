import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { IDBFactory } from "fake-indexeddb";
import { Journal } from "../src/storage/journal.mjs";
import { CaptureCache } from "../src/storage/captures.mjs";
import { readIdmap, IDMAP_KEY } from "../src/storage/compat.mjs";
import { Budget } from "../src/budget/bucket.mjs";
import { CachedReader } from "../src/budget/reader.mjs";
import { Validator } from "../src/runner/validate.mjs";
import { Runner, Paused } from "../src/runner/runner.mjs";
import { parseManifest, planOrder, ManifestError } from "../src/runner/manifest.mjs";
import { mergeAi, mergeForUpdate } from "../src/runner/recipes.mjs";
import { FakeGame, FakeClient, CrashSignal } from "./fakegame.mjs";
import { Reconciler } from "../src/reconcile/reconciler.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";

const SCHEMAS = JSON.parse(readFileSync(new URL("../../skills/building-tnr-content/data/45d_DATA_entity_schemas.json", import.meta.url), "utf8"));

function harness({ game = new FakeGame(), storage = new MemoryStorage(), idb = new IDBFactory(), reconcile = true } = {}) {
  const clock = fakeClock();
  const journal = new Journal(storage, clock);
  const cache = new CaptureCache(idb, clock);
  const budget = new Budget({ storage, clock, sleep: async (ms) => clock.tick(ms) });
  const client = new FakeClient(game);
  const reader = new CachedReader({ client, cache, budget });
  const reconciler = reconcile ? new Reconciler({ storage, reader, clock }) : null;
  const runner = new Runner({ journal, client, reader, cache, budget, validator: new Validator(SCHEMAS), storage, reconciler });
  return { game, storage, idb, clock, journal, cache, budget, client, reader, runner };
}
const M = {
  oneJutsu: { items: [{ entity: "jutsu", slot: "create", name: "Ember Step", srcId: "ember", data: { name: "Ember Step", description: "d", hidden: true, effects: [{ type: "damage", power: 150 }] } }] },
  twoCreates: { items: [
    { entity: "jutsu", slot: "create", name: "A", srcId: "a", data: { name: "A", hidden: true } },
    { entity: "asset", slot: "create", name: "B", srcId: "b", data: { name: "B", hidden: true, type: "STATIC", url: "https://x/y.webp" } },
  ] },
  editQuest: (id) => ({ items: [{ entity: "quest", slot: "edit", name: "Q", targetId: id, data: { name: "Renamed", consecutiveObjectives: true } }] }),
  aiWithRules: { items: [{ entity: "ai", slot: "create", name: "Pale Fang", srcId: "fang", data: { username: "Pale Fang", level: 10, rules: [{ conditions: [], action: { type: "end_turn", description: "End turn" } }], includeDefaultRules: false } }] },
  refChain: { items: [
    { entity: "quest", slot: "create", name: "Q", srcId: "q1", data: { name: "Q", content: { objectives: [{ id: "o1", task: "defeat_opponents", opponentAIs: [{ ids: ["@ai:boss"], number: 1 }] }], reward: {}, sceneBackground: "", sceneCharacters: [] } } },
    { entity: "ai", slot: "create", name: "Boss", srcId: "boss", data: { username: "Boss", level: 5 } },
  ] },
};

// ---------------------------------------------------------------- planning
test("parseManifest: normalises slots, mirrors name into data on creates, refuses bad shapes", () => {
  const m = parseManifest(M.oneJutsu);
  assert.equal(m.items[0].op, "create"); assert.equal(m.items[0].data.name, "Ember Step");
  assert.equal(parseManifest(M.editQuest("x")).items[0].op, "update");
  assert.throws(() => parseManifest({ items: [{ entity: "jutsu", slot: "create", name: "no srcId", data: {} }] }), /needs srcId/);
  assert.throws(() => parseManifest({ items: [{ entity: "jutsu", slot: "edit", name: "no target", data: {} }] }), /needs targetId/);
  assert.throws(() => parseManifest({ items: [{ entity: "nope", slot: "create", srcId: "x", data: {} }] }), /unknown entity/);
  assert.throws(() => parseManifest("{"), ManifestError);
  assert.throws(() => parseManifest({ items: [] }), /no items/);
  assert.ok(parseManifest({ items: [], capture: { after: [{ proc: "jutsu.getAllNames" }] } }));
});

test("planOrder: an item referencing @ai:boss is moved after the boss create; unknown ref and cycles refuse", () => {
  const order = planOrder(parseManifest(M.refChain));
  assert.deepEqual(order.map((o) => o.srcId), ["boss", "q1"]);
  assert.deepEqual(order[1].deps, ["boss"]);
  assert.throws(() => planOrder(parseManifest({ items: [{ entity: "quest", slot: "create", srcId: "q", name: "Q", data: { x: "@ai:ghost" } }] })), /unknown/);
  assert.throws(() => planOrder(parseManifest({ items: [
    { entity: "quest", slot: "create", srcId: "a", name: "A", data: { x: "@quest:b" } },
    { entity: "quest", slot: "create", srcId: "b", name: "B", data: { x: "@quest:a" } }] })), /cycle/);
  // a ref satisfied by the idmap is not a dependency
  const o2 = planOrder(parseManifest({ items: [{ entity: "quest", slot: "create", srcId: "q", name: "Q", data: { x: "@ai:known" } }] }), { known: "id-known" });
  assert.deepEqual(o2[0].deps, []);
});

test("mergeForUpdate picks the 45d field set from live ∪ asserted (relations dropped)", () => {
  const v = new Validator(SCHEMAS);
  const live = { id: "j", name: "old", description: "d", hidden: true, bloodline: { id: "rel" }, bloodlineId: null, createdAt: new Date(0), effects: [] };
  const out = mergeForUpdate("jutsu", live, { name: "new" }, v.knownFields("jutsu"));
  assert.equal(out.name, "new"); assert.equal(out.description, "d");
  assert.ok(!("bloodline" in out)); assert.ok(!("id" in out)); assert.ok(!("createdAt" in out));
  assert.equal(out.bloodlineId, null);
});

test("mergeAi re-sends the live kit reshaped (omitting jutsus/items would delete them, law 70)", () => {
  const live = { userId: "u", username: "X", level: 3, isAi: true, aiProfileId: "p", questData: {}, jutsus: [{ jutsuId: "j1", jutsu: {} }], items: [{ itemId: "i1", quantity: 2, item: {} }] };
  const out = mergeAi(live, { level: 4 });
  assert.deepEqual(out.jutsus, ["j1"]);
  assert.deepEqual(out.items, [{ ids: ["i1"], number: 2 }]);
  assert.equal(out.level, 4); assert.equal(out.isAi, true);
  assert.ok(!("questData" in out)); assert.ok(!("aiProfileId" in out) || out.aiProfileId === "p");
  assert.ok(!("rules" in out));
  const asserted = mergeAi(live, { jutsus: ["j9"], items: ["i9"] });
  assert.deepEqual(asserted.jutsus, ["j9"]); assert.deepEqual(asserted.items, [{ ids: ["i9"], number: 1 }]);
});

// ---------------------------------------------------------------- happy paths
test("two-phase create: create -> placeholder -> update -> read-back VERIFIED; exactly one row", async () => {
  const h = harness();
  h.runner.plan(M.oneJutsu, { jobId: "j1", manifestPath: "push/x.json" });
  const s = await h.runner.run("j1");
  assert.equal(s.state, "DONE"); assert.deepEqual(s.counts, { VERIFIED: 1 });
  assert.equal(h.game.count("jutsu"), 1);
  const row = h.game.rows("jutsu")[0];
  assert.equal(row.name, "Ember Step"); assert.equal(row.effects[0].power, 150); // uncapped power went through
  assert.deepEqual(h.game.calls.map((c) => c.path), ["jutsu.getAllNames", "jutsu.create", "jutsu.get", "jutsu.update", "jutsu.get"]); // snapshot, create, fill-read, update, read-back
  assert.equal(readIdmap(h.storage).ember, row.id);
  assert.equal(h.journal.get("j1").items[0].entityId, row.id);
});

test("edit: get -> merge -> update -> VERIFIED on asserted keys only", async () => {
  const h = harness();
  const q = h.game.seed("quest", { id: "q-1", name: "Old", description: "keep", hidden: true, consecutiveObjectives: false, content: { objectives: [], reward: {}, sceneBackground: "", sceneCharacters: [] } });
  h.runner.plan(M.editQuest("q-1"), { jobId: "e1" });
  const s = await h.runner.run("e1");
  assert.equal(s.counts.VERIFIED, 1);
  assert.equal(q.name, "Renamed"); assert.equal(q.consecutiveObjectives, true); assert.equal(q.description, "keep");
  const upd = h.game.calls.find((c) => c.path === "quests.update");
  assert.ok(!("id" in upd.input.data) && !("createdAt" in upd.input.data));
});

test("ai with rules: create -> updateAi(kit re-sent) -> toggle -> updateAiProfile -> VERIFIED", async () => {
  const h = harness();
  h.runner.plan(M.aiWithRules, { jobId: "a1" });
  const s = await h.runner.run("a1");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  const ai = h.game.rows("ai")[0];
  assert.equal(ai.username, "Pale Fang"); assert.ok(ai.aiProfileId);
  const prof = h.game.tables.aiProfile.get(ai.aiProfileId);
  assert.equal(prof.rules[0].action.type, "end_turn"); assert.equal(prof.includeDefaultRules, false);
  assert.deepEqual(h.game.calls.map((c) => c.path), ["profile.getAllAiNames", "profile.create", "profile.getAi", "profile.updateAi", "profile.getAi", "ai.toggleAiProfile", "profile.getAi", "ai.updateAiProfile", "profile.getAi", "ai.getAiProfile"]);
  const upd = h.game.calls.find((c) => c.path === "profile.updateAi");
  assert.ok(!("rules" in upd.input.data)); assert.deepEqual(upd.input.data.jutsus, []); assert.equal(upd.input.data.isAi, true);
});

test("refs: @ai:boss resolves to the id minted earlier in the same job", async () => {
  const h = harness();
  h.runner.plan(M.refChain, { jobId: "r1" });
  const s = await h.runner.run("r1");
  assert.equal(s.counts.VERIFIED, 2, JSON.stringify(s));
  const bossId = h.game.rows("ai")[0].userId;
  const quest = h.game.rows("quest")[0];
  assert.equal(quest.content.objectives[0].opponentAIs[0].ids[0], bossId);
  assert.ok(!JSON.stringify(quest).includes("@ai:"));
});

// ---------------------------------------------------------------- failures that are not ambiguous
test("refused create (success:false) is FAILED, job continues, nothing retried", async () => {
  const h = harness({ game: new FakeGame({ refuse: new Set(["jutsu.create"]) }) });
  h.runner.plan(M.twoCreates, { jobId: "f1" });
  const s = await h.runner.run("f1");
  assert.equal(s.state, "DONE");
  assert.equal(s.items[0].state, "FAILED"); assert.match(s.items[0].error, /refused/);
  assert.equal(s.items[1].state, "VERIFIED");
  assert.equal(h.game.calls.filter((c) => c.path === "jutsu.create").length, 1);
});

test("pre-send validation: an unknown key is FAILED locally before any mutation is sent", async () => {
  const h = harness();
  h.game.seed("jutsu", { id: "j-1", name: "X", hidden: true, effects: [] });
  h.runner.plan({ items: [{ entity: "jutsu", slot: "edit", name: "X", targetId: "j-1", data: { nmae: "typo" } }] }, { jobId: "v1" });
  const s = await h.runner.run("v1");
  assert.equal(s.items[0].state, "FAILED"); assert.match(s.items[0].error, /unknown key "nmae"/);
  assert.ok(!h.game.calls.some((c) => c.path === "jutsu.update"));
});

test("pre-send validation does NOT enforce the 45g power cap (brief section 5)", async () => {
  const h = harness();
  h.game.seed("jutsu", { id: "j-2", name: "X", hidden: true, effects: [] });
  h.runner.plan({ items: [{ entity: "jutsu", slot: "edit", name: "X", targetId: "j-2", data: { effects: [{ type: "damage", power: 400 }] } }] }, { jobId: "p1" });
  const s = await h.runner.run("p1");
  assert.equal(s.items[0].state, "VERIFIED");
  assert.equal(h.game.rows("jutsu")[0].effects[0].power, 400);
});

test("unresolved ref at send time is FAILED, never shipped as a literal (push/16)", async () => {
  const h = harness();
  h.game.seed("quest", { id: "q-9", name: "Q", hidden: true, content: { objectives: [], reward: {}, sceneBackground: "", sceneCharacters: [] } });
  // idmap is empty, and the ref points at nothing in this manifest: planOrder refuses up front
  assert.throws(() => h.runner.plan({ items: [{ entity: "quest", slot: "edit", name: "Q", targetId: "q-9", data: { content: { objectives: [{ id: "o", task: "dialog", x: "@ai:ghost" }] } } }] }, { jobId: "u1" }), /unknown/);
});

// ---------------------------------------------------------------- the crash tests (mandatory)
test("CRASH before send: resume sends exactly once", async () => {
  const h = harness();
  h.runner.plan(M.oneJutsu, { jobId: "c0" });
  const after = h.storage.crash(); // evicted right after planning
  const h2 = harness({ game: h.game, storage: after, idb: h.idb });
  h2.runner.attach("c0", M.oneJutsu);
  const s = await h2.runner.resume("c0");
  assert.equal(s.counts.VERIFIED, 1); assert.equal(h.game.count("jutsu"), 1);
});

test("CRASH after create sent, before response: resume does NOT re-create; reconciliation adopts the one orphan", async () => {
  const game = new FakeGame({ crashAt: 2 }); // getAllNames(1) is the snapshot; jutsu.create(2) is applied server-side, then the tab dies
  const h = harness({ game });
  h.runner.plan(M.oneJutsu, { jobId: "c1" });
  // the runner treats anything thrown inside withSent as ambiguous: it pauses, the item stays SENT
  const s0 = await h.runner.run("c1");
  assert.equal(s0.state, "PAUSED"); assert.equal(s0.pause.reason, "AMBIGUOUS");
  assert.equal(game.count("jutsu"), 1, "the placeholder exists on the server");
  assert.equal(h.journal.get("c1").items[0].state, "SENT");
  // eviction: fresh process over what was flushed
  const after = h.storage.crash();
  const h2 = harness({ game, storage: after, idb: h.idb });
  h2.runner.attach("c1", M.oneJutsu);
  // run() refuses while SENT exists
  await assert.rejects(() => h2.runner.run("c1"), /SENT items/);
  const s = await h2.runner.resume("c1");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.equal(game.count("jutsu"), 1, "NEVER double-created");
  assert.equal(game.calls.filter((c) => c.path === "jutsu.create").length, 1);
  assert.equal(game.rows("jutsu")[0].name, "Ember Step");
});

test("CRASH after response, before journal flush: journal says SENT, reconciliation confirms, no re-create", async () => {
  const game = new FakeGame();
  const h = harness({ game });
  h.runner.plan(M.oneJutsu, { jobId: "c2" });
  // simulate: create applied AND response received, but the process dies before CONFIRMED is flushed.
  // Journal-level: withSent flushed SENT; we take the snapshot there.
  let snap = null;
  const origCall = h.client.call.bind(h.client);
  h.client.call = async (path, input) => { const r = await origCall(path, input); if (path === "jutsu.create") { snap = h.storage.crash(); throw new CrashSignal(0); } return r; };
  const s0 = await h.runner.run("c2");
  assert.equal(s0.state, "PAUSED"); assert.equal(s0.items[0].state, "SENT");
  assert.equal(game.count("jutsu"), 1);
  const h2 = harness({ game, storage: snap, idb: h.idb });
  h2.runner.attach("c2", M.oneJutsu);
  const s = await h2.runner.resume("c2");
  assert.equal(s.counts.VERIFIED, 1); assert.equal(game.count("jutsu"), 1);
  assert.equal(game.calls.filter((c) => c.path === "jutsu.create").length, 1);
});

test("CRASH mid two-phase create (update sent, no response): resume verifies the update landed and never re-creates", async () => {
  const game = new FakeGame({ crashAt: 4 }); // getAllNames(1) create(2) get(3) update(4): update applied, response lost
  const h = harness({ game });
  h.runner.plan(M.oneJutsu, { jobId: "c3" });
  const s0 = await h.runner.run("c3");
  assert.equal(s0.state, "PAUSED");
  const it = h.journal.get("c3").items[0];
  assert.equal(it.state, "SENT"); assert.equal(it.phase, "update"); assert.ok(it.entityId);
  assert.equal(game.rows("jutsu")[0].name, "Ember Step", "the update did land");
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("c3", M.oneJutsu);
  const s = await h2.runner.resume("c3");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.equal(game.count("jutsu"), 1);
  assert.equal(game.calls.filter((c) => c.path === "jutsu.create").length, 1);
  assert.equal(game.calls.filter((c) => c.path === "jutsu.update").length, 1, "the lost-response update was not re-sent either");
});

test("gameAsset ambiguity: two asset creates crashed in SENT -> ambiguous, surfaced as ORPHANED, never guessed", async () => {
  const game = new FakeGame();
  const two = { items: [
    { entity: "asset", slot: "create", name: "A", srcId: "a", data: { name: "A", hidden: true, type: "STATIC", url: "u" } },
    { entity: "asset", slot: "create", name: "B", srcId: "b", data: { name: "B", hidden: true, type: "STATIC", url: "u" } },
  ] };
  const h = harness({ game });
  h.runner.plan(two, { jobId: "g1" });
  // the snapshot the runner would take before the first asset create
  const snapKey = await h.runner.reconciler.beforeCreate(h.journal.get("g1"), h.journal.get("g1").items[0], "asset");
  h.journal.annotate("g1", 0, { snapshotKey: snapKey }); h.journal.annotate("g1", 1, { snapshotKey: snapKey });
  // force both items into SENT with two placeholders on the server (the worst case: both requests
  // left, neither response was seen)
  await h.journal.withSent("g1", 0, { phase: "create" }, async () => { game.handle("gameAsset.create"); });
  await h.journal.withSent("g1", 1, { phase: "create" }, async () => { game.handle("gameAsset.create"); });
  assert.equal(game.count("asset"), 2);
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("g1", two);
  const s = await h2.runner.resume("g1");
  assert.equal(s.items[0].state, "ORPHANED"); assert.equal(s.items[1].state, "ORPHANED");
  assert.equal(h2.journal.get("g1").items[0].candidates.length, 2, "both Placeholder rows listed as candidates");
  assert.match(h2.journal.get("g1").items[0].error, /2 new asset row/);
  assert.equal(game.count("asset"), 2, "no new creates, no deletes");
  // the user adopts explicitly, then the job continues at update
  const ids = game.rows("asset").map((r) => r.id);
  h2.runner.adopt("g1", 0, ids[0]); h2.runner.adopt("g1", 1, ids[1]);
  const s2 = await h2.runner.run("g1");
  assert.equal(s2.counts.VERIFIED, 2, JSON.stringify(s2));
  assert.equal(game.count("asset"), 2);
});

// ---------------------------------------------------------------- pauses
test("TOO_MANY_REQUESTS on a read pauses the job with path and countdown; nothing is retried", async () => {
  const game = new FakeGame({ limitPath: "jutsu.get" });
  const h = harness({ game });
  h.runner.plan(M.oneJutsu, { jobId: "l1" });
  const s = await h.runner.run("l1");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "TOO_MANY_REQUESTS"); assert.equal(s.pause.path, "jutsu.get");
  assert.ok(s.pause.until > h.clock());
  assert.equal(game.calls.filter((c) => c.path === "jutsu.get").length, 1);
  // the create landed and is CONFIRMED; the item waits at the update phase
  assert.equal(s.items[0].state, "CONFIRMED"); assert.equal(s.items[0].phase, "update");
  // run() while tripped stays paused without sending
  const before = game.calls.length;
  const s2 = await h.runner.run("l1");
  assert.equal(s2.state, "PAUSED"); assert.equal(game.calls.length, before);
});

test("a NetworkError inside withSent leaves the item SENT and pauses the job (ambiguous, not failed)", async () => {
  const h = harness();
  h.runner.plan(M.oneJutsu, { jobId: "n1" });
  const { NetworkError } = await import("../src/transport/client.mjs");
  h.client.call = async () => { throw new NetworkError(new TypeError("Failed to fetch"), { paths: ["jutsu.create"], kind: "mutation" }); };
  const s = await h.runner.run("n1");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "NETWORK");
  assert.equal(s.items[0].state, "SENT");
});
