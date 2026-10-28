#!/usr/bin/env python3
"""Battle-frame reel of the boss animations (art/skyglass_boss_fx/boss_fx.py): writes boss_reel.mp4 and boss_keys.png.
Placement and draw order as v3_preview.py; one-shots play over everything, the crown aura loops on the 'boss'."""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
E = os.path.join(ROOT, 'art/skyglass_boss_fx/exports')
OUT = os.path.join(ROOT, 'docs/design/skyglass_boss_fx')
STILL = os.path.join(ROOT, 'docs/design/celestial_dew_animation/battle_still_2026-10-24b.png')
K, HX, HY, COL, ROW = 184.1, 311.0, 225.5, 99.0, 66.0


def centre(q, r):
    return HX + COL * q, HY + ROW * r - (ROW / 2 if q % 2 else 0)


def strip(name):
    s = Image.open(os.path.join(E, f'anim_{name}_v1.webp')).convert('RGBA')
    return [s.crop((0, i * 50, 50, i * 50 + 50)).resize((round(K), round(K)), Image.BILINEAR) for i in range(s.height // 50)]


bg = Image.open(STILL).convert('RGBA')
m = Image.new('L', bg.size, 0); d = ImageDraw.Draw(m)
d.ellipse([278, 158.7, 344, 224.7], fill=255); d.rectangle([277, 144, 344, 162], fill=255); d.ellipse([300, 223.3, 322, 243.3], fill=255)
box = m.getbbox(); TOK = bg.crop(box); TOK.putalpha(m.crop(box)); OFF = (box[0] - HX, box[1] - HY)
CHARS = [(0, 0), (2, -1), (-2, 0)]
BOSS = (2, -1)
RING = [(0, 0), (0, -1), (0, 1), (-1, 0), (-1, 1), (1, 0), (1, 1)]
ALL = [(q, r) for q in range(-3, 4) for r in range(-4, 3)]
ROWS = [(q, 0) for q in range(-3, 4)] + [(q, 1) for q in range(-3, 4)]
FAN = [(-1, -1), (-2, -1), (-3, -2), (-1, 1), (-2, 2)]
SEQ = [('crimson_strike', [(0, 0)], 'Final Command'), ('chain_wrap', [(-2, 0)], 'Keelbind'), ('rot_claw', [(0, 0)], 'Splintered Grasp'),
       ('ships_bell', [BOSS], "Ship's Bell"), ('broadside', ROWS, 'Broadside'), ('maw', [c for c in ALL if c not in ((1, -1), (-2, 1), (2, 1))], 'Maw of the Deep'),
       ('exposed', [BOSS], 'Exposed Seam'), ('quench', RING, 'Quench'), ('recall', [(1, -2)], 'Recall'),
       ('command_absolute', [c for c in ALL if c not in ((1, -1), (-2, 1), (2, 1))], 'Command Absolute'), ('crownfall', FAN, 'Crownfall')]
F = {n: strip(n) for n, _, _ in SEQ}
AURA = strip('crown_aura')
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
frames, keys = [], []
tick = 0
for name, cells, label in SEQ:
    n = len(F[name])
    for k in range(n + 6):
        im = bg.copy()
        for c in CHARS:
            x, y = centre(*c); im.alpha_composite(TOK, (int(x + OFF[0]), int(y + OFF[1])))
        x, y = centre(*BOSS); im.alpha_composite(AURA[tick % len(AURA)], (int(x - K / 2), int(y - K / 2)))
        if k < n:
            for c in sorted(cells, key=lambda c: centre(*c)[1]):
                x, y = centre(*c); im.alpha_composite(F[name][k], (int(x - K / 2), int(y - K / 2)))
        ImageDraw.Draw(im).text((10, 8), label, fill=(20, 20, 20), font=font)
        frames.append(im.convert('RGB'))
        if k == n // 2:
            keys.append(frames[-1])
        tick += 1
sheet = Image.new('RGB', (bg.width * 4, bg.height * 3), (0, 0, 0))
for i, f in enumerate(keys[:12]):
    sheet.paste(f, ((i % 4) * bg.width, (i // 4) * bg.height))
sheet.save(os.path.join(OUT, 'boss_keys.png'))
with tempfile.TemporaryDirectory() as t:
    for i, f in enumerate(frames):
        f.resize((f.width * 2, f.height * 2), Image.NEAREST).save(os.path.join(t, f'{i:04d}.png'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '20', '-i', os.path.join(t, '%04d.png'), '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', os.path.join(OUT, 'boss_reel.mp4')], check=True)
print(len(frames), 'frames')
