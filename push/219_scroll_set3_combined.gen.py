#!/usr/bin/env python3
"""Build push/219: the combined set-3 + scroll-jutsu ticket (suggest mode).

    python3 push/219_scroll_set3_combined.gen.py capture   # (re)write push/218 (read-only capture of the 25 records)
    python3 push/219_scroll_set3_combined.gen.py build BUNDLE   # write push/219 from the push/218 results bundle

Sources: docs/handoffs/SCROLL_ICONS_SET3_ART_REQUEST.md, docs/handoffs/SCROLL_JUTSU_ICONS_ART_REQUEST.md,
docs/design/jutsu_overhaul/EVENT_JUTSU_STORY_TEXT.md (approved texts). One suggestion per record; jutsu suggestions carry
icon + description + battleDescription (+ name for Abyss of Shadows) and re-send injectableInBattle at its live value
(law 20). Subaku Palace also swaps its field asset (Shadow Field 2 -> zEvI0yd_As_FzNyrr5Iq4) in a copy of its live effects array. The image pack is pinned at the current HEAD, so commit the exports first. Refuses to build while any icon or
capture record is missing, and lists what is missing.
"""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
EV, VB, JU = 'art/item_icons/event_scrolls/exports/', 'art/village_bloodline_scrolls/exports/', 'art/jutsu_icons/scroll_jutsu/exports/'

ITEMS = [  # name, id, export, rationale
    ("Scroll of Cleave", "K5j9Hq19eRftSFDyIX6TN", EV + "icon_scroll_of_cleave_b.webp", "New icon: a steel scroll in a storm of silver blades with orange edges, matching Tempest Cleave."),
    ("Scroll of Bastion", "-qVND9J0r_tkDi7ZdRaCC", EV + "icon_scroll_of_bastion_v1.webp", "New icon: a scroll ringed by cracked stone and molten earth, matching Earthen Bastion."),
    ("Scroll of Renewal", "ZRrluzsDengJNuRYM_lQ6", EV + "icon_scroll_of_renewal_v1.webp", "New icon: a scroll in a swirl of water drops and leaves, matching Drops of Renewal."),
    ("Scroll of Blazing", "VPLmBobycTYFLhB4qX23A", EV + "icon_scroll_of_blazing_b.webp", "New icon: a scroll wrapped in flame with a fire dragon on the paper, matching Blazing Fang Strike."),
    ("Scroll of Celestial Dew", "FO7a7BlDpjx1Rxoy3X5bR", EV + "icon_scroll_of_celestial_dew_v1.webp", "New icon: a silver scroll with a star emblem in a swirl of dew, matching Celestial Dew."),
    ("Scroll of Hollow Veil", "4huDnXDq5zInzZ3dLgykM", EV + "icon_scroll_of_hollow_veil_b.webp", "New icon: a bone-white scroll in ash-gray mist, matching Hollow Veil."),
    ("Scroll of Shadows", "uLLAWOSCFeDz9Mc3d0rKw", EV + "icon_scroll_of_shadows_b.webp", "New icon: a black scroll in crimson shadow. The description names the jutsu's new name, Abyss of Shadows."),
    ("Shadow Scroll: Oblivion Seal", "7tZoY3uG2Jxg8Fp0dZlwE", VB + "icon_bloodline_scroll_oblivion_seal_b.webp", "Recoloured icon in the Oblivion Seal bloodline's own blue-violet, so it no longer matches the KGK scrolls."),
    ("Scroll of Metal", "Kzx7F3FsKMqfWNNVhpMbG", VB + "icon_bloodline_scroll_tetsugan_v1.webp", "New icon on the bloodline scroll shape: riveted dark iron, for the Tetsugan bloodline."),
    ("Scroll of Time", "_M2UwSUpP_szhbuicUoSC", VB + "icon_bloodline_scroll_sands_of_time_v1.webp", "New icon on the bloodline scroll shape: sand and bronze with an hourglass, for Sands of Time."),
    ("Dragon's Scroll", "mDBpVrKfygS5V5EZgvcn1", EV + "icon_dragons_scroll_v1.webp", "Own icon (it was reusing a KGK scroll image): a jade scroll with a gold dragon holding the colored jewel it grants."),
    ("Colored Jewel of the Dragon's Neck", "_8HEbybzN5QPX8vUG24Tk", EV + "icon_colored_jewel_of_the_dragons_neck_v1.webp", "New icon: the rainbow jewel, matching Dragon's Scroll, which grants it."),
    ("Forbidden Jutsu Scroll: Nexus", "XZfVErGEkHpPiPtPa7_VC", EV + "icon_forbidden_scroll_nexus_v1.webp", "New icon: a chained forbidden scroll with magenta seals, for Ethereal Nexus."),
    ("Forbidden Jutsu Scroll: Rebirth", "X5q3Ww-yfCeJ3m6ZqPmmz", EV + "icon_forbidden_scroll_rebirth_v1.webp", "New icon: a chained forbidden scroll with emerald seals, for Ethereal Rebirth."),
    ("Demon Scroll: Subaku Palace", "rFtea8kQnNDWfR8xw1GDw", EV + "icon_demon_scroll_subaku_palace_v1.webp", "New icon: red sandstone with demon-gold fittings and a demon-mask clasp, for Subaku Palace."),
]
SHADOWS_DESC = "Learn the jutsu Abyss of Shadows upon use."

JUTSU = [  # name, id, export, rationale
    ("Abyss of Shadows", "XS08zZhUhK615Dle4j3f3", JU + "icon_jutsu_abyss_of_shadows_b.webp", "Renamed from Aegis of Shadows: it curses the enemy rather than shielding the user. New black-sun icon, description and battle text to match."),
    ("Tempest Cleave", "Ul83iTziN__Z0i_UOzZTK", JU + "icon_jutsu_tempest_cleave_v1.webp", "New icon and premium description and battle text for this event jutsu."),
    ("Earthen Bastion", "_zNMEZqIzgjTqXoXQRWz0", JU + "icon_jutsu_earthen_bastion_v1.webp", "New icon and premium texts. The old battle text said it protects allies; it protects only the user. War Commander equips it and needs re-equipping after approval."),
    ("Drops of Renewal", "-7jaNkJCvt3ByWhPJSw3E", JU + "icon_jutsu_drops_of_renewal_v1.webp", "New icon and premium description and battle text for this event jutsu."),
    ("Blazing Fang Strike", "l3oXmqSJ7L-r4XI9IBIyh", JU + "icon_jutsu_blazing_fang_strike_v1.webp", "New fire-dragon icon and premium description and battle text for this event jutsu."),
    ("Celestial Dew", "2vNeMhph6A9Ld--WXa35O", JU + "icon_jutsu_celestial_dew_v1.webp", "New icon and premium texts. The old battle text said it heals allies; it affects only the user."),
    ("Hollow Veil", "GAhckNCW8xUES4YGTJPGL", JU + "icon_jutsu_hollow_veil_v1.webp", "New icon and premium description and battle text for this event jutsu."),
    ("Subaku Palace", "jELEiw5W3N4m2R3oJm3Pk", JU + "icon_jutsu_subaku_palace_v1.webp", "New icon and premium texts, and the palace's ground effect now shows the new demon-palace field instead of Shadow Field 2."),
    ("Ethereal Nexus", "iktsCP-RjIhlYlsTg-JTN", JU + "icon_jutsu_ethereal_nexus_v1.webp", "New icon and premium texts for this forbidden jutsu, including its cost to the user."),
    ("Ethereal Rebirth", "K0t6Z-Q4lau1jFt8Tkpot", JU + "icon_jutsu_ethereal_rebirth_v1.webp", "New icon and premium texts for this forbidden jutsu, including its cost to the user."),
]
SUBAKU = 'jELEiw5W3N4m2R3oJm3Pk'
OLD_FIELD, NEW_FIELD = 'dKEJjYMI4asyfvH9hsQUZ', 'zEvI0yd_As_FzNyrr5Iq4'  # Shadow Field 2 -> director's new field asset (2026-10-23)
WARN = '<br><br><span style="color:#D22B2B">DON\'T TRAIN. ALREADY CAPPED. IT HAS NO POWER PER LEVEL</span>'


def texts():
    s = open('docs/design/jutsu_overhaul/EVENT_JUTSU_STORY_TEXT.md').read()
    out = {}
    for block in s.split('\n## ')[1:]:
        m = re.search(r'\(`([^`]+)`\)', block.split('\n')[0])
        d = re.search(r'\*\*Description:\*\* (.+)', block)
        b = re.search(r'\*\*Battle line:\*\* (.+)', block)
        if m and d and b:
            desc = d.group(1).strip()
            warn = '(+ training warning)' in desc
            desc = desc.replace('*(+ training warning)*', '').strip()
            out[m.group(1)] = (desc + (WARN if warn else ''), b.group(1).strip())
    return out


def capture():
    m = {"_note": "READ-ONLY capture of the 25 records in the combined set-3 + scroll-jutsu ticket (push/219): two game assets (Shadow Field 2 and the new Subaku Palace field) and 15 items (the seven event scrolls, Oblivion Seal, Metal, Time, Dragon's Scroll, Colored Jewel, the forbidden pair, the Demon Scroll) and 10 jutsu (the seven event jutsu, Subaku Palace, Ethereal Nexus, Ethereal Rebirth). Fresh live state for the build (battleDescription, injectableInBattle). Zero items, zero writes. Generated by push/219_scroll_set3_combined.gen.py; run it just before the build.",
         "capture": {"before": [{"proc": "item.get", "input": {"id": i}, "persist": "full"} for _, i, _, _ in ITEMS] +
                               [{"proc": "jutsu.get", "input": {"id": i}, "persist": "full"} for _, i, _, _ in JUTSU] +
                               [{"proc": "gameAsset.get", "input": {"id": a}, "persist": "full"} for a in (OLD_FIELD, NEW_FIELD)], "after": []},
         "items": []}
    json.dump(m, open('push/218_scroll_set3_combined_capture.json', 'w'), indent=1, ensure_ascii=False)
    open('push/218_scroll_set3_combined_capture.json', 'a').write('\n')
    print('wrote push/218_scroll_set3_combined_capture.json (%d reads)' % len(m['capture']['before']))


def build(bundle):
    live = {c['data']['id']: c['data'] for c in json.load(open(bundle))['captures'] if c.get('ok') and isinstance(c.get('data'), dict)}
    T = texts()
    missing = [p for _, _, p, _ in ITEMS + JUTSU if not os.path.exists(p)]
    missing += ['capture: %s %s' % (n, i) for n, i, _, _ in ITEMS + JUTSU if i not in live]
    missing += ['text: %s' % n for n, i, _, _ in JUTSU if i not in T]
    missing += ['empty battleDescription (save would fail): %s' % n for n, i, _, _ in ITEMS if i in live and not (live[i].get('battleDescription') or '').strip()]
    na, oa = live.get(NEW_FIELD), live.get(OLD_FIELD)
    if not na: missing.append('capture: new field asset %s' % NEW_FIELD)
    elif oa and na.get('type') != oa.get('type'): missing.append('new field asset type %s differs from Shadow Field 2 (%s)' % (na.get('type'), oa.get('type')))
    if SUBAKU in live:
        hits = [e for e in live[SUBAKU]['effects'] if e.get('staticAssetPath') == OLD_FIELD]
        if len(hits) != 1: missing.append('Subaku Palace: expected exactly one effect on Shadow Field 2, found %d' % len(hits))
    if missing:
        print('NOT BUILT, missing:\n  ' + '\n  '.join(missing)); return 1
    ref = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    for _, _, p, _ in ITEMS + JUTSU:
        subprocess.run(['git', 'cat-file', '-e', f'{ref}:{p}'], check=True)
    files, sizes, items, dropped = {}, {}, [], []
    def pack(p):
        fn = os.path.basename(p); b = open(p, 'rb').read()
        files[fn] = {'path': p, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}; sizes[fn] = len(b)
        return '@img:' + fn
    for n, i, p, why in JUTSU:
        desc, battle = T[i]
        d = {'image': pack(p), 'description': desc, 'battleDescription': battle, 'injectableInBattle': live[i]['injectableInBattle']}
        if i == 'XS08zZhUhK615Dle4j3f3': d['name'] = 'Abyss of Shadows'
        if i == SUBAKU:  # whole array from live, only the field asset swapped (arrays are replaced, not merged)
            d['effects'] = [dict(e, staticAssetPath=NEW_FIELD) if e.get('staticAssetPath') == OLD_FIELD else dict(e) for e in live[i]['effects']]
            nested = json.load(open('forge/src/runner/nested.json'))  # pinned key sets; the server drops other keys on any save (push/170 precedent)
            for e in d['effects']:
                ok = set(nested['sets'][nested['effects'][e['type']]])
                for k in [k for k in e if k not in ok]:
                    dropped.append('%s.%s' % (e['type'], k)); del e[k]
        items.append({'entity': 'jutsu', 'slot': 'edit', 'name': n, 'targetId': i, 'data': d,
                      'suggestion': {'category': 'CONSISTENCY', 'title': 'New icon and text', 'rationale': why}})
    for n, i, p, why in ITEMS:
        d = {'image': pack(p)}
        if i == 'uLLAWOSCFeDz9Mc3d0rKw': d['description'] = SHADOWS_DESC
        items.append({'entity': 'item', 'slot': 'edit', 'name': n, 'targetId': i, 'data': d,
                      'suggestion': {'category': 'CONSISTENCY' if 'description' in d else 'VISUAL', 'title': 'New scroll icon', 'rationale': why}})
    m = {"_note": "Combined ticket (director, 2026-10-22/23): scroll icons set 3 (docs/handoffs/SCROLL_ICONS_SET3_ART_REQUEST.md) and the scroll-jutsu icons with their approved premium texts (docs/handoffs/SCROLL_JUTSU_ICONS_ART_REQUEST.md, docs/design/jutsu_overhaul/EVENT_JUTSU_STORY_TEXT.md). Suggest mode: one suggestion per record; nothing changes until a reviewer approves. Aegis of Shadows is renamed Abyss of Shadows (RUL-2026-10-23-001). Subaku Palace re-sends its live effects array with only the field asset changed (staticAssetPath Shadow Field 2 dKEJjYMI4asyfvH9hsQUZ -> zEvI0yd_As_FzNyrr5Iq4, director 2026-10-23). Every jutsu re-sends injectableInBattle at its live value (law 20). Earthen Bastion is equipped by War Commander: approving its suggestion severs the link and the director re-equips War Commander afterwards (director, 2026-10-22). Obsolete effect keys the server drops on any save are left out: %s. Live state from push/218 (%s). Generated by push/219_scroll_set3_combined.gen.py; do not hand-edit. Operator runs it from Forge; never skipPreflight." % (', '.join(dropped) or 'none', os.path.basename(bundle)),
         "mode": "suggest", "suggestion": {"category": "VISUAL", "title": "New scroll icon", "rationale": "New icon from the refreshed scroll icon set."},
         "imgSizes": sizes, "imagePack": {"ref": ref, "files": files}, "items": items}
    json.dump(m, open('push/219_scroll_set3_combined.json', 'w'), indent=1, ensure_ascii=False)
    open('push/219_scroll_set3_combined.json', 'a').write('\n')
    print('wrote push/219_scroll_set3_combined.json: %d suggestions (%d items, %d jutsu), pack @ %s' % (len(items), len(ITEMS), len(JUTSU), ref[:7]))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['capture']: capture()
    elif a[:1] == ['build'] and len(a) == 2: sys.exit(build(a[1]))
    else: print(__doc__); sys.exit(2)
