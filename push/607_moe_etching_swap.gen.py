#!/usr/bin/env python3
"""607: swap the 605 etching colour art into the 7 MoE etching jutsu.

Usage: python3 push/607_moe_etching_swap.gen.py harvests/inbox/<605 results>.json
Reads state/moe_etch_colours/etch7_full_20261113.json (full live records, read 21:43Z),
state/moe_etch_colours/asset_map.json (live slice id -> 605 srcId) and the 605 results
idmap (srcId -> new asset id). Writes push/607_moe_etching_swap.json.
Phases: 10 unequip (law 18), 15 unhide the 258 new assets, 20 jutsu effects with the new
appearAnimation and animationScale 2.5 on every art effect, 30 full kits back.
"""
import json, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
res = json.load(open(sys.argv[1]))
assert res.get("journal", {}).get("manifestNumber") == 605, "not a 605 results bundle"
assert res.get("outcome") == "success", res.get("outcome")
idmap = res["idmap"]
recs = json.load(open(root / "state/moe_etch_colours/etch7_full_20261113.json"))
amap = json.load(open(root / "state/moe_etch_colours/asset_map.json"))["jutsu"]

GLASS = "H3pNj2qUWpMpVRINiH6Vn"; SAINT = "k0hgSrghl_KcYs9ATVDJT"
GLASS_KIT = ["-MtfLHClmIwSSGBIw9O7X","0g0Iy9PKsIVC6ggG1Exz2","2pU7fdUPQPQQjyd19JDWA","54nmWiFXqvFW7u0vSG5zK","6Pe__8eUXSMQYZlP4o6jY","Avu4B2M_9_SE0-Oqqhplw","BeOpXT1M_7oRkwYCcXk6Z","eovhl9XyDQq1N19lDwr77","Et0ZiYFsvqelXKBLdL5xj","F5qD1aXjt-kPQ6IR7nDoo","G_b5yaxm6GMOuQ3eaofKb","I5lwaFCaVSH6cpxAPHvFA","JilCGgeP6-sIoY9FjbvAj","K702_TNz_99W53EIXOmp1","KIwfifD8OGNVbs9I8O6Rw","l1TpeIKJyNDzQQkI1Az1K","lkcsor1I5A8gD038ncrBW","lmlhn5p68Oszhj16wKbvx","nNUaP5r8r7UxYNiAtuF0l","Pr7i3DK5KiRQRePy8Xw41","S9AUnSu9A0qnShbtI2FdV","yzI6KIOPzy6P2B0U6Cqyp","Zny2xURYBn9gTwYA99X-q"]
SAINT_KIT = ["0yple4t11fS5B6F2fYbad","1p44ivUB8TjzaPFiqyitx","2z3YsMSEzMK7R49pYhlX1","6ixza9w2RBvRD48dMWPFc","6P9RJUe64Nwes1gWvsoJa","9lSbi9Zy1xTeGhE9DQgUF","a-LtVaVvVHN6LcvhA-Jla","D6iaypIXK3-gQeNV5tCQi","DOZXlM7mjxqszpLdVhN-r","dpcEjvUOy58-KE0_H6v8D","edEaSEaOJ08dyDAGa9PKv","eovhl9XyDQq1N19lDwr77","EXkpU9iaPS5poSvlAYaxu","G_b5yaxm6GMOuQ3eaofKb","lkcsor1I5A8gD038ncrBW","LS6aApTpLhkEE76EOuf66","Ltj0rYwo2a4VGV3JXr976","mZRQTuyZVYgAukuxle8OL","nNUaP5r8r7UxYNiAtuF0l","qrSWUp7qT6a-djyQV-HVi","TwapdTPQAxVoj1sdLipJv","wYMWB84DZyFeAqTEoB1td","xWDUss579mnkoUiSn-fTt","Z6vdY9Ir1kKEZouZ-hzY9","ZxhhjjP4-msn4gjP5Ss0j"]
ETCH = list(recs)
items = [
  {"entity":"ai","slot":"edit","targetId":GLASS,"phase":10,"name":"Sayo, Glasswright: etching jutsu off (law 18)","data":{"jutsus":[j for j in GLASS_KIT if j not in ETCH]}},
  {"entity":"ai","slot":"edit","targetId":SAINT,"phase":10,"name":"Sayo, Saint: Rime, Ember, Heart off (law 18)","data":{"jutsus":[j for j in SAINT_KIT if j not in ETCH]}},
]
new_ids = []
for jid, r in recs.items():
    m = amap[jid]["map"]
    effs = []
    for e in r["effects"]:
        e = dict(e)
        if e["type"] == "visual":
            nid = idmap[m[e["appearAnimation"]]]
            new_ids.append(nid); e["appearAnimation"] = nid; e["animationScale"] = 2.5
        effs.append(e)
    items.append({"entity":"jutsu","slot":"edit","targetId":jid,"phase":20,"name":f"{r['name']}: colour art at 2.5x","data":{"effects":effs,"injectableInBattle":r["injectableInBattle"]}})
assert len(new_ids) == len(set(new_ids)) == 258, len(set(new_ids))
for i, a in enumerate(new_ids):
    items.append({"entity":"asset","slot":"edit","targetId":a,"phase":15,"name":f"605 etching slice {i+1}: unhide","data":{"hidden":False}})
items += [
  {"entity":"ai","slot":"edit","targetId":GLASS,"phase":30,"name":"Sayo, Glasswright: full kit back","data":{"jutsus":GLASS_KIT}},
  {"entity":"ai","slot":"edit","targetId":SAINT,"phase":30,"name":"Sayo, Saint: full kit back","data":{"jutsus":SAINT_KIT}},
]
items.sort(key=lambda x: x["phase"])
out = {"_note":"607: MoE fix 4 part 2. 605's colour-coded etching art swapped into Etching Rime/Hail/Ember/Seam/Heart and Recast Heart/Seam (appearAnimation), art effects at 2.5x, 258 new slices unhidden. Law 18: Glasswright and Saint etching jutsu off, edit, full kits back. Gameplay effects untouched; jutsu stay hidden.","items":items}
json.dump(out, open(root/"push/607_moe_etching_swap.json","w"), indent=1)
print("items", len(items))
