// Verified asset bytes live in their own database, keyed by their own digest.
//
// Two properties, both of which a reviewer should be able to check in one read: the database is
// SEPARATE (so a rolled-back bundle can still open the journal it understands), and the key IS the
// content (so a hit can never be bytes nobody asked for).
import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { AssetCache, ASSET_DB_NAME, ASSET_DB_VERSION, ASSET_UPLOADS_KEY, MAX_ASSET_BYTES, readAssetUploads, recordAssetUpload } from "../src/storage/assets.mjs";
import { REPO_DB_NAME } from "../src/storage/repotext.mjs";
import { DB_NAME, DB_VERSION } from "../src/storage/captures.mjs";
import { IDMAP_KEY } from "../src/storage/compat.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";

const SHA = "a".repeat(64);
const bytes = (n, fill = 1) => new Uint8Array(n).fill(fill).buffer;

test("asset bytes use a third database, distinct from the capture and repository stores", () => {
  assert.equal(ASSET_DB_NAME, "tnr_forge_assets");
  assert.equal(ASSET_DB_VERSION, 1);
  assert.equal(new Set([ASSET_DB_NAME, REPO_DB_NAME, DB_NAME]).size, 3);
  // The capture DB version must not move to hold asset bytes: that is a one-way door for a rollback.
  assert.equal(DB_VERSION, 2, "tnr_forge version changed; a rollback would be unable to open it");
});

test("round-trips bytes under their digest and reports its own size", async () => {
  const cache = new AssetCache(new IDBFactory(), fakeClock());
  assert.equal(await cache.get(SHA), null);
  await cache.put({ sha256: SHA, bytes: bytes(1000), path: "art/a.webp", ref: "c".repeat(40) });
  const hit = await cache.get(SHA);
  assert.equal(hit.sha256, SHA);
  assert.equal(hit.size, 1000);
  assert.equal(hit.bytes.byteLength, 1000);
  assert.equal(hit.path, "art/a.webp", "the path rides along as provenance");
  assert.equal(hit.ref, "c".repeat(40));
  assert.deepEqual(await cache.size(), { count: 1, bytes: 1000 });

  await cache.delete(SHA);
  assert.equal(await cache.get(SHA), null);
  assert.deepEqual(await cache.size(), { count: 0, bytes: 0 });
});

test("THE KEY IS THE DIGEST: re-putting the same content under a new path replaces one entry", async () => {
  const cache = new AssetCache(new IDBFactory(), fakeClock());
  await cache.put({ sha256: SHA, bytes: bytes(64), path: "art/one.webp", ref: "c".repeat(40) });
  await cache.put({ sha256: SHA, bytes: bytes(64), path: "art/two.webp", ref: "d".repeat(40) });
  assert.deepEqual(await cache.size(), { count: 1, bytes: 64 }, "one blob is one entry however many paths hold it");
  assert.equal((await cache.get(SHA)).path, "art/two.webp");
  await cache.clear();
  assert.deepEqual(await cache.size(), { count: 0, bytes: 0 });
});

test("an asset larger than any upload ceiling could accept is refused rather than stored", async () => {
  const cache = new AssetCache(new IDBFactory(), fakeClock());
  await assert.rejects(() => cache.put({ sha256: SHA, bytes: bytes(MAX_ASSET_BYTES + 1) }), /over the \d+-byte cache limit/);
  assert.deepEqual(await cache.size(), { count: 0, bytes: 0 });
});

test("the upload ledger is keyed by content and is NOT the builder's name-keyed idmap", () => {
  assert.notEqual(ASSET_UPLOADS_KEY, IDMAP_KEY);
  const storage = new MemoryStorage();
  assert.deepEqual(readAssetUploads(storage), {});
  recordAssetUpload(storage, SHA, "https://utfs.io/f/x", { path: "art/a.webp", ref: "c".repeat(40), at: 7 });
  assert.deepEqual(readAssetUploads(storage), { [SHA]: { url: "https://utfs.io/f/x", at: 7, path: "art/a.webp", ref: "c".repeat(40) } });
  assert.equal(storage.getItem(IDMAP_KEY), null, "recording an upload must not touch the shared idmap");

  // unreadable content is treated as empty rather than thrown, so one bad write cannot wedge a run
  storage.setItem(ASSET_UPLOADS_KEY, "not json");
  assert.deepEqual(readAssetUploads(storage), {});
  storage.setItem(ASSET_UPLOADS_KEY, "[1,2]");
  assert.deepEqual(readAssetUploads(storage), {});
});
