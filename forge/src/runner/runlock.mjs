// The run lock: one game writer per account at a time (RUL-2026-11-07-133).
//
// Every runner on the director's account (the browser tab, a Claude session over the game
// connection, Duet) shares two limits it cannot see the others spend: the game connection's 30
// calls per minute per user, and the game's per-procedure 60 per minute, whose mutation overruns
// fine the account 1% of money and bank. The lock is a file on main, state/run_lock.json; a claim
// is a commit pushed to main, so git's fast-forward check is the compare-and-swap (two claimers,
// one push wins). This module is the pure part: reading a lock and deciding whether a holder may
// run. The git side is forge/tools/run_lock.mjs; the browser reads the file through the GitHub
// contents API and refuses Start while someone else holds it.

export const LOCK_PATH = "state/run_lock.json";
export const DEFAULT_TTL_MINUTES = 60;

/** Parse the lock file. Missing or empty text is a free lock; anything unreadable is refused. */
export function parseLock(text) {
  if (text == null || String(text).trim() === "") return { holder: null };
  let j;
  try { j = JSON.parse(text); } catch { throw new Error(`${LOCK_PATH} is not JSON`); }
  if (!j || typeof j !== "object" || Array.isArray(j)) throw new Error(`${LOCK_PATH} is not an object`);
  if (j.holder != null && (typeof j.holder !== "string" || !j.holder.trim())) throw new Error(`${LOCK_PATH}: holder must be a non-empty string or null`);
  if (j.holder != null && Number.isNaN(Date.parse(j.expiresAt))) throw new Error(`${LOCK_PATH}: a held lock needs an ISO expiresAt`);
  return j;
}

/** {held, holder, expired, minutesLeft} at time `now` (ms). An expired lock is free to take. */
export function lockState(lock, now) {
  if (!lock || lock.holder == null) return { held: false, holder: null, expired: false, minutesLeft: 0 };
  const left = (Date.parse(lock.expiresAt) - now) / 60000;
  return { held: left > 0, holder: lock.holder, expired: left <= 0, minutesLeft: Math.max(0, Math.ceil(left)) };
}

/** Why `holder` may NOT run now, or null when it may. holder null means "a runner that never claims" (the browser): it may run only while nobody holds the lock. */
export function blockReason(lock, holder, now) {
  const s = lockState(lock, now);
  if (!s.held) return holder ? `${holder} has not claimed the run lock (node forge/tools/run_lock.mjs claim --holder ${holder} --job ...)` : null;
  if (holder && s.holder === holder) return null;
  return `the run lock is held by ${s.holder}${lock.job ? ` (${lock.job})` : ""} for up to ${s.minutesLeft} more minute(s); wait for it to finish, or for it to release the lock`;
}

/** The lock body a claim or heartbeat writes. */
export function claimBody({ holder, job, ttlMinutes = DEFAULT_TTL_MINUTES, now, prev = null }) {
  if (!holder || typeof holder !== "string") throw new Error("a claim needs a holder");
  const t = new Date(now).toISOString();
  return {
    holder,
    job: job ?? prev?.job ?? null,
    claimedAt: prev && prev.holder === holder && prev.claimedAt ? prev.claimedAt : t,
    heartbeatAt: t,
    expiresAt: new Date(now + ttlMinutes * 60000).toISOString(),
    note: "One game writer per account at a time (RUL-2026-11-07-133). Claim, heartbeat and release with node forge/tools/run_lock.mjs; do not hand-edit while held.",
  };
}

/** The lock body a release writes. */
export function releaseBody({ holder, now }) {
  return { holder: null, job: null, releasedBy: holder, releasedAt: new Date(now).toISOString(),
    note: "Free. Claim with node forge/tools/run_lock.mjs claim --holder NAME --job TEXT (RUL-2026-11-07-133)." };
}
