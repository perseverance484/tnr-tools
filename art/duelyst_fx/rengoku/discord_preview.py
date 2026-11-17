#!/usr/bin/env python3
"""Discord showcase GIF for Rengoku Ro's new animation, from the final strips (what will be uploaded).

    python3 art/duelyst_fx/rengoku/discord_preview.py

Real board geometry (hex 2:1, clip = tile height x 3), zoomed on one target; strike once, then the smoulder loop for
its two rounds, on one clock. Output: preview/rengoku_discord.gif (640x360).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "jutsu_icons", "forbidden_chakra_fury", "animation"))
import build_v5 as V  # noqa: E402

FINAL = os.path.join(HERE, "final")
STRIKE, STRIKE_MS = "anim_rengoku_strike_tight_300.webp", 70
SMOULDER, SMOULDER_MS = "anim_rengoku_smoulder_tight_300.webp", 70
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def strip_frames(path):
    im = Image.open(path).convert("RGBA")
    s = im.width
    return [im.crop((0, i * s, s, (i + 1) * s)) for i in range(im.height // s)]


def main():
    W, H = 640, 360
    w = 190                     # hex width on this canvas (zoomed board)
    h = w / 2
    e = int(h * 3)              # clip side at animationScale 3
    cx, cy = W * 0.6, H * 0.7   # the target's tile centre
    strike = [f.resize((e, e), Image.LANCZOS) for f in strip_frames(os.path.join(FINAL, STRIKE))]
    smoulder = [f.resize((e, e), Image.LANCZOS) for f in strip_frames(os.path.join(FINAL, SMOULDER))]

    base = Image.new("RGBA", (W, H), (30, 32, 29, 255))
    d = ImageDraw.Draw(base)
    col_step, STACK = w * 0.75, 0.25
    for c in range(-3, 4):
        for r in range(-3, 4):
            x = cx + c * col_step
            y = cy + r * h + (h / 2 if c % 2 else 0)
            d.polygon(V.hex_poly(x, y, w, h), outline=(255, 255, 255, 30))
    d.polygon(V.hex_poly(cx, cy, w, h), fill=(44, 40, 52, 255), outline=(190, 160, 255, 70))
    # stand-in target figure (a silhouette, so the dome's height reads against a body)
    fig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fig)
    bw, bh = w * 0.17, h * 1.55
    fd.ellipse((cx - bw * 0.55, cy - bh - bw * 0.9, cx + bw * 0.55, cy - bh + bw * 0.15), fill=(58, 54, 70, 255))
    fd.rounded_rectangle((cx - bw / 2, cy - bh, cx + bw / 2, cy - 4), radius=10, fill=(58, 54, 70, 255))
    fd.ellipse((cx - w * 0.16, cy - h * 0.09, cx + w * 0.16, cy + h * 0.09), fill=(0, 0, 0, 70))
    title = ImageFont.truetype(FONT, 30)
    sub = ImageFont.truetype(FONT2, 15)

    strike_end = len(strike) * STRIKE_MS
    loop_end = 2 * len(smoulder) * SMOULDER_MS   # two full smoulder cycles: the second shows its re-flare alone
    total = loop_end + 400
    step = 35
    frames, durs = [], []
    for t in range(0, total, step):
        im = base.copy()
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        im.alpha_composite(sh)
        im.alpha_composite(fig)
        if t < strike_end:
            im.alpha_composite(strike[t // STRIKE_MS], (int(cx - e / 2), int(cy - e / 2)))
        if t < loop_end:
            im.alpha_composite(smoulder[(t // SMOULDER_MS) % len(smoulder)], (int(cx - e / 2), int(cy - e / 2)))
        dd = ImageDraw.Draw(im)
        dd.text((22, 16), "Rengoku Rō", font=title, fill=(236, 222, 255, 255))
        dd.text((24, 54), "Purgatory Prison · new battle animation", font=sub, fill=(190, 176, 220, 255))
        frames.append(im.convert("RGB"))
        durs.append(step)
    pal = [f.quantize(colors=200, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for f in frames]
    out = os.path.join(HERE, "preview", "rengoku_discord.gif")
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=True, disposal=1)
    print(out, len(frames), "frames", os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
