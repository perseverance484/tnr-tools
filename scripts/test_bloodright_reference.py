#!/usr/bin/env python3
"""Tests for scripts/bloodright_reference.py. Socket-free: every socket is refused for the whole
module, acquisition uses an injected fake fetcher, and repository sources are either the real
offline git objects (pinned roster) or an in-memory fixture.

    python3 -m unittest scripts/test_bloodright_reference.py -v
"""

from __future__ import annotations

import copy
import hashlib
import io
import json
import socket
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bloodright_reference as br  # noqa: E402
import jutsu_art as ja  # noqa: E402

PE = br.ProvenanceError
_REAL_SOCKET = socket.socket


class _NoSocket(socket.socket):
    def __init__(self, *a, **k):
        raise AssertionError("a test tried to open a socket")


def setUpModule():
    socket.socket = _NoSocket


def tearDownModule():
    socket.socket = _REAL_SOCKET


def img(fmt="PNG", color=(10, 120, 200), size=(8, 6), frames=1) -> bytes:
    ims = [Image.new("RGB", size, (color[0], color[1], (color[2] + 30 * i) % 256)) for i in range(frames)]
    buf = io.BytesIO()
    if frames > 1:
        ims[0].save(buf, fmt, save_all=True, append_images=ims[1:])
    else:
        ims[0].save(buf, fmt)
    return buf.getvalue()


CDN = "https://ui0arpl8sm.ufs.sh/f/"


# ---------------------------------------------------------------------------------------------
# In-memory fixture: a two-bloodline cohort (one INCLUDE S, one REFERENCE A) plus noise records
# ---------------------------------------------------------------------------------------------
class FakeSource:
    def __init__(self, files: dict, blobs: dict):
        self.files, self.blobs = files, blobs

    def file(self, rel):
        if rel not in self.files:
            raise PE(f"{rel}: missing")
        return self.files[rel]

    def blob(self, ref, path):
        if (ref, path) not in self.blobs:
            raise PE(f"no blob {ref}:{path}")
        return self.blobs[(ref, path)]

    def listdir(self, ref, path):
        return sorted(p.rsplit("/", 1)[-1] for (r, p) in self.blobs if r == ref and p.startswith(path + "/"))


REF = "a" * 40
KITS = "kits"
BL_S, BL_A = "BL_S_id", "BL_A_id"
J_S = ["sA1", "sB-2", "s_C3"]
J_A = ["aX1", "aY2"]


def make_world(*, images=None, records_override=None, capture_mutator=None, extra_roster=None):
    images = images or {}
    roster = {"records": [
        {"review_id": "BR-002", "bloodline_id": BL_S, "name": "Ethereal Fixture", "rank": "S", "hidden": False,
         "owner_decision": "INCLUDE", "public_jutsu_ids": J_S, "public_jutsu_count": 3, "hidden_jutsu_ids": []},
        {"review_id": "BR-001", "bloodline_id": BL_A, "name": "Référence Kami", "rank": "A", "hidden": False,
         "owner_decision": "REFERENCE", "public_jutsu_ids": J_A, "public_jutsu_count": 2, "hidden_jutsu_ids": []},
        {"review_id": "BR-003", "bloodline_id": "hidden_bl", "name": "Hidden", "rank": "H", "hidden": True,
         "owner_decision": "DEFER", "public_jutsu_ids": ["h1"], "public_jutsu_count": 1, "hidden_jutsu_ids": []},
        {"review_id": "BR-004", "bloodline_id": "b_rank", "name": "B Rank", "rank": "B", "hidden": False,
         "owner_decision": "INCLUDE", "public_jutsu_ids": ["b1"], "public_jutsu_count": 1, "hidden_jutsu_ids": []},
    ], "excluded_ids": [], "deferred_ids": ["hidden_bl"]}
    if records_override:
        records_override(roster)
    if extra_roster:
        roster.update(extra_roster)
    names = {"sA1": "Sixth Wind", "sB-2": "Tamashī no Sakeme", "s_C3": "Founder’s Wrath", "aX1": "Sun Fist", "aY2": "Sun Fist"}
    types = {"sA1": "SPECIAL"}
    kit_s = {"review_id": "BR-002", "bloodline_id": BL_S, "rank": "S",
             "jutsu": [{"id": j, "name": names[j], "visibility": "public", "jutsuType": types.get(j, "BLOODLINE")} for j in J_S]}
    kit_a = {"review_id": "BR-001", "bloodline_id": BL_A, "rank": "A",
             "jutsu": [{"id": j, "name": names[j], "visibility": "public", "jutsuType": "BLOODLINE"} for j in J_A]}
    roster_bytes = json.dumps(roster).encode()
    blobs = {(REF, "roster.json"): roster_bytes,
             (REF, f"{KITS}/ethereal.json"): json.dumps(kit_s).encode(),
             (REF, f"{KITS}/ref.json"): json.dumps(kit_a).encode()}

    reads = [("jutsu.get", j) for j in J_S + J_A] + [("bloodline.get", BL_S)]
    manifest = {"capture": {"before": [{"proc": p, "input": {"id": i}, "persist": "full"} for p, i in reads], "after": []}, "items": []}
    mhash = ja.manifest_hash(manifest)
    job = "1-job"
    caps = []
    for n, (p, i) in enumerate(reads):
        if p == "jutsu.get":
            bl = BL_S if i in J_S else BL_A
            data = {"id": i, "name": names[i], "jutsuType": types.get(i, "BLOODLINE"), "bloodlineId": bl, "hidden": False,
                    "image": images.get(i, f"{CDN}{i}")}
        else:
            data = {"id": i, "name": "Ethereal Fixture", "rank": "S", "hidden": False, "image": images.get(i, f"{CDN}bl-{i}")}
        caps.append({"phase": "before", "proc": p, "input": {"id": i}, "ok": True, "rows": 1, "error": None,
                     "persist": "full", "snapshotKey": f"{job}::before::{n}", "persistOk": True, "persistError": None,
                     "at": f"2026-10-17T00:00:{n:02d}Z", "data": data})
    bundle = {"state": "DONE", "outcome": "success", "entries": [], "captures": caps,
              "journal": {"jobId": job, "manifestPath": "push/1.json", "manifestNumber": 1, "manifestHash": mhash,
                          "state": "DONE", "items": [], "capturesBeforePartial": None,
                          "capturesBefore": [{k: c[k] for k in ("proc", "input", "ok", "rows", "persist", "persistOk", "snapshotKey")} for c in caps]}}
    if capture_mutator:
        capture_mutator(bundle)
    bundle_bytes = json.dumps(bundle).encode()
    sources = {"brief": {"sha": "b" * 40}, "roster": {"branch": "fable/fixture", "ref": REF, "path": "roster.json", "blob": br.git_blob_sha1(roster_bytes), "kits_dir": KITS},
               "expected": {"bloodlines": 2, "ranks": {"A": 1, "S": 1, "H": 0}, "jutsu": 5},
               "captures": [{"manifest": "push/1.json", "manifest_number": 1, "manifest_hash": mhash, "bundle": "h/1.json",
                             "bundle_sha256": hashlib.sha256(bundle_bytes).hexdigest(), "job_id": job}]}
    files = {br.SOURCES_PATH: json.dumps(sources).encode(), "push/1.json": json.dumps(manifest).encode(), "h/1.json": bundle_bytes}
    return FakeSource(files, blobs)


def resign(src: FakeSource) -> FakeSource:
    """Re-pin the bundle sha after a deliberate edit, so a test reaches the check behind the pin."""
    s = json.loads(src.files[br.SOURCES_PATH])
    s["captures"][0]["bundle_sha256"] = hashlib.sha256(src.files["h/1.json"]).hexdigest()
    src.files[br.SOURCES_PATH] = json.dumps(s).encode()
    return src


def edit_bundle(src: FakeSource, fn) -> FakeSource:
    b = json.loads(src.files["h/1.json"])
    fn(b)
    src.files["h/1.json"] = json.dumps(b).encode()
    return resign(src)


class Fetcher:
    """Fake CDN. Maps URL -> bytes or an exception; records every call."""

    def __init__(self, table=None, default=None):
        self.table = table or {}
        self.default = default
        self.calls = []

    def __call__(self, url):
        br.check_url(url)  # the real _fetch refuses a bad URL before any request
        self.calls.append(url)
        v = self.table.get(url, self.default(url) if self.default else None)
        if isinstance(v, Exception):
            raise v
        if v is None:
            raise PE(f"HTTP 404 for {url}")
        return v


def distinct_png(url: str) -> bytes:
    h = hashlib.sha256(url.encode()).digest()
    return img("PNG", color=(h[0], h[1], h[2]), size=(4 + h[3] % 5, 4 + h[4] % 5))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.cache = self.tmp / "cache"
        self.out = self.tmp / "out"

    def world(self, **kw):
        src = make_world(**kw)
        inv, _ = br.inventory(src)
        return src, inv


# ---------------------------------------------------------------------------------------------
# Real pinned cohort (offline git objects only)
# ---------------------------------------------------------------------------------------------
def _have_roster() -> bool:
    try:
        src = br.RepoSource()
        s = br.load_sources(src)
        src.blob(s["roster"]["ref"], s["roster"]["path"])
        return True
    except Exception:  # noqa: BLE001
        return False


@unittest.skipUnless(_have_roster(), "pinned roster commit not in this clone: git fetch origin fable/bloodright-planning-20261003")
class RealCohort(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inv, cls.sources = br.inventory()

    def test_membership_is_29_bloodlines_166_distinct_ids(self):
        bl = self.inv["bloodlines"]
        self.assertEqual(len(bl), 29)
        self.assertEqual({r: sum(b["rank"] == r for b in bl) for r in "ASH"}, {"A": 19, "S": 6, "H": 4})
        ids = [j["id"] for b in bl for j in b["jutsu"]]
        self.assertEqual(len(ids), 166)
        self.assertEqual(len(set(ids)), 166)

    def test_special_jutsu_with_bloodline_id_are_members(self):
        special = [j for b in self.inv["bloodlines"] for j in b["jutsu"] if j["kit_type"] == "SPECIAL"]
        self.assertTrue(special, "SPECIAL-typed linked jutsu must not be filtered out")

    def test_deferred_and_excluded_are_never_members(self):
        src = br.RepoSource()
        roster = json.loads(src.blob(self.sources["roster"]["ref"], self.sources["roster"]["path"]))
        out = set(roster["excluded_ids"]) | set(roster["deferred_ids"])
        self.assertFalse(out & {b["bloodline_id"] for b in self.inv["bloodlines"]})

    def test_ethereal_monarch_pilot_is_six_verified_ids(self):
        em = next(b for b in self.inv["bloodlines"] if b["review_id"] == "BR-023")
        self.assertEqual(em["status"], "READY")
        self.assertEqual([j["id"] for j in em["jutsu"]], ["0_ip_8I2Dh_Ti2mYUcuAu", "Q3hmgslgYbbLHwwOZckT-", "AK8P4xmHSdbUOh2ywzb1l",
                                                          "q7QKL0ETYGDEawoF_yzkS", "xPfjuu4WMe786wDVaizik", "nvMSommJJLlG5xwT7nQ6b"])
        for j in em["jutsu"]:
            self.assertEqual(j["evidence"]["job_id"], "101-mvbxb3q6")
            br.check_url(j["image"])
        self.assertEqual(em["identity"]["status"], "READY")

    def test_uncaptured_bloodlines_are_source_blocked_with_exact_gaps(self):
        s = self.inv["summary"]
        self.assertLess(s["bloodlines_ready"], 29)
        self.assertEqual(len(s["missing"]), s["jutsu"] - s["jutsu_ready"])
        for m in s["missing"]:
            self.assertEqual(m["status"], "MISSING_CAPTURE")
            self.assertTrue(m["id"] and m["kit_name"] and m["review_id"])

    def test_full_library_is_refused_while_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(PE, "full library refused"):
                br.pack(self.inv, None, Path(d) / "c", Path(d) / "o")
            self.assertFalse((Path(d) / "o").exists())


# ---------------------------------------------------------------------------------------------
# Cohort and evidence rules
# ---------------------------------------------------------------------------------------------
class CohortRules(Base):
    def test_fixture_cohort_selects_include_ash_and_reference_only(self):
        _, inv = self.world()
        self.assertEqual([b["review_id"] for b in inv["bloodlines"]], ["BR-001", "BR-002"])
        self.assertEqual(inv["summary"]["jutsu"], 5)

    def test_roster_blob_tamper_is_fatal(self):
        src = make_world()
        src.blobs[(REF, "roster.json")] += b" "
        with self.assertRaisesRegex(PE, "blob"):
            br.inventory(src)

    def test_deferred_member_is_rejected(self):
        src = make_world(extra_roster={"deferred_ids": ["hidden_bl", BL_S]})
        with self.assertRaisesRegex(PE, "excluded/deferred"):
            br.inventory(src)

    def test_jutsu_shared_by_two_bloodlines_is_rejected(self):
        def dup(r):
            r["records"][1]["public_jutsu_ids"] = ["aX1", "sA1"]
        src = make_world(records_override=dup)
        with self.assertRaises(PE):
            br.inventory(src)

    def test_kit_roster_disagreement_is_rejected(self):
        src = make_world()
        k = json.loads(src.blobs[(REF, f"{KITS}/ref.json")])
        k["jutsu"].pop()
        src.blobs[(REF, f"{KITS}/ref.json")] = json.dumps(k).encode()
        with self.assertRaisesRegex(PE, "disagree"):
            br.inventory(src)

    def test_unexpected_count_is_rejected(self):
        def more(r):
            r["records"][3]["rank"] = "A"  # the B-rank record now qualifies -> 3 bloodlines
        src = make_world(records_override=more)
        k = {"review_id": "BR-004", "bloodline_id": "b_rank", "rank": "A", "jutsu": [{"id": "b1", "name": "x", "visibility": "public", "jutsuType": "BLOODLINE"}]}
        src.blobs[(REF, f"{KITS}/b.json")] = json.dumps(k).encode()
        with self.assertRaisesRegex(PE, "bloodlines, pinned"):
            br.inventory(src)


class EvidenceRules(Base):
    def status(self, inv, jid):
        return next(j for b in inv["bloodlines"] for j in b["jutsu"] if j["id"] == jid)

    def test_clean_fixture_is_ready(self):
        _, inv = self.world()
        self.assertEqual(inv["summary"]["jutsu_ready"], 5)

    def test_bundle_sha_pin(self):
        src = make_world()
        src.files["h/1.json"] += b"\n"
        with self.assertRaisesRegex(PE, "sha256"):
            br.inventory(src)

    def test_manifest_hash_pin(self):
        src = make_world()
        m = json.loads(src.files["push/1.json"])
        m["capture"]["before"].pop()
        src.files["push/1.json"] = json.dumps(m).encode()
        with self.assertRaisesRegex(PE, "hash"):
            br.inventory(src)

    def test_unpersisted_body_is_fatal(self):
        src = edit_bundle(make_world(), lambda b: b["captures"][0].update(persistOk=False))
        with self.assertRaisesRegex(PE, "not persisted"):
            br.inventory(src)

    def test_record_id_mismatch_is_fatal(self):
        src = edit_bundle(make_world(), lambda b: b["captures"][1]["data"].update(id="sA1"))
        with self.assertRaisesRegex(PE, "record id"):
            br.inventory(src)

    def test_job_with_mutations_is_refused(self):
        src = edit_bundle(make_world(), lambda b: b.update(entries=[{"op": "create"}]))
        with self.assertRaisesRegex(PE, "zero mutations"):
            br.inventory(src)

    def test_bloodline_mismatch_blocks(self):
        src = edit_bundle(make_world(), lambda b: b["captures"][0]["data"].update(bloodlineId="other"))
        inv, _ = br.inventory(src)
        self.assertEqual(self.status(inv, "sA1")["status"], "BLOODLINE_MISMATCH")
        self.assertEqual(next(b for b in inv["bloodlines"] if b["bloodline_id"] == BL_S)["status"], "SOURCE_BLOCKED")

    def test_missing_and_null_and_bad_urls_block(self):
        for url, want in [(None, "NULL_IMAGE"), ("", "NULL_IMAGE"), ("http://ui0arpl8sm.ufs.sh/f/x", "BAD_URL"),
                          ("https://theninja-rpg.com/x.png", "BAD_URL"), ("https://evil.example/x.png", "BAD_URL"),
                          (f"{CDN}x?token=secret", "BAD_URL"), ("https://user:pw@ui0arpl8sm.ufs.sh/f/x", "BAD_URL"),
                          ("https://ui0arpl8sm.ufs.sh:8443/f/x", "BAD_URL"), (f"{CDN}../../x", "BAD_URL"), (f"{CDN}ü", "BAD_URL")]:
            with self.subTest(url=url):
                _, inv = self.world(images={"sA1": url})
                self.assertEqual(self.status(inv, "sA1")["status"], want)

    def test_uncaptured_member_is_missing_capture(self):
        src = make_world()
        m = json.loads(src.files["push/1.json"])
        b = json.loads(src.files["h/1.json"])
        m["capture"]["before"].pop(0)
        b["captures"].pop(0)
        b["journal"]["capturesBefore"].pop(0)
        job = b["journal"]["jobId"]
        for n, c in enumerate(b["captures"]):
            c["snapshotKey"] = b["journal"]["capturesBefore"][n]["snapshotKey"] = f"{job}::before::{n}"
        h = ja.manifest_hash(m)
        b["journal"]["manifestHash"] = h
        src.files["push/1.json"] = json.dumps(m).encode()
        src.files["h/1.json"] = json.dumps(b).encode()
        s = json.loads(src.files[br.SOURCES_PATH])
        s["captures"][0]["manifest_hash"] = h
        src.files[br.SOURCES_PATH] = json.dumps(s).encode()
        inv, _ = br.inventory(resign(src))
        self.assertEqual(self.status(inv, "sA1")["status"], "MISSING_CAPTURE")
        self.assertEqual([m["id"] for m in inv["summary"]["missing"]], ["sA1"])

    def test_two_bundles_disagreeing_on_image_is_ambiguous(self):
        src = make_world()
        s = json.loads(src.files[br.SOURCES_PATH])
        b2 = json.loads(src.files["h/1.json"])
        b2["captures"][0]["data"]["image"] = f"{CDN}different"
        b2_bytes = json.dumps(b2).encode()
        src.files["h/2.json"] = b2_bytes
        s["captures"].append({**s["captures"][0], "bundle": "h/2.json", "bundle_sha256": hashlib.sha256(b2_bytes).hexdigest()})
        src.files[br.SOURCES_PATH] = json.dumps(s).encode()
        inv, _ = br.inventory(src)
        self.assertEqual(self.status(inv, "sA1")["status"], "AMBIGUOUS")

    def test_hidden_live_record_blocks(self):
        src = edit_bundle(make_world(), lambda b: b["captures"][0]["data"].update(hidden=True))
        inv, _ = br.inventory(src)
        self.assertEqual(self.status(inv, "sA1")["status"], "NOT_PUBLIC")


# ---------------------------------------------------------------------------------------------
# Acquisition (fake transport only)
# ---------------------------------------------------------------------------------------------
class Acquire(Base):
    def test_fetches_only_allowlisted_cdn_and_never_the_game(self):
        _, inv = self.world()
        f = Fetcher(default=distinct_png)
        r = br.acquire(inv, None, self.cache, fetch=f)
        self.assertEqual(r["game_requests"], 0)
        self.assertEqual(r["cdn_gets"], len(f.calls))
        for u in f.calls:
            self.assertIn(br.urllib.parse.urlsplit(u).hostname, ja.CDN_HOSTS)
            self.assertNotIn("theninja-rpg", u)
        self.assertEqual(len(f.calls), 6)  # 5 jutsu + 1 identity
        self.assertEqual(len(br.read_cache(self.cache)), 6)

    def test_blocked_selection_fetches_nothing(self):
        _, inv = self.world(images={"sA1": None})
        f = Fetcher(default=distinct_png)
        with self.assertRaisesRegex(PE, "SOURCE_BLOCKED"):
            br.acquire(inv, ["BR-002"], self.cache, fetch=f)
        self.assertEqual(f.calls, [])
        self.assertFalse(self.cache.exists())

    def test_bad_bodies_fail_closed_and_write_nothing(self):
        png = img()
        cases = {
            "html": b"<!doctype html><html>error</html>",
            "truncated": png[: len(png) // 2],
            "signature_mismatch": b"\x89PNG\r\n\x1a\n" + img("GIF")[8:],
            "multiframe": img("GIF", frames=3),
            "empty": b"",
        }
        for label, body in cases.items():
            with self.subTest(label):
                _, inv = self.world()
                cache = self.tmp / f"c_{label}"
                f = Fetcher(default=distinct_png, table={f"{CDN}sA1": body})
                with self.assertRaises(PE):
                    br.acquire(inv, ["BR-002"], cache, fetch=f)
                self.assertFalse(cache.exists(), "nothing may be written on a failed acquisition")

    def test_failure_midway_leaves_previous_cache_intact(self):
        _, inv = self.world()
        br.acquire(inv, ["BR-001"], self.cache, fetch=Fetcher(default=distinct_png))
        before = (self.cache / br.LEDGER).read_bytes()
        objs = sorted(p.name for p in (self.cache / "objects").iterdir())
        f = Fetcher(default=distinct_png, table={f"{CDN}s_C3": OSError("connection reset")})
        with self.assertRaisesRegex(PE, "nothing written"):
            br.acquire(inv, ["BR-002"], self.cache, fetch=f)
        self.assertEqual((self.cache / br.LEDGER).read_bytes(), before)
        self.assertEqual(sorted(p.name for p in (self.cache / "objects").iterdir()), objs)

    def test_cached_urls_are_not_refetched(self):
        _, inv = self.world()
        br.acquire(inv, None, self.cache, fetch=Fetcher(default=distinct_png))
        f = Fetcher(default=distinct_png)
        r = br.acquire(inv, None, self.cache, fetch=f)
        self.assertEqual(f.calls, [])
        self.assertEqual(r["cdn_gets"], 0)

    def test_remote_byte_drift_is_surfaced_not_accepted(self):
        _, inv = self.world()
        br.acquire(inv, None, self.cache, fetch=Fetcher(default=distinct_png))
        before = (self.cache / br.LEDGER).read_bytes()
        f = Fetcher(default=distinct_png, table={f"{CDN}aX1": img(color=(1, 2, 3))})
        with self.assertRaisesRegex(PE, "REMOTE BYTES CHANGED"):
            br.acquire(inv, None, self.cache, fetch=f, recheck=True)
        self.assertEqual((self.cache / br.LEDGER).read_bytes(), before)

    def test_cache_tamper_is_detected(self):
        _, inv = self.world()
        br.acquire(inv, None, self.cache, fetch=Fetcher(default=distinct_png))
        obj = next((self.cache / "objects").iterdir())
        obj.write_bytes(img(color=(9, 9, 9)))
        with self.assertRaisesRegex(PE, "tampered"):
            br.read_cache(self.cache)

    def test_identity_failure_is_reported_not_fatal(self):
        _, inv = self.world()
        f = Fetcher(default=distinct_png, table={f"{CDN}bl-{BL_S}": PE("HTTP 404")})
        r = br.acquire(inv, None, self.cache, fetch=f)
        self.assertEqual(len(r["identity_failed"]), 1)
        self.assertEqual(len(br.read_cache(self.cache)), 5)

    def test_redirect_handler_refuses_non_cdn_targets(self):
        h = br._Redirects()
        self.assertEqual(h.max_redirections, br.MAX_REDIRECTS)
        for bad in ("https://theninja-rpg.com/a.png", "http://utfs.io/f/a", "https://169.254.169.254/latest", "https://localhost/a"):
            with self.subTest(bad), self.assertRaises(PE):
                h.redirect_request(None, None, 302, "Found", {}, bad)


# ---------------------------------------------------------------------------------------------
# Pack and verify (offline)
# ---------------------------------------------------------------------------------------------
class PackVerify(Base):
    def built(self, ids=("BR-002",), fetch=None):
        src, inv = self.world()
        fetch = fetch or Fetcher(default=distinct_png)
        br.acquire(inv, list(ids), self.cache, fetch=fetch)
        r = br.pack(inv, list(ids), self.cache, self.out)
        return inv, r, Path(r["path"]).read_bytes()

    def test_pilot_is_named_pilot_and_verifies(self):
        inv, r, data = self.built()
        self.assertEqual(Path(r["path"]).name, f"{br.FULL_STEM}_PILOT_BR-002.zip")
        self.assertFalse((self.out / f"{br.FULL_STEM}.zip").exists())
        self.assertEqual((r["scope"], r["bloodlines"], r["jutsu"]), ("PILOT", 1, 3))
        z = zipfile.ZipFile(io.BytesIO(data))
        idx = json.loads(z.read(f"{br.FULL_STEM}_PILOT_BR-002/BLOODLINE_INDEX.json"))
        self.assertEqual(idx["status"], "PILOT_NOT_FULL_LIBRARY")
        self.assertIn("not the full library", z.read(f"{br.FULL_STEM}_PILOT_BR-002/README.md").decode())

    def test_single_top_folder_and_android_safe_names(self):
        _, r, data = self.built()
        z = zipfile.ZipFile(io.BytesIO(data))
        self.assertEqual({n.split("/")[0] for n in z.namelist()}, {r["stem"]})
        for n in z.namelist():
            br.check_member(n)
            self.assertTrue(n.isascii())

    def test_nested_bytes_equal_acquired_bytes(self):
        fetch = Fetcher(default=distinct_png)
        inv, r, data = self.built(fetch=fetch)
        outer = zipfile.ZipFile(io.BytesIO(data))
        inner = zipfile.ZipFile(io.BytesIO(outer.read(f"{r['stem']}/BLOODLINE_PACKS/BR-002_Ethereal_Fixture.zip")))
        man = json.loads(inner.read("manifest.json"))
        self.assertEqual([j["jutsu_id"] for j in man["jutsu"]], J_S)
        for j in man["jutsu"]:
            b = inner.read(j["file"])
            self.assertEqual(b, distinct_png(j["image_url"]))
            self.assertEqual(hashlib.sha256(b).hexdigest(), j["sha256"])
            self.assertEqual(len(b), j["bytes"])
            self.assertTrue(j["file"].startswith(f"images/{j['jutsu_id']}_"))
            self.assertTrue(j["file"].endswith(".png"))
        self.assertEqual(man["identity"]["status"], "INCLUDED")
        self.assertIn("Tamashī no Sakeme", [j["name"] for j in man["jutsu"]], "manifest keeps Unicode display names")
        self.assertIn("images/sB-2_Tamashi_no_Sakeme.png", inner.namelist())
        self.assertIn("images/s_C3_Founders_Wrath.png", inner.namelist())

    def test_extension_follows_decoded_format(self):
        fetch = Fetcher(default=distinct_png, table={f"{CDN}sA1": img("WEBP"), f"{CDN}sB-2": img("JPEG")})
        _, r, data = self.built(fetch=fetch)
        inner = zipfile.ZipFile(io.BytesIO(zipfile.ZipFile(io.BytesIO(data)).read(f"{r['stem']}/BLOODLINE_PACKS/BR-002_Ethereal_Fixture.zip")))
        names = inner.namelist()
        self.assertIn("images/sA1_Sixth_Wind.webp", names)
        self.assertIn("images/sB-2_Tamashi_no_Sakeme.jpg", names)

    def test_duplicate_display_names_with_different_ids_get_distinct_files(self):
        _, r, data = self.built(ids=("BR-001",))
        inner = zipfile.ZipFile(io.BytesIO(zipfile.ZipFile(io.BytesIO(data)).read(f"{r['stem']}/BLOODLINE_PACKS/BR-001_Reference_Kami.zip")))
        imgs = [n for n in inner.namelist() if n.startswith("images/") and not n.endswith("/")]
        self.assertEqual(sorted(imgs), ["images/aX1_Sun_Fist.png", "images/aY2_Sun_Fist.png"])

    def test_repacking_identical_cache_is_byte_identical(self):
        src, inv = self.world()
        br.acquire(inv, None, self.cache, fetch=Fetcher(default=distinct_png), now=lambda: "2026-01-01T00:00:00Z")
        a = Path(br.pack(inv, ["BR-001", "BR-002"], self.cache, self.out)["path"]).read_bytes()
        # a later recheck changes ledger timestamps only; the archive must not change
        br.acquire(inv, None, self.cache, fetch=Fetcher(default=distinct_png), recheck=True, now=lambda: "2027-06-06T06:06:06Z")
        out2 = self.tmp / "out2"
        b = Path(br.pack(inv, ["BR-001", "BR-002"], self.cache, out2)["path"]).read_bytes()
        self.assertEqual(hashlib.sha256(a).hexdigest(), hashlib.sha256(b).hexdigest())
        za, zb = zipfile.ZipFile(io.BytesIO(a)), zipfile.ZipFile(io.BytesIO(b))
        for n in za.namelist():
            if n.endswith(".zip"):
                self.assertEqual(za.read(n), zb.read(n), n)

    def test_full_library_requires_every_bloodline_and_is_written_only_then(self):
        src, inv = self.world()
        br.acquire(inv, None, self.cache, fetch=Fetcher(default=distinct_png))
        r = br.pack(inv, None, self.cache, self.out)
        self.assertEqual(Path(r["path"]).name, f"{br.FULL_STEM}.zip")
        self.assertEqual((r["scope"], r["bloodlines"], r["jutsu"]), ("FULL", 2, 5))

    def test_full_library_refused_with_one_gap(self):
        _, inv = self.world(images={"aY2": None})
        with self.assertRaisesRegex(PE, "full library refused"):
            br.pack(inv, None, self.cache, self.out)
        self.assertFalse(self.out.exists())

    def test_pack_without_cache_bytes_refuses(self):
        _, inv = self.world()
        with self.assertRaisesRegex(PE, "not in cache"):
            br.pack(inv, ["BR-002"], self.cache, self.out)

    def test_failed_repack_preserves_existing_verified_archive(self):
        inv, r, data = self.built()
        obj = next((self.cache / "objects").iterdir())
        obj.write_bytes(b"corrupt")
        with self.assertRaises(PE):
            br.pack(inv, ["BR-002"], self.cache, self.out)
        self.assertEqual(Path(r["path"]).read_bytes(), data)
        self.assertEqual([p.name for p in self.out.iterdir()], [Path(r["path"]).name], "no temp or partial files left")

    def test_unsafe_names_rejected(self):
        for bad in ("../x", "/abs", "a/../b", "C:/x", "a\\b", "con.txt", "a/NUL", "trail.", "üni", "a//b", "sp ace"):
            with self.subTest(bad), self.assertRaises(PE):
                br.check_member(bad)

    def test_case_collision_rejected(self):
        with self.assertRaisesRegex(PE, "case-insensitively"):
            br.build_zip([("images/AbC.png", b"1"), ("images/abc.png", b"2")])

    def test_slug(self):
        self.assertEqual(br.slug("Tamashī no Sakeme"), "Tamashi_no_Sakeme")
        self.assertEqual(br.slug("Founder’s Wrath"), "Founders_Wrath")
        self.assertEqual(br.slug("天照"), "untitled")


class Build(Base):
    def test_build_is_acquire_then_verified_pack(self):
        _, inv = self.world()
        f = Fetcher(default=distinct_png)
        r = br.build(inv, ["BR-002"], self.cache, self.out, fetch=f)
        self.assertEqual(r["acquire"]["game_requests"], 0)
        self.assertEqual(r["acquire"]["cdn_gets"], 4)
        self.assertTrue(r["pack"]["verified"])
        self.assertTrue(Path(r["pack"]["path"]).name.endswith("_PILOT_BR-002.zip"))

    def test_build_fetches_nothing_and_writes_nothing_when_blocked(self):
        _, inv = self.world(images={"sA1": None})
        f = Fetcher(default=distinct_png)
        with self.assertRaises(PE):
            br.build(inv, ["BR-002"], self.cache, self.out, fetch=f)
        self.assertEqual(f.calls, [])
        self.assertFalse(self.out.exists())


class CaptureManifests(Base):
    def blocked_world(self):
        # drop every capture so both fixture bloodlines are MISSING_CAPTURE
        src = make_world()
        s = json.loads(src.files[br.SOURCES_PATH])
        s["captures"] = []
        src.files[br.SOURCES_PATH] = json.dumps(s).encode()
        return br.inventory(src)[0]

    def test_whole_bloodlines_capped_reads_capture_only(self):
        inv = self.blocked_world()
        out = br.capture_manifests(inv, 200, limit=3)
        self.assertEqual([p for p, _ in out], ["push/200_bloodright_reference_capture_batch_1.json",
                                               "push/201_bloodright_reference_capture_batch_2.json"])
        seen = []
        for _, m in out:
            self.assertEqual((m["items"], m["capture"]["after"]), ([], []))
            self.assertLessEqual(sum(c["proc"] == "jutsu.get" for c in m["capture"]["before"]), 3)
            for c in m["capture"]["before"]:
                self.assertEqual(c["persist"], "full")
                self.assertIn(c["proc"], ("jutsu.get", "bloodline.get"))
                seen.append(c["input"]["id"])
        self.assertEqual(sorted(x for x in seen if x not in (BL_A, BL_S)), sorted(J_A + J_S))
        self.assertEqual(len(seen), len(set(seen)))

    def test_ready_bloodlines_are_not_recaptured(self):
        _, inv = self.world()
        self.assertEqual(br.capture_manifests(inv, 200), [])

    def test_bloodline_larger_than_limit_is_refused(self):
        with self.assertRaisesRegex(PE, "exceed"):
            br.capture_manifests(self.blocked_world(), 200, limit=2)

    def test_non_capture_gap_needs_a_decision(self):
        _, inv = self.world(images={"sA1": "https://evil.example/x.png"})
        with self.assertRaisesRegex(PE, "needs a decision"):
            br.capture_manifests(inv, 200)


class VerifyTamper(Base):
    def setUp(self):
        super().setUp()
        _, self.inv = self.world()
        br.acquire(self.inv, ["BR-002"], self.cache, fetch=Fetcher(default=distinct_png))
        self.r = br.pack(self.inv, ["BR-002"], self.cache, self.out)
        self.data = Path(self.r["path"]).read_bytes()
        self.stem = self.r["stem"]

    def rebuild(self, mutate):
        z = zipfile.ZipFile(io.BytesIO(self.data))
        entries = [(i.filename, None if i.filename.endswith("/") else z.read(i.filename)) for i in z.infolist()]
        entries = mutate(entries)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as out:
            for n, d in entries:
                out.writestr(n, d or b"")
        return buf.getvalue()

    def inner_name(self):
        return f"{self.stem}/BLOODLINE_PACKS/BR-002_Ethereal_Fixture.zip"

    def test_clean_archive_verifies_against_cache(self):
        self.assertTrue(br.verify_bytes(self.data, self.inv, ["BR-002"], self.cache)["verified"])

    def test_compromised_inner_manifest_is_detected(self):
        def mutate(entries):
            out = []
            for n, d in entries:
                if n == self.inner_name():
                    inner = zipfile.ZipFile(io.BytesIO(d))
                    man = json.loads(inner.read("manifest.json"))
                    man["jutsu"][0]["sha256"] = "0" * 64
                    items = [(i.filename, None if i.filename.endswith("/") else (br.canonical_json(man) if i.filename == "manifest.json" else inner.read(i.filename)))
                             for i in inner.infolist()]
                    d = br.build_zip(items)
                out.append((n, d))
            return out
        with self.assertRaises(PE):
            br.verify_bytes(self.rebuild(mutate), self.inv, ["BR-002"])

    def test_swapped_image_bytes_detected_even_with_matching_sums(self):
        def mutate(entries):
            out, new_inner = [], None
            for n, d in entries:
                if n == self.inner_name():
                    inner = zipfile.ZipFile(io.BytesIO(d))
                    items = []
                    for i in inner.infolist():
                        b = None if i.filename.endswith("/") else inner.read(i.filename)
                        if i.filename.startswith("images/s"):
                            b = img(color=(1, 1, 1))
                        items.append((i.filename, b))
                    d = new_inner = br.build_zip(items)
                out.append((n, d))
            return out
        with self.assertRaises(PE):
            br.verify_bytes(self.rebuild(mutate), self.inv, ["BR-002"])

    def test_duplicate_entry_is_detected(self):
        with self.assertRaisesRegex(PE, "duplicate"):
            br.verify_bytes(self.rebuild(lambda e: e + [e[1]]), self.inv, ["BR-002"])

    def test_extra_entry_is_detected(self):
        with self.assertRaisesRegex(PE, "layout"):
            br.verify_bytes(self.rebuild(lambda e: e + [(f"{self.stem}/extra.txt", b"x")]), self.inv, ["BR-002"])

    def test_sha256sums_mismatch_is_detected(self):
        def mutate(entries):
            return [(n, (d.replace(d[:4], b"0000", 1) if n.endswith("SHA256SUMS.txt") else d)) for n, d in entries]
        with self.assertRaises(PE):
            br.verify_bytes(self.rebuild(mutate), self.inv, ["BR-002"])

    def test_corrupt_crc_is_detected(self):
        bad = bytearray(self.data)
        i = bad.find(b"\x89PNG")
        bad[i + 40] ^= 0xFF
        with self.assertRaises(PE):
            br.verify_bytes(bytes(bad), self.inv, ["BR-002"])

    def test_pilot_cannot_pass_as_full(self):
        with self.assertRaises(PE):
            br.verify_bytes(self.data, self.inv, None)

    def test_cache_disagreement_is_detected(self):
        other = self.tmp / "other_cache"
        br.acquire(self.inv, ["BR-002"], other, fetch=Fetcher(default=lambda u: img(color=(5, 5, 5), size=(3, 3))))
        with self.assertRaisesRegex(PE, "acquired cache"):
            br.verify_bytes(self.data, self.inv, ["BR-002"], other)


if __name__ == "__main__":
    unittest.main()
