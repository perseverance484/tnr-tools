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

How the domain reads as summoned on a floor that is already there (the director's arrival, 2026-11-05/06;
RUL-2026-11-06-128):
- each band's strip covers its WHOLE hex with the floor without any gold (no fighter keep-out, by the director's
  choice), so tick 0 shows the domain as bare stone;
- the bloom: rings ignite 4 ticks apart (ring 1 on 7, ring 4 on 19); in each hex the light runs along the rails from
  the centre to the edge midpoints in 4 ticks (a bright node at the head, a 2-tick trail on the rail, nothing under
  2 x 2 px, the cracks flaring behind); where the head passes the cover opens on the real tile (exact hand-off);
  the ring-1 cover is notched to keep the caster's head and meters clear;
- every strip is self-contained (its own hex only, no cross-hex light), so a late strip only delays its own rings;
- the seal (the ground appear, all 60 hexes, x2, hard alpha so the duplicate changes nothing): the final pulse, the
  rails at their own width ramping 27-32 (white-hot on 29), off fighter standing areas and meter rows.

Exports:
- tile_sbk_domain_v3.webp (STATIC 128 px, the spec minimum): the ground tag's staticAssetPath (3 rounds).
  floor.py, 'rails'.
- anim_sbk_wave_b{k}_v1.webp (k = 0..6, 36 x 50 ms, 150 px frames): the band visual tags' appearAnimation.
- anim_sbk_seal_v1.webp (36 x 50 ms): the ground tag's appearAnimation.
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
NF = 36
SPEED = 50
SEAL_PEAK = 29
# a band lights its OWN hex only (plus a 0.04 seam margin): each band is self-contained, so a late-loading strip
# cannot run back over a lit ring, and nothing spills past the rim onto the bare board (QA B3/B4, 2026-11-05)
EMBER = [(110, 12, 8), (184, 28, 16), (255, 74, 28), (255, 150, 60)]
BURN = [(255, 207, 74), (255, 229, 138), (255, 244, 200)]
GOLD = [(138, 90, 18), (196, 138, 28), (232, 180, 58)]   # lit demon gold (the trail cooling)
SEAL_FACE = (236, 176, 70)       # the rail face burning at about 70 % toward the burning gold
GRID, EXPORT = 50, 3
HW_S, HH_S = 132, 66             # the true-scale hex box on screen (the live still's scale)
SPAN = 4                         # ticks for the light to run from a hex's centre out to its edge midpoints = the ring
                                 # interval, so each ring's rails reach the next ring's as it ignites (QA r3 S2)
TRAIL = 2                        # ticks of burning trail behind the head
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def _mask(n, test):
    k = Image.new('L', (n, n), 0)
    p = k.load()
    h = n / RATIO
    for py in range(n):
        for px in range(n):
            x = abs(px + 0.5 - n / 2) / h
            y = (n / 2 + h / 2 - (py + 0.5)) / h          # tile heights up from the hex bottom
            if test(x, y):
                p[px, py] = 255
    return k


def keepout(n=GRID):
    """The cover has no fighter keep-out (director 2026-11-05: "I don't care if the animation covers the fighter for
    a moment"): the whole hex."""
    return Image.new('L', (n, n), 255)


def seal_keepout(n=GRID):
    """255 where the final pulse may paint: off the fighter standing areas and meter rows inside the hex (QA r3 B1):
    the hex's own fighter (+-0.35 h, from 0.15 h up), the lower hex's fighter head (+-0.35 h, up to 0.45 h) and its
    meter rows (+-0.52 h; LPC 0.22-0.6 h, AI originals 0.72-1.07 h; combatActors.ts:116-146)."""
    return _mask(n, lambda x, y: not ((x <= 0.35 and y >= 0.0) or (x <= 0.52 and 0.22 <= y <= 0.6)
                                      or (x <= 0.52 and 0.72 <= y <= 1.07)))


def caster_notch(n=GRID):
    """255 where the ring-1 cover may paint: the band 1.0 hexes include the one above the caster, whose bottom centre
    holds the caster's head and meter rows during the anticipation (QA r3 S1). A notch keeps them clear there (it
    shows a little of the tile on the other three band-1.0 hexes)."""
    return _mask(n, lambda x, y: not ((x <= 0.18 and y <= 0.45) or (x <= 0.52 and 0.22 <= y <= 0.6)))


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
    D, S_screen = screen_look(tile_dim)
    cover = T.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
    gold_raw = g50(G)
    # grow the cover 1 px where the tile's gold crosses the hex border (no gold flecks at the edge midpoints)
    grow = ImageChops.multiply(cover.filter(ImageFilter.MaxFilter(3)), gold_raw)
    cover = ImageChops.lighter(cover, grow)
    ko = keepout()
    area = ImageChops.multiply(cover, ko)
    Rn = R.resize((GRID, GRID), Image.NEAREST)
    return {'T': T, 'D': D, 'area': area, 'gold': ImageChops.multiply(g50(G), area),
            'chan': ImageChops.multiply(g50(C), area), 'crack': ImageChops.multiply(g50(K), area), 'R': Rn,
            'T_screen': T_screen, 'S_screen': S_screen, 'ko': ko, 'seal_ko': seal_keepout(),
            'notch': caster_notch(),
            'rail_tight': ImageChops.multiply(G.resize((GRID, GRID), Image.BOX).point(lambda v: 255 if v >= 170 else 0),
                                              area)}


def solid(frame, mask, colour):
    frame.paste(Image.new('RGBA', frame.size, colour + (255,)), (0, 0), mask)


def arrival(L, t, land, lo, hi):
    """Pixels the bloom front reached in [lo, hi) ticks before t: arrival = land + hex norm x SPAN."""
    def sel(v):
        n = v / 127.5
        a = land + n * SPAN
        return 255 if lo <= t - a < hi else 0
    return L['R'].point(sel)


def clean2(m):
    """Keep only pixels that belong to a full 2 x 2 block: no 1 px specks."""
    src = m.load()
    out = Image.new('L', m.size, 0)
    dst = out.load()
    w, h = m.size
    for y in range(h):
        for x in range(w):
            if not src[x, y]:
                continue
            for dx, dy in ((0, 0), (-1, 0), (0, -1), (-1, -1)):
                x0, y0 = x + dx, y + dy
                if 0 <= x0 < w - 1 and 0 <= y0 < h - 1 and src[x0, y0] and src[x0 + 1, y0] and \
                        src[x0, y0 + 1] and src[x0 + 1, y0 + 1]:
                    dst[x, y] = 255
                    break
    return out


def wave_frame(L, t, land, notch=False):
    """The director's arrival (2026-11-05/06). Until the light reaches it, the whole hex is covered with its floor
    WITHOUT gold, so the domain reads as bare stone. On the band's ignition tick the light runs out along the rails
    from the hex centre to the edge midpoints in SPAN ticks. The head is a bright node filling the rail; a 2-tick
    burning trail follows on the rail face, decaying as shortening runs (nothing under 2 x 2); the cracks flare a
    tick behind the head. Where the head has passed, the cover is open on the real tile (an exact hand-off) and
    nothing lingers."""
    f = Image.new('RGBA', (GRID, GRID), (0, 0, 0, 0))
    if t > land + SPAN + TRAIL:
        return f
    area = ImageChops.multiply(L['area'], L['notch']) if notch else L['area']
    ahead = arrival(L, t, land, -99, 0)
    f.paste(L['D'], (0, 0), ImageChops.multiply(area, ahead))
    head = arrival(L, t, land, 0, 1)
    trail1 = arrival(L, t, land, 1, 2)
    trail2 = arrival(L, t, land, 2, TRAIL + 1)
    node = ImageChops.multiply(ImageChops.multiply(L['chan'], head).filter(ImageFilter.MaxFilter(3)), L['gold'])
    solid(f, clean2(ImageChops.multiply(L['gold'], trail2)), GOLD[2])
    solid(f, clean2(ImageChops.multiply(L['gold'], trail1)), BURN[0])
    solid(f, clean2(ImageChops.lighter(node, ImageChops.multiply(L['gold'], head))), BURN[1])
    solid(f, node, BURN[2])
    solid(f, clean2(ImageChops.multiply(L['crack'], trail1)), EMBER[3])
    solid(f, clean2(ImageChops.multiply(L['crack'], trail2)), EMBER[2])
    return f


SEAL_RAMP = {27: 0.40, 28: 0.75, 29: 1.00, 30: 0.70, 31: 0.40, 32: 0.15}   # QA r3 B1
GROOVE_C = (70, 40, 10)          # the tile's rail groove (floor.py GROOVE)


def seal_frame(L, t):
    """The final pulse on the ground appear (all 60 hexes, x2, hard alpha): only the tile's own rails light, at the
    rail's width (pixels at least two-thirds rail), ramping 27-32 (white-hot on 29, the gates' held beat), off the fighter standing areas and
    meter rows."""
    f = Image.new('RGBA', (GRID, GRID), (0, 0, 0, 0))
    k = SEAL_RAMP.get(t)
    if not k:
        return f
    lerp = lambda a, b, u: tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
    col = BURN[2] if k >= 1.0 else lerp(GROOVE_C, BURN[1], k / 0.75) if k <= 0.75 else lerp(BURN[1], BURN[2], (k - 0.75) / 0.25)
    rail = ImageChops.multiply(L['rail_tight'], L['seal_ko'])        # the rail at its own width, never wider
    solid(f, rail, col)
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
    held = wave_frame(L, 7 + SPAN + TRAIL, 7)        # the last frame with anything in it: only lit rails
    first = wave_frame(L, 0, 7)
    area = on_screen(Image.merge('RGBA', [L['area']] * 4)).getchannel('A').point(lambda v: 255 if v >= 250 else 0)
    out = {}
    out['handoff'] = ('exact by construction: behind the trail the clip is transparent and the real tile shows; '
                      'the last non-empty frame (land + SPAN + TRAIL) holds only lit rail pixels')
    for name, fr in (('late_pop', first),):
        s = on_screen(to_pixels(fr).resize((GRID, GRID), Image.NEAREST))
        a, b = s.convert('RGB'), L['T_screen'].convert('RGB')
        d = ImageChops.difference(a, b).convert('L')
        px = [v for v, m in zip(d.getdata(), area.getdata()) if m]
        out[name] = {'mean_abs': round(sum(px) / len(px), 1), 'share_over_32': round(sum(v > 32 for v in px) / len(px),
                                                                                       3), 'pixels': len(px)}
    # gold visible through the cover at tick 0 (on screen): tile pixels that differ from the stone-only floor by more
    # than 32 and are not under an opaque clip pixel
    T_s, S_s = L['T_screen'].convert('RGB'), L['S_screen'].convert('RGB')
    gold = ImageChops.difference(T_s, S_s).convert('L').point(lambda v: 255 if v > 32 else 0)
    cov = on_screen(to_pixels(first).resize((GRID, GRID), Image.NEAREST)).getchannel('A')
    hexa = L['T_screen'].getchannel('A').point(lambda v: 255 if v >= 128 else 0)
    trip = list(zip(gold.getdata(), cov.getdata(), hexa.getdata()))
    gp = sum(1 for g, c, h in trip if h and g)
    out['gold_visible_t0'] = round(sum(1 for g, c, h in trip if h and g and c < 128) / max(1, gp), 3)
    return out


BANDS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]


def land_tick(b):
    """Rings ignite 4 ticks apart: whole bands at 3 + 4 d (ring 1 on tick 7, ring 4 on 19). A half band holds ring d on
    one parity and d + 1 on the other: it ignites exactly between them, at 5 + 4 d (100 ms late on one parity, 100 ms
    early on the other)."""
    d = math.floor(b)
    return 3 + 4 * d + (2 if b != d else 0)


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
    FL.MODE = 'stone'
    tile_dim = FL.tile(size=128)
    FL.MODE = 'full'
    L = layers(tile_full, tile_dim)
    meta = {'ratio': RATIO, 'speed': SPEED, 'tile': 'rails', 'order': 'rings', 'assets': {}, 'groups': []}
    G = groups()
    for k, (land, offs) in enumerate(G):
        name = f'anim_sbk_wave_b{k}_v1.webp'
        strip([wave_frame(L, t, land, notch=(k == 0)) for t in range(NF)]).save(os.path.join(OUT, name), lossless=True, method=6)
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
