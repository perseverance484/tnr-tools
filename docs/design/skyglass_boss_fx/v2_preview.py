#!/usr/bin/env python3
"""Battle-frame GIF of the v2 danger language (art/skyglass_boss_fx/animate.py) on the director's phone still.

    python3 docs/design/skyglass_boss_fx/v2_preview.py

Placement as v1 (measured): the 50-unit effect square is 184.1 still px, hex centre of the recorded character at
(311, 225.5), columns every 99 px, rows every 66 px, odd columns half a row up. Frames are magnified with bilinear
filtering, as three.js does. Effects draw over the characters.
"""
import os
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
E = os.path.join(ROOT, 'art/skyglass_boss_fx/exports')
OUT = os.path.join(ROOT, 'docs/design/skyglass_boss_fx')
STILL = os.path.join(ROOT, 'docs/design/celestial_dew_animation/battle_still_2026-10-24b.png')
K, HX, HY, COL, ROW, TICK = 184.1, 311.0, 225.5, 99.0, 66.0, 50


def centre(q, r):
    return HX + COL * q, HY + ROW * r - (ROW / 2 if q % 2 else 0)


def frames(aid):
    s = Image.open(os.path.join(E, f'anim_{aid}_v2.webp')).convert('RGBA')
    return [s.crop((0, i * 50, 50, i * 50 + 50)).resize((round(K), round(K)), Image.BILINEAR) for i in range(s.height // 50)]


F = {a: frames(a) for a in ('tg_heavy', 'tg_control', 'tg_linger', 'tg_safe', 'dt_heavy', 'dt_shard')}
RING = [(0, 0), (0, -1), (0, 1), (-1, 0), (-1, 1), (1, 0), (1, 1)]
LINE = [(2, -2), (2, -1), (2, 0)]
POOL = [(-2, -1), (-3, 0), (-2, 0)]
SAFE = [(1, -1), (-2, 1), (2, 1)]
ALL = [(q, r) for q in range(-3, 4) for r in range(-4, 3)]
FAN = [(-1, -1), (-2, -1), (-3, -2), (-1, 1), (-2, 2)]

# timeline in ticks: (start, end, anim, cells, loop)
T = [(0, 48, 'tg_heavy', RING, True), (0, 140, 'tg_control', LINE, True), (0, 140, 'tg_linger', POOL, True),
     (0, 48, 'tg_safe', [(-1, 2)], True), (48, 60, 'dt_heavy', RING, False),
     (64, 112, 'tg_heavy', [c for c in ALL if c not in SAFE and c not in LINE and c not in POOL], True),
     (64, 112, 'tg_safe', SAFE, True), (112, 124, 'dt_heavy', [c for c in ALL if c not in SAFE and c not in LINE and c not in POOL], False),
     (126, 140, 'dt_shard', FAN, False)]
bg = Image.open(STILL).convert('RGBA')
out = []
for tick in range(140):
    im = bg.copy()
    for s, e, aid, cells, loop in T:
        if s <= tick < e:
            fr = F[aid]
            k = (tick - s) % len(fr) if loop else min(tick - s, len(fr) - 1)
            for c in sorted(cells, key=lambda c: centre(*c)[1]):
                x, y = centre(*c)
                im.alpha_composite(fr[k], (int(x - K / 2), int(y - K / 2)))
    out.append(im.convert('RGB'))
for scale, name in ((1, 'v2_battle_1x.gif'), (2, 'v2_battle_2x.gif')):
    fs = [f.resize((f.width * scale, f.height * scale), Image.NEAREST) for f in out]
    fs[0].save(os.path.join(OUT, name), save_all=True, append_images=fs[1:], duration=TICK, loop=0, optimize=True)
keys = [0, 8, 50, 52, 56, 70, 116, 130, 133]
sheet = Image.new('RGB', (out[0].width * 3, out[0].height * 3))
for i, k in enumerate(keys):
    sheet.paste(out[k], ((i % 3) * out[0].width, (i // 3) * out[0].height))
sheet.save(os.path.join(OUT, 'v2_battle_keys.png'))
print('ok')
