#!/usr/bin/env python3
"""Forbidden Chakra Fury v17: one overwhelming discharge (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v17/build_v17.py

Director on v16: "reads more like a firecracker ... rather than one large discharge. I'm imagining the bolts spawning
off the player over ~300ms, leaving in random intervals, and streaking across to the edge ... rather than striking the
tiles themselves. Like an overwhelming burst that strikes at the entire aoe ... like we're looking at a night sky with
lightning strikes head on."
- NIGHT (recoil, scale 2, centred): the area darkens like a night sky just before the release and lifts after it,
  feathered past each hex edge so it reads as one shadow; a faint violet sheen in it.
- STREAK (damage, beamed, alternate = empty): every bolt leaves the user inside a 300 ms window (stagger 300, no
  ripple) and streaks outward along its beam: it races out in two frames, saturates, flickers once down the same
  channel, and dies. It does not strike: no impact, the far end thins and splits into a few hair-fine forks, like
  spider lightning seen head-on. The outer rings hold most tiles, so most bolts run to the edge of the area.
- CASTER (visual, scale 3): the storm winds up on the user; on release the flash, the nova and a crackling core while
  the bolts leave.
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
for v in ("v16", "v15", "v14", "v13"):
    sys.path.insert(0, os.path.join(HERE, "..", v))
import build_v13 as V  # noqa: E402
import build_v14 as V14  # noqa: E402
import build_v15 as V15  # noqa: E402
import build_v16 as V16  # noqa: E402
import fxlight as L  # noqa: E402
import ground_hd as G  # noqa: E402

K = V.K
N, SS = V.N, V.SS
SC, SH = V14.SC, V14.SH
blank = V14.blank
C_MS, S_MS, F_MS = 80, 50, 50
RELEASE = 5
SETTINGS = {
    "storm": dict(beam=True, mirror=True, stagger=300, ripple=0, alternate=True),
    "night": dict(mirror=False, stagger=0, ripple=0),
}
S_LEAD_MS = 400            # the bolts start leaving on the release
N_LEAD_MS = 160            # the night falls a little before it


def streak_frames(seed):
    """Caster at the left edge, the far end at the right. Races out, saturates, flickers, dies; far end splits."""
    rnd = random.Random(seed)
    W = N * SS
    channel = G.angular((0, SC), (N * 0.86, SC + rnd.uniform(-4, 4)), rnd, 0.16, 0.035)
    channel = [(x, SC + (y - SC) * 3.2) for x, y in channel]
    tip = channel[-1]
    forks = []
    for _ in range(3):
        a = rnd.uniform(-0.9, 0.9)
        forks.append(G.angular(tip, (min(N - 2, tip[0] + 18), tip[1] + math.tan(a) * 18 * 1.8), rnd, 0.4, 0.05))
    beats = [("race", 0.5), ("race", 1.0), ("stroke", 0), ("after", 0), ("dark", 0), ("restrike", 0), ("die", 0),
             ("die", 1)]
    out = []
    for t, (beat, k) in enumerate(beats):
        cv = V.Canvas()
        if beat == "race":                     # the leader racing outward, already bright at its root
            n = int(len(channel) * k)
            V16.big_bolt(cv, channel[:n], 2.4 + 1.2 * k, 170 + 60 * k)
        elif beat == "stroke":                 # saturates end to end; forks lit
            V16.big_bolt(cv, channel, 4.6, 255)
            for f in forks:
                cv.tapered(f, 1.4, 0.2, 230, 40)
        elif beat == "after":
            V16.big_bolt(cv, channel, 2.6, 180)
            for f in forks[:1]:
                cv.tapered(f, 0.8, 0.2, 150, 30)
        elif beat == "dark":
            cv.tapered(channel, 1.0, 0.8, 45, 30)
        elif beat == "restrike":
            V16.big_bolt(cv, channel, 3.6, 235)
        else:
            cv.tapered(channel, 1.0 - 0.4 * k, 0.6, 60 - 30 * k, 20)
        out.append(cv.render(V.plasma(seed, t, W), gains=(1.0, 1.1, 0.6), pool_r=6))
    return out


def night_frames():
    """A darkening that covers the hex past its edges (feathered), with a faint violet sheen; falls, holds, lifts."""
    h = c = N / 2
    W = N * SS
    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).polygon([(x * SS, y * SS) for x, y in G.hex_pts(c, c, h * 1.04)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(4 * SS)).resize((N, N), Image.LANCZOS)
    out = []
    levels = [0.25, 0.5, 0.7, 0.8, 0.82, 0.82, 0.8, 0.78, 0.74, 0.7, 0.64, 0.56, 0.46, 0.36, 0.26, 0.17, 0.1, 0.04]
    for i, a in enumerate(levels):
        dark = Image.new("RGBA", (N, N), (10, 6, 22, 0))
        dark.putalpha(mask.point(lambda v, a=a: int(v * a * 0.62)))
        sheen = Image.new("RGBA", (N, N), (120, 60, 220, 0))
        sheen.putalpha(mask.point(lambda v, a=a: int(v * a * 0.06)))
        dark.alpha_composite(sheen)
        out.append(dark)
    return out


def caster_frames():
    rnd = random.Random(7)
    body = (SC, SC - 0.4 * SH)
    W = N * SS
    nsrc = K.squared(K.frames("fx_f4_shadownova"))
    nk = N / nsrc[0].width
    nova = []
    for i in list(range(0, 12)) + [13, 15]:
        f = nsrc[i].resize((N, N), Image.LANCZOS)
        cvn = blank()
        cvn.paste(f, (0, int(round(body[1] - 98 * nk))), f)
        nova.append(cvn)
    n = RELEASE + len(nova)
    out = []
    for t in range(n):
        cv = V.Canvas()
        r = random.Random(90 + t)
        if t < RELEASE:
            rad = 10 + 3 * t
            for j in range(3 + t):
                a0 = j * 2.4 + t * 0.9
                p = (body[0] + math.cos(a0) * rad, body[1] + math.sin(a0) * rad * 0.9)
                q = (body[0] + math.cos(a0 + 1.6) * rad, body[1] + math.sin(a0 + 1.6) * rad * 0.9)
                cv.tapered(G.angular(p, q, r, 0.4, 0.05), 1.4, 1.0, 170 + 18 * t, 150)
            cv.blob(body[0], body[1], rad + 4, rad + 2, 60 + 30 * t)
            cv.blob(body[0], body[1], 4 + t, 4 + t, 150 + 20 * t, 0.4, target="core")
        else:
            j = t - RELEASE
            if j < 2:
                cv.blob(body[0], body[1], 40 - 10 * j, 32 - 8 * j, 255 - 70 * j, 0.45, target="core")
            if j < 6:                                  # a crackling core while the bolts leave
                for _ in range(4 - j // 2):
                    a = r.uniform(0, 2 * math.pi)
                    q = (body[0] + math.cos(a) * r.uniform(10, 20), body[1] + math.sin(a) * r.uniform(8, 16))
                    cv.tapered(G.angular(body, q, r, 0.4, 0.05), 2.0, 0.4, 240 - 30 * j, 120)
                cv.blob(body[0], body[1], 12, 12, 200 - 30 * j, 0.4)
        light = cv.render(V.plasma(5, t, W), gains=(1.0, 1.2, 0.8))
        light.putalpha(ImageChops.multiply(light.getchannel("A"), V15.EDGE))
        frame = blank()
        if t >= RELEASE:
            frame.alpha_composite(nova[t - RELEASE])
        frame.alpha_composite(light)
        out.append(frame)
    return out


def clips():
    s = streak_frames(61)
    return {
        "caster": (caster_frames(), C_MS, 3),
        "streak": (s, S_MS, 3),
        "night": (night_frames(), F_MS, 2),
    }


def main():
    cs = clips()
    for cid, (frs, ms, scale) in cs.items():
        px = frs[0].width
        assert px * len(frs) <= 4096, (cid, px, len(frs))
        fn = os.path.join(HERE, f"anim_fcf_v17_{cid}_{px}.webp")
        b = K.write_strip(frs, fn, px)
        assert b <= 460800, (cid, b)
        print(f"{os.path.basename(fn)}: {len(frs)} frames x {ms} ms, scale {scale}, {px} px, {b} bytes")
    return cs


if __name__ == "__main__":
    main()
