"""The brain: one resident process that makes every decision (design 4.1).

    python3 -m player.brain run            the resident process: answers requests, watches for a silent relay
    python3 -m player.brain next [TOKEN]   what a relay runs: hand in batch TOKEN's results, print the next batch
    python3 -m player.brain put TOKEN N    a relay whose transcript cannot be read hands in call N's result (stdin)
    python3 -m player.brain set KEY=JSON   change a setting (writes live/control.json; Duet does the same)
    python3 -m player.brain stopped TOKEN  the operator's word that a replaced relay has been stopped (or: all)
    python3 -m player.brain status         print live/status.json

One tick (Brain.handle): apply the director's settings, fold the results into the world model, let each activity
read what it understands, pick the activity with the highest priority class and score (the arbiter, design 4.4),
check its calls at the gates, pace them under the call budget, and write the batch, the status file and the world
model. The relay copies the batch to the game and comes back with `brain next`.

`brain next` starts the resident process when none is running, and answers the request itself if it has to: a relay
is never left without a batch. Every wait is spent here, in the brain, where it costs the relay nothing.

A tick that fails after the results are folded in is undone as a whole: what it learned stays, what it decided
does not, so a plan that never reached the relay is never remembered as sent. A fight's tick that fails twice
running still sends what the turn is owed (Battle.last_resort): no turn is lost to a crash.

Every request a relay's `brain next` makes carries the relay's name, the request's number and an id of its own.
The answer is kept in the world model, saved in the same write as everything the request changed, before the
request is answered: so also when the tick failed. The same request made again (its `brain next` died before it
had the answer down) gets that answer again, and nothing is applied a second time.

Who has which batch is kept by `brain next` (live/client.json), from what it printed and to whom, never from
what a relay says of itself. A batch is the request's id; it is held by the relay it was printed to until that
relay hands it in. A relay that is replaced while it holds one leaves it loose in the call ledger
(player/budget.py), until it comes back with that batch's token or the operator says it has been stopped.
"""
import contextlib
import fcntl
import glob
import json
import os
import subprocess
import sys
import time
import traceback

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
        self.ask = {}                                               # what the request being answered said
        for a in self.reg.activities.values():
            a.combat, a.budget, a.gates = self.combat, self.budget, self.gates
        if not self.world["records"].get("handover"):               # once: carry on from where the pilot stands
            took = self.combat.pilot_handover()
            self.world["inventory"].update({k: took[k] for k in ("full_potion_uid",) if k in took})
            for k in ("lost_to", "skip"):
                self.world["opponents"][k].update(took.get(k) or {})
            self.world["records"]["handover"] = True

    # ------------------------------------------------------------ one tick
    def handle(self, results, usage=None, strays=0, ask=None):
        """Fold the results in and return the next batch: {"steps", "hold", "stop", "note", "activity"}.
        strays: calls the relay made that the last batch did not ask for (their results are not used).
        ask: what the relay's `brain next` said beside the results (a request file, see _exchange): its relay,
        number and id; held, the batch this relay is handing in; gone, the batches printed to relays that were
        replaced before they handed them in; ended, those of them that are known to be over since; clock "ours"
        when the results' times are the brain's own."""
        w, ask = self.world, ask or {}
        self.ask = ask
        console.apply_control(w, self.reg.activities)
        relay.log_tokens(w, w["relay"]["seq"], usage, w["relay"].get("note", ""))
        self._take_in(results, strays)
        known = json.dumps(w.d)                 # what is known before anything is decided
        try:
            out = self._decide(any(r.error == RATE_LIMITED for r in results))
            (w["battle"] or {}).pop("crashed", None)
            self._record(out)
        except Exception:
            out = self._undo(known)
            if out is None:
                raise
        return out

    def _take_in(self, results, strays):
        """What the request brings: what became of the last batch's calls, then the results, to everything that
        reads them. One reader that fails on a result does not cost the others theirs."""
        w = self.world
        takers = [("the call ledger", self._ledger), ("the world model", w.absorb), ("the combat tools", self.combat.absorb)]
        for name, take in takers + [(a.name, lambda rs, a=a: a.on_result(w, rs)) for a in self.reg.activities.values()]:
            try:
                take(results)
            except Exception as err:  # noqa: BLE001
                w.event("error", f"{name} could not take a result in: {err!r}"[:300], about="crash")
        for r in results:
            if r.error and r.error != RATE_LIMITED:
                w.event("error", f"{r.endpoint}: {r.error}", about="call")
        if strays:
            self.budget.stray(strays)
            w.event("finding", f"the relay made {strays} call(s) the batch did not ask for", about="relay")

    def _ledger(self, results):
        """What became of the last batch's calls, from who the request says has which batch. Evidence that a
        loose batch is over comes first. Then the last batch, by what the request positively says of it:
          handed in     the relay asking holds it: it was printed to that relay, and that relay is back
          gone          it was printed to a relay that has been replaced since: loose, under that relay's token
          never printed its `brain next` died before it had the answer down, or it grew old unprinted: counted
                        from now all the same
          not on record none of these: loose, with no relay to its name. Not knowing who has a batch is not
                        knowing that nobody has it (review of efa79808, finding 2: a client file without the
                        record, an older one for one, made a printed batch count as never printed)
        A caller that says nothing of who has what (a test that drives the brain itself) is the relay back;
        but not one that says, in an older version's word, that the batch was lost."""
        w, ask, last = self.world, self.ask, self.world["budget"].get("batch")
        self.evidence(ask)
        held = ask.get("held")
        if ("held" not in ask and not ask.get("lost")) or (held and held.get("id") == last):
            self.budget.settle(results, w["relay"].get("last_batch") or [], ask.get("clock") == "ours")
            return
        holder = next((g for g in ask.get("gone") or [] if isinstance(g, dict) and g.get("id") == last), None)
        if holder:
            self.budget.settle(holder=holder.get("token"))
        elif last is not None and last in (ask.get("unprinted") or []):
            self.budget.settle(asked=())
        else:
            self.budget.settle(holder=None)

    def evidence(self, ask):
        """The request's word that held batches are over: a replaced relay came back, or the operator says one
        was stopped. Each row names one batch by its id, so taking it twice changes nothing, and it never
        reaches a batch that went loose after it was said. So it is taken from every request, also one that is
        otherwise answered from its receipt."""
        for row in ask.get("ended") or []:
            if isinstance(row, list) and len(row) >= 2:
                n = self.budget.ended(row[0], row[1])
                if n and row[3:4] == ["stopped"]:
                    self.world.event("setting_changed", f"the operator says {row[2] or 'the relay of batch ' + str(row[0])} "
                                                        f"has been stopped: {n} held call(s) are counted from then",
                                     about="budget")

    def _undo(self, known):
        """The tick failed. The batch will not reach the relay, so nothing it planned was sent: back to what
        was known. In a fight that has now failed twice running, the last resort's batch; else None, and the
        request is noted as answered with no batch, so the same request gets the same again. Either way what
        the request brought, the count of failures and the receipt are on disk before the request is answered:
        the next brain may be a new one (review of 442a6311, finding 3: a brain started by `brain next` itself
        kept them in memory only, so every failure was the first and the last resort never came)."""
        w = self.world
        w.d = json.loads(known)
        fight = w["battle"]
        if fight:
            fight["crashed"] = fight.get("crashed", 0) + 1
            if fight["crashed"] > 1:            # it has failed twice: the turn is played from what is known
                out = self._last_resort()
                if out:
                    return out
                w["battle"].pop("inbox", None)  # not even that: the same read is not tried a third time
        self._receipt(None)
        self._save()        # what the request brought, the count and the receipt: kept before it is answered
        return None

    def _save(self):
        """The world model to disk. When that fails the brain goes on with what it has in memory, and says so."""
        try:
            self.world.save()
        except Exception as err:  # noqa: BLE001
            _crashed(self, self.world.live, f"the world model could not be saved: {err!r}")

    def _last_resort(self):
        """The fight's tick has failed twice running. Whatever broke it (review of c0006266, finding 1: a log
        line the tick could not read stayed in the fight's state, and every tick after it failed), the turn is
        not lost to it: the best line the turn has, or a basic action, goes out from the last good read, with a
        plain read behind it. None when even that cannot be made; the tick then fails as before."""
        w, crash = self.world, traceback.format_exc()
        known = json.dumps(w.d)
        try:
            act = self.reg.activities["battle"]
            p = act.last_resort(w)
            steps = self._compose(act, p)
            if steps is None:
                raise ValueError("the gates refused the last resort")
            steps, hold, _ = self._paced(steps, p.lane, 0.0)
            out = {"steps": steps, "hold": hold, "stop": None, "activity": act.name, "note": p.note, "queue": []}
            _crashed(self, w.live, crash)
            self._record(out)
            return out
        except Exception:  # noqa: BLE001
            w.d = json.loads(known)
            return None
    def rank(self):
        """The activities that can act now, best first: by priority class, then by value times the goal's weight
        (design 4.4). A paused player only fights. An activity that cannot even say whether it can act is set
        aside like one whose plan failed; the fight is never set aside."""
        w, ctl = self.world, self.world["control"]
        weights = {**C.goals()["weights"], **ctl["goal_weights"]}
        blocked, acts = w.own("brain").setdefault("blocked", {}), []
        for a in self.reg.activities.values():
            if (not ctl["activities"].get(a.name, True) or blocked.get(a.name, 0) > w.now
                    or getattr(a, "rides", False) or (a.priority != "battle" and ctl["paused"])):
                continue
            try:
                if a.available(w):
                    acts.append((CLASSES.index(a.priority), -a.value(w) * weights.get(a.goal, 1.0), len(acts), a))
            except Exception as err:  # noqa: BLE001
                if a.priority == "battle":
                    raise
                self._set_aside(a, f"it could not say whether it can act ({err!r})")
        return [x[-1] for x in sorted(acts, key=lambda x: x[:3])]

    def _set_aside(self, act, why):
        self.world.event("error", f"{act.name}: {why}; set aside for {BLOCK_FOR:.0f} s"[:300], about="crash")
        self.world.own("brain")["blocked"][act.name] = self.world.now + BLOCK_FOR

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
            steps, hold, waited = self._paced(steps, "recovery" if p.tag == "fight_end" else p.lane, hold)
            return {"steps": steps, "hold": hold, "stop": None, "activity": act.name,
                    "note": p.note + (f" (paced {waited}s)" if waited else ""),
                    "queue": [(a.name, a.priority, 0) for a in ranked[i + 1:]]}
        why = "paused" if w["control"]["paused"] else "nothing to do"
        return {"steps": [], "hold": IDLE_HOLD, "stop": None, "note": why, "activity": None, "queue": []}

    def _paced(self, steps, lane, hold):
        """A plan's steps under the call budget: (the steps, the wait in front of them, the seconds paced). When
        the minute has room for none of the calls the plan asked for, the relay is not sent straight back for
        the same answer: it waits. Every path that makes a batch comes through here (review of efa79808,
        finding 3: the last resort did not, and answered with nothing and no wait, again and again).

        The ledger has placed the last batch before any plan is made (_ledger). Should a batch still be out
        here all the same, it is held: the budget's own rule, that a batch being paced means the last one is
        back, is for a caller that drives the budget by itself, and the brain does not lean on it."""
        wanted = any("call" in x for x in steps)
        self.budget.settle(holder=None)           # a batch still out here was never placed: it is not on record
        steps, waited = self.budget.pace(steps, lane, self.world.now + hold)
        steps, hold = _lead(steps, hold)
        if wanted and not any("call" in x for x in steps):
            hold = max(hold, C.RATE_BACKOFF)
        return steps, hold, waited

    def _plan(self, act):
        """The activity's plan. A fight's plan that fails fails the tick (which is undone, and the turn's clock
        takes over). Any other activity that fails is set aside for a minute and the next one is asked, so one
        bad scan or reply cannot stop the player."""
        try:
            return act.plan(self.world)
        except Exception as err:  # noqa: BLE001
            if act.priority == "battle":
                raise
            self._set_aside(act, f"its plan failed ({err!r})")
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
                try:
                    if w["control"]["activities"].get(rider.name, True) and rider.available(w):
                        extra = rider.plan(w)
                        if extra and self.gates.screen(extra.steps, w, rider.name)[0]:
                            steps += extra.steps
                except Exception as err:  # noqa: BLE001  (a rider never costs the batch it rides on)
                    self._set_aside(rider, f"its plan failed ({err!r})")
        for s in steps:
            if "call" in s:
                self.gates.sent(s, w)
        return steps

    def _record(self, out):
        """Book-keeping after a decision: the relay's state, the console's files, the world model on disk."""
        w, r = self.world, self.world["relay"]
        if not out["stop"] and out["hold"] <= 0 and not any("call" in x for x in out["steps"]):
            out["hold"] = C.RATE_BACKOFF        # nothing to do and no wait would bring the relay straight back
        prev = r.get("activity")
        if prev and prev != out["activity"] and prev not in QUIET:
            w.event("activity_done", f"{prev}: {r.get('note', '')}", activity=prev)
        r.update(seq=r["seq"] + 1, activity=out["activity"], note=out["note"], issued_at=w.now + out["hold"],
                 expect=None if out["stop"] else relay.seconds(out["steps"]), stalled=False,
                 last_batch=[{k: s[k] for k in ("call", "input")} for s in out["steps"] if "call" in s])
        w["budget"]["batch"] = self.ask.get("id")                   # the batch whose calls are out: its request's id
        self._receipt(out)
        try:
            console.write_status(w, self.budget, out["activity"], out["note"], out["queue"])
        except Exception as err:  # noqa: BLE001  (the console's file is not worth a batch)
            w.event("error", f"the status file could not be written: {err!r}"[:300], about="crash")
        w.save()

    def _receipt(self, out):
        """Keep the answer to this request beside what it changed (it is saved, or lost, in the same write)."""
        if self.ask.get("relay") is not None:
            self.world["relay"]["answered"] = {"relay": self.ask["relay"], "seq": self.ask.get("seq"),
                                               "id": self.ask.get("id"), "at": self.world.now,
                                               "batch": _wire(out) if out else None}

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


def _wire(out):
    """A batch as it is written for `brain next`."""
    return {"stop": out["stop"], "hold": out["hold"],
            "steps": [{k: s[k] for k in ("call", "input", "select")} if "call" in s else s for s in out["steps"]]}


def _after_crash(brain):
    """What a relay is told when the tick crashed: come back in a moment (sooner in a fight)."""
    return {"steps": [], "hold": 1.0 if brain.world.in_battle() else 3.0, "stop": None}


def _answered(brain, req):
    """The answer this very request already had, when it is made again: its `brain next` died before it had
    the answer down, and the results it carries are in the world model already (review of c0006266, finding 3:
    they were applied a second time). False for a request older than the last one answered for the same relay:
    it is dropped. None for a request that is new."""
    done = brain.world["relay"].get("answered") or {}
    if req.get("relay") is None or req["relay"] != done.get("relay") or not isinstance(done.get("seq"), int):
        return None
    if req["seq"] < done["seq"]:
        brain.world.event("finding", f"request {req['seq']} came after request {done['seq']} of the same relay "
                                     f"was answered; it is dropped", about="relay")
        return False
    if req["seq"] > done["seq"]:
        return None
    batch = dict(done["batch"] or _after_crash(brain), id=done.get("id"))   # the batch it made then, not a new one
    batch["hold"] = round(max(0.0, batch["hold"] - (brain.world.now - done["at"])), 1)   # what is left of the wait
    return batch


REQUEST = ("seq", "id", "relay", "held", "gone", "ended", "unprinted")
"""What every request of this version's `brain next` carries: its number, its id, its relay, and what that relay
knows of who has which batch."""


def serve(brain, live, path):
    """A request file as a running player meets it: the resident brain looking through live/inbox, or `brain
    next` answering for itself. Only a request this version's `brain next` wrote is answered. Any other file
    there was left by an older version (or is no request at all): it is removed unanswered, and that is said.
    Its `brain next` is long gone, and what it does not say must not be read as if it had said it (review of
    426a9fba, finding 1: a request from before, with no word of who held the last batch, was answered by a
    brain that came home, and that batch was taken to be back)."""
    req = relay.read(path)
    if isinstance(req, dict) and all(k in req for k in REQUEST):
        return answer(brain, live, path)
    with contextlib.suppress(OSError):
        os.unlink(path)
    brain.world.event("finding", f"{os.path.basename(path)} is not a request of this version's `brain next`: "
                                 f"it is removed and not answered", about="relay")


def answer(brain, live, path):
    """Answer one request file with a batch file: the one with the request's own number and id, so an answer
    never reaches a `brain next` that asked something else. A tick that crashes still answers: the relay is told
    to come back in a moment (sooner in a fight), and the crash is written down for Duet (live/crash.log and an
    error event). The brain has undone what that tick decided, and saved the rest.

    This takes any request: a test may drive the brain with a bare one. A running player comes through
    `serve`, which lets through only what its own `brain next` wrote."""
    req = relay.read(path)
    if req is not None:
        out = _answered(brain, req)
        if out is not None and req.get("ended"):                   # nothing is run again, but word that a held
            brain.evidence(req)                                    # batch is over is never dropped unread
            brain._save()
        if out is None:
            try:
                out = dict(_wire(brain.handle(relay.unpack(req.get("results")), req.get("usage"),
                                              req.get("strays", 0), ask=req)), id=req.get("id"))
            except Exception:  # noqa: BLE001  (a relay left without a batch loses turns; a logged crash does not)
                out = _after_crash(brain)
                _crashed(brain, live)
        if out:
            relay.write(relay.batch_path(live, req["seq"], req.get("id")),
                        dict(out, seq=req["seq"], relay=req.get("relay"), request=req.get("id")))
    with contextlib.suppress(OSError):          # only the file that was read: never a newer request
        os.unlink(path)


def _crashed(brain, live, text=None):
    text = text or traceback.format_exc()
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
            serve(brain, live, path)
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
    transcript's path or None). Nothing of this batch is removed here: a `brain next` that dies before the
    brain has answered leaves the results where the next one finds them."""
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
        if not name.startswith(f"put-{token}-"):
            os.unlink(os.path.join(inbox, name))                   # a result for any other batch is dropped
            continue
        row = relay.read(os.path.join(inbox, name))                # this batch's stay until the brain has them
        if row and not path:
            results.append(relay.unpack([row])[0])
    return results, usage, strays, path


def _taken(live, token):
    """The brain has this batch's results: the ones handed in with `brain put` can go."""
    for path in glob.glob(os.path.join(live, "inbox", f"put-{token}-*.json")):
        with contextlib.suppress(OSError):
            os.unlink(path)


@contextlib.contextmanager
def _client(live):
    """The lock on live/client.json: who the relay is, and the batch it is owed. One `brain next` at a time reads
    it, talks to the brain and writes it back, so a relay that takes over and one that is still waiting cannot
    each write over the other (AP1 re-review, finding 3)."""
    with open(os.path.join(live, "client.lock"), "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


SUPERSEDED = "STOP superseded: another relay has taken over"
RETRY_IN = 5.0            # s before a relay asks again when the brain gave no answer


def _who(client):
    """client.json, in the shape this code writes: a file from an older version, or one that was edited, never
    makes a batch look held or gone that this code did not print, never has a batch printed that this code did
    not store, and never stops `brain next` from running. What is dropped here is not taken for its opposite:
    a batch that this file says nothing of is, to the brain, not on record."""
    state = relay.read(client)
    state = state if isinstance(state, dict) else {}
    if not _a_relay(state):
        for k in ("relay", "token", "seq"):                        # no relay is known by such a file: the next
            state.pop(k, None)                                     # `brain next` with no token starts one afresh
    state["calls"] = state["calls"] if isinstance(state.get("calls"), list) else []
    state["pending"] = state.get("pending") if _a_waiting_batch(state.get("pending")) else None
    state["held"] = state.get("held") if _a_batch(state.get("held")) else None
    state["gone"] = [g for g in state.get("gone") or [] if _a_batch(g)]
    state["ended"] = [e for e in state.get("ended") or [] if _a_word(e)]
    state["unprinted"] = [u for u in state.get("unprinted") or [] if isinstance(u, str)]
    return state


def _a_relay(state):
    """The relay that is running, as client.json names it: its name, its token, its last request's number."""
    return (isinstance(state.get("relay"), str) and isinstance(state.get("token"), str)
            and isinstance(state.get("seq"), int) and not isinstance(state.get("seq"), bool))


def _a_batch(g):
    """A printed batch, as client.json keeps it under held and gone: its relay's token and its id."""
    return isinstance(g, dict) and isinstance(g.get("token"), str) and isinstance(g.get("id"), str)


def _a_waiting_batch(p):
    """A batch the brain made that is waiting to be printed, as client.json keeps it under pending."""
    return (isinstance(p, dict) and isinstance(p.get("id"), str) and isinstance(p.get("seq"), int)
            and isinstance(p.get("steps"), list) and isinstance(p.get("ready_at"), (int, float)) and "stop" in p)


def _a_word(e):
    """Word that a batch is over, as client.json keeps it under ended: [the batch, when, whose, how]."""
    return (isinstance(e, list) and len(e) == 4 and isinstance(e[0], (str, int)) and not isinstance(e[0], bool)
            and isinstance(e[1], (int, float)) and e[3] in ("back", "stopped"))


def next_batch(live=None, token=None, out=sys.stdout, sleep=time.sleep):
    """`brain next [token]`: hand in the results, wait for the batch (answering it here if no brain is running),
    spend the brain-side wait, print the batch.

    Without a token the relay is new: it is given a name and one line to run, and nothing is taken from it yet.
    With the token of the batch it was last given, it hands that batch in. Any other token is a relay that has
    been replaced (it is told to stop) or a `brain next` run twice (it is given the current line again).

    A batch the brain has made is kept in client.json until a relay has it. The brain-side wait is spent with
    the lock released, so a replacement can take over meanwhile; whoever owns the relay when the wait is over
    gets the batch, and a relay that was replaced during it is told to stop and prints no call.

    client.json says who has what: held is the batch printed to the relay that is running, from the moment it
    is printed until the brain has taken its results; gone are the batches that were held by relays replaced
    since; ended is the evidence, not yet given to the brain, that one of those is over."""
    live = live or C.live_dir()
    os.makedirs(os.path.join(live, "inbox"), exist_ok=True)
    client = os.path.join(live, "client.json")
    with _client(live):
        state = _who(client)
        said = _greet(client, state, token)
        if said:
            out.write(said + "\n")
            return 0
        me, (pending, hold) = state["relay"], _exchange(live, client, state, sleep)
    if pending is None:                                            # the brain gave no answer: nothing has moved,
        sleep(hold)                                                # and the relay asks the same thing again
        out.write(relay.next_line(token) + "\n")
        return 0
    wait = hold if hold is not None else pending["ready_at"] - time.time()
    if wait > 0:
        sleep(wait)
    with _client(live):
        state = _who(client)
        if state.get("relay") != me:
            out.write(SUPERSEDED + "\n")                           # the batch stays for the relay that took over
        elif (state.get("pending") or {}).get("id") != pending["id"]:
            # the batch this call waited for is not the one that is owed any more: another call of this relay
            # has it, or it grew too old and the brain was asked afresh. Print nothing of it; come back.
            out.write(relay.next_line(state["token"]) + "\n")
        else:
            token = f"{me}-{pending['seq']}"
            calls = [[x["call"], x["input"]] for x in pending["steps"] if "call" in x]
            state.update(seq=pending["seq"], token=token, issued_at=time.time(), pending=None, calls=calls,
                         held={"token": token, "id": pending["id"]} if calls else None)   # printed: this relay's
            relay.write(client, state)
            out.write("\n".join(relay.lines(pending["steps"], pending["stop"], token,
                                            echo=not state.get("transcript"))) + "\n")
    return 0


def _greet(client, state, token):
    """What to say to a `brain next` that hands nothing in: a new relay gets its name and its first line, a
    replaced one is told to stop, a second call for the same batch gets the current line. None for a relay that
    is handing in the batch it was last given.

    A new relay replaces the one that was running. A batch that one still holds (it was printed to it, and the
    brain has not had its results) is gone with it. When a replaced relay comes back with the very token of a
    batch that is gone, that batch is over: that is noted (ended) for the brain. No other token proves anything:
    a relay that asked and was replaced before its batch was printed held nothing (review of 442a6311, finding
    2: such a relay's token carried the number of a batch another relay held, and released it)."""
    if token is None:
        gone = (state.get("gone") or []) + ([state["held"]] if state.get("held") else [])
        state = {"relay": os.urandom(3).hex(), "seq": state.get("seq", 0), "calls": [], "transcript": None,
                 "new": True, "pending": state.get("pending"), "held": None, "gone": gone,
                 "ended": state.get("ended") or [], "unprinted": state.get("unprinted") or []}
        state["token"] = f"{state['relay']}-{state['seq']}"
        relay.write(client, state)
        return relay.next_line(state["token"])
    if token != state.get("token"):
        if token.split("-")[0] == state.get("relay"):
            return relay.next_line(state["token"])
        was = next((g for g in state.get("gone") or [] if g["token"] == token), None)
        if was:
            state["gone"].remove(was)
            state["ended"] = (state.get("ended") or []) + [[was["id"], time.time(), token, "back"]]
            relay.write(client, state)
        return SUPERSEDED
    return None


def _exchange(live, client, state, sleep):
    """Hand this relay's results to the brain and get the next batch, unless a batch is already waiting for a
    relay. The batch is written into client.json before anything else happens to it. Returns (the batch, the
    brain-side wait still to spend, or None for one that was already waiting); or (None, a wait) when the brain
    gave no answer: then nothing is marked as handed in, and no evidence is dropped."""
    results, usage, strays, path = _collect(live, state, sleep)
    if state.get("handed") == state["token"]:                      # this batch's results have gone in already
        results, usage, strays = [], {}, 0
    pending, hold = _owed(state), None
    if pending is None:
        seq, rid = state["seq"] + 1, os.urandom(4).hex()
        _sweep(live)
        req = relay.request_path(live, seq, rid)
        ask = {"seq": seq, "id": rid, "relay": state["relay"], "results": relay.pack(results), "usage": usage,
               "strays": strays, "at": time.time(), "clock": "transcript" if path else "ours",
               "held": state.get("held"), "gone": state["gone"], "ended": state["ended"],
               "unprinted": state["unprinted"]}
        # On record before it is asked: whatever the brain makes of this request has not been printed. If this
        # `brain next` dies now, the next one can say so, and the brain need not hold that batch for anyone.
        state["unprinted"] = state["unprinted"] + [rid]
        relay.write(client, state)
        relay.write(req, ask)
        batch = _await(live, seq, rid, req, sleep)
        if batch is None:
            return None, RETRY_IN
        hold = batch["hold"]
        pending = {"id": batch.get("id") or rid, "seq": seq, "steps": batch["steps"], "stop": batch["stop"],
                   "ready_at": time.time() + hold}
        state.update(held=None, ended=[], unprinted=[])            # the brain has them, saved beside its answer
    state.update(pending=pending, transcript=path, new=False, handed=state["token"])
    relay.write(client, state)
    _taken(live, state["token"])                                   # and only now are they no longer needed here
    return pending, hold


def _sweep(live):
    """Called with the client's lock held, when no `brain next` is waiting on the brain: a request or a batch
    file that is there now was left by one that died. Such a request is not answered late, and such a batch is
    never printed."""
    for path in glob.glob(os.path.join(live, "inbox", "req-*.json")) + glob.glob(os.path.join(live, "outbox", "batch-*.json")):
        with contextlib.suppress(OSError):
            os.unlink(path)


def _owed(state):
    """A batch the brain made that no relay has had yet (its relay was replaced while it waited), unless it has
    waited too long to be worth sending: then the brain is asked afresh, under the next number. A batch is known
    by its own id, so a call that is still waiting on the old one cannot publish it in the new one's place
    (review of 0d10b7c6, finding 3)."""
    pending = state.get("pending")
    if pending and time.time() - pending["ready_at"] > C.STALE_OUTBOX:
        state["seq"] = max(state.get("seq", 0), pending["seq"])    # its number is not used again
        state["unprinted"] = state["unprinted"] + [pending["id"]]  # it was not printed, and now never will be
        state["pending"] = None
        return None
    return pending


def _await(live, seq, rid, req, sleep, limit=90.0):
    """The answer to this request. When no brain holds the lock, this process answers and then starts one."""
    t0, mine = time.time(), relay.batch_path(live, seq, rid)
    while time.time() - t0 < limit:
        batch = relay.read(mine)
        if batch is not None:
            os.unlink(mine)
            if batch.get("request") == rid:                        # the answer to this very request
                return batch
        lock = _lock(live)
        if lock is not None:                                       # nobody is home: answer here, then start a brain
            try:
                if os.path.exists(req):
                    serve(Brain(live), live, req)
            finally:
                lock.close()
            if os.environ.get("TNR_PLAYER_NO_DAEMON") != "1":
                subprocess.Popen([sys.executable, "-m", "player.brain", "run"], cwd=C.ROOT, start_new_session=True,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            continue
        sleep(C.BRAIN_WAIT)
    return None


def stopped(live, names, out=sys.stdout):
    """`brain stopped TOKEN ...`, or `brain stopped all`: the operator's word that a relay which did not hand
    its batch in has been stopped and will make no call from now on. The brain was holding that batch against
    the minute; it now counts those calls from this moment, so they leave a minute from now.

    The word covers the batches that are held at the moment it is said, each by its id, and is kept that way:
    it is never read again as "whatever is held by then" (review of efa79808, finding 1). `all` is every held
    batch: those of the relays replaced so far, and those the ledger holds for a relay that is not on record.
    It is never the batch of the relay that is running, and never one that goes loose later. A batch can also
    be named by its id, as the listing shows it: an older version's batch has a number for one, and is named
    by that number (review of 426a9fba, finding 2: the number typed did not match the number kept). With no
    name: the batches that are held, and nothing is changed.

    Say it only of relays that are known to be stopped: this is the one statement the ledger takes on trust."""
    client = os.path.join(live, "client.json")
    with _client(live):
        state, now = _who(client), time.time()
        held = _held(live, state)
        said = {b: t for b, t in held.items() if "all" in names or t in names or str(b) in names}
        if said:
            state["gone"] = [g for g in state["gone"] if g["id"] not in said]
            state["ended"] = state["ended"] + [[b, now, t, "stopped"] for b, t in said.items()]
            relay.write(client, state)

    def name(batch):
        return held[batch] or f"batch {batch}"
    known = {str(b) for b in held} | {t for t in held.values() if t}
    out.write(json.dumps({"stopped": [name(b) for b in said], "all": "all" in names,
                          "not_held": [n for n in names if n != "all" and n not in known],
                          "still_held": [name(b) for b in held if b not in said]}) + "\n")
    return 0


def _held(live, state):
    """Every batch that is held now, by its id, with the token of the relay that has it (None when that is not
    on record): those the client's file says went with a replaced relay, and those the brain's saved ledger
    holds, whoever has them. Never the batch of the relay that is running: that one is out, not loose."""
    held = {g["id"]: g["token"] for g in state["gone"]}
    ledger = ((relay.read(os.path.join(live, "world.json")) or {}).get("budget") or {}).get("calls") or []
    for c in ledger:
        if c[2:3] == ["loose"] and len(c) > 3 and c[3] is not None:
            held.setdefault(c[3], c[5] if len(c) > 5 else None)
    return held


def put(live, token, index, text):
    """`brain put TOKEN N`, with the result on standard input: call N (from 1) of batch TOKEN, from a relay whose
    transcript cannot be read. A result for any batch but the one in progress is dropped."""
    state = _who(os.path.join(live, "client.json"))
    calls = state["calls"]
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
    if cmd == "stopped":
        return stopped(live, argv[1:], sys.stdout)
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
