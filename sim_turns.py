"""TNR turn engine: Endless Night 14-rule profile interpreter + validation vs captured fight.
Semantics per 24_GUIDE + source: rules top-down; threshold sums matching effect powers, >= compare;
distance = hex (odd-q); combo casts both; stances via default rules ignored for action choice."""
import json, sys
sys.path.insert(0,"/home/claude")

KIT_AP={"crown":40,"law":40,"unravel":60,"chains":60,"edict":60,"answers":60,
        "swallow":60,"forever":60,"reach":60,"testament":60}
KIT_CD={"crown":6,"law":6,"unravel":5,"chains":5,"edict":6,"answers":4,
        "swallow":4,"forever":5,"reach":3,"testament":4}
KIT_RANGE={"crown":0,"law":4,"unravel":4,"chains":4,"edict":3,"answers":5,
           "swallow":4,"forever":4,"reach":4,"testament":5}

def axial(x,y):
    r=y-(x-(x&1))/2
    return x,r
def hexdist(a,b):
    q1,r1=axial(*a); q2,r2=axial(*b)
    dq,dr=q1-q2,r1-r2
    return (abs(dq)+abs(dr)+abs(dq+dr))/2

def fx_sum(fx,t):
    return sum(abs(e.get("power") or 0) for e in fx if e["type"]==t)

class Boss:
    def __init__(self):
        self.last={k:-99 for k in KIT_AP}
    def ready(self,k,rnd):
        return rnd-self.last[k]>=KIT_CD[k]
    def turn(self,rnd,dist,player_fx,ap=100):
        """Return list of kit casts this turn per the 14-rule cascade."""
        casts=[]
        def can(k): return self.ready(k,rnd) and KIT_AP[k]<=ap and dist<=KIT_RANGE[k] if KIT_RANGE[k] else self.ready(k,rnd) and KIT_AP[k]<=ap
        while ap>=40:
            pick=None
            idg=fx_sum(player_fx,"increasedamagegiven")
            ddt=fx_sum(player_fx,"decreasedamagetaken")
            ab=fx_sum(player_fx,"absorb")
            sh=fx_sum(player_fx,"shield")
            sl=fx_sum(player_fx,"seal")
            idt=fx_sum(player_fx,"increasedamagetaken")
            if rnd<2 and self.ready("crown",rnd) and ap>=KIT_AP["crown"]: pick=("crown",)
            elif idg>=100 and dist<4 and self.ready("law",rnd) and self.ready("unravel",rnd) and ap>=100: pick=("law","unravel")
            elif ddt>=60 and dist<4 and self.ready("law",rnd) and self.ready("unravel",rnd) and ap>=100: pick=("law","unravel")
            elif ab>=50 and dist<4 and self.ready("law",rnd) and self.ready("unravel",rnd) and ap>=100: pick=("law","unravel")
            elif dist>5 and self.ready("answers",rnd) and ap>=60: pick=("answers",)
            elif sh>=1 and dist<5 and self.ready("testament",rnd) and ap>=60: pick=("testament",)
            elif sl>=1 and dist<4 and self.ready("edict",rnd) and ap>=60: pick=("edict",)
            elif dist<5 and self.ready("chains",rnd) and ap>=60: pick=("chains",)
            elif dist<4 and self.ready("edict",rnd) and ap>=60: pick=("edict",)
            elif idt>=1 and dist<5 and self.ready("forever",rnd) and ap>=60: pick=("forever",)
            elif dist<5 and self.ready("swallow",rnd) and ap>=60: pick=("swallow",)
            elif dist>2: pick=("MOVE",)
            elif dist<5 and self.ready("reach",rnd) and ap>=60: pick=("reach",)
            else: pick=("BASIC",)
            if pick[0]=="MOVE":
                casts.append("MOVE"); ap-=10; dist=max(1,dist-1); continue
            if pick[0]=="BASIC":
                casts.append("BASIC"); break
            for k in pick:
                casts.append(k); ap-=KIT_AP[k]; self.last[k]=rnd
        return casts

NAME2KEY={"Crown of No Dawn":"crown","Law of No Dawn":"law","Unravel the Thread":"unravel",
 "Chains of the Dawnless":"chains","Crownfall Edict":"edict","The Night Answers":"answers",
 "Swallowed Star":"swallow","Forever Dark":"forever","Reach of the Endless":"reach","Night's Testament":"testament"}

if __name__=="__main__":
    ks=json.load(open("ks_fight.json"))
    states={int(k):v for k,v in ks["states"].items()}
    # observed boss kit casts by round
    obs={}
    for r,n in ks["casts"]:
        k=NAME2KEY.get(n)
        if k: obs.setdefault(r,[]).append(k)
    boss=Boss()
    match=0; total=0
    print("round | predicted            | observed")
    for rnd in range(1,13):
        # pre-turn state: earliest state at that round
        cands=sorted(v for v,b in states.items() if b["round"]==rnd)
        b=states[cands[0]] if cands else None
        if not b: continue
        pl=[u for u in b["usersState"] if not u.get("isAi")][0]
        bo=[u for u in b["usersState"] if u.get("isAi")][0]
        d=hexdist((bo["longitude"],bo["latitude"]),(pl["longitude"],pl["latitude"]))
        pfx=[e for e in b.get("usersEffects",[]) if e.get("targetId")==pl["userId"]]
        pred=[c for c in boss.turn(rnd,d,pfx) if c not in ("MOVE","BASIC")]
        o=obs.get(rnd,[])
        ok=set(pred)==set(o)
        match+=ok; total+=1
        print(f"  r{rnd:>2}  | {','.join(pred) or '-':20} | {','.join(o) or '-':20} {'OK' if ok else 'X'}")
    print(f"\nboss-turn reproduction: {match}/{total}")
