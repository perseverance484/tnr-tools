#!/usr/bin/env python3
"""Calibrate the planner's value model from every logged fight that has action ids (fights/*.json).

Writes tools/calibration.json, which turn.py reads. Run it after postfight (postfight.py calls it).

What it measures (engine rules from game_pin app/src/libs/combat, see combat_rules.md):
  my_base[action]   median base damage of each of my hits = observed damage / modelled multiplier
                    (my live +given x his live +taken x prod(1 - his DR)); shield-absorbed hits skipped.
  en_hit            median base damage of an enemy damaging action, same normalisation the other way round.
  en_turn_norm / en_burst_norm  median / 85th percentile of active (>= 250) enemy turns in base units.
  en_turn / en_burst  median and 80th-percentile HP the enemy took off me per active turn (all sources:
                    hits, wound/drain ticks, afterburn, recoil). AFK fights excluded.
  p_*               how often enemies did each threat when they could (experience weights for the
                    enemy option set): pierce when ready, Clear when held and I had a live buff, Smoke
                    once per fight, setup (buff + debuff me, little damage), burst.
  debuff_value      mean HP a live debuff package on me was worth to them over its 2 rounds (what Cleanse saves).
  buff_value        same for his buffs (what Clear saves).
  fight_len         median rounds per fight (scales long-cooldown reserves).
"""
import glob
import json
import os
import re
import statistics as st

import shotplan
from ingest import IDS

HERE = os.path.dirname(os.path.abspath(__file__))
FIGHTS = os.path.join(HERE, "..", "fights")
ME, ME_NAME = "user_37qazcrgUPldBPI65bb25DQiCjz", "dauntless"
PIERCE_IDS = {"osJq3k77YPGoFWgof12FQ", "G6MRbppaDZ2a5Wr0GIjH8"}
SMOKE_ID = "TtYPd-LcXKeK3sMuhq1TP"
HIT = re.compile(r"^(\S+) takes ([\d.]+) damage$")
ANY_DMG = re.compile(r"^dauntless takes ([\d.]+) (?:\w+ )?damage$")


def q(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else 0.0


def load(path):
    d = json.load(open(path))
    eff = d.get("*.appliedEffects.*.txt")
    if eff is None:  # older capture: list of effect objects per row
        eff = [[e.get("txt", "") if isinstance(e, dict) else str(e) for e in (row or [])] for row in d["*.appliedEffects"]]
    rows = list(zip(d["*.battleRound"], d["*.userId"], d["*.actionId"], eff))
    rows.reverse()  # oldest first
    return rows


def enemy_name(rows):
    for _, u, _, ts in rows:
        for t in ts or []:
            w = t.split(" ", 1)[0]
            if w != ME_NAME and w not in ("The", "Parry") and not w.endswith("'s"):
                return w
    return None


def main():
    my_base, en_hit, en_turn, en_norm = {}, [], [], []
    opp = {"pierce_vs_shield": [0, 0], "clear_vs_2buffs": [0, 0], "clear_vs_3buffs": [0, 0], "clear_vs_4buffs": [0, 0], "pierce": [0, 0], "clear": [0, 0], "smoke": [0, 0], "setup": [0, 0], "cleanse": [0, 0]}
    debuff_vals, buff_vals, lengths = [], [], []
    clear_wait = []  # per Clear on a 4+ stack: how many 4+ opportunities he had seen in that fight (1 = the first)
    for path in sorted(glob.glob(os.path.join(FIGHTS, "*.json"))):
        if "_afk" in path:
            continue
        rows = load(path)
        en_id = next((u for _, u, _, _ in rows if u != ME), None)
        en = enemy_name(rows)
        if not en_id or not en:
            continue
        lengths.append(max(r for r, *_ in rows))
        lines, me_side, en_side = [], None, None
        his_turns = {}
        pierce_last, clear_used, smoke_used, cleanse_used = None, False, False, False
        opp4_seen = 0
        for i, (r, u, a, ts) in enumerate(rows):
            me_side, en_side = shotplan.rebuild(lines, ME_NAME, en, 5050, 5050)
            ts = ts or []
            shielded = any("shield absorbs" in t for t in ts)
            for t in ts:
                m = HIT.match(t.strip())
                if not m or shielded:
                    continue
                who, dmg = m.group(1), float(m.group(2))
                if u == ME and who == en and a in IDS:
                    mult = me_side.mult("given", r) * en_side.mult("taken", r)
                    for x in en_side.live("dr", r):
                        mult *= 1 - x[1]
                    name = IDS[a]
                    if name in ("stormblade", "nights"):
                        mult = 1.0
                    if mult > 0.3:
                        my_base.setdefault(name, []).append(dmg / mult)
                elif u == en_id and who == ME_NAME:
                    mult = en_side.mult("given", r) * me_side.mult("taken", r)
                    for x in me_side.live("dr", r):
                        mult *= 1 - x[1]
                    if a not in PIERCE_IDS and mult > 0.3:
                        en_hit.append(dmg / mult)
            if u == en_id:
                tot = sum(float(m.group(1)) for t in ts if (m := ANY_DMG.match(t.strip())))
                his_turns.setdefault(r, [0.0, set()])
                his_turns[r][0] += tot
                his_turns[r][1].add(a)
                # opportunity counting (once per enemy turn)
                if len(his_turns[r][1]) == 1:
                    ready = pierce_last is None or r - pierce_last >= 3
                    me_buffed = any(shotplan.positive(x) and x[2] <= r <= x[3] for x in me_side.tags)
                    me_debuffed = False
                    my_pos = sum(1 for x in me_side.tags if shotplan.positive(x) and x[2] <= r <= x[3])
                    shield_up = bool(me_side.live("shield", r))
                    if ready:
                        opp["pierce"][1] += 1
                        if shield_up:
                            opp["pierce_vs_shield"][1] += 1
                            cond_pierce = True
                    stack = sum(1 for x in me_side.tags if shotplan.positive(x) and x[2] <= r <= x[3]
                                and x[1] not in ("clearimmune", "debuffimmune"))
                    clear_locked = bool(me_side.live("clearimmune", r))
                    if not clear_used and my_pos >= 2:
                        opp["clear_vs_2buffs"][1] += 1
                        cond_clear = True
                    if not clear_used and not clear_locked and stack >= 3:
                        opp["clear_vs_3buffs"][1] += 1
                    if not clear_used and not clear_locked and stack >= 4:
                        opp["clear_vs_4buffs"][1] += 1
                        opp4_seen += 1
                    if not clear_used and me_buffed:
                        opp["clear"][1] += 1
                    if not smoke_used:
                        opp["smoke"][1] += 1
                    opp["setup"][1] += 1
                    en_debuffed = any(not shotplan.positive(x) and x[2] <= r <= x[3] for x in en_side.tags)
                    if not cleanse_used and en_debuffed:
                        opp["cleanse"][1] += 1
                is_pierce = a in PIERCE_IDS or any("pierced" in t or "immunity to buff prevention" in t for t in ts)
                if is_pierce and (pierce_last is None or r - pierce_last >= 3):
                    opp["pierce"][0] += 1; pierce_last = r
                    if me_side.live("shield", r):
                        opp["pierce_vs_shield"][0] += 1
                if a == "clear" and not clear_used:
                    opp["clear"][0] += 1; clear_used = True
                    if sum(1 for x in me_side.tags if shotplan.positive(x) and x[2] <= r <= x[3]) >= 2:
                        opp["clear_vs_2buffs"][0] += 1
                    if sum(1 for x in me_side.tags if shotplan.positive(x) and x[2] <= r <= x[3]
                           and x[1] not in ("clearimmune", "debuffimmune")) >= 3:
                        opp["clear_vs_3buffs"][0] += 1
                    if sum(1 for x in me_side.tags if shotplan.positive(x) and x[2] <= r <= x[3]
                           and x[1] not in ("clearimmune", "debuffimmune")) >= 4:
                        opp["clear_vs_4buffs"][0] += 1
                        clear_wait.append(opp4_seen)
                if (a == SMOKE_ID or any("decreased by up to 70%" in t for t in ts)) and not smoke_used:
                    opp["smoke"][0] += 1; smoke_used = True
                if a == "cleanse" and not cleanse_used:
                    opp["cleanse"][0] += 1; cleanse_used = True
            lines += [f"{r}|{t.strip()}" for t in ts]
        turns = [(r, v[0], v[1]) for r, v in sorted(his_turns.items()) if v[1] - {"wait", "move"}]
        me_end, en_end = shotplan.rebuild(lines, ME_NAME, en, 5050, 5050)
        for r, dmg, acts in turns:
            en_turn.append(dmg)
            if dmg >= 250:  # active damage turn, normalised to base units (his +given, my +taken, my DR)
                mult = en_end.mult("given", r) * me_end.mult("taken", r)
                for x in me_end.live("dr", r):
                    mult *= 1 - x[1]
                en_norm.append(dmg / max(mult, 0.3))
            if dmg < 250:
                opp["setup"][0] += 1
        # value of a debuff package / buff package: extra HP it produced over its live rounds
        me_side, en_side = shotplan.rebuild(lines, ME_NAME, en, 5050, 5050)
        tmed = st.median([d for _, d, _ in turns]) if turns else 0
        for r, dmg, _ in turns:
            extra_t = me_side.mult("taken", r) - 1
            ticks = me_side.total("wound", r) + me_side.total("drain", r)
            if extra_t > 0 or ticks > 0:
                debuff_vals.append(tmed * extra_t + ticks)
            extra_g = en_side.mult("given", r) - 1
            if extra_g > 0:
                buff_vals.append(tmed * extra_g)
    out = {
        "_doc": "Generated by calibrate.py from fights/*.json. Do not hand-edit; rerun after postfight.",
        "fights": len(lengths),
        "my_base": {k: {"median": round(st.median(v)), "n": len(v)} for k, v in sorted(my_base.items())},
        "en_hit": round(st.median(en_hit)) if en_hit else 450,
        "en_turn": round(st.median(en_turn)) if en_turn else 700,
        "en_burst": round(q(en_turn, 0.8)) if en_turn else 1200,
        "en_turn_norm": round(st.median(en_norm)) if en_norm else 800,
        "en_burst_norm": round(q(en_norm, 0.85)) if en_norm else 1500,
        "p": {k: round(v[0] / v[1], 3) if v[1] else 0.0 for k, v in opp.items()},
        "opportunities": opp,
        "debuff_value": round(st.mean(debuff_vals)) if debuff_vals else 400,
        "buff_value": round(st.mean(buff_vals)) if buff_vals else 300,
        "fight_len": st.median(lengths) if lengths else 7,
    }
    out["clear_wait_4buffs"] = clear_wait
    json.dump(out, open(os.path.join(HERE, "calibration.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("_doc",)}, indent=1))


if __name__ == "__main__":
    main()
