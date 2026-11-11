"""Session: waking the character when a hunt starts. AP2 adds the rest of the session's life (the run lock, the
end-of-session training, sleep at home, the loadouts)."""
from .. import calls as K
from ..registry import REGISTRY, Activity, plan


@REGISTRY.activity
class Session(Activity):
    name = "session"
    priority = "deadlines"

    def available(self, world):
        return world.status() == "ASLEEP" and world["control"]["mode"] == "hunt"

    def value(self, world):
        return 10.0

    def plan(self, world):
        return plan([K.wake(), K.user()], "world", "ASLEEP, hunt mode: waking")
