"""AP2, the upkeep activities (brief AP2; design 4.3): restock and repair here; training, equipment, bank and
session in their own classes below. Each rule of the pilot's restock.py that was ported has its test.
"""
import json
import os
import unittest

from player import calls as K, config as C
from player.activities import bank, equipment, repair, restock, training
from unittest import mock

from player.tests.support import Rig, my_items, res, user
from player.world import RATE_LIMITED, utc_day

KIMS, SMOKE, PANACEA, PILL, KUNAI, KIT = list(restock.TRACK)
POTION = "fullpotion_item"
STOCKED = [("u1", KIMS, 6, "ITEM_1", False, None), ("u2", SMOKE, 6, "ITEM_2", False, None),
           ("u3", PANACEA, 6, "ITEM_3", False, None), ("u4", PILL, 15, "ITEM_4", False, None),
           ("u5", KUNAI, 30, "THROWN", False, None), ("u6", KIT, 20, "NONE", False, None),
           (C.FULL_POTION, POTION, 15, "NONE", False, None)]


def stock(**changes):
    """A read of my items with everything in stock, but for the rows named: item id -> a row's tail, or None
    for an item that is not there at all."""
    rows = []
    for row in STOCKED:
        change = changes.get(row[1], row[2:])
        if change is not None:
            rows.append(row[:2] + tuple(change))
    return my_items(*rows + list(changes.get("more", [])))


def rich(**more):
    return user(**{"money": 10_000_000, "bank": 900_000_000, **more})


class Upkeep(unittest.TestCase):
    def rig(self):
        rig = Rig(upkeep=True)
        rig.world["control"]["activities"] = {"training": False, "equipment": False, "bank": False}
        return rig

    def passes(self, rig, *results, **tick):
        """One tick with these results; the batch's calls."""
        return rig.calls(rig.tick(*results, **tick))


class Restock(Upkeep):
    def test_a_pass_reads_my_items_first_and_rests_when_nothing_is_short(self):
        rig = self.rig()
        self.assertEqual(self.passes(rig, rich()), ["item.getUserItems", "profile.getUser"])
        out = rig.tick(stock(), rich())
        self.assertEqual(out["activity"], "pvp_hunt")                       # nothing short: the hunt goes on
        self.assertEqual((rig.world["inventory"]["empty_items"], rig.world.own("restock")["active"]), ([], False))
        rig.t += restock.EVERY - 5
        self.assertNotEqual(rig.tick(rich())["activity"], "restock")
        rig.t += 10
        self.assertEqual(rig.tick(rich())["activity"], "restock")           # and again a quarter of an hour on

    def test_what_the_shop_sells_for_ryo_is_bought_up_to_the_target(self):
        rig = self.rig()
        rig.tick(rich())
        out = rig.tick(stock(**{PANACEA: (2, "ITEM_3", False, None), PILL: None}), rich())
        buys = [s for s in out["steps"] if s.get("call") == "item.buy"]
        self.assertEqual([(s["input"]["itemId"], s["input"]["stack"]) for s in buys], [(PANACEA, 4), (PILL, 15)])
        self.assertEqual(buys[0]["input"]["villageId"], C.HOME_VILLAGE)
        self.assertEqual(rig.calls(out)[-2:], ["item.getUserItems", "profile.getUser"])   # and it looks again
        self.assertEqual(rig.world["inventory"]["empty_items"], [PILL])     # the planners leave that one out
        rig.tick(res("item.buy", {"success": True}, buys[0]["input"]), stock(), rich())
        self.assertIn("bought 4 Panacea (220,000 ryo)", rig.events("item")[-1]["text"])

    def test_the_pocket_the_reserve_and_the_days_cap_bound_what_is_bought(self):
        """A Panacea costs 55,000. The pocket pays; the reserve is what pocket and bank keep between them."""
        for pocket, bank_, spent, n in ((120_000, 900_000_000, 0, 2),                # what the pocket can pay
                                        (300_000, C.RESERVE - 180_000, 0, 2),      # 120,000 above the reserve
                                        (300_000, C.RESERVE - 299_990, 0, 0),      # 10 above it
                                        (10_000_000, 900_000_000, C.DAILY_CAP - 60_000, 1)):
            rig = self.rig()
            rig.tick(user(money=pocket, bank=bank_))
            rig.world["records"]["spend"] = {"day": utc_day(rig.t + 1), "ryo": float(spent)}
            out = rig.tick(stock(**{PANACEA: (0, "ITEM_3", False, None)}), user(money=pocket, bank=bank_))
            buys = [s["input"]["stack"] for s in out["steps"] if s.get("call") == "item.buy"]
            self.assertEqual(buys, [n] if n else [], (pocket, bank_, spent))
            self.assertNotIn("draw", rig.world["inventory"])                # and the bank is not asked for more

    def test_one_pass_spends_what_is_in_the_pocket_once(self):
        rig = self.rig()
        pocket = user(money=200_000, bank=900_000_000)
        rig.tick(pocket)
        out = rig.tick(stock(**{PANACEA: (0, "ITEM_3", False, None), PILL: None}), pocket)
        buys = [(s["input"]["itemId"], s["input"]["stack"]) for s in out["steps"] if s.get("call") == "item.buy"]
        self.assertEqual(buys, [(PANACEA, 3), (PILL, 15)])                  # 165,000, then 15,000 of the 35,000 left
        self.assertEqual(rig.world.own("restock")["purse"], 20_000)

    def test_a_pocket_that_cannot_pay_for_one_asks_the_bank_and_buys_when_it_has(self):
        rig = self.rig()
        rig.world["control"]["activities"] = {"training": False, "equipment": False}   # the bank is on
        poor = user(money=30_000, bank=900_000_000)
        rig.tick(poor)
        out = rig.tick(stock(**{PANACEA: (0, "ITEM_3", False, None)}), poor)
        self.assertNotIn("item.buy", rig.calls(out))
        self.assertEqual(rig.world["inventory"]["draw"]["ryo"], C.POCKET_LIMIT)   # six cost 330,000: the limit holds
        out = rig.tick(poor)                                                # the bank's turn comes with the next tick
        self.assertEqual((out["activity"], out["steps"][0]), ("bank", K.to_pocket(C.POCKET_LIMIT - 30_000)))
        filled = user(money=C.POCKET_LIMIT, bank=900_000_000 - 170_000)
        out = rig.tick(res("bank.toPocket", {"success": True}, out["steps"][0]["input"]), filled)
        self.assertEqual(rig.calls(out), ["item.getUserItems", "profile.getUser"])   # restock looks again at once
        out = rig.tick(stock(**{PANACEA: (0, "ITEM_3", False, None)}), filled)
        self.assertEqual([s["input"]["stack"] for s in out["steps"] if s.get("call") == "item.buy"], [3])
        self.assertNotIn("draw", rig.world["inventory"])

    def test_a_purchase_the_caps_do_not_allow_is_asked_first(self):
        rig = self.rig()
        rig.world["control"]["spend_caps"] = {"daily": 100_000}
        rig.tick(rich())
        rig.world["control"]["spend_caps"] = {}                             # the plan was sized under the old cap
        out = rig.tick(stock(**{KIMS: (0, "ITEM_1", False, None)}), rich(money=700_000, bank=0))
        self.assertNotIn("item.buy", rig.calls(out))                        # one would cut into the reserve
        rig = self.rig()
        rig.tick(rich())
        step = K.buy(KIMS, 6, 900_000)
        rig.world["control"]["spend_caps"] = {"daily": 500_000}
        ok, verdict, _ = rig.brain.gates.screen([step], rig.world, "restock")
        self.assertEqual((ok, verdict.kind, len(rig.world["decisions"])), (False, "ask", 1))

    def test_what_is_stored_at_home_is_taken_out_before_anything_is_bought(self):
        rig = self.rig()
        rig.tick(rich())
        out = rig.tick(stock(**{SMOKE: (1, "ITEM_2", False, None), "more": [("h1", SMOKE, 9, "NONE", True, None)]}), rich())
        self.assertEqual([(s["call"], s["input"]) for s in out["steps"][:1]], [("home.toggleStoreItem", {"userItemId": "h1"})])
        self.assertNotIn("item.buy", rig.calls(out))

    def test_a_carried_stack_goes_back_into_the_slot_it_had(self):
        rig = self.rig()
        rig.tick(rich())
        rig.tick(stock(), rich())                                           # the slots are remembered from this read
        rig.t += restock.EVERY + 1
        rig.tick(rich())
        out = rig.tick(stock(**{SMOKE: (6, "NONE", False, None)}), rich())
        self.assertEqual(out["steps"][0], K.equip("u2", "ITEM_2"))

    def test_what_the_shop_does_not_sell_is_looked_for_at_auction_under_its_cap(self):
        rig = self.rig()
        rig.tick(rich())
        out = rig.tick(stock(**{KIT: (2, "NONE", False, None)}), rich())
        (ask,) = [s for s in out["steps"] if s.get("call") == "auction.getAuctionListings"]
        self.assertEqual(ask["input"], {"itemName": "Repair Kit", "limit": 20, "listingType": "AUCTION"})
        listed = res("auction.getAuctionListings", {
            "data.*.id": ["a1", "a2", "a3", "a4"], "data.*.currencyType": ["MONEY", "REPUTATION", "MONEY", "MONEY"],
            "data.*.buyoutPrice": [450_000, 10, 2_000_000, 300_000], "data.*.quantity": [10, 10, 10, 10],
            "data.*.userItem.itemId": [KIT, KIT, KIT, PILL], "data.*.userItem.quantity": [10, 10, 10, 10]})
        out = rig.tick(listed, stock(**{KIT: (2, "NONE", False, None)}), rich())
        (bid,) = [s for s in out["steps"] if s.get("call") == "auction.placeBid"]
        self.assertEqual(bid["input"], {"auctionId": "a1", "amount": 450_000})   # in ryo, this item, 45,000 each
        self.assertEqual(bid["meta"], {"ryo": 450_000.0, "currency": "MONEY"})

    def test_with_no_listing_under_the_cap_the_auction_house_is_left_alone_for_an_hour(self):
        rig = self.rig()
        rig.tick(rich())
        short = stock(**{KIT: (2, "NONE", False, None)})
        rig.tick(short, rich())
        dear = res("auction.getAuctionListings", {"data.*.id": ["a3"], "data.*.currencyType": ["MONEY"],
                                                  "data.*.buyoutPrice": [2_000_000], "data.*.quantity": [10],
                                                  "data.*.userItem.itemId": [KIT], "data.*.userItem.quantity": [10]})
        self.assertNotEqual(rig.tick(dear, short, rich())["activity"], "restock")
        rig.t += restock.EVERY + 1
        rig.tick(rich())
        self.assertNotIn("auction.getAuctionListings", self.passes(rig, short, rich()))
        rig.t += restock.AUCTION_RETRY
        rig.tick(rich())
        self.assertIn("auction.getAuctionListings", self.passes(rig, short, rich()))

    def test_nothing_that_costs_more_than_ryo_counts_as_sold_for_ryo(self):
        self.assertTrue(restock.for_ryo({"inShop": True, "cost": 5, "repsCost": 0, "seichiSilverCost": 0}))
        for rec in ({"inShop": True, "repsCost": 5}, {"inShop": True, "seichiSilverCost": 1}, {"inShop": False}, {}):
            self.assertFalse(restock.for_ryo(rec), rec)
        rig = self.rig()                                                    # and what the shop sells for more
        rig.tick(rich())                                                    # than ryo is never bought there
        rig.combat.item_record = lambda item_id: {"name": "Panacea", "inShop": True, "cost": 10, "repsCost": 5}
        calls = self.passes(rig, stock(**{PANACEA: (0, "ITEM_3", False, None)}), rich())
        self.assertEqual(("item.buy" in calls, "auction.getAuctionListings" in calls), (False, True))

    def test_a_shop_that_keeps_saying_no_ends_the_pass_after_four_tries(self):
        rig = self.rig()
        rig.tick(rich())
        short, tries = stock(**{PANACEA: (0, "ITEM_3", False, None)}), 0
        out = rig.tick(short, rich())
        while "item.buy" in rig.calls(out) and tries < 10:
            tries += 1
            (buy,) = [s for s in out["steps"] if s.get("call") == "item.buy"]
            out = rig.tick(res("item.buy", {"success": False, "message": "Not enough money"}, buy["input"]), short, rich())
        self.assertEqual(tries, restock.PASSES)
        self.assertEqual(len([e for e in rig.events("finding") if "Not enough money" in e["text"]]), restock.PASSES)
        self.assertEqual(rig.events("item"), [])                            # nothing is said to be bought

    def test_a_read_of_my_items_that_does_not_line_up_is_not_acted_on(self):
        rig = self.rig()
        rig.tick(rich())
        bad = res("item.getUserItems", {"*.id": ["u1", "u2"], "*.itemId": [KIMS], "*.quantity": [0, 0]})
        for _ in range(restock.READ_TRIES - 1):                             # (the first read is the one above)
            self.assertEqual(self.passes(rig, bad, rich()), ["item.getUserItems", "profile.getUser"])
        self.assertNotEqual(rig.tick(bad, rich())["activity"], "restock")   # given up until the next time
        self.assertNotIn("items", rig.world["inventory"])
        self.assertTrue(any("do not line up" in e["text"] for e in rig.events("finding")))

    def test_the_full_potion_is_known_by_the_stack_that_is_carried(self):
        rig = self.rig()
        rig.tick(rich())
        rig.tick(stock(), rich())
        self.assertEqual(rig.world["inventory"]["full_potion_item"], POTION)
        rig.t += restock.EVERY + 1
        rig.tick(rich())
        rig.tick(stock(**{POTION: None, "more": [("new_stack", POTION, 15, "NONE", False, None)]}), rich())
        self.assertEqual(rig.world["inventory"]["full_potion_uid"], "new_stack")
        self.assertEqual(rig.brain.reg.activities["recovery"]._potion(rig.world)["input"]["userItemId"], "new_stack")

    def test_a_fight_calls_for_a_pass_and_a_fight_that_starts_takes_the_tick(self):
        rig = self.rig()
        rig.tick(rich())
        rig.tick(stock(), rich())
        rig.world["inventory"]["restock_due"] = True                        # what the battle activity leaves behind
        self.assertEqual(self.passes(rig, rich()), ["item.getUserItems", "profile.getUser"])
        out = rig.tick(stock(**{PANACEA: (0, "ITEM_3", False, None)}), user("BATTLE", bid="B1", money=10_000_000))
        self.assertEqual((out["activity"], "item.buy" in rig.calls(out)), ("battle", False))


class Repair(Upkeep):
    WORN = ("g1", "armour_id", 1, "CHEST", False, 90)                       # 90 of 400: under a quarter

    def test_an_equipped_item_under_a_quarter_is_repaired_with_kits_first(self):
        rig = self.rig()
        rig.tick(rich())
        out = rig.tick(stock(more=[self.WORN]), rich())
        self.assertEqual((out["activity"], rig.calls(out)), ("repair", ["item.useRepairAll", "item.getUserItems"]))
        out = rig.tick(res("item.useRepairAll", {"success": True}), stock(more=[("g1", "armour_id", 1, "CHEST", False, 400)]),
                       rich())
        self.assertNotEqual(out["activity"], "repair")
        self.assertEqual(rig.events("repair")[-1]["text"], "repaired Kaeruun Armor 90/400 with Repair Kits")

    def test_when_the_kits_are_refused_ryo_is_tried_and_neither_twice_in_ten_minutes(self):
        rig = self.rig()
        rig.tick(rich())
        worn = stock(more=[self.WORN])
        rig.tick(worn, rich())
        out = rig.tick(res("item.useRepairAll", {"success": False, "message": "No repair kits"}), worn, rich())
        self.assertEqual(rig.calls(out)[0], "item.repairAll")
        out = rig.tick(res("item.repairAll", {"success": False, "message": "Crafting only"}), worn, rich())
        self.assertNotEqual(out["activity"], "repair")
        self.assertEqual(len([e for e in rig.events("finding") if e.get("about") == "repair"]), 2)
        rig.t += repair.RETRY + 1
        self.assertEqual(rig.tick(rich())["activity"], "repair")

    def test_worn_is_fine_and_what_is_not_equipped_is_left(self):
        rig = self.rig()
        rig.tick(rich())
        rows = [("g1", "armour_id", 1, "CHEST", False, 110), ("g2", "armour_id", 1, "NONE", False, 5),
                ("g3", "armour_id", 1, "CHEST", True, 5), ("g4", "armour_id", 1, "LEGS", False, None)]
        self.assertNotEqual(rig.tick(stock(more=rows), rich())["activity"], "repair")
        self.assertEqual(rig.brain.reg.activities["repair"].worn(rig.world), [])


T = training.TARGETS


def queue(waiting=(), capacity=4):
    return res("jutsu.getTrainingQueue", {"capacity": capacity, "waiting.*.jutsuId": [j for j, _ in waiting],
                                          "waiting.*.level": [n for _, n in waiting]})


def jutsu(levels, active=()):
    return res("jutsu.getUserJutsus", {"*.jutsuId": list(levels), "*.level": list(levels.values()),
                                       "*.finishTraining": ["2026-11-12T10:00:00Z" if j in active else None for j in levels]})


class Training(Upkeep):
    def rig(self):
        rig = Rig(upkeep=True)
        rig.world["control"]["activities"] = {"restock": False, "equipment": False, "bank": False}
        return rig

    def trained(self, out):
        return [s["input"]["jutsuId"] for s in out["steps"] if s.get("call") == "jutsu.startTraining"]

    def test_the_queue_is_read_and_every_free_place_goes_to_the_lowest_next_level(self):
        rig = self.rig()
        self.assertEqual(self.passes(rig, rich()), ["jutsu.getTrainingQueue", "jutsu.getUserJutsus", "profile.getUser"])
        levels = {T[0]: 9, T[1]: 3, T[2]: 3, T[3]: 12}
        out = rig.tick(queue([(T[1], 4)]), jutsu(levels, active=[T[0]]), rich())
        # T[0] is training to 10, T[1] waits for 4: three places are free. The unowned targets are at 0, the
        # lowest; among equals the director's order decides.
        self.assertEqual(self.trained(out), [T[4], T[5], T[6]])
        self.assertTrue(all(s["input"]["levels"] == 1 for s in out["steps"] if s.get("call") == "jutsu.startTraining"))
        out = rig.tick(res("jutsu.startTraining", {"success": True}, {"jutsuId": T[4], "levels": 1}), rich())
        self.assertNotEqual(out["activity"], "training")                    # nothing more until the next look
        rig.t += training.LOOK + 1
        self.assertEqual(rig.tick(rich())["activity"], "training")

    def test_with_nothing_training_one_more_place_is_free_and_the_cap_ends_a_target(self):
        rig = self.rig()
        rig.tick(rich())
        levels = dict.fromkeys(T, training.CAP)
        levels.update({T[7]: 19, T[9]: 18})
        out = rig.tick(queue(), jutsu(levels), rich())
        self.assertEqual(self.trained(out), [T[9], T[7], T[9]])             # 18 to 19, 19 to 20, 19 to 20: then none
        rig = self.rig()
        rig.tick(rich())
        self.assertEqual(self.trained(rig.tick(queue([(T[0], 2)] * 4), jutsu({T[0]: 1}, active=[T[0]]), rich())), [])

    def test_a_refused_target_is_left_alone_a_day_or_ten_minutes_when_it_is_the_moment(self):
        for said, wait in (("Jutsu not for you", training.REFUSED_FOR), ("You are traveling", training.SOON),
                           ("Not enough money", training.SOON)):
            rig = self.rig()
            rig.tick(rich())
            levels = dict.fromkeys(T, training.CAP)
            levels[T[2]] = 5
            rig.tick(queue(), jutsu(levels), rich())
            rig.tick(res("jutsu.startTraining", {"success": False, "message": said}, {"jutsuId": T[2], "levels": 1}), rich())
            rig.t += training.LOOK + 1
            rig.tick(rich())
            self.assertEqual(self.trained(rig.tick(queue(), jutsu(levels), rich())), [] if wait > training.LOOK else [T[2]] * 5)
            self.assertIn(said, rig.events("finding")[-1]["text"])

    def test_a_fill_waits_for_the_bank_to_fill_the_pocket_and_the_rest_goes_back(self):
        rig = self.rig()
        rig.world["control"]["activities"] = {"restock": False, "equipment": False}   # the bank is on
        road = dict(money=150_000, bank=900_000_000)                        # what is carried on the road
        self.assertEqual(self.passes(rig, user(**road))[0], "jutsu.getTrainingQueue")
        out = rig.tick(queue(), jutsu({T[0]: 3}), user(**road))
        self.assertEqual(self.trained(out), [])                             # not paid out of the 150,000:
        self.assertEqual((out["activity"], out["steps"][0]), ("bank", K.to_pocket(C.TRAINING_DRAW - 150_000)))
        drawn = dict(money=C.TRAINING_DRAW, bank=900_000_000 - C.TRAINING_DRAW + 150_000)
        out = rig.tick(res("bank.toPocket", {"success": True}, out["steps"][0]["input"]), user(**drawn))
        self.assertEqual(len(self.trained(out)), 5)                         # the fill, with ten million in hand
        self.assertNotIn("draw_until", rig.world["training"])
        left = dict(drawn, money=9_400_000)
        out = rig.tick(*[res("jutsu.startTraining", {"success": True}, s["input"]) for s in out["steps"][:5]], user(**left))
        self.assertEqual((out["activity"], out["steps"][0]), ("bank", K.to_bank(9_400_000 - bank.KEEP)))

    def test_with_no_bank_to_draw_on_the_fill_goes_ahead(self):
        for bank_, waits in ((900_000_000, True), (C.RESERVE, False)):      # (the bank activity is off here)
            rig = self.rig()
            road = user(money=150_000, bank=bank_)
            rig.tick(road)
            out = rig.tick(queue(), jutsu({T[0]: 3}), road)
            self.assertEqual(bool(self.trained(out)), not waits, bank_)     # nothing to add: it goes ahead at once
            if waits:
                rig.t += training.DRAW_FOR + 1                              # nobody filled the pocket: it goes ahead
                self.assertEqual(len(self.trained(rig.tick(road))), 5)

    def test_energy_is_trained_in_the_village_on_the_stat_that_trails(self):
        for stats, stat in (({"intelligence": 900, "willpower": 1000}, "intelligence"),
                            ({"intelligence": 1000, "willpower": 1000}, "willpower")):
            rig = self.rig()
            rig.world.own("training")["next"] = rig.t + 9999                # (the queue was just looked at)
            home = rich(sector=C.HOME_SECTOR, curEnergy=450, **stats)
            out = rig.tick(home)
            self.assertEqual(out["steps"][0], K.train_stat(stat, 450))
            out = rig.tick(res("train.startTraining", {"success": True}, out["steps"][0]["input"]),
                           rich(sector=C.HOME_SECTOR, curEnergy=0, **stats))
            self.assertNotEqual(out["activity"], "training")
        rig = self.rig()
        rig.world.own("training")["next"] = rig.t + 9999
        self.assertNotEqual(rig.tick(rich(sector=C.HOME_SECTOR, curEnergy=training.ENERGY_MIN - 1))["activity"], "training")

    def test_a_lot_of_energy_elsewhere_is_worth_the_trip_and_a_refusal_ends_it_for_an_hour(self):
        rig = self.rig()
        rig.world.own("training")["next"] = rig.t + 99999
        road = {"money": 150_000}                                           # (within what the pocket may hold)
        self.assertNotEqual(rig.tick(rich(curEnergy=training.TRIP - 1, **road))["activity"], "training")
        out = rig.tick(rich(curEnergy=training.TRIP, **road))
        self.assertEqual((out["activity"], out["steps"][0]["input"]), ("training", {"sector": C.HOME_SECTOR}))
        self.assertNotEqual(rig.tick(rich(curEnergy=training.TRIP, **road))["activity"], "training")   # not a second trip
        home = rich(sector=C.HOME_SECTOR, curEnergy=training.TRIP)
        out = rig.tick(home)
        self.assertEqual(out["steps"][0]["call"], "train.startTraining")
        out = rig.tick(res("train.startTraining", {"success": False, "message": "Wrong sector"}, out["steps"][0]["input"]), home)
        self.assertNotEqual(out["activity"], "training")
        rig.t += training.ENERGY_BLOCK + 1
        self.assertEqual(rig.tick(home)["steps"][0]["call"], "train.startTraining")

    def test_unspent_experience_levels_intelligence_and_willpower_and_then_goes_to_both(self):
        """ryo_plan.md: "Put it into intelligence until it matches willpower, then split." """
        for stats, exp, points in (
                ({"intelligence": 900, "willpower": 1000}, 7054, {"intelligence": 3577, "willpower": 3477}),
                ({"intelligence": 5000, "willpower": 1000}, 3000, {"willpower": 3000}),   # the one that trails, first
                ({"intelligence": 1000, "willpower": 1000}, 1001, {"intelligence": 501, "willpower": 500})):
            rig = self.rig()
            rig.world.own("training")["next"] = rig.t + 9999                # (the queue was just looked at)
            out = rig.tick(rich(earnedExperience=exp, **stats))
            self.assertEqual((out["activity"], out["steps"][0]), ("training", K.spend_experience(points)), exp)
            sent = out["steps"][0]["input"]
            self.assertEqual((sorted(sent), sum(sent.values())), (sorted(K.STATS), exp))   # every field; all of it
        self.assertIn("userData.earnedExperience", K.user()["select"])     # and the profile read asks for it
        rig = self.rig()
        rig.world.own("training")["next"] = rig.t + 9999
        little = rich(earnedExperience=training.EXP_MIN - 1, intelligence=1, willpower=2)
        self.assertNotEqual(rig.tick(little)["activity"], "training")       # not worth a call yet

    def test_experience_is_not_assigned_twice_in_ten_minutes_and_a_refusal_stops_it_for_an_hour(self):
        rig = self.rig()
        rig.world.own("training")["next"] = rig.t + 99999
        me = rich(earnedExperience=5000, intelligence=1000, willpower=1000)
        out = rig.tick(me)
        yes = res("profile.useUnusedExperiencePoints", {"success": True}, out["steps"][0]["input"])
        self.assertNotEqual(rig.tick(yes, me)["activity"], "training")      # (a profile that still shows it)
        done = [e["text"] for e in rig.events("activity_done")]
        self.assertEqual(done, ["training: experience assigned (2,500 to intelligence, 2,500 to willpower)",
                                "training: 2,500 experience to intelligence, 2,500 experience to willpower"])
        rig.t += training.SOON + 1
        out = rig.tick(me)
        self.assertEqual(out["activity"], "training")                       # ten minutes on, when it is still there
        no = res("profile.useUnusedExperiencePoints", {"success": False, "message": "No"}, out["steps"][0]["input"])
        rig.tick(no, me)
        self.assertIn("the experience was refused (No)", rig.events("finding")[-1]["text"])
        rig.t += training.SOON + 1
        self.assertNotEqual(rig.tick(me)["activity"], "training")
        rig.t += training.ENERGY_BLOCK
        self.assertEqual(rig.tick(me)["activity"], "training")

    def test_a_queue_read_that_cannot_be_used_is_read_again_later(self):
        rig = self.rig()
        rig.tick(rich())
        bad = res("jutsu.getUserJutsus", {"*.jutsuId": [T[0], T[1]], "*.level": [3]})
        self.assertEqual(self.trained(rig.tick(queue(), bad, rich())), [])
        self.assertNotIn("levels", rig.world["training"])
        rig.t += training.SOON + 1
        self.assertEqual(self.passes(rig, rich())[0], "jutsu.getTrainingQueue")


class Equipment(Upkeep):
    BACKUP = equipment.BACKUP_THROWN[0]

    def rig(self, mode="guard"):
        rig = Rig(mode=mode, upkeep=True)
        rig.world["control"]["activities"] = {"training": False, "bank": False}
        return rig

    def test_what_is_equipped_is_written_where_the_planners_look(self):
        rig = self.rig()
        rig.tick(rich())
        rig.tick(stock(), rich())
        with open(os.path.join(rig.combat.live, "equipped.json"), encoding="utf8") as f:
            slots = json.load(f)
        self.assertEqual((slots["THROWN"], slots["ITEM_1"], rig.combat.used["equipped"]), (KUNAI, KIMS, 1))
        self.assertFalse(rig.world["inventory"]["backup_thrown"])

    def test_an_empty_thrown_slot_takes_the_backup_and_restock_stops_buying_the_kunai(self):
        rig = self.rig()
        rig.tick(rich())
        spent = stock(**{KUNAI: None, "more": [("b1", self.BACKUP, 50, "NONE", False, None)]})
        out = rig.tick(spent, rich())
        swaps = [s for s in out["steps"] if s.get("call") == "item.toggleEquip"]
        while not swaps and out["activity"] in ("restock", "equipment"):
            out = rig.tick(spent, rich())
            swaps = [s for s in out["steps"] if s.get("call") == "item.toggleEquip"]
        self.assertEqual(swaps, [K.equip("b1", "THROWN")])
        self.assertNotIn("auction.getAuctionListings", [c for e in rig.events() for c in [e.get("call")] if c])
        self.assertTrue(rig.world["inventory"]["backup_thrown"])
        self.assertEqual(rig.brain.reg.activities["restock"]._one(rig.world, KUNAI, "kunai", 10, 30, 3000), ([], None))

    def test_the_pvp_1_loadouts_are_selected_once_for_the_hunt_and_not_on_guard(self):
        rig = self.rig()
        rig.world["control"]["activities"]["restock"] = False
        self.assertNotEqual(rig.tick(rich())["activity"], "equipment")      # on guard: nothing is selected
        rig = self.rig(mode="hunt")
        rig.world["control"]["activities"]["restock"] = False
        out = rig.tick(rich())
        self.assertEqual(out["steps"][:2], K.loadouts(*equipment.PVP1))
        self.assertEqual(out["steps"][2], K.items())                        # what the selection equipped is read
        answers = [res(s["call"], {"success": True}, s["input"]) for s in out["steps"][:2]]
        self.assertNotEqual(rig.tick(*answers, stock(), rich())["activity"], "equipment")
        self.assertEqual(rig.world.own("equipment")["selected"], list(equipment.PVP1))
        rig.t += 3 * equipment.RETRY
        self.assertNotEqual(rig.tick(rich())["activity"], "equipment")      # selected, and remembered

    def test_a_refused_selection_is_said_and_tried_again_later(self):
        rig = self.rig(mode="hunt")
        rig.world["control"]["activities"]["restock"] = False
        out = rig.tick(rich())
        no = res(out["steps"][0]["call"], {"success": False, "message": "In a pyramid"}, out["steps"][0]["input"])
        self.assertNotEqual(rig.tick(no, stock(), rich())["activity"], "equipment")
        self.assertIn("In a pyramid", rig.events("finding")[-1]["text"])
        rig.t += equipment.RETRY + 1
        self.assertEqual(rig.tick(rich())["activity"], "equipment")

    def test_one_loadout_answered_is_not_both_selected(self):
        """The jutsu loadout's yes came back, the item loadout's answer did not (or it said no)."""
        for second in (None, {"success": False, "message": "No"}):
            rig = self.rig(mode="hunt")
            rig.world["control"]["activities"]["restock"] = False
            out = rig.tick(rich())
            answers = [res(out["steps"][0]["call"], {"success": True}, out["steps"][0]["input"])]
            if second:
                answers.append(res(out["steps"][1]["call"], second, out["steps"][1]["input"]))
            rig.tick(*answers, stock(), rich())
            self.assertNotIn("selected", rig.world.own("equipment"), second)
            self.assertEqual([e for e in rig.events("activity_done") if "loadouts are selected" in e["text"]], [])
            rig.t += equipment.RETRY + 1
            self.assertEqual(rig.tick(rich())["steps"][:2], K.loadouts(*equipment.PVP1), second)   # both, again


class Bank(Upkeep):
    """RUL-2026-11-12-153: "10m is fine to pull out for training but 200k is the in pocket limit for running
    around"."""

    def rig(self):
        rig = Rig(mode="guard", upkeep=True)
        rig.world["control"]["activities"] = {"restock": False, "training": False, "equipment": False}
        return rig

    def move(self, pocket, bank_, training_for=0, purchase=None, later=0):
        """The transfer that is made with this much in pocket and in the bank, or None: with training asking
        for that many seconds, restock asking for a purchase's price, and that much time gone since."""
        rig = self.rig()
        if training_for:
            rig.world["training"]["draw_until"] = rig.t + training_for
        if purchase:
            rig.world["inventory"]["draw"] = {"ryo": purchase, "until": rig.t + 60}
        out = rig.tick(user(money=pocket, bank=bank_), dt=later)
        return out["steps"][0] if out["activity"] == "bank" else None

    def test_running_around_the_pocket_holds_no_more_than_its_limit(self):
        self.assertEqual((bank.POCKET, bank.TRAINING), (200_000, 10_000_000))   # the director's two figures
        for pocket, bank_, step in ((bank.POCKET + 1, 0, K.to_bank(bank.POCKET + 1 - bank.KEEP)),
                                    (10_000_000, 900_000_000, K.to_bank(10_000_000 - bank.KEEP)),
                                    (bank.POCKET, 0, None), (bank.LOW, 900_000_000, None),
                                    (bank.LOW - 1, 900_000_000, K.to_pocket(bank.KEEP - bank.LOW + 1)),
                                    (bank.LOW - 1, C.RESERVE + 30_000, K.to_pocket(30_000)),
                                    (bank.LOW - 1, C.RESERVE, None)):
            self.assertEqual(self.move(pocket, bank_), step, (pocket, bank_))

    def test_for_a_training_fill_the_pocket_is_filled_to_ten_million(self):
        for pocket, bank_, step in ((150_000, 900_000_000, K.to_pocket(bank.TRAINING - 150_000)),
                                    (150_000, C.RESERVE + 4_000_000, K.to_pocket(4_000_000)),
                                    (150_000, C.RESERVE, None),             # the bank is not taken under the reserve
                                    (bank.TRAINING, 900_000_000, None),     # it has it: and it stays while it is wanted
                                    (12_000_000, 900_000_000, None)):
            self.assertEqual(self.move(pocket, bank_, training_for=60), step, (pocket, bank_))
        # the wish lasts a few minutes at most: after it, what is left goes back to the bank
        self.assertEqual(self.move(9_400_000, 900_000_000, training_for=60, later=61), K.to_bank(9_400_000 - bank.KEEP))

    def test_for_a_purchase_the_pocket_is_filled_to_its_price_and_never_past_the_limit(self):
        for pocket, price, step in ((30_000, 165_000, K.to_pocket(135_000)),
                                    (30_000, 450_000, K.to_pocket(bank.POCKET - 30_000)),
                                    (180_000, 165_000, None)):
            self.assertEqual(self.move(pocket, 900_000_000, purchase=price), step, (pocket, price))
        self.assertIsNone(self.move(30_000, 900_000_000, purchase=165_000, later=61))   # the wish has run out
        rig = self.rig()
        rig.world["inventory"]["draw"] = {"ryo": 165_000, "until": rig.t + 60}
        out = rig.tick(user(money=30_000, bank=900_000_000))
        rig.tick(res("bank.toPocket", {"success": True}, out["steps"][0]["input"]), user(money=165_000, bank=899_865_000))
        self.assertIs(rig.world["inventory"]["restock_due"], True)          # restock is told the pocket can pay

    def test_a_transfer_spends_nothing_and_a_refused_one_waits(self):
        rig = self.rig()
        out = rig.tick(user(money=30_000_000, bank=0))
        out = rig.tick(res("bank.toBank", {"success": True}, out["steps"][0]["input"]),
                       user(money=bank.KEEP, bank=30_000_000 - bank.KEEP))
        self.assertEqual((rig.world.spent_today(), out["activity"] == "bank"), (0.0, False))
        self.assertIn("29,900,000 ryo to the bank", rig.events("activity_done")[-1]["text"])
        rig = self.rig()
        out = rig.tick(user(money=30_000_000, bank=0))
        no = res("bank.toBank", {"success": False, "message": "No"}, out["steps"][0]["input"])
        self.assertNotEqual(rig.tick(no, user(money=30_000_000, bank=0))["activity"], "bank")
        rig.t += bank.RETRY + 1
        self.assertEqual(rig.tick(user(money=30_000_000, bank=0))["activity"], "bank")


class SessionEnd(Upkeep):
    def test_the_energy_is_trained_and_pvp_1_selected_before_the_character_sleeps(self):
        rig = Rig(upkeep=True)
        rig.world["control"]["activities"] = {"restock": False, "bank": False}
        rig.world["control"]["end_session"] = True
        rig.world.own("training")["next"] = rig.t + 99999
        home = dict(sector=C.HOME_SECTOR, intelligence=1, willpower=2)
        out, energy, order = rig.tick(rich(curEnergy=900, **home)), 900, []
        for _ in range(6):
            order.append(out["activity"])
            answers = [res(s["call"], {"success": True}, s["input"]) for s in out["steps"]
                       if s.get("call") in ("train.startTraining",) + equipment.SELECTS]
            answers += [stock()] if "item.getUserItems" in rig.calls(out) else []
            if out["activity"] == "session":
                break
            energy = 0 if out["activity"] == "training" else energy         # spent, once the game has it
            out = rig.tick(*answers, rich(curEnergy=energy, **home))
        self.assertEqual(order, ["equipment", "training", "session"])       # then the session's own call: sleep
        self.assertEqual(out["steps"][0], K.wake())

    def test_with_the_upkeep_switched_off_it_sleeps_at_once(self):
        rig = Rig()
        rig.world["control"]["end_session"] = True
        out = rig.tick(rich(curEnergy=900, sector=C.HOME_SECTOR))
        self.assertEqual((out["activity"], out["steps"][0]), ("session", K.wake()))


class UpkeepUnderTrouble(Upkeep):
    """The chaos cases of the brief's AP1 step 7, for the upkeep: a brain that restarts, a refusal by the rate
    limit, an activity that fails."""

    def test_a_brain_that_restarts_in_the_middle_of_a_pass_goes_on_with_it(self):
        rig = self.rig()
        rig.tick(rich())
        rig.world.save()
        rig.new_brain()                                                     # between the read and its answer
        out = rig.tick(stock(**{PANACEA: (2, "ITEM_3", False, None)}), rich())
        self.assertEqual([s["input"]["stack"] for s in out["steps"] if s.get("call") == "item.buy"], [4])
        rig.world.save()
        rig.new_brain()                                                     # and between the purchase and its answer
        out = rig.tick(res("item.buy", {"success": True}, {"itemId": PANACEA, "stack": 4}), stock(), rich())
        self.assertEqual((out["activity"] == "restock", len(rig.events("item"))), (False, 1))

    def test_a_purchase_the_rate_limit_refused_is_not_said_to_be_made(self):
        rig = self.rig()
        rig.tick(rich())
        short = stock(**{PANACEA: (2, "ITEM_3", False, None)})
        out = rig.tick(short, rich())
        (buy,) = [s for s in out["steps"] if s.get("call") == "item.buy"]
        out = rig.tick(res("item.buy", None, buy["input"], error=RATE_LIMITED), short, rich())
        self.assertEqual(rig.events("item"), [])
        self.assertIn("item.buy", rig.calls(out))                           # still short: asked for again
        self.assertGreaterEqual(out["hold"], C.RATE_BACKOFF)                # after the pause the limit calls for

    def test_an_upkeep_activity_that_fails_is_set_aside_and_the_hunt_goes_on(self):
        rig = self.rig()
        with mock.patch.object(restock.Restock, "plan", side_effect=RuntimeError("the table is broken")):
            out = rig.tick(rich())
        self.assertEqual(out["activity"], "pvp_hunt")
        self.assertIn("restock: its plan failed", rig.events("error")[-1]["text"])
        self.assertEqual(rig.tick(rich(), dt=5)["activity"], "pvp_hunt")    # set aside for a minute
        rig.t += 61
        self.assertEqual(rig.tick(rich())["activity"], "restock")

    def test_nothing_of_the_upkeep_is_done_while_the_player_is_paused_or_in_a_fight(self):
        rig = Rig(upkeep=True)
        rig.world["control"]["paused"] = True
        self.assertIsNone(rig.tick(rich(curEnergy=9000, money=90_000_000))["activity"])
        rig = Rig(upkeep=True)
        out = rig.tick(user("BATTLE", bid="B1", money=90_000_000, curEnergy=9000))
        self.assertEqual(out["activity"], "battle")


if __name__ == "__main__":
    unittest.main()
