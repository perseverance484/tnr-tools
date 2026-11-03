#!/usr/bin/env python3
"""Socket-free tests for item_icon_batch.py (Pillow required)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import item_icon_batch as batch


class ItemIconBatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.wave = self.write("wave.json", {
            "wave": "W01 Elemental Kunai", "family": "elemental-kunai",
            "items": [{"id": "a1", "name": "Ikazuchi Kunai"},
                      {"id": "a2", "name": "Katon Kunai"}],
            "context": [{"id": "a3", "name": "Bloodthorn Kunai"}]})
        self.bundle = self.write("capture.json", {
            "cfg": "forge", "outcome": "success", "state": "DONE", "entries": [],
            "at": "2026-10-25T12:00:00Z",
            "captures": [self.cap("a1", "Ikazuchi Kunai", "https://example.invalid/i.webp"),
                         self.cap("a3", "Bloodthorn Kunai", "https://example.invalid/b.webp")]})

    def write(self, name, data):
        p = self.root / name
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    @staticmethod
    def cap(ident, name, image):
        return {"proc": "item.get", "input": {"id": ident}, "ok": True,
                "persistOk": True, "snapshotKey": "captured::" + ident,
                "at": "2026-10-25T11:59:00Z",
                "data": {"id": ident, "name": name, "image": image,
                         "itemType": "WEAPON", "rarity": "EPIC", "slot": "HAND"}}

    def test_capture_and_missing_statuses(self):
        roster = batch.make_roster(self.wave, [self.bundle])
        self.assertEqual([r["status"] for r in roster["rows"]],
                         ["CAPTURED", "CAPTURE_MISSING", "CAPTURED"])
        self.assertEqual(roster["rows"][0]["image_url"], "https://example.invalid/i.webp")
        self.assertEqual(roster["rows"][0]["snapshot_key"], "captured::a1")
        self.assertEqual(roster["rows"][0]["source_sha256"], batch.digest(self.bundle))
        self.assertIsNone(roster["rows"][1]["image_url"])
        self.assertEqual(roster["rows"][2]["role"], "context")
        batch.save_roster(roster, self.root / "out")
        self.assertIn("CAPTURE_MISSING", (self.root / "out/roster.csv").read_text())
        self.assertEqual(json.loads((self.root / "out/roster.json").read_text()), roster)

    def test_draft_without_captures(self):
        roster = batch.make_roster(self.wave, [])
        self.assertTrue(all(r["status"] == "CAPTURE_MISSING" for r in roster["rows"]))

    def test_rejects_art_index_and_columnar_seed(self):
        cases = [
            ("art.json", {"counts": {"assets": 3}, "assets": [{"type": "STATIC"}]}),
            ("seed.json", {"cols": ["id", "n"], "rows": [["a1", "Ikazuchi Kunai"]]})]
        for name, data in cases:
            with self.subTest(name=name), self.assertRaises(ValueError):
                batch.make_roster(self.wave, [self.write(name, data)])

    def test_failed_and_mismatched_capture_rejected(self):
        bad = json.loads(self.bundle.read_text())
        bad["captures"][0]["input"]["id"] = "wrong"
        with self.assertRaisesRegex(ValueError, "mismatched"):
            batch.make_roster(self.wave, [self.write("mismatch.json", bad)])
        bad = json.loads(self.bundle.read_text())
        bad["outcome"] = "unverified"
        with self.assertRaisesRegex(ValueError, "DONE/success"):
            batch.make_roster(self.wave, [self.write("unverified.json", bad)])

    def test_conflict_and_name_mismatch_not_autoselected(self):
        later = self.write("later.json", {
            "cfg": "forge", "outcome": "success", "state": "DONE",
            "captures": [self.cap("a1", "Ikazuchi Kunai", "https://example.invalid/changed.webp")]})
        row = batch.make_roster(self.wave, [self.bundle, later])["rows"][0]
        self.assertEqual(row["status"], "CONFLICT")
        self.assertIsNone(row["image_url"])
        rename = self.write("rename.json", {
            "captures": [self.cap("a1", "Other Kunai", "https://example.invalid/i.webp")]})
        row = batch.make_roster(self.wave, [rename])["rows"][0]
        self.assertEqual(row["status"], "NAME_MISMATCH")

    def test_local_list_not_promoted_to_verified_capture(self):
        p = self.write("local.json", [{"id": "a2", "name": "Katon Kunai",
                                       "image": "https://example.invalid/k.webp"}])
        self.assertEqual(batch.make_roster(self.wave, [p])["rows"][1]["status"], "LOCAL_RECORD")

    def test_contact_sheet_deterministic_and_draft_when_incomplete(self):
        batch.save_roster(batch.make_roster(self.wave, [self.bundle]), self.root / "out")
        art = self.root / "original.png"
        Image.new("RGBA", (256, 256), (12, 230, 73, 180)).save(art)
        mapping = self.write("map.json", {
            "a1": {"path": str(art), "sha256": batch.digest(art)}, "a3": str(art)})
        output = self.root / "contact.png"
        first = batch.make_sheet(self.root / "out/roster.json", mapping, output)
        self.assertEqual(first["status"], "DRAFT_INCOMPLETE")
        self.assertEqual([x["status"] for x in first["images"]],
                         ["PRESENT", "MISSING", "PRESENT"])
        self.assertEqual(first["sheet_sha256"],
                         batch.make_sheet(self.root / "out/roster.json", mapping, output)["sheet_sha256"])
        self.assertTrue(output.with_suffix(".json").is_file())

    def test_contact_sheet_hash_mismatch(self):
        batch.save_roster(batch.make_roster(self.wave, [self.bundle]), self.root / "out")
        art = self.root / "original.png"
        Image.new("RGBA", (32, 32), "red").save(art)
        mapping = self.write("map.json", {"a1": {"path": str(art), "sha256": "deadbeef"}})
        r = batch.make_sheet(self.root / "out/roster.json", mapping, self.root / "bad.png")
        self.assertEqual(r["images"][0]["status"], "HASH_MISMATCH")

    def test_cli_require_complete_returns_two(self):
        r = subprocess.run([
            sys.executable, str(Path(batch.__file__)), "roster", "--wave", str(self.wave),
            "--capture", str(self.bundle), "--out", str(self.root / "cli"),
            "--require-complete"], capture_output=True, text=True, check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("CAPTURE_MISSING", r.stdout)


if __name__ == "__main__":
    unittest.main()
