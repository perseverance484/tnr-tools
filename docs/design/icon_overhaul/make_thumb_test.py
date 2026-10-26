"""The 45 px test sheet: every reverted icon (ours and the original) at its real mobile size, plus a grayscale blurred
copy (the silhouette test), sorted by the director's score. Each 45 px image is enlarged 2x with nearest-neighbour so
the sheet shows exactly the pixels a phone shows."""
import json, re
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
B = 'docs/design/icon_overhaul/'
Q = json.load(open(B + 'queue.json'))
score = {int(r[1]): int(r[4].split('/')[0]) for r in (l.split('|') for l in open(B + 'ICON_SCORES.md').read().splitlines() if re.match(r'\| \d+ \|', l))}
F = lambda s, b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
def at45(p): return Image.open(p).convert('RGB').resize((45, 45), Image.LANCZOS)
def big(im): return im.resize((90, 90), Image.NEAREST)
def sil(im): return ImageOps.grayscale(im).filter(ImageFilter.GaussianBlur(1.6)).convert('RGB')
Q = sorted(Q, key=lambda x: (-score[x['n']], x['n']))
CW, CH, COLS = 4 * 94 + 10, 90 + 40, 4
rows = (len(Q) + COLS - 1) // COLS
W, H = COLS * CW + 20, 110 + rows * CH
s = Image.new('RGB', (W, H), (24, 26, 32)); d = ImageDraw.Draw(s)
d.text((14, 12), "45 px test: ours vs original at real phone size, with the blurred grey silhouette", font=F(24, True), fill=(235, 235, 240))
d.text((14, 46), "Per jutsu: ours | ours blurred | original | original blurred.  Sorted by director score.", font=F(17), fill=(165, 168, 178))
d.text((14, 72), "If the blurred copy is a shapeless blob, the icon fails the name test.", font=F(17), fill=(165, 168, 178))
for i, x in enumerate(Q):
    cx, cy = 10 + (i % COLS) * CW, 110 + (i // COLS) * CH
    o, g = at45(x['ours_file']), at45(x['original_file'])
    for k, im in enumerate((o, sil(o), g, sil(g))):
        s.paste(big(im), (cx + k * 94, cy + 22))
    v = score[x['n']]; col = (60, 170, 90) if v >= 9 else (215, 170, 40) if v >= 6 else (205, 70, 60)
    d.text((cx, cy + 2), f"{v}/10", font=F(15, True), fill=col)
    d.text((cx + 52, cy + 2), x['name'][:30], font=F(15), fill=(235, 235, 240))
s.save(B + 'thumb_test_45px.png', optimize=True); print(s.size)
