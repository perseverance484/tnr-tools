"""Bank: the money that is not being worked with stays in the bank (design 4.3; director 2026-11-09: "keep about
10M in pocket, the rest banked").

With more than HIGH in pocket, what is over WORKING goes to the bank. With less than LOW in pocket, the pocket is
filled to WORKING from the bank, as far as the bank holds more than the reserve. Moving money between the two
spends nothing: the day's spend is the fall of the two together (world.py). A transfer the game refuses is not
tried again for RETRY seconds.

WORKING is the director's word. LOW and HIGH are mine, and his to change: they only say how far the pocket may
drift from it before a transfer is worth a call.
"""
from .. import calls as K
from ..registry import REGISTRY, Activity, plan

WORKING = 10_000_000       # ryo kept in pocket
LOW = 2_000_000            # under this the pocket is filled again
HIGH = 20_000_000          # over this the surplus is banked
RETRY = 600.0              # s before a refused transfer is tried again
MOVES = {"bank.toBank": "to the bank", "bank.toPocket": "to the pocket"}


@REGISTRY.activity
class Bank(Activity):
    name = "bank"
    priority = "upkeep"
    reads = tuple(MOVES)

    def move(self, world):
        """(the call, a note) for the transfer that is due, or None."""
        me = world.me
        if me.get("money") is None or me.get("bank") is None or world.now < world.own(self.name).get("not_before", 0):
            return None
        pocket, bank = float(me["money"]), float(me["bank"])
        if pocket > HIGH:
            return K.to_bank(pocket - WORKING), f"bank: {pocket - WORKING:,.0f} ryo to the bank"
        spare = bank - world.caps()["reserve"]
        if pocket < LOW and spare >= 1:
            return K.to_pocket(min(WORKING - pocket, spare)), f"bank: {min(WORKING - pocket, spare):,.0f} ryo to the pocket"
        return None

    def available(self, world):
        return world.status() == "AWAKE" and not world.in_battle() and bool(self.move(world))

    def value(self, world):
        return 2.0

    def plan(self, world):
        step, note = self.move(world)
        world.own(self.name)["not_before"] = world.now + RETRY     # the profile read behind it shows whether it took
        return plan([step, K.user()], "world", note)

    def on_result(self, world, results):
        for r in results:
            if r.endpoint not in MOVES:
                continue
            amount = f"{(r.input or {}).get('amount', 0):,.0f} ryo {MOVES[r.endpoint]}"
            if not r.error and isinstance(r.data, dict) and r.data.get("success"):
                world.own(self.name)["not_before"] = 0
                world.event("activity_done", f"bank: {amount}", activity=self.name)
            else:
                said = r.error or (r.data.get("message") if isinstance(r.data, dict) else r.data)
                world.event("finding", f"bank: {amount} was refused ({said})"[:300], about="bank")
