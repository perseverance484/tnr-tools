#!/usr/bin/env python3
"""Tests for scripts/skyglass_check.py. Socket-free; reads only repository files and temporary copies.

    python3 -m unittest scripts/test_skyglass_check.py -v
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skyglass_check as sc  # noqa: E402

ROOT = sc.ROOT
FIX = os.path.join(ROOT, "scripts", "fixtures", "skyglass_check")
FAIL = {"fail_picks.json": "picks", "fail_win_only.json": "win-only", "fail_chest_text.json": "chest-text",
        "fail_voice.json": "voice", "fail_chart_tier.json": "chart-tier", "fail_prof_chest.json": "prof-chest"}


def run(paths, root=ROOT):
    findings, scanned, io_errors = sc.check(root, paths)
    return findings, scanned, io_errors


def errors(findings):
    return [f for f in findings if f.level == "ERROR"]


class DesignIntegrity(unittest.TestCase):
    def test_repository_design_data_matches_its_sources(self):
        d = sc.Design(ROOT)
        self.assertEqual([str(f) for f in d.findings], [])

    def test_every_section_4a_row_is_in_the_data(self):
        d = sc.Design(ROOT)
        rows = {r["doc_row"] for r in d.data["picks"]["runs"]}
        self.assertEqual(rows, {"Low Tide Run", "Night Watch", "Buried Cache", "Drowned Foundry", "Quarantined Archive",
                                "Captain's Watch", "Sealed Reliquary", "The Fall", "Tainted runs", "Crownhold"})
        self.assertEqual({r["run"]: r["pickCount"] for r in d.runs.values() if r["pickCount"] != 1},
                         {"The Rotted Reliquary": 2, "The Burning Heading": 2})

    def test_banned_words_are_parsed_from_the_story_bible(self):
        words = [w for w, _, _ in sc.Design(ROOT).banned]
        for w in ("system", "network", "lattice", "conduit", "lift", "unit", "seven-bladed", "hunt chart"):
            self.assertIn(w, words)


class TempRoot(unittest.TestCase):
    """A copy of just the files the design check reads, so a doc edit can be simulated."""
    PURSE = "Captain's Purse (1,000,000 ryo)"
    FILES = [sc.DESIGN, sc.LOOT, sc.BIBLE, sc.RULINGS, sc.TEXT, sc.NAMES, "state/crownhold/ids.json",
             "push/skyglass_hunts.gen.py", "push/skyglass_update.gen.py", "push/elemental_pouch.gen.py",
             "push/crownhold.gen.py"]

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for rel in self.FILES:
            os.makedirs(os.path.dirname(os.path.join(self.tmp, rel)), exist_ok=True)
            shutil.copy(os.path.join(ROOT, rel), os.path.join(self.tmp, rel))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, rel, old, new, count=1):
        p = os.path.join(self.tmp, rel)
        with open(p, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn(old, text)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text.replace(old, new, count))

    def design_errors(self):
        return [f for f in sc.Design(self.tmp).findings if f.level == "ERROR"]

    def test_copy_is_clean(self):
        self.assertEqual(self.design_errors(), [])

    def test_doc_cell_change_is_caught(self):
        self.edit(sc.LOOT, "| Buried Cache | Medicine Inro / Galley Stores / Chart of the Drowned Foundry |",
                  "| Buried Cache | Medicine Inro / Galley Stores / Tide Chart |")
        msgs = [f.msg for f in self.design_errors()]
        self.assertTrue(any("section 4a now reads" in m and "Tide Chart" in m for m in msgs), msgs)

    def test_new_doc_row_is_caught(self):
        self.edit(sc.LOOT, "| Crownhold | Crown's Hoard", "| Proving Ground | Skyglass Coffer |\n| Crownhold | Crown's Hoard")
        msgs = [f.msg for f in self.design_errors()]
        self.assertTrue(any("'Proving Ground' has no entry" in m for m in msgs), msgs)

    def test_pick_rule_change_is_caught(self):
        self.edit(sc.LOOT, "**Pick 1 on every run; tainted runs pick 2.**", "**Pick 2 on every run.**")
        self.assertTrue(any(f.field == "doc_rule" for f in self.design_errors()))

    def test_chart_tier_row_change_is_caught(self):
        self.edit(sc.RULINGS, "| Rare | hunt charts | Sage's Strongbox", "| Epic | hunt charts | Sage's Strongbox")
        self.assertTrue(any(f.where == "chart_tiers.Rare charts" and f.field == "doc_row" for f in self.design_errors()))

    def test_id_missing_from_its_source_is_caught(self):
        self.edit("push/elemental_pouch.gen.py", "D0gtI5dOgj2dFO4VexsLJ", "somethingelse", count=-1)
        self.assertTrue(any("D0gtI5dOgj2dFO4VexsLJ" in f.msg for f in self.design_errors()))

    def test_badge_resolves_from_ids_file_when_it_exists(self):
        p = os.path.join(self.tmp, "state/crownhold/ids.json")
        with open(p, encoding="utf-8") as fh:
            ids = json.load(fh)
        ids.pop("badge:crownbreaker", None)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(ids, fh)
        self.assertIsNone(sc.Design(self.tmp).ids["crownhold_badge"])
        ids["badge:crownbreaker"] = "BADGE123"
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(ids, fh)
        self.assertEqual(sc.Design(self.tmp).ids["crownhold_badge"], "BADGE123")

    def test_tier_colour_change_in_section_0_is_caught(self):
        self.edit(sc.LOOT, '<span style="color:#3b82f6"><b>Rare', '<span style="color:#2563eb"><b>Rare')
        self.assertTrue(any(f.field == "TIER_COLOURS" and "Rare" in f.msg for f in self.design_errors()))

    def test_forbidden_colour_is_bound_to_its_sources(self):
        # RUL-2026-10-29-058: Forbidden is not in the section 0 template; its name/red come from the loot tables header
        # and its hex from the text doc. Changing either source fails the design check.
        self.edit(sc.TEXT, "Forbidden tier uses red `#ef4444`", "Forbidden tier uses red `#dc2626`")
        self.assertTrue(any(f.field == "TIER_COLOUR_EVIDENCE" and "#ef4444" in f.msg for f in self.design_errors()))
        self.setUp()
        self.edit(sc.LOOT, "plus **Forbidden** above Legendary (red)", "plus **Mythic** above Legendary (red)")
        self.assertTrue(any(f.field == "TIER_COLOUR_EVIDENCE" for f in self.design_errors()))

    def test_profession_flag_rule_is_bound_to_section_4b(self):
        self.edit(sc.LOOT, "The chests need no huntable/gatherable flags.", "The chests are flagged huntable/gatherable.")
        self.assertTrue(any(f.where == "profession_chests.flags" and f.field == "doc" for f in self.design_errors()))
        self.setUp()
        self.edit_data(lambda d: d["profession_chests"].pop("flags"))
        self.assertTrue(any(f.where == "profession_chests.flags" for f in self.design_errors()))

    def test_profession_flags_are_enforced_again_when_required(self):
        self.edit_data(lambda d: d["profession_chests"]["flags"].update(required=True))
        findings, _, _ = sc.check(self.tmp, [os.path.join(FIX, "fail_prof_chest.json")])
        self.assertTrue(any("canBeHunted=false" in f.msg for f in errors(findings)), [str(f) for f in findings])

    def _foundry_with(self, reward):
        with open(os.path.join(FIX, "pass.json"), encoding="utf-8") as fh:
            m = json.load(fh)
        it = next(i for i in m["items"] if (i.get("data") or {}).get("name") == "The Drowned Foundry")
        win = next(o for o in it["data"]["content"]["objectives"] if o.get("task") == "win_quest")
        win.update(reward)
        p = os.path.join(self.tmp, "foundry_prof.json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(m, fh)
        findings, _, _ = sc.check(self.tmp, [p])
        return [f for f in errors(findings) if f.check == "prof-chest"]

    def test_review_plain_profession_chest_reward_is_caught(self):
        cid = sc.Design(self.tmp).ids["epic_hunters_chest"]
        errs = self._foundry_with({"reward_items": [{"ids": [cid], "number": 100, "quantity": 1}]})
        self.assertTrue(any("carries no profession drops" in f.msg for f in errs), errs)

    def test_review_profession_chest_inside_a_package_is_caught(self):
        cid = sc.Design(self.tmp).ids["epic_hunters_chest"]
        errs = self._foundry_with({"reward_packages": [{"rewards": {"reward_items": [{"ids": [cid], "number": 100, "quantity": 1}]}}]})
        self.assertTrue(any("carries no profession drops" in f.msg for f in errs), errs)

    def test_section_4b_no_drops_row_is_bound(self):
        self.edit(sc.LOOT, "- **Shared hunts carry no profession drops.**", "- **Shared hunts carry Epic profession drops.**")
        self.assertTrue(any(f.where == "profession_chests.areas" and f.field == "doc_row" for f in self.design_errors()))

    def edit_data(self, mutate):
        p = os.path.join(self.tmp, sc.DESIGN)
        with open(p, encoding="utf-8") as fh:
            data = json.load(fh)
        mutate(data)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(data, fh)

    def test_review4_data_values_must_match_the_doc_values(self):
        def wrong(data):
            run = next(r for r in data["picks"]["runs"] if r["run"] == "Drowned Foundry")
            run["pickCount"] = 2
            run["options"][1] = {"money": 1}
        self.edit_data(wrong)
        errs = {(f.where, f.field) for f in self.design_errors()}
        self.assertIn(("picks.Drowned Foundry", "pickCount"), errs)
        self.assertIn(("picks.Drowned Foundry", "options"), errs)
        # and a manifest matching those wrong values does not pass: the design errors fail the run
        findings, _, _ = sc.check(self.tmp, [os.path.join(FIX, "pass.json")])
        self.assertTrue(any(f.check == "design" and f.level == "ERROR" for f in findings))

    def test_review4_wrong_quantity_and_inherited_pick_count(self):
        def wrong(data):
            for r in data["picks"]["runs"]:
                if r["run"] == "The Fall":
                    r["options"][3] = {"item": "galley_stores", "quantity": 2}
                if r["run"] == "The Rotted Reliquary":
                    r["pickCount"] = 1
        self.edit_data(wrong)
        errs = {(f.where, f.field) for f in self.design_errors()}
        self.assertIn(("picks.The Fall", "options"), errs)
        self.assertIn(("picks.The Rotted Reliquary", "pickCount"), errs)

    def test_review4_doc_value_change_is_caught_even_with_doc_options_updated(self):
        self.edit(sc.LOOT, "| The Fall | Skyglass Coffer ×2 / Sealed Treasury / Skyglass Token ×2 / Galley Stores ×3 |",
                  "| The Fall | Skyglass Coffer ×2 / Sealed Treasury / Skyglass Token ×2 / Galley Stores ×4 |")
        self.edit_data(lambda d: next(r for r in d["picks"]["runs"] if r["run"] == "The Fall")
                       .update(doc_options="Skyglass Coffer ×2 / Sealed Treasury / Skyglass Token ×2 / Galley Stores ×4"))
        self.assertTrue(any(f.field == "options" and "'quantity': 4" in f.msg for f in self.design_errors()))

    def test_review4_ruling_backed_alias_and_tainted_evidence(self):
        self.edit(sc.RULINGS, "The Captain's Purse becomes 1,000,000 ryo", "The Captain's Purse becomes 1,200,000 ryo")
        self.edit(sc.LOOT, "- **The Burning Heading** (tainted Last Heading)", "- **The Burning Heading** (tainted Reliquary Seal)")
        fields = {f.field for f in self.design_errors()}
        self.assertIn("evidence", fields)
        self.assertIn("doc_evidence", fields)

    def test_review5_purse_alias_amount_is_bound_to_its_ruling(self):
        # Alias and data both moved to 1 ryo while the ruling still says 1,000,000: must fail.
        def wrong(d):
            d["picks"]["doc_aliases"][self.PURSE].update(money=1)
            next(r for r in d["picks"]["runs"] if r["run"] == "Captain's Watch")["options"][1] = {"money": 1}
        self.edit_data(wrong)
        self.assertTrue(any(f.field == "money" and "1000000" in f.msg for f in self.design_errors()))

    def test_purse_amount_in_the_cell_is_bound(self):
        # The section 4a cell states the amount; changing it breaks the alias name and so the option.
        self.edit(sc.LOOT, "Captain's Purse (1,000,000 ryo)", "Captain's Purse (2,000,000 ryo)")
        self.assertTrue(any(f.where == "picks.Captain's Watch" and "names nothing" in f.msg for f in self.design_errors()))

    def test_review5_tainted_inheritance_is_derived_from_section_5(self):
        self.edit_data(lambda d: next(r for r in d["picks"]["runs"] if r["run"] == "The Rotted Reliquary")
                       .update(options_from="The Fall"))
        self.assertTrue(any(f.field == "options_from" and "Sealed Reliquary" in f.msg for f in self.design_errors()))

    def test_review6_money_alias_requires_evidence(self):
        for mutate in (lambda a: a.pop("evidence"), lambda a: a.update(evidence=""),
                       lambda a: a.pop("evidence_file"), lambda a: a.update(evidence_file="")):
            with self.subTest(mutate=mutate):
                self.setUp()
                def change(d, mutate=mutate):
                    a = d["picks"]["doc_aliases"][self.PURSE]
                    a.update(money=1)
                    mutate(a)
                self.edit_data(change)
                self.assertTrue(any(f.field == "evidence" for f in self.design_errors()))
                self.tearDown()
        self.setUp()

    def test_missing_never_use_line_is_caught(self):
        self.edit(sc.BIBLE, "- **Never use:**", "- **Avoid:**")
        self.assertTrue(any(f.field == "doc_marker" for f in self.design_errors()))


class Fixtures(unittest.TestCase):
    def test_pass_fixture_has_no_errors(self):
        findings, scanned, io_errors = run([os.path.join(FIX, "pass.json")])
        self.assertEqual(io_errors, [])
        self.assertEqual([str(f) for f in errors(findings)], [])
        # Only pending-id warnings remain (records not created yet, e.g. Galley Stores, the Skyglass Token, the Watch
        # Roster and Crown's Hoard).
        self.assertTrue(all("pending" in f.msg for f in findings), [str(f) for f in findings])

    def test_each_fail_fixture_trips_only_its_check(self):
        for name, check in FAIL.items():
            with self.subTest(fixture=name):
                findings, _, _ = run([os.path.join(FIX, name)])
                errs = errors(findings)
                self.assertTrue(errs, f"{name} produced no error")
                self.assertEqual({f.check for f in errs}, {check}, [str(f) for f in errs])

    def test_specific_failures(self):
        def msgs(name):
            return [f"{f.field} {f.msg}" for f in errors(run([os.path.join(FIX, name)])[0])]
        p = msgs("fail_picks.json")
        self.assertTrue(any("rewardPickCount" in m and "needs 1" in m for m in p))
        self.assertTrue(any("missing option: Chart of the Drowned Foundry" in m for m in p))
        self.assertTrue(any("not in section 4a: 50,000 ryo" in m for m in p))
        self.assertTrue(any("[Low Tide Run] missing option: Medicine Inro" in m for m in p))
        self.assertTrue(any("missing option: 1,000,000 ryo" in m for m in p))
        self.assertTrue(any("not in section 4a: 100,000 ryo" in m for m in p))
        self.assertTrue(any("missing option: Skyglass Coffer ×3" in m for m in p))
        self.assertTrue(any("Elemental Tool Pouch (1% chance)" in m for m in p))
        self.assertTrue(any("reward_rank" in m for m in p))
        self.assertTrue(any("also sends content" in m for m in p) and any("also sends effects" in m for m in p))
        w = msgs("fail_win_only.json")
        self.assertTrue(any("reward_exp=500" in m for m in w))
        self.assertTrue(any("data.effects[0].reward_gathering_items_ids" in m for m in w))
        c = msgs("fail_chest_text.json")
        for want in ("stated 70% but the cache weight is 69%", "'Rare' is coloured #f59e0b", "'Epic' lists 'Sealed Treasury'",
                     "tier line for 'Mythic'", "outside the coloured tier-line format", "but the item has no fixed reward",
                     "needs '<b>Always:</b> 150,000 ryo'", "needs a roll line '3–6 rolls'", "and more'",
                     "same-named tiers share one", "no tier line for 'Legendary'",
                     "does not state 'Medicine Inro'", "states 'Medicine Inro ×99'",
                     "tier name 'Epic' is used by 2 tiers", "'Forbidden' is coloured #f59e0b; the format uses #ef4444",
                     "tier 'Forbidden' (7%) outweighs 'Legendary' (3%)", "'Forbidden 7%: Lastlight Lantern' states a tier rate"):
            self.assertTrue(any(want in m for m in c), (want, c))
        v = msgs("fail_voice.json")
        self.assertTrue(any("'system'" in m for m in v) and any("seven-bladed" in m for m in v)
                        and any("'hunt chart'" in m for m in v))
        t = msgs("fail_chart_tier.json")
        self.assertTrue(any("Rare charts are RARE" in m for m in t) and any("without a rarity" in m for m in t))
        self.assertTrue(any("Lastlight Lantern is EPIC; Legendary charts are LEGENDARY" in m for m in t))
        pc = msgs("fail_prof_chest.json")
        self.assertTrue(any("Epic Hunter's Chest: this run carries no profession drops" in m for m in pc))
        self.assertTrue(any("is not a hunter profession chest" in m for m in pc))
        self.assertTrue(any("is RARE; section 4b sets EPIC" in m for m in pc))
        # Section 4b: the chests need no hunt/gather flags, so the fixture's flags are not an error.
        self.assertFalse(any("canBeHunted" in m or "canBeGathered" in m for m in pc))


class Units(unittest.TestCase):
    def test_pct_text(self):
        self.assertEqual(sc.pct_text(6900), "69")
        self.assertEqual(sc.pct_text(250), "3")      # 2.5 rounds half up
        self.assertEqual(sc.pct_text(10000), "100")
        self.assertEqual(sc.pct_text(50), "1")       # whole percent only (RUL-2026-10-28-030)
        self.assertEqual(sc.pct_text(49), "0")
        self.assertEqual(sc.pct_text(100), "1")

    def test_tier_items_text(self):
        names = {"a": "Alpha", "b": "Beta", "c": "Gamma", "d": "Delta"}
        e = lambda *xs: {"items": [{"itemId": i, "quantity": q} for i, q in xs]}
        self.assertEqual(sc.tier_items_text([e(("a", 1))], names), "Alpha")
        self.assertEqual(sc.tier_items_text([e(("a", 3)), e(("b", 1))], names), "Alpha ×3 or Beta")
        self.assertEqual(sc.tier_items_text([e(("a", 1)), e(("b", 1)), e(("c", 1)), e(("d", 1))], names),
                         "Alpha or Beta or Gamma and more")
        self.assertEqual(sc.tier_items_text([e(("a", 1), ("b", 2))], names), "Alpha + Beta ×2")
        self.assertIsNone(sc.tier_items_text([e(("zz", 1))], names))
        self.assertEqual(sc.norm_items("Alpha <i>or</i> Beta <i>or</i> Gamma, and more"), "Alpha or Beta or Gamma and more")

    def test_fixed_roll_line_is_not_required_and_only_warned(self):
        d = sc.Design(ROOT)
        with open(os.path.join(FIX, "pass.json"), encoding="utf-8") as fh:
            fx = json.load(fh)
        coffer = next(it for it in fx["items"] if it["name"] == "Skyglass Coffer: text")
        self.assertNotIn("roll", coffer["data"]["description"].replace("Each roll", ""))
        coffer["data"]["description"] = coffer["data"]["description"].replace("<br><br>", "<br><i>1 roll.</i><br>", 1)
        ch = sc.Checker(d)
        ch.run("m.json", {"items": [coffer]}, True)
        self.assertEqual([(f.level, f.check) for f in ch.findings], [("WARN", "chest-text")])

    def test_forbidden_tier_line_and_tier_rules(self):
        d = sc.Design(ROOT)
        with open(os.path.join(FIX, "pass.json"), encoding="utf-8") as fh:
            fx = json.load(fh)
        case = next(it for it in fx["items"] if it["name"].startswith("Archive Chart Case"))
        ch = sc.Checker(d)
        ch.run("m.json", {"items": [case]}, True)
        self.assertEqual([str(f) for f in ch.findings], [])   # a red Forbidden 3% line passes
        tiers = case["data"]["effects"][0]["weightedCache"]["tiers"]
        # two tiers with one name (RUL-2026-10-29-058): an error even when the text sums them correctly
        dup = json.loads(json.dumps(case))
        dup["data"]["effects"][0]["weightedCache"]["tiers"] = tiers[:4] + [dict(tiers[3], probability=0)] + [
            dict(tiers[4], name="Legendary")]
        dup["data"]["description"] = dup["data"]["description"].replace(
            '<span style="color:#f59e0b"><b>Legendary 7%</b></span> · Chart of the Buried Cache<br>'
            '<span style="color:#ef4444"><b>Forbidden 3%</b></span> · Lastlight Lantern',
            '<span style="color:#f59e0b"><b>Legendary 10%</b></span> · Chart of the Buried Cache or Lastlight Lantern')
        ch = sc.Checker(d)
        ch.run("m.json", {"items": [dup]}, True)
        self.assertEqual([f.msg for f in errors(ch.findings)],
                         ["tier name 'Legendary' is used by 2 tiers; each name is used once per cache (RUL-2026-10-29-058)"])
        # a higher tier that outweighs a lower one
        heavy = json.loads(json.dumps(case))
        t = heavy["data"]["effects"][0]["weightedCache"]["tiers"]
        t[1]["probability"], t[2]["probability"] = 2000, 2500
        heavy["data"]["description"] = heavy["data"]["description"].replace("Rare 25%", "Rare 20%").replace("Epic 20%", "Epic 25%")
        ch = sc.Checker(d)
        ch.run("m.json", {"items": [heavy]}, True)
        self.assertEqual([f.msg for f in errors(ch.findings)],
                         ["tier 'Epic' (25%) outweighs 'Rare' (20%); tier names follow the order of weight (RUL-2026-10-29-058)"])

    def test_cards_follow_the_engine(self):
        cards, unresolved = sc.reward_cards({
            "reward_money": 10000, "reward_exp": 0, "reward_tokens": 1000,
            "reward_items": [{"ids": ["A", "B", "A"], "number": 5, "quantity": 2}],
            "reward_jutsus": ["J"], "reward_hunter_items": True, "reward_hunter_items_ids": ["H"],
            "reward_packages": [{"id": "p", "name": "P", "rewards": {"reward_money": 10000, "reward_items": [{"ids": ["C"], "quantity": 1}]}},
                                {"id": "q", "name": "empty", "rewards": {}}, {"id": "r"}]})
        self.assertEqual(sorted(cards, key=str), sorted([
            ("money", 10000), ("reward_tokens", 1000), ("item", "A", 2), ("item", "B", 2), ("jutsu", "J"),
            ("package", tuple(sorted([("money", 10000), ("item", "C", 1, 100)], key=str)))], key=str))
        self.assertEqual(unresolved, [{"id": "r"}])

    def test_choice_text_and_ai_rules_scope(self):
        d = sc.Design(ROOT)
        ch = sc.Checker(d)
        ch.run("m.json", {"items": [
            {"entity": "ai", "slot": "edit", "targetId": "x", "data": {"username": "Crown Echo",
             "rules": [{"action": {"description": "Select specific jutsu unit"}}]}},
            {"entity": "quest", "slot": "edit", "targetId": "y", "data": {"content": {"objectives": [
                {"id": "d_conduit", "task": "dialog", "description": "ok", "nextObjectiveId": [{"text": "Scan the deck", "nextObjectiveId": "n"}]}]}}},
        ]}, True)
        voice = [f for f in ch.findings if f.check == "voice"]
        self.assertEqual(len(voice), 1, [str(f) for f in voice])   # the choice text; not the node id, not AI rule text
        self.assertIn("'scan'", voice[0].msg)

    def test_non_skyglass_manifest_only_gets_the_pool_check(self):
        d = sc.Design(ROOT)
        ch = sc.Checker(d)
        ch.run("m.json", {"items": [{"entity": "item", "slot": "edit", "targetId": "z", "data": {
            "description": "a system", "effects": [{"reward_hunter_items": True, "reward_hunter_items_ids": []}]}}]}, False)
        self.assertEqual([f.check for f in ch.findings], ["win-only"])


class ReviewRegressions(unittest.TestCase):
    """REQUEST CHANGES on b1e7527b: one regression per finding."""
    POUCH, INRO = "D0gtI5dOgj2dFO4VexsLJ", "ixEKlJ0MmDrX7JoMNJVhi"

    def findings(self, items, package_run=False):
        d = sc.Design(ROOT)
        if package_run:
            # No section 4a run offers a package card any more (RUL-2026-10-28-034 cut the +10,000 ryo packages), but the
            # package comparison is engine logic: pin it on a synthetic Low Tide Run of two Pouch/Inro + 10,000 ryo packages.
            d.runs["Low Tide Run"] = dict(d.runs["Low Tide Run"], options=[
                {"package": [{"item": "elemental_tool_pouch", "quantity": 1}, {"money": 10000}]},
                {"package": [{"item": "medicine_inro", "quantity": 1}, {"money": 10000}]}])
        ch = sc.Checker(d)
        ch.run("m.json", {"items": items}, True)
        return ch.findings

    def low_tide(self, packages):
        return {"entity": "quest", "slot": "create", "srcId": "lt", "name": "lt", "data": {"name": "The Low Tide Run",
                "content": {"rewardMode": "choose", "rewardPickCount": 1, "reward": {"reward_packages": packages}}}}

    def pkg(self, item, number=100, **extra):
        return {"id": item, "name": item, "rewards": {"reward_money": 10000, **extra,
                "reward_items": [{"ids": [item], "number": number, "quantity": 1}]}}

    def test_finding1_package_drop_chance_and_structural_fields_count(self):
        ok = self.findings([self.low_tide([self.pkg(self.POUCH), self.pkg(self.INRO)])], package_run=True)
        self.assertEqual([str(f) for f in errors(ok)], [])
        # against the real section 4a Low Tide Run (plain cards), the packages are not options
        real = [f for f in errors(self.findings([self.low_tide([self.pkg(self.POUCH), self.pkg(self.INRO)])])) if f.check == "picks"]
        self.assertTrue(any("not in section 4a: package" in f.msg for f in real), [str(f) for f in real])
        for bad in ([self.pkg(self.POUCH, number=1), self.pkg(self.INRO, number=1)],
                    [self.pkg(self.POUCH, reward_hunter_items=True, reward_hunter_items_ids=["x"]), self.pkg(self.INRO)],
                    [self.pkg(self.POUCH, reward_rank="JONIN"), self.pkg(self.INRO)],
                    [self.pkg(self.POUCH, reward_exp=1), self.pkg(self.INRO)]):
            with self.subTest(bad=bad[0]["rewards"]):
                errs = [f for f in errors(self.findings([self.low_tide(bad)], package_run=True)) if f.check == "picks"]
                self.assertTrue(any("missing option: package" in f.msg for f in errs), [str(f) for f in errs])

    def test_finding1_direct_cards_unchanged(self):
        q = {"entity": "quest", "slot": "edit", "targetId": "UGHSuhi83C3wRtH3FD4Eu", "data": {"content": {
             "rewardMode": "choose", "reward": {"reward_items": [{"ids": [self.POUCH], "number": 5, "quantity": 1},
                                                                 {"ids": [self.INRO], "number": 5, "quantity": 1}]}}}}
        self.assertEqual([str(f) for f in errors(self.findings([q]))], [])

    def test_finding2_retired_records_may_only_be_hidden(self):
        hide_q = {"entity": "quest", "slot": "edit", "targetId": "3BYr-HMkOepywS77vJvJh", "data": {"hidden": True}}
        hide_i = {"entity": "item", "slot": "edit", "targetId": "Fz1MU04kLIIM0EMXgouo6", "data": {"hidden": True}}
        self.assertEqual([str(f) for f in errors(self.findings([hide_q, hide_i]))], [])
        pay_q = {**hide_q, "data": {"hidden": True, "content": {"objectives": [
            {"id": "w", "task": "win_quest", "reward_money": 100000}]}}}
        pay_i = {**hide_i, "data": {"hidden": True, "effects": [
            {"type": "noncombatconsumereward", "rewardMode": "standard", "reward_money": 100000}]}}
        rename = {**hide_i, "data": {"hidden": True, "name": "Armory Requisition II"}}
        create = {**hide_q, "slot": "convert"}
        for bad in (pay_q, pay_i, rename, create):
            with self.subTest(bad=bad["data"]):
                self.assertTrue(errors(self.findings([bad])))

    def kit(self, always, fixed_items=(), money=0):
        return {"entity": "item", "slot": "edit", "targetId": "kit", "data": {
            "description": (f"<b>Always:</b> {always}<br>" if always is not None else "")
            + '<span style="color:#9ca3af"><b>Common 100%</b></span> · Skyglass Coffer',
            "effects": [{"type": "noncombatconsumereward", "rewardMode": "standard", "reward_money": money,
                         "reward_items": [{"ids": [i], "number": 100, "quantity": q} for i, q in fixed_items]},
                        {"type": "noncombatconsumereward", "rewardMode": "weightedCache", "weightedCache": {
                            "rolls": [{"count": 1, "probability": 10000}],
                            "tiers": [{"name": "Common", "probability": 10000,
                                       "entries": [{"items": [{"itemId": "THo7rfzP-S82_43aN8fs3", "quantity": 1}]}]}]}}]}}

    def test_finding3_always_line_compares_whole_entries(self):
        good = self.kit("150,000 ryo · Medicine Inro ×2", [(self.INRO, 2)], 150000)
        self.assertEqual([str(f) for f in errors(self.findings([good]))], [])
        for always, fixed, money in (("Medicine Inro ×99", [(self.INRO, 1)], 0),   # wrong quantity
                                     ("Medicine Inro ×1", [(self.INRO, 1)], 0),    # ×1 is not shown
                                     ("Medicine Inro · 5,000 ryo", [(self.INRO, 1)], 0),  # extra entry
                                     ("1,500,000 ryo", [], 150000),                # amount that contains the right one
                                     ("150,000 ryo", [(self.INRO, 1)], 150000)):   # missing entry
            with self.subTest(always=always):
                errs = [f for f in errors(self.findings([self.kit(always, fixed, money)])) if f.check == "chest-text"]
                self.assertTrue(errs)


class Cli(unittest.TestCase):
    def call(self, argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = sc.main(argv)
        return code, out.getvalue()

    def test_exit_codes(self):
        self.assertEqual(self.call([os.path.join(FIX, "pass.json")])[0], 0)
        self.assertEqual(self.call([os.path.join(FIX, "fail_voice.json")])[0], 1)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write("{not json")
        try:
            self.assertEqual(self.call([fh.name])[0], 2)
        finally:
            os.unlink(fh.name)

    def test_json_output(self):
        code, out = self.call(["--json", os.path.join(FIX, "fail_chart_tier.json")])
        doc = json.loads(out)
        self.assertEqual(code, 1)
        self.assertEqual(doc["errors"], 3)
        self.assertEqual({f["check"] for f in doc["findings"]}, {"chart-tier"})


if __name__ == "__main__":
    unittest.main()
