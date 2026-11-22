#!/usr/bin/env python3
"""FCF v24, today's engine: v23 cut into the clips the current renderer can play (2026-11-22).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v24/cut_today.py

The record is GROUND, AOE_SPIRAL_SHOOT range 4 (the caster's tile excluded). Three layers, 128 px frames, at most 32 per strip (the frame time is each clip's length / 32):

| Layer  | Carrier            | Scale | Settings                                   | Job |
|--------|--------------------|-------|--------------------------------------------|-----|
| caster | visual tag (self)  | 3     | none                                       | seal, six tags burning, flames, eruption, the climax core with bolt roots fading out at the clip edge, smoke |
| fury   | recoil appear      | 2     | alternate, mirror, stagger 90, ripple 25   | A lashes on beat 1 (400 ms), B on beat 2 (550 ms): a small whip snaps and bursts on the tile |
| storm  | damage appear      | 3     | alternate, mirror, stagger 140, ripple 15  | the climax (700 ms): a bolt slams down, an impact burst, restrikes; B is smaller, offset, 40 ms later |

A tile clip cannot point at the caster, so the whips and the seven aimed bolts of v23 become per-tile lashes and
strikes; the ripple carries them outward from the caster. Every clip waits on transparent lead frames so its beat
lands on v23's clock. Writes anim_fcf_v24_<layer>.webp strips (each <= 4096 px tall) and preview_fcf_v24_today.gif.
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v23"))
import fcf_v23 as F  # noqa: E402

D, V, BV = F.D, F.V, F.BV
TW, TH, SQ = F.TW, F.TH, F.SQ
CELL = 128                  # the skill's minimum frame size; with the 4096 px strip that allows 32 frames
MAX_FRAMES = 4096 // CELL
K = 2.0                     # drawing pixels per 2x-board pixel (supersampled, then reduced to the strip cell)
LAYERS = {  # name: (scale, duration ms); each layer's frame time is duration / 32, rounded up
    "caster": (3, 1350), "fury": (2, 860), "storm": (3, 1150)}


def ms(layer):
    return -(-LAYERS[layer][1] // MAX_FRAMES)


def canvas(scale):
    e = int(round(TH * scale * K))
    return Image.new("RGBA", (e, e), (0, 0, 0, 0)), e / 2, e / 2


def at(c, dx, dy):
    """Clip point from an offset (2x-board px) from the hex centre."""
    return c[0] + dx * K, c[1] + dy * K


def radial_fade(img, inner, outer):
    w, h = img.size
    m = Image.radial_gradient("L").resize((w, h))          # 0 at the centre, 255 at the corners' circle
    lo, hi = int(255 * inner), int(255 * outer)
    m = m.point(lambda v: 255 if v <= lo else (0 if v >= hi else int(255 * (hi - v) / (hi - lo))))
    img.putalpha(ImageChops.multiply(img.getchannel("A"), m))
    return img


def caster_frames(rnd):
    scale, dur = LAYERS["caster"]
    MS = ms("caster")
    out = []
    tags = [200, 240, 300, 340, 160, 20]                    # back and sides only: never across the fighter
    flames = [i * 36 + rnd.uniform(-8, 8) for i in range(10)]
    bolts = [(i * 51.4 + rnd.uniform(-12, 12), rnd.choice(V.BOLTS), rnd.random() < 0.5) for i in range(7)]
    smoke = [i * 72 + 20 for i in range(5)]
    feet = (0, 0.4 * TH)
    body = (0, -0.4 * TH)
    for t in range(0, dur, MS):
        fr, cx, cy = canvas(scale)
        c = (cx, cy)
        if t < 400:                                         # the seal on the ground under the user
            u = min(1, t / 250)
            f = D.SEC * u * (1 if t < 300 else 1 - (t - 300) / 100)
            D.put(fr, D.xform(D.OUTER, TW * 1.35 * K * (1.1 - 0.1 * u), t * 0.1, f, SQ), *at(c, *feet))
            D.put(fr, D.xform(D.RUNES, TW * 1.0 * K, -t * 0.15, f, SQ), *at(c, *feet))
        if t < 400:                                         # tags catch fire one after another and burn away
            for a in sorted(tags, key=lambda a: math.sin(math.radians(a))):
                x = math.cos(math.radians(a)) * TW * 0.55
                y = 0.4 * TH + math.sin(math.radians(a)) * TW * 0.55 * SQ
                p = max(0.0, (t - 110 - (a % 90) * 0.4) / 220)
                if p < 1:
                    F.place(fr, "tag", F.seq_frame("tag", p), at(c, x, y - TH * 0.1 - TH * 0.8), TH * 0.8 * K / 225,
                            alpha=min(1.0, t / 60))
        if 300 <= t < 1100:                                 # chakra flames at the feet
            e = min(1, (t - 300) / 100) * (1 if t < 900 else 1 - (t - 900) / 200)
            for a in flames:
                x = math.cos(math.radians(a)) * TW * 0.45
                y = 0.4 * TH + math.sin(math.radians(a)) * TW * 0.45 * SQ
                hgt = TH * (0.45 if math.sin(math.radians(a)) > 0.2 else 1.0)
                F.place(fr, "flame", F.seq_frame("flame", (t - 300) / 620 + a / 97.0), at(c, x, y), hgt * K / 225,
                        alpha=0.95 * e)
        if 300 <= t < 360:
            D.put(fr, D.xform(V.FLASH[2], TW * K * (0.9 + (t - 300) / 250), 0, 0.9 * (1 - (t - 300) / 60)), *at(c, *body))
        if 700 <= t < 900:                                  # the climax core: bolt roots leave the user and fade out
            ph = t - 700
            k = 1.0 - ph / 150 if ph < 50 else {1: 0.45, 2: 1.0, 3: 0.18}.get(ph // 50, 0) * (1 - (ph % 50) / 120)
            if k > 0:
                layer = Image.new("RGBA", fr.size, (0, 0, 0, 0))
                for a, img, flip in bolts:
                    r = TH * 1.6
                    end = at(c, body[0] + math.cos(math.radians(a)) * r * 2, body[1] + math.sin(math.radians(a)) * r)
                    s, cc = D.bolt_sprite(img, at(c, *body), end, TH * 1.2 * K, k, flip)
                    D.put(layer, s, *cc)
                fr.alpha_composite(radial_fade(layer, 0.45, 0.98))
            if ph < 50:
                D.put(fr, D.xform(V.FLASH[3], TW * K * (1.2 + ph / 100), 0, 0.92 * (1 - ph / 70)), *at(c, *body))
        for i, a in enumerate(smoke):                       # smoke opens into wisps and thins
            q = (t - 900 - i * 40) / 400
            if 0 <= q <= 1:
                F.place(fr, "smoke", F.seq_frame("smoke", q), at(c, math.cos(math.radians(a)) * TW * 0.35,
                        0.3 * TH + math.sin(math.radians(a)) * TW * 0.17 - 8 * q), TW * 0.8 * K / 250, alpha=0.32)
        out.append(fr)
    return out


def fury_frames(start, flip, seed):
    scale, dur = LAYERS["fury"]
    MS = ms("fury")
    out = []
    for t in range(0, dur, MS):
        fr, cx, cy = canvas(scale)
        ph = t - start
        if 0 <= ph < 310:
            # a short whip from the tile's left edge, snapping across the tile, with the burst where it lands
            p = F.WHIP_EXT * V.ease_out(ph / 70) if ph < 70 else F.WHIP_EXT + (1 - F.WHIP_EXT) * (ph - 70) / 180
            a, b = ((-TW * 0.55, TH * 0.15), (TW * 0.3, -TH * 0.2)) if not seed else ((-TW * 0.35, -TH * 0.6), (TW * 0.3, TH * 0.25))
            dy = -F.WHIP_DY if flip else F.WHIP_DY
            reach = math.hypot(b[0] - a[0], b[1] - a[1]) * K
            ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]) - math.atan2(dy * F.THIN, F.WHIP_DX))
            F.place(fr, "whip", F.seq_frame("whip", p), at((cx, cy), *a), reach / math.hypot(F.WHIP_DX, F.WHIP_DY * F.THIN),
                    ang, alpha=1.0 if ph < 200 else 1 - (ph - 200) / 110, flip=flip, thin=F.THIN)
            if ph >= 60:
                F.place(fr, "burst", F.seq_frame("burst", (ph - 60) / 250), at((cx, cy), b[0], b[1] + TH * 0.25),
                        TW * 0.7 * K / 260)
        out.append(fr)
    return out


def storm_frames(rnd, variant):
    scale, dur = LAYERS["storm"]
    MS = ms("storm")
    out = []
    bolt, flip = rnd.choice(V.BOLTS), rnd.random() < 0.5
    for t in range(0, dur, MS):
        fr, cx, cy = canvas(scale)
        c = (cx, cy)
        ph = t - 700 - (40 if variant else 0)
        ox, oy, size, top = ((TW * 0.15, TH * 0.12, 0.85, (-TW * 0.35, -TH * 1.45)) if not variant else
                             (-TW * 0.2, -TH * 0.05, 0.6, (TW * 0.3, -TH * 1.3)))
        if 0 <= ph < 200:                                   # strike, then two restrikes down the same channel
            k = 1.0 - ph / 150 if ph < 50 else {1: 0.45, 2: 1.0, 3: 0.18}.get(ph // 50, 0) * (1 - (ph % 50) / 120)
            if k > 0:
                layer = Image.new("RGBA", fr.size, (0, 0, 0, 0))
                s, cc = D.bolt_sprite(bolt, at(c, *top), at(c, ox, oy), TH * 1.1 * K, min(1.0, k * 1.3), flip)
                D.put(layer, s, *cc)
                fr.alpha_composite(radial_fade(layer, 0.7, 1.0))
        if 0 <= ph < 330:
            F.place(fr, "burst", F.seq_frame("burst", ph / 330), at(c, ox, oy + TH * 0.2), TW * size * K / 260)
        out.append(fr)
    return out


def strip(frames, cell, path):
    s = Image.new("RGBA", (cell, cell * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        f = f.resize((cell, cell), Image.LANCZOS)
        m = Image.new("L", f.size, 0)                       # 2 px clear margin: linear sampling bleeds between frames
        m.paste(255, (0, 2, cell, cell - 2))
        f.putalpha(ImageChops.multiply(f.getchannel("A"), m))
        s.alpha_composite(f, (0, i * cell))
    assert s.height <= 4096, (path, s.height)
    # 256-colour palette, still saved lossless: the glow keeps its look and the strip fits the byte ceiling
    alpha = s.getchannel("A")                           # the palette would lift empty pixels off zero alpha
    s = s.quantize(256, method=Image.Quantize.FASTOCTREE).convert("RGBA")
    s.putalpha(alpha)
    s.save(path, "WEBP", lossless=True, quality=100, method=6)
    print(os.path.basename(path), f"{cell}x{s.height}", len(frames), "frames", os.path.getsize(path), "bytes")
    return [s.crop((0, i * cell, cell, (i + 1) * cell)) for i in range(len(frames))]


def main():
    rnd = random.Random(24)
    caster = strip(caster_frames(rnd), CELL, os.path.join(HERE, "anim_fcf_v24_caster.webp"))
    fa = strip(fury_frames(400, False, 0), CELL, os.path.join(HERE, "anim_fcf_v24_fury_a.webp"))
    fb = strip(fury_frames(550, True, 1), CELL, os.path.join(HERE, "anim_fcf_v24_fury_b.webp"))
    st = strip(storm_frames(rnd, 0), CELL, os.path.join(HERE, "anim_fcf_v24_storm_a.webp"))
    sb = strip(storm_frames(rnd, 1), CELL, os.path.join(HERE, "anim_fcf_v24_storm_b.webp"))
    shots = BV.render([(fa, fb, ms("fury"), 2, dict(alternate=True, mirror=True, stagger=90, ripple=25)),
                       (st, sb, ms("storm"), 3, dict(alternate=True, mirror=True, stagger=140, ripple=15))],
                      (caster, ms("caster"), 3), "Today's engine", step=20, tail=200)
    BV.save(shots, os.path.join(HERE, "preview_fcf_v24_today.gif"), step=20)


if __name__ == "__main__":
    main()
