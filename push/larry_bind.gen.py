#!/usr/bin/env python3
"""Larry's Undertow: tie every dialog step to Larry's overworld placement (director go 2026-11-09 20:21).

    python3 push/larry_bind.gen.py --from <549 bundle>   -> push/550_larry_dialog_bind.json  (LIVE edit)

Why: an overworld quest whose dialog steps carry no overworldPlacementId shows only blind choices in the logbook
(layout/Logbook.tsx LogbookEntry renders the scene only with showScene). With the binding, tapping Larry opens the
NPC Dialog window (scene, characters, text, choices) and spends no daily roll (server/api/routers/overworldAi.ts:
bound objectives are checked before the quest roll). The full record is rebuilt from the 549 capture; the only change
is the added overworldPlacementId on dialog objectives. Objective ids are unchanged, so players mid-quest keep their place.
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QID, PLACEMENT = "4pNH8x9ZOOoIyERKSmPa-", "tXSxW0uwZCHFHA-crlzBj"
DROP = {"id", "createdAt", "updatedAt", "raidBossMaxHealth", "raidBossCurrentHealth", "raidStartedAt", "raidEndsAt",
        "raidCaptureDeadline", "raidGracePeriodEnd"}

ap = argparse.ArgumentParser()
ap.add_argument("--from", dest="bundle", required=True)
a = ap.parse_args()
b = json.load(open(a.bundle))
live = next(c["data"] for c in b["captures"] if c["proc"] == "quests.get" and c["input"]["id"] == QID)
assert live["name"] == "Larry's Undertow" and live["questType"] == "overworld" and live["consecutiveObjectives"]
data = {k: v for k, v in live.items() if k not in DROP}
# Gate laws 72/42: drop nulls the write validator doesn't know and inert NONE ranks (defaults are the same).
for k in ["petTaskMinutes", "requiredNinjutsuMastery", "requiredGenjutsuMastery", "requiredTaijutsuMastery",
          "requiredBukijutsuMastery", "requiredBloodlineMastery", "requiredSageMastery"]:
    if data.get(k) is None: data.pop(k, None)
for k in ["huntingRank", "gatheringRank", "medicalRank"]:
    if data.get(k) == "NONE": data.pop(k)
n = 0
for o in data["content"]["objectives"]:
    if o["task"] == "dialog":
        assert not o.get("overworldPlacementId"), "already bound: stale capture or 550 ran"
        o["overworldPlacementId"] = PLACEMENT
        n += 1
out = os.path.join(ROOT, "push/550_larry_dialog_bind.json")
json.dump({"_note": f"push/550, LIVE: Larry's Undertow ({QID}), {n} dialog steps tied to Larry's placement "
                    f"({PLACEMENT}) so taps on Larry show the scenes. Built from {os.path.basename(a.bundle)} by "
                    "push/larry_bind.gen.py; do not hand-edit.",
           "items": [{"entity": "quest", "slot": "edit", "targetId": QID, "phase": 1,
                      "name": "Larry's Undertow: dialog tied to Larry", "data": data}]},
          open(out, "w"), indent=1, ensure_ascii=False)
print(out, n)
