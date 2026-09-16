#!/usr/bin/env python3
"""Static adversarial contract test for the Quest Studio source-push worker."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github" / "workflows" / "quest_studio.yml"


def require(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle not in text:
        failures.append(label)


def forbid(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle in text:
        failures.append(label)


def require_order(text: str, needles: list[str], label: str, failures: list[str]) -> None:
    positions = [text.find(needle) for needle in needles]
    if any(pos < 0 for pos in positions) or positions != sorted(positions):
        failures.append(label)


def workflow_run_text(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        match = re.match(r"^(\s*)run:\s*(.*?)\s*$", line)
        if not match:
            continue
        indent = len(match.group(1))
        value = match.group(2)
        if value and not re.fullmatch(r"[|>][+-]?", value):
            out.append(value)
            continue
        for body in lines[i + 1:]:
            if body.strip() and len(body) - len(body.lstrip()) <= indent:
                break
            out.append(body)
    return "\n".join(out)


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    failures: list[str] = []

    # Trigger model: authored Quest Source pushes, not repository-wide Actions dispatch permission.
    require(text, 'branches:', "worker declares a branch filter", failures)
    require(text, '- "studio/quest/**"', "worker is scoped to Studio request branches", failures)
    require(text, 'paths:', "worker declares a path filter", failures)
    require(text, '- "studio/requests/*.quest.json"', "worker triggers only on Quest Source writes", failures)
    forbid(text, "workflow_dispatch", "worker does not require workflow_dispatch", failures)
    forbid(text, "${{ inputs.", "worker has no workflow_dispatch inputs", failures)

    # Executable code and authored data are separate. Compiler code comes from trusted main.
    require(text, "name: Checkout trusted compiler", "trusted compiler checkout exists", failures)
    require(text, "ref: main", "compiler checkout comes from trusted main", failures)
    require(text, "path: tools", "trusted compiler checkout is isolated under tools/", failures)
    require(text, "persist-credentials: false", "trusted compiler checkout cannot push", failures)
    require(text, "git -C tools rev-parse HEAD", "compiler revision is measured from trusted checkout", failures)
    require(text, "name: Checkout authored request source", "request checkout exists", failures)
    require(text, "ref: ${{ steps.identity.outputs.source_sha }}", "request checkout is pinned to push SHA", failures)
    require(text, "path: request", "request checkout is isolated under request/", failures)

    # Push identity must be validated before authored content is checked out or compiled.
    require(text, "name: Validate push identity", "push identity validation exists", failures)
    require(text, 'REQUEST_BRANCH: ${{ github.ref_name }}', "request branch comes from push event", failures)
    require(text, 'SOURCE_SHA: ${{ github.sha }}', "source revision comes from exact push SHA", failures)
    require(text, '[[ "$REQUEST_BRANCH" == studio/quest/* ]]', "request branch prefix is validated", failures)
    require(text, 'SOURCE_PATH="studio/requests/$REQUEST_ID.quest.json"', "source path is derived from validated request id", failures)
    require_order(
        text,
        [
            "name: Validate push identity",
            "name: Checkout authored request source",
            "name: Validate request content",
            "name: Compile Quest Source",
        ],
        "push validation precedes request checkout and compile",
        failures,
    )

    # The only executed compiler path comes from tools/. Request branch content is data only.
    require(text, "python3 tools/skills/building-tnr-content/scripts/quest_compile.py", "canonical compiler runs from trusted checkout", failures)
    forbid(text, "python3 request/", "request checkout cannot provide executable Python", failures)
    forbid(text, "bash request/", "request checkout cannot provide executable shell", failures)
    forbid(text, "sh request/", "request checkout cannot provide executable shell", failures)

    run_text = workflow_run_text(text)
    forbid(run_text, "${{ inputs.", "untrusted workflow inputs are not interpolated into shell", failures)
    forbid(run_text, "${{ github.event.inputs.", "legacy workflow input expressions are not interpolated into shell", failures)

    # Persistence is request-scoped and refuses to publish an obsolete result if the branch advanced.
    require(text, 'RESULT_PATH="request/studio/results/$REQUEST_ID.build.json"', "result path is request-scoped", failures)
    require(text, 'BUILD_PATH="request/studio/builds/$REQUEST_ID"', "build path is request-scoped", failures)
    require(text, '[[ "$REMOTE_SHA" == "$SOURCE_SHA" ]]', "stale source result is refused before persistence", failures)
    require(text, 'git -C request add -- "studio/results/$REQUEST_ID.build.json" "studio/builds/$REQUEST_ID"', "git add allowlists generated paths", failures)
    forbid(text, "git -C tools push", "trusted compiler checkout is never pushed", failures)

    # Worker remains compile-only and contains no live-game path.
    for token in ("theninja-rpg.com", "/api/trpc", "curl ", "wget "):
        forbid(text.lower(), token.lower(), f"worker contains no live-game/network token {token}", failures)

    if failures:
        for label in failures:
            print(f"FAIL  {label}")
        print()
        print(f"{len(failures)} contract failures")
        return 1

    for label in (
        "source-push trigger requires no Actions dispatch",
        "trusted compiler/request checkouts separated",
        "push identity and source SHA fail closed",
        "authored request checkout never executed",
        "generated persistence confined to request paths",
        "worker has no live-game path",
    ):
        print(f"PASS  {label}")
    print()
    print("Quest Studio source-push trust boundary pinned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
