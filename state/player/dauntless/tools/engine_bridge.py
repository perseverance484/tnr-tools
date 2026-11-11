#!/usr/bin/env python3
"""Bridge from turn.py to the offline engine harness (harness/pvp_turn): exact one-turn outcomes.

For a set of my candidate bundles it builds one request — my real kit records (harness/pvp_turn/kit), my live
profile, cooldowns from the log, live tags rebuilt by shotplan, and his reply options — runs the pinned engine
(socket syscalls denied) and returns, per bundle, my HP and his HP after my turn and after each of his replies.

His kit is a calibrated stand-in (his records are unknown until he uses them): formula hits sized to the logged
enemy hit/turn/burst (calibration.json), his real-world Night's Testament / Elite Smoke Bomb / Clear when those
are still available to him, and a set-up pair (+35% given on him, +35% taken on me).
Calibration (harness/pvp_turn/CALIBRATION.md): both sides at engine jonin caps, +33% damage-given passive on each
side (gear/keystone/elemental boost; fitted to 10 logged moves, mean error 3.0%; pierce exact).
Returns None when the engine is unavailable; turn.py then falls back to its own simulator.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
HARNESS = os.path.join(REPO, "harness", "pvp_turn")
APP_POINTER = os.path.join(HARNESS, ".engine_app")   # local, untracked: path of the installed engine app
PASSIVE = 33
ITEM_IDS = {"TtYPd-LcXKeK3sMuhq1TP", "6DnJn4x6LWWXtBu7UZybb", "tZTvqYWiAc_OrY64nDvIo", "rsc2uO5QuffXzejfhwF_F",
            "_8HEbybzN5QPX8vUG24Tk", "yVNeLzxHSFkNpTPnlm7yQ", "osJq3k77YPGoFWgof12FQ", "PhP5ZEF5iVa97jcumJ15c"}
BASIC = {"clear", "cleanse", "basicHeal", "defensiveStance", "offensiveStance", "replacementTechnique", "move",
         "basicAttack", "meditate"}
NIGHTS, SMOKE = "osJq3k77YPGoFWgof12FQ", "TtYPd-LcXKeK3sMuhq1TP"


def engine_app():
    app = os.environ.get("TNR_ENGINE_APP")
    if not app and os.path.exists(APP_POINTER):
        app = open(APP_POINTER).read().strip()
    return app if app and os.path.isdir(os.path.join(app, "node_modules")) else None


_CATALOG = None


def _records():
    """Every known jutsu/item record, read offline: kit/catalog.json (all harvested records, built by
    harness/pvp_turn/tools/build_catalog.py; it already folds in kit/records.json and live_overrides.json).
    Built on first use if missing. Never a live lookup."""
    global _CATALOG
    if _CATALOG is None:
        path = os.path.join(HARNESS, "kit", "catalog.json")
        if not os.path.exists(path):
            subprocess.run([sys.executable, os.path.join(HARNESS, "tools", "build_catalog.py")],
                           capture_output=True, text=True, timeout=120)
        try:
            _CATALOG = json.load(open(path))
        except (OSError, ValueError):
            _CATALOG = json.load(open(os.path.join(HARNESS, "kit", "records.json")))
    return _CATALOG


def opponent_kit(user_id):
    """His real equipped kit saved before the fight by opponent_kit.py (kit/opponents/<userId>.json), or None."""
    path = os.path.join(HARNESS, "kit", "opponents", f"{user_id}.json")
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return None


def _profile():
    return json.load(open(os.path.join(HARNESS, "kit", "dauntless_profile.json")))


def _synthetic(base, rid, name, effects, ap, cd=0, target="OPPONENT"):
    r = copy.deepcopy(base)
    r.update({"id": rid, "name": name, "effects": effects, "actionCostPerc": ap, "cooldown": cd, "target": target,
              "method": "SINGLE", "range": 4, "jutsuType": "NORMAL", "bloodlineId": "", "battleUsageType": "BOTH",
              "jutsuWeapon": "NONE", "elementClassification": "None", "villageId": "", "requiredRank": "CHUNIN",
              "jutsuRank": "C", "chakraCost": 0, "staminaCost": 0, "healthCost": 0})
    return r


def _dmg(power):
    return {"type": "damage", "power": power, "powerPerLevel": 0, "rounds": 0, "target": "INHERIT",
            "elements": ["None"], "direction": "offence", "statTypes": ["None"], "calculation": "formula",
            "dmgModifier": 0, "friendlyFire": "ENEMIES", "generalTypes": ["Highest"], "residualModifier": 0,
            "allowBloodlineDamageDecrease": True, "allowBloodlineDamageIncrease": True}


def _tag(t, power, rounds, target):
    return {"type": t, "power": power, "powerPerLevel": 0, "rounds": rounds, "target": target,
            "direction": "offence", "calculation": "percentage", "friendlyFire": "ALL"}


def enemy_kit(cal):
    """Calibrated stand-in kit. Engine at caps + 33%: damage power p -> ~13.4 * p HP; sized so
    hit60 ~ en_hit, hit60+hit40 ~ en_turn_norm, big60+hit40 ~ en_burst_norm."""
    recs = _records()
    base = recs["Lg_thN-MB8FRAr_Agf9tn"]["record"]
    k = 13.4
    hit = cal.get("en_hit", 508) / k
    turn_rest = max(5.0, cal.get("en_turn_norm", 795) / k - hit)
    big = max(hit, cal.get("en_burst_norm", 1440) / k - turn_rest)
    kit = {
        "syn-hit60": _synthetic(base, "syn-hit60", "Hit 60", [_dmg(round(hit))], 60),
        "syn-hit40": _synthetic(base, "syn-hit40", "Hit 40", [_dmg(round(turn_rest))], 40),
        "syn-big60": _synthetic(base, "syn-big60", "Big 60", [_dmg(round(big))], 60, cd=3),
        "syn-light20": _synthetic(base, "syn-light20", "Light 20", [_dmg(round(hit * 0.4))], 20),
        "syn-buff40": _synthetic(base, "syn-buff40", "Self buff", [_tag("increasedamagegiven", 35, 2, "SELF")], 40,
                                 cd=3, target="SELF"),
        "syn-debuff40": _synthetic(base, "syn-debuff40", "Debuff", [_tag("increasedamagetaken", 35, 2, "INHERIT")], 40,
                                   cd=3),
    }
    out = [{"record": r, "kind": "jutsu", "level": 1} for r in kit.values()]
    out.append({"record": recs[NIGHTS]["record"], "kind": "item", "level": 25})
    out.append({"record": recs[SMOKE]["record"], "kind": "item", "level": 25})
    return out


REPLY_ACTIONS = {
    "turn": ["syn-hit60", "syn-hit40"],
    "burst": ["syn-big60", "syn-hit40"],
    "setup": ["syn-buff40", "syn-debuff40", "syn-light20"],
    "pierce": [NIGHTS, "syn-hit60"],
    "clear": ["clear", "syn-hit40"],
    "smoke": [SMOKE, "syn-hit60", "syn-light20"],
}


def reply_name(actions):
    a = list(actions)
    if "pierce" in a:
        return "pierce"
    if "clear" in a:
        return "clear"
    if "smoke" in a:
        return "smoke"
    if "buff" in a:
        return "setup"
    if "burst" in a:
        return "burst"
    return "turn"


TAGMAP = {"taken": "increasedamagetaken", "dr": "decreasedamagetaken", "absorb": "absorb", "lifesteal": "lifesteal",
          "reflect": "reflect", "parry": "parry", "wound": "wound", "drain": "drain", "recoil_self": "recoil",
          "shield": "shield", "debuffimmune": "debuffprevent", "buffblock": "buffprevent",
          "clearimmune": "clearprevent", "stun": "stun", "healcut": "decreaseheal"}
STATIC = {"wound", "drain", "stun", "shield", "debuffprevent", "buffprevent", "clearprevent"}
STATIC_CALC_PCT_POWER = {"parry"}  # schema wants calculation "static" but the power is still a percentage


def effects_from(side, on, by_other, R):
    out = []
    for t in side.tags:
        kind, val, first, last = t[0], t[1], t[2], t[3]
        if last < R:
            continue
        if kind == "given":
            typ, power = ("increasedamagegiven", val * 100) if val > 0 else ("decreasedamagegiven", -val * 100)
        elif kind in TAGMAP:
            typ = TAGMAP[kind]
            power = val if typ in STATIC else val * 100
        else:
            continue
        positive = kind in ("absorb", "lifesteal", "reflect", "parry", "dr", "shield", "debuffimmune", "clearimmune") \
            or (kind == "given" and val > 0)
        e = {"type": typ, "on": on, "by": on if positive else by_other, "power": round(power, 2),
             "rounds": max(1, last - max(first, R) + 1), "fresh": first > R}
        if typ in STATIC or typ in STATIC_CALC_PCT_POWER:
            e["calculation"] = "static"
        if typ in ("debuffprevent", "buffprevent", "clearprevent"):
            e["power"] = 100
        if typ == "shield":
            e["fields"] = {"health": val, "power": val}
        if typ == "absorb":
            e["fields"] = {"poolsAffected": ["Health"]}
        out.append(e)
    return out


def evaluate(bundles_with_targets, me, en, me_pos, en_pos, R, me0, en0, my_used, his_used, replies, cal,
             my_ap=100, his_turn="same", timeout=20):
    """bundles_with_targets: [[(name, actionId, (x, y)), ...]]; replies: [(weight, name)].
    Returns [{bundle, legal, afterMe, replies:[{name, me, him, legal}]}] or None."""
    app = engine_app()
    if not app:
        return None
    recs, prof = _records(), _profile()
    mykit = []
    for aid in sorted({a for b in bundles_with_targets for _, a, _ in b if a not in BASIC} | set(my_used)):
        if aid in recs:
            mykit.append({"record": recs[aid]["record"], "kind": "item" if aid in ITEM_IDS else "jutsu",
                          "level": prof["jutsuLevels"].get(aid, 25)})
    req = {
        "round": R, "hisTurn": his_turn,
        "me": {"id": "me", "hp": me["curHealth"], "x": me_pos[0], "y": me_pos[1], "ap": my_ap, "profile": prof,
               "kit": mykit, "used": [{"actionId": a, "round": r} for a, r in my_used.items()],
               "passives": [{"type": "increasedamagegiven", "power": PASSIVE}]},
        "him": {"id": "him", "hp": en["curHealth"], "x": en_pos[0], "y": en_pos[1], "kit": enemy_kit(cal),
                "used": [{"actionId": a, "round": r} for a, r in his_used.items()],
                "passives": [{"type": "increasedamagegiven", "power": PASSIVE}]},
        "effects": effects_from(me0, "me", "him", R) + effects_from(en0, "him", "me", R),
        "candidates": [[{"actionId": a, "x": t[0], "y": t[1]} for _, a, t in b] for b in bundles_with_targets],
        "replies": [{"name": n, "actions": [{"actionId": a} for a in REPLY_ACTIONS[n]]} for _, n in replies],
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(req, f)
    try:
        out = subprocess.run([os.path.join(HARNESS, "run.sh"), f.name], capture_output=True, text=True,
                             timeout=timeout, env=dict(os.environ, TNR_ENGINE_APP=app))
        if out.returncode != 0:
            if os.environ.get("TNR_ENGINE_DEBUG"):
                print("engine error:", out.stderr[-1500:])
            return None
        if os.environ.get("TNR_ENGINE_DEBUG") and "skipped effects" in out.stderr:
            print([l for l in out.stderr.splitlines() if "skipped effects" in l][0][:600])
        return json.loads(out.stdout)
    except (subprocess.TimeoutExpired, ValueError) as err:
        if os.environ.get("TNR_ENGINE_DEBUG"):
            print("engine error:", repr(err)[:300])
        return None
    finally:
        os.unlink(f.name)


# ---------------------------------------------------------------- replay mode (harness/pvp_turn/engine/replay_sim.ts)
MY_KIT_IDS = ["K0t6Z-Q4lau1jFt8Tkpot", "GiKpip6NxsC8QWlZi6l_R", "zCmYLVL4JYzfhjPXHi9rH", "Lg_thN-MB8FRAr_Agf9tn",
              "Wy7EBGd7gpP96hyumb0Lz", "cvLrFEzeNcRogHqyLv0Ig", "G6MRbppaDZ2a5Wr0GIjH8", "jELEiw5W3N4m2R3oJm3Pk",
              "e2eC-x4UXc5m6QexNbx8w", "qNeccb2eF20oL0Ws-VhKS", "73Sn-ihCNNRwxZ_G_2lTZ", "ou7VyChQ-SFCm8T8yGS7I",
              "g-b0Fs5o8EzQIphq0YIAX", "GAyHRgaa1lkYGhE9WxlRL", "FimDQpYL0LWRv8U81ZP9H"] + sorted(ITEM_IDS)
SKIP = {"wait", "move", "flee"}


def missing_records(rows, me_id):
    """Logged action ids with no record in the offline catalog (a catalog gap: refresh harvests between fights and
    rerun build_catalog.py; never fetched mid-fight)."""
    recs = _records()
    return sorted({a for r, u, a, _ in rows if u != me_id and a not in SKIP and a not in BASIC and a not in recs})


def his_kit_source(en_id):
    """'real' when his equipped kit was saved before the fight, else 'estimated' (calibrated stand-in)."""
    return "real" if opponent_kit(en_id) else "estimated"


def _his_kit(rows, en_id, cal):
    recs = _records()
    opp = opponent_kit(en_id)
    levels = dict((opp or {}).get("jutsuLevels", {}))
    ids = set((opp or {}).get("jutsu", [])) | set((opp or {}).get("items", []))
    ids |= {a for r, u, a, _ in rows if u == en_id and a in recs}   # anything he used counts, equipped list or not
    kit = [{"record": recs[a]["record"], "kind": recs[a].get("kind") or ("item" if recs[a]["record"].get("itemType") else "jutsu"),
            "level": levels.get(a, 25)} for a in sorted(ids) if a in recs]
    if not opp:
        # no pre-fight kit: his unseen jutsu are unknown, so the calibrated stand-in fills the reply set (flagged
        # ESTIMATED by turn.py). With a saved kit there is no stand-in at all.
        kit += [k for k in enemy_kit(cal) if k["record"]["id"] not in ids]
    return kit


def _replay_request(rows, me_id, en_id, me, en, me_pos, en_pos, R, his_turn, cal):
    recs, prof = _records(), _profile()
    his_kit = _his_kit(rows, en_id, cal)
    log = [{"round": r, "actor": "me" if u == me_id else "him", "actionId": a}
           for r, u, a, _ in rows if u in (me_id, en_id)]
    return {
        "round": R, "hisTurn": his_turn,
        "me": {"id": "me", "hp": me["curHealth"], "x": me_pos[0], "y": me_pos[1], "profile": prof,
               "kit": [{"record": recs[a]["record"], "kind": "item" if a in ITEM_IDS else "jutsu",
                        "level": prof["jutsuLevels"].get(a, 25)} for a in MY_KIT_IDS if a in recs],
               "passives": [{"type": "increasedamagegiven", "power": PASSIVE}]},
        "him": {"id": "him", "hp": en["curHealth"], "x": en_pos[0], "y": en_pos[1], "kit": his_kit,
                "passives": [{"type": "increasedamagegiven", "power": PASSIVE}]},
        "log": log,
    }


def _run(req, timeout):
    app = engine_app()
    if not app:
        return None
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(req, f)
    try:
        out = subprocess.run([os.path.join(HARNESS, "run.sh"), f.name, "replay_sim.ts"], capture_output=True,
                             text=True, timeout=timeout, env=dict(os.environ, TNR_ENGINE_APP=app))
        if out.returncode != 0:
            if os.environ.get("TNR_ENGINE_DEBUG"):
                print("engine error:", out.stderr[-1200:])
            return None
        d = json.loads(out.stdout)
        if os.environ.get("TNR_ENGINE_DEBUG") and d.get("results"):
            print("reply failures:", [r.get("replyFail") for r in d["results"]][:2], "counts:", [r.get("replyCount") for r in d["results"]])
        return d
    except (subprocess.TimeoutExpired, ValueError) as err:
        if os.environ.get("TNR_ENGINE_DEBUG"):
            print("engine error:", repr(err)[:300])
        return None
    finally:
        os.unlink(f.name)


def replay_list(rows, me_id, en_id, me, en, me_pos, en_pos, R, his_turn, cal, timeout=8):
    """Engine state after replaying the log: {ap, available:[{id,name,cost}], replayIssues}."""
    req = _replay_request(rows, me_id, en_id, me, en, me_pos, en_pos, R, his_turn, cal)
    req["mode"] = "list"
    return _run(req, timeout)


def replay_eval(rows, me_id, en_id, me, en, me_pos, en_pos, R, his_turn, cal, bundles_with_targets, timeout=10):
    req = _replay_request(rows, me_id, en_id, me, en, me_pos, en_pos, R, his_turn, cal)
    req["mode"] = "eval"
    req["candidates"] = [[{"actionId": a, "x": t[0], "y": t[1]} for _, a, t in b] for b in bundles_with_targets]
    req["replyCap"] = 40
    return _run(req, timeout)
