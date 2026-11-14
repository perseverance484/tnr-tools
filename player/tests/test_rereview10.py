"""The second review of c412de4d (docs/reviews/AI_PLAYER_AP1_REREVIEW9_LANE_A_REVIEW.md on
chatgpt/review-ai-player-ap1-rereview9-lane-a @ f586a6b2). Its first finding is the H1 of the first review of that
commit, corrected at 7cf7d73c (test_rereview9.py). Its second is new: the class H2 here, built on the review's own
script. Those tests fail on 7cf7d73c.

H2  the hold on a ledger taken over from another version was named by that file's bytes and nothing else. An
    empty world.json was `update-da39a3ee` every time. The operator spoke of the first; `brain next` died before
    it had the brain's answer down, and so kept the word; the brain had saved. Two minutes later the file was
    empty again: a second takeover, under the same name. The kept word let its hold go, and a call was printed
    61.5 s later with no word said of it

What is required: a new takeover is told from a retry of the same one, also when the bytes repeat. Word of an
earlier one releases nothing of a later one. The name is the same from before any brain has the file until one
has saved it, so the operator can speak before a relay is started.

The correction counts the takeovers a live folder's brains have saved (live/takeovers.json) and puts the count in
the name. It also changes when a hold is let go, so the protocol's number changes with it: 7cf7d73c is a version
before this one, and the last class holds it to that with its own package.
"""
import io
import json
import os
import tempfile
import time
import types
import unittest
from unittest import mock

from player import brain, config as C, relay
from player.budget import UPDATE
from player.tests import support, test_rereview7
from player.tests.test_relay import token_of
from player.tests.test_rereview4 import Killed, dies_before_the_receipt
from player.tests.test_rereview5 import update
from player.tests.test_rereview6 import calls_of
from player.tests.test_rereview8 import hold
from player.tests.test_rereview9 import WhatAVersionBeforeLeft
from player.world import World, found, generation, takeovers

LAST = "7cf7d73c5cb235801b66e4b4763cb63e1bc7b14e"
"""The head before this one: it has the hold and the number 2, and names the hold by the file's bytes alone."""


class H2AWordIsForOneTakeover(unittest.TestCase):
    """The review's script. A live folder whose world.json cannot be read, on the test's clock."""

    def setUp(self):
        self.live = support.bare(tempfile.mkdtemp(prefix="player-unreadable-"))
        self.path = os.path.join(self.live, "world.json")
        self.now, self.real = [time.time()], brain.Brain
        for p in (mock.patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_PLAYER_LIVE": self.live,
                                               "TNR_TRANSCRIPT": os.path.join(self.live, "none"),
                                               "TNR_PLAYER_FIGHTS": os.path.join(self.live, "fights")}),
                  mock.patch.object(time, "time", lambda: self.now[0]),
                  mock.patch.object(brain, "Brain", lambda live: self.real(live, clock=lambda: self.now[0]))):
            p.start()
            self.addCleanup(p.stop)
        self.printed = []                                                   # when a batch with calls was printed

    def unreadable(self, text="", written=None):
        """world.json is written over with this, at this time (now, when none is given)."""
        with open(self.path, "w", encoding="utf8") as f:
            f.write(text)
        at = self.now[0] if written is None else written
        os.utime(self.path, (at, at))
        return at

    def says(self, *names):
        out = io.StringIO()
        brain.stopped(self.live, list(names), out)
        return json.loads(out.getvalue())

    def next(self, token=None):
        out = io.StringIO()
        brain.next_batch(self.live, token, out, lambda t: self.now.__setitem__(0, self.now[0] + max(0, t)))
        lines = out.getvalue().splitlines()
        if calls_of(lines):
            self.printed.append(self.now[0])
        return lines

    def asks(self, token, seconds):
        """The relay asks for that long, or until it is given a call: (the calls, its token)."""
        t0, calls = self.now[0], []
        while not calls and self.now[0] < t0 + seconds:
            lines = self.next(token)
            calls, token = calls_of(lines), token_of(lines[-1])
        return calls, token

    def client(self):
        return relay.read(os.path.join(self.live, "client.json"))

    def the_first_is_spoken_of_and_saved_and_the_word_is_kept(self):
        """Steps 1 and 2 of the review: (the first hold's name, the relay's token). self.spoken: when the
        word was said."""
        self.unreadable()
        said, self.spoken = self.says("all"), self.now[0]
        (name,) = said["stopped"]
        word = self.client()["ended"]
        token = token_of(self.next()[0])
        with dies_before_the_receipt(types.SimpleNamespace(dir=self.live)):
            with self.assertRaises(Killed):
                self.next(token)                                            # the brain answers, and has saved;
        self.assertEqual(self.client()["ended"], word)                      # `brain next` died with the word kept
        self.assertTrue(relay.ours(relay.read(self.path)["budget"]))
        return name, token

    def a_later_takeover_is_held_whatever_was_said_of_the_first(self, **second):
        first, token = self.the_first_is_spoken_of_and_saved_and_the_word_is_kept()
        self.now[0] += 120
        self.unreadable(**second)                                           # step 3: a second takeover
        (listed,) = self.says()["still_held"]
        self.assertNotEqual(listed, first)                                  # was: the first one's name
        calls, token = self.asks(token, 600)                                # step 4: the retry, and ten minutes more
        self.assertEqual(calls, [])                                         # was: a call 61.5 s later
        self.assertEqual(len(update(self.live)), C.CALL_LIMIT)
        self.assertEqual(f"the relays from before the update ({hold(self.live)})", listed)
        self.assertEqual(self.says("all")["stopped"], [listed])             # word of this one lets it go,
        spoken = self.now[0]
        calls, _ = self.asks(token, 300)
        self.assertTrue(calls)
        self.assertGreaterEqual(self.printed[0], spoken + 60)               # a minute after it was said

    def test_a_word_kept_through_a_crash_does_not_let_a_later_takeover_of_the_same_bytes_go(self):
        self.a_later_takeover_is_held_whatever_was_said_of_the_first()

    def test_nor_when_the_later_file_was_written_at_the_very_same_time(self):
        """The time a file was written does not tell two takeovers apart either: the count does."""
        written = self.now[0]
        self.a_later_takeover_is_held_whatever_was_said_of_the_first(written=written)

    def test_the_word_kept_through_the_crash_is_taken_again_and_does_no_harm(self):
        """The control: the same crash, and no second takeover. The retry is answered, and calls start a
        minute after the one word."""
        _, token = self.the_first_is_spoken_of_and_saved_and_the_word_is_kept()
        calls, _ = self.asks(token, 300)
        self.assertTrue(calls)
        self.assertGreaterEqual(self.printed[0], self.spoken + 60)
        self.assertLess(self.printed[0], self.spoken + 80)
        self.assertEqual(update(self.live), [])

    def test_a_takeover_keeps_its_name_until_a_brain_has_saved_it(self):
        """The other control: the operator speaks before any relay is started, brains come and go without
        saving, and the word still names the hold."""
        self.unreadable()
        (listed,) = self.says()["still_held"]
        for _ in range(3):
            started = self.real(self.live, clock=lambda: self.now[0])       # a brain that ends before it saves
            self.assertEqual({c[3] for c in started.world["budget"]["calls"]}, {listed.split("(")[1][:-1]})
            self.now[0] += 30
        self.assertEqual(self.says()["still_held"], [listed])
        self.assertFalse(os.path.exists(os.path.join(self.live, "takeovers.json")))   # nothing is counted yet
        self.assertEqual(self.says("all")["stopped"], [listed])
        spoken = self.now[0]
        calls, _ = self.asks(token_of(self.next()[0]), 300)
        self.assertTrue(calls)
        self.assertGreaterEqual(self.printed[0], spoken + 60)
        self.assertEqual(takeovers(self.live), 1)                           # saved: counted, once

    def test_a_brain_that_ends_between_the_count_and_the_save_leaves_the_file_under_a_new_name(self):
        """The count's file is written first (since the review of e4a267cd it says "saving", and whoever comes
        next counts the save that was left). So the takeover that was not saved is asked about again, under a
        new name; it is never the other way round, a saved takeover whose name stays free."""
        self.unreadable()
        (first,) = self.says("all")["stopped"]
        write = World._write

        def dies(path, obj):
            if path == self.path:
                raise Killed
            write(path, obj)
        with mock.patch.object(World, "_write", staticmethod(dies)):
            with self.assertRaises(Killed):
                self.real(self.live, clock=lambda: self.now[0]).world.save()
        self.assertEqual((generation(self.live), relay.read(self.path)), ((0, True), None))   # the file as it was
        with mock.patch.object(brain.client, "LOOKS", (1, 0)):
            (second,) = self.says()["still_held"]                           # nobody is home: it is counted here
        self.assertEqual(generation(self.live), (1, False))
        self.assertNotEqual(first, second)
        calls, token = self.asks(token_of(self.next()[0]), 300)
        self.assertEqual(calls, [])                                         # the word of before names nothing now
        self.says("all")
        self.assertTrue(self.asks(token, 300)[0])


class H2TheCount(unittest.TestCase):
    def folder(self):
        live = support.bare(tempfile.mkdtemp(prefix="player-count-"))
        return live, os.path.join(live, "world.json"), os.path.join(live, "takeovers.json")

    def test_only_a_saved_takeover_is_counted(self):
        live, path, count = self.folder()
        first = brain.Brain(live)                                           # a first start: nothing to take over
        first._save()
        brain.Brain(live)._save()                                           # an ordinary restart
        self.assertEqual((takeovers(live), os.path.exists(count)), (0, False))
        for n in (1, 2):
            world = relay.read(path)
            world["budget"].pop("protocol")                                 # another version's ledger
            relay.write(path, world)
            taken = brain.Brain(live)
            self.assertEqual(takeovers(live), n - 1)                        # not before it is saved,
            taken._save()
            taken._save()
            self.assertEqual(takeovers(live), n)                            # and once

    def test_the_same_bytes_are_another_takeover_after_each_one_that_was_saved(self):
        live, path, count = self.folder()
        names = []
        for _ in range(3):
            with open(path, "w", encoding="utf8"):
                pass                                                        # empty, every time,
            os.utime(path, (1_700_000_000, 1_700_000_000))                  # and written at the same time
            names.append(found(path))
            self.assertEqual(found(path), names[-1])                        # the same to everyone who looks,
            taken = brain.Brain(live)
            self.assertEqual({c[3] for c in taken.world["budget"]["calls"]}, {UPDATE + names[-1]})
            taken._save()
        self.assertEqual(len(set(names)), 3)                                # was: da39a3ee, three times

    def test_a_file_that_is_written_again_is_not_the_file_that_was_spoken_of(self):
        """Before any brain has saved it: the same bytes, written again later. Whatever wrote them was still
        about after the operator spoke."""
        live, path, count = self.folder()
        names = []
        for written in (1_700_000_000, 1_700_000_000, 1_700_000_060):
            with open(path, "w", encoding="utf8") as f:
                f.write("{ not a world model")
            os.utime(path, (written, written))
            names.append(found(path))
            brain.Brain(live)                                               # a brain looks, and ends without saving
        self.assertEqual((names[0] == names[1], names[1] == names[2], takeovers(live)), (True, False, 0))

    def test_a_count_that_cannot_be_read_is_none(self):
        live, path, count = self.folder()
        for text in ("", "{", "[1]", '{"count": "2"}', '{"count": true}', '{"count": -1}', '{"other": 1}'):
            with open(count, "w", encoding="utf8") as f:
                f.write(text)
            self.assertEqual(takeovers(live), 0, text)
        relay.write(count, {"count": 7})
        self.assertEqual(takeovers(live), 7)


class H2TheHeadBeforeThisOne(WhatAVersionBeforeLeft):
    """7cf7d73c let a hold go on word that was not said of it. What it made is another version's."""

    def test_nothing_it_made_is_delivered_and_its_ledger_is_held(self):
        self.nothing_it_made_is_delivered(LAST)


class H2ItsBrainIsStillRunning(test_rereview7.P1AnOlderBrainIsStillRunning):
    """The three process tests, against the resident brain of 7cf7d73c."""
    VERSION = LAST


if __name__ == "__main__":
    unittest.main()
