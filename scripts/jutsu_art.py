#!/usr/bin/env python3
"""Jutsu art lookup: name -> captured record -> image URL, from committed census bundles.

The corpus is the completed player-facing jutsu census (#68-#74, seven Forge capture-only
batches of exact `jutsu.get` full-record reads) plus the #66 partial bundle, which is used
ONLY for its `jutsu.getAllNames` live row count (coverage evidence). The target id list is
the #67 recovery manifest, whose order the batches preserve tranche by tranche.

Every source is pinned in SOURCES below. `build` and `verify` re-derive everything from the
bundles and fail closed on any state/outcome/count/persist/id/manifest-hash mismatch; a
stamped `answers/jutsu_art.json` is never trusted merely because it exists.

Lookup policy: a name resolves only by NORMALIZED EXACT match (NFKC, curly quotes folded to
ASCII, whitespace collapsed and trimmed, casefolded). A miss prints suggestions and exits 1;
nothing is ever auto-selected by similarity.

Zero TNR requests. `materialize` (optional) is the only networked command: it fetches image
bytes from the allowlisted asset CDNs named below and refuses any other host.

    python3 scripts/jutsu_art.py build            # write answers/jutsu_art.json
    python3 scripts/jutsu_art.py verify           # rebuild in memory, compare byte for byte
    python3 scripts/jutsu_art.py lookup "Name"    # exact normalized match
    python3 scripts/jutsu_art.py search fang      # substring search over names
    python3 scripts/jutsu_art.py record "Name"    # full captured record from its bundle
    python3 scripts/jutsu_art.py image-url "Name" # bare URL, for piping
    python3 scripts/jutsu_art.py materialize "Name" --out DIR [--dry-run]
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import sys
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = "answers/jutsu_art.json"
SCHEMA = "tnr.jutsu_art/1"

# ---------------------------------------------------------------------------------------------
# Source pins. Changing any of these is a deliberate corpus change, not a refresh.
# ---------------------------------------------------------------------------------------------
SOURCES = {
    # #66 ran under the ORIGINAL manifest text (commit 1a1c4b9, which still carried the invalid
    # jutsu.getAll read), hence the journal hash differs from today's push/66 file. Only its
    # completed getAllNames summary is used; its state is pinned as the partial it is.
    "coverage": {
        "bundle": "harvests/inbox/tnr_results_1791244038469.json",
        "manifest": "push/66_player_facing_jutsu_census.json",
        "manifest_number": 66,
        "manifest_hash": "61579eea",
        "state": "RUNNING",
        "outcome": "open",
        "proc": "jutsu.getAllNames",
        "live_rows": 1493,
        # The census-time known universe (#67 note: 1,491 = 1,472 seed catalog + 19 hot), pinned
        # as the historical fact it is. Today's answers/ count is a diagnostic only: equal counts
        # from different snapshots never prove the extra live rows were classified (JA-R1).
        "known_rows_at_census": 1491,
        # UNRESOLVED until a reviewed change adopts follow-up capture evidence that identifies and
        # classifies the missing live rows. No count, catalog regeneration or rebuild clears it.
        "status": "UNRESOLVED",
        "resolution": None,
    },
    # The 604-id target list. Its bundle is a stranded partial; only the manifest identity is used.
    "target": {
        "bundle": "harvests/inbox/tnr_results_1791246123358.json",
        "manifest": "push/67_player_facing_jutsu_census_recovery.json",
        "manifest_number": 67,
        "manifest_hash": "4d6b25d1",
        "count": 604,
    },
    "batches": [
        {"manifest": "push/68_player_facing_jutsu_census_batch_1.json", "manifest_number": 68, "manifest_hash": "cad2b183",
         "bundle": "harvests/inbox/tnr_results_1791246947793.json", "start": 0, "count": 100},
        {"manifest": "push/69_player_facing_jutsu_census_batch_2.json", "manifest_number": 69, "manifest_hash": "5cc539a8",
         "bundle": "harvests/inbox/tnr_results_1791247158542.json", "start": 100, "count": 100},
        {"manifest": "push/70_player_facing_jutsu_census_batch_3.json", "manifest_number": 70, "manifest_hash": "21df27eb",
         "bundle": "harvests/inbox/tnr_results_1791247363737.json", "start": 200, "count": 100},
        {"manifest": "push/71_player_facing_jutsu_census_batch_4.json", "manifest_number": 71, "manifest_hash": "09d2edb8",
         "bundle": "harvests/inbox/tnr_results_1791247737840.json", "start": 300, "count": 100},
        {"manifest": "push/72_player_facing_jutsu_census_batch_5.json", "manifest_number": 72, "manifest_hash": "ec8b2cf6",
         "bundle": "harvests/inbox/tnr_results_1791247939010.json", "start": 400, "count": 100},
        {"manifest": "push/73_player_facing_jutsu_census_batch_6.json", "manifest_number": 73, "manifest_hash": "276cf5e0",
         "bundle": "harvests/inbox/tnr_results_1791248138851.json", "start": 500, "count": 100},
        {"manifest": "push/74_player_facing_jutsu_census_batch_7.json", "manifest_number": 74, "manifest_hash": "6209d917",
         "bundle": "harvests/inbox/tnr_results_1791248170855.json", "start": 600, "count": 4},
    ],
    # Today's known jutsu name universe (seed catalog plus hot-shard delta). DIAGNOSTIC ONLY: it is
    # printed by build/verify but never written to the output and never changes coverage status.
    "known_names": {"catalog": "answers/names_jutsu.json", "hot": "answers/hot.json"},
    "expected": {"captured": 604, "eligible": 441, "eligible_unique_image_urls": 440},
}

# #66 inclusion policy: the census targets these catalog types; the final census discards
# hidden records, live AI/BLOODLINE types, and records with direct bloodline ownership.
PLAYER_TYPES = ("CLAN", "EVENT", "FORBIDDEN", "LOYALTY", "NORMAL", "SPECIAL")
ELIGIBILITY_RULE = (
    "eligible = live hidden is exactly false AND live jutsuType in "
    + "/".join(PLAYER_TYPES)
    + " AND live bloodlineId is empty (#66 inclusion policy)"
)

# Asset CDNs that serve TNR uploads. materialize refuses every other host, and refuses the game
# itself outright even if someone adds it here by mistake.
CDN_HOSTS = (
    "ui0arpl8sm.ufs.sh",
    "utfs.io",
    "uploadthing.b-cdn.net",
    "uploadthing.com",
    "theninja-user-uploads.s3.us-west-2.amazonaws.com",
)
GAME_HOST_SUFFIXES = ("theninja-rpg.com",)
MAX_IMAGE_BYTES = 8 * 1024 * 1024


class ProvenanceError(Exception):
    """A source does not match its pin. Nothing derived from it may be used."""


class LookupMiss(Exception):
    def __init__(self, query: str, suggestions: list[str]):
        super().__init__(query)
        self.query = query
        self.suggestions = suggestions


# ---------------------------------------------------------------------------------------------
# Forge manifest identity (mirrors forge/src/storage/hash.mjs + runner/manifest.mjs)
# ---------------------------------------------------------------------------------------------
def _stable(v) -> str:
    if v is None or isinstance(v, (bool, int, float, str)):
        return json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    if isinstance(v, list):
        return "[" + ",".join(_stable(x) for x in v) + "]"
    return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + _stable(v[k]) for k in sorted(v)) + "}"


def _fnv1a32(s: str) -> str:
    h = 0x811C9DC5
    b = s.encode("utf-16-le")  # JS charCodeAt walks UTF-16 code units
    for i in range(0, len(b), 2):
        h ^= b[i] | (b[i + 1] << 8)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def manifest_hash(manifest: dict) -> str:
    """Forge's identity for a default-policy manifest (all census manifests are default-policy)."""
    for key in ("dedupNames", "readBack", "skipPreflight", "imgSizes", "imagePack"):
        if key in manifest:
            raise ProvenanceError(f"manifest carries execution policy key {key!r}; census manifests must not")
    raw = manifest.get("items") if isinstance(manifest.get("items"), list) else []
    return _fnv1a32(_stable({"items": raw, "capture": manifest.get("capture")}))


# ---------------------------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------------------------
_QUOTES = str.maketrans({"‘": "'", "’": "'", "‛": "'", "′": "'",
                         "“": '"', "”": '"', "″": '"'})


def normalize(name: str) -> str:
    s = unicodedata.normalize("NFKC", name).translate(_QUOTES)
    return " ".join(s.split()).casefold()


# ---------------------------------------------------------------------------------------------
# Loading and provenance
# ---------------------------------------------------------------------------------------------
def _load(root: Path, rel: str) -> dict:
    path = root / rel
    if not path.is_file():
        raise ProvenanceError(f"{rel}: missing")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProvenanceError(f"{rel}: not JSON ({exc})") from exc


def _sha256(root: Path, rel: str) -> str:
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


def _need(cond: bool, msg: str) -> None:
    if not cond:
        raise ProvenanceError(msg)


def _target_ids(manifest: dict, rel: str) -> list[str]:
    before = (manifest.get("capture") or {}).get("before") or []
    ids = []
    for i, c in enumerate(before):
        _need(c.get("proc") == "jutsu.get", f"{rel}: capture.before[{i}] is {c.get('proc')!r}, expected jutsu.get")
        _need(c.get("persist") == "full", f"{rel}: capture.before[{i}] persist {c.get('persist')!r}, expected 'full'")
        _need(isinstance((c.get("input") or {}).get("id"), str), f"{rel}: capture.before[{i}] has no input.id")
        ids.append(c["input"]["id"])
    _need(not manifest.get("items"), f"{rel}: has items; census manifests are capture-only")
    _need(not (manifest.get("capture") or {}).get("after"), f"{rel}: has after-captures")
    return ids


def _check_journal(bundle: dict, rel: str, pin: dict) -> dict:
    j = bundle.get("journal") or {}
    _need(j.get("manifestPath") == pin["manifest"], f"{rel}: journal.manifestPath {j.get('manifestPath')!r} != {pin['manifest']!r}")
    _need(j.get("manifestNumber") == pin["manifest_number"], f"{rel}: journal.manifestNumber {j.get('manifestNumber')!r} != {pin['manifest_number']}")
    _need(j.get("manifestHash") == pin["manifest_hash"], f"{rel}: journal.manifestHash {j.get('manifestHash')!r} != pinned {pin['manifest_hash']}")
    return j


def load_corpus(root: Path = ROOT, sources: dict = SOURCES) -> dict:
    """Read and verify every pinned source. Raises ProvenanceError on any mismatch."""
    # --- coverage (#66): live name universe ------------------------------------------------
    cov = sources["coverage"]
    cb = _load(root, cov["bundle"])
    cj = _check_journal(cb, cov["bundle"], cov)
    _need(cb.get("state") == cov["state"] and cj.get("state") == cov["state"],
          f"{cov['bundle']}: state {cb.get('state')!r}/{cj.get('state')!r}, pinned {cov['state']!r}")
    _need(cb.get("outcome") == cov["outcome"], f"{cov['bundle']}: outcome {cb.get('outcome')!r}, pinned {cov['outcome']!r}")
    _need(not cb.get("entries") and not cj.get("items"), f"{cov['bundle']}: carries items/entries; expected zero mutations")
    summaries = (cj.get("capturesBefore") or []) + (cj.get("capturesBeforePartial") or [])
    rows = [s for s in summaries if s.get("proc") == cov["proc"]]
    _need(len(rows) == 1, f"{cov['bundle']}: expected exactly one {cov['proc']} summary, found {len(rows)}")
    s = rows[0]
    _need(s.get("ok") is True and s.get("error") is None and isinstance(s.get("rows"), int),
          f"{cov['bundle']}: {cov['proc']} did not complete cleanly")
    live_rows = s["rows"]
    _need(live_rows == cov["live_rows"], f"{cov['bundle']}: {cov['proc']} rows {live_rows}, pinned {cov['live_rows']}")
    if cov["resolution"] is not None or cov["status"] != "UNRESOLVED":
        # No follow-up evidence path exists yet; adopting one is a reviewed code change, not a pin flip.
        raise ProvenanceError("coverage resolution pinned without an implemented follow-up evidence check")

    # --- target list (#67) ------------------------------------------------------------------
    tgt = sources["target"]
    tm = _load(root, tgt["manifest"])
    _need(manifest_hash(tm) == tgt["manifest_hash"], f"{tgt['manifest']}: hash {manifest_hash(tm)} != pinned {tgt['manifest_hash']}")
    _check_journal(_load(root, tgt["bundle"]), tgt["bundle"], tgt)
    target = _target_ids(tm, tgt["manifest"])
    _need(len(target) == tgt["count"], f"{tgt['manifest']}: {len(target)} target ids, pinned {tgt['count']}")
    _need(len(set(target)) == len(target), f"{tgt['manifest']}: duplicate target ids")

    # --- batches (#68-#74) ------------------------------------------------------------------
    records: list[dict] = []
    batch_meta: list[dict] = []
    expected_start = 0
    for pin in sources["batches"]:
        mrel, brel = pin["manifest"], pin["bundle"]
        m = _load(root, mrel)
        got = manifest_hash(m)
        _need(got == pin["manifest_hash"], f"{mrel}: hash {got} != pinned {pin['manifest_hash']}")
        ids = _target_ids(m, mrel)
        _need(pin["start"] == expected_start, f"{mrel}: starts at ordinal {pin['start']}, expected {expected_start}")
        _need(len(ids) == pin["count"], f"{mrel}: {len(ids)} reads, pinned {pin['count']}")
        _need(ids == target[pin["start"]:pin["start"] + pin["count"]],
              f"{mrel}: ids are not target ordinals {pin['start']}-{pin['start'] + pin['count'] - 1} of {tgt['manifest']}")
        expected_start += pin["count"]

        b = _load(root, brel)
        j = _check_journal(b, brel, pin)
        _need(b.get("state") == "DONE" and j.get("state") == "DONE", f"{brel}: state {b.get('state')!r}/{j.get('state')!r}, expected DONE")
        _need(b.get("outcome") == "success", f"{brel}: outcome {b.get('outcome')!r}, expected 'success'")
        _need(not b.get("entries") and not j.get("items"), f"{brel}: carries items/entries; expected zero mutations")
        _need(j.get("capturesBeforePartial") is None, f"{brel}: journal still holds a partial capture list")
        caps = b.get("captures")
        _need(isinstance(caps, list) and len(caps) == len(ids), f"{brel}: {len(caps) if isinstance(caps, list) else caps!r} captures, expected {len(ids)}")
        jcaps = j.get("capturesBefore") or []
        _need(len(jcaps) == len(ids), f"{brel}: journal lists {len(jcaps)} captures, expected {len(ids)}")
        job = j.get("jobId")
        for i, (c, jc, want) in enumerate(zip(caps, jcaps, ids)):
            where = f"{brel}: capture {i}"
            _need(c.get("phase") == "before" and c.get("proc") == "jutsu.get", f"{where}: not a before jutsu.get")
            _need(c.get("ok") is True and c.get("error") is None and c.get("rows") == 1, f"{where}: read not ok/1 row")
            _need(c.get("persist") == "full" and c.get("persistOk") is True and c.get("persistError") is None,
                  f"{where}: persist {c.get('persist')!r} ok={c.get('persistOk')!r}, expected full/True")
            _need(c.get("snapshotKey") == f"{job}::before::{i}", f"{where}: snapshotKey {c.get('snapshotKey')!r}")
            _need((c.get("input") or {}).get("id") == want, f"{where}: input.id {(c.get('input') or {}).get('id')!r} != manifest {want!r}")
            data = c.get("data")
            _need(isinstance(data, dict) and data.get("id") == want, f"{where}: data.id {(data or {}).get('id')!r} != {want!r}")
            _need(isinstance(data.get("name"), str), f"{where}: record has no name")
            for k in ("proc", "input", "ok", "rows", "persist", "persistOk", "snapshotKey"):
                _need(jc.get(k) == c.get(k), f"{where}: journal summary disagrees on {k}")
            records.append({"ordinal": pin["start"] + i, "batch": pin["manifest_number"], "bundle": brel,
                            "snapshotKey": c["snapshotKey"], "at": c.get("at"), "data": data})
        batch_meta.append({
            "manifest": mrel, "manifest_number": pin["manifest_number"], "manifest_hash": pin["manifest_hash"],
            "bundle": brel, "bundle_sha256": _sha256(root, brel), "job_id": job,
            "state": b["state"], "outcome": b["outcome"], "at": b.get("at"),
            "ordinals": [pin["start"], pin["start"] + pin["count"] - 1], "captures": len(caps),
        })
    _need(expected_start == len(target), f"batches cover {expected_start} ordinals, target has {len(target)}")
    _need(len({r["data"]["id"] for r in records}) == len(records), "duplicate record ids across batches")

    # --- known name universe (diagnostic only) --------------------------------------------
    kn = sources["known_names"]
    catalog = _load(root, kn["catalog"])
    hot = _load(root, kn["hot"])
    cat_ids = {row[0] for row in catalog.get("rows", [])}
    _need(len(cat_ids) == catalog.get("count"), f"{kn['catalog']}: count {catalog.get('count')} != {len(cat_ids)} unique rows")
    hot_rows = ((hot.get("entities") or {}).get("jutsu") or {}).get("rows") or []
    hot_ids = {row[0] for row in hot_rows} - cat_ids
    known = len(cat_ids) + len(hot_ids)

    return {
        "records": records,
        "batches": batch_meta,
        "coverage": {"bundle": cov["bundle"], "bundle_sha256": _sha256(root, cov["bundle"]),
                     "manifest_hash": cov["manifest_hash"], "proc": cov["proc"], "live_rows": live_rows,
                     "known_rows_at_census": cov["known_rows_at_census"], "status": cov["status"]},
        "target": {"manifest": tgt["manifest"], "manifest_hash": tgt["manifest_hash"], "count": len(target)},
        "current_known": {"catalog": kn["catalog"], "catalog_rows": len(cat_ids), "hot": kn["hot"],
                          "hot_new_rows": len(hot_ids), "total": known},
    }


# ---------------------------------------------------------------------------------------------
# Derivation
# ---------------------------------------------------------------------------------------------
def exclusions(data: dict) -> list[str]:
    out = []
    if data.get("hidden") is not False:
        out.append("hidden" if data.get("hidden") is True else f"hidden={data.get('hidden')!r}")
    if data.get("jutsuType") not in PLAYER_TYPES:
        out.append(f"jutsuType={data.get('jutsuType')}")
    if data.get("bloodlineId"):
        out.append("bloodline-owned")
    return out


def _image(data: dict) -> str | None:
    url = data.get("image")
    if not isinstance(url, str):
        return None
    p = urllib.parse.urlsplit(url)
    return url if p.scheme == "https" and p.hostname else None


def derive(corpus: dict, sources: dict = SOURCES) -> dict:
    rows = []
    for r in corpus["records"]:
        d = r["data"]
        ex = exclusions(d)
        img = _image(d)
        if not ex and img is None:
            ex = ["no-https-image"]
        rows.append({
            "id": d["id"], "name": d["name"], "norm": normalize(d["name"]),
            "eligible": not ex, "exclusions": ex,
            "jutsuType": d.get("jutsuType"), "jutsuRank": d.get("jutsuRank"), "hidden": d.get("hidden"),
            "image": d.get("image"), "updatedAt": d.get("updatedAt"),
            "batch": r["batch"], "ordinal": r["ordinal"],
        })
    by_norm: dict[str, list[str]] = {}
    for row in rows:
        by_norm.setdefault(row["norm"], []).append(row["id"])
    ambiguous = {k: sorted(v) for k, v in by_norm.items() if len(v) > 1}

    eligible = [r for r in rows if r["eligible"]]
    by_url: dict[str, list[str]] = {}
    for r in eligible:
        by_url.setdefault(r["image"], []).append(r["id"])
    shared = [{"image": u, "ids": sorted(ids)} for u, ids in sorted(by_url.items()) if len(ids) > 1]

    cov = corpus["coverage"]
    live, known = cov["live_rows"], cov["known_rows_at_census"]
    warnings = []
    if cov["status"] == "UNRESOLVED":
        warnings.append(
            f"UNRESOLVED name-universe drift: live jutsu.getAllNames = {live} rows (#66) vs {known} repository ids "
            f"known at census time. The census covers only that known candidate set; {live - known:+d} live row(s) "
            "were never classified. Only reviewed follow-up capture evidence clears this - never a catalog count."
        )
    if ambiguous:
        warnings.append(f"{len(ambiguous)} normalized name(s) map to more than one captured id; those names never auto-resolve")

    counts = {
        "captured": len(rows),
        "eligible": len(eligible),
        "eligible_unique_image_urls": len(by_url),
        "excluded": len(rows) - len(eligible),
    }
    return {
        "schema": SCHEMA,
        "_note": "GENERATED by scripts/jutsu_art.py build from committed census bundles - never edit by hand. "
                 "Run `python3 scripts/jutsu_art.py verify` before trusting it.",
        "lookup_policy": "normalized exact match only (NFKC, curly quotes -> ASCII, whitespace collapsed, casefold); "
                         "suggestions on miss; never fuzzy auto-selection",
        "eligibility_rule": ELIGIBILITY_RULE,
        "counts": counts,
        "expected": sources["expected"],
        "coverage": {
            "live_name_rows": live, "known_name_rows_at_census": known, "drift": live - known,
            "status": cov["status"], "live_source": cov,
        },
        "warnings": warnings,
        "sources": {"target": corpus["target"], "batches": corpus["batches"]},
        "shared_images": shared,
        "ambiguous_names": ambiguous,
        "records": sorted(rows, key=lambda r: (r["norm"], r["id"])),
    }


def render(doc: dict) -> str:
    return json.dumps(doc, ensure_ascii=False, indent=1) + "\n"


def check_expected(doc: dict) -> list[str]:
    exp, got = doc["expected"], doc["counts"]
    return [f"{k}: derived {got.get(k)} != expected {v}" for k, v in exp.items() if got.get(k) != v]


def build(root: Path = ROOT, sources: dict = SOURCES) -> tuple[dict, str]:
    doc, text, _ = build_with_diagnostics(root, sources)
    return doc, text


def build_with_diagnostics(root: Path = ROOT, sources: dict = SOURCES) -> tuple[dict, str, list[str]]:
    corpus = load_corpus(root, sources)
    doc = derive(corpus, sources)
    bad = check_expected(doc)
    if bad:
        raise ProvenanceError("derived corpus does not match pinned expectations: " + "; ".join(bad))
    cur, cov = corpus["current_known"], corpus["coverage"]
    diag = [f"diagnostic: today's known jutsu ids = {cur['total']} ({cur['catalog_rows']} catalog + "
            f"{cur['hot_new_rows']} hot) vs {cov['known_rows_at_census']} at census time; "
            "this count never changes coverage status"]
    return doc, render(doc), diag


# ---------------------------------------------------------------------------------------------
# Lookup over the derived file
# ---------------------------------------------------------------------------------------------
def load_derived(root: Path = ROOT) -> dict:
    path = root / OUTPUT
    if not path.is_file():
        raise ProvenanceError(f"{OUTPUT} missing - run `python3 scripts/jutsu_art.py build`")
    doc = json.loads(path.read_text(encoding="utf-8"))
    _need(doc.get("schema") == SCHEMA, f"{OUTPUT}: schema {doc.get('schema')!r} != {SCHEMA!r}")
    recs = doc.get("records") or []
    _need(len(recs) == doc["counts"]["captured"] and sum(r["eligible"] for r in recs) == doc["counts"]["eligible"],
          f"{OUTPUT}: record list disagrees with its own counts - rebuild")
    return doc


def resolve(doc: dict, query: str, *, by_id: bool = False) -> dict:
    recs = doc["records"]
    if by_id:
        hits = [r for r in recs if r["id"] == query]
    else:
        key = normalize(query)
        hits = [r for r in recs if r["norm"] == key]
        if len(hits) > 1:
            raise ProvenanceError(f"{query!r} is ambiguous: ids {', '.join(r['id'] for r in hits)} - use --id")
    if not hits:
        raise LookupMiss(query, [] if by_id else suggest(doc, query))
    return hits[0]


def suggest(doc: dict, query: str, n: int = 8) -> list[str]:
    key = normalize(query)
    names = {r["norm"]: r["name"] for r in doc["records"]}
    out: list[str] = []
    if key:
        out += sorted(n_ for n_ in names if key in n_ or n_ in key)
        out += difflib.get_close_matches(key, sorted(names), n=n, cutoff=0.6)
    seen, picks = set(), []
    for k in out:
        if k not in seen:
            seen.add(k)
            picks.append(names[k].strip())
    return picks[:n]


def search(doc: dict, query: str, *, include_all: bool = False) -> list[dict]:
    key = normalize(query)
    return [r for r in doc["records"] if key in r["norm"] and (include_all or r["eligible"])]


def full_record(root: Path, row: dict) -> dict:
    """The captured record exactly as its bundle holds it, after full provenance verification."""
    corpus = load_corpus(root)
    for r in corpus["records"]:
        if r["data"]["id"] == row["id"]:
            return {"provenance": {k: r[k] for k in ("bundle", "batch", "ordinal", "snapshotKey", "at")}, "record": r["data"]}
    raise ProvenanceError(f"{row['id']} is in {OUTPUT} but not in the verified bundles - rebuild")


# ---------------------------------------------------------------------------------------------
# Materialize (CDN only)
# ---------------------------------------------------------------------------------------------
def check_cdn_url(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    host = (p.hostname or "").lower()
    if p.scheme != "https":
        raise ProvenanceError(f"refusing non-https URL {url!r}")
    if any(host == s or host.endswith("." + s) for s in GAME_HOST_SUFFIXES):
        raise ProvenanceError(f"refusing game host {host!r}: materialize never contacts TNR")
    if host not in CDN_HOSTS:
        raise ProvenanceError(f"refusing host {host!r}: not an allowlisted asset CDN")
    return url


def sniff(data: bytes) -> str | None:
    """Container signature only - a cheap pre-filter. It proves nothing about decodability."""
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:3] == b"\xff\xd8\xff":
        return "jpg"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    return None


_PIL_FORMATS = {"PNG": "png", "JPEG": "jpg", "GIF": "gif", "WEBP": "webp"}


def decode_image(data: bytes) -> dict:
    """Fully decode every frame with Pillow (the approved art dependency). Truncated, header-only
    or otherwise undecodable bytes raise ProvenanceError. Animated GIF/WebP are kept as-is."""
    try:
        from PIL import Image, ImageFile
    except ImportError as exc:  # pragma: no cover
        raise ProvenanceError("materialize needs Pillow: pip install pillow --break-system-packages") from exc
    import io
    if ImageFile.LOAD_TRUNCATED_IMAGES:
        raise ProvenanceError("PIL.ImageFile.LOAD_TRUNCATED_IMAGES is enabled; refusing to validate under it")
    sig = sniff(data)
    if sig is None:
        raise ProvenanceError("response is not a recognised image container")
    try:
        with Image.open(io.BytesIO(data)) as im:
            ext = _PIL_FORMATS.get(im.format)
            frames = getattr(im, "n_frames", 1)
            for i in range(frames):
                im.seek(i)
                im.load()
            size = im.size
    except ProvenanceError:
        raise
    except Exception as exc:  # UnidentifiedImageError, OSError (truncated), EOFError, SyntaxError, ...
        raise ProvenanceError(f"response does not decode as an image ({type(exc).__name__}: {exc})") from exc
    if ext != sig:
        raise ProvenanceError(f"container signature {sig!r} disagrees with decoded format {ext!r}")
    return {"ext": ext, "width": size[0], "height": size[1], "frames": frames}


class _CdnRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_cdn_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch(url: str) -> bytes:
    opener = urllib.request.build_opener(_CdnRedirects())
    with opener.open(urllib.request.Request(url, headers={"User-Agent": "tnr-tools jutsu_art"}), timeout=30) as resp:
        data = resp.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise ProvenanceError(f"{url}: larger than {MAX_IMAGE_BYTES} bytes")
    return data


INDEX_NAME = "materialized.json"


def _read_index(out: Path) -> dict:
    """The existing index, checked against the files it names. An index that does not describe
    the directory exactly is refused before any request, so nothing is ever built on drift."""
    index = out / INDEX_NAME
    if not index.exists():
        return {}
    try:
        prior = json.loads(index.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProvenanceError(f"{index}: unreadable index ({exc})") from exc
    if not isinstance(prior, dict):
        raise ProvenanceError(f"{index}: not a JSON object")
    for rid, e in prior.items():
        f = e.get("file") if isinstance(e, dict) else None
        if not isinstance(f, str) or "/" in f or "\\" in f or f.startswith(".") or not f.startswith(rid + "."):
            raise ProvenanceError(f"{index}: entry {rid!r} names an invalid file {f!r}")
        path = out / f
        if not path.is_file():
            raise ProvenanceError(f"{index}: {f} is indexed but missing")
        if hashlib.sha256(path.read_bytes()).hexdigest() != e.get("sha256"):
            raise ProvenanceError(f"{index}: {f} does not match its indexed sha256")
    return prior


def _write_temp(out: Path, data: bytes) -> Path:
    import os
    import tempfile
    fd, tmp = tempfile.mkstemp(dir=out, prefix=".jutsu_art-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    return Path(tmp)


def materialize(doc: dict, queries: list[str], out: Path, *, by_id=False, dry_run=False, fetch=_fetch) -> list[dict]:
    """All-or-nothing: every name resolves, the existing index is verified, and every image is
    fetched AND fully decoded before the directory is touched. Any failure up to that point leaves
    the previous files and index exactly as they were. Publishing then stages every file as a
    temp in the same directory and swaps them in with os.replace, index last."""
    import os
    rows, seen = [], set()
    for q in queries:  # every name resolves before any request
        row = resolve(doc, q, by_id=by_id)
        if row["id"] not in seen:
            seen.add(row["id"])
            rows.append(row)
    for row in rows:
        if not row["eligible"]:
            raise ProvenanceError(f"{row['name'].strip()!r} is not eligible ({', '.join(row['exclusions'])})")
        check_cdn_url(row["image"])
    if dry_run:
        return [{"id": r["id"], "name": r["name"], "image": r["image"], "action": "would-fetch"} for r in rows]

    prior = _read_index(out) if out.is_dir() else {}
    if out.exists() and not out.is_dir():
        raise ProvenanceError(f"{out} exists and is not a directory")

    staged = []
    for row in rows:
        data = fetch(row["image"])
        try:
            info = decode_image(data)
        except ProvenanceError as exc:
            raise ProvenanceError(f"{row['image']}: {exc}") from exc
        name = f"{row['id']}.{info['ext']}"
        old = prior.get(row["id"], {}).get("file")
        if (out / name).exists() and old != name:
            raise ProvenanceError(f"{out / name} exists but is not indexed for {row['id']}; refusing to overwrite it")
        staged.append((row, data, info, name, old))

    out.mkdir(parents=True, exist_ok=True)
    temps: list[tuple[Path, Path]] = []
    try:
        for row, data, info, name, old in staged:
            temps.append((_write_temp(out, data), out / name))
        index = dict(prior)
        results = []
        for row, data, info, name, old in staged:
            entry = {"id": row["id"], "name": row["name"], "image": row["image"], "file": name,
                     "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), **info}
            del entry["ext"]
            index[row["id"]] = entry
            results.append({**entry, "action": "fetched"})
        text = json.dumps(dict(sorted(index.items())), ensure_ascii=False, indent=1) + "\n"
        temps.append((_write_temp(out, text.encode("utf-8")), out / INDEX_NAME))
    except BaseException:
        for tmp, _ in temps:
            tmp.unlink(missing_ok=True)
        raise
    for tmp, final in temps:  # images first, index last
        os.replace(tmp, final)
    for row, data, info, name, old in staged:
        if old and old != name:  # format changed: the superseded file is no longer indexed
            (out / old).unlink(missing_ok=True)
    return results


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------
def _describe(r: dict) -> str:
    status = "eligible" if r["eligible"] else "EXCLUDED (" + ", ".join(r["exclusions"]) + ")"
    return f"{r['name'].strip()}  [{r['id']}]  {r['jutsuType']}  {status}\n  image: {r['image']}"


def _print_miss(doc: dict, miss: LookupMiss) -> None:
    print(f"no captured jutsu named {miss.query!r} (normalized exact match)", file=sys.stderr)
    if miss.suggestions:
        print("did you mean (not selected):", file=sys.stderr)
        for s in miss.suggestions:
            print(f"  {s}", file=sys.stderr)
    for w in doc.get("warnings", []):
        print(f"warning: {w}", file=sys.stderr)


def _shared_note(doc: dict, row: dict) -> str | None:
    for s in doc.get("shared_images", []):
        if row["id"] in s["ids"]:
            others = [i for i in s["ids"] if i != row["id"]]
            return f"note: this image URL is shared with {', '.join(others)}"
    return None


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help=f"derive {OUTPUT} from the pinned bundles")
    sub.add_parser("verify", help=f"re-derive and compare with {OUTPUT}")
    for name in ("lookup", "record", "image-url"):
        p = sub.add_parser(name)
        p.add_argument("query")
        p.add_argument("--id", action="store_true", help="treat query as an exact record id")
        if name == "lookup":
            p.add_argument("--json", action="store_true")
        if name == "image-url":
            p.add_argument("--any", action="store_true", help="also print URLs of excluded records")
    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--all", action="store_true", help="include excluded records")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("materialize", help="download eligible images from the asset CDN (never TNR)")
    p.add_argument("query", nargs="+")
    p.add_argument("--id", action="store_true")
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    try:
        if a.cmd == "build":
            doc, text, diag = build_with_diagnostics(root)
            (root / OUTPUT).write_text(text, encoding="utf-8")
            c = doc["counts"]
            print(f"wrote {OUTPUT}: {c['captured']} captured / {c['eligible']} eligible / "
                  f"{c['eligible_unique_image_urls']} unique image URLs")
            for w in doc["warnings"]:
                print(f"warning: {w}")
            for d in diag:
                print(d)
            return 0
        if a.cmd == "verify":
            doc, text, diag = build_with_diagnostics(root)
            path = root / OUTPUT
            current = path.read_text(encoding="utf-8") if path.is_file() else None
            c = doc["counts"]
            print(f"sources verified: {len(doc['sources']['batches'])} batch bundles, "
                  f"{c['captured']} captured / {c['eligible']} eligible / {c['eligible_unique_image_urls']} unique image URLs")
            for w in doc["warnings"]:
                print(f"warning: {w}")
            for d in diag:
                print(d)
            if current != text:
                print(f"FAIL: {OUTPUT} is {'missing' if current is None else 'stale'} - run build", file=sys.stderr)
                return 1
            print(f"OK: {OUTPUT} matches a fresh derivation byte for byte")
            return 0

        doc = load_derived(root)
        if a.cmd == "search":
            hits = search(doc, a.query, include_all=a.all)
            if a.json:
                print(json.dumps(hits, ensure_ascii=False, indent=1))
            else:
                for r in hits:
                    print(_describe(r))
                print(f"{len(hits)} match(es)", file=sys.stderr)
            return 0 if hits else 1
        if a.cmd == "materialize":
            for r in materialize(doc, a.query, a.out, by_id=a.id, dry_run=a.dry_run):
                print(f"{r['action']}: {r['name'].strip()} [{r['id']}] {r.get('file', r['image'])}")
            return 0

        row = resolve(doc, a.query, by_id=a.id)
        if a.cmd == "lookup":
            print(json.dumps(row, ensure_ascii=False, indent=1) if a.json else _describe(row))
        elif a.cmd == "record":
            print(json.dumps(full_record(root, row), ensure_ascii=False, indent=1))
        elif a.cmd == "image-url":
            if not row["eligible"] and not a.any:
                print(f"{row['name'].strip()!r} is excluded ({', '.join(row['exclusions'])}); pass --any to print anyway",
                      file=sys.stderr)
                return 1
            print(row["image"])
        note = _shared_note(doc, row)
        if note:
            print(note, file=sys.stderr)
        return 0
    except LookupMiss as miss:
        _print_miss(doc, miss)
        return 1
    except ProvenanceError as exc:
        print(f"FAIL CLOSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
