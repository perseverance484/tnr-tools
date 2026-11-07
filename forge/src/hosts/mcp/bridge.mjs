import { Paused } from "../../runner/paused.mjs";
// The game-connection transport: Forge's runner, driven through the game's own MCP endpoint
// (https://www.theninja-rpg.com/api/mcp) instead of a signed-in browser tab.
//
// WHY THIS EXISTS. A run in the browser host stalls whenever the tab sleeps (job 102 on a
// backgrounded phone). The game publishes an MCP server whose `callEndpoint` meta-tool reaches
// every tRPC procedure through a server-side caller (studie-tech/TheNinjaRPG
// app/src/libs/mcp/handler.ts and meta-tools.ts at 15a37ea, 2026-11-06): "All game procedures are
// exposed; metadata customizes descriptions". Authentication is the operator's own OAuth grant
// to an MCP client, so nothing here ever holds a password, a cookie or a token.
//
// WHO HOLDS THE CONNECTION. Not this process. The MCP client (a Claude session with the game
// connected as a connector) owns the OAuth grant and makes the actual tool call. This client only
// turns each Forge call into a `callEndpoint` request, hands it to an injected `transport`, and
// decodes the text that comes back into the same {ok, data} | {ok:false, error} elements the
// browser transport (envelope.decodeResponse) produces, so the Runner, budget, journal and
// reconciler run unchanged.
//
// WHAT CHANGES ON THIS WIRE, and how each is mapped (meta-tools.ts executeProcedure /
// handleCallEndpoint):
//   - a result is JSON.stringify(result), undefined becoming {} (no superjson: Dates arrive as
//     ISO strings, which is also what an exported bundle carries);
//   - a thrown TRPCError arrives as the TEXT "Error calling <endpoint>: <message>" with NO code.
//     The code is recovered from the game's own message wording below. Anything unrecognised is
//     SERVER (classifyError's default): a definite refusal, never a success;
//   - the MCP layer's own refusals ("Insufficient permissions", "Endpoint not found", "Missing
//     required fields") happen BEFORE the procedure runs, so they are definite and nothing ran;
//   - the MCP endpoint limits every caller to 30 calls per rolling minute per user AND per IP
//     (route.ts), across all paths together. The tRPC per-path limiter (60/min, fines on
//     mutations) still applies inside, and Forge's Budget keeps mirroring that. The Pacer here
//     keeps the whole wire under the MCP limit on top.
//
// NO BATCHING. The MCP surface is one procedure per tool call, so batch() is sequential.

import { NetworkError } from "../../transport/client.mjs";
import { TransportError } from "../../transport/envelope.mjs";
import { procedure } from "../../transport/procedures.mjs";

export const MCP_TOOL = "callEndpoint";
export const MCP_LIMIT = 30;             // route.ts: slidingWindow(30, "60 s"), per IP and per user
export const MCP_WINDOW_MS = 60_000;
export const DEFAULT_MCP_ALLOWANCE = 20; // headroom for the operator's own MCP use and clock skew
export const PACER_KEY = "tnr_forge_mcp_sendlog_v1";

const ERROR_PREFIX = /^Error calling ([^:]+): ([\s\S]*)$/;

// The game's own wording, app/src/server/api/trpc.ts at 15a37ea.
const RATE_LIMIT_TEXT = /You're moving too fast!|You are moving too fast|You are acting too fast|Too many requests for this page|Too many sign-in attempts/;
const UNAUTHORIZED_TEXT = /^Unauthorized for tRPC endpoint\.|^No user ID or IP found for rate limit middleware/;

/**
 * Turn one MCP tool answer into a decoded element.
 *
 * @param {string} path   the procedure that was called
 * @param {{text?: string, toolError?: string}} answer  exactly what the MCP client got back:
 *   `text` is the tool result's text content, verbatim; `toolError` is set instead when the tool
 *   call itself failed (HTTP error, 429 from the MCP layer, connector error).
 * @param {{mutation?: boolean}} [opts]
 * @returns {{ok: true, data: any} | {ok: false, error: object}}
 * @throws {NetworkError} the call failed in a way that leaves a mutation ambiguous
 * @throws {TransportError} a mutation answer that is not decodable (ambiguous, as in the browser)
 */
export function decodeMcpAnswer(path, answer, { mutation = false } = {}) {
  if (!answer || typeof answer !== "object") throw new TransportError("no MCP answer", { paths: [path] });
  if (typeof answer.toolError === "string") {
    // The MCP endpoint's own 429 is returned before auth and before the procedure: nothing ran.
    if (/\b429\b|Too many requests/i.test(answer.toolError)) {
      return err(path, "TOO_MANY_REQUESTS", 429, "MCP endpoint rate limit: " + answer.toolError.slice(0, 200));
    }
    // Anything else (connector down, timeout, 5xx) may or may not have reached the procedure.
    throw new NetworkError(new Error(answer.toolError.slice(0, 300)), { paths: [path], kind: mutation ? "mutation" : "query", phase: "connect" });
  }
  if (typeof answer.text !== "string") throw new TransportError("MCP answer carries no text", { paths: [path] });
  // A file written by hand may gain a trailing newline; neither JSON nor the game's messages
  // carry meaningful outer whitespace.
  const text = answer.text.trim();

  // MCP-layer refusals: the procedure never ran.
  if (text.startsWith("Insufficient permissions:")) return err(path, "UNAUTHORIZED", 401, text);
  if (text.startsWith("Endpoint not found:")) return err(path, "NOT_FOUND", 404, `No procedure found on path "${path}" (${text})`);
  if (text.startsWith("Invalid procedure path:")) return err(path, "NOT_FOUND", 404, `No procedure found on path "${path}" (${text})`);
  if (text.startsWith("Missing required fields for ") || text.startsWith("Invalid input: expected an object")) {
    return err(path, "BAD_REQUEST", 400, text);
  }
  if (text.startsWith("Missing required argument:") || text.startsWith("Unknown tool:")) {
    return err(path, "METHOD_NOT_SUPPORTED", 400, "MCP client sent a malformed tool call: " + text);
  }

  const m = ERROR_PREFIX.exec(text);
  if (m) {
    const message = m[2];
    if (RATE_LIMIT_TEXT.test(message)) return err(path, "TOO_MANY_REQUESTS", 429, message);
    if (UNAUTHORIZED_TEXT.test(message)) return err(path, "UNAUTHORIZED", 401, message);
    if (/Please complete registration\.$/.test(message)) return err(path, "NOT_FOUND", 404, message);
    const zod = zodIssues(message);
    if (zod) return { ok: false, error: { code: "BAD_REQUEST", httpStatus: 400, message, path, zodError: zod } };
    if (/Output validation failed/.test(message)) return err(path, "INTERNAL_SERVER_ERROR", 500, message);
    if (/\bnot found\b/i.test(message)) return err(path, "NOT_FOUND", 404, message);
    return err(path, "MCP_ERROR", 500, message);
  }

  let data;
  try { data = JSON.parse(text); }
  catch (e) {
    if (mutation) throw new TransportError(`mutation answer for ${path} is not JSON: ${e.message}`, { paths: [path], snippet: text.slice(0, 200) });
    return { ok: false, error: { code: "MALFORMED_ELEMENT", httpStatus: 200, message: "MCP answer is not JSON: " + e.message, path, zodError: null, raw: text.slice(0, 200) } };
  }
  return { ok: true, data };
}

function err(path, code, httpStatus, message) {
  return { ok: false, error: { code, httpStatus, message, path, zodError: null } };
}

/** A tRPC zod failure's message is the JSON array of issues. */
function zodIssues(message) {
  const t = message.trim();
  if (!t.startsWith("[")) return null;
  try {
    const a = JSON.parse(t);
    if (Array.isArray(a) && a.length && a.every((z) => z && typeof z.message === "string")) return a;
  } catch { /* not zod */ }
  return null;
}

/**
 * Keeps the whole wire under the MCP endpoint's limit: at most `allowance` sends in any rolling
 * window. The send log lives in storage and is written BEFORE a request leaves, so a restarted
 * process cannot overspend a window an earlier process already used.
 */
export class Pacer {
  constructor({ storage, clock = () => Date.now(), sleep = (ms) => new Promise((r) => setTimeout(r, ms)), allowance = DEFAULT_MCP_ALLOWANCE, windowMs = MCP_WINDOW_MS } = {}) {
    if (!Number.isInteger(allowance) || allowance < 1 || allowance >= MCP_LIMIT) throw new Error(`MCP allowance must be an integer from 1 to ${MCP_LIMIT - 1}`);
    Object.assign(this, { storage, clock, sleep, allowance, windowMs });
  }
  _load() { try { return JSON.parse(this.storage.getItem(PACER_KEY) || "[]"); } catch { return []; } }
  _save(a) { this.storage.setItem(PACER_KEY, JSON.stringify(a)); }
  /** How long until one more send fits. 0 when it fits now. */
  wait() {
    const now = this.clock();
    const recent = this._load().filter((t) => now - t < this.windowMs).sort((a, b) => a - b);
    if (recent.length < this.allowance) return 0;
    return recent[recent.length - this.allowance] + this.windowMs - now + 1;
  }
  async acquire() {
    for (let w = this.wait(); w > 0; w = this.wait()) await this.sleep(w);
    const now = this.clock();
    const kept = this._load().filter((t) => now - t < this.windowMs);
    kept.push(now);
    this._save(kept);
  }
}

/**
 * Drop-in for TrpcClient: call(path, input) and batch(calls), same decoded elements.
 *
 * @param {object} d
 * @param {{send: (req: object) => Promise<{text?: string, toolError?: string}>}} d.transport
 *   delivers one MCP tool call and returns what came back. Requests are plain data:
 *   {seq, tool: "callEndpoint", arguments: {endpointName, input}, kind}.
 * @param {Pacer} [d.pacer]
 * @param {(rec: object) => void} [d.onExchange]  observer, no secrets
 */
export class McpBridgeClient {
  constructor({ transport, pacer = null, onExchange = null }) {
    if (!transport || typeof transport.send !== "function") throw new TransportError("McpBridgeClient needs a transport with send()");
    Object.assign(this, { transport, pacer, onExchange });
    this.seq = 0;
  }

  async call(path, input) { const [r] = await this.batch([{ path, input }]); return r; }

  async batch(calls) {
    const out = [];
    for (let i = 0; i < calls.length; i++) {
      try { out.push(await this._one(calls[i])); }
      catch (e) { e.results = out.slice(); e.failedIndices = [i]; throw e; }
    }
    return out;
  }

  async _one({ path, input }) {
    const kind = procedure(path).kind; // throws on an unknown path, before anything is sent
    if (this.pacer) await this.pacer.acquire();
    const seq = ++this.seq;
    const args = { endpointName: path };
    if (input !== undefined) args.input = input;
    let answer;
    try { answer = await this.transport.send({ seq, tool: MCP_TOOL, arguments: args, kind }); }
    catch (e) {
      this._observe({ kind, paths: [path], status: null, error: String(e && e.message) });
      // A run-lock refusal at the wire (mcp_run.mjs) was never sent: it pauses the job as itself,
      // not as a connection failure that would leave a mutation ambiguous.
      if (e instanceof Paused) throw e;
      if (e instanceof NetworkError || e instanceof TransportError) throw e;
      throw new NetworkError(e, { paths: [path], kind, phase: "connect" });
    }
    const el = decodeMcpAnswer(path, answer, { mutation: kind === "mutation" });
    this._observe({ kind, paths: [path], status: el.ok ? 200 : el.error.httpStatus, outcomes: [el.ok ? "ok" : el.error.code] });
    return el;
  }

  _observe(rec) { if (this.onExchange) { try { this.onExchange(rec); } catch { /* never break transport */ } } }
}

/**
 * The run lock at the wire (RUL-2026-11-07-133): the lease is checked after the pacer's wait, at the
 * last moment before a request is handed to the session, because a pacer sleep can outlast the
 * stop margin. A refusal throws a Paused-shaped error, which the bridge passes through unsent.
 */
export function leaseGatedTransport(transport, lease) {
  return {
    send(req) {
      const why = lease.check();
      if (why) throw new Paused("RUN_LOCK", { detail: why, sent: false, notDispatched: true });
      return transport.send(req);
    },
  };
}
