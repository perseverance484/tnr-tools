"""process_jutsu_icon.py RAW SLUG [VER]  -> raw copy + 256x256 lossless WebP (opaque JUTSU_ICON route, RUL-2026-10-14-001).
Square art is resized only (no keying, no retouching). A transparent source is flattened onto black."""
import sys, os
from PIL import Image
src, slug = sys.argv[1], sys.argv[2]
ver = sys.argv[3] if len(sys.argv) > 3 else 'v1'
base = 'art/jutsu_icons/scroll_jutsu'
raw = f'{base}/raws/raw_jutsu_{slug}_{ver}.png'
Image.open(src).save(raw)
im = Image.open(raw)
if im.mode in ('RGBA', 'LA', 'P'):
    im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, (0, 0, 0, 255)); bg.alpha_composite(im); im = bg
im = im.convert('RGB')
w, h = im.size
if abs(w - h) > 0.02 * max(w, h):
    raise SystemExit(f'not square: {w}x{h}')
out = im.resize((256, 256), Image.LANCZOS)
o = f'{base}/exports/icon_jutsu_{slug}_{ver}.webp'
out.save(o, 'WEBP', lossless=True, method=6)
print(raw, im.size, '->', o, os.path.getsize(o))
S = '/tmp/claude-0/-home-user-tnr-tools/ca560e9e-87f0-5f58-92c7-de44dd0b4bbb/scratchpad/'
pv = Image.new('RGB', (256 + 128 + 64 + 32 + 40, 256), (30, 30, 34)); x = 0
for sz in (256, 128, 64, 32):
    pv.paste(out.resize((sz, sz), Image.LANCZOS), (x, 0)); x += sz + 10
pv.save(S + f'jutsu_{slug}_preview.png')
