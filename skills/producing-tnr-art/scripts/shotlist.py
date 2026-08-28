#!/usr/bin/env python3
"""
shotlist.py - generate the art shot list FROM the quest graph.

Hand-authoring the shot list is where assets go missing, land at the wrong aspect, or get a
filename the manifest never references. The graph already knows what art it needs: every
distinct sceneBackground, every distinct sceneCharacter, every node that draws a map pin.
So read the graph and emit the requirements, each with the exact numbers from
25x_DATA_art_spec.json and the @img ref the manifest will use.

    python3 shotlist.py quest_capture.json [--spec 25x_DATA_art_spec.json]
                                           [--slug thorn] [--folder crimsonreckoning]
                                           [--json out.json] [--selftest]

Input is a `quests.get` capture (the tRPC envelope, a bare record, or a builder capture
bundle - all three are unwrapped). Existing asset ids are reported as SATISFIED and are not
put in the shot list; only the gaps are work.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

DEFAULT_SPEC = "25x_DATA_art_spec.json"

# Law 52: drawQuest returns early when an objective has no image, so no image means no pin.
# Dialog nodes draw a marker but nothing worth guiding to, so they are listed as optional.
PIN_TASKS = {"move_to_location", "collect_item", "deliver_item", "defeat_opponents"}

# Two different reference kinds, confirmed against a live capture of Copies, Not Thefts:
#   sceneBackground / sceneCharacters hold gameAsset IDS, resolved by gameAsset.getSceneAssets.
#   objectives[].image and quest.image hold RAW URLS - drawQuest passes objective.image straight
#   to loadTexture, and quest.image goes to ContentImage.
# So a pin needs no asset record at all: `image: "@img:file.webp"` resolves to the stored URL and
# is done. A scene character needs an asset record created first, then its id. Getting this
# backwards produces a manifest that pushes cleanly and renders nothing.
ID_FIELDS = ("sceneBackground", "sceneCharacters")
URL_FIELDS = ("image",)

# Suppressor assets: deliberately blank, deliberately reused on many nodes. Not a shared-face
# defect. `sceneCharacters` inheritance means a node with an explicit blank overrides the
# top-level character, which is how a scene is made to show nobody.
SUPPRESSOR_ASSET_IDS = {
    "1YXbXYW2wz3GETVMb6DT6",  # ghostship/Blank Scene Character
}
SUPPRESSOR_NAME_HINTS = ("blank", "theghost")
PIN_OPTIONAL_TASKS = {"dialog"}


# --------------------------------------------------------------------------- input

def asset_names_from_bundle(payload) -> dict:
    """Pull id -> name from any gameAsset.getAllNames captures in the same bundle.

    Reporting a bare nanoid tells nobody anything. The capture that fetches the quest normally
    fetches the name tables too, so use them rather than making the reader join by hand.
    """
    out: dict[str, str] = {}
    caps = payload.get("captures") if isinstance(payload, dict) else None
    for cap in caps or []:
        if cap.get("proc") != "gameAsset.getAllNames":
            continue
        for row in cap.get("data") or []:
            if isinstance(row, dict) and row.get("id"):
                out[row["id"]] = row.get("name") or ""
    return out


def unwrap(payload):
    """Find the quest record inside a tRPC envelope, a capture bundle, or a bare record."""
    seen = []

    def walk(node, depth=0):
        if depth > 8 or not isinstance(node, (dict, list)):
            return
        if isinstance(node, dict):
            if "content" in node and isinstance(node.get("content"), dict):
                if "objectives" in node["content"]:
                    seen.append(node)
            for value in node.values():
                walk(value, depth + 1)
        else:
            for value in node:
                walk(value, depth + 1)

    walk(payload)
    if not seen:
        raise SystemExit("error  no quest record found (looked for content.objectives)")
    return seen[0]


def slugify(text: str) -> str:
    out = re.sub(r"[^a-zA-Z0-9]+", "_", str(text)).strip("_").lower()
    return out or "x"


# --------------------------------------------------------------------------- extraction

def extract(quest: dict) -> dict:
    content = quest.get("content") or {}
    objectives = content.get("objectives") or []

    backgrounds: dict[str, list[str]] = {}
    characters: dict[str, list[str]] = {}
    pins: list[dict] = []

    def note(bucket: dict, value, where: str):
        if value:
            bucket.setdefault(str(value), []).append(where)

    note(backgrounds, content.get("sceneBackground"), "quest.content (travel popup)")
    for cid in content.get("sceneCharacters") or []:
        note(characters, cid, "quest.content (fallback)")

    for obj in objectives:
        oid = obj.get("id", "?")
        task = obj.get("task", "?")
        where = f"{oid} ({task})"
        note(backgrounds, obj.get("sceneBackground"), where)
        for cid in obj.get("sceneCharacters") or []:
            note(characters, cid, where)

        if task in PIN_TASKS or task in PIN_OPTIONAL_TASKS:
            pins.append(
                {
                    "objectiveId": oid,
                    "task": task,
                    "image": obj.get("image"),
                    "required": task in PIN_TASKS,
                    "locationType": obj.get("locationType"),
                    "longitude": obj.get("longitude"),
                    "latitude": obj.get("latitude"),
                    "sector": obj.get("sector"),
                    "description": (obj.get("description") or "").strip(),
                }
            )

    return {
        "questId": quest.get("id"),
        "questName": quest.get("name"),
        "objectiveCount": len(objectives),
        "backgrounds": backgrounds,
        "characters": characters,
        "pins": pins,
        "topLevelBackground": content.get("sceneBackground"),
        "consecutiveObjectives": quest.get("consecutiveObjectives"),
    }


# --------------------------------------------------------------------------- shot list

def render_prompt(spec: dict, target: str, subject: str | None = None,
                  frame: str | None = None) -> dict | None:
    """Assemble the generator prompt for one shot from spec.prompt_scaffolds.

    The scaffolds live in the spec rather than in prompts.md so that exactly one copy of the
    ratified wording exists. prompts.md cites this block; this function renders it. A clause
    that is paraphrased on the way to a generator stops being the ratified clause, which is
    how "smooth painterly shading" got in, so [STYLE] is expanded by joining the clause
    strings verbatim and never by restating them.

    [SUBJECT] is left literal when no subject is supplied. That is deliberate: an unfilled
    slot is visible in the emitted prompt, whereas a guessed subject is not.
    """
    ps = spec.get("prompt_scaffolds")
    if not ps:
        return None
    sc = ps.get("scaffolds", {}).get(target)
    if not sc:
        return None

    clauses = spec.get("house_style", {}).get("clauses", {})
    # Scoped per target: a clause about arms has no referent in a background or a pin, and the
    # generator will still try to satisfy it. Falls back to the global order if the spec
    # predates the scope block.
    order = (ps.get("style_clause_scope", {}).get("by_target", {}).get(target)
             or ps.get("style_clause_order", []))
    style = ", ".join(clauses[k] for k in order if k in clauses)

    if "positive_by_frame" in sc:
        frame = frame or sc.get("default_frame")
        positive = sc["positive_by_frame"][frame]
    else:
        positive = sc["positive"]

    positive = positive.replace(ps.get("style_token", "[STYLE]"), style)
    subject_token = ps.get("subject_token", "[SUBJECT]")
    if subject:
        positive = positive.replace(subject_token, subject)

    out = {
        "positive": positive,
        "negative": sc.get("negative"),
        "subject_filled": bool(subject),
    }
    if sc.get("subject_label"):
        label = sc["subject_label"]
        out["subject_line"] = label.replace(subject_token, subject) if subject else label
    if sc.get("carries_costume_grammar"):
        hs = spec.get("house_style", {})
        out["costume_grammar"] = hs.get("costume_grammar")
        out["hard_negatives"] = hs.get("hard_negatives")
    for extra in ("reserve_note", "design_note", "length_rule"):
        if sc.get(extra):
            out[extra] = sc[extra]
    return out


def shot(spec: dict, target: str, slug: str, folder: str, index: int, note: str,
         subject: str | None = None, frame: str | None = None) -> dict:
    t = spec["targets"][target]
    aspect = t["aspect"]
    accepted = aspect.get("accepted") or ([aspect["value"]] if aspect.get("value") else [])
    suffix = {
        "SCENE_BACKGROUND": "background",
        "SCENE_CHARACTER": "scene_char",
        "STATIC": "pin",
    }[target]
    filename = f"{slug}_{index:02d}_{suffix}.{t['format']}"
    return {
        "target": target,
        "gameAsset_type": t.get("gameAsset_type"),
        "filename": filename,
        "img_ref": f"@img:{filename}",
        "folder": folder,
        "aspect_accepted": accepted,
        "aspect_rule": aspect.get("rule"),
        "min_width_px": t.get("min_width_px", {}).get("value"),
        "recommended_source_px": t.get("recommended_source_px", {}).get("value"),
        "delivered_width_px": t.get("delivered_width_px"),
        "format": t["format"],
        "format_mode": t.get("format_mode"),
        "byte_ceiling_bytes": t.get("byte_ceiling_bytes"),
        "chroma_key": t.get("chroma_key"),
        "padding_rule": t.get("padding_rule"),
        "client_field": t.get("client_field"),
        "note": note,
        "prompt": render_prompt(spec, target, subject, frame),
    }


def build(quest: dict, spec: dict, slug: str, folder: str,
          asset_names: dict | None = None) -> dict:
    found = extract(quest)
    slug = slug or slugify(found.get("questName") or "quest")
    folder = folder or re.sub(r"[^a-zA-Z0-9]", "", slug)

    shots: list[dict] = []
    satisfied: list[dict] = []
    warnings: list[str] = []
    index = 0

    for asset_id, uses in found["backgrounds"].items():
        satisfied.append({"target": "SCENE_BACKGROUND", "ref": "id", "assetId": asset_id,
                          "name": (asset_names or {}).get(asset_id), "usedBy": uses,
                          "reuse": len(uses)})
    for asset_id, uses in found["characters"].items():
        satisfied.append({"target": "SCENE_CHARACTER", "ref": "id", "assetId": asset_id,
                          "name": (asset_names or {}).get(asset_id), "usedBy": uses,
                          "reuse": len(uses)})

    # Law 25: the travel popup renders content.sceneBackground only, and the client fallback
    # is arbitrary when it is empty.
    if not found["topLevelBackground"]:
        index += 1
        shots.append(
            shot(spec, "SCENE_BACKGROUND", slug, folder, index,
                 "quest.content.sceneBackground is empty. The travel-page popup renders this "
                 "field ONLY and falls back arbitrarily. Set a deliberate global scene, "
                 "normally the entry exterior.")
        )

    for pin in found["pins"]:
        if pin["image"]:
            satisfied.append({"target": "STATIC", "ref": "url", "assetId": pin["image"],
                              "usedBy": [pin["objectiveId"]], "reuse": 1})
            continue
        if not pin["required"]:
            continue
        index += 1
        shots.append(
            shot(spec, "STATIC", slug, folder, index,
                 f"objective {pin['objectiveId']} ({pin['task']}) has no image, so it draws NO "
                 f"map pin. Marker tint is fixed by task, so the pin must carry meaning through "
                 f"silhouette and read at 50px inside a circular mask.",
                 subject=pin.get("description") or None)
        )
        if pin["locationType"] == "specific" and not (pin["longitude"] and pin["latitude"]):
            warnings.append(
                f"{pin['objectiveId']}: locationType 'specific' with no coordinates places the "
                f"objective at tile 0,0 (law 54)"
            )

    # Law 48: one scene character per node; extras stack in the same spot.
    for obj_uses in found["characters"].values():
        pass
    per_node: dict[str, int] = {}
    for uses in found["characters"].values():
        for use in uses:
            per_node[use] = per_node.get(use, 0) + 1
    for node, count in per_node.items():
        if count > 1:
            warnings.append(
                f"{node}: {count} scene characters. The client renders every entry at "
                f"`absolute bottom-0 w-2/5`, so they stack in one spot (law 48)"
            )

    # The RenWake defect, generalised: one image doing the work of many named characters.
    for asset_id, uses in found["characters"].items():
        if len(uses) < 4 or asset_id in SUPPRESSOR_ASSET_IDS:
            continue
        name = (asset_names or {}).get(asset_id, "")
        if any(h in name.lower().replace(" ", "") for h in SUPPRESSOR_NAME_HINTS):
            continue
        label = f"{name} ({asset_id})" if name else asset_id
        warnings.append(
            f"asset {label} is the scene character for {len(uses)} nodes. Check it is one NPC "
            f"appearing repeatedly and not several NPCs sharing one face"
        )

    return {
        "quest": {
            "id": found["questId"],
            "name": found["questName"],
            "objectives": found["objectiveCount"],
            "consecutiveObjectives": found["consecutiveObjectives"],
        },
        "slug": slug,
        "folder": folder,
        "shots": shots,
        "satisfied": satisfied,
        "warnings": warnings,
        "house_style": spec["house_style"]["name"],
    }


# --------------------------------------------------------------------------- output

def render(result: dict) -> str:
    q = result["quest"]
    lines = [
        f"SHOT LIST  {q['name']}  ({q['id']})",
        f"  {q['objectives']} objectives, slug `{result['slug']}`, folder `{result['folder']}`",
        f"  house style: {result['house_style']}",
        "",
    ]

    if result["satisfied"]:
        lines.append(f"SATISFIED ({len(result['satisfied'])} assets already wired)")
        for s in result["satisfied"]:
            reuse = f" x{s['reuse']}" if s["reuse"] > 1 else ""
            label = s.get("name") or s["assetId"]
            if s.get("ref") == "url" and not s.get("name"):
                label = "(url) " + s["assetId"].rsplit("/", 1)[-1][:24]
            lines.append(f"  {s['target']:17} {label}{reuse}")
        lines.append("")

    if result["shots"]:
        lines.append(f"TO GENERATE ({len(result['shots'])})")
        for s in result["shots"]:
            lines.append(f"  {s['filename']}")
            lines.append(f"    type      {s['target']} -> gameAsset {s['gameAsset_type']}")
            lines.append(f"    aspect    {' or '.join(s['aspect_accepted'])}"
                         + (f"  ({s['aspect_rule']})" if s["aspect_rule"] else ""))
            lines.append(f"    source    {s['recommended_source_px']}  (min width {s['min_width_px']}px, "
                         f"delivered at {s['delivered_width_px']}px)")
            lines.append(f"    export    {s['format']} {s['format_mode']}, "
                         f"under {s['byte_ceiling_bytes'] // 1024}KB"
                         + (f", chroma {s['chroma_key']}" if s["chroma_key"] else ""))
            lines.append(f"    manifest  {s['img_ref']}   folder: {s['folder']}")
            lines.append(f"    why       {s['note']}")
            lines.append("")
    else:
        lines.append("TO GENERATE (0) - every asset this graph needs is already wired.\n")

    if result["warnings"]:
        lines.append(f"WARNINGS ({len(result['warnings'])})")
        for w in result["warnings"]:
            lines.append(f"  {w}")
        lines.append("")

    return "\n".join(lines)


# --------------------------------------------------------------------------- selftest

FIXTURE = {
    "id": "q-selftest",
    "name": "The Nameless Thorn",
    "consecutiveObjectives": True,
    "content": {
        "sceneBackground": None,
        "sceneCharacters": [],
        "objectives": [
            {"id": "a1", "task": "dialog", "sceneBackground": "bg-safehouse",
             "sceneCharacters": ["sc-handler"], "image": None},
            {"id": "a2", "task": "dialog", "sceneBackground": "bg-safehouse",
             "sceneCharacters": ["sc-handler", "sc-kanna"], "image": None},
            {"id": "b1", "task": "move_to_location", "sceneBackground": "bg-alley",
             "sceneCharacters": [], "image": None,
             "locationType": "specific", "longitude": 0, "latitude": 0},
            {"id": "b2", "task": "defeat_opponents", "sceneBackground": "bg-alley",
             "sceneCharacters": [], "image": "static-crossedblades"},
            {"id": "c1", "task": "deliver_item", "sceneBackground": None,
             "sceneCharacters": ["sc-handler"], "image": None},
            {"id": "c2", "task": "dialog", "sceneBackground": "bg-safehouse",
             "sceneCharacters": ["sc-handler"], "image": None},
            {"id": "d1", "task": "dialog", "sceneBackground": "bg-safehouse",
             "sceneCharacters": ["sc-handler"], "image": None},
            {"id": "w1", "task": "win_quest"},
        ],
    },
}


def selftest(spec: dict) -> int:
    result = build(unwrap({"result": {"data": {"json": FIXTURE}}}), spec, "", "",
                   {"sc-handler": "test/Handler"})
    failures = []

    checks = []

    def want(cond, label):
        # Counted rather than hardcoded: a hardcoded total silently stops matching the moment
        # a check is added, and then the pass count is fiction.
        checks.append(label)
        if not cond:
            failures.append(label)

    filenames = [s["filename"] for s in result["shots"]]
    targets = [s["target"] for s in result["shots"]]

    want(result["slug"] == "the_nameless_thorn", "slug derived from quest name")
    want("SCENE_BACKGROUND" in targets, "empty top-level sceneBackground raises a shot")
    want(targets.count("STATIC") == 2, "two pinless required-pin nodes raise two STATIC shots")
    want(all(f.endswith(".webp") for f in filenames), "every filename carries the spec format")
    want(all(s["img_ref"] == "@img:" + s["filename"] for s in result["shots"]),
         "@img ref matches the filename exactly")
    want(len({s["filename"] for s in result["shots"]}) == len(filenames), "filenames unique")

    sat_ids = {s["assetId"] for s in result["satisfied"]}
    want(sat_ids == {"bg-safehouse", "bg-alley", "sc-handler", "sc-kanna", "static-crossedblades"},
         "every wired asset reported as satisfied and none of them re-listed as work")

    joined = " | ".join(result["warnings"])
    want("a2" in joined and "stack" in joined, "law 48 stacking warning on the two-character node")
    want("b1" in joined and "0,0" in joined, "law 54 coordinate warning")
    want("sc-handler" in joined, "shared-face warning on the 5-node character")

    sc_shot_targets = [s for s in result["shots"] if s["target"] == "SCENE_CHARACTER"]
    want(not sc_shot_targets, "no scene-character shot raised when all are wired")

    static = next(s for s in result["shots"] if s["target"] == "STATIC")
    want(static["delivered_width_px"] == 50, "STATIC carries the 50px delivered width from spec")
    want(static["aspect_accepted"] == ["1:1"], "STATIC aspect read from spec")

    bg = next(s for s in result["shots"] if s["target"] == "SCENE_BACKGROUND")
    want(bg["format_mode"] == "lossy_q85", "background export mode read from spec")
    want(bg["chroma_key"] is None, "background carries no chroma key")

    # Prompt emission. The scaffolds live in the spec, so a shot without a prompt means the
    # spec lost its prompt_scaffolds block, not that this quest needed no art direction.
    want(all(s.get("prompt") for s in result["shots"]), "every shot carries a rendered prompt")
    want("[STYLE]" not in bg["prompt"]["positive"], "[STYLE] expanded, not left as a token")
    want("crisp pixel lineart" in bg["prompt"]["positive"],
         "house_style clauses pasted verbatim into the prompt")
    want("smooth painterly" not in bg["prompt"]["positive"].lower()
         and "rim lighting" not in bg["prompt"]["positive"].lower(),
         "struck clauses absent from every rendered prompt")
    want(bg["prompt"]["subject_filled"] is False and "[SUBJECT]" in bg["prompt"]["positive"],
         "an unsupplied subject stays a visible [SUBJECT] slot rather than being invented")
    want(bg["prompt"].get("reserve_note"), "background prompt carries the lower-left reserve note")
    want(static["prompt"].get("design_note"), "pin prompt carries the 50px silhouette rule")
    want(static["prompt"]["negative"] and "no thin lines" in static["prompt"]["negative"],
         "pin negatives rendered from the spec")

    for label in failures:
        print(f"  FAIL  {label}")
    passed = len(checks) - len(failures)
    print(f"\n{passed} passed, {len(failures)} failed")
    if not failures:
        print("\n--- rendered output ---\n")
        print(render(result))
    return len(failures)


# --------------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("capture", nargs="?")
    ap.add_argument("--spec", default=DEFAULT_SPEC)
    ap.add_argument("--slug", default="")
    ap.add_argument("--folder", default="")
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.spec):
        raise SystemExit(f"error  spec not found: {args.spec}")
    with open(args.spec) as fh:
        spec = json.load(fh)

    if args.selftest:
        return selftest(spec)

    if not args.capture:
        raise SystemExit("error  pass a quests.get capture, or --selftest")

    with open(args.capture) as fh:
        payload = json.load(fh)

    result = build(unwrap(payload), spec, args.slug, args.folder,
                   asset_names_from_bundle(payload))
    print(render(result))
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(result, fh, indent=1)
        print(f"written  {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
