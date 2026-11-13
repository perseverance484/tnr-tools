"""The re-review of AP2's correction at 87e497a6 (docs/reviews/AI_PLAYER_AP2_REREVIEW1_LANE_A_REVIEW.md on
chatgpt/review-ai-player-ap2-rereview1 @ 89a18dc3). H1 is closed there. Three stay open, each a class here,
built on the review's own script (overlap.py there): the real `brain next` and `brain put`, one relay that
replaces another, the saved files, and a brain made afresh for every request.

H2  A reservation was dropped as soon as its batch was over and any profile read had come. Relay B replaced
    relay A, read the profile, and handed that read in together with the word that A was back. A had bought
    for 180,000 ryo in between. The read showed nothing spent; the reservation went; 180,000 more were
    admitted, 360,000 against the 180,000 the day had left, and nobody was asked
H3  With the bank activity switched off the pocket's limit was not minded: training, a session's end and the
    hunt set off with 9,400,000. That exception was the implementer's. The ruling has none
H4  The stale mark was one flag, and any read of my items took it away. B's read, made before A had selected,
    took it away while A's selection was still loose, and the hunt went on with the old weapon in the feed

What is required: a batch that is over and a read that measures it are two things. What a batch owes is paid
off by a read that is known to follow it (player/owed.py).
"""
import contextlib
import io
import json
import os
import unittest
from unittest import mock

from player import brain, calls as K, config as C, owed, relay
from player.activities import equipment, training
from player.tests.support import Rig, res, user
from player.tests.test_relay import token_of
from player.tests.test_rereview4 import Killed, dies_before_the_receipt
from player.tests.test_rereview9 import WhatAVersionBeforeLeft
from player.tests.test_upkeep import KUNAI, PANACEA, PILL, stock
from player.world import utc_day

REVIEWED = "87e497a6efa781fb1b43ef809cce3a3bd48b1842"
"""The head the re-review was of: protocol 6."""
SHORT = {PANACEA: (0, "ITEM_3", False, None), PILL: None}
PRICES = {PANACEA: 55_000, PILL: 1_000}
READS = ["item.getUserItems", "profile.getUser"]


class TwoRelays(unittest.TestCase):
    """The review's harness: a live folder with 180,000 ryo of the day's allowance left, `brain next` as a relay
    runs it, and `brain put` for what the relay's calls returned."""

    def start(self, pocket=200_000, equipment_on=False):
        self.r = r = Rig(upkeep=True)
        r.world["control"]["activities"].update(training=False, equipment=equipment_on)
        self.me = user(money=pocket, bank=900_000_000)
        r.world.absorb([self.me._replace(at=r.t)])
        r.world["records"]["spend"] = {"day": utc_day(r.t), "ryo": C.DAILY_CAP - 180_000}
        r.world.save()
        self.decisions, real = 0, brain.Brain

        def make(live):
            b = real(live, clock=lambda: r.t, combat=r.combat, gates=r.brain.gates)
            handle = b.handle

            def counted(*args, **kwargs):
                self.decisions += 1
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

    def next(self, token=None):
        """`brain next`: (the token to come back with, the batch's calls, the lines)."""
        out = io.StringIO()
        brain.next_batch(self.r.dir, token, out, lambda n: setattr(self.r, "t", self.r.t + n))
        lines = out.getvalue().splitlines()
        steps = [json.loads(x) for x in lines if x.startswith("{") and "call" in json.loads(x)]
        return (None if lines[-1].startswith("STOP") else token_of(lines[-1])), steps, lines

    def does(self, token, steps, items=None, me=None):
        """The relay makes the batch's calls, which takes it a second, and hands each result in."""
        self.r.t += 1
        for i, s in enumerate(steps, 1):
            data = {"item.getUserItems": (items or stock()).data, "profile.getUser": (me or self.me).data}
            self.assertEqual(brain.put(self.r.dir, token, i, json.dumps(data.get(s["call"], {"success": True}))), 0)

    def first_batch(self, items):
        """Relay A reads my items and the profile, and gets what the brain makes of them."""
        token, _, _ = self.next()
        token, steps, _ = self.next(token)
        self.assertEqual([s["call"] for s in steps][:2], READS)
        self.does(token, steps, items)
        return self.next(token)

    def a_is_back(self, a):
        """Relay A has made the calls of the batch it had, and asks again: it is told that it was replaced."""
        self.r.t += 1
        self.assertEqual(self.next(a)[2], [brain.SUPERSEDED])

    def saved(self):
        return relay.read(os.path.join(self.r.dir, "world.json"))

    def batch_held(self):
        return relay.read(os.path.join(self.r.dir, "client.json"))["held"]["id"]

    @staticmethod
    def bought(steps):
        return sum(s["input"]["stack"] * PRICES[s["input"]["itemId"]] for s in steps if s["call"] == "item.buy")


class H2TheMeasureFollowsThePurchases(TwoRelays):
    def a_buys_and_b_takes_over(self):
        """A is given 180,000 ryo of purchases. B replaces it and is given a read of my items and the profile."""
        self.start(pocket=400_000)
        a, steps, _ = self.first_batch(stock(**SHORT))
        self.assertEqual(self.bought(steps), 180_000)
        self.batch_a = self.batch_held()
        b, _, _ = self.next()
        b, reads, _ = self.next(b)
        self.assertEqual([s["call"] for s in reads], READS)
        return a, b, reads

    def spend(self):
        return self.saved()["records"]["spend"]

    def then_the_next_read_measures_them(self, b, steps):
        """B makes its next batch after A's purchases: its profile read shows them, and the reservation goes."""
        self.does(b, steps, stock(), user(money=100_000, bank=900_120_000))      # 180,000 less, and a deposit
        _, steps, _ = self.next(b)
        self.assertEqual((self.spend()["ryo"], self.spend()["out"], self.bought(steps)), (C.DAILY_CAP, [], 0))
        self.assertEqual(self.saved()["decisions"], [])

    # ---- the review's case
    def test_a_read_made_before_the_purchases_does_not_stand_for_them(self):
        a, b, reads = self.a_buys_and_b_takes_over()
        self.does(b, reads, stock(**SHORT))                                 # B reads before A buys: 400,000 still
        self.a_is_back(a)                                                   # A buys for 180,000, and is back
        self.r.t += 1
        b, steps, _ = self.next(b)                                          # B hands its read in, with that word
        self.assertEqual(self.bought(steps), 0)                             # was: 180,000 more, nobody asked
        self.assertEqual(self.spend()["ryo"], C.DAILY_CAP - 180_000)        # nothing is measured yet,
        self.assertEqual(self.spend()["out"], [[self.batch_a, 180_000.0, True]])   # and so it stays reserved
        self.assertEqual(self.saved()["decisions"], [])
        self.then_the_next_read_measures_them(b, steps)

    def test_a_read_made_after_them_measures_them_and_the_reservation_goes_with_the_read_after(self):
        """The review's control. The brain cannot tell this read from the one above: it was asked for before the
        brain knew A was back. What it shows is counted; the reservation waits for one more read."""
        a, b, reads = self.a_buys_and_b_takes_over()
        self.a_is_back(a)
        self.r.t += 1
        self.does(b, reads, stock(), user(money=220_000, bank=900_000_000))
        self.r.t += 1
        b, steps, _ = self.next(b)
        self.assertEqual((self.spend()["ryo"], self.bought(steps)), (C.DAILY_CAP, 0))
        self.assertEqual(self.spend()["out"], [[self.batch_a, 180_000.0, True]])
        self.then_the_next_read_measures_them(b, steps)

    def test_a_request_answered_again_from_its_receipt_changes_nothing_of_it(self):
        a, b, reads = self.a_buys_and_b_takes_over()
        self.does(b, reads, stock(**SHORT))
        self.a_is_back(a)
        self.r.t += 1
        with dies_before_the_receipt(self.r), self.assertRaises(Killed):
            self.next(b)                                                    # answered, and its `brain next` dies
        b, steps, _ = self.next(b)                                          # the same request again
        self.assertEqual((self.decisions, self.bought(steps)), (4, 0))      # (four requests before; none run twice)
        self.assertEqual(self.spend()["out"], [[self.batch_a, 180_000.0, True]])
        self.then_the_next_read_measures_them(b, steps)

    def test_the_operators_word_ends_the_batch_and_does_not_measure_it_either(self):
        a, b, reads = self.a_buys_and_b_takes_over()
        self.does(b, reads, stock(**SHORT))
        brain.stopped(self.r.dir, ["all"], io.StringIO())                   # A is ended by hand, having bought
        self.r.t += 1
        b, steps, _ = self.next(b)
        self.assertEqual((self.bought(steps), self.spend()["out"]), (0, [[self.batch_a, 180_000.0, True]]))
        self.then_the_next_read_measures_them(b, steps)


class H4TheLookFollowsTheSelection(TwoRelays):
    OTHER = equipment.BACKUP_THROWN[0]

    def other_loadout(self):
        return stock(**{KUNAI: (30, "NONE", False, None), "more": [("b1", self.OTHER, 50, "THROWN", False, None)]})

    def a_selects_and_b_takes_over(self):
        """A is given the selection. B replaces it, and after READ_AGAIN is given a read of my items."""
        self.start(equipment_on=True)
        a, steps, _ = self.first_batch(stock())
        self.assertEqual([s["call"] for s in steps], list(equipment.SELECTS) + READS)
        self.batch_a = self.batch_held()
        b, _, _ = self.next()
        self.r.t += equipment.READ_AGAIN + 1
        b, reads, _ = self.next(b)
        self.assertEqual([s["call"] for s in reads], READS)
        return a, b, reads

    def loose(self):
        return any(c[2:3] == ["loose"] and c[3] == self.batch_a for c in self.saved()["budget"]["calls"])

    def thrown(self):
        return relay.read(os.path.join(self.r.combat.live, "equipped.json"))["THROWN"]

    def then_the_read_after_it_ends_the_wait(self, b, steps):
        self.assertEqual([s["call"] for s in steps], READS)                 # asked for at once, now that it is over
        self.does(b, steps, self.other_loadout())
        self.next(b)
        saved = self.saved()
        self.assertEqual((saved["inventory"].get("stale"), saved["relay"]["activity"], self.thrown()),
                         (None, "pvp_hunt", self.OTHER))

    # ---- the review's case
    def test_a_read_made_before_the_selection_does_not_end_the_wait(self):
        a, b, reads = self.a_selects_and_b_takes_over()
        self.does(b, reads, stock())                                        # B reads before A selects: the old loadout
        b, steps, _ = self.next(b)
        saved = self.saved()
        self.assertTrue(self.loose())
        self.assertEqual(saved["inventory"]["stale"], [[self.batch_a, None]])   # was: gone,
        self.assertNotEqual(saved["relay"]["activity"], "pvp_hunt")            # and the hunt on
        self.assertEqual(self.thrown(), KUNAI)                              # (what was equipped then, truly)
        self.a_is_back(a)                                                   # A selects, and is back
        self.r.t += 1
        self.does(b, steps)
        b, steps, _ = self.next(b)
        self.assertEqual((self.loose(), self.saved()["inventory"]["stale"]), (False, [[self.batch_a, None, True]]))
        self.then_the_read_after_it_ends_the_wait(b, steps)

    def test_a_read_handed_in_with_the_word_that_it_is_over_is_not_known_to_follow_it(self):
        """The review's control: A selects and is back before B makes its read. The feed is right at once; the
        brain cannot know that this read followed the selection, and asks for one that does."""
        a, b, reads = self.a_selects_and_b_takes_over()
        self.a_is_back(a)
        self.does(b, reads, self.other_loadout())
        b, steps, _ = self.next(b)
        self.assertEqual((self.loose(), self.thrown()), (False, self.OTHER))
        self.assertEqual(self.saved()["inventory"]["stale"], [[self.batch_a, None, True]])
        self.then_the_read_after_it_ends_the_wait(b, steps)

    def test_while_the_selection_is_loose_no_read_ends_the_wait_however_many_come(self):
        a, b, steps = self.a_selects_and_b_takes_over()
        for _ in range(3):
            self.does(b, steps, stock())
            self.r.t += equipment.READ_AGAIN + 1
            b, steps, _ = self.next(b)
            self.assertEqual(self.saved()["inventory"]["stale"], [[self.batch_a, None]])
            self.assertNotEqual(self.saved()["relay"]["activity"], "pvp_hunt")
        self.assertEqual([s["call"] for s in steps], READS)                 # the feed is kept to what is equipped


class H3TheLimitDoesNotHangOnTheBankSwitch(unittest.TestCase):
    AWAY = {"sector": C.CIRCUIT[0]}

    def rig(self, ending=False):
        r = Rig(upkeep=True)
        r.world["control"]["activities"].update(bank=False)                 # the director has the bank switched off
        r.world.own("restock")["next"] = r.t + 9000
        r.world.own("training")["next"] = r.t + 9000
        r.world.own("equipment")["selected"] = list(equipment.PVP1)
        r.world["control"]["end_session"] = ending
        return r

    def no_trip(self, r, out):
        self.assertNotIn("travel.startGlobalMove", r.calls(out))            # was: on the road with 9,400,000
        self.assertEqual([e for e in r.events("finding") if e.get("rule") == "pocket_limit"], [])   # not even planned

    # ---- the review's three cases
    def test_training_does_not_set_off_for_the_village(self):
        r = self.rig()
        self.no_trip(r, r.tick(user(money=9_400_000, curEnergy=training.TRIP, **self.AWAY)))
        self.assertIsNone(r.brain.reg.activities["training"]._energy(r.world))

    def test_a_session_does_not_set_off_for_home_and_says_why(self):
        r = self.rig(ending=True)
        out = r.tick(user(money=9_400_000, **self.AWAY))
        self.no_trip(r, out)
        self.assertEqual((out["activity"], r.calls(out)), ("session", ["profile.getUser"]))
        self.assertIn("9,400,000 ryo in the pocket and 200,000 is the most it may hold on the road", out["note"])
        self.assertIn("the bank activity is switched off", out["note"])
        self.assertGreaterEqual(out["hold"], 30)
        out = r.tick(user(money=150_000, **self.AWAY))                      # banked by hand: home it goes
        self.assertEqual((out["activity"], out["steps"][0]["input"]), ("session", {"sector": C.HOME_SECTOR}))

    def test_the_hunt_stays_where_it_is_and_says_why(self):
        r = self.rig()
        r.tick(user(money=9_400_000, sector=C.HOME_SECTOR))
        out = r.tick(user(money=9_400_000, sector=C.HOME_SECTOR))
        self.no_trip(r, out)
        self.assertEqual(out["activity"], "pvp_hunt")
        self.assertIn("staying here: the pocket holds more than it may on the road", out["note"])

    def test_the_gate_refuses_the_trip_for_each_of_them(self):
        r = self.rig()
        r.tick(user(money=9_400_000, **self.AWAY))
        self.assertTrue(r.world.overfull())                                 # was: False, the bank being off
        for activity in ("training", "session", "pvp_hunt"):
            verdict = r.brain.gates.check(K.trip(C.HOME_SECTOR)[0], r.world, activity)
            self.assertEqual((verdict.kind, verdict.rule), ("refuse", "pocket_limit"), activity)   # was: allow
        self.assertTrue(r.brain.gates.check(K.trip(C.HOME_SECTOR)[0], r.world, "recovery").ok)    # not by choice

    def test_at_the_limit_the_trips_go_bank_or_no_bank(self):
        r = self.rig(ending=True)
        out = r.tick(user(money=C.POCKET_LIMIT, **self.AWAY))
        self.assertEqual((out["activity"], r.calls(out)[0]), ("session", "travel.startGlobalMove"))


class WhatABatchOwes(unittest.TestCase):
    """player/owed.py by itself, on a rig's ledger: batch "x" owes, and "y" is the batch made after it."""

    def world(self, out=None, loose=(), last="y"):
        w = Rig().world
        calls = [[w.now, "world", "out"]] if out else []
        w["budget"].update(batch=out or last, calls=calls + [[w.now, "world", "loose", b, w.now, "ra-1"] for b in loose])
        return w

    def test_only_a_read_known_to_follow_the_batch_pays_it_off(self):
        row = [["x", 5]]
        for name, w, kept in (("the batch is out", self.world(out="x"), row), ("it is loose", self.world(loose=["x"]), row),
                              ("it is over, and the read is another batch's", self.world(), row),
                              ("it is over, and the read is its own, behind its calls", self.world(last="x"), [])):
            self.assertEqual(owed.read(w, row), kept, name)
        self.assertEqual(owed.read(self.world(last="x"), row, own=False), row)   # its own, from before its calls
        self.assertEqual(owed.read(self.world(loose=["x"]), [["x", 5, True]]), [])   # (marked: the brain knew)

    def test_a_row_is_marked_once_its_batch_is_over_and_then_any_read_pays_it_off(self):
        for w, marked in ((self.world(out="x"), False), (self.world(loose=["x"]), False), (self.world(), True)):
            kept = owed.settle(w, [["x", 5]])
            self.assertEqual(kept, [["x", 5, True]] if marked else [["x", 5]])
            self.assertEqual(owed.read(self.world(), kept), [] if marked else [["x", 5]])
        self.assertEqual(owed.settle(self.world(), [["x", 5, True]]), [["x", 5, True]])

    def test_what_the_version_before_kept_is_read_and_not_taken_for_paid(self):
        self.assertEqual((owed.rows(None), owed.rows([]), owed.rows(True)), ([], [], [[None, None]]))
        self.assertEqual(owed.rows([["x", 180_000.0]]), [["x", 180_000.0]])
        r = Rig(upkeep=True)
        r.world["control"]["activities"].update(training=False, bank=False)
        r.world.own("equipment")["selected"] = list(equipment.PVP1)
        r.world["records"]["spend"]["out"], r.world["inventory"]["stale"] = [["gone", 180_000.0]], True
        r.world.save()
        r.new_brain()
        self.assertEqual(r.world.reserved(), 180_000)
        out = r.tick(user())                                                # neither batch is in the ledger: over
        self.assertEqual((r.world["records"]["spend"]["out"], r.world["inventory"]["stale"]),
                         ([["gone", 180_000.0, True]], [[None, None, True]]))
        self.assertEqual((out["activity"], r.calls(out)), ("equipment", READS))   # the read that is owed
        out = r.tick(stock(), user())
        self.assertEqual((r.world.reserved(), r.world["inventory"].get("stale")), (0, None))


class TheHeadThatWasReviewed(WhatAVersionBeforeLeft):
    """87e497a6 let a second batch of purchases through on a read that measured nothing. What it made is another
    version's."""

    def test_nothing_it_made_is_delivered_and_its_ledger_is_held(self):
        self.nothing_it_made_is_delivered(REVIEWED)


if __name__ == "__main__":
    unittest.main()
