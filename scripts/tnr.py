#!/usr/bin/env python3
"""Small task entry point. Commands delegate to repository-owned tools; no game requests."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'skills/building-tnr-content/scripts'
sys.path.insert(0, str(TOOLS))
import record_index

CONTEXTS = {
    'missions.check': 'skills/building-tnr-content/packs/mission-check.md',
    'jutsu.art': 'docs/workflows/JUTSU_ART_LOOKUP.md',
    'content.build': 'skills/building-tnr-content/SKILL.md',
    'code.review': 'docs/workflows/FABLE_REVIEW.md',
    'art.produce': 'docs/workflows/ART_PRODUCTION.md',
    'repository.audit': 'docs/agents/RELEASE_AUDITOR.md',
}


def revision():
    proc = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode:
        raise ValueError('cannot identify repository revision')
    dirty = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True)
    return {'commit': proc.stdout.strip(), 'tracked_changes': bool(dirty)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    missions = sub.add_parser('missions', help='query committed mission observations')
    msub = missions.add_subparsers(dest='operation', required=True)
    check = msub.add_parser('check', help='bounded structural inspection; no construction or balance audit')
    check.add_argument('--rank', choices=['A', 'B', 'C', 'D', 'S'], required=True)
    check.add_argument('--id', action='append', default=[], help='restrict to exact record ID; repeatable')
    check.add_argument('--json', action='store_true')
    context = sub.add_parser('context', help='print only the selected task packet')
    context.add_argument('task', choices=CONTEXTS)
    context.add_argument('--rank', choices=['A', 'B', 'C', 'D', 'S'], default='A')
    workstream = sub.add_parser('workstream', help='delegate to content_workstream.py')
    workstream.add_argument('args', nargs=argparse.REMAINDER)
    session = sub.add_parser('session', help='read-only global summary')
    session.add_argument('--guards', action='store_true')
    sub.add_parser('verify', help='run repository consistency gates')
    args = parser.parse_args(argv)
    try:
        if args.command == 'missions':
            report = record_index.mission_report(record_index.load_current(ROOT), args.rank, args.id)
            report['repository'] = revision()
            if args.json:
                print(json.dumps(report, indent=2, ensure_ascii=False))
            else:
                print(f"Repository {report['repository']['commit']} (tracked changes: {report['repository']['tracked_changes']})")
                print(record_index.mission_text(report), end='')
            # Unknown overall population is coverage metadata, not an assertion of failure.
            # A requested identity that cannot be resolved must never look like a successful lookup.
            return int(not report['records'] or bool(report['requested_ids_not_resolved'])
                       or any(r['mission']['findings'] for r in report['records']))
        if args.command == 'context':
            rev = revision()
            print(f"Repository: perseverance484/tnr-tools @ {rev['commit']}; tracked changes: {rev['tracked_changes']}")
            print(f"Task: {args.task}. Continue the requested task; do not initialize unrelated workstreams.")
            if args.task == 'missions.check':
                print(f'Command: python3 scripts/tnr.py missions check --rank {args.rank}')
            print((ROOT / CONTEXTS[args.task]).read_text(), end='')
            return 0
        if args.command == 'workstream':
            return subprocess.call([sys.executable, str(ROOT / 'scripts/content_workstream.py'), *args.args], cwd=ROOT)
        if args.command == 'session':
            command = [sys.executable, str(TOOLS / 'session_open.py')]
            return subprocess.call(command + (['--guards'] if args.guards else []), cwd=ROOT)
        return subprocess.call([sys.executable, str(ROOT / 'scripts/check_repo.py')], cwd=ROOT)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f'UNVERIFIED: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
