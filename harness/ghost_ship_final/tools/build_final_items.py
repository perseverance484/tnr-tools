#!/usr/bin/env python3
"""Build the deterministic FINAL 2/2 Skyglass item candidate records (RUL-2026-10-11-006).

Katana: full captured Night's Testament row + RUL004/005/006 overrides. Its only
mechanical differences from the 3/3 test carrier are Consume rounds 3 -> 2 and
shieldRounds 3 -> 2. Crystal: captured Flaming Sword shape donor + RUL005/006
overrides (LEGENDARY, tradable, not craftable, no recipe, one Consume10 2/2).
Every Crystal field the director has not decided is listed as an unapproved
carrier value; presentation stays pending. This is a candidate record packet,
not a write manifest. No engine imports, network, credentials or other writes.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[3]
OUT = "state/ghost_ship_skyglass_final_item_records.json"
CONTRACT = "state/ghost_ship_skyglass_final_item_contract.json"
R4_KATANA = "state/ghost_ship_skyglass_katana_record.json"
CARRIERS_3X3 = "state/ghost_ship_skyglass_active_consume_carriers.json"
NT_CAPTURE = "harvests/inbox/tnr_results_1791727479372.json"
FS_CAPTURE = "harvests/inbox/tnr_results_1788235198666.json"
ENGINE = "585534d7eb21d6f0dd678d5c3eb92662f611d39b"
DESIGN = "fd7f021762940f11c3896c70b2af3bc53f7711dc"
DROPPED = ["id", "createdAt", "updatedAt"]
PRESENTATION = ["description", "battleDescription", "image"]
VISUALS = ["appearSfx", "disappearSfx", "appearAnimation", "disappearAnimation", "staticAnimation", "staticAssetPath"]
# Crystal fields carried from the Flaming Sword shape donor that no ruling decides.
# They validate, but they are NOT proposals: the director has not set them.
CRYSTAL_UNAPPROVED = ["actionCostPerc", "battleUsageType", "canStack", "chakraCost", "cooldown", "cost",
                      "destroyOnUse", "maxDurability", "maxEquips", "maxImbueNumber", "requiredLevel",
                      "stackSize", "staminaCost", "xpToLevel"]


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


def consume(spec):
    keys = ("type", "power", "calculation", "target", "rounds", "shieldRounds")
    return {**{k: spec[k] for k in keys}, "powerPerLevel": 0, "direction": "offence",
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
    contract = load(CONTRACT)
    assert contract["ruling"] == "RUL-2026-10-11-006"
    k_spec, c_spec = contract["katana"]["consume"], contract["crystal"]["consume"]
    assert (k_spec["power"], k_spec["rounds"], k_spec["shieldRounds"]) == (15, 2, 2)
    assert (c_spec["power"], c_spec["rounds"], c_spec["shieldRounds"]) == (10, 2, 2)
    cc = contract["crystal"]
    assert (cc["itemType"], cc["crystalTargetTypes"], cc["rarity"], cc["canBeTraded"], cc["canBeCrafted"]) == \
        ("CRYSTAL", "WEAPON", "LEGENDARY", True, False)

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
    k_over = {
        "name": ("Skyglass Katana", "RUL-2026-10-10-007"),
        "effects": ([pierce, immunity, consume(k_spec)], "RUL004 retained Pierce50 (Crystal)/SELF immunity2r; RUL005 Consume15; RUL006 rounds2/shieldRounds2; pending visual IDs cleared"),
        "canBeImbued": (False, "RUL-2026-10-10-007"),
        "canBeCrafted": (False, "RUL-2026-10-11-004 drop-only"),
        "craftingExperience": (0, "RUL-2026-10-11-004 drop-only"),
        "hidden": (True, "creation doctrine; no publication"),
        **{f: (None, "presentation pending; validation/battle helper uses labelled placeholders") for f in PRESENTATION},
    }
    katana, katana_prov = derived(nt, k_over, "Night's Testament; RUL004 approved non-effect baseline")
    r4_diff = diff(load(R4_KATANA)["record"], katana)
    assert r4_diff == [{"path": "/effects/2/power", "before": 40, "after": 15},
                       {"path": "/effects/2/rounds", "before": 0, "after": 2},
                       {"path": "/effects/2/shieldRounds", "before": 3, "after": 2}], r4_diff
    old = load(CARRIERS_3X3)
    k33_diff = diff(old["katana"]["record"], katana)
    assert k33_diff == [{"path": "/effects/2/rounds", "before": 3, "after": 2},
                        {"path": "/effects/2/shieldRounds", "before": 3, "after": 2}], k33_diff

    fs_cap = load(FS_CAPTURE)["captures"][8]
    fs = fs_cap["data"]["items"][0]["item"]
    assert fs["id"] == "1GmiQAGuBZZsjIFqcqPkR" and fs["weaponType"] == "SWORD"
    c_over = {
        "name": ("Skyglass Crystal", "approved item name (reward decisions)"),
        "itemType": ("CRYSTAL", "RUL005/006 category"),
        "crystalTargetTypes": ("WEAPON", "RUL005/006 weapon-only"),
        "effects": ([consume(c_spec)], "RUL005 sole Consume10; RUL006 rounds2/shieldRounds2"),
        "rarity": ("LEGENDARY", "RUL-2026-10-11-006"),
        "canBeTraded": (True, "RUL-2026-10-11-006"),
        "canBeCrafted": (False, "RUL-2026-10-11-006; 12-Filament recipe removed"),
        "craftingExperience": (0, "inert with canBeCrafted:false; RUL006 removes the recipe"),
        "craftingRequirements": ([], "RUL-2026-10-11-006: no recipe in new construction"),
        "inShop": (False, "RUL006 acquisition is the independent 3% Reliquary drop only"),
        "hidden": (True, "creation doctrine; no publication"),
        "canBeImbued": (False, "a Crystal is not an imbue recipient"),
        "weaponType": ("NONE", "crystal shape"),
        "slot": ("ITEM", "crystal shape"),
        "target": ("SELF", "crystal shape; Consume target is SELF"),
        "method": ("SINGLE", "crystal shape"),
        "range": (0, "crystal shape"),
        **{f: (None, "presentation pending; validation helper uses labelled placeholders") for f in PRESENTATION},
    }
    crystal, crystal_prov = derived(fs, c_over, "Flaming Sword shape donor; UNAPPROVED carrier value")
    unapproved = sorted(k for k, p in crystal_prov.items() if p["source"] != "override" and k in CRYSTAL_UNAPPROVED)
    assert unapproved == CRYSTAL_UNAPPROVED, unapproved
    c33_diff = diff(old["crystal"]["record"], crystal)
    return {
        "schema": "tnr.ghost_ship_skyglass_final_item_records.v1",
        "status": "FINAL_2X2_CANDIDATE_RECORDS; RUNTIME_VALIDATION_IN_THIS_PACKAGE; PRESENTATION_AND_CRYSTAL_CARRIER_FIELDS_PENDING; NOT_A_WRITE_MANIFEST",
        "ruling": contract["ruling"], "designCommit": DESIGN, "engineCommit": ENGINE,
        "contract": {"file": CONTRACT, "sha256": digest(CONTRACT)},
        "timing": {"consumeRounds": 2, "generatedShieldRounds": 2, "approved": True, "ruling": "RUL-2026-10-11-006"},
        "consumeOverlap": "DIRECTOR_DEFERRED; native behaviour preserved; no restriction or correction",
        "historical": {
            "r4Katana": {"file": R4_KATANA, "sha256": digest(R4_KATANA), "tnrCommit": "3f825562ea051306a3803f47428b742ae5100011", "katanaDiff": r4_diff},
            "activeConsume3x3": {"file": CARRIERS_3X3, "sha256": digest(CARRIERS_3X3), "tnrCommit": "fcd79e5a3401dc8d95abbdaa05d0d4664c04a6e2",
                                 "katanaDiff": k33_diff, "crystalDiff": c33_diff},
        },
        "katana": {
            "status": "RUL004_BASELINE + RUL005_RATE + RUL006_TIMING; PRESENTATION_PENDING",
            "baseline": {"capture": NT_CAPTURE, "captureSha256": digest(NT_CAPTURE), "pointer": "/captures/0/data",
                         "id": nt["id"], "name": nt["name"], "capturedAt": nt_cap.get("at")},
            "droppedFields": DROPPED, "presentationPending": PRESENTATION,
            "record": katana, "provenance": katana_prov,
        },
        "crystal": {
            "status": "RUL005/006 DECIDED FIELDS + UNAPPROVED SHAPE-DONOR CARRIER FIELDS; PRESENTATION_PENDING",
            "baseline": {"capture": FS_CAPTURE, "captureSha256": digest(FS_CAPTURE), "pointer": "/captures/8/data/items/0/item",
                         "id": fs["id"], "name": fs["name"], "capturedAt": fs_cap.get("at")},
            "droppedFields": DROPPED, "presentationPending": PRESENTATION,
            "unapprovedCarrierFields": {k: crystal[k] for k in CRYSTAL_UNAPPROVED},
            "absentEconomyFields": ["auctionMinPrice", "auctionMaxPrice", "purchaseLimit", "purchaseLimitPeriod"],
            "note": "Unapproved carrier values validate but are not proposals. Absent economy fields take validator defaults (null/NONE). No live ID, cost or Filament policy is invented.",
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
    print(f"wrote {OUT} (final 2/2 candidates: Katana15 / Crystal10)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
