#!/usr/bin/env python3
"""Subaku Palace domain floor, 'rails' (QA 2026-11-05 on be8646d1, toward the director's refs a-d).

    python3 floor.py [OUT.webp]        # the static tile (corner-to-corner hex, stretched 2:1 by the game)

The floor is a field f(x, y) that repeats with the hex lattice. The tile is f on one hex (plus a 0.06 bleed so linear
filtering opens no seam), and the cast's clips sample the same f, so their light lands on the floor's own pixels.

One tile only: a ground tag has ONE staticAssetPath (validators/combat.ts:121, combatEffects.ts:135) and the engine
has no per-hex variant, so the repeat cannot be broken by tile variants without splitting the mechanic into several
COORDINATES ground tags (which would also leave the 4 parity-only rim hexes without the effect). The repeat is
broken inside the tile instead: a non-directional composition (refs a-d), per-pixel grain, whole tapered joints.

Pattern (regular flat-top hex, circumradius 1, y down):
- the main current: a double-rail gold band M2 -> M5 (lower-left to upper-right edge midpoints), square to both
  edges, a gentle S; the cast's current runs in the recessed channel between the two rails;
- two large arcs, M1-M3 and M0-M4, each centred where its two edges' lines meet (so it leaves both edges square), a
  narrower double rail; the main current weaves over them. Hex to hex the arcs chain at 60 deg, across the currents'
  150 deg, so the gold forms an open woven lattice rather than parallel stripes (the structure of refs a-d);
- every feature is evaluated at the 7 lattice translations, so nothing is cut at a hex edge; every band leaves its
  hex at a midpoint with the same width and a symmetric profile, so the joins are exact;
- the stone: periodic basalt flagstones (16 Voronoi seeds repeating with the lattice), each with its own tone and a
  soft top-left bevel, fine lattice-periodic grain (a sum of reciprocal-lattice waves, so it is seamless too), dark
  mortar lit faintly red, and whole joints glowing ember, tapering to nothing at the stone corners.
Pillow only, deterministic.
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

STONE = [(48, 44, 46), (40, 37, 39), (56, 50, 50), (44, 40, 40), (52, 47, 46), (36, 33, 35), (60, 54, 53)]
MORTAR = (12, 8, 8)
EMBER = [(92, 10, 6), (168, 24, 12), (238, 60, 22), (255, 120, 50)]
OUTLINE = (34, 18, 6)
GROOVE = (70, 40, 10)                        # the recessed channel between the rails
RAIL = [(118, 74, 18), (176, 124, 40), (222, 172, 76), (250, 220, 150)]
MAIN_W = 0.105                               # half-width of the main double rail (hex radius units)
ARC_W = 0.075
AMP = 0.16
LIGHT = (-0.6, -0.8)
BLEED = 0.06
MODE = 'full'     # 'dim': the rails engraved but unlit (the cast's cover, before the gold forms)

_rnd = random.Random(23)
NSEED = 16
SEEDS = []
while len(SEEDS) < NSEED:
    x, y = _rnd.uniform(-1, 1), _rnd.uniform(-H, H)
    if abs(y) <= H and SQ3 * abs(x) + abs(y) <= SQ3 and all(math.hypot(x - a, y - b) > 0.33 for a, b, _ in SEEDS):
        SEEDS.append((x, y, len(SEEDS)))
_FAR = NEIGH + [(3, 0), (-3, 0), (1.5, 3 * H), (-1.5, 3 * H), (1.5, -3 * H), (-1.5, -3 * H), (0, 2 * SQ3),
                (0, -2 * SQ3)]
PTS = [(x + dx, y + dy, i) for x, y, i in SEEDS for dx, dy in _FAR]
TONE = {i: STONE[_rnd.randrange(len(STONE))] for i in range(NSEED)}
GLOWING = {(a, b) for a in range(NSEED) for b in range(NSEED) if a < b and _rnd.random() < 0.34}

# lattice-periodic grain: waves on the reciprocal lattice (a1 = (1.5, H), a2 = (0, SQ3))
_det = 1.5 * SQ3
B1 = (SQ3 / _det, -0.0)                      # b1 . a1 = 1, b1 . a2 = 0
B1 = (1 / 1.5, -H / (1.5 * SQ3))
B2 = (0.0, 1 / SQ3)
WAVES = []
for _ in range(36):
    m, n = _rnd.randint(-14, 14), _rnd.randint(-14, 14)
    if abs(m) + abs(n) < 5:
        continue
    kx, ky = m * B1[0] + n * B2[0], m * B1[1] + n * B2[1]
    WAVES.append((kx, ky, _rnd.uniform(0, 2 * math.pi), 1 / math.hypot(kx, ky) ** 0.6))
_WN = sum(a for *_, a in WAVES)

UA = math.radians(150)
UX, UY = math.cos(UA), math.sin(UA)
NX, NY = UY, -UX


def grain(x, y):
    return sum(a * math.cos(2 * math.pi * (kx * x + ky * y) + p) for kx, ky, p, a in WAVES) / _WN


def g(w):
    return AMP * math.sin(2 * math.pi * w) * (1 - math.cos(2 * math.pi * w)) / 2


def gp(w):
    return (g(w + 1e-4) - g(w - 1e-4)) / 2e-4


def current_dist(x, y):
    t = (x * UX + y * UY) / H
    w = (t + 1) / 2
    if not -0.2 <= w <= 1.2:
        return None
    wc = max(0.0, min(1.0, w))
    off = x * NX + y * NY
    f = g(wc)
    s = gp(wc) / (2 * H)
    if w == wc:
        d = (off - f) / math.sqrt(1 + s * s)
    else:
        tt = 2 * wc - 1
        px, py = tt * H * UX + f * NX, tt * H * UY + f * NY
        d = math.copysign(math.hypot(x - px, y - py), off - f)
    ang = math.atan(s)
    nx = NX * math.cos(ang) - UX * math.sin(ang)
    ny = NY * math.cos(ang) - UY * math.sin(ang)
    return d / MAIN_W, nx * LIGHT[0] + ny * LIGHT[1]


def _mid(k):
    a = math.radians(60 * k + 30)
    return H * math.cos(a), H * math.sin(a)


def _line_meet(k1, k2):
    """Where the lines of edges k1 and k2 meet (the centre of the arc joining their midpoints, square to both)."""
    a1, a2 = math.radians(60 * k1 + 30), math.radians(60 * k2 + 30)
    # n . p = H for both normals
    n1, n2 = (math.cos(a1), math.sin(a1)), (math.cos(a2), math.sin(a2))
    det = n1[0] * n2[1] - n1[1] * n2[0]
    return (H * n2[1] - H * n1[1]) / det, (n1[0] * H - n2[0] * H) / det


ARCS = []
for k1, k2 in ((1, 3), (0, 4)):
    cx, cy = _line_meet(k1, k2)
    mx, my = _mid(k1)
    ARCS.append((cx, cy, math.hypot(mx - cx, my - cy), math.atan2(_mid(k1)[1] - cy, _mid(k1)[0] - cx),
                 math.atan2(_mid(k2)[1] - cy, _mid(k2)[0] - cx)))


def arc_dist(x, y, arc):
    cx, cy, R, a0, a1 = arc
    vx, vy = x - cx, y - cy
    r = math.hypot(vx, vy)
    if abs(r - R) > ARC_W * 1.5:
        return None
    span = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi        # the short way round (inside the hex)
    da = (math.atan2(vy, vx) - a0 + math.pi) % (2 * math.pi) - math.pi
    if span >= 0:
        ok = -0.02 <= da <= span + 0.02
    else:
        ok = span - 0.02 <= da <= 0.02
    if not ok:
        return None
    return (r - R) / ARC_W, (vx * LIGHT[0] + vy * LIGHT[1]) / (r or 1)


def features(x, y):
    """[(s, lit, over)] for every band near (x, y), over all 7 lattice translations; over = 1 for the main current."""
    out = []
    for dx, dy in NEIGH:
        lx, ly = x - dx, y - dy
        v = current_dist(lx, ly)
        if v is not None:
            out.append(v + (1,))
        for arc in ARCS:
            v = arc_dist(lx, ly, arc)
            if v is not None:
                out.append(v + (0,))
    return out


def rail_colour(s, lit):
    """Double rail: outline | rail | groove | rail | outline. The rail facing the light carries the highlight."""
    a = abs(s)
    if a > 0.90:
        return OUTLINE
    if a < 0.26:
        return GROOVE
    if a < 0.34:
        return OUTLINE                       # inner edge of each rail
    lit_side = s * lit > 0
    mid = 0.62
    if abs(a - mid) < 0.12:
        return RAIL[3] if lit_side else RAIL[2]
    return RAIL[2] if lit_side else RAIL[1] if a < 0.80 else RAIL[0]


def sample(x, y):
    """Local point -> (rgb, gold, channel, crack, along=-1)."""
    best = sorted(((x - a) ** 2 + (y - b) ** 2, a, b, i) for a, b, i in PTS)[:3]
    d1, sx, sy, i1 = best[0]
    d2, _, _, i2 = best[1]
    d3 = best[2][0]
    e = math.sqrt(d2) - math.sqrt(d1)                    # distance to the joint (x2)
    corner = math.sqrt(d3) - math.sqrt(d2)               # distance from the joint's ends (stone corners)
    col = TONE[i1]
    vx, vy = x - sx, y - sy
    n = math.hypot(vx, vy) or 1
    lit = (vx * LIGHT[0] + vy * LIGHT[1]) / n
    k = 1.0 + (0.20 * lit * (1 - e / 0.09) if e < 0.09 else 0)
    k *= 1.0 + 0.16 * grain(x, y)
    c = [v * k for v in col]
    glow = tuple(sorted((i1, i2))) in GLOWING
    taper = max(0.0, min(1.0, corner / 0.16)) if glow else 0.0
    crack = 0
    if e < 0.026:
        c = list(MORTAR)
        if taper > 0.05:
            core = 0.026 * taper
            if e < core * 0.45:
                c, crack = list(EMBER[3] if taper > 0.7 else EMBER[2]), 255
            elif e < core:
                c, crack = list(EMBER[2] if taper > 0.5 else EMBER[1]), 255
            else:
                c, crack = list(EMBER[0]), 140
        else:
            c = [MORTAR[0] + 18, MORTAR[1], MORTAR[2]]   # the mortar holds a little red light everywhere
    elif taper > 0.05 and e < 0.026 + 0.07 * taper:      # red light spilling onto the stone edges
        f = 0.55 * taper * (1 - (e - 0.026) / (0.07 * taper))
        c = [c[j] * (1 - f) + EMBER[1][j] * f for j in range(3)]
    c = tuple(max(0, min(255, int(v))) for v in c)
    gold = chan = 0
    feats = features(x, y)
    for s, _, _ in feats:
        if 1.0 < abs(s) <= 1.32:
            c = tuple(int(v * 0.40) for v in c)
    inside = [(-over, abs(s), s, l) for s, l, over in feats if abs(s) <= 1.0]
    if inside:
        neg_over, _, s, l = min(inside)              # the main current wins where it crosses an arc
        c = rail_colour(s, l)
        if MODE == 'dim':                         # an empty engraving: the rails' shape in near-black bronze
            c = tuple(int(v * 0.30) for v in rail_colour(s, -l))
        if neg_over == 0 and MODE != 'dim' and any(o == 1 and 1.0 < abs(ss) <= 1.45 for ss, _, o in feats):
            c = tuple(int(v * 0.5) for v in c)       # the arc passes under the current's shadow
        gold, crack = 255, 0
        if abs(s) < 0.26:
            chan = 255
    return c, gold, chan, crack, -1.0


def reduce(x, y):
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


def inside_hex(x, y, eps=0.0):
    return abs(y) <= H + eps and SQ3 * abs(x) + abs(y) <= SQ3 + eps


def tile(n=400, size=120):
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    p = img.load()
    for py in range(n):
        for px in range(n):
            x, y = (px + 0.5 - n / 2) / (n / 2), (py + 0.5 - n / 2) / (n / 2) * H
            if inside_hex(x, y, BLEED):
                lx, ly = reduce(x, y)
                p[px, py] = sample(lx, ly)[0] + (255,)
    return img.convert('RGBa').resize((size, size), Image.BOX).convert('RGBA')


def field_masks(clip, ratio=2.5):
    """Gold / channel / crack / (unused) masks of the field over one clip square centred on a hex, plus the hex-norm
    map (127.5 on the hex edge)."""
    G, C, K, A, R = (Image.new('L', (clip, clip), 0) for _ in range(5))
    gpx, cp, kp, rp = G.load(), C.load(), K.load(), R.load()
    for py in range(clip):
        for px in range(clip):
            x = (px + 0.5 - clip / 2) / clip * ratio
            y = (py + 0.5 - clip / 2) / clip * ratio * SQ3
            lx, ly = reduce(x, y)
            _, gg, cc, kk, _ = sample(lx, ly)
            gpx[px, py], cp[px, py], kp[px, py] = gg, cc, kk
            rp[px, py] = min(255, int(max(abs(y) / H, (SQ3 * abs(x) + abs(y)) / SQ3) * 127.5))
    return G, C, K, A, R


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exports',
                                                              'tile_sbk_domain_v3.webp')
    tile().save(out, lossless=True, method=6)
    print('wrote', out, os.path.getsize(out))
