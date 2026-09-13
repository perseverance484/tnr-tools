"""Static SVG inspection at 360px; these are not browser screenshots."""
from pathlib import Path
import cairosvg
from PIL import Image, ImageDraw
root=Path('test-output/fixtures');outdir=Path('docs/review');outdir.mkdir(parents=True,exist_ok=True)
for name in ['aerathiel','night-parade']:
    files=sorted((root/name).glob('*.svg'))
    wanted=[p for p in files if 'build' not in p.name]
    tiles=[]
    for p in wanted:
        dest=p.with_suffix('.png');cairosvg.svg2png(url=str(p),write_to=str(dest),output_width=360)
        im=Image.open(dest);tile=Image.new('RGB',(380,im.height+46),'#f8f3e7');tile.paste(im,(10,26));ImageDraw.Draw(tile).text((10,4),p.stem,fill='black');tiles.append(tile)
    rows=[tiles[i:i+3] for i in range(0,len(tiles),3)];height=sum(max(t.height for t in row) for row in rows)
    out=Image.new('RGB',(1140,height),'#f8f3e7');y=0
    for row in rows:
        for i,t in enumerate(row):out.paste(t,(i*380,y))
        y+=max(t.height for t in row)
    out.save(outdir/(name+'-cards.webp'),quality=90)
