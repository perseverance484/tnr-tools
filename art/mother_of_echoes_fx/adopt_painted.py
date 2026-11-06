#!/usr/bin/env python3
"""Adopt reviewed painted-region slices into exports/ and write exports/moe_fx_painted_a14.json (push/mother_of_echoes.gen.py
PAINT_META). Each source is DIR:META[:PREFIX]; rows keep their region unless PREFIX is given, then the region becomes
PREFIX_<region> (e.g. glassfall_first_pane). Existing rows of other regions are kept; rows of a re-adopted region are
replaced. Files are copied byte for byte.

    python3 art/mother_of_echoes_fx/adopt_painted.py SRC_DIR:META.json[:prefix] [...]
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORTS = os.path.join(HERE, "exports")
OUT = os.path.join(EXPORTS, "moe_fx_painted_a14.json")


def main():
    have = json.load(open(OUT))["slices"] if os.path.exists(OUT) else []
    new = []
    for arg in sys.argv[1:]:
        parts = arg.split(":")
        d, meta = parts[0], parts[1]
        prefix = parts[2] if len(parts) > 2 else None
        for r in json.load(open(os.path.join(d, meta)))["slices"]:
            region = f"{prefix}_{r['region']}" if prefix else r["region"]
            shutil.copyfile(os.path.join(d, r["file"]), os.path.join(EXPORTS, r["file"]))
            new.append({"file": r["file"], "region": region, "col": r["col"], "row": r["row"], "frames": r["frames"]})
    regions = {r["region"] for r in new}
    rows = [r for r in have if r["region"] not in regions] + new
    keys = [(r["region"], r["col"], r["row"]) for r in rows]
    if len(keys) != len(set(keys)):
        raise SystemExit("duplicate (region, col, row) rows")
    with open(OUT, "w") as fh:
        json.dump({"source": "art/mother_of_echoes_fx/adopt_painted.py", "slices": sorted(rows, key=lambda r: (r["region"], r["col"], r["row"]))},
                  fh, indent=1)
        fh.write("\n")
    print(len(rows), "rows,", len(regions), "regions adopted:", ", ".join(sorted(regions)))


if __name__ == "__main__":
    main()
