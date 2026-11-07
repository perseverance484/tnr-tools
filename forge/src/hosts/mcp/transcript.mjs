// Answers the file hand-off from the session's own record, so no answer is ever copied by hand.
//
// The session holding the game connection makes each callEndpoint call. Claude Code records the
// call and its exact result in the session transcript (a JSONL file under ~/.claude/projects/).
// Copying the result into the answer file by hand is the weak point of the hand-off: the text has
// to arrive byte for byte, and a large answer does not even appear in the conversation (the tool
// result is replaced by a notice that the output was saved to a file). This reads the transcript
// instead:
//
//   1. When a request is written, the transcript's current size is marked. Only calls recorded
//      after that point can answer it, so an earlier read of the same record never does.
//   2. A tool_use whose name ends in "__callEndpoint" answers the request when its endpointName
//      and input are exactly the request's (key order aside) and it carries no select, search or
//      maxLength (a filtered answer is not the answer). Each call answers at most one request.
//   3. Its tool_result text is the answer. When it is the "Output has been saved to <file>"
//      notice, the saved file is the answer, but only if the file sits under the transcript's own
//      folder and its length is exactly the character count the notice states; otherwise the call
//      is passed over and the session can answer by hand. A result marked is_error is a failed
//      tool call and goes to the error file, as the hand-off defines.
//
// Nothing here edits, trims or re-encodes an answer: what the game returned is what Forge reads.

import { closeSync, existsSync, openSync, readSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve, sep } from "node:path";
import { homedir } from "node:os";

const SAVED = /^Error: result \(([\d,]+) characters[^)]*\) exceeds maximum allowed tokens\. Output has been saved to (\S+?\.txt)\./;
const FILTERS = ["select", "search", "maxLength"];

/** JSON with object keys sorted, for comparing inputs regardless of key order. */
export function canonical(v) {
  if (v === undefined) return "undefined";
  if (Array.isArray(v)) return "[" + v.map(canonical).join(",") + "]";
  if (v && typeof v === "object") return "{" + Object.keys(v).sort().map((k) => JSON.stringify(k) + ":" + canonical(v[k])).join(",") + "}";
  return JSON.stringify(v);
}

/** Whether a recorded callEndpoint call is exactly the requested one. */
export function sameCall(args, used) {
  if (!used || typeof used !== "object") return false;
  if (FILTERS.some((f) => used[f] !== undefined)) return false;
  return used.endpointName === args.endpointName && canonical(used.input) === canonical(args.input);
}

/** Find this session's transcript: ~/.claude/projects/<any>/<session id>.jsonl. */
export function findTranscript({ sessionId = process.env.CLAUDE_CODE_SESSION_ID, home = process.env.CLAUDE_CONFIG_DIR || join(homedir(), ".claude") } = {}) {
  if (!sessionId) throw new Error("no session id (CLAUDE_CODE_SESSION_ID is not set); pass --transcript PATH");
  const root = join(home, "projects");
  if (existsSync(root)) {
    for (const d of readdirSync(root)) {
      const p = join(root, d, sessionId + ".jsonl");
      if (existsSync(p)) return p;
    }
  }
  throw new Error(`no transcript for session ${sessionId} under ${root}; pass --transcript PATH`);
}

export class TranscriptAnswerer {
  /**
   * @param {object} o
   * @param {string} o.path  the session transcript (JSONL)
   * @param {(note: object) => void} [o.onNote]  told when a call is answered or passed over
   */
  constructor({ path, onNote = null }) {
    this.path = resolve(path);
    this.folder = dirname(this.path) + sep;
    this.onNote = onNote;
    this.pos = 0;
    this.rest = "";
    this.used = new Set();   // tool_use ids that already answered (or were passed over)
    this.calls = new Map();  // tool_use id -> callEndpoint arguments, seen since the mark
    this.results = new Map(); // tool_use id -> tool_result block, seen since the mark
  }

  /** Called as a request is written: only what is recorded after this point can answer it. */
  mark() {
    this.pos = existsSync(this.path) ? statSync(this.path).size : 0;
    this.rest = "";
    this.calls.clear();
    this.results.clear();
  }

  /**
   * Look for the answer to `args` ({endpointName, input}) recorded since the mark.
   * @returns {{text: string} | {toolError: string} | null}
   */
  poll(args) {
    this._read();
    for (const [id, used] of this.calls) {
      if (this.used.has(id) || !sameCall(args, used)) continue;
      const block = this.results.get(id);
      if (!block) continue; // the call is recorded, its result not yet
      this.used.add(id);
      const got = this._answer(block);
      if (got) { this._note({ type: "answered", via: "transcript", call: id, chars: (got.text ?? got.toolError).length, error: !!got.toolError }); return got; }
    }
    return null;
  }

  _note(n) { if (this.onNote) { try { this.onNote(n); } catch { /* observer only */ } } }

  _read() {
    if (!existsSync(this.path)) return;
    const size = statSync(this.path).size;
    if (size <= this.pos) return;
    const fd = openSync(this.path, "r");
    try {
      const buf = Buffer.alloc(size - this.pos);
      readSync(fd, buf, 0, buf.length, this.pos);
      this.pos = size;
      const text = this.rest + buf.toString("utf8");
      const cut = text.lastIndexOf("\n");
      // A line still being written stays in `rest` until its newline arrives. (A UTF-8 sequence
      // split across reads can only fall in that unfinished tail, never in a complete line.)
      this.rest = cut < 0 ? text : text.slice(cut + 1);
      if (cut >= 0) for (const line of text.slice(0, cut).split("\n")) this._line(line);
    } finally { closeSync(fd); }
  }

  _line(line) {
    if (!line.trim()) return;
    let rec;
    try { rec = JSON.parse(line); } catch { return; }
    const content = rec?.message?.content;
    if (!Array.isArray(content)) return;
    for (const b of content) {
      if (b?.type === "tool_use" && typeof b.name === "string" && b.name.endsWith("__callEndpoint")) this.calls.set(b.id, b.input);
      else if (b?.type === "tool_result" && typeof b.tool_use_id === "string") this.results.set(b.tool_use_id, b);
    }
  }

  _answer(block) {
    let text;
    if (typeof block.content === "string") text = block.content;
    else if (Array.isArray(block.content) && block.content.every((c) => c?.type === "text")) text = block.content.map((c) => c.text).join("");
    else { this._note({ type: "passed-over", reason: "the result is not plain text" }); return null; }
    if (block.is_error === true) return { toolError: text };
    const saved = SAVED.exec(text);
    if (!saved) return { text };
    const file = resolve(saved[2]);
    const want = Number(saved[1].replace(/,/g, ""));
    if (!file.startsWith(this.folder)) { this._note({ type: "passed-over", reason: "the saved output is outside the session folder" }); return null; }
    if (!existsSync(file)) { this._note({ type: "passed-over", reason: "the saved output file is missing" }); return null; }
    const body = readFileSync(file, "utf8");
    if (body.length !== want) { this._note({ type: "passed-over", reason: `the saved output has ${body.length} characters, the notice says ${want}` }); return null; }
    return { text: body };
  }
}
