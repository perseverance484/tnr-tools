"""The review of c412de4d (docs/reviews/AI_PLAYER_AP1_REREVIEW9_REVIEW.md on chatgpt/review-ai-player-ap1-rereview9
@ e7e4c0f6): one finding, the class H1, built on the review's own scripts. Those tests fail on c412de4d.

H1  c412de4d holds every call after it takes over another version's ledger, until the operator has spoken. It
    brought that rule in and kept the protocol's number, so everything its predecessor 29797ba0 had made without
    the rule passed for its own: a batch waiting in client.json was printed eight seconds later with no word
    said, the batch in a receipt was given again, and a brain of 29797ba0 that was still running answered this
    version's request with calls. Each of them went round the hold, also when the hold was saved already

The files under fixtures/upgrade_29797ba0_pending and upgrade_29797ba0_receipt were written by the 29797ba0
package itself (made.json says how). Tests here have that package make them again, and run its `brain run`,
when the repository's history holds the commit.

What is required: nothing the predecessor left reaches a relay; no call until the operator has spoken, and none
for a minute after; what the predecessor's relay may still hold stays held; results a brain has taken in are not
taken in twice; and what this version made is delivered as before, with no hold.
"""
import io
import json
import os
import subprocess
import sys
import unittest
from unittest import mock

from player import brain, config as C, relay
from player.tests.support import user
from player.tests.test_relay import token_of
from player.tests.test_rereview5 import by_the_version_at, held, recorded, the_package_at, update
from player.tests.test_rereview6 import calls_of
from player.tests import test_rereview7
from player.tests.test_rereview8 import AfterAnUpdate, hold

PREDECESSOR = "29797ba0f769152381e71710f812605be9e0bfea"
"""The version c412de4d was reviewed against: the last one without the hold."""
REVIEWED = "c412de4df43baf4f11fbd817efb0f7ae95c08226"
"""The version the review was of: it has the hold, under the predecessor's number. It is the version before this."""
EARLIER = ("06358ca539372cae12d41b086a465719f403aba7", PREDECESSOR, REVIEWED,
           "7cf7d73c5cb235801b66e4b4763cb63e1bc7b14e", "e4a267cd1ab5ff85c3b2399bab713f2870da6ccb",
           "ce1be6e98eb39550e79806c5c8f9da87f67fa4eb")
"""Versions whose records carry a number, and whose rules are not this version's."""
FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")
PENDING, RECEIPT = (os.path.join(FIXTURES, f"upgrade_29797ba0_{what}") for what in ("pending", "receipt"))
OLD_PROGRAM = r'''
import io, json, os, sys, time
from unittest.mock import patch
from player import brain, relay
from player.tests.support import Rig, user
from player.tests.test_relay import token_of
r = Rig(); r.world.absorb([user()._replace(at=r.t)]); r.world.save()
now, real, write, client = [r.t], brain.Brain, relay.write, os.path.join(r.dir, "client.json")
class Killed(Exception):
    pass
def dies(path, obj):
    """`brain next` is killed over the batch it was given: just after it wrote it into client.json ("pending"),
    or just before ("receipt": then the brain's receipt is all there is of that batch)."""
    batch = path == client and obj.get("pending")
    if not (batch and sys.argv[1] == "receipt"):
        write(path, obj)
    if batch:
        raise Killed
def nxt(token=None):
    out = io.StringIO()
    brain.next_batch(r.dir, token, out, lambda t: now.__setitem__(0, now[0] + max(t, 0)))
    return out.getvalue().splitlines()
with patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(r.dir, "none"),
                             "TNR_PLAYER_FIGHTS": os.path.join(r.dir, "fights")}), \
        patch.object(time, "time", lambda: now[0]), \
        patch.object(brain, "Brain", lambda live: real(live, clock=lambda: now[0])):
    token = token_of(nxt()[0])                      # a relay starts,
    with patch.object(relay, "write", dies):
        try:
            nxt(token)                              # and its `brain next` dies over its first batch
        except Killed:
            pass
    done = relay.read(os.path.join(r.dir, "world.json"))["relay"]["answered"]
    print(json.dumps({"live": r.dir, "now": now[0], "relay": token, "protocol": relay.PROTOCOL,
                      "batch": [s["call"] for s in done["batch"]["steps"] if "call" in s]}))
'''
OLD_ASLEEP = r'''
import io, json, os, subprocess, sys, time
from unittest.mock import patch
from player import brain, relay
from player.tests.support import Rig, user
from player.tests.test_relay import token_of
r = Rig(); r.world.absorb([user()._replace(at=r.t)]); r.world.save()
new_root, said = sys.argv[1], []
env = {"TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(r.dir, "none"),
       "TNR_PLAYER_FIGHTS": os.path.join(r.dir, "fights"), "TNR_PLAYER_LIVE": r.dir}
def sleep(t):
    """The wait `brain next` spends for the brain before it prints: meanwhile the code is updated, and a relay
    of the new version starts (its `brain next` runs from the new code's folder)."""
    if t > 1 and not said:
        with open(os.path.join(r.dir, "control.json"), "w") as f:      # (the director's word for a relay without
            json.dump({"version": 0, "relay_without_hooks": True}, f)  # hooks, which the new code asks for)
        out = subprocess.run([sys.executable, "-W", "ignore", "-m", "player.brain", "next"], cwd=new_root,
                             capture_output=True, text=True, env={**os.environ, **env, "PYTHONPATH": new_root})
        said.append(out.stdout.strip().splitlines())
def nxt(token=None):
    out = io.StringIO()
    brain.next_batch(r.dir, token, out, sleep)
    return out.getvalue().splitlines()
with patch.dict(os.environ, env):
    lines = nxt(token_of(nxt()[0]))                 # its first batch: it wakes from the wait with the old code
    done = relay.read(os.path.join(r.dir, "world.json"))["relay"]["answered"]
    print(json.dumps({"live": r.dir, "now": time.time(), "old": lines, "new": said[0],
                      "batch": [s["call"] for s in done["batch"]["steps"] if "call" in s]}))
'''


def by_this_version(*args):
    """The same program, run by the package under test: (the live folder, what was made)."""
    out = subprocess.run([sys.executable, "-W", "ignore", "-c", OLD_PROGRAM, *args], cwd=C.ROOT, text=True,
                         capture_output=True, env={**os.environ, "PYTHONPATH": C.ROOT})
    made = json.loads(out.stdout.strip().splitlines()[-1])
    return made["live"], made


def client(live):
    return relay.read(os.path.join(live, "client.json"))


def saved(live):
    return relay.read(os.path.join(live, "world.json"))


class WhatAVersionBeforeLeft(AfterAnUpdate):
    """A relay of an earlier version started, and its `brain next` died over its first batch: four calls, made
    by that version's rules. Then this version. No test of its own."""

    def start(self, state):
        super().start(state)
        self.OLD_CALLS = len(self.made["batch"])
        self.assertEqual(self.OLD_CALLS, 4)

    def a_new_relay_asks(self, seconds=0):
        """A relay of this version starts and asks, for that long: every line it was given."""
        token, lines, t0 = token_of(self.next()[0]), [], self.now[0]
        while not lines or self.now[0] < t0 + seconds:
            lines.append(self.next(token))
            token = token_of(lines[-1][-1])
        return [x for batch in lines for x in batch]

    def held_for_the_predecessors_relay(self):
        """The calls of the batch it made are in the ledger still, for a relay that is not on record."""
        kept = held(self.live)
        self.assertEqual((len(kept), {c[5] for c in kept}), (self.OLD_CALLS, {None}))

    def nothing_it_made_is_delivered(self, commit):
        """The package of that commit makes the state, with the batch waiting and with the batch in the receipt:
        none of it reaches a relay, no call goes until the word, and none for a minute after."""
        for mode in ("pending", "receipt"):
            state = by_the_version_at(commit, OLD_PROGRAM, mode)
            if state is None:
                self.skipTest(f"the repository's history does not hold {commit[:8]}")
            self.start(state)
            number = saved(self.live)["budget"].get("protocol")
            self.assertTrue(type(number) is int and number != relay.PROTOCOL, number)   # its ledger has its number
            if mode == "receipt":
                self.assertEqual(self.next(self.made["relay"]), [brain.SUPERSEDED])
            lines = self.a_new_relay_asks(seconds=120)
            self.assertEqual(calls_of(lines), [], mode)
            self.held_for_the_predecessors_relay()
            self.says("all")
            spoken = self.now[0]
            self.asks_until_a_call(token_of(lines[-1]))
            self.assertGreaterEqual(self.printed[0][0], spoken + 60, mode)
            self.inside_the_limits(spoken - .1)


class H1WhatThePredecessorLeft(WhatAVersionBeforeLeft):
    """The review's script, mode by mode, with 29797ba0 as the earlier version."""

    # ---- the batch that was waiting in client.json
    def nothing_of_the_waiting_batch_is_sent(self, state, late=0):
        self.start(state)
        waiting = client(self.live)["pending"]
        self.assertEqual([s["call"] for s in waiting["steps"] if "call" in s], self.made["batch"])
        self.assertLess(waiting["ready_at"] - self.now[0], 10)              # it was to go within seconds
        self.now[0] += late
        self.assertEqual(calls_of(self.a_new_relay_asks(seconds=120)), [])  # was: its four calls, with no word
        self.assertIsNone(client(self.live)["pending"])
        self.held_for_the_predecessors_relay()
        self.assertEqual(len(update(self.live)), C.CALL_LIMIT)
        self.inside_the_limits(self.now[0] - .1)

    def test_its_waiting_batch_is_not_printed(self):
        self.nothing_of_the_waiting_batch_is_sent(recorded(PENDING))

    def test_nor_once_it_has_grown_too_old_to_send(self):
        self.nothing_of_the_waiting_batch_is_sent(recorded(PENDING), late=C.STALE_OUTBOX + 11)

    def test_nor_when_a_brain_of_this_version_has_the_ledger_already(self):
        """The review's `installed`: the hold was saved, and the batch was printed past it."""
        self.start(recorded(PENDING))
        self.real(self.live, clock=lambda: self.now[0])._save()
        self.assertTrue(relay.ours(saved(self.live)["budget"]))
        batch = hold(self.live)
        self.assertEqual(calls_of(self.a_new_relay_asks(seconds=120)), [])  # was: four calls
        self.assertEqual((hold(self.live), len(update(self.live))), (batch, C.CALL_LIMIT))   # the one hold, whole

    def test_the_word_and_then_a_minute(self):
        """The review's `ack`: the word is said before any relay of this version has asked."""
        self.start(recorded(PENDING))
        listed = self.says()["still_held"]
        self.assertEqual(len(listed), 1)
        self.assertEqual(self.says("all")["stopped"], listed)
        spoken = self.now[0]
        lines, _ = self.asks_until_a_call(token_of(self.next()[0]))
        self.assertTrue(calls_of(lines))
        self.assertGreaterEqual(self.printed[0][0], spoken + 60)            # was: eight seconds after
        self.assertLess(self.printed[0][0], spoken + 75)
        self.assertEqual(update(self.live), [])
        self.held_for_the_predecessors_relay()                              # its batch is held beside, until the
        self.inside_the_limits(spoken - .1)                                 # operator speaks of that too
        token = token_of(lines[-1])
        self.assertEqual(len(self.says("all")["stopped"]), 1)
        self.next(token)
        self.assertEqual(held(self.live), [])

    # ---- the batch in the receipt
    def test_its_receipt_is_not_given_again(self):
        self.start(recorded(RECEIPT))
        done = saved(self.live)["relay"]["answered"]
        self.assertEqual([s["call"] for s in done["batch"]["steps"] if "call" in s], self.made["batch"])
        self.assertIsNone(client(self.live).get("pending"))                 # `brain next` never had it down
        lines = self.next(self.made["relay"])                               # that relay asks again
        self.assertEqual(lines, [brain.SUPERSEDED])                         # was: the receipt's four calls
        self.assertEqual(calls_of(self.a_new_relay_asks(seconds=120)), [])
        self.held_for_the_predecessors_relay()
        self.assertEqual(len(update(self.live)), C.CALL_LIMIT)
        self.inside_the_limits(self.now[0] - .1)

    def test_the_request_it_answered_is_not_run_again_by_this_brain(self):
        """Should a request of this version ever name that relay and number: the results it brings went into
        the world model with the predecessor's answer, and are not taken in twice; the batch is not given."""
        self.start(recorded(RECEIPT))
        was = saved(self.live)
        done = was["relay"]["answered"]
        ask = {"protocol": relay.PROTOCOL, "seq": done["seq"], "id": done["id"], "relay": done["relay"],
               "results": relay.pack([user(sector=77)._replace(at=self.now[0])]), "usage": {}, "strays": 0,
               "at": self.now[0], "clock": "ours", "held": None, "gone": [], "ended": [], "unprinted": []}
        relay.write(relay.request_path(self.live, ask["seq"], ask["id"]), ask)
        seen, handle = [], self.real.handle
        with mock.patch.object(self.real, "handle", lambda *a, **k: seen.append(1) or handle(*a, **k)):
            brain.run(self.live, forever=False)
        answer = relay.read(relay.batch_path(self.live, ask["seq"], ask["id"]))
        self.assertEqual((seen, [s for s in answer["steps"] if "call" in s]), ([], []))
        self.assertEqual(saved(self.live), was)                             # sector 77 was not taken in: nothing was
        self.assertEqual(len(self.says()["still_held"]), 1)                 # and the update's minute is held still

    # ---- the predecessor's package itself
    def test_a_brain_next_of_the_predecessor_that_wakes_after_the_update_prints_nothing(self):
        """Not from the review. A `brain next` of 29797ba0 is in its wait, with its batch, when the code is
        updated and a relay of this version starts. It wakes with the old code."""
        state = by_the_version_at(PREDECESSOR, OLD_ASLEEP, C.ROOT)
        if state is None:
            self.skipTest("the repository's history does not hold 29797ba0")
        self.start(state)
        self.assertEqual(self.made["old"], [brain.SUPERSEDED])              # the file is no longer one it reads
        token = token_of(self.made["new"][0])                               # this version's relay goes on:
        for _ in range(20):
            lines = self.next(token)
            token = token_of(lines[-1])
            self.assertEqual(calls_of(lines), [])
        self.held_for_the_predecessors_relay()
        self.assertEqual(len(update(self.live)), C.CALL_LIMIT)

    def test_the_version_that_was_reviewed_is_a_version_before_too(self):
        """c412de4d made the same state under the number it shared with 29797ba0."""
        self.nothing_it_made_is_delivered(REVIEWED)

    def test_the_predecessor_itself(self):
        for mode, kept in (("pending", PENDING), ("receipt", RECEIPT)):
            state = by_the_version_at(PREDECESSOR, OLD_PROGRAM, mode)
            if state is None:
                self.skipTest("the repository's history does not hold 29797ba0")
            for name in ("client.json", "world.json"):                      # the recorded files are true to it
                was, now = relay.read(os.path.join(recorded(kept)[0], name)), relay.read(os.path.join(state[0], name))
                self.assertEqual(sorted(was), sorted(now), (mode, name))
                self.assertEqual(sorted(was.get("pending") or {}), sorted(now.get("pending") or {}), mode)
                self.assertEqual((was.get("protocol"), was.get("budget", {}).get("protocol")),
                                 (now.get("protocol"), now.get("budget", {}).get("protocol")), (mode, name))
            self.start(state)
            if mode == "receipt":
                self.assertEqual(self.next(self.made["relay"]), [brain.SUPERSEDED])
            lines = self.a_new_relay_asks(seconds=120)
            self.assertEqual(calls_of(lines), [], mode)                     # was: four calls
            self.says("all")
            spoken = self.now[0]
            self.asks_until_a_call(token_of(lines[-1]))
            self.assertGreaterEqual(self.printed[0][0], spoken + 60, mode)
            self.inside_the_limits(spoken - .1)


class H1ThePredecessorsBrainIsStillRunning(test_rereview7.P1AnOlderBrainIsStillRunning):
    """The review's second script: the resident brain of 29797ba0 is home when this version's relay asks. It
    read this version's request and answered it with calls, and the answer was taken. The three tests are the
    ones written for a brain of 442a6311, with this brain in its place."""
    VERSION = PREDECESSOR


class H1TheReviewedVersionsBrainIsStillRunning(test_rereview7.P1AnOlderBrainIsStillRunning):
    """The same three tests against the resident brain of c412de4d."""
    VERSION = REVIEWED


class H1WhatThisVersionMadeIsDeliveredAsBefore(AfterAnUpdate):
    """The controls. The same program, run by this version: the batch it leaves is this version's own."""

    def start(self, state):
        super().start(state)
        self.assertEqual(self.made["protocol"], relay.PROTOCOL)
        self.assertEqual(self.says()["still_held"], [])                     # nothing is held: no update was made

    def test_its_waiting_batch_is_printed_when_its_wait_is_over(self):
        self.start(by_this_version("pending"))
        waiting, t0 = client(self.live)["pending"], self.now[0]
        lines = self.next(token_of(self.next()[0]))                         # a relay that takes over is given it
        self.assertEqual(calls_of(lines), self.made["batch"])
        self.assertEqual(self.now[0], max(t0, waiting["ready_at"]))         # after its own wait, and no longer
        self.assertEqual(update(self.live), [])

    def test_its_receipt_answers_the_same_request_with_the_same_batch(self):
        self.start(by_this_version("receipt"))
        seen, handle = [], self.real.handle
        with mock.patch.object(self.real, "handle", lambda *a, **k: seen.append(1) or handle(*a, **k)):
            lines = self.next(self.made["relay"])                           # the same relay asks again
        self.assertEqual((calls_of(lines), seen), (self.made["batch"], []))  # the batch made then; nothing run twice
        self.assertEqual(update(self.live), [])

    def test_a_brain_of_this_version_that_is_home_answers(self):
        self.start(by_this_version("pending"))
        token = token_of(self.next(token_of(self.next()[0]))[-1])
        home = brain._lock(self.live)                                       # a resident brain has the lock,
        self.addCleanup(home.close)
        resident, real = self.real(self.live, clock=lambda: self.now[0]), brain._await

        def sleep(t):                                                       # and looks at the inbox while
            for path in relay.pending_requests(self.live):                 # `brain next` waits
                brain.serve(resident, self.live, path)
            self.now[0] += max(t, 0)
        out = io.StringIO()
        with mock.patch.object(brain, "_await", lambda *a: real(*a, limit=5.0)):
            brain.next_batch(self.live, token, out, sleep)
        self.assertEqual(token_of(out.getvalue().splitlines()[-1]).split("-")[1], "2")   # its answer is taken
        self.assertEqual(update(self.live), [])


class H1TheNumber(unittest.TestCase):
    def test_what_the_predecessor_recorded_has_another_number(self):
        for folder in (PENDING, RECEIPT):
            live, made = recorded(folder)
            numbers = {made["protocol"], client(live)["protocol"], saved(live)["relay"]["answered"]["protocol"]}
            self.assertEqual(numbers, {1})
            self.assertNotIn("protocol", saved(live)["budget"])             # its ledger carried no number yet
            self.assertNotIn(relay.PROTOCOL, numbers)                       # was: the same number, 1

    def test_no_earlier_version_has_this_versions_number(self):
        for commit in EARLIER:
            root = the_package_at(commit)
            if root is None:
                self.skipTest(f"the repository's history does not hold {commit[:8]}")
            out = subprocess.run([sys.executable, "-c", "from player import relay; print(relay.PROTOCOL)"], cwd=root,
                                 capture_output=True, text=True, env={**os.environ, "PYTHONPATH": root})
            self.assertNotEqual(int(out.stdout), relay.PROTOCOL, commit)    # was: c412de4d had 29797ba0's


if __name__ == "__main__":
    unittest.main()
