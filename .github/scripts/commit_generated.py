#!/usr/bin/env python3
"""Commit generated files and retry a concurrent branch advance by rebasing."""

from __future__ import annotations

import os
import subprocess
import sys


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check)


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: commit_generated.py MESSAGE PATHSPEC...", file=sys.stderr)
        return 2

    branch = os.environ.get("GITHUB_REF_NAME")
    if not branch or os.environ.get("GITHUB_REF_TYPE") != "branch":
        print("generated commits require a branch ref", file=sys.stderr)
        return 2

    message, *paths = sys.argv[1:]
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run("git", "add", "--", *paths)

    if run("git", "diff", "--cached", "--quiet", check=False).returncode == 0:
        print("no generated changes")
        return 0

    run("git", "commit", "-m", message)
    for attempt in range(1, 4):
        if run("git", "push", "origin", f"HEAD:{branch}", check=False).returncode == 0:
            return 0
        if attempt == 3:
            break
        print(f"branch advanced during generated commit; rebasing (attempt {attempt}/2)")
        run("git", "fetch", "origin", f"+refs/heads/{branch}:refs/remotes/origin/{branch}")
        if run("git", "rebase", f"origin/{branch}", check=False).returncode != 0:
            run("git", "rebase", "--abort", check=False)
            print("generated commit conflicts with the new branch head", file=sys.stderr)
            return 1

    print("generated commit could not be pushed after 3 attempts", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
