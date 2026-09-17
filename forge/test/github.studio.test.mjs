import test from "node:test";
import assert from "node:assert/strict";

import { GH, Github, GithubError } from "../src/github.mjs";
import {
  QUEST_STUDIO,
  QuestStudioRepository,
  questBranch,
  questResultPath,
  questSourcePath,
  validateBuildResult,
  validateQuestSource,
} from "../src/studio/repository.mjs";

function storageWithPat(pat = "test-token") {
  return {
    getItem(key) { return key === "tnr_bk_gh_v1" ? JSON.stringify({ on: true, pat }) : null; },
    setItem() {},
  };
}

function jsonResponse(value, status = 200) {
  return new Response(JSON.stringify(value), { status, headers: { "content-type": "application/json" } });
}

test("legacy Github.put still writes main by default", async () => {
  const calls = [];
  const fetchImpl = async (url, init = {}) => {
    calls.push({ url, init });
    if ((init.method || "GET") === "GET") return new Response("", { status: 404 });
    return jsonResponse({ content: { sha: "blob", html_url: "x" }, commit: { sha: "a".repeat(40) } }, 201);
  };
  const github = new Github({ fetchImpl, storage: storageWithPat() });
  const saved = await github.put("harvests/inbox/x.json", "{}", "test");
  const put = calls.find((c) => c.init.method === "PUT");
  assert.equal(JSON.parse(put.init.body).branch, "main");
  assert.equal(saved.commitSha, "a".repeat(40));
});

test("Github.put honors an explicit Studio branch without changing GH.branch", async () => {
  const calls = [];
  const fetchImpl = async (url, init = {}) => {
    calls.push({ url, init });
    if ((init.method || "GET") === "GET") return new Response("", { status: 404 });
    return jsonResponse({ content: { sha: "blob" }, commit: { sha: "b".repeat(40) } }, 201);
  };
  const github = new Github({ fetchImpl, storage: storageWithPat() });
  await github.put("studio/requests/demo.quest.json", "{}", "test", { branch: "studio/quest/demo" });
  const put = calls.find((c) => c.init.method === "PUT");
  assert.equal(JSON.parse(put.init.body).branch, "studio/quest/demo");
  assert.equal(GH.branch, "main");
});

test("Github.ensureBranch creates from main and tolerates an already-existing branch", async () => {
  const calls = [];
  let targetExists = false;
  const fetchImpl = async (url, init = {}) => {
    calls.push({ url, init });
    if (url.includes("/branches/studio%2Fquest%2Fdemo")) {
      return targetExists ? jsonResponse({ name: "studio/quest/demo", commit: { sha: "c".repeat(40) } }) : new Response("", { status: 404 });
    }
    if (url.endsWith("/branches/main")) return jsonResponse({ name: "main", commit: { sha: "d".repeat(40) } });
    if (url.endsWith("/git/refs") && init.method === "POST") {
      targetExists = true;
      const body = JSON.parse(init.body);
      assert.deepEqual(body, { ref: "refs/heads/studio/quest/demo", sha: "d".repeat(40) });
      return jsonResponse({ object: { sha: "d".repeat(40) } }, 201);
    }
    throw new Error("unexpected fetch " + url);
  };
  const github = new Github({ fetchImpl, storage: storageWithPat() });
  const made = await github.ensureBranch("studio/quest/demo");
  assert.equal(made.created, true);
  const existing = await github.ensureBranch("studio/quest/demo");
  assert.equal(existing.created, false);
  assert.equal(calls.filter((c) => c.url.endsWith("/git/refs")).length, 1);
});



test("unsafe branch and request identifiers fail before a request is sent", async () => {
  let calls = 0;
  const github = new Github({ fetchImpl: async () => { calls += 1; return new Response("", { status: 500 }); }, storage: storageWithPat() });
  await assert.rejects(() => github.ensureBranch("../main"), GithubError);
  assert.throws(() => questBranch("../main"), GithubError);
  assert.equal(calls, 0);
});

test("QuestStudioRepository writes a fresh source revision that triggers the worker without Actions dispatch", async () => {
  const log = [];
  const github = {
    async ensureBranch(branch, base) { log.push(["branch", branch, base]); return { created: true, sha: "1".repeat(40) }; },
    async put(path, text, message, opts) { log.push(["put", path, JSON.parse(text), message, opts]); return { commitSha: "2".repeat(40) }; },
  };
  const repo = new QuestStudioRepository({ github, buildRequestId: () => "build-request-001" });
  const source = {
    schemaVersion: 1,
    kind: "quest",
    requestId: "demo-mission",
    subtype: "mission",
    content: { rank: "D", name: "Demo" },
    meta: { authoredIn: "test" },
  };
  const submitted = await repo.submit(source);
  assert.equal(submitted.branch, "studio/quest/demo-mission");
  assert.equal(submitted.sourcePath, "studio/requests/demo-mission.quest.json");
  assert.equal(submitted.sourceCommit, "2".repeat(40));
  assert.deepEqual(log[0], ["branch", "studio/quest/demo-mission", "main"]);
  assert.equal(log.length, 2);
  assert.equal(log[1][0], "put");
  assert.equal(log[1][1], "studio/requests/demo-mission.quest.json");
  assert.equal(log[1][2].meta.authoredIn, "test");
  assert.equal(log[1][2].meta.repositoryBuildRequestId, "build-request-001");
  assert.equal(log[1][4].branch, "studio/quest/demo-mission");
  assert.equal(source.meta.repositoryBuildRequestId, undefined);
});

test("QuestStudioRepository changes repository build-request metadata on every compile request", async () => {
  const written = [];
  let n = 0;
  const github = {
    async ensureBranch() { return { created: false, sha: "1".repeat(40) }; },
    async put(_path, text) { written.push(JSON.parse(text)); return { commitSha: String(++n).padStart(40, "0") }; },
  };
  const tokens = ["build-a", "build-b"];
  const repo = new QuestStudioRepository({ github, buildRequestId: () => tokens.shift() });
  const source = { schemaVersion: 1, kind: "quest", requestId: "demo-retry", subtype: "mission", content: {} };
  await repo.submit(source);
  await repo.submit(source);
  assert.equal(written[0].meta.repositoryBuildRequestId, "build-a");
  assert.equal(written[1].meta.repositoryBuildRequestId, "build-b");
  assert.notDeepEqual(written[0], written[1]);
});

test("QuestStudioRepository refuses build reads without an exact submitted source identity", async () => {
  const repo = new QuestStudioRepository({ github: { async json() { throw new Error("must not read"); } } });
  await assert.rejects(() => repo.buildResult("demo-mission"), /requires the exact submitted source commit/);
});

test("QuestStudioRepository marks an older persisted result stale", async () => {
  const result = {
    schemaVersion: 1,
    kind: "quest-build",
    requestId: "demo-mission",
    subtype: "mission",
    status: "blocked",
    liveGameTouched: false,
    provenance: { sourceRevision: "3".repeat(40) },
  };
  const github = { async json(path, ref) {
    assert.equal(path, questResultPath("demo-mission"));
    assert.equal(ref, questBranch("demo-mission"));
    return result;
  } };
  const repo = new QuestStudioRepository({ github });
  const got = await repo.buildResult("demo-mission", { expectedSourceCommit: "4".repeat(40) });
  assert.equal(got.stale, true);
  assert.equal(got.result.status, "blocked");
});

test("Quest Studio refuses a result that claims repository compilation touched the live game", () => {
  assert.throws(() => validateBuildResult({
    schemaVersion: 1,
    kind: "quest-build",
    requestId: "demo-mission",
    status: "valid",
    liveGameTouched: true,
  }, "demo-mission"), /liveGameTouched:false/);
});

test("generated manifest reads cannot escape the request build directory", async () => {
  let reads = 0;
  const github = { async text() { reads += 1; return "{}"; } };
  const repo = new QuestStudioRepository({ github });
  const base = {
    schemaVersion: 1,
    kind: "quest-build",
    requestId: "demo-mission",
    subtype: "mission",
    status: "valid",
    liveGameTouched: false,
    generated: {},
  };
  for (const path of [
    "studio/builds/demo-mission/../other/manifest.json",
    "studio/builds/demo-mission/./manifest.json",
    "studio/builds/demo-mission//manifest.json",
    "studio/builds/demo-mission/..\\other\\manifest.json",
    "studio/builds/demo-mission/..%2f..%2fpush%2f46.json",
    "studio/builds/demo-mission/%2e%2e/%2e%2e/push/46.json",
    "studio/builds/demo-mission/a?ref=main&x=.json",
  ]) {
    await assert.rejects(() => repo.generatedManifest("demo-mission", { ...base, generated: { manifestPath: path } }), GithubError);
  }
  assert.equal(reads, 0);

  const ok = { ...base, generated: {
    manifestPath: "studio/builds/demo-mission/manifest.json",
    manifestSha256: "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
  } };
  await repo.generatedManifest("demo-mission", ok);
  assert.equal(reads, 1);

  await assert.rejects(() => repo.generatedManifest("demo-mission", {
    ...base,
    generated: {
      manifestPath: "studio/builds/demo-mission/manifest.json",
      manifestSha256: "0".repeat(64),
    },
  }), /does not match the compiler result digest/);
  assert.equal(reads, 2);
});

test("Quest Source validation preserves repository-owned subtype policy", () => {
  const source = validateQuestSource({
    schemaVersion: 1,
    kind: "quest",
    requestId: "demo-story",
    subtype: "story",
    content: {},
  });
  assert.equal(source.subtype, "story");
  assert.equal(questSourcePath(source.requestId), "studio/requests/demo-story.quest.json");
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
  assert.match(seen, /a%3Fref%3Dmain%23x\.json\?ref=studio%2Fquest%2Fdemo$/);
  assert.doesNotMatch(seen, /\/a\?ref=main/);
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
