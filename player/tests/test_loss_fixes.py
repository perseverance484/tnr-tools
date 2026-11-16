"""Fixes from AP run 2's two losses (2026-11-16, fight 6 vs Shisui, fight 8 vs Selaphiel): the planner's own record.

Nothing kept what a turn's plan was or why, so the losses had to be rebuilt from the archived states and planned again
offline. Every planner run now leaves one line in fights/live_states/<battle>.plans.jsonl.gz (which planner, how
long, the bans, its summary and what it fired), and the fight's keep pushes it with the log.
Socket-free: no game call, no connector call; the planner process is a stand-in.
"""
import gzip
import json
import os
import subprocess
import tempfile
import unittest
from unittest import mock

from player import calls as K, config as C, keep
from player.combat import Combat
from player.tests.support import Rig, fixture, user

OUT = """R3 v14 | MY TURN | he acted first this round
me 3880 HP AP 80 (STUNNED -20) | him Selaphiel 3651 HP | dist 2 | his base turn 1005
his clock: ready on his turn: Danse Macabre
kunai: close race (1.02) -> cost 0
planner2: 12 legal bundles in 0.10s. TOP 2:
1.  -1612  clear@5,4 -> kims@4,6  [swing -222 mine 717 his 1794]
2.  -1945  replace@3,5 -> kims@3,5 -> shield@3,5  [swing +150 mine 450 his 2245]
FIRE: [{"actionId": "clear", "longitude": 5, "latitude": 4, "name": "clear"}]
"""


def rows_of(ents):
    return [[ents[k][i] for k in K.ENT] for i in range(len(ents["*.battleRound"]))]


def records(fights, bid):
    with gzip.open(os.path.join(fights, "live_states", f"{bid}.plans.jsonl.gz"), "rt") as f:
        return [json.loads(line) for line in f]


class PlanRecord(unittest.TestCase):
    def test_every_planner_run_leaves_its_choice_and_candidates(self):
        combat = Combat(tempfile.mkdtemp(), spawn=False)
        battle, ents = fixture("anbu_r3.txt")
        with mock.patch("player.combat.subprocess.run",
                        side_effect=lambda argv, **kw: subprocess.CompletedProcess(argv, 0, OUT, "")):
            plan, how = combat.plan_turn("B1", battle, rows_of(ents), "ANBU Member", ban=["qNeccb2eF20oL0Ws-VhKS"])
        self.assertEqual(plan[0]["actionId"], "clear")
        rec = records(combat.fights, "B1")
        self.assertEqual(len(rec), 1)
        r = rec[0]
        self.assertEqual((r["round"], r["version"], r["script"], r["how"]),
                         (battle["battle.round"], battle["battle.version"], "planner2.py", how))
        self.assertEqual(r["ban"], ["qNeccb2eF20oL0Ws-VhKS"])
        self.assertTrue(r["out"][0].startswith("R3 v14"))
        self.assertIn("kunai: close race (1.02) -> cost 0", r["out"])
        self.assertTrue(any(x.startswith("1.  -1612  clear") for x in r["out"]))
        self.assertTrue(r["out"][-1].startswith("FIRE: "))
        self.assertFalse(any(x.startswith("his clock") for x in r["out"]))   # the long lines stay out

    def test_a_failed_run_is_recorded_too(self):
        combat = Combat(tempfile.mkdtemp(), spawn=False)
        battle, ents = fixture("anbu_r3.txt")
        with mock.patch("player.combat.subprocess.run",
                        side_effect=lambda argv, **kw: subprocess.CompletedProcess(argv, 1, "", "boom")):
            plan, how = combat.plan_turn("B2", battle, rows_of(ents), "ANBU Member")
        self.assertIsNone(plan)
        rec = records(combat.fights, "B2")
        self.assertEqual((rec[-1]["script"], rec[-1]["how"]), (None, how))
        self.assertIn("planner failed", how)

    def test_a_record_that_cannot_be_written_never_costs_the_turn(self):
        combat = Combat(tempfile.mkdtemp(), spawn=False)
        battle, ents = fixture("anbu_r3.txt")
        with mock.patch("player.combat.subprocess.run",
                        side_effect=lambda argv, **kw: subprocess.CompletedProcess(argv, 0, OUT, "")), \
                mock.patch("player.combat.gzip.open", side_effect=OSError("disk full")):
            plan, _ = combat.plan_turn("B3", battle, rows_of(ents), "ANBU Member")
        self.assertEqual(plan[0]["actionId"], "clear")

    def test_the_fight_keep_pushes_the_record_with_the_log(self):
        fights = tempfile.mkdtemp()
        os.makedirs(os.path.join(fights, "live_states"))
        for name in ("B4_entries.json", os.path.join("live_states", "B4.plans.jsonl.gz")):
            with open(os.path.join(fights, name), "w") as f:
                f.write("x")
        names = [os.path.relpath(p, fights) for p in keep.fight_files("B4", fights)]
        self.assertIn(os.path.join("live_states", "B4.plans.jsonl.gz"), names)


class RamenAfterEveryFight(unittest.TestCase):
    """Director 2026-11-16: "Repair, heal and large ramen after every fight"; "The brain can use Ramen, sure."
    Ramen refills chakra and stamina only; before, it was bought only under 50%, so run 2 never bought one."""

    def end_fight(self, rig, result="won", hp=5050):
        rig.world["records"]["fight_end"] = {"bid": "B1", "result": result, "hp": hp, "max": 5050, "at": rig.t}
        return rig.brain.reg.activities["recovery"].after_fight(rig.world)

    def test_a_large_ramen_after_a_fight_that_left_the_pools_down(self):
        rig = Rig()
        out = rig.tick(user(curChakra=79))
        self.assertNotIn("village.buyFood", rig.calls(out))            # 79% and no fight: nothing (floor is 50%)
        self.assertEqual(self.end_fight(rig), [])                       # full HP: no potion in the closing batch
        out = rig.tick(user(curChakra=79))
        self.assertEqual((out["activity"], rig.calls(out)), ("recovery", ["village.buyFood", "profile.getUser"]))
        self.assertEqual(out["steps"][0]["input"], {"ramen": "large"})
        out = rig.tick(user(curChakra=79))
        self.assertNotIn("village.buyFood", rig.calls(out))            # one ramen per fight, not a loop

    def test_no_ramen_when_the_pools_are_full_enough(self):
        rig = Rig()
        self.end_fight(rig)
        out = rig.tick(user(curStamina=96))
        self.assertNotIn("village.buyFood", rig.calls(out))
        self.assertNotIn("ramen_due", rig.world.own("recovery"))

    def test_after_a_loss_the_hospital_first_then_the_ramen(self):
        rig = Rig()
        self.end_fight(rig, result="lost", hp=0)
        out = rig.tick(user("HOSPITALIZED", hp=1, curChakra=40, curStamina=60))
        self.assertEqual(rig.calls(out), ["hospital.npcHeal", "profile.getUser"])
        out = rig.tick(user(curChakra=60, curStamina=90))
        self.assertEqual(rig.calls(out), ["village.buyFood", "profile.getUser"])
        self.assertEqual(C.POOLS_AFTER_FIGHT, 0.95)


if __name__ == "__main__":
    unittest.main()
