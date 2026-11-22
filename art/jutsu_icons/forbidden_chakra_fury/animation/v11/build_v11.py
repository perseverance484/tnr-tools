#!/usr/bin/env python3
"""Forbidden Chakra Fury v11: the whole move designed first (DESIGN.md), then cut into engine clips (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v11/build_v11.py

Clips (one drawn pixel = h/28 on the board everywhere):
  caster    visual, scale 3, 80 ms   charge, fury burst (v7 nova), sky column, cracks on the caster's tile
  floor_a/b recoil, scale 2, 70 ms   shockwave band, then a cracked floor that joins across every hex edge
  storm_a/b damage, scale 3, 70 ms   eruption out of the cracks / seeking bolt from the sky with rubble
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SKILL = os.environ.get("TNR_ART_SCRIPTS", os.path.join(REPO, "skills", "producing-tnr-art", "scripts"))
sys.path.insert(0, SKILL)
import duelyst_kit as K  # noqa: E402

DEEP = (92, 24, 186)
VIO = (160, 84, 255)
LIL = (204, 160, 255)
HOT = (246, 236, 255)
ROCK = (34, 26, 48)
ROCK_RIM = (120, 70, 210)
LICENSE = ("CC0 1.0 - OpenDuelyst (open-duelyst/duelyst): fx_f2_eightgates_purpleflame, fx_f4_shadownova, adapted "
           "for TNR; floor, cracks, lightning and rubble drawn for TNR")

C_MS, F_MS, S_MS = 80, 70, 70
RELEASE = 5          # caster frame of the fury burst (400 ms)
F_LEAD = 6           # floor waits to 420 ms, then ripples out
S_LEAD = 8           # storm waits to 560 ms, then scatters
H = 28               # tile height in drawn px, every clip


# ---------------------------------------------------------------------------------------------- drawing kit
def jag(a, b, amp, rnd, depth=4):
    pts = [a, b]
    for d in range(depth):
        out = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
            dx, dy = q[0] - p[0], q[1] - p[1]
            ln = math.hypot(dx, dy) or 1
            off = rnd.uniform(-1, 1) * amp * ln / (1.7 ** d) / 2
            out += [(mx - dy / ln * off, my + dx / ln * off), q]
        pts = out
    return [(round(x), round(y)) for x, y in pts]


def bolt(im, pts, heat=1.0, thick=1, branches=0, rnd=None, upto=1.0):
    """Layered lightning. heat 1 = white core; falls toward violet then dim as it cools."""
    n = max(2, int(round(len(pts) * upto)))
    pts = pts[:n]
    d = ImageDraw.Draw(im)
    a = max(0.0, min(1.0, heat))
    d.line(pts, fill=DEEP + (int(110 * a),), width=3 + 2 * thick)
    d.line(pts, fill=VIO + (int(255 * a),), width=1 + 2 * thick)
    core = HOT if heat > 0.7 else (LIL if heat > 0.35 else VIO)
    d.line(pts, fill=core + (int(255 * a),), width=thick)
    for _ in range(branches):
        i = rnd.randrange(1, max(2, len(pts) - 1))
        p = pts[i]
        ang = rnd.uniform(0, 2 * math.pi)
        ln = rnd.uniform(4, 9)
        br = jag(p, (p[0] + math.cos(ang) * ln, p[1] + math.sin(ang) * ln * 0.7), 0.6, rnd, 2)
        d.line(br, fill=DEEP + (int(90 * a),), width=3)
        d.line(br, fill=(LIL if heat > 0.6 else VIO) + (int(230 * a),), width=1)


def hex_pts(cx, cy, h):
    w = 2 * h
    return [(cx - w / 2, cy), (cx - w / 4, cy - h / 2), (cx + w / 4, cy - h / 2), (cx + w / 2, cy),
            (cx + w / 4, cy + h / 2), (cx - w / 4, cy + h / 2)]


def edge_mids(cx, cy, h):
    p = hex_pts(cx, cy, h)
    return [((p[i][0] + p[(i + 1) % 6][0]) / 2, (p[i][1] + p[(i + 1) % 6][1]) / 2) for i in range(6)]


def blank(n):
    return Image.new("RGBA", (n, n), (0, 0, 0, 0))


def up(frs, k):
    return [f.resize((f.width * k, f.height * k), Image.NEAREST) for f in frs]


def lead(frs, n):
    return [blank(frs[0].width) for _ in range(n)] + frs


# ----------------------------------------------------------------------------------------------- floor
FL = 56              # scale 2: 56 drawn px = 2 tile heights; the hex is exactly 56 wide


def crack_web(seed, cx, cy, h):
    """Crack polylines that reach all six edge midpoints through two or three inner nodes, plus spurs."""
    rnd = random.Random(seed)
    mids = edge_mids(cx, cy, h)
    nodes = [(cx + rnd.uniform(-7, 7), cy + rnd.uniform(-3, 3)) for _ in range(rnd.choice((2, 3)))]
    paths = []
    for i, m in enumerate(mids):
        n = min(nodes, key=lambda q: math.hypot(q[0] - m[0], (q[1] - m[1]) * 2) + rnd.uniform(0, 4))
        paths.append(jag(m, n, 0.5, rnd, 3))   # from the edge inward: a crack enters from the neighbour
    for a, b in zip(nodes, nodes[1:]):
        paths.append(jag(a, b, 0.6, rnd, 2))
    spurs = []
    for _ in range(4):
        p = rnd.choice(paths)
        q = p[rnd.randrange(1, len(p) - 1)]
        ang = rnd.uniform(0, 2 * math.pi)
        ln = rnd.uniform(3, 6)
        spurs.append(jag(q, (q[0] + math.cos(ang) * ln, q[1] + math.sin(ang) * ln * 0.5), 0.5, rnd, 2))
    return paths, spurs


def floor_frames(seed):
    rnd = random.Random(seed + 100)
    c = FL / 2
    hexp = hex_pts(c, c, H)
    paths, spurs = crack_web(seed, c, c, H)
    # band: the shockwave crossing (bright fill), crack: the floor splitting, glow: holding, cool: fading
    plan = [("band", 1.0), ("band", 0.6), ("crack", 0.35), ("crack", 0.7), ("crack", 1.0), ("glow", 1.0),
            ("glow", 0.85), ("glow", 0.95), ("glow", 0.8), ("glow", 0.7), ("cool", 0.6), ("cool", 0.48),
            ("cool", 0.36), ("cool", 0.25), ("cool", 0.15), ("cool", 0.06)]
    out = []
    for i, (beat, v) in enumerate(plan):
        im = blank(FL)
        d = ImageDraw.Draw(im)
        if beat == "band":
            d.polygon(hexp, fill=VIO + (int(105 * v),))
        else:
            # effects draw over the fighters, so the scorch stays a light tint
            dark = {"crack": 50, "glow": 58, "cool": int(60 * v)}[beat]
            d.polygon(hexp, fill=ROCK + (dark,))
            grow = v if beat == "crack" else 1.0
            heat = 1.0 if beat == "crack" else (0.6 + 0.4 * (i % 2) if beat == "glow" else v)
            for p in paths:
                n = max(2, int(len(p) * grow))
                d.line(p[:n], fill=DEEP + (int(160 * min(1, heat + 0.2)),), width=3)
                d.line(p[:n], fill=(HOT if heat > 0.8 else LIL if heat > 0.45 else VIO) + (int(255 * min(1, heat + 0.25)),),
                       width=1)
            if beat != "crack":
                for s in spurs:
                    d.line(s, fill=VIO + (int(220 * heat),), width=1)
            if beat == "glow" and i % 2:
                for _ in range(3):
                    p = rnd.choice(paths)
                    x, y = p[rnd.randrange(len(p))]
                    d.point((x, y - 1), fill=HOT + (255,))
        out.append(im)
    return out


# ----------------------------------------------------------------------------------------------- storm
SL = 84              # scale 3: 84 drawn px = 3 tile heights; ground point at the centre, sky at the top
SC = SL / 2


def rock_poly(rnd, x, y, r):
    k = rnd.randrange(4, 6)
    return [(x + math.cos(a) * r * rnd.uniform(0.6, 1.1), y + math.sin(a) * r * rnd.uniform(0.6, 1.1))
            for a in sorted(rnd.uniform(0, 2 * math.pi) for _ in range(k))]


def rubble(im, rnd, chunks, t):
    d = ImageDraw.Draw(im)
    for x0, y0, vx, vy, r in chunks:
        x, y = x0 + vx * t, y0 + vy * t + 0.55 * t * t
        if y > SC + 6 or t < 0:
            continue
        poly = rock_poly(random.Random(int(x0 * 7 + r * 13)), x, y, r)
        d.polygon(poly, fill=ROCK + (255,), outline=ROCK_RIM + (255,))


def ground_flash(im, r, col, a):
    ImageDraw.Draw(im).ellipse((SC - r, SC - r / 2, SC + r, SC + r / 2), fill=col + (a,))


def storm_eruption(seed=61):
    """A: one pillar of lightning tears up out of the cracks with a smaller sister bolt; rock thrown up and out."""
    rnd = random.Random(seed)
    main = (SC + rnd.uniform(-3, 3), SC)
    side = (SC + rnd.choice((-1, 1)) * rnd.uniform(7, 10), SC + rnd.uniform(-2, 2))
    tops = [(main[0] + 9, 1), (side[0] - 6, rnd.uniform(14, 20))]   # leaning, so the field is not all verticals
    chunks = [(SC + rnd.uniform(-5, 5), SC, rnd.uniform(-2.4, 2.4), rnd.uniform(-5.5, -3.5), rnd.uniform(1.5, 2.6))
              for _ in range(5)]
    out = []
    for t in range(2):                                   # anticipation: the cracks under it flare
        im = blank(SL)
        ground_flash(im, 6 + 4 * t, VIO, 80 + 50 * t)
        bolt(im, jag(main, (main[0] + rnd.uniform(-3, 3), main[1] - 4 - 4 * t), 0.6, rnd, 2), 0.7 + 0.2 * t)
        out.append(im)
    for t in range(3):                                   # eruption
        im = blank(SL)
        ground_flash(im, 13 - 2 * t, VIO, 120)
        ground_flash(im, 6 - 2 * t, HOT, 230 - 60 * t)
        bolt(im, jag(main, tops[0], 0.38, rnd, 5), 1.0, 2 if t < 2 else 1, 3, rnd, upto=min(1, 0.55 + 0.45 * t))
        if t:
            bolt(im, jag(side, tops[1], 0.45, rnd, 4), 0.9, 1, 1, rnd)
        rubble(im, rnd, chunks, t)
        out.append(im)
    for t in range(3):                                   # crackle and fall
        im = blank(SL)
        if t != 1:
            bolt(im, jag(main, tops[0], 0.42, rnd, 5), 0.75 - 0.2 * t, 1, 1, rnd)
        rubble(im, rnd, chunks, t + 3)
        out.append(im)
    for t in range(3):                                   # embers
        im = blank(SL)
        d = ImageDraw.Draw(im)
        for j in range(5):
            d.point((round(main[0] + rnd.uniform(-3, 3)), round(main[1] - 3 - t * 3 - j * 4)),
                    fill=LIL + (max(0, 220 - 70 * t),))
        out.append(im)
    return out


def storm_seeker(seed=83):
    """B: a seeking bolt falls from the sky onto the tile: flash, rubble burst, ground arcs."""
    rnd = random.Random(seed)
    top = (SC - 26, 0)   # comes in on a slant: the bolts seek their targets from the sky at an angle
    chunks = [(SC + rnd.uniform(-4, 4), SC, rnd.uniform(-3, 3), rnd.uniform(-4.5, -2.5), rnd.uniform(1.4, 2.4))
              for _ in range(6)]
    out = []
    for t in range(2):                                   # a target mark tightens, the leader comes down
        im = blank(SL)
        d = ImageDraw.Draw(im)
        r = 9 - 3 * t
        d.ellipse((SC - r, SC - r / 2, SC + r, SC + r / 2), outline=LIL + (200,))
        bolt(im, jag(top, (top[0] + (SC - top[0]) * (0.25 + 0.25 * t), SC * (0.25 + 0.25 * t)), 0.5, rnd, 3), 0.7)
        out.append(im)
    for t in range(3):                                   # strike
        im = blank(SL)
        ground_flash(im, 14 - 2 * t, VIO, 130)
        ground_flash(im, 7 - 2 * t, HOT, 240 - 60 * t)
        bolt(im, jag(top, (SC, SC), 0.42, rnd, 5), 1.0, 2 if t < 2 else 1, 3, rnd)
        for _ in range(3):
            a = rnd.uniform(0, 2 * math.pi)
            bolt(im, jag((SC, SC), (SC + math.cos(a) * 14, SC + math.sin(a) * 7), 0.6, rnd, 3), 0.9)
        rubble(im, rnd, chunks, t)
        out.append(im)
    for t in range(3):                                   # ground arcs, rubble falls
        im = blank(SL)
        for _ in range(2):
            a = rnd.uniform(0, 2 * math.pi)
            bolt(im, jag((SC, SC), (SC + math.cos(a) * 13, SC + math.sin(a) * 6.5), 0.6, rnd, 3), 0.75 - 0.2 * t)
        rubble(im, rnd, chunks, t + 3)
        out.append(im)
    for t in range(3):                                   # embers
        im = blank(SL)
        d = ImageDraw.Draw(im)
        for j in range(6):
            a = j * 1.05
            d.point((round(SC + math.cos(a) * 6), round(SC + math.sin(a) * 3 - t * 3)), fill=LIL + (max(0, 220 - 70 * t),))
        out.append(im)
    return out


# ---------------------------------------------------------------------------------------------- caster
def caster_frames():
    rnd = random.Random(7)
    side = SL * 2
    body = (SC, SC - 0.4 * H)
    feet = (SC, SC + 0.4 * H)
    # the gate pillar (fx_f2_eightgates_purpleflame), feet anchored
    src = K.squared(K.frames("fx_f2_eightgates_purpleflame"))
    top, base_row = 3, 169
    k = 1.7 * (side / 3) / (base_row - top)
    s = int(round(src[0].width * k))
    pillar = []
    for f in src:
        cv = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        cv.paste(f.resize((s, s), Image.LANCZOS), (int(side / 2 - s / 2), int(side / 2 + 0.4 * side / 3 - base_row * k)),
                 f.resize((s, s), Image.LANCZOS))
        pillar.append(cv)
    seq = [2, 4, 6, 8, 10] + list(range(23, 31))
    # the v7 nova on the body
    nsrc = K.squared(K.frames("fx_f4_shadownova"))
    nk = side / nsrc[0].width
    nova = []
    for i in list(range(0, 12)) + [13, 15]:
        f = nsrc[i].resize((side, side), Image.LANCZOS)
        cv = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        cv.paste(f, (0, int(round(side / 2 - 0.4 * side / 3 - 98 * nk))), f)
        nova.append(cv)
    paths, _ = crack_web(5, SC, SC, H)               # the floor web on the caster's own tile, lines only
    n = RELEASE + len(nova)
    out = []
    for t in range(n):
        lt = blank(SL)
        d = ImageDraw.Draw(lt)
        if t < RELEASE:                              # charge
            for _ in range(1 + t):
                a = (body[0] + rnd.uniform(-5, 5), body[1] + rnd.uniform(-11, 9))
                b = (body[0] + rnd.uniform(-7, 7), body[1] + rnd.uniform(-11, 11))
                bolt(lt, jag(a, b, 0.6, rnd, 3), 0.7 + 0.06 * t)
            if t >= 2:
                for _ in range(t - 1):
                    g = (feet[0] + rnd.choice((-1, 1)) * rnd.uniform(5, 13), feet[1] + rnd.uniform(-2, 2))
                    bolt(lt, jag((body[0], body[1] + 6), g, 0.5, rnd, 3), 0.8)
            grow = t / RELEASE
            for p in paths:
                d.line(p[:max(2, int(len(p) * grow * 0.6))], fill=LIL + (160,), width=1)
        else:
            j = t - RELEASE
            if j < 2:                                # the fury flash: a burst of light on the body
                for r, a in ((26, 50), (17, 90), (9, 170)):
                    r -= 6 * j
                    d.ellipse((body[0] - r, body[1] - r * 0.8, body[0] + r, body[1] + r * 0.8),
                              fill=HOT + (a // (j + 1),))
            if j < 7:                                # the sky column: lightning straight up off the top of the clip
                for k2 in range(3 if j < 4 else 1):
                    x0 = body[0] + rnd.uniform(-3, 3)
                    bolt(lt, jag((x0, body[1]), (x0 + rnd.uniform(-6, 6), -4), 0.35, rnd, 5),
                         1.0 - 0.12 * j, 2 if j < 3 else 1, 2, rnd, upto=min(1, 0.5 + 0.5 * j))
            heat = max(0.15, 1 - 0.09 * j)
            for p in paths:
                d.line(p, fill=DEEP + (int(160 * heat),), width=3)
                d.line(p, fill=(HOT if heat > 0.8 else LIL if heat > 0.45 else VIO) + (int(255 * heat),), width=1)
        cv = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        if t < len(seq):
            cv.alpha_composite(pillar[seq[t]])
        if t >= RELEASE:
            cv.alpha_composite(nova[t - RELEASE])
        cv.alpha_composite(lt.resize((side, side), Image.NEAREST))
        out.append(cv)
    return out


# ----------------------------------------------------------------------------------------------- build
SETTINGS = {
    "floor": dict(mirror=True, stagger=40, ripple=70),
    "storm": dict(mirror=True, stagger=600, ripple=60, alternate=True),
}


def clips():
    return {
        "caster": (caster_frames(), C_MS, 3),
        "floor_a": (lead(up(floor_frames(11), 3), F_LEAD), F_MS, 2),
        "floor_b": (lead(up(floor_frames(29), 3), F_LEAD), F_MS, 2),
        "storm_a": (lead(up(storm_eruption(), 2), S_LEAD), S_MS, 3),
        "storm_b": (lead(up(storm_seeker(), 2), S_LEAD), S_MS, 3),
    }


def main():
    for cid, (frs, ms, scale) in clips().items():
        px = frs[0].width
        assert px * len(frs) <= 4096, (cid, px, len(frs))
        fn = os.path.join(HERE, f"anim_fcf_v11_{cid}_{px}.webp")
        b = K.write_strip(frs, fn, px)
        print(f"{os.path.basename(fn)}: {len(frs)} frames x {ms} ms, scale {scale}, {px} px "
              f"({px * len(frs)} px tall), {b} bytes")


if __name__ == "__main__":
    main()
