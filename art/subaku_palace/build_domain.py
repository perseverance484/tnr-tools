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

How the domain reads as summoned on a floor that is already there (revised after QA on be8646d1):
- no veil: the floor is visible from tick 0 (and a veil drew over fighters and meters);
- each band's strip lights its OWN hex only: on the landing tick the channels go white-hot and the rail faces burn,
  then the tail cools over 3 ticks and recedes outward toward the next ring; the cracks flare a tick behind. The
  bands land 1-2 ticks apart, so the light steps out ring by ring along the woven rails;
- every strip is self-contained (no cross-hex overshoot), so a strip that loads late (each record starts when its own
  images are ready) at worst lights its ring a little late; it never runs back over a lit ring or spills past the rim;
- keep-outs: no clip pixel over the hex's own fighter, the lower hex's head and meters, or the diagonal neighbours'
  meters (see keepout());
- the seal (the ground appear, all 60 hexes, x2, hard alpha so the duplicate changes nothing): the held beat, the
  whole rail face burning solid on ticks 19-21, white-hot channels on 20.

Exports:
- tile_sbk_domain_v3.webp (STATIC 128 px, the spec minimum, small so it loads first): the ground tag's staticAssetPath (3 rounds).
  floor.py, 'rails'.
- anim_sbk_wave_b{k}_v1.webp (k = 0..6, 32 x 50 ms, 150 px frames): the band visual tags' appearAnimation.
- anim_sbk_seal_v1.webp (32 x 50 ms): the ground tag's appearAnimation.
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
# a band lights its OWN hex only (plus a 0.04 seam margin): each band is self-contained, so a late-loading strip
# cannot run back over a lit ring, and nothing spills past the rim onto the bare board (QA B3/B4, 2026-11-05)
EMBER = [(110, 12, 8), (184, 28, 16), (255, 74, 28), (255, 150, 60)]
BURN = [(255, 207, 74), (255, 229, 138), (255, 244, 200)]
SEAL_FACE = (236, 176, 70)       # the rail face burning at about 70 % toward the burning gold
GRID, EXPORT = 50, 3
HW_S, HH_S = 132, 66             # the true-scale hex box on screen (the live still's scale)
BLOOM = 4                        # ticks for the gold to form from the hex centre to its edges
DISSOLVE = 3                     # once formed, an ordered dissolve hands over to the real tile at once (the clip is
                                 # coarser than the tile: 50 px over 2.5 h, so the less of it on screen the better)
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def keepout(n=GRID):
    """255 where a clip may paint (n px clip). Tile heights: x from the hex centre, y up from the hex bottom.
    K1 the hex's own fighter (centre column +-0.35 h from the bottom up; +-0.55 h from 1.25 h up: its meters, LPC
    hudTop 1.5 h, AI originals 1.99 h);
    K2 the lower hex's fighter head and meters (+-0.55 h, 0.15-1.0 h: LPC meters at 0.3-0.5 h, AI at 0.8-1.0 h); K3 the diagonal neighbours (|x| >= 1 h,
    y >= 0.7 h). From combatActors.ts (LPC 1.35 h, feet 0.234 h; AI 1.6 h at 0.9 h) and the meter rows."""
    k = Image.new('L', (n, n), 255)
    p = k.load()
    h = n / RATIO
    for py in range(n):
        for px in range(n):
            x = abs(px + 0.5 - n / 2) / h
            y = (n / 2 + h / 2 - (py + 0.5)) / h
            if (x <= 0.35 and y >= 0.0) or (x <= 0.55 and y >= 1.25) or (x <= 0.55 and 0.15 <= y <= 1.0) \
                    or (x >= 1.0 and y >= 0.7):
                p[px, py] = 0
    return k


def screen_look(tile_img):
    """What the static tile looks like on screen (50 px rendition, linear onto the 132 x 66 box), placed in the
    clip square at true scale and brought back to the clip's 50 px grid: the colours a clip must show to match it."""
    r = (tile_img.resize((50, 50), Image.LANCZOS) if tile_img.width > 50 else tile_img).convert('RGBa')
    k = round(HH_S * RATIO)
    sx, sy = 50 / HW_S, 50 / HH_S
    ox, oy = (k - HW_S) / 2, (k - HH_S) / 2              # exact centring (the engine anchors both at 0.5)
    sq = r.transform((k, k), Image.AFFINE, (sx, 0, (sx - 1) / 2 - ox * sx, 0, sy, (sy - 1) / 2 - oy * sy),
                     resample=Image.BILINEAR).convert('RGBA')
    return sq.convert('RGBa').resize((GRID, GRID), Image.BOX).convert('RGBA'), sq


def layers(tile_full, tile_dim):
    G, C, K, A, R = FL.field_masks(CLIP, RATIO)
    g50 = lambda m: m.resize((GRID, GRID), Image.BOX).point(lambda v: 255 if v >= 100 else 0)
    T, T_screen = screen_look(tile_full)
    D, _ = screen_look(tile_dim)
    cover = T.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
    ko = keepout()
    area = ImageChops.multiply(cover, ko)
    Rn = R.resize((GRID, GRID), Image.NEAREST)
    return {'T': T, 'D': D, 'area': area, 'gold': ImageChops.multiply(g50(G), area),
            'chan': ImageChops.multiply(g50(C), area), 'crack': ImageChops.multiply(g50(K), area), 'R': Rn,
            'T_screen': T_screen, 'ko': ko}


def solid(frame, mask, colour):
    frame.paste(Image.new('RGBA', frame.size, colour + (255,)), (0, 0), mask)


def band(L, lo, hi):
    """Pixels whose hex norm (0 centre, 1 edge) is in [lo, hi)."""
    return L['R'].point(lambda v: 255 if int(127.5 * lo) <= v < int(127.5 * hi) else 0)


def wave_frame(L, t, land):
    """The director's arrival (2026-11-05). Each hex of the band (keep-outs aside) is covered by its own floor with the
    gold engraved but unlit, so the domain reads as empty stone. On the landing tick the gold forms from the hex
    centre outward over 4 ticks: a white-hot head along the rails, a burning trail, the cracks flaring behind; behind
    the trail the clip shows the tile's on-screen look. Then an ordered dissolve over 3 ticks hands over to the real
    tile underneath. The seal's held beat (19-21) is on the ground strip, under the clips, seen once they are gone."""
    f = Image.new('RGBA', (GRID, GRID), (0, 0, 0, 0))
    hold_to = land + BLOOM - 1
    if t > hold_to + DISSOLVE:
        return f
    u = t - land
    # front radius (hex norm): 0.35, 0.7, 1.05 on the first three ticks; the fourth is the plain formed floor
    r = 0.0 if u < 0 else (9.0 if u >= BLOOM - 1 else 0.35 * (u + 1))
    formed = band(L, 0, max(0.0, r - 0.35))
    front = band(L, max(0.0, r - 0.35), r)
    ahead = band(L, r, 9)
    f.paste(L['D'], (0, 0), ImageChops.multiply(L['area'], ahead))
    f.paste(L['T'], (0, 0), ImageChops.multiply(L['area'], ImageChops.add(formed, front)))
    if 0 <= u < BLOOM - 1:
        solid(f, ImageChops.multiply(L['gold'], front), BURN[0])
        solid(f, ImageChops.multiply(L['chan'], front), BURN[2])
        trail = band(L, max(0.0, r - 0.7), max(0.0, r - 0.35))
        solid(f, ImageChops.multiply(L['chan'], trail), BURN[1])
        solid(f, ImageChops.multiply(L['crack'], trail), EMBER[3])
    if t > hold_to:                                                     # ordered dissolve
        cut = (t - hold_to) * 16 / DISSOLVE
        a = f.getchannel('A')
        ap = a.load()
        for y in range(GRID):
            for x in range(GRID):
                if BAYER[y % 4][x % 4] < cut:
                    ap[x, y] = 0
        f.putalpha(a)
    return f


def seal_frame(L, t):
    """The ground appear (all 60 hexes, x2, drawn under the band clips): the held beat 19-21, the whole rail face
    burning solid and the channels white-hot on 20. By then rings 1-3 have dissolved; ring 4 is mid-dissolve."""
    f = Image.new('RGBA', (GRID, GRID), (0, 0, 0, 0))
    if 19 <= t <= 21:
        solid(f, L['gold'], SEAL_FACE)
        solid(f, L['chan'], BURN[2] if t == 20 else BURN[0])
        solid(f, L['crack'], EMBER[3] if t == 20 else EMBER[2])
    return f


def to_pixels(f):
    """Hard alpha, 1 px clear rows top and bottom, x3 nearest."""
    a = f.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
    ap = a.load()
    for x in range(GRID):
        ap[x, 0] = ap[x, GRID - 1] = 0
    g = f.copy()
    g.putalpha(a)
    return g.resize((GRID * EXPORT, GRID * EXPORT), Image.NEAREST)


def strip(frames):
    n = GRID * EXPORT
    s = Image.new('RGBA', (n, n * len(frames)), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        s.paste(to_pixels(fr), (0, i * n))
    return s


def handoff_check(L):
    """The clip's held frame vs the tile, both on screen at true scale, over the covered area: mean abs difference
    (0-255) and the share of pixels off by more than 32. Also the cover's first frame vs the tile (the pop a late
    strip would show)."""
    k = round(HH_S * RATIO)

    def on_screen(img50):
        return img50.convert('RGBa').transform((k, k), Image.AFFINE, (50 / k, 0, (50 / k - 1) / 2, 0, 50 / k,
                                                                         (50 / k - 1) / 2),
                                               resample=Image.BILINEAR).convert('RGBA')
    held = wave_frame(L, 7 + BLOOM - 1, 7)
    first = wave_frame(L, 0, 7)
    area = on_screen(Image.merge('RGBA', [L['area']] * 4)).getchannel('A').point(lambda v: 255 if v >= 250 else 0)
    out = {}
    for name, fr in (('handoff', held), ('late_pop', first)):
        s = on_screen(to_pixels(fr).resize((GRID, GRID), Image.NEAREST))
        a, b = s.convert('RGB'), L['T_screen'].convert('RGB')
        d = ImageChops.difference(a, b).convert('L')
        px = [v for v, m in zip(d.getdata(), area.getdata()) if m]
        out[name] = {'mean_abs': round(sum(px) / len(px), 1), 'share_over_32': round(sum(v > 32 for v in px) / len(px),
                                                                                       3), 'pixels': len(px)}
    return out


BANDS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]


def land_tick(b):
    """Whole bands land on their ring's tick (4 + 3 d). A half band holds ring d on one parity and d + 1 on the
    other: it lands at 3 d + 5, rounded toward the earlier ring (QA S5): 50 ms late on one parity, 100 ms early on
    the other."""
    d = math.floor(b)
    return 4 + 3 * d + (1 if b != d else 0)


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
    tile_full = FL.tile(size=128)
    tile_full.save(os.path.join(OUT, 'tile_sbk_domain_v3.webp'), lossless=True, method=6)
    FL.MODE = 'dim'
    tile_dim = FL.tile(size=128)
    FL.MODE = 'full'
    L = layers(tile_full, tile_dim)
    meta = {'ratio': RATIO, 'speed': SPEED, 'tile': 'rails', 'order': 'rings', 'assets': {}, 'groups': []}
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
    meta['handoff_check'] = handoff_check(L)
    json.dump(meta, open(os.path.join(OUT, 'subaku_domain_v1.json'), 'w'), indent=1)
    print('handoff', meta['handoff_check'])
    print('ok', [(land, len(o)) for land, o in G])


if __name__ == '__main__':
    main()
