"""Light reads on his turn (director 2026-11-12, RUL-2026-11-12-154: the proposal of the live-session handoff,
"His turn would be watched with a five-field read; the full state would be read once, when my turn starts";
and 2026-11-13, RUL-2026-11-13-155: "Keep the opponent state").

Every poll of a fight used to be a full read: the fighters, the whole live effect list, the ground and the
log's last lines, every few seconds, on his turn as on mine. In the live session of 2026-11-11 each added
about 14,000 tokens to what the relay carries (docs/reviews/AI_PLAYER_AP1_LIVE_HANDOFF.md).

Now a round has two full reads: the one behind my actions, which is the state his turn starts on and is kept
for the opponent models, and the one my turn starts with, which is the state I plan on and brings the log of
his whole turn. Between them his turn is watched with a light read: the fighters' columns, the version and
whose turn it is.

What must not change: no turn of mine is missed. A light read that shows my turn starts the turn's clock; the
full read is asked for at once; if it is refused or does not come, the turn is played from the last good read.
"""
import json
import unittest

from player import budget as B, calls as K, config as C
from player.tests.support import FOE, LINE, Rig, battle_read, fixture, limited, log_read, res, start_fight, user
from player.tests.test_review import NOT_VALID, about, acts, answers, turns

LIGHT = K.battle("B1")["select"]
"""What a light read asks for: the version, the round, whose turn it is, and the fighters' columns."""


def kinds(out):
    """A batch in words: act, wait, full, light, log N, kit, profile."""
    words = []
    for s in out["steps"]:
        if "wait" in s:
            words.append("wait")
        elif s["call"] == "combat.getBattle":
            words.append("full" if "battle.usersEffects" in s["select"] else "light")
        elif s["call"] == "combat.getBattleEntries":
            words.append(f"log {s['input']['limit']}")
        else:
            words.append({"combat.performAction": "act", "jutsu.getPublicUserJutsus": "kit",
                          "profile.getUser": "profile"}[s["call"]])
    return words


def watching(out):
    return [bool((s.get("meta") or {}).get("poll")) for s in out["steps"] if "call" in s]


class TheReadsOfARound(unittest.TestCase):
    def his_turn(self, rig=None):
        """My turn of round R is played, and the read behind my actions shows his turn. -> (rig, his read, out)."""
        rig = rig or Rig()
        rig.combat.kits.add(FOE)                                            # (his kit is on file: no kit read rides)
        battle, ents, out = start_fight(rig)
        self.assertEqual(kinds(out), ["act", "wait", "act", "full", "log 8"])   # the read behind my actions: full
        self.R, self.v = battle["battle.round"], battle["battle.version"]
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.version": self.v + 2})
        out = rig.tick(*answers(out), battle_read("B1", dict(his, **{"battle.usersEffects": []})))
        return rig, his, out

    def my_turn(self, his, **more):
        """The light read that shows my next turn: he acted twice."""
        return dict(his, **{"battle.activeUserId": C.ME, "battle.round": self.R + 1, "battle.version": self.v + 4,
                            **more})

    # ---- his turn
    def test_once_the_state_his_turn_began_on_is_on_record_it_is_watched_light(self):
        rig, his, out = self.his_turn()
        self.assertIn(f"{self.R}:him", rig.world["battle"]["archived"])
        holds = []
        for _ in range(5):
            self.assertEqual((kinds(out), watching(out)), (["light"], [True]))   # was: full, log 8, every time
            self.assertEqual(out["steps"][0]["select"], LIGHT)
            self.assertIn("his turn", out["note"])
            holds.append(out["hold"])
            out = rig.tick(battle_read("B1", his), dt=out["hold"] + 1)
        self.assertEqual(holds, [3.0, 4.0, 5.0, 6.0, 6.0])                  # the same backing off as before
        self.assertEqual(rig.combat.used["live_state"], 2)                  # my state and his, and no more of them

    def test_until_it_is_on_record_his_turn_is_read_in_full(self):
        rig = Rig()
        rig.combat.kits.add(FOE)
        battle, ents, out = start_fight(rig)
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.version": battle["battle.version"] + 2})
        for _ in range(3):                                                  # the read behind my actions came plain
            out = rig.tick(battle_read("B1", his), dt=out["hold"] + 1)
            self.assertEqual(kinds(out), ["full", "log 8"])
        out = rig.tick(battle_read("B1", dict(his, **{"battle.usersEffects": []})), dt=out["hold"] + 1)
        self.assertEqual(kinds(out), ["light"])
        rows = [(r["round"], r["turn"]) for r in self.archive(rig)]
        self.assertEqual(rows, [(battle["battle.round"], "me"), (battle["battle.round"], "him")])

    def test_the_record_of_one_round_does_not_stand_for_the_next(self):
        rig, his, out = self.his_turn()                                     # round R: his state is on record
        mine = self.my_turn(his)
        rig.tick(battle_read("B1", mine))
        out = rig.tick(battle_read("B1", dict(mine, **{"battle.usersEffects": []})))
        later = dict(mine, **{"battle.activeUserId": FOE, "battle.version": self.v + 6})
        out = rig.tick(*answers(out), battle_read("B1", later))             # round R+1: the read behind my actions
        self.assertEqual(kinds(out), ["full", "log 8"])                     # came plain, so his turn is read in full
        out = rig.tick(battle_read("B1", dict(later, **{"battle.usersEffects": []})))
        self.assertEqual(kinds(out), ["light"])
        self.assertEqual([(r["round"], r["turn"]) for r in self.archive(rig)][-1], (self.R + 1, "him"))

    @staticmethod
    def archive(rig):
        import gzip
        import os
        with gzip.open(os.path.join(rig.combat.fights, "live_states", "B1.full.jsonl.gz"), "rt") as f:
            return [json.loads(line) for line in f]

    def test_his_kit_read_rides_a_light_read_too(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.usersEffects": []})
        out = rig.tick(battle_read("B1", his))
        self.assertEqual(kinds(out), ["light", "kit"])

    def test_an_ais_turn_is_not_watched_the_read_behind_the_nudge_stays_full(self):
        """An AI acts when it is nudged, so the read behind the nudge is the one my turn starts with. Were it a
        light one, every round against an AI would cost a round trip more and save nothing."""
        rig = Rig()
        battle, ents, out = start_fight(rig)
        users = battle["battle.usersState.*.userId"]
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.version": battle["battle.version"] + 2,
                              "battle.usersState.*.isAi": [u == FOE for u in users]})
        out = rig.tick(*answers(out), battle_read("B1", dict(his, **{"battle.usersEffects": []})))
        self.assertIn(f"{battle['battle.round']}:him", rig.world["battle"]["archived"])   # on record, and still:
        self.assertEqual((kinds(out), watching(out)), (["act", "full", "log 8"], [False, True, True]))
        self.assertIn("AI turn", out["note"])
        mine = dict(his, **{"battle.activeUserId": C.ME, "battle.round": battle["battle.round"] + 1,
                            "battle.version": his["battle.version"] + 3, "battle.usersEffects": []})
        out = rig.tick(*answers(out), battle_read("B1", mine))
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])          # planned on at once: no second read

    def test_a_light_read_that_comes_back_empty_is_still_followed_by_the_full_read_when_my_turn_shows(self):
        rig, his, out = self.his_turn()
        out = rig.tick(battle_read("B1", {}), user("BATTLE", bid="B1"))     # the light read: nothing in it
        self.assertEqual(kinds(out), ["light", f"log {C.ENTRIES_TURN}", "profile"])   # asked again, plainly
        out = rig.tick(battle_read("B1", self.my_turn(his)), user("BATTLE", bid="B1"), dt=1)
        self.assertEqual(kinds(out), ["full", f"log {C.ENTRIES_TURN}"])     # that read had no effect list either
        self.assertEqual(acts(out), [])

    def test_the_fights_end_is_seen_on_a_light_read(self):
        rig, his, out = self.his_turn()
        hp = list(his["battle.usersState.*.curHealth"])
        hp[his["battle.usersState.*.userId"].index(FOE)] = 0
        out = rig.tick(battle_read("B1", dict(his, **{"battle.usersState.*.curHealth": hp})))
        self.assertIn("BATTLE OVER (won)", out["note"])

    def test_an_empty_answer_to_a_light_read_says_nothing_about_full_reads(self):
        rig, his, out = self.his_turn()
        rig.tick(battle_read("B1", {}), user("BATTLE", bid="B1"))
        self.assertNotIn("ground_refused", rig.world["battle"])
        self.assertNotIn("full_refused", rig.world["battle"])

    def test_an_empty_answer_to_my_turns_full_read_drops_the_richest_part_it_asked_for(self):
        rig, his, out = self.his_turn()
        out = rig.tick(battle_read("B1", self.my_turn(his)))                # my turn: the full read, with the ground
        self.assertTrue(any(k.startswith("battle.groundEffects") for k in out["steps"][0]["select"]))
        rig.tick(battle_read("B1", {}), user("BATTLE", bid="B1"))
        self.assertTrue(rig.world["battle"]["ground_refused"])

    # ---- my turn
    def test_a_light_read_that_shows_my_turn_is_followed_by_the_full_read_at_once(self):
        rig, his, out = self.his_turn()
        mine = self.my_turn(his)
        out = rig.tick(battle_read("B1", mine), dt=out["hold"] + 1)
        self.assertEqual((kinds(out), out["hold"]), (["full", f"log {C.ENTRIES_TURN}"], 0))   # was: the actions
        self.assertEqual(watching(out), [False, False])                     # my turn's read: the budget keeps it
        self.assertIn("MY TURN: reading the live state", out["note"])
        self.assertEqual(rig.world["battle"]["turn"]["T"], rig.t)           # the turn's clock runs from here
        n = len(rig.combat.plan_args)
        out = rig.tick(battle_read("B1", dict(mine, **{"battle.usersEffects": []})), dt=2)
        self.assertEqual(kinds(out), ["act", "wait", "act", "full", "log 8"])
        self.assertEqual([s["input"]["version"] for s in out["steps"] if s.get("call") == "combat.performAction"],
                         [self.v + 4, self.v + 5])
        plan = rig.combat.plan_args[n:]
        self.assertEqual((len(plan), plan[0]["live"]), (1, True))           # planned once, on the exact state
        self.assertAlmostEqual(plan[0]["seconds"], C.BEST_LINE_AT - 2, places=3)   # the round trip came off it
        self.assertEqual([(r["round"], r["turn"]) for r in self.archive(rig)][-1], (self.R + 1, "me"))

    def test_the_log_of_his_whole_turn_comes_with_my_turns_full_read(self):
        rig, his, out = self.his_turn()
        mine = self.my_turn(his)
        rig.tick(battle_read("B1", mine))
        lines = dict(zip(K.ENT, ([f"h{i}" for i in range(12)], [self.R] * 12, [FOE] * 12,
                                 [f"a{i}" for i in range(12)], [["hit"]] * 12)))
        out = rig.tick(battle_read("B1", dict(mine, **{"battle.usersEffects": []})),
                       res("combat.getBattleEntries", lines, {"battleId": "B1", "limit": C.ENTRIES_TURN}))
        kept = [e[3] for e in rig.world["battle"]["entries"] if e[2] == FOE and str(e[0]).startswith("h")]
        self.assertEqual(sorted(kept), sorted(f"a{i}" for i in range(12)))  # twelve lines: more than a poll's eight
        self.assertEqual(kinds(out)[-1], "log 8")                           # all new, but fewer than asked: no gap

    def test_a_read_as_long_as_was_asked_for_that_reaches_a_known_line_left_nothing_out(self):
        rig, his, out = self.his_turn()
        mine = self.my_turn(his)
        rig.tick(battle_read("B1", mine))
        last = rig.world["battle"]["entries"][-1]                           # the newest line in hand
        n = C.ENTRIES_TURN - 1
        lines = dict(zip(K.ENT, ([f"h{i}" for i in range(n)] + [last[0]], [self.R] * n + [last[1]],
                                 [FOE] * n + [last[2]], ["a"] * n + [last[3]], [["hit"]] * (n + 1))))
        out = rig.tick(battle_read("B1", dict(mine, **{"battle.usersEffects": []})),
                       res("combat.getBattleEntries", lines, {"battleId": "B1", "limit": C.ENTRIES_TURN}))
        self.assertEqual(kinds(out)[-1], "log 8")                           # nineteen new and one known: no gap
        self.assertEqual([e[0] for e in rig.world["battle"]["entries"]][-n - 1:], [last[0]] + lines["*.id"][:n][::-1])

    def test_a_turn_of_his_longer_than_the_read_is_read_again_whole(self):
        ents = fixture()[1]
        rig, his, out = self.his_turn()
        mine = self.my_turn(his)
        rig.tick(battle_read("B1", mine))
        n = C.ENTRIES_TURN
        lines = dict(zip(K.ENT, ([f"h{i}" for i in range(n)], [self.R] * n, [FOE] * n, ["a"] * n, [["hit"]] * n)))
        full = res("combat.getBattleEntries", lines, {"battleId": "B1", "limit": n})
        out = rig.tick(battle_read("B1", dict(mine, **{"battle.usersEffects": []})), full)   # twenty lines, all new
        self.assertEqual(kinds(out)[-1], f"log {C.ENTRIES_START}")          # older ones may lie between: all of it
        between = [f"g{i}" for i in range(5)]                               # five more that the read left out
        was = [e[0] for e in rig.world["battle"]["entries"] if not e[0].startswith("h")]
        whole = {k: lines[k] + c + ents[k] for k, c in zip(K.ENT, (between, [self.R] * 5, [FOE] * 5, ["a"] * 5,
                                                                      [["hit"]] * 5))}
        out = rig.tick(*answers(out), battle_read("B1", dict(his, **{"battle.usersEffects": []})),
                       res("combat.getBattleEntries", whole, {"battleId": "B1", "limit": C.ENTRIES_START}))
        self.assertFalse(rig.world["battle"]["log_gap"])                    # (these are known now)
        kept = [e[0] for e in rig.world["battle"]["entries"]]               # in the game's order, oldest first:
        self.assertEqual(kept, was + between[::-1] + lines["*.id"][::-1])   # the five before the twenty

    def test_a_slow_round_trip_still_leaves_the_planner_three_seconds(self):
        rig, his, out = self.his_turn()
        mine = self.my_turn(his)
        rig.tick(battle_read("B1", mine))
        out = rig.tick(battle_read("B1", dict(mine, **{"battle.usersEffects": []})), dt=14.0)
        self.assertAlmostEqual(rig.combat.plan_args[-1]["seconds"], C.PLAN_AT_LEAST, places=3)   # was: 1 s
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])
        row = self.played(rig, out, mine)
        self.assertEqual((row["fired_after"], row["outcome"]), (14.0, "acted"))

    def test_only_the_turns_first_plan_is_given_the_three_seconds(self):
        """A plan the game refused is replaced from what is left of the fifteen seconds, as on any turn: past
        them the best line so far or a basic action goes out at once."""
        rig, his, out = self.his_turn()
        mine = self.my_turn(his)
        rig.tick(battle_read("B1", mine))
        live = dict(mine, **{"battle.usersEffects": []})
        out = rig.tick(battle_read("B1", live), dt=14.0)                    # the first plan: three seconds
        out = rig.tick(*answers(out, NOT_VALID), battle_read("B1", live), dt=2.0)   # refused, at T+16
        self.assertAlmostEqual(rig.combat.plan_args[-1]["seconds"], C.BEST_LINE_AT - 16.0, places=3)
        self.assertEqual(len(acts(out)), 1)                                 # (no planner time: a basic action)

    def played(self, rig, out, mine):
        """The turn is over: its row in turns.jsonl."""
        rig.tick(*answers(out), battle_read("B1", dict(mine, **{"battle.activeUserId": FOE,
                                                                "battle.version": mine["battle.version"] + 2})))
        return turns(rig)[-1]

    def test_a_full_read_that_is_refused_is_not_waited_for(self):
        rig, his, out = self.his_turn()
        moved = [9 if u == FOE else x for u, x in zip(his["battle.usersState.*.userId"],
                                                      his["battle.usersState.*.longitude"])]
        mine = self.my_turn(his, **{"battle.usersState.*.longitude": moved})
        rig.tick(battle_read("B1", mine))
        out = rig.tick(limited("combat.getBattle", {"battleId": "B1"}), dt=1)
        self.assertIn("last good read", out["note"])
        sent = [s["input"] for s in out["steps"] if s.get("call") == "combat.performAction"]
        self.assertEqual([a["version"] for a in sent], [self.v + 4, self.v + 5])   # the light read's version,
        self.assertEqual(rig.world["battle"]["battle"]["battle.usersState.*.longitude"], moved)   # and where he stands
        self.assertFalse(rig.combat.plan_args[-1]["live"])                  # (the effect list is not known)
        self.assertEqual(self.played(rig, out, mine)["outcome"], "acted")

    def test_his_turns_lines_that_come_without_their_read_are_not_taken_off_my_hp_twice(self):
        """The fight's result, when no read shows its end, is my last HP less what the log shows on me after
        it. The light read that shows my turn has his whole turn in its HP, and none of his lines yet."""
        rig, his, out = self.his_turn()
        mine = self.my_turn(his)
        rig.tick(battle_read("B1", mine))
        state = rig.world["battle"]
        n = len(state["entries"])
        self.assertEqual(state["n_at_battle"], n)
        lines = dict(zip(K.ENT, (["h2", "h1", "h0"], [self.R] * 3, [FOE] * 3, ["a"] * 3, [["hit"]] * 3)))
        out = rig.tick(limited("combat.getBattle", {"battleId": "B1"}),     # the full read is refused; the log
                       res("combat.getBattleEntries", lines, {"battleId": "B1", "limit": C.ENTRIES_TURN}), dt=1)
        self.assertIn("last good read", out["note"])                        # read beside it comes
        self.assertEqual((len(state["entries"]), state["n_at_battle"]), (n + 3, n + 3))

    def test_a_full_read_that_does_not_come_is_not_waited_for_past_twelve_seconds(self):
        rig, his, out = self.his_turn()
        mine = self.my_turn(his)
        rig.tick(battle_read("B1", mine))
        out = rig.tick(dt=5)                                                # the relay is back with nothing
        self.assertEqual((kinds(out), acts(out)), (["light", f"log {C.ENTRIES_TURN}"], []))   # asked again, plainly
        out = rig.tick(dt=C.LAST_GOOD_READ_AT - 5)
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])
        self.assertIn("last good read", out["note"])
        self.assertEqual(self.played(rig, out, mine)["outcome"], "acted")
        self.assertEqual(rig.world["records"]["turns_missed"], 0)

    def test_a_full_read_that_comes_back_plain_is_planned_on_and_not_asked_for_again(self):
        rig, his, out = self.his_turn()
        mine = self.my_turn(his)
        rig.tick(battle_read("B1", mine))
        out = rig.tick(battle_read("B1", mine), dt=1)                       # the fighters, and no effect list
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])
        self.assertNotIn("reading the live state", out["note"])

    def test_a_turn_whose_state_is_in_hand_already_asks_for_nothing(self):
        """He let his turn run out and nothing moved: the version is the one my last full read was of."""
        rig, his, out = self.his_turn()
        out = rig.tick(battle_read("B1", dict(his, **{"battle.activeUserId": C.ME, "battle.round": self.R + 1})))
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])
        self.assertTrue(rig.combat.plan_args[-1]["live"])

    def test_the_directors_window_is_watched_light_and_the_state_is_read_once(self):
        rig = Rig()
        rig.combat.kits.add(FOE)
        rig.world["control"]["director_mode"] = True
        battle, ents = fixture()
        rig.tick(user("BATTLE", bid="B1"))
        live = dict(battle, **{"battle.usersEffects": []})
        out, seen = rig.tick(battle_read("B1", live), log_read("B1", ents)), []
        for _ in range(6):
            seen.append(kinds(out))
            self.assertIn("director's move", out["note"])
            out = rig.tick(battle_read("B1", battle), dt=5)
        self.assertEqual(seen, [["light"]] * 6)                             # was: full, log 8, six times
        v = battle["battle.version"]
        out = rig.tick(battle_read("B1", dict(battle, **{"battle.version": v + 1})), dt=1)   # he acted: read it
        self.assertEqual(kinds(out), ["full", f"log {C.ENTRIES_TURN}"])
        out = rig.tick(battle_read("B1", dict(live, **{"battle.version": v + 1})), dt=1)
        self.assertEqual(kinds(out), ["light"])                             # and back to watching


    def test_where_the_effect_list_cannot_be_had_the_directors_window_asks_for_it_once(self):
        rig = Rig()
        rig.combat.kits.add(FOE)
        rig.world["control"]["director_mode"] = True
        battle, ents = fixture()
        rig.tick(user("BATTLE", bid="B1"))
        out, seen = rig.tick(battle_read("B1", battle), log_read("B1", ents)), []   # the opening read: no effects
        for _ in range(5):
            seen.append(kinds(out))
            out = rig.tick(battle_read("B1", battle), dt=out["hold"] + 1)   # nor in any read after it
        self.assertEqual(seen, [["full", "log 8"]] + [["light"]] * 4)       # one try at this version, then watching
        moved = dict(battle, **{"battle.version": battle["battle.version"] + 1})
        out, seen = rig.tick(battle_read("B1", moved), dt=1), []            # he acted: one try at the new version
        for _ in range(4):
            seen.append(kinds(out))
            out = rig.tick(battle_read("B1", moved), dt=out["hold"] + 1)
        self.assertEqual(seen, [["full", f"log {C.ENTRIES_TURN}"]] + [["light"]] * 3)


class Duel:
    """A stand-in for a fight against a player, turn by turn. It answers exactly the calls of each batch, in
    order. My turn passes to him when the game has taken the last action of a batch; his turn lasts `his_turn`
    seconds, he acts `his_actions` times in it (a new version and a log line each), and then the round goes up
    and the turn is mine. The relay takes `lag` seconds before a batch's first call. `lost`: the numbers of the
    full reads that do not come back (the connector refuses them)."""

    def __init__(self, rig, his_turn=20.0, his_actions=3, lag=3.0, lost=()):
        self.rig, self.his_turn, self.his_actions, self.lag, self.lost = rig, his_turn, his_actions, lag, set(lost)
        self.state, self.first_log = fixture()
        self.R, self.v = self.state["battle.round"], self.state["battle.version"]
        self.mine, self.his_at, self.lines, self.asked, self.fulls, self.sizes = True, [], [], [], 0, []
        self.out = rig.tick(user("BATTLE", bid="B1"))

    def advance(self, now):
        """What he has done by now."""
        while not self.mine and self.his_at and now >= self.his_at[0]:
            at = self.his_at.pop(0)
            self.v += 1
            if self.his_at:
                self.lines.insert(0, (f"h{self.v}", self.R, FOE, f"his_{len(self.his_at)}", ["hit"]))
            else:
                self.mine, self.R = True, self.R + 1                # his last moment: the turn is mine

    def answer(self, step, now):
        ep, inp = step["call"], step["input"]
        self.advance(now)
        if ep == "combat.performAction":
            if not self.mine or inp["version"] != self.v:
                return res(ep, {"notification": "This action is not valid anymore"}, inp)
            self.v += 1
            self.lines.insert(0, (f"m{self.v}", self.R, C.ME, inp["actionId"], ["hit"]))
            self.acted = True
            return res(ep, {}, inp)
        if ep == "combat.getBattle":
            if self.acted:                                          # my actions are in: the turn is his now
                self.acted, self.mine = False, False
                step_ = self.his_turn / (self.his_actions + 1)
                self.his_at = [now + step_ * (i + 1) for i in range(self.his_actions + 1)]
            full = "battle.usersEffects" in step["select"]
            self.asked.append("full" if full else "light")
            if full:
                self.fulls += 1
                if self.fulls in self.lost:
                    return limited(ep, inp)
            read = dict(self.state, **{"battle.round": self.R, "battle.version": self.v,
                                       "battle.activeUserId": C.ME if self.mine else FOE})
            if full:
                read["battle.usersEffects"] = []
            return res(ep, read, inp)
        if ep == "combat.getBattleEntries":
            self.asked.append("log")
            self.sizes.append(inp["limit"])
            rows = self.lines[:inp["limit"]]
            read = {k: [r[i] for r in rows] for i, k in enumerate(K.ENT)}
            if inp["limit"] >= C.ENTRIES_START:                     # the whole log: the lines before the stand-in's too
                read = {k: (read[k] + self.first_log[k])[:inp["limit"]] for k in K.ENT}
            return res(ep, read, inp)
        if ep == "jutsu.getPublicUserJutsus":
            return res(ep, {"*.jutsuId": ["j1"], "*.level": [25], "*.equipped": [True]}, inp)
        return user("BATTLE", bid="B1")

    def play(self, seconds):
        end, self.acted = self.rig.t + seconds, False
        while self.rig.t < end:
            out, now, results = self.out, self.rig.t + self.out["hold"] + self.lag, []
            for step in out["steps"]:
                if "wait" in step:
                    now += step["wait"]
                    continue
                now += 0.4
                results.append(self.answer(step, now)._replace(at=now))
            self.out = self.rig.tick(*results, dt=now - self.rig.t)
        return self


class AWholeFight(unittest.TestCase):
    def fight(self, seconds=420, **kw):
        rig = Rig()
        rig.combat.kits.add(FOE)
        return rig, Duel(rig, **kw).play(seconds)

    def every_turn_was_played(self, rig, at_least):
        played = turns(rig)
        self.assertGreaterEqual(len(played), at_least)
        self.assertEqual({t["outcome"] for t in played}, {"acted"})
        self.assertEqual(rig.world["records"]["turns_missed"] + rig.world["records"]["turns_unresolved"], 0)
        return played

    def test_two_full_reads_a_round_and_every_turn_played(self):
        rig, game = self.fight()
        played = self.every_turn_was_played(rig, 10)
        rounds = len(played)
        self.assertLessEqual(game.asked.count("full"), 2 * rounds + 2)      # was: every poll, 6 to 8 a round
        self.assertGreater(game.asked.count("light"), 2 * rounds)           # his turn is still watched as often
        self.assertLessEqual(max(t["fired_after"] for t in played), C.FIRE_BY)
        self.assertEqual(about(rig, "turn"), [])

    def test_both_states_of_every_round_are_on_record(self):
        rig, game = self.fight()
        rows = [(r["round"], r["turn"]) for r in TheReadsOfARound.archive(rig)]
        first, last = rows[0][0], rows[-1][0]
        self.assertEqual(rows[:-1], [(r, side) for r in range(first, last + 1) for side in ("me", "him")][:len(rows) - 1])
        self.assertEqual(len(set(rows)), len(rows))                         # each once

    def test_the_log_keeps_every_line_of_his_and_of_mine(self):
        rig, game = self.fight(his_actions=6)
        kept = {e[0] for e in rig.world["battle"]["entries"]}
        made = {line[0] for line in game.lines[8:]}                         # (the newest are read with the next poll)
        self.assertEqual(made - kept, set())

    def test_a_turn_of_his_with_more_lines_than_my_turns_read_asks_for(self):
        rig, game = self.fight(seconds=300, his_actions=C.ENTRIES_TURN + 5, his_turn=40.0)
        self.every_turn_was_played(rig, 5)
        self.assertIn(C.ENTRIES_START, game.sizes[1:])                      # the whole log was read again
        kept = [e[0] for e in rig.world["battle"]["entries"]]
        self.assertEqual({line[0] for line in game.lines[C.ENTRIES_TURN:]} - set(kept), set())
        made = [line[0] for line in game.lines[::-1]]                       # oldest first, as the game logged them
        self.assertEqual([i for i in kept if i in set(made)], [i for i in made if i in set(kept)])   # in its order

    def test_with_a_relay_that_takes_ten_seconds_a_batch(self):
        rig, game = self.fight(seconds=600, lag=10.0, his_turn=30.0)
        played = self.every_turn_was_played(rig, 8)
        self.assertLessEqual(max(t["fired_after"] for t in played), C.FIRE_BY)   # the round trip fits in the rule

    def test_when_every_third_full_read_is_refused(self):
        rig, game = self.fight(lost=range(3, 200, 3))
        played = self.every_turn_was_played(rig, 10)
        self.assertTrue(any(t["from_last_read"] for t in played))           # some turns went from the light read
        self.assertLessEqual(max(t["fired_after"] for t in played), C.FIRE_BY)


if __name__ == "__main__":
    unittest.main()
