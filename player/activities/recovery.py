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


USES = {"item.consume": "Full Potion", "village.buyFood": "ramen"}


@REGISTRY.activity
class Recovery(Activity):
    name = "recovery"
    priority = "safety"
    reads = ("profile.getUser", "item.consume", "village.buyFood")

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
        """What the game said to a potion or a meal (the console's event is written here, from its answer, never
        when the call is only planned), and whether the next profile read shows it worked."""
        own = world.own(self.name)
        for r in results:
            if r.endpoint in USES:
                self._used(world, own, r)
        if not any(r.endpoint == "profile.getUser" and not r.error for r in results):
            return
        last = own.pop("healing", None)
        if last and world.pools()[last[0]] <= last[1] + 1e-9:
            own.setdefault("broken", {})[last[0]] = world.now + C.HEAL_RETRY
        before, after = own.pop("pocket", None), world.me.get("money")
        if own.pop("bought", False) and None not in (before, after) and after < before:
            own["ramen_cost"] = max(own.get("ramen_cost", 0), before - after)    # what a ramen costs, measured

    @staticmethod
    def _used(world, own, r):
        item, why = USES[r.endpoint], (own.get("why") or {}).pop(r.endpoint, None)
        if not r.error and isinstance(r.data, dict) and r.data.get("success"):
            world.event("item", f"{item} {'bought' if item == 'ramen' else 'used'}", item=item, why=why)
            own["bought"] = item == "ramen"
        elif not r.error:
            world.event("finding", f"{item}: the game said no ({(r.data or {}).get('message')})", about="recovery")

    def plan(self, world):
        need, own = self._need(world), world.own(self.name)
        if need == "hospital":
            return plan([K.hospital(), K.user()], "recovery", "HOSPITALIZED: healing")
        own["healing"] = [need, world.pools()[need]]
        if need == "hp":
            own.setdefault("why", {})["item.consume"] = f"HP at {world.pools()['hp']:.0%}"
            return plan([self._potion(world), K.user()], "recovery", "Full Potion")
        own.setdefault("why", {})["village.buyFood"] = f"chakra or stamina at {world.pools()['cpsp']:.0%}"
        own["pocket"] = world.me.get("money")                     # the next profile read shows what it cost
        return plan([K.ramen(own.get("ramen_cost")), K.user()], "recovery", "ramen")

    @staticmethod
    def _potion(world):
        return K.potion(world["inventory"].get("full_potion_uid", C.FULL_POTION))

    def after_fight(self, world):
        """The steps to put in front of a fight's closing batch: a Full Potion when I am alive and hurt."""
        end = world["records"].pop("fight_end", None) or {}
        if end.get("result") != "lost" and 0 < end.get("hp", 0) < C.HEAL_BELOW * end.get("max", C.MAX_HP):
            world.own(self.name).setdefault("why", {})["item.consume"] = f"end of fight at {end['hp']:.0f} HP"
            return [self._potion(world)]
        return []
