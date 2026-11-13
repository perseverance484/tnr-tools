#!/usr/bin/env python3
"""The salvager's thread: Wreck Sighted rebuilt as an in-game explainer, plus a repeatable copy (RUL-2026-11-07-136).

    python3 push/skyglass_thread.gen.py create                  -> push/509_skyglass_thread_create.json  (browser: images)
    python3 push/skyglass_thread.gen.py create --uploaded <uploaded.json>
                                                                -> the same 509 with image URLs (connector, mcp_run)
    python3 push/skyglass_thread.gen.py golive --from <509 bundle> --live <Wreck Sighted read>
                                                                -> push/510_skyglass_thread_golive.json  (connector)

509 creates, all HIDDEN: 18 scene-background boards (511's three chests boards folded in, RUL-2026-11-09-140) (art/skyglass_thread/compose_boards.py) and the new repeatable quest
At the Salvager's Fire. Staff can play hidden quests (libs/quest.ts canPlayHiddenQuests), so the director plays the Fire
quest before anything players see changes.

510 (after the director's playtest): unhides the boards and the Fire quest, and rewrites the live Wreck Sighted
(_zp1l7Y9a_77pgonAdsYx, published by push/507) onto the same nodes. The edit replaces the whole record, so it is built
from a fresh live read (--live, a JSON file of quest.get for that id); every field not listed in EDIT_FIELDS is copied
from the read unchanged.

Both quests share every node; text of record is docs/design/SKYGLASS_TEXT.md section 1b, copied verbatim through
push/skyglass_text.py. Scene rules: one scene character per node (ENGINE_LAWS 48), the salvager PT01 on every scene;
the boards keep the left 40% and the bottom third clear (laws 50, 79). The graph is acyclic (law 87); "Ask something
else" is a reset_quest whose resetObjectiveId is the menu, a dialog node (law 88). Every reset and win is preceded by a
dialog (law 47). Do not hand-edit the outputs.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "push"))
import skyglass_text as T  # noqa: E402

SHARED = "Salvager's thread"
WRECK_Q, FIRE_Q = "Wreck Sighted (thread)", "At the Salvager's Fire"
WRECK_SIGHTED_ID = "_zp1l7Y9a_77pgonAdsYx"
NPC_PLACEMENT = "goagM4WhKWtnVb8oP5euM"   # the salvager's one overworld NPC (sector 210)   # live, published by push/507
TIDE_CHART = "H1s2IwtZ5JqgPEoJ55IVj"
SALVAGER = "Xugt7415D3-tepLfxpwM5"           # PT01 scene character (push/374)
SHORE = "rX78pJPETsUL2JrsSvGHn"              # the shore scene background (push/385)
QUEST_IMG = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"  # Wreck Sighted icon
FOLDER = "SkyglassSalvagersThread"
EXPORTS = "art/skyglass_thread/exports"

BOARDS = [  # key, topic label for the asset name
    ("menu", "the board"), ("threes", "go in threes"), ("hulls", "two hulls"), ("loot", "what comes back"),
    ("once", "a chart is good once"), ("ladder", "the chart ladder"), ("pick", "pick a reward"),
    ("seals", "the sealed runs"), ("rot", "steeping"), ("lantern", "lantern and Crownhold"), ("haul", "the Haul"),
    ("trade", "trade"), ("token", "Skyglass Token"),
    ("logboard", "the watch log"), ("orders", "a page's orders"),
]
# Added after 509 ran (RUL-2026-11-07-138): created hidden by push/511 (browser), unhidden by 510.
BOARDS_511 = [("chests", "the chests"), ("supplies", "supplies"), ("craft", "crafting")]
# Held back with the shards topic (RUL-2026-11-09-140): ("shards", "four shards"), ("below", "below Crownhold");
# their boards stay in EXPORTS and the topic returns as TOPICS ("s_four", "shards", ["s_below"]), ("s_below", "below", "END").
JOB = {k: 509 for k, _ in BOARDS} | {k: 511 for k, _ in BOARDS_511}

# node, board (None = the shore), next nodes; "END" marks a topic's last scene (Ask something else / I'm ready)
TOPICS = [
    ("a_threes", "threes", ["a_hulls"]), ("a_hulls", "hulls", ["a_drift"]), ("a_drift", "hulls", ["a_loot"]),
    ("a_loot", "loot", "END"),  # a_drift: The Driftline (early-game thread); drop it if The Driftline is held
    ("c_once", "once", ["c_ladder"]), ("c_ladder", "ladder", ["c_pick"]), ("c_pick", "pick", "END"),
    ("x_chests", "chests", ["x_supplies"]), ("x_supplies", "supplies", ["x_craft"]), ("x_craft", "craft", "END"),
    ("p_seals", "seals", ["p_rot"]), ("p_rot", "rot", ["p_lantern"]), ("p_lantern", "lantern", "END"),
    ("h_haul", "haul", "END"),
    ("t_salvage", "trade", ["t_prices"]), ("t_prices", "trade", "END"),  # salvage (director 2026-11-09 15:58)
    ("t_trade", "trade", ["t_token"]), ("t_token", "token", "END"),
    ("w_board", "logboard", ["w_orders"]), ("w_orders", "orders", "END"),
]
MENU_TOPICS = ["a_threes", "c_once", "x_chests", "p_seals", "h_haul", "t_salvage", "t_trade", "w_board"]  # in menu-choice order

# The pose each scene wants (docs/handoffs/SKYGLASS_ART_PROMPTS.md section 11). Until a pose's scene-character id is
# added to POSE_IDS, its scenes fall back to PT01, so adding a pose later is a one-line change and a quest edit.
POSE_IDS = {"PT01": SALVAGER, "PT02": "JIGXen2b2Z1-FK44RSVMO", "PT03": "HfHafDRKp2h_gm_pv87m6", "PT04": "xY9N_r7ywtUWp9TIBJfSW",
            "PT05": "gG8Ez235q6MTuOtXoewYg", "PT06": "FcKwVdP0NxQyjhYuMQi8i", "PT07": "7hheStqNV0F5iO6z8srrl"}  # created hidden 2026-11-13 (director's painted poses)
SCENE_POSE = {
    "d_open": "PT06", "d_menu": "PT02", "a_threes": "PT03", "a_hulls": "PT02", "a_drift": "PT01", "a_loot": "PT01", "c_once": "PT01",
    "c_ladder": "PT02", "c_pick": "PT01", "x_chests": "PT02", "x_supplies": "PT05", "x_craft": "PT02", "p_seals": "PT02", "p_rot": "PT01", "p_lantern": "PT04", "h_haul": "PT02",
    "s_four": "PT05", "s_below": "PT04", "t_salvage": "PT07", "t_prices": "PT07", "t_trade": "PT07", "t_token": "PT07", "w_board": "PT02", "w_orders": "PT02",
    "z_chart": "PT01", "z_bye": "PT06", "r_menu": "PT02",
}


def pose(node):
    return POSE_IDS.get(SCENE_POSE.get(node, "PT01"), SALVAGER)


QUESTS = {
    "wreck": {"q": WRECK_Q, "end": "z_chart", "reward_items": [{"ids": [TIDE_CHART], "number": 100, "quantity": 1}]},
    "fire": {"q": FIRE_Q, "end": "z_bye", "reward_items": []},
}


def scene(board):
    return SHORE if board is None else f"@scene:sg{JOB[board]}_board_{board}"


def dialog(node, board, text, choices):
    return {"id": node, "task": "dialog", "description": text, "sceneBackground": scene(board),
            "sceneCharacters": [pose(node)], "nextObjectiveId": [{"text": t, "nextObjectiveId": n} for t, n in choices]}


def objectives(which):
    spec = QUESTS[which]
    q = spec["q"]
    back = T.block(f"obj:{SHARED}/back.choice")
    ready = T.block(f"obj:{q}/ready.choice")
    out = [dialog("d_open", None, T.block(f"obj:{SHARED}/d_open.description"),
                  zip(T.choices(f"obj:{SHARED}/d_open.description"), ["d_menu"]))]
    menu_ch = T.choices(f"obj:{SHARED}/d_menu.description")
    assert len(menu_ch) == len(MENU_TOPICS), menu_ch
    out.append(dialog("d_menu", "menu", T.block(f"obj:{SHARED}/d_menu.description"),
                      list(zip(menu_ch, MENU_TOPICS)) + [(ready, spec["end"])]))
    for node, board, nexts in TOPICS:
        target = f"obj:{SHARED}/{node}.description"
        if nexts == "END":
            assert T.choices(target) == [], node
            ch = [(back, "r_menu"), (ready, spec["end"])]
        else:
            texts = T.choices(target)
            assert len(texts) == len(nexts), (node, texts)
            ch = list(zip(texts, nexts))
        out.append(dialog(node, board, T.block(target), ch))
    out.append({"id": "r_menu", "task": "reset_quest", "description": "Back to the fire.", "resetObjectiveId": "d_menu",
                "sceneBackground": scene("menu"), "sceneCharacters": [pose("r_menu")]})
    end_target = f"obj:{q}/{spec['end']}.description"
    out.append(dialog(spec["end"], None, T.block(end_target), zip(T.choices(end_target), ["w_done"])))
    win = {"id": "w_done", "task": "win_quest", "description": T.block(f"obj:{q}/w_done.description"),
           "sceneBackground": SHORE, "sceneCharacters": []}
    if spec["reward_items"]:
        win["reward_items"] = spec["reward_items"]
    out.append(win)
    check_graph(out)
    return out


def check_graph(objs):
    """Every edge resolves, every node is reachable, no cycle through nextObjectiveId (law 87)."""
    ids = {o["id"] for o in objs}
    edges = {o["id"]: [c["nextObjectiveId"] for c in o.get("nextObjectiveId", [])] for o in objs}
    for o in objs:
        for n in edges[o["id"]]:
            assert n in ids, (o["id"], n)
        if o["task"] == "reset_quest":
            assert o["resetObjectiveId"] in ids
    seen, stack = set(), ["d_open"]
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.add(n)
            stack.extend(edges[n])
    assert seen == ids, ids - seen
    state = {}

    def visit(n):
        state[n] = 1
        for m in edges[n]:
            assert state.get(m) != 1, f"cycle at {n}->{m}"
            if m not in state:
                visit(m)
        state[n] = 2
    visit("d_open")
    for o in objs:  # law 47: a dialog precedes every silent terminal
        if o["task"] in ("reset_quest", "win_quest"):
            parents = [p for p, e in edges.items() if o["id"] in e]
            assert parents and all(next(x for x in objs if x["id"] == p)["task"] == "dialog" for p in parents)
    for o in objs:
        if o["task"] == "dialog":
            plain = re.sub("<[^>]+>", "", o["description"])
            assert len(plain) <= 360, (o["id"], len(plain))
            assert "—" not in o["description"], o["id"]


def image_pack(boards):
    files, sizes, refs = {}, {}, set()
    for key, _ in boards:
        path = f"{EXPORTS}/board-{key}.webp"
        disk = open(os.path.join(ROOT, path), "rb").read()
        ref = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%H", "HEAD", "--", path], text=True).strip()
        assert ref and subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{path}"]) == disk, f"{path}: commit it first"
        refs.add(ref)
        name = f"sg-thread-board-{key}.webp"
        files[name] = {"path": path, "sha256": hashlib.sha256(disk).hexdigest(), "bytes": len(disk)}
        sizes[name] = len(disk)
    ref = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%H", "HEAD", "--", EXPORTS], text=True).strip()
    return sizes, {"ref": ref, "files": files}


def fire_quest_data():
    return {"name": T.block(f"quest:{FIRE_Q}.name"), "description": T.block(f"quest:{FIRE_Q}.description"),
            "image": QUEST_IMG, "questType": "event", "questRank": "D",
            "successDescription": T.block(f"quest:{FIRE_Q}.successDescription"),
            "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
            "requiredLevel": 1, "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100,  # validator max 100 each
            "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
            "startsAt": None, "endsAt": None,
            "content": {"objectives": objectives("fire"), "sceneBackground": SHORE, "sceneCharacters": [SALVAGER],
                        "entryItems": [], "reward": {}}}


def create(uploaded=None):
    assert uploaded or not os.path.exists(os.path.join(ROOT, "push/509_skyglass_thread_create.json")), \
        "push/509 exists; once it has run it is the record. Delete it only if no harvests/inbox bundle has sg509_ ids"
    items = []
    for key, topic in BOARDS + BOARDS_511:  # 511's three boards fold into 509 (neither had run; RUL-2026-11-09-140)
        name = f"Skyglass thread: board - {topic}"
        assert re.fullmatch(r"[A-Za-z0-9]*", FOLDER)
        items.append({"entity": "asset", "slot": "create", "srcId": f"sg{JOB[key]}_board_{key}", "phase": 1, "name": name,
                      "data": dict(asset_row(name, True), image=f"@img:sg-thread-board-{key}.webp")})
    data = fire_quest_data()
    items.append({"entity": "quest", "slot": "create", "srcId": "sg509_fire", "phase": 2, "name": data["name"], "data": data})
    sizes, pack = image_pack(BOARDS + BOARDS_511)
    objectives("wreck")  # the Wreck Sighted graph must build too; it ships in 510
    note = (f"push/509, HIDDEN: the salvager's thread (RUL-2026-11-07-136, -140). {len(BOARDS) + len(BOARDS_511)} scene-background boards (folder "
            f"{FOLDER}) and the new repeatable quest At the Salvager's Fire (event, maxAttempts/maxCompletes 100, no "
            f"reward): a menu at the fire with {len(MENU_TOPICS)} topics, each 1 to 3 scenes, ending on Ask something else (reset to "
            "the menu) or That's all for now. Staff can play it hidden. Wreck Sighted is NOT touched here: push/510 "
            "rewrites it onto the same nodes after the director's playtest. Generated by push/skyglass_thread.gen.py; "
            "do not hand-edit.")
    if not uploaded:
        write(509, "create", {"_note": note, "dedupNames": True, "imgSizes": sizes, "imagePack": pack, "items": items})
        return
    # Connector form (RUL-2026-11-09-140): the boards are already on the director's UploadThing app
    # (state/moe_upload on the duet/moe-uploadthing branch), so each @img becomes its URL and the imagePack goes.
    up = json.load(open(uploaded))["files"]
    for it in items:
        if it["entity"] == "asset":
            f = up[it["srcId"]]
            assert f["sha256"] == pack["files"][it["data"]["image"][5:]]["sha256"], it["srcId"]
            it["data"]["image"] = f["url"]
    note += f" Connector form: board images from the director's UploadThing app ({os.path.basename(uploaded)}), no imagePack."
    write(509, "create", {"_note": note, "dedupNames": True, "items": items})


def extra():
    """push/511: the three chests-topic boards, hidden (browser Forge: images). Retired: folded into 509 (RUL-2026-11-09-140)."""
    sys.exit("push/511 is folded into push/509 (RUL-2026-11-09-140); run create instead")
    items = []
    for key, topic in BOARDS_511:
        name = f"Skyglass thread: board - {topic}"
        items.append({"entity": "asset", "slot": "create", "srcId": f"sg511_board_{key}", "phase": 1, "name": name,
                      "data": dict(asset_row(name, True), image=f"@img:sg-thread-board-{key}.webp")})
    sizes, pack = image_pack(BOARDS_511)
    objectives("wreck"), objectives("fire")  # both graphs must build with the new topic
    note = ("push/511, HIDDEN: three scene-background boards for the salvager's new chests topic (RUL-2026-11-07-138), "
            f"folder {FOLDER}. 510 is built from the 509 and 511 bundles and publishes them with the thread. Generated by "
            "push/skyglass_thread.gen.py extra; do not hand-edit.")
    write(511, "boards", {"_note": note, "dedupNames": True, "imgSizes": sizes, "imagePack": pack, "items": items})


def created(path):
    """srcId -> created id, from a Forge/connector results bundle (entries with slot create, state ok; then idmap)."""
    b = json.load(open(path))
    got = {}
    for e in b.get("entries") or []:
        if e.get("slot") == "create" and e.get("state") == "ok" and e.get("id") and (e.get("srcId") or "").startswith(("sg509_", "sg511_")):
            got[e["srcId"]] = e["id"]
    for k, v in (b.get("idmap") or {}).items():
        if k.startswith(("sg509_", "sg511_")):
            got.setdefault(k, v)
    return got


def asset_row(name, hidden):
    return {"name": name, "type": "SCENE_BACKGROUND", "folder": FOLDER, "frames": 1, "speed": 1, "hidden": hidden,
            "onInitialBattleField": False, "licenseDetails": "TNR"}


def golive(bundle_paths, live_path):
    ids = {}
    for path in bundle_paths:
        ids.update(created(path))
    miss = [k for k in [f"sg{JOB[b]}_board_{b}" for b in JOB] + ["sg509_fire"] if k not in ids]
    assert not miss, f"the 509/511 bundles lack {miss}"
    bundle_path = " + ".join(os.path.basename(p) for p in bundle_paths)
    live = json.load(open(live_path))
    live = live.get("data", live)
    assert live.get("id") in (None, WRECK_SIGHTED_ID) and live.get("name") == "Wreck Sighted", "wrong live record"

    def resolve(objs):
        s = json.dumps(objs)
        for src, real in ids.items():
            s = s.replace(f"@scene:{src}", real)
        assert "@scene:" not in s
        return json.loads(s)
    items = []
    for key, topic in BOARDS + BOARDS_511:
        name = f"Skyglass thread: board - {topic}"
        items.append({"entity": "asset", "slot": "edit", "targetId": ids[f"sg{JOB[key]}_board_{key}"], "phase": 1,
                      "name": f"{name}: unhide", "data": asset_row(name, False)})
    fire = fire_quest_data()
    fire["hidden"] = False
    fire.update(FIRE_GOLIVE)
    fire["content"]["objectives"] = resolve(fire["content"]["objectives"])
    items.append({"entity": "quest", "slot": "edit", "targetId": ids["sg509_fire"], "phase": 2,
                  "name": "At the Salvager's Fire: publish", "data": fire})
    wreck = {k: v for k, v in live.items() if k not in ("id", "createdAt", "updatedAt")}
    # Every dialog step tied to her NPC: tapping her opens the scene and choices, no roll (director 2026-11-09 20:21).
    wobjs = [dict(o, overworldPlacementId=NPC_PLACEMENT) if o["task"] == "dialog" else o
             for o in resolve(objectives("wreck"))]
    wreck["content"] = dict(live["content"], objectives=wobjs, sceneBackground=SHORE,
                            sceneCharacters=[SALVAGER])
    wreck["questType"] = "overworld"  # one-off at her NPC, no longer an Administration Building event (15:58)
    items.append({"entity": "quest", "slot": "edit", "targetId": WRECK_SIGHTED_ID, "phase": 2,
                  "name": "Wreck Sighted: the salvager's thread", "data": wreck})
    note = (f"push/510, LIVE: unhide the {len(BOARDS) + len(BOARDS_511)} thread boards and At the Salvager's Fire, and rewrite Wreck Sighted "
            f"({WRECK_SIGHTED_ID}) onto the thread's nodes. Built from {bundle_path} and a live read "
            f"of Wreck Sighted ({os.path.basename(live_path)}). Players mid-way through the old Wreck Sighted keep their "
            "attempt; editing a live event quest does not restart it.")
    write(510, "golive", {"_note": note, "items": items})


# At release Wreck Sighted moves to the salvager's one overworld NPC (director 2026-11-09 15:58). The Fire stays an
# Administration Building event so the no-reward repeat costs no daily NPC roll (director 2026-11-09 19:57); it only
# gains Wreck Sighted as its prerequisite at release, so staff can keep playtesting it hidden until then.
FIRE_GOLIVE = {"questType": "event", "prerequisiteQuestId": WRECK_SIGHTED_ID}


def fire_text(bundle_paths, num=544):
    """push/544, HIDDEN: the Fire quest's text and graph for the one-NPC setup and the salvage topic. Still event."""
    ids = {}
    for path in bundle_paths:
        ids.update(created(path))
    s = json.dumps(objectives("fire"))
    for src, real in ids.items():
        s = s.replace(f"@scene:{src}", real)
    assert "@scene:" not in s
    fire = fire_quest_data()
    fire["content"]["objectives"] = json.loads(s)
    objectives("wreck")  # the Wreck Sighted graph must still build
    write(num, "fire_text", {"_note": f"push/{num}, HIDDEN: At the Salvager's Fire text (SKYGLASS_TEXT 1b). The Fire stays "
                             "an Administration Building event with no reward and no daily NPC roll (director 2026-11-09 "
                             "19:57); her overworld NPC hands out Wreck Sighted and the trades. Stays hidden so it can be "
                             "playtested; 510 unhides it and adds Wreck Sighted as prerequisite. Generated by "
                             "push/skyglass_thread.gen.py firetext; do not hand-edit.", "items": [{"entity": "quest", "slot": "edit", "targetId": ids["sg509_fire"],
                                                     "phase": 1, "name": "At the Salvager's Fire: one NPC, salvage topic",
                                                     "data": fire}]})


def write(num, tag, obj):
    out = os.path.join(ROOT, f"push/{num}_skyglass_thread_{tag}.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"{os.path.relpath(out, ROOT)}: {len(obj['items'])} items")


def main():
    ap = argparse.ArgumentParser(description="the salvager's thread")
    ap.add_argument("step", choices=["create", "extra", "golive", "firetext"])
    ap.add_argument("--from", dest="bundle", nargs="+")
    ap.add_argument("--live")
    ap.add_argument("--num", type=int, default=544, help="firetext: push number to write")
    ap.add_argument("--uploaded", help="create: uploaded.json from the UploadThing branch; writes the connector form")
    a = ap.parse_args()
    if a.step == "create":
        create(a.uploaded)
    elif a.step == "firetext":
        fire_text(a.bundle, a.num)
    elif a.step == "extra":
        extra()
    else:
        assert a.bundle and a.live, "golive needs --from <509 bundle> <511 bundle> and --live <Wreck Sighted read>"
        golive(a.bundle, a.live)


if __name__ == "__main__":
    main()
