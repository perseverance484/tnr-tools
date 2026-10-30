#!/usr/bin/env python3
"""Merge hunts_main.ts result files (run per path group, to keep each process small) into one.

    python3 harness/skyglass_wreck_sim/tools/hunts_merge.py OUT.json IN1.json IN2.json ...
"""
import json
import sys

out, ins = sys.argv[1], sys.argv[2:]
docs = [json.load(open(p)) for p in ins]
merged = dict(docs[0])
merged["results"] = [r for d in docs for r in d["results"]]
merged["mergedFrom"] = ins
json.dump(merged, open(out, "w"), indent=1)
open(out, "a").write("\n")
print(f"wrote {out}: {len(merged['results'])} paths")
