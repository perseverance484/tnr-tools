// The core API/snapshot golden required by the Phase 0 contract:
// "explicit core API/snapshot golden so the UI boundary cannot silently widen".
//
// The other core suite proves the core WORKS without a DOM. This one proves the seam cannot GROW.
// The distinction matters because every widening found in review was invisible to a behaviour
// test: screens wrote a search string, a render callback and a browser-permission flag onto core
// machine state, and every test stayed green. A golden is the only thing that catches that class.
//
// Updating these goldens is allowed and is meant to be a deliberate, reviewed edit.
import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { ForgeCore, REQUIRED_DEPS, OPTIONAL_DEPS } from "../src/core/core.mjs";
import { composeForTest } from "./compose.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { FakeGame } from "./fakegame.mjs";

const ACTIONS = [
  "adopt", "blockedPaths", "changed", "clearSelection", "drive", "establishAuth", "exportJob",
  "fail", "go", "loadPicker", "notify", "recheckAuth", "requestPause", "resolveCaptures",
  "resumeBlockedReason", "resumeJob", "say", "selectManifest", "skip", "snapshot", "startJob",
  "subscribe",
];
const STATE_KEYS = ["screen", "jobId", "picker", "pickerAt", "pickerError", "selected", "running", "runningNote"];

function core() {
  const storage = new MemoryStorage();
  const clock = fakeClock();
  const d = composeForTest({ game: new FakeGame(), storage, idb: new IDBFactory(), clock });
  d.github = { list: async () => [], text: async () => "{}", put: async () => ({ sha: "s" }) };
  return new ForgeCore({ version: "contract", storage, now: clock, ...d });
}

test("the public action surface is exactly the golden", () => {
  const actual = Object.getOwnPropertyNames(ForgeCore.prototype)
    .filter((n) => n !== "constructor" && !n.startsWith("_"))
    .sort();
  assert.deepEqual(actual, [...ACTIONS].sort(),
    "the core's public actions changed; update the golden deliberately if that is intended");
  assert.deepEqual([...ForgeCore.ACTIONS].sort(), [...ACTIONS].sort(), "ForgeCore.ACTIONS drifted from the golden");
});

test("machine-state keys are exactly the golden, and snapshot() reports all of them", () => {
  const c = core();
  assert.deepEqual(Object.keys(c.state).sort(), [...STATE_KEYS].sort());
  assert.deepEqual(Object.keys(c.snapshot()).sort(), [...STATE_KEYS].sort());
  assert.deepEqual([...ForgeCore.STATE_KEYS].sort(), [...STATE_KEYS].sort());
});

test("a snapshot is JSON-serializable and carries no function, node or dependency handle", () => {
  const c = core();
  c.state.selected = { entry: { name: "x" }, plan: [{ idx: 0 }], problems: [], images: [] };
  const snap = c.snapshot();
  assert.doesNotThrow(() => JSON.stringify(snap));

  const walk = (v, path) => {
    assert.notEqual(typeof v, "function", `${path} is a function`);
    if (v && typeof v === "object") {
      assert.ok(!("nodeType" in v), `${path} looks like a DOM node`);
      assert.ok(!("appendChild" in v), `${path} looks like a DOM node`);
      for (const [k, x] of Object.entries(v)) walk(x, `${path}.${k}`);
    }
  };
  walk(snap, "snapshot");

  // and it is a copy: mutating it must not reach the core
  snap.screen = "tampered";
  assert.equal(c.state.screen, "jobs");
});

test("the dependency contract is explicit: required deps fail closed, unknown deps are ignored", () => {
  const storage = new MemoryStorage();
  const clock = fakeClock();
  const d = composeForTest({ game: new FakeGame(), storage, idb: new IDBFactory(), clock });
  d.github = { list: async () => [], text: async () => "{}", put: async () => ({ sha: "s" }) };

  for (const drop of REQUIRED_DEPS) {
    const bag = { version: "x", storage, now: clock, ...d, [drop]: undefined };
    assert.throws(() => new ForgeCore(bag), new RegExp(`missing required dependencies: .*${drop}`),
      `omitting ${drop} must fail closed`);
  }

  // repoCache specifically: it must NOT silently fall back to the game capture cache, because that
  // reverses the Phase 0 storage isolation without failing anything (independent review F1).
  assert.throws(() => new ForgeCore({ version: "x", storage, now: clock, ...d, repoCache: undefined }),
    /repoCache/, "repoCache must be required, never defaulted to the capture cache");

  const c = new ForgeCore({ version: "x", storage, now: clock, ...d, aViewHelper: () => {}, renderThing: {} });
  assert.equal(c.aViewHelper, undefined, "an unknown dependency must not be absorbed");
  assert.equal(c.renderThing, undefined, "an unknown dependency must not be absorbed");
  for (const k of REQUIRED_DEPS) assert.ok(c[k] != null, `${k} should be held`);
  assert.ok(OPTIONAL_DEPS.length > 0);
});

test("rendering every screen adds no key and no function to core machine state", async () => {
  // The regression that motivated this golden: screens wrote pickerQuery, a DOM render callback
  // and navigator.storage.persist()'s result straight onto core state.
  const { installDom, renderScenarios } = await import("./screen_scenarios.mjs");
  const { App } = await import("../src/ui/app.mjs");
  installDom();
  await renderScenarios(); // exercises all five screens across 12 states

  const storage = new MemoryStorage();
  const clock = fakeClock();
  const d = composeForTest({ game: new FakeGame(), storage, idb: new IDBFactory(), clock });
  d.github = { list: async () => [{ name: "45_a.json", path: "push/45_a.json", sha: "s", size: 1, type: "file" }], text: async () => "{\"items\":[]}", put: async () => ({ sha: "s" }) };
  const app = new App({ version: "contract", storage, now: clock, ...d });
  app.mount(globalThis.document.body);
  await app.loadPicker(true);
  app.go("manifests"); app.go("captures"); app.go("settings"); app.go("run"); app.go("jobs");

  assert.deepEqual(Object.keys(app.core.state).sort(), [...STATE_KEYS].sort(),
    "rendering added a key to core machine state");
  for (const [k, v] of Object.entries(app.core.state)) {
    assert.notEqual(typeof v, "function", `core state key ${k} holds a function after rendering`);
  }
  assert.doesNotThrow(() => JSON.stringify(app.core.snapshot()), "core state stopped being serializable after rendering");

  // the view-owned state is where those things actually went
  assert.equal(typeof app.view.renderPicker, "function", "the picker callback belongs to the view");
  assert.ok("pickerQuery" in app.view && "persisted" in app.view);
});

test("go() refuses an unknown patch key instead of minting core state", () => {
  // The residual F1 defect: go(screen, patch) was Object.assign(this.state, patch, { screen }),
  // so any shell could create a new machine-state key through the public API and neither the
  // snapshot golden nor the render test would see it.
  const c = core();
  const before = Object.keys(c.state).sort();

  for (const patch of [{ pickerQuery: "x" }, { persisted: true }, { renderPicker: () => {} }, { jobId: "ok", extra: 1 }]) {
    assert.throws(() => c.go("jobs", patch), /refuses unknown state keys/, `go() accepted ${JSON.stringify(Object.keys(patch))}`);
  }
  assert.deepEqual(Object.keys(c.state).sort(), before, "a refused go() must leave state untouched");

  // the permitted patch still works
  c.go("run", { jobId: "j-1" });
  assert.equal(c.state.screen, "run");
  assert.equal(c.state.jobId, "j-1");
  assert.deepEqual(Object.keys(c.state).sort(), before);
});

test("go() refuses an unknown screen and a non-object patch", () => {
  const c = core();
  for (const screen of ["dashboard", "", null, 42]) {
    assert.throws(() => c.go(screen), /unknown screen/, `go() accepted screen ${JSON.stringify(screen)}`);
  }
  for (const patch of [null, [], "jobId"]) {
    assert.throws(() => c.go("jobs", patch), TypeError);
  }
});

test("the view cannot write core machine state, including during mount", async () => {
  const { installDom } = await import("./screen_scenarios.mjs");
  const { App } = await import("../src/ui/app.mjs");
  installDom();
  const storage = new MemoryStorage();
  const clock = fakeClock();
  const d = composeForTest({ game: new FakeGame(), storage, idb: new IDBFactory(), clock });
  d.github = { list: async () => [], text: async () => "{}", put: async () => ({ sha: "s" }) };
  const app = new App({ version: "contract", storage, now: clock, ...d });
  app.mount(globalThis.document.body);

  assert.throws(() => { app.state.screen = "run"; }, TypeError, "a known key must not be writable from the view");
  assert.throws(() => { app.state.somethingNew = 1; }, TypeError, "a new key must not be writable from the view");
  assert.throws(() => { delete app.state.jobId; }, TypeError, "the view must not delete machine state");
  assert.throws(() => { Object.defineProperty(app.state, "x", { value: 1 }); }, TypeError);

  // reads still work, and the action path still works
  assert.equal(app.state.screen, "jobs");
  app.go("run", { jobId: "j-2" });
  assert.equal(app.state.screen, "run");
  assert.deepEqual(Object.keys(app.core.state).sort(), [...STATE_KEYS].sort());
});
