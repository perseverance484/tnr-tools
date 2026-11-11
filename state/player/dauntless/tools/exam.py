#!/usr/bin/env python3
"""Battle exam: how often does the planner make the director's call?

Ground truth = the director's own turns in fights he played (director 2026-11-11: "up to this point I've been coaching
it ... develop its overall battle intelligence"). For every turn of his, the state just before it is rebuilt from the
log (HP from the damage/heal lines, tags by the planner's own rebuild), the planner is asked, and its action set is
compared with his: exact match, or overlap (shared actions / his actions). Moves (step / Replacement / Phantom's leap
target) are compared by name only; positions are not logged, so both sides stand adjacent.

Usage: exam.py [--fights F1,F2] [--verbose]   (offline, python planner, ~2 s a turn)
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIGHTS = os.path.join(HERE, "..", "fights")
ME = "user_37qazcrgUPldBPI65bb25DQiCjz"
sys.path.insert(0, HERE)
from ingest import IDS  # noqa: E402

# director-played fights: battle id -> (opponent name as logged, loadout then)
EXAM = {
    "CPrSC7ITz-P983Vu3_Z4u": ("Zaruza", "pvp1_parry"),
    "CECJR-hUmD_9Z_C1lbbCT": ("HikuroHatake", "pvp1_parry"),
    "ghAJqelEhXlxn7ksdOYXv": ("TearsOfAngel", "pvp1_parry"),
    "6GEbt0oeNAjdmNmn_nxuX": ("ANBU Member", "pvp1_parry"),
}
SKIP = {"move", "wait", "step", "stepback"}
HP_LOSS = re.compile(r"^(\S+(?: Member)?) (?:takes|loses) ([\d.]+) (?:\w+ )?(?:damage|HP to drain)")
HP_GAIN = re.compile(r"^(\S+(?: Member)?) (?:heals ([\d.]+) HP|absorbs ([\d.]+) damage and converts|steals ([\d.]+) damage as health)")


def hp_track(rows, names):
    hp = {n: 5050.0 for n in names}
    out = []
    for r, u, a, ts in rows:
        out.append(dict(hp))
        for t in ts or []:
            t = t.strip()
            if (m := HP_LOSS.match(t)) and m.group(1) in hp:
                hp[m.group(1)] -= float(m.group(2))
            elif (m := HP_GAIN.match(t)) and m.group(1) in hp:
                hp[m.group(1)] += float(next(g for g in m.groups()[1:] if g))
            for n in hp:
                hp[n] = max(1.0, min(5050.0, hp[n]))
    return out


def turns(bid, enemy):
    d = json.load(open(os.path.join(FIGHTS, f"{bid}_entries.json")))
    rows = list(zip(d["*.battleRound"], d["*.userId"], d["*.actionId"], d["*.appliedEffects.*.txt"]))[::-1]
    en_id = next(u for _, u, _, _ in rows if u != ME)
    hps = hp_track(rows, ["dauntless", enemy])
    seen = set()
    for i, (r, u, a, ts) in enumerate(rows):
        if u != ME or r in seen:
            continue
        seen.add(r)
        mine = [IDS.get(x, x) for rr, uu, x, _ in rows[i:] if rr == r and uu == ME]
        mine = sorted(x for x in mine if x not in SKIP)
        if not mine:
            continue
        pre = rows[:i][::-1]
        hp = hps[i]
        b = {"battle.version": 1, "battle.round": r, "battle.activeUserId": ME,
             "battle.usersState.*.userId": [en_id, ME], "battle.usersState.*.username": [enemy, "dauntless"],
             "battle.usersState.*.curHealth": [hp[enemy], hp["dauntless"]],
             "battle.usersState.*.maxHealth": [5050, 5050], "battle.usersState.*.longitude": [6, 7],
             "battle.usersState.*.latitude": [4, 4], "battle.usersState.*.actionPoints": [0, 100]}
        e = {"*.battleRound": [x[0] for x in pre], "*.userId": [x[1] for x in pre], "*.actionId": [x[2] for x in pre],
             "*.appliedEffects.*.txt": [x[3] for x in pre]}
        yield r, b, e, mine, hp


PLANNER = "turn.py"


def ask(b, e, bid, r, loadout, enemy, dump=None):
    path = os.path.join(HERE, "..", "fights", "live", f"exam_{bid}_{r}.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(json.dumps(b) + "\n" + json.dumps(e) + "\n")
    out = subprocess.run([sys.executable, os.path.join(HERE, PLANNER), path, "--battle", f"EXAM_{bid}_{r}",
                          "--top", "1", "--no-engine", "--loadout", loadout, "--enemy", enemy]
                         + (["--dump", dump] if dump else []),
                         capture_output=True, text=True, timeout=60).stdout
    m = re.search(r"^FIRE: (.*)$", out, re.M)
    os.unlink(path)
    if not m:
        return None
    return sorted(x["name"] for x in json.loads(m.group(1)) if x["name"] not in SKIP)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--planner", default="turn.py")
    ap.add_argument("--tune", action="store_true", help="planner2: fit its score weights to the director's turns")
    a = ap.parse_args()
    global PLANNER
    PLANNER = a.planner
    if a.tune:
        return tune(a)
    pick = a.fights.split(",") if a.fights else list(EXAM)
    exact = n = 0
    overlap = 0.0
    for bid in pick:
        enemy, loadout = EXAM[bid]
        for r, b, e, his, hp in turns(bid, enemy):
            got = ask(b, e, bid, r, loadout, enemy) or []
            n += 1
            ok = got == his
            exact += ok
            ov = len(set(got) & set(his)) / max(1, len(set(his)))
            overlap += ov
            if a.verbose or not ok:
                print(f"{enemy[:12]:12} R{r} hp {hp['dauntless']:.0f}/{hp[enemy]:.0f}  director {'+'.join(his):32} "
                      f"planner {'+'.join(got) or '-':32} {'OK' if ok else f'{ov:.0%}'}")
    print(f"\nEXAM: {exact}/{n} exact ({exact / max(1, n):.0%}), mean overlap {overlap / max(1, n):.0%}")


def collect(pick):
    """planner2 feature dumps for every exam turn: [(director's set, [(bundle, row)])]."""
    data = []
    for bid in pick:
        enemy, loadout = EXAM[bid]
        for r, b, e, his, hp in turns(bid, enemy):
            dump = os.path.join(FIGHTS, "live", f"exam_dump_{bid}_{r}.json")
            ask(b, e, bid, r, loadout, enemy, dump)
            if not os.path.exists(dump):
                continue
            rows = json.load(open(dump))["bundles"]
            os.unlink(dump)
            data.append((bid, r, his, [(sorted(x for x in row["b"] if x not in SKIP), row) for row in rows]))
    return data


def evaluate(W, data):
    """(-mean percentile rank of the director's bundle, exact top-1 count, mean overlap of the top pick). The rank is
    the tuning objective: smooth, and it uses every turn, not only the near-misses."""
    import planner2
    exact = 0
    ov = pct = 0.0
    for bid, r, his, cands in data:
        sc = [planner2.total(W, c[1]["f"], c[1]["term"], c[1]["rc"], c[1]["waste"], c[1]["guard"]) for c in cands]
        best = max(range(len(cands)), key=lambda i: sc[i])
        exact += cands[best][0] == his
        ov += len(set(cands[best][0]) & set(his)) / max(1, len(set(his)))
        mine = [sc[i] for i, c in enumerate(cands) if c[0] == his]
        pct += (sum(1 for x in sc if x > max(mine)) / len(sc)) if mine else 1.0
    n = max(1, len(data))
    return -round(pct / n, 4), exact, round(ov / n, 3)


def tune(a):
    """Coordinate search on planner2's weights: maximise exact matches, then overlap (features are linear in W, so
    each trial is a re-rank of the dumped candidates, not a re-plan). Leave-one-fight-out score printed as a check
    against overfitting."""
    import planner2
    pick = a.fights.split(",") if a.fights else list(EXAM)
    data = collect(pick)
    W0 = planner2.load_weights()

    def fit(train):
        W = dict(W0)
        best = evaluate(W, train)
        steps = {k: (0.5 if k != "race" else 100.0) if k != "waste" else 60.0 for k in W if k != "swing"}
        for _ in range(6):
            improved = False
            for k in list(steps):
                for sign in (1, -1):
                    T = dict(W)
                    T[k] = max(0.0, W[k] + sign * steps[k])
                    sc = evaluate(T, train)
                    if sc > best:
                        W, best, improved = T, sc, True
            if not improved:
                steps = {k: v / 2 for k, v in steps.items()}
        return W, best

    W, best = fit(data)
    print(f"tuned on {len(data)} turns: director pick at top {-best[0]:.1%} on average, {best[1]} exact, overlap {best[2]:.0%} (start: {evaluate(W0, data)})")
    print("weights:", json.dumps({k: round(v, 3) for k, v in W.items()}))
    held = [0, 0.0, 0]
    for bid in pick:
        tr = [d for d in data if d[0] != bid]
        te = [d for d in data if d[0] == bid]
        Wf, _ = fit(tr)
        p, ex, ov = evaluate(Wf, te)
        held[0] += -p * len(te); held[1] += ex; held[2] += len(te)
    print(f"leave-one-fight-out: director pick at top {held[0] / max(1, held[2]):.1%} on average, {held[1]}/{held[2]} exact")
    json.dump({k: round(v, 4) for k, v in W.items()}, open(planner2.WFILE, "w"), indent=1)
    print("saved", planner2.WFILE)


if __name__ == "__main__":
    main()
