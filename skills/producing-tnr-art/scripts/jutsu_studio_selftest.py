#!/usr/bin/env python3
"""jutsu_studio_selftest.py - socket-free adversarial tests for jutsu_studio.py.

    python3 jutsu_studio_selftest.py

Every fixture is synthesized in a temp directory. Sockets are disabled for the run,
so any accidental network use fails loudly. Exit code is the failure count.
"""

from __future__ import annotations

import copy
import io
import json
import os
import shutil
import socket
import stat
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jutsu_studio as js  # noqa: E402
from PIL import Image  # noqa: E402


def _no_network(*_a, **_k):
    raise RuntimeError("network use is forbidden in jutsu_studio_selftest")


socket.socket = _no_network  # type: ignore[assignment]
socket.create_connection = _no_network  # type: ignore[assignment]

FAILS: list[str] = []
PASSES = 0


def want(cond: bool, label: str) -> None:
    global PASSES
    print(("  ok   " if cond else "  FAIL ") + label)
    if cond:
        PASSES += 1
    else:
        FAILS.append(label)


def refused(fn, needle: str) -> bool:
    try:
        fn()
    except js.StudioError as exc:
        if needle in str(exc):
            return True
        print(f"         (refused, but message lacked {needle!r}: {exc})")
        return False
    print(f"         (not refused; expected {needle!r})")
    return False


def png(seed: int, size: int = 64, mode: str = "RGB") -> bytes:
    img = js.synth_image(seed, size)
    if mode == "RGBA":
        img = img.convert("RGBA")
        img.putpixel((0, 0), (0, 0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def jpeg(seed: int, size: int = 64) -> bytes:
    buf = io.BytesIO()
    js.synth_image(seed, size).save(buf, "JPEG", quality=90)
    return buf.getvalue()


def raw_zip(entries: list[tuple], compression=zipfile.ZIP_DEFLATED) -> bytes:
    """entries: (name, bytes[, external_attr])"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression) as zf:
        for e in entries:
            info = zipfile.ZipInfo(e[0], js.ZIP_TIME)
            info.compress_type = compression
            if len(e) > 2:
                info.external_attr = e[2]
            zf.writestr(info, e[1])
    return buf.getvalue()


def manifest_pack(names, files=None, extra=None, with_sha=True, bloodline=None):
    entries, roster = [], []
    for i, n in enumerate(names):
        data = png(i)
        fname = (files or {}).get(n, f"art/{i:02d}.png")
        entries.append((fname, data))
        row = {"jutsu_id": f"ID{i}", "name": n, "file": fname}
        if with_sha:
            row["sha256"] = js.sha256(data)
        roster.append(row)
    man = {"bloodline": bloodline or {"id": "BL1", "name": "Test Line", "rank": "B"}, "jutsu": roster}
    entries.append(("manifest.json", json.dumps(man).encode()))
    entries += extra or []
    return raw_zip(entries), man


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="jutsu-studio-selftest-"))
    spec = js.load_spec(js.DEFAULT_SPEC)
    nums = js.spec_numbers(spec)
    try:
        run_intake_tests(tmp)
        run_layout_tests()
        run_finalize_tests(tmp, spec, nums)
        run_p1_tests(tmp, spec, nums)
        run_correction_tests(tmp, spec, nums)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{PASSES} passed, {len(FAILS)} failed")
    for f in FAILS:
        print(f"  - {f}")
    return len(FAILS)


# ---------------------------------------------------------------------------------------------


def run_intake_tests(tmp: Path) -> None:
    print("ZIP safety")
    good = png(1)
    cases = [
        ("zip-slip traversal", [("../evil.png", good)], "path traversal"),
        ("absolute path", [("/etc/evil.png", good)], "absolute path"),
        ("drive-letter path", [("C:/evil.png", good)], "absolute path"),
        ("backslash name", [("a\\b.png", good)], "backslash"),
        ("symlink entry", [("link.png", b"target", (stat.S_IFLNK | 0o777) << 16)], "symbolic link"),
        ("case-colliding names", [("A.png", good), ("a.png", good)], "case-collides"),
    ]
    for label, entries, needle in cases:
        want(refused(lambda e=entries: js.scan_zip(raw_zip(e)), needle), f"{label} is refused")
    dup = io.BytesIO()
    with zipfile.ZipFile(dup, "w") as zf:
        zf.writestr("x.png", good)
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            zf.writestr("x.png", good)
    want(refused(lambda: js.scan_zip(dup.getvalue()), "duplicate entry"), "duplicate entry names are refused")
    bomb = raw_zip([("bomb.bin", b"\0" * (4 * 1024 * 1024))])
    want(refused(lambda: js.scan_zip(bomb), "ZIP bomb"), "an extreme compression ratio is refused as a bomb")
    many = raw_zip([(f"f{i}.txt", b"x") for i in range(js.MAX_MEMBERS + 1)], zipfile.ZIP_STORED)
    want(refused(lambda: js.scan_zip(many), "entry bound"), "too many members are refused")
    corrupt = bytearray(raw_zip([("c.png", good)], zipfile.ZIP_STORED))
    at = bytes(corrupt).find(good[:16])
    corrupt[at + 40] ^= 0xFF
    want(refused(lambda: js.scan_zip(bytes(corrupt)), "CRC"), "a corrupt member fails its CRC check")
    want(refused(lambda: js.scan_zip(b"not a zip"), "not a readable ZIP"), "a non-ZIP is refused")
    members, ignored, _ = js.scan_zip(raw_zip([("ok.png", good), ("__MACOSX/._ok.png", b"junk"), (".DS_Store", b"x")]))
    want([m["path"] for m in members] == ["ok.png"] and len(ignored) == 2, "archive junk is ignored and reported, not mapped")

    print("\nintake mapping")
    names = ["Crimson Tide", "Iron Veil", "Ghost Step"]
    pack, man = manifest_pack(names)
    z = tmp / "p1.zip"
    z.write_bytes(pack)
    code = js.intake(z, tmp / "i1")
    src = json.loads((tmp / "i1" / "source_index.json").read_text())
    want(code == 0 and src["n"] == 3 and all(j["mapping"] == "MANIFEST_VERIFIED" for j in src["jutsu"]),
         "a structured pack maps every jutsu by manifest + hash (exit 0)")
    want(all((tmp / "i1" / f).is_file() for f in ("intake_report.md", "studio_ledger.json", "approved_template.json", "orientation_index.png")),
         "intake writes the report, ledger, approval template and orientation index")
    want(all(js.sha256((tmp / "i1" / m["extracted_as"]).read_bytes()) == m["sha256"]
             for m in src["members"] if m.get("extracted_as")), "extracted originals keep their exact bytes")
    want(src["style_exemplars"]["status"] in ("PINNED", "STYLE_REFERENCE_PIXELS_PENDING"), "style exemplar status is reported, never assumed")
    want(refused(lambda: js.intake(z, tmp / "i1"), "not empty"), "intake refuses to write into a non-empty directory")

    bad = copy.deepcopy(man)
    bad["jutsu"][1]["sha256"] = "0" * 64
    entries = [(r["file"], png(i)) for i, r in enumerate(man["jutsu"])] + [("manifest.json", json.dumps(bad).encode())]
    (tmp / "p2.zip").write_bytes(raw_zip(entries))
    code = js.intake(tmp / "p2.zip", tmp / "i2")
    src = json.loads((tmp / "i2" / "source_index.json").read_text())
    want(code == 1 and src["jutsu"][1]["mapping"] == "HASH_MISMATCH", "an altered hash is reported as HASH_MISMATCH (exit 1)")

    bad = copy.deepcopy(man)
    bad["jutsu"][2]["file"] = "art/missing.png"
    entries = [(r["file"], png(i)) for i, r in enumerate(man["jutsu"])] + [("manifest.json", json.dumps(bad).encode())]
    (tmp / "p3.zip").write_bytes(raw_zip(entries))
    code = js.intake(tmp / "p3.zip", tmp / "i3")
    src = json.loads((tmp / "i3" / "source_index.json").read_text())
    want(code == 1 and any(i["code"] == "MISSING_MAPPED_FILE" for i in src["issues"]), "a missing mapped file is an error")

    bad = copy.deepcopy(man)
    bad["jutsu"][1]["jutsu_id"] = "ID0"
    (tmp / "p4.zip").write_bytes(raw_zip([("manifest.json", json.dumps(bad).encode())]))
    want(refused(lambda: js.intake(tmp / "p4.zip", tmp / "i4"), "duplicate jutsu_id"), "a duplicate roster jutsu_id is refused")
    (tmp / "p5.zip").write_bytes(raw_zip([("manifest.json", json.dumps({"jutsu": "nope"}).encode())]))
    want(refused(lambda: js.intake(tmp / "p5.zip", tmp / "i5"), "non-empty 'jutsu' array"), "a manifest schema mismatch is refused")

    loose = raw_zip([("Crimson_Tide.png", png(1)), ("iron-veil_v2.jpg", jpeg(2)), ("ghost step.PNG", jpeg(3)), ("cover.png", png(4))])
    (tmp / "p6.zip").write_bytes(loose)
    code = js.intake(tmp / "p6.zip", tmp / "i6")
    src = json.loads((tmp / "i6" / "source_index.json").read_text())
    want(code == 3 and src["n"] is None and src["n_status"] == "UNKNOWN_NO_ROSTER", "a loose pack without a roster reports N unknown (exit 3)")
    disguised = [m for m in src["members"] if m["path"] == "ghost step.PNG"][0]
    want(disguised["decoded_format"] == "JPEG" and disguised["suffix_matches"] is False and disguised["role"] == "unmapped",
         "a JPEG named .PNG is detected by its bytes and kept, not rejected")

    roster = tmp / "roster.csv"
    roster.write_text("jutsu_id,name\nR1,Crimson Tide\nR2,Iron Veil\nR3,Ghost Step\nR4,Silent Bloom\n")
    code = js.intake(tmp / "p6.zip", tmp / "i7", roster_path=roster)
    src = json.loads((tmp / "i7" / "source_index.json").read_text())
    maps = {j["name"]: j["mapping"] for j in src["jutsu"]}
    want(maps["Crimson Tide"] == "NAME_MATCH" and maps["Iron Veil"] == "NAME_MATCH" and maps["Ghost Step"] == "NAME_MATCH",
         "a CSV roster maps loose files by exact normalized name only")
    want(maps["Silent Bloom"] == "MAPPING_REQUIRED" and code == 3, "a roster jutsu with no file is MAPPING_REQUIRED, never guessed")
    want(any(m["path"] == "cover.png" and m["role"] == "unmapped" for m in src["members"]), "an unclaimed image is listed as unmapped, not discarded")
    ledger = json.loads((tmp / "i7" / "studio_ledger.json").read_text())
    want(all(r["gates"]["RAW_VISUAL_APPROVED"] == "PENDING" for r in ledger["rows"]), "a fresh ledger starts every approval gate PENDING")

    amb = raw_zip([("ghost_step.png", png(1)), ("Ghost-Step.jpg", jpeg(2))])
    (tmp / "p8.zip").write_bytes(amb)
    r2 = tmp / "r2.csv"
    r2.write_text("jutsu_id,name\nG1,Ghost Step\n")
    js.intake(tmp / "p8.zip", tmp / "i8", roster_path=r2)
    src = json.loads((tmp / "i8" / "source_index.json").read_text())
    want(src["jutsu"][0]["mapping"] == "MAPPING_REQUIRED" and len(src["jutsu"][0]["candidates"]) == 2,
         "two files matching one name are MAPPING_REQUIRED with both candidates listed")

    conv = raw_zip([("icon_tl_crimson_tide_v2.webp", png(1)), ("icon_tl_iron_veil_v1.webp", png(2)), ("icon_tl_ghost_step_v1.webp", png(3))])
    (tmp / "p8b.zip").write_bytes(conv)
    r2b = tmp / "r2b.csv"
    r2b.write_text("jutsu_id,name\nA,Crimson Tide\nB,Iron Veil\nC,Ghost Step\n")
    code = js.intake(tmp / "p8b.zip", tmp / "i8b", roster_path=r2b)
    src = json.loads((tmp / "i8b" / "source_index.json").read_text())
    want(code == 0 and all(j["mapping"] == "NAME_MATCH" for j in src["jutsu"]),
         "the icon_<family>_<slug>_vN convention maps by exact name")
    same_word = raw_zip([("crimson_tide.png", png(1)), ("crimson_veil.png", png(2))])
    (tmp / "p8c.zip").write_bytes(same_word)
    r2c = tmp / "r2c.csv"
    r2c.write_text("jutsu_id,name\nA,Crimson Tide\nB,Crimson Veil\n")
    code = js.intake(tmp / "p8c.zip", tmp / "i8c", roster_path=r2c)
    src = json.loads((tmp / "i8c" / "source_index.json").read_text())
    want(code == 0 and all(j["mapping"] == "NAME_MATCH" for j in src["jutsu"]),
         "a real first word shared by every file name is not stripped away")

    r3 = tmp / "r3.json"
    r3.write_text(json.dumps({"jutsu": [{"jutsu_id": "ID0", "name": "Crimson Tide"}, {"jutsu_id": "ID1", "name": "Iron Veil"},
                                        {"jutsu_id": "ID9", "name": "Ghost Step"}]}))
    code = js.intake(z, tmp / "i9", roster_path=r3)
    src = json.loads((tmp / "i9" / "source_index.json").read_text())
    want(code == 1 and sum(i["code"] == "ROSTER_CONFLICT" for i in src["issues"]) >= 2,
         "a director roster that disagrees with the ZIP manifest is a conflict, not silently merged")

    big = Image.new("L", (8000, 7000))
    buf = io.BytesIO()
    big.save(buf, "PNG")
    (tmp / "p10.zip").write_bytes(raw_zip([("huge.png", buf.getvalue())]))
    js.intake(tmp / "p10.zip", tmp / "i10")
    src = json.loads((tmp / "i10" / "source_index.json").read_text())
    want(any(i["code"] == "UNDECODABLE_IMAGE" and "pixel" in i["message"] for i in src["issues"]),
         "an oversized image is refused by the pixel bound")


# ---------------------------------------------------------------------------------------------


def run_layout_tests() -> None:
    print("\nshowcase layout")
    want(js.grid_rows(5) == [3, 2], "N=5 is 3+2")
    want(js.grid_rows(8) == [4, 4], "N=8 is 4+4")
    want(js.grid_rows(12) == [4, 4, 4], "N=12 is 4+4+4")
    want(js.grid_rows(7) == [4, 3] and js.grid_rows(4) == [2, 2] and js.grid_rows(9) == [3, 3, 3], "N=4/7/9 follow the table")
    want(js.grid_rows(10) == [4, 3, 3] and js.grid_rows(11) == [4, 4, 3] and js.grid_rows(13) == [4, 3, 3, 3],
         "N>=10 is balanced, at most four per row, longer rows first (D5)")
    ok = True
    for n in range(1, 17):
        rows = js.grid_rows(n)
        ok &= sum(rows) == n and max(rows) <= 4 and max(rows) - min(rows) <= 1
        if n >= 10:
            ok &= rows == sorted(rows, reverse=True) and min(rows) >= 3
    want(ok, "N=1..16: every icon placed once, rows differ by at most one, no lone final tile for N>=10")
    want(js.caption_kb(79999) == "80.0kB" and js.caption_kb(84216) == "84.2kB", "captions are bytes/1000 to one decimal")


# ---------------------------------------------------------------------------------------------


def family(tmp: Path, n: int, name="fam", size=512, cap=None, tag=""):
    root = tmp / f"{name}{tag}"
    (root / "raws").mkdir(parents=True)
    rows = []
    for i in range(n):
        p = root / "raws" / f"r{i}.png"
        js.synth_image(i + 7, size).save(p, "PNG")
        rows.append({"jutsu_id": f"J{i}", "name": f"Technique Number {i + 1}", "slug": f"technique_{i + 1}", "version": 1,
                     "raw_file": f"raws/r{i}.png", "raw_sha256": js.file_sha(p),
                     "director_raw_approval": {"status": "APPROVED", "evidence": "fixture approval"},
                     "quantize": None, "superseded_raw_sha256": []})
    doc = {"schema": "tnr.jutsu-studio.approved/1", "bloodline": {"id": "BLX", "name": "Fixture Line", "family": name},
           "family_byte_cap_exclusive": cap, "family_byte_cap_ruling": "RUL-fixture" if cap else None,
           "family_acceptance": {"status": "PENDING", "evidence": ""}, "jutsu": rows}
    path = root / "approved.json"
    path.write_text(json.dumps(doc))
    return root, path, doc


def rewrite(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc))


def run_finalize_tests(tmp: Path, spec: dict, nums: dict) -> None:
    print("\napproved ledger")
    root, path, doc = family(tmp, 3)
    plan = js.verify_approved(path, spec)
    want(len(plan["rows"]) == 3, "a clean approved ledger verifies")
    checks = [
        ("duplicate jutsu_id", lambda d: d["jutsu"][1].__setitem__("jutsu_id", "J0"), "duplicate jutsu_id"),
        ("unapproved raw", lambda d: d["jutsu"][0]["director_raw_approval"].__setitem__("status", "PENDING"), "director_raw_approval"),
        ("approval without evidence", lambda d: d["jutsu"][0]["director_raw_approval"].__setitem__("evidence", " "), "director_raw_approval"),
        ("wrong raw hash", lambda d: d["jutsu"][0].__setitem__("raw_sha256", "a" * 64), "does not match"),
        ("superseded raw", lambda d: d["jutsu"][2].__setitem__("superseded_raw_sha256", [d["jutsu"][0]["raw_sha256"]]), "superseded"),
        ("missing raw", lambda d: d["jutsu"][0].__setitem__("raw_file", "raws/nope.png"), "not found"),
        ("traversing raw path", lambda d: d["jutsu"][0].__setitem__("raw_file", "../x.png"), "without '..'"),
        ("cap without ruling", lambda d: d.update(family_byte_cap_exclusive=80000, family_byte_cap_ruling=None), "director decision"),
        ("quantize without approval", lambda d: d["jutsu"][0].__setitem__("quantize", {"method": "MEDIANCUT", "colors": 256}), "director_approved"),
        ("bad slug", lambda d: d["jutsu"][0].__setitem__("slug", "Bad Slug"), "slug"),
        ("family accepted without evidence", lambda d: d.__setitem__("family_acceptance", {"status": "ACCEPTED", "evidence": "", "gallery_sha256": "a" * 64, "members_sha256": "b" * 64}), "evidence"),
        ("family accepted without a gallery sha", lambda d: d.__setitem__("family_acceptance", {"status": "ACCEPTED", "evidence": "director said yes", "members_sha256": "b" * 64}), "gallery_sha256"),
        ("family accepted without a members commitment", lambda d: d.__setitem__("family_acceptance", {"status": "ACCEPTED", "evidence": "director said yes", "gallery_sha256": "a" * 64}), "members_sha256"),
    ]
    for label, mutate, needle in checks:
        d = copy.deepcopy(doc)
        mutate(d)
        rewrite(path, d)
        want(refused(lambda: js.verify_approved(path, spec), needle), f"{label} is refused")
    rewrite(path, doc)

    def raw_variant(label, img, needle):
        p = root / "raws" / f"variant_{label}.png"
        img.save(p, "PNG")
        d = copy.deepcopy(doc)
        d["jutsu"][0].update(raw_file=f"raws/{p.name}", raw_sha256=js.file_sha(p))
        rewrite(path, d)
        want(refused(lambda: js.verify_approved(path, spec), needle), f"a {label} raw is refused")
        rewrite(path, doc)

    raw_variant("non-square", js.synth_image(1, 512).resize((512, 400)), "square")
    raw_variant("too-small", js.synth_image(1, 128), "no upscaling")
    t = js.synth_image(1, 512).convert("RGBA")
    t.putpixel((3, 3), (0, 0, 0, 0))
    raw_variant("transparent", t, "transparency")

    src_index = tmp / "si.json"
    src_index.write_text(json.dumps({"jutsu": [{"jutsu_id": f"J{i}", "name": f"Technique Number {i + 1}"} for i in range(4)]}))
    want(refused(lambda: js.verify_approved(path, spec, source_index=src_index), "silent omission"),
         "an approved set missing a roster jutsu is refused (no silent omission)")

    print("\nexport, preflight, showcase, pack")
    raw_before = {r["raw_file"]: js.file_sha(root / r["raw_file"]) for r in doc["jutsu"]}
    res = js.finalize(path, root / "out", label="v1")
    want(all(e["verdict"] == "PASS" and e["checks"]["codec"] == "VP8L" and e["checks"]["size"] == [nums["size"]] * 2
             for e in res["exports"]), "exports are lossless VP8L RGB at the spec size")
    want(all(e["checks"]["pixels_equal_transformed"] for e in res["exports"]), "export pixels equal the approved transformed pixels")
    want({r["raw_file"]: js.file_sha(root / r["raw_file"]) for r in doc["jutsu"]} == raw_before, "approved raws are never modified")
    want(res["preflight"]["verdict"] == "PASS" and res["preflight"]["exit_code"] == 0 and "--type JUTSU_ICON" in res["preflight"]["command"],
         "the real artpreflight.py runs with --type JUTSU_ICON and passes")
    sc = res["showcase"]
    want(sc["row_lengths"] == [3] and sc["tile_pixel_equality"]["all_equal"] and sc["tile_pixel_equality"]["tiles"] == 3,
         "the N=3 showcase is one row, audited pixel-equal from its written bytes")
    want(all(i["caption"].endswith(js.caption_kb((root / "out" / "exports" / i["output_filename"]).stat().st_size)) for i in sc["icons"]),
         "every caption carries the real export bytes/1000")
    want(sc["director_family_acceptance"]["status"] == "PENDING", "family acceptance stays PENDING unless the director recorded it")
    closeout = root / "out" / "dist" / res["archives"]["closeout"]["file"]
    zf = zipfile.ZipFile(closeout)
    sums = dict(reversed(line.split("  ", 1)) for line in zf.read("SHA256SUMS").decode().splitlines())
    want(zf.testzip() is None and all(js.sha256(zf.read(n)) == h for n, h in sums.items()) and len(sums) == len(zf.namelist()) - 1,
         "the closeout ZIP passes CRC and every member matches SHA256SUMS")
    flat = res["archives"]["webps"]["file"]
    want(sorted(zipfile.ZipFile(root / "out" / "dist" / flat).namelist()) == sorted(e["output"] for e in res["exports"]),
         "the flat WebP ZIP is exactly the N current WebPs")
    want("upload" not in flat and "_PREFLIGHT_PASS_" in flat and not any("upload" in a["file"] for a in res["archives"].values()),
         "no archive is named 'upload'; the flat ZIP carries the preflight verdict (D6)")
    ledger = json.loads((root / "out" / "studio_ledger.json").read_text())
    want(all(r["gates"]["USER_UPLOAD_READBACK"] == "NOT_PERFORMED" and r["gates"]["GIT_BINARY_PIN"] == "NOT_PERFORMED" for r in ledger["rows"]),
         "the ledger never claims upload, read-back or Git pinning")
    want(all(list(r["gates"]) == list(js.GATES) for r in ledger["rows"]) and set(ledger["collection_gates"]) == set(js.GATES),
         "per-icon and collection gates use exactly the K vocabulary (D7)")

    res_again = js.finalize(path, root / "out", label="v1")
    want(res_again["cache"]["encoded"] == 0 and res_again["cache"]["reused"] == 3 and res_again["archives"]["closeout"]["state"] == "UNCHANGED",
         "an identical rerun reuses every export and leaves the archive unchanged")
    other = js.finalize(path, root / "out_replay", label="v1")
    want(other["archives"]["closeout"]["sha256"] == res["archives"]["closeout"]["sha256"],
         "a fresh replay produces a byte-identical closeout ZIP")

    print("\nincremental rerun and refusals")
    d = copy.deepcopy(doc)
    p = root / "raws" / "r1_new.png"
    js.synth_image(500, 512).save(p, "PNG")
    d["jutsu"][1].update(raw_file="raws/r1_new.png", raw_sha256=js.file_sha(p))
    rewrite(path, d)
    want(refused(lambda: js.finalize(path, root / "out", label="v2"), "Bump that jutsu's version"),
         "a changed raw under the same versioned filename is refused")
    d["jutsu"][1].update(version=2, superseded_raw_sha256=[doc["jutsu"][1]["raw_sha256"]])
    rewrite(path, d)
    res2 = js.finalize(path, root / "out", label="v2")
    want(res2["cache"]["encoded"] == 1 and res2["cache"]["reused"] == 2, "changing one approved raw re-encodes only that icon")
    old_zip = closeout.read_bytes()
    want(refused(lambda: js.finalize(path, root / "out", label="v1"), "Use a new --label"),
         "reusing an archive label for changed contents is refused")
    want(closeout.read_bytes() == old_zip, "the earlier archive is untouched by the refused run")
    want((root / "out" / "exports" / "icon_fam_technique_2_v1.webp").is_file(), "the superseded export is preserved, not deleted")
    want(res2["showcase"]["gallery"]["sha256"] != res["showcase"]["gallery"]["sha256"], "the derived showcase is rebuilt for the changed family")

    tampered = root / "out" / "exports" / "icon_fam_technique_1_v1.webp"
    keep = tampered.read_bytes()
    tampered.write_bytes(keep[:-1] + bytes([keep[-1] ^ 1]))
    want(refused(lambda: js.finalize(path, root / "out", label="v3"), "modified after export"), "a tampered cached export is refused")
    tampered.write_bytes(keep)

    rec = root / "out" / "cache" / "icon_fam_technique_3_v1.webp.json"
    tgt = root / "out" / "exports" / "icon_fam_technique_3_v1.webp"
    saved = tgt.read_bytes()
    tgt.unlink()
    res3 = js.finalize(path, root / "out", label="v2")
    want(tgt.read_bytes() == saved and res3["cache"]["encoded"] == 1, "an interrupted export (record written, file missing) is re-encoded identically")
    rec_saved = rec.read_bytes()
    rec.unlink()
    want(refused(lambda: js.finalize(path, root / "out", label="v2"), "unknown provenance"), "an export with no cache record is never adopted")
    rec.write_bytes(rec_saved)

    print("\nbyte caps and quantization")
    size0 = res["exports"][0]["output_bytes"]
    for cap, ok in ((size0, False), (size0 + 1, True)):
        r4, p4, d4 = family(tmp, 1, name="capf", cap=cap, tag=str(cap))
        if ok:
            out = js.finalize(p4, r4 / "out", label="v1", stop_after="preflight")
            want(out["preflight"]["verdict"] == "PASS" and f"--max-bytes {cap}" in out["preflight"]["command"],
                 f"a {size0}-byte export passes an exclusive cap of {cap} (and preflight gets --max-bytes)")
        else:
            want(refused(lambda: js.finalize(p4, r4 / "out", label="v1"), "not under the family cap"),
                 f"a {size0}-byte export fails an exclusive cap of {cap}")
    r5, p5, d5 = family(tmp, 1, name="quant")
    d5["jutsu"][0]["quantize"] = {"method": "MEDIANCUT", "colors": 64, "director_approved": "fixture: director accepted 125/64/32 comparison"}
    rewrite(p5, d5)
    out5 = js.finalize(p5, r5 / "out", label="v1", stop_after="export")
    e5 = out5["exports"][0]
    with Image.open(r5 / "out" / "exports" / e5["output"]) as im:
        colours = len(im.getcolors(1 << 16) or [])
    want(e5["verdict"] == "PASS" and e5["checks"]["pixels_equal_transformed"] and colours <= 64 and e5["quantize"]["colors"] == 64,
         "director-approved quantization is applied, recorded, and lossless relative to the quantized pixels")

    print("\ncanonical preflight evidence")
    exp = [root / "out" / "exports" / e["output"] for e in res["exports"]]
    nr = js.run_preflight(exp, js.DEFAULT_SPEC, None, tmp / "no_such_preflight.py")
    want(nr["verdict"] == "NOT_RUN", "a missing preflight script is NOT_RUN, never a pass")
    fake = tmp / "fake_ok.py"
    fake.write_text("print('all good')\n")
    want(js.run_preflight(exp, js.DEFAULT_SPEC, None, fake)["verdict"] == "FAIL", "exit 0 without the JSON evidence is FAIL, not PASS")
    fake2 = tmp / "fake_partial.py"
    fake2.write_text("import json;print(json.dumps({'rows':[],'errors':0}))\n")
    want(js.run_preflight(exp, js.DEFAULT_SPEC, None, fake2)["verdict"] == "FAIL", "a preflight that did not inspect every file is FAIL")
    fake3 = tmp / "fake_errors.py"
    fake3.write_text("import json,sys,os\nfiles=[a for a in sys.argv[1:] if a.endswith('.webp')]\n"
                     "print(json.dumps({'rows':[{'level':'error','file':os.path.basename(f),'check':'x','message':'m'} for f in files],'errors':len(files)}))\n"
                     "sys.exit(len(files))\n")
    want(js.run_preflight(exp, js.DEFAULT_SPEC, None, fake3)["verdict"] == "FAIL", "reported preflight errors are FAIL")
    fake4 = tmp / "fake_mismatch.py"
    fake4.write_text("import json,sys,os\nfiles=[a for a in sys.argv[1:] if a.endswith('.webp')]\n"
                     "print(json.dumps({'rows':[{'level':'note','file':os.path.basename(f),'check':'x','message':'m'} for f in files],'errors':1}))\n")
    want(js.run_preflight(exp, js.DEFAULT_SPEC, None, fake4)["verdict"] == "FAIL", "exit 0 with a nonzero error count is still FAIL")


# ---------------------------------------------------------------------------------------------
# P1 (RUL-2026-10-19-005): source fidelity, provenance, target lock, attempts, compare, doctor
# ---------------------------------------------------------------------------------------------


def expect_raise(fn) -> str:
    try:
        fn()
    except js.StudioError as exc:
        return str(exc)
    return ""


def png_of(img) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def lock_doc(names: list[str], approve: bool = True) -> dict:
    targets = []
    for i, n in enumerate(names):
        tg = {"jutsu_id": f"J{i}", "name": n, "version": 1, "evidence_level": "director_roster",
              "action": f"technique {i} strikes", "dominant_silhouette": f"shape {i}",
              "camera": "frontal, near camera", "motion_axis": "toward viewer", "secondary_effect": "particle trail",
              "sibling_exclusions": [{"jutsu_id": f"J{k}", "silhouette": f"shape {k}"} for k in range(len(names)) if k != i],
              "references": [{"sha256": f"{i:x}" * 64 if i < 10 else "c" * 64, "role": "identity-only", "kind": "individual"}],
              "anatomy_exception": None, "direction_approval": {"status": "PENDING", "evidence": ""}}
        if approve:
            tg["direction_approval"] = {"status": "APPROVED", "evidence": "fixture director approval",
                                        "lock_sha256": js.lock_sha(tg)}
        targets.append(tg)
    return {"schema": "tnr.jutsu-studio.locks/1", "bloodline": {"id": "BLX", "name": "Fixture Line"}, "targets": targets}


def reapprove(tg: dict) -> None:
    tg["direction_approval"] = {"status": "APPROVED", "evidence": "fixture re-approval", "lock_sha256": js.lock_sha(tg)}


def attempt(jid, n, sid, outcome, reasons=(), sha=None, **kw) -> dict:
    a = {"jutsu_id": jid, "attempt": n, "session_id": sid, "outcome": outcome, "reasons": list(reasons),
         "candidate_sha256": sha}
    a.update(kw)
    return a


def run_p1_tests(tmp: Path, spec: dict, nums: dict) -> None:
    base = tmp / "p1"
    base.mkdir()

    print("\nP1 family acceptance binds to the exact gallery (G1)")
    root, path, doc = family(base, 3, name="acc")
    r1 = js.finalize(path, root / "out", label="v1")
    g1 = r1["showcase"]["gallery"]["sha256"]
    m1 = r1["showcase"]["members_sha256"]
    p1 = r1["showcase"]["gallery"]["pixels_sha256"]
    d = copy.deepcopy(doc)
    d["family_acceptance"] = {"status": "ACCEPTED", "evidence": "fixture: director accepted v1 sheet", "gallery_sha256": g1,
                              "gallery_pixels_sha256": p1, "members_sha256": m1}
    rewrite(path, d)
    r2 = js.finalize(path, root / "out", label="v1acc")
    want(r2["showcase"]["director_family_acceptance"]["status"] == "ACCEPTED"
         and r2["showcase"]["gallery"]["sha256"] == g1, "acceptance applies to the gallery whose sha it names")
    newraw = root / "raws" / "r0_new.png"
    js.synth_image(777, 512).save(newraw, "PNG")
    d["jutsu"][0].update(raw_file="raws/r0_new.png", raw_sha256=js.file_sha(newraw), version=2,
                         superseded_raw_sha256=[doc["jutsu"][0]["raw_sha256"]])
    rewrite(path, d)
    r3 = js.finalize(path, root / "out", label="v2")
    acc = r3["showcase"]["director_family_acceptance"]
    want(acc["status"] == "INVALIDATED" and acc["recorded_gallery_sha256"] == g1
         and all(r["gates"]["FAMILY_SHOWCASE_ACCEPTED"] == "INVALIDATED" for r in r3["ledger"]["rows"]),
         "a changed raw invalidates the earlier acceptance instead of inheriting it")
    d["family_acceptance"] = {"status": "REJECTED", "evidence": "fixture", "gallery_sha256": g1, "members_sha256": m1}
    rewrite(path, d)
    r4 = js.finalize(path, root / "out", label="v2rej")
    want(r4["showcase"]["director_family_acceptance"]["status"] == "PENDING",
         "a rejection of an older gallery leaves the new gallery PENDING, not REJECTED")

    print("\nF1 acceptance binds to member bytes, not only gallery pixels")
    from PIL import PngImagePlugin
    d = copy.deepcopy(doc)
    d["family_acceptance"] = {"status": "ACCEPTED", "evidence": "fixture", "gallery_sha256": g1,
                              "gallery_pixels_sha256": p1, "members_sha256": m1}
    meta = root / "raws" / "r0_meta.png"
    info = PngImagePlugin.PngInfo()
    info.add_text("Comment", "metadata only")
    with Image.open(root / doc["jutsu"][0]["raw_file"]) as im:
        im.save(meta, "PNG", pnginfo=info)
    with Image.open(meta) as a, Image.open(root / doc["jutsu"][0]["raw_file"]) as b:
        same_pixels = a.convert("RGB").tobytes() == b.convert("RGB").tobytes()
    d["jutsu"][0].update(raw_file="raws/r0_meta.png", raw_sha256=js.file_sha(meta), version=3,
                         superseded_raw_sha256=[doc["jutsu"][0]["raw_sha256"]])
    rewrite(path, d)
    r5 = js.finalize(path, root / "out", label="v3meta")
    a5 = r5["showcase"]["director_family_acceptance"]
    want(same_pixels and js.file_sha(meta) != doc["jutsu"][0]["raw_sha256"] and r5["showcase"]["gallery"]["sha256"] == g1
         and a5["status"] == "INVALIDATED" and not a5["members_match"] and a5["gallery_match"] == "file",
         "a metadata-only raw re-encode keeps identical gallery pixels/bytes yet INVALIDATES the acceptance")
    icons = r1["showcase"]["icons"]
    rec = {"status": "ACCEPTED", "gallery_sha256": g1, "gallery_pixels_sha256": p1, "members_sha256": m1}
    want(js.acceptance_for(rec, "e" * 64, p1, m1)["status"] == "ACCEPTED"
         and js.acceptance_for(rec, "e" * 64, p1, m1)["matched_by"] == "pixels",
         "a re-encoded gallery container with identical pixels and members stays ACCEPTED (pixel domain)")
    cross = {"status": "ACCEPTED", "gallery_sha256": p1, "members_sha256": m1}
    want(js.acceptance_for(cross, "e" * 64, p1, m1)["status"] == "INVALIDATED",
         "a recorded file sha is never compared with a pixel sha (no cross-domain match)")
    swapped = copy.deepcopy(icons)
    swapped[1]["output_sha256"] = "f" * 64
    want(js.acceptance_for(rec, g1, p1, js.members_commitment(swapped))["status"] == "INVALIDATED",
         "a pixel-equivalent but byte-different export invalidates the acceptance")
    want(js.acceptance_for({"status": "ACCEPTED", "gallery_sha256": g1}, g1, p1, m1)["status"] == "INVALIDATED",
         "an acceptance without a members commitment never matches")
    rewrite(path, doc)

    print("\nP1 every stage re-proves its inputs (G2, G3)")
    root, path, doc = family(base, 3, name="swap")
    exports = root / "out" / "exports"

    def swap_export(stage_name):
        def hook(stage):
            if stage == stage_name:
                f = sorted(exports.glob("*.webp"))[0]
                img = js.synth_image(4242, nums["size"])
                f.write_bytes(js.encode_webp(img))
        return hook

    msg = expect_raise(lambda: js.finalize(path, root / "out", label="s1", on_stage=swap_export("export")))
    want("not the recorded bytes" in msg, "an export swapped after the export stage is refused before preflight")
    shutil.rmtree(root / "out")
    msg = expect_raise(lambda: js.finalize(path, root / "out", label="s1", on_stage=swap_export("preflight")))
    want("not the recorded bytes" in msg and not (root / "out" / "showcase").exists(),
         "an export swapped between preflight and showcase is refused; no gallery is written")
    shutil.rmtree(root / "out")
    good = js.finalize(path, root / "out", label="s1")
    good_zip = (root / "out" / "dist" / good["archives"]["closeout"]["file"]).read_bytes()
    raw0 = root / doc["jutsu"][0]["raw_file"]
    keep = raw0.read_bytes()

    def swap_raw(stage):
        if stage == "showcase":
            js.synth_image(99, 512).save(raw0, "PNG")

    msg = expect_raise(lambda: js.finalize(path, root / "out", label="s2", on_stage=swap_raw))
    raw0.write_bytes(keep)
    want("approved raw" in msg and "not the recorded bytes" in msg and
         not any("_s2" in f.name for f in (root / "out" / "dist").iterdir()),
         "a raw swapped between showcase and pack is refused and no archive is written")
    want((root / "out" / "dist" / good["archives"]["closeout"]["file"]).read_bytes() == good_zip,
         "the earlier archive stays byte-identical")

    print("\nP1 audit-gallery (G4, G14)")
    sdir = root / "out" / "showcase"
    man = json.loads((sdir / "showcase_manifest.json").read_text())
    gal = (sdir / man["gallery"]["file"]).read_bytes()
    au = js.audit_gallery(gal, man, exports)
    want(au["verdict"] == "VALID" and all(x["pixel_equal"] for x in au["tiles"]), "the deterministic gallery audits VALID")
    with Image.open(io.BytesIO(gal)) as im:
        canvas = im.convert("RGB")
    pos = [ic["position"] for ic in man["icons"]]
    T = js.TILE

    def variant(mutate):
        c = canvas.copy()
        mutate(c)
        return js.audit_gallery(png_of(c), man, exports)

    def onepx(c):
        x, y = pos[0]["x"] + 5, pos[0]["y"] + 5
        r, g, b = c.getpixel((x, y))
        c.putpixel((x, y), ((r + 1) % 256, g, b))

    v = variant(onepx)
    want(v["verdict"] == "INVALID" and any("row 1 col 1" in x for x in v["problems"]), "a single altered tile pixel is INVALID, naming the tile")
    v = variant(lambda c: c.paste(c.crop((pos[1]["x"], pos[1]["y"], pos[1]["x"] + T, pos[1]["y"] + T)), (pos[0]["x"], pos[0]["y"])))
    want(v["verdict"] == "INVALID", "a tile replaced by its sibling is INVALID")

    def recolour(c):
        box = (pos[2]["x"], pos[2]["y"], pos[2]["x"] + T, pos[2]["y"] + T)
        r, g, b = c.crop(box).split()
        c.paste(Image.merge("RGB", (b, g, r)), box[:2])

    want(variant(recolour)["verdict"] == "INVALID", "a recoloured tile is INVALID")

    def lookalike(c):
        box = (pos[0]["x"], pos[0]["y"], pos[0]["x"] + T, pos[0]["y"] + T)
        regen = c.crop(box).resize((T // 2, T // 2), Image.BILINEAR).resize((T, T), Image.BICUBIC)
        c.paste(regen, box[:2])

    want(variant(lookalike)["verdict"] == "INVALID", "a regenerated lookalike tile is INVALID")
    v = variant(lambda c: c.putpixel((pos[0]["x"] + 3, pos[0]["y"] + T + 30), (255, 0, 0)))
    want(v["verdict"] == "INVALID" and any("non-tile" in x for x in v["problems"]), "an edited caption/background pixel is INVALID")
    m2 = copy.deepcopy(man)
    m2["icons"][0]["caption"] = m2["icons"][0]["caption"].replace("kB", "KiB")
    want(js.audit_gallery(gal, m2, exports)["verdict"] == "INVALID", "a KiB or wrong-size caption is INVALID")
    m2 = copy.deepcopy(man)
    m2["icons"][0]["output_bytes"] += 1000
    want(js.audit_gallery(gal, m2, exports)["verdict"] == "INVALID", "a manifest byte count that disagrees with the export is INVALID")
    m2 = copy.deepcopy(man)
    m2["icons"][0], m2["icons"][1] = m2["icons"][1], m2["icons"][0]
    want(js.audit_gallery(gal, m2, exports)["verdict"] == "INVALID", "swapped tile order is INVALID")
    m2 = copy.deepcopy(man)
    m2["icons"][1] = copy.deepcopy(m2["icons"][0])
    want(js.audit_gallery(gal, m2, exports)["verdict"] == "INVALID", "a duplicated tile is INVALID")
    m2 = copy.deepcopy(man)
    m2["icons"].pop()
    want(js.audit_gallery(gal, m2, exports)["verdict"] == "INVALID", "a missing tile is INVALID")
    buf = io.BytesIO()
    canvas.save(buf, "PNG", compress_level=1)
    v = js.audit_gallery(buf.getvalue(), man, exports)
    want(v["verdict"] == "VALID" and any("pixels are identical" in x for x in v["notes"]),
         "a re-encoded PNG with identical pixels is VALID with the byte difference noted")
    want(js.audit_gallery(b"not an image", man, exports)["verdict"] == "INVALID", "an undecodable gallery is INVALID")
    rc = js.main(["audit-gallery", str(sdir / man["gallery"]["file"]), "--manifest", str(sdir / "showcase_manifest.json"),
                  "--exports", str(exports)])
    want(rc == 0, "audit-gallery CLI exits 0 on VALID")

    print("\nP1 canonical preflight pins (G8, D9) and archive naming (G6, D6)")
    st = js.canonical_status(js.DEFAULT_PREFLIGHT, js.DEFAULT_SPEC)
    want(st["canonical"], "the shipped artpreflight.py and art spec match data/preflight_pins.json (re-pin when either changes)")
    tweaked = tmp / "artpreflight.py"
    tweaked.write_bytes(js.DEFAULT_PREFLIGHT.read_bytes() + b"\n# local edit\n")
    ex = [exports / e["output"] for e in good["exports"]]
    rec = js.run_preflight(ex, js.DEFAULT_SPEC, None, tweaked)
    want(rec["verdict"] == "NON_CANONICAL" and rec["exit_code"] == 0, "a locally edited artpreflight.py that reports 0 errors is NON_CANONICAL, not PASS")
    spec2 = tmp / "spec_copy.json"
    spec2.write_bytes(js.DEFAULT_SPEC.read_bytes() + b"\n")
    want(js.run_preflight(ex, spec2, None)["verdict"] == "NON_CANONICAL", "a spec that is not the pinned blob is NON_CANONICAL")
    want(js.run_preflight(ex, js.DEFAULT_SPEC, None, pins=tmp / "no_pins.json")["verdict"] == "NON_CANONICAL",
         "missing pins mean canonical status cannot be proven")
    root_n, path_n, _ = family(base, 2, name="nrun")
    rn = js.finalize(path_n, root_n / "out", label="v1", preflight_script=tmp / "absent.py")
    fname = rn["archives"]["webps"]["file"]
    want("_PREFLIGHT_NOT_RUN_" in fname and "upload" not in fname
         and all(r["gates"]["CANONICAL_PREFLIGHT"] == "NOT_RUN" for r in rn["ledger"]["rows"]),
         "with preflight NOT_RUN the flat ZIP is named PREFLIGHT_NOT_RUN and the gate says so")
    rnc = js.finalize(path_n, root_n / "out", label="v2", preflight_script=tweaked)
    want("_PREFLIGHT_NON_CANONICAL_" in rnc["archives"]["webps"]["file"], "a non-canonical run is named NON_CANONICAL")

    print("\nP1 doctor")
    dr = js.doctor()
    want(dr["verdict"] == "RUN_CAPABLE_CANONICAL" and all(c["ok"] for c in dr["checks"]),
         "doctor proves the canonical path runs here (real artpreflight probe)")
    want(js.doctor(script=tweaked)["verdict"].startswith("RUN_CAPABLE_NON_CANONICAL"), "doctor reports a non-pinned script as non-canonical")
    want(js.doctor(script=tmp / "absent.py")["verdict"].startswith("NOT_RUN"), "doctor reports a missing script as NOT_RUN")

    print("\nP1 roster evidence levels (G9)")
    data, _ = manifest_pack(["Alpha Strike", "Beta Wave"])
    zp = base / "ev.zip"
    zp.write_bytes(data)
    js.intake(zp, base / "ev_out")
    si = json.loads((base / "ev_out" / "source_index.json").read_text())
    rep = (base / "ev_out" / "intake_report.md").read_text()
    want(all(j["evidence_level"] == "historical_capture" for j in si["jutsu"]) and "not a current-live check" in rep,
         "a ZIP manifest roster is labelled historical_capture, never current-live")
    roster = base / "roster.csv"
    roster.write_text("jutsu_id,name,file\nID0,Alpha Strike,art/00.png\nID1,Beta Wave,art/01.png\n")
    js.intake(zp, base / "ev_out2", roster)
    si2 = json.loads((base / "ev_out2" / "source_index.json").read_text())
    want(all(j["evidence_level"] == "director_roster" for j in si2["jutsu"]), "a director roster is labelled director_roster")
    data3, man3 = manifest_pack(["Alpha Strike"])
    man3["jutsu"][0]["evidence_level"] = "current_live"
    zp3 = base / "ev3.zip"
    zp3.write_bytes(raw_zip([("art/00.png", png(0)), ("manifest.json", json.dumps(man3).encode())]))
    want(js.intake(zp3, base / "ev_out3") == 1, "a roster claiming 'current_live' is an intake error")
    lg = json.loads((base / "ev_out" / "studio_ledger.json").read_text())
    want(all(list(r["gates"]) == list(js.GATES) and r["gates"]["ORIGINAL_SOURCE_VERIFIED"] == "VERIFIED" for r in lg["rows"]),
         "the intake ledger uses the K gates; hash-verified members are ORIGINAL_SOURCE_VERIFIED")

    print("\nP1 gate table refusals (G10)")
    okg = {"ORIGINAL_SOURCE_VERIFIED": "VERIFIED", "DIRECTION_APPROVED": "APPROVED", "RAW_VISUAL_APPROVED": "APPROVED",
           "OUTPUT_LOCAL_QC": "PASS", "CANONICAL_PREFLIGHT": "PASS", "FAMILY_SHOWCASE_ACCEPTED": "PENDING",
           "ZIP_DELIVERED": "BUILT_NOT_DELIVERED", "GIT_BINARY_PIN": "NOT_PERFORMED", "USER_UPLOAD_READBACK": "NOT_PERFORMED"}
    want(js.check_gates(dict(okg)) == okg, "a consistent gate table is accepted")
    bad_cases = [
        ("CANONICAL_PREFLIGHT PASS without local QC PASS", {"OUTPUT_LOCAL_QC": "FAIL"}),
        ("ZIP built without local QC", {"OUTPUT_LOCAL_QC": "NOT_RUN", "CANONICAL_PREFLIGHT": "NOT_RUN",
                                        "FAMILY_SHOWCASE_ACCEPTED": "NOT_BUILT"}),
        ("tooling claiming a Git pin", {"GIT_BINARY_PIN": "PINNED"}),
        ("tooling claiming upload/read-back", {"USER_UPLOAD_READBACK": "PERFORMED"}),
        ("an export for an unapproved raw", {"RAW_VISUAL_APPROVED": "PENDING"}),
        ("an unknown gate name", {"ARCHIVE_DELIVERED": "NOT_RUN"}),
    ]
    for label, change in bad_cases:
        g = dict(okg)
        g.update(change)
        want(refused(lambda: js.check_gates(g), "inconsistent"), f"gate table refuses {label}")

    print("\nP1 exemplar provenance (G11)")
    sys.path.insert(0, str(js.SCRIPT_DIR))
    import style_refs  # noqa: E402
    idx = json.loads((js.SCRIPT_DIR.parent / "data" / "style_refs.json").read_text())
    jrefs = [r for r in idx["references"] if r.get("target") == "JUTSU_ICON"]
    partial = {r["key"] for r in jrefs if style_refs.provenance_status(r) == "PROVENANCE_PARTIAL"}
    want(partial == {"bee_sanguine_plague"} and len(jrefs) == 16,
         "exactly the BEE sanguine_plague_v3 exemplar is PROVENANCE_PARTIAL among the 16")
    ex_rows = si["style_exemplars"].get("primary", [])
    want(all("provenance" in r for r in ex_rows), "intake exemplar rows carry a provenance field")

    print("\nP1 target lock (P0 A/B)")
    names = ["Technique Number 1", "Technique Number 2", "Technique Number 3"]
    lp = base / "locks.json"
    ld = lock_doc(names)
    lp.write_text(json.dumps(ld))
    li = js.check_locks(lp)
    want(li["approved"] == {"J0", "J1", "J2"} and not li["incomplete"], "a complete, approved lock set checks clean")
    l2 = copy.deepcopy(ld)
    del l2["targets"][0]["camera"]
    l2["targets"][0]["direction_approval"] = {"status": "PENDING", "evidence": ""}
    l2["targets"][1]["sibling_exclusions"].pop()
    reapprove(l2["targets"][1])
    lp.write_text(json.dumps(l2))
    msg = expect_raise(lambda: js.check_locks(lp))
    want("direction APPROVED on an incomplete lock" in msg and "sibling_exclusions for J2" in msg,
         "approval of a lock missing a sibling exclusion is refused")
    l2["targets"][1]["direction_approval"] = {"status": "PENDING", "evidence": ""}
    lp.write_text(json.dumps(l2))
    li2 = js.check_locks(lp)
    want("camera" in li2["incomplete"]["J0"] and any("J2" in m for m in li2["incomplete"]["J1"]),
         "a missing camera/motion field or sibling exclusion is LOCK_INCOMPLETE")
    want(js.main(["lock-check", str(lp)]) == 3, "lock-check exits 3 while any lock is incomplete")
    l3 = copy.deepcopy(ld)
    l3["targets"][2]["dominant_silhouette"] = "something else"
    lp.write_text(json.dumps(l3))
    want(refused(lambda: js.check_locks(lp), "lock changed after DIRECTION_APPROVED"), "editing a lock after approval is refused")
    l3["targets"][2]["version"] = 2
    reapprove(l3["targets"][2])
    lp.write_text(json.dumps(l3))
    want(js.check_locks(lp)["approved"] == {"J0", "J1", "J2"}, "a version bump with a fresh approval is accepted")
    l4 = copy.deepcopy(ld)
    l4["targets"][0]["references"] = [{"sha256": "d" * 64, "role": "style-only", "kind": "sheet"}]
    reapprove(l4["targets"][0])
    lp.write_text(json.dumps(l4))
    want(refused(lambda: js.check_locks(lp), "never a sheet"), "a contact sheet as a reference is refused")
    l4["targets"][0]["references"] = [{"sha256": c * 64, "role": "style-only", "kind": "individual"} for c in "def"]
    reapprove(l4["targets"][0])
    lp.write_text(json.dumps(l4))
    want(refused(lambda: js.check_locks(lp), "at most two"), "more than two references is refused")
    l4["targets"][0]["references"] = [{"sha256": "d" * 64, "role": "inspiration", "kind": "individual"}]
    reapprove(l4["targets"][0])
    lp.write_text(json.dumps(l4))
    want(refused(lambda: js.check_locks(lp), "role"), "an unlabelled reference role is refused")
    si_path = base / "lock_si.json"
    si_path.write_text(json.dumps({"bloodline": {"id": "BLX"}, "jutsu": [
        {"jutsu_id": "J0", "name": "Technique Number 1"}, {"jutsu_id": "J1", "name": "Wrong Name"},
        {"jutsu_id": "J2", "name": "Technique Number 3"}]}))
    lp.write_text(json.dumps(ld))
    want(refused(lambda: js.check_locks(lp, si_path), "roster name"), "a lock whose name disagrees with the intake roster is refused")
    lp.write_text(json.dumps(ld))

    print("\nP1 attempt log (P0 B, J)")
    ap_ = base / "attempts.json"

    def write_attempts(rows):
        ap_.write_text(json.dumps({"schema": "tnr.jutsu-studio.attempts/1", "attempts": rows}))

    write_attempts([attempt("J0", 1, "s1", "rejected", ["wrong_target"]),
                    attempt("J0", 2, "s1", "rejected", ["composition"]),
                    attempt("J0", 3, "s1", "rejected", ["quality"])])
    want(refused(lambda: js.check_attempts(ap_), "RESTART_REQUIRED"),
         "a third attempt in a session after two wrong-target/composition failures is refused")
    write_attempts([attempt("J0", 1, "s1", "rejected", ["wrong_target"]),
                    attempt("J0", 2, "s1", "rejected", ["composition"])])
    want(js.check_attempts(ap_)["per_jutsu"]["J0"]["restart_required_session"] == "s1",
         "two such failures surface RESTART_REQUIRED for that session")
    write_attempts([attempt("J0", 1, "s1", "rejected", ["wrong_target"], sha="1" * 64),
                    attempt("J0", 2, "s2", "approved", sha="2" * 64, references=["1" * 64])])
    want(refused(lambda: js.check_attempts(ap_), "rejected candidate"), "conditioning on a rejected candidate is refused")
    write_attempts([attempt("J0", 1, "s1", "rejected", [])])
    want(refused(lambda: js.check_attempts(ap_), "reason code"), "a rejection without a reason code is refused")
    write_attempts([attempt("J0", 1, "s1", "approved")])
    want(refused(lambda: js.check_attempts(ap_), "candidate_sha256"), "an approval without the candidate sha is refused")
    write_attempts([attempt("J0", 2, "s1", "approved", sha="2" * 64)])
    want(refused(lambda: js.check_attempts(ap_), "numbered"), "attempts must be numbered 1..n")
    write_attempts([attempt("J1", 1, "s1", "approved", sha="3" * 64, anatomy_present=True)])
    lp.write_text(json.dumps(ld))
    want(refused(lambda: js.check_attempts(ap_, js.check_locks(lp)), "anatomy_exception"),
         "an approved candidate with anatomy and no target exception is refused")
    la = copy.deepcopy(ld)
    la["targets"][0]["anatomy_exception"] = {"scope": "abstract five-digit contact print", "director_evidence": "fixture"}
    reapprove(la["targets"][0])
    lp.write_text(json.dumps(la))
    want(refused(lambda: js.check_attempts(ap_, js.check_locks(lp)), "does not carry over"),
         "an anatomy exception for one target does not cover another")
    write_attempts([attempt("J0", 1, "s1", "approved", sha="3" * 64, anatomy_present=True)])
    want(js.check_attempts(ap_, js.check_locks(lp))["per_jutsu"]["J0"]["approved_raw_after_attempt_n"] == 1,
         "the target's own director anatomy exception allows its approval")
    lp.write_text(json.dumps(ld))

    # Aerathiel-shaped accounting, as records only (retrospective table; no Aerathiel bytes are used).
    S = lambda c: c * 64
    rows = [
        attempt("AS", 1, "as1", "rejected", ["art_style_drift"]), attempt("AS", 2, "as1", "rejected", ["art_style_drift"]),
        attempt("AS", 3, "as1", "rejected", ["quality"]), attempt("AS", 4, "as1", "approved", sha=S("a")),
        attempt("WD", 1, "wd1", "approved", sha=S("b")),
        attempt("DM", 1, "dm1", "approved", sha=S("c")),
        attempt("DT", 1, "dt1", "rejected", ["wrong_target", "silhouette_conflict"]),
        attempt("DT", 2, "dt1", "rejected", ["wrong_target"]), attempt("DT", 3, "dt2", "approved", sha=S("d")),
        attempt("PC", 1, "pc1", "rejected", ["wrong_target", "silhouette_conflict"], shown_to_director=True),
        attempt("PC", 2, "pc1", "rejected", ["wrong_target", "silhouette_conflict"], shown_to_director=True),
        attempt("PC", 3, "pc2", "rejected", ["anatomy"]), attempt("PC", 4, "pc2", "rejected", ["invented_symbol"]),
        attempt("PC", 5, "pc2", "rejected", ["composition"]), attempt("PC", 6, "pc2", "approved", sha=S("e"),
                                                                       generator_wait_ms=41000),
    ]
    write_attempts(rows)
    st = js.check_attempts(ap_)
    f = st["family"]
    want(f["attempt_count"] == 15 and f["approved"] == 5 and f["first_attempt_approvals"] == 2
         and f["generations_per_approved_raw"] == 3.0, "the log reproduces 15 generations / 5 approvals / 2 first-pass")
    pc = st["per_jutsu"]["PC"]
    want(pc["approved_raw_after_attempt_n"] == 6 and pc["wrong_target_count"] == 2 and pc["anatomy_rejection_count"] == 1
         and pc["invented_symbol_count"] == 1 and pc["wrong_target_shown_to_director"] == 2 and pc["sessions"] == 2,
         "Particle Cannon: wrong target x2 shown, clean restart, anatomy + invented symbol, approved at attempt 6")
    want(f["generator_wait_ms"] == 41000 and f["generator_wait_measured_n"] == 1,
         "generator wait is summed only over attempts where it was measured")

    print("\nP1 approved raws tie to their lock and last approved attempt")
    root, path, doc = family(base, 3, name="tie")
    lp.write_text(json.dumps(ld))
    write_attempts([attempt(f"J{i}", 1, f"s{i}", "approved", sha=doc["jutsu"][i]["raw_sha256"]) for i in range(3)])
    plan = js.verify_approved(path, spec, locks=lp, attempts=ap_)
    want(plan["attempts"]["family"]["approved"] == 3 and plan["locks"]["approved"] == {"J0", "J1", "J2"},
         "approved raws that match their approved attempts and approved locks verify")
    write_attempts([attempt("J0", 1, "s0", "approved", sha="f" * 64)] +
                   [attempt(f"J{i}", 1, f"s{i}", "approved", sha=doc["jutsu"][i]["raw_sha256"]) for i in (1, 2)])
    want(refused(lambda: js.verify_approved(path, spec, locks=lp, attempts=ap_), "terminal approved attempt"),
         "an approved raw that is not its terminal approved candidate is refused")
    lp.write_text(json.dumps(lock_doc(names, approve=False)))
    want(refused(lambda: js.verify_approved(path, spec, locks=lp), "DIRECTION_APPROVED"),
         "a raw whose target lock is not direction-approved is refused")
    lp.write_text(json.dumps(ld))
    write_attempts([attempt(f"J{i}", 1, f"s{i}", "approved", sha=doc["jutsu"][i]["raw_sha256"]) for i in range(3)])
    rt = js.finalize(path, root / "out", label="v1", locks=lp, attempts=ap_)
    zf = zipfile.ZipFile(root / "out" / "dist" / rt["archives"]["closeout"]["file"])
    want(all(r["gates"]["DIRECTION_APPROVED"] == "APPROVED" for r in rt["ledger"]["rows"])
         and {"manifest/locks.json", "manifest/attempts.json"} <= set(zf.namelist()),
         "finalize records DIRECTION_APPROVED and seals the locks and attempt log into the closeout")

    print("\nP1 compare review aid (P0 C)")
    cand = base / "cand.png"
    js.synth_image(31337, 1024).save(cand, "PNG")
    cand_sha = js.file_sha(cand)
    fam_files = [exports / e["output"] for e in good["exports"]]
    rec = js.compare(cand, fam_files, base / "cmp", label="c1")
    sheet = Image.open(base / "cmp" / "compare_c1.png").convert("RGB")
    ok = True
    for cell in rec["cells"]:
        src = cand if cell["role"] == "candidate" else exports / cell["file"]
        with Image.open(src) as im:
            want_tile = im.convert("RGB").resize((cell["size"], cell["size"]), Image.LANCZOS)
        ok &= sheet.crop((cell["x"], cell["y"], cell["x"] + cell["size"], cell["y"] + cell["size"])).tobytes() == want_tile.tobytes()
    want(ok and len(rec["cells"]) == 3 * 4, "every compare cell is the exact 125/64/32 resize of its source")
    want(js.file_sha(cand) == cand_sha and rec["status"].startswith("REVIEW AID - NOT A GALLERY"),
         "the candidate bytes are unchanged and the sheet is labelled a review aid, not a gallery")
    want(js.compare(cand, fam_files, base / "cmp", label="c1")["sheet"]["sha256"] == rec["sheet"]["sha256"],
         "compare is deterministic (identical rerun)")
    want(refused(lambda: js.compare(cand, [cand] + fam_files, base / "cmp", label="c2"), "same bytes twice"),
         "a candidate listed in its own family is refused")


# ---------------------------------------------------------------------------------------------
# review corrections F2-F6 (docs/reviews/JUTSU_ICON_P1_FROZEN_SHA_REVIEW_20261019.md)
# ---------------------------------------------------------------------------------------------


def run_correction_tests(tmp: Path, spec: dict, nums: dict) -> None:
    base = tmp / "corr"
    base.mkdir()
    names = ["Technique Number 1", "Technique Number 2", "Technique Number 3"]

    print("\nF2 sealed lock/attempt/approval evidence is the verified bytes")
    root, path, doc = family(base, 3, name="evid")
    lp, ap_ = root / "locks.json", root / "attempts.json"
    lp.write_text(json.dumps(lock_doc(names)))
    good_attempts = {"schema": "tnr.jutsu-studio.attempts/1",
                     "attempts": [attempt(f"J{i}", 1, f"s{i}", "approved", sha=doc["jutsu"][i]["raw_sha256"]) for i in range(3)]}
    ap_.write_text(json.dumps(good_attempts))

    def swap_after_showcase(target: Path, content: bytes):
        def hook(stage):
            if stage == "showcase":
                target.write_bytes(content)
        return hook

    for label, target, content in (
            ("lock", lp, json.dumps(lock_doc(names, approve=False)).encode()),
            ("attempt", ap_, b'{"schema": "tnr.jutsu-studio.attempts/1", "attempts": []}'),
            ("approved", path, json.dumps({**doc, "family_acceptance": {"status": "REJECTED"}}).encode())):
        keep_l, keep_a, keep_p = lp.read_bytes(), ap_.read_bytes(), path.read_bytes()
        out = root / f"out_{label}"
        msg = expect_raise(lambda: js.finalize(path, out, label="v1", locks=lp, attempts=ap_,
                                               on_stage=swap_after_showcase(target, content)))
        want("not the recorded bytes" in msg and not (out / "dist").exists(),
             f"a {label} record swapped after verification is refused before any archive is written")
        lp.write_bytes(keep_l)
        ap_.write_bytes(keep_a)
        path.write_bytes(keep_p)
    ok = js.finalize(path, root / "out_ok", label="v1", locks=lp, attempts=ap_)
    zf = zipfile.ZipFile(root / "out_ok" / "dist" / ok["archives"]["closeout"]["file"])
    want(zf.read("manifest/locks.json") == lp.read_bytes() and zf.read("manifest/attempts.json") == ap_.read_bytes()
         and ok["ledger"]["locks_sha256"] == js.sha256(lp.read_bytes())
         and ok["ledger"]["attempts_sha256"] == js.sha256(ap_.read_bytes()),
         "the closeout seals exactly the verified lock/attempt bytes and the ledger records their sha256")

    print("\nF3 terminal approval and one jutsu per session")
    rows = [attempt("J0", 1, "s0", "approved", sha=doc["jutsu"][0]["raw_sha256"]),
            attempt("J0", 2, "s0", "rejected", ["quality"])] + \
           [attempt(f"J{i}", 1, f"s{i}", "approved", sha=doc["jutsu"][i]["raw_sha256"]) for i in (1, 2)]
    ap_.write_text(json.dumps({"schema": "tnr.jutsu-studio.attempts/1", "attempts": rows}))
    want(refused(lambda: js.verify_approved(path, spec, locks=lp, attempts=ap_), "terminal attempt (2) is rejected"),
         "an approval followed by a later rejection does not let the earlier raw finalize")
    rows.insert(2, attempt("J0", 3, "s0b", "approved", sha=doc["jutsu"][0]["raw_sha256"]))
    ap_.write_text(json.dumps({"schema": "tnr.jutsu-studio.attempts/1", "attempts": rows}))
    want(len(js.verify_approved(path, spec, locks=lp, attempts=ap_)["rows"]) == 3,
         "a fresh terminal approved attempt re-affirms the raw explicitly")
    shared = [attempt("J0", 1, "shared", "approved", sha=doc["jutsu"][0]["raw_sha256"]),
              attempt("J1", 1, "shared", "approved", sha=doc["jutsu"][1]["raw_sha256"]),
              attempt("J2", 1, "s2", "approved", sha=doc["jutsu"][2]["raw_sha256"])]
    ap_.write_text(json.dumps({"schema": "tnr.jutsu-studio.attempts/1", "attempts": shared}))
    want(refused(lambda: js.check_attempts(ap_), "exactly one jutsu"), "one session id used for two jutsu is refused")
    ap_.write_text(json.dumps(good_attempts))

    print("\nF4 doctor is green only when every check passes")
    bad = js.doctor(git_ref="does-not-exist-ref")
    want(bad["verdict"].startswith("NOT_READY") and "git_ref_blobs" in bad["verdict"],
         "a supplied --git-ref that cannot be compared blocks green")
    want(js.main(["doctor", "--git-ref", "does-not-exist-ref"]) == 3, "doctor exits non-zero with a failed requested check")
    real = js.encode_webp
    flip = {"n": 0}

    def unstable(img):
        flip["n"] += 1
        buf = io.BytesIO()
        img.save(buf, "WEBP", lossless=True, method=6 if flip["n"] % 2 else 0, exact=True)
        return buf.getvalue()

    js.encode_webp = unstable
    try:
        nd = js.doctor()
    finally:
        js.encode_webp = real
    want(nd["verdict"].startswith("NOT_READY") and "encoder_determinism" in nd["verdict"],
         "a non-deterministic encoder blocks green even when the preflight probe runs")
    want(js.doctor()["verdict"] == "RUN_CAPABLE_CANONICAL", "with every check passing doctor is green")

    print("\nF5 audit refuses a non-conforming layout as final")
    r10, p10, d10 = family(base, 10, name="ten", size=256)
    res10 = js.finalize(p10, r10 / "out", label="v1", stop_after="preflight")
    ex10 = r10 / "out" / "exports"
    items, icons = [], []
    for e in res10["exports"]:
        data = (ex10 / e["output"]).read_bytes()
        items.append({"name": e["name"], "output_bytes": len(data), "tile": js.tile_from_export(data)})
    old_rows = [4, 4, 2]
    canvas, placed, _ = js.render_canvas(items, old_rows)
    for e, pl in zip(res10["exports"], placed):
        icons.append({"jutsu_id": e["jutsu_id"], "jutsu_name": e["name"], "approved_raw_sha256": e["raw_sha256"],
                      "output_filename": e["output"], "output_sha256": e["output_sha256"],
                      "output_bytes": e["output_bytes"], **pl})
    old_man = {"schema": "tnr.jutsu-showcase/1", "n": 10, "row_lengths": old_rows, "icons": icons,
               "geometry": {"canvas": list(canvas.size)}, "members_sha256": js.members_commitment(icons)}
    au = js.audit_gallery(png_of(canvas), old_man, ex10)
    want(au["verdict"] == "INVALID" and au["layout"] == "NONCONFORMING" and au["pixel_fidelity"] == "FAITHFUL",
         "a faithful 4+4+2 ten-icon sheet is INVALID as a final gallery but reported pixel-FAITHFUL")
    full10 = js.finalize(p10, r10 / "out", label="v1full")
    want(full10["showcase"]["row_lengths"] == [4, 3, 3], "the tool itself builds 10 = 4+3+3")
    bad_man = copy.deepcopy(old_man)
    bad_man["members_sha256"] = "0" * 64
    want(any("members_sha256" in x for x in js.audit_gallery(png_of(canvas), bad_man, ex10)["problems"]),
         "a manifest whose members commitment disagrees with its icons is a problem")

    print("\nF6 source-index bloodline identity")
    si = base / "si_bl.json"
    si.write_text(json.dumps({"bloodline": {"id": "BLX", "name": "Fixture Line"},
                              "jutsu": [{"jutsu_id": f"J{i}", "name": names[i]} for i in range(3)]}))
    want(len(js.verify_approved(path, spec, source_index=si)["rows"]) == 3, "matching bloodline identity verifies")
    for label, change, needle in (("a different bloodline id", {"id": "OTHER"}, "!= intake 'BLX'"),
                                  ("a missing bloodline id", {"id": ""}, "bloodline.id is required"),
                                  ("a different bloodline name", {"name": "Some Other Line"}, "bloodline.name")):
        dd = copy.deepcopy(doc)
        dd["bloodline"].update(change)
        rewrite(path, dd)
        want(refused(lambda: js.verify_approved(path, spec, source_index=si), needle),
             f"{label} against the intake roster is refused (no --locks needed)")
    rewrite(path, doc)


if __name__ == "__main__":
    sys.exit(main())
