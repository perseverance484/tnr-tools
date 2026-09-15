#!/usr/bin/env python3
"""Archive captured Godstorm image URLs. Never calls the game API or writes Git.

Reads two immutable, hash-checked Git blobs; extracts the retained population;
GETs allowlisted /f/ image URLs only; preserves original hosted bytes; writes a
provenance index, offline gallery and ZIP. Default avatars remain explicit gaps.
Requires Pillow. A download is not artwork approval or proof of capture-time bytes.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib import error, parse, request
import warnings
import zipfile
from PIL import Image

REPO = 'perseverance484/tnr-tools'
BASE = '6e09b15bb6f3d1c90ba416d14211b533f5b4a367'
SOURCES = (
    ('harvests/inbox/tnr_results_1789401726302.json',
     '4faa45084b7b921cc3ef03240a561566943c4e53',
     'push/23_godstorm_tower_root_capture.json', {'quests.get': 3}),
    ('harvests/inbox/tnr_results_1789402842027.json',
     '86524d9f248b3731894826c064279ecef089d956',
     'push/24_godstorm_tower_related_capture.json',
     {'profile.getAi': 23, 'item.get': 3, 'gameAsset.get': 4}),
)
QUEST_NAMES = (
    'The Tower of Endless Night: The Marrow Vaults',
    'The Tower of Endless Night: The Stormcourt',
)
HOSTS = frozenset(('ui0arpl8sm.ufs.sh', 'uploadthing.b-cdn.net'))
MAX_BYTES = 8 * 1024 * 1024
MAX_TOTAL = 80 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 20_000_000
warnings.simplefilter('error', Image.DecompressionBombWarning)
EXT = {'PNG': '.png', 'WEBP': '.webp', 'JPEG': '.jpg', 'GIF': '.gif'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def utc():
    return datetime.now(timezone.utc).isoformat()


def git_blob_hash(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def checked_source(data, expected_sha, manifest, procedures):
    require(git_blob_hash(data) == expected_sha, 'capture blob hash mismatch')
    obj = json.loads(data)
    require(obj.get('state') == 'DONE' and obj.get('outcome') == 'success',
            'capture run not successful')
    require(obj.get('entries') == [], 'mutation entries present or absent evidence')
    journal = obj.get('journal', {})
    require(journal.get('items') == [] and journal.get('manifestPath') == manifest,
            'journal mutation/manifest mismatch')
    caps = obj.get('captures')
    require(isinstance(caps, list), 'missing captures')
    require(Counter(c.get('proc') for c in caps) == Counter(procedures),
            'capture procedure population mismatch')
    for c in caps:
        require(c.get('ok') is True and c.get('persistOk') is True
                and c.get('persist') == 'full' and c.get('error') is None,
                'failed or unpersisted capture')
        require(isinstance(c.get('snapshotKey'), str), 'missing snapshot key')
    return obj


def inventory(roots, related):
    """Extract IDs/URLs from whole records, not transcribed tool snippets."""
    records, opponents, referenced_bgs = [], {}, set()
    def add(c, i, source_i, category, field, ident, name, consumers):
        value = c['data'].get(field)
        state = ('missing' if not value else
                 'default' if '_default.' in parse.urlsplit(value).path else 'assigned')
        records.append(dict(category=category, entity_id=ident, name=name,
                            source_field=field, source_url=value, state=state,
                            consumers=consumers, capture_path=SOURCES[source_i][0],
                            json_pointer=f'/captures/{i}/data/{field}',
                            snapshot_key=c['snapshotKey'], captured_at=c.get('at')))
    for name in QUEST_NAMES:
        found = [(i, c) for i, c in enumerate(roots['captures'])
                 if c.get('proc') == 'quests.get' and isinstance(c.get('data'), dict)
                 and c['data'].get('name') == name]
        require(len(found) == 1, 'retained quest selection is not unique: ' + name)
        i, c = found[0]
        q = c['data']; qid = q['id']
        require(c['input'].get('id') == qid, 'quest input/data identity mismatch')
        require(q.get('questType') == 'battlepyramid', 'wrong quest type')
        add(c, i, 0, 'quest_listing', 'image', qid, name, [qid])
        battles = [o for o in q['content']['objectives'] if o['task'] == 'start_battle']
        require(len(battles) == 25, 'expected 25 battles per retained quest')
        for o in q['content']['objectives']:
            if o.get('sceneBackground'):
                referenced_bgs.add(o['sceneBackground'])
        if q['content'].get('sceneBackground'):
            referenced_bgs.add(q['content']['sceneBackground'])
        for battle in battles:
            for group in battle['opponentAIs']:
                for aid in group['ids']:
                    opponents.setdefault(aid, []).append({'quest_id': qid,
                                                         'objective_id': battle['id']})
    require(len(opponents) == 18, 'retained AI population differs from 18')
    ai_rows = {}
    for i, c in enumerate(related['captures']):
        if c['proc'] == 'profile.getAi':
            aid = c['data']['userId']
            require(aid not in ai_rows, 'duplicate captured AI')
            require(c['input'].get('userId') == aid, 'AI input/data identity mismatch')
            ai_rows[aid] = (i, c)
    for aid in sorted(opponents):
        require(aid in ai_rows, 'unresolved retained AI: ' + aid)
        i, c = ai_rows[aid]
        add(c, i, 1, 'ai_avatar', 'avatar', aid, c['data']['username'], opponents[aid])
    bgs = set()
    for i, c in enumerate(related['captures']):
        if c['proc'] == 'gameAsset.get':
            asset = c['data']; aid = asset['id']
            require(asset['type'] == 'SCENE_BACKGROUND', 'unexpected candidate asset type')
            require(aid not in bgs and c['input'].get('id') == aid, 'asset identity mismatch')
            require(aid in referenced_bgs or asset['name'] == 'StormCourtyard',
                    'background outside approved direct/candidate scope')
            bgs.add(aid)
            add(c, i, 1, 'scene_background', 'image', aid, asset['name'],
                ['captured_reference' if aid in referenced_bgs else 'unwired_candidate'])
    require(referenced_bgs <= bgs and len(bgs) == 4, 'background closure differs')
    require(len(records) == 24, 'expected 2 listings + 18 avatars + 4 backgrounds')
    avatar_states = Counter(r['state'] for r in records if r['category'] == 'ai_avatar')
    require(avatar_states == {'assigned': 13, 'default': 5}, 'avatar census changed')
    return records


def validate_url(url):
    p = parse.urlsplit(url)
    require(p.scheme == 'https' and p.hostname in HOSTS and p.port in (None, 443),
            'URL outside exact HTTPS host allowlist')
    require(not p.username and not p.password and not p.query and not p.fragment,
            'credentials/query/fragment not allowed')
    require(re.fullmatch(r'/f/[A-Za-z0-9_-]+(?:\.[A-Za-z0-9]+)?', p.path) is not None,
            'not an allowed image-file path')
    return url


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('redirect refused; review destination before expanding scope')


def download(url):
    validate_url(url)
    opener = request.build_opener(request.ProxyHandler({}), NoRedirect())
    req = request.Request(url, headers={
        'User-Agent': 'tnr-tools/godstorm-source-art-pack (capture-backed archive)',
        'Accept': 'image/*', 'Accept-Encoding': 'identity'}, method='GET')
    with opener.open(req, timeout=20) as response:
        require(response.status == 200, 'image request did not return 200')
        length = response.headers.get('Content-Length')
        require(length is None or int(length) <= MAX_BYTES, 'image byte limit exceeded')
        blob = response.read(MAX_BYTES + 1)
        require(0 < len(blob) <= MAX_BYTES, 'empty or oversized image')
        return blob, {'http_status': response.status, 'content_type': response.headers.get('Content-Type'),
                      'final_url': response.geturl(), 'downloaded_at': utc()}


def image_info(blob):
    require(len(blob) <= MAX_BYTES, 'image byte limit exceeded')
    with Image.open(io.BytesIO(blob)) as im:
        require(im.format in EXT, 'unsupported image format')
        fmt, size, frames = im.format, im.size, getattr(im, 'n_frames', 1)
        require(frames == 1, 'animated file outside this still-image pack')
        im.verify()
    with Image.open(io.BytesIO(blob)) as im:
        im.load()
    return {'format': fmt, 'width': size[0], 'height': size[1], 'bytes': len(blob),
            'sha256': hashlib.sha256(blob).hexdigest()}


def save_results(out, records, sources, assets, failures):
    obj = dict(schema='tnr.godstorm_source_art.v1', repository=REPO, capture_ref=BASE,
               created_at=utc(), status='partial' if failures else 'downloaded_unreviewed',
               caveat='Hosted bytes retrieved now; not proof of capture-time bytes or generation masters. No art approval.',
               sources=sources, inventory=records, assets=assets, failures=failures,
               counts={'inventory': len(records), 'assigned': sum(r['state']=='assigned' for r in records),
                       'defaults': sum(r['state']=='default' for r in records),
                       'files': len(assets), 'failed_urls': len(failures)},
               out_of_scope=['fresh game reads', 'scene portrait creation', 'jutsu/VFX closure',
                             'reward changes', 'game uploads', 'global style-reference corpus'])
    (out/'index.json').write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
    blocks = ['<!doctype html><meta charset="utf-8"><title>Godstorm source art</title>',
              '<style>body{font:16px system-ui;max-width:1100px;margin:2em auto;padding:1em} '
              'img{max-width:100%;max-height:560px} figure{margin:2em 0;border-top:1px solid;padding:1em 0}'
              '</style><h1>Godstorm source art</h1><p>Captured references; hosted originals retrieved now. '
              'Unreviewed artwork. Images load locally, without network access.</p>']
    for a in assets:
        labels = [records[i]['name'] for i in a['inventory_indices']]
        blocks.append('<figure><h2>'+html.escape(' / '.join(labels))+'</h2><img src="'+
                      html.escape(a['file'], quote=True)+'" alt="'+html.escape(labels[0],quote=True)+
                      '"><figcaption>'+str(a['width'])+' × '+str(a['height'])+'; '+str(a['bytes'])+
                      ' bytes; SHA-256 '+a['sha256']+'</figcaption></figure>')
    for r in records:
        if r['state'] != 'assigned':
            blocks.append('<p>'+html.escape(r['name']+': '+r['state'])+'</p>')
    for f in failures:
        blocks.append('<p>DOWNLOAD FAILED: '+html.escape(f['source_url']+' — '+f['error'])+'</p>')
    (out/'gallery.html').write_text('\n'.join(blocks), encoding='utf-8')
    return obj


def collect(records, out, sources, fetch=download):
    require(not out.exists(), 'output already exists; use a fresh directory to avoid stale-file ambiguity')
    out.mkdir(parents=True); (out/'originals').mkdir()
    urls = {}
    for i, r in enumerate(records):
        if r['state'] == 'assigned':
            validate_url(r['source_url'])
            urls.setdefault(r['source_url'], []).append(i)
    assets, failures, total = [], [], 0
    for url, uses in urls.items():
        try:
            blob, transfer = fetch(url)
            meta = image_info(blob)
            require(total + len(blob) <= MAX_TOTAL, 'pack byte ceiling exceeded')
            total += len(blob)
            first = records[uses[0]]
            slug = re.sub(r'[^a-z0-9]+', '_', first['name'].lower()).strip('_')[:64]
            file = 'originals/' + first['category']+'_'+slug+'_'+meta['sha256'][:16]+EXT[meta['format']]
            (out/file).write_bytes(blob)
            assets.append(dict(file=file, source_url=url, inventory_indices=uses, **meta, **transfer))
        except Exception as exc:
            failures.append({'source_url': url, 'inventory_indices': uses,
                             'error': type(exc).__name__+': '+str(exc)[:350]})
        save_results(out, records, sources, assets, failures)
        if fetch is download:
            time.sleep(0.25)
    result = save_results(out, records, sources, assets, failures)
    with zipfile.ZipFile(out.with_suffix('.zip'), 'x', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file():
                z.write(p, p.relative_to(out))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path('.'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    sources, loaded = [], []
    for path, sha, manifest, procs in SOURCES:
        blob = subprocess.run(['git','-C',str(args.repo_root),'show',BASE+':'+path],
                              check=True, capture_output=True).stdout
        obj = checked_source(blob, sha, manifest, procs)
        loaded.append(obj)
        sources.append({'path':path,'git_blob_sha':sha,'sha256':hashlib.sha256(blob).hexdigest(),
                        'captured_at':obj['at'],'manifest':manifest})
    result = collect(inventory(*loaded), args.out, sources)
    print(json.dumps({'status':result['status'],'counts':result['counts']}, indent=2))
    return 1 if result['failures'] else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('FAILED: '+str(exc), file=sys.stderr)
        sys.exit(2)
