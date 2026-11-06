#!/usr/bin/env python3
"""Subaku domain tile v2 (proposal): the director's DemonCastleFloor materials on exact interlocking geometry.

    python3 tile_v2.py            # exports/tile_sbk_domain_v3.webp (+ masks for the wave strips, in memory)

Why: the live tile (ref a) only meets its neighbours approximately (about 1 band end in 3 meets exactly), so a
current cannot run hex to hex. Here every band leaves its hex at an edge midpoint, square to the edge, with a
symmetric profile, so identical tiles join everywhere (the Headless Rider domain method, a different pattern).

Geometry (regular flat-top hex, circumradius 1, y down; the game stretches the square canvas to the 2:1 hex box):
- the spine: an S-band from the top-edge midpoint to the bottom-edge midpoint, vertical at both ends. Stacked hexes
  make one continuous wavy gold line down every column;
- two small arcs (radius 1/2) round the left and right corners. They chain hex to hex into zig-zag gold links
  across the columns, so the bands form one connected lattice: the palace floor's inlay.
- the stone: periodic flagstones (a Voronoi floor whose seeds repeat with the hex lattice), so stones cross hex seams
  unbroken; mortar dark, a share of the joints glowing ember (the director's red cracks).
Materials sampled from the director's tile: stone mean (40, 36, 33), gold (190, 134, 52), cracks (128, 3, 2).
Pillow only; deterministic (fixed seed).
"""
import math
import os
import random

from PIL import Image, ImageFilter

N = 512
SQ3 = math.sqrt(3)
SY = 2 / SQ3            # regular-hex y -> canvas (the flat top and bottom touch the canvas edge)
H = SQ3 / 2             # apothem
CORNERS = [(math.cos(math.radians(60 * k)), math.sin(math.radians(60 * k))) for k in range(6)]
LATTICE = [(0, 0), (0, SQ3), (0, -SQ3), (1.5, H), (1.5, -H), (-1.5, H), (-1.5, -H),
           (3, 0), (-3, 0), (1.5, 3 * H), (-1.5, 3 * H), (1.5, -3 * H), (-1.5, -3 * H), (0, 2 * SQ3), (0, -2 * SQ3)]

STONE = [(44, 38, 36), (52, 45, 42), (38, 33, 32), (58, 50, 46), (47, 41, 40), (41, 35, 33)]
MORTAR = (14, 9, 8)
EMBER = [(110, 12, 8), (184, 28, 16), (255, 74, 28)]
GOLD_EDGE = (42, 22, 6)      # dark outline
GOLD = [(84, 50, 12), (124, 80, 20), (156, 108, 34), (184, 138, 56), (212, 172, 96)]  # demon gold at rest (quiet; the lit current is burning gold)
BAND_W = 0.095               # half-width of a band (hex radius units)
ARC_R = 0.5
S_AMP = 0.13
BLEED = 0.06               # content continues past the edge (periodic), so linear filtering opens no seam


def to_hex(px, py):
    return (px + 0.5 - N / 2) / (N / 2), (py + 0.5 - N / 2) / (N / 2) / SY


def inside(x, y, eps=0.0):
    ax, ay = abs(x), abs(y)
    return ay <= H + eps and SQ3 * ax + ay <= SQ3 + eps


def spine_x(y):
    """S-band centre x at height y (y from -H to H), vertical tangent at both ends."""
    u = (y + H) / (2 * H)
    return 0.30 * math.sin(2 * math.pi * u) * (1 - math.cos(2 * math.pi * u)) / 2


def spine_dxdy(y):
    e = 1e-4
    return (spine_x(y + e) - spine_x(y - e)) / (2 * e)


def band_profile(s, along):
    """Colour across a band: s in [-1, 1] across, symmetric so joins match; along in [0, 1] for burnish streaks."""
    a = abs(s)
    if a > 0.86:
        return GOLD_EDGE
    if a > 0.68:
        return GOLD[0]
    if a < 0.10:
        return GOLD[1]          # the engraved channel: the current runs here
    # burnish: slow streaks along the band, faded out near the ends so the seams match
    fade = min(1.0, along / 0.15, (1 - along) / 0.15)
    streak = 0.5 + 0.5 * math.sin(along * 23.0 + 1.3) * math.sin(along * 7.0)
    lvl = 2 + (1 if a < 0.40 else 0) + (1 if (a < 0.30 and streak * fade > 0.55) else 0)
    return GOLD[min(4, lvl)]


def band_dists(x, y, pattern):
    """[(signed distance across, position along 0..1)] for every band near (x, y)."""
    out = []
    if pattern == 'spine':
        if -H - 0.01 <= y <= H + 0.01:
            out.append(((x - spine_x(y)) / math.sqrt(1 + spine_dxdy(y) ** 2), (y + H) / (2 * H)))
        corners = [CORNERS[0], CORNERS[3]]
    elif pattern == 'rings':
        corners = [CORNERS[0], CORNERS[2], CORNERS[4]]
    elif pattern in ('swirl', 'streams'):
        fams = (0, 1, 2) if pattern == 'swirl' else (2,)
        amp = 0.30 if pattern == 'swirl' else 0.22
        for k in fams:
            a = math.radians(60 * k + 30)
            ux, uy = math.cos(a), math.sin(a)
            t = (x * ux + y * uy) / H
            w = (t + 1) / 2
            g = lambda w: amp * math.sin(2 * math.pi * w) * (1 - math.cos(2 * math.pi * w)) / 2
            f = g(w)
            slope = (g(w + 1e-4) - f) / (1e-4 * 2 * H)
            off = x * uy - y * ux
            if pattern == 'swirl' and math.hypot(x, y) < 0.30:
                continue                       # the arms run into the spiral hub
            if -0.02 <= w <= 1.02:
                out.append(((off - f) / math.sqrt(1 + slope * slope), w))
        corners = [] if pattern == 'swirl' else [CORNERS[1], CORNERS[4]]
    elif pattern == 'palace':  # three S-channels through the centre, square to the edges; the medallion covers the meet
        for k in range(3):
            a = math.radians(60 * k + 30)
            ux, uy = math.cos(a), math.sin(a)
            t = (x * ux + y * uy) / H
            w = (t + 1) / 2
            f = S_AMP * math.sin(2 * math.pi * w) * (1 - math.cos(2 * math.pi * w)) / 2
            e = 1e-4
            f2 = S_AMP * math.sin(2 * math.pi * (w + e)) * (1 - math.cos(2 * math.pi * (w + e))) / 2
            slope = (f2 - f) / (e * 2 * H)
            off = x * uy - y * ux
            if -0.02 <= w <= 1.02:
                out.append(((off - f) / math.sqrt(1 + slope * slope), w))
        corners = []
    else:  # channels: three straight channels through the centre, square to the edges, and a centre ring
        for k in range(3):
            a = math.radians(60 * k + 30)
            ux, uy = math.cos(a), math.sin(a)
            out.append((x * uy - y * ux, (x * ux + y * uy + H) / (2 * H)))
        out.append((math.hypot(x, y) - 0.34, 0.5))
        corners = []
    for cx, cy in corners:
        r = math.hypot(x - cx, y - cy)
        ang = math.atan2(y - cy, x - cx)
        base = math.atan2(-cy, -cx)
        da = (ang - base + math.pi) % (2 * math.pi) - math.pi
        out.append((r - ARC_R, (da + math.pi / 3) / (2 * math.pi / 3)))
    return out


def studs(x, y, pattern):
    """Gold studs centred on lattice vertices (radially symmetric, so the three hexes' wedges join)."""
    if pattern == 'swirl':
        r = math.hypot(x, y)
        if r < 0.36:
            th = math.atan2(y, x)
            # a two-turn Archimedean spiral, r = 0.045 + 0.05 * phi, phi in [0, 4 pi] (sense matches the arms' curl)
            best = 9.0
            for kk in range(-1, 3):
                phi = (-th) % (2 * math.pi) + 2 * math.pi * kk
                if 0 <= phi <= 4 * math.pi + 0.6:
                    best = min(best, abs(r - (0.045 + 0.022 * phi)))
            return ('spiral', best, r)
        return None
    if pattern == 'palace':
        r = math.hypot(x, y)
        if r < 0.34:
            return ('medallion', r)
        return None
    if pattern != 'rings':
        return None
    for k in (1, 3, 5):
        cx, cy = CORNERS[k]
        r = math.hypot(x - cx, y - cy)
        if r < 0.17:
            return r / 0.17
    return None


def build(seed=7, pattern='rings', nseeds=13):
    rnd = random.Random(seed)
    seeds = []
    while len(seeds) < nseeds:
        x, y = rnd.uniform(-1, 1), rnd.uniform(-H, H)
        if inside(x, y) and all(math.hypot(x - a, y - b) > 0.36 for a, b, _ in seeds):
            seeds.append((x, y, len(seeds)))
    pts = [(x + dx, y + dy, i) for x, y, i in seeds for dx, dy in LATTICE]
    glowing = {tuple(sorted((a, b))) for a in range(nseeds) for b in range(nseeds) if a < b and rnd.random() < 0.40}
    img = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    gold = Image.new('L', (N, N), 0)
    chan = Image.new('L', (N, N), 0)
    crack = Image.new('L', (N, N), 0)
    along_im = Image.new('L', (N, N), 0)       # 1..255: position along a channel (edge midpoint to opposite one)
    ip, gp, cp, kp, ap = img.load(), gold.load(), chan.load(), crack.load(), along_im.load()
    lx, ly = -0.6, -0.8
    for py in range(N):
        for px in range(N):
            x, y = to_hex(px, py)
            if not inside(x, y, BLEED):
                continue
            # --- stone
            best = sorted(((x - a) ** 2 + (y - b) ** 2, a, b, i) for a, b, i in pts)[:2]
            d1, sx, sy, i1 = best[0]
            d2, _, _, i2 = best[1]
            e = math.sqrt(d2) - math.sqrt(d1)
            col = STONE[i1 % len(STONE)]
            vx, vy = x - sx, y - sy
            n = math.hypot(vx, vy) or 1
            lit = (vx * lx + vy * ly) / n
            h = (hash((px * 7919) ^ (py * 104729)) % 13) - 6
            k = 1.0
            if e < 0.07:
                k += 0.22 * lit * (1 - e / 0.07)
            c = tuple(max(0, min(255, int(v * k + h))) for v in col)
            glow = tuple(sorted((i1, i2))) in glowing
            if e < (0.034 if glow else 0.022):
                c = MORTAR
                if glow:
                    c = EMBER[2] if e < 0.012 else EMBER[1] if e < 0.024 else EMBER[0]
                    kp[px, py] = 255 if e < 0.024 else 140
            elif e < 0.05 and glow:
                c = tuple(int(c[j] * 0.6 + EMBER[0][j] * 0.4) for j in range(3))
            # --- bands (pattern-dependent; every band meets the edges at midpoints, square, symmetric profile)
            bands = band_dists(x, y, pattern)
            for dd, along in bands:
                if abs(dd) <= BAND_W * 1.25 and abs(dd) > BAND_W:
                    c = tuple(int(v * 0.45) for v in c)     # cast shadow either side (symmetric)
            for dd, along in bands:
                if abs(dd) <= BAND_W:
                    s = dd / BAND_W
                    c = band_profile(s, max(0.0, min(1.0, along)))
                    gp[px, py] = 255
                    if abs(s) < 0.22:
                        cp[px, py] = 255
                        ap[px, py] = 1 + int(254 * max(0.0, min(1.0, along)))
            st = studs(x, y, pattern)
            if isinstance(st, tuple) and st[0] == 'spiral':
                d, rr = st[1], st[2]
                hw = BAND_W * 0.8
                if d <= hw * 1.25 and d > hw and rr > 0.05:
                    c = tuple(int(v * 0.45) for v in c)
                elif d <= hw:
                    c = band_profile(d / hw, 0.5)
                    gp[px, py] = 255
                    if d / hw < 0.22:
                        cp[px, py] = 255
                if rr < 0.05:
                    c = EMBER[2]
                    kp[px, py] = 255
                st = None
            if isinstance(st, tuple):
                r = st[1]
                ap[px, py] = 0                  # the medallion is not part of a channel
                if r < 0.075:
                    c = EMBER[2] if r < 0.04 else EMBER[1]
                    kp[px, py] = 255
                elif r < 0.10:
                    c = GOLD_EDGE
                elif r < 0.155:
                    c = GOLD[3] if r < 0.125 else GOLD[2]
                    gp[px, py] = 255
                elif r < 0.19:
                    c = (24, 14, 10)            # the dark field inside the ring
                elif r < 0.31:
                    ss = (r - 0.25) / 0.06
                    c = band_profile(ss, 0.5)
                    gp[px, py] = 255
                    if abs(ss) < 0.22:
                        cp[px, py] = 255
                        ap[px, py] = 0
                else:
                    c = GOLD_EDGE
                st = None
            if st is not None:
                c = GOLD_EDGE if st > 0.82 else GOLD[2] if st > 0.45 else GOLD[4] if st < 0.2 else GOLD[3]
                gp[px, py] = 255
            ip[px, py] = c + (255,)
    # cut to the exact hex (corner to corner), so stretched tiles butt with no gap
    m = Image.new('L', (N, N), 0)
    mp = m.load()
    for py in range(N):
        for px in range(N):
            if inside(*to_hex(px, py), BLEED):
                mp[px, py] = 255
    img.putalpha(m)
    return img, gold, chan, crack, m, along_im


def export(path, size=256, pattern='rings'):
    img, gold, chan, crack, m, _ = build(pattern=pattern)
    small = img.convert('RGBa').resize((size, size), Image.BOX).convert('RGBA')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    small.save(path, lossless=True, method=6)
    return img


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    import sys
    pat = sys.argv[1] if len(sys.argv) > 1 else 'rings'
    p = os.path.join(here, 'exports', f'tile_sbk_domain_v3_{pat}.webp')
    export(p, pattern=pat)
    print('wrote', p, os.path.getsize(p))
