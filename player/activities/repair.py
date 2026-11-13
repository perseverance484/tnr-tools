"""Repair: only what is close to broken (design 4.3; director 2026-11-11: worn is fine, broken is not). Ported
from the pilot's restock.py.

An equipped item under BELOW of its durability when new is repaired, with everything else that is worn: first
with Repair Kits (item.useRepairAll), then with ryo (item.repairAll, which needs the Crafting occupation).
Whichever the game refuses, the other is tried next; neither is tried twice within RETRY seconds. The items
are read again behind the repair, so the next look knows whether it took. Restock keeps the kits in stock.
"""
from .. import calls as K
from ..registry import REGISTRY, Activity, plan

BELOW = 0.25               # of the durability when new
RETRY = 600.0              # s before the same way of repairing is tried again
WAYS = (("item.useRepairAll", True, "Repair Kits"), ("item.repairAll", False, "ryo"))


@REGISTRY.activity
class Repair(Activity):
    name = "repair"
    priority = "upkeep"
    reads = tuple(w[0] for w in WAYS)

    def worn(self, world):
        """The equipped items that are close to broken: ["name durability/when new", ...]."""
        out = []
        for x in world.items(carried=True):
            rec = self.combat.item_record(x["itemId"]) if x["worn"] else {}
            new, left = rec.get("maxDurability") or 0, x["durability"]
            if new and isinstance(left, (int, float)) and not isinstance(left, bool) and left < BELOW * new:
                out.append(f"{rec.get('name') or x['itemId']} {left:g}/{new:g}")
        return out

    def _way(self, world):
        tried = world.own(self.name).get("tried") or {}
        return next((w for w in WAYS if world.now - tried.get(w[0], 0) > RETRY), None)

    def available(self, world):
        return (world.status() == "AWAKE" and not world.in_battle() and not world["inventory"].get("stale")
                and bool(self._way(world)) and bool(self.worn(world)))

    def value(self, world):
        return 8.0

    def plan(self, world):
        (endpoint, kits, how), worn = self._way(world), self.worn(world)
        own = world.own(self.name)
        own.setdefault("tried", {})[endpoint] = world.now
        own["doing"] = f"{', '.join(worn)} with {how}"
        return plan([K.repair(kits), K.items()], "world", f"repair with {how}: {', '.join(worn)}")

    def on_result(self, world, results):
        own = world.own(self.name)
        for r in results:
            if r.endpoint not in self.reads:
                continue
            what = own.pop("doing", None) or r.endpoint
            if not r.error and isinstance(r.data, dict) and r.data.get("success"):
                world.event("repair", f"repaired {what}")
            else:
                said = r.error or (r.data.get("message") if isinstance(r.data, dict) else r.data)
                world.event("finding", f"repair: {what}: the game said no ({said})"[:300], about="repair")
