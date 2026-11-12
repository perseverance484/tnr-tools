"""Restock: the battle consumables, kept up from the item shop, home storage and the auction house (design 4.3).
Ported from the pilot's restock.py `plan` (director 2026-11-11: "restock all items automatically from item shop,
inventory, home storage and auction house").

A pass: read my items and my profile, act on what is short, read again, until nothing is short or PASSES passes
have gone. Then again every EVERY seconds, and after every fight (an item the game refused is the usual sign of
an empty stack). Per tracked item, in this order:
  1. carried, and no stack of it equipped: equip it in the slot it used to have;
  2. stored at home: take it out (then 1, on the next pass);
  3. sold in the item shop for ryo and for nothing else: buy up to the target;
  4. otherwise the auction house: a listing in ryo with a buyout at or under the item's cap for one unit.
What a purchase costs goes to the gates with it (spend_cap holds it against the reserve and the day's cap), and
only a purchase the catalog or the listing shows to be in ryo is asked for at all (ryo_only).

The shop is paid from the pocket, and the pocket holds little on the road (activities/bank.py). A pass buys what
the pocket can pay, each purchase out of what the one before left. When it cannot pay for one piece of what is
short and the bank could, the bank is asked to fill the pocket (inventory.draw, never past the pocket's limit),
and restock looks again once it has. The auction house is paid from the bank.
"""
from .. import calls as K
from .. import config as C
from ..registry import REGISTRY, Activity, plan

# item id -> (short name, keep at least, refill to, auction cap for one unit in ryo); the pilot's table
TRACK = {
    "6DnJn4x6LWWXtBu7UZybb": ("kims", 3, 6, 150_000),
    "TtYPd-LcXKeK3sMuhq1TP": ("smoke", 3, 6, 50_000),
    "rsc2uO5QuffXzejfhwF_F": ("panacea", 3, 6, 55_000),
    "tZTvqYWiAc_OrY64nDvIo": ("pill", 5, 15, 1_000),
    "yVNeLzxHSFkNpTPnlm7yQ": ("kunai", 10, 30, 3_000),
    # Repair Kits are not sold in the shop (7 fixed the whole set and both swords, 2026-11-11)
    "1ovHq7jsGdut2fSNKs5q_": ("repairkit", 7, 20, 50_000),
}
KUNAI = "yVNeLzxHSFkNpTPnlm7yQ"
FULL_POTION_KEEP = ("fullpotion", 5, 15, 20_000)
EVERY = 900.0              # s between passes when nothing calls for one
PASSES = 4                 # acting passes in a row before it lets go until the next time
READ_TRIES = 3             # item reads that cannot be used before a pass is given up
AUCTION_RETRY = 3600.0     # s before the auction house is searched again for an item it did not have
DRAW_FOR = 300.0           # s the bank is asked to fill the pocket for a purchase
BOUGHT = {"item.buy": "bought", "auction.placeBid": "won at auction"}


def what(step_or_result):
    """What a restock call is filed under until the game has answered it: the endpoint and the thing it names."""
    inp = step_or_result.input if hasattr(step_or_result, "input") else step_or_result["input"]
    name = step_or_result.endpoint if hasattr(step_or_result, "endpoint") else step_or_result["call"]
    return f"{name}:{(inp or {}).get('itemId') or (inp or {}).get('auctionId') or (inp or {}).get('userItemId')}"


def unit_price(listing, iid):
    """What one unit costs at a listing's buyout, when the listing is of this item and in ryo; else None."""
    price = listing["buyoutPrice"]
    if listing["currencyType"] != "MONEY" or listing["userItem.itemId"] != iid \
            or not isinstance(price, (int, float)) or isinstance(price, bool) or price <= 0:
        return None
    return price / max(1, listing["quantity"] or listing["userItem.quantity"] or 1)


def for_ryo(rec):
    """The catalog shows the shop sells it, for ryo and nothing else."""
    return bool(rec.get("inShop")) and not rec.get("repsCost") and not rec.get("seichiSilverCost")


@REGISTRY.activity
class Restock(Activity):
    name = "restock"
    priority = "upkeep"
    reads = ("item.getUserItems", "auction.getAuctionListings", "item.buy", "auction.placeBid", "item.toggleEquip",
             "home.toggleStoreItem")

    def available(self, world):
        own = world.own(self.name)
        return (world.status() == "AWAKE" and not world.in_battle()
                and bool(own.get("active") or world["inventory"].get("restock_due") or world.now >= own.get("next", 0)))

    def value(self, world):
        return 6.0

    # ------------------------------------------------------------ what the game said
    def on_result(self, world, results):
        own, inv = world.own(self.name), world["inventory"]
        for r in results:
            if r.endpoint == "item.getUserItems":
                self._read(world, own, inv)
            elif r.endpoint == "auction.getAuctionListings" and own.get("query"):
                rows = None if r.error or not isinstance(r.data, dict) else K.rows(r.data, "data.*.", K.AUCTION_COLS)
                own["listings"] = {"item": own.pop("query"), "rows": rows or []}
            elif r.endpoint in BOUGHT or r.endpoint in ("item.toggleEquip", "home.toggleStoreItem"):
                self._said(world, own, r)

    @staticmethod
    def _read(world, own, inv):
        """A read of my items came back. When the world model took it, the pass may act on it."""
        if inv.get("read_at") != own.get("seen"):
            own.update(seen=inv.get("read_at"), fresh=True, tries=0)
        else:
            own["tries"] = own.get("tries", 0) + 1

    @staticmethod
    def _said(world, own, r):
        thing = (own.get("doing") or {}).pop(what(r), None) or r.endpoint
        if not r.error and isinstance(r.data, dict) and r.data.get("success"):
            if r.endpoint in BOUGHT:
                world.event("item", f"restock: {BOUGHT[r.endpoint]} {thing}", item=thing)
        else:
            said = r.error or (r.data.get("message") if isinstance(r.data, dict) else r.data)
            world.event("finding", f"restock: {thing}: the game said no ({said})"[:300], about="restock")

    # ------------------------------------------------------------ the pass
    def plan(self, world):
        own, inv = world.own(self.name), world["inventory"]
        if not own.get("active"):
            own.update(active=True, passes=0, fresh=False, tries=0, query=None, listings=None)
            inv.pop("restock_due", None)
        if not own.get("fresh"):
            if own.get("tries", 0) >= READ_TRIES:
                return self._rest(world, ["my items could not be read"])
            return plan([K.items(), K.user()], "world", "restock: reading my items")
        own["fresh"] = False
        steps, notes = self._short(world)
        if not steps or own["passes"] >= PASSES:
            return self._rest(world, notes)
        own["passes"] += 1
        return plan(steps + [K.items(), K.user()], "world", "restock: " + "; ".join(notes))

    @staticmethod
    def _rest(world, notes):
        """The pass is over: nothing more until EVERY has gone, or a fight has."""
        world.own("restock").update(active=False, next=world.now + EVERY, last=notes)
        return None

    def _short(self, world):
        """(the calls for everything that is short, in the table's order; a note for each)."""
        inv, steps, notes = world["inventory"], [], []
        world.own(self.name)["purse"] = float(world.me.get("money") or 0)   # what the pocket can still pay this pass
        inv.pop("draw", None)
        self._potion(world)
        inv["empty_items"] = [i for i in TRACK if not world.items(i, carried=True)]
        for iid, (name, keep, fill, cap) in self._tracked(world).items():
            got, note = self._one(world, iid, name, keep, fill, cap)
            steps += got
            if note:
                notes.append(note)
        return steps, notes

    @staticmethod
    def _potion(world):
        """The Full Potion is used by the id of the stack that is carried: keep that id current."""
        inv = world["inventory"]
        row = next((x for x in world.items() if x["id"] == inv.get("full_potion_uid", C.FULL_POTION)), None)
        if row:
            inv["full_potion_item"] = row["itemId"]
        carried = world.items(inv["full_potion_item"], carried=True) if inv.get("full_potion_item") else []
        if carried:
            inv["full_potion_uid"] = carried[0]["id"]

    @staticmethod
    def _tracked(world):
        """The table, with the thrown weapon that is equipped in the kunai's place, and the Full Potion."""
        inv, table = world["inventory"], dict(TRACK)
        thrown = (inv.get("equipped") or {}).get("THROWN")
        if thrown and thrown not in table:
            table[thrown] = table.pop(KUNAI)
        if inv.get("full_potion_item"):
            table[inv["full_potion_item"]] = FULL_POTION_KEEP
        return table

    def _one(self, world, iid, name, keep, fill, cap):
        """(calls, note) for one tracked item."""
        inv, own = world["inventory"], world.own(self.name)
        carried = world.items(iid, carried=True)
        slot = self._lost_slot(inv, iid, carried)
        if slot:
            return [K.equip(carried[0]["id"], slot)], f"equip {name} in {slot}"
        have = sum(x["quantity"] for x in carried)
        if have >= keep or (name == "kunai" and inv.get("backup_thrown")):
            return [], None                    # enough; or a backup thrown weapon goes in when these run out
        home = world.items(iid, carried=False)
        if home:
            return [K.unstore(x["id"]) for x in home], f"{name}: take {sum(x['quantity'] for x in home)} out of storage"
        rec = self.combat.item_record(iid)
        if for_ryo(rec):
            return self._shop(world, own, iid, name, fill - have, rec)
        return self._auction(world, own, iid, name, f"{have}/{keep}", cap, rec)

    @staticmethod
    def _lost_slot(inv, iid, carried):
        """The slot a carried item used to sit in, when no stack of it is equipped now (the Full Potion has none)."""
        if not carried or iid == inv.get("full_potion_item") or any(x["worn"] for x in carried):
            return None
        return (inv.get("slots") or {}).get(iid)

    @staticmethod
    def _shop(world, own, iid, name, want, rec):
        caps, unit, purse = world.caps(), max(1.0, float(rec.get("cost") or 0)), own.get("purse", 0.0)
        above = purse + float(world.me.get("bank") or 0) - caps["reserve"]
        can = int(min(want, above // unit, (caps["daily"] - world.spent_today()) // unit, rec.get("stackSize") or 50, 50))
        if can <= 0:
            return [], f"{name}: short, and the reserve or the day's cap leaves nothing to buy it with"
        n = int(min(can, purse // unit))
        if n <= 0 and unit > C.POCKET_LIMIT:
            return [], f"{name}: short, and one costs more than the pocket may hold ({unit:,.0f} ryo)"
        if n <= 0:
            world["inventory"]["draw"] = {"ryo": min(can * unit, C.POCKET_LIMIT), "until": world.now + DRAW_FOR}
            return [], f"{name}: short, and the pocket cannot pay for one: the bank is asked"
        own["purse"] = purse - n * unit
        step = K.buy(iid, n, n * unit)
        own.setdefault("doing", {})[what(step)] = f"{n} {rec.get('name') or name} ({n * unit:,.0f} ryo)"
        return [step], f"{name}: buy {n} in the shop ({n * unit:,.0f} ryo)"

    def _auction(self, world, own, iid, name, count, cap, rec):
        listed = own.get("listings") or {}
        if listed.get("item") == iid:
            own["listings"] = None
            best = self._best(world, listed["rows"], iid, cap)
            if best:
                price, qty = best["buyoutPrice"], best["quantity"] or best["userItem.quantity"] or 1
                step = K.bid(best["id"], price)
                own.setdefault("doing", {})[what(step)] = f"{qty} {rec.get('name') or name} ({price:,.0f} ryo)"
                return [step], f"{name}: auction buyout, {qty} for {price:,.0f} ryo"
            own.setdefault("none", {})[iid] = world.now
            return [], f"{name}: short ({count}), no auction listing at or under {cap:,} ryo each"
        if not own.get("query") and world.now - (own.get("none") or {}).get(iid, 0) > AUCTION_RETRY:
            own["query"] = iid
            return [K.listings(iid, rec.get("name") or name)], f"{name}: short ({count}), searching the auction house"
        return [], None

    @staticmethod
    def _best(world, rows, iid, cap):
        """The cheapest listing of this item, for one unit, that is in ryo, has a buyout at or under the cap,
        and that the bank can pay above the reserve and inside the day's cap. None when there is none."""
        caps, bank = world.caps(), float(world.me.get("bank") or 0)
        afford = min(bank - caps["reserve"], caps["daily"] - world.spent_today())
        priced = [(unit_price(x, iid), x) for x in rows]
        fits = [(unit, n, x) for n, (unit, x) in enumerate(priced)
                if unit is not None and unit <= cap and x["buyoutPrice"] <= afford]
        return min(fits)[2] if fits else None
