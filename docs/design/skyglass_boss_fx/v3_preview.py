#!/usr/bin/env python3
"""Battle-frame preview of the v3 marks: STILL tiles under the characters, glint animations and detonations over them.

    python3 docs/design/skyglass_boss_fx/v3_preview.py   (writes v3_battle_keys.png and v3_battle.mp4)

Draw order as the game (libs/threejs/combat.ts): background, mark tiles (staticAssetPath, stretched to the hex box,
under the users), characters, then animations (glints, the floating safe emblem, detonations) over everything.
Placement as v1/v2: hex 132 x 66 still px, the 50-unit sprite 184.1 px, centre (311, 225.5), columns 99, rows 66.
"""
import os
import subprocess
import tempfile
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
E = os.path.join(ROOT, 'art/skyglass_boss_fx/exports')
OUT = os.path.join(ROOT, 'docs/design/skyglass_boss_fx')
STILL = os.path.join(ROOT, 'docs/design/celestial_dew_animation/battle_still_2026-10-24b.png')
K, HX, HY, COL, ROW, HW, HH = 184.1, 311.0, 225.5, 99.0, 66.0, 132, 66


def centre(q, r):
    return HX + COL * q, HY + ROW * r - (ROW / 2 if q % 2 else 0)


def strip(name):
    s = Image.open(os.path.join(E, name)).convert('RGBA')
    return [s.crop((0, i * 50, 50, i * 50 + 50)).resize((round(K), round(K)), Image.BILINEAR) for i in range(s.height // 50)]


TILE = {n: Image.open(os.path.join(E, f'tile_{n}_v3.webp')).convert('RGBA').resize((HW, HH), Image.BILINEAR)
        for n in ('heavy', 'control', 'linger', 'safe')}
GL = {n: strip(f'anim_{n}_glint_v3.webp') for n in ('heavy', 'control', 'linger', 'safe')}
DT = {n: strip(f'anim_dt_{n}_v2.webp') for n in ('heavy', 'shard')}
bg = Image.open(STILL).convert('RGBA')
m = Image.new('L', bg.size, 0); d = ImageDraw.Draw(m)
d.ellipse([278, 158.7, 344, 224.7], fill=255); d.rectangle([277, 144, 344, 162], fill=255); d.ellipse([300, 223.3, 322, 243.3], fill=255)
box = m.getbbox(); TOK = bg.crop(box); TOK.putalpha(m.crop(box)); OFF = (box[0] - HX, box[1] - HY)
CHARS = [(0, 0), (2, -1), (-2, 0)]
RING = [(0, 0), (0, -1), (0, 1), (-1, 0), (-1, 1), (1, 0), (1, 1)]
LINE = [(2, -2), (2, -1), (2, 0)]
POOL = [(-2, 0), (-3, 0), (-2, -1)]
SAFE = [(1, -1), (-2, 1), (2, 1)]
ALL = [(q, r) for q in range(-3, 4) for r in range(-4, 3)]
FIELD = [c for c in ALL if c not in SAFE]
FAN = [(-1, -1), (-2, -1), (-3, -2), (-1, 1), (-2, 2)]
# phases: (start, end, under-tiles {name: cells}, glints {name: cells}, detonation (name, cells) or None)
P = [(0, 48, {'heavy': RING, 'control': LINE, 'linger': POOL, 'safe': [(-1, 2)]}, {'heavy': RING, 'control': LINE, 'linger': POOL, 'safe': [(-1, 2)]}, None),
     (48, 60, {'control': LINE, 'linger': POOL}, {'control': LINE, 'linger': POOL}, ('heavy', RING)),
     (64, 112, {'heavy': FIELD, 'safe': SAFE}, {'heavy': FIELD, 'safe': SAFE}, None),
     (112, 124, {}, {}, ('heavy', FIELD)),
     (126, 140, {}, {}, ('shard', FAN))]
frames = []
for tick in range(140):
    im = bg.copy()
    # paint the original token out by re-laying background under it is not possible; characters are redrawn on top
    ph = next((p for p in P if p[0] <= tick < p[1]), None)
    if ph:
        s, e, under, glint, det = ph
        for n, cells in under.items():
            for c in cells:
                x, y = centre(*c); im.alpha_composite(TILE[n], (int(x - HW / 2), int(y - HH / 2)))
    for c in CHARS:
        x, y = centre(*c); im.alpha_composite(TOK, (int(x + OFF[0]), int(y + OFF[1])))
    if ph:
        for n, cells in glint.items():
            fr = GL[n][(tick - s) % len(GL[n])]
            for c in cells:
                x, y = centre(*c); im.alpha_composite(fr, (int(x - K / 2), int(y - K / 2)))
        if det:
            n, cells = det
            fr = DT[n][min(tick - s, len(DT[n]) - 1)]
            for c in sorted(cells, key=lambda c: centre(*c)[1]):
                x, y = centre(*c); im.alpha_composite(fr, (int(x - K / 2), int(y - K / 2)))
    frames.append(im.convert('RGB'))
keys = [0, 8, 50, 52, 70, 80, 116, 130, 133]
sheet = Image.new('RGB', (bg.width * 3, bg.height * 3))
for i, k in enumerate(keys):
    sheet.paste(frames[k], ((i % 3) * bg.width, (i // 3) * bg.height))
sheet.save(os.path.join(OUT, 'v3_battle_keys.png'))
with tempfile.TemporaryDirectory() as t:
    for i, f in enumerate(frames):
        f.resize((f.width * 2, f.height * 2), Image.NEAREST).save(os.path.join(t, f'{i:04d}.png'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '20', '-i', os.path.join(t, '%04d.png'), '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', os.path.join(OUT, 'v3_battle.mp4')], check=True)
print('ok')
