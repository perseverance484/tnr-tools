"""The call budget and the battle turn clock (design 4.6).

The connector allows 30 calls a minute for the whole account. No call is scheduled past that, whatever its lane: a
31st call would only be refused. What the lanes decide is who gives way first:
  battle    a fight in progress. My turn's actions may use the whole minute. No read takes the room of a turn's
            actions (TURN_ACTIONS). The reads that only watch the fight (the poll behind my actions, the polls of
            his turn) leave TURN_RESERVE free, room for a turn and the read behind it; but for that reserve the
            fight is never left unread longer than BLIND_MAX.
  recovery  the Full Potion at the end of a fight, the hospital. May use the whole minute.
  world     everything else: at most WORLD_CAP calls in any rolling minute, and none while a fight is on. It leaves
            TURN_RESERVE free too, so a fight that starts always finds room for its opening read and a first turn.
When the minute is full all the same, the call waits for room. A wait in front of an action or a recovery call, or
one that leaves the fight unread longer than BLIND_MAX, is written down as a finding: the limit is never passed
silently, and a moment when the rules cannot all be met is on record.

No batch makes the relay sit on answers it already has: a watching read that would have to wait more than a poll's
gap behind the calls in front of it is left out of the batch, and the brain asks again on the next tick (so the
answers to my actions come back at once). The brain spends a wait in front of a batch's first call itself.

Every call the brain issues is written down, so a brain that restarts still knows what the last minute cost. A
call is in one of three states, and only the brain's own clock moves it from one to the next:
  out     issued in the last batch. It is admitted at the earliest moment it could run (the batch's start and the
          waits in front of it, with no time allowed for the calls themselves), and it counts in every minute.
  settled its relay came back with the batch (`brain next` is a batch's last line, so every call of it has run by
          then). It is counted from the moment the relay came back. A time the relay's transcript gives for an
          answer is not used: that is another clock, and one that reads early would let the call leave the minute
          early. Only a result handed in with `brain put` carries a time of the brain's own clock, and is counted
          from it. A settled call leaves the minute sixty seconds later.
  loose   its relay was replaced while it had the batch, so nothing says when its calls ran, or whether they still
          will. They count in every minute, for as long as that takes, until there is evidence that they are
          over: the replaced relay comes back (it is told to stop: its calls had run by then), or the operator
          says that relay has been stopped (`brain stopped`). From that moment they are settled, and leave a
          minute later. No length of time is evidence (review of 442a6311: a hold that ended by itself let a
          call made just before its end go uncounted). After LOOSE_ALERT a held batch is raised as a stall.
A batch is known by the id of the request that made it, and a loose call carries that id and the token its relay
had: only a report for that very batch settles it. A batch is also loose when nothing on record says who has
it: not knowing is not knowing that nobody has it (review of efa79808, finding 2).

A ledger that another version of the player kept cannot say what is out: that version may have let calls go
that its relays can still make (442a6311 did, after fifteen minutes), and a call that is not written down cannot
be held. So a brain that takes such a ledger over holds a whole minute's calls, CALL_LIMIT of them, under an id
of their own (Budget.taken_over). They are loose like any other: no call is sent until the operator says the
relays from before the update have been stopped, and from that word they count for sixty seconds more (review of
29797ba0). The id is made from the file that was taken over, so the word names that one hold: it lets go neither
the hold of a later update nor anything else, and it can be said before the brain has started as well as after.

So with a relay that is slow, uneven, wrong about the time, or replaced in the middle of a batch, the ledger is
never ahead of the account's real minute. The price is room: calls held for relays that never come back use up
the minute until the operator says they are stopped. A call that then cannot fit under the limit, however long
it waits, is not sent, and that is raised as a stall.

The turn clock: a turn of mine starts (T) when a read first shows it. The planner is cut off at T+15 s and the best
line so far is fired; a missing exact read is not waited for past T+12 s; the actions are out by T+20 s. Every
turn's timing is logged (turns.jsonl) with how long the fight went unread before the turn was seen, and with how
the turn ended: acted, missed, or unresolved. A turn that lands within 20 s of the game's limit is a finding.
"""
import os

from . import calls as K
from . import config as C

HOW_TO_RELEASE = ("When that relay is known to have been stopped, say so: python3 -m player.brain stopped TOKEN "
                  "(or: all, when every relay but the one running is known to be stopped).")
TURN_ACTIONS = 5            # the most actions one turn of mine sends: no read ever takes their room
TURN_RESERVE = TURN_ACTIONS + 3     # kept free for my turn while the fight is only watched: its actions and a poll
WINDOW = 60.0
BLIND_MAX = 2 * C.POLL_GAP_MAX      # s: the longest the reserve may keep the fight unread


NEVER = float("inf")       # no wait is long enough: the room is taken by calls with no time yet
UPDATE = "update-"         # how the id of the hold on a ledger taken over from another version begins


def _state(c):
    return c[2] if len(c) > 2 else None


def _until(times, t, ceiling):
    """Seconds from t until fewer than `ceiling` of these calls are inside the minute; NEVER when none may be."""
    if ceiling <= 0:
        return NEVER
    live = [x for x in times if x > t - WINDOW]
    if len(live) < ceiling:
        return 0.0
    return live[len(live) - ceiling] + WINDOW + 0.5 - t


def is_poll(step):
    return bool((step.get("meta") or {}).get("poll"))


def _whose(c):
    """A loose call's relay, in words."""
    if str(c[3]).startswith(UPDATE):
        return f"the relays from before the update ({c[3]})"
    return f"relay {c[5]}" if c[5] else f"a relay that is not on record (batch {c[3]})"


def _orphan():
    """An id for a batch that has none on record, so that it can still be named when it is let go."""
    return "unknown-" + os.urandom(3).hex()


class Budget:
    def __init__(self, world):
        self.world = world
        self._shape()

    def _shape(self):
        """A ledger written by an earlier version of this code: a loose call gets the fields it has now (its
        batch, since when, whose). It stays loose; only an end by the clock, which it may have had, is dropped."""
        for c in self.world["budget"]["calls"]:
            if _state(c) == "loose" and len(c) != 6:
                c[2:] = ["loose", c[3] if len(c) > 3 and c[3] is not None else _orphan(), self.world.now, None]

    def _hist(self, now):
        """The calls that count at `now`: the settled ones of the last minute, and every call that is out or
        loose, however long ago it was admitted. A call with no time yet cannot have left the minute (review
        of 0d10b7c6, finding 1; review of 442a6311, finding 1)."""
        real = self.world.now
        kept = [c for c in self.world["budget"]["calls"] if _state(c) or c[0] > real - WINDOW]
        self.world["budget"]["calls"] = kept
        self._alert(kept, real)
        return [c for c in kept if _state(c) or c[0] > now - WINDOW]

    def _alert(self, calls, now):
        """A batch that has been loose for LOOSE_ALERT is raised once, with what the operator can do about it."""
        loose = {c[3]: c for c in calls if _state(c) == "loose"}
        told = [b for b in self.world["budget"].get("alerted") or [] if b in loose]
        for batch, c in loose.items():
            if batch not in told and now - c[4] > C.LOOSE_ALERT:
                told.append(batch)
                n = sum(1 for x in calls if _state(x) == "loose" and x[3] == batch)
                why = ("nobody has said that they are stopped" if str(batch).startswith(UPDATE)
                       else "it had a batch in hand and has not come back")
                self.world.event("stall", f"{n} call(s) of {_whose(c)} have been held against the minute for "
                                          f"{now - c[4]:.0f} s: {why}. {HOW_TO_RELEASE}", about="budget")
        self.world["budget"]["alerted"] = told

    def used(self, now=None, lane=None):
        """Calls that count in the minute (settled in it, out, or loose), in one lane or in all."""
        now = self.world.now if now is None else now
        return sum(1 for c in self._hist(now) if lane is None or c[1] == lane)

    def loose(self):
        """The batches held for relays that have not come back: [(the relay's token, or None when it is not on
        record; the batch's id; calls; held since), ...]."""
        groups = {}
        for c in self.world["budget"]["calls"]:
            if _state(c) == "loose":
                groups.setdefault((c[5], c[3], c[4]), []).append(c)
        return [(token, batch, len(cs), since) for (token, batch, since), cs in groups.items()]

    def taken_over(self, found, written):
        """This ledger was kept by another version of the player, and is now this brain's. What that version
        wrote down is kept and held as it stands. What it did not write down, or let go by a rule of its own,
        cannot be known: so a whole minute's calls are held as well, under an id of their own, until the
        operator says the relays from before the update have been stopped (`brain stopped`). found: the print
        of the file that was taken over (world.found), which makes the id. written: when that file was last
        written; the operator's word counts from when it was said, but never from before that. Returns the id."""
        now, batch = self.world.now, UPDATE + found
        self.world["budget"]["calls"] += [[written, "update", "loose", batch, now, None] for _ in range(C.CALL_LIMIT)]
        self.world.event("stall", f"this call ledger was kept by another version of the player, which may have "
                                  f"let go calls that its relays can still make. No call is sent until the "
                                  f"operator says that every relay from before the update has been stopped "
                                  f"(python3 -m player.brain stopped all, or: stopped {batch}). Calls start a "
                                  f"minute after that word.", about="budget")
        return batch

    def stray(self, n):
        """Calls the relay made that no batch asked for. They used the account's minute all the same."""
        self.world["budget"]["calls"] += [[self.world.now, "stray"] for _ in range(n)]

    def settle(self, results=(), asked=None, own_clock=False, holder=None):
        """What became of the last batch's calls.

        asked given (the batch's calls, in order): the relay that had the batch is back. Every call of it has run
        by now and is counted from now; with own_clock, the results' times are the brain's own (`brain put`), and
        an answered call is counted from its answer when that lies between its admission and now.

        asked None: the batch is given up. Its relay (holder: the token it had, or None when nothing on record
        says who has the batch) did not hand it in, so its calls are loose (review of c0006266, finding 2: they
        were taken to have run by now, and a relay that went on with them afterwards made a 31st call in a
        minute). A loose batch always has an id, so that evidence can name it."""
        now, out = self.world.now, [c for c in self.world["budget"]["calls"] if _state(c) == "out"]
        if asked is None:
            batch = self.world["budget"].get("batch")
            batch = _orphan() if batch is None else batch
            for c in out:
                c[2:] = ["loose", batch, now, holder]
            if out:
                self.world.event("finding", f"{len(out)} call(s) of {_whose(out[0])} count in every minute until "
                                            f"it comes back or is confirmed stopped: it did not hand its batch "
                                            f"in. {HOW_TO_RELEASE}", about="budget")
            return
        left = list(results) if own_clock and len(asked) == len(out) else []
        for i, c in enumerate(out):
            hit = next((r for r in left if r.endpoint == asked[i]["call"] and r.input == asked[i]["input"]), None)
            if hit:
                left.remove(hit)
            at = hit.at if hit and isinstance(hit.at, (int, float)) else now
            c[0] = at if c[0] <= at <= now else now
            del c[2:]

    def ended(self, batch, at):
        """There is evidence that batch `batch` is over as of `at`, by the brain's clock: its replaced relay came
        back, or the operator says that relay was stopped. Its calls are counted from then. Only the batch with
        that very id is settled, so evidence taken a second time, or after other batches have gone loose,
        settles nothing more (review of efa79808, finding 1: "every loose batch" was a word that grew with the
        ledger). Returns how many calls."""
        now, n = self.world.now, 0
        at = at if isinstance(at, (int, float)) and not isinstance(at, bool) else now
        mine = batch is not None and self.world["budget"].get("batch") == batch   # still out: not yet called loose
        for c in self.world["budget"]["calls"]:
            if (_state(c) == "loose" and batch is not None and c[3] == batch) or (_state(c) == "out" and mine):
                c[0] = at if c[0] <= at <= now else now
                del c[2:]
                n += 1
        return n

    def headroom(self, now=None):
        """World calls that could go right now."""
        now = self.world.now if now is None else now
        if self.world.in_battle():
            return 0
        return max(0, min(C.WORLD_CAP - self.used(now, "world"), C.CALL_LIMIT - TURN_RESERVE - self.used(now)))

    def free(self, now=None):
        """Calls left in the minute once the reserve for my turn is set aside."""
        return C.CALL_LIMIT - TURN_RESERVE - self.used(now)

    def _gap(self, hist, t, lane, step, n=1):
        """(seconds before n calls like this one may start at t, the part of that wait that is a finding).
        BLIND_MAX counts from now, the moment the brain last heard from the fight.

        A loose call has no time: it takes one place in every minute, and NEVER is the answer when the loose
        ones leave no place at all. The calls of the batch being paced count from the times they are given
        here: the relay makes them in order with the batch's waits between them, so they are never closer
        together than that."""
        timed = [x for x in hist if _state(x) != "loose"]
        held, times = len(hist) - len(timed), sorted(x[0] for x in timed)
        since, room = max(0.0, t - self.world.now), C.CALL_LIMIT - held - n + 1
        if lane == "recovery" or step.get("call") == "combat.performAction":
            limit = _until(times, t, room)
            return limit, limit
        floor = _until(times, t, room - TURN_ACTIONS)
        reserve = _until(times, t, room - TURN_RESERVE)
        if lane == "world":
            world = sorted(x[0] for x in timed if x[1] == "world")
            held_world = sum(1 for x in hist if _state(x) == "loose" and x[1] == "world")
            return max(reserve, _until(world, t, C.WORLD_CAP - held_world - n + 1)), 0.0
        if is_poll(step):
            floor = max(floor, min(reserve, max(0.0, BLIND_MAX - since)))
        return floor, floor if since + floor > BLIND_MAX else 0.0

    def pace(self, steps, lane, start=None):
        """Schedule a batch that the relay gets at `start` (now, or later when the brain holds it first). Returns
        (steps, waited): a call that does not fit in the minute gets a pause in front of it (see the module's
        notes for who gives way first), and a watching read that would have to wait long behind other calls is
        left out. Every call that stays is written down at the earliest moment it can run, marked as still out.

        A batch is paced when a relay asks for it. Unless the brain was told the last batch is given up, that is
        the relay that had it, back from it."""
        now = self.world.now
        self.settle(asked=())                                     # what is still out has run by now
        hist = self._hist(now)
        out, t, waited, called, shut = [], now if start is None else start, 0.0, False, []
        for s in steps:
            if "wait" in s:
                t += s["wait"]
                out.append(s)
                continue
            gap, forced = self._gap(hist, t, lane, s)
            if gap == NEVER:
                shut.append(s["call"])                            # no wait would make room for it: not sent
                continue
            if called and is_poll(s) and gap > C.POLL_GAP:
                continue                                          # left for the next batch: see the module's notes
            called = True
            if forced > 0:
                self._full(s["call"], forced)
            if gap > 0:
                out.append(K.wait(gap))
                t += gap
                waited += gap
            hist.append([round(t, 2), lane, "out"])
            out.append(s)
        if shut:
            held = sum(1 for c in hist if _state(c) == "loose")
            self.world.event("stall", f"{len(shut)} call(s) not sent ({', '.join(sorted(set(shut)))}): {held} call(s) "
                                      f"of relays that were replaced are held against the minute's "
                                      f"{C.CALL_LIMIT}. {HOW_TO_RELEASE}", about="budget")
        self.world["budget"]["calls"] = hist
        return out, round(waited, 1)

    def unsend(self, n):
        """The last n calls that pace wrote down are taken back: they are not in the batch after all (the run
        lock's lease ends before they would be made: Brain._paced)."""
        calls = self.world["budget"]["calls"]
        if n:
            assert all(_state(c) == "out" for c in calls[-n:]), "only calls that were just paced are taken back"
            del calls[-n:]

    def poll_hold(self, n_calls, hold):
        """How long the brain waits before a poll of his turn: at least `hold`, and until the poll's calls fit with
        the reserve for my own turn left free (for at most BLIND_MAX; after that only the account's limit holds
        it). The wait is spent in the brain, not by the relay."""
        now = self.world.now
        gap, forced = self._gap(self._hist(now), now, "battle", {"meta": {"poll": True}}, n_calls)
        if gap == NEVER:
            return max(hold, C.POLL_GAP_MAX)                      # pace will say that it cannot be sent
        if forced > 0:
            self._full("the poll of his turn", forced)
        return round(max(hold, gap), 1)

    def _full(self, what, seconds):
        self.world.event("finding", f"the minute's {C.CALL_LIMIT} calls are used: {what} waits {seconds:.0f} s",
                         about="budget", waited=round(seconds, 1))


# ---------------------------------------------------------------- the turn clock
def turn_open(state, rnd, now, unseen=None):
    """The clock of my turn in round rnd: started once, when a read first shows the turn. unseen: how long the
    fight had gone unread when it did (the turn began at most that long before T).

    What the turn keeps about its actions: sent and answered count the plan last issued, accepted counts every
    action of the turn the game took, unknown the ones whose answer was an error."""
    turn = state.get("turn")
    if not turn or turn.get("round") != rnd:
        turn = state["turn"] = {"round": rnd, "T": now, "unseen": unseen, "fired_at": None, "how": None,
                                "actions": 0, "from_last_read": False, "landed": False,
                                "sent": 0, "answered": 0, "accepted": 0, "unknown": 0}
    return turn


def planner_seconds(turn, now):
    """Seconds the planner may still take: it is cut off at T + BEST_LINE_AT. A turn's first plan gets
    PLAN_AT_LEAST whatever is left. It is late only when the turn waited for its read (a light read showed the
    turn, and the full one took its time or never came): that wait is not taken out of the planner whole. A
    plan that replaces the first gets what is left."""
    left = turn["T"] + C.BEST_LINE_AT - now
    return left if turn.get("fired_at") else max(C.PLAN_AT_LEAST, left)


def read_is_overdue(turn, now):
    """True once a missing exact read is no longer waited for (T + LAST_GOOD_READ_AT)."""
    return now >= turn["T"] + C.LAST_GOOD_READ_AT


def turn_fired(world, bid, turn, how, n_actions, from_last_read=False):
    """A plan for this turn goes out with this batch. (A tick that fails before the batch reaches the relay is
    undone as a whole by the brain, so a plan that was never sent is never left marked as fired.)"""
    now, first = world.now, not turn.get("fired_at")
    if turn.get("unknown") or turn.get("sent", 0) > turn.get("answered", 0):
        turn["doubt"] = True                          # the plan this one replaces may have landed, or not
    turn.update(fired_at=now, actions=n_actions, from_last_read=from_last_read, sent=n_actions, answered=0,
                unknown=0, looked=False, plans=turn.get("plans", 0) + 1)
    if first:                                         # the turn's timing is its first plan's; later ones add to it
        turn.update(first_fired_at=now, how=how)
    if first and now - turn["T"] > C.FIRE_BY:
        world.event("finding", f"round {turn['round']}: actions went out {now - turn['T']:.1f} s into the turn "
                               f"(the rule is {C.FIRE_BY:.0f} s)", about="turn", battle=bid)


def turn_owed(turn, refused, now):
    """On my turn with no read in hand: must a plan go out now, from the last good read? Not once the game has
    taken an action of this turn. Otherwise yes when the connector refused the read or an action, when every
    action sent came back refused, or when the read has been waited for long enough (T+12 s). The game checks an
    action against the battle's version, so a plan sent again from the same read cannot land twice."""
    if not turn or turn.get("landed") or turn.get("accepted"):
        return False
    waiting = turn.get("sent", 0) > turn.get("answered", 0)
    dead = turn.get("sent", 0) > 0 and not waiting and not turn.get("unknown")
    if refused or dead:
        return True
    # a plan whose answers never came back may have landed: one read is asked for after it before it is sent again
    return read_is_overdue(turn, now) and (not waiting or bool(turn.get("looked")))


def turn_outcome(turn, logged, ended=False):
    """How a turn of mine ended, from evidence only. acted: the game took an action (its answer, or my line in the
    battle log). missed: nothing was taken and nothing is outstanding. unresolved: an action went out and its
    answer never came back or was an error, or the fight ended, and the log does not settle it."""
    if turn.get("accepted") or logged:
        return "acted"
    if ended or turn.get("doubt") or turn.get("unknown") or turn.get("sent", 0) > turn.get("answered", 0):
        return "unresolved"
    return "missed"


def turn_closed(world, bid, turn, outcome, now=None):
    """The turn is over (a read shows the next state, or the fight ended). Log its timing and its outcome once;
    a missed turn is a stall, an unresolved or late one a finding."""
    if not turn or turn.get("landed"):
        return
    now = world.now if now is None else now
    turn["landed"] = True
    fired = turn.get("first_fired_at") or turn.get("fired_at")
    took = (fired - turn["T"]) if fired else None
    row = {"at": round(now, 1), "battle": bid, "round": turn["round"], "T": round(turn["T"], 1),
           "unseen": turn.get("unseen"), "fired_after": round(took, 1) if took is not None else None,
           "last_fired_after": round(turn["fired_at"] - turn["T"], 1) if turn.get("fired_at") else None,
           "plans": turn.get("plans", 0), "how": turn.get("how"), "actions": turn.get("actions"),
           "accepted": turn.get("accepted", 0), "from_last_read": turn.get("from_last_read"), "outcome": outcome}
    world._append("turns.jsonl", row)
    records = world["records"]
    if outcome == "missed":
        records["turns_missed"] = records.get("turns_missed", 0) + 1
        world.event("stall", f"MISSED TURN in {bid[:6]} round {turn['round']}: the game took no action of mine",
                    about="missed_turn", battle=bid)
    elif outcome == "unresolved":
        records["turns_unresolved"] = records.get("turns_unresolved", 0) + 1
        world.event("finding", f"round {turn['round']} in {bid[:6]}: no proof that an action of mine landed "
                               f"(no answer came back and the log does not show one)", about="turn", battle=bid)
    elif took is not None and took > C.LATE_TURN:
        world.event("finding", f"round {turn['round']}: fired {took:.1f} s into a {C.TURN_LIMIT:.0f} s turn",
                    about="turn", battle=bid)
    if (turn.get("unseen") or 0) > C.FIRE_BY:
        world.event("finding", f"round {turn['round']}: the fight went unread for {turn['unseen']:.0f} s before my "
                               f"turn was seen", about="turn", battle=bid)
