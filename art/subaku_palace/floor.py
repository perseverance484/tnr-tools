#!/usr/bin/env python3
"""Subaku Palace domain floor, 'flow' pattern: one lattice-periodic field, sampled anywhere on the plane.

    python3 floor.py [OUT.webp]        # the 150 px static tile (corner-to-corner hex, stretched 2:1 by the game)

The floor is a field f(x, y) that repeats with the hex lattice, so:
- the static tile is f on one hex (plus a 0.06 bleed so linear filtering opens no seam);
- the cast's clips (2.5 tile heights square, overlapping their neighbours) can sample f past their own hex and land
  on exactly the pixels the neighbouring tiles show, whatever the caster's column parity.

Pattern (regular flat-top hex, circumradius 1, y down):
- the current: one sinuous band per hex from the lower-left edge midpoint (M2) to the upper-right one (M5), square
  to both edges; its width swells to 1.4x mid-hex and returns to the same width at both ends, so the joins are exact
  and the stacked hexes make long calligraphic currents sweeping across the whole domain;
- the eddies: thin arcs round the lower-right and upper-left corners (M0-M1, M3-M4), radius 1/2, square to the edges;
  across the lattice they chain into secondary filaments between the currents;
- two spiral curls per hex shed off the current into the open stone (they touch no edge, so they need no join),
  point-symmetric, so the field never reads as a single repeated hook;
- the stone: periodic flagstones (Voronoi seeds repeating with the lattice), dark mortar, a share of the joints
  glowing ember (the director's red cracks).
Pillow only, deterministic. Materials sampled from the director's tile (stone mean (40, 36, 33), gold (190, 134, 52),
cracks (128, 3, 2)); the gold is quieter at rest so the cast's burning current reads.
"""
import math
import os
import random
import sys

from PIL import Image

SQ3 = math.sqrt(3)
H = SQ3 / 2
CORNERS = [(math.cos(math.radians(60 * k)), math.sin(math.radians(60 * k))) for k in range(6)]
NEIGH = [(0, 0), (0, SQ3), (0, -SQ3), (1.5, H), (1.5, -H), (-1.5, H), (-1.5, -H)]

STONE = [(44, 38, 36), (52, 45, 42), (38, 33, 32), (58, 50, 46), (47, 41, 40), (41, 35, 33)]
MORTAR = (14, 9, 8)
EMBER = [(110, 12, 8), (184, 28, 16), (255, 74, 28)]
GOLD_EDGE = (40, 21, 6)
GOLD = [(84, 50, 12), (124, 80, 20), (156, 108, 34), (186, 140, 58), (216, 178, 102)]
BW = 0.09                       # base half-width of the current (hex radius units)
AMP = 0.24                      # the current's sweep
CURL_W = 0.042
BLEED = 0.06

_rnd = random.Random(7)
SEEDS = []
while len(SEEDS) < 13:
    x, y = _rnd.uniform(-1, 1), _rnd.uniform(-H, H)
    if abs(y) <= H and SQ3 * abs(x) + abs(y) <= SQ3 and all(math.hypot(x - a, y - b) > 0.36 for a, b, _ in SEEDS):
        SEEDS.append((x, y, len(SEEDS)))
PTS = [(x + dx, y + dy, i) for x, y, i in SEEDS for dx, dy in NEIGH + [(3, 0), (-3, 0), (1.5, 3 * H), (-1.5, 3 * H),
                                                                       (1.5, -3 * H), (-1.5, -3 * H), (0, 2 * SQ3),
                                                                       (0, -2 * SQ3)]]
GLOWING = {(a, b) for a in range(13) for b in range(13) if a < b and _rnd.random() < 0.40}

# the current runs along direction 150 deg (M5 at 330 deg -> M2 at 150 deg); w = 0 at M5, 1 at M2
UA = math.radians(150)
UX, UY = math.cos(UA), math.sin(UA)


def g(w):
    return AMP * math.sin(2 * math.pi * w) * (1 - math.cos(2 * math.pi * w)) / 2


def current_point(w, off):
    t = 2 * w - 1
    return t * H * UX + off * UY, t * H * UY - off * UX


CURLS = []
for w0, side in ((0.30, 1), (0.70, -1)):
    cx, cy = current_point(w0, g(w0) + side * 0.30)
    CURLS.append((cx, cy, side))


def reduce(x, y):
    """Plane point -> (local x, local y) in its own hex (nearest lattice centre)."""
    i0 = round(x / 1.5)
    best = None
    for i in (i0 - 1, i0, i0 + 1):
        j = round(y / SQ3 - i / 2)
        for jj in (j - 1, j, j + 1):
            cx, cy = 1.5 * i, SQ3 * (jj + i / 2)
            d = (x - cx) ** 2 + (y - cy) ** 2
            if best is None or d < best[0]:
                best = (d, x - cx, y - cy)
    return best[1], best[2]


def profile(s, streak=0.0):
    a = abs(s)
    if a > 0.84:
        return GOLD_EDGE
    if a > 0.64:
        return GOLD[0]
    if a < 0.14:
        return GOLD[1]                     # the engraved channel the current runs in
    return GOLD[min(4, 2 + (a < 0.40) + (a < 0.30 and streak > 0.55))]


def sample(x, y):
    """Local point (inside its hex, plus bleed) -> (rgb, gold, channel, crack, along) with along in 0..1 or -1."""
    # stone
    best = sorted(((x - a) ** 2 + (y - b) ** 2, a, b, i) for a, b, i in PTS)[:2]
    d1, sx, sy, i1 = best[0]
    d2, _, _, i2 = best[1]
    e = math.sqrt(d2) - math.sqrt(d1)
    col = STONE[i1 % len(STONE)]
    vx, vy = x - sx, y - sy
    n = math.hypot(vx, vy) or 1
    lit = (vx * -0.6 + vy * -0.8) / n
    k = 1.0 + (0.22 * lit * (1 - e / 0.07) if e < 0.07 else 0)
    noise = (hash((int(x * 977) * 7919) ^ (int(y * 977) * 104729)) % 13) - 6
    c = tuple(max(0, min(255, int(v * k + noise))) for v in col)
    gold = chan = crack = 0
    along = -1.0
    glow = tuple(sorted((i1, i2))) in GLOWING
    if e < (0.034 if glow else 0.022):
        c = MORTAR
        if glow:
            c = EMBER[2] if e < 0.012 else EMBER[1] if e < 0.024 else EMBER[0]
            crack = 255 if e < 0.024 else 140
    elif e < 0.05 and glow:
        c = tuple(int(c[j] * 0.6 + EMBER[0][j] * 0.4) for j in range(3))
    bands = []
    # the current
    t = (x * UX + y * UY) / H
    w = (t + 1) / 2
    if -0.03 <= w <= 1.03:
        f = g(w)
        slope = (g(w + 1e-4) - f) / (1e-4 * 2 * H)
        off = x * UY - y * UX
        hw = BW * (1.0 + 0.4 * math.sin(math.pi * max(0.0, min(1.0, w))))
        bands.append(((off - f) / math.sqrt(1 + slope * slope), hw, w, True))
    # eddy arcs round corners 1 and 4
    for kk in (1, 4):
        cx, cy = CORNERS[kk]
        r = math.hypot(x - cx, y - cy)
        ang = math.atan2(y - cy, x - cx)
        base = math.atan2(-cy, -cx)
        da = (ang - base + math.pi) % (2 * math.pi) - math.pi
        bands.append((r - 0.5, BW * 0.62, (da + math.pi / 3) / (2 * math.pi / 3), True))
    for dd, hw, a, _ in bands:
        if hw < abs(dd) <= hw * 1.3:
            c = tuple(int(v * 0.45) for v in c)
    for dd, hw, a, _ in bands:
        if abs(dd) <= hw:
            s = dd / hw
            streak = 0.5 + 0.5 * math.sin(a * 23.0 + 1.3) * math.sin(a * 7.0)
            fade = min(1.0, a / 0.15, (1 - a) / 0.15)
            c = profile(s, streak * fade)
            gold = 255
            if abs(s) < 0.24:
                chan, along = 255, max(0.0, min(1.0, a))
    # the curls: a 1.6-turn spiral, opening toward the current
    for cx, cy, side in CURLS:
        r = math.hypot(x - cx, y - cy)
        if r < 0.20:
            th = math.atan2(y - cy, x - cx) * side
            bestd = 9.0
            for kk in range(-1, 3):
                phi = th % (2 * math.pi) + 2 * math.pi * kk
                if 0 <= phi <= 3.2 * math.pi:
                    bestd = min(bestd, abs(r - (0.018 + 0.016 * phi)))
            if bestd <= CURL_W:
                c = profile(bestd / CURL_W)
                gold = 255
                if bestd / CURL_W < 0.3:
                    chan = 255
            elif bestd <= CURL_W * 1.35:
                c = tuple(int(v * 0.5) for v in c)
    return c, gold, chan, crack, along


def inside(x, y, eps=0.0):
    return abs(y) <= H + eps and SQ3 * abs(x) + abs(y) <= SQ3 + eps


def tile(n=512, size=150):
    """The static tile: the canvas is the hex corner to corner (the game stretches it to the 2:1 hex box)."""
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    p = img.load()
    for py in range(n):
        for px in range(n):
            x, y = (px + 0.5 - n / 2) / (n / 2), (py + 0.5 - n / 2) / (n / 2) * H
            if inside(x, y, BLEED):
                lx, ly = reduce(x, y)
                p[px, py] = sample(lx, ly)[0] + (255,)
    return img.convert('RGBa').resize((size, size), Image.BOX).convert('RGBA')


def field_masks(clip, ratio=2.5):
    """Gold / channel / crack / along masks (L) of the field over one clip square centred on a hex, plus the hex-norm
    map (0 at the centre, 255 at 2x the hex radius) for timing. Clip px -> regular coords: one tile height = ratio
    clip/ratio px; x in hex radii = dx_h, y = dy_h * sqrt3."""
    G, C, K, A, R = (Image.new('L', (clip, clip), 0) for _ in range(5))
    gp, cp, kp, ap, rp = G.load(), C.load(), K.load(), A.load(), R.load()
    for py in range(clip):
        for px in range(clip):
            dxh = (px + 0.5 - clip / 2) / clip * ratio
            dyh = (py + 0.5 - clip / 2) / clip * ratio
            x, y = dxh, dyh * SQ3
            lx, ly = reduce(x, y)
            _, gg, cc, kk, al = sample(lx, ly)
            gp[px, py], cp[px, py], kp[px, py] = gg, cc, kk
            ap[px, py] = 0 if al < 0 else 1 + int(254 * al)
            nrm = max(abs(y) / H, (SQ3 * abs(x) + abs(y)) / SQ3)      # 1 on this hex's edge
            rp[px, py] = min(255, int(nrm * 127.5))
    return G, C, K, A, R


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exports',
                                                              'tile_sbk_domain_v3.webp')
    tile().save(out, lossless=True, method=6)
    print('wrote', out, os.path.getsize(out), 'curls', [(round(a, 3), round(b, 3)) for a, b, _ in CURLS])
