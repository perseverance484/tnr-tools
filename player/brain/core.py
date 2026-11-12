"""The brain itself: one tick, from the results a relay brings to the batch it takes away (Brain.handle), and
what is kept of it. The package's own page (player/brain/__init__.py) says how the pieces fit.
"""
import json
import os
import time
import traceback

from .. import config as C
from .. import console, registry, relay
from ..budget import Budget
from ..combat import Combat
from ..gates import Gates
from ..registry import CLASSES
from ..world import RATE_LIMITED, World

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
        self._take_over()
        self.ask = {}                                               # what the request being answered said
        for a in self.reg.activities.values():
            a.combat, a.budget, a.gates = self.combat, self.budget, self.gates
        if not self.world["records"].get("handover"):               # once: carry on from where the pilot stands
            took = self.combat.pilot_handover()
            self.world["inventory"].update({k: took[k] for k in ("full_potion_uid",) if k in took})
            for k in ("lost_to", "skip"):
                self.world["opponents"][k].update(took.get(k) or {})
            self.world["records"]["handover"] = True

    def _take_over(self):
        """The ledger as this brain finds it. One that a brain of this protocol kept carries its number, and is
        taken as it stands. Any other that was on disk was kept by another version, by rules this one cannot
        check, and may be short of calls that are still out: a minute's calls are held until the operator has
        spoken (Budget.taken_over; review of 29797ba0). A first start has no ledger to take over. The number is
        on disk with the first thing this brain saves; a brain that ends before that leaves the ledger as it
        was, and the next one takes it over afresh."""
        ledger = self.world["budget"]
        if relay.ours(ledger):
            return
        if self.world.found:
            self.budget.taken_over(self.world.found, self.world.found_at)
            self.world.taken_over = True                            # counted with the first save (World.save)
        ledger["protocol"] = relay.PROTOCOL

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
            self.world["relay"]["answered"] = {"protocol": relay.PROTOCOL, "relay": self.ask["relay"],
                                               "seq": self.ask.get("seq"), "id": self.ask.get("id"),
                                               "at": self.world.now, "batch": _wire(out) if out else None}

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


def _wire(out):
    """A batch as it is written for `brain next`."""
    return {"stop": out["stop"], "hold": out["hold"],
            "steps": [{k: s[k] for k in ("call", "input", "select")} if "call" in s else s for s in out["steps"]]}


def _crashed(brain, live, text=None):
    text = text or traceback.format_exc()
    with open(os.path.join(live, "crash.log"), "a", encoding="utf8") as f:
        f.write(f"--- {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n{text}\n")
    try:
        brain.world.event("error", "the brain's tick crashed: " + text.strip().splitlines()[-1], about="crash")
    except Exception:  # noqa: BLE001
        pass
