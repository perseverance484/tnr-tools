"""The review of 426a9fba (docs/reviews/AI_PLAYER_AP1_REREVIEW5_REVIEW.md on chatgpt/review-ai-player-ap1-rereview5
@ 8dc89799): two findings, the classes M1 and M2, each built on the review's own reproducer. Those tests fail on
426a9fba.

M1  a brain that came home answered a request an older version had left in the inbox. That request says nothing
    of who holds the last batch, and saying nothing was read as "its relay is back"
M2  `brain stopped 1` did not name the batch that the listing shows as `batch 1`

The files under fixtures/upgrade_442a6311 were written by the 442a6311 package itself (made.json says how): a
relay with four calls in hand, its replacement's request in the inbox, that replacement's `brain next` dead.
One test here has that package make them again, when the repository's history holds the commit.
"""
import contextlib
import glob
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from player import brain, calls as K, config as C, relay
from player.budget import UPDATE
from player.tests.support import Rig, user
from player.tests.test_relay import token_of
from player.tests.test_rereview2 import most_in_a_minute
from player.tests.test_rereview3 import Client

RECORDED = os.path.join(os.path.dirname(__file__), "fixtures", "upgrade_442a6311")
BEFORE = "442a63119d2fa3fe033877bedc86f5df8cd9be00"
OLD_PROGRAM = r'''
import io, json, os
from unittest.mock import patch
from player import brain, relay
from player.tests.support import Rig, user
from player.tests.test_relay import token_of
r = Rig(); r.world.absorb([user()._replace(at=r.t)]); r.world.save()
def nxt(token=None):
    out = io.StringIO(); brain.next_batch(r.dir, token, out, lambda _: None)
    return out.getvalue().splitlines()
with patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(r.dir, "missing"),
                             "TNR_PLAYER_FIGHTS": os.path.join(r.dir, "fights")}):
    a = token_of(nxt(token_of(nxt()[0]))[-1])
    n = len(relay.read(os.path.join(r.dir, "world.json"))["budget"]["calls"])
    b = token_of(nxt()[0])
    with patch.object(brain, "_await", side_effect=RuntimeError("killed after request write")):
        try:
            nxt(b)
        except RuntimeError:
            pass
    print(json.dumps({"live": r.dir, "holder": a, "calls": n}))
'''


class Killed(Exception):
    pass


def recorded(folder=RECORDED):
    """A live folder as the version before left it, from the recorded files. Returns (the folder, what was made)."""
    live = tempfile.mkdtemp(prefix="player-upgrade-")
    os.makedirs(os.path.join(live, "inbox"))
    for name in os.listdir(folder):
        if name.startswith("req-"):
            shutil.copy(os.path.join(folder, name), os.path.join(live, "inbox", name))
        elif name != "made.json":
            shutil.copy(os.path.join(folder, name), os.path.join(live, name))
    with open(os.path.join(folder, "made.json"), encoding="utf8") as f:
        return live, json.load(f)


PACKAGE = []


def the_package_before():
    """The 442a6311 package out of the repository's history, in a folder of its own; None without it."""
    def git(*args):
        return subprocess.run(["git", *args], cwd=C.ROOT, capture_output=True)
    if not PACKAGE:
        PACKAGE.append(None)
        if not git("cat-file", "-e", BEFORE + "^{commit}").returncode:
            root = tempfile.mkdtemp(prefix="player-before-")
            for name in git("ls-tree", "-r", "--name-only", BEFORE, "--", "player").stdout.decode().splitlines():
                path = os.path.join(root, name)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as f:
                    f.write(git("show", f"{BEFORE}:{name}").stdout)
            for name in ("state", "data", "docs", "scripts", "harness", ".claude"):
                os.symlink(os.path.join(C.ROOT, name), os.path.join(root, name), target_is_directory=True)
            PACKAGE[0] = root
    return PACKAGE[0]


def by_the_version_before(program=OLD_PROGRAM, *args):
    """What that package makes when it runs a program (the default: the state of the review of 426a9fba), as
    the program's last line says: (the live folder, what was made). None without the package."""
    root = the_package_before()
    if root is None:
        return None
    out = subprocess.run([sys.executable, "-W", "ignore", "-c", program, *args], cwd=root, capture_output=True,
                         text=True, env={**os.environ, "PYTHONPATH": root})
    made = json.loads(out.stdout.strip().splitlines()[-1])
    return made["live"], made


def ledger(live):
    return relay.read(os.path.join(live, "world.json"))["budget"]["calls"]


def held(live):
    """The calls the saved ledger holds for batches: every loose call but the minute that is held after an
    update, which stands for no batch (Budget.taken_over; review of 29797ba0)."""
    return [c for c in ledger(live) if c[2:3] == ["loose"] and not str(c[3]).startswith(UPDATE)]


def update(live):
    """The minute held for the relays from before the update: [] when there is none."""
    return [c for c in ledger(live) if c[2:3] == ["loose"] and str(c[3]).startswith(UPDATE)]


def events(live, kind):
    with open(os.path.join(live, "events.jsonl"), encoding="utf8") as f:
        return [e for e in map(json.loads, f) if e["kind"] == kind]


class M1AnOlderRequestSaysNothingOfTheBatch(unittest.TestCase):
    """The request the version before left says `lost` and has no `held`. The resident brain, starting, answered
    whatever was in the inbox; no `held` was the sign of a test driving the brain itself, and meant "back". So
    the four calls of a relay that had not come back were settled: 34 calls in a minute, 24 in the world lane."""

    def setUp(self):
        # every brain these tests start keeps its fights in a folder of its own: nothing here can write into
        # the repository's, whatever the code under test does with an old request
        env = mock.patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": "/nowhere/none.jsonl",
                                           "TNR_PLAYER_FIGHTS": tempfile.mkdtemp(prefix="player-fights-")})
        env.start()
        self.addCleanup(env.stop)

    def next(self, live, token=None):
        out = io.StringIO()
        with mock.patch.dict(os.environ, {"TNR_PLAYER_LIVE": live}):
            brain.next_batch(live, token, out, lambda _: None)
        return out.getvalue().splitlines()

    def a_brain_comes_home(self, live, made):
        """The review's script: the resident brain starts, with the old request waiting."""
        (old,) = relay.pending_requests(live)
        self.assertTrue(relay.read(old)["lost"] and "held" not in relay.read(old))
        brain.run(live, forever=False)
        self.assertEqual(relay.pending_requests(live), [])                  # the old request is removed,
        self.assertEqual(glob.glob(os.path.join(live, "outbox", "*")), [])  # not answered,
        out = [c[2:] for c in ledger(live) if c not in update(live)]
        self.assertEqual(out, [["out"]] * made["calls"])                    # and nothing is settled by it
        self.assertIn("not a request of this version", events(live, "finding")[-1]["text"])

    def test_the_files_the_version_before_left(self):
        live, made = recorded()
        self.a_brain_comes_home(live, made)                                 # was: all four settled
        new = token_of(self.next(live, token_of(self.next(live)[0]))[-1])   # a relay of this version asks
        mine = held(live)
        self.assertEqual((len(mine), {c[5] for c in mine}), (made["calls"], {None}))   # held, for nobody on record
        self.assertEqual(self.next(live, made["holder"]), [brain.SUPERSEDED])   # the old relay coming back
        new = token_of(self.next(live, new)[-1])
        self.assertEqual(len(held(live)), made["calls"])                    # proves nothing
        said = io.StringIO()
        with mock.patch.dict(os.environ, {"TNR_PLAYER_LIVE": live}), contextlib.redirect_stdout(said):
            brain.main(["stopped", "1"])                                    # the operator names it as it is listed
        self.assertEqual(json.loads(said.getvalue())["stopped"], ["batch 1"])
        self.next(live, new)
        self.assertEqual((held(live), len(update(live))), ([], C.CALL_LIMIT))   # that batch, and not the update's minute

    def test_the_version_before_itself(self):
        state = by_the_version_before()
        if state is None:
            self.skipTest("the repository's history does not hold 442a6311")
        live, made = state
        (old,) = relay.pending_requests(live)
        with open(glob.glob(os.path.join(RECORDED, "req-*.json"))[0], encoding="utf8") as f:
            self.assertEqual(sorted(relay.read(old)), sorted(json.load(f)))    # the recorded files are true to it
        self.a_brain_comes_home(live, made)
        self.next(live, token_of(self.next(live)[0]))
        self.assertEqual(len(held(live)), made["calls"])

    def test_the_old_relay_going_on_stays_under_the_limits(self):
        """The review's count. The player is paused, as in its script, so that no batch of this version's is in
        the minute beside the old relay's four calls. The minute held for the update is let go here, as of a
        minute before, so that the count is of what the old ledger's own four calls hold."""
        for lane, batches, limit in (("recovery", 15, C.CALL_LIMIT), ("world", 10, C.WORLD_CAP)):
            live, made = recorded()
            relay.write(os.path.join(live, "control.json"), {"version": 1, "paused": True})
            brain.run(live, forever=False)
            self.next(live, token_of(self.next(live)[0]))                   # a relay of this version asks
            now = [time.time() + 62]
            budget = brain.Brain(live, clock=lambda: now[0]).budget
            self.assertEqual(budget.ended(update(live)[0][3], now[0] - 61), C.CALL_LIMIT)
            done = [now[0]] * made["calls"]                                 # the old relay makes its four calls
            for _ in range(batches):
                steps, _ = budget.pace([K.user(), K.user()], lane)
                for s in steps:
                    if "wait" in s:
                        now[0] += s["wait"]
                    else:
                        done.append(now[0])
                        now[0] += .01
            self.assertLessEqual(most_in_a_minute(done), limit, lane)       # was 34, and 24

    def test_what_is_no_request_at_all_is_removed_too(self):
        rig = Rig()
        rig.world.save()
        for n, content in enumerate(([1, 2], {}, {"seq": 3, "relay": "aa11bb", "results": []}, "text"), 1):
            relay.write(relay.request_path(rig.dir, n), content)
        brain.run(rig.dir, forever=False)
        self.assertEqual(relay.pending_requests(rig.dir), [])
        self.assertEqual(glob.glob(os.path.join(rig.dir, "outbox", "*")), [])
        self.assertEqual(len([e for e in rig.events("finding") if e.get("about") == "relay"]), 4)

    def test_lost_in_an_older_word_is_never_back(self):
        """Whoever hands the brain such a request, by whatever way."""
        rig = Rig()
        rig.tick(user())
        rig.world["budget"]["calls"] = []
        n = len(rig.calls(rig.tick(user())))
        path = relay.request_path(rig.dir, 9)
        with open(glob.glob(os.path.join(RECORDED, "req-*.json"))[0], encoding="utf8") as f:
            relay.write(path, json.load(f))
        rig.t += 5
        brain.answer(rig.brain, rig.dir, path)
        held = [c for c in rig.world["budget"]["calls"] if c[2:3] == ["loose"]]
        self.assertEqual(len(held), n)                                      # was 0: settled, as if its relay were back


class M1TheRequestsOfThisVersionAreStillAnswered(Client):
    def test_by_a_brain_that_comes_home(self):
        a = self.new_relay_with_a_batch()
        with mock.patch.object(brain, "_await", side_effect=Killed):
            with self.assertRaises(Killed):
                self.next(a)                                                # its `brain next` dies; the request waits
        (request,) = relay.pending_requests(self.rig.dir)
        self.assertTrue(all(k in relay.read(request) for k in brain.REQUEST))
        brain.run(self.rig.dir, forever=False)
        self.assertEqual(relay.pending_requests(self.rig.dir), [])
        self.assertEqual(len(glob.glob(os.path.join(self.rig.dir, "outbox", "batch-*.json"))), 1)   # answered
        self.assertEqual(self.saved()["relay"]["answered"]["relay"], a.split("-")[0])
        seen, handle = [], brain.Brain.handle
        with mock.patch.object(brain.Brain, "handle", lambda *a_, **k: seen.append(1) or handle(*a_, **k)):
            again = self.next(a)                                            # the relay asks the same again:
        self.assertEqual((seen, bool(self.calls(again))), ([], True))       # the answer it had, run once
        self.assertEqual(self.loose(), [])

    def test_the_brain_never_paces_over_a_batch_it_has_not_placed(self):
        """Should the ledger's own step fail, the batch that is out is held; it is not taken to be back."""
        a = self.new_relay_with_a_batch()
        n = len(self.client()["calls"])
        with mock.patch.object(brain.Brain, "_ledger", side_effect=RuntimeError("the ledger's step failed")):
            self.next(a)
        self.assertEqual(len(self.loose()), n)                              # was: settled by the next pacing


class M1AClientFileOfAnyShapeDoesNotStopBrainNext(Client):
    def test_whatever_an_older_file_holds(self):
        """Not from the review: the other file an older version leaves. A batch waiting in it with no id, a
        number that is no number, a file that is a list. Each as that version left it, and with this version's
        protocol number on the file (it is then read, and what is not in this version's shape is dropped)."""
        path = os.path.join(self.rig.dir, "client.json")
        shapes = ([1, 2], "text", {"seq": "7", "relay": "aa11bb", "token": "aa11bb-7"},
                  {"seq": 3, "relay": "aa11bb", "token": "aa11bb-3", "calls": 5,
                   "pending": {"seq": 4, "steps": [{"call": "old.call", "input": {}, "select": []}],
                               "stop": None, "ready_at": time.time()}})
        for content in shapes + tuple(dict(c, protocol=relay.PROTOCOL) for c in shapes if isinstance(c, dict)):
            relay.write(path, content)
            told = self.next("aa11bb-3")                                    # a relay from before asks
            self.assertNotIn("old.call", "".join(told), content)            # a batch this code did not store
            first = self.next()                                             # is never printed; and a new relay
            self.assertTrue(self.calls(self.next(token_of(first[0]))), content)   # starts and gets its batch
            self.assertEqual(brain.put(self.rig.dir, "aa11bb-3", "1", "{}"), 1)


class M2ABatchIsNamedAsItIsListed(unittest.TestCase):
    """The batch an older version left is known by a number. The listing shows `batch 1`; the command line gives
    the operator's `1` as text, and text was not the number, so that one batch could not be let go by name."""

    def setUp(self):
        """The review's script: a batch with a number for an id, and another relay's batch that is still running."""
        self.rig = rig = Rig()
        rig.world["budget"]["calls"] = [[rig.t, "world", "loose", 1, rig.t, None],
                                        [rig.t, "world", "loose", "other", rig.t, "still-running-2"]]
        rig.world.save()

    def cli(self, *names):
        out = io.StringIO()
        with mock.patch.dict(os.environ, {"TNR_PLAYER_LIVE": self.rig.dir}), contextlib.redirect_stdout(out):
            brain.main(["stopped", *names])
        return json.loads(out.getvalue())

    def queued(self):
        return (relay.read(os.path.join(self.rig.dir, "client.json")) or {}).get("ended") or []

    def test_the_number_typed_is_the_number_kept(self):
        self.assertEqual(self.cli()["still_held"], ["batch 1", "still-running-2"])
        said = self.cli("1")
        self.assertEqual(said, {"stopped": ["batch 1"], "all": False, "not_held": [],     # was: not_held ["1"]
                                "still_held": ["still-running-2"]})
        self.assertEqual([row[0] for row in self.queued()], [1])            # said of that batch, by the id it has
        rig = self.rig
        rig.brain.evidence(brain._who(os.path.join(rig.dir, "client.json")))
        calls = rig.world["budget"]["calls"]
        self.assertEqual((calls[0][2:], calls[1][2]), ([], "loose"))        # that one batch, and no other
        self.assertEqual(rig.brain.budget.used(), 2)
        rig.t += 61
        self.assertEqual(rig.brain.budget.used(), 1)                        # counted a minute more, then gone

    def test_a_name_nobody_has_reaches_nothing(self):
        for name in ("2", "11", "batch 1", "", "None", "still-running"):
            self.assertEqual(self.cli(name)["not_held"], [name], name)
        self.assertEqual(self.queued(), [])

    def test_the_other_ways_to_name_a_batch_still_work(self):
        self.assertEqual(self.cli("other")["stopped"], ["still-running-2"])     # by its id
        self.setUp()
        self.assertEqual(self.cli("still-running-2")["stopped"], ["still-running-2"])   # by its relay's token
        self.setUp()
        self.assertEqual(sorted(self.cli("all")["stopped"]), ["batch 1", "still-running-2"])


if __name__ == "__main__":
    unittest.main()
