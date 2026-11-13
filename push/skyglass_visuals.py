#!/usr/bin/env python3
"""Overlay the Nov 13 visuals on At the Salvager's Fire or Wreck Sighted, leaving all text and flow alone.

    python3 push/skyglass_visuals.py <read.json> [--out quest_data.json]

<read.json> is a quests.get read of the record (or a manifest item's "data" after the text pass). For each
objective whose id is in the thread's node map it sets:
  - sceneCharacters = [the scene's painted pose] (push/skyglass_thread.gen.py SCENE_POSE / POSE_IDS)
  - sceneBackground = the revised Nov 13 board (state/skyglass_thread_boards_v2.json) where one exists
Every other field is copied from the input unchanged. Prints a per-node diff. Run it LAST, on the freshest read,
right before the edit, so it never undoes a text or kickoff change made in between.
The 6 pose characters and 7 v2 boards are hidden assets: they must be unhidden in the same go-live sitting.
"""
import argparse, importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("thread", os.path.join(ROOT, "push/skyglass_thread.gen.py"))
G = importlib.util.module_from_spec(spec); sys.path.insert(0, os.path.join(ROOT, "push")); spec.loader.exec_module(G)
V2 = json.load(open(os.path.join(ROOT, "state/skyglass_thread_boards_v2.json")))
BOARD_NODES = {"d_menu": "menu", "r_menu": "menu", "a_threes": "threes", "a_hulls": "hulls", "a_drift": "driftline",
               "a_loot": "loot", "t_salvage": "salvage", "t_prices": "salvage", "w_board": "logboard"}
DROP = ("id", "createdAt", "updatedAt", "raidStartedAt", "raidEndsAt", "raidCaptureDeadline", "raidGracePeriodEnd")


def overlay(rec):
    data = {k: v for k, v in rec.items() if k not in DROP}
    changes = []
    for o in data["content"]["objectives"]:
        nid = o.get("id")
        if nid in G.SCENE_POSE and o.get("task") in ("dialog", "reset_quest"):
            want = [G.pose(nid)]
            if o.get("sceneCharacters") != want:
                changes.append((nid, "pose", o.get("sceneCharacters"), want)); o["sceneCharacters"] = want
        if nid in BOARD_NODES:
            want = V2[BOARD_NODES[nid]]
            if o.get("sceneBackground") != want:
                changes.append((nid, "board", o.get("sceneBackground"), want)); o["sceneBackground"] = want
    return data, changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("read"); ap.add_argument("--out")
    a = ap.parse_args()
    rec = json.load(open(a.read)); rec = rec.get("data", rec)
    rid = rec.get("id")
    data, ch = overlay(rec)
    for c in ch:
        print(f"{c[0]:10} {c[1]:5} {c[2]} -> {c[3]}")
    print(f"{rec.get('name')}: {len(ch)} changes")
    if a.out:
        json.dump({"id": rid, "data": data}, open(a.out, "w"), ensure_ascii=False)
        print("wrote", a.out)


if __name__ == "__main__":
    main()
