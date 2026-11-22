#!/usr/bin/env python3
"""The combat engine map (docs/combat-engine/, read from the game source) as a module the planner, replay and
critique tools load instead of hardcoding engine facts.

    import combat_map as CM
    CM.CAP_ABSORB, CM.CAP_REFLECT, CM.CAP_LEECH, CM.CAP_AFTERBURN    # 0.6 each today, from rules.json
    CM.polarity("absorb")        # "positive" (Clear removes) / "negative" (Cleanse removes) / "neutral"
    CM.removed_by("wound")       # "cleanse"
    CM.prevented_by("lifesteal") # ["healprevent"]
    CM.edges("absorb", "incoming")  # [(other tag, kind, note), ...]

CLI:
    python3 combat_map.py TAG            what the engine does with TAG, its timing and its links
    python3 combat_map.py --check        the planner's hardcoded tables against the map (exit 1 on drift)

The map wins over a hardcoded guess. When the check fails, fix the planner table or, if the map is out of date
with the game, regenerate the map (docs/combat-engine/README.md) and say which in the commit.
Set TNR_COMBAT_MAP to another docs/combat-engine directory to read a different copy.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAP_DIR = os.environ.get("TNR_COMBAT_MAP") or os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "docs",
                                                                          "combat-engine"))

# The planner's own effect kinds (planner2.KIND, shotplan, turn) -> the engine tag each one models.
# "given" splits by sign; "recoil_self" is recoil on its caster. Kinds missing here are planner-only bookkeeping.
KIND_TAG = {
    "given+": "increasedamagegiven", "given-": "decreasedamagegiven", "taken": "increasedamagetaken",
    "dr": "decreasedamagetaken", "absorb": "absorb", "lifesteal": "lifesteal", "reflect": "reflect",
    "parry": "parry", "shield": "shield", "debuffimmune": "debuffprevent", "clearimmune": "clearprevent",
    "buffblock": "buffprevent", "wound": "wound", "drain": "drain", "recoil": "recoil", "recoil_self": "recoil",
    "healcut": "decreaseheal", "stun": "stun", "afterburn": "afterburn",
}

# Used only when the map files are missing (a stripped copy of the tools): the values the map held at 29cd91b.
_FALLBACK_CAPS = {"absorb": 0.6, "reflect": 0.6, "lifesteal_vamp": 0.6, "afterburn": 0.6, "damage_reduction": 0.9,
                  "parry_pct": 100}


def _load(name):
    path = os.path.join(MAP_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


_TAGS = _load("tags.json")
_EDGES = _load("interactions.json")
_RULES = _load("rules.json")
AVAILABLE = bool(_TAGS and _EDGES and _RULES)
TAGS = (_TAGS or {}).get("tags", {})
GAME_COMMIT = (_TAGS or {}).get("pinned_game_commit")


def rule(group, key):
    """A numeric engine constant from rules.json (falls back to the 29cd91b value if the map is missing)."""
    if _RULES and key in _RULES.get(group, {}):
        return _RULES[group][key]["value"]
    if key in _FALLBACK_CAPS:
        return _FALLBACK_CAPS[key]
    raise KeyError(f"{group}.{key} is not in the combat engine map")


CAP_ABSORB = rule("caps", "absorb")
CAP_REFLECT = rule("caps", "reflect")
CAP_LEECH = rule("caps", "lifesteal_vamp")       # lifesteal and vamp share it
CAP_AFTERBURN = rule("caps", "afterburn")
CAP_PARRY = rule("caps", "parry_pct") / 100.0
DR_CAP = rule("caps", "damage_reduction")        # reductions never take more than this share of a hit


def tag(name):
    if name not in TAGS:
        raise KeyError(f"{name} is not a combat tag in the map ({len(TAGS)} tags)")
    return TAGS[name]


def polarity(name):
    return tag(name)["polarity"]


def removed_by(name):
    return {"positive": "clear", "negative": "cleanse"}.get(polarity(name))


def prevented_by(name):
    return list(tag(name).get("prevented_by", []))


def live_from(name):
    return tag(name).get("live_from")


def edges(name, direction="both", kind=None):
    """[(other tag, kind, note)] for links into ("incoming"), out of ("outgoing") or around ("both") a tag."""
    out = []
    for e in (_EDGES or {}).get("edges", []):
        if kind and e["kind"] != kind:
            continue
        if direction in ("outgoing", "both") and e["from"] == name:
            out.append((e["to"], e["kind"], e.get("note", "")))
        if direction in ("incoming", "both") and e["to"] == name:
            out.append((e["from"], e["kind"], e.get("note", "")))
    return out


def kind_polarity(kind):
    """Polarity of a planner kind ("given+", "absorb", ...), or None for planner-only kinds."""
    t = KIND_TAG.get(kind)
    return polarity(t) if t else None


def check_planner():
    """Every place the planner hardcodes engine facts, against the map. Returns a list of mismatches."""
    sys.path.insert(0, HERE)
    import engine_bridge
    import planner2 as P2
    import shotplan
    import turn
    bad = []
    if not AVAILABLE:
        return [f"combat engine map not found at {MAP_DIR}"]
    # 1. which side Clear and Cleanse strip (planner2.POSK / NEGK, shotplan.POSITIVE, engine_bridge's positive list)
    inv = {v: k for k, v in P2.KIND.items()}
    for idx in P2.POSK + P2.NEGK:
        kind = inv.get(idx) or {P2.GUP: "given+", P2.GDN: "given-"}.get(idx)
        if not kind or kind not in KIND_TAG:
            continue
        want = "positive" if idx in P2.POSK else "negative"
        got = kind_polarity(kind)
        # clearprevent is neutral in the engine; the planner lists it as positive but only ever reads it to block
        # Clear, so neither side's removal of it is ever modelled. Accept that one.
        if got != want and not (kind == "clearimmune" and got == "neutral"):
            bad.append(f"planner2 lists {kind} ({KIND_TAG[kind]}) as {want}; the engine has it {got}")
    for kind in shotplan.POSITIVE:
        got = kind_polarity(kind)
        if got not in ("positive",) and not (kind == "clearimmune" and got == "neutral"):
            bad.append(f"shotplan.POSITIVE has {kind} ({KIND_TAG.get(kind)}); the engine has it {got}")
    # 2. the planner's kind -> engine tag names (engine_bridge.TAGMAP) are real tags with the same meaning
    for kind, t in engine_bridge.TAGMAP.items():
        if t not in TAGS:
            bad.append(f"engine_bridge.TAGMAP maps {kind} to {t}, which is not a combat tag")
        elif KIND_TAG.get(kind) != t:
            bad.append(f"engine_bridge.TAGMAP maps {kind} to {t}; combat_map.KIND_TAG says {KIND_TAG.get(kind)}")
    # 3. hostile ground kinds really are debuffs
    for t in turn.HOSTILE_KINDS:
        if t in TAGS and polarity(t) != "negative":
            bad.append(f"turn.HOSTILE_KINDS has {t}; the engine has it {polarity(t)}")
        elif t not in TAGS:
            bad.append(f"turn.HOSTILE_KINDS has {t}, which is not a combat tag")
    # 4. the caps the planners use are the map's
    for mod in (P2, turn, shotplan):
        src = open(mod.__file__).read()
        if "min(0.6," in src:
            bad.append(f"{os.path.basename(mod.__file__)} still hardcodes a 0.6 cap; use combat_map.CAP_*")
    return bad


def describe(name):
    t = tag(name)
    lines = [f"{name}  [{t['polarity']}; removed by {removed_by(name) or 'neither Clear nor Cleanse'}]",
             f"  {t['behavior']}",
             f"  stage: {t.get('stage')}   live from: {t.get('live_from') or 'see behavior'}",
             f"  applies: {t['applies']}" if t.get("applies") else None,
             f"  prevented by: {', '.join(t.get('prevented_by') or []) or 'nothing'}"
             + (f" ({t['prevent_check']})" if t.get("prevent_check") else "")
             + f"   copy can take: {t.get('copy_can_take')}   mirror can pass: {t.get('mirror_can_pass')}",
             f"  source: {'; '.join(t.get('source', []))}"]
    lines = [x for x in lines if x is not None]
    for direction in ("outgoing", "incoming"):
        for kind, others in sorted(t.get("interactions", {}).get(direction, {}).items()):
            arrow = "->" if direction == "outgoing" else "<-"
            lines.append(f"  {arrow} {kind}: {', '.join(others)}")
    return "\n".join(lines)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--check":
        bad = check_planner()
        for b in bad:
            print("DRIFT  " + b)
        print(f"combat map @ {GAME_COMMIT}: " + ("planner tables agree" if not bad else f"{len(bad)} mismatch(es)"))
        return 1 if bad else 0
    for name in argv:
        print(describe(name))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
