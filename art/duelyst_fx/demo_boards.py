#!/usr/bin/env python3
"""Duelyst effects on the real TNR board (demo for the director, 2026-11-16).

    python3 art/duelyst_fx/demo_boards.py --duelyst /path/to/duelyst/app

Builds preview/*.gif with the FCF board (spiral radius 4 around the caster, 60 tiles) from build_v5.board:
  fcf_duelyst_a: caster = eightgates_purpleflame (scale 3); field = shadowcreep spikes per tile (scale 2);
                 ground/glint/drain = our v5 tessellating scar.
  fcf_duelyst_b: same caster; field = our v5 through-cut with shadowcreep spikes erupting from it (hybrid).
"""
import argparse
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FCF = os.path.join(HERE, "..", "jutsu_icons", "forbidden_chakra_fury", "animation")
sys.path.insert(0, HERE)
sys.path.insert(0, FCF)
import duelyst_fx as D  # noqa: E402
import build_v5 as V  # noqa: E402

SIZE = 192


def dclip(app, name, fit, dy=0.0, tint=None):
    src = os.path.join(app, "resources", "fx")
    frs = D.place(D.frames(src, name), SIZE, fit, dy, tint)
    return frs, D.delay_ms(os.path.join(app, "data", "resources.js"), name)


def resample(frs, src_ms, dst_ms):
    """Re-time a clip onto another frame clock (the board draws the field on one ms value)."""
    n = max(1, round(len(frs) * src_ms / dst_ms))
    return [frs[min(len(frs) - 1, int(i * dst_ms / src_ms))] for i in range(n)]


def over(a, b):
    c = a.copy()
    c.alpha_composite(b)
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duelyst", required=True, help="the Duelyst app/ folder")
    a = ap.parse_args()
    prev = os.path.join(HERE, "preview")
    os.makedirs(prev, exist_ok=True)
    rt = lambda frs: [f.resize((SIZE, SIZE), Image.LANCZOS) for f in frs]  # noqa: E731
    v5 = {"loop": rt(V.build_field_loop()), "end": rt(V.build_field_end()),
          "ground": V.build_field_ground().resize((384, 192), Image.LANCZOS)}
    caster, cms = dclip(a.duelyst, "fx_f2_eightgates_purpleflame", fit=0.95, dy=-0.18)
    creep, kms = dclip(a.duelyst, "fx_shadowcreep:fx_shadowcreep_spawn_", fit=0.95, dy=-0.12)
    print("eightgates", len(caster), cms, "ms; shadowcreep", len(creep), kms, "ms")

    # A: pure Duelyst pieces on top of our scar
    V.MS.update({"field": kms, "caster": cms})
    clips = dict(v5, field=creep, caster=caster)
    print("A", V.board(clips, os.path.join(prev, "fcf_duelyst_a.gif")))

    # B: hybrid, our cut (42 ms clock) with the spikes erupting from it at the flash (frame 8)
    cut = rt(V.build_field_appear())
    spikes = resample(creep, kms, 42)
    field = []
    for i in range(max(len(cut), 8 + len(spikes))):
        f = cut[i] if i < len(cut) else Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        if i >= 8 and i - 8 < len(spikes):
            f = over(f, spikes[i - 8])
        field.append(f)
    V.MS.update({"field": 42, "caster": cms})
    clips = dict(v5, field=field, caster=caster)
    print("B", V.board(clips, os.path.join(prev, "fcf_duelyst_b.gif")))


if __name__ == "__main__" and "--extra" not in sys.argv:
    main()


def sampler(app, out, picks, scale=3.0, px=2, shrink=0.75):
    """Hero pieces on single targets, one after another (as actions replay), on the real board."""
    cols, rows, STACK, width_css = 12, 10, 0.25, 360
    hs = width_css / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    W, H = int(width_css * px), int((rows + 0.5) * h)
    pos = lambda c, r: (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))  # noqa: E731
    spots = [(2, 2), (5, 2), (8, 2), (10, 4), (2, 6), (5, 6), (8, 7), (10, 8)]
    from PIL import ImageDraw
    base = Image.new("RGBA", (W, H), (38, 40, 36, 255))
    d = ImageDraw.Draw(base)
    for c in range(cols):
        for r in range(rows):
            x, y = pos(c, r)
            d.polygon(V.hex_poly(x, y, w, h), outline=(255, 255, 255, 34))
    e = int(h * scale)
    clips = []
    t0 = 0
    for (name, fit, dy, label), spot in zip(picks, spots):
        frs, ms = dclip(app, name, fit, dy)
        frs = [f.resize((e, e), Image.LANCZOS) for f in frs]
        clips.append((pos(*spot), frs, ms, t0, label))
        t0 += len(frs) * ms * 0.55  # overlap a little, like a fast replay
    total = int(max(t + len(f) * m for _, f, m, t, _ in clips)) + 400
    frames = []
    for t in range(0, total, 40):
        im = base.copy()
        dd = ImageDraw.Draw(im)
        for (x, y), frs, ms, st, label in clips:
            dd.rounded_rectangle((x - w * 0.13, y - h * 1.7, x + w * 0.13, y), radius=6, fill=(70, 66, 84, 255),
                                 outline=(150, 140, 170, 255))
            dd.text((x - w * 0.5, y + h * 0.35), label, fill=(230, 230, 230, 255))
            k = int((t - st) // ms)
            if 0 <= k < len(frs):
                im.alpha_composite(frs[k], (int(x - e / 2), int(y - e / 2)))
        im = im.convert("RGB").resize((int(W * shrink), int(H * shrink)), Image.LANCZOS)
        frames.append(im)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=40, loop=0, optimize=True)
    return len(frames)


def extra(app):
    prev = os.path.join(HERE, "preview")
    rt = lambda frs: [f.resize((SIZE, SIZE), Image.LANCZOS) for f in frs]  # noqa: E731
    caster, cms = dclip(app, "fx_f2_eightgates_purpleflame", fit=1.0, dy=-0.2)
    V.MS.update({"field": 42, "caster": cms})
    clips = {"field": rt(V.build_field_appear()), "loop": rt(V.build_field_loop()), "end": rt(V.build_field_end()),
             "ground": V.build_field_ground().resize((384, 192), Image.LANCZOS), "caster": caster}
    print("C", V.board(clips, os.path.join(prev, "fcf_duelyst_c.gif")))
    picks = [("fx_f2_spiraltechnique02", 0.9, -0.15, "spiraltechnique"),
             ("fx_f2_mistdragonseal", 0.9, -0.15, "mistdragonseal"),
             ("fx_heavenlystrike", 1.0, -0.3, "heavenlystrike"),
             ("fx_crossslash", 0.9, -0.12, "crossslash"),
             ("fx_f4_voidpulse", 0.95, -0.1, "voidpulse"),
             ("fx_fireslash", 0.85, -0.12, "fireslash"),
             ("fx_f6_hailstoneprison", 1.0, -0.1, "hailstoneprison"),
             ("fx_f4_obliterate", 1.0, 0.0, "obliterate")]
    print("sampler", sampler(app, os.path.join(prev, "duelyst_sampler.gif"), picks))


if __name__ == "__main__" and "--extra" in sys.argv:
    extra(sys.argv[sys.argv.index("--duelyst") + 1])
