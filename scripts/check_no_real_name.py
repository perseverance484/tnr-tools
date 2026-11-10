#!/usr/bin/env python3
"""Refuse the director's real first name in tracked files and commit messages (D-no-real-name).

    python3 scripts/check_no_real_name.py                 every tracked text file
    python3 scripts/check_no_real_name.py --commits A..B  also the messages of that commit range
    python3 scripts/check_no_real_name.py --selftest

The name is not written in this file. Each word of the text is lowercased, salted and hashed,
and compared with the stored digest, so the check can live in a public repository. Possessives
("X's") are matched through their stem. Hits print the path (or the commit) and a line number,
never the matched text. Exit 1 on any hit, 0 clean, 2 on a usage problem.
Stdlib only; reads the repository and nothing else.
"""
import hashlib
import re
import subprocess
import sys

SALT = b"tnr-tools:"
DIGESTS = {"d23901dc44be1b3a1d9345d25baeb36731de96134841e9e826ec27d7459ec3cc"}
WORD = re.compile(r"[A-Za-z]{3,}")
MAX_BYTES = 8 * 1024 * 1024


def is_name(word: str, cache: dict) -> bool:
    word = word.lower()
    hit = cache.get(word)
    if hit is None:
        hit = hashlib.sha256(SALT + word.encode()).hexdigest() in DIGESTS
        cache[word] = hit
    return hit


def scan_text(text: str, cache: dict) -> list:
    return [n for n, line in enumerate(text.splitlines(), 1)
            if any(is_name(w, cache) for w in WORD.findall(line))]


def tracked_files() -> list:
    out = subprocess.check_output(["git", "ls-files", "-z"])
    return [p for p in out.decode().split("\0") if p]


def main(argv) -> int:
    cache, hits = {}, []
    if argv[:1] == ["--selftest"]:
        probe = "".join(chr(c) for c in (122, 111, 114, 118, 97, 116, 104))
        ok = (scan_text(f"approved by {probe} today", cache) == [1]
              and scan_text(f"{probe.lower()}'s go", cache) == [1]
              and scan_text("approved by dauntless today", cache) == []
              and scan_text(f"x{probe}y is another word", cache) == [])
        print("selftest OK" if ok else "selftest FAILED")
        return 0 if ok else 1
    commits = None
    if argv[:1] == ["--commits"] and len(argv) == 2:
        commits = argv[1]
    elif argv:
        print(__doc__)
        return 2
    for path in tracked_files():
        try:
            data = open(path, "rb").read(MAX_BYTES + 1)
        except OSError:
            continue
        if len(data) > MAX_BYTES or b"\0" in data[:4096]:
            continue
        for line in scan_text(data.decode("utf-8", "replace"), cache):
            hits.append(f"{path}:{line}")
    if commits:
        log = subprocess.check_output(["git", "log", "--format=%H%x00%B%x01", commits]).decode("utf-8", "replace")
        for entry in log.split("\x01"):
            sha, _, body = entry.strip().partition("\0")
            if sha and scan_text(body, cache):
                hits.append(f"commit {sha[:12]} (message)")
    for hit in hits:
        print(f"real first name: {hit}")
    print(f"check_no_real_name: {len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
