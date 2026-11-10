#!/usr/bin/env python3
"""Refuse the director's real first name in tracked files and commit messages (D-no-real-name).

    python3 scripts/check_no_real_name.py                      every tracked text file
    python3 scripts/check_no_real_name.py --commits A..B       also the messages of that range
    python3 scripts/check_no_real_name.py --ci EVENT BEFORE BASE DEFAULT_REF
                                                               tracked files, plus every commit
                                                               the push or pull request introduces
    python3 scripts/check_no_real_name.py --selftest

The name is not written in this file in any form, reversible or not: only a salted digest is
stored. Each word of the text is lowercased, salted and hashed, and compared with the digest.
Possessives ("X's") are matched through their stem. Hits print the path (or the commit) and a
line number, never the matched text. The selftest uses a made-up word and its own digest.

--ci works out which commits an event introduced and scans all of their messages:
  pull_request   BASE..HEAD            (BASE is the pull request's base commit)
  push           BEFORE..HEAD          (BEFORE is the branch's previous tip)
  push, new ref  DEFAULT_REF..HEAD     (BEFORE is all zeros: everything not already on the
                                        default branch)
  forced push    DEFAULT_REF..HEAD     (BEFORE is gone: a superset of what was pushed; on the
                                        default branch itself this is an error, not a scan)
It fails closed: a shallow checkout, or a BEFORE / BASE / DEFAULT_REF that cannot be resolved,
is an error (exit 2), never a narrower scan. Check out with full history (fetch-depth: 0).

Exit 1 on any hit, 0 clean, 2 on a usage problem or an unresolvable range.
Stdlib only; reads the repository and nothing else.
"""
import hashlib
import os
import re
import subprocess
import sys
import tempfile

SALT = b"tnr-tools:"
DIGESTS = frozenset({"d23901dc44be1b3a1d9345d25baeb36731de96134841e9e826ec27d7459ec3cc"})
WORD = re.compile(r"[A-Za-z]{3,}")
MAX_BYTES = 8 * 1024 * 1024
ZEROS = re.compile(r"^0+$")


class RangeError(Exception):
    """The commits to scan cannot be determined. Never narrowed, always reported."""


def digest(word: str) -> str:
    return hashlib.sha256(SALT + word.lower().encode()).hexdigest()


def scan_text(text: str, digests, cache: dict) -> list:
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for word in WORD.findall(line):
            word = word.lower()
            if word not in cache:
                cache[word] = digest(word) in digests
            if cache[word]:
                hits.append(n)
                break
    return hits


def git(args, cwd=None) -> str:
    return subprocess.check_output(["git"] + args, cwd=cwd, stderr=subprocess.DEVNULL).decode("utf-8", "replace")


def resolves(ref: str, cwd=None) -> bool:
    try:
        git(["cat-file", "-e", f"{ref}^{{commit}}"], cwd)
        return True
    except subprocess.CalledProcessError:
        return False


def ci_range(event: str, before: str, base: str, default_ref: str, cwd=None) -> str:
    """The exact range an event introduced, or RangeError. Never a guess."""
    if git(["rev-parse", "--is-shallow-repository"], cwd).strip() == "true":
        raise RangeError("the checkout is shallow, so earlier commits of the push may be "
                         "missing; check out with fetch-depth: 0")
    if event == "pull_request":
        if not base or not resolves(base, cwd):
            raise RangeError(f"pull request base {base!r} cannot be resolved")
        return f"{base}..HEAD"
    if event != "push":
        raise RangeError(f"unsupported event {event!r}")
    if before and not ZEROS.match(before):
        if resolves(before, cwd):
            return f"{before}..HEAD"
        # A forced update: the old tip is gone. Everything not on the default branch is a
        # superset of what was pushed, so it is safe, unless this IS the default branch, where
        # that range would be empty and the scan would be narrowed to nothing.
        if (default_ref and resolves(default_ref, cwd)
                and git(["rev-parse", default_ref], cwd) != git(["rev-parse", "HEAD"], cwd)):
            return f"{default_ref}..HEAD"
        raise RangeError(f"the previous tip {before} is not in this checkout and no wider "
                         f"range is available")
    # A new branch or tag: everything it has that the default branch does not.
    if not default_ref or not resolves(default_ref, cwd):
        raise RangeError(f"new ref, and the default branch {default_ref!r} cannot be resolved")
    return f"{default_ref}..HEAD"


def scan_commits(rng: str, digests, cache: dict, cwd=None) -> list:
    log = git(["log", "--format=%H%x00%B%x01", rng], cwd)
    hits = []
    for entry in log.split("\x01"):
        sha, _, body = entry.strip().partition("\0")
        if sha and scan_text(body, digests, cache):
            hits.append(f"commit {sha[:12]} (message)")
    return hits


def scan_tree(digests, cache: dict, cwd=None) -> list:
    hits = []
    for path in [p for p in git(["ls-files", "-z"], cwd).split("\0") if p]:
        try:
            data = open(os.path.join(cwd or ".", path), "rb").read(MAX_BYTES + 1)
        except OSError:
            continue
        if len(data) > MAX_BYTES or b"\0" in data[:4096]:
            continue
        hits += [f"{path}:{line}" for line in scan_text(data.decode("utf-8", "replace"), digests, cache)]
    return hits


def selftest() -> int:
    word = "zorvath"                      # a made-up word; nothing to do with the real name
    digests = frozenset({digest(word)})
    checks, failures = [], []

    def want(cond, label):
        checks.append(label)
        if not cond:
            failures.append(label)

    want(scan_text(f"approved by {word.title()} today", digests, {}) == [1], "the word is found, any case")
    want(scan_text(f"{word}'s go", digests, {}) == [1], "a possessive is found through its stem")
    want(scan_text("approved by dauntless today", digests, {}) == [], "other words pass")
    want(scan_text(f"x{word}y is another word", digests, {}) == [], "a longer word containing it passes")
    want(all(len(d) == 64 and re.fullmatch(r"[0-9a-f]+", d) for d in DIGESTS), "the stored value is a digest")
    want(digest(word) not in DIGESTS, "the test word is not the protected one")

    with tempfile.TemporaryDirectory() as tmp:
        env_git = ["-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false"]
        origin = os.path.join(tmp, "origin")
        os.mkdir(origin)

        def commit(repo, message, name="f.txt", body="x"):
            with open(os.path.join(repo, name), "a") as fh:
                fh.write(body + "\n")
            git(["add", "-A"], repo)
            git(env_git + ["commit", "-q", "-m", message], repo)
            return git(["rev-parse", "HEAD"], repo).strip()

        git(["init", "-q", "-b", "main"], origin)
        first = commit(origin, "first")
        git(["checkout", "-q", "-b", "work"], origin)
        commit(origin, f"earlier message naming {word}")
        commit(origin, "a clean tip")

        rng = ci_range("push", first, "", "main", origin)
        want(scan_commits(rng, digests, {}, origin) != [],
             "push: an earlier offending message behind a clean tip is found")
        want(scan_commits("HEAD~1..HEAD", digests, {}, origin) == [],
             "(control: the tip-only range the old workflow fell back to misses it)")
        rng = ci_range("push", "0" * 40, "", "main", origin)
        want(rng == "main..HEAD" and scan_commits(rng, digests, {}, origin) != [],
             "new branch: every commit not on the default branch is scanned")
        rng = ci_range("pull_request", "", first, "main", origin)
        want(scan_commits(rng, digests, {}, origin) != [], "pull request: base..HEAD is scanned")
        rng = ci_range("push", "1" * 40, "", "main", origin)
        want(rng == "main..HEAD" and scan_commits(rng, digests, {}, origin) != [],
             "forced push to a branch: the wider default-branch range is scanned")
        git(["checkout", "-q", "main"], origin)
        try:
            ci_range("push", "1" * 40, "", "main", origin)
            want(False, "forced push to the default branch fails closed")
        except RangeError:
            want(True, "forced push to the default branch fails closed")
        git(["checkout", "-q", "work"], origin)
        for label, args in (("an unknown previous tip with no default branch", ("push", "1" * 40, "", "nope")),
                            ("a new branch with no default branch", ("push", "0" * 40, "", "nope")),
                            ("a pull request with no base", ("pull_request", "", "", "main")),
                            ("an unknown event", ("schedule", "", "", "main"))):
            try:
                ci_range(*args, cwd=origin)
                want(False, f"{label} fails closed")
            except RangeError:
                want(True, f"{label} fails closed")
        shallow = os.path.join(tmp, "shallow")
        git(["clone", "-q", "--depth", "1", "--branch", "work", "file://" + origin, shallow])
        try:
            ci_range("push", first, "", "main", shallow)
            want(False, "a shallow checkout fails closed")
        except RangeError:
            want(True, "a shallow checkout fails closed")
        with open(os.path.join(origin, "note.txt"), "w") as fh:
            fh.write(f"line one\nsigned off by {word}\n")
        git(["add", "-A"], origin)
        want(scan_tree(digests, {}, origin) == ["note.txt:2"], "a tracked file is reported by path and line")

    for label in failures:
        print(f"  FAIL  {label}")
    print(f"{len(checks) - len(failures)} passed, {len(failures)} failed")
    return 1 if failures else 0


def main(argv) -> int:
    if argv[:1] == ["--selftest"]:
        return selftest()
    rng = None
    if argv[:1] == ["--commits"] and len(argv) == 2:
        rng = argv[1]
    elif argv[:1] == ["--ci"] and len(argv) == 5:
        try:
            rng = ci_range(*argv[1:])
        except RangeError as err:
            print(f"check_no_real_name: cannot determine the commits to scan: {err}")
            return 2
        print(f"check_no_real_name: commit range {rng}")
    elif argv:
        print(__doc__)
        return 2
    cache = {}
    hits = scan_tree(DIGESTS, cache)
    if rng:
        try:
            hits += scan_commits(rng, DIGESTS, cache)
        except subprocess.CalledProcessError:
            print(f"check_no_real_name: the range {rng} cannot be read")
            return 2
    for hit in hits:
        print(f"real first name: {hit}")
    print(f"check_no_real_name: {len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
