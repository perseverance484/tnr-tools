"""Automatic restock of battle consumables (director 2026-11-11: "restock all items automatically from item shop,
inventory, home storage and auction house").

Pure planning; pilot.py sends the calls. One pass = read my items (+ money/bank, + an auction search for one missing
non-shop item) -> plan -> act -> read again, until nothing is missing (at most 4 passes), then every 15 minutes and
after any battle where the game refused an item.

Per tracked item, in this order:
  1. carried but not equipped while no stack of it is equipped -> equip it in the slot it used to have;
  2. stored at home -> take it out (home.toggleStoreItem), then 1;
  3. sold in the item shop (catalog inShop, ryo price, no reputation cost) -> item.buy up to the target;
  4. otherwise the auction house: a MONEY listing (never reputation) with a buyout at or under the cap -> buyout bid.
Spending guards: a ryo reserve that is never spent, a daily cap, per-unit price caps for auctions.
"""
import time

# item id -> (short name, keep at least, refill to, auction price cap per unit in ryo)
TRACK = {
    "6DnJn4x6LWWXtBu7UZybb": ("kims", 3, 6, 150_000),
    "TtYPd-LcXKeK3sMuhq1TP": ("smoke", 3, 6, 50_000),
    "rsc2uO5QuffXzejfhwF_F": ("panacea", 3, 6, 55_000),
    "tZTvqYWiAc_OrY64nDvIo": ("pill", 5, 15, 1_000),
    "yVNeLzxHSFkNpTPnlm7yQ": ("kunai", 10, 30, 3_000),
}
FULL_POTION_KEEP = (5, 15, 20_000)
RESERVE = 500_000          # ryo never spent by restock
DAILY_CAP = 3_000_000      # ryo restock may spend per UTC day
EVERY = 900
ITEM_SEL = ["*.id", "*.itemId", "*.quantity", "*.equipped", "*.storedAtHome", "*.durability"]
REPAIR_BELOW = 0.6         # repair when any equipped item is under this share of its max durability
AUCTION_SEL = ["data.*.id", "data.*.currencyType", "data.*.buyoutPrice", "data.*.quantity",
               "data.*.userItem.itemId", "data.*.userItem.quantity", "data.*.listingType", "data.*.sellerId"]


def rows(items):
    keys = ["id", "itemId", "quantity", "equipped", "storedAtHome", "durability"]
    n = len(items.get("*.id") or [])
    cols = [items.get(f"*.{k}") or [None] * n for k in keys]
    return [dict(zip(keys, r)) for r in zip(*cols)]


def tracked(st):
    t = dict(TRACK)
    fp = st.get("full_potion_item")
    if fp:
        t[fp] = ("fullpotion",) + FULL_POTION_KEEP
    return t


def spent_today(st):
    day = time.strftime("%Y-%m-%d", time.gmtime())
    rec = st.setdefault("restock_spend", {})
    if rec.get("day") != day:
        rec.clear(); rec["day"] = day; rec["ryo"] = 0
    return rec


def plan(st, items, user, records, listings=None, home_village=None, full_potion_uid=None):
    """-> (calls, notes, auction_query): calls are (endpoint, input, select) tuples."""
    rs = rows(items or {})
    if full_potion_uid:
        fp = next((r for r in rs if r["id"] == full_potion_uid), None)
        if fp:
            st["full_potion_item"] = fp["itemId"]
    for r in rs:                                           # remember each item's slot while it is equipped
        if r["equipped"] and r["equipped"] != "NONE":
            st.setdefault("item_slots", {})[r["itemId"]] = r["equipped"]
    # durability (director 2026-11-11: "Items are broken again ... Are durability checks not happening"): any equipped
    # item worn under 60% of its max is repaired, with repair kits first (item.useRepairAll), then ryo
    # (item.repairAll, which needs the Crafting occupation); whichever the game refuses, the other is tried next pass
    worn = []
    for r in rs:
        if r["equipped"] in (None, "NONE") or r["storedAtHome"]:
            continue
        mx = (records.get(r["itemId"]) or {}).get("maxDurability") or 0
        if mx and r.get("durability") is not None and r["durability"] < REPAIR_BELOW * mx:
            worn.append(f"{(records.get(r['itemId']) or {}).get('name', r['itemId'])} {r['durability']}/{mx}")
    repair_calls = []
    if worn:
        tried = st.setdefault("repair_tried", {})
        how = "item.useRepairAll" if time.time() - tried.get("item.useRepairAll", 0) > 600 else "item.repairAll"
        if time.time() - tried.get(how, 0) > 600:
            tried[how] = time.time()
            repair_calls.append((how, {}, ["success", "message"]))
        st["worn"] = worn
    else:
        st["worn"] = []
    money = float(user.get("userData.money") or 0)
    bank = float(user.get("userData.bank") or 0)
    spend = spent_today(st)
    calls, notes, query = list(repair_calls), ([f"repair ({repair_calls[0][0].split('.')[-1]}): " + ", ".join(worn)]
                                                if repair_calls else [f"worn: {', '.join(worn)} (repair tried)"] if worn else []), None
    st["empty_items"] = []                              # battle items I carry none of: the planners leave them out
    for iid, (name, keep, fill, cap) in tracked(st).items():
        mine = [r for r in rs if r["itemId"] == iid and (r["quantity"] or 0) > 0]
        carried = [r for r in mine if not r["storedAtHome"]]
        if not carried and iid in TRACK:
            st["empty_items"].append(iid)
        home = [r for r in mine if r["storedAtHome"]]
        equipped = [r for r in carried if r["equipped"] and r["equipped"] != "NONE"]
        slot = st.get("item_slots", {}).get(iid)
        if iid == st.get("full_potion_item") and carried:
            st["full_potion_uid"] = carried[0]["id"]       # Full Potion is consumed by user-item id: keep it current
        if not equipped and slot and iid != st.get("full_potion_item"):
            spare = [r for r in carried if r["equipped"] in (None, "NONE")]
            if spare:
                calls.append(("item.toggleEquip", {"userItemId": spare[0]["id"], "slot": slot}, ["success", "message"]))
                notes.append(f"equip {name} -> {slot}")
                continue
        have = sum(r["quantity"] for r in carried)
        if have >= keep:
            continue
        if home:
            for r in home:
                calls.append(("home.toggleStoreItem", {"userItemId": r["id"]}, ["success", "message"]))
            notes.append(f"{name}: take {sum(r['quantity'] for r in home)} out of home storage")
            continue
        rec = records.get(iid) or {}
        want = fill - have
        if rec.get("inShop") and not rec.get("repsCost") and not rec.get("seichiSilverCost"):
            unit = float(rec.get("cost") or 0)
            n = int(min(want, max(0, (money - RESERVE) // max(1, unit)),
                        max(0, (DAILY_CAP - spend["ryo"]) // max(1, unit)), rec.get("stackSize") or 50, 50))
            if n > 0:
                calls.append(("item.buy", {"itemId": iid, "stack": n, "villageId": home_village},
                              ["success", "message"]))
                spend["ryo"] += n * unit
                notes.append(f"{name}: buy {n} in the shop (~{n * unit:,.0f} ryo)")
            else:
                notes.append(f"{name}: short ({have}/{keep}) but ryo reserve / daily cap reached")
            continue
        # not in the shop: the auction house, MONEY listings with a buyout under the cap
        if listings is not None and listings.get("_item") == iid:
            best = None
            ids = listings.get("data.*.id") or []
            for k in range(len(ids)):
                g = lambda f: (listings.get(f"data.*.{f}") or [None] * len(ids))[k]
                if g("currencyType") != "MONEY" or not g("buyoutPrice") or g("userItem.itemId") != iid:
                    continue
                qty = g("quantity") or g("userItem.quantity") or 1
                unit = g("buyoutPrice") / max(1, qty)
                if unit <= cap and g("buyoutPrice") <= bank - RESERVE and spend["ryo"] + g("buyoutPrice") <= DAILY_CAP:
                    if best is None or unit < best[0]:
                        best = (unit, ids[k], g("buyoutPrice"), qty)
            if best:
                calls.append(("auction.placeBid", {"auctionId": best[1], "amount": int(best[2])},
                              ["success", "message"]))
                spend["ryo"] += best[2]
                notes.append(f"{name}: auction buyout {best[3]} for {best[2]:,.0f} ryo")
            else:
                notes.append(f"{name}: short ({have}/{keep}), no auction listing under {cap:,} ryo each")
                st.setdefault("auction_none", {})[iid] = time.time()
            continue
        if query is None and time.time() - st.get("auction_none", {}).get(iid, 0) > 3600:
            query = (iid, rec.get("name") or name)
            notes.append(f"{name}: short ({have}/{keep}), searching the auction house")
    return calls, notes, query
