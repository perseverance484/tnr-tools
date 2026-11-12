"""The brain: one resident process that makes every decision (design 4.1).

    python3 -m player.brain run            the resident process: answers requests, watches for a silent relay
    python3 -m player.brain next [TOKEN]   what a relay runs: hand in batch TOKEN's results, print the next batch
    python3 -m player.brain put TOKEN N    a relay whose transcript cannot be read hands in call N's result (stdin)
    python3 -m player.brain set KEY=JSON   change a setting (writes live/control.json; Duet does the same)
    python3 -m player.brain status         print live/status.json

One tick (Brain.handle): apply the director's settings, fold the results into the world model, let each activity
read what it understands, pick the activity with the highest priority class and score (the arbiter, design 4.4),
check its calls at the gates, pace them under the call budget, and write the batch, the status file and the world
model. The relay copies the batch to the game and comes back with `brain next`.

`brain next` starts the resident process when none is running, and answers the request itself if it has to: a relay
is never left without a batch. Every wait is spent here, in the brain, where it costs the relay nothing.

A tick that fails after the results are folded in is undone as a whole: what it learned stays, what it decided
does not, so a plan that never reached the relay is never remembered as sent.
"""
import contextlib
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
    def handle(self, results, usage=None, strays=0):
        """Fold the results in and return the next batch: {"steps", "hold", "stop", "note", "activity"}.
        strays: calls the relay made that the last batch did not ask for (their results are not used)."""
        w = self.world
        console.apply_control(w, self.reg.activities)
        relay.log_tokens(w, w["relay"]["seq"], usage, w["relay"].get("note", ""))
        self.budget.settle(results, w["relay"].get("last_batch") or [])     # when the last batch's calls really ran
        w.absorb(results)
        self.combat.absorb(results)
        for a in self.reg.activities.values():
            try:
                a.on_result(w, results)
            except Exception as err:  # noqa: BLE001  (one activity's bad result must not cost the others theirs)
                w.event("error", f"{a.name} could not take a result in: {err!r}"[:300], about="crash")
        for r in results:
            if r.error and r.error != RATE_LIMITED:
                w.event("error", f"{r.endpoint}: {r.error}", about="call")
        if strays:
            self.budget.stray(strays)
            w.event("finding", f"the relay made {strays} call(s) the batch did not ask for", about="relay")
        known = json.dumps(w.d)                 # what is known before anything is decided
        try:
            out = self._decide(any(r.error == RATE_LIMITED for r in results))
            (w["battle"] or {}).pop("crashed", None)
            self._record(out)
        except Exception:
            w.d = json.loads(known)             # the batch will not reach the relay: nothing it planned was sent
            fight = w["battle"]
            if fight:
                fight["crashed"] = fight.get("crashed", 0) + 1
                if fight["crashed"] > 1:        # the same read has failed twice: it is not tried a third time,
                    fight.pop("inbox", None)    # and the turn's clock decides from the last good read
            raise
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
        if w["control"]["end_session"] and w.status() == "ASLEEP":
            return "session ended by the director: asleep at home"   # never while awake (activities/session.py)
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
            p = self._plan(act)
            if p is None:
                continue
            steps = self._compose(act, p)
            if steps is None:                                     # the gates refused it: do something else
                w.own("brain")["blocked"][act.name] = w.now + BLOCK_FOR
                continue
            hold = max(p.hold, C.RATE_BACKOFF) if limited and p.lane == "world" else p.hold
            steps, waited = self.budget.pace(steps, "recovery" if p.tag == "fight_end" else p.lane, w.now + hold)
            steps, hold = _lead(steps, hold)
            return {"steps": steps, "hold": hold, "stop": None, "activity": act.name,
                    "note": p.note + (f" (paced {waited}s)" if waited else ""),
                    "queue": [(a.name, a.priority, 0) for a in ranked[i + 1:]]}
        why = "paused" if w["control"]["paused"] else "nothing to do"
        return {"steps": [], "hold": IDLE_HOLD, "stop": None, "note": why, "activity": None, "queue": []}

    def _plan(self, act):
        """The activity's plan. A fight's plan that fails fails the tick (which is undone, and the turn's clock
        takes over). Any other activity that fails is set aside for a minute and the next one is asked, so one
        bad scan or reply cannot stop the player."""
        try:
            return act.plan(self.world)
        except Exception as err:  # noqa: BLE001
            if act.priority == "battle":
                raise
            self.world.event("error", f"{act.name}: its plan failed ({err!r}); set aside for {BLOCK_FOR:.0f} s"[:300],
                             about="crash")
            self.world.own("brain")["blocked"][act.name] = self.world.now + BLOCK_FOR
            return None

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


def _lead(steps, hold):
    """A wait in front of a batch's first call is spent by the brain, not the relay: (the steps without it, the
    hold with it added)."""
    if steps and "wait" in steps[0]:
        return steps[1:], round(hold + steps[0]["wait"], 1)
    return steps, hold


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
    back in a moment (sooner in a fight), and the crash is written down for Duet (live/crash.log and an error
    event). The brain has undone what that tick decided, so the next one starts from what is known."""
    req = relay.read(path)
    if req is not None:
        try:
            out = brain.handle(relay.unpack(req.get("results")), req.get("usage"), req.get("strays", 0))
        except Exception:  # noqa: BLE001  (a relay left without a batch loses turns; a logged crash does not)
            out = {"steps": [], "hold": 1.0 if brain.world.in_battle() else 3.0, "stop": None}
            _crashed(brain, live)
        relay.write(relay.batch_path(live, req["seq"]),
                    {"seq": req["seq"], "stop": out["stop"], "hold": out["hold"],
                     "steps": [{k: s[k] for k in ("call", "input", "select")} if "call" in s else s
                               for s in out["steps"]]})
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


def _transcript(state, sleep):
    """The transcript that carries this batch's token, or None. A new relay's, and one that was readable for the
    relay's last batch, is given a moment for its newest line to be written."""
    token, hint = state["token"], state.get("transcript")
    path, tries = relay.find_transcript(token, hint), 4 if hint or state.get("new") else 0
    while not path and tries:
        sleep(0.25)
        path, tries = relay.find_transcript(token, hint), tries - 1
    return path


def _collect(live, state, sleep=time.sleep):
    """The results of the batch this relay was last given: from its own transcript when one carries the batch's
    token, else the ones it handed in with `brain put` for that token. Returns (results, usage, strays, the
    transcript's path or None)."""
    token, expected = state["token"], [tuple(c) for c in state.get("calls") or []]
    path = _transcript(state, sleep)
    results, usage, strays = [], {}, 0
    if path:
        try:
            results, usage, strays = relay.read_batch(path, token, expected)
        except OSError:
            path = None
    inbox = os.path.join(live, "inbox")
    for name in sorted(f for f in os.listdir(inbox) if f.startswith("put-")):
        row = relay.read(os.path.join(inbox, name))
        if row and not path and name.startswith(f"put-{token}-"):
            results.append(relay.unpack([row])[0])
        os.unlink(os.path.join(inbox, name))                       # a result for any other batch is dropped
    return results, usage, strays, path


@contextlib.contextmanager
def _client(live):
    """The lock on live/client.json: who the relay is, and the batch it is owed. One `brain next` at a time reads
    it, talks to the brain and writes it back, so a relay that takes over and one that is still waiting cannot
    each write over the other (AP1 re-review, finding 3)."""
    with open(os.path.join(live, "client.lock"), "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


SUPERSEDED = "STOP superseded: another relay has taken over"


def next_batch(live=None, token=None, out=sys.stdout, sleep=time.sleep):
    """`brain next [token]`: hand in the results, wait for the batch (answering it here if no brain is running),
    spend the brain-side wait, print the batch.

    Without a token the relay is new: it is given a name and one line to run, and nothing is taken from it yet.
    With the token of the batch it was last given, it hands that batch in. Any other token is a relay that has
    been replaced (it is told to stop) or a `brain next` run twice (it is given the current line again).

    A batch the brain has made is kept in client.json until a relay has it. The brain-side wait is spent with
    the lock released, so a replacement can take over meanwhile; whoever owns the relay when the wait is over
    gets the batch, and a relay that was replaced during it is told to stop and prints no call."""
    live = live or C.live_dir()
    os.makedirs(os.path.join(live, "inbox"), exist_ok=True)
    client = os.path.join(live, "client.json")
    with _client(live):
        state = relay.read(client) or {}
        said = _greet(client, state, token)
        if said:
            out.write(said + "\n")
            return 0
        me, (pending, hold) = state["relay"], _exchange(live, client, state, sleep)
    wait = hold if hold is not None else pending["ready_at"] - time.time()
    if wait > 0:
        sleep(wait)
    with _client(live):
        state = relay.read(client) or {}
        if state.get("relay") != me:
            out.write(SUPERSEDED + "\n")                           # the batch stays for the relay that took over
        elif (state.get("pending") or {}).get("id") != pending["id"]:
            # the batch this call waited for is not the one that is owed any more: another call of this relay
            # has it, or it grew too old and the brain was asked afresh. Print nothing of it; come back.
            out.write(relay.next_line(state["token"]) + "\n")
        else:
            state.update(seq=pending["seq"], token=f"{me}-{pending['seq']}", issued_at=time.time(), pending=None,
                         calls=[[x["call"], x["input"]] for x in pending["steps"] if "call" in x])
            relay.write(client, state)
            out.write("\n".join(relay.lines(pending["steps"], pending["stop"], state["token"],
                                            echo=not state.get("transcript"))) + "\n")
    return 0


def _greet(client, state, token):
    """What to say to a `brain next` that hands nothing in: a new relay gets its name and its first line, a
    replaced one is told to stop, a second call for the same batch gets the current line. None for a relay that
    is handing in the batch it was last given."""
    if token is None:
        state = {"relay": os.urandom(3).hex(), "seq": state.get("seq", 0), "calls": [], "transcript": None,
                 "new": True, "pending": state.get("pending")}
        state["token"] = f"{state['relay']}-{state['seq']}"
        relay.write(client, state)
        return relay.next_line(state["token"])
    if token != state.get("token"):
        return relay.next_line(state["token"]) if token.split("-")[0] == state.get("relay") else SUPERSEDED
    return None


def _exchange(live, client, state, sleep):
    """Hand this relay's results to the brain and get the next batch, unless a batch is already waiting for a
    relay. The batch is written into client.json before anything else happens to it. Returns (the batch, the
    brain-side wait still to spend, or None for one that was already waiting)."""
    results, usage, strays, path = _collect(live, state, sleep)
    if state.get("handed") == state["token"]:                      # this batch's results have gone in already
        results, usage, strays = [], {}, 0
    pending, hold = _owed(state), None
    if pending is None:
        seq = state["seq"] + 1
        req = relay.request_path(live, seq)
        relay.write(req, {"seq": seq, "results": relay.pack(results), "usage": usage, "strays": strays,
                          "at": time.time()})
        batch = _await(live, seq, req, sleep)
        if batch is None:                                          # never leave the relay without a next step
            batch = {"steps": [], "stop": None, "hold": 5.0}
        hold = batch["hold"]
        pending = {"id": os.urandom(4).hex(), "seq": seq, "steps": batch["steps"], "stop": batch["stop"],
                   "ready_at": time.time() + hold}
    state.update(pending=pending, transcript=path, new=False, handed=state["token"])
    relay.write(client, state)
    return pending, hold


def _owed(state):
    """A batch the brain made that no relay has had yet (its relay was replaced while it waited), unless it has
    waited too long to be worth sending: then the brain is asked afresh, under the next number. A batch is known
    by its own id, so a call that is still waiting on the old one cannot publish it in the new one's place
    (review of 0d10b7c6, finding 3)."""
    pending = state.get("pending")
    if pending and time.time() - pending["ready_at"] > C.STALE_OUTBOX:
        state["seq"] = max(state.get("seq", 0), pending["seq"])    # its number is not used again
        return None
    return pending


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


def put(live, token, index, text):
    """`brain put TOKEN N`, with the result on standard input: call N (from 1) of batch TOKEN, from a relay whose
    transcript cannot be read. A result for any batch but the one in progress is dropped."""
    state = relay.read(os.path.join(live, "client.json")) or {}
    calls = state.get("calls") or []
    if token != state.get("token") or not str(index).isdigit() or not 1 <= int(index) <= len(calls):
        return 1
    ep, inp = calls[int(index) - 1]
    relay.write(os.path.join(live, "inbox", f"put-{token}-{int(index):03d}.json"),
                list(relay.from_text(ep, inp, text.strip(), time.time())))
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
        return next_batch(live, argv[1] if len(argv) > 1 else None)
    if cmd == "put" and len(argv) == 3:
        return put(live, argv[1], argv[2], sys.stdin.read())
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
