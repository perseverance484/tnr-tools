import json, os, zipfile, shutil
R = "/home/claude/tnr-tools"
NEW = os.path.join(R, "harvests/inbox/tnr_results_1788127352899.json")
NAMES = os.path.join(R, "harvests/inbox/tnr_results_1788110429856.json")

nb = json.load(open(NEW))
# live quest records captured tonight -> rank + id, extracted, never transcribed
live = {}
for c in nb["captures"]:
    if c.get("proc") == "quests.get":
        r = c["data"]
        if isinstance(r, dict) and "data" in r: r = r["data"]
        if isinstance(r, list): r = r[0]
        live[r["name"]] = r
assert len(live) == 10, len(live)

nn = json.load(open(NAMES))
allnames = None
for c in nn["captures"]:
    if c.get("proc") == "quests.getAllNames":
        allnames = c["data"]["data"] if isinstance(c["data"], dict) else c["data"]
assert allnames and len(allnames) == 415
byname = {}
for r in allnames: byname.setdefault(r["name"], r)

CAPTURE_NAMES = [
 "Well Rounds","The Runaway Goat","Poachers' Due","One White Ear","Night Watch Shadow",
 "The Misfiled Board","The Long Road","Lantern Rounds","The Cartographer's Satchel",
 "The Cartographer's Ink",
 "Case Contract: Courier Intercept","Case Contract: Ledger Sweep","Case Contract: Route Watch",
 "Case Contract: Site Sweep",
 "Blacksteel Contract: Cleanup Detail","Blacksteel Contract: Iron Hunt",
 "Blacksteel Contract: Perimeter Breach","Blacksteel Contract: Shard Salvage",
 "Blacksteel Contract: Supply Raid",
 "Copies, Not Thefts","Witness Detail",
]
missing = [n for n in CAPTURE_NAMES if n not in byname]
assert not missing, missing
cap = [{"proc": "quests.get", "input": {"id": byname[n]["id"]}} for n in CAPTURE_NAMES]
assert len({c["input"]["id"] for c in cap}) == 21

ICON = {"D": "icon_rank_D.webp", "C": "icon_rank_C.webp", "B": "icon_rank_B.webp", "A": "icon_rank_A.webp"}

# Rank source per quest. "live" = questRank read from tonight's quests.get capture.
# "asserted" = not yet read live; carried on the stated evidence and re-read by
# capture.before in this same bundle, so a wrong one shows up in the results.
ASSERTED = {
    # the ten D-set missions - every one has a matching 'DM Icon <name>' asset in the
    # dmissionicons folder, which is the D-rank icon set being retired
    "Well Rounds": "D", "The Runaway Goat": "D", "Poachers' Due": "D",
    "One White Ear": "D", "Night Watch Shadow": "D", "The Misfiled Board": "D",
    "The Long Road": "D", "Lantern Rounds": "D", "The Cartographer's Satchel": "D",
    "The Cartographer's Ink": "D",
    # board record: B x4 = Nothing to Report / The Loud Way / these two
    "Copies, Not Thefts": "B", "Witness Detail": "B",
}
items = []
for name in sorted(live, key=lambda n: (live[n]["questRank"], n)):
    r = live[name]
    rank = r["questRank"]
    assert rank in ICON and r["questType"] == "mission", (name, rank, r["questType"])
    items.append({"entity": "quest", "slot": "edit", "name": "%s [%s icon, rank live]" % (name, rank),
                  "targetId": r["id"], "data": {"image": "@img:" + ICON[rank]}})
for name in sorted(ASSERTED, key=lambda n: (ASSERTED[n], n)):
    assert name not in live, name
    rank = ASSERTED[name]
    assert rank in ICON
    items.append({"entity": "quest", "slot": "edit", "name": "%s [%s icon, rank asserted]" % (name, rank),
                  "targetId": byname[name]["id"], "data": {"image": "@img:" + ICON[rank]}})
assert len(items) == 22
assert len({i["targetId"] for i in items}) == 22

used = sorted({i["data"]["image"].split(":", 1)[1] for i in items})
SRC = os.path.join(R, "skills/producing-tnr-art/data/rank_icons")
imgsz = {f: os.path.getsize(os.path.join(SRC, f)) for f in used}
man = {"capture": {"before": cap}, "items": items, "imgSizes": imgsz}

os.makedirs("pack", exist_ok=True)
open("pack/manifest.json", "w").write(json.dumps(man, indent=1))
for f in used: shutil.copy(os.path.join(SRC, f), os.path.join("pack", f))
out = os.path.join(R, "push/22_rank_icon_wiring_wave1.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.write("pack/manifest.json", "manifest.json")
    for f in used: z.write(os.path.join("pack", f), f)
print("wrote", out)
print("captures", len(cap), "items", len(items), "imgs", used)
for i in items: print(" ", i["targetId"], i["name"], i["data"]["image"])
