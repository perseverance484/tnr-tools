#!/usr/bin/env python3
"""Post-run evidence gate: every named gate file must exist, record checks, and have no failed
check. Reproduced findings (engine/design defects) are printed; they never count as passes."""
import json, os, sys

def main() -> int:
    out, gates = sys.argv[1], sys.argv[2:]
    status = 0
    for gate in gates:
        path = os.path.join(out, f"{gate}.json")
        if not os.path.exists(path):
            print(f"evidence: {gate}: MISSING"); status = 1; continue
        data = json.load(open(path))
        n, failed = data.get("assertions", 0), [c["name"] for c in data.get("checks", []) if not c.get("pass")]
        print(f"evidence: {gate}: {n} checks, {len(failed)} failed")
        if n == 0 or failed:
            status = 1
            for name in failed[:20]: print(f"  FAILED {name}")
        for f in data.get("findings", []):
            print(f"  FINDING {f['id']} reproduced={f['reproduced']}: {f['summary']}")
    return status

if __name__ == "__main__":
    sys.exit(main())
