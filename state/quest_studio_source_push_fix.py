#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one replacement, found {count}: {old[:100]!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def replace_count(path: Path, old: str, new: str, expected: int) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"{path}: expected {expected} replacements, found {count}: {old[:100]!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def replace_test(path: Path, name: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    marker = f'test("{name}"'
    start = text.find(marker)
    if start < 0:
        raise SystemExit(f"{path}: test not found: {name}")
    end = text.find('\n\ntest("', start + len(marker))
    if end < 0:
        end = len(text)
    new = text[:start] + replacement.rstrip() + text[end:]
    path.write_text(new, encoding="utf-8")


WORKER = '''name: quest-studio

on:
  push:
    branches:
      - "studio/quest/**"
    paths:
      - "studio/requests/*.quest.json"

permissions:
  contents: write

# A newer source revision for the same request supersedes an older in-flight compile.
concurrency:
  group: quest-studio-${{ github.ref }}
  cancel-in-progress: true

jobs:
  compile:
    runs-on: ubuntu-latest
    steps:
      # The browser credential only writes authored data. Executable compiler code is always
      # checked out separately from the current trusted main branch and never from the request branch.
      - name: Checkout trusted compiler
        uses: actions/checkout@v4
        with:
          ref: main
          path: tools
          fetch-depth: 1
          persist-credentials: false

      - name: Resolve trusted compiler revision
        id: compiler
        run: echo "compiler_sha=$(git -C tools rev-parse HEAD)" >> "$GITHUB_OUTPUT"

      - name: Validate push identity
        id: identity
        env:
          REQUEST_BRANCH: ${{ github.ref_name }}
          SOURCE_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail
          [[ "$REQUEST_BRANCH" == studio/quest/* ]] || { echo "invalid Quest Studio request branch" >&2; exit 2; }
          REQUEST_ID="${REQUEST_BRANCH#studio/quest/}"
          [[ "$REQUEST_ID" =~ ^[a-z0-9][a-z0-9._-]{2,63}$ ]] || { echo "invalid request id" >&2; exit 2; }
          [[ "$SOURCE_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "invalid source sha" >&2; exit 2; }
          SOURCE_PATH="studio/requests/$REQUEST_ID.quest.json"
          {
            echo "request_branch=$REQUEST_BRANCH"
            echo "request_id=$REQUEST_ID"
            echo "source_path=$SOURCE_PATH"
            echo "source_sha=$SOURCE_SHA"
          } >> "$GITHUB_OUTPUT"

      - name: Checkout authored request source
        uses: actions/checkout@v4
        with:
          ref: ${{ steps.identity.outputs.source_sha }}
          path: request
          fetch-depth: 1

      - name: Validate request content
        id: boundary
        env:
          SOURCE_PATH: ${{ steps.identity.outputs.source_path }}
          REQUEST_ID: ${{ steps.identity.outputs.request_id }}
          SOURCE_SHA: ${{ steps.identity.outputs.source_sha }}
          RUNNER_TEMP: ${{ runner.temp }}
        run: |
          set -euo pipefail
          ERROR=""
          ACTUAL_SHA="$(git -C request rev-parse HEAD)"
          if [[ "$ACTUAL_SHA" != "$SOURCE_SHA" ]]; then
            ERROR="request checkout mismatch: expected $SOURCE_SHA, checked out $ACTUAL_SHA"
          fi
          if [[ -z "$ERROR" ]]; then
            for p in request/studio request/studio/requests request/studio/results request/studio/builds; do
              if [[ -L "$p" ]]; then
                ERROR="refusing symlinked Studio path: $p"
                break
              fi
            done
          fi
          if [[ -z "$ERROR" && ( ! -f "request/$SOURCE_PATH" || -L "request/$SOURCE_PATH" ) ]]; then
            ERROR="Quest Source is missing, not a regular file, or is a symlink"
          fi

          if [[ -n "$ERROR" ]]; then
            echo "$ERROR" >&2
            TMP_ROOT="$RUNNER_TEMP/tnr-quest-studio/$REQUEST_ID"
            mkdir -p "$TMP_ROOT"
            printf '%s\n' "$ERROR" > "$TMP_ROOT/boundary-error.txt"
            echo "boundary_rc=2" >> "$GITHUB_OUTPUT"
          else
            echo "boundary_rc=0" >> "$GITHUB_OUTPUT"
          fi

      - name: Compile Quest Source
        id: compile
        env:
          SOURCE_PATH: ${{ steps.identity.outputs.source_path }}
          REQUEST_ID: ${{ steps.identity.outputs.request_id }}
          SOURCE_SHA: ${{ steps.identity.outputs.source_sha }}
          COMPILER_SHA: ${{ steps.compiler.outputs.compiler_sha }}
          BOUNDARY_RC: ${{ steps.boundary.outputs.boundary_rc }}
          RUNNER_TEMP: ${{ runner.temp }}
        run: |
          set -uo pipefail
          TMP_ROOT="$RUNNER_TEMP/tnr-quest-studio/$REQUEST_ID"
          TMP_BUILD="$TMP_ROOT/build"
          TMP_RESULT="$TMP_ROOT/build-result.json"
          mkdir -p "$TMP_BUILD"

          if [[ "$BOUNDARY_RC" != "0" ]]; then
            ERROR_MESSAGE="$(cat "$TMP_ROOT/boundary-error.txt")"
            python3 - "$TMP_RESULT" "$REQUEST_ID" "$SOURCE_SHA" "$COMPILER_SHA" "$ERROR_MESSAGE" <<'PY'
          import json
          from pathlib import Path
          import sys
          result_path, request_id, source_sha, compiler_sha, message = sys.argv[1:]
          result = {
              "schemaVersion": 1,
              "kind": "quest-build",
              "requestId": request_id,
              "subtype": None,
              "status": "failed",
              "resolvedEngineType": None,
              "blockers": [],
              "errors": [{"code": "request_boundary_failed", "message": message}],
              "warnings": [],
              "generated": {},
              "art": None,
              "validation": None,
              "provenance": {
                  "sourceSha256": None,
                  "sourceRevision": source_sha,
                  "compilerRevision": compiler_sha,
                  "registrySchemaVersion": None,
                  "compiler": "skills/building-tnr-content/scripts/quest_compile.py",
              },
              "liveGameTouched": False,
          }
          Path(result_path).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
          PY
            RC="$BOUNDARY_RC"
          else
            set +e
            python3 tools/skills/building-tnr-content/scripts/quest_compile.py \
              "request/$SOURCE_PATH" \
              --result "$TMP_RESULT" \
              --artifact-dir "$TMP_BUILD" \
              --artifact-prefix "studio/builds/$REQUEST_ID" \
              --source-revision "$SOURCE_SHA" \
              --compiler-revision "$COMPILER_SHA" \
              --request-id "$REQUEST_ID"
            RC=$?
            set -e
          fi

          test -f "$TMP_RESULT" || { echo "compiler produced no build result" >&2; exit 4; }
          echo "compile_rc=$RC" >> "$GITHUB_OUTPUT"

      - name: Persist build result to request branch
        env:
          REQUEST_BRANCH: ${{ steps.identity.outputs.request_branch }}
          REQUEST_ID: ${{ steps.identity.outputs.request_id }}
          SOURCE_SHA: ${{ steps.identity.outputs.source_sha }}
          RUNNER_TEMP: ${{ runner.temp }}
        run: |
          set -euo pipefail
          TMP_ROOT="$RUNNER_TEMP/tnr-quest-studio/$REQUEST_ID"
          RESULT_PATH="request/studio/results/$REQUEST_ID.build.json"
          BUILD_PATH="request/studio/builds/$REQUEST_ID"

          REMOTE_SHA="$(git -C request ls-remote origin "refs/heads/$REQUEST_BRANCH" | awk '{print $1}')"
          [[ "$REMOTE_SHA" == "$SOURCE_SHA" ]] || {
            echo "request branch advanced from $SOURCE_SHA to $REMOTE_SHA; refusing to persist stale build evidence" >&2
            exit 5
          }

          rm -rf "$RESULT_PATH" "$BUILD_PATH"
          mkdir -p "$(dirname "$RESULT_PATH")" "$BUILD_PATH"
          cp "$TMP_ROOT/build-result.json" "$RESULT_PATH"
          cp -a "$TMP_ROOT/build/." "$BUILD_PATH/"

          git -C request config user.name "quest-studio[bot]"
          git -C request config user.email "quest-studio@users.noreply.github.com"
          git -C request add -- "studio/results/$REQUEST_ID.build.json" "studio/builds/$REQUEST_ID"

          if git -C request diff --cached --quiet; then
            echo "No generated changes to persist"
          else
            git -C request commit -m "studio: build $REQUEST_ID"
            git -C request push origin "HEAD:$REQUEST_BRANCH"
          fi

      - name: Surface compiler failure after evidence is persisted
        env:
          COMPILE_RC: ${{ steps.compile.outputs.compile_rc }}
        run: |
          set -euo pipefail
          [[ "$COMPILE_RC" == "0" ]] || {
            echo "Quest Studio compiler returned $COMPILE_RC; structured failure result was persisted" >&2
            exit "$COMPILE_RC"
          }
'''

WORKER_TEST = '''#!/usr/bin/env python3
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
    require(text, 'branches:\n      - "studio/quest/**"', "worker is scoped to Studio request branches", failures)
    require(text, 'paths:\n      - "studio/requests/*.quest.json"', "worker triggers only on Quest Source writes", failures)
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
        print(f"\n{len(failures)} contract failures")
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
    print("\nQuest Studio source-push trust boundary pinned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

(ROOT / ".github/workflows/quest_studio.yml").write_text(WORKER, encoding="utf-8")
(ROOT / "skills/building-tnr-content/scripts/quest_worker_contract_test.py").write_text(WORKER_TEST, encoding="utf-8")

# Browser repository adapter: source write is the build request; no Actions dispatch.
p = ROOT / "forge/src/studio/repository.mjs"
replace_once(p, '  workflow: "quest_studio.yml",\n', '')
replace_once(
    p,
    'export function questResultPath(id) { return `${QUEST_STUDIO.resultRoot}/${questRequestId(id)}.build.json`; }\n',
    'export function questResultPath(id) { return `${QUEST_STUDIO.resultRoot}/${questRequestId(id)}.build.json`; }\n\nfunction defaultBuildRequestId() {\n  const uuid = globalThis.crypto?.randomUUID?.();\n  return uuid || `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;\n}\n',
)
replace_once(
    p,
    '  constructor({ github, baseRef = "main" }) {\n    this.github = github;\n    this.baseRef = baseRef;\n  }\n',
    '  constructor({ github, baseRef = "main", buildRequestId = defaultBuildRequestId }) {\n    this.github = github;\n    this.baseRef = baseRef;\n    this.buildRequestId = buildRequestId;\n  }\n',
)
old_submit = '''  /**\n   * Persist a source revision on its dedicated branch and dispatch the trusted repository worker.\n   * The returned sourceCommit is the exact revision the worker must compile.\n   */\n  async submit(source) {\n    source = validateQuestSource(source);\n    const id = source.requestId;\n    const branch = questBranch(id);\n    const sourcePath = questSourcePath(id);\n    await this.github.ensureBranch(branch, this.baseRef);\n    const saved = await this.github.put(\n      sourcePath,\n      JSON.stringify(source, null, 2) + "\\n",\n      `studio: save Quest Source ${id}`,\n      { branch },\n    );\n    if (!saved.commitSha) throw new GithubError("Quest Studio source save returned no commit SHA");\n    await this.dispatch(id, saved.commitSha);\n    return { requestId: id, branch, sourcePath, sourceCommit: saved.commitSha };\n  }\n\n  /** Retry only the build request for an already-saved exact source revision. */\n  async dispatch(requestId, sourceCommit) {\n    const id = questRequestId(requestId);\n    if (typeof sourceCommit !== "string" || !/^[0-9a-f]{40}$/.test(sourceCommit)) throw new GithubError("Quest Studio sourceCommit must be a 40-character lowercase git SHA");\n    await this.github.dispatch(QUEST_STUDIO.workflow, {\n      ref: this.baseRef,\n      inputs: {\n        request_branch: questBranch(id),\n        source_path: questSourcePath(id),\n        request_id: id,\n        source_sha: sourceCommit,\n      },\n    });\n    return { requestId: id, sourceCommit };\n  }\n'''
new_submit = '''  /**\n   * Persist a fresh exact Quest Source revision on its dedicated branch. The source write itself\n   * is the approved build request: quest_studio.yml listens only to studio/requests/*.quest.json\n   * on studio/quest/* branches. No Actions API permission is required in the browser.\n   */\n  async submit(source) {\n    source = validateQuestSource(source);\n    const id = source.requestId;\n    const branch = questBranch(id);\n    const sourcePath = questSourcePath(id);\n    const requestToken = String(this.buildRequestId());\n    if (!requestToken || requestToken.length > 160) throw new GithubError("Quest Studio build request id is invalid");\n    const persistedSource = {\n      ...source,\n      meta: { ...(source.meta && typeof source.meta === "object" ? source.meta : {}), repositoryBuildRequestId: requestToken },\n    };\n    await this.github.ensureBranch(branch, this.baseRef);\n    const saved = await this.github.put(\n      sourcePath,\n      JSON.stringify(persistedSource, null, 2) + "\\n",\n      `studio: request Quest Source build ${id}`,\n      { branch },\n    );\n    if (!saved.commitSha) throw new GithubError("Quest Studio source save returned no commit SHA");\n    return { requestId: id, branch, sourcePath, sourceCommit: saved.commitSha };\n  }\n'''
replace_once(p, old_submit, new_submit)

# GitHub transport no longer exposes an Actions-dispatch primitive to Forge.
p = ROOT / "forge/src/github.mjs"
replace_once(p, 'const DISPATCHABLE_WORKFLOWS = new Set(["quest_studio.yml"]);\n\n', '')
start = p.read_text(encoding="utf-8").find('  /** Dispatch an allowlisted repository workflow; callers choose the workflow/ref explicitly. */')
if start < 0:
    raise SystemExit("Github.dispatch block not found")
text = p.read_text(encoding="utf-8")
end = text.find('\n}\n\nexport function b64utf8', start)
if end < 0:
    raise SystemExit("Github.dispatch block end not found")
text = text[:start] + text[end + 1:]
p.write_text(text, encoding="utf-8")

# Settings reflects the selected least-privilege model.
p = ROOT / "forge/src/ui/screens.mjs"
replace_once(
    p,
    'fine-grained PAT (contents: write + actions: write on tnr-tools only)',
    'fine-grained PAT (Contents: write only on tnr-tools; do not grant Actions or Workflows)',
)

# Repository tests: remove dispatch tests and prove source-push behavior/retry identity.
p = ROOT / "forge/test/github.studio.test.mjs"
replace_test(p, "Github.dispatch sends workflow inputs to GitHub only", "")
replace_test(p, "Github.dispatch allowlists Quest Studio and explains missing Actions permission", "")
replace_test(
    p,
    "QuestStudioRepository writes source to its dedicated branch then dispatches exact commit",
    '''test("QuestStudioRepository writes a fresh source revision that triggers the worker without Actions dispatch", async () => {\n  const log = [];\n  const github = {\n    async ensureBranch(branch, base) { log.push(["branch", branch, base]); return { created: true, sha: "1".repeat(40) }; },\n    async put(path, text, message, opts) { log.push(["put", path, JSON.parse(text), message, opts]); return { commitSha: "2".repeat(40) }; },\n  };\n  const repo = new QuestStudioRepository({ github, buildRequestId: () => "build-request-001" });\n  const source = {\n    schemaVersion: 1,\n    kind: "quest",\n    requestId: "demo-mission",\n    subtype: "mission",\n    content: { rank: "D", name: "Demo" },\n    meta: { authoredIn: "test" },\n  };\n  const submitted = await repo.submit(source);\n  assert.equal(submitted.branch, "studio/quest/demo-mission");\n  assert.equal(submitted.sourcePath, "studio/requests/demo-mission.quest.json");\n  assert.equal(submitted.sourceCommit, "2".repeat(40));\n  assert.deepEqual(log[0], ["branch", "studio/quest/demo-mission", "main"]);\n  assert.equal(log.length, 2);\n  assert.equal(log[1][0], "put");\n  assert.equal(log[1][1], "studio/requests/demo-mission.quest.json");\n  assert.equal(log[1][2].meta.authoredIn, "test");\n  assert.equal(log[1][2].meta.repositoryBuildRequestId, "build-request-001");\n  assert.equal(log[1][4].branch, "studio/quest/demo-mission");\n  assert.equal(source.meta.repositoryBuildRequestId, undefined);\n});\n\ntest("QuestStudioRepository changes repository build-request metadata on every compile request", async () => {\n  const written = [];\n  let n = 0;\n  const github = {\n    async ensureBranch() { return { created: false, sha: "1".repeat(40) }; },\n    async put(_path, text) { written.push(JSON.parse(text)); return { commitSha: String(++n).padStart(40, "0") }; },\n  };\n  const tokens = ["build-a", "build-b"];\n  const repo = new QuestStudioRepository({ github, buildRequestId: () => tokens.shift() });\n  const source = { schemaVersion: 1, kind: "quest", requestId: "demo-retry", subtype: "mission", content: {} };\n  await repo.submit(source);\n  await repo.submit(source);\n  assert.equal(written[0].meta.repositoryBuildRequestId, "build-a");\n  assert.equal(written[1].meta.repositoryBuildRequestId, "build-b");\n  assert.notDeepEqual(written[0], written[1]);\n});''',
)

# Studio CI should rerun when the credential-scope copy changes.
p = ROOT / ".github/workflows/quest_studio_ci.yml"
replace_count(p, '      - "forge/src/ui/dom.mjs"\n', '      - "forge/src/ui/dom.mjs"\n      - "forge/src/ui/screens.mjs"\n', 2)

# Durable director decision in the ledger and architecture owner.
p = ROOT / "docs/RULINGS.md"
ruling_id = "RUL-2026-09-16-001"
text = p.read_text(encoding="utf-8")
if ruling_id not in text:
    text = text.rstrip() + '''\n\n---\n\n## RUL-2026-09-16-001 — Quest Studio repository builds use source-push with Contents-only browser credentials\n\n**Date:** 2026-09-16  \n**Domain:** Forge Next / repository build security  \n**Status:** ACTIVE  \n**Supersedes:** none\n\n**Ruling:** Quest Studio's initial repository build transport uses **source-push** rather than browser `workflow_dispatch`. Forge may hold a fine-grained GitHub credential with **Contents: write only** for `tnr-tools`; Quest Studio must not require Actions or Workflows write permission on the operator device. Pressing Compile persists a fresh exact Quest Source revision on its dedicated `studio/quest/*` branch, and that source write triggers the trusted repository worker. The worker executes compiler code from trusted `main`, treats the request branch as authored data only, and writes generated results back only to that request branch. Compile remains separate from all live-game execution.\n\n**Rationale:** This keeps the one-stop repository-backed Studio workflow while reducing the blast radius of a browser-stored repository credential. A stolen Contents-only token can alter repository content within its granted scope but cannot use Quest Studio's required permission set to dispatch unrelated Actions workflows.\n\n**Canonical destination:** `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`, the accepted Quest Studio implementation contract/handoff, and the eventual unified Forge implementation brief. Branch retention/cleanup and later transport replacement remain engineering decisions.\n'''
    p.write_text(text, encoding="utf-8")

p = ROOT / "docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md"
replace_once(
    p,
    'The exact transport may initially be GitHub Contents + Actions and later become a thinner purpose-built service if that materially improves latency/security. The product contract should depend on the **request/result semantics**, not on a particular transport provider.\n',
    'The product contract depends on the **request/result semantics**, not on a particular transport provider. For the initial Quest Studio implementation, `RUL-2026-09-16-001` fixes the transport to **GitHub Contents source-push**: Compile writes a fresh exact Quest Source revision to a dedicated `studio/quest/*` branch, that source write triggers the trusted repository worker, and the browser credential is limited to **Contents: write** rather than Actions/Workflows write. A later purpose-built service may replace that transport if it materially improves latency/security without changing the Studio request/result contract.\n',
)

print("Quest Studio source-push correction applied")
