#!/usr/bin/env python3
"""GIF of an Ethereal Rebirth animation strip playing over the director's avatar, from a clean frame of the 2026-10-24
battle recording. Geometry measured from that frame: avatar token centre (207, 180), rim radius 26 px; with the game's
token proportions (centre 0.283 of the frame from the top, radius 0.248) the 50 px effect frame spans 105 recording px,
centred at (207, 203).

    python3 docs/design/ethereal_rebirth_animation/avatar_preview.py [STRIP] [OUT.gif]
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
REC = os.path.join(ROOT, 'docs/design/icon_overhaul/ethereal_rebirth/showcase/battle_recording_2026-10-24.mp4')
STRIP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'art/jutsu_icons/ethereal_rebirth/animation/exports/anim_ethereal_rebirth_v2.webp')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'docs/design/ethereal_rebirth_animation/v2_over_avatar.gif')
BOX = (112, 96, 302, 238)           # clear of the battle tooltip
CX, CY, F = 207, 203, 105
SC, MS = 4, 60
LABEL = sys.argv[3] if len(sys.argv) > 3 else 'Ethereal Rebirth: cast animation over your avatar'

with tempfile.TemporaryDirectory() as t:
    p = os.path.join(t, 'clean.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.1', '-i', REC, '-frames:v', '1', p], check=True)
    bg = Image.open(p).convert('RGBA').crop(BOX)
bw, bh = bg.size
bg = bg.resize((bw * SC, bh * SC), Image.LANCZOS)
strip = Image.open(STRIP).convert('RGBA')
n = strip.height // strip.width
fs = strip.width
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
frames = []
for i in list(range(n)) + [n - 1] * 10:
    fr = strip.crop((0, i * fs, fs, (i + 1) * fs)).resize((F * SC, F * SC), Image.LANCZOS)
    c = bg.copy()
    c.alpha_composite(fr, ((CX - F // 2 - BOX[0]) * SC, (CY - F // 2 - BOX[1]) * SC))
    out = Image.new('RGB', (c.width, c.height + 40), (20, 22, 30))
    out.paste(c.convert('RGB'), (0, 40))
    ImageDraw.Draw(out).text((12, 9), LABEL, font=font, fill=(238, 238, 242))
    frames.append(out)
frames = [frames[0]] * 6 + frames
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=MS, loop=0, optimize=True)
print(OUT, os.path.getsize(OUT))
