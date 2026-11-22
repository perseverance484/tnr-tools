#!/usr/bin/env python3
"""Forbidden Chakra Fury v13: HD look, with the ground detail moved to where the engine can hide the repeat
(2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v13/build_v13.py

Director: v12's ground webs looked like "a 90s game"; wanted a high-definition modern look. Then chose, for the
ground: "Glow floor + crater rifts".
- FLOOR (recoil, scale 2): a charged glow that fills each hex edge to edge with feathered edges, so tiles join
  seamlessly; a drifting plasma texture runs through it, and HD lightning crawls across the ground in new shapes
  every couple of frames. Nothing on it is a permanent pattern, so the per-tile repeat does not show.
- STORM (damage, scale 3; A eruption / B diving seeker): every strike blasts a local crater of HD rifts (dark rift,
  molten body, hot filament, flowing plasma glow, lit rock plates), which then cools. Bolts are HD: tapered, a
  second strand, branches that fork twice.
- CASTER (visual, scale 3): v12's charge, fury flash, nova and sky column; the ground under the user splits into a
  crater of the same rifts.
Engine cut, timings and settings are v11's (see v11/DESIGN.md).
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SKILL = os.environ.get("TNR_ART_SCRIPTS", os.path.join(REPO, "skills", "producing-tnr-art", "scripts"))
sys.path.insert(0, SKILL)
import duelyst_kit as K  # noqa: E402
import fxlight as L  # noqa: E402
import ground_hd as G  # noqa: E402

SS = L.SS
N = 168
C_MS, F_MS, S_MS = 80, 70, 70
RELEASE, F_LEAD, S_LEAD = 5, 6, 8
SETTINGS = {
    "floor": dict(mirror=True, stagger=40, ripple=70, alternate=True),
    "storm": dict(mirror=True, stagger=600, ripple=60, alternate=True),
}
LICENSE = ("CC0 1.0 - OpenDuelyst (open-duelyst/duelyst): fx_f2_eightgates_purpleflame, fx_f4_shadownova, fx_smoke2, "
           "adapted for TNR; light, rifts, rock and glow drawn for TNR")


def blank():
    return Image.new("RGBA", (N, N), (0, 0, 0, 0))


def lead(frs, n):
    return [blank() for _ in range(n)] + frs


# ------------------------------------------------------------------------------------------- noise
def fbm(size, seed):
    rnd_state = random.getstate()
    random.seed(seed)
    out = None
    for s, w in ((5, 0.45), (12, 0.35), (28, 0.2)):
        small = Image.effect_noise((max(2, size[0] // s), max(2, size[1] // s)), 80)
        big = small.resize(size, Image.BICUBIC)
        out = big if out is None else Image.blend(out, big, w)
    random.setstate(rnd_state)
    return out.point(lambda v: max(0, min(255, int((v - 128) * 2.4 + 128))))


NOISE = {}


def plasma(seed, t, W):
    """A crop of a larger noise field, drifting with t: the texture flows instead of strobing."""
    big = NOISE.get(seed)
    if big is None:
        big = NOISE[seed] = fbm((W * 2, W * 2), seed)
    dx, dy = int(t * W * 0.06) % W, int(t * W * 0.025) % W
    return big.crop((dx, dy, dx + W, dy + W))


# ------------------------------------------------------------------------------------------- canvas
class Canvas:
    """core: hot thin light; body: molten fill; matter: what occludes (rift darks, rock, dust)."""

    def __init__(self, n=N):
        self.n, self.W = n, n * SS
        self.core = Image.new("L", (self.W, self.W), 0)
        self.body = Image.new("L", (self.W, self.W), 0)
        self.matter = Image.new("RGBA", (self.W, self.W), (0, 0, 0, 0))
        self.dc, self.db, self.dm = ImageDraw.Draw(self.core), ImageDraw.Draw(self.body), ImageDraw.Draw(self.matter)

    def line(self, pts, w, val, target="core"):
        d = self.dc if target == "core" else self.db
        d.line([(x * SS, y * SS) for x, y in pts], fill=int(max(0, min(255, val))), width=max(1, int(w * SS)),
               joint="curve")

    def tapered(self, pts, w0, w1, v0, v1):
        n = len(pts)
        for i, (p, q) in enumerate(zip(pts, pts[1:])):
            t = i / max(1, n - 2)
            self.dc.line([(p[0] * SS, p[1] * SS), (q[0] * SS, q[1] * SS)], fill=int(max(0, min(255, v0 + (v1 - v0) * t))),
                         width=max(1, int((w0 + (w1 - w0) * t) * SS)))

    def blob(self, cx, cy, rx, ry, val, blur=0.35, target="body"):
        layer = Image.new("L", (self.W, self.W), 0)
        ImageDraw.Draw(layer).ellipse(((cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS),
                                      fill=int(max(0, min(255, val))))
        if blur:
            layer = layer.filter(ImageFilter.GaussianBlur(max(0.5, rx * blur) * SS))
        if target == "body":
            self.body = ImageChops.lighter(self.body, layer)
            self.db = ImageDraw.Draw(self.body)
        else:
            self.core = ImageChops.lighter(self.core, layer)
            self.dc = ImageDraw.Draw(self.core)

    def render(self, noise=None, lut=L.STORM_LUT, gains=(1.2, 2.0, 1.5), cap=1.0, pool_r=13):
        src = ImageChops.lighter(self.core, self.body)
        tight = src.filter(ImageFilter.GaussianBlur(1.6 * SS)).point(lambda v: min(255, int(v * gains[0])))
        mid = src.filter(ImageFilter.GaussianBlur(5 * SS)).point(lambda v: min(255, int(v * gains[1])))
        if noise is not None:
            mid = ImageChops.multiply(mid, noise.point(lambda v: 90 + v * 165 // 255))
        pool = G.squashed_blur(src, pool_r * SS).point(lambda v: min(255, int(v * gains[2])))
        inten = ImageChops.lighter(ImageChops.lighter(self.core, self.body), ImageChops.lighter(tight, ImageChops.lighter(mid, pool)))
        inten = inten.resize((self.n, self.n), Image.LANCZOS)
        if cap < 1:
            inten = inten.point(lambda v: int(v * cap))
        rgb = Image.merge("RGB", [inten.point([c[i] for c in lut]) for i in range(3)])
        alpha = inten.point(lambda v: min(255, int(255 * (v / 255) ** 0.72 * 1.12)))
        light = rgb.convert("RGBA")
        light.putalpha(alpha)
        out = self.matter.resize((self.n, self.n), Image.LANCZOS)
        out.alpha_composite(light)
        return out


# --------------------------------------------------------------------------------------- HD bolt
def hd_bolt(cv, path, rnd, w=3.0, val=255, branches=3, flat=1.0, strand=True, upto=1.0):
    path = path[:max(2, int(round(len(path) * upto)))]
    n = len(path)
    half = n // 2
    cv.tapered(path[:half + 1], w * 0.55, w, val * 0.85, val)
    cv.tapered(path[half:], w, w * 0.6, val, val * 0.9)
    if strand and n > 12:
        i0, i1 = sorted(rnd.sample(range(3, n - 3), 2))
        if i1 - i0 > 6:
            cv.tapered(L.jag(path[i0], path[i1], 0.5, rnd, 4), w * 0.3, w * 0.3, val * 0.7, val * 0.7)
    span = math.hypot(path[-1][0] - path[0][0], path[-1][1] - path[0][1])
    for _ in range(branches):
        if n < 6:
            break
        i = rnd.randrange(2, n - 2)
        p, q = path[i - 1], path[i]
        tang = math.atan2(q[1] - p[1], q[0] - p[0])
        a = tang + rnd.choice((-1, 1)) * rnd.uniform(0.35, 0.9)
        ln = span * rnd.uniform(0.18, 0.35)
        end = (q[0] + math.cos(a) * ln, q[1] + math.sin(a) * ln * flat)
        br = L.jag(q, end, 0.45, rnd, 5)
        cv.tapered(br, w * 0.5, 0.2, val * 0.8, val * 0.15)
        k = rnd.randrange(len(br) // 3, len(br) - 2)
        p2, q2 = br[k - 1], br[k]
        t2 = math.atan2(q2[1] - p2[1], q2[0] - p2[0]) + rnd.choice((-1, 1)) * rnd.uniform(0.4, 0.9)
        cv.tapered(L.jag(q2, (q2[0] + math.cos(t2) * ln * 0.45, q2[1] + math.sin(t2) * ln * 0.45 * flat), 0.5, rnd, 4),
                   w * 0.28, 0.15, val * 0.6, val * 0.1)


# ------------------------------------------------------------------------------------------ rifts
class Crater:
    """A local crater of HD rifts radiating from an impact point, with lit rock plates; opens, then cools."""

    def __init__(self, seed, cx, cy, reach, count=5):
        rnd = random.Random(seed)
        self.cx, self.cy = cx, cy
        self.rifts = []
        base = rnd.uniform(0, 2 * math.pi)
        for k in range(count):
            a = base + k * 2 * math.pi / count + rnd.uniform(-0.35, 0.35)
            ln = reach * rnd.uniform(0.6, 1.0)
            end = (cx + math.cos(a) * ln, cy + math.sin(a) * ln * 0.5)
            path = G.angular((cx, cy), end, rnd, 0.3, 0.07)
            fork = None
            if rnd.random() < 0.7:
                j = rnd.randrange(len(path) // 3, 2 * len(path) // 3)
                fa = a + rnd.choice((-1, 1)) * rnd.uniform(0.4, 0.8)
                fl = ln * rnd.uniform(0.3, 0.5)
                fork = G.angular(path[j], (path[j][0] + math.cos(fa) * fl, path[j][1] + math.sin(fa) * fl * 0.5),
                                 rnd, 0.35, 0.07)
            self.rifts.append((path, fork, rnd.uniform(3.2, 4.6), rnd.uniform(0, 6)))
        self.plates = []
        for path, _, w, _ in self.rifts:
            for k in range(len(path) // 4, len(path), max(4, len(path) // 3)):
                x, y = path[k]
                for sgn in (-1, 1):
                    if rnd.random() < 0.5:
                        continue
                    r = rnd.uniform(3.5, 6.5)
                    poly = L.rock(rnd, x + rnd.uniform(-2, 2), y + sgn * rnd.uniform(4, 7), r)
                    self.plates.append((poly, sgn))

    def draw(self, cv, grow, heat, plates=True, fade=1.0):
        for path, fork, w, ph in self.rifts:
            for pts, base in ((path, w), (fork, w * 0.6)):
                if not pts:
                    continue
                m = max(2, int(round(len(pts) * grow)))
                pts = pts[:m]
                ws = []
                for k in range(len(pts)):
                    u = k / max(1, len(pts) - 1)
                    ws.append(base * (1 - 0.8 * u) * (0.7 + 0.3 * abs(math.sin(u * 9 + ph))))
                cv.dm.polygon(G.fissure_poly(pts, [x * 2.3 for x in ws]), fill=(12, 5, 20, int(170 * min(1, grow + 0.3) * fade)))
                cv.db.polygon(G.fissure_poly(pts, ws), fill=int(150 * heat))
                cv.tapered(pts, base * 0.24, 0.3, 255 * heat, 160 * heat)
        if plates and grow > 0.5:
            for poly, sgn in self.plates:
                P = [(a * SS, b * SS) for a, b in poly]
                cv.dm.polygon(P, fill=(30, 22, 40, int(175 * fade)))
                rim = sorted(P, key=lambda p: -sgn * p[1])[:3]
                cv.dm.line(sorted(rim), fill=(200, 150, 255, int(235 * max(0.3, heat) * fade)), width=int(1.4 * SS),
                           joint="curve")


# ------------------------------------------------------------------------------------------ dust
_DUST = None


def dust(cv, cx, cy, t, width):
    global _DUST
    if _DUST is None:
        src = K.squared(K.frames("fx_smoke2"))
        _DUST = []
        for f in src:
            g = ImageOps.grayscale(f.convert("RGB"))
            im = Image.merge("RGB", [g.point(lambda v, c=c: int(c * (0.45 + 0.55 * v / 255))) for c in (96, 78, 128)])
            im = im.convert("RGBA")
            im.putalpha(f.getchannel("A").point(lambda a: int(a * 0.45)))
            _DUST.append(im)
    if 0 <= t < 4:
        d = _DUST[t].resize((int(width * SS), int(width * SS)), Image.LANCZOS)
        cv.matter.alpha_composite(d, (int((cx - width / 2) * SS), int((cy - width * 0.62) * SS)))


# ------------------------------------------------------------------------------------------ floor
def floor_frames(seed):
    """A charged glow filling the hex edge to edge (feathered past the edge so tiles join), plasma drifting through
    it, and HD lightning crawling over the ground in new shapes every couple of frames."""
    h = N / 2
    c = N / 2
    hexp = G.hex_pts(c, c, h)
    rnd = random.Random(seed)
    W = N * SS
    fill = Image.new("L", (W, W), 0)
    ImageDraw.Draw(fill).polygon([(x * SS, y * SS) for x, y in G.hex_pts(c, c, h * 0.96)], fill=255)
    fill = fill.filter(ImageFilter.GaussianBlur(3 * SS))

    def pt():
        while True:
            p = (c + rnd.uniform(-0.9, 0.9) * h, c + rnd.uniform(-0.45, 0.45) * h)
            if G.inside(p, c, c, h, 0.95):
                return p

    def arc():
        a = pt()
        for _ in range(40):
            b = pt()
            if 0.7 * h < math.hypot(b[0] - a[0], (b[1] - a[1]) * 2) < 1.6 * h:
                break
        lift = rnd.uniform(2, 7)
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - lift)
        path = L.jag(a, m, 0.38, rnd, 5) + L.jag(m, b, 0.38, rnd, 5)[1:]
        return [path, rnd.randrange(1 << 30), 2]

    plan = [  # (veil, glow, arc heat, new arcs)
        (0.14, 0.0, 0.0, 0), (0.06, 0.08, 0.6, 1), (0, 0.13, 0.9, 1), (0, 0.16, 1.0, 1), (0, 0.17, 1.0, 2),
        (0, 0.16, 0.95, 1), (0, 0.17, 0.95, 1), (0, 0.16, 0.9, 2), (0, 0.14, 0.85, 1), (0, 0.13, 0.75, 1),
        (0, 0.11, 0.65, 1), (0, 0.09, 0.55, 0), (0, 0.07, 0.4, 0), (0, 0.05, 0.3, 0), (0, 0.03, 0.0, 0),
        (0, 0.01, 0.0, 0)]
    live = []
    out = []
    for t, (veil, glow, heat, new) in enumerate(plan):
        cv = Canvas()
        g = max(veil, glow)
        if g:
            tex = plasma(seed, t, W)
            layer = ImageChops.multiply(fill.point(lambda v, g=g: int(v * g)), tex.point(lambda v: 110 + v * 145 // 255))
            cv.body = ImageChops.lighter(cv.body, layer)
            cv.db = ImageDraw.Draw(cv.body)
        live = [a for a in live if a[2] > 0]
        for _ in range(new):
            live.append(arc())
        for a in live:
            r = random.Random(a[1] + a[2])
            hd_bolt(cv, L.wobble(a[0], r, 0.6), r, w=1.9 if a[2] == 2 else 1.4, val=230 * heat, branches=2, flat=0.6)
            a[2] -= 1
        out.append(cv.render(plasma(seed + 1, t, W) if g else None, gains=(1.1, 1.6, 1.3), cap=0.9))
    return out


# ------------------------------------------------------------------------------------------ storm
SH = N / 3
SC = N / 2


def storm_eruption(seed=61):
    rnd = random.Random(seed)
    W = N * SS
    crater = Crater(seed, SC, SC + 2, 34)
    main = L.jag((SC, SC), (SC + 18, 2), 0.3, rnd, 6)
    sister = L.jag((SC - 16, SC + 1), (SC - 30, SC - 40), 0.38, rnd, 5)
    out = []
    plan = [("antic", 0), ("antic", 1), ("erupt", 0), ("erupt", 1), ("erupt", 2), ("crackle", 0), ("crackle", 1),
            ("crackle", 2), ("cool", 0), ("cool", 1), ("cool", 2)]
    for t, (beat, k) in enumerate(plan):
        cv = Canvas()
        r = random.Random(seed * 13 + t)
        if beat == "antic":
            crater.draw(cv, 0.25 + 0.2 * k, 0.8, plates=False)
            cv.blob(SC, SC, 12 + 6 * k, 5 + 3 * k, 120 + 50 * k)
            hd_bolt(cv, main[: len(main) // (5 - 2 * k)], r, w=1.8, val=200, branches=0, strand=False)
        elif beat == "erupt":
            dust(cv, SC, SC, k, 96)
            L.debris(_Shim(cv), seed, (SC, SC - 2), k + 1)
            crater.draw(cv, 0.75 + 0.25 * k, 1.0)
            cv.blob(SC, SC, 26 - 4 * k, 11 - 2 * k, 190 - 40 * k)
            cv.blob(SC, SC, 6 - k, 3 - 0.4 * k, 255, 0.25, target="core")
            hd_bolt(cv, L.wobble(main, r, 0.6), r, w=5.0 if k == 0 else 3.6, val=255, branches=3,
                    upto=min(1, 0.6 + 0.4 * k))
            if k:
                hd_bolt(cv, L.wobble(sister, r, 0.6), r, w=2.4, val=225, branches=2)
            L.sparks(_Shim(cv), seed, (SC, SC), k + 1)
        elif beat == "crackle":
            dust(cv, SC, SC, k + 3, 96)
            L.debris(_Shim(cv), seed, (SC, SC - 2), k + 4)
            crater.draw(cv, 1.0, 0.9 - 0.12 * k)
            if k != 1:
                hd_bolt(cv, L.wobble(main, r, 0.9), r, w=2.4, val=200 - 60 * k, branches=1)
            L.sparks(_Shim(cv), seed, (SC, SC), k + 4)
        else:
            crater.draw(cv, 1.0, 0.5 - 0.17 * k, fade=0.7 - 0.3 * k)
            for _ in range(5):
                x, y = SC + r.uniform(-12, 12), SC - r.uniform(4, 20) - 4 * k
                cv.blob(x, y, 1.3, 1.3, 220 - 70 * k, 0.3, target="core")
        out.append(cv.render(plasma(seed, t, W)))
    return out


def storm_seeker(seed=83):
    rnd = random.Random(seed)
    W = N * SS
    crater = Crater(seed, SC, SC, 38, count=6)
    top = (SC - 58, 0)
    path = L.jag(top, (SC, SC), 0.3, rnd, 6)
    out = []
    plan = [("mark", 0), ("mark", 1), ("strike", 0), ("strike", 1), ("strike", 2), ("crackle", 0), ("crackle", 1),
            ("crackle", 2), ("cool", 0), ("cool", 1), ("cool", 2)]
    for t, (beat, k) in enumerate(plan):
        cv = Canvas()
        r = random.Random(seed * 17 + t)
        if beat == "mark":
            rr = 24 - 9 * k
            cv.dc.ellipse(((SC - rr) * SS, (SC - rr * 0.45) * SS, (SC + rr) * SS, (SC + rr * 0.45) * SS),
                          outline=110 + 40 * k, width=int(0.8 * SS))
            hd_bolt(cv, path[: int(len(path) * (0.35 + 0.3 * k))], r, w=1.4, val=180, branches=1, strand=False)
        elif beat == "strike":
            dust(cv, SC, SC, k, 108)
            L.debris(_Shim(cv), seed, (SC, SC - 2), k + 1, n=7)
            crater.draw(cv, min(1, 0.6 + 0.3 * k), 1.0)
            cv.blob(SC, SC, 30 - 5 * k, 13 - 2 * k, 200 - 50 * k)
            cv.blob(SC, SC, 7 - 2 * k, 3.5 - k, 255, 0.25, target="core")
            hd_bolt(cv, L.wobble(path, r, 0.5), r, w=4.4 if k == 0 else 3.2, val=255, branches=3)
            L.sparks(_Shim(cv), seed, (SC, SC), k + 1, n=10)
        elif beat == "crackle":
            dust(cv, SC, SC, k + 3, 108)
            L.debris(_Shim(cv), seed, (SC, SC - 2), k + 4, n=7)
            crater.draw(cv, 1.0, 0.85 - 0.12 * k)
            if k == 0:
                hd_bolt(cv, L.wobble(path, r, 0.8), r, w=2.0, val=170, branches=1)
            L.sparks(_Shim(cv), seed, (SC, SC), k + 4, n=10)
        else:
            crater.draw(cv, 1.0, 0.5 - 0.17 * k, fade=0.7 - 0.3 * k)
            for _ in range(6):
                a = r.uniform(0, 2 * math.pi)
                cv.blob(SC + math.cos(a) * 10, SC + math.sin(a) * 4 - 4 * k - 2, 1.3, 1.3, 220 - 70 * k, 0.3,
                        target="core")
        out.append(cv.render(plasma(seed, t, W)))
    return out


class _Shim:
    """Lets fxlight's debris/sparks helpers draw into a Canvas (they expect a fxlight.Frame)."""

    def __init__(self, cv):
        self.cv = cv

    def poly_matter(self, pts, fill, rim=None):
        P = [(x * SS, y * SS) for x, y in pts]
        self.cv.dm.polygon(P, fill=fill)
        if rim:
            top = sorted(P, key=lambda p: p[1])[:max(2, len(P) // 2)]
            self.cv.dm.line(sorted(top), fill=rim, width=max(1, SS))

    def stroke(self, pts, w0, w1, val=255, upto=1.0):
        self.cv.tapered(pts, w0, w1, val, val)


# ----------------------------------------------------------------------------------------- caster
def caster_frames():
    rnd = random.Random(7)
    body = (SC, SC - 0.4 * SH)
    feet = (SC, SC + 0.4 * SH)
    src = K.squared(K.frames("fx_f2_eightgates_purpleflame"))
    top, base_row = 3, 169
    k = 1.7 * SH / (base_row - top)
    s = int(round(src[0].width * k))
    pillar = []
    for f in src:
        cvp = blank()
        g = f.resize((s, s), Image.LANCZOS)
        cvp.paste(g, (int(N / 2 - s / 2), int(feet[1] - base_row * k)), g)
        pillar.append(cvp)
    seq = [2, 4, 6, 8, 10] + list(range(23, 31))
    nsrc = K.squared(K.frames("fx_f4_shadownova"))
    nk = N / nsrc[0].width
    nova = []
    for i in list(range(0, 12)) + [13, 15]:
        f = nsrc[i].resize((N, N), Image.LANCZOS)
        cvn = blank()
        cvn.paste(f, (0, int(round(body[1] - 98 * nk))), f)
        nova.append(cvn)
    crater = Crater(5, SC, feet[1] - 2, 40, count=6)
    crawl = [L.jag((body[0] + rnd.uniform(-8, 8), body[1] + rnd.uniform(-20, 14)),
                   (body[0] + rnd.uniform(-10, 10), body[1] + rnd.uniform(-20, 20)), 0.5, rnd, 5) for _ in range(6)]
    bites = [L.jag((body[0], body[1] + 10), (feet[0] + sgn * rnd.uniform(12, 26), feet[1] + rnd.uniform(-3, 3)), 0.45,
                   rnd, 5) for sgn in (-1, 1, -1, 1)]
    column = [L.jag((body[0] + dx, body[1] - 4), (body[0] + dx * 2.2 + rnd.uniform(-6, 6), -6), 0.28, rnd, 6)
              for dx in (-3, 0, 4)]
    W = N * SS
    n = RELEASE + len(nova)
    out = []
    for t in range(n):
        cv = Canvas()
        r = random.Random(70 + t)
        if t < RELEASE:
            for c in crawl[: 2 + t]:
                hd_bolt(cv, L.wobble(c, r, 0.8), r, w=1.5, val=175 + 15 * t, branches=1, strand=False)
            for b in bites[: max(0, t - 1)]:
                hd_bolt(cv, L.wobble(b, r, 0.6), r, w=1.7, val=210, branches=1, strand=False)
            cv.blob(body[0], body[1], 14 + 2 * t, 18 + 2 * t, 50 + 18 * t)
            if t >= 2:
                crater.draw(cv, 0.1 + 0.12 * t, 0.8, plates=False)
        else:
            j = t - RELEASE
            if j < 2:
                cv.blob(body[0], body[1], 40 - 10 * j, 34 - 8 * j, 255 - 70 * j, 0.45, target="core")
                cv.blob(body[0], body[1], 14, 14, 255, 0.2, target="core")
            if j < 7:
                for c in column[: 3 if j < 4 else 1]:
                    hd_bolt(cv, L.wobble(c, r, 0.6), r, w=4.0 if j < 2 else 2.4, val=255 - 25 * j, branches=2,
                            upto=min(1, 0.55 + 0.45 * j))
            crater.draw(cv, min(1, 0.6 + 0.2 * j), max(0.2, 1 - 0.08 * j))
        light = cv.render(plasma(5, t, W))
        frame = blank()
        if t < len(seq):
            frame.alpha_composite(pillar[seq[t]])
        if t >= RELEASE:
            frame.alpha_composite(nova[t - RELEASE])
        frame.alpha_composite(light)
        out.append(frame)
    return out


def clips():
    return {
        "caster": (caster_frames(), C_MS, 3),
        "floor_a": (lead(floor_frames(11), F_LEAD), F_MS, 2),
        "floor_b": (lead(floor_frames(29), F_LEAD), F_MS, 2),
        "storm_a": (lead(storm_eruption(), S_LEAD), S_MS, 3),
        "storm_b": (lead(storm_seeker(), S_LEAD), S_MS, 3),
    }


def main():
    cs = clips()
    for cid, (frs, ms, scale) in cs.items():
        px = frs[0].width
        assert px * len(frs) <= 4096, (cid, px, len(frs))
        fn = os.path.join(HERE, f"anim_fcf_v13_{cid}_{px}.webp")
        b = K.write_strip(frs, fn, px)
        assert b <= 460800, (cid, b)
        print(f"{os.path.basename(fn)}: {len(frs)} frames x {ms} ms, scale {scale}, {px} px "
              f"({px * len(frs)} px tall), {b} bytes")
    return cs


if __name__ == "__main__":
    main()
