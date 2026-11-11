#!/usr/bin/env python3
"""Add a jutsu/item record (JSON from jutsu.get / item.get, read from stdin or a file) to harness/pvp_turn/kit/records.json.
Usage: add_record.py [FILE]   (between fights only; rerun harness/pvp_turn/tools/build_catalog.py afterwards)"""
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
path = os.path.join(REPO, "harness/pvp_turn/kit/records.json")
rec = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else json.load(sys.stdin)
store = json.load(open(path))
store[rec["id"]] = {"record": rec, "source": "connector read", "updatedAt": rec.get("updatedAt", "")}
json.dump(store, open(path, "w"), indent=1)
print("added", rec["id"], rec.get("name"))
