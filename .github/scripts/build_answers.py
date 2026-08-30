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

CAP_PROC = {"jutsu.getAllNames": "jutsu", "item.getAllNames": "item",
            "quests.getAllNames": "quest", "gameAsset.getAllNames": "asset",
            "profile.getAllAiNames": "ai"}


def bundle_epoch(path):
    m = re.search(r"tnr_results_(\d+)", os.path.basename(path))
    if not m:
        return None
    return datetime.datetime.fromtimestamp(int(m.group(1)) / 1000,
                                           datetime.timezone.utc).strftime("%Y-%m-%d %H:%MZ")


def hot_rows(repo):
    """Newest inbox capture per entity -> {entity: {rows, source, captured}}.
    Fixes the seed-lag gap: a fresh create is visible here the moment its
    bundle lands, without waiting for a seed re-harvest."""
    out = {}
    for p in sorted(glob.glob(os.path.join(repo, "harvests", "inbox", "tnr_results_*.json"))):
        try:
            d = json.load(open(p))
        except Exception:
            continue
        for c in d.get("captures") or []:
            ent = CAP_PROC.get(str(c.get("proc") or ""))
            if not ent:
                continue
            rows = c.get("rows") if isinstance(c.get("rows"), list) else                    (c.get("data") if isinstance(c.get("data"), list) else None)
            if rows is None:
                continue
            norm = [[r.get("id") or r.get("userId"), r.get("name") or r.get("username"),
                     r.get("hidden")] for r in rows if isinstance(r, dict)]
            norm = [r for r in norm if r[0] and r[1]]
            if norm:      # later bundles overwrite earlier: sorted() = oldest first
                out[ent] = {"rows": norm, "source": os.path.relpath(p, repo),
                            "captured": bundle_epoch(p) or "unknown"}
    return out


def main():
    repo = "."; out = "answers"
    a = sys.argv[1:]
    if "--repo" in a: repo = a[a.index("--repo")+1]
    if "--out" in a: out = a[a.index("--out")+1]
    os.makedirs(os.path.join(repo, out), exist_ok=True)
    hot = hot_rows(repo)
    index = ["# answers/INDEX.md - the lookup layer", "",
             "Two fetches answer any name/id lookup: this INDEX, then the entity file",
             "(plus hot.json when its delta column below is non-zero). Rows are",
             "`[id, name, hidden]`; `hidden: null` means the source did not carry the",
             "flag. `generated` stamps are DERIVED from sources, so regeneration is",
             "idempotent. Raw CDN caches ~5 min; fresher than that takes a capture.", "",
             "| entity | rows | source stamp | hot delta (newer, uncataloged) | fetch |",
             "|---|---|---|---|---|"]
    wrote = 0
    hot_out = {"note": ("Recently harvested records NOT yet in the seed catalogs: "
                        "newest inbox capture per entity, minus rows the seed already "
                        "holds. A name here is live even though names_<entity>.json "
                        "lacks it."),
               "entities": {}}
    for ent, frags in ENTITIES.items():
        src = newest(repo, frags)
        if not src:
            index.append(f"| {ent} | - | none committed | - | - |"); continue
        rows, stamp = rows_from(src)
        rows.sort(key=lambda r: (r[1] or "").lower())
        seed_ids = {r[0] for r in rows}
        h = hot.get(ent)
        delta = []
        if h:
            delta = sorted([r for r in h["rows"] if r[0] not in seed_ids],
                           key=lambda r: (r[1] or "").lower())
            if delta:
                hot_out["entities"][ent] = {"source_bundle": h["source"],
                                            "captured": h["captured"],
                                            "row_delta": len(delta), "rows": delta}
        fn = f"names_{ent}.json"
        rel_src = os.path.relpath(src, repo)
        payload = {"generated": stamp or "unknown", "entity": ent, "source": rel_src,
                   "source_stamp": stamp, "count": len(rows),
                   "hot_delta": len(delta),
                   "hot_hint": (f"{len(delta)} newer record(s) live but uncataloged - "
                                f"fetch answers/hot.json" if delta else None),
                   "rows": rows}
        with open(os.path.join(repo, out, fn), "w") as f:
            json.dump(payload, f, separators=(",", ":"))
        index.append(f"| {ent} | {len(rows)} | {stamp or 'unknown'} | "
                     f"{len(delta)} | {RAW}/answers/{fn} |")
        wrote += 1
    with open(os.path.join(repo, out, "hot.json"), "w") as f:
        json.dump(hot_out, f, separators=(",", ":"))
    index += ["", f"Hot shard (delta rows + capture stamps): {RAW}/answers/hot.json",
              "", "Other fetchable canon:",
              f"- Engine laws (full numbered text): {RAW}/docs/ENGINE_LAWS.md",
              f"- Doctrine (single source): {RAW}/docs/DOCTRINE.md",
              "", "Skill zips (download, not fetch): /dist/ on the repo page.",
              "", "A capture beats any file here (precedence). Retention: see",
              "docs/COMPACTION_RUNBOOK.md - manual-only, seed is the audit floor."]
    open(os.path.join(repo, out, "INDEX.md"), "w").write("\n".join(index) + "\n")
    print(f"answers: {wrote} entity files + hot.json "
          f"({sum(v['row_delta'] for v in hot_out['entities'].values())} delta rows) + INDEX.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
