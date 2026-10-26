#!/usr/bin/env python3
"""Manifest-specific validate.py exception gate.

    python3 scripts/validate_exception.py <ledger.json>            # check (exit 0 = exception holds)
    python3 scripts/validate_exception.py <ledger.json> --write    # (re)write the ledger's hash and diagnostics

A ledger names one manifest, its exact SHA-256, the director ruling that approved the exception, and the exact
validate.py --strict diagnostics that ruling accepts. The check passes only when the manifest still hashes to the
ledger's value and validate.py reports exactly those diagnostics and nothing else. Any change to the manifest, or
any new diagnostic, voids the exception.
"""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "skills/building-tnr-content/data")


def diagnostics(manifest):
    r = subprocess.run([sys.executable, "../scripts/validate.py", "--strict", os.path.join(ROOT, manifest)],
                       cwd=DATA, capture_output=True, text=True)
    lines = [l.strip() for l in (r.stdout + r.stderr).splitlines() if re.match(r"^(ERROR|WARN)\b", l.strip())]
    return sorted(lines)


def main():
    ledger_path = os.path.join(ROOT, sys.argv[1])
    led = json.load(open(ledger_path))
    sha = hashlib.sha256(open(os.path.join(ROOT, led["manifest"]), "rb").read()).hexdigest()
    found = diagnostics(led["manifest"])
    if "--write" in sys.argv:
        led["sha256"], led["accepted"] = sha, found
        json.dump(led, open(ledger_path, "w"), indent=1)
        print("ledger written:", sha[:12], len(found), "diagnostic(s)")
        return 0
    ok = True
    if sha != led["sha256"]:
        print("VOID: manifest changed:", sha, "!=", led["sha256"]); ok = False
    if found != sorted(led["accepted"]):
        print("VOID: diagnostics differ from the approved set"); print(" found:", found); print(" approved:", led["accepted"]); ok = False
    if ok:
        print(f"exception holds ({led['ruling']}): {led['manifest']} @ {sha[:12]}, {len(found)} approved diagnostic(s)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
