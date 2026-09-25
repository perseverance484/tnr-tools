#!/usr/bin/env python3
"""
Build the One Perfect Crop launch-final EDIT/CLOSEOUT manifest.

This generator never creates or runs live content. It edits the three already-created
hidden records from the committed hidden-core readback, applies only the director-approved
launch-final deltas, and binds the two accepted combat-avatar files to an immutable repo commit.

Usage from repository root:

    python3 push/54_one_perfect_crop_launch_final.gen.py --image-ref <40-hex-art-commit>
    python3 push/54_one_perfect_crop_launch_final.gen.py --image-ref <40-hex-art-commit> --check

The image ref is intentionally required. It must be an immutable commit that already contains
both processed avatar files. This avoids a self-referential manifest commit and makes Forge's
imagePack content binding independently reviewable.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "push", "47_one_perfect_crop_core_manifest.json")
PATCH = os.path.join(
    ROOT, "state", "workstreams", "one_perfect_crop", "launch_final_patch.json"
)
OUT = os.path.join(ROOT, "push", "54_one_perfect_crop_launch_final.json")

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

ROAD_AI = "dKEz_VsgZjrfbtxt4ldo8"
BOAR_AI = "2-gJmijAA8lGns_thDRjz"
QUEST_ID = "CZIZoHDAOWjxDtVaQwr6V"
MARKET_CLERK = "XsLLy8awDAtaE6hXVIi_0"

# The final authored quest edit must not carry any substitute eligibility gate.
# Optional delay fields are included here because the director explicitly requires them unset.
FORBIDDEN_QUEST_FIELDS = {
    "retryDelay",
    "attemptDelay",
    "requiredLevel",
    "maxLevel",
    "requiredVillage",
    "requiredBloodlineId",
    "requiredSageModeId",
    "requiredSageRank",
    "prerequisiteQuestId",
    "medicalRank",
    "huntingRank",
    "gatheringRank",
}

PROSE_NODES = {"opc_g1", "opc_g1_pass", "opc_f1_1", "opc_g4", "opc_g4_pass"}
CHOICE_TEXT_NODES = {"opc_g1", "opc_g4"}


def load_json(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def committed_bytes(ref: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", ROOT, "show", f"{ref}:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise SystemExit(
            f"{path}: not readable at image ref {ref}: "
            + proc.stderr.decode("utf-8", errors="replace").strip()
        )
    return proc.stdout


def require_commit(ref: str) -> None:
    if not COMMIT_RE.fullmatch(ref):
        raise SystemExit("--image-ref must be a 40-hex immutable commit SHA")
    proc = subprocess.run(
        ["git", "-C", ROOT, "cat-file", "-e", f"{ref}^{{commit}}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise SystemExit(f"--image-ref is not a local commit: {ref}")
    ancestor = subprocess.run(
        ["git", "-C", ROOT, "merge-base", "--is-ancestor", ref, "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if ancestor.returncode != 0:
        raise SystemExit(f"--image-ref {ref} is not an ancestor of HEAD")


def edge_targets(obj: dict[str, Any]) -> list[str]:
    out: list[str] = []
    nxt = obj.get("nextObjectiveId")
    if isinstance(nxt, str):
        out.append(nxt)
    elif isinstance(nxt, list):
        for choice in nxt:
            if isinstance(choice, dict) and isinstance(choice.get("nextObjectiveId"), str):
                out.append(choice["nextObjectiveId"])
    fail = obj.get("failObjectiveId")
    if isinstance(fail, str):
        out.append(fail)
    return out


def build_image_pack(patch: dict[str, Any], image_ref: str) -> tuple[dict[str, int], dict[str, Any]]:
    img_sizes: dict[str, int] = {}
    files: dict[str, Any] = {}
    for key in ("roadBandit", "harvestBoar"):
        spec = patch["avatars"][key]
        name, path = spec["name"], spec["path"]
        if os.path.basename(path) != name:
            raise AssertionError(f"{key}: path basename must equal logical @img name")
        raw = committed_bytes(image_ref, path)
        if not raw:
            raise AssertionError(f"{key}: committed avatar is empty")
        size = len(raw)
        digest = hashlib.sha256(raw).hexdigest()
        img_sizes[name] = size
        files[name] = {"path": path, "sha256": digest, "bytes": size}

        # When the file is present in the checkout, require exact byte identity with the
        # immutable image-ref copy. This catches a dirty/uncommitted art substitution.
        working = os.path.join(ROOT, path)
        if os.path.exists(working):
            with open(working, "rb") as fh:
                now = fh.read()
            if now != raw:
                raise AssertionError(
                    f"{path}: working bytes differ from immutable image ref {image_ref}"
                )

    return img_sizes, {"ref": image_ref, "files": dict(sorted(files.items()))}


def apply_patch(core: dict[str, Any], patch: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    quest_items = [
        item for item in core.get("items", [])
        if item.get("entity") == "quest" and item.get("srcId") == "opc_quest"
    ]
    if len(quest_items) != 1:
        raise AssertionError("hidden-core baseline must contain exactly one opc_quest create")
    baseline = copy.deepcopy(quest_items[0]["data"])
    content = copy.deepcopy(baseline["content"])
    objectives = content["objectives"]

    by_id = {o["id"]: o for o in objectives}
    if len(by_id) != len(objectives):
        raise AssertionError("hidden-core baseline has duplicate objective ids")

    for oid, delta in patch["prose"].items():
        if oid not in by_id:
            raise AssertionError(f"prose patch references missing objective {oid}")
        obj = by_id[oid]
        obj["description"] = delta["description"]
        if "choices" in delta:
            # Choice labels may change; the destination ids are frozen.
            before_edges = edge_targets(obj)
            obj["nextObjectiveId"] = copy.deepcopy(delta["choices"])
            if edge_targets(obj) != before_edges:
                raise AssertionError(f"{oid}: prose patch changed routing")

    background_for: dict[str, str] = {}
    for background_id, objective_ids in patch["sceneWiring"]["backgrounds"].items():
        for oid in objective_ids:
            if oid in background_for:
                raise AssertionError(f"{oid}: duplicate scene-background mapping")
            background_for[oid] = background_id

    dialogs = [o for o in objectives if o.get("task") == "dialog"]
    dialog_ids = {o["id"] for o in dialogs}
    if set(background_for) != dialog_ids:
        missing = sorted(dialog_ids - set(background_for))
        extra = sorted(set(background_for) - dialog_ids)
        raise AssertionError(f"scene-background map mismatch; missing={missing}, extra={extra}")

    default_characters = patch["sceneWiring"]["sceneCharactersDefault"]
    per_objective = patch["sceneWiring"]["sceneCharactersByObjective"]
    for obj in dialogs:
        oid = obj["id"]
        obj["sceneBackground"] = background_for[oid]
        obj["sceneCharacters"] = copy.deepcopy(per_objective.get(oid, default_characters))

    # No mechanical reward package is introduced. Keep the hidden core's explicit empty reward.
    content["reward"] = {}

    admin = patch["questAdmin"]
    quest_data = {
        # These are deliberately the only quest-level assertions besides content.
        # Forge merges the remaining validator fields from live before quests.update.
        "name": baseline["name"],
        "hidden": True,
        "maxAttempts": admin["maxAttempts"],
        "maxCompletes": admin["maxCompletes"],
        "content": content,
    }
    return baseline, quest_data


def verify_structural_diff(
    baseline: dict[str, Any],
    quest_data: dict[str, Any],
    patch: dict[str, Any],
) -> None:
    assert quest_data["name"] == "One Perfect Crop"
    assert quest_data["hidden"] is True
    assert quest_data["maxAttempts"] == 100
    assert quest_data["maxCompletes"] == 1
    assert FORBIDDEN_QUEST_FIELDS.isdisjoint(quest_data)
    assert quest_data["content"]["reward"] == {}
    assert quest_data["content"].get("sceneBackground", "") == baseline["content"].get(
        "sceneBackground", ""
    )
    assert quest_data["content"].get("sceneCharacters", []) == baseline["content"].get(
        "sceneCharacters", []
    )

    before = baseline["content"]["objectives"]
    after = quest_data["content"]["objectives"]
    assert [o["id"] for o in after] == [o["id"] for o in before]
    before_by = {o["id"]: o for o in before}
    after_by = {o["id"]: o for o in after}

    # Graph structure is frozen. Labels may change only on G1/G4; destinations never do.
    for oid in before_by:
        assert before_by[oid]["task"] == after_by[oid]["task"], oid
        assert edge_targets(before_by[oid]) == edge_targets(after_by[oid]), oid

    # Only the approved prose keys plus dialog scene wiring may move.
    for oid, old in before_by.items():
        new = after_by[oid]
        changed = {k for k in set(old) | set(new) if old.get(k) != new.get(k)}
        allowed = {"sceneBackground", "sceneCharacters"} if old.get("task") == "dialog" else set()
        if oid in PROSE_NODES:
            allowed.add("description")
        if oid in CHOICE_TEXT_NODES:
            allowed.add("nextObjectiveId")
        extra = changed - allowed
        if extra:
            raise AssertionError(f"{oid}: unrelated launch-final drift in {sorted(extra)}")

    # Approved prose input must match byte-for-byte.
    for oid, delta in patch["prose"].items():
        assert after_by[oid]["description"] == delta["description"], oid
        if "choices" in delta:
            assert after_by[oid]["nextObjectiveId"] == delta["choices"], oid

    # The only non-empty scene-character reuse is the already-captured Market Clerk.
    for obj in after:
        if obj.get("task") != "dialog":
            continue
        chars = obj.get("sceneCharacters")
        assert isinstance(chars, list), obj["id"]
        if chars:
            assert chars == [MARKET_CLERK], obj["id"]
            assert obj["id"] in {"opc_d1", "opc_d2", "opc_d3", "opc_d4", "opc_d5"}

    # Battle contracts and sealed loss routes remain exactly as the hidden core authored them.
    for oid in ("opc_f2_battle", "opc_c1_battle"):
        assert stable_json(before_by[oid]) == stable_json(after_by[oid]), oid
        assert after_by[oid]["opponent_scaled_to_user"] is True
        assert after_by[after_by[oid]["failObjectiveId"]]["task"] == "fail_quest"

    assert sum(o.get("task") == "win_quest" for o in after) == 1
    assert sum(o.get("task") == "fail_quest" for o in after) == 6


def build_manifest(image_ref: str) -> dict[str, Any]:
    require_commit(image_ref)
    core = load_json(BASE)
    patch = load_json(PATCH)

    targets = patch["liveTargets"]
    assert targets == {
        "roadBanditAi": ROAD_AI,
        "harvestBoarAi": BOAR_AI,
        "quest": QUEST_ID,
    }

    baseline, quest_data = apply_patch(core, patch)
    verify_structural_diff(baseline, quest_data, patch)

    img_sizes, image_pack = build_image_pack(patch, image_ref)
    road_name = patch["avatars"]["roadBandit"]["name"]
    boar_name = patch["avatars"]["harvestBoar"]["name"]

    manifest = {
        "_note": (
            "One Perfect Crop launch-final EDIT/CLOSEOUT against the three existing hidden "
            "records. No creates, no publish/unhide, no replacement quest."
        ),
        "imgSizes": img_sizes,
        "imagePack": image_pack,
        "items": [
            {
                "name": "One Perfect Crop — Road Bandit avatar",
                "entity": "ai",
                "slot": "edit",
                "targetId": ROAD_AI,
                "data": {"avatar": "@img:" + road_name},
            },
            {
                "name": "One Perfect Crop — Harvest Boar avatar",
                "entity": "ai",
                "slot": "edit",
                "targetId": BOAR_AI,
                "data": {"avatar": "@img:" + boar_name},
            },
            {
                "name": "One Perfect Crop — launch-final quest closeout",
                "entity": "quest",
                "slot": "edit",
                "targetId": QUEST_ID,
                "data": quest_data,
            },
        ],
        "capture": {"after": copy.deepcopy(patch["afterCapture"])},
    }
    verify_manifest(manifest, patch)
    return manifest


def verify_manifest(manifest: dict[str, Any], patch: dict[str, Any]) -> None:
    items = manifest["items"]
    assert [(i["entity"], i["slot"]) for i in items] == [
        ("ai", "edit"),
        ("ai", "edit"),
        ("quest", "edit"),
    ]
    assert [i["targetId"] for i in items] == [ROAD_AI, BOAR_AI, QUEST_ID]
    assert all("srcId" not in i for i in items)
    assert all(i["slot"] != "create" for i in items)

    assert items[0]["data"] == {
        "avatar": "@img:" + patch["avatars"]["roadBandit"]["name"]
    }
    assert items[1]["data"] == {
        "avatar": "@img:" + patch["avatars"]["harvestBoar"]["name"]
    }

    q = items[2]["data"]
    assert q["hidden"] is True
    assert q["maxAttempts"] == 100 and q["maxCompletes"] == 1
    assert FORBIDDEN_QUEST_FIELDS.isdisjoint(q)
    assert q["content"]["reward"] == {}

    blob = stable_json(manifest)
    assert "Cabbage Seed" not in blob
    assert '"entity":"item"' not in blob
    assert '"slot":"create"' not in blob
    assert "one_perfect_crop_road_bandit_scene" not in blob
    assert "@scene:" not in blob
    assert "skipPreflight" not in manifest

    names = {
        patch["avatars"]["roadBandit"]["name"],
        patch["avatars"]["harvestBoar"]["name"],
    }
    assert set(manifest["imgSizes"]) == names
    assert set(manifest["imagePack"]["files"]) == names
    for name in names:
        entry = manifest["imagePack"]["files"][name]
        assert entry["bytes"] == manifest["imgSizes"][name]
        assert re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])

    captures = manifest["capture"]["after"]
    assert captures == patch["afterCapture"]
    assert all(c.get("persist") == "full" for c in captures)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image-ref", required=True, help="immutable 40-hex commit containing both avatars")
    ap.add_argument(
        "--check",
        action="store_true",
        help="do not write; fail unless the committed/generated JSON is already exact",
    )
    args = ap.parse_args()

    manifest = build_manifest(args.image_ref)
    rendered = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not os.path.exists(OUT):
            print(f"MISSING: {OUT}", file=sys.stderr)
            return 1
        with open(OUT, encoding="utf-8") as fh:
            current = fh.read()
        if current != rendered:
            print(f"STALE: {OUT}", file=sys.stderr)
            return 1
        print(f"OK: {OUT} is generator-exact")
        return 0

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(rendered)
    print(
        f"{OUT}: {len(manifest['items'])} edit items, "
        f"{len(manifest['imgSizes'])} immutable avatar bindings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
