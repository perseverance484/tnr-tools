"""True-scale mockup of a TNR sector map, following the client's drawing rules.

Rules (from app/src/libs/rendering/sectorSprites.ts, sprites.ts, hexgrid.ts):
- flat-top hexes, width = hexsize, height h = hexsize*0.5; columns 0.75*width apart; odd columns half a row up.
- world is Y-up: row 0 is the bottom of the screen.
- decoration: size = h * scale * heightScale; library uploads (no frame) are drawn SQUARE (size x size);
  atlas trees keep aspect (height = size), heightScale 1.2.
  sprite bottom = tile bottom edge lifted by 0.1*size; x = tile.x + width*offsetX.
- small:true decorations use the 50px rendition (nearest sampling).
- map locations (wrecks): height = h * asset.renderScale(2.4) * location scale, keep aspect,
  anchorY 0.85 at tile.y + h/10.
- decorations are skipped on structure and location tiles.
"""
import json, sys, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageChops

S = '/tmp/claude-0/-home-user/bdca9902-ac7d-58cd-bb4b-b0c1a9fcc6c3/scratchpad/'
mp = json.load(open(sys.argv[1])); out = sys.argv[2]
crop = sys.argv[3] if len(sys.argv) > 3 else None
N = 26
data = mp['layers'][0]['data']
CODE = {1: 'ocean', 2: 'ground', 3: 'dessert', 4: 'ice', 5: 'dessert'}
s282 = json.load(open(S + 'map3/s282.json'))
T282 = {'G': 'ground', 'D': 'dessert', 'O': 'ocean'}

h = 36.0; w = 2 * h; colsp = 0.75 * w
ROW_MIN, ROW_MAX = -5, 9          # rows of 210 shown (negative = sector 282's top rows)
MX = 20
W = int(MX * 2 + (N - 1) * colsp + w)
TOPPAD = 9 * h
H = int(TOPPAD + (ROW_MAX - ROW_MIN + 1.5) * h)
Y0 = H - h * 0.75 + ROW_MIN * h    # screen y of row 0 centre (even col)

def pos(c, r):
    return MX + w / 2 + c * colsp, Y0 - r * h - (h / 2 if c % 2 else 0)

def terr(c, r):
    if not (0 <= c < N): return None
    if r >= 0:
        return CODE[data[r * N + c]] if r < N else None
    rr = 26 + r
    row = s282['terr'].get(str(rr))
    return T282[row[c]] if row else 'ground'

def nbrs(c, r):
    dd = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, -1), (-1, -1)] if c % 2 == 0 else [(1, 0), (-1, 0), (0, -1), (0, 1), (1, 1), (-1, 1)]
    return [(c + a, r + b) for a, b in dd]

def water_dist(c, r):
    seen = {(c, r)}; fr = [(c, r)]
    for k in range(1, 4):
        nf = []
        for p in fr:
            for q in nbrs(*p):
                if q in seen: continue
                seen.add(q); t = terr(*q)
                if t is not None and t != 'ocean': return k
                nf.append(q)
        fr = nf
    return 9

# night palette: ocean/ground sampled from the director's screenshot, the rest = stock colours x night tint
MUL = (0.42, 0.48, 0.55); ADD = (2, 5, 14)
def night(rgb): return tuple(int(min(255, v * m + a)) for v, m, a in zip(rgb, MUL, ADD))
PAL = {
    'ground': [(45, 67, 52), (43, 65, 51), (40, 61, 49)],
    'dessert': [night((0xcf, 0xb7, 0x87)), night((0xc3, 0xa9, 0x77)), night((0xb6, 0xa0, 0x6f))],
    'ice': [night((0xb0, 0xcd, 0xd4)), night((0xaa, 0xc8, 0xd0)), night((0x9e, 0xbe, 0xc9))],
}
OCEAN = {1: (54, 84, 93), 2: (38, 69, 87), 3: (30, 62, 84), 9: (26, 58, 81)}

img = Image.new('RGBA', (W, H), (26, 58, 81, 255))
d = ImageDraw.Draw(img)
def hexpts(x, y, s=1.0):
    return [(x - w / 2 * s, y), (x - w / 4 * s, y - h / 2 * s), (x + w / 4 * s, y - h / 2 * s),
            (x + w / 2 * s, y), (x + w / 4 * s, y + h / 2 * s), (x - w / 4 * s, y + h / 2 * s)]
rnd = random.Random(7)
order = sorted([(c, r) for r in range(ROW_MIN - 1, ROW_MAX + 6) for c in range(N)], key=lambda p: -pos(*p)[1])
for c, r in order:
    t = terr(c, r)
    if t is None: continue
    x, y = pos(c, r)
    if t == 'ocean':
        col = OCEAN[water_dist(c, r)]
    else:
        col = PAL[t][(c * 7 + r * 13) % 3]
    d.polygon(hexpts(x, y, 1.01), fill=col)
# land edges: stock ocean is recessed 0.18 of the tile edge, so land shows a bank where it meets water below it
for c, r in order:
    t = terr(c, r)
    if t in (None, 'ocean'): continue
    x, y = pos(c, r)
    for (nc, nr) in nbrs(c, r):
        if terr(nc, nr) == 'ocean' and nc == c and nr == r - 1:
            nx, ny = pos(nc, nr)
            # the shared edge between the two hexes
            mx, my = (x + nx) / 2, (y + ny) / 2
            dx, dy = nx - x, ny - y
            L = math.hypot(dx, dy); ex, ey = -dy / L * w / 4, dx / L * w / 4
            dep = h * 0.18
            bank = (max(0, col_[0]) for col_ in [PAL[t][0]])
            bc = tuple(int(v * 0.55) for v in PAL[t][0])
            d.polygon([(mx + ex, my + ey), (mx - ex, my - ey), (mx - ex, my - ey + dep), (mx + ex, my + ey + dep)], fill=bc)
# faint hex lines
lines = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lines)
for c, r in order:
    if terr(c, r) is None: continue
    ld.polygon(hexpts(*pos(c, r)), outline=(0, 0, 0, 28))
img = Image.alpha_composite(img, lines)
d = ImageDraw.Draw(img)

# ---------- sprites ----------
def tint(im):
    r, g, b, a = im.split()
    r = r.point(lambda v: v * MUL[0] + ADD[0]); g = g.point(lambda v: v * MUL[1] + ADD[1]); b = b.point(lambda v: v * MUL[2] + ADD[2])
    return Image.merge('RGBA', (r, g, b, a))
atlas = Image.open(S + 'gameart/woodland_atlas.png').convert('RGBA')
FR = {'oak': (22.5, 38, 124.5, 138), 'golden-tree': (184, 41, 119.5, 137.5), 'cedar': (338.5, 34, 110, 147),
      'shrine': (341.5, 222, 119, 124), 'lantern': (353, 375, 86, 111.5), 'reeds': (26.5, 507.5, 112.5, 98.5),
      'rocks': (16.5, 379.5, 133.5, 104), 'stones': (497.5, 521, 103.5, 85)}
cache = {}
def frame(name):
    if name not in cache:
        x, y, fw, fh = FR[name]
        cache[name] = tint(atlas.crop((round(x), round(y), round(x + fw), round(y + fh))))
    return cache[name]
TREE = {'tree.green.round': 'oak', 'tree.green.tall': 'cedar', 'tree.green.wide': 'golden-tree'}
PROPS = {}
SMALL = {'kelp', 'planks'}
def prop(n):
    if n not in PROPS:
        im = Image.open(S + f'art/sq/wreck_{n}_b.webp').convert('RGBA')
        if n in SMALL:   # 50px rendition, nearest
            im = im.resize((50, 50), Image.LANCZOS)
        PROPS[n] = tint(im)
    return PROPS[n]
DESERT_BIOME = True
dr = Image.open(S + 'gameart/desert_rocks.png').convert('RGBA')
bs = Image.open(S + 'gameart/biome_scenery.png').convert('RGBA')
DRF = {'rock.grey': (258, 2, 122, 83), 'rock.slate': (386, 2, 124, 97), 'rock.sand': (130, 2, 125, 92)}
BSF = {'rock.grey': (22.5, 381.5, 121.5, 83), 'rock.slate': (177, 365.5, 124, 96.5), 'rock.sand': (483, 225, 125, 91.5)}
def rock(k, dry):
    key = (k, dry)
    if key not in cache:
        x, y, fw, fh = (DRF if dry else BSF)[k]
        cache[key] = tint((dr if dry else bs).crop((round(x), round(y), round(x + fw), round(y + fh))))
    return cache[key]
wreck = tint(Image.open(S + 'gameart/skyglass_wreck.png').convert('RGBA'))

sprites = []   # (groundY, image, left, top)
def add(im, cx, bottom, size, keep, nearest=True, gy=None):
    sw = size * im.width / im.height if keep else size
    rs = im.resize((max(1, round(sw)), max(1, round(size))), Image.NEAREST if nearest else Image.LANCZOS)
    sprites.append((gy if gy is not None else bottom, rs, cx - sw / 2, bottom - size))

def rc(o):
    p = {q['name']: q['value'] for q in o.get('properties', [])}
    if 'gridX' in p: return p['gridX'], p['gridY'], p
    c = round((o['x'] - 32) / 48); r = round((o['y'] - (28 if c % 2 else 0) - 28) / 56)
    return c, r, p

# locations of 210 (wrecks) and the shrine; decorations skip these tiles
LOC = {(7, 1): 3, (21, 6): 5}
SHRINE = (13, 5)
blocked_deco = set(LOC) | {SHRINE}
courts = []
for (c, r), ss in LOC.items():
    x, y = pos(c, r); size = h * 2.4 * ss
    ay = y - h / 10
    add(wreck, x, ay + 0.15 * size, size, True, gy=ay)
    courts.append((x, y, wreck.width / wreck.height * size * 0.62, h * 0.9))
x, y = pos(*SHRINE); size = h * 3.6
add(frame('shrine'), x, y + 0.15 * size - 0.85 * size + size * 0.85, size, True, gy=y)  # base on tile centre
courts.append((x, y, w * 0.9, h * 0.8))

def deco(c, r, p):
    k = p['assetKey']; s = float(p.get('scale', 1)); ox = float(p.get('offsetX', 0)); oy = float(p.get('offsetY', 0))
    x, y = pos(c, r); x += w * ox
    if k in TREE:
        size = h * s * 1.2
        add(frame(TREE[k]), x, y + h / 2 - 0.1 * size - h * oy, size, True)
    elif k.startswith('rock.'):
        dry = terr(c, r) == 'dessert' and DESERT_BIOME
        im = rock(k, dry); size = h * s * {'rock.slate': 0.45, 'rock.grey': 0.35, 'rock.sand': 0.4}[k]
        add(im, x, y + h / 2 - 0.1 * size - h * oy, size, True)
    elif k.startswith('grass'):
        # ground detail art is tiny (0.28-0.34 tile heights)
        sprites.append((y + h / 2, 'dry' if terr(c, r) == 'dessert' else None, x, y + h * 0.3 - h * oy))
    elif k.startswith('wreck.skyglass.'):
        n = k.split('.')[-1]; size = h * s
        add(prop(n), x, y + h / 2 - 0.1 * size - h * oy, size, False, nearest=True)

for o in mp['layers'][1]['objects']:
    if o.get('type') != 'decoration': continue
    c, r, p = rc(o)
    if (c, r) in blocked_deco: continue
    deco(c, r, p)
for o in s282['objs']:
    deco(o['x'], o['y'] - 26, {'assetKey': {'R': 'tree.green.round', 'T': 'tree.green.tall', 'W': 'tree.green.wide', 'g': 'grass.tuft'}[o['k']], 'scale': o['scale']})

# courts: a sandy apron in front of each location (the game draws an entrance court)
ct = Image.new('RGBA', img.size, (0, 0, 0, 0)); cd = ImageDraw.Draw(ct)
for x, y, cw, chh in courts:
    cd.ellipse((x - cw / 2, y - chh * 0.2, x + cw / 2, y + chh), fill=PAL['dessert'][1] + (255,))
ct = ct.filter(ImageFilter.GaussianBlur(h * 0.12))
img = Image.alpha_composite(img, ct)

sprites.sort(key=lambda s: s[0])
for gy, im, left, top in sprites:
    if im is None or im == 'dry':
        d = ImageDraw.Draw(img)
        if im == 'dry':
            for dx in (-3, 0, 3):
                d.line((left + dx, top + 2, left + dx * 1.6, top - 5), fill=(98, 96, 72, 255), width=1)
        else:
            d.ellipse((left - 2, top - 1, left + 2, top + 1), fill=(36, 58, 42, 255))
        continue
    img.alpha_composite(im, (round(left), round(top)))

if crop:
    x0, y0, x1, y1 = map(float, crop.split(','))
    img = img.crop((int(x0), int(y0), int(x1), int(y1)))
img.convert('RGB').save(out)
print(out, img.size, 'h=', h)
