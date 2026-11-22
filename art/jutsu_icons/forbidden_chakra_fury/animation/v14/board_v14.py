#!/usr/bin/env python3
"""Board preview for FCF v14, simulating the PR's per-tile variation plus the proposed `animationAim` (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v14/board_v14.py

Aim: each tile's clip is turned so its right-hand side points away from the caster's tile (screen angle from the
caster tile centre to the tile centre); mirror flips across that axis (top/bottom) instead of left/right.
Writes preview_fcf_v14_board.gif and stills_fcf_v14.png.
"""
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "v10"))
import board_v10 as BV  # noqa: E402
import build_v14 as B  # noqa: E402

BEATS = [("1 Storm forms", 280), ("2 Fury", 440), ("3 Lash out", 560), ("4 Arcing out", 680), ("5 Full storm", 840),
         ("6 Settle", 1400)]


def hexpoly(x, y, w, h):
    return [(x - w / 2, y), (x - w / 4, y - h / 2), (x + w / 4, y - h / 2), (x + w / 2, y), (x + w / 4, y + h / 2),
            (x - w / 4, y + h / 2)]


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
        d.polygon(hexpoly(x, y, w, h), outline=(255, 255, 255, 30))

    def figure(k, col):
        x, y = tiles[k]
        feet, top = y + 0.4 * h, y - 1.2 * h
        d.ellipse((x - w * 0.16, feet - h * 0.09, x + w * 0.16, feet + h * 0.09), fill=(0, 0, 0, 80))
        d.rounded_rectangle((x - w * 0.085, top + w * 0.16, x + w * 0.085, feet - 3), radius=6, fill=col)
        d.ellipse((x - w * 0.1, top, x + w * 0.1, top + w * 0.2), fill=col)
    for k in enemies:
        figure(k, (96, 58, 52, 255))
    figure(caster, (52, 50, 66, 255))
    cx, cy = tiles[caster]

    layers, total = [], 0
    for key in ("floor", "storm"):
        s = dict(B.SETTINGS[key])
        aim = s.pop("aim", False)
        fa, ms, scale = clips[key + "_a"]
        fb = clips[key + "_b"][0]
        e = int(round(h * scale))
        sa = [f.resize((e, e), Image.LANCZOS) for f in fa]
        sb = [f.resize((e, e), Image.LANCZOS) for f in fb]
        plan = {}
        for k in area:
            m, delay, alt = BV.variation(*k, BV.dist(k, caster), **s)
            src = sb if alt else sa
            x, y = tiles[k]
            if aim:
                deg = -math.degrees(math.atan2(y - cy, x - cx))
                frs = [(f.transpose(Image.FLIP_TOP_BOTTOM) if m else f).rotate(deg, Image.BICUBIC) for f in src]
            else:
                frs = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in src] if m else src
            plan[k] = (frs, delay)
            total = max(total, delay + len(src) * ms)
        layers.append((e, ms, plan))
    cf, cms, cscale = clips["caster"]
    ce = int(round(h * cscale))
    ca = [f.resize((ce, ce), Image.LANCZOS) for f in cf]
    total = max(total, len(ca) * cms) + 500
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
            im.alpha_composite(ca[t // cms], (int(cx - ce / 2), int(cy - ce / 2)))
        shots.append(im.convert("RGB"))
    return shots


def main():
    cs = B.main()
    shots = render(cs)
    BV.save(shots, os.path.join(HERE, "preview_fcf_v14_board.gif"))
    W, H = shots[0].size
    crop = (int(W * 0.04), 0, int(W * 0.9), H)
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]
    sheet = Image.new("RGB", (cw, (ch + 4) * len(BEATS)), (10, 10, 10))
    for i, (name, t) in enumerate(BEATS):
        im = shots[min(t // 40, len(shots) - 1)].crop(crop)
        ImageDraw.Draw(im).text((8, 6), f"{name}  ({t} ms)", fill=(255, 255, 255))
        sheet.paste(im, (0, i * (ch + 4)))
    sheet.save(os.path.join(HERE, "stills_fcf_v14.png"))


if __name__ == "__main__":
    main()
