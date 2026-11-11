"""The brain: one resident process that makes every decision (design 4.1).

    python3 -m player.brain run            the resident process: answers requests, watches for a silent relay
    python3 -m player.brain next           what a relay runs: hand in the last batch's results, print the next batch
    python3 -m player.brain put N JSON     a relay that cannot be read from its transcript hands in call N's result
    python3 -m player.brain set KEY=JSON   change a setting (writes live/control.json; Duet does the same)
    python3 -m player.brain status         print live/status.json

One tick (Brain.handle): apply the director's settings, fold the results into the world model, let each activity
read what it understands, pick the activity with the highest priority class and score (the arbiter, design 4.4),
check its calls at the gates, pace them under the call budget, and write the batch, the status file and the world
model. The relay copies the batch to the game and comes back with `brain next`.

`brain next` starts the resident process when none is running, and answers the request itself if it has to: a relay
is never left without a batch. Every wait is spent here, in the brain, where it costs the relay nothing.
"""
import fcntl
import json
import os
import subprocess
import sys
import time

from . import config as C
from . import console, registry, relay
from .budget import Budget
from .combat import Combat
from .gates import Gates
from .registry import CLASSES
from .world import RATE_LIMITED, World

IDLE_HOLD = 30.0          # s between looks when there is nothing to do (paused, or waiting on the director)
BLOCK_FOR = 60.0          # s an activity is passed over after the gates refused its plan
QUIET = ("watch", "harvest", "battle")     # activities whose end is not an event of its own


class Brain:
    def __init__(self, live=None, clock=time.time, combat=None, gates=None):
        self.world = World(live, clock)
        self.reg = registry.load()
        self.combat = combat or Combat()
        self.gates = gates or Gates()
        self.budget = Budget(self.world)
        for a in self.reg.activities.values():
            a.combat, a.budget, a.gates = self.combat, self.budget, self.gates
        if not self.world["records"].get("handover"):               # once: carry on from where the pilot stands
            took = self.combat.pilot_handover()
            self.world["inventory"].update({k: took[k] for k in ("full_potion_uid",) if k in took})
            for k in ("lost_to", "skip"):
                self.world["opponents"][k].update(took.get(k) or {})
            self.world["records"]["handover"] = True

    # ------------------------------------------------------------ one tick
    def handle(self, results, usage=None):
        """Fold the results in and return the next batch: {"steps", "hold", "stop", "note", "activity"}."""
        w = self.world
        console.apply_control(w, self.reg.activities)
        relay.log_tokens(w, w["relay"]["seq"], usage, w["relay"].get("note", ""))
        w.absorb(results)
        self.combat.absorb(results)
        for a in self.reg.activities.values():
            a.on_result(w, results)
        for r in results:
            if r.error and r.error != RATE_LIMITED:
                w.event("error", f"{r.endpoint}: {r.error}", about="call")
        out = self._decide(any(r.error == RATE_LIMITED for r in results))
        self._record(out)
        return out

    def rank(self):
        """The activities that can act now, best first: by priority class, then by value times the goal's weight
        (design 4.4). A paused player only fights."""
        w, ctl = self.world, self.world["control"]
        weights = {**C.goals()["weights"], **ctl["goal_weights"]}
        blocked = w.own("brain").setdefault("blocked", {})
        acts = [a for a in self.reg.activities.values()
                if ctl["activities"].get(a.name, True) and blocked.get(a.name, 0) <= w.now
                and not getattr(a, "rides", False) and (a.priority == "battle" or not ctl["paused"])
                and a.available(w)]
        return sorted(acts, key=lambda a: (CLASSES.index(a.priority), -a.value(w) * weights.get(a.goal, 1.0)))

    def _stop(self):
        """Why the relay should end now, or None. Never in a fight."""
        w = self.world
        if w.in_battle():
            return None
        if w["control"]["end_session"]:
            return "session ended by the director"
        if relay.should_rotate(w):
            w["relay"].update(baseline_tokens=None, context_tokens=0, rotations=w["relay"].get("rotations", 0) + 1)
            return "rotate: start a fresh relay"
        if w.status() == "ASLEEP" and w["control"]["mode"] != "hunt":
            return "asleep"
        return None

    def _decide(self, limited):
        w = self.world
        stop = self._stop()
        if stop:
            return {"steps": [], "hold": 0.0, "stop": stop, "note": f"STOP {stop}", "activity": None, "queue": []}
        ranked = self.rank()
        for i, act in enumerate(ranked):
            p = act.plan(w)
            if p is None:
                continue
            steps = self._compose(act, p)
            if steps is None:                                     # the gates refused it: do something else
                w.own("brain")["blocked"][act.name] = w.now + BLOCK_FOR
                continue
            hold = max(p.hold, C.RATE_BACKOFF) if limited and p.lane == "world" else p.hold
            steps, waited = self.budget.pace(steps, "recovery" if p.tag == "fight_end" else p.lane, w.now + hold)
            return {"steps": steps, "hold": hold, "stop": None, "activity": act.name,
                    "note": p.note + (f" (paced {waited}s)" if waited else ""),
                    "queue": [(a.name, a.priority, 0) for a in ranked[i + 1:]]}
        why = "paused" if w["control"]["paused"] else "nothing to do"
        return {"steps": [], "hold": IDLE_HOLD, "stop": None, "note": why, "activity": None, "queue": []}

    def _compose(self, act, p):
        """The plan's steps as they will be sent, or None when the gates refuse one. A fight's closing batch gets
        recovery in front of it; a quiet world batch may carry a rider's reads."""
        w, steps = self.world, list(p.steps)
        if not self.gates.screen(steps, w, act.name)[0]:
            return None
        if p.tag == "fight_end":
            heal = self.reg.activities["recovery"].after_fight(w)
            if heal and self.gates.screen(heal, w, "recovery")[0]:
                steps = heal + steps
        if p.tag == "idle":
            for rider in (a for a in self.reg.activities.values() if getattr(a, "rides", False)):
                if w["control"]["activities"].get(rider.name, True) and rider.available(w):
                    extra = rider.plan(w)
                    if extra and self.gates.screen(extra.steps, w, rider.name)[0]:
                        steps += extra.steps
        for s in steps:
            if "call" in s:
                self.gates.sent(s, w)
        return steps

    def _record(self, out):
        """Book-keeping after a decision: the relay's state, the console's files, the world model on disk."""
        w, r = self.world, self.world["relay"]
        prev = r.get("activity")
        if prev and prev != out["activity"] and prev not in QUIET:
            w.event("activity_done", f"{prev}: {r.get('note', '')}", activity=prev)
        r.update(seq=r["seq"] + 1, activity=out["activity"], note=out["note"], issued_at=w.now + out["hold"],
                 expect=None if out["stop"] else relay.seconds(out["steps"]), stalled=False,
                 last_batch=[{k: s[k] for k in ("call", "input")} for s in out["steps"] if "call" in s])
        console.write_status(w, self.budget, out["activity"], out["note"], out["queue"])
        w.save()

    def watchdog(self):
        """A relay that has not come back in time is a stall (design 4.1). Called by the resident process."""
        w, r = self.world, self.world["relay"]
        if r.get("expect") is None or r.get("stalled"):
            return False
        if w.now <= r["issued_at"] + r["expect"] + C.STALE_OUTBOX:
            return False
        r["stalled"] = True
        w.event("stall", f"the relay has not come back for {w.now - r['issued_at']:.0f} s"
                         + (" (in a fight)" if w.in_battle() else ""), about="relay")
        console.write_status(w, self.budget, r.get("activity"), "STALLED: " + str(r.get("note", "")), [])
        w.save()
        return True


# ---------------------------------------------------------------- the resident process and its client
def _lock(live, wait=False):
    """The one-brain lock: whoever holds it owns the world model. Returns the open file, or None."""
    os.makedirs(live, exist_ok=True)
    f = open(os.path.join(live, "brain.lock"), "w")  # noqa: SIM115 (held for the life of the holder)
    try:
        fcntl.flock(f, fcntl.LOCK_EX | (0 if wait else fcntl.LOCK_NB))
        return f
    except OSError:
        f.close()
        return None


def answer(brain, live, path):
    """Answer one request file with a batch file. A tick that crashes still answers: the relay is told to come
    back in a few seconds, and the crash is written down for Duet (live/crash.log and an error event)."""
    req = relay.read(path)
    if req is not None:
        try:
            out = brain.handle(relay.unpack(req.get("results")), req.get("usage"))
        except Exception:  # noqa: BLE001  (a relay left without a batch loses turns; a logged crash does not)
            out = {"steps": [], "hold": 3.0, "stop": None}
            _crashed(brain, live)
        relay.write(relay.batch_path(live, req["seq"]),
                    {"seq": req["seq"], "lines": relay.lines(out["steps"], out["stop"]), "hold": out["hold"],
                     "calls": [[s["call"], s["input"]] for s in out["steps"] if "call" in s]})
    os.unlink(path)


def _crashed(brain, live):
    import traceback
    text = traceback.format_exc()
    with open(os.path.join(live, "crash.log"), "a", encoding="utf8") as f:
        f.write(f"--- {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n{text}\n")
    try:
        brain.world.event("error", "the brain's tick crashed: " + text.strip().splitlines()[-1], about="crash")
    except Exception:  # noqa: BLE001
        pass


def run(live=None, forever=True):
    """The resident process. Exits at once when another brain already holds the lock."""
    live = live or C.live_dir()
    lock = _lock(live)
    if lock is None:
        return 1
    brain = Brain(live)
    while True:
        for path in relay.pending_requests(live):
            answer(brain, live, path)
        brain.watchdog()
        if not forever:
            return 0
        time.sleep(C.BRAIN_WAIT)


def _collect(live, state):
    """The results of the batch the relay just made: from its transcript, plus any handed in with `brain put`."""
    results, usage = [], {}
    path = relay.find_transcript()
    if path:
        try:
            results, usage = relay.read_results(path, state.get("issued_at", 0))
        except OSError:
            path = None
    for p in sorted(os.path.join(live, "inbox", f) for f in os.listdir(os.path.join(live, "inbox"))
                    if f.startswith("put-")):
        row = relay.read(p)
        if row:
            results.append(relay.unpack([row])[0])
        os.unlink(p)
    return results, usage, path is not None


def next_batch(live=None, out=sys.stdout, sleep=time.sleep):
    """`brain next`: hand in the results, wait for the batch (answering it here if no brain is running), spend the
    brain-side wait, print the batch."""
    live = live or C.live_dir()
    os.makedirs(os.path.join(live, "inbox"), exist_ok=True)
    state = relay.read(os.path.join(live, "client.json")) or {"seq": 0, "issued_at": 0}
    results, usage, readable = _collect(live, state)
    seq = state["seq"] + 1
    req = relay.request_path(live, seq)
    relay.write(req, {"seq": seq, "results": relay.pack(results), "usage": usage, "at": time.time()})
    batch = _await(live, seq, req, sleep)
    if batch is None:                                              # never leave the relay without a next step
        batch = {"lines": relay.lines([]), "hold": 5.0, "calls": []}
    if batch["hold"] > 0:
        sleep(batch["hold"])
    relay.write(os.path.join(live, "client.json"), {"seq": seq, "issued_at": time.time(), "calls": batch["calls"]})
    echo = [] if readable or batch["lines"][0].startswith("STOP") else ["ECHO"]   # no transcript: results by `put`
    out.write("\n".join(echo + batch["lines"]) + "\n")
    return 0


def _await(live, seq, req, sleep, limit=90.0):
    """The batch for request seq. When no brain holds the lock, this process answers and then starts one."""
    t0 = time.time()
    while time.time() - t0 < limit:
        batch = relay.read(relay.batch_path(live, seq))
        if batch is not None:
            os.unlink(relay.batch_path(live, seq))
            return batch
        lock = _lock(live)
        if lock is not None:                                       # nobody is home: answer here, then start a brain
            try:
                if os.path.exists(req):
                    answer(Brain(live), live, req)
            finally:
                lock.close()
            if os.environ.get("TNR_PLAYER_NO_DAEMON") != "1":
                subprocess.Popen([sys.executable, "-m", "player.brain", "run"], cwd=C.ROOT, start_new_session=True,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            continue
        sleep(C.BRAIN_WAIT)
    return None


def put(live, index, text):
    """`brain put N JSON`: the result of call N (from 1) of the last batch, for a relay with no readable transcript."""
    state = relay.read(os.path.join(live, "client.json")) or {}
    ep, inp = (state.get("calls") or [])[int(index) - 1]
    try:
        row = [ep, inp, json.loads(text), None, time.time()]
    except ValueError:
        row = [ep, inp, None, RATE_LIMITED if "Too Many Requests" in text else text[:300], time.time()]
    relay.write(os.path.join(live, "inbox", f"put-{time.time():.3f}-{index}.json"), row)
    return 0


def _setting(arg):
    """KEY=VALUE from the command line: the value is JSON when it parses (true, 3, {"harvest": false}), else text."""
    key, value = arg.split("=", 1)
    try:
        return key, json.loads(value)
    except ValueError:
        return key, value


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    live = C.live_dir()
    cmd = argv[0] if argv else "status"
    if cmd == "run":
        return run(live)
    if cmd == "next":
        return next_batch(live)
    if cmd == "put":
        return put(live, argv[1], argv[2])
    if cmd == "set":
        print(json.dumps(console.set_control(live, **dict(_setting(a) for a in argv[1:]))))
        return 0
    if cmd == "status":
        print(json.dumps(relay.read(os.path.join(live, "status.json")), indent=1))
        return 0
    sys.stderr.write(__doc__.split("\n\n")[1] + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
