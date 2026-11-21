"""merge_results.py refuses parts from different code, scenarios or pins.  python3 -m unittest this file."""
import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import merge_results  # noqa: E402

PART = {
    "invocation": {"script": "main.ts", "args": ["--only", "A"]}, "scenario": "scenarios/x.json", "scenarioSha256": "s",
    "harnessCode": "c", "enginePin": "p", "seeds": 10, "maxRounds": 120, "mode": "dungeon", "seedFormula": "f",
    "assumptions": ["a"], "sources": {"ai/x": "src"}, "builds": {"A": []}, "variants": [{"name": "A"}],
    "tracesFirstSeed": {"A/Floor 1": {}},
}


def part(name, **over):
    p = copy.deepcopy(PART)
    p["builds"] = {name: []}
    p["variants"] = [{"name": name}]
    p["tracesFirstSeed"] = {f"{name}/Floor 1": {}}
    p.update(over)
    return p


class MergeTest(unittest.TestCase):
    def test_merges_in_order_with_invocations_and_traces(self):
        m = merge_results.merge([part("A"), part("B")])
        self.assertEqual([v["name"] for v in m["variants"]], ["A", "B"])
        self.assertEqual(len(m["invocations"]), 2)
        self.assertEqual(set(m["tracesFirstSeed"]), {"A/Floor 1", "B/Floor 1"})

    def test_refuses_mismatches(self):
        for k, v in [("harnessCode", "other"), ("scenarioSha256", "other"), ("enginePin", "other"), ("seeds", 5), ("maxRounds", 40)]:
            with self.assertRaises(SystemExit, msg=k):
                merge_results.merge([part("A"), part("B", **{k: v})])

    def test_refuses_duplicate_variant(self):
        with self.assertRaises(SystemExit):
            merge_results.merge([part("A"), part("A")])

    def test_refuses_missing_code_hash(self):
        with self.assertRaises(SystemExit):
            merge_results.merge([part("A", harnessCode=None), part("B", harnessCode=None)])


if __name__ == "__main__":
    unittest.main()
