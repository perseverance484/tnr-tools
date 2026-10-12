#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

out, app, bun_status, evidence_status, negative_status, source_status = sys.argv[1:]
here = Path(__file__).resolve().parents[1]
repo = here.parents[1]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
run = lambda *a: subprocess.check_output(a, text=True).strip()
files = sorted(p for sub in ('engine', 'selftest', 'tools') for p in (here/sub).rglob('*')
               if p.is_file() and '__pycache__' not in p.parts)
files += [here/'run.sh']
record = repo/'state/ghost_ship_skyglass_final_item_records.json'
data = {
 'engine': {'repository': 'studie-tech/TheNinjaRPG', 'commit': '585534d7eb21d6f0dd678d5c3eb92662f611d39b',
            'export': 'git archive <pin> app; every pinned file checked before and after tests',
            'bunLockSha256': sha(Path(app)/'bun.lock'), 'packageJsonSha256': sha(Path(app)/'package.json')},
 'designCommit': '8a78115367feda143e9591f524b739a7d56330af',
 'historicalActiveConsume3x3': 'fcd79e5a3401dc8d95abbdaa05d0d4664c04a6e2',
 'historicalR4': '3f825562ea051306a3803f47428b742ae5100011',
 'runtime': {'bun': run('bun','--version'), 'node': run('node','--version'), 'python': sys.version.split()[0]},
 'isolation': {'mode': os.environ.get('TNR_NETWORK_ISOLATION','unshare'),
               'network': 'socket/connect/bind/listen/accept/send/io_uring syscalls denied; inherited by descendants',
               'database': 'none; write-trapping read-only stub', 'environment': 'env -i allowlist; CI placeholders only; Bun --no-env-file --no-install'},
 'dependencies': 'existing user-approved frozen install; dependency manifests unchanged from historical engine',
 'finalRecordsSha256': sha(record),
 'crownedBehaviorSha256': sha(repo/'state/ghost_ship_skyglass_crowned_support_behavior.md'),
 'harnessFileSha256': {str(p.relative_to(here)): sha(p) for p in files},
 'historicalM0ScriptSha256': sha(repo/'harness/ghost_ship_stage2/m0_verify.py'),
 'exitStatuses': {'bun':int(bun_status),'evidence':int(evidence_status),'negativeSelftest':int(negative_status),'sourceIntegrity':int(source_status)},
}
Path(out,'provenance.json').write_text(json.dumps(data,indent=1,sort_keys=True)+'\n')
