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
    0-5 the floor plan she cut is redrawn white-gold top to bottom, scribe sparks on the cutting front; 6-7 HOLD hot;
    8 one pale frame; 9-12 panes of pale glass stand up along the scores (each its own size, placed across the region,
    not per hex); 13-14 the Remainder's black cracks race up them; 15-18 they shatter, chunks thrown and falling, black
    cracks run along the lattice; 19-23 it settles: the lattice dims to the recast floor's broken gold and black and
    dissolves (dither) onto the floor tile under it."""
    cv = MZ.Canvas(cells)
    rm = region_mask(cv)
    x0, y0, x1, y1 = rm.getbbox()
    rnd = random.Random(seed)
    hs = list(range(y0 + 7, y1, 20))
    vs = list(range(x0 + 12, x1, 30))
    hgaps = {(k, xa): rnd.random() < 0.3 for k in range(len(hs)) for xa in range(x0, x1, 15)}
    vgaps = {(k, ya): rnd.random() < 0.3 for k in range(len(vs)) for ya in range(y0, y1, 10)}
    panes = []
    for y in hs:
        x = x0 + rnd.uniform(3, 8)
        while x < x1 - 4:
            if rm.getpixel((int(x), int(y))):
                panes.append((x, y, rnd.uniform(9, 18), rnd.uniform(4, 7), rnd.uniform(-0.12, 0.12), rnd.random()))
            x += rnd.uniform(7, 12)

    def lattice(f, col, width, ycut=None, keep=1.0, crack=False):
        lat = cv.frame()
        d = ImageDraw.Draw(lat)
        yc = y1 if ycut is None else ycut
        for k, y in enumerate(hs):
            if y > yc:
                continue
            for xa in range(x0, x1, 15):
                if hgaps[(k, xa)]:
                    continue
                d.line([(xa, y + 1), (xa + 15, y + 1)], fill=(*SCORE, 255))
                d.line([(xa, y), (xa + 15, y)], fill=(*col, 255), width=width)
                if crack and (k + xa) % 3 == 0:
                    d.line([(xa + 3, y - 1), (xa + 11, y + 2)], fill=(*CRACK, 255), width=2)
        for k, x in enumerate(vs):
            for ya in range(y0, int(yc), 10):
                if vgaps[(k, ya)]:
                    continue
                d.line([(x + 1, ya), (x + 1, min(yc, ya + 10))], fill=(*SCORE, 255))
                d.line([(x, ya), (x, min(yc, ya + 10))], fill=(*col, 255), width=width)
        f.alpha_composite(dither_keep(masked(lat, rm), keep))

    out = []
    for i in range(frames):
        f = cv.frame()
        if i < 6:
            ycut = y0 + (y1 - y0) * (i + 1) / 6
            lattice(f, GOLD, 1, ycut)
            for x in vs + [x0 + 6, x1 - 6]:
                A4.star(f, x, ycut, WHITE, 2)
        elif i < 8:
            lattice(f, GOLD_HOT, 2)
        elif i == 8:
            pale = cv.frame()
            ImageDraw.Draw(pale).rectangle((x0, y0, x1, y1), fill=(*STEEL_L, 255))
            f.alpha_composite(dither_keep(masked(pale, rm), 0.5))
            lattice(f, WHITE, 2)
        elif i < 19:
            v = i - 9
            lattice(f, GOLD if v < 6 else GOLD_DIM, 1, crack=v >= 4)
            for k, (bx, by, h, w, tilt, ph) in enumerate(panes):
                if v < 6:
                    g = min(1.0, (v + 1) / 3) * (0.85 + 0.3 * ph)
                    hh = h * g
                    n = cv.frame()
                    dd = ImageDraw.Draw(n)
                    tx = bx + tilt * hh
                    top = [(tx - w * 0.65, by - hh), (tx + w * 0.65, by - hh)]
                    dd.polygon([(bx - w / 2, by), top[0], top[1], (bx + w / 2, by)], fill=(*STEEL_S, 255))
                    dd.polygon([(bx - w / 2, by), top[0], (tx, by - hh), (bx, by)], fill=(*STEEL_L, 255))
                    dd.line([top[0], (bx - w / 2, by)], fill=(*WHITE, 255))
                    dd.line([(bx - w * 0.5, by - hh * 0.5), (bx + w * 0.5, by - hh * 0.5)], fill=(*GOLD, 255))
                    if v >= 4:
                        c = (v - 3) / 2
                        dd.line([(bx, by), (bx + tilt * hh * c + (1 if k % 2 else -1), by - hh * min(1, c))],
                                fill=(*CRACK, 255), width=2)
                    F.outline_alpha(n, SCORE)
                    f.alpha_composite(n)
                else:
                    u = v - 6
                    for j in range(3):
                        cx = bx + (j - 1) * (2 + u * 1.3)
                        cy = by - h * (0.25 + 0.25 * j) + 0.45 * u * u
                        if cy < by + 3:
                            A4.cluster(f, cx, cy, (STEEL_L, STEEL_S, CRACK)[j], SCORE)
        else:                                                    # settle onto the floor: dim, then dissolve
            keep = 1.0 - (i - 18) / 5
            lattice(f, GOLD_DIM, 1, keep=keep, crack=True)
        out.append(f)
    return cv, out


def recast_regions(spec_path):
    """Every Recast region in the spec, painted and sliced: {name: {(col, row): frames}}."""
    spec = json.load(open(spec_path))
    out = {}
    for j in spec["jutsu"]:
        r = j["record"]
        if r["name"].startswith("Recast:"):
            cells = [(c["longitude"], c["latitude"]) for c in r["coordinateTargeting"]["coordinates"]]
            cv, fr = recast_region(cells, seed=sum(map(ord, r["name"])))
            out[r["name"].split(": ")[1].lower()] = cv.slices(fr)
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
