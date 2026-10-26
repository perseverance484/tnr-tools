"""Side-by-side review cards for the icon overhaul: original vs ours, at tile size and at mobile size."""
import json
from PIL import Image, ImageDraw, ImageFont
Q = json.load(open('docs/design/icon_overhaul/queue.json'))
BG, FG, DIM = (24, 26, 32), (235, 235, 240), (150, 152, 160)
def font(sz, bold=False):
    p = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else '')
    try: return ImageFont.truetype(p, sz)
    except OSError: return ImageFont.load_default()
def tile(path, s):
    im = Image.open(path).convert('RGB')
    return im.resize((s, s), Image.LANCZOS)
for x in Q:
    W, H = 600, 470
    c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    d.text((24, 16), f"{x['n']}/{len(Q)}  {x['name']}", font=font(26, True), fill=FG)
    d.text((24, 50), x['family'], font=font(18), fill=DIM)
    for i, (lab, k) in enumerate((('Original (live now)', 'original_file'), ('Ours (reverted)', 'ours_file'))):
        x0 = 24 + i * 288
        d.text((x0, 86), lab, font=font(18, True), fill=FG)
        c.paste(tile(x[k], 256), (x0, 114))
        sm = tile(x[k], 45); c.paste(sm, (x0, 400))
        c.paste(tile(x[k], 32), (x0 + 60, 406))
        d.text((x0 + 104, 410), 'mobile sizes', font=font(14), fill=DIM)
    c.save(f"docs/design/icon_overhaul/review/{x['n']:02d}_{x['slug']}.png", optimize=True)
print('cards', len(Q))
