// AI creates after upstream migration 0056 (app/drizzle/migrations/0056_unified_combat_stats_masteries.sql).
//
// The live game's AI row has offence/defence and six masteries, and no preferredStat. Forge's pinned
// field set (345d18ac) predates the migration, so before this change an AI create could not set the
// combat columns at all (refused as unknown keys before the placeholder was minted), and lint L05
// demanded preferredStat, a key the live server strips and the read-back then reports as drift.
// Found while reviewing push/90's Sealwright create (docs/handoffs/GHOST_SHIP_SKYGLASS_RELEASE_MANIFEST_HANDOFF.md).
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { IDBFactory } from "fake-indexeddb";
import { Validator, AI_POST_0056_KEYS } from "../src/runner/validate.mjs";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";
import { composeForTest } from "./compose.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";

const SCHEMAS = JSON.parse(readFileSync(new URL("../src/runner/fields.json", import.meta.url), "utf8"));
const NESTED = JSON.parse(readFileSync(new URL("../src/runner/nested.json", import.meta.url), "utf8"));
const POST0056 = { rank: "JONIN", regeneration: 60, preferredGeneral1: "Speed", preferredGeneral2: "Strength" };
const STATS = { offence: 1391300, defence: 1391300, strength: 1391300, intelligence: 1391300, willpower: 1391300, speed: 1391300,
  ninjutsuMastery: 834780, genjutsuMastery: 834780, taijutsuMastery: 834780, bukijutsuMastery: 834780, bloodlineMastery: 10, sageMastery: 10 };

test("post-0056: the combat columns are accepted on an AI create, before any live row exists", () => {
  const v = new Validator(SCHEMAS, NESTED);
  assert.deepEqual([...AI_POST_0056_KEYS].sort(), ["bloodlineMastery", "bukijutsuMastery", "defence", "genjutsuMastery", "ninjutsuMastery", "offence", "sageMastery", "taijutsuMastery"]);
  assert.deepEqual(v.problems("ai", { username: "S", level: 100, statsMultiplier: 5, ...POST0056, ...STATS }, null, { preCreate: true }), []);
  // the additive list does not open the door to typos, omitted or server-owned columns
  assert.match(v.problems("ai", { username: "S", offense: 1 }, null, { preCreate: true }).join(";"), /unknown key "offense"/);
  assert.match(v.problems("ai", { username: "S", occupation: "NONE" }, null, { preCreate: true }).join(";"), /not writable on an ai/);
  // Re-pinned at 94f9d84 (post-0056): the pre-0056 per-type stats and preferredStat are gone upstream,
  // so they are refused loudly instead of being stripped silently by the server.
  assert.equal(v.knownFields("ai").size, 189);
  const old = v.problems("ai", { username: "S", ninjutsuOffence: 1, preferredStat: "Ninjutsu" }, null, { preCreate: true }).join(";");
  assert.match(old, /unknown key "ninjutsuOffence"/); assert.match(old, /unknown key "preferredStat"/);
});

test("post-0056: L05 no longer requires preferredStat on an AI create, and still requires the rest", () => {
  const without = { items: [{ entity: "ai", slot: "create", name: "S", srcId: "s", data: { username: "S", level: 100, ...POST0056 } }] };
  assert.equal(parseManifest(without).items.length, 1);
  for (const k of Object.keys(POST0056)) {
    const d = { username: "S", level: 100, ...POST0056 }; delete d[k];
    assert.throws(() => parseManifest({ items: [{ entity: "ai", slot: "create", name: "S", srcId: "s", data: d }] }),
      (e) => e instanceof ManifestError && new RegExp(`L05 AI create missing ${k}`).test(e.message));
  }
});

test("post-0056: one AI create carrying all combat columns runs create -> update -> rules -> VERIFIED", async () => {
  const game = new FakeGame();
  const h = composeForTest({ game, storage: new MemoryStorage(), idb: new IDBFactory() });
  const M = { items: [{ entity: "ai", slot: "create", name: "Sealwright", srcId: "sw", data: {
    username: "Sealwright", level: 100, statsMultiplier: 5, ...POST0056, ...STATS, jutsus: [], items: [],
    rules: [{ conditions: [], action: { type: "end_turn", description: "End turn" } }], includeDefaultRules: false } }] };
  h.runner.plan(M, { jobId: "p0056" });
  const s = await h.runner.run("p0056");
  assert.equal(s.items[0].state, "VERIFIED", JSON.stringify(s.items[0]));
  const row = game.rows("ai")[0];
  for (const [k, v] of Object.entries(STATS)) assert.equal(row[k], v, k);
  assert.ok(!("preferredStat" in row), "nothing sent a dropped column");
  assert.equal(game.calls.filter((c) => c.path === "profile.create").length, 1);
});
