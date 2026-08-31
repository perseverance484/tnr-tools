"""push/34_old_ghost_prose.json - Old Ghost prose pass, rulings 1a / 6 / 8.

1a: g30 SPLIT into three route-specific endings. g30 keeps the ask-around route (fed by
    g16, east verge), g30b takes the contact route (g24, dye works), g30c takes the
    stakeout route (g31, foot of the wall). All three converge on g32 as before, so the
    officer scene is untouched.
6:  "Bingo Book" retired for BOUNTY CONTRACT throughout.
8:  silent portrait carried to all three endings - each new node takes Forsworn Scene -
    Old Ghost, the portrait g30 already had, over the background of the fight that led to
    it (East Road Ambush Site / Drying Yard / Back Alley Night).

Also: g34 rewritten off g33's borrowed sentence, g35's exit choice no longer repeats its own
closing line, g15 pronoun tangle untangled.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(R, "harvests/inbox/tnr_results_1788135094828.json")
for c in json.load(open(SRC))["captures"]:
    if c.get("proc") != "quests.get": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    if r["name"] == "Old Ghost": q = json.loads(json.dumps(r))
objs = {o["id"]: o for o in q["content"]["objectives"]}
OG_PORTRAIT = objs["g30"]["sceneCharacters"][0]
BG = {"g30": objs["g16"]["sceneBackground"],      # east verge
      "g30b": objs["g24"]["sceneBackground"],     # dye works
      "g30c": objs["g31"]["sceneBackground"]}     # foot of the wall
FILED = "You file it that night. Old Ghost. Bounty contract. Taken inside the village."

END = {
 "g30": ("He is down at the verge with his business already concluded and nothing on him to show "
         "what it was. <br> <br> He was finished by noon. You spent the day walking, and he let "
         "you. <br> <br> " + FILED),
 "g30b": ("Three down in a dye works yard, and the lights still on in a building with no reason to "
          "have them. <br> <br> He waited for the other two to commit before he moved once, which "
          "is how he has stayed on that contract as long as he has. <br> <br> " + FILED),
 "g30c": ("Alone at the foot of the wall, with the two he left behind still in a lane on the other "
          "side of the slope. <br> <br> He ran out of village before he ran out of breath, and he "
          "never once looked back at them. <br> <br> " + FILED),
}
for nid, text in END.items():
    o = objs["g30"] if nid == "g30" else json.loads(json.dumps(objs["g30"]))
    o["id"] = nid
    o["description"] = text
    o["sceneCharacters"] = [OG_PORTRAIT]
    o["sceneBackground"] = BG[nid]
    o["nextObjectiveId"] = [{"text": '"I got him."', "nextObjectiveId": "g32"}]
    if nid != "g30":
        q["content"]["objectives"].append(o)
        objs[nid] = o
objs["g24"]["nextObjectiveId"] = "g30b"
objs["g31"]["nextObjectiveId"] = "g30c"
assert objs["g16"]["nextObjectiveId"] == "g30"

# ruling 6 - bounty contract
objs["g2"]["description"] = ("An old bounty contract, faded and worn, pinned to the board with a fresh "
    "mission brief. <br> <br> Old Ghost. Resurfaced after years in hiding.")
objs["g33"]["description"] = ('"I believe your report. I have believed four of them." <br> <br> She signs '
    'it and does not close the contract. <br> <br> "He was ANBU here once. I was on the road the first '
    'time somebody confirmed him dead. Take the pay and do not think about it too hard."')
objs["g35"]["description"] = ('"Because he taught me how to be sure." <br> <br> She does not look up from '
    'the page. <br> <br> "That is all you get. The contract stays open. It always does."')
objs["g36"]["description"] = ("The pay is A rank and it clears the same day. <br> <br> The contract stays open.")
objs["g_win"]["description"] = "Report filed. Contract open."

# g34 off g33's borrowed sentence
objs["g34"]["description"] = ("The pen moves. She does not look up while it does, and the contract is still "
    "open when she sets it down. <br> <br> When you are at the door she says it to your back. <br> <br> "
    '"Many have reported the same. Myself included."')
# g35 exit choice no longer repeats g35's last line
objs["g35"]["nextObjectiveId"] = [{"text": "Take the pay.", "nextObjectiveId": "g_win"}]
# g15 pronoun tangle
objs["g15"]["description"] = ("By dusk you have four addresses. Three are empty. The fourth is a woman who "
    "has never heard the name, and who flinched when she heard it anyway. <br> <br> Not at you. At the "
    "name. <br> <br> Whoever he came to meet, he met them on this street, and he is already done.")

allids = {o["id"] for o in q["content"]["objectives"]}
assert len(allids) == len(q["content"]["objectives"]) == 47
blob = json.dumps(q["content"])
assert "Bingo Book" not in blob and "—" not in blob and "–" not in blob
for o in q["content"]["objectives"]:
    nxt = o.get("nextObjectiveId")
    for t in ([c["nextObjectiveId"] for c in nxt] if isinstance(nxt, list) else ([nxt] if nxt else [])):
        assert t in allids, (o["id"], t)
    if o.get("failObjectiveId"): assert o["failObjectiveId"] in allids
    if isinstance(nxt, list):
        tg = [c["nextObjectiveId"] for c in nxt]
        assert len(set(tg)) == len(tg), (o["id"], tg)
data = {k: v for k, v in q.items() if k not in ("createdAt", "updatedAt", "village")}
man = {"items": [{"entity": "quest", "slot": "edit", "name": "Old Ghost [prose pass]",
                  "targetId": q["id"], "data": data}],
       "capture": {"after": [{"proc": "quests.get", "input": {"id": q["id"]}}]}}
open(os.path.join(R, "push/34_old_ghost_prose.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/34 - 45 -> 47 objectives; endings g30 / g30b / g30c")
