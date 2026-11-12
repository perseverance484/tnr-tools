"""The review of efa79808 (docs/reviews/AI_PLAYER_AP1_REREVIEW4_REVIEW.md on chatgpt/review-ai-player-ap1-rereview4
@ 430a782f): three findings, the classes L1 to L3, each built on the review's own reproducer (its blocks D1 to
D3). Those tests fail on efa79808.

L1  "stopped all" was kept as a word for every held batch, and read again later it let go of a relay that was
    replaced after the operator spoke
L2  a batch the client's file said nothing of was taken to have never been printed
L3  the last resort answered with nothing and no wait when held calls filled the minute
"""
import contextlib
import io
import json
import os
import time
import unittest
from unittest import mock

from player import brain, budget as B, calls as K, config as C, relay
from player.tests.support import Rig, start_fight, user
from player.tests.test_rereview2 import ask, most_in_a_minute
from player.tests.test_rereview3 import Client


class Killed(Exception):
    pass


def dies_before_the_receipt(rig):
    """relay.write, for a `brain next` that is killed just before it writes down the batch it is owed."""
    real = relay.write

    def write(path, obj):
        if path == os.path.join(rig.dir, "client.json") and obj.get("pending"):
            raise Killed
        return real(path, obj)
    return mock.patch.object(relay, "write", write)


class L1TheOperatorsWordNamesTheBatchesItIsSaidOf(Client):
    """`stopped all` was written down as "every held batch". The brain reads such word again when a request is
    answered from its receipt, and by then a relay the operator had not spoken of was held too."""

    def test_a_relay_replaced_after_the_word_is_not_let_go_by_it(self):
        """The review's script (D1)."""
        retired = self.new_relay_with_a_batch()
        active = self.new_relay_with_a_batch()                              # the retired one is stopped; this runs
        said = self.stopped("all")
        self.assertEqual((said["stopped"], said["still_held"]), ([retired], []))   # the running relay is not in it
        b = token_of_first(self.next())                                     # the running relay is replaced after
        with dies_before_the_receipt(self.rig):
            with self.assertRaises(Killed):
                self.next(b)
        n = len(self.loose(active))
        self.assertEqual((n > 0, self.loose(retired)), (True, []))
        self.next(b)                                                        # answered from its receipt: the word
        self.assertEqual(len(self.loose(active)), n)                        # is read again. Was 0
        self.assertEqual(self.next(active), [brain.SUPERSEDED])             # only that relay itself,
        self.next(self.client()["token"])
        self.assertEqual(self.loose(active), [])                            # or a word said of it, lets it go

    def test_the_word_is_kept_as_the_batches_it_covers(self):
        first = self.new_relay_with_a_batch()
        second = self.new_relay_with_a_batch()
        self.new_relay_with_a_batch()
        self.stopped("all")
        rows = self.client()["ended"]
        self.assertEqual(sorted(r[2] for r in rows), sorted([first, second]))
        self.assertTrue(all(isinstance(r[0], str) and r[0] != "*" and r[3] == "stopped" for r in rows))
        self.assertEqual({r[0] for r in rows}, {c[3] for c in self.loose()})   # each by its batch's id

    def test_asking_what_is_held_changes_nothing(self):
        """(The review planted this: a listing that let go of everything passed every test and 200 walks.)"""
        old = self.new_relay_with_a_batch()
        current = self.new_relay_with_a_batch()
        n, before = len(self.loose(old)), self.client()
        listed = self.stopped()
        self.assertEqual((listed["stopped"], listed["still_held"], listed["all"]), ([], [old], False))
        said = io.StringIO()
        with contextlib.redirect_stdout(said):                              # the same from the command line
            brain.main(["stopped"])
        self.assertEqual(json.loads(said.getvalue())["still_held"], [old])
        self.assertEqual(self.client(), before)                             # nothing is written,
        self.next(current)
        self.assertEqual(len(self.loose(old)), n)                           # and nothing is let go

    def test_all_reaches_what_is_held_with_no_relay_to_its_name(self):
        a = self.new_relay_with_a_batch()
        state = self.client()
        state.pop("held")                                                   # the record of who has it is lost
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        b = self.new_relay_with_a_batch()
        held = self.loose()
        self.assertEqual({c[5] for c in held}, {None})                      # held, for a relay not on record
        listed = self.stopped()
        self.assertEqual(listed["still_held"], [f"batch {held[0][3]}"])     # the operator can see it and name it
        self.assertEqual(self.stopped(a)["not_held"], [a])                  # (not by a token nobody recorded)
        self.assertEqual(self.stopped("all")["stopped"], [f"batch {held[0][3]}"])
        self.next(b)
        self.assertEqual(self.loose(), [])

    def test_a_batch_can_be_named_by_its_id(self):
        old = self.new_relay_with_a_batch()
        current = self.new_relay_with_a_batch()
        batch = self.loose(old)[0][3]
        self.assertEqual(self.stopped(batch)["stopped"], [old])
        self.next(current)
        self.assertEqual(self.loose(), [])


def token_of_first(lines):
    return json.loads(lines[0])["bash"].split()[-1]


class L2NotOnRecordIsNotNeverPrinted(Client):
    """A batch that the request named neither as handed in nor as gone was taken to have never been printed, and
    counted from that moment. A client file without the record (an older one, an edited one) made that true of
    a batch a relay still had: 34 calls in a minute, 24 in the world lane."""

    def without_the_record(self):
        """The review's script (D2): four calls printed to A; the record of it gone from the file; B replaces A."""
        a = self.new_relay_with_a_batch()
        n = len(self.client()["calls"])
        state = self.client()
        state.pop("held")
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        self.next(token_of_first(self.next()))
        return a, n

    def test_a_printed_batch_the_file_says_nothing_of_stays_held(self):
        a, n = self.without_the_record()
        self.assertEqual(len(self.loose()), n)                              # was 0: settled, A not back
        self.assertIn("not on record", [e["text"] for e in self.rig.events("finding")
                                        if e.get("about") == "budget"][-1])

    def test_and_its_relay_going_on_later_stays_under_the_limits(self):
        for lane, batches, limit in (("recovery", 15, C.CALL_LIMIT), ("world", 10, C.WORLD_CAP)):
            self.setUp()
            a, n = self.without_the_record()
            rig = self.rig
            rig.new_brain()
            rig.t = time.time() + 30
            rig.brain.budget.settle(asked=())                               # the replacement's own calls are done
            rig.t += 62
            made = [rig.t] * n                                              # and now A makes its four
            for _ in range(batches):
                out, _ = rig.brain.budget.pace([K.user(), K.user()], lane)
                for s in out:
                    if "wait" in s:
                        rig.t += s["wait"]
                    else:
                        made.append(rig.t)
                        rig.t += .01
            self.assertLessEqual(most_in_a_minute(made), limit, lane)       # was 34, and 24

    def test_files_as_the_version_before_wrote_them(self):
        """What 442a6311 left behind with a batch out: the ledger's batch a number, the client's file with the
        token and the calls but no record of who holds what."""
        a = self.new_relay_with_a_batch()
        number, n = int(a.split("-")[1]), len(self.client()["calls"])
        state = {k: v for k, v in self.client().items() if k not in ("held", "unprinted")}
        state.update(gone=[f"dead01-{number - 1}"], ended=[[number - 1, time.time()]])   # as it wrote them then
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        world = self.saved()
        world["budget"]["batch"] = number
        world["budget"]["calls"] += [[time.time() - 5000, "world", "loose", number - 1, time.time() - 4000]]
        relay.write(os.path.join(self.rig.dir, "world.json"), world)
        b = self.new_relay_with_a_batch()
        held = self.loose()
        self.assertEqual(len(held), n + 1)                                  # A's batch, and the one loose before:
        self.assertEqual({len(c) for c in held}, {6})                       # held, in the shape of today,
        self.assertEqual(self.next(a), [brain.SUPERSEDED])                  # and A coming back proves nothing now
        self.next(b)
        self.assertEqual(len(self.loose()), n + 1)
        self.stopped("all")                                                 # the operator's word is the way out
        self.next(self.client()["token"])
        self.assertEqual(self.loose(), [])

    def test_the_running_relay_handing_in_what_the_file_lost_track_of(self):
        a = self.new_relay_with_a_batch()
        n = len(self.client()["calls"])
        state = self.client()
        state.pop("held")
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        a = self.next(a)[-1]                                                # the same relay, back with its batch
        self.assertEqual(len(self.loose()), n)                              # nothing on record says it was its own

    # ---- what was never printed is still known, because the client says so
    def test_a_batch_whose_brain_next_died_is_known_to_be_unprinted(self):
        a = self.new_relay_with_a_batch()
        with dies_before_the_receipt(self.rig):
            with self.assertRaises(Killed):
                self.next(a)                                                # the brain made a batch; nobody got it
        made = self.saved()["budget"]["batch"]
        self.assertIn(made, self.client()["unprinted"])                     # on record before it was asked for
        self.next(token_of_first(self.next()))                              # a replacement asks
        self.assertEqual(self.loose(), [])                                  # held for nobody: it was never printed
        self.assertEqual(self.client()["unprinted"], [])

    def test_two_deaths_in_a_row_are_both_remembered(self):
        a = self.new_relay_with_a_batch()
        with dies_before_the_receipt(self.rig):
            with self.assertRaises(Killed):
                self.next(a)
        first = self.saved()["budget"]["batch"]
        b = token_of_first(self.next())
        with mock.patch.object(brain, "_await", side_effect=Killed):        # the replacement's first request dies
            with self.assertRaises(Killed):                                 # before the brain has seen it
                self.next(b)
        self.assertEqual(self.client()["unprinted"][0], first)
        self.next(b)
        self.assertEqual(self.loose(), [])

    def test_a_ledger_in_an_older_shape_keeps_its_holds(self):
        rig = Rig()
        rig.world["budget"]["calls"] = [[rig.t - 9000, "world", "loose", 7, rig.t - 8000],
                                        [rig.t - 9000, "world", "loose", 7, rig.t - 8000],
                                        [rig.t - 9000, "battle", "loose"], [rig.t - 5, "world"]]
        rig.world.save()
        rig.new_brain()
        held = rig.brain.budget.loose()
        self.assertEqual(sorted(n for _, _, n, _ in held), [1, 2])          # still held, each batch with an id
        self.assertTrue(all(batch is not None for _, batch, _, _ in held))
        self.assertEqual(rig.brain.budget.used(), 4)
        rig.tick(user())
        self.assertEqual({h["relay"] for h in rig.status()["budget"]["held"]}, {None})   # and the operator sees them


class L3NoAnswerWithNothingToDoAndNoWait(unittest.TestCase):
    """With the minute full of held calls the plan's calls are not sent. The ordinary tick then makes the relay
    wait; the last resort did not, and a relay that follows its lines came straight back, again and again."""

    def full(self, failing):
        """The review's script (D3)."""
        rig = Rig()
        battle, _, out = start_fight(rig)
        T, seen = rig.t, []
        rig.world["budget"]["calls"] = [[rig.t, "battle", "loose", "old-request", rig.t, "old-relay-1"]
                                        for _ in range(C.CALL_LIMIT)]
        rig.world["battle"]["inbox"] = dict(battle)
        fight = type(rig.brain.reg.activities["battle"])
        with mock.patch.object(fight, "available", side_effect=RuntimeError("persistent tick fault") if failing
                               else None, return_value=True):
            for seq in range(1, 6):
                out = ask(rig, seq, at=T + seq, relay="offline")
                seen.append((rig.calls(out), out["hold"]))
        return rig, seen

    def test_the_last_resort_waits_like_any_other_tick(self):
        rig, seen = self.full(failing=True)
        self.assertEqual(seen[0], ([], 1.0))                                # the first failure: come back soon
        self.assertEqual(seen[1:], [([], C.RATE_BACKOFF)] * 4)              # was ([], 0.0), four times

    def test_the_ordinary_tick_did_and_does(self):
        rig, seen = self.full(failing=False)
        self.assertEqual(seen, [([], C.RATE_BACKOFF)] * 5)

    def test_no_batch_with_nothing_in_it_is_given_without_a_wait(self):
        """Whatever makes it: a batch with no call, no wait and no STOP would bring the relay straight back."""
        rig = Rig()
        real = brain.Brain._decide
        with mock.patch.object(brain.Brain, "_decide", lambda self_, limited: dict(real(self_, limited),
                                                                                   steps=[], hold=0.0)):
            out = rig.tick()
        self.assertEqual((out["steps"], out["hold"]), ([], C.RATE_BACKOFF))


if __name__ == "__main__":
    unittest.main()
