#!/usr/bin/env python3
"""Slice mosaics: one large composition cut into per-hex clips (director, 2026-11-05: "you can also have them each play
a different frame of a larger animation to make one big effect").

    python3 art/mother_of_echoes_fx/build_fx_mosaic.py --out DIR   (prototype: the Refraction line, 12 slices)

Engine geometry (docs/design/COMBAT_ANIMATION_ENGINE.md 3.1; theninjarpg@3314d122): a tile box is hexSize x 0.5
hexSize (flat hex), columns sit 0.75 hexSize apart and rows one tile height apart, odd columns half a row LOWER
(honeycomb-grid's default offset -1 = odd-q; util.ts:3419). Every clip is a square of 2.5 tile heights centred on its
hex, drawn from the 50 px CDN rendition with linear filtering, so one source pixel is 1/20 of a tile height on every
hex. In source pixels: column pitch 30, row pitch 20, odd-column drop 10, hex footprint 40 x 20, clip 50 x 50. The
composition is drawn once on a canvas at that density and each hex's clip carries only the canvas pixels that hex
OWNS: the nearest covered hex centre in the hex metric (y doubled, so cells are the hex footprints), out to its clip
square, plus a 1 px overlap so linear filtering never opens a seam. Shapes may rise above or below the row: those
pixels belong to the nearest covered hex as long as they sit in its clip square.
Timing: every slice of one cast arrives in the same snapshot and starts when its own texture is ready
(combatEffects.ts:157-166, :212). Once loaded they start on the same frame; on the first cast in a battle each slice
waits for its own texture (2.4 first-use lag), so the very first play can stagger. Pieces are drawn so a stagger reads
as a ripple, not a tear: no single shape is split across more than two hexes.
"""
import argparse
import importlib.util
import json
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, file):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


A4 = _load("build_fx_a4", "build_fx_a4.py")
A, F = A4.A, A4.F
PAL, PRISM, WHITE, SCORE, EMB_Y = A.PAL, A4.PRISM, F.WHITE, F.SCORE, F.EMBER_YEL
CP, RP, DROP, HALF = 30, 20, 10, 25        # column pitch, row pitch, odd-column drop, clip half-size (source px)
PAD = 30                                   # canvas margin round the covered hexes


def centre(col, row):
    return CP * col, RP * row + (DROP if col % 2 else 0)


class Canvas:
    """A composition canvas over a set of (col, row) hexes."""

    def __init__(self, cells):
        self.cells = list(cells)
        xs = [centre(*c)[0] for c in self.cells]
        ys = [centre(*c)[1] for c in self.cells]
        self.ox, self.oy = min(xs) - PAD, min(ys) - PAD
        self.w, self.h = max(xs) - self.ox + PAD + 1, max(ys) - self.oy + PAD + 1
        self.owner = self._owners()

    def c(self, col, row):
        x, y = centre(col, row)
        return x - self.ox, y - self.oy

    def frame(self):
        return Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))

    def _owners(self):
        """Per hex: an L mask of the canvas pixels its clip carries (nearest centre, y doubled, + 1 px overlap)."""
        cs = [self.c(*k) for k in self.cells]
        masks = {k: Image.new("L", (self.w, self.h), 0) for k in self.cells}
        px = {k: m.load() for k, m in masks.items()}
        for y in range(self.h):
            for x in range(self.w):
                d = [math.hypot(x - cx, 2 * (y - cy)) for cx, cy in cs]
                best = min(d)
                for k, (cx, cy), dk in zip(self.cells, cs, d):
                    if dk <= best + 2.2 and abs(x - cx) < HALF - 1 and abs(y - cy) < HALF - 1:
                        px[k][x, y] = 255
        return masks

    def slices(self, frames):
        """{(col, row): [50 x 50 frames]}: each hex's own part of every canvas frame."""
        out = {}
        for k in self.cells:
            cx, cy = self.c(*k)
            box = (int(cx) - HALF, int(cy) - HALF, int(cx) + HALF, int(cy) + HALF)
            m = self.owner[k].crop(box)
            fr = []
            for f in frames:
                g = Image.new("RGBA", (2 * HALF, 2 * HALF), (0, 0, 0, 0))
                g.paste(f.crop(box), (0, 0), m)
                fr.append(g)
            out[k] = fr
        return out


# ------------------------------------------------------------------------------------------------ Refraction Breaks: the line
def shard_on(f, x, base, h, w, tilt, hot=False):
    """A Heartglass shard on a canvas: framed, white facet line, the ember edge on its right face."""
    p = PAL["I"]
    n = Image.new("RGBA", f.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(n)
    tip = (x + tilt * h, base - h)
    mid = (x + tilt * h * 0.5, base - h * 0.2)
    d.polygon([(x - w / 2, base), tip, mid], fill=(*(WHITE if hot else p["lite"]), 255))
    d.polygon([mid, tip, (x + w / 2, base)], fill=(*p["body"], 255))
    d.line([(x - w / 2 + 1, base - 1), tip], fill=(*WHITE, 255))
    d.line([tip, (x + w / 2, base)], fill=(*EMB_Y, 255))
    F.outline_alpha(n, p["frame"])
    f.alpha_composite(n)


def refraction_line(cells, mirrored=False, frames=32):
    """One Refraction line shattering as a single image: light runs in from both walls along the line (or, mirrored, from
    one wall across the hall), meets in a white flash, the line cracks along its length, a palisade of Heartglass shards
    bursts up across hex seams, then breaks into prism light and falls."""
    cv = Canvas(cells)
    pts = sorted(cv.c(*k) for k in cells)
    xl, xr = pts[0][0], pts[-1][0]
    p = PAL["I"]

    def y_at(x):  # the line's height at x: through the hex centres
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / max(1, x1 - x0)
        return pts[0][1] if x < xl else pts[-1][1]

    import random
    rnd = random.Random(11)
    shards = []
    x = xl - 14
    while x < xr + 14:
        shards.append((x, rnd.uniform(14, 30), rnd.uniform(6, 10), rnd.uniform(-0.25, 0.25), rnd.random()))
        x += rnd.uniform(6, 10)
    out = []
    RUN, HIT = 7, 2
    for i in range(frames):
        f = cv.frame()
        if i < RUN:                                        # the light runs in
            t = (i + 1) / RUN
            heads = [xl - 15 + (xr - xl + 30) * t] if mirrored else [xl - 15 + (xr - xl) / 2 * t + 15 * t,
                                                                     xr + 15 - (xr - xl) / 2 * t - 15 * t]
            lo, hi = (xl - 15, heads[0]) if mirrored else (None, None)
            for xx in range(int(xl - 15), int(xr + 16)):
                lit = (lo <= xx <= hi) if mirrored else (xx <= heads[0] or xx >= heads[1])
                if not lit:
                    continue
                y = y_at(xx)
                F.px(f, xx, y - 1, p["lite"])
                F.px(f, xx, y, WHITE)
                F.px(f, xx, y + 1, p["lite"])
                F.px(f, xx, y - 2, PRISM[xx % 4], keep=0.5)
            for hx in heads:
                A4.star(f, hx, y_at(hx), WHITE, 3)
                for k in range(4):
                    F.px(f, hx - (6 + 3 * k) * (1 if (mirrored or hx < (xl + xr) / 2) else -1), y_at(hx) - 2 + k,
                         PRISM[k])
        elif i < RUN + HIT:                                # the flash: the whole line white, cracked along its length
            for xx in range(int(xl - 16), int(xr + 17)):
                y = y_at(xx)
                for dy in range(-3, 4):
                    F.px(f, xx, y + dy, WHITE if abs(dy) < 2 else p["hot"])
                if xx % 7 == 0:
                    F.seg(f, (xx, y - 4), (xx + 3, y + 4), p["frame"])
        else:                                              # the palisade bursts up, holds, breaks and falls
            u = i - RUN - HIT
            for k, (sx, h, w, tilt, ph) in enumerate(shards):
                base = y_at(sx) + 4
                if u < 9:
                    g = min(1.0, (u + 1) / 3)
                    hh = h * g * (1 + 0.08 * math.sin(u + ph * 6))
                    shard_on(f, sx, base, hh, w, tilt, hot=u < 2)
                    if 3 <= u < 9 and int(ph * 6 + u) % 6 == 0:  # a mirror glint slides up the shard
                        A4.star(f, sx + tilt * hh * 0.6, base - hh * 0.6, WHITE, 2)
                else:
                    v = u - 9
                    if v > 12 or (v > 7 and k % 2):
                        continue
                    for j in range(3):
                        cx = sx + (j - 1) * 3 + tilt * h * 0.5 + (j - 1) * v * 0.6
                        cy = base - h * (0.3 + 0.25 * j) + 0.35 * v * v
                        F.blob(f, cx, cy, (WHITE, p["lite"], p["body"])[j] if v < 6 else PRISM[(k + j) % 4], r=2 if v < 5 else 1)
            if u < 4:                                      # the crack line stays lit under the burst
                for xx in range(int(xl - 16), int(xr + 17)):
                    F.px(f, xx, y_at(xx) + 3, EMB_Y if u < 2 else F.EMBER_RED)
        out.append(f)
    return cv, out


def export(out_dir, prefix, sl):
    rows = []
    for (col, row), fr in sorted(sl.items()):
        name = f"{prefix}_c{col}_r{row}.webp"
        F.strip(fr).save(os.path.join(out_dir, name), lossless=True, quality=100, method=6)
        rows.append({"file": name, "col": col, "row": row, "frames": len(fr)})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="prototype output folder (slices are not shipped yet)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cv, fr = refraction_line([(c, 1) for c in range(12)])
    rows = export(a.out, "anim_moe_rline", cv.slices(fr))
    cv.frame()  # keep the canvas alive for previews
    with open(os.path.join(a.out, "moe_fx_mosaic.json"), "w") as fh:
        json.dump({"source": "art/mother_of_echoes_fx/build_fx_mosaic.py", "slices": rows}, fh, indent=1)
    # whole-composition preview (unsliced) for comparison
    sheet = Image.new("RGBA", (cv.w, cv.h * 8), (40, 44, 56, 255))
    for j, t in enumerate((2, 5, 7, 9, 11, 15, 20, 26)):
        sheet.alpha_composite(fr[t], (0, j * cv.h))
    sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(os.path.join(a.out, "_rline_canvas.png"))
    print(len(rows), "slices")


if __name__ == "__main__":
    main()
