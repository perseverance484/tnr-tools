#!/usr/bin/env python3
from pathlib import Path

def replace(path, old, new, expected=1):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"{path}: expected {expected} occurrence(s), found {count}: {old[:80]!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")

def append(path, text):
    p = Path(path)
    current = p.read_text(encoding="utf-8")
    if text in current:
        raise SystemExit(f"{path}: appended correction already present")
    p.write_text(current + text, encoding="utf-8")

# F1: retain only the legitimate release-marker correction and restore the exact userscript
# origin/activation assertions that this feature branch had no reason to weaken.
replace(
    "forge/test/release_loader.test.mjs",
'''test("release loader: at most one @x-release-pending marker, and it names the package version", () => {
  const markers = LOADER.match(/^\\/\\/ @x-release-pending\\s+\\S+$/gm) || [];
  assert.ok(markers.length <= 1, "a second marker would shadow the real one from the checker");
  if (markers.length === 1) assert.equal(markers[0].split(/\\s+/)[2], PKG_VERSION);
});''',
'''test("release loader: pending marker matches release state and package version", () => {
  const markers = LOADER.match(/^\\/\\/ @x-release-pending\\s+\\S+$/gm) || [];
  const loaderVersion = (/^\\/\\/ @version\\s+(\\S+)$/m.exec(LOADER) || [])[1];
  assert.ok(loaderVersion, "loader must declare @version");
  const expected = loaderVersion === PKG_VERSION ? 0 : 1;
  assert.equal(markers.length, expected, "released loader has no pending marker; staged package has exactly one");
  if (expected === 1) assert.equal(markers[0].split(/\\s+/)[2], PKG_VERSION);
});'''
)
replace(
    "forge/test/release_loader.test.mjs",
'''test("release loader: @match covers the whole game origin, both hosts, so the carrier route is reachable", () => {
  const matches = LOADER.match(/^\\/\\/ @match\\s+\\S+$/gm) || [];
  assert.ok(matches.includes("// @match        *://www.theninja-rpg.com/*"));
  assert.ok(matches.includes("// @match        *://theninja-rpg.com/*"));
});''',
'''test("release loader: @match covers the whole game origin, both hosts, so the carrier route is reachable", () => {
  const matches = (LOADER.match(/^\\/\\/ @match\\s+(\\S+)$/gm) || []).map((line) => line.split(/\\s+/)[2]);
  assert.deepEqual(matches, ["*://www.theninja-rpg.com/*", "*://theninja-rpg.com/*"]);
  assert.ok(!matches.some((m) => m.includes("/forge")), "a /forge-only match cannot reach the carrier");
});'''
)
replace(
    "forge/test/release_loader.test.mjs",
'''  assert.match(LOADER, /tab that has NOT been armed through \\/forge, the bundle does nothing at all/);''',
'''  assert.match(LOADER, /has NOT been armed[\\s\\S]*does nothing at all/);'''
)
replace(
    "forge/test/release_loader.test.mjs",
'''  assert.match(LOADER, /Open https:\\/\\/www\\.theninja-rpg\\.com\\/forge while logged in/);''',
'''  assert.match(LOADER, /theninja-rpg\\.com\\/forge/);'''
)

# F11: make the repository's no-HTML-string-sink law enforceable in the shared helper.
replace(
    "forge/src/ui/dom.mjs",
'''// DOM helpers. createElement and CSSOM only; no innerHTML anywhere (repo law).

export function h(tag, attrs = {}, ...children) {''',
'''// DOM helpers. createElement and CSSOM only; no innerHTML anywhere (repo law).

const HTML_SINKS = new Set(["innerHTML", "outerHTML", "srcdoc", "insertAdjacentHTML"]);

export function h(tag, attrs = {}, ...children) {'''
)
replace(
    "forge/src/ui/dom.mjs",
'''    else if (k === "value" && "value" in el) el.value = String(v);
    else if (k in el && typeof v !== "string") el[k] = v;''',
'''    else if (k === "value" && "value" in el) el.value = String(v);
    else if (HTML_SINKS.has(k)) throw new Error(`h(): ${k} is not assignable (repo law: no HTML-string sinks)`);
    else if (k in el && typeof v !== "string") el[k] = v;'''
)

# F3/F8/F9: encode content paths, allowlist dispatchable workflows, and make the PAT
# permission failure actionable.
replace(
    "forge/src/github.mjs",
'''function assertBranch(branch) {
  if (typeof branch !== "string" || !branch || branch.startsWith("/") || branch.endsWith("/") || branch.includes("..") || !/^[A-Za-z0-9._/-]+$/.test(branch)) {
    throw new GithubError(`unsafe branch name ${JSON.stringify(branch)}`);
  }
  return branch;
}

export class Github {''',
'''function assertBranch(branch) {
  if (typeof branch !== "string" || !branch || branch.startsWith("/") || branch.endsWith("/") || branch.includes("..") || !/^[A-Za-z0-9._/-]+$/.test(branch)) {
    throw new GithubError(`unsafe branch name ${JSON.stringify(branch)}`);
  }
  return branch;
}

function encodeRepoPath(path) {
  if (typeof path !== "string" || !path || path.startsWith("/") || path.endsWith("/")) {
    throw new GithubError(`unsafe repository path ${JSON.stringify(path)}`);
  }
  return path.split("/").map((segment) => encodeURIComponent(segment)).join("/");
}

const DISPATCHABLE_WORKFLOWS = new Set(["quest_studio.yml"]);

export class Github {'''
)
replace(
    "forge/src/github.mjs",
'''  _url(path, ref = this.cfg.branch) {
    return this._repo(`contents/${path}?ref=${encodeURIComponent(assertBranch(ref))}`);
  }''',
'''  _url(path, ref = this.cfg.branch) {
    return this._repo(`contents/${encodeRepoPath(path)}?ref=${encodeURIComponent(assertBranch(ref))}`);
  }'''
)
replace(
    "forge/src/github.mjs",
'''    const r = await this.fetchImpl(this._repo(`contents/${path}`), {
      method: "PUT", headers: { ...this._headers(), "content-type": "application/json" }, body: JSON.stringify(body),
    });''',
'''    const r = await this.fetchImpl(this._repo(`contents/${encodeRepoPath(path)}`), {
      method: "PUT", headers: { ...this._headers(), "content-type": "application/json" }, body: JSON.stringify(body),
    });'''
)
replace(
    "forge/src/github.mjs",
'''    if (typeof workflow !== "string" || !/^[A-Za-z0-9._-]+$/.test(workflow)) {
      throw new GithubError(`unsafe workflow name ${JSON.stringify(workflow)}`);
    }
    ref = assertBranch(ref);''',
'''    if (typeof workflow !== "string" || !/^[A-Za-z0-9._-]+$/.test(workflow)) {
      throw new GithubError(`unsafe workflow name ${JSON.stringify(workflow)}`);
    }
    if (!DISPATCHABLE_WORKFLOWS.has(workflow)) {
      throw new GithubError(`workflow ${JSON.stringify(workflow)} is not dispatchable from Forge`);
    }
    ref = assertBranch(ref);'''
)
replace(
    "forge/src/github.mjs",
'''    if (r.status !== 204) {
      const t = await r.text();
      throw new GithubError(`dispatch ${workflow}: HTTP ${r.status} ${t.slice(0, 140)}`, { status: r.status });
    }''',
'''    if (r.status !== 204) {
      const t = await r.text();
      if (r.status === 403) {
        throw new GithubError(`dispatch ${workflow}: HTTP 403; the fine-grained PAT needs Actions: write on tnr-tools`, { status: 403 });
      }
      throw new GithubError(`dispatch ${workflow}: HTTP ${r.status} ${t.slice(0, 140)}`, { status: r.status });
    }'''
)

# F8: result-supplied artifact paths may not smuggle URL syntax or encoded traversal.
replace(
    "forge/src/studio/repository.mjs",
'''  if (!tail || path.includes("\\\\") || segments.some((segment) => !segment || segment === "." || segment === "..")) {
    throw new GithubError("Quest Studio generated manifest path escapes its request build directory");
  }''',
'''  if (!tail || /[%?#]/.test(tail) || path.includes("\\\\") || segments.some((segment) => !segment || segment === "." || segment === "..")) {
    throw new GithubError("Quest Studio generated manifest path escapes its request build directory");
  }'''
)

# F3: operator setup copy must match workflow_dispatch's actual fine-grained token scope.
replace(
    "forge/src/ui/screens.mjs",
'''placeholder: "fine-grained PAT (contents: write on tnr-tools only)"''',
'''placeholder: "fine-grained PAT (contents: write + actions: write on tnr-tools only)"'''
)

# F2/F7: read repository profile sentinels honestly and keep generated-manifest inspection
# inside the visible Studio surface.
replace(
    "forge/src/studio/ui.mjs",
'''function cleanText(value) { return typeof value === "string" ? value.trim() : ""; }

export function missionSourceFromDraft(draft) {''',
'''function cleanText(value) { return typeof value === "string" ? value.trim() : ""; }

const AWAITING_RULING = "AWAITING_RULING";

function containsAwaitingRuling(value) {
  if (value === AWAITING_RULING) return true;
  if (Array.isArray(value)) return value.some(containsAwaitingRuling);
  if (value && typeof value === "object") return Object.values(value).some(containsAwaitingRuling);
  return false;
}

function profileShapeNumber(profile, key) {
  const raw = profile?.shape?.[key];
  return typeof raw === "number" && Number.isFinite(raw) ? raw : null;
}

export function missionSourceFromDraft(draft) {'''
)
replace(
    "forge/src/studio/ui.mjs",
'''export function missionDraftProblems(draft, profiles) {
  const out = [];
  const profile = profiles?.ranks?.[draft.profile];
  if (!profile) out.push("Choose a repository Mission profile.");
  if (profile?.shape?.battle_nodes > 0) out.push("This profile needs combat authoring; the Encounter editor is not in this first UI slice yet.");
  if (!cleanText(draft.name)) out.push("Mission name is required.");
  if (!cleanText(draft.description)) out.push("Mission premise/description is required.");
  if (!cleanText(draft.successDescription)) out.push("Success outcome is required.");
  const beats = Array.isArray(draft.beats) ? draft.beats : [];
  if (!beats.length) out.push("Add at least one story beat.");
  for (let i = 0; i < beats.length; i++) if (!cleanText(beats[i]?.description)) out.push(`Beat ${i + 1} needs player-facing text.`);
  const expected = Number(profile?.shape?.objective_count);
  if (Number.isInteger(expected) && expected > 0 && beats.length + 1 !== expected) {
    out.push(`The ${draft.profile} profile owns an objective count of ${expected}; this draft currently has ${beats.length + 1}.`);
  }
  return out;
}

function profileLabel(key, profile) {
  const battles = Number(profile?.shape?.battle_nodes || 0);
  const nodes = Number(profile?.shape?.objective_count || 0);
  return `${key} · ${nodes || "?"} nodes${battles ? ` · ${battles} battle${battles === 1 ? "" : "s"}` : " · no combat"}`;
}''',
'''export function missionDraftProblems(draft, profiles) {
  const out = [];
  const profile = profiles?.ranks?.[draft.profile];
  if (!profile) out.push("Choose a repository Mission profile.");
  const unresolved = !!profile && containsAwaitingRuling(profile);
  const battles = profileShapeNumber(profile, "battle_nodes");
  if (unresolved) out.push(`The ${draft.profile} Mission profile is awaiting a director ruling; unresolved profile values cannot compile.`);
  else if (battles !== null && battles > 0) out.push("This profile needs combat authoring; the Encounter editor is not in this first UI slice yet.");
  if (!cleanText(draft.name)) out.push("Mission name is required.");
  if (!cleanText(draft.description)) out.push("Mission premise/description is required.");
  if (!cleanText(draft.successDescription)) out.push("Success outcome is required.");
  const beats = Array.isArray(draft.beats) ? draft.beats : [];
  if (!beats.length) out.push("Add at least one story beat.");
  for (let i = 0; i < beats.length; i++) if (!cleanText(beats[i]?.description)) out.push(`Beat ${i + 1} needs player-facing text.`);
  const expected = profileShapeNumber(profile, "objective_count");
  if (expected !== null && expected > 0 && beats.length + 1 !== expected) {
    out.push(`The ${draft.profile} profile owns an objective count of ${expected}; this draft currently has ${beats.length + 1}.`);
  }
  return out;
}

function profileLabel(key, profile) {
  if (containsAwaitingRuling(profile)) return `${key} · awaiting ruling`;
  const battles = profileShapeNumber(profile, "battle_nodes");
  const nodes = profileShapeNumber(profile, "objective_count");
  if (battles === null || nodes === null) return `${key} · profile shape unavailable`;
  return `${key} · ${nodes} nodes${battles ? ` · ${battles} battle${battles === 1 ? "" : "s"}` : " · no combat"}`;
}'''
)
replace(
    "forge/src/studio/ui.mjs",
'''    const count = Math.max(1, Number(profile.shape?.objective_count || 2) - 1);
    this.draft.beats = Array.from({ length: count }, () => ({ description: "", choiceText: "Continue" }));''',
'''    const objectiveCount = profileShapeNumber(profile, "objective_count");
    if (objectiveCount === null) return;
    const count = Math.max(1, objectiveCount - 1);
    this.draft.beats = Array.from({ length: count }, () => ({ description: "", choiceText: "Continue" }));'''
)
replace(
    "forge/src/studio/ui.mjs",
'''  matchProfileShape() {
    const expected = Number(this.profiles?.ranks?.[this.draft.profile]?.shape?.objective_count || 0);
    if (!expected) return;''',
'''  matchProfileShape() {
    const expected = profileShapeNumber(this.profiles?.ranks?.[this.draft.profile], "objective_count");
    if (expected === null || expected <= 0) return;'''
)
replace(
    "forge/src/studio/ui.mjs",
'''    for (const [key, profile] of Object.entries(ranks)) {
      const combat = Number(profile?.shape?.battle_nodes || 0) > 0;
      options.push(h("option", { value: key, selected: this.draft.profile === key, disabled: combat }, profileLabel(key, profile) + (combat ? " · Encounter editor required" : "")));
    }
    const select = h("select", { value: this.draft.profile, onChange: (e) => this.chooseProfile(e.target.value) }, options);
    const profile = ranks[this.draft.profile];
    const expected = Number(profile?.shape?.objective_count || 0);
    const problems = missionDraftProblems(this.draft, this.profiles);''',
'''    for (const [key, profile] of Object.entries(ranks)) {
      const unresolved = containsAwaitingRuling(profile);
      const battleNodes = profileShapeNumber(profile, "battle_nodes");
      const combat = battleNodes !== null && battleNodes > 0;
      const suffix = !unresolved && combat ? " · Encounter editor required" : "";
      options.push(h("option", { value: key, selected: this.draft.profile === key, disabled: combat || unresolved }, profileLabel(key, profile) + suffix));
    }
    const select = h("select", { value: this.draft.profile, onChange: (e) => this.chooseProfile(e.target.value) }, options);
    const profile = ranks[this.draft.profile];
    const expected = profileShapeNumber(profile, "objective_count");
    const battleNodes = profileShapeNumber(profile, "battle_nodes");
    const problems = missionDraftProblems(this.draft, this.profiles);'''
)
replace(
    "forge/src/studio/ui.mjs",
'''      profile ? h("div", { class: "qs-two" },
        h("div", { class: "qs-callout info" }, h("div", { class: "qs-status-title" }, `${expected} objective${expected === 1 ? "" : "s"}`), h("div", { class: "qs-muted" }, "Owned by the selected Mission profile.")),
        h("div", { class: "qs-callout info" }, h("div", { class: "qs-status-title" }, `${Number(profile.shape?.battle_nodes || 0)} battle node${Number(profile.shape?.battle_nodes || 0) === 1 ? "" : "s"}`), h("div", { class: "qs-muted" }, "Combat profiles unlock after the Encounter editor lands."))) : null,
      expected ? h("div", { class: "qs-actions" }, h("button", { onClick: () => this.matchProfileShape() }, "Match profile shape")) : null,''',
'''      profile ? h("div", { class: "qs-two" },
        h("div", { class: expected === null ? "qs-callout warn" : "qs-callout info" }, h("div", { class: "qs-status-title" }, expected === null ? "Awaiting ruling" : `${expected} objective${expected === 1 ? "" : "s"}`), h("div", { class: "qs-muted" }, "Owned by the selected Mission profile.")),
        h("div", { class: battleNodes === null ? "qs-callout warn" : "qs-callout info" }, h("div", { class: "qs-status-title" }, battleNodes === null ? "Awaiting ruling" : `${battleNodes} battle node${battleNodes === 1 ? "" : "s"}`), h("div", { class: "qs-muted" }, battleNodes === null ? "Repository profile is unresolved." : "Combat profiles unlock after the Encounter editor lands."))) : null,
      expected !== null && expected > 0 ? h("div", { class: "qs-actions" }, h("button", { onClick: () => this.matchProfileShape() }, "Match profile shape")) : null,'''
)
replace(
    "forge/src/studio/ui.mjs",
'''    if (state.waiting) return h("div", { class: "qs-callout info" }, h("div", { class: "qs-status-title" }, "Build still running"), h("div", { class: "qs-muted" }, "No current result has landed yet. Refresh status without resubmitting the source."));''',
'''    if (state.waiting) return h("div", { class: "qs-callout info" }, h("div", { class: "qs-status-title" }, "Build result not available yet"), h("div", { class: "qs-muted" }, "No current result has landed. The worker may still be running, or it may have failed before result persistence. Refresh status before resubmitting the source."));'''
)
replace(
    "forge/src/studio/ui.mjs",
'''      result.status === "valid" && !stale ? h("div", { class: "qs-actions" }, h("button", { onClick: () => this.inspectManifest() }, "Inspect generated manifest")) : null,
      h("div", { class: "qs-provenance" }, `Source revision: ${result.provenance?.sourceRevision || "unknown"} · Compiler: ${result.provenance?.compilerRevision || "unknown"}`));''',
'''      result.status === "valid" && !stale ? h("div", { class: "qs-actions" }, h("button", { onClick: () => this.inspectManifest() }, "Inspect generated manifest")) : null,
      state.manifestText ? h("label", { class: "qs-field" }, h("span", {}, "Generated manifest · inspection only"), h("textarea", { value: state.manifestText, readOnly: true, rows: 18 })) : null,
      h("div", { class: "qs-provenance" }, `Source revision: ${result.provenance?.sourceRevision || "unknown"} · Compiler: ${result.provenance?.compilerRevision || "unknown"}`));'''
)
replace(
    "forge/src/studio/ui.mjs",
'''      const text = await this.repository.generatedManifest(this.draft.requestId, result);
      this.app.showExport(text, `Generated manifest · ${this.draft.name || this.draft.requestId}`);''',
'''      const text = await this.repository.generatedManifest(this.draft.requestId, result);
      this.buildState = { ...this.buildState, manifestText: text };
      this.renderMission();'''
)

# F4/F5: bind every result to the validated request id, and enforce Mission profile shape
# canonically in the repository adapter rather than only in the browser.
replace(
    "skills/building-tnr-content/scripts/quest_compile.py",
'''def validate_source(raw: Any) -> dict:''',
'''def validate_source(raw: Any, expected_request_id: str | None = None) -> dict:'''
)
replace(
    "skills/building-tnr-content/scripts/quest_compile.py",
'''    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id):
        raise QuestSourceError(
            "requestId must match ^[a-z0-9][a-z0-9._-]{2,63}$"
        )
    subtype = raw.get("subtype")''',
'''    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id):
        raise QuestSourceError(
            "requestId must match ^[a-z0-9][a-z0-9._-]{2,63}$"
        )
    if expected_request_id is not None and request_id != expected_request_id:
        raise QuestSourceError(
            f"Quest Source requestId {request_id!r} does not match worker request id {expected_request_id!r}"
        )
    subtype = raw.get("subtype")'''
)
replace(
    "skills/building-tnr-content/scripts/quest_compile.py",
'''def entity_summary(manifest: dict) -> dict:
    counts: dict[str, int] = {}
    creates = 0
    updates = 0
    for item in manifest.get("items") or []:
        ent = str(item.get("entity") or "unknown")
        counts[ent] = counts.get(ent, 0) + 1
        if item.get("slot") == "create":
            creates += 1
        else:
            updates += 1
    return {"counts": counts, "creates": creates, "updates": updates}


def compile_mission(source: dict, artifact_dir: Path, artifact_prefix: str) -> dict:''',
'''def entity_summary(manifest: dict) -> dict:
    counts: dict[str, int] = {}
    creates = 0
    updates = 0
    for item in manifest.get("items") or []:
        ent = str(item.get("entity") or "unknown")
        counts[ent] = counts.get(ent, 0) + 1
        if item.get("slot") == "create":
            creates += 1
        else:
            updates += 1
    return {"counts": counts, "creates": creates, "updates": updates}


def enforce_mission_profile_shape(source: dict, profiles: dict, manifest: dict) -> None:
    rank = source.get("content", {}).get("rank")
    profile = (profiles.get("ranks") or {}).get(rank)
    if not isinstance(profile, dict):
        raise QuestSourceError(f"unknown Mission profile {rank!r}")
    shape = profile.get("shape") or {}
    expected_objectives = shape.get("objective_count")
    expected_battles = shape.get("battle_nodes")
    # mission.py owns unresolved-ruling refusal. Only ratified numeric shape values are enforced here.
    if type(expected_objectives) is not int or type(expected_battles) is not int:
        return

    quest_item = next((item for item in manifest.get("items") or [] if item.get("entity") == "quest"), None)
    data = quest_item.get("data") if isinstance(quest_item, dict) else None
    objectives = data.get("objectives") if isinstance(data, dict) else None
    if not isinstance(objectives, list):
        raise QuestSourceError("mission adapter produced no quest objective list")

    battle_tasks = {"start_battle", "defeat_opponents"}
    actual_objectives = len(objectives)
    actual_battles = sum(1 for objective in objectives if objective.get("task") in battle_tasks)
    mismatches = []
    if actual_objectives != expected_objectives:
        mismatches.append(f"{actual_objectives} objectives; profile requires {expected_objectives}")
    if actual_battles != expected_battles:
        mismatches.append(f"{actual_battles} battle nodes; profile requires {expected_battles}")
    if mismatches:
        raise QuestBlocked(
            "profile_shape_unmet",
            f"Mission profile shape is not met for {rank}: " + "; ".join(mismatches),
        )


def compile_mission(source: dict, artifact_dir: Path, artifact_prefix: str) -> dict:'''
)
replace(
    "skills/building-tnr-content/scripts/quest_compile.py",
'''    manifest = built.get("manifest")
    if not isinstance(manifest, dict):
        raise QuestSourceError("mission adapter returned no manifest")

    artifact_dir.mkdir(parents=True, exist_ok=True)''',
'''    manifest = built.get("manifest")
    if not isinstance(manifest, dict):
        raise QuestSourceError("mission adapter returned no manifest")
    enforce_mission_profile_shape(source, profiles, manifest)

    artifact_dir.mkdir(parents=True, exist_ok=True)'''
)
replace(
    "skills/building-tnr-content/scripts/quest_compile.py",
'''    ap.add_argument("--source-revision")
    ap.add_argument("--compiler-revision")''',
'''    ap.add_argument("--source-revision")
    ap.add_argument("--compiler-revision")
    ap.add_argument("--request-id", help="validated worker request identity; binds failure envelopes to the request")'''
)
replace(
    "skills/building-tnr-content/scripts/quest_compile.py",
'''    result_path = Path(args.result).resolve()
    artifact_dir = Path(args.artifact_dir).resolve()
    try:
        source = load_json(Path(args.source).resolve())
        source = validate_source(source)
        result = compile_source(
            source,
            artifact_dir=artifact_dir,
            artifact_prefix=args.artifact_prefix.strip("/"),
            source_revision=args.source_revision,
            compiler_revision=args.compiler_revision,
        )
    except Exception as exc:
        # We can only emit the standard envelope when request identity is readable.
        # Malformed top-level JSON/source is a worker failure, not a content blocker.
        result = {
            "schemaVersion": RESULT_VERSION,
            "kind": "quest-build",
            "requestId": None,
            "subtype": None,''',
'''    result_path = Path(args.result).resolve()
    artifact_dir = Path(args.artifact_dir).resolve()
    expected_request_id = args.request_id
    if expected_request_id is not None and not REQUEST_ID_RE.fullmatch(expected_request_id):
        raise SystemExit("--request-id must match ^[a-z0-9][a-z0-9._-]{2,63}$")
    raw_source: Any = None
    try:
        raw_source = load_json(Path(args.source).resolve())
        source = validate_source(raw_source, expected_request_id=expected_request_id)
        result = compile_source(
            source,
            artifact_dir=artifact_dir,
            artifact_prefix=args.artifact_prefix.strip("/"),
            source_revision=args.source_revision,
            compiler_revision=args.compiler_revision,
        )
    except Exception as exc:
        # The worker-supplied identity survives malformed authored source so Forge can always read
        # a request-scoped failed envelope instead of wedging the draft on requestId:null.
        fallback_request_id = expected_request_id
        if fallback_request_id is None and isinstance(raw_source, dict):
            candidate = raw_source.get("requestId")
            if isinstance(candidate, str) and REQUEST_ID_RE.fullmatch(candidate):
                fallback_request_id = candidate
        subtype = raw_source.get("subtype") if isinstance(raw_source, dict) and isinstance(raw_source.get("subtype"), str) else None
        result = {
            "schemaVersion": RESULT_VERSION,
            "kind": "quest-build",
            "requestId": fallback_request_id,
            "subtype": subtype,'''
)

# Integration coverage for request identity and canonical profile-shape enforcement.
replace(
    "skills/building-tnr-content/scripts/quest_compile_integration_test.py",
'''        print("PASS  current D Mission source compiles through mission.py + validate.py")
        print("PASS  provenance and live-game boundary are preserved")
        return 0''',
'''        print("PASS  current D Mission source compiles through mission.py + validate.py")
        print("PASS  provenance and live-game boundary are preserved")

        bad_shape = json.loads(json.dumps(source))
        bad_shape["requestId"] = "selftest-mission-shape"
        bad_shape["content"]["rank"] = "C"
        shape_result = quest_compile.compile_source(
            bad_shape,
            artifact_dir=root / "shape-build",
            artifact_prefix="studio/builds/selftest-mission-shape",
            source_revision="3" * 40,
            compiler_revision="4" * 40,
        )
        if shape_result.get("status") != "blocked":
            print(json.dumps(shape_result, indent=2))
            raise SystemExit("Combat Mission without required battle nodes was not blocked")
        if not any(x.get("code") == "profile_shape_unmet" for x in shape_result.get("blockers", [])):
            raise SystemExit("Profile-shape blocker did not use profile_shape_unmet")

        invalid_source = root / "invalid.quest.json"
        invalid_result = root / "invalid.build.json"
        invalid_source.write_text(json.dumps({
            "schemaVersion": 1,
            "kind": "quest",
            "requestId": "selftest-invalid",
            "subtype": "guide",
            "content": {},
        }), encoding="utf-8")
        rc = quest_compile.main([
            str(invalid_source),
            "--result", str(invalid_result),
            "--artifact-dir", str(root / "invalid-build"),
            "--artifact-prefix", "studio/builds/selftest-invalid",
            "--source-revision", "5" * 40,
            "--compiler-revision", "6" * 40,
            "--request-id", "selftest-invalid",
        ])
        failed = json.loads(invalid_result.read_text(encoding="utf-8"))
        if rc != 1 or failed.get("status") != "failed" or failed.get("requestId") != "selftest-invalid":
            print(json.dumps(failed, indent=2))
            raise SystemExit("Failed source did not preserve worker request identity")

        print("PASS  repository adapter blocks Mission profile-shape mismatches")
        print("PASS  failed envelopes preserve the validated worker request id")
        return 0'''
)

# F6/F10: validate dispatch identity before touching authored content, pin the request checkout to
# the exact source commit, persist content-boundary failures as standard failed envelopes, and pass
# the worker identity to the compiler.
replace(
    ".github/workflows/quest_studio.yml",
'''      - name: Checkout authored request branch
        uses: actions/checkout@v4
        with:
          ref: ${{ inputs.request_branch }}
          path: request
          fetch-depth: 1

      - name: Validate request boundary
        env:
          TRUSTED_REF: ${{ github.ref }}
          REQUEST_BRANCH: ${{ inputs.request_branch }}
          SOURCE_PATH: ${{ inputs.source_path }}
          REQUEST_ID: ${{ inputs.request_id }}
          SOURCE_SHA: ${{ inputs.source_sha }}
        run: |
          set -euo pipefail
          [[ "$TRUSTED_REF" == "refs/heads/main" ]] || { echo "Quest Studio worker must be dispatched from main" >&2; exit 2; }
          [[ "$REQUEST_ID" =~ ^[a-z0-9][a-z0-9._-]{2,63}$ ]] || { echo "invalid request_id" >&2; exit 2; }
          [[ "$SOURCE_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "invalid source_sha" >&2; exit 2; }
          [[ "$REQUEST_BRANCH" == "studio/quest/$REQUEST_ID" ]] || { echo "request branch does not match request id" >&2; exit 2; }
          [[ "$SOURCE_PATH" == "studio/requests/$REQUEST_ID.quest.json" ]] || { echo "source path does not match request id" >&2; exit 2; }

          ACTUAL_SHA="$(git -C request rev-parse HEAD)"
          [[ "$ACTUAL_SHA" == "$SOURCE_SHA" ]] || {
            echo "request branch advanced: expected $SOURCE_SHA, checked out $ACTUAL_SHA" >&2
            exit 3
          }

          for p in request/studio request/studio/requests request/studio/results request/studio/builds; do
            [[ ! -L "$p" ]] || { echo "refusing symlinked Studio path: $p" >&2; exit 2; }
          done
          [[ -f "request/$SOURCE_PATH" && ! -L "request/$SOURCE_PATH" ]] || {
            echo "Quest Source is missing, not a regular file, or is a symlink" >&2
            exit 2
          }''',
'''      - name: Validate dispatch identity
        env:
          TRUSTED_REF: ${{ github.ref }}
          REQUEST_BRANCH: ${{ inputs.request_branch }}
          SOURCE_PATH: ${{ inputs.source_path }}
          REQUEST_ID: ${{ inputs.request_id }}
          SOURCE_SHA: ${{ inputs.source_sha }}
        run: |
          set -euo pipefail
          [[ "$TRUSTED_REF" == "refs/heads/main" ]] || { echo "Quest Studio worker must be dispatched from main" >&2; exit 2; }
          [[ "$REQUEST_ID" =~ ^[a-z0-9][a-z0-9._-]{2,63}$ ]] || { echo "invalid request_id" >&2; exit 2; }
          [[ "$SOURCE_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "invalid source_sha" >&2; exit 2; }
          [[ "$REQUEST_BRANCH" == "studio/quest/$REQUEST_ID" ]] || { echo "request branch does not match request id" >&2; exit 2; }
          [[ "$SOURCE_PATH" == "studio/requests/$REQUEST_ID.quest.json" ]] || { echo "source path does not match request id" >&2; exit 2; }

      - name: Checkout authored request source
        uses: actions/checkout@v4
        with:
          ref: ${{ inputs.source_sha }}
          path: request
          fetch-depth: 1

      - name: Validate request content
        id: boundary
        env:
          SOURCE_PATH: ${{ inputs.source_path }}
          REQUEST_ID: ${{ inputs.request_id }}
          SOURCE_SHA: ${{ inputs.source_sha }}
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
              if [[ -L "$p" ]]; then ERROR="refusing symlinked Studio path: $p"; break; fi
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
          fi'''
)
replace(
    ".github/workflows/quest_studio.yml",
'''          SOURCE_PATH: ${{ inputs.source_path }}
          REQUEST_ID: ${{ inputs.request_id }}
          SOURCE_SHA: ${{ inputs.source_sha }}
          COMPILER_SHA: ${{ github.sha }}
          RUNNER_TEMP: ${{ runner.temp }}''',
'''          SOURCE_PATH: ${{ inputs.source_path }}
          REQUEST_ID: ${{ inputs.request_id }}
          SOURCE_SHA: ${{ inputs.source_sha }}
          COMPILER_SHA: ${{ github.sha }}
          BOUNDARY_RC: ${{ steps.boundary.outputs.boundary_rc }}
          RUNNER_TEMP: ${{ runner.temp }}'''
)
replace(
    ".github/workflows/quest_studio.yml",
'''          rm -rf "$TMP_ROOT"
          mkdir -p "$TMP_BUILD"

          set +e
          python3 tools/skills/building-tnr-content/scripts/quest_compile.py \\
            "request/$SOURCE_PATH" \\
            --result "$TMP_RESULT" \\
            --artifact-dir "$TMP_BUILD" \\
            --artifact-prefix "studio/builds/$REQUEST_ID" \\
            --source-revision "$SOURCE_SHA" \\
            --compiler-revision "$COMPILER_SHA"
          RC=$?
          set -e''',
'''          mkdir -p "$TMP_BUILD"

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
          Path(result_path).write_text(json.dumps(result, indent=2) + "\\n", encoding="utf-8")
          PY
            RC="$BOUNDARY_RC"
          else
            set +e
            python3 tools/skills/building-tnr-content/scripts/quest_compile.py \\
              "request/$SOURCE_PATH" \\
              --result "$TMP_RESULT" \\
              --artifact-dir "$TMP_BUILD" \\
              --artifact-prefix "studio/builds/$REQUEST_ID" \\
              --source-revision "$SOURCE_SHA" \\
              --compiler-revision "$COMPILER_SHA" \\
              --request-id "$REQUEST_ID"
            RC=$?
            set -e
          fi'''
)

# F10: static worker test must pin order, exact-SHA request checkout, and robust multiline run bodies.
replace(
    "skills/building-tnr-content/scripts/quest_worker_contract_test.py",
'''from pathlib import Path''',
'''from pathlib import Path
import re'''
)
replace(
    "skills/building-tnr-content/scripts/quest_worker_contract_test.py",
'''def forbid(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle in text:
        failures.append(label)


def main() -> int:''',
'''def forbid(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle in text:
        failures.append(label)


def require_order(text: str, needles: list[str], label: str, failures: list[str]) -> None:
    positions = [text.find(needle) for needle in needles]
    if any(pos < 0 for pos in positions) or positions != sorted(positions):
        failures.append(label)


def multiline_run_text(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        match = re.match(r"^(\\s*)run:\\s*[|>][+-]?\\s*$", line)
        if not match:
            continue
        indent = len(match.group(1))
        for body in lines[i + 1:]:
            if body.strip() and len(body) - len(body.lstrip()) <= indent:
                break
            out.append(body)
    return "\\n".join(out)


def main() -> int:'''
)
replace(
    "skills/building-tnr-content/scripts/quest_worker_contract_test.py",
'''    require(text, "name: Checkout authored request branch", "request checkout exists", failures)
    require(text, "ref: ${{ inputs.request_branch }}", "request checkout follows request branch input", failures)
    require(text, "path: request", "request checkout is isolated under request/", failures)

    # Dispatch must execute the trusted workflow on main and bind branch/path/id exactly.
    require(text, '[[ "$TRUSTED_REF" == "refs/heads/main" ]]', "dispatch is main-only", failures)''',
'''    require(text, "name: Checkout authored request source", "request checkout exists", failures)
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
    require(text, '[[ "$TRUSTED_REF" == "refs/heads/main" ]]', "dispatch is main-only", failures)'''
)
replace(
    "skills/building-tnr-content/scripts/quest_worker_contract_test.py",
'''    # Workflow expressions for untrusted inputs belong in env/ref fields, never interpolated into run scripts.
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
    run_text = "\\n".join(run_lines)
    forbid(run_text, "${{ inputs.", "untrusted workflow inputs are not interpolated into shell", failures)''',
'''    # Workflow expressions for untrusted inputs belong in env/ref fields, never interpolated into run scripts.
    run_text = multiline_run_text(text)
    forbid(run_text, "${{ inputs.", "untrusted workflow inputs are not interpolated into shell", failures)'''
)
replace(
    "skills/building-tnr-content/scripts/quest_worker_contract_test.py",
'''    checks = 21''',
'''    checks = 26'''
)

# Tests: real profile sentinel, visible manifest inspection, HTML-sink denial, dispatch allowlist/scope,
# failed-envelope readability, and URL/path traversal hardening.
replace(
    "forge/test/quest.studio.ui.test.mjs",
'''import { JSDOM } from "jsdom";

import { MemoryStorage } from "./shim.mjs";''',
'''import { JSDOM } from "jsdom";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { MemoryStorage } from "./shim.mjs";
import { h } from "../src/ui/dom.mjs";

const REPO = join(dirname(fileURLToPath(import.meta.url)), "..", "..");'''
)
replace(
    "forge/test/quest.studio.ui.test.mjs",
'''function repositoryStub({ result = null } = {}) {''',
'''function repositoryStub({ result = null, profiles: profileOverride = null } = {}) {'''
)
replace(
    "forge/test/quest.studio.ui.test.mjs",
'''  const profiles = {
    ranks: {
      D: { shape: { objective_count: 4, battle_nodes: 0 } },
      D_combat: { shape: { objective_count: 4, battle_nodes: 1 } },
    },
  };''',
'''  const profiles = profileOverride ?? {
    ranks: {
      D: { shape: { objective_count: 4, battle_nodes: 0 } },
      D_combat: { shape: { objective_count: 4, battle_nodes: 1 } },
    },
  };'''
)
append(
    "forge/test/quest.studio.ui.test.mjs",
'''

test("real Mission profile sentinels render as awaiting ruling and block compile", async () => {
  const profiles = JSON.parse(readFileSync(join(REPO, "skills/building-tnr-content/data/48_DATA_mission_profiles.json"), "utf8"));
  const draft = newMissionDraft();
  Object.assign(draft, {
    profile: "S", name: "Unresolved S", description: "Test.", successDescription: "Done.",
    beats: [{ description: "1" }, { description: "2" }, { description: "3" }],
  });
  assert.match(missionDraftProblems(draft, profiles).join(" "), /awaiting a director ruling/i);

  const win = setupDom();
  const app = fakeApp(win);
  const studio = new QuestStudioWorkspace({ app, repository: repositoryStub({ profiles }), pollMs: 0, maxPolls: 1 }).install();
  await studio.open();
  studio.draft = draft;
  await studio.openMission(false);
  const sOption = [...studio.shell.querySelectorAll("select option")].find((x) => x.value === "S");
  assert.equal(sOption.disabled, true);
  assert.match(sOption.textContent, /awaiting ruling/i);
  assert.doesNotMatch(studio.shell.textContent, /NaN|S · \\? nodes|S · no combat/);
  assert.equal(studio.shell.querySelector(".qs-compile").disabled, true);
});

test("generated manifest inspection is visible inside the Studio shell", async () => {
  const win = setupDom();
  const app = fakeApp(win);
  const result = {
    schemaVersion: 1, kind: "quest-build", requestId: "quest-inspect", subtype: "mission",
    status: "valid", blockers: [], errors: [], warnings: [],
    generated: { manifestPath: "studio/builds/quest-inspect/manifest.json", entities: { counts: { quest: 1 } } },
    provenance: { sourceRevision: "a".repeat(40), compilerRevision: "b".repeat(40) },
    liveGameTouched: false,
  };
  const studio = new QuestStudioWorkspace({ app, repository: repositoryStub({ result }), pollMs: 0, maxPolls: 1 }).install();
  await studio.open();
  studio.draft = {
    version: 1, requestId: "quest-inspect", subtype: "mission", profile: "D",
    name: "Inspect", description: "A.", successDescription: "B.",
    beats: [{ description: "1" }, { description: "2" }, { description: "3" }],
    updatedAt: new Date().toISOString(), sourceCommit: "a".repeat(40), lastResult: null,
  };
  await studio.openMission(false);
  studio.buildState = { result, stale: false, sourceCommit: "a".repeat(40) };
  studio.renderMission();
  await studio.inspectManifest();
  assert.match(studio.shell.textContent, /Generated manifest · inspection only/);
  const manifest = [...studio.shell.querySelectorAll("textarea")].at(-1);
  assert.equal(manifest.value, '{"items":[]}');
  assert.equal(app.root.dataset.exportText, undefined);
});

test("DOM helper rejects HTML string sinks even through property coercion", () => {
  setupDom();
  assert.throws(() => h("div", { innerHTML: { toString: () => "<b>unsafe</b>" } }), /not assignable/);
});
'''
)
append(
    "forge/test/github.studio.test.mjs",
'''

test("Github.dispatch allowlists Quest Studio and explains missing Actions permission", async () => {
  let calls = 0;
  const github = new Github({
    fetchImpl: async () => { calls += 1; return new Response("forbidden", { status: 403 }); },
    storage: storageWithPat(),
  });
  await assert.rejects(
    () => github.dispatch("relay.yml", { ref: "main", inputs: {} }),
    /not dispatchable from Forge/,
  );
  assert.equal(calls, 0);
  await assert.rejects(
    () => github.dispatch("quest_studio.yml", { ref: "main", inputs: {} }),
    /Actions: write/,
  );
  assert.equal(calls, 1);
});

test("Github content URLs encode path syntax instead of allowing ref/query injection", async () => {
  let seen = "";
  const github = new Github({
    fetchImpl: async (url) => {
      seen = url;
      return new Response("{}", { status: 200 });
    },
    storage: storageWithPat(),
  });
  await github.text("studio/builds/demo/a?ref=main#x.json", "studio/quest/demo");
  assert.match(seen, /a%3Fref%3Dmain%23x\\.json\\?ref=studio%2Fquest%2Fdemo$/);
  assert.doesNotMatch(seen, /\\/a\\?ref=main/);
});

test("failed build envelope remains readable when it carries the worker request identity", () => {
  const result = validateBuildResult({
    schemaVersion: 1,
    kind: "quest-build",
    requestId: "demo-mission",
    subtype: "guide",
    status: "failed",
    errors: [{ code: "source_invalid", message: "unknown subtype" }],
    liveGameTouched: false,
  }, "demo-mission");
  assert.equal(result.status, "failed");
});
'''
)
replace(
    "forge/test/github.studio.test.mjs",
'''    "studio/builds/demo-mission/..\\\\other\\\\manifest.json",
  ]) {''',
'''    "studio/builds/demo-mission/..\\\\other\\\\manifest.json",
    "studio/builds/demo-mission/..%2f..%2fpush%2f46.json",
    "studio/builds/demo-mission/%2e%2e/%2e%2e/push/46.json",
    "studio/builds/demo-mission/a?ref=main&x=.json",
  ]) {'''
)

print("Quest Studio correction edits prepared.")
