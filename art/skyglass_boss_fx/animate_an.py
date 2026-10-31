#!/usr/bin/env python3
"""Skyglass boss FX AN01-AN09: animation strips from the director-approved raw layers (2026-10-31).

    python3 art/skyglass_boss_fx/animate_an.py

Inputs: raw/an/AN0n_raw_fx_<slug>.png (1254 x 1254, native RGBA alpha, one element each; requested in
docs/handoffs/SKYGLASS_ART_PROMPTS.md section 5).
Outputs:
  exports/anim_fx_<slug>_v1.webp   vertical strips, one square frame per row
  exports/tile_fx_<slug>_v1.webp   STATIC stills (AN03 barrier, AN06 ember tile)
  exports/anim_fx_spreading_fire_glint_v1.webp  the portrait-clear glint that pairs with the AN06 tile
  exports/an_v1.json               per file: frames, speed (ms per frame), suggested use
  docs/design/skyglass_boss_fx/an_v1_*.png  preview sheets

House method (animate.py, boss_fx.py): every frame is drawn on the 50 px grid the combat sprite is served at, with
stepped alpha, a 1 px clear margin, outline protection and the RGB under transparent pixels filled from the nearest
drawn pixel. Every loop peaks on frame 0 and shares the 0.8 s beat.

Delivered size. The ANIMATION target in skills/producing-tnr-art/data/25x_DATA_art_spec.json sets a 112 px minimum
frame width (the content list's 112 px canvas downloads the original sheet), which the earlier 50 px strips fail. So
each 50 px frame is delivered enlarged x3 by nearest neighbour (150 px frames): the CDN's ?width=50 rendition is an
exact 3:1 reduction back to the drawn grid, and the 112 px canvas gets a crisp image instead of a 50 px one.
DELIVER_SCALE = 1 reproduces the earlier 50 px convention.

Fades use an ordered dither of the drawn pixels rather than the 130 alpha step where the 130 step would push a strip
over the spec's soft-edge ceiling (house_style.measured_signature.soft_edge_share_max).
"""
import importlib.util
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, f'{name}.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


A = _load('animate')
B = _load('boss_fx')
N, EXPORTS, DOCS = A.N, A.EXPORTS, A.DOCS
RAW_AN = os.path.join(HERE, 'raw', 'an')
VERSION = 'v1'
MS = A.MS             # 50 ms per frame
BEAT = A.BEAT         # 16 frames = 0.8 s
DELIVER_SCALE = 3     # 50 px drawn grid -> 150 px delivered frames (spec min_width 112)
MAX_BYTES = A.MAX_BYTES

SLUGS = {
    'AN01': 'command_banner', 'AN02': 'phase_shift', 'AN03': 'gunwale_barrier', 'AN04': 'core_enrage',
    'AN05': 'hexweave', 'AN06': 'spreading_fire_embers', 'AN07': 'bile_glob', 'AN08': 'bile_splash',
    'AN09': 'undertow',
}


# ------------------------------------------------------------------------------------------------ raw handling
def raw(an, thr=128, mid=420):
    """Native-alpha loader (the AN raws carry real alpha, not a magenta key). The generator left a faint haze of
    alpha 1-15 across much of each canvas; it is dropped by thresholding, and the subject's alpha (mostly 250-254) is
    made fully opaque. Cropped to the subject and box-reduced to an intermediate of `mid` px on the long side, which
    keeps the drawn outline several pixels wide for reduce()'s outline protection and keeps warps/rotations cheap."""
    im = Image.open(os.path.join(RAW_AN, f'{an}_raw_fx_{SLUGS[an]}.png')).convert('RGBA')
    a = np.array(im)
    a[..., 3] = np.where(a[..., 3] >= thr, 255, 0)
    im = Image.fromarray(a)
    im = im.crop(im.getbbox())
    k = mid / max(im.size)
    if k < 1:
        im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.BOX)
    return im


def fit(img, w=None, h=None, colors=20, outline=0.55, gain=1.0, thr=140):
    """reduce() to a box, keeping the aspect unless both sides are given."""
    if w is None:
        w = max(1, round(h * img.width / img.height))
    if h is None:
        h = max(1, round(w * img.height / img.width))
    if gain != 1.0:
        img = A.bright(img, gain)
    return A.reduce(img, w, h, colors=colors, thr=thr, outline=outline)


def dither(img, level):
    """Fade without partial alpha: keep `level` (0..1) of the drawn pixels on a 4x4 Bayer pattern."""
    bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16 + 1 / 32
    a = np.array(img).copy()
    h, w = a.shape[:2]
    m = np.tile(bayer, (h // 4 + 1, w // 4 + 1))[:h, :w]
    a[..., 3] = np.where(m < level, a[..., 3], 0)
    return Image.fromarray(a)


def put_c(f, img, cx, cy):
    A.put(f, img, cx - img.width / 2, cy - img.height / 2)


def own_face():
    """This sprite's own portrait disc (animate.py PORTRAIT_C / PORTRAIT_R) and its health bars."""
    yy, xx = np.mgrid[0:N, 0:N]
    cx, cy = A.PORTRAIT_C
    disc = np.hypot(xx - cx, yy - cy) <= A.PORTRAIT_R
    bars = (xx >= cx - 10) & (xx <= cx + 10) & (yy >= cy - 15) & (yy <= cy - 7)
    return disc, bars


def mask_face(f, clear_bars=False, veil_disc=False):
    disc, bars = own_face()
    a = np.array(f).copy()
    if veil_disc:
        a[..., 3] = np.where(disc & (a[..., 3] > 130), 130, a[..., 3])
    else:
        a[..., 3] = np.where(disc, 0, a[..., 3])
    if clear_bars:
        a[..., 3] = np.where(bars, 0, a[..., 3])
    return Image.fromarray(a)


def drop(f, x, y, rgb, ink=(18, 12, 16)):
    """A 2 px droplet with a dark lower pixel."""
    A.px(f, x, y, rgb)
    A.px(f, x, y + 1, ink)


# ------------------------------------------------------------------------------------------------ the animations
def an01_command_banner():
    """Aura loop on the Captain: the banner stands at his left shoulder and snaps in the wind behind him. A ripple runs
    along the cloth from the pole to the torn hem; the pole stays still. The cloth passes behind the Captain: his own
    portrait disc and health bars are kept clear. 16 frames, one beat."""
    src = raw('AN01', mid=360)
    W, H = src.size
    s = np.array(src)
    pole_x = 0.10 * W   # the pole is the left ~10% of the drawn width; the cloth flies to the right
    yy, xx = np.mgrid[0:H, 0:W]
    reach = np.clip((xx - pole_x) / (W - pole_x), 0, 1)
    out = []
    for i in range(BEAT):
        ph = 2 * math.pi * i / BEAT
        dy = 0.05 * H * reach ** 1.2 * np.sin(ph - 2 * math.pi * xx / (0.7 * W))
        dx = -0.025 * W * reach * (0.5 + 0.5 * np.cos(ph - 2 * math.pi * yy / H))
        sy = np.clip(np.round(yy - dy), 0, H - 1).astype(int)
        sx = np.clip(np.round(xx - dx), 0, W - 1).astype(int)
        warped = Image.fromarray(s[sy, sx])
        t = fit(warped, h=36, colors=16, gain=1.25, thr=70)  # thr 70 keeps the 1 px pole whole
        f = A.frame()
        A.put(f, A.bright(t, 0.95 + 0.15 * A.pulse(i)), 2, 3)
        if i in (0, 1):  # the cyan emblem glints on the beat
            ex, ey = 2 + 0.52 * t.width, 3 + 0.33 * t.height
            A.px(f, ex, ey, (255, 255, 255)); A.px(f, ex + 1, ey - 1, (200, 240, 250))
        out.append(mask_face(f, clear_bars=True))
    return out


def an02_phase_shift():
    """Cast flourish: the frost ring bursts outward from the boss's feet, flashes white, and its shards fly off while
    the ring thins away. 12 frames."""
    src = raw('AN02')
    full = fit(src, w=48, colors=16, gain=1.1)
    scales = [0.30, 0.50, 0.70, 0.86, 0.96, 1.0, 1.0]
    out = []
    for i in range(12):
        f = A.frame()
        if i < 7:
            w = max(6, round(48 * scales[i]))
            r = fit(src, w=w, colors=16, gain=1.1) if w != 48 else full
            put_c(f, A.bright(r, 1.55 if i == 3 else 1.25 if i == 4 else 1.0), 25, 30)
        else:
            k = i - 6
            put_c(f, dither(A.bright(full, 1.0 - 0.06 * k), 1 - k / 6), 25, 30 - k)
            for j in range(14):  # shards flung out along the ring
                ang = 2 * math.pi * j / 14 + 0.2
                rx, ry = 22 + k * 2.4, 10 + k * 1.2
                A.px(f, 25 + math.cos(ang) * rx, 30 + math.sin(ang) * ry - k, (230, 250, 255) if k < 3 else (120, 190, 230))
        out.append(f)
    return out


def an03_gunwale_barrier():
    """Raise the Gunwale: the timber wall rises out of the deck in front of the boss, slams with a dust kick, and
    holds. In the held frames the wall veils the portrait (130 step) so the face still reads. 12 frames; the last
    frame is the STATIC still."""
    src = raw('AN03')
    wall = fit(src, w=42, colors=18)
    ww, wh = wall.size
    base = 46
    out = []
    for i in range(12):
        f = A.frame()
        if i <= 4:
            vis = round(wh * [0.25, 0.5, 0.75, 0.95, 1.0][i])
            part = wall.crop((0, 0, ww, vis))           # the top comes up first, out of the deck
            A.put(f, part, 25 - ww // 2, base - vis + (2 if i == 4 else 0))
        else:
            A.put(f, A.bright(wall, 1.3 if i == 5 else 1.0), 25 - ww // 2, base - wh)
        if 4 <= i <= 8:  # dust and splinters kicked out at the base
            k = i - 3
            for j, side in enumerate((-1, 1)):
                for d in range(3):
                    x = 25 + side * (ww / 2 - 2 + k * 1.6 + d)
                    y = base - 1 - d - (k * 0.8 if d else 0) + 0.25 * k * k
                    A.px(f, x, y, (150, 130, 115) if k < 4 else (100, 88, 80))
        an03_gunwale_barrier.held = f   # the unveiled held frame, for the STATIC still (drawn under the characters)
        out.append(mask_face(f, veil_disc=True) if i >= 6 else f)
    return out


def an04_core_enrage():
    """Aura loop on the Core Horror: the rot ring hangs round it, breathing on the beat; drips fall from its lower arc
    and the skyglass flecks glint. The boss's own portrait disc stays clear. 32 frames (two beats)."""
    src = raw('AN04')
    ringt = fit(src, w=46, colors=18, gain=1.1)
    rw, rh = ringt.size
    cx, cy = 25, 21
    drips = [(13, 34, 0), (21, 39, 9), (31, 38, 4), (38, 33, 13), (26, 40, 20), (17, 37, 26)]
    period = 2 * BEAT
    out = []
    for i in range(period):
        p = A.pulse(i)
        f = A.frame()
        put_c(f, A.bright(ringt, 0.88 + 0.25 * p), cx, cy + (1 if p < 0.3 else 0))
        for x, y0, t0 in drips:
            k = (i - t0) % period
            if k < 8:
                y = y0 + 0.18 * k * k
                if y < N - 2:
                    drop(f, x, y, (168, 194, 58) if k < 5 else (107, 143, 30))
        if i in (0, 1, 16, 17):
            for gx, gy in ((10, 15), (40, 24), (18, 36)):
                A.px(f, gx, gy, (225, 245, 250))
        out.append(mask_face(f))
    return out


def an05_hexweave():
    """Hit: the violet knot winds itself shut on the target (spins in from wide and loose to tight), flashes, pulses
    tight twice, then flicks ink droplets off its edges and frays away. Reads apart from chain_wrap (chains rising in a
    spiral) and the binding seal (a chain ring). 12 frames."""
    src = raw('AN05')
    out = []
    rng = np.random.RandomState(5)
    flecks = [(rng.uniform(0, 2 * math.pi), rng.uniform(1.6, 2.6)) for _ in range(10)]
    for i in range(12):
        f = A.frame()
        if i <= 3:
            ang = [70, 40, 18, 0][i]
            w = [24, 30, 36, 38][i]
            r = fit(src.rotate(ang, resample=Image.BICUBIC, expand=True), w=w, colors=14, gain=1.05)
            put_c(f, r if i < 3 else A.bright(r, 1.5), 25, 24)
        elif i <= 8:
            w = 38 if i % 2 == 0 else 36
            put_c(f, fit(src, w=w, colors=14, gain=1.05), 25, 24)
        else:
            k = i - 8
            put_c(f, dither(fit(src, w=38, colors=14), 1 - k / 4), 25, 24)
        if i >= 6:
            k = i - 5
            for ang, sp in flecks:
                x, y = 25 + math.cos(ang) * (12 + sp * k), 24 + math.sin(ang) * (9 + sp * k * 0.6) + 0.3 * k * k
                A.px(f, x, y, (150, 100, 210) if k < 4 else (60, 30, 90))
        out.append(f)
    return out


def an06_ember_patch(w=38, h=22):
    return fit(raw('AN06'), w=w, h=h, colors=18, gain=1.05)


def ember_flicker(img, i, period=BEAT, seed=3):
    """Brighten and dim the ember cracks (warm, bright pixels) in patches that drift out of phase with each other."""
    a = np.array(img).astype(float)
    h, w = a.shape[:2]
    rng = np.random.RandomState(seed)
    phase = np.array(Image.fromarray((rng.rand(max(2, h // 4), max(2, w // 4)) * 255).astype('uint8'))
                     .resize((w, h), Image.BILINEAR)).astype(float) / 255 * 2 * math.pi
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hot = (r > 170) & (r > b + 60) & (a[..., 3] > 0)
    k = 0.72 + 0.42 * (0.5 + 0.5 * np.cos(2 * math.pi * i / period + phase))
    k = np.where(hot, k, 1.0)
    a[..., :3] = np.clip(a[..., :3] * k[..., None], 0, 255)
    return Image.fromarray(a.astype('uint8'))


def an06_tile():
    """STATIC drain tile (staticAssetPath: stretched to the hex box and drawn UNDER the characters, like the v3 mark
    tiles). The raw is already drawn foreshortened at about 3:2, so it is stretched to a square first; the game's 2:1
    hex stretch then gives it back a ground-plane look."""
    src = raw('AN06')
    sq = src.resize((max(src.size), max(src.size)), Image.BOX)
    return A.tile(sq, colors=18, fill=0.94)


def an06_glint():
    """The loop that pairs with the tile (drawn OVER the characters, so portrait-clear like the v3 glints): sparks lift
    off the patch's rim and a few low flame tongues flicker at its left and right ends. 16 frames."""
    out = []
    sparks = [(9, 0), (16, 5), (34, 2), (41, 9), (12, 11), (38, 13), (22, 7), (29, 14)]
    for i in range(BEAT):
        f = A.frame()
        for x0, t0 in sparks:
            k = (i - t0) % BEAT
            if k < 7:
                y0 = 25 + 7.5 * math.sin(math.acos(max(-1, min(1, (x0 - 25) / 17))))
                A.px(f, x0 + (1 if (k // 2) % 2 else 0), y0 - 1.6 * k, (255, 236, 150) if k < 3 else (255, 140, 50) if k < 5 else (150, 50, 30))
        for x0 in (8, 42):  # flame tongues
            hgt = 2 + (i + (0 if x0 < 25 else 5)) % 3
            for d in range(hgt):
                A.px(f, x0, 27 - d, (255, 230, 120) if d == hgt - 1 else (240, 90, 30))
        out.append(f)
    return A.mind_portrait(out, 'clear')


def an06_patch_loop():
    """ALTERNATIVE, the whole patch as an ANIMATION loop (staticAnimation): the ember cracks flicker and sparks rise.
    It is drawn OVER the characters, so it covers the feet of whoever stands on the hex and the lower half of the
    portrait of the hex below; the tile + glint pair is the recommended use. 16 frames."""
    patch = an06_ember_patch()
    out = []
    for i in range(BEAT):
        f = A.frame()
        put_c(f, ember_flicker(patch, i), 25, 27)
        for x0, t0 in ((13, 0), (24, 6), (35, 3), (19, 11), (31, 13)):
            k = (i - t0) % BEAT
            if k < 7:
                A.px(f, x0 + (k // 2) % 2, 22 - 1.7 * k, (255, 236, 150) if k < 3 else (255, 140, 50) if k < 5 else (150, 50, 30))
        out.append(f)
    return out


def an07_bile_glob():
    """Layer 1 of 2 (cast/hit): the glob drops in from the upper right along its own tail line and lands on the hex,
    squashing on the last frame. The splash (AN08) plays on landing. 8 frames."""
    src = raw('AN07')
    glob = fit(src, w=26, colors=16, gain=1.05)
    gw, gh = glob.size
    path = [(47, -2), (43, 2), (38, 6), (34, 12), (31, 18), (28, 23), (26, 27)]
    out = []
    for i in range(8):
        f = A.frame()
        if i < 7:
            x, y = path[i]
            put_c(f, glob, x, y)
            if i >= 1:  # a few drips shed behind it
                px_, py_ = path[i - 1]
                drop(f, px_ + 7, py_ - 5, (168, 194, 58))
        else:
            sq = glob.resize((round(gw * 1.2), round(gh * 0.7)), Image.NEAREST)
            put_c(f, A.bright(sq, 1.2), 25, 31)
        out.append(f)
    return out


def an08_bile_splash():
    """Layer 2 of 2: the splash bursts flat across the hex, holds wet, then its droplets fall back and it sinks away
    into the deck. 12 frames."""
    src = raw('AN08')
    full = fit(src, w=46, colors=16, gain=1.05)
    fw, fh = full.size
    out = []
    rng = np.random.RandomState(9)
    drops = [(rng.uniform(-1, 1), rng.uniform(-2.8, -1.4)) for _ in range(10)]
    for i in range(12):
        f = A.frame()
        if i <= 2:
            w = [18, 32, 44][i]
            put_c(f, A.bright(fit(src, w=w, colors=16, gain=1.05), 1.3 if i == 2 else 1.0), 25, 29)
        elif i <= 6:
            put_c(f, full if i != 3 else A.bright(full, 1.15), 25, 29)
        else:
            k = i - 6
            flat = full.resize((fw, max(2, round(fh * (1 - 0.1 * k)))), Image.NEAREST)
            put_c(f, dither(A.bright(flat, 1 - 0.06 * k), 1 - k / 6), 25, 29 + k * 0.6)
        if 2 <= i <= 9:
            t = i - 1
            for vx, vy in drops:
                drop(f, 25 + vx * 20 + vx * t * 1.6, 27 + vy * t + 0.42 * t * t, (216, 232, 106) if t < 4 else (168, 194, 58))
        out.append(f)
    return out


def an09_undertow():
    """Hit: the water streak rushes in from the left across the target, crests with a white flash, then drains away
    tail-first, throwing spray. 10 frames."""
    src = raw('AN09')
    s = fit(src, w=48, colors=16, gain=1.05)
    sw, sh = s.size
    out = []
    for i in range(10):
        f = A.frame()
        a = np.array(s).copy()
        xx = np.arange(sw)[None, :]
        if i <= 3:  # the streak slides in from the left, crest leading, and flashes as it crests
            img = Image.fromarray(a)
            put_c(f, img if i < 3 else A.bright(img, 1.45), 25 - [30, 18, 8, 0][i], 27)
        elif i <= 5:
            put_c(f, s, 25 + (i - 3), 27)
        else:  # it drains away tail-first, thinning, and throws spray off the crest
            k = i - 5
            keep = xx >= sw * k / 5
            a[..., 3] = np.where(keep, a[..., 3], 0)
            put_c(f, dither(Image.fromarray(a), 1 - k / 5), 25 + 2 + k, 27)
            for j in range(6):
                A.px(f, 25 + sw / 2 - 8 + 2 * j, 27 - 8 - k * 1.5 + (j % 3) + 0.5 * k * k,
                     (220, 245, 250) if k < 3 else (110, 170, 190))
        out.append(f)
    return out


# ------------------------------------------------------------------------------------------------ export
def deliver(strip):
    if DELIVER_SCALE == 1:
        return strip
    return strip.resize((strip.width * DELIVER_SCALE, strip.height * DELIVER_SCALE), Image.NEAREST)


def save_strip(name, frames):
    p = os.path.join(EXPORTS, f'{name}_{VERSION}.webp')
    deliver(A.finish(frames)).save(p, lossless=True, quality=100, method=6)
    size = os.path.getsize(p)
    assert size < MAX_BYTES, (name, size)
    return p, size


def save_still(name, img):
    a = np.array(img).copy()
    a[0, :, 3] = a[-1, :, 3] = 0
    a[:, 0, 3] = a[:, -1, 3] = 0
    still = A.finish([Image.fromarray(a)])
    p = os.path.join(EXPORTS, f'{name}_{VERSION}.webp')
    deliver(still).save(p, lossless=True, quality=100, method=6)
    size = os.path.getsize(p)
    assert size < MAX_BYTES, (name, size)
    return p, size


def build():
    """(an, file stem, frames, kind, use, note)"""
    return [
        ('AN01', 'anim_fx_command_banner', an01_command_banner(), 'ANIMATION', 'static',
         'cp_command aura loop on the Captain (buff staticAnimation); 16 frames = one 0.8 s beat'),
        ('AN02', 'anim_fx_phase_shift', an02_phase_shift(), 'ANIMATION', 'appear',
         'cc_phase_shift cast flourish (appearAnimation on the boss self effect)'),
        ('AN03', 'anim_fx_gunwale_barrier', an03_gunwale_barrier(), 'ANIMATION', 'appear',
         'cp_gunwale barrier rises and holds (appearAnimation); pair with tile_fx_gunwale_barrier for the held state'),
        ('AN04', 'anim_fx_core_enrage', an04_core_enrage(), 'ANIMATION', 'static',
         'ch_enrage aura loop on the Core Horror (buff staticAnimation); 32 frames = two beats'),
        ('AN05', 'anim_fx_hexweave', an05_hexweave(), 'ANIMATION', 'appear',
         'cc_hexweave hit (appearAnimation on the hit hex)'),
        ('AN06', 'anim_fx_spreading_fire_glint', an06_glint(), 'ANIMATION', 'static',
         'Spreading Fire: portrait-clear spark/flame loop drawn over the tile_fx_spreading_fire_embers still (recommended pair)'),
        ('AN06', 'anim_fx_spreading_fire_embers', an06_patch_loop(), 'ANIMATION', 'static',
         'ALTERNATIVE Spreading Fire loop: the whole patch flickering; draws over the characters and the lower portrait of the hex below'),
        ('AN07', 'anim_fx_bile_glob', an07_bile_glob(), 'ANIMATION', 'appear',
         'ch_bile_spit layer 1: glob drops onto the hex (appearAnimation); AN08 plays on landing'),
        ('AN08', 'anim_fx_bile_splash', an08_bile_splash(), 'ANIMATION', 'appear',
         'ch_bile_spit layer 2: splash (appearAnimation on the damage effect)'),
        ('AN09', 'anim_fx_undertow', an09_undertow(), 'ANIMATION', 'appear',
         'ch_undertow hit (appearAnimation); optional move, still a PROBE'),
    ]


def export():
    os.makedirs(EXPORTS, exist_ok=True)
    os.makedirs(DOCS, exist_ok=True)
    rows, listing = [], []
    items = build()
    for an, stem, frames, kind, use, note in items:
        p, size = save_strip(stem, frames)
        listing.append({'an': an, 'file': os.path.relpath(p, A.ROOT), 'type': kind, 'frames': len(frames), 'speed': MS,
                        'speed_unit': 'ms per frame (gameAsset.speed)', 'duration_ms': len(frames) * MS,
                        'frame_px': N * DELIVER_SCALE, 'drawn_grid_px': N, 'bytes': size, 'use': use, 'note': note})
        rows.append((an, stem, frames))
        print(f'{an} {stem}: {len(frames)} frames x {MS} ms, {size} bytes')
    stills = [('AN03', 'tile_fx_gunwale_barrier', an03_gunwale_barrier.held,
               'cp_gunwale held barrier as a STATIC still (the strip\'s held frame, unveiled: a staticAssetPath draws '
               'under the characters). The game stretches a staticAssetPath to the 2:1 hex box, so the wall is shown '
               'squashed; prefer the strip if that reads too flat'),
              ('AN06', 'tile_fx_spreading_fire_embers', an06_tile(),
               'Spreading Fire drain tile, STATIC (staticAssetPath, stretched to the hex, drawn under the characters)')]
    for an, stem, img, note in stills:
        p, size = save_still(stem, img)
        listing.append({'an': an, 'file': os.path.relpath(p, A.ROOT), 'type': 'STATIC', 'frames': 1, 'speed': None,
                        'frame_px': N * DELIVER_SCALE, 'drawn_grid_px': N, 'bytes': size, 'use': 'static', 'note': note})
        print(f'{an} {stem}: still, {size} bytes')
    with open(os.path.join(EXPORTS, f'an_{VERSION}.json'), 'w') as fh:
        json.dump({'source': 'art/skyglass_boss_fx/raw/an/ (director-approved 2026-10-31)',
                   'builder': 'art/skyglass_boss_fx/animate_an.py',
                   'layout': 'vertical strip, one square frame per row',
                   'speed_note': 'gameAsset.speed is ms per frame (as push/*_animation.gen.py use it)',
                   'use_values': 'appear = effect appearAnimation (plays once); static = staticAnimation loop or, '
                                 'for STATIC files, staticAssetPath; disappear = disappearAnimation',
                   'assets': listing}, fh, indent=1)
        fh.write('\n')
    previews(rows, stills)
    return listing


# ------------------------------------------------------------------------------------------------ previews
BG = (52, 56, 64, 255)


def guides(img, z):
    """Faint hex (36 x 18) and portrait disc guides on a magnified frame."""
    d = ImageDraw.Draw(img)
    cx, cy = 25 * z, 25 * z
    hx = [(cx - 18 * z, cy), (cx - 9 * z, cy - 9 * z), (cx + 9 * z, cy - 9 * z), (cx + 18 * z, cy),
          (cx + 9 * z, cy + 9 * z), (cx - 9 * z, cy + 9 * z)]
    d.polygon(hx, outline=(90, 96, 108))
    pc, pr = A.PORTRAIT_C, A.PORTRAIT_R
    d.ellipse([(pc[0] - pr) * z, (pc[1] - pr) * z, (pc[0] + pr) * z, (pc[1] + pr) * z], outline=(110, 90, 90))


def magnified(fr, z):
    big = Image.new('RGBA', (N * z, N * z), BG)
    guides(big, z)
    big.alpha_composite(fr.resize((N * z, N * z), Image.NEAREST))
    return big


def sheet_for(stem, frames, keys=6):
    z_all, z_key = 2, 5
    n = len(frames)
    idx = sorted(set(round(k * (n - 1) / (keys - 1)) for k in range(keys))) if n > 1 else [0]
    W = max(n * (N * z_all + 2), len(idx) * (N * z_key + N + 8)) + 8
    H = 24 + N * z_all + 20 + N * z_key + 24
    sh = Image.new('RGBA', (W, H), (30, 30, 34, 255))
    d = ImageDraw.Draw(sh)
    d.text((6, 4), f'{stem}_{VERSION}: {n} frames x {MS} ms (all frames x2; key frames x5 with hex + portrait guides, '
                   f'and at the in-game 50 px)', fill=(220, 220, 220))
    for k, fr in enumerate(frames):
        cell = Image.new('RGBA', (N * z_all, N * z_all), BG)
        cell.alpha_composite(fr.resize((N * z_all, N * z_all), Image.NEAREST))
        sh.alpha_composite(cell, (4 + k * (N * z_all + 2), 22))
    y = 22 + N * z_all + 18
    for j, k in enumerate(idx):
        x = 4 + j * (N * z_key + N + 8)
        sh.alpha_composite(magnified(frames[k], z_key), (x, y))
        native = Image.new('RGBA', (N, N), BG)
        native.alpha_composite(frames[k])
        sh.alpha_composite(native, (x + N * z_key + 2, y))
        d.text((x + 2, y + N * z_key + 4), f'frame {k}', fill=(180, 180, 180))
    return sh


def previews(rows, stills):
    sheets = []
    for an, stem, frames in rows:
        sh = sheet_for(stem, frames)
        sh.convert('RGB').save(os.path.join(DOCS, f'an_v1_{stem.replace("anim_fx_", "")}.png'))
        sheets.append(sh)
    # stills: the 50 px tile, x5, and stretched to the 2:1 hex box as the game draws a staticAssetPath
    W = 4 + len(stills) * (N * 5 + N + 36 * 5 + 24)
    st = Image.new('RGBA', (W, 24 + N * 5 + 20), (30, 30, 34, 255))
    d = ImageDraw.Draw(st)
    d.text((6, 4), 'STATIC stills: x5, native 50 px, and squashed to the 36 x 18 hex box (x5) as staticAssetPath draws',
           fill=(220, 220, 220))
    x = 4
    for an, stem, img, _ in stills:
        st.alpha_composite(magnified(img, 5), (x, 22))
        nat = Image.new('RGBA', (N, N), BG); nat.alpha_composite(img)
        st.alpha_composite(nat, (x + N * 5 + 2, 22))
        hexbox = Image.new('RGBA', (36 * 5, 18 * 5), BG)
        hexbox.alpha_composite(img.resize((36, 18), Image.BILINEAR).resize((36 * 5, 18 * 5), Image.NEAREST))
        st.alpha_composite(hexbox, (x + N * 5 + N + 6, 22))
        d.text((x + 2, 22 + N * 5 + 2), stem, fill=(180, 180, 180))
        x += N * 5 + N + 36 * 5 + 24
    st.convert('RGB').save(os.path.join(DOCS, 'an_v1_stills.png'))
    # one overview: every strip, all frames at x2
    W = max(s.width for s in sheets)
    ov_rows = []
    for an, stem, frames in rows:
        r = Image.new('RGBA', (W, N * 2 + 16), (30, 30, 34, 255))
        ImageDraw.Draw(r).text((4, 2), f'{an} {stem}', fill=(220, 220, 220))
        for k, fr in enumerate(frames):
            cell = Image.new('RGBA', (N * 2, N * 2), BG)
            cell.alpha_composite(fr.resize((N * 2, N * 2), Image.NEAREST))
            r.alpha_composite(cell, (4 + k * (N * 2 + 2), 14))
        ov_rows.append(r)
    ov = Image.new('RGBA', (W, sum(r.height for r in ov_rows)), (30, 30, 34, 255))
    y = 0
    for r in ov_rows:
        ov.alpha_composite(r, (0, y)); y += r.height
    ov.convert('RGB').save(os.path.join(DOCS, 'an_v1_contact.png'))


if __name__ == '__main__':
    export()
