#!/usr/bin/env python3
"""FCF v18 MASTER: the whole discharge drawn in board space first, with no engine constraints (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v18/master_v18.py

Director: "lightning forks more ... I keep saying draw the whole effect first and then create the individual
animations." So this is the target the engine cut must match, drawn as one picture over the real board.

The discharge is one branching tree grown from the user, the way a stepped leader grows (and the way a Lichtenberg
figure looks): five to seven main channels leave the body; every channel steps outward with a jittered heading and
keeps forking (children leave at 20-50 degrees, shorter and thinner), until the branches reach the edge of the
area (range 4). Thickness and brightness follow how much tree hangs off each segment, so the trunks read as a few
big bolts and the fine forks fill the area.
Timing (real-lightning order): the leader tree gropes outward over ~300 ms, faint, each branch at its own pace, with
pauses; then the return stroke lights the WHOLE tree at once (the white-hot impact frame); then the fine branches go
out and the trunks flicker down the same channels twice; then it dies. The area darkens like a night sky around it.
Writes master_fcf_v18.gif and master_stills_v18.png.
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v13"))
sys.path.insert(0, os.path.join(HERE, "..", "v10"))
import board_v10 as BV  # noqa: E402
import fxlight as L  # noqa: E402

COLS, ROWS, CASTER, RADIUS, PX = 12, 8, (5, 4), 4, 2
STACK = 0.25
HS = 360 / (COLS - STACK * (COLS - 1))
TW, TH = HS * PX, HS * 0.5 * PX
W, H = int(360 * PX), int((ROWS + 0.5) * TH)
TILES = {(c, r): (c * TW * (1 - STACK) + TW / 2, r * TH + TH / 2 + (TH / 2 if c % 2 else 0))
         for c in range(COLS) for r in range(ROWS)}
AREA = [k for k in TILES if k != CASTER and BV.dist(k, CASTER) <= RADIUS]
CX, CY = TILES[CASTER]
SRC = (CX, CY - 0.4 * TH)                    # the bolts leave from the body
SS = 3


def in_area(p):
    """Inside the area's footprint: within half a tile of some area tile centre (on the 2:1 board)."""
    for k in AREA + [CASTER]:
        x, y = TILES[k]
        if ((p[0] - x) / (TW * 0.5)) ** 2 + ((p[1] - y) / (TH * 0.55)) ** 2 <= 1:
            return True
    return False


class Seg:
    __slots__ = ("a", "b", "t0", "t1", "parent", "children", "weight", "depth")

    def __init__(self, a, b, t0, t1, parent, depth):
        self.a, self.b, self.t0, self.t1, self.parent, self.depth = a, b, t0, t1, parent, depth
        self.children, self.weight = [], 1


def grow(seed):
    """Branches step outward with a pull toward 'away from the user', fork with decaying odds, and stop at the edge
    of the area or when their life runs out, so the tree reads as a few trunks with forks, not a scribble."""
    rnd = random.Random(seed)
    segs = []
    tips = []
    n_main = 7
    for k in range(n_main):
        ang = k * 2 * math.pi / n_main + rnd.uniform(-0.4, 0.4)
        tips.append((SRC, ang, 0.0, None, 0, rnd.uniform(0.85, 1.2), 60, 0))
    step = TH * 0.3
    while tips:
        p, ang, t, parent, depth, speed, life, gen = tips.pop()
        out = math.atan2((p[1] - SRC[1]) / 0.62, p[0] - SRC[0]) if depth > 0 else ang
        d_ang = (out - ang + math.pi) % (2 * math.pi) - math.pi
        ang += rnd.gauss(0, 0.38) + 0.25 * d_ang
        q = (p[0] + math.cos(ang) * step, p[1] + math.sin(ang) * step * 0.62)
        if not in_area(q) or life <= 0:
            continue
        dt = step / 0.8 / speed
        if rnd.random() < 0.06:
            dt += rnd.uniform(8, 30)
        s = Seg(p, q, t, t + dt, parent, depth)
        if parent:
            parent.children.append(s)
        segs.append(s)
        tips.append((q, ang, t + dt, s, depth + 1, speed, life - 1, gen))
        if depth > 1 and rnd.random() < 0.24 * (0.72 ** gen):
            tips.append((q, ang + rnd.choice((-1, 1)) * rnd.uniform(0.4, 0.9), t + dt, s, depth + 1,
                         speed * rnd.uniform(0.85, 1.05), int(life * rnd.uniform(0.3, 0.7)), gen + 1))
    for s in reversed(segs):
        if s.parent:
            s.parent.weight += s.weight
    return segs


def frame(segs, t, t_stroke, night):
    base = Image.new("RGBA", (W, H), (52, 64, 44, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in TILES.values():
        d.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                   (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], outline=(255, 255, 255, 30))
    for k, col in (((8, 3), (96, 58, 52, 255)), ((2, 5), (96, 58, 52, 255)), ((6, 7), (96, 58, 52, 255)),
                   (CASTER, (52, 50, 66, 255))):
        x, y = TILES[k]
        feet, top = y + 0.4 * TH, y - 1.2 * TH
        d.ellipse((x - TW * 0.16, feet - TH * 0.09, x + TW * 0.16, feet + TH * 0.09), fill=(0, 0, 0, 80))
        d.rounded_rectangle((x - TW * 0.085, top + TW * 0.16, x + TW * 0.085, feet - 3), radius=6, fill=col)
        d.ellipse((x - TW * 0.1, top, x + TW * 0.1, top + TW * 0.2), fill=col)
    if night:
        dark = Image.new("RGBA", (W, H), (10, 6, 22, 0))
        m = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(m)
        for k in AREA + [CASTER]:
            x, y = TILES[k]
            md.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                        (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], fill=255)
        dark.putalpha(m.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * night * 0.62)))
        base.alpha_composite(dark)
    light = Image.new("L", (W * SS, H * SS), 0)
    dl = ImageDraw.Draw(light)
    maxw = max(s.weight for s in segs)

    def seg_line(s, w, v, frac=1.0):
        b = (s.a[0] + (s.b[0] - s.a[0]) * frac, s.a[1] + (s.b[1] - s.a[1]) * frac)
        dl.line([(s.a[0] * SS, s.a[1] * SS), (b[0] * SS, b[1] * SS)], fill=int(max(0, min(255, v))),
                width=max(1, int(w * SS)))
    phase = t - t_stroke
    for s in segs:
        order = (s.weight / maxw) ** 0.45            # 1 for a trunk, small for a twig
        if phase < 0:                                 # leader: faint, growing, the newest steps brightest
            if t < s.t0:
                continue
            frac = min(1.0, (t - s.t0) / max(1, s.t1 - s.t0))
            seg_line(s, 0.5 + 0.8 * order, 35 + 45 * order + (110 if t - s.t1 < 25 else 0), frac)   # faint; the tips glow
        elif phase < 50:                              # return stroke: the whole tree, white-hot
            seg_line(s, 0.8 + 5.5 * order, 170 + 85 * order)
        elif phase < 100:
            if order > 0.25:
                seg_line(s, 0.6 + 3.5 * order, 120 + 100 * order)
        elif phase < 150:
            if order > 0.4:
                seg_line(s, 0.8, 50 * order)
        elif phase < 200 or 250 <= phase < 300:       # two restrikes down the trunks
            if order > 0.35:
                seg_line(s, 0.6 + 4.0 * order, 140 + 110 * order)
        elif phase < 450:
            if order > 0.5:
                seg_line(s, 0.8, max(0, 60 - (phase - 300) / 3) * order)
    tight = light.filter(ImageFilter.GaussianBlur(1.5 * SS)).point(lambda v: min(255, int(v * 1.6)))
    mid = light.filter(ImageFilter.GaussianBlur(5 * SS)).point(lambda v: min(255, int(v * 1.4)))
    wide = light.filter(ImageFilter.GaussianBlur(14 * SS)).point(lambda v: min(255, int(v * 1.2)))
    inten = ImageChops.lighter(ImageChops.lighter(light, tight), ImageChops.lighter(mid, wide))
    inten = inten.resize((W, H), Image.LANCZOS)
    rgb = Image.merge("RGB", [inten.point([c[i] for c in L.STORM_LUT]) for i in range(3)])
    alpha = inten.point(lambda v: min(255, int(255 * (v / 255) ** 0.75 * 1.1)))
    lt = rgb.convert("RGBA")
    lt.putalpha(alpha)
    base.alpha_composite(lt)
    return base.convert("RGB")


def main():
    segs = grow(23)
    t_stroke = max(s.t1 for s in segs) + 20
    print(len(segs), "segments; leader done at", round(t_stroke), "ms")
    shots = []
    step = 25
    for t in range(-150, int(t_stroke) + 550, step):
        night = max(0.0, min(1.0, (t + 150) / 150)) * (1.0 if t < t_stroke + 300 else max(0, 1 - (t - t_stroke - 300) / 250))
        shots.append(frame(segs, max(0, t), t_stroke, night))
    shots[0].save(os.path.join(HERE, "master_fcf_v18.gif"), save_all=True, append_images=shots[1:], duration=step,
                  loop=0, optimize=True)
    times = [int(t_stroke * 0.35), int(t_stroke * 0.8), int(t_stroke) + 10, int(t_stroke) + 75, int(t_stroke) + 260]
    pick = [next(i for i, tt in enumerate(range(-150, int(t_stroke) + 550, step)) if tt >= x) for x in times]
    sheet = Image.new("RGB", (W, H * len(pick)))
    for i, p in enumerate(pick):
        sheet.paste(shots[min(p, len(shots) - 1)], (0, i * H))
    sheet.save(os.path.join(HERE, "master_stills_v18.png"))
    import pickle
    with open(os.path.join(HERE, "master_tree.pkl"), "wb") as f:
        pickle.dump([(s.a, s.b, s.t0, s.t1, s.weight, segs.index(s.parent) if s.parent else -1) for s in segs], f)


if __name__ == "__main__":
    main()
