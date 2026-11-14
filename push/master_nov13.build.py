#!/usr/bin/env python3
"""build_master.py: merge tonight's release manifests into MASTER_A (hidden prep + text + icons + safe flips)
and MASTER_B_flips (open-time unhides). Items are grouped by type (asset, jutsu, ai, item, quest) so each
endpoint runs as one block under its own per-path limit. Several items on one record merge into one item:
data overlaid in source order (a later full 'content' replaces an earlier one). Dungeons are excluded
(Forge can't edit them tonight; they go by direct coop.dungeon.save)."""
import json, copy
R = '/mnt/project-files/tnr/release_nov13/'
ORDER = ['asset', 'jutsu', 'ai', 'item', 'quest']
PHASE = {'asset': 1, 'jutsu': 5, 'ai': 20, 'item': 25, 'quest': 30}
SALV = 'https://bbenpyo9uu.ufs.sh/f/0tzd8oDeiVIztTw3VgzGhyvTwHIbs5xCj3PVfDMUm2z4pn6u'   # Wreck Salvage icon
DEFAULT = 'https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp'
ICONS = {  # quests with the blank default icon -> hosted art matched to the quest (interim until Brandon's icons)
 '26MTz1wdUuKbfm1nPQNGU': ('The Salvager\'s Trade: The Lantern', 'https://ui0arpl8sm.ufs.sh/f/e4eNC9JdUPrchiJKcMGUX.webp'),
 'oMBY3r0XiSZ_2HaJN0L39': ('The Salvager\'s Trade: A Sealed Chart', 'https://ui0arpl8sm.ufs.sh/f/GnbyPivtXnCa3YLP97KfO.webp'),
 'OCrpmCXlh1v9CnQPzDRpj': ('The Salvager\'s Trade: Hold Charts', 'https://bbenpyo9uu.ufs.sh/f/0tzd8oDeiVIzxSrkvFDZouNGF4UVirBmDjJE9Av510SeWbdK'),
 'zYhkIQeVGNUMljwev3-ud': ('The Salvager\'s Trade: Deck Charts', 'https://ui0arpl8sm.ufs.sh/f/q7byk0MolOXjyV6NFCY5w.webp'),
 'lEg5pVXqA8lzJpIPrykNi': ('At the Salvager\'s Fire', SALV),
 'ktVUByCZUfREmWYsvPtzQ': ('The Split Hold', 'https://ui0arpl8sm.ufs.sh/f/iS35oVeCsybzoJYcfJ2xp.webp'),
 'BDUY4nScGzYiZoHGkmkxP': ('The Broken Stern', 'https://ui0arpl8sm.ufs.sh/f/xigFDKI7-1Qr1qgdrrpcI.webp'),
 'IBPNwhAzlAJPXoeEnp8gW': ('The Mother of Echoes', 'https://ui0arpl8sm.ufs.sh/f/HYiGu0fn2knteovR2CWiQ.webp'),
}
NEVER_UNHIDE = {'TdYCx3GME2s6L33GjnWHx','7pk21EmBrmL_EyHuPK2Xp','jUQYz9zyMdJIRdLbucYjm','MSQJTdZEQK1JWjFiVtQVI','yZUKtA7Tsmax9LshlRV_v','lBmX8J_msc3irxMGYbGeI'}

def load(p): return json.load(open(R + p))['items']

def merge(sources, label):
    acc, order = {}, []
    for items in sources:
        for i in items:
            assert i['slot'] == 'edit', i['name']
            if i['entity'] == 'dungeon': continue
            k = (i['entity'], i['targetId'])
            if k not in acc:
                acc[k] = {'entity': i['entity'], 'slot': 'edit', 'targetId': i['targetId'], 'phase': PHASE[i['entity']], 'name': i['name'], 'data': {}}
                order.append(k)
            else:
                acc[k]['name'] += ' + ' + i['name']
            for f, v in i['data'].items():
                acc[k]['data'][f] = copy.deepcopy(v)
    out = sorted((acc[k] for k in order), key=lambda x: ORDER.index(x['entity']))
    for x in out:
        if x['data'].get('hidden') is False: assert x['targetId'] not in NEVER_UNHIDE, x
        if len(x['name']) > 300: x['name'] = x['name'][:297] + '...'
    return {'_note': label, 'items': out}

dailies = load('dailies/dailies_overworld_manifest.json')
for i in dailies:
    if i['data'].get('image') == DEFAULT: i['data']['image'] = SALV
icons = [{'entity': 'quest', 'slot': 'edit', 'targetId': t, 'name': f'{n}: icon (was the blank default)', 'data': {'image': u}} for t, (n, u) in ICONS.items()]
oc1b = load('qa_fixes/OC1b_opening_critical.json')
ws2 = load('qa_fixes/WS2_wreck_sighted_splitstern_levels.json')
A = merge([
    load('sitting/ASSETS_golive_unhide.json'),
    [i for i in load('charts_mender/v2_closing/599_hullbound_mender_golive.json') if i['entity'] == 'asset'],
    load('driftline/DL1_driftline_hidden.json'),
    [i for i in load('charts_mender/v2_closing/538_skyglass_new_charts_golive.noKuq.json') if i['entity'] != 'quest'],
    [i for i in load('charts_mender/v2_closing/599_hullbound_mender_golive.json') if i['entity'] == 'item'],
    load('chart_text/CT1_chart_text.json'),
    oc1b, ws2, dailies, load('fire/fire_v6_manifest.json'),
    [i for i in load('charts_mender/v2_closing/538_skyglass_new_charts_golive.noKuq.json') if i['entity'] == 'quest'],
    [i for i in load('charts_mender/v2_closing/599_hullbound_mender_golive.json') if i['entity'] == 'quest'],
    load('chart_text/PY1_pyramid_text.json'), load('chart_text/CR1_chart_run_levels.json'),
    icons,
], 'MASTER_A (Nov 13 release): 31 boards/poses + 9 Mender assets unhidden; Driftline prep (hidden); new charts + Cradle chart unhidden, '
   'all 23 chart texts; Cradle Lantern 10%, Rotted Heading 81+ gate, both Wreck Sighted texts (still hidden), 30-80 page (hidden), '
   '4 dailies (hidden), the Fire v6 (hidden), new chart runs + Cradle run unhidden, 23 run texts + levels (30+/81+, no max), 8 quest icons. '
   'Grouped by type. Built by master/build_master.py; run BEFORE 545 (545 reads fresh after this lands).')
fl = lambda t, n, h: {'entity': 'quest', 'slot': 'edit', 'targetId': t, 'name': n, 'data': {'hidden': h}}
a3 = load('watchlog_kickoff/A3_page_30_80_publish.json')
for i in a3:
    if i['targetId'] == 'CLONE_ID_30_80': i['targetId'] = '73ivWjFFk0dwSEG7bNhMj'
B = merge([
    load('dailies/dailies_golive_quests.json'), a3,
    [fl('IZgCt17ReC_0vtUG-GNRl', 'Wreck Sighted (Levels 30 to 80): unhide', False),
     fl('-UjsbiBbaSyPtZ4zAH10A', 'Wreck Sighted (Level 81 and up): unhide', False),
     fl('_zp1l7Y9a_77pgonAdsYx', 'Wreck Sighted (original): hide', True),
     fl('lEg5pVXqA8lzJpIPrykNi', "At the Salvager's Fire: publish", False)],
], 'MASTER_B_flips (Nov 13 release, open time): unhide 4 dailies, the 30-80 page, both Wreck Sighted copies, the Fire; hide the original Wreck Sighted. '
   'Run right after 545, then the placement goes active and 603 opens the Wrecks.')
FIXES = [('The Fall, The Closing Hold and both', 'The Fall, The Drowned Cradle and both'),
         ('Two new ones drop in the Faded Wreck, for levels 30 to 80: <b>Split Hold</b> and <b>Broken Stern</b>.',
          'Two new ones drop in the Faded Wreck: <b>Split Hold</b> and <b>Broken Stern</b>, both open from level 30.')]
A = json.loads(_s := json.dumps(A, ensure_ascii=False)) if False else A
_s = json.dumps(A, ensure_ascii=False)
for a, b in FIXES: print('fix', a[:30], _s.count(a)); _s = _s.replace(a, b)
A = json.loads(_s)
for name, m in (('MASTER_A.json', A), ('MASTER_B_flips.json', B)):
    json.dump(m, open(R + 'master/' + name, 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(name, len(m['items']), dict(Counter(i['entity'] for i in m['items'])))
