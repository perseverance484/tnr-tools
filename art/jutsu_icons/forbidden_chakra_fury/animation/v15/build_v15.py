#!/usr/bin/env python3
"""Forbidden Chakra Fury v15: the v14 storm with real-lightning timing (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v15/build_v15.py

Director: "The lightning does not need to start at the same time nor strike at the same time or be uniform. Look at
actual lightning strikes/storms and also look at anime that use attacks like this."
What real lightning does (NOAA/NWS/Britannica, NAP Physics of Lightning): a dim stepped leader gropes out in jerky
steps, branching; when one branch connects, the return stroke lights the whole channel at once (over 99% of the
light) and the dead branches light with it; then dart leaders re-strike the same channel two to four times, 40-80 ms
apart, which is the flicker. Anime adds impact frames (one or two white-hot frames on contact) and holds.
So each lash: leader groping in (dim, branching) -> impact frame (whole channel and branches white-hot) -> dark ->
one or two restrikes down the same channel -> forks crawl on outward -> embers. Lash A is a big strike with two
restrikes, lash B a smaller one with one. Wide stagger (350 ms) plus ripple (90 ms per hex) scatters them: the storm
keeps lashing out for about a second instead of firing in rings. The caster keeps throwing bolts in changing
directions while it lasts. Clips are drawn pointing away from the caster (see v14 on aim).
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

EDGE = Image.new("L", (168, 168), 0)
ImageDraw.Draw(EDGE).ellipse((10, 10, 158, 158), fill=255)
EDGE = EDGE.filter(ImageFilter.GaussianBlur(9))

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v14"))
sys.path.insert(0, os.path.join(HERE, "..", "v13"))
import build_v13 as V  # noqa: E402
import build_v14 as V14  # noqa: E402
import fxlight as L  # noqa: E402

K = V.K
N, SS = V.N, V.SS
C_MS, S_MS, F_MS = 80, 50, 50
RELEASE, S_LEAD = 5, 6
F_LEAD = S_LEAD + 3            # the crater opens on the return stroke
SETTINGS = {
    "storm": dict(aim=True, mirror=True, stagger=350, ripple=90, alternate=True),
    "floor": dict(mirror=True, stagger=350, ripple=90, alternate=True),   # same hash and delays: lands with the bolt
}
SC = V14.SC
SH = V14.SH
blank, lead = V14.blank, V14.lead


def lash_frames(seed, big=True):
    rnd = random.Random(seed)
    W = N * SS
    start = (0, SC + rnd.choice((-1, 1)) * rnd.uniform(6, 16))
    channel = L.jag(start, (SC, SC), 0.42, rnd, 6)
    probes = []                                   # leader branches that never connect
    for _ in range(4 if big else 2):
        i = rnd.randrange(len(channel) // 5, len(channel) - 6)
        p = channel[i]
        a = rnd.uniform(-1.1, 1.1)
        ln = rnd.uniform(12, 26)
        probes.append((i, L.jag(p, (p[0] + math.cos(a) * ln, p[1] + math.sin(a) * ln * 0.8), 0.5, rnd, 4)))
    forks = []
    for _ in range(3 if big else 2):
        a = rnd.uniform(-0.8, 0.8)
        ln = rnd.uniform(0.5, 0.95) * (N - SC)
        forks.append(L.jag((SC, SC), (SC + math.cos(a) * ln, SC + math.sin(a) * ln * 0.75), 0.42, rnd, 5))
    w = 4.4 if big else 3.0
    beats = [("leader", 0.35), ("leader", 0.62), ("leader", 0.86), ("stroke", 0), ("dark", 0), ("restrike", 0),
             ("dark", 1)]
    beats += [("restrike", 1), ("forks", 0)] if big else [("forks", 0), ("forks", 1)]
    beats += [("forks", 1 if big else 2), ("crawl", 0), ("crawl", 1), ("ember", 0), ("ember", 1)]
    out = []
    for t, (beat, k) in enumerate(beats):
        cv = V.Canvas()
        r = random.Random(seed * 41 + t)
        if beat == "leader":                     # dim, jerky, groping branches
            n = int(len(channel) * k)
            cv.tapered(L.wobble(channel[:n], r, 0.4), 1.2, 1.0, 120, 150)
            for i, pr in probes:
                if i < n:
                    cv.tapered(pr[: max(2, int(len(pr) * min(1, (n - i) / 12)))], 0.9, 0.3, 110, 40)
            tip = channel[max(0, n - 1)]
            cv.blob(tip[0], tip[1], 3, 2.4, 200, 0.4, target="core")
        elif beat == "stroke":                   # the impact frame: the whole channel and its dead branches white-hot
            cv.blob(SC, SC, 30, 15, 230)
            cv.blob(SC, SC, 9, 5, 255, 0.25, target="core")
            V.hd_bolt(cv, channel, r, w=w, val=255, branches=0)
            for i, pr in probes:
                cv.tapered(pr, w * 0.45, 0.3, 240, 120)
            L.sparks(V._Shim(cv), seed, (SC, SC), 1, n=12)
        elif beat == "dark":                     # the pause between strokes: an afterglow only
            cv.tapered(channel, 1.0, 1.0, 70 - 25 * k, 70 - 25 * k)
            cv.blob(SC, SC, 14, 7, 90)
        elif beat == "restrike":                 # a dart leader down the same channel, no branches
            cv.blob(SC, SC, 20 - 4 * k, 10 - 2 * k, 190 - 40 * k)
            V.hd_bolt(cv, L.wobble(channel, r, 0.4), r, w=w * (0.8 - 0.15 * k), val=250 - 30 * k, branches=0,
                      strand=False)
            L.sparks(V._Shim(cv), seed + 1 + k, (SC, SC), 1, n=6)
        elif beat == "forks":                    # the charge lashes on outward toward the next ring
            g = 0.45 + 0.3 * k
            for f in forks:
                V.hd_bolt(cv, L.wobble(f, r, 0.5), r, w=2.4 - 0.4 * k, val=245 - 40 * k, branches=2, upto=min(1, g))
                tip = f[max(0, int(len(f) * min(1, g)) - 1)]
                cv.blob(tip[0], tip[1], 3.5, 2.6, 220 - 50 * k, 0.4, target="core")
            cv.tapered(channel, 1.2, 1.2, 90 - 30 * k, 90 - 30 * k)
        elif beat == "crawl":
            for j in range(3):
                a = r.uniform(0, 2 * math.pi)
                c = L.jag((SC, SC), (SC + math.cos(a) * r.uniform(12, 24), SC + math.sin(a) * r.uniform(5, 10)), 0.5, r, 4)
                V.hd_bolt(cv, c, r, w=1.2, val=170 - 50 * k, branches=1, strand=False)
        else:
            for _ in range(5):
                cv.blob(SC + r.uniform(-14, 14), SC - r.uniform(2, 14) - 3 * k, 1.2, 1.2, 200 - 60 * k, 0.3,
                        target="core")
        out.append(cv.render(V.plasma(seed, t, W), gains=(1.1, 1.3, 0.9)))
    return out


def caster_frames():
    """The storm forms on the user, then keeps throwing bolts in changing directions: a burst on release, then two
    or three new ones every frame, each a leader, a stroke and a flicker."""
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

    def bolt_path(a):
        end = (SC + math.cos(a) * N * rnd.uniform(0.36, 0.44), feet[1] + math.sin(a) * N * rnd.uniform(0.16, 0.22))
        return L.jag((body[0] + rnd.uniform(-3, 3), body[1] + rnd.uniform(0, 10)), end, 0.34, rnd, 6)
    live = []                                    # [path, age]
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
                V.hd_bolt(cv, L.jag(p, q, 0.6, r, 4), r, w=1.4 + 0.15 * t, val=170 + 18 * t, branches=1, strand=False)
            cv.blob(body[0], body[1], rad + 4, rad + 2, 60 + 30 * t)
            cv.blob(body[0], body[1], 4 + t, 4 + t, 150 + 20 * t, 0.4, target="core")
            if t >= 3:
                crater.draw(cv, 0.15 * (t - 2), 0.8, plates=False)
        else:
            j = t - RELEASE
            if j < 2:
                cv.blob(body[0], body[1], 42 - 10 * j, 34 - 8 * j, 255 - 70 * j, 0.45, target="core")
            spawn = 6 if j == 0 else (rnd.choice((1, 2, 3)) if j < 9 else 0)
            for _ in range(spawn):
                live.append([bolt_path(rnd.uniform(0, 2 * math.pi)), 0])
            for b in live:
                age = b[1]
                if age == 0:
                    V.hd_bolt(cv, b[0], r, w=3.4, val=255, branches=2)
                elif age == 1:
                    cv.tapered(b[0], 1.0, 1.0, 70, 70)
                elif age == 2 and r.random() < 0.6:
                    V.hd_bolt(cv, L.wobble(b[0], r, 0.4), r, w=2.2, val=220, branches=0, strand=False)
                b[1] += 1
            live = [b for b in live if b[1] < 3]
            crater.draw(cv, min(1, 0.6 + 0.2 * j), max(0.2, 1 - 0.07 * j))
        light = cv.render(V.plasma(5, t, W))
        light.putalpha(ImageChops.multiply(light.getchannel("A"), EDGE))   # no square edge on the glow
        frame = blank()
        if t >= RELEASE:
            frame.alpha_composite(nova[t - RELEASE])
        frame.alpha_composite(light)
        out.append(frame)
    return out


def clips():
    return {
        "caster": (caster_frames(), C_MS, 3),
        "storm_a": (lead(lash_frames(61, True), S_LEAD), S_MS, 3),
        "storm_b": (lead(lash_frames(83, False), S_LEAD), S_MS, 3),
        "floor_a": (lead(V14.floor_frames(11), F_LEAD), F_MS, 2),
        "floor_b": (lead(V14.floor_frames(29), F_LEAD), F_MS, 2),
    }


def main():
    cs = clips()
    for cid, (frs, ms, scale) in cs.items():
        px = frs[0].width
        assert px * len(frs) <= 4096, (cid, px, len(frs))
        fn = os.path.join(HERE, f"anim_fcf_v15_{cid}_{px}.webp")
        b = K.write_strip(frs, fn, px)
        assert b <= 460800, (cid, b)
        print(f"{os.path.basename(fn)}: {len(frs)} frames x {ms} ms, scale {scale}, {px} px "
              f"({px * len(frs)} px tall), {b} bytes")
    return cs


if __name__ == "__main__":
    main()
