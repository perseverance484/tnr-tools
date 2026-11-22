#!/usr/bin/env python3
"""FCF v24, full: the whole of v23 as one visual on the user, for the extended PR (2026-11-22).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v24/cut_full.py

Needs the PR's two additions: a visual tag with target SELF may be scaled past 3 (up to 15), and an effect sheet may
be a grid of square cells. v23 is rendered on a transparent board, then a square of SCALE tile heights centred on the
user's hex is cut from every frame (the engine draws a clip as a square of tile height x scale on the hex's centre),
its last few percent faded so nothing ends on a hard edge. Frames are 30 ms; the grid is 7 x 7 cells of CELL px.
Writes anim_fcf_v24_full.webp and preview_fcf_v24_full.gif (the engine's playback on the board).
"""
import math
import os
import sys

from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["FCF_STEP"] = "30"
sys.path.insert(0, os.path.join(HERE, "..", "v23"))
import fcf_v23 as F  # noqa: E402

SCALE = 14           # the area's farthest hex edge sits 272 px (2x board) from the user's hex centre: 14 x 38.9 / 2
CELL = 320           # 7 x 7 cells of 320 px: 2240 px square, and under the 450 KB upload ceiling
MS = 30


def edge_fade(size, band=0.06):
    m = Image.new("L", (size, size), 255)
    px = m.load()
    b = size * band
    for y in range(size):
        for x in range(size):
            d = min(x, y, size - 1 - x, size - 1 - y)
            if d < b:
                px[x, y] = int(255 * (d / b) ** 1.5)
    return m


def main():
    cx, cy = F.M.TILES[F.M.CASTER]
    side = SCALE * F.TH
    box = tuple(int(round(v)) for v in (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2))
    fade = edge_fade(CELL)
    cells = []

    def sink(t, fr):
        c = fr.crop(box).resize((CELL, CELL), Image.LANCZOS)
        c.putalpha(ImageChops.multiply(c.getchannel("A"), fade))
        cells.append(c)

    F.main(board=lambda: Image.new("RGBA", (F.W, F.H), (0, 0, 0, 0)), sink=sink)
    cols = math.ceil(math.sqrt(len(cells)))
    rows = math.ceil(len(cells) / cols)
    sheet = Image.new("RGBA", (cols * CELL, rows * CELL), (0, 0, 0, 0))
    for i, c in enumerate(cells):
        sheet.alpha_composite(c, ((i % cols) * CELL, (i // cols) * CELL))
    assert max(sheet.size) <= 4096
    # 256 colours and alpha in steps of 16, empty pixels kept at exactly zero (the palette alone lifts them to a
    # faint haze over the whole square): saved lossless, this fits the upload ceiling
    alpha = sheet.getchannel("A").point(lambda v: 0 if v == 0 else max(16, min(255, round(v / 16) * 16)))
    sheet = sheet.quantize(256, method=Image.Quantize.FASTOCTREE).convert("RGBA")
    sheet.putalpha(alpha)
    out = os.path.join(HERE, "anim_fcf_v24_full.webp")
    sheet.save(out, "WEBP", lossless=True, quality=100, method=6)
    print(os.path.basename(out), sheet.size, len(cells), "frames", f"{cols}x{rows}", os.path.getsize(out), "bytes")
    # the engine's playback: one clip of SCALE tile heights on the caster's hex
    back = [sheet.crop(((i % cols) * CELL, (i // cols) * CELL, (i % cols + 1) * CELL, (i // cols + 1) * CELL))
            for i in range(len(cells))]
    shots = F.BV.render([], (back, MS, SCALE), "Extended PR: one visual on the user", step=30, tail=150)
    F.BV.save(shots, os.path.join(HERE, "preview_fcf_v24_full.gif"), step=30)


if __name__ == "__main__":
    main()
