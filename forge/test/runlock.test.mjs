// The run lock (RUL-2026-11-07-133): one game writer per account at a time.
import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { parseLock, lockState, blockReason, claimBody, releaseBody, LOCK_PATH } from "../src/runner/runlock.mjs";
import { ForgeCore } from "../src/core/core.mjs";
import { composeForTest } from "./compose.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { FakeGame } from "./fakegame.mjs";

const TOOL = join(dirname(fileURLToPath(import.meta.url)), "..", "tools", "run_lock.mjs");
const T0 = Date.parse("2026-11-07T06:00:00Z");
const held = (holder, minutes, job = "push/502") => claimBody({ holder, job, ttlMinutes: minutes, now: T0 });

test("parseLock: missing or empty is free; junk and a held lock without expiry are refused", () => {
  assert.equal(parseLock(null).holder, null);
  assert.equal(parseLock("  ").holder, null);
  assert.throws(() => parseLock("{"), /not JSON/);
  assert.throws(() => parseLock("[]"), /not an object/);
  assert.throws(() => parseLock(JSON.stringify({ holder: "duet" })), /expiresAt/);
  assert.throws(() => parseLock(JSON.stringify({ holder: "", expiresAt: new Date(T0).toISOString() })), /holder/);
});

test("lockState: held until expiresAt, then expired and free to take", () => {
  const l = held("duet", 30);
  assert.deepEqual(lockState(l, T0 + 10 * 60000), { held: true, holder: "duet", expired: false, minutesLeft: 20 });
  assert.equal(lockState(l, T0 + 30 * 60000).held, false);
  assert.equal(lockState(l, T0 + 31 * 60000).expired, true);
  assert.equal(lockState(releaseBody({ holder: "duet", now: T0 }), T0).held, false);
});

test("blockReason: the browser runs only while nobody holds it; a claimer runs only while it holds it", () => {
  const l = held("duet", 30);
  assert.match(blockReason(l, null, T0), /held by duet \(push\/502\)/);
  assert.equal(blockReason(l, null, T0 + 31 * 60000), null, "expired: the browser may run");
  assert.equal(blockReason(l, "duet", T0), null);
  assert.match(blockReason(l, "claude", T0), /held by duet/);
  assert.match(blockReason({ holder: null }, "claude", T0), /has not claimed/);
  assert.equal(blockReason({ holder: null }, null, T0), null);
});

test("claimBody: a heartbeat by the holder keeps claimedAt and moves expiresAt", () => {
  const first = held("claude", 60);
  const beat = claimBody({ holder: "claude", ttlMinutes: 60, now: T0 + 15 * 60000, prev: first });
  assert.equal(beat.claimedAt, first.claimedAt);
  assert.equal(beat.job, "push/502");
  assert.equal(Date.parse(beat.expiresAt), T0 + 75 * 60000);
  assert.throws(() => claimBody({ holder: "", now: T0 }), /holder/);
});

// ------------------------------------------------------------------ the git compare-and-swap
function git(cwd, ...args) { return execFileSync("git", args, { cwd, encoding: "utf8", stdio: ["pipe", "pipe", "pipe"] }); }

function sandbox() {
  const root = mkdtempSync(join(tmpdir(), "runlock-test-"));
  const remote = join(root, "remote.git");
  git(root, "init", "-q", "--bare", "-b", "main", remote);
  const seed = join(root, "seed");
  git(root, "clone", "-q", remote, seed);
  git(seed, "config", "user.email", "t@t"); git(seed, "config", "user.name", "t");
  writeFileSync(join(seed, "README"), "x\n");
  git(seed, "add", "README"); git(seed, "commit", "-q", "-m", "seed"); git(seed, "push", "-q", "origin", "HEAD:main");
  const clone = (name) => {
    const d = join(root, name);
    git(root, "clone", "-q", remote, d);
    git(d, "config", "user.email", `${name}@t`); git(d, "config", "user.name", name);
    return d;
  };
  return { root, remote, clone, done: () => rmSync(root, { recursive: true, force: true }) };
}

function lockTool(repo, ...args) {
  return new Promise((res) => {
    const p = spawn(process.execPath, [TOOL, ...args], { env: { ...process.env, RUN_LOCK_REPO: repo } });
    let out = ""; p.stdout.on("data", (b) => { out += b; });
    p.on("close", (code) => res({ code, out: JSON.parse(out.trim().split("\n").pop()) }));
  });
}

test("run_lock.mjs: claim, refuse a second holder, release only by the holder, then claim again", async () => {
  const sb = sandbox();
  try {
    const a = sb.clone("a"), b = sb.clone("b");
    assert.equal((await lockTool(a, "status")).out.held, false);
    const c1 = await lockTool(a, "claim", "--holder", "claude", "--job", "push/502", "--ttl", "30");
    assert.equal(c1.code, 0); assert.equal(c1.out.type, "claimed");
    const c2 = await lockTool(b, "claim", "--holder", "duet", "--job", "scan");
    assert.equal(c2.code, 4); assert.match(c2.out.text, /held by claude \(push\/502\)/);
    const r1 = await lockTool(b, "release", "--holder", "duet");
    assert.equal(r1.code, 4);
    const hb = await lockTool(b, "heartbeat", "--holder", "claude", "--ttl", "45");
    assert.equal(hb.code, 0, "a heartbeat works from any checkout of the holder");
    const r2 = await lockTool(a, "release", "--holder", "claude");
    assert.equal(r2.code, 0); assert.equal(r2.out.type, "released");
    const c3 = await lockTool(b, "claim", "--holder", "duet", "--job", "scan");
    assert.equal(c3.code, 0);
    // Each write is one commit touching only the lock file, on top of whatever main was.
    git(a, "fetch", "-q", "origin", "main");
    assert.equal(git(a, "show", "--name-only", "--format=", "FETCH_HEAD").trim(), LOCK_PATH);
    assert.match(git(a, "log", "-1", "--format=%s", "FETCH_HEAD"), /run-lock: claim by duet \(scan\)/);
    assert.equal(git(a, "show", "FETCH_HEAD:README"), "x\n", "the rest of main is untouched");
  } finally { sb.done(); }
});

test("run_lock.mjs: two simultaneous claims, exactly one wins", async () => {
  const sb = sandbox();
  try {
    const a = sb.clone("a"), b = sb.clone("b");
    const [x, y] = await Promise.all([
      lockTool(a, "claim", "--holder", "claude", "--job", "j1"),
      lockTool(b, "claim", "--holder", "duet", "--job", "j2"),
    ]);
    assert.deepEqual([x.code, y.code].sort(), [0, 4]);
  } finally { sb.done(); }
});

// ------------------------------------------------------------------ the browser gate
const MANIFEST = JSON.stringify({ items: [{ entity: "jutsu", slot: "create", name: "Lock A", srcId: "lk-a", data: { name: "Lock A", hidden: true } }] });
const ENTRY = { name: "46_lock.json", path: "push/46_lock.json", sha: "lk", size: 64, type: "file" };

function browserCore(lockText) {
  const storage = new MemoryStorage();
  const clock = fakeClock();
  const game = new FakeGame();
  const d = composeForTest({ game, storage, idb: new IDBFactory(), clock });
  d.github = {
    list: async () => [ENTRY],
    text: async (path) => {
      if (path === LOCK_PATH) {
        if (lockText === 404) { const e = new Error("HTTP 404"); e.status = 404; throw e; }
        if (lockText === 500) { const e = new Error("HTTP 500"); e.status = 500; throw e; }
        return lockText;
      }
      return MANIFEST;
    },
    put: async () => ({ sha: "s" }),
  };
  const core = new ForgeCore({ version: "test", storage, ...d });
  const said = [];
  core.subscribe((n) => { if (n.type === "message") said.push(n); });
  return { core, game, said, clock };
}

test("browser Forge: Start is refused while another runner holds the lock, and nothing is sent", async () => {
  const lock = JSON.stringify(claimBody({ holder: "duet", job: "push/509", ttlMinutes: 600, now: Date.now() }));
  const { core, said } = browserCore(lock);
  await core.selectManifest(ENTRY);
  await core.startJob();
  assert.equal(core.state.jobId ?? null, null, "no job opened");
  assert.ok(said.some((m) => /Not started: the run lock is held by duet \(push\/509\)/.test(m.text)));
});

test("browser Forge: a free, missing or unreadable lock does not block Start", async () => {
  for (const lockText of [JSON.stringify(releaseBody({ holder: "duet", now: Date.now() })), 404, 500]) {
    const { core, said } = browserCore(lockText);
    await core.selectManifest(ENTRY);
    await core.startJob();
    assert.ok(core.state.jobId, `a job opened (${lockText})`);
    assert.equal(said.some((m) => /Not started/.test(m.text)), false);
    if (lockText === 500) assert.ok(said.some((m) => /Could not read the run lock/.test(m.text)), "an unreadable lock warns");
  }
});
