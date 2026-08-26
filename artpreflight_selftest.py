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
case("unclassifiable filename", "SCENE_CHARACTER", "untitled_final_v2.webp",
     lambda p: save(figure(682, 1023), p), [])


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
    finally:
        shutil.rmtree(tmp)

    print(f"\n{passed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    sys.exit(run())
