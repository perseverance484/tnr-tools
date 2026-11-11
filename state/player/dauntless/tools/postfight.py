#!/usr/bin/env python3
"""Post-fight check, run after EVERY fight (director, 2026-11-10: "After every fight there needs to be a check. If afk
discard data. If not afk, assign training data weights. Analyze fight in full to update weights and Analyze how much
value each turn provided, looking for good plays and blunders").

Input: the full battle log saved from combat.getBattleEntries {battleId, limit: 200} with
select ["*.battleRound","*.userId","*.actionId","*.appliedEffects.*.txt"] (newest first, as returned).

1. AFK check: if the enemy did nothing (only "wait"/timeouts, or no damage and no effects) on half or more of their
   turns, the fight is AFK -> its data is discarded (nothing written to train_log.jsonl).
2. Turn review: for every round I acted in, my actions, damage dealt / taken over the whole round (my turn + his),
   net value, running HP estimate, and flags:
     blunders - timeout (lost turn), Chakra Shield pierced, my buffs Cleared before they paid off, 60-AP burst into
                his absorb (>= 35% healed back), burst while I was smoked, Dr. Kim's when acting first while his
                same-round debuffs landed, death to a wound/drain tick;
     good     - net >= +600, kill blow, Cleanse removing a wound before it ticked, a Smoke/Subaku round that held his
                turn under 300.
3. Training data: samples (state, my actions, discounted return + win/loss terminal) replace any earlier samples of
   this battle in train_log.jsonl. Sample weight 1.0, 1.5 for flagged rounds (blunders and good plays teach most);
   then the policy is retrained from the hand seed on everything.
4. Writes fights/<battle>_review.md and prints a summary.

Usage: postfight.py FILE --battle ID --enemy NAME --result win|loss [--en-max 5050] [--no-train]
"""
import argparse
import json
import os
import re

import policy
from ingest import IDS, ME, swing
from state_rules import build_ctx

HERE = os.path.dirname(os.path.abspath(__file__))
FIGHTS = os.path.join(HERE, "..", "fights")
BURST = {"rebirth", "shrapnel", "lotus", "fury", "ember", "danse", "resonance"}
BUFFS = {"overflow", "ember", "thunders", "eclipse", "parry", "pill", "jewel", "sealnull", "kims", "phantom"}


def load(path):
    raw = json.load(open(path))
    effs = raw.get("*.appliedEffects.*.txt") or [[e["txt"] for e in (x or [])] for x in raw["*.appliedEffects"]]
    rows = list(zip(raw["*.battleRound"], raw["*.userId"], raw["*.actionId"], effs))[::-1]
    return [(r, u, a, [t.strip() for t in (e or [])]) for r, u, a, e in rows]


def afk_check(rows, me):
    turns, idle = {}, {}
    for r, u, a, t in rows:
        if u == me:
            continue
        turns.setdefault(r, []).append((a, t))
    rounds = sorted({r for r, *_ in rows})
    n_idle = 0
    for r in rounds:
        acts = turns.get(r, [])
        real = [a for a, t in acts if a not in ("wait",)]
        if not real:
            n_idle += 1
            idle[r] = True
    return n_idle, len(rounds), idle


def review(rows, me, enemy, en_max, me_max=5050.0):
    rounds = sorted({r for r, *_ in rows})
    out, lines, my_hp, en_hp = [], [], me_max, en_max
    cfg, th, _ = policy.cfg_for(enemy)
    for rnd in rounds:
        ents = [e for e in rows if e[0] == rnd]
        mine = [e for e in ents if e[1] == me]
        theirs = [e for e in ents if e[1] != me]
        first = bool(ents) and ents[0][1] == me
        ctx = build_ctx(lines, rnd, "dauntless", enemy, my_hp, en_hp)
        x = policy.features(ctx, th, me_max, en_max, [0.0] * 6, 3)
        acts = [IDS.get(a, a) for _, _, a, _ in mine]
        d, tk = swing([t for e in ents for t in e[3]], "dauntless", enemy)
        flags = []
        # ---- blunders
        if "wait" in acts:
            flags.append("BLUNDER timeout: lost my turn")
        if "shield" in acts and any("shield was pierced" in t for e in rows if e[0] in (rnd, rnd + 1) for t in e[3]):
            flags.append("BLUNDER Chakra Shield pierced (his pierce was ready)")
        buffs = [a for a in acts if a in BUFFS]
        last_mine = max((i for i, e in enumerate(rows) if e[0] == rnd and e[1] == me), default=-1)
        if buffs and any("dauntless was cleared of all positive" in t for e in rows[last_mine + 1:]
                         if e[0] in (rnd, rnd + 1) and e[1] != me for t in e[3]):
            flags.append(f"BLUNDER buffs {'+'.join(buffs)} Cleared before paying off")
        for _, _, a, t in mine:
            name = IDS.get(a, a)
            hit = sum(float(m.group(1)) for x_ in t for m in [re.match(rf"{enemy} takes ([\d.]+) damage", x_)] if m)
            heal = sum(float(m.group(1)) for x_ in t for m in [re.match(rf"{enemy} absorbs ([\d.]+)", x_)] if m)
            if name in BURST | {"nights", "stormblade"} and hit and heal >= 0.35 * hit:
                flags.append(f"BLUNDER {name} into absorb ({heal:.0f} of {hit:.0f} healed back)")
            if name in BURST and ctx.get("me_smoked"):
                flags.append(f"BLUNDER {name} while smoked (-70%)")
        if "kims" in acts and first and any(re.match(r"dauntless (damage taken .* increased|will recoil|will take)", t)
                                            for e in theirs for t in e[3]):
            flags.append("BLUNDER Dr. Kim's while acting first - his same-round debuffs still landed")
        # ---- good plays
        if d - tk >= 600:
            flags.append(f"GOOD net {d - tk:+.0f}")
        if "cleanse" in acts and ctx.get("me_wound_live") and acts and acts[0] == "cleanse":
            flags.append("GOOD Cleanse first: wound/drain removed before ticking")
        prev = [e for e in rows if e[0] == rnd - 1 and e[1] == me]
        if any(IDS.get(a) in ("smoke", "subaku") for _, _, a, _ in prev):
            his = sum(float(m.group(1)) for e in theirs for t in e[3]
                      for m in [re.match(r"dauntless takes ([\d.]+) damage", t)] if m)
            if his < 300:
                flags.append(f"GOOD Smoke/Subaku held his turn to {his:.0f}")
        en_hp -= d
        my_hp -= tk
        lines += [f"{rnd}|{t}" for e in ents for t in e[3]]
        if acts:
            out.append({"round": rnd, "first": first, "acts": acts, "dealt": round(d), "taken": round(tk),
                        "net": round(d - tk), "my_hp": round(my_hp), "en_hp": round(en_hp), "flags": flags, "x": x})
    if out and out[-1]["my_hp"] <= 0 and any("wound" in t or "drain" in t for e in rows if e[0] == out[-1]["round"]
                                               and e[1] == me for t in e[3]):
        out[-1]["flags"].append("BLUNDER died to my own wound/drain tick (Cleanse was needed)")
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("file"); p.add_argument("--battle", required=True); p.add_argument("--enemy", required=True)
    p.add_argument("--result", required=True, choices=["win", "loss"]); p.add_argument("--en-max", type=float, default=5050)
    p.add_argument("--no-train", action="store_true")
    a = p.parse_args()
    rows = load(a.file)
    n_idle, n_rounds, idle = afk_check(rows, ME)
    afk = n_rounds > 0 and n_idle * 2 >= n_rounds
    turns = review(rows, ME, a.enemy, a.en_max)
    md = [f"# {a.battle} vs {a.enemy}: {a.result.upper()} in R{n_rounds}",
          f"AFK check: enemy idle in {n_idle}/{n_rounds} rounds -> {'AFK: data discarded' if afk else 'active: data kept'}",
          "", "| R | first | my actions | dealt | taken | net | my HP | his HP | notes |", "|---|---|---|---|---|---|---|---|---|"]
    for t in turns:
        md.append(f"| {t['round']} | {'me' if t['first'] else 'him'} | {'+'.join(t['acts'])} | {t['dealt']} | {t['taken']} | "
                  f"{t['net']:+d} | {t['my_hp']} | {t['en_hp']} | {'; '.join(t['flags'])} |")
    blunders = [f for t in turns for f in t["flags"] if f.startswith("BLUNDER")]
    goods = [f for t in turns for f in t["flags"] if f.startswith("GOOD")]
    best = max(turns, key=lambda t: t["net"]) if turns else None
    worst = min(turns, key=lambda t: t["net"]) if turns else None
    md += ["", f"Blunders: {len(blunders)}. Good plays: {len(goods)}."]
    if best:
        md.append(f"Best turn: R{best['round']} {'+'.join(best['acts'])} ({best['net']:+d}); "
                  f"worst: R{worst['round']} {'+'.join(worst['acts'])} ({worst['net']:+d}).")
    os.makedirs(FIGHTS, exist_ok=True)
    open(os.path.join(FIGHTS, f"{a.battle}_review.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))
    if afk or a.no_train:
        print("no training data written" + (" (AFK)" if afk else ""))
        return
    d = {"enemy": a.enemy, "result": a.result,
         "rounds": {str(t["round"]): {"x": t["x"], "acts": [x for x in t["acts"] if x in policy.ACTIONS],
                                      "r": t["net"] / 1000} for t in turns}}
    ss = policy.samples_from(d, a.battle)
    flagged = {t["round"] for t in turns if t["flags"]}
    for s in ss:
        s["w"] = 1.5 if s.get("round") in flagged else 1.0
    keep = []
    if os.path.exists(policy.TRAIN_LOG):
        keep = [l for l in open(policy.TRAIN_LOG) if json.loads(l).get("battle") != a.battle]
    with open(policy.TRAIN_LOG, "w") as f:
        f.writelines(keep)
        for s in ss:
            f.write(json.dumps(s) + "\n")
    print(f"{len(ss)} training samples written (weights 1.0 / 1.5 flagged)")
    policy.retrain(10, 0.003)
    recalibrate()


def recalibrate():
    """Refresh calibration.json (turn.py's value model) from every logged fight, including this one."""
    import subprocess, sys
    r = subprocess.run([sys.executable, os.path.join(HERE, "calibrate.py")], capture_output=True, text=True)
    print("value model recalibrated" if r.returncode == 0 else f"calibrate.py failed: {r.stderr[-300:]}")


if __name__ == "__main__":
    main()
