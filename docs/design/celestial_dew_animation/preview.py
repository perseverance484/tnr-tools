#!/usr/bin/env python3
"""GIF of Celestial Dew's whole life over the director's avatar, composited on real time: the appear (shield appear)
and the loop (shield static) start on one tick; the loop carries on; then the shield ends (shield disappear; the loop
stops). Frame times come from the build script's MS.

    python3 docs/design/celestial_dew_animation/preview.py [VERSION] [OUT.gif]
"""
import importlib.util, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# The director's phone recording of 2026-10-24 (battle_recording_2026-10-24b.mp4) and where the game draws the 50 px
# effect square on it: measured from the v5 ward ring shown in that recording (184.1 recording px across, top-left at
# (219.3, 132.1)); consistent with the pinned source's portrait geometry for h = 16.1 (build_strip.py H_REF).
STILL = os.path.join(ROOT, 'docs/design/celestial_dew_animation/battle_still_2026-10-24b.png')
V = sys.argv[1] if len(sys.argv) > 1 else 'v6'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, f'docs/design/celestial_dew_animation/{V}_over_avatar.gif')
A = os.path.join(ROOT, 'art/jutsu_icons/celestial_dew/animation/')
spec = importlib.util.spec_from_file_location('cd', A + 'build_strip.py'); cd = importlib.util.module_from_spec(spec); spec.loader.exec_module(cd)
K, L, T = 184.1, 219.3, 132.1
BOX, SC, TICK = (215, 100, 405, 300), 2, 40
bg = Image.open(STILL).convert('RGBA').crop(BOX)
bg = bg.resize((bg.width * SC, bg.height * SC), Image.LANCZOS)


def fr(n):
    s = Image.open(f'{A}exports/anim_celestial_dew_{n}_{V}.webp').convert('RGBA')
    return [s.crop((0, i * s.width, s.width, (i + 1) * s.width)).resize((round(K * SC), round(K * SC)), Image.LANCZOS) for i in range(s.height // s.width)]


appear, loop, brk = fr('appear'), fr('loop'), fr('break')
# the heal effect's own appear animation (I9aYhT5wMB, kept; supplied by the director; 20 frames of 128 px). Its frame time
# is not on record here: HEAL_MS is an assumption.
HEAL_MS = 60
_h = Image.open(os.path.join(ROOT, 'art/jutsu_icons/celestial_dew/refs/ref_cd_heal_animation_I9aYhT5wMB.webp')).convert('RGBA')
heal = [_h.crop((0, i * _h.width, _h.width, (i + 1) * _h.width)).resize((round(K * SC), round(K * SC)), Image.LANCZOS) for i in range(_h.height // _h.width)]
ma, ml, mb = cd.MS['appear'], cd.MS['loop'], cd.MS['break']
pos = (round((L - BOX[0]) * SC), round((T - BOX[1]) * SC))
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
up_ms = len(loop) * ml * 2                      # two breaths of the shield, then it ends
out = []
for ms in range(0, up_ms + len(brk) * mb + 400, TICK):
    c = bg.copy()
    if ms < up_ms:
        if ms // HEAL_MS < len(heal):
            c.alpha_composite(heal[ms // HEAL_MS], pos)
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
