#!/usr/bin/env python3
"""Replay fidelity: does the engine replay of a logged fight reproduce the logged damage, action by action?

Replays every logged action of both sides (replay_sim.ts, real records from kit/catalog.json, his saved kit and
levels when kit/opponents/<id>.json exists) and compares the engine's HP loss on the target with the log's
"<target> takes N damage" lines (direct hits only; afterburn / recoil / reflect / wound / drain ticks excluded on
both the logged side and, where separable, reported as notes). Offline; no live calls.

Note: the replay floors both sides at 3000 HP between actions so a long log never kills anyone; a per-action delta is
exact unless a single action crosses that floor.
Usage: replay_fidelity.py FIGHT_ENTRIES.json --enemy NAME --en-id USER_ID [--me-id ID]
"""
import argparse
import json
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "state/player/dauntless/tools"))
import engine_bridge as EB  # noqa: E402
import value_model  # noqa: E402

ME = "user_37qazcrgUPldBPI65bb25DQiCjz"
HIT = re.compile(r"^(\S+) takes ([\d.]+) damage$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entries")
    ap.add_argument("--enemy", required=True)
    ap.add_argument("--en-id", required=True)
    ap.add_argument("--me-id", default=ME)
    a = ap.parse_args()
    d = json.load(open(a.entries))
    rows = list(zip(d["*.battleRound"], d["*.userId"], d["*.actionId"], d["*.appliedEffects.*.txt"]))[::-1]
    R = max(r for r, *_ in rows)
    req = EB._replay_request(rows, a.me_id, a.en_id, {"curHealth": 5050}, {"curHealth": 5050}, (8, 5), (7, 4),
                             R + 1, "same", value_model.load_cal())
    req["round"] = R + 1
    req["mode"] = "list"
    req["trace"] = True
    out = EB._run(req, 60)
    if not out:
        sys.exit("engine run failed (set TNR_ENGINE_DEBUG=1)")
    names = {k: v["record"]["name"] for k, v in EB._records().items()}
    trace = list(out.get("trace", []))
    errs = []
    print(f"{'R':>2} {'actor':5} {'action':28} {'logged':>7} {'engine':>7}")
    for r, u, act, ts in rows:
        if act in EB.SKIP or act in ("move",):
            continue
        actor = "me" if u == a.me_id else "him"
        target = a.enemy if actor == "me" else "dauntless"
        logged = sum(float(m.group(2)) for t in ts or [] if (m := HIT.match(t.strip())) and m.group(1) == target)
        i = next((k for k, x in enumerate(trace) if (x["round"], x["actor"], x["actionId"]) == (r, actor, act)), None)
        t = trace.pop(i) if i is not None else None
        eng = (t["him"] if actor == "me" else t["me"]) if t else None
        flag = ""
        if eng is not None and logged >= 100:
            e = abs(eng - logged) / logged
            errs.append(e)
            flag = f"{e:5.0%}" + ("  <-- off" if e > 0.15 else "")
        print(f"{r:>2} {actor:5} {names.get(act, act)[:28]:28} {logged:7.0f} {eng if eng is not None else '-':>7} {flag}")
    if out.get("replayIssues"):
        print("replay issues:", [(i["round"], i["actor"], names.get(i["actionId"], i["actionId"]), i["reason"])
                                 for i in out["replayIssues"]])
    if errs:
        errs.sort()
        print(f"compared {len(errs)} hits: median error {errs[len(errs) // 2]:.1%}, within 10% {sum(e <= .1 for e in errs)}")
    print("his kit:", EB.his_kit_source(a.en_id))


if __name__ == "__main__":
    main()
