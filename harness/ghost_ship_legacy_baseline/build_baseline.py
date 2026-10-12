#!/usr/bin/env python3
"""Re-baseline the eleven retained legacy jutsu to the post-0056 push/86 capture.

    python3 harness/ghost_ship_legacy_baseline/build_baseline.py          # write the packet
    python3 harness/ghost_ship_legacy_baseline/build_baseline.py --check  # verify, write nothing

WHY A COMPANION PACKET. `state/ghost_ship_legacy_jutsu_conversion.json` pins
`protectedRecordSha256` over the October 1 rows. Live rows no longer hash to those values: upstream
migration 0056 changed 20 schema columns on every jutsu record, with no mechanic change. The
conversion packet is read by the frozen Stage 2 r4, 3/3 Consume and final-item harnesses, and
their M0 evidence records its SHA-256, so editing it would break the byte-identical reproduction of
three frozen review targets. This tool leaves it untouched and writes
`state/ghost_ship_legacy_jutsu_baseline_push86.json` beside it.

WHAT IS PROVEN (fail-closed; any failure exits 1 and writes nothing):
  1. Both capture files match their pinned SHA-256 (the conversion packet's for October 1).
  2. Each October 1 row still hashes to the packet's protectedRecordSha256 (same method).
  3. Every push/86 copy of each id is byte-identical (full-record hash), across every AI kit.
  4. October 1 -> push/86 differs only by the same 20-column schema delta for all 11 records:
     8 removed required*Offence/Defence, 11 added columns, statClassification Highest -> None.
     Every removed and added value is null (or "None" for elementClassification), so no
     requirement is lost or gained. Every other field, effects included, is identical.
  5. Presentation fields (name, description, battleDescription) still equal the packet's `before`.

Hash method, unchanged from the packet: SHA-256 of UTF-8 JSON after removing only name,
description and battleDescription; sorted keys; separators (",", ":"); ensure_ascii=False.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACKET = "state/ghost_ship_legacy_jutsu_conversion.json"
PUSH86 = "harvests/inbox/tnr_results_1791727613862.json"
OUT = "state/ghost_ship_legacy_jutsu_baseline_push86.json"
PRESENTATION = ("name", "description", "battleDescription")

REMOVED = sorted(f"required{a}{s}" for a in ("Ninjutsu", "Genjutsu", "Taijutsu", "Bukijutsu") for s in ("Offence", "Defence"))
ADDED = {
    "requiredNinjutsuMastery": None, "requiredGenjutsuMastery": None, "requiredTaijutsuMastery": None,
    "requiredBukijutsuMastery": None, "requiredBloodlineMastery": None, "requiredSageMastery": None,
    "requiredSkillId": None, "bloodlineReskinId": None, "reskinParentJutsuId": None,
    "coordinateTargeting": None, "elementClassification": "None",
}
CHANGED = {"statClassification": ("Highest", "None")}


def read(rel: str) -> tuple[dict, str]:
    with open(os.path.join(ROOT, rel), "rb") as fh:
        raw = fh.read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def canon(obj) -> str:
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def protected(rec: dict) -> str:
    return canon({k: v for k, v in rec.items() if k not in PRESENTATION})


def ptr(doc, pointer: str):
    for t in pointer.strip("/").split("/"):
        t = t.replace("~1", "/").replace("~0", "~")
        doc = doc[int(t)] if isinstance(doc, list) else doc[t]
    return doc


def build() -> tuple[dict, list[str]]:
    errors: list[str] = []
    packet, packet_sha = read(PACKET)
    src = packet["source"]
    oct1, oct1_sha = read(src["capture"])
    p86, p86_sha = read(PUSH86)
    if oct1_sha != src["captureFileSha256"]:
        errors.append(f"October 1 capture sha {oct1_sha} != packet {src['captureFileSha256']}")

    # every push/86 kit copy, by jutsu id
    copies: dict[str, list[tuple[str, dict]]] = {}
    for i, cap in enumerate(p86["captures"]):
        if cap.get("proc") != "profile.getAi":
            continue
        for j, uj in enumerate(cap["data"]["jutsus"]):
            copies.setdefault(uj["jutsuId"], []).append((f"/captures/{i}/data/jutsus/{j}/jutsu", uj["jutsu"]))

    records = []
    for conv in packet["conversions"]:
        tid = conv["targetId"]
        old = ptr(oct1, conv["sourcePointers"][0])
        if protected(old) != conv["protectedRecordSha256"]:
            errors.append(f"{tid}: October 1 row no longer hashes to the packet value")
        live = copies.get(tid, [])
        if not live:
            errors.append(f"{tid}: not present in any push/86 kit")
            continue
        fulls = {canon(r) for _, r in live}
        if len(fulls) != 1:
            errors.append(f"{tid}: push/86 copies differ ({len(fulls)} distinct)")
        new = live[0][1]
        if any(new.get(k) != conv["before"][k] for k in PRESENTATION):
            errors.append(f"{tid}: push/86 presentation differs from packet 'before'")
        removed = sorted(k for k in old if k not in new)
        added = {k: new[k] for k in new if k not in old}
        changed = {k: (old[k], new[k]) for k in old if k in new and old[k] != new[k]}
        if removed != REMOVED or any(old[k] is not None for k in removed):
            errors.append(f"{tid}: removed columns {removed} (values {[old[k] for k in removed]})")
        if added != ADDED:
            errors.append(f"{tid}: added columns {added}")
        if changed != CHANGED:
            errors.append(f"{tid}: changed fields {changed}")
        records.append({
            "targetId": tid,
            "name": new["name"],
            "push86Pointers": [p for p, _ in live],
            "protectedRecordSha256": protected(new),
            "fullRecordSha256": fulls.pop() if len(fulls) == 1 else None,
            "october1ProtectedRecordSha256": conv["protectedRecordSha256"],
        })

    doc = {
        "schema": "tnr.ghost_ship_legacy_jutsu_baseline",
        "version": 1,
        "status": "CURRENT_LIVE_BASELINE (post-migration 0056)",
        "supersedesForLiveComparison": f"{PACKET} protectedRecordSha256 (October 1 rows; kept unchanged for the frozen harnesses)",
        "generator": "harness/ghost_ship_legacy_baseline/build_baseline.py",
        "source": {"capture": PUSH86, "captureFileSha256": p86_sha, "proc": "profile.getAi (embedded kit rows)",
                   "conversionPacket": PACKET, "conversionPacketSha256": packet_sha,
                   "october1Capture": src["capture"], "october1CaptureSha256": oct1_sha},
        "hashMethod": packet["offlineVerification"]["hashMethod"],
        "schemaDelta": {
            "upstream": "app/drizzle/migrations/0056_unified_combat_stats_masteries.sql",
            "removedAllNull": REMOVED, "addedValues": ADDED,
            "changed": {k: {"from": a, "to": b} for k, (a, b) in CHANGED.items()},
            "otherFieldsIdentical": True, "presentationUnchanged": True,
        },
        "records": records,
    }
    return doc, errors


def main() -> int:
    check = "--check" in sys.argv[1:]
    doc, errors = build()
    for e in errors:
        print("FAIL " + e, file=sys.stderr)
    if errors:
        return 1
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    path = os.path.join(ROOT, OUT)
    if check:
        cur = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if cur != text:
            print(f"STALE: {OUT}", file=sys.stderr)
            return 1
        print(f"OK: {OUT} current; 11 records verified against push/86")
        return 0
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"wrote {OUT}: {len(doc['records'])} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
