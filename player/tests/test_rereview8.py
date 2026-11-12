"""The review of 29797ba0 (docs/reviews/AI_PLAYER_AP1_REREVIEW8_REVIEW.md on chatgpt/review-ai-player-ap1-rereview8
@ 56dfb24d). It found no new defect, and required what the last handoff had left open as its known limit 2: the
class Q1, built on the review's own script. Those tests fail on 29797ba0.

Q1  a ledger that another version of the player kept cannot say what is out. 442a6311 lets a held call go after
    fifteen minutes: relay A has four calls and never comes back, that version counts again a quarter of an hour
    later, and its ledger is empty. This version took the empty ledger at its word and sent calls at once: 34 in
    a minute, 24 in the world lane. The operator's word did not help, for there was nothing in the ledger for it
    to name

The files under fixtures/upgrade_442a6311_forgotten were written by the 442a6311 package itself (made.json says
how). One test here has that package make them again, when the repository's history holds the commit.

What is required: after such a takeover no call is sent until the operator has said that the relays from before
the update are stopped, and none for a minute after that word. The word names this one takeover.
"""
import io
import json
import os
import tempfile
import time
import unittest
from unittest import mock

from player import brain, calls as K, config as C, relay
from player.budget import UPDATE
from player.tests.support import Rig, battle_read, fixture, log_read, user
from player.tests.test_relay import token_of
from player.tests.test_rereview2 import most_in_a_minute
from player.tests.test_rereview3 import Client
from player.tests.test_rereview4 import Killed, dies_before_the_receipt
from player.tests.test_rereview5 import by_the_version_before, held, ledger, recorded, update
from player.tests.test_rereview6 import calls_of

RECORDED = os.path.join(os.path.dirname(__file__), "fixtures", "upgrade_442a6311_forgotten")
BRAIN = brain.Brain                     # the class itself: a test here puts a clock on it more than once
OLD_PROGRAM = r'''
import io, json, os, time
from unittest.mock import patch
from player import brain, relay
from player.tests.support import Rig, user
from player.tests.test_relay import token_of
r = Rig(); r.world.absorb([user()._replace(at=r.t)]); r.world.save()
now, real = [r.t], brain.Brain
def nxt(token=None):
    out = io.StringIO()
    brain.next_batch(r.dir, token, out, lambda t: now.__setitem__(0, now[0] + max(t, 0)))
    return out.getvalue().splitlines()
with patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(r.dir, "none"),
                             "TNR_PLAYER_FIGHTS": os.path.join(r.dir, "fights")}), \
        patch.object(time, "time", lambda: now[0]), \
        patch.object(brain, "Brain", lambda live: real(live, clock=lambda: now[0])):
    a = token_of(nxt(token_of(nxt()[0]))[-1])       # relay A is given four calls, and does not come back
    b = token_of(nxt(token_of(nxt()[0]))[-1])       # relay B replaces it
    relay.write(os.path.join(r.dir, "control.json"), {"version": 1, "paused": True})
    b = token_of(nxt(b)[-1])
    now[0] += 1000                                  # a quarter of an hour and more:
    nxt(b)                                          # that version counts again, and lets A's calls go
    print(json.dumps({"live": r.dir, "now": now[0], "holder": a,
                      "ledger": relay.read(os.path.join(r.dir, "world.json"))["budget"]["calls"]}))
'''


def hold(live):
    """The id of the minute that is held for the relays from before the update."""
    (batch,) = {c[3] for c in update(live)}
    return batch


def first_call_in(out):
    """Seconds from the moment a batch is made until its first call can go; None when it has no call."""
    wait = out["hold"]
    for s in out["steps"]:
        if "call" in s:
            return wait
        wait += s.get("wait", 0)
    return None


class Q1TheLedgerOfAnotherVersion(unittest.TestCase):
    """The review's script: the old version has let relay A's four calls go, and has ended. Then this version."""

    def start(self, state):
        self.live, self.made = state
        self.assertEqual(ledger(self.live), [])                             # A never came back; nothing says so
        self.now, self.real = [self.made["now"]], BRAIN
        relay.write(os.path.join(self.live, "control.json"), {"version": 2, "paused": False})
        for p in (mock.patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_PLAYER_LIVE": self.live,
                                               "TNR_TRANSCRIPT": os.path.join(self.live, "none"),
                                               "TNR_PLAYER_FIGHTS": tempfile.mkdtemp(prefix="player-fights-")}),
                  mock.patch.object(time, "time", lambda: self.now[0]),
                  mock.patch.object(brain, "Brain", lambda live: self.real(live, clock=lambda: self.now[0]))):
            p.start()
            self.addCleanup(p.stop)
        self.printed = []                                                   # (when, how many calls) of this version

    def next(self, token=None):
        out = io.StringIO()
        brain.next_batch(self.live, token, out, lambda t: self.now.__setitem__(0, self.now[0] + max(0, t)))
        lines = out.getvalue().splitlines()
        if calls_of(lines):
            self.printed.append((self.now[0], len(calls_of(lines))))
        return lines

    def says(self, *names):
        out = io.StringIO()
        brain.stopped(self.live, list(names), out)
        return json.loads(out.getvalue())

    def most(self, lane, batches, last_old_call):
        """The review's count: relay A makes its four calls at `last_old_call`; this version's calls so far are
        counted when they were printed, and then it paces `batches` more."""
        clock = [self.now[0]]
        budget = self.real(self.live, clock=lambda: clock[0]).budget
        made = [last_old_call] * 4 + [at for at, n in self.printed for _ in range(n)]
        for _ in range(batches):
            steps, _ = budget.pace([K.user(), K.user()], lane)
            for s in steps:
                if "wait" in s:
                    clock[0] += s["wait"]
                else:
                    made.append(clock[0])
                    clock[0] += .01
        return most_in_a_minute(made)

    def inside_the_limits(self, last_old_call):
        self.assertLessEqual(self.most("recovery", 15, last_old_call), C.CALL_LIMIT)    # was 34
        self.assertLessEqual(self.most("world", 10, last_old_call), C.WORLD_CAP)       # was 24

    def asks_until_a_call(self, token, limit=300):
        """The relay asks until it is given a call, for at most `limit` seconds: (the lines, the token)."""
        t0, lines = self.now[0], []
        while not calls_of(lines) and self.now[0] < t0 + limit:
            lines = self.next(token)
            token = token_of(lines[-1])
        return lines, token

    # ---- no word
    def nothing_is_sent(self, state):
        self.start(state)
        lines = self.next(token_of(self.next()[0]))
        self.assertEqual(calls_of(lines), [])                               # was: four calls, at once
        self.assertEqual((held(self.live), len(update(self.live))), ([], C.CALL_LIMIT))   # a minute's calls held
        self.inside_the_limits(self.now[0] - .1)
        return token_of(lines[-1])

    def test_no_call_is_sent_until_the_operator_has_spoken(self):
        token = self.nothing_is_sent(recorded(RECORDED))
        t0, asks = self.now[0], 0
        while self.now[0] < t0 + 1200:                                      # however long it takes
            lines = self.next(token)
            token, asks = token_of(lines[-1]), asks + 1
            self.assertEqual(calls_of(lines), [])
        self.assertLessEqual(asks, 1200 / C.RATE_BACKOFF + 1)               # and the relay is made to wait
        status = relay.read(os.path.join(self.live, "status.json"))["budget"]["held"]
        self.assertEqual([(h["relay"], h["batch"], h["calls"]) for h in status], [(None, hold(self.live), C.CALL_LIMIT)])
        with open(os.path.join(self.live, "events.jsonl"), encoding="utf8") as f:
            said = [e["text"] for e in map(json.loads, f) if e["kind"] == "stall" and "another version" in e["text"]]
        self.assertEqual(len(said), 1)                                      # said once, with what to do about it
        self.assertIn(f"stopped {hold(self.live)}", said[0])

    def test_the_version_before_itself(self):
        state = by_the_version_before(OLD_PROGRAM)
        if state is None:
            self.skipTest("the repository's history does not hold 442a6311")
        kept, _ = recorded(RECORDED)
        for name in ("client.json", "world.json"):                          # the recorded files are true to it
            was, now = relay.read(os.path.join(kept, name)), relay.read(os.path.join(state[0], name))
            self.assertEqual(sorted(was), sorted(now), name)
        self.assertEqual(relay.read(os.path.join(kept, "world.json"))["budget"], {"batch": 4, "calls": []})
        self.assertEqual(relay.read(os.path.join(state[0], "world.json"))["budget"], {"batch": 4, "calls": []})
        token = self.nothing_is_sent(state)
        self.says("all")
        spoken = self.now[0]
        self.asks_until_a_call(token)
        self.assertGreaterEqual(self.printed[0][0], spoken + 60)
        self.inside_the_limits(spoken - .1)

    # ---- the word, and the minute after it
    def test_calls_start_a_minute_after_the_word(self):
        token = self.nothing_is_sent(recorded(RECORDED))
        self.now[0] += 200
        listed = self.says()                                                # asking changes nothing
        self.assertEqual(listed["still_held"], [f"the relays from before the update ({hold(self.live)})"])
        self.assertEqual(self.next(token)[:-1], [])
        said = self.says("all")                                             # relay A is stopped: it made its last
        spoken = self.now[0]                                                # calls just before this
        self.assertEqual((said["stopped"], said["still_held"]), (listed["still_held"], []))
        lines, token = self.asks_until_a_call(token)
        self.assertTrue(calls_of(lines))
        self.assertGreaterEqual(self.printed[0][0], spoken + 60)            # not one call inside that minute
        self.assertLess(self.printed[0][0], spoken + 75)
        self.assertEqual(update(self.live), [])
        self.inside_the_limits(spoken - .1)

    def test_the_word_can_be_said_before_any_relay_of_this_version_has_asked(self):
        """The review's two other cases. The hold is named from the file that is taken over, so the listing
        shows it, and the word can name it, before a brain of this version has started."""
        for quiet in (0, 60):
            self.start(recorded(RECORDED))
            was = relay.read(os.path.join(self.live, "world.json"))
            listed = self.says()
            self.assertEqual(len(listed["still_held"]), 1)
            self.assertEqual(relay.read(os.path.join(self.live, "world.json")), was)   # nothing is written by it
            said, spoken = self.says("all"), self.now[0]
            self.assertEqual(said["stopped"], listed["still_held"])
            self.now[0] += quiet
            lines, _ = self.asks_until_a_call(token_of(self.next()[0]))
            self.assertTrue(calls_of(lines), quiet)
            self.assertGreaterEqual(self.printed[0][0], spoken + 60, quiet)  # was: at once (34 and 24 with no quiet)
            self.inside_the_limits(spoken - .1)

    def test_the_word_for_one_old_batch_is_not_the_word_for_the_update(self):
        token = self.nothing_is_sent(recorded(RECORDED))
        self.assertEqual(self.says("4")["not_held"], ["4"])                 # the old ledger's last batch: not held
        self.assertEqual(self.says(self.made["holder"])["not_held"], [self.made["holder"]])   # nor is relay A known
        for _ in range(20):
            lines = self.next(token)
            token = token_of(lines[-1])
            self.assertEqual(calls_of(lines), [])
        self.assertEqual(len(update(self.live)), C.CALL_LIMIT)


class Q1TheHoldIsThisTakeoversAndLasts(Client):
    """What needs no older package: a ledger of this version's, with its number taken off and its rows dropped,
    is to this version what the review's file is."""

    def another_versions_ledger(self, calls=()):
        world = self.saved()
        world["budget"] = {"batch": world["budget"].get("batch"), "calls": list(calls)}
        relay.write(os.path.join(self.rig.dir, "world.json"), world)

    def asks(self, token, wait=None):
        seen, handle = [], brain.Brain.handle
        with mock.patch.object(brain.Brain, "handle", lambda *a, **k: seen.append(1) or handle(*a, **k)):
            lines = self.next(token, *([wait] if wait else []))
        return lines, seen

    def test_a_ledger_this_version_kept_is_taken_as_it_stands(self):
        """The control: an ordinary restart. Every request here is answered by a brain started for it."""
        a = self.new_relay_with_a_batch()
        for _ in range(3):
            lines = self.next(a)
            self.assertTrue(self.calls(lines))
            a = token_of(lines[-1])
        self.assertEqual(update(self.rig.dir), [])

    def test_a_first_start_has_nothing_to_take_over(self):
        """The other control: a live folder that is new."""
        first = brain.Brain(tempfile.mkdtemp(prefix="player-first-"))
        self.assertEqual(first.budget.loose(), [])
        self.assertTrue(first.budget.pace([K.user()], "world")[0])

    def test_a_ledger_says_whose_it_is_from_the_first_thing_saved(self):
        self.new_relay_with_a_batch()
        kept = self.saved()["budget"]
        self.assertEqual((type(kept["protocol"]), kept["protocol"]), (int, relay.PROTOCOL))
        for other in ("absent", 0, relay.PROTOCOL + 1, str(relay.PROTOCOL), float(relay.PROTOCOL), True, None):
            self.another_versions_ledger()
            world = self.saved()
            if other != "absent":
                world["budget"]["protocol"] = other
            relay.write(os.path.join(self.rig.dir, "world.json"), world)
            self.assertEqual(len(brain.Brain(self.rig.dir).budget.loose()), 1, other)   # each of them: another's

    def test_the_hold_outlasts_a_brain_a_retry_and_a_new_relay(self):
        a = self.new_relay_with_a_batch()
        self.another_versions_ledger()
        lines = self.next(a)                                                # a brain takes the ledger over
        a, batch = token_of(lines[-1]), hold(self.rig.dir)
        self.assertEqual(self.calls(lines), [])
        with dies_before_the_receipt(self.rig):
            with self.assertRaises(Killed):
                self.next(a)                                                # its `brain next` dies with the answer
        for token in (a, None):                                             # the same request again, then a new relay
            lines, _ = self.asks(token or token_of(self.next()[0]))
            self.assertEqual(self.calls(lines), [])
            self.assertEqual((hold(self.rig.dir), len(update(self.rig.dir))), (batch, C.CALL_LIMIT))   # one hold

    def test_a_brain_that_ends_before_it_saves_leaves_the_ledger_and_the_next_holds_the_same(self):
        self.new_relay_with_a_batch()
        self.another_versions_ledger()
        was = self.saved()
        ids = [{c[3] for c in brain.Brain(self.rig.dir).world["budget"]["calls"] if c[2:3] == ["loose"]} for _ in range(2)]
        self.assertEqual(self.saved(), was)                                 # looking at a ledger writes nothing
        self.assertEqual((ids[0], len(ids[0])), (ids[1], 1))

    def test_the_word_is_for_this_takeover_and_no_other(self):
        a = self.new_relay_with_a_batch()
        self.another_versions_ledger()
        a = token_of(self.next(a)[-1])
        first = hold(self.rig.dir)
        word = [first, time.time(), None, "stopped"]
        self.assertEqual(self.stopped("all")["stopped"], [f"the relays from before the update ({first})"])
        self.next(a)                                                        # the brain has the word
        self.assertEqual(update(self.rig.dir), [])
        self.another_versions_ledger()                                      # and then the ledger is another's again
        a = self.client()["token"]
        self.next(a)
        second = hold(self.rig.dir)
        self.assertNotEqual(first, second)
        state = self.client()
        state["ended"] = [word]                                             # the word of the first, said once more
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        self.assertEqual(self.stopped(first)["not_held"], [first])
        self.assertEqual(self.calls(self.next(self.client()["token"])), [])
        self.assertEqual((hold(self.rig.dir), len(update(self.rig.dir))), (second, C.CALL_LIMIT))

    def test_the_word_does_not_count_from_before_the_ledger_was_last_written(self):
        """A word that claims to be older than the file it is about is taken as said now."""
        a = self.new_relay_with_a_batch()
        self.another_versions_ledger()
        a = token_of(self.next(a)[-1])
        state = self.client()
        state["ended"] = [[hold(self.rig.dir), os.path.getmtime(os.path.join(self.rig.dir, "world.json")) - 3600, None,
                           "stopped"]]
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        waits = []
        lines, _ = self.asks(a, waits.append)
        after = [c[0] for c in self.saved()["budget"]["calls"] if c[1] == "update"]
        self.assertEqual(len(after), C.CALL_LIMIT)                          # counted, all of them,
        self.assertGreater(min(after), time.time() - 30)                    # from now: not from an hour ago
        self.assertTrue(not self.calls(lines) or max(waits) >= 55)          # so no call inside the minute

    def test_a_ledger_that_cannot_be_read_is_another_versions(self):
        for text in ("{ not a world model", "[1, 2]", ""):
            self.setUp()
            self.new_relay_with_a_batch()
            with open(os.path.join(self.rig.dir, "world.json"), "w", encoding="utf8") as f:
                f.write(text)
            listed = self.stopped()["still_held"]
            self.assertEqual(len(listed), 1, text)                          # it is listed before a brain has it,
            self.assertEqual(self.calls(self.next(self.client()["token"])), [], text)
            self.assertEqual(f"the relays from before the update ({hold(self.rig.dir)})", listed[0])   # by one id

    def test_known_holds_are_kept_beside_it_and_let_go_one_by_one(self):
        a = self.new_relay_with_a_batch()
        n = len(self.client()["calls"])
        b = self.new_relay_with_a_batch()                                   # A is replaced with its batch in hand
        self.assertEqual(len(self.loose(a)), n)
        self.another_versions_ledger(self.saved()["budget"]["calls"])       # the rows stay; the number goes
        b = token_of(self.next(b)[-1])
        self.assertEqual((len([c for c in self.loose(a) if c[1] != "update"]), len(update(self.rig.dir))),
                         (n, C.CALL_LIMIT))
        self.stopped(a)                                                     # A is stopped: its batch, and no more
        b = token_of(self.next(b)[-1])
        self.assertEqual((held(self.rig.dir), len(update(self.rig.dir))), ([], C.CALL_LIMIT))


class Q1NoLaneIsLeftOpen(unittest.TestCase):
    def test_not_even_a_turn_of_mine_goes_out(self):
        rig = Rig()
        battle, ents = fixture()
        out = rig.tick(user("BATTLE", bid="B1"))                            # a fight is on when the update comes
        self.assertEqual(rig.calls(out)[:1], ["combat.getBattle"])
        rig.world.save()
        world = relay.read(os.path.join(rig.dir, "world.json"))
        world["budget"] = {"batch": None, "calls": []}                      # as another version would have left it
        relay.write(os.path.join(rig.dir, "world.json"), world)
        rig.new_brain()
        out = rig.tick(battle_read("B1", battle), log_read("B1", ents))     # my turn
        self.assertEqual(rig.calls(out), [])                                # was: the turn's actions
        self.assertGreaterEqual(out["hold"], C.RATE_BACKOFF if not rig.world.in_battle() else 1.0)
        (batch,) = {c[3] for c in rig.world["budget"]["calls"] if c[2:3] == ["loose"]}
        self.assertTrue(batch.startswith(UPDATE))
        spoken = rig.t
        rig.brain.evidence({"ended": [[batch, spoken, None, "stopped"]]})   # the operator's word
        out = rig.tick(battle_read("B1", battle), log_read("B1", ents), dt=5)
        gap = first_call_in(out)
        self.assertTrue(gap is None or rig.t + gap >= spoken + 60, out)     # and nothing inside the minute after it


if __name__ == "__main__":
    unittest.main()
