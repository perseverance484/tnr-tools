"""Recovery: the Full Potion, ramen and the hospital (design 4.3). Ported from the pilot's world().

- Hospitalized: heal at the village hospital.
- While hunting: under 95% HP a Full Potion; chakra or stamina under 50%, ramen (which refills those two only).
  A heal that changed nothing is not tried again for 10 minutes: a guard against a loop, not a fix.
- At the end of a fight: the Full Potion goes in the same batch as the fight's last read (after_fight), because a
  wounded winner is a third party's target within seconds. Then, as soon as the profile shows me out of the
  fight and awake, two tiles off the tile it ended on (not at home); and a repair is owed (repair.py).
- After every fight, a large ramen when chakra or stamina is under POOLS_AFTER_FIGHT, on the first tick awake in hunt
  mode (director 2026-11-16: "Repair, heal and large ramen after every fight"; "The brain can use Ramen, sure.").
  Jutsu spend those pools; the next fight is not started on what the last one left.
"""
from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan


USES = {"item.consume": "Full Potion", "village.buyFood": "ramen"}


@REGISTRY.activity
class Recovery(Activity):
    name = "recovery"
    priority = "safety"
    reads = ("profile.getUser", "item.consume", "village.buyFood")      # (travel.moveInSector: after_fight only)

    def _need(self, world):
        """"hospital", "hp", "cpsp" or None."""
        if world.status() == "HOSPITALIZED":
            return "hospital"
        own = world.own(self.name)
        if world.status() != "AWAKE":
            own.pop("step_off", None)                             # asleep, in a fight or travelling: nothing to step off
            return None
        if own.get("step_off") and not self._off_the_tile(world):
            own.pop("step_off", None)                             # at home, or no tile known: nothing to do
        if own.get("step_off"):
            return "step_off"
        if world["control"]["mode"] != "hunt":
            return None
        pools = world.pools()
        broken = {k for k, t in own.get("broken", {}).items() if t > world.now}
        if pools["hp"] < C.HEAL_BELOW and "hp" not in broken:
            return "hp"
        if pools["cpsp"] < C.POOLS_BELOW and "cpsp" not in broken:
            return "cpsp"
        if own.get("ramen_due"):
            if pools["cpsp"] < C.POOLS_AFTER_FIGHT and "cpsp" not in broken:
                return "cpsp"
            own.pop("ramen_due", None)                            # full enough: nothing owed
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
        if need == "step_off":
            own.pop("step_off", None)
            return plan(self._off_the_tile(world) + [K.user()], "recovery", "off the tile the fight ended on")
        own["healing"] = [need, world.pools()[need]]
        if need == "hp":
            own.setdefault("why", {})["item.consume"] = f"HP at {world.pools()['hp']:.0%}"
            return plan([self._potion(world), K.user()], "recovery", "Full Potion")
        why = "after the fight: " if own.pop("ramen_due", None) else ""
        own.setdefault("why", {})["village.buyFood"] = f"{why}chakra or stamina at {world.pools()['cpsp']:.0%}"
        own["pocket"] = world.me.get("money")                     # the next profile read shows what it cost
        return plan([K.ramen(own.get("ramen_cost")), K.user()], "recovery", "ramen")

    @staticmethod
    def _potion(world):
        return K.potion(world["inventory"].get("full_potion_uid", C.FULL_POTION))

    def after_fight(self, world):
        """The steps to put in front of a fight's closing batch: a Full Potion when I am alive and hurt."""
        end = world["records"].pop("fight_end", None) or {}
        if end:
            world.own(self.name)["ramen_due"] = True              # chakra and stamina, once the fight's reads are in
            if world["control"]["activities"].get("repair", True):
                world.own("repair")["after_fight"] = True         # and a repair (director: "after every fight")
        steps = []
        if end.get("result") != "lost" and 0 < end.get("hp", 0) < C.HEAL_BELOW * end.get("max", C.MAX_HP):
            world.own(self.name).setdefault("why", {})["item.consume"] = f"end of fight at {end['hp']:.0f} HP"
            steps.append(self._potion(world))
        if end and end.get("result") != "lost" and end.get("hp", 0) > 0:
            world.own(self.name)["step_off"] = True               # off the tile, as soon as the profile is read
        return steps

    @staticmethod
    def _off_the_tile(world):
        """One step off the tile the fight ended on, behind the potion: a third party jumps the winner where he
        stands (director: "I usually move it by hand and heal to avoid snipes after fights. You may take over when
        this occurs."). Not at home, where the session sleeps instead, and not without a known tile."""
        me, (x, y) = world.me, world.position()
        sec = me.get("sector")
        if sec is None or sec == C.HOME_SECTOR or not all(isinstance(v, (int, float)) for v in (x, y)):
            return []
        dest = (x + 2 if x < 12 else x - 2, y)
        return [K.move((x, y), dest, sec)]
