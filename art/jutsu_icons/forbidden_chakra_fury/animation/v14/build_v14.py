#!/usr/bin/env python3
"""Forbidden Chakra Fury v14: one storm forms on the user, then lashes out across the area (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v14/build_v14.py

Director on v13: "still a bunch of separate animations ... I'm imagining one big lightning storm forming on the player
then arcing out. The bolts travel from the player and lash out to the tiles, forking and striking them. Rather than
the lightning coming from above it comes from the players tile."

That needs a tile clip that knows which way the caster is. The engine cannot do that today (mirror only flips left /
right). This build assumes one more per-effect setting for the area-variation PR, `animationAim`: each tile's clip
is turned so its right-hand side points away from the caster's tile (the angle from the caster tile centre to the
tile centre, on screen); mirror then flips across that axis. With it the pieces chain into one storm:
- CASTER (visual, scale 3, 80 ms): a ball of lightning winds up around the user, then the fury flash and the nova,
  and eight bolts lash out from the body across the user's hex in every direction.
- LASH A / B (damage, scale 3, 50 ms, aimed, ripple 100 ms per hex): a bolt enters from the caster side (from the
  inner neighbour's centre), runs to the tile centre in two frames, strikes, and forks on outward toward the next ring.
  The next ring's bolts start where these forks end, 100 ms later, so the lightning reads as travelling out from the
  user and splitting at every tile.
- FLOOR (recoil, scale 2, 50 ms, not aimed): when the bolt lands, a crater of HD rifts opens under it in the charged
  glow, then cools.
"""
import math
import os
import random
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
V13 = os.path.join(HERE, "..", "v13")
sys.path.insert(0, V13)
import build_v13 as V  # noqa: E402  (Canvas, hd_bolt, Crater, plasma, dust, debris shim, Duelyst kit)
import fxlight as L  # noqa: E402
import ground_hd as G  # noqa: E402

K = V.K
N, SS = V.N, V.SS
C_MS, S_MS, F_MS = 80, 50, 50
RELEASE = 5                 # caster frame of the release (400 ms)
S_LEAD = 6                  # lash: the first ring starts at 300 + 100 ms ripple = 400 ms
F_LEAD = S_LEAD + 2         # floor: the crater opens as the bolt lands
SETTINGS = {
    "storm": dict(aim=True, mirror=True, stagger=70, ripple=100, alternate=True),
    "floor": dict(mirror=True, stagger=0, ripple=100, alternate=True),
}
SH = N / 3
SC = N / 2


def blank():
    return Image.new("RGBA", (N, N), (0, 0, 0, 0))


def lead(frs, n):
    return [blank() for _ in range(n)] + frs


# ------------------------------------------------------------------------------------------- lash
def lash_frames(seed):
    """The clip is drawn pointing right: the caster is to the left. The bolt arrives from the left edge (the inner
    neighbour's centre), strikes the centre, and forks on to the right."""
    rnd = random.Random(seed)
    W = N * SS
    start = (0, SC + rnd.choice((-1, 1)) * rnd.uniform(8, 16))     # off-axis, so the field is not a sunburst
    bolt = L.jag(start, (SC, SC), 0.42, rnd, 6)
    forks = []
    for k in range(rnd.choice((2, 3))):
        ang = rnd.uniform(-0.75, 0.75)
        ln = rnd.uniform(0.55, 0.95) * (N - SC)
        end = (SC + math.cos(ang) * ln, SC + math.sin(ang) * ln * 0.75)
        forks.append(L.jag((SC, SC), end, 0.4, rnd, 5))
    crackle = [L.jag((SC + rnd.uniform(-4, 4), SC + rnd.uniform(-2, 2)),
                     (SC + math.cos(a) * rnd.uniform(14, 26), SC + math.sin(a) * rnd.uniform(6, 12)), 0.5, rnd, 4)
               for a in (rnd.uniform(0, 6.28) for _ in range(5))]
    out = []
    plan = [("travel", 0.55), ("travel", 1.0), ("strike", 0), ("strike", 1), ("fork", 0), ("fork", 1),
            ("crackle", 0), ("crackle", 1), ("fade", 0), ("fade", 1), ("fade", 2)]
    for t, (beat, k) in enumerate(plan):
        cv = V.Canvas()
        r = random.Random(seed * 31 + t)
        if beat == "travel":                 # the bolt runs in from the caster side; its head is white-hot
            V.hd_bolt(cv, L.wobble(bolt, r, 0.5), r, w=3.2, val=245, branches=2, upto=k)
            head = bolt[max(0, int(len(bolt) * k) - 1)]
            cv.blob(head[0], head[1], 6, 4, 255, 0.4, target="core")
        elif beat == "strike":               # it lands: flash, the bolt at full heat
            cv.blob(SC, SC, 24 - 6 * k, 12 - 3 * k, 210 - 40 * k)
            cv.blob(SC, SC, 7 - 2 * k, 4 - k, 255, 0.25, target="core")
            V.hd_bolt(cv, L.wobble(bolt, r, 0.5), r, w=4.2 - k, val=255, branches=3)
            for f in forks:
                V.hd_bolt(cv, L.wobble(f, r, 0.5), r, w=2.4, val=235, branches=1, upto=0.35 + 0.3 * k)
            L.sparks(V._Shim(cv), seed, (SC, SC), k + 1, n=8)
        elif beat == "fork":                 # the forks lash on outward to the next ring
            cv.blob(SC, SC, 16, 8, 140 - 30 * k)
            V.hd_bolt(cv, L.wobble(bolt, r, 0.7), r, w=2.4, val=200 - 40 * k, branches=1)
            for f in forks:
                V.hd_bolt(cv, L.wobble(f, r, 0.5), r, w=2.6 - 0.4 * k, val=250, branches=2, upto=0.8 + 0.2 * k)
                tip = f[-1]
                cv.blob(tip[0], tip[1], 4, 3, 230 - 60 * k, 0.4, target="core")
            L.sparks(V._Shim(cv), seed, (SC, SC), k + 3, n=8)
        elif beat == "crackle":              # what is left crawls and flickers
            for j, c in enumerate(crackle):
                if (j + k) % 2 == 0:
                    V.hd_bolt(cv, L.wobble(c, r, 0.8), r, w=1.3, val=200 - 35 * k, branches=1, strand=False)
            if k in (0, 2):
                V.hd_bolt(cv, L.wobble(bolt, r, 1.0), r, w=1.6, val=150 - 40 * k, branches=0, strand=False)
            if k < 2:
                for f in forks:
                    V.hd_bolt(cv, L.wobble(f, r, 0.9), r, w=1.2, val=150 - 60 * k, branches=0, strand=False)
        else:                                # embers
            for _ in range(5):
                x, y = SC + r.uniform(-14, 14), SC - r.uniform(2, 14) - 3 * k
                cv.blob(x, y, 1.2, 1.2, 210 - 50 * k, 0.3, target="core")
        out.append(cv.render(V.plasma(seed, t, W), gains=(1.1, 1.3, 0.9)))
    return out


# ------------------------------------------------------------------------------------------ floor
def floor_frames(seed):
    """Not aimed. The charged glow and a crater of rifts open the moment the bolt lands, then cool."""
    h = N / 2
    c = N / 2
    W = N * SS
    from PIL import ImageChops, ImageDraw, ImageFilter
    fill = Image.new("L", (W, W), 0)
    ImageDraw.Draw(fill).polygon([(x * SS, y * SS) for x, y in G.hex_pts(c, c, h * 0.96)], fill=255)
    fill = fill.filter(ImageFilter.GaussianBlur(3 * SS))
    crater = V.Crater(seed, c, c, h * 0.62, count=5)
    plan = [(0.6, 1.0, 0.18), (1.0, 1.0, 0.17), (1.0, 0.95, 0.16), (1.0, 0.9, 0.15), (1.0, 0.82, 0.14),
            (1.0, 0.74, 0.13), (1.0, 0.66, 0.12), (1.0, 0.58, 0.1), (1.0, 0.5, 0.09), (1.0, 0.42, 0.08),
            (1.0, 0.34, 0.06), (1.0, 0.26, 0.05), (1.0, 0.18, 0.03), (1.0, 0.1, 0.02)]
    out = []
    for t, (grow, heat, glow) in enumerate(plan):
        cv = V.Canvas()
        tex = V.plasma(seed, t, W)
        layer = ImageChops.multiply(fill.point(lambda v, g=glow: int(v * g)), tex.point(lambda v: 110 + v * 145 // 255))
        cv.body = ImageChops.lighter(cv.body, layer)
        cv.db = ImageDraw.Draw(cv.body)
        crater.draw(cv, grow, heat, fade=min(1.0, heat * 1.4))
        out.append(cv.render(V.plasma(seed + 1, t, W), gains=(1.1, 1.6, 1.3), cap=0.92))
    return out


# ----------------------------------------------------------------------------------------- caster
def caster_frames():
    """The storm forms on the user (a ball of lightning winding up around the body), then the fury: the flash, the
    nova, and eight bolts lashing out from the body across the hex in every direction."""
    rnd = random.Random(7)
    body = (SC, SC - 0.4 * SH)
    feet = (SC, SC + 0.4 * SH)
    W = N * SS
    nsrc = K.squared(K.frames("fx_f4_shadownova"))
    nk = N / nsrc[0].width
    nova = []
    for i in list(range(0, 12)) + [13, 15]:
        f = nsrc[i].resize((N, N), Image.LANCZOS)
        cvn = blank()
        cvn.paste(f, (0, int(round(body[1] - 98 * nk))), f)
        nova.append(cvn)
    crater = V.Crater(5, SC, feet[1] - 2, 40, count=6)
    lashes = []
    for k in range(8):
        a = k * 2 * math.pi / 8 + rnd.uniform(-0.2, 0.2)
        end = (SC + math.cos(a) * N * 0.52, feet[1] + math.sin(a) * N * 0.26)
        lashes.append(L.jag((body[0], body[1] + 6), end, 0.32, rnd, 6))
    n = RELEASE + len(nova)
    out = []
    for t in range(n):
        cv = V.Canvas()
        r = random.Random(90 + t)
        if t < RELEASE:                       # the storm winds up: arcs orbit the body and the ball grows
            rad = 10 + 3 * t
            for j in range(3 + t):
                a0 = j * 2.4 + t * 0.9
                p = (body[0] + math.cos(a0) * rad, body[1] + math.sin(a0) * rad * 0.9)
                q = (body[0] + math.cos(a0 + 1.6) * rad, body[1] + math.sin(a0 + 1.6) * rad * 0.9)
                V.hd_bolt(cv, L.jag(p, q, 0.6, r, 4), r, w=1.4 + 0.15 * t, val=170 + 18 * t, branches=1, strand=False)
            cv.blob(body[0], body[1], rad + 4, rad + 2, 60 + 30 * t)
            cv.blob(body[0], body[1], 4 + t, 4 + t, 150 + 20 * t, 0.4, target="core")
            if t >= 3:
                crater.draw(cv, 0.15 * (t - 2), 0.8, plates=False)
        else:
            j = t - RELEASE
            if j < 2:
                cv.blob(body[0], body[1], 42 - 10 * j, 34 - 8 * j, 255 - 70 * j, 0.45, target="core")
            if j < 6:
                for k, l in enumerate(lashes):
                    if j >= 3 and (k + j) % 2:
                        continue
                    V.hd_bolt(cv, L.wobble(l, r, 0.6), r, w=3.6 if j < 2 else 2.2, val=255 - 30 * j, branches=2,
                              upto=min(1, 0.5 + 0.5 * j))
            crater.draw(cv, min(1, 0.6 + 0.2 * j), max(0.2, 1 - 0.08 * j))
        light = cv.render(V.plasma(5, t, W))
        frame = blank()
        if t >= RELEASE:
            frame.alpha_composite(nova[t - RELEASE])
        frame.alpha_composite(light)
        out.append(frame)
    return out


def clips():
    return {
        "caster": (caster_frames(), C_MS, 3),
        "storm_a": (lead(lash_frames(61), S_LEAD), S_MS, 3),
        "storm_b": (lead(lash_frames(83), S_LEAD), S_MS, 3),
        "floor_a": (lead(floor_frames(11), F_LEAD), F_MS, 2),
        "floor_b": (lead(floor_frames(29), F_LEAD), F_MS, 2),
    }


def main():
    cs = clips()
    for cid, (frs, ms, scale) in cs.items():
        px = frs[0].width
        assert px * len(frs) <= 4096, (cid, px, len(frs))
        fn = os.path.join(HERE, f"anim_fcf_v14_{cid}_{px}.webp")
        b = K.write_strip(frs, fn, px)
        assert b <= 460800, (cid, b)
        print(f"{os.path.basename(fn)}: {len(frs)} frames x {ms} ms, scale {scale}, {px} px "
              f"({px * len(frs)} px tall), {b} bytes")
    return cs


if __name__ == "__main__":
    main()
