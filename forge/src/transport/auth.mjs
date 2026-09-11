// Authentication health for the GAME session, and nothing else.
//
// WHAT THIS FILE MAY NOT DO, and the reason it is written the way it is (brief section C).
// Forge must benefit from the browser's established authenticated context; it must never become
// a credential manager. So nothing here:
//   - reads document.cookie, or names __session or any other Clerk cookie;
//   - calls Clerk's getToken(), reads session.lastActiveToken, or touches a JWT;
//   - adds an Authorization header to a game request (CookieSession refuses one anyway);
//   - writes anything auth-derived to localStorage, sessionStorage, IndexedDB, the journal, a
//     capture, or an exported bundle.
// The ONLY things this module ever holds are (a) one of four state strings below and (b) the
// booleans it read off the page runtime to get there. Neither is credential material, and a
// static test asserts the forbidden identifiers appear nowhere in src/.
//
// TWO SIGNALS, in this order:
//
//   1. RUNTIME READINESS (free, no request). The carrier page is a real application route, so the
//      normal TNR root layout has mounted ClerkProvider and clerk-js. clerk-js publishes
//      window.Clerk with a `loaded` flag and a `session` property; the PRESENCE of a session
//      object is all that is read - never its contents. This answers "has the page's own auth
//      runtime finished starting up", which is the thing /forge could never answer, because
//      global-not-found.tsx mounts no provider at all.
//
//   2. A SERVER PROBE (one request, body discarded). Runtime readiness is a page-side belief;
//      the server's answer is the truth, and it is the same truth a protected job will meet.
//      The probe sends ONE protected query for an id that cannot exist and reads only the error
//      CODE: UNAUTHORIZED (or the route handler's "Please complete registration") means signed
//      out, anything else - including a perfectly ordinary empty answer - means the protected
//      surface accepted this session.
//
//      profile.getAi is the probe path because it is protected (routers/profile.ts:1121), carries
//      no rate limiter (`limited: false`, so a probe costs no budget a real read might need), and
//      takes a single id. PROBE_ID is a nanoid-shaped sentinel that names itself, so nothing real
//      is read: this is deliberately NOT "capture your own profile and see if it works", which
//      would pull a real user record into the client to answer a yes/no question. The decoded
//      element never leaves this file - it is not cached (the probe calls the client directly,
//      never the CachedReader), not journaled and not exported.
//
// A probe that cannot complete (network, transport, rate limit) leaves the state UNKNOWN. UNKNOWN
// is not permission: the gate treats anything other than READY as "do not send protected work",
// so a broken probe fails closed and says so, rather than letting a job discover the answer by
// sending a mutation.

import { classifyError } from "./outcome.mjs";
import { isProtected } from "./procedures.mjs";

/**
 * UNKNOWN   not established yet, or the probe could not complete. Fails closed.
 * READY     the server answered a protected procedure for this session.
 * SIGNED_OUT the server refused a protected procedure: UNAUTHORIZED, or a session with no
 *            UserData row, which cannot do content work either.
 * PROBING   a probe is in flight.
 */
export const AUTH = Object.freeze({ UNKNOWN: "unknown", PROBING: "probing", READY: "ready", SIGNED_OUT: "signed_out" });

export const PROBE_PATH = "profile.getAi";
// nanoid-shaped (21 chars of [A-Za-z0-9_-]) so it is a well-formed input, and self-describing so
// that a row with this id cannot plausibly exist. The answer is thrown away either way.
export const PROBE_ID = "forge-auth-probe-0000";

/** Thrown by the gate BEFORE anything is journaled or sent. Never ambiguous: nothing left. */
export class AuthUnavailable extends Error {
  constructor(state, path) {
    super(`TNR authentication is ${state === AUTH.SIGNED_OUT ? "signed out" : "not confirmed"}; ${path} is a protected procedure and was not sent`);
    this.name = "AuthUnavailable";
    this.state = state;
    this.path = path;
    this.sent = false;
  }
}

/**
 * A protected procedure came back UNAUTHORIZED on a read that is NOT the runner's own call site -
 * today that means inside reconciliation, which reads through the CachedReader and has no auth
 * dependency of its own. Reconciliation's honest answer to an unreadable record is ORPHANED, and
 * for a SENT item that turns a five-minute sign-in into an adopt-or-skip decision about a write
 * that is probably fine (independent review round 2, surviving path B). Throwing this instead
 * surfaces the condition to the Runner, which invalidates the shared auth state, pauses, and
 * leaves every SENT item exactly as it was for a later reconciliation.
 *
 * It carries the decoded error element so the Runner can classify and report it without the
 * reconciler needing to know anything about AuthState.
 */
export class AuthRefused extends Error {
  constructor(path, error) {
    super(`the game refused ${path} as unauthenticated`);
    this.name = "AuthRefused";
    this.path = path;
    this.error = error;
  }
}

export class AuthState {
  /**
   * @param {object} d
   * @param {{call: (path: string, input: object) => Promise<object>}} d.client  the tRPC client
   * @param {() => ({loaded: boolean, signedIn: boolean|null}|null)} [d.runtime]  page auth runtime
   *   reader. Returns null when the page publishes no auth runtime at all. Injected so no test
   *   needs Clerk, and so this file never reaches for window itself.
   * @param {() => number} [d.clock]
   * @param {string} [d.state]  initial state; tests that are not about auth start READY.
   */
  constructor({ client = null, runtime = null, clock = () => Date.now(), state = AUTH.UNKNOWN } = {}) {
    this.client = client;
    this.runtime = runtime;
    this.clock = clock;
    this.state = state;
    this.at = null;         // when the state was last established
    this.detail = null;     // one short human sentence for the UI; never a token, never a body
    this.listeners = new Set();
  }

  get ready() { return this.state === AUTH.READY; }
  /** Is it already known that protected work cannot run? (UNKNOWN is blocked but not *known*.) */
  get signedOut() { return this.state === AUTH.SIGNED_OUT; }

  onChange(fn) { this.listeners.add(fn); return () => this.listeners.delete(fn); }
  _set(state, detail = null) {
    const changed = this.state !== state || this.detail !== detail;
    this.state = state;
    this.detail = detail;
    if (state === AUTH.READY || state === AUTH.SIGNED_OUT) this.at = this.clock();
    if (changed) for (const fn of this.listeners) { try { fn(this); } catch { /* a listener must never break the gate */ } }
    return state;
  }

  /** What the page's own auth runtime says right now. {present, loaded, signedIn}. */
  runtimeStatus() {
    if (typeof this.runtime !== "function") return { present: false, loaded: false, signedIn: null };
    let r = null;
    try { r = this.runtime(); } catch { r = null; }
    if (!r) return { present: false, loaded: false, signedIn: null };
    return { present: true, loaded: !!r.loaded, signedIn: r.signedIn === null || r.signedIn === undefined ? null : !!r.signedIn };
  }

  /**
   * Wait for the page's auth runtime to finish loading, bounded. Resolves with the last status
   * seen; a runtime that never appears resolves {present:false} rather than hanging, and the
   * probe then decides. No request is issued here.
   */
  async waitForRuntime({ timeoutMs = 15_000, pollMs = 100, sleep } = {}) {
    const wait = sleep ?? ((ms) => new Promise((r) => setTimeout(r, ms)));
    const deadline = this.clock() + timeoutMs;
    let status = this.runtimeStatus();
    while (!(status.present && status.loaded) && this.clock() < deadline) {
      await wait(pollMs);
      status = this.runtimeStatus();
    }
    return status;
  }

  /**
   * Establish the state against the server. One request, body discarded, nothing cached.
   * Returns the new state.
   */
  async probe() {
    if (!this.client) return this._set(AUTH.UNKNOWN, "no transport is wired for the auth check");
    // A runtime that has loaded and reports nobody signed in is already an answer; asking the
    // server would only confirm it at the cost of a request.
    const status = this.runtimeStatus();
    if (status.present && status.loaded && status.signedIn === false) {
      return this._set(AUTH.SIGNED_OUT, "the page's Clerk runtime reports no signed-in session");
    }
    this._set(AUTH.PROBING);
    let decoded;
    try {
      decoded = await this.client.call(PROBE_PATH, { userId: PROBE_ID });
    } catch (e) {
      return this._set(AUTH.UNKNOWN, "the auth check could not reach the game: " + String((e && e.message) || e).slice(0, 160));
    }
    if (decoded && decoded.ok) return this._set(AUTH.READY, "a protected procedure answered for this session");
    const cls = classifyError(decoded && decoded.error);
    if (cls === "SESSION") return this._set(AUTH.SIGNED_OUT, "the game refused a protected procedure: " + String(decoded.error.code));
    if (cls === "RATE_LIMITED") return this._set(AUTH.UNKNOWN, "the auth check was rate limited; sign-in state is unconfirmed");
    // Any other error still proves the protected middleware let this session through.
    return this._set(AUTH.READY, "a protected procedure answered for this session");
  }

  /** waitForRuntime + probe, in the order the boot sequence needs them. */
  async establish(opts = {}) {
    await this.waitForRuntime(opts);
    return this.probe();
  }

  /**
   * Record a SERVER-PROVEN refusal: a protected procedure came back UNAUTHORIZED (or the route
   * handler's "Please complete registration"), so this session cannot do protected work whatever
   * the page runtime or the last probe believed.
   *
   * This exists because a probe is a snapshot and a session can die a minute later (independent
   * review FPA-2). Without it the standing banner kept saying "TNR session active" while the run
   * screen said authentication was unavailable, and Resume would happily send the next protected
   * request against a session the server had already refused. The server's answer is the most
   * authoritative signal there is, so it wins over the probe, and the gate then blocks every
   * protected path until probe() succeeds again.
   *
   * @returns {string} the new state
   */
  refuse(detail = null) {
    return this._set(AUTH.SIGNED_OUT, detail ? String(detail).slice(0, 200) : "the game refused a protected procedure for this session");
  }

  /**
   * THE GATE. Throws AuthUnavailable when `path` is protected and the session is not established.
   * Callers must call it BEFORE journaling a send, so a refusal can never leave an item SENT: a
   * blocked mutation is a mutation that was never written down as sent, which is the whole point
   * (brief section E). A public path is never gated - a signed-out capture-only job over public
   * procedures still runs, exactly as the procedure guards allow.
   */
  assert(path) {
    if (!isProtected(path)) return;
    if (this.state !== AUTH.READY) throw new AuthUnavailable(this.state, path);
  }

  /** Non-throwing form, for the UI deciding whether to offer a button. */
  allows(path) { return !isProtected(path) || this.state === AUTH.READY; }

  /** For the Settings screen. Deliberately has no room for a secret to appear in. */
  describe() { return { state: this.state, detail: this.detail, at: this.at }; }
}
