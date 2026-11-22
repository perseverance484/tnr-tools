#!/usr/bin/env python3
"""FCF v18d MASTER: v18c with the bolts drawn the way modern anime draws energy (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v18/master_v18d.py

Director: the bolts "should look more like autonomous purple lightning chakra ... Demon Slayer and JJK really know how
to nail these kinds of effects." Techniques taken from those productions and from effects animation write-ups:
- CEL-SHADED SHAPES, not lines: each bolt is a filled, faceted shape in flat tones - a dark violet rim, a magenta-violet
  body, a white-pink core - with the width swelling and pinching along it (hand-drawn effects split into tones; bold
  geometric effect shapes; varied thickness along the bolt).
- COMPOSITED BLOOM WITH HUE SEPARATION (Ufotable's satsuei): the glow is laid over the cel shapes; the whites bloom
  without clipping the shape, and the hue shifts from pink at the core to deep indigo at the edge of the glow.
- LIVING MOTION: each bolt lunges out like a whip on twos - its leading third drawn as a stretched smear shape the
  frame it travels - and the shapes boil (redrawn with small changes every two frames), so the chakra looks alive
  and self-directed rather than a static flash.
- IMPACT FRAME (JJK's Black Flash language): at the release one inverted frame - the area goes near-black and the
  first bolts show as black cores with blazing violet rims - then the colours snap back.
v18c's notes follow.

Director: "I'm just worried it doesn't look like a ninja jutsu using chakra." What reads as a jutsu in the source
material: the user gathers chakra first (it is pulled in, the body flares with a flame-like chakra aura), the release
is a pressure burst from the body (a shockwave and dust kicked off the ground), and the chakra itself is visible in
the attack (lightning chakra is a bolt inside a living, flame-like sheath, not bare electricity). Added to v18b:
- GATHER (350 ms before the release): violet chakra streams pulled in from the area onto the user; the Duelyst gate
  flame (fx_f2_eightgates_purpleflame, CC0) rises round the body and keeps burning through the release.
- RELEASE: a chakra pressure ring races out across the area and a dust ring is blown off the user's tile.
- CHAKRA SHEATH: every bolt carries a turbulent violet flame round its white core (a wide soft layer textured by a
  drifting noise field), so the strikes read as chakra.
v18b's notes follow.

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
sys.path.insert(0, os.path.join(HERE, "..", "v13"))
import build_v13 as V13  # noqa: E402

K = V13.K

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
    pillar = _pillar()
    dust = _dust()
    streams = [(rnd.uniform(0, 2 * math.pi), rnd.uniform(0.6, 1.0), rnd.uniform(-60, 0)) for _ in range(26)]
    for t in range(-350, int(t_end) + 200, STEP_MS):
        night = max(0.0, min(1.0, (t + 350) / 200)) * (1.0 if t < t_end - 150 else max(0, 1 - (t - (t_end - 150)) / 300))
        base = M.frame([], 0, 0, night) if False else None
        base = _board(night, flash=1.0 if first_land <= t < first_land + STEP_MS else 0.0)
        light = Image.new("L", (W * SS, H * SS), 0)
        dl = ImageDraw.Draw(light)
        sheath = Image.new("L", (W * SS, H * SS), 0)
        cel = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
        dc = ImageDraw.Draw(cel)
        invert = 0 <= t < STEP_MS
        dsh = ImageDraw.Draw(sheath)
        # GATHER: chakra streams pulled in onto the user
        if t < 0:
            for ang, rr, off in streams:
                u = (t + 350 + off) / 350
                if not 0 <= u <= 1:
                    continue
                r0 = (1 - u) * rr * TW * 3.0
                r1 = max(0, r0 - TW * 0.5)
                p0 = (SRC[0] + math.cos(ang) * r0, SRC[1] + math.sin(ang) * r0 * 0.62)
                a0 = ang + 1.2 * u
                p0 = (SRC[0] + math.cos(a0) * r0, SRC[1] + math.sin(a0) * r0 * 0.62)
                p1 = (SRC[0] + math.cos(a0 + 0.35) * r1, SRC[1] + math.sin(a0 + 0.35) * r1 * 0.62)
                dsh.line([(p0[0] * SS, p0[1] * SS), (p1[0] * SS, p1[1] * SS)], fill=200, width=int(4 * SS))
                dl.line([(p0[0] * SS, p0[1] * SS), (p1[0] * SS, p1[1] * SS)], fill=150, width=max(1, SS))
            _blob(light, SRC, 8 + (t + 350) / 30, 110 + (t + 350) / 3)
        elif t < 120:
            _blob(light, SRC, 30 - t / 8, 255 - t)
        # RELEASE: the pressure ring
        if 0 <= t < 175:
            u = t / 175
            rx, ry = 12 + u * TW * 3.2, (12 + u * TW * 3.2) * 0.62
            cy = SRC[1] + 0.4 * TH
            dsh.ellipse(((SRC[0] - rx) * SS, (cy - ry) * SS, (SRC[0] + rx) * SS, (cy + ry) * SS), outline=int(220 * (1 - u)),
                        width=int(10 * SS))
            dl.ellipse(((SRC[0] - rx) * SS, (cy - ry) * SS, (SRC[0] + rx) * SS, (cy + ry) * SS), outline=int(200 * (1 - u)),
                       width=int(2 * SS))
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
                dsh.line([(a[0] * SS, a[1] * SS), (b[0] * SS, b[1] * SS)], fill=int(max(0, min(255, v * 0.85))),
                         width=max(1, int((w * 4.5 + 9) * SS)), joint="curve")
            # the cel shapes for this beat: main channel and forks as filled, faceted, three-tone shapes
            boil = random.Random(int(launch * 7) + i)
            mains = [x for x in segs if x[2] == 0]
            forks = [x for x in segs if x[2] == 1]
            if beat in ("shoot", "land", "glow", "re"):
                frac = k if beat == "shoot" else 1.0
                n_on = max(1, int(round(len(mains) * frac)))
                pts = [mains[0][0]] + [x[1] for x in mains[:n_on]]
                pts = [(x + boil.uniform(-0.8, 0.8), y + boil.uniform(-0.8, 0.8)) for x, y in pts]
                base_w = {"shoot": 12.0, "land": 19.0, "glow": 9.0, "re": 15.0 - 3 * k}[beat]
                _cel_bolt(dc, pts, base_w, boil, smear=(beat == "shoot"), invert=invert)
                if beat in ("land", "re") or (beat == "shoot" and k >= 1):
                    for f in forks:
                        fp = [f[0], f[1]]
                        _cel_bolt(dc, fp, base_w * 0.4, boil, invert=invert)
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
        # the user's chakra flame and the dust blown off at the release, under the light
        pi = int((t + 350) / 40)
        if t < 300 and 0 <= pi < len(pillar):
            g = pillar[pi]
            base.alpha_composite(g, (int(M.CX - g.width / 2), int(M.CY - g.height / 2)))
        di = int(t / 50)
        if 0 <= di < len(dust):
            g = dust[di]
            base.alpha_composite(g, (int(M.CX - g.width / 2), int(M.CY + 0.4 * TH - g.height * 0.6)))
        if invert:                                   # the inverted impact frame: the area drops to near-black
            m = Image.new("L", (W, H), 0)
            md = ImageDraw.Draw(m)
            for kk in M.AREA + [M.CASTER]:
                x, y = M.TILES[kk]
                md.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                            (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], fill=255)
            blk = Image.new("RGBA", (W, H), (4, 0, 10, 0))
            blk.putalpha(m.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.9)))
            base = base.copy()
            base.alpha_composite(blk)
        shots.append(_finish(base, light, sheath, t, cel))
    shots[0].save(os.path.join(HERE, "master_fcf_v18d.gif"), save_all=True, append_images=shots[1:],
                  duration=STEP_MS, loop=0, optimize=True)
    times = list(range(-350, int(t_end) + 200, STEP_MS))
    picks = [-250, -75, 25, 100, 200, 330]
    sheet = Image.new("RGB", (W, H * len(picks)))
    for i, x in enumerate(picks):
        j = next(k for k, tt in enumerate(times) if tt >= x)
        sheet.paste(shots[j], (0, i * H))
    sheet.save(os.path.join(HERE, "master_stills_v18d.png"))
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


CHAKRA_RAMP = L.lut([(0.0, (70, 20, 150)), (0.4, (110, 40, 210)), (0.75, (150, 80, 245)), (1.0, (190, 130, 255))])
NOISE = {}


def _noise(t):
    big = NOISE.get(0)
    if big is None:
        big = NOISE[0] = V13.fbm((W * 2, H * 2), 4)
    dx, dy = int(t * 0.35) % W, int(t * 0.2) % H
    return big.crop((dx, dy, dx + W, dy + H))


def _pillar():
    src = K.squared(K.frames("fx_f2_eightgates_purpleflame"))
    top, base_row = 3, 169
    k = 2.6 * TH / (base_row - top)       # a tall chakra flame, well above the head
    s = int(round(src[0].width * k))
    side = int(TH * 4)
    out = []
    for f in list(src[1:11]) + list(src[23:31]) * 1:
        cv = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        g = f.resize((s, s), Image.LANCZOS)
        cv.paste(g, (int(side / 2 - s / 2), int(side / 2 + 0.4 * TH - base_row * k)), g)
        out.append(cv)
    return out


def _dust():
    from PIL import ImageOps
    src = K.squared(K.frames("fx_smoke2"))
    out = []
    for f in src:
        g = ImageOps.grayscale(f.convert("RGB"))
        im = Image.merge("RGB", [g.point(lambda v, c=c: int(c * (0.45 + 0.55 * v / 255))) for c in (110, 92, 140)])
        im = im.convert("RGBA")
        im.putalpha(f.getchannel("A").point(lambda a: int(a * 0.6)))
        out.append(im.resize((int(TW * 2.2), int(TW * 2.2)), Image.LANCZOS))
    return out


RIM, BODY, CORE = (58, 8, 118, 255), (186, 92, 255, 255), (255, 232, 255, 255)


def _cel_bolt(dc, pts, w, rnd, smear=False, invert=False):
    """A bolt as a filled, faceted shape in three flat tones; width swells and pinches; tapers to a point at the tip.
    smear: the leading third stretched wider, the frame it travels. invert: black core, blazing rim (impact frame)."""
    if len(pts) < 2:
        return
    n = len(pts)
    widths = []
    for j in range(n):
        u = j / (n - 1)
        swell = 0.75 + 0.35 * rnd.random()               # facets: each joint its own width
        tip = 0.35 + 0.65 * (1 - u) ** 0.8
        sm = 1.6 if smear and u > 0.66 else 1.0
        widths.append(max(0.4, w * swell * tip * sm))
    import ground_hd as G
    ss = M.SS
    def poly(scale):
        return [(x * ss, y * ss) for x, y in G.fissure_poly(pts, [x * scale for x in widths])]
    rim, body, core = (BODY, (20, 0, 40, 255), (10, 0, 20, 255)) if invert else (RIM, BODY, CORE)
    old = G.SS
    G.SS = 1
    try:
        dc.polygon(poly(1.0), fill=rim)
        dc.polygon(poly(0.62), fill=body)
        dc.polygon(poly(0.26), fill=core)
    finally:
        G.SS = old


HUE_RAMP = L.lut([(0.0, (60, 20, 170)), (0.35, (120, 50, 235)), (0.65, (200, 110, 255)), (0.85, (245, 180, 255)),
                  (1.0, (255, 240, 255))])


def _finish(base, light, sheath=None, t=0, cel=None):
    if sheath is not None:
        # the chakra sheath: soft, turbulent, darker violet flame round every bolt
        sh = sheath.filter(ImageFilter.GaussianBlur(3 * SS)).resize((W, H), Image.LANCZOS)
        sh = ImageChops.multiply(sh.point(lambda v: min(255, int(v * 1.4))), _noise(t).point(lambda v: max(0, (v - 70) * 255 // 185)))
        rgb = Image.merge("RGB", [sh.point([c[i] for c in CHAKRA_RAMP]) for i in range(3)])
        layer = rgb.convert("RGBA")
        layer.putalpha(sh.point(lambda v: min(255, int(v * 0.85))))
        base = base.copy()
        base.alpha_composite(layer)
    if cel is not None:
        # bloom laid over the cel shapes (whites bloom, the shape keeps its edges), hue-separated
        cel_small = cel.resize((W, H), Image.LANCZOS)
        lum = cel_small.convert("L")
        lum = ImageChops.multiply(lum, cel_small.getchannel("A"))
        g1 = lum.filter(ImageFilter.GaussianBlur(4)).point(lambda v: min(255, int(v * 1.4)))
        g2 = lum.filter(ImageFilter.GaussianBlur(14)).point(lambda v: min(255, int(v * 1.1)))
        glow = ImageChops.lighter(g1, g2)
        rgb = Image.merge("RGB", [glow.point([c[i] for c in HUE_RAMP]) for i in range(3)])
        gl = rgb.convert("RGBA")
        gl.putalpha(glow.point(lambda v: min(255, int(255 * (v / 255) ** 0.8))))
        base = base.copy()
        base.alpha_composite(gl)
        base.alpha_composite(cel_small)
        light = light.point(lambda v: v * 2 // 3)  # the line light adds the hot halo round the shapes
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
