"""push/33_copies_converging_fix.json - fixes the three converging menus in Copies, Not Thefts.

validate.py and the builder preflight both reject this record on a1, a2 and f1. All three
are menus where the options do not lead anywhere different, so the player's input is
decorative. The fix gives the distinct questions distinct answers rather than deleting the
options, which is the cheaper fix but loses the writing.

Four new dialog nodes: a1b, a1c, a2b, f4. Every one clones the field set of its neighbour
in the same scene, so scene character, background and the other 35 keys stay consistent.

Base is the CURRENT live record (post scene-character retirement), full content sent, so
nothing else in the flow moves.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(R, "harvests/inbox/tnr_results_1788135994502.json")

for c in json.load(open(SRC))["captures"]:
    if c.get("proc") != "quests.get": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    q = json.loads(json.dumps(r))
assert q["name"] == "Copies, Not Thefts"
objs = {o["id"]: o for o in q["content"]["objectives"]}
assert {"a1", "a2", "f1", "f2", "f3", "a3", "l1"} <= set(objs)

def clone(template, new_id, text, nxt_id, nxt_label):
    o = json.loads(json.dumps(objs[template]))
    o["id"] = new_id
    o["description"] = text
    o["nextObjectiveId"] = [{"text": nxt_label, "nextObjectiveId": nxt_id}]
    o.pop("failObjectiveId", None) if objs[template].get("failObjectiveId") is None else None
    return o

A1B = ("<i> She does not answer straight away. </i> <br> <br> "
       "\"A private archive does not buy anything. It stores, and it sells access. "
       "Whoever paid is a line in their ledger, which is why I want the ledger and not the archivist.\"")
A1C = ("<i> She lets the question sit longer than it deserves. </i> <br> <br> "
       "\"Openly means a village that knows its letters were read. That is a different problem than the one "
       "I have tonight.\" <br> <br> \"And four people sent openly are four people who can be counted.\"")
A2B = ("\"Then it is watched by men paid to watch a door, not by men paid to expect you.\" <br> <br> "
       "<i> She does not look up from the map. </i> <br> <br> "
       "\"Come back out the way you find it. If that means the front, use the front.\"")
F4 = ("<i> The clerk's pen stops. </i> <br> <br> \"The Kage's office does not hold an account here.\" <br> <br> "
      "He says it politely, and he says it loudly enough for the two men by the stair. The writ does not come "
      "back to you, and neither does the conversation.")

new = [
    clone("a1", "a1b", A1B, "a2", "Go on."),
    clone("a1", "a1c", A1C, "a2", "Go on."),
    clone("a2", "a2b", A2B, "a3", "Understood."),
    clone("f1", "f4",  F4,  "l1", "Leave before they decide. The roof, then."),
]

objs["a1"]["nextObjectiveId"] = [
    {"text": "Who bought them?", "nextObjectiveId": "a1b"},
    {"text": "Why is ANBU not handling this openly?", "nextObjectiveId": "a1c"}]
objs["a2"]["nextObjectiveId"] = [
    {"text": "Understood.", "nextObjectiveId": "a3"},
    {"text": "And if the door is watched?", "nextObjectiveId": "a2b"}]
objs["f1"]["nextObjectiveId"] = [
    {"text": "The autumn index.", "nextObjectiveId": "f2"},
    {"text": "The index for the year, all of it.", "nextObjectiveId": "f3"},
    {"text": "Whichever one the Kage's office uses.", "nextObjectiveId": "f4"}]

# ruling 4 (dauntless): l4, c6 and d5 carried empty descriptions - both failure resets and
# the win node showed the player a blank screen. Old Ghost and The Tenth Name both give
# these a line.
FILL = {
    "l4": ("The bell rings twice more before anybody reaches it, and by then the alley is empty "
           "in both directions. <br> <br> Whatever was worth guarding tonight will not be there "
           "tomorrow."),
    "c6": ("You come to on the floor of the stacks with your kit gone and the drawer sealed again. "
           "<br> <br> The ledger is back on its shelf, in order, as though nobody had ever asked "
           "for it."),
    "d5": "Ledger copied. Files out. Nobody knows you were there.",
}
for _id, _text in FILL.items():
    assert not (objs[_id].get("description") or "").strip(), _id
    objs[_id]["description"] = _text

q["content"]["objectives"].extend(new)
allids = {o["id"] for o in q["content"]["objectives"]}
assert len(allids) == 29 == len(q["content"]["objectives"])
for o in q["content"]["objectives"]:                      # every edge resolves
    nxt = o.get("nextObjectiveId")
    for t in ([c["nextObjectiveId"] for c in nxt] if isinstance(nxt, list) else ([nxt] if nxt else [])):
        assert t in allids, (o["id"], t)
    if o.get("failObjectiveId"): assert o["failObjectiveId"] in allids, o["id"]
for mid in ("a1", "a2", "f1"):                            # no menu converges any more
    tg = [c["nextObjectiveId"] for c in objs[mid]["nextObjectiveId"]]
    assert len(set(tg)) == len(tg), (mid, tg)
for o in new:
    assert "—" not in o["description"] and "–" not in o["description"]
    assert o.get("sceneCharacters"), o["id"]

data = {k: v for k, v in q.items() if k not in ("createdAt", "updatedAt", "village")}
assert data["hidden"] is False
man = {"items": [{"entity": "quest", "slot": "edit", "name": "Copies, Not Thefts [converging menu fix]",
                  "targetId": q["id"], "data": data}],
       "capture": {"after": [{"proc": "quests.get", "input": {"id": q["id"]}}]}}
open(os.path.join(R, "push/33_copies_converging_fix.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/33 - 25 -> 29 objectives, new:", [o["id"] for o in new])
