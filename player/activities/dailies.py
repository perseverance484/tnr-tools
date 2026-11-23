"""Dailies: once a UTC day, the activity streak and the bank's interest (tnr-autopilot DESIGN.md section 5).

The day starts with a read of both (no select: their shapes are not on record yet, so the whole answer is kept in
live/captures/ for the model and for the first review). Then:
  streak    each streak the read shows as claimable today is claimed: activityStreak.claimStreakDay with
            payCatchUp false and reset false, always. A catch-up can cost premium currency, and a reset gives up a
            streak: neither is the player's to choose. When the read's shape is not one this file can read, nothing
            is claimed and that is a finding for the model (about "exception").
  interest  claimed when the read shows any interest pending.
Never activityStreak.purchaseEventPass (a payment; it is not on the allowlist either).
"""
import datetime as dt
import json
import os

from .. import calls as K
from ..registry import REGISTRY, Activity, plan

CLAIMABLE = ("canClaim", "claimable", "canClaimToday", "isClaimable", "available")
CLAIMED = ("claimedToday", "isClaimedToday", "claimed")


def today(world):
    return dt.datetime.fromtimestamp(world.now, dt.timezone.utc).strftime("%Y-%m-%d")


def claimable_streaks(data):
    """The configIds a streak read shows as claimable today: every object that carries a configId (or a config's
    id) and a true claimable flag, and no true claimed flag. None when no object in it carries a configId: a
    shape this file cannot read."""
    found, seen = [], False

    def walk(x):
        nonlocal seen
        if isinstance(x, dict):
            cid = x.get("configId")
            if not cid and isinstance(x.get("config"), dict):
                cid = x["config"].get("id")
            if isinstance(cid, str) and cid:
                seen = True
                if any(x.get(k) is True for k in CLAIMABLE) and not any(x.get(k) is True for k in CLAIMED):
                    found.append(cid)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(data)
    return sorted(set(found)) if seen else None


def pending_interest(data):
    """The interest the read shows pending: a number, or the first of amount / interest / pending in it."""
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return float(data)
    if isinstance(data, dict):
        for k in ("amount", "interest", "pending", "pendingInterest", "data"):
            v = pending_interest(data.get(k))
            if v is not None:
                return v
    return None


@REGISTRY.activity
class Dailies(Activity):
    name = "dailies"
    priority = "upkeep"
    goal = "daily_caps"
    reads = ("activityStreak.getUserStreaks", "bank.getPendingInterest", "activityStreak.claimStreakDay",
             "bank.claimInterest")

    def _day(self, world):
        own = world.own(self.name)
        if own.get("day") != today(world):
            own.clear()
            own["day"] = today(world)
        return own

    def available(self, world):
        own = self._day(world)
        return (world.status() == "AWAKE" and not world.in_battle() and not own.get("done")
                and own.get("asked_at", 0) + 300 <= world.now)

    def value(self, world):
        return 3.0

    def plan(self, world):
        own = self._day(world)
        own["asked_at"] = world.now
        if "streaks" not in own:
            return plan([K.call("activityStreak.getUserStreaks", {}, []), K.call("bank.getPendingInterest", {}, [])],
                        "world", "reading the streak and the interest")
        steps = [K.call("activityStreak.claimStreakDay", {"configId": c, "payCatchUp": False, "reset": False},
                        ["success", "message"]) for c in own["streaks"]]
        if own.get("interest"):
            steps.append(K.call("bank.claimInterest", {}, ["success", "message"]))
        own["done"] = True
        if not steps:
            return plan([K.user()], "world", "nothing to claim today")
        return plan(steps + [K.user()], "world", f"claiming {len(steps)}")

    def on_result(self, world, results):
        own = self._day(world)
        for r in results:
            if r.endpoint not in self.reads or r.error:
                continue
            if r.endpoint == "activityStreak.getUserStreaks":
                own["asked_at"] = 0                    # the read is back: the claims may go in the next batch
                self._keep(world, r)
                ids = claimable_streaks(r.data)
                own["streaks"] = ids or []
                if ids is None:
                    world.event("finding", "dailies: the streak read has a shape the player cannot read; it is kept "
                                           "in live/captures/ for the model", about="exception")
            elif r.endpoint == "bank.getPendingInterest":
                self._keep(world, r)
                own["interest"] = (pending_interest(r.data) or 0) > 0
            else:
                ok = isinstance(r.data, dict) and r.data.get("success")
                what = "interest" if r.endpoint == "bank.claimInterest" else f"streak {r.input.get('configId')}"
                world.event("activity_done" if ok else "finding",
                            f"dailies: {what} {'claimed' if ok else 'refused: ' + str((r.data or {}).get('message'))}"[:300],
                            **({"activity": self.name} if ok else {"about": "dailies"}))

    @staticmethod
    def _keep(world, r):
        """The whole answer, for the model and the first review (its shape is not on record yet)."""
        folder = os.path.join(world.live, "captures")
        try:
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, f"{r.endpoint}.json"), "w", encoding="utf8") as f:
                json.dump({"at": world.now, "data": r.data}, f, default=str)
        except OSError:
            pass
