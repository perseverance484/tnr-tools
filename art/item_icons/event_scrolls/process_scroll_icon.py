"""scroll_icon.py RAW SLUG [T]  -> raw copy, keyed/cleaned 256px lossless WebP, preview."""
import sys, os
from collections import deque
from PIL import Image
src, slug = sys.argv[1], sys.argv[2]
T = int(sys.argv[3]) if len(sys.argv) > 3 else 8
BLO, BHI = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (48, 192)
base = 'art/item_icons/event_scrolls'
VER = os.environ.get('VER', 'v1')
raw = f'{base}/raws/raw_{slug}_{VER}.png'
Image.open(src).save(raw)
im = Image.open(raw).convert('RGBA'); w, h = im.size; px = im.load()
opaque = all(px[x, y][3] == 255 for x, y in [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)])
if opaque:  # black background shares the outline colour: keep black only near artwork
    from PIL import ImageFilter
    R = int(os.environ.get('KEEP_R', '7'))
    rgb = im.convert('RGB')
    lum = rgb.point(lambda v: 255 if v > T else 0).convert('L').point(lambda v: 255 if v > 0 else 0)
    keep = lum.filter(ImageFilter.MaxFilter(2*R+1))
    im.putalpha(keep)
    print('kept', sum(1 for v in keep.get_flattened_data() if v), 'of', w*h, 'R', R)
else:
    r, g, b, a = im.split(); a = a.point(lambda v: 255 if v >= 224 else (0 if v <= 24 else v)); im = Image.merge('RGBA', (r, g, b, a))
bb = im.getchannel('A').getbbox(); crop = im.crop(bb); cw, ch = crop.size
side = int(max(cw, ch)/0.90); can = Image.new('RGBA', (side, side), (0, 0, 0, 0)); can.paste(crop, ((side-cw)//2, (side-ch)//2))
out = can.resize((256, 256), Image.LANCZOS)
r, g, b, a = out.split(); a = a.point(lambda v: 255 if v >= BHI else (0 if v <= BLO else v)); out = Image.merge('RGBA', (r, g, b, a))
p2 = out.load()
for y in range(256):
    for x in range(256):
        if p2[x, y][3] == 0: p2[x, y] = (0, 0, 0, 0)
o = f'{base}/exports/icon_{slug}_{VER}.webp'
out.save(o, 'WEBP', lossless=True, method=6, exact=True)
vals = list(out.getchannel('A').get_flattened_data()); vis = sum(v > 0 for v in vals); part = sum(0 < v < 255 for v in vals)
print(o, os.path.getsize(o), 'bbox', bb, 'partial% visible', round(100*part/vis, 2))
S = '/tmp/claude-0/-home-user-tnr-tools/ca560e9e-87f0-5f58-92c7-de44dd0b4bbb/scratchpad/'
pv = Image.new('RGB', (784, 384), 'white')
for i, bg in enumerate([(24, 24, 28), (235, 235, 235)]):
    c = Image.new('RGBA', (256, 256), bg+(255,)); c.alpha_composite(out); pv.paste(c.convert('RGB').resize((384, 384), Image.NEAREST), (i*400, 0))
pv.save(S+f'{slug}_preview.png')
