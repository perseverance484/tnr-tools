#!/usr/bin/env python3
"""Negative tests for check_validate.judge (review F3), on synthetic validate.py output. No subprocess."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_validate import EXPECTED, EXPECTED_EXIT, EXPECTED_WARNINGS, judge

LINES = [f"ERROR  {line}" for line, _ in EXPECTED]
WARN = [f"warn   synthetic warning {i}" for i in range(EXPECTED_WARNINGS)]
def out(errors, warns=WARN, summary=None):
    n = summary if summary is not None else (len(errors), len(warns))
    return "\n".join(["manifest.json: 27 entries", *errors, *warns, f"{n[0]} errors, {n[1]} warnings", ""])

CASES = [
    ("documented output, exit 1", out(LINES), EXPECTED_EXIT, True),
    ("one documented error duplicated (summary updated)", out(LINES + LINES[:1]), 1, False),
    ("one documented error missing", out(LINES[1:]), 1, False),
    ("one documented error reworded", out(LINES[:-1] + [LINES[-1] + "!"]), 1, False),
    ("one new error", out(LINES + ["ERROR  [quest:x] brand new"]), 1, False),
    ("summary count disagrees with lines", out(LINES, summary=(10, EXPECTED_WARNINGS)), 1, False),
    ("warning count changed", out(LINES, warns=WARN[:-1]), 1, False),
    ("validate.py exit 0", out(LINES), 0, False),
    ("validate.py killed (-9)", out(LINES), -9, False),
    ("validate.py crashed (exit 2, no summary)", "Traceback (most recent call last):\n", 2, False),
]
fails = 0
for name, text, rc, want_ok in CASES:
    _, problems = judge(text, rc)
    ok = (not problems) == want_ok
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name} -> {'pass' if not problems else 'fail'}{'' if ok else f' (problems: {problems})'}")
print(f"test_check_validate: {fails} failed")
sys.exit(1 if fails else 0)
