"""Discord review sheets: per family, each jutsu shows old vs new with the director's score and feedback."""
import json, re, textwrap
from PIL import Image, ImageDraw, ImageFont
B = 'docs/design/icon_overhaul/'
Q = json.load(open(B + 'queue.json'))
rows = {int(r[1]): (r[4].strip(), r[5].strip()) for r in
        (l.split('|') for l in open(B + 'ICON_SCORES.md').read().splitlines() if re.match(r'\| \d+ \|', l))}
F = lambda s, b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
BG, CARD, FG, DIM = (24, 26, 32), (34, 37, 45), (235, 235, 240), (165, 168, 178)
def col(v): return (60, 170, 90) if v >= 9 else (215, 170, 40) if v >= 6 else (205, 70, 60)
def clean(t): return re.sub(r'\s*\(`[^`]*`[^)]*\)', '', t).strip()
T, PAD, CW = 230, 24, 2 * 230 + 3 * 24
fams = []
for x in Q:
    if not fams or fams[-1][0] != x['family']: fams.append((x['family'], []))
    fams[-1][1].append(x)
sheets = []
for fam, items in fams:
    per = 4 if len(items) > 6 else 6
    chunks = [items[i:i + per] for i in range(0, len(items), per)]
    for ci, ch in enumerate(chunks):
        sheets.append((fam + (f' ({ci + 1}/{len(chunks)})' if len(chunks) > 1 else ''), ch))
out = []
for si, (title, ch) in enumerate(sheets, 1):
    cards = []
    for x in ch:
        score, fb = rows[x['n']]; v = int(score.split('/')[0])
        lines = textwrap.wrap(clean(fb), 44)
        h = 50 + 26 + T + 16 + 44 + len(lines) * 24 + 20
        c = Image.new('RGB', (CW, h), CARD); d = ImageDraw.Draw(c)
        d.text((PAD, 16), x['name'], font=F(24, True), fill=FG)
        for j, (lab, k) in enumerate((('Old', 'original_file'), ('New', 'ours_file'))):
            px = PAD + j * (T + PAD)
            d.text((px, 54), lab, font=F(17, True), fill=DIM)
            c.paste(Image.open(x[k]).convert('RGB').resize((T, T), Image.LANCZOS), (px, 78))
        y = 78 + T + 16
        d.rounded_rectangle((PAD, y, PAD + 96, y + 34), 8, fill=col(v))
        d.text((PAD + 48, y + 17), score, font=F(20, True), fill=(255, 255, 255), anchor='mm')
        y += 44
        for ln in lines: d.text((PAD, y), ln, font=F(18), fill=FG); y += 24
        cards.append(c)
    colsN = 2; gap = 20
    rh = [max(c.height for c in cards[i:i + colsN]) for i in range(0, len(cards), colsN)]
    W = colsN * CW + (colsN + 1) * gap; H = 104 + sum(rh) + gap * (len(rh) + 1)
    s = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(s)
    d.text((gap, 22), f"Icon review: {title}", font=F(30, True), fill=FG)
    d.text((W - gap, 30), f"sheet {si}/{len(sheets)}", font=F(18), fill=DIM, anchor='ra')
    d.text((gap, 66), "Old = original, live now.  New = our icon, reverted.  Scores and notes: first review pass.", font=F(17), fill=DIM)
    y = 104
    for r, i in enumerate(range(0, len(cards), colsN)):
        for k, c in enumerate(cards[i:i + colsN]):
            x0 = gap + k * (CW + gap); d.rectangle((x0, y, x0 + CW - 1, y + rh[r] - 1), fill=CARD); s.paste(c, (x0, y))
        y += rh[r] + gap
    p = f"{B}discord/{si:02d}_{re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')}.png"
    s.save(p, optimize=True); out.append(p)
print('\n'.join(out))
