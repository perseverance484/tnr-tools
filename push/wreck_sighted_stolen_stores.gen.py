#!/usr/bin/env python3
"""Stolen Stores: this weekend's two Wreck Sighted copies hand out the Chart of the Flooded Stores.

    python3 push/wreck_sighted_stolen_stores.gen.py create
        -> push/649: create both copies, HIDDEN (30 to 80 and 81+), from today's live reads
    python3 push/wreck_sighted_stolen_stores.gen.py release --from <649 results bundle>
        -> push/650: RELEASE ONLY (Friday Nov 20, with the director's go): unhide both new copies, hide last
           weekend's copies, and give At the Salvager's Fire the same topic changes (no grant scene)

The director's call, 2026-11-19 14:36 UTC, relayed in this thread: "Definitely put the new chart". The design is
doc rev 33, "The Salvager and her Fire": a new This weekend topic, six changed topics, and the grant scene with the
ration tin. The Watch Log pages already say "Every player gets its chart from Wreck Sighted" (push/641).

Why new copies and not an edit: Wreck Sighted is once per player (maxCompletes 1). Last weekend's copies
(IZgCt17ReC_0vtUG-GNRl 30 to 80, -UjsbiBbaSyPtZ4zAH10A 81+) were done by everyone who played; an edit would reach
only new players. They also grant last weekend's pages. The new copies grant this weekend's pages instead:
the Shallows page qOhvkP3aPCPH88wI7-IZW (30 to 80) and page 3, AgGR962c3XNo6Pr0up2qT (81+), as in push/643.

Chart band: the Chart of the Flooded Stores (FuQzaFNlpyOUGlO5BtjyX) is Rare, read live 2026-11-19 (hidden until
Friday). The director's chart rule puts every chart below Epic at 30+ with no cap, so it fits both copies.

Friday order: unhide the chart item first (it is hidden and push/644 says the same), then this release push with
push/643 and push/644. The This weekend topic names the beach crew and Short Rations: those go live the same
Friday (push/638, push/639). If they slip, drop the n_crew and n_rations answers before running.

Base: the live records, read 2026-11-19 ~14:45Z and committed under
state/stolen_stores_captures/wreck_sighted_2026-11-19/. A quest edit replaces content whole, so the Fire edit
sends its full content from that read; re-read it before Friday's run.

Do not hand-edit the generated push files.
"""
import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "state", "stolen_stores_captures", "wreck_sighted_2026-11-19")

OLD_LOW, OLD_HIGH, FIRE = "IZgCt17ReC_0vtUG-GNRl", "-UjsbiBbaSyPtZ4zAH10A", "lEg5pVXqA8lzJpIPrykNi"
TIDE_CHART = "H1s2IwtZ5JqgPEoJ55IVj"
FLOODED_CHART = "FuQzaFNlpyOUGlO5BtjyX"
PAGE = {OLD_LOW: "qOhvkP3aPCPH88wI7-IZW", OLD_HIGH: "AgGR962c3XNo6Pr0up2qT"}
OLD_PAGE = {OLD_LOW: "73ivWjFFk0dwSEG7bNhMj", OLD_HIGH: "V-i3ZcAqPu0hB3G9IEzGo"}
NAME = {OLD_LOW: "Wreck Sighted: Stolen Stores (Levels 30 to 80)",
        OLD_HIGH: "Wreck Sighted: Stolen Stores (Level 81 and up)"}
SRC = {OLD_LOW: "ws649_low", OLD_HIGH: "ws649_high"}

# Fields a quest create takes (push/641's create shape).
CREATE_FIELDS = ["name", "description", "successDescription", "image", "questType", "questRank", "requiredLevel",
                 "maxLevel", "tierLevel", "prerequisiteQuestId", "requiredVillage", "requiredBloodlineId",
                 "consecutiveObjectives", "maxAttempts", "maxCompletes", "retryDelay", "attemptDelay", "startsAt",
                 "endsAt", "hidden", "content"]

WEEK_HUB = ('She glances down the beach, at the crates split open along the tideline. "The tide\'s been busy."'
            '<br><br><i>This weekend on her shore. Pick one.</i>')
WEEK = [
    ("n_crew", "The crew on the sand",
     '"The tide\'s been leaving her crew on my beach. They wake up, find a crate, and start dragging it back to the '
     'hull like it\'s still their watch."<br><br><i>Looting Deckhands and Quartermaster\'s Mates wander sector 210. '
     'Walk up and attack: they never start a fight, and every fight is sized to you. Deckhands sometimes drop Wreck '
     'Salvage. Mates drop it more often, and now and then a Flooded Stores chart.</i>'),
    ("n_qm", "The Quartermaster",
     '"Forty years he\'s handed out rations to a crew that doesn\'t eat. Never once asked where they went."'
     '<br><br><i><b>The Flooded Stores</b>: a rare run, alone, in the Battle Arena, from level 30. He feeds his crew '
     'so they can\'t fall, so deal with whoever is handing out the food first. After three fights, take the stores, '
     'or go below.</i>'),
    ("n_rations", "Short Rations",
     '"Thin them out and I\'ll pay you. My crates, my sand."<br><br><i><b>Short Rations</b> is on the Wake Island '
     'board, once a day from level 30: beat 3 Looting Deckhands and a Quartermaster\'s Mate in sector 210 for 3 '
     'Wreck Salvage. It doesn\'t use a daily NPC roll.</i>'),
    ("n_eat", "What's eating the stores?",
     'She pokes the fire. "That crew don\'t eat. Whatever\'s down there came in from the sea."'),
]
BOARD_LINE = "The tide's been busy."

# (node, old text, new text): each old text must occur exactly once in that node.
TOPIC_EDITS = [
    ("d_open", 'by a driftwood fire below the wreck. "Another one come to pick her bones. Sit, then. Ask."',
     'by a driftwood fire below the wreck. Crates lie split open along the tideline behind her. "Another one come '
     'to pick her bones. Mind the sand tonight. Sit, then. Ask."'),
    ("a_drift", "Two new ones drop in the Faded Wreck: <b>Split Hold</b> and <b>Broken Stern</b>, both open from "
                "level 30.",
     "New this weekend: <b>The Flooded Stores</b>, open from level 30."),
    ("c_rare", "Spoiled Hold, Broken Stern.", "Spoiled Hold, Broken Stern, Flooded Stores."),
    ("t_earn", "Watch Log challenge: 3. Dailies: 1 to 5.</i>",
     "Watch Log challenge: 3. Dailies: 1 to 5. Beach crew: Deckhands 1, one fight in ten; Mates 1, three in ten. "
     "Short Rations: 3.</i>"),
    ("t_deck", "or the Buried Cache or Rotted Galley chart,", "or the Buried Cache, Rotted Galley or Flooded Stores chart,"),
    ("t_work", "Lose a fight and the run ends.</i>",
     "Lose a fight and the run ends. Her crew on the sand are fair game too: see The tide's been busy.</i>"),
]
GRANT_OLD = ('She pulls a <b>Tide Chart</b> from her coat, still damp at one corner. "Low tide opens her lower hull. '
             'Don\'t sit on it. She\'s already changing shape."<br><br><i>')
GRANT_NEW = ('She pulls a chart from a dented ration tin, still smelling of salt and old biscuit. "Took this off one '
             'of the crew on the sand last night. The Quartermaster\'s issue sheet. He signs for everything."<br><br>'
             '<i>The <b>Chart of the Flooded Stores</b> opens The Flooded Stores, from level 30. ')


def load(qid):
    return json.load(open(os.path.join(CAP, qid + ".json")))


def node(objs, nid):
    hits = [o for o in objs if o["id"] == nid]
    assert len(hits) == 1, (nid, len(hits))
    return hits[0]


def swap(text, old, new, where):
    assert text.count(old) == 1, (where, old, text.count(old))
    return text.replace(old, new)


def add_week(objs, after_label):
    """Board line on d_menu and the four answers. Answers go back to the board and, like every other leaf,
    offer the exit the record already uses (the chart on Wreck Sighted, That's all on the Fire)."""
    menu = node(objs, "d_menu")
    labels = [o["text"] for o in menu["nextObjectiveId"]]  # d_menu holds option objects on both records
    exit_opt = ({"text": "I'm ready. Give me the chart", "nextObjectiveId": "z_chart"}
                if "z_chart" in [o["nextObjectiveId"] for o in menu["nextObjectiveId"]]
                else {"text": "That's all", "nextObjectiveId": "f_leave"})
    menu["nextObjectiveId"].insert(labels.index(after_label) + 1, {"text": BOARD_LINE, "nextObjectiveId": "n_week"})
    tmpl = node(objs, "t_odds")  # a plain dialog leaf with this record's scene
    hub = copy.deepcopy(tmpl)
    hub.update(id="n_week", description=WEEK_HUB,
               nextObjectiveId=[{"text": label, "nextObjectiveId": nid} for nid, label, _ in WEEK]
               + [{"text": "Back to the fire", "nextObjectiveId": "r_menu"}])
    new = [hub]
    for nid, _, text in WEEK:
        leaf = copy.deepcopy(tmpl)
        leaf.update(id=nid, description=text,
                    nextObjectiveId=[{"text": "Back to the fire", "nextObjectiveId": "r_menu"}, dict(exit_opt)])
        new.append(leaf)
    at = objs.index(node(objs, "r_menu"))  # dialog nodes sit before the reset node, as in the live records
    objs[at:at] = new


def topics(content):
    objs = content["objectives"]
    for nid, old, new in TOPIC_EDITS:
        n = node(objs, nid)
        n["description"] = swap(n["description"], old, new, nid)
    add_week(objs, "Got any work for me?")


def build_copy(qid):
    live = load(qid)
    data = {k: copy.deepcopy(live[k]) for k in CREATE_FIELDS}
    data["name"], data["hidden"] = NAME[qid], True
    c = data["content"]
    topics(c)
    z = node(c["objectives"], "z_chart")
    z["description"] = swap(z["description"], GRANT_OLD, GRANT_NEW, "z_chart")
    grant = node(c["objectives"], "k_grant")
    assert grant["newQuestIds"] == [OLD_PAGE[qid]], grant["newQuestIds"]
    grant["newQuestIds"] = [PAGE[qid]]
    done = node(c["objectives"], "w_done")
    assert done["reward_items"] == [{"ids": [TIDE_CHART], "number": 100, "quantity": 1}], done["reward_items"]
    done["reward_items"] = [{"ids": [FLOODED_CHART], "number": 100, "quantity": 1}]
    check(live, data, copy_=True)
    return data


def build_fire():
    live = load(FIRE)
    content = copy.deepcopy(live["content"])
    topics(content)
    check(live, {"content": content}, copy_=False)
    return {"content": content}


def check(live, new, copy_):
    s = json.dumps(new, ensure_ascii=False)
    assert "—" not in s and "–" not in s, "dash"
    objs = new["content"]["objectives"]
    ids = [o["id"] for o in objs]
    assert len(ids) == len(set(ids)), "duplicate node id"
    for o in objs:  # every option points at a node that exists
        nxt = o.get("nextObjectiveId") or []
        for opt in [nxt] if isinstance(nxt, str) else nxt:
            target = opt if isinstance(opt, str) else opt["nextObjectiveId"]
            assert target in ids, (o["id"], opt)
    if copy_:
        assert TIDE_CHART not in s and s.count(FLOODED_CHART) == 1, "chart swap"
        assert "Tide Chart</b> from her coat" not in s
    # Nothing else moved: every live node keeps every field, and only the edited nodes change text.
    before = {o["id"]: o for o in live["content"]["objectives"]}
    touched = {e[0] for e in TOPIC_EDITS} | {"d_menu"} | ({"z_chart", "k_grant", "w_done"} if copy_ else set())
    for nid, o in before.items():
        if nid not in touched:
            assert node(objs, nid) == o, nid
    assert set(ids) - set(before) == {"n_week"} | {w[0] for w in WEEK}


def write(num, slug, note, items):
    out = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    json.dump({"_note": note, "items": items}, open(out, "w"), indent=1, ensure_ascii=False)
    print("wrote", out, len(items), "items")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "create":
        items = [{"entity": "quest", "slot": "create", "srcId": SRC[q], "phase": 1,
                  "name": NAME[q],
                  "data": build_copy(q)} for q in (OLD_LOW, OLD_HIGH)]
        write(649, "wreck_sighted_stolen_stores_create",
              "push/649, HIDDEN: create this weekend's two Wreck Sighted copies. Each hands out the Chart of the "
              "Flooded Stores in place of the Tide Chart, grants this weekend's page (Shallows / page 3), and "
              "carries the Stolen Stores topic changes (doc rev 33). Hidden until push/650 on Friday. Generated by "
              "push/wreck_sighted_stolen_stores.gen.py; do not hand-edit.", items)
    elif mode == "release":
        assert sys.argv[2] == "--from", "release --from <649 results bundle>"
        bundle = json.load(open(sys.argv[3]))
        made = {e["srcId"]: e["id"] for e in bundle["entries"] if e.get("srcId") in SRC.values()}
        assert set(made) == set(SRC.values()), made
        items = []
        for q in (OLD_LOW, OLD_HIGH):
            items.append({"entity": "quest", "slot": "edit", "targetId": made[SRC[q]], "phase": 10,
                          "name": NAME[q] + ": unhide", "data": {"hidden": False}})
            items.append({"entity": "quest", "slot": "edit", "targetId": q, "phase": 20,
                          "name": load(q)["name"] + " (last weekend's copy): hide", "data": {"hidden": True}})
        items.append({"entity": "quest", "slot": "edit", "targetId": FIRE, "phase": 30,
                      "name": "At the Salvager's Fire: Stolen Stores topics (This weekend, six changed topics)",
                      "data": build_fire()})
        write(650, "wreck_sighted_stolen_stores_release",
              "push/650, RELEASE ONLY (Friday Nov 20, with the director's go): unhide this weekend's two Wreck "
              "Sighted copies, hide last weekend's, and give At the Salvager's Fire the Stolen Stores topics. Unhide "
              "the Chart of the Flooded Stores item first; run with push/643 and push/644, after push/638 and "
              "push/639. Re-read the Fire before running (its content goes whole). Generated by "
              "push/wreck_sighted_stolen_stores.gen.py; do not hand-edit.", items)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
