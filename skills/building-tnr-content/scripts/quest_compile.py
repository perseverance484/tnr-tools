#!/usr/bin/env python3
"""Canonical repository-side compiler entry point for Forge Quest Studio.

The browser authors a versioned Quest Source. This script validates that source,
selects the repository-owned subtype adapter, delegates to existing deterministic
content tools, runs canonical manifest validation, and emits one machine-readable
build result. It never contacts the live game.

Initial production adapter: mission -> mission.py + 48_DATA_mission_profiles.json.
Other subtypes are declared in 49_DATA_quest_studio_subtypes.json but refuse until
an executable adapter exists.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

SCHEMA_VERSION = 1
RESULT_VERSION = 1
REQUEST_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,63}$")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CONTENT_ROOT = REPO / "skills" / "building-tnr-content"
CONTENT_DATA = CONTENT_ROOT / "data"
CONTENT_SCRIPTS = CONTENT_ROOT / "scripts"
ART_ROOT = REPO / "skills" / "producing-tnr-art"
ART_DATA = ART_ROOT / "data"
ART_SCRIPTS = ART_ROOT / "scripts"
REGISTRY_PATH = CONTENT_DATA / "49_DATA_quest_studio_subtypes.json"
PROFILES_PATH = CONTENT_DATA / "48_DATA_mission_profiles.json"
ART_SPEC_PATH = ART_DATA / "25x_DATA_art_spec.json"
VALIDATE_PATH = CONTENT_SCRIPTS / "validate.py"


class QuestSourceError(ValueError):
    pass


class QuestBlocked(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def stable_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def source_hash(source: dict) -> str:
    return hashlib.sha256(stable_bytes(source)).hexdigest()


def validate_source(raw: Any, expected_request_id: str | None = None) -> dict:
    if not isinstance(raw, dict):
        raise QuestSourceError("Quest Source must be a JSON object")
    if raw.get("schemaVersion") != SCHEMA_VERSION:
        raise QuestSourceError(
            f"unsupported Quest Source schemaVersion {raw.get('schemaVersion')!r}; expected {SCHEMA_VERSION}"
        )
    if raw.get("kind") != "quest":
        raise QuestSourceError("Quest Source kind must be 'quest'")
    request_id = raw.get("requestId")
    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id):
        raise QuestSourceError(
            "requestId must match ^[a-z0-9][a-z0-9._-]{2,63}$"
        )
    if expected_request_id is not None and request_id != expected_request_id:
        raise QuestSourceError(
            f"Quest Source requestId {request_id!r} does not match worker request id {expected_request_id!r}"
        )
    subtype = raw.get("subtype")
    if not isinstance(subtype, str) or not subtype:
        raise QuestSourceError("subtype is required")
    content = raw.get("content")
    if not isinstance(content, dict):
        raise QuestSourceError("content must be an object")
    if "project" in raw and raw["project"] is not None and not isinstance(raw["project"], dict):
        raise QuestSourceError("project must be an object when present")
    if "meta" in raw and raw["meta"] is not None and not isinstance(raw["meta"], dict):
        raise QuestSourceError("meta must be an object when present")
    return raw


def registry_entry(registry: dict, subtype: str) -> dict:
    entry = (registry.get("subtypes") or {}).get(subtype)
    if not isinstance(entry, dict):
        raise QuestSourceError(f"unknown Quest Studio subtype {subtype!r}")
    return entry


def classify_mission_error(message: str) -> QuestBlocked | None:
    """Only known human-decision refusals become `blocked`.

    Everything else remains a failed build. This is intentionally conservative:
    a compiler defect or malformed source must never masquerade as a director decision.
    """
    markers = (
        "rulings, not defaults",
        "balance call",
        "Give the roster entry an explicit `level`",
    )
    if any(marker in message for marker in markers):
        return QuestBlocked("decision_required", message)
    return None


def ensure_import_paths() -> None:
    for path in (CONTENT_SCRIPTS, ART_SCRIPTS):
        s = str(path)
        if s not in sys.path:
            sys.path.insert(0, s)


def run_manifest_validation(manifest_path: Path) -> tuple[bool, str]:
    cmd = [sys.executable, str(VALIDATE_PATH), str(manifest_path)]
    proc = subprocess.run(
        cmd,
        cwd=str(CONTENT_DATA),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode == 0, proc.stdout


def entity_summary(manifest: dict) -> dict:
    counts: dict[str, int] = {}
    creates = 0
    updates = 0
    for item in manifest.get("items") or []:
        ent = str(item.get("entity") or "unknown")
        counts[ent] = counts.get(ent, 0) + 1
        if item.get("slot") == "create":
            creates += 1
        else:
            updates += 1
    return {"counts": counts, "creates": creates, "updates": updates}


def enforce_mission_profile_shape(source: dict, profiles: dict, manifest: dict) -> None:
    rank = source.get("content", {}).get("rank")
    profile = (profiles.get("ranks") or {}).get(rank)
    if not isinstance(profile, dict):
        raise QuestSourceError(f"unknown Mission profile {rank!r}")
    shape = profile.get("shape") or {}
    expected_objectives = shape.get("objective_count")
    expected_battles = shape.get("battle_nodes")
    # mission.py owns unresolved-ruling refusal. Only ratified numeric shape values are enforced here.
    if type(expected_objectives) is not int or type(expected_battles) is not int:
        return

    quest_item = next((item for item in manifest.get("items") or [] if item.get("entity") == "quest"), None)
    data = quest_item.get("data") if isinstance(quest_item, dict) else None
    content = data.get("content") if isinstance(data, dict) else None
    objectives = content.get("objectives") if isinstance(content, dict) else None
    if not isinstance(objectives, list):
        raise QuestSourceError("mission adapter produced no quest objective list")

    battle_tasks = {"start_battle", "defeat_opponents"}
    actual_objectives = len(objectives)
    actual_battles = sum(1 for objective in objectives if objective.get("task") in battle_tasks)
    mismatches = []
    if actual_objectives != expected_objectives:
        mismatches.append(f"{actual_objectives} objectives; profile requires {expected_objectives}")
    if actual_battles != expected_battles:
        mismatches.append(f"{actual_battles} battle nodes; profile requires {expected_battles}")
    if mismatches:
        raise QuestBlocked(
            "profile_shape_unmet",
            f"Mission profile shape is not met for {rank}: " + "; ".join(mismatches),
        )


def compile_mission(source: dict, artifact_dir: Path, artifact_prefix: str) -> dict:
    ensure_import_paths()
    import mission  # type: ignore

    profiles = load_json(PROFILES_PATH)
    art_spec = load_json(ART_SPEC_PATH) if ART_SPEC_PATH.exists() else None
    old_cwd = Path.cwd()
    try:
        os.chdir(CONTENT_DATA)
        built = mission.build(source["content"], profiles, art_spec)
    except mission.MissionError as exc:  # type: ignore[attr-defined]
        blocked = classify_mission_error(str(exc))
        if blocked:
            raise blocked
        raise QuestSourceError(str(exc)) from exc
    finally:
        os.chdir(old_cwd)

    manifest = built.get("manifest")
    if not isinstance(manifest, dict):
        raise QuestSourceError("mission adapter returned no manifest")
    enforce_mission_profile_shape(source, profiles, manifest)

    artifact_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = artifact_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    valid, validation_output = run_manifest_validation(manifest_path)
    if not valid:
        raise QuestSourceError("canonical manifest validation failed:\n" + validation_output)

    warnings: list[dict[str, str]] = []
    art = built.get("art")
    if isinstance(art, dict) and art.get("error"):
        warnings.append({"code": "art_requirements_unavailable", "message": str(art["error"])})

    return {
        "resolvedEngineType": "mission",
        "generated": {
            "manifestPath": f"{artifact_prefix}/manifest.json",
            "entities": entity_summary(manifest),
            "enemies": built.get("enemies") or [],
        },
        "art": art if isinstance(art, dict) else None,
        "validation": {"ok": True, "output": validation_output},
        "warnings": warnings,
    }


def make_result(source: dict, *, status: str, source_revision: str | None,
                compiler_revision: str | None, registry: dict,
                resolved_engine_type: str | None = None,
                blockers: list[dict] | None = None,
                errors: list[dict] | None = None,
                warnings: list[dict] | None = None,
                generated: dict | None = None,
                art: dict | None = None,
                validation: dict | None = None) -> dict:
    return {
        "schemaVersion": RESULT_VERSION,
        "kind": "quest-build",
        "requestId": source.get("requestId"),
        "subtype": source.get("subtype"),
        "status": status,
        "resolvedEngineType": resolved_engine_type,
        "blockers": blockers or [],
        "errors": errors or [],
        "warnings": warnings or [],
        "generated": generated or {},
        "art": art,
        "validation": validation,
        "provenance": {
            "sourceSha256": source_hash(source),
            "sourceRevision": source_revision,
            "compilerRevision": compiler_revision,
            "registrySchemaVersion": (registry.get("_meta") or {}).get("schemaVersion"),
            "compiler": "skills/building-tnr-content/scripts/quest_compile.py",
        },
        "liveGameTouched": False,
    }


def compile_source(source: dict, *, artifact_dir: Path, artifact_prefix: str,
                   source_revision: str | None = None,
                   compiler_revision: str | None = None,
                   registry: dict | None = None) -> dict:
    source = validate_source(source)
    registry = registry or load_json(REGISTRY_PATH)
    entry = registry_entry(registry, source["subtype"])
    adapter = entry.get("compilerAdapter")
    if entry.get("maturity") != "supported" or not adapter:
        return make_result(
            source,
            status="blocked",
            source_revision=source_revision,
            compiler_revision=compiler_revision,
            registry=registry,
            blockers=[{
                "code": "subtype_not_executable",
                "message": (
                    f"{entry.get('label', source['subtype'])} is registered but does not yet have "
                    "an executable repository compiler adapter."
                ),
            }],
        )

    try:
        if adapter == "mission":
            detail = compile_mission(source, artifact_dir, artifact_prefix)
        else:
            raise QuestSourceError(f"unsupported compiler adapter {adapter!r}")
    except QuestBlocked as exc:
        return make_result(
            source,
            status="blocked",
            source_revision=source_revision,
            compiler_revision=compiler_revision,
            registry=registry,
            blockers=[{"code": exc.code, "message": exc.message}],
        )
    except Exception as exc:
        return make_result(
            source,
            status="failed",
            source_revision=source_revision,
            compiler_revision=compiler_revision,
            registry=registry,
            errors=[{"code": "compile_failed", "message": str(exc)}],
        )

    return make_result(
        source,
        status="valid",
        source_revision=source_revision,
        compiler_revision=compiler_revision,
        registry=registry,
        resolved_engine_type=detail.get("resolvedEngineType"),
        warnings=detail.get("warnings"),
        generated=detail.get("generated"),
        art=detail.get("art"),
        validation=detail.get("validation"),
    )


def selftest() -> int:
    failures: list[str] = []
    checks = 0

    def want(cond: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        print(("PASS  " if cond else "FAIL  ") + label)
        if not cond:
            failures.append(label)

    base = {
        "schemaVersion": 1,
        "kind": "quest",
        "requestId": "selftest-mission",
        "subtype": "mission",
        "content": {},
    }
    want(validate_source(dict(base))["requestId"] == "selftest-mission", "valid source accepted")
    try:
        validate_source({**base, "requestId": "../bad"})
        want(False, "unsafe request id rejected")
    except QuestSourceError:
        want(True, "unsafe request id rejected")

    registry = load_json(REGISTRY_PATH)
    want(registry_entry(registry, "mission").get("compilerAdapter") == "mission",
         "mission adapter is repository-declared")
    want(registry_entry(registry, "battle_pyramid").get("maturity") != "supported",
         "unsupported subtype is not advertised executable")

    h1 = source_hash(base)
    h2 = source_hash(json.loads(json.dumps(base)))
    want(h1 == h2 and len(h1) == 64, "source hash is stable sha256")

    blocked = compile_source(
        {**base, "subtype": "battle_pyramid"},
        artifact_dir=Path("/tmp/tnr-quest-studio-selftest"),
        artifact_prefix="studio/builds/selftest-mission",
        registry=registry,
    )
    want(blocked["status"] == "blocked" and blocked["blockers"],
         "registered subtype without adapter returns structured blocker")
    want(blocked["liveGameTouched"] is False, "result states live game untouched")

    b = classify_mission_error("profile incomplete; these are rulings, not defaults")
    want(isinstance(b, QuestBlocked), "mission unresolved ruling classifies as blocker")
    want(classify_mission_error("invalid objective graph") is None,
         "ordinary compiler error is not mislabeled a director decision")

    print(f"\n{checks - len(failures)} passed, {len(failures)} failed")
    return 1 if failures else 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", nargs="?", help="Quest Source JSON")
    ap.add_argument("--result", help="build-result JSON path")
    ap.add_argument("--artifact-dir", help="directory for generated artifacts")
    ap.add_argument("--artifact-prefix", help="repository-relative artifact path recorded in result")
    ap.add_argument("--source-revision")
    ap.add_argument("--compiler-revision")
    ap.add_argument("--request-id", help="validated worker request identity; binds failure envelopes to the request")
    ap.add_argument("--selftest", action="store_true")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.selftest:
        return selftest()
    if not args.source or not args.result or not args.artifact_dir or not args.artifact_prefix:
        raise SystemExit("source, --result, --artifact-dir and --artifact-prefix are required")

    result_path = Path(args.result).resolve()
    artifact_dir = Path(args.artifact_dir).resolve()
    expected_request_id = args.request_id
    if expected_request_id is not None and not REQUEST_ID_RE.fullmatch(expected_request_id):
        raise SystemExit("--request-id must match ^[a-z0-9][a-z0-9._-]{2,63}$")
    raw_source: Any = None
    try:
        raw_source = load_json(Path(args.source).resolve())
        source = validate_source(raw_source, expected_request_id=expected_request_id)
        result = compile_source(
            source,
            artifact_dir=artifact_dir,
            artifact_prefix=args.artifact_prefix.strip("/"),
            source_revision=args.source_revision,
            compiler_revision=args.compiler_revision,
        )
    except Exception as exc:
        # The worker-supplied identity survives malformed authored source so Forge can always read
        # a request-scoped failed envelope instead of wedging the draft on requestId:null.
        fallback_request_id = expected_request_id
        if fallback_request_id is None and isinstance(raw_source, dict):
            candidate = raw_source.get("requestId")
            if isinstance(candidate, str) and REQUEST_ID_RE.fullmatch(candidate):
                fallback_request_id = candidate
        subtype = raw_source.get("subtype") if isinstance(raw_source, dict) and isinstance(raw_source.get("subtype"), str) else None
        result = {
            "schemaVersion": RESULT_VERSION,
            "kind": "quest-build",
            "requestId": fallback_request_id,
            "subtype": subtype,
            "status": "failed",
            "resolvedEngineType": None,
            "blockers": [],
            "errors": [{"code": "source_invalid", "message": str(exc)}],
            "warnings": [],
            "generated": {},
            "art": None,
            "validation": None,
            "provenance": {
                "sourceSha256": None,
                "sourceRevision": args.source_revision,
                "compilerRevision": args.compiler_revision,
                "registrySchemaVersion": None,
                "compiler": "skills/building-tnr-content/scripts/quest_compile.py",
            },
            "liveGameTouched": False,
        }

    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result.get("status"),
        "requestId": result.get("requestId"),
        "result": str(result_path),
    }))
    return 1 if result.get("status") == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
