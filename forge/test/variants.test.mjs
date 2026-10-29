// Item variants and variant tokens (RUL-2026-10-29-047), and the dungeon drop's onlyOnce flag.
// Socket-free: the game is FakeGame, whose item.getItemVariants / item.upsertItemVariant routes mirror
// routers/item.ts at studie-tech/TheNinjaRPG@3314d122 and are written independently of
// src/runner/variants.mjs.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";
import { recipe, mergeForUpdate, updateInput } from "../src/runner/recipes.mjs";
import { Validator } from "../src/runner/validate.mjs";
import { HIDDENLESS } from "../src/runner/catalog.mjs";
import { variantProblems, MAX_VARIANTS } from "../src/runner/variants.mjs";
import { dungeonProblems, CONTRACT as DUNGEON } from "../src/dungeon/validate.mjs";
import { PROCEDURES, isProtected } from "../src/transport/procedures.mjs";
import { checkManifest } from "../tools/check_manifest.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const FIX = fileURLToPath(new URL("./fixtures/variants/", import.meta.url));
const fixture = (name) => JSON.parse(readFileSync(join(FIX, name), "utf8"));
const FIELDS = JSON.parse(readFileSync(new URL("../src/runner/fields.json", import.meta.url), "utf8"));
const NESTED = JSON.parse(readFileSync(new URL("../src/runner/nested.json", import.meta.url), "utf8"));
const harness = (opts = {}) => composeForTest({ game: new FakeGame(), storage: new MemoryStorage(), idb: new IDBFactory(), ...opts });
const BASE = "trophyBaseItem0000001";
const VARIANT = () => structuredClone(fixture("variant_create.json").items[1].data);
const seedBase = (game) => game.seed("item", { id: BASE, name: "Fixture Blade", itemType: "WEAPON", hidden: false, effects: [], createdAt: new Date(0), updatedAt: new Date(0) });
// one variant create on the seeded item, no token: the shape the crash tests need (warned, not refused)
const solo = (data = {}) => ({ items: [{ entity: "itemVariant", slot: "create", name: "Solo Trophy", srcId: "fx_solo",
  data: { itemId: BASE, name: "Solo Trophy", image: "https://utfs.io/f/solo.webp", costType: "VARIANT_TOKEN", cost: 0, order: 1, hidden: true, ...data } }] });

// ------------------------------------------------------------------ contract
test("contract: the variant field set, procedures, refs and the new nested keys at the 3314d122 pin", () => {
  assert.equal(FIELDS._provenance.pin, "3314d122c93e036618483d18229a793ad7ad21fd");
  assert.deepEqual([FIELDS.entities.itemVariant.source, Object.keys(FIELDS.entities.itemVariant.fields)], ["app/src/validators/item.ts:92",
    ["id", "name", "image", "requiredItemId", "costType", "cost", "order", "description", "battleDescription", "furnitureData"]]);
  for (const p of ["item.getItemVariants", "item.upsertItemVariant"]) assert.deepEqual([isProtected(p), PROCEDURES[p].limited], [true, false], p);
  assert.ok(HIDDENLESS.includes("itemVariant"));
  assert.ok(NESTED.sets[NESTED.effects.unlockitemvariant].includes("variantId"));
  assert.deepEqual(DUNGEON.dropFlags, ["onlyOnce"]);
  const rc = recipe("itemVariant");
  assert.deepEqual([rc.create.path, rc.update, rc.get, rc.oneStep, rc.names], ["item.upsertItemVariant", "item.upsertItemVariant", "item.getItemVariants", true, undefined]);
});

test("contract: the hand-held variant facts still match the pinned source, when a checkout is supplied", { skip: !process.env.TNR_GAME_CHECKOUT && "set TNR_GAME_CHECKOUT to a checkout at 3314d122" }, () => {
  const root = process.env.TNR_GAME_CHECKOUT;
  const read = (f) => readFileSync(join(root, f), "utf8");
  assert.match(read("app/drizzle/constants.ts"), new RegExp(`export const MAX_ITEM_VARIANTS = ${MAX_VARIANTS};`));
  const schema = read("app/drizzle/schema.ts");
  const t = schema.slice(schema.indexOf('mysqlTable(\n  "ItemVariant"'), schema.indexOf("export type ItemVariant ="));
  assert.ok(t.length > 100 && !/\bhidden\s*:/.test(t), "ItemVariant has no hidden column");
  assert.match(t, /name: varchar\("name", \{ length: 191 \}\)/);
  assert.match(t, /image: varchar\("image", \{ length: 512 \}\)/);
  assert.match(t, /uniqueIndex\("ItemVariant_itemId_order_key"\)\.on\(\s*table\.itemId,\s*table\.order,?\s*\)/);
  const router = read("app/src/server/api/routers/item.ts");
  assert.match(router, /\n  getItemVariants: protectedProcedure\n    \.input\(z\.object\(\{ itemId: z\.string\(\) \}\)\)/);
  assert.match(router, /\n  upsertItemVariant: protectedProcedure\n    \.input\(upsertItemVariantInputSchema\)/);
  assert.match(router, /return \{ success: true, message: "Variant saved" \};/, "the create answers no id");
  assert.match(router, /effect\.type === "unlockitemvariant" &&\s*\(!effect\.variantId \|\| effect\.variantId === input\.variant\.id\)/);
  assert.match(router, /if \(input\.variant\.requiredItemId && input\.variant\.costType !== "VARIANT_TOKEN"\)/);
  assert.match(read("app/src/validators/combat.ts"), /variantId: z\.string\(\)\.trim\(\)\.nullable\(\)\.prefault\(null\)/);
  assert.match(read("app/src/validators/dungeon.ts"), /onlyOnce: z\.boolean\(\)\.optional\(\)/);
});

// ------------------------------------------------------------------ recipe and validator
test("recipe: the create sends {itemId, variant} without id or hidden; an edit re-sends the live record and omits a stored null description", () => {
  const rc = recipe("itemVariant");
  const input = rc.create.input({ ...VARIANT(), requiredItemId: "tok" });
  assert.deepEqual(Object.keys(input), ["itemId", "variant"]);
  assert.ok(!("hidden" in input.variant) && !("id" in input.variant) && !("itemId" in input.variant));
  const live = { id: "v1", itemId: BASE, name: "Old", image: "https://utfs.io/f/a.webp", requiredItemId: null, costType: "VARIANT_TOKEN", cost: 0, order: 2,
    description: null, battleDescription: "Flash", furnitureData: null, createdAt: new Date(0), updatedAt: new Date(0) };
  const v = new Validator(FIELDS, NESTED);
  const merged = mergeForUpdate("itemVariant", live, { itemId: BASE, name: "New" }, v.knownFields("itemVariant"));
  const sent = updateInput(rc, "v1", merged);
  assert.equal(sent.itemId, BASE);
  assert.deepEqual(sent.variant, { id: "v1", name: "New", image: live.image, requiredItemId: null, costType: "VARIANT_TOKEN", cost: 0, order: 2, battleDescription: "Flash", furnitureData: null });
});

test("validator: ItemVariantValidator bounds and the column limits, before anything is sent", () => {
  const v = new Validator(FIELDS, NESTED);
  assert.deepEqual(v.problems("itemVariant", { ...VARIANT(), requiredItemId: null }, null, { preCreate: true }), []);
  const p = (d, o = { preCreate: true }) => v.problems("itemVariant", d, null, o).join(" | ");
  const bad = fixture("variant_bad.json").items[1].data;
  const all = p(bad);
  for (const re of [/unknown key "colour"/, /id: the variant id is the item's targetId/, /name: 1-191/, /cost: an integer/, /order: an integer 1\.\.7/,
    /description: a string/, /only a VARIANT_TOKEN variant can require/]) assert.match(all, re);
  assert.match(p({ name: "X" }), /itemId/);
  assert.match(p({ itemId: BASE, name: "x".repeat(192) }, {}), /name: 1-191/);
  assert.match(p({ itemId: BASE, image: "https://utfs.io/f/" + "a".repeat(500) }, {}), /512/);
  assert.match(p({ itemId: BASE }), /name is required/);
  assert.equal(p({ itemId: BASE, name: "Edit only" }, {}), "", "an edit needs only its itemId and the keys it changes");
  assert.deepEqual(variantProblems({ itemId: BASE, hidden: true, image: "@img:t.webp" }), []);
});

test("lints: token items, a token bound before its variant exists, (itemId, order) twins and the visibility warnings", () => {
  assert.throws(() => parseManifest(fixture("variant_bad.json")), (e) => {
    assert.ok(e instanceof ManifestError);
    for (const re of [/VARIANT variantId "not-an-id"/, /requires destroyOnUse true/, /needs an unlockitemvariant with variantId null/, /at order 3; \(itemId, order\) is unique/]) assert.match(e.message, re);
    return true;
  });
  const m = parseManifest(fixture("variant_create.json"));
  assert.deepEqual(m.warnings, []);
  assert.match(parseManifest(solo()).warnings.join(), /no requiredItemId: any token whose unlockitemvariant has no variantId/);
  assert.match(parseManifest(solo({ costType: "MONEY", cost: 10 })).warnings.join(), /no hidden switch/);
});

// ------------------------------------------------------------------ runner
test("a trophy end to end: token (variantId null), the variant requiring it, then the token bound by @variant at send time", async () => {
  const game = new FakeGame();
  seedBase(game);
  const h = harness({ game });
  h.runner.plan(fixture("variant_create.json"), { jobId: "t1" });
  const s = await h.runner.run("t1");
  assert.equal(s.counts.VERIFIED, 2, JSON.stringify(s));
  const [tokenId, variantId] = h.journal.get("t1").items.map((it) => it.entityId);
  const row = game.rows("itemVariant")[0];
  assert.deepEqual([game.count("itemVariant"), row.id, row.requiredItemId, row.itemId, row.order], [1, variantId, tokenId, BASE, 2]);
  assert.equal(game.calls.filter((c) => c.path === "item.upsertItemVariant").length, 1);
  // step 2, a later manifest: the token's variantId names the variant by ref, resolved from the idmap
  const bind = { items: [{ entity: "item", slot: "edit", name: "Fixture Trophy Token", targetId: tokenId, data: {
    effects: [{ ...fixture("variant_create.json").items[0].data.effects[0], variantId: "@variant:fx_trophy" }] } }] };
  h.runner.plan(bind, { jobId: "t2" });
  const s2 = await h.runner.run("t2");
  assert.equal(s2.counts.VERIFIED, 1, JSON.stringify(s2));
  assert.equal(game.tables.item.get(tokenId).effects[0].variantId, variantId, "the ref was resolved before the send");
  // and a later variant edit still satisfies the server's check against the now-bound token
  h.runner.plan({ items: [{ entity: "itemVariant", slot: "edit", name: "Fixture Trophy", targetId: variantId, data: { itemId: BASE, battleDescription: "It gleams." } }] }, { jobId: "t3" });
  const s3 = await h.runner.run("t3");
  assert.equal(s3.counts.VERIFIED, 1, JSON.stringify(s3));
  assert.deepEqual([game.rows("itemVariant")[0].battleDescription, game.rows("itemVariant")[0].description], ["It gleams.", "A fixture trophy look."]);
});

test("pre-create read: a taken order or a full item fails the item with nothing sent", async () => {
  for (const [rows, re] of [[[{ order: 1, name: "Taken" }], /order 1 is already used by "Taken"/], [[1, 2, 3, 4, 5, 6, 7].map((order) => ({ order, name: "V" + order })), /already has 7 variants/]]) {
    const game = new FakeGame();
    seedBase(game);
    rows.forEach((r, i) => game.seed("itemVariant", { id: "seededVariant0000000" + i, itemId: BASE, image: "x", costType: "MONEY", cost: 1, ...r }));
    const h = harness({ game });
    h.runner.plan(solo(), { jobId: "p" });
    const s = await h.runner.run("p");
    assert.equal(s.items[0].state, "FAILED");
    assert.match(s.items[0].error, re);
    assert.equal(game.calls.filter((c) => c.path === "item.upsertItemVariant").length, 0);
  }
});

test("a refused upsert is FAILED and never resent; a malformed one is refused before it is sent", async () => {
  const game = new FakeGame();
  seedBase(game);
  game.refuse.add("item.upsertItemVariant");
  const h = harness({ game });
  h.runner.plan(solo(), { jobId: "r" });
  const s = await h.runner.run("r");
  assert.deepEqual([s.items[0].state, game.count("itemVariant")], ["FAILED", 0]);
  assert.match(s.items[0].error, /create refused: Not allowed/);
  const g2 = new FakeGame(); seedBase(g2);
  const h2 = harness({ game: g2 });
  h2.runner.plan(solo({ order: 9 }), { jobId: "r2" });
  const s2 = await h2.runner.run("r2");
  assert.match(s2.items[0].error, /order: an integer 1\.\.7/);
  assert.equal(g2.calls.length, 0);
});

test("CRASH after the upsert is applied: ORPHANED with the row at the planned order as a matching candidate; adopted, read back, never re-sent", async () => {
  const game = new FakeGame({ crashAt: 2 }); // pre-create read (1), upsert applied server-side (2), tab dies
  seedBase(game);
  const h = harness({ game });
  h.runner.plan(solo(), { jobId: "c1" });
  const s0 = await h.runner.run("c1");
  assert.equal(s0.state, "PAUSED");
  assert.equal(game.count("itemVariant"), 1);
  const h2 = harness({ game, storage: h.storage.crash(), idb: h.idb });
  h2.runner.attach("c1", solo());
  await h2.runner.resume("c1");
  const it = h2.journal.get("c1").items[0];
  assert.equal(it.state, "ORPHANED");
  assert.deepEqual(it.candidates.map((c) => [c.id, c.order, c.matches]), [[game.rows("itemVariant")[0].id, 1, true]]);
  h2.runner.adopt("c1", 0, it.candidates[0].id);
  const s = await h2.runner.run("c1");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.equal(game.calls.filter((c) => c.path === "item.upsertItemVariant").length, 1, "the adopted row is not created again");
});

test("the id read after a landed create fails: the item stays SENT, then reconciles to ORPHANED; nothing is re-sent", async () => {
  const game = new FakeGame({ dropAt: 3 }); // pre-create read (1), upsert (2), the id read dies on the wire (3)
  seedBase(game);
  const h = harness({ game });
  h.runner.plan(solo(), { jobId: "d1" });
  const s0 = await h.runner.run("d1");
  assert.equal(s0.state, "PAUSED");
  assert.equal(h.journal.get("d1").items[0].state, "SENT");
  assert.deepEqual(h.journal.get("d1").items[0].variantSnapshot, []);
  await h.runner.resume("d1");
  const it = h.journal.get("d1").items[0];
  assert.equal(it.state, "ORPHANED");
  assert.equal(it.candidates.length, 1);
  assert.equal(game.calls.filter((c) => c.path === "item.upsertItemVariant").length, 1);
});

test("a row at the planned order that does not hold the plan is ORPHANED, not claimed", async () => {
  const game = new FakeGame();
  seedBase(game);
  // the server stores what it was sent; make the stored name differ from the plan, as a concurrent edit would
  const orig = game.itemVariant;
  game.itemVariant = function (proc, input, ok, err) {
    const r = orig.call(this, proc, input, ok, err);
    if (proc === "upsertItemVariant") for (const v of this.tables.itemVariant.values()) v.name = "Someone else's";
    return r;
  };
  const h = harness({ game });
  h.runner.plan(solo(), { jobId: "o1" });
  const s = await h.runner.run("o1");
  assert.equal(s.pause?.reason, "ORPHANED");
  const it = h.journal.get("o1").items[0];
  assert.deepEqual([it.state, it.candidates[0].matches], ["ORPHANED", false]);
});

// ------------------------------------------------------------------ species effects and dungeon onlyOnce
test("species innate effects take skillTarget per effect (3314d122); the species-level key is gone", () => {
  const v = new Validator(FIELDS, NESTED);
  const fx = { type: "heal", power: 2, calculation: "percentage", rounds: 100, target: "SELF" };
  assert.deepEqual(v.nestedProblems("petSpecies", { effects: [{ ...fx, skillTarget: "ENEMIES" }] }), []);
  assert.match(v.nestedProblems("petSpecies", { effects: [{ ...fx, skilTarget: "SELF" }] }).join(), /unknown key "skilTarget"/);
  assert.match(v.nestedProblems("jutsu", { effects: [{ ...fx, skillTarget: "SELF" }] }).join(), /unknown key "skillTarget"/, "only a species' effects take it");
  assert.match(v.problems("petSpecies", { skillTarget: "SELF" }).join(), /unknown key "skillTarget"/);
});

test("dungeon onlyOnce: a boolean on a drop; saved and read back as sent", async () => {
  const once = JSON.parse(readFileSync(fileURLToPath(new URL("./fixtures/dungeon/onlyonce_manifest.json", import.meta.url)), "utf8"));
  const content = once.items[0].data;
  assert.deepEqual(dungeonProblems(content, null, { preCreate: true }), []);
  const bad = structuredClone(content); bad.rewards.drops[1].onlyOnce = "yes";
  assert.match(dungeonProblems(bad, null, { preCreate: true }).join(), /rewards\.drops\[1\]\.onlyOnce must be true or false/);
  const game = new FakeGame();
  game.notStaff = false;
  const h = harness({ game });
  h.runner.plan(once, { jobId: "dg" });
  const s = await h.runner.run("dg");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.equal(game.rows("dungeon")[0].content.rewards.drops[1].onlyOnce, true);
});

// ------------------------------------------------------------------ offline gates
test("check_manifest.mjs and validate.py agree on every variant fixture", () => {
  const data = fileURLToPath(new URL("../../skills/building-tnr-content/data/", import.meta.url));
  const py = (f) => { try { return { code: 0, out: execFileSync("python3", ["../scripts/validate.py", "--strict", f], { cwd: data, encoding: "utf8" }) }; } catch (e) { return { code: e.status, out: String(e.stdout) + String(e.stderr) }; } };
  const forge = (f) => { try { return checkManifest(f).problems; } catch (e) { return [e.message]; } };
  for (const good of ["variant_create.json", "variant_bind_edit.json"]) {
    const f = join(FIX, good);
    assert.deepEqual(forge(f), [], good);
    assert.equal(py(f).code, 0, good + "\n" + py(f).out);
  }
  const f = join(FIX, "variant_bad.json"), fp = forge(f).join("\n"), r = py(f);
  assert.notEqual(r.code, 0);
  for (const re of [/variantId/, /destroyOnUse/, /variantId null when this variant is created/, /order 3/]) { assert.match(fp, re, "forge"); assert.match(r.out, re, "validate.py"); }
  const dg = fileURLToPath(new URL("./fixtures/dungeon/onlyonce_manifest.json", import.meta.url));
  assert.deepEqual(forge(dg), []);
  assert.equal(py(dg).code, 0, py(dg).out);
});
