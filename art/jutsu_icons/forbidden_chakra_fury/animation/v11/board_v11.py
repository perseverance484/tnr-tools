#!/usr/bin/env python3
"""Board preview for FCF v11 on the real board geometry, with the PR's per-tile variation (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v11/board_v11.py

Uses v10/board_v10.py's port of combatEffects.tileVariation and the board layout. The area is the record's
AOE_SPIRAL_SHOOT range 4: every tile within four hexes of the caster except the caster's own. Three stand-in enemies
sit in the area. Writes preview_fcf_v11_board.gif.
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "v10"))
import board_v10 as BV  # noqa: E402
import build_v11 as B  # noqa: E402


def render(clips, cols=12, rows=8, caster=(5, 4), radius=4, enemies=((8, 3), (2, 5), (6, 7)), px=2, step=40):
    STACK = 0.25
    hs = 360 / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    W, H = int(360 * px), int((rows + 0.5) * h)
    tiles = {(c, r): (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))
             for c in range(cols) for r in range(rows)}
    area = sorted([k for k in tiles if k != caster and BV.dist(k, caster) <= radius], key=lambda k: tiles[k][1])
    base = Image.new("RGBA", (W, H), (52, 64, 44, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in tiles.values():
        d.polygon(BV_hex(x, y, w, h), outline=(255, 255, 255, 30))

    def figure(k, col):
        x, y = tiles[k]
        feet, top = y + 0.4 * h, y - 1.2 * h
        d.ellipse((x - w * 0.16, feet - h * 0.09, x + w * 0.16, feet + h * 0.09), fill=(0, 0, 0, 80))
        d.rounded_rectangle((x - w * 0.085, top + w * 0.16, x + w * 0.085, feet - 3), radius=6, fill=col)
        d.ellipse((x - w * 0.1, top, x + w * 0.1, top + w * 0.2), fill=col)
    for k in enemies:
        figure(k, (96, 58, 52, 255))
    figure(caster, (52, 50, 66, 255))

    def sized(frs, scale):
        e = int(round(h * scale))
        a = [f.resize((e, e), Image.LANCZOS) for f in frs]
        return e, a, [f.transpose(Image.FLIP_LEFT_RIGHT) for f in a]

    layers, total = [], 0
    for key in ("floor", "storm"):
        s = B.SETTINGS[key]
        fa, ms, scale = clips[key + "_a"]
        fb = clips[key + "_b"][0]
        e, a, am = sized(fa, scale)
        _, b, bm = sized(fb, scale)
        plan = {}
        for k in area:
            m, delay, alt = BV.variation(*k, BV.dist(k, caster), **s)
            src = (b, bm) if alt else (a, am)
            plan[k] = (src[1] if m else src[0], delay)
            total = max(total, delay + len(fa) * ms)
        layers.append((e, ms, plan))
    cf, cms, cscale = clips["caster"]
    ce, ca, _ = sized(cf, cscale)
    total = max(total, len(ca) * cms) + 700
    shots = []
    for t in range(0, total, step):
        im = base.copy()
        for e, ms, plan in layers:
            for k in area:
                frs, delay = plan[k]
                i = (t - delay) // ms
                if t >= delay and i < len(frs):
                    x, y = tiles[k]
                    im.alpha_composite(frs[i], (int(x - e / 2), int(y - e / 2)))
        if t // cms < len(ca):
            cx, cy = tiles[caster]
            im.alpha_composite(ca[t // cms], (int(cx - ce / 2), int(cy - ce / 2)))
        shots.append(im.convert("RGB"))
    return shots


def BV_hex(x, y, w, h):
    return [(x - w / 2, y), (x - w / 4, y - h / 2), (x + w / 4, y - h / 2), (x + w / 2, y), (x + w / 4, y + h / 2),
            (x - w / 4, y + h / 2)]


def main():
    shots = render(B.clips())
    BV.save(shots, os.path.join(HERE, "preview_fcf_v11_board.gif"))


if __name__ == "__main__":
    main()
