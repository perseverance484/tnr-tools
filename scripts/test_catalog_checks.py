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
        # (url, Forge's url() on Node: http(s), no whitespace, new URL() parses). Node results recorded 2026-10-29.
        # Python may be stricter (a conservative host subset: no IDNA, dotted-decimal IPv4 only, no empty labels,
        # no sub-delims) but must never accept a URL Forge refuses. A 35,000-case random fuzz found no looser case.
        sys.path.insert(0, str(ROOT / "skills" / "building-tnr-content" / "scripts"))
        from catalog_checks import _url
        cases = [
            ("https://example.com:99999/a.png", False),
            ("https://example.com:bad/a.png", False),
            ("https://exa%mple.com/a.png", False),
            ("https://[", False),
            ("https://[::1]/a.png", True),
            ("https://[zz]/a.png", False),
            ("https://example.com:65535/a.png", True),
            ("https://example.com:/a.png", True),
            ("https://utfs.io/f/abc", True),
            ("http://a.b/c?d=e#f", True),
            ("https://user:pw@host.com/x", True),
            ("https://ho|st.com/x", False),
            ("https://ho^st.com/x", False),
            ("https://host.com:0/x", True),
            ("https:///x", True),
            ("https://example.com:-1/a", False),
            ("https://256.1.1.1/a.png", False),
            ("https://[fe80::1%25eth0]/a.png", False),
            ("https://\u200d.com/a.png", False),
            ("https://1.2.3.4/a", True),
            ("https://1.2.3.4:8080/a", True),
            ("https://example.123/a", False),
            ("https://a..b/x", True),
            ("https://example.com./x", True),
            ("https://ex_ample.com/x", True),
            ("https://-a.com/x", True),
            ("https://xn--nxasmq6b.com/x", True),
            ("https://ex\u00e4mple.com/x", True),
            ("https://[::ffff:1.2.3.4]/x", True),
            ("https://0x7f.0.0.1/x", True),
            ("https://1.2.3/x", True),
            ("https://EXAMPLE.COM/X", True),
            ("https://ex*ample.com/x", True),
            ("https://ex!ample.com/x", True),
            ("https://ex$ample.com/x", True),
            ("https://localhost/x", True),
            ("https://a.b.c.d.e/x", True),
            ("https://[::1]:443/x", True),
            ("https://u@[::1]/x", True),
        ]
        stricter = {"https:///x", "https://a..b/x", "https://exämple.com/x", "https://0x7f.0.0.1/x", "https://1.2.3/x",
                    "https://ex*ample.com/x", "https://ex!ample.com/x", "https://ex$ample.com/x"}
        for v, node in cases:
            got = _url(v)
            if got:
                self.assertTrue(node, f"Python accepts what Forge refuses: {v!r}")
            self.assertEqual(got, node and v not in stricter, v)
        for v in ("https://example.com:99999/a.png", "https://256.1.1.1/a.png", "https://[fe80::1%25eth0]/a.png",
                  "https://‍.com/a.png"):
            code, out = self.validate("badge", {**BADGE, "image": v})
            self.assertNotEqual(code, 0, v)


if __name__ == "__main__":
    unittest.main()
