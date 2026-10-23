#!/usr/bin/env python3
"""Assemble the Chakra Overflow cast animation from the art director's layers (route A), v3 (dissolve in and out).

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
from PIL import Image

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


def build(n_frames):
    """v3 (director: "faded in and out, like a dissolve effect"): the finished emblem materializes through a particle
    dissolve, holds while sparks stream upward, then dissolves away. Nothing changes size or position."""
    star, wings, flash, sparks = (load(f) for f in ('anim_co_L1_star.png', 'anim_co_L2_wings.png',
                                                     'anim_co_L3_flash.png', 'anim_co_L4_sparks.png'))
    emblem = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    place(emblem, wings, WING_S, WING_S, dy=WING_DY)
    place(emblem, star, STAR_SX, STAR_SY, dy=STAR_DY)
    spark_layer = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    field = dissolve_field()
    frames = []
    for i in range(n_frames):
        t = i / (n_frames - 1)
        c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
        p_in = ease_in_out(seg(t, 0.0, 0.32))          # dissolve in (about 0.7 s)
        p_out = 1 - ease_in_out(seg(t, 0.68, 1.0))     # dissolve out (about 0.7 s), after a hold of about 0.8 s
        p = min(p_in, p_out)
        if p > 0:
            c.alpha_composite(apply_dissolve(emblem, field, p))
        # a soft swell of light at the heart as the emblem completes
        fl = 0.55 * np.exp(-((t - 0.31) / 0.09) ** 2)
        place(c, flash, 0.42, 0.42, alpha=fl, dy=STAR_DY * 0.6)
        # sparks stream upward during the hold and dissolve with the emblem
        sp = seg(t, 0.24, 1.0)
        s = Image.new('RGBA', (W, W), (0, 0, 0, 0))
        place(s, sparks, 0.95, 0.95, alpha=seg(t, 0.24, 0.38), dy=60 - 150 * sp)
        if p_out < 1:
            s = apply_dissolve(s, 1 - field, p_out)
        c.alpha_composite(s)
        frames.append(c)
    return frames


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frames', type=int, default=40)
    ap.add_argument('--ms', type=int, default=2200, help='total duration in ms')
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
