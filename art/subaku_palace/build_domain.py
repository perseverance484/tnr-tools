#!/usr/bin/env python3
"""Subaku Palace: the domain floor and its ring-by-ring summoning (Pillow only).

    python3 build_domain.py        # writes exports/ and exports/subaku_domain_v1.json

Engine (docs/design/COMBAT_ANIMATION_ENGINE.md; theninjarpg@3314d122 and upstream main cb755375, read, never run):
- AOE_SPIRAL_SHOOT stamps the ground tag on spiral(caster, 4) minus the caster's hex (targeting.ts:56-58): 60 hexes in
  one action, so every record starts on the same tick. There is no per-tag delay field in the game source, and static
  art (staticAssetPath) is drawn from the record's first ready frame for its whole life, so the floor is present
  from tick 0. Ring order is baked into strips carried by visual-only COORDINATES tags (origin CASTER), one per
  half-ring band (7, RUL-2026-11-05-125).
- Clips: EFFECT_ANIMATION_HEX_RATIO tile heights square (2.5; the director's build target, 2026-11-05), from the
  50 px rendition, linear, drawn OVER the fighters. Static art: under the fighters, stretched to the 2:1 hex box.

How the domain reads as summoned on a floor that is already there:
- each band's strip holds its own hex in shadow (a 50 % ordered dither, x1) until its band lands, so the floor is
  uncovered ring by ring. A veil on the ground tag's appear would play x2, and linear filtering turns two dithered
  copies into 75 % black over the fighters, so the ground appear (the seal) carries only one breath of light through
  every channel as the rim lands;
- each band's strip carries the current: it starts at the hex centre on the band's landing tick and runs outward
  along the gold currents, eddies and curls at a fixed speed (one hex pitch per 3 ticks), past its own hex edge into
  the neighbours (the clip overlaps them, and the floor is one periodic field, so the pixels line up on any caster
  parity). The next ring's front starts as this one arrives, so the light crosses each seam as one continuous current;
  the overshoot fades out 0.3 hex radius past the edge so no front runs back over a lit ring.
- the cracks flare a tick behind the front, then everything settles to the static floor.

Exports:
- tile_sbk_domain_v3.webp (STATIC 150 px): the ground tag's staticAssetPath (3 rounds). floor.py, 'flow'.
- anim_sbk_wave_b{k}_v1.webp (k = 0..6, 32 x 50 ms, 150 px frames): the band visual tags' appearAnimation.
- anim_sbk_seal_v1.webp (32 x 50 ms): the ground tag's appearAnimation (all 60 hexes, x2: hard alpha, so the
  duplicate changes nothing).
"""
import json
import math
import os
import sys

from PIL import Image, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import floor as FL  # noqa: E402

OUT = os.path.join(HERE, 'exports')
RATIO = float(os.environ.get('SBK_RATIO', '2.5'))
CLIP = 100            # authoring size; finished on the 50 px grid, exported x3 nearest (150 px)
NF = 32
SPEED = 50
SEAL_PEAK = 20
VEIL_LIFT = 16
TICKS_PER_PITCH = 3.0  # the front travels one hex pitch (sqrt3 radii) in 3 ticks: the ring spacing
OVERSHOOT = 0.30       # hex radii past the own edge (hex norm 1.0 -> 1.3), fading

SHADOW = (22, 10, 9)
EMBER = [(110, 12, 8), (184, 28, 16), (255, 74, 28), (255, 150, 60)]
GOLD = [(138, 90, 18), (196, 138, 28), (232, 180, 58)]
BURN = [(255, 207, 74), (255, 229, 138), (255, 244, 200)]
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
GRID, EXPORT = 50, 3


def layers():
    G, C, K, A, R = FL.field_masks(CLIP, RATIO)
    # reach: full inside the own hex (norm <= 1), fading to 0 at 1 + OVERSHOOT; and away from the clip edge
    reach = R.point(lambda v: 255 if v <= 127 else max(0, int(255 * (1 - (v / 127.5 - 1) / OVERSHOOT))))
    side = Image.new('L', (CLIP, CLIP), 0)
    sp = side.load()
    for y in range(2, CLIP - 2):
        for x in range(2, CLIP - 2):
            e = min(x, y, CLIP - 1 - x, CLIP - 1 - y)
            sp[x, y] = 255 if e >= 8 else int(255 * e / 8)
    reach = ImageChops.multiply(reach, side)
    # travel time: radial distance from the hex centre in regular units, in half ticks
    T = Image.new('L', (CLIP, CLIP), 0)
    tp = T.load()
    for y in range(CLIP):
        for x in range(CLIP):
            dx = (x + 0.5 - CLIP / 2) / CLIP * RATIO
            dy = (y + 0.5 - CLIP / 2) / CLIP * RATIO * math.sqrt(3)
            tp[x, y] = min(255, int(math.hypot(dx, dy) / math.sqrt(3) * TICKS_PER_PITCH * 2))
    lv = [ImageChops.multiply(T.point(lambda v, i=i: 255 if v == i else 0), reach) for i in range(10)]
    hexm = R.point(lambda v: 255 if v <= 129 else 0)
    return {'gold': G, 'chan': C, 'crack': K, 'levels': lv, 'hex': hexm, 'reach': reach}


def head(u):
    if u < 0:
        return 0.0
    if u < 1:
        return 1.0
    return max(0.0, 0.8 * (0.74 ** (u - 1)))


def tail(u):
    return 0.0 if u < 0 else max(0.0, 0.9 ** u)


def stepped(i, ramp):
    return None if i <= 0 else ramp[min(len(ramp) - 1, int(i * len(ramp) - 1e-6))]


def paint(frame, mask, colour, alpha):
    if alpha <= 0.01 or colour is None:
        return
    frame.paste(Image.new('RGBA', frame.size, colour + (255,)), (0, 0), mask.point(lambda v: int(v * min(1, alpha))))


def wave_frame(L, t, land):
    f = Image.new('RGBA', (CLIP, CLIP), (0, 0, 0, 0))
    if t < land:            # this hex is still in shadow: a 50 % ordered dither, lifted the tick its band lands
        paint(f, L['hex'], SHADOW, 0.5)
    for k, lvm in enumerate(L['levels']):
        u = t - land - k * 0.5
        if u < 0:
            continue
        i, j = head(u), tail(u)
        band = ImageChops.multiply(L['gold'], lvm)
        ch = ImageChops.multiply(L['chan'], lvm)
        paint(f, band, stepped(i, [GOLD[2], BURN[0], BURN[1]]), 0.15 + 0.6 * i)
        paint(f, ch.filter(ImageFilter.MaxFilter(3)), BURN[0], 0.55 * max(i, 0.5 * j))
        paint(f, ch, stepped(max(i, 0.6 * j), [BURN[0], BURN[1], BURN[2]]), 0.95 * max(i, 0.75 * j))
        cr = ImageChops.multiply(L['crack'], lvm)
        ci = head(u - 1)
        paint(f, cr.filter(ImageFilter.MaxFilter(3)), EMBER[1], 0.35 * ci)
        paint(f, cr, stepped(ci, [EMBER[2], EMBER[3]]), 0.15 + 0.85 * ci)
    return f


def seal_frame(L, t):
    f = Image.new('RGBA', (CLIP, CLIP), (0, 0, 0, 0))
    u = t - SEAL_PEAK
    if -2 <= u <= 6:
        i = {-2: 0.4, -1: 0.75}.get(u, 1.0 if u == 0 else 0.85 * 0.7 ** u)
        paint(f, ImageChops.multiply(L['chan'], L['hex']), stepped(i, [GOLD[2], BURN[0], BURN[1]]), 0.9 * i)
        paint(f, ImageChops.multiply(L['crack'], L['hex']), EMBER[2], 0.8 * i)
    return f


def to_pixels(fr):
    """Finish on the 50 px grid: hard alpha (threshold; an ordered-dither step only in the mid band, so a veil
    becomes a deliberate dither and decaying tails do not turn to glitter), 1 px clear rows top and bottom (no frame
    bleed), x3 nearest."""
    small = fr.convert('RGBa').resize((GRID, GRID), Image.BOX).convert('RGBA')
    px = small.load()
    for y in range(GRID):
        for x in range(GRID):
            r, g, b, a = px[x, y]
            keep = a >= 150 or (a >= 60 and a > (BAYER[y % 4][x % 4] + 0.5) * 16 * 0.6 + 50)
            px[x, y] = (r, g, b, 255) if keep and 0 < y < GRID - 1 else (0, 0, 0, 0)
    return small.resize((GRID * EXPORT, GRID * EXPORT), Image.NEAREST)


def strip(frames):
    n = GRID * EXPORT
    s = Image.new('RGBA', (n, n * len(frames)), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        s.paste(to_pixels(fr), (0, i * n))
    return s


BANDS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]


def land_tick(b):
    return int(4 + 3 * b + 0.5)


def _cube(c, r):
    return c, r - (c - (c & 1)) // 2


def _dist(a, b):
    (q1, r1), (q2, r2) = _cube(*a), _cube(*b)
    dq, dr = q1 - q2, r1 - r2
    return max(abs(dq), abs(dr), abs(dq + dr))


def groups(radius=4):
    """[(land_tick, [(dcol, drow)])]: offsets inside the domain on BOTH caster parities (56 of 60), banded by the mean
    hex distance over the two parities (offsets are col/row, targeting.ts:59-75)."""
    E, O = (10, 10), (11, 10)
    out = {b: [] for b in BANDS}
    for dc in range(-radius - 1, radius + 2):
        for dr in range(-radius - 1, radius + 2):
            de = _dist((E[0] + dc, E[1] + dr), E)
            do = _dist((O[0] + dc, O[1] + dr), O)
            if 0 < max(de, do) <= radius:
                out[(de + do) / 2].append((dc, dr))
    return [(land_tick(b), out[b]) for b in BANDS]


def main():
    os.makedirs(OUT, exist_ok=True)
    FL.tile().save(os.path.join(OUT, 'tile_sbk_domain_v3.webp'), lossless=True, method=6)
    L = layers()
    meta = {'ratio': RATIO, 'speed': SPEED, 'tile': 'flow', 'order': 'rings', 'assets': {}, 'groups': []}
    G = groups()
    for k, (land, offs) in enumerate(G):
        name = f'anim_sbk_wave_b{k}_v1.webp'
        strip([wave_frame(L, t, land) for t in range(NF)]).save(os.path.join(OUT, name), lossless=True, method=6)
        meta['assets'][name] = {'type': 'ANIMATION', 'frames': NF, 'speed': SPEED,
                                'use': 'visual tag (COORDINATES, origin CASTER) appearAnimation'}
        meta['groups'].append({'asset': name, 'lands_tick': land,
                               'offsets': [{'longitude': c, 'latitude': r} for c, r in offs]})
    strip([seal_frame(L, t) for t in range(NF)]).save(os.path.join(OUT, 'anim_sbk_seal_v1.webp'), lossless=True,
                                                       method=6)
    meta['assets']['anim_sbk_seal_v1.webp'] = {'type': 'ANIMATION', 'frames': NF, 'speed': SPEED,
                                               'use': 'ground tag (decreasedamagegiven) appearAnimation, 60 hexes'}
    meta['assets']['tile_sbk_domain_v3.webp'] = {'type': 'STATIC', 'use': 'ground tag staticAssetPath (3 rounds)'}
    for n in meta['assets']:
        meta['assets'][n]['bytes'] = os.path.getsize(os.path.join(OUT, n))
    json.dump(meta, open(os.path.join(OUT, 'subaku_domain_v1.json'), 'w'), indent=1)
    print('ok', [(land, len(o)) for land, o in G])


if __name__ == '__main__':
    main()
