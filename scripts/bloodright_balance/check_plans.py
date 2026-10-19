#!/usr/bin/env python3
"""Check that scoring only the top candidate schedules matches scoring every distinct schedule."""
import json, random, sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
import evaluator as E

TAGS = ["damage", "increasedamagegiven", "decreasedamagegiven", "increasedamagetaken", "decreasedamagetaken",
        "afterburn", "lifesteal", "reflect", "pierce", "absorb", "heal", "drain", "poison", "consume", "vamp"]
rng = random.Random(11)
kits = E.load_kits()
worst = 0.0
for slug in kits:
    ev = E.Evaluator(slug, kits)
    cands = ev.candidate_plans()
    allp = ev._all_plans
    m = ev.mirror()
    misses = 0
    for _ in range(25):
        b = {t: rng.choice([2, 5, 10]) for t in rng.sample(TAGS, 4)}
        b["damage"] = rng.choice([0.4, 1.6])
        k2 = [E.apply_bonuses(j, b, ev.elements) for j in ev.base_kit]
        for pr in (0.5, 1.0, 1.5):
            full = max(E.simulate([k2, ev.base_kit], [p, m], pr)[0] for p in allp)
            part = max(E.simulate([k2, ev.base_kit], [p, m], pr)[0] for p in cands)
            if full - part > 1e-6:
                misses += 1
                worst = max(worst, (full - part) / E.WEIGHT)
    print(f"{slug:28} plans {len(allp):5} kept {len(cands):3} misses {misses}")
print("worst Weight error", round(worst, 4))
