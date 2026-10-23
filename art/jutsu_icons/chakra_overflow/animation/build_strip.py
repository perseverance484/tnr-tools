#!/usr/bin/env python3
"""Assemble the Chakra Overflow cast animation from the art director's layers (route A), v2.

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


def build(n_frames):
    star, wings, flash, sparks = (load(f) for f in ('anim_co_L1_star.png', 'anim_co_L2_wings.png',
                                                     'anim_co_L3_flash.png', 'anim_co_L4_sparks.png'))
    frames = []
    for i in range(n_frames):
        t = i / (n_frames - 1)
        c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
        # release (0.66-1.0): the emblem rises steadily and dissolves from the bottom up
        rel = seg(t, 0.66, 1.0)
        rise = -34 * rel
        gone = rel                                    # 0 -> 1: dissolve line climbs steadily from the bottom to the top
        fade = 1 - ease_in_out(seg(t, 0.84, 1.0))

        # wings (0.20-0.50): uncovered from the bottom up while settling 40 px into place; never rescaled
        wr = ease_in_out(seg(t, 0.20, 0.50))
        if wr > 0:
            place(c, wings, WING_S, WING_S, alpha=seg(t, 0.20, 0.30) * fade,
                  dy=WING_DY + 40 * (1 - ease_out(seg(t, 0.20, 0.50))) + rise,
                  keep_from=1.08 - wr * 1.2, keep_to=1.1 - gone * 1.25)

        # star (0.00-0.30): one continuous grow from a point to the final size, fixed center
        g = 0.06 + 0.94 * ease_out(seg(t, 0.0, 0.30))
        place(c, star, STAR_SX * g, STAR_SY * g, alpha=min(1, 0.4 + 2.4 * t) * fade,
              dy=STAR_DY + rise, keep_to=1.1 - max(0, gone - 0.15) * 1.3)

        # flash: ignition burst, then a soft swell when the wings complete
        fl = np.exp(-((t - 0.10) / 0.07) ** 2) + 0.30 * np.exp(-((t - 0.50) / 0.07) ** 2)
        fs = 0.18 + 0.30 * ease_out(seg(t, 0.0, 0.18))
        place(c, flash, fs, fs, alpha=min(1.0, fl), dy=STAR_DY * 0.6)

        # sparks (0.44-1.0): stream upward at a constant speed, fade in and out
        sp = seg(t, 0.44, 1.0)
        place(c, sparks, 0.95, 0.95, alpha=seg(t, 0.44, 0.54) * (1 - seg(t, 0.86, 1.0)), dy=60 - 150 * sp)
        frames.append(c)
    return frames


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frames', type=int, default=30)
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
    speed = round(1300 / len(frames))
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
