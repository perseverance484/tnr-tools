#!/usr/bin/env python3
"""Snapshot the exact records the Bastion commanders and regulars equip, with provenance.

Jutsu: every id in skills/building-tnr-content/data/32b_DATA_pool.json that the authoring
design references, plus Tempest Cleave, taken from committed operator captures
(harvests/inbox/*.json, guide-studio/fixtures/*.json): latest `updatedAt` per id wins, ties by
file name. Weapons: Solar Bow / Crossbow have no committed capture, so they come from the pinned
upstream seed `app/data/item.sql` (historic seed; NOT proof of the current live record).

    python3 tools/extract_sources.py --engine <engine export app dir>   # write sources/
    python3 tools/extract_sources.py --engine <dir> --check              # verify current
"""
import argparse, glob, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(ROOT, "../.."))
OUT = os.path.join(ROOT, "sources", "source_records.json")
POOL = "skills/building-tnr-content/data/32b_DATA_pool.json"
EXTRA_JUTSU = {"Ul83iTziN__Z0i_UOzZTK": "Tempest Cleave"}
SEED_ITEMS = {"ALqXVSL58QMfJ4DgoJ5Il": "Solar Bow", "LbccOnzfsADLgTBPSHjKK": "Crossbow"}
ITEM_COLS = None

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def design_codes():
    codes = set()
    for f in ("commanders.json", "regulars.json"):
        p = os.path.join(ROOT, "design", f)
        if not os.path.exists(p):
            continue
        for unit in json.load(open(p))["units"]:
            codes.update(k for k in unit["kit"] if not k.startswith("X:"))
    return codes

def captures():
    files = sorted(glob.glob(os.path.join(REPO, "harvests/inbox/*.json")) + glob.glob(os.path.join(REPO, "guide-studio/fixtures/*.json")))
    for f in files:
        try:
            yield f, json.load(open(f))
        except Exception:
            continue

def find_jutsu(ids):
    found = {}
    for f, d in captures():
        stack = [d]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                if o.get("id") in ids and "effects" in o and "actionCostPerc" in o:
                    key = (str(o.get("updatedAt", "")), os.path.basename(f))
                    if o["id"] not in found or key > found[o["id"]][0]:
                        found[o["id"]] = (key, os.path.relpath(f, REPO), o)
                stack.extend(o.values())
            elif isinstance(o, list):
                stack.extend(o)
    return found

def parse_sql_row(row):
    vals, i, cur, q = [], 0, "", False
    while i < len(row):
        ch = row[i]
        if q:
            if ch == "\\" and i + 1 < len(row):
                cur += row[i + 1]; i += 2; continue
            if ch == "'":
                q = False
            else:
                cur += ch
        elif ch == "'":
            q = True
        elif ch == ",":
            vals.append(cur.strip()); cur = ""
        else:
            cur += ch
        i += 1
    vals.append(cur.strip())
    return vals

def seed_items(engine):
    path = os.path.join(engine, "data", "item.sql")
    text = open(path, encoding="utf-8").read()
    cols = re.search(r"INSERT INTO `Item` \(([^)]*)\)", text).group(1).replace("`", "").split(", ")
    out = {}
    for line in text.splitlines():
        m = re.match(r"\s*\((.*)\)[,;]\s*$", line)
        if not m:
            continue
        vals = parse_sql_row(m.group(1))
        if vals[0] in SEED_ITEMS:
            rec = dict(zip(cols, vals))
            rec["effects"] = json.loads(rec["effects"])
            for k in ("cost", "chakraCost", "staminaCost", "range", "actionCostPerc", "healthCost", "cooldown", "stackSize"):
                rec[k] = int(rec[k])
            for k in ("canStack", "destroyOnUse", "hidden", "inShop", "isEventItem", "preventBattleUsage"):
                rec[k] = rec[k] == "1"
            out[vals[0]] = rec
    return out, os.path.relpath(path, engine), sha(path)

def build(engine):
    pool = json.load(open(os.path.join(REPO, POOL)))["records"]
    codes = sorted(design_codes() | {c for c in pool if c in {"B33", "B14", "B28", "B37", "S07", "B08", "B10", "B16", "B32",
        "B06", "B07", "B13", "B15", "B22", "B23", "B29", "B34", "B35", "S35", "B03", "B12", "B11", "B30", "S31", "B17",
        "B18", "S34", "B09", "EA04", "B27", "B05", "B26", "B20"}})
    missing = [c for c in codes if c not in pool and not c.startswith("TC")]
    if missing:
        sys.exit(f"pool codes not in {POOL}: {missing}")
    ids = {pool[c]["id"]: c for c in codes if c in pool}
    ids.update({k: "TC" for k in EXTRA_JUTSU})
    found = find_jutsu(set(ids))
    absent = sorted(set(ids) - set(found))
    if absent:
        sys.exit(f"no committed full capture for: {absent}")
    jutsu = {}
    for jid, code in sorted(ids.items(), key=lambda x: x[1]):
        (_, f, rec) = found[jid]
        jutsu[code] = {"id": jid, "name": rec["name"], "provenance": {"capture": f, "updatedAt": rec.get("updatedAt")},
                       "poolSummary": pool.get(code), "record": rec}
    items, seedpath, seedsha = seed_items(engine)
    return {
        "schema": "tnr.silent_bastion_authoring.source_records.v1",
        "status": "EVIDENCE SNAPSHOT — committed operator captures + pinned upstream seed; not a fresh live readback",
        "pool": {"path": POOL, "sha256": sha(os.path.join(REPO, POOL))},
        "enginePin": open(os.path.join(engine, "..", "PIN")).read().strip(),
        "jutsu": jutsu,
        "seedItems": {"source": {"path": seedpath, "sha256": seedsha, "note": "historic seed rows; current live records unverified"},
                      "records": {SEED_ITEMS[k]: v for k, v in sorted(items.items())}},
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    text = json.dumps(build(os.path.abspath(a.engine)), indent=1, sort_keys=True) + "\n"
    if a.check:
        cur = open(OUT).read() if os.path.exists(OUT) else ""
        print("source_records.json:", "current" if cur == text else "STALE")
        return 0 if cur == text else 1
    open(OUT, "w").write(text)
    d = json.loads(text)
    print(f"wrote sources/source_records.json: {len(d['jutsu'])} jutsu, {len(d['seedItems']['records'])} seed items")
    return 0

if __name__ == "__main__":
    sys.exit(main())
