// The credential seam (brief section 6). Every request the app issues to the GAME goes
// through a Session. There is exactly one implementation today, cookie-based and
// same-origin. Two later implementations are anticipated and must be additions, not rewrites:
//   - NativeCookieSession: a shell lifts the Clerk cookie into native networking
//   - BearerSession: if TNR enables mcp.enabled on the remaining content writes
//
// The game session NEVER carries an Authorization header (spec section 7). The GitHub PAT
// lives in a different object (github.mjs) and never touches this path.

export class Session {
  /** @returns {Promise<Response>} */
  async fetch(_url, _init) { throw new Error("Session.fetch not implemented"); }
  /** Human-readable, for the Settings screen. Must never include a secret. */
  describe() { return { kind: "abstract" }; }
}

export class CookieSession extends Session {
  /**
   * @param {object} opts
   * @param {(url: string, init: object) => Promise<Response>} opts.fetchImpl  the page's fetch
   * @param {string} [opts.origin]  "" for same-origin relative URLs (the userscript case)
   */
  constructor({ fetchImpl, origin = "" } = {}) {
    super();
    if (typeof fetchImpl !== "function") throw new Error("CookieSession needs fetchImpl");
    this.fetchImpl = fetchImpl;
    this.origin = origin;
  }

  async fetch(url, init = {}) {
    const headers = new Headers(init.headers ?? {});
    if (headers.has("authorization")) {
      // Structural guard: nothing in the game path may carry a bearer. If a caller tries,
      // that is a bug in the caller, and it fails here rather than leaking a token.
      throw new Error("CookieSession refuses an Authorization header on a game request");
    }
    return this.fetchImpl(this.origin + url, { ...init, headers, credentials: "same-origin" });
  }

  describe() { return { kind: "cookie", origin: this.origin || "(same-origin)" }; }
}
