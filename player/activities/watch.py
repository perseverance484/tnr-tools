"""Watch: the idle heartbeat. When nothing else has a call to make, read my profile every few seconds: an attack
opens with a 15 s lobby, so a read every ~9 s cannot miss one."""
from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan


@REGISTRY.activity
class Watch(Activity):
    name = "watch"
    priority = "scouting"

    def available(self, world):
        return world.status() != "ASLEEP"

    def value(self, world):
        return 0.1

    def plan(self, world):
        if not world.status():
            return plan([K.user()], "world", "start")
        me = world.me
        return plan([K.user()], "world", f"AWAKE guard {me.get('curHealth', 0):.0f}/{me.get('maxHealth', 0):.0f} HP "
                                          f"@ {me.get('sector')}: guarding", hold=C.WATCH_WAIT)
