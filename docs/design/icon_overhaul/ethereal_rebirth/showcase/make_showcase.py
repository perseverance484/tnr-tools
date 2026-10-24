#!/usr/bin/env python3
"""Staff-facing showcase for the Ethereal Rebirth rework: icons (old, reverted, new), text before/after, and the cast
animation in a live battle (frames from battle_recording_2026-10-24.mp4, cropped around the caster).

    python3 docs/design/icon_overhaul/ethereal_rebirth/showcase/make_showcase.py

Needs ffmpeg for the recording frames. Writes ethereal_rebirth_showcase.png and battle_animation.gif next to this file.
"""
import glob, os, subprocess, tempfile, textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
REC = os.path.join(HERE, 'battle_recording_2026-10-24.mp4')
CROP = 'crop=190:140:112:96'      # around the caster's tile, clear of the battle tooltip
F = lambda s, b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
BG, CARD, FG, DIM, GRN = (20, 22, 30), (32, 35, 46), (238, 238, 242), (165, 168, 178), (110, 200, 130)
OLD_D = "A forbidden art that breaks the seal upon the user's soul and burns them anew in green flame, turning every wound into new life at the cost of their strength."
OLD_B = "%user cracks open the seal upon their own soul, and the elements burn through them in a roar of green flame that erupts outward to strike %target. In the fire's wake %user's body begins to unmake and remake itself, turning every wound they suffer into new life. The rebirth is not gentle; it pulls the strength from %user's arms to feed the blaze, and for a time their blows fall soft as ash. What rises from those flames is harder to kill than what entered them."
NEW_D = "A forbidden art that breaks the seal upon the user's soul, loosing its raw light to strike the enemy. The user is remade from within, wounds turning to new life as the strength drains from their blows."
NEW_B = "%user throws their arms wide and the seal upon their soul cracks open, a golden core blazing to life at their chest. Ribbons of pale soul-light pour out of them and spin around their body before one lashes out to strike %target. Within that whirling light %user's body unmakes and remakes itself, turning every wound into new life, though the rebirth drinks the strength from their arms until their blows fall soft as ash. What rises from the light is harder to kill than what entered it."
ICONS = [('Old', 'the original icon', 'art/jutsu_icons/ethereal_rebirth/refs/ref_er_original.webp'),
         ('Reverted', 'our first rework', 'docs/design/icon_overhaul/src/10_ethereal_rebirth_ours'),
         ('New', 'premium upgrade of the original', 'art/jutsu_icons/ethereal_rebirth/exports/icon_jutsu_ethereal_rebirth_v1.webp')]


def frames(tmp):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '0.9', '-t', '2.9', '-i', REC, '-vf', CROP + ',fps=20',
                    os.path.join(tmp, 'c_%03d.png')], check=True)
    return [Image.open(f).convert('RGB') for f in sorted(glob.glob(os.path.join(tmp, 'c_*.png')))]


def para(d, x, y, text, width, font, fill, lh):
    for line in textwrap.wrap(text, width):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def main():
    with tempfile.TemporaryDirectory() as tmp:
        fr = frames(tmp)
    W, G = 1240, 28
    s = Image.new('RGB', (W, 3000), BG)
    d = ImageDraw.Draw(s)
    d.text((G, 24), 'Ethereal Rebirth: premium rework', font=F(36, True), fill=FG)
    y = para(d, G, 72, 'New icon, new text and a new cast animation, made to tell one story: the seal on the soul breaks and '
                       'ribbons of soul-light pour out.', 130, F(16), DIM, 22) + 18
    iw = (W - 4 * G) // 3
    for i, (t, sub, p) in enumerate(ICONS):
        x = G + i * (iw + G)
        im = Image.open(os.path.join(ROOT, p)).convert('RGB')
        d.rounded_rectangle((x - 8, y - 8, x + iw + 8, y + iw + 112), 14, fill=CARD)
        m = Image.new('L', (iw, iw), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, iw - 1, iw - 1), 18, fill=255)
        s.paste(im.resize((iw, iw), Image.LANCZOS), (x, y), m)
        d.text((x, y + iw + 12), t, font=F(24, True), fill=GRN if t == 'New' else FG)
        d.text((x, y + iw + 44), sub, font=F(15), fill=DIM)
        s.paste(im.resize((45, 45), Image.LANCZOS).resize((90, 90), Image.NEAREST), (x + iw - 90, y + iw + 10))
        d.text((x, y + iw + 76), 'right: at phone size (shown 2x)', font=F(12), fill=DIM)
    y += iw + 150
    d.text((G, y), 'Text', font=F(26, True), fill=FG)
    y += 44
    cw = (W - 3 * G) // 2
    tops = []
    for k, (lab, col, de, ba) in enumerate((('Before (live now)', FG, OLD_D, OLD_B), ('After', GRN, NEW_D, NEW_B))):
        x = G + k * (cw + G)
        yy = y + 34
        yy = para(d, x, yy + 22, de, 74, F(15), FG, 21)
        yy = para(d, x, yy + 34, ba, 74, F(15), FG, 21)
        tops.append(yy)
    th = max(tops) - y + 16
    d.rectangle((0, y - 10, W, y + th + 10), fill=BG)
    for k, (lab, col, de, ba) in enumerate((('Before (live now)', FG, OLD_D, OLD_B), ('After', GRN, NEW_D, NEW_B))):
        x = G + k * (cw + G)
        d.rounded_rectangle((x - 8, y - 8, x + cw + 8, y + th), 14, fill=CARD)
        d.text((x, y), lab, font=F(19, True), fill=col)
        d.text((x, y + 34), 'Description', font=F(14, True), fill=DIM)
        yy = para(d, x, y + 56, de, 74, F(15), FG, 21)
        d.text((x, yy + 12), 'Battle line', font=F(14, True), fill=DIM)
        para(d, x, yy + 34, ba, 74, F(15), FG, 21)
    y = para(d, G, y + th + 12, 'Why the text changed: the jutsu deals non-elemental damage, so the green flame and the elements '
                                'were removed. The new lines describe exactly what the icon and the animation show.', 140, F(14), DIM, 20) + 30
    d.text((G, y), 'Cast animation, in battle', font=F(26, True), fill=FG)
    y = para(d, G, y + 38, 'Before: no animation on the caster (only the hit on the enemy). After: the seal bursts at the chest, '
                           'gold and blue ribbons wrap the avatar, one lashes out, then they fade into flecks.', 140, F(14), DIM, 20) + 14
    pick = [6, 12, 18, 24, 30, 34, 38, 42, 46, 52]
    fw = (W - 2 * G - 4 * 12) // 5
    fh = int(fw * 140 / 190)
    for i, k in enumerate(pick):
        s.paste(fr[min(k, len(fr) - 1)].resize((fw, fh), Image.LANCZOS), (G + (i % 5) * (fw + 12), y + (i // 5) * (fh + 12)))
    y += 2 * (fh + 12) + 6
    d.text((G, y), 'Frames from a live battle recording, 2026-10-24. Animated version: battle_animation.gif', font=F(13), fill=DIM)
    s.crop((0, 0, W, y + 36)).save(os.path.join(HERE, 'ethereal_rebirth_showcase.png'), optimize=True)
    gif = []
    for f in fr:
        c = Image.new('RGB', (570, 456), BG)
        c.paste(f.resize((570, 420), Image.NEAREST), (0, 36))
        ImageDraw.Draw(c).text((12, 9), 'Ethereal Rebirth: new cast animation, in battle', font=F(18, True), fill=FG)
        gif.append(c)
    gif += [gif[-1]] * 8
    gif[0].save(os.path.join(HERE, 'battle_animation.gif'), save_all=True, append_images=gif[1:], duration=50, loop=0, optimize=True)
    print('written')


if __name__ == '__main__':
    main()
