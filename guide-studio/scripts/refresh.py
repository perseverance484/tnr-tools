#!/usr/bin/env python3
"""Operator-run read-only snapshot refresh. Never shipped in the public bundle.
No auth, environment credentials, cookie jars, redirects, or mutation procedures.
"""
import argparse, datetime, json, pathlib, urllib.parse, urllib.request

ORIGIN = 'https://www.theninja-rpg.com'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Catalog refresh refuses redirects')

def query(proc, data):
    if proc not in {'bloodline.get', 'jutsu.getAll'}:
        raise ValueError('Not a catalog read')
    encoded = urllib.parse.quote(json.dumps({'0': {'json': data}}, separators=(',', ':')))
    req = urllib.request.Request(f'{ORIGIN}/api/trpc/{proc}?batch=1&input={encoded}', headers={'Accept': 'application/json'}, method='GET')
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=30) as response:
        body = response.read(8_000_001)
    if len(body) > 8_000_000: raise ValueError('Response limit exceeded')
    return json.loads(body)[0]['result']['data']['json']

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--bloodline', action='append', required=True)
    args = parser.parse_args()
    path = pathlib.Path(args.output)
    if path.exists(): raise ValueError('Snapshots are immutable; choose a new filename')
    captures = []
    for ident in args.bloodline:
        for proc, data in [('bloodline.get', {'id': ident}), ('jutsu.getAll', {'bloodline': ident, 'limit': 1000, 'hidden': False})]:
            result = query(proc, data)
            if proc == 'jutsu.getAll' and result.get('nextCursor') is not None:
                raise ValueError('Incomplete catalog page; refusing snapshot')
            captures.append({'proc': proc, 'input': data, 'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'data': result})
    path.write_text(json.dumps({'source': ORIGIN, 'readOnly': True, 'captures': captures}, indent=2) + '\n')
    print(f'{len(captures)} public GETs; 0 mutations; 0 credentials. Saved {path}')

if __name__ == '__main__': main()
