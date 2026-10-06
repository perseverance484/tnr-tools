#!/usr/bin/env python3
"""Derived, read-only record views from persisted Forge captures; no game transport.

Older builder captures remain evidence but are not promoted through this adapter.
An exact-record read proves that record's fields at that time, never a population.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = 'answers/records.json'
SCHEMA = 'tnr.records/1'
PROCEDURES = {
    'quests.get': ('quest', 'id'),
    'jutsu.get': ('jutsu', 'id'),
    'item.get': ('item', 'id'),
    'gameAsset.get': ('asset', 'id'),
    'profile.getAi': ('ai', 'userId'),
}
PRODUCER = 'skills/building-tnr-content/scripts/record_index.py'


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inputs(root):
    paths = [root / PRODUCER, *sorted((root / 'harvests/inbox').glob('*.json'))]
    return {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in paths}


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('missing capture timestamp')
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('capture timestamp has no timezone')
    return dt.astimezone(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def mission_fields(data):
    """Only structural observations; no build-profile, balance or reachability verdict."""
    findings = []
    content = data.get('content')
    objectives = content.get('objectives') if isinstance(content, dict) else None
    if not isinstance(objectives, list):
        findings.append('missing objective list')
        objectives = []
    ids = [o.get('id') for o in objectives if isinstance(o, dict)]
    if len(ids) != len(objectives) or any(not isinstance(i, str) or not i for i in ids):
        findings.append('invalid objective identity')
    valid_ids = [i for i in ids if isinstance(i, str) and i]
    if len(set(valid_ids)) != len(valid_ids):
        findings.append('duplicate objective IDs')
    targets = set()
    enemies = set()
    tasks = Counter()
    for o in objectives:
        if not isinstance(o, dict):
            continue
        task = o.get('task')
        if isinstance(task, str):
            tasks[task] += 1
        else:
            findings.append('missing objective task')
        nxt = o.get('nextObjectiveId')
        if isinstance(nxt, str):
            if nxt:
                targets.add(nxt)
        elif isinstance(nxt, list):
            for choice in nxt:
                if isinstance(choice, dict) and isinstance(choice.get('nextObjectiveId'), str):
                    targets.add(choice['nextObjectiveId'])
                else:
                    findings.append('invalid objective choice')
        elif nxt is not None:
            findings.append('unsupported nextObjectiveId shape')
        for field in ('opponentAIs', 'attackers'):
            for group in o.get(field) or []:
                if isinstance(group, dict):
                    enemies.update(i for i in group.get('ids', []) if isinstance(i, str))
    dangling = targets - set(valid_ids)
    if dangling:
        findings.append('missing edge targets: ' + ', '.join(sorted(dangling)))
    return {
        'questType': data.get('questType'), 'rank': data.get('questRank'),
        'requiredLevel': data.get('requiredLevel'), 'maxLevel': data.get('maxLevel'),
        'objective_count': len(objectives), 'tasks': dict(sorted(tasks.items())),
        'enemy_ids': sorted(enemies), 'findings': sorted(set(findings)),
    }


def derive(root=ROOT):
    root = Path(root)
    source_hashes = inputs(root)
    attempts = defaultdict(list)
    excluded = Counter()
    scanned = 0
    for path, digest in source_hashes.items():
        if not path.startswith('harvests/'):
            continue
        bundle = json.loads((root / path).read_text())
        if not isinstance(bundle, dict) or not isinstance(bundle.get('captures', []), list):
            raise ValueError(f'{path}: invalid capture envelope')
        for ordinal, capture in enumerate(bundle.get('captures', [])):
            scanned += 1
            if not isinstance(capture, dict):
                raise ValueError(f'{path}: capture {ordinal} is not an object')
            proc = capture.get('proc')
            if proc not in PROCEDURES:
                excluded['unsupported_procedure'] += 1
                continue
            if bundle.get('cfg') != 'forge':
                excluded['legacy_adapter_required'] += 1
                continue
            if capture.get('persist') != 'full':
                excluded['summary_not_record_evidence'] += 1
                continue
            entity, id_key = PROCEDURES[proc]
            inp = capture.get('input')
            record_id = inp.get(id_key) if isinstance(inp, dict) else None
            if not isinstance(record_id, str) or not record_id:
                raise ValueError(f'{path} /captures/{ordinal}: no exact input identity')
            evidence = {'bundle': path, 'pointer': f'/captures/{ordinal}/data',
                        'bundle_sha256': digest, 'procedure': proc, 'input': inp}
            errors = []
            try:
                at = timestamp(capture.get('at'))
            except (ValueError, TypeError) as error:
                at = None
                errors.append(str(error))
            evidence['captured_at'] = at
            if bundle.get('state') != 'DONE' or bundle.get('outcome') != 'success':
                errors.append('bundle is not a completed successful run')
            if capture.get('ok') is not True or capture.get('error'):
                errors.append('capture did not succeed')
            if capture.get('persist') != 'full' or capture.get('persistOk') is not True or capture.get('persistError'):
                errors.append('full record was not successfully persisted')
            if not isinstance(capture.get('snapshotKey'), str) or not capture.get('snapshotKey'):
                errors.append('missing snapshot identity')
            data = capture.get('data')
            if not isinstance(data, dict) or data.get(id_key) != record_id:
                errors.append('input/record identity mismatch')
            name = data.get('name', data.get('username')) if isinstance(data, dict) else None
            if not isinstance(name, str) or not name.strip():
                errors.append('missing record name')
            if isinstance(data, dict) and 'hidden' in data and type(data['hidden']) is not bool:
                errors.append('invalid hidden flag')
            record = None
            if not errors:
                record = {'entity': entity, 'id': record_id, 'name': name,
                          'hidden': data.get('hidden'), 'evidence': evidence,
                          'record_sha256': sha(encoded(data).encode())}
                if entity == 'quest':
                    record['mission'] = mission_fields(data)
            attempts[(entity, record_id)].append({'at': at, 'record': record,
                                                   'evidence': evidence, 'errors': errors})
    records, unresolved = [], []
    for (entity, record_id), candidates in sorted(attempts.items()):
        # Undated evidence cannot safely be ordered behind a valid snapshot.
        undated = [c for c in candidates if c['at'] is None]
        newest = max((c['at'] for c in candidates if c['at']), default=None)
        current = undated or [c for c in candidates if c['at'] == newest]
        errors = sorted({e for c in current for e in c['errors']})
        hashes = {c['record']['record_sha256'] for c in current if c['record']}
        if len(hashes) > 1:
            errors.append('conflicting records at the same timestamp')
        if errors:
            unresolved.append({'entity': entity, 'id': record_id, 'reasons': errors,
                               'evidence': [c['evidence'] for c in current]})
        else:
            records.append(current[-1]['record'])
    return {'schema': SCHEMA, 'inputs': source_hashes,
            'coverage': {'complete_population': False,
                         'note': 'Exact-record captures only. Missing records and excluded legacy captures prove no absence. No live request was made.',
                         'bundles_scanned': len(source_hashes) - 1, 'captures_scanned': scanned,
                         'excluded': dict(sorted(excluded.items()))},
            'records': records, 'unresolved': unresolved}


def load_current(root=ROOT):
    """Consume a hash-current generated view; otherwise derive in memory, without writes."""
    root = Path(root)
    try:
        cached = json.loads((root / OUTPUT).read_text())
        if cached.get('schema') == SCHEMA and cached.get('inputs') == inputs(root):
            return cached
    except (OSError, ValueError, AttributeError):
        pass
    return derive(root)


def mission_report(index, rank, record_ids=()):
    wanted = set(record_ids)
    records = [r for r in index['records'] if r['entity'] == 'quest'
               and r['mission']['questType'] == 'mission' and r['mission']['rank'] == rank
               and (not wanted or r['id'] in wanted)]
    records.sort(key=lambda r: (r['name'].casefold(), r['id']))
    # Unknown rank on unresolved evidence cannot be silently filtered out of a rank query.
    unresolved = [r for r in index['unresolved'] if r['entity'] == 'quest'
                  and (not wanted or r['id'] in wanted)]
    missing = sorted(wanted - {r['id'] for r in records})
    return {'rank': rank, 'scope': 'latest eligible committed observations, not live verification',
            'coverage': index['coverage'], 'records': records, 'unresolved': unresolved,
            'requested_ids_not_resolved': missing,
            'checks': ['objective identities', 'duplicate objective IDs', 'explicit nextObjectiveId targets'],
            'not_checked': ['balance', 'engine reachability', 'fresh live state', 'complete rank population']}


def mission_text(report):
    lines = [f"Repository snapshot check: {len(report['records'])} rank-{report['rank']} mission(s).",
             'Coverage: PARTIAL / total rank population unknown. This is not a live-game check.']
    for r in report['records']:
        m, e = r['mission'], r['evidence']
        state = 'hidden' if r['hidden'] is True else 'visible' if r['hidden'] is False else 'visibility unknown'
        findings = '; '.join(m['findings']) or 'no findings in the listed structural checks'
        lines += [f"- {r['name']} [{r['id']}]: {state}; {m['objective_count']} objectives; {findings}.",
                  f"  Captured {e['captured_at']}; {e['bundle']}#{e['pointer']}"]
    if report['unresolved']:
        lines.append(f"Coverage limitation: {len(report['unresolved'])} quest ID(s) have unresolved evidence and cannot be classified by rank. Use --json for details.")
    if report['requested_ids_not_resolved']:
        lines.append('Requested IDs not resolved in this rank: ' + ', '.join(report['requested_ids_not_resolved']))
    lines += ['Checked: ' + ', '.join(report['checks']) + '.',
              'Not checked: ' + ', '.join(report['not_checked']) + '.']
    return '\n'.join(lines) + '\n'
