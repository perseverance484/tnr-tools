#!/usr/bin/env python3
"""Repository-layout integration test for the Quest Studio Mission adapter.

This deliberately does not call mission.py --selftest: that legacy selftest currently carries
an old D-combat fixture whose headcount conflicts with today's mission profile. Quest Studio's
seam needs to prove something narrower and current: a source that is valid under the CURRENT D
profile can travel through mission.py, shotlist.py and validate.py and return a valid build.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile

import quest_compile


def main() -> int:
    source = {
        "schemaVersion": 1,
        "kind": "quest",
        "requestId": "selftest-mission-current",
        "subtype": "mission",
        "content": {
            "rank": "D",
            "srcId": "studio_selftest_mission_current",
            "slug": "studio_selftest_mission_current",
            "folder": "studio_selftest_mission_current",
            "name": "Quest Studio Current Mission Selftest",
            "description": "A messenger follows a short sequence of instructions.",
            "successDescription": "The instructions are complete.",
            "objectives": [
                {
                    "id": "n1",
                    "task": "dialog",
                    "description": "Read the first instruction.",
                    "nextObjectiveId": [{"text": "Continue", "nextObjectiveId": "n2"}],
                },
                {
                    "id": "n2",
                    "task": "dialog",
                    "description": "Confirm the second instruction.",
                    "nextObjectiveId": [{"text": "Continue", "nextObjectiveId": "n3"}],
                },
                {
                    "id": "n3",
                    "task": "dialog",
                    "description": "Report that the route is clear.",
                    "nextObjectiveId": [{"text": "Finish", "nextObjectiveId": "n4"}],
                },
                {
                    "id": "n4",
                    "task": "win_quest",
                    "description": "Complete the mission.",
                    "successDescription": "The report is delivered.",
                },
            ],
        },
    }

    root = Path(tempfile.mkdtemp(prefix="tnr-quest-studio-"))
    try:
        result = quest_compile.compile_source(
            source,
            artifact_dir=root / "build",
            artifact_prefix="studio/builds/selftest-mission-current",
            source_revision="1" * 40,
            compiler_revision="2" * 40,
        )
        if result.get("status") != "valid":
            print(json.dumps(result, indent=2))
            raise SystemExit("Mission adapter did not produce a valid build")
        if result.get("resolvedEngineType") != "mission":
            raise SystemExit("Mission adapter did not resolve engine type mission")
        if result.get("liveGameTouched") is not False:
            raise SystemExit("Repository compile result must state liveGameTouched:false")
        if result.get("provenance", {}).get("sourceRevision") != "1" * 40:
            raise SystemExit("source revision provenance was not preserved")
        manifest = root / "build" / "manifest.json"
        if not manifest.is_file():
            raise SystemExit("Mission adapter did not materialize manifest.json")
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        quest = next((x for x in payload.get("items", []) if x.get("entity") == "quest"), None)
        if not quest or quest.get("data", {}).get("questType") != "mission":
            raise SystemExit("generated manifest does not contain a mission quest entry")
        print("PASS  current D Mission source compiles through mission.py + validate.py")
        print("PASS  provenance and live-game boundary are preserved")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
