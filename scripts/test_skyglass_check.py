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
        words = [w for w, _ in sc.Design(ROOT).banned]
        for w in ("system", "network", "lattice", "conduit", "lift", "unit", "seven-bladed"):
            self.assertIn(w, words)


class TempRoot(unittest.TestCase):
    """A copy of just the files the design check reads, so a doc edit can be simulated."""
    FILES = [sc.DESIGN, sc.LOOT, sc.BIBLE, sc.RULINGS, sc.NAMES, "state/crownhold/ids.json",
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
        self.edit(sc.LOOT, "| Buried Cache | 25,000 ryo / Medicine Inro / Galley Stores |",
                  "| Buried Cache | 30,000 ryo / Medicine Inro / Galley Stores |")
        msgs = [f.msg for f in self.design_errors()]
        self.assertTrue(any("section 4a now reads" in m and "30,000" in m for m in msgs), msgs)

    def test_new_doc_row_is_caught(self):
        self.edit(sc.LOOT, "| Crownhold | Crown's Hoard", "| Proving Ground | Skyglass Coffer |\n| Crownhold | Crown's Hoard")
        msgs = [f.msg for f in self.design_errors()]
        self.assertTrue(any("'Proving Ground' has no entry" in m for m in msgs), msgs)

    def test_pick_rule_change_is_caught(self):
        self.edit(sc.LOOT, "**Pick 1 on every run; tainted runs pick 2.**", "**Pick 2 on every run.**")
        self.assertTrue(any(f.field == "doc_rule" for f in self.design_errors()))

    def test_chart_tier_row_change_is_caught(self):
        self.edit(sc.RULINGS, "| Hunt charts | Rare | cyan |", "| Hunt charts | Epic | cyan |")
        self.assertTrue(any("Hunt charts" in f.msg for f in self.design_errors()))

    def test_id_missing_from_its_source_is_caught(self):
        self.edit("push/elemental_pouch.gen.py", "D0gtI5dOgj2dFO4VexsLJ", "somethingelse", count=-1)
        self.assertTrue(any("D0gtI5dOgj2dFO4VexsLJ" in f.msg for f in self.design_errors()))

    def test_badge_resolves_from_ids_file_when_it_exists(self):
        self.assertIsNone(sc.Design(self.tmp).ids["crownhold_badge"])
        p = os.path.join(self.tmp, "state/crownhold/ids.json")
        with open(p, encoding="utf-8") as fh:
            ids = json.load(fh)
        ids["badge:crownbreaker"] = "BADGE123"
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(ids, fh)
        self.assertEqual(sc.Design(self.tmp).ids["crownhold_badge"], "BADGE123")

    def test_missing_never_use_line_is_caught(self):
        self.edit(sc.BIBLE, "- **Never use:**", "- **Avoid:**")
        self.assertTrue(any(f.field == "doc_marker" for f in self.design_errors()))


class Fixtures(unittest.TestCase):
    def test_pass_fixture_has_no_errors(self):
        findings, scanned, io_errors = run([os.path.join(FIX, "pass.json")])
        self.assertEqual(io_errors, [])
        self.assertEqual([str(f) for f in errors(findings)], [])
        # Only pending-id warnings remain (Galley Stores and Echo Jar are not created yet).
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
        self.assertTrue(any("missing option: 25,000 ryo" in m for m in p))
        self.assertTrue(any("not in section 4a: 50,000 ryo" in m for m in p))
        w = msgs("fail_win_only.json")
        self.assertTrue(any("reward_exp=500" in m for m in w))
        self.assertTrue(any("data.effects[0].reward_gathering_items_ids" in m for m in w))
        c = msgs("fail_chest_text.json")
        self.assertTrue(any("stated 70% but the cache weight is 69%" in m for m in c))
        self.assertTrue(any("Mythic 1%" in m for m in c))
        self.assertTrue(any("150,000 ryo" in m for m in c))
        self.assertTrue(any("'3 rolls 60%'" in m for m in c))
        v = msgs("fail_voice.json")
        self.assertTrue(any("'system'" in m for m in v) and any("seven-bladed" in m for m in v))
        t = msgs("fail_chart_tier.json")
        self.assertTrue(any("Hunt charts are RARE" in m for m in t) and any("without a rarity" in m for m in t))
        pc = msgs("fail_prof_chest.json")
        self.assertTrue(any("outside the area's tier (Rare)" in m for m in pc))
        self.assertTrue(any("is not a hunter profession chest" in m for m in pc))
        self.assertTrue(any("canBeHunted=false" in m for m in pc))


class Units(unittest.TestCase):
    def test_pct_text(self):
        self.assertEqual(sc.pct_text(6900), "69")
        self.assertEqual(sc.pct_text(250), "3")      # 2.5 rounds half up
        self.assertEqual(sc.pct_text(10000), "100")
        self.assertEqual(sc.pct_text(50), "0.5")
        self.assertEqual(sc.pct_text(100), "1")

    def test_cards_follow_the_engine(self):
        cards, unresolved = sc.reward_cards({
            "reward_money": 10000, "reward_exp": 0, "reward_tokens": 1000,
            "reward_items": [{"ids": ["A", "B", "A"], "number": 5, "quantity": 2}],
            "reward_jutsus": ["J"], "reward_hunter_items": True, "reward_hunter_items_ids": ["H"],
            "reward_packages": [{"id": "p", "name": "P", "rewards": {"reward_money": 10000, "reward_items": [{"ids": ["C"], "quantity": 1}]}},
                                {"id": "q", "name": "empty", "rewards": {}}, {"id": "r"}]})
        self.assertEqual(sorted(cards, key=str), sorted([
            ("money", 10000), ("reward_tokens", 1000), ("item", "A", 2), ("item", "B", 2), ("jutsu", "J"),
            ("package", tuple(sorted([("money", 10000), ("item", "C", 1)])))], key=str))
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
        self.assertEqual(doc["errors"], 2)
        self.assertEqual({f["check"] for f in doc["findings"]}, {"chart-tier"})


if __name__ == "__main__":
    unittest.main()
