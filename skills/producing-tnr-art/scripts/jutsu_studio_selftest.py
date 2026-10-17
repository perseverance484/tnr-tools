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
    want(js.grid_rows(10) == [4, 4, 2] and js.grid_rows(13) == [4, 4, 4, 1], "N>=10 uses at most four per row")
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
        ("family accepted without evidence", lambda d: d.__setitem__("family_acceptance", {"status": "ACCEPTED", "evidence": ""}), "evidence"),
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
    want(sc["row_lengths"] == [3] and sc["tile_pixel_equality"], "the N=3 showcase is one row with pixel-equal tiles")
    want(all(i["caption"].endswith(js.caption_kb((root / "out" / "exports" / i["output_filename"]).stat().st_size)) for i in sc["icons"]),
         "every caption carries the real export bytes/1000")
    want(sc["director_family_acceptance"]["status"] == "PENDING", "family acceptance stays PENDING unless the director recorded it")
    closeout = root / "out" / "dist" / res["archives"]["closeout"]["file"]
    zf = zipfile.ZipFile(closeout)
    sums = dict(reversed(line.split("  ", 1)) for line in zf.read("SHA256SUMS").decode().splitlines())
    want(zf.testzip() is None and all(js.sha256(zf.read(n)) == h for n, h in sums.items()) and len(sums) == len(zf.namelist()) - 1,
         "the closeout ZIP passes CRC and every member matches SHA256SUMS")
    want(sorted(zipfile.ZipFile(root / "out" / "dist" / res["archives"]["upload"]["file"]).namelist()) == sorted(e["output"] for e in res["exports"]),
         "the upload ZIP is exactly the N current WebPs, flat")
    ledger = json.loads((root / "out" / "studio_ledger.json").read_text())
    want(all(r["gates"]["USER_UPLOAD_READBACK"] == "NOT_PERFORMED" and r["gates"]["GIT_BYTES_PINNED"] == "NOT_PERFORMED" for r in ledger["rows"]),
         "the ledger never claims upload, read-back or Git pinning")

    res_again = js.finalize(path, root / "out", label="v1")
    want(res_again["cache"] == {"encoded": 0, "reused": 3} and res_again["archives"]["closeout"]["state"] == "UNCHANGED",
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
    want(res2["cache"] == {"encoded": 1, "reused": 2}, "changing one approved raw re-encodes only that icon")
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


if __name__ == "__main__":
    sys.exit(main())
