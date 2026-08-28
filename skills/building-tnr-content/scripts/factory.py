#!/usr/bin/env python3
"""Construct TNR payloads instead of authoring them.

Every shape failure this project has had came from the same place: a payload
typed from memory. The AI rule shape was documented correctly and still got
written as a flat {action, condition, conditionValue} triple. Effect objects
got assembled from a field list instead of a live exemplar. A jutsu edit
omitted injectableInBattle and tripped a guard nobody could read.

A shape that cannot be built wrong needs no law. So this builds from the
generated files rather than checking after the fact:

  45c_DATA_constructors.json   tagged shapes: effect tags, quest objectives,
                               AI conditions, AI actions
  45d_DATA_entity_schemas.json per-entity fields, bounds, defaults, nullability
  45g_DATA_checks.json         the shared check config, also read by the
                               builder preflight and by validate.py

Usage as a library:

    from factory import Factory
    f = Factory()                       # loads the generated files
    tag  = f.tag("damage", power=40, statTypes=["Highest"])
    rule = f.rule(f.condition("distance_lower_than", value=3),
                  action=f.action("use_specific_jutsu", jutsuId="..."))
    node = f.objective("dialog", id="n1", description="...")
    entry = f.entry("jutsu", "create", name="X", data={...})

Every constructor fills the schema defaults first, then applies your values,
then rejects anything the schema does not know. Construction raises rather
than returning a shape the server will refuse.

Self-test:
    python3 factory.py --selftest
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEARCH = [os.getcwd(), HERE, os.path.join(HERE, ".."), "/mnt/project"]


class FactoryError(ValueError):
    """A shape that would have been rejected by the server, caught at build."""


def _find(name):
    for d in SEARCH:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise FactoryError(f"{name} not found. Copy the generated files into the "
                       f"working directory (looked in {SEARCH})")


class Factory:
    def __init__(self, ctors=None, entities=None, checks=None):
        self.ctors = json.load(open(ctors or _find("45c_DATA_constructors.json")))["unions"]
        self.ents = json.load(open(entities or _find("45d_DATA_entity_schemas.json")))["entities"]
        self.checks = json.load(open(checks or _find("45g_DATA_checks.json")))

    # ---------------------------------------------------------------- tagged
    def _member(self, union, key):
        members = self.ctors.get(union)
        if not members:
            raise FactoryError(f"union {union} missing from 45c")
        if key not in members:
            near = ", ".join(sorted(members)[:8])
            raise FactoryError(f"'{key}' is not a member of {union}. Valid: {near}...")
        return members[key]

    def _build(self, union, key, values, disc="type"):
        spec = self._member(union, key)
        fields = spec["fields"]
        unknown = set(values) - set(fields)
        if unknown:
            raise FactoryError(f"{union}.{key}: unknown field(s) {sorted(unknown)}. "
                               f"Valid: {', '.join(sorted(fields))}")
        out = {}
        for f, rule in fields.items():
            if "default" in rule:
                out[f] = rule["default"]
        out[disc] = key
        out.update(values)
        for f, v in out.items():
            self._bounds(f"{union}.{key}.{f}", fields.get(f) or {}, v)
        return out

    @staticmethod
    def _bounds(where, rule, v):
        if isinstance(v, bool) or v is None:
            return
        if rule.get("enum") and isinstance(v, str) and v not in rule["enum"]:
            raise FactoryError(f"{where}={v!r} not in enum ({', '.join(rule['enum'][:8])})")
        if isinstance(v, (int, float)):
            if "min" in rule and v < rule["min"]:
                raise FactoryError(f"{where}={v} below min {rule['min']}")
            if "max" in rule and v > rule["max"]:
                raise FactoryError(f"{where}={v} above max {rule['max']}")
            if rule.get("int") and v != int(v):
                raise FactoryError(f"{where}={v} must be an integer")

    def tag(self, type_, **values):
        if type_ in self.checks["runtime_only_tags"]["values"]:
            raise FactoryError(
                f"'{type_}' is a runtime-only tag (law 77): the engine injects it in battle "
                "and every authored record carrying it is rejected")
        return self._build("AllTags", type_, values)

    def condition(self, type_, **values):
        return self._build("ZodAllAiConditions", type_, values)

    def action(self, type_, **values):
        return self._build("ZodAllAiActions", type_, values)

    def objective(self, task, **values):
        return self._build("AllObjectives", task, values, disc="task")

    # ----------------------------------------------------------------- rules
    def rule(self, *conditions, action):
        """An AI rule is {conditions: [...], action: {...}}, tagged on both
        sides. Passing a bare string for the action is the failure mode this
        signature exists to make impossible."""
        if isinstance(action, str):
            raise FactoryError("action must be a constructed object from .action(), not a "
                               "string. The flat {action, condition} triple is not the shape")
        return {"conditions": list(conditions), "action": action}

    def rules(self, *rules, ranges=None):
        """Assemble a rule set and enforce the two laws that make a rule set
        work rather than merely validate:

        - the chain must END on an action that always executes, or the AI
          falls off the end and burns its turn on movement (laws 41, 63);
        - every attack rule needs a distance gate of exactly range + 1, since
          rule distance is A* path length: a higher gate fires out of range
          and strands a human player in combat, a lower one forfeits the
          outermost band (law 40).

        `ranges` maps jutsuId -> range so the gate can be checked rather than
        trusted. Omit it and the gate check is skipped with a warning.
        """
        terminal = self.checks["terminal_actions"]["values"]
        if not rules:
            raise FactoryError("a rule set cannot be empty")
        last = rules[-1]
        if last["conditions"] or last["action"].get("type") not in terminal:
            raise FactoryError(
                f"the last rule must be unconditional and one of {terminal}. "
                f"Got conditions={len(last['conditions'])}, "
                f"action={last['action'].get('type')!r} (law 41)")
        for i, r in enumerate(rules[:-1]):
            if not r["conditions"] and r["action"].get("type") in terminal:
                raise FactoryError(f"rule {i} is unconditional and terminal; every rule below "
                                   "it is dead (law 41)")
        warnings = []
        for i, r in enumerate(rules):
            jid = r["action"].get("jutsuId")
            if not jid:
                continue
            gate = next((c["value"] for c in r["conditions"]
                         if c["type"] == "distance_lower_than"), None)
            if ranges is None:
                warnings.append(f"rule {i}: no range table supplied, gate unchecked")
            elif jid in ranges and gate != ranges[jid] + 1:
                raise FactoryError(f"rule {i}: jutsu range is {ranges[jid]}, so the gate must "
                                   f"be {ranges[jid] + 1}, got {gate} (law 40)")
        return list(rules), warnings

    # -------------------------------------------------------------- entities
    def entry(self, entity, slot, name=None, srcId=None, targetId=None, data=None):
        """A manifest entry. Applies on construction what used to be linted:
        hidden on creates, data.name mirroring, targetId on edits, null
        handling by the generated nullability map."""
        fields = self.ents.get(entity)
        if fields is None:
            raise FactoryError(f"unknown entity '{entity}'. Known: {', '.join(sorted(self.ents))}")
        fields = fields["fields"]
        data = dict(data or {})

        if slot in ("edit", "convert") and not targetId:
            raise FactoryError(f"{entity} {slot} needs a top-level targetId: srcId and the id "
                               "map do not self-resolve on edits (law 5)")
        if slot == "create":
            if self.checks["hidden_on_create"]["values"]:
                data.setdefault("hidden", True)
            if name:
                # the entry-level name is manifest metadata the server never
                # sees; data.name is what lands (law 36)
                data.setdefault("name", name)
            missing = [f for f in self.checks["required_on_create"]["fields"].get(entity, [])
                       if f not in data and f not in ("effects", "content")]
            if missing:
                raise FactoryError(f"{entity} create missing required field(s) with no schema "
                                   f"default: {missing[:8]}")

        nullable = set(self.checks["nullable"]["fields"].get(entity, []))
        for f, v in list(data.items()):
            if v is None and f not in nullable:
                raise FactoryError(f"{entity}.{f} is null but the validator is not nullable. "
                                   "Omit the key; null is rejected (law 72)")
            if f == "image" and v == "":
                raise FactoryError("image sent as an empty string is nulled at the write path "
                                   "and 500s. Omit the key (law 46)")
            self._bounds(f"{entity}.{f}", fields.get(f) or {}, v)

        for f in self.checks["cap_100"]["fields"].get(entity, []):
            if isinstance(data.get(f), (int, float)) and data[f] > 100:
                raise FactoryError(f"{entity}.{f}={data[f]} exceeds the cap of 100 (law 8)")
        for f in self.checks["date_fields"]["fields"].get(entity, []):
            v = data.get(f)
            if v and not (isinstance(v, str) and len(v) == 10 and v[4] == v[7] == "-"):
                raise FactoryError(f"{entity}.{f} must be plain YYYY-MM-DD, got {v!r} (law 7)")

        self._effects(entity, data.get("effects"))

        entry = {"entity": entity, "slot": slot}
        if name:
            entry["name"] = name
        if srcId:
            entry["srcId"] = srcId
        if targetId:
            entry["targetId"] = targetId
        entry["data"] = data
        return entry

    def _effects(self, entity, effects):
        if not effects:
            return
        types = [e.get("type") for e in effects if isinstance(e, dict)]
        for e in effects:
            if not isinstance(e, dict):
                raise FactoryError("every effect must be an object")
            t = e.get("type")
            if t in self.checks["runtime_only_tags"]["values"]:
                raise FactoryError(f"'{t}' is a runtime-only tag (law 77)")
            needs = self.checks["companion_required"]["values"].get(t)
            if needs and not any(x in types for x in needs):
                raise FactoryError(f"'{t}' requires one of {needs} on the same action (law 78)")
            only = self.checks["entity_only_tags"]["values"].get(t)
            if only and entity != only:
                raise FactoryError(f"'{t}' is {only}-only, not legal on {entity} (law 78)")
            if t in self.checks["zero_power_per_level"]["values"] and e.get("powerPerLevel"):
                raise FactoryError(f"powerPerLevel must be 0 for '{t}' (law 78)")
            cap = self.checks["tag_power_max"]["fields"].get(t)
            if cap is not None and isinstance(e.get("power"), (int, float)) and e["power"] > cap:
                raise FactoryError(f"'{t}' power {e['power']} exceeds the cap of {cap} (law 6)")
            if t in self.checks["formula_tags"]["values"] and e.get("calculation", "formula") == "formula":
                if not e.get("statTypes") or not e.get("generalTypes"):
                    raise FactoryError(f"formula effect '{t}' needs BOTH statTypes and "
                                       "generalTypes; an empty one detonates the damage "
                                       "formula rather than zeroing it (law 4)")

    # -------------------------------------------------------------- manifest
    def manifest(self, entries, capture=None):
        order = self.checks["build_order"]["values"]
        seen = [e["entity"] for e in entries]
        idx = [order.index(x) for x in seen if x in order]
        if idx != sorted(idx):
            raise FactoryError(f"entries are out of build order. Required: {' -> '.join(order)}. "
                               "Out of order means composing references to records that do not "
                               "exist yet, and unresolved refs are stripped silently (law 17)")
        man = {"items": entries}
        if capture:
            man["capture"] = capture
        return man


# ------------------------------------------------------------------ selftest

def _selftest():
    """The Phase 4 exit test: a deliberately malformed payload of each entity
    type must be caught by CONSTRUCTION, not by review."""
    f = Factory()
    cases = []

    def expect(label, fn):
        try:
            fn()
        except FactoryError as e:
            cases.append((label, True, str(e)[:90]))
        else:
            cases.append((label, False, "NOT CAUGHT"))

    expect("jutsu: runtime-only tag", lambda: f.tag("activatesagemode", power=1))
    expect("jutsu: power over cap", lambda: f.tag("damage", power=400))
    expect("jutsu: unknown tag field", lambda: f.tag("damage", nonsense=1))
    # NOTE: these use the edit slot deliberately. On a create the required-field
    # check fires first and the case would pass without ever reaching the effect
    # laws, which would make the test green for the wrong reason.
    expect("jutsu: formula without generals",
           lambda: f.entry("jutsu", "edit", targetId="t",
                           data={"effects": [{"type": "damage", "power": 10,
                                              "statTypes": ["Highest"]}]}))
    expect("jutsu: consume without damage",
           lambda: f.entry("jutsu", "edit", targetId="t",
                           data={"effects": [{"type": "consume", "power": 10}]}))
    expect("item: rollsagemode on a jutsu",
           lambda: f.entry("jutsu", "edit", targetId="t",
                           data={"effects": [{"type": "rollsagemode", "power": 5}]}))
    expect("jutsu: create missing required fields",
           lambda: f.entry("jutsu", "create", name="X", data={}))
    expect("ai: flat rule triple",
           lambda: f.rule(f.condition("health_below", value=30), action="use_specific_jutsu"))
    expect("ai: unknown condition", lambda: f.condition("distance", value=2))
    expect("ai: chain ends conditional",
           lambda: f.rules(f.rule(f.condition("health_below", value=30),
                                  action=f.action("use_random_jutsu"))))
    expect("ai: dead rule below a terminal",
           lambda: f.rules(f.rule(action=f.action("end_turn")),
                           f.rule(action=f.action("end_turn"))))
    expect("ai: wrong distance gate",
           lambda: f.rules(f.rule(f.condition("distance_lower_than", value=5),
                                  action=f.action("use_specific_jutsu", jutsuId="J")),
                           f.rule(action=f.action("end_turn")),
                           ranges={"J": 2}))
    expect("quest: unknown task", lambda: f.objective("go_somewhere", id="n1"))
    expect("quest: cap over 100",
           lambda: f.entry("quest", "edit", targetId="t", data={"maxCompletes": 500}))
    expect("quest: bad date",
           lambda: f.entry("quest", "edit", targetId="t", data={"startsAt": "2026-08-26T00:00Z"}))
    expect("quest: null on a non-nullable field",
           lambda: f.entry("quest", "edit", targetId="t", data={"consecutiveObjectives": None}))
    expect("any: edit without targetId", lambda: f.entry("item", "edit", data={"name": "X"}))
    expect("any: empty-string image",
           lambda: f.entry("item", "edit", targetId="t", data={"image": ""}))
    expect("manifest: out of build order",
           lambda: f.manifest([f.entry("quest", "edit", targetId="t", data={}),
                               f.entry("jutsu", "edit", targetId="t2", data={})]))

    # things that must NOT raise
    ok = []
    try:
        f.tag("damage", power=40, statTypes=["Highest"], generalTypes=["Highest"])
        f.entry("quest", "edit", targetId="t", data={"requiredVillage": None})
        f.rules(f.rule(f.condition("distance_lower_than", value=3),
                       action=f.action("use_specific_jutsu", jutsuId="J")),
                f.rule(action=f.action("move_towards_opponent")),
                ranges={"J": 2})
        ok.append(("legal shapes construct cleanly", True, ""))
    except FactoryError as e:
        ok.append(("legal shapes construct cleanly", False, str(e)[:90]))

    rows = cases + ok
    for label, passed, detail in rows:
        print(f"  {'PASS' if passed else 'FAIL'}  {label:<42} {detail}")
    bad = [r for r in rows if not r[1]]
    print(f"\n{len(rows) - len(bad)}/{len(rows)} passed")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
