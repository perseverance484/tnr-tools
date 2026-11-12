"""A fight in progress: the hard real-time lane (design 4.6). Ported from the pilot's battle_tick, rule for rule.

What is kept from the live pilot (Duet's fixes of 2026-11-11):
- every poll is a full read (the live effect list rides on it), so my turn never waits on a second read;
- a read that comes back without the battle is retried plainer before the fight is called over;
- when a read is refused on my turn, the plan is made from the last good read and the actions go first;
- his kit is read on the first polls until it saves (three tries);
- a refused action is banned for the rest of the fight, and a plan that did not move the battle is not resent;
- the fight's result is the log's own HP count, not the status alone;
- the Full Potion goes in the same batch as the fight's end (the brain puts recovery in front of this activity's
  closing batch).

New here: the turn clock (player/budget.py). The planner is cut off at T+15 s, and his turn is polled less often
the longer it lasts, with the wait spent in the brain. Each turn keeps what happened to its actions (sent,
answered, accepted), so a plan the game refused or never got is replaced while the turn is still open, and a
turn is closed as acted, missed or unresolved from evidence only.

The fight's state is world["battle"]: the same dict the combat tools read as fights/live/<battle>.json.
"""
import json
import time

from .. import budget as B
from .. import calls as K
from .. import config as C
from ..combat import ground_effects, live_effects, perm_effects
from ..registry import REGISTRY, Activity, plan
from ..world import RATE_LIMITED

EMERGENCY = (("defensiveStance", "Defensive Stance"), ("wait", "End Turn"))
"""With no line from the planner: the basic actions tried in its place, in order."""


def watching(steps):
    """Mark the reads that only watch the fight: the budget keeps room for my turn in front of them."""
    for s in steps:
        s.setdefault("meta", {})["poll"] = True
    return steps


@REGISTRY.activity
class Battle(Activity):
    name = "battle"
    priority = "battle"
    reads = ("profile.getUser", "combat.getBattle", "combat.getBattleEntries", "combat.performAction")


    def available(self, world):
        return world.in_battle()

    def value(self, world):
        return 1000.0

    # ------------------------------------------------------------ results
    def on_result(self, world, results):
        for r in results:
            try:
                if r.endpoint == "profile.getUser" and not r.error:
                    self._profile(world)
                state = world["battle"]
                if state and r.endpoint in self.reads[1:] and r.input.get("battleId") == state["bid"]:
                    self._take(world, state, r)
            except Exception as err:  # noqa: BLE001  (one answer that cannot be taken in never costs the next)
                world.event("error", f"battle could not take {r.endpoint} in: {err!r}"[:300], about="crash")

    def _profile(self, world):
        """A profile read opens a fight (status BATTLE) and settles the result of the one that just closed."""
        status, bid = world.status(), world.me.get("battleId")
        pend = world["records"].get("pending_result")
        if pend and status != "BATTLE":
            # a loss does not always hospitalize, so the log's own HP count settles it too
            self._result(world, pend, "lost" if status == "HOSPITALIZED" or pend.get("log_lost") else "won")
            world["records"]["pending_result"] = None
        state = world["battle"]
        if state:
            state.pop("prove", None)                              # the profile that was asked for has come
            if status != "BATTLE" or (bid and bid != state["bid"]):
                state["left"] = True                              # it is out of this battle: the fight is over
        if status == "BATTLE" and bid and not world["battle"]:
            self._open(world, bid)

    @staticmethod
    def _open(world, bid):
        world["battle"] = {"bid": bid, "entries": [], "opened": world.now}
        world.event("fight_start", f"fight started ({bid[:6]})", battle=bid,
                    director_mode=world["control"]["director_mode"])

    def _left(self, world, state):
        """My profile is out of this battle. Out of combat: the fight is closed, and its closing batch carries the
        Full Potion. Straight into another fight (a rematch, a third party; AP1 re-review of c225ed36, finding
        4): the old fight is closed and kept, its result is the log's own count, no potion is sent into the new
        fight, and the new fight opens in this same tick."""
        bid = world.me.get("battleId")
        if world.status() != "BATTLE" or not bid:
            return self._close(world, state, None)
        self._close(world, state, "lost" if self.combat.log_says_lost(state) else "won")
        world["records"].pop("fight_end", None)                   # nothing of recovery goes into a fight
        self._open(world, bid)
        return self.plan(world)

    @staticmethod
    def _result(world, fight, result):
        if result == "lost":
            for u in fight.get("foes", []):
                world["opponents"]["lost_to"][u] = world.now + C.LOST_TO_HOURS * 3600
        world["records"]["results"] = (world["records"]["results"] + [[fight["bid"], result, round(world.now)]])[-200:]
        world.event("fight_end", f"{result.upper()} vs {fight.get('enemy') or '?'} in round {fight.get('round')}",
                    battle=fight["bid"], result=result, opponent=fight.get("enemy"), round=fight.get("round"),
                    turning_point=fight.get("turning_point"), joined=fight.get("joined"),
                    unseen_rounds=fight.get("unseen_rounds") or [])

    def _take(self, world, state, r):
        """One answer about this fight."""
        take = {"combat.getBattle": self._read, "combat.getBattleEntries": self._log,
                "combat.performAction": self._acted}[r.endpoint]
        take(world, state, r)

    @staticmethod
    def _read(world, state, r):
        if r.error == RATE_LIMITED:
            state["refused_read"] = True
        elif not r.error and isinstance(r.data, dict):
            state["inbox"] = dict(r.data)                        # the read plan() works on
            state.pop("refused_read", None)

    @staticmethod
    def _log(world, state, r):
        """Fold a log read in. Who did what in which round always lines up. The effect texts do not when a line
        has no effect (2026-11-11, live: every such read was dropped). Then the lines are kept without their
        texts, and from there on this fight's log is read with each line's effects whole, which fills them in."""
        if r.error or not isinstance(r.data, dict) or "*.id" not in r.data:
            return
        rows = K.log_rows(r.data)
        if rows is None:
            world.event("finding", "the battle log's columns do not line up, or a line is incomplete; that read "
                                   "is dropped", about="selects", battle=state["bid"])
            return
        if rows and rows[0][4] is None and not state.get("log_whole"):
            state["log_whole"] = True
            world.event("finding", "the battle log's effect texts do not line up with its lines: the lines are "
                                   "kept, and the log is read with whole effects from now on",
                        about="selects", battle=state["bid"])
        known = {e[0]: e for e in state["entries"]}
        for row in rows[::-1]:                                    # oldest first
            if row[0] not in known:
                state["entries"].append(row)
            elif known[row[0]][4] is None:
                known[row[0]][4] = row[4]                         # a line first seen without its texts

    def _acted(self, world, state, r):
        turn = state.get("turn") or {}
        open_turn = bool(turn) and not turn.get("landed")       # an AI-turn nudge is no action of a turn of mine
        if open_turn:
            turn["answered"] = turn.get("answered", 0) + 1
        if r.error == RATE_LIMITED:
            # the connector refused it, the game never saw it: nothing to ban, and the turn is still to play
            state["refused_read"] = True
            state["sent_plan"] = None
        elif r.error or not isinstance(r.data, dict):
            # an error, or an answer that is not an object (nothing, false, 0, a list, a text): nothing in it
            # says the game took the action. It may have landed: a read or the log will say. (Review of
            # 442a6311, finding 4: the empty ones were taken for an empty object, which is a taken action.)
            if open_turn:
                turn["unknown"] = turn.get("unknown", 0) + 1
            if not r.error and not state.get("odd_answer"):
                state["odd_answer"] = True
                world.event("finding", f"an answer to an action was not an object ({json.dumps(r.data)[:60]}): "
                                       f"it is not known to have landed", about="selects", battle=state["bid"])
        elif str(r.data.get("notification") or "").strip():
            self._refusal(world, state, r)
        else:
            state["acts_ok"] = True                              # this action landed: the last read is now stale
            if open_turn:
                turn["accepted"] = turn.get("accepted", 0) + 1

    @staticmethod
    def _refusal(world, state, r):
        """The game said no to an action. "Not valid anymore" bans it for the rest of the fight, so the next plan
        routes around it; any other reason bans it for this turn only. The lobby's "battle has not started"
        refuses nothing for cause: the plan is simply sent again. Each new reason is written down once."""
        note, aid = str(r.data.get("notification", "")), r.input.get("actionId")
        if "has not started" in note.lower():
            state["sent_plan"] = None
            state["banned"] = []
            return
        if "not valid anymore" in note.lower():
            where = state.setdefault("banned", [])
            world["inventory"]["restock_due"] = True              # an empty item is the usual cause
        else:
            where = (state.get("turn") or {}).setdefault("refused", [])
        if aid and aid not in where:
            where.append(aid)
        if note not in state.setdefault("refusals", []):
            state["refusals"] = (state["refusals"] + [note])[-12:]
            world.event("finding", f"the game refused {aid}: {note[:200]}", about="refusal", battle=state["bid"])

    # ------------------------------------------------------------ the tick
    def plan(self, world):
        state = world["battle"]
        bid = state["bid"]
        read = state.pop("inbox", None)
        refused = state.pop("refused_read", False)
        acts_ok = state.pop("acts_ok", False)
        if state.pop("left", False):
            return self._left(world, state)
        if read is not None:
            return self._tick(world, state, read)
        if "battle" not in state and not state.get("empty_reads"):
            # the fight just started (or its opening read never came back): one full read and the whole log
            state["asked_start"] = True
            return plan([K.battle(bid, effects=True), self._log_read(state, C.ENTRIES_START)], "battle",
                        f"BATTLE START {bid}", hold=C.RATE_BACKOFF if refused else 0.0, tag="urgent")
        return self._no_read(world, state, refused, acts_ok)

    @staticmethod
    def _log_read(state, n):
        return K.entries(state["bid"], n, bool(state.get("log_whole")))

    @staticmethod
    def _proof(state):
        """My profile, asked beside every read after one came back without the battle, until it comes: it says
        whether the fight is still on. It is not a watching read: the budget does not leave it out."""
        return [K.user()] if state.get("prove") else []

    def _without_the_battle(self, world, state, battle):
        """A read came back without the battle. That alone never ends a fight (2026-11-11, live: four such reads
        each closed a fight that was still on, and a Full Potion was sent into it). A fight ends when a read
        shows a fighter down, or when my profile has left the battle. So my profile is asked beside the next
        read, which is a plain one; on my turn the plan goes from the last good read meanwhile, as after a
        refused read."""
        n = state["empty_reads"] = state.get("empty_reads", 0) + 1
        if n == 1 or n % 10 == 0:
            world.event("finding", f"a battle read came back without the battle ({n} in a row). It held: "
                                   f"{json.dumps(battle, default=str)[:160]}", about="read", battle=state["bid"])
        state["prove"] = True
        return self._no_read(world, state, True, False, hold=0.0 if n == 1 else C.RATE_BACKOFF)

    def _no_read(self, world, state, refused, acts_ok, hold=None):
        """A tick with no read of the fight in hand: act from the last good read when the turn is owed an action,
        else read again."""
        bid, b = state["bid"], state.get("battle") or {}
        mine = b.get("battle.activeUserId") == C.ME and C.ME in (b.get("battle.usersState.*.userId") or [])
        if mine and not acts_ok and B.turn_owed(state.get("turn"), refused, world.now):
            # my turn, the game has taken nothing of it, and no read: a refusal is not waited for at all, a plan
            # that came back refused is replaced at once, and a read that simply has not come back is not waited
            # for past T+12 s. Plan from the last good read and act now.
            return self._tick(world, state, dict(b), from_last_read=True)
        # an action of mine landed, or it is not my turn: read again (at once while my turn still waits on it)
        turn = state.get("turn") or {}
        if mine and turn:
            turn["looked"] = True
        state["asked_full"] = state["asked_ground"] = False       # this read asks for neither effects nor ground
        again = [K.battle(bid), self._log_read(state, C.ENTRIES_POLL)]
        if hold is None:
            hold = C.RATE_BACKOFF if refused and not mine else 0.0
        return plan((again if mine and not turn.get("accepted") else watching(again)) + self._proof(state), "battle",
                    f"resume battle {bid}", hold=hold, tag="urgent")

    def last_resort(self, world):
        """The tick has failed twice running (the brain calls this in its place). It uses only what _usable has
        checked: the fighters, the round, the version and whose turn it is, from the read that came with the
        failure when that read is a good one, else from the last good read. On my turn, while the game has taken
        nothing of it, the best line the turn already has or a basic action goes out; a plain read of the fight
        follows either way, with my profile beside it once a fighter is down. Once my profile is out of the
        fight, only my profile is read."""
        state = world["battle"]
        bid, steps, note = state["bid"], [], "the tick failed: reading again"
        if state.get("left") or world.status() != "BATTLE" or world.me.get("battleId") != bid:
            # my profile is out of this fight (review of 442a6311, finding 6: a fight that could not be closed
            # was still acted on from its last read). Nothing more is sent into it, whatever keeps it open.
            return plan([K.user()], "battle", "the tick failed, and my profile is out of this fight", tag="urgent")
        b, mine = self._known(world, state)
        turn = state.get("turn") or {}
        if b and (not mine or turn.get("round") != b["battle.round"]):
            self._turn_over(world, state)                         # a turn of mine that this read shows is over
            turn = {}
        if mine and not turn.get("accepted"):
            turn = B.turn_open(state, b["battle.round"], world.now, state.get("unseen"))
            steps, how = self._stand_in(world, state, b, turn)
            note = f"MY TURN, {how} (last good read)"
        state["asked_full"] = state["asked_ground"] = False
        again = [K.battle(bid), self._log_read(state, C.ENTRIES_POLL)]
        return plan(steps + (again if mine and not turn.get("accepted") else watching(again)) + self._proof(state),
                    "battle", note, tag="urgent")

    def _known(self, world, state):
        """For the last resort: (the checked part of the newest good read, is it my turn in a fight still on)."""
        read = state.pop("inbox", None)
        if isinstance(read, dict) and self._usable(read) and C.ME in read["battle.usersState.*.userId"]:
            state["battle"] = {k: read[k] for k in ["battle.round", "battle.version", "battle.activeUserId"]
                               + [f"battle.usersState.*.{c}" for c in K.STATE_COLS[:6]]}
            state["read_at"] = world.now
        b = state.get("battle") or {}
        hp = b.get("battle.usersState.*.curHealth") or [0]
        if b and min(hp) <= 0:
            state["prove"] = True                                 # it looks over: my profile will say
        return b, b.get("battle.activeUserId") == C.ME and min(hp) > 0

    def _stand_in(self, world, state, b, turn):
        """For the last resort: (the steps of the best line this turn has, or of a basic action; what it is)."""
        bid, v, i = state["bid"], b["battle.version"], b["battle.usersState.*.userId"].index(C.ME)
        me_xy = (b["battle.usersState.*.longitude"][i], b["battle.usersState.*.latitude"][i])
        line, how = self._fallback(turn, v, me_xy, state.get("banned", []) + turn.get("refused", []),
                                   "the tick failed")
        world.event("finding", f"round {b['battle.round']}: {how}", about="crash", battle=bid)
        if not line:
            return [], how
        state["sent_plan"] = {"v": v, "first": line[0]["actionId"], "stand_in": True}
        state["pick"] = {"round": b["battle.round"], "actions": [a["name"] for a in line], "why": how}
        B.turn_fired(world, bid, turn, how, len(line), True)
        return [K.act(bid, a["actionId"], a["longitude"], a["latitude"], v + k) for k, a in enumerate(line)], how

    def _tick(self, world, state, battle, from_last_read=False):
        """One read of the fight, in order: is the read usable, is the fight over, whose turn is it."""
        bid = state["bid"]
        users = battle.get("battle.usersState.*.userId")
        users = users if isinstance(users, list) else []          # anything else is a read without the fighters
        asked_ground = state.get("asked_ground", False)
        self._plainer(state, users)
        if C.ME not in users:
            return self._without_the_battle(world, state, battle)
        if not self._usable(battle):
            # a fighter's column came back short, or the read lacks the round, the version or whose turn it is:
            # nothing can be told apart. It is not planned on, and it is not a read either: the turn's clock and
            # the last good read decide what happens next, as when no read came back at all (AP1 re-review,
            # finding 2: such reads used to ask for another read for ever, past every deadline of the turn).
            n = state["bad_reads"] = state.get("bad_reads", 0) + 1
            if n == 1 or n % 10 == 0:
                world.event("finding", f"a battle read cannot be used ({n} so far): a column is short, a value "
                                       f"is missing or of the wrong kind, or the fighter to move is not in it",
                            about="selects", battle=bid)
            return self._no_read(world, state, False, False)
        if not from_last_read:                                    # how long the fight went unread before this
            state["unseen"] = round(world.now - state.get("read_at", state.get("opened", world.now)), 1)
            state["read_at"] = world.now
            state.pop("empty_reads", None)
            self._joined(world, state, battle)
        self._seat(state, battle)
        self._absorb(state, battle, users, asked_ground, from_last_read)
        hp = battle["battle.usersState.*.curHealth"]
        me_i = users.index(C.ME)
        foes = [i for i in range(len(users)) if i != me_i and hp[i] > 0]
        if hp[me_i] <= 0 or not foes:
            return self._close(world, state, "won" if hp[me_i] > 0 else "lost")
        names = battle["battle.usersState.*.username"]
        state.update(enemy=names[foes[0]], round=battle["battle.round"], my_hp=hp[me_i], his_hp=hp[foes[0]])
        head = (f"BATTLE R{battle['battle.round']} v{battle['battle.version']} | me {hp[me_i]:.0f} | "
                f"{names[foes[0]]} {hp[foes[0]]:.0f}")
        ai = battle.get("battle.usersState.*.isAi") or []
        if len(ai) != len(users):
            ai = []                                               # not one flag per fighter: treat them as players
        poll = self._poll(state, users[foes[0]], bool(ai and ai[foes[0]]))
        me_xy = (battle["battle.usersState.*.longitude"][me_i], battle["battle.usersState.*.latitude"][me_i])
        active = battle["battle.activeUserId"]
        if active != C.ME:
            return self._not_my_turn(world, state, battle, poll, head, me_xy,
                                     bool(active in users and ai and ai[users.index(active)]))
        return self._mine(world, state, battle, poll, head, me_xy, hp[foes[0]], from_last_read)

    def _not_my_turn(self, world, state, battle, poll, head, me_xy, ai_turn):
        bid, v = state["bid"], battle["battle.version"]
        self._turn_over(world, state)
        if ai_turn:
            # an AI's turn only advances when some client calls performAction during it
            return plan([K.act(bid, "wait", me_xy[0], me_xy[1], v)] + poll, "battle", head + " | AI turn: nudge")
        # his turn: poll less often the longer it lasts; the wait is spent in the brain, not by the relay
        k = state["his_polls"] = state.get("his_polls", 0) + 1 if state.get("his_v") == v else 0
        state["his_v"] = v
        return plan(poll, "battle", head + " | his turn",
                    hold=self.budget.poll_hold(1, min(C.POLL_GAP + k, C.POLL_GAP_MAX)))

    def _mine(self, world, state, battle, poll, head, me_xy, his_hp, from_last_read):
        R, v = battle["battle.round"], battle["battle.version"]
        state.pop("his_v", None)
        if (state.get("turn") or {}).get("round") != R:
            self._turn_over(world, state)                         # a turn of an earlier round no read closed
        turn = B.turn_open(state, R, world.now, state.get("unseen"))
        turn.setdefault("v", v)
        if world["control"]["director_mode"]:
            wait_for_him = self._director(world, state, turn, poll, head, v, from_last_read)
            if wait_for_him:
                return wait_for_him
        return self._my_turn(world, state, battle, turn, poll, head, me_xy, his_hp, from_last_read)

    @staticmethod
    def _usable(battle):
        """A read the tick can work on. The round and the version are numbers. Every fighter column has one value
        per fighter and none is missing: ids and names are text, health and position are numbers. The fighters
        are distinct, and the one whose turn it is, is one of them. Anything else is not planned on and does not
        replace the last good read (review of 0d10b7c6, finding 2: an active id that was no fighter passed for
        his turn, and a null position reached an action)."""
        def number(v):
            return isinstance(v, (int, float)) and not isinstance(v, bool)
        rows = K.columns(battle, "battle.usersState.*.", K.STATE_COLS[:6])
        if not rows or not number(battle.get("battle.round")) or not number(battle.get("battle.version")):
            return False
        ids = [r["userId"] for r in rows]
        return (len(set(map(str, ids))) == len(ids) and battle.get("battle.activeUserId") in ids
                and all(isinstance(r["userId"], str) and isinstance(r["username"], str)
                        and all(number(r[k]) for k in ("curHealth", "maxHealth", "longitude", "latitude"))
                        for r in rows))

    @staticmethod
    def _seat(state, battle):
        """Who moves first in a round, told once, from the first read of the fight: on my turn I am second when he
        has already acted this round; on his turn I am first when I have."""
        if "seat" in state or battle.get("battle.round") is None:
            return
        mine = battle.get("battle.activeUserId") == C.ME
        moved = any(e[1] == battle["battle.round"] and (e[2] != C.ME) == mine for e in state["entries"])
        state["seat"] = (2 if moved else 1) if mine else (1 if moved else 2)

    @staticmethod
    def _ground(battle, asked):
        """The ground of a read: (as the game sent it, what that is, the rows the planner gets or None). It comes
        whole or as columns; asked for and bare means there is none on the field; not asked for means not known."""
        whole = battle.pop("battle.groundEffects", None)
        if whole is not None:
            return (whole, "whole", whole) if isinstance(whole, list) else (whole, "misaligned", None)
        cols = {k: v for k, v in battle.items() if k.startswith("battle.groundEffects.")}
        rows = K.ground_cols(battle)
        if rows is None:
            return ([], "none on the field", []) if asked else (None, "not asked", None)
        return (cols, "misaligned", None) if rows is False else (cols, "columns", rows)

    @staticmethod
    def _plainer(state, users):
        """What a read says about the reads to ask for next. One that came back with the fighters proves its kind
        works. One that came back without them drops the richest part it asked for (the ground columns, then the
        effect list), so the next polls are plainer."""
        asked_full = state.pop("asked_full", False)
        asked_ground = state.pop("asked_ground", False)
        asked_start = state.pop("asked_start", False)             # the opening read: counted like a full read
        if users:
            state["full_ok"] = state.get("full_ok") or asked_full
        elif asked_ground and not state.get("ground_refused"):
            state["ground_refused"] = True
        elif (asked_full or asked_start) and not state.get("full_ok") and state.get("full_refused", 0) < 2:
            state["full_refused"] = state.get("full_refused", 0) + 1
        elif state.get("perm_tries") and "perm_effects" not in state and state.get("perm_retry", 0) < 2:
            state["perm_retry"] = state.get("perm_retry", 0) + 1
            state["perm_tries"] = 9

    @staticmethod
    def _joined(world, state, battle):
        """Once, at the first read of a fight: the rounds already over that show no action of mine. Nothing was
        playing them, or I could not act (2026-11-11, live: a rematch began while no relay ran). They are counted
        apart from missed turns and named in the fight's end event."""
        if "joined" in state or battle.get("battle.round") is None:
            return
        rnd = state["joined"] = battle["battle.round"]
        mine = {e[1] for e in state["entries"] if e[2] == C.ME and e[3] != "wait"}   # the game logs a timeout as wait
        state["unseen_rounds"] = sorted({e[1] for e in state["entries"] if e[1] < rnd} - mine)
        world["records"]["turns_unseen"] = world["records"].get("turns_unseen", 0) + len(state["unseen_rounds"])

    def _absorb(self, state, battle, users, asked_ground, from_last_read):
        """Fold a read into the fight's state: ground, the live effect list, permanent effects, the fight bases."""
        bid = state["bid"]
        sent_g, how_g, raw_g = self._ground(battle, asked_ground)
        if raw_g is not None:
            state["ground"] = ground_effects(raw_g)
        raw = battle.pop("battle.usersEffects", None)
        if not isinstance(raw, list):
            raw = None                                            # no effect list, or not one: as if not sent
        if raw is not None:
            self._archive(state, battle, raw, sent_g, how_g)
            state["live"], state["live_v"] = live_effects(raw), battle.get("battle.version")
            state.setdefault("live_hist", {})[str(battle.get("battle.round"))] = state["live"]   # exact state, kept
            for foe in [u for u in users if u != C.ME]:
                if self.combat.learn_weapons(foe, state["live"]):
                    state["bases_ids"] = None                     # his kit changed: the fight bases run again
            state.setdefault("perm_effects", perm_effects(raw))
        # both kits' bases for this matchup from the engine: at the start, and whenever he shows a new action
        his_ids = sorted({e[3] for e in state["entries"] if e[2] != C.ME})
        if "perm_effects" in state and (state.get("bases_ids") is None or set(his_ids) - set(state["bases_ids"])):
            state["bases_ids"] = his_ids
            self.combat.write_cache(bid, state, battle)
            self.combat.start_fight_bases(bid)
        if "perm_effects" in state:
            battle["battle.permEffects"] = state["perm_effects"]
        if raw_g is not None:
            battle["battle.groundEffects"] = state["ground"]      # this read's ground only: a stale one would mislead
        if not from_last_read:
            state["battle"] = battle
            state["n_at_battle"] = len(state["entries"])          # log lines already counted in this HP read
        self.combat.write_cache(bid, state)

    def _archive(self, state, battle, raw, ground, ground_read):
        """Keep the full live state of the round, once for the start of my turn and once for the start of his: the
        whole effect list, the fighters' columns and the ground, each as the game sent it (ground_read says what
        the ground field is: whole, columns, none on the field, not asked, misaligned). These are the states each
        side decided on, so the opponent models and the move atlas never need a second capture."""
        side = "me" if battle.get("battle.activeUserId") == C.ME else "him"
        key = f"{battle.get('battle.round')}:{side}"
        if key in state.setdefault("archived", []):
            return
        state["archived"].append(key)
        self.combat.archive_state(state["bid"], {
            "round": battle.get("battle.round"), "version": battle.get("battle.version"), "turn": side,
            "active": battle.get("battle.activeUserId"), "seat": state.get("seat"),
            "fighters": {k: v for k, v in battle.items() if k.startswith("battle.usersState.")},
            "effects": raw, "ground": ground, "ground_read": ground_read, "log_lines": len(state["entries"])})

    def _poll(self, state, foe_id, foe_is_ai):
        """The next read of the fight. Every poll is a full read (same call count), so my turn never waits on a
        second one; plain only after full reads were refused twice. His kit read rides it until it saves."""
        bid = state["bid"]
        want = "perm_effects" not in state and state.get("perm_tries", 0) < 2   # a refused read never blocks the fight
        if want:
            state["perm_tries"] = state.get("perm_tries", 0) + 1
        full = want or state.get("full_refused", 0) < 2
        state["asked_full"] = full
        state["asked_ground"] = bool(full and state.get("full_ok") and not state.get("ground_refused"))
        poll = [K.battle(bid, effects=full, ground=state["asked_ground"]), self._log_read(state, C.ENTRIES_POLL)]
        if (not foe_is_ai and not self.combat.kit_known(foe_id) and state.get("kit_tries", 0) < C.KIT_TRIES
                and self.budget.free() > len(poll)):              # his kit can wait for a minute with room in it
            state["kit_tries"] = state.get("kit_tries", 0) + 1
            poll.append(K.kit(foe_id))
        return watching(poll) + self._proof(state)

    @staticmethod
    def _director(world, state, turn, poll, head, v, from_last_read):
        """Director mode: each of my turns is his for HANDOFF_WAIT s, counted once from the start of the turn; the
        player covers only a turn he leaves untouched. Returns the waiting batch, or None when the player plays."""
        bid = state["bid"]
        if not from_last_read and state.get("live_v") != v and state.get("live_try_v") != v:
            state["live_try_v"] = v                               # he has the time: one exact read first
            return plan([K.battle(bid, effects=True), K.entries(bid, C.ENTRIES_POLL, bool(state.get("log_whole")))],
                        "battle", head + " | MY TURN: reading the live state", tag="urgent")
        left = C.HANDOFF_WAIT - (world.now - turn["T"])
        if left > 0:
            return plan(poll, "battle", head + f" | MY TURN: director's move (covered in {left:.0f}s)",
                        hold=min(5.0, max(1.0, left)))
        if turn["round"] not in state.setdefault("pilot_rounds", []):
            state["pilot_rounds"].append(turn["round"])
        return None

    def _my_turn(self, world, state, battle, turn, poll, head, me_xy, his_hp, from_last_read):
        bid, v, R = state["bid"], battle["battle.version"], battle["battle.round"]
        if state.get("live_v") == v:
            battle["battle.liveEffects"] = state["live"]          # plan on the exact live state
        # a plan already sent for this exact battle version that did not move it is not resent as is. (Only a
        # fresh read can show that: from the last good read the same plan goes again, and the game's own version
        # check keeps it from landing twice.)
        sent, said_no = state.get("sent_plan") or {}, turn.setdefault("refused", [])
        if (not from_last_read and sent.get("v") == v and sent.get("first") and sent["first"] not in said_no
                and sent["first"] not in state.setdefault("banned", [])):
            # the game gave no reason. A planner's line: for the fight, as in the pilot; a stand-in: for this turn
            (said_no if sent.get("stand_in") else state["banned"]).append(sent["first"])
        if world["control"]["director_mode"] or turn.get("accepted"):
            # what is left of the turn: after the director's window, or after the actions it has already taken
            # (2026-11-11, live: a turn's later plans got no planner time once T+15 s had passed)
            seconds = max(3.0, min(C.BEST_LINE_AT, C.TURN_LIMIT - (world.now - turn["T"]) - 8.0))
        else:
            seconds = B.planner_seconds(turn, world.now)
        no = state.get("banned", []) + turn.get("refused", [])
        line, how = self._line(world, state, battle, his_hp, no + list(world["inventory"].get("empty_items", [])),
                               seconds)
        tail = " (last good read)" if from_last_read else ""
        if line:
            turn["line"] = {"v": v, "actions": line}              # the best line this turn has so far
            state["sent_plan"] = {"v": v, "first": line[0]["actionId"]}
            note = f"MY TURN: {' + '.join(a['name'] for a in line)} ({how}){tail}"
        else:
            line, how = self._fallback(turn, v, me_xy, state.get("banned", []) + turn.get("refused", []), how)
            world.event("finding", f"round {R}: {how}", about="planner", battle=bid)
            if not line:
                state["pick"] = {"round": R, "actions": [], "why": how}
                return plan(poll, "battle", head + f" | MY TURN, nothing to send: {how}", tag="urgent")
            state["sent_plan"] = {"v": v, "first": line[0]["actionId"], "stand_in": True}
            note = f"MY TURN, {how}{tail}"
        state["pick"] = {"round": R, "actions": [a["name"] for a in line], "why": how + tail}
        steps = []
        for k, a in enumerate(line):                              # a short gap between actions: not all at once
            if k:
                steps.append(K.wait(C.ACTION_GAP))
            steps.append(K.act(bid, a["actionId"], a["longitude"], a["latitude"], v + k))
        B.turn_fired(world, bid, turn, how, len(line), from_last_read)
        return plan(steps + poll, "battle", head + " | " + note, tag="urgent")

    def _line(self, world, state, battle, his_hp, ban, seconds):
        """The planner's line for this turn, or (None, why). A planner that crashes has no line. A line with an
        action the gates would refuse is planned again without that action: the gates stop the call either way,
        and a turn is not lost to it."""
        bid, t0 = state["bid"], time.time()
        for _ in range(3):
            left = None if seconds is None else seconds - (time.time() - t0)
            try:
                line, how = self.combat.plan_turn(bid, battle, state["entries"], state["enemy"], exact=his_hp <= 2000,
                                                  ban=ban, seconds=left)
            except Exception as err:  # noqa: BLE001
                return None, f"planner crashed: {err}"
            if line and not all(self._sendable(a) for a in line):
                return None, "planner failed: its line cannot be sent"
            bad = next((a["actionId"] for a in line or []
                        if not self.gates.check(K.act(bid, a["actionId"], 0, 0, 0), world, self.name).ok), None)
            if bad is None:
                return line, how
            world.event("finding", f"the planner chose {bad}, which the gates refuse: planning without it",
                        about="gate", battle=bid)
            state.setdefault("banned", []).append(bad)
            ban = ban + [bad]
        return None, "planner failed: every line held an action the gates refuse"

    @staticmethod
    def _sendable(action):
        """One action of a planner's line: a name, an action id, and a tile given in numbers."""
        return (isinstance(action, dict) and all(isinstance(action.get(k), str) for k in ("actionId", "name"))
                and all(isinstance(action.get(k), (int, float)) and not isinstance(action.get(k), bool)
                        for k in ("longitude", "latitude")))

    @staticmethod
    def _fallback(turn, v, me_xy, banned, why):
        """With no line from the planner: the best line this turn already had, when the battle has not moved and
        the game has refused none of it; else the first basic action the game has not refused. (None, why) when
        it has refused them all: nothing is left that it would take."""
        best = turn.get("line") or {}
        if best.get("v") == v and not {a["actionId"] for a in best["actions"]} & set(banned):
            return best["actions"], f"best line so far ({why})"
        for aid, name in EMERGENCY:
            if aid not in banned:
                return [{"actionId": aid, "longitude": me_xy[0], "latitude": me_xy[1], "name": name}], \
                    f"no plan ({why}): {aid}"
        return None, f"no plan ({why}) and the game has refused every fallback"

    @staticmethod
    def _turn_over(world, state, ended=False):
        """My turn is over (a read shows the next state, or the fight ended): close its clock with what the
        evidence says. An action counts when the game answered it, or when the battle log shows it."""
        turn = state.get("turn")
        if turn and not turn.get("landed"):
            # (a wait of mine in the log proves nothing: the game writes one for a turn that timed out)
            logged = any(e[1] == turn["round"] and e[2] == C.ME and e[3] != "wait" for e in state["entries"])
            B.turn_closed(world, state["bid"], turn, B.turn_outcome(turn, logged, ended))

    def _close(self, world, state, result):
        """The fight is over: keep it for the tools that learn from it, and hand the brain the closing batch (the
        brain puts the Full Potion in front of it). result None: not known yet; the next profile read and the
        log's own HP count decide. The fight's books (its last turn, its result, its archive) never keep it
        open: when they fail, that is written down, the fight's state is kept as it is, and the fight closes."""
        bid = state["bid"]
        last = state.get("battle") or {}
        users = last.get("battle.usersState.*.userId") or []
        try:
            self._books(world, state, result, users)
            kept = f"log saved fights/{bid}_entries.json"
        except Exception as err:  # noqa: BLE001
            kept = self._unarchived(world, state, err)
        me = users.index(C.ME) if C.ME in users else None
        world["records"]["fight_end"] = {
            "bid": bid, "result": result, "at": world.now,
            "hp": last["battle.usersState.*.curHealth"][me] if me is not None else 0,
            "max": (last.get("battle.usersState.*.maxHealth") or [C.MAX_HP] * len(users))[me] if me is not None
            else C.MAX_HP}
        world["inventory"]["restock_due"] = True                  # after every fight: durability and stock (AP2)
        world["battle"] = None
        return plan([K.user()], "battle", f"BATTLE OVER ({result or 'closed, result on the next read'}): {kept}",
                    tag="fight_end")

    def _books(self, world, state, result, users):
        """The end of a fight on record: its last turn closed, its result (or what the next profile needs to
        tell it), and the fight kept for the tools that learn from it."""
        bid = state["bid"]
        self._turn_over(world, state, ended=True)
        fight = {"bid": bid, "foes": [u for u in users if u != C.ME], "enemy": state.get("enemy"),
                 "round": state.get("round"), "turning_point": self.combat.turning_point(state),
                 "joined": state.get("joined"), "unseen_rounds": state.get("unseen_rounds") or []}
        if result is None:
            world["records"]["pending_result"] = dict(fight, log_lost=self.combat.log_says_lost(state))
        else:
            self._result(world, fight, result)
        self.combat.close_fight(bid, state, sorted(set(state.get("pilot_rounds", []))),
                                world["control"]["director_mode"])

    @staticmethod
    def _unarchived(world, state, err):
        """The fight's books failed. Its state goes to live/unarchived-<battle>.json as it is, for Duet."""
        name = f"unarchived-{state['bid']}.json"
        try:
            world._append(name, state)
        except Exception:  # noqa: BLE001
            name = "nowhere: that failed too"
        world.event("error", f"the fight {state['bid'][:6]} could not be put on record ({err!r}); its state is "
                             f"kept in live/{name}"[:300], about="crash", battle=state["bid"])
        return f"NOT archived, state kept in live/{name}"
