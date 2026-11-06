#!/usr/bin/env python3
"""Build the Subaku Palace art jobs (jutsu jELEiw5W3N4m2R3oJm3Pk; docs/design/SUBAKU_PALACE_ANIMATION.md).

    python3 push/subaku_palace.gen.py                    -> push/503_subaku_palace_assets.json
    python3 push/subaku_palace.gen.py unhide <503 bundle> -> push/504_subaku_palace_unhide.json
    python3 push/subaku_palace.gen.py jutsu  <503 bundle> -> push/505_subaku_palace_jutsu.json

503 (direct): creates the 10 art assets HIDDEN (law 16b) in folder JutsuSubakuPalace (RUL-2026-11-05-127, folder
    per RUL-2026-11-06-130), and reads the live jutsu back in full (capture.before, jutsu.get, persist full). It
    changes no jutsu: an edit replaces the effects array, so it must be built from the live record, and the
    repository holds no full capture of this jutsu.
504 (direct): unhides those assets by literal id from the 503 bundle's idmap (law 16c: battles load only unhidden
    assets). Run before 505.
505 (suggest mode, the player-jutsu precedent push/240): edits the jutsu from the 503 capture.
    - Ground decreasedamagegiven: staticAssetPath -> the domain floor; appearAnimation -> the seal; appearSfx ""
      (the Heal sound played about 120 times per cast).
    - SELF increasedamagegiven: appearAnimation -> the gates rise; appearSfx -> Earth (once per cast);
      staticAssetPath and staticAnimation cleared.
    - 7 visual tags (COORDINATES, origin CASTER, the band offsets, power 2, rounds 1), one per half-ring band, each
      carrying its band's wave strip.
    - Every other field of every effect, and every jutsu field, is re-sent exactly as captured. The generator
      refuses a record whose mechanics do not match the design (power, rounds, target, friendlyFire, calculation).
      injectableInBattle is re-sent at its live value (law 20).
    Law 18 (editing an equipped jutsu severs an AI's combat link): Subaku Palace is a player EVENT jutsu, and no AI
    in the repository's records holds it. An AI outside the census that holds it is not covered.
The image pack is pinned at HEAD: commit the exports first. Generated files; do not hand-edit them.
"""
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
JID = 'jELEiw5W3N4m2R3oJm3Pk'
FOLDER = 'JutsuSubakuPalace'
E = 'art/subaku_palace/exports/'
G = 'art/subaku_palace/gates/exports/'
EARTH = 'XBlRonNjvwAZx1_HFpHdM'
HEAL = '4iG_WpgEmPGUzHn8z129r'
BAND_LABELS = ['1', '1.5', '2', '2.5', '3', '3.5', '4']
META = json.load(open(E + 'subaku_domain_v1.json'))
TILE = next(n for n, a in META['assets'].items() if a.get('type') == 'STATIC')

# srcId, library name, path, type, frames, speed (ms per frame)
ASSETS = [('sbk_floor', 'Subaku Palace: domain floor', E + TILE, 'STATIC', 1, 1),
          ('sbk_seal', 'Subaku Palace: domain seal', E + 'anim_sbk_seal_v2.webp', 'ANIMATION', 36, 50)]
for k, g in enumerate(META['groups']):
    ASSETS.append((f'sbk_wave_b{k}', f'Subaku Palace: ring {BAND_LABELS[k]} wave', E + g['asset'], 'ANIMATION', 36, 50))
ASSETS.append(('sbk_gates', 'Subaku Palace: gates rise', G + 'anim_sbk_gates_rise_v6.webp', 'ANIMATION', 44, 50))

# the design's mechanics (unchanged): the generator refuses a live record that differs
SELF_FX = {'type': 'increasedamagegiven', 'target': 'SELF', 'power': 30, 'rounds': 2}
GROUND_FX = {'type': 'decreasedamagegiven', 'power': 15, 'rounds': 3}

N_CREATE, N_UNHIDE, N_JUTSU = 503, 504, 505


def write(path, m):
    json.dump(m, open(path, 'w'), indent=1, ensure_ascii=False)
    open(path, 'a').write('\n')


def build_create():
    from PIL import Image
    ref = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    pack, sizes, items = {}, {}, []
    for src, name, path, typ, frames, speed in ASSETS:
        w, h = Image.open(path).size
        assert (w, h) == ((128, 128) if typ == 'STATIC' else (150, 150 * frames)), (path, w, h)
        b = open(path, 'rb').read()
        assert subprocess.check_output(['git', 'show', f'{ref}:{path}']) == b, f'commit {path} first'
        fn = os.path.basename(path)
        pack[fn] = {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
        sizes[fn] = len(b)
        items.append({"entity": "asset", "slot": "create", "srcId": src, "name": name,
                      "data": {"name": name, "type": typ, "folder": FOLDER, "frames": frames, "speed": speed,
                               "hidden": True, "onInitialBattleField": False, "licenseDetails": "TNR",
                               "image": "@img:" + fn}, "phase": 10})
    m = {"_note": (f"push/{N_CREATE}: Subaku Palace art (jutsu {JID}). Creates the {len(items)} art assets HIDDEN "
                   f"(law 16b) in folder {FOLDER}: the domain floor (static, the director's tile joined), the "
                   "domain seal, the 7 ring waves and the gates rise. Reads the jutsu back in full (capture.before) "
                   f"for push/{N_JUTSU}; changes no jutsu. Then push/{N_UNHIDE} (unhide) and push/{N_JUTSU} (the "
                   "jutsu, suggest mode), both built from this run's results bundle. Generated by "
                   "push/subaku_palace.gen.py; do not hand-edit."),
         "dedupNames": True,
         "imgSizes": sizes,
         "imagePack": {"ref": ref, "files": pack},
         "capture": {"before": [{"proc": "jutsu.get", "input": {"id": JID}, "persist": "full"}], "after": []},
         "items": items}
    out = f'push/{N_CREATE}_subaku_palace_assets.json'
    write(out, m)
    print(f'wrote {out}: {len(items)} hidden asset creates, 1 full capture, pack @ {ref[:7]}')


def bundle_ids(path):
    d = json.load(open(path))
    if (d.get('journal') or {}).get('manifestNumber') != N_CREATE:
        raise SystemExit(f'{path} is not the push/{N_CREATE} results bundle')
    idmap = d.get('idmap') or {}
    ids = {src: idmap.get(src) for src, *_ in ASSETS}
    missing = [s for s, v in ids.items() if not v]
    if missing:
        raise SystemExit(f'not in the bundle idmap (run push/{N_CREATE} first): {missing}')
    return d, ids


def build_unhide(path):
    _, ids = bundle_ids(path)
    create = json.load(open(f'push/{N_CREATE}_subaku_palace_assets.json'))
    items = []
    for it in create['items']:
        data = dict(it['data'], hidden=False)
        data.pop('image')                          # the image is not re-sent (Forge merges the live record)
        items.append({"entity": "asset", "slot": "edit", "targetId": ids[it['srcId']], "name": it['name'],
                      "data": data})
    out = f'push/{N_UNHIDE}_subaku_palace_unhide.json'
    write(out, {"_note": (f"push/{N_UNHIDE}: unhides the {len(items)} Subaku Palace art assets created by "
                          f"push/{N_CREATE} (law 16c: battles load only unhidden assets). Run before push/{N_JUTSU}. "
                          "Generated by push/subaku_palace.gen.py; do not hand-edit."), "items": items})
    print(f'wrote {out}: unhide ' + ', '.join(i['targetId'] for i in items))


def live_record(d):
    for c in d.get('captures') or []:
        if c.get('proc') == 'jutsu.get' and (c.get('input') or {}).get('id') == JID:
            if not c.get('ok'):
                raise SystemExit(f'the jutsu capture failed: {c.get("error")}')
            data = c.get('data')
            for cand in (data, (data or {}).get('data') if isinstance(data, dict) else None):
                if isinstance(cand, dict) and cand.get('id') == JID:
                    return cand
    raise SystemExit(f'{JID} not captured in the bundle')


def check(fx, want, label):
    bad = {k: (fx.get(k), v) for k, v in want.items() if fx.get(k) != v}
    if bad:
        raise SystemExit(f'{label} does not match the design ({bad}); re-read the record before editing')


def jutsu_effects(live, ids):
    effects = [dict(e) for e in live['effects']]
    if any(e.get('type') == 'visual' for e in effects):
        raise SystemExit('the live record already carries visual tags; inspect it before adding the ring bands')
    selfs = [e for e in effects if e.get('type') == SELF_FX['type']]
    grounds = [e for e in effects if e.get('type') == GROUND_FX['type']]
    if len(selfs) != 1 or len(grounds) != 1:
        raise SystemExit(f'expected one {SELF_FX["type"]} and one {GROUND_FX["type"]} effect, got '
                         f'{[e.get("type") for e in effects]}')
    check(selfs[0], SELF_FX, 'the SELF effect')
    check(grounds[0], GROUND_FX, 'the ground effect')
    if grounds[0].get('appearSfx') not in ('', HEAL):
        print(f'note: the ground effect carries appearSfx {grounds[0].get("appearSfx")!r}, not Heal; cleared anyway')
    selfs[0].update(appearAnimation=ids['sbk_gates'], appearSfx=EARTH, staticAssetPath='', staticAnimation='')
    grounds[0].update(staticAssetPath=ids['sbk_floor'], appearAnimation=ids['sbk_seal'], appearSfx='')
    for k, g in enumerate(META['groups']):
        effects.append({"staticAssetPath": "", "staticAnimation": "", "appearAnimation": ids[f'sbk_wave_b{k}'],
                        "disappearAnimation": "", "appearSfx": "", "disappearSfx": "", "rounds": 1, "power": 2,
                        "powerPerLevel": 0, "direction": "offence", "target": "COORDINATES",
                        "calculation": "static", "type": "visual",
                        "coordinateTargeting": {"origin": "CASTER", "selection": "ALL",
                                                "coordinates": g['offsets']},
                        "description": f"Subaku Palace: ring {BAND_LABELS[k]} wave (art only)"})
    return effects


def build_jutsu(path):
    d, ids = bundle_ids(path)
    live = live_record(d)
    assert live.get('name') == 'Subaku Palace', live.get('name')
    effects = jutsu_effects(live, ids)
    title = "Subaku Palace: the domain summoning"
    rationale = ("The demon palace's domain is summoned ring by ring: the director's floor tile, joined so its gold "
                 "runs unbroken from hex to hex, lights up outward from the caster as a burning current, the whole "
                 "domain flares as the palace stands, and red sandstone oni gates rise round the caster. One Earth "
                 "sound per cast replaces the Heal sound that played about 120 times. Mechanics unchanged.")
    out = f'push/{N_JUTSU}_subaku_palace_jutsu.json'
    write(out, {
        "_note": (f"push/{N_JUTSU}: Subaku Palace ({JID}), one suggest-mode edit built from the push/{N_CREATE} "
                  "capture. Ground decreasedamagegiven: the domain floor tile and the seal, Heal sound off. SELF "
                  "increasedamagegiven: the gates rise and one Earth sound; its static slots cleared. 7 visual "
                  "ring-band tags (COORDINATES, origin CASTER). Every other field as captured; mechanics checked "
                  f"unchanged; injectableInBattle re-sent at its live value (law 20). Run push/{N_UNHIDE} first. "
                  "Generated by push/subaku_palace.gen.py; do not hand-edit. Operator runs it from Forge; never "
                  "skipPreflight."),
        "mode": "suggest",
        "suggestion": {"category": "CONSISTENCY", "title": title, "rationale": rationale},
        "items": [{"entity": "jutsu", "slot": "edit", "name": "Subaku Palace", "targetId": JID,
                   "data": {"effects": effects, "injectableInBattle": live.get('injectableInBattle', False)},
                   "suggestion": {"category": "CONSISTENCY", "title": title, "rationale": rationale}}]})
    print(f'wrote {out}: 1 suggestion, {len(effects)} effects ({len(effects) - len(live["effects"])} ring tags added)')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        build_create()
    elif len(a) == 2 and a[0] == 'unhide':
        build_unhide(a[1])
    elif len(a) == 2 and a[0] == 'jutsu':
        build_jutsu(a[1])
    else:
        raise SystemExit(__doc__)
