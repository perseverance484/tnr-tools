#!/usr/bin/env python3
"""Celestial Dew animations from the art director's layers (raws/anim_cd_*.png), the Ethereal Rebirth method.

    python3 art/jutsu_icons/celestial_dew/animation/build_strip.py [--only appear|loop|break]

Three strips, one clock (36 ms per frame, 112 px frames), all on the SHIELD effect (director, 2026-10-24: "Have cast and
ward form both start from shield appear so they can be timed correctly"):
- appear (shield appearAnimation, 66 frames): a small upright moon appears on top of the head; a drop of starlight swells
  at its lower horn and falls into the portrait's centre; it splashes, ripples run out, and where they hit the rim it
  charges into the ward ring (nothing of the ward before); the moon fades.
- loop (shield staticAnimation, 100 frames, seamless): the ward ring, faint, a brighter arc travelling round it, stars
  twinkling. The game starts it on the cast's tick, so it is kept to a whisper.
- break (shield disappearAnimation, 30 frames): the ring flashes and breaks into curved shards that drift out and fade.
Pillow only.
"""
import argparse
import importlib.util
import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
DOCS = os.path.join(ROOT, 'docs', 'design', 'celestial_dew_animation')
_spec = importlib.util.spec_from_file_location(
    'er', os.path.join(ROOT, 'art', 'jutsu_icons', 'ethereal_rebirth', 'animation', 'build_strip.py'))
er = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(er)
S, PCY = er.S, er.PORTRAIT_CY            # working size; portrait centre (measured from the director's recording)
ease, seg, smooth = er.ease, er.seg, er.smooth
BEHIND_MASK, EDGE_FADE = er.BEHIND_MASK, er.EDGE_FADE

# Slower (director, 2026-10-24: "it plays way too fast"). Frame times per strip; the appear and the loop start on one
# tick, and the loop's first glow peak lands when the ripples reach the rim: IGNITE * MS['appear'] = LOOP_N * MS['loop'] / 2.
MS = {'appear': 46, 'loop': 72, 'break': 46}
CAST_N, LOOP_N, BREAK_N, SIZE = 74, 64, 30, 112
IMPACT = 30          # the drop lands (1.38 s)
IGNITE = 50          # the ripples reach the rim (2.30 s): the ward's first glow peak
LOOP_PEAK = 0.95     # the ward's glow at its brightest
RING_INNER = 0.215   # the ward band's inner edge, as a frame radius: it sits over the portrait's white rim
W1_INNER = 390 / 1254  # the band's inner edge in the W1 art (measured), as a fraction of its canvas
R1_OUTER = 536 / 1254  # the R1 art's outer crest radius, as a fraction of its canvas width (measured)


def raw(name, crop=True):
    im = Image.open(os.path.join(HERE, 'raws', f'anim_cd_{name}.png')).convert('RGBA')
    if crop:   # the two ring layers keep their full canvas: their measured radii are fractions of it
        im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
    # tame the painted halo a little (it is wide and saturated; at 50 px it would swallow the shapes)
    im.putalpha(im.getchannel('A').point(lambda v: int(255 * (v / 255) ** 1.25)))
    return im


def put(layer, img, cx, cy, width, alpha=1.0, rot=0.0):
    """Composite img centred at (cx, cy) (frame fractions), `width` frame-widths wide, rotated `rot` degrees
    counter-clockwise, at `alpha`."""
    if alpha <= 0.01 or width <= 0:
        return
    w = max(2, int(width * S))
    h = max(2, int(w * img.height / img.width))
    im = img.resize((w, h), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        im.putalpha(im.getchannel('A').point(lambda v, a=alpha: int(v * a)))
    layer.alpha_composite(im, (int(cx * S - im.width / 2), int(cy * S - im.height / 2)))


def ring_width():
    """W1 drawn at this width puts its band's inner edge at RING_INNER."""
    return 2 * RING_INNER / (2 * W1_INNER)


def wedge_mask(a0, span, soft=18):
    """An angular wedge mask round the portrait centre (degrees, clockwise from 3 o'clock), soft-edged."""
    m = Image.new('L', (S, S), 0)
    d = ImageDraw.Draw(m)
    for i in range(soft, 0, -1):
        k = i / soft
        d.pieslice([0.5 * S - S, PCY * S - S, 0.5 * S + S, PCY * S + S], a0 - span / 2 * k, a0 + span / 2 * k,
                   fill=int(255 * (1 - k) + 40 * k))
    return m.filter(ImageFilter.GaussianBlur(4))


def finish(back, front, top=None):
    def glowed(layer):
        g = layer.filter(ImageFilter.GaussianBlur(S * 0.008))
        g.putalpha(g.getchannel('A').point(lambda v: int(v * 0.4)))
        return Image.alpha_composite(g, layer)
    back = glowed(back)
    back.putalpha(ImageChops.multiply(back.getchannel('A'), BEHIND_MASK))
    out = Image.alpha_composite(back, glowed(front))
    if top is not None:
        out = Image.alpha_composite(out, top)
    out.putalpha(ImageChops.multiply(out.getchannel('A'), EDGE_FADE))
    return out.resize((SIZE, SIZE), Image.LANCZOS)


L = {}


def layers():
    if not L:
        for k in ('M1_crescent', 'D1_drop', 'S1_splash'):
            L[k] = raw(k)
        for k in ('R1_ripples', 'W1_ward_ring'):
            L[k] = raw(k, crop=False)
        L['glints'] = er.flecks_from(raw('P1_glints'))
        L['shards'] = er.flecks_from(raw('X1_shards'))
    return L


# The moon (director, 2026-10-24: "a much smaller moon ... oriented directly above the player portrait like we did for
# the chakra overflow rising star"): upright as in the icon (a C opening to the right), about a fifth of the frame tall,
# on top of the head (Chakra Overflow's crown star sits at 0.075 of the frame from the top, about 0.24 tall). It is
# placed so its lower horn's tip is directly above the portrait's centre: the drop falls from it straight down.
MOON_H, MOON_Y = 0.20, 0.105


def _moon_place():
    """(centre x, centre y, width) of the moon, and its lower horn tip."""
    m = layers()['M1_crescent']
    w = MOON_H * m.width / m.height
    lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    put(lay, m, 0.5, MOON_Y, w)
    a = lay.getchannel('A').load()
    best, tip = -9, (0.55, MOON_Y + 0.08)
    for y in range(S // 2):
        for x in range(S):
            if a[x, y] > 200 and y / S + 0.5 * x / S > best:     # the lowest, right-most bright point: the lower horn
                best, tip = y / S + 0.5 * x / S, (x / S, y / S)
    dx = 0.5 - tip[0]
    return (0.5 + dx, MOON_Y, w), (0.5, tip[1])


def appear_frames():
    """The shield's appearAnimation: the whole cast on one clock (director: "Have cast and ward form both start from
    shield appear so they can be timed correctly"). Moon appears, the drop falls from its horn into the portrait's centre
    and splashes, ripples run out and, reaching the rim, charge it into the ward; the moon fades."""
    Lr = layers()
    (mx, my, mw), horn = _moon_place()
    rnd = random.Random(3)
    thrown = [dict(img=Lr['glints'][i % len(Lr['glints'])], ang=-math.pi / 2 + rnd.uniform(-1.3, 1.3),
                   v=rnd.uniform(0.008, 0.013), s=rnd.uniform(0.035, 0.06)) for i in range(6)]
    out = []
    for f in range(CAST_N):
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        top = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        # 1. the moon appears above the head, glints, then fades upward once the ward has formed
        bloom = ease(seg(f, 0, 14))
        gone = ease(seg(f, IGNITE - 4, IGNITE + 18))
        if bloom > 0 and gone < 1:
            put(top, Lr['M1_crescent'], mx, my - 0.03 * gone, mw * (0.8 + 0.2 * bloom), bloom * (1 - gone))
        tw = math.sin(math.pi * seg(f, 6, 20))
        if tw > 0:
            put(top, Lr['glints'][1], mx - mw * 0.30, my - MOON_H * 0.30, 0.05 * tw, tw)
        # 2. the drop swells at the lower horn, then falls straight into the portrait's centre, accelerating
        if 12 <= f < IMPACT:
            sw = ease(seg(f, 12, 20))
            q = seg(f, 20, IMPACT) ** 2
            y = horn[1] + 0.02 + (PCY - horn[1] - 0.02) * q
            put(top, Lr['D1_drop'], 0.5, y, 0.07 * (0.4 + 0.6 * sw), 1.0)
        # 3. the splash at the centre, a flash, glints thrown up
        if IMPACT <= f < IMPACT + 15:
            p = seg(f, IMPACT, IMPACT + 15)
            put(front, Lr['S1_splash'], 0.5, PCY - 0.02, 0.30 * (0.6 + 0.4 * ease(min(1, p * 3))), 0.85 * (1 - ease(p)))
        fl = ease(seg(f, IMPACT - 1, IMPACT + 1)) * (1 - ease(seg(f, IMPACT + 1, IMPACT + 7)))
        if fl > 0:
            g = Image.new('L', (S, S), 0)
            ImageDraw.Draw(g).ellipse([0.5 * S - 0.06 * S, PCY * S - 0.06 * S, 0.5 * S + 0.06 * S, PCY * S + 0.06 * S], fill=255)
            g = g.filter(ImageFilter.GaussianBlur(S * 0.025)).point(lambda v, a=fl: int(v * a))
            top.alpha_composite(Image.merge('RGBA', (Image.new('L', (S, S), 240), Image.new('L', (S, S), 248), Image.new('L', (S, S), 255), g)))
        for d in thrown:
            p = seg(f, IMPACT, IMPACT + 22)
            if 0 < p < 1:
                tt = p * 22
                put(front, d['img'], 0.5 + math.cos(d['ang']) * d['v'] * tt,
                    PCY + math.sin(d['ang']) * d['v'] * tt + 0.0005 * tt * tt, d['s'] * (1 - 0.4 * p), 1 - ease(p))
        # 4. ripples run out across the portrait; the outer one reaches the rim exactly at IGNITE
        for k, (f0, f1) in enumerate(((IMPACT + 1, IGNITE), (IMPACT + 6, IGNITE + 5))):
            p = seg(f, f0, f1)
            if 0 < p < 1:
                r_out = 0.03 + (0.272 - 0.03) * p ** 0.8           # steady outward run, a touch faster at first
                put(front, Lr['R1_ripples'], 0.5, PCY, r_out / R1_OUTER, 0.6 * (1 - p ** 4))
        # 5. where the ripples hit the rim, sparks: the ward itself is the loop (shield static), whose glow peaks now
        for k in range(8):
            p = seg(f, IGNITE - 1 + (k % 3), IGNITE + 11 + (k % 3))
            if 0 < p < 1:
                ang = math.radians(22.5 + 45 * k)
                r = RING_INNER + 0.04 + 0.02 * p
                q = math.sin(math.pi * p)
                put(top, Lr['glints'][(k * 2 + 1) % len(Lr['glints'])], 0.5 + r * math.cos(ang), PCY + r * math.sin(ang),
                    0.05 * (0.5 + 0.5 * q), q)
        out.append(finish(Image.new('RGBA', (S, S), (0, 0, 0, 0)), front, top))
    return out


def ring_layer(f_clock, alpha):
    """The ward ring at loop phase f_clock (turns once per LOOP_N frames), at alpha."""
    lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    # the ring itself holds still (a turning texture changes every pixel and costs about 3x the bytes); the light
    # travelling round it and the stars carry the motion
    put(lay, layers()['W1_ward_ring'], 0.5, PCY, ring_width(), alpha)
    return lay


def loop_frames():
    """The ward glowing (director, 2026-10-24: "Have the shields loop be the ward glowing, like fading in and out ...
    timed to when the drops flow outward and power up the shield the first time"). The game starts it on the appear's
    tick, so it starts dark (nothing of the ward before the ripples), rises as they run out, peaks when they reach the rim
    (half a loop = IGNITE on the appear's clock), then fades out and breathes again: one slow breath per loop."""
    Lr = layers()
    out = []
    for f in range(LOOP_N):
        t = f / LOOP_N
        # dark until the ripples are most of the way out, a quick rise to the peak as they reach the rim (t = 0.5),
        # then a long, slow fade back to dark at the seam
        a = LOOP_PEAK * (ease(seg(t, 0.40, 0.5)) if t < 0.5 else 0.5 + 0.5 * math.cos(math.pi * (t - 0.5) / 0.5))
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        front.alpha_composite(ring_layer(f, a))
        for ang, ph in ((300, 0.44), (140, 0.50), (40, 0.56)):            # a few stars wink near each peak
            q = max(0.0, 1 - abs(t - ph) / 0.08)
            if q > 0:
                r = RING_INNER + 0.035
                put(front, Lr['glints'][1], 0.5 + r * math.cos(math.radians(ang)), PCY + r * math.sin(math.radians(ang)),
                    0.05 * (0.5 + 0.5 * q), 0.9 * q)
        out.append(finish(Image.new('RGBA', (S, S), (0, 0, 0, 0)), front))
    return out


def ward_parts(f):
    """The ward forming at IGNITE (front, top layers): the rim ignites as the ripples arrive, flares, a light runs once
    round it, a sheen washes the portrait, glints spark; then it fades over the loop's copy."""
    Lr = layers()
    if True:
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        top = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        # the ring ignites as the ripples reach the rim, flares, then fades over the loop's copy (same turn angle)
        a = ease(seg(f, IGNITE - 2, IGNITE + 2)) * (1 - ease(seg(f, IGNITE + 3, CAST_N - 3)))
        if a > 0:
            front.alpha_composite(ring_layer(f, min(1.0, a)))
        # a light runs once round the ring
        p = seg(f, IGNITE, IGNITE + 14)
        if 0 < p < 1:
            arc = ring_layer(f, 1.0)
            arc.putalpha(ImageChops.multiply(arc.getchannel('A'), wedge_mask(90 + 360 * ease(p), 80)))
            arc.putalpha(arc.getchannel('A').point(lambda v, k=1 - p: int(v * k)))
            top.alpha_composite(arc)
        # a faint glassy sheen washes over the portrait as it is energised
        sh = ease(seg(f, IGNITE, IGNITE + 3)) * (1 - ease(seg(f, IGNITE + 3, IGNITE + 14)))
        if sh > 0:
            g = Image.new('L', (S, S), 0)
            r = (RING_INNER + 0.01) * S
            ImageDraw.Draw(g).ellipse([0.5 * S - r, PCY * S - r, 0.5 * S + r, PCY * S + r], fill=int(70 * sh))
            g = g.filter(ImageFilter.GaussianBlur(S * 0.02))
            front.alpha_composite(Image.merge('RGBA', (Image.new('L', (S, S), 200), Image.new('L', (S, S), 225), Image.new('L', (S, S), 255), g)))
        # glints spark round the rim
        for k in range(6):
            p = seg(f, IGNITE + k, IGNITE + k + 10)
            if 0 < p < 1:
                ang = math.radians(30 + 60 * k)
                r = RING_INNER + 0.04
                q = math.sin(math.pi * p)
                put(top, Lr['glints'][(k * 2 + 1) % len(Lr['glints'])], 0.5 + r * math.cos(ang), PCY + r * math.sin(ang),
                    0.055 * (0.5 + 0.5 * q), q)
    return front, top


def break_frames():
    Lr = layers()
    shards = Lr['shards']
    rnd = random.Random(9)
    pieces = [dict(img=shards[i % len(shards)], ang=2 * math.pi * i / 9 + rnd.uniform(-0.15, 0.15),
                   spin=rnd.uniform(-40, 40), v=rnd.uniform(0.004, 0.007)) for i in range(9)]
    out = []
    for f in range(BREAK_N):
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        top = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        # the ring, at the loop's strength, flashes and is gone
        a = (0.5 + 0.5 * ease(seg(f, 0, 2))) * (1 - ease(seg(f, 2, 6)))
        if a > 0:
            front.alpha_composite(ring_layer(0, a))
        # curved shards spring from the ring, drift outward, turn and fade
        for d in pieces:
            p = seg(f, 2, BREAK_N - 2)
            if 0 < p < 1:
                tt = p * (BREAK_N - 4)
                r = RING_INNER + 0.035 + d['v'] * tt
                x, y = 0.5 + r * math.cos(d['ang']), PCY + r * math.sin(d['ang']) + 0.0006 * tt * tt
                tangent = -math.degrees(d['ang']) - 90
                put(front, d['img'], x, y, 0.09 * (1 - 0.3 * p), (1 - ease(p)) * min(1, f / 3), tangent + d['spin'] * p)
        # stardust rises
        for k in range(5):
            p = seg(f, 3 + k, 3 + k + 16)
            if 0 < p < 1:
                ang = math.radians(200 + 35 * k)
                r = RING_INNER + 0.05
                put(top, Lr['glints'][(2 * k) % len(Lr['glints'])], 0.5 + r * math.cos(ang), PCY + r * math.sin(ang) - 0.12 * p,
                    0.045, math.sin(math.pi * p))
        out.append(finish(Image.new('RGBA', (S, S), (0, 0, 0, 0)), front, top))
    return out


def save_strip(frames, name):
    strip = Image.new('RGBA', (SIZE, SIZE * len(frames)), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        strip.paste(fr, (0, SIZE * i))
    strip.putalpha(strip.getchannel('A').point(lambda v: 0 if v < 4 else v))
    os.makedirs(os.path.join(HERE, 'exports'), exist_ok=True)
    p = os.path.join(HERE, 'exports', f'anim_celestial_dew_{name}.webp')
    strip.save(p, lossless=True, method=6)
    ms = MS[name.split('_')[0]]
    print(f'{name}: {len(frames)} frames of {SIZE} px at {ms} ms = {len(frames) * ms / 1000:.2f} s, {os.path.getsize(p)} bytes (ceiling 460800)')


BUILDERS = {'appear': appear_frames, 'loop': loop_frames, 'break': break_frames}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', choices=list(BUILDERS))
    a = ap.parse_args()
    for name, fn in BUILDERS.items():
        if a.only in (None, name):
            save_strip(fn(), f'{name}_v3')
