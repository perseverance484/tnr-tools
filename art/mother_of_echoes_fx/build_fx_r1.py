#!/usr/bin/env python3
"""Mother of Echoes, the ratio-1 re-author (director's ruling 2026-11-05: upstream game main cb755375 is the live game).

    python3 art/mother_of_echoes_fx/build_fx_r1.py [--out DIR]

Geometry (game main cb755375, read-only): an effect clip is drawn h x h at the hex centre (animation.ts:72
EFFECT_ANIMATION_HEX_RATIO = 1; combatEffects.ts:126/130), from the 50 px rendition, linear. Hexes are w x h with w = 2h,
columns 1.5h apart, odd columns h/2 lower. So a clip covers only the middle half of its hex and never touches its
neighbours' clips: a 0.5h gap lies between columns. Static art (staticAssetPath) still fills the whole w x h box
(combatEffects.ts:139-150), under the fighters.

So a line or field that must read as one picture is split in two layers:
- the GROUND layer (static tile per hex, cropped to the hex outline so neighbours never double-draw): what stays and
  what carries the line across the column seams;
- the MOTION layer (clip per hex, the h x h window at the centre): the run, the hold, the burst, sliced from the same
  painting so every centre lines up with its neighbours' ground.

The canvas is drawn at the clip's own scale: 1 px = h/50 (2.5x finer than the old 2.5h clip). Static tiles carry
50 x 50 source pixels over a 2h x h box, so the ground layer is drawn at full scale and halved horizontally.

Batch R1-1: the Refraction line (director's 10/10 bar).
- anim_moe_rbreak1_{l,r}{col}_r1.webp: the Breaks payoff, motion layer.
- tile_moe_rscar_{l,r}{col}_r1.webp: the Breaks' ground: the cracked line the break leaves on the floor.
- tile_moe_rmark_{l,r}{col}_r1.webp: the omen's ground: the lit mark line (replaces the a6 mark-arrival clip as the
  line's continuity; the arrival run survives as anim_moe_rmark1_{l,r}{col}_r1.webp in the centres).
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
_s = importlib.util.spec_from_file_location("build_fx_mosaic", os.path.join(HERE, "build_fx_mosaic.py"))
MZ = importlib.util.module_from_spec(_s)
_s.loader.exec_module(MZ)
A4, A, F = MZ.A4, MZ.A, MZ.F
PAL, PRISM, WHITE = A.PAL, MZ.PRISM, F.WHITE
P = PAL["I"]

H = 50                      # px per hex height (the clip's own source scale)
CP, DROP = 75, 25           # column pitch 1.5h, odd-column drop h/2
PADX, PADY = 60, 40
ROWS = {"L": [(c, 1) for c in range(0, 9)], "R": [(c, 1) for c in range(3, 12)]}


class Canvas1:
    """A composition canvas over a set of (col, row) hexes in the ratio-1 geometry."""

    def __init__(self, cells):
        self.cells = list(cells)
        c0 = min(c for c, _ in self.cells)
        r0 = min(r for _, r in self.cells)
        self.c0, self.r0 = c0, r0
        xs = [self.c(*k)[0] for k in self.cells]
        ys = [self.c(*k)[1] for k in self.cells]
        self.w, self.h = int(max(xs) + PADX + 1), int(max(ys) + PADY + DROP)

    def c(self, col, row):
        return PADX + CP * (col - self.c0), PADY + H * (row - self.r0) + (DROP if col % 2 else 0)

    def frame(self):
        return Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))

    def clip(self, k, frames):
        cx, cy = self.c(*k)
        box = (cx - H // 2, cy - H // 2, cx + H // 2, cy + H // 2)
        return [f.crop(box) for f in frames]

    def ground(self, k, img):
        """The hex's own part of a ground painting: its w x h box cropped to the hex outline, then halved horizontally
        (static art carries 50 source px across 2h) and tripled to the 150 px tile the uploader expects."""
        cx, cy = self.c(*k)
        box = (cx - H, cy - H // 2, cx + H, cy + H // 2)
        m = Image.new("L", (2 * H, H), 0)
        ImageDraw.Draw(m).polygon([(0, H / 2), (H / 2, 0), (1.5 * H, 0), (2 * H, H / 2), (1.5 * H, H), (H / 2, H)],
                                  fill=255, outline=255)
        g = Image.new("RGBA", (2 * H, H), (0, 0, 0, 0))
        g.paste(img.crop(box), (0, 0), m)
        half = Image.new("RGBA", (H, H), (0, 0, 0, 0))
        src = g.load()
        dst = half.load()
        for y in range(H):
            for x in range(H):
                a, b = src[2 * x, y], src[2 * x + 1, y]
                dst[x, y] = a if a[3] >= b[3] else b      # keep the line: the stronger of each pair
        return half.resize((150, 150), Image.NEAREST)


def line_of(cv):
    pts = sorted(cv.c(*k) for k in cv.cells)
    xl, xr = pts[0][0] - H, pts[-1][0] + H                       # to the hex's outer vertex: the wall

    def y_at(x):
        if x <= pts[0][0]:
            return pts[0][1] + (pts[0][1] - pts[1][1]) * (pts[0][0] - x) / CP
        if x >= pts[-1][0]:
            return pts[-1][1] + (pts[-1][1] - pts[-2][1]) * (x - pts[-1][0]) / CP
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts, xl, xr, y_at


def in_clip(cv, x, margin=2):
    return any(abs(x - cv.c(*k)[0]) <= H // 2 - margin for k in cv.cells)


def shard(n, x, y, hgt, wid, lean):
    d = ImageDraw.Draw(n)
    tip = (x + lean, y - hgt)
    d.polygon([(x - wid, y), (x + wid, y), tip], fill=(*P["body"], 255))
    d.line([(x - wid + 1, y - 1), tip], fill=(*P["lite"], 255))
    d.line([(x + 1, y - 1), (tip[0] + 0.4, tip[1] + 2)], fill=(*P["hot"], 255))
    F.px(n, tip[0], tip[1], WHITE)


def refraction_break(cells, frames=32, seed=7):
    """The Breaks payoff, motion layer: light runs from the wall along the line through every hex centre (the ground
    carries it across the seams), the whole line holds white for two frames with a star on every centre, the line
    cracks and a low palisade of Heartglass shards stands up out of it, then breaks into prism light and falls,
    and the clip thins to exactly the scar the ground keeps."""
    cv = Canvas1(cells)
    pts, xl, xr, y_at = line_of(cv)
    rnd = random.Random(seed)
    RUN, HOLD, RISE = 10, 2, 9
    xs = [x for x in range(int(xl) + 4, int(xr) - 3, 6)]
    def near(x):
        return min(abs(x - cx) for cx, _ in pts)
    # each hex's palisade is a bloom: tallest at its centre, tapering to the clip's edge (the ground carries the seam)
    spikes = [(x + rnd.randint(-1, 1), int(rnd.randint(15, 20) * (1 - 0.65 * (near(x) / 22) ** 2)), rnd.choice((2, 2, 3)),
               rnd.uniform(-2, 2) + (x - min(pts, key=lambda p: abs(x - p[0]))[0]) * 0.12, rnd.randint(0, 4))
              for x in range(int(xl) + 4, int(xr) - 3, 4) if in_clip(cv, x, 4)]
    hang = [(x + 3, rnd.randint(4, 7)) for x in xs[::2] if in_clip(cv, x, 6)]
    out = []
    for i in range(frames):
        f = cv.frame()
        if i < RUN:                                              # the run: one head, from the wall
            t = A4.ease((i + 1) / RUN)
            hx = xl + (xr - xl) * t
            for x in range(int(xl), int(hx) + 1):
                y = y_at(x)
                F.px(f, x, y - 1, P["lite"]); F.px(f, x, y, WHITE); F.px(f, x, y + 1, P["lite"]); F.px(f, x, y + 2, P["seam"])
            hy = y_at(hx)
            for k in range(-9, 10):                              # the head: a white star with a tall flare
                F.px(f, hx, hy + k, WHITE if abs(k) < 5 else P["hot"])
            A4.star(f, hx, hy, WHITE, 5)
            for k in range(3):
                A4.cluster(f, hx - (8 + 6 * k), hy - 4 + 3 * k, PRISM[k], P["seam"])
        elif i < RUN + HOLD:                                     # the hold: nothing moves; every centre is a prism node
            for x in range(int(xl), int(xr) + 1):
                y = y_at(x)
                for dy in (-2, -1, 0, 1, 2):
                    F.px(f, x, y + dy, WHITE if abs(dy) < 1 else P["hot"] if abs(dy) < 2 else P["lite"])
                F.px(f, x, y + 3, P["seam"])
            for (cx, cy) in pts:
                A4.star(f, cx, cy, WHITE, 11 if i == RUN else 9)
                for k in range(-5, 6):
                    F.px(f, cx + k, cy + k, P["hot"]); F.px(f, cx + k, cy - k, P["hot"])
                for k, (dx, dy) in enumerate(((-9, -6), (9, -6), (-10, 5), (10, 5))):
                    A4.cluster(f, cx + dx, cy + dy, PRISM[k], P["seam"])
        elif i < RUN + HOLD + RISE:                              # the crack and the palisade
            u = (i - RUN - HOLD + 1) / RISE
            n = cv.frame()
            for x in range(int(xl), int(xr) + 1):
                y = y_at(x)
                F.px(f, x, y - 1, P["hot"]); F.px(f, x, y, WHITE if u < 0.3 else P["hot"]); F.px(f, x, y + 1, P["lite"])
                if (x // 3) % 2 == 0 or u > 0.5:                 # the crack opens along the line
                    F.px(f, x, y + 2 + ((x // 5) % 2), P["deep"])
            for sx, hgt, wid, lean, lag in spikes:
                v = A4.ease(max(0.0, (u * RISE - lag * 0.5) / (RISE * 0.6)))
                if v > 0:
                    shard(n, sx, y_at(sx) - 1, max(2, hgt * v), wid, lean * v)
            for hx, hl in hang:
                v = A4.ease(u)
                d = ImageDraw.Draw(n)
                y = y_at(hx) + 2
                d.polygon([(hx - 1.5, y), (hx + 1.5, y), (hx, y + hl * v)], fill=(*P["body"], 255))
            F.outline_alpha(n, P["deep"])
            f.alpha_composite(n)
            if u > 0.7:
                for k, (sx, hgt, *_r) in enumerate(spikes[::3]):
                    A4.star(f, sx, y_at(sx) - hgt, WHITE, 2)
        else:                                                    # the break: prism light falls, the line thins to the scar
            v = i - RUN - HOLD - RISE
            span = frames - RUN - HOLD - RISE
            keep = max(0.0, 1 - v / (span - 1))
            for x in range(int(xl), int(xr) + 1):
                y = y_at(x)
                F.px(f, x, y, P["lite"] if v < 4 else P["glint"], keep=max(keep, 0.0))
                F.px(f, x, y + 1, P["deep"], keep=keep)
            for k, (sx, hgt, *_r) in enumerate(spikes):
                y0 = y_at(sx) - hgt * 0.6
                for j in range(2):
                    fx = sx + (j * 2 - 1) * (1 + 0.6 * v) + (k % 3 - 1)
                    fy = y0 + 1.5 * v + 0.45 * v * v + 3 * j
                    if fy > y_at(sx) + 20 or keep <= 0:
                        continue
                    if v < 3:
                        A4.cluster(f, fx, fy, P["body"] if j else P["lite"], P["deep"])
                    else:
                        F.px(f, fx, fy, PRISM[(k + j) % 4], keep=keep + 0.15)
                        F.px(f, fx + 1, fy, PRISM[(k + j) % 4], keep=keep)
        out.append(f)
    return cv, out


def refraction_mark_run(cells, frames=16):
    """The omen's motion layer: a head of light runs in from the wall through the centres and leaves the lit mark the
    ground keeps; the last frame matches the ground, then the clip clears."""
    cv = Canvas1(cells)
    pts, xl, xr, y_at = line_of(cv)
    RUN = 8
    out = []
    for i in range(frames):
        f = cv.frame()
        if i < RUN:
            t = A4.ease((i + 1) / RUN)
            hx = xl + (xr - xl) * t
            for x in range(int(xl), int(hx) + 1):
                y = y_at(x)
                F.px(f, x, y - 1, P["lite"]); F.px(f, x, y, WHITE); F.px(f, x, y + 1, P["lite"])
            hy = y_at(hx)
            A4.star(f, hx, hy, WHITE, 4)
            for k in range(2):
                A4.cluster(f, hx - (7 + 6 * k), hy - 2 + 3 * k, PRISM[k], P["seam"])
        else:
            keep = max(0.0, 1 - (i - RUN) / (frames - RUN - 1))
            for x in range(int(xl), int(xr) + 1):
                y = y_at(x)
                F.px(f, x, y, WHITE if i < RUN + 2 else P["hot"], keep=keep)
            for (cx, cy) in pts:
                if i < RUN + 3:
                    A4.star(f, cx, cy, WHITE, 4)
        out.append(f)
    return cv, out


def ground_mark(cells):
    """The omen's ground: the lit mark line, one painting across every seam (Heartglass, SAYO_BIBLE.md §5 exception)."""
    cv = Canvas1(cells)
    pts, xl, xr, y_at = line_of(cv)
    g = cv.frame()
    for x in range(int(xl), int(xr) + 1):
        y = y_at(x)
        F.px(g, x, y - 2, P["seam"]); F.px(g, x, y - 1, P["lite"]); F.px(g, x, y, P["hot"]); F.px(g, x, y + 1, P["lite"])
        F.px(g, x, y + 2, P["seam"])
    for (cx, cy) in pts:
        for dx in (-30, 0, 30):
            x = cx + dx
            F.px(g, x, y_at(x) - 3, WHITE); F.px(g, x, y_at(x) - 4, P["hot"])
    return cv, g


def ground_scar(cells, seed=7):
    """The Breaks' ground: the line cracked open, a black seam with a glass lip, broken stubs standing on it."""
    cv = Canvas1(cells)
    pts, xl, xr, y_at = line_of(cv)
    rnd = random.Random(seed)
    g = cv.frame()
    for x in range(int(xl), int(xr) + 1):
        y = y_at(x)
        F.px(g, x, y - 1, P["glint"]); F.px(g, x, y, P["deep"]); F.px(g, x, y + 1, P["deep"])
        F.px(g, x, y + 2 + ((x // 5) % 2), P["seam"])
    for x in range(int(xl) + 4, int(xr) - 3, 6):
        y = y_at(x)
        h = rnd.randint(2, 5)
        for k in range(h):
            F.px(g, x, y - 2 - k, P["body"] if k < h - 1 else P["hot"])
        F.px(g, x + 1, y - 2, P["lite"])
    return cv, g


def mirror(frames):
    return [f.transpose(Image.FLIP_LEFT_RIGHT) for f in frames]


def assets():
    out = []
    for side, cells in ROWS.items():
        mir = side == "R"
        cv, fr = refraction_break(cells)
        cv2, mr = refraction_mark_run(cells)
        _, gm = ground_mark(cells)
        _, gs = ground_scar(cells)
        if mir:
            fr, mr = mirror(fr), mirror(mr)
            gm, gs = gm.transpose(Image.FLIP_LEFT_RIGHT), gs.transpose(Image.FLIP_LEFT_RIGHT)
        for k in cells:
            col = k[0]
            kk = k   # the mirror is about the row's middle: every column keeps its place and parity
            s = side.lower()
            out.append(("ANIMATION", f"anim_moe_rbreak1_{s}{col}_r1.webp", cv.clip(kk, fr), f"Refraction Breaks (ratio 1), {side} {col}"))
            out.append(("ANIMATION", f"anim_moe_rmark1_{s}{col}_r1.webp", cv.clip(kk, mr), f"Refraction mark run (ratio 1), {side} {col}"))
            out.append(("STATIC", f"tile_moe_rmark_{s}{col}_r1.webp", cv.ground(kk, gm), f"Refraction mark ground, {side} {col}"))
            out.append(("STATIC", f"tile_moe_rscar_{s}{col}_r1.webp", cv.ground(kk, gs), f"Refraction scar ground, {side} {col}"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=F.EXPORTS)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rows = []
    for kind, name, data, note in assets():
        p = os.path.join(a.out, name)
        if kind == "ANIMATION":
            F.strip(data, margin=False).save(p, lossless=True, quality=100, method=6)
        else:
            data.save(p, lossless=True, quality=100, method=6)
        rows.append({"file": f"art/mother_of_echoes_fx/exports/{name}", "type": kind,
                     "frames": len(data) if kind == "ANIMATION" else 1, "speed": F.MS, "bytes": os.path.getsize(p),
                     "note": note})
    with open(os.path.join(a.out, "moe_fx_r1.json"), "w") as fh:
        json.dump({"source": "art/mother_of_echoes_fx/build_fx_r1.py", "geometry": "game main cb755375, clip h x h",
                   "assets": rows}, fh, indent=1)
        fh.write("\n")
    print(len(rows), "assets")


if __name__ == "__main__":
    main()
