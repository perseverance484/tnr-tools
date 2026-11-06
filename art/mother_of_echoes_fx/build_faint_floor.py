#!/usr/bin/env python3
"""Faint lingering floors (director, 2026-11-06: approved at 18%). The engine shows a ground effect's static tile the
moment it loads (combatEffects.ts:139-200), so a vivid floor sat under every payoff from frame 0. Now:
- the lingering floor tile is the same floor at 18% (ordered dither, hard alpha): a faint stain before the break;
- the payoff carries the VIVID floor itself: from its break frame each hex's clip draws the vivid floor in its own hex
  footprint under the payoff (dithering in over 2 frames), and when the payoff ends the clip holds it, then fades it
  down to the faint tile over 7 frames.

    python3 art/mother_of_echoes_fx/build_faint_floor.py tiles            # writes the faint floor tiles into exports/
    python3 art/mother_of_echoes_fx/build_faint_floor.py settle SRC_DIR META REGION FLOOR_FILE BREAK OUT_DIR

`settle` rewrites every slice of REGION in META (frames are 50 px, delivered x3; a slice's leading empty frames are its
wave lead and stay empty) into OUT_DIR as <file>_ff.webp and writes <OUT_DIR>/<META stem>_ff_<region>.json. Pillow only.
"""
import importlib.util
import json
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("build_fx", os.path.join(HERE, "build_fx.py"))
F = importlib.util.module_from_spec(_s)
_s.loader.exec_module(F)
EXPORTS = os.path.join(HERE, "exports")
FAINT = 0.18
FADE = 7
TILES = {"tile_moe_floor_i_a8.webp": "tile_moe_floor_i_faint_a14.webp",
         "tile_moe_recast_floor_a8.webp": "tile_moe_recast_floor_faint_a14.webp",
         "tile_moe_floor_iii_a8.webp": "tile_moe_floor_iii_faint_a14.webp"}


def dither(img, keep):
    img = img.copy()
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if px[x, y][3] and F.BAYER[y % 4][x % 4] >= keep * 16:
                px[x, y] = (0, 0, 0, 0)
    return img


def tile50(path):
    t = Image.open(path).convert("RGBA")
    return t.resize((50, 50), Image.NEAREST)


def tiles():
    for src, dst in TILES.items():
        F.tile_out(dither(tile50(os.path.join(EXPORTS, src)), FAINT)).save(os.path.join(EXPORTS, dst), lossless=True,
                                                                          quality=100, method=6)
        print(dst)


BODY = (19, 15, 31, 30)              # the fighter's legs and torso in a 50 px clip over its own hex (LPC envelope)


def settle(src, meta, region, floor, brk, out):
    """QA S1: the fade ends in three gentle steps below the faint level, so the hand-off to the faint tile does not pop.
    QA S2: the in-clip vivid floor is at most 50% (ordered dither) over the fighter's body window.
    QA S3: every slice of the region starts its fade on the same frame (strips padded to the region's longest)."""
    os.makedirs(out, exist_ok=True)
    m = Image.new("L", (40, 20), 0)
    ImageDraw.Draw(m).polygon([(0, 10), (10, 0), (30, 0), (40, 10), (30, 20), (10, 20)], fill=255)
    hexfloor = Image.new("RGBA", (50, 50), (0, 0, 0, 0))     # the floor in the clip's own hex footprint (40 x 20 at 5, 15)
    hexfloor.paste(tile50(floor).resize((40, 20), Image.NEAREST), (5, 15), m)
    body = dither(hexfloor.crop(BODY), 0.5)
    hexfloor.paste((0, 0, 0, 0), BODY)
    hexfloor.alpha_composite(body, BODY[:2])
    rows = [r for r in json.load(open(os.path.join(src, meta)))["slices"] if r["region"] == region]
    strips = {}
    for r in rows:
        if r["file"] in strips:
            continue
        st = Image.open(os.path.join(src, r["file"])).convert("RGBA")
        st = st.resize((st.width // 3, st.height // 3), Image.NEAREST)
        fr = [st.crop((0, i * 50, 50, i * 50 + 50)) for i in range(st.height // st.width)]
        lead = next((i for i, f in enumerate(fr) if f.getbbox()), 0)
        outf = []
        for i, f in enumerate(fr):
            t = i - lead
            if t >= brk:
                g = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
                g.alpha_composite(dither(hexfloor, min(1.0, 0.5 + 0.25 * (t - brk))))
                g.alpha_composite(f)
                f = g
            outf.append(f)
        strips[r["file"]] = outf
    longest = max(len(v) for v in strips.values())
    keeps = [1.0 - (k + 1) / FADE * (1 - FAINT) for k in range(FADE)] + [0.12, 0.06, 0.0]
    done, new = {}, []
    for fname, outf in strips.items():
        outf = outf + [hexfloor.copy() for _ in range(longest - len(outf))]
        for keep in keeps:
            outf.append(dither(hexfloor, keep) if keep > 0 else Image.new("RGBA", (50, 50), (0, 0, 0, 0)))
        fn = fname.replace(".webp", "_ff.webp")
        F.strip(outf).save(os.path.join(out, fn), lossless=True, quality=100, method=6)
        done[fname] = (fn, len(outf))
    for r in rows:
        fn, n = done[r["file"]]
        new.append({**r, "file": fn, "frames": n})
    stem = os.path.splitext(os.path.basename(meta))[0]
    json.dump({"slices": new}, open(os.path.join(out, f"{stem}_ff_{region}.json"), "w"), indent=1)
    print(region, len(new), "slices,", len(done), "strips")


if __name__ == "__main__":
    if sys.argv[1] == "tiles":
        tiles()
    else:
        settle(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7])
