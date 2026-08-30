#!/usr/bin/env python3
"""sentinel_hash.py - canonical contract hashes for the upstream-drift sentinel.

Hashes extracted 45x contract files at the ARTIFACT level (report W3-RQ3):
upstream refactors that do not change contracts stay silent; contract changes
ring. Volatile top-level keys (anything starting with '_': provenance stamps,
generation notes) are stripped before hashing, then the document is serialized
sort_keys canonical and sha256'd - so the hash is stable across extraction
runs, key order, and stamp differences.

Usage
  python3 sentinel_hash.py FILE [FILE...]                     # print hashes
  python3 sentinel_hash.py --baseline OUT.json [--meta k=v] FILE...
  python3 sentinel_hash.py --check BASELINE.json FILE...      # exit 1 on drift

--check compares by basename, prints per-file same/CHANGED/new, exit 1 when
anything changed or a baseline file is missing from the inputs. Stdlib only.
"""
import hashlib
import json
import sys
import time
from os.path import basename


def canon_hash(path):
    doc = json.load(open(path))
    if isinstance(doc, dict):
        doc = {k: v for k, v in doc.items() if not k.startswith("_")}
    blob = json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 0
    meta = {}
    if "--meta" in a:
        i = a.index("--meta")
        k, _, v = a[i + 1].partition("=")
        meta[k] = v
        a = a[:i] + a[i + 2:]
    if a[0] == "--baseline":
        out, files = a[1], a[2:]
        doc = {
            "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "meta": meta,
            "files": {basename(f): canon_hash(f) for f in sorted(files)},
        }
        doc["combined"] = hashlib.sha256(
            json.dumps(doc["files"], sort_keys=True).encode()).hexdigest()
        json.dump(doc, open(out, "w"), indent=1)
        print("baseline -> %s (combined %s)" % (out, doc["combined"][:12]))
        return 0
    if a[0] == "--check":
        base, files = json.load(open(a[1])), a[2:]
        cur = {basename(f): canon_hash(f) for f in files}
        drift = 0
        for name, h in sorted(base.get("files", {}).items()):
            c = cur.get(name)
            if c is None:
                print("MISSING  %s (in baseline, not among inputs)" % name)
                drift = 1
            elif c != h:
                print("CHANGED  %s  %s -> %s" % (name, h[:12], c[:12]))
                drift = 1
            else:
                print("same     %s  %s" % (name, h[:12]))
        for name in sorted(set(cur) - set(base.get("files", {}))):
            print("NEW      %s  %s (not in baseline)" % (name, cur[name][:12]))
            drift = 1
        print("drift" if drift else "no drift vs baseline %s" %
              base.get("generated", "?"))
        return 1 if drift else 0
    for f in a:
        print("%s  %s" % (canon_hash(f), basename(f)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
