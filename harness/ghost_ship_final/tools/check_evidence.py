#!/usr/bin/env python3
"""Fail unless every required Stage 2 evidence file exists and is clean.

    check_evidence.py <results-dir> <gate> [<gate> ...]

A gate file (`<gate>.json`, lower-case; engine-gate or M0 layout) is clean when it parses, records at
least one assertion, reports `failed: 0`, and every entry in `checks` passed
(the count and the entries must agree). Exit 0 when all named gates are clean,
1 otherwise, 2 on usage error. Prints one line per gate.
"""
import json
import os
import sys


def check(path):
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except FileNotFoundError:
        return "missing"
    except (OSError, ValueError) as exc:
        return f"unreadable ({exc})"
    if isinstance(doc.get("allChecks"), list):
        # M0 (m0_verify.py): {"checks": <count>, "failed": <count>, "allChecks": [...]}.
        checks, count, name = doc["allChecks"], doc.get("checks"), "check"
    else:
        # Engine gates (lib/report.ts): {"assertions": <count>, "failed": <count>, "checks": [...]}.
        checks, count, name = doc.get("checks"), doc.get("assertions"), "name"
    if not isinstance(checks, list) or not checks:
        return "no assertions recorded"
    bad = [c.get(name) for c in checks if c.get("pass") is not True]
    if count != len(checks):
        return f"assertion count {count} != {len(checks)} checks"
    if doc.get("failed") != len(bad):
        return f"failed count {doc.get('failed')} != {len(bad)} failing checks"
    if bad:
        return f"{len(bad)} failed: " + "; ".join(str(b) for b in bad)
    return None


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    out, gates = argv[1], argv[2:]
    status = 0
    for gate in gates:
        problem = check(os.path.join(out, f"{gate.lower()}.json"))
        print(f"evidence {gate}: {'FAIL - ' + problem if problem else 'clean'}")
        if problem:
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
