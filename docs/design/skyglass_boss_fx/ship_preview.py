#!/usr/bin/env python3
"""Battle-frame previews of the eleven boss strips as they ship (push/470+): the delivered *_v1_x3d.webp files on the
battle still, at the pixi renderer's sizes, each on the hexes its move hits.

    python3 docs/design/skyglass_boss_fx/ship_preview.py

Writes, next to this file: ship_keys_<id>.png (keyframes of each strip on the battle still) and ship_battle.mp4
(the whole sequence at the strips' 50 ms per frame).

Pattern and sizes: docs/design/mother_of_echoes_fx/preview.py (theninjarpg@3314d122 pixi renderer,
libs/rendering/scenes/combatEffects.ts): an ANIMATION clip is ONE square sprite of tile.height * 2.5 centred on its
hex (EFFECT_ANIMATION_HEX_RATIO, libs/rendering/animation.ts), drawn over the actors; appearAnimation plays once,
staticAnimation loops. The still's hex is 132 x 66 px, so a clip is 165 px square. Clips are scaled from the
delivered 150 px frames with bilinear filtering, as the GPU does. Draw order: background, characters, animations.
Hex sets are representative of each move's pattern (push/342 coordinateTargeting), not exact game coordinates.
"""
import json
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SKY = os.path.join(ROOT, 'art/skyglass_boss_fx/exports')
STILL = os.path.join(ROOT, 'docs/design/celestial_dew_animation/battle_still_2026-10-24b.png')
HX, HY, COL, ROW, HW, HH = 311.0, 225.5, 99.0, 66.0, 132, 66
K = round(HH * 2.5)   # 165: tile.height * EFFECT_ANIMATION_HEX_RATIO


def centre(q, r):
    return HX + COL * q, HY + ROW * r - (ROW / 2 if q % 2 else 0)


def clip_frames(sid):
    s = Image.open(os.path.join(SKY, f'anim_{sid}_v1_x3d.webp')).convert('RGBA')
    w = s.width
    return [s.crop((0, i * w, w, i * w + w)).resize((K, K), Image.BILINEAR) for i in range(s.height // w)]


bg = Image.open(STILL).convert('RGBA')
m = Image.new('L', bg.size, 0)
d = ImageDraw.Draw(m)
d.ellipse([278, 158.7, 344, 224.7], fill=255); d.rectangle([277, 144, 344, 162], fill=255); d.ellipse([300, 223.3, 322, 243.3], fill=255)
box = m.getbbox(); TOK = bg.crop(box); TOK.putalpha(m.crop(box)); OFF = (box[0] - HX, box[1] - HY)

BOSS = (-2, 0)
PLAYERS = [(0, 0), (1, -1), (2, -2)]
CHARS = [BOSS] + PLAYERS
ARENA = [(q, r) for q in range(-3, 3) for r in range(-3, 2)]
SAFE = (1, -2)
# (strip, move, loop?, cells, ticks)
PH = [
    ('ships_bell', "Ship's Bell (ring round the Captain)", False,
     [(-2, -1), (-2, 1), (-3, 0), (-3, 1), (-1, 0), (-1, 1), (-2, 0)], None),
    ('broadside_field', 'Broadside (two raking rows, field variant)', False,
     [(q, r) for q in range(-3, 3) for r in (-2, 0)], None),
    ('command_absolute_field', 'Command Absolute (every hex but the safe one, field variant)', False,
     [c for c in ARENA if c != SAFE], None),
    ('crownfall', 'Crownfall (blade line)', False, [(q, 0) for q in range(-1, 3)], None),
    ('maw_field', 'Maw of the Deep (every hex but the safe one, field variant)', False,
     [c for c in ARENA if c != SAFE], None),
    ('exposed', 'Maw / Quench / Lowered Guard window on the boss (loop)', True, [BOSS], 30),
    ('quench', 'Quench (every hex but the safe one, full size)', False, [c for c in ARENA if c != SAFE], None),
    ('recall', 'Recall / Stonebound Summons (summon flourish)', False, [(-1, -1), (-1, 1)], None),
    ('crown_aura', "The Crown's Will on the Crowned Captain (loop)", True, [BOSS], 64),
    ('crimson_strike', 'Final Command (single target)', False, [(0, 0)], None),
    ('chain_wrap', 'Keelbind / Chain Hook (single target)', False, [(1, -1)], None),
    ('chain_wrap', 'Binding: Seal Cross (violet blast on a cross)', False,
     [(0, 0), (-1, 0), (1, -1), (0, -1), (0, 1), (1, 0)], None),
]


def render():
    frames, marks = [], []
    for sid, label, loop, cells, ticks in PH:
        clip = clip_frames(sid)
        n = ticks or len(clip) + 6
        start = len(frames)
        for t in range(n):
            im = bg.copy()
            for c in CHARS:
                x, y = centre(*c)
                im.alpha_composite(TOK, (int(x + OFF[0]), int(y + OFF[1])))
            f = clip[t % len(clip)] if loop else (clip[t] if t < len(clip) else None)
            if f is not None:
                for c in sorted(cells, key=lambda c: centre(*c)[1]):
                    x, y = centre(*c)
                    im.alpha_composite(f, (int(x - K / 2), int(y - K / 2)))
            frames.append(im.convert('RGB'))
        marks.append((sid, label, start, n, len(clip)))
    return frames, marks


def keys(frames, marks):
    out = []
    for i, (sid, label, s, n, nf) in enumerate(marks):
        ticks = sorted({0, nf // 4, nf // 2, (3 * nf) // 4, nf - 1})
        cells = [frames[s + min(t, n - 1)] for t in ticks]
        w, h = cells[0].size
        sheet = Image.new('RGB', (w * len(cells), h + 18), (12, 14, 18))
        dd = ImageDraw.Draw(sheet)
        dd.text((6, 3), f'{sid} - {label}: frames {ticks} of {nf} (50 ms each); clip {K}px = 2.5 x hex height, pixi',
                fill=(220, 225, 232))
        for j, c in enumerate(cells):
            sheet.paste(c, (j * w, 18))
        p = os.path.join(HERE, f'ship_keys_{i:02d}_{sid}.png')
        sheet.save(p)
        out.append(p)
    return out


if __name__ == '__main__':
    frames, marks = render()
    written = keys(frames, marks)
    with tempfile.TemporaryDirectory() as t:
        for i, f in enumerate(frames):
            f.resize((f.width * 2, f.height * 2), Image.NEAREST).save(os.path.join(t, f'{i:04d}.png'))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '20', '-i', os.path.join(t, '%04d.png'),
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart',
                        os.path.join(HERE, 'ship_battle.mp4')], check=True)
    print(json.dumps({'frames': len(frames), 'keys': [os.path.relpath(p, ROOT) for p in written],
                      'mp4': 'docs/design/skyglass_boss_fx/ship_battle.mp4'}, indent=1))
