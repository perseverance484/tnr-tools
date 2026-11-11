"""Travel: landing a trip that is under way. Any activity starts a trip with calls.go(sector); while the character
is in transit nothing else can be done, so this waits for the arrival time and finishes the move."""
from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan

STILL = ("AWAKE", "BATTLE", "ASLEEP", "HOSPITALIZED")


@REGISTRY.activity
class Travel(Activity):
    name = "travel"
    priority = "deadlines"

    def available(self, world):
        return bool(world.status()) and world.status() not in STILL

    def value(self, world):
        return 10.0

    def plan(self, world):
        arrive = world["timers"].get("arrive")
        left = max(0.0, arrive - world.now) if arrive else 5.0     # unknown arrival: try again in 5 s
        left = max(left, C.TRAVEL_RETRY)                           # past the arrival time and not landed: pause
        return plan([K.finish_trip(), K.user()], "world", f"{world.status()}: arriving in {left:.0f}s",
                    hold=round(min(left + 0.5, 20.0), 1))
