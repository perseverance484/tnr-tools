#!/usr/bin/env python3
"""Bloodright Jutsu Reference Packager.

Assembles source-verified original jutsu artwork for the approved Bloodright cohort (29 public
A/S/H bloodlines, 166 linked jutsu) into one master ZIP holding one independently uploadable ZIP
per bloodline. Brief: chatgpt/bloodright-reference-library-brief-20261016@1b3b93b
(state/prompt_bloodright_reference_library.md on that branch).

Four separate operations. Only `acquire` touches the network, only with --allow-network, and only
the allowlisted asset CDNs from scripts/jutsu_art.py. Nothing here ever contacts the game.

    inventory   offline: cohort from the pinned roster + kit dossiers, image evidence from pinned
                capture-only results bundles; per-bloodline READY / SOURCE_BLOCKED report
    acquire     CDN GETs for READY bloodlines into a checksum-indexed local cache
    pack        offline: deterministic inner + master ZIPs from verified cache bytes only
    verify      offline: re-check a built master ZIP end to end

    python3 scripts/bloodright_reference.py inventory [--write]
    python3 scripts/bloodright_reference.py acquire --pilot BR-023 --cache DIR --allow-network
    python3 scripts/bloodright_reference.py pack    --pilot BR-023 --cache DIR --out DIR
    python3 scripts/bloodright_reference.py verify  ZIP --pilot BR-023 [--cache DIR]
    python3 scripts/bloodright_reference.py build   --pilot BR-023 --cache DIR --out DIR --allow-network
                                                    (acquire + pack + verify in one step)
    (use --all instead of --pilot for the full 29-bloodline library)

Fail-closed: the full `Bloodright_Jutsu_Reference_Library.zip` is only written when 29/29
bloodlines and 166/166 images pass. A pilot is always named `..._PILOT_<ids>.zip`.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jutsu_art as ja  # noqa: E402  reused: CDN allowlist, sniff, full Pillow decode, Forge manifest hash

ROOT = Path(__file__).resolve().parent.parent
SOURCES_PATH = "state/bloodright_reference_library/sources.json"
INVENTORY_PATH = "state/bloodright_reference_library/inventory.json"
SCHEMA = "tnr.bloodright_reference/1"
FULL_STEM = "Bloodright_Jutsu_Reference_Library"
RANKS = ("A", "S", "H")
ZIP_DATE = (1980, 1, 1, 0, 0, 0)
MAX_REDIRECTS = 3
FETCH_TIMEOUT = 30
LEDGER = "ledger.json"
PROVENANCE_NOTE = ("Bytes are exactly as served by the asset CDN for the image URL in a verified jutsu.get record. "
                   "A CDN rendition is not proven byte-identical to the uploader's original file.")

ProvenanceError = ja.ProvenanceError


def _need(cond: bool, msg: str) -> None:
    if not cond:
        raise ProvenanceError(msg)


def canonical_json(obj) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# ---------------------------------------------------------------------------------------------
# Repository access (offline). Tests substitute a dict-backed source.
# ---------------------------------------------------------------------------------------------
class RepoSource:
    def __init__(self, root: Path = ROOT):
        self.root = root

    def file(self, rel: str) -> bytes:
        p = self.root / rel
        _need(p.is_file(), f"{rel}: missing")
        return p.read_bytes()

    def _git(self, *args: str) -> bytes:
        try:
            return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True).stdout
        except subprocess.CalledProcessError as exc:
            raise ProvenanceError(f"git {' '.join(args)} failed ({exc.stderr.decode(errors='replace').strip()}); "
                                  "fetch the pinned roster branch first") from exc

    def blob(self, ref: str, path: str) -> bytes:
        return self._git("cat-file", "blob", f"{ref}:{path}")

    def listdir(self, ref: str, path: str) -> list[str]:
        return [n.rsplit("/", 1)[-1] for n in self._git("ls-tree", "--name-only", f"{ref}:{path}").decode().split()]


def load_sources(src) -> dict:
    try:
        return json.loads(src.file(SOURCES_PATH))
    except json.JSONDecodeError as exc:
        raise ProvenanceError(f"{SOURCES_PATH}: not JSON ({exc})") from exc


# ---------------------------------------------------------------------------------------------
# Cohort: pinned roster + kit dossiers
# ---------------------------------------------------------------------------------------------
def load_cohort(src, sources: dict) -> list[dict]:
    r = sources["roster"]
    raw = src.blob(r["ref"], r["path"])
    _need(git_blob_sha1(raw) == r["blob"], f"{r['path']}@{r['ref'][:7]}: blob {git_blob_sha1(raw)} != pinned {r['blob']}")
    roster = json.loads(raw)
    records = roster.get("records")
    _need(isinstance(records, list), "roster: no records list")
    excluded = set(roster.get("excluded_ids") or []) | set(roster.get("deferred_ids") or [])

    sel = [x for x in records
           if x.get("hidden") is False and (
               (x.get("owner_decision") == "INCLUDE" and x.get("rank") in RANKS) or x.get("owner_decision") == "REFERENCE")]
    _need(sum(1 for x in sel if x.get("owner_decision") == "REFERENCE") == 1, "roster: expected exactly one REFERENCE record")

    kits = {}
    for name in src.listdir(r["ref"], r["kits_dir"]):
        if name.endswith(".json"):
            k = json.loads(src.blob(r["ref"], f"{r['kits_dir']}/{name}"))
            if isinstance(k, dict) and k.get("bloodline_id"):
                _need(k["bloodline_id"] not in kits, f"kits: two dossiers for bloodline {k['bloodline_id']}")
                kits[k["bloodline_id"]] = {**k, "_path": f"{r['kits_dir']}/{name}"}

    cohort, seen_j, seen_b = [], set(), set()
    for x in sel:
        bid = x["bloodline_id"]
        _need(bid not in excluded, f"{x['review_id']}: bloodline {bid} is in excluded/deferred ids")
        _need(bid not in seen_b, f"roster: duplicate bloodline {bid}")
        seen_b.add(bid)
        _need(not x.get("hidden_jutsu_ids"), f"{x['review_id']}: has hidden jutsu; out of scope for a public pack")
        ids = x.get("public_jutsu_ids") or []
        _need(len(ids) == x.get("public_jutsu_count"), f"{x['review_id']}: public_jutsu_count disagrees with ids")
        _need(len(ids) > 0, f"{x['review_id']}: no linked jutsu")
        kit = kits.get(bid)
        _need(kit is not None, f"{x['review_id']}: no kit dossier for bloodline {bid}")
        _need(kit.get("review_id") == x["review_id"] and kit.get("rank") == x["rank"],
              f"{kit['_path']}: review_id/rank disagree with roster")
        kit_public = [j for j in kit.get("jutsu") or [] if j.get("visibility") == "public"]
        _need([j["id"] for j in kit_public] == ids, f"{kit['_path']}: public jutsu ids disagree with roster {x['review_id']}")
        members = []
        for j in kit_public:
            _need(j["id"] not in seen_j, f"jutsu {j['id']} linked to more than one cohort bloodline")
            seen_j.add(j["id"])
            members.append({"id": j["id"], "kit_name": j.get("name"), "kit_type": j.get("jutsuType")})
        cohort.append({"review_id": x["review_id"], "bloodline_id": bid, "name": x["name"], "rank": x["rank"],
                       "disposition": x["owner_decision"], "kit": kit["_path"], "jutsu": members})

    exp = sources["expected"]
    ranks = {k: sum(1 for b in cohort if b["rank"] == k) for k in RANKS}
    _need(len(cohort) == exp["bloodlines"], f"cohort has {len(cohort)} bloodlines, pinned {exp['bloodlines']}")
    _need(ranks == exp["ranks"], f"cohort ranks {ranks}, pinned {exp['ranks']}")
    _need(len(seen_j) == exp["jutsu"], f"cohort has {len(seen_j)} jutsu, pinned {exp['jutsu']}")
    return sorted(cohort, key=lambda b: b["review_id"])


# ---------------------------------------------------------------------------------------------
# Evidence: pinned capture-only results bundles
# ---------------------------------------------------------------------------------------------
EVIDENCE_PROCS = ("jutsu.get", "bloodline.get")


def load_evidence(src, sources: dict) -> dict:
    """{"jutsu": {id: [evidence]}, "bloodline": {id: [evidence]}} from every pinned bundle."""
    out = {"jutsu": {}, "bloodline": {}}
    for pin in sources["captures"]:
        mrel, brel = pin["manifest"], pin["bundle"]
        manifest = json.loads(src.file(mrel))
        _need(ja.manifest_hash(manifest) == pin["manifest_hash"], f"{mrel}: hash {ja.manifest_hash(manifest)} != pinned {pin['manifest_hash']}")
        _need(not manifest.get("items") and not (manifest.get("capture") or {}).get("after"), f"{mrel}: not capture-only")
        planned = (manifest.get("capture") or {}).get("before") or []
        raw = src.file(brel)
        _need(sha256(raw) == pin["bundle_sha256"], f"{brel}: sha256 {sha256(raw)} != pinned {pin['bundle_sha256']}")
        b = json.loads(raw)
        j = b.get("journal") or {}
        _need(j.get("manifestPath") == mrel and j.get("manifestHash") == pin["manifest_hash"]
              and j.get("manifestNumber") == pin["manifest_number"], f"{brel}: journal names a different manifest")
        _need(j.get("jobId") == pin["job_id"], f"{brel}: job {j.get('jobId')!r} != pinned {pin['job_id']!r}")
        _need(b.get("state") == "DONE" and j.get("state") == "DONE" and b.get("outcome") == "success", f"{brel}: job not DONE/success")
        _need(not b.get("entries") and not j.get("items"), f"{brel}: carries items/entries; expected zero mutations")
        _need(j.get("capturesBeforePartial") is None, f"{brel}: journal still holds a partial capture list")
        caps = b.get("captures")
        _need(isinstance(caps, list) and len(caps) == len(planned), f"{brel}: capture count disagrees with {mrel}")
        jcaps = j.get("capturesBefore") or []
        _need(len(jcaps) == len(caps), f"{brel}: journal capture count disagrees")
        for i, (c, jc, want) in enumerate(zip(caps, jcaps, planned)):
            where = f"{brel}: capture {i}"
            proc, wid = want.get("proc"), (want.get("input") or {}).get("id")
            _need(proc in EVIDENCE_PROCS and want.get("persist") == "full", f"{mrel}: capture {i} is not a full {'/'.join(EVIDENCE_PROCS)} read")
            _need(c.get("phase") == "before" and c.get("proc") == proc and (c.get("input") or {}).get("id") == wid,
                  f"{where}: does not match its manifest read")
            _need(c.get("ok") is True and c.get("error") is None and c.get("rows") == 1, f"{where}: read not ok/1 row")
            _need(c.get("persist") == "full" and c.get("persistOk") is True and c.get("persistError") is None, f"{where}: full body not persisted")
            _need(c.get("snapshotKey") == f"{pin['job_id']}::before::{i}", f"{where}: snapshotKey {c.get('snapshotKey')!r}")
            for k in ("proc", "input", "ok", "rows", "persist", "persistOk", "snapshotKey"):
                _need(jc.get(k) == c.get(k), f"{where}: journal summary disagrees on {k}")
            d = c.get("data")
            _need(isinstance(d, dict) and d.get("id") == wid, f"{where}: record id {(d or {}).get('id')!r} != requested {wid!r}")
            ev = {"bundle": brel, "bundle_sha256": pin["bundle_sha256"], "manifest": mrel, "manifest_hash": pin["manifest_hash"],
                  "job_id": pin["job_id"], "capture_index": i, "snapshot_key": c["snapshotKey"], "read_at": c.get("at"),
                  "input": {"proc": proc, "id": wid},
                  "record": {k: d.get(k) for k in ("id", "name", "jutsuType", "bloodlineId", "hidden", "rank", "image")}}
            out["jutsu" if proc == "jutsu.get" else "bloodline"].setdefault(wid, []).append(ev)
    return out


def check_url(url) -> str:
    """jutsu_art's CDN policy, tightened: no credentials, port, query or fragment, ASCII only."""
    _need(isinstance(url, str) and url, "image is missing or not a string")
    _need(url.isascii() and not any(ch.isspace() or ord(ch) < 32 for ch in url), "image URL has non-ASCII or whitespace")
    p = urllib.parse.urlsplit(url)
    _need(p.username is None and p.password is None, "image URL carries credentials")
    _need(p.port is None, "image URL names a port")
    _need(not p.query and not p.fragment, "image URL has a query or fragment")
    _need(p.path.startswith("/") and ".." not in p.path.split("/"), "image URL path is not plain")
    ja.check_cdn_url(url)
    return url


def plan(cohort: list[dict], evidence: dict) -> dict:
    blood = []
    for b in cohort:
        rows, blocked = [], 0
        for m in b["jutsu"]:
            evs = evidence["jutsu"].get(m["id"], [])
            row = {"id": m["id"], "kit_name": m["kit_name"], "kit_type": m["kit_type"], "status": "READY", "problems": [], "warnings": []}
            if not evs:
                row["status"] = "MISSING_CAPTURE"
                row["problems"].append("no verified jutsu.get persist:full read in any pinned bundle")
            else:
                images = sorted({e["record"]["image"] for e in evs if isinstance(e["record"]["image"], str)})
                if len(images) > 1:
                    row["status"] = "AMBIGUOUS"
                    row["problems"].append(f"pinned captures disagree on image: {images}")
                ev = max(evs, key=lambda e: (e["read_at"] or "", e["bundle"], e["capture_index"]))
                rec = ev["record"]
                row.update({"name": rec["name"], "jutsu_type": rec["jutsuType"], "image": rec["image"], "evidence": ev,
                            "evidence_reads": len(evs)})
                if rec["bloodlineId"] != b["bloodline_id"]:
                    row["status"] = "BLOODLINE_MISMATCH"
                    row["problems"].append(f"live bloodlineId {rec['bloodlineId']!r} != {b['bloodline_id']!r}")
                if rec["hidden"] is not False:
                    row["status"] = "NOT_PUBLIC"
                    row["problems"].append(f"live hidden={rec['hidden']!r}")
                try:
                    check_url(rec["image"])
                except ProvenanceError as exc:
                    row["status"] = "NULL_IMAGE" if not rec["image"] else "BAD_URL"
                    row["problems"].append(str(exc))
                if rec["name"] != m["kit_name"]:
                    row["warnings"].append(f"live name {rec['name']!r} differs from kit name {m['kit_name']!r}")
                if rec["jutsuType"] != m["kit_type"]:
                    row["warnings"].append(f"live jutsuType {rec['jutsuType']!r} differs from kit {m['kit_type']!r}")
            blocked += row["status"] != "READY"
            rows.append(row)
        ident = {"status": "NOT_CAPTURED"}
        bevs = evidence["bloodline"].get(b["bloodline_id"], [])
        if bevs:
            ev = max(bevs, key=lambda e: (e["read_at"] or "", e["bundle"], e["capture_index"]))
            ident = {"status": "READY", "image": ev["record"]["image"], "evidence": ev}
            try:
                check_url(ev["record"]["image"])
            except ProvenanceError as exc:
                ident = {"status": "UNUSABLE", "reason": str(exc), "evidence": ev}
        blood.append({**{k: b[k] for k in ("review_id", "bloodline_id", "name", "rank", "disposition", "kit")},
                      "status": "READY" if not blocked else "SOURCE_BLOCKED", "jutsu_count": len(rows),
                      "ready_count": len(rows) - blocked, "jutsu": rows, "identity": ident})
    ready = [b for b in blood if b["status"] == "READY"]
    return {"schema": SCHEMA + "/inventory", "bloodlines": blood,
            "summary": {"bloodlines": len(blood), "bloodlines_ready": len(ready),
                        "jutsu": sum(b["jutsu_count"] for b in blood),
                        "jutsu_ready": sum(b["ready_count"] for b in blood),
                        "missing": [{"review_id": b["review_id"], "bloodline": b["name"], "id": j["id"],
                                     "kit_name": j["kit_name"], "status": j["status"], "problems": j["problems"]}
                                    for b in blood for j in b["jutsu"] if j["status"] != "READY"]}}


def inventory(src=None) -> tuple[dict, dict]:
    src = src or RepoSource()
    sources = load_sources(src)
    inv = plan(load_cohort(src, sources), load_evidence(src, sources))
    inv["source_lock"] = {"sources_sha256": sha256(src.file(SOURCES_PATH)), "brief": sources["brief"],
                          "roster": sources["roster"], "captures": sources["captures"]}
    return inv, sources


def select(inv: dict, review_ids: list[str] | None) -> list[dict]:
    """None means the full library."""
    by = {b["review_id"]: b for b in inv["bloodlines"]}
    if review_ids is None:
        return list(inv["bloodlines"])
    _need(len(set(review_ids)) == len(review_ids), "duplicate review id in selection")
    for r in review_ids:
        _need(r in by, f"{r} is not in the approved cohort")
    return [by[r] for r in sorted(review_ids)]


# ---------------------------------------------------------------------------------------------
# Acquire (the only networked step; CDN only)
# ---------------------------------------------------------------------------------------------
class _Redirects(urllib.request.HTTPRedirectHandler):
    max_redirections = MAX_REDIRECTS

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch(url: str) -> bytes:
    check_url(url)
    opener = urllib.request.build_opener(_Redirects())  # no cookie processor: no cookies are sent or kept
    req = urllib.request.Request(url, headers={"User-Agent": "tnr-tools bloodright_reference", "Accept": "image/*"})
    with opener.open(req, timeout=FETCH_TIMEOUT) as resp:
        _need(resp.status == 200, f"HTTP {resp.status}")
        check_url(resp.geturl())
        data = resp.read(ja.MAX_IMAGE_BYTES + 1)
    _need(len(data) <= ja.MAX_IMAGE_BYTES, f"larger than {ja.MAX_IMAGE_BYTES} bytes")
    return data


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".br-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def image_info(data: bytes) -> dict:
    info = ja.decode_image(data)
    _need(info["frames"] == 1, f"{info['frames']}-frame image; reference art must be a single frame")
    _need(info["width"] > 0 and info["height"] > 0, "empty image")
    return {"format": info["ext"], "width": info["width"], "height": info["height"], "frames": 1,
            "bytes": len(data), "sha256": sha256(data)}


def read_cache(cache: Path) -> dict:
    """The ledger, with every object it names re-hashed and re-decoded. Tamper is fatal."""
    p = cache / LEDGER
    if not p.exists():
        return {}
    try:
        ledger = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProvenanceError(f"{p}: unreadable ledger ({exc})") from exc
    _need(isinstance(ledger, dict), f"{p}: not an object")
    for url, e in ledger.items():
        check_url(url)
        _need(isinstance(e, dict) and re.fullmatch(r"[0-9a-f]{64}", str(e.get("sha256"))), f"{p}: bad entry for {url}")
        data = object_bytes(cache, e["sha256"])
        info = image_info(data)
        for k in ("format", "width", "height", "bytes", "sha256"):
            _need(info[k] == e.get(k), f"{p}: cached object for {url} disagrees on {k}")
    return ledger


def object_bytes(cache: Path, digest: str) -> bytes:
    f = cache / "objects" / f"{digest}.bin"
    _need(f.is_file(), f"cache object {digest} is missing")
    data = f.read_bytes()
    _need(sha256(data) == digest, f"cache object {digest} does not match its name (tampered)")
    return data


def acquire(inv: dict, review_ids: list[str] | None, cache: Path, *, fetch=_fetch, recheck=False,
            identity=True, now=None) -> dict:
    sel = select(inv, review_ids)
    blocked = [b["review_id"] for b in sel if b["status"] != "READY"]
    _need(not blocked, f"SOURCE_BLOCKED, nothing fetched: {', '.join(blocked)} (run inventory)")
    need = sorted({j["image"] for b in sel for j in b["jutsu"]})
    ident = sorted({b["identity"]["image"] for b in sel if identity and b["identity"]["status"] == "READY"} - set(need))
    for u in need + ident:
        check_url(u)
    ledger = read_cache(cache) if cache.exists() else {}
    stamp = (now or (lambda: _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))()
    report = {"cdn_gets": 0, "game_requests": 0, "fetched": [], "cached": [], "identity_failed": []}

    def get(url):
        report["cdn_gets"] += 1
        data = fetch(url)
        return data, image_info(data)

    staged = {}
    for url in need:  # all-or-nothing for required jutsu images: nothing is written on any failure
        if url in ledger and not recheck:
            report["cached"].append(url)
            continue
        try:
            data, info = get(url)
        except (ProvenanceError, urllib.error.URLError, OSError, ValueError) as exc:
            raise ProvenanceError(f"{url}: {exc}; nothing written") from exc
        if url in ledger and ledger[url]["sha256"] != info["sha256"]:
            raise ProvenanceError(f"{url}: REMOTE BYTES CHANGED (cached {ledger[url]['sha256']}, served {info['sha256']}); "
                                  "nothing written, existing cache kept")
        staged[url] = (data, info)
    for url in ident:  # optional: a failure is reported, never fatal
        if url in ledger and not recheck:
            report["cached"].append(url)
            continue
        try:
            data, info = get(url)
            if url in ledger and ledger[url]["sha256"] != info["sha256"]:
                raise ProvenanceError(f"remote bytes changed (cached {ledger[url]['sha256']}, served {info['sha256']})")
            staged[url] = (data, info)
        except Exception as exc:  # noqa: BLE001
            report["identity_failed"].append({"url": url, "error": f"{type(exc).__name__}: {exc}"})
    new = dict(ledger)
    for url, (data, info) in staged.items():
        _atomic_write(cache / "objects" / f"{info['sha256']}.bin", data)
        prev = ledger.get(url, {})
        new[url] = {**info, "first_fetched_at": prev.get("first_fetched_at", stamp), "last_verified_at": stamp}
        report["fetched"].append(url)
    if staged:
        _atomic_write(cache / LEDGER, canonical_json(dict(sorted(new.items()))))  # ledger last
    return report


# ---------------------------------------------------------------------------------------------
# Pack (offline, deterministic)
# ---------------------------------------------------------------------------------------------
_RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(10)), *(f"lpt{i}" for i in range(10))}


def slug(text: str, limit: int = 40) -> str:
    s = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:limit].strip("_")
    return s or "untitled"


def check_member(name: str) -> str:
    _need(name.isascii() and all(32 < ord(c) < 127 for c in name), f"zip entry {name!r}: not plain printable ASCII")
    _need(not name.startswith("/") and "\\" not in name and ":" not in name, f"zip entry {name!r}: absolute or device path")
    parts = name.rstrip("/").split("/")
    for p in parts:
        _need(p and p not in (".", "..") and not p.endswith(".") and p.split(".")[0].lower() not in _RESERVED,
              f"zip entry {name!r}: unsafe path segment {p!r}")
    _need(len(name) <= 180, f"zip entry {name!r}: too long")
    return name


def build_zip(entries: list[tuple[str, bytes | None]]) -> bytes:
    """Fixed order, timestamps, permissions; STORED (images are already compressed). None = directory."""
    seen = set()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as z:
        for name, data in entries:
            check_member(name)
            _need(name.casefold() not in seen, f"zip entry {name!r} collides case-insensitively")
            seen.add(name.casefold())
            zi = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            zi.create_system = 3
            zi.compress_type = zipfile.ZIP_STORED
            if data is None:
                _need(name.endswith("/"), f"directory entry {name!r} must end with /")
                zi.external_attr = (0o40755 << 16) | 0x10
                z.writestr(zi, b"")
            else:
                zi.external_attr = 0o100644 << 16
                z.writestr(zi, data)
    return buf.getvalue()


def inner_name(b: dict) -> str:
    return f"{b['review_id']}_{slug(b['name'])}.zip"


def stem_for(review_ids: list[str] | None) -> str:
    return FULL_STEM if review_ids is None else f"{FULL_STEM}_PILOT_{'_'.join(sorted(review_ids))}"


INNER_README = """# {review_id} {ascii_name} - jutsu reference pack

Bloodline: {name} (rank {rank}, id `{bloodline_id}`)
Jutsu images: {count}

`images/` holds the original artwork for every approved linked jutsu of this bloodline, one file
per jutsu, named `<jutsu-id>_<name>.<ext>`. `manifest.json` gives each image's display name,
jutsu type, the verified capture it came from, its format, dimensions, byte length and SHA-256.
{identity_line}
How to use in Art Studio: upload this ZIP. The Studio must unpack it and attach one or two
selected images to each image-generation conversation; uploading the ZIP to an image generator
by itself is not proof the images were read.

{provenance}
"""


def build_inner(b: dict, ledger: dict, cache: Path, source_lock: dict) -> tuple[bytes, dict]:
    files, rows = [], []
    for j in b["jutsu"]:
        _need(j["status"] == "READY", f"{b['review_id']} {j['id']}: {j['status']}")
        e = ledger.get(j["image"])
        _need(e is not None, f"{b['review_id']} {j['id']}: image not in cache; run acquire")
        data = object_bytes(cache, e["sha256"])
        info = image_info(data)
        _need(info["sha256"] == e["sha256"], f"{j['id']}: cache disagrees with ledger")
        fname = f"images/{j['id']}_{slug(j['name'])}.{info['format']}"
        files.append((fname, data))
        ev = j["evidence"]
        rows.append({"jutsu_id": j["id"], "name": j["name"], "jutsu_type": j["jutsu_type"], "file": fname,
                     "image_url": j["image"], "format": info["format"], "width": info["width"], "height": info["height"],
                     "bytes": info["bytes"], "sha256": info["sha256"], "warnings": j["warnings"],
                     "source": {k: ev[k] for k in ("bundle", "bundle_sha256", "manifest", "manifest_hash", "job_id",
                                                    "capture_index", "snapshot_key", "read_at", "input")}})
    identity = {"status": "NOT_INCLUDED", "reason": "no verified bloodline.get image in the cache"}
    if b["identity"]["status"] == "READY" and b["identity"]["image"] in ledger:
        url = b["identity"]["image"]
        data = object_bytes(cache, ledger[url]["sha256"])
        info = image_info(data)
        fname = f"identity/{b['bloodline_id']}_{slug(b['name'])}.{info['format']}"
        files.append((fname, data))
        ev = b["identity"]["evidence"]
        identity = {"status": "INCLUDED", "file": fname, "image_url": url, "format": info["format"], "width": info["width"],
                    "height": info["height"], "bytes": info["bytes"], "sha256": info["sha256"],
                    "source": {k: ev[k] for k in ("bundle", "bundle_sha256", "manifest", "manifest_hash", "job_id",
                                                   "capture_index", "snapshot_key", "read_at", "input")}}
    elif b["identity"]["status"] != "READY":
        identity = {"status": "NOT_INCLUDED", "reason": f"identity {b['identity']['status']}"}
    manifest = {"schema": SCHEMA + "/bloodline_pack", "review_id": b["review_id"],
                "bloodline": {"id": b["bloodline_id"], "name": b["name"], "rank": b["rank"]},
                "approved_jutsu_count": len(b["jutsu"]), "packaged_jutsu_count": len(rows), "jutsu": rows,
                "identity": identity, "provenance_note": PROVENANCE_NOTE, "source_lock": source_lock}
    readme = INNER_README.format(
        review_id=b["review_id"], ascii_name=slug(b["name"]).replace("_", " "), name=b["name"], rank=b["rank"],
        bloodline_id=b["bloodline_id"], count=len(rows), provenance=PROVENANCE_NOTE,
        identity_line=("\nThe bloodline's own identity image is in `identity/` (optional; for context only).\n"
                       if identity["status"] == "INCLUDED" else ""))
    entries = [("README.md", readme.encode("utf-8")), ("manifest.json", canonical_json(manifest)), ("images/", None)]
    entries += sorted((f for f in files if f[0].startswith("images/")), key=lambda f: f[0])
    idf = [f for f in files if f[0].startswith("identity/")]
    if idf:
        entries += [("identity/", None)] + idf
    return build_zip(entries), manifest


OUTER_README = """# {title}

{status_line}

## On Android

1. Download `{stem}.zip`.
2. Extract it once. You get one folder, `{stem}`, with `BLOODLINE_PACKS/` inside.
3. When you start a bloodline in Art Studio, upload just that bloodline's ZIP from
   `BLOODLINE_PACKS/` (for example `{example}`). Do not extract the inner ZIPs.

## Contents

{table}

`BLOODLINE_INDEX.json` lists every pack with its rank, approved and packaged jutsu counts,
SHA-256 and the source lock. `SHA256SUMS.txt` covers every pack plus this README and the index.

{provenance}
"""


def pack(inv: dict, review_ids: list[str] | None, cache: Path, out_dir: Path) -> dict:
    """Builds in memory, verifies the built bytes, then atomically places the one output file.
    A pre-existing output is replaced only after the new archive passes verify()."""
    sel = select(inv, review_ids)
    if review_ids is None:
        s = inv["summary"]
        _need(s["bloodlines_ready"] == s["bloodlines"] and s["jutsu_ready"] == s["jutsu"],
              f"full library refused: {s['bloodlines_ready']}/{s['bloodlines']} bloodlines and "
              f"{s['jutsu_ready']}/{s['jutsu']} jutsu are source-verified")
    blocked = [b["review_id"] for b in sel if b["status"] != "READY"]
    _need(not blocked, f"SOURCE_BLOCKED: {', '.join(blocked)}")
    ledger = read_cache(cache)
    stem = stem_for(review_ids)
    lock = inv["source_lock"]
    packs, index = [], []
    for b in sel:
        data, man = build_inner(b, ledger, cache, lock)
        name = inner_name(b)
        packs.append((f"{stem}/BLOODLINE_PACKS/{name}", data))
        index.append({"review_id": b["review_id"], "bloodline_id": b["bloodline_id"], "name": b["name"], "rank": b["rank"],
                      "zip": f"BLOODLINE_PACKS/{name}", "approved_jutsu_count": man["approved_jutsu_count"],
                      "packaged_jutsu_count": man["packaged_jutsu_count"], "identity": man["identity"]["status"],
                      "bytes": len(data), "sha256": sha256(data)})
    scope = "FULL" if review_ids is None else "PILOT"
    idx = {"schema": SCHEMA + "/index", "scope": scope, "status": "VERIFIED_COMPLETE" if scope == "FULL" else "PILOT_NOT_FULL_LIBRARY",
           "bloodlines": len(index), "jutsu": sum(r["packaged_jutsu_count"] for r in index),
           "full_library_expected": {"bloodlines": inv["summary"]["bloodlines"], "jutsu": inv["summary"]["jutsu"]},
           "packs": index, "source_lock": lock, "provenance_note": PROVENANCE_NOTE}
    title = ("Bloodright Jutsu Reference Library" if scope == "FULL"
             else f"Bloodright Jutsu Reference Library - PILOT ({', '.join(r['review_id'] for r in index)})")
    status_line = (f"Complete: {idx['bloodlines']} bloodline packs, {idx['jutsu']} jutsu images, all verified."
                   if scope == "FULL" else
                   f"PILOT ONLY - {idx['bloodlines']} of {inv['summary']['bloodlines']} bloodlines, {idx['jutsu']} of "
                   f"{inv['summary']['jutsu']} jutsu. This is not the full library.")
    table = "\n".join(f"- `{r['zip'].split('/')[-1]}` - {r['name']} ({r['rank']}), {r['packaged_jutsu_count']} jutsu"
                      for r in index)
    readme = OUTER_README.format(title=title, status_line=status_line, stem=stem, example=index[0]["zip"].split("/")[-1],
                                 table=table, provenance=PROVENANCE_NOTE).encode("utf-8")
    idx_bytes = canonical_json(idx)
    sums = "".join(f"{sha256(d)}  {n[len(stem) + 1:]}\n" for n, d in
                   sorted([(f"{stem}/BLOODLINE_INDEX.json", idx_bytes), (f"{stem}/README.md", readme)] + packs))
    entries = [(f"{stem}/", None), (f"{stem}/README.md", readme), (f"{stem}/BLOODLINE_INDEX.json", idx_bytes),
               (f"{stem}/SHA256SUMS.txt", sums.encode()), (f"{stem}/BLOODLINE_PACKS/", None)] + packs
    archive = build_zip(entries)
    report = verify_bytes(archive, inv, review_ids, cache)  # never place an archive that does not verify
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / f"{stem}.zip"
    _atomic_write(final, archive)
    return {**report, "path": str(final)}


# ---------------------------------------------------------------------------------------------
# Verify (offline)
# ---------------------------------------------------------------------------------------------
def _open_zip(data: bytes, what: str) -> zipfile.ZipFile:
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise ProvenanceError(f"{what}: not a ZIP ({exc})") from exc
    names = z.namelist()
    _need(len(names) == len(set(names)), f"{what}: duplicate entries")
    _need(len({n.casefold() for n in names}) == len(names), f"{what}: case-insensitive name collision")
    for info in z.infolist():
        check_member(info.filename)
        mode = info.external_attr >> 16
        _need((mode & 0o170000) != 0o120000, f"{what}: {info.filename} is a symlink")
    bad = z.testzip()
    _need(bad is None, f"{what}: CRC failure in {bad}")
    return z


def verify_bytes(archive: bytes, inv: dict, review_ids: list[str] | None, cache: Path | None = None) -> dict:
    sel = select(inv, review_ids)
    if review_ids is None:
        _need(len(sel) == inv["summary"]["bloodlines"], "full verify needs every cohort bloodline")
    stem = stem_for(review_ids)
    z = _open_zip(archive, "master")
    names = set(z.namelist())
    expected = {f"{stem}/", f"{stem}/README.md", f"{stem}/BLOODLINE_INDEX.json", f"{stem}/SHA256SUMS.txt",
                f"{stem}/BLOODLINE_PACKS/"} | {f"{stem}/BLOODLINE_PACKS/{inner_name(b)}" for b in sel}
    _need(names == expected, f"master layout mismatch: extra {sorted(names - expected)}, missing {sorted(expected - names)}")
    _need({n.split("/")[0] for n in names} == {stem}, "master must extract to exactly one top-level folder")
    sums = {}
    for line in z.read(f"{stem}/SHA256SUMS.txt").decode().splitlines():
        d, n = line.split("  ", 1)
        sums[n] = d
    covered = {n[len(stem) + 1:] for n in expected if not n.endswith("/")} - {"SHA256SUMS.txt"}
    _need(set(sums) == covered, "SHA256SUMS.txt does not cover exactly the packs, README and index")
    for n, d in sums.items():
        _need(sha256(z.read(f"{stem}/{n}")) == d, f"SHA256SUMS mismatch for {n}")
    idx = json.loads(z.read(f"{stem}/BLOODLINE_INDEX.json"))
    _need(idx["scope"] == ("FULL" if review_ids is None else "PILOT"), "index scope mismatch")
    _need([p["review_id"] for p in idx["packs"]] == [b["review_id"] for b in sel], "index lists the wrong bloodlines")
    _need(idx["source_lock"] == inv["source_lock"], "index source lock differs from the current inventory")
    ledger = read_cache(cache) if cache is not None else None
    total = 0
    for b, p in zip(sel, idx["packs"]):
        data = z.read(f"{stem}/{p['zip']}")
        _need(sha256(data) == p["sha256"] and len(data) == p["bytes"], f"{p['zip']}: index hash/length mismatch")
        inner = _open_zip(data, p["zip"])
        man = json.loads(inner.read("manifest.json"))
        _need(man["review_id"] == b["review_id"] and man["bloodline"]["id"] == b["bloodline_id"], f"{p['zip']}: wrong bloodline")
        ids = [r["jutsu_id"] for r in man["jutsu"]]
        _need(ids == [j["id"] for j in b["jutsu"]], f"{p['zip']}: jutsu ids differ from the approved membership")
        _need(man["approved_jutsu_count"] == man["packaged_jutsu_count"] == len(ids) == p["packaged_jutsu_count"]
              == p["approved_jutsu_count"], f"{p['zip']}: counts disagree")
        want = {"README.md", "manifest.json", "images/"} | {r["file"] for r in man["jutsu"]}
        if man["identity"]["status"] == "INCLUDED":
            want |= {"identity/", man["identity"]["file"]}
        _need(set(inner.namelist()) == want, f"{p['zip']}: unexpected or missing entries")
        rows = man["jutsu"] + ([man["identity"]] if man["identity"]["status"] == "INCLUDED" else [])
        for j, r in zip(b["jutsu"] + [b["identity"]], rows):
            img = inner.read(r["file"])
            info = image_info(img)
            _need(info["sha256"] == r["sha256"] and info["bytes"] == r["bytes"], f"{r['file']}: bytes differ from manifest")
            _need((info["format"], info["width"], info["height"]) == (r["format"], r["width"], r["height"]), f"{r['file']}: format/size mismatch")
            _need(r["file"].endswith("." + info["format"]), f"{r['file']}: extension is not the decoded format")
            _need(r["image_url"] == j["image"], f"{r['file']}: URL differs from verified evidence")
            if ledger is not None:
                _need(ledger.get(r["image_url"], {}).get("sha256") == info["sha256"], f"{r['file']}: bytes differ from acquired cache")
        total += len(ids)
    if review_ids is None:
        _need(len(sel) == inv["summary"]["bloodlines"] and total == inv["summary"]["jutsu"], "full library incomplete")
    return {"stem": stem, "scope": idx["scope"], "bloodlines": len(sel), "jutsu": total, "sha256": sha256(archive),
            "bytes": len(archive), "verified": True}


MAX_READS_PER_MANIFEST = 100  # the #68-#74 census ran 100 full jutsu.get reads per Forge job cleanly


def capture_manifests(inv: dict, start: int, *, identity=True, limit=MAX_READS_PER_MANIFEST) -> list[tuple[str, dict]]:
    """Capture-only Forge manifests for every SOURCE_BLOCKED bloodline whose gap is a missing
    capture: one jutsu.get persist:"full" per approved member (+ one optional bloodline.get),
    whole bloodlines per manifest, at most `limit` reads each. Returns [(push path, manifest)].
    Any other gap (mismatch, bad URL, ambiguity) needs a human decision and is refused here."""
    todo = [b for b in inv["bloodlines"] if b["status"] != "READY"]
    for b in todo:
        odd = [j for j in b["jutsu"] if j["status"] not in ("READY", "MISSING_CAPTURE")]
        _need(not odd, f"{b['review_id']}: {', '.join(j['id'] + ' ' + j['status'] for j in odd)} needs a decision, not a recapture")
    groups, cur = [], []
    for b in todo:
        reads = [{"proc": "jutsu.get", "input": {"id": j["id"]}, "persist": "full"} for j in b["jutsu"]]
        if identity:
            reads.append({"proc": "bloodline.get", "input": {"id": b["bloodline_id"]}, "persist": "full"})
        _need(len(reads) <= limit, f"{b['review_id']}: {len(reads)} reads exceed the per-manifest limit")
        if cur and sum(len(r) for _, r in cur) + len(reads) > limit:
            groups.append(cur)
            cur = []
        cur.append((b, reads))
    if cur:
        groups.append(cur)
    lock = inv["source_lock"]
    out = []
    for n, g in enumerate(groups):
        num = start + n
        ids = [b["review_id"] for b, _ in g]
        reads = [r for _, rs in g for r in rs]
        names = ", ".join(f"{b['review_id']} {b['name']}" for b, _ in g)
        note = (f"READ-ONLY Bloodright Jutsu Reference Library capture, batch {n + 1} of {len(groups)}: "
                f"{len(g)} bloodlines ({ids[0]}..{ids[-1]}), {sum(1 for r in reads if r['proc'] == 'jutsu.get')} jutsu.get + "
                f"{sum(1 for r in reads if r['proc'] == 'bloodline.get')} optional bloodline.get, all persist:\"full\". Zero items, zero mutations. "
                f"Members from the pinned roster {lock['roster']['branch']}@{lock['roster']['ref']} {lock['roster']['path']} "
                f"(blob {lock['roster']['blob']}) per brief {lock['brief']['sha']}, generated by "
                f"scripts/bloodright_reference.py manifests. Bloodlines: {names}. "
                "Operator-executed only; agents make zero live requests.")
        out.append((f"push/{num}_bloodright_reference_capture_batch_{n + 1}.json",
                    {"_note": note, "capture": {"before": reads, "after": []}, "items": []}))
    return out


def build(inv: dict, review_ids: list[str] | None, cache: Path, out_dir: Path, *, fetch=_fetch, recheck=False,
          identity=True) -> dict:
    """acquire then pack (pack verifies before placing the file). One command for the operator."""
    got = acquire(inv, review_ids, cache, fetch=fetch, recheck=recheck, identity=identity)
    return {"acquire": got, "pack": pack(inv, review_ids, cache, out_dir)}


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------
def _scope(a) -> list[str] | None:
    if a.all:
        return None
    return a.pilot


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("inventory")
    pi.add_argument("--write", action="store_true", help=f"write {INVENTORY_PATH}")
    pm = sub.add_parser("manifests", help="write capture-only manifests for SOURCE_BLOCKED bloodlines into push/")
    pm.add_argument("--start", type=int, required=True, help="first push/ manifest number")
    pm.add_argument("--no-identity", action="store_true")
    for name in ("acquire", "pack", "verify", "build"):
        p = sub.add_parser(name)
        if name == "verify":
            p.add_argument("zip", type=Path)
        g = p.add_mutually_exclusive_group(required=True)
        g.add_argument("--pilot", nargs="+", metavar="BR-NNN")
        g.add_argument("--all", action="store_true")
        p.add_argument("--cache", type=Path, required=name != "verify")
        if name in ("acquire", "build"):
            p.add_argument("--allow-network", action="store_true", required=True)
            p.add_argument("--recheck", action="store_true", help="re-fetch cached URLs and fail on byte drift")
            p.add_argument("--no-identity", action="store_true")
        if name in ("pack", "build"):
            p.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    try:
        inv, _ = inventory()
        if a.cmd == "inventory":
            s = inv["summary"]
            for b in inv["bloodlines"]:
                print(f"{b['review_id']} {b['rank']} {b['status']:<15} {b['ready_count']}/{b['jutsu_count']}  {b['name']}")
            print(f"\n{s['bloodlines_ready']}/{s['bloodlines']} bloodlines READY, {s['jutsu_ready']}/{s['jutsu']} jutsu source-verified")
            if a.write:
                (ROOT / INVENTORY_PATH).write_bytes(canonical_json(inv))
                print(f"wrote {INVENTORY_PATH}")
        elif a.cmd == "acquire":
            r = acquire(inv, _scope(a), a.cache, recheck=a.recheck, identity=not a.no_identity)
            print(json.dumps(r, indent=1))
        elif a.cmd == "manifests":
            for rel, m in capture_manifests(inv, a.start, identity=not a.no_identity):
                path = ROOT / rel
                _need(not path.exists(), f"{rel} already exists")
                path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(f"wrote {rel}  ({len(m['capture']['before'])} reads, hash {ja.manifest_hash(m)})")
        elif a.cmd == "build":
            r = build(inv, _scope(a), a.cache, a.out, recheck=a.recheck, identity=not a.no_identity)
            print(json.dumps(r, indent=1))
            print(f"\nOK: {r['pack']['path']}  ({r['pack']['bloodlines']} bloodline pack(s), {r['pack']['jutsu']} images, "
                  f"{r['acquire']['cdn_gets']} CDN GETs, 0 game requests)")
        elif a.cmd == "pack":
            print(json.dumps(pack(inv, _scope(a), a.cache, a.out), indent=1))
        else:
            print(json.dumps(verify_bytes(a.zip.read_bytes(), inv, _scope(a), a.cache), indent=1))
    except ProvenanceError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
