#!/usr/bin/env python3
"""Mother of Echoes, Act II: the Etchings and their Recasts as PICTURES (director, 2026-11-05: "it's supposed to draw
patterns on the floor that explode the next turn and you have to remember"; the hatch lattice did not read).

    python3 art/mother_of_echoes_fx/build_fx_etch.py --spec SPEC --out DIR [--regions rime,heart]

Each Etching carves one recognisable picture over its region (fixed board positions: BATTLEFIELD, sliced exactly):
- Rime (north): frost ferns spreading from the north wall;
- Ember (south): a burning brand;
- Seam (west wall): one long jagged scar-crack;
- Heart (middle): a heart-sigil with concentric rings, beating once;
- Hail (scattered): individual struck star-points.
Etching clip: her scribing hand draws it in (a white cutting front, the carve gold), it glows (3-frame hold), then
cools to a faint residual line. The residual is also cut per hex as a STATIC tile (the floor keeps the picture until the
Recast). Recast clip: the same picture remembered: it relights white-hot along its own lines (the replay), holds 3
frames, then bursts upward ALONG ITS LINES as Act II Heartglass (pale glass, gold score, the Remainder's black cracks),
shatters, and settles onto the recast floor. Everything is masked to the region: nothing draws over a hex it misses.
Pillow only.
"""
import argparse
import importlib.util
import json
import math
import os
import random

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("build_fx_paint", os.path.join(HERE, "build_fx_paint.py"))
P = importlib.util.module_from_spec(_s)
_s.loader.exec_module(P)
MZ, A4, A, F = P.MZ, P.A4, P.A, P.F
WHITE, SCORE, GOLD_HOT, GOLD, GOLD_DIM, CRACK = P.WHITE, P.SCORE, P.GOLD_HOT, P.GOLD, P.GOLD_DIM, P.CRACK
STEEL_L, STEEL_S = P.STEEL_L, P.STEEL_S
SMOKE = P.SMOKE
BOARD = [(c, r) for c in range(12) for r in range(10)]


# ------------------------------------------------------------------------------------------------ strokes
def poly(pts, t0, t1, w=2):
    """Sample a polyline at 1 px, its carve time running t0 -> t1 along its length."""
    segs = list(zip(pts, pts[1:]))
    L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs) or 1.0
    out, acc = [], 0.0
    for a, b in segs:
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1])))
        for k in range(n):
            u = k / n
            x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
            out.append((x, y, t0 + (t1 - t0) * (acc + u * math.hypot(b[0] - a[0], b[1] - a[1])) / L, w))
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
    out.append((pts[-1][0], pts[-1][1], t1, w))
    return out


def ellipse(cx, cy, rx, ry, t0, t1, a0=-math.pi / 2, w=2, n=90):
    return poly([(cx + rx * math.cos(a0 + 2 * math.pi * k / n), cy + ry * math.sin(a0 + 2 * math.pi * k / n))
                 for k in range(n + 1)], t0, t1, w)


def motif_rime(cv, cells, rnd):
    """Frost ferns: three fronds from the north wall, pinnate side branches, a second level of tiny barbs, and a
    crystal vein joining them; each frond spreads from its root outward."""
    S = []
    xs = sorted({cv.c(*k)[0] for k in cells})
    top = min(cv.c(*k)[1] for k in cells) - 8
    bot = max(cv.c(*k)[1] for k in cells) + 6
    roots = [xs[1] + 8, (xs[0] + xs[-1]) / 2 + rnd.uniform(-8, 8), xs[-2] - 8]
    for j, rx in enumerate(roots):
        ang = math.pi / 2 + (-0.55, 0.15, 0.6)[j]
        x, y = rx, top
        stem = [(x, y)]
        L = (bot - top) * 1.9
        for k in range(26):
            ang += rnd.uniform(-0.08, 0.08) + (0.02 if j == 0 else -0.02 if j == 2 else 0)
            x += math.cos(ang) * L / 26
            y += 0.5 * math.sin(ang) * L / 26
            stem.append((x, y))
        t0 = 0.05 * j
        S += poly(stem, t0, t0 + 0.55, 2)
        for k in range(3, len(stem) - 2, 3):              # pinnate branches, alternating sides, shorter toward the tip
            for side in (-1, 1):
                bx, by = stem[k]
                a2 = math.atan2(2 * (stem[k + 1][1] - by), stem[k + 1][0] - bx) + side * rnd.uniform(0.8, 1.1)
                bl = (1 - k / len(stem)) * 26 + 6
                br = [(bx, by)]
                for q in range(6):
                    a2 += -side * 0.08
                    br.append((br[-1][0] + math.cos(a2) * bl / 6, br[-1][1] + 0.5 * math.sin(a2) * bl / 6))
                tb = t0 + 0.55 * k / len(stem)
                S += poly(br, tb, tb + 0.18, 1)
                for q in (2, 4):                          # barbs
                    cx_, cy_ = br[q]
                    a3 = a2 + side * 0.9
                    S += poly([(cx_, cy_), (cx_ + math.cos(a3) * 5, cy_ + 0.5 * math.sin(a3) * 5)], tb + 0.1, tb + 0.16, 1)
    return S


def motif_heart(cv, cells, rnd, centre_cells=None):
    """A heart-sigil: the heart drawn first (two lobes into the point), then two concentric rings round it, then
    eight short ticks between the rings, like a seal."""
    cs = [cv.c(*k) for k in (centre_cells or cells)]
    cx = (min(c[0] for c in cs) + max(c[0] for c in cs)) / 2
    cy = (min(c[1] for c in cs) + max(c[1] for c in cs)) / 2
    S = []
    hw = 20                                                  # heart half-width (x); y is squashed 2:1 like the floor
    pts = []
    for k in range(61):
        a = math.pi * 2 * k / 60
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * hw / 16, cy + y * hw / 16 * 0.55))
    S += poly(pts, 0.0, 0.4, 2)
    xs_ = [c[0] for c in cs]; ys_ = [c[1] for c in cs]
    RX, RY = (max(xs_) - min(xs_)) / 2 + 12, (max(ys_) - min(ys_)) / 2 + 6     # the seal fills the whole field
    for k, (sc, t0) in enumerate(((0.62, 0.42), (1.0, 0.62))):
        S += ellipse(cx, cy + 1, max(30, RX * sc), max(17, RY * sc), t0, t0 + 0.2, w=2 if k == 0 else 1)
    for k in range(12):
        a = math.pi * 2 * k / 12 + math.pi / 12
        r0, r1 = 0.66, 0.94
        S += poly([(cx + RX * r0 * math.cos(a), cy + 1 + RY * r0 * math.sin(a)),
                   (cx + RX * r1 * math.cos(a), cy + 1 + RY * r1 * math.sin(a))], 0.84, 0.92, 1)
    return S, (cx, cy)


def motif_ember(cv, cells, rnd):
    """A burning brand: a crest pressed into the floor. A long bar across the region, a diamond at its middle, three
    flames rising out of the diamond, thorned hooks at the bar's ends; carved from the middle outward."""
    xs = [cv.c(*k)[0] for k in cells]; ys = [cv.c(*k)[1] for k in cells]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2 + 2
    S = []
    S += poly([(cx - 28, cy), (cx, cy - 15), (cx + 28, cy), (cx, cy + 15), (cx - 28, cy)], 0.0, 0.3, 2)       # diamond
    S += poly([(cx - 14, cy), (cx, cy - 7), (cx + 14, cy), (cx, cy + 7), (cx - 14, cy)], 0.25, 0.4, 1)
    for k, dx in enumerate((-12, 0, 12)):                     # three flames out of the diamond
        h = 13 if dx == 0 else 9
        base = (cx + dx, cy - 3)
        pts = [base]
        for q in range(1, 9):
            u = q / 8
            pts.append((cx + dx + math.sin(u * 5 + k) * 3 * (1 - u), cy - 3 - h * u))
        S += poly(pts, 0.32 + 0.05 * k, 0.5 + 0.05 * k, 2 if dx == 0 else 1)
    for side in (-1, 1):                                      # the bar, out to both ends, thorned hooks
        x_end = (max(xs) - 6) if side > 0 else (min(xs) + 6)
        S += poly([(cx + 28 * side, cy), (x_end, cy)], 0.45, 0.85, 2)
        for q in range(1, 6):
            tx = cx + side * (28 + (abs(x_end - cx) - 28) * q / 6)
            S += poly([(tx, cy), (tx + 4 * side, cy - 6)], 0.45 + 0.4 * q / 6, 0.5 + 0.4 * q / 6, 1)
            S += poly([(tx, cy), (tx + 4 * side, cy + 6)], 0.45 + 0.4 * q / 6, 0.5 + 0.4 * q / 6, 1)
        S += poly([(x_end, cy), (x_end - 6 * side, cy - 9), (x_end - 12 * side, cy - 6)], 0.85, 0.95, 2)
    return S


def motif_seam(cv, cells, rnd):
    """One long jagged scar-crack down the west wall, splinters breaking off it; carved top to bottom."""
    xs = [cv.c(*k)[0] for k in cells]; ys = [cv.c(*k)[1] for k in cells]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys) - 6, max(ys) + 6
    pts, x = [], (x0 + x1) / 2
    n = 22
    for q in range(n + 1):
        y = y0 + (y1 - y0) * q / n
        x = max(x0 + 6, min(x1 - 6, x + rnd.uniform(-9, 9)))
        pts.append((x, y))
    S = poly(pts, 0.0, 0.85, 2)
    for q in range(2, n - 1, 3):                              # splinters
        px_, py_ = pts[q]
        side = rnd.choice((-1, 1))
        L = rnd.uniform(9, 16)
        a = side * rnd.uniform(0.3, 0.8)
        tip = (max(x0 - 8, min(x1 + 8, px_ + side * L)), py_ + L * 0.5 * math.sin(a))
        t0 = 0.85 * q / n
        S += poly([(px_, py_), ((px_ + tip[0]) / 2, (py_ + tip[1]) / 2 + rnd.uniform(-2, 2)), tip], t0, t0 + 0.1, 1)
    return S


def motif_hail(cv, cells, rnd):
    """Struck star-points: one eight-pointed star on each hex of the scatter, each struck at its own moment."""
    S = []
    order = list(cells)
    rnd.shuffle(order)
    for j, k in enumerate(order):
        cx, cy = cv.c(*k)
        t0 = 0.75 * j / len(order)
        for q in range(8):
            a = math.pi * q / 4
            r = 9 if q % 2 == 0 else 5
            S += poly([(cx, cy), (cx + r * math.cos(a), cy + r * 0.55 * math.sin(a))], t0, t0 + 0.12, 2 if q % 2 == 0 else 1)
    return S


MOTIFS = {"rime": motif_rime, "heart": motif_heart, "ember": motif_ember, "seam": motif_seam, "hail": motif_hail}


# ------------------------------------------------------------------------------------------------ the two clips
def draw_lines(f, S, upto, col, front=None, glow=False, keep=1.0):
    n = Image.new("RGBA", f.size, (0, 0, 0, 0))
    px = n.load()
    for (x, y, t, w) in S:
        if t > upto:
            continue
        c = WHITE if front is not None and t > upto - front else col
        for dx in range(w):
            for dy in range(w if w > 1 else 1):
                X, Y = int(x) + dx, int(y) + dy
                if 0 <= X < f.width and 0 <= Y < f.height and F.BAYER[Y % 4][X % 4] < keep * 16:
                    px[X, Y + 1 if False else Y] = (*c, 255)
        if glow and w > 1:
            X, Y = int(x), int(y) - 1
            if 0 <= X < f.width and 0 <= Y < f.height:
                px[X, Y] = (*WHITE, 255)
    sh = Image.new("RGBA", f.size, (0, 0, 0, 0))             # the scored groove under it, 1 px down
    a = n.getchannel("A")
    sh.paste((*SCORE, 255), (0, 1), a)
    f.alpha_composite(sh)
    f.alpha_composite(n)


def etching(cv, rm, S, frames=22):
    """0-9 the scribe draws it in (white cutting front + spark); 10-12 HOLD, glowing; 13-21 it cools to the residual."""
    out = []
    heads = {}
    for i in range(frames):
        f = cv.frame()
        if i < 10:
            T = (i + 1) / 10
            draw_lines(f, S, T, GOLD, front=0.06)
            for (x, y, t, w) in S:                           # sparks on each live cutting front
                if T - 0.012 < t <= T and w > 1:
                    A4.star(f, x, y, WHITE, 2)
        elif i < 13:
            draw_lines(f, S, 1.0, GOLD_HOT, glow=True)
        else:
            u = (i - 12) / (frames - 13)
            draw_lines(f, S, 1.0, GOLD if u < 0.4 else GOLD_DIM, keep=1.0 - 0.75 * u)
        out.append(P.masked(f, rm))
    return out


def residual(cv, rm, S):
    f = cv.frame()
    draw_lines(f, S, 1.0, GOLD_DIM)
    return P.masked(f, rm)


def recast(cv, rm, S, frames=24, seed=3):
    """0-2 the glass remembers: the picture relights white-hot along its own lines, in the carve's order, fast;
    3-5 HOLD (identical); 6-11 Heartglass bursts upward along the lines, the Remainder's cracks creep up it;
    12-17 it shatters, chunks thrown and falling; 18-23 it settles: the lines dim to broken gold and black, dissolving."""
    rnd = random.Random(seed)
    up = {}
    m = rm.load()

    def room(x, y):                                          # how far a shard may rise and stay on our hexes
        h = 0
        while h < 16 and 0 <= y - h - 1 and m[int(x), int(y - h - 1)]:
            h += 1
        return h
    shards = []
    for k, (x, y, t, w) in enumerate(S):
        if k % (4 if w > 1 else 7) == 0 and 0 <= int(x) < cv.w and 0 <= int(y) < cv.h and m[int(x), int(y)]:
            h = min(room(x, y) - 1, rnd.randint(7, 14) if w > 1 else rnd.randint(4, 8))
            if h >= 3:
                shards.append((x, y, h, rnd.choice((2, 2, 3)), rnd.uniform(-0.25, 0.25), t))
    out = []
    for i in range(frames):
        f = cv.frame()
        if i < 3:
            draw_lines(f, S, 1.0, GOLD_DIM)
            draw_lines(f, S, (i + 1) / 3, WHITE, front=0.15)
        elif i < 6:
            draw_lines(f, S, 1.0, WHITE, glow=True)
        elif i < 12:
            v = i - 6
            draw_lines(f, S, 1.0, GOLD_HOT)
            n = cv.frame()
            d = ImageDraw.Draw(n)
            for (x, y, h, wd, tilt, t) in sorted(shards, key=lambda s_: s_[1]):
                g = min(1.0, (v + 1) / 3 - 0.4 * t)
                if g <= 0:
                    continue
                hh = h * g
                tip = (x + tilt * hh, y - hh)
                d.polygon([(x - wd, y), (x + wd, y), tip], fill=(*STEEL_L, 255))
                d.line([(x + wd, y), tip], fill=(*STEEL_S, 255))
                d.line([(x - wd + 0.5, y - 1), tip], fill=(*WHITE, 255))
                if hh > 6:
                    d.line([(x - wd * 0.6, y - hh * 0.45), (x + wd * 0.6, y - hh * 0.45)], fill=(*GOLD, 255))
                if v >= 3:
                    c_ = min(1.0, (v - 2) / 3)
                    d.line([(x, y), (x + tilt * hh * c_, y - hh * c_ * 0.9)], fill=(*CRACK, 255), width=1)
            F.outline_alpha(n, SCORE)
            f.alpha_composite(n)
        elif i < 18:
            u = i - 11
            draw_lines(f, S, 1.0, GOLD_DIM)
            for k, (x, y, h, wd, tilt, t) in enumerate(shards):
                for j in range(2):
                    cx_ = x + (j * 2 - 1) * (1 + 1.1 * u) + tilt * h
                    cy_ = y - h * (0.4 + 0.3 * j) - 1.6 * u + 0.5 * u * u
                    if cy_ < y + 4 and (u < 4 or (k + j) % 2):
                        P.cluster(f, cx_, cy_, STEEL_L if j else STEEL_S, SCORE)
                if u < 3 and k % 3 == 0:
                    F.px(f, x, y - h * 0.6 - u, SMOKE)
            f = P.masked(f, rm)
        else:
            keep = 1.0 - (i - 17) / 6
            draw_lines(f, S, 1.0, GOLD_DIM, keep=keep)
            n = cv.frame()
            for k, (x, y, t, w) in enumerate(S):
                if k % 9 < 3 and w > 1:
                    F.px(n, x, y, CRACK, keep=keep)
            f.alpha_composite(n)
        out.append(P.masked(f, rm))
    return out


def hex_tile(cv, k, img):
    """A hex's own part of a ground painting as a static tile: its w x h box onto the 50 px tile, hex-masked."""
    cx, cy = cv.c(*k)
    t = img.crop((int(cx) - 20, int(cy) - 10, int(cx) + 20, int(cy) + 10)).resize((50, 50), Image.NEAREST)
    m = Image.new("L", (50, 50), 0)
    ImageDraw.Draw(m).polygon(F.T_HEX, fill=255)
    out = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    out.paste(t, (0, 0), m)
    return F.tile_out(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--regions", default="rime,heart")
    ap.add_argument("--residual", action="store_true", help="also cut the residual picture per hex as static tiles")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    spec = json.load(open(a.spec))
    reg = {}
    for j in spec["jutsu"]:
        r = j["record"]
        for pre in ("Etching: ", "Recast: "):
            if r["name"].startswith(pre):
                reg.setdefault(r["name"][len(pre):].lower(), {})[pre.strip(": ").lower()] = \
                    [(c["longitude"], c["latitude"]) for c in r["coordinateTargeting"]["coordinates"]]
    rows = []
    for name in a.regions.split(","):
        ec, rc = reg[name]["etching"], reg[name]["recast"]
        if set(ec) != set(rc):                                # director 2026-11-05: Heart's Etching widens to the Recast field
            print(f"{name}: Etching {len(ec)} hexes vs Recast {len(rc)}; carving over the Recast field")
            ec = rc
        cv = MZ.Canvas(BOARD)
        rnd = random.Random(sum(map(ord, name)))
        got = MOTIFS[name](cv, ec, rnd)
        S = got[0] if isinstance(got, tuple) else got
        for kind, cells, frames in (("etch", ec, None), ("recast", rc, None)):
            sub = MZ.Canvas(BOARD)
            sub.cells = list(cells)
            rm = P.region_mask(sub)
            fr = etching(cv, rm, S) if kind == "etch" else recast(cv, rm, S)
            sl = cv.slices(fr)
            for k in cells:
                fn = f"anim_moe_{kind}2_{name}_p{k[0]}_{k[1]}_a14.webp"
                F.strip(sl[k]).save(os.path.join(a.out, fn), lossless=True, quality=100, method=6)
                rows.append({"file": fn, "region": f"{kind}_{name}", "col": k[0], "row": k[1], "frames": len(fr)})
            if kind == "etch" and a.residual:                # director 2026-11-05: none (the picture lives in the carve)
                res = residual(cv, rm, S)
                for k in cells:
                    fn = f"tile_moe_etch2_{name}_p{k[0]}_{k[1]}_a14.webp"
                    hex_tile(cv, k, res).save(os.path.join(a.out, fn), lossless=True, quality=100, method=6)
                    rows.append({"file": fn, "region": f"etchtile_{name}", "col": k[0], "row": k[1], "frames": 1})
    json.dump({"slices": rows}, open(os.path.join(a.out, f"moe_fx_etch2_{a.regions.replace(',', '_')}.json"), "w"), indent=1)
    print(len(rows), "assets")


if __name__ == "__main__":
    main()
