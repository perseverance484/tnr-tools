from PIL import Image, ImageDraw, ImageFont
F="/usr/share/fonts/truetype/dejavu/"
def f(n,s): return ImageFont.truetype(F+n,s)
T=f("DejaVuSerif-Bold.ttf",54); SUB=f("DejaVuSans.ttf",23)
RK=f("DejaVuSans-Bold.ttf",27); NM=f("DejaVuSans-Bold.ttf",31)
PR=f("DejaVuSans.ttf",23); ST=f("DejaVuSansMono.ttf",21)
LB=f("DejaVuSans-Bold.ttf",24); LS=f("DejaVuSans.ttf",21); FT=f("DejaVuSans.ttf",21)
BG=(18,20,24); FG=(233,230,224); MUT=(138,144,152); LINE=(46,50,57)
ACC={"C":(122,152,168),"B":(186,146,84),"A":(176,86,86)}
W=1200; im=Image.new("RGB",(W,2200),BG); d=ImageDraw.Draw(im)
def wrap(t,fo,mw):
    out=[];cur=""
    for w in t.split():
        c=(cur+" "+w).strip()
        if d.textlength(c,font=fo)<=mw: cur=c
        else: out.append(cur); cur=w
    if cur: out.append(cur); return out
M=[("C","Chalk and Corner","Survey four chalk-marked boundary stones and record what is on them.",14,1,2),
   ("C","The Empty Contract","A dead courier's contract names a place, a night and a price, but never the job.",15,2,1),
   ("C","The Waystation","Escort an old keeper up the pass road to reopen her waystation. The posting says bandits.",17,3,2),
   ("C","Protection","A merchant has paid someone for two years and never been given a name. Stand three nights at his yard.",17,1,3),
   ("B","The Loud Way","Eleven crates signed into a bonded warehouse in four months and never signed out.",29,4,2),
   ("B","Nothing to Report","Walk one clerk and two years of ledgers to the audit before dawn.",25,2,2),
   ("A","Three Rounds","A four-person squad watching a handover has missed two signal windows.",45,4,2),
   ("A","The Long Winter","Three of five signatures on one wartime authorisation have died in nine days. Protect the fifth.",35,3,3),
   ("A","Old Ghost","A name out of the old bounty listings resurfaces after years in hiding.",42,5,2),
   ("A","The Tenth Name","A page off a body lists ten targets. Nine are ours, copied in a hand that is not.",33,3,3)]
y=54
d.text((60,y),"THE FORSWORN",font=T,fill=FG); y+=68
d.text((62,y),"Wave 1  ·  status 28 Aug 2026",font=SUB,fill=MUT); y+=52
d.line([(60,y),(W-60,y)],fill=LINE,width=2); y+=30
for lab,val in [("MISSIONS","10"),("NODES","272"),("BATTLES","28"),("ENDINGS","22"),("ENEMIES","9")]:
    pass
x=60
for lab,val in [("MISSIONS","10"),("NODES","272"),("BATTLES","28"),("ENDINGS","22"),("ENEMIES","9")]:
    d.text((x,y),val,font=f("DejaVuSans-Bold.ttf",40),fill=FG)
    d.text((x,y+48),lab,font=f("DejaVuSans.ttf",18),fill=MUT); x+=224
y+=100
d.line([(60,y),(W-60,y)],fill=LINE,width=2); y+=34
cur=None
for rk,name,prem,n,b,e in M:
    if rk!=cur:
        cur=rk
        cnt=sum(1 for m in M if m[0]==rk)
        d.rectangle([60,y,66,y+30],fill=ACC[rk])
        d.text((82,y+2),f"{rk} RANK",font=RK,fill=ACC[rk])
        d.text((208,y+6),f"{cnt} missions",font=LS,fill=MUT); y+=48
    d.text((82,y),name,font=NM,fill=FG)
    chip=f"{n:>3} nodes   {b} fights   {e} endings"
    d.text((W-60-d.textlength(chip,font=ST),y+6),chip,font=ST,fill=MUT); y+=38
    for ln in wrap(prem,PR,820):
        d.text((82,y),ln,font=PR,fill=(176,180,188)); y+=30
    y+=20
y+=6; d.line([(60,y),(W-60,y)],fill=LINE,width=2); y+=32
d.text((60,y),"THE LADDER",font=LB,fill=FG)
d.text((242,y+3),"nine rungs, and the tier is what they lost",font=LS,fill=MUT); y+=44
for tier,col,rows in [("UNMARKED",(150,156,164),"Stray 25   ·   Blade 30   ·   Shadow 35"),
                      ("FACELESS",ACC["B"],"Stray 40   ·   Blade 50   ·   Shadow 55"),
                      ("NAMED",ACC["A"],"Pale Fang 70   ·   Winter Crow 80   ·   Old Ghost 85")]:
    d.rectangle([60,y+4,66,y+26],fill=col)
    d.text((82,y),tier,font=LB,fill=col)
    d.text((272,y+2),rows,font=LS,fill=(176,180,188)); y+=40
y+=14; d.line([(60,y),(W-60,y)],fill=LINE,width=2); y+=26
d.text((60,y),"Built and validating clean · all content hidden · nothing pushed",font=FT,fill=MUT); y+=30
d.text((60,y),"World and prose pass: 8 of 10 complete · Art: not started",font=FT,fill=MUT); y+=44
im.crop((0,0,W,y)).save("/mnt/user-data/outputs/forsworn_status.png")
print("saved",y)
