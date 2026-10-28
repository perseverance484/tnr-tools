#!/usr/bin/env python3
"""Skyglass boss FX v2: the shared danger language animated from the director's drawn key art.

    python3 art/skyglass_boss_fx/animate.py

Inputs (raw/, the director's art sessions, 2026-10-28, style anchored on the Crownbreaker badge v2):
  raw_fx_safe_star.png, raw_fx_heavy_ring.png, raw_fx_binding_seal.png, raw_fx_bile_seep.png,
  raw_fx_ember_eruption.png, raw_fx_crystal_shards.png (all on a magenta key).
Outputs: exports/anim_<id>_v2.webp (vertical strips of 50 px frames) and docs/design/skyglass_boss_fx/v2_* previews.

Engine facts this follows (theninjarpg 2af4b32; measured in v1, build_fx.py on fable/skyglass-boss-fx):
- every effect is one 50 x 50 world-unit sprite centred on its hex, drawn over the characters; the CDN serves the strip
  at ?width=50, so frames are drawn natively at 50 px (no resample of the pixel grid);
- the hex covers about 36 x 18 px of the frame (flat-topped, 2:1);
- three.js magnifies with linear filtering, so RGB under transparent pixels is filled from the nearest drawn pixel and
  every frame keeps a 1 px transparent margin;
- all marks laid in one round start on the same tick, so every loop shares one pulse (peak on frame 0);
- every hex of one effect plays the same frame at the same time (no per-hex stagger is possible).
Alpha is stepped (0 / 130 / 255): no gradients, no anti-aliasing. Scaling to 50 px is a box reduction plus palette
quantisation, with the drawn black outline protected.
"""
import math
import os

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
RAW = os.path.join(HERE, 'raw')
EXPORTS = os.path.join(HERE, 'exports')
DOCS = os.path.join(ROOT, 'docs', 'design', 'skyglass_boss_fx')
VERSION = 'v2'
N = 50          # frame size
MS = 50         # ms per frame (the asset's speed)
BEAT = 16       # shared pulse: 16 x 50 ms = 0.8 s
MAX_BYTES = 460800


# ------------------------------------------------------------------------------------------------ key art handling
def keyed(name, dist=75):
    a = np.array(Image.open(os.path.join(RAW, name)).convert('RGBA')).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    a[..., 3] = np.where(np.sqrt((r - 255) ** 2 + g ** 2 + (b - 255) ** 2) < dist, 0, 255)
    im = Image.fromarray(a.astype('uint8'))
    return im.crop(im.getbbox())


def reduce(img, w, h, colors=12, thr=140, soft=None, outline=0.30):
    """Box-reduce to w x h, quantise, step the alpha, and keep the drawn outline where it dominated the source block."""
    src = np.array(img).astype(float)
    small = np.array(img.resize((w, h), Image.BOX)).astype(float)
    alpha = small[..., 3]
    rgb = Image.fromarray(small[..., :3].astype('uint8')).quantize(colors, method=Image.MEDIANCUT).convert('RGB')
    rgb = np.array(rgb).astype(int)
    dark = ((src[..., :3].mean(-1) < 45) & (src[..., 3] > 0)).astype(float)
    dfrac = np.array(Image.fromarray((dark * 255).astype('uint8')).resize((w, h), Image.BOX)).astype(float) / 255
    ink = np.array([10, 10, 16])
    rgb = np.where((dfrac > outline)[..., None], ink, rgb)
    if soft is None:
        al = np.where(alpha > thr, 255, 0)
    else:
        al = np.where(alpha > thr, 255, np.where(alpha > soft, 130, 0))
    return Image.fromarray(np.dstack([rgb, al]).astype('uint8'))


def radial(img):
    a = np.array(img).astype(int)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    return a, np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)), a[..., :3].mean(-1)


def bright(img, f):
    a = np.array(img).astype(float)
    a[..., :3] = np.clip(a[..., :3] * f, 0, 255)
    return Image.fromarray(a.astype('uint8'))


def tint(img, mul):
    a = np.array(img).astype(float)
    a[..., :3] = np.clip(a[..., :3] * np.array(mul), 0, 255)
    return Image.fromarray(a.astype('uint8'))


def with_alpha(img, level):
    a = np.array(img).copy()
    a[..., 3] = np.where(a[..., 3] > 0, min(level, 255), 0)
    return Image.fromarray(a)


def frame():
    return Image.new('RGBA', (N, N), (0, 0, 0, 0))


def put(f, img, x, y):
    f.alpha_composite(img, (int(round(x)), int(round(y))))


def px(f, x, y, rgb, a=255):
    x, y = int(round(x)), int(round(y))
    if 1 <= x < N - 1 and 1 <= y < N - 1:
        f.putpixel((x, y), (*rgb, a))


def pulse(i, period=BEAT):
    """1.0 at frame 0 (peak), 0.0 at half period."""
    return 0.5 + 0.5 * math.cos(2 * math.pi * i / period)


def finish(frames):
    """1 px clear margin; RGB under transparent pixels filled from the nearest drawn pixel (no dark fringe when the GPU
    interpolates); one vertical strip."""
    out = []
    for f in frames:
        a = np.array(f).copy()
        a[0, :, 3] = a[-1, :, 3] = 0
        a[:, 0, 3] = a[:, -1, 3] = 0
        drawn = a[..., 3] > 0
        if drawn.any():
            _, (iy, ix) = ndimage.distance_transform_edt(~drawn, return_indices=True)
            a[..., :3] = a[iy, ix, :3]
        out.append(Image.fromarray(a))
    strip = Image.new('RGBA', (N, N * len(out)))
    for i, f in enumerate(out):
        strip.paste(f, (0, i * N))
    return strip


# ------------------------------------------------------------------------------------------------ the six animations
def build():
    star = keyed('raw_fx_safe_star.png')
    ring = keyed('raw_fx_heavy_ring.png')
    seal = keyed('raw_fx_binding_seal.png', dist=70)
    pool = keyed('raw_fx_bile_seep.png', dist=70)
    erupt = keyed('raw_fx_ember_eruption.png', dist=80)
    shards_src = keyed('raw_fx_crystal_shards.png', dist=80)
    anims = {}

    # tg_heavy: a hollow cracked ember ring (characters stay visible inside it); each beat a crack-light runs inward.
    a, rr, lum = radial(ring)
    hollow = a.copy(); hollow[..., 3] = np.where((rr < 0.62) & (lum < 90), 0, a[..., 3])
    cracks = a.copy(); cracks[..., 3] = np.where((rr < 0.62) & (lum > 150), 255, 0)
    ring_t = reduce(Image.fromarray(hollow.astype('uint8')), 32, 16)
    crack_t = reduce(Image.fromarray(cracks.astype('uint8')), 32, 16, thr=60, outline=1.1)
    fr = []
    for i in range(BEAT):
        p = pulse(i)
        f = frame()
        put(f, bright(ring_t, 0.78 + 0.32 * p), 9, 17)
        if i < 5:  # crack light runs inward on the beat, then fades
            put(f, with_alpha(bright(crack_t, 1.15), 255 if i < 2 else 130), 9, 17)
        fr.append(f)
    anims['tg_heavy'] = fr

    # tg_control: a chain ring with a small lock set in its top edge; the lock glints on the beat and the seal sigil
    # flashes inside.
    a, rr, lum = radial(seal)
    hollow = a.copy(); hollow[..., 3] = np.where(rr < 0.66, 0, a[..., 3])
    sig = a.copy(); sig[..., 3] = np.where((rr < 0.5) & (lum > 110), 255, 0)
    w0, h0 = seal.size
    lock = seal.crop((int(w0 * 0.40), 0, int(w0 * 0.60), int(h0 * 0.24))); lock = lock.crop(lock.getbbox())
    chain_t = reduce(bright(Image.fromarray(hollow.astype('uint8')), 1.35), 34, 17)
    sig_t = reduce(Image.fromarray(sig.astype('uint8')), 18, 9, thr=60, outline=1.1)
    lock_t = reduce(lock, 8, int(round(8 * lock.height / lock.width)))
    fr = []
    for i in range(BEAT):
        p = pulse(i)
        f = frame()
        put(f, bright(chain_t, 0.8 + 0.3 * p), 8, 17)
        put(f, bright(lock_t, 0.9 + 0.35 * p), 25 - lock_t.width // 2, 14)
        if i in (0, 1):  # glint
            px(f, 25 + 1, 15, (255, 255, 255)); px(f, 25 + 2, 14, (240, 230, 255))
        fr.append(f)
    anims['tg_control'] = fr

    # tg_linger: a sicklier, tighter bile pool; the dark interior is translucent; bubbles rise and pop.
    a, rr, lum = radial(pool)
    a[..., 3] = np.where((rr < 0.62) & (lum < 70), 150, a[..., 3])
    pool_t = reduce(tint(Image.fromarray(a.astype('uint8')), (1.0, 0.9, 0.6)), 30, 15, thr=170, soft=110, outline=0.6)
    period = BEAT * 3 // 2  # 1.2 s
    bubbles = [(17, 24, 0), (30, 22, 8), (24, 27, 15)]
    fr = []
    for i in range(period):
        p = pulse(i, period)
        f = frame()
        put(f, bright(pool_t, 0.85 + 0.2 * p), 10, 18)
        for bx, by, t0 in bubbles:
            k = (i - t0) % period
            if k < 6:  # grows for 5 frames, pops on the 6th
                r = 1 + k // 2
                col = (190, 220, 60) if k < 5 else (240, 255, 150)
                for dx in range(-r, r + 1):
                    for dy in range(-r, r + 1):
                        if abs(math.hypot(dx, dy * 1.6) - r) < 0.7:
                            px(f, bx + dx, by + dy, col)
                if k == 5:
                    for dx, dy in ((-2, -1), (2, -1), (0, -2)):
                        px(f, bx + dx, by + dy, (240, 255, 150))
        fr.append(f)
    anims['tg_linger'] = fr

    # tg_safe: the emblem floats over its own faint reflection on the hex, bobbing; motes of light rise from the hex.
    ground = reduce(star, 34, 17)
    emblem = reduce(star, 22, 22)
    period = BEAT * 2  # 1.6 s
    motes = [(14, 0), (36, 9), (22, 17), (30, 25)]
    fr = []
    for i in range(period):
        p = pulse(i, period)
        f = frame()
        put(f, with_alpha(bright(ground, 0.9 + 0.2 * p), 130), 8, 17)
        bob = round(1.5 * math.sin(2 * math.pi * i / period))
        put(f, bright(emblem, 0.95 + 0.2 * p), 14, 2 + bob)
        for mx, t0 in motes:
            k = (i - t0) % period
            if k < 14:
                y = 30 - k * 1.6
                px(f, mx + (1 if k % 6 > 3 else 0), y, (200, 245, 255) if k < 10 else (120, 200, 240), 255 if k < 10 else 130)
        fr.append(f)
    anims['tg_safe'] = fr

    # dt_heavy: ring flash, the eruption rises in 3 frames, one bright hold, then it breaks apart into flying chunks
    # while the ground cracks glow and fade. 12 frames (0.6 s).
    er = reduce(erupt, 34, int(round(34 * erupt.height / erupt.width)), colors=14)
    ew, eh = er.size
    base_x, base_y = 25 - ew // 2, 36 - eh
    ring_flash = bright(ring_t, 1.4)
    rng = np.random.RandomState(7)
    chunks = [(25 + rng.randint(-8, 9), 24 + rng.randint(-6, 4), rng.uniform(-2.2, 2.2), rng.uniform(-3.2, -1.6))
              for _ in range(9)]
    fr = []
    for i in range(12):
        f = frame()
        if i <= 1:
            put(f, ring_flash, 9, 17)
        if 1 <= i <= 3:  # rise: reveal from the ground up
            k = i / 3
            vis = int(eh * k)
            part = er.crop((0, eh - vis, ew, eh))
            put(f, part if i < 3 else bright(part, 1.25), base_x, base_y + (eh - vis))
        elif i == 4:  # hold, hottest frame
            put(f, bright(er, 1.3), base_x, base_y)
        elif 5 <= i <= 7:  # the column collapses from the top
            cut = int(eh * (i - 4) / 4)
            part = er.crop((0, cut, ew, eh))
            put(f, with_alpha(bright(part, 1.0 - 0.1 * (i - 5)), 255 if i < 7 else 130), base_x, base_y + cut)
        if i >= 4:  # debris chunks fly and fall
            t = i - 4
            for cx, cy, vx, vy in chunks:
                x, y = cx + vx * t, cy + vy * t + 0.45 * t * t
                col = (60, 30, 24) if t > 4 else (255, 170, 60)
                px(f, x, y, col); px(f, x + 1, y, col)
        if i >= 5:  # cracked ground glows, then fades
            put(f, with_alpha(bright(crack_t, 1.1), 255 if i < 9 else 130), 9, 17)
            put(f, with_alpha(bright(ring_t, 0.7 - 0.05 * (i - 5)), 130), 9, 17)
        fr.append(f)
    anims['dt_heavy'] = fr

    # dt_shard: a skyglass shard falls point-first onto the hex and shatters (Crownfall, Shardstorm). 12 frames.
    lab, _ = ndimage.label(np.array(shards_src)[..., 3] > 0)
    objs = sorted([s for s in ndimage.find_objects(lab) if (lab[s] > 0).sum() > 2000], key=lambda s: (s[0].start // 300, s[1].start))
    sh = shards_src.crop((objs[1][1].start, objs[1][0].start, objs[1][1].stop, objs[1][0].stop))
    sh_t = reduce(sh, 9, int(round(9 * sh.height / sh.width)), colors=8)
    sw, shh = sh_t.size
    fr = []
    burst = [(math.cos(a) * 1.0, math.sin(a) * 0.5) for a in np.linspace(0, 2 * math.pi, 10, endpoint=False)]
    for i in range(12):
        f = frame()
        land = 27 - shh
        if i < 5:  # the fall, with a short trail
            y = -shh + (land + shh) * (i / 4) ** 1.6
            put(f, sh_t, 25 - sw // 2, y)
            for t in range(1, 4):
                px(f, 25, y - 2 * t, (200, 240, 255), 130)
        if i == 5:  # impact: white flash on the hex, the shard still standing
            put(f, bright(sh_t, 1.6), 25 - sw // 2, land)
            for k in range(20):
                ang = 2 * math.pi * k / 20
                px(f, 25 + math.cos(ang) * 6, 27 + math.sin(ang) * 3, (255, 255, 255))
        if i >= 6:  # shatter: fragments spray up and fall, a light ring spreads on the ground
            t = i - 5
            for bx, by in burst:
                x, y = 25 + bx * t * 2.4, 24 + by * t * 1.5 - 2.6 * t + 0.55 * t * t
                col = (235, 250, 255) if t < 3 else (130, 200, 240)
                px(f, x, y, col, 255 if t < 5 else 130); px(f, x, y + 1, (90, 160, 220), 255 if t < 5 else 130)
            rad = 6 + t * 2.2
            for k in range(30):
                ang = 2 * math.pi * k / 30
                px(f, 25 + math.cos(ang) * rad, 27 + math.sin(ang) * rad / 2, (160, 225, 255), 255 if t < 3 else 130)
        fr.append(f)
    anims['dt_shard'] = fr
    return anims


def export(anims):
    os.makedirs(EXPORTS, exist_ok=True)
    out = {}
    for aid, frames in anims.items():
        strip = finish(frames)
        p = os.path.join(EXPORTS, f'anim_{aid}_{VERSION}.webp')
        strip.save(p, lossless=True, quality=100, method=6)
        size = os.path.getsize(p)
        assert size < MAX_BYTES, (aid, size)
        out[aid] = (p, len(frames), size)
        print(f'{aid}: {len(frames)} frames x {MS} ms, {size} bytes')
    return out


# ------------------------------------------------------------------------------------------------ v3: tiles under, glints over
# Director 2026-10-28: marks play under the characters. An effect's staticAssetPath is a plain Sprite with depthTest on,
# placed on EFFECTS_LAYER (-6) behind the users (USER_LAYER -4, whose avatar sprites write depth), and stretched to the
# hex box (libs/threejs/combat.ts ~632-641): so a STILL tile draws under the characters and fills the hex. Animations
# (ActionSprite, depthTest false, drawn after the users) always draw over them. Precedent: Hellfire Harvest's domain
# tile (art/halloween_headless_rider/release/tile_hrh_rider_domain_pumpkin.webp, a square stretched to the hex).
# So each mark = a STILL tile of the director's full art (under) + a light glint animation that only touches the
# tile's rim and empty space (over). The tile is a 50 px square (the delivered width); the game squashes it to the
# 2:1 hex, so the art is drawn round in the square.
TILE = 50
RX, RY = 17, 8.5     # the ring's rim in frame px, as the hex shows it (36 x 18 hex, art filling about 94%)


def tile(img, colors=16, fill=0.94):
    w = int(TILE * fill)
    t = reduce(img, w, w, colors=colors)
    f = Image.new('RGBA', (TILE, TILE), (0, 0, 0, 0))
    f.alpha_composite(t, ((TILE - w) // 2, (TILE - w) // 2))
    return f


def rim(f, i, period, rgb, n=3, phase=0.0, rx=RX, ry=RY, cy=25):
    for k in range(n):
        ang = 2 * math.pi * (i / period + k / n + phase)
        x, y = 25 + math.cos(ang) * rx, cy + math.sin(ang) * ry
        px(f, x, y, rgb)
        px(f, x - math.sin(ang) * 1.2, y + math.cos(ang) * 0.6, rgb, 130)


def build_v3():
    star = keyed('raw_fx_safe_star.png')
    tiles = {'heavy': tile(keyed('raw_fx_heavy_ring.png')),
             'control': tile(keyed('raw_fx_binding_seal.png', dist=70)),
             'linger': tile(tint(keyed('raw_fx_bile_seep.png', dist=70), (1.0, 0.92, 0.65)), fill=0.9),
             'safe': tile(star, fill=0.9)}
    glints = {}
    fr = []  # heavy: three embers race round the rim; a hot flash of the rim on the beat
    for i in range(BEAT):
        f = frame()
        rim(f, i, BEAT, (255, 220, 120))
        if i < 2:
            for k in range(40):
                ang = 2 * math.pi * k / 40
                px(f, 25 + math.cos(ang) * RX, 25 + math.sin(ang) * RY, (255, 170, 60), 255 if i == 0 else 130)
        fr.append(f)
    glints['heavy'] = fr
    fr = []  # control: a lilac spark runs the chain; the lock (top of the rim) glints on the beat
    for i in range(BEAT):
        f = frame()
        rim(f, i, BEAT, (225, 200, 255), n=2, phase=0.25)
        if i in (0, 1):
            px(f, 25, 25 - RY, (255, 255, 255)); px(f, 26, 25 - RY - 1, (240, 230, 255)); px(f, 24, 25 - RY + 1, (240, 230, 255), 130)
        fr.append(f)
    glints['control'] = fr
    period = BEAT * 3 // 2  # linger: bubbles rise and pop at the pool's rim
    bubbles = [(13, 23, 0), (36, 24, 8), (25, 31, 15), (29, 19, 20)]
    fr = []
    for i in range(period):
        f = frame()
        for bx, by, t0 in bubbles:
            k = (i - t0) % period
            if k < 6:
                r = 1 + k // 2
                col = (200, 230, 70) if k < 5 else (245, 255, 160)
                for dx in range(-r, r + 1):
                    for dy in range(-r, r + 1):
                        if abs(math.hypot(dx, dy * 1.6) - r) < 0.7:
                            px(f, bx + dx, by + dy, col)
                if k == 5:
                    for dx, dy in ((-2, -1), (2, -1), (0, -2)):
                        px(f, bx + dx, by + dy, (245, 255, 160))
        fr.append(f)
    glints['linger'] = fr
    # safe: two beacon pillars of skyglass light rise at the hex's left and right corners, framing whoever stands there
    # (the emblem itself is the floor tile; nothing crosses the portrait).
    period = BEAT * 2
    fr = []
    for i in range(period):
        p = pulse(i, period)
        f = frame()
        for x0 in (10, 40):
            top = int(6 + 4 * (1 - p))
            for y in range(top, 27):
                k = (y - top) / max(1, 26 - top)
                col = (235, 252, 255) if k < 0.25 else (150, 225, 255) if k < 0.7 else (80, 170, 235)
                px(f, x0, y, col, 255 if k > 0.15 else 130)
                if k > 0.5:
                    px(f, x0 + (1 if x0 < 25 else -1), y, (80, 170, 235), 130)
            for t0 in (0, 11, 21):  # motes climbing the pillar
                kk = (i - t0) % period
                if kk < 12:
                    px(f, x0 + (1 if x0 < 25 else -1) * (1 + (kk // 3) % 2), 26 - kk * 1.7, (220, 250, 255))
        fr.append(f)
    glints['safe'] = fr
    return tiles, glints


def export_v3():
    tiles, glints = build_v3()
    for name, t in tiles.items():
        p = os.path.join(EXPORTS, f'tile_{name}_v3.webp')
        t.save(p, lossless=True, quality=100, method=6)
        print(f'tile_{name}: {os.path.getsize(p)} bytes')
    for name, frames in glints.items():
        frames = mind_portrait(frames, 'clear')
        p = os.path.join(EXPORTS, f'anim_{name}_v3.webp' if name.startswith('dt_') else f'anim_{name}_glint_v3.webp')
        finish(frames).save(p, lossless=True, quality=100, method=6)
        assert os.path.getsize(p) < MAX_BYTES
        print(f'anim_{name}_glint: {len(frames)} frames, {os.path.getsize(p)} bytes')
    return tiles, glints


def build_dt_heavy_v3():
    """The heavy blast, portrait-mindful: three smaller eruptions burst from the ring's rim (left, right and front)
    instead of one column through the middle; chunks fly outward, the rim flashes and the cracks glow."""
    erupt = keyed('raw_fx_ember_eruption.png', dist=80)
    small = reduce(erupt, 9, int(round(9 * erupt.height / erupt.width)), colors=10)
    sw, sh = small.size
    spots = [(11, 29), (39, 29)]   # rim left and right (base points): the only room clear of every portrait
    rng = np.random.RandomState(7)
    chunks = [(sx + rng.randint(-2, 3), sy - 6, (sx - 25) / 10 + rng.uniform(-0.8, 0.8), rng.uniform(-2.8, -1.4))
              for sx, sy in spots for _ in range(3)]
    fr = []
    for i in range(12):
        f = frame()
        if i <= 1:
            for k in range(40):
                ang = 2 * math.pi * k / 40
                px(f, 25 + math.cos(ang) * RX, 25 + math.sin(ang) * RY, (255, 230, 150))
        for sx, sy in spots:
            if 1 <= i <= 3:
                vis = int(sh * i / 3)
                part = small.crop((0, sh - vis, sw, sh))
                put(f, part if i < 3 else bright(part, 1.25), sx - sw // 2, sy - vis)
            elif i == 4:
                put(f, bright(small, 1.3), sx - sw // 2, sy - sh)
            elif 5 <= i <= 7:
                cut = int(sh * (i - 4) / 4)
                put(f, with_alpha(small.crop((0, cut, sw, sh)), 255 if i < 7 else 130), sx - sw // 2, sy - sh + cut)
        if i >= 4:
            t = i - 4
            for cx, cy, vx, vy in chunks:
                col = (60, 30, 24) if t > 4 else (255, 170, 60)
                px(f, cx + vx * t, cy + vy * t + 0.45 * t * t, col)
        if i >= 3:  # rim embers glow and fade
            for k in range(0, 40, 2):
                ang = 2 * math.pi * k / 40
                px(f, 25 + math.cos(ang) * RX, 25 + math.sin(ang) * RY, (255, 140, 50) if i < 9 else (140, 60, 30), 255 if i < 9 else 130)
        fr.append(f)
    return fr


# ------------------------------------------------------------------------------------------------ portrait safety
# Director 2026-10-28: "The animations should be mindful of player portraits" ... "Explosions and other temporary effects
# can do whatever, I meant the tile effects that are always playing." So the looping glints over the mark tiles keep clear
# of every portrait; the one-shot blasts (dt_heavy, dt_shard) are unrestricted. Measured on the battle still (hex centre (311, 225.5), 184.1 still px per
# 50 frame px): the portrait disc is centred 9.2 px above the hex centre with radius 9 frame px, and the health bars sit
# 17-22 px above it. In frame px: disc (25, 15.8) r 9.5, bars x 16-34, y 2-9.
PORTRAIT_C, PORTRAIT_R = (25.0, 15.8), 9.5


def portrait_mask():
    """Every portrait this sprite can overlap: its own hex's and the six neighbours'. Portraits rise above their hex, so
    the hex below's portrait sits on this hex's lower half. In frame px: column step 27, row step 18, odd columns half a
    row offset; each portrait a disc of radius 9.5 centred 9.2 px above its hex centre, health bars above that."""
    yy, xx = np.mgrid[0:N, 0:N]
    m = np.zeros((N, N), bool)
    for dx, dy in ((0, 0), (0, -18), (0, 18), (-27, -9), (-27, 9), (27, -9), (27, 9)):
        cx, cy = PORTRAIT_C[0] + dx, PORTRAIT_C[1] + dy
        m |= np.hypot(xx - cx, yy - cy) <= PORTRAIT_R
        m |= (xx >= cx - 10) & (xx <= cx + 10) & (yy >= cy - 15) & (yy <= cy - 7)
    return m


def mind_portrait(frames, mode):
    """mode 'clear': drop every pixel over the portrait (glints); 'veil': hold them at the 130 step (emblem, blasts) so
    the face still shows through."""
    m = portrait_mask()
    out = []
    for f in frames:
        a = np.array(f).copy()
        if mode == 'clear':
            a[..., 3] = np.where(m, 0, a[..., 3])
        else:
            a[..., 3] = np.where(m & (a[..., 3] > 130), 130, a[..., 3])
        out.append(Image.fromarray(a))
    return out


if __name__ == '__main__':
    export(build())
    export_v3()
