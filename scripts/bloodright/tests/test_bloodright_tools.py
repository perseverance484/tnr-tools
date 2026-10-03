#!/usr/bin/env python3
"""Fixture tests for the Bloodright planning tooling (socket-free, repo data only).

  python3 -m unittest scripts/bloodright/tests/test_bloodright_tools.py -v
"""
from __future__ import annotations

import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import bloodright_lib as L  # noqa: E402

REFERENCE = os.path.join(L.DESIGN_DIR, "examples", "taiyo_kami.json")
REFERENCE_VALIDATION = os.path.join(L.DESIGN_DIR, "examples", "taiyo_kami_validation.json")
TAIYO_ID = "6C2t3jK35hvPoVocLiHEl"


def taiyo_rows():
    snap = L.load_snapshot()
    roster = L.load_roster()
    kit = L.census_index(snap, roster)[TAIYO_ID]["kit"]
    return L.kit_rows(kit)


def mini_tree(nodes):
    return {"title": "t", "nodes": nodes, "examples": []}


def n(id_, cat, parents, tag="damage", flat=2, name=None):
    return {"id": id_, "name": name or f"Node {id_}".replace(id_, chr(64 + int(id_))), "category": cat, "cost": 1,
            "parents": parents, "modifiers": [{"tag": tag, "flat": flat}]}


class ReferenceReproduction(unittest.TestCase):
    def test_taiyo_kami_audit_matches_handoff(self):
        tree = L.load_json(REFERENCE)
        ref = L.load_json(REFERENCE_VALIDATION)
        rows = taiyo_rows()
        self.assertEqual(L.validate_structure(tree), [])
        a = L.audit_tree(tree, rows)
        self.assertEqual(a["available_skills"], ref["available_skills"])
        self.assertEqual(a["foundation_count"], ref["foundation_count"])
        self.assertEqual(a["hidden_art_count"], ref["hidden_art_count"])
        self.assertEqual(a["advanced_art_count"], ref["advanced_art_count"])
        self.assertEqual(a["maximum_advanced_arts"], ref["maximum_advanced_arts"])
        self.assertEqual(a["minimum_two_advanced_cost"], ref["minimum_two_advanced_cost"])
        self.assertEqual(a["legal_allocations_by_size"], ref["legal_allocations_by_size"])
        self.assertEqual(a["full_budget_allocations"], ref["full_budget_allocations"])
        self.assertEqual(a["non_dominated_full_allocations"], ref["non_dominated_full_allocations"])
        self.assertTrue(a["all_nodes_in_non_dominated_builds"])
        self.assertEqual(a["maximum_tag_bonuses"], ref["maximum_tag_bonuses"])

    def test_taiyo_kami_legal_builds_match_handoff(self):
        tree = L.load_json(REFERENCE)
        rows = taiyo_rows()
        a = L.audit_tree(tree, rows)
        mine = sorted(tuple(b["ids"]) for b in a["full_builds"])
        theirs = sorted(tuple(b["ids"]) for b in tree["legal_full_budget_builds"])
        self.assertEqual(mine, theirs)
        by = {tuple(b["ids"]): b["bonuses"] for b in a["full_builds"]}
        for b in tree["legal_full_budget_builds"]:
            want = {k: v for k, v in b["bonuses"].items() if v}
            self.assertEqual(by[tuple(b["ids"])], want)

    def test_taiyo_kami_example_finals_match(self):
        tree = L.load_json(REFERENCE)
        rows = taiyo_rows()
        for ex in tree["examples"]:
            mine = L.finals_for(ex["ids"], tree, rows)
            theirs = ex["finals"]
            self.assertEqual(len(mine), len(theirs))
            for m, t in zip(mine, theirs):
                self.assertEqual((m["jutsu"], m["row"], m["tag"]), (t["jutsu"], t["row"], t["tag"]))
                self.assertAlmostEqual(m["base"], t["base"])
                self.assertEqual(m["gain"], t["gain"])
                self.assertAlmostEqual(m["final"], t["final"])
                self.assertEqual(sorted(m["combat_elements"]), sorted(t["combat_elements"]))

    def test_taiyo_roles(self):
        rows = {(r.jutsu_name, r.row): r for r in taiyo_rows()}
        self.assertEqual(rows[("Solar Reverb", 1)].role, "ENEMY DEBUFF")  # Afterburn is an enemy debuff
        self.assertEqual(rows[("Stellar Inferno", 1)].role, "ENEMY DEBUFF")  # IDT on enemy
        self.assertEqual(rows[("Celestial Ignition", 0)].role, "SELF BUFF")
        self.assertEqual(rows[("Radiant Embers", 0)].role, "ENEMY DEBUFF")
        self.assertEqual(rows[("Solar Reverb", 0)].role, "DAMAGE")
        self.assertFalse(any(r.adverse for r in rows.values() if r.supported))


class Arithmetic(unittest.TestCase):
    def test_static_addition_and_cap(self):
        tree = mini_tree([n("1", "Foundation", [], "increasedamagegiven", 5, "Alpha")])
        r = L.Row("j", "J", "A", "BLOODLINE", "", 0, "increasedamagegiven", "x", "percentage", 35.0, 25, 0.4, 2,
                  [], ["None"], "INHERIT", "SELF", None, "self", "self", "SELF BUFF", False, None, None, "offence",
                  True, "public", None, "BOTH", False, False, 40, 7, "SINGLE", 0)
        f = L.finals_for(["1"], tree, [r])[0]
        self.assertEqual(f["final"], 40.0)
        r2 = copy.copy(r)
        r2.base = 98.0
        f2 = L.finals_for(["1"], tree, [r2])[0]
        self.assertEqual(f2["final"], 100.0)
        self.assertTrue(f2["capped_at_100"])
        r3 = copy.copy(r)
        r3.tag = "damage"; r3.calculation = "formula"; r3.base = 40.0
        tree2 = mini_tree([n("1", "Foundation", [], "damage", 5, "Alpha")])
        self.assertEqual(L.finals_for(["1"], tree2, [r3])[0]["final"], 45.0)

    def test_level_scaling(self):
        self.assertEqual(L.scaled_power({"power": 30, "powerPerLevel": 0.4}, 25), 40.0)
        self.assertEqual(L.scaled_power({"power": 25, "powerPerLevel": 0}, 25), 25.0)

    def test_element_fallback(self):
        self.assertEqual(L.effective_elements({"elements": []}), ["None"])
        self.assertEqual(L.effective_elements({}), ["None"])
        self.assertEqual(L.effective_elements({"elements": ["Scorch"]}), ["Scorch"])


class Structure(unittest.TestCase):
    def test_two_advanced_under_one_hidden_rejected(self):
        tree = mini_tree([n("1", "Foundation", [], name="Root"), n("2", "Hidden Art", ["1"], name="Mid"),
                          n("3", "Advanced Art", ["2"], name="Left"), n("4", "Advanced Art", ["2"], name="Right")])
        errs = L.validate_structure(tree)
        self.assertTrue(any("jointly affordable for 4" in e for e in errs), errs)

    def test_taiyo_shape_accepted(self):
        tree = mini_tree([n("1", "Foundation", [], name="Root"), n("2", "Hidden Art", ["1"], name="Mid"),
                          n("3", "Advanced Art", ["2"], name="Left"), n("4", "Hidden Art", ["1"], name="Mid Two"),
                          n("5", "Advanced Art", ["4"], name="Right")])
        self.assertEqual(L.validate_structure(tree), [])
        by = {x.id: x for x in L.parse_nodes(tree)}
        self.assertEqual(L.audit_tree(tree, [])["minimum_two_advanced_cost"], 5)

    def test_convergence_rejected(self):
        tree = mini_tree([n("1", "Foundation", [], name="Root"), n("2", "Foundation", [], name="Root Two"),
                          n("3", "Hidden Art", ["1", "2"], name="Join")])
        errs = L.validate_structure(tree)
        self.assertTrue(any("forks only" in e for e in errs), errs)

    def test_too_many_nodes_rejected(self):
        nodes = [n("1", "Foundation", [], name="Root")] + [n(str(i), "Hidden Art", ["1"], name=f"Branch {chr(64+i)}") for i in range(2, 12)]
        errs = L.validate_structure(mini_tree(nodes))
        self.assertTrue(any("ceiling" in e for e in errs), errs)

    def test_unsupported_tag_rejected(self):
        tree = mini_tree([n("1", "Foundation", [], "wound", 2, "Root")])
        errs = L.validate_structure(tree)
        self.assertTrue(any("not a supported potency tag" in e for e in errs), errs)

    def test_cycle_rejected(self):
        tree = mini_tree([n("1", "Hidden Art", ["2"], name="Loop A"), n("2", "Hidden Art", ["1"], name="Loop B")])
        errs = L.validate_structure(tree)
        self.assertTrue(errs)

    def test_depth_five_unreachable(self):
        tree = mini_tree([n("1", "Foundation", [], name="Root"), n("2", "Hidden Art", ["1"], name="Two"),
                          n("3", "Hidden Art", ["2"], name="Three"), n("4", "Hidden Art", ["3"], name="Four"),
                          n("5", "Advanced Art", ["4"], name="Five")])
        errs = L.validate_structure(tree)
        self.assertTrue(any("needs 5 BP" in e for e in errs), errs)

    def test_skill_number_in_name_rejected(self):
        tree = mini_tree([n("1", "Foundation", [], name="Skill 01")])
        errs = L.validate_structure(tree)
        self.assertTrue(any("digit" in e for e in errs), errs)


class Recipients(unittest.TestCase):
    def test_dai_kenja_self_idt_is_adverse(self):
        snap = L.load_snapshot(); roster = L.load_roster()
        idx = L.census_index(snap, roster)
        kit = next(v["kit"] for v in idx.values() if v["kit"]["bloodline"]["name"] == "Dai Kenja")
        rows = {(r.jutsu_name, r.row): r for r in L.kit_rows(kit)}
        r = rows[("Overloaded Impact", 2)]
        self.assertEqual(r.tag, "increasedamagetaken")
        self.assertEqual(r.recipient, "self")
        self.assertEqual(r.role, "SELF DEBUFF")
        self.assertTrue(r.adverse)
        self.assertEqual(rows[("Chakra Overload", 1)].role, "ENEMY DEBUFF")

    def test_ground_friendly_rows(self):
        snap = L.load_snapshot(); roster = L.load_roster()
        idx = L.census_index(snap, roster)
        kit = next(v["kit"] for v in idx.values() if v["kit"]["bloodline"]["name"] == "Nature's Blessing")
        rows = {(r.jutsu_name, r.row): r for r in L.kit_rows(kit)}
        self.assertEqual(rows[("Verdant Bastion", 0)].role, "SELF BUFF")   # heal SELF on GROUND
        self.assertEqual(rows[("Verdant Bastion", 1)].role, "SELF BUFF")   # increaseheal INHERIT ff FRIENDLY
        self.assertEqual(rows[("Nature's Fury", 1)].role, "ENEMY DEBUFF")  # IDT on OTHER_USER

    def test_classification_kinds(self):
        snap = L.load_snapshot(); roster = L.load_roster()
        idx = L.census_index(snap, roster)
        def audit(name):
            kit = next(v["kit"] for v in idx.values() if v["kit"]["bloodline"]["name"].strip() == name)
            return L.classification_audit(kit, L.kit_rows(kit), snap, roster)
        self.assertEqual(audit("Taiyo Kami")["proposed_label"], "Scorch")
        self.assertEqual(audit("Vaporia")["label_kind"], "element")
        self.assertTrue(audit("Vaporia")["element_exclusive_within_census"])
        self.assertEqual(audit("Primal Radiance")["label_kind"], "bloodline-keyed extension")  # basic Fire
        self.assertEqual(audit("Ancient Tailed Demon")["label_kind"], "bloodline-keyed extension")  # None only
        self.assertEqual(audit("Shiroi Youso")["label_kind"], "bloodline-keyed extension")  # multi-element
        self.assertEqual(len(audit("Ethereal Monarch")["injected_children"]), 1)


if __name__ == "__main__":
    unittest.main()
