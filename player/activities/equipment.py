"""Equipment: what is equipped, kept right for what the character is doing (design 4.3; RUL-2026-11-11-150 and
-152 item 4). Three things, and no more yet:

  1. What sits in each slot is written where the planners look for it (the `equipped` feed), from every read
     of my items: the thrown weapon in it is the one the planner's "kunai" throws. This was the pilot's
     restock.py, which wrote the file as a side effect.
  2. When the thrown slot is empty and a backup thrown weapon is carried, the backup goes in (director
     2026-11-11: "I bought 50 ikazuchi kunai that can be swapped in when the elemental kunai run out"). While a
     backup is carried, restock does not buy the kunai again.
  3. The PvP 1 loadouts are selected for the hunt: when a hunt begins, and before a session ends. PvP 1 is
     selected and never edited. Nothing the brain is allowed to read yet says which loadout is selected (those
     reads are proposed on the allowlist), so it selects, and remembers that it did.

     A selection changes what is equipped, so it is not finished until my items have been read again. From
     the moment it is planned the items are `stale` (world["inventory"], a row for the batch that changes
     them: player/owed.py): the hunt, restock and repair wait, and the read goes in the same batch behind the
     two selections (review of 988c56cc, H4: the selection was followed by a profile read only, and the next
     fight threw the weapon of the loadout before).

     Only a read that is known to follow the selection ends the wait: the batch's own, handed in with it, or
     one asked for after the brain knew the batch was over. While that batch can still run (a replaced relay
     has it) no read ends it: a replacement's read, made before the first relay had selected, used to
     (re-review of 87e497a6, H4). While the wait lasts my items are asked for again every READ_AGAIN seconds,
     and at once when the batch is known to be over. Each such read brings the feed up to what is equipped at
     that moment, which is what a fight that comes unasked is planned on.

Not built here: choosing PvP 2 (which opponent calls for it is the dossier's to say: AP4), changing what is in
PvP 2, and equipping an upgrade the account already owns (nothing says yet which of two items is the better).
"""
from .. import calls as K
from .. import owed
from ..registry import REGISTRY, Activity, plan

BACKUP_THROWN = ("GMF1JZ0MChUHc7AtnKABw",)                     # Ikazuchi Kunai, in the order to try them
PVP1 = ("soXekhNjk7qihu-Rsok-6", "B-bCCtg-_fvcJSrvR1ts0")      # jutsu loadout, item loadout (pvp_playbook.md)
SELECTS = ("jutsu.selectJutsuLoadout", "item.selectItemLoadout")
RETRY = 600.0              # s before a refused swap or selection is tried again
READ_AGAIN = 30.0          # s before my items are asked for again after a selection whose read did not come


@REGISTRY.activity
class Equipment(Activity):
    name = "equipment"
    priority = "upkeep"
    reads = ("item.getUserItems", "item.toggleEquip") + SELECTS

    # ------------------------------------------------------------ what there is to do
    @staticmethod
    def backup(world):
        """The carried stack of the first backup thrown weapon that is not the one equipped, or None."""
        thrown = (world["inventory"].get("equipped") or {}).get("THROWN")
        return next((x for b in BACKUP_THROWN if b != thrown for x in world.items(b, carried=True)), None)

    def wants(self, world):
        """"read" (my items, after a selection), "thrown" (the backup goes in), "loadout" (PvP 1 is to be
        selected), or None."""
        own, inv = world.own(self.name), world["inventory"]
        if inv.get("stale"):
            return "read" if world.now >= own.get("read_next", 0) else None
        if world.now < own.get("not_before", 0):
            return None
        if "equipped" in inv and not inv["equipped"].get("THROWN") and self.backup(world):
            return "thrown"
        hunting = world["control"]["mode"] == "hunt" or world["control"]["end_session"]
        return "loadout" if hunting and own.get("selected") != list(PVP1) else None

    def available(self, world):
        return world.status() == "AWAKE" and not world.in_battle() and bool(self.wants(world))

    def value(self, world):
        return 5.0

    # ------------------------------------------------------------ what the game said
    def on_result(self, world, results):
        own, inv = world.own(self.name), world["inventory"]
        for r in results:
            if r.endpoint == "item.getUserItems" and inv.get("read_at") != own.get("seen"):
                own["seen"] = inv.get("read_at")                   # (a read that could be used: the world took it)
                self.combat.write_equipped(inv.get("equipped") or {})
                inv["backup_thrown"] = bool(self.backup(world))
                inv["stale"] = owed.read(world, inv.get("stale"))   # what it is known to have been read behind
            elif r.endpoint in SELECTS or (r.endpoint == "item.toggleEquip" and own.get("swapping")):
                self._said(world, own, r)
        was, inv["stale"] = owed.rows(inv.get("stale")), owed.settle(world, inv.get("stale"))
        if inv["stale"] != was:
            own["read_next"] = world.now                            # a batch is over: the read that follows it, now
        if not inv["stale"]:
            del inv["stale"]

    @staticmethod
    def _said(world, own, r):
        ok = not r.error and isinstance(r.data, dict) and bool(r.data.get("success"))
        if r.endpoint == "item.toggleEquip":
            own.pop("swapping", None)
        elif ok:
            own.setdefault("answered", []).append((r.input or {}).get("id"))
            if sorted(own["answered"]) == sorted(PVP1):
                own.update(selected=list(PVP1), answered=[])
                world.event("activity_done", "equipment: the PvP 1 loadouts are selected", activity="equipment")
        if not ok:
            said = r.error or (r.data.get("message") if isinstance(r.data, dict) else r.data)
            own.update(not_before=world.now + RETRY, answered=[])
            world.event("finding", f"equipment: {r.endpoint} was refused ({said})"[:300], about="equipment")

    # ------------------------------------------------------------ the plan
    @staticmethod
    def _changing(world):
        """The batch this tick makes changes what is equipped: my items are stale until they are read behind it."""
        inv = world["inventory"]
        inv["stale"] = owed.rows(inv.get("stale")) + [[world.making, None]]

    def plan(self, world):
        own, what = world.own(self.name), self.wants(world)
        own["read_next"] = world.now + READ_AGAIN
        if what == "read":
            return plan([K.items(), K.user()], "world", "reading what is equipped since the loadouts were selected")
        own["not_before"] = world.now + RETRY                      # an answer that says yes needs no second try
        if what == "thrown":
            spare = self.backup(world)
            own["swapping"] = True
            self._changing(world)
            return plan([K.equip(spare["id"], "THROWN"), K.items()], "world",
                        f"the thrown slot is empty, the backup goes in ({spare['quantity']})")
        own["answered"] = []
        self._changing(world)
        return plan(K.loadouts(*PVP1) + [K.items(), K.user()], "world", "selecting the PvP 1 loadouts")
