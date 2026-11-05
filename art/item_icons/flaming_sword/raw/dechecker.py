import sys
from PIL import Image, ImageFilter
from collections import deque
src,out=sys.argv[1],sys.argv[2]
im=Image.open(src).convert('RGB'); W,H=im.size; px=im.load()
def bg(p):
    r,g,b=p; return max(r,g,b)-min(r,g,b)<=10 and min(r,g,b)>=200
seen=bytearray(W*H); q=deque()
for x in range(W):
    for y in (0,H-1): q.append((x,y))
for y in range(H):
    for x in (0,W-1): q.append((x,y))
while q:
    x,y=q.popleft(); i=y*W+x
    if seen[i] or not bg(px[x,y]): continue
    seen[i]=1
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx,ny=x+dx,y+dy
        if 0<=nx<W and 0<=ny<H and not seen[ny*W+nx]: q.append((nx,ny))
a=Image.frombytes('L',(W,H),bytes(0 if s else 255 for s in seen))
# one-px erode of fringe: remove light neutral pixels adjacent to bg (anti-alias halo)
a=a.filter(ImageFilter.MinFilter(3))
rgba=im.convert('RGBA'); rgba.putalpha(a)
bb=a.getbbox(); print('bbox',bb)
rgba.crop(bb).save(out)
