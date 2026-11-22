#!/usr/bin/env python3
"""FCF v21: the approved blockout (blockout_v21.py) dressed with the painted sprite kit, tier by tier (2026-11-22).

    python3 .../v20/slice_kit.py && python3 .../v21/dress_v21.py

Same beats and 50 ms frames as the blockout, at real board size. Value tiers carried into opacity and size:
  PRIMARY   painted bolts at full strength, their heavy end at the strike point (the brightest edge where the eye
            should go); the climax starburst
  SECONDARY seal parts and the shockwave at ~65 % opacity
  TERTIARY  motes, sparks, smoke: small, ~35-60 % opacity, few
Writes fcf_v21_real.gif, fcf_v21_2x.gif and fcf_v21_beats.png.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v20"))
import master_v20 as V  # noqa: E402  (sprites, xform, put, board geometry)
import blockout_v21 as BO  # noqa: E402

M, BV = V.M, V.BV
W, H, TW, TH, SRC, GROUND = V.W, V.H, V.TW, V.TH, V.SRC, V.GROUND
SQ, xform, put = V.SQ, V.xform, V.put
SEAL_R = BO.SEAL_R
STEP = 50
SEC = 0.65


def board():
    im = Image.new("RGBA", (W, H), (46, 54, 40, 255))
    d = ImageDraw.Draw(im)
    for (x, y) in M.TILES.values():
        d.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                   (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], outline=(62, 72, 56, 255))
    for k in ((8, 3), (2, 5), (6, 7), M.CASTER):
        x, y = M.TILES[k]
        col = (70, 66, 82, 255) if k == M.CASTER else (100, 64, 58, 255)
        d.ellipse((x - TW * 0.16, y + 0.4 * TH - TH * 0.09, x + TW * 0.16, y + 0.4 * TH + TH * 0.09), fill=(0, 0, 0, 80))
        d.rounded_rectangle((x - TW * 0.085, y - 1.2 * TH + TW * 0.16, x + TW * 0.085, y + 0.4 * TH - 3), 6, fill=col)
        d.ellipse((x - TW * 0.1, y - 1.2 * TH, x + TW * 0.1, y - 1.2 * TH + TW * 0.2), fill=col)
    return im


def bolt_sprite(img, a, b, thick, alpha, flip):
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    body = img.transpose(Image.FLIP_LEFT_RIGHT)          # heavy end at the strike point
    if flip:
        body = body.transpose(Image.FLIP_TOP_BOTTOM)
    body = xform(body, L, -ang, alpha, 1.0, hgt=thick)
    return body, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def main(seed=21):
    rnd = random.Random(seed)
    by_sec = {s: [] for s in range(8)}
    for k in M.AREA:
        x, y = M.TILES[k]
        a = math.atan2(y - SRC[1], x - SRC[0])
        by_sec[int(((a + math.pi / 8) % (2 * math.pi)) // (math.pi / 4))].append(k)
    far = [sorted(by_sec[s], key=lambda k: -BV.dist(k, M.CASTER))[0] for s in range(8) if by_sec[s]]
    mains = far[:7]
    strag = far[7:8] + [k for s in (1, 3, 5) for k in by_sec[s] if BV.dist(k, M.CASTER) == 2][:3]

    def end(k, extra=1.06):
        x, y = M.TILES[k]
        return (SRC[0] + (x - SRC[0]) * extra, SRC[1] + (y - SRC[1]) * extra)
    mb = [(end(k), rnd.choice(V.BOLTS), rnd.random() < 0.5, TH * rnd.uniform(1.4, 1.8)) for k in mains]
    sb = [(400 + i * 50, end(k), rnd.choice(V.BOLTS), rnd.random() < 0.5, TH * rnd.uniform(1.1, 1.4))
          for i, k in enumerate(strag)]
    motes = [(rnd.uniform(0, 2 * math.pi), rnd.uniform(0.6, 1.0), rnd.choice(V.DOTS)) for _ in range(14)]
    sparks = [(e, rnd.uniform(0, 2 * math.pi), rnd.choice(V.SPARKS)) for e, _, _, _ in mb for _ in range(2)]
    shards = [(i * math.pi / 4 + 0.3, V.SHARDS[i]) for i in range(8)]
    smoke = [(i * 1.26, rnd.choice(V.SMOKE)) for i in range(5)]
    frames, labels = [], []
    for t in range(0, 1000, STEP):
        fr = board()
        beat = ""
        if t < 300:                                       # WIND-UP
            beat = "WIND-UP"
            u = t / 300
            spin = t * 0.15
            put(fr, xform(V.OUTER, SEAL_R * 2 * (1.15 - 0.15 * u), spin, SEC * min(1, 0.4 + u), SQ), *GROUND)
            if t >= 100:
                put(fr, xform(V.RUNES, SEAL_R * 1.4, -spin * 1.5, SEC, SQ), *GROUND)
            if t >= 200:
                for i in range(8):
                    a = i * 45 + spin * 0.4
                    s = V.SPOKES[i % len(V.SPOKES)]
                    x = GROUND[0] + math.cos(math.radians(a)) * SEAL_R * 0.42
                    y = GROUND[1] + math.sin(math.radians(a)) * SEAL_R * 0.42 * SQ
                    put(fr, xform(s, SEAL_R * 0.11, -a - 90, SEC, SQ, hgt=SEAL_R * 0.4), x, y)
                put(fr, xform(V.STAR, SEAL_R * 0.6, -spin, SEC, SQ), *GROUND)
            put(fr, xform(V.FLASH[0], TW * (0.4 + 0.6 * u), 0, 0.45 + 0.4 * u), *SRC)
            for a, rr, img in motes:
                rad = (1 - u) * rr * TW * 4
                put(fr, xform(img, 12, 0, 0.55), SRC[0] + math.cos(a + 2 * u) * rad,
                    SRC[1] + math.sin(a + 2 * u) * rad * 0.6)
        if t == 300:                                      # CLIMAX
            beat = "CLIMAX"
            for e, img, flip, th in mb:
                s, c = bolt_sprite(img, SRC, e, th * 1.15, 1.0, flip)
                put(fr, s, *c)
            put(fr, xform(V.FLASH[3], TW * 1.7, 0, 1.0), *SRC)
        if 300 <= t < 700:                                # the seal breaks
            u = (t - 300) / 400
            for a, img in shards:
                rr = SEAL_R * (0.45 + 1.0 * u)
                put(fr, xform(img, SEAL_R * 0.32 * (1 - 0.4 * u), (t - 300) * 0.6, SEC * (1 - u) ** 1.2, 0.7),
                    GROUND[0] + math.cos(a) * rr, GROUND[1] + math.sin(a) * rr * SQ - TH * 0.6 * math.sin(math.pi * u))
        if 350 <= t < 500:                                # FLICKER + shockwave
            beat = beat or "FLICKER"
            k, w = {350: (0.45, 0.8), 400: (1.0, 1.0), 450: (0.18, 0.7)}[t]
            for e, img, flip, th in mb:
                s, c = bolt_sprite(img, SRC, e, th * w, k, flip)
                put(fr, s, *c)
            u = (t - 350) / 150
            put(fr, xform(V.RINGS[0], TW * (3 + 8.4 * u), 0, SEC * (1 - u * 0.7), SQ), *GROUND)
        for t0, e, img, flip, th in sb:                   # STRAGGLERS
            ph = t - t0
            if ph in (0, 50):
                s, c = bolt_sprite(img, SRC, e, th * (1 if ph == 0 else 0.8), 1.0 if ph == 0 else 0.4, flip)
                put(fr, s, *c)
                if ph == 0:
                    beat = beat or "STRAGGLERS"
        if 300 < t < 650:                                 # sparks at the strike points
            u = (t - 300) / 350
            for (x, y), a, img in sparks:
                put(fr, xform(img, TW * 0.35 * (1 - 0.5 * u), (t - 300) * 0.5, 0.6 * (1 - u)),
                    x + math.cos(a) * 30 * u, y + math.sin(a) * 18 * u + 10 * u * u)
        if 500 <= t < 900:                                # FADE-OUT: a little smoke
            beat = beat or "FADE-OUT"
            u = (t - 500) / 400
            for a, img in smoke:
                put(fr, xform(img, TW * (0.7 + 0.4 * u), 0, 0.35 * math.sin(math.pi * u)),
                    GROUND[0] + math.cos(a) * SEAL_R * 0.5, GROUND[1] + math.sin(a) * SEAL_R * 0.25 - 30 * u)
        frames.append(fr.convert("RGB").resize((W // 2, H // 2), Image.LANCZOS))
        labels.append((t, beat))
    frames[0].save(os.path.join(HERE, "fcf_v21_real.gif"), save_all=True, append_images=frames[1:], duration=STEP,
                   loop=0)
    big = [f.resize((f.width * 2, f.height * 2), Image.LANCZOS) for f in frames]
    big[0].save(os.path.join(HERE, "fcf_v21_2x.gif"), save_all=True, append_images=big[1:], duration=STEP, loop=0)
    cols = 4
    fw, fh = big[0].size
    sheet = Image.new("RGB", (fw * cols, (fh + 14) * ((len(big) + cols - 1) // cols)), (12, 12, 12))
    sd = ImageDraw.Draw(sheet)
    for i, (f, (t, b)) in enumerate(zip(big, labels)):
        x, y = (i % cols) * fw, (i // cols) * (fh + 14)
        sheet.paste(f, (x, y + 14))
        sd.text((x + 3, y + 1), f"{t} ms  {b}", fill=(255, 220, 90))
    sheet.save(os.path.join(HERE, "fcf_v21_beats.png"))
    print(len(frames), "frames")


if __name__ == "__main__":
    main()
