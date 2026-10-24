"""Measure the 51 reverted icons (ours and the originals) as players see them, against the director's scores.

Metrics at 45 px (mobile battle bar): busyness (edge density), focal contrast (centre vs border luminance),
silhouette clarity (share of the largest bright blob), palette spread, radial sameness (similarity to its own
90/180-degree rotations; high = centred swirl/burst), and distinctness from family siblings at 32 px.
"""
import json, re, math, statistics as st
from PIL import Image, ImageFilter, ImageOps
B = 'docs/design/icon_overhaul/'
Q = json.load(open(B + 'queue.json'))
score = {int(r[1]): int(r[4].split('/')[0]) for r in (l.split('|') for l in open(B + 'ICON_SCORES.md').read().splitlines() if re.match(r'\| \d+ \|', l))}

def load(p, s): return Image.open(p).convert('RGB').resize((s, s), Image.LANCZOS)
def lum(im): return list(im.convert('L').get_flattened_data())

def metrics(path):
    im = load(path, 45); L = lum(im); n = 45
    E = lum(im.convert('L').filter(ImageFilter.FIND_EDGES).convert('RGB'))
    busy = sum(1 for v in E if v > 40) / len(E)
    cen = [L[y * n + x] for y in range(12, 33) for x in range(12, 33)]
    bor = [L[y * n + x] for y in range(n) for x in range(n) if x < 6 or x > 38 or y < 6 or y > 38]
    focal = (st.mean(cen) - st.mean(bor)) / 255
    thr = sorted(L)[int(len(L) * 0.7)]
    mask = [v >= thr for v in L]; seen = [False] * len(L); comps = []
    for i in range(len(L)):
        if mask[i] and not seen[i]:
            stack = [i]; seen[i] = True; c = 0
            while stack:
                k = stack.pop(); c += 1; y, x = divmod(k, n)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < n and 0 <= xx < n:
                        j = yy * n + xx
                        if mask[j] and not seen[j]: seen[j] = True; stack.append(j)
            comps.append(c)
    sil = max(comps) / sum(comps)
    g = ImageOps.grayscale(load(path, 24)); a = list(g.get_flattened_data())
    def sim(b): return 1 - sum(abs(x - y) for x, y in zip(a, list(b.get_flattened_data()))) / (255 * len(a))
    radial = (sim(g.rotate(90)) + sim(g.rotate(180))) / 2
    hues = set(); hsv = im.convert('HSV')
    for h, s_, v in hsv.get_flattened_data():
        if s_ > 60 and v > 60: hues.add(h // 32)
    return dict(busy=busy, focal=focal, sil=sil, radial=radial, hues=len(hues), mean=st.mean(L) / 255, std=st.pstdev(L) / 255)

def vec(path): return [c for px in load(path, 16).get_flattened_data() for c in px]
def dist(a, b): return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))) / (255 * math.sqrt(len(a)))

def spearman(x, y):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2
            i = j + 1
        return r
    a, b = rk(x), rk(y); ma, mb = st.mean(a), st.mean(b)
    num = sum((p - ma) * (q - mb) for p, q in zip(a, b)); den = math.sqrt(sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b))
    return num / den

rows = []
for x in Q:
    mo, mn = metrics(x['original_file']), metrics(x['ours_file'])
    rows.append(dict(n=x['n'], name=x['name'], family=x['family'], score=score[x['n']], ours=mo and mn, orig=mo))
# family distinctness (ours): mean distance to nearest sibling
fam = {}
for x in Q: fam.setdefault(x['family'], []).append(x)
for r in rows:
    x = next(q for q in Q if q['n'] == r['n']); sib = [q for q in fam[x['family']] if q['n'] != x['n']]
    for key, f in (('ours', 'ours_file'), ('orig', 'original_file')):
        r[key]['nearest_sibling'] = min(dist(vec(x[f]), vec(q[f])) for q in sib) if sib else None
keys = ['busy', 'focal', 'sil', 'radial', 'hues', 'mean', 'std', 'nearest_sibling']
out = {'per_icon': rows, 'correlation_with_score_ours': {}, 'means': {}}
sc = [r['score'] for r in rows]
for k in keys:
    v = [r['ours'][k] for r in rows]
    ok = [(a, b) for a, b in zip(v, sc) if a is not None]
    out['correlation_with_score_ours'][k] = round(spearman([a for a, _ in ok], [b for _, b in ok]), 2)
    for grp, sel in (('ours_10', lambda r: r['score'] == 10), ('ours_0to4', lambda r: r['score'] <= 4), ('ours_all', lambda r: True)):
        vals = [r['ours'][k] for r in rows if sel(r) and r['ours'][k] is not None]
        out['means'].setdefault(k, {})[grp] = round(st.mean(vals), 3)
    out['means'][k]['originals_all'] = round(st.mean([r['orig'][k] for r in rows if r['orig'][k] is not None]), 3)
json.dump(out, open(B + 'analysis_45px.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps({'corr': out['correlation_with_score_ours'], 'means': out['means']}, indent=1))
