"""A random walk of relays against the real `brain next`, to look for the interleaving nobody thought of.

Each walk: relays that do their batches line by line; replacements at any moment, also while the relay that is
running waits for the batch it asked for; replaced relays that go on with the batch they have, at once or much
later, and come back; relays that were told to stop and ask again all the same; relays that die without a
word; `brain next` processes that die before the brain answers, before the answer is written down, or before
the batch is printed (the relay then runs the line again, or is gone); long pauses; a client file that loses
its record of who holds what, is left without this version's number, or is lost whole; a ledger that turns
into one another version kept (it loses its number, and some of the calls it held: that version let them go);
and an operator who lists what is held, says "stopped" of one relay only when that relay is, and says "stopped
all" only when every relay but the running one is. The hunt
is kept at its fastest, so the world lane runs at its cap and a call that is not counted shows as one call too
many. Time is the walk's own clock; no call leaves the process.

After every step:
  cap       no more calls really made in any minute than the world lane allows (every call here is a world call)
  ledger    every call really made in the last minute is counted by the saved ledger: it is never ahead
  evidence  the calls of a batch whose relay has neither come back nor been stopped are all still held (out or
            loose): nothing but evidence settles them, and no evidence reaches a batch it was not said of
  heard     once `brain next` has handed the brain the word that a batch is over, none of its calls is loose
  real      a loose call belongs to a batch that was printed to a relay (or was the brain's last batch when the
            client's record was lost): none is held for a batch nobody can have
  once      no batch's results reach Brain.handle twice
  alone     no batch is printed twice, to one relay or to two
  listing   asking what is held changes nothing

    python3 -m player.tests.test_walk [WALKS [STEPS]]     more walks than the test suite runs (default 200, 300)

What it does not cover: fights and the other lanes, results read from a transcript (the relays here hand
results in with `brain put`), real processes and locks (a death here is an exception), and a relay that breaks
its contract (calls out of order, or `brain next` before its calls).
"""
import collections
import io
import json
import os
import random
import sys
import time
import traceback
import unittest
from unittest import mock

from player import brain, config as C, relay
from player.tests.support import Rig, user

PROFILE = json.dumps(user().data)
DEATHS = ("before the answer", "before the receipt", "before the print")


class Died(Exception):
    """A `brain next` process that is killed."""


class Walk:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.rig = Rig()
        self.now = [self.rig.t]
        self.rig.world.absorb([user()._replace(at=self.now[0])])
        self.rig.world.save()
        self.made, self.handed, self.printed, self.batches = [], collections.Counter(), {}, {}
        self.given = set()                        # every batch that was printed, or marked as printed, to a relay
        self.heard = set()                        # every batch the client has had word of that it is over
        self.inside = False                       # in a replacement's handshake made during another relay's wait
        self.relays, self.cur, self.problems = [], None, []
        real_brain, real_handle = brain.Brain, brain.Brain.handle

        def handle(self_, results, usage=None, strays=0, ask=None):
            if results and ask and ask.get("held"):
                self.handed[ask["held"]["id"]] += 1
            return real_handle(self_, results, usage, strays, ask)
        self.patches = [
            mock.patch.dict(os.environ, {
                "TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(self.rig.dir, "none"),
                "TNR_PLAYER_LIVE": self.rig.dir, "TNR_PLAYER_FIGHTS": os.path.join(self.rig.dir, "fights")}),
            mock.patch.object(time, "time", side_effect=lambda: self.now[0]),
            mock.patch.object(C, "HUNT_WAIT", 0.5),
            mock.patch.object(brain, "Brain", lambda live: real_brain(live, clock=lambda: self.now[0])),
            mock.patch.object(real_brain, "handle", handle)]

    # ------------------------------------------------------------ `brain next`, and what a relay does with it
    def next(self, token, die=None):
        """One `brain next`, killed at `die` if that is given. Its brain-side waits move the clock."""
        real_answer, real_write = brain.answer, relay.write

        def sleep(wait):
            self.now[0] += max(0.0, wait)
            # the brain-side wait is spent with the client's lock released: a replacement may shake hands now
            if wait not in (0.25, C.BRAIN_WAIT) and not self.inside and self.rng.random() < 0.08:
                self.inside = True
                try:
                    self.cur = {"name": f"r{len(self.relays)}", "token": None, "todo": []}
                    self.relays.append(self.cur)
                    self.take(self.cur, self.next(None))
                finally:
                    self.inside = False

        def answer(*a, **k):
            if die == "before the answer":
                raise Died
            return real_answer(*a, **k)

        def write(path, obj):
            if die == "before the receipt" and path.endswith("client.json") and obj.get("pending"):
                raise Died
            return real_write(path, obj)

        class Out(io.StringIO):
            def write(self, text):
                if die == "before the print" and '"call"' in text:
                    raise Died
                return super().write(text)
        out = Out()
        try:
            with mock.patch.object(brain, "answer", answer), mock.patch.object(relay, "write", write):
                brain.next_batch(self.rig.dir, token, out, sleep)
        finally:
            self.seen()
        return out.getvalue().splitlines()

    def client(self):
        """What the client's file says. One without this version's number says nothing."""
        state = relay.read(os.path.join(self.rig.dir, "client.json")) or {}
        return state if state.get("protocol") == relay.PROTOCOL else {}

    def seen(self):
        """After anything that writes the client's file: what it now says is printed, and what is over."""
        state = self.client()
        self.given.add((state.get("held") or {}).get("id"))
        self.heard |= {e[0] for e in state.get("ended") or []}

    def take(self, r, lines):
        """A relay reads what `brain next` printed. The walk notes which batch that is, by the brain's id."""
        if not lines or lines[0].startswith("STOP"):
            r["over"] = r["told"] = True
            return
        r["todo"] = [json.loads(x) for x in lines]
        held = self.client().get("held")
        if held and any("call" in x for x in r["todo"]):
            if held["id"] in self.printed:
                self.problems.append(f"batch {held['id']} printed to {self.printed[held['id']]} and to {r['name']}")
            self.printed[held["id"]] = r["name"]
            r["batch"] = held["id"]
            self.batches[held["id"]] = {"calls": sum(1 for x in r["todo"] if "call" in x), "over": False}
        if " next" in r["todo"][-1].get("bash", ""):
            r["token"] = r["todo"][-1]["bash"].split(" next")[1].strip() or None

    def step(self, r, die=None):
        """A relay does the next line it has."""
        if r.get("over"):
            return
        x = r["todo"].pop(0) if r["todo"] else {"bash": f"x next {r['token'] or ''}".rstrip()}
        self.now[0] += self.rng.choice((0.05, 0.3, 0.3, 1.0, 2.5))
        if "call" in x:
            self.made.append(self.now[0])
            r["last"] = PROFILE if x["call"] == "profile.getUser" else "{}"
        elif "put" in x:
            token, n = x["put"].split()[-2:]
            brain.put(self.rig.dir, token, n, r.get("last", "{}"))
        elif " next" not in x["bash"]:
            self.now[0] += float(x["bash"].split("sleep(")[1].split(")")[0])
        else:
            if r.get("batch"):
                self.batches[r["batch"]]["over"] = True           # it has done every line of it: it is back
            try:
                self.take(r, self.next(x["bash"].split(" next")[1].strip() or None, die))
            except Died:
                r["todo"] = [x] if self.rng.random() < 0.7 else []  # it runs the line again, or it is gone
                r["over"] = r["dead"] = not r["todo"]

    def new(self):
        """A new relay. The one that was running goes on with what it has, dies, or goes on much later."""
        if self.cur and not self.cur.get("over"):
            self.cur["fate"] = self.rng.choice(("goes on", "goes on", "dies", "late"))
            self.cur["over"] = self.cur["dead"] = self.cur["fate"] == "dies"
        self.cur = {"name": f"r{len(self.relays)}", "token": None, "todo": []}
        self.relays.append(self.cur)
        self.step(self.cur)

    # ------------------------------------------------------------ what must hold after every step
    def check(self, what):
        now = self.now[0]
        worst = max((sum(1 for u in self.made if t - 60 < u <= t) for t in self.made[-40:]), default=0)
        if worst > C.WORLD_CAP:
            self.problems.append(f"{worst} calls in a minute after {what}")
        budget = (relay.read(os.path.join(self.rig.dir, "world.json")) or {}).get("budget") or {}
        calls = budget.get("calls", [])
        counted, recent = [c for c in calls if len(c) > 2 or c[0] > now - 60], [t for t in self.made if t > now - 60]
        if budget.get("protocol") == relay.PROTOCOL and len(counted) < len(recent):   # (a ledger of this version)
            self.problems.append(f"the ledger counts {len(counted)}; {len(recent)} calls were made in the last "
                                 f"minute, after {what}")
        for batch, b in self.batches.items():
            held = sum(1 for c in calls if (c[2:3] == ["loose"] and c[3] == batch)
                       or (c[2:3] == ["out"] and budget.get("batch") == batch))
            if not b["over"] and not b.get("forgotten") and held != b["calls"]:
                self.problems.append(f"batch {batch}: {held} of its {b['calls']} calls are still held, though its "
                                     f"relay has neither come back nor been stopped, after {what}")
        waiting = {e[0] for e in self.client().get("ended") or []}
        for batch in {c[3] for c in calls if c[2:3] == ["loose"]}:
            if batch not in self.given and not str(batch).startswith("update-"):
                self.problems.append(f"calls are held for batch {batch}, which no relay was given, after {what}")
            elif batch in self.heard and batch not in waiting:
                self.problems.append(f"batch {batch} is still loose, though the brain was told it is over, "
                                     f"after {what}")
        twice = [k for k, n in self.handed.items() if n > 1]
        if twice:
            self.problems.append(f"the results of {twice} reached the brain twice, after {what}")

    def one(self):
        """One random event; returns what it was."""
        roll = self.rng.random()
        old = [r for r in self.relays if r is not self.cur and not r.get("over")]
        dead = [r for r in self.relays if r.get("dead") and r.get("token") and not r.get("said")]
        if self.cur.get("over") or roll < 0.06:
            self.new()
            return "a replacement"
        if roll < 0.12 and old:
            r = self.rng.choice(old)
            self.now[0] += self.rng.choice((30, 70, 400, 2000)) if r.get("fate") == "late" else 0
            self.step(r)
            return "a replaced relay going on"
        if roll < 0.16:
            self.now[0] += self.rng.choice((5, 15, 45, 90, 1000))
            return "a pause"
        if roll < 0.20 and dead:
            r = self.rng.choice(dead)
            r["said"] = True
            if r.get("batch"):
                self.batches[r["batch"]]["over"] = True
            self.operator([r["token"]])
            return "the operator's word of one relay"
        told = [r for r in self.relays if r.get("told") and r.get("token")]
        if roll < 0.23 and told:
            r = self.rng.choice(told)                             # a relay that was told to stop asks again
            if self.next(r["token"]) != [brain.SUPERSEDED]:
                self.problems.append(f"a replaced relay was not told to stop the second time ({r['name']})")
            return "a stopped relay asking again"
        if roll < 0.29:
            die = self.rng.choice(DEATHS)
            self.step(self.cur, die)
            return f"a `brain next` that died {die}"
        if roll < 0.31:
            before = self.client()
            self.operator([])
            if self.client() != before:
                self.problems.append("asking what is held changed the client's file")
            return "the operator asking what is held"
        if roll < 0.33 and not old:                               # every relay but the running one is stopped
            for r in self.relays:
                if r is not self.cur and r.get("batch"):
                    self.batches[r["batch"]]["over"] = True
            for batch in self.batches:                            # also what the running relay had and handed in
                if batch != self.cur.get("batch"):
                    self.batches[batch]["over"] = True
            self.operator(["all"])
            if self.rng.random() < 0.5:
                return "the operator's word of every relay but the one running"
            # and then the running relay is replaced, and the replacement's first request dies before it has
            # its answer down and is asked again: the word is read a second time, with one more relay held
            self.new()
            self.step(self.cur, "before the receipt")
            self.cur["todo"] = self.cur["todo"] or [{"bash": f"x next {self.cur['token'] or ''}".rstrip()}]
            self.cur["over"] = self.cur["dead"] = False
            self.step(self.cur)
            return "the operator's word of every relay, then a replacement that asks twice"
        if roll < 0.345:
            return self.lose()
        if roll < 0.355:
            return self.forget()
        self.step(self.cur)
        return "a step"

    def operator(self, names):
        brain.stopped(self.rig.dir, names, io.StringIO())
        self.seen()

    def lose(self):
        """The client's file loses its record of who holds what, or its number (it is then another version's,
        and none of it is read), or is lost whole. What the brain had out then may come to be held for a relay
        that is not on record; word that was waiting in the file is gone."""
        path, state = os.path.join(self.rig.dir, "client.json"), self.client()
        budget = (relay.read(os.path.join(self.rig.dir, "world.json")) or {}).get("budget") or {}
        self.given.add(budget.get("batch"))
        self.heard -= {e[0] for e in state.get("ended") or []}
        roll = self.rng.random()
        if roll < 0.4 and state:
            state.pop("held", None)
            state.pop("ended", None)
            relay.write(path, state)
            return "a client file that lost its record of who holds what"
        if roll < 0.7 and state:
            state.pop("protocol", None)
            relay.write(path, state)
            return "a client file without this version's number"
        if os.path.exists(path):
            os.unlink(path)
        return "a client file that was lost"

    def forget(self):
        """The ledger becomes one that another version of the player kept: its number is gone, and so are some
        of the calls it held for relays that have not come back (review of 29797ba0: 442a6311 let a held call
        go after fifteen minutes). Those relays go on as before. Nothing stands for their calls now but the
        minute the brain holds when it takes such a ledger over, until the operator has spoken."""
        path = os.path.join(self.rig.dir, "world.json")
        world = relay.read(path)
        if not world:
            return "a pause"
        calls = world["budget"]["calls"]
        gone = {c[3] for c in calls if c[2:3] == ["loose"] and not str(c[3]).startswith("update-")
                and self.rng.random() < 0.6}
        world["budget"] = {"batch": world["budget"].get("batch"),
                           "calls": [c for c in calls if not (c[2:3] == ["loose"] and c[3] in gone)]}
        relay.write(path, world)
        for batch in gone & set(self.batches):
            self.batches[batch]["forgotten"] = True
        return "a ledger that another version kept, which let held calls go"

    def run(self, steps):
        """The problems of a walk of this many steps: the first step that has any ends it."""
        for p in self.patches:
            p.start()
        try:
            self.new()
            for i in range(steps):
                self.check(f"step {i}: {self.one()}")
                if self.problems:
                    break
        except Exception as err:  # noqa: BLE001  (a walk that raises is a walk with a problem)
            self.problems.append(f"raised {err!r} at {traceback.format_exc().splitlines()[-3].strip()}")
        finally:
            for p in self.patches:
                p.stop()
        return self.problems


class RandomWalks(unittest.TestCase):
    def test_a_few_walks_keep_every_promise(self):
        for seed in range(6):
            walk = Walk(seed)
            self.assertEqual(walk.run(200), [], f"seed {seed}")
            self.assertGreater(len(walk.made), 10, f"seed {seed}")          # and calls were really made


if __name__ == "__main__":
    walks, steps = (int(a) for a in (sys.argv[1:3] + ["200", "300"][len(sys.argv) - 1:])[:2])
    bad = made = 0
    for n in range(walks):
        w = Walk(n)
        found = w.run(steps)
        made += len(w.made)
        bad += bool(found)
        if found and bad <= 8:
            print("seed", n, found[:2])
    print(f"{walks} walks of {steps} steps, {made} calls made: {bad} with a problem")
    sys.exit(1 if bad else 0)
