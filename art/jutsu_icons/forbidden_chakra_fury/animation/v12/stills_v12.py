#!/usr/bin/env python3
"""Beat stills (and the board GIF with --gif) for FCF v12 on the real board geometry (2026-11-21).

    TNR_DUELYST=<cache> TNR_ART_SCRIPTS=<skill scripts> python3 .../v12/stills_v12.py [--gif]
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "v11"))
import board_v11  # noqa: E402
import build_v12 as B  # noqa: E402

board_v11.B = B
BEATS = [("1 Charge", 240), ("2 Fury", 440), ("3 Shatter", 760), ("4 Storm", 1080), ("5 Settle", 1760)]


def main():
    cs = B.main()
    shots = board_v11.render(cs)
    W, H = shots[0].size
    crop = (int(W * 0.04), 0, int(W * 0.9), H)
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]
    sheet = Image.new("RGB", (cw, (ch + 4) * len(BEATS)), (10, 10, 10))
    for i, (name, t) in enumerate(BEATS):
        im = shots[min(t // 40, len(shots) - 1)].crop(crop)
        ImageDraw.Draw(im).text((8, 6), f"{name}  ({t} ms)", fill=(255, 255, 255))
        sheet.paste(im, (0, i * (ch + 4)))
        im.save(os.path.join(HERE, f"still_{i + 1}_{name.split()[1].lower()}.png"))
    sheet.save(os.path.join(HERE, "stills_fcf_v12.png"))
    if "--gif" in sys.argv:
        board_v11.BV.save(shots, os.path.join(HERE, "preview_fcf_v12_board.gif"))


if __name__ == "__main__":
    main()
