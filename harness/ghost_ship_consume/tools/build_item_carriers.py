#!/usr/bin/env python3
"""Build deterministic ACTIVE CONSUME TEST CARRIERS, never production records.

Katana: full captured Night's Testament row + RUL004/005 overrides. The only
mechanical differences from frozen r4 are Consume power 40 -> 15 and rounds
0 -> 3. Both Consume durations are explicit 3-round TEST INPUTS, not approved
balance. Crystal: Flaming Sword shape donor with disclosed carrier overrides;
only CRYSTAL/WEAPON target and the single Consume10 effect are design locks.
No engine imports, network, credentials or writes outside the new output file.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[3]
OUT = "state/ghost_ship_skyglass_active_consume_carriers.json"
OLD = "state/ghost_ship_skyglass_katana_record.json"
DELTA = "state/ghost_ship_skyglass_consume_revision.json"
NT_CAPTURE = "harvests/inbox/tnr_results_1791727479372.json"
FS_CAPTURE = "harvests/inbox/tnr_results_1788235198666.json"
ENGINE = "585534d7eb21d6f0dd678d5c3eb92662f611d39b"
DROPPED = ["id", "createdAt", "updatedAt"]
PRESENTATION = ["description", "battleDescription", "image"]
VISUALS = ["appearSfx", "disappearSfx", "appearAnimation", "disappearAnimation", "staticAnimation", "staticAssetPath"]


def load(path):
    return json.loads((REPO / path).read_text())


def digest(path):
    return hashlib.sha256((REPO / path).read_bytes()).hexdigest()


def diff(before, after, path=""):
    if isinstance(before, dict) and isinstance(after, dict):
        return [d for k in sorted(before.keys() | after.keys())
                for d in diff(before.get(k), after.get(k), f"{path}/{k}")]
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        return [d for i, (b, a) in enumerate(zip(before, after)) for d in diff(b, a, f"{path}/{i}")]
    return [] if before == after else [{"path": path, "before": before, "after": after}]


def consume(power):
    return {"type": "consume", "power": power, "calculation": "percentage", "target": "SELF",
            "rounds": 3, "shieldRounds": 3, "powerPerLevel": 0, "direction": "offence",
            "description": "placeholder", **{k: "" for k in VISUALS}}


def derived(donor, overrides, donor_label):
    record, provenance = {}, {}
    for key in sorted(donor.keys() | overrides.keys()):
        if key in DROPPED:
            continue
        if key in overrides:
            record[key], why = copy.deepcopy(overrides[key])
            provenance[key] = {"source": "override", "why": why}
        else:
            record[key] = copy.deepcopy(donor[key])
            provenance[key] = {"source": donor_label}
    return record, provenance


def build():
    delta = load(DELTA)
    assert delta["ruling"] == "RUL-2026-10-11-005"
    assert delta["katana"]["consume"]["power"] == 15 and delta["crystal"]["consume"]["power"] == 10
    nt_cap = load(NT_CAPTURE)["captures"][0]
    nt = nt_cap["data"]
    assert nt_cap["proc"] == "item.get" and nt["id"] == "osJq3k77YPGoFWgof12FQ"
    assert (nt["itemType"], nt["rarity"], nt["weaponType"]) == ("WEAPON", "LEGENDARY", "SWORD")
    pierce = copy.deepcopy(next(e for e in nt["effects"] if e["type"] == "pierce"))
    immunity = copy.deepcopy(next(e for e in nt["effects"] if e["type"] == "immunity"))
    assert pierce["power"] == 50 and pierce["powerPerLevel"] == 0
    assert (immunity["blocks"], immunity["target"], immunity["rounds"]) == ("buffprevent", "SELF", 2)
    pierce["elements"] = ["Crystal"]
    for tag in (pierce, immunity):
        for field in VISUALS:
            if field in tag:
                tag[field] = ""
    overrides = {
        "name": ("Skyglass Katana", "RUL-2026-10-10-007"),
        "effects": ([pierce, immunity, consume(15)], "RUL004 retained Pierce/Immunity; RUL005 Consume15; Consume rounds3/shieldRounds3 TEST CARRIER ONLY; pending visual IDs cleared"),
        "canBeImbued": (False, "RUL-2026-10-10-007"),
        "canBeCrafted": (False, "RUL-2026-10-11-004 drop-only"),
        "craftingExperience": (0, "RUL-2026-10-11-004 drop-only"),
        "hidden": (True, "creation doctrine; no publication"),
        **{field: (None, "presentation pending; validation/battle helper uses labelled placeholders") for field in PRESENTATION},
    }
    katana, katana_prov = derived(nt, overrides, "Night's Testament; RUL004 approved non-effect baseline")
    old_diff = diff(load(OLD)["record"], katana)
    assert old_diff == [{"path": "/effects/2/power", "before": 40, "after": 15},
                        {"path": "/effects/2/rounds", "before": 0, "after": 3}], old_diff
    fs_cap = load(FS_CAPTURE)["captures"][8]
    fs = fs_cap["data"]["items"][0]["item"]
    assert fs["id"] == "1GmiQAGuBZZsjIFqcqPkR" and fs["weaponType"] == "SWORD"
    crystal_overrides = {
        "name": ("Skyglass Crystal (offline carrier)", "test identity; name Skyglass Crystal approved"),
        "itemType": ("CRYSTAL", "RUL005 retained category"),
        "crystalTargetTypes": ("WEAPON", "RUL005 retained weapon-only restriction"),
        "effects": ([consume(10)], "RUL005 sole Consume10; rounds3/shieldRounds3 TEST CARRIER ONLY"),
        "weaponType": ("NONE", "crystal carrier shape"),
        "slot": ("ITEM", "crystal carrier shape"),
        "target": ("SELF", "crystal carrier shape; Consume target is SELF"),
        "method": ("SINGLE", "crystal carrier shape"),
        "range": (0, "crystal carrier shape"),
        "rarity": ("RARE", "TEST CARRIER ONLY; rarity unapproved; guards also test EPIC/LEGENDARY"),
        "canBeImbued": (False, "crystal carrier is not an imbue recipient"),
        "description": ("harness placeholder (presentation pending)", "test presentation"),
        "battleDescription": ("harness placeholder (presentation pending)", "test presentation"),
        "image": ("", "test presentation; no art or CDN fetch"),
    }
    crystal, crystal_prov = derived(fs, crystal_overrides, "Flaming Sword TEST CARRIER ONLY; not a Crystal policy decision")
    return {
        "schema": "tnr.ghost_ship_skyglass_active_consume_carriers.v1",
        "status": "OFFLINE_TEST_CARRIERS_ONLY; TIMING_ECONOMY_PRESENTATION_NOT_FROZEN; NOT_A_WRITE_MANIFEST",
        "ruling": delta["ruling"], "engineCommit": ENGINE,
        "designDelta": {"file": DELTA, "sha256": digest(DELTA)},
        "testTiming": {"consumeRounds": 3, "generatedShieldRounds": 3, "approved": False,
                       "note": "Explicit source-default test inputs; separate director timing decisions remain open."},
        "historicalKatana": {"file": OLD, "sha256": digest(OLD), "tnrCommit": "3f825562ea051306a3803f47428b742ae5100011", "recordDiff": old_diff},
        "katana": {
            "status": "RUL004_BASELINE_PLUS_RUL005_RATE_WITH_TEST_TIMING; PRESENTATION_PENDING",
            "baseline": {"capture": NT_CAPTURE, "captureSha256": digest(NT_CAPTURE), "pointer": "/captures/0/data",
                         "id": nt["id"], "name": nt["name"], "capturedAt": nt_cap.get("at")},
            "droppedFields": DROPPED, "presentationPending": PRESENTATION,
            "record": katana, "provenance": katana_prov,
        },
        "crystal": {
            "status": "FULL_SCHEMA_TEST_CARRIER; NON_EFFECT_FIELDS_NOT_DIRECTOR_APPROVED",
            "baseline": {"capture": FS_CAPTURE, "captureSha256": digest(FS_CAPTURE), "pointer": "/captures/8/data/items/0/item",
                         "id": fs["id"], "name": fs["name"], "capturedAt": fs_cap.get("at")},
            "droppedFields": DROPPED, "presentationPending": PRESENTATION,
            "openPolicy": ["rarity", "trading", "crafting rank/occupation economics", "all remaining non-effect Crystal fields"],
            "note": "Carried shop/cost/trade/craft/level fields are test data only, not proposals or implementation defaults. The 12-Filament recipe is supplied separately to the craft guard test; no live recipe ID is invented.",
            "record": crystal, "provenance": crystal_prov,
        },
    }


def main():
    data = json.dumps(build(), indent=1, ensure_ascii=False) + "\n"
    output = REPO / OUT
    if "--check" in sys.argv:
        current = output.exists() and output.read_text() == data
        print("current" if current else "STALE")
        return 0 if current else 1
    output.write_text(data)
    print(f"wrote {OUT} (test carriers; Consume 15/10; test timing 3/3)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
