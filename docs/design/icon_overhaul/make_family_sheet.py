"""Old vs new comparison sheets for one family, for sharing (e.g. Discord). Usage: make_family_sheet.py "<family>" <out_prefix> [per_sheet]"""
import json, sys
from PIL import Image, ImageDraw, ImageFont
fam, out = sys.argv[1], sys.argv[2]; per = int(sys.argv[3]) if len(sys.argv) > 3 else 4
Q = [x for x in json.load(open('docs/design/icon_overhaul/queue.json')) if x['family'] == fam]
BG, FG, DIM = (24, 26, 32), (235, 235, 240), (150, 152, 160)
F = lambda s, b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
T = 240; CW = 2 * T + 40; COLS = 2
for si in range(0, len(Q), per):
    grp = Q[si:si + per]; rows = (len(grp) + COLS - 1) // COLS
    W = COLS * CW + (COLS + 1) * 30; H = 90 + rows * (T + 80) + 20
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    d.text((30, 22), f"{fam}: old vs new  ({si // per + 1}/{(len(Q) + per - 1) // per})", font=F(30, True), fill=FG)
    for i, x in enumerate(grp):
        cx = 30 + (i % COLS) * (CW + 30); cy = 90 + (i // COLS) * (T + 80)
        d.text((cx, cy), x['name'], font=F(22, True), fill=FG)
        for j, (lab, k) in enumerate((('Old', 'original_file'), ('New', 'ours_file'))):
            px = cx + j * (T + 20)
            c.paste(Image.open(x[k]).convert('RGB').resize((T, T), Image.LANCZOS), (px, cy + 32))
            d.text((px + 6, cy + 36), lab, font=F(18, True), fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    c.save(f"{out}_{si // per + 1}.png", optimize=True)
