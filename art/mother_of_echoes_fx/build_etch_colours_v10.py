#!/usr/bin/env python3
"""Job 605: give each Mother of Echoes etching its own colour (QA: all five read as the same gold).

Luminance-preserving recolour of the live etching slices (exports/anim_moe_etch2_<x>_p<c>_<r>_a14.webp, srcIds
sg498_etch_<x>__<c>_<r>) and the Recast: Heart / Recast: Seam slices (exports/anim_moe_recast2_<x>_p<c>_<r>_a14_ff.webp):
each opaque pixel's luma is mapped onto a ramp dark-tone -> element colour -> white, at the original alpha, so the
drawn shapes and the white-hot cutting front are kept and only the hue changes.

The sources are exact 3x nearest upscales of a 50 px art grid (the game serves the 50 px sheet), so the work is done
on that grid and upscaled 3x nearest again. Seam: brightened (luma lifted before the ramp) and its strokes thickened by
one art pixel (2x2 max on alpha, 3 px at 150 px scale), the smallest growth that survives the game's 50 px sheet.
Every other slice keeps its alpha exactly.

Run: python3 art/mother_of_echoes_fx/build_etch_colours_v10.py  ->  exports_v10/anim_moe_{etch3,recast3}_*.webp
     add --preview <dir> to write one board per set (frame 14 of each slice at col*50,row*50 on a dark 600x500 board).
"""
import glob
import os
import re
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "exports")
DST = os.path.join(HERE, "exports_v10")
TILE = 150
NATIVE = 3  # source upscale factor

COLOURS = {  # element colour; Seam is the bright white-gold
    "rime": (165, 215, 255),
    "hail": (245, 248, 255),
    "ember": (255, 125, 40),
    "heart": (60, 220, 200),
    "seam": (255, 228, 150),
}
DARK = 0.28      # dark tone = colour * DARK
KNEE = 0.55      # luma at which the ramp reaches the element colour
WHITE_GAMMA = 1.8  # above the knee, stay coloured longer, then go white-hot
SEAM_LIFT = 0.6  # seam luma ** SEAM_LIFT (brighter)

SETS = [("etch", x, f"anim_moe_etch2_{x}_p*_a14.webp", "anim_moe_etch3_{x}_p{c}_{r}_a14.webp") for x in COLOURS]
SETS += [("recast", x, f"anim_moe_recast2_{x}_p*_a14_ff.webp", "anim_moe_recast3_{x}_p{c}_{r}_a14_ff.webp") for x in ("heart", "seam")]


def ramp(luma, colour):
    col = np.array(colour, float) / 255.0
    dark = col * DARK
    white = np.ones(3)
    L = luma[..., None]
    lo = dark + (col - dark) * np.clip(L / KNEE, 0, 1)
    t = np.clip((L - KNEE) / (1 - KNEE), 0, 1) ** WHITE_GAMMA
    hi = col + (white - col) * t
    return np.where(L <= KNEE, lo, hi)


def recolour(path, element, kind):
    im = Image.open(path)
    assert getattr(im, "n_frames", 1) == 1
    a = np.array(im.convert("RGBA"))
    small = a[::NATIVE, ::NATIVE].astype(float)
    if not (np.repeat(np.repeat(small, NATIVE, 0), NATIVE, 1) == a).all():
        raise SystemExit(f"{path}: not an exact {NATIVE}x nearest upscale")
    rgb, alpha = small[..., :3] / 255.0, small[..., 3]
    luma = rgb @ np.array([0.299, 0.587, 0.114])
    if element == "seam" and kind == "etch":
        luma = luma ** SEAM_LIFT
        # thicken: 2x2 max on alpha (one art pixel); new pixels take the brightest neighbour's luma
        pad_a = np.pad(alpha, ((1, 0), (1, 0)))
        pad_l = np.pad(np.where(alpha > 0, luma, -1), ((1, 0), (1, 0)), constant_values=-1)
        h, w = alpha.shape
        stack_a = np.stack([pad_a[dy:dy + h, dx:dx + w] for dy in (0, 1) for dx in (0, 1)])
        stack_l = np.stack([pad_l[dy:dy + h, dx:dx + w] for dy in (0, 1) for dx in (0, 1)])
        new_alpha = stack_a.max(0)
        luma = np.where(alpha > 0, luma, np.clip(stack_l.max(0), 0, 1) * 0.85)
        # a frame-boundary guard: thickening must not bleed across frame rows (each frame is 50x50 on the art grid)
        fh = TILE // NATIVE
        rows = np.arange(h) % fh == 0
        new_alpha[rows] = np.where(alpha[rows] > 0, new_alpha[rows], 0)
        alpha = new_alpha
    out_rgb = ramp(luma, COLOURS[element])
    out = np.zeros(small.shape, np.uint8)
    out[..., :3] = np.round(out_rgb * 255).clip(0, 255).astype(np.uint8)
    out[..., 3] = alpha.astype(np.uint8)
    out[alpha == 0, :3] = 0
    big = np.repeat(np.repeat(out, NATIVE, 0), NATIVE, 1)
    return Image.fromarray(big, "RGBA")


def tile_of(name):
    m = re.search(r"_p(\d+)_(\d+)_a14", name)
    return int(m.group(1)), int(m.group(2))


def main():
    os.makedirs(DST, exist_ok=True)
    preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    for kind, x, pat, outpat in SETS:
        files = sorted(glob.glob(os.path.join(SRC, pat)))
        board_new = Image.new("RGBA", (600, 500), (14, 16, 22, 255))
        board_old = Image.new("RGBA", (600, 500), (14, 16, 22, 255))
        for f in files:
            c, r = tile_of(os.path.basename(f))
            img = recolour(f, x, kind)
            src = Image.open(f)
            assert img.size == src.size, (f, img.size, src.size)
            img.save(os.path.join(DST, outpat.format(x=x, c=c, r=r)), "WEBP", lossless=True, quality=100, method=6, exact=True)
            if preview:
                fr = 14
                box = (0, fr * TILE, TILE, (fr + 1) * TILE)
                for board, im in ((board_new, img), (board_old, src.convert("RGBA"))):
                    board.alpha_composite(im.crop(box).resize((50, 50), Image.NEAREST), (c * 50, r * 50))
        if preview:
            os.makedirs(preview, exist_ok=True)
            board_new.save(os.path.join(preview, f"preview_605_{kind}_{x}_new.png"))
            board_old.save(os.path.join(preview, f"preview_605_{kind}_{x}_old.png"))
        print(kind, x, len(files), "slices")


if __name__ == "__main__":
    main()
