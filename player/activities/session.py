"""Session: waking the character when a hunt starts, and putting it to bed when the session ends.

A session ends with the character asleep at home, never awake where it stands (2026-11-11, live: the relay was
stopped with the character awake at 648 HP in an enemy sector; a rematch began with nothing running and its first
round went unplayed). With `end_session` set, the hunt stops, recovery still heals, this activity walks home and
sleeps, and only then does the brain tell the relay to stop. A fight that starts on the way is fought first.

AP2 adds the rest of the session's life (the run lock, the end-of-session training, the loadouts).
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
        return ending and world.status() == "AWAKE"

    def value(self, world):
        return 10.0

    def plan(self, world):
        if world.status() == "ASLEEP":
            return plan([K.wake(), K.user()], "world", "ASLEEP, hunt mode: waking")
        if world.me.get("sector") != C.HOME_SECTOR:
            return plan(K.trip(C.HOME_SECTOR), "world", f"session ending: going home ({C.HOME_SECTOR})")
        return plan([K.wake(), K.user()], "world", "session ending: sleeping at home", hold=C.TRAVEL_RETRY)
