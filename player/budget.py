"""The call budget and the battle turn clock (design 4.6).

The connector allows 30 calls a minute for the whole account. The budget keeps three lanes under it:
  battle    a fight in progress. Never delayed: my turn's reads and actions and the fight's last batch go at once.
            The only thing scheduled here is how often his turn is polled, and that leaves room for my turn.
  recovery  the Full Potion at the end of a fight, the hospital. Never delayed.
  world     everything else. Paced: at most WORLD_CAP calls in any rolling minute, and none while a fight is on.

Every call the brain issues is written down with the time it will run, so a brain that restarts still knows what
the last minute cost.

The turn clock: a turn of mine starts (T) when a read first shows it. The planner is cut off at T+15 s and the best
line so far is fired; a missing exact read is not waited for past T+12 s; the actions are out by T+20 s. Every
turn's timing is logged (turns.jsonl), and a turn that lands within 20 s of the game's limit is a finding.
"""
from . import calls as K
from . import config as C

TURN_RESERVE = 8            # calls kept free for my turn while his turn is polled (up to 5 actions and a poll)
WINDOW = 60.0


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
        return max(0, min(C.WORLD_CAP - self.used(now, "world"), C.CALL_LIMIT - self.used(now)))

    def pace(self, steps, lane):
        """Schedule a batch. Returns (steps, waited): world calls get a pause in front of them when the window is
        full; battle and recovery calls are never delayed. Every call is recorded with the time it will run."""
        now = self.world.now
        hist = self._hist(now)
        out, t, waited = [], now, 0.0
        for s in steps:
            if "wait" in s:
                t += s["wait"]
                out.append(s)
                continue
            if lane == "world":
                recent = sorted(x[0] for x in hist if x[0] > t - WINDOW)
                world_recent = sorted(x[0] for x in hist if x[0] > t - WINDOW and x[1] == "world")
                gap = 0.0
                if len(world_recent) >= C.WORLD_CAP:
                    gap = max(gap, world_recent[len(world_recent) - C.WORLD_CAP] + WINDOW + 0.5 - t)
                if len(recent) >= C.CALL_LIMIT:
                    gap = max(gap, recent[len(recent) - C.CALL_LIMIT] + WINDOW + 0.5 - t)
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
        """How long to wait before a poll of his turn: at least `hold`, and long enough that the poll's calls plus
        a reserve for my own turn still fit in the minute."""
        now = self.world.now
        times = sorted(t for t, _ in self._hist(now))
        room = C.CALL_LIMIT - TURN_RESERVE - n_calls
        if len(times) > room:
            hold = max(hold, times[len(times) - room - 1] + WINDOW + 0.5 - now)
        return round(max(0.0, hold), 1)


# ---------------------------------------------------------------- the turn clock
def turn_open(state, rnd, now):
    """The clock of my turn in round rnd: started once, when a read first shows the turn."""
    turn = state.get("turn")
    if not turn or turn.get("round") != rnd:
        turn = state["turn"] = {"round": rnd, "T": now, "fired_at": None, "how": None, "actions": 0,
                                "from_last_read": False, "landed": False}
    return turn


def planner_seconds(turn, now):
    """Seconds the planner may still take: it is cut off at T + BEST_LINE_AT."""
    return turn["T"] + C.BEST_LINE_AT - now


def read_is_overdue(turn, now):
    """True once a missing exact read is no longer waited for (T + LAST_GOOD_READ_AT)."""
    return now >= turn["T"] + C.LAST_GOOD_READ_AT


def turn_fired(world, bid, turn, how, n_actions, from_last_read=False):
    now = world.now
    turn.update(fired_at=now, how=how, actions=n_actions, from_last_read=from_last_read)
    if now - turn["T"] > C.FIRE_BY:
        world.event("finding", f"round {turn['round']}: actions went out {now - turn['T']:.1f} s into the turn "
                               f"(the rule is {C.FIRE_BY:.0f} s)", about="turn", battle=bid)


def turn_closed(world, bid, turn, acted, now=None):
    """The turn is over (a read shows the next state). Log its timing once; a late or missed turn is a finding."""
    if not turn or turn.get("landed"):
        return
    now = world.now if now is None else now
    turn["landed"] = True
    took = (turn["fired_at"] - turn["T"]) if turn.get("fired_at") else None
    row = {"at": round(now, 1), "battle": bid, "round": turn["round"], "T": round(turn["T"], 1),
           "fired_after": round(took, 1) if took is not None else None, "how": turn.get("how"),
           "actions": turn.get("actions"), "from_last_read": turn.get("from_last_read"), "acted": bool(acted)}
    world._append("turns.jsonl", row)
    if not acted:
        world["records"]["turns_missed"] = world["records"].get("turns_missed", 0) + 1
        world.event("stall", f"MISSED TURN in {bid[:6]} round {turn['round']}: no action of mine is in the log",
                    about="missed_turn", battle=bid)
    elif took is not None and took > C.LATE_TURN:
        world.event("finding", f"round {turn['round']}: fired {took:.1f} s into a {C.TURN_LIMIT:.0f} s turn",
                    about="turn", battle=bid)
