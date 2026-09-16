#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one replacement, found {count}: {old[:80]!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def replace_count(path: Path, old: str, new: str, expected: int) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"{path}: expected {expected} replacements, found {count}: {old[:80]!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


# M3: bind the generated manifest bytes to the build result.
p = ROOT / "skills/building-tnr-content/scripts/quest_compile.py"
replace_once(
    p,
    '''    manifest_path.write_text(\n        json.dumps(manifest, ensure_ascii=False, indent=2) + "\\n",\n        encoding="utf-8",\n    )\n\n    valid, validation_output = run_manifest_validation(manifest_path)\n''',
    '''    manifest_path.write_text(\n        json.dumps(manifest, ensure_ascii=False, indent=2) + "\\n",\n        encoding="utf-8",\n    )\n    manifest_sha256 = hashlib.sha256(manifest_path.read_bytes()).hexdigest()\n\n    valid, validation_output = run_manifest_validation(manifest_path)\n''',
)
replace_once(
    p,
    '''            "manifestPath": f"{artifact_prefix}/manifest.json",\n            "entities": entity_summary(manifest),\n''',
    '''            "manifestPath": f"{artifact_prefix}/manifest.json",\n            "manifestSha256": manifest_sha256,\n            "entities": entity_summary(manifest),\n''',
)

p = ROOT / "skills/building-tnr-content/scripts/quest_compile_integration_test.py"
replace_once(p, "import json\n", "import hashlib\nimport json\n")
replace_once(
    p,
    '''        manifest = root / "build" / "manifest.json"\n        if not manifest.is_file():\n            raise SystemExit("Mission adapter did not materialize manifest.json")\n        payload = json.loads(manifest.read_text(encoding="utf-8"))\n''',
    '''        manifest = root / "build" / "manifest.json"\n        if not manifest.is_file():\n            raise SystemExit("Mission adapter did not materialize manifest.json")\n        manifest_sha256 = hashlib.sha256(manifest.read_bytes()).hexdigest()\n        if result.get("generated", {}).get("manifestSha256") != manifest_sha256:\n            raise SystemExit("build result does not bind the generated manifest bytes")\n        payload = json.loads(manifest.read_text(encoding="utf-8"))\n''',
)
replace_once(
    p,
    '        print("PASS  provenance and live-game boundary are preserved")\n',
    '        print("PASS  provenance, manifest digest and live-game boundary are preserved")\n',
)

p = ROOT / "forge/src/studio/repository.mjs"
replace_once(
    p,
    '''  if (result.liveGameTouched !== false) throw new GithubError("Quest Studio repository build must state liveGameTouched:false");\n  return result;\n}\n\nfunction generatedArtifactPath(path, requestId) {\n''',
    '''  if (result.liveGameTouched !== false) throw new GithubError("Quest Studio repository build must state liveGameTouched:false");\n  if (result.status === "valid" && !/^[0-9a-f]{64}$/.test(result.generated?.manifestSha256 || "")) {\n    throw new GithubError("Quest Studio valid build result must carry generated.manifestSha256");\n  }\n  return result;\n}\n\nasync function sha256Hex(text) {\n  const subtle = globalThis.crypto?.subtle;\n  if (!subtle) throw new GithubError("Quest Studio SHA-256 verification is unavailable in this browser");\n  const digest = await subtle.digest("SHA-256", new TextEncoder().encode(text));\n  return [...new Uint8Array(digest)].map((x) => x.toString(16).padStart(2, "0")).join("");\n}\n\nfunction generatedArtifactPath(path, requestId) {\n''',
)
replace_once(
    p,
    '''    const actual = result.provenance?.sourceRevision ?? null;\n    return { result, stale: !!expectedSourceCommit && actual !== expectedSourceCommit };\n''',
    '''    const actual = result.provenance?.sourceRevision ?? null;\n    return { result, stale: !expectedSourceCommit || actual !== expectedSourceCommit };\n''',
)
replace_once(
    p,
    '''    const result = validateBuildResult(buildResult, id);\n    const path = generatedArtifactPath(result.generated?.manifestPath, id);\n    return this.github.text(path, questBranch(id));\n''',
    '''    const result = validateBuildResult(buildResult, id);\n    const path = generatedArtifactPath(result.generated?.manifestPath, id);\n    const text = await this.github.text(path, questBranch(id));\n    const actual = await sha256Hex(text);\n    if (actual !== result.generated.manifestSha256) {\n      throw new GithubError("Quest Studio generated manifest digest does not match the build result");\n    }\n    return text;\n''',
)

p = ROOT / "forge/test/github.studio.test.mjs"
replace_once(
    p,
    'import assert from "node:assert/strict";\n\n',
    'import assert from "node:assert/strict";\nimport { createHash } from "node:crypto";\n\n',
)
replace_once(
    p,
    '''function jsonResponse(value, status = 200) {\n  return new Response(JSON.stringify(value), { status, headers: { "content-type": "application/json" } });\n}\n''',
    '''function jsonResponse(value, status = 200) {\n  return new Response(JSON.stringify(value), { status, headers: { "content-type": "application/json" } });\n}\n\nfunction sha256(text) { return createHash("sha256").update(text).digest("hex"); }\n''',
)
replace_once(
    p,
    '''test("QuestStudioRepository marks an older persisted result stale", async () => {\n''',
    '''test("QuestStudioRepository fails staleness closed when no expected source commit is supplied", async () => {\n  const result = {\n    schemaVersion: 1, kind: "quest-build", requestId: "demo-mission", subtype: "mission",\n    status: "blocked", liveGameTouched: false, provenance: { sourceRevision: "3".repeat(40) },\n  };\n  const github = { async json() { return result; } };\n  const repo = new QuestStudioRepository({ github });\n  const got = await repo.buildResult("demo-mission");\n  assert.equal(got.stale, true);\n});\n\ntest("QuestStudioRepository marks an older persisted result stale", async () => {\n''',
)
replace_once(
    p,
    '''    generated: {},\n  };\n''',
    '''    generated: { manifestSha256: sha256("{}") },\n  };\n''',
)
replace_count(
    p,
    'generated: { manifestPath: path }',
    'generated: { ...base.generated, manifestPath: path }',
    1,
)
replace_once(
    p,
    '''  const ok = { ...base, generated: { manifestPath: "studio/builds/demo-mission/manifest.json" } };\n  await repo.generatedManifest("demo-mission", ok);\n  assert.equal(reads, 1);\n});\n''',
    '''  const ok = { ...base, generated: { ...base.generated, manifestPath: "studio/builds/demo-mission/manifest.json" } };\n  await repo.generatedManifest("demo-mission", ok);\n  assert.equal(reads, 1);\n\n  const tampered = new QuestStudioRepository({ github: { async text() { return '{"tampered":true}'; } } });\n  await assert.rejects(() => tampered.generatedManifest("demo-mission", ok), /digest does not match/);\n});\n''',
)

# M4: any edit invalidates the submitted-source identity before it is persisted.
p = ROOT / "forge/src/studio/ui.mjs"
replace_once(
    p,
    '''  saveDraft() { writeDraft(this.app.storage, this.draft, this.app.now ? this.app.now() : Date.now()); }\n\n  chooseProfile(key) {\n''',
    '''  saveDraft() { writeDraft(this.app.storage, this.draft, this.app.now ? this.app.now() : Date.now()); }\n\n  markDraftDirty() {\n    this.pollToken++;\n    this.draft.sourceCommit = null;\n    this.draft.lastResult = null;\n    this.buildState = null;\n    this.saveDraft();\n  }\n\n  chooseProfile(key) {\n''',
)
replace_count(
    p,
    '''this.buildState = null; this.saveDraft();''',
    '''this.markDraftDirty();''',
    7,
)
replace_once(
    p,
    '''    this.buildState = null;\n    this.saveDraft();\n    this.renderMission();\n''',
    '''    this.markDraftDirty();\n    this.renderMission();\n''',
)
replace_once(
    p,
    '''      this.buildState = null;\n      this.saveDraft();\n      this.renderMission();\n''',
    '''      this.markDraftDirty();\n      this.renderMission();\n''',
)
replace_once(
    p,
    '''      this.pollToken++;\n      this.draft = newMissionDraft(this.app.now ? this.app.now() : Date.now());\n      this.buildState = null;\n      this.saveDraft();\n      this.renderMission();\n''',
    '''      this.draft = newMissionDraft(this.app.now ? this.app.now() : Date.now());\n      this.markDraftDirty();\n      this.renderMission();\n''',
)

p = ROOT / "forge/test/quest.studio.ui.test.mjs"
insert = '''\ntest("editing a submitted draft clears persisted build identity before reopen", async () => {\n  const win = setupDom();\n  const storage = new MemoryStorage();\n  const app = fakeApp(win, storage);\n  const repository = repositoryStub();\n  const studio = new QuestStudioWorkspace({ app, repository, pollMs: 0, maxPolls: 1 }).install();\n  await studio.open();\n  studio.draft = {\n    version: 1, requestId: "quest-dirty", subtype: "mission", profile: "D",\n    name: "Compiled title", description: "Carry the note.", successDescription: "Delivered.",\n    beats: [\n      { description: "Accept it.", choiceText: "Take it" },\n      { description: "Check the address.", choiceText: "Continue" },\n      { description: "Deliver it.", choiceText: "Deliver" },\n    ],\n    updatedAt: new Date().toISOString(), sourceCommit: null, lastResult: null,\n  };\n  await studio.openMission(false);\n  studio.draft.sourceCommit = "a".repeat(40);\n  studio.draft.lastResult = { status: "valid" };\n  studio.saveDraft();\n  studio.renderMission();\n\n  const nameField = [...studio.shell.querySelectorAll(".qs-field")].find((x) => x.querySelector("span")?.textContent === "Mission name");\n  const input = nameField.querySelector("input");\n  input.value = "Edited title";\n  input.dispatchEvent(new win.Event("input", { bubbles: true }));\n\n  assert.equal(studio.draft.sourceCommit, null);\n  assert.equal(studio.draft.lastResult, null);\n  const persisted = JSON.parse(storage.getItem("tnr_forge_quest_studio_draft_v1"));\n  assert.equal(persisted.sourceCommit, null);\n  assert.equal(persisted.lastResult, null);\n\n  const app2 = fakeApp(win, storage);\n  const repository2 = repositoryStub();\n  const reopened = new QuestStudioWorkspace({ app: app2, repository: repository2, pollMs: 0, maxPolls: 1 }).install();\n  await reopened.open();\n  await reopened.openMission(false);\n  assert.equal(repository2.calls.filter((x) => x[0] === "result").length, 0);\n  assert.match(reopened.shell.textContent, /No repository build has been requested for the current draft revision/);\n});\n'''
replace_once(
    p,
    '''\ntest("DOM helper rejects HTML string sinks even through property coercion", () => {\n''',
    insert + '''\ntest("DOM helper rejects HTML string sinks even through property coercion", () => {\n''',
)

# Minor m1: make the workflow-shell regression test cover single-line/folded run and both input spellings.
p = ROOT / "skills/building-tnr-content/scripts/quest_worker_contract_test.py"
replace_once(
    p,
    '''def multiline_run_text(text: str) -> str:\n    lines = text.splitlines()\n    out: list[str] = []\n    for i, line in enumerate(lines):\n        match = re.match(r"^(\\s*)run:\\s*[|>][+-]?\\s*$", line)\n        if not match:\n            continue\n        indent = len(match.group(1))\n        for body in lines[i + 1:]:\n            if body.strip() and len(body) - len(body.lstrip()) <= indent:\n                break\n            out.append(body)\n    return "\\n".join(out)\n''',
    '''def workflow_run_text(text: str) -> str:\n    lines = text.splitlines()\n    out: list[str] = []\n    for i, line in enumerate(lines):\n        match = re.match(r"^(\\s*)run:\\s*(.*?)\\s*$", line)\n        if not match:\n            continue\n        indent = len(match.group(1))\n        value = match.group(2)\n        if value and not re.fullmatch(r"[|>][+-]?", value):\n            out.append(value)\n            continue\n        for body in lines[i + 1:]:\n            if body.strip() and len(body) - len(body.lstrip()) <= indent:\n                break\n            out.append(body)\n    return "\\n".join(out)\n''',
)
replace_once(
    p,
    '''    run_text = multiline_run_text(text)\n    forbid(run_text, "${{ inputs.", "untrusted workflow inputs are not interpolated into shell", failures)\n''',
    '''    run_text = workflow_run_text(text)\n    forbid(run_text, "${{ inputs.", "untrusted workflow inputs are not interpolated into shell", failures)\n    forbid(run_text, "${{ github.event.inputs.", "legacy workflow input expressions are not interpolated into shell", failures)\n''',
)
replace_once(p, "    checks = 26\n", "    checks = 27\n")

print("Quest Studio follow-up patch applied")
