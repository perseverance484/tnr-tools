#!/usr/bin/env python3
"""Independent QA render of Subaku Palace (2.5h clip, 50 px rendition, linear). Imports qa_preview read-only.
usage: python3 qa_render.py even|odd [skew]"""
import os, sys, json
os.environ['LPC'] = '1'; os.environ['CLIP_RATIO'] = '2.5'
SP = '/tmp/claude-0/-home-claude/7b0c37c7-23de-5628-97e5-5a20d2af594f/scratchpad'
sys.path.insert(0, SP + '/custom')
PAR = sys.argv[1]; SKEW = len(sys.argv) > 2
sys.argv = sys.argv[:1]
import qa_preview as Q
from PIL import Image, ImageDraw

A = SP + '/subaku/art/subaku_palace/'
OUT = SP + '/sbk_qa2/'
HW, HH, K = 132, 66, Q.K
X0, YB = 110, 830
W, H = X0 * 2 + 99 * 12, YB + 120


def pos(c, r):
    return X0 + 99 * c, YB - 66 * r - (33 if c & 1 else 0)


Q.centre = pos
# board: the still's own 2-column period
per = Q.bg_light.crop((262, 193, 460, 259)); perd = Q.bg_dark.crop((262, 193, 460, 259))


def board(p):
    b = Image.new('RGBA', (W, H))
    for i in range(-1, W // 198 + 2):
        for j in range(-2, H // 66 + 2):
            b.paste(p, (X0 - 49 + 198 * i, YB - 33 - 66 * j))
    return b


BL, BD = board(per), board(perd)


def cube(c, r):
    return c, r - (c - (c & 1)) // 2


def dist(a, b):
    (q1, r1), (q2, r2) = cube(*a), cube(*b)
    dq, dr = q1 - q2, r1 - r2
    return max(abs(dq), abs(dr), abs(dq + dr))


CASTER = (6, 5) if PAR == 'even' else (7, 5)
DOMAIN = [(c, r) for c in range(13) for r in range(11) if 0 < dist((c, r), CASTER) <= 4]
meta = json.load(open(A + 'exports/subaku_domain_v1.json'))
BANDS = []
for gi, g in enumerate(meta['groups']):
    cells = [(CASTER[0] + o['longitude'], CASTER[1] + o['latitude']) for o in g['offsets']]
    BANDS.append((g['asset'], g['lands_tick'], cells))
tagged = {c for _, _, cs in BANDS for c in cs}
untagged = [c for c in DOMAIN if c not in tagged]
outside_tag = [c for c in tagged if c not in DOMAIN]
ringerr = []
for _, land, cs in BANDS:
    for c in cs:
        d = dist(c, CASTER); true_land = int(4 + 3 * d + 0.5)
        ringerr.append((c, d, land, land - true_land))
TILE = Q.tile(A + 'exports/tile_sbk_domain_v4.webp')
SEAL = Q.clip(A + 'exports/anim_sbk_seal_v2.webp')
GATES = Q.clip(A + 'gates/exports/anim_sbk_gates_rise_v6.webp')
WAVE = {a: Q.clip(A + 'exports/' + a) for a, _, _ in BANDS}
# fighters: caster LPC; enemies LPC at ring1 above/below, ring 2, ring 4; AI originals at ring 1/3
dc = CASTER[0]
LPCS = {CASTER: 'caster', (dc, 6): 'lpc_r1_above', (dc, 4): 'lpc_r1_below', (dc - 2, 5): 'lpc_r2', (dc + 4, 5): 'lpc_r4'}
AIS = {(dc + 1, 5): 'avatar_moe_worn_porter.webp', (dc - 3, 7): 'avatar_moe_worn_hana.webp', (dc + 2, 3): 'avatar_moe_worn_tomo.webp'}
START = {}  # per-asset start offset in ticks (skew sim)
if SKEW:
    START = {'tile': 4, 'seal': 4, 'anim_sbk_wave_b0_v1.webp': 3, 'anim_sbk_wave_b5_v1.webp': -2, 'anim_sbk_wave_b6_v1.webp': 0}


def meters(d, x, y, ai):
    bot = y + HH / 2
    top = 1.99 if ai else 1.5  # hudTop (h above hex bottom), combatActors.ts:119-124
    for i, col in enumerate([(178, 34, 34), (0, 128, 0), (0, 0, 255)]):
        z0 = (top - 0.1 * i) * HH
        d.rectangle([x - HW / 4, bot - z0 - 0.1 * HH, x + HW / 4, bot - z0], fill=col, outline=(0, 0, 0))


def actors(im, maskmode=False):
    masks = {}
    cells = sorted(list(LPCS) + list(AIS), key=lambda c: -pos(*c)[1])
    for c in cells:
        x, y = pos(*c)
        if maskmode:
            t = Image.new('RGBA', (W, H)); m2 = Image.new('RGBA', (W, H))
            (Q.draw_ai(t, c, AIS[c]) if c in AIS else Q.draw_player(t, c))
            meters(ImageDraw.Draw(m2), x, y, c in AIS)
            masks[c] = (t.getchannel('A').point(lambda v: 255 if v > 128 else 0), m2.getchannel('A'))
        else:
            (Q.draw_ai(im, c, AIS[c]) if c in AIS else Q.draw_player(im, c))
            meters(ImageDraw.Draw(im), x, y, c in AIS)
    return masks


def frame_at(fr, t):
    return fr[t] if 0 <= t < len(fr) else None


def clips(t):
    L = Image.new('RGBA', (W, H))
    def put(f, c):
        if f is None: return
        x, y = pos(*c)
        L.alpha_composite(f, (int(x - K / 2), int(y - K / 2)))
    so = START.get('seal', 0)
    for c in DOMAIN:
        put(frame_at(SEAL, t - so), c); put(frame_at(SEAL, t - so), c)
    for a, _, cs in BANDS:
        o = START.get(a, 0)
        for c in cs: put(frame_at(WAVE[a], t - o), c)
    put(frame_at(GATES, t), CASTER)
    return L


def render(bg, t):
    im = bg.copy()
    if t >= START.get('tile', 0):
        for c in DOMAIN:
            x, y = pos(*c); im.alpha_composite(TILE, (int(x - HW / 2), int(y - HH / 2)))
    actors(im)
    L = clips(t)
    im.alpha_composite(L)
    return im, L


if __name__ == '__main__':
    tag = PAR + ('_skew' if SKEW else '')
    masks = actors(None, True)
    NT = 40
    stats = {str(c): [] for c in masks}
    os.makedirs(OUT + 'f_' + tag, exist_ok=True)
    gl, gd = [], []
    for t in range(NT):
        a, L = render(BL, t); b, _ = render(BD, t)
        al = L.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
        for c, (bm, mm) in masks.items():
            def cov(m):
                tot = m.histogram()[255]
                inter = Image.composite(al, Image.new('L', al.size, 0), m).histogram()[255]
                return round(inter / tot, 3) if tot else 0
            stats[str(c)].append((cov(bm), cov(mm)))
        a.convert('RGB').save(OUT + f'f_{tag}/light_{t:02d}.png'); b.convert('RGB').save(OUT + f'f_{tag}/dark_{t:02d}.png')
        gl.append(a.convert('RGB').resize((W // 2, H // 2), Image.LANCZOS)); gd.append(b.convert('RGB').resize((W // 2, H // 2), Image.LANCZOS))
    gl[0].save(OUT + f'arena_light_{tag}.gif', save_all=True, append_images=gl[1:], duration=50, loop=0)
    gd[0].save(OUT + f'arena_dark_{tag}.gif', save_all=True, append_images=gd[1:], duration=50, loop=0)
    rep = {'caster': CASTER, 'untagged_domain_hexes': untagged, 'tagged_outside_domain': outside_tag,
           'ring_err_ticks': sorted({e for *_, e in ringerr}),
           'n_off': sum(1 for *_, e in ringerr if e), 'n_tag': len(ringerr),
           'off_list': [(c, d, l, e) for c, d, l, e in ringerr if e],
           'labels': {str(c): LPCS.get(c, AIS.get(c)) for c in masks}, 'cover': stats}
    json.dump(rep, open(OUT + f'stats_{tag}.json', 'w'), indent=0)
    print(json.dumps({k: rep[k] for k in ('caster', 'untagged_domain_hexes', 'tagged_outside_domain', 'ring_err_ticks', 'n_off', 'n_tag')}))
    for c, s in stats.items():
        bm = [x for x, _ in s]; mm = [y for _, y in s]
        print(rep['labels'][c], c, 'body max %.2f (t%d) frames>25%%: %d' % (max(bm), bm.index(max(bm)), sum(v > .25 for v in bm)),
              '| meters max %.2f (t%d) frames>25%%: %d' % (max(mm), mm.index(max(mm)), sum(v > .25 for v in mm)))
