#!/usr/bin/env python3
"""Replay a saved fight through turn.py at one of my turns (offline test, no live calls).
Usage: replay.py ENTRIES_JSON ROUND --enemy NAME --enemy-id ID --me X,Y,HP,AP --him X,Y,HP [--battle tag]
Entries up to and including the enemy's actions in ROUND that came before my turn are kept."""
import argparse, json, os, subprocess, sys, tempfile
from ingest import ME
p = argparse.ArgumentParser()
p.add_argument("entries"); p.add_argument("round", type=int)
p.add_argument("--enemy", required=True); p.add_argument("--enemy-id", required=True)
p.add_argument("--me", required=True); p.add_argument("--him", required=True); p.add_argument("--battle", default="replay")
a = p.parse_args()
raw = json.load(open(a.entries))
rows = list(zip(raw["*.battleRound"], raw["*.userId"], raw["*.actionId"], raw["*.appliedEffects.*.txt"]))[::-1]
keep = []
for r in rows:
    if r[0] < a.round or (r[0] == a.round and r[1] != ME):
        keep.append(r)
    elif r[0] == a.round and r[1] == ME:
        break
keep = keep[::-1]
ent = {"*.battleRound": [k[0] for k in keep], "*.userId": [k[1] for k in keep], "*.actionId": [k[2] for k in keep],
       "*.appliedEffects.*.txt": [k[3] for k in keep]}
mx, my, mhp, map_ = [float(x) for x in a.me.split(",")]
hx, hy, hhp = [float(x) for x in a.him.split(",")]
bat = {"battle.version": 1, "battle.round": a.round, "battle.activeUserId": ME,
       "battle.usersState.*.userId": [a.enemy_id, ME], "battle.usersState.*.username": [a.enemy, "dauntless"],
       "battle.usersState.*.curHealth": [hhp, mhp], "battle.usersState.*.maxHealth": [5050, 5050],
       "battle.usersState.*.longitude": [int(hx), int(mx)], "battle.usersState.*.latitude": [int(hy), int(my)],
       "battle.usersState.*.actionPoints": [100, int(map_)]}
f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
f.write(json.dumps(bat) + "\n" + json.dumps(ent) + "\n"); f.close()
sys.exit(subprocess.call([sys.executable, os.path.join(os.path.dirname(__file__), "turn.py"), f.name, "--battle", a.battle, "--enemy", a.enemy, "--top", os.environ.get("TOPN", "3")]))
