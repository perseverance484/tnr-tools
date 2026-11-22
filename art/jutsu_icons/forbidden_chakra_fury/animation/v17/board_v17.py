#!/usr/bin/env python3
"""Board preview for FCF v17 with the proposed `animationBeam` (2026-11-21): writes preview_fcf_v17_board.gif."""
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "v10"))
import board_v10 as BV  # noqa: E402
import build_v17 as B  # noqa: E402


def render(cs, cols=12, rows=8, caster=(5, 4), radius=4, enemies=((8, 3), (2, 5), (6, 7)), px=2, step=40):
    STACK = 0.25
    hs = 360 / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    Wd, Hd = int(360 * px), int((rows + 0.5) * h)
    tiles = {(c, r): (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))
             for c in range(cols) for r in range(rows)}
    area = [k for k in tiles if k != caster and BV.dist(k, caster) <= radius]
    base = Image.new("RGBA", (Wd, Hd), (52, 64, 44, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in tiles.values():
        d.polygon([(x - w / 2, y), (x - w / 4, y - h / 2), (x + w / 4, y - h / 2), (x + w / 2, y),
                   (x + w / 4, y + h / 2), (x - w / 4, y + h / 2)], outline=(255, 255, 255, 30))

    def figure(k, col):
        x, y = tiles[k]
        feet, top = y + 0.4 * h, y - 1.2 * h
        d.ellipse((x - w * 0.16, feet - h * 0.09, x + w * 0.16, feet + h * 0.09), fill=(0, 0, 0, 80))
        d.rounded_rectangle((x - w * 0.085, top + w * 0.16, x + w * 0.085, feet - 3), radius=6, fill=col)
        d.ellipse((x - w * 0.1, top, x + w * 0.1, top + w * 0.2), fill=col)
    for k in enemies:
        figure(k, (96, 58, 52, 255))
    figure(caster, (52, 50, 66, 255))
    cx, cy = tiles[caster]
    src_y = cy - 0.4 * h
    nf, nms, nscale = cs["night"]
    ne = int(round(h * nscale))
    night = [f.resize((ne, ne), Image.LANCZOS) for f in nf]
    sf, sms, _ = cs["streak"]
    thick = int(round(h * 3))
    beams, total = {}, 0
    s = B.SETTINGS["storm"]
    for k in area:
        m, delay, alt = BV.variation(*k, BV.dist(k, caster), mirror=s["mirror"], stagger=s["stagger"], ripple=0,
                                     alternate=True)
        if alt:
            continue
        x, y = tiles[k]
        L_ = max(10, int(math.hypot(x - cx, y - src_y)))
        ang = -math.degrees(math.atan2(y - src_y, x - cx))
        frs = [(f.transpose(Image.FLIP_TOP_BOTTOM) if m else f).resize((L_, thick), Image.LANCZOS)
               .rotate(ang, Image.BICUBIC, expand=True) for f in sf]
        beams[k] = (frs, delay + B.S_LEAD_MS, ((cx + x) / 2, (src_y + y) / 2))
        total = max(total, delay + B.S_LEAD_MS + len(sf) * sms)
    cf, cms, cscale = cs["caster"]
    ce = int(round(h * cscale))
    ca = [f.resize((ce, ce), Image.LANCZOS) for f in cf]
    total = max(total, len(ca) * cms, B.N_LEAD_MS + len(night) * nms) + 400
    shots = []
    for t in range(0, total, step):
        im = base.copy()
        i = (t - B.N_LEAD_MS) // nms
        if t >= B.N_LEAD_MS and i < len(night):
            for k in area + [caster]:
                x, y = tiles[k]
                im.alpha_composite(night[i], (int(x - ne / 2), int(y - ne / 2)))
        for k, (frs, delay, (mx, my)) in beams.items():
            i = (t - delay) // sms
            if t >= delay and i < len(frs):
                g = frs[i]
                im.alpha_composite(g, (int(mx - g.width / 2), int(my - g.height / 2)))
        if t // cms < len(ca):
            im.alpha_composite(ca[t // cms], (int(cx - ce / 2), int(cy - ce / 2)))
        shots.append(im.convert("RGB"))
    return shots


def main():
    shots = render(B.main())
    BV.save(shots, os.path.join(HERE, "preview_fcf_v17_board.gif"))


if __name__ == "__main__":
    main()
