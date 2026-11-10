#!/usr/bin/env python3
"""Learned PvP policy (director, 2026-11-10: "You dont do live thinking you edit the weights for the state rules and
modify the jutsu kit" / "Treat it like a neural network" / "You hand tune it based on your knowledge initially and it
fine tunes" / "Add range checking and make it more sophisticated").

Network (pure Python, no deps):
  input x   = battle-state features (state_rules.build_ctx on the battle log) + enemy-threat features
              (enemy_model.threat_features for profiled opponents) + range features.
  hidden h  = ReLU(W1 x + b1), H units (small random init).
  output    = one unit per kit action: q(a) = w_a . x  (hand-tuned prior, linear skip)  +  v_a . h  (learned, starts 0)
  bundle    = sum q(a) + pair weights P[a|b] (hand-tuned synergy / anti-synergy, trainable) - cooldown cost
So on day one the policy is exactly the hand-tuned rules; fights train both the prior and the hidden layer.

Legality (hard filter, never learned): AP (80 when stunned), own cooldowns + shared locks (cd_plan state),
debuff immunity, RANGE: targeted actions need the enemy within their range after any move in the bundle
(Phantom Step / Replacement 5, basic step 1 at 10 AP), AP must be fully spent (< 10 left over).

Training: per round, reward r = (dealt - taken)/1000 (+ heal/absorb counts in taken already). Target is the
discounted n-step return G_t = r_t + g*r_{t+1} + ... + g^k * terminal (+2 win / -2 loss), so setup rounds get
credit for the payoff round. Squared-error backprop through skip weights, output weights, hidden layer and pairs.
Every sample is appended to tools/train_log.jsonl; `retrain` replays all of them (epochs) from the hand seed.

Usage:
  policy.py init [--keep]            hand seed from rules_config.json (--keep: keep learned weights, add new units)
  policy.py act LOG ROUND --enemy NAME --battle B --dist N [--ap 100] [--my-hp N --en-hp N] [--top 3]
  policy.py reward B ROUND ACTIONS DEALT TAKEN
  policy.py result B win|loss
  policy.py train B [--lr 0.03]       train on one fight
  policy.py retrain [--epochs 20]     re-seed and replay every logged fight
  policy.py show [ACTION]
"""
import argparse
import itertools
import json
import math
import os
import random

from cd_plan import ACTIONS, LOADOUTS, MOVES, RANGE, load, ready_round
from enemy_model import threat_features
from state_rules import build_ctx

HERE = os.path.dirname(os.path.abspath(__file__))
WFILE = os.path.join(HERE, "policy_weights.json")
CFG = os.path.join(HERE, "rules_config.json")
TRAIN_LOG = os.path.join(HERE, "train_log.jsonl")
H = 12
GAMMA = 0.6
TERMINAL = 1.0

FEATURES = ["bias", "lethal_risk", "kill_window", "stack_clearable", "stack_clearable_immune",
            "stack_clearprevented", "recoil_on_me", "en_sustain", "en_dr_or_shield", "me_debuffed", "en_reflect",
            "stack_building", "my_absorb_down", "en_immune", "me_stunned", "my_given_live", "en_taken_live",
            "my_hp_frac", "en_hp_frac", "en_idg",
            "pred_burst", "pred_buff", "pred_stun", "pred_immune", "en_pierce_ready", "en_clear_ready",
            "far", "close", "me_wound", "me_smoked", "i_first", "en_clear_spent", "nights_kills", "storm_kills"]
RULE_FEATURE = {"always": "bias"}
# firing order inside a bundle: move first, then instant protection / strip, then buffs, then damage, fillers last
ORDER = ["phantom", "replace", "step", "clear", "cleanse", "kims", "sealnull", "danse", "shield", "subaku", "fury",
         "smoke", "severed", "disaster", "ember", "aetherion", "overflow", "thunders", "eclipse", "parry", "rebirth",
         "shrapnel", "lotus", "resonance", "leech", "yuki", "stormblade", "nights", "kunai", "pill", "jewel",
         "panacea", "defstance", "offstance"]


def features(c, th, my_max, en_max, threats, dist):
    idg = c["en_idg"]
    f = {
        "bias": 1.0,
        # lethal: low HP into a stack, OR any HP into a huge stack (+150%: his burst is ~2-3k)
        "lethal_risk": float(bool(c["my_hp"]) and ((c["my_hp"] < th["lethal_my_hp"] and idg > th["lethal_en_idg"])
                                                     or (idg >= 1.5 and c["my_hp"] < 4200))),
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
        "far": float(dist > 4), "close": float(dist <= 2),
        "me_wound": float(c.get("me_wound_live", False)),
        "me_smoked": float(c.get("me_smoked", False)),
        "i_first": float(c.get("i_first", False)),
        "en_clear_spent": float(c.get("en_clear_spent", False)),
        # flat pierce finishes: Night's 631, Stormblade 707 (ignore DR/smoke; shields break)
        "nights_kills": float(0 < c["en_hp"] <= 631),
        "storm_kills": float(0 < c["en_hp"] <= 707),
    }
    for k, v in zip(["pred_burst", "pred_buff", "pred_stun", "pred_immune", "en_pierce_ready", "en_clear_ready"],
                    threats):
        f[k] = v
    return [f[k] for k in FEATURES]


def cfg_for(enemy):
    cfg = json.load(open(CFG))
    prof = cfg.get("profiles", {}).get((enemy or "").lower(), {})
    th = dict(cfg["thresholds"], **prof.get("thresholds", {}))
    return cfg, th, prof


# ---------------------------------------------------------------- network
def blank():
    rnd = random.Random(7)
    return {"W": {a: [0.0] * len(FEATURES) for a in ACTIONS},
            "V": {a: [0.0] * H for a in ACTIONS},
            "W1": [[rnd.gauss(0, 0.15) for _ in FEATURES] for _ in range(H)],
            "b1": [0.0] * H,
            "P": {}, "features": FEATURES, "H": H}


def seed(keep=False, quiet=False):
    cfg = json.load(open(CFG))
    net = blank()
    W = net["W"]
    fx = FEATURES.index
    for rule in cfg["rules"]:
        fi = fx(RULE_FEATURE.get(rule["when"], rule["when"]))
        for rank, bundle in enumerate(rule["bundles"]):
            for a in bundle:
                W[a][fi] += rule["weight"] / 100 * ACTIONS[a][0] / 100 * (1.0 - 0.25 * rank) * (0.3 if fi == 0 else 1.0)
    for a in ("rebirth", "shrapnel", "fury", "ember", "danse", "lotus", "resonance", "aetherion", "kunai",
              "stormblade", "nights"):  # cash in while buffs/debuffs are live
        W[a][fx("my_given_live")] += 0.5 * ACTIONS[a][0] / 100
        W[a][fx("en_taken_live")] += 0.5 * ACTIONS[a][0] / 100
    for a in ("overflow", "thunders", "eclipse", "parry", "pill", "jewel"):
        W[a][fx("my_given_live")] -= 0.3 * ACTIONS[a][0] / 100
    hand = cfg.get("prior", {})  # extra hand weights: {"action": {"feature": w}}
    for a, fw in hand.items():
        for f, w in fw.items():
            W[a][fx(f)] += w
    for pair, w in cfg.get("pairs", {}).items():
        net["P"][pair] = w
    if keep and os.path.exists(WFILE):
        old = json.load(open(WFILE))
        if old.get("features") == FEATURES and old.get("H") == H:
            for k in ("W", "V"):
                for a, w in old[k].items():
                    if a in net[k]:
                        net[k][a] = w
            net["W1"], net["b1"] = old["W1"], old["b1"]
            net["P"].update(old["P"])
    json.dump(net, open(WFILE, "w"))
    if not quiet:
        print(f"net: {len(FEATURES)} inputs -> {H} hidden -> {len(ACTIONS)} action units, {len(net['P'])} pair weights")
    return net


def hidden(net, x):
    z = [sum(w * v for w, v in zip(row, x)) + b for row, b in zip(net["W1"], net["b1"])]
    return z, [max(0.0, t) for t in z]


def q(net, x, h, a):
    return sum(w * v for w, v in zip(net["W"][a], x)) + sum(w * v for w, v in zip(net["V"][a], h))


def pkey(a, b):
    return "|".join(sorted((a, b)))


def bundle_value(net, x, h, b, cd_cost):
    v = sum(q(net, x, h, a) for a in b)
    v += sum(net["P"].get(pkey(a, c), 0.0) for a, c in itertools.combinations(b, 2))
    v -= cd_cost * sum(ACTIONS[a][1] for a in b if a not in ("step",))
    return v


# ---------------------------------------------------------------- legality
def legal(state, rnd, ap, immune, blocked, loadout, dist):
    names = [n for n in loadout if n in ACTIONS and (state is None or ready_round(state, n) <= rnd)]
    if immune:
        names = [n for n in names if n not in blocked]
    out = []
    for k in (1, 2, 3, 4):
        for combo in itertools.combinations(names, k):
            cost = sum(ACTIONS[c][0] for c in combo)
            if cost > ap:
                continue
            tags = [ACTIONS[c][2] for c in combo if ACTIONS[c][2]]
            if len(tags) != len(set(tags)):
                continue
            need = min([RANGE[c] for c in combo if RANGE.get(c)], default=99)
            d = max(1, dist - sum(MOVES.get(c, 0) for c in combo))
            steps = max(0, d - need)
            mv = [c for c in combo if c in ("replace",)]  # pure moves: only if needed to reach range
            if mv and (need == 99 or max(1, dist - sum(MOVES.get(c, 0) for c in combo if c != "replace")) <= need):
                continue
            if steps * 10 + cost > ap:
                continue
            full = combo + ("step",) * steps
            if ap - (cost + steps * 10) >= 10:  # unspent AP
                continue
            out.append(full)
    return out


def ordered(b):
    return sorted(b, key=lambda a: ORDER.index(a) if a in ORDER else 99)


# ---------------------------------------------------------------- commands
# rough unbuffed damage per action (observed 2026-11-10: Rebirth ~600, Shrapnel ~650, Lotus ~600, Ember ~600,
# Fury ~450, Danse ~500, Captain's Decree ~350, basic ~150; pierce flat)
EST = {"rebirth": 600, "shrapnel": 650, "lotus": 600, "ember": 600, "fury": 450, "danse": 500, "resonance": 450,
       "aetherion": 350, "phantom": 0, "basic": 150, "kunai": 300, "stormblade": 707, "nights": 631}
PIERCE = {"stormblade", "nights"}


def est_damage(bundle, c):
    """Damage this bundle deals now: my live +given x their +taken x their DR, smoke; pierce flat."""
    mult = (1 + c.get("my_given_mult", 0)) * (1 + c.get("en_taken_mult", 0)) * (1 - c["en_dr"])
    if c.get("me_smoked"):
        mult *= 0.3
    return sum(EST.get(a, 0) * (1 if a in PIERCE else mult) for a in bundle)


def act(a):
    cfg, th, prof = cfg_for(a.enemy)
    net = json.load(open(WFILE))
    lines = [l.strip() for l in open(a.log) if l.strip() and "|" in l]
    c = build_ctx(lines, a.round, "dauntless", a.enemy, a.my_hp, a.en_hp)
    # look ahead: his next turn may be in round R+1 (he moves first) - threats use the worse of R and R+1
    c2 = build_ctx(lines, a.round + 1, "dauntless", a.enemy, a.my_hp, a.en_hp)
    for k in ("en_idg", "en_absorb", "en_lifesteal", "en_reflect"):
        c[k] = max(c[k], c2[k])
    c["en_clearprevent"] = c["en_clearprevent"] or c2["en_clearprevent"]
    c["i_first"] = a.first
    thr = threat_features(a.enemy, a.battle, a.round) if a.battle else [0.0] * 6
    x = features(c, th, a.my_max, a.en_max, thr, a.dist)
    _, h = hidden(net, x)
    state = load(a.battle) if a.battle else None
    loadout = state["loadout"] if state else LOADOUTS["pvp1"]
    ap = a.ap - (20 if c["me_stunned"] and a.ap == 100 else 0)
    bundles = legal(state, a.round, ap, c["en_immune"], set(cfg["immune_blocked"]), loadout, a.dist)
    cd_cost = cfg.get("cd_cost", 0.01)
    # per-opponent weight overrides from rules_config profiles nudge the rule's first bundle
    bonus = {}
    for rule in cfg["rules"]:
        if rule["id"] in prof.get("weights", {}):
            delta = (prof["weights"][rule["id"]] - rule["weight"]) / 100
            fi = FEATURES.index(RULE_FEATURE.get(rule["when"], rule["when"]))
            if x[fi]:
                bonus[tuple(sorted(rule["bundles"][0]))] = delta
    ranked = sorted(((bundle_value(net, x, h, b, cd_cost) + bonus.get(tuple(sorted(s for s in b if s != "step")), 0), b)
                     for b in bundles), key=lambda t: -t[0])
    # hard rule: a flat pierce that kills beats any scored plan (Night's 631, Stormblade 707)
    if a.en_hp > 0:
        killers = [r for r in ranked if ("nights" in r[1] and a.en_hp <= 631) or ("stormblade" in r[1] and a.en_hp <= 707)]
        if killers:
            ranked = killers + [r for r in ranked if r not in killers]
            print("LETHAL: flat pierce kills")
        else:  # estimated burst kill (director 2026-11-10: "Why didnt you do lotus dance and basic attack to win?")
            est = sorted(((est_damage(r[1], c), r) for r in ranked), key=lambda t: -t[0])
            if est and est[0][0] >= a.en_hp * 1.1:
                ranked = [est[0][1]] + [r for r in ranked if r is not est[0][1]]
                print(f"LETHAL: est {est[0][0]:.0f} >= {a.en_hp:.0f}")
    on = [k for k, v in zip(FEATURES, x) if v and k not in ("bias", "my_hp_frac", "en_hp_frac", "en_idg")]
    print(f"r{a.round} {ap} AP dist {a.dist}  on: {', '.join(on) or 'none'}  (en_idg {c['en_idg']:+.0%})")
    if not ranked:
        print("FIRE: defstance (no legal bundle)")
        return
    best = ranked[0]
    backup = next((r for r in ranked[1:] if not (set(r[1]) & set(best[1])) - {"step"}), ranked[1] if len(ranked) > 1 else None)
    print(f"FIRE:   {' > '.join(ordered(best[1]))}   ({best[0]:.2f})")
    if backup:
        print(f"BACKUP: {' > '.join(ordered(backup[1]))}   ({backup[0]:.2f})")
    for v, b in ranked[2:2 + max(0, a.top - 2)]:
        print(f"  also: {' > '.join(ordered(b))}   ({v:.2f})")
    if a.battle:
        p = f"/tmp/policy_{a.battle}.json"
        d = json.load(open(p)) if os.path.exists(p) else {"enemy": a.enemy, "rounds": {}}
        d["rounds"].setdefault(str(a.round), {})["x"] = x
        json.dump(d, open(p, "w"))


def reward(b, rnd, acts, dealt, taken):
    p = f"/tmp/policy_{b}.json"
    d = json.load(open(p))
    d["rounds"].setdefault(str(rnd), {}).update({"acts": acts.split(","), "r": (float(dealt) - float(taken)) / 1000})
    json.dump(d, open(p, "w"))
    print(f"r{rnd}: {acts} reward {(float(dealt) - float(taken)) / 1000:+.2f}")


def result(b, outcome):
    p = f"/tmp/policy_{b}.json"
    d = json.load(open(p))
    d["result"] = outcome
    json.dump(d, open(p, "w"))
    print(f"{b}: {outcome}")


def samples_from(d, battle):
    rounds = sorted(((int(k), v) for k, v in d["rounds"].items() if "x" in v and "acts" in v), key=lambda t: t[0])
    term = {"win": TERMINAL, "loss": -TERMINAL}.get(d.get("result"), 0.0)
    out = []
    for i, (rnd, s) in enumerate(rounds):
        G, g = 0.0, 1.0
        for _, s2 in rounds[i:]:
            G += g * s2["r"]
            g *= GAMMA
        G += g * term
        out.append({"battle": battle, "enemy": d["enemy"], "round": rnd, "x": s["x"], "acts": s["acts"],
                    "r": s["r"], "G": G, "w": d.get("w", 1.0)})
    return out


ANCHOR = 0.05  # L2 pull of the linear weights back toward the hand-tuned seed (small data must not erase doctrine)


def step(net, s, lr, seed_w=None):
    x, acts = s["x"], [a for a in s["acts"] if a in net["W"]]
    lr = lr * s.get("w", 1.0)  # sample weight (AFK fights 0.3)
    if not acts:
        return 0.0
    z, h = hidden(net, x)
    pred = sum(q(net, x, h, a) for a in acts) + sum(net["P"].get(pkey(a, c), 0.0)
                                                     for a, c in itertools.combinations(acts, 2))
    err = max(-3.0, min(3.0, s["G"] - pred))  # clip
    n = len(acts)
    gh = [0.0] * H
    for a in acts:
        for j in range(H):
            gh[j] += net["V"][a][j]
        w0 = seed_w[a] if seed_w else net["W"][a]
        net["W"][a] = [w + lr * (err / n * v - ANCHOR * (w - s0)) for w, v, s0 in zip(net["W"][a], x, w0)]
        net["V"][a] = [w + lr * err / n * hj for w, hj in zip(net["V"][a], h)]
    for j in range(H):
        if z[j] > 0:
            net["W1"][j] = [w + lr * err * gh[j] / n * v for w, v in zip(net["W1"][j], x)]
            net["b1"][j] += lr * err * gh[j] / n
    for a, c in itertools.combinations(acts, 2):
        k = pkey(a, c)
        net["P"][k] = net["P"].get(k, 0.0) + lr * err / n
    return err * err


def seed_weights():
    cur = open(WFILE).read() if os.path.exists(WFILE) else None
    w = seed(quiet=True)["W"]
    if cur is not None:
        open(WFILE, "w").write(cur)
    return w


def train(b, lr):
    sw = seed_weights()
    net = json.load(open(WFILE))
    d = json.load(open(f"/tmp/policy_{b}.json"))
    ss = samples_from(d, b)
    loss = sum(step(net, s, lr, sw) for s in ss)
    json.dump(net, open(WFILE, "w"))
    with open(TRAIN_LOG, "a") as f:
        for s in ss:
            f.write(json.dumps(s) + "\n")
    print(f"trained on {len(ss)} rounds of {b} ({d.get('result', 'no result')}), loss {loss / max(1, len(ss)):.3f}")


def retrain(epochs, lr):
    net = seed(quiet=True)
    sw = json.loads(json.dumps(net["W"]))
    ss = [json.loads(l) for l in open(TRAIN_LOG)] if os.path.exists(TRAIN_LOG) else []
    rnd = random.Random(1)
    for e in range(epochs):
        rnd.shuffle(ss)
        loss = sum(step(net, s, lr, sw) for s in ss)
    json.dump(net, open(WFILE, "w"))
    print(f"retrained from hand seed on {len(ss)} samples x {epochs} epochs, final loss "
          f"{(loss / max(1, len(ss))) if ss else 0:.3f}")


def show(action):
    net = json.load(open(WFILE))
    for a in ([action] if action else sorted(net["W"])):
        top = sorted(zip(FEATURES, net["W"][a]), key=lambda t: -abs(t[1]))[:5]
        vn = math.sqrt(sum(v * v for v in net["V"][a]))
        print(f"{a:11s} " + "  ".join(f"{k}:{v:+.2f}" for k, v in top if v) + f"   |hidden| {vn:.2f}")
    if not action:
        print("pairs: " + ", ".join(f"{k}:{v:+.2f}" for k, v in sorted(net["P"].items(), key=lambda t: t[1])))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("init"); s.add_argument("--keep", action="store_true")
    s = sp.add_parser("act"); s.add_argument("log"); s.add_argument("round", type=int)
    s.add_argument("--enemy", required=True); s.add_argument("--battle", default="")
    s.add_argument("--dist", type=int, default=3)
    s.add_argument("--first", action="store_true", help="I act first this round (delayed defence won't cover his turn)")
    s.add_argument("--ap", type=int, default=100); s.add_argument("--my-hp", type=float, default=0)
    s.add_argument("--en-hp", type=float, default=0); s.add_argument("--my-max", type=float, default=5050)
    s.add_argument("--en-max", type=float, default=5000); s.add_argument("--top", type=int, default=3)
    s = sp.add_parser("reward"); [s.add_argument(k) for k in ("battle", "round", "acts", "dealt", "taken")]
    s = sp.add_parser("result"); s.add_argument("battle"); s.add_argument("outcome", choices=["win", "loss"])
    s = sp.add_parser("train"); s.add_argument("battle"); s.add_argument("--lr", type=float, default=0.003)
    s = sp.add_parser("retrain"); s.add_argument("--epochs", type=int, default=10)
    s.add_argument("--lr", type=float, default=0.003)
    s = sp.add_parser("show"); s.add_argument("action", nargs="?")
    a = p.parse_args()
    {"init": lambda: seed(a.keep), "act": lambda: act(a),
     "reward": lambda: reward(a.battle, a.round, a.acts, a.dealt, a.taken),
     "result": lambda: result(a.battle, a.outcome), "train": lambda: train(a.battle, a.lr),
     "retrain": lambda: retrain(a.epochs, a.lr), "show": lambda: show(a.action)}[a.cmd]()
