#!/usr/bin/env python3
"""validate.py's badge/title checks (catalog_checks.py), review round 1 of the badge/title builder.

    python3 -m unittest scripts/test_catalog_checks.py -v

Synthetic manifests in a temp dir; no game checkout, no network. Forge's side is
forge/test/catalog.test.mjs.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "skills" / "building-tnr-content" / "data"

BADGE = {"name": "Fixture Crest", "image": "https://utfs.io/f/fixture-crest", "description": "A test badge.", "hidden": True}
TITLE = {"name": "Fixture Warden", "archived": False, "hidden": True}


class CatalogChecks(unittest.TestCase):
    def validate(self, entity, data, raw=None):
        item = {"entity": entity, "slot": "create", "name": (data or {}).get("name", "Fixture"), "srcId": "fx_one", "data": data}
        text = json.dumps({"items": [item]}) if raw is None else raw
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write(text)
        try:
            r = subprocess.run([sys.executable, "../scripts/validate.py", "--strict", f.name],
                               cwd=DATA, capture_output=True, text=True)
        finally:
            Path(f.name).unlink()
        return r.returncode, r.stdout + r.stderr

    def test_baselines_pass(self):
        for entity, data in (("badge", BADGE), ("title", {**TITLE, "description": "d", "effects": []})):
            code, out = self.validate(entity, data)
            self.assertEqual(code, 0, out)

    def test_f1_malformed_badge_url_is_refused(self):
        for bad in ("https://[", "https://", "https://exa mple.com/a.png"):
            code, out = self.validate("badge", {**BADGE, "image": bad})
            self.assertNotEqual(code, 0, bad)
            self.assertIn("image must be an @img ref or an absolute URL", out, bad)

    def test_f2_padded_names_are_refused(self):
        for entity, base in (("badge", BADGE), ("title", TITLE)):
            for bad in (" Crest", "Crest ", "Crest\n"):
                code, out = self.validate(entity, {**base, "name": bad})
                self.assertNotEqual(code, 0, (entity, bad))
                self.assertIn("leading or trailing whitespace", out)

    def test_f3_minimal_title_create_matches_forge(self):
        code, out = self.validate("title", TITLE)
        self.assertEqual(code, 0, out)
        code, out = self.validate("title", {"name": "Fixture Warden", "hidden": True})
        self.assertNotEqual(code, 0)
        self.assertIn("archived is required on a title create", out)
        for k in ("name", "image", "description"):
            code, out = self.validate("badge", {x: v for x, v in BADGE.items() if x != k})
            self.assertIn(f"{k} is required on a badge create", out)

    def test_f4_nonfinite_title_power_is_refused(self):
        item = {"entity": "title", "slot": "create", "name": TITLE["name"], "srcId": "fx_one",
                "data": {**TITLE, "effects": [{"type": "increaseregeneration", "power": "POWER"}]}}
        raw = json.dumps({"items": [item]}).replace('"POWER"', "1e309")
        code, out = self.validate("title", None, raw=raw)
        self.assertNotEqual(code, 0)
        self.assertIn("power must be finite and >= 0", out)


if __name__ == "__main__":
    unittest.main()
