#!/usr/bin/env python3
"""FCF v20 MASTER: a particle animation built from the director's painted sprite kit (2026-11-22).

    python3 .../v20/slice_kit.py && python3 .../v20/master_v20.py

Director: "take the painted pieces and animate them yourself with code ... Particle animations are what I'm after."
Every element is a sprite from sprites/ (sliced by slice_kit.py) moved by code: spawned, scaled, rotated, faded,
never slid as a whole picture. Board space, the real board geometry; the seal may span several hexes.

Timeline (t = 0 is the release):
  -500  GATHER   motes spiral in from the whole area onto the user; the seal assembles on the ground across about
                 five hexes: outer ring and rune band scale in and counter-rotate, spokes fly in and lock, the inner
                 ring and star ignite; violet flame tongues lick up round the seal's rim.
  -120  CHARGE   the seal blazes and spins faster; sparks crackle on the user.
     0  RELEASE  starburst and streak flare on the user; one inverted impact frame; the seal shatters (shards fly
                 out spinning, decelerating); an electric shockwave ring and a crisp ring race across the ground.
  0-260 STORM    fourteen painted bolts lash from the user to every part of the area at random moments: each grows
                 out over two frames, lands (flash, a spark burst, two forks thrown off it, rock debris kicked up),
                 afterglows, sometimes restrikes, dies.
  200+  AFTER    smoke puffs rise and curl off the seal and the strike points, motes drift up, it fades.
Writes master_fcf_v20.gif and master_stills_v20.png.
"""
import glob
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v18"))
sys.path.insert(0, os.path.join(HERE, "..", "v10"))
import master_v18 as M  # noqa: E402
import board_v10 as BV  # noqa: E402

W, H, TW, TH, SRC = M.W, M.H, M.TW, M.TH, M.SRC
GROUND = (M.CX, M.CY + 0.4 * TH)                # the user's feet: the seal's centre
STEP = 25
SQ = 0.5                                          # ground squash (the board is 2:1)

SPR = {}
for f in sorted(glob.glob(os.path.join(HERE, "sprites", "*.png"))):
    SPR[os.path.basename(f)[:-4]] = Image.open(f).convert("RGBA")


def kind(k):
    return [SPR[n] for n in sorted(SPR) if n.startswith(k + "_")]


def centred(img):
    """Pad so the alpha centroid sits at the image centre (decorations and glow make crops lopsided)."""
    a = img.getchannel("A").resize((img.width // 4 or 1, img.height // 4 or 1))
    tot = sx = sy = 0
    px = a.load()
    for y in range(a.height):
        for x in range(a.width):
            v = px[x, y]
            tot += v
            sx += v * x
            sy += v * y
    cx, cy = (sx / tot + 0.5) * 4, (sy / tot + 0.5) * 4
    hw = int(max(cx, img.width - cx)) + 1
    hh = int(max(cy, img.height - cy)) + 1
    side = max(hw, hh)
    out = Image.new("RGBA", (2 * side, 2 * side), (0, 0, 0, 0))
    out.paste(img, (int(side - cx), int(side - cy)))
    return out


SEAL = kind("seal")
SEAL[:4] = [centred(x) for x in SEAL[:4]]
OUTER, RUNES, INNER, STAR = SEAL[0], SEAL[1], SEAL[2], SEAL[3]
SPOKES = [img for img in SEAL[4:] if img.height > img.width * 1.4]   # the upright spokes, turned in code
SHARDS, BOLTS, FORKS, SPARKS = kind("shard"), kind("bolt"), kind("fork"), kind("spark")
FLAMES, SMOKE, MOTES, FLASH = kind("flame"), kind("smoke"), kind("mote"), kind("flash")
RINGS, DEBRIS = [centred(x) for x in kind("ring")], kind("debris")
DOTS = MOTES[:16]

_cache = {}


def xform(img, w, rot=0.0, alpha=1.0, squash=1.0, hgt=None):
    """Scale to width w (keeping aspect unless hgt), rotate, squash vertically (ground plane), fade."""
    w = max(2, int(w))
    h = max(2, int(hgt if hgt else img.height * w / img.width))
    key = (id(img), w, h, int(rot) % 360, round(squash, 2))
    out = _cache.get(key)
    if out is None:
        out = img.resize((w, h), Image.LANCZOS)
        if rot:
            out = out.rotate(rot, Image.BICUBIC, expand=True)
        if squash != 1.0:
            out = out.resize((out.width, max(2, int(out.height * squash))), Image.LANCZOS)
        if len(_cache) > 6000:
            _cache.clear()
        _cache[key] = out
    if alpha < 0.999:
        out = out.copy()
        out.putalpha(out.getchannel("A").point(lambda v: int(v * max(0.0, alpha))))
    return out


def put(frame, img, x, y):
    frame.alpha_composite(img, (int(x - img.width / 2), int(y - img.height / 2)))


def ease_out(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def env(t, a, b, fin=0.15, fout=0.3):
    """0 outside [a, b]; fades in over the first fin and out over the last fout of the span."""
    if t < a or t > b:
        return 0.0
    u = (t - a) / max(1, b - a)
    return min(1.0, u / fin if fin else 1.0, (1 - u) / fout if fout else 1.0)


def main(seed=20):
    rnd = random.Random(seed)
    seal_r = TW * 2.3                              # seal radius on the ground (about five hexes across)
    # --- gather motes: spiral in from the area
    gather = [(rnd.uniform(0, 2 * math.pi), rnd.uniform(0.5, 1.0), rnd.uniform(-520, -260), rnd.choice(DOTS),
               rnd.uniform(0.5, 1.2)) for _ in range(60)]
    # --- flame tongues round the rim
    tongues = []
    for k in range(18):
        a = k * 2 * math.pi / 18 + rnd.uniform(-0.1, 0.1)
        tongues.append((a, rnd.uniform(-380, -60), rnd.uniform(280, 520), rnd.choice(FLAMES), rnd.uniform(0.7, 1.3)))
    # --- bolts: two per on-screen sector (far and mid), launch order walks round the circle so every moment of
    # the storm has bolts in different directions
    by_sec = {sec: [] for sec in range(8)}
    for k in M.AREA:
        x, y = M.TILES[k]
        a = math.atan2(y - SRC[1], x - SRC[0])
        by_sec[int(((a + math.pi / 8) % (2 * math.pi)) // (math.pi / 4))].append(k)
    far, mid = [], []
    for sec in range(8):
        ks = sorted(by_sec[sec], key=lambda k: -BV.dist(k, M.CASTER))
        if ks:
            far.append(rnd.choice([k for k in ks if BV.dist(k, M.CASTER) == BV.dist(ks[0], M.CASTER)]))
            mids = [k for k in ks if BV.dist(k, M.CASTER) == 2]
            if mids:
                mid.append(rnd.choice(mids))
    order = [0, 4, 2, 6, 1, 5, 3, 7]
    chosen = [far[i] for i in order if i < len(far)] + [mid[i] for i in order[::-1] if i < len(mid)]
    bolts = []
    for k in chosen:
        x, y = M.TILES[k]
        L = math.hypot(x - SRC[0], y - SRC[1]) * 1.08
        ang = math.degrees(math.atan2(y - SRC[1], x - SRC[0]))
        end = (SRC[0] + math.cos(math.radians(ang)) * L, SRC[1] + math.sin(math.radians(ang)) * L)
        forks = [(rnd.uniform(0.45, 0.8), rnd.choice(FORKS), rnd.choice((-1, 1)) * rnd.uniform(25, 50), rnd.uniform(0.5, 0.8))]
        sparks = [(rnd.uniform(0, 2 * math.pi), rnd.uniform(30, 70), rnd.choice(SPARKS), rnd.uniform(0, 360),
                   rnd.uniform(0.22, 0.4)) for _ in range(4)]
        debris = [(rnd.uniform(-1, 1) * 40, -rnd.uniform(60, 110), rnd.choice(DEBRIS), rnd.uniform(-400, 400),
                   rnd.uniform(0.12, 0.2)) for _ in range(rnd.choice((0, 1, 2)))]
        bolts.append(dict(launch=len(bolts) * 260 / max(1, len(chosen) - 1) + rnd.uniform(-12, 12), img=rnd.choice(BOLTS), L=L, ang=ang, end=end,
                          thick=TH * rnd.uniform(1.3, 1.8), flip=rnd.random() < 0.5, two=rnd.random() < 0.5,
                          forks=forks, sparks=sparks, debris=debris))
    # --- shards: the seal breaks into these, flying out from where they sat
    shards = []
    for i, img in enumerate(SHARDS[:8]):
        a = i * 2 * math.pi / 8 + rnd.uniform(-0.2, 0.2)
        r0 = seal_r * rnd.uniform(0.25, 0.8)
        shards.append((a, r0, img, rnd.uniform(-300, 300), rnd.uniform(0.28, 0.4) * seal_r * 2 / 3))
    # --- smoke and drifting motes afterwards
    smoke = []
    for _ in range(8):
        a = rnd.uniform(0, 2 * math.pi)
        r0 = seal_r * rnd.uniform(0.3, 0.9)
        smoke.append((GROUND[0] + math.cos(a) * r0, GROUND[1] + math.sin(a) * r0 * SQ, rnd.uniform(180, 520),
                      rnd.choice(SMOKE), rnd.uniform(-40, 40), rnd.uniform(0.8, 1.4)))
    for b in bolts:
        smoke.append((b["end"][0], b["end"][1], b["launch"] + 160, rnd.choice(SMOKE), rnd.uniform(-40, 40),
                      rnd.uniform(0.5, 0.8)))
    drift = [(GROUND[0] + rnd.uniform(-1, 1) * seal_r, GROUND[1] + rnd.uniform(-1, 1) * seal_r * SQ,
              rnd.uniform(150, 600), rnd.choice(DOTS), rnd.uniform(0.4, 0.9)) for _ in range(30)]

    times = list(range(-560, 1100, STEP))
    shots = []
    for t in times:
        night = env(t, -560, 1100, 0.18, 0.3)
        fr = _board(night, invert=0 <= t < STEP)
        # ---------------------------------------------------------------- seal (ground plane)
        if t < 0:
            u = ease_out((t + 520) / 300)
            spin = (t + 600) * 0.06 * (1 + (2.0 if t > -120 else 0.0))
            glow = 0.55 + 0.45 * ease_out((t + 300) / 300)
            if t > -120:
                glow = 1.0
            put(fr, xform(OUTER, seal_r * 2 * (1.25 - 0.25 * u), spin, u * glow, SQ), *GROUND)
            put(fr, xform(RUNES, seal_r * 1.55 * (1.3 - 0.3 * u), -spin * 1.4, ease_out((t + 460) / 260) * glow, SQ),
                *GROUND)
            for i in range(8):                       # spokes fly in and lock
                s = SPOKES[i % len(SPOKES)]
                v = ease_out((t + 400 - i * 25) / 180)
                if v <= 0:
                    continue
                a = i * 45 + spin * 0.5
                rr = seal_r * (0.55 + 0.9 * (1 - v))
                x = GROUND[0] + math.cos(math.radians(a)) * rr
                y = GROUND[1] + math.sin(math.radians(a)) * rr * SQ
                # spoke drawn along its own radius: rotate so its long axis points out
                put(fr, xform(s, seal_r * 0.22 * s.width / s.height * 2.2, -a - 90, v * glow, SQ,
                              hgt=seal_r * 0.48), x, y)
            iv = ease_out((t + 260) / 160)
            if iv > 0:
                put(fr, xform(INNER, seal_r * 0.9, spin * 2, iv * glow, SQ), *GROUND)
            sv = ease_out((t + 180) / 140)
            if sv > 0:
                pulse = 1 + (0.12 * math.sin(t / 18) if t > -120 else 0)
                put(fr, xform(STAR, seal_r * 0.75 * pulse, -spin * 0.8, sv, SQ), *GROUND)
            if t > -120:                              # the blaze: the seal drawn twice
                put(fr, xform(RUNES, seal_r * 1.55, -spin * 1.4, 0.6, SQ), *GROUND)
        # ---------------------------------------------------------------- flame tongues on the rim
        for a, t0, life, img, sc in tongues:
            e = env(t, t0, t0 + life, 0.25, 0.4)
            if e <= 0:
                continue
            u = (t - t0) / life
            x = GROUND[0] + math.cos(a) * seal_r * 0.95
            y = GROUND[1] + math.sin(a) * seal_r * 0.95 * SQ
            hgt = TH * 1.3 * sc * (0.5 + 0.7 * math.sin(math.pi * min(1, u * 1.2)))
            wob = 6 * math.sin(t / 30 + a * 3)
            spr = xform(img, hgt * img.width / img.height, wob, e * 0.9)
            fr.alpha_composite(spr, (int(x - spr.width / 2), int(y - spr.height)))
        # ---------------------------------------------------------------- gather motes spiral in
        for a, rr, t0, img, sc in gather:
            u = (t - t0) / 380
            if not 0 <= u <= 1:
                continue
            r = (1 - ease_out(u)) * rr * TW * 4.2
            aa = a + 2.4 * u
            x = SRC[0] + math.cos(aa) * r
            y = SRC[1] + math.sin(aa) * r * 0.62
            put(fr, xform(img, 14 * sc * (0.6 + 0.6 * u), 0, min(1, u * 4) * (1 - u * 0.3)), x, y)
        # ---------------------------------------------------------------- charge sparks on the user
        if -140 < t < 40:
            for j in range(3):
                img = SPARKS[(t // STEP * 3 + j) % len(SPARKS)]
                a = (t * 7 + j * 120) % 360
                put(fr, xform(img, 34, a, 0.9), SRC[0] + rnd.uniform(-10, 10), SRC[1] + rnd.uniform(-14, 10))
        # ---------------------------------------------------------------- release
        if 0 <= t < 175:
            u = t / 175
            put(fr, xform(FLASH[3], TW * (2.2 - 1.2 * u), t * 0.8, 1 - u), *SRC)
            put(fr, xform(FLASH[4], TW * 5 * (1 - 0.4 * u), 0, (1 - u) * 0.9), *SRC)
        if 0 <= t < 450:                              # shockwave rings on the ground
            for img, delay, a0 in ((RINGS[0], 0, 0.85),):
                u = (t - delay) / 300
                if 0 <= u <= 1:
                    put(fr, xform(img, TW * (1 + 5.6 * ease_out(u)), 0, a0 * (1 - u) ** 1.5, SQ), *GROUND)
        for a, r0, img, spin, size in shards:          # the seal breaks
            u = t / 450
            if not 0 <= u <= 1:
                continue
            r = r0 + seal_r * 1.6 * ease_out(u)
            x = GROUND[0] + math.cos(a) * r
            y = GROUND[1] + math.sin(a) * r * SQ - TH * 1.2 * math.sin(math.pi * u) * 0.6
            put(fr, xform(img, size, spin * u, (1 - u) ** 1.3, 0.75), x, y)
        # ---------------------------------------------------------------- the storm
        for b in bolts:
            ph = t - b["launch"]
            if ph < 0:
                continue
            beats = ["grow", "land", "glow", "dark", "re", "die"] if b["two"] else ["grow", "land", "glow", "die"]
            i = int(ph // 50)
            if i < len(beats):
                beat = beats[i]
                img = b["img"].transpose(Image.FLIP_TOP_BOTTOM) if b["flip"] else b["img"]
                body = img.resize((int(b["L"]), int(b["thick"])), Image.LANCZOS)
                if beat == "grow":
                    frac = 0.5 if ph % 50 < 25 else 0.85
                    m = Image.new("L", body.size, 0)
                    ImageDraw.Draw(m).rectangle((0, 0, int(body.width * frac), body.height), fill=255)
                    m = m.filter(ImageFilter.GaussianBlur(max(2, body.width * 0.05)))
                    body.putalpha(ImageChops.multiply(body.getchannel("A"), m))
                k = {"grow": 1.0, "land": 1.0, "glow": 0.55, "dark": 0.15, "re": 0.95, "die": 0.25}[beat]
                if k < 1:
                    body.putalpha(body.getchannel("A").point(lambda v, k=k: int(v * k)))
                r = body.rotate(-b["ang"], Image.BICUBIC, expand=True)
                cx = SRC[0] + math.cos(math.radians(b["ang"])) * b["L"] / 2
                cy = SRC[1] + math.sin(math.radians(b["ang"])) * b["L"] / 2
                put(fr, r, cx, cy)
                if beat in ("land", "re"):              # forks thrown off the bolt
                    for along, fimg, off, sc in b["forks"]:
                        px = SRC[0] + math.cos(math.radians(b["ang"])) * b["L"] * along
                        py = SRC[1] + math.sin(math.radians(b["ang"])) * b["L"] * along
                        put(fr, xform(fimg, TW * 0.9 * sc, -(b["ang"] + off), 0.9 if beat == "land" else 0.6), px, py)
                if beat == "land":
                    put(fr, xform(FLASH[2], TW * 0.45, b["ang"], 0.7), *b["end"])   # a small crisp glint, no ball
            ex, ey = b["end"]
            for a, spd, simg, rot, sc in b["sparks"]:   # spark burst at the strike
                u = (ph - 50) / 300
                if 0 <= u <= 1:
                    d = spd * ease_out(u)
                    put(fr, xform(simg, TW * sc * (1 - 0.5 * u), rot + 200 * u, 1 - u),
                        ex + math.cos(a) * d, ey + math.sin(a) * d * 0.6 + 20 * u * u)
            for vx, vy, dimg, spin, sc in b["debris"]:  # rock kicked up, falls back
                s = (ph - 50) / 1000
                if 0 <= s <= 0.45:
                    x = ex + vx * s * 2
                    y = ey + vy * s * 2 + 520 * s * s
                    if y <= ey + 4:
                        put(fr, xform(dimg, TW * sc, spin * s, min(1, (0.45 - s) * 6)), x, y)
        # ---------------------------------------------------------------- aftermath
        for x0, y0, t0, img, spin, sc in smoke:
            e = env(t, t0, t0 + 550, 0.25, 0.55)
            if e <= 0:
                continue
            u = (t - t0) / 550
            spr = xform(img, TW * 0.75 * sc * (0.7 + 0.7 * u), spin * u, e * 0.5)
            put(fr, spr, x0 + 10 * math.sin(u * 3 + x0), y0 - TH * 0.8 * u - spr.height * 0.3)
        for x0, y0, t0, img, sc in drift:
            e = env(t, t0, t0 + 600, 0.2, 0.5)
            if e > 0:
                u = (t - t0) / 600
                put(fr, xform(img, 12 * sc, 0, e), x0 + 8 * math.sin(u * 5 + y0), y0 - TH * 1.4 * u)
        shots.append(fr.convert("RGB"))
    shots[0].save(os.path.join(HERE, "master_fcf_v20.gif"), save_all=True, append_images=shots[1:], duration=STEP,
                  loop=0, optimize=True)
    picks = [-380, -150, 0, 75, 200, 400, 700]
    sheet = Image.new("RGB", (W, H * len(picks)))
    for i, x in enumerate(picks):
        sheet.paste(shots[next(j for j, tt in enumerate(times) if tt >= x)], (0, i * H))
    sheet.save(os.path.join(HERE, "master_stills_v20.png"))
    print(len(shots), "frames")


def _board(night, invert=False):
    base = Image.new("RGBA", (W, H), (52, 64, 44, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in M.TILES.values():
        d.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                   (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], outline=(255, 255, 255, 30))
    for k, col in (((8, 3), (96, 58, 52, 255)), ((2, 5), (96, 58, 52, 255)), ((6, 7), (96, 58, 52, 255)),
                   (M.CASTER, (52, 50, 66, 255))):
        x, y = M.TILES[k]
        feet, top = y + 0.4 * TH, y - 1.2 * TH
        d.ellipse((x - TW * 0.16, feet - TH * 0.09, x + TW * 0.16, feet + TH * 0.09), fill=(0, 0, 0, 80))
        d.rounded_rectangle((x - TW * 0.085, top + TW * 0.16, x + TW * 0.085, feet - 3), radius=6, fill=col)
        d.ellipse((x - TW * 0.1, top, x + TW * 0.1, top + TW * 0.2), fill=col)
    if night:
        m = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(m)
        for k in M.AREA + [M.CASTER]:
            x, y = M.TILES[k]
            md.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                        (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(8))
        dark = Image.new("RGBA", (W, H), (6, 2, 14, 0))
        dark.putalpha(m.point(lambda v: int(v * night * (0.93 if invert else 0.6))))
        base.alpha_composite(dark)
    return base


if __name__ == "__main__":
    main()
