#!/usr/bin/env python3
"""Profession chest icons (the eight Hunter's / Gatherer's Chests edited by go-live push/339): intake.

Raws arrive two ways from the same generator: native alpha (cleaned as in ic01_07_intake.py), or flattened onto pure
black. A black background cannot be keyed by colour here: the chests' own outline is the same near-black. So for a
black raw the background is the near-black region flood-filled from the canvas border (max channel <= BLACK_T), which
also takes the outline; the outline is then rebuilt by dilating the kept subject by OUTLINE_PX (measured 8-12 px on the
native-alpha raws of the same family) and filling that ring near-black, as the original outline was. Interior blacks
are never touched (the flood only enters from the border). Then the shared ICON framing: trim, even margin, 256 px,
firmed alpha, lossless webp.

usage: python3 state/skyglass_art/profession_chests_intake.py RAW_DIR OUT_DIR WORK_DIR
Pillow only.
"""
import importlib.util
import os
import sys
from collections import deque
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("ic", os.path.join(HERE, "ic01_07_intake.py"))
IC = importlib.util.module_from_spec(_s)
_s.loader.exec_module(IC)

BLACK_T = 6
OUTLINE_PX = 9
OUTLINE_RGB = (2, 2, 3)

# code, raw file, export file, item
CHESTS = [
    ("PC01", "PC01_raw_icon-common-hunters-chest.png", "icon-common-hunters-chest.webp", "Common Hunter's Chest"),
    ("PC02", "PC02_raw_icon-common-gatherers-chest.png", "icon-common-gatherers-chest.webp", "Common Gatherer's Chest"),
    ("PC03", "PC03_raw_icon-rare-hunters-chest.png", "icon-rare-hunters-chest.webp", "Rare Hunter's Chest"),
    ("PC04", "PC04_raw_icon-rare-gatherers-chest.png", "icon-rare-gatherers-chest.webp", "Rare Gatherer's Chest"),
    ("PC05", "PC05_raw_icon-epic-hunters-chest.png", "icon-epic-hunters-chest.webp", "Epic Hunter's Chest"),
    ("PC06", "PC06_raw_icon-epic-gatherers-chest.png", "icon-epic-gatherers-chest.webp", "Epic Gatherer's Chest"),
    ("PC07", "PC07_raw_icon-legendary-hunters-chest.png", "icon-legendary-hunters-chest.webp", "Legendary Hunter's Chest"),
    ("PC08", "PC08_raw_icon-legendary-gatherers-chest.png", "icon-legendary-gatherers-chest.webp", "Legendary Gatherer's Chest"),
]


def unblack(im):
    im = im.convert("RGB")
    w, h = im.size
    px = im.load()
    bg = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.extend([(x, 0), (x, h - 1)])
    for y in range(h):
        q.extend([(0, y), (w - 1, y)])
    while q:
        x, y = q.popleft()
        if bg[y * w + x] or max(px[x, y]) > BLACK_T:
            continue
        bg[y * w + x] = 1
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx]:
                q.append((nx, ny))
    keep = Image.frombytes("L", (w, h), bytes(0 if v else 255 for v in bg))
    grown = keep.filter(ImageFilter.MaxFilter(2 * OUTLINE_PX + 1))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (w, h), OUTLINE_RGB + (255,)), (0, 0), grown)
    rgba = im.convert("RGBA")
    out.paste(rgba, (0, 0), keep)
    return out


def main():
    raw_dir, out_dir, work = sys.argv[1:4]
    os.makedirs(work, exist_ok=True)
    for code, raw, out_name, _ in CHESTS:
        p = os.path.join(raw_dir, raw)
        if not os.path.exists(p):
            print(f"{code} {raw}: not delivered yet")
            continue
        im = Image.open(p)
        if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] < 16:
            img, dust = IC.clean(im)
        else:
            img, dust = IC.clean(unblack(im))
        IC.run(code, img, out_name, out_dir, work)


if __name__ == "__main__":
    main()
