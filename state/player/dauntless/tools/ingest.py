#!/usr/bin/env python3
"""Pre-train policy.py from recorded fights (director, 2026-11-10: "Pre-train it on all 3 luka fights and the
ashutosh fight").

Input: combat.getBattleEntries {battleId, limit} with select ["*.battleRound","*.userId","*.actionId",
"*.appliedEffects"] saved as JSON (newest first, as the endpoint returns). For each round I acted in, the state is
rebuilt from every effect line logged before my first action that round (state_rules.build_ctx), my actions are
mapped to kit short names, and the reward is that round's net HP swing (damage to them incl. afterburn/reflect/
recoil/drain minus their heals, minus damage to me net of my absorb/heals). Samples get discounted returns +
terminal from policy.samples_from and are appended to train_log.jsonl. Distance and enemy-threat inputs are not in
the entries, so they are filled neutral (dist 3, threats 0).

Usage: ingest.py FILE --battle ID --enemy NAME --result win|loss [--me-id user_...] [--en-max 5000]
"""
import argparse
import json
import re

import policy
from cd_plan import ACTIONS
from state_rules import build_ctx

ME = "user_37qazcrgUPldBPI65bb25DQiCjz"
IDS = {"K0t6Z-Q4lau1jFt8Tkpot": "rebirth", "GiKpip6NxsC8QWlZi6l_R": "shrapnel", "zCmYLVL4JYzfhjPXHi9rH": "lotus",
       "Lg_thN-MB8FRAr_Agf9tn": "fury", "Wy7EBGd7gpP96hyumb0Lz": "ember", "cvLrFEzeNcRogHqyLv0Ig": "danse",
       "G6MRbppaDZ2a5Wr0GIjH8": "stormblade", "jELEiw5W3N4m2R3oJm3Pk": "subaku", "e2eC-x4UXc5m6QexNbx8w": "overflow",
       "qNeccb2eF20oL0Ws-VhKS": "thunders", "73Sn-ihCNNRwxZ_G_2lTZ": "parry", "ou7VyChQ-SFCm8T8yGS7I": "eclipse",
       "g-b0Fs5o8EzQIphq0YIAX": "sealnull", "GAyHRgaa1lkYGhE9WxlRL": "phantom", "FimDQpYL0LWRv8U81ZP9H": "shield",
       "kxtK9kUTK4dRb-WPLo16I": "severed", "0nIgI7oNn-PSesn8T8kGl": "leech", "LRgY4b-lE1n2gi6_P8B_1": "resonance",
       "TtYPd-LcXKeK3sMuhq1TP": "smoke", "rsc2uO5QuffXzejfhwF_F": "panacea", "_8HEbybzN5QPX8vUG24Tk": "jewel",
       "tZTvqYWiAc_OrY64nDvIo": "pill", "6DnJn4x6LWWXtBu7UZybb": "kims", "osJq3k77YPGoFWgof12FQ": "nights",
       "Z-JdppXvrSokRymXavpOw": "yuki", "RM9DjOswzqNTRWnd-FsdE": "disaster", "GMF1JZ0MChUHc7AtnKABw": "kunai", "PhP5ZEF5iVa97jcumJ15c": "aetherion",
       "clear": "clear", "cleanse": "cleanse", "replacementTechnique": "replace", "defensiveStance": "defstance",
       "offensiveStance": "offstance", "move": "step"}
NUM = r"([\d.]+)"


def swing(txts, me, en):
    dealt = taken = 0.0
    for t in txts:
        m = re.match(rf"{en} takes {NUM}", t)
        if m:
            dealt += float(m.group(1))
        m = re.match(rf"{me} takes {NUM}", t)
        if m:
            taken += float(m.group(1))
        m = re.match(rf"{en} (?:heals|vamps|absorbs|steals) {NUM}", t)
        if m and "SP" not in t and "CP" not in t:
            dealt -= float(m.group(1))
        m = re.match(rf"{me} (?:heals|vamps|absorbs|steals) {NUM}", t)
        if m and "SP" not in t and "CP" not in t:
            taken -= float(m.group(1))
    return dealt, taken


def ingest(path, battle, enemy, result, me_id=ME, en_max=5000.0, me_max=5050.0, weight=1.0):
    raw = json.load(open(path))
    rounds, users, acts = (raw[k] for k in ("*.battleRound", "*.userId", "*.actionId"))
    if "*.appliedEffects.*.txt" in raw:
        effs = [[{"txt": t} for t in e] for e in raw["*.appliedEffects.*.txt"]]
    else:
        effs = raw["*.appliedEffects"]
    entries = list(zip(rounds, users, acts, effs))[::-1]  # chronological
    cfg, th, _ = policy.cfg_for(enemy)
    lines, out, my_hp, en_hp = [], {}, me_max, en_max
    seen = set()
    for i, (r, u, a, eff) in enumerate(entries):
        txts = [e["txt"].strip() for e in (eff or [])]
        if u == me_id and r not in seen:
            seen.add(r)
            c = build_ctx(lines, r, "dauntless", enemy, my_hp, en_hp)
            x = policy.features(c, th, me_max, en_max, [0.0] * 6, 3)
            mine = [IDS.get(e[2], "?") for e in entries if e[0] == r and e[1] == me_id]
            rt = [t.strip() for e in entries if e[0] == r for t in [x_["txt"] for x_ in (e[3] or [])]]
            d, tk = swing(rt, "dauntless", enemy)
            out[str(r)] = {"x": x, "acts": [m for m in mine if m in ACTIONS], "r": (d - tk) / 1000,
                           "raw": mine, "dealt": round(d), "taken": round(tk)}
        d, tk = swing(txts, "dauntless", enemy)
        en_hp -= d
        my_hp -= tk
        lines += [f"{r}|{t}" for t in txts]
    d = {"enemy": enemy, "rounds": out, "result": result}
    ss = policy.samples_from(d, battle)
    with open(policy.TRAIN_LOG, "a") as f:
        for s in ss:
            s["w"] = weight
            f.write(json.dumps(s) + "\n")
    for k, v in sorted(out.items(), key=lambda t: int(t[0])):
        print(f"  r{k}: {'+'.join(v['raw']):40s} dealt {v['dealt']:5d} taken {v['taken']:5d}")
    print(f"{battle} vs {enemy} ({result}): {len(ss)} samples, est. HP end me {my_hp:.0f} / them {en_hp:.0f}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("file"); p.add_argument("--battle", required=True); p.add_argument("--enemy", required=True)
    p.add_argument("--result", required=True, choices=["win", "loss"]); p.add_argument("--me-id", default=ME)
    p.add_argument("--en-max", type=float, default=5000)
    p.add_argument("--weight", type=float, default=1.0, help="0.3 for AFK opponents")
    a = p.parse_args()
    ingest(a.file, a.battle, a.enemy, a.result, a.me_id, a.en_max, weight=a.weight)
