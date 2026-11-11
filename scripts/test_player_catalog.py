#!/usr/bin/env python3
"""The player's record catalogue holds no hidden record (RUL-2026-11-11-149: "Do not use hidden records, treat them
like they are actually hidden"). Socket-free; temporary trees only, plus one read-only build check of the catalogue.

    python3 -m unittest scripts/test_player_catalog.py -v
"""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "harness", "pvp_turn", "tools")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(TOOLS, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def jutsu(i, hidden, at="2026-11-01"):
    return {"id": i, "name": i, "jutsuType": "NORMAL", "effects": [{"type": "damage"}], "hidden": hidden, "updatedAt": at}


class HiddenRecords(unittest.TestCase):
    def build(self, harvest, records=None, patches=()):
        bc = load("build_catalog")
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "harvests", "inbox"))
            kit = os.path.join(d, "kit")
            os.makedirs(kit)
            with open(os.path.join(d, "harvests", "inbox", "c.json"), "w") as f:
                json.dump(harvest, f)
            if records is not None:
                with open(os.path.join(kit, "records.json"), "w") as f:
                    json.dump(records, f)
            if patches:
                with open(os.path.join(kit, "live_jutsu_2026-11-11.jsonl"), "w") as f:
                    f.write("\n".join(json.dumps(p) for p in patches) + "\n")
            with contextlib.redirect_stdout(io.StringIO()):
                out = bc.build(repo=d, kit=kit)
            with open(os.path.join(kit, "bloodlines.json")) as f:
                bls = json.load(f)
            with open(os.path.join(kit, "catalog.json")) as f:
                self.assertEqual(set(json.load(f)), set(out))
        return out, bls

    def test_a_hidden_record_never_reaches_the_catalogue(self):
        harvest = {"captures": [{"data": {"data": [
            jutsu("seen", False), jutsu("secret", True),
            {"id": "blade", "name": "Blade", "itemType": "WEAPON", "effects": [], "hidden": True},
            {"id": "pill", "name": "Pill", "itemType": "CONSUMABLE", "effects": [], "hidden": False},
            {"id": "bl_open", "name": "Open", "rank": "A", "regenIncrease": 1, "effects": [], "hidden": False},
            {"id": "bl_shut", "name": "Shut", "rank": "S", "regenIncrease": 1, "effects": [], "hidden": True}]}}]}
        out, bls = self.build(harvest)
        self.assertEqual(set(out), {"seen", "pill"})
        self.assertEqual(set(bls), {"bl_open"})

    def test_no_later_layer_brings_one_back(self):
        harvest = {"rows": [jutsu("seen", False), jutsu("secret", True)]}
        records = {"curated": {"record": jutsu("curated", True, "2026-11-10"), "source": "connector read",
                               "updatedAt": "2026-11-10"}}
        patch = {"id": "secret", "updatedAt": "2026-11-11", "effects": [{"type": "stun"}], "range": 4}
        out, _ = self.build(harvest, records, [patch])
        self.assertEqual(set(out), {"seen"})

    def test_a_record_published_later_is_in(self):
        harvest = {"rows": [jutsu("event", True, "2026-10-01"), jutsu("event", False, "2026-11-05")]}
        out, _ = self.build(harvest)
        self.assertEqual(set(out), {"event"})

    def test_the_fetch_tool_asks_for_no_hidden_record(self):
        fc = load("fetch_catalog")
        self.assertTrue(fc.PULLS)
        for name, proc, base, limit in fc.PULLS:
            self.assertIsNot(base.get("hidden"), True, name)

    def test_add_record_refuses_a_hidden_record(self):
        tool = os.path.join(ROOT, "state", "player", "dauntless", "tools", "add_record.py")
        path = os.path.join(ROOT, "harness", "pvp_turn", "kit", "records.json")
        with open(path) as f:
            before = f.read()
        r = subprocess.run([sys.executable, tool], input=json.dumps(jutsu("secret", True)), capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("hidden", r.stderr)
        with open(path) as f:
            self.assertEqual(f.read(), before)

    def test_the_committed_sources_hold_no_hidden_curated_record_or_hidden_pull(self):
        with open(os.path.join(ROOT, "harness", "pvp_turn", "kit", "records.json")) as f:
            for i, v in json.load(f).items():
                if not i.startswith("_"):
                    self.assertFalse(v["record"].get("hidden"), i)
        with open(os.path.join(ROOT, "harvests", "inbox", "tnr_results_1794368544997.json")) as f:
            cap = json.load(f)
        self.assertTrue(all(c["input"].get("hidden") is not True for c in cap["captures"]))
        self.assertFalse(any(r.get("hidden") for c in cap["captures"] for r in c["data"].get("data", [])))


if __name__ == "__main__":
    unittest.main()
