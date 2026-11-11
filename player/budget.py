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

Every call the brain issues is written down with the time it will run, so a brain that restarts still knows what
the last minute cost.

The turn clock: a turn of mine starts (T) when a read first shows it. The planner is cut off at T+15 s and the best
line so far is fired; a missing exact read is not waited for past T+12 s; the actions are out by T+20 s. Every
turn's timing is logged (turns.jsonl) with how long the fight went unread before the turn was seen, and with how
the turn ended: acted, missed, or unresolved. A turn that lands within 20 s of the game's limit is a finding.
"""
from . import calls as K
from . import config as C

TURN_ACTIONS = 5            # the most actions one turn of mine sends: no read ever takes their room
TURN_RESERVE = TURN_ACTIONS + 3     # kept free for my turn while the fight is only watched: its actions and a poll
WINDOW = 60.0
BLIND_MAX = 2 * C.POLL_GAP_MAX      # s: the longest the reserve may keep the fight unread


def _until(times, t, ceiling):
    """Seconds from t until fewer than `ceiling` of these calls are inside the minute."""
    live = [x for x in times if x > t - WINDOW]
    if len(live) < ceiling or not live:
        return 0.0
    return live[len(live) - max(1, ceiling)] + WINDOW + 0.5 - t


def is_poll(step):
    return bool((step.get("meta") or {}).get("poll"))


class Budget:
    def __init__(self, world):
        self.world = world

    def _hist(self, now):
        hist = [c for c in self.world["budget"]["calls"] if c[0] > now - WINDOW]
        self.world["budget"]["calls"] = hist
        return hist

    def used(self, now=None, lane=None):
        """Calls in the last minute (issued or still to run), in one lane or in all."""
        now = self.world.now if now is None else now
        return sum(1 for t, ln in self._hist(now) if lane is None or ln == lane)

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
        BLIND_MAX counts from now, the moment the brain last heard from the fight."""
        times, since = sorted(x[0] for x in hist), max(0.0, t - self.world.now)
        if lane == "recovery" or step.get("call") == "combat.performAction":
            limit = _until(times, t, C.CALL_LIMIT - n + 1)
            return limit, limit
        floor = _until(times, t, C.CALL_LIMIT - TURN_ACTIONS - n + 1)
        reserve = _until(times, t, C.CALL_LIMIT - TURN_RESERVE - n + 1)
        if lane == "world":
            world = sorted(x[0] for x in hist if x[1] == "world")
            return max(reserve, _until(world, t, C.WORLD_CAP - n + 1)), 0.0
        if is_poll(step):
            floor = max(floor, min(reserve, max(0.0, BLIND_MAX - since)))
        return floor, floor if since + floor > BLIND_MAX else 0.0

    def pace(self, steps, lane, start=None):
        """Schedule a batch that the relay gets at `start` (now, or later when the brain holds it first). Returns
        (steps, waited): a call that does not fit in the minute gets a pause in front of it (see the module's
        notes for who gives way first), and a watching read that would have to wait long behind other calls is
        left out. Every call that stays is recorded with the time it will run."""
        now = self.world.now
        hist = self._hist(now)
        out, t, waited, called = [], now if start is None else start, 0.0, False
        for s in steps:
            if "wait" in s:
                t += s["wait"]
                out.append(s)
                continue
            gap, forced = self._gap(hist, t, lane, s)
            if called and is_poll(s) and gap > C.POLL_GAP:
                continue                                          # left for the next batch: see the module's notes
            called = True
            if forced > 0:
                self._full(s["call"], forced)
            if gap > 0:
                out.append(K.wait(gap))
                t += gap
                waited += gap
            hist.append([round(t + C.CALL_COST, 2), lane])
            t += C.CALL_COST
            out.append(s)
        self.world["budget"]["calls"] = hist[-120:]
        return out, round(waited, 1)

    def poll_hold(self, n_calls, hold):
        """How long the brain waits before a poll of his turn: at least `hold`, and until the poll's calls fit with
        the reserve for my own turn left free (for at most BLIND_MAX; after that only the account's limit holds
        it). The wait is spent in the brain, not by the relay."""
        now = self.world.now
        gap, forced = self._gap(self._hist(now), now, "battle", {"meta": {"poll": True}}, n_calls)
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
    """Seconds the planner may still take: it is cut off at T + BEST_LINE_AT."""
    return turn["T"] + C.BEST_LINE_AT - now


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
