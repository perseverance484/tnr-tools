// The game-connection host (src/hosts/mcp/). Socket-free: the "MCP server" here is FakeGame
// behind a stand-in that answers the way the game's callEndpoint meta-tool does
// (TheNinjaRPG app/src/libs/mcp/meta-tools.ts at 15a37ea): JSON text on success, the text
// "Error calling <endpoint>: <message>" when the procedure throws.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, existsSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { IDBFactory } from "fake-indexeddb";
import { ForgeCore } from "../src/core/core.mjs";
import { classifyError } from "../src/transport/outcome.mjs";
import { NetworkError } from "../src/transport/client.mjs";
import { AUTH } from "../src/transport/auth.mjs";
import { writeGh } from "../src/storage/compat.mjs";
import { decodeMcpAnswer, McpBridgeClient, Pacer, PACER_KEY } from "../src/hosts/mcp/bridge.mjs";
import { FileExchange, FileStorage } from "../src/hosts/mcp/exchange.mjs";
import { composeForTest } from "./compose.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { FakeGame } from "./fakegame.mjs";

/** FakeGame answered as the MCP meta-tool would. `lose` drops the answer AFTER the call ran. */
class FakeMcpServer {
  constructor(game, { lose = () => false } = {}) { this.game = game; this.lose = lose; this.requests = []; }
  async send(req) {
    this.requests.push(req);
    assert.equal(req.tool, "callEndpoint");
    const { endpointName, input } = req.arguments;
    const r = this.game.handle(endpointName, input);
    if (this.lose(req, this.requests)) return { toolError: "MCP error -32001: Request timed out" };
    if (r.ok) return { text: JSON.stringify(r.data === undefined ? {} : r.data) };
    if (r.error.zodError) return { text: `Error calling ${endpointName}: ${JSON.stringify(r.error.zodError)}` };
    // the live server's own wording for a missing session (trpc.ts enforceUserIsAuthed)
    if (r.error.code === "UNAUTHORIZED") return { text: `Error calling ${endpointName}: Unauthorized for tRPC endpoint. Path: ${endpointName}.` };
    return { text: `Error calling ${endpointName}: ${r.error.message}` };
  }
}

const MANIFEST = JSON.stringify({
  items: [
    { entity: "jutsu", slot: "create", name: "Wire A", srcId: "w-a", data: { name: "Wire A", hidden: true } },
    { entity: "jutsu", slot: "create", name: "Wire B", srcId: "w-b", data: { name: "Wire B", hidden: true } },
  ],
});
const ENTRY = { name: "45_wire.json", path: "push/45_wire.json", sha: "s", size: 1, type: "file", number: 45, text: MANIFEST };

function harness({ lose, authState = AUTH.UNKNOWN } = {}) {
  const game = new FakeGame();
  const server = new FakeMcpServer(game, { lose });
  const storage = new MemoryStorage();
  const clock = fakeClock();
  writeGh(storage, { on: true, pat: "local-working-tree" });
  const client = new McpBridgeClient({ transport: server, pacer: new Pacer({ storage, clock, sleep: async (ms) => clock.tick(ms) }) });
  const d = composeForTest({ game, storage, idb: new IDBFactory(), clock, client, authState });
  const committed = [];
  d.github = { list: async () => [], text: async () => MANIFEST, put: async (path, text) => { committed.push({ path, text }); return { sha: null }; } };
  const core = new ForgeCore({ version: "mcp-test", storage, now: clock, ...d });
  return { core, d, game, server, committed, clock, storage };
}

test("decode: JSON text is data, and undefined-as-{} survives", () => {
  assert.deepEqual(decodeMcpAnswer("jutsu.get", { text: '{"id":"x","name":"A"}\n' }), { ok: true, data: { id: "x", name: "A" } });
  assert.deepEqual(decodeMcpAnswer("jutsu.get", { text: "null" }), { ok: true, data: null });
  const m = decodeMcpAnswer("jutsu.create", { text: '{"success":true,"message":"abcdefghijklmnopqrstu"}' }, { mutation: true });
  assert.equal(m.data.message, "abcdefghijklmnopqrstu");
});

test("decode: the game's own wording recovers the error codes Forge acts on", () => {
  const code = (text, path = "jutsu.update") => decodeMcpAnswer(path, { text }).error.code;
  assert.equal(code("Error calling jutsu.update: You're moving too fast! You were fined 10 ryo (pocket) and 0 ryo (bank). Slow down to avoid further fines."), "TOO_MANY_REQUESTS");
  assert.equal(code("Error calling jutsu.get: Too many requests for this page. Please wait a moment and try again."), "TOO_MANY_REQUESTS");
  assert.equal(code("Error calling profile.getAi: Unauthorized for tRPC endpoint. Path: profile.getAi."), "UNAUTHORIZED");
  assert.equal(code("Insufficient permissions: jutsu.update is a mutation and requires authentication or write scope. Current scopes: none"), "UNAUTHORIZED");
  assert.equal(code("Error calling item.getItemWithCraftingRequirements: Item not found"), "NOT_FOUND");
  assert.equal(code("Missing required fields for jutsu.update: id"), "BAD_REQUEST");
  assert.equal(code("Error calling jutsu.update: Something odd happened"), "MCP_ERROR");
  // and they classify the way the browser path's codes do
  assert.equal(classifyError(decodeMcpAnswer("x.y", { text: "Error calling x.y: You are moving too fast" }).error), "RATE_LIMITED");
  assert.equal(classifyError(decodeMcpAnswer("x.y", { text: "Insufficient permissions: x" }).error), "SESSION");
  assert.equal(classifyError(decodeMcpAnswer("x.y", { text: "Endpoint not found: x.y. Use listRouterEndpoints" }).error), "CLIENT_BUG");
  assert.equal(classifyError(decodeMcpAnswer("x.y", { text: "Error calling x.y: Please complete registration." }).error), "SESSION");
});

test("decode: a zod failure keeps its issues for the runner's message", () => {
  const issues = [{ code: "too_small", path: ["name"], message: "Too small" }];
  const e = decodeMcpAnswer("jutsu.update", { text: `Error calling jutsu.update: ${JSON.stringify(issues)}` }).error;
  assert.equal(e.code, "BAD_REQUEST");
  assert.deepEqual(e.zodError, issues);
  assert.equal(classifyError(e), "VALIDATION");
});

test("decode: a failed tool call is a definite 429 only when the MCP layer said so; otherwise ambiguous", () => {
  assert.equal(decodeMcpAnswer("jutsu.update", { toolError: "HTTP 429 Too many requests" }, { mutation: true }).error.code, "TOO_MANY_REQUESTS");
  assert.throws(() => decodeMcpAnswer("jutsu.update", { toolError: "request timed out" }, { mutation: true }), NetworkError);
  // an undecodable mutation answer stays ambiguous, never a verdict
  assert.throws(() => decodeMcpAnswer("jutsu.update", { text: "<html>gateway</html>" }, { mutation: true }), /not JSON/);
  assert.equal(decodeMcpAnswer("jutsu.get", { text: "<html>" }).error.code, "MALFORMED_ELEMENT");
});

test("a whole job runs through the game connection: auth probe, creates, read-back, bundle", async () => {
  const { core, d, server, committed } = harness();
  await core.recheckAuth();
  assert.equal(d.auth.state, AUTH.READY, "the probe went over the connection and was accepted");
  assert.equal(server.requests[0].arguments.endpointName, "profile.getAi");
  await core.selectManifest(ENTRY);
  assert.deepEqual(core.state.selected.problems, []);
  await core.startJob();
  const job = d.journal.get(core.state.jobId);
  assert.equal(job.state, "DONE");
  assert.ok(job.items.every((i) => i.state === "VERIFIED"));
  assert.ok(server.requests.every((r) => r.tool === "callEndpoint" && typeof r.arguments.endpointName === "string"));
  assert.ok(server.requests.some((r) => r.kind === "mutation" && r.arguments.endpointName === "jutsu.create"));
  assert.equal(committed.length, 1);
  assert.equal(JSON.parse(committed[0].text).outcome, "success");
});

test("signed out over the connection: the gate holds and no write is sent", async () => {
  const { core, d, game, server } = harness();
  game.signedOut = true;
  await core.recheckAuth();
  assert.equal(d.auth.state, AUTH.SIGNED_OUT);
  await core.selectManifest(ENTRY);
  await core.startJob();
  assert.ok(!server.requests.some((r) => r.kind === "mutation"), "nothing was written");
});

test("an answer lost after the write landed pauses as ambiguous, and resume adopts it", async () => {
  // the first create's answer is lost after the game applied it
  let lost = false;
  const lose = (req) => { if (!lost && req.arguments.endpointName === "jutsu.create") { lost = true; return true; } return false; };
  const { core, d, game } = harness({ lose });
  await core.recheckAuth();
  await core.selectManifest(ENTRY);
  await core.startJob();
  const jobId = core.state.jobId;
  let job = d.journal.get(jobId);
  assert.notEqual(job.state, "DONE", "a lost answer is never reported as finished");
  assert.equal(job.items[0].state, "SENT");
  assert.equal(game.tables.jutsu.size, 1, "the write did land");
  await core.resumeJob(jobId);
  job = d.journal.get(jobId);
  assert.equal(job.state, "DONE");
  assert.equal(game.tables.jutsu.size, 2, "the landed write was adopted, not duplicated");
});

test("the pacer keeps the whole wire under the MCP limit, across restarts", async () => {
  const storage = new MemoryStorage();
  const clock = fakeClock();
  const slept = [];
  const p = new Pacer({ storage, clock, allowance: 3, sleep: async (ms) => { slept.push(ms); clock.tick(ms); } });
  for (let i = 0; i < 3; i++) await p.acquire();
  assert.deepEqual(slept, []);
  const again = new Pacer({ storage, clock, allowance: 3, sleep: async (ms) => { slept.push(ms); clock.tick(ms); } });
  await again.acquire();
  assert.equal(slept.length, 1, "a fresh process still sees the window the first one used");
  assert.ok(slept[0] > 59_000);
  assert.ok(JSON.parse(storage.getItem(PACER_KEY)).length <= 3);
  assert.throws(() => new Pacer({ storage, allowance: 30 }), /allowance/);
});

test("the file hand-off: one request, answered verbatim, stale answers ignored", async () => {
  const dir = mkdtempSync(join(tmpdir(), "forge-mcp-"));
  writeFileSync(join(dir, "answer-old-1.txt"), '{"stale":true}'); // left by an earlier process
  const x = new FileExchange({ dir, pollMs: 5, runId: "new" });
  const p = x.send({ seq: 1, tool: "callEndpoint", arguments: { endpointName: "jutsu.get", input: { id: "abc" } }, kind: "query" });
  const req = JSON.parse(readFileSync(join(dir, "request.json"), "utf8"));
  assert.equal(req.id, "new-1");
  assert.deepEqual(req.arguments, { endpointName: "jutsu.get", input: { id: "abc" } });
  writeFileSync(join(dir, req.answerFile), '{"id":"abc"}\n');
  assert.deepEqual(await p, { text: '{"id":"abc"}\n' });
  assert.ok(!existsSync(join(dir, "request.json")), "the request is cleared once answered");
  const q = x.send({ seq: 2, tool: "callEndpoint", arguments: { endpointName: "jutsu.get" }, kind: "query" });
  writeFileSync(join(dir, "answer-new-2.error.txt"), "connector unavailable");
  assert.deepEqual(await q, { toolError: "connector unavailable" });
});

test("file storage survives a restart", () => {
  const dir = mkdtempSync(join(tmpdir(), "forge-mcp-s-"));
  const a = new FileStorage(join(dir, "s.json"));
  a.setItem("k", "v"); a.setItem("n", 1);
  const b = new FileStorage(join(dir, "s.json"));
  assert.equal(b.getItem("k"), "v"); assert.equal(b.getItem("n"), "1"); assert.equal(b.length, 2);
  b.removeItem("k");
  assert.equal(new FileStorage(join(dir, "s.json")).getItem("k"), null);
});

test("stripWireDates drops ISO timestamp strings from profile.updateAi data only", async () => {
  const { stripWireDates } = await import("../src/hosts/mcp/bridge.mjs");
  const input = { id: "a", data: { userId: "a", username: "An Absence", createdAt: "2026-11-07T23:49:59.078Z", regenAt: "2026-11-07T23:49:59Z", travelFinishAt: null, npcTitle: "2026", jutsus: ["x"] } };
  const out = stripWireDates("profile.updateAi", input);
  assert.deepEqual(out, { id: "a", data: { userId: "a", username: "An Absence", travelFinishAt: null, npcTitle: "2026", jutsus: ["x"] } });
  assert.equal(input.data.createdAt, "2026-11-07T23:49:59.078Z"); // caller's object untouched
  assert.equal(stripWireDates("jutsu.update", input), input);
  assert.equal(stripWireDates("profile.updateAi", undefined), undefined);
});
