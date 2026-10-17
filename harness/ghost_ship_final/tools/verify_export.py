#!/usr/bin/env python3
"""Verify every pinned app file against its git blob; ignores added harness/dependencies."""
import hashlib
from pathlib import Path
import subprocess
import sys

src, pin, export = sys.argv[1:]
tree = subprocess.check_output(["git", "-C", src, "ls-tree", "-rz", pin, "app"])
checked = 0
for row in tree.split(b"\0"):
    if not row:
        continue
    header, name = row.split(b"\t", 1)
    mode, kind, expected = header.split()
    if kind != b"blob":
        raise SystemExit(f"unsupported tree entry: {name!r}")
    path = Path(export) / name.decode()
    raw = str(path.readlink()).encode() if mode == b"120000" else path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if actual != expected.decode():
        raise SystemExit(f"engine export differs from pin: {name.decode()}")
    checked += 1
print(f"engine export: {checked} pinned files unchanged")
