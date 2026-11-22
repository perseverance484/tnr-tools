#!/usr/bin/env python3
"""Forbidden Chakra Fury v16: one big streak per strike (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v16/build_v16.py

Director: "Lightning doesn't look like that. It looks like 1 large streak or bolt." Reference: high-speed lightning
footage descriptions (NWS 4,000 fps; ICAE 2014 attachment study; 11,000 fps study): the stepped leader is faint and
branched; when a branch connects, the return stroke saturates the frame, the unconnected branches re-illuminate and go
out within about a millisecond, and what remains is a single bright channel; restrikes run down that same channel.
At game frame rates (50 ms) that reads as: a faint flicker of leader, then ONE thick white-hot channel, a dark gap,
one or two restrikes down the same channel, gone. No crawling forks, no glowing heads.
- STRIKE A (damage, aimed): that sequence, a thick channel with a few large kinks running from the inner neighbour's
  centre to this tile, two short stubs that die after the stroke frame. STRIKE B (the alternate): no bolt, a faint
  charge only, so about half the tiles are struck and each strike stands alone as a big streak.
- FLOOR A (recoil): the crater flashes open under the strike and cools in about 0.4 s. FLOOR B: the charged glow
  only. Same hash bit as the strike's alternate, so craters land only where bolts land.
- CASTER: the storm forms on the user; on release three big streaks, then one or two new ones per frame.
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
for v in ("v15", "v14", "v13"):
    sys.path.insert(0, os.path.join(HERE, "..", v))
import build_v13 as V  # noqa: E402
import build_v14 as V14  # noqa: E402
import build_v15 as V15  # noqa: E402
import fxlight as L  # noqa: E402
import ground_hd as G  # noqa: E402

K = V.K
N, SS = V.N, V.SS
C_MS, S_MS, F_MS = 80, 50, 50
RELEASE, S_LEAD = 5, 6
F_LEAD = S_LEAD + 2
SETTINGS = {
    "storm": dict(aim=True, mirror=True, stagger=450, ripple=90, alternate=True),
    "floor": dict(mirror=True, stagger=450, ripple=90, alternate=True),
}
SC, SH = V14.SC, V14.SH
blank, lead = V14.blank, V14.lead
EDGE = V15.EDGE


def streak(a, b, rnd):
    """A lightning channel: three or four big kinks, then fine grit along each run."""
    return G.angular(a, b, rnd, 0.26, 0.05)


def big_bolt(cv, path, w, val, glow=True):
    """One thick channel: a broad glowing body, a white-hot core, tapering slightly at both ends."""
    n = len(path)
    for i, (p, q) in enumerate(zip(path, path[1:])):
        u = i / max(1, n - 2)
        taper = 0.7 + 0.3 * math.sin(math.pi * min(1, u * 1.2))
        cv.dc.line([(p[0] * SS, p[1] * SS), (q[0] * SS, q[1] * SS)], fill=int(val),
                   width=max(1, int(w * taper * SS)))
        cv.db.line([(p[0] * SS, p[1] * SS), (q[0] * SS, q[1] * SS)], fill=int(val * 0.55),
                   width=max(1, int(w * 2.4 * taper * SS)))


def strike_frames(seed):
    rnd = random.Random(seed)
    W = N * SS
    start = (0, SC + rnd.choice((-1, 1)) * rnd.uniform(6, 14))
    channel = streak(start, (SC, SC), rnd)
    stubs = []
    for _ in range(2):
        i = rnd.randrange(len(channel) // 4, 3 * len(channel) // 4)
        p = channel[i]
        a = rnd.uniform(-1.0, 1.0)
        ln = rnd.uniform(8, 16)
        stubs.append(G.angular(p, (p[0] + math.cos(a) * ln, p[1] + math.sin(a) * ln * 0.8), rnd, 0.35, 0.05))
    leaders = []
    for _ in range(3):
        j = rnd.randrange(len(channel) // 5, len(channel) - 3)
        p = channel[j]
        a = rnd.uniform(-1.2, 1.2)
        leaders.append((j, G.angular(p, (p[0] + math.cos(a) * 18, p[1] + math.sin(a) * 14), rnd, 0.4, 0.06)))
    beats = [("leader", 0.5), ("leader", 0.9), ("stroke", 0), ("after", 0), ("dark", 0), ("restrike", 0),
             ("dark", 1), ("restrike", 1), ("after", 1), ("ember", 0), ("ember", 1)]
    out = []
    for t, (beat, k) in enumerate(beats):
        cv = V.Canvas()
        if beat == "leader":                     # 20-100x dimmer than the stroke: a faint branched flicker
            n = int(len(channel) * k)
            cv.tapered(channel[:n], 0.9, 0.7, 70, 90)
            for j, l in leaders:
                if j < n:
                    cv.tapered(l, 0.6, 0.3, 60, 20)
        elif beat == "stroke":                   # the frame that saturates: one channel, white-hot, stubs lit
            big_bolt(cv, channel, 6.0, 255)
            for s in stubs:
                cv.tapered(s, 2.2, 0.3, 230, 90)
            cv.blob(SC, SC, 28, 7, 200)
            cv.blob(SC, SC, 7, 3, 255, 0.3, target="core")
        elif beat == "after":                    # still hot, stubs gone
            big_bolt(cv, channel, 3.6 - 1.2 * k, 200 - 50 * k)
            cv.blob(SC, SC, 18, 5, 120)
        elif beat == "dark":
            cv.tapered(channel, 1.2, 1.2, 55 - 20 * k, 55 - 20 * k)
        elif beat == "restrike":                 # down the same channel, no branches
            big_bolt(cv, channel, 4.8 - 1.0 * k, 245 - 25 * k)
            cv.blob(SC, SC, 20, 5, 150 - 30 * k)
        else:
            r = random.Random(seed + t)
            for _ in range(4):
                cv.blob(SC + r.uniform(-10, 10), SC - r.uniform(2, 10) - 3 * k, 1.1, 1.1, 180 - 60 * k, 0.3,
                        target="core")
        out.append(cv.render(V.plasma(seed, t, W), gains=(1.0, 1.2, 0.8)))
    return out


def quiet_frames(n):
    return [blank() for _ in range(n)]


def caster_frames():
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

    def new_bolt():
        a = rnd.uniform(0, 2 * math.pi)
        end = (SC + math.cos(a) * N * 0.42, feet[1] + math.sin(a) * N * 0.2)
        return [streak((body[0] + rnd.uniform(-2, 2), body[1] + rnd.uniform(2, 10)), end, rnd), 0]
    live = []
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
            if t >= 3:
                crater.draw(cv, 0.15 * (t - 2), 0.8, plates=False)
        else:
            j = t - RELEASE
            if j < 2:
                cv.blob(body[0], body[1], 40 - 10 * j, 32 - 8 * j, 255 - 70 * j, 0.45, target="core")
            for _ in range(3 if j == 0 else (rnd.choice((1, 1, 2)) if j < 9 else 0)):
                live.append(new_bolt())
            for b in live:
                if b[1] == 0:
                    big_bolt(cv, b[0], 5.0, 255)
                elif b[1] == 1:
                    big_bolt(cv, b[0], 2.6, 170)
                elif b[1] == 3:
                    big_bolt(cv, b[0], 3.8, 230)
                b[1] += 1
            live = [b for b in live if b[1] < 4]
            crater.draw(cv, min(1, 0.6 + 0.2 * j), max(0.2, 1 - 0.07 * j))
        light = cv.render(V.plasma(5, t, W), gains=(1.0, 1.2, 0.8))
        light.putalpha(ImageChops.multiply(light.getchannel("A"), EDGE))
        frame = blank()
        if t >= RELEASE:
            frame.alpha_composite(nova[t - RELEASE])
        frame.alpha_composite(light)
        out.append(frame)
    return out


def glow_only(seed):
    """Floor B: the charged glow without a crater (tiles no bolt strikes)."""
    h = c = N / 2
    W = N * SS
    fill = Image.new("L", (W, W), 0)
    ImageDraw.Draw(fill).polygon([(x * SS, y * SS) for x, y in G.hex_pts(c, c, h * 0.96)], fill=255)
    fill = fill.filter(ImageFilter.GaussianBlur(3 * SS))
    out = []
    for t, g in enumerate((0.1, 0.13, 0.14, 0.13, 0.11, 0.09, 0.07, 0.05, 0.03, 0.015)):
        cv = V.Canvas()
        layer = ImageChops.multiply(fill.point(lambda v, g=g: int(v * g)), V.plasma(seed, t, W).point(lambda v: 110 + v * 145 // 255))
        cv.body = ImageChops.lighter(cv.body, layer)
        cv.db = ImageDraw.Draw(cv.body)
        out.append(cv.render(V.plasma(seed + 1, t, W), gains=(1.1, 1.6, 1.3), cap=0.92))
    return out


def clips():
    a = strike_frames(61)
    return {
        "caster": (caster_frames(), C_MS, 3),
        "storm_a": (lead(a, S_LEAD), S_MS, 3),
        "storm_b": (lead(quiet_frames(len(a)), S_LEAD), S_MS, 3),
        "floor_a": (lead(V15.floor_frames(11), F_LEAD), F_MS, 2),
        "floor_b": (lead(glow_only(29), F_LEAD), F_MS, 2),
    }


def main():
    cs = clips()
    for cid, (frs, ms, scale) in cs.items():
        px = frs[0].width
        assert px * len(frs) <= 4096, (cid, px, len(frs))
        fn = os.path.join(HERE, f"anim_fcf_v16_{cid}_{px}.webp")
        b = K.write_strip(frs, fn, px)
        assert b <= 460800, (cid, b)
        print(f"{os.path.basename(fn)}: {len(frs)} frames x {ms} ms, scale {scale}, {px} px "
              f"({px * len(frs)} px tall), {b} bytes")
    return cs


if __name__ == "__main__":
    main()
