#!/usr/bin/env python3
"""push/698: the 3 live jutsu records (data blocks for jutsu.update), from the sim design plus live asset ids."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(f'{D}/ledger.json'))
P = 'anim_rin_nn_c_'
design = {j['name']: j for j in json.load(open('/mnt/project-files/tnr/resort_in_need/sim/rin_nova_p1.json'))['designs'][0]['ai']['msKodzIJSH2J_BO-1FCIN']['jutsus']}
DROP = ('id', 'createdAt', 'updatedAt')
BASE_TAG = {'appearSfx': '', 'disappearSfx': '', 'disappearAnimation': '', 'powerPerLevel': 0}
def rec(name):
    r = {k: v for k, v in design[name].items() if k not in DROP}
    r['hidden'] = True; r['jutsuType'] = 'AI'
    return r
swell = rec('Nettle Swell')
mark, primed = swell['effects']
mark.update(appearAnimation=L[P+'swell_mark_appear_c'], staticAnimation=L[P+'swell_mark_loop_c'],
            staticAssetPath=L['ground_rin_nn_c_swell_mark_ground_c'], animationScale=2)
primed.update(appearAnimation=L[P+'swell_boss_c'], animationScale=3)
nova = rec('Nettle Nova')
nova['battleDescription'] = nova['description'] = '%user bursts! Stinging chakra floods the marked water, then its own chakra seals shut.'
dmg, _residue, seal = nova['effects']
dmg['appearAnimation'] = ''
seal.update(staticAnimation=L[P+'sealed_aura_c'], animationScale=3, description='Sealed: its chakra is spent')
burst = []
for lon in (-2, 0, 2):
    for lat in (2, -1):
        key = f"{P}nova_burst_c{'m' if lon < 0 else 'p'}{abs(lon)}_r{'m' if lat < 0 else 'p'}{abs(lat)}_c"
        burst.append({**BASE_TAG, 'type': 'visual', 'power': 2, 'rounds': 1, 'target': 'COORDINATES', 'direction': 'offence',
                      'calculation': 'static', 'description': 'Nettle Nova: burst slice', 'animationScale': 3,
                      'appearAnimation': L[key], 'staticAnimation': '', 'staticAssetPath': '',
                      'coordinateTargeting': {'origin': 'CASTER', 'selection': 'ALL',
                                              'coordinates': [{'longitude': lon, 'latitude': lat}], 'randomCount': 1}})
nova['effects'] = [dmg, seal] + burst
lash = rec('Stinging Lash')
out = {'Nettle Swell': swell, 'Nettle Nova': nova, 'Stinging Lash': lash}
json.dump(out, open(f'{D}/jutsu_records.json', 'w'), indent=1)
for n, r in out.items():
    print(n, r['method'], r['range'], r['actionCostPerc'], r['cooldown'], [(e['type'], e.get('target'), e.get('power'), e.get('rounds'), e.get('appearAnimation'), e.get('staticAnimation'), e.get('staticAssetPath')) for e in r['effects']])
