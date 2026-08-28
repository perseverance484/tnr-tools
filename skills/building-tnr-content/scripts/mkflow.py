from PIL import Image, ImageDraw, ImageFont
F="/usr/share/fonts/truetype/dejavu/"
def f(n,s): return ImageFont.truetype(F+n,s)
T=f("DejaVuSerif-Bold.ttf",48); SUB=f("DejaVuSans.ttf",22)
SEC=f("DejaVuSans-Bold.ttf",22); ID=f("DejaVuSansMono.ttf",16)
LBL=f("DejaVuSans.ttf",19); LBLB=f("DejaVuSans-Bold.ttf",19); FT=f("DejaVuSans.ttf",19)
BG=(18,20,24); FG=(233,230,224); MUT=(138,144,152); LINE=(56,61,69)
DLG=(34,38,44); ACT=(186,146,84); BTL=(176,86,86); END=(122,152,168); ARR=(96,104,114)
W=1500
N={}; ORD=[]
def place(nid,label,x,y,w=420,h=54,kind="dialog",tag=None):
    N[nid]=dict(x=x,y=y,w=w,h=h,kind=kind,label=label,tag=tag); ORD.append(nid); return y+h
CX=W//2-160
y=44; TOP=y
y+=118; RULE1=y; y+=30
SEC1=y; y+=36
place("g1","You go looking for a serious job",CX,y); y+=76
place("g2","An old entry, pinned with a fresh brief",CX,y); y+=76
place("g3","Read further: he ran a cell here",CX-400,y,w=340)
place("g4","Where do you begin?",CX,y,kind="hub"); y+=96
SEC2=y; y+=40
COLS=[70,420,770,1120]; SW=320
for (a,b,t,r),x in zip([("g5","g6","Village walls","Fresh mortar, a bored sentry"),
                        ("g7","g8","Market","Four descriptions, one is you"),
                        ("g9","g10","Back alleys","A courier, somebody's laundry"),
                        ("g11","The slums, eastern side","","")],COLS):
    if a=="g11":
        place("g11","The slums, eastern side",x,y,w=SW,h=48,kind="action",tag="ACTION")
        place("g12","How do you work it?",x,y+66,w=SW,h=76,kind="hub")
    else:
        place(a,t,x,y,w=SW,h=48,kind="action",tag="ACTION")
        place(b,r,x,y+66,w=SW,h=76)
y+=66+76+34; RULE2=y; y+=26
SEC3=y; y+=72
VC=[70,560,1050]; CW=390
V=[[("g13","Ask around the district",None),("g14","A circle somebody drew for you","ACTION"),
    ("g15","The fourth one flinched",None),("g16","EAST GATE   1x Old Ghost","BATTLE")],
   [("g18","An old contact from before rank",None),("g19","A warehouse off the cut, tonight",None),
    ("g20","AMBUSH   2x Faceless Shadow","BATTLE"),("g21","This was never his location",None),
    ("g22","What was it keeping you from?","ACTION"),("g23","Lights in the old dye works",None),
    ("g24","DYE WORKS   Ghost + 2 Shadow","BATTLE")],
   [("g25","Wait for the light to go",None),("g26","Three leave a house, no lamps","ACTION"),
    ("g27","The lead stops without turning",None),("g28","THE LANE   2x Faceless Shadow","BATTLE"),
    ("g28_x4","He never looked back once",None),("g29","Over the slope, four roofs","ACTION"),
    ("g29_x6","\"You are the fifth. Or the sixth.\"",None),("g31","THE WALL   1x Old Ghost","BATTLE")]]
for col,x in zip(V,VC):
    yy=y
    for nid,lab,tag in col:
        k="battle" if tag=="BATTLE" else ("action" if tag=="ACTION" else "dialog")
        place(nid,lab,x,yy,w=CW,h=76,kind=k,tag=tag); yy+=88
y+=8*88+16; RULE3=y; BUS=y+22; y+=52
place("g30","You file it that night",CX,y,kind="hub"); y+=80
place("g32","She reads it. Then reads it again.",CX,y); y+=84
place("g33","\"You do not believe me.\"",CX-420,y,w=380); place("g34","Say nothing",CX+420,y,w=380); y+=84
place("g35","ENDING   \"He taught me to be sure.\"",CX-420,y,w=420,kind="end")
place("g36","ENDING   The entry stays open",CX+420,y,w=420,kind="end")
y+=76; RULE4=y; H=y+80
im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
def head(a): return (N[a]['x']+N[a]['w']//2, N[a]['y'])
def foot(a): return (N[a]['x']+N[a]['w']//2, N[a]['y']+N[a]['h'])
def tip(p,c=ARR): d.polygon([(p[0],p[1]),(p[0]-6,p[1]-9),(p[0]+6,p[1]-9)],fill=c)
def elbow(a,b,c=ARR):
    sx,sy=foot(a); ex,ey=head(b)
    if abs(sx-ex)<4: d.line([(sx,sy),(ex,ey-4)],fill=c,width=2)
    else:
        my=sy+(ey-sy)//2
        d.line([(sx,sy),(sx,my)],fill=c,width=2); d.line([(sx,my),(ex,my)],fill=c,width=2)
        d.line([(ex,my),(ex,ey-4)],fill=c,width=2)
    tip((ex,ey),c)
for a,b in [("g1","g2"),("g2","g3"),("g2","g4"),("g3","g4"),
            ("g4","g5"),("g4","g7"),("g4","g9"),("g4","g11"),
            ("g5","g6"),("g7","g8"),("g9","g10"),("g11","g12"),
            ("g12","g13"),("g12","g18"),("g12","g25"),
            ("g30","g32"),("g32","g33"),("g32","g34"),
            ("g33","g35"),("g33","g36"),("g34","g35"),("g34","g36")]: elbow(a,b)
for col in V:
    for i in range(len(col)-1): elbow(col[i][0],col[i+1][0])
for b in ["g16","g24","g31"]:
    sx,sy=foot(b); ex,ey=head("g30")
    d.line([(sx,sy),(sx,BUS)],fill=ARR,width=2); d.line([(sx,BUS),(ex,BUS)],fill=ARR,width=2)
d.line([(N['g30']['x']+N['g30']['w']//2,BUS),(N['g30']['x']+N['g30']['w']//2,N['g30']['y']-4)],fill=ARR,width=2)
tip(head("g30"))
LOOP=(150,108,108)
MARK={"g6":"back to g4","g8":"back to g4","g10":"back to g4",
      "g16":"lose: to g12","g20":"lose: to g12","g24":"lose: to g12",
      "g28":"lose: to g12","g31":"lose: to g12"}
for nid in ORD:
    n=N[nid]; x,yy,w,h,k=n['x'],n['y'],n['w'],n['h'],n['kind']
    col={"dialog":DLG,"action":DLG,"battle":(46,26,28),"end":(24,34,40),"hub":(30,36,44)}[k]
    edge={"dialog":LINE,"action":ACT,"battle":BTL,"end":END,"hub":(96,116,136)}[k]
    d.rounded_rectangle([x,yy,x+w,yy+h],8,fill=col,outline=edge,width=2 if k in("battle","hub","end") else 1)
    d.text((x+12,yy+6),nid,font=ID,fill=MUT)
    fo=LBLB if k in("battle","hub","end") else LBL
    fill={"battle":(236,172,172),"end":(180,208,224),"hub":FG}.get(k,FG)
    d.text((x+12,yy+25),n['label'],font=fo,fill=fill)
    if n['tag']: d.text((x+w-12-d.textlength(n['tag'],font=ID),yy+8),n['tag'],font=ID,fill=ACT if k=="action" else (200,140,140))
    if nid in MARK:
        mw=d.textlength(MARK[nid],font=ID); d.text((x+w-12-mw,yy+h-24),MARK[nid],font=ID,fill=LOOP)
    lw=d.textlength(n['label'],font=fo)
    avail=w-24
    if lw>avail: print("OVERFLOW",nid,int(lw),">",int(avail))
d.text((60,TOP),"OLD GHOST",font=T,fill=FG)
d.text((60,TOP+62),"A rank  ·  42 nodes  ·  5 battles  ·  2 endings",font=SUB,fill=MUT)
for r in (RULE1,RULE2,RULE3,RULE4): d.line([(60,r),(W-60,r)],fill=LINE,width=2)
def hdr(x,yy,txt,fo,fill):
    wdt=d.textlength(txt,font=fo); d.rectangle([x-8,yy-6,x+wdt+10,yy+30],fill=BG); d.text((x,yy),txt,font=fo,fill=fill)
hdr(60,SEC1,"THE BOARD",SEC,ACT)
hdr(60,SEC2,"SEARCH THE VILLAGE",SEC,ACT)
hdr(330,SEC2+3,"three of the four lead nowhere and loop back",LBL,MUT)
hdr(60,SEC3,"THREE VECTORS",SEC,ACT)
hdr(262,SEC3+3,"different lengths, different fights, every loss returns to the slums",LBL,MUT)
for h_,x in zip(["ASK AROUND","AN OLD CONTACT","WATCH AT DUSK"],VC): hdr(x+4,SEC3+34,h_,ID,MUT)
d.text((60,RULE4+22),"Three routes to the same man. Win on any of them and the report is identical.",font=FT,fill=MUT)
im.save("/mnt/user-data/outputs/oldghost_flow.png"); print("ok",H)
