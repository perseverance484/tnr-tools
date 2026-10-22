#!/usr/bin/env python3
"""validate.py checks added with the TheNinjaRPG@107d7a8 re-pin (RUL-2026-10-22-005).

    python3 -m unittest scripts/test_validate_107d7a8.py

- generated 45d bounds on top-level numbers (requiredLevel .max(MAX_PLAYER_LEVEL) = 110);
- law 8's quest caps read from 45d (maxLevel 110; maxAttempts/maxCompletes stay 100);
- the Elite Jonin milestone superRefine (validators/objectives.ts QuestValidator).

Runs validate.py as the skill runs it (cwd skill data/), on throwaway manifests. No network.
"""
import copy
import json
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "skills", "building-tnr-content", "data")
VALIDATE = os.path.join(ROOT, "skills", "building-tnr-content", "scripts", "validate.py")

MILESTONE = {
    "entity": "quest", "slot": "create", "name": "Milestone 101",
    "data": {
        "name": "Milestone 101", "hidden": True, "questType": "starter", "requiredLevel": 100,
        "maxLevel": 100, "maxCompletes": 1, "consecutiveObjectives": True,
        "content": {"rewardMode": "all", "objectives": [{"task": "dialog", "id": "o1"}],
                    "reward": {"reward_level": 101, "reward_stats": 20000}},
    },
}


def run(items):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump({"items": items}, fh)
        path = fh.name
    try:
        out = subprocess.run(["python3", VALIDATE, path], cwd=DATA, capture_output=True, text=True)
        return out.stdout + out.stderr
    finally:
        os.unlink(path)


def milestone_lines(text):
    return [line for line in text.splitlines() if "milestone" in line or "reward_level" in line
            or "reward_stats" in line]


def variant(mutate, slot="create"):
    entry = copy.deepcopy(MILESTONE)
    entry["slot"] = slot
    if slot == "edit":
        entry["targetId"] = "q" * 21
    mutate(entry["data"])
    return entry


class Bounds(unittest.TestCase):
    def test_required_level_cap_is_110(self):
        ok = {"entity": "jutsu", "slot": "edit", "name": "J", "targetId": "j" * 21,
              "data": {"requiredLevel": 110, "injectableInBattle": False}}
        bad = copy.deepcopy(ok)
        bad["data"]["requiredLevel"] = 111
        self.assertNotIn("requiredLevel", run([ok]))
        self.assertIn("requiredLevel=111 is above the validator's max 110 (MAX_PLAYER_LEVEL)", run([bad]))

    def test_quest_max_level_110_is_legal_but_max_completes_stays_100(self):
        q = {"entity": "quest", "slot": "edit", "name": "Q", "targetId": "q" * 21,
             "data": {"maxLevel": 110, "maxCompletes": 100}}
        self.assertNotIn("law 8", run([q]))
        q["data"]["maxCompletes"] = 101
        self.assertIn("law 8: maxCompletes=101 exceeds the cap of 100", run([q]))


class Milestone(unittest.TestCase):
    def test_valid_milestone_has_no_milestone_findings(self):
        self.assertEqual(milestone_lines(run([MILESTONE])), [])

    def test_each_broken_rule_is_refused(self):
        cases = {
            "questType='mission'": lambda d: d.update(questType="mission"),
            "teamEnabled=True": lambda d: d.update(teamEnabled=True),
            "requiredLevel=99 must be 100": lambda d: d.update(requiredLevel=99),
            "maxLevel=101 must be 100": lambda d: d.update(maxLevel=101),
            "maxCompletes=2 must be 1": lambda d: d.update(maxCompletes=2),
            "retryDelay='1d'": lambda d: d.update(retryDelay="1d"),
            "rewardMode='pick'": lambda d: d["content"].update(rewardMode="pick"),
            "objectives[0].reward_rank='JONIN'": lambda d: d["content"]["objectives"][0].update(reward_rank="JONIN"),
            "reward_stats must be positive": lambda d: d["content"]["reward"].pop("reward_stats"),
            "reward_level=100 must be an integer 101-110": lambda d: d["content"]["reward"].update(reward_level=100),
        }
        for expect, mutate in cases.items():
            with self.subTest(expect):
                self.assertTrue(any(expect in line for line in milestone_lines(run([variant(mutate)]))), expect)

    def test_stats_without_level_and_level_on_objective_are_refused(self):
        stats_only = variant(lambda d: d["content"]["reward"].pop("reward_level"))
        self.assertIn("reward_stats needs a reward_level", run([stats_only]))
        on_obj = variant(lambda d: d["content"]["objectives"][0].update(reward_level=101))
        self.assertIn("belong on content.reward, not on an objective", run([on_obj]))

    def test_edit_without_the_gating_fields_warns_instead_of_erroring(self):
        def strip(d):
            for k in ("questType", "requiredLevel", "maxLevel", "maxCompletes"):
                d.pop(k)
        lines = milestone_lines(run([variant(strip, slot="edit")]))
        self.assertTrue(lines)
        self.assertTrue(all(line.startswith("warn") for line in lines), lines)


if __name__ == "__main__":
    unittest.main()
