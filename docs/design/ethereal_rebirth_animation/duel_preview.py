#!/usr/bin/env python3
"""GIF of Ethereal Rebirth on both tiles at once, as one battle round plays it: the caster (cast + loop, absorb effect)
on the left and the target (the hit, damage effect) on the right, all started on the same tick (one drawCombatEffects
pass, theninjarpg libs/threejs/combat.ts:482). The director's portrait stands in for the enemy's (same token geometry).

    python3 docs/design/ethereal_rebirth_animation/duel_preview.py CAST LOOP HIT MS OUT.gif [LOOPS]
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
REC = os.path.join(ROOT, 'docs/design/icon_overhaul/ethereal_rebirth/showcase/battle_recording_2026-10-24.mp4')
cast_p, loop_p, hit_p, ms, out_p = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
loops = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
BOX, CX, CY, F, SC = (140, 120, 274, 250), 207, 203, 105, 2
with tempfile.TemporaryDirectory() as t:
    p = os.path.join(t, 'clean.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.1', '-i', REC, '-frames:v', '1', p], check=True)
    bg = Image.open(p).convert('RGBA').crop(BOX)
bg = bg.resize((bg.width * SC, bg.height * SC), Image.LANCZOS)


def frames_of(path):
    s = Image.open(path).convert('RGBA')
    n = s.height // s.width
    return [s.crop((0, i * s.width, s.width, (i + 1) * s.width)).resize((F * SC, F * SC), Image.LANCZOS) for i in range(n)]


cast, loop, hit = frames_of(cast_p), frames_of(loop_p), frames_of(hit_p)
pos = ((CX - F // 2 - BOX[0]) * SC, (CY - F // 2 - BOX[1]) * SC)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
n = max(len(cast), len(hit)) + int(loops * len(loop))
out = []
for i in range(n):
    me, foe = bg.copy(), bg.copy()
    me.alpha_composite(loop[i % len(loop)], pos)
    if i < len(cast):
        me.alpha_composite(cast[i], pos)
    if i < len(hit):
        foe.alpha_composite(hit[i], pos)
    fr = Image.new('RGB', (me.width * 2 + 12, me.height + 28), (20, 22, 30))
    fr.paste(me.convert('RGB'), (0, 28))
    fr.paste(foe.convert('RGB'), (me.width + 12, 28))
    d = ImageDraw.Draw(fr)
    d.text((8, 6), 'You: cast + absorb loop', font=font, fill=(238, 238, 242))
    d.text((me.width + 20, 6), 'Enemy: the hit', font=font, fill=(238, 238, 242))
    d.text((fr.width - 70, 6), f'{i * ms / 1000:.2f} s', font=font, fill=(160, 165, 180))
    out.append(fr)
out[0].save(out_p, save_all=True, append_images=out[1:], duration=ms, loop=0)
print(out_p, len(out), 'frames', os.path.getsize(out_p), 'bytes')
