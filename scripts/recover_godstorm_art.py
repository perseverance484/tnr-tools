#!/usr/bin/env python3
"""Archive only saved Godstorm image URLs. Never contacts a game API.

Pinned capture files are read from Git objects, not a possibly edited worktree.
Normal execution requires a repository and a network-enabled runtime. Original
hosted bytes are retained; no art edits are made.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "6e09b15bb6f3d1c90ba416d14211b533f5b4a367"
ROOTS = ("2yvE9PUQqlD8lbYNfgX-b", "OSADdXqostbyVliCxWk6k")
BACKGROUND = "cKHhHoboreP88iH5WjDe7"
CAPTURES = (
    ("harvests/inbox/tnr_results_1789401726302.json",
     "push/23_godstorm_tower_root_capture.json", 3),
    ("harvests/inbox/tnr_results_1789402842027.json",
     "push/24_godstorm_tower_related_capture.json", 30),
)
HOSTS = frozenset(("ui0arpl8sm.ufs.sh", "uploadthing.b-cdn.net",
                   "tnr-storage-cdn.b-cdn.net", "utfs.io"))
MAX_BYTES = 5 * 1024 * 1024
USER_AGENT = "tnr-tools/godstorm-art-recovery (capture-backed image archiving)"
EXTENSIONS = {"PNG": ".png", "WEBP": ".webp", "JPEG": ".jpg", "GIF": ".gif"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def check_url(url: str) -> str:
    """Fail closed on unexpected hosts, credentials, ports or non-file routes."""
    p = urllib.parse.urlsplit(url)
    if (p.scheme != "https" or p.hostname not in HOSTS or p.username or p.password
            or p.port not in (None, 443) or p.query or p.fragment
            or not re.fullmatch(r"/f/[A-Za-z0-9_.-]+", p.path)):
        raise ValueError("URL outside the capture-art HTTPS allowlist")
    return url


class CheckedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def read_pinned(repo: Path, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{BASE}:{path}"])


def load_capture(repo: Path, source: tuple) -> dict:
    path, manifest, count = source
    raw = read_pinned(repo, path)
    doc = json.loads(raw)
    if (doc.get("state") != "DONE" or doc.get("outcome") != "success"
            or doc.get("entries") != [] or len(doc.get("captures", [])) != count
            or doc.get("journal", {}).get("manifestPath") != manifest):
        raise ValueError(f"Capture envelope does not match approved input: {path}")
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    return {"doc": doc, "path": path, "sha256": hashlib.sha256(raw).hexdigest(),
            "git_blob_sha": blob}


def point(source: dict, proc: str, entity_id: str) -> tuple:
    matches = [(i, c) for i, c in enumerate(source["doc"]["captures"])
               if c.get("proc") == proc and c.get("input", {}).get("id") == entity_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {proc} record for {entity_id}")
    i, c = matches[0]
    if (c.get("ok") is not True or c.get("rows") != 1 or c.get("persist") != "full"
            or c.get("persistOk") is not True or not isinstance(c.get("data"), dict)
            or c["data"].get("id") != entity_id or not c.get("snapshotKey")):
        raise ValueError(f"Incomplete persisted record: {proc}/{entity_id}")
    return i, c


def ref(source: dict, proc: str, entity_id: str, field: str, kind: str,
        used_by: list[str]) -> dict:
    i, c = point(source, proc, entity_id)
    d = c["data"]
    url = d.get(field)
    status = "missing" if not url else "default" if "_default." in url else "pending"
    if url:
        check_url(url)
    return {"entity_id": entity_id, "name": d.get("username") or d.get("name"),
            "kind": kind, "used_by": used_by, "source_field": field,
            "source_url": url, "status": status,
            "capture_path": source["path"], "snapshot_key": c["snapshotKey"],
            "capture_pointer": f"/captures/{i}/data/{field}", "captured_at": c.get("at")}


def select(sources: list[dict]) -> list[dict]:
    quest_source, related = sources
    references, ais, backgrounds = [], {}, {BACKGROUND: ["candidate_for_stormcourt"]}
    for qid in ROOTS:
        _, c = point(quest_source, "quests.get", qid)
        q = c["data"]
        if q.get("questType") != "battlepyramid":
            raise ValueError("Retained root is not a battlepyramid")
        nodes = q["content"]["objectives"]
        battles = [n for n in nodes if n.get("task") == "start_battle"]
        if len(battles) != 25:
            raise ValueError("Unexpected battle count; stop for scope review")
        references.append(ref(quest_source, "quests.get", qid, "image", "listing", [qid]))
        for b in battles:
            for group in b.get("opponentAIs", []):
                for aid in group.get("ids", []):
                    ais.setdefault(aid, set()).add(qid)
        for n in [q["content"]] + nodes:
            asset_id = n.get("sceneBackground")
            if asset_id:
                backgrounds.setdefault(asset_id, []).append(qid)
    if len(ais) != 18 or len(backgrounds) != 4:
        raise ValueError("Scope census changed; stop for review")
    for aid, owners in sorted(ais.items()):
        references.append(ref(related, "profile.getAi", aid, "avatar", "avatar", sorted(owners)))
    for bid, owners in sorted(backgrounds.items()):
        _, c = point(related, "gameAsset.get", bid)
        if c["data"].get("type") != "SCENE_BACKGROUND":
            raise ValueError("Unexpected background asset type")
        references.append(ref(related, "gameAsset.get", bid, "image", "background", sorted(set(owners))))
    if len(references) != 24 or sum(r["status"] == "default" for r in references) != 5:
        raise ValueError("Unexpected original/default census; stop for review")
    return references


def download(url: str) -> tuple[bytes, str, str]:
    check_url(url)
    opener = urllib.request.build_opener(CheckedRedirect())
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "image/*"})
    with opener.open(req, timeout=20) as response:
        final_url = check_url(response.geturl())
        data = response.read(MAX_BYTES + 1)
        content_type = response.headers.get("Content-Type", "")
    if len(data) > MAX_BYTES or not data:
        raise ValueError("Image is empty or exceeds 5 MiB")
    return data, final_url, content_type


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.out.exists():
        raise ValueError("Output already exists; preserve prior evidence and choose a fresh path")
    sources = [load_capture(repo, c) for c in CAPTURES]
    refs = select(sources)
    # Reuse the repository decoder without changing its capture approval pin.
    module_path = repo / "skills/producing-tnr-art/scripts/style_refs.py"
    spec = importlib.util.spec_from_file_location("tnr_style_refs", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    args.out.mkdir(parents=True)
    (args.out / "originals").mkdir()
    report = {"schema": "godstorm.source_art_archive.v1", "repository": "perseverance484/tnr-tools",
              "capture_commit": BASE, "generated_at": utc_now(), "state": "INCOMPLETE",
              "notice": "Hosted bytes downloaded now; not proven original generation masters or capture-time bytes. No visual acceptance implied.",
              "scope": "Two retained listing images, 18 retained primary avatar references, four captured background candidates. No game API.",
              "sources": [{k: s[k] for k in ("path", "sha256", "git_blob_sha")} for s in sources],
              "references": refs, "files": []}
    unique = sorted({r["source_url"] for r in refs if r["status"] == "pending"})
    failures = []
    for number, url in enumerate(unique, 1):
        owners = [r for r in refs if r["source_url"] == url]
        try:
            data, final_url, content_type = download(url)
            fmt, width, height = module.decode_header(data)
            if fmt not in EXTENSIONS or not (0 < width <= 8192 and 0 < height <= 8192):
                raise ValueError("Image dimensions or format outside archive bounds")
            sha = hashlib.sha256(data).hexdigest()
            relative = f"originals/{sha}{EXTENSIONS[fmt]}"
            target = args.out / relative
            if target.exists() and target.read_bytes() != data:
                raise ValueError("Hash filename collision")
            target.write_bytes(data)
            report["files"].append({"path": relative, "sha256": sha, "bytes": len(data),
                "format": fmt, "width": width, "height": height, "source_url": url,
                "final_url": final_url, "http_content_type": content_type, "downloaded_at": utc_now(),
                "validation": "header decoded; full pixel/visual QC pending"})
            for owner in owners:
                owner.update(status="downloaded", file=relative, sha256=sha)
            print(f"[{number}/{len(unique)}] OK {owners[0]['name']}: {width}x{height}, {len(data)} bytes", flush=True)
        except (OSError, ValueError) as exc:
            message = str(exc)[:300]
            for owner in owners:
                owner.update(status="download_failed", error=message)
            failures.append({"source_url": url, "error": message})
            print(f"[{number}/{len(unique)}] FAILED {owners[0]['name']}: {message}", flush=True)
        time.sleep(0.3)
    report["state"] = "PARTIAL" if failures else "COMPLETE"
    report["failures"] = failures
    report["summary"] = {"references": len(refs), "default_references_skipped": 5,
                         "unique_urls_requested": len(unique), "downloads_ok": len(report["files"]),
                         "downloads_failed": len(failures)}
    (args.out / "index.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    return 2 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        sys.exit(1)
