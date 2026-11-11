#!/usr/bin/env python3
"""Out-of-sample check of the engine harness against logged fights.

For every one of my turns in state/player/dauntless/fights/*_entries.json: rebuild the live tags from the log
before that turn (shotplan.rebuild), fire my ACTUAL bundle on the engine (adjacent placement, both 5050 HP), and
compare the predicted direct damage to the opponent with the logged direct damage ("<enemy> takes N damage";
reflect/afterburn/recoil/wound excluded). Prints per-turn rows and the error summary; writes
harness/pvp_turn/results/validation.json.
Usage: TNR_ENGINE_APP=... validate_engine.py
"""
import glob
import json
import os
import re
import statistics as st
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "state/player/dauntless/tools"))
import engine_bridge as EB  # noqa: E402
import shotplan  # noqa: E402

ME = "user_37qazcrgUPldBPI65bb25DQiCjz"
HIT = re.compile(r"^(\S+) takes ([\d.]+) damage$")
SELF_LIKE = {"defensiveStance", "offensiveStance", "basicHeal", "cleanse", "meditate"}
MOVES = {"move", "replacementTechnique", "GAyHRgaa1lkYGhE9WxlRL"}


def load(path):
    d = json.load(open(path))
    return list(zip(d["*.battleRound"], d["*.userId"], d["*.actionId"], d["*.appliedEffects.*.txt"]))[::-1]


def enemy_name(rows):
    for _, u, _, ts in rows:
        if u != ME:
            for t in ts or []:
                w = t.split(" ", 1)[0]
                if w not in ("dauntless", "The", "Parry") and not w.endswith("'s"):
                    return w
    return None


def main():
    app = EB.engine_app()
    if not app:
        sys.exit("set TNR_ENGINE_APP or harness/pvp_turn/.engine_app")
    recs, prof = EB._records(), EB._profile()
    rows_out = []
    for path in sorted(glob.glob(os.path.join(REPO, "state/player/dauntless/fights/*_entries.json"))):
        rows = load(path)
        en = enemy_name(rows)
        if not en:
            continue
        turns = {}
        for i, (r, u, a, ts) in enumerate(rows):
            if u == ME:
                turns.setdefault(r, []).append((i, a, ts or []))
        used = {}
        for R, acts in sorted(turns.items()):
            first = acts[0][0]
            lines = [f"{r}|{t.strip()}" for r, u, a, ts in rows[:first] for t in (ts or [])]
            me0, en0 = shotplan.rebuild(lines, "dauntless", en, 5050, 5050)
            bundle = [a for _, a, _ in acts if a not in ("wait",)]
            if any(a not in recs and a not in EB.BASIC for a in bundle):
                for _, a, _ in acts:
                    used[a] = R
                continue
            dealt = sum(float(m.group(2)) for _, _, ts in acts for t in ts
                        if (m := HIT.match(t.strip())) and m.group(1) == en
                        and "shield absorbs" not in " ".join(ts))
            kit = [{"record": recs[a]["record"], "kind": "item" if a in EB.ITEM_IDS else "jutsu",
                    "level": prof["jutsuLevels"].get(a, 25)} for a in sorted({*bundle, *used} & set(recs))]
            cand = []
            for a in bundle:
                if a in MOVES:
                    cand.append({"actionId": a, "x": 3, "y": 4})
                elif a in SELF_LIKE or recs.get(a, {}).get("record", {}).get("target") == "SELF":
                    cand.append({"actionId": a, "x": 4, "y": 4})
                else:
                    cand.append({"actionId": a, "x": 5, "y": 4})
            req = {"round": R, "hisTurn": "same",
                   "me": {"id": "me", "hp": 5050, "x": 4, "y": 4, "profile": prof, "kit": kit,
                          "used": [{"actionId": a, "round": r} for a, r in used.items()],
                          "passives": [{"type": "increasedamagegiven", "power": EB.PASSIVE}]},
                   "him": {"id": "him", "hp": 5050, "x": 5, "y": 4, "kit": [], "used": [],
                           "passives": [{"type": "increasedamagegiven", "power": EB.PASSIVE}]},
                   "effects": EB.effects_from(me0, "me", "him", R) + EB.effects_from(en0, "him", "me", R),
                   "candidates": [cand], "replies": []}
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
                json.dump(req, f)
            out = subprocess.run([os.path.join(EB.HARNESS, "run.sh"), f.name], capture_output=True, text=True,
                                 env=dict(os.environ, TNR_ENGINE_APP=app))
            os.unlink(f.name)
            for _, a, _ in acts:
                used[a] = R
            try:
                res = json.loads(out.stdout)[0]
            except (ValueError, IndexError):
                rows_out.append({"fight": os.path.basename(path)[:12], "round": R, "error": out.stderr[-200:]})
                continue
            pred = 5050 - res["afterMe"]["him"] if res.get("legal") else None
            rows_out.append({"fight": os.path.basename(path)[:12], "enemy": en, "round": R,
                             "bundle": [EB_NAME.get(a, a) for a in bundle], "logged": round(dealt),
                             "engine": pred, "legal": res.get("legal"), "reason": res.get("reason")})
            print(rows_out[-1])
    good = [r for r in rows_out if r.get("engine") is not None and r["logged"] >= 100]
    errs = [abs(r["engine"] - r["logged"]) / r["logged"] for r in good]
    summary = {"turns": len(rows_out), "compared": len(good),
               "median_abs_err": round(st.median(errs), 3) if errs else None,
               "mean_abs_err": round(st.mean(errs), 3) if errs else None,
               "within_10pct": sum(e <= 0.10 for e in errs), "within_20pct": sum(e <= 0.20 for e in errs),
               "illegal": [r for r in rows_out if r.get("legal") is False]}
    os.makedirs(os.path.join(REPO, "harness/pvp_turn/results"), exist_ok=True)
    json.dump({"summary": summary, "rows": rows_out}, open(os.path.join(REPO, "harness/pvp_turn/results/validation.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != "illegal"}), "illegal:", len(summary["illegal"]))


try:
    from ingest import IDS as _IDS
    EB_NAME = dict(_IDS)
except Exception:  # noqa: BLE001
    EB_NAME = {}

if __name__ == "__main__":
    main()
