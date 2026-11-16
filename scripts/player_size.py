#!/usr/bin/env python3
"""The AI player's size, for every handoff (state/prompt_ai_player_overhaul.md section 4: "Keep complexity visible
from AP1 on") and for AP6's budget: total lines, the largest file, the largest function, and the most branching
function, over player/ without its tests.

    python3 scripts/player_size.py            the report
    python3 scripts/player_size.py --json     the same numbers as JSON

Branching is counted the usual way (cyclomatic complexity): 1 for the function, plus 1 for every if, loop, except
handler, conditional expression, comprehension loop and boolean operator beyond the first operand.
Stdlib only; reads the repository and nothing else.
"""
import ast
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCH = (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.IfExp, ast.comprehension, ast.AsyncFor)


def branching(fn):
    n = 1
    for node in ast.walk(fn):
        if isinstance(node, BRANCH):
            n += 1
        elif isinstance(node, ast.BoolOp):
            n += len(node.values) - 1
    return n


def measure(root=ROOT):
    files, funcs = [], []
    for path in sorted(glob.glob(os.path.join(root, "player", "**", "*.py"), recursive=True)):
        rel = os.path.relpath(path, root)
        if f"{os.sep}tests{os.sep}" in path:
            continue
        with open(path, encoding="utf8") as f:
            src = f.read()
        files.append((len(src.splitlines()), rel))
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                funcs.append((node.end_lineno - node.lineno + 1, branching(node), f"{rel}:{node.name}"))
    tests = sum(len(open(p, encoding="utf8").read().splitlines())
                for p in glob.glob(os.path.join(root, "player", "tests", "*.py")))
    return {"lines": sum(n for n, _ in files), "files": len(files), "test_lines": tests,
            "largest_file": max(files), "largest_function": max(funcs)[::2],
            "most_branching": max((b, n) for _, b, n in funcs),
            "functions_over_60_lines": sorted(n for ln, _, n in funcs if ln > 60),
            "functions_over_12_branches": sorted(f"{n} ({b})" for _, b, n in funcs if b > 12),
            "files_over_400_lines": sorted(n for ln, n in files if ln > 400),
            "by_file": {n: ln for ln, n in files}}


if __name__ == "__main__":
    m = measure()
    if "--json" in sys.argv:
        print(json.dumps(m, indent=1))
    else:
        print(f"player code: {m['lines']:,} lines in {m['files']} files (tests: {m['test_lines']:,} lines)")
        print(f"largest file: {m['largest_file'][1]} ({m['largest_file'][0]} lines)")
        print(f"largest function: {m['largest_function'][1]} ({m['largest_function'][0]} lines)")
        print(f"most branching: {m['most_branching'][1]} ({m['most_branching'][0]})")
        for k in ("files_over_400_lines", "functions_over_60_lines", "functions_over_12_branches"):
            print(f"{k.replace('_', ' ')}: {', '.join(m[k]) or 'none'}")
