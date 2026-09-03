// Outcome reading (spec section 8). The verdict for a mutation is baseServerResponse.success
// on the DECODED body. On create, message carries the new id; on failure it carries a
// sentence. HTTP status is never consulted for the verdict.

export const NANOID_RE = /^[A-Za-z0-9_-]{21}$/; // nanoid() default length; tnr-tools ID_LEN = 21

export class OutcomeError extends Error {
  constructor(message, info = {}) { super(message); this.name = "OutcomeError"; Object.assign(this, info); }
}

/** Is this decoded data a baseServerResponse? */
export function isBaseServerResponse(v) {
  return !!v && typeof v === "object" && typeof v.success === "boolean" && typeof v.message === "string";
}

/**
 * Interpret a decoded mutation outcome.
 * @param {{ok: boolean, data?: any, error?: object}} decoded  one element from decodeResponse
 * @returns {{ kind: "ok"|"refused"|"error", message: string, id?: string, error?: object }}
 *   ok       success:true. For a create, id is populated when message is nanoid-shaped.
 *   refused  success:false delivered as HTTP 200: a role miss, a guard, a name collision.
 *   error    a tRPC error element: validation (zodError), TOO_MANY_REQUESTS, UNAUTHORIZED, etc.
 */
export function readMutation(decoded) {
  if (!decoded.ok) return { kind: "error", message: decoded.error.message, error: decoded.error };
  const d = decoded.data;
  if (!isBaseServerResponse(d)) {
    throw new OutcomeError("mutation returned something other than baseServerResponse", { data: d });
  }
  if (!d.success) return { kind: "refused", message: d.message };
  const out = { kind: "ok", message: d.message };
  if (NANOID_RE.test(d.message)) out.id = d.message;
  return out;
}

/**
 * For a create specifically: success:true whose message is NOT an id is a contract break,
 * not a success. Never let it pass as one.
 */
export function readCreate(decoded) {
  const o = readMutation(decoded);
  if (o.kind === "ok" && !o.id) {
    throw new OutcomeError("create reported success but message is not an id: " + JSON.stringify(o.message).slice(0, 80), { outcome: o });
  }
  return o;
}

/** Classify an error element for the layers above. */
export function classifyError(error) {
  const code = error?.code;
  if (code === "TOO_MANY_REQUESTS") return "RATE_LIMITED";       // budget: hard stop, never retry
  if (code === "UNAUTHORIZED") return "SESSION";                  // cookie missing/expired: stop, tell user
  if (code === "BAD_REQUEST" && error.zodError) return "VALIDATION"; // R10: structured issues
  if (code === "METHOD_NOT_SUPPORTED") return "CLIENT_BUG";       // we sent GET to a mutation
  if (code === "NOT_FOUND") {
    const m = String(error.message || "");
    if (/^No procedure found on path/.test(m)) return "CLIENT_BUG";                       // adapter: unknown path
    if (/Please complete registration\.$/.test(m)) return "SESSION";                       // route handler: session with no UserData row
    return "NOT_FOUND";
  }
  if (code === "MALFORMED_ELEMENT") return "CLIENT_BUG";
  if (code === "INTERNAL_SERVER_ERROR" && /Output validation failed/.test(String(error.message || ""))) return "CONTRACT"; // server broke its own output schema; never retry
  return "SERVER";
}
