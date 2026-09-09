"""push/35_tenth_name_prose.json - The Tenth Name prose pass, rulings 2 / 3 / 6.

2: Clanless CUT and the counting simplified. The quest previously said three fields, then
   four words, then four public facts, then four fields. It is now three throughout:
   three words, three sources, three lists. The x20 exit choice said "Four words." and now
   says "Three words."
3: ruled dependent on 2, so both items land - x25 plays the officer instead of narrating
   her, and x_win closes on the date rather than on "Page recovered."
6: "Bingo Book" retired for BOUNTY CONTRACT (x2).

NOT in this manifest: ruling 5 (x22-x28 speaker is a village official). Those nodes carry
ANBU Commander Portrait today and there is no village-official portrait in the asset table -
see the change note. Prose here stays speaker-neutral so the portrait swap is a one-field
follow-up, not a rewrite.
"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(R, "harvests/inbox/tnr_results_1788135094828.json")
for c in json.load(open(SRC))["captures"]:
    if c.get("proc") != "quests.get": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    if r["name"] == "The Tenth Name": q = json.loads(json.dumps(r))
objs = {o["id"]: o for o in q["content"]["objectives"]}

objs["x2"]["description"] = ('Ten entries. <br> <br> "Nine of them I recognise, because nine of them are '
    'lines off our own bounty contracts, copied in a hand that is not ours." <br> <br> "They keep a book '
    'on themselves. On its own that is a week\'s work."')

# ruling 2 - Clanless cut, counting simplified to three
objs["x20"]["description"] = ("The nine known entries carry the same three fields under the name. A year, "
    "a prefix, and a single word. <br> <br> Passed. Debt. Discipline. Passed. Debt. Discipline. Passed. "
    "Debt. Discipline.")
objs["x20"]["nextObjectiveId"] = [{"text": "Three words.", "nextObjectiveId": "x21"}]
objs["x21b"]["description"] = ("Promotion boards go up on a wall four times a year. The lending register is "
    "open to any creditor who asks. Discipline dockets are posted so the punishment is seen to be done. "
    "<br> <br> Three lists. All public, all ours. <br> <br> Nobody infiltrated anything. This village "
    "publishes the people it has disappointed, and somebody has been walking in and reading it.")
objs["x22"]["description"] = ("She reads the three words before she reads the tenth line. <br> <br> "
    '"Every one of these is on a wall somewhere in this village with my authority at the bottom of it." '
    '<br> <br> "They are not recruiting out of our ranks. They are standing at the bottom of a slope we '
    'built and pointed downhill."')
objs["x24"]["description"] = ('"Nothing at all. Which is the problem I am about to have upstairs, because '
    'the moment this goes up, everybody matching those three words becomes a watch list." <br> <br> "And '
    'then the date will be right for reasons we caused."')
objs["x27"]["description"] = ("Nobody knocks. The service number is never looked up. <br> <br> What goes "
    "upstairs is a proposal about the reading room, and it takes seven months and most of her remaining "
    "goodwill. <br> <br> It removes exactly one of the three lists. <br> <br> \"One of three means the next "
    "list is harder to build and less accurate. It is also the only one of the three that cost this village "
    "nothing to give up, which is why it is the one I got.\" <br> <br> \"Be angrier about that than I am "
    "able to be in this office.\"")
objs["x28"]["description"] = ("The page goes up with your report and the route drawn out in full. <br> <br> "
    "It comes back in nine days approved for circulation to section heads. Everybody matching those three "
    "words is now a name on a desk somewhere. <br> <br> \"They wanted it read. Now it is read by us as well, "
    "and I cannot decide whether that is counter-intelligence or doing their filing.\" <br> <br> She signs "
    "the circulation. <br> <br> \"Nine of those section heads will treat it as a warning about the village. "
    "One will treat it as a list of suspects. I do not get to choose which.\"")

objs["x23"]["description"] = ('"A forecast that will probably be right, which is worse. Nobody has '
    'spoken to this person. Nobody has offered them anything." <br> <br> "Somebody read three public '
    'facts and wrote a date, and on the evidence of the nine above it I would not bet against the date."')

# ruling 3
objs["x25"]["description"] = ("She has the page and the route, which is what she asked for. <br> <br> "
    '"What happens next is not a field decision." <br> <br> She does not put the page down. <br> <br> '
    '"You walked that route. Tell me what you think and then I will ignore you if I want to."')
objs["x_win"]["description"] = ("Page recovered. Route mapped. <br> <br> The tenth line is still eight "
    "months out.")

blob = json.dumps(q["content"])
for bad in ("Clanless", "Bingo Book", "four fields", "four public facts", "Four words", "—", "–"):
    assert bad not in blob, bad
allids = {o["id"] for o in q["content"]["objectives"]}
assert len(allids) == len(q["content"]["objectives"]) == 36
for o in q["content"]["objectives"]:
    nxt = o.get("nextObjectiveId")
    for t in ([c["nextObjectiveId"] for c in nxt] if isinstance(nxt, list) else ([nxt] if nxt else [])):
        assert t in allids, (o["id"], t)
    if isinstance(nxt, list):
        tg = [c["nextObjectiveId"] for c in nxt]
        assert len(set(tg)) == len(tg), (o["id"], tg)
data = {k: v for k, v in q.items() if k not in ("createdAt", "updatedAt", "village")}
man = {"items": [{"entity": "quest", "slot": "edit", "name": "The Tenth Name [prose pass]",
                  "targetId": q["id"], "data": data}],
       "capture": {"after": [{"proc": "quests.get", "input": {"id": q["id"]}}]}}
open(os.path.join(R, "push/35_tenth_name_prose.json"), "w").write(json.dumps(man, indent=1))
print("wrote push/35 - 36 objectives, 9 nodes rewritten, Clanless gone")
