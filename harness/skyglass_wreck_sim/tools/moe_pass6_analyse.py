import json,sys,collections,statistics
ERUPT=("Refraction","Facet","Lucid","Nothing Moves","Stillness","Recast","Shatterfall","Names","Every Name","Glassfall")
SUMMON=("Feeler","Likeness","Your Own","Worn","Porter","Tomo","Hana")
def cat(src):
    if src.startswith("own turn"): return "pools/drain"
    who,_,move=src.partition(": ")
    if "Glass Remembers" in move: return "enrage"
    if any(w in who for w in SUMMON): return "summon"
    if any(move.startswith(e) or e in move for e in ERUPT): return "eruption"
    if "Breathless" in move: return "Breathless Pull"
    return "filler"
HP=6250
for f in sys.argv[1:]:
    d=json.load(open(f))
    for cn,c in d['cells'].items():
        label=cn+("" if d.get('kill','sayo')=='sayo' else " (silence first)")
        byround=collections.Counter(); deaths=collections.Counter(); per=collections.defaultdict(lambda:[0,0,0]); endhp=[]
        for r in c['runs']:
            for a in r['acts']:
                if a.get('deathCause'): deaths[cat(a['deathCause'])]+=1; byround[(a['act'], (a['rounds']-1)//10*10)]+=1
                g=per[a['act']]
                filler=sum(v for k,v in (a.get('dmgBySource') or {}).items() if cat(k)=='filler')
                g[0]+=filler; g[1]+=a['rounds']; g[2]+=sum((a.get('bossTurns') or {}).values())
            if r['cleared']: endhp.append(100*r['acts'][-1]['endHp'])
        fill={act:(round(100*v[0]/max(1,v[1])/5050,1), round(100*v[0]/max(1,v[2])/5050,1)) for act,v in sorted(per.items())}
        print(f"{label}: clears {sum(r['cleared'] for r in c['runs'])}/{len(c['runs'])}; median end HP of clears {round(statistics.median(endhp)) if endhp else '-'}%; filler % of 5,050 per round / per boss turn by act {fill}; deaths {dict(deaths)}; deaths by act/round band {dict(sorted(byround.items()))}")
