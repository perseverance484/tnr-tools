import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { Reconciler, SNAP_PREFIX } from "../src/reconcile/reconciler.mjs";
import { Journal } from "../src/storage/journal.mjs";
import { CaptureCache } from "../src/storage/captures.mjs";
import { Budget } from "../src/budget/bucket.mjs";
import { CachedReader } from "../src/budget/reader.mjs";
import { FakeGame, FakeClient } from "./fakegame.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";

function mk(game = new FakeGame()) {
  const storage = new MemoryStorage(); const clock = fakeClock();
  const journal = new Journal(storage, clock);
  const cache = new CaptureCache(new IDBFactory(), clock);
  const budget = new Budget({ storage, clock, sleep: async (ms) => clock.tick(ms) });
  const reader = new CachedReader({ client: new FakeClient(game), cache, budget });
  const rec = new Reconciler({ storage, reader, clock });
  return { game, storage, clock, journal, cache, budget, reader, rec };
}
const specs = (entity, n) => Array.from({ length: n }, (_, i) => ({ entity, op: "create", name: `${entity}${i}`, srcId: `${entity}${i}`, payloadHash: "h" }));

test("beforeCreate snapshots once per (job, entity), synchronously, keyed on the item", async () => {
  const { game, storage, journal, rec, budget } = mk();
  game.seed("jutsu", { id: "old-1", name: "Existing" });
  journal.open({ jobId: "j", items: specs("jutsu", 2) });
  const job = journal.get("j");
  const k1 = await rec.beforeCreate(job, job.items[0], "jutsu");
  assert.equal(k1, SNAP_PREFIX + "j:jutsu");
  const snap = JSON.parse(storage.getItem(k1));
  assert.deepEqual(snap.ids, ["old-1"]); assert.equal(snap.path, "jutsu.getAllNames");
  const calls = game.calls.length;
  const k2 = await rec.beforeCreate(job, job.items[1], "jutsu");
  assert.equal(k2, k1); assert.equal(game.calls.length, calls, "second create of the same type does not re-snapshot");
  assert.equal(budget.available("jutsu.getAllNames"), 29, "one limited token spent");
});

test("create: exactly one new id and one pending SENT -> adopt; name cross-check recorded", async () => {
  const { game, journal, rec } = mk();
  game.seed("jutsu", { id: "old-1", name: "Existing" });
  journal.open({ jobId: "j", items: specs("jutsu", 1) });
  await rec.beforeCreate(journal.get("j"), journal.get("j").items[0], "jutsu");
  journal.transition("j", 0, "SENT", { phase: "create" });
  game.handle("jutsu.create"); // the request left and applied; response lost
  const r = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], {});
  assert.equal(r.action, "confirm"); assert.equal(r.phase, "update");
  assert.equal(r.entityId, game.rows("jutsu").find((x) => x.id !== "old-1").id);
  assert.match(r.note, /adopted/); assert.ok(!/check it/.test(r.note));
});

test("create: rows that existed before the snapshot are never adopted (cross-job noise)", async () => {
  const { game, journal, rec } = mk();
  game.handle("jutsu.create"); // a stale placeholder from some earlier session, present BEFORE our snapshot
  journal.open({ jobId: "j", items: specs("jutsu", 1) });
  await rec.beforeCreate(journal.get("j"), journal.get("j").items[0], "jutsu");
  journal.transition("j", 0, "SENT", { phase: "create" });
  // our request never actually left (nothing new on the server)
  const r = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], {});
  assert.equal(r.action, "orphan"); assert.deepEqual(r.candidates, []); assert.match(r.note, /0 new/);
});

test("create: ids this job already confirmed are subtracted before deciding", async () => {
  const { game, journal, rec } = mk();
  journal.open({ jobId: "j", items: specs("asset", 2) });
  const job = journal.get("j");
  await rec.beforeCreate(job, job.items[0], "asset");
  // item 0 created and confirmed normally
  const a = game.handle("gameAsset.create").data.message;
  journal.transition("j", 0, "SENT", { phase: "create" }); journal.transition("j", 0, "CONFIRMED", { entityId: a, phase: "update" });
  // item 1 sent, applied, response lost
  journal.transition("j", 1, "SENT", { phase: "create" });
  const b = game.handle("gameAsset.create").data.message;
  const r = await rec.resolveSent(journal.get("j"), journal.get("j").items[1], {});
  assert.equal(r.action, "confirm"); assert.equal(r.entityId, b);
});

test("gameAsset: two pending, two new 'Placeholder' rows -> ambiguous, candidates listed, nothing adopted", async () => {
  const { game, journal, rec } = mk();
  journal.open({ jobId: "j", items: specs("asset", 2) });
  const job = journal.get("j");
  await rec.beforeCreate(job, job.items[0], "asset");
  journal.transition("j", 0, "SENT", { phase: "create" }); journal.transition("j", 1, "SENT", { phase: "create" });
  game.handle("gameAsset.create"); game.handle("gameAsset.create");
  const r0 = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], {});
  assert.equal(r0.action, "orphan"); assert.equal(r0.candidates.length, 2);
  assert.ok(r0.candidates.every((c) => c.name === "Placeholder"));
  assert.match(r0.note, /2 new asset row\(s\).*2 create\(s\) pending/);
  assert.equal(game.count("asset"), 2);
});

test("create with no snapshot -> orphan, never a guess", async () => {
  const { game, journal, rec } = mk();
  journal.open({ jobId: "j", items: specs("quest", 1) });
  journal.transition("j", 0, "SENT", { phase: "create" });
  game.handle("quests.create");
  const r = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], {});
  assert.equal(r.action, "orphan"); assert.match(r.note, /no pre-create snapshot/);
});

test("update: asserted keys already match live -> landed (verify next, no re-send); differ -> orphan", async () => {
  const { game, journal, rec } = mk();
  game.seed("quest", { id: "q", name: "Renamed", description: "d", content: { objectives: [] } });
  journal.open({ jobId: "j", items: [{ entity: "quest", op: "update", name: "Q", targetId: "q", payloadHash: "h" }] });
  journal.transition("j", 0, "SENT", { phase: "update" });
  const landed = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], { planned: { data: { name: "Renamed" } } });
  assert.equal(landed.action, "confirm"); assert.equal(landed.landed, true); assert.equal(landed.phase, "verify");
  const not = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], { planned: { data: { name: "Other" } } });
  assert.equal(not.action, "orphan"); assert.match(not.note, /live differs on name/);
});

test("rules-toggle and rules phases resolve from the profile row", async () => {
  const { game, journal, rec } = mk();
  const ai = game.seed("ai", { userId: "u1", username: "X", isAi: true, aiProfileId: null, jutsus: [], items: [] });
  journal.open({ jobId: "j", items: [{ entity: "ai", op: "update", name: "X", targetId: "u1", payloadHash: "h" }] });
  journal.transition("j", 0, "SENT", { phase: "rules-toggle", entityId: "u1" });
  let r = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], {});
  assert.equal(r.action, "orphan"); // toggle never applied
  game.handle("ai.toggleAiProfile", { aiId: "u1" });
  r = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], {});
  assert.equal(r.action, "confirm"); assert.equal(r.phase, "rules");
  journal.transition("j", 0, "CONFIRMED", { phase: "rules" });
  journal.transition("j", 0, "SENT", { phase: "rules", aiProfileId: ai.aiProfileId });
  const rules = [{ conditions: [], action: { type: "end_turn" } }];
  r = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], { planned: { data: { rules } } });
  assert.equal(r.action, "orphan");
  game.handle("ai.updateAiProfile", { id: ai.aiProfileId, rules, includeDefaultRules: false });
  r = await rec.resolveSent(journal.get("j"), journal.get("j").items[0], { planned: { data: { rules } } });
  assert.equal(r.action, "confirm"); assert.equal(r.landed, true);
});

test("forget drops a job's snapshots and nothing else", async () => {
  const { game, storage, journal, rec } = mk();
  journal.open({ jobId: "a", items: specs("jutsu", 1) }); journal.open({ jobId: "b", items: specs("jutsu", 1) });
  await rec.beforeCreate(journal.get("a"), journal.get("a").items[0], "jutsu");
  await rec.beforeCreate(journal.get("b"), journal.get("b").items[0], "jutsu");
  assert.equal(rec.forget("a"), 1);
  assert.equal(storage.getItem(SNAP_PREFIX + "a:jutsu"), null);
  assert.ok(storage.getItem(SNAP_PREFIX + "b:jutsu"));
  assert.ok(journal.get("a"));
});
