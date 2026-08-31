"""push/25_mission_census_probe.json - capture-only, sizes the full mission census.

The hide half needs every mission in the game, not just ours, and quests.getAll has
never been called from this toolchain: it is unknown whether it returns fat rows
(content and objectives, ~380 of them) or trimmed listing rows. Pulling limit 500
blind could push megabytes through Firefox mobile and the sync token. These three
small reads settle the row shape and per-row cost first.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
man = {"capture": {"before": [
    {"proc": "quests.getAll", "input": {"limit": 5, "cursor": 0}},
    {"proc": "quests.getAll", "input": {"questType": "mission", "limit": 25, "cursor": 0}},
    {"proc": "quests.getAll", "input": {"questType": "mission", "limit": 25, "cursor": 1}},
]}, "items": []}
out = os.path.join(R, "push/25_mission_census_probe.json")
open(out, "w").write(json.dumps(man, indent=1))
print("wrote", out, "-", len(man["capture"]["before"]), "reads, 0 mutations")
