#!/usr/bin/env python3
"""Tests for scripts/jutsu_art.py. Socket-free: materialize is exercised with an injected fetcher.

    python3 -m unittest scripts/test_jutsu_art.py -v
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jutsu_art as ja  # noqa: E402

ROOT = ja.ROOT
WEBP = b"RIFF\x10\x00\x00\x00WEBPVP8 " + b"\x00" * 16


def _source_paths() -> list[str]:
    s = ja.SOURCES
    paths = [s["coverage"]["bundle"], s["target"]["bundle"], s["target"]["manifest"],
             s["known_names"]["catalog"], s["known_names"]["hot"]]
    for b in s["batches"]:
        paths += [b["manifest"], b["bundle"]]
    return paths


class TempRepo:
    """A scratch copy of exactly the pinned sources, so tamper tests never touch the checkout."""

    def __enter__(self) -> Path:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        for rel in _source_paths():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, root / rel)
        return root

    def __exit__(self, *exc):
        self.tmp.cleanup()

    @staticmethod
    def edit(root: Path, rel: str, fn) -> None:
        p = root / rel
        d = json.loads(p.read_text(encoding="utf-8"))
        fn(d)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def run(argv, root=ROOT):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = ja.main(argv, root=root)
    return rc, out.getvalue(), err.getvalue()


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc, cls.text = ja.build(ROOT)

    def test_expected_counts(self):
        c = self.doc["counts"]
        self.assertEqual((c["captured"], c["eligible"], c["eligible_unique_image_urls"]), (604, 441, 440))

    def test_committed_output_is_current(self):
        self.assertEqual((ROOT / ja.OUTPUT).read_text(encoding="utf-8"), self.text)

    def test_drift_warning_preserved(self):
        cov = self.doc["coverage"]
        self.assertEqual((cov["live_name_rows"], cov["known_name_rows"], cov["status"]), (1493, 1491, "UNRESOLVED"))
        self.assertTrue(any("UNRESOLVED" in w for w in self.doc["warnings"]))

    def test_deterministic(self):
        self.assertEqual(ja.build(ROOT)[1], self.text)

    def test_one_shared_image(self):
        self.assertEqual(len(self.doc["shared_images"]), 1)
        self.assertEqual(len(self.doc["shared_images"][0]["ids"]), 2)

    def test_manifest_hash_matches_forge(self):
        for b in ja.SOURCES["batches"]:
            m = json.loads((ROOT / b["manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(ja.manifest_hash(m), b["manifest_hash"], b["manifest"])

    def test_exclusion_reasons(self):
        reasons = {e for r in self.doc["records"] for e in r["exclusions"]}
        self.assertTrue({"hidden", "jutsuType=AI", "bloodline-owned"} <= reasons, reasons)


class LookupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = ja.load_derived(ROOT)

    def test_normalized_exact(self):
        # stored with a double space; curly vs straight apostrophes fold together
        self.assertEqual(ja.resolve(self.doc, "  crescent REAPER fang ")["id"], "cjRErpuffG4GiwIU8OsCw")
        a = ja.resolve(self.doc, "Amaterasu's Renewal")
        self.assertEqual(ja.resolve(self.doc, "Amaterasu’s Renewal")["id"], a["id"])

    def test_miss_suggests_but_never_selects(self):
        with self.assertRaises(ja.LookupMiss) as cm:
            ja.resolve(self.doc, "Crescent Reaper")
        self.assertIn("Crescent  Reaper Fang", cm.exception.suggestions)
        rc, out, err = run(["image-url", "Crescent Reaper"])
        self.assertEqual((rc, out), (1, ""))
        self.assertIn("did you mean", err)
        self.assertIn("UNRESOLVED", err)

    def test_by_id(self):
        self.assertEqual(ja.resolve(self.doc, "cjRErpuffG4GiwIU8OsCw", by_id=True)["name"], "Crescent  Reaper Fang")

    def test_image_url_refuses_excluded_without_any(self):
        excluded = next(r for r in self.doc["records"] if not r["eligible"])
        rc, out, _ = run(["image-url", "--id", excluded["id"]])
        self.assertEqual((rc, out), (1, ""))
        rc, out, _ = run(["image-url", "--id", "--any", excluded["id"]])
        self.assertEqual((rc, out.strip()), (0, excluded["image"]))

    def test_image_url_prints_bare_url(self):
        rc, out, _ = run(["image-url", "Crescent Reaper Fang"])
        self.assertEqual(rc, 0)
        self.assertTrue(out.startswith("https://") and out.count("\n") == 1)

    def test_search(self):
        hits = ja.search(self.doc, "abyssal")
        self.assertTrue(hits and all("abyssal" in r["norm"] and r["eligible"] for r in hits))
        self.assertGreaterEqual(len(ja.search(self.doc, "abyssal", include_all=True)), len(hits))

    def test_record_returns_bundle_record(self):
        rc, out, _ = run(["record", "Crescent Reaper Fang"])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload["record"]["id"], "cjRErpuffG4GiwIU8OsCw")
        self.assertIn("effects", payload["record"])
        self.assertTrue(payload["provenance"]["snapshotKey"].endswith(f"::before::{payload['provenance']['ordinal'] % 100}"))

    def test_ambiguous_name_never_resolves(self):
        doc = copy.deepcopy(self.doc)
        twin = dict(doc["records"][0], id="TWIN")
        doc["records"].append(twin)
        with self.assertRaises(ja.ProvenanceError):
            ja.resolve(doc, twin["name"])


class FailClosedTests(unittest.TestCase):
    def assertFails(self, root, needle):
        with self.assertRaises(ja.ProvenanceError) as cm:
            ja.build(root)
        self.assertIn(needle, str(cm.exception))

    def test_clean_copy_builds(self):
        with TempRepo() as root:
            self.assertEqual(ja.build(root)[1], ja.build(ROOT)[1])

    def test_state(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][2]["bundle"], lambda d: d.update(state="RUNNING"))
            self.assertFails(root, "state")

    def test_outcome(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][0]["bundle"], lambda d: d.update(outcome="open"))
            self.assertFails(root, "outcome")

    def test_count(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][6]["bundle"], lambda d: d["captures"].pop())
            self.assertFails(root, "captures")

    def test_persist(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][1]["bundle"], lambda d: d["captures"][5].update(persistOk=False))
            self.assertFails(root, "persist")

    def test_record_id(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][3]["bundle"], lambda d: d["captures"][7]["data"].update(id="x"))
            self.assertFails(root, "data.id")

    def test_input_id(self):
        def swap(d):
            c = d["captures"]
            c[0]["input"], c[1]["input"] = c[1]["input"], c[0]["input"]
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][4]["bundle"], swap)
            self.assertFails(root, "input.id")

    def test_manifest_edit(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][5]["manifest"], lambda d: d.update(_note="x", items=[{"entity": "jutsu"}]))
            self.assertFails(root, "hash")

    def test_journal_hash(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][0]["bundle"], lambda d: d["journal"].update(manifestHash="00000000"))
            self.assertFails(root, "manifestHash")

    def test_coverage_summary(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["coverage"]["bundle"], lambda d: d["journal"].update(capturesBeforePartial=[]))
            self.assertFails(root, "getAllNames")

    def test_expected_counts_pin(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][0]["bundle"], lambda d: [c["data"].update(hidden=True) for c in d["captures"]])
            self.assertFails(root, "expectations")

    def test_verify_detects_stale_output(self):
        with TempRepo() as root:
            (root / "answers").mkdir(exist_ok=True)
            (root / ja.OUTPUT).write_text("{}\n", encoding="utf-8")
            rc, _, err = run(["verify"], root=root)
            self.assertEqual(rc, 1)
            self.assertIn("stale", err)
            self.assertEqual(run(["build"], root=root)[0], 0)
            self.assertEqual(run(["verify"], root=root)[0], 0)

    def test_cli_exit_code_on_provenance_failure(self):
        with TempRepo() as root:
            TempRepo.edit(root, ja.SOURCES["batches"][0]["bundle"], lambda d: d.update(state="RUNNING"))
            rc, _, err = run(["verify"], root=root)
            self.assertEqual(rc, 2)
            self.assertIn("FAIL CLOSED", err)


class MaterializeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = ja.load_derived(ROOT)

    def test_host_policy(self):
        ja.check_cdn_url("https://utfs.io/f/abc")
        for bad in ("http://utfs.io/f/abc", "https://www.theninja-rpg.com/api/trpc/x",
                    "https://theninja-rpg.com/x", "https://example.com/a.png"):
            with self.assertRaises(ja.ProvenanceError):
                ja.check_cdn_url(bad)

    def test_every_eligible_url_is_cdn(self):
        for r in self.doc["records"]:
            if r["eligible"]:
                ja.check_cdn_url(r["image"])

    def test_fetch_writes_and_indexes(self):
        calls = []
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            res = ja.materialize(self.doc, ["Crescent Reaper Fang"], out, fetch=lambda u: calls.append(u) or WEBP)
            self.assertEqual(res[0]["file"], "cjRErpuffG4GiwIU8OsCw.webp")
            self.assertEqual((out / res[0]["file"]).read_bytes(), WEBP)
            index = json.loads((out / "materialized.json").read_text(encoding="utf-8"))
            self.assertIn("cjRErpuffG4GiwIU8OsCw", index)
        self.assertEqual(len(calls), 1)

    def test_any_miss_aborts_before_fetching(self):
        calls = []
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ja.LookupMiss):
                ja.materialize(self.doc, ["Crescent Reaper Fang", "No Such Jutsu"], Path(tmp), fetch=calls.append)
        self.assertEqual(calls, [])

    def test_dry_run_and_non_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            res = ja.materialize(self.doc, ["Crescent Reaper Fang"], Path(tmp), dry_run=True, fetch=None)
            self.assertEqual(res[0]["action"], "would-fetch")
            with self.assertRaises(ja.ProvenanceError):
                ja.materialize(self.doc, ["Crescent Reaper Fang"], Path(tmp), fetch=lambda u: b"<html>")

    def test_excluded_refused(self):
        excluded = next(r for r in self.doc["records"] if not r["eligible"])
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ja.ProvenanceError):
                ja.materialize(self.doc, [excluded["id"]], Path(tmp), by_id=True, fetch=lambda u: WEBP)


if __name__ == "__main__":
    unittest.main()
