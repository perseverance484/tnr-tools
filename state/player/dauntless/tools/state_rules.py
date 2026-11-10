#!/usr/bin/env python3
"""Generic state rules for every opponent (director, 2026-11-10: "You should have a predictor going for all enemies
regardless for generic things like if IDG exceeds X amount do Y. If Absorb exceeds X amount do Y. If I get stunned
do this. And so on").

Feed it the battle log's appliedEffects lines (copy `combat.getBattleEntries` *.appliedEffects.*.txt into a file,
newest first or any order) plus the round, and it rebuilds the live tag state on both sides, then fires the rules
below, highest priority first. Combine with enemy_model.py (opponent-specific habits) and cd_plan.py (legality).

Usage: state_rules.py LOGFILE ROUND ENTRY_ROUND_FILE? --me dauntless --enemy NAME [--my-hp N --en-hp N]
  LOGFILE lines: "<round>|<effect text>"  (round = battleRound of the entry)
"""
import argparse
import re

PCT = r"by up to ([\d.]+)%"


def parse(lines, me, en):
    st = {k: [] for k in ["en_idg", "en_dr", "en_absorb", "en_lifesteal", "en_reflect", "me_idt", "me_dg_down",
                          "me_recoil", "me_wound", "me_drain", "en_taken_up", "en_given_down", "me_dr", "me_absorb"]}
    flags = set()
    for line in lines:
        if "|" not in line:
            continue
        r, t = line.split("|", 1)
        r = int(r)
        rounds = re.search(r"next (\d+) rounds?", t)
        n = int(rounds.group(1)) if rounds else 1
        live = (r + 1, r + n)  # most tags start next round
        p = re.search(PCT, t)
        v = float(p.group(1)) / 100 if p else 0
        who_en = t.startswith(en)
        who_me = t.startswith(me)
        if "cleared of all positive" in t:  # Clear: drop that side's buffs applied so far (lines are chronological)
            keys = ("en_idg", "en_dr", "en_absorb", "en_lifesteal", "en_reflect") if who_en else ("me_dr", "me_absorb")
            for k in keys:
                st[k] = [(v_, (a_, b_)) for v_, (a_, b_) in st[k] if a_ > r + 1 or b_ < r]  # keep only future-dated
                st[k] = []
            if who_en:
                flags = {f for f in flags if f[0] not in ("en_immune", "en_shield")}
            continue
        if "cleared of all negative" in t:  # Cleanse
            keys = ("me_idt", "me_dg_down", "me_recoil", "me_wound", "me_drain") if who_me else ("en_taken_up", "en_given_down")
            for k in keys:
                st[k] = []
            continue
        if who_en and "damage given" in t and "increased" in t:
            st["en_idg"].append((v, live))
        elif who_en and "damage taken" in t and "decreased" in t:
            st["en_dr"].append((v, live))
        elif who_en and "damage taken" in t and "increased" in t:
            st["en_taken_up"].append((v, live))
        elif who_en and "damage given" in t and "decreased" in t:
            st["en_given_down"].append((v, live))
        elif who_en and "will absorb" in t:
            st["en_absorb"].append((float(re.search(r"absorb up to ([\d.]+)%", t).group(1)) / 100, live))
        elif who_en and "will steal" in t:
            st["en_lifesteal"].append((float(re.search(r"steal ([\d.]+)%", t).group(1)) / 100, live))
        elif who_en and "will reflect" in t:
            st["en_reflect"].append((float(re.search(r"reflect ([\d.]+)%", t).group(1)) / 100, live))
        elif who_en and "cannot be debuffed" in t:
            flags.add(("en_immune", live[0] - 1 if "next" not in t else live[0], live[1]))
        elif who_en and "cannot be cleared" in t:
            flags.add(("en_clearprevent", live[0], live[1]))
        elif who_en and "shield with" in t:
            flags.add(("en_shield", r, r + n - 1))
        elif who_me and "stunned" in t:
            flags.add(("me_stunned", r, r + n))
        elif who_me and "will recoil" in t:
            st["me_recoil"].append((float(re.search(r"recoil ([\d.]+)%", t).group(1)) / 100, live))
        elif who_me and "wound damage for" in t:
            st["me_wound"].append((float(re.search(r"take ([\d.]+) wound", t).group(1)), live))
        elif who_me and "will be drained" in t:
            st["me_drain"].append((float(re.search(r"drained ([\d.]+)", t).group(1)), live))
        elif who_me and "damage taken" in t and "increased" in t:
            st["me_idt"].append((v, live))
        elif who_me and "damage given" in t and "decreased" in t:
            st["me_dg_down"].append((v, live))
        elif "marked the ground with recoil" in t and who_me:
            flags.add(("en_on_my_recoil", r, r + n - 1))
        elif t.startswith(en) and "marked the ground with recoil" in t:
            flags.add(("me_on_their_recoil", r, r + n - 1))
    return st, flags


def total(st, key, rnd, mult=True):
    vals = [v for v, (a, b) in st[key] if a <= rnd <= b]
    if not mult:
        return sum(vals)
    m = 1.0
    for v in vals:
        m *= 1 + v
    return m - 1


def active(flags, name, rnd):
    return any(f == name and a <= rnd <= b for f, a, b in flags)


RULES = [
    # (priority, condition(ctx), advice)
    (100, lambda c: c["my_hp"] and c["my_hp"] < 1200 and c["en_idg"] > 0.3,
     "LETHAL RISK: their stack is live and I'm low. Survive first: instant shield (Chakra Shield) / Subaku / Danse "
     "seal / Smoke for next round; or kill now if my instant damage >= their HP."),
    (95, lambda c: c["en_hp"] and c["en_hp"] < 800,
     "KILL WINDOW: their HP < 800. Pierce (Stormblade 707 / Night's 631) or best boosted hit; ignore setup."),
    (90, lambda c: c["en_idg"] >= 0.6 and not c["en_clearprevent"],
     "Their damage-given stack >= +60%: Clear it this turn (Clear is not a debuff; immunity doesn't stop it). If they "
     "were debuff-immune, Smoke now lands too."),
    (88, lambda c: c["en_idg"] >= 0.6 and c["en_clearprevent"],
     "Big stack but Clear-prevented (Dr. Kim's): recoil (Fury, if their pierce is down) + absorb, or Danse seal + "
     "instant shield; Clear next round."),
    (85, lambda c: c["me_stunned"],
     "I'm stunned: 80 AP. Plan 60+20 / 40+40 / 40+20+20 (Cleanse does not remove stun)."),
    (80, lambda c: c["me_recoil"] >= 0.3,
     "Recoil on me >= 30%: deal pierce or drain (no recoil), or Cleanse; don't basic/burst into it."),
    (78, lambda c: c["en_absorb"] >= 0.3 or c["en_lifesteal"] >= 0.35,
     "Their absorb/lifesteal >= 30-35%: Severed Pulse (-50% healing) before the big hit; drains and pierce dodge absorb "
     "less; Clear strips both."),
    (75, lambda c: c["en_dr"] >= 0.4 or c["en_shield"],
     "Their DR >= 40% or shield: pierce (destroys shields, ignores DR) or drain; don't spend boosted hits now."),
    (72, lambda c: c["me_debuffs"] >= 2 or c["me_wound_drain"] >= 300,
     "2+ debuffs on me or >= 300/round wound+drain: Cleanse (check clear-family lock)."),
    (70, lambda c: c["en_immune"],
     "They are debuff-immune this round: no Subaku/Smoke/Disaster/Severed; seal and Clear still work."),
    (65, lambda c: c["en_reflect"] >= 0.3,
     "Their reflect >= 30%: pierce reflects too; set up or Clear instead of feeding big hits."),
    (60, lambda c: c["en_idg"] >= 0.3 and c["en_idg"] < 0.6,
     "Their stack is building (+30-60%): recoil ground (Fury) or Seal of Nullification so the next layer can't land."),
    (50, lambda c: c["my_absorb_low"],
     "My absorb is down: refresh (Rebirth or Chakra Shield, never both, cap 60)."),
    (40, lambda c: True,
     "No threat: set up the swing (Ember + Overflow) or cash in live buffs."),
]


def build_ctx(lines, R, me, en, my_hp, en_hp):
    st, flags = parse(lines, me, en)

    def live_for(who, word):
        for l in lines:
            r, t = l.split("|", 1)
            m = re.search(r"next (\d+)", t)
            if word in t and t.startswith(who) and int(r) + 1 <= R <= int(r) + (int(m.group(1)) if m else 1):
                return True
        return False

    my_absorb_live = live_for(me, "absorb")
    c = {
        "my_hp": my_hp, "en_hp": en_hp,
        "my_given_live": live_for(me, "damage given [all damage] is increased"),
        "en_taken_live": live_for(en, "damage taken [all damage] is increased"),
        "en_idg": total(st, "en_idg", R), "en_dr": 1 - (1 / (1 + total(st, "en_dr", R))) if total(st, "en_dr", R) else 0,
        "en_absorb": total(st, "en_absorb", R, False), "en_lifesteal": total(st, "en_lifesteal", R, False),
        "en_reflect": total(st, "en_reflect", R, False),
        "me_recoil": max([v for v, (x, y) in st["me_recoil"] if x <= R <= y], default=0),
        "me_stunned": active(flags, "me_stunned", R), "en_immune": active(flags, "en_immune", R),
        "en_clearprevent": active(flags, "en_clearprevent", R), "en_shield": active(flags, "en_shield", R),
        "me_debuffs": sum(1 for k in ("me_idt", "me_dg_down", "me_recoil", "me_wound", "me_drain")
                          if any(x <= R <= y for _, (x, y) in st[k])),
        "me_wound_drain": total(st, "me_wound", R, False) + total(st, "me_drain", R, False),
        "my_absorb_low": not my_absorb_live,
        "me_wound_live": any(x <= R <= y for _, (x, y) in st["me_wound"]),
    }
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logfile")
    ap.add_argument("round", type=int)
    ap.add_argument("--me", default="dauntless")
    ap.add_argument("--enemy", required=True)
    ap.add_argument("--my-hp", type=float, default=0)
    ap.add_argument("--en-hp", type=float, default=0)
    a = ap.parse_args()
    lines = [l.strip() for l in open(a.logfile) if l.strip()]
    R = a.round
    c = build_ctx(lines, R, a.me, a.enemy, a.my_hp, a.en_hp)
    print(f"round {R} state: enemy +given {c['en_idg']:+.0%}, enemy DR ~{c['en_dr']:.0%}, enemy absorb "
          f"{c['en_absorb']:.0%}, lifesteal {c['en_lifesteal']:.0%}, reflect {c['en_reflect']:.0%}; me: stunned="
          f"{c['me_stunned']}, recoil {c['me_recoil']:.0%}, debuffs {c['me_debuffs']}, wound+drain "
          f"{c['me_wound_drain']:.0f}/r; enemy immune={c['en_immune']}, clear-prevent={c['en_clearprevent']}")
    for pr, cond, adv in sorted(RULES, key=lambda x: -x[0]):
        try:
            if cond(c):
                print(f"  [{pr}] {adv}")
        except Exception:
            pass


if __name__ == "__main__":
    main()
