#!/usr/bin/env python3
"""
Build push/48_godstorm_current_manifest.json from the saved Godstorm captures.

Current safe executable scope only:
- create the three director-approved Stormcourt SCENE_BACKGROUND assets;
- edit all 18 retained AI profiles to bound their final highest-damage fallback
  to the engine-native adjacent-distance guard (<= 2).

The two quest records are deliberately NOT emitted yet. Their graph delta is
approved, but exact copy, rewards/cadence/chest and scene-character assets are
not frozen. Emitting a quest mutation now would either preserve rejected
Tower/cash-out prose or invent user-owned decisions.

This generator fails closed on target/range mismatches, missing/unequipped
jutsu references, changed retained-AI census, or any profile that does not have
exactly one unbounded authored highest-damage fallback.

Run from repository root:
    python3 push/48_godstorm_current_manifest.gen.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_CAPTURE = ROOT / "harvests/inbox/tnr_results_1789401726302.json"
AI_CAPTURE = ROOT / "harvests/inbox/tnr_results_1789402842027.json"
PROFILE_CAPTURE = ROOT / "harvests/inbox/tnr_results_1789403623148.json"
OUT = ROOT / "push/48_godstorm_current_manifest.json"

QUEST_IDS = (
    "2yvE9PUQqlD8lbYNfgX-b",
    "OSADdXqostbyVliCxWk6k",
)
OPPONENT_RULE_TARGETS = {"RANDOM_OPPONENT", "CLOSEST_OPPONENT"}

ART = (
    {
        "label": "Godstorm Stormcourt Upper Court",
        "src": "godstorm_sc_upper",
        "record_name": "GodstormStormcourtUpperCourt",
        "file": "bg_godstorm_stormcourt_upper_court.webp",
        "bytes": 379928,
        "sha256": "c0587d9fdeb8c4c75ecc6f5eaf0c08a0b783461299793c774f66f7aaab4f12b9",
    },
    {
        "label": "Godstorm Stormcourt Binding Dais Active",
        "src": "godstorm_sc_dais_active",
        "record_name": "GodstormStormcourtBindingDaisActive",
        "file": "bg_godstorm_stormcourt_binding_dais_active.webp",
        "bytes": 283000,
        "sha256": "41ca12f9d21604151f754ded0df2211bed5b671dcc2dd7c954e53c5f17f36d70",
    },
    {
        "label": "Godstorm Stormcourt Binding Dais Released",
        "src": "godstorm_sc_dais_released",
        "record_name": "GodstormStormcourtBindingDaisReleased",
        "file": "bg_godstorm_stormcourt_binding_dais_released.webp",
        "bytes": 256826,
        "sha256": "97fc11d4ad1c24beeaffaf2e7f8a589715806dce6d17290d0fa253694fd3ef18",
    },
)


AVATARS = (
    {
        "label": "Umbral Reaver avatar",
        "ai_id": "9uDe65Qt90xnT-fM5vJZ7",
        "file": "ai_godstorm_marrow_umbral_reaver.webp",
        "bytes": 161650,
        "sha256": "30693d5dc252f8ce61638a0b4c191523ef7df8461b8252ff309e21192154bfcc",
    },
    {
        "label": "Hollow Lantern avatar",
        "ai_id": "IG5Mbfi_2lpUTnUU4_XhZ",
        "file": "ai_godstorm_marrow_hollow_lantern.webp",
        "bytes": 196056,
        "sha256": "50d1786fb6f5c2a2350b04dd27ec1ff8b0e1d58237e98337c0a2065e226b6055",
    },
    {
        "label": "Starless Monk avatar",
        "ai_id": "qQ6jMh8w6aiyr4pevwDh-",
        "file": "ai_godstorm_marrow_starless_monk.webp",
        "bytes": 207410,
        "sha256": "877eef3b0cecc914d4e3300e21cb50c87030093c5730d4feb54b71a7e7cdc870",
    },
    {
        "label": "Nightveil Sentinel avatar",
        "ai_id": "YvinZCoMWiz0RY8ZBP5EW",
        "file": "ai_godstorm_marrow_nightveil_sentinel.webp",
        "bytes": 115618,
        "sha256": "d5c5a8c8a2be20700a7df16b9ac38e4b9cd6a7a2917efa5d7d815d19deebd9e2",
    },
)


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def full_success(doc: dict, path: Path) -> None:
    if doc.get("state") != "DONE" or doc.get("outcome") != "success":
        raise SystemExit(f"{path}: capture is not DONE/success")
    if doc.get("entries") not in ([], None):
        raise SystemExit(f"{path}: mutation entries are not empty")


def capture_map(doc: dict, proc: str, response_key: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for c in doc.get("captures", []):
        if c.get("proc") != proc or not isinstance(c.get("data"), dict):
            continue
        data = c["data"]
        key = data.get(response_key)
        if not isinstance(key, str) or not key:
            continue
        if key in out:
            raise SystemExit(f"{proc}: duplicate captured response key {key}")
        out[key] = data
    return out


def retained_ai_ids(root: dict) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    roots = {
        c["data"]["id"]: c["data"]
        for c in root.get("captures", [])
        if c.get("proc") == "quests.get"
        and isinstance(c.get("data"), dict)
        and c["data"].get("id") in QUEST_IDS
    }
    if set(roots) != set(QUEST_IDS):
        raise SystemExit("retained quest roots did not resolve exactly")
    for qid in QUEST_IDS:
        q = roots[qid]
        battles = [o for o in q["content"]["objectives"] if o.get("task") == "start_battle"]
        if len(battles) != 25:
            raise SystemExit(f"{qid}: expected 25 battles, got {len(battles)}")
        for battle in battles:
            for group in battle.get("opponentAIs", []):
                for ai_id in group.get("ids", []):
                    if ai_id not in seen:
                        seen.add(ai_id)
                        result.append(ai_id)
    if len(result) != 18:
        raise SystemExit(f"retained AI census changed: expected 18, got {len(result)}")
    return result


def equipped_jutsu(ai: dict) -> dict[str, dict]:
    out = {}
    for row in ai.get("jutsus", []):
        j = row.get("jutsu") if isinstance(row, dict) else None
        if not row.get("equipped") or not isinstance(j, dict):
            continue
        jid = j.get("id")
        if isinstance(jid, str) and jid:
            out[jid] = j
    return out


def range_guards(rule: dict, target: str) -> list[int]:
    vals = []
    for c in rule.get("conditions", []):
        if c.get("type") == "distance_lower_than" and c.get("target") == target:
            value = c.get("value")
            if isinstance(value, (int, float)):
                vals.append(int(value))
    return vals


def audit_and_patch(ai: dict, profile: dict) -> list[dict]:
    jmap = equipped_jutsu(ai)
    rules = json.loads(json.dumps(profile.get("rules", [])))
    if not isinstance(rules, list) or not rules:
        raise SystemExit(f"{ai.get('username')}: no captured authored profile rules")

    fallback_count = 0
    for i, rule in enumerate(rules):
        action = rule.get("action", {})
        atype = action.get("type")
        refs: list[str] = []
        if atype == "use_specific_jutsu":
            refs = [action.get("jutsuId")]
        elif atype == "use_combo_action":
            refs = list(action.get("comboIds", []))

        resolved = []
        for jid in refs:
            if not isinstance(jid, str) or jid not in jmap:
                raise SystemExit(
                    f"{ai.get('username')} rule {i}: missing or unequipped jutsu {jid!r}"
                )
            j = jmap[jid]
            resolved.append(j)
            if j.get("target") == "SELF" and action.get("target") != "SELF":
                raise SystemExit(
                    f"{ai.get('username')} rule {i}: SELF jutsu {j.get('name')} "
                    f"uses profile target {action.get('target')}"
                )
            if (
                j.get("target") == "OTHER_USER"
                and action.get("target") not in OPPONENT_RULE_TARGETS
            ):
                raise SystemExit(
                    f"{ai.get('username')} rule {i}: opponent jutsu {j.get('name')} "
                    f"uses profile target {action.get('target')}"
                )

        offensive = [j for j in resolved if j.get("target") == "OTHER_USER"]
        if offensive:
            minimum_range = min(int(j.get("range", -1)) for j in offensive)
            guards = range_guards(rule, action.get("target"))
            if not guards:
                raise SystemExit(
                    f"{ai.get('username')} rule {i}: offensive specific/combo rule "
                    "has no upper distance guard"
                )
            if min(guards) > minimum_range:
                raise SystemExit(
                    f"{ai.get('username')} rule {i}: guard {min(guards)} exceeds "
                    f"minimum referenced jutsu range {minimum_range}"
                )

        if (
            atype == "use_highest_power_action"
            and action.get("effect") == "damage"
            and not rule.get("conditions")
        ):
            fallback_count += 1
            rule["conditions"] = [
                {
                    "type": "distance_lower_than",
                    "description": "Distance lower than or equal given value",
                    "value": 2,
                    "target": "RANDOM_OPPONENT",
                }
            ]

    if fallback_count != 1:
        raise SystemExit(
            f"{ai.get('username')}: expected exactly one unbounded highest-damage "
            f"fallback, got {fallback_count}"
        )

    # Post-patch invariant: every authored highest-damage fallback is bounded <= 2.
    for i, rule in enumerate(rules):
        action = rule.get("action", {})
        if (
            action.get("type") == "use_highest_power_action"
            and action.get("effect") == "damage"
        ):
            guards = range_guards(rule, action.get("target"))
            if not guards or min(guards) > 2:
                raise SystemExit(
                    f"{ai.get('username')} rule {i}: highest-damage fallback remains unsafe"
                )
    return rules


def main() -> None:
    root = load(ROOT_CAPTURE)
    ais = load(AI_CAPTURE)
    profiles = load(PROFILE_CAPTURE)
    for doc, path in (
        (root, ROOT_CAPTURE),
        (ais, AI_CAPTURE),
        (profiles, PROFILE_CAPTURE),
    ):
        full_success(doc, path)

    ids = retained_ai_ids(root)
    ai_by_id = capture_map(ais, "profile.getAi", "userId")
    profile_by_id = capture_map(profiles, "ai.getAiProfile", "userId")

    items = []
    img_sizes = {}
    for art in ART:
        img_sizes[art["file"]] = art["bytes"]
        items.append(
            {
                "name": art["label"],
                "entity": "asset",
                "slot": "create",
                "srcId": art["src"],
                "data": {
                    "name": art["record_name"],
                    "type": "SCENE_BACKGROUND",
                    "image": f"@img:{art['file']}",
                    "folder": "Godstorm",
                    "frames": 1,
                    "speed": 1,
                    "hidden": True,
                    "onInitialBattleField": False,
                    "licenseDetails": "TNR",
                },
            }
        )

    for avatar in AVATARS:
        if avatar["ai_id"] not in ids:
            raise SystemExit(f"{avatar['label']}: AI is no longer retained")
        img_sizes[avatar["file"]] = avatar["bytes"]
        items.append(
            {
                "name": avatar["label"],
                "entity": "ai",
                "slot": "edit",
                "targetId": avatar["ai_id"],
                "data": {"avatar": f"@img:{avatar['file']}"},
            }
        )

    for ai_id in ids:
        ai = ai_by_id.get(ai_id)
        profile = profile_by_id.get(ai_id)
        if ai is None or profile is None:
            raise SystemExit(f"{ai_id}: missing AI/profile capture")
        rules = audit_and_patch(ai, profile)
        items.append(
            {
                "name": f"{ai['username']} AI profile safety",
                "entity": "aiProfile",
                "slot": "edit",
                "targetId": ai_id,
                "data": {
                    "rules": rules,
                    "includeDefaultRules": profile.get("includeDefaultRules") is True,
                },
            }
        )

    expected = len(ART) + len(AVATARS) + len(ids)
    if len(items) != expected:
        raise SystemExit(f"expected {expected} manifest items, got {len(items)}")

    manifest = {
        "_note": (
            "Godstorm current-scope manifest, 2026-09-19. COMPLETE for currently "
            "safe executable writes only: create the three director-approved "
            "Stormcourt SCENE_BACKGROUND assets, update four accepted "
            "Marrow AI avatars, and apply the source-audited range-safe fallback "
            "correction to all 18 retained AI profiles. This intentionally does NOT "
            "mutate the two quests yet: exact player-facing copy, rewards/cadence/chest, "
            "Warden of the First Dark avatar, ten keeper "
            "SCENE_CHARACTER assets, and the blank SCENE_CHARACTER are still "
            "unresolved. No quest graph/content write is safe until those release "
            "dependencies are frozen. See docs/plans/GODSTORM_MANIFEST_STAGING.md "
            "and docs/reviews/REVIEW_2026-09-19_godstorm_ai_rule_safety.md."
        ),
        "dedupNames": True,
        "imgSizes": img_sizes,
        "items": items,
    }

    OUT.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print(
        f"wrote {OUT}: {len(items)} items "
        f"({len(ART)} asset creates, {len(AVATARS)} ai avatar edits, "
        f"{len(ids)} aiProfile edits)"
    )


if __name__ == "__main__":
    main()
