"""Bank: the pocket holds what the character may lose on the road, and no more (design 4.3; director 2026-11-12,
RUL-2026-11-12-153: "10m is fine to pull out for training but 200k is the in pocket limit for running around").

Running around, the pocket holds at most POCKET: more than that goes to the bank, down to KEEP. With less than
LOW in it, it is filled to KEEP again (a ramen is paid from the pocket).

Two activities may ask for more. Each says so in the shared section it writes, and for a few minutes at most:
  training   world["training"]["draw_until"]: places in the queue are to be filled. The pocket is filled to
             TRAINING, and what the fill leaves goes back to the bank when the wish is over.
  restock    world["inventory"]["draw"] {"ryo", "until"}: the shop price of what is short. The pocket is filled
             to that, never past POCKET; restock is told when it is there (inventory.restock_due).

The bank is never taken under the reserve. Moving money between the two spends nothing: the day's spend is the
fall of the two together (world.py). A transfer the game refuses is not tried again for RETRY seconds.

POCKET and TRAINING are the director's words (config.py). KEEP and LOW are mine, and his to change: they only
say how far under the limit the pocket may drift before a transfer is worth a call.
"""
from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan

POCKET = C.POCKET_LIMIT    # ryo: the most the pocket holds while running around
TRAINING = C.TRAINING_DRAW  # ryo: what the pocket is filled to for a training fill
KEEP = 100_000             # ryo a transfer leaves in the pocket when nothing asks for more
LOW = 20_000               # under this the pocket is filled to KEEP again
RETRY = 600.0              # s before a refused transfer is tried again
MOVES = {"bank.toBank": "to the bank", "bank.toPocket": "to the pocket"}


def wish(world):
    """(the ryo the pocket is asked to hold now, who asks): training's wish, else restock's, else (0, None)."""
    if world["training"].get("draw_until", 0) > world.now:
        return TRAINING, "training"
    draw = world["inventory"].get("draw") or {}
    if draw.get("until", 0) > world.now:
        return min(float(draw.get("ryo") or 0), POCKET), "restock"
    return 0, None


@REGISTRY.activity
class Bank(Activity):
    name = "bank"
    priority = "upkeep"
    reads = tuple(MOVES)

    def move(self, world):
        """(the call, a note, who it is for) for the transfer that is due, or None."""
        me = world.me
        if me.get("money") is None or me.get("bank") is None or world.now < world.own(self.name).get("not_before", 0):
            return None
        pocket, spare = float(me["money"]), float(me["bank"]) - world.caps()["reserve"]
        want, who = wish(world)
        if who and pocket < want:
            give = min(want - pocket, spare)
            return (K.to_pocket(give), f"bank: {give:,.0f} ryo to the pocket for {who}", who) if give >= 1 else None
        if who == "training":
            return None                        # the fill is still to come: what is in the pocket stays there
        if pocket > POCKET:
            return K.to_bank(pocket - KEEP), f"bank: {pocket - KEEP:,.0f} ryo to the bank", None
        if pocket < LOW and spare >= 1:
            give = min(KEEP - pocket, spare)
            return K.to_pocket(give), f"bank: {give:,.0f} ryo to the pocket", None
        return None

    def available(self, world):
        return world.status() == "AWAKE" and not world.in_battle() and bool(self.move(world))

    def value(self, world):
        return 2.0

    def plan(self, world):
        step, note, who = self.move(world)
        world.own(self.name).update(not_before=world.now + RETRY, who=who)   # the answer shows whether it took
        return plan([step, K.user()], "world", note)

    def on_result(self, world, results):
        own = world.own(self.name)
        for r in results:
            if r.endpoint not in MOVES:
                continue
            amount = f"{(r.input or {}).get('amount', 0):,.0f} ryo {MOVES[r.endpoint]}"
            if not r.error and isinstance(r.data, dict) and r.data.get("success"):
                own["not_before"] = 0
                if own.pop("who", None) == "restock":
                    world["inventory"]["restock_due"] = True       # the pocket can pay now: restock looks again
                world.event("activity_done", f"bank: {amount}", activity=self.name)
            else:
                said = r.error or (r.data.get("message") if isinstance(r.data, dict) else r.data)
                world.event("finding", f"bank: {amount} was refused ({said})"[:300], about="bank")
