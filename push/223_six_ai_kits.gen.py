#!/usr/bin/env python3
"""Build push/223: kits, rank, preferred stat and basic rules for six new bandit-camp AIs.

    python3 push/223_six_ai_kits.gen.py

Director, 2026-10-23: kits from the shared AI pool as drafted; JONIN for L70-L100, ELITE JONIN for
L110-L120 (STUDENT caps every stat at 20k in battle, combat.ts:3058 capUserStats at 107d7a8);
Second Wind fires only before round 5 and below 50% HP (with its 6-round
cooldown that is once per fight). The approved "Bukijutsu" preference has no field any more
(preferredStat was removed in the stat rework; the nearest lever is bukijutsuMastery, an absolute
number), so it is held for a director decision and not sent. Inputs (committed): push/222 bundle (live AI before-image) and the
public AI-jutsu read (live range/method/target of every pool jutsu). Do not hand-edit the output.

Rules per AI (laws 39-41, 41b, 62-64): Second Wind (conditional) -> stance (unconditional; falls
through while on cooldown) -> attacks strongest first, each gated at range+1 except ALL-method ->
unconditional move_towards_opponent. includeDefaultRules false (project standard).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, 'skills/building-tnr-content/scripts')
from factory import Factory  # noqa: E402

AI_BUNDLE = 'harvests/inbox/tnr_results_1792731111886.json'   # push/222
JUTSU_BUNDLE = 'harvests/inbox/tnr_results_1792731158723.json'  # public jutsu.getAll (AI type)
OUT = 'push/223_six_ai_kits.json'

ROSTER = [  # name, userId, rank, kit codes (approved 2026-10-23)
    ("Mara Vane", "fv33ZNwcZ_eXFWt-d-yrF", "JONIN", ["S03", "S04", "S44", "B37", "S35"]),
    ("Kellan Flint", "dVr5LmHVke0wYz52uWlZr", "JONIN", ["S06", "S07", "S08", "S29", "B38"]),
    ("Sable Crow", "FQ0ouWe29LXiUficxTACS", "JONIN", ["S04", "S29", "S28", "B33", "B21"]),
    ("Brigg Tusk", "t4tCdrXKXhQ15l3u4XH-c", "JONIN", ["S01", "B28", "B26", "EE02", "B22"]),
    ("Yara Reed", "mNvh7ddWnV412kGt9zVX8", "ELITE JONIN", ["A1", "S27", "S29", "B36", "B20", "S35"]),
    ("Goro Blackthorn", "fh8BgCYYChLhPNMFKRZ4I", "ELITE JONIN", ["B14", "B30", "B35", "B33", "B19", "S36"]),
]
SECOND_WIND = "S35"
D = 'skills/building-tnr-content/data/'


def main():
    f = Factory(ctors=D + '45c_DATA_constructors.json', entities=D + '45d_DATA_entity_schemas.json', checks=D + '45g_DATA_checks.json')
    pool = json.load(open('skills/building-tnr-content/data/32b_DATA_pool.json'))['records']
    live_j = {}
    for c in json.load(open(JUTSU_BUNDLE))['captures']:
        for j in c['data']['data']:
            live_j[j['id']] = j
    live_ai = {c['data']['userId']: c['data'] for c in json.load(open(AI_BUNDLE))['captures']
               if c['proc'] == 'profile.getAi' and c.get('ok')}

    def power(j):  # strongest first: summed damage/pierce power, then longer cooldown
        p = sum(e.get('power', 0) for e in j['effects'] if e['type'] in ('damage', 'pierce'))
        return (-p, -j['cooldown'])

    items, notes = [], []
    for name, uid, rank, codes in ROSTER:
        a = live_ai[uid]
        if a['username'].strip() != name:
            raise SystemExit(f'{uid}: live name {a["username"]!r} != {name!r}')
        if a.get('jutsus') or a.get('items'):
            raise SystemExit(f'{name}: live kit is not empty; this generator assumes a blank AI')
        kit = [(c, live_j[pool[c]['id']]) for c in codes]
        heal = [(c, j) for c, j in kit if c == SECOND_WIND]
        selfs = [(c, j) for c, j in kit if j['target'] == 'SELF' and c != SECOND_WIND]
        attacks = sorted([(c, j) for c, j in kit if j['target'] != 'SELF'], key=lambda x: power(x[1]))
        rules, ranges = [], {}
        for c, j in heal:
            rules.append(f.rule(f.condition('round_lower_than', value=5), f.condition('health_below', value=50),
                                action=f.action('use_specific_jutsu', jutsuId=j['id'], target='SELF')))
        for c, j in selfs:
            rules.append(f.rule(action=f.action('use_specific_jutsu', jutsuId=j['id'], target='SELF')))
        for c, j in attacks:
            if j['method'] == 'ALL':
                rules.append(f.rule(action=f.action('use_specific_jutsu', jutsuId=j['id'], target='CLOSEST_OPPONENT')))
                continue
            ranges[j['id']] = j['range']
            rules.append(f.rule(f.condition('distance_lower_than', value=j['range'] + 1, target='CLOSEST_OPPONENT'),
                                action=f.action('use_specific_jutsu', jutsuId=j['id'], target='CLOSEST_OPPONENT')))
        rules.append(f.rule(action=f.action('move_towards_opponent', target='CLOSEST_OPPONENT')))
        rules, warn = f.rules(*rules, ranges=ranges)
        notes += [f'{name}: {w}' for w in warn]
        order = [c for c, _ in heal] + [c for c, _ in selfs] + [c for c, _ in attacks]
        items.append({
            "entity": "ai", "slot": "edit", "targetId": uid,
            "name": f"{name} (L{a['level']}): {rank}, kit {' '.join(order)} + basic rules",
            "data": {"rank": rank,
                     "jutsus": [pool[c]['id'] for c in codes], "items": [],
                     "rules": rules, "includeDefaultRules": False},
        })
    m = {"_note": "Six new bandit-camp AIs (director, 2026-10-23): Mara Vane L70, Kellan Flint L80, Sable Crow L90, Brigg Tusk L100 -> JONIN; Yara Reed L110, Goro Blackthorn L120 -> ELITE JONIN (they were STUDENT, which caps every stat at 20k in battle). Kits from the shared AI pool (approved). Basic rules: Second Wind only before round 5 and below 50% HP; stance unconditional; attacks strongest first, each gated at range+1 (ALL-method ungated); move_towards_opponent last; includeDefaultRules false. Kellan Flint has no AI profile yet; Forge toggles one before writing his rules. Live stats, pools and the rest of each record are re-sent unchanged (Forge mergeAi). Before-image: push/222 (" + AI_BUNDLE + "). Generated by push/223_six_ai_kits.gen.py; do not hand-edit. Direct edit (AI records); operator runs it from Forge.",
         "items": items,
         "capture": {"before": [], "after": [{"proc": "profile.getAi", "input": {"userId": uid}, "persist": "full"} for _, uid, _, _ in ROSTER]}}
    json.dump(m, open(OUT, 'w'), indent=1, ensure_ascii=False)
    open(OUT, 'a').write('\n')
    print(f'wrote {OUT}: {len(items)} AI edits')
    for n in notes:
        print('  note:', n)


if __name__ == '__main__':
    main()
