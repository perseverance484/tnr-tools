// Forge-side repository adapter for Quest Studio. It translates a human-authored Quest Source
// into the narrow GitHub request contract implemented by .github/workflows/quest_studio.yml.
// Canonical compilation still happens in repository Python tooling; this module owns transport,
// request identity and stale-result detection only.

import { GithubError } from "../github.mjs";

const REQUEST_RE = /^[a-z0-9][a-z0-9._-]{2,63}$/;

export const QUEST_STUDIO = Object.freeze({
  sourceSchemaVersion: 1,
  resultSchemaVersion: 1,
  registryPath: "skills/building-tnr-content/data/49_DATA_quest_studio_subtypes.json",
  missionProfilesPath: "skills/building-tnr-content/data/48_DATA_mission_profiles.json",
  workflow: "quest_studio.yml",
  branchPrefix: "studio/quest/",
  sourceRoot: "studio/requests",
  resultRoot: "studio/results",
  buildRoot: "studio/builds",
});

export function questRequestId(value) {
  if (typeof value !== "string" || !REQUEST_RE.test(value)) throw new GithubError(`invalid Quest Studio request id ${JSON.stringify(value)}`);
  return value;
}

export function questBranch(id) { return QUEST_STUDIO.branchPrefix + questRequestId(id); }
export function questSourcePath(id) { return `${QUEST_STUDIO.sourceRoot}/${questRequestId(id)}.quest.json`; }
export function questResultPath(id) { return `${QUEST_STUDIO.resultRoot}/${questRequestId(id)}.build.json`; }

export function validateQuestSource(source) {
  if (!source || typeof source !== "object" || Array.isArray(source)) throw new GithubError("Quest Source must be an object");
  if (source.schemaVersion !== QUEST_STUDIO.sourceSchemaVersion) throw new GithubError(`Quest Source schemaVersion must be ${QUEST_STUDIO.sourceSchemaVersion}`);
  if (source.kind !== "quest") throw new GithubError("Quest Source kind must be quest");
  questRequestId(source.requestId);
  if (typeof source.subtype !== "string" || !source.subtype) throw new GithubError("Quest Source subtype is required");
  if (!source.content || typeof source.content !== "object" || Array.isArray(source.content)) throw new GithubError("Quest Source content must be an object");
  return source;
}

export function validateBuildResult(result, requestId) {
  const id = questRequestId(requestId);
  if (!result || typeof result !== "object" || Array.isArray(result)) throw new GithubError("Quest Studio build result must be an object");
  if (result.schemaVersion !== QUEST_STUDIO.resultSchemaVersion || result.kind !== "quest-build") throw new GithubError("Quest Studio build result has an unsupported contract version");
  if (result.requestId !== id) throw new GithubError(`Quest Studio result belongs to ${JSON.stringify(result.requestId)}, expected ${JSON.stringify(id)}`);
  if (!new Set(["valid", "blocked", "failed"]).has(result.status)) throw new GithubError(`Quest Studio result has unknown status ${JSON.stringify(result.status)}`);
  if (result.liveGameTouched !== false) throw new GithubError("Quest Studio repository build must state liveGameTouched:false");
  return result;
}

export class QuestStudioRepository {
  constructor({ github, baseRef = "main" }) {
    this.github = github;
    this.baseRef = baseRef;
  }

  async registry() {
    const j = await this.github.json(QUEST_STUDIO.registryPath, this.baseRef);
    if (!j || typeof j !== "object" || j._meta?.schemaVersion !== 1 || !j.subtypes) throw new GithubError("Quest Studio subtype registry has an unsupported shape");
    return j;
  }

  async missionProfiles() {
    const j = await this.github.json(QUEST_STUDIO.missionProfilesPath, this.baseRef);
    if (!j || typeof j !== "object" || !j.ranks || typeof j.ranks !== "object") throw new GithubError("Mission profile source has an unsupported shape");
    return j;
  }

  /**
   * Persist a source revision on its dedicated branch and dispatch the trusted repository worker.
   * The returned sourceCommit is the exact revision the worker must compile.
   */
  async submit(source) {
    source = validateQuestSource(source);
    const id = source.requestId;
    const branch = questBranch(id);
    const sourcePath = questSourcePath(id);
    await this.github.ensureBranch(branch, this.baseRef);
    const saved = await this.github.put(
      sourcePath,
      JSON.stringify(source, null, 2) + "\n",
      `studio: save Quest Source ${id}`,
      { branch },
    );
    if (!saved.commitSha) throw new GithubError("Quest Studio source save returned no commit SHA");
    await this.dispatch(id, saved.commitSha);
    return { requestId: id, branch, sourcePath, sourceCommit: saved.commitSha };
  }

  /** Retry only the build request for an already-saved exact source revision. */
  async dispatch(requestId, sourceCommit) {
    const id = questRequestId(requestId);
    if (typeof sourceCommit !== "string" || !/^[0-9a-f]{40}$/.test(sourceCommit)) throw new GithubError("Quest Studio sourceCommit must be a 40-character lowercase git SHA");
    await this.github.dispatch(QUEST_STUDIO.workflow, {
      ref: this.baseRef,
      inputs: {
        request_branch: questBranch(id),
        source_path: questSourcePath(id),
        request_id: id,
        source_sha: sourceCommit,
      },
    });
    return { requestId: id, sourceCommit };
  }

  /**
   * Read the latest persisted build result. A stale result is returned explicitly rather than
   * hidden: it is useful evidence, but must not be mistaken for the current draft's build.
   */
  async buildResult(requestId, { expectedSourceCommit = null } = {}) {
    const id = questRequestId(requestId);
    let result;
    try {
      result = validateBuildResult(await this.github.json(questResultPath(id), questBranch(id)), id);
    } catch (e) {
      if (e instanceof GithubError && e.status === 404) return null;
      throw e;
    }
    const actual = result.provenance?.sourceRevision ?? null;
    return { result, stale: !!expectedSourceCommit && actual !== expectedSourceCommit };
  }

  async generatedManifest(requestId, buildResult) {
    const id = questRequestId(requestId);
    const result = validateBuildResult(buildResult, id);
    const path = result.generated?.manifestPath;
    const expectedPrefix = `${QUEST_STUDIO.buildRoot}/${id}/`;
    if (typeof path !== "string" || !path.startsWith(expectedPrefix) || !path.endsWith(".json")) {
      throw new GithubError("Quest Studio result does not contain a safe generated manifest path");
    }
    return this.github.text(path, questBranch(id));
  }
}
