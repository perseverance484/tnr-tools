#!/usr/bin/env python3
"""Selftest for check_draft.py: the committed draft passes; each hard check fails closed.

    python3 harness/crafting_caches/selftest.py
"""
import copy
import os
import socket
import sys
import tempfile
import unittest


def _no_network(*_a, **_k):
    raise AssertionError("selftest attempted a network connection")


socket.socket = _no_network  # type: ignore[misc,assignment]
socket.create_connection = _no_network  # type: ignore[assignment]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_draft as C  # noqa: E402

DRAFT, CENSUS = C.load(C.DRAFT, C.CENSUS)
CENSUS_NAMES = {k: v["name"] for k, v in C.index(CENSUS).items()}


def line(d, name):
    return next(ln for c in d["caches"] for ln in c["lines"] if ln["name"] == name)


class Draft(unittest.TestCase):
    def expect(self, mutate, needle):
        d = copy.deepcopy(DRAFT)
        mutate(d)
        errs = C.check(d, CENSUS)
        self.assertTrue(any(needle in e for e in errs), (needle, errs))

    def test_committed_draft_is_clean(self):
        self.assertEqual(C.check(DRAFT, CENSUS), [])

    def test_report_is_current(self):
        self.assertEqual(C.main(["--check"]), 0)

    def test_quantity_outside_ruled_set(self):
        self.expect(lambda d: line(d, "Cracked Auditory Core").update(quantity=7), "not in the ruled set")

    def test_common_factor_without_policy(self):
        def m(d):
            d.pop("quantity_policy")
            line(d, "Cracked Auditory Core").update(quantity=5)
        self.expect(m, "shares a factor")

    def test_unknown_id(self):
        self.expect(lambda d: line(d, "Iron Ore").update(id="nope"), "not in census")

    def test_name_mismatch(self):
        self.expect(lambda d: line(d, "Iron Ore").update(name="Iron Ingot"), "census name")

    def test_excluded_item(self):
        def m(d):
            hid = next(k for k, v in d["exclusions"]["ids"].items() if v == "Heart of Kaeruun")
            d["caches"][1]["lines"].append({"id": hid, "name": "Heart of Kaeruun", "quantity": 1, "chance": 1, "band": "rare"})
        self.expect(m, "exclusion list")

    def test_event_item(self):
        def m(d):
            uid = next(i["id"] for i in CENSUS["items"] if i["name"] == "Unobtanium")
            d["exclusions"]["ids"].pop(uid)
            d["caches"][1]["lines"].append({"id": uid, "name": "Unobtanium", "quantity": 1, "chance": 1, "band": "rare"})
        self.expect(m, "event item")

    def test_hidden_item(self):
        def m(d):
            h = next(i for i in CENSUS["items"] if i["hidden"])
            d["caches"][0]["lines"].append({"id": h["id"], "name": h["name"], "quantity": 1, "chance": 1, "band": "rare"})
        self.expect(m, "hidden")

    def test_bad_chance_and_quantity(self):
        self.expect(lambda d: line(d, "Iron Ore").update(chance=0), "chance 0")
        self.expect(lambda d: line(d, "Glimmer Dust").update(quantity=100000), "stackSize")

    def test_target_ingredient_not_supplied(self):
        def m(d):
            d["caches"][0]["lines"] = [ln for ln in d["caches"][0]["lines"] if ln["name"] != "Glimmer Dust"]
        self.expect(m, "Glimmer Dust is not supplied")

    def test_cache_carries_off_target_item(self):
        def m(d):
            ore = next(g for g in CENSUS["ingredients"] if g["name"] == "Silver Ore")
            d["caches"][0]["lines"].append({"id": ore["id"], "name": "Silver Ore", "quantity": 3, "chance": 5, "band": "rare"})
        self.expect(m, "carries Silver Ore, which no target uses")

    def test_target_must_be_player_craftable(self):
        def m(d):
            h = next(i for i in CENSUS["items"] if not i["craftable_by_players_at_pin"])
            d["caches"][2]["targets"].append({"id": h["id"], "name": h["name"]})
        self.expect(m, "not a player-craftable census recipe")

    def test_pill_pack_expands_to_reagents(self):
        recipes = {i["id"]: i for i in CENSUS["items"] if i["craftable_by_players_at_pin"]}
        pack = next(i for i in recipes.values() if i["name"] == "Pill Pack")
        carried = {ln["id"] for ln in DRAFT["caches"][0]["lines"]}
        need = {CENSUS_NAMES[k]: v for k, v in C.raw_demand(pack["id"], recipes, carried).items()}
        self.assertEqual(need, {"Galecrest Sage": 9, "Glimmer Dust": 4, "Mosswolf Tuft": 4,
                                "Moonlight Antlers": 10, "Sunroot": 10})

    def test_wrong_census(self):
        self.expect(lambda d: d["census"].update(capture_sha256="0" * 64), "different census")

    def test_stale_report_detected(self):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "r.md")
            open(p, "w").write("old\n")
            self.assertEqual(C.main(["--check", "--report", p]), 1)


class Compare(unittest.TestCase):
    def test_known_chests_and_metrics(self):
        import compare_chests as K
        bundle = os.path.join(C.REPO, "harvests", "inbox", "tnr_results_1790826836406.json")
        found, problems, missing, _ = K.chests_from_bundles([bundle])
        self.assertEqual(sorted(v["row"]["name"] for v in found.values()), ["Mystery Chest", "Ornate Chest"])
        self.assertEqual(problems, [])
        self.assertEqual(len(missing), 20)
        ornate = next(v for v in found.values() if v["row"]["name"] == "Ornate Chest")
        m = K.metrics(ornate["effect"]["reward_items"], K.catalog())
        self.assertAlmostEqual(m["expected_units"], 14.01, places=2)
        self.assertAlmostEqual(m["expected_lines_hit"], 2.51, places=2)
        self.assertEqual(m["guaranteed_lines"], 0)

    def test_draft_metrics_use_chance_and_quantity(self):
        import compare_chests as K
        inro = next(c for c in DRAFT["caches"] if c["name"] == "Medicine Inro")
        expect = sum(ln["quantity"] * ln["chance"] / 100 for ln in inro["lines"])
        self.assertAlmostEqual(K.metrics(inro["lines"], K.catalog())["expected_units"], expect)

    def test_push95_baseline(self):
        import compare_chests as K
        bundle = os.path.join(C.REPO, "harvests", "inbox", "tnr_results_1791863274945.json")
        if not os.path.exists(bundle):
            self.skipTest("push/95 results not present")
        found, problems, missing, not_chests = K.chests_from_bundles([bundle])
        self.assertEqual((len(found), problems, missing, len(not_chests)), (20, [], [], 2))
        text = K.render(found, [], K.catalog(), problems, missing, {"x"}, not_chests)
        self.assertIn("`[PILL_PACK_ID]` — malformed placeholder", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
