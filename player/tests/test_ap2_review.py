"""The review of AP2's first part at 988c56cc (docs/reviews/AI_PLAYER_AP2_LANE_A_REVIEW.md on
chatgpt/review-ai-player-ap2 @ 12bf61d3): two high findings and two medium, each a class here, built on the
review's own script (docs/reviews/evidence/ap2_lane_a/reproduce.py there).

H1  The run lock was asked when a batch was planned, and nothing looked at it when the calls were delivered. A
    batch planned 65 s before the lease's end went out 56 s before it, inside the minute in which no call is
    made; a paced one 4.5 s before it; one that waited through a crash, or was given again from its receipt,
    after it
H2  Every purchase of a restock pass was sized by the whole of what the day still allowed, and the gate held
    each call against it alone: 180,000 ryo were admitted with 170,000 left, and nobody was asked
H3  With 9,400,000 left in the pocket by a training fill, training set off for the village and a session's end
    for home: the bank's deposit ranks below both, and nothing made them wait for it
H4  A loadout selection was followed by a profile read only. What sits in the slots was not read again, the
    hunt went on, and the planners' feed still named the thrown weapon of the loadout before
"""
import contextlib
import io
import json
import os
import unittest
from unittest import mock

from player import brain, calls as K, config as C, relay, runlock
from player.activities import bank, equipment, training
from player.registry import plan
from player.tests.support import Rig, my_items, res, user
from player.tests.test_relay import token_of
from player.tests.test_rereview4 import Killed, dies_before_the_receipt
from player.tests.test_rereview6 import calls_of
from player.tests.test_rereview9 import WhatAVersionBeforeLeft
from player.tests.test_runlock import on_the_accounts_folder
from player.tests.test_upkeep import KUNAI, PANACEA, PILL, T, jutsu, queue, stock
from player.world import utc_day

REVIEWED = "988c56ccbff9f153a0fa546e9cae3a2d99c696b6"
"""The head the review was of: its batches carry no cutoff."""
AP1 = "62e1aab13c61f5e48b70c9a66b4d7bc1824fe1f9"
"""AP1's head, which this stands on: no run lock, no cutoff, and the number before this one."""
HUNT = ["profile.getUser", "travel.getSectorData", "stealth.useSensory"]


class H1TheLeaseAtDelivery(unittest.TestCase):
    """The review's harness: the real `brain next`, its file, the receipt, the pacing and the brain, with a
    scripted lock tool and the test's clock. The brain is the one of the account's own folder."""

    def start(self, before, crowded=False, renews=False):
        """A hunt whose claim has `before` seconds left when the relay asks. renews: whether a renewal can be
        pushed. crowded: twenty world calls are in the minute, so the batch is paced."""
        self.r = r = Rig()
        r.world.absorb([user()._replace(at=r.t)])
        self.tool = on_the_accounts_folder(r)
        r.brain.lock.hold()
        self.expires = r.brain.lock.state["expires"]
        self.cutoff = self.expires - runlock.STOP_MARGIN
        r.t = self.expires - before
        self.tool.broken = None if renews else "offline renewal"
        if crowded:
            r.world["budget"]["calls"] = [[r.t, "world"] for _ in range(C.WORLD_CAP)]
        r.world.save()
        self.handled, self.oversleeps, self.dies_in_the_wait, real = 0, 0.0, False, brain.Brain

        def make(live):
            b = real(live, clock=lambda: r.t, combat=r.combat, gates=r.brain.gates)
            b.lock, handle = runlock.RunLock(b.world, tool=self.tool, rehearsal=False), b.handle

            def counted(*args, **kwargs):
                self.handled += 1
                return handle(*args, **kwargs)
            b.handle = counted
            return b
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(brain, "Brain", make))
            stack.enter_context(mock.patch.object(brain.time, "time", lambda: r.t))
            stack.enter_context(mock.patch.dict(os.environ, {
                "TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(r.dir, "absent"),
                "TNR_PLAYER_FIGHTS": os.path.join(r.dir, "fights")}))
            self.addCleanup(stack.pop_all().close)
        self.token = token_of(self.next()[0])

    def next(self, token=None):
        def sleep(n):
            if self.dies_in_the_wait and n >= 1:
                self.dies_in_the_wait = False
                raise Killed
            self.r.t += n + (self.oversleeps if n >= 1 else 0)
        out = io.StringIO()
        brain.next_batch(self.r.dir, token, out, sleep)
        return out.getvalue().splitlines()

    def client(self):
        return relay.read(os.path.join(self.r.dir, "client.json"))

    def out_or_loose(self):
        return [c for c in relay.read(os.path.join(self.r.dir, "world.json"))["budget"]["calls"] if len(c) > 2]

    def said_too_short(self):
        return [e for e in self.r.events("stall") if "lease ends too soon" in e["text"]]

    # ---- the brain: a call that is due at or after the cutoff is not put in a batch
    def test_a_call_due_inside_the_last_minute_is_not_put_in_a_batch(self):
        self.start(before=65)
        self.assertEqual(calls_of(self.next(self.token)), [])               # was: four calls, 56 s before the end
        self.assertEqual((self.out_or_loose(), len(self.said_too_short())), ([], 1))

    def test_a_paced_call_that_would_run_after_the_cutoff_is_not_either(self):
        self.start(before=65, crowded=True)
        self.assertEqual(calls_of(self.next(self.token)), [])               # was: three calls, 4.5 s before the end
        self.assertEqual(self.out_or_loose(), [])

    def test_it_is_said_once_for_a_lease_and_not_at_every_ask(self):
        self.start(before=100, crowded=True)                                # paced to 40 s before the end
        for _ in range(3):
            lines = self.next(self.token)
            self.assertEqual(calls_of(lines), [])
            self.token = token_of(lines[-1])
        self.assertLess(self.r.t, self.cutoff)                              # the lock was held all the while
        self.assertEqual(len(self.said_too_short()), 1)

    def test_a_call_due_before_the_cutoff_goes_though_the_renewal_failed(self):
        self.start(before=75)
        self.assertEqual(calls_of(self.next(self.token))[:3], HUNT)
        self.assertLess(self.r.t, self.cutoff)                              # the lease runs out by itself
        self.assertEqual(self.client()["held"]["token"], f"{self.client()['relay']}-1")

    def test_a_renewed_lease_carries_the_paced_batch(self):
        self.start(before=65, crowded=True, renews=True)
        self.assertEqual(calls_of(self.next(self.token)), HUNT)
        self.assertGreater(self.r.t, self.cutoff)                           # past the old cutoff, and
        self.assertLess(self.r.t, relay.read(os.path.join(self.r.dir, "world.json"))["records"]["run_lock"]["expires"]
                        - runlock.STOP_MARGIN)

    # ---- `brain next`: a batch whose lease no longer reaches its last call is not printed
    def nothing_of_it_is_printed_and_the_brain_is_asked_afresh(self, lines):
        """`brain next` woke with the batch in hand and gave it up: the relay is sent straight back, and the
        brain, told that the batch was not printed, decides afresh, with no lease and so with no call."""
        self.assertEqual(lines, [relay.next_line(self.token)])
        state = self.client()
        self.assertEqual((state["pending"], state["held"], len(state["unprinted"])), (None, None, 1))
        self.assertEqual(self.handled, 1)
        self.tool.other = "forge"                                           # another runner has the lock by now
        self.assertEqual(calls_of(self.next(self.token)), [])
        self.the_batch_is_counted_as_not_printed()

    def the_batch_is_counted_as_not_printed(self):
        self.assertEqual(self.handled, 2)                                   # a fresh decision, not the old batch
        self.assertEqual((self.out_or_loose(), self.client()["unprinted"], self.client()["held"]), ([], [], None))

    def test_a_batch_whose_brain_next_wakes_after_the_cutoff_is_not_printed(self):
        self.start(before=75)
        self.oversleeps = 150.0
        lines = self.next(self.token)                                       # was: printed 150 s late
        self.assertGreater(self.r.t, self.expires)
        self.nothing_of_it_is_printed_and_the_brain_is_asked_afresh(lines)

    def test_a_batch_that_waited_through_a_crash_is_not_printed_after_the_cutoff(self):
        self.start(before=75)
        self.dies_in_the_wait = True
        with self.assertRaises(Killed):
            self.next(self.token)
        waiting = self.client()["pending"]
        self.assertEqual(waiting["until"], self.cutoff)
        self.r.t = self.cutoff + 1
        self.assertLess(self.r.t - waiting["ready_at"], C.STALE_OUTBOX)     # not too old to print: only too late
        self.assertEqual(calls_of(self.next(self.token)), [])               # was: printed, a second after the cutoff
        self.the_batch_is_counted_as_not_printed()                          # (given up and asked afresh in one go)

    def test_a_batch_given_again_from_its_receipt_is_not_printed_after_the_cutoff(self):
        self.start(before=75)
        with dies_before_the_receipt(self.r), self.assertRaises(Killed):
            self.next(self.token)
        self.r.t = self.expires + 70
        lines = self.next(self.token)                                       # was: three calls, 71 s after the end
        self.assertEqual(self.handled, 1)                                   # the same request: nothing run twice
        self.nothing_of_it_is_printed_and_the_brain_is_asked_afresh(lines)

    def test_the_same_crash_inside_the_lease_prints_the_batch(self):
        self.start(before=600)
        self.dies_in_the_wait = True
        with self.assertRaises(Killed):
            self.next(self.token)
        self.r.t = self.client()["pending"]["ready_at"]
        self.assertEqual(calls_of(self.next(self.token))[:3], HUNT)
        self.assertEqual(self.handled, 1)

    def test_a_waiting_batch_with_no_cutoff_on_record_is_not_this_versions(self):
        self.start(before=600)
        self.dies_in_the_wait = True
        with self.assertRaises(Killed):
            self.next(self.token)
        state = self.client()
        del state["pending"]["until"]
        relay.write(os.path.join(self.r.dir, "client.json"), state)
        self.assertIsNone(brain._who(os.path.join(self.r.dir, "client.json"))["pending"])

    # ---- the waits inside a batch count
    def test_a_batch_lapses_by_its_last_call_with_the_waits_in_front_of_it(self):
        steps = [K.user(), K.wait(30), K.user(), K.wait(20)]
        for until, now, late in ((None, 0, False), (100, 69.9, False), (100, 70, True), (100, 99, True)):
            self.assertIs(runlock.lapsed({"steps": steps, "until": until}, now), late, (until, now))
        self.assertFalse(runlock.lapsed({"steps": [K.wait(500)], "until": 100}, 99))    # no call: nothing to stop
        self.assertTrue(runlock.lapsed({"steps": steps, "until": "soon"}, 0))            # a cutoff that is no time

    def test_a_batch_is_cut_at_the_first_call_that_would_run_at_or_after_the_cutoff(self):
        steps = [K.user(), K.wait(4), K.user(), K.wait(6), K.user(), K.wait(1), K.user()]
        kept, late = runlock.within(steps, 100, 110)
        self.assertEqual(([("call" in s, s.get("wait")) for s in kept], late),
                         ([(True, None), (False, 4), (True, None)], 2))     # the call at 110 is cut, and what is
        self.assertEqual(runlock.within(steps, 100, 110.01), (steps[:5], 1))   # behind it; no wait is left over
        self.assertEqual(runlock.within(steps, 100, None), (steps, 0))
        self.assertEqual(runlock.within([K.wait(600)], 100, 110), ([K.wait(600)], 0))

    def test_what_is_cut_is_not_left_in_the_ledger(self):
        r = Rig()
        r.world.absorb([user()._replace(at=r.t)])
        on_the_accounts_folder(r)
        r.brain.lock.hold()
        r.t = r.brain.lock.state["expires"] - runlock.STOP_MARGIN - 5       # five seconds to the cutoff
        plan_ = [K.user(), K.wait(3), K.user(), K.wait(3), K.user()]
        steps, _, _ = r.brain._paced(plan_, "world", 0.0)
        self.assertEqual(steps, plan_[:3])
        self.assertEqual(len([c for c in r.world["budget"]["calls"] if c[2:3] == ["out"]]), 2)   # was: three

    def test_a_rehearsal_has_no_cutoff(self):
        r = Rig()
        out = r.tick(user())
        self.assertTrue(r.calls(out))
        self.assertIsNone(out["until"])
        self.assertNotIn("run_lock", r.world["records"])


class H1TheHeadThatWasReviewed(WhatAVersionBeforeLeft):
    """A batch that 988c56cc made says nothing of the lease it was made under. It is another version's."""

    def test_nothing_it_made_is_delivered_and_its_ledger_is_held(self):
        self.nothing_it_made_is_delivered(REVIEWED)

    def test_nor_what_ap1s_head_made_under_the_number_before_this_one(self):
        """A batch in a receipt of AP1's has no cutoff on record. Under one number with this version's it would
        be given again as a batch that has none to keep."""
        self.nothing_it_made_is_delivered(AP1)


class H2OneAllowanceForABatch(unittest.TestCase):
    def rig(self, left, pocket=200_000):
        """An upkeep rig with `left` ryo of the day's allowance not yet spent."""
        r = Rig(upkeep=True)
        r.world["control"]["activities"] = {"training": False, "equipment": False, "bank": False}
        self.me = user(money=pocket, bank=900_000_000)
        r.tick(self.me)
        r.world["records"]["spend"] = {"day": utc_day(r.t), "ryo": C.DAILY_CAP - left}
        return r

    @staticmethod
    def buys(out):
        return [s for s in out["steps"] if s.get("call") == "item.buy"]

    # ---- the review's case
    def test_a_restock_pass_stays_inside_what_the_day_still_allows(self):
        r = self.rig(left=170_000)
        out = r.tick(stock(**{PANACEA: (0, "ITEM_3", False, None), PILL: None}), self.me)
        bought = self.buys(out)
        self.assertEqual([s["input"]["stack"] for s in bought], [3, 5])     # was: 3 and 15
        self.assertEqual(sum(s["meta"]["ryo"] for s in bought), 170_000)    # was: 180,000 admitted
        self.assertEqual(r.world["decisions"], [])

    def test_and_buys_everything_when_it_fits(self):
        r = self.rig(left=180_000)
        out = r.tick(stock(**{PANACEA: (0, "ITEM_3", False, None), PILL: None}), self.me)
        self.assertEqual([s["input"]["stack"] for s in self.buys(out)], [3, 15])

    def test_what_is_still_out_counts_against_the_pass(self):
        r = self.rig(left=170_000)
        r.world["records"]["spend"]["out"] = [["bx", 100_000]]              # a batch that went with a replaced relay
        r.world["budget"]["calls"].append([r.t, "world", "loose", "bx", r.t, "ra-1"])
        out = r.tick(stock(**{PANACEA: (0, "ITEM_3", False, None), PILL: None}), self.me)
        self.assertEqual([s["input"]["stack"] for s in self.buys(out)], [1, 15])    # 55,000 and 15,000 of 70,000
        self.assertEqual(r.world["decisions"], [])

    # ---- the gate, for whatever plans a batch
    def test_the_gate_holds_a_call_against_the_calls_before_it_in_its_batch(self):
        r = self.rig(left=170_000)
        one, two = K.buy(PANACEA, 3, 165_000), K.buy(PILL, 15, 15_000)
        for plan in ([one], [two]):
            self.assertTrue(r.brain.gates.screen(plan, r.world, "restock")[0])       # each fits by itself
        ok, verdict, step = r.brain.gates.screen([one, two], r.world, "restock")
        self.assertEqual((ok, verdict.kind, verdict.rule, step), (False, "ask", "spend_cap", two))   # was: admitted
        self.assertFalse(r.brain.gates.screen([two], r.world, "recovery", ahead=[one])[0])   # added to a batch
        self.assertTrue(r.brain.gates.check(two, r.world, "restock").ok)             # nothing is left standing

    def test_and_the_reserve_against_them_too(self):
        r = Rig(upkeep=True)
        r.tick(user(money=200_000, bank=C.RESERVE - 30_000))                # 170,000 above the reserve
        one, two = K.buy(PANACEA, 3, 165_000), K.buy(PILL, 15, 15_000)
        self.assertTrue(r.brain.gates.screen([one], r.world, "restock")[0])
        ok, verdict, _ = r.brain.gates.screen([one, two], r.world, "restock")
        self.assertEqual((ok, verdict.kind), (False, "ask"))
        self.assertIn("reserve", verdict.reason)

    def test_calls_with_no_price_share_the_pocket_once(self):
        """Three places of the training queue: each may take all of the pocket, and all three no more."""
        r = self.rig(left=15_000_000, pocket=C.TRAINING_DRAW)
        fill = [K.train_jutsu(j) for j in T[:3]]
        self.assertEqual(r.brain.gates.price(fill, r.world), C.TRAINING_DRAW)
        self.assertTrue(r.brain.gates.screen(fill, r.world, "training")[0])
        costly = K.buy(PANACEA, 3, 6_000_000)
        self.assertEqual(r.brain.gates.price([costly] + fill, r.world), 6_000_000 + C.TRAINING_DRAW)
        self.assertFalse(r.brain.gates.screen([costly] + fill, r.world, "training")[0])   # 16,000,000 of 15,000,000
        self.assertEqual(r.brain.gates.price([K.user(), K.items()], r.world), 0)

    def test_a_step_that_is_put_in_front_of_a_batch_is_held_against_what_is_in_it(self):
        """The brain adds recovery's step to a fight's closing batch, and a rider's to a quiet one."""
        for left, goes in ((170_000, False), (180_000, True)):
            r = self.rig(left=left)
            closing = plan([K.buy(PANACEA, 3, 165_000)], "world", "a closing batch", tag="fight_end")
            with mock.patch.object(r.brain.reg.activities["recovery"], "after_fight", lambda w: [K.ramen(15_000)]):
                steps = r.brain._compose(r.brain.reg.activities["restock"], closing)
            self.assertEqual([s["call"] for s in steps], ["village.buyFood"] * goes + ["item.buy"], left)
            self.assertEqual(r.world.reserved(), 180_000 if goes else 165_000)

    def test_the_same_question_of_the_other_gate_that_counts(self):
        """One level transfer in 24 hours: the last one is written down when a batch is made, so two in one
        plan were each held against a day with none in it."""
        r = self.rig(left=1_000_000)
        one = K.call("jutsu.transferLevel", {"fromJutsuId": "a", "toJutsuId": "b", "transferLevels": 24}, K.DONE)
        two = K.call("jutsu.transferLevel", {"fromJutsuId": "c", "toJutsuId": "d", "transferLevels": 3}, K.DONE)
        self.assertTrue(r.brain.gates.screen([one], r.world, "training")[0])
        ok, verdict, step = r.brain.gates.screen([one, two], r.world, "training")
        self.assertEqual((ok, verdict.rule, step), (False, "one_transfer_a_day", two))   # was: both admitted

    # ---- what is admitted stays reserved until a profile read has shown what it cost
    def out_with(self, r, ask):
        """One tick as a relay's request brings it: (the batch, the id it is known by)."""
        r.t += 1
        return r.brain.handle([x._replace(at=r.t) for x in ask.pop("results")],
                              ask={"relay": "ra", "held": None, "gone": [], "ended": [], "unprinted": [], **ask})

    def a_purchase_is_out(self):
        r = self.rig(left=1_000_000)
        short = stock(**{PANACEA: (0, "ITEM_3", False, None), PILL: None})
        out = self.out_with(r, {"id": "b1", "seq": 1, "results": [short, self.me]})
        self.assertEqual(sum(s["meta"]["ryo"] for s in self.buys(out)), 180_000)
        return r, out

    def test_a_batch_that_is_out_keeps_its_cost_reserved_through_a_restart(self):
        r, _ = self.a_purchase_is_out()
        self.assertEqual((r.world.reserved(), r.world.spent_today()), (180_000, C.DAILY_CAP - 1_000_000))
        r.new_brain()
        self.assertEqual(r.world.reserved(), 180_000)
        more = K.buy(PILL, 15, 900_000)                                     # 180,000 + 900,000 of 1,000,000
        self.assertFalse(r.brain.gates.screen([more], r.world, "restock")[0])
        self.assertTrue(r.brain.gates.screen([K.buy(PILL, 15, 820_000)], r.world, "restock")[0])

    def test_the_profile_read_behind_the_purchases_turns_the_reservation_into_what_was_spent(self):
        r, out = self.a_purchase_is_out()
        paid = [res(s["call"], {"success": True}, s["input"]) for s in self.buys(out)]
        self.out_with(r, {"id": "b2", "seq": 2, "held": {"id": "b1", "token": "ra-1"},
                          "results": paid + [stock(), user(money=20_000, bank=900_000_000)]})
        self.assertEqual((r.world.reserved(), r.world.spent_today()), (0, C.DAILY_CAP - 1_000_000 + 180_000))

    def test_a_profile_read_from_before_the_purchases_does_not(self):
        r, out = self.a_purchase_is_out()
        paid = [res(s["call"], {"success": True}, s["input"]) for s in self.buys(out)]
        r.world["control"]["activities"]["restock"] = False
        self.out_with(r, {"id": "b2", "seq": 2, "held": {"id": "b1", "token": "ra-1"}, "results": [self.me] + paid})
        self.assertEqual(r.world.reserved(), 180_000)                       # that read shows nothing of them
        self.out_with(r, {"id": "b3", "seq": 3, "held": {"id": "b2", "token": "ra-2"},
                          "results": [user(money=20_000, bank=900_000_000)]})
        self.assertEqual((r.world.reserved(), r.world.spent_today()), (0, C.DAILY_CAP - 1_000_000 + 180_000))

    def test_a_batch_that_went_with_a_replaced_relay_keeps_its_reservation_until_it_is_over(self):
        r, _ = self.a_purchase_is_out()
        r.world["control"]["activities"]["restock"] = False
        gone = [{"id": "b1", "token": "ra-1"}]
        self.out_with(r, {"id": "c1", "seq": 2, "relay": "rb", "gone": gone, "results": [self.me]})
        self.assertEqual(r.world.reserved(), 180_000)                       # its relay may still make the calls
        self.out_with(r, {"id": "c2", "seq": 3, "relay": "rb", "held": {"id": "c1", "token": "rb-2"},
                          "ended": [["b1", r.t, "ra-1", "stopped"]], "results": [self.me]})
        self.assertEqual(r.world.reserved(), 0)


class H3NoTripWithAFullPocket(unittest.TestCase):
    AWAY = {"sector": C.CIRCUIT[0]}

    def rig(self, ending=False):
        r = Rig(upkeep=True)
        r.world.own("restock")["next"] = r.t + 9000
        r.world.own("equipment")["selected"] = list(equipment.PVP1)
        r.world.own("training")["next"] = r.t + 9000
        r.world["control"]["end_session"] = ending
        return r

    @staticmethod
    def trips(out):
        return [s for s in out["steps"] if s.get("call") == "travel.startGlobalMove"]

    # ---- the review's sequence: the fill leaves 9,400,000 and the energy is worth the trip
    def test_what_a_training_fill_leaves_is_banked_before_the_trip_to_the_village(self):
        r = Rig(upkeep=True)
        r.world.own("restock")["next"] = r.t + 900
        r.world.own("equipment")["selected"] = list(equipment.PVP1)
        road = {"money": 150_000, "bank": 900_000_000, "curEnergy": training.TRIP - 1}
        r.tick(user(**road))
        out = r.tick(queue(), jutsu({T[0]: 3}), user(**road))
        self.assertEqual(r.calls(out)[0], "bank.toPocket")
        drawn = {**road, "money": C.TRAINING_DRAW, "bank": 890_150_000}
        out = r.tick(res("bank.toPocket", {"success": True}, out["steps"][0]["input"]), user(**drawn))
        fills = [s for s in out["steps"] if s.get("call") == "jutsu.startTraining"]
        self.assertTrue(fills)
        left = {**drawn, "money": 9_400_000, "curEnergy": training.TRIP}
        out = r.tick(*[res(s["call"], {"success": True}, s["input"]) for s in fills], user(**left))
        self.assertEqual((out["activity"], r.calls(out)), ("bank", ["bank.toBank", "profile.getUser"]))   # was: training's trip
        out = r.tick(res("bank.toBank", {"success": True}, out["steps"][0]["input"]),
                     user(**{**left, "money": bank.KEEP}))
        self.assertEqual((out["activity"], len(self.trips(out))), ("training", 1))   # and then the trip

    def test_a_session_does_not_set_off_for_home_before_the_deposit(self):
        r = self.rig(ending=True)
        out = r.tick(user(money=9_400_000, **self.AWAY))
        self.assertEqual((out["activity"], self.trips(out)), ("bank", []))  # was: session, on the road with it
        out = r.tick(res("bank.toBank", {"success": True}, out["steps"][0]["input"]),
                     user(money=bank.KEEP, **self.AWAY))
        self.assertEqual((out["activity"], len(self.trips(out))), ("session", 1))

    # ---- a deposit that is refused, or waits to be tried again
    def test_no_trip_by_choice_while_a_refused_deposit_waits(self):
        for ending, energy in ((True, 0), (False, training.TRIP), (False, 0)):
            r = self.rig(ending)
            full = user(money=9_400_000, curEnergy=energy, **self.AWAY)
            out = r.tick(full)
            self.assertEqual(out["activity"], "bank")
            no = res("bank.toBank", {"success": False, "message": "The bank is closed"}, out["steps"][0]["input"])
            out = r.tick(no, full)
            for _ in range(8):                                              # the ten minutes until it is tried again
                self.assertEqual(self.trips(out), [], (ending, energy, out["activity"]))
                self.assertNotIn(out["activity"], ("bank", "session"))
                out = r.tick(full, dt=bank.RETRY / 9)
            r.t += bank.RETRY / 4
            self.assertEqual(r.tick(full)["activity"], "bank")              # and it is tried again
            self.assertEqual([e for e in r.events("finding") if e.get("rule") == "pocket_limit"], [])   # planned, not refused

    def test_the_hunt_stays_where_it_is_and_says_why(self):
        r = self.rig()
        r.world["control"]["activities"]["bank"] = True
        r.world.own("bank")["not_before"] = r.t + 9000                      # a refused deposit is waiting
        r.tick(user(money=9_400_000, sector=C.HOME_SECTOR))
        out = r.tick(user(money=9_400_000, sector=C.HOME_SECTOR))
        self.assertEqual((out["activity"], self.trips(out)), ("pvp_hunt", []))   # was: off to the circuit
        self.assertIn("the pocket holds more than it may on the road", out["note"])

    # ---- the gate, for whichever activity plans a trip
    def test_the_gate_refuses_a_trip_by_choice_and_lets_the_fights_and_recoverys_go(self):
        r = self.rig()
        go = K.trip(C.HOME_SECTOR)[0]
        r.tick(user(money=C.POCKET_LIMIT + 1, **self.AWAY))
        for activity in ("training", "session", "pvp_hunt", "travel", None):
            verdict = r.brain.gates.check(go, r.world, activity)
            self.assertEqual((verdict.kind, verdict.rule), ("refuse", "pocket_limit"), activity)
        for activity in ("battle", "recovery"):
            self.assertNotEqual(r.brain.gates.check(go, r.world, activity).rule, "pocket_limit", activity)
        r.tick(user(money=C.POCKET_LIMIT, **self.AWAY))
        self.assertNotEqual(r.brain.gates.check(go, r.world, "session").rule, "pocket_limit")   # at the limit: goes
        r.tick(user(money=9_400_000, **self.AWAY))
        r.world["control"]["activities"]["bank"] = False                    # the director has the bank switched off:
        self.assertFalse(r.world.overfull())                                # the pocket is not the player's to mind
        self.assertNotEqual(r.brain.gates.check(go, r.world, "session").rule, "pocket_limit")

    def test_at_home_the_deposit_comes_before_the_character_sleeps(self):
        r = self.rig(ending=True)
        out = r.tick(user(money=9_400_000, sector=C.HOME_SECTOR))
        self.assertEqual(out["activity"], "bank")
        out = r.tick(res("bank.toBank", {"success": True}, out["steps"][0]["input"]),
                     user(money=bank.KEEP, sector=C.HOME_SECTOR))
        self.assertEqual((out["activity"], out["note"]), ("session", "session ending: sleeping at home"))


class H4ASelectionIsFinishedByARead(unittest.TestCase):
    OTHER = equipment.BACKUP_THROWN[0]

    def selected(self):
        """A hunt begins: the two loadouts are selected. -> (the rig, the answers to the two selections)."""
        r = Rig(upkeep=True)
        r.world["control"]["activities"].update(training=False, bank=False)
        self.me = user(money=100_000)
        r.tick(self.me)
        out = r.tick(stock(), self.me)
        self.assertEqual(r.calls(out), list(equipment.SELECTS) + ["item.getUserItems", "profile.getUser"])   # was: no item read
        self.assertTrue(r.world["inventory"]["stale"])
        return r, [res(s["call"], {"success": True}, s["input"]) for s in out["steps"][:2]]

    @staticmethod
    def thrown(r):
        with open(os.path.join(r.combat.live, "equipped.json"), encoding="utf8") as f:
            return json.load(f)["THROWN"]

    def other_loadout(self):
        """What PvP 1 equips here: another thrown weapon than the loadout before."""
        return stock(**{KUNAI: (30, "NONE", False, None), "more": [("b1", self.OTHER, 50, "THROWN", False, None)]})

    # ---- the review's case: the selection changes the thrown weapon
    def test_the_weapon_of_the_selected_loadout_is_in_the_feed_before_the_hunt_goes_on(self):
        r, yes = self.selected()
        self.assertEqual(self.thrown(r), KUNAI)
        out = r.tick(*yes, self.other_loadout(), self.me)
        self.assertEqual(self.thrown(r), self.OTHER)                        # was: the kunai still, and the hunt on
        self.assertEqual((out["activity"], r.world["inventory"].get("stale")), ("pvp_hunt", None))
        self.assertEqual(r.world.own("equipment")["selected"], list(equipment.PVP1))

    # ---- the read does not come back, or cannot be used
    def test_until_the_items_are_read_nothing_that_goes_by_them_acts(self):
        failed = res("item.getUserItems", None, {}, error="the connector timed out")
        unusable = res("item.getUserItems", {"*.id": ["u1", "u2"], "*.itemId": ["only one"]})
        for what, read in (("it failed", [failed]), ("its columns do not line up", [unusable]), ("it never came", [])):
            r, yes = self.selected()
            out = r.tick(*yes, *read, self.me)
            self.assertTrue(r.world["inventory"]["stale"], what)
            self.assertEqual(self.thrown(r), KUNAI, what)
            for _ in range(5):                                              # under READ_AGAIN: everybody waits
                self.assertNotIn(out["activity"], ("pvp_hunt", "restock", "repair", "equipment"), what)
                out = r.tick(self.me, dt=equipment.READ_AGAIN / 8)
            r.t += equipment.READ_AGAIN
            out = r.tick(self.me)
            self.assertEqual((out["activity"], r.calls(out)), ("equipment", ["item.getUserItems", "profile.getUser"]), what)
            out = r.tick(self.other_loadout(), self.me)
            self.assertEqual((self.thrown(r), out["activity"]), (self.OTHER, "pvp_hunt"), what)
            self.assertEqual(r.calls(r.tick(self.me)).count("item.selectItemLoadout"), 0, what)   # not selected again

    def test_restock_and_repair_wait_for_the_read_too(self):
        r, _ = self.selected()
        acts = r.brain.reg.activities
        r.world.own("restock").update(active=True)
        r.world.absorb([stock(more=[("g1", "armour_id", 1, "CHEST", False, 90)])._replace(at=r.t)])   # worn thin
        self.assertEqual([acts[n].available(r.world) for n in ("pvp_hunt", "restock", "repair")], [False] * 3)
        r.world["inventory"].pop("stale")
        self.assertEqual([acts[n].available(r.world) for n in ("pvp_hunt", "restock", "repair")], [True] * 3)

    def test_a_backup_that_goes_in_is_read_back_the_same_way(self):
        r = Rig(upkeep=True)
        r.world["control"]["activities"].update(training=False, bank=False)
        r.world.own("equipment")["selected"] = list(equipment.PVP1)
        me = user(money=100_000)
        r.tick(me)
        out = r.tick(stock(**{KUNAI: None, "more": [("b1", self.OTHER, 50, "NONE", False, None)]}), me)
        self.assertEqual(r.calls(out)[:2], ["item.toggleEquip", "item.getUserItems"])
        out = r.tick(res("item.toggleEquip", {"success": True}, out["steps"][0]["input"]), me)   # the read did not come
        self.assertTrue(r.world["inventory"]["stale"])
        self.assertNotEqual(out["activity"], "pvp_hunt")


if __name__ == "__main__":
    unittest.main()
