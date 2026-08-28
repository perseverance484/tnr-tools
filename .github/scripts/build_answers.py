#!/usr/bin/env python3
"""Build the answer layer from /harvests. Newest source per entity wins.

Accepts three shapes: catalog {_freshness, cols, rows}, raw dump [ {...}, ... ],
or {data: [...]}. Emits answers/names_<entity>.json + answers/INDEX.md with
absolute raw URLs (the fetcher cannot mint URLs, so every link is absolute).
"""
import os, sys, json, glob, re, datetime

RAW = "https://raw.githubusercontent.com/perseverance484/tnr-tools/main"
ENTITIES = {  # entity -> filename fragments that identify a source, most specific first
    "jutsu": ["40_INDEX_jutsu", "jutsu"],
    "item":  ["41_INDEX_item", "item"],
    "ai":    ["42_INDEX_ai", "ai_catalog", "userdata", "_ai"],
    "asset": ["43_INDEX_asset", "asset", "gameasset"],
    "quest": ["47_INDEX_quest", "quest"],
}

def rows_from(path):
    d = json.load(open(path))
    stamp = None
    if isinstance(d, dict):
        fresh = d.get("_freshness") or {}
        stamp = (fresh.get("generated") or fresh.get("date") or fresh.get("harvested")
                 or fresh.get("newest_record") or d.get("generated"))
        if stamp and "unknown" in str(stamp): stamp = "seed catalog (pre-answers)"
        if "cols" in d and "rows" in d:
            cols = [c.lower() for c in d["cols"]]
            def idx(*names):
                for n in names:
                    if n in cols: return cols.index(n)
                return None
            ii, ni, hi = idx("id"), idx("name","username","n"), idx("hidden","hid")
            out = []
            for r in d["rows"]:
                if ii is None or ni is None: break
                out.append([r[ii], r[ni], (bool(r[hi]) if hi is not None and r[hi] is not None else None)])
            return out, stamp
        d = d.get("data") or d.get("rows") or []
    if isinstance(d, list) and d and isinstance(d[0], dict):
        out = []
        for r in d:
            rid = r.get("id") or r.get("userId")
            nm = r.get("name") or r.get("username")
            if rid and nm: out.append([rid, nm, r.get("hidden")])
        return out, stamp
    return [], stamp

def newest(repo, frags):
    cands = []
    for p in glob.glob(os.path.join(repo, "harvests", "**", "*.json"), recursive=True):
        base = os.path.basename(p).lower()
        for rank, f in enumerate(frags):
            if f.lower() in base:
                cands.append((rank, -os.path.getmtime(p), p)); break
    return sorted(cands)[0][2] if cands else None

def main():
    repo = "."; out = "answers"
    a = sys.argv[1:]
    if "--repo" in a: repo = a[a.index("--repo")+1]
    if "--out" in a: out = a[a.index("--out")+1]
    os.makedirs(os.path.join(repo, out), exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    index = [f"# answers/INDEX.md - the lookup layer", "",
             f"generated: {now}. Raw CDN caches ~5 min; a lookup that must be fresher takes a capture.",
             "Rows are `[id, name, hidden]`; `hidden: null` means the source did not carry the flag.", "",
             "| entity | rows | source | source stamp | fetch |", "|---|---|---|---|---|"]
    wrote = 0
    for ent, frags in ENTITIES.items():
        src = newest(repo, frags)
        if not src:
            index.append(f"| {ent} | - | none committed | - | - |"); continue
        rows, stamp = rows_from(src)
        rows.sort(key=lambda r: (r[1] or "").lower())
        fn = f"names_{ent}.json"
        rel_src = os.path.relpath(src, repo)
        payload = {"generated": now, "entity": ent, "source": rel_src,
                   "source_stamp": stamp, "count": len(rows), "rows": rows}
        with open(os.path.join(repo, out, fn), "w") as f:
            json.dump(payload, f, separators=(",", ":"))
        index.append(f"| {ent} | {len(rows)} | `{rel_src}` | {stamp or 'unknown'} | {RAW}/answers/{fn} |")
        wrote += 1
    index += ["", "Other fetchable canon:",
              f"- Engine laws (full numbered text): {RAW}/docs/ENGINE_LAWS.md",
              f"- Rollout plan: {RAW}/docs/ROLLOUT_PLAN.md",
              "", "Skill zips (download, not fetch): /dist/ on the repo page.",
              "", "A capture beats any file here (precedence). Hidden content of the current",
              "wave may predate the newest committed harvest; absence is not proof."]
    open(os.path.join(repo, out, "INDEX.md"), "w").write("\n".join(index) + "\n")
    print(f"answers: wrote {wrote} entity files + INDEX.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
