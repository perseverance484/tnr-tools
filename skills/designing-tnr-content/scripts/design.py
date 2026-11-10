#!/usr/bin/env python3
"""
design.py - the design sheet: scaffold it, check it, explain it, compile it.

A design sheet is the one contract between designing-tnr-content and building-tnr-content. It
holds the creative and structural half of a piece of content and names every decision that is
still open. It never holds an engine field the build tools derive: mission.py's rule ("a sheet
cannot reach a profile field") is kept and extended here, not loosened.

    design.py new <kind> [--id ID] [--title T] [--from SHEET.json] [-o OUT.json]
    design.py check <sheet.json> [--json]
    design.py explain <sheet.json> [-o OUT.md]
    design.py compile <sheet.json> -o push/NNN_x.json
    design.py --selftest

kinds: ai, ai_line, boss, quest, quest_chain, dungeon, event

What `check` does, and where each rule comes from (this tool cites owners, it states no rule):
  schema      data/design_sheet.schema.json
  engine      a sheet key that the build tools own is refused. The key list is READ from
              building-tnr-content: 48_DATA_mission_profiles.json `_field_routing`, and
              enemy.py STAT_FIELDS / ROLE_DEFAULTS. Nothing is listed here by hand except the
              three AI record fields noted at ENGINE_AI_EXTRA.
  libraries   every `use` / `structure` / `recipe` id must resolve in data/libraries/*.json.
              A family with no library file yet is reported as pending, not as an error;
              `compile` refuses while any reference is pending.
  slots       every AWAITING_RULING / AUTHOR left in the sheet, by path. Open slots do not
              fail `check`; they are the list the director is shown.
  payout      a number in `payout` or `tuning` must carry its source (an owner path or a
              ruling id), or be a reward-package reference, or be AWAITING_RULING. A bare
              number is refused: docs/DOCTRINE.md D-reserved-dauntless.
  text        references/writing.md lists the owners of each lint.

Exit codes: 0 clean (open slots allowed), 1 errors, 2 usage or unreadable input,
3 compile refused.

Stdlib only. Socket-free. Reads repository or skill files and nothing else.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCHEMA_PATH = os.path.join(SKILL, "data", "design_sheet.schema.json")
LIB_DIR = os.path.join(SKILL, "data", "libraries")
SLOTS = ("AWAITING_RULING", "AUTHOR")
LEGACY_SLOT = "dauntless"          # event sheet (26x) spelling, accepted inside `event` only
KINDS = ("ai", "ai_line", "boss", "quest", "quest_chain", "dungeon", "event")
# Phase that ships `compile` for each kind (state/prompt_skill_overhaul.md section 8).
COMPILE_PHASE = {"ai": "P2", "ai_line": "P2", "quest": "P3", "quest_chain": "P3",
                 "dungeon": "P3", "event": "P3", "boss": "P4"}
# AI record fields the factory derives that enemy.py does not expose as a constant:
# law 14 (rank), law 15 (pools are overwritten). Cited, not restated.
ENGINE_AI_EXTRA = ("rank", "maxHealth", "curHealth", "maxChakra", "curChakra",
                   "maxStamina", "curStamina")
BATTLE_PLACEHOLDERS = ("%user", "%target", "%jutsu")   # owner: building references/jutsu.md 2
EM_DASH = "—"
DIALOG_FIELDS = ("dialog", "choice")                   # owner: D-emdash-dialog, lint L11


class DesignError(Exception):
    """Usage or input problem (exit 2)."""


# ------------------------------------------------------------------ locating the build skill

def build_skill_dirs() -> list:
    env = os.environ.get("TNR_BUILD_SKILL")
    roots = [env] if env else []
    roots += [os.path.join(os.path.dirname(SKILL), "building-tnr-content"),
              "/mnt/skills/user/building-tnr-content"]
    return [r for r in roots if r and os.path.isdir(r)]


def build_file(*parts) -> str | None:
    for root in build_skill_dirs():
        p = os.path.join(root, *parts)
        if os.path.exists(p):
            return p
    return None


def engine_keys() -> dict:
    """Keys a sheet may not carry, read from their owners. Returns {key: owner}."""
    out = {}
    prof = build_file("data", "48_DATA_mission_profiles.json")
    if not prof:
        raise DesignError("cannot find building-tnr-content (48_DATA_mission_profiles.json); "
                          "set TNR_BUILD_SKILL or install the skill beside this one")
    routing = json.load(open(prof))["_field_routing"]
    owner = "48_DATA_mission_profiles.json _field_routing"
    for key in routing["profile"]:
        out[key.split(".")[-1]] = owner + ".profile"
    for key in routing["fixed"]:
        out[key] = owner + ".fixed"
    for key in routing["null_by_design"]:
        out[key] = owner + ".null_by_design"
    scripts = build_file("scripts", "enemy.py")
    if scripts:
        sys.path.insert(0, os.path.dirname(scripts))
        try:
            import enemy as enemy_mod
            for key in enemy_mod.STAT_FIELDS:
                out[key] = "enemy.py STAT_FIELDS"
            for role in enemy_mod.ROLE_DEFAULTS.values():
                for key in role:
                    if key[0].islower() and key[1:] != key[1:].lower():   # camelCase = record field
                        out[key] = "enemy.py ROLE_DEFAULTS"
        finally:
            sys.path.pop(0)
    for key in ENGINE_AI_EXTRA:
        out[key] = "engine laws 14, 15 (derived by enemy.py)"
    return out


def entity_bounds() -> dict:
    """{entity: {field: (min, max)}} from 45d, when the build skill is present."""
    path = build_file("data", "45d_DATA_entity_schemas.json")
    if not path:
        return {}
    out = {}
    for name, ent in json.load(open(path)).get("entities", {}).items():
        fields = ent.get("fields") if isinstance(ent, dict) else None
        if isinstance(fields, dict):
            out[name] = {f: (v.get("min"), v.get("max")) for f, v in fields.items()
                         if isinstance(v, dict) and ("min" in v or "max" in v)}
    return out


# ------------------------------------------------------------------ schema subset validator

def _is_type(value, name: str) -> bool:
    if name == "string":
        return isinstance(value, str)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    if name == "array":
        return isinstance(value, list)
    if name == "object":
        return isinstance(value, dict)
    return False


def validate(value, node: dict, root: dict, path: str, errs: list) -> None:
    if "$ref" in node:
        ref = node["$ref"]
        if not ref.startswith("#/$defs/"):
            raise DesignError(f"schema: unsupported $ref {ref}")
        node = root["$defs"][ref.split("/")[-1]]
    if "anyOf" in node:
        trials = []
        for option in node["anyOf"]:
            sub = []
            validate(value, option, root, path, sub)
            if not sub:
                return
            trials.append(sub)
        errs.append(f"{path}: matches none of the allowed forms "
                    f"(closest: {min(trials, key=len)[0].split(': ', 1)[-1]})")
        return
    if node.get("x-slot") and value in SLOTS:
        return
    types = node.get("type")
    if types:
        types = [types] if isinstance(types, str) else types
        if not any(_is_type(value, t) for t in types):
            slot_hint = " or a slot word (AWAITING_RULING, AUTHOR)" if node.get("x-slot") else ""
            shown = repr(value) if isinstance(value, (str, int, float, bool)) else type(value).__name__
            errs.append(f"{path}: expected {' or '.join(types)}{slot_hint}, got {shown}")
            return
    if "const" in node and value != node["const"]:
        errs.append(f"{path}: must be {node['const']!r}")
    if ("minimum" in node and isinstance(value, (int, float)) and not isinstance(value, bool)
            and value < node["minimum"]):
        errs.append(f"{path}: {value} is below the minimum of {node['minimum']}")
    if "enum" in node and value not in node["enum"]:
        errs.append(f"{path}: {value!r} is not one of {', '.join(map(str, node['enum']))}")
    if isinstance(value, str):
        if "pattern" in node and not re.search(node["pattern"], value):
            errs.append(f"{path}: {value!r} does not match {node['pattern']}")
        if len(value) < node.get("minLength", 0):
            errs.append(f"{path}: shorter than {node['minLength']} characters")
    if isinstance(value, list):
        if len(value) < node.get("minItems", 0):
            errs.append(f"{path}: needs at least {node['minItems']} item(s)")
        if "items" in node:
            for i, item in enumerate(value):
                validate(item, node["items"], root, f"{path}[{i}]", errs)
    if isinstance(value, dict):
        props = node.get("properties", {})
        for key in node.get("required", []):
            if key not in value:
                errs.append(f"{path}.{key}: required")
        for key, item in value.items():
            if key in props:
                validate(item, props[key], root, f"{path}.{key}", errs)
            elif node.get("additionalProperties") is False:
                errs.append(f"{path}.{key}: not a sheet field")


# ------------------------------------------------------------------ sheet handling

def load_schema() -> dict:
    return json.load(open(SCHEMA_PATH))


def normalise(raw: dict) -> tuple:
    """Accept the two older sheet forms unchanged. Returns (sheet, note)."""
    if not isinstance(raw, dict):
        raise DesignError("not a design sheet: the file's top level is not a JSON object")
    if "kind" in raw:
        return raw, None
    if "rank" in raw and "objectives" in raw:          # a bare mission.py sheet
        name = raw.get("name") if isinstance(raw.get("name"), str) else None
        src = raw.get("srcId") if isinstance(raw.get("srcId"), str) else None
        sid = re.sub(r"[^a-z0-9_]", "_", (src or name or "mission").lower())
        return ({"sheet_version": "1", "kind": "quest", "id": sid[:63] or "mission",
                 "title": name or "AUTHOR",
                 "brief": {"purpose": "AUTHOR", "audience": f"rank {raw['rank']} mission",
                           "home": "mission hall", "size": "single"},
                 "mission": raw},
                "read as a mission sheet (mission.py form) and wrapped as kind quest")
    if "identity" in raw and "structure" in raw:       # a bare 26x event sheet instance
        ident = raw["identity"] if isinstance(raw["identity"], dict) else {}
        name = ident.get("name") if isinstance(ident.get("name"), str) and ident.get("name") else None
        theme = ident.get("theme") if isinstance(ident.get("theme"), str) and ident.get("theme") else None
        sid = re.sub(r"[^a-z0-9_]", "_", (name or "event").lower())
        return ({"sheet_version": "1", "kind": "event", "id": sid[:63] or "event",
                 "title": name or "AUTHOR",
                 "brief": {"purpose": theme or "AUTHOR",
                           "audience": "AUTHOR", "home": "AUTHOR", "size": "event"},
                 "event": raw},
                "read as an event sheet (26x form) and wrapped as kind event")
    raise DesignError("not a design sheet: no `kind`, and not a mission or event sheet either")


def check_legacy(sheet: dict, errs: list) -> None:
    """The two older sheets ride as opaque objects in the schema, because their owners validate
    them at build time. The few container types this tool itself reads are checked here, so a
    malformed one is a diagnostic and never reaches the renderer."""
    def expect(holder, key, kinds, where, required=False):
        if key not in holder:
            if required:
                errs.append(f"{where}.{key}: required")
            return
        if not isinstance(holder[key], kinds) or isinstance(holder[key], bool):
            names = " or ".join(k.__name__ for k in (kinds if isinstance(kinds, tuple) else (kinds,)))
            errs.append(f"{where}.{key}: expected {names}, got {type(holder[key]).__name__}")

    for where, mission in (("sheet.mission", sheet.get("mission")),
                           ("sheet.quest.mission", (sheet.get("quest") or {}).get("mission")
                            if isinstance(sheet.get("quest"), dict) else None)):
        if not isinstance(mission, dict):
            continue
        expect(mission, "rank", str, where, required=True)
        expect(mission, "name", str, where)
        expect(mission, "objectives", list, where, required=True)
        expect(mission, "roster", list, where)
        for key in ("objectives", "roster"):
            if isinstance(mission.get(key), list):
                for i, item in enumerate(mission[key]):
                    if not isinstance(item, dict):
                        errs.append(f"{where}.{key}[{i}]: expected dict, got {type(item).__name__}")
    event = sheet.get("event")
    if isinstance(event, dict):
        for key in ("identity", "structure", "enemies", "economy"):
            expect(event, key, dict, "sheet.event")
        if isinstance(event.get("identity"), dict):
            for key in ("name", "theme"):
                expect(event["identity"], key, str, "sheet.event.identity")


def walk(value, path=""):
    yield path, value
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk(item, f"{path}.{key}" if path else key)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from walk(item, f"{path}[{i}]")


def find_slots(sheet: dict) -> list:
    out = []
    for path, value in walk(sheet):
        if value in SLOTS:
            out.append((path, value))
        elif value == LEGACY_SLOT and (path == "event" or path.startswith("event.")
                                       or path.startswith("event[")):
            out.append((path, "AWAITING_RULING"))
    return out


def library_index() -> dict:
    """{family: set(ids)} from data/libraries/<family>.json: {"entries": {"<id>": {...}}}."""
    index = {}
    if os.path.isdir(LIB_DIR):
        for name in sorted(os.listdir(LIB_DIR)):
            if name.endswith(".json"):
                data = json.load(open(os.path.join(LIB_DIR, name)))
                index[name[:-5]] = set(data.get("entries", {}))
    return index


def library_refs(sheet: dict) -> list:
    refs = []
    for path, value in walk(sheet):
        if path.startswith("mission") or path.startswith("event"):
            continue
        leaf = path.rsplit(".", 1)[-1]
        if leaf in ("use", "structure", "recipe") and isinstance(value, str) and value not in SLOTS:
            refs.append((path, value))
    return refs


def check_engine_keys(sheet: dict, forbidden: dict, errs: list) -> None:
    for path, value in walk(sheet):
        if not path or path == "event" or path.startswith("event.") or path.startswith("event["):
            continue                                  # the 26x form predates this rule; see sheet.md
        if ".params" in path or path.endswith("params"):
            continue                                  # library parameters are bounded by their entry
        leaf = re.sub(r"\[\d+\]$", "", path.rsplit(".", 1)[-1])
        if path.startswith("mission.") and path.count(".") > 1:
            continue                                  # only the mission sheet's top level is the sheet
        if path.startswith("mission.") and not forbidden.get(leaf, "").startswith("48_"):
            continue                                  # `rank` selects the profile there; it is not the AI field
        if leaf in forbidden:
            errs.append(f"{path}: a sheet cannot reach `{leaf}`; it is derived at build time "
                        f"(owner: {forbidden[leaf]})")


def check_payout(sheet: dict, errs: list) -> None:
    for block in ("payout", "tuning"):
        for path, value in walk(sheet.get(block) or {}, block):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            parent = path.rsplit(".", 1)[0]
            holder = sheet
            for part in re.findall(r"[^.\[\]]+", parent):
                holder = holder[int(part)] if part.isdigit() else holder[part]
            if not (isinstance(holder, dict) and holder.get("source")):
                errs.append(f"{path}: a number with no source; cite its owner or leave "
                            f"AWAITING_RULING (D-reserved-dauntless)")


def lint_text(sheet: dict, schema: dict, bounds: dict, errs: list, warns: list) -> None:
    """Runs only on a structurally valid sheet, so every entry has for, entity, field, text."""
    entity_map = schema["_meta"]["text_entities"]
    field_map = schema["_meta"]["text_fields"]
    banned = (sheet.get("voice") or {}).get("banned_words", [])
    unbounded = set()
    for i, entry in enumerate((sheet.get("text") or {}).get("entries", [])):
        where = f"text.entries[{i}] ({entry['for']}, {entry['entity']}.{entry['field']})"
        text, field = entry["text"], entry["field"]
        if text in SLOTS:
            continue
        if not text.strip():
            errs.append(f"{where}: empty text; write it or leave AUTHOR")
            continue
        if field in DIALOG_FIELDS and EM_DASH in text:
            errs.append(f"{where}: em dash in player-facing dialog (D-emdash-dialog, lint L11)")
        elif EM_DASH in text and entry.get("player_facing", True):
            warns.append(f"{where}: em dash in player-facing text; banned in dialog only, but "
                         f"shipped events keep it out of all player text (references/writing.md)")
        if field in ("battleDescription", "log_line"):
            for token in re.findall(r"%[A-Za-z]+", text):
                if token not in BATTLE_PLACEHOLDERS:
                    errs.append(f"{where}: unknown placeholder {token}; the engine knows "
                                f"{', '.join(BATTLE_PLACEHOLDERS)} (references/jutsu.md 2)")
        contract, record_field = entity_map.get(entry["entity"]), field_map.get(field)
        if record_field is None:
            pass                                      # an objective-level field: no entity bound exists
        elif contract is None:
            unbounded.add(entry["entity"])
        elif contract not in bounds:
            errs.append(f"{where}: cannot check its length: no `{contract}` contract in 45d "
                        f"(is building-tnr-content present and current?)")
        else:
            lo, hi = bounds[contract].get(record_field, (None, None))
            if hi is not None and len(text) > hi:
                errs.append(f"{where}: {len(text)} characters, over the schema bound of {hi} "
                            f"(45d {contract}.{record_field})")
            if lo is not None and len(text) < lo:
                errs.append(f"{where}: under the schema bound of {lo} characters "
                            f"(45d {contract}.{record_field})")
        if entry.get("player_facing", True):
            for word in banned:
                if re.search(r"\b" + re.escape(word) + r"\b", text, re.I):
                    errs.append(f"{where}: banned word '{word}' (this sheet's voice.banned_words)")
    for entity in sorted(unbounded):
        warns.append(f"text for entity `{entity}` has no generated length contract; its lengths "
                     f"were not checked")
    if not banned and (sheet.get("text") or {}).get("entries"):
        warns.append("voice.banned_words is empty; an event with a story bible should list its "
                     "\"never use\" words here")


def check(raw) -> dict:
    """Never raises on any parsed JSON value: every problem comes back as a diagnostic."""
    result = {"sheet": None, "errors": [], "warnings": [], "slots": [],
              "pending_library_refs": [], "open_decisions": [], "structural": True}
    errs, warns = result["errors"], result["warnings"]
    try:
        sheet, note = normalise(raw)
    except DesignError as err:
        errs.append(str(err))
        return result
    result["sheet"] = sheet
    schema = load_schema()
    if note:
        warns.append(note)
    validate(sheet, schema, schema, "sheet", errs)
    kind = sheet.get("kind")
    block = schema["_meta"]["kind_blocks"].get(kind) if isinstance(kind, str) else None
    wrapped_mission = isinstance(kind, str) and kind == "quest" and "mission" in sheet and "quest" not in sheet
    if block and block not in sheet and not wrapped_mission:
        errs.append(f"sheet.{block}: required for kind {kind}")
    check_legacy(sheet, errs)
    result["structural"] = bool(errs)
    try:
        check_engine_keys(sheet, engine_keys(), errs)      # a plain walk: safe on any shape
        bounds = entity_bounds()
    except DesignError as err:
        errs.append(str(err))
        bounds = {}
    result["slots"] = find_slots(sheet)                    # also a plain walk
    if result["structural"]:
        # The checks below read fields by name. On a sheet whose shape is wrong they would
        # either crash or report nonsense, so they wait until the structure is valid.
        warns.append("structure errors above: the payout, text and library checks were not run")
        return result
    check_payout(sheet, errs)
    lint_text(sheet, schema, bounds, errs, warns)
    index = library_index()
    for path, ref in library_refs(sheet):
        family = ref.split("/", 1)[0]
        if family not in index:
            result["pending_library_refs"].append((path, ref))
        elif ref not in index[family]:
            errs.append(f"{path}: '{ref}' is not in the {family} library")
    result["open_decisions"] = [d for d in sheet.get("decisions", []) if d["status"] == "open"]
    return result


# ------------------------------------------------------------------ new

def _enemy(key: str) -> dict:
    return {"key": key, "name": "AUTHOR", "role": "AWAITING_RULING", "level": "AWAITING_RULING",
            "combat_role": "AUTHOR", "tactical_read": "AUTHOR", "rules": [],
            "loadout": {"kit": [], "signatures": []}, "art": []}


def scaffold(kind: str, sid: str, title: str) -> dict:
    sheet = {
        "sheet_version": "1", "kind": kind, "id": sid, "title": title,
        "brief": {"purpose": "AUTHOR", "audience": "AUTHOR", "home": "AUTHOR",
                  "size": {"ai": "single", "ai_line": "small", "quest": "single"}.get(kind, "event"),
                  "agreed": False},
        "concept": {"hook": "AUTHOR", "fantasy": "AUTHOR", "references": [], "options": [],
                    "chosen": "AWAITING_RULING"},
        "voice": {"register": "", "banned_words": []},
    }
    if kind == "ai":
        sheet["enemy"] = _enemy("enemy")
    elif kind == "ai_line":
        sheet["line"] = {"name": "AUTHOR", "premise": "AUTHOR",
                         "rungs": [_enemy("rung_1"), _enemy("rung_2")], "build_order": []}
    elif kind == "boss":
        sheet["boss"] = {"enemy": _enemy("boss"), "bible": "AUTHOR",
                         "acts": [{"id": "act1", "title": "AUTHOR",
                                   "script": [{"when": "round 1", "beat": "AUTHOR"}],
                                   "telegraphs": [{"omen": "AUTHOR", "payoff": "AUTHOR",
                                                   "rounds_between": "AWAITING_RULING"}]}],
                         "enrage": "AWAITING_RULING"}
        sheet["tuning"] = {"targets": [{"profile": "AWAITING_RULING", "metric": "clear rate",
                                        "value": "AWAITING_RULING"}]}
    elif kind == "quest":
        sheet["quest"] = {"structure": "quest_structure/single_battle/v1", "summary": "AUTHOR",
                          "gating": "AUTHOR", "enemies": [], "setup": []}
    elif kind == "quest_chain":
        sheet["chain"] = {"premise": "AUTHOR", "quests": [
            {"id": "q1", "structure": "quest_structure/single_battle/v1", "summary": "AUTHOR"},
            {"id": "q2", "structure": "quest_structure/single_battle/v1", "summary": "AUTHOR",
             "after": "q1"}], "enemies": []}
    elif kind == "dungeon":
        sheet["dungeon"] = {"premise": "AUTHOR", "enemies": [_enemy("mob")], "floors": [
            {"id": "floor1", "waves": [{"enemies": [{"key": "mob", "count": "AWAITING_RULING"}],
                                        "delay_rounds": "AWAITING_RULING"}]}]}
    elif kind == "event":
        sheet["event"] = {"identity": {"name": title, "theme": "AUTHOR"}, "structure": {},
                          "enemies": {"roster": []}, "economy": {}}
    if kind != "ai":
        sheet["payout"] = {"entries": [{"for": sid, "what": "completion reward",
                                        "value": "AWAITING_RULING"}]}
    sheet["text"] = {"entries": []}
    sheet["art"] = {"slots": []}
    sheet["decisions"] = []
    return sheet


def cmd_new(args) -> int:
    if args.kind not in KINDS:
        raise DesignError(f"kind must be one of: {', '.join(KINDS)}")
    sid = args.id or f"new_{args.kind}"
    if getattr(args, "source", None):
        sheet, _ = normalise(json.load(open(args.source)))
        sheet = copy.deepcopy(sheet)
        if sheet["kind"] != args.kind:
            raise DesignError(f"--from sheet is kind {sheet['kind']}, not {args.kind}")
        sheet["id"] = sid
        if args.title:
            sheet["title"] = args.title
    else:
        sheet = scaffold(args.kind, sid, args.title or "AUTHOR")
    text = json.dumps(sheet, indent=1, ensure_ascii=False) + "\n"
    if args.out:
        open(args.out, "w", encoding="utf-8").write(text)
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(text)
    return 0


# ------------------------------------------------------------------ check / explain / compile

def report(result: dict) -> str:
    lines = []
    for e in result["errors"]:
        lines.append(f"ERROR  {e}")
    for w in result["warnings"]:
        lines.append(f"note   {w}")
    for path, ref in result["pending_library_refs"]:
        lines.append(f"pending library  {path}: '{ref}' (its library has not shipped; compile will refuse)")
    for path, kind in result["slots"]:
        lines.append(f"open slot  {kind}  {path}")
    for d in result["open_decisions"]:
        lines.append(f"open decision  {d['id']}: {d['topic']}")
    lines.append(f"\n{len(result['errors'])} error(s), {len(result['slots'])} open slot(s), "
                 f"{len(result['pending_library_refs'])} pending library reference(s), "
                 f"{len(result['open_decisions'])} open decision(s)")
    return "\n".join(lines)


def cmd_check(args) -> int:
    result = check(json.load(open(args.sheet)))
    if args.json:
        out = {k: v for k, v in result.items() if k not in ("sheet", "structural")}
        print(json.dumps(out, indent=1))
    else:
        print(report(result))
    return 1 if result["errors"] else 0


def _cell(value) -> str:
    if isinstance(value, dict):
        if "reward_package" in value:
            return f"reward package `{value['reward_package']}`"
        if "value" in value:
            return f"{value['value']} (source: {value['source']})"
    return str(value).replace("|", "/")


def _params(params) -> str:
    if not params:
        return ""
    return " (" + ", ".join(f"{k} = {json.dumps(v, ensure_ascii=False)}" for k, v in sorted(params.items())) + ")"


def _ref(ref: dict) -> str:
    return f"`{ref['use']}`{_params(ref.get('params'))}" + (f": {ref['note']}" if ref.get("note") else "")


def leaves(value, path=""):
    """Every scalar on the sheet, by path. The appendix of the design doc is built from this, so
    no choice on a sheet can be missing from the document the director reads."""
    if isinstance(value, dict):
        if not value:
            yield path, "{}"
        for key, item in value.items():
            yield from leaves(item, f"{path}.{key}" if path else key)
    elif isinstance(value, list):
        if not value:
            yield path, "[]"
        for i, item in enumerate(value):
            yield from leaves(item, f"{path}[{i}]")
    else:
        yield path, json.dumps(value, ensure_ascii=False)


def _enemy_md(e: dict) -> list:
    out = [f"**{e.get('name')}**" + (f", {e['title']}" if e.get("title") else ""),
           f"- Role: {e.get('role')}. Level: {e.get('level')}."
           + (f" Element: {e['element']}." if e.get("element") else "")]
    kit = e.get("loadout", {})
    for label, key in (("Tagline", "tagline"), ("Rank flavour", "rank_flavour"),
                       ("In a fight", "combat_role"), ("How to beat it", "tactical_read")):
        if e.get(key):
            out.append(f"- {label}: {e[key]}")
    for r in e.get("rules", []):
        out.append(f"- Behaviour: {_ref(r)}")
    for ph in e.get("phases", []):
        out.append(f"- Phase {ph['id']} (when: {ph['trigger']})"
                   + (f", cue: {ph['cue']}" if ph.get("cue") else "") + ":")
        out += [f"  - {_ref(r)}" for r in ph["rules"]]
    if kit.get("recipe"):
        out.append(f"- Loadout recipe: `{kit['recipe']}`")
    if kit.get("kit"):
        out.append("- Kit (pool codes): " + ", ".join(kit["kit"]))
    for sig in kit.get("signatures", []):
        out.append(f"- Signature: {sig['name']}: {sig['intent']}"
                   + (" (telegraphed)" if sig.get("telegraphs") else ""))
    return out + [""]


def explain(result: dict) -> str:
    if result["structural"] or result["sheet"] is None:
        raise DesignError("explain: the sheet's structure is not valid; run check")
    s = result["sheet"]
    md = [f"# {s['title']}", "",
          "<!-- GENERATED by design.py explain from the design sheet. Edit the sheet, never this file. -->",
          "", f"Kind: {s['kind']}. Sheet id: `{s['id']}`.", "", "## Brief", ""]
    b = s["brief"]
    md += [f"- Purpose: {b['purpose']}", f"- Audience: {b['audience']}", f"- Where it lives: {b['home']}",
           f"- Size: {b['size']}", f"- Agreed by the director: {'yes' if b.get('agreed') else 'not yet'}", ""]
    c = s.get("concept")
    if c:
        md += ["## Concept", "", f"- Hook: {c.get('hook')}", f"- Fantasy: {c.get('fantasy')}"]
        for opt in c.get("options", []):
            md.append(f"- Option {opt['id']}: {opt['pitch']}")
        md += [f"- Chosen: {c.get('chosen')}", ""]
    enemies = []
    if "enemy" in s:
        enemies = [s["enemy"]]
    elif "line" in s:
        md += ["## Line", "", f"{s['line'].get('name')}: {s['line'].get('premise', '')}", ""]
        enemies = s["line"]["rungs"]
    elif "boss" in s:
        enemies = [s["boss"]["enemy"]] + s["boss"].get("allies", [])
    else:
        for key in ("quest", "chain", "dungeon"):
            enemies += (s.get(key) or {}).get("enemies", [])
    if "quest" in s:
        md += ["## Quest", "", f"- Structure: `{s['quest']['structure']}`{_params(s['quest'].get('params'))}",
               f"- Summary: {s['quest'].get('summary')}", f"- Gating: {s['quest'].get('gating')}"]
        md += [f"- Setup: {_ref(r)}" for r in s["quest"].get("setup", [])] + [""]
    if "mission" in s:
        m = s["mission"]
        md += ["## Mission sheet", "", f"- Rank {m.get('rank')}: {m.get('name')}",
               f"- {len(m.get('objectives', []))} objective(s), {len(m.get('roster') or [])} enemy(ies)", ""]
    if "chain" in s:
        md += ["## Chain", "", f"{s['chain'].get('premise', '')}", ""] + [f"- `{q['id']}`: `{q['structure']}`{_params(q.get('params'))}"
                                  + (f", after `{q['after']}`" if q.get("after") else "")
                                  + f": {q.get('summary')}" for q in s["chain"]["quests"]] + [""]
    if "dungeon" in s:
        md += ["## Dungeon", "", f"{s['dungeon'].get('premise', '')}", ""]
        for fl in s["dungeon"]["floors"]:
            md.append(f"- {fl['id']}{' (boss floor)' if fl.get('boss_floor') else ''}:")
            for n, w in enumerate(fl["waves"], 1):
                mobs = " + ".join(f"{m['count']} x {m['key']}" for m in w["enemies"])
                delay = w.get("delay_rounds")
                md.append(f"  - wave {n}: {mobs}"
                          + (f", arriving after {delay} round(s)" if delay is not None else ""))
        md.append("")
    if "event" in s:
        ident = s["event"].get("identity", {})
        md += ["## Event sheet", "", f"- {ident.get('name')}: {ident.get('theme')}", ""]
    if enemies:
        md += ["## Enemies", ""]
        for e in enemies:
            md += _enemy_md(e)
    if "boss" in s:
        md += ["## Fight", "", f"Character bible: {s['boss'].get('bible')}", ""]
        for act in s["boss"]["acts"]:
            md.append(f"### {act['id']}: {act['title']}")
            md += [f"- {beat['when']}: {beat['beat']}" for beat in act.get("script", [])]
            md += [f"- Telegraph: {t['omen']} then {t['payoff']} "
                   f"({t.get('rounds_between', '?')} round(s) later)" for t in act.get("telegraphs", [])]
            md.append("")
        if s["boss"].get("anti_camping"):
            md.append(f"Anti-camping: {_ref(s['boss']['anti_camping'])}\n")
        md.append(f"Enrage: {_cell(s['boss'].get('enrage', 'not set'))}\n")
    for title, block, cols in (("Payouts", "payout", ("for", "what")), ("Tuning targets", "tuning", ("profile", "metric"))):
        rows = (s.get(block) or {}).get("entries" if block == "payout" else "targets", [])
        if rows:
            md += [f"## {title}", "", f"| {cols[0].title()} | {cols[1].title()} | Value |", "|---|---|---|"]
            md += [f"| {r[cols[0]]} | {r[cols[1]]} | {_cell(r['value'])} |" for r in rows] + [""]
    rows = (s.get("text") or {}).get("entries", [])
    if rows:
        md += ["## Text", "", "| For | Field | Text |", "|---|---|---|"]
        md += [f"| {r['for']} | {r['field']} | {_cell(r['text'])} |" for r in rows] + [""]
    rows = (s.get("art") or {}).get("slots", [])
    if rows:
        md += ["## Art slots", "", "| Slot | For | Goes to |", "|---|---|---|"]
        md += [f"| {r['id']} | {r['for']} | {r['handoff']} |" for r in rows] + [""]
    md += ["## Open items", ""]
    if not (result["slots"] or result["pending_library_refs"] or result["open_decisions"] or result["errors"]):
        md.append("None. The sheet is complete.")
    md += [f"- Error: {e}" for e in result["errors"]]
    md += [f"- {kind}: `{path}`" for path, kind in result["slots"]]
    md += [f"- Library not shipped yet: `{ref}` at `{path}`" for path, ref in result["pending_library_refs"]]
    for d in result["open_decisions"]:
        md += ["", "```", f"GO? {d['id']} {d['topic']}",
               f"What changes:  {d.get('consequence', '-')}",
               f"Needs you:  {' / '.join(d.get('options', [])) or 'a decision'}",
               f"Blocks:  {d.get('blocks', '-')}", "```"]
    md += ["", "## Every value on the sheet", "",
           "The sections above are the readable design. This list is complete by construction: every",
           "value on the sheet appears here, so nothing can be on the sheet and missing from this document.",
           "", "| Path | Value |", "|---|---|"]
    md += [f"| `{path}` | {value.replace('|', '/')} |" for path, value in leaves(s)]
    return "\n".join(md).rstrip() + "\n"


def cmd_explain(args) -> int:
    result = check(json.load(open(args.sheet)))
    if result["structural"]:
        print("explain refused: the sheet's structure is not valid, so a design doc built from it "
              "would misstate the design. Fix these first:")
        for e in result["errors"]:
            print("  " + e)
        return 1
    text = explain(result)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(text)
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(text)
    return 0


def compile_refusal(result: dict) -> list:
    """Why this sheet cannot be compiled. Empty only when a compiler for its kind exists."""
    why = [f"error: {e}" for e in result["errors"]]
    why += [f"open slot: {kind} at {path}" for path, kind in result["slots"]]
    why += [f"library not shipped: {ref} at {path}" for path, ref in result["pending_library_refs"]]
    why += [f"open decision: {d['id']}" for d in result["open_decisions"]]
    kind = (result["sheet"] or {}).get("kind")
    if not isinstance(kind, str) or kind not in COMPILE_PHASE:
        return why                                    # the kind error is already in the list
    why.append(f"compile for kind '{kind}' is delivered in phase {COMPILE_PHASE[kind]} of the "
               f"skill overhaul; this build has new, check and explain only")
    return why


def cmd_compile(args) -> int:
    why = compile_refusal(check(json.load(open(args.sheet))))
    print("compile refused:")
    for line in why:
        print("  " + line)
    return 3


# ------------------------------------------------------------------ selftest

def selftest() -> int:
    checks, failures = [], []

    def want(cond, label):
        checks.append(label)
        if not cond:
            failures.append(label)

    schema = load_schema()
    want(set(schema["_meta"]["kind_blocks"]) == set(KINDS), "schema and tool agree on the kinds")

    # 1. Every scaffold is schema-clean and reports its open slots instead of failing.
    for kind in KINDS:
        r = check(scaffold(kind, f"t_{kind}", "Test"))
        want(not r["errors"], f"new {kind}: scaffold checks clean ({r['errors'][:1]})")
        want(len(r["slots"]) >= 3, f"new {kind}: open slots are reported, not hidden")
        want(compile_refusal(r) != [], f"new {kind}: compile refuses")

    base = scaffold("ai", "t_ai", "Test")

    # 2. A sheet cannot reach an engine field.
    bad = copy.deepcopy(base)
    bad["enemy"]["poolsMultiplier"] = 2
    r = check(bad)
    want(any("cannot reach `poolsMultiplier`" in e for e in r["errors"]),
         "an AI multiplier on the sheet is refused, naming its owner")
    bad = copy.deepcopy(scaffold("quest", "t_q", "Test"))
    bad["maxAttempts"] = 3
    want(any("cannot reach `maxAttempts`" in e for e in check(bad)["errors"]),
         "a mission profile field on the sheet is refused")
    wrapped = {"rank": "D", "name": "Old Sheet", "description": "x", "successDescription": "y",
               "objectives": [{"id": "n1", "task": "dialog"}]}
    r = check(wrapped)
    want(not r["errors"] and r["sheet"]["kind"] == "quest", "a bare mission sheet is accepted and wrapped")
    want(any("cannot reach `maxAttempts`" in e for e in check(dict(wrapped, maxAttempts=9))["errors"]),
         "the mission sheet's top level is held to the same rule")
    want(not check(dict(wrapped, objectives=[{"id": "n1", "task": "dialog", "hidden": True}]))["errors"],
         "objective nodes inside a mission sheet are the build skill's to check, not this rule's")

    # 3. The event sheet form rides unchanged, and its older slot word counts as open.
    ev = {"identity": {"name": "Tide Fair", "theme": "t", "gates": {"maxAttempts": "dauntless"}},
          "structure": {"pattern": "pyramid"}}
    r = check(ev)
    want(not r["errors"] and r["sheet"]["kind"] == "event", "a bare event sheet is accepted and wrapped")
    want(("event.identity.gates.maxAttempts", "AWAITING_RULING") in r["slots"],
         "'dauntless' in an event sheet is reported as an open ruling slot")

    # 4. Numbers need a source.
    pay = copy.deepcopy(scaffold("quest", "t_q", "Test"))
    pay["payout"]["entries"][0]["value"] = 5000
    want(any("none of the allowed forms" in e for e in check(pay)["errors"]), "a bare payout number is refused")
    pay["payout"]["entries"][0]["value"] = {"value": 5000, "source": "RUL-0000-00-00-000"}
    want(not check(pay)["errors"], "a number with its source is accepted")
    pay["payout"]["entries"][0]["value"] = {"reward_package": "S-Rank Dungeons Level 100"}
    want(not check(pay)["errors"], "a reward-package reference is accepted")
    pay["payout"]["entries"][0]["value"] = {"value": 5000, "source": ""}
    want(check(pay)["errors"] != [], "an empty source is refused")

    # 5. Library references: pending while no library exists, never silently accepted.
    lib = copy.deepcopy(base)
    lib["enemy"]["rules"] = [{"use": "rule_pattern/telegraph_payoff/v1", "params": {"statsMultiplier": 1}}]
    r = check(lib)
    want(r["pending_library_refs"] == [("enemy.rules[0].use", "rule_pattern/telegraph_payoff/v1")]
         or "rule_pattern" in library_index(), "an unshipped library reference is reported as pending")
    want(not any("statsMultiplier" in e for e in r["errors"]),
         "library parameters are not mistaken for sheet fields")
    lib["enemy"]["rules"] = [{"use": "Telegraph Payoff"}]
    want(any("does not match" in e for e in check(lib)["errors"]), "a library id must be a versioned id")

    # 6. Text lint.
    txt = copy.deepcopy(base)
    txt["text"]["entries"] = [
        {"for": "n1", "entity": "quest", "field": "dialog", "text": "Wait — not yet."},
        {"for": "j1", "entity": "jutsu", "field": "battleDescription", "text": "%user strikes %enemy"},
        {"for": "j2", "entity": "jutsu", "field": "battleDescription", "text": "%user strikes %target"},
        {"for": "q", "entity": "quest", "field": "name", "text": "x" * 400},
        {"for": "j3", "entity": "jutsu", "field": "description", "text": "AUTHOR"},
        {"for": "j4", "entity": "jutsu", "field": "description", "text": "It hums like a lattice."}]
    txt["voice"]["banned_words"] = ["lattice"]
    r = check(txt)
    want(any("em dash" in e and "entries[0]" in e for e in r["errors"]), "em dash in dialog is refused")
    want(any("%enemy" in e for e in r["errors"]), "an unknown battle placeholder is refused")
    want(not any("entries[2]" in e for e in r["errors"]), "a correct battle line passes")
    want(any("entries[3]" in e and "bound" in e for e in r["errors"]) or not entity_bounds(),
         "a name over the schema bound is refused")
    want(("text.entries[4].text", "AUTHOR") in r["slots"], "unwritten text is an open slot, not an error")
    want(any("banned word 'lattice'" in e for e in r["errors"]), "the sheet's banned words are enforced")

    # 7. Structure errors are named by path.
    broken = copy.deepcopy(base)
    del broken["enemy"]["loadout"]
    broken["enemy"]["surprise"] = 1
    r = check(broken)
    want(any(e.startswith("sheet.enemy.loadout: required") for e in r["errors"]), "a missing block is named")
    want(any("sheet.enemy.surprise: not a sheet field" in e for e in r["errors"]), "an unknown key is named")
    want(any("required for kind ai" in e for e in check({k: v for k, v in base.items() if k != "enemy"})["errors"]),
         "the kind's own block is required")

    # 8. explain is generated from the sheet and carries the open items and the go card.
    done = copy.deepcopy(base)
    done["decisions"] = [{"id": "D-x", "topic": "Does it drop anything?", "status": "open",
                          "options": ["no drops", "a shared token"], "blocks": "build handoff"}]
    doc = explain(check(done))
    want("GENERATED by design.py explain" in doc and "GO? D-x Does it drop anything?" in doc,
         "explain renders the design doc and a go card per open decision")
    want("AWAITING_RULING: `enemy.level`" in doc, "explain lists every open slot by path")
    want(explain(check(done)) == doc, "explain is deterministic")

    # 10. The design doc shows every choice (review of 7441a87c, finding 1).
    dg = scaffold("dungeon", "t_d", "Test")
    dg["dungeon"]["floors"][0]["waves"][0]["delay_rounds"] = 0
    slow = copy.deepcopy(dg)
    slow["dungeon"]["floors"][0]["waves"][0]["delay_rounds"] = 10
    want(explain(check(dg)) != explain(check(slow)), "a changed wave delay changes the design doc")
    want("arriving after 10 round(s)" in explain(check(slow)), "the wave delay is in the readable section")
    rich = copy.deepcopy(base)
    rich["enemy"]["rules"] = [{"use": "rule_pattern/enrage/v1", "params": {"round": 12}}]
    want("rule_pattern/enrage/v1` (round = 12)" in explain(check(rich)), "rule parameters are rendered")
    qs = scaffold("quest", "t_q", "Test")
    qs["quest"]["params"] = {"floors": 3}
    want("(floors = 3)" in explain(check(qs)), "quest structure parameters are rendered")
    changed = unchanged = 0
    for kind in KINDS:
        sheet0 = scaffold(kind, f"t_{kind}", "Test")
        doc0 = explain(check(sheet0))
        for path, shown in leaves(sheet0):
            if shown in ("[]", "{}"):
                continue                               # an empty container has no value to change
            mutated = copy.deepcopy(sheet0)
            holder, parts = mutated, re.findall(r"[^.\[\]]+", path)
            for part in parts[:-1]:
                holder = holder[int(part)] if isinstance(holder, list) else holder[part]
            last = int(parts[-1]) if isinstance(holder, list) else parts[-1]
            holder[last] = "zz-mutated-zz"
            if explain({**check(sheet0), "sheet": mutated}) != doc0:
                changed += 1
            else:
                unchanged += 1
    want(changed > 100 and unchanged == 0,
         f"every value on every scaffold reaches the design doc ({unchanged} did not)")

    # 11. Malformed input comes back as diagnostics, never as a crash (finding 2).
    for label, breaker in (("text.entries: [null]", lambda x: x["text"].update(entries=[None])),
                           ("decisions: [null]", lambda x: x.update(decisions=[None])),
                           ("a numeric banned word", lambda x: x["voice"].update(banned_words=[5])),
                           ("payout: 7", lambda x: x.update(payout=7)),
                           ("kind: 3", lambda x: x.update(kind=3))):
        mal = copy.deepcopy(scaffold("quest", "t_q", "Test"))
        breaker(mal)
        try:
            r = check(mal)
            json.dumps({k: v for k, v in r.items() if k != "sheet"})
            want(r["errors"] != [] and r["structural"], f"{label}: reported as a structure error")
        except Exception as err:                       # noqa: BLE001 - the point is that none escapes
            want(False, f"{label}: reported as a structure error (raised {type(err).__name__})")
    for top in ([], "sheet", 5, None):
        r = check(top)
        want(r["errors"] != [] and r["sheet"] is None, f"a top-level {type(top).__name__} is a diagnostic")
    want(compile_refusal(check([])) != [], "compile refuses an unreadable sheet without crashing")

    # 12. Text bounds use the contract's entity names, and need the entity (finding 3).
    if entity_bounds():
        tb = copy.deepcopy(base)
        tb["text"]["entries"] = [{"for": "a1", "entity": "asset", "field": "name", "text": "x" * 400}]
        want(any("gameAsset.name" in e and "bound" in e for e in check(tb)["errors"]),
             "an asset name over its bound is refused (asset is gameAsset in 45d)")
        tb["text"]["entries"] = [{"for": "a1", "field": "name", "text": "x" * 400}]
        want(any("entity: required" in e for e in check(tb)["errors"]), "a text entry must name its entity")
        tb["text"]["entries"] = [{"for": "e1", "entity": "ai", "field": "name", "text": "Deck Warden"}]
        r = check(tb)
        want(not r["errors"] and any("`ai` has no generated length contract" in w for w in r["warnings"]),
             "an entity with no contract is said to be unchecked, not silently passed")
        mapped = schema["_meta"]["text_entities"]
        want(all(v is None or v in entity_bounds() for k, v in mapped.items() if k != "note"),
             "every mapped text entity exists in 45d")

    # 13. Numeric fields take an integer or a slot word, nothing else (finding 4).
    for label, setter in (
            ("level", lambda x, v: x["dungeon"]["enemies"][0].update(level=v)),
            ("enemy count", lambda x, v: x["dungeon"]["floors"][0]["waves"][0]["enemies"][0].update(count=v)),
            ("wave delay", lambda x, v: x["dungeon"]["floors"][0]["waves"][0].update(delay_rounds=v))):
        for value, ok in (("soon", False), (-1, False), (2.5, False), (True, False),
                          (3, True), ("AWAITING_RULING", True)):
            num = scaffold("dungeon", "t_d", "Test")
            setter(num, value)
            r = check(num)
            want((not r["errors"]) == ok, f"{label} = {value!r} is {'accepted' if ok else 'refused'}")
    tele = scaffold("boss", "t_b", "Test")
    tele["boss"]["acts"][0]["telegraphs"][0]["rounds_between"] = "soon"
    want(any("rounds_between" in e for e in check(tele)["errors"]), "telegraph spacing = 'soon' is refused")

    # 14. Malformed older sheets and a non-string kind (review of c33a558b). CLI, end to end.
    import contextlib, io, tempfile

    def cli(argv, payload):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(payload, fh)
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                code = main(argv + [fh.name])
        except BaseException as err:                    # noqa: BLE001 - a crash is the failure
            return f"raised {type(err).__name__}", out.getvalue()
        finally:
            os.unlink(fh.name)
        return code, out.getvalue()

    code, out = cli(["check", "--json"], {"identity": [], "structure": {}})
    try:
        parsed = json.loads(out)
    except ValueError:
        parsed = None
    want(code == 1 and parsed and any("event.identity" in e for e in parsed["errors"]),
         f"CLI: an event sheet with identity [] gives a JSON report, exit 1 (got {code})")
    bad_mission = {"rank": "D", "name": "Test mission", "objectives": None}
    code, out = cli(["check"], bad_mission)
    want(code == 1 and "mission.objectives: expected list" in out,
         f"CLI: a mission sheet with objectives null fails check (got {code})")
    code, out = cli(["explain"], bad_mission)
    want(code == 1 and "explain refused" in out, f"CLI: explain refuses that sheet (got {code})")
    bad_kind = dict(scaffold("quest", "t_q", "Test"), kind=[])
    code, out = cli(["check"], bad_kind)
    want(code == 1 and "sheet.kind" in out, f"CLI: kind [] fails check (got {code})")
    code, out = cli(["compile"], bad_kind)
    want(code == 3 and "sheet.kind" in out, f"CLI: compile refuses kind [] with the reason (got {code})")
    code, out = cli(["explain"], bad_kind)
    want(code == 1, f"CLI: explain refuses kind [] (got {code})")

    # 15. Sweep: put a wrong value at every position of every sheet form. Nothing may raise.
    forms = [scaffold(k, f"t_{k}", "Test") for k in KINDS]
    forms += [{"rank": "D", "srcId": "m", "name": "Old", "description": "x", "successDescription": "y",
               "objectives": [{"id": "n1", "task": "dialog"}], "roster": [{"name": "Thug", "kit": ["S01"]}]},
              {"identity": {"name": "Fair", "theme": "t", "gates": {}}, "structure": {"pattern": "pyramid"},
               "enemies": {"roster": []}, "economy": {}}]
    full = scaffold("boss", "t_full", "Test")
    full["boss"]["enemy"]["rules"] = [{"use": "rule_pattern/x/v1", "params": {"a": 1}}]
    full["boss"]["enemy"]["phases"] = [{"id": "p2", "trigger": "below half", "rules": []}]
    full["boss"]["anti_camping"] = {"use": "rule_pattern/absence/v1"}
    full["text"]["entries"] = [{"for": "j", "entity": "jutsu", "field": "description", "text": "It burns."}]
    full["art"]["slots"] = [{"id": "a", "for": "boss", "handoff": "producing-tnr-art"}]
    full["decisions"] = [{"id": "D-x", "topic": "t", "status": "open", "options": ["a", "b"]}]
    full["payout"]["entries"][0]["value"] = {"value": 1, "source": "RUL-x"}
    forms.append(full)
    crashes, tried = [], 0
    for form in forms:
        paths = [p for p, _ in walk(form)]
        for path in paths:
            for wrong in (None, [], {}, "x", 5, True, [None], {"k": None}):
                mutated = copy.deepcopy(form)
                if path:
                    holder, parts = mutated, re.findall(r"[^.\[\]]+", path)
                    for part in parts[:-1]:
                        holder = holder[int(part)] if isinstance(holder, list) else holder[part]
                    holder[int(parts[-1]) if isinstance(holder, list) else parts[-1]] = wrong
                else:
                    mutated = wrong
                tried += 1
                try:
                    r = check(mutated)
                    json.dumps({k: v for k, v in r.items() if k != "sheet"})
                    report(r)
                    compile_refusal(r)
                    if not r["structural"] and r["sheet"] is not None:
                        explain(r)
                except Exception as err:                # noqa: BLE001
                    crashes.append(f"{path or '<top>'} = {wrong!r}: {type(err).__name__}: {err}")
    want(not crashes and tried > 2000,
         f"sweep of {tried} malformed sheets: check, report, compile and explain never raise "
         f"({len(crashes)} did; first: {crashes[:2]})")

    # 9. Without the build skill the engine-field rule cannot run, and check says so loudly.
    global build_skill_dirs
    real = build_skill_dirs
    build_skill_dirs = lambda: []
    try:
        r = check(copy.deepcopy(base))
        want(any("cannot find building-tnr-content" in e for e in r["errors"]),
             "a missing build skill is an error, never a silently skipped check")
    finally:
        build_skill_dirs = real

    for label in failures:
        print(f"  FAIL  {label}")
    print(f"\n{len(checks) - len(failures)} passed, {len(failures)} failed")
    return 1 if failures else 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--selftest"]:
        return selftest()
    ap = argparse.ArgumentParser(prog="design.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new"); p.add_argument("kind"); p.add_argument("--id"); p.add_argument("--title")
    p.add_argument("--from", dest="source"); p.add_argument("-o", "--out"); p.set_defaults(fn=cmd_new)
    p = sub.add_parser("check"); p.add_argument("sheet"); p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("explain"); p.add_argument("sheet"); p.add_argument("-o", "--out"); p.set_defaults(fn=cmd_explain)
    p = sub.add_parser("compile"); p.add_argument("sheet"); p.add_argument("-o", "--out"); p.set_defaults(fn=cmd_compile)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except DesignError as err:
        print(f"design.py: {err}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError) as err:
        print(f"design.py: cannot read input: {err}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
