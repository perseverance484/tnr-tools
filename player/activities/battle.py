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
the longer it lasts, with the wait spent in the brain.

The fight's state is world["battle"]: the same dict the combat tools read as fights/live/<battle>.json.
"""
from .. import budget as B
from .. import calls as K
from .. import config as C
from ..combat import ground_effects, live_effects, perm_effects
from ..registry import REGISTRY, Activity, plan
from ..world import RATE_LIMITED


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
            if r.endpoint == "profile.getUser" and not r.error:
                self._profile(world)
            state = world["battle"]
            if state and r.endpoint in self.reads[1:] and r.input.get("battleId") == state["bid"]:
                self._take(world, state, r)

    def _profile(self, world):
        """A profile read opens a fight (status BATTLE) and settles the result of the one that just closed."""
        status, bid = world.status(), world.me.get("battleId")
        pend = world["records"].get("pending_result")
        if pend and status != "BATTLE":
            # a loss does not always hospitalize, so the log's own HP count settles it too
            self._result(world, pend, "lost" if status == "HOSPITALIZED" or pend.get("log_lost") else "won")
            world["records"]["pending_result"] = None
        if status == "BATTLE" and bid and not world["battle"]:
            world["battle"] = {"bid": bid, "entries": [], "opened": world.now}
            world.event("fight_start", f"fight started ({bid[:6]})", battle=bid,
                        director_mode=world["control"]["director_mode"])

    @staticmethod
    def _result(world, fight, result):
        if result == "lost":
            for u in fight.get("foes", []):
                world["opponents"]["lost_to"][u] = world.now + C.LOST_TO_HOURS * 3600
        world["records"]["results"] = (world["records"]["results"] + [[fight["bid"], result, round(world.now)]])[-200:]
        world.event("fight_end", f"{result.upper()} vs {fight.get('enemy') or '?'} in round {fight.get('round')}",
                    battle=fight["bid"], result=result, opponent=fight.get("enemy"), round=fight.get("round"),
                    turning_point=fight.get("turning_point"))

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
        if r.error or not isinstance(r.data, dict) or "*.id" not in r.data:
            return
        rows = K.columns(r.data, "", K.ENT)
        if rows is None:
            world.event("finding", "the battle log's columns do not line up; that read is dropped",
                        about="selects", battle=state["bid"])
            return
        seen = {e[0] for e in state["entries"]}
        new = [[row[k] for k in K.ENT] for row in rows if row["*.id"] not in seen]
        state["entries"] += new[::-1]                             # oldest first

    def _acted(self, world, state, r):
        if r.error == RATE_LIMITED:
            # the connector refused it, the game never saw it: nothing to ban, and the turn is still to play
            state["refused_read"] = True
            state["sent_plan"] = None
            if state.get("turn"):
                state["turn"]["fired_at"] = None
        elif not r.error and str((r.data or {}).get("notification") or "").strip():
            self._refusal(world, state, r)
        elif not r.error:
            state["acts_ok"] = True                              # this action landed: the last read is now stale

    @staticmethod
    def _refusal(world, state, r):
        """An action the game refuses is banned for the rest of the fight, so the next plan routes around it. The
        lobby's "battle has not started" refuses nothing for cause: the plan is simply sent again."""
        note = str(r.data.get("notification", "")).lower()
        if "has not started" in note:
            state["sent_plan"] = None
            state["banned"] = []
        elif "not valid anymore" in note:
            aid = r.input.get("actionId")
            if aid and aid not in state.setdefault("banned", []):
                state["banned"].append(aid)
            world["inventory"]["restock_due"] = True              # an empty item is the usual cause

    # ------------------------------------------------------------ the tick
    def plan(self, world):
        state = world["battle"]
        bid = state["bid"]
        read = state.pop("inbox", None)
        refused = state.pop("refused_read", False)
        acts_ok = state.pop("acts_ok", False)
        if read is not None:
            return self._tick(world, state, read)
        if "battle" not in state:
            # the fight just started (or its opening read never came back): one full read and the whole log
            state["asked_start"] = True
            return plan([K.battle(bid, effects=True), K.entries(bid, C.ENTRIES_START)], "battle",
                        f"BATTLE START {bid}", hold=C.RATE_BACKOFF if refused else 0.0, tag="urgent")
        b = state.get("battle") or {}
        mine = b.get("battle.activeUserId") == C.ME and C.ME in (b.get("battle.usersState.*.userId") or [])
        turn = state.get("turn") or {}
        if mine and not acts_ok and not turn.get("fired_at") and (
                refused or (turn and B.read_is_overdue(turn, world.now))):
            # my turn and no read: a refusal is not waited for at all, and a read that simply has not come back is
            # not waited for past T+12 s. Plan from the last good read and act now.
            return self._tick(world, state, dict(b), from_last_read=True)
        # an action of mine landed, or it is not my turn: read again (at once when the turn may still be mine)
        return plan([K.battle(bid), K.entries(bid, C.ENTRIES_POLL)], "battle", f"resume battle {bid}",
                    hold=C.RATE_BACKOFF if refused and not mine else 0.0, tag="urgent")

    def _tick(self, world, state, battle, from_last_read=False):
        """One read of the fight, in order: is the read usable, is the fight over, whose turn is it."""
        bid = state["bid"]
        users = battle.get("battle.usersState.*.userId") or []
        asked_ground = state.get("asked_ground", False)
        early = self._read_came_back_empty(state, users)
        if early:
            return early
        if C.ME not in users:                                     # the battle is gone (finished battles are deleted)
            # the last state seen does not settle it: the next profile read and the log's HP count do
            return self._close(world, state, None)
        if K.columns(battle, "battle.usersState.*.", K.STATE_COLS[:6]) is None:
            # a fighter's column came back short: nothing can be told apart, so read again rather than guess
            world.event("finding", "the fighters' columns do not line up; reading again", about="selects", battle=bid)
            return plan([K.battle(bid, effects=True), K.entries(bid, C.ENTRIES_POLL)], "battle",
                        f"BATTLE {bid}: misaligned read, reading again", tag="urgent")
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
        self._turn_over(world, state, v)
        if ai_turn:
            # an AI's turn only advances when some client calls performAction during it
            return plan([K.act(bid, "wait", me_xy[0], me_xy[1], v)] + poll, "battle", head + " | AI turn: nudge")
        # his turn: poll less often the longer it lasts; the wait is spent in the brain, not by the relay
        k = state["his_polls"] = state.get("his_polls", 0) + 1 if state.get("his_v") == v else 0
        state["his_v"] = v
        return plan(poll, "battle", head + " | his turn",
                    hold=self.budget.poll_hold(len(poll), min(C.POLL_GAP + k, C.POLL_GAP_MAX)))

    def _mine(self, world, state, battle, poll, head, me_xy, his_hp, from_last_read):
        R, v = battle["battle.round"], battle["battle.version"]
        state.pop("his_v", None)
        turn = B.turn_open(state, R, world.now)
        if "v" not in turn:
            turn["v"] = v
            state.setdefault("seat", 2 if any(e[1] == R and e[2] != C.ME for e in state["entries"]) else 1)
        if world["control"]["director_mode"]:
            wait_for_him = self._director(world, state, turn, poll, head, v, from_last_read)
            if wait_for_him:
                return wait_for_him
        return self._my_turn(world, state, battle, turn, poll, head, me_xy, his_hp, from_last_read)

    @staticmethod
    def _read_came_back_empty(state, users):
        """A read that came back without the battle is not yet the end of the fight: the richer reads are dropped
        one at a time first (ground columns, then the effect list)."""
        bid = state["bid"]
        asked_full = state.pop("asked_full", False)
        asked_ground = state.pop("asked_ground", False)
        asked_start = state.pop("asked_start", False)             # the opening read: retried like a full read
        if users:
            if asked_full:
                state["full_ok"] = True
            return None
        if asked_ground and not state.get("ground_refused"):
            state["ground_refused"] = True
            return plan([K.battle(bid, effects=True), K.entries(bid, C.ENTRIES_POLL)], "battle",
                        f"BATTLE {bid}: ground read refused, full read")
        if (asked_full or asked_start) and not state.get("full_ok") and state.get("full_refused", 0) < 2:
            state["full_refused"] = state.get("full_refused", 0) + 1
            return plan([K.battle(bid), K.entries(bid, C.ENTRIES_POLL)], "battle",
                        f"BATTLE {bid}: full read refused, plain read")
        if state.get("perm_tries") and "perm_effects" not in state and state.get("perm_retry", 0) < 2:
            state["perm_retry"] = state.get("perm_retry", 0) + 1
            state["perm_tries"] = 9
            return plan([K.battle(bid), K.entries(bid, C.ENTRIES_POLL)], "battle",
                        f"BATTLE {bid}: effect read refused, plain read")
        return None

    def _absorb(self, state, battle, users, asked_ground, from_last_read):
        """Fold a read into the fight's state: ground, the live effect list, permanent effects, the fight bases."""
        bid = state["bid"]
        raw_g = battle.pop("battle.groundEffects", None)
        if raw_g is None:
            raw_g = K.ground_cols(battle)
            if raw_g is None and asked_ground:
                raw_g = []                                        # asked and the field is bare: no ground now
            elif raw_g is False:
                raw_g = None                                      # misaligned columns: keep no ground from this read
        if raw_g is not None:
            state["ground"] = ground_effects(raw_g)
        raw = battle.pop("battle.usersEffects", None)
        if raw is not None:
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
        poll = [K.battle(bid, effects=full, ground=state["asked_ground"]), K.entries(bid, C.ENTRIES_POLL)]
        if not foe_is_ai and not self.combat.kit_known(foe_id) and state.get("kit_tries", 0) < C.KIT_TRIES:
            state["kit_tries"] = state.get("kit_tries", 0) + 1
            poll.append(K.kit(foe_id))
        return poll

    @staticmethod
    def _director(world, state, turn, poll, head, v, from_last_read):
        """Director mode: each of my turns is his for HANDOFF_WAIT s, counted once from the start of the turn; the
        player covers only a turn he leaves untouched. Returns the waiting batch, or None when the player plays."""
        bid = state["bid"]
        if not from_last_read and state.get("live_v") != v and state.get("live_try_v") != v:
            state["live_try_v"] = v                               # he has the time: one exact read first
            return plan([K.battle(bid, effects=True), K.entries(bid, C.ENTRIES_POLL)], "battle",
                        head + " | MY TURN: reading the live state", tag="urgent")
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
        # a plan already sent for this exact battle version that did not move it is not resent as is
        sent = state.get("sent_plan") or {}
        if sent.get("v") == v and sent.get("first") and sent["first"] not in state.setdefault("banned", []):
            state["banned"].append(sent["first"])
        if world["control"]["director_mode"]:                     # what is left of the turn after his window
            seconds = max(3.0, min(C.BEST_LINE_AT, C.TURN_LIMIT - (world.now - turn["T"]) - 8.0))
        else:
            seconds = B.planner_seconds(turn, world.now)
        ban = state.get("banned", []) + list(world["inventory"].get("empty_items", []))
        line, how = self.combat.plan_turn(bid, battle, state["entries"], state["enemy"], exact=his_hp <= 2000,
                                          ban=ban, seconds=seconds)
        tail = " (last good read)" if from_last_read else ""
        if not line:
            world.event("finding", f"round {R}: no line ({how}); Defensive Stance", about="planner", battle=bid)
            state["pick"] = {"round": R, "actions": ["Defensive Stance"], "why": how}
            B.turn_fired(world, bid, turn, how, 1, from_last_read)
            return plan([K.act(bid, "defensiveStance", me_xy[0], me_xy[1], v)] + poll, "battle",
                        head + f" | MY TURN, no plan ({how}): defensiveStance{tail}", tag="urgent")
        state["sent_plan"] = {"v": v, "first": line[0]["actionId"]}
        state["pick"] = {"round": R, "actions": [a["name"] for a in line], "why": how + tail}
        steps = []
        for k, a in enumerate(line):                              # a short gap between actions: not all at once
            if k:
                steps.append(K.wait(C.ACTION_GAP))
            steps.append(K.act(bid, a["actionId"], a["longitude"], a["latitude"], v + k))
        B.turn_fired(world, bid, turn, how, len(line), from_last_read)
        return plan(steps + poll, "battle", head + f" | MY TURN: {' + '.join(a['name'] for a in line)} ({how}){tail}",
                    tag="urgent")

    @staticmethod
    def _turn_over(world, state, v):
        """A read shows it is no longer my turn: close the turn's clock and say whether I acted in it."""
        turn = state.get("turn")
        if turn and not turn.get("landed"):
            mine = any(e[1] == turn["round"] and e[2] == C.ME for e in state["entries"])
            B.turn_closed(world, state["bid"], turn, mine or (bool(turn.get("fired_at")) and v > turn.get("v", v)))

    def _close(self, world, state, result):
        """The fight is over: keep it for the tools that learn from it, and hand the brain the closing batch (the
        brain puts the Full Potion in front of it). result None: not known yet; the next profile read and the
        log's own HP count decide."""
        bid = state["bid"]
        last = state.get("battle") or {}
        users = last.get("battle.usersState.*.userId") or []
        self._turn_over(world, state, (last.get("battle.version") or 0) + 1)
        fight = {"bid": bid, "foes": [u for u in users if u != C.ME], "enemy": state.get("enemy"),
                 "round": state.get("round"), "turning_point": self.combat.turning_point(state)}
        if result is None:
            world["records"]["pending_result"] = dict(fight, log_lost=self.combat.log_says_lost(state))
        else:
            self._result(world, fight, result)
        self.combat.close_fight(bid, state, sorted(set(state.get("pilot_rounds", []))),
                                world["control"]["director_mode"])
        me = users.index(C.ME) if C.ME in users else None
        world["records"]["fight_end"] = {
            "bid": bid, "result": result, "at": world.now,
            "hp": last["battle.usersState.*.curHealth"][me] if me is not None else 0,
            "max": (last.get("battle.usersState.*.maxHealth") or [C.MAX_HP] * len(users))[me] if me is not None
            else C.MAX_HP}
        world["inventory"]["restock_due"] = True                  # after every fight: durability and stock (AP2)
        world["battle"] = None
        return plan([K.user()], "battle", f"BATTLE OVER ({result or 'closed, result on the next read'}): "
                                          f"log saved fights/{bid}_entries.json", tag="fight_end")
