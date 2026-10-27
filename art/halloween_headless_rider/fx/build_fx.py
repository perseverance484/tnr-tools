#!/usr/bin/env python3
"""Hellfire Harvest + Aura of Despair: assets and battlefield simulation from the art director's layers.

    python3 build_fx.py            # all exports + all previews
    python3 build_fx.py --assets   # exports only
    python3 build_fx.py --previews # previews only (needs exports)

Exports (exports/), one gameAsset each:
  tile_hellfire_scorch.webp      STATIC     Hellfire Harvest recoil effect     staticAssetPath
  anim_hellfire_appear.webp      ANIMATION  Hellfire Harvest damage effect     appearAnimation
  tile_aura_mist.webp            STATIC     Aura of Despair pool-cost effect   staticAssetPath
  anim_aura_appear.webp          ANIMATION  Aura of Despair pool-cost effect   appearAnimation
  anim_aura_loop.webp            ANIMATION  Aura of Despair pool-cost effect   staticAnimation
  anim_aura_disappear.webp       ANIMATION  Aura of Despair pool-cost effect   disappearAnimation

Battlefield model (TheNinjaRPG 58801f9; see fxkit.py for the citations):
  - COMBAT battles are 12 x 10 FLAT hexes (libs/combat/util.ts battle sizes); hexsize = width / 9.25; hex height 0.5 w.
  - Effect groups sit at z = EFFECTS_LAYER (-6). Inside a group the still (staticAssetPath) is at +0, so -6: UNDER the
    units (USER_LAYER -4). Appear and static animations are at +5, so -1: OVER the units and their status bars (-3).
  - Hellfire Harvest is method ALL: one ground effect on every tile (libs/combat/targeting.ts getTargetTiles).
  - Aura of Despair is AOE_SPIRAL_SHOOT, range 5: every tile within 5 hex steps of the CASTER, except his own tile.
  - All tiles of one cast start their animations on the same tick; a later cast's still is drawn over an earlier one.
"""
import argparse
import math
import os
import random
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fxkit as fx  # noqa: E402

HH = os.path.join(fx.ART, 'hellfire_harvest', 'raws')
AD = os.path.join(fx.ART, 'aura_of_despair', 'raws')
OUT = fx.EXPORTS
PREV = os.path.join(fx.HERE, 'previews')

HELL_TILE = 'tile_rider_domain.webp'   # the domain floor (domain_tile.py); 'tile_hellfire_scorch.webp' was v2
MS = {'hellfire_appear': 40, 'aura_appear': 50, 'aura_loop': 70, 'aura_disappear': 60}
OPACITY = {'scorch': 0.62, 'mist': 0.50}


def L(path):
    return Image.open(path).convert('RGBA')


def W(code):
    return L(os.path.join(fx.WORK, f'{code}.png'))


def prep():
    """Trimmed working copies and split pieces (idempotent)."""
    for d, names in ((HH, ['T1_scorch', 'B1_scythe_blade', 'C1_slash_arc', 'F1_flame_burst', 'G1_grin', 'E1_embers']),
                     (AD, ['M1_mist_pool', 'L1_lantern_flare', 'R1_mist_ring', 'W1_wisps', 'D1_gutter'])):
        for n in names:
            code = n.split('_')[0]
            if not os.path.exists(os.path.join(fx.WORK, f'{code}.png')):
                fx.ingest(os.path.join(d, f'{n}_raw.png'), code)
    if not os.path.exists(os.path.join(fx.WORK, 'E1_00.png')):
        fx.split(os.path.join(HH, 'E1_embers_raw.png'), 'E1', 1500)
    if not os.path.exists(os.path.join(fx.WORK, 'W1_00.png')):
        fx.split(os.path.join(AD, 'W1_wisps_raw.png'), 'W1', 8000)


# Split pieces, classified from the contact sheet (2026-10-26): W1_00 and W1_06 carry the faces; E1_07/08/12 are ash.
FACES = ['W1_00', 'W1_06']
PLAIN_WISPS = ['W1_01', 'W1_02', 'W1_03', 'W1_04', 'W1_05', 'W1_07']
EMBERS = ['E1_00', 'E1_01', 'E1_02', 'E1_04', 'E1_05', 'E1_06', 'E1_09', 'E1_10', 'E1_11', 'E1_13', 'E1_14']
ASH = ['E1_07', 'E1_08', 'E1_12']

# Frame geometry: the effect square is 50 units centred on the tile; at a 360 px phone canvas the hex is 38.9 x 19.5
# units, so the hex footprint inside the frame is 0.78 wide and 0.39 tall around the centre. The ground line is y 0.5.
HEX_W, HEX_H = 0.78, 0.39
GROUND = 0.5


# ----------------------------------------------------------------------------------------------- Hellfire Harvest
def hellfire_appear():
    """0.72 s, built for 120 copies at once (method ALL). Simulation v1 showed the full blade + tall burst + grin on every
    tile merges into a solid wall of fire that hides every unit, and 120 synced grins read as clutter. So each tile gets
    only what reads as ONE wave across the board: the slash sweeps low along the ground, the ground ignites, short
    flame tongues lick up (under a third of the frame), embers spit and fall, and the scorch is left behind. The scythe
    blade and the grin are kept for the jutsu icon and promo art rather than repeated per tile."""
    slash, burst, scorch = W('C1'), W('F1'), W('T1')
    embers = [W(e) for e in EMBERS[:5]] + [W(ASH[0])]
    rnd = random.Random(7)
    flight = [(rnd.uniform(-0.28, 0.28), rnd.uniform(-0.2, -0.1), rnd.uniform(0.04, 0.06), rnd.uniform(-40, 40))
              for _ in embers]
    frames = []
    n = 18
    for i in range(n):
        t = i / (n - 1)
        fr = fx.frame()
        # the slash runs along the ground line, flattened, left to right: across the board it reads as one sweep
        st = fx.seg(t, 0.0, 0.3)
        if st > 0 and t < 0.7:
            fx.place(fr, fx.wipe(slash, st, 'lr'), 0.5, GROUND + 0.01, 0.9, 0.95 * (1 - fx.seg(t, 0.35, 0.7)),
                     squash=0.42)
        # the ground ignites behind it and settles into the scorch still
        sa = fx.seg(t, 0.12, 0.32) * (1 - 0.65 * fx.seg(t, 0.5, 1.0))
        fx.place(fr, scorch, 0.5, GROUND + 0.02, HEX_W * (0.75 + 0.25 * fx.ease_out(fx.seg(t, 0.12, 0.35))), sa,
                 squash=fx.HEX_ASPECT)
        # short flame tongues: low, wide, quick
        ft = fx.seg(t, 0.18, 0.42)
        if ft > 0 and t < 0.8:
            hgt = 0.18 + 0.32 * fx.ease_out(ft) * (1 - 0.6 * fx.seg(t, 0.5, 0.8))
            wid = 0.5
            h_frac = burst.height / burst.width * wid * hgt
            fx.place(fr, burst, 0.5, GROUND + 0.05 - h_frac / 2, wid, 0.9 * (1 - fx.seg(t, 0.55, 0.8)), squash=hgt)
        # embers spit up a little and fall
        et = fx.seg(t, 0.35, 1.0)
        if et > 0:
            for img, (dx, dy, w, rot) in zip(embers, flight):
                x = 0.5 + dx * fx.ease_out(et)
                y = GROUND - 0.02 + dy * math.sin(math.pi * min(1, et * 1.1))
                fx.place(fr, img, x, y, w, 1 - fx.seg(et, 0.5, 1.0), rot=rot * et)
        frames.append(fr)
    return frames


# ----------------------------------------------------------------------------------------------- Aura of Despair
def aura_appear():
    """0.70 s: the lantern flare pulses on the ground and a ring of black-red mist rolls outward and settles."""
    flare, ring, gutter = W('L1'), W('R1'), W('D1')
    frames = []
    n = 14
    for i in range(n):
        t = i / (n - 1)
        fr = fx.frame()
        ga = 0.55 * fx.seg(t, 0.25, 0.8)
        fx.place(fr, gutter, 0.5, GROUND + 0.03, HEX_W * 0.85, ga, squash=fx.HEX_ASPECT)
        rt = fx.ease_out(fx.seg(t, 0.12, 1.0))
        fx.place(fr, ring, 0.5, GROUND, 0.3 + 0.62 * rt, fx.seg(t, 0.1, 0.25) * (1 - 0.55 * fx.seg(t, 0.7, 1.0)),
                 squash=fx.HEX_ASPECT)
        fa = fx.seg(t, 0.0, 0.14) * (1 - fx.seg(t, 0.3, 0.55))
        fx.place(fr, flare, 0.5, GROUND - 0.01, 0.35 + 0.5 * fx.ease_out(fx.seg(t, 0.0, 0.5)), fa,
                 squash=fx.HEX_ASPECT)
        frames.append(fr)
    return frames


def aura_loop():
    """2.8 s seamless, built for the whole range-5 patch drifting in sync. Simulation v1 showed tall rising wisps line up
    into vertical stripes across the patch, so the smoke now stays low: two short trails per tile drift sideways on a
    shared wind just above the ground and thin out before they leave the tile, under a breathing dull-red underlight.
    The patch reads as one fog bank creeping across the board. A face shows for two frames per cycle."""
    gutter = W('D1')
    wisps = [W(w) for w in PLAIN_WISPS[:2]]
    face = W(FACES[0])
    n = 40
    frames = []

    def path(p, k):
        x = 0.18 + 0.64 * p
        y = GROUND - 0.05 - 0.09 * p + 0.02 * math.sin(2 * math.pi * (p + k * 0.5))
        return x, y

    for i in range(n):
        ph = i / n
        fr = fx.frame()
        breath = 0.36 + 0.16 * (0.5 + 0.5 * math.sin(2 * math.pi * ph))
        fx.place(fr, gutter, 0.5, GROUND + 0.03, HEX_W * 0.9, breath, squash=fx.HEX_ASPECT)
        for k, img in enumerate(wisps):
            p = (ph + k / len(wisps)) % 1.0
            x, y = path(p, k)
            a = 0.5 * math.sin(math.pi * p) ** 1.3
            fx.place(fr, img, x, y, 0.16, a, rot=-62 + 8 * math.sin(2 * math.pi * p), squash=0.55)
        if i in (22, 23):
            x, y = path((ph + 0.0) % 1.0, 0)
            fx.place(fr, face, x, y - 0.06, 0.16, 0.55 if i == 22 else 0.3)
        frames.append(fr)
    return frames


def aura_disappear():
    """0.72 s: the light gutters out and the mist sinks into the ground."""
    gutter, ring = W('D1'), W('R1')
    wisps = [W(w) for w in PLAIN_WISPS[3:5]]
    frames = []
    n = 12
    for i in range(n):
        t = i / (n - 1)
        fr = fx.frame()
        flick = 1 - t if i % 3 else (1 - t) * 0.6
        fx.place(fr, gutter, 0.5, GROUND + 0.03, HEX_W * 0.85, 0.55 * flick, squash=fx.HEX_ASPECT)
        fx.place(fr, ring, 0.5, GROUND + 0.02 * t, 0.9 - 0.35 * fx.ease_in(t), 0.5 * (1 - t),
                 squash=fx.HEX_ASPECT * (1 - 0.4 * t))
        for k, img in enumerate(wisps):
            fx.place(fr, img, 0.38 + 0.24 * k, GROUND - 0.18 + 0.12 * t, 0.12, 0.5 * (1 - t), squash=1 - 0.5 * t)
        frames.append(fr)
    return frames


# ----------------------------------------------------------------------------------------------- exports
def assets():
    prep()
    os.makedirs(OUT, exist_ok=True)
    fx.static_tile(os.path.join(fx.WORK, 'T1.png'), os.path.join(OUT, 'tile_hellfire_scorch.webp'), OPACITY['scorch'])
    fx.static_tile(os.path.join(fx.WORK, 'M1.png'), os.path.join(OUT, 'tile_aura_mist.webp'), OPACITY['mist'])
    fx.save_strip(hellfire_appear(), 'anim_hellfire_appear', MS['hellfire_appear'])
    fx.save_strip(aura_appear(), 'anim_aura_appear', MS['aura_appear'])
    fx.save_strip(aura_loop(), 'anim_aura_loop', MS['aura_loop'])
    fx.save_strip(aura_disappear(), 'anim_aura_disappear', MS['aura_disappear'])


# ----------------------------------------------------------------------------------------------- simulation
CANVAS_CSS, COLS, ROWS, SCALE = 360, 12, 10, 3


def geometry():
    hexsize = CANVAS_CSS / (COLS - fx.STACK * (COLS - 1)) * SCALE
    w, h = hexsize, hexsize * fx.HEX_ASPECT
    tiles = {}
    for c in range(COLS):
        for r in range(ROWS):
            tiles[(c, r)] = (c * w * (1 - fx.STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))
    return tiles, w, h, (int(CANVAS_CSS * SCALE), int((ROWS + 0.5) * h)), fx.EFFECT * SCALE


def cube(c, r):
    q = c
    rr = r - (c - (c & 1)) // 2
    return q, rr, -q - rr


def hexdist(a, b):
    x1, y1, z1 = cube(*a)
    x2, y2, z2 = cube(*b)
    return max(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))


def battlefield(tiles, w, h, size):
    """The procedural grass-and-sand board the game draws under everything (TILES / DIRT layers), approximated."""
    rnd = random.Random(3)
    img = Image.new('RGBA', size, (20, 34, 18, 255))
    d = ImageDraw.Draw(img)
    for (c, r), (x, y) in tiles.items():
        n = math.sin(c * 0.7) + math.cos(r * 0.9) + rnd.uniform(-0.4, 0.4)
        base = (214, 196, 128) if n > 1.25 else (58 + int(14 * n), 118 + int(16 * n), 46 + int(8 * n))
        poly = [(x - w / 2, y), (x - w / 4, y - h / 2), (x + w / 4, y - h / 2), (x + w / 2, y), (x + w / 4, y + h / 2),
                (x - w / 4, y + h / 2)]
        d.polygon(poly, fill=base + (255,), outline=(0, 0, 0, 60))
        for _ in range(3):
            gx, gy = x + rnd.uniform(-w / 3, w / 3), y + rnd.uniform(-h / 4, h / 4)
            d.line((gx, gy, gx + 2, gy - 6), fill=(30, 80, 30, 255), width=2)
    return img


def unit_layer(units, tiles, h):
    """Round portraits on their tiles (libs/threejs/combat.ts createUserSprite): avatar 0.8 h, 0.5 h above the centre,
    on a white marker with a village-colour rim. Drawn between the stills and the animations."""
    rider = L(os.path.join(fx.ART, 'headless_rider_avatar.webp'))
    out = []
    for pos, kind in units:
        x, y = tiles[pos]
        r = int(0.8 * h)
        disc = Image.new('L', (r, r), 0)
        ImageDraw.Draw(disc).ellipse((0, 0, r - 1, r - 1), fill=255)
        face = rider.resize((r, r), Image.LANCZOS) if kind == 'rider' else Image.new('RGBA', (r, r), (70, 100, 160, 255))
        port = Image.new('RGBA', (r + 10, r + 10), (0, 0, 0, 0))
        dd = ImageDraw.Draw(port)
        dd.ellipse((0, 0, r + 9, r + 9), fill=(160, 20, 20, 255) if kind == 'rider' else (40, 90, 200, 255))
        dd.ellipse((2, 2, r + 7, r + 7), fill=(245, 245, 245, 255))
        inner = Image.new('RGBA', (r, r), (0, 0, 0, 0))
        inner.paste(face, (0, 0), disc)
        port.alpha_composite(inner, (5, 5))
        out.append((port, (int(x - port.width / 2), int(y - 0.5 * h - port.height / 2))))
    return out


class Cast:
    def __init__(self, name, start_ms, tiles, still=None, appear=None, appear_ms=40, loop=None, loop_ms=70,
                 disappear=None, disappear_ms=60, end_ms=None):
        self.name, self.start, self.tiles = name, start_ms, tiles
        self.still = L(still) if still else None
        self.appear = fx.strip_frames(appear) if appear else []
        self.loop = fx.strip_frames(loop) if loop else []
        self.disappear = fx.strip_frames(disappear) if disappear else []
        self.ams, self.lms, self.dms, self.end = appear_ms, loop_ms, disappear_ms, end_ms


def simulate(out_name, casts, units, seconds, tick=40, label=''):
    tiles, w, h, size, eff = geometry()
    base = battlefield(tiles, w, h, size)
    ulayer = unit_layer(units, tiles, h)
    cache = {}

    def sized(img, wh):
        k = (id(img), wh)
        if k not in cache:
            cache[k] = img.resize(wh, Image.BOX if wh[0] < img.width else Image.LANCZOS)
        return cache[k]

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    frames = []
    for ms in range(0, int(seconds * 1000), tick):
        c = base.copy()
        live = [k for k in casts if ms >= k.start and (k.end is None or ms < k.end + len(k.disappear) * k.dms)]
        # stills (z -6), in cast order: under the units
        for k in live:
            if k.still and (k.end is None or ms < k.end):
                st = sized(k.still, (int(w), int(h)))
                for t in k.tiles:
                    x, y = tiles[t]
                    c.alpha_composite(st, (int(x - w / 2), int(y - h / 2)))
        for img, pos in ulayer:
            c.alpha_composite(img, pos)
        # animations (z -1): over the units
        for k in live:
            el = ms - k.start
            layer = []
            if k.end is not None and ms >= k.end:
                di = (ms - k.end) // k.dms
                if di < len(k.disappear):
                    layer.append(k.disappear[di])
            else:
                if k.loop:
                    layer.append(k.loop[(el // k.lms) % len(k.loop)])
                ai = el // k.ams
                if ai < len(k.appear):
                    layer.append(k.appear[ai])
            for fr in layer:
                f2 = sized(fr, (eff, eff))
                for t in k.tiles:
                    x, y = tiles[t]
                    c.alpha_composite(f2, (int(x - eff / 2), int(y - eff / 2)))
        if label:
            ImageDraw.Draw(c).text((14, 10), label, font=font, fill=(255, 255, 255, 230), stroke_width=3,
                                   stroke_fill=(0, 0, 0, 255))
        frames.append(c.convert('RGB'))
    os.makedirs(PREV, exist_ok=True)
    gif = os.path.join(PREV, out_name + '.gif')
    half = [f.resize((f.width // 2, f.height // 2), Image.LANCZOS) for f in frames]
    half[0].save(gif, save_all=True, append_images=half[1:], duration=tick, loop=0, optimize=True)
    mp4 = os.path.join(PREV, out_name + '.mp4')
    tmp = os.path.join(PREV, '_f')
    os.makedirs(tmp, exist_ok=True)
    for i, f in enumerate(frames):
        f.save(os.path.join(tmp, f'{i:05d}.png'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(1000 // tick), '-i', os.path.join(tmp, '%05d.png'),
                    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                    '-pix_fmt', 'yuv420p', mp4], check=True)
    for p in os.listdir(tmp):
        os.remove(os.path.join(tmp, p))
    os.rmdir(tmp)
    print(f'{out_name}: {len(frames)} frames, {size[0]}x{size[1]} -> {gif} ({os.path.getsize(gif)//1024} KB), '
          f'{mp4} ({os.path.getsize(mp4)//1024} KB)')
    return gif, mp4


def previews():
    tiles, *_ = geometry()
    rider = (3, 4)
    units = [(rider, 'rider'), ((6, 3), 'p'), ((7, 6), 'p'), ((9, 2), 'p')]
    every = list(tiles)
    spiral = [t for t in tiles if t != rider and hexdist(t, rider) <= 5]
    E = lambda n: os.path.join(OUT, n)
    hell = lambda start, end=None: Cast('hellfire', start, every, E(HELL_TILE),
                                        E('anim_hellfire_appear.webp'), MS['hellfire_appear'], end_ms=end)
    aura = lambda start, end=None: Cast('aura', start, spiral, E('tile_aura_mist.webp'), E('anim_aura_appear.webp'),
                                        MS['aura_appear'], E('anim_aura_loop.webp'), MS['aura_loop'],
                                        E('anim_aura_disappear.webp'), MS['aura_disappear'], end_ms=end)
    simulate('hellfire_harvest_battlefield', [hell(400)], units, 3.2, label='Hellfire Harvest (all tiles)')
    simulate('aura_of_despair_battlefield', [aura(400, 5200)], units, 6.4,
             label='Aura of Despair (range 5 around the Rider)')
    simulate('combined_battlefield', [hell(300), aura(1900)], units, 7.0,
             label='Hellfire Harvest, then Aura of Despair')
    close(units)


def close(units):
    """One tile, large: scorch still, mist still, then the loops, as they stack in the combined state."""
    E = lambda n: os.path.join(OUT, n)
    scorch, mist = L(E(HELL_TILE)), L(E('tile_aura_mist.webp'))
    happ, aapp, aloop = (fx.strip_frames(E(n)) for n in ('anim_hellfire_appear.webp', 'anim_aura_appear.webp',
                                                         'anim_aura_loop.webp'))
    Z = 8
    tw, th, eff = int(38.9 * Z), int(19.5 * Z), 50 * Z
    size = (eff + 160, eff + 60)
    cx, cy = size[0] // 2, size[1] // 2 + 20
    bg = Image.new('RGBA', size, (58, 118, 46, 255))
    d = ImageDraw.Draw(bg)
    d.polygon([(cx - tw / 2, cy), (cx - tw / 4, cy - th / 2), (cx + tw / 4, cy - th / 2), (cx + tw / 2, cy),
               (cx + tw / 4, cy + th / 2), (cx - tw / 4, cy + th / 2)], outline=(0, 0, 0, 120), width=3)
    frames = []
    tick = 40
    t0h, t0a = 200, 1200
    for ms in range(0, 4200, tick):
        c = bg.copy()
        if ms >= t0h:
            c.alpha_composite(scorch.resize((tw, th), Image.LANCZOS), (cx - tw // 2, cy - th // 2))
        if ms >= t0a:
            c.alpha_composite(mist.resize((tw, th), Image.LANCZOS), (cx - tw // 2, cy - th // 2))
        r = int(0.8 * th)
        ImageDraw.Draw(c).ellipse((cx - r // 2, cy - th // 2 - r // 2, cx + r // 2, cy - th // 2 + r // 2),
                                  fill=(70, 100, 160, 255), outline=(245, 245, 245, 255), width=5)
        layer = []
        if ms >= t0a:
            layer.append(aloop[((ms - t0a) // MS['aura_loop']) % len(aloop)])
            ai = (ms - t0a) // MS['aura_appear']
            if ai < len(aapp):
                layer.append(aapp[ai])
        if ms >= t0h:
            hi = (ms - t0h) // MS['hellfire_appear']
            if hi < len(happ):
                layer.append(happ[hi])
        for fr in layer:
            c.alpha_composite(fr.resize((eff, eff), Image.NEAREST), (cx - eff // 2, cy - eff // 2))
        frames.append(c.convert('RGB'))
    gif = os.path.join(PREV, 'combined_closeup.gif')
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=tick, loop=0, optimize=True)
    print(f'combined_closeup: {len(frames)} frames -> {gif} ({os.path.getsize(gif)//1024} KB)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--assets', action='store_true')
    ap.add_argument('--previews', action='store_true')
    a = ap.parse_args()
    if a.assets or not a.previews:
        assets()
    if a.previews or not a.assets:
        previews()
