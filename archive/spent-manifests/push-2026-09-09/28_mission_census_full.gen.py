"""push/28_mission_census_full.json - capture-only, the full mission table.

The probe settled the shape: quests.getAll returns FAT rows - full content, objectives
and all - at roughly 17-22KB per mission, and `cursor` is a page index. So the census is
paged at 50, not pulled at 500.

Scale correction: there are 87 missions in the game, not the ~380 assumed earlier. That
number came from the 415-row all-quests list, which is mostly events, story, achievement,
gathering and hunting - none of which are in scope. 30 of the 87 are ours (One White Ear
is questType event, so it is not among them), leaving 57 candidates for the hide list.

Two pages cover 87 rows; the third is a guard in case the table grew. Expect a bundle
around 1.5-2MB.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
reads = [{"proc": "quests.getAll", "input": {"questType": "mission", "limit": 50, "cursor": c}}
         for c in (0, 1, 2)]
man = {"capture": {"before": reads}, "items": []}
out = os.path.join(R, "push/28_mission_census_full.json")
open(out, "w").write(json.dumps(man, indent=1))
print("wrote", out, "-", len(reads), "paged reads, 0 mutations")
