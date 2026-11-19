#!/usr/bin/env python3
"""Merge main.ts results files from separate --only runs of ONE scenario into one results file.

    merge_results.py OUT PART.json [PART.json ...]

Refuses unless every part has the same scenario, scenario hash, harness code hash, engine pin, seeds, maxRounds and
mode, and no variant appears twice. Variants keep the scenario's order; each part's invocation is kept.
"""
import json
import sys

SAME = ["scenario", "scenarioSha256", "harnessCode", "enginePin", "seeds", "maxRounds", "mode", "seedFormula", "assumptions"]


def merge(parts):
    first = parts[0]
    for k in SAME:
        vals = {json.dumps(p.get(k), sort_keys=True) for p in parts}
        if len(vals) != 1:
            raise SystemExit(f"parts disagree on {k}: {sorted(vals)}")
    if not first.get("harnessCode"):
        raise SystemExit("parts carry no harnessCode; rerun through run.sh")
    out = {k: first[k] for k in ["scenario", "scenarioSha256", "harnessCode", "enginePin", "seeds", "maxRounds", "mode", "seedFormula", "assumptions"]}
    out["invocations"] = [p["invocation"] for p in parts]
    out["sources"], out["builds"], out["variants"], out["tracesFirstSeed"] = {}, {}, [], {}
    for p in parts:
        for k, v in p["sources"].items():
            if out["sources"].setdefault(k, v) != v:
                raise SystemExit(f"parts disagree on source {k}")
        for v in p["variants"]:
            if v["name"] in out["builds"]:
                raise SystemExit(f"variant {v['name']} appears in more than one part")
            out["builds"][v["name"]] = p["builds"][v["name"]]
            out["variants"].append(v)
        out["tracesFirstSeed"].update(p["tracesFirstSeed"])
    return out


def main(argv):
    if len(argv) < 3:
        raise SystemExit(__doc__)
    parts = []
    for path in argv[2:]:
        with open(path) as f:
            parts.append(json.load(f))
    out = merge(parts)
    with open(argv[1], "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv)
