#!/usr/bin/env python3
"""Forbidden Chakra Fury v12: the v11 move (v11/DESIGN.md) redrawn light-first (fxlight.py) (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v12/build_v12.py [--stills]

Same engine cut and timing as v11; what changed is how every element is drawn:
- light is drawn as a tapered greyscale intensity at 4x, bloomed, and mapped through the icon's ramp (violet ->
  lilac-pink -> white), then reduced to 168 px: no outlines, no stair-steps;
- each bolt keeps one shape per beat and only shimmers, grows, flashes and fades;
- a brightness budget: the floor never reaches white, the storm whites only at its strike points, the caster burst is
  the one full-white moment;
- matter (scorch, rock with a lit rim, recoloured Duelyst dust) is drawn separately under the light.
"""
import math
import os
import random
import sys

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SKILL = os.environ.get("TNR_ART_SCRIPTS", os.path.join(REPO, "skills", "producing-tnr-art", "scripts"))
sys.path.insert(0, SKILL)
import duelyst_kit as K  # noqa: E402
import fxlight as L  # noqa: E402

N = 168
C_MS, F_MS, S_MS = 80, 70, 70
RELEASE, F_LEAD, S_LEAD = 5, 6, 8
SETTINGS = {
    "floor": dict(mirror=True, stagger=40, ripple=70),
    "storm": dict(mirror=True, stagger=600, ripple=60, alternate=True),
}
LICENSE = ("CC0 1.0 - OpenDuelyst (open-duelyst/duelyst): fx_f2_eightgates_purpleflame, fx_f4_shadownova, fx_smoke2, "
           "adapted for TNR; light, cracks, rock and glow drawn for TNR")


def blank():
    return Image.new("RGBA", (N, N), (0, 0, 0, 0))


def lead(frs, n):
    return [blank() for _ in range(n)] + frs


# ------------------------------------------------------------------------------------------------ dust
def dust_frames():
    """fx_smoke2 (a flat impact dust ring), recoloured to violet-grey and softened."""
    src = K.squared(K.frames("fx_smoke2"))
    out = []
    for f in src:
        g = ImageOps.grayscale(f.convert("RGB"))
        tint = Image.merge("RGB", [g.point(lambda v, c=c: int(c * (0.45 + 0.55 * v / 255))) for c in (96, 78, 128)])
        im = tint.convert("RGBA")
        im.putalpha(f.getchannel("A").point(lambda a: int(a * 0.45)))
        out.append(im)
    return out


DUST = None


def dust(fr, cx, cy, t, width):
    global DUST
    if DUST is None:
        DUST = dust_frames()
    if 0 <= t < min(4, len(DUST)):
        d = DUST[t].resize((int(width), int(width)), Image.LANCZOS)
        fr.paste_matter(d, (cx - width / 2, cy - width * 0.62))


# ----------------------------------------------------------------------------------------------- floor
def hex_pts(cx, cy, h):
    w = 2 * h
    return [(cx - w / 2, cy), (cx - w / 4, cy - h / 2), (cx + w / 4, cy - h / 2), (cx + w / 2, cy),
            (cx + w / 4, cy + h / 2), (cx - w / 4, cy + h / 2)]


def crack_web(seed, cx, cy, h):
    """Cracks from all six edge midpoints in to two or three inner nodes (so they meet the neighbours'), plus spurs.
    Each crack carries a width taper: thick where it enters, thin inside."""
    rnd = random.Random(seed)
    p = hex_pts(cx, cy, h)
    mids = [((p[i][0] + p[(i + 1) % 6][0]) / 2, (p[i][1] + p[(i + 1) % 6][1]) / 2) for i in range(6)]
    nodes = [(cx + rnd.uniform(-0.25, 0.25) * h, cy + rnd.uniform(-0.1, 0.1) * h) for _ in range(rnd.choice((2, 3)))]
    main = []
    for m in mids:
        n = min(nodes, key=lambda q: math.hypot(q[0] - m[0], (q[1] - m[1]) * 2) + rnd.uniform(0, 0.15 * h))
        main.append(L.jag(m, n, 0.45, rnd, 4))
    links = [L.jag(a, b, 0.5, rnd, 3) for a, b in zip(nodes, nodes[1:])]
    spurs = []
    for _ in range(6):
        path = rnd.choice(main)
        q = path[rnd.randrange(2, len(path) - 2)]
        a = rnd.uniform(0, 2 * math.pi)
        ln = rnd.uniform(0.08, 0.18) * h * 2
        spurs.append(L.jag(q, (q[0] + math.cos(a) * ln, q[1] + math.sin(a) * ln * 0.5), 0.5, rnd, 3))
    return main, links, spurs


def floor_frames(seed):
    h = N / 2                               # scale 2: the clip is two tile heights; the hex spans its width
    c = N / 2
    hexp = hex_pts(c, c, h)
    main, links, spurs = crack_web(seed, c, c, h)
    rnd = random.Random(seed + 7)
    # (beat, value): band = the shockwave crossing; crack = splitting in from the edges; glow = hot; cool = fading
    plan = [("band", 0.13), ("band", 0.05), ("crack", 0.4), ("crack", 0.75), ("crack", 1.0), ("glow", 1.0),
            ("glow", 0.82), ("glow", 0.94), ("glow", 0.78), ("glow", 0.7), ("cool", 0.6), ("cool", 0.48),
            ("cool", 0.36), ("cool", 0.25), ("cool", 0.14), ("cool", 0.05)]
    out = []
    for i, (beat, v) in enumerate(plan):
        fr = L.Frame(N)
        if beat == "band":
            # the shockwave: flat light filling the hex edge to edge, so neighbours join into one band
            fr.dl.polygon([(x * L.SS, y * L.SS) for x, y in hexp], fill=int(255 * v))
        else:
            # depth: a dark seam under each crack (no hex-shaped fill, so fading tiles leave no patchwork)
            grow0 = v if beat == "crack" else 1.0
            seam = Image.new("L", (fr.W, fr.W), 0)
            from PIL import ImageDraw as _D, ImageFilter as _F
            sd = _D.Draw(seam)
            for p in main:
                q = p[:max(2, int(round(len(p) * grow0)))]
                sd.line([(x * L.SS, y * L.SS) for x, y in q], fill=255, width=int(4.5 * L.SS))
            a = {"crack": 120, "glow": 130, "cool": int(130 * v)}[beat]
            seam = seam.filter(_F.GaussianBlur(2.2 * L.SS)).point(lambda n, a=a: n * a // 255)
            dark = Image.new("RGBA", (fr.W, fr.W), (14, 6, 24, 0))
            dark.putalpha(seam)
            fr.matter.alpha_composite(dark)
            grow = v if beat == "crack" else 1.0
            heat = {"crack": 1.0, "glow": v, "cool": v}[beat]
            for p in main:
                fr.stroke(p, 2.4, 0.8, 255 * heat, upto=grow)
            if beat != "crack" or v >= 1.0:
                for p in links:
                    fr.stroke(p, 1.4, 1.0, 220 * heat)
                for p in spurs:
                    fr.stroke(p, 1.0, 0.3, 200 * heat)
            if beat == "glow" and i % 2:
                for _ in range(4):
                    p = rnd.choice(main)
                    x, y = p[rnd.randrange(len(p))]
                    fr.blob(x, y, 2.2, 1.6, 255, 0.4)
        # the band is a flat wash (no bloom, so it stays a thin veil); the cracks bloom
        out.append(fr.render(L.FLOOR_LUT, bloom=() if beat == "band" else ((1.2, 0.7), (4, 0.4)), cap=0.92))
    return out


# ----------------------------------------------------------------------------------------------- storm
SH = N / 3                                  # tile height at scale 3
SC = N / 2                                  # ground point


def storm_eruption(seed=61):
    """A: a leaning pillar of lightning tears up out of the cracks with a sister bolt; rock and dust thrown up."""
    rnd = random.Random(seed)
    g = (SC, SC)
    main = L.jag(g, (SC + 18, 2), 0.32, rnd, 6)
    sister_root = (SC - 20, SC + 2)
    sister = L.jag(sister_root, (SC - 34, SC - 38), 0.4, rnd, 5)
    branches = []
    for _ in range(4):
        i = rnd.randrange(len(main) // 4, len(main) - 4)
        p = main[i]
        a = rnd.uniform(-2.6, -0.5)
        ln = rnd.uniform(10, 20)
        branches.append(L.jag(p, (p[0] + math.cos(a) * ln * rnd.choice((-1, 1)), p[1] + math.sin(a) * ln), 0.5, rnd, 4))
    out = []
    for t in range(2):                                   # anticipation: the cracks under it flare and a spark climbs
        fr = L.Frame(N)
        fr.blob(SC, SC, 14 + 6 * t, 6 + 3 * t, 120 + 60 * t)
        fr.stroke(main[: len(main) // (6 - 2 * t)], 1.8, 0.8, 200)
        out.append(fr.render())
    for t in range(3):                                   # eruption
        fr = L.Frame(N)
        dust(fr, SC, SC, t, 92)
        L.debris(fr, seed, (SC, SC - 2), t + 1)
        fr.blob(SC, SC, 26 - 4 * t, 11 - 2 * t, 200 - 40 * t)
        fr.blob(SC, SC, 7 - t, 3.5 - 0.5 * t, 255, 0.25)
        fr.stroke(L.wobble(main, rnd, 0.6), 5.0 if t == 0 else 3.6, 0.9, 255, upto=min(1, 0.6 + 0.4 * t))
        for b in branches:
            fr.stroke(L.wobble(b, rnd, 0.5), 1.8, 0.3, 230)
        if t:
            fr.stroke(L.wobble(sister, rnd, 0.6), 2.4, 0.5, 220)
        L.sparks(fr, seed, (SC, SC), t + 1)
        out.append(fr.render())
    for t in range(3):                                   # crackle: the pillar flickers out, rock falls, dust spreads
        fr = L.Frame(N)
        dust(fr, SC, SC, t + 3, 92)
        L.debris(fr, seed, (SC, SC - 2), t + 4)
        fr.blob(SC, SC, 18, 8, 110 - 30 * t)
        if t != 1:
            fr.stroke(L.wobble(main, rnd, 0.9), 2.4, 0.6, 200 - 60 * t)
        for b in branches[: 2 - t // 2]:
            fr.stroke(L.wobble(b, rnd, 0.7), 1.2, 0.3, 150)
        L.sparks(fr, seed, (SC, SC), t + 4)
        out.append(fr.render())
    for t in range(3):                                   # embers drift up and die
        fr = L.Frame(N)
        dust(fr, SC, SC, t + 6, 92)
        er = random.Random(seed + 3)
        for _ in range(6):
            x, y = SC + er.uniform(-10, 10), SC - er.uniform(4, 20) - 4 * t
            fr.blob(x, y, 1.4, 1.4, 220 - 70 * t, 0.3)
        out.append(fr.render())
    return out


def storm_seeker(seed=83):
    """B: a seeking bolt dives in on a slant from the sky: a target mark tightens, the strike, ground arcs, rock."""
    rnd = random.Random(seed)
    top = (SC - 58, 0)
    path = L.jag(top, (SC, SC), 0.3, rnd, 6)
    branches = []
    for _ in range(3):
        i = rnd.randrange(len(path) // 3, len(path) - 6)
        p = path[i]
        a = rnd.uniform(0.2, 1.4)
        ln = rnd.uniform(10, 18)
        branches.append(L.jag(p, (p[0] + math.cos(a) * ln, p[1] + math.sin(a) * ln), 0.5, rnd, 4))
    arcs = []
    for k in range(5):
        a = k * 2 * math.pi / 5 + rnd.uniform(-0.4, 0.4)
        arcs.append(L.jag((SC, SC), (SC + math.cos(a) * 34, SC + math.sin(a) * 15), 0.55, rnd, 4))
    out = []
    for t in range(2):                                   # the mark tightens; the leader comes down
        fr = L.Frame(N)
        r = 24 - 9 * t
        fr.ring(SC, SC, r, r * 0.45, 1.2, 170 + 50 * t)
        fr.stroke(path[: int(len(path) * (0.35 + 0.3 * t))], 0.6, 1.4, 170)
        out.append(fr.render())
    for t in range(3):                                   # strike
        fr = L.Frame(N)
        dust(fr, SC, SC, t, 104)
        L.debris(fr, seed, (SC, SC - 2), t + 1, n=7)
        fr.blob(SC, SC, 30 - 5 * t, 13 - 2 * t, 210 - 50 * t)
        fr.blob(SC, SC, 8 - 2 * t, 4 - t, 255, 0.25)
        fr.stroke(L.wobble(path, rnd, 0.5), 1.0, 4.4 if t == 0 else 3.2, 255)
        for b in branches:
            fr.stroke(L.wobble(b, rnd, 0.5), 1.6, 0.3, 220)
        for a in arcs:
            fr.stroke(L.wobble(a, rnd, 0.6), 2.0, 0.3, 230, upto=min(1, 0.5 + 0.35 * t))
        L.sparks(fr, seed, (SC, SC), t + 1, n=10)
        out.append(fr.render())
    for t in range(3):                                   # ground arcs crawl, rock falls, dust spreads
        fr = L.Frame(N)
        dust(fr, SC, SC, t + 3, 104)
        L.debris(fr, seed, (SC, SC - 2), t + 4, n=7)
        fr.blob(SC, SC, 20, 9, 100 - 30 * t)
        if t == 0:
            fr.stroke(L.wobble(path, rnd, 0.8), 0.6, 2.0, 170)
        for k, a in enumerate(arcs):
            if (k + t) % 2 == 0:
                fr.stroke(L.wobble(a, rnd, 0.9), 1.5, 0.3, 190 - 50 * t)
        L.sparks(fr, seed, (SC, SC), t + 4, n=10)
        out.append(fr.render())
    for t in range(3):
        fr = L.Frame(N)
        dust(fr, SC, SC, t + 6, 104)
        er = random.Random(seed + 5)
        for _ in range(6):
            a = er.uniform(0, 2 * math.pi)
            fr.blob(SC + math.cos(a) * 10, SC + math.sin(a) * 4 - 4 * t - 2, 1.4, 1.4, 220 - 70 * t, 0.3)
        out.append(fr.render())
    return out


# ---------------------------------------------------------------------------------------------- caster
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
        cv = blank()
        g = f.resize((s, s), Image.LANCZOS)
        cv.paste(g, (int(N / 2 - s / 2), int(feet[1] - base_row * k)), g)
        pillar.append(cv)
    seq = [2, 4, 6, 8, 10] + list(range(23, 31))
    nsrc = K.squared(K.frames("fx_f4_shadownova"))
    nk = N / nsrc[0].width
    nova = []
    for i in list(range(0, 12)) + [13, 15]:
        f = nsrc[i].resize((N, N), Image.LANCZOS)
        cv = blank()
        cv.paste(f, (0, int(round(body[1] - 98 * nk))), f)
        nova.append(cv)
    main, links, spurs = crack_web(5, SC, SC, SH)
    crawl = [L.jag((body[0] + rnd.uniform(-8, 8), body[1] + rnd.uniform(-20, 14)),
                   (body[0] + rnd.uniform(-10, 10), body[1] + rnd.uniform(-20, 20)), 0.5, rnd, 4) for _ in range(6)]
    bites = [L.jag((body[0], body[1] + 10), (feet[0] + sgn * rnd.uniform(12, 26), feet[1] + rnd.uniform(-3, 3)), 0.45,
                   rnd, 4) for sgn in (-1, 1, -1, 1)]
    column = [L.jag((body[0] + dx, body[1] - 4), (body[0] + dx * 2.2 + rnd.uniform(-6, 6), -6), 0.28, rnd, 6)
              for dx in (-3, 0, 4)]
    n = RELEASE + len(nova)
    out = []
    for t in range(n):
        fr = L.Frame(N)
        if t < RELEASE:                                   # charge: crawl over the body, bites into the ground
            for c in crawl[: 2 + t]:
                fr.stroke(L.wobble(c, rnd, 0.8), 1.6, 0.5, 170 + 15 * t)
            for b in bites[: max(0, t - 1)]:
                fr.stroke(L.wobble(b, rnd, 0.6), 1.8, 0.4, 210)
            fr.blob(body[0], body[1], 14 + 2 * t, 18 + 2 * t, 50 + 18 * t)
            for p in main:
                fr.stroke(p, 1.6, 0.6, 140, upto=0.15 + 0.12 * t)
        else:
            j = t - RELEASE
            if j < 2:                                     # the fury: the one full-white moment
                fr.blob(body[0], body[1], 40 - 10 * j, 34 - 8 * j, 255 - 70 * j, 0.45)
                fr.blob(body[0], body[1], 14, 14, 255, 0.2)
            if j < 7:                                     # the sky column
                for c in column[: 3 if j < 4 else 1]:
                    fr.stroke(L.wobble(c, rnd, 0.6), 4.0 if j < 2 else 2.4, 0.8, 255 - 25 * j,
                              upto=min(1, 0.55 + 0.45 * j))
            heat = max(0.2, 1 - 0.08 * j)
            for p in main:
                fr.stroke(p, 2.0, 0.7, 230 * heat)
            for p in links + spurs:
                fr.stroke(p, 1.0, 0.3, 190 * heat)
        light = fr.render()
        cv = blank()
        if t < len(seq):
            cv.alpha_composite(pillar[seq[t]])
        if t >= RELEASE:
            cv.alpha_composite(nova[t - RELEASE])
        cv.alpha_composite(light)
        out.append(cv)
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
        fn = os.path.join(HERE, f"anim_fcf_v12_{cid}_{px}.webp")
        b = K.write_strip(frs, fn, px)
        print(f"{os.path.basename(fn)}: {len(frs)} frames x {ms} ms, scale {scale}, {px} px "
              f"({px * len(frs)} px tall), {b} bytes")
    return cs


if __name__ == "__main__":
    main()
