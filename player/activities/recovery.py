"""Recovery: the Full Potion, ramen and the hospital (design 4.3). Ported from the pilot's world().

- Hospitalized: heal at the village hospital.
- While hunting: under 95% HP a Full Potion; chakra or stamina under 50%, ramen (which refills those two only).
  A heal that changed nothing is not tried again for 10 minutes: a guard against a loop, not a fix.
- At the end of a fight: the Full Potion goes in the same batch as the fight's last read (after_fight), because a
  wounded winner is a third party's target within seconds.
"""
from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan


@REGISTRY.activity
class Recovery(Activity):
    name = "recovery"
    priority = "safety"
    reads = ("profile.getUser",)

    def _need(self, world):
        """"hospital", "hp", "cpsp" or None."""
        if world.status() == "HOSPITALIZED":
            return "hospital"
        if world.status() != "AWAKE" or world["control"]["mode"] != "hunt":
            return None
        own, pools = world.own(self.name), world.pools()
        broken = {k for k, t in own.get("broken", {}).items() if t > world.now}
        if pools["hp"] < C.HEAL_BELOW and "hp" not in broken:
            return "hp"
        if pools["cpsp"] < C.POOLS_BELOW and "cpsp" not in broken:
            return "cpsp"
        return None

    def available(self, world):
        return self._need(world) is not None

    def value(self, world):
        return 100.0

    def on_result(self, world, results):
        """After a heal, the next profile read shows whether it worked."""
        if not any(r.endpoint == "profile.getUser" and not r.error for r in results):
            return
        own = world.own(self.name)
        last = own.pop("healing", None)
        if last and world.pools()[last[0]] <= last[1] + 1e-9:
            own.setdefault("broken", {})[last[0]] = world.now + C.HEAL_RETRY

    def plan(self, world):
        need, own = self._need(world), world.own(self.name)
        if need == "hospital":
            return plan([K.hospital(), K.user()], "recovery", "HOSPITALIZED: healing")
        own["healing"] = [need, world.pools()[need]]
        if need == "hp":
            world.event("item", "Full Potion used", item="Full Potion", why=f"HP at {world.pools()['hp']:.0%}")
            return plan([self._potion(world), K.user()], "recovery", "Full Potion")
        world.event("item", "ramen bought", item="ramen", why=f"chakra or stamina at {world.pools()['cpsp']:.0%}")
        return plan([K.ramen(), K.user()], "recovery", "ramen")

    @staticmethod
    def _potion(world):
        return K.potion(world["inventory"].get("full_potion_uid", C.FULL_POTION))

    def after_fight(self, world):
        """The steps to put in front of a fight's closing batch: a Full Potion when I am alive and hurt."""
        end = world["records"].pop("fight_end", None) or {}
        if end.get("result") != "lost" and 0 < end.get("hp", 0) < C.HEAL_BELOW * end.get("max", C.MAX_HP):
            world.event("item", "Full Potion used", item="Full Potion", why=f"end of fight at {end['hp']:.0f} HP")
            return [self._potion(world)]
        return []
