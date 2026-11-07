// The game-connection host's two durability fixes:
//   - answers taken from the session's own record of each call (hosts/mcp/transcript.mjs), so
//     nothing is copied by hand, the large "saved to a file" answers included;
//   - capture cache and capture snapshots kept on disk (hosts/mcp/idbfile.mjs), so a job that
//     crashes and resumes in a new process still exports its full captures.
import { test } from "node:test";
import assert from "node:assert/strict";
import { appendFileSync, mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { IDBFactory } from "fake-indexeddb";
import { ForgeCore } from "../src/core/core.mjs";
import { AUTH } from "../src/transport/auth.mjs";
import { writeGh } from "../src/storage/compat.mjs";
import { CaptureCache, snapshotKey } from "../src/storage/captures.mjs";
import { McpBridgeClient, Pacer } from "../src/hosts/mcp/bridge.mjs";
import { FileExchange, FileStorage } from "../src/hosts/mcp/exchange.mjs";
import { FileIDB } from "../src/hosts/mcp/idbfile.mjs";
import { TranscriptAnswerer, canonical, sameCall } from "../src/hosts/mcp/transcript.mjs";
import { composeForTest } from "./compose.mjs";
import { fakeClock } from "./shim.mjs";
import { FakeGame } from "./fakegame.mjs";

const tmp = (p) => mkdtempSync(join(tmpdir(), p));

// ------------------------------------------------------------------ transcript answers

/** A transcript in the shape Claude Code writes: one JSON record per line. */
function transcript() {
  const dir = tmp("forge-tr-");
  const path = join(dir, "session.jsonl");
  writeFileSync(path, JSON.stringify({ type: "system", message: { content: "start" } }) + "\n");
  let n = 0;
  const t = {
    dir, path,
    use(input, name = "mcp__Tnr__callEndpoint") {
      const id = "toolu_" + ++n;
      appendFileSync(path, JSON.stringify({ type: "assistant", message: { content: [{ type: "tool_use", id, name, input }] } }) + "\n");
      return id;
    },
    result(id, content, extra = {}) {
      appendFileSync(path, JSON.stringify({ type: "user", message: { content: [{ type: "tool_result", tool_use_id: id, content, ...extra }] } }) + "\n");
    },
    call(input, content, extra) { const id = t.use(input); t.result(id, content, extra); return id; },
  };
  return t;
}
const ARGS = { endpointName: "jutsu.get", input: { id: "abc", hidden: true } };

test("canonical inputs compare regardless of key order, and filtered calls never match", () => {
  assert.equal(canonical({ b: 1, a: [1, { d: 2, c: 3 }] }), canonical({ a: [1, { c: 3, d: 2 }], b: 1 }));
  assert.notEqual(canonical(undefined), canonical({}), "an absent input is not an empty one");
  assert.ok(sameCall(ARGS, { endpointName: "jutsu.get", input: { hidden: true, id: "abc" } }));
  assert.ok(!sameCall(ARGS, { ...ARGS, select: ["name"] }));
  assert.ok(!sameCall(ARGS, { ...ARGS, maxLength: 100 }));
  assert.ok(!sameCall(ARGS, { endpointName: "jutsu.get", input: { id: "abd", hidden: true } }));
});

test("transcript: the call made after the request answers it, verbatim; an earlier read does not", () => {
  const t = transcript();
  t.call(ARGS, [{ type: "text", text: '{"id":"abc","name":"OLD"}' }]); // before the request
  const a = new TranscriptAnswerer({ path: t.path });
  a.mark();
  assert.equal(a.poll(ARGS), null, "nothing recorded since the mark");
  t.call({ endpointName: "jutsu.get", input: { id: "abc" } }, [{ type: "text", text: "wrong input" }]);
  t.call({ ...ARGS, select: ["name"] }, [{ type: "text", text: "filtered" }]);
  const body = '{"name":"Ünïcode 𝚅 \\"quoted\\"","id":"abc"}\n';
  t.call({ endpointName: "jutsu.get", input: { hidden: true, id: "abc" } }, [{ type: "text", text: body }]);
  assert.deepEqual(a.poll(ARGS), { text: body });
  assert.equal(a.poll(ARGS), null, "one call answers one request");
});

test("transcript: a string result, an is_error result, and a line still being written", () => {
  const t = transcript();
  const a = new TranscriptAnswerer({ path: t.path });
  a.mark();
  t.call(ARGS, "null");
  assert.deepEqual(a.poll(ARGS), { text: "null" });
  a.mark();
  t.call(ARGS, "MCP error -32001: Request timed out", { is_error: true });
  assert.deepEqual(a.poll(ARGS), { toolError: "MCP error -32001: Request timed out" });
  a.mark();
  const id = t.use(ARGS);
  const line = JSON.stringify({ type: "user", message: { content: [{ type: "tool_result", tool_use_id: id, content: "[1,2]" }] } });
  appendFileSync(t.path, line.slice(0, 20));
  assert.equal(a.poll(ARGS), null, "half a line is not read");
  appendFileSync(t.path, line.slice(20) + "\n");
  assert.deepEqual(a.poll(ARGS), { text: "[1,2]" });
});

test("transcript: a large answer saved to a file is read from that file, and only when it checks out", () => {
  const t = transcript();
  const results = join(t.dir, "session", "tool-results");
  mkdirSync(results, { recursive: true });
  const big = JSON.stringify(Array.from({ length: 3000 }, (_, i) => ({ id: "j" + i, name: "Jutsu " + i + " ✦" })));
  const file = join(results, "mcp-Tnr-callEndpoint-1.txt");
  writeFileSync(file, big);
  const notice = (chars, path) => `Error: result (${chars.toLocaleString("en-US")} characters across 1 line) exceeds maximum allowed tokens. Output has been saved to ${path}.\nFormat: Plain text\nSearch within the file`;
  const notes = [];
  const a = new TranscriptAnswerer({ path: t.path, onNote: (n) => notes.push(n) });

  a.mark();
  t.call(ARGS, notice(big.length, file));
  assert.deepEqual(a.poll(ARGS), { text: big });

  a.mark();
  t.call(ARGS, notice(big.length + 1, file)); // truncated or not the same output
  assert.equal(a.poll(ARGS), null);
  assert.match(notes.at(-1).reason, /characters/);

  a.mark();
  const outside = join(tmp("forge-out-"), "x.txt");
  writeFileSync(outside, big);
  t.call(ARGS, notice(big.length, outside));
  assert.equal(a.poll(ARGS), null);
  assert.match(notes.at(-1).reason, /outside the session folder/);
});

test("the file hand-off answers itself from the transcript, and a hand-written answer still works", async () => {
  const t = transcript();
  const dir = tmp("forge-x-");
  const x = new FileExchange({ dir, pollMs: 5, runId: "r", answerer: new TranscriptAnswerer({ path: t.path }) });
  const p = x.send({ seq: 1, tool: "callEndpoint", arguments: ARGS, kind: "query" });
  setTimeout(() => t.call(ARGS, [{ type: "text", text: '{"id":"abc"}' }]), 20);
  assert.deepEqual(await p, { text: '{"id":"abc"}' });
  const q = x.send({ seq: 2, tool: "callEndpoint", arguments: ARGS, kind: "query" });
  writeFileSync(join(dir, "answer-r-2.txt"), "by hand");
  assert.deepEqual(await q, { text: "by hand" });
});

// ------------------------------------------------------------------ durable captures

test("captures and snapshots survive a new process; deletes, clears and aborts are honoured", async () => {
  const path = join(tmp("forge-idb-"), "captures.idb");
  const one = await FileIDB.open(path);
  const c1 = new CaptureCache(one.factory);
  await c1.put({ path: "jutsu.get", id: "a", data: { id: "a", at: new Date(5) } });
  await c1.put({ path: "jutsu.get", id: "b", data: { id: "b" } });
  await c1.putSnapshot({ key: snapshotKey("job1", "before", 0), jobId: "job1", phase: "before", ordinal: 0, path: "jutsu.get", id: "a", data: { id: "a", name: "kept" } });
  await c1.delete("jutsu.get", "b");
  await assert.rejects(c1._tx("readwrite", async (s) => { s.put({ key: "never", path: "x" }); s.transaction.abort(); }));
  c1.close();

  const two = await FileIDB.open(path); // a new process
  const c2 = new CaptureCache(two.factory);
  assert.deepEqual((await c2.getSnapshot(snapshotKey("job1", "before", 0))).data, { id: "a", name: "kept" });
  const a = await c2.get("jutsu.get", "a");
  assert.ok(a.data.at instanceof Date, "dates come back as dates");
  assert.equal(await c2.get("jutsu.get", "b"), null, "the delete was kept");
  const never = await c2._tx("readonly", (s) => new Promise((ok) => { const r = s.get("never"); r.onsuccess = () => ok(r.result); }));
  assert.equal(never, undefined, "an aborted transaction left nothing behind");
  await c2.clear();
  c2.close();

  const three = await FileIDB.open(path);
  const c3 = new CaptureCache(three.factory);
  assert.equal(await c3.get("jutsu.get", "a"), null, "the clear was kept");
  assert.ok(await c3.getSnapshot(snapshotKey("job1", "before", 0)), "clearing the read cache never touches a snapshot");
  c3.close();

  writeFileSync(path, "not a mirror");
  await assert.rejects(FileIDB.open(path), /refusing to start with an empty one/);
});

/** FakeGame answered as the MCP meta-tool would. */
class FakeMcpServer {
  constructor(game, lose = () => false) { this.game = game; this.lose = lose; }
  async send(req) {
    const { endpointName, input } = req.arguments;
    const r = this.game.handle(endpointName, input);
    if (this.lose(req)) return { toolError: "MCP error -32001: Request timed out" };
    if (r.ok) return { text: JSON.stringify(r.data === undefined ? {} : r.data) };
    return { text: `Error calling ${endpointName}: ${r.error.message}` };
  }
}

const SEED = "fkseed00000000000001";
const MANIFEST = JSON.stringify({
  capture: { before: [{ proc: "jutsu.get", input: { id: SEED }, id: SEED, persist: "full" }] },
  items: [
    { entity: "jutsu", slot: "create", name: "Wire A", srcId: "w-a", data: { name: "Wire A", hidden: true } },
    { entity: "jutsu", slot: "create", name: "Wire B", srcId: "w-b", data: { name: "Wire B", hidden: true } },
  ],
});
const ENTRY = { name: "46_durable.json", path: "push/46_durable.json", sha: "s", size: 1, type: "file", number: 46, text: MANIFEST };

/** One "process": its own storage handle, IndexedDB and Forge, over the same game and state dir. */
function proc({ game, dir, idb, lose }) {
  const storage = new FileStorage(join(dir, "storage.json"));
  const clock = fakeClock();
  writeGh(storage, { on: true, pat: "local-working-tree" });
  const client = new McpBridgeClient({ transport: new FakeMcpServer(game, lose), pacer: new Pacer({ storage, clock, sleep: async (ms) => clock.tick(ms) }) });
  const d = composeForTest({ game, storage, idb, clock, client, authState: AUTH.UNKNOWN });
  const committed = [];
  d.github = { list: async () => [], text: async () => MANIFEST, put: async (path, text) => { committed.push(JSON.parse(text)); return { sha: null }; } };
  const core = new ForgeCore({ version: "mcp-test", storage, now: clock, ...d });
  return { core, d, committed };
}

async function crashThenResume(idbFor) {
  const game = new FakeGame();
  game.seed("jutsu", { id: SEED, name: "Seeded Original", hidden: false, effects: [], createdAt: new Date(0), updatedAt: new Date(0) });
  const dir = tmp("forge-crash-");
  let lost = false;
  const lose = (req) => { if (!lost && req.arguments.endpointName === "jutsu.create") { lost = true; return true; } return false; };
  const first = proc({ game, dir, idb: await idbFor(dir), lose });
  await first.core.recheckAuth();
  await first.core.selectManifest(ENTRY);
  await first.core.startJob();
  const jobId = first.core.state.jobId;
  assert.notEqual(first.d.journal.get(jobId).state, "DONE", "the lost answer stopped the job mid-run");
  // The server changes the record after the before-capture: a re-read would see a different body.
  game.tables.jutsu.get(SEED).name = "Changed Later";

  const second = proc({ game, dir, idb: await idbFor(dir) }); // a new process
  await second.core.recheckAuth();
  await second.core.resumeJob(jobId);
  assert.equal(second.d.journal.get(jobId).state, "DONE");
  assert.equal(game.tables.jutsu.size, 3, "seed plus two creates, the lost one adopted, not duplicated");
  return second.committed.at(-1).captures.find((c) => c.phase === "before");
}

test("a job that crashes and resumes in a new process still exports its full before-capture", async () => {
  const cap = await crashThenResume(async (dir) => (await FileIDB.open(join(dir, "captures.idb"))).factory);
  assert.equal(cap.persistOk, true, cap.persistError);
  assert.equal(cap.data.name, "Seeded Original", "the body read before the writes, not a re-read");
});

test("control: with the old in-memory store, the same crash loses the before-capture", async () => {
  const cap = await crashThenResume(async () => new IDBFactory());
  assert.equal(cap.persistOk, false);
  assert.match(cap.persistError, /gone/);
});
