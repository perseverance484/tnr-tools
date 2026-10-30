#!/usr/bin/env python3
"""Skyglass weekend economy: expected yields for one dedicated player over a 12-hour weekend (stdlib only).

    python3 harness/skyglass_wreck_sim/tools/economy.py [--inputs economy_inputs.json] [--hours 12]
        [--haul-wreck 0.02] [--haul-hunt 0.0125] [--target-haul 1.5] [--json out.json]

Model (expected values, no sampling):
- The player farms the endgame Wreck (3-player party; every drop is per member) and runs every chart, page and Lantern
  it yields, solo, in sequence. Time = Wreck minutes + every run's minutes (a failed run costs `failFrac` of a clear).
- Drop tables: docs/design/SKYGLASS_LOOT_TABLES.md section 2 (Wreck), 3 (caches), 4a (picks), 5 (chart ladder, tainted,
  Core Rot), 5d (tokens, trophy tokens); Haul pages per profession: RUL-2026-10-29-053 (Wreck 2%, hunt endings 1.25%).
- A chart run's drops pay only on a clear (RUL-2026-10-28-022), except the Core Horror's Core Rot (an AI drop, paid on
  winning his fight) and the 1 Core Rot consolation on a failed rare / tainted run (RUL-2026-10-28-019).
- Steeping (RUL-2026-10-29-055): a rare chart + 3 Core Rot; win (measured) -> tainted chart; loss -> chart back, Rot spent.
  Policy: steep whenever the Rot allows (tainted is the better run); limited by Rot supply.
- Picks: one per run, two on tainted runs. Token policy: `always` takes the Skyglass Token card whenever offered,
  `typical` takes it on half of those picks, `never` never; every other pick is spread evenly over the run's
  non-token options (so chart options feed the ladder at that rate).
- Fixed point: runs per Wreck clear r = wreck_drops + M r (M = charts produced by each run type), solved by iteration.

Inputs (`--inputs`): measured clear rates and minutes per run type (harness results); missing keys fall back to the
DEFAULTS below and are listed as such in the output.
"""
import argparse
import json

RUNS = ["tide", "roster", "buried", "foundry", "archive", "watch", "reliquary", "fall", "t_rel", "t_fall", "crown", "haul"]
NAMES = {"tide": "Low Tide Run", "roster": "Night Watch", "buried": "Buried Cache", "foundry": "Drowned Foundry",
         "archive": "Quarantined Archive", "watch": "Captain's Watch", "reliquary": "Sealed Reliquary", "fall": "The Fall",
         "t_rel": "Rotted Reliquary", "t_fall": "Burning Heading", "crown": "Crownhold", "haul": "The Haul"}
DEFAULTS = {
    "wreck": {"minutes": 24.0},
    # clear: probability; minutes: a clear's length; pressOn: probability the player presses on; pressWin: of those.
    **{k: {"clear": 0.9, "minutes": 6.0, "pressOn": 0.0, "pressWin": 0.6} for k in RUNS},
    "steep": {"win": 0.75, "minutes": 3.0},
    "failFrac": 0.5,
    "overheadMin": 0.5,
}

# Endgame Wreck clear, per member (loot tables section 2). "crown" = the Lastlight Lantern (Crownhold access).
WRECK_CHARTS = {"buried": 0.20, "foundry": 0.12, "archive": 0.06, "watch": 0.06, "crown": 0.03, "tide": 0.15, "roster": 0.10}
WRECK_ROT = 0.15
WRECK_TREASURY = 0.03
COC = 0.10  # chest of chests: Common 40 Inro/Pouch, Rare 35 Strongbox/Galley, Epic 18 Coffer/Chart Case, Legendary 7 Treasury/Token
COC_TIERS = {"common": 0.40, "rare": 0.35, "epic": 0.18, "legendary": 0.07}
CHART_CASE = {"foundry": 0.45, "archive": 0.25, "watch": 0.20, "crown": 0.03, "reliquary": 0.035, "fall": 0.035}

# Chart ladder (ending drops on a clear) and press-on extras (loot tables section 5).
LADDER = {
    "tide": {"buried": 0.10}, "roster": {"buried": 0.10}, "buried": {"foundry": 0.15}, "foundry": {"archive": 0.10},
    "archive": {"reliquary": 0.25, "t_rel": 0.01}, "watch": {"fall": 0.25, "t_fall": 0.01},
    "reliquary": {"crown": 0.15}, "fall": {"crown": 0.15}, "t_rel": {"crown": 0.30}, "t_fall": {"crown": 0.30},
    "crown": {"reliquary": 0.25, "fall": 0.25}, "haul": {},
}
PRESS_EXTRA = {"archive": {"reliquary": 0.20}, "watch": {"fall": 0.20}, "reliquary": {"t_rel": 0.05}, "fall": {"t_fall": 0.05}}
HUNT_ENDINGS = ["buried", "foundry", "archive", "watch"]  # "each hunt ending" for the Haul pages
ROT_ON_CLEAR = {"tide": 0.15, "roster": 0.15, "t_rel": 0.40, "t_fall": 0.40}
ROT_CORE_HORROR = {"fall": 0.40}  # paid on winning his fight (the Fall's 3rd fight; approximated by the clear rate)
ROT_CONSOLATION = ["reliquary", "fall", "t_rel", "t_fall"]
TREASURY_STEP = {"tide": 0.01, "roster": 0.02, "buried": 0.01, "foundry": 0.05, "archive": 0.05, "watch": 0.04,
                 "reliquary": 0.06, "fall": 0.06, "t_rel": 0.06, "t_fall": 0.06, "crown": 0.06}

# Completion picks (section 4a). Each option: (name, {yield: amount}); "token" marks the Skyglass Token card.
PICKS = {
    "tide": [("Medicine Inro", {}), ("Galley Stores", {}), ("Watch Roster", {"chart:roster": 1})],
    "roster": [("Medicine Inro", {}), ("Galley Stores", {}), ("Tide Chart", {"chart:tide": 1})],
    "buried": [("Medicine Inro", {}), ("Galley Stores", {}), ("Foundry chart", {"chart:foundry": 1})],
    "foundry": [("Elemental Tool Pouch", {}), ("Medicine Inro", {}), ("Galley Stores", {})],
    "archive": [("Archive Chart Case", {"case": 1}), ("Sage's Strongbox", {}), ("Skyglass Token", {"token": 1})],
    "watch": [("Skyglass Coffer", {"coffer": 1}), ("Captain's Purse", {}), ("Skyglass Token", {"token": 1})],
    "reliquary": [("Skyglass Coffer x2", {"coffer": 2}), ("Sealed Treasury", {"treasury": 1}), ("Skyglass Token x2", {"token": 2}), ("Archive Chart Case x2", {"case": 2})],
    "fall": [("Skyglass Coffer x2", {"coffer": 2}), ("Sealed Treasury", {"treasury": 1}), ("Skyglass Token x2", {"token": 2}), ("Galley Stores x3", {})],
    "crown": [("Crown's Hoard", {"coffer": 1, "treasury": 1, "token": 1}), ("Skyglass Coffer x3", {"coffer": 3}), ("Crownbreaker badge", {}), ("Crownhold jutsu", {}), ("Crown Fragment", {})],
    "haul": [],
}
PICKS["t_rel"] = PICKS["reliquary"]
PICKS["t_fall"] = PICKS["fall"]
# Trophy (variant) tokens: bosses with a chart/hunt trophy per run, and the rate (RUL-2026-10-29-050 item 3).
TROPHY = {"foundry": (["Foundry Warden"], 0.01), "archive": (["Sealwright"], 0.01), "watch": (["Wayfinder"], 0.01),
          "reliquary": (["Foundry Warden", "Sealwright", "First Blade"], 0.02), "fall": ([], 0.02),
          "t_rel": (["Foundry Warden", "Sealwright", "First Blade"], 0.04), "t_fall": (["Wayfinder"], 0.04)}


def pick_yield(run, policy, picks=1):
    """Expected pick yields for one clear of `run` (dict yield -> amount)."""
    opts = PICKS.get(run, [])
    if not opts:
        return {}
    tok = [o for o in opts if "token" in o[1]]
    rest = [o for o in opts if "token" not in o[1]]
    p_tok = {"always": 1.0, "typical": 0.5, "never": 0.0}[policy] if tok else 0.0
    out = {}

    def add(o, w):
        for k, v in o[1].items():
            out[k] = out.get(k, 0) + v * w

    if picks == 1:
        for o in tok:
            add(o, p_tok / len(tok))
        for o in rest:
            add(o, (1 - p_tok) / len(rest))
    else:  # pick 2 distinct cards: the token card at most once (with p_tok), the other pick(s) spread over the rest
        for o in tok:
            add(o, p_tok / len(tok))
        n_rest = picks - p_tok
        for o in rest:
            add(o, n_rest / len(rest))
    return out


def solve(I, policy, haul_wreck, haul_hunt, hours, steep=True):
    clear = {k: I[k]["clear"] for k in RUNS}
    press = {k: I[k].get("pressOn", 0) * I[k].get("pressWin", 0) for k in RUNS}
    steep_win = I["steep"]["win"]
    # Charts per Wreck clear (direct drops + chest of chests Epic Chart Case half the time).
    w = {k: 0.0 for k in RUNS}
    for k, p in WRECK_CHARTS.items():
        w[k] += p
    for k, p in CHART_CASE.items():
        w[k] += COC * COC_TIERS["epic"] * 0.5 * p
    w["haul"] += 2 * haul_wreck
    # Iterate: r[k] = expected runs of k per Wreck clear (before steeping reassigns rare charts to tainted).
    r = dict(w)
    for _ in range(500):
        obtained = dict(w)
        for k in RUNS:
            n_clear = r[k] * clear[k]
            for t, p in LADDER[k].items():
                obtained[t] += n_clear * p
            for t, p in PRESS_EXTRA.get(k, {}).items():
                obtained[t] += r[k] * clear[k] * press.get(k, 0) * p if k in ("archive", "watch") else 0
            if k in ("reliquary", "fall"):
                obtained["t_rel" if k == "reliquary" else "t_fall"] += n_clear * press[k] * PRESS_EXTRA[k]["t_rel" if k == "reliquary" else "t_fall"]
            if k in HUNT_ENDINGS:
                obtained["haul"] += n_clear * 2 * haul_hunt
            picks = 2 if k in ("t_rel", "t_fall") else 1
            y = pick_yield(k, policy, picks)
            for yk, v in y.items():
                if yk.startswith("chart:"):
                    obtained[yk[6:]] += n_clear * v
                elif yk == "case":
                    for t, p in CHART_CASE.items():
                        obtained[t] += n_clear * v * p
        # Core Rot supply per Wreck clear -> steeping converts rare charts into tainted charts.
        rot = WRECK_ROT
        for k in RUNS:
            rot += r[k] * clear[k] * ROT_ON_CLEAR.get(k, 0) + r[k] * clear[k] * ROT_CORE_HORROR.get(k, 0)
            if k in ROT_CONSOLATION:
                rot += r[k] * (1 - clear[k])
        rares = obtained["reliquary"] + obtained["fall"]
        # Each tainted chart costs 3/steep_win Rot on average (a loss returns the chart, spends the Rot).
        tainted_possible = rot / (3.0 / steep_win)
        steep_frac = (min(1.0, tainted_possible / rares) if rares > 0 else 0.0) if steep else 0.0
        new = dict(obtained)
        for base, t in (("reliquary", "t_rel"), ("fall", "t_fall")):
            moved = obtained[base] * steep_frac
            new[base] -= moved
            new[t] += moved
        if max(abs(new[k] - r[k]) for k in RUNS) < 1e-12:
            r = new
            break
        r = new
    steep_attempts = max(0.0, (obtained["reliquary"] + obtained["fall"]) * steep_frac / steep_win)
    ff = I["failFrac"]
    oh = I["overheadMin"]
    run_min = {k: I[k]["minutes"] * (clear[k] + (1 - clear[k]) * ff) + oh for k in RUNS}
    cycle = I["wreck"]["minutes"] + sum(r[k] * run_min[k] for k in RUNS) + steep_attempts * (I["steep"]["minutes"] + oh)
    W = hours * 60 / cycle
    per = lambda x: x * W  # noqa: E731
    clears = {k: per(r[k] * clear[k]) for k in RUNS}
    runs = {k: per(r[k]) for k in RUNS}
    # Tokens, trophies, Core Rot, Treasury, Coffers.
    tok = per(COC * COC_TIERS["legendary"] * 0.5)
    coffer = per(COC * COC_TIERS["epic"] * 0.5)
    treasury = per(WRECK_TREASURY + COC * COC_TIERS["legendary"] * 0.5)
    for k in RUNS:
        y = pick_yield(k, policy, 2 if k in ("t_rel", "t_fall") else 1)
        tok += clears[k] * y.get("token", 0)
        coffer += clears[k] * y.get("coffer", 0)
        treasury += clears[k] * (y.get("treasury", 0) + TREASURY_STEP.get(k, 0))
    trophies = {}
    for k, (bosses, p) in TROPHY.items():
        for b in bosses:
            trophies[b] = trophies.get(b, 0) + clears[k] * p
    rot_in = per(WRECK_ROT) + sum(clears[k] * (ROT_ON_CLEAR.get(k, 0) + ROT_CORE_HORROR.get(k, 0)) for k in RUNS) + sum(runs[k] - clears[k] for k in ROT_CONSOLATION)
    rot_spent = per(steep_attempts) * 3
    time_split = {"wreck": round(W * I["wreck"]["minutes"] / 60, 2), **{k: round(runs[k] * run_min[k] / 60, 2) for k in RUNS if runs[k] > 0.005},
                  "steeping": round(per(steep_attempts) * (I["steep"]["minutes"] + oh) / 60, 2)}
    return {
        "policy": policy, "hauls": {"wreckPerPage": haul_wreck, "huntEndingPerPage": haul_hunt},
        "wreckClears": round(W, 2), "cycleMinutes": round(cycle, 1),
        "runs": {k: round(runs[k], 2) for k in RUNS}, "clears": {k: round(clears[k], 2) for k in RUNS},
        "chartsByTier": {
            "common (Tide, Roster)": round(runs["tide"] + runs["roster"], 2),
            "hunt (Buried, Foundry, Archive, Watch)": round(runs["buried"] + runs["foundry"] + runs["archive"] + runs["watch"], 2),
            "rare (Reliquary, Fall)": round(runs["reliquary"] + runs["fall"], 2),
            "tainted (Rotted, Burning)": round(runs["t_rel"] + runs["t_fall"], 2),
            "Lantern (Crownhold)": round(runs["crown"], 2),
            "Haul pages": round(runs["haul"], 2),
        },
        "steepAttempts": round(per(steep_attempts), 2), "steepFracOfRareCharts": round(steep_frac, 2),
        "coreRot": {"gained": round(rot_in, 2), "spentSteeping": round(rot_spent, 2)},
        "skyglassTokens": round(tok, 2), "trophyTokens": {k: round(v, 3) for k, v in trophies.items()}, "trophyTokensTotal": round(sum(trophies.values()), 3),
        "skyglassCoffers": round(coffer, 2), "sealedTreasuries": round(treasury, 2),
        "littleHorrorJarChance": round(1 - (1 - 0.05) ** W, 3),
        "hoursSplit": time_split,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs")
    ap.add_argument("--hours", type=float, default=12)
    ap.add_argument("--haul-wreck", type=float, default=0.02)
    ap.add_argument("--haul-hunt", type=float, default=0.0125)
    ap.add_argument("--target-haul", type=float, default=1.5)
    ap.add_argument("--json")
    a = ap.parse_args()
    I = json.loads(json.dumps(DEFAULTS))
    used_default = set(RUNS) | {"wreck", "steep"}
    if a.inputs:
        given = json.load(open(a.inputs))
        for k, v in given.items():
            if isinstance(v, dict):
                I.setdefault(k, {}).update(v)
                used_default.discard(k)
            elif not k.startswith("_"):
                I[k] = v
    out = {"inputs": I, "defaultsUsedFor": sorted(used_default), "hours": a.hours}
    for pol in ("typical", "always", "never"):
        out[pol] = solve(I, pol, a.haul_wreck, a.haul_hunt, a.hours)
    out["typical_noSteeping"] = solve(I, "typical", a.haul_wreck, a.haul_hunt, a.hours, steep=False)
    # Haul page rates for the target (typical policy): scale both rates together (Wreck : hunt kept at 2 : 1.25).
    lo, hi = 0.0, 20.0
    for _ in range(60):
        m = (lo + hi) / 2
        h = solve(I, "typical", a.haul_wreck * m, a.haul_hunt * m, a.hours)["runs"]["haul"]
        lo, hi = (m, hi) if h < a.target_haul else (lo, m)
    m = (lo + hi) / 2
    out["haulTarget"] = {"targetRuns": a.target_haul, "scale": round(m, 3), "wreckPerPage": round(a.haul_wreck * m, 4), "huntEndingPerPage": round(a.haul_hunt * m, 4),
                         "check": solve(I, "typical", a.haul_wreck * m, a.haul_hunt * m, a.hours)["runs"]["haul"]}
    # Wreck-only alternative: keep hunt endings at their rate, raise only the Wreck's.
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mw = (lo + hi) / 2
        h = solve(I, "typical", mw, a.haul_hunt, a.hours)["runs"]["haul"]
        lo, hi = (mw, hi) if h < a.target_haul else (lo, mw)
    out["haulTargetWreckOnly"] = {"wreckPerPage": round((lo + hi) / 2, 4), "huntEndingPerPage": a.haul_hunt}
    txt = json.dumps(out, indent=1)
    if a.json:
        open(a.json, "w").write(txt + "\n")
    t = out["typical"]
    print(f"Wreck clears {t['wreckClears']} (cycle {t['cycleMinutes']} min); Haul runs {t['runs']['haul']}; tokens typical {t['skyglassTokens']} / always {out['always']['skyglassTokens']} / never {out['never']['skyglassTokens']}")
    print(f"charts by tier: {t['chartsByTier']}")
    print(f"Core Rot {t['coreRot']}; steeping attempts {t['steepAttempts']}; trophy tokens {t['trophyTokensTotal']} {t['trophyTokens']}")
    print(f"Haul target {a.target_haul}: Wreck {out['haulTarget']['wreckPerPage']} / hunt {out['haulTarget']['huntEndingPerPage']} per page (x{out['haulTarget']['scale']}); Wreck-only: {out['haulTargetWreckOnly']}")
    print(f"defaults used for: {out['defaultsUsedFor']}")


if __name__ == "__main__":
    main()
