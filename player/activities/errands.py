"""Errands: the day's D-rank errands in Hyorin, paced across the day (tnr-autopilot DESIGN.md section 5; director
2026-11-10: "20 missions and 50 errands is the cap"; 2026-11-13: "get all your missions and errands done").
Ported from the pilot's errand_tick, which ran 50 of 50 on 2026-11-15.

One whole errand per batch at home (sector 177): start it, walk to each goal and check it, claim it. Only the
errand the pilot knows is run (Hyorin's Broken Gate, goals (5,5) then (10,7)): a start that hands out any other
stops errands for an hour and is a finding, so the model can add it. A start the game refuses stops errands for
an hour, or for the day when it speaks of a limit. The day's count is the profile's own (userData.dailyErrands).

Pacing (the schedule solver's deficit rule): the value grows with how far the count is behind an even spread of
the cap from 00:00 to 20:00 UTC, so the hunt keeps the account until errands fall behind, then errands run in a
burst until they are nearly caught up (BURST_UNTIL). Stealth is cast in the errand's batch when it is down
(hunt thread 2026-11-15, after a loss during errands: "PvP loadouts + stealth during errands").
"""
import datetime as dt

from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan
from . import pvp_hunt

CAP = 50                   # director 2026-11-10 (the caps are his to confirm: DESIGN.md section 10)
NAME = "Hyorin's Broken Gate"
QUEST_ID = "A3he5vVNzt5mbQI8JPQj9"
STEPS = [(5, 5), (10, 7)]
DAY_END = 20.0             # h UTC by which the spread expects the cap done
BURST_FLOOR = 0.35         # a burst keeps the value at this share: 2 + 40 x 0.35 = 16, x 0.7 = 11.2 over the hunt's 10
BURST_UNTIL = 0.05         # a burst ends when the count is within this share of the cap of the spread
RETRY = 3600.0             # s errands rest after a refused or unknown start


def behind(done, cap, now, day_end=DAY_END):
    """How far the day's count is behind an even spread of the cap, as a share of the cap (0 when ahead)."""
    t = dt.datetime.fromtimestamp(now, dt.timezone.utc)
    hours = t.hour + t.minute / 60 + t.second / 3600
    expected = cap * min(1.0, hours / day_end)
    return max(0.0, expected - done) / cap


def paced_value(share, burst):
    """The arbiter's value for a daily job: low when on schedule, over the hunt's once well behind (with the
    daily-caps weight of 0.7, 2 + 40 x share passes the hunt's 10 at about a third of the cap behind), and kept
    up through a burst."""
    return 2.0 + 40.0 * max(share, BURST_FLOOR if burst else 0.0)


@REGISTRY.activity
class Errands(Activity):
    name = "errands"
    priority = "goals"
    goal = "daily_caps"
    reads = ("quests.startRandom",)

    def done_today(self, world):
        n = world.me.get("dailyErrands")
        return int(n) if isinstance(n, (int, float)) and not isinstance(n, bool) else None

    def available(self, world):
        own, n = world.own(self.name), self.done_today(world)
        return (world.status() == "AWAKE" and not world.in_battle() and world["control"]["mode"] == "hunt"
                and not world["control"]["end_session"] and n is not None and n < CAP
                and own.get("rest_until", 0) <= world.now)

    def value(self, world):
        own, share = world.own(self.name), behind(self.done_today(world) or 0, CAP, world.now)
        if own.get("burst") and share <= BURST_UNTIL:
            own["burst"] = False
        return paced_value(share, own.get("burst"))

    def plan(self, world):
        own, n, sector = world.own(self.name), self.done_today(world), world.me.get("sector")
        own["burst"] = True
        if sector != C.HOME_SECTOR:
            return plan(K.go(C.HOME_SECTOR), "world", f"{n}/{CAP} done today: going to the village ({C.HOME_SECTOR})")
        steps = []
        if not pvp_hunt.stealth_up(world) and world.now >= pvp_hunt.stealth(world).get("ready_at", 0):
            steps.append(K.stealth_on())
            pvp_hunt.stealth(world)["ready_at"] = world.now + C.STEALTH_COOLDOWN
        steps.append(K.call("quests.startRandom", {"type": "errand", "rank": "D", "userLevel": 100,
                                                   "userSector": C.HOME_SECTOR, "userVillageId": C.HOME_VILLAGE},
                            ["success", "message"]))
        cur = world.position()
        for p in STEPS:
            if p != cur:
                steps.append(K.move(cur, p, C.HOME_SECTOR))
            steps.append(K.call("quests.checkLocationQuest", {}, ["success", "message"]))
            cur = p
        steps += [K.call("quests.checkRewards", {"questId": QUEST_ID}, ["success", "message"]), K.user(),
                  K.sector(C.HOME_SECTOR)]
        own["sent"] = True
        return plan(steps, "world", f"errand {n + 1}/{CAP} ({NAME})")

    def on_result(self, world, results):
        own = world.own(self.name)
        for r in results:
            if r.endpoint != "quests.startRandom" or (r.input or {}).get("type") != "errand" or not own.pop("sent", None):
                continue
            data = r.data if isinstance(r.data, dict) else {}
            msg = str(data.get("message") or r.error or "")
            if r.error or not data.get("success"):
                own["rest_until"] = world.now + (86_400 if "limit" in msg.lower() else RETRY)
                world.event("finding", f"errands: the start was refused ({msg[:120]})", about="errands")
            elif NAME not in msg:
                own["rest_until"] = world.now + RETRY
                world.event("finding", f"errands: an errand the player does not know ({msg[:120]}): resting an "
                                       f"hour; the model adds it", about="exception")
            else:
                world.event("activity_done", f"errands: {NAME}", activity=self.name)
