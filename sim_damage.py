"""TNR damage core - original implementation from extracted facts (COMBAT_FACTS.md).
Validated against the repo's own damage_formula.test.ts expectations."""
import math

CFG = dict(stats_scaling=1.0, base_hits=10, curve=1.6, amplitude=0.75,
           ep_normalization=40, gen_weight=2.0, advantage_min=0.01, advantage_max=10.0)
DMG_REDUCTION_CAP = 0.9
OOC_BASE_INC = 60   # percentage points, pre-battle increase pool
OOC_BASE_DR  = 50   # percentage points, pre-battle DR pool
HP_PER_LVL = 50

def calc_hp(level): return 100 + HP_PER_LVL * (level - 1)

def power_effect(atk, dfn, attacker_level, effect_power, cfg=CFG):
    ep_scale = effect_power / max(1, cfg["ep_normalization"])
    baseline = calc_hp(attacker_level) / max(1, cfg["base_hits"])
    adv = 1.0
    if atk > 0 or dfn > 0:
        ratio = atk / max(1, dfn)
        raw = 1.0 + cfg["amplitude"] * (ratio ** cfg["curve"] - 1.0)
        adv = min(cfg["advantage_max"], max(cfg["advantage_min"], raw))
    return baseline * ep_scale * adv

def damage_calc(effect, origin, target, cfg=CFG):
    """effect: dict(power, calculation, statTypes, generalTypes, highestOffence?,
    targetHighestDefence?, residualModifier?, dmgModifier?, castThisRound?)
    origin/target: dict of stats + level + highestGenerals"""
    power = effect["power"] + effect.get("level", 0) * effect.get("powerPerLevel", 0)
    dmg = power
    if effect.get("calculation") == "formula" and origin is not None:
        atk_s = dfn_s = 0.0
        for st in effect.get("statTypes", []):
            if st == "Highest":
                a, b = effect.get("highestOffence"), effect.get("targetHighestDefence")
                if not a or not b: continue
            else:
                a, b = st.lower() + "Offence", st.lower() + "Defence"
            if a in origin and b in target:
                atk_s += math.sqrt(max(0, origin[a]))
                dfn_s += math.sqrt(max(0, target[b]))
        atk_g = dfn_g = 0.0
        gens = effect.get("generalTypes", [])
        resolved = []
        for g in gens:
            if g == "Highest": resolved += origin.get("highestGenerals", [])
            else: resolved.append(g.lower())
        for g in resolved:
            if g in origin and g in target:
                atk_g += math.sqrt(max(0, origin[g]))
                dfn_g += math.sqrt(max(0, target[g]))
        atk = cfg["stats_scaling"] * atk_s + cfg["gen_weight"] * atk_g
        dfn = cfg["stats_scaling"] * dfn_s + cfg["gen_weight"] * dfn_g
        dmg = power_effect(atk, dfn, origin["level"], power, cfg)
    if not effect.get("castThisRound", True) and effect.get("residualModifier"):
        dmg *= effect["residualModifier"]
    if effect.get("dmgModifier"):
        dmg *= effect["dmgModifier"]
    return dmg

def apply_dr(damage, fraction): return damage * max(0.0, 1.0 - fraction)

def compute_damage_packet(raw, boosts_pct=(), dr_pct=(), static_inc=0.0, static_dr=0.0,
                          gear_inc_pts=0.0, gear_dr_pts=0.0):
    """Staged pipeline per process.ts computeDamagePacket (bloodline/keystone lanes omitted;
    add when a scenario uses them). boosts/dr are lists of percentage powers with ratio already applied."""
    damage = raw
    inc_points = OOC_BASE_INC + gear_inc_pts
    damage *= 1 + inc_points / 100
    for p in boosts_pct:
        damage *= 1 + p / 100
    base_after_boosts = damage
    dr_points = OOC_BASE_DR + gear_dr_pts
    damage = apply_dr(damage, dr_points / 100)
    for p in dr_pct:
        damage = apply_dr(damage, abs(p) / 100)
    base_after_system_dr = apply_dr(base_after_boosts, OOC_BASE_DR / 100)
    min_damage = base_after_system_dr * (1 - DMG_REDUCTION_CAP)
    damage = max(damage, min_damage)
    damage += static_inc
    damage = max(min_damage, damage - static_dr)
    return damage

if __name__ == "__main__":
    mk = lambda lvl=50, base=1000: dict(level=lvl, highestGenerals=["strength"],
        **{s+t: base for s in ("ninjutsu","genjutsu","taijutsu","bukijutsu") for t in ("Offence","Defence")},
        **{g: base for g in ("strength","intelligence","willpower","speed")})
    eff = dict(power=40, calculation="formula", statTypes=["Ninjutsu"], generalTypes=[], castThisRound=True)

    # Fixture 1: static returns power
    assert damage_calc(dict(power=50, calculation="static"), mk(), mk()) == 50
    # Fixture 2: no origin returns power
    assert damage_calc(dict(power=30, calculation="formula"), None, mk()) == 30
    # Fixture 3: level scaling 5050/100
    r = damage_calc(eff, mk(100), mk()) / damage_calc(eff, mk(1), mk())
    assert abs(r - 5050/100) < 0.5, r
    # Fixture 4: equal stats L50 EP40 -> 255
    d = damage_calc(eff, mk(50), mk(50))
    assert abs(d - 255) < 0.5, d
    # Fixture 5: equal buffs cancel
    a=mk(); b=mk(); a["ninjutsuOffence"]*=1.3; b["ninjutsuDefence"]*=1.3
    assert abs(damage_calc(eff, a, b) - damage_calc(eff, mk(), mk())) < 0.5
    # Fixture 6: EP linearity 80/40 = 2.0
    e80 = dict(eff, power=80)
    assert abs(damage_calc(e80, mk(), mk()) / damage_calc(eff, mk(), mk()) - 2.0) < 1e-5
    print("ALL 6 REPO FIXTURES PASS")

    # Boss reference: L110 attacker, 60 EP, capped stats both sides even
    boss = mk(110, 450000); boss.update({g:200000 for g in ("strength","intelligence","willpower","speed")})
    player = mk(100, 450000); player.update({g:200000 for g in ("strength","intelligence","willpower","speed")})
    e = dict(power=60, calculation="formula", statTypes=["Ninjutsu"], generalTypes=["Highest"], castThisRound=True)
    raw = damage_calc(e, boss, player)
    print("boss L110 60EP raw (even capped stats):", round(raw,1))
    print("after packet (no in-battle mods):", round(compute_damage_packet(raw),1))
    print("with player 2x35% DDT:", round(compute_damage_packet(raw, dr_pct=[35,35]),1))
    print("with boss +60%% IDG passive too:", round(compute_damage_packet(raw, boosts_pct=[60], dr_pct=[35,35]),1))
