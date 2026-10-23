"""Prototype only: derive a cast animation strip from the approved Chakra Overflow icon."""
import numpy as np, math
from PIL import Image, ImageFilter
OUT='/tmp/claude-0/-home-user-tnr-tools/ca560e9e-87f0-5f58-92c7-de44dd0b4bbb/scratchpad/anim/proto/'
src=Image.open('art/jutsu_icons/chakra_overflow/raws/raw_chakra_overflow_v1.png').convert('RGB').resize((512,512),Image.LANCZOS)
a=np.asarray(src).astype(float)/255
L=a.max(axis=2)
bg=np.array([0.02,0.03,0.09])
alpha=np.clip((L-0.10)/0.75,0,1)**0.9
col=np.clip((a-bg*(1-alpha[...,None]))/np.maximum(alpha[...,None],1e-3),0,1)
rgba=np.dstack([col,alpha])
emblem=Image.fromarray((rgba*255).astype('uint8'),'RGBA')
N=24; S=128; frames=[]
rng=np.random.default_rng(7)
sparks=[(rng.uniform(-0.35,0.35),rng.uniform(0.05,0.35),rng.uniform(0.6,1.4),rng.uniform(0,1)) for _ in range(26)]
def ease(t): return 1-(1-t)**3
for i in range(N):
    t=i/(N-1)
    canvas=Image.new('RGBA',(512,512),(0,0,0,0))
    # phase timing
    grow=ease(min(1,t/0.35))                  # 0..0.35 expand
    rise=max(0,(t-0.55)/0.45)                  # 0.55..1 drift up and fade
    fade=1-ease(rise)
    scale=0.35+0.70*grow+0.05*rise
    em=emblem.resize((int(512*scale),int(512*scale)),Image.LANCZOS)
    # wings reveal: vertical mask rising from bottom (sweep upward)
    m=np.asarray(em.split()[3]).astype(float)
    h=m.shape[0]; yy=np.arange(h)[:,None]/h
    reveal=np.clip((1.15-yy-(1-grow)*1.0)/0.25,0,1)
    m=m*reveal*fade
    em.putalpha(Image.fromarray(m.astype('uint8')))
    off=(256-em.width//2, 256-em.height//2-int(30*rise))
    canvas.alpha_composite(em,off)
    # flash at the core early
    flash=math.exp(-((t-0.12)/0.07)**2)
    if flash>0.02:
        f=Image.new('RGBA',(512,512),(0,0,0,0)); fa=np.zeros((512,512))
        yy2,xx2=np.mgrid[0:512,0:512]; d=np.sqrt((xx2-256)**2+(yy2-240)**2)
        fa=np.clip(1-d/(60+140*flash),0,1)**2*flash
        f=Image.fromarray(np.dstack([np.full((512,512),255),np.full((512,512),250),np.full((512,512),220),fa*255]).astype('uint8'),'RGBA')
        canvas.alpha_composite(f)
    # sparks rising (gold/blue)
    sp=np.zeros((512,512,4))
    for k,(x0,y0,spd,ph) in enumerate(sparks):
        life=(t*spd+ph)%1.0
        if t<0.15: continue
        x=256+x0*512; y=300-y0*512-life*220
        al=(1-life)*fade
        c=(255,205,90) if k%2 else (90,140,255)
        Image.Image.paste(canvas, Image.new('RGBA',(6,6),c+(int(255*al),)), (int(x),int(y)), Image.new('L',(6,6),int(255*al)))
    frames.append(canvas.resize((S,S),Image.LANCZOS))
strip=Image.new('RGBA',(S,S*N),(0,0,0,0))
for i,f in enumerate(frames): strip.paste(f,(0,i*S))
strip.save(OUT+'anim_chakra_overflow_proto_strip.webp','WEBP',lossless=True)
# previews: on three battle-like backgrounds, at 128 and 50 px
bgs=[(15,23,42),(110,120,100),(170,190,140)]
gif=[]
for f in frames:
    row=Image.new('RGB',(3*(128+12)+3*(50+12),140),(30,30,34)); x=6
    for b in bgs:
        t=Image.new('RGBA',(128,128),b+(255,)); t.alpha_composite(f); row.paste(t.convert('RGB'),(x,6)); x+=140
    for b in bgs:
        t=Image.new('RGBA',(128,128),b+(255,)); t.alpha_composite(f); row.paste(t.convert('RGB').resize((50,50),Image.LANCZOS),(x,45)); x+=62
    gif.append(row)
gif[0].save(OUT+'anim_chakra_overflow_proto_preview.gif',save_all=True,append_images=gif[1:],duration=50,loop=0)
sheet=Image.new('RGB',(128*12,128*2),(15,23,42))
for i,f in enumerate(frames):
    t=Image.new('RGBA',(128,128),(15,23,42,255)); t.alpha_composite(f); sheet.paste(t.convert('RGB'),((i%12)*128,(i//12)*128))
sheet.save(OUT+'anim_chakra_overflow_proto_frames.png')
print('frames',N,'strip',strip.size)
