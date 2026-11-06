#!/usr/bin/env python3
"""Subaku Palace domain floor, 'bold flow' (director 2026-11-05: bolder, sparser, toward his original tile).

    python3 floor.py [OUT.webp]        # the 150 px static tile (corner-to-corner hex, stretched 2:1 by the game)

The floor is a field f(x, y) that repeats with the hex lattice, so:
- the static tile is f on one hex (plus a 0.06 bleed so linear filtering opens no seam);
- the cast's clips (2.5 tile heights square) sample f past their own hex and land on exactly the pixels the
  neighbouring tiles show, on either caster column parity.

Pattern (regular flat-top hex, circumradius 1, y down), few bold elements and broad dark stone:
- the current: ONE bold bevelled band per hex from the lower-left edge midpoint (M2) to the upper-right one (M5),
  square to both edges, same width at both ends (the joins are exact). It swells 1.35x mid-hex and sweeps in a broad S,
  so the stacked hexes make long calligraphic currents across the whole domain, 1.5 hex radii apart;
- the curl: one bold spiral tendril per hex branching off the current's concave side into the open stone;
- no corner arcs (they read as fish scale at 50 px);
- every feature is evaluated at the 7 lattice translations, so nothing is cut at a hex edge;
- the bevel is lit from the upper left (a highlight on the lit flank, a shadow on the far one); the normal is continuous
  across hexes, so the light matches at the joins;
- the stone: periodic basalt flagstones (Voronoi seeds repeating with the lattice), dark mortar, a share of joints
  glowing ember (the director's red cracks).
Pillow only, deterministic.
"""
import math
import os
import random
import sys

from PIL import Image

SQ3 = math.sqrt(3)
H = SQ3 / 2
NEIGH = [(0, 0), (0, SQ3), (0, -SQ3), (1.5, H), (1.5, -H), (-1.5, H), (-1.5, -H)]

STONE = [(42, 36, 34), (50, 43, 40), (36, 31, 30), (56, 48, 44), (45, 39, 38), (39, 33, 31)]
MORTAR = (14, 9, 8)
EMBER = [(110, 12, 8), (184, 28, 16), (255, 74, 28)]
OUTLINE = (40, 21, 6)
# burnished demon gold, dark rim -> highlight (bold, like the director's tile; the cast's burning gold is brighter)
GOLD = [(96, 58, 14), (140, 92, 24), (180, 128, 42), (214, 164, 70), (240, 204, 124)]
BW = 0.15                       # base half-width of the current (hex radius units)
SWELL = 0.35
AMP = 0.30                      # the S sweep
CURL_W = 0.07
LIGHT = (-0.6, -0.8)
BLEED = 0.06

_rnd = random.Random(11)
SEEDS = []
while len(SEEDS) < 11:
    x, y = _rnd.uniform(-1, 1), _rnd.uniform(-H, H)
    if abs(y) <= H and SQ3 * abs(x) + abs(y) <= SQ3 and all(math.hypot(x - a, y - b) > 0.42 for a, b, _ in SEEDS):
        SEEDS.append((x, y, len(SEEDS)))
_FAR = NEIGH + [(3, 0), (-3, 0), (1.5, 3 * H), (-1.5, 3 * H), (1.5, -3 * H), (-1.5, -3 * H), (0, 2 * SQ3),
                (0, -2 * SQ3)]
PTS = [(x + dx, y + dy, i) for x, y, i in SEEDS for dx, dy in _FAR]
GLOWING = {(a, b) for a in range(11) for b in range(11) if a < b and _rnd.random() < 0.38}

UA = math.radians(150)          # the current runs M5 (330 deg) -> M2 (150 deg); w = 0 at M5, 1 at M2
UX, UY = math.cos(UA), math.sin(UA)
NX, NY = UY, -UX                # the current's base normal (positive offset side)


def g(w):
    return AMP * math.sin(2 * math.pi * w) * (1 - math.cos(2 * math.pi * w)) / 2


def gp(w):
    return (g(w + 1e-4) - g(w - 1e-4)) / 2e-4


def current_point(w, off):
    t = 2 * w - 1
    return t * H * UX + off * NX, t * H * UY + off * NY


# the curl: on the concave side of the S's first lobe, its outer turn merging into the current
W0 = 0.30
SIDE = -1 if g(W0) > 0 else 1
CURL_R = 0.30
CX, CY = current_point(W0, g(W0) + SIDE * (CURL_R + 0.02))
TURNS = 1.25
CURL_B = (CURL_R - 0.05) / (TURNS * 2 * math.pi)


def reduce(x, y):
    """Plane point -> local coords in its own hex (nearest lattice centre)."""
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


def current_dist(x, y):
    """(signed distance / half-width, lit term) to this hex's current, ends capped at the midpoints."""
    t = (x * UX + y * UY) / H
    w = (t + 1) / 2
    if not -0.25 <= w <= 1.25:
        return None
    wc = max(0.0, min(1.0, w))
    off = x * NX + y * NY
    f = g(wc)
    s = gp(wc) / (2 * H)
    d = (off - f) / math.sqrt(1 + s * s)
    if w != wc:                                     # past an end: distance to the end cap (exactly at the midpoint)
        px, py = current_point(wc, f)
        d = math.copysign(math.hypot(x - px, y - py), off - f) if abs(off - f) > 1e-9 else math.hypot(x - px, y - py)
    hw = BW * (1 + SWELL * math.sin(math.pi * wc))
    # normal for the bevel: rotate the base normal by the curve's slope
    ang = math.atan(s)
    nx = NX * math.cos(ang) - UX * math.sin(ang)
    ny = NY * math.cos(ang) - UY * math.sin(ang)
    return d / hw, nx * LIGHT[0] + ny * LIGHT[1]


def curl_dist(x, y):
    vx, vy = x - CX, y - CY
    r = math.hypot(vx, vy)
    if r > CURL_R + CURL_W * 1.4:
        return None
    th = (math.atan2(vy, vx) * SIDE) % (2 * math.pi)
    best = 9.0
    for k in range(0, 3):
        phi = th + 2 * math.pi * k
        if phi <= TURNS * 2 * math.pi + 0.3:
            rr = 0.05 + CURL_B * phi
            if abs(r - rr) < abs(best):
                best = r - rr
    lit = (vx * LIGHT[0] + vy * LIGHT[1]) / (r or 1) * (1 if best > 0 else -1)
    return best / CURL_W, lit


def features(x, y):
    out = []
    for dx, dy in NEIGH:
        for fn in (current_dist, curl_dist):
            v = fn(x - dx, y - dy)
            if v is not None:
                out.append(v)
    return out


def gold_colour(s, lit):
    """Bevelled band: outline, rim, face; the flank facing the light catches a highlight, the far one darkens."""
    a = abs(s)
    if a > 0.88:
        return OUTLINE
    side_lit = (s * lit) > 0
    if a > 0.66:
        return GOLD[1] if side_lit else GOLD[0]
    if a > 0.40:
        return GOLD[4] if side_lit else GOLD[2]
    if a < 0.12:
        return GOLD[1]                              # the engraved channel the cast's current runs in
    return GOLD[3]


def sample(x, y):
    """Local point -> (rgb, gold, channel, crack, along=-1)."""
    best = sorted(((x - a) ** 2 + (y - b) ** 2, a, b, i) for a, b, i in PTS)[:2]
    d1, sx, sy, i1 = best[0]
    d2, _, _, i2 = best[1]
    e = math.sqrt(d2) - math.sqrt(d1)
    col = STONE[i1 % len(STONE)]
    vx, vy = x - sx, y - sy
    n = math.hypot(vx, vy) or 1
    lit = (vx * LIGHT[0] + vy * LIGHT[1]) / n
    k = 1.0 + (0.24 * lit * (1 - e / 0.08) if e < 0.08 else 0)
    noise = (hash((int(x * 977) * 7919) ^ (int(y * 977) * 104729)) % 11) - 5
    c = tuple(max(0, min(255, int(v * k + noise))) for v in col)
    gold = chan = crack = 0
    glow = tuple(sorted((i1, i2))) in GLOWING
    if e < (0.036 if glow else 0.022):
        c = MORTAR
        if glow:
            c = EMBER[2] if e < 0.013 else EMBER[1] if e < 0.026 else EMBER[0]
            crack = 255 if e < 0.026 else 140
    elif e < 0.05 and glow:
        c = tuple(int(c[j] * 0.6 + EMBER[0][j] * 0.4) for j in range(3))
    feats = features(x, y)
    for s, _ in feats:                              # cast shadow round every band
        if 1.0 < abs(s) <= 1.35:
            c = tuple(int(v * 0.42) for v in c)
    inside_band = [(abs(s), s, l) for s, l in feats if abs(s) <= 1.0]
    if inside_band:
        _, s, l = min(inside_band)
        c = gold_colour(s, l)
        gold = 255
        crack = 0
        if abs(s) < 0.2:
            chan = 255
    return c, gold, chan, crack, -1.0


def inside(x, y, eps=0.0):
    return abs(y) <= H + eps and SQ3 * abs(x) + abs(y) <= SQ3 + eps


def tile(n=384, size=150):
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
    map (0 at the centre, 127.5 on the hex edge)."""
    G, C, K, A, R = (Image.new('L', (clip, clip), 0) for _ in range(5))
    gp_, cp, kp, rp = G.load(), C.load(), K.load(), R.load()
    for py in range(clip):
        for px in range(clip):
            x = (px + 0.5 - clip / 2) / clip * ratio
            y = (py + 0.5 - clip / 2) / clip * ratio * SQ3
            lx, ly = reduce(x, y)
            _, gg, cc, kk, _ = sample(lx, ly)
            gp_[px, py], cp[px, py], kp[px, py] = gg, cc, kk
            nrm = max(abs(y) / H, (SQ3 * abs(x) + abs(y)) / SQ3)
            rp[px, py] = min(255, int(nrm * 127.5))
    return G, C, K, A, R


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exports',
                                                              'tile_sbk_domain_v3.webp')
    tile().save(out, lossless=True, method=6)
    print('wrote', out, os.path.getsize(out), 'curl centre', round(CX, 3), round(CY, 3), 'side', SIDE)
