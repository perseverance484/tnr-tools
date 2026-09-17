// The five released Forge screens, each rendered from a deterministic state.
//
// This is the byte-identity net for the Phase 0 extraction. Every scenario is built from a fixed
// clock, a fixed tab id, an in-memory store and a fake game, and every identifier that would
// otherwise carry a timestamp is passed in explicitly. Nothing here reaches the network.
//
// Adding a scenario is cheap and is the right response to finding an unguarded branch. Changing an
// existing scenario is not: the fixtures exist so that a change in rendered output has to be an
// intentional, reviewed act rather than a silent side effect of moving domain logic.

import { JSDOM } from "jsdom";
import { IDBFactory } from "fake-indexeddb";
import { App } from "../src/ui/app.mjs";
import { JobsScreen, ManifestsScreen, RunScreen, CapturesScreen, SettingsScreen } from "../src/ui/screens.mjs";
import { composeForTest } from "./compose.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { FakeGame } from "./fakegame.mjs";
import { serializeScreen } from "./serialize_screen.mjs";

const MANIFEST = JSON.stringify({
  items: [
    { entity: "jutsu", slot: "create", name: "Fixture Jutsu", srcId: "fx-1", data: { name: "Fixture Jutsu", hidden: true } },
    { entity: "item", slot: "create", name: "Fixture Item", srcId: "fx-2", data: { name: "Fixture Item", hidden: true } },
  ],
});

const ENTRY = { name: "45_fixture.json", path: "push/45_fixture.json", sha: "fixturesha", size: 128, type: "file" };

// A capture-only research manifest exercising all three Phase 1 tiers plus a bounded paged walk.
// The tier a capture will land in is operator-visible BEFORE the read runs, and what a paged walk
// actually asked for is visible after it, so both are pinned byte for byte here.
const RESEARCH = JSON.stringify({
  items: [],
  capture: {
    after: [
      { proc: "gameAsset.get", input: { id: "fx-asset" }, persist: "repo-safe" },
      { proc: "quests.get", input: { id: "fx-quest" }, persist: "projected", projection: ["id", "name", "content.objectives.id"] },
      { proc: "combat.getBattleEntries", input: { battleId: "fx-battle", limit: 2 }, persist: "local-only", pages: 2 },
    ],
  },
});
const RESEARCH_ENTRY = { name: "46_research.json", path: "push/46_research.json", sha: "researchsha", size: 256, type: "file" };

export function installDom() {
  const d = new JSDOM("<!doctype html><html><head></head><body></body></html>", { url: "https://www.theninja-rpg.com/forge" });
  const win = d.window;
  win.confirm = () => true;
  win.navigator.clipboard = { writeText: async () => {} };
  for (const [k, v] of Object.entries({
    document: win.document, window: win, navigator: win.navigator, location: win.location,
    confirm: win.confirm, MutationObserver: win.MutationObserver, CSSStyleSheet: win.CSSStyleSheet,
    HTMLElement: win.HTMLElement,
  })) Object.defineProperty(globalThis, k, { value: v, configurable: true, writable: true });
  return win;
}

function buildApp({ entry = ENTRY, text = MANIFEST, seed = null } = {}) {
  const storage = new MemoryStorage();
  const clock = fakeClock();
  const game = new FakeGame();
  if (seed) seed(game);
  const d = composeForTest({ game, storage, idb: new IDBFactory(), clock });
  d.github = {
    list: async () => [entry],
    text: async () => text,
    put: async () => ({ sha: "committedsha" }),
  };
  const app = new App({ version: "fixture", storage, now: clock, ...d });
  return { app, storage, clock, game };
}

/** The records the research scenario reads, fixed so the rendered counts are deterministic. */
function seedResearch(game) {
  game.seed("asset", { id: "fx-asset", name: "Fixture Plate", type: "STATIC", image: "https://utfs.io/f/fx.webp", hidden: false });
  game.seed("quest", { id: "fx-quest", name: "Fixture Quest", rank: "B", content: { objectives: [{ id: "n1", type: "dialog" }], reward: {} } });
  game.seedBattle(
    { battleId: "fx-battle", battleType: "COMBAT", createdAt: "2026-09-10T00:00:00.000Z", attackedId: "a", defenderId: "d", attacker: {}, defender: {} },
    Array.from({ length: 3 }, (_, i) => ({ id: `fx-${i}`, battleId: "fx-battle", userId: "me", battleRound: 3 - i, battleVersion: 1 })));
}

async function selection(app) {
  await app.loadPicker(true);
  await app.selectManifest({ ...ENTRY, number: 45, text: MANIFEST, summary: null, loading: false });
  return app.state.selected;
}

/**
 * @returns {Promise<Array<{name: string, text: string}>>} canonical serialization per scenario,
 *   in a stable order.
 */
export async function renderScenarios() {
  const out = [];
  const add = (name, rendered) => out.push({ name, text: serializeScreen(rendered) });

  // ---- empty states: what the operator sees on a clean install -------------------------------
  {
    const { app } = buildApp();
    app.mount(globalThis.document.body);
    add("jobs_empty", JobsScreen(app));
    add("captures_empty", CapturesScreen(app));
    add("settings_default", SettingsScreen(app));
    add("manifests_unloaded", ManifestsScreen(app));
    add("run_no_job", RunScreen(app));  // no job selected: mount() leaves jobId null
  }

  // ---- manifests: picker loaded, and a manifest selected with its plan ------------------------
  {
    const { app } = buildApp();
    app.mount(globalThis.document.body);
    await app.loadPicker(true);
    add("manifests_loaded", ManifestsScreen(app));
    await selection(app);
    add("manifests_selected", ManifestsScreen(app));
  }

  // ---- a planned job, before anything is sent -------------------------------------------------
  {
    const { app } = buildApp();
    app.mount(globalThis.document.body);
    await selection(app);
    app.runner.plan(MANIFEST, { jobId: "fixture-job", manifestPath: ENTRY.path, manifestNumber: 45 });
    app.go("run", { jobId: "fixture-job" });
    add("run_planned", RunScreen(app));
    add("jobs_with_planned_job", JobsScreen(app));
  }

  // ---- a job driven to completion against the fake game ----------------------------------------
  {
    const { app } = buildApp();
    app.mount(globalThis.document.body);
    await selection(app);
    app.runner.plan(MANIFEST, { jobId: "fixture-done", manifestPath: ENTRY.path, manifestNumber: 45 });
    await app.runner.run("fixture-done");
    app.go("run", { jobId: "fixture-done" });
    add("run_finished", RunScreen(app));
    add("jobs_with_finished_job", JobsScreen(app));
    add("captures_after_run", CapturesScreen(app));
  }

  // ---- the Phase 1 research tiers, before and after the read ----------------------------------
  {
    const { app } = buildApp({ entry: RESEARCH_ENTRY, text: RESEARCH, seed: seedResearch });
    app.mount(globalThis.document.body);
    await app.loadPicker(true);
    await app.selectManifest({ ...RESEARCH_ENTRY, number: 46, text: RESEARCH, summary: null, loading: false });
    // what the operator is told about where each body will go, while it is still a decision
    add("manifests_selected_research", ManifestsScreen(app));
    app.runner.plan(RESEARCH, { jobId: "fixture-research", manifestPath: RESEARCH_ENTRY.path, manifestNumber: 46 });
    await app.runner.run("fixture-research");
    await app.resolveCaptures("fixture-research");
    app.go("run", { jobId: "fixture-research" });
    // ...and what it actually did, per tier and per page
    add("run_finished_research", RunScreen(app));
  }

  out.sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0));
  return out;
}
