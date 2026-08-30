#!/usr/bin/env python3
"""pushpack.py - build a push pack: one zip = manifest.json + its images.

    python3 pushpack.py manifest.json img1.webp img2.webp ... [-o pack.zip] [--no-validate]

The pack is what builder v4.25's Load button eats whole: no image picker, no
per-file downloads, exact filenames preserved. This tool exists so the pack
cannot be built wrong:

  1. validate.py runs on the manifest first (same dir as this script, else cwd).
     Nonzero exit aborts the pack. --no-validate skips, and says so loudly.
  2. Every @img:<name> reference must have a matching image argument, by exact
     basename. A missing one aborts; an unreferenced provided image warns.
  3. imgSizes is (re)written into the packed manifest from the actual bytes,
     so the builder's integrity gate always checks against truth.
  4. Images are written STORED (webp does not recompress); the manifest too,
     so the browser reader never needs DecompressionStream.

Stdlib only.
"""
import argparse, json, os, re, subprocess, sys, zipfile

IMGRE = re.compile(r'@img:([A-Za-z0-9_.\-]+)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest')
    ap.add_argument('images', nargs='*')
    ap.add_argument('-o', '--out', default=None)
    ap.add_argument('--no-validate', action='store_true')
    a = ap.parse_args()

    with open(a.manifest, 'r', encoding='utf-8') as f:
        mtext = f.read()
    try:
        m = json.loads(mtext)
    except Exception as e:
        sys.exit('manifest is not JSON: %s' % e)

    # 1. reference <-> file matching
    refs = sorted(set(IMGRE.findall(mtext)))
    by_name = {}
    for p in a.images:
        if not os.path.exists(p):
            sys.exit('image not found: ' + p)
        by_name[os.path.basename(p)] = p
    missing = [r0 for r0 in refs if r0 not in by_name]
    if missing:
        sys.exit('@img references with no provided image: ' + ', '.join(missing))
    extra = [n for n in by_name if n not in refs]
    for n in extra:
        print('note: %s is not referenced by any @img (packed anyway)' % n)

    # 2. sizes ledger from actual bytes, injected BEFORE validation so the
    #    validated manifest is byte-identical to the shipped one (and L17 sees
    #    the ledger this tool just wrote)
    sizes = {n: os.path.getsize(p) for n, p in by_name.items()}
    m['imgSizes'] = dict(m.get('imgSizes') or {}, **sizes)
    packed_manifest = json.dumps(m, ensure_ascii=False, indent=1)

    # 3. validate the packed manifest
    if a.no_validate:
        print('WARNING: --no-validate: this pack ships an UNVALIDATED manifest')
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        vp = os.path.join(here, 'validate.py')
        if not os.path.exists(vp):
            vp = 'validate.py'
        if not os.path.exists(vp):
            sys.exit('validate.py not found beside pushpack.py or in cwd; '
                     'run from the workdir or pass --no-validate (discouraged)')
        import tempfile
        with tempfile.NamedTemporaryFile('w', suffix='_packed.json',
                                         dir='.', delete=False) as tf:
            tf.write(packed_manifest)
            tmp = tf.name
        try:
            r = subprocess.run([sys.executable, vp, tmp],
                               capture_output=True, text=True)
        finally:
            os.unlink(tmp)
        tail = (r.stdout or '') + (r.stderr or '')
        if r.returncode != 0:
            sys.exit('validate.py FAILED on the packed manifest:\n' + tail)
        line = [l for l in tail.splitlines() if 'error' in l]
        print('validate.py (packed): ' + (line[-1].strip() if line else 'pass'))

    # 4. write pack, everything STORED
    out = a.out or (os.path.splitext(os.path.basename(a.manifest))[0] + '_pack.zip')
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_STORED) as z:
        z.writestr('manifest.json', packed_manifest)
        for n, p in sorted(by_name.items()):
            z.write(p, n)

    kb = os.path.getsize(out) / 1024.0
    print('pack: %s (%.1fKB) = manifest.json + %d image(s)' % (out, kb, len(by_name)))
    for n in sorted(sizes):
        print('  %s  %dB' % (n, sizes[n]))
    if refs:
        print('all %d @img reference(s) satisfied, sizes ledgered' % len(refs))


if __name__ == '__main__':
    main()
