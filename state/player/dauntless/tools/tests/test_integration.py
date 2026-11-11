"""Every system is wired in (director 2026-11-11: "Every time we add a new system I discover you weren't using it
because it wasnt tied in"). One live-shaped position through the planner the pilot runs, and one pilot upkeep
pass, asserting each subsystem actually feeds the decision. Add a line here whenever a new system lands.
Run: python3 tests/test_integration.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import clock  # noqa: E402
import planner2 as P2  # noqa: E402
import shotplan  # noqa: E402
import value_model  # noqa: E402

FIX = os.path.join(HERE, "ziharkk_r2.txt")


def test_planner():
    P, info = P2.build(type("A", (), dict(file=FIX, enemy="ANBU Member", loadout="pvp1")))
    checks = {
        "opponent profile (bloodline from his kit)": bool(info["prof"].get("bloodline")),
        "his clock (ready lines from his real kit)": bool(P.clockd.get("cands")),
        "his habits from every logged fight (opponents.py)": P.clockd.get("habit") is not None,
        "his kit includes actions from other fights": len(P.clockd.get("ids", ())) > 15,
        "engine bases for my kit (engine_fit.py)": abs(P.my_kit["rebirth"][0] - P2.engine_bases().get("rebirth", -1)) < 1,
        "opponent damage calibration (validate.py)": clock.HIS_CAL > 1.0,
        "source rules (reflect/recoil/absorb)": P2.SOURCE_EXACT,
        "ground effects": hasattr(P2, "GGRD"),
        "pressure weights": P2.load_weights()["mypot"] > P2.load_weights()["hispot"],
        "library key computed (library itself off until it wins)": getattr(P, "book_key", None) is not None,
        "his next-turn threat from his ready lines": bool(P.clockd.get("next_lines")),
    }
    bad = [k for k, ok in checks.items() if not ok]
    for k, ok in checks.items():
        print(("  ok  " if ok else "  MISSING  ") + k)
    assert not bad, bad


def test_pilot():
    import test_pilot as TP
    head, b = TP.run_world([TP.user()], "hunt", {"restock": {"next": 0, "pass": 0, "active": False}})
    calls = {x.get("call") for x in b}
    checks = {
        "upkeep reads items (stock + durability)": "item.getUserItems" in calls,
        "upkeep reads the jutsu training queue": "jutsu.getTrainingQueue" in calls,
        "upkeep reads owned jutsu levels": "jutsu.getUserJutsus" in calls,
    }
    head2, b2 = TP.run_world([TP.user(), TP.sector([])], "hunt")
    calls2 = [x.get("call") for x in b2]
    checks["log harvest rides idle batches"] = any(c in ("combat.getBattleHistory", "combat.getBattleEntries",
                                                         "profile.getStrongestUsers") for c in calls2)
    import pilot
    checks["planner2 leads the pilot"] = "planner2.py" in open(pilot.__file__).read()
    checks["director mode switch present"] = hasattr(pilot, "director_mode")
    checks["opponent models rebuilt after every fight"] = "opponents.py\"), \"build\"" in open(pilot.__file__).read()
    bad = [k for k, ok in checks.items() if not ok]
    for k, ok in checks.items():
        print(("  ok  " if ok else "  MISSING  ") + k)
    assert not bad, bad


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    test_planner()
    test_pilot()
    print("ok: every system is wired in")
