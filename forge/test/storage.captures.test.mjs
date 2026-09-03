import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { CaptureCache, captureKey, entityOfPath } from "../src/storage/captures.mjs";
import { fakeClock } from "./shim.mjs";

const fresh = () => new CaptureCache(new IDBFactory(), fakeClock());

test("key and entity mapping", () => {
  assert.equal(captureKey("jutsu.get", "abc"), "jutsu.get:abc");
  assert.equal(captureKey("jutsu.getAllNames"), "jutsu.getAllNames:");
  assert.equal(entityOfPath("gameAsset.get"), "asset");
  assert.equal(entityOfPath("profile.getAi"), "ai");
  assert.equal(entityOfPath("ai.getAiProfile"), "ai");
  assert.equal(entityOfPath("quests.getAllNames"), "quest");
});

test("put/get round-trip keeps decoded data and stamps at/bytes", async () => {
  const c = fresh();
  await c.put({ path: "jutsu.get", id: "j1", input: { id: "j1" }, data: { id: "j1", name: "X", createdAt: "2026-09-01T00:00:00.000Z" } });
  const r = await c.get("jutsu.get", "j1");
  assert.equal(r.entity, "jutsu");
  assert.equal(r.data.name, "X");
  assert.ok(r.at.endsWith("Z"));
  assert.ok(r.bytes > 0);
  assert.equal(await c.get("jutsu.get", "nope"), null);
});

test("invalidateRecord drops the record's gets AND the entity's list captures, leaves others", async () => {
  const c = fresh();
  await c.put({ path: "jutsu.get", id: "j1", data: {} });
  await c.put({ path: "jutsu.get", id: "j2", data: {} });
  await c.put({ path: "jutsu.getAllNames", data: [] });
  await c.put({ path: "item.get", id: "i1", data: {} });
  const n = await c.invalidateRecord("jutsu", "j1");
  assert.equal(n, 2); // j1 + the list
  assert.equal(await c.get("jutsu.get", "j1"), null);
  assert.ok(await c.get("jutsu.get", "j2"));
  assert.equal(await c.get("jutsu.getAllNames"), null);
  assert.ok(await c.get("item.get", "i1"));
});

test("invalidateEntity drops everything for the entity across routers (profile + ai are both 'ai')", async () => {
  const c = fresh();
  await c.put({ path: "profile.getAi", id: "u1", data: {} });
  await c.put({ path: "ai.getAiProfile", id: "p1", data: {} });
  await c.put({ path: "profile.getAllAiNames", data: [] });
  await c.put({ path: "jutsu.get", id: "j1", data: {} });
  assert.equal(await c.invalidateEntity("ai"), 3);
  assert.equal((await c.list()).length, 1);
});

test("list and size", async () => {
  const c = fresh();
  await c.put({ path: "quests.get", id: "q1", data: { a: 1 } });
  await c.put({ path: "quests.get", id: "q2", data: { b: 22 } });
  const l = await c.list();
  assert.equal(l.length, 2);
  assert.ok(l.every((r) => r.key && r.at && !("data" in r)));
  const sz = await c.size();
  assert.equal(sz.count, 2);
  assert.ok(sz.bytes > 0);
  await c.clear();
  assert.equal((await c.size()).count, 0);
});

test("reopen after close sees the same data (persistence across app restarts)", async () => {
  const idb = new IDBFactory();
  const c1 = new CaptureCache(idb, fakeClock());
  await c1.put({ path: "bloodline.get", id: "b1", data: { x: 1 } });
  c1.close();
  const c2 = new CaptureCache(idb, fakeClock());
  assert.equal((await c2.get("bloodline.get", "b1")).data.x, 1);
});
