#!/usr/bin/env python3
"""Assemble the Chakra Overflow cast animation from the art director's keys and layers (route A).

    python3 art/jutsu_icons/chakra_overflow/animation/build_strip.py [--frames N] [--size PX] [--preview DIR]

Inputs: raws/anim_co_K1..K5.png (key poses) and raws/anim_co_L1_star, L2_wings, L3_flash, L4_sparks (layers), all
1254 px transparent PNGs registered on one center. Output: exports/anim_chakra_overflow_v1.webp, a vertical strip of
square frames (the game's ANIMATION format; libs/threejs/util.ts showAnimation), intended at 50 ms per frame.
Beats (docs/handoffs/CHAKRA_OVERFLOW_ANIMATION_ART_REQUEST.md section 4): ignition, star flare, wings rise, overflow,
release.
"""
import argparse, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
W = 512            # working canvas
FIT = 0.80         # whole composition scaled into the central 80% so the rise and sparks stay inside the frame

def load(name):
    im = Image.open(os.path.join(HERE, 'raws', name)).convert('RGBA')
    return im.resize((int(W * FIT), int(W * FIT)), Image.LANCZOS)

def ease_out(t): return 1 - (1 - t) ** 3
def ease_in_out(t): return 3 * t * t - 2 * t ** 3
def seg(t, a, b): return min(1.0, max(0.0, (t - a) / (b - a)))

def place(canvas, layer, scale=1.0, alpha=1.0, dy=0, reveal=None):
    """Composite `layer` centered (plus dy), scaled and faded; `reveal` 0..1 uncovers it from the bottom up."""
    if alpha <= 0.003 or scale <= 0.01:
        return
    sz = max(1, int(layer.width * scale))
    im = layer.resize((sz, sz), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    a[..., 3] *= alpha
    if reveal is not None and reveal < 1:
        h = a.shape[0]
        y = np.arange(h, dtype=np.float32)[:, None] / h
        edge = 1.05 - reveal * 1.1                     # reveal line moves from bottom to top
        a[..., 3] *= np.clip((y - edge) / 0.18, 0, 1)
    im = Image.fromarray(a.astype(np.uint8), 'RGBA')
    canvas.alpha_composite(im, (W // 2 - sz // 2, W // 2 - sz // 2 + int(dy)))

def build(n_frames):
    K = {k: load(f'anim_co_K{k}.png') for k in range(1, 6)}
    star, wings, flash, sparks = (load(f) for f in ('anim_co_L1_star.png', 'anim_co_L2_wings.png',
                                                     'anim_co_L3_flash.png', 'anim_co_L4_sparks.png'))
    frames = []
    for i in range(n_frames):
        t = i / (n_frames - 1)
        c = Image.new('RGBA', (W, W), (0, 0, 0, 0))
        # 1 ignition (0-0.12): K1 grows in, flash builds
        a1 = (0.55 + 0.45 * ease_out(seg(t, 0.0, 0.06))) * (1 - seg(t, 0.10, 0.18))
        place(c, K[1], 0.7 + 0.5 * seg(t, 0.0, 0.12), a1)
        fl = np.exp(-((t - 0.13) / 0.06) ** 2) + 0.35 * np.exp(-((t - 0.55) / 0.06) ** 2)
        place(c, flash, 0.25 + 0.45 * seg(t, 0.02, 0.2), min(1, fl))
        # 2 star flare (0.08-0.30): the star snaps open
        s2 = ease_out(seg(t, 0.08, 0.24))
        a_star = seg(t, 0.08, 0.12) * (1 - seg(t, 0.44, 0.52))
        place(c, K[2], 0.35 + 0.65 * s2, a_star * (1 - seg(t, 0.26, 0.36)))
        place(c, star, 0.35 + 0.65 * s2, a_star * seg(t, 0.24, 0.32))
        # 3 wings rise (0.22-0.48): wings sweep up from below, uncovered bottom-up
        r3 = ease_in_out(seg(t, 0.22, 0.46))
        place(c, wings, 0.88 + 0.12 * r3, seg(t, 0.22, 0.28) * (1 - seg(t, 0.44, 0.52)), dy=40 * (1 - r3), reveal=r3)
        place(c, K[3], 1.0, seg(t, 0.36, 0.44) * (1 - seg(t, 0.46, 0.54)))
        # 5 release (0.72-1.0): K5 takes over, lifts and dissolves upward
        r5 = seg(t, 0.72, 1.0)
        place(c, K[5], 1.0 + 0.04 * r5, seg(t, 0.72, 0.76) * (1 - ease_in_out(seg(t, 0.84, 1.0))), dy=-36 * r5)
        # 4 overflow (0.46-0.74): the full emblem, a breath of pulse, sparks streaming up
        pulse = 1.0 + 0.03 * np.sin(seg(t, 0.5, 0.74) * np.pi)
        a4 = seg(t, 0.46, 0.54) * (1 - seg(t, 0.75, 0.79))
        place(c, K[4], pulse, a4)
        sp = seg(t, 0.50, 1.0)
        place(c, sparks, 1.0 + 0.08 * sp, seg(t, 0.50, 0.58) * (1 - seg(t, 0.86, 1.0)), dy=-70 * sp)
        frames.append(c)
    return frames

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frames', type=int, default=26)
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
    print(out, strip.size, os.path.getsize(out), 'bytes', f'{len(frames)} frames')
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
                    append_images=gif[1:], duration=50, loop=0)
        n = len(frames); cols = 13
        sheet = Image.new('RGB', (cols * a.size, ((n + cols - 1) // cols) * a.size), (15, 23, 42))
        for i, f in enumerate(frames):
            t = Image.new('RGBA', f.size, (15, 23, 42, 255)); t.alpha_composite(f)
            sheet.paste(t.convert('RGB'), ((i % cols) * a.size, (i // cols) * a.size))
        sheet.save(os.path.join(a.preview, 'anim_chakra_overflow_v1_frames.png'))

if __name__ == '__main__':
    main()
