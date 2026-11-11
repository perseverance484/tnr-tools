#!/usr/bin/env python3
"""Solution library (director 2026-11-11: "a library of 'solutions' to things we encounter, like best scored moves or
answers to opponents. A way to quickly pull the correct response without having to mull it over").

1. Situation key: a position compressed to what decides the right answer: turn order (P1 = I act first this round,
   so his reply lands before my new tags; P2 = my tags cover his next turn), both HP bands, my next-hit and his
   next-hit multiplier bands, immunities, ground, his live buff count, his Clear / pierce, my key cooldowns, a copier
   in his kit.
2. Solver: for a position from a simulated fight, planner2's top candidates are each played out to the end several
   times (fightsim: planner2 for me with a fast shortlist, his bot sampling his lines), with common random seeds
   across candidates. The candidate with the best mean outcome is the solution. This is where turn order, damage
   windows and cadence get learned: a move is judged by how the fight actually goes after it, not by a one-turn score.
3. Library: solutions.json {key: {best, votes, value, alts, why}}; repeated keys vote.
4. Lookup at play time (planner2.rank): ~1 ms; a confident entry gets a bonus if that bundle is legal. The live
   simulation and guards still check it.

Usage:
  solutions.py build [--fights 6] [--rollouts 4] [--cands 6]   simulate fights, solve each of my turns, merge
  solutions.py show [N]                                        library summary
Offline only; run under `nice`.
"""
import argparse
import copy
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import planner2 as P2  # noqa: E402

LIB = os.path.join(HERE, "solutions.json")             # the library being built / tested in the simulator
LIVE = os.path.join(HERE, "solutions_live.json")       # promoted copy the live planner reads (after it wins in sims)
PIERCE = ("stormblade", "nights")


# ------------------------------------------------------------------ situation key
def band(x, edges):
    for i, e in enumerate(edges):
        if x < e:
            return i
    return len(edges)


def his_signature(ids, acts):
    """What his last turn did, as letters: H hit, P pierce, B buffed himself, R reduced his damage taken, I immune /
    clear-proof, D debuffed me, M smoked, S stunned me, C cleared me, Y copied my buffs, L lifesteal/absorb."""
    out = set()
    for a in ids or ():
        spec = (acts.get(a) or (None, 0, 0, set(), (0, [])))[4]
        if spec[0]:
            out.add("P" if spec[2:3] == ("pierce",) else "H")
        for t in spec[1]:
            who, kind, val = t[0], t[1], t[2]
            if kind == "clear":
                out.add("C")
            elif kind == "copy":
                out.add("Y")
            elif kind == "stun":
                out.add("S")
            elif who == "en" and kind == "given" and val > 0:
                out.add("B")
            elif who == "en" and kind == "dr":
                out.add("R")
            elif who == "en" and kind in ("debuffimmune", "clearimmune"):
                out.add("I")
            elif who == "en" and kind in ("absorb", "lifesteal", "reflect", "parry"):
                out.add("L")
            elif who == "me" and kind == "given" and val <= -0.5:
                out.add("M")
            elif who == "me" and (kind in ("taken", "wound", "drain", "recoil_self", "healcut") or (kind == "given" and val < 0)):
                out.add("D")
    return "".join(sorted(out)) or "0"


def situation_key(P, ctx, st, R, his_last=None, acts=None):
    import cd_plan
    m, e = P.me0, P.en0
    hr = P.hr
    ready = {n for n in st["loadout"] if n in cd_plan.ACTIONS and cd_plan.ready_round(st, n) <= R}
    mine = m.given(1) * e.g(P2.TAKEN, 1) * e.g(P2.DR, 1)
    his = e.given(hr) * m.g(P2.TAKEN, hr) * m.g(P2.DR, hr)
    parts = [
        "P2" if P.en_acted else "P1",
        f"h{band(m.hp / 5050, (0.2, 0.4, 0.6, 0.8))}{band(e.hp / 5050, (0.2, 0.4, 0.6, 0.8))}",
        f"x{band(mine, (0.6, 0.9, 1.2, 1.7))}{band(his, (0.6, 0.9, 1.2, 1.7))}",
        f"b{min(3, int(e.g(P2.NSTK, hr)))}",
        "".join(c for c, f in (("D", m.g(P2.DIMM, hr)), ("d", e.g(P2.DIMM, 0)), ("c", e.g(P2.CIMM, 0)),
                              ("g", m.g(P2.GGRD, 0) < 0.999), ("s", m.g(P2.STUN, 0)),
                              ("n", m.g(P2.TAKEN, 0) > 1.001 or m.g(P2.GDN, 0) < 0.999 or m.g(P2.WND, 0)))
                if f) or "-",
        ("C" if ctx.get("clear_held") else "") + ("P" if ctx.get("pierce_ready") else "")
        + ("Y" if ctx.get("copier") else ""),
        "".join(c for c, n in (("K", "clear"), ("L", "cleanse"), ("M", "smoke"), ("S", "sealnull"), ("I", "kims"))
                if n in ready) + ("X" if ready & set(PIERCE) else ""),
        "o" + his_signature(his_last, acts or {}),
    ]
    return "|".join(parts)


# ------------------------------------------------------------------ library
_LIB = {}


def load(path=None):
    path = path or LIB
    if path not in _LIB:
        try:
            _LIB[path] = json.load(open(path))
        except (OSError, ValueError):
            _LIB[path] = {}
    return _LIB[path]


def coarser(key):
    """The same position at lower resolution, for when the exact key was never solved: mid keeps turn order, HP,
    multipliers, his buff count, flags and his last turn; coarse keeps turn order, multipliers and his last turn."""
    p = key.split("|")
    if len(p) < 8:
        return []
    return ["M|" + "|".join([p[0], p[1], p[2], p[3], p[4], p[7]]), "C|" + "|".join([p[0], p[2], p[7]])]


def lookup(key, path=None):
    """(bundle tuple, confidence) or None: the exact key, else its mid / coarse versions at reduced confidence.
    Confidence = vote share x a votes factor x a margin factor, 0..1."""
    lib = load(path)
    for k, f in [(key, 1.0)] + list(zip(coarser(key), (0.8, 0.6))):
        if k in lib:
            r = _lookup_one(lib[k])
            if r:
                return r[0], r[1] * f
    return None


def _lookup_one(ent):
    if not ent:
        return None
    votes = ent["votes"]
    tot = sum(votes.values())
    best, n = max(votes.items(), key=lambda kv: kv[1])
    if os.environ.get("TNR_BOOK_FULL"):          # experiment: trust any solved answer fully
        return tuple(best.split("+")), 1.0
    conf = (n / tot) * min(1.0, tot / 3) * min(1.0, ent.get("margin", 0) / 0.15)
    return tuple(best.split("+")), conf


# ------------------------------------------------------------------ solver
def fast_policy(f, ap, keep=40):
    """Planner2 on a shortlist: every legal bundle pre-scored by its own turn (damage now, my next-turn potential),
    the best `keep` fully ranked. ~10x faster than the full rank, for rollouts."""
    P, st = f.planner(ap)
    bundles = P2.legal_bundles(st, f.R, ap, 1, f.loadout, P.me0, P.en0)
    if not bundles:
        return ()
    pre = []
    for b in bundles:
        m, e = P.me0.copy(), P.en0.copy()
        if "cleanse" in b:
            m.wipe(P2.NEGK)
        d, t = P2.run_turn(m, e, [P.my_kit[x] for x in b if x in P.my_kit], 0, 5050, 5050)
        pot, _ = P.my_potential(b, m, e)
        pre.append((d - t + 0.5 * pot, b))
    pre.sort(key=lambda x: -x[0])
    short = [b for _, b in pre[:keep]]
    return P2.rank(P, short, ap, P2.load_weights())[0][1]


def outcome(f):
    r = f.result()
    v = (r["me"] - r["him"]) / 5050
    if r["ko"]:
        v += 1.0 if r["win"] else -1.0
    return v


def rollout(snap, first, seed):
    f = copy.copy(snap)
    f.me, f.en = snap.me.copy(), snap.en.copy()
    f.rows, f.used, f.log = list(snap.rows), [list(x) for x in snap.used], list(snap.log)
    f.rng = random.Random(seed)
    forced = [tuple(first)]
    f.policy = lambda ap: forced.pop() if forced else fast_policy(f, ap)
    f.resume_from_my_turn()
    return outcome(f)


def solve(snap, cands=6, rollouts=4, also=None):
    ap = 100 - (20 if snap.me.g(P2.STUN, 0) else 0)
    P, st = snap.planner(ap)
    bundles = P2.legal_bundles(st, snap.R, ap, 1, snap.loadout, P.me0, P.en0)
    ranked = P2.rank(P, bundles, ap, P2.load_weights())
    top = [r[1] for r in ranked[:cands]]
    # the move actually played in a replay is always rated too, so every replay turn gets a verdict
    if also:
        legal = {tuple(sorted(b)): b for b in bundles}
        b = legal.get(tuple(sorted(also)))
        if b and b not in top:
            top.append(b)
    vals = []
    for b in top:
        v = sum(rollout(snap, b, 1000 + k) for k in range(rollouts)) / rollouts
        vals.append((v, b))
    vals.sort(key=lambda x: -x[0])
    key = situation_key(P, P.ctx, st, snap.R, snap.his_prev, snap.acts)
    return key, vals, top[0]


def merge(lib, key, vals, planner_pick):
    for k in [key] + coarser(key):
        _merge_one(lib, k, vals, planner_pick)


def _merge_one(lib, key, vals, planner_pick):
    best_v, best = vals[0]
    margin = best_v - (vals[1][0] if len(vals) > 1 else best_v - 1)
    ent = lib.setdefault(key, {"votes": {}, "value": {}, "margin": 0.0, "n": 0})
    name = "+".join(best)
    ent["votes"][name] = ent["votes"].get(name, 0) + 1
    ent["value"][name] = round(best_v, 3)
    ent["margin"] = round((ent["margin"] * ent["n"] + margin) / (ent["n"] + 1), 3)
    ent["n"] += 1
    ent["planner"] = "+".join(planner_pick)
    ent["alts"] = [["+".join(b), round(v, 3)] for v, b in vals[1:4]]


def replay_snapshots():
    """Every one of my turns in every logged fight, rebuilt as a simulator position against that opponent's model
    ("playing back replays and trying to find the right moves"). Yields (label, snapshot, the move actually played)."""
    import exam
    import fightsim
    import opponents as OM
    from ingest import IDS, ME
    models = OM.load()
    for bid, path, rows, meta in OM.load_logs():
        users = {u for _, u, _, _ in rows if (u or "").startswith("user_")}
        if ME not in users:
            continue
        en_id = next((u for u in users if u != ME), None)
        m = models.get(en_id)
        if not m or len(m.get("bundles", [])) < 2:
            continue
        name = m["names"][0]
        acts, habit = OM.acts_for(m), OM.habit_fn(m)
        d = json.load(open(path))
        hps = exam.hp_track(rows, ["dauntless", name])
        seen = set()
        for i, (r, u, a, ts) in enumerate(rows):
            if u != ME or r in seen:
                continue
            seen.add(r)
            played = sorted(IDS.get(x, x) for rr, uu, x, _ in rows[i:] if rr == r and uu == ME
                            and IDS.get(x, x) not in ("move", "wait", "step"))
            pre = rows[:i][::-1]
            hp = hps[i]
            b = {"battle.version": 1, "battle.round": r, "battle.activeUserId": ME,
                 "battle.usersState.*.userId": [en_id, ME], "battle.usersState.*.username": [name, "dauntless"],
                 "battle.usersState.*.curHealth": [hp[name], hp["dauntless"]],
                 "battle.usersState.*.maxHealth": [5050, 5050], "battle.usersState.*.longitude": [6, 7],
                 "battle.usersState.*.latitude": [4, 4], "battle.usersState.*.actionPoints": [0, 100]}
            e = {"*.battleRound": [x[0] for x in pre], "*.userId": [x[1] for x in pre],
                 "*.actionId": [x[2] for x in pre], "*.appliedEffects.*.txt": [x[3] for x in pre]}
            tmp = os.path.join(HERE, "..", "fights", "live", f"replay_{bid}_{r}.txt")
            open(tmp, "w").write(json.dumps(b) + "\n" + json.dumps(e) + "\n")
            try:
                P, info = P2.build(type("A", (), dict(file=tmp, enemy=name, loadout="pvp1")))
            finally:
                os.unlink(tmp)
            if P is None:
                continue
            f = fightsim.Fight(acts, info["prof"], not info["en_acted"], seed=hash((bid, r)) & 0xffff, habit=habit)
            f.me, f.en = P.me0.copy(), P.en0.copy()
            f.rows = [(rr, uu if uu == ME else fightsim.EN_ID, x, None) for rr, uu, x, _ in rows[:i]]
            f.used = [list(x) for x in info["st"]["used"]]
            f.R = r
            his = OM.turns_of(rows[:i], en_id)
            f.his_prev, f.his_turns = (his[-1][1] if his else None), len(his)
            yield f"{name} {bid[:6]} R{r}", f, played


def build(n_fights, rollouts, cands, replays=True, only=None):
    import fightsim
    opps = fightsim.opponents(styles=False)
    if only:
        opps = {k: v for k, v in opps.items() if any(x.lower() in k.lower() for x in only.split(","))}
    lib = load()
    t0 = time.time()
    solved = changed = 0
    blunders = []
    if replays:
        for label, s, played in replay_snapshots():
            key, vals, pick = solve(s, cands, rollouts, also=played)
            merge(lib, key, vals, pick)
            solved += 1
            best = "+".join(vals[0][1])
            pv = next((v for v, b in vals if sorted(b) == played), None)
            if pv is not None and vals[0][0] - pv > 0.25:
                blunders.append((label, "+".join(played), best, round(vals[0][0] - pv, 2)))
            print(f"[{time.time() - t0:5.0f}s] replay {label:28} played {'+'.join(played):28} -> solved {best:28} "
                  f"({vals[0][0]:+.2f}{'' if pv is None else f', played {pv:+.2f}'})", flush=True)
            json.dump(lib, open(LIB, "w"), indent=0, sort_keys=True)
        json.dump(blunders, open(os.path.join(HERE, "..", "fights", "blunders.json"), "w"), indent=1)
    names = list(opps)
    for i in range(n_fights):
        name = names[i % len(names)]
        acts, prof, habit = (tuple(opps[name]) + (None,))[:3]
        first = (i // len(names)) % 2 == 0
        f = fightsim.Fight(acts, prof, first, seed=500 + i, habit=habit)
        snaps = []
        f.on_my_turn = lambda fight: snaps.append(fight.snapshot())
        f.run()
        for s in snaps:
            key, vals, pick = solve(s, cands, rollouts)
            merge(lib, key, vals, pick)
            solved += 1
            changed += tuple(vals[0][1]) != tuple(pick)
            print(f"[{time.time() - t0:5.0f}s] {name[:14]:14} {'P1' if first else 'P2'} R{s.R} {key:42} "
                  f"planner {'+'.join(pick):28} -> solved {'+'.join(vals[0][1]):28} ({vals[0][0]:+.2f})", flush=True)
        json.dump(lib, open(LIB, "w"), indent=0, sort_keys=True)
    print(f"solved {solved} positions, {changed} changed from the planner's pick; library {len(lib)} keys")


REVIEW = os.path.join(HERE, "..", "fights", "loss_review.json")


def review_losses(rollouts=4, cands=6):
    """Every logged fight I lost, replayed turn by turn against that opponent's model (director 2026-11-11: "add every
    loss too. It should replay them and find win conditions"). Each of my turns is solved by playouts, the move I
    actually played included; a turn whose best line wins in the playouts while my move did not is a win condition.
    The earliest one is where the fight was lost. Results: fights/loss_review.json (new losses only on reruns);
    every solved turn also goes into the library."""
    import exam
    import opponents as OM
    from ingest import ME
    done = {}
    try:
        done = json.load(open(REVIEW))
    except (OSError, ValueError):
        pass
    lib = load()
    by_fight = {}
    for label, snap, played in replay_snapshots():
        bid = label.split()[-2]
        by_fight.setdefault(bid, []).append((label, snap, played))
    for bid, turns in by_fight.items():
        full = next((k for k in done if k.startswith(bid)), None)
        if full:
            continue
        logs = {b[:6]: (b, rows) for b, _, rows, _ in OM.load_logs()}
        b_full, rows = logs.get(bid, (bid, None))
        if rows is None:
            continue
        name = turns[0][0].rsplit(" ", 2)[0]
        hp = exam.hp_track(rows + [(0, "", "", [])], ["dauntless", name])[-1]
        if hp["dauntless"] > 1.0 and hp["dauntless"] >= hp[name]:
            done[b_full] = {"lost": False}
            continue                                         # a win: nothing to find
        out = []
        for label, snap, played in turns:
            key, vals, pick = solve(snap, cands, rollouts, also=played)
            merge(lib, key, vals, pick)
            pv = next((v for v, bb in vals if sorted(bb) == played), None)
            out.append({"turn": label, "played": "+".join(played), "played_value": None if pv is None else round(pv, 2),
                        "best": "+".join(vals[0][1]), "best_value": round(vals[0][0], 2),
                        "alts": [["+".join(bb), round(v, 2)] for v, bb in vals[1:3]]})
            print(f"{label:30} played {'+'.join(played):30} ({'?' if pv is None else f'{pv:+.2f}'}) "
                  f"best {'+'.join(vals[0][1]):30} ({vals[0][0]:+.2f})", flush=True)
        wc = next((t for t in out if t["best_value"] > 0 and (t["played_value"] is None or t["played_value"] <= 0)), None)
        done[b_full] = {"lost": True, "opponent": name, "turns": out, "win_condition": wc}
        print(f"== {name} {bid}: " + (f"win condition at {wc['turn']}: {wc['best']} instead of {wc['played']}"
                                       if wc else "no winning line found in the playouts"), flush=True)
        json.dump(done, open(REVIEW, "w"), indent=1)
        json.dump(lib, open(LIB, "w"), indent=0, sort_keys=True)
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "show", "losses"])
    ap.add_argument("n", nargs="?", type=int, default=20)
    ap.add_argument("--fights", type=int, default=6)
    ap.add_argument("--rollouts", type=int, default=4)
    ap.add_argument("--cands", type=int, default=6)
    ap.add_argument("--only", help="opponents to train against (substrings), e.g. luka,hikuro")
    ap.add_argument("--no-replays", action="store_true")
    a = ap.parse_args()
    if a.cmd == "losses":
        review_losses(a.rollouts, a.cands)
        return
    if a.cmd == "build":
        build(a.fights, a.rollouts, a.cands, replays=not a.no_replays, only=a.only)
    else:
        lib = load()
        for k, ent in sorted(lib.items(), key=lambda kv: -kv[1]["n"])[:a.n]:
            print(k, lookup(k), ent.get("planner"))


if __name__ == "__main__":
    main()
