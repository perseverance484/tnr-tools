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
    check_cross_module_refs(loaded, errors)

    for error in errors:
        print("ERROR  " + error)
    for note in notes:
        print("note   " + note)
    print(f"\n{len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
