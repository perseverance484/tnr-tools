"""planner2's numeric engine vs shotplan's tag simulator: same HP after my turn on every exam state for a sample of
legal bundles, and after his reply for every option (python, no live calls). Run: python3 tests/test_planner2.py"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import exam, planner2 as p2, shotplan, value_model  # noqa: E402
p2.SOURCE_EXACT = False      # compare the core shared with shotplan; the source-only details are checked by engine_fit
p2._ENGINE_BASES = {}     # and the shared calibrated bases
p2.ENGINE_STATE = False   # and the same state (the text rebuild shotplan shares; engine_check covers the engine state)
p2._OPP_SCALES = {}      # and no per-opponent log scales (shotplan has none)


def states():
    for bid, (enemy, loadout) in exam.EXAM.items():
        for r, b, e, his, hp in exam.turns(bid, enemy):
            path = os.path.join(HERE, f"_p2_{bid}_{r}.txt")
            open(path, "w").write(json.dumps(b) + "\n" + json.dumps(e) + "\n")
            try:
                yield p2.build(type("A", (), dict(file=path, enemy=enemy, loadout=loadout)))
            finally:
                os.unlink(path)


def test_parity():
    rng = random.Random(1)
    n = bad = 0
    gk = None
    for P, info in states():
        R, sme, sen = info["R"], info["sme"], info["sen"]
        bundles = p2.legal_bundles(info["st"], R, info["ap"], info["d0"], info["st"]["loadout"], P.me0, P.en0)
        if gk is None:
            gk = value_model.generic_kit(value_model.load_cal())
        for bnd in rng.sample(bundles, min(40, len(bundles))):
            m, e = value_model.copy_side(sme), value_model.copy_side(sen)
            if "cleanse" in bnd:
                m.tags = [x for x in m.tags if shotplan.positive(x) or shotplan.ground(x)]
            shotplan.run_turn(m, e, list(bnd), shotplan.MINE, R, True)
            m.hp, e.hp = min(m.hp, 5050), min(e.hp, 5050)
            pm, pe = P.me0.copy().passives(), P.en0.copy().passives()   # shotplan has no bloodline passives
            if "cleanse" in bnd:
                pm.wipe(p2.NEGK)
            p2.run_turn(pm, pe, [P.my_kit[x] for x in bnd], 0, 5050, 5050)
            # his reply (each generic option) in the next round on both engines
            for opt in (["turn"], ["buff", "debuff", "light"], ["clear", "light"], ["smoke", "light"], ["pierce", "light"]):
                m2, e2 = value_model.copy_side(m), value_model.copy_side(e)
                shotplan.run_turn(e2, m2, opt, gk, R + 1, False)
                pm2, pe2 = pm.copy(), pe.copy()
                p2.run_turn(pe2, pm2, [p2.compile_spec(gk[o], False) for o in opt], 1, 1e9, 1e9)
                n += 1
                if abs(m2.hp - pm2.hp) > 0.5 or abs(e2.hp - pe2.hp) > 0.5:
                    bad += 1
                    print("MISMATCH", R, bnd, opt, round(m2.hp), round(pm2.hp), round(e2.hp), round(pe2.hp))
    print(f"parity: {n - bad}/{n} lines match")
    assert bad == 0


if __name__ == "__main__":
    test_parity()
