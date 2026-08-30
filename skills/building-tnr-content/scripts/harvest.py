#!/usr/bin/env python3
"""Read a network monitor capture or a harvester bundle without hand-parsing it.

Every capture this session was picked apart by hand: batched tRPC URLs split
on commas, responses zipped back to procedure names, `input` query params
decoded to find out what a call was actually filtered to. That work is
identical every time and it is where two mistakes came from: reading a
type-filtered asset list as proof the map pins did not exist, and reading a
harvest taken hours before a build as proof the same.

So this tool always reports the INPUT alongside the output. A procedure that
was called with a filter is labelled as filtered, and absence from a filtered
call is never evidence of anything.

Usage
  python3 tnr_harvest.py index   capture.json
  python3 tnr_harvest.py get     capture.json --proc quests.get [--out quest.json]
  python3 tnr_harvest.py assets  capture.json [--out assets.json]
  python3 tnr_harvest.py names   capture.json --proc jutsu.getAllNames
  python3 tnr_harvest.py diff    results_bundle.json   # pushed vs live, per entry
  python3 tnr_harvest.py verify  results_bundle.json   # v4.28 asserted-field verdicts; exit 1 on FAIL/UNVERIFIED
  python3 tnr_harvest.py stamp   catalog.json --out stamped.json

`index` first, always. It tells you what the capture can and cannot answer.

Results bundles from builder v4.26+ (harvests/inbox/) are read natively: their
captures[] entries normalise exactly like monitor calls, so index/get/names/assets
work on a pulled inbox bundle without hand-parsing. `diff` still reads the push
entries of the same bundle.
"""
import json, os, sys, urllib.parse
from collections import OrderedDict

TRPC = "/api/trpc/"


# ------------------------------------------------------------------ parsing

def load(path):
    with open(path) as fh:
        return json.load(fh)


def entries(cap):
    """Normalise a monitor capture into [{proc, input, data, filtered}]."""
    out = []
    if isinstance(cap, dict) and isinstance(cap.get("captures"), list) and (
            "builder" in cap or any(isinstance(c, dict) and "proc" in c for c in cap["captures"])):
        # v4.26+ results bundle: the builder took these captures itself.
        for c in cap["captures"]:
            if not isinstance(c, dict) or "proc" not in c:
                continue
            inp = c.get("input") or None
            data = c.get("data")
            if data is None and isinstance(c.get("rows"), list):
                data = c["rows"]
            out.append({
                "proc": c["proc"],
                "input": inp,
                "filtered": isinstance(inp, dict) and len(inp) > 0,
                "data": data,
                "status": c.get("status"),
                "t": c.get("at"),
            })
        return out
    rows = cap if isinstance(cap, list) else cap.get("entries") or []
    for e in rows:
        if not isinstance(e, dict):
            continue
        url = e.get("url") or ""
        if TRPC not in url:
            continue
        procs = url.split(TRPC)[-1].split("?")[0].split(",")
        try:
            q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            inputs = json.loads(q["input"][0]) if "input" in q else {}
        except Exception:
            inputs = {}
        body = e.get("resp") or e.get("response") or ""
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except Exception:
                body = []
        if not isinstance(body, list):
            body = [body]
        for i, proc in enumerate(procs):
            raw = inputs.get(str(i)) or inputs.get(str(i), {})
            inp = (raw or {}).get("json") if isinstance(raw, dict) else None
            data = None
            if i < len(body) and isinstance(body[i], dict):
                data = body[i].get("result", {}).get("data", {}).get("json")
            out.append({
                "proc": proc,
                "input": inp,
                "filtered": bool(inp) and isinstance(inp, dict) and len(inp) > 0,
                "data": data,
                "status": e.get("status"),
                "t": e.get("t"),
            })
    return out


def harvester_rows(cap):
    """A tnr_h1_* harvester bundle: {tool, collector, t, payload:{rows}}."""
    if isinstance(cap, dict) and "payload" in cap:
        return cap.get("collector"), cap.get("t"), cap["payload"].get("rows") or []
    return None, None, []


# ------------------------------------------------------------------ commands

def cmd_index(path):
    cap = load(path)
    coll, t, rows = harvester_rows(cap)
    if coll:
        print(f"harvester bundle: collector={coll}  taken={t}  rows={len(rows)}")
        print("this is a FULL collector dump, not a filtered call.")
        newest = max((r.get("createdAt") or "" for r in rows if isinstance(r, dict)), default="")
        if newest:
            print(f"newest record inside: {newest[:19]}")
            print("anything created after that timestamp is NOT in this file and its absence proves nothing.")
        return 0

    es = entries(cap)
    if not es:
        print("no tRPC calls found. Is this a monitor capture?")
        return 1
    print(f"{len(es)} tRPC calls\n")
    print("%-42s %-7s %-8s %s" % ("procedure", "rows", "status", "input filter"))
    seen = OrderedDict()
    for e in es:
        d = e["data"]
        n = len(d) if isinstance(d, list) else ("obj" if isinstance(d, dict) else "-")
        key = (e["proc"], json.dumps(e["input"], sort_keys=True))
        if key in seen:
            continue
        seen[key] = True
        filt = json.dumps(e["input"]) if e["filtered"] else ""
        print("%-42s %-7s %-8s %s" % (e["proc"][:42], n, e["status"], filt[:60]))
    print()
    filtered = [e for e in es if e["filtered"] and "getAll" in e["proc"]]
    if filtered:
        print("FILTERED LIST CALLS in this capture:")
        for e in filtered:
            print(f"  {e['proc']}  input={json.dumps(e['input'])}")
        print("  Absence of a record from these proves nothing. Re-call without the filter,")
        print("  or with the type you actually need, before concluding anything does not exist.")
    return 0


def _pick(cap, proc):
    return [e for e in entries(cap) if e["proc"] == proc and e["data"] is not None]


def cmd_get(path, proc, out=None):
    cap = load(path)
    hits = _pick(cap, proc)
    if not hits:
        print(f"{proc} not in this capture. Run `index` to see what is.")
        return 1
    d = hits[-1]["data"]
    if isinstance(d, dict):
        ident = d.get("id") or d.get("userId") or ""
        name = d.get("name") or d.get("username") or ""
        print(f"{proc}: id={ident} name={name!r} keys={len(d)}")
        if "content" in d and isinstance(d["content"], dict):
            objs = d["content"].get("objectives") or []
            print(f"  quest record: {len(objs)} objectives, hidden={d.get('hidden')}, rank={d.get('questRank')}")
    elif isinstance(d, list):
        print(f"{proc}: {len(d)} rows")
    if out:
        json.dump(d, open(out, "w"), indent=1)
        print(f"written to {out}")
    return 0


def cmd_assets(path, out=None):
    """Merge every gameAsset.getAllNames call, keeping track of which types were asked for."""
    cap = load(path)
    coll, t, rows = harvester_rows(cap)
    if coll == "assets" or (rows and isinstance(rows[0], dict) and "folder" in rows[0] and "type" in rows[0]):
        merged, types = rows, sorted({r.get("type") for r in rows if isinstance(r, dict)})
        asked = types
    else:
        hits = _pick(cap, "gameAsset.getAllNames")
        merged, asked = [], []
        for h in hits:
            if isinstance(h["data"], list):
                merged += h["data"]
            if isinstance(h["input"], dict) and h["input"].get("type"):
                asked.append(h["input"]["type"])
        types = sorted({r.get("type") for r in merged if isinstance(r, dict) and r.get("type")})
    if not merged:
        print("no asset rows in this capture")
        return 1
    print(f"{len(merged)} asset rows")
    print(f"types requested: {', '.join(asked) if asked else 'unfiltered'}")
    if types:
        print(f"types present:   {', '.join(types)}")
    missing = {"STATIC", "SCENE_BACKGROUND", "SCENE_CHARACTER", "SFX", "MUSIC"} - set(asked or types)
    if asked and missing:
        print(f"NOT COVERED:     {', '.join(sorted(missing))}")
        print("  a record of one of those types cannot appear here regardless of whether it exists.")
    from collections import Counter
    folders = Counter((r.get("folder") or "(none)") for r in merged if isinstance(r, dict))
    print("\ntop folders: " + ", ".join(f"{k} {v}" for k, v in folders.most_common(8)))
    if out:
        json.dump({"_generated_at": t, "_types_requested": asked or "unfiltered",
                   "_source": os.path.basename(path), "rows": merged},
                  open(out, "w"), indent=1)
        print(f"\nwritten to {out}")
    return 0


def cmd_names(path, proc, out=None):
    cap = load(path)
    hits = _pick(cap, proc)
    if not hits:
        print(f"{proc} not in this capture")
        return 1
    rows = []
    for h in hits:
        if isinstance(h["data"], list):
            rows += h["data"]
    print(f"{proc}: {len(rows)} rows")
    dupes = {}
    for r in rows:
        if isinstance(r, dict) and r.get("name"):
            dupes.setdefault(r["name"].strip().lower(), []).append(r.get("id"))
    coll = {k: v for k, v in dupes.items() if len(v) > 1}
    if coll:
        print(f"duplicate names live right now: {len(coll)}")
        for k, v in list(coll.items())[:8]:
            print(f"  {k!r} x{len(v)}")
        print("  name uniqueness is enforced on update; a create colliding with one of these")
        print("  produces a blank shell. Dedup against this list before naming anything.")
    if out:
        json.dump(rows, open(out, "w"), indent=1)
        print(f"written to {out}")
    return 0




def deep_diff(a, b, path=""):
    """Minimal recursive diff: [(path, before, after)]. Lists compare whole."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            out += deep_diff(a.get(k), b.get(k), f"{path}.{k}" if path else k)
    elif a != b:
        sa = json.dumps(a, default=str)
        sb = json.dumps(b, default=str)
        out.append((path, sa[:60], sb[:60]))
    return out


IGNORE_DIFF = {"updatedAt", "createdAt", "experience", "curHealth", "curChakra", "curStamina"}


def cmd_diff(path):
    """Diff pushed vs live for every entry in a results bundle: shows exactly
    what the server rewrote. This is how scaleUserStats normalisation, silent
    field stripping and enum coercion become visible without a source dive."""
    d = load(path)
    es = d.get("entries") or []
    if not es:
        print("no entries; is this a results bundle?")
        return 1
    for e in es:
        p, l = e.get("pushed"), e.get("live")
        name = e.get("name") or e.get("id")
        if not p or not l:
            print(f"{name}: {'no read-back' if p else 'no pushed payload'}")
            continue
        rows = [(k, a, b) for k, a, b in deep_diff(p, l) if k.split(".")[0] not in IGNORE_DIFF]
        print("\n%s (%s/%s) -> %s: %d field(s) rewritten server-side" % (
            name, e.get("entity"), e.get("slot"), e.get("id"), len(rows)))
        for k, a, b in rows[:30]:
            print(f"  {k:<28} {a}  ->  {b}")
        if len(rows) > 30:
            print(f"  ... {len(rows)-30} more")
    return 0

def cmd_verify(path):
    """Per-entry verification verdict for a results bundle (builder v4.28+).

    Reads entries[].asserted (the manifest-asserted-fields checklist) and the
    v4.24 full-record verdict, and prints one line per write entry:

      OK          asserted fields all landed (and full-record verdict shown)
      FAIL        one or more asserted fields missing / blanked / unref /
                  mismatch on the live read-back
      UNVERIFIED  the write reported success but the read-back returned no
                  record (live=NONE) - this is NOT success, treat as unshipped

    Exit code is 1 if any FAIL or UNVERIFIED write entry exists, so this can
    gate a session close. Bundles older than v4.28 lack `asserted`; those fall
    back to the full-record verdict only and say so.
    """
    d = load(path)
    es = d.get("entries") or []
    if not es:
        if d.get("captures"):
            print("capture-only bundle (0 write entries): nothing to verify")
            return 0
        print("no entries; is this a results bundle?")
        return 1
    bver = d.get("builder", "?")
    bad = 0
    n_ok = n_fail = n_unv = n_skip = 0
    for e in es:
        name = e.get("name") or e.get("id") or "?"
        ident = e.get("id") or "-"
        if e.get("state") != "ok":
            print(f"SKIP        {name}: state={e.get('state')} ({e.get('detail','')[:60]})")
            n_skip += 1
            continue
        v = e.get("verdict")
        a = e.get("asserted")
        if v == "skipped" or e.get("entity") == "aiProfile":
            print(f"SKIP        {name} ({e.get('entity')}): read-back not applicable")
            n_skip += 1
            continue
        if v == "unread" or (e.get("pushed") and e.get("live") is None):
            print(f"UNVERIFIED  {name} -> {ident}: write ok but live=NONE (read-back empty)")
            n_unv += 1
            bad += 1
            continue
        if a is None:
            tag = "OK?" if v == "match" else "FAIL?"
            print(f"{tag:<11} {name} -> {ident}: pre-v4.28 bundle, no asserted checklist; "
                  f"full-record verdict={v}")
            if v != "match":
                bad += 1
            continue
        fails = a.get("fail") or []
        # server normalization: '' sent vs null stored (or vice versa) on the
        # SAME top-level key is byte-different but semantically identical -
        # observed live on jutsu requiredBloodlineItemId/parentJutsuId while
        # bloodlineId/villageId kept ''. Reclassify, never fail on it. The
        # panel-side comparator (pfEq) gets the same rule in v4.29.
        norm = []
        real = []
        p_, l_ = e.get("pushed") or {}, e.get("live") or {}
        for f in fails:
            k = f.get("k")
            pv, lv = p_.get(k), l_.get(k)
            if f.get("c") == "mismatch" and (
                    (pv == "" and lv is None) or (pv is None and lv == "")):
                norm.append(k)
            else:
                real.append(f)
        fails = real
        if fails:
            n_fail += 1
            bad += 1
            det = "  ".join(f"{f.get('c')}:{f.get('k')}" for f in fails[:6])
            print(f"FAIL        {name} -> {ident}: {len(fails)} asserted field(s) [{det}]"
                  + (f" +{len(fails)-6} more" if len(fails) > 6 else ""))
            for f in fails[:6]:
                for dd in (f.get("d") or [])[:2]:
                    print(f"              {dd}")
        else:
            n_ok += 1
            extra = "" if v == "match" else f"  (full-record {v}: server rewrote unasserted fields)"
            if norm:
                extra += "  (%d field(s) ''<->null server-normalized: %s)" % (len(norm), ",".join(norm))
            print(f"OK          {name} -> {ident}: A:{a.get('ok',0)} asserted field(s) landed{extra}")
    print(f"\nbuilder {bver}: {n_ok} ok, {n_fail} fail, {n_unv} unverified, {n_skip} skipped"
          f"  ->  {'VERIFY FAILED' if bad else 'verified'}")
    return 1 if bad else 0


def cmd_stamp(path, out=None):
    """Add a freshness contract to a catalog so staleness is visible."""
    d = load(path)
    rows = d.get("rows") or d.get("payload", {}).get("rows") or []
    newest = max((r.get("createdAt") or "" for r in rows if isinstance(r, dict)), default="")
    stamp = {
        "_freshness": {
            "row_count": len(rows),
            "newest_record": newest[:19] or "unknown",
            "contract": ("This is a TRIMMED SNAPSHOT for id lookup and dedup only. It is not truth about "
                         "content, and it is never evidence of absence: anything created after "
                         f"{newest[:19] or 'the harvest'} is not in here. Re-harvest before deleting, "
                         "renaming, or concluding a record does not exist."),
        }
    }
    if isinstance(d, dict):
        d = {**stamp, **d}
    tgt = out or path
    json.dump(d, open(tgt, "w"), indent=1)
    print(f"stamped {tgt}: {len(rows)} rows, newest {newest[:19] or 'unknown'}")
    return 0


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 0
    cmd, path = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]

    def opt(n, d=None):
        return args[args.index(n) + 1] if n in args else d

    if cmd == "index":
        return cmd_index(path)
    if cmd == "get":
        return cmd_get(path, opt("--proc"), opt("--out"))
    if cmd == "assets":
        return cmd_assets(path, opt("--out"))
    if cmd == "names":
        return cmd_names(path, opt("--proc"), opt("--out"))
    if cmd == "diff":
        return cmd_diff(path)
    if cmd == "verify":
        return cmd_verify(path)
    if cmd == "stamp":
        return cmd_stamp(path, opt("--out"))
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
