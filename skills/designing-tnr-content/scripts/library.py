#!/usr/bin/env python3
"""
library.py - the building blocks a design sheet names instead of spelling out.

A library entry is data plus a builder. The data (data/libraries/<family>.json) says what the
block is, which parameters it takes and within what bounds, which engine laws it rests on, what
shipped content proves it, how it fails, and what standing its values have. The builder (a
function in this file, named by the entry) turns parameters into records through the build
skill's factory.py, so no rule object is ever written by hand.

Families shipped here:

  rule_pattern   behaviour: each builder returns AI rules made by Factory.condition/.action/.rule
  loadout        a kit shape: each checker inspects a list of pool codes against the pool
  archetype      a role: maps to a role enemy.py already knows; adds no number of its own

Adding a block is adding an entry and, for a new behaviour, one small builder. Nothing else in
the tools changes. Values that are the director's stay out of entries: a parameter is supplied
by the sheet, where it can be an open slot.

    python3 library.py list [family]
    python3 library.py show <id>
    python3 library.py --selftest

Stdlib only. Socket-free. Reads this skill's data and the build skill's data and scripts.
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
LIB_DIR = os.path.join(SKILL, "data", "libraries")
SLOTS = ("AWAITING_RULING", "AUTHOR")
ID = re.compile(r"^[a-z0-9_]+(/[a-z0-9_]+)*/v[0-9]+$")
ENTRY_KEYS = {"summary", "params", "builder", "rule_count", "laws", "exemplars",
              "failure_modes", "standing", "maps_to", "notes"}
REQUIRED = ("summary", "params", "laws", "exemplars", "failure_modes", "standing")
STANDINGS = ("engine", "shipped", "proposed")
PARAM_TYPES = ("pool_code", "pool_codes", "integer", "enum", "opponent")
# `when`: extra conditions a sheet may put on any block. Key -> (condition type, value field).
# The condition types and their fields are the engine's (law 39, law 64; 45c). Thresholds on
# the two effect conditions are fixed at 1 here because 0 is always true (ai.md, R50).
WHEN = {
    "health_below": ("health_below", "value"),
    "round_greater_than": ("round_greater_than", "value"),
    "round_lower_than": ("round_lower_than", "value"),
    "specific_round": ("specific_round", "value"),
    "distance_at_least": ("distance_higher_than", "value"),
    "self_has_effect": ("has_effect", "effectType"),
    "target_has_effect": ("target_has_effect", "effectType"),
    "no_summon": ("does_not_have_summon", None),
}
BASIC_ATTACK = "basicAttack"     # ai.md "confirmed rule vocabulary"; RUL-2026-10-31-071
BASIC_ATTACK_RANGE = 1


class LibraryError(Exception):
    """A block used wrongly, or a library file that is not well formed."""


# ------------------------------------------------------------------ loading

def load_all(lib_dir: str = LIB_DIR) -> dict:
    """{family: {"meta": {...}, "entries": {id: entry}}}. Raises LibraryError on a bad file."""
    out = {}
    if not os.path.isdir(lib_dir):
        return out
    for name in sorted(os.listdir(lib_dir)):
        if not name.endswith(".json"):
            continue
        family = name[:-5]
        try:
            data = json.load(open(os.path.join(lib_dir, name), encoding="utf-8"))
        except (OSError, ValueError) as err:
            raise LibraryError(f"{name}: cannot be read: {err}")
        problems = lint_family(family, data)
        if problems:
            raise LibraryError(f"{name}: " + "; ".join(problems))
        out[family] = {"meta": data.get("_meta", {}), "entries": data["entries"]}
    return out


def lint_family(family: str, data) -> list:
    if not isinstance(data, dict) or not isinstance(data.get("entries"), dict):
        return ["needs an object with an `entries` object"]
    problems = []
    for eid, entry in data["entries"].items():
        where = f"entry {eid}"
        if not ID.match(eid) or eid.split("/", 1)[0] != family:
            problems.append(f"{where}: id must be {family}/<name>/vN")
        if not isinstance(entry, dict):
            problems.append(f"{where}: not an object")
            continue
        for key in REQUIRED:
            if key not in entry:
                problems.append(f"{where}: missing `{key}`")
        for key in entry:
            if key not in ENTRY_KEYS:
                problems.append(f"{where}: unknown key `{key}`")
        if entry.get("standing") not in STANDINGS:
            problems.append(f"{where}: standing must be one of {', '.join(STANDINGS)}")
        if not all(isinstance(n, (int, str)) for n in entry.get("laws", [])):
            problems.append(f"{where}: laws are cited by number")
        for pname, spec in (entry.get("params") or {}).items():
            if not isinstance(spec, dict) or spec.get("type") not in PARAM_TYPES:
                problems.append(f"{where}: param {pname} needs a type in {', '.join(PARAM_TYPES)}")
        builder = entry.get("builder")
        if family == "rule_pattern" and builder not in RULE_BUILDERS:
            problems.append(f"{where}: builder `{builder}` is not a rule builder in library.py")
        if family == "loadout" and builder not in KIT_CHECKS:
            problems.append(f"{where}: builder `{builder}` is not a kit check in library.py")
        if family == "archetype" and not isinstance(entry.get("maps_to"), dict):
            problems.append(f"{where}: an archetype needs `maps_to`")
    return problems


def entry_of(libs: dict, ref: str) -> dict:
    family = ref.split("/", 1)[0]
    if family not in libs:
        raise LibraryError(f"'{ref}': the {family} library has not shipped")
    if ref not in libs[family]["entries"]:
        raise LibraryError(f"'{ref}' is not in the {family} library "
                           f"(it has: {', '.join(sorted(libs[family]['entries']))})")
    return libs[family]["entries"][ref]


# ------------------------------------------------------------------ parameters

def check_params(ref: str, entry: dict, params: dict, pool: dict | None) -> list:
    """Problems with `params` for this entry. A slot word is allowed anywhere a value is."""
    problems = []
    specs = entry.get("params") or {}
    params = params or {}
    for name in params:
        if name not in specs:
            problems.append(f"'{ref}' has no parameter `{name}` (it takes: {', '.join(specs) or 'none'})")
    for name, spec in specs.items():
        if name not in params:
            if spec.get("required", True) and "default" not in spec:
                problems.append(f"'{ref}' needs parameter `{name}`")
            continue
        value = params[name]
        if value in SLOTS:
            continue
        kind = spec["type"]
        if kind == "integer":
            if isinstance(value, bool) or not isinstance(value, int):
                problems.append(f"'{ref}' {name}: expected a whole number or a slot word, got {value!r}")
            elif not spec.get("min", value) <= value <= spec.get("max", value):
                problems.append(f"'{ref}' {name}: {value} is outside {spec.get('min')} to {spec.get('max')}")
        elif kind == "enum":
            if value not in spec["values"]:
                problems.append(f"'{ref}' {name}: {value!r} is not one of {', '.join(spec['values'])}")
        elif kind == "opponent":
            if value not in opponent_targets():
                problems.append(f"'{ref}' {name}: {value!r} is not one of {', '.join(opponent_targets())}")
        elif kind in ("pool_code", "pool_codes"):
            codes = [value] if kind == "pool_code" else value
            if kind == "pool_codes" and (not isinstance(value, list) or not value):
                problems.append(f"'{ref}' {name}: expected a list of pool codes")
                continue
            for code in codes:
                if not isinstance(code, str):
                    problems.append(f"'{ref}' {name}: {code!r} is not a pool code")
                elif pool is not None and code not in pool:
                    problems.append(f"'{ref}' {name}: pool code {code} does not exist (32b_DATA_pool.json)")
    return problems


_TARGETS = []


def opponent_targets() -> list:
    """The opponent targets a distance condition accepts, read from 45c (law 39)."""
    if not _TARGETS:
        path = os.path.join(_build_skill(), "data", "45c_DATA_constructors.json")
        fields = json.load(open(path))["unions"]["ZodAllAiConditions"]["distance_lower_than"]["fields"]
        _TARGETS.extend(t for t in fields["target"]["enum"] if t.endswith("_OPPONENT")
                        and not t.startswith("BARRIER"))
    return _TARGETS


def check_when(when, where: str) -> list:
    problems = []
    if when is None:
        return problems
    if not isinstance(when, dict):
        return [f"{where}: `when` must be an object"]
    for key, value in when.items():
        if key not in WHEN:
            problems.append(f"{where}: `when` has no condition `{key}` (it has: {', '.join(WHEN)})")
        elif value in SLOTS:
            continue
        elif key == "no_summon":
            if value is not True:
                problems.append(f"{where}: when.no_summon must be true")
        elif WHEN[key][1] == "effectType":
            if not isinstance(value, str) or not re.fullmatch(r"[a-z]+", value):
                problems.append(f"{where}: when.{key} must be an effect type such as `shield`")
        elif isinstance(value, bool) or not isinstance(value, int) or value < 1:
            problems.append(f"{where}: when.{key} must be a whole number of at least 1 or a slot word")
    return problems


def when_conditions(when, factory) -> list:
    out = []
    for key, value in (when or {}).items():
        ctype, field = WHEN[key]
        if field is None:
            out.append(factory.condition(ctype))
        elif field == "effectType":
            out.append(factory.condition(ctype, effectType=value, threshold=1))
        else:
            out.append(factory.condition(ctype, value=value))
    return out


# ------------------------------------------------------------------ rule builders
# Each returns a list of (rule, pool_code_or_None). ctx = {"factory", "pool", "target"}.

def _jutsu_rule(ctx, code: str, target: str | None = None):
    """One rule that uses one pool jutsu, gated the way the pool says (law 40)."""
    fac, pool = ctx["factory"], ctx["pool"]
    j = pool[code]
    if j.get("target") == "ground":
        raise LibraryError(f"{code} ({j['name']}) targets the ground; ground patterns belong to "
                           f"the boss fight grammar and are not a plain rule pattern")
    if j.get("gate") is None:
        # A self-target jutsu takes no distance gate, and its rule targets SELF (law 40;
        # ai.md Part 2, targets).
        return fac.rule(action=fac.action("use_specific_jutsu", jutsuId=j["id"], target="SELF")), code
    target = target or "RANDOM_OPPONENT"
    return fac.rule(fac.condition("distance_lower_than", value=j["gate"], target=target),
                    action=fac.action("use_specific_jutsu", jutsuId=j["id"], target=target)), code


def build_use_jutsu(ctx, params):
    return [_jutsu_rule(ctx, params["jutsu"], params.get("target"))]


def build_rotation(ctx, params):
    return [_jutsu_rule(ctx, code, params.get("target")) for code in params["jutsus"]]


def build_opener(ctx, params):
    j = ctx["pool"][params["jutsu"]]
    if j.get("gate") is not None:
        raise LibraryError(f"opener: {params['jutsu']} ({j['name']}) is not a self-target stance")
    if any(e.split()[0] == "stealth" for e in j.get("effects", [])):
        raise LibraryError(f"opener: {params['jutsu']} ({j['name']}) grants stealth, and a stealthed "
                           f"AI cannot attack that round (law 62); use it behind `when.health_below`")
    return [_jutsu_rule(ctx, params["jutsu"])]


def build_basic_attack(ctx, params):
    fac = ctx["factory"]
    target = params.get("target") or "CLOSEST_OPPONENT"
    return [(fac.rule(fac.condition("distance_lower_than", value=BASIC_ATTACK_RANGE + 1, target=target),
                      action=fac.action("use_specific_jutsu", jutsuId=BASIC_ATTACK, target=target)), None)]


def build_fallback(ctx, params):
    fac = ctx["factory"]
    mode = params.get("mode", "move")
    if mode == "end_turn":
        return [(fac.rule(action=fac.action("end_turn")), None)]
    rules = []
    if mode == "basic_attack_then_move":
        rules += build_basic_attack(ctx, {})
    rules.append((fac.rule(action=fac.action("move_towards_opponent")), None))
    return rules


RULE_BUILDERS = {"use_jutsu": build_use_jutsu, "rotation": build_rotation, "opener": build_opener,
                 "basic_attack": build_basic_attack, "fallback": build_fallback}
TERMINAL_BUILDERS = ("fallback",)


def expand_rules(libs: dict, refs: list, factory, pool: dict, extra_when=None) -> list:
    """Sheet rule references -> [(rule, pool_code_or_None)], in order. `extra_when` is a phase's."""
    ctx = {"factory": factory, "pool": pool}
    out = []
    for ref in refs:
        entry = entry_of(libs, ref["use"])
        params = dict(ref.get("params") or {})
        for name, spec in (entry.get("params") or {}).items():
            if name not in params and "default" in spec:
                params[name] = spec["default"]
        problems = check_params(ref["use"], entry, params, pool)
        if problems:
            raise LibraryError("; ".join(problems))
        built = RULE_BUILDERS[entry["builder"]](ctx, params)
        when = {**(extra_when or {}), **(ref.get("when") or {})}
        if when and entry["builder"] in TERMINAL_BUILDERS:
            raise LibraryError(f"'{ref['use']}' is the unconditional end of the list and takes no `when` (law 41)")
        extra = when_conditions(when, factory)
        for rule, code in built:
            rule["conditions"] = extra + rule["conditions"]
            out.append((rule, code))
    return out


# ------------------------------------------------------------------ loadout checks
# Each returns (problems, notes) for a list of pool codes.

def kit_stance_and_attacks(codes: list, pool: dict, params: dict):
    problems, notes = [], []
    kit = [pool[c] for c in codes]
    if not any(j.get("ap", 60) <= 40 for j in kit):
        problems.append("the kit has no 40 AP action: a turn is 100 AP, so a kit of 60 AP attacks "
                        "alone leaves the AI unable to fill its turn (laws 61, 63)")
    if not any(any(e.split()[0] in ("damage", "pierce") for e in j.get("effects", [])) for j in kit):
        problems.append("the kit has no damaging action")
    if len(set(codes)) != len(codes):
        problems.append("a pool code appears twice in the kit")
    return problems, notes


KIT_CHECKS = {"stance_and_attacks": kit_stance_and_attacks}


def check_kit(libs: dict, recipe: str, codes: list, pool: dict):
    entry = entry_of(libs, recipe)
    return KIT_CHECKS[entry["builder"]](codes, pool, {})


# ------------------------------------------------------------------ cli and selftest

def _build_skill():
    roots = [os.environ.get("TNR_BUILD_SKILL"),
             os.path.join(os.path.dirname(SKILL), "building-tnr-content"),
             "/mnt/skills/user/building-tnr-content"]
    for root in roots:
        if root and os.path.isdir(root):
            return root
    raise LibraryError("cannot find building-tnr-content")


def build_tools():
    """(Factory instance, pool records, rule cap) from the build skill, by explicit path."""
    root = _build_skill()
    scripts, data = os.path.join(root, "scripts"), os.path.join(root, "data")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from factory import Factory
    fac = Factory(ctors=os.path.join(data, "45c_DATA_constructors.json"),
                  entities=os.path.join(data, "45d_DATA_entity_schemas.json"),
                  checks=os.path.join(data, "45g_DATA_checks.json"))
    pool = json.load(open(os.path.join(data, "32b_DATA_pool.json")))["records"]
    cap = json.load(open(os.path.join(data, "45e_DATA_constants.json")))["constants"]["AI_PROFILE_MAX_RULES"]["value"]
    return fac, pool, cap


def selftest() -> int:
    checks, failures = [], []

    def want(cond, label):
        checks.append(label)
        if not cond:
            failures.append(label)

    libs = load_all()
    want({"rule_pattern", "loadout", "archetype"} <= set(libs), "the three P2 families load and lint clean")
    fac, pool, cap = build_tools()
    want(isinstance(cap, int) and cap > 0, "the rule cap is read from 45e, not written here")

    built = expand_rules(libs, [
        {"use": "rule_pattern/opener/v1", "params": {"jutsu": "B37"}},
        {"use": "rule_pattern/rotation/v1", "params": {"jutsus": ["S06", "S02"]}},
        {"use": "rule_pattern/use_jutsu/v1", "params": {"jutsu": "S35"}, "when": {"health_below": 30}},
        {"use": "rule_pattern/fallback/v1"}], fac, pool)
    rules = [r for r, _ in built]
    want(len(rules) == 5, "four blocks expand to five rules")
    want(rules[0]["conditions"] == [] and rules[0]["action"]["target"] == "SELF",
         "an opener is ungated and targets SELF")
    want(rules[1]["conditions"][0]["value"] == pool["S06"]["gate"] == pool["S06"]["range"] + 1,
         "an attack carries the pool's own gate, range + 1 (law 40)")
    want([c["type"] for c in rules[3]["conditions"]] == ["health_below"],
         "`when` adds its condition; a self-target jutsu still takes no distance gate")
    want(rules[-1]["conditions"] == [] and rules[-1]["action"]["type"] == "move_towards_opponent",
         "the fallback is unconditional and terminal (law 41)")
    try:
        ranges = {pool[c]["id"]: pool[c]["range"] for _, c in built if c and pool[c]["range"] is not None}
        fac.rules(*rules, ranges=ranges)
        want(True, "the build skill's own rule-set check accepts the result")
    except Exception as err:                            # noqa: BLE001
        want(False, f"the build skill's own rule-set check accepts the result ({err})")
    both = expand_rules(libs, [{"use": "rule_pattern/fallback/v1", "params": {"mode": "basic_attack_then_move"}}], fac, pool)
    want(both[0][0]["action"]["jutsuId"] == BASIC_ATTACK and both[0][0]["conditions"][0]["value"] == 2,
         "the basic attack is gated at its range + 1")

    def refuses(label, refs):
        try:
            expand_rules(libs, refs, fac, pool)
            want(False, label)
        except LibraryError:
            want(True, label)

    refuses("an unknown pool code is refused", [{"use": "rule_pattern/use_jutsu/v1", "params": {"jutsu": "ZZ99"}}])
    refuses("an unknown parameter is refused", [{"use": "rule_pattern/use_jutsu/v1", "params": {"jutsu": "S01", "power": 9}}])
    refuses("a missing parameter is refused", [{"use": "rule_pattern/use_jutsu/v1"}])
    refuses("an attack cannot be an opener", [{"use": "rule_pattern/opener/v1", "params": {"jutsu": "S01"}}])
    refuses("a stealth stance cannot be an opener (law 62)", [{"use": "rule_pattern/opener/v1", "params": {"jutsu": "B09"}}])
    refuses("a conditional fallback is refused (law 41)", [{"use": "rule_pattern/fallback/v1", "when": {"health_below": 50}}])
    refuses("an unknown block is refused", [{"use": "rule_pattern/nope/v1"}])
    refuses("an unshipped family is refused", [{"use": "boss_grammar/omen/v1"}])
    want(check_when({"health_below": 0}, "x") != [] and check_when({"mood": 1}, "x") != []
         and check_when({"health_below": "AWAITING_RULING", "no_summon": True}, "x") == [],
         "`when` values are whole numbers, known conditions, or slot words")

    problems, _ = check_kit(libs, "loadout/stance_and_attacks/v1", ["S01", "S02"], pool)
    want(any("40 AP" in p for p in problems), "an all-attack kit fails the stance-and-attacks recipe (laws 61, 63)")
    problems, _ = check_kit(libs, "loadout/stance_and_attacks/v1", ["B37", "S01"], pool)
    want(problems == [], "a stance plus an attack passes it")

    for family, lib in libs.items():
        for eid, entry in lib["entries"].items():
            want(entry["laws"] or entry["standing"] != "engine", f"{eid}: an engine-standing block cites its laws")
    bad = {"entries": {"rule_pattern/x/v1": {"summary": "s", "params": {}, "builder": "nope", "laws": [],
                                             "exemplars": [], "failure_modes": [], "standing": "ratified"}}}
    want(len(lint_family("rule_pattern", bad)) == 2, "a library file with an unknown builder or standing fails its lint")

    for label in failures:
        print(f"  FAIL  {label}")
    print(f"\n{len(checks) - len(failures)} passed, {len(failures)} failed")
    return 1 if failures else 0


def main(argv) -> int:
    if argv[:1] == ["--selftest"]:
        return selftest()
    try:
        libs = load_all()
        if argv[:1] == ["list"]:
            for family, lib in libs.items():
                if len(argv) > 1 and argv[1] != family:
                    continue
                for eid, entry in lib["entries"].items():
                    print(f"{eid}  [{entry['standing']}]  {entry['summary']}")
            return 0
        if argv[:1] == ["show"] and len(argv) == 2:
            print(json.dumps(entry_of(libs, argv[1]), indent=1))
            return 0
    except LibraryError as err:
        print(f"library.py: {err}", file=sys.stderr)
        return 2
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
