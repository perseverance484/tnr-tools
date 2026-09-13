#!/usr/bin/env python3
from pathlib import Path

p = Path("skills/building-tnr-content/scripts/quest_worker_contract_test.py")
text = p.read_text(encoding="utf-8")
old = '''    require(text, '[[ "$ACTUAL_SHA" == "$SOURCE_SHA" ]]', "request checkout is exact-SHA pinned", failures)
    require(text, '[[ -f "request/$SOURCE_PATH" && ! -L "request/$SOURCE_PATH" ]]', "source must be a regular non-symlink file", failures)'''
new = '''    require(text, 'if [[ "$ACTUAL_SHA" != "$SOURCE_SHA" ]]; then', "request checkout SHA is verified after exact-SHA checkout", failures)
    require(text, '! -f "request/$SOURCE_PATH" || -L "request/$SOURCE_PATH"', "source must be a regular non-symlink file", failures)'''
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected one stale worker-contract assertion block, found {count}")
p.write_text(text.replace(old, new), encoding="utf-8")
print("Follow-up worker-contract assertions updated.")
