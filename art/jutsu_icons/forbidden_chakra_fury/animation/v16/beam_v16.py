#!/usr/bin/env python3
"""FCF v16 beam study: each strike is ONE streak from the caster to the struck tile (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v16/beam_v16.py

Simulates a proposed per-effect setting `animationBeam` (an extension of the area-variation PR): instead of centring
each tile's clip on the tile, the renderer stretches it from the caster's tile to that tile - positioned at the
midpoint, turned to the angle between them, widened to their distance. Art is drawn left (caster) to right (tile).
With alternate = an empty clip, about half the tiles are struck; a wide stagger spreads the strikes over ~0.8 s.
Writes preview_fcf_v16_beam.gif.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "v10"))
import board_v10 as BV  # noqa: E402
import build_v16 as B  # noqa: E402

V, G, L = B.V, B.G, B.L
N, SS, SC = B.N, B.SS, B.SC
BEAM = dict(mirror=True, stagger=700, ripple=30, alternate=True)


def beam_frames(seed):
    """Drawn across the whole clip, caster at the left edge, the struck tile at the right; many sharp kinks so the
    streak stays jagged when the renderer stretches it to the distance."""
    rnd = random.Random(seed)
    W = N * SS
    channel = G.angular((0, SC), (N - 6, SC + rnd.uniform(-3, 3)), rnd, 0.16, 0.035)
    channel = [(x, SC + (y - SC) * 3.2) for x, y in channel]   # tall kinks: they flatten when stretched
    stubs = []
    for _ in range(3):
        i = rnd.randrange(len(channel) // 4, len(channel) - 3)
        p = channel[i]
        a = rnd.uniform(-1.0, 1.0)
        stubs.append(G.angular(p, (p[0] + math.cos(a) * 14, p[1] + math.sin(a) * 18), rnd, 0.35, 0.05))
    beats = [("leader", 0.45), ("leader", 0.85), ("stroke", 0), ("after", 0), ("dark", 0), ("restrike", 0),
             ("dark", 1), ("restrike", 1), ("after", 1), ("fade", 0)]
    out = []
    end = channel[-1]
    for t, (beat, k) in enumerate(beats):
        cv = V.Canvas()
        if beat == "leader":
            n = int(len(channel) * k)
            cv.tapered(channel[:n], 1.0, 0.8, 80, 100)
        elif beat == "stroke":
            B.big_bolt(cv, channel, 5.0, 255)
            for s in stubs:
                cv.tapered(s, 1.8, 0.3, 220, 80)
            cv.blob(end[0], end[1], 12, 9, 220)
            cv.blob(end[0], end[1], 5, 4, 255, 0.3, target="core")
        elif beat == "after":
            B.big_bolt(cv, channel, 3.2 - k, 190 - 50 * k)
        elif beat == "dark":
            cv.tapered(channel, 1.0, 1.0, 50 - 15 * k, 50 - 15 * k)
        elif beat == "restrike":
            B.big_bolt(cv, channel, 4.2 - 0.8 * k, 245 - 25 * k)
            cv.blob(end[0], end[1], 9, 7, 160)
        else:
            cv.tapered(channel, 0.8, 0.8, 30, 30)
        out.append(cv.render(V.plasma(seed, t, W), gains=(1.0, 1.1, 0.6), pool_r=6))
    return out


def render(clips, beam_a, cols=12, rows=8, caster=(5, 4), radius=4, enemies=((8, 3), (2, 5), (6, 7)), px=2, step=40,
           lead_ms=400):
    STACK = 0.25
    hs = 360 / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    Wd, Hd = int(360 * px), int((rows + 0.5) * h)
    tiles = {(c, r): (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))
             for c in range(cols) for r in range(rows)}
    area = sorted([k for k in tiles if k != caster and BV.dist(k, caster) <= radius], key=lambda k: tiles[k][1])
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
    src_y = cy - 0.4 * h                      # bolts leave from the body
    # floor (centred, not beamed)
    fa, fms, fscale = clips["floor_a"]
    fb = clips["floor_b"][0]
    fe = int(round(h * fscale))
    fA = [f.resize((fe, fe), Image.LANCZOS) for f in fa]
    fB = [f.resize((fe, fe), Image.LANCZOS) for f in fb]
    beams, floors, total = {}, {}, 0
    thick = int(round(h * 3))
    for k in area:
        m, delay, alt = BV.variation(*k, BV.dist(k, caster), **BEAM)
        x, y = tiles[k]
        floors[k] = (fB if alt else fA, delay + lead_ms + 2 * 50 - 8 * 50)
        if alt:
            continue
        L_ = max(10, int(math.hypot(x - cx, y - src_y)))
        ang = -math.degrees(math.atan2(y - src_y, x - cx))
        frs = []
        for f in beam_a:
            g = f.transpose(Image.FLIP_TOP_BOTTOM) if m else f
            g = g.resize((L_, thick), Image.LANCZOS).rotate(ang, Image.BICUBIC, expand=True)
            frs.append(g)
        beams[k] = (frs, delay + lead_ms, ((cx + x) / 2, (src_y + y) / 2))
        total = max(total, delay + lead_ms + len(beam_a) * 50)
    cf, cms, cscale = clips["caster"]
    ce = int(round(h * cscale))
    ca = [f.resize((ce, ce), Image.LANCZOS) for f in cf]
    total = max(total, len(ca) * cms) + 500
    shots = []
    for t in range(0, total, step):
        im = base.copy()
        for k, (frs, delay) in floors.items():
            i = (t - delay) // fms
            if t >= delay and i < len(frs):
                x, y = tiles[k]
                im.alpha_composite(frs[i], (int(x - fe / 2), int(y - fe / 2)))
        for k, (frs, delay, (mx, my)) in beams.items():
            i = (t - delay) // 50
            if t >= delay and i < len(frs):
                g = frs[i]
                im.alpha_composite(g, (int(mx - g.width / 2), int(my - g.height / 2)))
        if t // cms < len(ca):
            im.alpha_composite(ca[t // cms], (int(cx - ce / 2), int(cy - ce / 2)))
        shots.append(im.convert("RGB"))
    return shots


def main():
    cs = B.clips()
    ba = beam_frames(61)
    shots = render(cs, ba)
    BV.save(shots, os.path.join(HERE, "preview_fcf_v16_beam.gif"))
    sheet_t = (440, 600, 800, 1000, 1200, 1500)
    W, H = shots[0].size
    out = Image.new("RGB", (W, H * len(sheet_t)))
    for i, t in enumerate(sheet_t):
        out.paste(shots[min(t // 40, len(shots) - 1)], (0, i * H))
    out.save(os.path.join(HERE, "stills_fcf_v16_beam.png"))
    fn = os.path.join(HERE, f"anim_fcf_v16_beam_{N}.webp")
    print("beam strip", B.K.write_strip(ba, fn, N), "bytes")


if __name__ == "__main__":
    main()
