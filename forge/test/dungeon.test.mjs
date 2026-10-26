// Dungeon recipe (state/prompt_forge_dungeon_recipe.md). Socket-free: the game is FakeGame, whose
// dungeon routes mirror routers/dungeon.ts at the pin recorded in src/dungeon/contract.json.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { dungeonProblems, CONTRACT } from "../src/dungeon/validate.mjs";
import { parseManifest, planOrder, ManifestError, MAX_DUNGEON_WRITES } from "../src/runner/manifest.mjs";
import { mergeForUpdate, recipe } from "../src/runner/recipes.mjs";
import { checkManifest } from "../tools/check_manifest.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const B = CONTRACT.bounds;
const floor = (kind, ...aiIds) => ({ kind, waves: [{ aiIds }] });
/** Two tiers, the Skyglass Wreck shape: floors, a mini-boss, more floors, the boss. */
function content(over = {}) {
  return {
    name: "Skyglass Wreck",
    description: "A downed warship on the tideline.",
    sector: 222, longitude: 12, latitude: 7,
    expiresAt: null, hidden: true, background: "ocean",
    tiers: [
      [floor("floor", "ai-1"), floor("floor", "ai-2"), floor("floor", "ai-3"), floor("floor", "ai-4"), floor("mini-boss", "ai-5")],
      [floor("floor", "ai-6"), floor("floor", "ai-7"), floor("floor", "ai-8"), floor("floor", "ai-9"), floor("boss", "ai-10")],
    ],
    rewards: { money: 5000, experience: 2000, drops: [{ type: "item", id: "chest-1", chance: 100, quantity: 1 }] },
    ...over,
  };
}
const create = (data = content(), extra = {}) => ({ items: [{ entity: "dungeon", slot: "create", name: data.name, srcId: "wreck", data, ...extra }] });
const harness = (opts = {}) => composeForTest({ game: new FakeGame(), storage: new MemoryStorage(), idb: new IDBFactory(), ...opts });

// ------------------------------------------------------------------ contract
test("contract: derived from the pin, covering every rule the validator mirrors", () => {
  assert.equal(CONTRACT._meta.pin, "107d7a86894f806a4c9cec89effef5992118a0ed");
  assert.deepEqual(CONTRACT.contentFields, ["name", "description", "structureAssetId", "structureScale", "sector", "longitude", "latitude", "expiresAt", "hidden", "background", "tiers", "rewards"]);
  assert.deepEqual(CONTRACT.dropFields, ["type", "id", "chance", "quantity", "package"]);
  assert.deepEqual(CONTRACT.floorKinds, ["floor", "mini-boss", "boss"]);
  assert.deepEqual(CONTRACT.dropTypes, ["item", "jutsu", "cache", "package"]);
  assert.equal(B.floorsPerTier, 5); assert.equal(B.maxTiers, 4); assert.equal(B.maxWaves, 5); assert.equal(B.maxMobs, 10);
  assert.equal(B.sector.max, 1943); assert.equal(B.longitude.max, 25); assert.equal(B.maxRewardAmount, 1e9);
  assert.deepEqual(CONTRACT.facts, { partySize: 3, runSeconds: 3600, inactiveRounds: 3 });
});

test("contract: tools/derive_dungeon.mjs --check against a game checkout, when one is supplied", { skip: !process.env.TNR_GAME_CHECKOUT && "set TNR_GAME_CHECKOUT to a checkout at the pin" }, () => {
  const out = execFileSync(process.execPath, [fileURLToPath(new URL("../tools/derive_dungeon.mjs", import.meta.url)), process.env.TNR_GAME_CHECKOUT, "--check"], { encoding: "utf8" });
  assert.match(out, /dungeon contract current/);
});

// ------------------------------------------------------------------ validator
test("validator: the two-tier Skyglass Wreck shape is accepted on create", () => {
  assert.deepEqual(dungeonProblems(content(), null, { preCreate: true }), []);
});

test("validator: a create must ship hidden", () => {
  assert.match(dungeonProblems(content({ hidden: false }), null, { preCreate: true }).join(), /hidden:true/);
  const { hidden: _h, ...noHidden } = content();
  assert.match(dungeonProblems(noHidden, null, { preCreate: true }).join(), /hidden:true/);
});

test("validator: floor kinds follow the server refinement (mini-boss ends each tier, boss ends the last)", () => {
  const c = content();
  c.tiers[0][4] = floor("boss", "ai-5");
  assert.match(dungeonProblems(c, null, { preCreate: true }).join(), /tiers\[0\]\[4\]\.kind must be "mini-boss"/);
  const one = content({ tiers: [[floor("floor", "a"), floor("floor", "b"), floor("floor", "c"), floor("floor", "d"), floor("mini-boss", "e")]] });
  assert.match(dungeonProblems(one, null, { preCreate: true }).join(), /tiers\[0\]\[4\]\.kind must be "boss"/);
});

test("validator: tier sizes, wave counts, enemy counts and first-wave delay", () => {
  const short = content(); short.tiers[1] = short.tiers[1].slice(0, 4);
  assert.match(dungeonProblems(short, null, { preCreate: true }).join(), /exactly 5 floors/);
  assert.match(dungeonProblems(content({ tiers: [] }), null, { preCreate: true }).join(), /1\.\.4 tiers/);
  const crowd = content(); crowd.tiers[0][0].waves[0].aiIds = Array.from({ length: 11 }, (_, i) => `x${i}`);
  assert.match(dungeonProblems(crowd, null, { preCreate: true }).join(), /1\.\.10 enemies/);
  const late = content(); late.tiers[0][1].waves[0].delayRounds = 2;
  assert.match(dungeonProblems(late, null, { preCreate: true }).join(), /first wave starts immediately/);
  const second = content(); second.tiers[0][1].waves.push({ aiIds: ["z"], delayRounds: 21 });
  assert.match(dungeonProblems(second, null, { preCreate: true }).join(), /0\.\.20/);
});

test("validator: unknown keys are refused at every level, as the server would drop them silently", () => {
  const c = content({ minLevel: 40 });
  c.tiers[0][0].boss = true;
  c.tiers[0][0].waves[0].delay = 3;
  c.rewards.ryo = 10;
  c.rewards.drops[0].odds = 5;
  const p = dungeonProblems(c, null, { preCreate: true }).join("\n");
  for (const k of ["minLevel", "boss", "delay", "ryo", "odds"]) assert.match(p, new RegExp(`unknown key "${k}"`));
});

test("validator: placement, biome, scale and expiry", () => {
  const p = (over) => dungeonProblems(content(over), null, { preCreate: true }).join();
  assert.match(p({ sector: 1944 }), /sector/);
  assert.match(p({ longitude: 26 }), /longitude/);
  assert.match(p({ latitude: -1 }), /latitude/);
  assert.match(p({ background: "lava" }), /background/);
  assert.match(p({ structureScale: 6 }), /structureScale/);
  assert.match(p({ expiresAt: "not a date" }), /expiresAt/);
  const { expiresAt: _e, ...noExpiry } = content();
  assert.match(dungeonProblems(noExpiry, null, { preCreate: true }).join(), /expiresAt is required/);
  assert.match(p({ structureAssetId: "@scene:wreck" }), /mapAsset/);
  assert.deepEqual(dungeonProblems(content({ expiresAt: "2027-01-01" }), null, { preCreate: true }), []);
});

test("validator: drops — types, ids and refs, chance, quantity, jutsu once, package payload, item bound", () => {
  const p = (drops) => dungeonProblems(content({ rewards: { drops } }), null, { preCreate: true }).join("\n");
  assert.equal(p([{ type: "item", id: "@item:chest", chance: 100 }]), "");
  assert.equal(p([{ type: "cache", id: "@item:inro", chance: 50, quantity: 2 }]), "");
  assert.equal(p([{ type: "jutsu", id: "@jutsu:art", chance: 3 }]), "");
  assert.match(p([{ type: "item", id: "@jutsu:x", chance: 1 }]), /not a @item: ref/);
  assert.match(p([{ type: "package", id: "@item:x", chance: 1 }]), /literal id/);
  assert.match(p([{ type: "chest", id: "x", chance: 1 }]), /type must be one of/);
  assert.match(p([{ type: "item", id: "x", chance: 0 }]), /chance must be 1\.\.100/);
  assert.match(p([{ type: "item", id: "x", chance: 1, quantity: 101 }]), /quantity/);
  assert.match(p([{ type: "jutsu", id: "j", chance: 1, quantity: 2 }]), /learned once/);
  assert.match(p([{ type: "package", id: "pk", chance: 1, package: { name: "x" } }]), /server copies the catalog snapshot/);
  assert.match(p(Array.from({ length: 21 }, (_, i) => ({ type: "item", id: `i${i}`, chance: 1, quantity: 100 }))), /exceeds 2000/);
  assert.match(p(Array.from({ length: 101 }, (_, i) => ({ type: "item", id: `i${i}`, chance: 1 }))), /at most 100 drops/);
  assert.match(dungeonProblems(content({ rewards: { tokens: 1.5 } }), null, { preCreate: true }).join(), /tokens/);
});

test("validator: an edit is checked against live content merged with the asserted keys", () => {
  const live = { id: "d1", content: content(), updatedAt: new Date(1) };
  assert.deepEqual(dungeonProblems({ name: "Skyglass Wreck II" }, live), []);
  assert.match(dungeonProblems({ sector: -4 }, live).join(), /sector/);
  // before the live row is known only the key surface is checkable
  assert.deepEqual(dungeonProblems({ name: "x" }, null), []);
  assert.match(dungeonProblems({ nmae: "x" }, null).join(), /unknown key "nmae"/);
});

// ------------------------------------------------------------------ manifest and recipe
test("manifest: dungeon is an entity; suggest mode refuses it; the write cap holds", () => {
  const m = parseManifest(create());
  assert.equal(m.items[0].entity, "dungeon");
  assert.equal(m.items[0].op, "create");
  assert.throws(() => parseManifest({ mode: "suggest", suggestion: { title: "Move the wreck", rationale: "A rationale that is long enough." }, items: [{ entity: "dungeon", slot: "edit", name: "W", targetId: "d1", data: { sector: 3 } }] }),
    /dungeon cannot be suggested/);
  const many = { items: Array.from({ length: MAX_DUNGEON_WRITES + 1 }, (_, i) => ({ entity: "dungeon", slot: "edit", name: `D${i}`, targetId: `d${i}`, data: { sector: 3 } })) };
  assert.throws(() => parseManifest(many), (e) => e instanceof ManifestError && /rate-limited/.test(e.message));
});

test("manifest: @ai and @item refs inside waves and drops order the plan after their creates", () => {
  const c = content();
  c.tiers[1][4].waves[0].aiIds = ["@ai:captain"];
  c.rewards.drops = [{ type: "item", id: "@item:chest", chance: 100 }];
  const m = parseManifest({ items: [
    { entity: "dungeon", slot: "create", name: c.name, srcId: "wreck", data: c },
    { entity: "item", slot: "create", name: "Chest", srcId: "chest", data: { name: "Chest", hidden: true } },
    { entity: "ai", slot: "create", name: "Captain", srcId: "captain", data: { username: "Captain", level: 100, hidden: true, rank: "JONIN", regeneration: 1, preferredGeneral1: "Strength", preferredGeneral2: "Speed" } },
  ] });
  const order = planOrder(m).map((it) => it.srcId);
  assert.ok(order.indexOf("wreck") > order.indexOf("chest") && order.indexOf("wreck") > order.indexOf("captain"), order.join());
});

test("recipe: one-step save, id from the response field, content-only update input, rows used as they come", () => {
  const rc = recipe("dungeon");
  assert.equal(rc.oneStep, true);
  assert.deepEqual(rc.create.input({ name: "x" }), { content: { name: "x" } });
  assert.equal(rc.createdId({ success: true, message: "Dungeon saved.", id: "abc" }), "abc");
  assert.deepEqual(rc.updateInput("d1", { name: "x" }), { id: "d1", content: { name: "x" } });
  const live = { id: "d1", content: content(), updatedAt: new Date(1) };
  const merged = mergeForUpdate("dungeon", live, { name: "Renamed" }, new Set(CONTRACT.contentFields));
  assert.equal(merged.name, "Renamed");
  assert.ok(!("id" in merged) && !("updatedAt" in merged), "row keys never travel inside content");
  assert.deepEqual(merged.tiers, content().tiers, "the whole live content is re-sent: save replaces it");
});

// ------------------------------------------------------------------ runner against the fake game
test("create: snapshot, save {content}, read-back through getAll; VERIFIED, exactly one row", async () => {
  const h = harness();
  h.runner.plan(create(), { jobId: "d1" });
  const s = await h.runner.run("d1");
  assert.equal(s.state, "DONE", JSON.stringify(s)); assert.deepEqual(s.counts, { VERIFIED: 1 });
  assert.equal(h.game.count("dungeon"), 1);
  assert.deepEqual(h.game.calls.map((c) => c.path), ["coop.dungeon.getAll", "coop.dungeon.save", "coop.dungeon.getAll"]);
  const save = h.game.calls.find((c) => c.path === "coop.dungeon.save");
  assert.ok(!("id" in save.input), "a create sends no id");
  const row = h.game.rows("dungeon")[0];
  assert.equal(row.content.name, "Skyglass Wreck");
  assert.equal(h.journal.get("d1").items[0].entityId, row.id);
});

test("edit: getAll -> merge -> save {id, content} carrying the whole content -> VERIFIED", async () => {
  const h = harness();
  h.game.seed("dungeon", { id: "dun-1", content: content(), updatedAt: new Date(0) });
  h.runner.plan({ items: [{ entity: "dungeon", slot: "edit", name: "W", targetId: "dun-1", data: { name: "Skyglass Wreck: Low Tide", background: "ground" } }] }, { jobId: "e1" });
  const s = await h.runner.run("e1");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  const save = h.game.calls.find((c) => c.path === "coop.dungeon.save");
  assert.equal(save.input.id, "dun-1");
  assert.equal(save.input.content.name, "Skyglass Wreck: Low Tide");
  assert.equal(save.input.content.tiers.length, 2, "untouched content travels with the edit");
  assert.ok(!("data" in save.input));
  assert.equal(h.game.rows("dungeon")[0].content.description, "A downed warship on the tideline.");
});

test("refused save (success:false) is FAILED and nothing is retried", async () => {
  const game = new FakeGame({ refuse: new Set(["coop.dungeon.save"]) });
  const h = harness({ game });
  h.runner.plan(create(), { jobId: "r1" });
  const s = await h.runner.run("r1");
  assert.equal(s.counts.FAILED, 1);
  assert.equal(game.calls.filter((c) => c.path === "coop.dungeon.save").length, 1);
});

test("pre-send validation fails locally before any save", async () => {
  const h = harness();
  const bad = content(); bad.tiers[0][4].kind = "floor";
  h.runner.plan(create(bad), { jobId: "v1" });
  const s = await h.runner.run("v1");
  assert.equal(s.counts.FAILED, 1);
  assert.equal(h.game.calls.filter((c) => c.path === "coop.dungeon.save").length, 0);
});

test("a success without a well-formed id is a contract break, not a success", async () => {
  const game = new FakeGame();
  const real = game.dungeon.bind(game);
  game.dungeon = (proc, input, ok, err) => (proc === "save" ? ok({ success: true, message: "Dungeon saved." }) : real(proc, input, ok, err));
  const h = harness({ game });
  h.runner.plan(create(), { jobId: "x1" });
  const s = await h.runner.run("x1");
  assert.notEqual(s.counts.VERIFIED, 1, JSON.stringify(s));
});

test("dedupNames: a live dungeon of the same name fails the create before it is sent", async () => {
  const h = harness();
  h.game.seed("dungeon", { id: "dun-1", content: content(), updatedAt: new Date(0) });
  h.runner.plan({ dedupNames: true, ...create() }, { jobId: "n1" });
  const s = await h.runner.run("n1");
  assert.equal(s.counts.FAILED, 1);
  assert.match(h.journal.get("n1").items[0].error, /LIVE NAME COLLISION/);
  assert.equal(h.game.calls.filter((c) => c.path === "coop.dungeon.save").length, 0);
});

test("CRASH after save sent, before response: the one matching row is a candidate the operator binds; never re-saved", async () => {
  const game = new FakeGame({ crashAt: 2 }); // getAll snapshot (1), save applied server-side (2), tab dies
  const h = harness({ game });
  h.runner.plan(create(), { jobId: "c1" });
  const s0 = await h.runner.run("c1");
  assert.equal(s0.state, "PAUSED"); assert.equal(s0.pause.reason, "AMBIGUOUS");
  assert.equal(game.count("dungeon"), 1);
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("c1", create());
  const s1 = await h2.runner.resume("c1");
  // review F2: matching content is evidence, not ownership; nothing is adopted without the operator
  const it = h2.journal.get("c1").items[0];
  assert.equal(it.state, "ORPHANED", JSON.stringify(s1));
  assert.deepEqual(it.candidates.map((c) => [c.id, c.matches]), [[game.rows("dungeon")[0].id, true]]);
  h2.runner.adopt("c1", 0, it.candidates[0].id);
  const s = await h2.runner.run("c1");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.equal(game.count("dungeon"), 1, "NEVER double-created");
  assert.equal(game.calls.filter((c) => c.path === "coop.dungeon.save").length, 1, "the adopted row is not saved again");
});

test("CRASH after save: a new row that does not match the plan is ORPHANED, never adopted", async () => {
  const game = new FakeGame({ crashAt: 2 });
  const h = harness({ game });
  h.runner.plan(create(), { jobId: "c2" });
  await h.runner.run("c2");
  // someone else edits the row between the crash and the resume
  game.rows("dungeon")[0].content.name = "Someone Else's Dungeon";
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("c2", create());
  const s = await h2.runner.resume("c2");
  assert.equal(h2.journal.get("c2").items[0].state, "ORPHANED", JSON.stringify(s));
  assert.equal(game.calls.filter((c) => c.path === "coop.dungeon.save").length, 1);
});

test("a read-only capture of coop.dungeon.getAll needs no write path", async () => {
  const h = harness();
  h.game.seed("dungeon", { id: "dun-1", content: content(), updatedAt: new Date(0) });
  h.runner.plan({ capture: { before: [{ proc: "coop.dungeon.getAll" }] } }, { jobId: "cap" });
  const s = await h.runner.run("cap");
  assert.equal(s.state, "DONE", JSON.stringify(s));
  assert.ok(h.game.calls.every((c) => c.path === "coop.dungeon.getAll"));
});

// ------------------------------------------------------------------ offline gates
test("check_manifest.mjs and validate.py both accept a dungeon manifest and refuse a broken one", () => {
  const dir = mkdtempSync(join(tmpdir(), "dungeon-"));
  const good = join(dir, "good.json"), bad = join(dir, "bad.json");
  writeFileSync(good, JSON.stringify(create()));
  const broken = content(); broken.tiers[1][4].kind = "mini-boss";
  writeFileSync(bad, JSON.stringify(create(broken)));
  assert.deepEqual(checkManifest(good).problems, []);
  assert.ok(checkManifest(bad).problems.some((p) => /must be "boss"/.test(p)));
  const data = fileURLToPath(new URL("../../skills/building-tnr-content/data/", import.meta.url));
  const py = (f) => { try { return { code: 0, out: execFileSync("python3", ["../scripts/validate.py", "--strict", f], { cwd: data, encoding: "utf8" }) }; } catch (e) { return { code: e.status, out: String(e.stdout) + String(e.stderr) }; } };
  const g = py(good);
  assert.equal(g.code, 0, g.out);
  const b = py(bad);
  assert.notEqual(b.code, 0, b.out);
  assert.match(b.out, /must be "boss"/);
});
