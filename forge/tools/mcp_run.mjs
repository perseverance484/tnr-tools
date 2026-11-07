#!/usr/bin/env node
// Run a Forge manifest through the game connection (MCP) instead of a browser tab.
// See docs/forge/MCP_RUNNER.md for the whole loop. Usage, from the repository root:
//
//   node forge/tools/mcp_run.mjs plan   push/412_x.json
//       Offline. Parse, plan and pre-send validate exactly as Forge does on "open"; prints the
//       plan and any problems. Nothing is sent (a Bloodright collection is the exception: Forge
//       reads the live inventory when one is opened, so plan refuses those).
//
//   node forge/tools/mcp_run.mjs run    push/412_x.json --state DIR [--allowance 20]
//   node forge/tools/mcp_run.mjs resume JOB_ID         --state DIR
//       Live. Every game call is written to DIR/exchange/request.json and waits for its answer
//       (see exchange.mjs); the session holding the game connection answers them one by one.
//       The journal, send logs and id map persist in DIR/storage.json, so a stopped run resumes.
//       The results bundle is written to harvests/inbox/ in this working tree, to be committed.
//
//   node forge/tools/mcp_run.mjs jobs   --state DIR
//       Offline. Lists the journal's jobs and their states.
//
// What this host refuses, and why:
//   - manifests that upload images (@img refs or an imagePack): uploads go to /api/uploadthing,
//     which is not a tRPC procedure and is not on the MCP surface. Run those in the browser.
//   - Bloodright collections in `plan`, as above.

import { readFileSync, readdirSync, statSync, mkdirSync, writeFileSync } from "node:fs";
import { join, resolve, basename, dirname, isAbsolute } from "node:path";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { compose } from "../src/main.mjs";
import { ForgeCore } from "../src/core/core.mjs";
import { AUTH } from "../src/transport/auth.mjs";
import { writeGh } from "../src/storage/compat.mjs";
import { manifestNumber } from "../src/github.mjs";
import { McpBridgeClient, Pacer, DEFAULT_MCP_ALLOWANCE } from "../src/hosts/mcp/bridge.mjs";
import { FileExchange, FileStorage } from "../src/hosts/mcp/exchange.mjs";

const REPO = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");

function arg(name, fallback = null) {
  const i = process.argv.indexOf(name);
  return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}
const out = (o) => process.stdout.write(JSON.stringify(o) + "\n");
const die = (msg, code = 2) => { out({ type: "refused", text: msg }); process.exit(code); };

/** The repository working tree stands in for the GitHub contents API. */
function localGithub() {
  return {
    async list(dir = "push") {
      return readdirSync(join(REPO, dir)).filter((n) => n.endsWith(".json")).map((name) => {
        const path = `${dir}/${name}`;
        return { name, path, sha: null, size: statSync(join(REPO, path)).size, type: "file" };
      });
    },
    async text(path) { return readFileSync(join(REPO, path), "utf8"); },
    async raw(path) { const b = readFileSync(join(REPO, path)); return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength); },
    async put(path, text) {
      if (!/^harvests\/inbox\/[^/]+\.json$/.test(path)) throw new Error("the MCP host only writes results bundles to harvests/inbox/");
      mkdirSync(dirname(join(REPO, path)), { recursive: true });
      writeFileSync(join(REPO, path), text);
      out({ type: "bundle", path });
      return { sha: null, htmlUrl: null };
    },
  };
}

function build({ stateDir, live }) {
  mkdirSync(stateDir, { recursive: true });
  const storage = new FileStorage(join(stateDir, "storage.json"));
  // Results go to the local inbox; there is no PAT on this host (the flag only selects the path).
  writeGh(storage, { on: true, pat: "local-working-tree" });
  let client;
  if (live) {
    const exchange = new FileExchange({
      dir: join(stateDir, "exchange"),
      onRequest: (r) => out({ type: "request", id: r.id, endpoint: r.arguments.endpointName, kind: r.kind, file: join(stateDir, "exchange", "request.json") }),
    });
    const allowance = Number(arg("--allowance", DEFAULT_MCP_ALLOWANCE));
    client = new McpBridgeClient({ transport: exchange, pacer: new Pacer({ storage, allowance }) });
  } else {
    client = { call: async (p) => { throw new Error(`offline: ${p} was not sent`); }, batch: async (c) => { throw new Error(`offline: ${c.map((x) => x.path).join(",")} was not sent`); } };
  }
  const refuseFetch = async (url) => { throw new Error(`the MCP host makes no direct HTTP requests (${String(url).slice(0, 60)})`); };
  const deps = compose({ storage, indexedDB: new IDBFactory(), fetchImpl: refuseFetch, client, authState: AUTH.UNKNOWN, tabId: "mcp-" + process.pid, log: () => {} });
  deps.github = localGithub();
  const core = new ForgeCore({ version: "forge-mcp", storage, ...deps });
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
    const { core } = build({ stateDir: join(stateDir, "plan-scratch"), live: false });
    await core.selectManifest(entry);
    const s = core.state.selected;
    if (!s) die(core.state.openError?.text ?? "could not open the manifest");
    out({ type: "plan", manifest: entry.path, items: s.plan.map((it) => ({ idx: it.idx, entity: it.entity, slot: it.slot, name: it.name })),
          captures: { before: s.manifest.capture?.before?.length ?? 0, after: s.manifest.capture?.after?.length ?? 0 },
          images: s.images, problems: s.problems });
    process.exit(s.problems.length ? 1 : 0);
  }
  if (cmd === "jobs") {
    const { deps } = build({ stateDir, live: false });
    for (const j of deps.journal.listJobs()) out({ type: "job", jobId: j.jobId ?? j.id, state: j.state, manifest: j.manifestPath ?? null });
    return;
  }
  if (cmd === "run" || cmd === "resume") {
    const { core, deps } = build({ stateDir, live: true });
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
