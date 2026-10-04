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



class ReferenceTrees(unittest.TestCase):
    """Generated trees that encode director rulings must match them exactly."""

    def _tree(self, slug):
        return L.load_json(os.path.join(L.TREES_DIR, slug + ".json"))

    def _mods(self, tree):
        return {n["id"]: (n["name"], n["category"], tuple(n["parents"]), tuple((m["tag"], m["flat"]) for m in n["modifiers"]))
                for n in tree["nodes"]}

    def test_taiyo_projection_preserves_handoff_values(self):
        hand = L.load_json(REFERENCE)
        proj = self._tree("taiyo_kami")
        self.assertEqual(self._mods(proj), self._mods(hand))
        self.assertEqual([e["ids"] for e in proj["examples"]], [e["ids"] for e in hand["examples"]])
        self.assertEqual(proj["classification"]["qualifying_elements"], ["Scorch"])
        self.assertEqual(proj["classification"]["applies_to"], "matching supported tags on all Scorch jutsu")
        routes = {r["name"]: (r["primary_tag"], r["total"]) for r in proj["audit"]["ceilings"]["routes"]}
        self.assertEqual(routes, {"Solar Cataclysm": ("damage", 5), "Eternal Noon": ("afterburn", 10),
                                  "Sovereign Sun": ("decreasedamagetaken", 10), "Dying Light": ("decreasedamagegiven", 10)})

    def test_blood_enchanted_eyes_matches_rul_2026_10_04_001(self):
        t = self._tree("blood_enchanted_eyes")
        self.assertEqual(t["title"], "Blood-Enchanted Eyes — Crimson Covenant")
        want = {
            "01": ("Scarlet Gaze", "Foundation", (), (("increasedamagegiven", 2), ("increasedamagetaken", 2))),
            "02": ("Opened Veins", "Hidden Art", ("01",), (("increasedamagetaken", 3),)),
            "03": ("Rite of Exsanguination", "Advanced Art", ("02",), (("damage", 2),)),
            "09": ("Crimson Thirst", "Hidden Art", ("01",), (("lifesteal", 2),)),
            "10": ("Feast of the Fallen", "Advanced Art", ("09",), (("lifesteal", 3), ("increasedamagegiven", 5))),
            "06": ("Iron in the Blood", "Foundation", (), (("decreasedamagetaken", 2), ("decreasedamagegiven", 2))),
            "07": ("Closed Wounds", "Hidden Art", ("06",), (("decreasedamagetaken", 3),)),
            "08": ("Deathless Vitality", "Advanced Art", ("07",), (("decreasedamagetaken", 5), ("decreasedamagegiven", 3))),
            "04": ("Carrion Fever", "Hidden Art", ("06",), (("decreasedamagegiven", 3),)),
            "05": ("Red Pestilence", "Advanced Art", ("04",), (("decreasedamagegiven", 5), ("decreasedamagetaken", 3))),
        }
        self.assertEqual(self._mods(t), want)
        self.assertNotIn("afterburn", {m["tag"] for n in t["nodes"] for m in n["modifiers"]})
        self.assertEqual(t["classification"]["qualifying_elements"], ["Shadow"])
        self.assertEqual(t["classification"]["applies_to"], "matching supported tags on all Shadow jutsu")
        self.assertEqual({e["archetype"] for e in t["examples"]}, {"Burst", "Sustain Offense", "Fortress", "Suppression"})
        mx = t["audit"]["ceilings"]["maximum_over_all_legal_allocations"]
        self.assertEqual((mx["damage"], mx["lifesteal"], mx["decreasedamagetaken"], mx["decreasedamagegiven"]), (2, 5, 10, 10))
        # the keystones are castability gates, never prerequisites or printed scope
        for ext in (".json", ".md", ".svg"):
            txt = open(os.path.join(L.TREES_DIR, "blood_enchanted_eyes" + ext), encoding="utf-8").read()
            self.assertNotIn("Tithe of the Red Eye", txt)
            if ext == ".svg":
                self.assertNotIn("Wraith Pendant", txt.split('<metadata')[0])
                self.assertNotIn("Reaper's Ring", txt.split('<metadata')[0])
                self.assertIn("Bonuses apply to matching supported tags on all Shadow jutsu.", txt)

    def test_shakunetsu_sakura_matches_rul_2026_10_04_002(self):
        t = self._tree("shakunetsu_sakura")
        want = {
            "01": ("Ember Dragon's Roots", "Foundation", (), (("increasedamagegiven", 2),)),
            "02": ("Kindled Boughs", "Hidden Art", ("01",), (("increasedamagegiven", 3),)),
            "03": ("Dragon in Full Blossom", "Advanced Art", ("02",), (("increasedamagegiven", 5), ("heal", 5))),
            "04": ("Burning Petal Carpet", "Hidden Art", ("06",), (("increasedamagetaken", 2),)),
            "05": ("Conflagration in Bloom", "Advanced Art", ("04",), (("increasedamagetaken", 3), ("damage", 2))),
            "06": ("Falling Ember Petals", "Foundation", (), (("decreasedamagegiven", 2),)),
            "07": ("Blossom Dominion", "Hidden Art", ("01",), (("increasedamagegiven", 3),)),
            "08": ("Scorching Hanami", "Advanced Art", ("07",), (("increasedamagegiven", 5), ("decreasedamagegiven", 3))),
            "09": ("Smothering Petal Rain", "Hidden Art", ("06",), (("decreasedamagegiven", 3),)),
            "10": ("Deluge of Burning Petals", "Advanced Art", ("09",), (("decreasedamagegiven", 5), ("heal", 5))),
        }
        self.assertEqual(self._mods(t), want)
        # the approved tree reaches +13% IDG with a capstone plus the sibling Hidden Art: recorded, not silent
        self.assertEqual(t["audit"]["ceilings"]["maximum_over_all_legal_allocations"]["increasedamagegiven"], 13)
        self.assertEqual([e["tag"] for e in t["director_exceptions"]], ["increasedamagegiven"])
        self.assertEqual(L.ceiling_findings(t)[0], [])

    def test_arashima_matches_rul_2026_10_04_003(self):
        t = self._tree("arashima")
        self.assertEqual(t["title"], "Arashima — Reaper's Tempest")
        want = {
            "01": ("Tempest Hymn", "Foundation", (), (("increasedamagegiven", 3),)),
            "02": ("Gathering Thunderhead", "Hidden Art", ("01",), (("increasedamagegiven", 2),)),
            "03": ("Sundered Sky", "Advanced Art", ("02",), (("increasedamagegiven", 3), ("damage", 2))),
            "04": ("Crimson Downpour", "Hidden Art", ("01",), (("lifesteal", 2),)),
            "05": ("The Storm's Due", "Advanced Art", ("04",), (("lifesteal", 3), ("increasedamagegiven", 5))),
            "06": ("Stillness in the Squall", "Foundation", (), (("decreasedamagetaken", 2), ("decreasedamagegiven", 2))),
            "07": ("Stormwarden's Hide", "Hidden Art", ("06",), (("decreasedamagetaken", 3),)),
            "08": ("Unbroken Horizon", "Advanced Art", ("07",), (("decreasedamagetaken", 5), ("lifesteal", 2))),
            "09": ("Deadwind Dirge", "Hidden Art", ("06",), (("decreasedamagegiven", 3),)),
            "10": ("Silence After Thunder", "Advanced Art", ("09",), (("decreasedamagegiven", 5), ("decreasedamagetaken", 2))),
        }
        self.assertEqual(self._mods(t), want)
        names = {n["name"] for n in t["nodes"]}
        self.assertFalse(names & {"Reaper's Harvest", "Torrential Downpour"})

    def test_ethereal_monarch_director_correction(self):
        t = self._tree("ethereal_monarch")
        m = self._mods(t)
        self.assertEqual(t["title"], "Ethereal Monarch — Mandate of Heaven")
        self.assertEqual(m["03"][0], "Ethereal Coronation")
        self.assertEqual(m["03"][3], (("damage", 3),))
        self.assertEqual(m["05"][0], "Rain of Fallen Stars")
        self.assertEqual(m["05"][3], (("afterburn", 7), ("increasedamagetaken", 3), ("increasedamagegiven", 3)))
        self.assertEqual(L.ceiling_findings(t)[0], [])

    def test_every_tree_is_within_the_ceilings(self):
        import glob
        for p in sorted(glob.glob(os.path.join(L.TREES_DIR, "*.json"))):
            if p.endswith(".validation.json"):
                continue
            t = L.load_json(p)
            errs = L.ceiling_findings(t)[0]
            self.assertEqual(errs, [], os.path.basename(p))
            self.assertEqual(L.stale_language(t), [], os.path.basename(p))

    def test_no_bloodline_id_selector_in_classification(self):
        import glob
        for p in sorted(glob.glob(os.path.join(L.TREES_DIR, "*.json"))):
            if p.endswith(".validation.json"):
                continue
            t = L.load_json(p)
            c = t["classification"]
            name = t["bloodline"]["name"]
            self.assertNotIn("bloodline", c, os.path.basename(p))  # no bloodline key inside the selector
            self.assertTrue(c["applies_to"].startswith("matching supported tags on all "), p)
            self.assertIn("bloodline id or bloodline ownership", " ".join(c["not_selectors"]))
            self.assertTrue(any("equipment" in x for x in c["not_selectors"]))
            if c["label_kind"] != "classification extension":
                self.assertNotIn(name, c["applies_to"], p)
                for n in t["nodes"]:
                    self.assertNotIn(name, n["scope"], p)


class ReviewAudits(unittest.TestCase):
    """BALANCE_REVIEW_METHOD.md evidence: damage tiers, fourth purchases, overlap."""

    def _rows(self, bases):
        return [L.Row("j%d" % i, "J%d" % i, "A", "BLOODLINE", "", 0, "damage", "Damage", "formula", float(b), b, 0, 0,
                      ["Shadow"], ["Shadow"], "INHERIT", "OPPONENT", None, "enemy", "enemy", "DAMAGE", False, None, None,
                      None, True, "public", None, "BOTH", False, False, 60, 7, "SINGLE", 4) for i, b in enumerate(bases)]

    def test_damage_tiers(self):
        self.assertEqual([L.damage_tier(v) for v in (37, 38, 40, 44, 45, 49, 50, 51)],
                         ["below Light", "Light", "Normal", "Normal", "High", "High", "Nuke", "above Nuke"])

    def test_damage_threshold_audit_covers_every_reachable_total(self):
        t = _tree_with({"02": [("damage", 2)], "03": [("damage", 3)], "04": [("damage", 1)]})
        a = L.damage_threshold_audit(t, self._rows([40, 45, 50]))
        self.assertEqual(a["damage_totals_reachable"], [1, 2, 3, 5, 6])  # 01+04, 01+02, 01+02+04, 01+02+03, 01+02+03+04
        r40 = next(r for r in a["rows"] if r["base"] == 40)
        self.assertEqual([s["final"] for s in r40["steps"]], [41, 42, 43, 45, 46])
        self.assertTrue(next(s for s in r40["steps"] if s["added"] == 5)["tier_change"])  # 40 Normal -> 45 High
        self.assertEqual({(x["base"], x["final"]) for x in a["above_nuke"]}, {(45, 51), (50, 51), (50, 52), (50, 53), (50, 55), (50, 56)})

    def test_above_nuke_needs_rationale(self):
        import validate_tree as V
        t = L.load_json(os.path.join(L.TREES_DIR, "taiyo_kami.json"))
        self.assertTrue(t.get("above_nuke_rationale"))  # protected reference: Incandescent Nova 50 -> 55 is explained
        a = L.damage_threshold_audit(t, taiyo_rows())
        self.assertIn((50.0, 55.0), {(x["base"], x["final"]) for x in a["above_nuke"]})
        t2 = copy.deepcopy(t)
        t2.pop("above_nuke_rationale")
        snap = L.load_snapshot(); roster = L.load_roster()
        kit, rec = V.find_kit(t2, snap, roster)
        _, _, errors, _ = V.normalize(t2, kit, rec, taiyo_rows(), L.DEFAULT_JUTSU_LEVEL)
        self.assertTrue(any("above the 50 Nuke tier" in e for e in errors), errors)

    def test_fourth_bp_audit_lists_every_legal_fourth(self):
        t = _tree_with({"02": [("damage", 2)], "03": [("damage", 3)], "04": [("lifesteal", 5)]})
        rows = self._rows([40]) + [L.Row("k", "K", "A", "BLOODLINE", "", 0, "lifesteal", "Lifesteal", "percentage", 20.0, 20, 0, 2,
                                         [], ["None"], "SELF", "SELF", None, "self", "self", "SELF BUFF", False, None, None, None,
                                         True, "public", None, "BOTH", False, False, 40, 7, "SINGLE", 0)]
        fb = {x["advanced_art"]: x for x in L.fourth_bp_audit(t, rows)}
        c = fb["03"]
        self.assertEqual(c["path"], ["01", "02", "03"])
        self.assertEqual(sorted(f["id"] for f in c["fourths"]), ["04", "06"])  # sibling Hidden Art or the other Foundation
        self.assertEqual(c["highest_diagnostic_fourth"], "04")  # +5% Lifesteal on one row outweighs +1% IDG
        self.assertEqual(next(f for f in c["fourths"] if f["id"] == "04")["bonuses"]["lifesteal"], 5)

    def test_route_overlap_flags_same_primary_siblings(self):
        t = _tree_with({"03": [("increasedamagegiven", 5)], "05": [("increasedamagegiven", 5), ("heal", 3)],
                        "08": [("decreasedamagetaken", 5)], "10": [("decreasedamagegiven", 5)]})
        ov = L.route_overlap(t)
        pair = next(o for o in ov if {o["a"], o["b"]} == {"03", "05"})
        self.assertTrue(pair["same_primary_tag"] and pair["siblings"])
        self.assertFalse(any({o["a"], o["b"]} == {"08", "10"} and o["same_primary_tag"] for o in ov))

    def test_display_label_lint(self):
        t = {"design_notes": ["+2 Damage power on both rows"], "risks": ["the static row adds 5 heal power (300 HP per tick)"]}
        hits = L.stale_language(t)
        self.assertEqual(len(hits), 1, hits)
        self.assertIn("design_notes", hits[0])

    def _prow(self, tag, base, i=0, adverse=False):
        return L.Row("p%d" % i, "P%d" % i, "A", "BLOODLINE", "", 0, tag, L.TAG_LABELS[tag], "percentage", float(base), base, 0, 2,
                     ["Shadow"], ["Shadow"], "INHERIT", "SELF", None, "self", "self", "SELF BUFF", adverse, None, None, None,
                     True, "public", None, "BOTH", False, False, 40, 7, "SINGLE", 0)

    def test_compounded_factor(self):
        rows = [self._prow("increasedamagetaken", 35, 0), self._prow("increasedamagetaken", 35, 1),
                self._prow("decreasedamagetaken", 35, 2), self._prow("increasedamagetaken", 35, 3, adverse=True)]
        self.assertAlmostEqual(L.compounded_factor("increasedamagetaken", rows, 8), (1.43 / 1.35) ** 2, places=9)  # adverse row ignored
        self.assertAlmostEqual(L.compounded_factor("decreasedamagetaken", rows, 10), 0.55 / 0.65, places=9)
        self.assertEqual(L.compounded_factor("increasedamagegiven", rows, 5), 1.0)

    def test_capstone_free_near_ties(self):
        mods = {"01": [("increasedamagegiven", 2)], "02": [("increasedamagegiven", 2)], "03": [("increasedamagegiven", 4)],
                "04": [("increasedamagegiven", 3)], "05": [("heal", 5)], "06": [("decreasedamagetaken", 2)],
                "07": [("decreasedamagetaken", 3)], "08": [("decreasedamagetaken", 5)], "09": [("heal", 2)], "10": [("heal", 3)]}
        ties = L.capstone_free_near_ties(_tree_with(mods))
        self.assertEqual([(n["advanced_art"], n["route_total"], n["capstone_free"]) for n in ties], [("03", 8, 7)])  # 01+02+04 reach +7
        mods["04"] = [("increasedamagegiven", 1)]
        self.assertEqual(L.capstone_free_near_ties(_tree_with(mods)), [])

    def test_offense_packages_count_flat_damage(self):
        mods = {"01": [("increasedamagegiven", 2)], "02": [("increasedamagegiven", 3)], "03": [("damage", 2)],
                "04": [("decreasedamagetaken", 3)], "05": [("decreasedamagetaken", 5)], "06": [("decreasedamagetaken", 2)],
                "07": [("decreasedamagetaken", 3)], "08": [("decreasedamagetaken", 5)], "09": [("heal", 2)], "10": [("heal", 3)]}
        rows = self._rows([40, 50]) + [self._prow("increasedamagegiven", 35)]
        op = L.offense_packages(_tree_with(mods), rows)
        self.assertAlmostEqual(op["percent"]["factor"], round(1.40 / 1.35, 3))
        self.assertAlmostEqual(op["with_damage"]["factor"], round(1.40 / 1.35 * 42 / 40, 3))  # most-lifted row is the 40
        self.assertIn("03", op["with_damage"]["allocation"])

    def test_rebalance_audit_output_is_current(self):
        import rebalance_audit as RA
        d = RA.build()
        self.assertEqual(open(RA.OUT_MD, encoding="utf-8").read(), RA.md(d))


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

    def test_bands_are_guardrails_not_targets(self):
        # BALANCE_REVIEW_METHOD.md: route totals are reported, never warned for being off band
        mods = {"06": [("decreasedamagetaken", 2)], "07": [("decreasedamagetaken", 3)], "08": [("decreasedamagetaken", 2)]}
        errs, warns, rep = L.ceiling_findings(_tree_with(mods))
        self.assertEqual(errs, [])
        self.assertFalse(any("band" in w for w in warns), warns)
        hotel = next(r for r in rep["routes"] if r["advanced_art"] == "08")
        self.assertEqual((hotel["total"], hotel["on_band"]), (7, False))
        # a Damage route that is not Hidden +2 / Advanced +3 is not a warning either
        errs, warns, _ = L.ceiling_findings(_tree_with({"02": [("increasedamagetaken", 3)], "03": [("damage", 2)]}))
        self.assertFalse(any("default" in w for w in warns), warns)
        # an optional rationale is still carried, and must name an Advanced Art
        errs, warns, rep = L.ceiling_findings(_tree_with(mods, {"route_band_rationale": {"08": "single 2-round row"}}))
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
