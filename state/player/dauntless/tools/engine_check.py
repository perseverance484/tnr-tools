#!/usr/bin/env python3
"""planner2's numeric engine vs the game's own combat code (director 2026-11-11: "Check the simulator against source
and get it within ~1% on numbers").

For each of my logged turns (every fight with a log), the position is rebuilt two ways:
  engine  harness/pvp_turn/engine/replay_sim.ts replays every logged action of both sides through the TNR source
          (pinned upstream, offline) and then fires each candidate bundle: HP of both sides after my turn;
  python  planner2.build on the same log, then run_turn of the same bundle.
Compared: damage dealt to him and HP change on me, per bundle. Reports the error distribution and, per action, the
median ratio engine/python so a formula gap shows up as a factor on the actions that share it.

Usage: engine_check.py [--fights N] [--bundles 6] [--out ../fights/engine_check.json]
"""
import argparse
import json
import os
import statistics
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_bridge as EB  # noqa: E402
import exam  # noqa: E402
import opponents as OM  # noqa: E402
import planner2 as P2  # noqa: E402
import turn  # noqa: E402
import value_model  # noqa: E402
from ingest import IDS, ME  # noqa: E402

P2._OPP_SCALES = {}     # the engine replay has no per-opponent log scales: compare like with like


def positions(rows):
    """Turn files for each of my turns in a log: (round, path)."""
    users = [u for u in dict.fromkeys(u for _, u, _, _ in rows) if (u or "").startswith("user_")]
    if ME not in users or len(users) != 2:
        return
    en_id = next(u for u in users if u != ME)
    name = OM.names_in(rows, en_id)
    hps = exam.hp_track(rows, ["dauntless", name])
    seen = set()
    for i, (r, u, a, ts) in enumerate(rows):
        if u != ME or r in seen:
            continue
        seen.add(r)
        pre = rows[:i][::-1]
        hp = hps[i]
        b = {"battle.version": 1, "battle.round": r, "battle.activeUserId": ME,
             "battle.usersState.*.userId": [en_id, ME], "battle.usersState.*.username": [name, "dauntless"],
             "battle.usersState.*.curHealth": [hp[name], hp["dauntless"]],
             "battle.usersState.*.maxHealth": [5050, 5050], "battle.usersState.*.longitude": [6, 7],
             "battle.usersState.*.latitude": [4, 4], "battle.usersState.*.actionPoints": [0, 100]}
        e = {"*.battleRound": [x[0] for x in pre], "*.userId": [x[1] for x in pre], "*.actionId": [x[2] for x in pre],
             "*.appliedEffects.*.txt": [x[3] for x in pre]}
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.write(fd, (json.dumps(b) + "\n" + json.dumps(e) + "\n").encode())
        os.close(fd)
        yield r, path, name


EXACT = os.environ.get("TNR_EXACT") == "1"      # live-shaped: exact effect list + this fight's engine bases


def exact_inputs(path, name, cal):
    """Make a turn file live-shaped: the engine's replayed effect list as battle.liveEffects (what the pilot reads
    from getBattle), plus fight bases for this matchup under battle id ECHK."""
    import fight_bases
    battle, me, others, rows = turn.load_input(path)
    en = next(p for p in others if p["username"] == name)
    R = battle["battle.round"]
    ea = any(r == R and u == en["userId"] for r, u, _, _ in rows)
    st = EB.replay_state(rows, ME, en["userId"], me, en, (me["longitude"], me["latitude"]),
                         (en["longitude"], en["latitude"]), R, "next" if ea else "same", cal)
    live = [dict({k: v for k, v in e.items() if k != "target"}, targetId=ME if e["target"] == "me" else en["userId"])
            for e in ((st or {}).get("state") or {}).get("effects") or []]
    lines = open(path).read().splitlines()
    b = json.loads(lines[0])
    b["battle.liveEffects"] = live
    open(path, "w").write(json.dumps(b) + "\n" + lines[1] + "\n")
    key = (en["userId"], tuple(sorted({a for _, u, a, _ in rows if u == en["userId"]})))
    if _FB.get("key") != key:
        fb = {"me": fight_bases.mine(rows, en["userId"], [], cal), "him": fight_bases.his(rows, en["userId"], [], cal),
              "opp": en["userId"]}
        json.dump(fb, open(os.path.join(fight_bases.LIVE, "ECHK_bases.json"), "w"))
        _FB["key"] = key


_FB = {}


def compare(path, name, nb, cal):
    if EXACT:
        exact_inputs(path, name, cal)
    P, info = P2.build(type("A", (), dict(file=path, enemy=name, loadout="pvp1", battle="ECHK" if EXACT else None)))
    if P is None:
        return []
    battle, me, others, rows = turn.load_input(path)
    en = next(p for p in others if p["username"] == name)
    bundles = P2.legal_bundles(info["st"], info["R"], info["ap"], 1, info["st"]["loadout"], P.me0, P.en0)
    ranked = [r[1] for r in P2.rank(P, bundles, info["ap"], P2.load_weights())[:nb]]
    # single actions too: the clearest read of each action's numbers
    singles = sorted({(x,) for b in ranked for x in b if x not in ("step", "stepback")})
    cands = ranked + [s for s in singles if s not in ranked]
    me_pos, en_pos = (me["longitude"], me["latitude"]), (en["longitude"], en["latitude"])
    seqs = [turn.resolve_targets(b, me_pos, en_pos, set())[0] for b in cands]
    R = battle["battle.round"]
    en_acted = any(r == R and u == en["userId"] for r, u, _, _ in rows)
    res = EB.replay_eval(rows, ME, en["userId"], me, en, me_pos, en_pos, R, "next" if en_acted else "same", cal,
                         [[(n, aid, t) for n, aid, t in s] for s in seqs], timeout=60)
    out = []
    if not res or not res.get("results"):
        return out
    for b, er in zip(cands, res["results"]):
        if not er.get("legal"):
            continue
        m, e = P.me0.copy(), P.en0.copy()
        if "cleanse" in b:
            m.wipe(P2.NEGK)
        P2.run_turn(m, e, [P.my_kit[x] for x in b if x in P.my_kit], 0, 5050, 5050)
        eng_dealt = en["curHealth"] - er["afterMe"]["him"]
        py_dealt = en["curHealth"] - e.hp
        eng_self = me["curHealth"] - er["afterMe"]["me"]
        py_self = me["curHealth"] - m.hp
        out.append({"round": R, "opp": name, "bundle": list(b), "eng_dealt": round(eng_dealt), "py_dealt": round(py_dealt),
                    "his_hp": round(en["curHealth"]), "my_hp": round(me["curHealth"]),
                    "eng_self": round(eng_self), "py_self": round(py_self)})
    return out


def report(rows):
    # kill turns compare nothing: the engine stops at his remaining HP, the planner's raw sum runs past it
    rows = [x for x in rows if not ("his_hp" in x and x["eng_dealt"] >= x["his_hp"] - 1)]
    def err(x, k):
        e, p = x[f"eng_{k}"], x[f"py_{k}"]
        return (p - e) / max(100.0, abs(e))
    for k in ("dealt", "self"):
        rs = [x for x in rows if abs(x[f"eng_{k}"]) >= 50 or abs(x[f"py_{k}"]) >= 50]
        if not rs:
            continue
        es = [abs(err(x, k)) for x in rs]
        print(f"{k:5}: {len(rs)} bundles  median |err| {statistics.median(es):.1%}  within 1% {sum(e <= 0.01 for e in es) / len(es):.0%}"
              f"  within 5% {sum(e <= 0.05 for e in es) / len(es):.0%}  bias {statistics.mean(err(x, k) for x in rs):+.1%}")
    by = {}
    for x in rows:
        if len(x["bundle"]) == 1 and x["eng_dealt"] >= 50 and x["py_dealt"] >= 50:
            by.setdefault(x["bundle"][0], []).append(x["eng_dealt"] / x["py_dealt"])
    print("single actions, engine / python damage (median, n):")
    print("  " + ", ".join(f"{a} {statistics.median(v):.3f} ({len(v)})" for a, v in sorted(by.items())))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", type=int, default=6)
    ap.add_argument("--bundles", type=int, default=4)
    ap.add_argument("--out", default=os.path.join(HERE, "..", "fights", "engine_check.json"))
    ap.add_argument("--report", action="store_true", help="report the saved comparison only")
    ap.add_argument("--part", default="0/1", help="i/n: this run takes every n-th fight from the i-th (parallel shards)")
    ap.add_argument("--merge", nargs="*", help="report several saved shard files together")
    a = ap.parse_args()
    if a.report:
        report(json.load(open(a.out)))
        return
    if a.merge:
        report([x for f in a.merge for x in json.load(open(f))])
        return
    pi, pn = map(int, a.part.split("/"))
    cal = value_model.load_cal()
    allrows = []
    n = k = 0
    for bid, path, rows, meta in OM.load_logs():
        if n >= a.fights or "observed" in path:
            continue
        k += 1
        if (k - 1) % pn != pi:
            continue
        got = 0
        for r, tp, name in positions(rows):
            try:
                allrows += [dict(x, fight=bid) for x in compare(tp, name, a.bundles, cal)]
                got += 1
            except Exception as e:  # noqa: BLE001
                print(f"skip {bid} R{r}: {e}")
            finally:
                os.unlink(tp)
        if got:
            n += 1
            print(f"{bid[:8]}: {got} positions, {len(allrows)} bundles so far", flush=True)
    json.dump(allrows, open(a.out, "w"), indent=0)
    report(allrows)


if __name__ == "__main__":
    main()
