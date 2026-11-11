#!/usr/bin/env python3
"""Fast turn loop for live PvP (director 2026-11-11: missed/near-missed turns in 3 straight fights).

The slow part of a turn was never the planner alone: it was re-typing the whole battle log into a file each
turn (hundreds of lines), then planning only once my turn had started. This wrapper fixes both:

  * Incremental input. Each call takes ONE short stdin line: the getBattle select joined with the newest few
    getBattleEntries rows (limit 6, with "*.id"). Entries are merged into a per-battle cache by entry id, so the
    full log is never re-sent. The cache also keeps the log after the battle ends (entries are deleted then).
  * Pre-plan on his turn. When it is NOT my turn, the planner still runs (as if my turn had come with the
    current state) and the result is stored as the DEFAULT plan.
  * Hard budget on my turn. On my turn the planner re-runs with a time budget (default 14 s). If it does not
    finish, the stored default is printed instead. Either way the output is the exact performAction inputs,
    versions already filled in, ready to fire back to back.

Usage (stdin = one JSON object, the two select results merged; keys as the connector returns them):
  echo '<json>' | fight.py BATTLE_ID [--enemy NAME] [--budget 14]
Calls to make each poll (both in one parallel tool call):
  combat.getBattle   select: battle.version, battle.round, battle.activeUserId, battle.usersState.*.userId,
                     .username, .curHealth, .maxHealth, .longitude, .latitude, .actionPoints
  combat.getBattleEntries {limit: 6} select: *.id, *.battleRound, *.userId, *.actionId, *.appliedEffects.*.txt
Output: one status line, then `FIRE v<version>:` and one JSON performAction input per line.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ME = "user_37qazcrgUPldBPI65bb25DQiCjz"
CACHE_DIR = os.path.join(HERE, "..", "fights", "live")
ENT_KEYS = ("*.id", "*.battleRound", "*.userId", "*.actionId", "*.appliedEffects.*.txt")


def cache_path(bid):
    return os.path.join(CACHE_DIR, f"{bid}.json")


def load_cache(bid):
    try:
        return json.load(open(cache_path(bid)))
    except (OSError, ValueError):
        return {"battleId": bid, "entries": [], "default": None, "default_for": None}


def save_cache(c):
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = cache_path(c["battleId"]) + ".tmp"
    json.dump(c, open(tmp, "w"), indent=0)
    os.replace(tmp, cache_path(c["battleId"]))


def merge(cache, inp):
    """Add new entries (newest-first in the input) to the cache (kept oldest-first), by entry id."""
    if "*.id" not in inp:
        return 0
    seen = {e[0] for e in cache["entries"]}
    new = [list(x) for x in zip(*(inp.get(k, []) for k in ENT_KEYS)) if x[0] not in seen]
    cache["entries"].extend(new[::-1])
    return len(new)


def battle_part(inp):
    return {k: v for k, v in inp.items() if k.startswith("battle.")}


def turn_file(battle, entries, path):
    rows = entries[::-1]   # turn.py wants newest-first, like the connector
    ents = {k: [r[i] for r in rows] for i, k in enumerate(ENT_KEYS) if k != "*.id"}
    with open(path, "w") as f:
        f.write(json.dumps(battle) + "\n" + json.dumps(ents) + "\n")


def run_turn(path, bid, enemy, budget):
    cmd = [sys.executable, os.path.join(HERE, "turn.py"), path, "--battle", bid, "--top", "1"]
    if enemy:
        cmd += ["--enemy", enemy]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=budget).stdout
    except subprocess.TimeoutExpired:
        return None, "planner over budget"
    m = re.search(r"^FIRE: (.*)$", out, re.M)
    if not m:
        tail = [l for l in out.splitlines() if l.strip()][-2:]
        return None, "no FIRE line: " + " | ".join(tail)
    return json.loads(m.group(1)), ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("battle")
    ap.add_argument("--enemy")
    ap.add_argument("--budget", type=float, default=14)
    a = ap.parse_args()
    t0 = time.time()
    inp = json.loads(sys.stdin.read())
    c = load_cache(a.battle)
    n_new = merge(c, inp)
    battle = battle_part(inp) or c.get("battle")
    if not battle:
        sys.exit("no battle state in input or cache")
    c["battle"] = battle
    us = battle["battle.usersState.*.userId"]
    names = battle["battle.usersState.*.username"]
    hp = battle["battle.usersState.*.curHealth"]
    me_i = us.index(ME)
    en_i = next((i for i in range(len(us)) if i != me_i and hp[i] > 0), None)
    enemy = a.enemy or (names[en_i] if en_i is not None else None)
    R, v = battle["battle.round"], battle["battle.version"]
    mine = battle["battle.activeUserId"] == ME
    # turn clock: the battle exposes no timer we read, so time the turn from the first poll that saw it
    tk = [R, battle["battle.activeUserId"]]
    if c.get("turn_key") != tk:
        c["turn_key"], c["turn_seen"] = tk, t0
    elapsed = t0 - c["turn_seen"]
    status = (f"R{R} v{v} {'MY TURN' if mine else 'his turn'} {elapsed:.0f}s | me {hp[me_i]:.0f}"
              + (f" | {enemy} {hp[en_i]:.0f}" if en_i is not None else " | no living enemy") + f" | +{n_new} entries")
    save_cache(c)
    if en_i is None:
        print(status); return
    path = os.path.join(CACHE_DIR, f"{a.battle}.turn.txt")
    if not mine:
        # pre-plan: score my next turn from the current state, stored as the default
        b = dict(battle)
        b["battle.activeUserId"] = ME
        aps = list(b["battle.usersState.*.actionPoints"]); aps[me_i] = 100
        b["battle.usersState.*.actionPoints"] = aps
        turn_file(b, c["entries"], path)
        plan, err = run_turn(path, a.battle, enemy, 40)
        if plan:
            c["default"], c["default_for"] = plan, [R, len(c["entries"])]
            save_cache(c)
        print(status + " | default: " + (" + ".join(x["name"] for x in plan) if plan else f"none ({err})"))
        return
    turn_file(battle, c["entries"], path)
    # hard deadline: past 30 s into my turn there is no time to plan; fire the default (60 s turn timer)
    left = min(a.budget, 38 - elapsed) - (time.time() - t0)
    plan, err = run_turn(path, a.battle, enemy, left) if left >= 4 else (None, f"{elapsed:.0f}s into my turn")
    src = "fresh"
    if not plan:
        plan, src = c.get("default"), f"DEFAULT ({err})"
    print(status + f" | plan {src} ({time.time() - t0:.1f}s)")
    if not plan:
        print("NO PLAN: fire defensiveStance + best 60 manually"); return
    print(f"FIRE v{v}: " + " + ".join(x["name"] for x in plan))
    for k, x in enumerate(plan):
        print(json.dumps({"battleId": a.battle, "actionId": x["actionId"], "longitude": x["longitude"],
                          "latitude": x["latitude"], "version": v + k}))


if __name__ == "__main__":
    main()
