#!/usr/bin/env python3
"""Learned PvP policy (director, 2026-11-10: "You dont do live thinking you edit the weights for the state rules and
modify the jutsu kit" ... "Treat it like a neural network").

Network: input layer = battle-state features (from the battle log via state_rules.build_ctx), output layer = one
unit per kit action (cd_plan.ACTIONS short names). score(action) = w_action . features. A turn's bundle score is
the sum of its actions' scores; the policy fires the best LEGAL bundle (AP incl. stun, cooldowns and shared locks
from cd_plan state, debuff-immunity filter) and names the runner-up as the backup. No live reasoning: in a fight
run `act`, fire FIRE, on any refusal fire BACKUP.

Weights: tools/policy_weights.json. Hand-tuned seed (director: "You hand tune it based on your knowledge
initially and it fine tunes") from rules_config.json (the hand rules are the prior), then trained
after every fight from rewards (net HP swing of the round, mine minus theirs), by gradient steps on squared error
(w += lr * (reward - prediction) * x, prediction shared across the bundle's actions). The kit is the output layer:
add/remove an action in cd_plan.ACTIONS/LOADOUTS and run `init --keep` to add its unit.

Usage:
  policy.py init [--keep]                       seed weights from rules_config.json (--keep: only add new units)
  policy.py act LOG ROUND --enemy NAME --battle B [--ap 100] [--my-hp N --en-hp N] [--en-max 5000]
      prints FIRE / BACKUP; stores the features for this round in /tmp/policy_<B>.json
  policy.py reward B ROUND ACTIONS DEALT TAKEN   attach the outcome (actions actually fired, comma list)
  policy.py train B [--lr 0.05]                  gradient steps on that fight's samples; appends to train_log.jsonl
  policy.py show [ACTION]                         print weights
"""
import argparse
import itertools
import json
import os

from cd_plan import ACTIONS, LOCKS, LOADOUTS, load, ready_round
from state_rules import build_ctx

HERE = os.path.dirname(os.path.abspath(__file__))
WFILE = os.path.join(HERE, "policy_weights.json")
CFG = os.path.join(HERE, "rules_config.json")
TRAIN_LOG = os.path.join(HERE, "train_log.jsonl")

FEATURES = ["bias", "lethal_risk", "kill_window", "stack_clearable", "stack_clearable_immune",
            "stack_clearprevented", "recoil_on_me", "en_sustain", "en_dr_or_shield", "me_debuffed", "en_reflect",
            "stack_building", "my_absorb_down", "en_immune", "me_stunned", "my_given_live", "en_taken_live",
            "my_hp_frac", "en_hp_frac", "en_idg"]
RULE_FEATURE = {"always": "bias"}  # every other rule 'when' is a feature of the same name


def features(c, th, my_max, en_max):
    idg = c["en_idg"]
    f = {
        "bias": 1.0,
        "lethal_risk": float(bool(c["my_hp"]) and c["my_hp"] < th["lethal_my_hp"] and idg > th["lethal_en_idg"]),
        "kill_window": float(bool(c["en_hp"]) and c["en_hp"] < th["kill_en_hp"]),
        "stack_clearable": float(idg >= th["clear_en_idg"] and not c["en_clearprevent"] and not c["en_immune"]),
        "stack_clearable_immune": float(idg >= th["clear_en_idg"] and not c["en_clearprevent"] and c["en_immune"]),
        "stack_clearprevented": float(idg >= th["clear_en_idg"] and c["en_clearprevent"]),
        "recoil_on_me": float(c["me_recoil"] >= th["recoil_on_me"]),
        "en_sustain": float(c["en_absorb"] >= th["en_absorb"] or c["en_lifesteal"] >= th["en_lifesteal"]),
        "en_dr_or_shield": float(c["en_dr"] >= th["en_dr"] or c["en_shield"]),
        "me_debuffed": float(c["me_debuffs"] >= th["my_debuffs"] or c["me_wound_drain"] >= th["my_wound_drain"]),
        "en_reflect": float(c["en_reflect"] >= th["en_reflect"]),
        "stack_building": float(th["build_en_idg"] <= idg < th["clear_en_idg"]),
        "my_absorb_down": float(c["my_absorb_low"]),
        "en_immune": float(c["en_immune"]),
        "me_stunned": float(c["me_stunned"]),
        "my_given_live": float(c["my_given_live"]),
        "en_taken_live": float(c["en_taken_live"]),
        "my_hp_frac": (c["my_hp"] / my_max) if c["my_hp"] else 1.0,
        "en_hp_frac": (c["en_hp"] / en_max) if c["en_hp"] else 1.0,
        "en_idg": min(idg, 2.0),
    }
    return [f[k] for k in FEATURES]


def cfg_for(enemy):
    cfg = json.load(open(CFG))
    prof = cfg.get("profiles", {}).get((enemy or "").lower(), {})
    th = dict(cfg["thresholds"], **prof.get("thresholds", {}))
    return cfg, th


def seed(keep):
    cfg = json.load(open(CFG))
    old = json.load(open(WFILE)) if keep and os.path.exists(WFILE) else {}
    W = {a: [0.0] * len(FEATURES) for a in ACTIONS}
    for rule in cfg["rules"]:
        fi = FEATURES.index(RULE_FEATURE.get(rule["when"], rule["when"]))
        for rank, bundle in enumerate(rule["bundles"]):
            for a in bundle:
                # prior: rule weight/100, first bundle strongest; bias rule seeds weakly
                # scaled by AP share so a bundle's total ~= the rule weight whatever its size
                W[a][fi] += rule["weight"] / 100 * ACTIONS[a][0] / 100 * (1.0 - 0.25 * rank) * (0.3 if fi == 0 else 1.0)
    # cash-in priors: hits are worth more while my buffs / their +taken are live
    for a in ("rebirth", "shrapnel", "fury", "ember", "danse", "lotus", "resonance", "aetherion", "kunai"):
        W[a][FEATURES.index("my_given_live")] += 0.5 * ACTIONS[a][0] / 100
        W[a][FEATURES.index("en_taken_live")] += 0.5 * ACTIONS[a][0] / 100
    for a in ("overflow", "thunders", "eclipse", "parry", "pill", "jewel"):  # don't re-buff on a cash-in round
        W[a][FEATURES.index("my_given_live")] -= 0.3 * ACTIONS[a][0] / 100
    for a, w in old.items():
        if a in W and len(w) == len(FEATURES):
            W[a] = w
    json.dump(W, open(WFILE, "w"), indent=0)
    print(f"weights: {len(W)} action units x {len(FEATURES)} features -> {WFILE}")


def score(W, x, a):
    return sum(w * v for w, v in zip(W[a], x))


def legal(state, rnd, ap, immune, blocked, loadout):
    names = [n for n in loadout if n in ACTIONS and (state is None or ready_round(state, n) <= rnd)]
    if immune:
        names = [n for n in names if n not in blocked]
    out = []
    for k in (1, 2, 3, 4):
        for combo in itertools.combinations(names, k):
            cost = sum(ACTIONS[c][0] for c in combo)
            if cost > ap or ap - cost >= 20:  # must spend the AP (fillers included in the search)
                continue
            tags = [ACTIONS[c][2] for c in combo if ACTIONS[c][2]]
            if len(tags) != len(set(tags)):
                continue
            out.append(combo)
    return out


def act(a):
    cfg, th = cfg_for(a.enemy)
    W = json.load(open(WFILE))
    lines = [l.strip() for l in open(a.log) if l.strip()]
    c = build_ctx(lines, a.round, "dauntless", a.enemy, a.my_hp, a.en_hp)
    x = features(c, th, a.my_max, a.en_max)
    state = load(a.battle) if a.battle else None
    loadout = state["loadout"] if state else LOADOUTS["pvp1"]
    ap = a.ap - (20 if c["me_stunned"] and a.ap == 100 else 0)
    bundles = legal(state, a.round, ap, c["en_immune"], set(cfg["immune_blocked"]), loadout)
    ranked = sorted(((sum(score(W, x, n) for n in b), b) for b in bundles), key=lambda t: -t[0])
    on = [k for k, v in zip(FEATURES, x) if v and k not in ("bias", "my_hp_frac", "en_hp_frac", "en_idg")]
    print(f"r{a.round} {ap} AP  features on: {', '.join(on) or 'none'}  (en_idg {c['en_idg']:+.0%})")
    if not ranked:
        print("FIRE: defstance (no legal bundle)")
        return
    print(f"FIRE:   {' + '.join(ranked[0][1])}   ({ranked[0][0]:.2f})")
    backup = next((r for r in ranked[1:] if not set(r[1]) & set(ranked[0][1])), ranked[1] if len(ranked) > 1 else None)
    if backup:
        print(f"BACKUP: {' + '.join(backup[1])}   ({backup[0]:.2f})")
    if a.battle:
        p = f"/tmp/policy_{a.battle}.json"
        d = json.load(open(p)) if os.path.exists(p) else {"enemy": a.enemy, "rounds": {}}
        d["rounds"][str(a.round)] = {"x": x}
        json.dump(d, open(p, "w"))


def reward(b, rnd, acts, dealt, taken):
    p = f"/tmp/policy_{b}.json"
    d = json.load(open(p))
    d["rounds"].setdefault(str(rnd), {})
    d["rounds"][str(rnd)].update({"acts": acts.split(","), "r": (float(dealt) - float(taken)) / 1000})
    json.dump(d, open(p, "w"))
    print(f"r{rnd}: {acts} reward {(float(dealt) - float(taken)) / 1000:+.2f}")


def train(b, lr):
    W = json.load(open(WFILE))
    d = json.load(open(f"/tmp/policy_{b}.json"))
    n = 0
    for rnd, s in sorted(d["rounds"].items(), key=lambda t: int(t[0])):
        if "x" not in s or "acts" not in s:
            continue
        x, acts, r = s["x"], [a for a in s["acts"] if a in W], s["r"]
        pred = sum(score(W, x, a) for a in acts)
        err = r - pred
        for a in acts:
            W[a] = [w + lr * err / len(acts) * v for w, v in zip(W[a], x)]
        n += 1
        with open(TRAIN_LOG, "a") as f:
            f.write(json.dumps({"battle": b, "enemy": d["enemy"], "round": int(rnd), "x": x, "acts": acts,
                                "r": r}) + "\n")
    json.dump(W, open(WFILE, "w"), indent=0)
    print(f"trained on {n} rounds of {b}")


def show(action):
    W = json.load(open(WFILE))
    for a in ([action] if action else sorted(W)):
        top = sorted(zip(FEATURES, W[a]), key=lambda t: -abs(t[1]))[:5]
        print(f"{a:11s} " + "  ".join(f"{k}:{v:+.2f}" for k, v in top if v))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("init"); s.add_argument("--keep", action="store_true")
    s = sp.add_parser("act"); s.add_argument("log"); s.add_argument("round", type=int)
    s.add_argument("--enemy", required=True); s.add_argument("--battle", default="")
    s.add_argument("--ap", type=int, default=100); s.add_argument("--my-hp", type=float, default=0)
    s.add_argument("--en-hp", type=float, default=0); s.add_argument("--my-max", type=float, default=5050)
    s.add_argument("--en-max", type=float, default=5000)
    s = sp.add_parser("reward"); [s.add_argument(k) for k in ("battle", "round", "acts", "dealt", "taken")]
    s = sp.add_parser("train"); s.add_argument("battle"); s.add_argument("--lr", type=float, default=0.05)
    s = sp.add_parser("show"); s.add_argument("action", nargs="?")
    a = p.parse_args()
    if a.cmd == "init":
        seed(a.keep)
    elif a.cmd == "act":
        act(a)
    elif a.cmd == "reward":
        reward(a.battle, a.round, a.acts, a.dealt, a.taken)
    elif a.cmd == "train":
        train(a.battle, a.lr)
    elif a.cmd == "show":
        show(a.action)
