#!/usr/bin/env python3
"""His clock (director 2026-11-11: "You cant just understand your own turns to kill either, you need to read your
opponents clock. Understanding who is doing what and where things are going is important").

From his real kit (opp_profile / opponent_kit: equipped jutsu read at battle start, plus every item or jutsu he has
used in this fight) and his logged actions:
  - each of his actions compiled from its catalog record into the planner's spec format (damage power x 13.3 HP per
    point, pierce x 12.6, the same scale my calibrated kit sits on; tags with their real powers, levels and rounds);
  - what he can fire on his next turn and the turn after (own cooldowns + shared tag locks, as for me);
  - his best lines on his next turn, scored from his side (damage now + what his setup adds to his next turn), which
    become his reply options with weights, instead of a generic stand-in.
Offline, a few milliseconds. Usage: clock.py TURN_FILE [--enemy NAME]
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cd_plan  # noqa: E402
import engine_bridge as EB  # noqa: E402

K_DMG, K_PIERCE = 13.3, 12.6      # HP per power point (my calibrated kit / record powers at level 25: 11.8-13.7)
BASICS = {"clear": (60, 10, ["clear"]), "cleanse": (60, 10, ["cleanse"]), "basicAttack": (20, 1, []),
          "defensiveStance": (20, 1, []), "offensiveStance": (20, 1, [])}
SKIP = {"visual", "move", "consume", "injectjutsus", "increasepoolcost", "summon", "seal"}


def _pw(e, level):
    return (e.get("power") or 0) + (e.get("powerPerLevel") or 0) * level


def compile_record(rec, level=25):
    """Catalog record -> (ap, cooldown, lock tags, spec) with spec in shotplan form, perspective: "en" = him (the
    caster), "me" = me (his target)."""
    base, pierce, tags = 0.0, False, []
    self_cast = rec.get("target") in ("SELF",)
    for e in rec.get("effects", []):
        t = e.get("type")
        if t in SKIP:
            continue
        p = _pw(e, level)
        on_self = e.get("target") == "SELF" or (e.get("target") == "INHERIT" and self_cast)
        who = "en" if on_self else "me"
        n = int(e.get("rounds") or 0)
        pct = p / 100.0
        if t == "damage":
            base += p * K_DMG
        elif t == "pierce":
            base += p * K_PIERCE; pierce = True
        elif t == "increasedamagegiven":
            tags.append((who, "given", pct, n))
        elif t == "decreasedamagegiven":
            tags.append((who, "given", -pct, n))
        elif t == "increasedamagetaken":
            tags.append((who, "taken", pct, n))
        elif t == "decreasedamagetaken":
            tags.append((who, "dr", pct, n))
        elif t == "afterburn":
            # on a target: it takes that share again on every hit (= +taken); on himself: his hits carry it (= +given)
            tags.append((who, "taken" if who == "me" else "given", pct, n))
        elif t in ("absorb", "lifesteal", "reflect", "parry"):
            tags.append((who, t, pct, n))
        elif t == "leech":
            tags.append((who, "lifesteal", pct, n))
        elif t == "recoil":
            tags.append((who, "recoil_self", pct, n))
        elif t == "wound":
            tags.append((who, "wound", pct * max(base, 400.0), n))
        elif t == "drain":
            tags.append((who, "drain", p, n))
        elif t == "shield":
            tags.append((who, "shield", p, max(n, 1), True))
        elif t == "stun":
            tags.append(("me", "stun", 20, max(n, 1), True))
        elif t == "clearprevent":
            tags.append((who, "clearimmune", 1, n))
        elif t == "debuffprevent":
            tags.append((who, "debuffimmune", 1, n))
        elif t == "buffprevent":
            tags.append(("me", "buffblock", 1, n))
        elif t == "clear":
            tags.append(("me", "clear", 1, 0, True))
        elif t == "cleanse":
            tags.append(("en", "cleanse", 1, 0, True))
        elif t == "copy":
            tags.append(("en", "copy", pct, max(n, 1)))
        elif t == "heal":
            tags.append(("en", "heal", p if e.get("calculation") == "static" else pct * 5050, 0, True))
    locks = {e.get("type") for e in rec.get("effects", [])} & set(cd_plan.LOCKS)
    spec = (base, tags, "pierce") if pierce else (base, tags)
    return int(rec.get("actionCostPerc") or 60), int(rec.get("cooldown") or 0), locks, spec


def his_actions(en_id, rows):
    """{action id: (name, ap, cooldown, locks, spec)} for his saved kit + anything he used; None without a kit."""
    kit = EB.opponent_kit(en_id)
    if not kit:
        return None
    recs = EB._records()
    ids = list(kit.get("jutsu", [])) + [a for r, u, a, _ in rows if u == en_id and a in recs]
    return acts_from_ids(ids, kit.get("jutsuLevels", {}))


def acts_from_ids(ids, lv=None):
    """{action id: (name, ap, cooldown, locks, spec)} for these catalog ids plus the basics everyone has."""
    recs = EB._records()
    lv = lv or {}
    out = {}
    for a in dict.fromkeys(ids):
        rec = recs.get(a, {}).get("record")
        if rec:
            out[a] = (rec.get("name", a),) + compile_record(rec, lv.get(a, 25))
    for a, (ap, cd, tags) in BASICS.items():
        spec = (150.0, []) if a == "basicAttack" else (0.0, [("me", "clear", 1, 0, True)]) if a == "clear" else \
            (0.0, [("en", "cleanse", 1, 0, True)]) if a == "cleanse" else \
            (0.0, [("en", "dr", 0.15, 1)]) if a == "defensiveStance" else (0.0, [("en", "given", 0.15, 1)])
        out[a] = (a, ap, cd, set(tags) & set(cd_plan.LOCKS), spec)
    return out


def ready_at(acts, en_id, rows, rnd):
    """His actions usable in round rnd: own cooldown since last use, shared tag locks from his other actions."""
    last = {}
    for r, u, a, _ in rows:
        if u == en_id and a in acts:
            last[a] = max(last.get(a, -99), r)
    out = []
    for a, (name, ap, cd, locks, spec) in acts.items():
        if a in last and rnd - last[a] < cd:
            continue
        if any(rnd - lr < cd_plan.LOCKS[t] for b, lr in last.items() if b != a for t in locks & acts[b][3]):
            continue
        out.append(a)
    return out


def bundles(acts, ready, ap=100):
    ready = sorted(ready, key=lambda a: -acts[a][1])
    out = []

    def rec(i, cost, chosen, locks):
        if chosen and cost >= ap - 20:
            out.append(tuple(chosen))
        for j in range(i, len(ready)):
            a = ready[j]
            c = acts[a][1]
            if cost + c <= ap and not (acts[a][3] & locks):
                rec(j + 1, cost + c, chosen + [a], locks | acts[a][3])
    rec(0, 0, [], set())
    return out


def soft(scored, k=4, temp=250.0):
    top = sorted(scored, key=lambda x: -x[0])[:k]
    if not top:
        return []
    m = top[0][0]
    ws = [math.exp((s - m) / temp) for s, _ in top]
    tot = sum(ws)
    return [(w / tot, b) for w, (s, b) in zip(ws, top)]


if __name__ == "__main__":
    import turn
    battle, me, others, rows = turn.load_input(sys.argv[1])
    en = others[0]
    acts = his_actions(en["userId"], rows)
    if not acts:
        print("no saved kit for", en["username"]); sys.exit()
    R = battle["battle.round"]
    for rr in (R, R + 1):
        print(f"R{rr} ready:", ", ".join(f"{acts[a][0]}({acts[a][1]})" for a in ready_at(acts, en["userId"], rows, rr)))
