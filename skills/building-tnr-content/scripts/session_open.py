#!/usr/bin/env python3
"""Read-only session summary. Task queries do not require a global session ritual."""
import argparse
import json
from pathlib import Path
from session_close import run_guards

ROOT = Path(__file__).resolve().parents[3]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--guards', action='store_true', help='run repository guards explicitly')
    parser.add_argument('--read', metavar='PATH', help='report read size without editing the shared digest')
    args = parser.parse_args(argv)
    try:
        if args.read:
            path = (ROOT / args.read).resolve()
            path.relative_to(ROOT)
            print(f'READ {args.read}: {path.stat().st_size} bytes (session-local; no shared ledger write)')
            return 0
        digest = json.loads((ROOT / 'state/digest.json').read_text())
    except (OSError, ValueError) as error:
        print(f'SESSION UNAVAILABLE: {error}')
        return 1
    print(f"STATE AS OF {digest.get('generated', 'unknown')}: {digest.get('state_line', 'unknown')}")
    print("ROUTE docs/00_INDEX.md; continue the user's task. Workstreams: state/workstreams/INDEX.md")
    if not args.guards:
        print('Guards not run; use --guards for repository maintenance, not routine lookups.')
        return 0
    failures = run_guards(str(ROOT), digest)
    for line in digest.get('verified_at_close', []):
        print('GUARD ' + line)
    print('GUARDS FAILED: ' + ', '.join(failures) if failures else 'Applicable guards passed; see NOT APPLICABLE entries.')
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
