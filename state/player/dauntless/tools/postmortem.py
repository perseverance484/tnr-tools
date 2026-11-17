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

Then the replay review (critique.review_fight): every turn I played, checked against the director's fight 2
critique (positions vs my Subaku Palace, buffs into his ready Clear, the burst round without Limit Breaker or
Aetherion, no Danse Macabre / Chakra Resistance before a nuke, late pill and stance padding).

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
import critique  # noqa: E402
import value_model  # noqa: E402
from ingest import IDS, ME  # noqa: E402

OUT = os.environ.get("TNR_POSTMORTEM_OUT") or os.path.join(HERE, "..", "fights", "postmortems")
LEARN = os.environ.get("TNR_LEARN", "1") == "1"


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


def turns_after(rows, r_me, en_id, depth):
    """The turns that followed my turn of round r_me in the log, his and mine in turn, as the engine's script:
    [{"who": "him" | "me", "actions": [ids]}], from his next turn to his depth-th. Waits and plain moves are left
    out, as in his_next_turn; a turn that was only those is an empty one."""
    out, seen_me = [], False
    for r, u, a, ts in rows:
        if u == ME and r == r_me and not out:
            seen_me = True
            continue
        if not seen_me or u not in (ME, en_id):
            continue
        who = "me" if u == ME else "him"
        if not out or out[-1]["who"] != who or out[-1]["round"] != r:
            if sum(t["who"] == "him" for t in out) >= depth and who == "me":
                break
            out.append({"who": who, "round": r, "actions": []})
        if a not in ("wait", "move"):
            out[-1]["actions"].append(a)
    while out and out[0]["who"] == "me":                  # (my own turn went on: not a turn after it)
        out.pop(0)
    kept, his = [], 0
    for t in out:
        kept.append({"who": t["who"], "actions": t["actions"]})
        his += t["who"] == "him"
        if his >= depth:
            break
    return kept


def my_turn_at(rows, r_me):
    return [IDS.get(a, a) for r, u, a, ts in rows if u == ME and r == r_me and a not in ("wait", "move")]


def exchange(rows_pre, en, me, R, en_acted, cal, bundles, his_actual, script=None):
    """Engine: each bundle on this exact position, then his actual next turn replayed (as a scripted reply).
    Returns (my HP, his HP, his HP after my turn alone, deep) or None per bundle. With a script (turns_after, more
    than his one turn) the turns that followed are played on, mine as I actually played them, and deep is
    [(my HP, his HP)] after each of his turns; else it is None."""
    me_pos, en_pos = (me["longitude"], me["latitude"]), (en["longitude"], en["latitude"])
    seqs = [turn.resolve_targets(tuple(b), me_pos, en_pos, set())[0] for b in bundles]
    req = EB._replay_request(rows_pre, ME, en["userId"], me, en, me_pos, en_pos, R, "next" if en_acted else "same", cal)
    req["mode"] = "eval"
    req["candidates"] = [[{"actionId": a, "x": t[0], "y": t[1]} for _, a, t in s] for s in seqs]
    if script and len(script) > 1:
        req["script"] = script
    else:
        req["scriptedReply"] = list(his_actual)
    req["replyCap"] = 1
    res = EB._run(req, 90) or {}
    out = []
    for r in res.get("results") or []:
        if not r.get("legal"):
            out.append(None)
            continue
        his = [t for t in r.get("afterScript") or [] if t["who"] == "him"]
        after = (his[0] if his else None) or r.get("afterScripted") or r.get("afterMe")
        last = (r.get("afterScript") or [None])[-1]
        deep = [(t["me"], t["him"]) for t in his] + ([(last["me"], last["him"])] if last and last["who"] == "me" else [])
        out.append((after["me"], after["him"], r["afterMe"]["him"], deep if "script" in req else None))
    return out


UNMEASURED = ()      # what swings() gives for the exchanges when the engine gave no answer
# How many of his actual turns each alternative is played against (tune_real.py --depth). One: his next turn, as it
# always was. More: the turns that followed are played on, his and mine as the log has them, and each turn also
# keeps where things stood after his last one ("deep"). One exchange gives a buff no credit for the rounds after
# (RUL-2026-11-17-166, 3). The turns of mine that follow are the ones played after what was played, so the
# deeper figure leans to what was played: read it as "with the same follow-up", not as each line's best.
DEPTH = int(os.environ.get("TNR_TUNE_DEPTH", "1"))


def deep_swings(ex, n):
    """My HP minus his after the last turn the script reached, per bundle; None where there is none."""
    if len(ex) != n:
        return [None] * n
    return [(round(v[3][-1][0] - v[3][-1][1]) if v is not None and v[3] else None) for v in ex]


def swings(ex, n):
    """(the exchanges, my HP minus his after each of the n bundles and his actual reply). A bundle the engine
    rejects is None. With no answer for the turn (no engine app on this machine, or the engine failed), none of
    the n is measured: the turn keeps its read and its numbers, and has no regret. Run 2 ran where there is no
    engine, and the review of both its losses stopped here on the first turn."""
    if len(ex) != n:
        return UNMEASURED, [None] * n
    return ex, [(None if v is None else round(v[0] - v[1])) for v in ex]


def review(bid_prefix, n_alts=6):
    cal = value_model.load_cal()
    value_model.calibrate_kit(cal)
    log = next(((b, rows, p) for b, p, rows, m in OM.load_logs() if b.startswith(bid_prefix)), None)
    if not log:
        sys.exit(f"no log for {bid_prefix}")
    bid, rows, log_path = log
    en_id = critique.opponent_of(rows, ME)
    if en_id is None:
        sys.exit(f"{bid}: nobody but me acts in this log")
    os.environ["TNR_OM_EXCLUDE"] = bid          # his model without this fight: an honest read
    model = OM.load().get(en_id)
    acts = OM.acts_for(model) if model else {}
    out = {"fight": bid, "opp": OM.names_in(rows, en_id), "turns": [], "engine": True}
    # the replay review (director 2026-11-16: "analyze replays as I just did to spot errors"): every turn against
    # his fight 2 critique, from the log and the archived live states (critique.review_fight)
    out["errors"] = critique.review_fight(rows, ME, en_id, me_name=turn.ME_NAME,
                                          states=critique.archived_states(bid),
                                          limit_breaker=critique.had_limit_breaker(rows, ME, log_path),
                                          tiles=critique.log_tiles(log_path))
    learned = []
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
            script = turns_after(rows, r, en_id, DEPTH) if DEPTH > 1 else None
            ex, score = swings(exchange(rows_pre, en, me, info["R"], en_acted, cal, [played] + alts, his_actual,
                                        script), 1 + len(alts))
            out["engine"] = out["engine"] and ex is not UNMEASURED
            deep = deep_swings(ex, 1 + len(alts))
            # what worked against what he actually did goes into the solution library, keyed by the situation and
            # his last turn's signature (director 2026-11-11: "update the solutions library as we see it and
            # successfully respond to it")
            vals = sorted(((v, tuple(bb)) for v, bb in zip(score, [played] + alts) if v is not None), reverse=True)
            if LEARN and vals and getattr(P, "book_key", None):
                learned.append((P.book_key, vals, tuple(pick)))
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
            if DEPTH > 1:
                at = lambda b: next((deep[i] for i, bb in enumerate([played] + alts) if sorted(bb) == sorted(b)), None)
                out["turns"][-1]["deep"] = {
                    "his_turns": sum(t["who"] == "him" for t in script), "played": deep[0], "pick": at(pick),
                    "best": max((d for d in deep if d is not None), default=None)}
        finally:
            os.unlink(tp)
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, f"{bid}.json"), "w"), indent=1)
    if learned:
        import solutions
        lib = solutions.load(solutions.LIVE)
        done = set(lib.get("_fights", []))
        if bid not in done:                         # each fight teaches once
            for key, vals, pick in learned:
                solutions.merge(lib, key, [(float(v), list(b)) for v, b in vals], list(pick))
            lib["_fights"] = sorted(done | {bid})
            solutions.save(lib, solutions.LIVE)
        out["learned"] = len(learned)
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
    if not out.get("engine", True):
        print("  the engine gave no answer for a turn (no engine app on this machine? harness/pvp_turn/README.md, "
              "\"Engine version\"): what the alternatives were worth against his actual reply is not measured there")
    if out.get("errors") is not None:
        critique.report_fight(out["errors"])
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
