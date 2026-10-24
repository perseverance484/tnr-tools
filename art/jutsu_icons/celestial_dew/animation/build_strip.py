#!/usr/bin/env python3
"""Celestial Dew animations from the art director's layers (raws/anim_cd_*.png), the Ethereal Rebirth method.

    python3 art/jutsu_icons/celestial_dew/animation/build_strip.py [--only cast|ward|loop|break]

Four strips, one clock (36 ms per frame, 112 px frames; the game starts the heal's and the shield's animations in one
pass, and the shield's static loop on the same tick):
- cast  (heal appearAnimation, 66 frames): the crescent rises behind the portrait, a drop of starlight swells at its upper
  horn and falls into the portrait's centre, splashes, and ripples run out to the rim.
- ward  (shield appearAnimation, 66 frames): as the ripples reach the rim it ignites into the ward ring, flares, a light
  runs once round it, then it settles into the loop.
- loop  (shield staticAnimation, 100 frames, seamless): the ward ring, faint, turning once per loop, a brighter arc
  travelling round it, stars twinkling.
- break (shield disappearAnimation, 30 frames): the ring flashes and breaks into curved shards that drift out and fade.
Director's motion, 2026-10-24: "a drop falls into the middle of the portrait, splashes and then ripples flow outward and
hit the edges of the portrait and energize it with a celestial shield". Pillow only.
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

MS, CAST_N, LOOP_N, BREAK_N, SIZE = 36, 66, 100, 30, 112
IMPACT = 24          # the drop lands (0.86 s)
IGNITE = 38          # the ripples reach the rim (1.37 s)
RING_INNER = 0.215   # the ward band's inner edge, as a frame radius: it sits over the portrait's white rim
W1_INNER = 390 / 1254  # the band's inner edge in the W1 art (measured), as a fraction of its canvas
LOOP_ALPHA = 0.30
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


# the crescent rises behind the portrait (the portrait reaches the top of the effect square, so there is no room above
# it): a C opening to the upper right, its band outside the portrait on the left, its upper horn clear at the top right
# turned so its band arcs behind the upper left of the head like a halo and its upper horn stands at the top right
CRES_C, CRES_W, CRES_ROT, CRES_A = (0.42, 0.24), 0.80, -45, 0.85


def _horn():
    """The upper horn's tip as placed (the bright pixel furthest towards the upper right): where the drop forms."""
    lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    put(lay, layers()['M1_crescent'], CRES_C[0], CRES_C[1], CRES_W, 1.0, CRES_ROT)
    a = lay.getchannel('A').load()
    best, pt = -9, (0.75, 0.08)
    for y in range(0, S, 2):
        for x in range(0, S, 2):
            if a[x, y] > 200:
                v = x / S - 1.6 * y / S
                if v > best:
                    best, pt = v, (x / S, y / S)
    return pt


def cast_frames():
    Lr = layers()
    HORN = _horn()
    rnd = random.Random(3)
    thrown = [dict(img=Lr['glints'][i % len(Lr['glints'])], ang=-math.pi / 2 + rnd.uniform(-1.3, 1.3),
                   v=rnd.uniform(0.010, 0.016), s=rnd.uniform(0.04, 0.07)) for i in range(7)]
    out = []
    for f in range(CAST_N):
        back = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        top = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        # 1. the crescent blooms behind the head, holds, then drifts up and fades
        bloom = ease(seg(f, 0, 12))
        gone = ease(seg(f, 44, 62))
        if bloom > 0 and gone < 1:
            put(back, Lr['M1_crescent'], CRES_C[0], CRES_C[1] - 0.04 * gone, CRES_W * (0.86 + 0.14 * bloom),
                CRES_A * bloom * (1 - gone), CRES_ROT - 8 * (1 - bloom))
        # 2. the drop swells at the horn, then falls into the portrait's centre, accelerating
        if 10 <= f < IMPACT:
            sw = ease(seg(f, 10, 15))
            q = seg(f, 15, IMPACT) ** 2
            x = HORN[0] + (0.5 - HORN[0]) * q
            y = HORN[1] + (PCY + 0.01 - HORN[1]) * q
            ang = math.degrees(math.atan2(0.5 - HORN[0], PCY - HORN[1]))   # point back along the fall
            put(top, Lr['D1_drop'], x, y, 0.10 * (0.4 + 0.6 * sw), 1.0, -ang if q > 0 else 0)
        # 3. the splash at the centre, a flash, glints thrown up
        if IMPACT <= f < IMPACT + 12:
            p = seg(f, IMPACT, IMPACT + 12)
            put(front, Lr['S1_splash'], 0.5, PCY - 0.02, 0.34 * (0.6 + 0.4 * ease(min(1, p * 3))), 0.9 * (1 - ease(p)))
        fl = ease(seg(f, IMPACT - 1, IMPACT + 1)) * (1 - ease(seg(f, IMPACT + 1, IMPACT + 5)))
        if fl > 0:
            g = Image.new('L', (S, S), 0)
            ImageDraw.Draw(g).ellipse([0.5 * S - 0.07 * S, PCY * S - 0.07 * S, 0.5 * S + 0.07 * S, PCY * S + 0.07 * S], fill=255)
            g = g.filter(ImageFilter.GaussianBlur(S * 0.03)).point(lambda v, a=fl: int(v * a))
            top.alpha_composite(Image.merge('RGBA', (Image.new('L', (S, S), 240), Image.new('L', (S, S), 248), Image.new('L', (S, S), 255), g)))
        for d in thrown:
            p = seg(f, IMPACT, IMPACT + 18)
            if 0 < p < 1:
                tt = p * 18
                x = 0.5 + math.cos(d['ang']) * d['v'] * tt
                y = PCY + math.sin(d['ang']) * d['v'] * tt + 0.0009 * tt * tt
                put(front, d['img'], x, y, d['s'] * (1 - 0.4 * p), 1 - ease(p))
        # 4. ripples run out across the portrait to its rim (see-through)
        for k, f0 in enumerate((IMPACT + 1, IMPACT + 4)):
            p = seg(f, f0, IGNITE + k * 2)
            if 0 < p < 1:
                r_out = 0.04 + (0.29 - 0.04) * ease(p)            # the art's outer ring reaches the rim at the end
                put(front, Lr['R1_ripples'], 0.5, PCY, r_out / R1_OUTER, 0.55 * (1 - p ** 3))
        out.append(finish(back, front, top))
    return out


def ring_layer(f_clock, alpha):
    """The ward ring at loop phase f_clock (turns once per LOOP_N frames), at alpha."""
    lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    # the ring itself holds still (a turning texture changes every pixel and costs about 3x the bytes); the light
    # travelling round it and the stars carry the motion
    put(lay, layers()['W1_ward_ring'], 0.5, PCY, ring_width(), alpha)
    return lay


def loop_frames():
    Lr = layers()
    stars = [(200, 0.0), (320, 0.33), (75, 0.66)]   # (angle in degrees, twinkle phase)
    out = []
    for f in range(LOOP_N):
        t = f / LOOP_N
        front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        front.alpha_composite(ring_layer(f, LOOP_ALPHA))
        # a brighter arc travelling round the ring, the other way, once per loop
        arc = ring_layer(f, 0.35)
        arc.putalpha(ImageChops.multiply(arc.getchannel('A'), wedge_mask(360 * t, 70)))
        front.alpha_composite(arc)
        for ang, ph in stars:
            p = (t + ph) % 1.0
            if p < 0.35:
                q = math.sin(math.pi * p / 0.35)
                r = RING_INNER + 0.035
                put(front, Lr['glints'][1], 0.5 + r * math.cos(math.radians(ang)), PCY + r * math.sin(math.radians(ang)),
                    0.05 * (0.5 + 0.5 * q), 0.8 * q)
        out.append(finish(Image.new('RGBA', (S, S), (0, 0, 0, 0)), front))
    return out


def ward_frames():
    Lr = layers()
    out = []
    for f in range(CAST_N):
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
        out.append(finish(Image.new('RGBA', (S, S), (0, 0, 0, 0)), front, top))
    return out


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
        a = (LOOP_ALPHA + 0.6 * ease(seg(f, 0, 2))) * (1 - ease(seg(f, 2, 6)))
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
    print(f'{name}: {len(frames)} frames of {SIZE} px at {MS} ms, {os.path.getsize(p)} bytes (ceiling 460800)')


BUILDERS = {'cast': cast_frames, 'ward': ward_frames, 'loop': loop_frames, 'break': break_frames}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', choices=list(BUILDERS))
    a = ap.parse_args()
    for name, fn in BUILDERS.items():
        if a.only in (None, name):
            save_strip(fn(), f'{name}_v1')
