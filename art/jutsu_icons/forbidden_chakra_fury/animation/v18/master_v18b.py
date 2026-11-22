#!/usr/bin/env python3
"""FCF v18b MASTER: an anime chakra lightning storm, drawn whole in board space first (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v18/master_v18b.py

Director on v18: "It does need to strike those empty areas as well ... more big bolts less small, they don't all have
to strike at the same time, it can be spaced out over a couple hundred ms. Try for an anime type lightning storm of
chakra."
- Twelve big bolts leave the user, spread evenly round the circle so the whole area is struck, each launching at its
  own moment inside ~250 ms.
- Anime bolt shape: long straight runs with sharp kinks (big steps, hard turns pulled outward), a fat white core,
  few forks (two to four per bolt, one level, short) instead of a fine tree.
- Each bolt has its own life: it shoots out in two frames, lands white-hot (its impact frame), drops to an afterglow,
  restrikes once or twice down the same channel, dies. A chakra spark spray where it ends.
- Anime impact frame: when the first bolts land, the darkened area flashes violet-white for one frame.
- The area darkens like a night sky; the user's body flares at the release.
Writes master_fcf_v18b.gif and master_stills_v18b.png.
"""
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import master_v18 as M  # noqa: E402

L = M.L
W, H, TW, TH, SRC, SS = M.W, M.H, M.TW, M.TH, M.SRC, M.SS
STEP_MS = 25


def bolt_tree(rnd, ang0):
    """One anime bolt: segments (a, b, gen, along) from the body outward to the area's edge, with a few forks."""
    segs = []
    tips = [(SRC, ang0, 0, 0.0)]
    while tips:
        p, ang, gen, along = tips.pop()
        step = TH * (0.62 if gen == 0 else 0.42)
        life = 40 if gen == 0 else rnd.randrange(2, 5)
        for _ in range(life):
            out = math.atan2((p[1] - SRC[1]) / 0.62, p[0] - SRC[0]) if along > 0 else ang
            d_ang = (out - ang + math.pi) % (2 * math.pi) - math.pi
            ang += rnd.choice((-1, 1)) * rnd.uniform(0.25, 0.7) + 0.55 * d_ang     # hard kinks, pulled outward
            q = (p[0] + math.cos(ang) * step * rnd.uniform(0.7, 1.3), p[1] + math.sin(ang) * step * 0.62 * rnd.uniform(0.7, 1.3))
            if not M.in_area(q):
                break
            segs.append((p, q, gen, along))
            along += 1
            if gen == 0 and along > 2 and rnd.random() < 0.2 and sum(1 for s in segs if s[2] == 1) < 8:
                tips.append((q, ang + rnd.choice((-1, 1)) * rnd.uniform(0.5, 1.0), 1, along))
            p = q
    return segs


def main(seed=21):
    rnd = random.Random(seed)
    n = 12
    bolts = []
    for k in range(n):
        ang = k * 2 * math.pi / n + rnd.uniform(-0.18, 0.18)
        launch = rnd.uniform(0, 260)
        bolts.append((launch, bolt_tree(rnd, ang), rnd.random() < 0.5))
    # coverage: every one of eight sectors round the user gets a bolt that ends far out in it
    def end_of(segs):
        main = [x for x in segs if x[2] == 0]
        return main[-1][1] if main else SRC

    def sector(p):
        a = math.atan2(p[1] - SRC[1], p[0] - SRC[0])      # on screen, as the player sees the corners
        return int(((a + math.pi / 8) % (2 * math.pi)) // (math.pi / 4))

    def reach(p):
        return math.hypot(p[0] - SRC[0], (p[1] - SRC[1]) / 0.62)
    far = 0.6 * max(reach(end_of(b[1])) for b in bolts)
    for sec in (7, 3, 1, 5, 0, 2, 4, 6):   # the diagonals first: top-right, bottom-left, ...
        if any(sector(end_of(b[1])) == sec and reach(end_of(b[1])) >= far for b in bolts):
            continue
        for _ in range(40):                      # aim at the sector until a bolt makes it out
            segs = bolt_tree(rnd, sec * math.pi / 4 + rnd.uniform(-0.25, 0.25))
            e = end_of(segs)
            if sector(e) == sec and reach(e) >= far:
                bolts.append((rnd.uniform(40, 260), segs, rnd.random() < 0.5))
                break
    first_land = min(b[0] for b in bolts) + 2 * STEP_MS * 2
    t_end = max(b[0] for b in bolts) + 520
    shots = []
    for t in range(-150, int(t_end) + 200, STEP_MS):
        night = max(0.0, min(1.0, (t + 150) / 150)) * (1.0 if t < t_end - 150 else max(0, 1 - (t - (t_end - 150)) / 300))
        base = M.frame([], 0, 0, night) if False else None
        base = _board(night, flash=1.0 if first_land <= t < first_land + STEP_MS else 0.0)
        light = Image.new("L", (W * SS, H * SS), 0)
        dl = ImageDraw.Draw(light)
        # the user's body: charge before, flare at the release
        if t < 0:
            _blob(light, SRC, 10 + (t + 150) / 15, 160 + (t + 150) / 2)
        elif t < 120:
            _blob(light, SRC, 30 - t / 8, 255 - t)
        for launch, segs, two in bolts:
            ph = t - launch
            if ph < 0 or not segs:
                continue
            nmax = max(s[3] for s in segs) + 1
            beats = [("shoot", 0.5), ("shoot", 1.0), ("land", 0), ("glow", 0), ("dark", 0), ("re", 0), ("glow", 1)]
            beats += [("dark", 1), ("re", 1), ("die", 0)] if two else [("die", 0), ("die", 1)]
            i = int(ph // (STEP_MS * 2))           # each beat holds two 25 ms steps (anime on twos)
            if i >= len(beats):
                continue
            beat, k = beats[i]

            def line(seg, w, v):
                (a, b, gen, along) = seg
                dl.line([(a[0] * SS, a[1] * SS), (b[0] * SS, b[1] * SS)], fill=int(max(0, min(255, v))),
                        width=max(1, int(w * SS)), joint="curve")
            for seg in segs:
                gen, along = seg[2], seg[3]
                taper = 1 - 0.55 * along / nmax
                if beat == "shoot":
                    if along <= nmax * k:
                        line(seg, (4.6 if gen == 0 else 1.6) * taper, 235 if gen == 0 else 170)
                elif beat == "land":
                    line(seg, (8.0 if gen == 0 else 2.6) * taper, 255)
                elif beat == "glow":
                    if gen == 0:
                        line(seg, 3.6 * taper, 180 - 40 * k)
                elif beat == "dark":
                    if gen == 0:
                        line(seg, 1.4, 55)
                elif beat == "re":
                    if gen == 0:
                        line(seg, (6.4 - 1.2 * k) * taper, 250 - 20 * k)
                else:
                    if gen == 0:
                        line(seg, 1.0, 50 - 25 * k)
            end = segs[max(range(len(segs)), key=lambda j: segs[j][3] if segs[j][2] == 0 else -1)][1]
            if beat in ("land", "re"):                  # a spark spray where the bolt ends
                r2 = random.Random(int(launch * 10) + i)
                for _ in range(10):
                    a = r2.uniform(0, 2 * math.pi)
                    ln = r2.uniform(6, 16)
                    dl.line([(end[0] * SS, end[1] * SS), ((end[0] + math.cos(a) * ln) * SS,
                             (end[1] + math.sin(a) * ln * 0.6) * SS)], fill=170, width=max(1, int(0.7 * SS)))
        shots.append(_finish(base, light))
    shots[0].save(os.path.join(HERE, "master_fcf_v18b.gif"), save_all=True, append_images=shots[1:],
                  duration=STEP_MS, loop=0, optimize=True)
    times = list(range(-150, int(t_end) + 200, STEP_MS))
    picks = [0, 60, 120, 180, 260, 380]
    sheet = Image.new("RGB", (W, H * len(picks)))
    for i, x in enumerate(picks):
        j = next(k for k, tt in enumerate(times) if tt >= x)
        sheet.paste(shots[j], (0, i * H))
    sheet.save(os.path.join(HERE, "master_stills_v18b.png"))
    print(len(shots), "frames")


def _blob(light, p, r, v):
    layer = Image.new("L", light.size, 0)
    ImageDraw.Draw(layer).ellipse(((p[0] - r) * SS, (p[1] - r * 0.8) * SS, (p[0] + r) * SS, (p[1] + r * 0.8) * SS),
                                  fill=int(max(0, min(255, v))))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.5 * SS))
    light.paste(ImageChops.lighter(light, layer))


def _board(night, flash=0.0):
    im = M.frame([type("S", (), {"weight": 1})()], 0, 1, night) if False else None
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
    if night or flash:
        m = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(m)
        for k in M.AREA + [M.CASTER]:
            x, y = M.TILES[k]
            md.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                        (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(8))
        if night:
            dark = Image.new("RGBA", (W, H), (10, 6, 22, 0))
            dark.putalpha(m.point(lambda v: int(v * night * 0.66)))
            base.alpha_composite(dark)
        if flash:
            fl = Image.new("RGBA", (W, H), (200, 160, 255, 0))
            fl.putalpha(m.point(lambda v: int(v * 0.45 * flash)))
            base.alpha_composite(fl)
    return base


def _finish(base, light):
    tight = light.filter(ImageFilter.GaussianBlur(1.6 * SS)).point(lambda v: min(255, int(v * 1.7)))
    mid = light.filter(ImageFilter.GaussianBlur(5 * SS)).point(lambda v: min(255, int(v * 1.5)))
    wide = light.filter(ImageFilter.GaussianBlur(15 * SS)).point(lambda v: min(255, int(v * 1.25)))
    inten = ImageChops.lighter(ImageChops.lighter(light, tight), ImageChops.lighter(mid, wide)).resize((W, H), Image.LANCZOS)
    rgb = Image.merge("RGB", [inten.point([c[i] for c in L.STORM_LUT]) for i in range(3)])
    alpha = inten.point(lambda v: min(255, int(255 * (v / 255) ** 0.75 * 1.1)))
    lt = rgb.convert("RGBA")
    lt.putalpha(alpha)
    out = base.copy()
    out.alpha_composite(lt)
    return out.convert("RGB")


if __name__ == "__main__":
    main()
