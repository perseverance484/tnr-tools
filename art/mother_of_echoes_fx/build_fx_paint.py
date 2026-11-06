#!/usr/bin/env python3
"""Painted payoffs and lingering ground (director, 2026-11-05: "We can paint a picture or tell a story with these ...
the ground as it would appear in full because of the ability being used. We don't need to mark each hex as unsafe
toxic bubbles or use circles"; docs/design/MOTHER_OF_ECHOES_ART.md "Art direction: omens, payoffs, lingering ground").

    python3 art/mother_of_echoes_fx/build_fx_paint.py --out DIR [--spec SPEC_JSON]

Demo pair for the director's direction check (before everything is redone):
- PAYOFF: Recast: Seam as one picture over its whole remembered region, sliced per hex on the engine's geometry
  (build_fx_mosaic.Canvas): the lattice she drew is redrawn white-gold top to bottom in the order she cut it, it HOLDS,
  one pale frame, glass blades stand up along the scores, the Remainder's black cracks race up them, the region
  shatters as one, chunks fall. anim_moe_recast_seam_p{col}_{row}_a8.
- LINGERING GROUND: the floor after a Recast, as one continuous surface: smoked, shattered etched glass (black cracks
  running across hex edges, the gold scores dimmed and broken, glass chips), no bubbles, no circles, static. One tile
  whose pattern repeats with the hex grid's own period (column pitch 0.75 hexSize, odd columns half a row lower, row
  pitch one tile height), so every hex of the area shows the same asset and the surface runs on without seams:
  tile_moe_recast_floor_a8.
"""
import argparse
import importlib.util
import json
import math
import os
import random

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("build_fx_mosaic", os.path.join(HERE, "build_fx_mosaic.py"))
MZ = importlib.util.module_from_spec(_s)
_s.loader.exec_module(MZ)
A4, A, F = MZ.A4, MZ.A, MZ.F
P2 = A.PAL["II"]
WHITE, SCORE = F.WHITE, F.SCORE
GOLD_HOT, GOLD, GOLD_DIM = F.ETCH_HOT, F.ETCH_MID, F.ETCH_DIM
CRACK = P2["vein"]            # the Remainder's crack (creeping in)
SMOKE = P2["smoke"]
GLASS_L, GLASS_B = A.PAL["I"]["lite"], A.PAL["I"]["body"]


# ------------------------------------------------------------------------------------------------ geometry helpers
def hex_poly(cx, cy, w=40, h=20):
    return [(cx - w / 2, cy), (cx - w / 4, cy - h / 2), (cx + w / 4, cy - h / 2), (cx + w / 2, cy),
            (cx + w / 4, cy + h / 2), (cx - w / 4, cy + h / 2)]


def cluster(f, x, y, col, out):
    """A4.cluster for a canvas of any size (QA X2: A4.cluster draws on a 50 px frame composited at (0, 0), so on a
    region canvas every chunk beyond it was lost). A 3 px blob outlined 1 px, drawn on a local 9 x 9 patch."""
    x, y = int(round(x)), int(round(y))
    n = Image.new("RGBA", (9, 9), (0, 0, 0, 0))
    F.blob(n, 4, 4, col, r=1)
    F.outline_alpha(n, out)
    f.alpha_composite(n, (x - 4, y - 4)) if 0 <= x - 4 and 0 <= y - 4 and x + 5 <= f.width and y + 5 <= f.height else \
        _paste_clipped(f, n, x - 4, y - 4)


def _paste_clipped(f, n, ox, oy):
    box = (max(0, -ox), max(0, -oy), min(n.width, f.width - ox), min(n.height, f.height - oy))
    if box[0] < box[2] and box[1] < box[3]:
        f.alpha_composite(n.crop(box), (ox + box[0], oy + box[1]))


def region_mask(cv):
    m = Image.new("L", (cv.w, cv.h), 0)
    d = ImageDraw.Draw(m)
    for k in cv.cells:
        d.polygon(hex_poly(*cv.c(*k), 40, 20), fill=255)    # the footprint; PIL fills the boundary, so neighbours meet (QA S5, nit)
    return m


def masked(f, m):
    out = Image.new("RGBA", f.size, (0, 0, 0, 0))
    out.paste(f, (0, 0), m)
    return out


# ------------------------------------------------------------------------------------------------ the payoff
STEEL_L, STEEL_S = (222, 226, 236), (91, 103, 134)   # pale steel glass (no safe-cyan fill; QA S7, bible 5.1 revision)


def dither_keep(f, keep):
    """Fade a frame with the ordered dither (hard alpha): keep < 1 drops pixels by the Bayer threshold."""
    if keep >= 1:
        return f
    px = f.load()
    for y in range(f.height):
        for x in range(f.width):
            if px[x, y][3] and F.BAYER[y % 4][x % 4] >= keep * 16:
                px[x, y] = (0, 0, 0, 0)
    return f


def recast_region(cells, frames=24, seed=7):
    """One Recast as one picture over its whole region (QA B6: not a per-hex stamp), sliced exactly (BATTLEFIELD).
    Remember (SAYO_BIBLE.md 2.2): the return replays the original shape first, in the same place. The Etching's lattice
    is ONE floor plan across the hall (etch_tile: verticals every 15 px at x = 7.5 mod 15, rows every 10 px at
    y = 5 mod 10), so the Recast redraws exactly that lattice, cell for cell, over its own mark.
    0-5 the plan is redrawn white-gold top to bottom over the mark, scribe sparks on the front (slow: 3 rows a frame);
    6-8 HOLD hot (three identical frames: skew-safe); 9-12 the plan's cells stand up out of the floor as panes of pale
    glass, scored gold, lit top-left, each showing its thickness; 13-14 the Remainder's black cracks race up them;
    15-18 they shatter along the scores, pieces thrown and falling; 19-23 it settles: the lattice dims to the recast
    floor's broken gold and black and dissolves (dither) onto the floor tile under it."""
    cv = MZ.Canvas(cells)
    rm = region_mask(cv)
    x0, y0, x1, y1 = rm.getbbox()
    rnd = random.Random(seed)
    hs = [y for y in range(y0 - 10, y1 + 10) if y % 10 == 5]
    vs = [x for x in range(x0 - 15, x1 + 15) if x % 15 == 7]
    panes = []                                               # the plan's own cells, the ones whose middle is ours
    for y in hs:
        for x in vs:
            mx, my = x + 7, y + 5
            if 0 <= mx < cv.w and 0 <= my < cv.h and rm.getpixel((mx, my)) and rnd.random() < 0.5:
                panes.append((x, y, rnd.uniform(0.75, 1.0), rnd.random(), rnd.choice((-1, 1))))

    def lattice(f, col, width, ycut=None, keep=1.0, crack=False):
        lat = cv.frame()
        d = ImageDraw.Draw(lat)
        yc = y1 if ycut is None else ycut
        for k, y in enumerate(hs):
            if y > yc:
                continue
            d.line([(x0 - 2, y + width), (x1 + 2, y + width)], fill=(*SCORE, 255))
            d.line([(x0 - 2, y), (x1 + 2, y)], fill=(*col, 255), width=width)
            if crack:
                for x in vs[k % 3::3]:
                    d.line([(x + 3, y - 1), (x + 10, y + 2)], fill=(*CRACK, 255), width=2)
        for x in vs:
            d.line([(x + width, y0 - 2), (x + width, min(yc, y1 + 2))], fill=(*SCORE, 255))
            d.line([(x, y0 - 2), (x, min(yc, y1 + 2))], fill=(*col, 255), width=width)
        f.alpha_composite(dither_keep(masked(lat, rm), keep))

    def slab(f, x, y, lift, k_crack, flip):
        """One cell standing up: its face lifted `lift` px, the thickness showing below it, lit top-left."""
        n = cv.frame()
        d = ImageDraw.Draw(n)
        fx0, fx1, fy0, fy1 = x + 2, x + 14, y + 2 - lift, y + 9 - lift
        d.rectangle([fx0, fy1, fx1, y + 9], fill=(*STEEL_S, 255))              # the pane's thickness
        d.rectangle([fx0, fy0, fx1, fy1], fill=(*STEEL_L, 255))                # its face
        d.line([(fx0, fy0), (fx1, fy0)], fill=(*WHITE, 255))
        d.line([(fx0, fy0), (fx0, fy1)], fill=(*WHITE, 255))
        d.line([(fx0 + 1, (fy0 + fy1) // 2), (fx1 - 1, (fy0 + fy1) // 2)], fill=(*GOLD, 255))   # its score
        if k_crack > 0:
            cx_ = fx0 + 6 + 2 * flip
            d.line([(cx_, fy1), (cx_ - 2 * flip, fy1 - (fy1 - fy0) * min(1, k_crack))], fill=(*CRACK, 255), width=2)
        F.outline_alpha(n, SCORE)
        f.alpha_composite(masked(n, rm))

    out = []
    for i in range(frames):
        f = cv.frame()
        if i < 6:
            ycut = y0 + (y1 - y0) * (i + 1) / 6
            lattice(f, GOLD_HOT, 2, ycut)                    # brighter and wider than the mark it redraws
            for x in vs:
                if x0 <= x <= x1:
                    A4.star(f, x, ycut, WHITE, 2)
        elif i < 9:                                          # the HOLD: three identical frames
            lattice(f, GOLD_HOT, 2)
            for x in vs[1::2]:
                for y in hs[1::2]:
                    if rm.getpixel((max(0, min(cv.w - 1, x)), max(0, min(cv.h - 1, y)))):
                        A4.star(f, x, y, WHITE, 2)
        elif i < 15:                                         # the cells stand up; the Remainder's cracks race up them
            v = i - 9
            lattice(f, GOLD, 1, crack=v >= 4)
            for (x, y, hk, ph, flip) in sorted(panes, key=lambda p: p[1]):
                lift = round(6 * hk * min(1.0, (v + 1 - ph) / 3)) if v + 1 > ph else 0
                if lift > 0:
                    slab(f, x, y, lift, (v - 3) / 2 if v >= 4 else 0, flip)
        elif i < 19:                                         # they shatter along the scores
            u = i - 14
            lattice(f, GOLD_DIM, 1, crack=True)
            for (x, y, hk, ph, flip) in panes:
                top = y + 2 - round(6 * hk)
                for j, (dx, col) in enumerate(((-1, STEEL_L), (1, STEEL_S), (0, CRACK))):
                    px_ = x + 8 + dx * (3 + 1.6 * u) + flip
                    py_ = top + 2 + 3 * j - 2.2 * u + 0.6 * u * u
                    if py_ < y + 12 and (j < 2 or u < 3):
                        cluster(f, px_, py_, col, SCORE)
            f = masked(f, rm)
        else:                                                # settle onto the floor: dim, then dissolve
            keep = 1.0 - (i - 18) / 5
            lattice(f, GOLD_DIM, 1, keep=keep, crack=True)
        out.append(f)
    return cv, out


def recast_regions(spec_path, only=None):
    """Every Recast region in the spec, painted and sliced: {name: {(col, row): frames}}."""
    spec = json.load(open(spec_path))
    out = {}
    for j in spec["jutsu"]:
        r = j["record"]
        if r["name"].startswith("Recast:") and (only is None or r["name"].split(": ")[1].lower() in only):
            cells = [(c["longitude"], c["latitude"]) for c in r["coordinateTargeting"]["coordinates"]]
            cv, fr = recast_region(cells, seed=sum(map(ord, r["name"])))
            out[r["name"].split(": ")[1].lower()] = cv.slices(fr)
    return out


# ------------------------------------------------------------------------------------------------ Glassfall (S9)
R3 = dict(deep=(8, 10, 15), body=(18, 23, 30), lit=(39, 50, 60), frame=(20, 42, 51), vdim=(47, 92, 106),
          vlit=(146, 182, 191), hot=(200, 250, 255), void=(16, 8, 30), bone=(235, 236, 235))   # SAYO_BIBLE.md 5.1, Act III
EMB = dict(deep=(92, 30, 18), red=(214, 58, 26), yel=(255, 206, 84))                        # ember: heavy only


def glassfall_region(cells, frames=27, seed=11):
    """Glassfall: ONE thorned black pane, the size of the hall, falls point first; the third it lands on shows it
    (SAYO_BIBLE.md 3.4). The pane is drawn at the scale of the whole field, so every hex of the third carries an aligned
    piece of the same picture: its lozenge frame bars, one diagonal sheen, and cracks radiating from ONE point of fall.
    0-4 the shadow grows and the frame's shadow sharpens as the pane nears; 5 it arrives point first (white at the
    point); 6 the flash; 7-9 HOLD (identical frames: skew-safe); 10-14 the cracks run out from the point of fall as one
    wave across the hall; 15-19 the pane gives way: its pieces part and fall over the void; 20-25 it settles onto the
    Act III floor: the cracks freeze to teal and dissolve (dither) onto the floor tile under it."""
    cv = MZ.Canvas(cells)
    rm = region_mask(cv)
    rnd = random.Random(seed)
    pts = [(x, y) for y in range(cv.h) for x in range(cv.w) if rm.getpixel((x, y))]
    xs = [cv.c(*k)[0] for k in cells]; ys = [cv.c(*k)[1] for k in cells]
    aim = (min(xs) + (max(xs) - min(xs)) * rnd.uniform(0.38, 0.62), min(ys) + (max(ys) - min(ys)) * rnd.uniform(0.3, 0.5))
    imp = min((cv.c(*k) for k in cells), key=lambda c: math.hypot(c[0] - aim[0], c[1] - aim[1]))   # on a hex of the third
    dmax = max(math.hypot(x - imp[0], 2 * (y - imp[1])) for x, y in pts)
    PER, NS = 54, 13                                         # lozenge frame period; radial crack count
    rays = sorted(rnd.uniform(0, 2 * math.pi) for _ in range(NS))

    def bar(x, y, ox=0, oy=0):
        u, v = (x - ox) - 1.6 * (y - oy), (x - ox) + 1.6 * (y - oy)
        du, dv = u % PER, v % PER
        return min(du, PER - du) < 1.3 or min(dv, PER - dv) < 1.3, min(du, PER - du) < 2.6 or min(dv, PER - dv) < 2.6

    def sheen(x, y):
        s_ = ((0.55 * x + y) % 96) / 96
        return s_ < 0.16, abs(s_ - 0.16) < 0.012

    def crack(x, y):
        a_ = math.atan2(2 * (y - imp[1]), x - imp[0]) % (2 * math.pi)
        d_ = math.hypot(x - imp[0], 2 * (y - imp[1]))
        for k, r in enumerate(rays):
            wob = 0.035 * math.sin(d_ / 9 + k)
            da = (a_ - r - wob + math.pi) % (2 * math.pi) - math.pi
            if abs(da) * d_ < 0.8:
                return True, d_ / dmax
        return False, d_ / dmax

    info = {}
    for x, y in pts:
        b_core, b_wide = bar(x, y)
        s_lit, s_edge = sheen(x, y)
        c_on, d = crack(x, y)
        a_ = math.atan2(2 * (y - imp[1]), x - imp[0]) % (2 * math.pi)
        sector = sum(1 for r in rays if r < a_) % NS
        piece = (int(((x - 1.6 * y) // PER)), int(((x + 1.6 * y) // PER)), sector)
        info[(x, y)] = (b_core, b_wide, s_lit, s_edge, c_on, d, piece)
    thorn = [p for p, v in info.items() if v[0] and (p[0] * 3 + p[1]) % 9 == 0]
    rim = {p for p in info if any(not rm.getpixel((min(cv.w - 1, max(0, p[0] + dx)), min(cv.h - 1, max(0, p[1] + dy))))
                                  for dx, dy in ((2, 0), (0, 1), (-2, 0), (0, -1)))}
    cen = {}
    for p, v in info.items():
        cen.setdefault(v[6], []).append(p)
    cen = {k: (sum(q[0] for q in v) / len(v), sum(q[1] for q in v) / len(v)) for k, v in cen.items()}

    def pane_col(p, hot):
        b_core, b_wide, s_lit, s_edge, c_on, d, _ = info[p]
        if b_core:
            return R3["hot"] if hot == 2 else R3["vlit"] if hot else R3["frame"]
        if b_wide:
            return R3["frame"] if not hot else R3["vdim"]
        if s_edge:
            return R3["vlit"]
        return R3["lit"] if s_lit else R3["body"]

    def pane(f, hot=0, rim_col=None):
        px = f.load()
        for p in info:
            px[p] = (*pane_col(p, hot), 255)
        if rim_col:
            for p in rim:
                if (p[0] + p[1]) % 2 == 0 or rim_col == WHITE:
                    px[p] = (*rim_col, 255)
        for (x, y) in thorn:
            for t in range(1, 4):
                F.px(f, x, y - t, R3["deep"] if t < 3 else R3["vdim"])

    body = set()                                             # QA S4: the LPC body on each hex of the third
    for k in cells:
        bx, by = cv.c(*k)
        for y in range(int(by) - 16, int(by) + 6):
            for x in range(int(bx) - 6, int(bx) + 7):
                body.add((x, y))

    out = []
    for i in range(frames):
        f = cv.frame()
        px = f.load()
        if i < 5:                                            # the PANE's shadow: a lozenge, growing and sharpening
            g = (i + 1) / 5
            A_ = dmax * (0.35 + 0.8 * g)                     # its half-diagonal: the pane nears, the shadow spreads
            off = (1 - g) * 8                                # the frame bars' shadow converges on the frame
            for p, v in info.items():
                px[p] = (*R3["body"], 255)                   # QA S1: the hall floor as it stands, covered; the break reveals
                q = abs(p[0] - imp[0]) / A_ + abs(2 * (p[1] - imp[1])) / (0.62 * A_)
                if q > 1:
                    continue
                if q > 1 - 0.035 * (1 + g):                  # the shadow's edge: light spilling round the pane
                    px[p] = (*(R3["vlit"] if g > 0.5 else R3["vdim"]), 255)
                elif q > 1 - 0.09:
                    px[p] = (*R3["deep"], 255)
                elif bar(p[0], p[1], off, off * 0.5)[1 if g < 0.6 else 0]:
                    px[p] = (*R3["deep"], 255)               # the frame's shadow
                elif F.BAYER[p[1] % 4][p[0] % 4] < (0.35 + 0.5 * g) * 16:
                    px[p] = (*R3["deep"], 255)               # the glass's shadow: dark, deepening
            if i >= 2:
                A4.star(f, imp[0], imp[1], R3["vlit"] if i < 4 else R3["hot"], i)
        elif i == 5:                                         # it arrives, point first
            pane(f, hot=1)
            A4.star(f, imp[0], imp[1], WHITE, 7)
        elif i < 8:                                          # the flash: two identical frames, no per-hex rim (QA S2)
            pane(f, hot=2)
            A4.star(f, imp[0], imp[1], WHITE, 9)
        elif i < 11:                                         # HOLD: three identical frames, rimmed in lit vein (QA S3)
            pane(f, hot=1, rim_col=R3["vlit"])
            A4.star(f, imp[0], imp[1], R3["hot"], 4)
        elif i < 16:                                         # the crack wave runs out from the point of fall
            u = (i - 10) / 5
            pane(f, hot=0)
            for p, v in info.items():
                if v[4] and v[5] < u:
                    px[p] = (*(R3["hot"] if v[5] > u - 0.18 else R3["vlit"]), 255)
                elif v[4] and v[5] < u + 0.05 and (p[0] + p[1]) % 2:
                    px[p] = (*WHITE, 255)
        elif i < 21:                                         # it gives way: the pieces part and fall over the void
            t = i - 15
            for p in info:
                if F.BAYER[p[1] % 4][p[0] % 4] < (0.6 - 0.09 * t) * 16:
                    px[p] = (*R3["void"], 255)
            lay = cv.frame(); lp = lay.load()
            keep = 1.0 - 0.13 * t
            for p, v in info.items():
                cx, cy = cen[v[6]]
                vx, vy = cx - imp[0], cy - imp[1]
                n = max(1.0, math.hypot(vx, vy))
                dx = vx / n * (1.5 * t)
                dy = vy / n * 0.7 * t - 2.0 * t + 0.42 * t * t
                q = (int(round(p[0] + dx)), int(round(p[1] + dy)))
                if 0 <= q[0] < cv.w and 0 <= q[1] < cv.h and F.BAYER[q[1] % 4][q[0] % 4] < keep * 16:
                    c = R3["vlit"] if v[4] and t < 3 else pane_col(p, 0)
                    lp[q] = (*c, 255)
            f.alpha_composite(lay)
            for k, (cx, cy) in list(cen.items())[::4]:
                F.px(f, cx + (hash(k) % 3 - 1) * t, cy - 2 * t + 0.5 * t * t, R3["hot"] if t < 3 else R3["vlit"])
        else:                                                # settle onto the Act III floor; the last frame is empty
            keep = 1.0 - (i - 20) / (frames - 21)
            for p, v in info.items():
                if v[4] and F.BAYER[p[1] % 4][p[0] % 4] < keep * 16:
                    px[p] = (*(R3["vlit"] if i < 23 else R3["vdim"]), 255)
                elif v[0] and F.BAYER[p[1] % 4][p[0] % 4] < keep * 0.5 * 16:
                    px[p] = (*R3["frame"], 255)
        if i < 16:                                           # QA S4: open the glass over the fighter's body
            for p in body:
                if p in info and F.BAYER[p[1] % 4][p[0] % 4] >= 0.45 * 16:
                    px[p] = (0, 0, 0, 0)
        out.append(masked(f, rm))
    return cv, out


def painted_regions(spec_path, prefix, painter, only=None):
    """Every region in the spec whose name starts with `prefix`, painted by `painter` and sliced: {name: slices}."""
    spec = json.load(open(spec_path))
    out = {}
    for j in spec["jutsu"]:
        r = j["record"]
        key = r["name"].split(": ")[-1].lower().replace(" ", "_")
        if r["name"].startswith(prefix) and (only is None or key in only):
            cells = [(c["longitude"], c["latitude"]) for c in r["coordinateTargeting"]["coordinates"]]
            cv, fr = painter(cells, seed=sum(map(ord, r["name"])))
            out[key] = cv.slices(fr)
    return out


# ------------------------------------------------------------------------------------------------ Shatterfall (S9)
SF_LEAD = 2                 # frames per rank: the crack runs out from her at 15 px a frame


def _crack(f, a, b, col, rnd, w=2):
    """A crack from a to b with one jittered knee; endpoints exact (they are the shared hex vertices)."""
    mx, my = (a[0] + b[0]) / 2 + rnd.uniform(-2, 2), (a[1] + b[1]) / 2 + rnd.uniform(-1.5, 1.5)
    d = ImageDraw.Draw(f)
    for p0, p1 in ((a, (mx, my)), ((mx, my), b)):
        d.line([(p0[0], p0[1] + 1), (p1[0], p1[1] + 1)], fill=(*SCORE, 255), width=w)
        d.line([p0, p1], fill=(*col, 255), width=w)


def shatterfall_piece(rank, seed, frames=26):
    """One hex of Shatterfall Gives Way (CASTER origin; S9). Her offsets are added to her column as written, so a hex's
    neighbours sit half a row up or down by HER column's parity: exact slices of one painting would tear on one parity.
    What joins in both parities: hex VERTICES. A hex's west vertex is always its west neighbour's upper-right or
    lower-right vertex, whichever parity she stands on. So each piece draws its crack centre -> west vertex AND forks
    centre -> upper-right and lower-right: the network is continuous from her outward in either parity (the unused fork
    reads as a branch). The approved burst (build_fx_a3.burst III, the director's reference wave) erupts on each hex as
    the crack passes; ranks fire SF_LEAD frames apart from her. The crack stays, dims, and dissolves onto the pool."""
    rnd = random.Random(seed)
    C, W, UR, LR = (25, 25), (5, 25), (35, 15), (35, 35)
    burst = A.burst("III", scale=1.1, wide=True)
    lead = (rank - 1) * SF_LEAD + 1
    flip = rnd.random() < 0.5
    out = []
    for i in range(frames):
        f = F.frame()
        t = i - lead
        if t >= 0:
            hot = R3["hot"] if t < 2 else R3["vlit"] if t < 9 else R3["vdim"]
            cr = F.frame()
            if t >= 0:
                _crack(cr, UR, C, hot, random.Random(seed + 1))
                _crack(cr, LR, C, hot, random.Random(seed + 2))
            if t >= 1:
                _crack(cr, C, W, hot, random.Random(seed + 3))
            keep = 1.0 if t < 12 else max(0.0, 1 - (t - 11) / 6)
            f.alpha_composite(dither_keep(cr, keep))
            if t == 0:
                A4.star(f, 30, 25, WHITE, 2)
            if t == 1:
                A4.star(f, 15, 25, WHITE, 3)
            b = t + 1                                           # the burst, from its anticipation frame
            if 0 <= b < len(burst):
                g = burst[b].transpose(Image.FLIP_LEFT_RIGHT) if flip else burst[b]
                f.alpha_composite(g)
        out.append(f)
    return out


def shatterfall_centre(frames=26):
    """Her own hex: the floor under her heats (ember ring), a teal-white flash at her feet, and the fan of cracks
    leaves her: to her west vertex (the vertex every west-side piece joins) and two short forks."""
    C = (25, 25)
    out = []
    for i in range(frames):
        f = F.frame()
        if i <= 1:
            F.ground_ring(f, F.GRX - 1, F.GRY - 0.5, [(0, EMB["yel"] if i else EMB["red"]), (1, SCORE)])
        if 1 <= i < 16:
            col = R3["hot"] if i < 4 else R3["vlit"] if i < 10 else R3["vdim"]
            cr = F.frame()
            _crack(cr, C, (5, 25), col, random.Random(5))
            _crack(cr, C, (15, 15), col, random.Random(6))
            _crack(cr, C, (15, 35), col, random.Random(7))
            f.alpha_composite(dither_keep(cr, 1.0 if i < 11 else max(0.0, 1 - (i - 10) / 6)))
        if i == 1:
            A4.star(f, 25, 25, WHITE, 5)
        out.append(f)
    return out



# ------------------------------------------------------------------------------------------------ the lingering surface
S = 4                     # draw at 4x the tile's own pixels so the lattice period is integral
V1 = (0, 50 * S)          # one row down
V2 = (int(37.5 * S), 25 * S)  # one column right (odd columns half a row lower)


def periodic(draw_cell, size=7):
    """Draw draw_cell(d, ox, oy) at every lattice translate over a canvas of size x size periods; return the canvas and
    the canvas point of a central lattice node."""
    W, H = V2[0] * size, V1[1] * size
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for a in range(-2, size + 2):
        for b in range(-2, size + 2):
            ox, oy = a * V2[0], b * V1[1] + (a % 2) * V2[1]
            draw_cell(d, ox, oy)
    c = (V2[0] * (size // 2), V1[1] * (size // 2) + ((size // 2) % 2) * V2[1])
    return im, c


def recast_floor(seed=11):
    """Smoked, shattered etched glass: one period of cracks, broken gold scores and chips, repeated on the hex lattice."""
    rnd = random.Random(seed)
    cracks = []
    for _ in range(4):                                       # cracks long enough to run across hex edges
        x, y = rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1])
        pts = [(x, y)]
        ang = rnd.uniform(0, 2 * math.pi)
        for _ in range(7):
            ang += rnd.uniform(-0.7, 0.7)
            x, y = x + 12 * S * 0.5 * math.cos(ang), y + 12 * S * 0.5 * math.sin(ang)
            pts.append((x, y))
        cracks.append(pts)
    scores = [(rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1]), rnd.choice("hv"), rnd.uniform(8, 16) * S) for _ in range(5)]
    chips = [(rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1]), rnd.choice((WHITE, GOLD_DIM, (222, 226, 236)))) for _ in range(6)]
    smoke = [(rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1]), rnd.uniform(7, 12) * S) for _ in range(3)]

    def base(d, ox, oy):
        for x, y, r in smoke:
            d.ellipse([ox + x - r, oy + y - r * 0.6, ox + x + r, oy + y + r * 0.6], fill=(*SMOKE, 255))

    def ink(d, ox, oy):
        for x, y, o, L in scores:                            # the scores, dimmed and broken
            if o == "h":
                d.line([(ox + x, oy + y), (ox + x + L, oy + y)], fill=(*GOLD_DIM, 255), width=S)
            else:
                d.line([(ox + x, oy + y), (ox + x, oy + y + L * 0.6)], fill=(*GOLD_DIM, 255), width=S)
        for pts in cracks:
            q = [(ox + x, oy + y) for x, y in pts]
            d.line(q, fill=(*CRACK, 255), width=2 * S)
            d.line([(x - S, y - S) for x, y in q], fill=(222, 226, 236, 255), width=S)  # the lit edge (upper left)
        for x, y, c in chips:
            d.rectangle([ox + x - S, oy + y - S, ox + x + S, oy + y + S], fill=(*c, 255))

    # the ground stain: a dark smoked glass field (the whole hex) so "don't stand here" reads on the light board
    big, c = periodic(lambda d, ox, oy: None)
    W, H = big.size
    ground = Image.new("RGBA", (W, H), (*P2["deep"], 255))
    lift, _ = periodic(lambda d, ox, oy: [d.line([(ox + x, oy + y) for x, y in pts], fill=(91, 103, 134, 255), width=4 * S)
                                           for pts in cracks])   # a lit sheen along every crack: reads on dark boards
    ground.alpha_composite(lift)
    sm, _ = periodic(base)
    ground.alpha_composite(sm)
    ik, _ = periodic(ink)
    ground.alpha_composite(ik)
    tile = ground.crop((c[0] - 25 * S, c[1] - 25 * S, c[0] + 25 * S, c[1] + 25 * S)).resize((50, 50), Image.NEAREST)
    m = Image.new("L", (50, 50), 0)
    ImageDraw.Draw(m).polygon(F.T_HEX, fill=255)
    t = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    t.paste(tile, (0, 0), m)
    return F.tile_out(t)


def mended_floor(seed=23):
    """No One Is Mended: the whole hall's floor stilled. Black Remainder glass with frost lying in it (the Silence's
    frozen dust) and the teal veins frozen mid-crack; nothing moves, nothing heals. Same lattice-periodic tile."""
    rnd = random.Random(seed)
    P3 = A.PAL["III"]
    veins = []
    for _ in range(3):
        x, y = rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1])
        pts = [(x, y)]
        ang = rnd.uniform(0, 2 * math.pi)
        for _ in range(8):
            ang += rnd.uniform(-0.9, 0.9)
            x, y = x + 6 * S * math.cos(ang), y + 6 * S * math.sin(ang)
            pts.append((x, y))
        veins.append(pts)
    frost = [(rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1]), rnd.uniform(4, 9) * S) for _ in range(5)]
    dust = [(rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1])) for _ in range(7)]

    def body(d, ox, oy):
        for x, y, r in frost:                                 # frost lying in the glass: pale, matte, irregular
            d.ellipse([ox + x - r, oy + y - r * 0.55, ox + x + r, oy + y + r * 0.55], fill=(*P3["lite"], 255))
            d.ellipse([ox + x - r * 0.6, oy + y - r * 0.3, ox + x + r * 0.5, oy + y + r * 0.3], fill=(70, 84, 98, 255))

    def lines(d, ox, oy):
        for pts in veins:
            q = [(ox + x, oy + y) for x, y in pts]
            d.line(q, fill=(*P3["frame"], 255), width=4 * S)
            d.line(q, fill=(*P3["vein"], 255), width=S)
        for x, y in dust:
            d.rectangle([ox + x - S, oy + y - S, ox + x + S, oy + y + S], fill=(206, 210, 222, 255))

    big, c = periodic(lambda d, ox, oy: None)
    ground = Image.new("RGBA", big.size, (*P3["body"], 255))
    for fn in (body, lines):
        layer, _ = periodic(fn)
        ground.alpha_composite(layer)
    tile = ground.crop((c[0] - 25 * S, c[1] - 25 * S, c[0] + 25 * S, c[1] + 25 * S)).resize((50, 50), Image.NEAREST)
    m = Image.new("L", (50, 50), 0)
    ImageDraw.Draw(m).polygon(F.T_HEX, fill=255)
    t = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    t.paste(tile, (0, 0), m)
    return F.tile_out(t)


def _veined_tile(seed, ground, crack_dark, crack_lit, flecks, frost=None, nveins=4, step=6, wdark=3, lit_w=1):
    """A lattice-periodic floor: ground colour, optional matte frost patches, crack network (dark body + lit core),
    2-3 px flecks. One period, repeated on the hex lattice (seamless across hexes)."""
    rnd = random.Random(seed)
    veins = []
    for _ in range(nveins):
        x, y = rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1])
        pts = [(x, y)]
        ang = rnd.uniform(0, 2 * math.pi)
        for _ in range(8):
            ang += rnd.uniform(-0.8, 0.8)
            x, y = x + step * S * math.cos(ang), y + step * S * math.sin(ang)
            pts.append((x, y))
        veins.append(pts)
    pts_f = [(rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1]), rnd.choice(flecks)) for _ in range(7)]
    patches = [(rnd.uniform(0, V2[0]), rnd.uniform(0, V1[1]), rnd.uniform(5, 10) * S) for _ in range(4)] if frost else []

    def body(d, ox, oy):
        for x, y, r in patches:
            d.ellipse([ox + x - r, oy + y - r * 0.55, ox + x + r, oy + y + r * 0.55], fill=(*frost[0], 255))
            d.ellipse([ox + x - r * 0.55, oy + y - r * 0.3, ox + x + r * 0.45, oy + y + r * 0.28], fill=(*frost[1], 255))

    def lines(d, ox, oy):
        for pts in veins:
            q = [(ox + x, oy + y) for x, y in pts]
            d.line(q, fill=(*crack_dark, 255), width=wdark * S)
            d.line(q, fill=(*crack_lit, 255), width=lit_w * S)
        for x, y, c in pts_f:
            d.rectangle([ox + x - S, oy + y - S, ox + x + S, oy + y + S], fill=(*c, 255))

    big, c = periodic(lambda d, ox, oy: None)
    g = Image.new("RGBA", big.size, (*ground, 255))
    for fn in (body, lines):
        layer, _ = periodic(fn)
        g.alpha_composite(layer)
    tile = g.crop((c[0] - 25 * S, c[1] - 25 * S, c[0] + 25 * S, c[1] + 25 * S)).resize((50, 50), Image.NEAREST)
    m = Image.new("L", (50, 50), 0)
    ImageDraw.Draw(m).polygon(F.T_HEX, fill=255)
    t = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    t.paste(tile, (0, 0), m)
    return F.tile_out(t)


def floor_i():
    """Sayo, Act I: crazed white glass where the line broke; hairline cracks in gunmetal with white-gold lit cores,
    a few prismatic glints. Bright on the dark board; the gunmetal network carries it on the light one."""
    return _veined_tile(31, (176, 184, 200), (35, 34, 49), (255, 255, 250), [(255, 170, 170), (190, 180, 255), (255, 238, 196)],
                        frost=((214, 220, 232), (236, 240, 246)), nveins=5, step=5, wdark=3)


def floor_silence():
    """The Silence (the Hush, An Absence): matte ink that reflects nothing, frost lying in it, teal only in the veins."""
    return _veined_tile(41, (14, 12, 18), (39, 50, 60), (47, 92, 106), [(206, 210, 222), (206, 210, 222)],
                        frost=((70, 84, 98), (150, 160, 174)), nveins=3, step=6, wdark=2)


def floor_iii():
    """Sayo, Act III (the Remainder): blackened obsidian, teal cracks frozen mid-run, bone flecks."""
    return _veined_tile(53, (18, 23, 30), (20, 42, 51), (146, 182, 191), [(235, 236, 235), (170, 172, 176)],
                        nveins=4, step=6, wdark=4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cells", default="seam", help="seam: Recast: Seam's region (columns 0-3, every row)")
    ap.add_argument("--spec", help="QA B6: paint every Recast region in this spec (anim_moe_recast_<region>_p<col>_<row>_a13)")
    ap.add_argument("--shatterfall", action="store_true", help="with --spec: Shatterfall Gives Way pieces (CASTER)")
    ap.add_argument("--glassfall", action="store_true", help="with --spec: paint every Glassfall pane instead")
    ap.add_argument("--regions", default="", help="with --spec: a comma list of region names (default: all)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.spec and a.shatterfall:
        spec = json.load(open(a.spec))
        rec = next(j["record"] for j in spec["jutsu"] if j["record"]["name"] == "Shatterfall Gives Way")
        rows = []
        name = "anim_moe_shatterfall_c_a13.webp"
        F.strip(shatterfall_centre()).save(os.path.join(a.out, name), lossless=True, quality=100, method=6)
        rows.append({"file": name, "region": "shatterfall", "dx": 0, "dy": 0, "rank": 0, "frames": 26})
        for c in rec["coordinateTargeting"]["coordinates"]:
            dx, dy = c["longitude"], c["latitude"]
            name = f"anim_moe_shatterfall_{-dx}_{dy + 5}_a13.webp"
            F.strip(shatterfall_piece(abs(dx), seed=100 * dx + dy)).save(os.path.join(a.out, name), lossless=True, quality=100, method=6)
            rows.append({"file": name, "region": "shatterfall", "dx": dx, "dy": dy, "rank": abs(dx), "frames": 26})
        json.dump({"slices": rows}, open(os.path.join(a.out, "moe_fx_shatterfall.json"), "w"), indent=1)
        print(len(rows), "Shatterfall pieces")
        return
    if a.spec and a.glassfall:
        only = set(a.regions.split(",")) if a.regions else None
        rows = []
        for region, sl_ in painted_regions(a.spec, "Glassfall:", glassfall_region, only).items():
            for (col, row), sl in sorted(sl_.items()):
                name = f"anim_moe_glassfall_{region}_p{col}_{row}_a13.webp"
                F.strip(sl).save(os.path.join(a.out, name), lossless=True, quality=100, method=6)
                rows.append({"file": name, "region": region, "col": col, "row": row, "frames": len(sl)})
        json.dump({"slices": rows}, open(os.path.join(a.out, f"moe_fx_glassfall_{a.regions or 'all'}.json"), "w"), indent=1)
        print(len(rows), "Glassfall slices")
        return
    if a.spec:
        only = set(a.regions.split(",")) if a.regions else None
        rows = []
        for region, sl_ in recast_regions(a.spec, only).items():
            for (col, row), sl in sorted(sl_.items()):
                name = f"anim_moe_recast_{region}_p{col}_{row}_a13.webp"
                F.strip(sl).save(os.path.join(a.out, name), lossless=True, quality=100, method=6)
                rows.append({"file": name, "region": region, "col": col, "row": row, "frames": len(sl)})
        json.dump({"slices": rows}, open(os.path.join(a.out, f"moe_fx_recast_{a.regions or 'all'}.json"), "w"), indent=1)
        print(len(rows), "Recast slices")
        return
    cells = [(c, r) for c in range(4) for r in range(10)]
    cv, fr = recast_region(cells)
    rows = []
    for (col, row), sl in sorted(cv.slices(fr).items()):
        name = f"anim_moe_recast_seam_p{col}_{row}_a8.webp"
        F.strip(sl).save(os.path.join(a.out, name), lossless=True, quality=100, method=6)
        rows.append({"file": name, "col": col, "row": row, "frames": len(sl)})
    recast_floor().save(os.path.join(a.out, "tile_moe_recast_floor_a8.webp"), lossless=True, quality=100, method=6)
    mended_floor().save(os.path.join(a.out, "tile_moe_mended_floor_a8.webp"), lossless=True, quality=100, method=6)
    for name, fn in (("tile_moe_floor_i_a8.webp", floor_i), ("tile_moe_floor_silence_a8.webp", floor_silence),
                     ("tile_moe_floor_iii_a8.webp", floor_iii)):
        fn().save(os.path.join(a.out, name), lossless=True, quality=100, method=6)
    json.dump({"slices": rows}, open(os.path.join(a.out, "moe_fx_paint.json"), "w"), indent=1)
    print(len(rows), "slices + 1 tile")


if __name__ == "__main__":
    main()


# ------------------------------------------------------------------------------------------------ periodic slices
# One slice for every hex of any region: the composition is lattice-periodic (column pitch 30, row pitch 20, odd
# columns 10 lower, in clip pixels), so the slice of one hex is the slice of every hex, and neighbours join seamlessly.
# The wave comes from row bands: band k leads k * BAND_LEAD frames (the order she cut it, top to bottom). Shared by
# every Etching and every Recast, whatever the region's shape (10 strips each instead of one per hex).
BAND_LEAD = 1
N_BANDS = 10
CELL = [(c, r) for c in range(-2, 3) for r in range(-2, 3)]


def periodic_slice(draw):
    """draw(f, cx, cy, i) paints frame i of one cell's content around (cx, cy); returns the central hex's slice."""
    cv = MZ.Canvas(CELL)
    frames = []
    for i in range(draw.frames):
        f = cv.frame()
        for k in CELL:
            draw(f, *cv.c(*k), i)
        frames.append(f)
    return cv.slices(frames)[(0, 0)]


def _recast_cell(f, cx, cy, i):
    hot = 6 <= i < 8
    if i < 9:                                                    # the lattice redrawn: rows every 10, columns every 15
        u = min(1.0, (i + 1) / 6)
        col = WHITE if i == 8 else (GOLD_HOT if hot else GOLD)
        for dy in (-5, 5):
            x0 = cx - 15
            F.seg(f, (x0, cy + dy + 1), (x0 + 30 * u, cy + dy + 1), SCORE)
            F.seg(f, (x0, cy + dy), (x0 + 30 * u, cy + dy), col)
        for dx in (-7.5, 7.5):
            if dx < 0 or i >= 3:                                 # a doorway: one wall comes later
                F.seg(f, (cx + dx + 1, cy - 10), (cx + dx + 1, cy - 10 + 20 * u), SCORE)
                F.seg(f, (cx + dx, cy - 10), (cx + dx, cy - 10 + 20 * u), col)
        if i < 6:
            A4.star(f, cx - 15 + 30 * u, cy + 5, WHITE, 1)
    else:                                                        # panes stand up along the lower score, crack, shatter
        v = i - 9
        for k, (bx, hk) in enumerate(((cx - 9, 9), (cx, 12), (cx + 9, 8))):
            by = cy + 5
            if v < 5:
                h = hk * min(1.0, (v + 1) / 3)
                n = F.frame() if f.size == (F.N, F.N) else Image.new("RGBA", f.size, (0, 0, 0, 0))
                d = ImageDraw.Draw(n)
                d.polygon([(bx - 3, by), (bx - 4, by - h), (bx + 4, by - h), (bx + 3, by)], fill=(91, 103, 134, 255))
                d.polygon([(bx - 3, by), (bx - 4, by - h), (bx, by - h), (bx, by)], fill=(222, 226, 236, 255))
                d.line([(bx - 4, by - h), (bx - 3, by)], fill=(*WHITE, 255))
                d.line([(bx - 4, by - h * 0.5), (bx + 4, by - h * 0.5)], fill=(*GOLD, 255))
                if v >= 3:
                    d.line([(bx, by), (bx + (1 if k % 2 else -1), by - h * (v - 2) / 2)], fill=(*CRACK, 255), width=2)
                F.outline_alpha(n, SCORE)
                f.alpha_composite(n)
            elif v < 11:
                u = v - 5
                for j in range(2):
                    A4.cluster(f, bx + (j * 2 - 1) * (2 + u), by - 8 + 4 * j + 0.35 * u * u, ((222, 226, 236), CRACK)[j], SCORE)


_recast_cell.frames = 20


def _etch_cell(f, cx, cy, i):
    """The scribe carves the lattice (white spark, the cut flares gold), then it dims toward the etch tile."""
    u = min(1.0, (i + 1) / 6)
    col = WHITE if i < 6 else (GOLD_HOT if i < 9 else (GOLD if i < 12 else GOLD_DIM))
    for dy in (-5, 5):
        F.seg(f, (cx - 15, cy + dy + 1), (cx - 15 + 30 * u, cy + dy + 1), SCORE)
        F.seg(f, (cx - 15, cy + dy), (cx - 15 + 30 * u, cy + dy), col)
    for dx in (-7.5, 7.5):
        if dx < 0 or i >= 3:
            F.seg(f, (cx + dx, cy - 10), (cx + dx, cy - 10 + 20 * u), col)
    if i < 6:
        A4.star(f, cx - 15 + 30 * u, cy - 5, WHITE, 2)
        A4.cluster(f, cx - 15 + 30 * u - 3, cy - 4, GOLD_HOT, SCORE)


_etch_cell.frames = 14


def periodic_sets():
    rec, etch = periodic_slice(_recast_cell), periodic_slice(_etch_cell)
    out = []
    for k in range(N_BANDS):
        out.append((f"anim_moe_recast_b{k}_a10.webp", A.delayed(rec, k * BAND_LEAD), f"Recast region breaks, row band {k}"))
        out.append((f"anim_moe_etch_b{k}_a10.webp", A.delayed(etch, k * BAND_LEAD), f"Etching carved, row band {k}"))
    return out


def etch_tile():
    """The Etching's mark (the omen) drawn as the carve leaves it: the floor-plan lattice in gold on a faint pale wash,
    the same lines as _etch_cell (clip +-5 rows, +-7.5 columns map to tile +-12.5, +-9.375), so the carve lands on its
    own mark and the region reads as one etched sheet."""
    t = F.frame()
    d = ImageDraw.Draw(t)
    for y in (12.5, 37.5):
        d.line([(0, y + 1.5), (50, y + 1.5)], fill=(*SCORE, 255), width=2)
        d.line([(0, y), (50, y)], fill=(*GOLD, 255), width=2)
    for x in (15.625, 34.375):
        d.line([(x + 1.5, 0), (x + 1.5, 50)], fill=(*SCORE, 255), width=2)
        d.line([(x, 0), (x, 50)], fill=(*GOLD, 255), width=2)
    for x, y in ((15.625, 12.5), (34.375, 12.5), (15.625, 37.5), (34.375, 37.5)):
        F.blob(t, x, y, GOLD_HOT, r=2)
    m = Image.new("L", (50, 50), 0)
    ImageDraw.Draw(m).polygon(F.T_HEX, fill=255)
    out = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    out.paste(t, (0, 0), m)
    return F.tile_out(out)
