#!/usr/bin/env python3
"""Pacing + ledger for the Nettle Nova asset job (push/698).
  next N            -> prints the next N assets still to CREATE (create inputs), after pacing for N calls
  created srcId=id ...  -> records created ids
  upd N             -> prints update inputs (hidden true) for up to N created-not-updated assets, after pacing
  updated srcId ... -> records image updates done
  unhide N          -> prints update inputs (hidden false) for up to N assets not yet unhidden, after pacing
  unhidden srcId ...-> records unhides done
  status            -> counts
  ledger.json (srcId -> id) is rewritten on every record. Pacing: <= 20 game calls in any rolling 60 s."""
import json, os, sys, time
D = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(f'{D}/assets.json'))
LOG = f'{D}/ledger_698.jsonl'; CALLS = f'{D}/calls_698.json'
LIC = 'CC0 1.0 - OpenDuelyst (open-duelyst/duelyst @ df697549ca) effect sheets, recoloured and composited for TNR, plus code-drawn pieces'
FOLDER = 'resortneednn'; RATE = 20

def state():
    st = {}
    if os.path.exists(LOG):
        for line in open(LOG):
            r = json.loads(line); s = st.setdefault(r['srcId'], {})
            s.update({k: v for k, v in r.items() if k != 'srcId'})
    return st

def record(kind, args):
    st = state(); by = {a['srcId'] for a in A}
    with open(LOG, 'a') as f:
        for a in args:
            if kind == 'created':
                sid, aid = a.split('=', 1); assert sid in by and aid and 'id' not in st.get(sid, {}), a
                f.write(json.dumps({'srcId': sid, 'id': aid, 'created': True, 't': time.time()}) + '\n')
            else:
                assert a in st and 'id' in st[a], a
                f.write(json.dumps({'srcId': a, kind: True, 't': time.time()}) + '\n')
    st = state()
    json.dump({k: v['id'] for k, v in st.items() if 'id' in v}, open(f'{D}/ledger.json', 'w'), indent=0)
    print(kind, len(args), '| totals', counts(st))

def counts(st):
    return {'created': sum('id' in v for v in st.values()), 'updated': sum(bool(v.get('updated')) for v in st.values()),
            'unhidden': sum(bool(v.get('unhidden')) for v in st.values()), 'of': len(A)}

def pace(n):
    t = json.load(open(CALLS)) if os.path.exists(CALLS) else []
    while True:
        now = time.time(); t = [x for x in t if now - x < 60]
        if len(t) + n <= RATE: break
        time.sleep(max(0.5, 60 - (now - t[0]) + 0.2))
    now = time.time(); t += [now] * n; json.dump(t, open(CALLS, 'w'))

def data(a, hidden):
    return {'name': a['name'], 'image': a['url'], 'frames': a['frames'], 'speed': a['speed'], 'type': a['type'],
            'licenseDetails': LIC, 'onInitialBattleField': False, 'hidden': hidden, 'folder': FOLDER}

if __name__ == '__main__':
    cmd, rest = sys.argv[1], sys.argv[2:]
    st = state()
    if cmd == 'status': print(counts(st))
    elif cmd in ('created', 'updated', 'unhidden'): record(cmd, rest)
    else:
        n = int(rest[0]) if rest else 5
        if cmd == 'next': todo = [a for a in A if 'id' not in st.get(a['srcId'], {})][:n]
        elif cmd == 'upd': todo = [a for a in A if 'id' in st.get(a['srcId'], {}) and not st[a['srcId']].get('updated')][:n]
        elif cmd == 'unhide': todo = [a for a in A if st.get(a['srcId'], {}).get('updated') and not st[a['srcId']].get('unhidden')][:n]
        if not todo: print('NOTHING LEFT'); sys.exit(0)
        pace(len(todo))
        for a in todo:
            if cmd == 'next': print(a['srcId'], json.dumps({'name': a['name'], 'type': a['type'], 'folder': FOLDER}))
            else: print(a['srcId'], json.dumps({'id': st[a['srcId']]['id'], 'data': data(a, cmd == 'upd' and True or False)}))
