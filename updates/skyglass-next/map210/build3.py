import json, random, math
W=H=26
OCEAN,GROUND,SAND,ICE,SANDBLK=1,2,3,4,5
v4=json.load(open('v4_terrain_full.json'))
grid=[[v4[r*W+c] for c in range(W)] for r in range(H)]   # row 0 = south
FADED=(7,1); SKY=(21,6); SHRINE=(13,5); SPAWN=(13,7)
def nbrs(c,r):
    d=[(1,0),(-1,0),(0,-1),(0,1),(1,-1),(-1,-1)] if c%2==0 else [(1,0),(-1,0),(0,-1),(0,1),(1,1),(-1,1)]
    return [(c+a,r+b) for a,b in d if 0<=c+a<W and 0<=r+b<H]
def setsand(c,r):
    if grid[r][c]==OCEAN: grid[r][c]=SAND
# 1. ragged beach along the south edge (west of the ground triangle): depth per column
depth=[1,2,2,1,2,3,3,3,3,2,2,1,2,3]   # cols 0..13, deepest under the Faded wreck (7,1)
for c,dp in enumerate(depth):
    for r in range(dp+1): setsand(c,r)
# 2. sand spit from the shore up to the shrine's island (13,5): leave (13,5) as is
for c,r in [(12,3),(13,3),(13,4),(12,4),(14,4),(14,3)]: setsand(c,r)
# 3. widen the triangle's sandy edge by one ragged hex outward
edge=[(c,r) for r in range(H) for c in range(W) if grid[r][c]==OCEAN and any(grid[b][a] in (GROUND,SAND) for a,b in nbrs(c,r)) and 14<=c<=25 and r<=9]
rnd=random.Random(2100)
for c,r in edge:
    if rnd.random()<0.6 or abs(c-SKY[0])+abs(r-SKY[1])<=3: setsand(c,r)
# sand pocket around the Skyglass Wreck entrance
for a,b in nbrs(*SKY)+[SKY]: setsand(a,b)
for a,b in nbrs(*FADED)+[FADED]: setsand(a,b)
# 4. blocked sand under the big pieces of wreckage (all on the beach, none near an entrance)
HULL=(2,1); MASTA=(10,1); MASTB=(16,4)
for c,r in (HULL,MASTA,MASTB): grid[r][c]=SANDBLK
# ragged forest edge: some back-beach hexes become forest floor so the treeline isn't a ruler line
fr=random.Random(282); NEWTREES=[]
keepclear={FADED,(7,0),(6,1),(8,1),(6,0),(8,0),HULL,MASTA}
for c in range(12,14):
    for r in (0,1):
        if grid[r][c]!=SAND or (c,r) in keepclear: continue
        if r==1 and grid[0][c]!=GROUND: continue
        if fr.random()<(0.6 if r==0 else 0.35):
            grid[r][c]=GROUND; NEWTREES.append((c,r))
def walk(c,r): return grid[r][c]!=SANDBLK
for e in (FADED,SKY,SHRINE,SPAWN): assert walk(*e) and all(walk(*n) for n in nbrs(*e)), e

objs=[]; nid=[100]; occ=set()
def deco(key,c,r,scale,ox=0.0,oy=0.0):
    nid[0]+=1; occ.add((c,r))
    p=[{"name":"assetKey","value":key},{"name":"scale","value":round(scale,2)}]
    if abs(ox)>0.005: p.append({"name":"offsetX","value":round(ox,2)})
    if abs(oy)>0.005: p.append({"name":"offsetY","value":round(oy,2)})
    objs.append({"id":nid[0],"type":"decoration","x":c*48+32,"y":r*56+(28 if c%2 else 0)+28,"properties":p})
kept=cut=0
for line in open('v4_decos.txt'):
    i,c,r,k,s,ox=line.split(); c=int(c); r=int(r)
    if grid[r][c]==GROUND: deco(k,c,r,float(s),float(ox)); kept+=1
    else: cut+=1
for c,r in NEWTREES:
    deco(fr.choice(['tree.green.round','tree.green.tall','tree.green.tall','tree.green.wide']),c,r,fr.uniform(1.7,2.2),fr.uniform(-0.15,0.15))
    if fr.random()<0.5: deco(fr.choice(['grass.tuft','grass.sprout']),c,r,fr.uniform(0.9,1.05),fr.uniform(-0.3,0.3),fr.uniform(-0.2,0.2))
K='wreck.skyglass.'
# big wreckage, about half a wreck
deco(K+'hull',*HULL,4.6,0.05,0.1)
deco(K+'mast',*MASTA,4.0,0.0,0.1)
deco(K+'mast',*MASTB,3.6,0.05,0.1)
# lone landmarks
deco(K+'figurehead',4,2,2.4,0.1,0.1)
deco(K+'anchor',18,4,1.8,-0.1,0.05)
# salvager camp at the foot of the shrine island
deco(K+'cargo',12,4,1.5,-0.2,0.1)
deco(K+'cargo',12,4,1.2,0.25,-0.2)
deco(K+'anchor',14,4,1.6,0.15,0.05)
deco(K+'cargo',14,3,1.3,-0.1,0.0)
# lanterns: shrine -> down the spit -> west to the Faded wreck, east along the shore to the Skyglass wreck
for c,r,ox in [(13,3,-0.3),(12,2,-0.2),(10,2,0.1),(8,2,0.2)]: deco(K+'lantern',c,r,1.15,ox,0.2)
for c,r,ox in [(15,3,0.2),(17,4,0.0),(19,5,-0.1),(20,5,0.3)]: deco(K+'lantern',c,r,1.15,ox,0.2)
# debris: clustered round the wrecks, sparse along the tideline, none in rows
def wd(c,r): return min(math.hypot(c-FADED[0],r-FADED[1]),math.hypot(c-SKY[0],r-SKY[1]),math.hypot(c-HULL[0],r-HULL[1]))
def tideline(c,r): return any(grid[b][a]==OCEAN for a,b in nbrs(c,r))
nd=0
for r in range(H):
    for c in range(W):
        if grid[r][c]!=SAND or (c,r) in (FADED,SKY): continue
        d=wd(c,r); t=tideline(c,r)
        p=(0.55 if d<=1.5 else 0.35 if d<=3 else 0.1)*(1.3 if t else 0.6)
        n=0
        while rnd.random()<p and n<2:
            k=rnd.choices(['planks','kelp','cargo'],[5,4,1 if d<=3 else 0])[0]
            if not t and k=='kelp': k='planks'
            sc={'planks':rnd.uniform(1.1,1.4),'kelp':rnd.uniform(1.0,1.3),'cargo':rnd.uniform(1.1,1.3)}[k]
            deco(K+k,c,r,sc,rnd.uniform(-0.4,0.4),rnd.uniform(-0.35,0.35)); nd+=1; n+=1; p*=0.5

# dark beach rocks (stock rock.slate draws as the desert slate on sand) around the wrecks and the waterline
for c,r,sc,ox,oy in [(6,1,2.6,-0.35,0.25),(8,2,2.2,0.3,-0.1),(9,0,2.0,0.2,0.2),(3,2,2.4,-0.3,0.1),(1,1,2.8,0.2,-0.25),
                     (20,7,2.4,-0.2,0.1),(22,6,2.6,0.35,0.2),(19,6,2.0,0.1,-0.2),(23,7,2.2,0.0,0.1),(11,3,2.0,0.3,0.2),(15,4,2.2,-0.3,0.2)]:
    if grid[r][c] in (SAND,) and (c,r) not in (FADED,SKY): deco('rock.slate',c,r,sc,ox,oy)
for c,r,sc,ox,oy in [(5,0,2.2,0.2,0.2),(0,1,2.0,0.1,0.0),(9,2,1.8,-0.3,0.25),(17,5,1.8,0.3,0.1)]:
    if grid[r][c]==SAND: deco('rock.grey',c,r,sc,ox,oy)
# dune grass along the back of the sandbar (draws as dry grass on sand)
for c in range(0,12):
    if grid[0][c]==SAND and rnd.random()<0.8: deco(rnd.choice(['grass.tuft','grass.sprout']),c,0,1.0,rnd.uniform(-0.3,0.3),rnd.uniform(-0.3,0.0))

# flotsam washing in: a few pieces on the shallow water in front of the beach, and one sunken mast offshore
if grid[6][9]==OCEAN: deco(K+'mast',9,6,3.0,0.1,0.0)
anchors=[
 {"x":656,"y":448,"id":1,"name":"spawn.default","type":"anchor","point":True,"properties":[{"name":"gridX","type":"int","value":13},{"name":"gridY","type":"int","value":7}]},
 {"x":656,"y":336,"id":2,"name":"shrine.default","type":"anchor","point":True,"properties":[{"name":"gridX","type":"int","value":13},{"name":"gridY","type":"int","value":5}]},
 {"x":656,"y":56,"id":3,"name":"exit.north","type":"anchor","point":True,"properties":[{"name":"gridX","type":"int","value":13},{"name":"gridY","type":"int","value":0}]},
 {"x":656,"y":1456,"id":4,"name":"exit.south","type":"anchor","point":True,"properties":[{"name":"gridX","type":"int","value":13},{"name":"gridY","type":"int","value":25}]},
 {"x":32,"y":756,"id":5,"name":"exit.west","type":"anchor","point":True,"properties":[{"name":"gridX","type":"int","value":0},{"name":"gridY","type":"int","value":13}]},
 {"x":1232,"y":784,"id":6,"name":"exit.east","type":"anchor","point":True,"properties":[{"name":"gridX","type":"int","value":25},{"name":"gridY","type":"int","value":13}]}]
def tile(id,t,blocked=False,biome=None):
    p=[{"name":"terrain","type":"string","value":t},{"name":"zone","type":"string","value":"wilderness"},{"name":"blocked","type":"bool","value":blocked},{"name":"walkCost","type":"float","value":1},{"name":"battleBiome","type":"string","value":biome or {"ocean":"ocean","ice":"ice"}.get(t,"ground")}]
    return {"id":id,"type":t,"properties":p}
tm={"type":"map","version":"1.10","orientation":"hexagonal","renderorder":"right-down","staggeraxis":"x","staggerindex":"odd","hexsidelength":32,
    "infinite":False,"width":W,"height":H,"tilewidth":64,"tileheight":56,
    "tilesets":[{"name":"terrain","firstgid":1,"tilewidth":64,"tileheight":56,"tilecount":5,"columns":0,"margin":0,"spacing":0,
        "tiles":[tile(0,"ocean"),tile(1,"ground"),tile(2,"dessert",biome="dessert"),tile(3,"ice"),tile(4,"dessert",True,biome="dessert")]}],
    "layers":[{"name":"terrain","type":"tilelayer","data":[grid[r][c] for r in range(H) for c in range(W)]},
              {"name":"objects","type":"objectgroup","objects":anchors+objs}]}
json.dump(tm,open('map210_beach_v7.json','w'),separators=(',',':'))
print('kept',kept,'cut',cut,'debris',nd,'objects',len(objs))
sym={1:'~',2:'G',3:'s',4:'I',5:'X'}
print('   '+''.join(str(c%10) for c in range(26)))
for r in range(10,-1,-1): print(f'{r:2d} '+''.join(sym[v] for v in grid[r]))
