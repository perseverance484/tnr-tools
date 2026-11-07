// The run lock (RUL-2026-11-07-133): one game writer per account at a time.
//
// The four review findings on be1c3afd each have a test here:
//   R1 the browser claims and holds the lock for its whole run;
//   R2 a lapsed or lost lease stops sends (connector and browser);
//   R3 ownership is a per-claim token, not the holder label;
//   R4 a new claim waits out the previous holder's rolling minute.
import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { parseLock, lockState, blockReason, claimDecision, claimBody, renewBody, releaseBody, newToken, Lease, renewEveryMs, quietUntil,
  LOCK_PATH, QUIET_MS, STOP_MARGIN_MS } from "../src/runner/runlock.mjs";
import { ForgeCore } from "../src/core/core.mjs";
import { composeForTest, memoryLockStore } from "./compose.mjs";
import { McpBridgeClient, leaseGatedTransport } from "../src/hosts/mcp/bridge.mjs";

const TOOL = join(dirname(fileURLToPath(import.meta.url)), "..", "tools", "run_lock.mjs");
const T0 = Date.parse("2026-11-07T06:00:00Z");
const tok = () => newToken();
const held = (holder, minutes, now = T0, job = "push/502") => claimBody({ holder, job, token: tok(), ttlMinutes: minutes, now });

// ------------------------------------------------------------------ pure rules
test("parseLock: missing or empty is free; junk, short tokens and a held lock without expiry are refused", () => {
  assert.equal(parseLock(null).token, null);
  assert.equal(parseLock("  ").token, null);
  assert.throws(() => parseLock("{"), /not JSON/);
  assert.throws(() => parseLock("[]"), /not an object/);
  assert.throws(() => parseLock(JSON.stringify({ holder: "duet", token: "abc" })), /16\+/);
  assert.throws(() => parseLock(JSON.stringify({ holder: "duet", token: "a".repeat(32) })), /expiresAt/);
});

test("lockState: held until expiresAt, then expired", () => {
  const l = held("duet", 30);
  assert.deepEqual(lockState(l, T0 + 10 * 60000), { held: true, holder: "duet", job: "push/502", expired: false, minutesLeft: 20 });
  assert.equal(lockState(l, T0 + 30 * 60000).held, false);
  assert.equal(lockState(releaseBody(l, { now: T0 }), T0).held, false);
});

test("R3: blockReason is decided by the token; the label grants nothing", () => {
  const l = held("claude", 30);
  assert.equal(blockReason(l, l.token, T0), null);
  assert.match(blockReason(l, tok(), T0), /held by another claim \(claude, push\/502\)/, "another claude session's token");
  assert.match(blockReason(l, null, T0), /no run-lock claim/);
  assert.match(blockReason({ token: null }, l.token, T0), /no longer holds/);
  assert.match(blockReason(l, l.token, T0 + 30 * 60000 - STOP_MARGIN_MS), /about to expire/);
});

test("R4: claimDecision: held refuses; after a release or lapse the next claim waits the quiet period", () => {
  const l = held("duet", 30);
  assert.equal(claimDecision(l, T0).ok, false);
  assert.equal(claimDecision(l, T0).held, true);
  const rel = releaseBody(l, { now: T0 + 5 * 60000 });
  const d = claimDecision(rel, T0 + 5 * 60000 + 10_000);
  assert.equal(d.ok, false); assert.equal(d.held, false); assert.equal(d.waitMs, QUIET_MS - 10_000);
  assert.match(d.reason, /rolling minute/);
  assert.equal(claimDecision(rel, T0 + 5 * 60000 + QUIET_MS).ok, true);
  // a lapsed claim may have sent until its expiry: quiet runs from there
  assert.equal(quietUntil(l), Date.parse(l.expiresAt) + QUIET_MS);
  assert.equal(claimDecision(l, Date.parse(l.expiresAt) + 1000).ok, false);
  assert.equal(claimDecision(l, Date.parse(l.expiresAt) + QUIET_MS).ok, true);
  assert.equal(claimDecision({ token: null }, T0).ok, true, "never claimed: free");
});

test("R2: Lease stops sends a margin before the confirmed expiry and at once on loss; renewals only extend", () => {
  let now = T0;
  const lease = new Lease(() => now);
  assert.equal(lease.check(), null, "inactive: no run in progress");
  const l = held("claude", 10);
  lease.begin({ token: l.token, holder: "claude", expiresAt: l.expiresAt });
  now = T0 + 10 * 60000 - STOP_MARGIN_MS - 1; assert.equal(lease.check(), null);
  now += 1; assert.match(lease.check(), /ran out/);
  lease.renewed(new Date(T0 + 20 * 60000).toISOString()); assert.equal(lease.check(), null, "a confirmed renewal resumes sending");
  lease.renewed(new Date(T0).toISOString()); assert.equal(lease.check(), null, "an older expiry never shortens it");
  lease.lose("taken by duet"); assert.equal(lease.check(), "taken by duet");
  lease.renewed(new Date(T0 + 60 * 60000).toISOString()); assert.equal(lease.check(), "taken by duet", "a lost lease stays lost");
  // renewal cadence: a third of the TTL, so two renewals can fail before the stop margin
  assert.equal(renewEveryMs(6), 2 * 60000);
  assert.equal(renewEveryMs(60), 15 * 60000);
  assert.throws(() => renewEveryMs(1), /TTL/);
});

test("renewBody keeps the token and claim time; releaseBody records who and when", () => {
  const l = held("claude", 60);
  const r = renewBody(l, { ttlMinutes: 60, now: T0 + 15 * 60000 });
  assert.equal(r.token, l.token); assert.equal(r.claimedAt, l.claimedAt);
  assert.equal(Date.parse(r.expiresAt), T0 + 75 * 60000);
  const x = releaseBody(l, { now: T0 + 1 });
  assert.equal(x.token, null); assert.equal(x.releasedBy, "claude"); assert.equal(x.releasedJob, "push/502");
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
  return { clone, done: () => rmSync(root, { recursive: true, force: true }) };
}

function lockTool(repo, ...args) {
  return new Promise((res) => {
    const p = spawn(process.execPath, [TOOL, ...args], { env: { ...process.env, RUN_LOCK_REPO: repo } });
    let out = ""; p.stdout.on("data", (b) => { out += b; });
    p.on("close", (code) => res({ code, out: JSON.parse(out.trim().split("\n").pop()) }));
  });
}

test("run_lock.mjs: claim mints a token; others (same label included) cannot claim, renew or release it", async () => {
  const sb = sandbox();
  try {
    const a = sb.clone("a"), b = sb.clone("b");
    assert.equal((await lockTool(a, "status")).out.held, false);
    const c1 = await lockTool(a, "claim", "--holder", "claude", "--job", "push/502", "--ttl", "30");
    assert.equal(c1.code, 0); assert.equal(c1.out.type, "claimed"); assert.ok(c1.out.token.length >= 16);
    const c2 = await lockTool(b, "claim", "--holder", "claude", "--job", "other");
    assert.equal(c2.code, 4, "R3: the same label is refused"); assert.match(c2.out.text, /held by claude \(push\/502\)/);
    const hbWrong = await lockTool(b, "heartbeat", "--token", "f".repeat(32));
    assert.equal(hbWrong.code, 4);
    const relWrong = await lockTool(b, "release", "--token", "f".repeat(32));
    assert.equal(relWrong.code, 0); assert.equal(relWrong.out.already, true, "a foreign token releases nothing");
    assert.equal((await lockTool(a, "status")).out.held, true, "still held after the foreign release");
    const hb = await lockTool(b, "heartbeat", "--token", c1.out.token, "--ttl", "45");
    assert.equal(hb.code, 0, "the token works from any checkout");
    const r = await lockTool(a, "release", "--token", c1.out.token);
    assert.equal(r.code, 0); assert.equal(r.out.already, false);
    const c3 = await lockTool(b, "claim", "--holder", "duet", "--job", "scan");
    assert.equal(c3.code, 4, "R4: right after a release the next claim waits the quiet period");
    assert.match(c3.out.text, /rolling minute/); assert.ok(c3.out.waitMs > 0 && c3.out.waitMs <= QUIET_MS);
    // Each write is one commit touching only the lock file, on top of whatever main was.
    git(a, "fetch", "-q", "origin", "main");
    assert.equal(git(a, "show", "--name-only", "--format=", "FETCH_HEAD").trim(), LOCK_PATH);
    assert.equal(git(a, "show", "FETCH_HEAD:README"), "x\n", "the rest of main is untouched");
  } finally { sb.done(); }
});

test("R3: two simultaneous claims with the SAME label: exactly one wins", async () => {
  const sb = sandbox();
  try {
    const a = sb.clone("a"), b = sb.clone("b");
    const [x, y] = await Promise.all([
      lockTool(a, "claim", "--holder", "claude", "--job", "j1"),
      lockTool(b, "claim", "--holder", "claude", "--job", "j2"),
    ]);
    assert.deepEqual([x.code, y.code].sort(), [0, 4]);
  } finally { sb.done(); }
});

// ------------------------------------------------------------------ the browser
const MANIFEST = JSON.stringify({ items: [
  { entity: "jutsu", slot: "create", name: "Lock A", srcId: "lk-a", data: { name: "Lock A", hidden: true } },
  { entity: "jutsu", slot: "create", name: "Lock B", srcId: "lk-b", data: { name: "Lock B", hidden: true } },
] });
const ENTRY = { name: "46_lock.json", path: "push/46_lock.json", sha: "lk", size: 64, type: "file" };

function browserCore(lockStore = memoryLockStore()) {
  const d = composeForTest();
  d.github = { list: async () => [ENTRY], text: async () => MANIFEST, put: async () => ({ sha: "s" }) };
  const slept = [];
  const core = new ForgeCore({ version: "test", storage: d.storage, now: d.clock, ...d, lockStore,
    sleep: async (ms) => { slept.push(ms); d.clock.tick(ms); } });
  const said = [];
  core.subscribe((n) => { if (n.type === "message") said.push(n); });
  return { core, d, said, lockStore, slept };
}
const creates = (d) => d.game.calls.filter((c) => /\.create$/.test(c.path)).length;

test("R1: the browser claims for its run, holds it while running, and releases it after", async () => {
  const { core, d, lockStore } = browserCore();
  let seenDuring = null;
  d.runner.on((e) => { if (e.type === "item:start" && seenDuring == null) seenDuring = parseLock(lockStore.text); });
  await core.selectManifest(ENTRY);
  await core.startJob();
  assert.equal(seenDuring.holder, "browser", "held by the browser while its items ran");
  assert.ok(seenDuring.token);
  assert.equal(claimDecision(seenDuring, d.clock()).held, true, "a connector claim made mid-run is refused");
  const after = parseLock(lockStore.text);
  assert.equal(after.token, null); assert.equal(after.releasedBy, "browser");
  assert.equal(creates(d), 2);
  assert.deepEqual(lockStore.writes.map((w) => w.message.split(" by ")[0]), ["run-lock: claim", "run-lock: release"]);
});

test("R1: the browser does not start while another runner holds the lock; nothing is sent", async () => {
  const other = memoryLockStore(JSON.stringify(claimBody({ holder: "duet", job: "push/509", token: tok(), ttlMinutes: 60, now: composeForTest().clock() })));
  const { core, d, said } = browserCore(other);
  await core.selectManifest(ENTRY);
  await core.startJob();
  assert.equal(creates(d), 0);
  assert.ok(said.some((m) => /Not run: the run lock is held by duet \(push\/509\)/.test(m.text)));
});

test("R4: the browser waits out the quiet period after another runner's release, then claims", async () => {
  const c = composeForTest().clock;
  const rel = releaseBody(claimBody({ holder: "duet", job: "scan", token: tok(), ttlMinutes: 30, now: c() - 60000 }), { now: c() - 20_000 });
  const { core, d, slept } = browserCore(memoryLockStore(JSON.stringify(rel)));
  await core.selectManifest(ENTRY);
  await core.startJob();
  assert.equal(slept.length, 1); assert.ok(slept[0] >= QUIET_MS - 20_000 && slept[0] < QUIET_MS);
  assert.equal(creates(d), 2);
});

test("R2: a lease lost mid-run pauses the job before the next write; that write is never sent", async () => {
  const { core, d } = browserCore();
  d.runner.on((e) => { if (e.type === "item:end" && e.idx === 0) core.lease.lose("the run lock was taken by duet while this run held it"); });
  await core.selectManifest(ENTRY);
  await core.startJob();
  assert.equal(creates(d), 1, "the second create was not sent");
  const job = d.journal.get(core.state.jobId ?? d.journal.listJobs()[0].jobId ?? d.journal.listJobs()[0].id);
  assert.equal(job.state, "PAUSED"); assert.equal(job.pause.reason, "RUN_LOCK");
  assert.notEqual(job.items[1].state, "SENT", "withdrawn, not left ambiguous");
});

test("R2: renewRunLock notices the lock was taken and stops the lease; a failed write leaves it to run out", async () => {
  const { core, lockStore, d } = browserCore();
  const store = lockStore;
  // claim by hand through the core, as drive() does
  assert.equal(await core._acquireRunLock("push/46_lock.json"), null);
  assert.equal(core.lease.check(), null);
  const realWrite = store.write;
  store.write = async () => { throw new Error("HTTP 502"); };
  await core._renewRunLock();
  assert.equal(core.lease.check(), null, "a transient failure does not stop the lease early");
  store.write = realWrite;
  store.set(JSON.stringify(claimBody({ holder: "duet", job: "x", token: tok(), ttlMinutes: 60, now: d.clock() })));
  await core._renewRunLock();
  assert.match(core.lease.check(), /taken by duet/);
  await core._releaseRunLock();
  assert.equal(parseLock(store.text).holder, "duet", "releasing a lost claim never frees someone else's lock");
});

test("R2: an unrenewed browser lease stops sending a minute before expiry", async () => {
  const { core, d } = browserCore();
  assert.equal(await core._acquireRunLock("j"), null);
  d.clock.tick(20 * 60000 - STOP_MARGIN_MS);
  assert.match(core.lease.check(), /ran out/);
  await core._releaseRunLock();
});

test("R4: the same runner instance re-claiming skips the quiet period; any other instance waits", () => {
  const l = claimBody({ holder: "browser", job: "a", token: tok(), ttlMinutes: 20, now: T0, instance: "browser:tab1" });
  const rel = releaseBody(l, { now: T0 + 60000 });
  assert.equal(rel.releasedInstance, "browser:tab1");
  assert.equal(claimDecision(rel, T0 + 61000, "browser:tab1").ok, true);
  assert.equal(claimDecision(rel, T0 + 61000, "browser:tab2").ok, false);
  assert.equal(claimDecision(rel, T0 + 61000, null).ok, false);
  assert.equal(claimDecision(l, T0 + 1000, "browser:tab1").ok, false, "a HELD lock is refused even to its own instance (that is a heartbeat)");
});

test("R2: the connector's wire gate refuses after the pacer when the lease has lapsed; nothing reaches the session", async () => {
  let now = T0;
  const lease = new Lease(() => now);
  const l = held("claude", 10);
  lease.begin({ token: l.token, holder: "claude", expiresAt: l.expiresAt });
  const sent = [];
  const transport = leaseGatedTransport({ send: async (r) => { sent.push(r); return { text: '{"success":true,"message":"x"}' }; } }, lease);
  // the pacer's wait carries the clock past the stop margin
  const client = new McpBridgeClient({ transport, pacer: { acquire: async () => { now = Date.parse(l.expiresAt) - STOP_MARGIN_MS + 1; } } });
  await assert.rejects(client.call("jutsu.create", { name: "x" }), (e) => e.name === "Paused" && e.reason === "RUN_LOCK");
  assert.equal(sent.length, 0);
});

test("R2: the runner renews between items when due, on the run's own clock (no wall timer needed)", async () => {
  const { core, d, lockStore } = browserCore();
  // each create carries the clock 8 minutes on, past the 20-minute browser TTL over the two items
  d.runner.on((e) => { if (e.type === "item:end") d.clock.tick(8 * 60000); });
  await core.selectManifest(ENTRY);
  await core.startJob();
  assert.equal(creates(d), 2, "the second item ran: the lease was renewed, not run out");
  assert.ok(lockStore.writes.some((w) => /heartbeat/.test(w.message)));
});
