#!/usr/bin/env python3
"""Assemble the Chakra Overflow cast animation from the art director's layers (route A), v5 (dissolve in and out, glint during the hold).

    python3 art/jutsu_icons/chakra_overflow/animation/build_strip.py [--frames N] [--size PX] [--preview DIR]

v2 (director, 2026-10-23: "not smooth enough. The shapes seem to change size/shift"): v1 cross-faded between the key
poses K2-K5, which are separate drawings whose star differs in size, proportion and height from the star layer, so the
shapes jumped. v2 animates ONE star (L1) and ONE pair of wings (L2) on continuous, monotonic curves for the whole run,
with the flash (L3) and sparks (L4) on top. The key poses K1-K5 are kept as the timing and look reference only.

Final pose: wings at 0.98 scale, star narrowed to match the slimmer star of K4 (x 0.84*0.80, y 0.84) and raised 90 px
(1254 px space), as measured against K4. Output: exports/anim_chakra_overflow_v1.webp, a vertical strip of square frames
(libs/threejs/util.ts showAnimation), intended speed = 1300 ms / frames.
"""
import argparse, os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = 1254          # raw canvas
W = 512             # working canvas
FIT = 0.80          # composition scaled into the central 80% so the rise and sparks stay inside the frame
U = W * FIT / SRC   # raw-pixel to working-pixel factor

STAR_SX, STAR_SY, STAR_DY = 0.84 * 0.80, 0.84, -90   # final star, measured against K4
WING_S, WING_DY = 0.98, 10


def load(name):
    return Image.open(os.path.join(HERE, 'raws', name)).convert('RGBA')


def ease_out(t): return 1 - (1 - t) ** 3
def ease_in_out(t): return t * t * (3 - 2 * t)
def seg(t, a, b): return min(1.0, max(0.0, (t - a) / (b - a)))


def place(canvas, layer, sx, sy, alpha=1.0, dy=0.0, keep_from=None, keep_to=None):
    """Composite `layer` centered, scaled (sx, sy relative to the raw canvas), faded and shifted by dy raw pixels.

    keep_from / keep_to: 0..1 fractions of the layer's height (0 = top). Only the band between them is kept, with soft
    edges, which reveals the wings bottom-up and dissolves the emblem bottom-up without moving anything."""
    if alpha <= 0.003:
        return
    w, h = max(1, round(SRC * sx * U)), max(1, round(SRC * sy * U))
    a = np.asarray(layer.resize((w, h), Image.LANCZOS)).astype(np.float32)
    a[..., 3] *= alpha
    if keep_from is not None or keep_to is not None:
        y = np.arange(h, dtype=np.float32)[:, None] / h
        soft = 0.16
        m = np.ones_like(y)
        if keep_from is not None:
            m = m * np.clip((y - keep_from) / soft + 0.5, 0, 1)
        if keep_to is not None:
            m = m * np.clip((keep_to - y) / soft + 0.5, 0, 1)
        a[..., 3] *= m
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')
    x = W // 2 - w // 2
    yy = W // 2 - h // 2 + round(dy * U)
    canvas.alpha_composite(im, (x, yy))


def dissolve_field(seed=11):
    """A smooth noise field in 0..1: pixels with a low value appear first and vanish last."""
    rng = np.random.default_rng(seed)
    fine = Image.fromarray((rng.random((W // 4, W // 4)) * 255).astype(np.uint8)).resize((W, W), Image.BICUBIC)
    coarse = Image.fromarray((rng.random((W // 16, W // 16)) * 255).astype(np.uint8)).resize((W, W), Image.BICUBIC)
    f = 0.6 * np.asarray(fine, np.float32) + 0.4 * np.asarray(coarse, np.float32)
    f = (f - f.min()) / (f.max() - f.min())
    # bias so the center (the star's heart) resolves first and dissolves last
    yy, xx = np.mgrid[0:W, 0:W]
    r = np.sqrt((xx - W / 2) ** 2 + (yy - W / 2 + STAR_DY * U * 0.6) ** 2) / (W * 0.5)
    f = 0.7 * f + 0.3 * np.clip(r, 0, 1)
    return (f - f.min()) / (f.max() - f.min())


def apply_dissolve(img, field, p, soft=0.14):
    """Keep pixels whose field value is below the progress p (0 = nothing, 1 = everything), with a soft band, and fade
    the whole layer with p so the particles arrive and leave softly (a fade plus a dissolve)."""
    a = np.asarray(img).astype(np.float32)
    m = np.clip((p * (1 + soft) - field) / soft, 0, 1) * (0.35 + 0.65 * p)
    a[..., 3] *= m
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')


def glint_sparkle(size, rot_deg):
    """A crisp four-point lens glint: long thin horizontal and vertical rays, short diagonal rays, a hot core.
    Returned as a white RGBA layer of the working canvas size, centered."""
    yy, xx = np.mgrid[0:W, 0:W].astype(np.float32)
    cx, cy = W / 2, W / 2 + STAR_DY * U
    th = np.deg2rad(rot_deg)
    x = (xx - cx) * np.cos(th) + (yy - cy) * np.sin(th)
    y = -(xx - cx) * np.sin(th) + (yy - cy) * np.cos(th)
    L = max(size, 1e-3)
    ray = lambda u, v, length, width: np.exp(-(v / (width * (1 - 0.7 * np.clip(np.abs(u) / length, 0, 1)) + 0.5)) ** 2) * np.clip(1 - np.abs(u) / length, 0, 1) ** 1.3
    a = ray(x, y, L, 9.0) + ray(y, x, L * 1.3, 9.0)                       # main cross, vertical ray longest
    d1, d2 = (x + y) / np.sqrt(2), (x - y) / np.sqrt(2)
    a += 0.7 * (ray(d1, d2, L * 0.5, 6.0) + ray(d2, d1, L * 0.5, 6.0))   # short diagonal rays
    a += 1.5 * np.exp(-(x * x + y * y) / (2 * (0.10 * L + 4.0) ** 2))      # hot core
    a += 0.35 * np.exp(-(x * x + y * y) / (2 * (0.35 * L + 6.0) ** 2))     # soft halo
    a = np.clip(a, 0, 1)
    rgb = np.stack([np.full_like(a, 255), np.full_like(a, 250), np.full_like(a, 225)], -1)
    return Image.fromarray(np.dstack([rgb, a * 255]).astype(np.uint8), 'RGBA')


def brighten(img, mask_alpha, amount):
    """Push the pixels under mask_alpha (0..1) toward white by `amount` (0..1), keeping the alpha."""
    if amount <= 0.003:
        return img
    a = np.asarray(img).astype(np.float32)
    k = (amount * mask_alpha)[..., None]
    a[..., :3] = a[..., :3] + (255 - a[..., :3]) * k
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')


def build(n_frames):
    """v5 (director): dissolve in and out with a longer hold, and a glimmer while it holds: a band of light sweeps
    across the star, the star shines brighter, and a crisp four-point glint flares at its heart, then winks out.
    Timeline over the whole run: dissolve in 0-0.27, hold 0.27-0.73 (glint 0.42-0.64), dissolve out 0.73-1."""
    star, wings, flash, sparks = (load(f) for f in ('anim_co_L1_star.png', 'anim_co_L2_wings.png',
                                                     'anim_co_L3_flash.png', 'anim_co_L4_sparks.png'))
    emblem = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    place(emblem, wings, WING_S, WING_S, dy=WING_DY)
    star_only = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    place(star_only, star, STAR_SX, STAR_SY, dy=STAR_DY)
    emblem.alpha_composite(star_only)
    star_mask = np.asarray(star_only)[..., 3].astype(np.float32) / 255
    field = dissolve_field()
    yy, xx = np.mgrid[0:W, 0:W].astype(np.float32)
    frames = []
    for i in range(n_frames):
        t = i / (n_frames - 1)
        c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
        p_in = ease_in_out(seg(t, 0.0, 0.27))          # dissolve in (about 0.7 s)
        p_out = 1 - ease_in_out(seg(t, 0.73, 1.0))     # dissolve out (about 0.7 s), after a hold of about 1.2 s
        p = min(p_in, p_out)
        # glimmer: a diagonal band of light sweeps across the star (0.42-0.56), the star swells brighter to a peak at
        # 0.555, and the glint flares (0.52-0.555) then winks out to a point (0.555-0.60)
        sweep = seg(t, 0.42, 0.56)
        band_pos = -0.6 + 1.6 * ease_in_out(sweep)
        diag = ((xx - W / 2) + (yy - W / 2)) / W
        band = np.exp(-((diag - band_pos) / 0.11) ** 2) * (0 < sweep < 1)
        glow = np.exp(-((t - 0.57) / 0.06) ** 2)
        layer = brighten(emblem, np.clip(star_mask * (0.9 * band + 0.8 * glow), 0, 1), 1.0)
        # a white bloom around the star at the peak, so "shines brighter" reads on top of an already bright star
        bloom = Image.fromarray(np.dstack([np.full((W, W), 255), np.full((W, W), 248), np.full((W, W), 215),
                                           np.asarray(Image.fromarray((star_mask * 255).astype(np.uint8)).filter(
                                               ImageFilter.GaussianBlur(10))).astype(np.float32) * 0.85 * glow]).astype(np.uint8), 'RGBA')
        if p > 0:
            c.alpha_composite(apply_dissolve(layer, field, p))
            if glow > 0.01:
                c.alpha_composite(bloom)
        # soft swell of light at the heart as the emblem completes, and a smaller one under the glint
        fl = 0.55 * np.exp(-((t - 0.25) / 0.08) ** 2) + 0.5 * np.exp(-((t - 0.57) / 0.05) ** 2)
        place(c, flash, 0.42, 0.42, alpha=fl, dy=STAR_DY * 0.6)
        # the glint itself: grows fast, holds a breath, winks out to a point
        if 0.50 <= t <= 0.64:
            grow = ease_out(seg(t, 0.50, 0.56))
            wink = 1 - ease_in_out(seg(t, 0.58, 0.64))
            size = W * 0.48 * grow * (0.10 + 0.90 * wink)
            g = glint_sparkle(size, rot_deg=10 * seg(t, 0.50, 0.64))
            ga = np.asarray(g).astype(np.float32); ga[..., 3] *= min(1, 1.3 * wink + 0.0) * grow
            c.alpha_composite(Image.fromarray(ga.astype(np.uint8), 'RGBA'))
        # sparks stream upward during the hold and dissolve with the emblem
        sp = seg(t, 0.20, 1.0)
        s = Image.new('RGBA', (W, W), (0, 0, 0, 0))
        place(s, sparks, 0.95, 0.95, alpha=seg(t, 0.20, 0.32), dy=60 - 160 * sp)
        if p_out < 1:
            s = apply_dissolve(s, 1 - field, p_out)
        c.alpha_composite(s)
        frames.append(c)
    return frames


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frames', type=int, default=48)
    ap.add_argument('--ms', type=int, default=2600, help='total duration in ms')
    ap.add_argument('--size', type=int, default=128)
    ap.add_argument('--preview')
    a = ap.parse_args()
    frames = [f.resize((a.size, a.size), Image.LANCZOS) for f in build(a.frames)]
    strip = Image.new('RGBA', (a.size, a.size * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        strip.paste(f, (0, i * a.size))
    os.makedirs(os.path.join(HERE, 'exports'), exist_ok=True)
    out = os.path.join(HERE, 'exports', 'anim_chakra_overflow_v1.webp')
    strip.save(out, 'WEBP', lossless=True, method=6)
    speed = round(a.ms / len(frames))
    print(out, strip.size, os.path.getsize(out), 'bytes', f'{len(frames)} frames, speed {speed} ms')
    if a.preview:
        bgs = [(15, 23, 42), (120, 150, 90), (230, 235, 240)]
        gif = []
        for f in frames:
            row = Image.new('RGB', (3 * 140 + 3 * 62 + 6, 140), (30, 30, 34)); x = 6
            for b in bgs:
                t = Image.new('RGBA', f.size, b + (255,)); t.alpha_composite(f)
                row.paste(t.convert('RGB').resize((128, 128), Image.LANCZOS), (x, 6)); x += 140
            for b in bgs:
                t = Image.new('RGBA', f.size, b + (255,)); t.alpha_composite(f)
                row.paste(t.convert('RGB').resize((50, 50), Image.LANCZOS), (x, 45)); x += 62
            gif.append(row)
        gif[0].save(os.path.join(a.preview, 'anim_chakra_overflow_v1_preview.gif'), save_all=True,
                    append_images=gif[1:], duration=speed, loop=0)
        n = len(frames); cols = 15
        sheet = Image.new('RGB', (cols * a.size, ((n + cols - 1) // cols) * a.size), (15, 23, 42))
        for i, f in enumerate(frames):
            t = Image.new('RGBA', f.size, (15, 23, 42, 255)); t.alpha_composite(f)
            sheet.paste(t.convert('RGB'), ((i % cols) * a.size, (i // cols) * a.size))
        sheet.save(os.path.join(a.preview, 'anim_chakra_overflow_v1_frames.png'))


if __name__ == '__main__':
    main()
