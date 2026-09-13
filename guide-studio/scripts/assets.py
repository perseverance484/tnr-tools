#!/usr/bin/env python3
"""Acquire official CDN images from whitelisted fixture fields, independently of authoring."""
import base64, concurrent.futures, hashlib, io, json, pathlib, urllib.parse, urllib.request
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGET = ROOT / 'public/assets'
ALLOWED = {'ui0arpl8sm.ufs.sh', 'utfs.io', 'uploadthing.b-cdn.net'}
def acquire(pair):
    ident, url = pair
    if urllib.parse.urlsplit(url).hostname not in ALLOWED: raise ValueError('Unapproved asset host')
    path = TARGET / (hashlib.sha256(url.encode()).hexdigest()[:24] + '.webp')
    if path.exists(): return ident, json.loads(path.with_suffix('.json').read_text())
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'TNRGuideStudioCatalog/1.0','Accept':'image/webp,image/png,image/jpeg'}), timeout=30) as response: data = response.read(5_000_001)
    if len(data)>5_000_000: raise ValueError('Image too large')
    im=Image.open(io.BytesIO(data)); im.load(); im.thumbnail((768,768))
    im.save(path,format='WEBP',quality=88,method=6)
    meta={'url': '/assets/'+path.name,'sourceUrl':url,'sourceSha256':hashlib.sha256(data).hexdigest(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'width':im.width,'height':im.height,'mime':'image/webp','bytes':path.stat().st_size,'transform':'Pillow thumbnail <=768px; WebP quality 88'}
    path.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n');return ident,meta
def main():
    refs={}
    def walk(v):
        if isinstance(v,dict):
            if v.get('id') and v.get('image') and v.get('name'): refs[v['id']]=v['image']
            if v.get('userId') and v.get('avatar') and v.get('username'):refs[v['userId']]=v['avatar']
            for x in v.values():walk(x)
        elif isinstance(v,list):
            for x in v:walk(x)
    for p in sorted((ROOT/'fixtures').glob('*.json')):walk(json.loads(p.read_text()))
    TARGET.mkdir(parents=True,exist_ok=True)
    result={}; failures=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs={pool.submit(acquire,pair):pair[0] for pair in sorted(refs.items())}
        for future in concurrent.futures.as_completed(jobs):
            try:
                ident,meta=future.result();result[ident]=meta
            except Exception as error: failures.append((jobs[future],str(error)))
    if failures: raise RuntimeError(str(failures))
    (ROOT/'fixtures/official-assets.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(f'{len(result)} official CDN assets pinned. No TNR API or credential access.')
if __name__=='__main__': main()
