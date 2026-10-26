#!/usr/bin/env python3
"""Ethereal Rebirth cast animation: scripted feasibility prototype (not art).

Proves the "ribbons wrap around the avatar" illusion within the game's limits before the art director paints layers.
The game draws an effect animation as ONE square sprite centred on the caster's tile, ON TOP of the avatar
(libs/threejs/combat.ts: showAnimation(..., scale: EFFECT_ANIMATION_SIZE = 50, layer 5)); nothing can pass behind the
avatar. So, as with Chakra Overflow's crown layout, the avatar's round token is kept as a clear window: ribbon parts on
the far side of the spin are drawn only outside the window (they read as passing behind), and parts on the near side
cross in front, turning see-through at face height.

    python3 art/jutsu_icons/ethereal_rebirth/animation/prototype_wrap.py [--frames 40] [--ms 60]

Writes docs/design/ethereal_rebirth_animation/: proto_strip.webp (vertical strip, 128 px frames), proto_frames.png,
proto_preview.gif (128 px and 50 px over three battle backgrounds with a stand-in token), layout_guide.png.
Token geometry from the Chakra Overflow measurement of the director's battle recording: centre 0.283 of the frame from
the top, radius 0.248 (art/jutsu_icons/chakra_overflow/animation/build_strip.py). Pillow only.
"""
import argparse
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
OUT = os.path.join(ROOT, 'docs', 'design', 'ethereal_rebirth_animation')
S = 512                      # working size
TOKEN_CY, TOKEN_R = 0.283, 0.248
WINDOW_R = 0.96 * TOKEN_R
FACE_Y = (TOKEN_CY - 0.16, TOKEN_CY + 0.10)   # front ribbon goes see-through while crossing this band
CORE = (0.5, TOKEN_CY + 0.17)                 # the "seal" bursts at the chest: the lower part of the token
GOLD = (255, 214, 110)
GOLD_HI = (255, 246, 210)
BLUE = (150, 205, 255)
BLUE_HI = (232, 246, 255)


def ease(t):
    return t * t * (3 - 2 * t)


def seg(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a)))


def in_window(x, y):
    return math.hypot(x - 0.5, y - TOKEN_CY) < WINDOW_R


def ribbon_points(phase, yc, a, b, length, pitch, n=90):
    """Points along a tilted helix around the token's vertical axis. Returns (x, y, depth>0 = near side, u 0..1)."""
    pts = []
    for i in range(n + 1):
        u = i / n
        th = phase - u * length
        x = 0.5 + a * math.cos(th)
        y = yc + b * math.sin(th) + pitch * u
        pts.append((x, y, math.sin(th), u))
    return pts


def draw_ribbon(layer_back, layer_front, pts, colour, hi, width, alpha):
    db, df = ImageDraw.Draw(layer_back), ImageDraw.Draw(layer_front)
    for (x0, y0, d0, u0), (x1, y1, d1, u1) in zip(pts, pts[1:]):
        taper = math.sin(math.pi * min(1.0, max(0.0, u0))) ** 0.6     # thin at head and tail
        w = max(1.0, width * taper * S)
        near = (d0 + d1) / 2 > 0
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        if not near and in_window(mx, my):
            continue                                                  # far side, behind the token: hidden
        a = alpha if near else alpha * 0.55                          # far side dimmer and thinner: reads as behind
        if not near:
            w *= 0.7
        if near and in_window(mx, my) and FACE_Y[0] < my < FACE_Y[1]:
            a *= 0.30                                                 # near side over the face: see-through
        d = df if near else db
        p0, p1 = (x0 * S, y0 * S), (x1 * S, y1 * S)
        d.line([p0, p1], fill=colour + (int(255 * a),), width=int(w))
        d.ellipse([p1[0] - w / 2, p1[1] - w / 2, p1[0] + w / 2, p1[1] + w / 2], fill=colour + (int(255 * a),))
        if near:
            d.line([p0, p1], fill=hi + (int(255 * a),), width=max(1, int(w * 0.35)))


def core_burst(layer, t):
    if t <= 0:
        return
    d = ImageDraw.Draw(layer)
    cx, cy = CORE[0] * S, CORE[1] * S
    r = S * 0.05 * ease(min(1, t * 1.6)) * (1.15 - 0.15 * t)
    al = int(255 * (1 - seg(t, 0.55, 1.0)))
    for k in range(8):                                                # cracks of light
        ang = k * math.pi / 4 + 0.3
        L = r * (2.2 if k % 2 == 0 else 1.5)
        d.line([(cx, cy), (cx + L * math.cos(ang), cy + L * math.sin(ang))], fill=GOLD + (al,), width=max(1, int(S * 0.008)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD + (al,))
    d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5], fill=(255, 255, 255, al))


def flecks(layer, t, rnd_seed=3):
    rnd = random.Random(rnd_seed)
    d = ImageDraw.Draw(layer)
    for i in range(26):
        x0 = 0.5 + rnd.uniform(-0.30, 0.30)
        y0 = rnd.uniform(0.25, 0.80)
        start = rnd.uniform(0.25, 0.75)
        life = rnd.uniform(0.25, 0.4)
        p = seg(t, start, start + life)
        if p <= 0 or p >= 1:
            continue
        y = y0 - 0.25 * p
        x = x0 + 0.03 * math.sin(6 * p + i)
        if in_window(x, y):
            continue
        a = int(255 * math.sin(math.pi * p))
        r = S * 0.008 * (1.4 if i % 3 == 0 else 1)
        c = GOLD_HI if i % 2 else BLUE_HI
        d.rectangle([x * S - r, y * S - r, x * S + r, y * S + r], fill=c + (a,))


def frame(t):
    back = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    front = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    grow = ease(seg(t, 0.08, 0.55))            # ribbons pour out of the core and lengthen
    rise = ease(seg(t, 0.15, 0.85))            # the spin climbs from the waist to above the head
    fade = 1 - ease(seg(t, 0.78, 1.0))         # dissolve at the end
    if grow > 0 and fade > 0:
        yc = 0.62 - 0.42 * rise
        spin = 2 * math.pi * 1.6 * t
        for k, (c, hi) in enumerate(((GOLD, GOLD_HI), (BLUE, BLUE_HI))):
            phase = spin + k * math.pi
            length = 0.4 + 3.2 * grow
            a_r = 0.30 + 0.12 * grow           # the spin widens as it rises
            pts = ribbon_points(phase, yc, a_r, 0.12, length, 0.30 * grow)
            draw_ribbon(back, front, pts, c, hi, 0.050, 0.95 * fade)
    # one ribbon breaks away and lashes out of frame (towards the enemy)
    lash = seg(t, 0.55, 0.78)
    if 0 < lash < 1:
        pts = []
        for i in range(40):
            u = i / 39
            s = lash * 1.6 - u * 0.6
            if s < 0:
                break
            x = 0.62 + 0.55 * s
            y = 0.30 - 0.32 * s + 0.05 * math.sin(4 * s)
            pts.append((x, y, 1.0, u))
        if len(pts) > 2:
            draw_ribbon(back, front, pts, GOLD, GOLD_HI, 0.040, 0.95 * (1 - seg(lash, 0.7, 1.0)))
    core_burst(front, seg(t, 0.0, 0.45))
    flecks(front, t)
    img = Image.alpha_composite(back, front)
    glow = img.filter(ImageFilter.GaussianBlur(S * 0.012))
    out = Image.alpha_composite(glow, img)
    return out.resize((128, 128), Image.LANCZOS)


def stand_in_token(size):
    """A grey stand-in for the avatar token: disc, white rim, simple head-and-shoulders silhouette."""
    t = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    cx, cy, r = size * 0.5, size * TOKEN_CY, size * TOKEN_R
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 78, 96, 255), outline=(240, 240, 240, 255), width=max(1, size // 64))
    d.ellipse([cx - r * 0.32, cy - r * 0.55, cx + r * 0.32, cy + r * 0.05], fill=(200, 170, 150, 255))
    d.chord([cx - r * 0.8, cy + r * 0.05, cx + r * 0.8, cy + r * 1.4], 180, 360, fill=(40, 60, 110, 255))
    return t


def preview(frames, ms):
    bgs = [(18, 22, 34), (74, 104, 60), (205, 210, 214)]
    gif = []
    for f in frames:
        canvas = Image.new('RGB', (3 * 150 + 3 * 70, 160), (30, 32, 38))
        for i, bg in enumerate(bgs):
            tile = Image.new('RGBA', (128, 128), bg + (255,))
            tile.alpha_composite(stand_in_token(128))
            tile.alpha_composite(f)
            canvas.paste(tile.convert('RGB'), (10 + i * 150, 16))
            small = Image.new('RGBA', (50, 50), bg + (255,))
            small.alpha_composite(stand_in_token(50))
            small.alpha_composite(f.resize((50, 50), Image.LANCZOS))
            canvas.paste(small.convert('RGB'), (460 + i * 70, 55))
        gif.append(canvas)
    gif[0].save(os.path.join(OUT, 'proto_preview.gif'), save_all=True, append_images=gif[1:], duration=ms, loop=0)


def guide():
    g = Image.new('RGB', (S, S), (20, 24, 36))
    d = ImageDraw.Draw(g)
    cx, cy, r = S * 0.5, S * TOKEN_CY, S * TOKEN_R
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(220, 70, 70), width=3)
    d.rectangle([0, FACE_Y[0] * S, S, FACE_Y[1] * S], outline=(220, 180, 70), width=1)
    for k, c in enumerate(((255, 214, 110), (150, 205, 255))):
        pts = ribbon_points(k * math.pi, 0.40 + 0.20 * k, 0.40, 0.12, 2 * math.pi, 0.0, 120)
        for (x0, y0, d0, _), (x1, y1, d1, _) in zip(pts, pts[1:]):
            near = d0 > 0
            col = c if near else tuple(v // 3 for v in c)
            d.line([(x0 * S, y0 * S), (x1 * S, y1 * S)], fill=col, width=4 if near else 2)
    x, y = CORE[0] * S, CORE[1] * S
    d.ellipse([x - 10, y - 10, x + 10, y + 10], outline=(255, 255, 255), width=2)
    f = ImageFont.load_default()
    d.text((8, 8), "red: avatar token (keep clear except near-side ribbons)", fill=(220, 70, 70), font=f)
    d.text((8, 22), "yellow band: face height (near-side ribbons see-through)", fill=(220, 180, 70), font=f)
    d.text((8, 36), "bright: near side (in front); dim: far side (hidden inside the token)", fill=(200, 200, 200), font=f)
    d.text((8, 50), "white ring: the seal's core burst (chest, lower token)", fill=(255, 255, 255), font=f)
    g.save(os.path.join(OUT, 'layout_guide.png'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frames', type=int, default=40)
    ap.add_argument('--ms', type=int, default=60)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    frames = [frame(i / (a.frames - 1)) for i in range(a.frames)]
    strip = Image.new('RGBA', (128, 128 * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        strip.paste(f, (0, 128 * i))
    strip.save(os.path.join(OUT, 'proto_strip.webp'), lossless=True, method=6)
    sheet = Image.new('RGBA', (128 * 10, 128 * math.ceil(len(frames) / 10)), (18, 22, 34, 255))
    for i, f in enumerate(frames):
        cell = Image.new('RGBA', (128, 128), (18, 22, 34, 255))
        cell.alpha_composite(stand_in_token(128))
        cell.alpha_composite(f)
        sheet.paste(cell, ((i % 10) * 128, (i // 10) * 128))
    sheet.convert('RGB').save(os.path.join(OUT, 'proto_frames.png'))
    preview(frames, a.ms)
    guide()
    print(len(frames), 'frames,', os.path.getsize(os.path.join(OUT, 'proto_strip.webp')), 'bytes, speed', a.ms, 'ms')


if __name__ == '__main__':
    main()
