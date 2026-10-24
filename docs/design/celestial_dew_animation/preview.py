#!/usr/bin/env python3
"""GIF of Celestial Dew's whole life over the director's avatar: the cast (heal appear), the ward forming (shield
appear) and the loop (shield static) all start on one tick; the loop carries on; then the shield ends (shield
disappear, the loop stops).

    python3 docs/design/celestial_dew_animation/preview.py [VERSION] [OUT.gif]
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
REC = os.path.join(ROOT, 'docs/design/icon_overhaul/ethereal_rebirth/showcase/battle_recording_2026-10-24.mp4')
V = sys.argv[1] if len(sys.argv) > 1 else 'v1'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, f'docs/design/celestial_dew_animation/{V}_over_avatar.gif')
E = os.path.join(ROOT, 'art/jutsu_icons/celestial_dew/animation/exports/anim_celestial_dew_')
BOX, CX, CY, F, SC, MS = (140, 120, 274, 250), 207, 203, 105, 3, 36
with tempfile.TemporaryDirectory() as t:
    p = os.path.join(t, 'c.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.1', '-i', REC, '-frames:v', '1', p], check=True)
    bg = Image.open(p).convert('RGBA').crop(BOX)
bg = bg.resize((bg.width * SC, bg.height * SC), Image.LANCZOS)


def fr(n):
    s = Image.open(f'{E}{n}_{V}.webp').convert('RGBA')
    return [s.crop((0, i * s.width, s.width, (i + 1) * s.width)).resize((F * SC, F * SC), Image.LANCZOS) for i in range(s.height // s.width)]


cast, ward, loop, brk = fr('cast'), fr('ward'), fr('loop'), fr('break')
pos = ((CX - F // 2 - BOX[0]) * SC, (CY - F // 2 - BOX[1]) * SC)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
out = []
plan = [(i, 'cast') for i in range(len(cast))] + [(len(cast) + i, 'shield up') for i in range(50)] + [(i, 'shield ends') for i in range(len(brk))] + [(0, 'shield ends')] * 8
for i, phase in plan:
    c = bg.copy()
    if phase == 'shield ends':
        c.alpha_composite(brk[min(i, len(brk) - 1)], pos)
    else:
        c.alpha_composite(loop[i % len(loop)], pos)
        if i < len(cast):
            c.alpha_composite(cast[i], pos)
            c.alpha_composite(ward[i], pos)
    o = Image.new('RGB', (c.width, c.height + 28), (20, 22, 30))
    o.paste(c.convert('RGB'), (0, 28))
    ImageDraw.Draw(o).text((8, 6), 'Celestial Dew: ' + phase, font=font, fill=(238, 238, 242))
    out.append(o)
out[0].save(OUT, save_all=True, append_images=out[1:], duration=MS, loop=0)
print(OUT, len(out), 'frames', os.path.getsize(OUT), 'bytes')
