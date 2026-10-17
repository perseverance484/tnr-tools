#!/usr/bin/env python3
"""
artpreflight_selftest.py - the exit test for the art preflight.

For every asset type it builds one correct export and one deliberately wrong one, then
asserts the tool passes the first and names the specific fault in the second. The point
of the test is that a wrong export is caught by the tool rather than by eye, so a fault
that the tool merely warns about counts as a failure here.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import artpreflight as ap  # noqa: E402


def figure(w: int, h: int, alpha: bool = True, soft: bool = False, key_spill: bool = False):
    """A hard-edged blob on transparency, roughly the shape of a keyed character."""
    mode = "RGBA" if alpha else "RGB"
    img = Image.new(mode, (w, h), (0, 0, 0, 0) if alpha else (12, 14, 20))
    d = ImageDraw.Draw(img)
    fill = (40, 44, 58, 255) if alpha else (40, 44, 58)
    d.ellipse([w * 0.2, h * 0.05, w * 0.8, h * 0.95], fill=fill)
    if soft and alpha:
        # a feathered ring: partial alpha over a wide band
        px = img.load()
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a == 0 and (x + y) % 2 == 0 and w * 0.1 < x < w * 0.9:
                    px[x, y] = (40, 44, 58, 128)
    if key_spill:
        d.rectangle([0, 0, max(2, w // 20), max(2, h // 20)], fill=(0, 255, 0, 255))
    return img


def designed_icon(w: int, h: int):
    """An opaque full-bleed jutsu icon, with a near-lime patch a key check would misread."""
    img = Image.new("RGB", (w, h), (18, 40, 92))
    d = ImageDraw.Draw(img)
    d.polygon([(w * 0.5, h * 0.1), (w * 0.9, h * 0.5), (w * 0.5, h * 0.9), (w * 0.1, h * 0.5)],
              fill=(196, 232, 250))
    d.rectangle([0, 0, w // 8, h // 8], fill=(10, 245, 20))
    return img


def save(img, path, lossless=True):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".webp":
        img.save(path, "WEBP", lossless=lossless, quality=100 if lossless else 60)
    else:
        img.save(path)
    return path


CASES = []


def case(name, target, filename, builder, expect_checks):
    CASES.append((name, target, filename, builder, expect_checks))


# ---------------------------------------------------------------- good exports
case("scene character 2:3", "SCENE_CHARACTER", "boss_scene_char.webp",
     lambda p: save(figure(682, 1023), p), [])
case("scene character 1:1 bust", "SCENE_CHARACTER", "handler_scene_char.webp",
     lambda p: save(figure(682, 682), p), [])
case("background 3:2", "SCENE_BACKGROUND", "alley_background.webp",
     lambda p: save(figure(1024, 683, alpha=False), p, lossless=False), [])
case("avatar 1:1", "AI_AVATAR", "prowler_avatar.webp",
     lambda p: save(figure(640, 640), p), [])
case("icon 1:1", "ICON", "stormglass_icon.webp",
     lambda p: save(figure(256, 256), p), [])
case("pin 1:1", "STATIC", "shrine_pin.webp",
     lambda p: save(figure(256, 256), p), [])
# RUL-2026-10-14-001: jutsu icons may carry a designed opaque background.
case("jutsu icon, opaque designed background", "JUTSU_ICON", "ice_shackles_jutsu_icon.webp",
     lambda p: save(designed_icon(256, 256), p), [])
case("jutsu icon, keyed transparent", "JUTSU_ICON", "glacial_volley_jutsu.webp",
     lambda p: save(figure(256, 256), p), [])

# ---------------------------------------------------------------- wrong exports
case("scene character re-exported to 4:3", "SCENE_CHARACTER", "bad_wide_scene_char.webp",
     lambda p: save(figure(682, 512), p), ["aspect"])
case("scene character taller than the clip bound", "SCENE_CHARACTER", "bad_tall_scene_char.webp",
     lambda p: save(figure(400, 900), p), ["aspect", "clip_bound"])
case("scene character under the delivered width", "SCENE_CHARACTER", "bad_small_scene_char.webp",
     lambda p: save(figure(200, 300), p), ["min_width"])
case("scene character saved lossy", "SCENE_CHARACTER", "bad_lossy_scene_char.webp",
     lambda p: save(figure(682, 1023), p, lossless=False), ["format_mode"]),
case("scene character with no alpha", "SCENE_CHARACTER", "bad_flat_scene_char.webp",
     lambda p: save(figure(682, 1023, alpha=False), p), ["alpha"])
case("scene character with residual key spill", "SCENE_CHARACTER", "bad_spill_scene_char.webp",
     lambda p: save(figure(682, 1023, key_spill=True), p), ["spill"])
case("scene character with chewed soft edges", "SCENE_CHARACTER", "bad_soft_scene_char.webp",
     lambda p: save(figure(682, 1023, soft=True), p), ["soft_edges"])
case("background at 16:9", "SCENE_BACKGROUND", "bad_wide_background.webp",
     lambda p: save(figure(1024, 576, alpha=False), p, lossless=False), ["aspect"])
case("background left as png", "SCENE_BACKGROUND", "bad_png_background.png",
     lambda p: save(figure(1024, 683, alpha=False), p), ["format"])
case("avatar left at 2:3", "AI_AVATAR", "bad_portrait_avatar.webp",
     lambda p: save(figure(640, 960), p), ["aspect"])
case("icon at 4:3", "ICON", "bad_wide_icon.webp",
     lambda p: save(figure(256, 192), p), ["aspect"])
case("pin under minimum", "STATIC", "bad_tiny_pin.webp",
     lambda p: save(figure(64, 64), p), ["min_width"])
case("item icon left opaque", "ICON", "bad_flat_item_icon.webp",
     lambda p: save(figure(256, 256, alpha=False), p), ["alpha"])
case("jutsu icon, keyed with residual spill", "JUTSU_ICON", "bad_spill_jutsu_icon.webp",
     lambda p: save(figure(256, 256, key_spill=True), p), ["spill"])
case("jutsu icon, keyed with chewed soft edges", "JUTSU_ICON", "bad_soft_jutsu_icon.webp",
     lambda p: save(figure(256, 256, soft=True), p), ["soft_edges"])
case("jutsu icon, opaque at 4:3", "JUTSU_ICON", "bad_wide_jutsu_icon.webp",
     lambda p: save(designed_icon(256, 192), p), ["aspect"])
case("jutsu icon, opaque saved lossy", "JUTSU_ICON", "bad_lossy_jutsu_icon.webp",
     lambda p: save(designed_icon(256, 256), p, lossless=False), ["format_mode"])
case("jutsu icon, opaque under minimum", "JUTSU_ICON", "bad_tiny_jutsu_icon.webp",
     lambda p: save(designed_icon(128, 128), p), ["min_width"])
case("unclassifiable filename", "SCENE_CHARACTER", "untitled_final_v2.webp",
     lambda p: save(figure(682, 1023), p), [])


# Item/jutsu class boundary, run the way an operator runs it: type INFERRED from the name,
# then the full check. `type` in the expected set means inference refused and the file is
# an error until someone passes --type. An item name must never come out alpha-optional.
OPAQUE = lambda p: save(designed_icon(256, 256), p)  # noqa: E731
BOUNDARY = [
    # item evidence beside a jutsu token -> refuse
    ("item_jutsu_scroll_icon.webp", OPAQUE, None, {"type"}),
    ("item_jutsu_scroll.webp", OPAQUE, None, {"type"}),
    ("img_jutsu_scroll.webp", OPAQUE, None, {"type"}),
    ("scroll_item_jutsu_icon.webp", OPAQUE, None, {"type"}),
    # jutsu inside a word is not a jutsu token -> stays ICON and keeps the alpha rule
    ("icon_ninjutsu_manual.webp", OPAQUE, "ICON", {"alpha", "spill"}),
    ("genjutsu_mirror_item_icon.webp", OPAQUE, "ICON", {"alpha", "spill"}),
    ("ninjutsu.webp", OPAQUE, None, {"type"}),
    # re-review F1-R1: the house item convention is `icon_<name>`, with no `item` token
    ("icon_jutsu_scroll.webp", OPAQUE, None, {"type"}),
    ("icon-jutsu-scroll.webp", OPAQUE, None, {"type"}),
    ("icon_forbidden_jutsu_tome.webp", OPAQUE, None, {"type"}),
    ("quest_icon_jutsu_seal.webp", OPAQUE, None, {"type"}),
    # re-review F1-R2: plural, numbered, mid-name and space-separated item markers
    ("items_jutsu_icon.webp", OPAQUE, None, {"type"}),
    ("scroll_items_jutsu_icon.webp", OPAQUE, None, {"type"}),
    ("item01_jutsu_scroll.webp", OPAQUE, None, {"type"}),
    ("item2_jutsu_icon.webp", OPAQUE, None, {"type"}),
    ("x_img_jutsu_icon.webp", OPAQUE, None, {"type"}),
    ("jutsu_item2.webp", OPAQUE, None, {"type"}),
    ("img-jutsu_scroll.webp", OPAQUE, None, {"type"}),
    ("jutsu_scroll item.webp", OPAQUE, None, {"type"}),
    ("bloodline_jutsu_icon.webp", OPAQUE, None, {"type"}),
    ("jutsu_jutsu_icon.webp", OPAQUE, None, {"type"}),
    # unrelated targets still refuse
    ("jutsu_avatar.webp", OPAQUE, None, {"type"}),
    ("blue_jutsu_marker.webp", OPAQUE, None, {"type"}),
    # genuine jutsu names -> JUTSU_ICON; opaque passes, keyed keeps every key check
    ("ice_shackles_jutsu_icon.webp", OPAQUE, "JUTSU_ICON", set()),
    ("glacial_volley_jutsu.webp", OPAQUE, "JUTSU_ICON", set()),
    ("jutsu_blade_resonance.webp", OPAQUE, "JUTSU_ICON", set()),
    ("arctic-frost-jutsu.webp", OPAQUE, "JUTSU_ICON", set()),
    ("Ice.Shackles.Jutsu.webp", OPAQUE, "JUTSU_ICON", set()),
    ("fire_jutsu_v2.webp", OPAQUE, "JUTSU_ICON", set()),
    ("ice shackles jutsu.webp", OPAQUE, "JUTSU_ICON", set()),
    ("ice_shackles_jutsu_icon.png.webp", OPAQUE, "JUTSU_ICON", set()),
    ("keyed_spill_jutsu_icon.webp", lambda p: save(figure(256, 256, key_spill=True), p),
     "JUTSU_ICON", {"spill"}),
    ("keyed_soft_jutsu_icon.webp", lambda p: save(figure(256, 256, soft=True), p),
     "JUTSU_ICON", {"soft_edges"}),
]

# CLI runs: (filename, builder, extra args, expected error checks). Exit code = error count.
CLI = [
    ("item_jutsu_scroll_icon.webp", OPAQUE, [], {"type"}),
    ("item_jutsu_scroll_icon.webp", OPAQUE, ["--type", "ICON"], {"alpha", "spill"}),
    ("icon_ninjutsu_manual.webp", OPAQUE, [], {"alpha", "spill"}),
    ("icon_jutsu_scroll.webp", OPAQUE, [], {"type"}),
    ("icon_jutsu_scroll.webp", OPAQUE, ["--type", "ICON"], {"alpha", "spill"}),
    ("items_jutsu_icon.webp", OPAQUE, ["--max-bytes", "80000"], {"type"}),
    ("item01_jutsu_scroll.webp", OPAQUE, [], {"type"}),
    ("ice_shackles_jutsu_icon.webp", OPAQUE, ["--max-bytes", "80000"], set()),
    ("ice_shackles_jutsu_icon.webp", OPAQUE, ["--type", "ICON"], {"alpha", "spill"}),
]


def inferred_errors(path: str, spec: dict) -> tuple[str | None, set[str]]:
    target = ap.infer_type(path)
    if target is None:
        return None, {"type"}
    report = ap.Report()
    ap.check_file(path, target, spec, report, None)
    return target, {r["check"] for r in report.rows if r["level"] == "error"}


def run() -> int:
    spec = ap.load_spec("25x_DATA_art_spec.json")
    tmp = tempfile.mkdtemp()
    passed = failed = 0
    try:
        for name, target, filename, builder, expect in CASES:
            path = os.path.join(tmp, filename)
            builder(path)
            report = ap.Report()
            ap.check_file(path, target, spec, report, None)
            got = {r["check"] for r in report.rows if r["level"] == "error"}
            want = set(expect)
            if got == want:
                passed += 1
                verdict = "ok"
            else:
                failed += 1
                verdict = f"FAIL  expected {sorted(want) or 'clean'}, got {sorted(got) or 'clean'}"
            print(f"  {'pass' if verdict == 'ok' else 'FAIL'}  {name:48} {'' if verdict == 'ok' else verdict}")

        # filename inference is a separate axis: every good filename must classify itself
        print("\n  filename inference:")
        for name, target, filename, _b, _e in CASES:
            inferred = ap.infer_type(filename)
            if filename.startswith("untitled") or filename == "bad_portrait_avatar.webp":
                ok = inferred is None
                label = "correctly refuses to guess (ambiguous)"
            else:
                ok = inferred == target
                label = f"{inferred}"
            print(f"  {'pass' if ok else 'FAIL'}  {filename:34} -> {label}")
            passed += ok
            failed += not ok

        # a workstream cap is "under N": a file of exactly N bytes fails, N - 1 headroom passes
        print("\n  workstream byte cap:")
        path = save(designed_icon(256, 256), os.path.join(tmp, "cap_jutsu_icon.webp"))
        size = os.path.getsize(path)
        for cap, want in ((size, {"bytes"}), (size + 1, set())):
            report = ap.Report()
            ap.check_file(path, "JUTSU_ICON", spec, report, None, max_bytes=cap)
            got = {r["check"] for r in report.rows if r["level"] == "error"}
            ok = got == want
            print(f"  {'pass' if ok else 'FAIL'}  {size} bytes against --max-bytes {cap:<10} "
                  f"-> {sorted(got) or 'clean'}")
            passed += ok
            failed += not ok

        print("\n  item/jutsu class boundary (inferred type, full check):")
        for filename, builder, want_target, want in BOUNDARY:
            path = os.path.join(tmp, filename)
            builder(path)
            target, got = inferred_errors(path, spec)
            ok = target == want_target and got == want
            print(f"  {'pass' if ok else 'FAIL'}  {filename:34} -> {target or 'refused'}, "
                  f"{sorted(got) or 'clean'}"
                  + ("" if ok else f"  (expected {want_target or 'refused'}, {sorted(want) or 'clean'})"))
            passed += ok
            failed += not ok

        print("\n  item/jutsu class boundary (CLI):")
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artpreflight.py")
        spec_path = os.path.abspath("25x_DATA_art_spec.json")
        for filename, builder, extra, want in CLI:
            path = os.path.join(tmp, "cli_" + filename)
            builder(path)
            proc = subprocess.run(
                [sys.executable, script, path, "--spec", spec_path, "--json", *extra],
                capture_output=True, text=True,
            )
            rows = json.loads(proc.stdout)["rows"]
            got = {r["check"] for r in rows if r["level"] == "error"}
            ok = got == want and proc.returncode == len([r for r in rows if r["level"] == "error"])
            label = " ".join(extra) or "inferred"
            print(f"  {'pass' if ok else 'FAIL'}  {filename:34} [{label}] exit {proc.returncode} "
                  f"-> {sorted(got) or 'clean'}")
            passed += ok
            failed += not ok
    finally:
        shutil.rmtree(tmp)

    print(f"\n{passed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    sys.exit(run())
