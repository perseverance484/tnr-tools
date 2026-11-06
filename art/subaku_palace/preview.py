#!/usr/bin/env python3
"""True-scale preview of Subaku Palace on a full 12 x 10 arena and a close-up, light and dark.

    QA=<dir holding the Mother of Echoes qa_preview.py> python3 preview.py [--odd] [--pulse] [--ticks N] [--out DIR]

Reuses the Mother of Echoes harness read-only (qa_preview: CDN 50 px rendition, linear GPU sampling, the player token,
AI avatar placement). Geometry from docs/design/COMBAT_ANIMATION_ENGINE.md: tile box 132 x 66 (the live still's scale),
odd columns half a row lower, clip 165 px square. Board: the real battle still (docs/design/celestial_dew_animation/
battle_still_2026-10-24b.png) tiled by its own hex period (2 columns x 1 row), so the grid and snow are the game's;
dark = the harness's stone-night grade of the same.

Records per cast (round N), in creation order: ground tag (decreasedamagegiven, 60 hexes: static floor under the
fighters, its appear x2 on every hex: client record + server visual; the occupant copy of a damage modifier skips
applySingleEffect, process.ts:657-723, so no third), the SELF buff on the caster, the band visual tags
(one record per hex, x1). Centre-payoff strips (second agent) are composited when present in --centre.
"""
import os
import sys

ARGS = sys.argv[1:]
sys.argv = sys.argv[:1]
HERE = os.path.dirname(os.path.abspath(__file__))
QA = os.environ.get('QA', os.path.join(HERE, '..', '..', '..', 'custom'))
sys.path.insert(0, QA)
import qa_preview as Q  # noqa: E402  (read-only import; it is not modified)
from PIL import Image, ImageDraw  # noqa: E402

sys.path.insert(0, HERE)
import build_domain as BD  # noqa: E402


def arg(name, default=None):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else default


EXP = os.path.join(HERE, 'exports' if os.environ.get('SBK_VARIANT', 'cover') == 'cover' else 'exports_light')
OUT = arg('--out', os.path.join(HERE, 'previews'))
W, H = 12, 10
HW, HH, CP, RP = 132, 66, 99, 66
# clip size: EFFECT_ANIMATION_HEX_RATIO x tile height (1 in upstream main 338126cb; 2.5 at 3314d122). The imported
# module's K is set here (its file is not modified), and its clip() reads it.
Q.K = round(HH * BD.RATIO)
K = Q.K
GATES_DIR = os.environ.get('SBK_GATES', os.path.join(HERE, 'gates', 'exports'))
X0, Y0 = 70, 50
CW, CH = int(X0 + CP * (W - 1) + HW / 2 + 4), int(Y0 + RP * (H - 1) + RP / 2 + HH / 2 + 4)
ODD = '--odd' in ARGS
PULSE = '--pulse' in ARGS
NT = int(arg('--ticks', 48))
CASTER = (6, 4) if ODD else (5, 4)
ENEMIES = {(CASTER[0] + 2, CASTER[1] - 1): 'avatar_moe_worn_porter.webp',
           (CASTER[0] - 3, CASTER[1] + 1): 'avatar_moe_worn_hana.webp',
           (CASTER[0] + 1, CASTER[1] + 3): 'avatar_moe_worn_tomo.webp'}
OUTSIDE = {(CASTER[0] + 5, CASTER[1] + 1): 'avatar_moe_worn_porter.webp'}  # one enemy outside the domain


def pos(col, row):
    return X0 + CP * col, Y0 + RP * row + (RP / 2 if col % 2 else 0)


Q.centre = pos


LPC_STANDIN = None


def draw_player_lpc(im, c):
    """Stand-in for the layered LPC avatar (upstream combatActors.ts: frame 1.8 h x LPC_COMBAT_SCALE 0.75 = 1.35 h,
    centre 0.825 h tile-local y-up; feet at groundY 0.234 h, i.e. 0.266 h below the hex centre). The LPC body fills
    LPC px x 18-46, y 10-62 of its 64 px frame (gates/build_gates.py lpc_body_mask), so the figure is 1.1 h tall,
    0.6 h wide, feet on the contact point. The LPC sheets are not in this repository: a same-size figure stands in."""
    global LPC_STANDIN
    if LPC_STANDIN is None:
        a = Image.open(os.path.join(Q.AV, 'avatar_moe_worn_tomo.webp')).convert('RGBA')
        a = a.crop(a.getbbox())
        hh = round(HH * 52 / 64 * 1.35)
        ww = min(round(HH * 28 / 64 * 1.35 * 1.3), round(a.width * hh / a.height))
        LPC_STANDIN = Q.gpu(Q.rendition(a, 256), ww, hh)
    s = LPC_STANDIN
    x, y = pos(*c)
    feet = y + 0.266 * HH
    im.alpha_composite(s, (int(x - s.width / 2), int(feet - s.height)))


def real_board(dark):
    """Tile the still by its hex period: 198 x 66 px block aligned to its grid (centre at HX, HY)."""
    src = Q.bg_dark if dark else Q.bg_light
    bx, by = int(Q.HX - 66 - CP), int(Q.HY - 225 + 0)  # top-left of a clean block in the top rows
    by = int(Q.HY - 3 * RP) - 0
    block = src.crop((bx, by, bx + 2 * CP, by + RP))
    im = Image.new('RGBA', (CW, CH))
    # align: in the still, column 0 (even) centre is at HX; our column 0 centre is at X0
    sx = (X0 - (Q.HX - bx)) % (2 * CP) - 2 * CP
    sy = (Y0 - (Q.HY - by)) % RP - RP
    y = sy
    while y < CH:
        x = sx
        while x < CW:
            im.paste(block, (int(x), int(y)))
            x += 2 * CP
        y += RP
    return im


def cells_in(r, centre):
    return [(c, w) for c in range(W) for w in range(H) if 0 < BD._dist((c, w), centre) <= r]


def load_clip(name, folder=EXP):
    p = os.path.join(folder, name)
    return Q.clip(p) if os.path.exists(p) else None


GATES = GATES_DIR


def fighter_boxes():
    """Avatar / token boxes (screen px) for the burial check: AI avatar 1.6h square centred 0.4h above the hex centre;
    the player's token from the still."""
    out = {}
    s = round(HH * 1.6)
    for c in list(ENEMIES) + list(OUTSIDE):
        x, y = pos(*c)
        out[c] = (int(x - s / 2), int(y - 0.4 * HH - s / 2), int(x + s / 2), int(y - 0.4 * HH + s / 2))
    x, y = pos(*CASTER)
    if True:  # LPC character avatars are live (303c6cbc)
        hh, ww = round(HH * 52 / 64 * 1.35), round(HH * 28 / 64 * 1.35)
        out[CASTER] = (int(x - ww / 2), int(y + 0.266 * HH - hh), int(x + ww / 2), int(y + 0.266 * HH))
    else:
        tw, th = Q.TOK.size
        out[CASTER] = (int(x + Q.OFF[0]), int(y + Q.OFF[1]), int(x + Q.OFF[0] + tw), int(y + Q.OFF[1] + th))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    tile = Q.tile(os.path.join(EXP, 'tile_sbk_domain_v3.webp'))
    seal = load_clip('anim_sbk_seal_v1.webp')
    pulse = load_clip('anim_sbk_pulse_loop_v1.webp') if PULSE else None
    import json
    meta = json.load(open(os.path.join(EXP, 'subaku_domain_v1.json')))
    waves = []
    for g in meta['groups']:
        fr = load_clip(g['asset'])
        for o in g['offsets']:
            c = (CASTER[0] + o['longitude'], CASTER[1] + o['latitude'])
            if 0 <= c[0] < W and 0 <= c[1] < H:
                waves.append((c, fr))
    domain = cells_in(4, CASTER)
    # the centre half (gates agent, art/subaku_palace/gates): all on the SELF increasedamagegiven record
    gname = os.environ.get('SBK_GATES_STRIP', 'anim_sbk_gates_rise_v6.webp' if BD.RATIO > 1.5 else 'anim_sbk_gates_rise_v3.webp')
    gates = load_clip(gname, GATES) if '--no-gates' not in ARGS else None
    # director 2026-11-05: no lingering buff animation and no dais (the sigil is symbolic and fades after round one)
    master = load_clip('anim_sbk_master_loop_v2.webp', GATES) if '--master' in ARGS else None
    dais = None
    boxes = fighter_boxes()
    tag = f"_r{BD.RATIO:g}_{meta['tile']}_{meta['order']}" + ('_odd' if ODD else '_even') + ('_pulse' if PULSE else '')
    report = {}
    ROUGH = '--rough' in ARGS
    for dark in ((True,) if ROUGH else (False, True)):
        bg = real_board(dark)
        frames, cover, buried = [], [], {c: 0.0 for c in boxes}
        for t in range(NT):
            im = bg.copy()
            # static art, under everything that moves: the floor (ground tag) then the dais (SELF record)
            for c in domain:
                x, y = pos(*c)
                im.alpha_composite(tile, (int(x - HW / 2), int(y - HH / 2)))
            if dais:
                x, y = pos(*CASTER)
                im.alpha_composite(dais, (int(x - HW / 2), int(y - HH / 2)))
            fighters = {**ENEMIES, **OUTSIDE, CASTER: 'player'}
            for c, who in sorted(fighters.items(), key=lambda kv: pos(*kv[0])[1]):
                if who == 'player':
                    draw_player_lpc(im, c)
                else:
                    Q.draw_ai(im, c, who)
            # clips, in creation order: ground records first (per hex: the ground tag's client record + its server
            # visual = the seal x2, its optional loop, then the band visual tag), then the SELF record (gates appear
            # z1, master loop z2)
            fx = Image.new('RGBA', im.size, (0, 0, 0, 0))
            wave_at = {c: fr for c, fr in waves}
            for c in domain:
                x, y = pos(*c)
                at = (int(x - K / 2), int(y - K / 2))
                if seal and t < len(seal):
                    fx.alpha_composite(seal[t], at)
                    fx.alpha_composite(seal[t], at)
                if pulse:
                    fx.alpha_composite(pulse[t % len(pulse)], at)
                fr = wave_at.get(c)
                if fr and t < len(fr):
                    fx.alpha_composite(fr[t], at)
            x, y = pos(*CASTER)
            at = (int(x - K / 2), int(y - K / 2))
            if gates and t < len(gates):
                fx.alpha_composite(gates[t], at)
            if master:
                fx.alpha_composite(master[t % len(master)], at)
            a = fx.getchannel('A')
            cover.append(sum(1 for v in a.getdata() if v > 8) / (CW * CH))
            for c, bx in boxes.items():
                crop = a.crop(bx)
                n = crop.width * crop.height
                buried[c] = max(buried[c], sum(1 for v in crop.getdata() if v >= 160) / n)
            im.alpha_composite(fx)
            frames.append(im.convert('RGB'))
        board = 'dark' if dark else 'light'
        name = f'subaku_arena_{board}{tag}'
        frames[0].save(os.path.join(OUT, name + '.gif'), save_all=True, append_images=frames[1:], duration=50, loop=0)
        x, y = pos(*CASTER)
        box = (int(x - 330), int(y - 210), int(x + 330), int(y + 190))
        cf = [f.crop(box) for f in frames]
        cname = f'subaku_close_{board}{tag}'
        cf[0].save(os.path.join(OUT, cname + '.gif'), save_all=True, append_images=cf[1:], duration=50, loop=0)
        picks = [t for t in ((0, 7, 12, 17, 22, 27, 29, 35) if ROUGH else (0, 6, 8, 10, 12, 14, 16, 19, 21, 23, 29, NT - 1)) if t < NT]
        sw, sh = frames[0].width // 2, frames[0].height // 2
        sheet = Image.new('RGB', (sw * 4, sh * 3 + 18), (12, 14, 18))
        ImageDraw.Draw(sheet).text((4, 3), f'{name}  ticks {picks} @50 ms  |  50 px rendition + linear, true size shown at 1/2  |'
                                   f'  peak clip coverage {100 * max(cover):.0f}% of the arena', fill=(235, 235, 235))
        for i, tt in enumerate(picks):
            sheet.paste(frames[tt].resize((sw, sh), Image.BILINEAR), ((i % 4) * sw, 18 + (i // 4) * sh))
        sheet.save(os.path.join(OUT, name + '_keys.png'))
        cw, ch = cf[0].size
        cs = Image.new('RGB', (cw * 4, ch * 3 + 18), (12, 14, 18))
        ImageDraw.Draw(cs).text((4, 3), f'{cname}  ticks {picks} @50 ms  |  TRUE SIZE (1:1), 50 px rendition + linear',
                                fill=(235, 235, 235))
        for i, tt in enumerate(picks):
            cs.paste(cf[tt], ((i % 4) * cw, 18 + (i // 4) * ch))
        cs.save(os.path.join(OUT, cname + '_keys.png'))
        report[board] = {'peak_cover': round(max(cover), 3), 'mean_cover': round(sum(cover) / len(cover), 3),
                         'max_share_of_fighter_box_under_clip_alpha_ge_160': {f'{c}': round(v, 3) for c, v in buried.items()}}
        print('wrote', name, cname, report[board], flush=True)
    import json
    json.dump(report, open(os.path.join(OUT, f'qa{tag}.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
