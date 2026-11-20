#!/usr/bin/env python3
"""Before/after GIFs for the upstream "vary area clips per tile" PR (2026-11-20).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v9/tile_variation_demo.py

Same art both times (FCF v9: the caster clip and the lightning field). "Today" shows the engine as it is: every
tile of the area plays the identical field clip at the same moment. "With tile variation" uses the PR's three
per-effect settings, simulated with the engine's own tile hash (tileVariation, ported here and checked equal on a
12 x 10 board): animationMirror, animationStagger 300 ms, and animationAlternate (a second vein pattern that meets
the same edge midpoints, so the network still joins).
"""
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v9 as V  # noqa: E402

M = 0xFFFFFFFF


def tile_variation(col, row, mirror, stagger, alternate):
    """Port of combatEffects.tileVariation (uint32 maths as JavaScript's Math.imul and >>>)."""
    imul = lambda a, b: (a * b) & M  # noqa: E731
    h = (imul((col + 0x632BE5AB) & M, 0x27D4EB2D) ^ imul((row + 0x85157AF5) & M, 0x165667B1)) & M
    h = imul(h ^ (h >> 15), 0x2C1B3C6D)
    h = (h ^ (h >> 12)) & M
    return (bool(mirror) and h & 1 == 1, math.floor((h >> 8) / 0x1000000 * stagger + 0.5),
            bool(alternate) and h & 2 == 2)


def board(caster_frs, field_a, field_b, out, title, vary, cols=12, rows=8, caster=(3, 4), radius=4, px=2):
    STACK = 0.25
    hs = 360 / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    W, H = int(360 * px), int((rows + 0.5) * h)
    tiles = {(c, r): (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))
             for c in range(cols) for r in range(rows)}

    def cube(c, r):
        z = r - (c - (c & 1)) // 2
        return c, -c - z, z
    field = sorted([k for k in tiles if k != caster and max(abs(a - b) for a, b in zip(cube(*k), cube(*caster))) <= radius],
                   key=lambda k: tiles[k][1])
    base = Image.new("RGBA", (W, H), (36, 40, 36, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in tiles.values():
        d.polygon([(x - w / 2, y), (x - w / 4, y - h / 2), (x + w / 4, y - h / 2), (x + w / 2, y), (x + w / 4, y + h / 2),
                   (x - w / 4, y + h / 2)], outline=(255, 255, 255, 30))
    cx, cy = tiles[caster]
    feet, top = cy + 0.4 * h, cy - 1.2 * h
    d.ellipse((cx - w * 0.16, feet - h * 0.09, cx + w * 0.16, feet + h * 0.09), fill=(0, 0, 0, 80))
    d.rounded_rectangle((cx - w * 0.085, top + w * 0.16, cx + w * 0.085, feet - 3), radius=6, fill=(66, 64, 78, 255))
    d.ellipse((cx - w * 0.1, top, cx + w * 0.1, top + w * 0.2), fill=(66, 64, 78, 255))
    fe, ce = int(round(h * 2)), int(round(h * 3))
    rs = lambda frs, e: [f.resize((e, e), Image.LANCZOS) for f in frs]  # noqa: E731
    fa, fb, ca = rs(field_a, fe), rs(field_b, fe), rs(caster_frs, ce)
    fam = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in fa]
    fbm = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in fb]
    plan = {}
    for k in field:
        m, delay, alt = tile_variation(*k, *((True, 300, True) if vary else (False, 0, False)))
        frs = (fbm if m else fb) if alt else (fam if m else fa)
        plan[k] = (frs, delay)
    total = max(len(ca) * V.C_MS, max(delay + len(frs) * V.F_MS for frs, delay in plan.values())) + 500
    shots, step = [], 20
    for t in range(0, total, step):
        im = base.copy()
        for k in field:
            frs, delay = plan[k]
            i = (t - delay) // V.F_MS
            if 0 <= t - delay and i < len(frs):
                x, y = tiles[k]
                im.alpha_composite(frs[i], (int(x - fe / 2), int(y - fe / 2)))
        if t // V.C_MS < len(ca):
            im.alpha_composite(ca[t // V.C_MS], (int(cx - ce / 2), int(cy - ce / 2)))
        ImageDraw.Draw(im).text((8, 6), f"{title}   t={t} ms", fill=(255, 255, 255, 230))
        shots.append(im.convert("RGB"))
    shots[0].save(out, save_all=True, append_images=shots[1:], duration=step, loop=0, optimize=True)
    return shots


def main():
    caster = V.caster_frames()
    a, b = V.field_frames(9), V.field_frames(23)
    today = board(caster, a, a, os.path.join(HERE, "pr_fcf_today_uniform.gif"), "Today: one clip, every tile alike", False)
    varied = board(caster, a, b, os.path.join(HERE, "pr_fcf_tile_variation.gif"),
                   "Tile variation: mirror + 300 ms stagger + alternate clip", True)
    n = max(len(today), len(varied))
    W, H = today[0].size
    pair = []
    for i in range(n):
        im = Image.new("RGB", (W, H * 2 + 6), (20, 20, 20))
        im.paste(today[min(i, len(today) - 1)], (0, 0))
        im.paste(varied[min(i, len(varied) - 1)], (0, H + 6))
        pair.append(im)
    p = os.path.join(HERE, "pr_fcf_side_by_side.gif")
    pair[0].save(p, save_all=True, append_images=pair[1:], duration=20, loop=0, optimize=True)
    for f in ("pr_fcf_today_uniform.gif", "pr_fcf_tile_variation.gif", "pr_fcf_side_by_side.gif"):
        print(f, os.path.getsize(os.path.join(HERE, f)), "bytes")


if __name__ == "__main__":
    main()
