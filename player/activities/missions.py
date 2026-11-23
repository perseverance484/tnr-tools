"""Missions and medical: the day's A-rank missions and D-rank medical runs (tnr-autopilot DESIGN.md section 5;
director 2026-11-10: "20 missions and 50 errands is the cap"; RUL-2026-11-11-149 item 5: 9 medical).

Off until the director switches it on (control.json activities.missions): a mission is a chain of steps the
player cannot read on its own yet. Each step's goals and next objective come from the quest's own record, whose
shape is not on record for the brain (the hunt thread ran nine medicals by hand on 2026-11-15: a chain of
quests.checkRewards with nextObjectiveId, a move and quests.checkLocationQuest at each goal, a PvE fight inside,
then quests.checkRewards with the questId alone to claim).

So, switched on, this activity does what is sure and hands the rest over: at home, it starts the run (medical
first, then missions), reads the account's quests whole and keeps the read in live/exceptions/, and writes a
finding about "exception": the model takes the chain from there. It starts nothing more while a run waits on the
model (WAIT), and a start the game refuses rests it for an hour, or for the day when it speaks of a limit. A fight
inside a run is a fight against AI: the battle activity plays it.
"""
import datetime as dt
import json
import os

from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan
from .errands import behind, paced_value

KINDS = (("medical", "D", 9), ("mission", "A", 20))     # type, rank, the day's cap (the director's to confirm)
WAIT = 1800.0              # s a started run is left to the model before the next one may start
HOLD = 120.0               # s between the profile reads that hold the account while a run waits on the model
RETRY = 3600.0


@REGISTRY.activity
class Missions(Activity):
    name = "missions"
    priority = "goals"
    goal = "daily_caps"
    starts_off = True
    reads = ("quests.startRandom", "quests.getUserQuests")

    def _day(self, world):
        own = world.own(self.name)
        day = dt.datetime.fromtimestamp(world.now, dt.timezone.utc).strftime("%Y-%m-%d")
        if own.get("day") != day:
            own.update(day=day, counts={k: 0 for k, _, _ in KINDS})
        return own

    def next_kind(self, world):
        own = self._day(world)
        return next(((k, r, cap) for k, r, cap in KINDS if own["counts"].get(k, 0) < cap
                     and own.get("rest", {}).get(k, 0) <= world.now), None)

    def waiting(self, world):
        """The run the model has, or None. The model's quest_done ends the wait (and is used up)."""
        own, ctl = self._day(world), world["control"]
        if ctl.get("quest_done"):
            ctl["quest_done"] = False
            if own.get("model_until", 0) > world.now:
                world.event("activity_done", f"missions: the model handed the {own.get('held', 'run')} back",
                            activity=self.name)
            own["model_until"] = 0
        return own.get("held") if own.get("model_until", 0) > world.now else None

    def available(self, world):
        if world.status() != "AWAKE" or world.in_battle() or world["control"]["mode"] != "hunt":
            return False
        if self.waiting(world):
            return True
        return not world["control"]["end_session"] and self.next_kind(world) is not None

    def value(self, world):
        if self.waiting(world):
            return 1000.0                               # the account stays put while the model runs the chain
        own, (kind, _, cap) = self._day(world), self.next_kind(world)
        return paced_value(behind(own["counts"].get(kind, 0), cap, world.now), False)

    def plan(self, world):
        held = self.waiting(world)
        if held:
            return plan([K.user()], "world", f"holding the account for the model's {held} run", hold=HOLD)
        kind, rank, cap = self.next_kind(world)
        own = self._day(world)
        if world.me.get("sector") != C.HOME_SECTOR:
            return plan(K.go(C.HOME_SECTOR), "world", f"{kind} {own['counts'][kind]}/{cap}: going to the village")
        own["sent"] = kind
        return plan([K.call("quests.startRandom", {"type": kind, "rank": rank, "userLevel": 100,
                                                   "userSector": C.HOME_SECTOR, "userVillageId": C.HOME_VILLAGE},
                            ["success", "message"]),
                     K.call("quests.getUserQuests", {"userId": C.ME}, []), K.user()],
                    "world", f"{kind} {own['counts'][kind] + 1}/{cap}: starting it, for the model to run")

    def on_result(self, world, results):
        own = self._day(world)
        for r in results:
            if r.endpoint == "quests.startRandom" and own.get("sent") and own["sent"] == (r.input or {}).get("type"):
                kind, data = own.pop("sent"), r.data if isinstance(r.data, dict) else {}
                msg = str(data.get("message") or r.error or "")
                if r.error or not data.get("success"):
                    own.setdefault("rest", {})[kind] = world.now + (86_400 if "limit" in msg.lower() else RETRY)
                    world.event("finding", f"{kind}: the start was refused ({msg[:120]})", about="missions")
                else:
                    own["counts"][kind] = own["counts"].get(kind, 0) + 1
                    own["model_until"], own["held"] = world.now + WAIT, kind
                    own["started"] = {"kind": kind, "message": msg[:200], "at": world.now}
            elif r.endpoint == "quests.getUserQuests" and own.get("started") and not r.error:
                path = self._keep(world, r, own.pop("started"))
                world.event("finding", f"a run is started and its chain is for the model: {path}", about="exception")

    @staticmethod
    def _keep(world, r, started):
        folder = os.path.join(world.live, "exceptions")
        name = f"quest-{int(world.now)}.json"
        try:
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, name), "w", encoding="utf8") as f:
                json.dump({"started": started, "quests": r.data}, f, default=str)
        except OSError:
            return "the quest read could not be kept"
        return f"live/exceptions/{name}"
