#!/usr/bin/env python3
"""Draw a player's battle portrait exactly as the game builds it (libs/threejs/combat.ts createUserSprite), from the
game's own images (art/battle_refs/), inside the effect square drawn at 2.5 tile heights (the upstream change). Used to
check that an animation lines up with the portrait on any screen: with effects at 2.5 h the layout is the same at every h.

    python3 docs/design/celestial_dew_animation/portrait_mock.py OUT.png [SIZE] [STRIP FRAME ...]
"""
import os, sys
from PIL import Image, ImageOps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
R = os.path.join(ROOT, 'art/battle_refs/')
EFFECT_H = 2.5


def portrait(size, avatar=None, village=(20, 20, 20)):
    """The effect square (size px) with the portrait drawn in it. Tile height h = size / 2.5; sprite y is up from the
    tile origin, the square's centre is at h/2."""
    h = size / EFFECT_H
    sq = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    def place(img, sw, sh, sy):   # sprite size (in h) centred at (w/2, sy h)
        im = img.resize((max(1, round(sw * h)), max(1, round(sh * h))), Image.LANCZOS)
        cy = size / 2 - (sy - 0.5) * h
        sq.alpha_composite(im, (round(size / 2 - im.width / 2), round(cy - im.height / 2)))
    marker = Image.open(R + 'game_user_marker_IMG_SECTOR_USER_MARKER.png').convert('L')
    def tinted(col):
        im = Image.new('RGBA', marker.size, col + (255,)); im.putalpha(marker); return im
    place(tinted(village), 1.0, 1.2, 0.9)          # village-colour outline
    place(tinted((255, 255, 255)), 0.9, 1.1, 0.9)  # white marker
    mask = Image.open(R + 'game_user_sprite_mask_IMG_SECTOR_USER_SPRITE_MASK.png').convert('L')
    av = (avatar or Image.new('RGB', (512, 512), (150, 30, 40))).convert('RGBA').resize(mask.size, Image.LANCZOS)
    av.putalpha(mask)
    place(av, 0.8, 0.8, 1.0)                       # avatar
    star = Image.open(R + 'game_battlefield_star_IMG_BATTLEFIELD_STAR.png').convert('RGBA')
    place(star, 0.4, 0.4, 0.4)                     # star (h / 2.5)
    return sq


if __name__ == '__main__':
    out, size = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 448
    base = Image.new('RGBA', (size, size), (225, 225, 228, 255))
    base.alpha_composite(portrait(size))
    args = sys.argv[3:]
    cells = []
    for i in range(0, len(args), 2):
        s = Image.open(args[i]).convert('RGBA'); f = int(args[i + 1])
        c = base.copy(); c.alpha_composite(s.crop((0, f * s.width, s.width, (f + 1) * s.width)).resize((size, size), Image.LANCZOS))
        cells.append(c)
    cells = cells or [base]
    sheet = Image.new('RGB', (size * len(cells), size), (20, 22, 30))
    for k, c in enumerate(cells): sheet.paste(c.convert('RGB'), (k * size, 0))
    sheet.save(out)
