"""The review of ce1be6e9 (docs/reviews/AI_PLAYER_AP1_REREVIEW12_LANE_A_REVIEW.md on
chatgpt/review-ai-player-ap1-rereview12-lane-a @ 39070bc9). The cases of the review before it are corrected; one
finding is left, the classes here, built on the review's own script.

H2  ce1be6e9 let whatever made a World count a save of a takeover that it found unfinished, the lock or no. A
    reader that made one between a living brain's first and second write closed that brain's save: the count's
    file said (1, not saving) over the old world model. `brain stopped`, in the same process, then took a word
    for the name of that moment. The brain saved its hold and finished on the count it had read before its
    first write, also 1. When the old file came back, byte for byte and with its time, that takeover had the
    name the word was kept under: four calls nine seconds later, and no word said of it

What is required: whoever only reads leaves a living brain's save alone; a save that was left is counted under
the brain's lock; a save does not finish on a count that has been passed. The crash behaviour and the controls
of the earlier reviews stay.

The correction: making a World writes nothing. A brain that starts counts a left save when the brain's lock is
its own process's, or nobody's (brain.resident._left_save); `brain stopped` does when nobody is home, as before.
World.save reads the count again for its third write. The last classes hold ce1be6e9 to the new number.
"""
import os
import subprocess
import sys
import unittest
from unittest import mock

from player import brain, config as C, relay, world
from player.tests import test_rereview7
from player.tests.test_rereview9 import WhatAVersionBeforeLeft
from player.tests.test_rereview11 import OLD, SAVING, AFolderOfAnotherVersion
from player.world import World, generation

REVIEWED = "ce1be6e98eb39550e79806c5c8f9da87f67fa4eb"
"""The head the review was of: protocol 4, a World that is made counts."""
A_READER_ASKS = r'''
import json, sys
from player import brain
from player.world import World
brain.client.LOOKS = (3, 0.01)
World(sys.argv[1])
brain.stopped(sys.argv[1], ["all"])
'''
A_BRAIN_OF_ITS_OWN_ASKS = A_READER_ASKS.replace("World(sys.argv[1])", "brain.Brain(sys.argv[1])")
HAS_THE_LOCK = r'''
import sys
from player import brain
lock = brain._lock(sys.argv[1])
print("home" if lock else "not home", flush=True)
sys.stdin.read()
'''


def name_in(line):
    """update-xxxxxxxx out of "the relays from before the update (update-xxxxxxxx)"."""
    return line.split("(")[1][:-1]


class AReaderWhileABrainSaves(AFolderOfAnotherVersion):
    def the_resident_saves_and_meanwhile(self, program):
        """The resident takes the old file over and saves; between its first write and its second, a process of
        its own runs `program`. -> what that process printed, and the count's file before and after it."""
        seen = {}

        def between(path, obj):
            if path == self.path and "word" not in seen:                    # the count's file says "saving" now
                probe = brain._lock(self.live)
                seen["home"] = probe is None                                # the resident has the brain's lock
                if probe is not None:
                    probe.close()
                seen["before"] = generation(self.live)
                seen["word"] = self.a_process_of_its_own_says_all(program)
                seen["after"] = generation(self.live)
            self.write(path, obj)
        os.makedirs(os.path.join(self.live, "inbox"))                       # a relay's request is waiting
        relay.write(relay.request_path(self.live, 1, "ab" * 4),
                    {"protocol": relay.PROTOCOL, "seq": 1, "id": "ab" * 4, "relay": "r1", "results": [],
                     "held": None, "gone": [], "ended": [], "unprinted": []})
        with mock.patch.object(World, "_write", staticmethod(between)):
            self.assertEqual(brain.run(self.live, forever=False), 0)
        self.assertTrue(seen["home"])
        return seen

    def nothing_was_counted_and_no_word_taken(self, seen):
        self.assertEqual((seen["before"], seen["after"]), ((0, True), (0, True)))       # was: (1, False) after
        self.assertEqual((seen["word"]["stopped"], seen["word"]["still_held"]), ([], [SAVING]))   # was: a name
        self.assertEqual(self.queued(), [])
        self.assertEqual(generation(self.live), (1, False))                 # the brain's own three writes, no more
        self.a_later_takeover_of_the_same_file_is_held([self.saved_hold()])

    # ---- the review's script: World(live), then `brain stopped all`, in the process that speaks
    def test_a_world_made_between_a_living_brains_writes_leaves_its_save_alone(self):
        self.nothing_was_counted_and_no_word_taken(self.the_resident_saves_and_meanwhile(A_READER_ASKS))

    def test_and_so_does_a_brain_that_a_script_makes_there(self):
        self.nothing_was_counted_and_no_word_taken(self.the_resident_saves_and_meanwhile(A_BRAIN_OF_ITS_OWN_ASKS))

    # ---- making a World writes nothing, whatever the count's file says
    def test_making_a_world_writes_nothing(self):
        relay.write(os.path.join(self.live, "takeovers.json"), {"count": 3, "saving": True})
        before = {name: os.stat(os.path.join(self.live, name)).st_mtime_ns for name in os.listdir(self.live)}
        made = World(self.live)
        self.assertEqual(generation(self.live), (3, True))                  # was: (4, False)
        self.assertEqual({name: os.stat(os.path.join(self.live, name)).st_mtime_ns
                          for name in os.listdir(self.live)}, before)
        self.assertEqual(made.found, world.print_of(OLD, 1_700_000_000_000_000_000, 3))


class WhoCountsASaveThatWasLeft(AFolderOfAnotherVersion):
    """(count 0, saving) stands over the old file: a brain began to save the takeover and is gone."""

    def setUp(self):
        super().setUp()
        relay.write(os.path.join(self.live, "takeovers.json"), {"count": 0, "saving": True})

    def a_brain_starts(self):
        return self.real(self.live, clock=lambda: self.now[0])

    def test_a_brain_whose_process_has_the_lock_counts_it(self):
        lock = brain._lock(self.live)                                       # as the resident has it, and a
        self.addCleanup(lock.close)                                         # `brain next` that answers for itself
        home = self.a_brain_starts()
        self.assertEqual(generation(self.live), (1, False))
        self.assertEqual(home.budget.loose()[0][1], "update-" + world.print_of(OLD, 1_700_000_000_000_000_000, 1))

    def test_a_brain_made_with_nobody_home_counts_it_and_leaves_the_lock_free(self):
        self.a_brain_starts()
        self.assertEqual(generation(self.live), (1, False))
        lock = brain._lock(self.live)
        self.assertIsNotNone(lock)
        lock.close()

    def test_a_brain_made_while_another_process_has_the_lock_does_not(self):
        other = subprocess.Popen([sys.executable, "-W", "ignore", "-c", HAS_THE_LOCK, self.live], cwd=C.ROOT,
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                                 env={**os.environ, **self.env, "PYTHONPATH": C.ROOT})
        self.addCleanup(other.stdout.close)
        self.addCleanup(other.wait)
        self.addCleanup(other.stdin.close)
        self.assertEqual(other.stdout.readline().strip(), "home")
        self.a_brain_starts()
        self.assertEqual(generation(self.live), (0, True))                  # that brain's to finish

    def test_a_lock_that_was_given_back_is_nobodys(self):
        lock = brain._lock(self.live)
        self.assertTrue(brain._home(self.live))
        lock.close()                                                        # the file is closed, and still there
        self.assertFalse(brain._home(self.live))
        with mock.patch.object(brain, "_lock", return_value=None):          # and now another has it
            self.a_brain_starts()
        self.assertEqual(generation(self.live), (0, True))


class ASaveDoesNotFinishOnACountThatWasPassed(AFolderOfAnotherVersion):
    def test_the_count_is_read_again_for_the_third_write(self):
        """The review's sequence with a brain that has no lock (a script's): its save is counted from outside
        between its writes, and word is taken for the name of that moment."""
        home, seen = self.real(self.live, clock=lambda: self.now[0]), {}

        def between(path, obj):
            if path == self.path and not seen:
                (seen["word"],) = self.says("all")["stopped"]               # nobody home: counted, and a name
                seen["at"] = generation(self.live)
            self.write(path, obj)
        with mock.patch.object(World, "_write", staticmethod(between)), mock.patch.object(brain.client, "LOOKS", (1, 0)):
            home.world.save()
        self.assertEqual(seen["at"], (1, False))
        self.assertEqual(generation(self.live), (2, False))                 # was: (1, False), the word's count
        self.a_later_takeover_of_the_same_file_is_held([name_in(seen["word"]), self.saved_hold()])


class WhereverABrainEndsInItsSave(AFolderOfAnotherVersion):
    """The review's table: the brain ends before any write and at each of the three; the next one starts under
    the lock; word that was said of the first takeover lets nothing of a later one go."""

    def test_the_next_brain_under_the_lock_and_the_old_word(self):
        for ends_at, left, at_restart, saved in (("saving", (0, False), (0, False), (1, False)),
                                                 ("world", (0, True), (1, False), (2, False)),
                                                 ("count", (0, True), (1, False), (1, False)),
                                                 (None, (1, False), (1, False), (1, False))):
            with self.subTest(ends_at=ends_at):
                for name in ("takeovers.json", "client.json"):
                    if os.path.exists(os.path.join(self.live, name)):
                        os.unlink(os.path.join(self.live, name))
                self.old_file()
                home = self.real(self.live, clock=lambda: self.now[0])
                (word,) = self.says("all")["stopped"]                       # said of the takeover, before the save
                if ends_at:
                    self.dies_at(home, ends_at)
                else:
                    home.world.save()
                self.assertEqual(generation(self.live), left)
                lock = brain._lock(self.live)
                try:
                    after = self.real(self.live, clock=lambda: self.now[0])
                    self.assertEqual(generation(self.live), at_restart)
                    after._save()
                finally:
                    lock.close()
                self.assertEqual(generation(self.live), saved)
                self.a_later_takeover_of_the_same_file_is_held([name_in(word)])

    def test_word_said_before_the_third_write_names_the_hold_that_is_saved(self):
        """Once the world model is written, its hold is a row of the saved ledger and is spoken of as that row,
        though "saving" still stands. It is the brain's own hold: the takeover that comes later stays held."""
        home, seen = self.real(self.live, clock=lambda: self.now[0]), {}

        def before_the_third(path, obj):
            if path != self.path and obj.get("saving") is False and not seen:
                seen["at"] = generation(self.live)
                seen["word"] = self.a_process_of_its_own_says_all()
            self.write(path, obj)
        with mock.patch.object(World, "_write", staticmethod(before_the_third)):
            home.world.save()
        hold = self.saved_hold()
        self.assertEqual(seen["at"], (0, True))
        self.assertEqual(seen["word"]["stopped"], [f"the relays from before the update ({hold})"])
        self.a_later_takeover_of_the_same_file_is_held([hold])


class TheHeadThatWasReviewed(WhatAVersionBeforeLeft):
    """ce1be6e9 could take word for a takeover that did not exist yet. What it made is another version's."""

    def test_nothing_it_made_is_delivered_and_its_ledger_is_held(self):
        self.nothing_it_made_is_delivered(REVIEWED)


class ItsBrainIsStillRunning(test_rereview7.P1AnOlderBrainIsStillRunning):
    """The three process tests, against the resident brain of ce1be6e9."""
    VERSION = REVIEWED


if __name__ == "__main__":
    unittest.main()
