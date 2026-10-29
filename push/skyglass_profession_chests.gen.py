import json,glob,collections,itertools
import sys; SP=sys.argv[1] if len(sys.argv)>1 else 'state/skyglass_design/'
items={}
for f in glob.glob('harvests/inbox/tnr_results_17932*.json'):
    for c in json.load(open(f)).get('captures',[]):
        x=c.get('data')
        if c.get('proc')=='item.get' and isinstance(x,dict): items[x['name']]=x
byid={x['id']:x for x in items.values()}
recs=[r for r in json.load(open(SP+'recipes.json')).values() if not r.get('hidden') and r.get('craftingRequirements')]
RAR=['COMMON','RARE','EPIC','LEGENDARY']; LOT={'COMMON':2,'RARE':3,'EPIC':5,'LEGENDARY':10}
EXCL={'Frostbite Leaf','Heart of Kaeruun','Seed of False Vitality','Imperial Gold','Bloodcore Ore','Bloodflower'}
def prof_ok(m,p): return (m['canBeHunted'] if p=='H' else m['canBeGathered'])
demand=collections.Counter(); kits=collections.defaultdict(list)
for r in recs:
    for p in 'HG':
        for rar in RAR:
            part=[(q['requirementItem']['name'],q['quantity']) for q in r['craftingRequirements']
                  if (m:=items.get(q['requirementItem']['name'])) and m['itemType']=='MATERIAL' and prof_ok(m,p) and m['rarity']==rar and not m['hidden'] and m['name'] not in EXCL]
            for n,qq in part: demand[(p,n)]+=qq
            if len(part)>=2: kits[(p,rar)].append((r['name'],tuple(sorted(part))))
def mats(p,rar):
    out=[]
    for m in items.values():
        if m['itemType']=='MATERIAL' and prof_ok(m,p) and m['rarity']==rar and not m['hidden'] and demand[(p,m['name'])]>0 and m['name'] not in EXCL:
            out.append(m['name'])
    if p=='G' and rar=='COMMON' and 'Copper Ore' not in out: out.append('Copper Ore')
    return sorted(out,key=lambda n:-demand[(p,n)])
def val(n): return items[n]['cost']
def entval(e): return sum(q*val(n) for n,q in e)
def chest(p,rar,target):
    i=RAR.index(rar); lot=LOT[rar]
    staples=mats(p,rar)
    # demand-weighted entries: copies proportional to demand (max 50 entries)
    tot=sum(demand[(p,n)] for n in staples)
    st_entries=[]
    for n in staples:
        k=max(1,round(20*demand[(p,n)]/tot))
        st_entries+= [((n,2*lot),)]*k
    kitlist={}
    for name,part in kits[(p,rar)]:
        kitlist.setdefault(part,name)
    kit_entries=[tuple((n,q) for n,q in part) for part in kitlist][:12]
    bulk=[((n,6*lot),) for n in staples[:3]]
    # RUL-2026-10-29-036: no Upgrade tier; its 2% goes back as Staples +1, Recipe kit +1 (Legendary keeps 55/25/12/8).
    tiers=[['Staples',5500,st_entries],['Recipe kit',2500,kit_entries or st_entries],['Bulk',1200,bulk]]
    if i<3:
        up=RAR[i+1]; ups=mats(p,up)[:4]
        tiers[0][1]+=100; tiers[1][1]+=100
        tiers.append(['Windfall',600,[((n,LOT[up]),) for n in ups]])
    else:
        heir=[tuple((n,q) for n,q in part) for name,part in kits[(p,rar)] if len(part)>=3][:4] or kit_entries
        tiers.append(['Heirloom',800,[tuple((n,q*2) for n,q in e) for e in heir]])
    s=sum(t[1] for t in tiers); tiers[0][1]+=10000-s
    rolls=[(3,6000),(4,3000),(6,1000)]
    return tiers,rolls
def ev(tiers,rolls,chestvals):
    per=0
    for name,pr,ents in tiers:
        vs=[sum(chestvals.get(n[9:],0) if n.startswith('__chest__') else q*val(n) for n,q in e) for e in ents]
        per+=pr/10000*sum(vs)/len(vs)
    return per*sum(c*p/10000 for c,p in rolls)
OLD={('H','COMMON'):4.2e6,('H','RARE'):6.0e6,('H','EPIC'):7.0e6,('H','LEGENDARY'):10.56e6,('G','COMMON'):3.2e6,('G','RARE'):None,('G','EPIC'):None,('G','LEGENDARY'):10.0e6}
# compute old gatherer values
for p,rar in OLD:
    if OLD[(p,rar)] is None:
        x=items[f"{rar.title()} {'Hunter' if p=='H' else 'Gatherer'}'s Chest"]
        OLD[(p,rar)]=sum(r['number']/100*r.get('quantity',1)*byid[r['ids'][0]]['cost'] for e in x['effects'] for r in (e.get('reward_items') or []) if r['ids'][0] in byid)
res={}
out=[]
for p in 'HG':
    cv={}
    for rar in reversed(RAR):
        tiers,rolls=chest(p,rar,OLD[(p,rar)])
        # scale quantities to target value
        base=[[t[0],t[1],t[2]] for t in tiers]; lot=LOT[rar]; best=None  # quantities clamped to the engine cap of 100
        for k in range(1,40):
            tt=[[t[0],t[1],[tuple((n,q if n.startswith('__chest__') else min(100//lot*lot,(lambda r: max(1,round(r*k/2)))(q//lot if q>=lot else 1)*lot)) for n,q in ent) for ent in t[2]]] for t in base]
            e=ev(tt,rolls,cv)
            if best is None or abs(e-OLD[(p,rar)])<abs(best[0]-OLD[(p,rar)]): best=(e,tt,k)
        e2,tiers,f=best; cv[rar]=e2
        res[(p,rar)]=(tiers,rolls,e2,OLD[(p,rar)],f)
json.dump({f"{p}:{r}":[[t[0],t[1],[[list(x) for x in en] for en in t[2]]] for t in v[0]] for (p,r),v in res.items()},open(SP+'chests.json','w'),indent=1)
for (p,rar),(tiers,rolls,e2,old,f) in res.items():
    print(f"\n### {rar.title()} {'Hunter' if p=='H' else 'Gatherer'}'s Chest — EV {e2/1e6:.1f}M (old {old/1e6:.1f}M), scale {f:.2f}")
    for name,pr,ents in tiers:
        uniq=[]
        for en in ents:
            s=' + '.join(f"{n.replace('__chest__','').title()+' chest' if n.startswith('__chest__') else n} ×{q}" for n,q in en)
            if s not in uniq: uniq.append(s)
        print(f"- {name} {pr/100:.0f}%: " + ' | '.join(uniq[:6]) + (' | …' if len(uniq)>6 else ''))
