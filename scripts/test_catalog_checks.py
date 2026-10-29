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


    def test_r1_url_parity_with_forge(self):
        # (url, Forge's url() on Node — http(s), no whitespace, new URL() parses — recorded 2026-10-29, Python's
        # expected result). Python accepts a conservative subset (catalog_checks.py): where the two differ, Python
        # must be the one refusing. Review rounds 2-3 found looser cases; each is listed here.
        sys.path.insert(0, str(ROOT / "skills" / "building-tnr-content" / "scripts"))
        from catalog_checks import _url
        cases = [
            ("https://example.com:99999/a.png", False, False),
            ("https://example.com:bad/a.png", False, False),
            ("https://exa%mple.com/a.png", False, False),
            ("https://[", False, False),
            ("https://[::1]/a.png", True, True),
            ("https://[zz]/a.png", False, False),
            ("https://example.com:65535/a.png", True, True),
            ("https://example.com:/a.png", True, True),
            ("https://utfs.io/f/abc", True, True),
            ("http://a.b/c?d=e#f", True, True),
            ("https://user:pw@host.com/x", True, False),
            ("https://ho|st.com/x", False, False),
            ("https://ho^st.com/x", False, False),
            ("https://host.com:0/x", True, True),
            ("https:///x", True, False),
            ("https://example.com:-1/a", False, False),
            ("https://256.1.1.1/a.png", False, False),
            ("https://[fe80::1%25eth0]/a.png", False, False),
            ("https://\u200d.com/a.png", False, False),
            ("https://1.2.3.4/a", True, True),
            ("https://1.2.3.4:8080/a", True, True),
            ("https://example.123/a", False, False),
            ("https://a..b/x", True, False),
            ("https://example.com./x", True, True),
            ("https://ex_ample.com/x", True, True),
            ("https://-a.com/x", True, True),
            ("https://xn--nxasmq6b.com/x", True, False),
            ("https://ex\u00e4mple.com/x", True, False),
            ("https://[::ffff:1.2.3.4]/x", True, True),
            ("https://0x7f.0.0.1/x", True, False),
            ("https://1.2.3/x", True, False),
            ("https://EXAMPLE.COM/X", True, True),
            ("https://ex*ample.com/x", True, False),
            ("https://ex!ample.com/x", True, False),
            ("https://ex$ample.com/x", True, False),
            ("https://localhost/x", True, True),
            ("https://a.b.c.d.e/x", True, True),
            ("https://[::1]:443/x", True, True),
            ("https://u@[::1]/x", True, False),
            ("https://xn--a.com/a.png", False, False),
            ("https://bad^host\\@example.com/a.png", False, False),
            ("https://xn--nxasmq6b.com/a.png", True, False),
            ("https://example.com\\a.png", True, False),
            ("https://example.com?x", True, True),
            ("https://example.com", True, True),
            ("https://0.0.0.0/a", True, True),
            ("https://4294967295/a", True, False),
        ]
        for v, node, py in cases:
            self.assertEqual(_url(v), py, v)
            if py:
                self.assertTrue(node, f"Python accepts what Forge refuses: {v!r}")
        for v in ("https://example.com:99999/a.png", "https://256.1.1.1/a.png", "https://[fe80::1%25eth0]/a.png",
                  "https://\u200d.com/a.png", "https://xn--a.com/a.png", "https://bad^host\\@example.com/a.png"):
            code, out = self.validate("badge", {**BADGE, "image": v})
            self.assertNotEqual(code, 0, v)


if __name__ == "__main__":
    unittest.main()
