#!/usr/bin/env node
// The run lock on main (RUL-2026-11-07-133): one game writer per account at a time.
//
//   node forge/tools/run_lock.mjs status
//   node forge/tools/run_lock.mjs claim     --holder NAME --job TEXT [--ttl MINUTES]
//   node forge/tools/run_lock.mjs heartbeat --holder NAME [--ttl MINUTES]
//   node forge/tools/run_lock.mjs release   --holder NAME
//
// NAME is the runner, e.g. claude, duet, browser. Each write is one commit on origin/main touching
// only state/run_lock.json, built with a private index so the working tree and its branch are never
// touched. The push is a plain fast-forward: if main moved, the claim re-reads the lock and tries
// again (at most 4 times), so two claimers cannot both win. Exit 0 on success, 4 when the lock is
// held by someone else, 2 on usage or git failure. Prints one JSON line.

import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { LOCK_PATH, DEFAULT_TTL_MINUTES, parseLock, lockState, claimBody, releaseBody } from "../src/runner/runlock.mjs";

const REPO = process.env.RUN_LOCK_REPO || resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const REMOTE = process.env.RUN_LOCK_REMOTE || "origin";
const BRANCH = process.env.RUN_LOCK_BRANCH || "main";
const out = (o) => process.stdout.write(JSON.stringify(o) + "\n");
const arg = (n, d = null) => { const i = process.argv.indexOf(n); return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };

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

export function attempt(fn) {
  let last;
  for (let i = 0; i < 4; i++) {
    const { base, lock } = fetchLock();
    const r = fn(base, lock);
    if (r.done) return r;
    try { r.commit = commitLock(base, r.body, r.message); return r; }
    catch (e) { last = e; } // main moved (or the push failed): re-read and decide again
  }
  throw new Error("could not push the lock after 4 attempts: " + String(last?.stderr || last?.message || last).trim());
}

/** Extend `holder`'s claim; throws when it no longer holds the lock. */
export function heartbeat(holder, ttl = DEFAULT_TTL_MINUTES) {
  const r = attempt((base, lock) => {
    const s = lockState(lock, Date.now());
    if (!s.held || s.holder !== holder) return { done: true, refused: `${holder} does not hold the lock` };
    return { body: claimBody({ holder, ttlMinutes: ttl, now: Date.now(), prev: lock }), message: `run-lock: heartbeat by ${holder}` };
  });
  if (r.refused) throw new Error(r.refused);
  return r.body;
}

/** Release `holder`'s claim (a no-op when it holds nothing). */
export function release(holder) {
  return attempt((base, lock) => {
    const s = lockState(lock, Date.now());
    if (s.holder !== holder) return { done: true, already: true };
    return { body: releaseBody({ holder, now: Date.now() }), message: `run-lock: release by ${holder}` };
  });
}

function main() {
  const cmd = process.argv[2];
  const holder = arg("--holder");
  const ttl = Number(arg("--ttl", DEFAULT_TTL_MINUTES));
  if (!Number.isFinite(ttl) || ttl < 1 || ttl > 240) { out({ type: "refused", text: "--ttl must be 1-240 minutes" }); process.exit(2); }
  if (cmd === "status") {
    const { lock } = fetchLock();
    out({ type: "lock", ...lockState(lock, Date.now()), job: lock.job ?? null, expiresAt: lock.expiresAt ?? null });
    return;
  }
  if (!holder) { out({ type: "refused", text: `${cmd ?? "a command"} needs --holder` }); process.exit(2); }
  if (cmd === "claim" || cmd === "heartbeat") {
    const job = arg("--job");
    if (cmd === "claim" && !job) { out({ type: "refused", text: "claim needs --job (what you are about to run)" }); process.exit(2); }
    const r = attempt((base, lock) => {
      const s = lockState(lock, Date.now());
      if (s.held && s.holder !== holder) return { done: true, refused: `held by ${s.holder}${lock.job ? ` (${lock.job})` : ""} for up to ${s.minutesLeft} more minute(s)` };
      if (cmd === "heartbeat" && (!s.held || s.holder !== holder)) return { done: true, refused: `${holder} does not hold the lock` };
      const body = claimBody({ holder, job, ttlMinutes: ttl, now: Date.now(), prev: s.holder === holder ? lock : null });
      return { body, message: `run-lock: ${cmd} by ${holder}${body.job ? ` (${body.job})` : ""}` };
    });
    if (r.refused) { out({ type: "refused", text: r.refused }); process.exit(4); }
    out({ type: cmd === "claim" ? "claimed" : "heartbeat", holder, job: r.body.job, expiresAt: r.body.expiresAt, commit: r.commit });
    return;
  }
  if (cmd === "release") {
    const force = process.argv.includes("--force-expired");
    const r = attempt((base, lock) => {
      const s = lockState(lock, Date.now());
      if (!s.held && !s.expired) return { done: true, already: true };
      if (s.holder !== holder && !(force && s.expired)) return { done: true, refused: `${holder} does not hold the lock (${s.holder} does)` };
      return { body: releaseBody({ holder, now: Date.now() }), message: `run-lock: release by ${holder}` };
    });
    if (r.refused) { out({ type: "refused", text: r.refused }); process.exit(4); }
    out({ type: "released", holder, already: !!r.already, commit: r.commit ?? null });
    return;
  }
  out({ type: "refused", text: "usage: run_lock.mjs status | claim --holder NAME --job TEXT [--ttl M] | heartbeat --holder NAME | release --holder NAME" });
  process.exit(2);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try { main(); } catch (e) { out({ type: "error", text: String(e?.message || e) }); process.exit(2); }
}
