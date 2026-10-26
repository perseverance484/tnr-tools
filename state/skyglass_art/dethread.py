"""Erase the thin control thread that runs from the top edge into a keyed avatar's head.
Traces the thread row by row from the topmost opaque run, following it within a small x window, clearing
pixels while the run stays thin; stops at the first row where the run widens (the head). Prints rows cleared."""
import sys
from PIL import Image
src, dst, out_preview = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src).convert("RGBA"); W, H = im.size; px = im.load()
MAXW, WIN = 14, 10
def runs(y, x0, x1):
    r, s = [], None
    for x in range(max(0, x0), min(W, x1)):
        if px[x, y][3] > 0:
            if s is None: s = x
        elif s is not None: r.append((s, x)); s = None
    if s is not None: r.append((s, min(W, x1)))
    return r
# start: topmost row with any opaque pixel must be a thin run in the top 3% of the image
y0 = next(y for y in range(H) if runs(y, 0, W))
start = [r for r in runs(y0, 0, W) if r[1] - r[0] <= MAXW]
if y0 > H * 0.03 or not start:
    print("no thread at top", y0); sys.exit(1)
cx = (start[0][0] + start[0][1]) / 2; cleared = 0; y = y0
while y < H:
    rr = [r for r in runs(y, int(cx - WIN - MAXW), int(cx + WIN + MAXW)) if r[0] <= cx + WIN and r[1] >= cx - WIN]
    if not rr: y += 1; continue
    r = min(rr, key=lambda r: abs((r[0] + r[1]) / 2 - cx))
    if r[1] - r[0] > MAXW: break
    for x in range(r[0], r[1]): px[x, y] = (0, 0, 0, 0)
    cx = (r[0] + r[1]) / 2; cleared += 1; y += 1
print("cleared rows", y0, "->", y, "stopped at x", int(cx))
bb = im.getchannel("A").getbbox(); im = im.crop(bb)
side = max(im.size); sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(im, ((side - im.size[0]) // 2, side - im.size[1])); sq.save(dst, "WEBP", lossless=True, method=6)
c = sq.crop((max(0, int(cx * side / W) - 160), 0, min(side, int(cx * side / W) + 160), 320)).resize((320, 320))
bg = Image.new("RGBA", c.size, (235, 235, 235, 255)); bg.alpha_composite(c); bg.save(out_preview)
