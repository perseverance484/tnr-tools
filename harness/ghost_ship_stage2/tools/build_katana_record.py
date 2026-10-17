#!/usr/bin/env python3
"""Derive the accepted Skyglass Katana record from the captured Night's Testament row.

Baseline: RUL-2026-10-11-004 (Night's Testament, push/85 capture). Every field is copied
from the capture unless it is named in OVERRIDES (each override cites its ruling) or
DROPPED (row identity/timestamps assigned at creation). Writes
state/ghost_ship_skyglass_katana_record.json. Deterministic, stdlib only.
"""
import copy, hashlib, json, os, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CAPTURE = "harvests/inbox/tnr_results_1791727479372.json"
POINTER = "/captures/0/data"
OUT = "state/ghost_ship_skyglass_katana_record.json"
PRESENTATION_PENDING = ("description", "battleDescription", "image")
VISUAL_TAG_FIELDS = ("appearSfx", "disappearSfx", "appearAnimation", "disappearAnimation", "staticAnimation", "staticAssetPath")


def main():
    raw = open(os.path.join(REPO, CAPTURE), "rb").read()
    cap = json.loads(raw)["captures"][0]
    nt = cap["data"]
    assert cap["proc"] == "item.get" and nt["id"] == "osJq3k77YPGoFWgof12FQ"
    assert (nt["itemType"], nt["rarity"], nt["weaponType"]) == ("WEAPON", "LEGENDARY", "SWORD")
    pierce = copy.deepcopy(next(e for e in nt["effects"] if e["type"] == "pierce"))
    immunity = copy.deepcopy(next(e for e in nt["effects"] if e["type"] == "immunity"))
    assert pierce["power"] == 50 and pierce.get("powerPerLevel") == 0
    assert immunity["blocks"] == "buffprevent" and immunity["rounds"] == 2 and immunity["target"] == "SELF"
    pierce["elements"] = ["Crystal"]
    for tag in (pierce, immunity):
        for f in VISUAL_TAG_FIELDS:
            if f in tag:
                tag[f] = ""
    consume = {"type": "consume", "power": 40, "calculation": "percentage", "target": "SELF",
               "rounds": 0, "shieldRounds": 3, "powerPerLevel": 0, "direction": "offence",
               "description": "placeholder", "appearSfx": "", "disappearSfx": "", "appearAnimation": "",
               "disappearAnimation": "", "staticAnimation": "", "staticAssetPath": ""}
    overrides = {
        "name": ("Skyglass Katana", "RUL-2026-10-10-007 approved name"),
        "effects": ([pierce, immunity, consume], "RUL-2026-10-10-007 three effects; RUL-2026-10-11-004 Pierce element Crystal (was Shadow); visual asset ids cleared pending art"),
        "canBeImbued": (False, "RUL-2026-10-10-007"),
        "canBeCrafted": (False, "RUL-2026-10-11-004 drop-only (3% Crowned Captain drop is the sole source)"),
        "craftingExperience": (0, "RUL-2026-10-11-004 drop-only"),
        "hidden": (True, "creation doctrine: new records are created hidden; publication is separate"),
    }
    for f in PRESENTATION_PENDING:
        overrides[f] = (None, "presentation pending (prose/art acceptance); not copied from Night's Testament")
    dropped = ("id", "createdAt", "updatedAt")
    record, provenance = {}, {}
    for k in sorted(nt):
        if k in dropped:
            continue
        if k in overrides:
            record[k], why = overrides[k]
            provenance[k] = {"source": "override", "why": why, "nightsTestament": nt[k] if k != "effects" else "see capture"}
        else:
            record[k] = nt[k]
            provenance[k] = {"source": "Night's Testament"}
    out = {
        "schema": "tnr.ghost_ship_skyglass_katana_record.v1",
        "status": "DIRECTOR_ACCEPTED_BASELINE_RUL-2026-10-11-004; NOT A WRITE MANIFEST",
        "baseline": {"capture": CAPTURE, "captureSha256": hashlib.sha256(raw).hexdigest(), "pointer": POINTER,
                     "id": nt["id"], "name": nt["name"], "capturedAt": cap.get("at")},
        "droppedFields": list(dropped),
        "presentationPending": list(PRESENTATION_PENDING),
        "record": record,
        "provenance": provenance,
    }
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        cur = open(os.path.join(REPO, OUT), encoding="utf-8").read()
        print("current" if cur == text else "STALE")
        return 0 if cur == text else 1
    open(os.path.join(REPO, OUT), "w", encoding="utf-8").write(text)
    print(f"wrote {OUT}: {len(record)} fields, {sum(1 for p in provenance.values() if p['source'] == 'override')} overrides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
