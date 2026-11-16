#!/usr/bin/env python3
"""Measure an opponent's worn-gear totals from the logged hits (no lookup: his gear is not public).

Engine pre-battle gear stage (damagePipeline.ts): a formula hit is scaled by
  (1 + (60 + attacker gear given points) / 100)   and   (1 - (50 + defender gear DR points) / 100).
So, replaying the log once with his assumed gear (dr0, g0):
  my hits on him:  logged / engine = (50 - dr) / (50 - dr0)   ->  dr = 50 - ratio * (50 - dr0)
  his hits on me:  logged / engine = (160 + g) / (160 + g0)   ->  g  = ratio * (160 + g0) - 160
using the median ratio over formula hits (pierce excluded: flat). Results are clamped to a plausible range and
written to kit/opponents/<userId>.json as "gearMods" (merged with any saved kit); the replay then uses them.
Director 2026-11-11: assume the Kaeruun endgame set; this corrects the assumption per opponent from evidence
(Lzl3j0y: offence gear but no DR pieces; Targaryen: chest DR, no Fortify).
Usage: fit_gear.py ENTRIES.json|TURN_FILE --enemy NAME --en-id USER_ID [--write]
In a fight: run it during HIS turn on the saved turn file once a formula hit exists each way (re-run as hits grow);
turn.py then replays with the measured totals. ~6 s, offline, no live calls.
"""
import argparse
import json
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_bridge as EB  # noqa: E402
import value_model  # noqa: E402

ME = "user_37qazcrgUPldBPI65bb25DQiCjz"
HIT = re.compile(r"^(\S+) takes ([\d.]+) damage$")
PIERCE = {"osJq3k77YPGoFWgof12FQ", "G6MRbppaDZ2a5Wr0GIjH8"}


def fit(rows, en_id, en_name, me_name="dauntless"):
    """rows oldest-first [(round, userId, actionId, texts)]. Returns {"drTakenFromGear", "incDamageGivenFromGear",
    "n_mine", "n_his"} or None when there is no formula hit either way yet."""
    R = max(r for r, *_ in rows)
    saved = os.environ.get("TNR_HIS_GEAR_MODS_OFF")
    os.environ["TNR_HIS_GEAR_MODS_OFF"] = "1"
    try:
        req = EB._replay_request(rows, ME, en_id, {"curHealth": 5050}, {"curHealth": 5050}, (8, 5), (7, 4), R + 1,
                                 "same", value_model.load_cal())
    finally:
        if saved is None:
            os.environ.pop("TNR_HIS_GEAR_MODS_OFF", None)
    req["him"].pop("gearMods", None)
    req.update(mode="state", trace=True, round=R + 1)
    out = EB._run(req, 90)
    if not out:
        return None
    gear0 = (out.get("state") or {}).get("gear") or {}
    him0 = gear0.get("him", {})
    dr0, g0 = him0.get("drTakenFromGear", 0), him0.get("incDamageGivenFromGear", 0)
    trace = list(out.get("trace", []))
    mine, his = [], []
    for r, u, a, ts in rows:
        actor = "me" if u == ME else "him" if u == en_id else None
        if not actor or a in PIERCE:
            continue
        target = en_name if actor == "me" else me_name
        logged = sum(float(m.group(2)) for t in ts or [] if (m := HIT.match(t.strip())) and m.group(1) == target)
        i = next((k for k, x in enumerate(trace) if (x["round"], x["actor"], x["actionId"]) == (r, actor, a)), None)
        if i is None or logged < 100:
            continue
        t = trace.pop(i)
        eng = t.get("hits", {}).get("him" if actor == "me" else "me", 0)
        if eng >= 100:
            (mine if actor == "me" else his).append(logged / eng)
    if not mine and not his:
        return None
    res = {"n_mine": len(mine), "n_his": len(his), "assumed": {"drTakenFromGear": dr0, "incDamageGivenFromGear": g0}}
    res["drTakenFromGear"] = round(max(0.0, min(40.0, 50 - st.median(mine) * (50 - dr0))), 1) if mine else dr0
    res["incDamageGivenFromGear"] = round(max(0.0, min(150.0, st.median(his) * (160 + g0) - 160)), 1) if his else g0
    return res


def save(en_id, res):
    path = os.path.join(EB.HARNESS, "kit", "opponents", f"{en_id}.json")
    doc = EB.opponent_kit(en_id) or {"userId": en_id, "jutsu": [], "jutsuLevels": {}, "items": []}
    doc["gearMods"] = {"drTakenFromGear": res["drTakenFromGear"], "incDamageGivenFromGear": res["incDamageGivenFromGear"]}
    doc["gearFit"] = {k: res[k] for k in ("n_mine", "n_his", "assumed")}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(doc, open(path, "w"), indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entries")
    ap.add_argument("--enemy", required=True)
    ap.add_argument("--en-id", required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    lines = [l for l in open(a.entries).read().splitlines() if l.strip()]
    d = json.loads(lines[-1])   # an entries file, or turn.py's two-line battle + entries file
    rows = list(zip(d["*.battleRound"], d["*.userId"], d["*.actionId"], d["*.appliedEffects.*.txt"]))[::-1]
    res = fit(rows, a.en_id, a.enemy)
    print(json.dumps(res))
    if res and a.write:
        save(a.en_id, res)
        print("saved gearMods for", a.enemy)


if __name__ == "__main__":
    main()
