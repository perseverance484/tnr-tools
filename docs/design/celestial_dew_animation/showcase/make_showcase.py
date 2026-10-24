#!/usr/bin/env python3
"""Staff-facing showcase for Celestial Dew: the icons (old, current and kept), the new animations as a storyboard over
the director's avatar, the text (unchanged; it already describes the animation), and a battle GIF.

    python3 docs/design/celestial_dew_animation/showcase/make_showcase.py

Writes celestial_dew_showcase.png and battle_animation.gif next to this file. Needs ffmpeg (the recording still).
"""
import importlib.util, os, subprocess, tempfile, textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
REC = os.path.join(ROOT, 'docs/design/icon_overhaul/ethereal_rebirth/showcase/battle_recording_2026-10-24.mp4')
A = os.path.join(ROOT, 'art/jutsu_icons/celestial_dew/animation/')
spec = importlib.util.spec_from_file_location('cd', A + 'build_strip.py'); cd = importlib.util.module_from_spec(spec); spec.loader.exec_module(cd)
V = 'v7'
F = lambda s, b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
BG, CARD, FG, DIM, ACC = (18, 22, 34), (30, 36, 52), (238, 240, 246), (160, 168, 186), (140, 190, 255)
BATTLE = ("%user closes their eyes and the night seems to answer, a pale crescent moon blooming into being above them. From "
          "its tip falls a single drop of starlight that splashes across %user and spreads into a dome of soft, silver "
          "light. Wounds knit closed beneath its glow as the dome settles into a quiet ward that swallows the blows meant "
          "for its keeper. Within it, for a few heartbeats, the battle seems very far away.")
ICONS = [('Old', 'the original (live now)', 'art/jutsu_icons/celestial_dew/refs/ref_cd_original_icon.webp', FG),
         ('New', 'our rework, back (scored 10/10)', 'art/jutsu_icons/celestial_dew/refs/ref_cd_live_icon.webp', ACC)]
# storyboard moments: (ms, caption)
BOARD = [(500, 'Moon appears; heal heart'), (1150, 'A drop of starlight falls'), (1500, 'It splashes'),
         (1950, 'Ripples run out'), (2300, 'They charge the rim: the ward'), (3600, 'The ward breathes while it lasts'),
         (6200, 'It fades in and out'), (-300, 'It shatters when it ends')]
# the director's phone recording (2026-10-24b) and where the game draws the 50 px effect square on it (see preview.py)
K, L, T = 184.1, 219.3, 132.1
BOX = (215, 100, 405, 300)


def still():
    return Image.open(os.path.join(ROOT, 'docs/design/celestial_dew_animation/battle_still_2026-10-24b.png')).convert('RGBA')


def strip(n):
    s = Image.open(f'{A}exports/anim_celestial_dew_{n}_{V}.webp').convert('RGBA')
    return [s.crop((0, i * s.width, s.width, (i + 1) * s.width)) for i in range(s.height // s.width)]


HEAL_MS = 60   # the heal's own appear animation (I9aYhT5wMB, kept): its frame time is not on record here (assumed)
_h = Image.open(os.path.join(ROOT, 'art/jutsu_icons/celestial_dew/refs/ref_cd_heal_animation_I9aYhT5wMB.webp')).convert('RGBA')
HEAL = [_h.crop((0, i * _h.width, _h.width, (i + 1) * _h.width)) for i in range(_h.height // _h.width)]


def at(bg, appear, loop, brk, ms, sc):
    c = bg.copy()
    pos = (round(L), round(T))
    FR = round(K)
    if ms >= 0 and ms // HEAL_MS < len(HEAL):
        c.alpha_composite(HEAL[ms // HEAL_MS].resize((FR, FR), Image.LANCZOS), pos)
    if ms >= 0:
        c.alpha_composite(loop[(ms // cd.MS['loop']) % len(loop)].resize((FR, FR), Image.LANCZOS), pos)
        if ms // cd.MS['appear'] < len(appear):
            c.alpha_composite(appear[ms // cd.MS['appear']].resize((FR, FR), Image.LANCZOS), pos)
    else:
        c.alpha_composite(brk[min(len(brk) - 1, -ms // cd.MS['break'])].resize((FR, FR), Image.LANCZOS), pos)
    c = c.crop(BOX)
    return c.resize((c.width * sc, c.height * sc), Image.LANCZOS)


def para(d, x, y, text, width, font, fill, lh):
    for line in textwrap.wrap(text, width):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def main():
    bg = still()
    appear, loop, brk = strip('appear'), strip('loop'), strip('break')
    W, G = 1240, 28
    s = Image.new('RGB', (W, 2400), BG)
    d = ImageDraw.Draw(s)
    d.text((G, 24), 'Celestial Dew: icon and animations', font=F(36, True), fill=FG)
    y = para(d, G, 74, 'Our reworked icon comes back (staff scored it 10/10), the text stays, and new animations play the '
                       'moment the jutsu describes, from the crescent moon to the ward.', 128, F(16), DIM, 22) + 18
    # icons
    iw = 300
    for i, (t, sub, p, col) in enumerate(ICONS):
        x = G + i * (iw + 3 * G)
        im = Image.open(os.path.join(ROOT, p)).convert('RGB')
        d.rounded_rectangle((x - 8, y - 8, x + iw + 8, y + iw + 86), 14, fill=CARD)
        m = Image.new('L', (iw, iw), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, iw - 1, iw - 1), 18, fill=255)
        s.paste(im.resize((iw, iw), Image.LANCZOS), (x, y), m)
        d.text((x, y + iw + 12), t, font=F(22, True), fill=col)
        d.text((x, y + iw + 44), sub, font=F(14), fill=DIM)
    tx = G + 2 * (iw + 3 * G)
    d.text((tx, y), 'The text (unchanged)', font=F(20, True), fill=FG)
    ty = para(d, tx, y + 34, BATTLE.replace('%user', 'the user').replace('the user closes', 'The user closes', 1), 46, F(14), DIM, 20)
    para(d, tx, ty + 14, 'The animation follows it beat for beat: the moon, the single drop, the splash, and the ward.',
         46, F(14), ACC, 20)
    y += iw + 120
    # storyboard
    d.text((G, y), 'The animation in battle (over a real player portrait)', font=F(22, True), fill=FG)
    y += 40
    cw = (W - 2 * G - 3 * 16) // 4
    for k, (ms, cap) in enumerate(BOARD):
        x, yy = G + (k % 4) * (cw + 16), y + (k // 4) * (cw + 70)
        im = at(bg, appear, loop, brk, ms if ms >= 0 else 400, 3).convert('RGB') if ms >= 0 else at(bg, appear, loop, brk, -400, 3).convert('RGB')
        im = im.resize((cw, int(cw * im.height / im.width)), Image.LANCZOS)
        d.rounded_rectangle((x - 6, yy - 6, x + cw + 6, yy + im.height + 52), 12, fill=CARD)
        s.paste(im, (x, yy))
        d.text((x, yy + im.height + 10), f'{k + 1}. {cap}', font=F(15, True), fill=FG)
        d.text((x, yy + im.height + 31), f'{ms / 1000:.1f} s' if ms >= 0 else 'shield ends', font=F(12), fill=DIM)
    y += 2 * (cw + 70) + 10
    y = para(d, G, y, 'How it plays: the cast (moon, drop, ripples) runs 3.4 s; the ward glows up the moment the ripples '
                      'reach the rim, then breathes slowly (once every 6.4 s) for as long as the shield holds. When the '
                      'shield ends, breaks or fails to form, the ward shatters into stardust. The heal keeps its own heart '
                      'effect, which plays alongside as before (step 1 above); before, nothing showed the shield.', 132, F(15), DIM, 21)
    s.crop((0, 0, W, y + 24)).save(os.path.join(HERE, 'celestial_dew_showcase.png'))
    # battle gif (2x, real time, two breaths then the break)
    frames, tick = [], 40
    up = len(loop) * cd.MS['loop'] * 2
    for ms in range(0, up + len(brk) * cd.MS['break'] + 400, tick):
        im = at(bg, appear, loop, brk, ms if ms < up else -(ms - up), 2).convert('RGB')
        frames.append(im)
    frames[0].save(os.path.join(HERE, 'battle_animation.gif'), save_all=True, append_images=frames[1:], duration=tick, loop=0)
    print('ok', os.path.getsize(os.path.join(HERE, 'battle_animation.gif')))


if __name__ == '__main__':
    main()
