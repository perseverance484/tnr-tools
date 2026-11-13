"""The review of e4a267cd (docs/reviews/AI_PLAYER_AP1_REREVIEW11_LANE_A_REVIEW.md on
chatgpt/review-ai-player-ap1-rereview11-lane-a @ 219515fe). H1 is closed there against three predecessors. Of H2
one finding is left, the classes here, built on the review's own script. Those tests fail on 25308e2a, which is
the code of e4a267cd after the split.

H2  e4a267cd counted a takeover before it saved it: the count's file was raised, then world.json was written.
    Between the two the old file and the raised count made the name of a takeover that did not exist yet.
    `brain stopped`, said in that moment by a process of its own, wrote word of that name down. So did one said
    after the world model could not be written, while the same brain lived and saved later. The brain's own hold
    had another name, so the word let nothing go; it stayed in client.json. When the old file came back, byte
    for byte and with its time, that later takeover had the name the word was kept under: four calls nine
    seconds later, and no word said of it

What is required: the operator cannot write down a name made of a count and a file that do not belong together.
The count-first behaviour at a crash stays. It holds for a word said during the save and for one said after a
save that failed, with the same brain going on. The name that is acknowledged is the hold's own.

The correction: the save of a takeover is three writes (World.save): "saving", the world model, the count. While
"saving" stands no name is spoken of. The last class holds e4a267cd to the new number with its own package.
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from player import brain, config as C, relay, world
from player.brain import client
from player.tests import test_rereview7
from player.tests.test_relay import token_of
from player.tests.test_rereview4 import Killed
from player.tests.test_rereview5 import update
from player.tests.test_rereview6 import calls_of
from player.tests.test_rereview9 import WhatAVersionBeforeLeft
from player.world import World, generation

REVIEWED = "e4a267cd1ab5ff85c3b2399bab713f2870da6ccb"
"""The head the review was of: protocol 3, the count raised before the world model is written."""
OLD = b"{ a ledger that another version kept"
SAVING = "the relays from before the update (a brain is saving the takeover: say it again in a moment)"
ASKS = r'''
import json, sys
from player import brain
brain.client.LOOKS = (3, 0.01)
brain.stopped(sys.argv[1], ["all"])
'''


class AFolderOfAnotherVersion(unittest.TestCase):
    """A live folder whose world.json is another version's, on the test's clock (which starts at the real time:
    a word said by a process of its own carries the real time). No tests of its own: the classes below, and
    those of the next review, are made of it."""

    def setUp(self):
        self.live = tempfile.mkdtemp(prefix="player-saving-")
        self.path = os.path.join(self.live, "world.json")
        self.now, self.real, self.write = [time.time()], brain.Brain, World._write
        self.env = {"TNR_PLAYER_NO_DAEMON": "1", "TNR_PLAYER_LIVE": self.live,
                    "TNR_TRANSCRIPT": os.path.join(self.live, "none"),
                    "TNR_PLAYER_FIGHTS": os.path.join(self.live, "fights")}
        for p in (mock.patch.dict(os.environ, self.env), mock.patch.object(time, "time", lambda: self.now[0]),
                  mock.patch.object(brain, "Brain", lambda live: self.real(live, clock=lambda: self.now[0])),
                  mock.patch.object(client, "LOOKS", (2, 0))):
            p.start()
            self.addCleanup(p.stop)
        self.old_file()

    def old_file(self):
        """The other version's ledger is on disk: the same bytes, written at the same time, every time."""
        with open(self.path, "wb") as f:
            f.write(OLD)
        os.utime(self.path, ns=(1_700_000_000_000_000_000, 1_700_000_000_000_000_000))

    def says(self, *names):
        out = io.StringIO()
        brain.stopped(self.live, list(names), out)
        return json.loads(out.getvalue())

    def a_process_of_its_own_says_all(self, program=ASKS):
        done = subprocess.run([sys.executable, "-W", "ignore", "-c", program, self.live], cwd=C.ROOT, timeout=60,
                              capture_output=True, text=True, env={**os.environ, **self.env, "PYTHONPATH": C.ROOT})
        return json.loads(done.stdout)

    def next(self, token=None):
        out = io.StringIO()
        brain.next_batch(self.live, token, out, lambda t: self.now.__setitem__(0, self.now[0] + max(0, t)))
        return out.getvalue().splitlines()

    def queued(self):
        return (relay.read(os.path.join(self.live, "client.json")) or {}).get("ended") or []

    def saved_hold(self):
        (name,) = {c[3] for c in relay.read(self.path)["budget"]["calls"] if c[1] == "update"}
        return name

    def a_later_takeover_of_the_same_file_is_held(self, spoken_of):
        """The old file comes back, byte for byte and with its time, two minutes on: another takeover. Nothing
        that was said before lets it go."""
        self.now[0] += 120
        self.old_file()
        (later,) = self.says()["still_held"]
        self.assertNotIn(later, [f"the relays from before the update ({n})" for n in spoken_of])   # was: the same
        token, t0 = token_of(self.next()[0]), self.now[0]
        while self.now[0] < t0 + 300:
            lines = self.next(token)
            token = token_of(lines[-1])
            self.assertEqual(calls_of(lines), [])                           # was: four calls, nine seconds later
        self.assertEqual(len(update(self.live)), C.CALL_LIMIT)

    def dies_at(self, home, which):
        """The brain ends at one of the save's writes: "saving" (the first), "world" (the second) or "count"
        (the third). The write it ends at is not made."""
        def dies(path, obj):
            if (which == "world" and path == self.path) or (which != "world" and path != self.path
                                                             and obj.get("saving") is (which == "saving")):
                raise Killed
            self.write(path, obj)
        with mock.patch.object(World, "_write", staticmethod(dies)):
            with self.assertRaises(Killed):
                home.world.save()


class WhileATakeoverIsSaved(AFolderOfAnotherVersion):
    # ---- the review's first way: a word said between the writes, by a process of its own
    def test_word_said_while_the_resident_saves_is_not_written_down(self):
        seen = {}

        def between(path, obj):
            if path == self.path and "word" not in seen:                    # the count's file says "saving" now
                seen["at"] = generation(self.live)
                probe = brain._lock(self.live)
                seen["home"] = probe is None                                # the resident has the brain's lock
                if probe is not None:
                    probe.close()
                seen["word"] = self.a_process_of_its_own_says_all()
            self.write(path, obj)
        os.makedirs(os.path.join(self.live, "inbox"))                       # a relay's request is waiting
        relay.write(relay.request_path(self.live, 1, "ab" * 4),
                    {"protocol": relay.PROTOCOL, "seq": 1, "id": "ab" * 4, "relay": "r1", "results": [],
                     "held": None, "gone": [], "ended": [], "unprinted": []})
        with mock.patch.object(World, "_write", staticmethod(between)):
            self.assertEqual(brain.run(self.live, forever=False), 0)        # the resident takes over, and saves
        self.assertEqual((seen["word"]["stopped"], seen["word"]["still_held"]), ([], [SAVING]))   # was: a name
        self.assertEqual(self.queued(), [])                                 # nothing is kept for later
        self.assertEqual((seen["at"], seen["home"]), ((0, True), True))
        self.assertEqual(generation(self.live), (1, False))
        hold = self.saved_hold()
        self.assertEqual(self.says("all")["stopped"], [f"the relays from before the update ({hold})"])   # the hold's own
        self.a_later_takeover_of_the_same_file_is_held([hold])

    # ---- the review's second way: the world model could not be written, and the same brain goes on
    def test_word_said_after_a_save_that_failed_is_not_written_down_while_that_brain_is_home(self):
        home_lock = brain._lock(self.live)                                  # a brain that is running holds its lock
        self.addCleanup(home_lock.close)
        home = self.real(self.live, clock=lambda: self.now[0])

        def no_world(path, obj):
            if path == self.path:
                raise OSError("the disk is full")
            self.write(path, obj)
        with mock.patch.object(World, "_write", staticmethod(no_world)):
            home._save()                                                    # it says so, and goes on
        said = self.says("all")
        self.assertEqual((said["stopped"], said["still_held"], self.queued()), ([], [SAVING], []))   # was: a name
        with open(self.path, "rb") as f:
            self.assertEqual((generation(self.live), f.read()), ((0, True), OLD))   # not the operator's to count
        home._save()                                                        # the same brain, later: all three writes
        self.assertEqual(generation(self.live), (1, False))
        hold = self.saved_hold()
        home_lock.close()
        self.a_later_takeover_of_the_same_file_is_held([hold])

    def test_with_nobody_home_the_save_that_was_left_is_counted_and_the_file_has_a_new_name(self):
        """The review's script makes its brain without the lock: to `brain stopped` nobody is home. The save
        that was left is counted, so a word is taken, for a name no brain had before; the brain that did not
        die counts again when it saves."""
        home = self.real(self.live, clock=lambda: self.now[0])

        def no_world(path, obj):
            if path == self.path:
                raise OSError("the disk is full")
            self.write(path, obj)
        with mock.patch.object(World, "_write", staticmethod(no_world)):
            home._save()
        (word,) = self.says("all")["stopped"]
        self.assertEqual(generation(self.live), (1, False))
        home._save()
        self.assertEqual(generation(self.live), (2, False))
        self.assertNotEqual(word, f"the relays from before the update ({self.saved_hold()})")
        self.a_later_takeover_of_the_same_file_is_held([word.split("(")[1][:-1], self.saved_hold()])

    # ---- the other moments of the three writes
    def test_a_brain_that_ends_after_the_world_model_is_written_has_its_save_counted_by_the_next(self):
        home = self.real(self.live, clock=lambda: self.now[0])
        self.dies_at(home, "count")
        self.assertEqual(generation(self.live), (0, True))                  # saved, and "saving" still stands
        hold = self.saved_hold()
        self.assertEqual(self.says()["still_held"], [f"the relays from before the update ({hold})"])   # by its rows
        self.real(self.live, clock=lambda: self.now[0])                     # the next brain to start
        self.assertEqual(generation(self.live), (1, False))
        self.a_later_takeover_of_the_same_file_is_held([hold])

    def test_and_when_the_old_file_is_back_before_any_brain_has_started(self):
        home = self.real(self.live, clock=lambda: self.now[0])
        (before,) = self.says()["still_held"]
        self.dies_at(home, "count")
        self.old_file()                                                     # "saving" stands, and the file is old
        (after,) = self.says("all")["stopped"]                              # nobody home: counted, a new name
        spoken = self.now[0]
        self.assertEqual(generation(self.live), (1, False))
        self.assertNotEqual(before, after)
        token, lines = token_of(self.next()[0]), []
        while not calls_of(lines) and self.now[0] < spoken + 300:
            lines = self.next(token)
            token = token_of(lines[-1])
        self.assertTrue(calls_of(lines))                                    # the word is for this takeover:
        self.assertGreaterEqual(self.now[0], spoken + 60)                   # a minute after it, the hold is over
        self.assertEqual(update(self.live), [])

    def test_other_holds_are_spoken_of_while_a_takeover_is_being_saved(self):
        home_lock = brain._lock(self.live)
        self.addCleanup(home_lock.close)
        relay.write(os.path.join(self.live, "takeovers.json"), {"count": 3, "saving": True})
        relay.write(os.path.join(self.live, "client.json"),
                    {"protocol": relay.PROTOCOL, "gone": [{"token": "aaaaaa-1", "id": "batch-of-a"}]})
        said = self.says("all")
        self.assertEqual((said["stopped"], said["still_held"]), (["aaaaaa-1"], [SAVING]))
        self.assertEqual([e[0] for e in self.queued()], ["batch-of-a"])
        self.assertEqual(self.says(client.SAVING)["not_held"], [client.SAVING])   # and it has no name to say


class TheCountAndTheFileAreReadTogether(unittest.TestCase):
    def test_a_save_that_runs_across_the_read_is_not_half_seen(self):
        live = tempfile.mkdtemp(prefix="player-seen-")
        path = os.path.join(live, "world.json")
        with open(path, "wb") as f:
            f.write(OLD)
        counts = iter([(0, False), (0, True), (0, True), (1, False), (1, False), (1, False)])
        with mock.patch.object(world, "generation", lambda _: next(counts)):
            raw, _, count, saving = world.seen(path)
        self.assertEqual((raw, count, saving), (OLD, 1, False))             # read again until the count stood still

    def test_the_count_keeps_the_older_file_and_says_saving_only_when_it_says_true(self):
        live = tempfile.mkdtemp(prefix="player-count-")
        for kept, said in (({"count": 2}, (2, False)), ({"count": 2, "saving": True}, (2, True)),
                           ({"count": 2, "saving": 1}, (2, False)), ({"count": 2, "saving": "true"}, (2, False)),
                           ({"saving": True}, (0, False)), ([2, True], (0, False))):
            relay.write(os.path.join(live, "takeovers.json"), kept)
            self.assertEqual(generation(live), said, kept)


class TheHeadThatWasReviewed(WhatAVersionBeforeLeft):
    """e4a267cd could take word for a takeover that did not exist yet. What it made is another version's."""

    def test_nothing_it_made_is_delivered_and_its_ledger_is_held(self):
        self.nothing_it_made_is_delivered(REVIEWED)


class ItsBrainIsStillRunning(test_rereview7.P1AnOlderBrainIsStillRunning):
    """The three process tests, against the resident brain of e4a267cd."""
    VERSION = REVIEWED


if __name__ == "__main__":
    unittest.main()
