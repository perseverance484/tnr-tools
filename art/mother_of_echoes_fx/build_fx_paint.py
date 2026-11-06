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


def region_mask(cv):
    m = Image.new("L", (cv.w, cv.h), 0)
    d = ImageDraw.Draw(m)
    for k in cv.cells:
        d.polygon(hex_poly(*cv.c(*k), 42, 22), fill=255)    # 1 px past the footprint so slices overlap, not gap
    return m


def masked(f, m):
    out = Image.new("RGBA", f.size, (0, 0, 0, 0))
    out.paste(f, (0, 0), m)
    return out


# ------------------------------------------------------------------------------------------------ the payoff
def recast_region(cells, frames=24, seed=7):
    cv = MZ.Canvas(cells)
    rm = region_mask(cv)
    bb = rm.getbbox()
    x0, y0, x1, y1 = bb
    rnd = random.Random(seed)
    # the lattice she cut: horizontal scores every half row, verticals every half column, as a floor plan (gaps)
    hs = [y for y in range(y0 + 7, y1, 20)]                  # one score a row, one a column: a floor plan, not a grid
    vs = [x for x in range(x0 + 12, x1, 30)]
    gaps = {(o, k): rnd.random() < 0.35 for o in "hv" for k in range(40)}
    hseg = [(y, xa, xb) for y in hs for xa, xb in [(x0, x1)] if True]
    blades = []
    for y in hs:                                              # panes stand up along the row scores
        x = x0 + 6
        while x < x1 - 4:
            if rm.getpixel((int(x), int(y))) and rnd.random() < 0.85:
                blades.append((x + rnd.uniform(-1.5, 1.5), y, rnd.uniform(10, 16), rnd.uniform(5, 7), rnd.uniform(-0.1, 0.1)))
            x += rnd.uniform(8, 11)
    out = []
    RUN, HOLD = 6, 2
    for i in range(frames):
        f = cv.frame()
        lat = cv.frame()
        if i < RUN + HOLD + 1:                               # the lattice redraws in the order she cut it
            ycut = y0 + (y1 - y0) * min(1.0, (i + 1) / RUN)
            hot = i >= RUN
            d = ImageDraw.Draw(lat)
            col = WHITE if hot and i == RUN + HOLD else (GOLD_HOT if hot else GOLD)
            for k, y in enumerate(hs):
                if y <= ycut:
                    for xa in range(x0, x1, 15):             # rooms: a score with doorways left out
                        if gaps[("h", (k * 7 + xa // 15) % 40)]:
                            continue
                        d.line([(xa, y + 1), (xa + 15, y + 1)], fill=(*SCORE, 255), width=1)
                        d.line([(xa, y), (xa + 15, y)], fill=(*col, 255), width=2 if hot else 1)
            for k, x in enumerate(vs):
                for ya in range(y0, int(ycut), 10):
                    if gaps[("v", (k * 5 + ya // 10) % 40)]:
                        continue
                    d.line([(x + 1, ya), (x + 1, min(ycut, ya + 10))], fill=(*SCORE, 255))
                    d.line([(x, ya), (x, min(ycut, ya + 10))], fill=(*col, 255), width=2 if hot else 1)
            if not hot:                                      # the scribe sparks at the cutting edge
                for x in vs[::2]:
                    A4.star(lat, x, ycut, WHITE, 2)
            if i == RUN + HOLD:                              # the pale frame: the whole region lights
                pale = cv.frame()
                ImageDraw.Draw(pale).rectangle(bb, fill=(*GLASS_L, 255))
                for y in range(y0, y1):
                    for x in range(x0, x1):
                        if F.BAYER[y % 4][x % 4] >= 8:
                            pale.putpixel((x, y), (0, 0, 0, 0))
                f.alpha_composite(masked(pale, rm))
            f.alpha_composite(masked(lat, rm))
        else:                                                # blades stand up along the scores, crack, shatter
            v = i - (RUN + HOLD + 1)
            for k, (bx, by, h, w, tilt) in enumerate(blades):
                if v < 6:
                    g = min(1.0, (v + 1) / 3)
                    hh = h * g
                    n = cv.frame()
                    dd = ImageDraw.Draw(n)
                    tx = bx + tilt * hh                     # a pane, wider at the top (bible 5.4), framed
                    top = [(tx - w * 0.7, by - hh), (tx + w * 0.7, by - hh)]
                    dd.polygon([(bx - w / 2, by), top[0], top[1], (bx + w / 2, by)], fill=(*GLASS_B, 255))
                    dd.polygon([(bx - w / 2, by), top[0], (tx, by - hh), (bx, by)], fill=(*GLASS_L, 255))
                    dd.line([top[0], (bx - w / 2, by)], fill=(*WHITE, 255))
                    dd.line([(bx - w * 0.55, by - hh * 0.5), (bx + w * 0.55, by - hh * 0.5)], fill=(*GOLD, 255))
                    tip = (tx, by - hh)
                    if v >= 3:                               # the Remainder's black crack races up the blade
                        c = (v - 2) / 3
                        dd.line([(bx, by), (bx + tilt * hh * c + (1 if k % 2 else -1), by - hh * c)], fill=(*CRACK, 255), width=2)
                    F.outline_alpha(n, SCORE)
                    f.alpha_composite(n)
                else:                                        # shatter: chunks thrown, then fall
                    u = v - 6
                    if u > 8 or (u > 5 and k % 2):
                        continue
                    for j in range(3):
                        cx = bx + (j - 1) * (2 + u * 1.2)
                        cy = by - h * (0.25 + 0.25 * j) + 0.4 * u * u
                        A4.cluster(f, cx, cy, (GLASS_L, GLASS_B, CRACK)[j], SCORE)
            if v < 3:                                        # the scores stay lit under the rising blades
                lat = cv.frame()
                d = ImageDraw.Draw(lat)
                for y in hs:
                    d.line([(x0, y), (x1, y)], fill=(*GOLD, 255))
                f.alpha_composite(masked(lat, rm))
        out.append(f)
    return cv, out


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
    return _veined_tile(41, (14, 12, 18), (70, 84, 98), (96, 214, 236), [(206, 210, 222), (206, 210, 222)],
                        frost=((70, 84, 98), (150, 160, 174)), nveins=3, step=6, wdark=2)


def floor_iii():
    """Sayo, Act III (the Remainder): blackened obsidian, teal cracks frozen mid-run, bone flecks."""
    return _veined_tile(53, (18, 23, 30), (20, 42, 51), (146, 182, 191), [(235, 236, 235), (170, 172, 176)],
                        nveins=4, step=6, wdark=4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cells", default="seam", help="seam: Recast: Seam's region (columns 0-3, every row)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
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
