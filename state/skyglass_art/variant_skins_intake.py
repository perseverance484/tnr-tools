#!/usr/bin/env python3
"""Skyglass variant skins (VS01-VS19) intake: approved native-alpha raws -> 256 px lossless ICON webps.

Same pipeline as ic01_07_intake.py (alpha cleanup, trim, small even margin, firmed alpha). Raws that arrive without
alpha are refused (regenerate with transparency). Each raw found in RAW_DIR is processed; the rest are skipped.

usage: python3 state/skyglass_art/variant_skins_intake.py RAW_DIR OUT_DIR WORK_DIR
"""
import glob
import importlib.util
import os
import re
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("ic", os.path.join(HERE, "ic01_07_intake.py"))
IC = importlib.util.module_from_spec(_s)
_s.loader.exec_module(IC)
# Thin blades have a high edge-to-area ratio, so the shared post-resize firming leaves >5% partial alpha (artpreflight
# soft_edges); a narrower ramp keeps the edge anti-aliasing to about one pixel.
IC.F_LOW, IC.F_HIGH = 115, 140


def main():
    raw_dir, out_dir, work = sys.argv[1:4]
    os.makedirs(work, exist_ok=True)
    for p in sorted(glob.glob(os.path.join(raw_dir, "VS[0-9][0-9]_raw_icon-variant-*.png"))):
        m = re.match(r"(VS\d\d)_raw_(icon-variant-.+)\.png$", os.path.basename(p))
        code, stem = m.group(1), m.group(2)
        im = Image.open(p)
        if im.mode != "RGBA" or im.getchannel("A").getextrema()[0] > 16:
            raise SystemExit(f"{code}: no transparency; regenerate with a transparent background")
        img, _ = IC.clean(im)
        IC.run(code, img, stem + ".webp", out_dir, work)


if __name__ == "__main__":
    main()
