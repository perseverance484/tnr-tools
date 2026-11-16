"""Harvest: other players' battle logs, read a couple at a time between fights, for the opponent models
(the pilot's harvest_calls). It never runs on its own: it rides a quiet hunt batch when the call budget has room.

The gate study_only keeps these reads out of a fight. What they teach may be used in live play, a named opponent
included (RUL-2026-11-09-146, RUL-2026-11-11-151). The director can switch this activity off from the console.
"""
from .. import calls as K
from ..registry import REGISTRY, Activity, plan

PER_BATCH = 2
SPARE = 4            # world calls left free after the harvest reads: a fight can start on any tick


@REGISTRY.activity
class Harvest(Activity):
    name = "harvest"
    priority = "scouting"
    reads = ("combat.getBattleHistory", "combat.getBattleEntries", "profile.getStrongestUsers")
    rides = True       # the brain adds its calls to another activity's quiet world batch

    def available(self, world):
        return (world.status() == "AWAKE" and not world.in_battle() and world["control"]["mode"] == "hunt"
                and self.budget.headroom() >= PER_BATCH + SPARE)

    def value(self, world):
        return 0.01

    def plan(self, world):
        hv = self.combat.harvest()
        h = hv.load()
        if not h.get("seeded"):
            hv.seed(h, self.combat.harvest_seed_ids())
        steps = [K.call(*c) for c in hv.next_calls(h, PER_BATCH)]
        hv.save(h)
        return plan(steps, "world", "harvest") if steps else None

    def on_result(self, world, results):
        got = [r for r in results if r.endpoint in self.reads and not r.error]
        if not got:
            return
        hv = self.combat.harvest()
        h = hv.load()
        if any([hv.ingest(h, r.endpoint, r.input, r.data) for r in got]):
            hv.save(h)
            world.own(self.name)["stats"] = hv.stats(h)
