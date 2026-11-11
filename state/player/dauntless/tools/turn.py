#!/usr/bin/env python3
"""One-call PvP turn planner (director, 2026-11-10: "I dont want you spending 30+ seconds a turn trying to sort out your
next move, you should have a planner that does that and you pick the highest value moves with a forecast for next
rounds for both you and the opponent").

Each turn: save the two connector responses into ONE file (two lines), run this, fire the printed actions in order.
  line 1: combat.getBattle {battleId} with select
          ["battle.version","battle.round","battle.activeUserId","battle.usersState.*.userId",
           "battle.usersState.*.username","battle.usersState.*.curHealth","battle.usersState.*.maxHealth",
           "battle.usersState.*.longitude","battle.usersState.*.latitude","battle.usersState.*.actionPoints"]
  line 2: combat.getBattleEntries {battleId, limit: 200} with select
          ["*.battleRound","*.userId","*.actionId","*.appliedEffects.*.txt"]
Usage: turn.py FILE --battle ID [--enemy NAME] [--loadout pvp1|pvp2] [--top 3]

What it does (no live calls, no guessing):
  - positions, HP and AP by USERNAME (never by array order), hex distance, who acts first this round, my stun;
  - my cooldowns from my own logged actions (engine actions.ts: usable when round - lastUsedRound >= cooldown) plus
    shared tag locks, written to the cd_plan state so policy.legal only offers usable bundles;
  - live/upcoming tags on both sides (cast in round N = live N+1 .. N+k), enemy resources spent (Clear, Cleanse, Smoke,
    Kim's, pierce) and his average damage per turn so far;
  - every legal bundle simulated with shotplan's engine model: my turn + his reply (Luka profile when known, otherwise a
    generic hitter calibrated from this fight), then my best follow-up; hard-rule penalties on top;
  - prints the top bundles in firing order with exact target hexes, plus the 2-round HP forecast for both sides.
"""
import argparse
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cd_plan  # noqa: E402
import shotplan  # noqa: E402
from ingest import IDS, ME  # noqa: E402
from policy import legal  # noqa: E402

ME_NAME = "dauntless"
GRID_W, GRID_H = 13, 9

# firing order inside a turn: reposition, strip/lock, defensive locks, buffs, damage, fillers, kite step last
ORDER = ["cleanse", "phantom", "replace", "step", "clear", "sealnull", "kims", "smoke", "ember", "overflow", "thunders",
         "parry", "eclipse", "pill", "jewel", "subaku", "severed", "disaster", "shield", "panacea", "lotus", "danse",
         "shrapnel", "fury", "rebirth", "resonance", "leech", "yuki", "stormblade", "nights", "aetherion", "kunai",
         "basic", "basicheal", "defstance", "offstance", "stepback"]
SELF_T = {"overflow", "thunders", "parry", "eclipse", "shield", "pill", "jewel", "panacea", "kims", "defstance",
          "offstance", "basicheal", "cleanse"}
BUFFS = {"overflow", "thunders", "parry", "eclipse", "pill", "jewel", "ember", "phantom"}
ACTION_ID = {v: k for k, v in IDS.items()}
ACTION_ID.update({"kunai": "yVNeLzxHSFkNpTPnlm7yQ", "basicheal": "basicHeal", "step": "move", "stepback": "move"})


# ---------------------------------------------------------------- hex helpers (odd-q, same as hx.py)
def cube(c, r):
    x = c
    z = r - (c - (c & 1)) // 2
    return x, -x - z, z


def dist(a, b):
    a, b = cube(*a), cube(*b)
    return max(abs(a[i] - b[i]) for i in range(3))


def hexes():
    return [(x, y) for x in range(GRID_W) for y in range(GRID_H)]


def neighbours(p):
    return [h for h in hexes() if dist(h, p) == 1]


# ---------------------------------------------------------------- input
def load_input(path):
    lines = [l for l in open(path).read().splitlines() if l.strip()]
    battle = json.loads(lines[0])
    ents = json.loads(lines[1]) if len(lines) > 1 else {}
    us = {k.split(".")[-1]: v for k, v in battle.items() if k.startswith("battle.usersState")}
    people = []
    for i, uid in enumerate(us["userId"]):
        people.append({k: us[k][i] for k in us})
    me = next(p for p in people if p["userId"] == ME)
    others = [p for p in people if p["userId"] != ME and p["curHealth"] > 0]
    rows = []
    if ents:
        effs = ents.get("*.appliedEffects.*.txt", [])
        rows = list(zip(ents["*.battleRound"], ents["*.userId"], ents["*.actionId"], effs))[::-1]  # oldest first
    return battle, me, others, rows


def my_history(rows):
    used = []
    for r, u, a, _ in rows:
        if u == ME and a in IDS:
            n = IDS[a]
            if n in ("step",):
                continue
            used.append([r, n])
    return used


def enemy_resources(rows, en_id, rnd):
    spent = {}
    pierce_last = None
    turns, dmg = 0, 0.0
    by_round = {}
    for r, u, a, t in rows:
        if u != en_id:
            continue
        txt = " ".join(t or [])
        if a == "clear":
            spent["clear"] = r
        elif a == "cleanse":
            spent["cleanse"] = r
        if "Elite Smoke" in txt or ("damage given [all damage] is decreased by up to 70%" in txt and ME_NAME in txt):
            spent["smoke"] = r
        if "cannot be cleared" in txt:
            spent["kims"] = r
        if "pierced" in txt or "shield was pierced" in txt:
            pierce_last = r
        for m in re.finditer(rf"{ME_NAME} takes ([\d.]+) (?:damage|afterburn damage|wound damage)", txt):
            by_round[r] = by_round.get(r, 0) + float(m.group(1))
    if by_round:
        turns = len(by_round)
        dmg = sum(by_round.values()) / turns
    return spent, pierce_last, dmg


# ---------------------------------------------------------------- planning
def generic_enemy(avg):
    base = max(500.0, avg or 900.0) / 2  # two hits per turn
    return {"hit": (base, []), "hit2": (base, []), "basic": (150, [])}


def place_phantom(me_pos, en_pos, need, occupied):
    """Phantom/Replacement landing hex: within 5 of me, at distance == need from him if possible, else closest."""
    best = None
    for h in hexes():
        if h in occupied or dist(h, me_pos) > 5 or h == en_pos or h == me_pos:
            continue
        d = dist(h, en_pos)
        key = (abs(d - need) + (0 if d <= need else 10), dist(h, me_pos))
        if best is None or key < best[0]:
            best = (key, h)
    return best[1] if best else me_pos


def step_toward(p, goal, occupied, away=False):
    cands = [h for h in neighbours(p) if h not in occupied]
    if not cands:
        return p
    return (max if away else min)(cands, key=lambda h: (dist(h, goal), h))


def resolve_targets(bundle, me_pos, en_pos, occupied):
    """Turn a bundle into ordered (action, actionId, (x, y)) steps with real hexes; moves first, kite step last."""
    seq = sorted(bundle, key=lambda a: ORDER.index(a) if a in ORDER else 50)
    ranged = [cd_plan.RANGE.get(a, 0) for a in seq if cd_plan.RANGE.get(a, 0)]
    need = min(ranged) if ranged else 4
    pos = me_pos
    out = []
    for a in seq:
        if a in ("phantom", "replace"):
            pos = place_phantom(pos, en_pos, need, occupied)
            tgt = pos
        elif a == "step":
            pos = step_toward(pos, en_pos, occupied)
            tgt = pos
        elif a == "stepback":
            pos = step_toward(pos, en_pos, occupied, away=True)
            tgt = pos
        elif a in SELF_T:
            tgt = pos
        else:
            tgt = en_pos
        out.append((a, ACTION_ID.get(a, a), tgt))
    return out, pos


def penalties(bundle, ctx):
    p, why = 0.0, []
    if "shield" in bundle and ctx["pierce_ready"]:
        p -= 800; why.append("shield into his ready pierce")
    if ctx["clear_held"]:
        nb = len([a for a in bundle if a in BUFFS and a != "phantom"])
        if nb >= 2 and "kims" not in bundle:
            p -= 250 * nb; why.append("stacking buffs while he still holds Clear")
    steps = bundle.count("step")
    if steps > 1:
        p -= 60 * (steps - 1); why.append(f"{steps} basic steps (use Phantom/Replacement)")
    if "smoke" in bundle and not ctx["me_immune_now"] and ctx["my_next_burst"]:
        p -= 150; why.append("smoke also cuts my next-round damage")
    # pierce is the answer to Smoke / shields / DR stacks; spending it early puts it on cooldown + the 3-round pierce lock
    # (director 2026-11-11: "Putting your pierce on GCD while the enemy hasn't used a smoke or shield yet is kind of risky")
    if any(x in bundle for x in ("nights", "stormblade")) and not ctx["pierce_window"]:
        p -= 450; why.append("pierce spent with no smoke/shield/DR to beat (save it)")
    if ctx["afk"]:
        wasted = [x for x in bundle if x in ("smoke", "panacea", "shield", "defstance", "kims", "sealnull", "parry")]
        if wasted:
            p -= 300 * len(wasted); why.append(f"enemy AFK: no defence needed ({'+'.join(wasted)})")
    if ctx["tick"] >= ctx["my_hp"] - 50 and "cleanse" not in bundle:
        p -= 6000; why.append(f"wound/drain tick {ctx['tick']:.0f} kills me: Cleanse FIRST")
    if "cleanse" in bundle and not ctx["me_debuffed"]:
        p -= 600; why.append("cleanse with nothing to remove")
    if "clear" in bundle and not ctx["en_buffed"]:
        p -= 600; why.append("clear with nothing to strip")
    return p, why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--battle", required=True)
    ap.add_argument("--enemy"); ap.add_argument("--loadout", default="pvp1"); ap.add_argument("--top", type=int, default=3)
    a = ap.parse_args()
    battle, me, others, rows = load_input(a.file)
    if not others:
        print("no living enemy"); return
    en = others[0] if not a.enemy else next((p for p in others if p["username"].lower() == a.enemy.lower()), others[0])
    R = battle["battle.round"]
    my_turn = battle["battle.activeUserId"] == ME
    en_acted = any(r == R and u == en["userId"] for r, u, _, _ in rows)
    me_pos, en_pos = (me["longitude"], me["latitude"]), (en["longitude"], en["latitude"])
    d0 = dist(me_pos, en_pos)
    occupied = {(p["longitude"], p["latitude"]) for p in others}

    # cooldown state from my own log
    st = {"loadout": list(cd_plan.LOADOUTS[a.loadout]) + ["basicheal"], "used": my_history(rows)}
    cd_plan.ACTIONS.setdefault("basicheal", (60, 5, None, "heal 600 instant"))
    shotplan.MINE.setdefault("basicheal", (0, [("me", "heal", 600, 0, True)]))
    cd_plan.save(a.battle, st)

    lines = [f"{r}|{t.strip()}" for r, u, _, ts in rows for t in (ts or [])]
    me0, en0 = shotplan.rebuild(lines, ME_NAME, en["username"], me["curHealth"], en["curHealth"])
    stunned = any("dauntless is stunned" in l and int(l.split("|")[0]) + 2 >= R and int(l.split("|")[0]) < R
                  for l in lines) or bool(me0.live("stun", R))
    ap_now = min(int(me["actionPoints"]) if my_turn else 100, 80 if stunned else 100)
    spent, pierce_last, avg = enemy_resources(rows, en["userId"], R)
    known = en["username"].lower() in shotplan.ENEMY
    ekit = shotplan.ENEMY.get(en["username"].lower()) or generic_enemy(avg)

    def tags(side, r):
        return sorted({f"{t[0]}{'' if t[0] in ('stun',) else f' {t[1]:g}'} (to R{t[3]})" for t in side.tags
                       if t[2] <= r <= t[3]})

    ctx = {
        "pierce_ready": pierce_last is None or R - pierce_last >= 3,
        "clear_held": "clear" not in spent,
        "me_immune_now": bool(me0.live("debuffimmune", R)),
        "me_debuffed": any(t[2] <= R + 1 and t[3] >= R and (t[0] in ("taken", "wound", "drain", "recoil_self")
                           or (t[0] == "given" and t[1] < 0)) for t in me0.tags),
        "en_buffed": any(t[3] >= R and shotplan.positive(t) for t in en0.tags),
        "my_next_burst": True,
        "my_hp": me["curHealth"],
        "afk": (lambda t: len(t) >= 1 and sum(1 for a in t if a == "wait") * 2 >= len(t))(
            [a for r, u, a, _ in rows if u == en["userId"] and (a == "wait" or a not in ("move",))]
            and [a for r, u, a, _ in rows if u == en["userId"]]),
        "pierce_window": bool(me0.mult("given", R) < 0.6 or en0.live("shield", R) or en0.total("dr", R) >= 0.3
                              or en0.total("absorb", R) >= 0.3 or en["curHealth"] <= 800),
        "tick": me0.total("wound", R) + me0.total("drain", R),
    }

    print(f"R{R} v{battle['battle.version']} | {'MY TURN' if my_turn else 'his turn'} | "
          f"{'he acted first this round' if en_acted else 'I act first this round'}")
    print(f"me {ME_NAME} {me['curHealth']:.0f} HP @ {me_pos}  AP {ap_now}{' (STUNNED -20)' if stunned else ''}")
    print(f"him {en['username']} {en['curHealth']:.0f} HP @ {en_pos}  dist {d0}  avg dmg/turn {avg:.0f}")
    print(f"my tags now: {', '.join(tags(me0, R)) or '-'} | next: {', '.join(tags(me0, R + 1)) or '-'}")
    print(f"his tags now: {', '.join(tags(en0, R)) or '-'} | next: {', '.join(tags(en0, R + 1)) or '-'}")
    print(f"enemy {'AFK (timing out)' if ctx['afk'] else 'active'}; his spent: {spent or '-'}; pierce {'READY' if ctx['pierce_ready'] else f'used R{pierce_last}'}; "
          f"Clear {'HELD' if ctx['clear_held'] else 'spent'}")
    waiting = sorted((cd_plan.ready_round(st, n), n) for n in st["loadout"] if n in cd_plan.ACTIONS
                     and cd_plan.ready_round(st, n) > R)
    print("on cooldown: " + ", ".join(f"{n}->R{r}" for r, n in waiting))
    if not my_turn:
        print("not my turn: poll again in <=15 s")
        return

    bundles = legal(st, R, ap_now, bool(en0.live("debuffimmune", R)),
                    {"ember", "severed", "disaster", "lotus", "danse", "sealnull", "yuki"}, st["loadout"], d0)
    # kite-back variants: one spare step moves me back out after ranged actions
    extra = []
    for b in bundles:
        cost = sum(cd_plan.ACTIONS[x][0] for x in b if x in cd_plan.ACTIONS)
        if "step" in b and ap_now - cost >= 10 and "basic" not in b:
            extra.append(tuple(b) + ("stepback",))
    cd_plan.ACTIONS.setdefault("stepback", (10, 0, None, "kite step"))
    shotplan.MINE.setdefault("stepback", (0, []))
    bundles = list(bundles) + extra
    his_now = shotplan.enemy_options(en["username"].lower(), a.battle, R) if known and en["username"].lower() in shotplan.PROFILES else [["hit", "hit2"]]
    his_next = shotplan.enemy_options(en["username"].lower(), a.battle, R + 1) if known and en["username"].lower() in shotplan.PROFILES else [["hit", "hit2"]]
    results = []
    for b in bundles:
        worst = None
        for h in (his_next if en_acted else his_now):
            m, e = copy.deepcopy(me0), copy.deepcopy(en0)
            log = []
            if "cleanse" in b:  # Cleanse fired first removes wound/drain before they tick (Korin 2026-11-11 R5)
                m.tags = [x for x in m.tags if shotplan.positive(x)]
            d, t = shotplan.run_turn(m, e, list(b), shotplan.MINE, R, True)
            m.hp = min(m.hp, me.get("maxHealth", 5050))
            log.append(("me", R, b, d, t, m.hp, e.hp))
            hr = R + 1 if en_acted else R
            if e.hp > 0:
                d2, t2 = shotplan.run_turn(e, m, h, ekit, hr, False)
                log.append(("him", hr, h, d2, t2, m.hp, e.hp))
            m.hp = min(m.hp, me.get("maxHealth", 5050)); e.hp = min(e.hp, en.get("maxHealth", 5050))
            sc = shotplan.score(m, e, me["curHealth"], en["curHealth"])
            # setup credit: my +given live next round, his +taken live next round
            sc += 300 * (m.mult("given", R + 1) - 1) + 300 * (e.mult("taken", R + 1) - 1)
            pen, why = penalties(b, ctx)
            if e.hp <= 0:  # a kill outweighs every saving rule
                pen = max(pen, 0); why = []
            sc += pen
            if worst is None or sc < worst[0]:
                worst = (sc, log, why)
        results.append((worst[0], b, worst[1], worst[2]))
    results.sort(key=lambda x: -x[0])
    print(f"{len(bundles)} legal bundles. TOP {a.top}:")
    for i, (sc, b, log, why) in enumerate(results[:a.top], 1):
        seq, end = resolve_targets(b, me_pos, en_pos, occupied)
        fire = " -> ".join(f"{x}@{t[0]},{t[1]}" for x, _, t in seq)
        fc = " | ".join(f"{w} R{r} {'+'.join(x)}: me {mh:.0f} / him {eh:.0f}" for w, r, x, _, _, mh, eh in log)
        print(f"{i}. {sc:+6.0f}  {fire}  (ends @{end}, dist {dist(end, en_pos)})")
        print(f"     forecast: {fc}" + (f"  [penalty: {'; '.join(why)}]" if why else ""))
    best = results[0][1]
    seq, _ = resolve_targets(best, me_pos, en_pos, occupied)
    print("FIRE:", json.dumps([{"actionId": aid, "longitude": t[0], "latitude": t[1], "name": n} for n, aid, t in seq]))


if __name__ == "__main__":
    main()
