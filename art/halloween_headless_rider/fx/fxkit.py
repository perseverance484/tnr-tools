#!/usr/bin/env python3
"""fxkit: ground-field battle effects (Hellfire Harvest, Aura of Despair) from the art director's raw layers.

The existing strip builders (ethereal_rebirth / celestial_dew / chakra_overflow) are built around a self-cast effect over
the caster's portrait. These two jutsu are GROUND effects that cover many tiles at once, so this kit adds what that
needs. Pillow only (+ ffmpeg for the optional MP4).

    python3 fxkit.py ingest RAW CODE              # raw QC + trimmed working copy in work/<CODE>.png
    python3 fxkit.py split RAW CODE [--min PX]    # cut a multi-piece sheet (E1 embers, W1 wisps) into work/<CODE>_NN.png
    python3 fxkit.py tile SRC OUT [--opacity A]   # STATIC ground tile: 256 px lossless WebP, alpha scaled, edge-safe
    python3 fxkit.py board OUT.gif [--tile T] [--appear STRIP MS] [--loop STRIP MS] [--pattern all|spiral]
    python3 fxkit.py selftest

How the game draws a ground effect (TheNinjaRPG 58801f9):
- libs/combat/util.ts getBattleGrid: FLAT hexes, width = hexsize, height = hexsize * HEX_ASPECT_RATIO (0.5).
- libs/threejs/combat.ts drawCombatBackground: hexsize = canvas_width / (cols - 0.25 * (cols - 1)).
- libs/threejs/combat.ts 610-680 (per effect, per tile):
    staticAssetPath -> a still Sprite scaled to (w, h): the square tile is squashed to 2:1, so a top-down disc becomes
                       a flat ellipse on the ground. Author still tiles top-down and square; the game adds perspective.
    appearAnimation -> a strip played ONCE at EFFECT_ANIMATION_SIZE = 50 units, square, centred on the tile, layer 5.
    staticAnimation -> the same, looping while the effect lasts.
  So ground-hugging parts of an animation (scorch, mist rings) must be drawn squashed to 0.5 inside the square frame,
  while upright parts (flames, blade, grin, wisps) stay unsquashed. place(..., squash=0.5) does that.
- gameAsset ANIMATION: vertical strip, square frames, frames = count; speed = ms per frame (the Celestial Dew strips run
  36 ms). Spec: >= 112 px frames, lossless WebP, < 460,800 bytes.
"""
import argparse
import math
import os
import random
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ART = os.path.join(ROOT, 'art', 'halloween_headless_rider')
WORK = os.path.join(HERE, 'work')
EXPORTS = os.path.join(HERE, 'exports')

FRAME = 112                 # exported frame size (spec ANIMATION minimum)
S = 448                     # working frame size (4x), downsampled once at export
BYTE_CEILING = 460_800
HEX_ASPECT = 0.5            # HEX_ASPECT_RATIO
STACK = 0.25                # HEX_STACKING_DISPLACEMENT
EFFECT = 50                 # EFFECT_ANIMATION_SIZE, world units = CSS px


# ----------------------------------------------------------------------------------------------- raw handling
def alpha_stats(img):
    a = img.getchannel('A').histogram()
    n = sum(a)
    return {'clear': sum(a[:8]) / n, 'solid': sum(a[248:]) / n, 'partial': sum(a[8:248]) / n}


def edge_touch(img, band=4):
    """Share of the canvas border band that is not clear: a generated element must not touch the edge."""
    a = img.getchannel('A')
    w, h = a.size
    px = a.load()
    hits = tot = 0
    for x in range(w):
        for y in list(range(band)) + list(range(h - band, h)):
            tot += 1
            hits += px[x, y] > 16
    for y in range(band, h - band):
        for x in list(range(band)) + list(range(w - band, w)):
            tot += 1
            hits += px[x, y] > 16
    return hits / tot


def ingest(raw, code):
    img = Image.open(raw)
    problems = []
    if img.mode != 'RGBA':
        problems.append(f'mode {img.mode}: no real alpha (regenerate with transparency, or key it first)')
        img = img.convert('RGBA')
    st = alpha_stats(img)
    if st['clear'] < 0.15:
        problems.append(f"only {st['clear']:.0%} clear: likely a backing colour or checkerboard")
    et = edge_touch(img)
    if et > 0.02:
        problems.append(f'{et:.1%} of the border is not clear: the element touches the canvas edge')
    bbox = img.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    out = img.crop(bbox) if bbox else img
    os.makedirs(WORK, exist_ok=True)
    p = os.path.join(WORK, f'{code}.png')
    out.save(p)
    print(f"{code}: {img.size} -> trimmed {out.size}; clear {st['clear']:.0%} solid {st['solid']:.0%} "
          f"partial {st['partial']:.0%}; border {et:.1%}")
    for pr in problems:
        print(f'  REJECT? {pr}')
    print(f'  -> {p}')
    return out, problems


def split(raw, code, min_px=400, pad=6):
    """Connected components of the alpha (8-neighbour, alpha > 24), each saved trimmed. Small specks merge into nothing."""
    img = Image.open(raw).convert('RGBA')
    a = img.getchannel('A')
    small = a.resize((a.width // 2, a.height // 2), Image.BOX)       # half-res labelling is plenty and 4x faster
    w, h = small.size
    px = small.load()
    seen = bytearray(w * h)
    pieces = []
    for y0 in range(h):
        for x0 in range(w):
            if seen[y0 * w + x0] or px[x0, y0] <= 24:
                continue
            stack = [(x0, y0)]
            seen[y0 * w + x0] = 1
            xs, ys, n = [x0, x0], [y0, y0], 0
            while stack:
                x, y = stack.pop()
                n += 1
                xs[0], xs[1] = min(xs[0], x), max(xs[1], x)
                ys[0], ys[1] = min(ys[0], y), max(ys[1], y)
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and px[nx, ny] > 24:
                            seen[ny * w + nx] = 1
                            stack.append((nx, ny))
            if n * 4 >= min_px:
                pieces.append((xs[0] * 2 - pad, ys[0] * 2 - pad, xs[1] * 2 + 2 + pad, ys[1] * 2 + 2 + pad, n * 4))
    pieces.sort(key=lambda p: -p[4])
    os.makedirs(WORK, exist_ok=True)
    out = []
    for i, (x0, y0, x1, y1, n) in enumerate(pieces):
        box = (max(0, x0), max(0, y0), min(img.width, x1), min(img.height, y1))
        p = os.path.join(WORK, f'{code}_{i:02d}.png')
        img.crop(box).save(p)
        out.append(p)
    print(f'{code}: {len(out)} pieces (min {min_px} px) -> {WORK}/{code}_NN.png')
    return out


# ----------------------------------------------------------------------------------------------- static tile
def static_tile(src, out, opacity=1.0, size=256, feather=0.06):
    """Square top-down ground tile for staticAssetPath. Scales alpha by `opacity` (readability over units) and feathers
    the outer `feather` of the inscribed circle so neighbouring tiles blend instead of showing square edges."""
    img = Image.open(src).convert('RGBA')
    side = max(img.size)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    sq.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
    sq = sq.resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    d = ImageDraw.Draw(mask)
    steps = max(1, int(size * feather))
    for i in range(steps + 1):
        v = int(255 * i / steps)
        r = size / 2 - (steps - i)
        d.ellipse((size / 2 - r, size / 2 - r, size / 2 + r, size / 2 + r), fill=v)
    a = sq.getchannel('A')
    a = Image.composite(a, Image.new('L', a.size, 0), mask).point(lambda v: int(v * opacity))
    sq.putalpha(a.point(lambda v: 0 if v < 4 else v))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sq.save(out, lossless=True, method=6)
    b = os.path.getsize(out)
    print(f'tile {out}: {size}x{size}, opacity {opacity}, {b} bytes ({"OK" if b < BYTE_CEILING else "OVER CEILING"})')
    return out


# ----------------------------------------------------------------------------------------------- frame compositing
def frame():
    return Image.new('RGBA', (S, S), (0, 0, 0, 0))


def place(layer, img, cx, cy, width, alpha=1.0, rot=0.0, squash=1.0, additive=False):
    """Composite `img` onto `layer`, centred at (cx, cy) in frame fractions, `width` as a frame fraction.
    squash < 1 flattens it onto the ground (0.5 = the game's hex perspective). additive brightens instead of covering."""
    if width <= 0 or alpha <= 0:
        return layer
    w = max(1, int(width * S))
    h = max(1, int(img.height * w / img.width * squash))
    im = img.resize((w, h), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    x, y = int(cx * S - im.width / 2), int(cy * S - im.height / 2)
    if additive:
        tmp = Image.new('RGBA', layer.size, (0, 0, 0, 0))
        tmp.paste(im, (x, y), im)
        rgb = Image.composite(tmp, Image.new('RGBA', layer.size, (0, 0, 0, 0)), tmp.getchannel('A'))
        from PIL import ImageChops
        merged = ImageChops.add(layer.convert('RGB'), rgb.convert('RGB'))
        a = ImageChops.lighter(layer.getchannel('A'), tmp.getchannel('A'))
        layer.paste(merged)
        layer.putalpha(a)
        return layer
    layer.alpha_composite(im, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))
    return layer


def wipe(img, t, direction='lr', soft=0.12):
    """Reveal `img` progressively (t 0..1) along a direction with a soft leading edge: a sweep without motion blur."""
    w, h = img.size
    m = Image.new('L', (w, h), 0)
    px = m.load()
    edge = t * (1 + soft)
    for x in range(w):
        u = x / max(1, w - 1) if direction == 'lr' else 1 - x / max(1, w - 1)
        v = max(0.0, min(1.0, (edge - u) / soft))
        col = int(255 * v)
        for y in range(h):
            px[x, y] = col
    out = img.copy()
    out.putalpha(Image.composite(img.getchannel('A'), Image.new('L', (w, h), 0), m))
    return out


def ease_out(t):
    return 1 - (1 - t) ** 3


def ease_in(t):
    return t ** 3


def seg(t, a, b):
    """0..1 progress of t through [a, b]."""
    return max(0.0, min(1.0, (t - a) / (b - a))) if b > a else float(t >= b)


def to_export(fr):
    """S -> FRAME. Box filter keeps pixel-art clusters solid instead of ringing; then drop near-zero alpha."""
    out = fr.resize((FRAME, FRAME), Image.BOX)
    out.putalpha(out.getchannel('A').point(lambda v: 0 if v < 6 else v))
    return out


def save_strip(frames, name, ms):
    os.makedirs(EXPORTS, exist_ok=True)
    fr = [to_export(f) for f in frames]
    strip = Image.new('RGBA', (FRAME, FRAME * len(fr)), (0, 0, 0, 0))
    for i, f in enumerate(fr):
        strip.paste(f, (0, FRAME * i))
    p = os.path.join(EXPORTS, f'{name}.webp')
    strip.save(p, lossless=True, method=6)
    b = os.path.getsize(p)
    print(f'{name}: {len(fr)} frames x {FRAME}px at {ms} ms = {len(fr) * ms / 1000:.2f} s; {b} bytes '
          f'({"OK" if b < BYTE_CEILING else "OVER CEILING"}); gameAsset frames={len(fr)} speed={ms}')
    return p


def strip_frames(path):
    s = Image.open(path).convert('RGBA')
    n = s.height // s.width
    return [s.crop((0, i * s.width, s.width, (i + 1) * s.width)) for i in range(n)]


# ----------------------------------------------------------------------------------------------- battle preview
def hex_board(width_css=360, cols=12, rows=7, scale=3):
    """Tile centres and sizes as the game lays them out (FLAT hexes, odd-q style offset), in preview pixels."""
    hexsize = width_css / (cols - STACK * (cols - 1))
    w, h = hexsize, hexsize * HEX_ASPECT
    tiles = []
    for c in range(cols):
        for r in range(rows):
            x = c * w * (1 - STACK) + w / 2
            y = r * h + h / 2 + (h / 2 if c % 2 else 0)
            tiles.append((c, r, x * scale, y * scale))
    return tiles, w * scale, h * scale, (width_css * scale, int((rows + 0.5) * h * scale)), EFFECT * scale


def spiral_tiles(tiles, centre, radius=2, w=1.0, h=1.0):
    """Tiles within `radius` hex steps of `centre` (approximate in preview space): the AOE_SPIRAL_SHOOT patch."""
    cx, cy = centre
    out = []
    for t in tiles:
        dx, dy = (t[2] - cx) / (w * 0.75), (t[3] - cy) / h
        if math.hypot(dx, dy) <= radius + 0.25:
            out.append(t)
    return out


def _hex_poly(x, y, w, h):
    return [(x - w / 2, y), (x - w / 4, y - h / 2), (x + w / 4, y - h / 2), (x + w / 2, y), (x + w / 4, y + h / 2),
            (x - w / 4, y + h / 2)]


def board(out, tile=None, appear=None, appear_ms=36, loop=None, loop_ms=60, pattern='all', seconds=None,
          bg=None, units=None, tick=40):
    """GIF of the board: background, hex outlines, units, the static tile on every affected tile, the appear strip
    played once on all of them at the same instant, the loop on top. The honest check that 2:1 squash, 50-unit effect
    size and full-board repetition read well."""
    tiles, w, h, (W, H), eff = hex_board()
    bg = bg or os.path.join(ART, 'headless_rider_horror_04_river.webp')
    base = Image.open(bg).convert('RGBA').resize((W, int(W * 2 / 3)), Image.LANCZOS)
    base = base.crop((0, max(0, base.height - H) // 2, W, max(0, base.height - H) // 2 + H)).resize((W, H))
    shade = Image.new('RGBA', (W, H), (0, 0, 0, 90))
    base.alpha_composite(shade)
    d = ImageDraw.Draw(base)
    for t in tiles:
        d.polygon(_hex_poly(t[2], t[3], w, h), outline=(255, 255, 255, 40))
    centre = tiles[len(tiles) // 2 + 2]
    hit = tiles if pattern == 'all' else spiral_tiles(tiles, (centre[2], centre[3]), 2, w, h)
    if tile:
        ti = Image.open(tile).convert('RGBA').resize((int(w), int(h)), Image.LANCZOS)
        for t in hit:
            base.alpha_composite(ti, (int(t[2] - w / 2), int(t[3] - h / 2)))
    # units: the Rider and three stand-in players, as round portraits on the tile (avatar 0.8 h at 1.0 h above centre)
    rider = Image.open(os.path.join(ART, 'headless_rider_avatar.webp')).convert('RGBA')
    units = units or [(tiles[3], rider), (tiles[40], None), (tiles[47], None), (tiles[61], None)]
    for t, img in units:
        r = int(0.8 * h * 2.2)
        x, y = int(t[2] - r / 2), int(t[3] - h - r / 2)
        disc = Image.new('L', (r, r), 0)
        ImageDraw.Draw(disc).ellipse((0, 0, r - 1, r - 1), fill=255)
        face = img.resize((r, r), Image.LANCZOS) if img else Image.new('RGBA', (r, r), (60, 90, 140, 255))
        port = Image.new('RGBA', (r, r), (0, 0, 0, 0))
        port.paste(face, (0, 0), disc)
        ImageDraw.Draw(base).ellipse((x - 2, y - 2, x + r + 1, y + r + 1), outline=(240, 240, 240, 255), width=2)
        base.alpha_composite(port, (x, y))
    a_fr = [f.resize((eff, eff), Image.BOX) for f in strip_frames(appear)] if appear else []
    l_fr = [f.resize((eff, eff), Image.BOX) for f in strip_frames(loop)] if loop else []
    total = seconds * 1000 if seconds else max(len(a_fr) * appear_ms + 1200, 2 * len(l_fr) * loop_ms, 1500)
    frames = []
    for ms in range(0, int(total), tick):
        c = base.copy()
        ai = ms // appear_ms
        for t in hit:
            pos = (int(t[2] - eff / 2), int(t[3] - eff / 2))
            if l_fr:
                c.alpha_composite(l_fr[(ms // loop_ms) % len(l_fr)], pos)
            if ai < len(a_fr):
                c.alpha_composite(a_fr[ai], pos)
        frames.append(c.convert('RGB'))
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=tick, loop=0, optimize=True)
    print(f'board {out}: {len(frames)} frames, {W}x{H}, {len(hit)} tiles, pattern {pattern}')
    return out


# ----------------------------------------------------------------------------------------------- selftest
def selftest():
    t1 = os.path.join(ART, 'hellfire_harvest', 'raws', 'T1_scorch_raw.png')
    ok = True
    img, probs = ingest(t1, 'T1')
    ok &= not probs
    tile = static_tile(os.path.join(WORK, 'T1.png'), os.path.join(EXPORTS, 'selftest_tile.webp'), opacity=0.7)
    # a throwaway appear: the scorch slammed down flat and fading, just to exercise place/squash/strip/board
    frames = []
    for i in range(12):
        t = i / 11
        fr = frame()
        place(fr, img, 0.5, 0.62, 0.3 + 0.6 * ease_out(t), alpha=1 - seg(t, 0.6, 1.0), squash=HEX_ASPECT)
        frames.append(fr)
    strip = save_strip(frames, 'selftest_appear', 36)
    ok &= len(strip_frames(strip)) == 12 and os.path.getsize(strip) < BYTE_CEILING
    board(os.path.join(EXPORTS, 'selftest_board.gif'), tile=tile, appear=strip, appear_ms=36, pattern='all', seconds=2)
    board(os.path.join(EXPORTS, 'selftest_spiral.gif'), tile=tile, appear=strip, appear_ms=36, pattern='spiral', seconds=2)
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('ingest'); p.add_argument('raw'); p.add_argument('code')
    p = sub.add_parser('split'); p.add_argument('raw'); p.add_argument('code'); p.add_argument('--min', type=int, default=400)
    p = sub.add_parser('tile'); p.add_argument('src'); p.add_argument('out'); p.add_argument('--opacity', type=float, default=1.0)
    p = sub.add_parser('board'); p.add_argument('out'); p.add_argument('--tile'); p.add_argument('--appear', nargs=2)
    p.add_argument('--loop', nargs=2); p.add_argument('--pattern', default='all', choices=['all', 'spiral'])
    p.add_argument('--seconds', type=float)
    sub.add_parser('selftest')
    a = ap.parse_args()
    if a.cmd == 'ingest':
        return 1 if ingest(a.raw, a.code)[1] else 0
    if a.cmd == 'split':
        split(a.raw, a.code, a.min)
    elif a.cmd == 'tile':
        static_tile(a.src, a.out, a.opacity)
    elif a.cmd == 'board':
        board(a.out, a.tile, a.appear[0] if a.appear else None, int(a.appear[1]) if a.appear else 36,
              a.loop[0] if a.loop else None, int(a.loop[1]) if a.loop else 60, a.pattern, a.seconds)
    elif a.cmd == 'selftest':
        return selftest()
    return 0


if __name__ == '__main__':
    sys.exit(main())
