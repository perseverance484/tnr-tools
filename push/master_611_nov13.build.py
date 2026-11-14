#!/usr/bin/env python3
"""build_611.py <readsdir>: 538 Wreck rows overlaid on the fresh dungeon reads -> salvager_golive.gen.py (545) ->
split: non-dungeon items + 610 flips = push/611_salvage_and_flips_nov13.json (grouped by type, merged per record);
dungeon items -> direct saves (fresh content + 545 rewards [built on 538's] + 603 expiresAt) = the open."""
import json, sys, os, shutil, subprocess, copy
sys.path.insert(0, '/mnt/project-files/tnr/release_nov13/master')
R = '/mnt/project-files/tnr/release_nov13/'; TT = '/home/claude/tnr-tools/'
src = sys.argv[1]; gen = src.rstrip('/') + '_gen'
shutil.rmtree(gen, ignore_errors=True); shutil.copytree(src, gen)
m538 = json.load(open(R + 'charts_mender/v2_closing/538_skyglass_new_charts_golive.json'))
for i in m538['items']:
    if i['entity'] != 'dungeon': continue
    p = f"{gen}/dungeon_{i['targetId']}.json"; d = json.load(open(p))
    for k, v in i['data'].items(): assert k in d; d[k] = v
    json.dump(d, open(p, 'w'), ensure_ascii=False); print('538 rows on', d['name'])
subprocess.run(['python3', TT + 'push/salvager_golive.gen.py', '--live', gen], check=True)
m545 = json.load(open(TT + 'push/545_salvager_trade_golive.json'))
RESET = {'ktVUByCZUfREmWYsvPtzQ', 'BDUY4nScGzYiZoHGkmkxP'}
for i in m545['items']:
    if i['entity'] == 'quest' and i['targetId'] in RESET and 'description' in i['data']:
        del i['data']['description']; i['name'] += ' (description left to 609)'
from build_master import merge  # noqa
B = json.load(open(R + 'master/MASTER_B_flips.json'))
DL2 = json.load(open(R + 'driftline/DL2_driftline_golive.json'))['items']
out = merge([[i for i in m545['items'] if i['entity'] != 'dungeon'], DL2, B['items']],
            '611 (Nov 13 release, open time): 545 salvage ladder (every Skyglass win and Rotted Heading order pays salvage, '
            'chain fix, Archive Chart Case, Haul pages Epic, Wreck Salvage + the four trades unhidden) and the 610 flips '
            '+ DL2 (Split Hold and Broken Stern charts and runs live, 30+, no max) (4 dailies, 30-80 page, both Wreck Sighted copies, the Fire unhidden; original Wreck Sighted hidden). Run after 609. '
            'Wreck drop rows and the open are direct dungeon saves by the release thread. Built by master/build_611.py.')
json.dump(out, open(TT + 'push/611_salvage_and_flips_nov13.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print('611', len(out['items']), dict(Counter(i['entity'] for i in out['items'])))
ga = {}
for f in os.listdir(src):
    if f.startswith('dungeon_') and f != 'dungeon_getall.json':
        d = json.load(open(f'{src}/{f}')); ga[d['id']] = {k: v for k, v in d.items() if k != 'id'}
exp = {i['targetId']: i['data']['expiresAt'] for i in json.load(open(TT + 'push/603_skyglass_wreck_window.json'))['items']}
for i in m545['items']:
    if i['entity'] != 'dungeon': continue
    c = copy.deepcopy(ga[i['targetId']])
    for k, v in i['data'].items(): assert k in c; c[k] = v
    c['expiresAt'] = exp[i['targetId']]
    if i['targetId'] == 'j4QEUtjbK_lbOYUPVoidk':  # 604: Split Hold 15%, Broken Stern 5%, four older charts trimmed
        tmp = gen + '/faded_for_604.json'; json.dump({'id': i['targetId'], **c}, open(tmp, 'w'), ensure_ascii=False)
        subprocess.run(['python3', TT + 'push/driftline_drops.gen.py', tmp], check=True)
        c['rewards'] = json.load(open(TT + 'push/604_driftline_drops.json'))['items'][0]['data']['rewards']
    p = R + f"master/OPEN_dsave_{i['targetId']}.json"
    json.dump({'id': i['targetId'], 'content': c}, open(p, 'w'), ensure_ascii=False)
    print('open save', c['name'], 'exp', c['expiresAt'], 'hidden', c.get('hidden'), 'maxPlayers', c['maxPlayers'],
          'req', c['requirements'].get('prerequisiteQuestId'), c['requirements'].get('requiredLevel'), 'drops', len(c['rewards']['drops']), p)
