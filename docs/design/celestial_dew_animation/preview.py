#!/usr/bin/env python3
"""GIF of Celestial Dew's whole life over the director's avatar, composited on real time: the appear (shield appear)
and the loop (shield static) start on one tick; the loop carries on; then the shield ends (shield disappear; the loop
stops). Frame times come from the build script's MS.

    python3 docs/design/celestial_dew_animation/preview.py [VERSION] [OUT.gif]
"""
import importlib.util, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
REC = os.path.join(ROOT, 'docs/design/icon_overhaul/ethereal_rebirth/showcase/battle_recording_2026-10-24.mp4')
V = sys.argv[1] if len(sys.argv) > 1 else 'v3'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, f'docs/design/celestial_dew_animation/{V}_over_avatar.gif')
A = os.path.join(ROOT, 'art/jutsu_icons/celestial_dew/animation/')
spec = importlib.util.spec_from_file_location('cd', A + 'build_strip.py'); cd = importlib.util.module_from_spec(spec); spec.loader.exec_module(cd)
BOX, CX, CY, F, SC, TICK = (140, 120, 274, 250), 207, 203, 105, 3, 40
with tempfile.TemporaryDirectory() as t:
    p = os.path.join(t, 'c.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.1', '-i', REC, '-frames:v', '1', p], check=True)
    bg = Image.open(p).convert('RGBA').crop(BOX)
bg = bg.resize((bg.width * SC, bg.height * SC), Image.LANCZOS)


def fr(n):
    s = Image.open(f'{A}exports/anim_celestial_dew_{n}_{V}.webp').convert('RGBA')
    return [s.crop((0, i * s.width, s.width, (i + 1) * s.width)).resize((F * SC, F * SC), Image.LANCZOS) for i in range(s.height // s.width)]


appear, loop, brk = fr('appear'), fr('loop'), fr('break')
ma, ml, mb = cd.MS['appear'], cd.MS['loop'], cd.MS['break']
pos = ((CX - F // 2 - BOX[0]) * SC, (CY - F // 2 - BOX[1]) * SC)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
up_ms = len(loop) * ml * 2                      # two breaths of the shield, then it ends
out = []
for ms in range(0, up_ms + len(brk) * mb + 400, TICK):
    c = bg.copy()
    if ms < up_ms:
        c.alpha_composite(loop[(ms // ml) % len(loop)], pos)
        if ms // ma < len(appear):
            c.alpha_composite(appear[ms // ma], pos)
        label = 'cast' if ms // ma < len(appear) else 'shield up'
    else:
        c.alpha_composite(brk[min(len(brk) - 1, (ms - up_ms) // mb)], pos)
        label = 'shield ends'
    o = Image.new('RGB', (c.width, c.height + 28), (20, 22, 30))
    o.paste(c.convert('RGB'), (0, 28))
    d = ImageDraw.Draw(o)
    d.text((8, 6), 'Celestial Dew: ' + label, font=font, fill=(238, 238, 242))
    d.text((o.width - 64, 6), f'{ms / 1000:.2f} s', font=font, fill=(160, 165, 180))
    out.append(o)
out[0].save(OUT, save_all=True, append_images=out[1:], duration=TICK, loop=0)
print(OUT, len(out), 'frames', os.path.getsize(OUT), 'bytes')
