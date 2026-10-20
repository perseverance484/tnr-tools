#!/usr/bin/env python3
"""Tests for scripts/elementaldamage_census_ledger.py. Socket-free; the input bundle is the one
forge/test/census.test.mjs proves the shipped census code exports.

    python3 -m unittest scripts/test_elementaldamage_census_ledger.py -v
"""

from __future__ import annotations

import copy
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import elementaldamage_census_ledger as led  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "forge/test/fixtures/census/elementaldamage_bundle.json"


def load():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def ledger(bundle):
    return led.build_ledger(bundle, bundle_path="fixture.json", bundle_sha256="0" * 64)


def run_cli(bundle) -> tuple[int, Path]:
    d = Path(tempfile.mkdtemp())
    p = d / "b.json"
    p.write_text(json.dumps(bundle), encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        rc = led.main([str(p), "--out-dir", str(d / "out")])
    return rc, d / "out"


def point(bundle, item_id):
    return next(c for c in bundle["captures"] if c.get("phase") == "census" and c["input"]["id"] == item_id)


class Classify(unittest.TestCase):
    def cls(self, **e):
        return led.classify({"type": "elementaldamage", **e})[0]

    def test_none_is_stat_scaling_positive_not_missing(self):
        self.assertEqual(self.cls(calculation="formula", statTypes=["None"], generalTypes=["Highest"]), led.C_BOTH)

    def test_empty_and_absent_are_missing(self):
        self.assertEqual(self.cls(calculation="formula", statTypes=[], generalTypes=["Strength"]), led.C_MISS_STATS)
        self.assertEqual(self.cls(calculation="formula", statTypes=["Ninjutsu"]), led.C_MISS_GENS)
        self.assertEqual(self.cls(calculation="formula"), led.C_MISS_BOTH)
        self.assertEqual(self.cls(calculation="formula", statTypes=None, generalTypes=[]), led.C_MISS_BOTH)

    def test_non_formula_is_out_of_scope_whatever_its_selectors(self):
        self.assertEqual(self.cls(calculation="static"), led.C_NONFORMULA)
        self.assertEqual(self.cls(calculation="percentage", statTypes=[]), led.C_NONFORMULA)

    def test_ambiguous_shapes_are_never_guessed(self):
        self.assertEqual(self.cls(statTypes=["None"]), led.C_MALFORMED)  # calculation absent
        self.assertEqual(self.cls(calculation="formula", statTypes="Highest"), led.C_MALFORMED)
        self.assertEqual(self.cls(calculation="formula", generalTypes=[1]), led.C_MALFORMED)
        self.assertEqual(led.classify("elementaldamage")[0], led.C_MALFORMED)


class Ledger(unittest.TestCase):
    def test_fixture_ledger(self):
        L = ledger(load())
        self.assertEqual(L["status"], "COMPLETE")
        self.assertEqual(L["ledgerErrors"], [])
        self.assertEqual(L["counts"]["inventory"], {"hidden:false": 7, "hidden:true": 2, "total": 9})
        self.assertEqual(L["counts"]["dynamicWeapons"], 8)
        self.assertEqual(L["candidates"], ["fx-both-missing", "fx-missing-gens", "fx-missing-stats", "fx-two-tags"])
        self.assertEqual(L["controls"], ["fx-both-present", "fx-static"])
        self.assertEqual(L["manualReview"], ["fx-ambiguous"])
        self.assertEqual(L["alreadyStaged"], [led.STORMRENDER_ID])
        self.assertTrue(L["zeroMutation"]["ok"])

    def test_stormrender_is_classified_but_never_a_new_candidate(self):
        r = ledger(load())["records"][led.STORMRENDER_ID]
        self.assertEqual(r["classifications"], [led.C_MISS_BOTH, led.C_STORMRENDER])
        self.assertTrue(r["status"].startswith("ALREADY STAGED / PR #73"))
        self.assertEqual([o["type"] for o in r["otherEffects"]], ["increasedamagetaken"])

    def test_each_dynamic_tag_is_assessed_independently(self):
        r = ledger(load())["records"]["fx-two-tags"]
        self.assertEqual([(d["position"], d["classification"]) for d in r["elementaldamageEffects"]], [(0, led.C_BOTH), (1, led.C_MISS_BOTH)])

    def test_ordinary_damage_is_context_not_a_candidate(self):
        L = ledger(load())
        self.assertNotIn("fx-damage-only", L["records"])
        self.assertIn("fx-damage-only", [r["id"] for r in load()["census"]["rows"]], "it is in the inventory denominator")
        ctx = L["records"]["fx-both-present"]["otherEffects"]
        self.assertEqual(ctx, [{"position": 1, "type": "damage", "calculation": "formula", "power": 30, "statTypes": "present", "generalTypes": "present"}])

    def test_original_values_and_provenance_are_kept(self):
        b = load()
        r = ledger(b)["records"]["fx-both-missing"]
        d = r["elementaldamageEffects"][0]
        self.assertEqual(d["original"], point(b, "fx-both-missing")["data"]["effects"][0])
        self.assertIs(d["allowBloodlineDamageIncrease"], False)
        self.assertEqual(d["statTypes"], [])
        self.assertEqual(d["generalTypes"], "<absent>")
        self.assertTrue(r["hidden"])
        self.assertEqual(r["provenance"]["snapshotKey"], "fixture::census::2")
        self.assertEqual(len(r["provenance"]["bodySha256"]), 64)

    def test_stale_point_is_recapture_required_and_not_complete(self):
        b = load()
        c = point(b, "fx-missing-stats")
        c["data"]["updatedAt"] = "2026-10-05T00:00:00.000Z"
        c["accepted"], c["stale"] = False, True
        b["census"]["verdict"] = "STALE"
        L = ledger(b)
        self.assertEqual(L["stale"], ["fx-missing-stats"])
        self.assertEqual(L["records"]["fx-missing-stats"]["status"], "RECAPTURE REQUIRED")
        self.assertTrue(L["status"].startswith("NOT COMPLETE"))
        self.assertEqual(run_cli(b)[0], 1)

    def test_a_missing_point_is_a_hard_failure(self):
        b = load()
        b["captures"] = [c for c in b["captures"] if c["input"]["id"] != "fx-static"]
        L = ledger(b)
        self.assertEqual(L["missing"], ["fx-static"])
        self.assertTrue(L["status"].startswith("NOT COMPLETE"))

    def test_an_unpersisted_body_is_failed_even_if_the_bundle_says_accepted(self):
        b = load()
        c = point(b, "fx-both-present")
        del c["data"]
        c["persistOk"], c["persistError"] = False, "gone"
        L = ledger(b)
        self.assertEqual(L["failed"], ["fx-both-present"])
        self.assertTrue(any("bundle says accepted=True" in e for e in L["ledgerErrors"]))

    def test_the_bundles_own_counts_and_targets_are_rechecked(self):
        b = load()
        b["census"]["counts"]["hidden:true"] = 5
        b["census"]["targets"] = b["census"]["targets"][1:]
        errs = ledger(b)["ledgerErrors"]
        self.assertTrue(any("census.counts[hidden:true]" in e for e in errs))
        self.assertTrue(any("census.targets is not exactly" in e for e in errs))

    def test_a_projection_row_carrying_extra_fields_is_flagged(self):
        b = load()
        b["census"]["rows"][0]["userId"] = "someone"
        self.assertTrue(any("non-projection fields" in e for e in ledger(b)["ledgerErrors"]))

    def test_a_bundle_that_wrote_anything_is_not_a_census_ledger(self):
        b = load()
        b["entries"] = [{"name": "x"}]
        L = ledger(b)
        self.assertFalse(L["zeroMutation"]["ok"])
        self.assertNotEqual(L["status"], "COMPLETE")

    def test_an_unstable_inventory_without_rows_is_refused(self):
        b = load()
        b["census"]["rows"] = None
        b["census"]["inventory"] = b["census"]["verdict"] = "UNSTABLE"
        self.assertEqual(run_cli(b)[0], 2)
        self.assertEqual(run_cli({"captures": []})[0], 2)

    def test_output_is_deterministic(self):
        b = load()
        rc1, o1 = run_cli(b)
        rc2, o2 = run_cli(b)
        self.assertEqual(rc1, 0)
        for name in ("b.ledger.json", "b.ledger.md"):
            a, c = (o1 / name).read_text(), (o2 / name).read_text()
            self.assertEqual(a.replace(str(o1.parent), ""), c.replace(str(o2.parent), ""))


if __name__ == "__main__":
    unittest.main()
