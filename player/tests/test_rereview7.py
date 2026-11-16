"""The review of 06358ca5 (docs/reviews/AI_PLAYER_AP1_REREVIEW7_REVIEW.md on chatgpt/review-ai-player-ap1-rereview7
@ 718a9512): one finding, the class P1, built on the review's own reproducer. Those tests fail on 06358ca5.

P1  a brain from before the update was still running, and took the request this version's `brain next` had put in
    the inbox. By its own rule a request without `lost` means the last relay is back: it settled that relay's
    four calls and saved the ledger. This version refused its answer, and the calls were gone all the same: 34
    calls in a minute, 24 in the world lane

The older brain in the first class is the 442a6311 package's own `brain run`, in a process of its own; those
tests skip where the repository's history lacks the commit. The second class needs no history: it holds this
version to the one fact that keeps its requests from every earlier brain, the name they are published under.
"""
import fnmatch
import glob
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from player import brain, calls as K, config as C, relay
from player.tests import support
from player.tests.test_relay import token_of
from player.tests.test_rereview2 import most_in_a_minute
from player.tests.test_rereview3 import Client
from player.tests.test_rereview4 import Killed
from player.tests.test_rereview5 import BEFORE, held, ledger, the_package_at, update

OLD_RESIDENT = r'''
import io, json, os
from unittest.mock import patch
from player import brain, relay
from player.tests import support
from player.tests.support import Rig, user
from player.tests import support
from player.tests.test_relay import token_of
r = Rig(); r.world.absorb([user()._replace(at=r.t)]); r.world.save()
def nxt(token=None):
    out = io.StringIO(); brain.next_batch(r.dir, token, out, lambda _: None)
    return out.getvalue().splitlines()
with patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(r.dir, "none"),
                             "TNR_PLAYER_FIGHTS": os.path.join(r.dir, "fights")}):
    a = token_of(nxt(token_of(nxt()[0]))[-1])       # relay A is given a batch, and does not come back
    real = brain.Brain
    def home(live):
        b = real(live)                              # said once the resident has the lock and its world model
        print(json.dumps({"live": r.dir, "holder": a, "calls": len(b.world["budget"]["calls"])}), flush=True)
        return b
    with patch.object(brain, "Brain", home):
        brain.run(r.dir)                            # that version's own resident loop, until it is ended
'''
EVERY_EARLIER_BRAIN_READS = "req-*.json"
"""player/relay.py `pending_requests`, in every commit of the player before this one."""


def requests(live):
    """Every request file in the inbox, under any name."""
    return sorted(glob.glob(os.path.join(live, "inbox", "*req-*.json")))


def loose(live):
    """The calls the saved ledger holds for batches (the minute held after an update is `update`)."""
    return held(live)


class P1AnOlderBrainIsStillRunning(unittest.TestCase):
    """The review's script. Relay A has four calls of the old version's and has not come back. That version's
    brain is running and holds the lock. Then this version's `brain next` starts a replacement."""

    VERSION = BEFORE                    # the commit whose `brain run` is the older brain: here 442a6311

    def setUp(self):
        root = the_package_at(self.VERSION)
        if root is None:
            self.skipTest(f"the repository's history does not hold {self.VERSION[:8]}")
        self.old = subprocess.Popen([sys.executable, "-W", "ignore", "-c", OLD_RESIDENT], cwd=root, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    env={**os.environ, "PYTHONPATH": root})
        self.addCleanup(self.the_old_brain_is_ended)
        made = json.loads(self.old.stdout.readline())
        self.live, self.real, self.waited, self.taken = support.bare(made["live"]), brain.Brain, False, None
        self.assertEqual(made["calls"], 4)
        self.assertIsNone(brain._lock(self.live))                           # it is home: the lock is its own
        # the review's one setting: with the player paused, no batch of this version's is in the minute beside
        # the four calls. It is no word about relay A.
        relay.write(os.path.join(self.live, "control.json"), support.and_bare({"version": 1, "paused": True}))
        self.now, self.rounds, lock = [time.time()], 0, brain._lock

        def counted(live, wait=False):
            """The test's clock moves only when `brain next` waits: one that goes round without waiting would
            never end, so it is stopped here."""
            self.rounds += 1
            self.assertLess(self.rounds, 2000, "`brain next` goes round and round without waiting")
            return lock(live, wait)
        for p in (mock.patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_PLAYER_LIVE": self.live,
                                               "TNR_TRANSCRIPT": os.path.join(self.live, "none"),
                                               "TNR_PLAYER_FIGHTS": tempfile.mkdtemp(prefix="player-fights-")}),
                  mock.patch.object(time, "time", lambda: self.now[0]),
                  mock.patch.object(brain, "_lock", counted),
                  mock.patch.object(brain, "Brain", lambda live: self.real(live, clock=lambda: self.now[0]))):
            p.start()
            self.addCleanup(p.stop)
        self.before = ledger(self.live)
        self.assertEqual([c[2:] for c in self.before], [["out"]] * 4)

    def the_old_brain_is_ended(self):
        if self.old.poll() is None:
            self.old.terminate()
            try:
                self.old.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.old.kill()
                self.old.wait()
        for pipe in (self.old.stdout, self.old.stderr):
            pipe.close()

    def next(self, token=None, meanwhile=None):
        """This version's `brain next`. Its wait for a brain runs on the test's clock. The first time it waits
        with its request in the inbox, the older brain is given two real seconds to take that request (it looks
        every 50 ms), and then `meanwhile` happens."""
        def sleep(t):
            if not self.waited and requests(self.live):
                self.waited, until = True, time.monotonic() + 2.0
                while time.monotonic() < until and requests(self.live):
                    time.sleep(0.02)
                self.taken = not requests(self.live)
                if meanwhile:
                    meanwhile()
            self.now[0], self.rounds = self.now[0] + max(t, 1.0), 0
        out = io.StringIO()
        brain.next_batch(self.live, token, out, sleep)
        return out.getvalue().splitlines()

    def most(self, lane, batches):
        """The review's count: relay A goes on with its four calls a minute later, beside this version's batches.
        The minute held for the update is let go here, as of a minute before: the count is of what the four
        calls themselves hold."""
        clock = [self.now[0] + 62]
        budget, made = self.real(self.live, clock=lambda: clock[0]).budget, [clock[0]] * 4
        self.assertEqual(budget.ended(update(self.live)[0][3], clock[0] - 61), C.CALL_LIMIT)
        for _ in range(batches):
            steps, _ = budget.pace([K.user(), K.user()], lane)
            for s in steps:
                if "wait" in s:
                    clock[0] += s["wait"]
                else:
                    made.append(clock[0])
                    clock[0] += .01
        return most_in_a_minute(made)

    def held_and_inside_the_limits(self):
        kept = loose(self.live)
        self.assertEqual((len(kept), {c[5] for c in kept}), (4, {None}))    # held, for a relay not on record
        self.assertEqual(len(update(self.live)), C.CALL_LIMIT)              # and the update's minute beside them
        self.assertLessEqual(self.most("recovery", 15), C.CALL_LIMIT)       # was 34
        self.assertLessEqual(self.most("world", 10), C.WORLD_CAP)           # was 24

    def test_a_replacement_asks_while_it_is_home(self):
        token = token_of(self.next()[0])
        lines = self.next(token)
        self.assertIs(self.taken, False)                                    # was: taken, by that brain's rules
        self.assertEqual(ledger(self.live), self.before)                    # was: all four settled
        self.assertEqual(lines, [relay.next_line(token)])                   # no batch: the relay is to ask again
        self.the_old_brain_is_ended()
        self.next(token)                                                    # and now this version's brain answers
        self.held_and_inside_the_limits()

    def test_it_is_ended_while_this_version_waits(self):
        """The moment the lock is free, the `brain next` that is waiting answers its own request."""
        token, seen, handle = token_of(self.next()[0]), [], self.real.handle
        with mock.patch.object(self.real, "handle", lambda *a, **k: seen.append(1) or handle(*a, **k)):
            self.next(token, meanwhile=self.the_old_brain_is_ended)
        self.assertEqual((self.taken, seen), (False, [1]))
        self.held_and_inside_the_limits()

    def test_it_is_ended_first(self):
        """The control: the order the operator's page asks for."""
        self.the_old_brain_is_ended()
        self.next(token_of(self.next()[0]))
        self.held_and_inside_the_limits()


class P1ARequestIsPublishedWhereOnlyThisProtocolLooks(Client):
    """What needs no older package. Every brain before this version looks for `req-*.json` in the inbox, and
    for nothing else there."""

    def asks_and_is_not_answered(self, token):
        """This version's `brain next` asks while a brain that does not answer holds the lock. Returns what it
        printed, and what the inbox held while it waited."""
        home, held, real = brain._lock(self.rig.dir), [], brain._await
        self.addCleanup(home.close)

        def sleep(_):
            held.append(sorted(os.listdir(os.path.join(self.rig.dir, "inbox"))))
        with mock.patch.object(brain, "_await", lambda *a: real(*a, limit=0.2)):
            lines = self.next(token, sleep)
        home.close()
        return lines, held[0]

    def a_request_of_this_version(self):
        """One that `brain next` wrote and no brain has had: (its file, what it says)."""
        a = self.new_relay_with_a_batch()
        with mock.patch.object(brain, "_await", side_effect=Killed):
            with self.assertRaises(Killed):
                self.next(a)
        (path,) = relay.pending_requests(self.rig.dir)
        return path, relay.read(path)

    def outbox(self):
        return glob.glob(os.path.join(self.rig.dir, "outbox", "*"))

    def test_no_earlier_brain_finds_this_versions_request(self):
        a = self.new_relay_with_a_batch()
        before = self.saved()
        lines, inbox = self.asks_and_is_not_answered(a)
        (name,) = inbox                                                     # one request waits,
        self.assertFalse(fnmatch.fnmatch(name, EVERY_EARLIER_BRAIN_READS))  # was: under the name they read
        self.assertTrue(relay.is_request(name) and f"p{relay.PROTOCOL}-" in name)   # under its protocol's own
        self.assertEqual((lines, self.saved()), ([relay.next_line(a)], before))

    def test_under_the_old_name_nothing_is_answered_whatever_it_says(self):
        path, ask = self.a_request_of_this_version()
        before = self.saved()["budget"]["calls"]
        os.unlink(path)
        old = os.path.join(self.rig.dir, "inbox", f"req-{ask['seq']:08d}-{ask['id']}.json")   # as 06358ca5 named it
        relay.write(old, ask)
        self.assertEqual(relay.pending_requests(self.rig.dir), [old])
        brain.run(self.rig.dir, forever=False)
        self.assertEqual((requests(self.rig.dir), self.outbox()), ([], []))  # removed, and not answered
        self.assertEqual(self.saved()["budget"]["calls"], before)
        relay.write(path, ask)                                              # the same words under this name
        brain.run(self.rig.dir, forever=False)
        self.assertEqual((requests(self.rig.dir), len(self.outbox())), ([], 1))

    def test_another_protocols_request_is_not_this_brains_to_open(self):
        path, ask = self.a_request_of_this_version()
        os.unlink(path)
        for number in (relay.PROTOCOL + 1, relay.PROTOCOL - 1):             # the next version's, and the one before's
            other = os.path.join(self.rig.dir, "inbox", f"p{number}-req-{ask['seq']:08d}-{ask['id']}.json")
            relay.write(other, dict(ask, protocol=number))
            before = self.saved()
            brain.run(self.rig.dir, forever=False)
            self.assertEqual((requests(self.rig.dir), self.outbox(), self.saved()), ([other], [], before), number)
            os.unlink(other)

    def test_with_nothing_to_answer_brain_next_waits_and_starts_one_brain(self):
        """Not from the review: nobody is home, the request is gone and no answer has come (a brain dropped
        it). `brain next` went round without a pause until its time was up, and started a brain every round."""
        live, seq, rid = self.rig.dir, 5, "ab" * 4
        waits = []
        with mock.patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "0"}), \
                mock.patch.object(brain.subprocess, "Popen") as started:
            got = brain._await(live, seq, rid, relay.request_path(live, seq, rid),
                               lambda t: waits.append(t) or time.sleep(0.01), limit=0.3)
        self.assertIsNone(got)
        self.assertEqual((set(waits), started.call_count), ({C.BRAIN_WAIT}, 1))   # was: no wait, a brain a round
        self.assertLess(len(waits), 40)

    def test_what_a_dead_brain_next_left_is_swept_under_any_name(self):
        a = self.new_relay_with_a_batch()
        for name in ("req-00000009.json", "req-00000009-abcdabcd.json", f"p{relay.PROTOCOL}-req-00000009-abcdabcd.json",
                     f"p{relay.PROTOCOL + 1}-req-00000009-abcdabcd.json", f"p{relay.PROTOCOL - 1}-req-00000009-abcdabcd.json"):
            relay.write(os.path.join(self.rig.dir, "inbox", name), {"seq": 9, "relay": "dead01", "results": []})
        seen, handle = [], brain.Brain.handle
        with mock.patch.object(brain.Brain, "handle", lambda *a_, **k: seen.append(1) or handle(*a_, **k)):
            self.next(a)
        self.assertEqual((seen, requests(self.rig.dir)), ([1], []))         # one request answered: this one's own


if __name__ == "__main__":
    unittest.main()
