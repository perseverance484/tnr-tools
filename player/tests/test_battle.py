"""The battle activity: the pilot's loop, rule for rule, and the same batches as the pilot on logged states."""
import importlib
import json
import os
import sys
import tempfile
import unittest

from player import config as C
from player.combat import Combat
from player.tests.support import (FOE, LINE, Rig, battle_read, fixture, limited, log_read, res, start_fight, user)


def seq(steps, hold=0.0):
    """A batch as comparable rows: waits and calls (endpoint, input, select)."""
    rows = [("wait", round(hold, 1))] if hold else []
    for s in steps:
        if "wait" in s:
            rows.append(("wait", s["wait"]))
        else:
            rows.append((s["call"], json.dumps(s["input"], sort_keys=True), tuple(s["select"])))
    return rows


def pilot_seq(battle, entries=None, kit_known=False):
    """The batch the pilot prints for the same read (its tick line dropped)."""
    live = tempfile.mkdtemp(prefix="pilot-live-")
    os.environ["TNR_PILOT_LIVE"] = live
    if C.TOOLS not in sys.path:
        sys.path.insert(0, C.TOOLS)
    import pilot
    importlib.reload(pilot)
    pilot.kit_known = lambda user_id: kit_known
    real = pilot.subprocess.Popen
    # the pilot starts fight_bases.py beside the fight (start_new_session): not from a test
    pilot.subprocess.Popen = lambda *a, **k: None if k.get("start_new_session") else real(*a, **k)
    try:
        head, batch = pilot.battle_tick({}, "PARITY", dict(battle), entries)
    finally:
        pilot.subprocess.Popen = real
        os.environ.pop("TNR_PILOT_LIVE")
        importlib.reload(pilot)
    rows = []
    for b in batch:
        if "call" in b:
            rows.append((b["call"], json.dumps(b["input"], sort_keys=True), tuple(b["select"])))
        elif "time.sleep(" in b["bash"]:
            rows.append(("wait", float(b["bash"].split("time.sleep(")[1].split(")")[0])))
    return head, rows


class SameAsThePilot(unittest.TestCase):
    def brain_seq(self, battle, ents, combat=None):
        rig = Rig(combat=combat)
        rig.tick(user("BATTLE", bid="PARITY"))
        out = rig.tick(battle_read("PARITY", battle), log_read("PARITY", ents))
        return out["note"], seq(out["steps"], out["hold"]), rig

    def test_my_turn_with_the_real_planner(self):
        battle, ents = fixture()
        battle["battle.usersEffects"] = []
        head, want = pilot_seq(dict(battle), dict(ents))
        note, got, rig = self.brain_seq(dict(battle), ents, Combat(tempfile.mkdtemp(), spawn=False))
        self.assertIn("MY TURN", head)
        self.assertEqual(got, want)
        self.assertEqual([r[0] for r in got if r[0] != "wait"][-3:],
                         ["combat.getBattle", "combat.getBattleEntries", "jutsu.getPublicUserJutsus"])
        self.assertIn(("wait", C.ACTION_GAP), got)                     # 1.2 s between the actions of the turn

    def test_his_turn(self):
        battle, ents = fixture()
        battle.update({"battle.activeUserId": FOE, "battle.usersEffects": []})
        head, want = pilot_seq(dict(battle), dict(ents))
        note, got, _ = self.brain_seq(dict(battle), ents)
        self.assertIn("his turn", note)
        self.assertEqual(got, want)

    def test_an_ai_turn_is_nudged(self):
        battle, ents = fixture()
        users = battle["battle.usersState.*.userId"]
        battle.update({"battle.activeUserId": FOE, "battle.usersEffects": [],
                       "battle.usersState.*.isAi": [u == FOE for u in users]})
        head, want = pilot_seq(dict(battle), dict(ents))
        note, got, _ = self.brain_seq(dict(battle), ents)
        self.assertIn("AI turn", note)
        self.assertEqual(got, want)
        self.assertEqual(got[0][0], "combat.performAction")


class Turns(unittest.TestCase):
    def test_a_fight_opens_with_one_full_read_and_the_whole_log(self):
        rig = Rig()
        out = rig.tick(user("BATTLE", bid="B1"))
        self.assertEqual(out["activity"], "battle")
        self.assertEqual([s["input"] for s in out["steps"]], [{"battleId": "B1"}, {"battleId": "B1", "limit": 200}])
        self.assertIn("battle.usersEffects", out["steps"][0]["select"])
        self.assertEqual([e["battle"] for e in rig.events("fight_start")], ["B1"])

    def test_my_turn_fires_the_plan_then_polls_with_the_full_state(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        v = battle["battle.version"]
        acts = [s for s in out["steps"] if s.get("call") == "combat.performAction"]
        self.assertEqual([(a["input"]["actionId"], a["input"]["version"]) for a in acts],
                         [("stormblade_id", v), ("kunai_id", v + 1)])
        kinds = ["wait" if "wait" in s else s["call"] for s in out["steps"]]
        self.assertEqual(kinds, ["combat.performAction", "wait", "combat.performAction", "combat.getBattle",
                                 "combat.getBattleEntries", "jutsu.getPublicUserJutsus"])
        self.assertEqual(out["steps"][1]["wait"], C.ACTION_GAP)
        self.assertIn("battle.usersEffects", out["steps"][3]["select"])    # the poll carries the exact state
        self.assertEqual(out["hold"], 0)                                   # my turn never waits
        self.assertTrue(rig.combat.plan_args[-1]["live"])                  # and it was planned on the live state
        self.assertAlmostEqual(rig.combat.plan_args[-1]["seconds"], C.BEST_LINE_AT, places=3)

    def test_his_kit_is_read_until_it_saves(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        battle = dict(battle, **{"battle.activeUserId": FOE})
        asked = [rig.calls(out).count("jutsu.getPublicUserJutsus")]
        for _ in range(3):
            out = rig.tick(battle_read("B1", battle))
            asked.append(rig.calls(out).count("jutsu.getPublicUserJutsus"))
        self.assertEqual(asked, [1, 1, 1, 0])                              # three tries, then none
        rig2 = Rig()
        battle, ents, out = start_fight(rig2)
        out = rig2.tick(battle_read("B1", dict(battle, **{"battle.activeUserId": FOE})),
                        res("jutsu.getPublicUserJutsus", {"*.jutsuId": []}, {"userId": FOE}))
        self.assertEqual(rig2.combat.saved, [FOE])
        self.assertNotIn("jutsu.getPublicUserJutsus", rig2.calls(out))     # saved: not read again

    def test_his_turn_is_polled_less_often_the_longer_it_lasts(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        his = dict(battle, **{"battle.activeUserId": FOE})
        holds = [rig.tick(battle_read("B1", his))["hold"] for _ in range(5)]
        self.assertEqual(holds, [3.0, 4.0, 5.0, 6.0, 6.0])
        moved = dict(his, **{"battle.version": his["battle.version"] + 1})
        self.assertEqual(rig.tick(battle_read("B1", moved))["hold"], 3.0)  # he acted: back to the short gap

    def test_a_refused_action_is_banned_and_the_lobby_bans_nothing(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        bad = res("combat.performAction", {"notification": "Action not valid anymore"},
                  {"battleId": "B1", "actionId": "stormblade_id"})
        out = rig.tick(bad, battle_read("B1", battle))
        self.assertEqual(rig.combat.plan_args[-1]["ban"], ["stormblade_id"])
        self.assertEqual([s["input"]["actionId"] for s in out["steps"] if s.get("call") == "combat.performAction"],
                         ["kunai_id"])
        lobby = res("combat.performAction", {"notification": "Battle has not started yet"},
                    {"battleId": "B1", "actionId": "kunai_id"})
        rig.tick(lobby, battle_read("B1", battle))
        self.assertEqual(rig.combat.plan_args[-1]["ban"], [])

    def test_a_plan_that_did_not_move_the_battle_is_not_sent_again(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        rig.tick(battle_read("B1", battle))                                # same version: the plan did not land
        self.assertEqual(rig.combat.plan_args[-1]["ban"], ["stormblade_id"])

    def test_no_line_means_defensive_stance_never_nothing(self):
        rig = Rig()
        rig.combat.line = None
        battle, ents, out = start_fight(rig)
        acts = [s["input"]["actionId"] for s in out["steps"] if s.get("call") == "combat.performAction"]
        self.assertEqual(acts, ["defensiveStance"])
        self.assertEqual([e["about"] for e in rig.events("finding")], ["planner"])

    def test_director_mode_waits_once_from_the_start_of_the_turn_then_covers(self):
        rig = Rig()
        rig.world["control"]["director_mode"] = True
        battle, ents = fixture()
        rig.tick(user("BATTLE", bid="B1"))
        out = rig.tick(battle_read("B1", battle), log_read("B1", ents))    # no live state yet: read it first
        self.assertIn("reading the live state", out["note"])
        live = dict(battle, **{"battle.usersEffects": []})
        out = rig.tick(battle_read("B1", live))
        self.assertIn("director's move", out["note"])
        self.assertNotIn("combat.performAction", rig.calls(out))
        self.assertEqual(out["hold"], 5.0)
        out = rig.tick(battle_read("B1", live), dt=30)                     # he acts mid-turn: the clock does not restart
        self.assertIn("director's move", out["note"])
        out = rig.tick(battle_read("B1", live), dt=10)                     # 41 s into the turn: the player covers it
        self.assertIn("combat.performAction", rig.calls(out))
        self.assertEqual(rig.world["battle"]["pilot_rounds"], [battle["battle.round"]])
        self.assertGreaterEqual(rig.combat.plan_args[-1]["seconds"], 3.0)


class Refusals(unittest.TestCase):
    def test_a_read_refused_on_my_turn_is_not_waited_for(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        rig.world["battle"]["turn"]["fired_at"] = None                     # the actions never went (all refused)
        rig.world["battle"]["sent_plan"] = None
        out = rig.tick(limited("combat.getBattle", {"battleId": "B1"}))
        self.assertIn("last good read", out["note"])
        self.assertEqual(out["steps"][0]["call"], "combat.performAction")  # actions first, then the read
        self.assertEqual(out["hold"], 0)

    def test_an_action_the_connector_refused_is_sent_again_not_banned(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        out = rig.tick(limited("combat.performAction", {"battleId": "B1", "actionId": "stormblade_id"}),
                       limited("combat.getBattle", {"battleId": "B1"}))
        acts = [s["input"]["actionId"] for s in out["steps"] if s.get("call") == "combat.performAction"]
        self.assertEqual(acts, ["stormblade_id", "kunai_id"])
        self.assertEqual(rig.combat.plan_args[-1]["ban"], [])

    def test_when_an_action_landed_the_stale_read_is_not_planned_on(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        out = rig.tick(res("combat.performAction", {}, {"battleId": "B1", "actionId": "stormblade_id"}),
                       limited("combat.getBattle", {"battleId": "B1"}))
        self.assertEqual(rig.calls(out), ["combat.getBattle", "combat.getBattleEntries"])
        self.assertEqual(out["hold"], 0)

    def test_a_read_that_comes_back_empty_is_retried_plainer_before_the_fight_is_called_over(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        notes = []
        for _ in range(4):
            out = rig.tick(battle_read("B1", {}))
            notes.append(out["note"])
        self.assertIn("full read refused, plain read", notes[0])
        self.assertTrue(any("BATTLE OVER" in n for n in notes))
        rig2 = Rig()
        rig2.tick(user("BATTLE", bid="B2"))
        out = rig2.tick(battle_read("B2", {}))                             # the very first read came back empty
        self.assertIn("full read refused", out["note"])
        self.assertTrue(rig2.world.in_battle())


class Columns(unittest.TestCase):
    """Lists are read as columns, and the connector drops a missing key from its column instead of padding it. So
    every column read checks its lengths, and a read that does not line up is never used."""

    def test_a_fighter_column_that_came_back_short_is_read_again_not_guessed(self):
        rig = Rig()
        battle, ents = fixture()
        rig.tick(user("BATTLE", bid="B1"))
        short = dict(battle, **{"battle.usersState.*.curHealth": [4943.4]})
        out = rig.tick(battle_read("B1", short), log_read("B1", ents))
        self.assertNotIn("combat.performAction", rig.calls(out))
        self.assertEqual(rig.calls(out), ["combat.getBattle", "combat.getBattleEntries"])
        self.assertEqual([e["about"] for e in rig.events("finding")], ["selects"])

    def test_a_log_whose_columns_do_not_line_up_is_dropped(self):
        rig = Rig()
        battle, ents = fixture()
        rig.tick(user("BATTLE", bid="B1"))
        bad = dict(ents, **{"*.actionId": ents["*.actionId"][:-1]})
        rig.tick(battle_read("B1", dict(battle, **{"battle.usersEffects": []})), log_read("B1", bad))
        self.assertEqual(rig.world["battle"]["entries"], [])
        self.assertIn("selects", [e["about"] for e in rig.events("finding")])

    def test_one_ai_flag_per_fighter_or_none_is_trusted(self):
        rig = Rig()
        battle, ents = fixture()
        rig.tick(user("BATTLE", bid="B1"))
        odd = dict(battle, **{"battle.usersState.*.isAi": [True], "battle.activeUserId": FOE,
                              "battle.usersEffects": []})
        out = rig.tick(battle_read("B1", odd), log_read("B1", ents))
        self.assertIn("his turn", out["note"])                             # not nudged as an AI on a short column


class EndOfFight(unittest.TestCase):
    def closed(self, rig, hurt=True):
        battle, ents, out = start_fight(rig)
        if not hurt:
            users = battle["battle.usersState.*.userId"]
            hp = [5050 if u == C.ME else 100 for u in users]
            rig.tick(battle_read("B1", dict(battle, **{"battle.usersState.*.curHealth": hp,
                                                       "battle.version": battle["battle.version"] + 2})))
        return rig.tick(battle_read("B1", {"battle.version": None}), dt=1)

    def gone(self, rig):
        """Empty reads until the fight is called over."""
        for _ in range(5):
            out = rig.tick(battle_read("B1", {}))
            if "BATTLE OVER" in out["note"]:
                return out
        raise AssertionError("the fight never closed")

    def test_the_full_potion_goes_in_the_same_batch_as_the_fights_end(self):
        rig = Rig()
        start_fight(rig)                                                   # I am at 2,757 of 5,050
        out = self.gone(rig)
        self.assertEqual(rig.calls(out), ["item.consume", "profile.getUser"])
        self.assertEqual(out["hold"], 0)
        self.assertFalse(rig.world.in_battle())

    def test_no_potion_at_full_health_or_after_a_loss(self):
        rig = Rig()
        battle, ents, _ = start_fight(rig)
        users = battle["battle.usersState.*.userId"]
        full = dict(battle, **{"battle.usersState.*.curHealth": [5050 if u == C.ME else 0 for u in users]})
        out = rig.tick(battle_read("B1", full))
        self.assertIn("BATTLE OVER (won)", out["note"])
        self.assertEqual(rig.calls(out), ["profile.getUser"])
        rig = Rig()
        battle, ents, _ = start_fight(rig)
        dead = dict(battle, **{"battle.usersState.*.curHealth": [0 if u == C.ME else 3000 for u in users]})
        out = rig.tick(battle_read("B1", dead))
        self.assertIn("BATTLE OVER (lost)", out["note"])
        self.assertEqual(rig.calls(out), ["profile.getUser"])
        self.assertGreater(rig.world["opponents"]["lost_to"][FOE], rig.t)
        self.assertEqual(rig.events("fight_end")[-1]["result"], "lost")

    def test_the_result_is_the_logs_hp_count_not_the_status_alone(self):
        rig = Rig()
        start_fight(rig)
        rig.combat.lost_by_log = True
        self.gone(rig)
        self.assertEqual(rig.events("fight_end"), [])                      # not known yet
        rig.tick(user("AWAKE"))                                            # awake, but the log says I died
        end = rig.events("fight_end")[-1]
        self.assertEqual((end["result"], end["opponent"]), ("lost", "AngelSaber"))
        self.assertTrue(end["turning_point"])
        self.assertEqual(rig.world["records"]["results"][-1][:2], ["B1", "lost"])
        rig = Rig()
        start_fight(rig)
        self.gone(rig)
        rig.tick(user("AWAKE"))
        self.assertEqual(rig.events("fight_end")[-1]["result"], "won")
        rig = Rig()
        start_fight(rig)
        self.gone(rig)
        rig.tick(user("HOSPITALIZED"))
        self.assertEqual(rig.events("fight_end")[-1]["result"], "lost")

    def test_the_fight_is_kept_for_the_tools_that_learn_from_it(self):
        rig = Rig()
        battle, ents, _ = start_fight(rig, effects=[{"type": "increasedamagegiven", "rounds": 2, "targetId": C.ME}])
        self.gone(rig)
        fights = rig.combat.fights
        with open(os.path.join(fights, "B1_entries.json")) as f:
            self.assertEqual(len(json.load(f)["*.id"]), len(ents["*.id"]))
        self.assertTrue(os.path.exists(os.path.join(fights, "B1_meta.json")))
        with open(os.path.join(fights, "live_states", "B1.json")) as f:
            self.assertIn(str(battle["battle.round"]), json.load(f))
        self.assertIn("opponents.py", " ".join(" ".join(a) for a in rig.combat.spawned))
        self.assertIn("postmortem.py", " ".join(" ".join(a) for a in rig.combat.spawned))
        self.assertIn("fight_bases.py", " ".join(" ".join(a) for a in rig.combat.spawned))

    def test_every_rounds_full_live_state_is_archived_as_the_game_sent_it(self):
        """Brief AP4 step 0, for AP1: nothing has to be captured again when the move atlas is built."""
        import gzip
        rig = Rig()
        effect = {"id": "fx1", "type": "increasedamagegiven", "rounds": 2, "targetId": C.ME, "power": 30,
                  "staticAssetPath": "x.png", "a_key_no_planner_reads": {"deep": [1, 2]}}
        battle, ents, _ = start_fight(rig, effects=[effect])                 # round 3, my turn
        R, v = battle["battle.round"], battle["battle.version"]
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.version": v + 2, "battle.usersEffects": [effect]})
        rig.tick(battle_read("B1", his))                                    # round 3, his turn
        rig.tick(battle_read("B1", dict(his, **{"battle.version": v + 3})))  # the same turn again: not kept twice
        rig.new_brain()                                                     # nor after a restart
        rig.tick(battle_read("B1", dict(his, **{"battle.version": v + 4})))
        nxt = dict(battle, **{"battle.round": R + 1, "battle.version": v + 6, "battle.usersEffects": []})
        rig.tick(battle_read("B1", nxt))                                    # round 4, my turn
        with gzip.open(os.path.join(rig.combat.fights, "live_states", "B1.full.jsonl.gz"), "rt") as f:
            rows = [json.loads(line) for line in f]
        self.assertEqual([(r["round"], r["turn"], r["version"]) for r in rows],
                         [(R, "me", v), (R, "him", v + 2), (R + 1, "me", v + 6)])
        self.assertEqual(rows[0]["effects"], [effect])                      # whole, not the planner's compact form
        self.assertEqual(rows[0]["fighters"]["battle.usersState.*.curHealth"], battle["battle.usersState.*.curHealth"])
        self.assertEqual(rows[2]["seat"], rig.world["battle"]["seat"])
        self.assertNotIn("a_key_no_planner_reads", json.dumps(rig.world["battle"]["live_hist"]))

    def test_a_turn_that_passes_without_an_action_of_mine_is_a_missed_turn(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        rig.world["battle"]["turn"]["fired_at"] = None
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.round": battle["battle.round"] + 1})
        rig.world["battle"]["entries"] = [e for e in rig.world["battle"]["entries"]
                                          if not (e[1] == battle["battle.round"] and e[2] == C.ME)]
        rig.tick(battle_read("B1", his))
        self.assertEqual(rig.world["records"]["turns_missed"], 1)
        self.assertEqual(len(rig.events("stall")), 1)

    def test_the_console_sees_the_fight(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        b = rig.status()["battle"]
        self.assertEqual((b["id"], b["opponent"], b["round"]), ("B1", "AngelSaber", battle["battle.round"]))
        self.assertEqual(b["pick"]["actions"], [a["name"] for a in LINE])
        self.assertIn(b["seat"], (1, 2))
        self.assertAlmostEqual(b["my_hp"], 2756.87, places=1)


if __name__ == "__main__":
    unittest.main()
