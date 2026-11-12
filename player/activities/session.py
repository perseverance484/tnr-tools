"""Session: waking the character when a hunt starts, and putting it to bed when the session ends.

A session ends with the character asleep at home, never awake where it stands (2026-11-11, live: the relay was
stopped with the character awake at 648 HP in an enemy sector; a rematch began with nothing running and its first
round went unplayed). With `end_session` set, the hunt stops, recovery still heals, this activity walks home and
sleeps, and only then does the brain tell the relay to stop. A fight that starts on the way is fought first.

At home, before it sleeps, the upkeep has its last turn (brief AP2): the energy that is left is trained, and the
PvP 1 loadouts are selected. Those are the training and the equipment activities' calls: this one only waits
for them, and only while they have something to do and are switched on.

Not built: the run lock (brief AP2: "start: lock ... release the lock"). The lock is a file on `main` that a
runner claims by pushing; how the player is to hold it (the brain itself, or whoever starts the relay) is not
decided, and nothing here pushes anywhere.
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
        """At home with the session ending: is there upkeep to do before the character sleeps."""
        if world.me.get("sector") != C.HOME_SECTOR:
            return False
        acts, on = REGISTRY.activities, world["control"]["activities"]
        return any(on.get(name, True) and acts[name].available(world) for name in ("training", "equipment")
                   if name in acts)

    def value(self, world):
        return 10.0

    def plan(self, world):
        if world.status() == "ASLEEP":
            return plan([K.wake(), K.user()], "world", "ASLEEP, hunt mode: waking")
        if world.me.get("sector") != C.HOME_SECTOR:
            return plan(K.trip(C.HOME_SECTOR), "world", f"session ending: going home ({C.HOME_SECTOR})")
        return plan([K.wake(), K.user()], "world", "session ending: sleeping at home", hold=C.TRAVEL_RETRY)
