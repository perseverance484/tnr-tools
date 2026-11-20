import json,sys
for n in sys.argv[1:]:
    try: d=json.load(open(f'out/{n}.json'))
    except Exception as e: print(n,'ERR',e); continue
    for r,v in d['reads'].items():
        s=v['summary']; a=s['bossActsPerFight']
        print(f"{n:6} r{r:4} win {s['winPct']:5} rW {s['rounds']['median']}/{s['rounds']['p90']} rAll {s['roundsAll']['median']}/{s['roundsAll']['max']} hp {s['hpLeftWin']['median']} idle {s['idleRoundsPerFight']} pet {s['petDiedRound']} scour {a.get('Scour',0)} hide {a.get('Hide',0)} harp {a.get('Harpoon',0)} flood {a.get('Flood',0)} bite {a.get('Bite',0)} UT {s['undertowDmgMedian']} lossBoss {s['bossHpLeftLossMedian']}")
