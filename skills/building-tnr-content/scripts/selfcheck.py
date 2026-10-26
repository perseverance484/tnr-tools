#!/usr/bin/env python3
"""Check the bundled scripts and generated contracts for internal consistency."""

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATED = (
    "45c_DATA_constructors.json",
    "45d_DATA_entity_schemas.json",
    "45g_DATA_checks.json",
)


def load_json(path, errors):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.name} is unreadable: {error}")
        return None


def check_scripts(errors, notes):
    scripts = sorted(HERE.glob("*.py"))
    for path in scripts:
        try:
            ast.parse(path.read_text())
        except SyntaxError as error:
            errors.append(f"{path.name} does not parse: {error}")
    notes.append(f"{len(scripts)} bundled scripts parse")


def check_generated(gdir, errors, notes):
    loaded = {}
    sources = {}
    for name in GENERATED:
        path = gdir / name
        if not path.exists():
            errors.append(f"{name} not found in {gdir}; pass --generated <contract-dir> or sync the generated files first")
            continue
        data = load_json(path, errors)
        if data is None:
            continue
        loaded[name] = data
        provenance = data.get("_provenance") or {}
        source = (
            provenance.get("source_drop")
            or provenance.get("source")
            or provenance.get("extracted")
        )
        if source:
            sources[name] = source

    if len(set(sources.values())) > 1:
        errors.append(f"generated files come from different sources: {sources}")
    elif sources:
        notes.append(f"generated source: {next(iter(sources.values()))}")
    return loaded


def check_factory(gdir, loaded, errors, notes):
    if not all(name in loaded for name in GENERATED):
        return
    result = subprocess.run(
        [sys.executable, str(HERE / "factory.py"), "--selftest"],
        cwd=gdir,
        capture_output=True,
        text=True,
    )
    tail = (result.stdout.strip().splitlines() or ["no output"])[-1]
    (notes if result.returncode == 0 else errors).append("factory selftest: " + tail)


def check_validator(gdir, loaded, errors, notes):
    checks = loaded.get("45g_DATA_checks.json")
    if checks is None:
        return
    declared = {key for key in checks if not key.startswith("_")}
    result = subprocess.run(
        [sys.executable, str(HERE / "validate.py"), "--check-ids", "x"],
        cwd=gdir,
        capture_output=True,
        text=True,
    )
    try:
        implemented = set(json.loads(result.stdout)["checks"])
    except (json.JSONDecodeError, KeyError, TypeError):
        errors.append("validate.py --check-ids did not return an inventory")
        return
    missing = sorted(declared - implemented)
    errors.extend(f"45g declares '{name}' but validate.py does not consume it" for name in missing)
    notes.append(f"validate.py consumes {len(declared) - len(missing)}/{len(declared)} declared 45g blocks")


AIPROFILE_CREATE_MSG = "aiProfile cannot be created directly"

# One valid rule, so the fixtures below fail (or pass) on the entity/slot
# question alone rather than on rule grammar.
_RULE = {
    "conditions": [{"type": "distance_lower_than", "value": 6, "target": "RANDOM_OPPONENT"}],
    "action": {"type": "use_specific_jutsu", "jutsuId": "YiRdVytsdxFzZtqkEDs5Q",
               "target": "RANDOM_OPPONENT"},
}
# No preferredStat: migration 0056 dropped it and Forge refuses the key (RUL-2026-10-25-009).
_AI_REQ = {"rank": "JONIN", "regeneration": 60,
           "preferredGeneral1": "Strength", "preferredGeneral2": "Speed"}

# Forge 0.4.1 refuses a standalone aiProfile create at parse time
# (forge/src/runner/manifest.mjs), and its aiProfile recipe is update-only.
# push/47 reached a frozen handoff carrying two of them because this validator
# said nothing: it was green while the runner would not open a job. These three
# fixtures pin both halves of the contract - the create is refused, and the two
# shapes Forge DOES support are not.
RUNNER_CONTRACT_FIXTURES = (
    ("aiProfile create", True, {"items": [
        {"entity": "aiProfile", "slot": "create", "name": "Probe", "srcId": "probe",
         "data": {"name": "Probe", "hidden": True, "rules": [_RULE],
                  "includeDefaultRules": True}}]}),
    ("aiProfile edit", False, {"items": [
        {"entity": "aiProfile", "slot": "edit", "name": "Probe",
         "targetId": "YiRdVytsdxFzZtqkEDs5Q",
         "data": {"rules": [_RULE], "includeDefaultRules": True}}]}),
    ("ai create carrying rules", False, {"items": [
        {"entity": "ai", "slot": "create", "name": "Probe", "srcId": "probe",
         "data": dict(_AI_REQ, username="Probe", hidden=True, level=100,
                      jutsus=["YiRdVytsdxFzZtqkEDs5Q"], rules=[_RULE],
                      includeDefaultRules=True)}]}),
)


def check_runner_contract(gdir, loaded, errors, notes):
    """validate.py must agree with the Forge manifest contract on aiProfile."""
    if not all(name in loaded for name in GENERATED):
        return
    import tempfile
    for label, want_refused, manifest in RUNNER_CONTRACT_FIXTURES:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "probe.json"
            path.write_text(json.dumps(manifest))
            result = subprocess.run(
                [sys.executable, str(HERE / "validate.py"), str(path)],
                cwd=gdir, capture_output=True, text=True,
            )
        refused = AIPROFILE_CREATE_MSG in result.stdout
        if refused != want_refused:
            errors.append(
                f"runner contract: {label} was "
                f"{'not refused' if want_refused else 'refused'} by validate.py. "
                f"Forge 0.4.1 {'refuses' if want_refused else 'supports'} it "
                f"(forge/src/runner/manifest.mjs, recipes.mjs)")
    notes.append(f"runner contract: {len(RUNNER_CONTRACT_FIXTURES)} aiProfile "
                 "slot fixtures agree with Forge")


# RUL-2026-10-25-009: law 4 / L06 and law 14 / L05 against the pinned schemas.
# Each fixture is (label, manifest, diagnostic fragments that MUST appear, fragments that must NOT).
# WoundTag has generalTypes and no statTypes at the pin; DamageTag and PierceTag have both; the AI
# row has no preferredStat after migration 0056. Forge carries the same per-tag rule
# (forge/test/l06_per_tag.test.mjs, forge/test/post0056.test.mjs).
_G, _S = ["Highest"], ["Highest"]
_DMG = {"type": "damage", "power": 40, "calculation": "formula", "statTypes": _S, "generalTypes": _G}


def _jutsu(*effects):
    return {"items": [{"entity": "jutsu", "slot": "create", "name": "Probe", "srcId": "probe",
                       "data": {"name": "Probe", "hidden": True, "effects": list(effects)}}]}


def _ai(**drop):
    data = dict(_AI_REQ, username="Probe", hidden=True, level=100)
    for k in drop:
        data.pop(k)
    return {"items": [{"entity": "ai", "slot": "create", "name": "Probe", "srcId": "probe", "data": data}]}


STALE_RULE_FIXTURES = (
    ("wound with generalTypes, no statTypes",
     _jutsu(_DMG, {"type": "wound", "power": 20, "rounds": 2, "calculation": "percentage", "generalTypes": _G}),
     (), ("L06", "law 4")),
    ("wound with no calculation key, generalTypes only",
     _jutsu(_DMG, {"type": "wound", "power": 20, "rounds": 2, "generalTypes": _G}),
     (), ("L06", "law 4")),
    ("wound without generalTypes",
     _jutsu(_DMG, {"type": "wound", "power": 20, "rounds": 2, "calculation": "percentage"}),
     ("L06 wound missing generalTypes (",), ("L06 wound missing statTypes",)),
    ("damage without statTypes",
     _jutsu({"type": "damage", "power": 40, "calculation": "formula", "generalTypes": _G}),
     ("L06 damage missing statTypes (", "law 4: formula effect 'damage'"), ()),
    ("pierce without statTypes",
     _jutsu({"type": "pierce", "power": 40, "calculation": "formula", "generalTypes": _G}),
     ("L06 pierce missing statTypes (", "law 4: formula effect 'pierce'"), ()),
    ("pierce without generalTypes",
     _jutsu({"type": "pierce", "power": 40, "calculation": "formula", "statTypes": _S}),
     ("L06 pierce missing generalTypes (",), ()),
    ("AI create without preferredStat", _ai(), (), ("preferredStat", "law 14")),
    ("AI create without rank", _ai(rank=1), ("law 14: AI create missing required field 'rank'",), ()),
    ("AI create without preferredGeneral2", _ai(preferredGeneral2=1),
     ("law 14: AI create missing required field 'preferredGeneral2'",), ()),
)


def check_stale_rules(gdir, loaded, errors, notes):
    """validate.py --strict must agree with the pinned schemas on law 4 / L06 and law 14."""
    if not all(name in loaded for name in GENERATED):
        return
    import tempfile
    tags = loaded["45c_DATA_constructors.json"]["unions"]["AllTags"]
    if "statTypes" in tags["wound"]["fields"] or "statTypes" not in tags["damage"]["fields"]:
        errors.append("stale rules: 45c no longer matches the pinned WoundTag/DamageTag key sets; "
                      "re-read combat.ts before trusting these fixtures")
    for label, manifest, must, must_not in STALE_RULE_FIXTURES:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "probe.json"
            path.write_text(json.dumps(manifest))
            result = subprocess.run(
                [sys.executable, str(HERE / "validate.py"), "--strict", str(path)],
                cwd=gdir, capture_output=True, text=True,
            )
        out = result.stdout + result.stderr
        diags = "\n".join(l for l in out.splitlines() if l.startswith(("ERROR", "WARN")))
        for frag in must:
            if frag not in diags:
                errors.append(f"stale rules: {label}: expected {frag!r}, got {diags or 'no diagnostics'}")
        for frag in must_not:
            if frag in diags:
                errors.append(f"stale rules: {label}: unexpected {frag!r} in {diags}")
    notes.append(f"stale rules: {len(STALE_RULE_FIXTURES)} law 4/L06 and law 14 fixtures agree "
                 "with the pinned schemas")


def check_cross_module_refs(loaded, errors):
    constructors = loaded.get("45c_DATA_constructors.json")
    if constructors is None:
        return
    objectives = (constructors.get("unions") or {}).get("AllObjectives") or {}
    for variant in ("start_battle", "defeat_opponents", "RaidObjective"):
        fields = (objectives.get(variant) or {}).get("fields") or {}
        if fields and "opponentAIs" not in fields:
            errors.append(f"45c: {variant} lost opponentAIs")
    for name, variant in objectives.items():
        fields = variant.get("fields") or {}
        if "attackers_scaled_to_user" in fields and "attackers" not in fields:
            errors.append(f"45c: {name} lost attackers")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generated", default=".")
    args = parser.parse_args()

    gdir = Path(args.generated).resolve()
    errors, notes = [], []
    check_scripts(errors, notes)
    loaded = check_generated(gdir, errors, notes)
    check_factory(gdir, loaded, errors, notes)
    check_validator(gdir, loaded, errors, notes)
    check_runner_contract(gdir, loaded, errors, notes)
    check_stale_rules(gdir, loaded, errors, notes)
    check_cross_module_refs(loaded, errors)

    for error in errors:
        print("ERROR  " + error)
    for note in notes:
        print("note   " + note)
    print(f"\n{len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
