import json,re,os,subprocess
R='/tmp/tnrgit/repo/app/src'
ct=open(R+'/validators/combat.ts').read().split('\n')
tg=open(R+'/libs/combat/tags.ts').read().split('\n')
pr=open(R+'/libs/combat/process.ts').read().split('\n')
ut=open(R+'/libs/combat/util.ts').read().split('\n')
d=json.load(open('/tmp/map/data.json'))
raw=json.load(open('/tmp/map/tags_raw.json'))
def line_of(lines,pat,start=0):
    for i,l in enumerate(lines[start:],start):
        if re.search(pat,l): return i+1
    return None
HANDLER={"damage":"damageUser","pierce":"damageUser","elementaldamage":None,"onehitkill":"onehitkill","weakness":"weakness","wound":"wound","afterburn":"afterburn","poison":"poison","drain":"drain","diffuse":None,"curse":"curse","increasedamagegiven":"increaseDamageGiven","decreasedamagegiven":"decreaseDamageGiven","increasedamagetaken":"increaseDamageTaken","decreasedamagetaken":"decreaseDamageTaken","increasepotency":"potency","decreasepotency":"potency","increasestat":"increaseStats","decreasestat":"decreaseStats","increasemastery":"increaseMastery","decreasemastery":"decreaseMastery","shield":"shield","barrier":"damageBarrier","absorb":"absorb","siphon":"registerShieldConversion","consume":"registerShieldConversion","finalstand":"finalStand","reflect":"reflect","parry":"parry","recoil":"recoil","mirror":"mirror","heal":"heal","lifesteal":"lifesteal","vamp":"vamp","increaseheal":"increaseHealGiven","decreaseheal":"decreaseHealGiven","clear":"clear","cleanse":"cleanse","copy":"copy","immunity":"immunity","stun":"stun","seal":"seal","elementalseal":"elementalseal","stealth":"stealth","timecompression":"temporalShift","timedilation":"temporalShift","increasepoolcost":"increasepoolcost","decreasepoolcost":"decreasepoolcost","increasecooldown":"increaseCooldown","decreasecooldown":"decreaseCooldown","injectjutsus":"injectjutsus","increaserange":"increaseRange","move":"move","redirection":"redirection","summon":"summon","clone":"clone","increasemaxpools":"increaseMaxPools","decreasemaxpools":"decreaseMaxPools","rob":"rob","flee":"flee","increaseaggro":"adjustAggro","decreaseaggro":"adjustAggro"}
for p in "buffprevent debuffprevent clearprevent cleanseprevent stunprevent sealprevent summonprevent onehitkillprevent robprevent fleeprevent healprevent moveprevent disarm".split(): HANDLER[p]="applyPreventTag"
EXTRA_SRC={
 "elementaldamage":["libs/combat/elementalDamage.ts resolveElementalDamage"],
 "diffuse":["libs/combat/damagePipeline.ts applyDiffuseToConsequences"],
 "curse":["libs/combat/tags.ts settleCurse","libs/combat/damagePipeline.ts getCurseDamageMultiplier (curse bonus)"],
 "increasedamagegiven":["libs/combat/damagePipeline.ts computeDamagePacket"],"decreasedamagegiven":["libs/combat/damagePipeline.ts computeDamagePacket"],"increasedamagetaken":["libs/combat/damagePipeline.ts computeDamagePacket"],"decreasedamagetaken":["libs/combat/damagePipeline.ts computeDamagePacket"],
 "increasepotency":["libs/combat/potency.ts resolvePotencyTags"],"decreasepotency":["libs/combat/potency.ts resolvePotencyTags"],
 "shield":["libs/combat/process.ts mitigateConsequence"],"finalstand":["libs/combat/tags.ts applyFinalStandDamage"],
 "pierce":["libs/combat/process.ts mitigateConsequence (destroys shields)"],
 "stun":["libs/combat/turn.ts calcApReduction"],
 "stealth":["libs/combat/actions.ts availableUserActions","libs/combat/actions.ts (stealthed target skipped)"],
 "disarm":["libs/combat/actions.ts availableUserActions"],"moveprevent":["libs/combat/actions.ts availableUserActions"],"summonprevent":["libs/combat/actions.ts availableUserActions"],"elementalseal":["libs/combat/actions.ts availableUserActions"],"injectjutsus":["libs/combat/actions.ts availableUserActions"],
 "seal":["libs/combat/util.ts isEffectEnabled / sealCheck"],
 "weakness":["libs/combat/tags.ts calcDmgModifier"],
 "barrier":["libs/combat/actions.ts (barrier path absorb)"],
 "damage":["libs/combat/tags.ts damageCalc","libs/combat/damagePipeline.ts computeDamagePacket"],
}
def schema_lines(k):
    s=line_of(ct,r'^export const '+k+r'\s*=')
    return s
def field_specs(k):
    v=raw[k]; blk=v['block']; out={}
    for m in re.finditer(r'^\s{2}(\w+):\s*(.+?),?\s*$',blk,re.M):
        n,e=m.group(1),m.group(2)
        if n in('type','description'):continue
        out[n]=e.rstrip(',')
    return out
GROUPS=["IncludeGeneralsAndElements","DamageModifierAttributes","HealModifierAttributes","PotencyAttributes","PoolCostAttributes","MaxPoolsAttributes","StatModifierAttributes","AggroAttributes","TimeShiftAttributes","PoolAttributes","ActivityBonusAttributes","PercentageCalculation","AggroAttributes"]
src='\n'.join(ct)
gspec={}
for g in GROUPS:
    m=re.search(r'const '+g+r' = \{(.*?)\n\};',src,re.S)
    if not m: continue
    sp={}
    for mm in re.finditer(r'^\s{2}(\w+):\s*(.+?),?\s*$',m.group(1),re.M): sp[mm.group(1)]=mm.group(2).rstrip(',')
    sp['_spreads']=re.findall(r'\.\.\.(\w+)',m.group(1))
    gspec[g]=sp
def resolve_group(g,acc):
    sp=gspec.get(g,{})
    for s in sp.get('_spreads',[]):
        if s not in('BaseAttributes','PowerAttributes'): resolve_group(s,acc)
    for k,v in sp.items():
        if k!='_spreads': acc[k]=v
EDGE_SRC={}
edges=d['edges']
EX_AREA={"dmgnow":"Damage now","dmglater":"Damage later","scaling":"Damage scaling","soak":"Soak damage","sendback":"Send it back","heal":"Healing","remove":"Remove effects","take":"Take effects","protect":"Protection","deny":"Deny actions","speed":"Speed up actions","position":"Position","fighters":"Extra fighters","pools":"Pools and money","escape":"Escape","aggro":"Enemy AI focus (PvE)","sage":"Sage mode","noncombat":"Outside battle or cosmetic"}
STAGE_TXT={"s0":"A0 cast prep","s1":"A1 copy and mirror (run first)","s2":"A2 prevents","s3":"A3 pre-modifiers","s4":"A4 mid-modifiers","s10":"A5 late main pass (unranked or last-ranked)","s7":"A8 damage pipeline","s8":"A9 pierce","s9":"A10 post-damage readers","nc":"outside combat"}
LIVE={}
for t in "increasedamagegiven decreasedamagegiven increasedamagetaken decreasedamagetaken increasestat decreasestat increasemastery decreasemastery increasepotency decreasepotency absorb reflect parry recoil afterburn lifesteal increaseheal decreaseheal".split(): LIVE[t]="next round (waits while isNew/castThisRound)"
for t in "damage pierce heal".split(): LIVE[t]="on cast if rounds 0 (instant); residual ticks on later rounds"
TICK=set("damage pierce heal drain wound poison clear cleanse flee rob stun seal increasepoolcost decreasepoolcost onehitkill increaseaggro decreaseaggro".split())
def yq(s):
    s=str(s)
    if s=='' : return '""'
    if re.search(r'[:#\[\]{}&*!|>\'"%@`,]|^\s|\s$|^-',s) or s.lower() in('yes','no','true','false','null','on','off'):
        return '"'+s.replace('\\','\\\\').replace('"','\\"')+'"'
    return s
os.makedirs('/tmp/map/kb/tags',exist_ok=True)
index=[]
for n in d['nodes']:
    t=n['id'];k=n['schema']
    L=[]
    L.append(f"tag: {t}")
    L.append(f"schema: validators/combat.ts {k} (line {schema_lines(k)})")
    L.append(f"exclusion_area: {yq(EX_AREA[n['area']])}")
    L.append(f"in_game_text: {yq(n['desc'])}")
    L.append(f"behavior: {yq(n['beh'])}")
    L.append(f"polarity: {n['pol']}   # positive = Clear removes; negative = Cleanse removes; neutral = neither")
    L.append(f"prevented_by: [{', '.join(n['pb'])}]" if n['pb'] else "prevented_by: []   # no prevent check in its handler")
    L.append(f"copy_can_take: {str(n['copy']).lower()}")
    L.append(f"mirror_can_pass: {str(n['mirror']).lower()}")
    L.append(f"potency_eligible: {str(n['potency']).lower()}")
    L.append(f"immunity_can_cancel: {str(n['prevtype']).lower()}")
    L.append(f"stage: {yq(STAGE_TXT.get(n['stage'],n['stage']))}")
    if t in LIVE: L.append(f"live_from: {yq(LIVE[t])}")
    if t in TICK: L.append("applies: on landing, then once a round when the holder acts")
    L.append(f"calculation: [{n['calc'] or 'static'}]")
    fs=field_specs(k)
    for g in raw[k]['spreads']:
        if g not in('BaseAttributes','PowerAttributes'):
            acc={};resolve_group(g,acc)
            for a,b2 in acc.items(): fs.setdefault(a,b2)
    if raw[k]['helper']=='basicActionTag': fs.setdefault('actionsAffected','array of AdjustableBasicActions (see basicActionTag)')
    if raw[k]['helper']=='masteryModifierTag': fs.setdefault('masteryTypes','array of MasteryTypes (see masteryModifierTag)')
    if raw[k]['helper']=='simpleTag': L.append("fields_note: simpleTag (BaseAttributes + PowerAttributes only)")
    if fs:
        L.append("own_fields:   # zod expressions copied from the schema; base fields are in engine.md section 6")
        for a,b2 in fs.items(): L.append(f"  {a}: {yq(b2)}")
    L.append(f"live_usage_2026_11_21: {{jutsu: {n['use']}, pvp_legal: {n['pvp']}}}")
    srcs=[]
    h=HANDLER.get(t)
    if h:
        ln=line_of(tg,r'^export const '+h+r'\s*=') or line_of(tg,r'^const '+h+r'\s*=')
        srcs.append(f"libs/combat/tags.ts {h} (line {ln})")
    dl=line_of(pr,r'effect\.type === "'+t+r'"')
    if dl: srcs.append(f"libs/combat/process.ts first reference (line {dl})")
    sl=line_of(ut,r'^\s+"'+t+r'",')
    if sl: srcs.append(f"libs/combat/util.ts EFFECT_SORT_RANK (line {sl})")
    srcs+=EXTRA_SRC.get(t,[])
    if srcs:
        L.append("source:   # game repo studie-tech/TheNinjaRPG @ 29cd91b, paths under app/src")
        for s_ in srcs: L.append(f"  - {yq(s_)}")
    outs=[e for e in edges if e['s']==t]; ins=[e for e in edges if e['t']==t]
    if outs or ins:
        L.append("interactions:   # full list with notes in ../interactions.json")
        if outs:
            L.append("  outgoing:")
            for kk in sorted(set(e['k'] for e in outs)):
                L.append(f"    {kk}: [{', '.join(e['t'] for e in outs if e['k']==kk)}]")
        if ins:
            L.append("  incoming:")
            for kk in sorted(set(e['k'] for e in ins)):
                L.append(f"    {kk}: [{', '.join(e['s'] for e in ins if e['k']==kk)}]")
    open(f'/tmp/map/kb/tags/{t}.yaml','w').write('\n'.join(L)+'\n')
    index.append((n['area'],t,n['use']))
print(len(index))
