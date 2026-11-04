import json,collections,csv,re,statistics as st
"""Classify every captured quest with requiredLevel <= 70 by its job in the levelling loop.

Run from this directory: python3 -I build.py
Reads harvests/inbox/tnr_results_*.json (de-duplicated by id, largest copy kept) and
harvests/seed/41_INDEX_item.json from the repo root; writes quests_l1_70.json/.csv here.
Classification is rule-based on questType and name, not a reading of each quest's prose.
"""
import glob,os
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..','..'))
def _walk(o):
    if isinstance(o,dict):
        if 'questType' in o and 'name' in o and 'id' in o and isinstance(o.get('content'),dict): yield o
        for v in o.values(): yield from _walk(v)
    elif isinstance(o,list):
        for v in o: yield from _walk(v)
Q={}
for _f in sorted(glob.glob(os.path.join(ROOT,'harvests','inbox','tnr_results_*.json'))):
    try: _d=json.load(open(_f))
    except Exception: continue
    for _q in _walk(_d):
        if _q['id'] not in Q or len(json.dumps(_q))>len(json.dumps(Q[_q['id']])): Q[_q['id']]=_q
for _q in Q.values():
    _q['content'].setdefault('objectives',[])
items={r[0]:r[1] for r in json.load(open(os.path.join(ROOT,'harvests','seed','41_INDEX_item.json')))['rows']}
ex=[q for q in Q.values() if q.get('requiredLevel',999)<=70]
TEST=re.compile(r'^New Quest|WEDGE_PROBE|Canary|keep out|DO NOT TAKE|Staff test|Rep for Skill Tree',re.I)
SPINE_EXAM=re.compile(r'Genin Trials|Chunin Exam|Path of a Shinobi|Getting Started|Road to Genin')
ENERGY=re.compile(r'energy|stamina|chakra|potion|pill|panacea|ramen|food',re.I)
def band(l):
    l=max(l,1)
    if l>=60: return '60-70'
    b=(l//10)*10
    return '1-10' if b==0 else f'{b}-{b+10}'
BANDS=['1-10','10-20','20-30','30-40','40-50','50-60','60-70']
BLO={'1-10':1,'10-20':10,'20-30':20,'30-40':30,'40-50':40,'50-60':50,'60-70':60}
BHI={'1-10':9,'10-20':19,'20-30':29,'30-40':39,'40-50':49,'50-60':59,'60-70':70}
def classify(q):
    t=q['questType']; n=q['name']; tasks=[o['task'] for o in q['content']['objectives']]
    daily = q.get('retryDelay')=='daily' or t=='daily'
    if TEST.search(n) or TEST.search(q.get('description') or ''): return 'other','staff/test stub'
    if SPINE_EXAM.search(n) and t in('starter','event'): return 'spine','exam chain'
    if t=='starter' and 'seeds_planted' in tasks: return 'onboarding','farming'
    if t=='starter': return 'spine','starter'
    if t=='daily': return 'grind_daily','daily'
    if t in('mission','crime','errand'): return 'grind_missionhall',t
    if t=='village_mission': return 'grind_missionhall','village_mission'
    if t in('battlepyramid','raid'): return 'capstone',t+(' (daily)' if daily else '')
    if t=='gathering': return 'system','gathering'
    if t=='hunting': return 'system','hunting'
    if t=='medical': return 'system','medical'
    if t=='anbu': return 'system','anbu'
    if t in('pvp','war'): return 'system','pvp'+('/war' if t=='war' else '')
    if t=='achievement': return 'achievement',(tasks[0] if tasks else '')
    if t=='tier': return 'achievement','tier'
    if t=='story':
        if n.startswith('Relic:'): return 'achievement','relic unlock (pvp/arena grind)'
        if 'EMERGENCY' in (q.get('description') or ''): return 'event','emergency dispatch'
        return 'spine','story'
    if t=='event':
        if 'deliver_item' in tasks: return 'grind_daily','profession supply turn-in'
        return 'event','event'
    if t=='overworld': return ('grind_daily' if daily else 'spine'),'overworld'+(' (daily)' if daily else ' chain')
    return 'other',t
def rew(o):
    return o.get('reward_exp',0) or 0, o.get('reward_money',0) or 0
rows=[]
for q in sorted(ex,key=lambda q:(q['requiredLevel'],q['questType'],q['name'])):
    R=q['content']['reward']; objs=q['content']['objectives']
    allr=[R]+objs
    exp=sum(r.get('reward_exp',0) or 0 for r in allr); ryo=sum(r.get('reward_money',0) or 0 for r in allr)
    it=[]; jut=[]; en=[]
    for r in allr:
        for i in r.get('reward_items') or []:
            for iid in i.get('ids',[]):
                nm=items.get(iid,iid); it.append(f"{nm} x{i.get('quantity',1)} @{i.get('number')}%")
                if ENERGY.search(nm): en.append(nm)
        jut+= r.get('reward_jutsus') or []
    fn,tag=classify(q)
    tc=collections.Counter(o['task'] for o in objs)
    pre=q.get('prerequisiteQuestId')
    rows.append(dict(id=q['id'],name=q['name'].strip(),type=q['questType'],rank=q['questRank'],
        requiredLevel=q['requiredLevel'],maxLevel=q.get('maxLevel'),band=band(q['requiredLevel']),hidden=bool(q.get('hidden')),
        retryDelay=q.get('retryDelay'),maxCompletes=q.get('maxCompletes'),repeat=('daily' if q.get('retryDelay')=='daily' else ('multi' if (q.get('maxCompletes') or 1)>1 else 'once')),
        prereq=(Q[pre]['name'].strip() if pre in Q else pre),
        profRank={k:q.get(k) for k in('gatheringRank','huntingRank','medicalRank') if q.get(k) not in(None,'NONE')},
        village=(q.get('village') or {}).get('name') if isinstance(q.get('village'),dict) else None,
        startsAt=q.get('startsAt'),endsAt=q.get('endsAt'),
        objective_tasks=dict(tc),
        exp_reward=R.get('reward_exp',0),ryo_reward=R.get('reward_money',0),exp_total=exp,ryo_total=ryo,
        items=it,jutsus=jut,energy_items=en,
        tokens=R.get('reward_tokens',0),prestige=R.get('reward_prestige',0),badges=len(R.get('reward_badges') or []),
        prof_xp={k[7:]:R.get(k) for k in R if k.endswith('_experience') and R.get(k)},
        function=fn,function_tag=tag))
json.dump(rows,open('quests_l1_70.json','w'),indent=1,ensure_ascii=False)
with open('quests_l1_70.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]))
    w.writeheader()
    for r in rows: w.writerow({k:(json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v) for k,v in r.items()})
V=[r for r in rows if not r['hidden']]; H=[r for r in rows if r['hidden']]
print('total',len(rows),'visible',len(V),'hidden',len(H))
fns=['spine','onboarding','system','grind_missionhall','grind_daily','capstone','achievement','event','other']
print('func'.ljust(18),*[b.rjust(6) for b in BANDS],'  tot')
for fn in fns:
    c=[sum(1 for r in V if r['function']==fn and r['band']==b) for b in BANDS]
    print(fn.ljust(18),*[str(x).rjust(6) for x in c],str(sum(c)).rjust(5), ' | hidden',sum(1 for r in H if r['function']==fn))
print('subtags visible',collections.Counter((r['function'],r['function_tag']) for r in V))
# mission hall
MH=[r for r in V if r['function']=='grind_missionhall']
print('\nMH by rank x introduced band')
for rk in 'DCBAS':
    print(rk,[sum(1 for r in MH if r['rank']==rk and r['band']==b) for b in BANDS],
      'avail:',[sum(1 for r in MH if r['rank']==rk and r['requiredLevel']<=BHI[b] and (r['maxLevel'] or 100)>=BLO[b]) for b in BANDS])
    xs=[r for r in MH if r['rank']==rk]
    if xs: print('   n',len(xs),'median exp',st.median(r['exp_total'] for r in xs),'ryo',st.median(r['ryo_total'] for r in xs),'min/max exp',min(r['exp_total'] for r in xs),max(r['exp_total'] for r in xs),'ryo',min(r['ryo_total'] for r in xs),max(r['ryo_total'] for r in xs))
print('MH by type',collections.Counter((r['type'],r['rank']) for r in MH))
for r in MH: print('  ',r['type'][:4],r['rank'],r['requiredLevel'],r['maxLevel'],r['exp_total'],r['ryo_total'],r['name'][:40],r['items'][:1])
# dailies
print('\nDAILY/repeat')
for r in rows:
    if r['repeat']!='once' or r['function']=='grind_daily':
        print(' H' if r['hidden'] else ' V',r['type'][:8],r['requiredLevel'],r['maxLevel'],r['retryDelay'],r['maxCompletes'],r['name'][:42],r['objective_tasks'],r['exp_total'],r['ryo_total'])
# windows
print('\nBROKEN windows')
for r in rows:
    if r['maxLevel'] is not None and r['maxLevel']<r['requiredLevel']: print(' maxLevel<req',r['name'])
    if r['startsAt'] and r['endsAt'] and r['startsAt']>r['endsAt']: print(' startsAt>endsAt',r['name'],r['startsAt'],r['endsAt'],'H' if r['hidden'] else 'V')
    if r['endsAt'] and r['endsAt']<'2026-11-04' and not r['hidden']: print(' expired but visible',r['name'],r['endsAt'])
    if r['maxLevel'] is not None and r['maxLevel']-r['requiredLevel']<=5: print(' narrow window',r['name'],r['requiredLevel'],r['maxLevel'],'H' if r['hidden'] else 'V')
print('energy items',[(r['name'],r['energy_items']) for r in rows if r['energy_items']])
print('jutsus',[(r['name'],r['jutsus']) for r in rows if r['jutsus']])
