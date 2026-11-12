"""The review of 60a28a84 (docs/reviews/AI_PLAYER_AP1_REREVIEW6_REVIEW.md on chatgpt/review-ai-player-ap1-rereview6
@ edd8b469): one finding, the class N1, built on the review's own reproducer. Those tests fail on 60a28a84.

N1  a batch the version before had made and not yet printed was printed by this version. It had every field a
    batch of this version has, and it had been admitted under a rule this version does not keep (a held call
    let go after fifteen minutes): 22 calls in the world lane in a minute

The files under fixtures/upgrade_442a6311_pending were written by the 442a6311 package itself (made.json says
how): seven relays replaced with their batches in hand, an eighth whose `brain next` was killed during the
brain-side wait, after the batch was stored. One test here has that package make them again, when the
repository's history holds the commit.

The other classes are not from the review. What makes a record this version's own is the protocol number it
carries (relay.PROTOCOL), and they hold that to every record the two sides keep for each other, and that a
record that does carry it is delivered as before.
"""
import glob
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from player import brain, config as C, relay
from player.tests.support import user
from player.tests.test_relay import token_of
from player.tests.test_rereview3 import Client
from player.tests.test_rereview4 import Killed, dies_before_the_receipt
from player.tests.test_rereview5 import (BEFORE, by_the_version_before, held, ledger, recorded, the_package_before,
                                         update)

RECORDED = os.path.join(os.path.dirname(__file__), "fixtures", "upgrade_442a6311_pending")
OLD_PROGRAM = r'''
import io, json, os, sys, time
from unittest.mock import patch
from player import brain, relay
from player.tests.support import Rig, user
from player.tests.test_relay import token_of
r = Rig(); r.world.absorb([user()._replace(at=r.t)]); r.world.save()
now, real, printed, woke = [r.t], brain.Brain, [], []
go = sys.argv[1] if len(sys.argv) > 1 else None
class Died(Exception):
    pass
def made():
    return json.dumps({"live": r.dir, "now": now[0], "relays": len(printed) + 1, "printed": printed, "woke": woke})
def sleep(t):
    if t > 100 and not go:
        raise Died                      # killed in the brain-side wait, with the batch stored and not printed
    if t > 100:                         # or not killed: it says where it stands, and wakes when it is told to
        with open(go + ".tmp", "w") as f:
            f.write(made())
        os.replace(go + ".tmp", go + ".made")
        while not os.path.exists(go):
            time.sleep(0.02)
        woke.append(True)
    now[0] += t
def nxt(token=None):
    out = io.StringIO(); brain.next_batch(r.dir, token, out, sleep)
    return out.getvalue().splitlines()
with patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(r.dir, "none"),
                             "TNR_PLAYER_FIGHTS": os.path.join(r.dir, "fights")}), \
        patch.object(time, "time", lambda: now[0]), \
        patch.object(brain, "Brain", lambda live: real(live, clock=lambda: now[0])):
    for i in range(15):
        token = token_of(nxt()[0])      # a relay replaces the one before, which keeps its batch
        try:
            lines = nxt(token)
        except Died:
            break
        if woke:
            woke[:] = lines             # what the one that waited printed when it woke
            break
        printed.append(lines)
    print(made())
'''
OLD_BRAIN = r'''
import json, sys
from player import brain, relay
live = sys.argv[1]
home = brain.Brain(live)                # the brain of the version before, still running after the upgrade
n = 0
for path in relay.pending_requests(live):
    brain.answer(home, live, path); n += 1
print(json.dumps({"live": live, "answered": n}))
'''


def made_at(lines, start):
    """When a relay that starts on these lines at `start` makes each call. It does them in order, and sleeps
    the waits between them."""
    t, made = start, []
    for line in lines:
        step = json.loads(line) if line.startswith("{") else {}
        if "call" in step:
            made.append(t)
            t += .001
        elif "sleep(" in step.get("bash", ""):
            t += float(re.search(r"sleep\((.*?)\)", step["bash"])[1])
    return made


def calls_of(lines):
    return [json.loads(x)["call"] for x in lines if x.startswith("{") and "call" in json.loads(x)]


def loose(live):
    """The calls the saved ledger holds for batches (the minute held after an update is `update`)."""
    return held(live)


STAMPS = ("absent", 0, relay.PROTOCOL - 1, relay.PROTOCOL + 1, str(relay.PROTOCOL), float(relay.PROTOCOL), True,
          None)
"""What a record of another maker has where this version's number goes: the version before this one had the
number before this one (review of c412de4d)."""


def stamped(record, stamp):
    return {k: v for k, v in dict(record, protocol=stamp).items() if (k, v) != ("protocol", "absent")}


class N1ABatchTheVersionBeforeLeftWaiting(unittest.TestCase):
    """The version before let a held call go after fifteen minutes, and had a batch made on that footing waiting
    in client.json when its `brain next` died. This version read it as a batch of its own: it waited for the
    old time and printed it, and the brain was never asked. The old relays, still about, had twenty calls in
    that minute."""

    def start(self, state):
        """This version, on the folder the version before left and on the clock it stopped at."""
        self.live, self.made = state
        self.now, real = [self.made["now"]], brain.Brain
        for p in (mock.patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_PLAYER_LIVE": self.live,
                                               "TNR_TRANSCRIPT": os.path.join(self.live, "none"),
                                               "TNR_PLAYER_FIGHTS": tempfile.mkdtemp(prefix="player-fights-")}),
                  mock.patch.object(time, "time", lambda: self.now[0]),
                  mock.patch.object(brain, "Brain", lambda live: real(live, clock=lambda: self.now[0]))):
            p.start()
            self.addCleanup(p.stop)
        self.left = relay.read(os.path.join(self.live, "client.json"))
        self.waiting = [x["call"] for x in self.left["pending"]["steps"] if "call" in x]
        self.batch = relay.read(os.path.join(self.live, "world.json"))["budget"]["batch"]   # as its brain names it
        out = [c for c in ledger(self.live) if c[2:3] == ["out"]]
        self.assertEqual((len(loose(self.live)), len(out), len(self.waiting)), (21, 2, 2))
        self.assertGreater(self.left["pending"]["ready_at"], self.now[0])   # it waits; it has not grown old

    def next(self, token=None):
        out = io.StringIO()
        brain.next_batch(self.live, token, out, lambda t: self.now.__setitem__(0, self.now[0] + max(0, t)))
        return out.getvalue().splitlines()

    def in_the_minute(self, lines):
        """The review's count: each old relay goes on half a second before these lines are printed. How many
        calls the minute up to then holds, with the ones printed now."""
        at = self.now[0]
        old = [t for batch in self.made["printed"] for t in made_at(batch, at - .5)]
        before = sum(at - 60 < t <= at for t in old)
        self.assertEqual(before, C.WORLD_CAP)                               # the lane is full of them already
        return before + len(calls_of(lines))

    def a_replacement_asks(self, state):
        """The review's script."""
        self.start(state)
        with mock.patch.object(brain, "serve", wraps=brain.serve) as served:
            lines = self.next(token_of(self.next()[0]))
        self.assertEqual(served.call_count, 1)                              # was 0: the brain was not asked
        self.assertEqual(calls_of(lines), [])                               # was: the two calls of the old batch
        self.assertLessEqual(self.in_the_minute(lines), C.WORLD_CAP)        # was 22
        kept = loose(self.live)
        self.assertEqual(len(kept), 23)                                     # the 21 that were held are held,
        self.assertEqual([c[5] for c in kept if c[3] == self.batch], [None, None])   # and the two that waited,
        self.assertEqual(len(update(self.live)), C.CALL_LIMIT)              # for nobody on record; and a minute
        return lines                                                        # for what that ledger may not say

    def test_the_files_the_version_before_left(self):
        lines = self.a_replacement_asks(recorded(RECORDED))
        token, asks, t0 = token_of(lines[-1]), 0, self.now[0]
        while self.now[0] < t0 + 1200:                                      # no length of time lets them go,
            lines = self.next(token)
            token, asks = token_of(lines[-1]), asks + 1
            self.assertEqual(calls_of(lines), [])
        self.assertLessEqual(asks, 1200 / C.RATE_BACKOFF + 1)               # and the relay is made to wait
        self.assertEqual(len(loose(self.live)), 23)
        said = io.StringIO()
        brain.stopped(self.live, ["all"], said)                             # the operator's word is the way out
        self.assertEqual(len(json.loads(said.getvalue())["stopped"]), 9)    # eight batches, and the update's minute
        spoken = self.now[0]
        while not calls_of(lines) and self.now[0] < spoken + 300:
            lines = self.next(token)
            token = token_of(lines[-1])
        self.assertTrue(calls_of(lines))
        self.assertGreaterEqual(self.now[0], spoken + 60)                   # a minute after it, not before
        self.assertEqual((loose(self.live), update(self.live)), ([], []))

    def test_the_version_before_itself(self):
        state = by_the_version_before(OLD_PROGRAM)
        if state is None:
            self.skipTest("the repository's history does not hold 442a6311")
        kept, _ = recorded(RECORDED)
        for name in ("client.json", "world.json"):                          # the recorded files are true to it
            was, now = relay.read(os.path.join(kept, name)), relay.read(os.path.join(state[0], name))
            self.assertEqual(sorted(was), sorted(now), name)
        was, now = relay.read(os.path.join(kept, "client.json")), relay.read(os.path.join(state[0], "client.json"))
        self.assertEqual({k: type(v) for k, v in was["pending"].items()},
                         {k: type(v) for k, v in now["pending"].items()})
        self.assertEqual([x.get("call") for x in was["pending"]["steps"]],
                         [x.get("call") for x in now["pending"]["steps"]])
        self.assertEqual([(len(c), c[1], c[2:3]) for c in ledger(kept)], [(len(c), c[1], c[2:3]) for c in ledger(state[0])])
        self.a_replacement_asks(state)

    def test_the_relay_it_was_made_for_asks_again(self):
        """The line whose `brain next` died is run again by the same relay. The file that names it is not this
        version's: the relay is told to stop, and has none of the batch."""
        self.start(recorded(RECORDED))
        before = (self.left, ledger(self.live))
        with mock.patch.object(brain, "serve", wraps=brain.serve) as served:
            self.assertEqual(self.next(self.left["token"]), [brain.SUPERSEDED])   # was: the old batch
        self.assertEqual(served.call_count, 0)
        self.assertEqual((relay.read(os.path.join(self.live, "client.json")), ledger(self.live)), before)
        lines = self.next(token_of(self.next()[0]))                         # and the relay started in its place
        self.assertEqual((calls_of(lines), len(loose(self.live))), ([], 23))

    def test_the_operator_names_one_old_batch_before_any_relay_of_this_version_has_asked(self):
        """The selective release, on these files: by the number the old ledger knows the batch by."""
        self.start(recorded(RECORDED))
        listed, said = io.StringIO(), io.StringIO()
        brain.stopped(self.live, [], listed)
        listed = json.loads(listed.getvalue())["still_held"]
        self.assertEqual(listed[:-1], [f"batch {n}" for n in range(1, 8)])
        self.assertTrue(listed[-1].startswith("the relays from before the update (update-"))
        self.assertEqual(relay.read(os.path.join(self.live, "client.json")), self.left)   # listing wrote nothing
        brain.stopped(self.live, ["3"], said)
        self.assertEqual(json.loads(said.getvalue())["stopped"], ["batch 3"])
        lines = self.next(token_of(self.next()[0]))
        kept = loose(self.live)
        self.assertEqual(sorted({c[3] for c in kept}), [1, 2, 4, 5, 6, 7, self.batch])   # that one, and no other
        self.assertEqual((len(kept), calls_of(lines)), (20, []))            # its three calls count a minute more
        self.assertEqual(len(update(self.live)), C.CALL_LIMIT)              # (and the update's minute is held)
        self.assertLessEqual(self.in_the_minute(lines), C.WORLD_CAP)

    def test_the_old_brain_next_was_not_killed_and_wakes(self):
        """Why the batch is held and not taken as never printed: the `brain next` that stored it may be waiting
        still. Here it is, the old package's own process. This version begins meanwhile; then its wait ends."""
        root = the_package_before()
        if root is None:
            self.skipTest("the repository's history does not hold 442a6311")
        go = os.path.join(tempfile.mkdtemp(prefix="player-go-"), "go")
        old = subprocess.Popen([sys.executable, "-W", "ignore", "-c", OLD_PROGRAM, go], cwd=root, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={**os.environ, "PYTHONPATH": root})
        self.addCleanup(lambda: (old.kill(), old.wait(), old.stdout.close(), old.stderr.close()))
        for _ in range(3000):
            if os.path.exists(go + ".made") or old.poll() is not None:
                break
            time.sleep(0.02)
        made = relay.read(go + ".made")
        self.start((made["live"], made))
        lines = self.next(token_of(self.next()[0]))                         # this version begins while it waits
        self.assertEqual(calls_of(lines), [])
        with open(go, "w", encoding="utf8"):
            pass                                                            # and now its wait is over
        said = json.loads(old.communicate(timeout=60)[0].strip().splitlines()[-1])
        self.assertEqual(said["woke"], [brain.SUPERSEDED])                  # it prints no call: the file is another's
        self.assertEqual(len(loose(self.live)), 23)


class N1ABatchOfThisVersionStillReachesItsRelay(Client):
    """The controls: a batch this version's brain made, waiting in this version's file, is printed as before,
    and the brain is not asked a second time for it."""

    def dies_in_the_wait(self, token):
        def dies(wait):
            if wait == C.HUNT_WAIT:
                raise Killed
        with self.assertRaises(Killed):
            self.next(token, dies)
        waiting = self.client()["pending"]
        return waiting, [x["call"] for x in waiting["steps"] if "call" in x]

    def asked(self, token):
        seen, handle = [], brain.Brain.handle
        with mock.patch.object(brain.Brain, "handle", lambda *a, **k: seen.append(1) or handle(*a, **k)):
            return self.next(token), seen

    def test_the_relay_it_was_made_for_asks_again(self):
        a = self.new_relay_with_a_batch()
        waiting, calls = self.dies_in_the_wait(a)
        lines, seen = self.asked(a)
        self.assertEqual((self.calls(lines), seen), (calls, []))
        self.assertEqual(self.client()["held"], {"token": token_of(lines[-1]), "id": waiting["id"]})

    def test_a_replacement_gets_it(self):
        a = self.new_relay_with_a_batch()
        waiting, calls = self.dies_in_the_wait(a)
        lines, seen = self.asked(token_of(self.next()[0]))
        self.assertEqual((self.calls(lines), seen), (calls, []))
        self.assertEqual(self.client()["held"], {"token": token_of(lines[-1]), "id": waiting["id"]})
        self.assertEqual(self.next(a), [brain.SUPERSEDED])

    def test_a_request_made_again_gets_the_answer_it_had(self):
        a = self.new_relay_with_a_batch()
        brain.put(self.rig.dir, a, 1, json.dumps(user(sector=77).data))
        with dies_before_the_receipt(self.rig):
            with self.assertRaises(Killed):
                self.next(a)                                                # dead before the batch was stored
        given = self.saved()["relay"]["answered"]
        lines, seen = self.asked(a)
        self.assertEqual(seen, [])                                          # from the receipt: nothing taken twice
        self.assertEqual(self.calls(lines), [x["call"] for x in given["batch"]["steps"] if "call" in x])
        self.assertTrue(self.calls(lines))
        self.assertEqual(self.loose(), [])


class N1NothingOfAnotherProtocolIsUsed(Client):
    """Not from the review: the other records the two sides keep for each other. Each is its maker's word about
    a batch, and none is taken from a maker that does not carry this version's number."""

    def asked(self, token):
        seen, handle = [], brain.Brain.handle
        with mock.patch.object(brain.Brain, "handle", lambda *a, **k: seen.append(1) or handle(*a, **k)):
            return self.next(token), seen

    def dies_in_the_wait(self, token):
        def dies(wait):
            if wait == C.HUNT_WAIT:
                raise Killed
        with self.assertRaises(Killed):
            self.next(token, dies)
        return self.client()["pending"]

    def write(self, state):
        relay.write(os.path.join(self.rig.dir, "client.json"), state)

    def test_every_record_carries_the_number(self):
        a = self.new_relay_with_a_batch()
        with mock.patch.object(brain, "_await", side_effect=Killed):
            with self.assertRaises(Killed):
                self.next(a)
        (path,) = relay.pending_requests(self.rig.dir)
        records = [relay.read(path), self.client()]                         # the request, the client's file,
        brain.run(self.rig.dir, forever=False)
        (answer,) = glob.glob(os.path.join(self.rig.dir, "outbox", "*"))
        records += [relay.read(answer), self.saved()["relay"]["answered"]]  # the answer, the receipt,
        records += [self.dies_in_the_wait(a)]                               # and the batch that waits
        self.assertEqual([(type(r["protocol"]), r["protocol"]) for r in records], [(int, relay.PROTOCOL)] * 5)

    def test_a_waiting_batch_in_this_versions_file(self):
        """An older `brain next` that runs on this version's file keeps the file's number, and stores a batch
        without one; the brain that made it for it kept a receipt without one."""
        for stamp in STAMPS:
            self.setUp()
            a = self.new_relay_with_a_batch()
            waiting = self.dies_in_the_wait(a)
            n = len([x for x in waiting["steps"] if "call" in x])
            state, world = self.client(), self.saved()
            state["pending"] = stamped(state["pending"], stamp)
            world["relay"]["answered"] = stamped(world["relay"]["answered"], stamp)
            self.write(state)
            relay.write(os.path.join(self.rig.dir, "world.json"), world)
            lines, seen = self.asked(a)
            self.assertEqual((self.calls(lines), seen), ([], []), stamp)    # not printed, from the file or the receipt
            self.next(token_of(lines[-1]))
            self.assertEqual(len([c for c in self.loose() if c[3] == waiting["id"]]), n, stamp)   # its calls: held

    def test_a_client_file_is_this_versions_or_no_file(self):
        """A file with every record in today's shape, and without the number: A replaced with a batch in hand,
        B with one too and another waiting, the operator's word about A not yet with the brain."""
        a = self.new_relay_with_a_batch()
        na = len(self.client()["calls"])
        b = self.new_relay_with_a_batch()
        waiting = self.dies_in_the_wait(b)
        self.stopped(a)
        state = self.client()
        self.assertTrue(state["ended"] and state["pending"] and state["relay"] == b.split("-")[0])
        del state["protocol"], state["pending"]["protocol"]
        self.write(state)
        world = self.saved()
        for old in (b, a):
            self.assertEqual(self.next(old), [brain.SUPERSEDED], old)       # nobody it names is the relay,
        self.assertEqual(brain.put(self.rig.dir, b, "1", "{}"), 1)          # no result is taken for its batch,
        self.assertEqual(self.stopped()["still_held"], [a])                 # what is held is what the ledger holds,
        self.assertEqual((self.client(), self.saved()), (state, world))     # and none of that wrote anything
        lines, seen = self.asked(token_of(self.next()[0]))
        self.assertEqual(seen, [1])                                         # a new relay: the brain is asked
        self.assertNotEqual((self.client()["held"] or {}).get("id"), waiting["id"])
        self.assertEqual(len(self.loose(a)), na)                            # A's batch is held as it was: the word
        self.assertEqual(len([c for c in self.loose() if c[3] == waiting["id"]]),   # about it went with the file;
                         len([x for x in waiting["steps"] if "call" in x]))        # the waiting batch is held too
        self.assertEqual(self.client()["protocol"], relay.PROTOCOL)

    def test_a_request(self):
        a = self.new_relay_with_a_batch()
        with mock.patch.object(brain, "_await", side_effect=Killed):
            with self.assertRaises(Killed):
                self.next(a)
        (path,) = relay.pending_requests(self.rig.dir)
        ask, before = relay.read(path), self.saved()["budget"]["calls"]
        self.assertEqual(ask["protocol"], relay.PROTOCOL)
        others = [stamped(ask, stamp) for stamp in STAMPS]                  # the number is not this version's,
        others += [{k: v for k, v in ask.items() if k != gone} for gone in brain.REQUEST]   # or a field is not there
        for other in others:
            relay.write(path, other)
            brain.run(self.rig.dir, forever=False)
            self.assertEqual(relay.pending_requests(self.rig.dir), [], other)   # removed,
            self.assertEqual(glob.glob(os.path.join(self.rig.dir, "outbox", "*")), [], other)   # not answered,
            self.assertEqual(self.saved()["budget"]["calls"], before, other)    # and nothing is settled by it
        relay.write(path, ask)
        brain.run(self.rig.dir, forever=False)
        (answer,) = glob.glob(os.path.join(self.rig.dir, "outbox", "*"))
        self.assertEqual(relay.read(answer)["protocol"], relay.PROTOCOL)    # the brain's answer carries its own

    def test_an_answer(self):
        """A brain of an older version is still running, and answers this version's request under the name this
        version reads."""
        live, seq, rid = self.rig.dir, 5, "ab" * 4
        mine, home = relay.batch_path(live, seq, rid), brain._lock(live)    # a brain is home: none is started here
        self.addCleanup(home.close)
        answer = {"steps": [{"call": "old.call", "input": {}, "select": []}], "hold": 0, "stop": None, "seq": seq,
                  "request": rid}
        for stamp, taken in [(x, False) for x in STAMPS] + [(relay.PROTOCOL, True)]:
            relay.write(mine, stamped(answer, stamp))
            got = brain._await(live, seq, rid, relay.request_path(live, seq, rid), lambda _: None, limit=0.2)
            self.assertEqual((got is not None, os.path.exists(mine)), (taken, False), stamp)
        relay.write(mine, [1, 2])                                           # and one that is no answer at all
        self.assertIsNone(brain._await(live, seq, rid, relay.request_path(live, seq, rid), lambda _: None, limit=0.2))

    def a_request_an_older_brain_answered(self, older_brain):
        """This version's `brain next` asks while an older brain is home. That brain takes the request's results
        in, makes a batch its own way, and keeps the receipt. Then it is gone, and the relay asks again."""
        a = self.new_relay_with_a_batch()
        brain.put(self.rig.dir, a, 1, json.dumps(user(sector=77).data))

        def no_answer_this_version_reads(live, seq, rid, req, sleep):
            older_brain(req)

        with mock.patch.object(brain, "_await", no_answer_this_version_reads):
            self.assertEqual(self.next(a, lambda _: None), [relay.next_line(a)])
        given = self.saved()["relay"]["answered"]
        old = [x["call"] for x in given["batch"]["steps"] if "call" in x]
        self.assertTrue(old and "protocol" not in given and given["relay"] == a.split("-")[0])
        lines, seen = self.asked(a)
        self.assertEqual(seen, [])                                          # its results are not taken in twice,
        self.assertEqual(self.calls(lines), [])                             # and that brain's batch is not given
        self.next(token_of(lines[-1]))                                      # (was: printed as this version's own)
        self.assertGreaterEqual(len(self.loose()), len(old))                # its calls are held, for nobody

    def test_a_receipt(self):
        def as_d7364237_kept_it(req):
            brain.answer(brain.Brain(self.rig.dir), self.rig.dir, req)
            world = self.saved()
            del world["relay"]["answered"]["protocol"]
            relay.write(os.path.join(self.rig.dir, "world.json"), world)
        self.a_request_an_older_brain_answered(as_d7364237_kept_it)

    def test_a_receipt_of_the_version_before_itself(self):
        """Until the review of 06358ca5 this test had the 442a6311 brain answer this version's request, and
        held that the receipt it kept was not given again. That brain cannot find the request any more (it is
        under this protocol's name: test_rereview7), so there is no such receipt: the brain of the version
        before takes nothing and changes nothing, and the relay's request is answered by this version's."""
        if the_package_before() is None:
            self.skipTest("the repository's history does not hold 442a6311")
        a = self.new_relay_with_a_batch()
        brain.put(self.rig.dir, a, 1, json.dumps(user(sector=77).data))
        before = self.saved()

        def the_older_brain_looks(live, seq, rid, req, sleep):
            self.assertEqual(by_the_version_before(OLD_BRAIN, self.rig.dir)[1]["answered"], 0)   # was 1

        with mock.patch.object(brain, "_await", the_older_brain_looks):
            self.assertEqual(self.next(a, lambda _: None), [relay.next_line(a)])
        self.assertEqual(self.saved(), before)                              # was: its batch, receipt and ledger
        lines, seen = self.asked(a)
        self.assertEqual((seen, bool(self.calls(lines)), self.loose()), ([1], True, []))   # results taken once
        self.assertEqual(BEFORE[:8], "442a6311")


if __name__ == "__main__":
    unittest.main()
