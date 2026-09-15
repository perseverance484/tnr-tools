import test from "node:test";
import assert from "node:assert/strict";
import { JSDOM } from "jsdom";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { MemoryStorage } from "./shim.mjs";
import { h } from "../src/ui/dom.mjs";

const REPO = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
import {
  QuestStudioWorkspace,
  missionDraftProblems,
  missionSourceFromDraft,
  newMissionDraft,
} from "../src/studio/ui.mjs";

function setupDom() {
  const jsdom = new JSDOM("<!doctype html><html><head></head><body></body></html>", { url: "https://www.theninja-rpg.com/" });
  const win = jsdom.window;
  for (const [k, v] of Object.entries({ document: win.document, window: win, navigator: win.navigator, HTMLElement: win.HTMLElement })) {
    Object.defineProperty(globalThis, k, { value: v, configurable: true, writable: true });
  }
  return win;
}

function fakeApp(win, storage = new MemoryStorage()) {
  const root = win.document.createElement("div");
  root.className = "f-app";
  const top = win.document.createElement("header");
  top.className = "f-top";
  const ver = win.document.createElement("span");
  ver.className = "f-ver";
  ver.textContent = "test";
  top.appendChild(ver);
  root.appendChild(top);
  win.document.body.appendChild(root);
  return {
    root,
    $top: top,
    storage,
    now: () => 1_800_000_000_000,
    confirm: (_message, fn) => fn(),
    showExport: (text, title) => { root.dataset.exportText = text; root.dataset.exportTitle = title; },
  };
}

function repositoryStub({ result = null, profiles: profileOverride = null } = {}) {
  const calls = [];
  const registry = {
    _meta: { schemaVersion: 1 },
    subtypes: {
      mission: { label: "Mission", maturity: "supported", compilerAdapter: "mission" },
      battle_pyramid: { label: "Battle Pyramid", maturity: "needs_recipe", compilerAdapter: null },
    },
  };
  const profiles = profileOverride ?? {
    ranks: {
      D: { shape: { objective_count: 4, battle_nodes: 0 } },
      D_combat: { shape: { objective_count: 4, battle_nodes: 1 } },
    },
  };
  return {
    calls,
    async registry() { calls.push(["registry"]); return registry; },
    async missionProfiles() { calls.push(["profiles"]); return profiles; },
    async submit(source) { calls.push(["submit", source]); return { sourceCommit: "a".repeat(40), requestId: source.requestId }; },
    async buildResult(id, opts) {
      calls.push(["result", id, opts]);
      return result ? { result, stale: false } : null;
    },
    async generatedManifest() { return '{"items":[]}'; },
  };
}

test("mission draft compiles human storyboard beats into Quest Source without raw payload authoring", () => {
  const draft = newMissionDraft(1_800_000_000_000);
  draft.profile = "D";
  draft.name = "Quiet Courier";
  draft.description = "Carry a sealed note through the village.";
  draft.successDescription = "The note reaches its recipient.";
  draft.beats = [
    { description: "Accept the sealed note.", choiceText: "Take it" },
    { description: "Confirm the delivery address.", choiceText: "Continue" },
    { description: "Hand over the note.", choiceText: "Deliver" },
  ];
  const source = missionSourceFromDraft(draft);
  assert.equal(source.kind, "quest");
  assert.equal(source.subtype, "mission");
  assert.equal(source.content.rank, "D");
  assert.equal(source.content.objectives.length, 4);
  assert.deepEqual(source.content.objectives[0].nextObjectiveId, [{ text: "Take it", nextObjectiveId: "n2" }]);
  assert.equal(source.content.objectives[3].task, "win_quest");
});

test("mission draft readiness uses repository profile shape and refuses combat profile in the foundation UI", () => {
  const profiles = { ranks: {
    D: { shape: { objective_count: 4, battle_nodes: 0 } },
    D_combat: { shape: { objective_count: 4, battle_nodes: 1 } },
  } };
  const draft = newMissionDraft();
  Object.assign(draft, {
    profile: "D", name: "X", description: "Y", successDescription: "Z",
    beats: [{ description: "1" }, { description: "2" }, { description: "3" }],
  });
  assert.deepEqual(missionDraftProblems(draft, profiles), []);
  draft.profile = "D_combat";
  assert.match(missionDraftProblems(draft, profiles).join(" "), /Encounter editor/);
  draft.profile = "D";
  draft.beats.pop();
  assert.match(missionDraftProblems(draft, profiles).join(" "), /profile owns an objective count of 4/);
});

test("Quest Studio home is one workspace: supported Mission opens, unsupported Battle Pyramid is honest", async () => {
  const win = setupDom();
  const app = fakeApp(win);
  const repository = repositoryStub();
  const studio = new QuestStudioWorkspace({ app, repository, pollMs: 0, maxPolls: 1 }).install();
  assert.equal(app.$top.querySelector(".qs-launch")?.textContent, "Quest Studio");
  await studio.open();
  const text = studio.shell.textContent;
  assert.match(text, /Mission/);
  assert.match(text, /Battle Pyramid/);
  const cards = [...studio.shell.querySelectorAll(".qs-card")];
  const pyramid = cards.find((c) => c.dataset.subtype === "battle_pyramid");
  assert.ok(pyramid.querySelector("button").disabled);
  assert.match(pyramid.textContent, /Adapter pending/);
  const mission = cards.find((c) => c.dataset.subtype === "mission");
  assert.equal(mission.querySelector("button").disabled, false);
  mission.querySelector("button").click();
  await new Promise((resolve) => setTimeout(resolve, 0));
  assert.match(studio.shell.textContent, /Mission profile/);
  const options = [...studio.shell.querySelectorAll("select option")];
  assert.equal(options.find((o) => o.value === "D_combat").disabled, true);
});

test("Mission rerender restores multiline prose through textarea value properties", async () => {
  const win = setupDom();
  const app = fakeApp(win);
  const repository = repositoryStub();
  const studio = new QuestStudioWorkspace({ app, repository, pollMs: 0, maxPolls: 1 }).install();
  await studio.open();
  studio.draft = {
    version: 1, requestId: "quest-multiline", subtype: "mission", profile: "D",
    name: "Quiet Courier",
    description: "Carry the sealed note.\nDo not break the wax.",
    successDescription: "The courier arrives.\nThe seal is intact.",
    beats: [
      { description: "Take the note.\nCheck the seal.", choiceText: "Take it" },
      { description: "Cross the village.\nAvoid delay.", choiceText: "Continue" },
      { description: "Deliver the note.\nWait for receipt.", choiceText: "Deliver" },
    ],
    updatedAt: new Date().toISOString(), sourceCommit: null, lastResult: null,
  };

  await studio.openMission(false);
  let values = [...studio.shell.querySelectorAll("textarea")].map((x) => x.value);
  assert.deepEqual(values, [
    "Carry the sealed note.\nDo not break the wax.",
    "The courier arrives.\nThe seal is intact.",
    "Take the note.\nCheck the seal.",
    "Cross the village.\nAvoid delay.",
    "Deliver the note.\nWait for receipt.",
  ]);

  studio.renderMission();
  values = [...studio.shell.querySelectorAll("textarea")].map((x) => x.value);
  assert.deepEqual(values, [
    "Carry the sealed note.\nDo not break the wax.",
    "The courier arrives.\nThe seal is intact.",
    "Take the note.\nCheck the seal.",
    "Cross the village.\nAvoid delay.",
    "Deliver the note.\nWait for receipt.",
  ]);
});

test("Mission compile submits Quest Source, reads canonical result, and never presents compile as live execution", async () => {
  const win = setupDom();
  const app = fakeApp(win);
  const buildResult = {
    schemaVersion: 1,
    kind: "quest-build",
    requestId: "quest-fixed",
    subtype: "mission",
    status: "valid",
    resolvedEngineType: "mission",
    blockers: [], errors: [], warnings: [],
    generated: { manifestPath: "studio/builds/quest-fixed/manifest.json", entities: { counts: { quest: 1 }, creates: 1, updates: 0 } },
    art: { shots: [] },
    validation: { ok: true },
    provenance: { sourceRevision: "a".repeat(40), compilerRevision: "b".repeat(40) },
    liveGameTouched: false,
  };
  const repository = repositoryStub({ result: buildResult });
  const studio = new QuestStudioWorkspace({ app, repository, pollMs: 0, maxPolls: 1 }).install();
  await studio.open();
  studio.draft = {
    version: 1, requestId: "quest-fixed", subtype: "mission", profile: "D",
    name: "Quiet Courier", description: "Carry the note.", successDescription: "Delivered.",
    beats: [
      { description: "Accept it.", choiceText: "Take it" },
      { description: "Check the address.", choiceText: "Continue" },
      { description: "Deliver it.", choiceText: "Deliver" },
    ],
    updatedAt: new Date().toISOString(), sourceCommit: null, lastResult: null,
  };
  await studio.openMission(false);
  await studio.compileMission();
  const submit = repository.calls.find((x) => x[0] === "submit");
  assert.ok(submit);
  assert.equal(submit[1].content.name, "Quiet Courier");
  assert.equal(studio.buildState.result.status, "valid");
  assert.match(studio.shell.textContent, /Mechanically valid/);
  assert.match(studio.shell.textContent, /Live game untouched/);
  assert.doesNotMatch(studio.shell.textContent, /Start live write|Publish now/);
});

test("real Mission profile sentinels render as awaiting ruling and block compile", async () => {

test("editing a submitted Mission invalidates persisted build identity before reopen", async () => {
  const win = setupDom();
  const storage = new MemoryStorage();
  const app = fakeApp(win, storage);
  const result = {
    schemaVersion: 1, kind: "quest-build", requestId: "quest-edit-stale", subtype: "mission",
    status: "valid", blockers: [], errors: [], warnings: [],
    generated: { manifestPath: "studio/builds/quest-edit-stale/manifest.json", entities: { counts: { quest: 1 } } },
    provenance: { sourceRevision: "a".repeat(40), compilerRevision: "b".repeat(40) },
    liveGameTouched: false,
  };
  const repository = repositoryStub({ result });
  const studio = new QuestStudioWorkspace({ app, repository, pollMs: 0, maxPolls: 1 }).install();
  await studio.open();
  studio.draft = {
    version: 1, requestId: "quest-edit-stale", subtype: "mission", profile: "D",
    name: "Before edit", description: "Carry the note.", successDescription: "Delivered.",
    beats: [
      { description: "Accept it.", choiceText: "Take it" },
      { description: "Check it.", choiceText: "Continue" },
      { description: "Deliver it.", choiceText: "Deliver" },
    ],
    updatedAt: new Date().toISOString(), sourceCommit: null, lastResult: null,
  };
  await studio.openMission(false);
  await studio.compileMission();
  assert.equal(studio.draft.sourceCommit, "a".repeat(40));

  const name = studio.shell.querySelector('input[type="text"]');
  name.value = "After edit";
  name.dispatchEvent(new win.Event("input", { bubbles: true }));
  assert.equal(studio.draft.sourceCommit, null);
  assert.equal(studio.draft.lastResult, null);

  const resultCalls = repository.calls.filter((x) => x[0] === "result").length;
  const reopened = new QuestStudioWorkspace({ app: fakeApp(win, storage), repository, pollMs: 0, maxPolls: 1 }).install();
  assert.equal(reopened.draft.sourceCommit, null);
  await reopened.open();
  await reopened.openMission(false);
  assert.equal(repository.calls.filter((x) => x[0] === "result").length, resultCalls);
  assert.match(reopened.shell.textContent, /No repository build has been requested for the current draft revision/);
});

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
  assert.doesNotMatch(studio.shell.textContent, /NaN|S · \? nodes|S · no combat/);
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
