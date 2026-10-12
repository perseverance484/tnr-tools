#!/usr/bin/env python3
"""Consumer audit for the eleven retained legacy jutsu (read-only, offline).

    python3 harness/ghost_ship_legacy_baseline/consumer_audit.py <census results.json> [...]
    python3 harness/ghost_ship_legacy_baseline/consumer_audit.py --check <census results.json> [...]
    ... --live-count <push/91 results.json>   use a fresh profile.getAllAiNames count instead of 522

A --live-count bundle must hold exactly one ok profile.getAllAiNames read taken AFTER every census
read; its row count replaces push/80's 522 (2026-10-09) as the expected live non-ELDER total.

INPUT: the Forge results of the queued, operator-run AI census push/81-84
(`push/8[1-4]_ai_pool_reequip_census_stage2_batch*.json`). Together they point-read every AI id the
repository knows (535) with profile.getAi persist:"full", so every body carries the AI's kit.
No separate Ghost Ship manifest is needed: the eleven jutsu are jutsuType AI and hidden, so the only
possible holders are AI kits, which is exactly what the census reads.

WHY: push/90 edits the presentation of these eleven jutsu. Law 18/60 says an edit severs the combat
link of every AI that has the jutsu equipped. push/90 unequips and re-equips them on the eleven
Ghost Ship AIs only, so any OTHER AI holding one would be left with a severed link.

VERDICT (fail-closed):
  CLEAR       every census id was read; non-null non-ELDER bodies == 522 (the census's own
              completeness rule from push/80's profile.getAllAiNames count); no AI outside the
              eleven Ghost Ship AIs holds any of the eleven jutsu.
  CONSUMERS   at least one other AI holds one; the list is written and push/90 --final refuses.
  INCOMPLETE  a census id is missing from the inputs, or the live count is not 522.
Writes state/ghost_ship_legacy_jutsu_consumer_audit.json; exit 0 only for CLEAR.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASELINE = "state/ghost_ship_legacy_jutsu_baseline_push86.json"
KIT = "state/ghost_ship_hybrid_kit_proposal.json"
OUT = "state/ghost_ship_legacy_jutsu_consumer_audit.json"
EDIT_SCOPE = "state/ghost_ship_legacy_jutsu_edit_scope.json"  # RUL-2026-10-12-010
CENSUS_GLOB = "push/8[1-4]_ai_pool_reequip_census_stage2_batch*.json"
LIVE_NON_ELDER = 522  # push/80 profile.getAllAiNames row count (tnr_results_1791583362574.json)


def read(rel: str) -> tuple[dict, str]:
    with open(os.path.join(ROOT, rel), "rb") as fh:
        raw = fh.read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def census_ids() -> tuple[set[str], dict[str, str]]:
    ids: set[str] = set()
    manifests = {}
    for path in sorted(glob.glob(os.path.join(ROOT, CENSUS_GLOB))):
        rel = os.path.relpath(path, ROOT)
        doc, sha = read(rel)
        manifests[rel] = sha
        ids |= {c["input"]["userId"] for c in doc["capture"]["before"] if c.get("proc") == "profile.getAi"}
    archived = sorted(glob.glob(os.path.join(ROOT, "archive", "spent-manifests", "*", "8[1-4]_ai_pool_reequip_census_stage2_batch*.json")))
    for path in archived:  # after the census is run and archived, read the manifests from there
        rel = os.path.relpath(path, ROOT)
        if rel not in manifests:
            doc, sha = read(rel)
            manifests[rel] = sha
            ids |= {c["input"]["userId"] for c in doc["capture"]["before"] if c.get("proc") == "profile.getAi"}
    return ids, manifests


def live_count(rel: str, after: str) -> tuple[int, dict]:
    doc, sha = read(rel)
    reads = [c for c in doc.get("captures", []) if c.get("proc") == "profile.getAllAiNames"]
    if len(reads) != 1 or reads[0].get("ok") is not True or not isinstance(reads[0].get("rows"), int):
        raise SystemExit(f"{rel}: expected exactly one ok profile.getAllAiNames read with a row count")
    at = reads[0].get("at") or doc.get("at")
    if not at or at <= after:
        raise SystemExit(f"{rel}: count taken at {at}, not after the last census read {after}")
    return reads[0]["rows"], {"path": rel, "sha256": sha, "at": at, "rows": reads[0]["rows"]}


def audit(result_paths: list[str], count_path: str | None = None) -> dict:
    baseline, baseline_sha = read(BASELINE)
    scope, scope_sha = read(EDIT_SCOPE)
    # Only jutsu push/90 edits can sever an outside link; excluded ones are reported, not counted.
    targets = {r["targetId"]: r["name"] for r in baseline["records"]}
    excluded = set(scope["excluded"])
    ghost = {e["aiId"] for e in read(KIT)[0]["entities"]}
    want, manifests = census_ids()
    if len(want) != 535:
        raise SystemExit(f"census manifests name {len(want)} AI ids, expected 535")

    bodies: dict[str, dict | None] = {}
    errors: list[str] = []
    inputs = {}
    for rel in result_paths:
        doc, sha = read(rel)
        inputs[rel] = {"sha256": sha, "at": doc.get("at"), "state": doc.get("state"), "outcome": doc.get("outcome")}
        for c in doc.get("captures", []):
            if c.get("proc") != "profile.getAi":
                continue
            uid = (c.get("input") or {}).get("userId")
            if not uid:
                continue  # supplementary reads (e.g. push/92) of ids outside the census also count
            if c.get("ok") is not True:
                errors.append(f"{uid}: read not ok ({c.get('error')})")
                continue
            if c.get("persist") not in (None, "full") or ("data" not in c):
                errors.append(f"{uid}: body not persisted")
                continue
            bodies[uid] = c["data"]

    expected, count_src = LIVE_NON_ELDER, {"path": "harvests/inbox/tnr_results_1791583362574.json (push/80)", "rows": LIVE_NON_ELDER}
    if count_path:
        last = max(c.get("at") or "" for rel in result_paths for c in read(rel)[0].get("captures", []))
        expected, count_src = live_count(count_path, last)
    missing = sorted(want - set(bodies))
    live = {u: b for u, b in bodies.items() if b is not None and b.get("rank") != "ELDER"}
    holders = []
    for uid, body in sorted(live.items()):
        for uj in body.get("jutsus") or []:
            jid = uj.get("jutsuId")
            if jid in targets:
                holders.append({"aiId": uid, "username": body.get("username"), "jutsuId": jid,
                                "jutsuName": targets[jid], "equipped": uj.get("equipped"),
                                "ghostShip": uid in ghost})
    others = [h for h in holders if not h["ghostShip"] and h["jutsuId"] not in excluded]
    unedited = [h for h in holders if not h["ghostShip"] and h["jutsuId"] in excluded]
    if missing or errors or len(live) != expected:
        verdict = "INCOMPLETE"
    elif others:
        verdict = "CONSUMERS"
    else:
        verdict = "CLEAR"
    return {
        "schema": "tnr.ghost_ship_legacy_jutsu_consumer_audit",
        "version": 1,
        "verdict": verdict,
        "generator": "harness/ghost_ship_legacy_baseline/consumer_audit.py",
        "baseline": {"path": BASELINE, "sha256": baseline_sha},
        "editScope": {"path": EDIT_SCOPE, "sha256": scope_sha, "excluded": sorted(excluded)},
        "censusManifests": manifests,
        "inputs": inputs,
        "coverage": {"censusIds": len(want), "read": len(bodies), "missing": missing,
                     "extraIdsRead": sorted(set(bodies) - want),
                     "deletedNull": sum(1 for b in bodies.values() if b is None),
                     "elder": sum(1 for b in bodies.values() if b is not None and b.get("rank") == "ELDER"),
                     "liveNonElder": len(live), "expectedLiveNonElder": expected, "liveCountSource": count_src,
                     "readErrors": errors},
        "ghostShipHolders": [h for h in holders if h["ghostShip"]],
        "otherHolders": others,
        "otherHoldersOfUneditedJutsu": unedited,
    }


def main() -> int:
    args = sys.argv[1:]
    check = "--check" in args
    count_path = None
    if "--live-count" in args:
        i = args.index("--live-count")
        count_path = args[i + 1]
        args = args[:i] + args[i + 2:]
    paths = [a for a in args if not a.startswith("--")]
    if not paths:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    doc = audit(paths, count_path)
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    out = os.path.join(ROOT, OUT)
    if check:
        cur = open(out, encoding="utf-8").read() if os.path.exists(out) else None
        if cur != text:
            print(f"STALE: {OUT}", file=sys.stderr)
            return 1
    else:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
    cov = doc["coverage"]
    print(f"{doc['verdict']}: read {cov['read']}/{cov['censusIds']}, live non-ELDER {cov['liveNonElder']}/{cov['expectedLiveNonElder']}, "
          f"Ghost Ship holders {len(doc['ghostShipHolders'])}, other holders {len(doc['otherHolders'])}")
    for h in doc["otherHolders"]:
        print(f"  CONSUMER {h['username']} ({h['aiId']}) holds {h['jutsuName']} ({h['jutsuId']}) equipped={h['equipped']}")
    return 0 if doc["verdict"] == "CLEAR" else 1


if __name__ == "__main__":
    raise SystemExit(main())
