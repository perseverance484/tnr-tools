from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np, math
N=512
def grad_fill(mask):
    # blue at the outside, gold, white-hot near the core (core at 0.5,0.52)
    yy,xx=np.mgrid[0:N,0:N]; d=np.sqrt((xx-N*0.5)**2+(yy-N*0.52)**2)/(N*0.42)
    d=np.clip(d,0,1)
    blue=np.array([30,70,230]); gold=np.array([255,190,40]); white=np.array([255,255,240])
    c=np.where(d[...,None]<0.25, white+(gold-white)*(d[...,None]/0.25), gold+(blue-gold)*np.clip((d[...,None]-0.25)/0.55,0,1))
    img=Image.fromarray(c.astype('uint8'))
    bg=Image.new('RGB',(N,N),(4,8,26))
    glow=Image.composite(img,bg,mask.filter(ImageFilter.GaussianBlur(18)))
    glow=ImageChops.blend(bg,glow,0.7)
    out=Image.composite(img,glow,mask)
    core=Image.new('L',(N,N),0); ImageDraw.Draw(core).ellipse([N*0.5-40,N*0.52-40,N*0.5+40,N*0.52+40],fill=255)
    out=Image.composite(Image.new('RGB',(N,N),(255,255,245)),out,core.filter(ImageFilter.GaussianBlur(22)))
    return out
def star4(cx,cy,top,side,bot,w):
    return [(cx,cy-top),(cx+w,cy-w),(cx+side,cy),(cx+w,cy+w),(cx,cy+bot),(cx-w,cy+w),(cx-side,cy),(cx-w,cy-w)]
def save(name,polys):
    m=Image.new('L',(N,N),0); d=ImageDraw.Draw(m)
    for p in polys: d.polygon(p,fill=255)
    grad_fill(m).save(name+'.png')
cx,cy=N*0.5,N*0.52
# A: tall four-point star (sparkle)
save('A_four_point_star',[star4(cx,cy,215,150,120,34)])
# B: double upward chevron with core
def chev(cx,ty,span,h,th):
    return [(cx,ty),(cx+span,ty+h),(cx+span-th*1.2,ty+h+th),(cx,ty+th*1.6),(cx-span+th*1.2,ty+h+th),(cx-span,ty+h)]
save('B_double_chevron',[chev(cx,60,170,140,52),chev(cx,200,170,140,52)])
# C: rising star: four-point star + chevron wings below sweeping up
wingL=[(cx-30,cy+20),(cx-200,cy-70),(cx-175,cy+10),(cx-40,cy+110)]
wingR=[(cx+30,cy+20),(cx+200,cy-70),(cx+175,cy+10),(cx+40,cy+110)]
save('C_rising_star',[star4(cx,cy,220,110,100,30),wingL,wingR])
# D: solid upward arrowhead / spear
save('D_arrowhead',[[(cx,40),(cx+150,cy+40),(cx+60,cy+10),(cx+40,cy+200),(cx-40,cy+200),(cx-60,cy+10),(cx-150,cy+40)]])
print('ok')
