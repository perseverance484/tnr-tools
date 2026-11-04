#!/usr/bin/env python3
"""Battle-frame previews of the Mother of Echoes code-built FX, at the pixi renderer's sizes.

    python3 docs/design/mother_of_echoes_fx/preview.py

Writes, next to this file: keys_<asset>.png (keyframes of each code-built export on the battle still) and
moe_fx_battle.mp4 (the whole sequence at the strips' 50 ms per frame).

Pattern: docs/design/skyglass_boss_fx/v3_preview.py, with the sizes of theninjarpg@3314d122's pixi renderer
(libs/rendering/scenes/combatEffects.ts): an ANIMATION clip is ONE square sprite of tile.height * 2.5 centred on the
hex (EFFECT_ANIMATION_HEX_RATIO, libs/rendering/animation.ts), drawn over the actors; a staticAssetPath is stretched
to tile.width x tile.height on the ground layer under the actors. The still's hex is 132 x 66 px (centre (311, 225.5),
column step 0.75 w = 99, row step h = 66, odd columns half a row up), so a clip is 165 px square here (the three.js
preview used 184.1). The fighter token is the still's own, re-laid on each standing hex. Clips are scaled from the
delivered 150 px frames with bilinear filtering, as the GPU does.
Draw order as the game: background, ground tiles, characters, animations.
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
MOE = os.path.join(ROOT, 'art/mother_of_echoes_fx/exports')
SKY = os.path.join(ROOT, 'art/skyglass_boss_fx/exports')
STILL = os.path.join(ROOT, 'docs/design/celestial_dew_animation/battle_still_2026-10-24b.png')
HX, HY, COL, ROW, HW, HH = 311.0, 225.5, 99.0, 66.0, 132, 66
K = round(HH * 2.5)   # 165: tile.height * EFFECT_ANIMATION_HEX_RATIO


def centre(q, r):
    return HX + COL * q, HY + ROW * r - (ROW / 2 if q % 2 else 0)


def clip_frames(path):
    s = Image.open(path).convert('RGBA')
    w = s.width
    return [s.crop((0, i * w, w, i * w + w)).resize((K, K), Image.BILINEAR) for i in range(s.height // w)]


def tile(path):
    return Image.open(path).convert('RGBA').resize((HW, HH), Image.BILINEAR)


M = lambda n: os.path.join(MOE, n)
S = lambda n: os.path.join(SKY, n)
TILES = {'etch': tile(M('tile_moe_etch_v2.webp')), 'heavy': tile(S('tile_heavy_v3.webp')),
         'control': tile(S('tile_control_v3.webp')), 'linger': tile(S('tile_linger_v3.webp')),
         'safe': tile(S('tile_safe_v3.webp'))}
GLINT = {'etch': clip_frames(M('anim_moe_etch_glint_v1.webp')), 'heavy': clip_frames(S('anim_heavy_glint_v3.webp')),
         'control': clip_frames(S('anim_control_glint_v3.webp')), 'linger': clip_frames(S('anim_linger_glint_v3.webp')),
         'safe': clip_frames(S('anim_safe_glint_v3.webp'))}
FILES = {'recast': 'anim_moe_recast_v1.webp', 'guard_open': 'anim_moe_guard_open_v1.webp',
         'quiet': 'anim_moe_quiet_v1.webp', 'lancet': 'anim_moe_lancet_v1.webp', 'feeler': 'anim_moe_feeler_v1.webp',
         'lull': 'anim_moe_lull_v2.webp', 'stillness': 'anim_moe_still_dark_v1.webp',
         'breathless': 'anim_moe_breath_draw_v1.webp', 'lucid': 'anim_moe_lucid_aura_v1.webp',
         'likeness': 'anim_moe_likeness_rise_v1.webp', 'worn': 'anim_moe_worn_rise_v1.webp'}
CLIP = {n: clip_frames(M(f)) for n, f in FILES.items()}

bg = Image.open(STILL).convert('RGBA')
m = Image.new('L', bg.size, 0)
d = ImageDraw.Draw(m)
d.ellipse([278, 158.7, 344, 224.7], fill=255); d.rectangle([277, 144, 344, 162], fill=255); d.ellipse([300, 223.3, 322, 243.3], fill=255)
box = m.getbbox(); TOK = bg.crop(box); TOK.putalpha(m.crop(box)); OFF = (box[0] - HX, box[1] - HY)

# --------------------------------------------------------------------------------------------- the scenario
# Each phase: (name, length in ticks, ground tiles {kind: cells}, loops {clip: cells}, one-shots {clip: cells}, chars)
CHARS = [(0, 0), (2, -1), (-2, 0)]
BAND = [(q, r) for q in range(-3, 4) for r in (-1, 0)]                  # an Etching band, two rows deep
SAFE3 = [(-2, 0), (1, 1), (3, 0)]
SAYO = (0, -2)
OTHERS = {'heavy': [(-3, 1)], 'control': [(-1, 1)], 'linger': [(1, 1)], 'safe': [(3, 1)]}
PH = [
    ('etch_field', 48, {'etch': BAND, **OTHERS}, {'etch': BAND, **OTHERS}, {}, CHARS),
    ('memory_gap', 16, {}, {}, {}, CHARS),
    ('recast', 12, {}, {}, {'recast': BAND}, CHARS),
    ('guard_open', 32, {}, {'guard_open': [c for c in CHARS if c in BAND]}, {}, CHARS),
    ('lancet', 10, {}, {}, {'lancet': [(0, 0)]}, CHARS),
    ('quiet', 12, {}, {}, {'quiet': [(2, -1)]}, CHARS),
    ('feeler', 14, {}, {}, {'feeler': [(1, 0)]}, CHARS),
    ('stillness', 10, {}, {}, {'stillness': [(0, 0)]}, CHARS),
    # Breathless Pull: the hit hexes play it; the three dry tiles (tg_safe, Where the Three Refused) do not
    ('breathless', 12, {'safe': SAFE3}, {'safe': SAFE3}, {'breathless': [(0, 0), (2, -1)]}, CHARS + [(-1, 1)]),
    ('likeness', 14, {}, {}, {'likeness': [(-1, 0)]}, CHARS),
    ('worn', 14, {}, {}, {'worn': [(1, -1), (-3, 0)]}, CHARS),
    # Lucid and the lull ride effects on Sayo herself (an AI portrait, h * 1.6 across)
    ('lucid', 32, {}, {'lucid': [SAYO]}, {}, CHARS, [SAYO]),
    ('lull', 32, {}, {'lull': [SAYO]}, {}, CHARS, [SAYO]),
]


TOK_AI = TOK.resize((round(TOK.width * 1.6), round(TOK.height * 1.6)), Image.BILINEAR)


def render():
    frames, marks = [], {}
    for ph in PH:
        name, length, under, loops, shots, chars = ph[:6]
        ais = ph[6] if len(ph) > 6 else []
        start = len(frames)
        for t in range(length):
            im = bg.copy()
            for kind, cells in under.items():
                for c in cells:
                    x, y = centre(*c)
                    im.alpha_composite(TILES[kind], (int(x - HW / 2), int(y - HH / 2)))
            for c in chars:
                x, y = centre(*c)
                im.alpha_composite(TOK, (int(x + OFF[0]), int(y + OFF[1])))
            for c in ais:   # an AI avatar disc, h * 1.6 across, centred 0.4 h above the hex centre
                x, y = centre(*c)
                im.alpha_composite(TOK_AI, (int(x - TOK_AI.width / 2), int(y - 0.4 * HH - TOK_AI.height / 2 + 4)))
            for kind, cells in loops.items():
                fr = (GLINT.get(kind) or CLIP[kind])
                f = fr[t % len(fr)]
                for c in sorted(cells, key=lambda c: centre(*c)[1]):
                    x, y = centre(*c)
                    im.alpha_composite(f, (int(x - K / 2), int(y - K / 2)))
            for kind, cells in shots.items():
                fr = CLIP[kind]
                if t < len(fr):
                    for c in sorted(cells, key=lambda c: centre(*c)[1]):
                        x, y = centre(*c)
                        im.alpha_composite(fr[t], (int(x - K / 2), int(y - K / 2)))
            frames.append(im.convert('RGB'))
        marks[name] = (start, length)
    return frames, marks


def keys(frames, marks):
    picks = {'etch_field': [0, 4, 8], 'recast': [0, 2, 4, 7], 'guard_open': [0, 6], 'lancet': [2, 4, 6],
             'quiet': [2, 5, 8], 'feeler': [3, 7, 11], 'stillness': [2, 5, 8], 'breathless': [2, 5, 9],
             'likeness': [3, 7, 11], 'worn': [3, 7, 11], 'lucid': [0, 8], 'lull': [0, 12]}
    out = []
    for name, ticks in picks.items():
        s, n = marks[name]
        cells = [frames[s + min(t, n - 1)] for t in ticks]
        w, h = cells[0].size
        sheet = Image.new('RGB', (w * len(cells), h + 18), (12, 14, 18))
        dd = ImageDraw.Draw(sheet)
        dd.text((6, 3), f'{name}: ticks {ticks} of {n} (50 ms each); clip {K}px = 2.5 x hex height, pixi', fill=(220, 225, 232))
        for i, c in enumerate(cells):
            sheet.paste(c, (i * w, 18))
        p = os.path.join(HERE, f'keys_{name}.png')
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
                        os.path.join(HERE, 'moe_fx_battle.mp4')], check=True)
    print(json.dumps({'frames': len(frames), 'keys': [os.path.relpath(p, ROOT) for p in written],
                      'mp4': 'docs/design/mother_of_echoes_fx/moe_fx_battle.mp4'}, indent=1))
