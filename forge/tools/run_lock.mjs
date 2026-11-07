#!/usr/bin/env node
// The run lock on main (RUL-2026-11-07-133): one game writer per account at a time.
//
//   node forge/tools/run_lock.mjs status
//   node forge/tools/run_lock.mjs claim     --holder LABEL --job TEXT [--ttl MINUTES] [--wait] [--instance ID]
//   node forge/tools/run_lock.mjs heartbeat --token TOKEN [--ttl MINUTES]
//   node forge/tools/run_lock.mjs release   --token TOKEN
//
// LABEL names the runner (claude, duet, browser); it is not ownership. A claim mints a random
// TOKEN and prints it: heartbeat, release and `mcp_run.mjs --token` need it, so two sessions with
// the same label can neither both hold the lock nor release each other's. A claim made less than
// QUIET_MS after the previous holder's last possible send is refused (or, with --wait, waits for
// it), because the game's rolling minute still counts that holder's calls. --instance names the
// runner's persistent pacer state (e.g. its --state dir): the same instance re-claiming skips the wait.
//
// Each write is one commit on origin/main touching only state/run_lock.json, built with a private
// index so the working tree and its branch are never touched. The push is a plain fast-forward:
// if main moved, the command re-reads the lock and decides again (at most 4 times), so two
// claimers cannot both win. Exit 0 on success, 4 when refused (held, quiet period, not yours),
// 2 on usage or git failure. Prints one JSON line.

import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { LOCK_PATH, DEFAULT_TTL_MINUTES, parseLock, lockState, claimDecision, claimBody, renewBody, releaseBody, newToken, checkTtl } from "../src/runner/runlock.mjs";

const REPO = process.env.RUN_LOCK_REPO || resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const REMOTE = process.env.RUN_LOCK_REMOTE || "origin";
const BRANCH = process.env.RUN_LOCK_BRANCH || "main";
const out = (o) => process.stdout.write(JSON.stringify(o) + "\n");
const arg = (n, d = null) => { const i = process.argv.indexOf(n); return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };

export class LockRefused extends Error {
  constructor(message, info = {}) { super(message); this.name = "LockRefused"; Object.assign(this, info); }
}

function git(args, opts = {}) {
  return execFileSync("git", args, { cwd: REPO, encoding: "utf8", stdio: ["pipe", "pipe", "pipe"], ...opts });
}

export function fetchLock() {
  git(["fetch", "-q", REMOTE, BRANCH]);
  const base = git(["rev-parse", "FETCH_HEAD"]).trim();
  let text = null;
  try { text = git(["show", `${base}:${LOCK_PATH}`]); } catch { text = null; }
  return { base, lock: parseLock(text) };
}

function commitLock(base, body, message) {
  const dir = mkdtempSync(join(tmpdir(), "runlock-"));
  const env = { ...process.env, GIT_INDEX_FILE: join(dir, "index") };
  try {
    git(["read-tree", base], { env });
    const blob = git(["hash-object", "-w", "--stdin"], { input: JSON.stringify(body, null, 1) + "\n" }).trim();
    git(["update-index", "--add", "--cacheinfo", `100644,${blob},${LOCK_PATH}`], { env });
    const tree = git(["write-tree"], { env }).trim();
    const commit = git(["commit-tree", tree, "-p", base, "-m", message], { env }).trim();
    git(["push", "-q", REMOTE, `${commit}:refs/heads/${BRANCH}`]);
    return commit;
  } finally { rmSync(dir, { recursive: true, force: true }); }
}

/** Read, decide, write against the version read; re-read and decide again if main moved. */
function attempt(decide) {
  let last;
  for (let i = 0; i < 4; i++) {
    const { base, lock } = fetchLock();
    const r = decide(lock, Date.now());
    if (r.done) return r;
    try { r.commit = commitLock(base, r.body, r.message); return r; }
    catch (e) { last = e; }
  }
  throw new Error("could not push the lock after 4 attempts: " + String(last?.stderr || last?.message || last).trim());
}

const sleepSync = (msec) => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, msec);

/** Claim the lock. Returns the written body (with its token). Throws LockRefused when held or (without wait) quiet. */
export function claim({ holder, job, ttlMinutes = DEFAULT_TTL_MINUTES, wait = false, instance = null }) {
  if (!holder) throw new LockRefused("a claim needs --holder LABEL");
  if (!job) throw new LockRefused("a claim needs --job (what you are about to run)");
  checkTtl(ttlMinutes);
  for (let round = 0; round < 3; round++) {
    const r = attempt((lock, now) => {
      const d = claimDecision(lock, now, instance);
      if (!d.ok) return { done: true, refused: d };
      const token = newToken();
      return { body: claimBody({ holder, job, token, ttlMinutes, now, instance }), message: `run-lock: claim by ${holder} (${job})` };
    });
    if (!r.refused) return r.body;
    if (r.refused.held || !wait) throw new LockRefused(r.refused.reason, { held: r.refused.held, waitMs: r.refused.waitMs });
    sleepSync(Math.min(r.refused.waitMs, 70_000) + 250);
  }
  throw new LockRefused("the quiet period kept restarting; another runner is active");
}

/** Extend the claim that `token` holds. Throws LockRefused when it no longer holds the lock. */
export function heartbeat(token, ttlMinutes = null) {
  const r = attempt((lock, now) => {
    if (!token || lock.token !== token) return { done: true, refused: `this claim no longer holds the run lock${lock.token ? ` (${lock.holder} does)` : ""}` };
    if (!lockState(lock, now).held) return { done: true, refused: "this claim's run lock has already expired" };
    return { body: renewBody(lock, { ttlMinutes: ttlMinutes ?? lock.ttlMinutes ?? DEFAULT_TTL_MINUTES, now }), message: `run-lock: heartbeat by ${lock.holder}` };
  });
  if (r.refused) throw new LockRefused(r.refused);
  return r.body;
}

/** Release the claim that `token` holds; a no-op (already: true) when it holds nothing. */
export function release(token) {
  const r = attempt((lock, now) => {
    if (!token || lock.token !== token) return { done: true, already: true };
    return { body: releaseBody(lock, { now }), message: `run-lock: release by ${lock.holder}` };
  });
  return { already: !!r.already, commit: r.commit ?? null };
}

function main() {
  const cmd = process.argv[2];
  const ttlArg = arg("--ttl");
  const ttl = ttlArg == null ? null : Number(ttlArg);
  try {
    if (cmd === "status") {
      const { lock } = fetchLock();
      const now = Date.now();
      const d = claimDecision(lock, now);
      out({ type: "lock", ...lockState(lock, now), expiresAt: lock.expiresAt ?? null, claimable: d.ok, waitMs: d.ok ? 0 : d.waitMs });
      return;
    }
    if (cmd === "claim") {
      const body = claim({ holder: arg("--holder"), job: arg("--job"), ttlMinutes: ttl ?? DEFAULT_TTL_MINUTES, wait: process.argv.includes("--wait"), instance: arg("--instance") });
      out({ type: "claimed", holder: body.holder, job: body.job, token: body.token, expiresAt: body.expiresAt });
      return;
    }
    if (cmd === "heartbeat") {
      const body = heartbeat(arg("--token"), ttl);
      out({ type: "heartbeat", holder: body.holder, expiresAt: body.expiresAt });
      return;
    }
    if (cmd === "release") {
      const r = release(arg("--token"));
      out({ type: "released", ...r });
      return;
    }
  } catch (e) {
    if (e instanceof LockRefused) { out({ type: "refused", text: e.message, waitMs: e.waitMs ?? null }); process.exit(4); }
    throw e;
  }
  out({ type: "refused", text: "usage: run_lock.mjs status | claim --holder LABEL --job TEXT [--ttl M] [--wait] | heartbeat --token T [--ttl M] | release --token T" });
  process.exit(2);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try { main(); } catch (e) { out({ type: "error", text: String(e?.message || e) }); process.exit(2); }
}
