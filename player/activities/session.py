"""Session: waking the character when a hunt starts, and putting it to bed when the session ends.

A session ends with the character asleep at home, never awake where it stands (2026-11-11, live: the relay was
stopped with the character awake at 648 HP in an enemy sector; a rematch began with nothing running and its first
round went unplayed). With `end_session` set, the hunt stops, recovery still heals, this activity walks home and
sleeps, and only then does the brain tell the relay to stop. A fight that starts on the way is fought first.

At home, before it sleeps, the upkeep has its last turn (brief AP2): the energy that is left is trained, and the
PvP 1 loadouts are selected. Those are the training and the equipment activities' calls: this one only waits
for them, and only while they have something to do and are switched on.

The run lock (brief AP2: "start: lock ... release the lock") is the brain's (director 2026-11-12: "Give it to
the brain then"): it is claimed before the session's first call and given back once the character is asleep.
That is not a game call and no activity's plan: player/runlock.py, called from the brain's tick.
"""
from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan


@REGISTRY.activity
class Session(Activity):
    name = "session"
    priority = "deadlines"

    def available(self, world):
        ending = world["control"]["end_session"]
        if world.status() == "ASLEEP":
            return world["control"]["mode"] == "hunt" and not ending
        return ending and world.status() == "AWAKE" and not self._chores(world)

    @staticmethod
    def _chores(world):
        """With the session ending, what comes before this activity's next step. Away from home: the bank, while
        the pocket holds more than it may on the road (no trip home with it: review of 988c56cc, H3). At home:
        the upkeep that has something to do before the character sleeps."""
        if world.me.get("sector") != C.HOME_SECTOR:
            return world.overfull()
        acts, on = REGISTRY.activities, world["control"]["activities"]
        return any(on.get(name, True) and acts[name].available(world) for name in ("training", "equipment", "bank")
                   if name in acts)

    def value(self, world):
        return 10.0

    def plan(self, world):
        if world.status() == "ASLEEP":
            return plan([K.wake(), K.user()], "world", "ASLEEP, hunt mode: waking")
        if world.me.get("sector") != C.HOME_SECTOR:
            return plan(K.trip(C.HOME_SECTOR), "world", f"session ending: going home ({C.HOME_SECTOR})")
        return plan([K.wake(), K.user()], "world", "session ending: sleeping at home", hold=C.TRAVEL_RETRY)
