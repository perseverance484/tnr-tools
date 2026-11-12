"""The independent review of AP1 (docs/reviews/AI_PLAYER_AP1_REVIEW.md on chatgpt/review-ai-player-ap1, e94bf21c):
one class per finding, each built from the review's own reproduction. Every test here fails on the reviewed commit
(583fe353). Finding 8 is player/tests/test_wiring.py.
"""
import datetime as dt
import gzip
import io
import json
import os
import subprocess
import time
import unittest

from player import brain, budget as B, calls as K, config as C, gates, relay
from player.tests.support import (FOE, LINE, Ledger, Rig, battle_read, fixture, gone, limited, log_read, res,
                                  start_fight, user)
from player.tests.test_relay import nxt, token_of, transcript
from player.world import utc_day

NOT_VALID = {"notification": "Action not valid anymore"}


def acts(out):
    return [s["input"]["actionId"] for s in out["steps"] if s.get("call") == "combat.performAction"]


def act_result(aid, data=None, error=None):
    return res("combat.performAction", data if data is not None or error else {}, {"battleId": "B1", "actionId": aid},
               error=error)


def answers(out, data=None, error=None):
    """One answer per action of a batch."""
    return [act_result(a, data, error) for a in acts(out)]


def waited(out):
    """Seconds the relay spends on a batch's waits."""
    return sum(s.get("wait", 0) for s in out["steps"])


def paced_actions(out):
    """The waits in front of a batch's actions that are not the gap between two actions of a turn."""
    steps = out["steps"]
    return [steps[i - 1]["wait"] for i, s in enumerate(steps)
            if s.get("call") == "combat.performAction" and i and "wait" in steps[i - 1]
            and steps[i - 1]["wait"] != C.ACTION_GAP]


def turns(rig):
    try:
        with open(os.path.join(rig.dir, "turns.jsonl"), encoding="utf8") as f:
            return [json.loads(line) for line in f]
    except OSError:
        return []


def about(rig, what, kind="finding"):
    return [e for e in rig.events(kind) if e.get("about") == what]


def my_line(rnd, action="stormblade_id"):
    """A battle-log read whose one line is an action of mine in that round."""
    return log_read("B1", dict(zip(K.ENT, (["e_mine"], [rnd], [C.ME], [action], [["hit"]]))))


class Game:
    """A stand-in for the game in a played-through fight. It answers exactly the calls each batch makes, in
    order, and nothing the brain did not ask for; an action is taken only on my turn and at the battle's own
    version; his turn lasts `his_turn` seconds (an AI's ends when it is nudged).

    It keeps its own clock of when each call really ran (`made`), apart from the budget's ledger: the relay
    spends `lag` seconds on a batch before its first call, and each call takes the next of `call_lags`."""

    def __init__(self, rig, his_turn=15.0, ai=False, lag=3.0, bid="B1", call_lags=(0.4,), before=()):
        self.rig, self.bid, self.his_turn, self.ai, self.lag = rig, bid, his_turn, ai, lag
        self.call_lags, self.made = call_lags, list(before)        # before: when earlier calls really ran
        self.state, self.first_log = fixture()
        users = self.state["battle.usersState.*.userId"]
        self.state["battle.usersState.*.isAi"] = [ai and u == FOE for u in users]
        self.R, self.v = self.state["battle.round"], self.state["battle.version"]
        self.mine, self.back_at, self.lines = True, None, []
        self.reads, self.delayed, self.fired = [], [], []
        self.out = rig.tick(user("BATTLE", bid=bid))

    def answer(self, step, now):
        ep, inp = step["call"], step["input"]
        if ep == "combat.performAction":
            if not self.mine:                                       # an AI's turn runs when a client asks
                self.mine, self.R, self.v = True, self.R + 1, self.v + 2
                return res(ep, {}, inp)
            if inp["version"] != self.v:
                return res(ep, NOT_VALID, inp)
            self.v += 1
            self.lines.insert(0, (f"m{self.v}", self.R, C.ME, inp["actionId"], ["hit"]))
            self.passed = True
            return res(ep, {}, inp)
        if ep == "combat.getBattle":
            if not self.mine and not self.ai and now >= self.back_at:
                self.mine, self.R, self.v = True, self.R + 1, self.v + 2
            self.reads.append(now)
            read = dict(self.state, **{"battle.round": self.R, "battle.version": self.v,
                                       "battle.activeUserId": C.ME if self.mine else FOE})
            if "battle.usersEffects" in step["select"]:
                read["battle.usersEffects"] = []
            return res(ep, read, inp)
        if ep == "combat.getBattleEntries":
            rows = self.lines[:inp["limit"]]
            return res(ep, dict(self.first_log) if inp["limit"] > 8 else
                       {k: [r[i] for r in rows] for i, k in enumerate(K.ENT)}, inp)
        if ep == "jutsu.getPublicUserJutsus":
            return res(ep, {"*.jutsuId": ["j1"], "*.level": [25], "*.equipped": [True]}, inp)
        return user("BATTLE", bid=self.bid)

    def play(self, seconds):
        """Run the loop for this long. Each batch: the brain's hold, the relay's `lag`, then every wait and call
        in order, each call at its own real time; the answers carry the time they came back."""
        end = self.rig.t + seconds
        while self.rig.t < end:
            out, now, results, self.passed = self.out, self.rig.t + self.out["hold"] + self.lag, [], False
            for step in out["steps"]:
                if "wait" in step:
                    now += step["wait"]
                    continue
                self.made.append(now)
                now += self.call_lags[len(self.made) % len(self.call_lags)]
                results.append(self.answer(step, now)._replace(at=now))
            if self.passed:                                         # my actions landed: the turn is his now
                self.mine, self.back_at = False, now + self.his_turn
            self.out = self.rig.tick(*results, dt=now - self.rig.t)
            self.delayed += paced_actions(self.out)
            self.fired += [self.rig.t] if acts(self.out) else []
        return self

    def longest_unread(self):
        return max(b - a for a, b in zip(self.reads, self.reads[1:]))

    def most_in_a_minute(self):
        """The most calls that really ran in any rolling minute, by this game's own clock."""
        return max(sum(1 for u in self.made if t - 60 < u <= t) for t in self.made)


class F1TheSharedLimit(unittest.TestCase):
    def test_the_reviews_sequence_never_passes_thirty_and_says_when_it_cannot_do_better(self):
        rig = Rig()
        rig.tick(user())
        rig.world["budget"]["calls"] = []
        ledger = Ledger(rig)
        rig.brain.budget.pace([K.user()] * C.WORLD_CAP, "world")           # twenty world calls at once
        rig.t += 10
        battle, ents, out = start_fight(rig)
        R, v = battle["battle.round"], battle["battle.version"]
        out = rig.tick(battle_read("B1", dict(battle, **{"battle.round": R + 1, "battle.version": v + 4})), dt=10)
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])
        self.assertEqual(paced_actions(out), [])                           # both turns' actions went at once
        his = dict(battle, **{"battle.round": R + 1, "battle.version": v + 6, "battle.activeUserId": FOE})
        out = rig.tick(battle_read("B1", his), dt=2)
        self.assertLessEqual(ledger.worst(), C.CALL_LIMIT)                  # was 32
        # thirty calls in twenty seconds leave none for the rest of the minute: the wait is real, and on record
        self.assertTrue(out["hold"] <= B.BLIND_MAX or about(rig, "budget"))

    def test_a_fight_that_starts_from_a_hunt_at_its_cap_keeps_every_promise(self):
        """World to battle, turn after turn, long turns of his, for four minutes: under thirty in every rolling
        minute, no action ever waits, the fight is never left unread for long, and every turn is played."""
        rig = Rig()
        rig.tick(user())
        rig.world["budget"]["calls"] = [[rig.t - 3.0 * i, "world"] for i in range(C.WORLD_CAP)][::-1]
        ledger = Ledger(rig)
        game = Game(rig, his_turn=15.0, call_lags=(0.4, 2.0, 0.2, 3.0, 0.3),
                    before=[c[0] for c in rig.world["budget"]["calls"]]).play(240)
        self.assertLessEqual(ledger.worst(), C.CALL_LIMIT)
        self.assertLessEqual(game.most_in_a_minute(), C.CALL_LIMIT)          # by the game's own clock
        self.assertEqual(game.delayed, [])
        self.assertEqual(about(rig, "budget"), [])
        self.assertLessEqual(game.longest_unread(), B.BLIND_MAX + game.lag + 2 * C.ACTION_GAP)
        played = turns(rig)
        self.assertGreaterEqual(len(played), 8)
        self.assertEqual({t["outcome"] for t in played}, {"acted"})
        self.assertLessEqual(max(t["unseen"] for t in played), B.BLIND_MAX + game.lag + 2 * C.ACTION_GAP)
        self.assertEqual(rig.world["records"]["turns_missed"] + rig.world["records"]["turns_unresolved"], 0)

    def test_the_same_fight_after_twenty_world_calls_at_once_says_what_it_could_not_do(self):
        """The review's start: a burst no activity makes, but that the budget alone would have let through."""
        rig = Rig()
        rig.tick(user())
        rig.world["budget"]["calls"] = []
        ledger = Ledger(rig)
        rig.brain.budget.pace([K.user()] * C.WORLD_CAP, "world")
        burst = [rig.t + 0.4 * i for i in range(C.WORLD_CAP)]               # when those twenty really ran
        rig.t += 10
        game = Game(rig, his_turn=6.0, call_lags=(0.2, 4.0, 0.3), before=burst).play(180)
        self.assertLessEqual(ledger.worst(), C.CALL_LIMIT)
        self.assertLessEqual(game.most_in_a_minute(), C.CALL_LIMIT)          # by the game's own clock
        self.assertEqual(game.delayed, [])                                  # the reads gave way, never an action
        self.assertEqual({t["outcome"] for t in turns(rig)}, {"acted"})     # and no turn was lost for it
        late = [e for e in about(rig, "budget")]
        self.assertTrue(late)                                               # the long blind wait is on record
        self.assertTrue(all("performAction" not in e["text"] for e in late))

    def test_turn_after_turn_against_an_ai_stays_under_the_limit(self):
        rig = Rig()
        ledger = Ledger(rig)
        game = Game(rig, ai=True, lag=2.0, call_lags=(0.2, 0.2, 5.0, 0.2)).play(240)   # as fast as the relay can go
        self.assertLessEqual(ledger.worst(), C.CALL_LIMIT)
        self.assertLessEqual(game.most_in_a_minute(), C.CALL_LIMIT)          # by the game's clock, not the ledger's
        self.assertEqual(game.delayed, [])                                  # the reads give way, never an action
        played = turns(rig)
        self.assertGreaterEqual(len(played), 10)
        self.assertEqual({t["outcome"] for t in played}, {"acted"})

    def test_a_storm_of_refusals_on_my_turn_stays_under_the_limit(self):
        rig = Rig()
        ledger = Ledger(rig)
        battle, ents, out = start_fight(rig)
        for _ in range(25):
            out = rig.tick(*[limited("combat.performAction", {"battleId": "B1", "actionId": a}) for a in acts(out)],
                           limited("combat.getBattle", {"battleId": "B1"}), dt=waited(out) + 1)
        self.assertLessEqual(ledger.worst(), C.CALL_LIMIT)

    def test_the_potion_at_the_fights_end_is_inside_the_limit_too(self):
        rig = Rig()
        ledger = Ledger(rig)
        battle, ents, out = start_fight(rig)
        rig.world["budget"]["calls"] += [[rig.t, "battle"]] * (C.CALL_LIMIT - 4 - rig.brain.budget.used())
        ledger.rows = [(c[0], c[1], "") for c in rig.world["budget"]["calls"]]
        out = gone(rig, dt=waited(out) + 1)
        self.assertEqual(rig.calls(out), ["item.consume", "profile.getUser"])
        self.assertLessEqual(ledger.worst(), C.CALL_LIMIT)

    def test_how_long_the_fight_went_unread_is_logged_apart_from_the_planning_time(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        R, v = battle["battle.round"], battle["battle.version"]
        his = dict(battle, **{"battle.version": v + 2, "battle.activeUserId": FOE})
        rig.tick(*answers(out), battle_read("B1", his), dt=4)
        rig.tick(battle_read("B1", dict(battle, **{"battle.round": R + 1, "battle.version": v + 4})), dt=9)
        self.assertEqual(rig.world["battle"]["turn"]["unseen"], 9.0)        # seen nine seconds after the last read
        rig.tick(*[act_result(a["actionId"]) for a in LINE], battle_read("B1", dict(his, **{"battle.round": R + 1})))
        self.assertEqual([(t["round"], t["unseen"], t["fired_after"]) for t in turns(rig)],
                         [(R, 1.0, 0.0), (R + 1, 9.0, 0.0)])


class F2APlanTheGameRefusedOrNeverGot(unittest.TestCase):
    def test_each_refused_plan_is_replaced_in_the_same_tick_until_nothing_is_left(self):
        """The review's sequence: both actions refused, then every read refused, at T+1, T+12, T+15 and T+20."""
        rig = Rig()
        battle, ents, out = start_fight(rig)
        seen = []
        for wait in (1, 11, 3, 5):
            out = rig.tick(*answers(out, NOT_VALID), limited("combat.getBattle", {"battleId": "B1"}), dt=wait)
            seen.append(acts(out))
            self.assertEqual(out["hold"], 0)
            if seen[-1]:
                self.assertEqual(out["steps"][0]["call"], "combat.performAction")   # the action first, then the read
        self.assertEqual(seen, [["defensiveStance"], ["wait"], [], []])
        self.assertIn("refused every fallback", rig.events("finding")[-1]["text"])
        self.assertEqual(rig.calls(out), ["combat.getBattle", "combat.getBattleEntries"])   # still asking

    def test_actions_that_errored_and_reads_that_fail_end_in_an_action_by_t_plus_12(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        boom = res("combat.getBattle", None, {"battleId": "B1"}, error="unreadable result: not JSON")
        out = rig.tick(*answers(out, error="Error calling combat.performAction: boom"), boom, dt=4)
        self.assertEqual(acts(out), [])                                     # they may have landed: look first
        out = rig.tick(boom, dt=C.LAST_GOOD_READ_AT - 4)
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])          # T+12 and still no read: act
        self.assertEqual(out["steps"][0]["input"]["version"], battle["battle.version"])   # at the version last seen
        self.assertEqual(rig.world["battle"].get("banned", []), [])          # nothing is banned on a guess

    def test_a_tick_that_crashes_after_planning_leaves_no_plan_marked_as_sent(self):
        for where in ("_compose", "_record"):
            rig = Rig()
            rig.tick(user("BATTLE", bid="B1"))
            battle, ents = fixture()
            real = getattr(rig.brain, where)

            def boom(*a, **k):
                setattr(rig.brain, where, real)
                raise RuntimeError("one-time crash")
            setattr(rig.brain, where, boom)
            rig.t += 1
            read = [battle_read("B1", dict(battle, **{"battle.usersEffects": []})), log_read("B1", ents)]
            req = relay.request_path(rig.dir, 1)
            relay.write(req, {"seq": 1, "results": relay.pack([r._replace(at=rig.t) for r in read]), "usage": {}})
            brain.answer(rig.brain, rig.dir, req)
            batch = relay.read(relay.batch_path(rig.dir, 1))
            self.assertEqual((batch["steps"], batch["hold"]), ([], 1.0), where)   # come back at once: a fight is on
            self.assertFalse((rig.world["battle"].get("turn") or {}).get("fired_at"), where)
            self.assertEqual(rig.brain.budget.used(), 2, where)             # the batch never went: it cost nothing
            t0 = rig.t
            out = rig.tick(limited("combat.getBattle", {"battleId": "B1"}), dt=1)   # and the next read fails
            self.assertEqual(acts(out), [a["actionId"] for a in LINE], where)
            self.assertEqual(rig.world["battle"]["turn"]["fired_at"] - t0, 1, where)   # two seconds after the read

    def test_a_planner_that_crashes_still_ends_in_an_action(self):
        rig = Rig()

        def crash(*a, **k):
            raise ValueError("bad FIRE line")
        rig.combat.plan_turn = crash
        battle, ents, out = start_fight(rig)
        self.assertEqual(acts(out), ["defensiveStance"])
        self.assertIn("planner crashed", rig.events("finding")[-1]["text"])

    def test_a_line_the_gates_refuse_is_planned_again_and_the_fight_is_not_set_aside(self):
        rig = Rig()
        rig.combat.line = [{"actionId": "flee", "longitude": 6, "latitude": 4, "name": "Flee"}] + LINE
        battle, ents, out = start_fight(rig)
        self.assertEqual((out["activity"], acts(out)), ("battle", [a["actionId"] for a in LINE]))
        self.assertEqual(rig.world.own("brain").get("blocked", {}), {})
        self.assertEqual([e["about"] for e in rig.events("finding")], ["gate"])


class F3TheFallbackHonoursRefusals(unittest.TestCase):
    def test_a_refused_stance_is_not_sent_again_when_the_planner_is_out_of_time(self):
        rig = Rig()
        rig.combat.line = None
        battle, ents, out = start_fight(rig)
        self.assertEqual(acts(out), ["defensiveStance"])
        out = rig.tick(*answers(out, NOT_VALID), battle_read("B1", battle), dt=C.BEST_LINE_AT)
        self.assertLess(rig.combat.plan_args[-1]["seconds"], 0.5)           # T+15: no planner run
        self.assertEqual(acts(out), ["wait"])                               # was defensiveStance again
        out = rig.tick(*answers(out, NOT_VALID), battle_read("B1", battle), dt=2)
        self.assertEqual(acts(out), [])                                     # the game has refused them all
        self.assertTrue(rig.calls(out))
        self.assertEqual(rig.world["battle"]["pick"]["actions"], [])

    def test_the_best_line_so_far_is_fired_when_the_planner_runs_out_of_time(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        out = rig.tick(*[limited("combat.performAction", {"battleId": "B1", "actionId": a}) for a in acts(out)],
                       battle_read("B1", battle), dt=C.BEST_LINE_AT)        # the connector refused the whole plan
        self.assertLess(rig.combat.plan_args[-1]["seconds"], 0.5)           # and now it is T+15
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])          # the line the turn already had
        self.assertIn("best line so far", out["note"])


class F4ResultsBelongToTheirRelayAndBatch(unittest.TestCase):
    def setUp(self):
        self.rig = Rig()
        self.rig.world.save()
        self.t = os.path.join(self.rig.dir, "relay.jsonl")
        os.environ.update(TNR_TRANSCRIPT=self.t, TNR_PLAYER_NO_DAEMON="1", TNR_PLAYER_LIVE=self.rig.dir,
                          TNR_PLAYER_FIGHTS=os.path.join(self.rig.dir, "fights"))

    def tearDown(self):
        for k in ("TNR_TRANSCRIPT", "TNR_PLAYER_NO_DAEMON", "TNR_PLAYER_LIVE", "TNR_PLAYER_FIGHTS",
                  "CLAUDE_CONFIG_DIR"):
            os.environ.pop(k, None)

    def next(self, token=None):
        out = io.StringIO()
        brain.next_batch(self.rig.dir, token, out, lambda s: None)
        return out.getvalue().splitlines()

    def world(self):
        return brain.Brain(self.rig.dir).world

    def start(self):
        """A relay that has shaken hands and been given its first batch (one profile read)."""
        t0 = token_of(self.next()[0])
        self.rows = [("bash", "n0", nxt(t0), time.time())]
        transcript(self.t, self.rows)
        lines = self.next(t0)
        self.assertEqual([json.loads(x).get("call") for x in lines[:-1]], ["profile.getUser"])
        return token_of(lines[-1])

    def test_a_call_made_before_the_batch_and_answered_after_it_is_not_its_result(self):
        p = os.path.join(self.rig.dir, "t.jsonl")
        transcript(p, [("use", "a", "profile.getUser", {}, 90), ("bash", "n1", nxt("ab12cd-1"), 91),
                       ("use", "b", "profile.getUser", {}, 105), ("bash", "n2", nxt("ab12cd-2"), 106),
                       ("res", "a", '{"userData.status":"BATTLE","userData.battleId":"OLD"}', 110),   # late
                       ("res", "b", '{"userData.status":"AWAKE"}', 111)])
        results, _, strays = relay.read_batch(p, "ab12cd-2", [("profile.getUser", {})])
        self.assertEqual([r.data for r in results], [{"userData.status": "AWAKE"}])
        self.assertEqual(strays, 0)

    def test_an_unrelated_transcript_is_never_taken_for_the_relays(self):
        del os.environ["TNR_TRANSCRIPT"]
        home = os.path.join(self.rig.dir, "claude")
        os.makedirs(os.path.join(home, "projects", "x"))
        os.environ["CLAUDE_CONFIG_DIR"] = home
        transcript(os.path.join(home, "projects", "x", "other.jsonl"), [
            ("use", "f", "profile.getUser", {}, time.time() + 1),
            ("res", "f", '{"userData.status":"BATTLE","userData.battleId":"FOREIGN"}', time.time() + 1)])
        lines = self.next(token_of(self.next()[0]))
        self.assertIn("put", json.loads(lines[1]))                          # nobody's transcript: results by put
        lines = self.next(token_of(lines[-1]))
        self.assertIsNone(self.world()["battle"])                           # was: battle FOREIGN opened
        self.assertNotIn("FOREIGN", "\n".join(lines))

    def test_a_relay_that_was_replaced_is_stopped_and_nothing_is_taken_from_it(self):
        t1 = self.start()
        t0_new = token_of(self.next()[0])                                   # a new relay shakes hands
        transcript(self.t, self.rows + [("use", "a", "profile.getUser", {}, time.time()),
                                        ("bash", "n1", nxt(t1), time.time()),
                                        ("res", "a", json.dumps(user("BATTLE", bid="OLD").data), time.time())])
        self.assertEqual(self.next(t1), ["STOP superseded: another relay has taken over"])
        self.assertIsNone(self.world()["battle"])
        transcript(self.t, [("bash", "m0", nxt(t0_new), time.time())])
        self.assertEqual(json.loads(self.next(t0_new)[0]).get("call"), "profile.getUser")   # the new one carries on

    def test_the_same_batch_handed_in_twice_is_taken_once(self):
        t1 = self.start()
        transcript(self.t, self.rows + [("use", "a", "profile.getUser", {}, time.time()),
                                        ("bash", "n1", nxt(t1), time.time()), ("bash", "n1b", nxt(t1), time.time()),
                                        ("res", "a", json.dumps(user().data), time.time())])
        lines = self.next(t1)
        t2, seq = token_of(lines[-1]), self.world()["relay"]["seq"]
        again = self.next(t1)                                               # the second copy of the same call
        self.assertEqual(again, [relay.next_line(t2)])                      # no calls: only "come back"
        self.assertEqual(self.world()["relay"]["seq"], seq)                 # and no second tick

    def test_a_call_the_batch_did_not_ask_for_is_not_a_result_and_is_reported(self):
        t1 = self.start()
        now = time.time()
        transcript(self.t, self.rows + [
            ("use", "x", "profile.getUser", {"userId": "someone"}, now),    # changed
            ("use", "a", "profile.getUser", {}, now), ("use", "a2", "profile.getUser", {}, now),   # and repeated
            ("bash", "n1", nxt(t1), now),
            ("res", "x", json.dumps(user(sector=1).data), now), ("res", "a", json.dumps(user(sector=99).data), now),
            ("res", "a2", json.dumps(user(sector=2).data), now)])
        self.next(t1)
        self.assertEqual(self.world().me["sector"], 99)
        self.assertEqual([e["text"] for e in about(self.rig, "relay")],
                         ["the relay made 2 call(s) the batch did not ask for"])

    def test_a_put_for_another_batch_is_dropped(self):
        os.environ["TNR_TRANSCRIPT"] = os.path.join(self.rig.dir, "missing.jsonl")
        lines = self.next(token_of(self.next()[0]))
        t1 = token_of(lines[-1])
        self.assertEqual(brain.put(self.rig.dir, "ab12cd-1", "1", json.dumps(user(sector=7).data)), 1)
        self.assertEqual(brain.put(self.rig.dir, t1, "2", json.dumps(user(sector=7).data)), 1)   # no such call
        self.assertEqual(brain.put(self.rig.dir, t1, "1", json.dumps(user(sector=99).data)), 0)
        self.next(t1)
        self.assertEqual(self.world().me["sector"], 99)


class F5AnUnknownPriceIsNotFree(unittest.TestCase):
    def hungry(self, spent=0.0, money=2_000_000, bank=50_000_000, caps=None):
        rig = Rig()
        rig.world["control"]["spend_caps"] = caps or {}
        rig.tick(user(money=money, bank=bank))
        rig.world["records"]["spend"] = {"day": utc_day(rig.t), "ryo": float(spent)}
        return rig, rig.tick(user(curChakra=10, money=money, bank=bank))

    def test_at_the_daily_cap_a_ramen_of_unknown_price_is_asked_not_bought(self):
        rig, out = self.hungry(spent=C.DAILY_CAP)
        self.assertNotIn("village.buyFood", rig.calls(out))
        self.assertEqual(len(rig.world["decisions"]), 1)

    def test_with_no_allowance_nothing_is_bought(self):
        rig, out = self.hungry(caps={"daily": 0})
        self.assertNotIn("village.buyFood", rig.calls(out))

    def test_the_daily_cap_at_its_edge(self):
        rig, out = self.hungry(spent=C.DAILY_CAP - 2_000_000)               # the pocket just fits
        self.assertIn("village.buyFood", rig.calls(out))
        rig, out = self.hungry(spent=C.DAILY_CAP - 2_000_000 + 1)
        self.assertNotIn("village.buyFood", rig.calls(out))

    def test_the_reserve_at_its_edge(self):
        rig, out = self.hungry(bank=C.RESERVE)                              # the whole pocket may go
        self.assertIn("village.buyFood", rig.calls(out))
        rig, out = self.hungry(bank=C.RESERVE - 1)
        self.assertNotIn("village.buyFood", rig.calls(out))
        self.assertIn("reserve", rig.world["decisions"][0]["text"])

    def test_a_price_once_measured_is_the_price_checked(self):
        rig, out = self.hungry(spent=C.DAILY_CAP - 2_000_000)
        bought = res("village.buyFood", {"success": True}, {"ramen": "large"})
        rig.tick(bought, user(money=2_000_000 - 1_500, bank=50_000_000))
        self.assertEqual(rig.world.own("recovery")["ramen_cost"], 1_500)
        step = K.ramen(rig.world.own("recovery")["ramen_cost"])
        self.assertTrue(rig.brain.gates.check(step, rig.world, "recovery").ok)   # 1,500 fits where the pocket did not
        rig.world["records"]["spend"]["ryo"] = float(C.DAILY_CAP - 1_499)
        self.assertEqual(rig.brain.gates.check(step, rig.world, "recovery").kind, "ask")

    def test_with_no_profile_read_yet_the_gate_asks(self):
        rig = Rig()
        self.assertEqual(rig.brain.gates.check(K.ramen(), rig.world, "recovery").kind, "ask")


class F6AHoldPastMidnight(unittest.TestCase):
    def held(self, line, when):
        rig = Rig()
        with open(rig.dna, "a", encoding="utf8") as f:
            f.write(line + "\n")
        now = dt.datetime.fromisoformat(when + "+00:00").timestamp()
        return {n for n in gates.do_not_attack(rig.dna, now)[0] if n in ("luka", "4qua")}

    def test_before_during_and_after_midnight(self):
        line = "- 2026-11-11 23:50-00:20 UTC: Luka and 4qua. Leave them be."
        self.assertEqual(self.held(line, "2026-11-11T23:40:00"), {"luka", "4qua"})   # before: already left alone
        self.assertEqual(self.held(line, "2026-11-11T23:55:00"), {"luka", "4qua"})   # was: free to attack
        self.assertEqual(self.held(line, "2026-11-12T00:10:00"), {"luka", "4qua"})
        self.assertEqual(self.held(line, "2026-11-12T00:21:00"), set())

    def test_a_hold_within_one_day_still_closes_on_time(self):
        line = "- 2026-11-11 16:22-16:52 UTC: Luka and 4qua. Leave them be."
        self.assertEqual(self.held(line, "2026-11-11T16:30:00"), {"luka", "4qua"})
        self.assertEqual(self.held(line, "2026-11-11T16:53:00"), set())

    def test_a_time_that_cannot_be_read_holds(self):
        line = "- 2026-11-11 23:50-24:20 UTC: Luka and 4qua. Leave them be."
        self.assertEqual(self.held(line, "2026-11-13T12:00:00"), {"luka", "4qua"})

    def test_a_hold_with_its_own_end_date_and_a_user_id(self):
        line = '- 2026-11-11 17:10 UTC to 2026-11-12 17:10 UTC: Slyrak (user_2enQ). Director: "24h."'
        rig = Rig()
        with open(rig.dna, "a", encoding="utf8") as f:
            f.write(line + "\n" + '- 2026-11-11 17:10 UTC to 2026-11-10 17:10 UTC: Backwards (user_back). Why.\n')
        at = lambda when: gates.do_not_attack(rig.dna, dt.datetime.fromisoformat(when + "+00:00").timestamp())[0]
        self.assertLessEqual({"slyrak", "user_2enq"}, at("2026-11-12T17:09:00"))
        self.assertEqual({"slyrak", "user_2enq"} & at("2026-11-12T17:11:00"), set())
        self.assertIn("backwards", at("2026-11-20T00:00:00"))             # ends before it starts: it holds

    def test_the_holds_in_the_repositorys_own_file_are_read(self):
        """state/player/dauntless/do_not_attack.md as committed: the director's 24 h hold of 2026-11-11."""
        inside = dt.datetime.fromisoformat("2026-11-12T12:00:00+00:00").timestamp()
        after = dt.datetime.fromisoformat("2026-11-12T17:11:00+00:00").timestamp()
        held = {"slyrak", "user_2enqypbkxmeuwyrrbbgqiqsp0gk"}
        self.assertLessEqual(held, gates.do_not_attack(None, inside)[0])
        self.assertEqual(held & gates.do_not_attack(None, after)[0], set())
        self.assertNotIn("utc", gates.do_not_attack(None, inside)[0])        # read as a hold, not as loose words

    def test_the_gate_refuses_the_attack_inside_the_hold(self):
        rig = Rig()
        with open(rig.dna, "a", encoding="utf8") as f:
            f.write("- 2026-11-11 23:50-00:20 UTC: Luka and 4qua. Leave them be.\n")
        rig.t = dt.datetime.fromisoformat("2026-11-11T23:55:00+00:00").timestamp()
        rig.tick(user())
        step = K.attack({"userId": "u_luka", "username": "Luka", "longitude": 1, "latitude": 1}, 1538)
        self.assertEqual(rig.brain.gates.check(step, rig.world, "pvp_hunt").rule, "do_not_attack")


class F7ATurnEndsAsTheEvidenceSays(unittest.TestCase):
    def fight(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        R = battle["battle.round"]
        state = rig.world["battle"]
        state["entries"] = [e for e in state["entries"] if not (e[1] == R and e[2] == C.ME)]
        return rig, battle, R, out

    def test_no_answer_and_no_line_of_mine_in_the_log_is_not_an_action(self):
        rig, battle, R, out = self.fight()
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.round": R + 1,
                              "battle.version": battle["battle.version"] + 3})   # the version moved on all the same
        rig.tick(battle_read("B1", his), dt=60)
        self.assertEqual(turns(rig)[-1]["outcome"], "unresolved")           # was acted: true
        self.assertEqual((rig.world["records"]["turns_missed"], rig.world["records"]["turns_unresolved"]), (0, 1))
        self.assertEqual(rig.status()["turns_unresolved"], 1)

    def test_a_jump_straight_to_my_next_round_still_closes_the_turn_before(self):
        rig, battle, R, out = self.fight()
        rig.tick(battle_read("B1", dict(battle, **{"battle.round": R + 1,
                                                   "battle.version": battle["battle.version"] + 5})), dt=70)
        self.assertEqual([(t["round"], t["outcome"]) for t in turns(rig)], [(R, "unresolved")])   # was: no row
        self.assertEqual(rig.world["battle"]["turn"]["round"], R + 1)

    def test_every_action_refused_and_the_turn_gone_is_a_missed_turn(self):
        rig, battle, R, out = self.fight()
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.round": R + 1})
        rig.tick(*answers(out, NOT_VALID), battle_read("B1", his))
        self.assertEqual(turns(rig)[-1]["outcome"], "missed")
        self.assertEqual(rig.world["records"]["turns_missed"], 1)

    def test_the_games_answer_or_the_log_is_an_action(self):
        rig, battle, R, out = self.fight()
        his = dict(battle, **{"battle.activeUserId": FOE})
        rig.tick(*answers(out), battle_read("B1", his))
        self.assertEqual((turns(rig)[-1]["outcome"], turns(rig)[-1]["accepted"]), ("acted", 2))
        rig, battle, R, out = self.fight()                                  # no answer this time, but the log has it
        rig.tick(battle_read("B1", his), my_line(R), dt=5)
        self.assertEqual((turns(rig)[-1]["outcome"], turns(rig)[-1]["accepted"]), ("acted", 0))

    def test_a_log_read_that_came_back_empty_proves_nothing(self):
        rig, battle, R, out = self.fight()
        his = dict(battle, **{"battle.activeUserId": FOE})
        rig.tick(battle_read("B1", his), log_read("B1", {k: [] for k in K.ENT}))
        self.assertEqual(turns(rig)[-1]["outcome"], "unresolved")

    def test_a_fight_that_ends_on_my_turn_with_no_proof_is_unresolved_not_acted(self):
        rig, battle, R, out = self.fight()
        gone(rig)
        self.assertEqual(turns(rig)[-1]["outcome"], "unresolved")

    def test_a_relay_lost_with_the_plan_in_hand_is_unresolved_until_a_read_settles_it(self):
        rig, battle, R, out = self.fight()
        rig.t += 30
        out = rig.tick()                                                    # a new relay: nothing to hand in
        self.assertEqual(acts(out), [])                                     # look before sending again
        moved = dict(battle, **{"battle.activeUserId": FOE, "battle.version": battle["battle.version"] + 2})
        rig.tick(battle_read("B1", moved), my_line(R))
        self.assertEqual(turns(rig)[-1]["outcome"], "acted")                # the log shows it landed


class F9AnEventIsWhatHappened(unittest.TestCase):
    def test_a_purchase_the_gates_stopped_is_not_reported_as_bought(self):
        rig = Rig()
        rig.tick(user())
        rig.world["records"]["spend"] = {"day": utc_day(rig.t), "ryo": float(C.DAILY_CAP) + 1}
        out = rig.tick(user(curChakra=10))
        self.assertNotIn("village.buyFood", rig.calls(out))
        self.assertEqual(rig.events("item"), [])                            # was: "ramen bought"
        self.assertEqual(len(rig.events("decision_raised")), 1)

    def test_a_potion_is_reported_when_the_game_confirms_it_and_only_then(self):
        rig = Rig()
        rig.tick(user())
        out = rig.tick(user(hp=3000))
        self.assertEqual(rig.calls(out), ["item.consume", "profile.getUser"])
        self.assertEqual(rig.events("item"), [])                            # planned and sent: not yet used
        used = res("item.consume", {"success": True}, out["steps"][0]["input"])
        rig.tick(used, user())
        self.assertEqual([(e["text"], e["why"]) for e in rig.events("item")], [("Full Potion used", "HP at 59%")])

    def test_a_call_that_failed_or_that_the_game_refused_is_not_a_use(self):
        for answer in (res("item.consume", None, {}, error="Error calling item.consume: boom"),
                       res("item.consume", {"success": False, "message": "You do not own this item"}, {})):
            rig = Rig()
            rig.tick(user())
            rig.tick(user(hp=3000))
            rig.tick(answer, user(hp=3000))
            self.assertEqual(rig.events("item"), [])
        self.assertEqual([e["about"] for e in rig.events("finding")], ["recovery"])   # the game's no is on record

    def test_the_potion_at_the_fights_end_is_reported_from_its_answer(self):
        rig = Rig()
        start_fight(rig)
        out = gone(rig)
        self.assertEqual((rig.calls(out)[0], rig.events("item")), ("item.consume", []))
        rig.tick(res("item.consume", {"success": True}, out["steps"][0]["input"]), user())
        self.assertEqual([e["text"] for e in rig.events("item")], ["Full Potion used"])


class F10TheOpeningArchive(unittest.TestCase):
    def rows(self, rig, bid="B1"):
        with gzip.open(os.path.join(rig.combat.fights, "live_states", f"{bid}.full.jsonl.gz"), "rt") as f:
            return [json.loads(line) for line in f]

    def test_the_first_row_has_the_seat(self):
        rig = Rig()
        battle, ents, _ = start_fight(rig, effects=[{"type": "x", "targetId": C.ME}])
        first = self.rows(rig)[0]
        self.assertEqual((first["seat"], rig.world["battle"]["seat"]), (2, 2))   # was None

    def test_the_seat_is_told_from_a_first_read_on_his_turn_too(self):
        rig = Rig()
        battle, ents = fixture()
        his = dict(battle, **{"battle.activeUserId": FOE})                  # his turn, and nothing of mine this round
        start_fight(rig, battle=his, ents=ents)
        self.assertEqual(self.rows(rig)[0]["seat"], 2)
        rig = Rig()
        mine = {k: [x] + ents[k] for k, x in zip(K.ENT, ("e_mine", battle["battle.round"], C.ME, "kunai_id", ["hit"]))}
        start_fight(rig, battle=his, ents=mine)                             # his turn, after mine: I move first
        self.assertEqual(self.rows(rig)[0]["seat"], 1)

    def test_the_ground_is_kept_as_the_game_sent_it(self):
        rig = Rig()
        battle, ents = fixture()
        whole = [{"id": "g1", "type": "barrier", "creatorId": FOE, "longitude": 5, "latitude": 4, "curHealth": 100,
                  "a_key_no_planner_reads": 1}]
        start_fight(rig, battle=dict(battle, **{"battle.groundEffects": whole}), ents=ents)
        first = self.rows(rig)[0]
        self.assertEqual((first["ground"], first["ground_read"]), (whole, "whole"))   # was the planner's short form
        self.assertNotIn("a_key_no_planner_reads", json.dumps(rig.world["battle"]["ground"]))

    def test_a_ground_that_was_not_asked_for_is_not_an_empty_one(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)                                # the opening read asks for no ground
        first = self.rows(rig)[0]
        self.assertEqual((first["ground"], first["ground_read"]), (None, "not asked"))
        R, v = battle["battle.round"], battle["battle.version"]
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.version": v + 2, "battle.usersEffects": []})
        out = rig.tick(battle_read("B1", his))                              # this one came with the effect list
        self.assertTrue(any(k.startswith("battle.groundEffects") for k in out["steps"][0]["select"]))
        cols = {"battle.groundEffects.*.type": ["fire"], "battle.groundEffects.*.creatorId": [FOE],
                "battle.groundEffects.*.longitude": [5], "battle.groundEffects.*.latitude": [4],
                "battle.groundEffects.*.power": [10], "battle.groundEffects.*.rounds": [2],
                "battle.groundEffects.*.createdRound": [R]}
        rig.tick(battle_read("B1", dict(battle, **{"battle.round": R + 1, "battle.version": v + 4,
                                                   "battle.usersEffects": [], **cols})))
        rig.tick(battle_read("B1", dict(his, **{"battle.round": R + 1, "battle.version": v + 6})))
        got = {(r["round"], r["turn"]): (r["ground"], r["ground_read"]) for r in self.rows(rig)}
        self.assertEqual(got[(R + 1, "me")], (cols, "columns"))
        self.assertEqual(got[(R + 1, "him")], ([], "none on the field"))


class F11HandingAResultInIsSafe(unittest.TestCase):
    RESULTS = ('{"message":"You don\'t have that item"}', '{"a":"say \\"hi\\"","b":"$(touch pwned) `id` \\\\ $HOME"}',
               '{\n  "success": true,\n  "message": "two\\nlines"\n}')

    def test_the_relays_put_command_carries_any_result_text(self):
        rig = Rig()
        rig.world.save()
        env = dict(os.environ, TNR_PLAYER_LIVE=rig.dir, TNR_PLAYER_NO_DAEMON="1", PYTHONPATH=C.ROOT,
                   TNR_TRANSCRIPT=os.path.join(rig.dir, "missing.jsonl"),
                   TNR_PLAYER_FIGHTS=os.path.join(rig.dir, "fights"))
        for text in self.RESULTS:
            relay.write(os.path.join(rig.dir, "client.json"),
                        {"protocol": relay.PROTOCOL, "relay": "ab12cd", "seq": 4, "token": "ab12cd-4",
                         "calls": [["item.consume", {"x": 1}]]})
            line = json.loads(relay.lines([K.potion("x")], token="ab12cd-4", echo=True)[1])["put"]
            # what player/RELAY.md tells the relay to run: the line, the heredoc mark, the result, the mark
            command = f"{line} <<'TNR_RESULT'\n{text}\nTNR_RESULT"
            done = subprocess.run(["bash", "-c", command], env=env, cwd=rig.dir, capture_output=True, text=True)
            self.assertEqual((done.returncode, done.stderr), (0, ""), text)
            row = relay.read(os.path.join(rig.dir, "inbox", "put-ab12cd-4-001.json"))
            self.assertEqual((row[0], row[2]), ("item.consume", json.loads(text)), text)
            os.unlink(os.path.join(rig.dir, "inbox", "put-ab12cd-4-001.json"))
        self.assertFalse(os.path.exists(os.path.join(rig.dir, "pwned")))

    def test_the_prompt_says_how_and_in_what_order(self):
        with open(os.path.join(C.ROOT, "player", "RELAY.md"), encoding="utf8") as f:
            text = f.read()
        for must in ("<<'TNR_RESULT'", "one line at a time", "wait for each line's result", "unchanged"):
            self.assertIn(must, text)
        self.assertNotIn("put N 'RESULT'", text)                            # the quoted form the review broke


if __name__ == "__main__":
    unittest.main()
