#!/usr/bin/env node
// Run a Forge manifest through the game connection (MCP) instead of a browser tab.
// See docs/forge/MCP_RUNNER.md for the whole loop. Usage, from the repository root:
//
//   node forge/tools/mcp_run.mjs plan   push/412_x.json
//       Offline. Parse, plan and pre-send validate exactly as Forge does on "open"; prints the
//       plan and any problems. Nothing is sent (a Bloodright collection is the exception: Forge
//       reads the live inventory when one is opened, so plan refuses those).
//
//   node forge/tools/mcp_run.mjs run    push/412_x.json --token T --state DIR [--allowance 20] [--transcript auto|PATH] [--inbox DIR] [--keep-lock]
//   node forge/tools/mcp_run.mjs resume JOB_ID         --token T --state DIR [--transcript auto|PATH] [--inbox DIR] [--keep-lock]
//       Both need the run lock on main held by the claim whose token is T (forge/tools/run_lock.mjs claim
//       prints it; or RUN_LOCK_TOKEN; RUL-2026-11-07-133). Checked before the first game call; renewed every
//       third of its TTL; every game call stops a minute before the last confirmed expiry, and at once if the
//       claim is lost. Released when the process exits unless --keep-lock (to chain the next job).
//       Live. Every game call is written to DIR/exchange/request.json and waits for its answer
//       (see exchange.mjs); the session holding the game connection makes each call. With
//       --transcript, the answer is taken from that session's own record of the call
//       (transcript.mjs; "auto" finds this session's transcript), so nothing is copied by hand.
//       The journal, send logs and id map persist in DIR/storage.json, and the capture cache and
//       capture snapshots in DIR/captures.idb (idbfile.mjs), so a stopped or crashed run resumes
//       with its evidence intact. The results bundle is written to harvests/inbox/ in this
//       working tree, to be committed (or to --inbox DIR).
//
//   node forge/tools/mcp_run.mjs jobs   --state DIR
//       Offline. Lists the journal's jobs and their states.
//
//   node forge/tools/mcp_run.mjs resend JOB_ID IDX --state DIR
//       Offline. Re-send the step an ORPHANED item stopped at (the UI's "Re-send <phase>"),
//       after you have checked the live record. The next resume sends it.
//
//   node forge/tools/mcp_run.mjs skip JOB_ID IDX... --reason TEXT --state DIR
//       Offline. Mark PLANNED items SKIPPED, for edits a separate read showed are already live.
//       Nothing is sent; the job's outcome stays "unverified", as a skip should.
//
// What this host refuses, and why:
//   - manifests that upload images (@img refs or an imagePack): uploads go to /api/uploadthing,
//     which is not a tRPC procedure and is not on the MCP surface. Run those in the browser.
//   - Bloodright collections in `plan`, as above.

import { readFileSync, readdirSync, statSync, mkdirSync, writeFileSync } from "node:fs";
import { join, resolve, basename, dirname, isAbsolute } from "node:path";
import { fileURLToPath } from "node:url";
import { compose } from "../src/main.mjs";
import { ForgeCore } from "../src/core/core.mjs";
import { AUTH } from "../src/transport/auth.mjs";
import { writeGh } from "../src/storage/compat.mjs";
import { manifestNumber } from "../src/github.mjs";
import { McpBridgeClient, Pacer, DEFAULT_MCP_ALLOWANCE, leaseGatedTransport } from "../src/hosts/mcp/bridge.mjs";
import { FileExchange, FileStorage } from "../src/hosts/mcp/exchange.mjs";
import { FileIDB } from "../src/hosts/mcp/idbfile.mjs";
import { TranscriptAnswerer, findTranscript } from "../src/hosts/mcp/transcript.mjs";
import { blockReason, Lease, renewEveryMs, DEFAULT_TTL_MINUTES } from "../src/runner/runlock.mjs";
import { fetchLock, heartbeat, release, LockRefused } from "./run_lock.mjs";

const REPO = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");

function arg(name, fallback = null) {
  const i = process.argv.indexOf(name);
  return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}
const out = (o) => process.stdout.write(JSON.stringify(o) + "\n");
const die = (msg, code = 2) => { out({ type: "refused", text: msg }); process.exit(code); };

/** The repository working tree stands in for the GitHub contents API. */
function localGithub(inbox = null) {
  return {
    async list(dir = "push") {
      return readdirSync(join(REPO, dir)).filter((n) => n.endsWith(".json")).map((name) => {
        const path = `${dir}/${name}`;
        return { name, path, sha: null, size: statSync(join(REPO, path)).size, type: "file" };
      });
    },
    async text(path) {
      try { return readFileSync(join(REPO, path), "utf8"); }
      catch (e) { if (e.code === "ENOENT") e.status = 404; throw e; }
    },
    async raw(path) { const b = readFileSync(join(REPO, path)); return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength); },
    async put(path, text) {
      if (!/^harvests\/inbox\/[^/]+\.json$/.test(path)) throw new Error("the MCP host only writes results bundles to harvests/inbox/");
      const target = inbox ? join(inbox, basename(path)) : join(REPO, path);
      mkdirSync(dirname(target), { recursive: true });
      writeFileSync(target, text);
      out({ type: "bundle", path: inbox ? target : path });
      return { sha: null, htmlUrl: null };
    },
  };
}

async function build({ stateDir, live, lease = null }) {
  mkdirSync(stateDir, { recursive: true });
  const storage = new FileStorage(join(stateDir, "storage.json"));
  // Results go to the local inbox; there is no PAT on this host (the flag only selects the path).
  writeGh(storage, { on: true, pat: "local-working-tree" });
  let client;
  if (live) {
    const t = arg("--transcript");
    const answerer = t ? new TranscriptAnswerer({ path: t === "auto" ? findTranscript() : t, onNote: (n) => out(n) }) : null;
    if (answerer) out({ type: "transcript", path: answerer.path });
    const exchange = new FileExchange({
      dir: join(stateDir, "exchange"),
      answerer,
      onRequest: (r) => out({ type: "request", id: r.id, endpoint: r.arguments.endpointName, kind: r.kind, file: join(stateDir, "exchange", "request.json") }),
    });
    const allowance = Number(arg("--allowance", DEFAULT_MCP_ALLOWANCE));
    // The lease is checked again at the wire, after the pacer's wait: a pacer sleep can outlast the
    // stop margin, and a request file is a send (RUL-2026-11-07-133).
    const transport = lease ? leaseGatedTransport(exchange, lease) : exchange;
    client = new McpBridgeClient({ transport, pacer: new Pacer({ storage, allowance }) });
  } else {
    client = { call: async (p) => { throw new Error(`offline: ${p} was not sent`); }, batch: async (c) => { throw new Error(`offline: ${c.map((x) => x.path).join(",")} was not sent`); } };
  }
  const refuseFetch = async (url) => { throw new Error(`the MCP host makes no direct HTTP requests (${String(url).slice(0, 60)})`); };
  const idb = await FileIDB.open(join(stateDir, "captures.idb"));
  const deps = compose({ lease, storage, indexedDB: idb.factory, fetchImpl: refuseFetch, client, authState: AUTH.UNKNOWN, tabId: "mcp-" + process.pid, log: () => {} });
  const inbox = arg("--inbox");
  deps.github = localGithub(inbox ? resolve(inbox) : null);
  const core = new ForgeCore({ version: "forge-mcp", storage, runLockMode: "external", ...deps });
  core.subscribe((n) => {
    if (n.type === "message") out({ type: "message", kind: n.kind ?? null, text: n.text });
    else if (n.type === "export") out({ type: "export", name: n.name }); // sync failed: bundle handed back
  });
  return { core, deps, storage };
}

function entryFor(path) {
  // Relative to the repository root, as Forge's picker names them (push/412_x.json). An absolute
  // path is read as given, for manifests kept outside the tree.
  const rel = path.replace(/^\.\//, "");
  const text = readFileSync(isAbsolute(rel) ? rel : join(REPO, rel), "utf8");
  return { name: basename(rel), path: rel, sha: null, size: text.length, type: "file", number: manifestNumber(basename(rel)), text };
}

function refuseUploads(sel) {
  if (sel.images?.length || sel.pack) {
    die(`this manifest uploads images (${(sel.images || []).join(", ") || "imagePack"}); uploads are not on the game connection, so run it in the browser`);
  }
}

function summary(core, deps, jobId) {
  const job = deps.journal.get(jobId);
  const tally = {};
  for (const it of job.items) tally[it.state] = (tally[it.state] ?? 0) + 1;
  return { type: "job", jobId, state: job.state, items: tally, exportName: job.exportName ?? null };
}

async function main() {
  const cmd = process.argv[2];
  const stateDir = resolve(arg("--state", join(REPO, ".forge-mcp")));
  if (cmd === "plan") {
    const entry = entryFor(process.argv[3] ?? die("plan needs a manifest path"));
    if (JSON.parse(entry.text).bloodrightCollection) die("a Bloodright collection reads the live game when opened; use run");
    const { core } = await build({ stateDir: join(stateDir, "plan-scratch"), live: false });
    await core.selectManifest(entry);
    const s = core.state.selected;
    if (!s) die(core.state.openError?.text ?? "could not open the manifest");
    out({ type: "plan", manifest: entry.path, items: s.plan.map((it) => ({ idx: it.idx, entity: it.entity, slot: it.slot, name: it.name })),
          captures: { before: s.manifest.capture?.before?.length ?? 0, after: s.manifest.capture?.after?.length ?? 0 },
          images: s.images, problems: s.problems });
    process.exit(s.problems.length ? 1 : 0);
  }
  if (cmd === "jobs") {
    const { deps } = await build({ stateDir, live: false });
    for (const j of deps.journal.listJobs()) out({ type: "job", jobId: j.jobId ?? j.id, state: j.state, manifest: j.manifestPath ?? null });
    return;
  }
  if (cmd === "skip") {
    // Offline: mark PLANNED items SKIPPED with a reason, for edits a separate read showed are
    // already live. Never touches an item that was sent; the job outcome stays "unverified".
    const jobId = process.argv[3];
    const reasonAt = process.argv.indexOf("--reason");
    const reason = reasonAt > 0 ? process.argv[reasonAt + 1] : null;
    const rest = process.argv.slice(4); const stop = rest.findIndex((a) => a.startsWith("--"));
    const idxs = (stop < 0 ? rest : rest.slice(0, stop)).map(Number);
    if (idxs.some((n) => !Number.isInteger(n))) die("skip: item indexes must be whole numbers");
    if (!jobId || !idxs.length || !reason) die("usage: mcp_run.mjs skip JOB_ID IDX... --reason TEXT --state DIR");
    const { deps } = await build({ stateDir, live: false });
    const job = deps.journal.get(jobId);
    if (!job) die(`no job ${jobId}`);
    for (const i of idxs) {
      const item = job.items[i];
      if (!item) die(`no item ${i} in ${jobId}`);
      if (item.state !== "PLANNED") die(`skip needs a PLANNED item; ${i} is ${item.state}`);
    }
    for (const i of idxs) deps.journal.transition(jobId, i, "SKIPPED", { error: null, skipReason: reason });
    out({ type: "skip", jobId, count: idxs.length, reason });
    return;
  }
  if (cmd === "resend") {
    // Offline. The UI's "Re-send <phase>" on an ORPHANED item that already has its id: the
    // operator has checked the record and chooses to send that same step again on resume.
    const [jobId, idxRaw] = [process.argv[3], process.argv[4]];
    if (!jobId || idxRaw === undefined) die("usage: mcp_run.mjs resend JOB_ID IDX --state DIR");
    const { deps } = await build({ stateDir, live: false });
    const item = deps.journal.get(jobId)?.items[Number(idxRaw)];
    if (!item) die(`no item ${idxRaw} in ${jobId}`);
    if (item.state !== "ORPHANED" || !item.entityId) die(`resend needs an ORPHANED item with an id; ${idxRaw} is ${item.state}`);
    // Not adopt(): its holder check refuses an id that an earlier step of the same manifest also
    // targets, and this item already holds its id. Same transition adopt() makes for a re-send.
    deps.journal.transition(jobId, Number(idxRaw), "CONFIRMED", { entityId: item.entityId, phase: item.phase, adopted: true, error: null });
    const after = deps.journal.get(jobId).items[Number(idxRaw)];
    out({ type: "resend", jobId, idx: Number(idxRaw), entityId: after.entityId, state: after.state, phase: after.phase });
    return;
  }
  if (cmd === "run" || cmd === "resume") {
    // The run lock before anything touches the game: one writer per account (RUL-2026-11-07-133).
    // The claim is made with run_lock.mjs; its token is the ownership, the label only a name.
    const token = arg("--token") ?? process.env.RUN_LOCK_TOKEN ?? die("run and resume need --token (from node forge/tools/run_lock.mjs claim --holder NAME --job TEXT)");
    let lock;
    try { lock = fetchLock().lock; } catch (e) { die("could not read the run lock: " + String(e?.message || e).trim() + "; nothing was sent", 4); }
    const why = blockReason(lock, token, Date.now());
    if (why) die(why + "; nothing was sent", 4);
    const lease = new Lease();
    const renew = async () => {
      try { const b = heartbeat(token); lease.renewed(b.expiresAt); out({ type: "lock", holder: b.holder, expiresAt: b.expiresAt, heartbeat: true }); }
      catch (e) {
        if (e instanceof LockRefused) lease.lose(e.message); // confirmed loss: no further sends
        out({ type: "message", kind: "bad", text: "run-lock heartbeat failed: " + String(e?.message || e).trim() });
      }
    };
    const every = renewEveryMs(lock.ttlMinutes ?? DEFAULT_TTL_MINUTES);
    lease.begin({ token, holder: lock.holder, expiresAt: lock.expiresAt, renewer: renew, renewEveryMs: every });
    out({ type: "lock", holder: lock.holder, expiresAt: lock.expiresAt });
    const beat = setInterval(() => { lease.renewNow(); }, every);
    beat.unref?.();
    // "exit" (not "beforeExit") so a refusal or crash after the claim releases too; the release is
    // synchronous git, which an exit handler may run. Sends have stopped by then.
    const keep = process.argv.includes("--keep-lock");
    process.on("exit", () => {
      clearInterval(beat);
      lease.end();
      if (keep) return;
      try { release(token); out({ type: "lock", released: true }); }
      catch (e) { out({ type: "message", kind: "bad", text: "run-lock release failed (it expires on its own): " + String(e?.message || e).trim() }); }
    });
    const { core, deps } = await build({ stateDir, live: true, lease });
    await core.recheckAuth(); // no page runtime on this host: probe only
    if (!deps.auth.ready) die(`the game connection is not confirmed (${deps.auth.state}${deps.auth.detail ? ": " + deps.auth.detail : ""}); nothing was sent`, 3);
    out({ type: "auth", state: deps.auth.state });
    let jobId;
    if (cmd === "run") {
      const entry = entryFor(process.argv[3] ?? die("run needs a manifest path"));
      await core.selectManifest(entry);
      const s = core.state.selected;
      if (!s) die(core.state.openError?.text ?? "could not open the manifest");
      refuseUploads(s);
      if (s.problems.length) die("preview problems: " + s.problems.join(" | "), 1);
      await core.startJob();
      jobId = core.state.jobId;
    } else {
      jobId = process.argv[3] ?? die("resume needs a job id");
      await core.resumeJob(jobId);
    }
    if (!jobId || !deps.journal.get(jobId)) die("no job was opened", 1);
    out(summary(core, deps, jobId));
    return;
  }
  die("usage: mcp_run.mjs plan|run|resume|jobs ... (see the header of this file)");
}

main().catch((e) => { out({ type: "error", text: String(e && e.stack || e) }); process.exit(1); });
