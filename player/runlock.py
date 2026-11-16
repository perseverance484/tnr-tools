"""The run lock: one game writer on the account at a time (RUL-2026-11-07-133; docs/workflows/FORGE_MCP_RUNNER.md).

The lock is state/run_lock.json on main. It is written only by forge/tools/run_lock.mjs, one commit a write, and
this module only runs that tool. The brain holds the lock for a play session (director 2026-11-12,
RUL-2026-11-12-154: "Give it to the brain then"):

- before a call is sent, the brain claims the lock as `player`, and no call is sent without it;
- it renews the claim every RENEW_EVERY seconds while it plays (in a fight only when the lease is close to its
  end: a renewal is a push, and takes a moment);
- it stops sending STOP_MARGIN seconds before the last expiry the tool confirmed, and at once when a renewal
  finds the lock taken (the workflow's rule for every runner). That moment is the claim's cutoff (until). It
  holds for when a call is made, not for when it is planned: a call that is due at or after it is not put in
  a batch (Brain._paced), and every batch carries the cutoff it was made under to `brain next`, which prints
  nothing of a batch whose last call would fall at or after it (lapsed), whether it waited, was kept through
  a crash, or is given again from its receipt (review of 988c56cc, H1);
- it gives the lock back when the session is over (asleep at home), when the player is asleep outside hunt mode,
  and when the director pauses it outside a fight.

The lock is the account's, so only the brain of the account's own live folder holds it. A brain on any other
folder is a rehearsal (a test, a replay, a review's script): no relay of its reaches the game, it claims
nothing, and its status says so. A play session is run on the account's own folder.

What the brain knows of its claim is in the world model (records.run_lock): the token, the expiry, when to renew,
and why it is waiting when it is. The token is ownership; it is never written to the status file.
"""
import datetime as dt
import json
import os
import re
import subprocess

from . import config as C

TOOL = os.path.join(C.ROOT, "forge", "tools", "run_lock.mjs")
HOLDER = "player"
JOB = "play session"
TTL_MINUTES = 60           # the tool's own default: a brain that dies gives the lock up within the hour
RENEW_EVERY = 900.0        # s between renewals (the workflow: a third of the lease, 15 minutes at most)
RENEW_NOW = 600.0          # s of lease left under which a fight no longer puts a renewal off
STOP_MARGIN = 60.0         # s before the last confirmed expiry at which no more calls are sent
RETRY = 60.0               # s between two tries when the tool could not be run, or a renewal failed
ASK_AGAIN = (10.0, 60.0)   # s: the least and the most between two claims while another runner has the lock


def own_folder(live):
    """Whether this is the account's own live folder: the one a play session runs on."""
    return os.path.realpath(live) == os.path.realpath(os.path.join(C.ACCOUNT_DIR, "live"))


def _epoch(text):
    try:
        return dt.datetime.fromisoformat(str(text).replace("Z", "+00:00")).timestamp()
    except (TypeError, ValueError):
        return None


class Tool:
    """forge/tools/run_lock.mjs, run in a process of its own. Every answer is the tool's one JSON line; what
    could not be run, or said nothing that can be read, comes back as {"type": "error"}."""

    def __init__(self, env=None, timeout=180.0):
        self.env, self.timeout = env, timeout

    def _run(self, *args):
        try:
            done = subprocess.run(["node", TOOL, *args], cwd=C.ROOT, capture_output=True, text=True,
                                  timeout=self.timeout, env={**os.environ, **(self.env or {})})
            said = json.loads(done.stdout.strip().splitlines()[-1])
            return said if isinstance(said, dict) and said.get("type") else {"type": "error", "text": done.stdout[:300]}
        except (OSError, ValueError, IndexError, subprocess.SubprocessError) as err:
            return {"type": "error", "text": f"the run lock tool could not be run: {err!r}"[:300]}

    def claim(self, instance):
        return self._run("claim", "--holder", HOLDER, "--job", JOB, "--ttl", str(TTL_MINUTES), "--instance", instance)

    def heartbeat(self, token):
        return self._run("heartbeat", "--token", token, "--ttl", str(TTL_MINUTES))

    def release(self, token):
        return self._run("release", "--token", token)


class RunLock:
    def __init__(self, world, tool=None, rehearsal=None):
        self.world, self.tool = world, tool or Tool()
        self.rehearsal = not own_folder(world.live) if rehearsal is None else rehearsal

    @property
    def state(self):
        return self.world["records"].setdefault("run_lock", {})

    def until(self):
        """The cutoff: the moment from which no call is made under this claim. None for a rehearsal, which has
        none; 0 with no claim."""
        if self.rehearsal:
            return None
        s = self.state
        return s.get("expires", 0) - STOP_MARGIN if s.get("token") else 0.0

    def held(self):
        """Whether a call may be sent now: a rehearsal, or a claim of this brain's with time left on it."""
        until = self.until()
        return until is None or self.world.now < until

    def too_short(self, calls):
        """Said once for each lease: calls were due after its cutoff, and were not put in the batch."""
        s = self.state if calls else {}
        if calls and s.get("short") != s.get("expires"):
            s["short"] = s.get("expires")
            self.world.event("stall", f"the run lock's lease ends too soon for {calls} call(s) that were due, and "
                                      f"it has not been renewed: they are not sent", about="run_lock")

    def hold(self, in_battle=False):
        """Have the lock for the calls that are about to be planned. None when they may be sent; else (the
        seconds until it is worth asking again, why)."""
        if self.rehearsal:
            return None
        s, now = self.state, self.world.now
        late = s.get("expires", 0) - now < RENEW_NOW
        if self.held() and now >= s.get("renew_at", 0) and (late or not in_battle):
            self._renew()
        if self.held():
            return None
        if now >= s.get("ask_at", 0):
            self._claim()
        return None if self.held() else (max(1.0, s.get("ask_at", 0) - now), s.get("why") or "the run lock is not held")

    def _claim(self):
        s, now = self.state, self.world.now
        said = self.tool.claim(os.path.realpath(self.world.live))
        expires = _epoch(said.get("expiresAt"))
        if said["type"] == "claimed" and said.get("token") and expires:
            s.clear()
            s.update(token=said["token"], expires=expires, renew_at=now + RENEW_EVERY)
            self.world.event("activity_done", f"session: the run lock is claimed as {HOLDER}", activity="session")
            return
        s.pop("token", None)
        wait = (said.get("waitMs") or 0) / 1000.0 if said["type"] == "refused" else RETRY
        why = f"waiting for the run lock: {said.get('text') or said['type']}"[:300]
        told = re.sub(r"\d+", "N", why)                            # (the minutes and seconds in it count down)
        if told != s.get("told"):                                  # said once for each reason, not at every ask
            self.world.event("stall" if said["type"] == "refused" else "error", why + ". No call is sent.",
                             about="run_lock")
        s.update(why=why, told=told, ask_at=now + min(max(wait, ASK_AGAIN[0]), ASK_AGAIN[1]))

    def _renew(self):
        s, now = self.state, self.world.now
        said = self.tool.heartbeat(s["token"])
        expires = _epoch(said.get("expiresAt"))
        if said["type"] == "heartbeat" and expires:
            s.update(expires=expires, renew_at=now + RENEW_EVERY)
        elif said["type"] == "refused":                            # the lock is somebody else's now: stop at once
            self.world.event("stall", f"the run lock is lost: {said.get('text')}. No call is sent."[:300],
                             about="run_lock")
            s.clear()
        else:                                                      # the push failed: the lease runs out by itself
            s["renew_at"] = now + RETRY
            self.world.event("error", f"the run lock could not be renewed: {said.get('text')}"[:300], about="run_lock")

    def release(self):
        """Give the lock back. Whatever the tool says, this brain no longer counts on it."""
        token = None if self.rehearsal else self.state.get("token")
        if not token:
            return
        said = self.tool.release(token)
        self.state.clear()
        if said["type"] == "released":
            self.world.event("activity_done", "session: the run lock is released", activity="session")
        else:
            self.world.event("error", f"the run lock could not be released: {said.get('text')}; its lease runs out "
                                      f"by itself"[:300], about="run_lock")

    def status(self):
        """For the status file: never the token."""
        if self.rehearsal:
            return {"state": "rehearsal: not the account's live folder, no lock is claimed"}
        s = self.state
        if self.held():
            at = dt.datetime.fromtimestamp(s["expires"], dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            return {"state": "held", "holder": HOLDER, "expires": at}
        return {"state": "not held", "why": s.get("why")}


def within(steps, start, until):
    """(the steps of a batch that may go, the number of its calls that may not), for a relay that gets the batch
    at `start`: the first call that would be made at or after the cutoff is left out with everything behind
    it, and no wait is left at the end of what stays. Each wait inside the batch counts: the relay spends it."""
    at = start
    for i, step in enumerate(steps):
        at += step.get("wait", 0)
        if "call" in step and until is not None and at >= until:
            kept = list(steps[:i])
            while kept and "wait" in kept[-1]:
                kept.pop()
            return kept, sum("call" in s for s in steps[i:])
    return steps, 0


def lapsed(batch, now):
    """Whether a batch may no longer be printed: one of its calls would be made at or after the cutoff it was
    made under. A batch with no cutoff (a rehearsal's) or no call never lapses; one whose cutoff cannot be
    read always has."""
    until = batch.get("until")
    if until is not None and not isinstance(until, (int, float)):
        return True
    return within(batch["steps"], now, until)[1] > 0


def given_up(state):
    """`brain next`, of the batch that waits in its file (client.json): it was not printed, and now never will
    be. Its number is not used again, and the next request tells the brain so (unprinted): its calls count
    from then, as for any batch that was not printed. -> None."""
    pending = state["pending"]
    state["seq"] = max(state.get("seq", 0), pending["seq"])
    state["unprinted"] = state["unprinted"] + [pending["id"]]
    state["pending"] = None
