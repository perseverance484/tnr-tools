#!/usr/bin/env python3
"""Simulator check against the real logs (director 2026-11-11: "Verify the simulator against the logs").

For every turn in every logged fight (mine and harvested), the state just before the turn is rebuilt from the log
(tags by shotplan.rebuild, HP from the damage lines), the actions that were actually taken are played through
planner2's engine, and the damage it predicts is compared with the damage the log shows for that turn:
  dealt  damage the actor did to the other side (direct hits, pierce, afterburn on the target)
Reported per side (my actions from my calibrated kit, his from his catalog records) as median / mean absolute
error and the share of turns within 20%, plus the worst turns so the cause can be read off.

Usage: validate.py [--fight BID] [--worst 15] [--mine-only]
"""
import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clock  # noqa: E402
import exam  # noqa: E402
import opp_profile  # noqa: E402
import opponents as OM  # noqa: E402
import planner2 as P2  # noqa: E402
import shotplan  # noqa: E402
import value_model  # noqa: E402
from ingest import IDS, ME  # noqa: E402

DMG = re.compile(r"^(.+?) takes ([\d.]+) (damage|afterburn damage)$")


def turns(rows):
    """[(start index, round, user, [action ids])] in log order, waits/moves kept out of the action list."""
    out, cur = [], None
    for i, (r, u, a, ts) in enumerate(rows):
        if cur is None or cur[1] != r or cur[2] != u:
            cur = [i, r, u, []]
            out.append(cur)
        if a not in ("wait", "move"):
            cur[3].append(a)
    return out


def logged_dealt(rows, start, end, target):
    tot = 0.0
    for r, u, a, ts in rows[start:end]:
        for t in ts or []:
            m = DMG.match((t or "").strip())
            if m and m.group(1) == target:
                tot += float(m.group(2))
    return tot


def check_fight(bid, rows, cal, mine_only=False):
    users = [u for u in dict.fromkeys(u for _, u, _, _ in rows) if (u or "").startswith("user_")]
    if ME not in users or len(users) != 2:
        return []
    en_id = next(u for u in users if u != ME)
    en_name = OM.names_in(rows, en_id)
    me_prof = opp_profile.own_profile()
    prof = opp_profile.profile(en_id, rows)
    scale = opp_profile.given_mult(prof) / max(1.0, opp_profile.given_mult(me_prof))
    my_kit = P2.make_my_kit(prof)
    his = clock.acts_from_ids([a for _, u, a, _ in rows if u == en_id])
    his_kit = {a: P2.compile_spec((v[4][0] * scale,) + tuple(v[4][1:]), False) for a, v in his.items()}
    hps = exam.hp_track(rows, ["dauntless", en_name])
    out = []
    tl = turns(rows)
    for k, (i, r, u, acts) in enumerate(tl):
        if not acts:
            continue
        end = tl[k + 1][0] if k + 1 < len(tl) else len(rows)
        mine = u == ME
        if mine_only and not mine:
            continue
        lines = [f"{rr}|{t.strip()}" for rr, uu, aa, ts in rows[:i] for t in (ts or [])]
        sme, sen = shotplan.rebuild(lines, "dauntless", en_name, hps[i]["dauntless"], hps[i][en_name])
        shotplan.off_ground(sme, rows[:i], ME, {"GAyHRgaa1lkYGhE9WxlRL", "replacementTechnique", "move"})
        me, en = P2.from_shotplan(sme, r), P2.from_shotplan(sen, r)
        me.passives(**me_prof.get("passives", {}))
        en.passives(**prof.get("passives", {}))
        if mine:
            names = [IDS.get(a, a) for a in acts]
            specs = [my_kit[n] for n in names if n in my_kit]
            unknown = [n for n in names if n not in my_kit and n not in ("step", "wait")]
            if "cleanse" in names:
                me.wipe(P2.NEGK)
            d, s = P2.run_turn(me, en, specs, 0, 1e9, 1e9)
            logged = logged_dealt(rows, i, end, en_name)
        else:
            specs = [his_kit[a] for a in acts if a in his_kit]
            unknown = [a for a in acts if a not in his_kit]
            d, s = P2.run_turn(en, me, specs, 0, 1e9, 1e9)
            logged = logged_dealt(rows, i, end, "dauntless")
        if logged < 50 and d < 50:
            continue                                          # a no-damage turn: nothing to compare
        names = [IDS.get(a) or (his.get(a) or (a,))[0] for a in acts]
        out.append({"fight": bid, "round": r, "side": "me" if mine else "him", "opp": en_name,
                    "acts": names, "pred": round(d), "logged": round(logged),
                    "err": (d - logged) / max(200.0, logged), "unknown": unknown})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fight")
    ap.add_argument("--worst", type=int, default=15)
    ap.add_argument("--mine-only", action="store_true")
    a = ap.parse_args()
    cal = value_model.load_cal()
    value_model.calibrate_kit(cal)
    res = []
    for bid, path, rows, meta in OM.load_logs():
        if a.fight and not bid.startswith(a.fight):
            continue
        try:
            res += check_fight(bid, rows, cal, a.mine_only)
        except Exception as e:  # noqa: BLE001
            print(f"skip {bid}: {e}")
    for side in ("me", "him"):
        rs = [x for x in res if x["side"] == side]
        if not rs:
            continue
        errs = [abs(x["err"]) for x in rs]
        bias = statistics.mean(x["err"] for x in rs)
        print(f"{side:3}: {len(rs)} turns  median |err| {statistics.median(errs):.0%}  mean |err| {statistics.mean(errs):.0%}"
              f"  within 20% {sum(e <= 0.2 for e in errs) / len(errs):.0%}  bias {bias:+.0%}"
              f"  (turns with unknown actions: {sum(1 for x in rs if x['unknown'])})")
    print("\nworst turns:")
    for x in sorted(res, key=lambda x: -abs(x["err"]))[:a.worst]:
        print(f"  {x['fight'][:6]} R{x['round']} {x['side']:3} vs {x['opp'][:12]:12} {'+'.join(x['acts'])[:60]:60} "
              f"pred {x['pred']:5} logged {x['logged']:5} ({x['err']:+.0%}){' unknown ' + ','.join(x['unknown']) if x['unknown'] else ''}")
    json.dump(res, open(os.path.join(HERE, "..", "fights", "validation.json"), "w"), indent=0)


def check_policy():
    """How often the simulator's opponent bot picks what the real player picked, on every logged turn of his
    (his ready actions from his log so far, scored by his own score + habits). In-sample for habits."""
    import fightsim
    models = OM.load()
    exact = n = 0
    ov = 0.0
    per = {}
    for bid, path, rows, meta in OM.load_logs():
        users = [u for u in dict.fromkeys(u for _, u, _, _ in rows) if (u or "").startswith("user_")]
        if ME not in users or len(users) != 2:
            continue
        en_id = next(u for u in users if u != ME)
        if os.environ.get("TNR_LOO"):
            m = OM.build(exclude=bid, save=False).get(en_id)    # his habits without this fight (honest check)
        else:
            m = models.get(en_id)
        if not m:
            continue
        acts, habit = OM.acts_for(m), OM.habit_fn(m)
        en_name = OM.names_in(rows, en_id)
        prof = opp_profile.profile(en_id, rows)
        hps = exam.hp_track(rows, ["dauntless", en_name])
        f = fightsim.Fight(acts, prof, True, habit=habit)
        tl = turns(rows)
        prev, nturn = None, 0
        for k, (i, r, u, act) in enumerate(tl):
            if u != en_id or not act:
                continue
            lines = [f"{rr}|{t.strip()}" for rr, uu, aa, ts in rows[:i] for t in (ts or [])]
            sme, sen = shotplan.rebuild(lines, "dauntless", en_name, hps[i]["dauntless"], hps[i][en_name])
            f.me, f.en = P2.from_shotplan(sme, r), P2.from_shotplan(sen, r)
            f.rows = [(rr, uu if uu == ME else fightsim.EN_ID, x, None) for rr, uu, x, _ in rows[:i]]
            f.R, f.his_prev, f.his_turns = r, prev, nturn
            ready = clock.ready_at(acts, fightsim.EN_ID, f.rows, r)
            lines_ = clock.bundles(acts, ready, 100)
            if not lines_:
                continue
            Pl = P2.Planner(f.me, f.en, r, f.ctx(), f.cal, {}, f.his_kit, {"loadout": [], "used": []}, False,
                            (5050, 5050), f.base_turn, {})
            best = max(lines_, key=lambda hb: Pl.his_score(hb, f.me, f.en) + habit(hb, r, prev, nturn == 0))
            real = set(a for a in act if a in acts)
            got = set(best)
            n += 1
            exact += got == real
            ov += len(got & real) / max(1, len(real))
            nm = m["names"][0]
            per.setdefault(nm, [0, 0])
            per[nm][0] += got == real; per[nm][1] += 1
            prev, nturn = tuple(act), nturn + 1
    print(f"opponent bot vs real choices: {exact}/{n} exact ({exact / max(1, n):.0%}), mean overlap {ov / max(1, n):.0%}")
    print("  " + ", ".join(f"{k} {a}/{b}" for k, (a, b) in sorted(per.items(), key=lambda kv: -kv[1][1])[:12]))


if __name__ == "__main__":
    if "--policy" in sys.argv:
        check_policy()
    else:
        main()
