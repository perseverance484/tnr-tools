// Repository text must be isolated from the game capture cache, and the isolation has to survive
// a rollback: an operator on the previous released bundle must still be able to open the capture
// and journal state that bundle understands.
import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { RepoTextCache, REPO_DB_NAME, REPO_DB_VERSION } from "../src/storage/repotext.mjs";
import { CaptureCache, DB_NAME, DB_VERSION } from "../src/storage/captures.mjs";
import { composeForTest } from "./compose.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { FakeGame } from "./fakegame.mjs";

test("repository text uses its own database, not the capture DB", () => {
  assert.notEqual(REPO_DB_NAME, DB_NAME);
  assert.equal(REPO_DB_NAME, "tnr_forge_repo");
  assert.equal(REPO_DB_VERSION, 1);
});

test("the capture DB version is NOT bumped to hold repository text", () => {
  // The released bundle understands tnr_forge at this version. Raising it to add a manifest store
  // would make a rollback unable to open the operator's journal and captures.
  assert.equal(DB_VERSION, 2, "tnr_forge version changed; a rollback would be unable to open it");
});

test("round-trips text and reports its own size", async () => {
  const idb = new IDBFactory();
  const cache = new RepoTextCache(idb, fakeClock());
  assert.equal(await cache.get("github.contents", "missing"), null);
  await cache.put({ path: "github.contents", id: "gh:push/45.json@abc", data: "{\"items\":[]}" });
  const hit = await cache.get("github.contents", "gh:push/45.json@abc");
  assert.equal(hit.data, "{\"items\":[]}");
  assert.equal((await cache.size()).count, 1);
  await cache.clear();
  assert.equal((await cache.size()).count, 0);
});

test("loading the picker writes manifest text to the repo DB and leaves the capture DB alone", async () => {
  const idb = new IDBFactory();
  const storage = new MemoryStorage();
  const d = composeForTest({ game: new FakeGame(), storage, idb, clock: fakeClock() });
  d.github = {
    list: async () => [{ name: "45_x.json", path: "push/45_x.json", sha: "sha1", size: 1, type: "file" }],
    text: async () => "{\"items\":[]}",
    put: async () => ({ sha: "x" }),
  };
  const { ForgeCore } = await import("../src/core/core.mjs");
  const core = new ForgeCore({ version: "t", storage, now: d.clock, ...d });
  await core.loadPicker(true);

  const repo = new RepoTextCache(idb, d.clock);
  assert.equal((await repo.size()).count, 1, "manifest text belongs in the repo DB");

  const captures = new CaptureCache(idb, d.clock);
  assert.equal(await captures.get("github.contents", "gh:push/45_x.json@sha1"), null,
    "repository text must not appear in the game capture cache");
});

test("a rolled-back bundle can still open the capture DB at the version it knows", async () => {
  const idb = new IDBFactory();
  // current code writes both databases
  const repo = new RepoTextCache(idb, fakeClock());
  await repo.put({ path: "github.contents", id: "k", data: "text" });
  const cache = new CaptureCache(idb, fakeClock());
  await cache.put({ path: "jutsu.get", id: "1", input: null, data: { name: "x" } });

  // the previous bundle opens tnr_forge at DB_VERSION and never opens the repo DB
  const reopened = await new Promise((resolve, reject) => {
    const req = idb.open(DB_NAME, DB_VERSION);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
    req.onblocked = () => reject(new Error("blocked"));
  });
  assert.equal(reopened.version, DB_VERSION, "rollback must not meet a newer capture DB");
  reopened.close();
});
