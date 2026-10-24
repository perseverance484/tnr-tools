#!/usr/bin/env python3
"""GIF of Ethereal Rebirth as the battle shows it: the cast animation (absorb appearAnimation, plays once) and the
passive loop (absorb staticAnimation, loops while the absorb is active) start together over the director's avatar
(libs/threejs/combat.ts adds both when the effect appears); after the cast, the loop carries on.

    python3 docs/design/ethereal_rebirth_animation/battle_preview.py CAST CAST_MS LOOP LOOP_MS OUT.gif [LOOPS]
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
REC = os.path.join(ROOT, 'docs/design/icon_overhaul/ethereal_rebirth/showcase/battle_recording_2026-10-24.mp4')
cast_p, cast_ms, loop_p, loop_ms, out_p = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5]
loops = float(sys.argv[6]) if len(sys.argv) > 6 else 2.5
BOX, CX, CY, F, SC, TICK = (112, 96, 302, 238), 207, 203, 105, 2, 40

with tempfile.TemporaryDirectory() as t:
    p = os.path.join(t, 'clean.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.1', '-i', REC, '-frames:v', '1', p], check=True)
    bg = Image.open(p).convert('RGBA').crop(BOX)
bg = bg.resize((bg.width * SC, bg.height * SC), Image.LANCZOS)


def frames_of(path):
    s = Image.open(path).convert('RGBA')
    n = s.height // s.width
    return [s.crop((0, i * s.width, s.width, (i + 1) * s.width)).resize((F * SC, F * SC), Image.LANCZOS) for i in range(n)]


cast = frames_of(cast_p) if cast_p != '-' else []
loop = frames_of(loop_p)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
pos = ((CX - F // 2 - BOX[0]) * SC, (CY - F // 2 - BOX[1]) * SC)
total = len(cast) * cast_ms + int(loops * len(loop) * loop_ms)
out = []
for ms in range(0, total, TICK):
    c = bg.copy()
    c.alpha_composite(loop[(ms // loop_ms) % len(loop)], pos)
    ci = ms // cast_ms
    if ci < len(cast):
        c.alpha_composite(cast[ci], pos)
    label = 'cast + absorb active' if ci < len(cast) else 'absorb active (loops)'
    fr = Image.new('RGB', (c.width, c.height + 30), (20, 22, 30))
    fr.paste(c.convert('RGB'), (0, 30))
    ImageDraw.Draw(fr).text((10, 6), 'Ethereal Rebirth: ' + label, font=font, fill=(238, 238, 242))
    out.append(fr)
out[0].save(out_p, save_all=True, append_images=out[1:], duration=TICK, loop=0)
print(out_p, len(out), 'frames', os.path.getsize(out_p), 'bytes')
