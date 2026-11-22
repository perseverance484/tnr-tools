#!/usr/bin/env python3
"""Apply curation.EDGE_OPS and curation.KIND_DEFS to interactions.json in place. Idempotent: running it twice
changes nothing the second time. Existing notes on links the ops don't name (the overlaps notes included) stay.

    python3 edges.py ../interactions.json
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import curation as C  # noqa: E402


def apply(doc):
    edges = doc["edges"]

    def find(s, t, k):
        return next((e for e in edges if (e["from"], e["to"], e["kind"]) == (s, t, k)), None)

    for op in C.EDGE_OPS:
        if op[0] == "del":
            _, s, t, k = op
            e = find(s, t, k)
            if e:
                edges.remove(e)
        elif op[0] == "put":
            _, s, t, k, note = op
            e = find(s, t, k)
            if e:
                e["note"] = note
                e["evidence"] = "source-verified"
            else:
                edges.append({"from": s, "to": t, "kind": k, "note": note, "evidence": "source-verified"})
        elif op[0] == "rekind":
            _, s, t, old, new, note = op
            e = find(s, t, old) or find(s, t, new)
            if e:
                e["kind"], e["note"], e["evidence"] = new, note, "source-verified"
            else:
                edges.append({"from": s, "to": t, "kind": new, "note": note, "evidence": "source-verified"})
        else:
            raise ValueError(op)
    kinds = dict(doc["kinds"])
    kinds.update(C.KIND_DEFS)
    doc["kinds"] = {k: kinds[k] for k in C.KIND_ORDER if k in kinds}
    missing = set(kinds) - set(doc["kinds"])
    if missing:
        raise ValueError(f"kinds not in KIND_ORDER: {missing}")
    used = {e["kind"] for e in edges}
    if used - set(doc["kinds"]):
        raise ValueError(f"links use undefined kinds: {used - set(doc['kinds'])}")
    seen = set()
    for e in edges:
        key = (e["from"], e["to"], e["kind"])
        if key in seen:
            raise ValueError(f"duplicate link {key}")
        seen.add(key)
    return doc


def main():
    path = sys.argv[1]
    doc = apply(json.load(open(path)))
    with open(path, "w") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    c = Counter(e["kind"] for e in doc["edges"])
    print(f"{path}: {len(doc['edges'])} links; " + ", ".join(f"{k} {n}" for k, n in c.most_common()))


if __name__ == "__main__":
    main()
