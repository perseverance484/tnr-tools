#!/usr/bin/env python3
"""Cut the five layers out of the art director's sheet (anim_er_sheet_v1.png: grey, glow-tinted panels, not transparent).

    python3 art/jutsu_icons/ethereal_rebirth/animation/extract_layers.py

The art itself is saturated colour or near-white light; the panels are low-saturation grey with a soft coloured glow.
Alpha = max(saturation ramp, brightness ramp), so the painted forms are kept and the baked-in glow halo is dropped (the
build script adds its own glow). Colours are kept as painted. Writes layers/anim_er_<name>.png (RGBA). Pillow only.
"""
import os
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'raws', 'anim_er_sheet_v1.png')
PANELS = {  # x0, y0, x1, y1 inside the panel borders (measured from the sheet's dark frame lines)
    'R1_ribbon_gold': (6, 6, 1529, 275),
    'R2_ribbon_blue': (6, 291, 1529, 557),
    'C1_core': (6, 571, 454, 1011),
    'F1_flecks': (466, 571, 940, 1011),
    'K1_peak': (954, 571, 1529, 1011),
}
S0, S1 = 0.62, 0.84      # saturation ramp (the gold panel's glow reaches about 0.55)
V0, V1 = 222, 246        # brightness ramp (the panels top out near 210)


def ramp(v, a, b):
    return 0.0 if v <= a else 1.0 if v >= b else (v - a) / (b - a)


def extract(panel):
    rgb = panel.convert('RGB')
    hsv = rgb.convert('HSV')
    out = Image.new('RGBA', rgb.size)
    src, hs, dst = rgb.load(), hsv.load(), out.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = src[x, y]
            _, s, v = hs[x, y]
            a = max(ramp(s / 255, S0, S1), ramp(v, V0, V1))
            dst[x, y] = (r, g, b, int(255 * a))
    # drop specks of one or two pixels
    al = out.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    out.putalpha(Image.eval(al, lambda v: v).point(lambda v: v) if False else Image.composite(out.getchannel('A'), al, al))
    return out


def main():
    sheet = Image.open(SRC)
    os.makedirs(os.path.join(HERE, 'layers'), exist_ok=True)
    for name, box in PANELS.items():
        layer = extract(sheet.crop(box))
        bb = layer.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        if bb:
            pad = 6
            bb = (max(0, bb[0] - pad), max(0, bb[1] - pad), min(layer.width, bb[2] + pad), min(layer.height, bb[3] + pad))
            layer = layer.crop(bb)
        layer.save(os.path.join(HERE, 'layers', f'anim_er_{name}.png'))
        print(name, layer.size)


if __name__ == '__main__':
    main()
