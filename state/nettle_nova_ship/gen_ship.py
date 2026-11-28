#!/usr/bin/env python3
"""push/698 Nettle Nova: build assets.json (11 gameAssets) from the strips' json and uploaded.json."""
import json, os
R = '/home/user/tnr-tools/state/nettle_nova_upload'
D = os.path.dirname(os.path.abspath(__file__))
up = json.load(open(f'{R}/uploaded.json'))['files']
NAMES = {
 'anim_rin_nn_c_swell_mark_appear_c': 'Nettle Swell mark appear',
 'anim_rin_nn_c_swell_mark_loop_c': 'Nettle Swell mark loop',
 'anim_rin_nn_c_swell_boss_c': 'Nettle Swell boss swell',
 'anim_rin_nn_c_sealed_aura_c': 'Nettle Nova sealed aura',
 'ground_rin_nn_c_swell_mark_ground_c': 'Nettle Swell mark ground',
}
out = []
for sid in sorted(up):
    j = json.load(open(f'{R}/strips/{sid}.json'))
    ground = sid.startswith('ground_')
    name = NAMES.get(sid) or 'Nettle Nova burst ' + sid.split('nova_burst_')[1].rsplit('_c', 1)[0]
    out.append({'srcId': sid, 'name': name, 'url': up[sid]['url'], 'sha256': up[sid]['sha256'],
                'type': 'STATIC' if ground else 'ANIMATION',
                'frames': 1 if ground else j['frames'], 'speed': 100 if ground else j['speed']})
json.dump(out, open(f'{D}/assets.json', 'w'), indent=1)
for a in out: print(a['type'], a['frames'], a['speed'], a['name'])
