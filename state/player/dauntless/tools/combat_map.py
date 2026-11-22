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
    python3 combat_map.py TAG                        what the engine does with TAG, its timing and its links
    python3 combat_map.py --check [--game PATH]      drift checks (exit 1 on any mismatch)

What --check covers, and what it does not:
  * Planner against the map (always): the planner's Clear/Cleanse polarity tables, its kind -> tag names, the
    hostile ground kinds, and an ast scan of planner2.py, turn.py and shotplan.py for min() calls that cap an
    absorb / reflect / lifesteal / afterburn / parry term with a number literal in any argument (they must use
    combat_map.CAP_*).
  * Map against the game (only with --game PATH, or TNR_GAME_SRC set): checks that rules.json, tags.json and
    interactions.json carry the same full 40-character pin, then re-reads every rules.json constant from that pinned
    commit's git objects in the checkout (not its working tree) and compares value, symbol and file:line. A copy
    without git metadata, or one missing the pinned commit, fails.
  * Not covered: tags.json, interactions.json and engine.md text are never re-read against the game; they are
    hand-checked (docs/combat-engine/_build/curation.py). A passing --check without --game says nothing about
    the game source at all.

The map wins over a hardcoded guess. When the check fails, fix the planner table or, if the map is out of date
with the game, regenerate the map (docs/combat-engine/README.md) and say which in the commit.
Set TNR_COMBAT_MAP to another directory holding tags.json, interactions.json and rules.json to read a different
copy of the data; the reader code always comes from this checkout.
"""
import ast
import importlib.util
import json
import os
import re
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
    # 4. the caps the planners use are the map's: no numeric literal in a min()/max() beside a capped term
    for mod in (P2, turn, shotplan):
        bad += cap_literals(mod.__file__)
    return bad


_CAP_TERM = re.compile(r"absorb|reflect|lifesteal|leech|afterburn|parry|\b(?:PAR|ABS|PABS|REF|PREF|LS|PLS|AFB)\b"
                       r"|\b(?:par|ab|refl|ls)\b")


def _is_number(node):
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        node = node.operand
    return isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool)


def cap_literals(path):
    """min() calls in a planner file that cap an absorb/reflect/leech/afterburn/parry term with a number literal,
    in any argument position and across lines (parsed with ast, so formatting doesn't hide one)."""
    src = open(path).read()
    out = []
    for node in ast.walk(ast.parse(src, filename=path)):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "min"):
            continue
        nums = [x for x in node.args if _is_number(x)]
        terms = [ast.get_source_segment(src, x) or "" for x in node.args if not _is_number(x)]
        if nums and any(_CAP_TERM.search(t) for t in terms):
            seg = " ".join((ast.get_source_segment(src, node) or "").split())
            out.append(f"{os.path.basename(path)}:{node.lineno} caps with a literal; use combat_map.CAP_*: {seg}")
    return out


# The reader is code, so it always comes from this tools checkout; TNR_COMBAT_MAP only chooses the data files.
_OWN_MAP_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "docs", "combat-engine"))
_HEX40 = re.compile(r"^[0-9a-f]{40}$")


def _rules_builder():
    """docs/combat-engine/_build/rules.py from this checkout, the same reader that wrote rules.json."""
    path = os.path.join(_OWN_MAP_DIR, "_build", "rules.py")
    spec = importlib.util.spec_from_file_location("combat_engine_rules", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_source(game_root):
    """rules.json against the game source at game_root, read from the pinned commit's git objects (never the
    working tree, so local edits can't pass as the pinned revision). Returns (mismatches, notes)."""
    bad, notes = [], []
    if not _RULES:
        return [f"rules.json not found at {MAP_DIR}"], notes
    pin = _RULES.get("pinned_game_commit") or ""
    if not _HEX40.match(pin):
        return [f"rules.json pin {pin!r} is not a full 40-character commit"], notes
    for name, data in (("tags.json", _TAGS), ("interactions.json", _EDGES)):
        other = (data or {}).get("pinned_game_commit")
        if other != pin:
            bad.append(f"{name} is pinned to {other!r}, rules.json to {pin}: the map is not one bundle")
    if not os.path.isdir(game_root):
        return bad + [f"game source not found at {game_root}"], notes
    R = _rules_builder()
    if not R.git_head(game_root):
        return bad + [f"{game_root} is not a git checkout, so the pinned revision can't be verified; use a clone "
                      f"that contains {pin}"], notes
    commit = R.resolve_commit(game_root, pin)
    if commit != pin:
        return bad + [f"pinned commit {pin} is not in the history at {game_root}"], notes
    head = R.git_head(game_root)
    if head != pin:
        notes.append(f"checkout HEAD is {head}; checked the pinned commit's files, not HEAD's")
    changed = R.changed_files(game_root, pin)
    if changed:
        notes.append(f"working tree differs from {pin[:12]} in {', '.join(changed)}; ignored, the pinned objects "
                     f"were checked")
    try:
        live = R.read_constants(game_root, pin)
    except (OSError, ValueError) as e:
        return bad + [f"could not read the game constants: {e}"], notes
    for grp, entries in live.items():
        mine = _RULES.get(grp, {})
        for key, e in entries.items():
            m = mine.get(key)
            if m is None:
                bad.append(f"rules.json lacks {grp}.{key} ({e['source']})")
                continue
            if m["value"] != e["value"]:
                bad.append(f"{grp}.{key}: rules.json {m['value']}, game {e['value']} ({e['source']})")
            if m["source"] != e["source"]:
                bad.append(f"{grp}.{key}: rules.json cites {m['source']}, game has it at {e['source']}")
        for key in set(mine) - set(entries):
            bad.append(f"rules.json has {grp}.{key}, which rules.py no longer reads from the game")
    return bad, notes


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
        game = os.environ.get("TNR_GAME_SRC")
        if "--game" in argv:
            i = argv.index("--game")
            if i + 1 >= len(argv):
                print("--game needs a path to a TheNinjaRPG checkout")
                return 2
            game = argv[i + 1]
        bad = check_planner()
        for b in bad:
            print("DRIFT  " + b)
        print(f"planner vs map @ {GAME_COMMIT}: " + ("agree" if not bad else f"{len(bad)} mismatch(es)"))
        if game:
            sbad, notes = check_source(game)
            for b in sbad:
                print("DRIFT  " + b)
            for n in notes:
                print("NOTE   " + n)
            print(f"rules.json vs game source at {game}: " + ("agree" if not sbad else f"{len(sbad)} mismatch(es)"))
            bad += sbad
        else:
            print("game source: not checked (pass --game PATH or set TNR_GAME_SRC)")
        return 1 if bad else 0
    for name in argv:
        print(describe(name))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
