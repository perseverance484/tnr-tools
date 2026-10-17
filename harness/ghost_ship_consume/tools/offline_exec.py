#!/usr/bin/env python3
"""Fail-closed offline launch; an explicit seccomp mode supports restricted containers.

Default unshare mode uses BOTH a private network namespace and syscall denial.
seccomp mode denies the same socket syscalls without requiring namespace privileges.
Neither mode executes the child when its isolation setup fails.
"""
import os
from pathlib import Path
import sys

mode = os.environ.get("TNR_NETWORK_ISOLATION", "unshare")
if mode not in ("unshare", "seccomp") or len(sys.argv) < 2:
    raise SystemExit("usage: TNR_NETWORK_ISOLATION=unshare|seccomp offline_exec.py COMMAND [ARGS]")
deny = str(Path(__file__).with_name("deny_network.py"))
child = sys.argv[1:]
if Path(child[0]).name == "bun":
    # Bun loads .env files independently of the parent's environment allowlist.
    child = [child[0], "--no-env-file", "--no-install", *child[1:]]
cmd = [sys.executable, deny, *child]
if mode == "unshare":
    cmd = ["unshare", "-rn", *cmd]
os.execvp(cmd[0], cmd)
