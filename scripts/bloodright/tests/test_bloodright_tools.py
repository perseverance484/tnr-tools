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
        # basic elements are ordinary element classifications now; sharing is expected
        self.assertEqual(audit("Primal Radiance")["label_kind"], "element")
        self.assertEqual(audit("Primal Radiance")["qualifying_elements"], ["Fire"])
        self.assertEqual(audit("Ancient Tailed Demon")["classification_status"], "requires classification extension")
        self.assertEqual(audit("Ancient Tailed Demon")["qualifying_elements"], [])
        self.assertEqual(audit("Godstorm Eclipse")["classification_status"], "multi-element: director review")
        self.assertEqual(audit("Godstorm Eclipse")["qualifying_elements"], ["Shadow", "Storm"])
        self.assertEqual(len(audit("Ethereal Monarch")["injected_children"]), 1)
        bee = audit("Blood-Enchanted Eyes")
        self.assertEqual(bee["qualifying_elements"], ["Shadow"])
        self.assertTrue(bee["shared_element_bloodlines"])  # other Shadow bloodlines: expected, not a blocker
        self.assertNotIn("census_collisions_on_signature_elements", bee)

    def test_jutsu_elements_mirror_check_jutsu_elements(self):
        self.assertEqual(L.jutsu_elements({"effects": [{"elements": ["Shadow"]}, {"elements": None}, {}]}), ["Shadow"])
        self.assertEqual(L.jutsu_elements({"effects": [{"elements": []}, {}]}), ["None"])
        self.assertEqual(L.jutsu_elements({"effects": [{"elements": ["Wind", "Fire"]}, {"elements": ["Fire"]}]}), ["Fire", "Wind"])


class RendererJutsuLabels(unittest.TestCase):
    """Coverage-line labels must never collapse two jutsu to one word or echo the classification."""

    def test_short_labels_when_unique_and_distinct_from_classification(self):
        import render_tree as R
        tree = {"classification": {"potency_classification": "Scorch", "display_element": None},
                "nodes": [{"coverage": {"jutsu": ["Incandescent Nova", "Solar Reverb"]}}],
                "examples": [{"finals": [{"jutsu": "Stellar Inferno"}]}]}
        self.assertEqual(R.jutsu_labels(tree), {"Incandescent Nova": "Nova", "Solar Reverb": "Reverb", "Stellar Inferno": "Inferno"})

    def test_full_names_when_short_labels_collide_or_match_classification(self):
        import render_tree as R
        tree = {"classification": {"potency_classification": "Storm", "display_element": "Storm"},
                "nodes": [{"coverage": {"jutsu": ["Demons Strike", "Reapers Storm"], "effect_rows": 2}}],
                "examples": [{"finals": [{"jutsu": "Death\u2019s Storm"}, {"jutsu": "Stormsinger"}]}]}
        labels = R.jutsu_labels(tree)
        self.assertEqual(labels["Reapers Storm"], "Reapers Storm")
        self.assertEqual(labels["Death\u2019s Storm"], "Death\u2019s Storm")
        self.assertEqual(labels["Demons Strike"], "Demons Strike")  # whole kit falls back together
        self.assertEqual(R.coverage_line(tree["nodes"][0], labels), "Demons Strike · Reapers Storm")

    def test_classification_echo_alone_forces_full_names(self):
        import render_tree as R
        tree = {"classification": {"potency_classification": "Wood"},
                "nodes": [{"coverage": {"jutsu": ["Iron Wood", "Verdant Bastion"]}}], "examples": []}
        self.assertEqual(R.jutsu_labels(tree), {"Iron Wood": "Iron Wood", "Verdant Bastion": "Verdant Bastion"})


class RendererAdverseRows(unittest.TestCase):
    """Adverse rows must be printed by their real recipient, not by the modifier's display role."""

    def _node(self):
        return {"id": "09", "name": "Cracked Vessel", "category": "Hidden Art", "cost": 1, "parents": ["06"],
                "modifiers": [{"tag": "increasedamagetaken", "flat": 2, "display_role": "ENEMY DEBUFF",
                               "row_roles": ["ENEMY DEBUFF", "SELF DEBUFF"]}],
                "coverage": {"jutsu": ["Chakra Overload", "Overloaded Impact"], "effect_rows": 2,
                             "adverse_rows": ["Overloaded Impact#2"]}}

    def _tree(self):
        finals = [{"jutsu": "Overloaded Impact", "row": 2, "tag": "increasedamagetaken", "recipient": "self",
                   "role": "SELF DEBUFF", "adverse": True},
                  {"jutsu": "Chakra Overload", "row": 1, "tag": "increasedamagetaken", "recipient": "enemy",
                   "role": "ENEMY DEBUFF", "adverse": False}]
        return {"classification": {"potency_classification": "Dai Kenja"}, "nodes": [self._node()],
                "examples": [{"finals": finals}]}

    def test_adverse_line_names_the_self_row_in_the_self_debuff_colour(self):
        import render_tree as R
        tree = self._tree()
        labels = R.jutsu_labels(tree)
        lines = R.adverse_lines(tree["nodes"][0], labels, R.finals_index(tree))
        self.assertEqual(lines, [("Impact: self debuff (adverse)", L.ROLE_COLORS["SELF DEBUFF"])])
        self.assertNotEqual(lines[0][1], L.ROLE_COLORS["ENEMY DEBUFF"])
        # the card grows by one line so the prerequisite block never overlaps
        self.assertEqual(R.card_height(tree["nodes"][0], 515, labels, R.finals_index(tree)) - R.card_height(self._node_without_adverse(), 515, labels), 30)

    def _node_without_adverse(self):
        n = self._node()
        n["coverage"] = {"jutsu": n["coverage"]["jutsu"], "effect_rows": 2}
        return n

    def test_no_adverse_rows_means_no_extra_lines(self):
        import render_tree as R
        self.assertEqual(R.adverse_lines(self._node_without_adverse(), {}, {}), [])

    def test_row_roles_fallback_without_finals(self):
        import render_tree as R
        self.assertEqual(R.adverse_lines(self._node(), {}, {}), [("Impact: self debuff (adverse)", L.ROLE_COLORS["SELF DEBUFF"])])



class ScopeAndDisplay(unittest.TestCase):
    """RUL-2026-10-03-005: element-wide scope and % display on every non-Damage modifier."""

    def test_scope_sentence_is_element_wide(self):
        self.assertEqual(L.scope_sentence({"qualifying_elements": ["Shadow"], "label_kind": "element"}),
                         "Bonuses apply to matching supported tags on all Shadow jutsu.")
        self.assertEqual(L.scope_sentence({"qualifying_elements": ["Shadow", "Storm"], "label_kind": "multi-element"}),
                         "Bonuses apply to matching supported tags on all Shadow and Storm jutsu.")
        self.assertEqual(L.scope_sentence({"qualifying_elements": [], "label_kind": "classification extension",
                                           "potency_classification": "Dai Kenja"}),
                         "Bonuses apply to matching supported tags on all Dai Kenja-classified jutsu (requires classification extension).")

    def test_percent_display(self):
        self.assertEqual(L.mod_text("damage", 2), "+2 Damage")
        self.assertEqual(L.mod_text("afterburn", 5), "+5% Afterburn")
        self.assertEqual(L.mod_text("lifesteal", 3), "+3% Lifesteal")
        self.assertEqual(L.mod_text("heal", 3), "+3% Heal")
        self.assertEqual(L.mod_text("increaseheal", 3), "+3% Increase Heal")
        self.assertEqual(L.mod_text("reflect", 4, abbr=True), "+4% REF")
        for tag in L.SUPPORTED_TAGS:
            txt = L.mod_text(tag, 1)
            self.assertEqual(txt.endswith("Damage") and "%" not in txt, tag == "damage", txt)

    def test_rendered_outputs_never_print_damage_percent_or_raw_power(self):
        import glob
        for p in glob.glob(os.path.join(L.TREES_DIR, "*.svg")) + glob.glob(os.path.join(L.TREES_DIR, "*.md")):
            txt = open(p, encoding="utf-8").read()
            for bad in ("% Damage<", "Damage power", "Heal power", "Damage %"):
                self.assertNotIn(bad, txt, f"{os.path.basename(p)} prints {bad!r}")


def _tree_with(mods_by_id, extra=None):
    """Taiyo shape: F1→H2→A3, F1→H4→A5, F6→H7→A8, F6→H9→A10."""
    shape = {"01": ("Foundation", []), "02": ("Hidden Art", ["01"]), "03": ("Advanced Art", ["02"]),
             "04": ("Hidden Art", ["01"]), "05": ("Advanced Art", ["04"]), "06": ("Foundation", []),
             "07": ("Hidden Art", ["06"]), "08": ("Advanced Art", ["07"]), "09": ("Hidden Art", ["06"]),
             "10": ("Advanced Art", ["09"])}
    names = {"01": "Alpha", "02": "Bravo", "03": "Charlie", "04": "Delta", "05": "Echo", "06": "Foxtrot",
             "07": "Golf", "08": "Hotel", "09": "India", "10": "Juliet"}
    nodes = []
    for i, (cat, par) in shape.items():
        mods = [{"tag": t, "flat": f} for t, f in mods_by_id.get(i, [("increasedamagegiven", 1)])]
        nodes.append({"id": i, "name": names[i], "category": cat, "cost": 1, "parents": par, "modifiers": mods})
    t = {"title": "t", "nodes": nodes, "examples": []}
    t.update(extra or {})
    return t


class Ceilings(unittest.TestCase):
    def test_damage_hard_ceiling_five_over_any_allocation(self):
        ok = _tree_with({"02": [("damage", 2)], "03": [("damage", 3)]})
        self.assertEqual(L.ceiling_findings(ok)[0], [])
        # a Foundation +1 Damage pushes the 4-purchase route to 6: invalid
        bad = _tree_with({"01": [("damage", 1)], "02": [("damage", 2)], "03": [("damage", 3)]})
        errs = L.ceiling_findings(bad)[0]
        self.assertTrue(any("Damage +6 Damage" in e and "hard ceiling +5 Damage" in e for e in errs), errs)
        # a fourth purchase on another branch also counts
        bad2 = _tree_with({"02": [("damage", 2)], "03": [("damage", 3)], "04": [("damage", 1)]})
        self.assertTrue(L.ceiling_findings(bad2)[0])

    def test_lifesteal_hard_ceiling_five(self):
        self.assertEqual(L.ceiling_findings(_tree_with({"04": [("lifesteal", 2)], "05": [("lifesteal", 3)]}))[0], [])
        errs = L.ceiling_findings(_tree_with({"04": [("lifesteal", 3)], "05": [("lifesteal", 5)]}))[0]
        self.assertTrue(any("+8% Lifesteal" in e and "hard ceiling +5% Lifesteal" in e for e in errs), errs)

    def test_afterburn_hard_ceiling_fifteen(self):
        self.assertEqual(L.ceiling_findings(_tree_with({"04": [("afterburn", 5)], "05": [("afterburn", 10)]}))[0], [])
        errs = L.ceiling_findings(_tree_with({"01": [("afterburn", 1)], "04": [("afterburn", 5)], "05": [("afterburn", 10)]}))[0]
        self.assertTrue(any("+16% Afterburn" in e for e in errs), errs)

    def test_hard_ceiling_cannot_be_excepted(self):
        t = _tree_with({"02": [("damage", 3)], "03": [("damage", 3)]},
                       {"director_exceptions": [{"tag": "damage", "max": 6, "reason": "x", "status": "pending director review"}]})
        errs = L.ceiling_findings(t)[0]
        self.assertTrue(any("cannot lift the hard Damage ceiling" in e for e in errs), errs)
        self.assertTrue(any("exceeds the hard ceiling" in e for e in errs), errs)

    def test_other_tag_over_ten_needs_reviewed_exception(self):
        mods = {"06": [("decreasedamagetaken", 2)], "07": [("decreasedamagetaken", 3)], "08": [("decreasedamagetaken", 7)]}
        errs, warns, _ = L.ceiling_findings(_tree_with(mods))
        self.assertTrue(any("+12% Decrease Damage Taken" in e and "director-review exception" in e for e in errs), errs)
        t = _tree_with(mods, {"director_exceptions": [{"tag": "decreasedamagetaken", "max": 12,
                                                        "reason": "single low-uptime row", "status": "pending director review"}]})
        errs, warns, _ = L.ceiling_findings(t)
        self.assertEqual(errs, [])
        self.assertTrue(any("director-review exception (pending director review)" in w for w in warns), warns)
        # an exception below the real maximum does not cover it
        t2 = _tree_with(mods, {"director_exceptions": [{"tag": "decreasedamagetaken", "max": 11, "reason": "r"}]})
        self.assertTrue(L.ceiling_findings(t2)[0])
        # an exception without a reason is not an exception
        t3 = _tree_with(mods, {"director_exceptions": [{"tag": "decreasedamagetaken", "max": 12, "reason": ""}]})
        self.assertTrue(L.ceiling_findings(t3)[0])

    def test_ten_percent_is_allowed_without_exception(self):
        mods = {"06": [("decreasedamagetaken", 2)], "07": [("decreasedamagetaken", 3)], "08": [("decreasedamagetaken", 5)]}
        errs, warns, rep = L.ceiling_findings(_tree_with(mods))
        self.assertEqual(errs, [])
        self.assertEqual(rep["maximum_over_all_legal_allocations"]["decreasedamagetaken"], 10)

    def test_irregular_route_warns_without_rationale(self):
        mods = {"06": [("decreasedamagetaken", 2)], "07": [("decreasedamagetaken", 3)], "08": [("decreasedamagetaken", 2)]}
        errs, warns, _ = L.ceiling_findings(_tree_with(mods))
        self.assertEqual(errs, [])
        self.assertTrue(any("route Hotel primary total +7% Decrease Damage Taken is off the 5/10/15 bands" in w for w in warns), warns)
        errs, warns, rep = L.ceiling_findings(_tree_with(mods, {"route_band_rationale": {"08": "single 2-round row"}}))
        self.assertFalse(any("route Hotel" in w for w in warns), warns)
        self.assertEqual(next(r for r in rep["routes"] if r["advanced_art"] == "08")["band_rationale"], "single 2-round row")
        self.assertTrue(L.ceiling_findings(_tree_with(mods, {"route_band_rationale": {"07": "x"}}))[0])

    def test_two_advanced_arts_cost_more_than_four(self):
        by = {x.id: x for x in L.parse_nodes(_tree_with({}))}
        adv = [i for i, x in by.items() if x.category == "Advanced Art"]
        import itertools
        for a, b in itertools.combinations(adv, 2):
            self.assertGreater(len(L.closure(a, by) | L.closure(b, by)), L.BP_CAP)


if __name__ == "__main__":
    unittest.main()
