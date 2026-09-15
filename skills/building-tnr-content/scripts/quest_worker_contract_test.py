#!/usr/bin/env python3
"""Static adversarial contract test for the Quest Studio GitHub Actions worker.

This test deliberately does not execute the workflow. It pins the security boundary that lets
Forge submit authored Quest Source while repository code remains the executable authority.
"""

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


def run_script_text(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        match = re.match(r"^(\s*)run:\s*(.*)$", line)
        if not match:
            continue
        indent = len(match.group(1))
        scalar = match.group(2).strip()
        if re.fullmatch(r"[|>][+-]?", scalar):
            for body in lines[i + 1:]:
                if body.strip() and len(body) - len(body.lstrip()) <= indent:
                    break
                out.append(body)
        elif scalar:
            out.append(scalar)
    return "\n".join(out)


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    failures: list[str] = []

    # Trusted executable code and untrusted authored source must live in separate checkouts.
    require(text, "name: Checkout trusted compiler", "trusted compiler checkout exists", failures)
    require(text, "ref: ${{ github.sha }}", "compiler checkout is pinned to workflow SHA", failures)
    require(text, "path: tools", "trusted compiler checkout is isolated under tools/", failures)
    require(text, "name: Checkout authored request source", "request checkout exists", failures)
    require(text, "ref: ${{ inputs.source_sha }}", "request checkout is pinned to exact source SHA", failures)
    require(text, "path: request", "request checkout is isolated under request/", failures)

    # Dispatch identity must be validated before authored content is checked out or compiled.
    require(text, "name: Validate dispatch identity", "dispatch identity validation exists", failures)
    require(text, "name: Validate request content", "request content validation exists", failures)
    require_order(
        text,
        [
            "name: Validate dispatch identity",
            "name: Checkout authored request source",
            "name: Validate request content",
            "name: Compile Quest Source",
        ],
        "dispatch validation precedes request checkout and compile",
        failures,
    )

    # Dispatch must execute the trusted workflow on main and bind branch/path/id exactly.
    require(text, '[[ "$TRUSTED_REF" == "refs/heads/main" ]]', "dispatch is main-only", failures)
    require(text, '[[ "$REQUEST_BRANCH" == "studio/quest/$REQUEST_ID" ]]', "request branch matches id", failures)
    require(text, '[[ "$SOURCE_PATH" == "studio/requests/$REQUEST_ID.quest.json" ]]', "source path matches id", failures)
    require(text, 'if [[ "$ACTUAL_SHA" != "$SOURCE_SHA" ]]; then', "request checkout SHA is verified after exact-SHA checkout", failures)
    require(text, '! -f "request/$SOURCE_PATH" || -L "request/$SOURCE_PATH"', "source must be a regular non-symlink file", failures)

    # The only executed compiler path must come from tools/. Authored request code is data only.
    require(text, "python3 tools/skills/building-tnr-content/scripts/quest_compile.py", "canonical compiler runs from trusted checkout", failures)
    forbid(text, "python3 request/", "request checkout cannot provide executable Python", failures)
    forbid(text, "bash request/", "request checkout cannot provide executable shell", failures)
    forbid(text, "sh request/", "request checkout cannot provide executable shell", failures)

    # Workflow expressions for untrusted inputs belong in env/ref fields, never interpolated into run scripts.
    run_text = run_script_text(text)
    if re.search(r"\$\{\{\s*(?:github\.event\.)?inputs\.", run_text):
        failures.append("untrusted workflow inputs are not interpolated into shell")

    # Persistence is confined to the request's result/build directories.
    require(text, 'RESULT_PATH="request/studio/results/$REQUEST_ID.build.json"', "result path is request-scoped", failures)
    require(text, 'BUILD_PATH="request/studio/builds/$REQUEST_ID"', "build path is request-scoped", failures)
    require(text, 'git -C request add -- "studio/results/$REQUEST_ID.build.json" "studio/builds/$REQUEST_ID"', "git add allowlists generated paths", failures)
    forbid(text, "git -C tools push", "trusted compiler checkout is never pushed", failures)

    # Repo worker is compile-only and must contain no live-game path.
    for token in ("theninja-rpg.com", "/api/trpc", "curl ", "wget "):
        forbid(text.lower(), token.lower(), f"worker contains no live-game/network token {token}", failures)

    checks = 26
    if failures:
        for label in failures:
            print(f"FAIL  {label}")
        print(f"\n{checks - len(failures)} passed, {len(failures)} failed")
        return 1

    for label in (
        "trusted compiler/request checkouts separated",
        "main-only dispatch and exact request identity pinned",
        "authored request checkout never executed",
        "untrusted inputs kept out of shell interpolation",
        "generated persistence confined to request paths",
        "worker has no live-game path",
    ):
        print(f"PASS  {label}")
    print("\nQuest Studio worker trust boundary pinned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
