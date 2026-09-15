#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one replacement, found {count}\n--- OLD ---\n{old}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def append_once(path: str, marker: str, addition: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if addition.strip() in text:
        return
    if marker not in text:
        raise SystemExit(f"{path}: append marker not found")
    p.write_text(text.replace(marker, marker + addition), encoding="utf-8")

# M3: bind the generated manifest bytes to the build envelope.
replace_once(
    "skills/building-tnr-content/scripts/quest_compile.py",
    '''    manifest_path.write_text(\n        json.dumps(manifest, ensure_ascii=False, indent=2) + "\\n",\n        encoding="utf-8",\n    )\n\n    valid, validation_output = run_manifest_validation(manifest_path)\n''',
    '''    manifest_path.write_text(\n        json.dumps(manifest, ensure_ascii=False, indent=2) + "\\n",\n        encoding="utf-8",\n    )\n    manifest_sha256 = hashlib.sha256(manifest_path.read_bytes()).hexdigest()\n\n    valid, validation_output = run_manifest_validation(manifest_path)\n''',
)
replace_once(
    "skills/building-tnr-content/scripts/quest_compile.py",
    '''            "manifestPath": f"{artifact_prefix}/manifest.json",\n            "entities": entity_summary(manifest),\n''',
    '''            "manifestPath": f"{artifact_prefix}/manifest.json",\n            "manifestSha256": manifest_sha256,\n            "entities": entity_summary(manifest),\n''',
)

# M3 + m6: verify manifest bytes and fail closed when result identity is not supplied.
replace_once(
    "forge/src/studio/repository.mjs",
    '''function generatedArtifactPath(path, requestId) {\n  const id = questRequestId(requestId);\n  const prefix = `${QUEST_STUDIO.buildRoot}/${id}/`;\n  if (typeof path !== "string" || !path.startsWith(prefix) || !path.endsWith(".json")) {\n    throw new GithubError("Quest Studio result does not contain a safe generated manifest path");\n  }\n  const tail = path.slice(prefix.length);\n  const segments = tail.split("/");\n  if (!tail || /[%?#]/.test(tail) || path.includes("\\\\") || segments.some((segment) => !segment || segment === "." || segment === "..")) {\n    throw new GithubError("Quest Studio generated manifest path escapes its request build directory");\n  }\n  return path;\n}\n''',
    '''function generatedArtifactPath(path, requestId) {\n  const id = questRequestId(requestId);\n  const prefix = `${QUEST_STUDIO.buildRoot}/${id}/`;\n  if (typeof path !== "string" || !path.startsWith(prefix) || !path.endsWith(".json")) {\n    throw new GithubError("Quest Studio result does not contain a safe generated manifest path");\n  }\n  const tail = path.slice(prefix.length);\n  const segments = tail.split("/");\n  if (!tail || /[%?#]/.test(tail) || path.includes("\\\\") || segments.some((segment) => !segment || segment === "." || segment === "..")) {\n    throw new GithubError("Quest Studio generated manifest path escapes its request build directory");\n  }\n  return path;\n}\n\nasync function sha256Hex(text) {\n  if (!globalThis.crypto?.subtle) throw new GithubError("SHA-256 verification is unavailable in this browser context");\n  const digest = await globalThis.crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));\n  return [...new Uint8Array(digest)].map((x) => x.toString(16).padStart(2, "0")).join("");\n}\n''',
)
replace_once(
    "forge/src/studio/repository.mjs",
    '''  async buildResult(requestId, { expectedSourceCommit = null } = {}) {\n    const id = questRequestId(requestId);\n    let result;\n''',
    '''  async buildResult(requestId, { expectedSourceCommit = null } = {}) {\n    const id = questRequestId(requestId);\n    if (typeof expectedSourceCommit !== "string" || !/^[0-9a-f]{40}$/.test(expectedSourceCommit)) {\n      throw new GithubError("Quest Studio buildResult requires the exact submitted source commit");\n    }\n    let result;\n''',
)
replace_once(
    "forge/src/studio/repository.mjs",
    '''    const actual = result.provenance?.sourceRevision ?? null;\n    return { result, stale: !!expectedSourceCommit && actual !== expectedSourceCommit };\n  }\n\n  async generatedManifest(requestId, buildResult) {\n    const id = questRequestId(requestId);\n    const result = validateBuildResult(buildResult, id);\n    const path = generatedArtifactPath(result.generated?.manifestPath, id);\n    return this.github.text(path, questBranch(id));\n  }\n''',
    '''    const actual = result.provenance?.sourceRevision ?? null;\n    return { result, stale: actual !== expectedSourceCommit };\n  }\n\n  async generatedManifest(requestId, buildResult) {\n    const id = questRequestId(requestId);\n    const result = validateBuildResult(buildResult, id);\n    const path = generatedArtifactPath(result.generated?.manifestPath, id);\n    const expected = result.generated?.manifestSha256;\n    if (typeof expected !== "string" || !/^[0-9a-f]{64}$/.test(expected)) {\n      throw new GithubError("Quest Studio result does not contain a valid generated manifest SHA-256");\n    }\n    const text = await this.github.text(path, questBranch(id));\n    const actual = await sha256Hex(text);\n    if (actual !== expected) throw new GithubError("Quest Studio generated manifest does not match the compiler result digest");\n    return text;\n  }\n''',
)

# M4: any authored edit invalidates the persisted submitted-build identity.
replace_once(
    "forge/src/studio/ui.mjs",
    '''  saveDraft() { writeDraft(this.app.storage, this.draft, this.app.now ? this.app.now() : Date.now()); }\n''',
    '''  saveDraft({ preserveBuild = false } = {}) {\n    if (!preserveBuild && this.draft) {\n      this.draft.sourceCommit = null;\n      this.draft.lastResult = null;\n      this.buildState = null;\n    }\n    writeDraft(this.app.storage, this.draft, this.app.now ? this.app.now() : Date.now());\n  }\n''',
)
replace_once(
    "forge/src/studio/ui.mjs",
    '''      this.draft.sourceCommit = submitted.sourceCommit;\n      this.draft.lastResult = null;\n      this.saveDraft();\n''',
    '''      this.draft.sourceCommit = submitted.sourceCommit;\n      this.draft.lastResult = null;\n      this.saveDraft({ preserveBuild: true });\n''',
)
replace_once(
    "forge/src/studio/ui.mjs",
    '''        this.draft.lastResult = got.result;\n        this.saveDraft();\n''',
    '''        this.draft.lastResult = got.result;\n        this.saveDraft({ preserveBuild: true });\n''',
)

# m1: make the shell-interpolation gate cover all run scalar forms and both Actions input spellings.
replace_once(
    "skills/building-tnr-content/scripts/quest_worker_contract_test.py",
    '''def multiline_run_text(text: str) -> str:\n    lines = text.splitlines()\n    out: list[str] = []\n    for i, line in enumerate(lines):\n        match = re.match(r"^(\\s*)run:\\s*[|>][+-]?\\s*$", line)\n        if not match:\n            continue\n        indent = len(match.group(1))\n        for body in lines[i + 1:]:\n            if body.strip() and len(body) - len(body.lstrip()) <= indent:\n                break\n            out.append(body)\n    return "\\n".join(out)\n''',
    '''def run_script_text(text: str) -> str:\n    lines = text.splitlines()\n    out: list[str] = []\n    for i, line in enumerate(lines):\n        match = re.match(r"^(\\s*)run:\\s*(.*)$", line)\n        if not match:\n            continue\n        indent = len(match.group(1))\n        scalar = match.group(2).strip()\n        if re.fullmatch(r"[|>][+-]?", scalar):\n            for body in lines[i + 1:]:\n                if body.strip() and len(body) - len(body.lstrip()) <= indent:\n                    break\n                out.append(body)\n        elif scalar:\n            out.append(scalar)\n    return "\\n".join(out)\n''',
)
replace_once(
    "skills/building-tnr-content/scripts/quest_worker_contract_test.py",
    '''    run_text = multiline_run_text(text)\n    forbid(run_text, "${{ inputs.", "untrusted workflow inputs are not interpolated into shell", failures)\n''',
    '''    run_text = run_script_text(text)\n    if re.search(r"\\$\\{\\{\\s*(?:github\\.event\\.)?inputs\\.", run_text):\n        failures.append("untrusted workflow inputs are not interpolated into shell")\n''',
)

# M3 integration proof: the digest in the envelope must bind the bytes actually written.
replace_once(
    "skills/building-tnr-content/scripts/quest_compile_integration_test.py",
    '''import json\nfrom pathlib import Path\n''',
    '''import hashlib\nimport json\nfrom pathlib import Path\n''',
)
replace_once(
    "skills/building-tnr-content/scripts/quest_compile_integration_test.py",
    '''        manifest = root / "build" / "manifest.json"\n        if not manifest.is_file():\n            raise SystemExit("Mission adapter did not materialize manifest.json")\n        payload = json.loads(manifest.read_text(encoding="utf-8"))\n''',
    '''        manifest = root / "build" / "manifest.json"\n        if not manifest.is_file():\n            raise SystemExit("Mission adapter did not materialize manifest.json")\n        expected_manifest_hash = hashlib.sha256(manifest.read_bytes()).hexdigest()\n        if result.get("generated", {}).get("manifestSha256") != expected_manifest_hash:\n            raise SystemExit("generated manifest digest does not bind manifest.json bytes")\n        payload = json.loads(manifest.read_text(encoding="utf-8"))\n''',
)
replace_once(
    "skills/building-tnr-content/scripts/quest_compile_integration_test.py",
    '''        print("PASS  provenance and live-game boundary are preserved")\n''',
    '''        print("PASS  provenance, manifest digest, and live-game boundary are preserved")\n''',
)

# Repository-side manifest verification and fail-closed stale detection regressions.
replace_once(
    "forge/test/github.studio.test.mjs",
    '''  const ok = { ...base, generated: { manifestPath: "studio/builds/demo-mission/manifest.json" } };\n  await repo.generatedManifest("demo-mission", ok);\n  assert.equal(reads, 1);\n});\n''',
    '''  const ok = { ...base, generated: {\n    manifestPath: "studio/builds/demo-mission/manifest.json",\n    manifestSha256: "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",\n  } };\n  await repo.generatedManifest("demo-mission", ok);\n  assert.equal(reads, 1);\n\n  await assert.rejects(() => repo.generatedManifest("demo-mission", {\n    ...base,\n    generated: {\n      manifestPath: "studio/builds/demo-mission/manifest.json",\n      manifestSha256: "0".repeat(64),\n    },\n  }), /does not match the compiler result digest/);\n  assert.equal(reads, 2);\n});\n''',
)
append_once(
    "forge/test/github.studio.test.mjs",
    '''test("QuestStudioRepository marks an older persisted result stale", async () => {\n''',
    '''\ntest("QuestStudioRepository refuses build reads without an exact submitted source identity", async () => {\n  const repo = new QuestStudioRepository({ github: { async json() { throw new Error("must not read"); } } });\n  await assert.rejects(() => repo.buildResult("demo-mission"), /requires the exact submitted source commit/);\n});\n\n''',
)

# UI regression: compile identity must not survive an authored edit or browser reopen.
append_once(
    "forge/test/quest.studio.ui.test.mjs",
    '''test("real Mission profile sentinels render as awaiting ruling and block compile", async () => {\n''',
    '''\ntest("editing a submitted Mission invalidates persisted build identity before reopen", async () => {\n  const win = setupDom();\n  const storage = new MemoryStorage();\n  const app = fakeApp(win, storage);\n  const result = {\n    schemaVersion: 1, kind: "quest-build", requestId: "quest-edit-stale", subtype: "mission",\n    status: "valid", blockers: [], errors: [], warnings: [],\n    generated: { manifestPath: "studio/builds/quest-edit-stale/manifest.json", entities: { counts: { quest: 1 } } },\n    provenance: { sourceRevision: "a".repeat(40), compilerRevision: "b".repeat(40) },\n    liveGameTouched: false,\n  };\n  const repository = repositoryStub({ result });\n  const studio = new QuestStudioWorkspace({ app, repository, pollMs: 0, maxPolls: 1 }).install();\n  await studio.open();\n  studio.draft = {\n    version: 1, requestId: "quest-edit-stale", subtype: "mission", profile: "D",\n    name: "Before edit", description: "Carry the note.", successDescription: "Delivered.",\n    beats: [\n      { description: "Accept it.", choiceText: "Take it" },\n      { description: "Check it.", choiceText: "Continue" },\n      { description: "Deliver it.", choiceText: "Deliver" },\n    ],\n    updatedAt: new Date().toISOString(), sourceCommit: null, lastResult: null,\n  };\n  await studio.openMission(false);\n  await studio.compileMission();\n  assert.equal(studio.draft.sourceCommit, "a".repeat(40));\n\n  const name = studio.shell.querySelector('input[type="text"]');\n  name.value = "After edit";\n  name.dispatchEvent(new win.Event("input", { bubbles: true }));\n  assert.equal(studio.draft.sourceCommit, null);\n  assert.equal(studio.draft.lastResult, null);\n\n  const resultCalls = repository.calls.filter((x) => x[0] === "result").length;\n  const reopened = new QuestStudioWorkspace({ app: fakeApp(win, storage), repository, pollMs: 0, maxPolls: 1 }).install();\n  assert.equal(reopened.draft.sourceCommit, null);\n  await reopened.open();\n  await reopened.openMission(false);\n  assert.equal(repository.calls.filter((x) => x[0] === "result").length, resultCalls);\n  assert.match(reopened.shell.textContent, /No repository build has been requested for the current draft revision/);\n});\n\n''',
)

print("Quest Studio follow-up patch applied")
