// Pet species and PETS jutsu (RUL-2026-10-28-012). Socket-free: the game is FakeGame, whose petSpecies
// routes mirror routers/petSpecies.ts at studie-tech/TheNinjaRPG@2af4b320 and are written independently
// of src/runner/pets.mjs.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";
import { recipe, mergeForUpdate } from "../src/runner/recipes.mjs";
import { Validator, diffAsserted } from "../src/runner/validate.mjs";
import { petJutsuProblems, PET_SLOTS } from "../src/runner/pets.mjs";
import { PROCEDURES } from "../src/transport/procedures.mjs";
import { checkManifest } from "../tools/check_manifest.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const FIX = fileURLToPath(new URL("./fixtures/pets/", import.meta.url));
const fixture = (name) => JSON.parse(readFileSync(join(FIX, name), "utf8"));
const FIELDS = JSON.parse(readFileSync(new URL("../src/runner/fields.json", import.meta.url), "utf8"));
const NESTED = JSON.parse(readFileSync(new URL("../src/runner/nested.json", import.meta.url), "utf8"));
const SPECIES = () => structuredClone(fixture("species_create.json").items[0].data);
const JUTSU = () => structuredClone(fixture("pet_jutsu_create.json").items[0].data);
const harness = (opts = {}) => composeForTest({ game: new FakeGame(), storage: new MemoryStorage(), idb: new IDBFactory(), ...opts });

// ------------------------------------------------------------------ contract
test("contract: petSpecies field set and procedures at the 3314d122 pin", () => {
  assert.equal(FIELDS._provenance.pin, "3314d122c93e036618483d18229a793ad7ad21fd");
  assert.equal(FIELDS.entities.petSpecies.source, "app/src/validators/petSpecies.ts:30");
  assert.deepEqual(Object.keys(FIELDS.entities.petSpecies.fields), ["name", "description", "artDirection", "rankConcepts", "rarity", "role",
    "preferredDamageElement", "isActive", "defaultJutsuIds", "aiRules", "includeDefaultRules", "effects"]);
  // 3314d122: skillTarget left the species for each innate effect (PetSpeciesEffect = AllTags.and({skillTarget}))
  assert.deepEqual(NESTED.sets[NESTED.petSpeciesEffect], ["skillTarget"]);
  assert.ok(FIELDS.entities.jutsu.fields.requiredPetSpeciesId, "jutsu carries the species lock");
  assert.equal(FIELDS.entities.ai.source, "app/src/validators/aiInput.ts:13", "insertAiSchema moved out of drizzle/schema.ts upstream");
  for (const p of ["petSpecies.create", "petSpecies.update"]) assert.equal(PROCEDURES[p].auth, "protected", p);
  for (const p of ["petSpecies.get", "petSpecies.getAll"]) assert.deepEqual([PROCEDURES[p].auth, PROCEDURES[p].limited], ["public", true], p);
  assert.deepEqual(PET_SLOTS, { COMMON: 2, UNCOMMON: 3, RARE: 4, EPIC: 5, LEGENDARY: 6 });
});

test("contract: the hand-held pet rules still match the pinned source, when a checkout is supplied", { skip: !process.env.TNR_GAME_CHECKOUT && "set TNR_GAME_CHECKOUT to a checkout at 3314d122" }, () => {
  const root = process.env.TNR_GAME_CHECKOUT;
  const src = readFileSync(join(root, "app/src/libs/pets/abilities.ts"), "utf8");
  const set = /const activeEffects = new Set<[^>]*>\(\[([\s\S]*?)\]\)/.exec(src)[1].match(/"([^"]+)"/g).map((s) => s.slice(1, -1));
  const mine = readFileSync(fileURLToPath(new URL("../src/runner/pets.mjs", import.meta.url)), "utf8");
  const held = /const ACTIVE_EFFECTS = new Set\(\[([\s\S]*?)\]\)/.exec(mine)[1].match(/"([^"]+)"/g).map((s) => s.slice(1, -1));
  assert.deepEqual(held, set);
  const consts = readFileSync(join(root, "app/drizzle/constants.ts"), "utf8");
  const slots = /PET_ABILITY_SLOTS_BY_RARITY[^=]*=\s*\{([^}]*)\}/.exec(consts)[1];
  assert.deepEqual(Object.fromEntries([...slots.matchAll(/([A-Z]+):\s*(\d+)/g)].map((m) => [m[1], Number(m[2])])), PET_SLOTS);
});

test("recipe: one-step create carrying the whole record, hidden stripped; update is {id, data}", () => {
  const rc = recipe("petSpecies");
  assert.equal(rc.oneStep, true);
  assert.equal(rc.create.path, "petSpecies.create");
  const input = rc.create.input(SPECIES());
  assert.ok(!("hidden" in input), "species have no hidden column; the key never travels");
  assert.equal(input.isActive, false);
  assert.deepEqual([rc.get, rc.update, rc.names], ["petSpecies.get", "petSpecies.update", "petSpecies.getAll"]);
  const v = new Validator(FIELDS, NESTED);
  const live = { id: "s1", ...SPECIES(), hidden: undefined, defaultJutsuIds: [], createdAt: new Date(0), updatedAt: new Date(0) };
  const merged = mergeForUpdate("petSpecies", live, { defaultJutsuIds: ["j1"] }, v.knownFields("petSpecies"));
  assert.deepEqual(merged.effects, SPECIES().effects, "an edit re-sends the live innate skill: update re-saves the whole record");
  assert.deepEqual(merged.defaultJutsuIds, ["j1"]);
  assert.ok(!("createdAt" in merged) && !("id" in merged) && !("hidden" in merged));
});

// ------------------------------------------------------------------ validator
test("validator: a species create is checked against PetSpeciesValidator's refinements", () => {
  const v = new Validator(FIELDS, NESTED);
  assert.deepEqual(v.problems("petSpecies", SPECIES(), null, { preCreate: true }), []);
  const p = (d, live = null, o = { preCreate: true }) => v.problems("petSpecies", d, live, o).join(" | ");
  assert.match(p({ ...SPECIES(), isActive: true }), /isActive must be false on create/);
  assert.match(p({ ...SPECIES(), hidden: false }), /no hidden column/);
  assert.match(p({ ...SPECIES(), colour: "grey" }), /unknown key "colour"/);
  assert.match(p({ ...SPECIES(), defaultJutsuIds: ["a", "a"] }), /only once/);
  assert.match(p({ ...SPECIES(), rarity: "COMMON", defaultJutsuIds: ["a", "b", "c"] }), /exceed the 2 jutsu slots/);
  assert.match(p({ ...SPECIES(), effects: [{ type: "move" }] }), /empty-ground/);
  assert.match(p({ ...SPECIES(), effects: [{ type: "heal", target: "COORDINATES" }] }), /COORDINATES/);
  assert.match(p({ ...SPECIES(), aiRules: [{ conditions: [], action: { type: "end_turn" }, flat: 1 }] }), /aiRules: rules\[0\] has keys outside/);
  assert.match(p({ ...SPECIES(), aiRules: [{ conditions: [], action: { type: "end_turn", nope: 1 } }] }), /rules\[0\]\.action \(end_turn\): unknown key "nope"/);
  // an edit is judged against the live rarity when it does not assert one, and may activate the species
  assert.match(p({ defaultJutsuIds: ["a", "b", "c"] }, { rarity: "COMMON" }, {}), /exceed the 2 jutsu slots of a COMMON/);
  assert.deepEqual(v.problems("petSpecies", { isActive: true }, { rarity: "COMMON" }), []);
});

test("validator: a PETS jutsu a pet could never equip is refused; other jutsu are untouched", () => {
  assert.deepEqual(petJutsuProblems(JUTSU()), []);
  const p = (over, live) => petJutsuProblems({ ...JUTSU(), ...over }, live).join(" | ");
  assert.match(p({ jutsuWeapon: "SWORD" }), /jutsuWeapon must be NONE/);
  assert.match(p({ elementClassification: "Fire" }), /elementClassification/);
  assert.match(p({ injectableInBattle: true }), /injectableInBattle/);
  assert.match(p({ jutsuRank: "H" }), /H rank/);
  assert.match(p({ battleUsageType: "PVP" }), /PVP/);
  assert.match(p({ villageId: "v1" }), /villageId/);
  assert.match(p({ requiredNinjutsuMastery: 5 }), /requiredNinjutsuMastery/);
  assert.match(p({ actionCostPerc: 5 }), /actionCostPerc/);
  assert.match(p({ cooldown: -1 }), /cooldown/);
  assert.match(p({ effects: [] }), /no effects/);
  assert.match(p({ effects: [{ type: "stun", power: 1 }] }), /stun is not a pet effect/);
  assert.match(p({ effects: [{ type: "damage", power: 5, elements: ["Fire"] }] }), /carries elements/);
  assert.match(p({ effects: [{ type: "heal", power: 150, calculation: "percentage" }] }), /percentage power above 100/);
  assert.match(p({ effects: [{ type: "heal", power: 5, powerPerLevel: -1 }] }), /powerPerLevel/);
  // hidden is publication state, not eligibility: every create ships hidden (law 16b)
  assert.deepEqual(petJutsuProblems({ ...JUTSU(), hidden: true }), []);
  // an edit is judged over the live row
  assert.match(petJutsuProblems({ description: "x" }, { ...JUTSU(), jutsuWeapon: "SWORD" }).join(), /jutsuWeapon/);
  assert.match(petJutsuProblems({ jutsuType: "NORMAL", requiredPetSpeciesId: "s1" }).join(), /needs jutsuType PETS/);
  assert.deepEqual(petJutsuProblems({ jutsuType: "NORMAL", jutsuWeapon: "SWORD", effects: [{ type: "stun" }] }), []);
  const v = new Validator(FIELDS, NESTED);
  assert.match(v.problems("jutsu", { ...JUTSU(), jutsuWeapon: "SWORD" }, null, { preCreate: true }).join(), /never equip/);
});

test("validator: pet experience is a reward on items and quests; reward_pets only on the item tag", () => {
  const v = new Validator(FIELDS, NESTED);
  const item = fixture("pet_rewards.json").items[0].data;
  assert.deepEqual(v.problems("item", item, null, { preCreate: true }), []);
  const quest = fixture("pet_rewards.json").items[1].data;
  assert.deepEqual(v.problems("quest", quest), []);
  const bad = structuredClone(quest); bad.content.reward.reward_pets = ["s1"];
  assert.match(v.problems("quest", bad).join(), /content\.reward: unknown key "reward_pets"/);
});

test("manifest: petSpecies is an entity, @petSpecies is a ref, and the PET lints refuse what the server would", () => {
  const m = parseManifest(fixture("species_create.json"));
  assert.equal(m.items[0].entity, "petSpecies");
  assert.throws(() => parseManifest(fixture("species_defaults_same_manifest.json")), (e) => e instanceof ManifestError && /created hidden in this manifest/.test(e.message));
  assert.throws(() => parseManifest(fixture("pet_rewards_bad.json")), /at most 1 companion[\s\S]*preventBattleUsage/);
  const locked = { items: [{ entity: "jutsu", slot: "edit", name: "J", srcId: "j", targetId: "fxPetJutsu00000000001", data: { requiredPetSpeciesId: "fxPetSpecies000000009" } },
    { entity: "petSpecies", slot: "edit", name: "S", targetId: "fxPetSpecies000000001", data: { defaultJutsuIds: ["@jutsu:j"] } }] };
  assert.throws(() => parseManifest(locked), /locked to another species \(fxPetSpecies000000009\)/);
});

// ------------------------------------------------------------------ runner against the fake game
test("build order across three pushes: species create -> locked jutsu create (@petSpecies from the idmap) -> publish -> species defaults edit", async () => {
  const game = new FakeGame();
  const storage = new MemoryStorage(), idb = new IDBFactory();
  const h = harness({ game, storage, idb });
  // push 1: the species, one step, read back
  h.runner.plan(fixture("species_create.json"), { jobId: "p1" });
  let s = await h.runner.run("p1");
  assert.deepEqual(s.counts, { VERIFIED: 1 }, JSON.stringify(s));
  assert.deepEqual(game.calls.map((c) => c.path), ["petSpecies.getAll", "petSpecies.create", "petSpecies.get"]);
  assert.ok(!("hidden" in game.calls[1].input), "hidden is stripped from the create");
  const speciesId = h.journal.get("p1").items[0].entityId;
  assert.equal(game.count("petSpecies"), 1);
  assert.equal(game.rows("petSpecies")[0].isActive, false);
  // push 2: the signature jutsu, locked through the retained idmap (the results bundle's id works the same way as a literal)
  const p2 = fixture("pet_jutsu_create.json"); p2.items[0].data.requiredPetSpeciesId = "@petSpecies:fx_moth";
  h.runner.plan(p2, { jobId: "p2" });
  s = await h.runner.run("p2");
  assert.deepEqual(s.counts, { VERIFIED: 1 }, JSON.stringify(s));
  const jutsuId = h.journal.get("p2").items[0].entityId;
  const jutsu = game.tables.jutsu.get(jutsuId);
  assert.deepEqual([jutsu.requiredPetSpeciesId, jutsu.jutsuType, jutsu.hidden], [speciesId, "PETS", true]);
  // a hidden default is refused by the server, and the job says so rather than calling it verified
  const edit = (id) => ({ items: [{ entity: "petSpecies", slot: "edit", name: "Fixture Moth", targetId: speciesId, data: { defaultJutsuIds: [id] } }] });
  h.runner.plan(edit(jutsuId), { jobId: "p3a" });
  s = await h.runner.run("p3a");
  assert.equal(s.counts.FAILED, 1, JSON.stringify(s));
  assert.match(h.journal.get("p3a").items[0].error, /published, compatible PETS jutsu/);
  // the director publishes the jutsu (a user decision; simulated here), then push 3 lands
  jutsu.hidden = false;
  h.runner.plan(edit(jutsuId), { jobId: "p3" });
  s = await h.runner.run("p3");
  assert.deepEqual(s.counts, { VERIFIED: 1 }, JSON.stringify(s));
  const row = game.rows("petSpecies")[0];
  assert.deepEqual(row.defaultJutsuIds, [jutsuId]);
  assert.deepEqual(row.effects, SPECIES().effects, "the innate skill survived the fetch-merge edit");
  assert.equal(row.description, SPECIES().description);
  const upd = game.calls.filter((c) => c.path === "petSpecies.update").at(-1);
  assert.equal(upd.input.id, speciesId);
  assert.ok(upd.input.data.aiRules && upd.input.data.rarity === "RARE", "the whole record is re-sent");
});

test("the literal-id fixtures run as committed: a locked jutsu needs its species to exist", async () => {
  const game = new FakeGame();
  game.seed("petSpecies", { id: "fxPetSpecies000000001", ...SPECIES(), defaultJutsuIds: [], createdAt: new Date(0), updatedAt: new Date(0) });
  const h = harness({ game });
  h.runner.plan(fixture("pet_jutsu_create.json"), { jobId: "j1" });
  assert.deepEqual((await h.runner.run("j1")).counts, { VERIFIED: 1 });
  const g2 = new FakeGame();
  const h2 = harness({ game: g2 });
  h2.runner.plan(fixture("pet_jutsu_create.json"), { jobId: "j2" });
  const s = await h2.runner.run("j2");
  assert.equal(s.counts.FAILED, 1, "no such species: the server refuses the lock");
  assert.match(h2.journal.get("j2").items[0].error, /valid companion species/);
});

test("dedupNames: a live species of the same name fails the create before it is sent", async () => {
  const h = harness();
  h.game.seed("petSpecies", { id: "s0", ...SPECIES(), createdAt: new Date(0), updatedAt: new Date(0) });
  h.runner.plan({ dedupNames: true, ...fixture("species_create.json") }, { jobId: "n1" });
  const s = await h.runner.run("n1");
  assert.equal(s.counts.FAILED, 1);
  assert.match(h.journal.get("n1").items[0].error, /LIVE NAME COLLISION/);
  assert.equal(h.game.calls.filter((c) => c.path === "petSpecies.create").length, 0);
});

test("CRASH after the create is sent: the matching row is a candidate the operator binds; never re-sent", async () => {
  const game = new FakeGame({ crashAt: 2 }); // getAll snapshot (1), create applied server-side (2), tab dies
  const h = harness({ game });
  h.runner.plan(fixture("species_create.json"), { jobId: "c1" });
  const s0 = await h.runner.run("c1");
  assert.equal(s0.state, "PAUSED");
  assert.equal(game.count("petSpecies"), 1);
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("c1", fixture("species_create.json"));
  await h2.runner.resume("c1");
  const it = h2.journal.get("c1").items[0];
  assert.equal(it.state, "ORPHANED");
  assert.deepEqual(it.candidates.map((c) => [c.id, c.matches]), [[game.rows("petSpecies")[0].id, true]]);
  h2.runner.adopt("c1", 0, it.candidates[0].id);
  const s = await h2.runner.run("c1");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.equal(game.calls.filter((c) => c.path === "petSpecies.create").length, 1, "the adopted row is not created again");
});

test("read-back: a species whose stored record differs from the asserted keys is drift, not verified", async () => {
  const game = new FakeGame();
  const real = game.petSpecies.bind(game);
  game.petSpecies = (proc, input, ok, err) => {
    const r = real(proc, input, ok, err);
    if (proc === "create" && r.ok && r.data.success) game.tables.petSpecies.get(r.data.message).role = "SUPPORT";
    return r;
  };
  const h = harness({ game });
  h.runner.plan(fixture("species_create.json"), { jobId: "d1" });
  const s = await h.runner.run("d1");
  assert.equal(s.verify.drift, 1, JSON.stringify(s));
  assert.deepEqual(diffAsserted("petSpecies", { hidden: true, role: "HEALER" }, { role: "HEALER" }), [], "hidden is never diffed");
});

// ------------------------------------------------------------------ offline gates
test("check_manifest.mjs and validate.py agree on every pet fixture", () => {
  const data = fileURLToPath(new URL("../../skills/building-tnr-content/data/", import.meta.url));
  const py = (f) => { try { return { code: 0, out: execFileSync("python3", ["../scripts/validate.py", "--strict", f], { cwd: data, encoding: "utf8" }) }; } catch (e) { return { code: e.status, out: String(e.stdout) + String(e.stderr) }; } };
  const forge = (f) => { try { return checkManifest(f).problems; } catch (e) { return [e.message]; } };
  for (const good of ["species_create.json", "pet_jutsu_create.json", "species_defaults_edit.json", "pet_rewards.json"]) {
    const f = join(FIX, good);
    assert.deepEqual(forge(f), [], good);
    const r = py(f);
    assert.equal(r.code, 0, good + "\n" + r.out);
  }
  const expect = {
    "species_bad.json": [/isActive must be false/, /only once/, /exceed the 4/, /empty-ground/, /COORDINATES/, /unknown key .colour/],
    "pet_jutsu_bad.json": [/jutsuWeapon must be NONE/, /elementClassification/, /injectableInBattle/, /actionCostPerc/, /stun.* is not a pet effect/, /carries elements/, /needs jutsuType PETS/],
    "species_defaults_same_manifest.json": [/created hidden in this manifest/],
    "pet_rewards_bad.json": [/at most 1 companion/, /standard/, /preventBattleUsage/],
  };
  for (const [bad, res] of Object.entries(expect)) {
    const f = join(FIX, bad);
    const fp = forge(f).join("\n"), r = py(f);
    assert.notEqual(r.code, 0, bad);
    for (const re of res) { assert.match(fp, re, `forge ${bad}`); assert.match(r.out, re, `validate.py ${bad}`); }
  }
  // validate.py additionally refuses what only it checks: pet AI actions and reward_pets on a quest
  assert.match(py(join(FIX, "species_bad.json")).out, /pet AI action 'use_random_jutsu'/);
  assert.match(py(join(FIX, "pet_rewards_bad.json")).out, /reward_pets is not a quest reward/);
  assert.ok(existsSync(join(data, "45e_DATA_constants.json")));
});

// ------------------------------------------------------------------ review fixes (45b02007)
const NORMALIZABLE = () => ({ ...SPECIES(), name: " Fixture Moth ", description: " A test companion species used by the pet builder fixtures. ",
  artDirection: "   ", rankConcepts: [" first rank ", null, "", ""] });

test("review F1: a species the server normalises verifies; real drift is still drift", async () => {
  const data = NORMALIZABLE();
  assert.deepEqual(diffAsserted("petSpecies", data, { ...data, name: "Fixture Moth", description: data.description.trim(), artDirection: null, rankConcepts: ["first rank"] }), []);
  assert.deepEqual(diffAsserted("petSpecies", { rankConcepts: ["a", null, "c"] }, { rankConcepts: ["a", "", "c"] }), []);
  assert.equal(diffAsserted("petSpecies", { rankConcepts: ["first rank", "x"] }, { rankConcepts: ["first rank"] }).length, 1);
  assert.equal(diffAsserted("petSpecies", { artDirection: "grey" }, { artDirection: null }).length, 1);
  assert.equal(diffAsserted("petSpecies", { name: "Moth" }, { name: "Moth II" }).length, 1);
  const h = harness();
  h.runner.plan({ items: [{ entity: "petSpecies", slot: "create", name: "Fixture Moth", srcId: "fx_moth", data }] }, { jobId: "nz" });
  const s = await h.runner.run("nz");
  assert.deepEqual(s.counts, { VERIFIED: 1 }, JSON.stringify(s));
  assert.deepEqual(h.game.rows("petSpecies")[0].rankConcepts, ["first rank"], "the fake stores what upstream stores");
});

test("review F1: a lost normalised create is a matching candidate, still adopted only by the operator, never re-sent", async () => {
  const game = new FakeGame({ crashAt: 2 });
  const m = { items: [{ entity: "petSpecies", slot: "create", name: "Fixture Moth", srcId: "fx_moth", data: NORMALIZABLE() }] };
  const h = harness({ game });
  h.runner.plan(m, { jobId: "lc" });
  assert.equal((await h.runner.run("lc")).state, "PAUSED");
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("lc", m);
  await h2.runner.resume("lc");
  const it = h2.journal.get("lc").items[0];
  assert.equal(it.state, "ORPHANED", "never adopted automatically");
  assert.deepEqual(it.candidates.map((c) => c.matches), [true]);
  game.rows("petSpecies")[0].rankConcepts = ["someone else's rank"];
  h2.runner.adopt("lc", 0, it.candidates[0].id);
  const s = await h2.runner.run("lc");
  assert.equal(s.verify.drift, 1, "a real difference after adoption is drift: " + JSON.stringify(s));
  assert.equal(game.calls.filter((c) => c.path === "petSpecies.create").length, 1);
});

test("review F2: the companion cap counts reward_pets across every effect of the item", () => {
  const one = fixture("pet_rewards.json"); one.items = [one.items[0]];
  assert.doesNotThrow(() => parseManifest(one));
  const two = structuredClone(one); two.items[0].data.effects.push(structuredClone(two.items[0].data.effects[0]));
  assert.throws(() => parseManifest(two), /at most 1 companion \(2 across its effects\)/);
  const noPets = structuredClone(two); noPets.items[0].data.effects[1].reward_pets = [];
  assert.doesNotThrow(() => parseManifest(noPets), "a second reward effect without a pet is fine");
});
