import sys, time
sys.path.insert(0, '.')
from PIL import Image
import ground_hd as G
t=time.time()
A=G.ground_storm_frames(11); B=G.ground_storm_frames(28)
print("built", round(time.time()-t,1), "s")
n=168; h=n/2; w=2*h
k=7  # frame index
tiles=[]
# board offsets for a patch: columns spaced 0.75w, odd columns shifted h/2
W=int(5*0.75*w+w); H=int(4*h+h)
img=Image.new("RGBA",(W,H),(52,64,44,255))
import random
for c in range(5):
    for r in range(4):
        x=c*0.75*w+w/2; y=r*h+h/2+(h/2 if c%2 else 0)
        rnd=random.Random(c*7+r)
        fr=(A if rnd.random()<.5 else B)[k]
        if rnd.random()<.5: fr=fr.transpose(Image.FLIP_LEFT_RIGHT)
        img.alpha_composite(fr,(int(x-n/2),int(y-n/2)))
img.save("/tmp/v13_patch.png"); print(img.size)
z=Image.new("RGBA",(n,n),(52,64,44,255)); z.alpha_composite(A[k]); z.resize((n*3,n*3),Image.LANCZOS).save("/tmp/v13_tile.png")
