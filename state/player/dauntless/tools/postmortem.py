#!/usr/bin/env python3
"""Why a real fight was lost, from the fight itself and the game's own combat code (director 2026-11-11: "try
against real enemies and actively scan logs to understand what caused a loss").

For each of my turns in the log the position is rebuilt exactly (engine replay of the log: every live effect, plus
this matchup's engine bases) and three things are measured:
  read     what the planner expected him to do next vs what he actually did (bundle, and its role: setup / payoff /
           defend / poke) -> where the opponent model was wrong
  numbers  the planner's damage for the bundle actually played vs the damage the log shows -> where the math was wrong
  choice   the bundle played vs the planner's top alternatives, each fired in the engine on that exact position and
           answered by his ACTUAL next turn (his logged actions replayed after mine) -> my HP minus his HP after the
           exchange. The gap to the best alternative is that turn's regret.
The turn with the largest regret is where the fight turned; a big miss on "read" there means the opponent model
caused it, a big miss on "numbers" means the simulator did, otherwise the choice itself was the mistake.

Writes fights/postmortems/<bid>.json and prints a short report.
Usage: postmortem.py <battleId prefix> [--alts 6]
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_bridge as EB  # noqa: E402
import engine_check as EC  # noqa: E402
import exam  # noqa: E402
import opponents as OM  # noqa: E402
import planner2 as P2  # noqa: E402
import turn  # noqa: E402
import validate  # noqa: E402
import value_model  # noqa: E402
from ingest import IDS, ME  # noqa: E402

OUT = os.path.join(HERE, "..", "fights", "postmortems")


def his_next_turn(rows, r_me, en_id):
    """His action ids in the turn that follows my turn of round r_me."""
    seen_me = False
    out, cur_r = [], None
    for r, u, a, ts in rows:
        if u == ME and r == r_me:
            seen_me = True
            continue
        if not seen_me:
            continue
        if u == en_id:
            if cur_r is None:
                cur_r = r
            if r != cur_r:
                break
            if a not in ("wait", "move"):
                out.append(a)
        elif out:
            break
    return out


def my_turn_at(rows, r_me):
    return [IDS.get(a, a) for r, u, a, ts in rows if u == ME and r == r_me and a not in ("wait", "move")]


def exchange(rows_pre, en, me, R, en_acted, cal, bundles, his_actual):
    """Engine: each bundle on this exact position, then his actual next turn replayed (as a scripted reply).
    Returns [(my HP, his HP)] or None per bundle."""
    me_pos, en_pos = (me["longitude"], me["latitude"]), (en["longitude"], en["latitude"])
    seqs = [turn.resolve_targets(tuple(b), me_pos, en_pos, set())[0] for b in bundles]
    req = EB._replay_request(rows_pre, ME, en["userId"], me, en, me_pos, en_pos, R, "next" if en_acted else "same", cal)
    req["mode"] = "eval"
    req["candidates"] = [[{"actionId": a, "x": t[0], "y": t[1]} for _, a, t in s] for s in seqs]
    req["scriptedReply"] = list(his_actual)
    req["replyCap"] = 1
    res = EB._run(req, 90) or {}
    out = []
    for r in res.get("results") or []:
        if not r.get("legal"):
            out.append(None)
            continue
        after = r.get("afterScripted") or r.get("afterMe")
        out.append((after["me"], after["him"], r["afterMe"]["him"]))
    return out


def review(bid_prefix, n_alts=6):
    cal = value_model.load_cal()
    value_model.calibrate_kit(cal)
    log = next(((b, rows) for b, p, rows, m in OM.load_logs() if b.startswith(bid_prefix)), None)
    if not log:
        sys.exit(f"no log for {bid_prefix}")
    bid, rows = log
    users = [u for u in dict.fromkeys(u for _, u, _, _ in rows) if (u or "").startswith("user_")]
    en_id = next(u for u in users if u != ME)
    os.environ["TNR_OM_EXCLUDE"] = bid          # his model without this fight: an honest read
    model = OM.load().get(en_id)
    acts = OM.acts_for(model) if model else {}
    out = {"fight": bid, "opp": OM.names_in(rows, en_id), "turns": []}
    try:
        live_hist = json.load(open(os.path.join(HERE, "..", "fights", "live_states", f"{bid}.json")))
    except (OSError, ValueError):
        live_hist = {}
    out["live_state_rounds"] = sorted(int(k) for k in live_hist)
    EC.EXACT = True
    for r, tp, name in EC.positions(rows):
        try:
            EC.exact_inputs(tp, name, cal)
            if str(r) in live_hist:            # the state the pilot read live at that turn beats the replay
                lines = open(tp).read().splitlines()
                bt = json.loads(lines[0])
                bt["battle.liveEffects"] = live_hist[str(r)]
                open(tp, "w").write(json.dumps(bt) + "\n" + lines[1] + "\n")
            P, info = P2.build(type("A", (), dict(file=tp, enemy=name, loadout="pvp1", battle="ECHK")))
            if P is None:
                continue
            battle, me, others, rows_pre = turn.load_input(tp)
            en = next(p for p in others if p["username"] == name)
            played = [x for x in my_turn_at(rows, r) if x in P.my_kit]
            his_actual = his_next_turn(rows, r, en_id)
            # read: his predicted reply to what I actually played
            m0, e0 = P.me0.copy(), P.en0.copy()
            if "cleanse" in played:
                m0.wipe(P2.NEGK)
            P2.run_turn(m0, e0, [P.my_kit[x] for x in played], 0, 5050, 5050)
            pred = P.replies(m0, e0)
            top = max(pred, key=lambda x: x[0]) if pred else (0, [])
            p_actual = sum(w for w, b in pred if set(b) == set(his_actual))
            role = lambda b: OM.role_of(tuple(b), acts) if acts else "?"
            # numbers: planner damage for the played bundle vs the log
            logged = validate.logged_dealt(rows, *_turn_span(rows, r), name)
            # choice: played vs the planner's alternatives, each answered by his actual next turn
            bundles = P2.legal_bundles(info["st"], info["R"], info["ap"], info["d0"], info["st"]["loadout"], P.me0, P.en0)
            ranked = P2.rank(P, bundles, info["ap"], P2.load_weights())
            if P2.LOOKAHEAD:
                ranked = P2.lookahead_rerank(P, info, ranked, P2.LA_BUDGET)
            pick = list(ranked[0][1])
            alts = [list(x[1]) for x in ranked[:n_alts] if sorted(x[1]) != sorted(played)]
            en_acted = info["en_acted"]
            ex = exchange(rows_pre, en, me, info["R"], en_acted, cal, [played] + alts, his_actual)
            score = [(None if v is None else round(v[0] - v[1])) for v in ex]
            eng_dealt = round(en["curHealth"] - ex[0][2]) if ex and ex[0] else None
            best_i = max((i for i, v in enumerate(score) if v is not None), key=lambda i: score[i], default=0)
            out["turns"].append({
                "round": r, "my_hp": round(me["curHealth"]), "his_hp": round(en["curHealth"]),
                "played": played, "his_next": [acts.get(a, (a,))[0] if acts else a for a in his_actual],
                "predicted": [acts.get(a, (a,))[0] if acts else a for a in top[1]], "p_his_actual": round(p_actual, 2),
                "role_pred": role(top[1]), "role_actual": role(his_actual),
                "dmg_planner": round(en["curHealth"] - e0.hp), "dmg_engine": eng_dealt, "dmg_logged": round(logged),
                "swing_played": score[0], "best_alt": ([played] + alts)[best_i], "swing_best": score[best_i],
                "regret": (score[best_i] - score[0]) if score[0] is not None and score[best_i] is not None else None,
                "pick": pick, "swing_pick": next((score[i] for i, bb in enumerate([played] + alts)
                                                  if sorted(bb) == sorted(pick)), None),
            })
        finally:
            os.unlink(tp)
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, f"{bid}.json"), "w"), indent=1)
    return out


def _turn_span(rows, r_me):
    idx = [i for i, (r, u, a, ts) in enumerate(rows) if u == ME and r == r_me]
    if not idx:
        return 0, 0
    end = idx[-1] + 1
    return idx[0], end


def report(out):
    print(f"{out['fight'][:8]} vs {out['opp']}")
    for t in out["turns"]:
        flag = []
        if t["regret"] and t["regret"] > 300:
            flag.append(f"REGRET {t['regret']:+d}: {'+'.join(t['best_alt'])}")
        if t["p_his_actual"] < 0.1:
            flag.append(f"misread him ({t['role_pred']} expected, {t['role_actual']} came)")
        if t["dmg_logged"] >= 100 and abs(t["dmg_planner"] - t["dmg_logged"]) > 0.05 * t["dmg_logged"]:
            flag.append(f"damage off (planner {t['dmg_planner']}, engine {t.get('dmg_engine')}, log {t['dmg_logged']})")
        print(f"  R{t['round']} {t['my_hp']:>4}/{t['his_hp']:<4} played {'+'.join(t['played'])} | he did "
              f"{'+'.join(t['his_next'])[:50]} (p {t['p_his_actual']:.0%}) | {'; '.join(flag) or 'ok'}")
    worst = max((t for t in out["turns"] if t["regret"] is not None), key=lambda t: t["regret"], default=None)
    if worst:
        cause = ("the opponent model (it did not see his turn coming)" if worst["p_his_actual"] < 0.1 else
                 "the damage numbers" if worst["dmg_logged"] >= 100 and abs(worst["dmg_planner"] - worst["dmg_logged"]) >
                 0.05 * worst["dmg_logged"] else "the choice itself")
        print(f"turning point: R{worst['round']}: {'+'.join(worst['best_alt'])} instead of {'+'.join(worst['played'])} "
              f"was worth {worst['regret']:+d} HP against what he actually did; cause: {cause}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bid")
    ap.add_argument("--alts", type=int, default=6)
    a = ap.parse_args()
    report(review(a.bid, a.alts))


if __name__ == "__main__":
    main()
