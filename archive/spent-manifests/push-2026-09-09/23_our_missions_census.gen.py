"""Generates push/23_our_missions_census.json - capture-only, zero mutations.

Reads every one of our 31 authored missions plus the full gameAsset table, so that
(a) the icon swap can be built on live questRank for all 31 instead of 22 live + 9
unknown, and (b) the delete list is cut from a fresh asset snapshot taken in the
same breath, with every mission's pre-swap image URL captured before it is overwritten.
Ids are extracted from bundle captures, never transcribed.
"""
import json, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW = os.path.join(R, "harvests/inbox/tnr_results_1788127352899.json")
NAMES = os.path.join(R, "harvests/inbox/tnr_results_1788110429856.json")

nb = json.load(open(NEW))
live = {}
for c in nb["captures"]:
    if c.get("proc") == "quests.get":
        r = c["data"]
        if isinstance(r, dict) and "data" in r: r = r["data"]
        if isinstance(r, list): r = r[0]
        live[r["name"]] = r["id"]
assert len(live) == 10, len(live)

nn = json.load(open(NAMES))
allnames = None
for c in nn["captures"]:
    if c.get("proc") == "quests.getAllNames":
        allnames = c["data"]["data"] if isinstance(c["data"], dict) else c["data"]
assert allnames and len(allnames) == 415
byname = {}
for r in allnames: byname.setdefault(r["name"], r)

OURS = [
    # Forsworn C/B/A - 10 of these have live rank already; re-read so the whole
    # census is one consistent snapshot
    "The Waystation", "Chalk and Corner", "Protection", "The Empty Contract",
    "Nothing to Report", "The Loud Way", "Copies, Not Thefts", "Witness Detail",
    "Three Rounds", "The Long Winter", "Old Ghost", "The Tenth Name",
    # D-set - rank never read live
    "Well Rounds", "The Runaway Goat", "Poachers' Due", "One White Ear",
    "Night Watch Shadow", "The Misfiled Board", "The Long Road", "Lantern Rounds",
    "The Cartographer's Satchel", "The Cartographer's Ink",
    # contracts - ours, ruled in scope, rank never read live
    "Case Contract: Courier Intercept", "Case Contract: Ledger Sweep",
    "Case Contract: Route Watch", "Case Contract: Site Sweep",
    "Blacksteel Contract: Cleanup Detail", "Blacksteel Contract: Iron Hunt",
    "Blacksteel Contract: Perimeter Breach", "Blacksteel Contract: Shard Salvage",
    "Blacksteel Contract: Supply Raid",
]
assert len(OURS) == 31 and len(set(OURS)) == 31
missing = [n for n in OURS if n not in byname]
assert not missing, missing
for n, i in live.items():
    assert byname[n]["id"] == i, (n, byname[n]["id"], i)   # two sources agree on every id

reads = [{"proc": "quests.get", "input": {"id": byname[n]["id"]}} for n in OURS]
reads.append({"proc": "gameAsset.getAll", "input": {"limit": 500, "cursor": 0}})
assert len({r["input"].get("id") for r in reads if r["proc"] == "quests.get"}) == 31

man = {"capture": {"before": reads}, "items": []}
out = os.path.join(R, "push/23_our_missions_census.json")
open(out, "w").write(json.dumps(man, indent=1))
print("wrote", out, "-", len(reads), "reads, 0 mutations")
