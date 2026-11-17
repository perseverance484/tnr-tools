#!/usr/bin/env python3
"""Forbidden Chakra Fury v5: a tessellating field plus one caster clip (director 2026-11-16).

    python3 art/jutsu_icons/forbidden_chakra_fury/animation/build_v5.py [--size 192] [--board] [--final]

Why v5: the spiral (AOE_SPIRAL_SHOOT, range 4) is centred on the CASTER and stamps the recoil's art on up to 60
tiles at the same instant. v4 played a 3x clip per tile, so neighbours overdrew into mush. Director rulings:
- the art stays on the recoil tag (no mosaic of visual tags: they clutter the jutsu stats screens);
- ONE extra visual tag is allowed, on the caster (COORDINATES, origin CASTER, offset 0,0), for a special effect that
  feeds the field.

Design:
- FIELD (recoil appear/static/disappear + ground image), animationScale 2.0: the clip is exactly one hex wide, the
  hex sits in the middle band of the frame. Each tile carries a jagged six-spoke crack whose spokes end exactly on
  the six hex edge midpoints, entering along the centre-to-midpoint line. Neighbouring tiles' spokes therefore meet
  end to end in a straight joint, so 60 identical synced stamps read as ONE crack network across the floor. Sparse
  per tile (one tall blade, one short) because everything is multiplied by 60.
- CASTER (visual tag appear), animationScale 3.0: chakra gathers into the body (frames 0-3), the body detonates
  (4+), and six drive-cracks run from the caster's hex centre to its own edge midpoints, which are exactly where the
  ring-1 tiles' spokes begin: the cut visibly leaves the caster and runs into the field.
- Timing on one clock (both appears start together): the field waits dark for frames 0-3 while the caster gathers,
  cuts outward 4-7 in step with the caster's drive-cracks, flashes at 8, blades erupt 9-12, shards rise and the web
  cools 13-23. The static loop starts at t=0 too (engine), so its first 15 frames (1.05 s) are quiet and cover the
  eruption; the glints come after, every cycle.
Pillow for drawing, numpy for compositing (as the earlier FCF builders).
"""
import argparse
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_strips as B  # noqa: E402  arr, img, over, dots, load, transform, bolt, noise, strip

N = 512
VIOLET = np.array([0.72, 0.42, 1.0], np.float32)
HOT = np.array([0.97, 0.93, 1.0], np.float32)
SCORCH = np.array([0.10, 0.04, 0.16], np.float32)
FIELD_SCALE = 2.0
CASTER_SCALE = 3.0
MS = {"field": 42, "caster": 42, "loop": 70, "end": 50}


# ----------------------------------------------------------------------------------------------- geometry
def tile_geom(n, scale):
    """Centre, width and height of the tile box inside an n x n clip frame (clip side = tile.height x scale)."""
    h = n / scale
    return n / 2, n / 2, 2 * h, h


def edge_midpoints(cx, cy, w, h):
    """Flat-top hex (vertices at +-w/2 on the axis, +-w/4 at +-h/2): top, upper-right, lower-right, bottom,
    lower-left, upper-left edge midpoints."""
    return [(cx, cy - h / 2), (cx + 3 * w / 8, cy - h / 4), (cx + 3 * w / 8, cy + h / 4),
            (cx, cy + h / 2), (cx - 3 * w / 8, cy + h / 4), (cx - 3 * w / 8, cy - h / 4)]


def hex_poly(cx, cy, w, h):
    return [(cx - w / 2, cy), (cx - w / 4, cy - h / 2), (cx + w / 4, cy - h / 2), (cx + w / 2, cy),
            (cx + w / 4, cy + h / 2), (cx - w / 4, cy + h / 2)]


def polyline_len(pts):
    d = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d.append(d[-1] + math.hypot(x1 - x0, y1 - y0))
    return d


def partial(pts, frac):
    """The first `frac` of a polyline (by length)."""
    d = polyline_len(pts)
    L = d[-1] * max(0.0, min(1.0, frac))
    out = [pts[0]]
    for i in range(1, len(pts)):
        if d[i] <= L:
            out.append(pts[i])
        else:
            t = (L - d[i - 1]) / max(1e-6, d[i] - d[i - 1])
            x0, y0 = pts[i - 1]
            x1, y1 = pts[i]
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
            break
    return out


def spoke(rng, hub, centre, mid, rough=0.16):
    """Jagged crack from the hub to an edge midpoint. The last 20% runs straight along the centre->midpoint line,
    so the neighbour's spoke (the point reflection through the midpoint) continues it without a kink."""
    ux, uy = mid[0] - centre[0], mid[1] - centre[1]
    knee = (centre[0] + ux * 0.8, centre[1] + uy * 0.8)
    L = math.hypot(knee[0] - hub[0], knee[1] - hub[1])
    ang = math.atan2(knee[1] - hub[1], knee[0] - hub[0])
    raw = B.bolt(rng, L, steps=5, rough=rough)
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(hub[0] + x * ca - y * sa, hub[1] + x * sa + y * ca) for x, y in raw]
    pts[-1] = knee
    return pts + [mid]


def branch(rng, pts, at, length, turn):
    """A short dead-end side crack leaving a spoke at fraction `at`."""
    p = partial(pts, at)
    (x0, y0), (x1, y1) = p[-2], p[-1]
    ang = math.atan2(y1 - y0, x1 - x0) + turn
    raw = B.bolt(rng, length, steps=3, rough=0.25)
    ca, sa = math.cos(ang), math.sin(ang)
    return [(x1 + x * ca - y * 0.5 * sa, y1 + x * sa * 0.5 + y * ca) for x, y in raw]


# ------------------------------------------------------------------------------------------------ painting
def stroke(paths, widths, n=N, blur=0.0):
    """Alpha mask (float n x n) of polylines with per-path width, drawn 2x supersampled."""
    ss = 2
    im = Image.new("L", (n * ss, n * ss), 0)
    d = ImageDraw.Draw(im)
    for pts, wd in zip(paths, widths):
        if len(pts) < 2 or wd <= 0:
            continue
        sp = [(x * ss, y * ss) for x, y in pts]
        d.line(sp, fill=255, width=max(1, int(wd * ss)), joint="curve")
        r = wd * ss / 2
        for x, y in (sp[0], sp[-1]):
            d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    im = im.resize((n, n), Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(im, dtype=np.float32) / 255.0


def layer(mask, colour, alpha=1.0):
    c = np.zeros(mask.shape + (4,), np.float32)
    c[..., :3] = colour
    c[..., 3] = np.clip(mask * alpha, 0, 1)
    return c


def crack_layers(paths, core_w, heat, glow=1.0, scorch=0.0, n=N):
    """Scorch underlay, violet glow, hot core. heat 0..1 pushes the core from violet to white and fattens the glow."""
    c = np.zeros((n, n, 4), np.float32)
    if scorch:
        c = B.over(c, layer(stroke(paths, [w * 2.2 for w in core_w], n, blur=2), SCORCH, scorch))
    if glow:
        g = stroke(paths, [w * (2.0 + 0.8 * heat) for w in core_w], n, blur=4 + 3 * heat)
        c = B.over(c, layer(g, VIOLET, glow * (0.40 + 0.25 * heat)))
    core = stroke(paths, core_w, n)
    col = VIOLET * (1 - heat) + HOT * heat
    return B.over(c, layer(core, col, 1.0))


def shard(n, x, base, top, width, lean=0.0):
    """A sharp vertical blade of light (Kanada-style angular shard): white core, violet edge."""
    im = Image.new("L", (n * 2, n * 2), 0)
    d = ImageDraw.Draw(im)
    poly = [(x - width, base), (x + lean * (base - top) * 0.15, top), (x + width * 0.7, base)]
    d.polygon([(px * 2, py * 2) for px, py in poly], fill=255)
    m = np.asarray(im.resize((n, n), Image.LANCZOS), np.float32) / 255
    inner = Image.new("L", (n * 2, n * 2), 0)
    ImageDraw.Draw(inner).polygon([(px * 2, py * 2) for px, py in
                                   [(x - width * 0.35, base), (x + lean * (base - top) * 0.15, top + (base - top) * 0.12),
                                    (x + width * 0.25, base)]], fill=255)
    mi = np.asarray(inner.resize((n, n), Image.LANCZOS), np.float32) / 255
    glow = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7)), np.float32) / 255
    c = layer(glow, VIOLET, 0.7)
    c = B.over(c, layer(m, VIOLET * 0.5 + HOT * 0.5, 1.0))
    return B.over(c, layer(mi, HOT, 1.0))


# --------------------------------------------------------------------------------------------- the field tile
def field_web(n=N, seed=21):
    cx, cy, w, h = tile_geom(n, FIELD_SCALE)
    rng = np.random.default_rng(seed)
    hub = (cx + 0.035 * w, cy - 0.03 * h)
    mids = edge_midpoints(cx, cy, w, h)
    # one through-cut per tile: upper-left midpoint -> hub -> lower-right midpoint. The tile across each of those
    # edges carries the same cut, so the tiles chain into long parallel slashes across the whole field.
    spokes = [spoke(rng, hub, (cx, cy), mids[5]), spoke(rng, hub, (cx, cy), mids[2])]
    branches = [branch(rng, spokes[1], 0.35, w * 0.12, -1.0), branch(rng, spokes[0], 0.55, w * 0.07, 1.2)]
    return hub, spokes, branches, (cx, cy, w, h)


def field_widths(n, spokes, branches, k=1.0):
    u = n / 192.0  # widths are authored in final-pixel units
    return [4.0 * u * k] * len(spokes), [2.2 * u * k] * len(branches)


def build_field_appear(n=N):
    hub, spokes, branches, (cx, cy, w, h) = field_web(n)
    sw, bw = field_widths(n, spokes, branches)
    blades = [  # (x on the floor, base y, peak height as fraction of frame, half width, lean, start frame)
        # a short spray along the cut, mixed heights (big/medium/small), so 60 copies read as eruption, not a fence
        (spokes[1][len(spokes[1]) // 2][0], spokes[1][len(spokes[1]) // 2][1], 0.46, n * 0.020, 0.25, 9),
        (spokes[0][len(spokes[0]) // 2][0], spokes[0][len(spokes[0]) // 2][1], 0.26, n * 0.014, -0.3, 9),
        (spokes[1][int(len(spokes[1]) * 0.8)][0], spokes[1][int(len(spokes[1]) * 0.8)][1], 0.15, n * 0.011, 0.4, 10),
    ]
    rng = np.random.default_rng(77)
    frames = []
    for f in range(24):
        c = np.zeros((n, n, 4), np.float32)
        if f in (2, 3):  # anticipation: a dark pinch at the hub while the caster gathers
            c = B.over(c, B.dots(n, [hub + (0.35 * (f - 1),)], SCORCH, n * 0.03))
        elif 4 <= f <= 7:  # the cut races out to the edges
            p = [0.22, 0.5, 0.8, 1.0][f - 4]
            paths = [partial(s, p) for s in spokes]
            c = B.over(c, crack_layers(paths, sw, heat=0.6, glow=0.9, scorch=0.5, n=n))
            heads = [pt[-1] for pt in paths]
            c = B.over(c, B.dots(n, [(x, y, 1.0) for x, y in heads], HOT, n * 0.022))
            if f >= 6:
                c = B.over(c, crack_layers([partial(b, (f - 5) / 2) for b in branches], bw, 0.4, 0.6, 0.4, n))
        elif f >= 8:
            heat = 1.0 if f == 8 else max(0.0, 1 - (f - 8) / 7)
            fade = 1.0 if f < 17 else max(0.0, 1 - (f - 16) / 7)
            k = 1.15 if f == 8 else 1.0
            sw2, bw2 = field_widths(n, spokes, branches, k)
            web = crack_layers(spokes + branches, sw2 + bw2, heat, glow=1.0, scorch=0.6, n=n)
            web[..., 3] *= fade
            c = B.over(c, web)
            for bx, by, peak, hw, lean, s0 in blades:
                t = f - s0
                if t < 0:
                    continue
                top_full = by - peak * n * 0.62
                if t <= 2:  # rise fast, hold
                    top = by - (by - top_full) * [0.45, 1.0, 1.0][t]
                    c = B.over(c, shard(n, bx, by, top, hw * (1 - 0.25 * (t == 2)), lean))
                elif t <= 9:  # shatter: shards fly up and fade
                    u = (t - 2) / 7
                    pts = []
                    for i in range(5):
                        fy = by - (by - top_full) * (0.25 + 0.17 * i) - n * 0.10 * u * (1 + 0.3 * i)
                        fx = bx + (i - 2) * hw * 0.9 * u + lean * 8
                        pts.append((fx, fy, (1 - u) ** 1.3))
                    c = B.over(c, B.dots(n, pts, VIOLET * 0.4 + HOT * 0.6, hw * (0.8 - 0.4 * u)))
        frames.append(B.img(c))
    return frames


def build_field_ground(n=N):
    """The scar under every struck tile for its 2 rounds: dark scorched cracks with a dim violet seam, the same web
    as the appear, so the leftover cracks also link tile to tile. Cropped to the tile box (2:1)."""
    hub, spokes, branches, (cx, cy, w, h) = field_web(n)
    sw, bw = field_widths(n, spokes, branches, 0.9)
    c = np.zeros((n, n, 4), np.float32)
    c = B.over(c, layer(stroke(spokes + branches, [x * 2.4 for x in sw + bw], n, blur=3), SCORCH, 0.85))
    c = B.over(c, layer(stroke(spokes + branches, [x * 0.55 for x in sw + bw], n), VIOLET * 0.8, 0.85))
    im = B.img(c)
    return im.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)))


def build_field_loop(n=N, frames=32, quiet=15):
    """Glints along the cracks. Plays from the strike (engine: static loops from t=0, over the appear), so the first
    `quiet` frames of each cycle are empty: in the first cycle that covers the eruption."""
    hub, spokes, branches, _ = field_web(n)
    rng = np.random.default_rng(5)
    pts_all = [p for s in spokes for p in s[1:-1]]
    sparks = [(pts_all[int(rng.integers(len(pts_all)))], int(rng.integers(0, frames - quiet - 5))) for _ in range(7)]
    sw, bw = field_widths(n, spokes, branches, 0.9)
    seam = layer(stroke(spokes + branches, sw + bw, n, blur=3), VIOLET, 1.0)
    out = []
    for f in range(frames):
        c = np.zeros((n, n, 4), np.float32)
        if f >= quiet:
            t = (f - quiet) / max(1, frames - quiet - 1)
            breathe = math.sin(math.pi * t) ** 2 * 0.45
            s = seam.copy()
            s[..., 3] *= breathe
            c = B.over(c, s)
            for (x, y), s0 in sparks:
                k = f - quiet - s0
                if 0 <= k < 5:
                    al = [0.5, 1.0, 0.8, 0.45, 0.2][k]
                    c = B.over(c, B.dots(n, [(x, y - k * n * 0.008, al)], HOT, n * (0.016 + 0.004 * (k == 1))))
        out.append(B.img(c))
    return out


def build_field_end(n=N):
    """Disappear (server visual; also replays on occupants), kept light: the seams flare once and drain, a few motes
    lift off."""
    hub, spokes, branches, _ = field_web(n)
    sw, bw = field_widths(n, spokes, branches, 0.9)
    rng = np.random.default_rng(9)
    pts_all = [p for s in spokes for p in s[1:-1]]
    motes = [pts_all[int(rng.integers(len(pts_all)))] for _ in range(6)]
    out = []
    for f in range(10):
        t = f / 9
        c = crack_layers(spokes + branches, sw + bw, heat=0.5 * (1 - t), glow=0.8, scorch=0.0, n=n)
        c[..., 3] *= (1 - t) ** 1.4 * (1.0 if f > 0 else 0.6)
        c = B.over(c, B.dots(n, [(x, y - n * 0.18 * t, 0.9 * (1 - t)) for x, y in motes], VIOLET * 0.6 + HOT * 0.4,
                             n * 0.012))
        out.append(B.img(c))
    return out


# ------------------------------------------------------------------------------------------------ the caster
def build_caster(n=N):
    """The body detonation on the caster (visual tag, scale 3) that drives the cut into the field."""
    cx, cy, w, h = tile_geom(n, CASTER_SCALE)
    mids = edge_midpoints(cx, cy, w, h)
    rng = np.random.default_rng(3)
    drives = [spoke(rng, (cx, cy), (cx, cy), m, rough=0.12) for m in mids]
    u = n / 192.0
    body = (cx, cy - 0.30 * h)  # the fighter stands on the tile; the burst sits at the chest
    A = B.load("A_fury_burst_keypose.png", n)
    rng2 = np.random.default_rng(8)
    motes = [(rng2.uniform(0, 2 * math.pi), rng2.uniform(0.32, 0.48)) for _ in range(26)]
    er = B.noise(n, 11, 5)
    frames = []
    for f in range(18):
        c = np.zeros((n, n, 4), np.float32)
        if f <= 3:  # gather: motes rush into the body, a core swells
            t = (f + 1) / 4
            pts = [(body[0] + math.cos(a) * r * n * (1 - 0.8 * t), body[1] + math.sin(a) * r * n * 0.7 * (1 - 0.8 * t),
                    0.9) for a, r in motes]
            c = B.over(c, B.dots(n, pts, VIOLET * 0.7 + HOT * 0.3, n * 0.010))
            c = B.over(c, B.dots(n, [body + (1.0,)], HOT, n * (0.02 + 0.03 * t)))
        if 4 <= f <= 7:  # drive-cracks leave the caster, in step with the field's cut
            p = [0.25, 0.55, 0.85, 1.0][f - 4]
            c = B.over(c, crack_layers([partial(d, p) for d in drives], [7.0 * u] * 6, heat=1.0, glow=1.0,
                                       scorch=0.4, n=n))
        if 8 <= f <= 12:
            k = max(0.0, 1 - (f - 8) / 5)
            c = B.over(c, crack_layers(drives, [6.0 * u] * 6, heat=k, glow=k, scorch=0.4 * k, n=n))
        if f >= 4:  # the body detonation (the painted keypose), vertical-biased, then ember dissolve
            t = (f - 4) / 13
            s = 0.35 + 0.75 * min(1.0, (f - 4) / 3) ** 0.6
            fr = B.arr(B.transform(A, s, (f - 4) * 1.5, dy=(body[1] - n / 2)))
            if f >= 9:
                thr = ((f - 9) / 8) ** 1.1
                fr[..., 3] *= np.clip((er - thr) / 0.12, 0, 1)
            if f <= 5:
                fl = 1 - (f - 4) / 2
                fr[..., :3] = fr[..., :3] * (1 - 0.5 * fl) + HOT * 0.5 * fl
            c = B.over(c, fr)
            if f >= 5:  # a flat shock ring on the floor, out to the edge of the caster's tile
                r = min(1.0, (f - 4) / 5)
                ring = Image.new("L", (n * 2, n * 2), 0)
                rw, rh = w * 0.55 * r * 2, h * 0.55 * r * 2
                ImageDraw.Draw(ring).ellipse((cx * 2 - rw, cy * 2 - rh, cx * 2 + rw, cy * 2 + rh), outline=255,
                                             width=int(6 * u * 2 * (1 - 0.5 * r)) + 1)
                m = np.asarray(ring.resize((n, n), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2)), np.float32) / 255
                c = B.over(c, layer(m, VIOLET * 0.5 + HOT * 0.5, max(0.0, 1 - (f - 4) / 7)))
        frames.append(B.img(c))
    return frames


# --------------------------------------------------------------------------------------------- board preview
def odd_q_to_cube(c, r):
    x = c
    z = r - (c - (c & 1)) // 2
    return x, -x - z, z


def hex_dist(a, b):
    ax, ay, az = odd_q_to_cube(*a)
    bx, by, bz = odd_q_to_cube(*b)
    return max(abs(ax - bx), abs(ay - by), abs(az - bz))


def board(clips, out, cols=12, rows=10, caster=(5, 5), radius=4, px=2, shrink=0.75):
    """Real board geometry (fx_board/hex_board sizing, 12 x 10): the field's clips on every spiral tile (radius 4
    around the caster, caster excluded), the caster clip on the caster's tile, all on one clock: appears from t=0,
    the loop from t=0 over the appear, the end clip after two loop cycles."""
    width_css = 360
    STACK = 0.25
    hs = width_css / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    W, H = int(width_css * px), int((rows + 0.5) * h)
    tiles = {}
    for c in range(cols):
        for r in range(rows):
            tiles[(c, r)] = (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))
    field = sorted([k for k in tiles if k != caster and hex_dist(k, caster) <= radius], key=lambda k: tiles[k][1])
    base = Image.new("RGBA", (W, H), (38, 40, 36, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in tiles.values():
        d.polygon(hex_poly(x, y, w, h), outline=(255, 255, 255, 34))
    fe = int(h * FIELD_SCALE)
    ce = int(h * CASTER_SCALE)
    rs = lambda fr, s: [f.resize((s, s), Image.LANCZOS) for f in fr]  # noqa: E731
    fa, fl, fend = rs(clips["field"], fe), rs(clips["loop"], fe), rs(clips["end"], fe)
    ca = rs(clips["caster"], ce)
    g = clips["ground"].resize((int(w), int(h)), Image.LANCZOS)
    a_ms, c_ms, l_ms, e_ms = MS["field"], MS["caster"], MS["loop"], MS["end"]
    lasting = len(fl) * l_ms * 2
    total = lasting + len(fend) * e_ms + 500
    marks = set(range(0, len(fa) * a_ms + 1, a_ms)) | set(range(0, len(ca) * c_ms + 1, c_ms)) | \
        set(range(0, lasting, l_ms)) | set(range(lasting, lasting + len(fend) * e_ms + 1, e_ms)) | {total}
    times = sorted(m for m in marks if m <= total)
    cx, cy = tiles[caster]
    frames, durs = [], []
    for i, t in enumerate(times[:-1]):
        im = base.copy()
        live = t < lasting
        if live:
            for k in field:
                x, y = tiles[k]
                im.alpha_composite(g, (int(x - w / 2), int(y - h / 2)))
        # the caster: a plain stand-in figure so the burst can be judged against a body
        ImageDraw.Draw(im).rounded_rectangle((cx - w * 0.13, cy - h * 1.7, cx + w * 0.13, cy), radius=6,
                                             fill=(70, 66, 84, 255), outline=(150, 140, 170, 255))
        layers = []
        if live and t < len(fa) * a_ms:
            layers.append(fa[t // a_ms])
        if live:
            layers.append(fl[(t // l_ms) % len(fl)])
        if not live and t - lasting < len(fend) * e_ms:
            layers.append(fend[(t - lasting) // e_ms])
        for fr in layers:
            for k in field:
                x, y = tiles[k]
                im.alpha_composite(fr, (int(x - fe / 2), int(y - fe / 2)))
        if t < len(ca) * c_ms:
            im.alpha_composite(ca[t // c_ms], (int(cx - ce / 2), int(cy - ce / 2)))
        ImageDraw.Draw(im).text((6, 4), f"FCF v5  field x{FIELD_SCALE}  caster x{CASTER_SCALE}  t={t}ms  "
                                        f"{len(field)} tiles", fill=(255, 255, 255, 220))
        im = im.convert("RGB")
        if shrink != 1:
            im = im.resize((int(W * shrink), int(H * shrink)), Image.LANCZOS)
        frames.append(im)
        durs.append(times[i + 1] - t)
    q, acc, done = [], 0, 0
    for dm in durs:
        acc += dm
        step = max(20, int(round((acc - done) / 10.0)) * 10)
        q.append(step)
        done += step
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=q, loop=0, optimize=True)
    return len(field), len(frames)


def margin(frames, size):
    out = []
    for f in frames:
        a = np.asarray(f.resize((size, size), Image.LANCZOS)).copy()
        a[:2, :, 3] = 0
        a[-2:, :, 3] = 0
        out.append(Image.fromarray(a, "RGBA"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=192)
    ap.add_argument("--board", action="store_true")
    ap.add_argument("--final", action="store_true", help="write the upload set to final/ (fresh v5 names)")
    a = ap.parse_args()
    clips = {"field": build_field_appear(), "loop": build_field_loop(), "end": build_field_end(),
             "caster": build_caster(), "ground": build_field_ground()}
    outdir = os.path.join(HERE, "final" if a.final else "exports")
    os.makedirs(outdir, exist_ok=True)
    names = {"field": ("anim_fcf_field_v5", True), "loop": ("anim_fcf_glint_v5", False),
             "end": ("anim_fcf_drain_v5", False), "caster": ("anim_fcf_caster_v5", True)}
    for key, (stem, pal) in names.items():
        p = os.path.join(outdir, f"{stem}_{a.size}.webp")
        b = B.strip(margin(clips[key], a.size), a.size, p, palette=pal)
        print(f"{os.path.basename(p)}: {len(clips[key])} frames x {MS[key]} ms, {b} bytes")
    g = os.path.join(outdir, "ground_fcf_scar_v5.webp")
    clips["ground"].resize((384, 192), Image.LANCZOS).save(g, "WEBP", lossless=True, method=6)
    print(f"{os.path.basename(g)}: 384x192, {os.path.getsize(g)} bytes")
    if a.board:
        prev = os.path.join(HERE, "preview")
        os.makedirs(prev, exist_ok=True)
        # judge from the delivered pixels: round-trip every clip through the exported size
        rt = {k: [f.resize((a.size, a.size), Image.LANCZOS) for f in clips[k]] for k in names}
        rt["ground"] = clips["ground"].resize((384, 192), Image.LANCZOS)
        nt, nf = board(rt, os.path.join(prev, "fcf_board_v5.gif"))
        print(f"board: {nt} field tiles, {nf} frames -> preview/fcf_board_v5.gif")


if __name__ == "__main__":
    main()
