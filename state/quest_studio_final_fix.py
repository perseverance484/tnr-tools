#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{path}: expected one replacement, found {n}")
    p.write_text(text.replace(old, new), encoding="utf-8")

# F1: unnest exact-source-identity test.
replace_once(
    "forge/test/github.studio.test.mjs",
    '''test("QuestStudioRepository marks an older persisted result stale", async () => {\n\ntest("QuestStudioRepository refuses build reads without an exact submitted source identity", async () => {\n  const repo = new QuestStudioRepository({ github: { async json() { throw new Error("must not read"); } } });\n  await assert.rejects(() => repo.buildResult("demo-mission"), /requires the exact submitted source commit/);\n});\n\n  const result = {''',
    '''test("QuestStudioRepository refuses build reads without an exact submitted source identity", async () => {\n  const repo = new QuestStudioRepository({ github: { async json() { throw new Error("must not read"); } } });\n  await assert.rejects(() => repo.buildResult("demo-mission"), /requires the exact submitted source commit/);\n});\n\ntest("QuestStudioRepository marks an older persisted result stale", async () => {\n  const result = {''',
)

# F1: unnest edited-draft identity invalidation test.
replace_once(
    "forge/test/quest.studio.ui.test.mjs",
    '''test("real Mission profile sentinels render as awaiting ruling and block compile", async () => {\n\ntest("editing a submitted Mission invalidates persisted build identity before reopen", async () => {''',
    '''test("editing a submitted Mission invalidates persisted build identity before reopen", async () => {''',
)
replace_once(
    "forge/test/quest.studio.ui.test.mjs",
    '''  assert.match(reopened.shell.textContent, /No repository build has been requested for the current draft revision/);\n});\n\n  const profiles = JSON.parse(readFileSync(join(REPO, "skills/building-tnr-content/data/48_DATA_mission_profiles.json"), "utf8"));''',
    '''  assert.match(reopened.shell.textContent, /No repository build has been requested for the current draft revision/);\n});\n\ntest("real Mission profile sentinels render as awaiting ruling and block compile", async () => {\n  const profiles = JSON.parse(readFileSync(join(REPO, "skills/building-tnr-content/data/48_DATA_mission_profiles.json"), "utf8"));''',
)

# F2: make the Workflows-write prohibition an explicit durable invariant.
replace_once(
    "docs/RULINGS.md",
    '''**Rationale:** This keeps the one-stop repository-backed Studio workflow while reducing the blast radius of a browser-stored repository credential. A stolen Contents-only token can alter repository content within its granted scope but cannot use Quest Studio's required permission set to dispatch unrelated Actions workflows.\n''',
    '''**Rationale:** This keeps the one-stop repository-backed Studio workflow while reducing the blast radius of a browser-stored repository credential. A stolen Contents-only token can alter repository content within its granted scope but cannot use Quest Studio's required permission set to dispatch unrelated Actions workflows. **Security invariant:** the browser credential must never hold GitHub Workflows write permission, because push-triggered workflow definitions are resolved from the pushed request ref; granting Workflows write would allow that credential to replace the worker definition on a request branch and defeat the trusted-main compiler boundary.\n''',
)
replace_once(
    "docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md",
    '''The product contract depends on the **request/result semantics**, not on a particular transport provider. For the initial Quest Studio implementation, `RUL-2026-09-16-002` fixes the transport to **GitHub Contents source-push**: Compile writes a fresh exact Quest Source revision to a dedicated `studio/quest/*` branch, that source write triggers the trusted repository worker, and the browser credential is limited to **Contents: write** rather than Actions/Workflows write. A later purpose-built service may replace that transport if it materially improves latency/security without changing the Studio request/result contract.\n''',
    '''The product contract depends on the **request/result semantics**, not on a particular transport provider. For the initial Quest Studio implementation, `RUL-2026-09-16-002` fixes the transport to **GitHub Contents source-push**: Compile writes a fresh exact Quest Source revision to a dedicated `studio/quest/*` branch, that source write triggers the trusted repository worker, and the browser credential is limited to **Contents: write** rather than Actions/Workflows write. **Credential invariant:** the browser credential must never be granted GitHub Workflows write permission. Push-triggered workflow definitions are resolved from the pushed request ref, so Workflows write on the browser credential would allow replacement of the request branch's worker definition and collapse the trusted-main execution boundary. The worker therefore also compares its pushed-ref workflow definition against trusted `main` and fails closed on drift as defence in depth. A later purpose-built service may replace that transport if it materially improves latency/security without changing the Studio request/result contract.\n''',
)

# F2/F5 permanent worker candidate. This is tested here but committed separately by connector.
p = ROOT / ".github/workflows/quest_studio.yml"
text = p.read_text(encoding="utf-8")
old = '''      - name: Resolve trusted compiler revision\n        id: compiler\n        run: echo "compiler_sha=$(git -C tools rev-parse HEAD)" >> "$GITHUB_OUTPUT"\n\n      - name: Validate push identity\n'''
new = '''      - name: Resolve trusted compiler revision\n        id: compiler\n        run: echo "compiler_sha=$(git -C tools rev-parse HEAD)" >> "$GITHUB_OUTPUT"\n\n      - name: Checkout pushed worker definition\n        uses: actions/checkout@v4\n        with:\n          ref: ${{ github.sha }}\n          path: request-definition\n          fetch-depth: 1\n          persist-credentials: false\n\n      - name: Verify worker definition matches trusted main\n        run: |\n          set -euo pipefail\n          cmp --silent request-definition/.github/workflows/quest_studio.yml tools/.github/workflows/quest_studio.yml || {\n            echo "request-branch Quest Studio worker differs from trusted main; refusing to compile" >&2\n            exit 2\n          }\n\n      - name: Validate push identity\n'''
if text.count(old) != 1:
    raise SystemExit("workflow trusted-worker insertion point mismatch")
text = text.replace(old, new)
old = '''      - name: Persist build result to request branch\n        env:\n          REQUEST_BRANCH: ${{ steps.identity.outputs.request_branch }}\n          REQUEST_ID: ${{ steps.identity.outputs.request_id }}\n          SOURCE_SHA: ${{ steps.identity.outputs.source_sha }}\n          RUNNER_TEMP: ${{ runner.temp }}\n        run: |\n          set -euo pipefail\n          TMP_ROOT="$RUNNER_TEMP/tnr-quest-studio/$REQUEST_ID"\n          RESULT_PATH="request/studio/results/$REQUEST_ID.build.json"\n          BUILD_PATH="request/studio/builds/$REQUEST_ID"\n\n          REMOTE_SHA='''
new = '''      - name: Persist build result to request branch\n        if: ${{ always() && steps.identity.outcome == 'success' }}\n        env:\n          REQUEST_BRANCH: ${{ steps.identity.outputs.request_branch }}\n          REQUEST_ID: ${{ steps.identity.outputs.request_id }}\n          SOURCE_SHA: ${{ steps.identity.outputs.source_sha }}\n          COMPILER_SHA: ${{ steps.compiler.outputs.compiler_sha }}\n          RUNNER_TEMP: ${{ runner.temp }}\n        run: |\n          set -euo pipefail\n          TMP_ROOT="$RUNNER_TEMP/tnr-quest-studio/$REQUEST_ID"\n          RESULT_PATH="request/studio/results/$REQUEST_ID.build.json"\n          BUILD_PATH="request/studio/builds/$REQUEST_ID"\n\n          if [[ ! -f "$TMP_ROOT/build-result.json" ]]; then\n            mkdir -p "$TMP_ROOT/build"\n            python3 - "$TMP_ROOT/build-result.json" "$REQUEST_ID" "$SOURCE_SHA" "$COMPILER_SHA" <<'PY'\n          import json\n          from pathlib import Path\n          import sys\n          result_path, request_id, source_sha, compiler_sha = sys.argv[1:]\n          result = {\n              "schemaVersion": 1, "kind": "quest-build", "requestId": request_id,\n              "subtype": None, "status": "failed", "resolvedEngineType": None,\n              "blockers": [],\n              "errors": [{"code": "compiler_no_result", "message": "Quest Studio compiler step produced no structured result"}],\n              "warnings": [], "generated": {}, "art": None, "validation": None,\n              "provenance": {\n                  "sourceSha256": None, "sourceRevision": source_sha,\n                  "compilerRevision": compiler_sha, "registrySchemaVersion": None,\n                  "compiler": "skills/building-tnr-content/scripts/quest_compile.py",\n              },\n              "liveGameTouched": False,\n          }\n          Path(result_path).write_text(json.dumps(result, indent=2) + "\\n", encoding="utf-8")\n          PY\n          fi\n\n          REMOTE_SHA='''
if text.count(old) != 1:
    raise SystemExit("workflow persist insertion point mismatch")
text = text.replace(old, new)
old = '''      - name: Surface compiler failure after evidence is persisted\n        env:\n          COMPILE_RC: ${{ steps.compile.outputs.compile_rc }}\n        run: |\n          set -euo pipefail\n          [[ "$COMPILE_RC" == "0" ]] || {\n            echo "Quest Studio compiler returned $COMPILE_RC; structured failure result was persisted" >&2\n            exit "$COMPILE_RC"\n          }\n'''
new = '''      - name: Surface compiler failure after evidence is persisted\n        if: ${{ always() && steps.identity.outcome == 'success' }}\n        env:\n          COMPILE_RC: ${{ steps.compile.outputs.compile_rc }}\n        run: |\n          set -euo pipefail\n          RC="${COMPILE_RC:-4}"\n          [[ "$RC" == "0" ]] || {\n            echo "Quest Studio compiler returned $RC; structured failure result was persisted" >&2\n            exit "$RC"\n          }\n'''
if text.count(old) != 1:
    raise SystemExit("workflow final failure step mismatch")
text = text.replace(old, new)
p.write_text(text, encoding="utf-8")

# Pin the new worker invariants in the contract test.
p = ROOT / "skills/building-tnr-content/scripts/quest_worker_contract_test.py"
text = p.read_text(encoding="utf-8")
needle = '''    require(text, "git -C tools rev-parse HEAD", "compiler revision is measured from trusted checkout", failures)\n'''
addition = needle + '''    require(text, "name: Verify worker definition matches trusted main", "request worker definition is compared with trusted main", failures)\n    require(text, "cmp --silent request-definition/.github/workflows/quest_studio.yml tools/.github/workflows/quest_studio.yml", "worker drift comparison fails closed", failures)\n'''
if text.count(needle) != 1:
    raise SystemExit("worker contract insertion point mismatch")
text = text.replace(needle, addition)
needle = '''    require(text, '[[ "$REMOTE_SHA" == "$SOURCE_SHA" ]]', "stale source result is refused before persistence", failures)\n'''
addition = needle + '''    require(text, "if: ${{ always() && steps.identity.outcome == 'success' }}", "terminal compile failures still reach structured persistence", failures)\n    require(text, '"code": "compiler_no_result"', "missing compiler result gets a structured failure envelope", failures)\n'''
if text.count(needle) != 1:
    raise SystemExit("worker persistence contract insertion point mismatch")
text = text.replace(needle, addition)
p.write_text(text, encoding="utf-8")

print("final Quest Studio correction applied")
