#!/usr/bin/env python3
"""Read-only repository consistency gate. Generated products are rebuilt in a temporary directory."""
from __future__ import annotations
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from tnr import CONTEXTS

ENTRY_POINTS = ['CHATGPT.md', 'CLAUDE.md', 'README.md', 'docs/00_INDEX.md',
                'docs/agents/PROJECT_INSTRUCTIONS.md', 'skills/building-tnr-content/packs/mission-check.md']
PATH = re.compile(r'(?<![\w/])(?:docs|skills|state|scripts|answers|harvests|forge|guide-studio|\.github)/[A-Za-z0-9_./-]+\.(?:md|json|py|mjs|yml|txt)\b')


def check_routes(root=ROOT):
    problems = []
    for path in set(ENTRY_POINTS) | set(CONTEXTS.values()):
        if not (root / path).is_file():
            problems.append(f'missing task source: {path}')
    for path in ENTRY_POINTS:
        if not (root / path).is_file():
            continue
        for ref in sorted(set(PATH.findall((root / path).read_text()))):
            if not (root / ref).is_file():
                problems.append(f'{path}: missing routed file {ref}')
    mirror = root / 'state/staged_workflows/release_pin.yml'
    if mirror.read_bytes() != (root / '.github/workflows/release_pin.yml').read_bytes():
        problems.append('release-pin compatibility mirror differs from installed owner')
    for name in ('32b_DATA_pool.json', '45c_DATA_constructors.json', '45g_DATA_checks.json'):
        if (root / name).read_bytes() != (root / 'skills/building-tnr-content/data' / name).read_bytes():
            problems.append(f'root contract mirror stale: {name}')
    return problems


def check_answers(root=ROOT):
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run([sys.executable, str(root / '.github/scripts/build_answers.py'),
                                 '--repo', str(root), '--out', tmp], capture_output=True, text=True)
        if result.returncode:
            return ['answer producer failed: ' + result.stdout + result.stderr]
        problems = []
        for path in sorted(Path(tmp).iterdir()):
            target = root / 'answers' / path.name
            if not target.exists() or path.read_bytes() != target.read_bytes():
                problems.append(f'stale generated answers/{path.name}')
        return problems


def main():
    problems = check_routes() + check_answers()
    for problem in problems:
        print('FAIL ' + problem, flush=True)
    tools = 'skills/building-tnr-content/scripts/'
    commands = [
        [tools+'doctrinemap.py'], [tools+'render_doctrine.py', '--check'],
        [tools+'build_packs.py', '--check'], [tools+'lawmap.py'],
        [tools+'session_close.py', '--check'],
        ['scripts/content_workstream.py', 'validate', '--all'],
        ['scripts/content_workstream.py', 'render', '--check'],
        ['scripts/content_workstream.py', '--selftest'],
        ['scripts/jutsu_art.py', 'verify'],
        ['-m', 'unittest', 'scripts/test_record_index.py', 'scripts/test_repo_tasks.py', 'scripts/test_jutsu_art.py'],
    ]
    for args in commands:
        p = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
        print(('PASS ' if p.returncode == 0 else 'FAIL ') + ' '.join(args), flush=True)
        if p.returncode:
            print(p.stdout + p.stderr, flush=True)
            problems.append(' '.join(args))
        elif args[0].endswith(('lawmap.py', 'jutsu_art.py')):
            # Existing warnings/coverage limitations must remain visible on successful gates.
            print(p.stdout.strip(), flush=True)
        elif args[0] == '-m':
            print(p.stderr.strip(), flush=True)
    print(f'Repository consistency: {len(problems)} failure(s).', flush=True)
    return int(bool(problems))


if __name__ == '__main__':
    raise SystemExit(main())
