#!/usr/bin/env python3
"""FCF v21 BLOCKOUT: timing and hierarchy in plain grey shapes, at true game size and engine frame rate (2026-11-22).

    python3 .../v21/blockout_v21.py

The step studios do before any art: lock the beats with simple shapes, then dress them. Rendered at real board scale
(the board is 360 px wide, one tile ~39 px wide) on 50 ms frames, the rate area clips play at. Three value tiers:
  PRIMARY   (white, 235)  the climax flash and the main bolts' tips/cores
  SECONDARY (grey, 150)   the seal and the shockwave
  TERTIARY  (dark, 95)    motes, sparks, smoke
Beats (1.2 s):
  0-300    WIND-UP   the seal draws on (ring, then band, then star) and tightens; charge glow on the user; motes in
  300      CLIMAX    one white frame: the flash, the seal breaks, 7 main bolts land at once (within 100 ms)
  350-450  FLICKER   main bolts dim, restrike once; shockwave ring runs to the area edge
  400-550  STRAGGLERS 4 late bolts into the gaps
  550-1200 FADE-OUT  sparks and a little smoke, fast; clear by 1.2 s
Writes blockout_fcf_v21_real.gif (real size), blockout_fcf_v21_2x.gif and blockout_beats_v21.png.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v18"))
sys.path.insert(0, os.path.join(HERE, "..", "v10"))
import master_v18 as M  # noqa: E402
import board_v10 as BV  # noqa: E402

W, H, TW, TH, SRC = M.W, M.H, M.TW, M.TH, M.SRC   # drawn at 2x, delivered at 1x
GROUND = (M.CX, M.CY + 0.4 * TH)
P, S, T = 235, 150, 95
STEP = 50
SEAL_R = TW * 2.3


def jag(a, b, rnd, kinks=4, amp=0.18):
    pts = [a]
    for k in range(1, kinks):
        u = k / kinks
        x = a[0] + (b[0] - a[0]) * u
        y = a[1] + (b[1] - a[1]) * u
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        off = rnd.uniform(-1, 1) * amp * L
        pts.append((x - dy / L * off, y + dx / L * off))
    return pts + [b]


def ell(d, c, rx, val, w):
    d.ellipse((c[0] - rx, c[1] - rx * 0.5, c[0] + rx, c[1] + rx * 0.5), outline=(val, val, val), width=int(w))


def main(seed=21):
    rnd = random.Random(seed)
    by_sec = {s: [] for s in range(8)}
    for k in M.AREA:
        x, y = M.TILES[k]
        a = math.atan2(y - SRC[1], x - SRC[0])
        by_sec[int(((a + math.pi / 8) % (2 * math.pi)) // (math.pi / 4))].append(k)
    far = []
    for s in range(8):
        ks = sorted(by_sec[s], key=lambda k: -BV.dist(k, M.CASTER))
        if ks:
            far.append(ks[0])
    mains = far[:7] if len(far) > 7 else far          # 7 main bolts, every direction but one
    stragglers = [far[7]] if len(far) > 7 else []
    mids = [k for s in (1, 3, 5) for k in by_sec[s] if BV.dist(k, M.CASTER) == 2][:3]
    stragglers += mids

    def bolt_path(k, extra=1.06):
        x, y = M.TILES[k]
        e = (SRC[0] + (x - SRC[0]) * extra, SRC[1] + (y - SRC[1]) * extra)
        return jag(SRC, e, rnd)
    main_paths = [bolt_path(k) for k in mains]
    strag = [(400 + i * 50, bolt_path(k)) for i, k in enumerate(stragglers)]
    motes = [(rnd.uniform(0, 2 * math.pi), rnd.uniform(0.6, 1.0)) for _ in range(14)]
    sparks = [(p[-1], rnd.uniform(0, 2 * math.pi)) for p in main_paths for _ in range(2)]
    frames, labels = [], []
    for t in range(0, 1000, STEP):
        im = Image.new("RGB", (W, H), (46, 54, 40))
        d = ImageDraw.Draw(im)
        for (x, y) in M.TILES.values():
            d.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                       (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], outline=(62, 72, 56))
        for k in ((8, 3), (2, 5), (6, 7), M.CASTER):
            x, y = M.TILES[k]
            col = (70, 66, 82) if k == M.CASTER else (100, 64, 58)
            d.rounded_rectangle((x - TW * 0.085, y - 1.2 * TH + TW * 0.16, x + TW * 0.085, y + 0.4 * TH - 3), 6, fill=col)
            d.ellipse((x - TW * 0.1, y - 1.2 * TH, x + TW * 0.1, y - 1.2 * TH + TW * 0.2), fill=col)
        beat = ""
        # WIND-UP: seal draws on and tightens; charge glow; motes in
        if t < 300:
            beat = "WIND-UP"
            u = t / 300
            ell(d, GROUND, SEAL_R * (1.15 - 0.15 * u), S, 4)
            if t >= 100:
                ell(d, GROUND, SEAL_R * 0.7, S, 6)
            if t >= 200:
                for i in range(8):
                    a = i * math.pi / 4
                    d.line([GROUND, (GROUND[0] + math.cos(a) * SEAL_R * 0.4, GROUND[1] + math.sin(a) * SEAL_R * 0.2)],
                           fill=(S, S, S), width=4)
            r = 8 + 14 * u
            d.ellipse((SRC[0] - r, SRC[1] - r, SRC[0] + r, SRC[1] + r), outline=(S, S, S), width=4)
            for a, rr in motes:
                rad = (1 - u) * rr * TW * 4
                x, y = SRC[0] + math.cos(a + 2 * u) * rad, SRC[1] + math.sin(a + 2 * u) * rad * 0.6
                d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(T, T, T))
        # CLIMAX
        if t == 300:
            beat = "CLIMAX"
            d.ellipse((SRC[0] - 46, SRC[1] - 40, SRC[0] + 46, SRC[1] + 40), fill=(P, P, P))
            for p in main_paths:
                d.line(p, fill=(P, P, P), width=12)
        if 300 <= t < 700:                             # the seal breaks: 8 chunks fly out
            u = (t - 300) / 400
            for i in range(8):
                a = i * math.pi / 4 + 0.3
                rr = SEAL_R * (0.5 + 1.0 * u)
                x, y = GROUND[0] + math.cos(a) * rr, GROUND[1] + math.sin(a) * rr * 0.5
                s = 14 * (1 - u)
                if s > 2:
                    d.rectangle((x - s, y - s / 2, x + s, y + s / 2), fill=(S, S, S))
        if 350 <= t < 500:                             # FLICKER: dim, restrike, dim
            beat = beat or "FLICKER"
            v, w = {350: (S, 6), 400: (P, 10), 450: (T, 4)}[t]
            for p in main_paths:
                d.line(p, fill=(v, v, v), width=w)
            u = (t - 350) / 150
            ell(d, GROUND, TW * (1.5 + 4.2 * u), S, 4)
        for t0, p in strag:                            # STRAGGLERS
            ph = t - t0
            if ph == 0:
                d.line(p, fill=(P, P, P), width=10)
                beat = beat or "STRAGGLERS"
            elif ph == 50:
                d.line(p, fill=(S, S, S), width=5)
        if 300 < t < 650:                              # sparks at main strike points
            u = (t - 300) / 350
            for (x, y), a in sparks:
                d.line([(x, y), (x + math.cos(a) * 30 * u, y + math.sin(a) * 18 * u + 10 * u * u)], fill=(T, T, T),
                       width=3)
        if 500 <= t < 900:                             # FADE-OUT: a little smoke
            beat = beat or "FADE-OUT"
            u = (t - 500) / 400
            v = int(46 + (T - 46) * (1 - u))
            for i in range(5):
                a = i * 1.26
                x = GROUND[0] + math.cos(a) * SEAL_R * 0.5
                y = GROUND[1] + math.sin(a) * SEAL_R * 0.25 - 30 * u
                r = 14 + 12 * u
                d.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.7), outline=(v, v, v), width=3)
        real = im.resize((W // 2, H // 2), Image.LANCZOS)
        frames.append(real)
        labels.append((t, beat))
    frames[0].save(os.path.join(HERE, "blockout_fcf_v21_real.gif"), save_all=True, append_images=frames[1:],
                   duration=STEP, loop=0)
    big = [f.resize((f.width * 2, f.height * 2), Image.NEAREST) for f in frames]
    big[0].save(os.path.join(HERE, "blockout_fcf_v21_2x.gif"), save_all=True, append_images=big[1:], duration=STEP,
                loop=0)
    cols = 5
    fw, fh = frames[0].size
    sheet = Image.new("RGB", (fw * cols, (fh + 14) * ((len(frames) + cols - 1) // cols)), (12, 12, 12))
    sd = ImageDraw.Draw(sheet)
    for i, (f, (t, b)) in enumerate(zip(frames, labels)):
        x, y = (i % cols) * fw, (i // cols) * (fh + 14)
        sheet.paste(f, (x, y + 14))
        sd.text((x + 3, y + 1), f"{t} ms  {b}", fill=(255, 220, 90))
    sheet.save(os.path.join(HERE, "blockout_beats_v21.png"))
    print(len(frames), "frames")


if __name__ == "__main__":
    main()
