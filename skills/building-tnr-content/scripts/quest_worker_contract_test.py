#!/usr/bin/env python3
"""Static adversarial contract test for the Quest Studio GitHub Actions worker.

This test deliberately does not execute the workflow. It pins the security boundary that lets
Forge submit authored Quest Source while repository code remains the executable authority.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github" / "workflows" / "quest_studio.yml"


def require(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle not in text:
        failures.append(label)


def forbid(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle in text:
        failures.append(label)


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    failures: list[str] = []

    # Trusted executable code and untrusted authored source must live in separate checkouts.
    require(text, "name: Checkout trusted compiler", "trusted compiler checkout exists", failures)
    require(text, "ref: ${{ github.sha }}", "compiler checkout is pinned to workflow SHA", failures)
    require(text, "path: tools", "trusted compiler checkout is isolated under tools/", failures)
    require(text, "name: Checkout authored request branch", "request checkout exists", failures)
    require(text, "ref: ${{ inputs.request_branch }}", "request checkout follows request branch input", failures)
    require(text, "path: request", "request checkout is isolated under request/", failures)

    # Dispatch must execute the trusted workflow on main and bind branch/path/id exactly.
    require(text, '[[ "$TRUSTED_REF" == "refs/heads/main" ]]', "dispatch is main-only", failures)
    require(text, '[[ "$REQUEST_BRANCH" == "studio/quest/$REQUEST_ID" ]]', "request branch matches id", failures)
    require(text, '[[ "$SOURCE_PATH" == "studio/requests/$REQUEST_ID.quest.json" ]]', "source path matches id", failures)
    require(text, '[[ "$ACTUAL_SHA" == "$SOURCE_SHA" ]]', "request checkout is exact-SHA pinned", failures)
    require(text, '[[ -f "request/$SOURCE_PATH" && ! -L "request/$SOURCE_PATH" ]]', "source must be a regular non-symlink file", failures)

    # The only executed compiler path must come from tools/. Authored request code is data only.
    require(text, "python3 tools/skills/building-tnr-content/scripts/quest_compile.py", "canonical compiler runs from trusted checkout", failures)
    forbid(text, "python3 request/", "request checkout cannot provide executable Python", failures)
    forbid(text, "bash request/", "request checkout cannot provide executable shell", failures)
    forbid(text, "sh request/", "request checkout cannot provide executable shell", failures)

    # Workflow expressions for untrusted inputs belong in env/ref fields, never interpolated into run scripts.
    in_run = False
    run_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("run: |"):
            in_run = True
            continue
        if in_run:
            # Every multiline run body here is indented ten spaces or more; a new step ends it.
            if line.startswith("      - name:") or line.startswith("      - uses:"):
                in_run = False
            else:
                run_lines.append(line)
    run_text = "\n".join(run_lines)
    forbid(run_text, "${{ inputs.", "untrusted workflow inputs are not interpolated into shell", failures)

    # Persistence is confined to the request's result/build directories.
    require(text, 'RESULT_PATH="request/studio/results/$REQUEST_ID.build.json"', "result path is request-scoped", failures)
    require(text, 'BUILD_PATH="request/studio/builds/$REQUEST_ID"', "build path is request-scoped", failures)
    require(text, 'git -C request add -- "studio/results/$REQUEST_ID.build.json" "studio/builds/$REQUEST_ID"', "git add allowlists generated paths", failures)
    forbid(text, "git -C tools push", "trusted compiler checkout is never pushed", failures)

    # Repo worker is compile-only and must contain no live-game path.
    for token in ("theninja-rpg.com", "/api/trpc", "curl ", "wget "):
        forbid(text.lower(), token.lower(), f"worker contains no live-game/network token {token}", failures)

    checks = 21
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
