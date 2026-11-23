#!/usr/bin/env python3
"""The PR's before and after on one clock (2026-11-22).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v24/compare_pr.py

Three panels, stacked: main today (v24's today-engine clips with no tile variation: every tile alike, all at once);
the same clips with this PR's tile variation; and the full v23 as one visual on the user (this PR's large visual and
grid sheet). Reads the strips cut_today.py and cut_full.py wrote. Writes pr_fcf_before_after.gif.
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cut_full as CF  # noqa: E402
import cut_today as CT  # noqa: E402

BV = CT.BV
STEP = 30


def strip(name):
    im = Image.open(os.path.join(HERE, name)).convert("RGBA")
    c = im.width
    return [im.crop((0, i * c, c, (i + 1) * c)) for i in range(im.height // c)]


def grid(name, frames, cols):
    im = Image.open(os.path.join(HERE, name)).convert("RGBA")
    c = im.width // cols
    return [im.crop(((i % cols) * c, (i // cols) * c, (i % cols + 1) * c, (i // cols + 1) * c)) for i in range(frames)]


def main():
    caster, fa, fb = strip("anim_fcf_v24_caster.webp"), strip("anim_fcf_v24_fury_a.webp"), strip("anim_fcf_v24_fury_b.webp")
    sa, sb = strip("anim_fcf_v24_storm_a.webp"), strip("anim_fcf_v24_storm_b.webp")
    full = grid("anim_fcf_v24_full.webp", 45, 7)
    ms = CT.ms
    plain = BV.render([(fa, None, ms("fury"), 2, {}), (sa, None, ms("storm"), 3, {})], (caster, ms("caster"), 3),
                      "Main today: every tile plays the same clip at once", step=STEP, tail=150)
    varied = BV.render([(fa, fb, ms("fury"), 2, dict(alternate=True, mirror=True, stagger=90, ripple=25)),
                        (sa, sb, ms("storm"), 3, dict(alternate=True, mirror=True, stagger=140, ripple=15))],
                       (caster, ms("caster"), 3), "This PR, tile variation: mirror, alternate, stagger, ripple",
                       step=STEP, tail=150)
    whole = BV.render([], (full, 30, CF.SCALE), "This PR, one visual on the user: 14x, grid sheet", step=STEP, tail=150)
    n = max(map(len, (plain, varied, whole)))
    W, H = plain[0].size
    out = []
    for i in range(n):
        im = Image.new("RGB", (W, H * 3 + 12), (18, 18, 18))
        for k, panel in enumerate((plain, varied, whole)):
            im.paste(panel[min(i, len(panel) - 1)], (0, k * (H + 6)))
        out.append(im.resize((W * 3 // 4, (H * 3 + 12) * 3 // 4), Image.LANCZOS))
    BV.save(out, os.path.join(HERE, "pr_fcf_before_after.gif"), step=STEP)


if __name__ == "__main__":
    main()
