// The run lock: one game writer per account at a time (RUL-2026-11-07-133).
//
// Every runner on the director's account (the browser tab, a Claude session over the game
// connection, Duet) shares two limits it cannot see the others spend: the game connection's 30
// calls per minute per user, and the game's per-procedure 60 per minute, whose mutation overruns
// fine the account 1% of money and bank. The lock is a file on main, state/run_lock.json. A claim
// is a write that only succeeds against the version it read (a fast-forward push from the CLI, a
// sha-checked contents-API PUT from the browser), so two claimers cannot both win.
//
// Four rules make "one runner at a time" hold, not just "one claim at a time":
//   1. Ownership is a random token minted per claim; holder ("claude", "duet", "browser") is a
//      label only. Heartbeat and release need the token, so two sessions with one label cannot
//      share or steal a claim.
//   2. Every runner claims, the browser included, for the whole run.
//   3. A runner stops sending STOP_MARGIN_MS before its last confirmed expiry (the Lease below),
//      and renews well before it, so a lease that lapses or is lost stops the sends.
//   4. Releasing or lapsing does not clear the server's rolling minute, so the next claim waits a
//      quiet period (QUIET_MS) after the previous holder's last possible send.
//
// This module is pure (no git, no fetch, no clock of its own). The CLI is forge/tools/run_lock.mjs.

export const LOCK_PATH = "state/run_lock.json";
export const DEFAULT_TTL_MINUTES = 60;
export const MIN_TTL_MINUTES = 5;
/** The server windows are 60 s; 5 s over covers clock skew between runners' machines. */
export const QUIET_MS = 65_000;
/** A holder stops sending this long before its confirmed expiry: skew plus one in-flight call. */
export const STOP_MARGIN_MS = 60_000;

const ms = (iso) => Date.parse(iso);

/** Parse the lock file. Missing or empty text is a free lock; anything unreadable is refused. */
export function parseLock(text) {
  if (text == null || String(text).trim() === "") return { holder: null, token: null };
  let j;
  try { j = JSON.parse(text); } catch { throw new Error(`${LOCK_PATH} is not JSON`); }
  if (!j || typeof j !== "object" || Array.isArray(j)) throw new Error(`${LOCK_PATH} is not an object`);
  if (j.token != null) {
    if (typeof j.token !== "string" || j.token.length < 16) throw new Error(`${LOCK_PATH}: token must be a string of 16+ characters`);
    if (Number.isNaN(ms(j.expiresAt))) throw new Error(`${LOCK_PATH}: a held lock needs an ISO expiresAt`);
  }
  return { holder: null, token: null, ...j };
}

/** {held, holder, job, expired, minutesLeft} at time `now` (ms). An expired lock is no longer held. */
export function lockState(lock, now) {
  if (!lock || lock.token == null) return { held: false, holder: null, job: null, expired: false, minutesLeft: 0 };
  const left = (ms(lock.expiresAt) - now) / 60000;
  return { held: left > 0, holder: lock.holder ?? "?", job: lock.job ?? null, expired: left <= 0, minutesLeft: Math.max(0, Math.ceil(left)) };
}

/** The earliest a NEW claim may start sending: QUIET_MS after the last moment the previous holder could have sent. */
export function quietUntil(lock) {
  if (!lock) return 0;
  if (lock.token != null) return ms(lock.expiresAt) + QUIET_MS; // lapsed: it may have sent until expiry
  return lock.releasedAt ? ms(lock.releasedAt) + QUIET_MS : 0;
}

/**
 * May a new claim be made now? {ok: true} or {ok: false, held: bool, waitMs, reason}.
 * Held by anyone (even the same label) refuses: re-claiming your own lease is a heartbeat, which
 * needs the token.
 */
export function claimDecision(lock, now, instance = null) {
  const s = lockState(lock, now);
  if (s.held) return { ok: false, held: true, waitMs: ms(lock.expiresAt) + QUIET_MS - now, reason: `the run lock is held by ${s.holder}${s.job ? ` (${s.job})` : ""} for up to ${s.minutesLeft} more minute(s)` };
  // The same runner instance re-claiming needs no quiet period: its own pacer and budget already
  // carry the calls it made under the previous claim.
  const mine = instance != null && (lock?.releasedInstance === instance || (lock?.token != null && lock?.instance === instance));
  const q = mine ? 0 : quietUntil(lock);
  if (now < q) return { ok: false, held: false, waitMs: q - now, reason: `the previous runner (${lock.holder ?? lock.releasedBy ?? "?"}) finished less than a minute ago; its calls still count against the game's rolling minute, so wait ${Math.ceil((q - now) / 1000)} s` };
  return { ok: true };
}

/** Why the holder of `token` may NOT send now, or null when it may. */
export function blockReason(lock, token, now) {
  if (!token) return "no run-lock claim (node forge/tools/run_lock.mjs claim --holder NAME --job TEXT prints the token)";
  const s = lockState(lock, now);
  if (lock?.token !== token) return s.held ? `the run lock is held by another claim (${s.holder}${s.job ? `, ${s.job}` : ""})` : "this claim no longer holds the run lock";
  if (!s.held) return "this claim's run lock has expired";
  if (ms(lock.expiresAt) - now <= STOP_MARGIN_MS) return "this claim's run lock is about to expire; renew it first";
  return null;
}

export function newToken() {
  const c = globalThis.crypto;
  if (c?.randomUUID) return c.randomUUID().replace(/-/g, "");
  if (c?.getRandomValues) return Array.from(c.getRandomValues(new Uint8Array(16)), (b) => b.toString(16).padStart(2, "0")).join("");
  throw new Error("no secure random source for a run-lock token");
}

export function checkTtl(ttlMinutes) {
  if (!Number.isFinite(ttlMinutes) || ttlMinutes < MIN_TTL_MINUTES || ttlMinutes > 240) throw new Error(`run-lock TTL must be ${MIN_TTL_MINUTES}-240 minutes`);
  return ttlMinutes;
}

/** How often a holder renews: a third of the TTL, so two renewals can fail before the stop margin. */
export const renewEveryMs = (ttlMinutes) => Math.min(15 * 60000, (checkTtl(ttlMinutes) * 60000) / 3);

/** The body a new claim writes. */
export function claimBody({ holder, job, token, ttlMinutes = DEFAULT_TTL_MINUTES, now, instance = null }) {
  if (!holder || typeof holder !== "string") throw new Error("a claim needs a holder label");
  if (!token) throw new Error("a claim needs a token");
  checkTtl(ttlMinutes);
  const t = new Date(now).toISOString();
  return { holder, job: job ?? null, token, instance, ttlMinutes, claimedAt: t, heartbeatAt: t, expiresAt: new Date(now + ttlMinutes * 60000).toISOString(),
    note: "One game writer per account at a time (RUL-2026-11-07-133). Written only by forge/tools/run_lock.mjs or Forge; do not hand-edit." };
}

/** The body a heartbeat writes: same claim, later expiry. */
export function renewBody(lock, { ttlMinutes = DEFAULT_TTL_MINUTES, now }) {
  checkTtl(ttlMinutes);
  return { ...lock, ttlMinutes, heartbeatAt: new Date(now).toISOString(), expiresAt: new Date(now + ttlMinutes * 60000).toISOString() };
}

/** The body a release writes. releasedAt starts the quiet period. */
export function releaseBody(lock, { now }) {
  return { holder: null, token: null, job: null, releasedBy: lock?.holder ?? null, releasedInstance: lock?.instance ?? null, releasedJob: lock?.job ?? null, releasedAt: new Date(now).toISOString(),
    note: "Free. Claim with node forge/tools/run_lock.mjs claim --holder NAME --job TEXT (RUL-2026-11-07-133)." };
}

/**
 * The sending side of a claim, held in memory by the runner that owns it. While a run is active,
 * every game call checks ok() first (see guardClient): sends stop STOP_MARGIN_MS before the last
 * CONFIRMED expiry, and at once when the claim is lost. Renewals only ever move the expiry when
 * the renewal itself was confirmed.
 */
export class Lease {
  constructor(clock = () => Date.now()) { this.clock = clock; this.end(); }
  /**
   * renewer (optional): async () => void, the holder's renewal. The runner calls it between items
   * once renewEveryMs has passed (due()), so a run renews on its own clock even where wall timers
   * are throttled (a background tab) or absent (a fake clock); a host timer may call it too.
   */
  begin({ token, holder, expiresAt, renewer = null, renewEveryMs = null }) {
    this.token = token; this.holder = holder; this.expiresAt = ms(expiresAt); this.lost = null; this.active = true;
    this.renewer = renewer; this.renewEvery = renewEveryMs; this.lastRenew = this.clock();
  }
  due() { return !!(this.active && !this.lost && this.renewer && this.renewEvery && this.clock() - this.lastRenew >= this.renewEvery); }
  async renewNow() { if (!this.active || !this.renewer) return; this.lastRenew = this.clock(); await this.renewer(); }
  renewed(expiresAt) { if (this.active && !this.lost) this.expiresAt = Math.max(this.expiresAt, ms(expiresAt)); }
  lose(reason) { if (this.active) this.lost = reason || "the run lock was lost"; }
  end() { this.active = false; this.token = null; this.holder = null; this.expiresAt = 0; this.lost = null; this.renewer = null; this.renewEvery = null; this.lastRenew = 0; }
  /** null when a send may go out now; otherwise why not. Inactive means no run is in progress (idle reads are not leased). */
  check() {
    if (!this.active) return null;
    if (this.lost) return this.lost;
    if (this.clock() >= this.expiresAt - STOP_MARGIN_MS) return "the run-lock lease ran out before it could be renewed";
    return null;
  }
}
