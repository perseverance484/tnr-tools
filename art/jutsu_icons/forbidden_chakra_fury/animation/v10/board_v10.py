#!/usr/bin/env python3
"""Board previews for FCF v10 and the upstream PR GIFs (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v10/board_v10.py

Simulates the PR's renderer on the real board geometry (2:1 squashed offset hexes, odd columns shoved down): each
ground effect plays its clip on every tile of the area, varied per tile by combatEffects.tileVariation (ported below,
checked equal to the TypeScript earlier: 0 mismatches over 120 tiles), with the delay
round(hashFraction * stagger) + ripple * hexDistance(caster tile, tile), capped at 2000 ms. The caster's visual plays
on the caster's tile. Layers draw glow first, then strikes, then the caster.

Outputs:
  preview_fcf_v10_board.gif   v10 with every setting on (what the jutsu would look like)
  pr_fcf_today.gif            the same v10 art as the engine draws it today: one clip, every tile alike
  pr_fcf_varied.gif           mirror + alternate + stagger 120 + ripple 90
  pr_fcf_compare.gif          the two stacked, on one clock
"""
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v10 as B  # noqa: E402

M = 0xFFFFFFFF
MAX_DELAY = 2000


def tile_hash(col, row):
    imul = lambda a, b: (a * b) & M  # noqa: E731
    h = (imul((col + 0x632BE5AB) & M, 0x27D4EB2D) ^ imul((row + 0x85157AF5) & M, 0x165667B1)) & M
    h = imul(h ^ (h >> 15), 0x2C1B3C6D)
    return (h ^ (h >> 12)) & M


def variation(col, row, dist, mirror=False, stagger=0, ripple=0, alternate=False):
    h = tile_hash(col, row)
    delay = min(MAX_DELAY, math.floor((h >> 8) / 0x1000000 * stagger + 0.5) + ripple * dist)
    return mirror and h & 1 == 1, delay, alternate and h & 2 == 2


def cube(c, r):
    z = r - (c - (c & 1)) // 2
    return c, -c - z, z


def dist(a, b):
    return max(abs(x - y) for x, y in zip(cube(*a), cube(*b)))


def render(layers, caster_clip, title, cols=12, rows=8, caster=(5, 4), radius=4, px=2, step=40, tail=600):
    """layers: [(frames_a, frames_b or None, ms, scale, settings dict)] drawn in order under the caster."""
    STACK = 0.25
    hs = 360 / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    W, H = int(360 * px), int((rows + 0.5) * h)
    tiles = {(c, r): (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))
             for c in range(cols) for r in range(rows)}
    area = sorted([k for k in tiles if k != caster and dist(k, caster) <= radius], key=lambda k: tiles[k][1])
    base = Image.new("RGBA", (W, H), (44, 52, 40, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in tiles.values():
        d.polygon([(x - w / 2, y), (x - w / 4, y - h / 2), (x + w / 4, y - h / 2), (x + w / 2, y),
                   (x + w / 4, y + h / 2), (x - w / 4, y + h / 2)], outline=(255, 255, 255, 34))
    cx, cy = tiles[caster]
    feet, top = cy + 0.4 * h, cy - 1.2 * h
    d.ellipse((cx - w * 0.16, feet - h * 0.09, cx + w * 0.16, feet + h * 0.09), fill=(0, 0, 0, 80))
    d.rounded_rectangle((cx - w * 0.085, top + w * 0.16, cx + w * 0.085, feet - 3), radius=6, fill=(66, 64, 78, 255))
    d.ellipse((cx - w * 0.1, top, cx + w * 0.1, top + w * 0.2), fill=(66, 64, 78, 255))

    def sized(frs, scale):
        e = int(round(h * scale))
        fa = [f.resize((e, e), Image.LANCZOS) for f in frs]
        return e, fa, [f.transpose(Image.FLIP_LEFT_RIGHT) for f in fa]

    plans, total = [], 0
    for frs_a, frs_b, ms, scale, s in layers:
        e, a, am = sized(frs_a, scale)
        b = sized(frs_b, scale)[1:] if frs_b else (a, am)
        plan = {}
        for k in area:
            m, delay, alt = variation(*k, dist(k, caster), **s)
            src = b if alt else (a, am)
            plan[k] = (src[1] if m else src[0], delay)
            total = max(total, delay + len(src[0]) * ms)
        plans.append((e, ms, plan))
    cf, cms, cscale = caster_clip
    ce, ca, _ = sized(cf, cscale)
    total = max(total, len(ca) * cms) + tail
    shots = []
    for t in range(0, total, step):
        im = base.copy()
        for e, ms, plan in plans:
            for k in area:
                frs, delay = plan[k]
                i = (t - delay) // ms
                if t >= delay and i < len(frs):
                    x, y = tiles[k]
                    im.alpha_composite(frs[i], (int(x - e / 2), int(y - e / 2)))
        if t // cms < len(ca):
            im.alpha_composite(ca[t // cms], (int(cx - ce / 2), int(cy - ce / 2)))
        ImageDraw.Draw(im).text((8, 6), title, fill=(255, 255, 255, 235))
        shots.append(im.convert("RGB"))
    return shots


def save(shots, path, step=40):
    shots[0].save(path, save_all=True, append_images=shots[1:], duration=step, loop=0, optimize=True)
    print(os.path.basename(path), len(shots), "frames,", os.path.getsize(path), "bytes")


def stack(top, bottom):
    n = max(len(top), len(bottom))
    W, H = top[0].size
    out = []
    for i in range(n):
        im = Image.new("RGB", (W, H * 2 + 6), (18, 18, 18))
        im.paste(top[min(i, len(top) - 1)], (0, 0))
        im.paste(bottom[min(i, len(bottom) - 1)], (0, H + 6))
        out.append(im)
    return out


def main():
    c = B.clips()
    caster = c["caster"]
    sa, sb, gl = c["strike_a"][0], c["strike_b"][0], c["glow"][0]
    on = dict(mirror=True, stagger=120, ripple=90)
    varied = render([(gl, None, B.G_MS, 2, on), (sa, sb, B.S_MS, 3, dict(on, alternate=True))], caster,
                    "Tile variation: mirror + alternate + stagger 120 ms + ripple 90 ms/hex")
    today = render([(gl, None, B.G_MS, 2, {}), (sa, None, B.S_MS, 3, {})], caster,
                   "Today: one clip, every tile alike, all at once")
    save(varied, os.path.join(HERE, "preview_fcf_v10_board.gif"))
    save(today, os.path.join(HERE, "pr_fcf_today.gif"))
    save(varied, os.path.join(HERE, "pr_fcf_varied.gif"))
    save(stack(today, varied), os.path.join(HERE, "pr_fcf_compare.gif"))


if __name__ == "__main__":
    main()
