#!/usr/bin/env python3
"""Isonade boss combat animations v1: eight battle effects (nine strips) drawn in code, plus battle-frame GIF previews.

    python3 build_isonade_anims.py            # writes the strips, previews/, isonade_anims_v1.json and README.md here

Offline art production only: no network, no uploads, no game requests. Pillow only (no NumPy).

Engine facts this follows (producing-tnr-art skill, references/combat_fx.md, and the Skyglass boss animation spec
docs/design/SKYGLASS_BOSS_ANIMATIONS.md in tnr-tools):
- ANIMATION asset = one vertical strip of square frames; `frames` and `speed` (ms per frame) fields; lossless WebP,
  real alpha, under the 460,800 byte ceiling. Director's standing rule: never a strip over 4096 px tall, so every
  strip here is at most 32 frames of 128 px.
- A clip is a square of tile.height x animationScale centred on its hex, drawn OVER the characters. Every strip here
  is drawn for animationScale 3 (the scale the Skyglass marks tg_heavy / tg_safe read at): inside a 128 px frame the
  hex footprint is about 85 x 43 px, centred.
- Battles fetch a 50 px-wide rendition of the whole strip, so shapes are bold and outlines thick (3 px at 128).
- Appear and loop of one action start on the same clock with the loop drawn on top; loops below are seamless (every
  moving part is periodic in the loop length) and marks share the 0.8 s beat (16 frames x 50 ms).
- Colour language: red = heavy hit (tg_heavy), green = lingers (tg_linger), cyan = safe / opening (tg_safe,
  anim_exposed). Body water uses blue-black only, so nobody reads it as a hazard.
Everything is drawn at 4x (512 px), reduced to 128 px, alpha stepped to four levels, colour-quantised, and given a
2 px clear margin (linear sampling bleeds between frames); RGB under clear pixels is filled from the nearest drawn
pixel.
"""
import json
import math
import os
import random
from collections import deque

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PREV = os.path.join(HERE, 'previews')
REPO = os.environ.get('TNR_REPO', '/home/user/tnr-tools')
SKY = os.path.join(REPO, 'art/skyglass_boss_fx/exports')
STILL = os.path.join(REPO, 'docs/design/celestial_dew_animation/battle_still_2026-10-24b.png')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

S = 128            # delivered frame size
SS = 4             # supersample
W = S * SS
MS = 50            # ms per frame (gameAsset.speed)
SCALE = 3          # animationScale every strip is drawn for
MAX_BYTES = 460_800
MAX_H = 4096
MAX_FRAMES = MAX_H // S   # 32
VERSION = 'v1'

# ------------------------------------------------------------------------------------------------ palette
INK = (10, 10, 16)
# body water: blue-black only
W0, W1, W2, W3, W4 = (12, 16, 29), (19, 27, 47), (29, 42, 68), (44, 63, 96), (70, 94, 128)
# the arms: wet black hide
A0, A1, A2, A3 = (7, 9, 15), (17, 22, 34), (40, 54, 76), (104, 128, 156)
BW0, BW1 = (72, 84, 100), (116, 128, 144)          # barnacles toned for the water
B0, B1 = (118, 120, 108), (170, 168, 150)          # barnacles out of the water
SK0, SK1 = (34, 43, 58), (22, 28, 40)              # suckers (low contrast: pale ones read as a ladder at 50 px)
# deck wood
D0, D1, D2, D3 = (56, 35, 21), (94, 63, 37), (138, 96, 56), (186, 142, 90)
# spray and foam (desaturated, never cyan)
F0, F1, F2, WH = (134, 150, 172), (200, 210, 224), (236, 241, 248), (255, 255, 255)
FLASH = (255, 250, 230)
# linger green (tg_linger family: #bedc3c, #77990d, #5f7b0a, #4d6408)
G0, G1, G2, G3, G4, G5, G6 = (18, 24, 8), (33, 44, 9), (77, 100, 8), (95, 123, 10), (119, 153, 13), (190, 220, 60), (238, 252, 150)
# skyglass cyan (tg_safe / anim_exposed family)
C0, C1, C2, C3, C4 = (4, 95, 190), (29, 184, 255), (110, 242, 255), (200, 250, 255), (242, 255, 255)
E0, E1 = (196, 202, 190), (242, 244, 234)          # sclera
T0, T1, T2, RU = (64, 72, 80), (116, 126, 136), (170, 180, 188), (136, 72, 40)   # tins


# ------------------------------------------------------------------------------------------------ drawing kit
def U(v):
    return v * SS


def new():
    return Image.new('RGBA', (W, W), (0, 0, 0, 0))


def rgba(c, a=255):
    return tuple(c) + (a,)


def ellipse(im, cx, cy, rx, ry, col, width=None):
    d = ImageDraw.Draw(im)
    box = [U(cx - rx), U(cy - ry), U(cx + rx), U(cy + ry)]
    if box[2] <= box[0] or box[3] <= box[1]:
        return im
    if width:
        d.ellipse(box, outline=rgba(col), width=max(1, int(U(width))))
    else:
        d.ellipse(box, fill=rgba(col))
    return im


def polygon(im, pts, col):
    ImageDraw.Draw(im).polygon([(U(x), U(y)) for x, y in pts], fill=rgba(col))
    return im


def line(im, pts, col, w):
    d = ImageDraw.Draw(im)
    d.line([(U(x), U(y)) for x, y in pts], fill=rgba(col), width=max(1, int(U(w))), joint='curve')
    r = w / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse([U(x - r), U(y - r), U(x + r), U(y + r)], fill=rgba(col))
    return im


def over(base, *layers):
    for l in layers:
        base.alpha_composite(l)
    return base


def clip(obj, mask):
    out = obj.copy()
    out.putalpha(ImageChops.multiply(obj.getchannel('A'), mask.getchannel('A')))
    return out


def alpha_mul(obj, k):
    out = obj.copy()
    out.putalpha(obj.getchannel('A').point(lambda v: int(v * k)))
    return out


def ink(obj, w=3.0, col=INK):
    """Ink outline of width w (128-px units) round the object's silhouette (ring only, never under it)."""
    a = obj.getchannel('A')
    d = a.filter(ImageFilter.GaussianBlur(U(w) / 1.86)).point(lambda v: 255 if v > 8 else 0)
    ring = ImageChops.subtract(d, a.point(lambda v: 255 if v > 0 else 0))
    out = Image.new('RGBA', (W, W), rgba(col, 0))
    out.putalpha(ring)
    out.alpha_composite(obj)
    return out


_NOISE = {}


def dissolve(obj, amount, seed=1):
    """Pixel dissolve (never a grey fade): amount 0 keeps all, 1 removes all. 1-px grain at the delivered size."""
    if amount <= 0:
        return obj
    if amount >= 1:
        return new()
    if seed not in _NOISE:
        rnd = random.Random(seed)
        n = Image.new('L', (S, S))
        n.putdata([rnd.randrange(256) for _ in range(S * S)])
        _NOISE[seed] = n.resize((W, W), Image.NEAREST)
    m = _NOISE[seed].point(lambda v: 255 if v >= amount * 256 else 0)
    out = obj.copy()
    out.putalpha(ImageChops.multiply(obj.getchannel('A'), m))
    return out


def bez(pts, n=40):
    """Bezier (quadratic or cubic) sampled at n points."""
    out = []
    for k in range(n):
        t = k / (n - 1)
        if len(pts) == 3:
            (x0, y0), (x1, y1), (x2, y2) = pts
            x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * x1 + t * t * x2
            y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * y1 + t * t * y2
        else:
            (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
            a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
            x = a * x0 + b * x1 + c * x2 + d * x3
            y = a * y0 + b * y1 + c * y2 + d * y3
        out.append((x, y))
    return out


def resample(path, step=0.5):
    out = [path[0]]
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / step))
        for k in range(1, n + 1):
            out.append((x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n))
    return out


def normals(path):
    out = []
    for k in range(len(path)):
        a, b = path[max(0, k - 1)], path[min(len(path) - 1, k + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        out.append((dy / L, -dx / L))
    # one consistent side: the shade side faces down-right
    sx = sum(n[0] + n[1] for n in out)
    if sx < 0:
        out = [(-x, -y) for x, y in out]
    return out


def tube(path, radius, col):
    """Union of discs along a path; radius(s) with s in 0..1."""
    im = new()
    d = ImageDraw.Draw(im)
    p = resample(path)
    n = len(p)
    for k, (x, y) in enumerate(p):
        r = radius(k / max(1, n - 1))
        if r <= 0:
            continue
        d.ellipse([U(x - r), U(y - r), U(x + r), U(y + r)], fill=rgba(col))
    return im


def arm(path, r0, r1, wet=True, barn=(B0, B1), suckers=False, seed=3, ink_w=3.0, spec=A3):
    """A cel-shaded wet black arm along `path`, tapering r0 -> r1, ink-outlined."""
    rad = lambda s: r0 + (r1 - r0) * s
    p = resample(path)
    nr = normals(p)
    base = tube(p, rad, A1)
    sh_path = [(x + nx * rad(k / len(p)) * 0.45, y + ny * rad(k / len(p)) * 0.45) for k, ((x, y), (nx, ny)) in enumerate(zip(p, nr))]
    hi_path = [(x - nx * rad(k / len(p)) * 0.5, y - ny * rad(k / len(p)) * 0.5) for k, ((x, y), (nx, ny)) in enumerate(zip(p, nr))]
    shade = clip(tube(sh_path, lambda s: rad(s) * 0.72, A0), base)
    hi = clip(tube(hi_path, lambda s: rad(s) * 0.26, A2), base)
    det = new()
    rnd = random.Random(seed)
    n = len(p)
    if wet:  # specular dashes on the highlight
        for k in range(int(n * 0.08), n, max(1, n // 7)):
            seg = hi_path[k:k + max(2, n // 18)]
            if len(seg) > 1:
                line(det, seg, spec, max(0.8, rad(k / n) * 0.16))
    if suckers:
        for k in range(int(n * 0.3), n - 2, max(1, n // 9)):
            (x, y), (nx, ny) = p[k], nr[k]
            r = rad(k / n)
            ellipse(det, x + nx * r * 0.62, y + ny * r * 0.62, r * 0.28 + 0.4, r * 0.2 + 0.3, SK0)
            ellipse(det, x + nx * r * 0.62, y + ny * r * 0.62, r * 0.12 + 0.2, r * 0.09 + 0.2, SK1)
    if barn:
        for k in range(int(n * 0.05), int(n * 0.7), max(1, n // 6)):
            (x, y), (nx, ny) = p[k], nr[k]
            r = rad(k / n)
            side = rnd.choice((-0.35, 0.1, 0.4))
            bx, by = x + nx * r * side + rnd.uniform(-1, 1), y + ny * r * side
            br = max(1.0, r * 0.22)
            ellipse(det, bx, by, br + 0.6, br + 0.6, INK)
            ellipse(det, bx, by, br, br, barn[0])
            ellipse(det, bx - br * 0.2, by - br * 0.25, br * 0.45, br * 0.45, barn[1])
    body = over(base, shade, hi, clip(det, base))
    return ink(body, ink_w)


def plank(cx, cy, length, width, ang, cols=(D1, D2, D3), seed=1, ink_w=2.0):
    """A broken plank / splinter: a long quad with jagged ends, a light edge and a grain line."""
    rnd = random.Random(seed)
    ca, sa = math.cos(ang), math.sin(ang)

    def P(u, v):
        return (cx + u * ca - v * sa, cy + u * sa + v * ca)
    L, Wd = length / 2, width / 2
    pts = [P(-L, -Wd), P(-L * 0.4, -Wd), P(L * 0.5, -Wd), P(L, -Wd * 0.3 + rnd.uniform(-0.6, 0.6)),
           P(L * 0.8, Wd * 0.2), P(L * 0.95, Wd), P(-L * 0.6, Wd), P(-L * 0.85, Wd * 0.1 + rnd.uniform(-0.5, 0.5))]
    im = new()
    polygon(im, pts, cols[0])
    hl = new()
    polygon(hl, [P(-L, -Wd), P(L * 0.5, -Wd), P(L * 0.45, -Wd * 0.2), P(-L, -Wd * 0.2)], cols[1])
    line(hl, [P(-L * 0.7, Wd * 0.25), P(L * 0.6, Wd * 0.25)], D0, max(0.6, width * 0.12))
    line(hl, [P(-L * 0.95, -Wd * 0.75), P(L * 0.35, -Wd * 0.75)], cols[2], max(0.6, width * 0.14))
    return ink(over(im, clip(hl, im)), ink_w)


def tin(cx, cy, ang, size=4.0, ink_w=1.6):
    """A ship's stores tin, tumbling."""
    ca, sa = math.cos(ang), math.sin(ang)

    def P(u, v):
        return (cx + u * ca - v * sa, cy + u * sa + v * ca)
    h, r = size * 1.2, size
    im = new()
    polygon(im, [P(-r, -h), P(r, -h), P(r, h), P(-r, h)], T1)
    band = new()
    polygon(band, [P(-r, -h * 0.3), P(r, -h * 0.3), P(r, h * 0.35), P(-r, h * 0.35)], RU)
    polygon(band, [P(-r * 0.75, -h), P(-r * 0.35, -h), P(-r * 0.35, h), P(-r * 0.75, h)], T2)
    polygon(band, [P(r * 0.5, -h), P(r, -h), P(r, h), P(r * 0.5, h)], T0)
    return ink(over(im, clip(band, im)), ink_w)


def drops(im, items, col, hi=None):
    for x, y, r in items:
        ellipse(im, x, y, r, r * 1.15, col)
        if hi and r > 1.6:
            ellipse(im, x - r * 0.3, y - r * 0.35, r * 0.4, r * 0.4, hi)
    return im


def pulse(i, period):
    return 0.5 + 0.5 * math.cos(2 * math.pi * i / period)


def wobble_ellipse(cx, cy, rx, ry, t, terms, n=110):
    pts = []
    for k in range(n):
        th = 2 * math.pi * k / n
        r = 1 + sum(a * math.sin(f * th + 2 * math.pi * m * t + ph) for a, f, m, ph in terms)
        pts.append((cx + rx * r * math.cos(th), cy + ry * r * math.sin(th)))
    return pts


def lerp(a, b, k):
    return a + (b - a) * k


def ease_in(k):
    return k * k


def ease_out(k):
    return 1 - (1 - k) ** 2


# ------------------------------------------------------------------------------------------------ 1. body water (loop)
def anim_body_water():
    """Churning black water with arm coils breaking the surface. Blue-black only. 32 frames = 1.6 s (two beats)."""
    N = 32
    coils = [dict(cx=42, cy=62, ph=0.0, dir=1, seed=11), dict(cx=88, cy=68, ph=0.5, dir=-1, seed=12),
             dict(cx=66, cy=55, ph=0.25, dir=1, seed=13, small=True)]
    frames = []
    for i in range(N):
        t = i / N
        pts = wobble_ellipse(64, 64, 43, 21, t, [(0.05, 3, 1, 0), (0.035, 5, -2, 1.3), (0.025, 8, 3, 2.1)])
        pool = polygon(new(), pts, W1)
        det = new()
        ellipse(det, 64, 66, 29, 12, W0)
        for k in range(3):  # three swirl arms, rotating 120 degrees per loop (seamless by symmetry)
            a0 = 2 * math.pi * (k / 3 + t / 3)
            arc = []
            for j in range(24):
                s = j / 23
                th = a0 + s * 2.5
                rr = 0.82 - 0.46 * s
                arc.append((64 + 43 * rr * math.cos(th), 65 + 21 * rr * math.sin(th)))
            line(det, arc, W2, 3.4)
            line(det, arc[2:12], W3, 1.4)
        for k in range(9):  # rim foam dashes riding round
            a0 = 2 * math.pi * (k / 9 + t / 9)
            dash = [(64 + 43 * 0.9 * math.cos(a0 + s * 0.32), 64 + 21 * 0.9 * math.sin(a0 + s * 0.32)) for s in (0, 0.5, 1)]
            line(det, dash, W3 if k % 2 else W4, 1.6)
        pool = over(pool, clip(det, pool))
        m = Image.new('L', (W, W), 255)
        ImageDraw.Draw(m).ellipse([U(64 - 35), U(65 - 15), U(64 + 35), U(65 + 15)], fill=118)
        pool.putalpha(ImageChops.multiply(pool.getchannel('A'), m))
        f = ink(pool, 2.4)
        for c in coils:
            u = (t - c['ph']) % 1.0
            life = 0.6
            sc = 0.7 if c.get('small') else 1.0
            if u < life:
                k = u / life
                h = math.sin(math.pi * k)
                x0 = c['cx'] + c['dir'] * 9 * (k - 0.5)
                span = (9 + 3 * h) * sc
                H = (3 + 16 * h) * sc
                cy = c['cy']
                path = bez([(x0 - span, cy + 2), (x0 - span * 0.9, cy - H * 1.3), (x0 + span * 0.9, cy - H * 1.3), (x0 + span, cy + 2)], 50)
                if c['dir'] < 0:
                    path = path[::-1]
                a = arm(path, 5.0 * sc, 3.2 * sc, barn=(BW0, BW1), seed=c['seed'], ink_w=2.6, spec=W4)
                cut = new()
                ImageDraw.Draw(cut).rectangle([0, 0, W, U(cy + 1.2)], fill=(0, 0, 0, 255))
                a = clip(a, cut)
                f.alpha_composite(a)
                fo = new()
                for sx in (-1, 1):  # foam breaking round each leg (front half only)
                    fx = x0 + sx * span
                    rx_, ry_ = 7.5 * sc, 2.6 * sc
                    arc = [(fx + rx_ * math.cos(a), cy + 1.5 + ry_ * math.sin(a)) for a in [math.pi * (0.05 + 0.9 * j / 10) for j in range(11)]]
                    line(fo, arc, W4, 1.3)
                f.alpha_composite(fo)
            else:
                v = (u - life) / (1 - life)
                rp = new()
                ellipse(rp, c['cx'] + c['dir'] * 4.5, c['cy'] + 1, (9 + 16 * v) * sc, (4 + 7 * v) * sc, W4, width=1.4)
                f.alpha_composite(dissolve(rp, v * 0.9, seed=c['seed']))
        frames.append(f)
    return frames


# ------------------------------------------------------------------------------------------------ 2. slam hit (appear)
def anim_slam():
    """A thick dark arm crashes down: white flash, splinters and spray rise, the arm hauls back. 14 frames, 0.7 s."""
    N = 14
    rnd = random.Random(21)
    splinters = [(64 + rnd.uniform(-9, 9), 60 + rnd.uniform(-3, 3), rnd.uniform(-3.4, 3.4), rnd.uniform(-12, -7.5),
                  rnd.uniform(0, math.pi), rnd.uniform(-0.6, 0.6), rnd.uniform(8, 13), k) for k in range(9)]
    spray = [(64 + rnd.uniform(-14, 14), 58, rnd.uniform(-3.0, 3.0), rnd.uniform(-15, -10), rnd.uniform(1.8, 3.6)) for _ in range(20)]
    tips = {0: (78, -4), 1: (73, 18), 2: (68, 42), 3: (65, 60), 4: (64, 63), 5: (64, 63), 6: (64, 63), 7: (65, 58),
            8: (68, 44), 9: (72, 24), 10: (76, 4)}

    def arm_at(i):
        tx, ty = tips[i]
        path = bez([(92, -40), (92, ty * 0.3 - 8), (tx + 6, ty - 14), (tx, ty)], 60)
        return arm(path, 15.5, 10.0, seed=22, suckers=True, barn=None, ink_w=3.4)
    frames = []
    for i in range(N):
        f = new()
        # shadow on the floor as the arm falls
        if i <= 3:
            sh = ellipse(new(), 64, 64, 14 + 5 * i, 6 + 2.4 * i, INK)
            f.alpha_composite(alpha_mul(sh, 0.55))
        # crater: broken boards and black water, stays then dissolves
        if i >= 4:
            cr = new()
            ellipse(cr, 64, 65, 24, 10.5, D0)
            ellipse(cr, 64, 65.5, 18, 7.5, W0)
            cr = ink(cr, 2.0)
            crk = random.Random(29)
            for k in range(7):  # jagged cracks split the boards
                a = 2 * math.pi * k / 7 + crk.uniform(-0.3, 0.3)
                L = crk.uniform(28, 36)
                mid = (64 + 0.65 * L * math.cos(a + 0.12), 65 + 0.65 * L * 0.45 * math.sin(a + 0.12))
                line(cr, [(64 + 18 * math.cos(a), 65 + 8 * math.sin(a)), mid, (64 + L * math.cos(a - 0.05), 65 + L * 0.45 * math.sin(a - 0.05))], INK, 1.1)
            f.alpha_composite(dissolve(cr, max(0, (i - 9) / 5), seed=23))
        # trailing smear on the fall
        if 1 <= i <= 3:
            f.alpha_composite(dissolve(arm_at(i - 1), 0.65, seed=25))
            sl = new()
            tx, ty = tips[i]
            for dx in (-9, -2, 6):
                line(sl, [(tx + dx + 6, ty - 34), (tx + dx + 2, ty - 12)], F0, 1.3)
            f.alpha_composite(sl)
        if i in tips:
            a = arm_at(i)
            if i >= 8:
                a = dissolve(a, (i - 7) / 4, seed=26)
            f.alpha_composite(a)
            if 4 <= i <= 6:  # the tip splays on the boards
                sp = ellipse(new(), 64, 64, 13, 4.5, A1)
                ellipse(sp, 62, 63, 7, 2, A2)
                f.alpha_composite(ink(sp, 2.4))
        # flash
        if i in (4, 5):
            fl = new()
            k = 1.0 if i == 4 else 0.6
            for r in range(10):
                a = 2 * math.pi * r / 10 + 0.15
                L = (58 if r % 2 else 40) * k
                polygon(fl, [(64 + 5 * math.cos(a + 1.57), 54 + 3 * math.sin(a + 1.57)),
                             (64 + L * math.cos(a), 54 + L * 0.8 * math.sin(a)),
                             (64 + 5 * math.cos(a - 1.57), 54 + 3 * math.sin(a - 1.57))], FLASH)
            ellipse(fl, 64, 58, 36 * k, 18 * k, FLASH)
            ellipse(fl, 64, 57, 24 * k, 12 * k, WH)
            polygon(fl, [(56, 58), (60, 14 + 20 * (1 - k)), (64, 4 + 20 * (1 - k)), (68, 14 + 20 * (1 - k)), (72, 58)], FLASH)
            polygon(fl, [(60, 58), (63, 16 + 20 * (1 - k)), (65, 16 + 20 * (1 - k)), (68, 58)], WH)
            f.alpha_composite(fl if i == 4 else dissolve(fl, 0.45, seed=24))
        # splinters and spray
        if i >= 5:
            tt = i - 4
            sp = new()
            dd = []
            for (x0, y0, vx, vy, a0, w0, L, k) in splinters:
                x, y = x0 + vx * tt * 1.6, y0 + vy * tt + 1.25 * tt * tt
                if y < 70:
                    sp.alpha_composite(plank(x, y, L, 3.2, a0 + w0 * tt, seed=k))
            for (x0, y0, vx, vy, r) in spray:
                x, y = x0 + vx * tt * 1.3, y0 + vy * tt + 1.3 * tt * tt
                if y < 72:
                    dd.append((x, y, r * (1 - 0.06 * tt)))
            wet = drops(new(), dd, F1, F2)
            sp = over(ink(wet, 1.4), sp)
            f.alpha_composite(dissolve(sp, max(0, (i - 9) / 5), seed=27))
        frames.append(f)
    return frames


# ------------------------------------------------------------------------------------------------ 3. brine pool (loop)
def anim_brine():
    """Green-black brine bubbling up through broken floorboards. tg_linger hue family. 24 frames = 1.2 s."""
    N = 24
    bubbles = [(42, 64, 0), (76, 58, 5), (60, 72, 10), (90, 67, 15), (50, 56, 19), (70, 63, 8), (36, 69, 13), (94, 60, 21)]
    stubs = [(25, 60, 0.12, 15), (103, 67, -0.1, 14), (44, 81, -0.18, 13), (86, 47, 0.16, 13)]
    floats = [(54, 59, 0.07, 20, 50), (82, 70, -0.05, 18, 51)]
    frames = []
    for i in range(N):
        t = i / N
        p = pulse(i, N)
        f = new()
        # broken board ends poking out under the brine's rim
        for k, (x, y, a, L) in enumerate(stubs):
            f.alpha_composite(plank(x, y, L, 5.0, a, seed=40 + k, ink_w=2.2))
        pts = wobble_ellipse(64, 64, 42, 20, t, [(0.05, 4, 1, 0.5), (0.03, 7, -1, 2.0), (0.02, 11, 2, 1.0)])
        pool = polygon(new(), pts, G2)
        det = new()
        ellipse(det, 64, 66, 32, 13.5, G1)
        ellipse(det, 64, 67, 23, 9, G0)
        for k, yy in enumerate((54, 62, 70, 78)):  # board seams under the brine
            line(det, [(14, yy + 2), (64, yy + (k % 2)), (114, yy - 1)], G0, 1.3)
        # sheen: brightest on the shared beat (frame 0)
        shc = G5 if p > 0.6 else G4
        arc = [(64 + 40 * 0.82 * math.cos(a), 64 + 19 * 0.82 * math.sin(a)) for a in [math.pi * (1.05 + 0.04 * k) for k in range(14)]]
        line(det, arc, shc, 2.6 + 0.8 * p)
        arc2 = [(64 + 40 * 0.7 * math.cos(a), 64 + 19 * 0.7 * math.sin(a)) for a in [math.pi * (1.7 + 0.035 * k) for k in range(9)]]
        line(det, arc2, G3, 1.6)
        rim = [(x, y) for x, y in pts]
        line(det, rim + rim[:1], G3 if p < 0.6 else G4, 3.0)
        # a slow swirl in the brine (one revolution of 3-fold symmetry per loop)
        for k in range(3):
            a0 = 2 * math.pi * (k / 3 + t / 3)
            sw = [(64 + 30 * (0.8 - 0.4 * s) * math.cos(a0 + s * 1.4), 66 + 13 * (0.8 - 0.4 * s) * math.sin(a0 + s * 1.4)) for s in [j / 9 for j in range(10)]]
            line(det, sw, G1, 1.2)
        pool = over(pool, clip(det, pool))
        m = Image.new('L', (W, W), 255)
        ImageDraw.Draw(m).ellipse([U(64 - 28), U(66 - 12), U(64 + 28), U(66 + 12)], fill=150)
        pool.putalpha(ImageChops.multiply(pool.getchannel('A'), m))
        f.alpha_composite(ink(pool, 2.6))
        for x, y, a, L, sd in floats:  # broken boards awash in the brine, bobbing with the pulse
            pl = plank(x, y + 0.6 * math.sin(2 * math.pi * t + sd), L, 6.0, a, seed=sd, ink_w=2.2)
            wet = new()
            polygon(wet, [(x - L, y + 0.5), (x + L, y + 0.5), (x + L, y + 6), (x - L, y + 6)], G1)
            f.alpha_composite(over(pl, alpha_mul(clip(wet, pl), 0.75)))
        bl = new()
        for bx, by, t0 in bubbles:
            k = (i - t0) % N
            if k < 7:
                r = 2.0 + 0.6 * k
                if k < 6:
                    ellipse(bl, bx, by - k * 0.4, r + 0.9, r * 0.8 + 0.9, INK)
                    ellipse(bl, bx, by - k * 0.4, r, r * 0.8, G3)
                    ellipse(bl, bx, by - k * 0.4, r, r * 0.8, G5, width=0.9)
                    ellipse(bl, bx - r * 0.35, by - k * 0.4 - r * 0.35, 0.8, 0.7, G6)
                else:  # pop: a ring of droplets
                    for a in range(6):
                        aa = 2 * math.pi * a / 6
                        ellipse(bl, bx + 5 * math.cos(aa), by - 2.4 + 2.5 * math.sin(aa), 1.1, 1.1, G6)
                    ellipse(bl, bx, by - 2.4, 4.6, 2.2, G5, width=0.9)
        f.alpha_composite(bl)
        frames.append(f)
    return frames


# ------------------------------------------------------------------------------------------------ 4. arm burst (appear)
def anim_arm_burst():
    """The deck heaves, bursts, and a Grasping Arm rises out of the hole. 16 frames, 0.8 s."""
    N = 16
    rnd = random.Random(31)
    shards = [(64 + rnd.uniform(-8, 8), 62, math.cos(a) * rnd.uniform(3.0, 4.6), rnd.uniform(-6.5, -3.5), rnd.uniform(0, 3),
               rnd.uniform(-0.5, 0.5), rnd.uniform(9, 14), k) for k, a in enumerate([j * 2 * math.pi / 8 + 0.2 for j in range(8)])]
    jets = [(64 + rnd.uniform(-8, 8), 62, rnd.uniform(-2, 2), rnd.uniform(-8, -5), rnd.uniform(1.6, 3.2)) for _ in range(14)]
    reach = {4: 12, 5: 28, 6: 44, 7: 56, 8: 63, 9: 66, 10: 67, 11: 67, 12: 66, 13: 66, 14: 66, 15: 66}
    frames = []
    for i in range(N):
        f = new()
        if i <= 2:  # the deck boards heave: each board snaps in the middle and its halves tilt up
            k = (i + 1) / 3
            gap = new()
            ellipse(gap, 64, 63, 4 + 8 * k, 3 + 9 * k, INK)
            f.alpha_composite(gap)
            for j, yy in enumerate((54, 61, 68, 75)):
                lift = (0.6, 1.0, 1.0, 0.6)[j] * k
                w = 22 - abs(j - 1.5) * 3
                for sgn in (-1, 1):
                    ang = sgn * 0.55 * lift
                    cx = 64 + sgn * (w / 2 * math.cos(ang) + 1 + 2 * lift)
                    cy = yy - 5 * lift - w / 2 * abs(math.sin(ang))
                    f.alpha_composite(plank(cx, cy, w, 5.2, ang, seed=60 + j * 2 + (sgn > 0), ink_w=2.0))
            cr = new()
            for j in range(6):
                a = 2 * math.pi * j / 6 + 0.25
                line(cr, [(64, 64), (64 + 30 * math.cos(a), 64 + 13 * math.sin(a))], INK, 1.2)
            f.alpha_composite(cr)
            dust = drops(new(), [(64 + 24 * math.cos(a), 60 + 9 * math.sin(a) - 6 * k, 1.5) for a in (0.3, 1.9, 3.3, 4.7, 5.6)], F0)
            f.alpha_composite(dust)
        if i >= 3:  # the hole: black water ringed with broken teeth of board
            h = new()
            for j in range(10):
                a = 2 * math.pi * j / 10
                polygon(h, [(64 + 20 * math.cos(a - 0.22), 65 + 9 * math.sin(a - 0.22)), (64 + 27 * math.cos(a), 65 + 12.5 * math.sin(a)),
                            (64 + 20 * math.cos(a + 0.22), 65 + 9 * math.sin(a + 0.22))], D2 if j % 2 else D1)
            ellipse(h, 64, 65, 21, 9.5, D0)
            ellipse(h, 64, 65.5, 17, 7.2, W0)
            ellipse(h, 64, 66.5, 12, 4.5, INK)
            h = ink(h, 2.2)
            f.alpha_composite(dissolve(h, max(0, (i - 12) / 4), seed=32))
        if i in (3, 4):
            fl = new()
            ellipse(fl, 64, 60, 30 if i == 3 else 20, 13 if i == 3 else 8, F2)
            f.alpha_composite(fl if i == 3 else dissolve(fl, 0.5, seed=33))
        if i in reach:
            L = reach[i]
            sway = 5 * math.sin((i - 4) * 0.7)
            path = bez([(64, 70), (62 - sway * 0.3, 70 - L * 0.45), (66 + sway, 70 - L * 0.85), (60 + sway * 1.4, 70 - L)], 60)
            if L > 40:  # the tip curls into a hook
                hx, hy = path[-1]
                path = path + bez([(hx, hy), (hx - 7, hy - 4), (hx - 9, hy + 3), (hx - 4, hy + 6)], 14)
            a = arm(path, 11.0, 2.4, suckers=True, seed=34)
            cut = new()  # the root stays in the hole
            ImageDraw.Draw(cut).rectangle([0, 0, W, U(67)], fill=(0, 0, 0, 255))
            ImageDraw.Draw(cut).ellipse([U(64 - 16), U(60), U(64 + 16), U(73)], fill=(0, 0, 0, 255))
            a = clip(a, cut)
            if i >= 13:
                a = dissolve(a, (i - 12) / 4, seed=35)
            f.alpha_composite(a)
        if i >= 3:
            tt = i - 3
            sp = new()
            for (x0, y0, vx, vy, a0, w0, L, k) in shards:
                x, y = x0 + vx * tt * 1.5, y0 + vy * tt + 0.7 * tt * tt
                if y < 74:
                    sp.alpha_composite(plank(x, y, L, 4.2, a0 + w0 * tt, seed=70 + k, ink_w=2.2))
            dd = [(x0 + vx * tt * 1.2, y0 + vy * tt + 0.85 * tt * tt, r) for (x0, y0, vx, vy, r) in jets if y0 + vy * tt + 0.85 * tt * tt < 72]
            wet = ink(drops(new(), dd, W3, W4), 1.4)
            f.alpha_composite(dissolve(over(wet, sp), max(0, (i - 11) / 5), seed=36))
        frames.append(f)
    return frames


# ------------------------------------------------------------------------------------------------ 5. arm lash (appear)
def anim_arm_lash():
    """A quick sideways swipe of the arm across the hex at chest height: a crescent smear, a hit spark and a spray of
    brine. 10 frames, 0.5 s."""
    N = 10
    piv = (2, 78)                     # where the arm swings from (its root runs off the left edge)
    TIPS = {0: (16, 30), 1: (42, 19), 2: (76, 21), 3: (104, 33), 4: (119, 52), 5: (108, 59), 6: (90, 64)}
    sweep = TIPS

    def tip(i):
        return TIPS[i]

    def track(last):
        pts = []
        for k in range(last):
            (x0, y0), (x1, y1) = TIPS[k], TIPS[k + 1]
            for s_ in range(5):
                u = s_ / 5
                pts.append((lerp(x0, x1, u), lerp(y0, y1, u) - 3 * math.sin(math.pi * u)))
        pts.append(TIPS[last])
        return pts
    rnd = random.Random(51)
    spray = [(rnd.uniform(1.2, 3.6), rnd.uniform(-3.5, 0.5), rnd.uniform(1.4, 2.8)) for _ in range(11)]

    def arm_at(i):
        tx, ty = tip(i)
        root = (-34, 84)
        path = bez([root, (piv[0], piv[1] + 2), (lerp(piv[0], tx, 0.55), lerp(piv[1], ty, 0.55) - 6), (tx, ty)], 60)
        return arm(path, 7.5, 2.4, seed=52, barn=None, ink_w=2.4)
    hit = tip(3)
    frames = []
    for i in range(N):
        f = new()
        if 1 <= i <= 6:  # the smear: a crescent swept by the arm since the wind-up
            last = min(i, 4)
            outer = track(last)
            inner = [(lerp(piv[0], x, 0.55), lerp(piv[1], y, 0.55)) for x, y in outer]
            if len(outer) > 2:
                sm = new()
                inner = [(lerp(piv[0], x, 0.72), lerp(piv[1], y, 0.72)) for x, y in outer]
                polygon(sm, outer + inner[::-1], F0)
                sm = dissolve(sm, 0.55, seed=57)
                line(sm, outer, F2, 3.0)
                line(sm, [(lerp(piv[0], x, 0.86), lerp(piv[1], y, 0.86)) for x, y in outer], F1, 1.4)
                f.alpha_composite(dissolve(ink(sm, 1.4), max(0, (i - 3) / 4), seed=53))
        a = arm_at(i if i in sweep else 6)
        if i >= 5:
            a = dissolve(a, (i - 4) / 4, seed=54)
        if i <= 6:
            f.alpha_composite(a)
        if i in (3, 4):  # the hit lands mid-hex, chest high
            fl = new()
            k = 1.0 if i == 3 else 0.6
            hx, hy = hit
            for r in range(8):
                aa = 2 * math.pi * r / 8
                L = (22 if r % 2 else 14) * k
                polygon(fl, [(hx + 2.5 * math.cos(aa + 1.57), hy + 2.5 * math.sin(aa + 1.57)), (hx + L * math.cos(aa), hy + L * 0.8 * math.sin(aa)),
                             (hx + 2.5 * math.cos(aa - 1.57), hy + 2.5 * math.sin(aa - 1.57))], FLASH)
            ellipse(fl, hx, hy, 7 * k, 6 * k, WH)
            f.alpha_composite(fl if i == 3 else dissolve(fl, 0.5, seed=55))
        if i >= 3:
            tt = i - 3
            hx, hy = hit
            dd = [(hx + vx * tt * 2.4, hy + vy * tt + 0.8 * tt * tt, r) for (vx, vy, r) in spray]
            wet = ink(drops(new(), dd, F1, F2), 1.3)
            f.alpha_composite(dissolve(wet, max(0, (i - 6) / 4), seed=56))
        frames.append(f)
    return frames


# ------------------------------------------------------------------------------------------------ 6. black water surge
def anim_surge():
    """A wall of black water rises from the floor to head height, curls, and crashes down, churning tins and
    splinters; then drains. A little wider than the hex, so neighbouring hexes join into one wave while a safe hex
    beside it stays clear. 24 frames, 1.2 s."""
    N = 24
    tops = [62, 57, 51, 45, 39, 33, 28, 25, 23, 22, 22, 23, 26, 34, 45, 55, 62, 64, 64, 64, 64, 64, 64, 64]
    HW = 47   # half width of the wall (the hex is about 43)

    def top_at(x, top, i):
        s_ = min(1.0, abs(x - 64) / HW) ** 12   # flat top, steep sides: a wall, never a round mound
        return lerp(top, 63, s_) + 2.0 * math.sin(x * 0.16 + i * 0.9) * (1 - s_)
    rnd = random.Random(61)
    debris = [('tin', 38, 0.55, 0.3, 0.35), ('tin', 80, 0.72, 1.4, -0.4), ('tin', 98, 0.35, 2.2, 0.3),
              ('pl', 56, 0.78, 0.5, 0.45), ('pl', 28, 0.4, 1.1, -0.4)]
    frames = []
    for i in range(N):
        f = new()
        top = tops[i]
        rising = i <= 12
        if i <= 15:
            hgt = 64 - top
            body = new()
            pts = []
            for k in range(41):
                x = 64 - HW + 2 * HW * k / 40
                pts.append((x, top_at(x, top, i)))
            bottom = [(x, 64 + 20 * math.sqrt(max(0, 1 - ((x - 64) / HW) ** 2))) for x in [64 + HW - 2 * HW * k / 40 for k in range(41)]]
            polygon(body, pts + bottom, W1)
            bands = new()
            polygon(bands, [(x, y + hgt * 0.5) for x, y in pts] + [(x, y + hgt * 0.02) for x, y in reversed(pts)], W2)
            polygon(bands, [(x, y + hgt * 0.22) for x, y in pts] + [(x, y - 2) for x, y in reversed(pts)], W3)
            line(bands, bottom, W0, 3.0)
            for k in range(6):  # curling streaks of current, climbing with the water
                x0 = 26 + k * 15 + 4 * math.sin(i * 0.6 + k)
                y0 = top + hgt * (0.3 + 0.08 * (k % 3))
                arc = bez([(x0, y0 + hgt * 0.45), (x0 - 6, y0 + hgt * 0.2), (x0 + 2, y0), (x0 + 8, y0 + 2)], 12)
                line(bands, arc, W3 if k % 2 else W1, 1.5)
            body = over(body, clip(bands, body))
            if i >= 5:  # the crest: rolling foam lobes riding the lip, spray thrown ahead of it
                cr = new()
                lip = [(x, y) for x, y in pts]
                line(cr, lip, F0, 3.0)
                big = 1.0 if (rising and i >= 8) or not rising else 0.6
                for k in range(6):
                    x = 23 + k * 16.5 + 5 * ((i * 0.35 + k * 0.5) % 1)
                    yt = top_at(x, top, i)
                    r = (3.4 + 1.6 * ((k * 7) % 3) / 2) * big
                    ellipse(cr, x, yt - r * 0.3, r, r * 0.85, F1)
                    ellipse(cr, x - r * 0.3, yt - r * 0.55, r * 0.45, r * 0.4, F2)
                if 7 <= i <= 12:
                    rs = random.Random(64 + i)
                    drops(cr, [(rs.uniform(24, 104), top - rs.uniform(3, 10), rs.uniform(1.2, 2.2)) for _ in range(6)], F1, F2)
                body = over(body, cr)
            f.alpha_composite(dissolve(ink(body, 3.0), 0.5 if i == 15 else 0, seed=65))
            # debris carried in the water
            dl = new()
            for kind, x, frac, ph, spin in debris:
                y = 64 - hgt * frac + 2 * math.sin(i * 0.8 + ph)
                if y > 64 - 2 or y < top + 4:
                    continue
                xx = x + 2 * math.sin(i * 0.5 + ph)
                ang = ph + spin * i
                dl.alpha_composite(tin(xx, y, ang) if kind == 'tin' else plank(xx, y, 11, 3.4, ang, seed=int(ph * 10)))
            f.alpha_composite(dl)
        if 13 <= i <= 19:  # the crash: spray crown and plumes thrown up as it falls
            tt = i - 13
            sp = new()
            dd = []
            for k in range(16):
                a = math.pi * (0.05 + 0.9 * k / 15)
                vx = math.cos(a) * 4.0
                vy = -math.sin(a) * 6.5 - 1.5
                x = 64 + math.cos(a) * 32 + vx * tt
                y = 64 + vy * tt + 0.95 * tt * tt
                if y < 74:
                    dd.append((x, y, 2.8 - 0.25 * tt))
            drops(sp, dd, F1, F2)
            if tt <= 3:  # rounded plumes of spray where the wall hits the floor (no spikes: nothing tooth-like)
                for k in range(7):
                    x = 24 + 80 * k / 6 + 3 * math.sin(k * 1.7)
                    hh = (13 if k % 2 else 8) * (1 - tt / 4) + 2
                    ellipse(sp, x, 62 - hh * 0.55, 5.5, hh * 0.6, F1)
                    ellipse(sp, x - 1.5, 62 - hh * 0.8, 2.4, 2.2, F2)
                    ellipse(sp, x + 1, 62 - hh * 1.15, 1.8, 1.8, F1)
                ellipse(sp, 64, 63, 45, 5, F1)
            sp = ink(sp, 1.5)
            f.alpha_composite(dissolve(sp, max(0, (tt - 3) / 4), seed=62))
            # tossed debris
            dl = new()
            for kind, x, frac, ph, spin in debris:
                y = 60 - 7 * tt + 1.4 * tt * tt * 0.6 + frac * 4
                x2 = x + (x - 64) * 0.08 * tt
                if y < 70:
                    ang = ph + spin * (i + tt * 2)
                    dl.alpha_composite(tin(x2, y, ang) if kind == 'tin' else plank(x2, y, 11, 3.4, ang, seed=int(ph * 10)))
            f.alpha_composite(dl)
        if i >= 15:  # the floor runs with it, then drains
            v = (i - 15) / (N - 15)
            dr = new()
            ellipse(dr, 64, 65, 46 - 10 * v, 21 - 5 * v, W1)
            ellipse(dr, 64, 65, 46 - 10 * v, 21 - 5 * v, F0, width=1.6)
            for k in range(6):
                a = 2 * math.pi * k / 6 + v
                ellipse(dr, 64 + (30 - 7 * v) * math.cos(a), 65 + (12 - 3 * v) * math.sin(a), 6, 2, F1)
            dr = ink(dr, 2.2)
            dl = new()
            for kind, x, frac, ph, spin in debris[::2]:
                dl.alpha_composite(tin(x * 0.8 + 13, 66 + 6 * math.sin(ph * 3), ph) if kind == 'tin' else plank(x * 0.8 + 13, 66 + 6 * math.sin(ph * 3), 11, 3.4, ph, seed=int(ph * 10)))
            g = over(dr, dl)
            f2 = dissolve(g, max(0, v * 1.15 - 0.15), seed=63)
            f2.alpha_composite(f)
            f = f2
        frames.append(f)
    return frames


# ------------------------------------------------------------------------------------------------ 7. open eye (loop)
def anim_eye():
    """Isonade's great pale eye, open, ringed with pale cyan light: hit it now. 16 frames = 0.8 s (the shared beat)."""
    N = 16
    ex, ey = 64, 42
    frames = []
    for i in range(N):
        t = i / N
        p = pulse(i, N)
        f = new()
        # ground ring of light, pulsing on the beat, plus a ring that spreads and dissolves each beat
        gr = new()
        rx = 41 + 3 * p
        ellipse(gr, 64, 64, rx, rx / 2, C1, width=5.0)
        ellipse(gr, 64, 64, rx - 1.6, rx / 2 - 0.8, C3 if p > 0.5 else C2, width=2.2)
        for k in range(8):  # light ticks on the ring
            a = 2 * math.pi * (k / 8 + t / 8)
            ellipse(gr, 64 + rx * math.cos(a), 64 + rx / 2 * math.sin(a), 1.8, 1.8, C4)
        f.alpha_composite(ink(gr, 1.5))
        wv = new()
        r2 = 34 + 26 * t
        ellipse(wv, 64, 64, r2, r2 / 2, C2, width=2.2)
        f.alpha_composite(dissolve(wv, t * 0.95, seed=71))
        # halo behind the eye
        ha = new()
        hr = 40 + 2.5 * p
        ellipse(ha, ex, ey, hr, hr * 0.62, C1, width=3.6)
        ellipse(ha, ex, ey, hr - 1.6, hr * 0.62 - 1.0, C3, width=1.6)
        for k in range(10):
            a = 2 * math.pi * k / 10 + 0.3
            L = 6 + 3 * p if k % 2 else 3 + 2 * p
            line(ha, [(ex + (hr + 2) * math.cos(a), ey + (hr + 2) * 0.62 * math.sin(a)),
                      (ex + (hr + 2 + L) * math.cos(a), ey + (hr + 2 + L) * 0.62 * math.sin(a))], C2, 1.6)
        f.alpha_composite(ink(ha, 1.4))
        # the lids: barnacled black hide round an almond opening
        lid = new()
        outer = wobble_ellipse(ex, ey + 1, 37, 20, 0, [(0.07, 3, 0, 0.4), (0.05, 5, 0, 1.9), (0.03, 9, 0, 0.7)], n=80)
        polygon(lid, outer, A1)
        lsh = new()
        polygon(lsh, [(x + 1, y + 5) for x, y in outer], A0)
        lid = over(lid, clip(lsh, lid))
        fold = new()  # heavy folds of hide over and under the eye
        line(fold, [(ex - 30 + 60 * k / 16, ey - 15.5 - 3.5 * math.sin(math.pi * k / 16)) for k in range(17)], A2, 1.6)
        line(fold, [(ex - 22 + 44 * k / 12, ey + 15.5 + 2.5 * math.sin(math.pi * k / 12)) for k in range(13)], A2, 1.3)
        line(fold, [(ex - 18 + 30 * k / 8, ey - 18.5 - 1.5 * math.sin(math.pi * k / 8)) for k in range(9)], A3, 0.9)
        lid = over(lid, clip(fold, lid))
        rnd = random.Random(72)
        for k in range(13):  # barnacle clusters on the hide (never on the opening)
            while True:
                a = rnd.uniform(0, 2 * math.pi)
                rr = rnd.uniform(0.84, 0.97)
                if not (0.2 < math.sin(a) < 0.9 and abs(math.cos(a)) < 0.3):
                    break
            bx, by = ex + 36 * rr * math.cos(a), ey + 1 + 19.5 * rr * math.sin(a)
            br = rnd.uniform(1.2, 2.6)
            ellipse(lid, bx, by, br + 0.6, br + 0.6, INK)
            ellipse(lid, bx, by, br, br, B0)
            ellipse(lid, bx - 0.4, by - 0.5, br * 0.45, br * 0.45, B1)
        # the opening
        def almond(w, h):
            return [(ex + w * math.cos(a), ey + h * math.sin(a) * abs(math.sin(a)) ** 0.3) for a in [2 * math.pi * k / 60 for k in range(60)]]
        opening = polygon(new(), almond(27, 14.5), E1)
        osh = new()
        polygon(osh, [(x, y - 4.5) for x, y in almond(27, 14.5)], E0)
        ins = new()
        drift = 2.2 * math.sin(2 * math.pi * t)
        ix, iy = ex + drift, ey + 0.5
        ellipse(ins, ix, iy, 11.5, 11.5, C1)
        ellipse(ins, ix, iy, 9.5, 9.5, C2)
        ellipse(ins, ix - 1.5, iy - 1.8, 5.5, 5.5, C3)
        ellipse(ins, ix, iy, 11.5, 11.5, C0, width=1.3)
        pw = 2.0 + 0.9 * (1 - p)  # the slit pupil breathes with the beat
        polygon(ins, [(ix, iy - 10), (ix + pw, iy), (ix, iy + 10), (ix - pw, iy)], INK)
        ellipse(ins, ix - 4, iy - 4.5, 2.0, 1.6, WH)
        ellipse(ins, ix + 4.5, iy + 4, 0.9, 0.9, C4)
        opening = over(opening, clip(osh, opening), clip(ins, opening))
        ol = new()
        line(ol, almond(27, 14.5) + almond(27, 14.5)[:1], INK, 2.6)
        lid = over(lid, opening, ol)
        f.alpha_composite(ink(lid, 3.0))
        # motes of light rising from the ring
        mo = new()
        for mx, t0 in ((22, 0), (104, 5), (40, 10), (88, 13)):
            k = (i - t0) % N
            if k < 11:
                ellipse(mo, mx, 66 - k * 3.4, 1.6, 1.6, C3 if k < 7 else C2)
        f.alpha_composite(ink(mo, 1.0))
        frames.append(f)
    return frames


# ------------------------------------------------------------------------------------------------ 8a. bite of the ship
def anim_bite():
    """Hull planks rip inward toward the beast and are crunched; a shockwave spreads; rot starts to seep.
    20 frames, 1.0 s. Pair with the rot drip loop (8b) on the same effect: appear = bite, static = drip."""
    N = 20
    rnd = random.Random(81)
    planks = []
    for k in range(7):
        a = 2 * math.pi * k / 7 + 0.35
        planks.append((64 + 70 * math.cos(a), 50 + 44 * math.sin(a), rnd.uniform(22, 28), a + rnd.uniform(-0.4, 0.4), rnd.uniform(-0.5, 0.5), k))
    shards = [(64, 50, math.cos(a) * rnd.uniform(3.5, 5.5), math.sin(a) * rnd.uniform(2.0, 3.2) - 2.5, rnd.uniform(0, 3), rnd.uniform(5, 9), k)
              for k, a in enumerate([j * 2 * math.pi / 10 for j in range(10)])]
    frames = []
    for i in range(N):
        f = new()
        if i <= 6:  # suction ring contracting on the floor
            v = i / 6
            sr = new()
            r = 60 - 44 * v
            ellipse(sr, 64, 64, r, r / 2, W3, width=2.6)
            ellipse(sr, 64, 64, r - 4, r / 2 - 2, F0, width=1.0)
            f.alpha_composite(ink(sr, 1.4))
        if i <= 7:  # planks torn off the hull fly inward, accelerating
            v = ease_in(min(1, i / 7))
            pl = new()
            sl = new()
            for (x0, y0, L, a0, w0, k) in planks:
                x, y = lerp(x0, 64, v), lerp(y0, 50, v)
                if i >= 1:
                    px_, py_ = lerp(x0, 64, ease_in((i - 1) / 7)), lerp(y0, 50, ease_in((i - 1) / 7))
                    line(sl, [(px_ - (x - px_) * 0.6, py_ - (y - py_) * 0.6), (x, y)], F0, 1.3)
                pl.alpha_composite(plank(x, y, L * (1 - 0.35 * v), 7.0, a0 + w0 * i, seed=90 + k, ink_w=2.4))
            f.alpha_composite(sl)
            f.alpha_composite(pl)
        if 6 <= i <= 9:  # the bite: jaws of black hide snap shut on the planks
            k = min(1, (i - 6) / 2)
            jw = new()
            gap = 16 * (1 - k)
            for sgn in (-1, 1):
                cy = 50 + sgn * (gap + 5)
                pts = [(64 + 32 * math.cos(a), cy + sgn * 12 * math.sin(a) * (1 + 0.12 * math.sin(5 * a))) for a in [math.pi * j / 24 for j in range(25)]]
                polygon(jw, pts, A1)
                line(jw, [(64 + 26 * math.cos(a), cy + sgn * 8 * math.sin(a)) for a in [math.pi * (0.15 + 0.7 * j / 12) for j in range(13)]], A2, 1.4)
                for j, tl in enumerate((5, 7, 4, 8, 6, 4, 7, 5)):  # uneven pale teeth along the bite edge
                    tx = 38 + j * 7.4
                    polygon(jw, [(tx - 2.6, cy), (tx + 2.6, cy), (tx + 0.5, cy - sgn * tl)], B1)
            jw = ink(jw, 2.6)
            if i == 9:
                jw = dissolve(jw, 0.6, seed=82)
            f.alpha_composite(jw)
        if i in (8, 9):
            fl = new()
            kk = 1.0 if i == 8 else 0.55
            for r in range(10):
                a = 2 * math.pi * r / 10
                L = (34 if r % 2 else 22) * kk
                polygon(fl, [(64 + 3 * math.cos(a + 1.57), 50 + 3 * math.sin(a + 1.57)), (64 + L * math.cos(a), 50 + L * 0.7 * math.sin(a)),
                             (64 + 3 * math.cos(a - 1.57), 50 + 3 * math.sin(a - 1.57))], FLASH)
            f.alpha_composite(fl if i == 8 else dissolve(fl, 0.5, seed=83))
        if i >= 8:  # shockwave rings spread over the floor
            for d0, wdt, col in ((8, 6.5, F1), (10, 3.6, F0)):
                if i >= d0:
                    v = (i - d0) / (N - d0)
                    sw = new()
                    r = 18 + 50 * ease_out(v)
                    ellipse(sw, 64, 64, r, r / 2, col, width=wdt * (1 - 0.5 * v))
                    sw = ink(sw, 1.4)
                    f.alpha_composite(dissolve(sw, v * 1.05, seed=84 + d0))
            tt = i - 8
            sp = new()
            for (x0, y0, vx, vy, a0, L, k) in shards:
                x, y = x0 + vx * tt * 1.4, y0 + vy * tt + 0.55 * tt * tt
                if y < 72:
                    sp.alpha_composite(plank(x, y, L, 3.0, a0 + 0.4 * tt, seed=110 + k, ink_w=1.8))
            f.alpha_composite(dissolve(sp, max(0, (i - 13) / 6), seed=85))
        if i >= 12:  # rot starts to seep where the bite landed
            v = (i - 12) / (N - 12)
            ro = new()
            ellipse(ro, 64, 66, 10 + 12 * v, 4 + 5 * v, G2)
            ellipse(ro, 61, 65, 6 + 7 * v, 2 + 2.4 * v, G4)
            for bx, b0 in ((58, 0.2), (70, 0.5), (64, 0.8)):
                if v > b0:
                    ellipse(ro, bx, 64 - 2 * (v - b0), 1.6, 1.3, G5)
            f.alpha_composite(ink(ro, 2.0))
        frames.append(f)
    return frames


# ------------------------------------------------------------------------------------------------ 8b. rot drip (loop)
def anim_rot_drip():
    """Rot-green ooze runs down the beast's rim and drips to the floor, for the rest of the fight. Drawn round the
    portrait's edge (circle centre about (64, 43), radius 21 in the frame) so the avatar stays readable.
    24 frames = 1.2 s."""
    N = 24
    cx, cy, R = 64, 43, 22
    drips = [(188, 0), (352, 6), (168, 12), (12, 18), (200, 9), (340, 3)]   # angle on the rim (deg), phase: the sides only,
    # so no drop falls across the portrait
    frames = []
    for i in range(N):
        t = i / N
        p = pulse(i, N)
        f = new()
        pd = new()  # puddle under the beast
        ellipse(pd, 64, 66, 22 + 2 * p, 6 + 0.6 * p, G1)
        ellipse(pd, 60, 65.5, 12, 3, G3)
        f.alpha_composite(ink(pd, 1.8))
        ooze = new()
        rnd = random.Random(91)
        for a0, a1 in ((146, 228), (312, 394)):  # blobby rot crusted on both shoulders of the rim
            for a in range(a0, a1 + 1, 4):
                ra = math.radians(a)
                r = 1.6 + 1.6 * abs(math.sin(a * 0.11)) + rnd.uniform(0, 0.6)
                ellipse(ooze, cx + (R + 0.5) * math.cos(ra), cy + (R + 0.5) * math.sin(ra), r, r, G2)
            for a in range(a0 + 6, a1 - 5, 10):
                ra = math.radians(a)
                ellipse(ooze, cx + (R + 0.2) * math.cos(ra) - 0.4, cy + (R + 0.2) * math.sin(ra) - 0.7, 1.1, 0.9, G4 if p > 0.5 else G3)
            for a, L in ((a0 + 14, 4), (a0 + 40, 3), (a1 - 30, 5)):  # short hanging tongues of ooze
                ra = math.radians(a)
                x0, y0 = cx + (R + 0.5) * math.cos(ra), cy + (R + 0.5) * math.sin(ra)
                Lk = L * (0.8 + 0.2 * math.sin(2 * math.pi * t + a))
                line(ooze, [(x0, y0), (x0, y0 + Lk)], G2, 2.2)
                ellipse(ooze, x0, y0 + Lk, 1.4, 1.6, G3)
        for a, ph in drips:
            u = (t - ph / N) % 1.0
            ra = math.radians(a)
            x0, y0 = cx + (R + 3.5) * math.cos(ra), cy + R * math.sin(ra) + 6
            if u < 0.5:  # the drip swells and lengthens
                L = 2 + 12 * (u / 0.5)
                line(ooze, [(x0, y0), (x0, y0 + L)], G2, 2.6)
                ellipse(ooze, x0, y0 + L, 2.2 + 1.2 * (u / 0.5), 2.4 + 1.2 * (u / 0.5), G3)
                ellipse(ooze, x0 - 0.7, y0 + L - 0.8, 0.7, 0.7, G5)
            elif u < 0.82:  # it falls
                k = (u - 0.5) / 0.32
                line(ooze, [(x0, y0), (x0, y0 + 4)], G2, 2.2)
                yd = y0 + 14 + (66 - y0 - 14) * k * k
                ellipse(ooze, x0, yd, 2.0, 2.8, G3)
                ellipse(ooze, x0 - 0.6, yd - 0.9, 0.6, 0.6, G5)
            else:  # splat
                k = (u - 0.82) / 0.18
                line(ooze, [(x0, y0), (x0, y0 + 3)], G2, 2.2)
                ellipse(ooze, x0, 66, 3 + 3 * k, 1.2 + 0.8 * k, G4)
                for s in (-1, 1):
                    ellipse(ooze, x0 + s * (3 + 3 * k), 64.5 - 2 * k, 0.9, 0.9, G5)
        f.alpha_composite(ink(ooze, 2.0))
        mo = new()  # rot motes rising
        for mx, t0 in ((34, 0), (96, 8), (52, 16), (80, 4)):
            k = (i - t0) % N
            if k < 14:
                ellipse(mo, mx + math.sin(k * 0.6) * 1.5, 62 - k * 2.6, 1.3, 1.3, G5 if k < 9 else G3)
        f.alpha_composite(mo)
        frames.append(f)
    return frames


# ------------------------------------------------------------------------------------------------ finishing
def step_alpha(v):
    return 0 if v < 48 else 110 if v < 128 else 184 if v < 208 else 255


def finish_frame(img):
    small = img.convert('RGBa').resize((S, S), Image.LANCZOS).convert('RGBA')
    a = small.getchannel('A').point(step_alpha)
    d = ImageDraw.Draw(a)
    d.rectangle([0, 0, S - 1, 1], fill=0)
    d.rectangle([0, S - 2, S - 1, S - 1], fill=0)
    d.rectangle([0, 0, 1, S - 1], fill=0)
    d.rectangle([S - 2, 0, S - 1, S - 1], fill=0)
    small.putalpha(a)
    return small


def bleed(fr):
    """RGB under clear pixels from the nearest drawn pixel (BFS), so linear sampling never pulls in a dark fringe."""
    px = fr.load()
    w, h = fr.size
    seen = bytearray(w * h)
    q = deque()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > 0:
                seen[y * w + x] = 1
                q.append((x, y))
    if not q:
        for y in range(h):
            for x in range(w):
                px[x, y] = INK + (0,)
        return fr
    while q:
        x, y = q.popleft()
        r, g, b, _ = px[x, y]
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                seen[ny * w + nx] = 1
                px[nx, ny] = (r, g, b, 0)
                q.append((nx, ny))
    return fr


def export(name, frames, colors=96):
    assert 1 <= len(frames) <= MAX_FRAMES, (name, len(frames))
    fr = [bleed(finish_frame(f)) for f in frames]
    strip = Image.new('RGBA', (S, S * len(fr)))
    for k, f in enumerate(fr):
        strip.paste(f, (0, k * S))
    alpha = strip.getchannel('A')
    rgb = strip.convert('RGB').quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    strip = rgb.convert('RGBA')
    strip.putalpha(alpha)
    path = os.path.join(HERE, name)
    strip.save(path, 'WEBP', lossless=True, quality=100, method=6, exact=True)
    size = os.path.getsize(path)
    h = strip.height
    assert h <= MAX_H, (name, h)
    assert size < MAX_BYTES, (name, size)
    # read back: frame geometry the engine derives (h / frames must equal width)
    rb = Image.open(path)
    assert rb.size == (S, S * len(frames)) and rb.mode == 'RGBA', (name, rb.size, rb.mode)
    return dict(file=name, frames=len(frames), frame_px=S, height_px=h, bytes=size)


# ------------------------------------------------------------------------------------------------ previews on the battle still
# Battle still and hex geometry: docs/design/skyglass_boss_fx/ship_preview.py (pixi renderer, theninjarpg@3314d122):
# hex 132 x 66 px on the still; a clip is tile.height x animationScale = 66 x 3 = 198 px, centred on its hex, drawn over
# the characters. Strips are first reduced to the 50 px-wide rendition the battle CDN serves, then magnified
# bilinearly, as the GPU does, so the previews show the delivered softness.
HX, HY, COL, ROW, HH = 311.0, 225.5, 99.0, 66.0, 66.0
K = round(HH * SCALE)


def centre(q, r):
    return HX + COL * q, HY + ROW * r - (ROW / 2 if q % 2 else 0)


def neighbours(q, r):
    if q % 2:
        return [(q, r - 1), (q, r + 1), (q - 1, r - 1), (q - 1, r), (q + 1, r - 1), (q + 1, r)]
    return [(q, r - 1), (q, r + 1), (q - 1, r), (q - 1, r + 1), (q + 1, r), (q + 1, r + 1)]


def game_frames(path):
    s = Image.open(path).convert('RGBA')
    n = s.height // s.width
    r = s.resize((50, 50 * n), Image.BILINEAR)
    return [r.crop((0, k * 50, 50, (k + 1) * 50)).resize((K, K), Image.BILINEAR) for k in range(n)]


def load_scene():
    bg = Image.open(STILL).convert('RGBA')
    m = Image.new('L', bg.size, 0)
    d = ImageDraw.Draw(m)
    d.ellipse([278, 158.7, 344, 224.7], fill=255)
    d.rectangle([277, 144, 344, 162], fill=255)
    d.ellipse([300, 223.3, 322, 243.3], fill=255)
    box = m.getbbox()
    tok = bg.crop(box)
    tok.putalpha(m.crop(box))
    off = (box[0] - HX, box[1] - HY)
    # boss placeholder token: same frame, the portrait replaced by a dark sea-beast stand-in (no Isonade avatar yet)
    boss = tok.copy()
    pd = ImageDraw.Draw(boss)
    ccx, ccy = 311 - box[0], 191.7 - box[1]
    pd.ellipse([ccx - 27, ccy - 27, ccx + 27, ccy + 27], fill=(16, 22, 36, 255))
    pd.ellipse([ccx - 13, ccy - 6, ccx + 13, ccy + 6], fill=(214, 218, 208, 255))
    pd.ellipse([ccx - 4, ccy - 4, ccx + 4, ccy + 4], fill=(110, 200, 230, 255))
    pd.ellipse([ccx - 1.5, ccy - 4, ccx + 1.5, ccy + 4], fill=(10, 10, 16, 255))
    arm_tok = tok.copy()
    pd = ImageDraw.Draw(arm_tok)
    pd.ellipse([ccx - 27, ccy - 27, ccx + 27, ccy + 27], fill=(22, 28, 42, 255))
    pd.line([(ccx - 8, ccy + 20), (ccx + 2, ccy), (ccx - 2, ccy - 14), (ccx + 9, ccy - 18)], fill=(60, 76, 100, 255), width=8)
    return bg, tok, boss, arm_tok, off


BOSS = (-1, -1)
BODY = neighbours(*BOSS)
PLAYERS = [(0, -1), (1, 0)]          # plus the player baked into the still at (0, 0)
ARENA = [(q, r) for q in range(-3, 4) for r in range(-3, 3)
         if 30 < centre(q, r)[0] < 590 and 20 < centre(q, r)[1] < 300 and (q, r) != BOSS]
SAFE = [(2, -1), (-1, 1)]            # the two crates


def render_gif(out, phases, scene, tokens, font, persist=()):
    """phases: list of (caption, ticks, layers); a layer = (frames, cells, start_tick, loop, z).
    persist: layers drawn under every phase on a global clock (e.g. the body water all fight)."""
    bg, tok, boss, arm_tok, off = scene
    imgs = []
    g = 0
    for caption, ticks, layers in phases:
        for tk in range(ticks):
            c = bg.copy()
            for kind, cell in sorted(tokens, key=lambda kc: centre(*kc[1])[1]):
                x, y = centre(*cell)
                c.alpha_composite({'p': tok, 'b': boss, 'a': arm_tok}[kind], (int(x + off[0]), int(y + off[1])))
            active = []
            for frs, cells, start, loop, z in list(persist):
                active.append((z, frs[(g - start) % len(frs)], cells))
            for frs, cells, start, loop, z in layers:
                k = tk - start
                if k < 0:
                    continue
                if loop:
                    active.append((z, frs[k % len(frs)], cells))
                elif k < len(frs):
                    active.append((z, frs[k], cells))
            for z, fr, cells in sorted(active, key=lambda a: a[0]):
                for cell in sorted(cells, key=lambda cc: centre(*cc)[1]):
                    x, y = centre(*cell)
                    c.alpha_composite(fr, (int(x - K / 2), int(y - K / 2)))
            fr_ = Image.new('RGB', (c.width, c.height + 24), (16, 18, 24))
            fr_.paste(c.convert('RGB'), (0, 24))
            ImageDraw.Draw(fr_).text((8, 4), f'{caption}   t={tk * MS} ms', font=font, fill=(236, 238, 242))
            imgs.append(fr_)
            g += 1
    # one shared palette, no dithering: small files and no shimmering grain on the background
    sample = imgs[::max(1, len(imgs) // 12)]
    mont = Image.new('RGB', (sample[0].width, sample[0].height * len(sample)))
    for k, im in enumerate(sample):
        mont.paste(im, (0, k * im.height))
    pal = mont.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [im.quantize(palette=pal, dither=Image.Dither.NONE) for im in imgs]
    q[0].save(out, save_all=True, append_images=q[1:], duration=MS, loop=0, optimize=True)
    return dict(file=os.path.relpath(out, HERE), frames=len(imgs), bytes=os.path.getsize(out))


def previews(built):
    os.makedirs(PREV, exist_ok=True)
    font = ImageFont.truetype(FONT, 13)
    scene = load_scene()
    F = {k: game_frames(os.path.join(HERE, v['file'])) for k, v in built.items()}
    tg_heavy = game_frames(os.path.join(SKY, 'anim_tg_heavy_v2.webp'))
    tg_safe = game_frames(os.path.join(SKY, 'anim_tg_safe_v2.webp'))
    toks = [('b', BOSS)] + [('p', c) for c in PLAYERS]
    body = [(F['body_water'], BODY, 0, True, 0)]
    out = []
    once = lambda key, cells, extra=8: (len(F[key]) + extra, [(F[key], cells, 0, False, 2)])
    P = lambda name, *a, **kw: out.append(render_gif(os.path.join(PREV, name), *a, font=font, **kw))

    P('isonade_body_water_v1.gif', [('Body water: 6 hexes round Isonade, all fight (static loop, scale 3)', 96, body)], scene, toks)
    slam_cells = [(0, -1), (1, 0), (1, -1)]
    n, L = once('slam', slam_cells)
    P('isonade_slam_v1.gif', [('Slam hit on 3 marked hexes (appear, scale 3)', n, L)], scene, toks, persist=body)
    P('isonade_brine_v1.gif', [('Brine pool, lingering 3 rounds (static loop, scale 3)', 72, [(F['brine'], slam_cells, 0, True, 1)])],
      scene, toks, persist=body)
    burst_cells = [(1, -2), (-2, 0)]
    n, L = once('arm_burst', burst_cells, 10)
    P('isonade_arm_burst_v1.gif', [('Grasping Arm bursts up on 2 hexes (summon appear, scale 3)', n, L)], scene, toks, persist=body)
    ARM = (1, -1)
    n, L = once('arm_lash', neighbours(*ARM), 10)
    P('isonade_arm_lash_v1.gif', [('Arm lash round the Grasping Arm hex (appear, scale 3)', n, L)], scene, toks + [('a', ARM)], persist=body)
    n, L = once('surge', [c for c in ARENA if c not in SAFE], 10)
    P('isonade_surge_v1.gif', [('Black Water surge on every hex but the crates (appear, scale 3)', n, L)], scene, toks, persist=body)
    P('isonade_eye_v1.gif', [('Open eye: 1-round punish window on Isonade (static loop, scale 3)', 64, [(F['eye'], [BOSS], 0, True, 3)])],
      scene, toks, persist=body)
    nb = len(F['bite'])
    P('isonade_bite_v1.gif', [('Bite of the ship at half health: bite (appear) + rot drip (static, on top)', nb + 48,
                               [(F['bite'], [BOSS], 0, False, 2), (F['rot_drip'], [BOSS], 0, True, 3)])], scene, toks, persist=body)
    # combined sequences
    rows = [(q, 0) for q in range(-3, 4)] + [(q, 1) for q in range(-3, 4)]
    rows = [c for c in rows if c in ARENA]
    P('isonade_seq_slam_v1.gif', [
        ('Turn 1: Slam marked on two rows (existing tg_heavy)', 32, [(tg_heavy, rows, 0, True, 1)]),
        ('Turn 2: Slam lands; brine pools stay (slam appear + brine loop on top, one clock)', len(F['slam']) + 48,
         [(F['slam'], rows, 0, False, 2), (F['brine'], rows, 0, True, 3)]),
    ], scene, toks, persist=body)
    P('isonade_seq_slam_brine_after_v1.gif', [
        ('ALTERNATIVE: Slam marked (tg_heavy)', 32, [(tg_heavy, rows, 0, True, 1)]),
        ('ALTERNATIVE: brine starts after the slam (later action / ground image), not on its clock', len(F['slam']) + 48,
         [(F['slam'], rows, 0, False, 2), (F['brine'], rows, len(F['slam']) - 4, True, 1)]),
    ], scene, toks, persist=body)
    unsafe = [c for c in ARENA if c not in SAFE]
    P('isonade_seq_black_water_v1.gif', [
        ('Turn 1: Black Water marked everywhere but the crates (tg_heavy + tg_safe)', 32,
         [(tg_heavy, unsafe, 0, True, 1), (tg_safe, SAFE, 0, True, 1)]),
        ('Turn 2: Black Water surge (safe marks shown still standing)', len(F['surge']) + 10,
         [(tg_safe, SAFE, 0, True, 1), (F['surge'], unsafe, 0, False, 2)]),
    ], scene, toks, persist=body)
    return out


def qc_sheet(name, path):
    """Every frame on dark, mid and bright grounds (spill and chewed edges hide on one ground)."""
    s = Image.open(path).convert('RGBA')
    n = s.height // s.width
    cols = min(n, 16)
    rows_ = math.ceil(n / cols)
    sheet = Image.new('RGB', (cols * S, rows_ * S * 3), (0, 0, 0))
    for gi, gcol in enumerate(((18, 20, 26), (110, 112, 116), (232, 232, 228))):
        for k in range(n):
            tile = Image.new('RGBA', (S, S), gcol + (255,))
            tile.alpha_composite(s.crop((0, k * S, S, (k + 1) * S)))
            sheet.paste(tile.convert('RGB'), ((k % cols) * S, (gi * rows_ + k // cols) * S))
    p = os.path.join(PREV, f'qc_{name}.png')
    sheet.save(p, optimize=True)
    return os.path.relpath(p, HERE)


# ------------------------------------------------------------------------------------------------ catalogue
CATALOGUE = [
    # key, builder, filename, slot, loops, use, shows
    ('body_water', anim_body_water, 'anim_isonade_body_water_v1.webp', 'staticAnimation', True,
     'Body water ground effect on the 6 hexes round Isonade, from round 1, all fight',
     'Black water churning with wet arm coils breaking the surface; blue-black only, no red/green/cyan'),
    ('slam', anim_slam, 'anim_isonade_slam_v1.webp', 'appearAnimation', False,
     'Slam damage effect on each hex marked red the turn before',
     'A thick dark arm crashes down: white flash, splinters and spray thrown up, crater; the arm hauls back up'),
    ('brine', anim_brine, 'anim_isonade_brine_v1.webp', 'staticAnimation', True,
     'Brine pool lingering ground effect (3 rounds), created by the Slam',
     'Green-black brine bubbling up through broken floorboards; tg_linger green family, pulse peaks on frame 0'),
    ('arm_burst', anim_arm_burst, 'anim_isonade_arm_burst_v1.webp', 'appearAnimation', False,
     'Summon flourish where a Grasping Arm appears',
     'The deck heaves and bursts, black water spouts, an arm rises and hooks, then dissolves to leave the summon'),
    ('arm_lash', anim_arm_lash, 'anim_isonade_arm_lash_v1.webp', 'appearAnimation', False,
     "Grasping Arm's attack damage effect on the hexes round its own hex",
     'A quick sideways swipe of the arm with a motion smear, hit spark and brine spray'),
    ('surge', anim_surge, 'anim_isonade_surge_v1.webp', 'appearAnimation', False,
     'Black Water damage effect on every hex but the safe crates, the turn after the room goes red',
     'A flat-topped wall of black water a little wider than the hex rises to head height with rolling foam, tins and '
     'splinters churning, crashes down in rounded spray plumes, then drains (rises and falls; no teeth, no mound, unlike Maw)'),
    ('eye', anim_eye, 'anim_isonade_eye_v1.webp', 'staticAnimation', True,
     "Open eye: buff/visual on Isonade's own hex for the 1-round punish window",
     'The great pale eye, open, iris drifting, slit pupil breathing, in a pale cyan halo; a cyan ring of light '
     'pulses on the floor and spreads each beat'),
    ('bite', anim_bite, 'anim_isonade_bite_v1.webp', 'appearAnimation', False,
     'Bite of the Ship at half health (appear of the same effect that carries the rot drip)',
     'Hull planks rip inward, jaws of black hide snap on them, white flash, shockwave rings spread, rot starts to seep'),
    ('rot_drip', anim_rot_drip, 'anim_isonade_rot_drip_v1.webp', 'staticAnimation', True,
     'Rot drip aura on Isonade for the rest of the fight (static of the Bite effect)',
     'Rot-green ooze on the rim of the portrait drips to a puddle on the floor; motes rise'),
]


def readme(built, prev, qcs):
    L = ['# Isonade combat animations v1', '',
         'Eight animations for the Isonade boss fight (nine strips: Bite of the Ship is a one-shot bite plus a looping '
         'drip). Built in code, offline: no live-game requests, nothing uploaded.', '',
         'Rebuild: `python3 build_isonade_anims.py` (Pillow only; reads the Skyglass strips and the battle still from '
         'the tnr-tools checkout at `$TNR_REPO`, default `/home/user/tnr-tools`).', '',
         '## Strips', '',
         'All: vertical strip of square 128 px frames, lossless WebP with real alpha, `speed` 50 ms per frame, drawn for '
         '`animationScale` 3. Limits checked by the build (it fails otherwise): height <= 4096 px (<= 32 frames of 128 px) '
         'and file < 460,800 bytes.', '',
         '| File | Engine slot | Frames | Frame | Height px | Bytes | Loops | Length | What it shows |',
         '|---|---|---|---|---|---|---|---|---|']
    for key, _, fn, slot, loops, use, shows in CATALOGUE:
        b = built[key]
        L.append(f"| `{fn}` | `{slot}`: {use} | {b['frames']} | 128 x 128 | {b['height_px']} | {b['bytes']:,} | "
                 f"{'yes' if loops else 'no'} | {b['frames'] * MS} ms | {shows} |")
    L += ['', 'Shared cadence: the eye loop is the 0.8 s beat (16 frames); body water 1.6 s (two beats); brine and drip '
          '1.2 s (as tg_linger). Every loop is seamless: each moving part is periodic in the loop length.', '',
          '## Previews (`previews/`)', '',
          'Battle frame: `docs/design/celestial_dew_animation/battle_still_2026-10-24b.png` (the real battle still the '
          'Skyglass previews use; hex 132 x 66 px), clips at tile.height x 3 = 198 px centred on their hexes and drawn over '
          'the characters, as the pixi renderer does. Each strip is first reduced to the 50 px-wide rendition the battle '
          'CDN serves and magnified bilinearly, so the softness shown is the delivered softness. The body water runs under '
          'every preview (it stays all fight). Tokens: the player token cut from the still (three players), a dark '
          'placeholder token with a pale eye for Isonade, and a dark placeholder for the Grasping Arm.', '']
    for p in prev:
        L.append(f"- `{p['file']}` ({p['frames']} frames at 50 ms, {p['bytes']:,} bytes)")
    L += ['', 'QC sheets (every frame on dark, mid and bright grounds): ' + ', '.join(f'`{q}`' for q in qcs), '',
          '## Weak spots, guesses, and what is not done', '',
          '- **Slam vs brine (the main open decision).** If the brine pool is a loop created by the same action as the '
          'slam, the engine starts it at the strike and draws it ON TOP of the slam (every loop above every appear). On a '
          'marked field the brine then hides the arms\' lower halves, the white flash and the crater: see '
          '`isonade_seq_slam_v1.gif`. `isonade_seq_slam_brine_after_v1.gif` shows the same slam with the brine starting '
          'as the slam ends, which reads far better. Ways to get there: the brine on a later action, or the brine pool as '
          'a still `staticAssetPath` ground image (drawn under characters and clips) with only the bubbles as a loop. '
          'Not built: it changes how the effect is authored, which is a content decision.',
          '- **Filled ground loops cover the head of the character in the hex below.** Clips draw over characters, and '
          'a pool that fills its hex reaches into the portrait of whoever stands one row in front (tg_heavy avoids this '
          'by being a hollow ring). Body water and brine keep a translucent middle (alpha 118 and 150) so the portrait '
          'shows through, but a dark rim still crosses it. The same `staticAssetPath` route would put them under the '
          'characters.',
          '- **Frame size.** Existing Skyglass strips are 50 px (tg_*) or 150 px (AN01-AN09) frames. These are 128 px per '
          'the brief, so 32 frames fit the 4096 px rule. Outline weight (3 px at 128, about 1 px at the 50 px battle '
          'rendition), hex footprint (about 85 x 43 px at scale 3, the size tg_heavy reads at) and palette follow the '
          'Skyglass set; the drawing is smooth cel-shaded, not the 50 px pixel grid of tg_*.',
          '- **animationScale 3 is a recommendation**, not checked against live records (none exist yet).',
          '- **Black Water vs Maw.** Maw (`anim_maw_v1`) is a round teal mound with a dark mouth and teeth. The surge is a '
          'flat-topped, steep-sided navy wall slightly wider than the hex (so neighbours join into one flood) with rolling '
          'white-grey foam lobes, tins and splinters; it falls back with rounded spray plumes (no spikes) and drains. '
          'At battle size the field reads as a room flooding; individual tiles still show as stacked blocks, which is '
          'the weakest look of the set.',
          '- **Safe crates during the surge.** Walls on the hexes in front of a crate rise over the crate hex\'s lower '
          'half; the tg_safe star stays visible above them. The preview keeps tg_safe standing through the surge; whether '
          'the mark survives into the detonation round, and the draw order between the two effects, were not checked.',
          '- **Open eye is one looping strip** (eye open the whole time). An eye-opening appear was not built: a loop of '
          'the same action draws on top of it, so the opening would be hidden.',
          '- **Bite + drip** are meant as the appear and static of one effect (the drip draws on top from the strike, as '
          'previewed). The drip runs on both sides of the portrait circle, whose place (centre about 21 px above the hex '
          'centre in the frame, radius 21) is measured from the player token on the still; an Isonade avatar framed '
          'differently may need the drip nudged. The rot drip is green (as the brief asks; the Core Horror enrage aura '
          'AN04 set that precedent), so it shares the linger colour.',
          '- **Arm lash** plays the same swipe, left to right, on every hex round the arm (the engine cannot vary it per '
          'hex). It is mostly a pale slash with a thin dark arm tip so six copies do not bury the characters.',
          '- **Backgrounds and tokens.** The only real battle frame in the repo is the snowy Celestial Dew still; there is '
          'no flooded-storeroom battle background yet, so contrast on a dark wooden floor is untested. Isonade and the '
          'Grasping Arm have no avatars: their tokens are placeholders.',
          '- **Byte counts** are the files as they sit on disk. This file store appends a C2PA provenance chunk (about '
          '5.8 KB) to each image after it is written, so a file is a few KB larger than the encoder\'s output; both are '
          'in `isonade_anims_v1.json`. Every file is far under the 460,800-byte ceiling either way.',
          '- **Preflight:** `artpreflight.py --type ANIMATION` passes width, aspect and bytes but flags `soft_edges` on '
          'every strip (7-40% partial-alpha pixels against a 5% ceiling). That gate targets chroma-keyed art; here the '
          'partial alpha is deliberate (stepped anti-aliased edges, translucent pool middles, dissolves). The approved '
          'tg_linger_v2 and tg_safe_v2 strips fail the same gate (25% and 53%).',
          '- **Not done:** no upload, no gameAsset rows, no manifest, no check in a real browser battle (the skill asks for '
          'one hidden test strip in a real battle before trusting fine detail). Filenames are new (`_v1`); a corrected '
          'strip needs a fresh name.']
    with open(os.path.join(HERE, 'README.md'), 'w') as fh:
        fh.write('\n'.join(L) + '\n')


def main():
    built = {}
    for key, fn_build, fn, slot, loops, use, shows in CATALOGUE:
        info = export(fn, fn_build())
        info.update(slot=slot, loops=loops, speed_ms=MS, duration_ms=info['frames'] * MS, animation_scale=SCALE, use=use)
        built[key] = info
        print(f"{fn}: {info['frames']} frames, {info['height_px']} px, {info['bytes']} bytes")
    os.makedirs(PREV, exist_ok=True)
    qcs = [qc_sheet(k, os.path.join(HERE, v['file'])) for k, v in built.items()]
    prev = previews(built)
    for p in prev:
        print(p)
    for k, v in built.items():  # the filestore appends a C2PA provenance chunk after the write: re-check on disk
        v['bytes_encoded'] = v['bytes']
        v['bytes'] = os.path.getsize(os.path.join(HERE, v['file']))
        assert v['bytes'] < MAX_BYTES, (k, v['bytes'])
        print(f"{v['file']}: {v['height_px']} px tall, {v['bytes']} bytes on disk ({v['bytes_encoded']} as encoded)")
    with open(os.path.join(HERE, 'isonade_anims_v1.json'), 'w') as fh:
        json.dump({'builder': 'build_isonade_anims.py', 'speed_unit': 'ms per frame (gameAsset.speed)',
                   'limits': {'max_height_px': MAX_H, 'max_bytes_exclusive': MAX_BYTES},
                   'strips': built, 'previews': prev}, fh, indent=1)
    readme(built, prev, qcs)


if __name__ == '__main__':
    main()
