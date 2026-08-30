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
items = []
for name in sorted(live, key=lambda n: (live[n]["questRank"], n)):
    r = live[name]
    rank = r["questRank"]
    assert rank in ICON and r["questType"] == "mission", (name, rank, r["questType"])
    items.append({"entity": "quest", "slot": "edit", "name": "%s [%s icon]" % (name, rank),
                  "targetId": r["id"], "data": {"image": "@img:" + ICON[rank]}})
assert len(items) == 10

used = sorted({i["data"]["image"].split(":", 1)[1] for i in items})
SRC = os.path.join(R, "skills/producing-tnr-art/data/rank_icons")
imgsz = {f: os.path.getsize(os.path.join(SRC, f)) for f in used}
probe = [{"proc": "quests.getAll", "input": {"limit": 25, "cursor": 0}},
         {"proc": "quests.getAll", "input": {"questType": "mission", "limit": 25, "cursor": 0}}]
man = {"capture": {"before": cap + probe}, "items": items, "imgSizes": imgsz}

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
