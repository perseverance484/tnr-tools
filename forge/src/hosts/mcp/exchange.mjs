// Node-side plumbing for the game-connection host: durable storage on disk, and the file
// hand-off through which the MCP client (the session that holds the game connection) answers
// each call. Nothing here talks to the network.
//
// THE HAND-OFF, one call at a time:
//   1. Forge writes <dir>/request.json:
//        {id, tool: "callEndpoint", arguments: {endpointName, input}, kind, answerFile, errorFile}
//   2. The MCP client makes exactly that tool call with exactly those arguments.
//   3. It writes the tool result's text, VERBATIM, to <dir>/<answerFile>; or, when the tool call
//      itself failed, the failure text to <dir>/<errorFile>.
//   4. Forge reads the answer, removes both files, and moves on.
// With an `answerer` (transcript.mjs), step 3 happens here: the answer is taken from the session's
// own record of the call and written to the answer file unchanged. Writing it by hand still works.
// The id carries a per-process run id, so an answer left behind by an earlier process can never
// be taken as the answer to a new request.

import { existsSync, mkdirSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { randomBytes } from "node:crypto";

const sleepMs = (ms) => new Promise((r) => setTimeout(r, ms));

function writeAtomic(path, text) {
  const tmp = path + ".tmp-" + process.pid;
  writeFileSync(tmp, text);
  renameSync(tmp, path);
}

/** localStorage over one JSON file, flushed on every write (the journal is write-ahead). */
export class FileStorage {
  constructor(path) {
    this.path = path;
    this._m = new Map();
    if (existsSync(path)) {
      const o = JSON.parse(readFileSync(path, "utf8"));
      for (const [k, v] of Object.entries(o)) this._m.set(k, String(v));
    }
  }
  get length() { return this._m.size; }
  key(i) { return Array.from(this._m.keys())[i] ?? null; }
  getItem(k) { return this._m.has(k) ? this._m.get(k) : null; }
  setItem(k, v) { this._m.set(k, String(v)); this._flush(); }
  removeItem(k) { this._m.delete(k); this._flush(); }
  clear() { this._m.clear(); this._flush(); }
  _flush() { writeAtomic(this.path, JSON.stringify(Object.fromEntries(this._m))); }
}

export class FileExchange {
  /**
   * @param {object} o
   * @param {string} o.dir         where request.json and answers live
   * @param {number} [o.pollMs]    how often to look for an answer
   * @param {number} [o.timeoutMs] give up on one answer after this long (the call is then
   *   treated as a network failure: ambiguous for a mutation, which reconciliation settles)
   * @param {(req: object) => void} [o.onRequest]  told when a request is waiting
   * @param {{mark: () => void, poll: (args: object) => ({text: string}|{toolError: string}|null)}} [o.answerer]
   *   finds the answer in the session's own record (TranscriptAnswerer)
   */
  constructor({ dir, pollMs = 500, timeoutMs = 30 * 60_000, onRequest = null, answerer = null, runId = randomBytes(4).toString("hex") }) {
    mkdirSync(dir, { recursive: true });
    Object.assign(this, { dir, pollMs, timeoutMs, onRequest, answerer, runId });
  }

  async send(req) {
    const id = `${this.runId}-${req.seq}`;
    const answerFile = `answer-${id}.txt`;
    const errorFile = `answer-${id}.error.txt`;
    const reqPath = join(this.dir, "request.json");
    const full = { id, tool: req.tool, arguments: req.arguments, kind: req.kind, answerFile, errorFile };
    if (this.answerer) this.answerer.mark(); // before the request exists, so no later call is missed
    writeAtomic(reqPath, JSON.stringify(full, null, 1));
    if (this.onRequest) { try { this.onRequest(full); } catch { /* observer only */ } }
    const started = Date.now();
    const a = join(this.dir, answerFile);
    const e = join(this.dir, errorFile);
    for (;;) {
      if (existsSync(e)) { const toolError = readFileSync(e, "utf8"); this._clear(reqPath, a, e); return { toolError }; }
      if (existsSync(a)) { const text = readFileSync(a, "utf8"); this._clear(reqPath, a, e); return { text }; }
      if (this.answerer) {
        const got = this.answerer.poll(req.arguments);
        if (got) { writeAtomic(got.toolError !== undefined ? e : a, got.toolError ?? got.text); continue; }
      }
      if (Date.now() - started > this.timeoutMs) {
        this._clear(reqPath);
        throw new Error(`no answer to ${req.arguments.endpointName} (${id}) within ${Math.round(this.timeoutMs / 1000)} s`);
      }
      await sleepMs(this.pollMs);
    }
  }

  _clear(...paths) { for (const p of paths) rmSync(p, { force: true }); }
}
