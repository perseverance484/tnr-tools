import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { CaptureCache, captureKey, snapshotKey, entityOfPath, DB_NAME, STORE, DB_VERSION, FULL_PERSIST_PATHS, canPersistFull, persistProcedureKind, MAX_FULL_CAPTURE_BYTES } from "../src/storage/captures.mjs";
import { PROCEDURES } from "../src/transport/procedures.mjs";
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

// ------------------------------------------------------------------ full persistence boundary
test("every full-persistence path is an audited content-record point read, and nothing else is", () => {
  for (const path of FULL_PERSIST_PATHS) {
    const p = PROCEDURES[path];
    assert.ok(p, `${path} is not in the audited crud surface; the allowlist may not invent a procedure`);
    assert.equal(p.kind, "query", `${path} is not a query; a mutation body may never be durably persisted`);
    assert.ok(/\.(get|getAi|getAiProfile)$/.test(path), `${path} is not a point read`);
    assert.ok(!/getAll/.test(path), `${path} is a list procedure`);
    assert.equal(canPersistFull(path), true);
    assert.equal(persistProcedureKind(path), "query");
  }
  // the closed half of the boundary: nothing else in the audited surface is persistable
  for (const path of Object.keys(PROCEDURES)) {
    if (FULL_PERSIST_PATHS.includes(path)) continue;
    assert.equal(canPersistFull(path), false, `${path} must not be persistable without a reviewed change`);
  }
  assert.equal(canPersistFull("asset.get"), false, "the un-audited asset.get alias is not a way in");
  assert.equal(canPersistFull("anything.else"), false);
  assert.equal(persistProcedureKind("asset.get"), null);
});

test("the full-capture ceiling is a named constant with room for the worst real record", () => {
  assert.equal(MAX_FULL_CAPTURE_BYTES, 512 * 1024);
  // the largest content record in this repository's own committed captures is a ~71 KB quest
  assert.ok(MAX_FULL_CAPTURE_BYTES > 71_000 * 5, "the ceiling must not be tight enough to reject real records");
});

// ------------------------------------------------------------------ immutable snapshots
test("snapshot keys name a capture occurrence, not a record", () => {
  assert.equal(snapshotKey("45-abc", "before", 0), "45-abc::before::0");
  assert.equal(snapshotKey("45-abc", "after", 3), "45-abc::after::3");
  // two captures of ONE record are two snapshots; that is the whole point (review FFC-1)
  assert.notEqual(snapshotKey("j", "before", 0), snapshotKey("j", "after", 0));
  assert.notEqual(snapshotKey("j", "after", 0), snapshotKey("j", "after", 1));
  assert.notEqual(snapshotKey("j1", "after", 0), snapshotKey("j2", "after", 0));
});

test("cache invalidation never touches capture snapshots", async () => {
  const c = fresh();
  const body = { id: "a1", name: "Before", image: "old.webp" };
  await c.put({ path: "gameAsset.get", id: "a1", input: { id: "a1" }, data: body });
  await c.putSnapshot({ key: snapshotKey("job", "before", 0), jobId: "job", phase: "before", ordinal: 0, path: "gameAsset.get", id: "a1", input: { id: "a1" }, data: body });

  // the write path, exactly as the runner drives it for an asset update
  await c.invalidateRecord("asset", "a1");
  assert.equal(await c.get("gameAsset.get", "a1"), null, "the read cache slot is gone, as it must be");
  assert.deepEqual((await c.getSnapshot(snapshotKey("job", "before", 0))).data, body, "the evidence is not");

  // and the blunter instrument, and the cache-wide clear
  await c.invalidateEntity("asset");
  await c.clear();
  assert.deepEqual((await c.getSnapshot(snapshotKey("job", "before", 0))).data, body);
  assert.equal((await c.listSnapshots()).length, 1);
  assert.deepEqual(await c.list(), [], "while the read cache really was cleared");
  c.close();
});

test("a later read of the same record cannot overwrite an earlier snapshot", async () => {
  const c = fresh();
  const first = { id: "a1", name: "First" };
  const second = { id: "a1", name: "Second" };
  const base = { jobId: "job", path: "gameAsset.get", id: "a1", input: { id: "a1" } };
  await c.putSnapshot({ ...base, key: snapshotKey("job", "after", 0), phase: "after", ordinal: 0, data: first });
  await c.put({ path: "gameAsset.get", id: "a1", input: { id: "a1" }, data: first });
  await c.putSnapshot({ ...base, key: snapshotKey("job", "after", 1), phase: "after", ordinal: 1, data: second });
  await c.put({ path: "gameAsset.get", id: "a1", input: { id: "a1" }, data: second }); // the cache slot moves on

  assert.equal((await c.getSnapshot(snapshotKey("job", "after", 0))).data.name, "First");
  assert.equal((await c.getSnapshot(snapshotKey("job", "after", 1))).data.name, "Second");
  assert.equal((await c.get("gameAsset.get", "a1")).data.name, "Second", "one cache slot, newest body");
  c.close();
});

test("snapshots record their own provenance and are listed and dropped by job", async () => {
  const c = fresh();
  const put = (jobId, phase, ordinal, id, data) => c.putSnapshot({ key: snapshotKey(jobId, phase, ordinal), jobId, phase, ordinal, path: "gameAsset.get", id, input: { id }, data });
  await put("j1", "after", 0, "a1", { id: "a1" });
  await put("j1", "after", 1, "a2", { id: "a2" });
  await put("j2", "before", 0, "a3", { id: "a3" });

  const recs = await c.listSnapshots();
  assert.equal(recs.length, 3);
  const one = recs.find((r) => r.key === snapshotKey("j1", "after", 0));
  assert.equal(one.entity, "asset");
  assert.equal(one.path, "gameAsset.get");
  assert.equal(one.id, "a1");
  assert.equal(one.phase, "after");
  assert.ok(one.bytes > 0 && typeof one.at === "string");
  assert.ok(!("data" in one), "listing is metadata; bodies are fetched one at a time");

  assert.equal(await c.deleteSnapshotsForJob("j1"), 2);
  assert.deepEqual((await c.listSnapshots()).map((r) => r.jobId), ["j2"]);
  await c.clearSnapshots();
  assert.deepEqual(await c.listSnapshots(), []);
  c.close();
});

test("the database upgrades a v1 cache in place and keeps its records", async () => {
  assert.equal(DB_VERSION, 2, "the snapshot store arrived with a version bump, not a silent schema change");
  const idb = new IDBFactory();
  // a store shaped like the shipped v1 database, opened at v1 with no snapshot store
  const req = idb.open(DB_NAME, 1);
  await new Promise((resolve, reject) => {
    req.onupgradeneeded = () => {
      const store = req.result.createObjectStore(STORE, { keyPath: "key" });
      store.createIndex("entity", "entity", { unique: false });
      store.createIndex("path", "path", { unique: false });
    };
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
  const v1 = req.result;
  await new Promise((resolve, reject) => {
    const tx = v1.transaction(STORE, "readwrite");
    tx.objectStore(STORE).put({ key: "jutsu.get:j1", path: "jutsu.get", id: "j1", entity: "jutsu", input: { id: "j1" }, data: { id: "j1", name: "Old" }, at: "2026-01-01T00:00:00.000Z", bytes: 26 });
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
  v1.close();

  const c = new CaptureCache(idb, fakeClock());
  assert.deepEqual((await c.get("jutsu.get", "j1")).data, { id: "j1", name: "Old" }, "the v1 cache survives the upgrade");
  await c.putSnapshot({ key: snapshotKey("j", "after", 0), jobId: "j", phase: "after", ordinal: 0, path: "jutsu.get", id: "j1", input: { id: "j1" }, data: { id: "j1", name: "New" } });
  assert.equal((await c.getSnapshot(snapshotKey("j", "after", 0))).data.name, "New", "and the new store exists after it");
  c.close();
});
