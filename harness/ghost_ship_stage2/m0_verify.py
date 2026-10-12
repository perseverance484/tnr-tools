#!/usr/bin/env python3
"""Ghost Ship / Skyglass Stage 2 — gate M0 deterministic fixture verification.

Offline, stdlib-only. Reads committed repository files only; performs no network
or game access. Verifies, without normalising any record:

  * source-file SHA-256 pins declared by the accepted kit packet and the legacy
    conversion packet;
  * all 65 accepted memberships resolve to exact full records (retained legacy
    records in the October 1 AI capture, shared records in the October 9 pool
    capture), with the packet's full-record hashes and AP/cooldown/range/
    method/target summaries;
  * the eleven retained records' protected-field hashes (every field except
    name/description/battleDescription), across every repeated capture of the
    same ID;
  * every AI and AI-profile pointer and hash, profile-id linkage, innate effect
    arrays (duplicates preserved) and baseline numeric profile summaries;
  * missing-versus-null field distinctions are reported as they are captured.

Usage:  python3 harness/ghost_ship_stage2/m0_verify.py [--out PATH]
Exit status 0 only when every check passes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KIT = "state/ghost_ship_hybrid_kit_proposal.json"
LEGACY = "state/ghost_ship_legacy_jutsu_conversion.json"
CONTRACT = "state/ghost_ship_skyglass_sealwright_rule_contract.json"
PRESENTATION_FIELDS = ("name", "description", "battleDescription")
SUMMARY_FIELDS = {"ap": "actionCostPerc", "cooldown": "cooldown", "range": "range",
                  "method": "method", "target": "target"}
EXPECTED = {"aiCount": 11, "memberships": 65, "retained": 11, "shared": 18}


def load(rel):
    with open(os.path.join(REPO, rel), "rb") as fh:
        raw = fh.read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def canon_hash(obj):
    """Packet hash method: SHA-256 of sorted-key compact UTF-8 JSON."""
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ptr(doc, pointer):
    for token in pointer.strip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        doc = doc[int(token)] if isinstance(doc, list) else doc[token]
    return doc


class Checks:
    def __init__(self):
        self.items = []

    def add(self, name, ok, detail=None):
        self.items.append({"check": name, "pass": bool(ok), "detail": detail})
        return ok

    @property
    def failed(self):
        return [c for c in self.items if not c["pass"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    c = Checks()

    kit, kit_sha = load(KIT)
    legacy, legacy_sha = load(LEGACY)
    contract, contract_sha = load(CONTRACT)

    # 1. Source-file hashes declared by the packets.
    files = {}
    for rel, want in kit["sourceFileSha256"].items():
        doc, got = load(rel)
        files[rel] = doc
        c.add(f"sourceFileSha256 {rel}", got == want, {"want": want, "got": got})
    lsrc = legacy["source"]
    c.add("legacy captureFileSha256 equals kit AI capture pin",
          lsrc["captureFileSha256"] == kit["sourceFileSha256"][kit["sourceFiles"]["ai"]],
          lsrc["captureFileSha256"])
    ai_doc = files[kit["sourceFiles"]["ai"]]
    prof_doc = files[kit["sourceFiles"]["profiles"]]
    pool_doc = files[kit["sourceFiles"]["poolRecords"]]

    # 2. Retained legacy records: protected-field hashes across all repeated captures.
    conv = {r["targetId"]: r for r in legacy["conversions"]}
    c.add("legacy conversion record count", len(conv) == EXPECTED["retained"], len(conv))
    retained = {}
    for tid, r in conv.items():
        hashes, full_hashes = [], []
        for p in r["sourcePointers"]:
            rec = ptr(ai_doc, p)
            c.add(f"legacy {tid} pointer {p} id", rec.get("id") == tid, rec.get("id"))
            prot = {k: v for k, v in rec.items() if k not in PRESENTATION_FIELDS}
            hashes.append(canon_hash(prot))
            full_hashes.append(canon_hash(rec))
            c.add(f"legacy {tid} captured name matches 'before'",
                  all(rec.get(k) == r["before"][k] for k in PRESENTATION_FIELDS),
                  {k: rec.get(k) for k in PRESENTATION_FIELDS})
        c.add(f"legacy {tid} protected hash", set(hashes) == {r["protectedRecordSha256"]},
              {"want": r["protectedRecordSha256"], "got": sorted(set(hashes))})
        c.add(f"legacy {tid} repeated captures identical", len(set(full_hashes)) == 1,
              len(r["sourcePointers"]))
        retained[tid] = ptr(ai_doc, r["sourcePointers"][0])

    # 3. Shared records: id, full-record hash and summary fields.
    shared = {}
    for code, ref in kit["sharedReferences"].items():
        rec = ptr(pool_doc, ref["sourcePointer"])
        shared[code] = rec
        c.add(f"shared {code} id", rec.get("id") == ref["id"], {"want": ref["id"], "got": rec.get("id")})
        c.add(f"shared {code} fullRecordSha256", canon_hash(rec) == ref["fullRecordSha256"])
        c.add(f"shared {code} name", rec.get("name") == ref["name"], rec.get("name"))
        for k, field in SUMMARY_FIELDS.items():
            c.add(f"shared {code} {k}", rec.get(field) == ref[k], {"want": ref[k], "got": rec.get(field)})
    c.add("shared unique id count", len(shared) == EXPECTED["shared"], len(shared))

    # 4. Entities: AI/profile pointers, hashes, innate arrays, memberships.
    ents = kit["entities"]
    c.add("AI count", len(ents) == EXPECTED["aiCount"], len(ents))
    memberships, entity_rows = 0, []
    used_retained, used_shared = set(), set()
    for e in ents:
        a = ptr(ai_doc, e["aiSourcePointer"])
        p = ptr(prof_doc, e["profileSourcePointer"])
        c.add(f"{e['name']} ai id", a.get("userId") == e["aiId"], a.get("userId"))
        c.add(f"{e['name']} capturedAiSha256", canon_hash(a) == e["capturedAiSha256"])
        c.add(f"{e['name']} capturedProfileSha256", canon_hash(p) == e["capturedProfileSha256"])
        c.add(f"{e['name']} profile linkage", p.get("id") == a.get("aiProfileId"),
              {"aiProfileId": a.get("aiProfileId"), "profileId": p.get("id")})
        c.add(f"{e['name']} innateEffectsSha256", canon_hash(a.get("effects")) == e["innateEffectsSha256"])
        bps = e["baselineProfileSummary"]
        c.add(f"{e['name']} baseline numeric profile",
              all(a.get(k) == v for k, v in bps.items()),
              {k: [v, a.get(k)] for k, v in bps.items() if a.get(k) != v})
        c.add(f"{e['name']} capturedKitCount", len(a["jutsus"]) == e["capturedKitCount"], len(a["jutsus"]))
        # Mapping covers every captured membership exactly once, in order.
        captured_ids = [uj["jutsuId"] for uj in a["jutsus"]]
        mapped_ids = [m["fromId"] for m in e["mapping"]]
        c.add(f"{e['name']} mapping covers captured memberships",
              sorted(captured_ids) == sorted(mapped_ids), {"captured": captured_ids, "mapped": mapped_ids})
        for m in e["mapping"]:
            rec = ptr(ai_doc, m["sourcePointer"])
            c.add(f"{e['name']} mapping pointer {m['fromId']}", rec.get("id") == m["fromId"], rec.get("id"))
        kit_ids = e["proposedKit"]
        mapped_to = {m["to"] for m in e["mapping"]}
        c.add(f"{e['name']} accepted kit = mapping targets",
              set(kit_ids) == mapped_to and len(kit_ids) == len(set(kit_ids)),
              {"kit": kit_ids, "mappedTo": sorted(mapped_to)})
        resolved = []
        for k in kit_ids:
            if k.startswith("legacy:"):
                tid = k.split(":", 1)[1]
                ok = tid in retained
                used_retained.add(tid)
                resolved.append({"member": k, "id": tid, "name": retained.get(tid, {}).get("name"), "resolved": ok})
            else:
                ok = k in shared
                used_shared.add(k)
                resolved.append({"member": k, "id": shared.get(k, {}).get("id"), "name": shared.get(k, {}).get("name"), "resolved": ok})
            c.add(f"{e['name']} member {k} resolves to full record", ok)
        memberships += len(kit_ids)
        innate = a.get("effects")
        entity_rows.append({
            "aiId": e["aiId"], "name": e["name"], "aiProfileId": a.get("aiProfileId"),
            "includeDefaultRules": p.get("includeDefaultRules"), "capturedRuleCount": len(p.get("rules", [])),
            "acceptedKit": resolved, "capturedKitIds": captured_ids,
            "innateEffects": {"isNull": innate is None, "count": 0 if innate is None else len(innate),
                              "typeCounts": dict(Counter(x.get("type") for x in innate or []))},
            "items": [{"itemId": ui["itemId"], "name": ui["item"]["name"], "itemType": ui["item"]["itemType"],
                       "equipped": ui["equipped"], "dropChancePerc": ui.get("dropChancePerc")} for ui in a.get("items", [])],
            "numericProfile": {k: a.get(k) for k in (
                "level", "rank", "statsMultiplier", "poolsMultiplier", "regeneration", "maxHealth",
                "maxChakra", "maxStamina", "preferredStat", "preferredGeneral1", "preferredGeneral2",
                "primaryElement", "secondaryElement", "strength", "ninjutsuOffence")},
        })
    c.add("accepted membership count", memberships == EXPECTED["memberships"], memberships)
    c.add("retained IDs all used", used_retained == set(retained), sorted(set(retained) - used_retained))
    c.add("shared IDs all used", used_shared == set(shared), sorted(set(shared) - used_shared))

    # 5. Specific accepted-boundary checks from RUL-2026-10-11-003.
    by_name = {e["name"]: e for e in ents}
    capt = by_name["The Captain"]["proposedKit"]
    c.add("regular Captain five-move comparator",
          capt == ["legacy:0Y10JpChssDwFUxNRk6p3", "legacy:MG9ZujAV8lK7--YxThVbQ",
                   "legacy:PdD44PGaNv4MN5fOALhAF", "B14", "B17"], capt)
    crowned = by_name["Crowned Captain"]["proposedKit"]
    c.add("Crowned Captain eleven moves with EA03 replacing Sharpened Focus",
          len(crowned) == 11 and "EA03" in crowned, len(crowned))
    sent = by_name["Sentinel"]
    c.add("Sentinel new retained memberships Rigging Snare/Hollow Timber",
          sorted(sent["newRetainedMembershipProposals"]) ==
          sorted(["legacy:1jXfTgrtGUaSfqTPSSa83", "legacy:Jz4Lb55NcpwZn3nUK5PrJ"]))
    c.add("First Blade uses EL04", "EL04" in by_name["First Blade"]["proposedKit"])
    capt_ai = ptr(ai_doc, by_name["The Captain"]["aiSourcePointer"])
    eq = {ui["item"]["name"]: ui["equipped"] for ui in capt_ai["items"]}
    c.add("Captain AI Heavy Armor / Cursed Dagger equipped:NONE",
          eq.get("AI Heavy Armor") == "NONE" and eq.get("Cursed Dagger") == "NONE", eq)
    inn = capt_ai["effects"]
    c.add("Captain innate Highest offence increasestat 30%/99r",
          len(inn) == 1 and inn[0]["type"] == "increasestat" and inn[0]["power"] == 30
          and inn[0]["rounds"] == 99 and inn[0]["statTypes"] == ["Highest"]
          and inn[0]["generalTypes"] == ["Highest"] and inn[0]["calculation"] == "percentage", inn)

    # 6. Sealwright seven shared IDs resolve in the pool capture.
    pool_by_id = {cap["data"]["id"]: cap["data"] for cap in pool_doc["captures"]
                  if isinstance(cap.get("data"), dict) and "id" in cap["data"]}
    sw = []
    for j in contract["jutsus"]:
        rec = pool_by_id.get(j["liveJutsuId"])
        ok = rec is not None and rec["name"] == j["name"] and rec["actionCostPerc"] == j["ap"] \
            and rec["cooldown"] == j["cooldown"]
        c.add(f"Sealwright {j['code']} {j['name']} resolves", ok)
        if rec:
            sw.append({"code": j["code"], "id": rec["id"], "name": rec["name"], "method": rec["method"],
                       "target": rec["target"], "range": rec["range"], "ap": rec["actionCostPerc"],
                       "cooldown": rec["cooldown"], "effects": [(e["type"], e.get("power"), e.get("rounds")) for e in rec["effects"]]})
    b32 = pool_by_id.get("JWZYiHKPNwYziWEFjw4Fn")
    c.add("B32 captured as ALL method / OTHER_USER / range 5",
          b32 and b32["method"] == "ALL" and b32["target"] == "OTHER_USER" and b32["range"] == 5)

    # 7. Missing-versus-null report (no normalisation). Shared IDs that were already
    # equipped by a Ghost Ship AI exist twice: embedded in the October 1 AI capture and
    # as the October 9 pool record. Report every field that differs, distinguishing an
    # absent key from an explicit null, and compare with the packet's declared drift.
    absent = "<ABSENT>"
    embedded = {}
    for cap in ai_doc["captures"]:
        for uj in (cap.get("data") or {}).get("jutsus", []) if isinstance(cap.get("data"), dict) else []:
            embedded.setdefault(uj["jutsuId"], []).append(uj["jutsu"])
    null_report = {}
    for code, rec in shared.items():
        copies = embedded.get(rec["id"], [])
        diffs = {}
        for old in copies:
            for k in sorted(set(old) | set(rec)):
                ov, nv = old.get(k, absent), rec.get(k, absent)
                if ov != nv:
                    diffs[k] = {"oct01AiEmbedded": ov, "oct09Pool": nv}
        null_report[code] = {"embeddedCopies": len(copies), "differingFields": diffs,
                             "nullFieldsInPoolRecord": sorted(k for k, v in rec.items() if v is None)}
    drift = kit["verification"]["existingSharedRecordDriftFields"]
    for code in shared:
        got = sorted(null_report[code]["differingFields"])
        c.add(f"shared {code} embedded-vs-pool drift fields match packet",
              got == sorted(drift.get(code, [])), {"declared": drift.get(code, []), "got": got})

    result = {
        "gate": "M0",
        "status": "PASS" if not c.failed else "FAIL",
        "checks": len(c.items), "failed": len(c.failed),
        "repoFiles": {KIT: kit_sha, LEGACY: legacy_sha, CONTRACT: contract_sha},
        "hashMethod": "SHA-256 of json.dumps(sort_keys=True, separators=(',',':'), ensure_ascii=False)",
        "entities": entity_rows, "sealwright": sw, "missingVersusNull": null_report,
        "failures": c.failed, "allChecks": c.items,
    }
    text = json.dumps(result, indent=1, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(f"M0 {result['status']}: {result['checks']} checks, {result['failed']} failed")
    for f in c.failed:
        print("  FAIL", f["check"], json.dumps(f["detail"], ensure_ascii=False)[:300])
    return 0 if not c.failed else 1


if __name__ == "__main__":
    sys.exit(main())
