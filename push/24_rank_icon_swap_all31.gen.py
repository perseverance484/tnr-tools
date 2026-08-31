"""Generates push/24_rank_icon_swap_all31.zip - the icon swap, all 31 of our missions.

Every questRank here is read live from the census bundle (tnr_results_1788134455342):
no asserted ranks. Each entry patches `image` only; the builder fetch-merges the live
record, so no content, rewards or flow are touched. The four icons ride the zip with a
byte ledger, so nothing is picked by hand and no raw URL is transcribed.
"""
import json, os, shutil, zipfile

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.join(R, "harvests/inbox/tnr_results_1788134455342.json")
SRC = os.path.join(R, "skills/producing-tnr-art/data/rank_icons")
ICON = {"D": "icon_rank_D.webp", "C": "icon_rank_C.webp",
        "B": "icon_rank_B.webp", "A": "icon_rank_A.webp"}

cb = json.load(open(CENSUS))
quests = []
for c in cb["captures"]:
    if c.get("proc") != "quests.get":
        continue
    assert c.get("status") == 200, c.get("input")
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    quests.append(r)
assert len(quests) == 31, len(quests)
assert len({q["id"] for q in quests}) == 31

items = []
for q in sorted(quests, key=lambda q: (q["questRank"], q["name"])):
    rank = q["questRank"]
    assert rank in ICON, (q["name"], rank)
    items.append({"entity": "quest", "slot": "edit",
                  "name": "%s [%s]" % (q["name"], rank),
                  "targetId": q["id"],
                  "data": {"image": "@img:" + ICON[rank]}})
assert len(items) == 31

used = sorted({i["data"]["image"].split(":", 1)[1] for i in items})
assert used == sorted(ICON.values()), used
imgsz = {f: os.path.getsize(os.path.join(SRC, f)) for f in used}

# read-back: re-read every record after the swap rather than trusting a green row
after = [{"proc": "quests.get", "input": {"id": i["targetId"]}} for i in items]
man = {"items": items, "imgSizes": imgsz, "capture": {"after": after}}

work = os.path.join(R, "..", "work_pack24")
work = os.path.abspath(work)
os.makedirs(work, exist_ok=True)
open(os.path.join(work, "manifest.json"), "w").write(json.dumps(man, indent=1))
for f in used:
    shutil.copy(os.path.join(SRC, f), os.path.join(work, f))
out = os.path.join(R, "push/24_rank_icon_swap_all31.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(work, "manifest.json"), "manifest.json")
    for f in used:
        z.write(os.path.join(work, f), f)
print("wrote", out)
import collections
print("items", len(items), "by rank", dict(collections.Counter(q["questRank"] for q in quests)))
print("read-backs", len(after))
