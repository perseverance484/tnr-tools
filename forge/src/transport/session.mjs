// The credential seam (brief section 6). Every request the app issues to the GAME goes
// through a Session. There is exactly one implementation today, cookie-based and
// same-origin. Two later implementations are anticipated and must be additions, not rewrites:
//   - NativeCookieSession: a shell lifts the Clerk cookie into native networking
//   - BearerSession: if TNR enables mcp.enabled on the remaining content writes
//
// The game session NEVER carries an Authorization header (spec section 7). The GitHub PAT
// lives in a different object (github.mjs) and never touches this path.

/** Thrown before anything leaves the device. The transport reports it as not-sent, never ambiguous. */
export class SessionRefused extends Error {
  constructor(message) { super(message); this.name = "SessionRefused"; this.sent = false; }
}

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
    // receiver-free: window.fetch throws "Illegal invocation" when called as a method of
    // another object, so never store it as a property that gets called with `this`
    this.fetchImpl = (u, i) => fetchImpl(u, i);
    this.origin = origin;
  }

  static ALLOWED_PATHS = /^\/api\/(trpc\/|uploadthing(\?|$))/;
  static ALLOWED_HEADERS = new Set(["content-type", "x-uploadthing-version", "accept"]);

  async fetch(url, init = {}) {
    if (typeof url !== "string" || !CookieSession.ALLOWED_PATHS.test(url)) {
      throw new SessionRefused("CookieSession only issues same-origin /api/trpc and /api/uploadthing requests, got " + String(url).slice(0, 80));
    }
    // allowlist by construction: the only headers that can leave are the ones a game request needs
    const headers = new Headers();
    new Headers(init.headers ?? {}).forEach((v, k) => {
      if (!CookieSession.ALLOWED_HEADERS.has(k)) throw new SessionRefused(`CookieSession refuses header ${k} on a game request`);
      headers.set(k, v);
    });
    return this.fetchImpl(this.origin + url, { ...init, headers, credentials: "same-origin" });
  }

  describe() { return { kind: "cookie", origin: this.origin || "(same-origin)" }; }
}
