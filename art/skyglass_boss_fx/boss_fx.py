#!/usr/bin/env python3
"""Skyglass boss animations from the director's twelve key-art pieces (2026-10-28), style anchored on the Crownbreaker
badge v2. One-shot hits play over everything (director: "Explosions and other temporary effects can do whatever"); the
one looping aura (the frost crown) frames the boss's portrait instead of covering it.

    python3 art/skyglass_boss_fx/boss_fx.py

Writes exports/anim_<id>_v1.webp (vertical strips of 50 px frames, 50 ms each) and
docs/design/skyglass_boss_fx/boss_contact.png. Uses the shared helpers in animate.py (key, reduce with outline
protection, the RGB fill under alpha for linear filtering).
"""
import importlib.util
import math
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('anim', os.path.join(HERE, 'animate.py'))
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
N, EXPORTS = A.N, A.EXPORTS
DOCS = A.DOCS


def art(name, w, colors=20, dist=80, outline=0.55, gain=1.0):
    src = A.keyed(f'raw_fx_{name}.png', dist=dist)
    if gain != 1.0:
        src = A.bright(src, gain)
    h = max(1, int(round(w * src.height / src.width)))
    if h > 48:
        w, h = int(round(w * 48 / h)), 48
    return A.reduce(src, w, h, colors=colors, outline=outline)


def place(f, img, cx, cy, scale=1.0, alpha=None, rot=0.0, bright=1.0):
    im = img
    if scale != 1.0:
        im = im.resize((max(1, int(round(im.width * scale))), max(1, int(round(im.height * scale)))), Image.NEAREST)
    if rot:
        im = im.rotate(rot, resample=Image.NEAREST, expand=True)
    if bright != 1.0:
        im = A.bright(im, bright)
    if alpha is not None:
        im = A.with_alpha(im, alpha)
    A.put(f, im, cx - im.width / 2, cy - im.height / 2)


def reveal(img, frac, direction):
    """Crop the drawn image to the first `frac` of it along a direction: 'up' (from the bottom), 'down', 'diag'."""
    a = np.array(img).copy()
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    if direction == 'up':
        keep = yy >= h * (1 - frac)
    elif direction == 'down':
        keep = yy <= h * frac
    else:  # diag: lower-left to upper-right
        keep = (xx / w + (1 - yy / h)) / 2 <= frac
    a[..., 3] = np.where(keep, a[..., 3], 0)
    return Image.fromarray(a)


def ring(f, cx, cy, r, rgb, alpha=255, squash=0.5, n=36):
    for k in range(n):
        t = 2 * math.pi * k / n
        A.px(f, cx + math.cos(t) * r, cy + math.sin(t) * r * squash, rgb, alpha)


def particles(f, seed, n, cx, cy, t, rgb, spread=2.4, lift=2.6, grav=0.5, alpha=255):
    rng = np.random.RandomState(seed)
    for _ in range(n):
        vx, vy = rng.uniform(-spread, spread), rng.uniform(-lift, -lift * 0.3)
        A.px(f, cx + vx * t, cy + vy * t + grav * t * t, rgb, alpha)


def build():
    out = {}

    # Maw of the Deep (per hex, arena-wide): the maw surges up out of the floor, gapes, then sinks, spraying water.
    maw = art('maw', 46, gain=1.25)
    fr = []
    for i in range(12):
        f = A.frame()
        if i <= 3:
            place(f, reveal(maw, (i + 1) / 4, 'up'), 25, 26 + (3 - i) * 2)
        elif i <= 6:
            place(f, maw, 25, 26, bright=1.15 if i == 4 else 1.0)
        elif i <= 9:
            place(f, reveal(maw, 1 - (i - 6) / 4, 'down'), 25, 26 + (i - 6) * 3, alpha=255 if i < 9 else 130)
        if i >= 5:
            particles(f, 3, 10, 25, 30, i - 4, (150, 220, 210))
        fr.append(f)
    out['maw'] = fr

    # Quench (per hex): crystals crack out, then the steam blooms and rises away.
    q = art('quench', 44)
    fr = []
    for i in range(12):
        f = A.frame()
        s = [0.45, 0.65, 0.85, 1.0, 1.05, 1.05, 1.08, 1.1, 1.12, 1.14, 1.16, 1.18][i]
        place(f, q, 25, 27 - max(0, i - 5) * 1.5, scale=s, alpha=255 if i < 8 else 130, bright=1.25 if i == 3 else 1.0)
        fr.append(f)
    out['quench'] = fr

    # Command Absolute (per hex, the stun): the crowned seal slams down from above, flashes, chains hold, then fade.
    ca = art('command_absolute', 46)
    fr = []
    for i in range(12):
        f = A.frame()
        if i <= 2:
            place(f, ca, 25, 26 - (2 - i) * 4, scale=1.3 - 0.1 * i, alpha=130 if i == 0 else 255)
        elif i == 3:
            place(f, ca, 25, 26, bright=1.5)
            ring(f, 25, 30, 20, (230, 210, 255))
        elif i <= 9:
            place(f, ca, 25, 26, bright=0.95 + 0.1 * math.cos(i))
        else:
            place(f, ca, 25, 26, alpha=130)
        fr.append(f)
    out['command_absolute'] = fr

    # Crownfall (per hex): a crown blade drops point-first and shatters.
    blade = art('crown_blade', 16)
    fr = []
    for i in range(12):
        f = A.frame()
        land = 30 - blade.height / 2
        if i <= 4:
            y = -blade.height / 2 + (land + blade.height / 2) * (i / 4) ** 1.7
            place(f, blade, 25, y)
        elif i == 5:
            place(f, blade, 25, land, bright=1.6)
            ring(f, 25, 30, 7, (255, 255, 255))
        else:
            t = i - 5
            ring(f, 25, 30, 7 + t * 2.4, (160, 225, 255), 255 if t < 3 else 130)
            particles(f, 11, 12, 25, 27, t, (225, 248, 255), alpha=255 if t < 4 else 130)
        fr.append(f)
    out['crownfall'] = fr

    # Broadside (per hex): the cannonball blast pops, holds hot, then breaks into smoke and flying planks.
    bs = art('broadside', 46)
    fr = []
    for i in range(10):
        f = A.frame()
        if i <= 2:
            place(f, bs, 25, 25, scale=0.45 + 0.27 * i, bright=1.3)
        elif i <= 5:
            place(f, bs, 25, 25, bright=1.0 if i > 3 else 1.15)
        else:
            place(f, A.tint(bs, (0.55, 0.5, 0.5)), 25, 25 - (i - 5) * 2, scale=1.0 + 0.05 * (i - 5), alpha=130)
        fr.append(f)
    out['broadside'] = fr

    # Ship's Bell (on the Captain's ring): the bell swings and tolls; gold sound rings burst outward.
    bell = art('ships_bell', 30)
    fr = []
    for i in range(14):
        f = A.frame()
        place(f, bell, 25, 18, rot=[0, -12, 10, -8, 6, -4, 3, -2, 1, 0, 0, 0, 0, 0][i], alpha=255 if i < 12 else 130)
        if 1 <= i <= 11:
            for k, r0 in enumerate((4, 10, 16)):
                r = r0 + (i - 1) * 2.2
                if r < 26:
                    ring(f, 25, 26, r, (255, 230, 120) if k == 0 else (240, 200, 90), 255 if r < 18 else 130)
        fr.append(f)
    out['ships_bell'] = fr

    # Final Command, the crimson strike: the slash wipes across, flashes, and its shards scatter.
    cs = art('crimson_strike', 46)
    fr = []
    for i in range(8):
        f = A.frame()
        if i <= 3:
            place(f, reveal(cs, (i + 1) / 4, 'diag'), 25, 25, bright=1.2 if i == 3 else 1.0)
        elif i <= 5:
            place(f, cs, 25, 25)
        else:
            place(f, cs, 25 + (i - 5) * 2, 25 - (i - 5) * 2, alpha=130)
        fr.append(f)
    out['crimson_strike'] = fr

    # Keelbind / Chain Hook: the chain coils up around the target from the ground, cinches with a violet flash, holds.
    cw = art('chain_wrap', 36, gain=1.2)
    fr = []
    for i in range(10):
        f = A.frame()
        if i <= 3:
            place(f, reveal(cw, (i + 1) / 4, 'up'), 25, 24)
        elif i == 4:
            place(f, cw, 25, 24, bright=1.4)
            ring(f, 25, 30, 12, (220, 190, 255))
        elif i <= 8:
            place(f, cw, 25, 24, scale=0.95 if i % 2 else 1.0)
        else:
            place(f, cw, 25, 24, alpha=130)
        fr.append(f)
    out['chain_wrap'] = fr

    # Recall: the echo rises out of the chakra haze, its eyes flare, and it settles.
    rc = art('recall', 40)
    fr = []
    for i in range(14):
        f = A.frame()
        if i <= 5:
            place(f, reveal(rc, (i + 1) / 6, 'up'), 25, 26 + (5 - i))
        elif i == 6:
            place(f, rc, 25, 26, bright=1.45)
        else:
            place(f, rc, 25, 26, alpha=255 if i < 11 else 130)
        fr.append(f)
    out['recall'] = fr

    # The Crown's Will / Last Directive (LOOP on the boss): a halo of frost points framing the portrait, never over
    # it. The portrait disc is centred (25, 15.8), radius 9.5; the halo sits around it with the face clear.
    halo = art('crown_aura', 46, colors=14)
    m = A.portrait_mask()
    own = np.hypot(*np.mgrid[0:N, 0:N][::-1] - np.array([25, 15.8])[:, None, None]) <= 9.5
    period = 32
    fr = []
    for i in range(period):
        f = A.frame()
        p = A.pulse(i, period)
        place(f, halo, 25, 15.8 + round(0.8 * math.sin(2 * math.pi * i / period)), bright=0.9 + 0.25 * p)
        k = (i * 2) % 40  # a glint sweeping across the points
        A.px(f, 4 + k * 1.05, 10, (255, 255, 255))
        a = np.array(f)
        a[..., 3] = np.where(own, 0, a[..., 3])  # the face stays clear
        fr.append(Image.fromarray(a))
    out['crown_aura'] = fr

    # Splintered Grasp, the rot claw: three slashes rake in one after another, then drip away.
    rcw = art('rot_claw', 44, gain=1.15)
    fr = []
    for i in range(9):
        f = A.frame()
        frac = min(1.0, (i + 1) / 4)
        place(f, reveal(rcw, frac, 'diag'), 25, 25, alpha=255 if i < 7 else 130, bright=1.15 if i == 3 else 1.0)
        if i >= 4:
            particles(f, 5, 8, 25, 25, i - 3, (170, 230, 60), spread=1.4, lift=0.5, grav=0.6)
        fr.append(f)
    out['rot_claw'] = fr

    # Exposed (the punish window, on the boss): the shell cracks open, light pours out, shards break away.
    ex = art('exposed', 40)
    fr = []
    for i in range(10):
        f = A.frame()
        place(f, ex, 25, 24, scale=[0.6, 0.8, 1.0, 1.08, 1.0, 1.0, 1.02, 1.0, 1.02, 1.0][i],
              bright=1.5 if i in (2, 3) else 1.0 + 0.1 * math.sin(i), alpha=255 if i < 9 else 130)
        fr.append(f)
    out['exposed'] = fr
    return out


def export(out):
    rows = []
    for name, frames in out.items():
        strip = A.finish(frames)
        p = os.path.join(EXPORTS, f'anim_{name}_v1.webp')
        strip.save(p, lossless=True, quality=100, method=6)
        size = os.path.getsize(p)
        assert size < A.MAX_BYTES, (name, size)
        print(f'{name}: {len(frames)} frames, {size} bytes')
        row = Image.new('RGBA', (len(frames) * 102, 102), (55, 58, 66, 255))
        for k, fr in enumerate(frames):
            row.alpha_composite(fr.resize((100, 100), Image.NEAREST), (k * 102, 0))
        rows.append(row)
    W = max(r.width for r in rows)
    sheet = Image.new('RGB', (W, len(rows) * 104), (30, 30, 34))
    for j, r in enumerate(rows):
        sheet.paste(r.convert('RGB'), (0, j * 104))
    sheet.save(os.path.join(DOCS, 'boss_contact.png'))


if __name__ == '__main__':
    export(build())
