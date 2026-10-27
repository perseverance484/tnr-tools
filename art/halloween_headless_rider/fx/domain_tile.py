#!/usr/bin/env python3
"""The Headless Rider's domain: a full-hex ground tile that tiles seamlessly across the battlefield.

    python3 domain_tile.py [--base PNG] [--out exports/tile_rider_domain.webp]

Why it tiles: the game stretches a staticAssetPath sprite to each hex's bounding box (libs/threejs/combat.ts:635,
sprite.scale.set(w, h)), so a flat-top hex drawn corner to corner in the square canvas fills the tile exactly. The bands
are a hex Truchet: three arcs centred on alternate corners (0, 2, 4), each of radius half an edge, so every arc meets
an edge exactly at its midpoint, square to it. Every tile is the same image, so each band leaving one tile at an edge
midpoint enters the neighbour at the matching midpoint: the field forms one continuous lattice of linked rings.

Look (Headless Rider Horror!): charred cracked ground with ember seams (the approved T1 scorch art as the floor), crossed
by channels of blackened iron filled with hellfire, a dark bevelled rim on every hex. Pixel-stepped colours, no
gradients: built at 1024 and box-reduced to 256 so the steps stay crisp.
"""
import argparse
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxkit as fx  # noqa: E402

N = 1024
SQ3 = math.sqrt(3)
# regular flat-top hex, circumradius R, centred; then stretched vertically to fill the square
R = N / 2
SY = N / (SQ3 * R)                       # vertical stretch so the hex's flat top and bottom touch the canvas


def P(x, y):
    """Regular-hex coords (centre 0,0, y down) -> canvas coords."""
    return N / 2 + x, N / 2 + y * SY


CORNERS = [(R * math.cos(math.radians(60 * k)), R * math.sin(math.radians(60 * k))) for k in range(6)]

IRON = [(18, 10, 9), (38, 22, 18), (62, 38, 30)]                         # dark -> light rim steps
FIRE = [(110, 8, 6), (196, 30, 12), (246, 96, 24), (255, 176, 56), (255, 236, 168)]  # outer -> core


def hex_mask(inset=0.0):
    m = Image.new('L', (N, N), 0)
    pts = [P(x * (1 - inset), y * (1 - inset)) for x, y in CORNERS]
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


def arc_points(cx, cy, r, a0, a1, steps=240):
    return [P(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / steps)),
              cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / steps))) for i in range(steps + 1)]


def _mid(k):
    (x1, y1), (x2, y2) = CORNERS[k], CORNERS[(k + 1) % 6]
    return (x1 + x2) / 2, (y1 + y2) / 2


def _line_intersect(k1, k2):
    """Intersection of the lines through edges k1 and k2 (extended)."""
    (x1, y1), (x2, y2) = CORNERS[k1], CORNERS[(k1 + 1) % 6]
    (x3, y3), (x4, y4) = CORNERS[k2], CORNERS[(k2 + 1) % 6]
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return x1 + t * (x2 - x1), y1 + t * (y2 - y1)


def _arc_between(e1, e2, centre):
    cx, cy = centre
    (ax, ay), (bx, by) = _mid(e1), _mid(e2)
    r = math.hypot(ax - cx, ay - cy)
    a0, a1 = math.degrees(math.atan2(ay - cy, ax - cx)), math.degrees(math.atan2(by - cy, bx - cx))
    d = (a1 - a0 + 540) % 360 - 180              # the short way round, the side that lies inside the hex
    return [P(cx + r * math.cos(math.radians(a0 + d * i / 240)), cy + r * math.sin(math.radians(a0 + d * i / 240)))
            for i in range(241)]


# Edge k runs from corner k to corner k+1. Corner 0 joins edges 5 and 0: a small arc round it. Edges 1-3 and 2-4 are two
# apart: large arcs, each centred where its two edges' lines meet, so it leaves both edges square. They cross once
# (the weave). All six midpoints used once each, so identical tiles join everywhere.
PATHS = [
    ('small', lambda: _arc_between(5, 0, CORNERS[0])),
    ('under', lambda: _arc_between(1, 3, _line_intersect(1, 3))),
    ('over', lambda: _arc_between(2, 4, _line_intersect(2, 4))),
]


def bands(width, which=None):
    m = Image.new('L', (N, N), 0)
    d = ImageDraw.Draw(m)
    for name, fn in PATHS:
        if which is None or name in which:
            d.line(fn(), fill=255, width=int(width), joint='curve')
    return m


def build(base_path, out, size=256):
    base = Image.open(base_path).convert('RGBA')
    # floor: the scorch art, centre-cropped and scaled to cover the whole canvas, darkened a step so the bands lead
    s = min(base.size)
    crop = base.crop(((base.width - s) // 2 + int(s * 0.12), (base.height - s) // 2 + int(s * 0.12),
                      (base.width + s) // 2 - int(s * 0.12), (base.height + s) // 2 - int(s * 0.12)))
    floor = Image.new('RGBA', (N, N), (16, 8, 6, 255))
    floor.alpha_composite(crop.resize((N, N), Image.LANCZOS))
    floor = Image.eval(floor.convert('RGB'), lambda v: int(v * 0.85)).convert('RGBA')

    img = floor.copy()
    # channel: iron rim (3 steps, widest first), then hellfire core (5 steps, narrowing to a white-hot line)
    widths_iron = [124, 108, 96]
    widths_fire = [84, 66, 46, 26, 10]
    for which in (('small', 'under'), ('over',)):
        shadow = bands(170, which).filter(ImageFilter.GaussianBlur(10))
        img.paste((0, 0, 0, 255), (0, 0), shadow.point(lambda v: int(v * 0.7)))
        for col, w in zip(IRON, widths_iron):
            img.paste(col + (255,), (0, 0), bands(w, which))
        for col, w in zip(FIRE, widths_fire):
            img.paste(col + (255,), (0, 0), bands(w, which))
    # hex rim: a dark bevel so each tile reads as a laid stone, matching the Subaku tile's framing
    rim_outer, rim_inner = hex_mask(0.0), hex_mask(0.035)
    rim = Image.eval(Image.composite(rim_outer, Image.new('L', (N, N), 0), Image.eval(rim_inner, lambda v: 255 - v)),
                     lambda v: v)
    img.paste((10, 5, 4, 255), (0, 0), rim)
    hi = Image.composite(hex_mask(0.035), Image.new('L', (N, N), 0), Image.eval(hex_mask(0.05), lambda v: 255 - v))
    img.paste((70, 30, 20, 255), (0, 0), hi)
    out_img = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    out_img.paste(img, (0, 0), hex_mask(0.0))
    small = out_img.convert('RGBa').resize((size, size), Image.BOX).convert('RGBA')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    small.save(out, lossless=True, method=6)
    print(f'domain tile {out}: {size}x{size}, {os.path.getsize(out)} bytes')
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=os.path.join(fx.ART, 'hellfire_harvest', 'raws', 'T1_scorch_raw.png'))
    ap.add_argument('--out', default=os.path.join(fx.EXPORTS, 'tile_rider_domain.webp'))
    a = ap.parse_args()
    build(a.base, a.out)


# ----------------------------------------------------------------------------------------------- pumpkin patch domain
VINE = [(8, 16, 8), (20, 38, 16), (38, 66, 26), (66, 102, 38)]            # outline -> highlight
LEAF = [(14, 30, 12), (34, 62, 24), (60, 96, 34)]
PUMPKIN = [(40, 12, 4), (120, 36, 6), (196, 78, 12), (238, 128, 28), (255, 186, 80)]  # outline -> highlight


def _leaves(img, path, every=48, size=34, seed=1):
    rnd = __import__('random').Random(seed)
    d = ImageDraw.Draw(img)
    for i in range(every // 2, len(path) - 4, every):
        (x0, y0), (x1, y1) = path[i], path[i + 3]
        ang = math.atan2(y1 - y0, x1 - x0) + (math.pi / 2 if (i // every) % 2 else -math.pi / 2)
        ang += rnd.uniform(-0.4, 0.4)
        tip = (x0 + size * 1.6 * math.cos(ang), y0 + size * 1.6 * math.sin(ang))
        left = (x0 + size * 0.7 * math.cos(ang + 0.9), y0 + size * 0.7 * math.sin(ang + 0.9))
        right = (x0 + size * 0.7 * math.cos(ang - 0.9), y0 + size * 0.7 * math.sin(ang - 0.9))
        d.polygon([(x0, y0), left, tip, right], fill=LEAF[0])
        sh = 0.75
        d.polygon([(x0, y0), (x0 + (left[0] - x0) * sh, y0 + (left[1] - y0) * sh), (x0 + (tip[0] - x0) * sh, y0 + (tip[1] - y0) * sh),
                   (x0 + (right[0] - x0) * sh, y0 + (right[1] - y0) * sh)], fill=LEAF[1])
        d.line([(x0, y0), (x0 + (tip[0] - x0) * 0.7, y0 + (tip[1] - y0) * 0.7)], fill=LEAF[2], width=4)


def _pumpkin(img, cx, cy, w, grin):
    """A carved jack-o-lantern seen slightly from above, lobed, with the hellfire grin (G1) glowing in its face."""
    h = w * 0.78
    d = ImageDraw.Draw(img)
    d.ellipse((cx - w * 0.55, cy + h * 0.28, cx + w * 0.55, cy + h * 0.62), fill=(0, 0, 0, 150))       # contact shadow
    lobes = [(-0.34, 0.30), (0.34, 0.30), (-0.17, 0.40), (0.17, 0.40), (0.0, 0.44)]
    for i, col in enumerate(PUMPKIN[:4]):
        g = 10 - i * 7
        for lx, lw in lobes:
            x = cx + lx * w
            ww = lw * w
            d.ellipse((x - ww - g + i * 3, cy - h / 2 - g + i * 4, x + ww + g - i * 3, cy + h / 2 + g - i * 2), fill=col)
    for lx, lw in lobes[2:]:
        x = cx + lx * w
        d.ellipse((x - lw * w * 0.35, cy - h * 0.42, x + lw * w * 0.2, cy - h * 0.05), fill=PUMPKIN[4])
    d.rectangle((cx - w * 0.05, cy - h * 0.66, cx + w * 0.05, cy - h * 0.42), fill=VINE[1])
    d.rectangle((cx - w * 0.03, cy - h * 0.66, cx + w * 0.01, cy - h * 0.46), fill=VINE[3])
    face = grin.resize((int(w * 0.74), int(w * 0.74 * grin.height / grin.width)), Image.LANCZOS)
    img.alpha_composite(face, (int(cx - face.width / 2), int(cy - face.height / 2 + h * 0.06)))


def build_pumpkin(base_path, grin_path, out, size=256):
    base = Image.open(base_path).convert('RGBA')
    s = min(base.size)
    crop = base.crop(((base.width - s) // 2 + int(s * 0.12), (base.height - s) // 2 + int(s * 0.12),
                      (base.width + s) // 2 - int(s * 0.12), (base.height + s) // 2 - int(s * 0.12)))
    floor = Image.new('RGBA', (N, N), (14, 9, 6, 255))
    floor.alpha_composite(crop.resize((N, N), Image.LANCZOS))
    img = Image.eval(floor.convert('RGB'), lambda v: int(v * 0.7)).convert('RGBA')
    for which in (('small', 'under'), ('over',)):
        sh = bands(110, which).filter(ImageFilter.GaussianBlur(9))
        img.paste((0, 0, 0, 255), (0, 0), sh.point(lambda v: int(v * 0.75)))
        for col, w in zip(VINE, (72, 58, 40, 14)):
            img.paste(col + (255,), (0, 0), bands(w, which))
        for name, fn in PATHS:
            if name in which:
                _leaves(img, fn(), seed=len(name))
    grin = Image.open(grin_path).convert('RGBA')
    gb = grin.getchannel('A').getbbox()
    # The game squashes this square to the hex's 2:1 box. Ground art wants that; an upright pumpkin does not. Draw it
    # on its own layer and pre-stretch it 2x tall, so after the game's squash it stands round.
    pl = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    _pumpkin(pl, N / 2, N / 2, N * 0.34, grin.crop(gb))
    bb = pl.getchannel('A').getbbox()
    pc = pl.crop(bb)
    pc = pc.resize((pc.width, int(pc.height / fx.HEX_ASPECT)), Image.NEAREST)
    img.alpha_composite(pc, (int(N / 2 - pc.width / 2), int(N / 2 - pc.height / 2 + N * 0.04)))
    rim_outer, rim_inner = hex_mask(0.0), hex_mask(0.035)
    img.paste((8, 6, 4, 255), (0, 0), Image.composite(rim_outer, Image.new('L', (N, N), 0),
                                                       Image.eval(rim_inner, lambda v: 255 - v)))
    hi = Image.composite(hex_mask(0.035), Image.new('L', (N, N), 0), Image.eval(hex_mask(0.05), lambda v: 255 - v))
    img.paste((56, 34, 14, 255), (0, 0), hi)
    out_img = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    out_img.paste(img, (0, 0), hex_mask(0.0))
    small = out_img.convert('RGBa').resize((size, size), Image.BOX).convert('RGBA')
    small.save(out, lossless=True, method=6)
    print(f'pumpkin domain tile {out}: {size}x{size}, {os.path.getsize(out)} bytes')
    return out
