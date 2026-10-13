#!/usr/bin/env python3
"""Socket-free selftest for build_census.py.

    python3 harness/crafting_recipe_census/selftest.py

Uses fixtures/raw_complete.json (written by make_fixture.mjs from the real console script against
the in-process fake server) and mutates copies of it to prove each coverage check fails closed.
"""
import copy
import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest


def _no_network(*_a, **_k):
    raise AssertionError("selftest attempted a network connection")


socket.socket = _no_network  # type: ignore[misc,assignment]
socket.create_connection = _no_network  # type: ignore[assignment]

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_census as B  # noqa: E402

FIXTURE = os.path.join(HERE, "fixtures", "raw_complete.json")
RAW_BYTES = open(FIXTURE, "rb").read()
RAW = json.loads(RAW_BYTES)


def run(raw):
    return B.build(raw, json.dumps(raw).encode(), "mutated.json")


def item(doc, iid):
    return next(i for i in doc["items"] if i["id"] == iid)


class Clean(unittest.TestCase):
    def setUp(self):
        self.verdict, self.doc = B.build(RAW, RAW_BYTES, "raw_complete.json")

    def test_complete_and_counts(self):
        self.assertEqual(self.verdict, "COMPLETE", self.doc["incomplete_reasons"])
        t = self.doc["totals"]
        self.assertEqual((t["craftable_items"], t["visible"], t["hidden"]), (11, 8, 3))
        self.assertEqual(t["requirement_rows"], 16)
        self.assertEqual(t["distinct_ingredients"], 6)
        self.assertEqual(self.doc["coverage"]["requests"]["by_procedure"],
                         {"item.getAll": 10, "item.getItemWithCraftingRequirements": 11})

    def test_pagination_coverage(self):
        p = self.doc["coverage"]["passes"]
        self.assertEqual([g["rows"] for g in p["hidden=false"]["pages"]], [3, 3, 2])
        self.assertEqual([g["rows"] for g in p["hidden=true"]["pages"]], [3, 0])
        self.assertTrue(all(v["terminated_on_null_cursor"] for v in p.values()))
        self.assertEqual(self.doc["coverage"]["list_filter"]["minCost"], -2147483648)

    def test_flags(self):
        d = self.doc
        self.assertEqual(item(d, "c-empty")["flags"], ["EMPTY_RECIPE"])
        self.assertIn("MISSING_INGREDIENT", item(d, "c-ghost")["flags"])
        self.assertIn("EVOLUTION_ITEM", item(d, "c-evo")["blocked"])
        self.assertIn("DUPLICATE_INGREDIENT", item(d, "h-dup")["flags"])
        self.assertIn("SELF_INGREDIENT", item(d, "h-self")["flags"])
        self.assertIn("HIDDEN_INGREDIENT", item(d, "h-crown")["flags"])
        self.assertIn("INGREDIENT_ACQUISITION_UNKNOWN", item(d, "h-crown")["flags"])
        self.assertNotIn("INGREDIENT_ACQUISITION_UNKNOWN", item(d, "c-blade")["flags"])
        self.assertEqual(item(d, "c-blade")["flags"], [])
        self.assertTrue(item(d, "c-blade")["craftable_by_players_at_pin"])
        self.assertFalse(item(d, "h-crown")["craftable_by_players_at_pin"])
        ghost = [i for i in item(d, "c-ghost")["ingredients"] if i["missing"]]
        self.assertEqual([(g["id"], g["name"], g["quantity"]) for g in ghost], [("deleted-item", None, 2)])

    def test_restrictions(self):
        d = self.doc
        crown = item(d, "h-crown")
        self.assertEqual(crown["craft"]["min_crafting_rank"], "FORGEMASTER")
        self.assertEqual(crown["use_restrictions"]["requiredBloodline"], {"id": "bl-1", "name": "Storm Blood"})
        self.assertEqual(item(d, "c-tonic")["craft"]["craft_minutes_per_unit"], {"static": 10})
        self.assertEqual(item(d, "h-dup")["craft"]["min_crafting_rank"], "MASTER")
        self.assertEqual(item(d, "c-stew")["craft"]["output_bucket"], "cooking")

    def test_ingredient_index(self):
        ore = next(i for i in self.doc["ingredients"] if i["id"] == "ing-ore")
        self.assertEqual(ore["recipe_count"], 5)
        self.assertEqual(ore["total_units_across_recipes"], 4 + 1 + 5 + 7 + 1)
        self.assertTrue(ore["canBeGathered"])
        thread = next(i for i in self.doc["ingredients"] if i["id"] == "ing-thread")
        self.assertTrue(thread["is_also_craftable_output"])

    def test_render_is_deterministic(self):
        self.assertEqual(B.render(self.doc), B.render(B.build(RAW, RAW_BYTES, "raw_complete.json")[1]))


class FailsClosed(unittest.TestCase):
    def expect(self, mutate, needle):
        raw = copy.deepcopy(RAW)
        mutate(raw)
        verdict, doc = run(raw)
        self.assertEqual(verdict, "INCOMPLETE")
        self.assertTrue(any(needle in r for r in doc["incomplete_reasons"]),
                        (needle, doc["incomplete_reasons"]))

    def test_halted_capture(self):
        self.expect(lambda r: r.update(status="halted", phase="details"), "capture status")

    def test_wrong_pin(self):
        self.expect(lambda r: r.update(sourcePin="studie-tech/TheNinjaRPG@deadbeef"), "sourcePin")

    def test_terminal_page_missing(self):
        def m(r):
            r["lists"]["main"]["hidden=false"]["pages"].pop()
        self.expect(m, "last page nextCursor")

    def test_cursor_gap(self):
        def m(r):
            del r["lists"]["main"]["hidden=false"]["pages"][1]
        self.expect(m, "has cursor")

    def test_unfinished_pass(self):
        def m(r):
            r["lists"]["confirm"]["hidden=true"]["done"] = False
        self.expect(m, "pass not finished")

    def test_row_outside_filter(self):
        def m(r):
            r["lists"]["main"]["hidden=true"]["pages"][0]["rows"][0]["hidden"] = False
        self.expect(m, "fails the filter")

    def test_duplicate_across_pages(self):
        def m(r):
            pages = r["lists"]["main"]["hidden=false"]["pages"]
            pages[1]["rows"][0] = copy.deepcopy(pages[0]["rows"][2])
        self.expect(m, "more than one page")

    def test_snapshot_drift(self):
        def m(r):
            r["lists"]["confirm"]["hidden=false"]["pages"][0]["rows"][0]["updatedAt"] = "changed"
        self.expect(m, "snapshot drift")

    def test_missing_detail(self):
        def m(r):
            del r["details"]["c-blade"]
        self.expect(m, "no detail read for c-blade")

    def test_not_found_detail(self):
        def m(r):
            r["details"]["c-blade"] = {"status": "not_found", "message": "NOT_FOUND 404"}
        self.expect(m, "detail c-blade: not_found")

    def test_detail_differs_from_list(self):
        def m(r):
            r["details"]["c-blade"]["data"]["rarity"] = "EPIC"
        self.expect(m, "differs from its list row")

    def test_foreign_procedure_logged(self):
        def m(r):
            r["requestLog"].append({"proc": "item.update", "outcome": "ok"})
        self.expect(m, "non-census procedures")


class Cli(unittest.TestCase):
    def test_write_check_and_refusal(self):
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "craftable_recipes.json")
            self.assertEqual(B.main([FIXTURE, "--out", out]), 0)
            self.assertEqual(B.main([FIXTURE, "--out", out, "--check"]), 0)
            with open(out, "a") as f:
                f.write(" ")
            self.assertEqual(B.main([FIXTURE, "--out", out, "--check"]), 1)

            bad = copy.deepcopy(RAW)
            bad["status"] = "halted"
            badp = os.path.join(td, "halted.json")
            json.dump(bad, open(badp, "w"))
            out2 = os.path.join(td, "x.json")
            self.assertEqual(B.main([badp, "--out", out2]), 2)
            self.assertFalse(os.path.exists(out2))
            self.assertEqual(B.main([badp, "--out", out2, "--allow-incomplete"]), 2)
            self.assertEqual(json.load(open(out2))["verdict"], "INCOMPLETE")


class FixtureProvenance(unittest.TestCase):
    def test_fixture_reproduces_from_console_script(self):
        try:
            r = subprocess.run(["node", os.path.join(HERE, "make_fixture.mjs"), "--check"],
                               capture_output=True, text=True)
        except FileNotFoundError:
            self.skipTest("node not installed")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
