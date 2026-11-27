#!/usr/bin/env python3
"""Check an engine export against the pinned game tree, file by file, before any of it runs.

    python3 harness/combat_sim/tools/verify_export.py GAME_CLONE PIN APP_DIR

Every regular file under APP_DIR (except node_modules/ and the launcher's own tnr_combat_sim_*/ run
folders) must be in `git ls-tree -r PIN app` with the same blob hash, and every file in that tree must be
present. Symlinks or other entry types in either side are refused. Exits 0 when they match, 2 otherwise.
Reads only; no network.
"""
import hashlib
import os
import subprocess
import sys

SKIP_TOP = ("node_modules",)
RUN_PREFIX = "tnr_combat_sim_"


def pinned(src, pin):
    out = subprocess.run(["git", "-C", src, "ls-tree", "-r", "-z", pin, "app"], check=True, capture_output=True).stdout
    want, bad = {}, []
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, kind, sha = meta.split(b" ")
        rel = os.fsdecode(path)[len("app/"):]
        if kind != b"blob" or mode not in (b"100644", b"100755"):
            bad.append(f"unsupported pinned entry {mode.decode()} {rel}")
            continue
        want[rel] = sha.decode()
    return want, bad


def blob_sha(path):
    h = hashlib.sha1()
    size = os.path.getsize(path)
    h.update(b"blob %d\0" % size)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def present(app):
    have, bad = {}, []
    for root, dirs, files in os.walk(app):
        rel_root = os.path.relpath(root, app)
        if rel_root == ".":
            dirs[:] = [d for d in dirs if d not in SKIP_TOP and not d.startswith(RUN_PREFIX)]
        for d in list(dirs):
            if os.path.islink(os.path.join(root, d)):
                bad.append(f"symlinked directory {os.path.normpath(os.path.join(rel_root, d))}")
                dirs.remove(d)
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.normpath(os.path.join(rel_root, f))
            if os.path.islink(p) or not os.path.isfile(p):
                bad.append(f"not a regular file {rel}")
                continue
            have[rel] = blob_sha(p)
    return have, bad


def compare(want, have):
    problems = []
    for rel in sorted(set(want) - set(have)):
        problems.append(f"missing {rel}")
    for rel in sorted(set(have) - set(want)):
        problems.append(f"extra {rel}")
    for rel in sorted(set(want) & set(have)):
        if want[rel] != have[rel]:
            problems.append(f"changed {rel}")
    return problems


def main(argv):
    if len(argv) != 4:
        raise SystemExit(__doc__)
    src, pin, app = argv[1], argv[2], argv[3]
    want, bad_want = pinned(src, pin)
    have, bad_have = present(app)
    problems = bad_want + bad_have + compare(want, have)
    if problems:
        sys.stderr.write(f"engine export {app} does not match pin {pin} ({len(problems)} problems):\n")
        sys.stderr.write("".join(f"  {p}\n" for p in problems[:20]))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
