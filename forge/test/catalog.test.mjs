// Badges and titles. Socket-free: the game is FakeGame, whose badge/title routes mirror
// routers/badge.ts, routers/title.ts and server/utils/titleRewards.ts at
// studie-tech/TheNinjaRPG@2af4b320 and are written independently of src/runner/catalog.mjs.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";
import { recipe, mergeForUpdate } from "../src/runner/recipes.mjs";
import { Validator, diffAsserted } from "../src/runner/validate.mjs";
import { HIDDENLESS } from "../src/runner/catalog.mjs";
import { PROCEDURES } from "../src/transport/procedures.mjs";
import { checkManifest } from "../tools/check_manifest.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const FIX = fileURLToPath(new URL("./fixtures/catalog/", import.meta.url));
const fixture = (name) => JSON.parse(readFileSync(join(FIX, name), "utf8"));
const FIELDS = JSON.parse(readFileSync(new URL("../src/runner/fields.json", import.meta.url), "utf8"));
const NESTED = JSON.parse(readFileSync(new URL("../src/runner/nested.json", import.meta.url), "utf8"));
const harness = (opts = {}) => composeForTest({ game: new FakeGame(), storage: new MemoryStorage(), idb: new IDBFactory(), ...opts });
const BADGE = () => structuredClone(fixture("badge_create.json").items[0].data);
const TITLE = () => structuredClone(fixture("title_create.json").items[0].data);
const URL_UP = "https://utfs.io/f/fixture-crest";
const withImage = (h) => {
  h.runner.files.set("fixture_crest.png", new File([new Uint8Array(2048)], "fixture_crest.png", { type: "image/png" }));
  h.uploader.upload = async () => ({ ufsUrl: URL_UP });
  return h;
};

// ------------------------------------------------------------------ contract
test("contract: badge and title field sets, title effect key sets and procedures at the 2af4b320 pin", () => {
  assert.equal(FIELDS._provenance.pin, "2af4b32066c39e2868efae5dba6b339278701dca");
  assert.deepEqual([FIELDS.entities.badge.source, Object.keys(FIELDS.entities.badge.fields)], ["app/src/validators/badge.ts:3", ["name", "image", "description"]]);
  assert.deepEqual([FIELDS.entities.title.source, Object.keys(FIELDS.entities.title.fields)], ["app/src/validators/title.ts:22", ["name", "description", "effects", "archived"]]);
  const at = (i) => NESTED.sets[i];
  assert.deepEqual(at(NESTED.titleEffects.increasemastery), ["masteryTypes", "power", "type"]);
  assert.deepEqual(at(NESTED.titleEffects.increaseregeneration), ["power", "type"]);
  for (const p of ["badge.create", "badge.update", "title.create", "title.update", "title.get"]) assert.equal(PROCEDURES[p].auth, "protected", p);
  for (const p of ["badge.get", "badge.getAllNames", "title.getAllNames"]) assert.deepEqual([PROCEDURES[p].auth, PROCEDURES[p].limited], ["public", true], p);
  assert.deepEqual(HIDDENLESS, ["petSpecies", "badge", "title"]);
});

test("contract: the hand-held badge/title facts still match the pinned source, when a checkout is supplied", { skip: !process.env.TNR_GAME_CHECKOUT && "set TNR_GAME_CHECKOUT to a checkout at 2af4b320" }, () => {
  const root = process.env.TNR_GAME_CHECKOUT;
  const read = (f) => readFileSync(join(root, f), "utf8");
  const schema = read("app/drizzle/schema.ts");
  const table = (name) => { const i = schema.search(new RegExp(`mysqlTable\\(\\s*"${name}"`)); assert.ok(i > 0, name); return schema.slice(i, schema.indexOf("export const", i)); };
  for (const t of ["Badge", "Title"]) assert.ok(!/\bhidden\s*:/.test(table(t)), `${t} has no hidden column`);
  assert.match(table("Badge"), /description: varchar\("description", \{ length: 500 \}\)/);
  assert.match(table("Title"), /archived: boolean\("archived"\)\.default\(false\)/);
  const badge = read("app/src/server/api/routers/badge.ts"), title = read("app/src/server/api/routers/title.ts");
  assert.match(badge, /name: `New Badge - \$\{id\}`/);
  assert.match(title, /name: `New Title - \$\{id\}`/);
  for (const [src, proc, kind] of [[badge, "get", "public"], [badge, "getAllNames", "public"], [badge, "create", "protected"], [badge, "update", "protected"],
    [title, "get", "protected"], [title, "getAllNames", "public"], [title, "create", "protected"], [title, "update", "protected"]]) {
    assert.match(src, new RegExp(`\\n  ${proc}: ${kind}Procedure`), proc);
  }
  assert.match(read("app/src/server/utils/titleRewards.ts"), /eq\(title\.archived, false\)/);
  const mastery = /export const MasteryTypes = \[([^\]]*)\]/.exec(read("app/drizzle/constants.ts"))[1].match(/"[^"]+"/g).map((x) => JSON.parse(x));
  for (const m of mastery) assert.equal(new Validator(FIELDS, NESTED).problems("title", { effects: [{ type: "increasemastery", power: 1, masteryTypes: [m] }] }).length, 0, m);
  const listed = /needs 1\+ of (\S+)/.exec(new Validator(FIELDS, NESTED).problems("title", { effects: [{ type: "increasemastery", power: 1, masteryTypes: ["Nope"] }] }).join())[1].split("/");
  assert.deepEqual(listed.sort(), [...mastery].sort(), "the Forge MasteryTypes mirror equals constants.ts");
  assert.match(read("app/src/server/api/routers/title.ts"), /\n  getAll: protectedProcedure/);
});

test("recipe: placeholder create with no input; update {id, data} picks the validator's fields, hidden never travels", () => {
  for (const [e, path, ph] of [["badge", "badge.create", "New Badge - x"], ["title", "title.create", "New Title - x"]]) {
    const rc = recipe(e);
    assert.equal(rc.oneStep, undefined);
    assert.equal(rc.create.path, path);
    assert.equal(rc.create.input(BADGE()), undefined);
    assert.equal(rc.placeholder("x"), ph);
  }
  const v = new Validator(FIELDS, NESTED);
  const live = { id: "b1", name: "New Badge - b1", image: "https://utfs.io/f/default-avatar", description: "", createdAt: new Date(0), updatedAt: new Date(0) };
  const merged = mergeForUpdate("badge", live, { ...BADGE(), image: URL_UP }, v.knownFields("badge"));
  assert.deepEqual(merged, { name: "Fixture Crest", image: URL_UP, description: BADGE().description });
  const t = mergeForUpdate("title", { id: "t1", name: "New Title - t1", description: "", effects: [], legacyOwnerId: null, archived: false }, TITLE(), v.knownFields("title"));
  assert.deepEqual(Object.keys(t).sort(), ["archived", "description", "effects", "name"]);
});

// ------------------------------------------------------------------ validator
test("validator: badge and title creates are checked before the placeholder is minted", () => {
  const v = new Validator(FIELDS, NESTED);
  const p = (e, d, o = { preCreate: true }) => v.problems(e, d, null, o).join(" | ");
  assert.equal(p("badge", BADGE()), "");
  assert.equal(p("title", TITLE()), "");
  assert.match(p("badge", { ...BADGE(), hidden: false }), /no hidden column/);
  assert.match(p("badge", { ...BADGE(), image: undefined }), /image is required on a badge create/);
  assert.match(p("badge", { ...BADGE(), description: "x".repeat(501) }), /Badge column holds 500/);
  // zod bounds refuse only at the update, after a listed placeholder exists: checked before the create
  assert.match(p("badge", { ...BADGE(), description: "" }), /description: 1-500/);
  assert.match(p("badge", { ...BADGE(), name: "  " }), /name: 1-191/);
  assert.match(p("badge", { ...BADGE(), image: "crest.png" }), /image: an @img ref or a URL/);
  assert.match(p("badge", { ...BADGE(), image: "https://utfs.io/f/" + "x".repeat(180) }), /at most 191/);
  // review F1: z.url() is a parse, not a shape; F2: the validators trim names, so padding reads back as drift
  for (const bad of ["https://[", "https://exa mple.com/a.png", "https://"]) assert.match(p("badge", { ...BADGE(), image: bad }), /image: an @img ref or a URL/, bad);
  for (const e of ["badge", "title"]) for (const bad of [" Crest", "Crest ", "Crest\n"]) assert.match(p(e, { ...(e === "badge" ? BADGE() : TITLE()), name: bad }), /no leading or trailing whitespace/, bad);
  assert.match(p("badge", { name: " Crest " }, {}), /no leading or trailing whitespace/, "an edit too");
  assert.match(p("title", { ...TITLE(), description: "x".repeat(513) }), /at most 512/);
  assert.match(p("title", { ...TITLE(), effects: Array(21).fill({ type: "increaseregeneration", power: 1 }) }), /at most 20/);
  assert.match(p("title", { ...TITLE(), effects: [{ type: "increaseregeneration", power: -1 }] }), /power must be a finite number >= 0/);
  assert.match(p("title", { ...TITLE(), effects: [{ type: "increasemastery", power: 1, masteryTypes: ["Kenjutsu"] }] }), /masteryTypes needs 1\+/);
  assert.equal(p("title", { ...TITLE(), effects: [{ type: "increasemastery", power: 0, masteryTypes: ["Sage", "Bloodline"] }] }), "");
  assert.equal(p("badge", { ...BADGE(), description: "x".repeat(500) }), "");
  assert.match(p("badge", { ...BADGE(), icon: "x" }), /unknown key "icon"/);
  assert.equal(p("badge", { description: "edit" }, {}), "", "an edit needs only the keys it changes");
  assert.match(p("title", { ...TITLE(), archived: undefined }), /archived is required on a title create/);
  assert.match(p("title", { ...TITLE(), archived: "no" }), /archived must be a boolean/);
  assert.match(p("title", { ...TITLE(), effects: [{ type: "increaseregeneration", power: 1, rounds: 2 }] }), /unknown key "rounds"/);
  assert.match(p("title", { ...TITLE(), effects: [{ type: "heal", power: 1 }] }), /unknown effect type "heal"/);
  // combat has an increasemastery tag too, with rounds/target/...; a title's strict member refuses those,
  // so the combat table must not be the one a title is checked against
  assert.ok(NESTED.sets[NESTED.effects.increasemastery].includes("rounds"));
  assert.match(p("title", { ...TITLE(), effects: [{ type: "increasemastery", power: 1, masteryTypes: ["Taijutsu"], rounds: 2 }] }), /unknown key "rounds"/);
  // fail closed: without the derived title table, title effects are refused rather than sent unchecked
  const noTitles = structuredClone(NESTED); delete noTitles.titleEffects;
  assert.match(new Validator(FIELDS, noTitles).problems("title", TITLE(), null, { preCreate: true }).join(), /unknown effect type "increasemastery"/);
  assert.deepEqual(diffAsserted("badge", { hidden: true, name: "A" }, { name: "A" }), [], "hidden is never diffed");
  assert.equal(diffAsserted("badge", { name: "A" }, { name: "B" }).length, 1);
});

test("manifest: badge and title are entities, @badge/@title are refs, and a title archived by the manifest that rewards it is refused", () => {
  const m = parseManifest({ items: [
    { entity: "quest", slot: "edit", name: "Q", targetId: "fxQuest00000000000001", data: { content: { reward: { reward_badges: ["@badge:fx_crest"], reward_titles: ["@title:fx_lancer"] } } } },
    ...fixture("title_create.json").items, ...fixture("badge_create.json").items], imgSizes: { "fixture_crest.png": 2048 } });
  assert.deepEqual(m.items.map((it) => it.entity), ["quest", "title", "title", "badge"]);
  assert.throws(() => parseManifest(fixture("title_archived_reward.json")), (e) => e instanceof ManifestError && /TITLE "@title:fx_retired" is archived/.test(e.message));
  const edit = { items: [{ entity: "title", slot: "edit", name: "T", targetId: "fxTitle00000000000001", data: { archived: true } },
    { entity: "item", slot: "edit", name: "I", targetId: "fxItem000000000000001", data: { effects: [{ type: "noncombatconsumereward", reward_titles: ["fxTitle00000000000001"] }] } }] };
  assert.throws(() => parseManifest(edit), /TITLE "fxTitle00000000000001" is archived/);
  assert.throws(() => parseManifest({ items: [{ ...fixture("badge_create.json").items[0], data: { ...BADGE(), hidden: false } }], imgSizes: { "fixture_crest.png": 2048 } }), /L13/);
});

// ------------------------------------------------------------------ runner
test("a badge create uploads its @img, fills the placeholder and reads it back; hidden never reaches the server", async () => {
  const h = withImage(harness());
  h.runner.plan(fixture("badge_create.json"), { jobId: "b1" });
  const s = await h.runner.run("b1");
  assert.deepEqual(s.counts, { VERIFIED: 1 }, JSON.stringify(s));
  assert.deepEqual(h.game.calls.map((c) => c.path), ["badge.getAllNames", "badge.create", "badge.get", "badge.update", "badge.get"]);
  const upd = h.game.calls.find((c) => c.path === "badge.update");
  assert.deepEqual(upd.input.data, { name: "Fixture Crest", image: URL_UP, description: BADGE().description });
  const [row] = h.game.rows("badge");
  assert.deepEqual([row.name, row.image, "hidden" in row], ["Fixture Crest", URL_UP, false]);
});

test("titles: created, filled with their effects, and rewarded by a quest through @title and @badge", async () => {
  const h = withImage(harness());
  h.runner.plan(fixture("title_create.json"), { jobId: "t1" });
  assert.deepEqual((await h.runner.run("t1")).counts, { VERIFIED: 2 });
  const lancer = h.game.rows("title").find((r) => r.name === "Fixture Lancer");
  assert.deepEqual([lancer.archived, lancer.effects], [false, TITLE().effects]);
  h.runner.plan(fixture("badge_create.json"), { jobId: "b1" });
  assert.deepEqual((await h.runner.run("b1")).counts, { VERIFIED: 1 });
  h.game.seed("quest", { id: "fxQuest00000000000001", name: "Fixture Quest", hidden: true, content: { objectives: [], reward: {} } });
  const quest = { items: [{ entity: "quest", slot: "edit", name: "Fixture Quest", targetId: "fxQuest00000000000001",
    data: { content: { objectives: [], reward: { reward_badges: ["@badge:fx_crest"], reward_titles: ["@title:fx_lancer", "@title:fx_warden"] } } } }] };
  h.runner.plan(quest, { jobId: "q1" });
  assert.deepEqual((await h.runner.run("q1")).counts, { VERIFIED: 1 });
  const reward = h.game.tables.quest.get("fxQuest00000000000001").content.reward;
  assert.deepEqual(reward.reward_badges, [h.game.rows("badge")[0].id]);
  assert.equal(reward.reward_titles.length, 2);
  // the server refuses a save rewarding an archived title (titleRewards.ts); the job says so
  lancer.archived = true;
  h.runner.plan({ ...quest, _note: "again" }, { jobId: "q2" });
  const s = await h.runner.run("q2");
  assert.equal(s.counts.FAILED, 1, JSON.stringify(s));
  assert.match(h.journal.get("q2").items[0].error, /missing, archived or private/);
});

test("a badge whose name another badge holds is refused by the server; dedupNames catches it before the placeholder", async () => {
  const h = withImage(harness());
  h.game.seed("badge", { id: "b0", name: "Fixture Crest", image: URL_UP, description: "taken" });
  h.runner.plan(fixture("badge_create.json"), { jobId: "n0" });
  const s0 = await h.runner.run("n0");
  assert.equal(s0.counts.FAILED, 1);
  assert.match(h.journal.get("n0").items[0].error, /Badge name already exists/);
  const h2 = withImage(harness());
  h2.game.seed("badge", { id: "b0", name: "Fixture Crest", image: URL_UP, description: "taken" });
  h2.runner.plan({ dedupNames: true, ...fixture("badge_create.json") }, { jobId: "n1" });
  assert.equal((await h2.runner.run("n1")).counts.FAILED, 1);
  assert.match(h2.journal.get("n1").items[0].error, /LIVE NAME COLLISION/);
  assert.equal(h2.game.calls.filter((c) => c.path === "badge.create").length, 0);
});

for (const [entity, file, names] of [["badge", "badge_create.json", 1], ["title", "title_create.json", 1]]) {
  test(`CRASH after a ${entity} create is applied: the placeholder is ORPHANED, filled only after the operator adopts it, never re-created`, async () => {
    const game = new FakeGame({ crashAt: names + 1 }); // name snapshot, create applied server-side, tab dies
    const h = withImage(harness({ game }));
    h.runner.plan(fixture(file), { jobId: "c1" });
    assert.equal((await h.runner.run("c1")).state, "PAUSED");
    assert.equal(game.count(entity), 1);
    const h2 = withImage(harness({ game, storage: h.storage.crash(), idb: h.idb }));
    h2.runner.attach("c1", fixture(file));
    await h2.runner.resume("c1");
    const it = h2.journal.get("c1").items[0];
    assert.equal(it.state, "ORPHANED", JSON.stringify(it));
    assert.deepEqual(it.candidates.map((c) => [c.id, c.placeholderName]), [[game.rows(entity)[0].id, true]]);
    h2.runner.adopt("c1", 0, it.candidates[0].id);
    const s = await h2.runner.run("c1");
    assert.ok(s.counts.VERIFIED >= 1, JSON.stringify(s));
    assert.equal(game.calls.filter((c) => c.path === `${entity}.create`).length, entity === "title" ? 2 : 1, "the adopted row is not created again");
    assert.equal(game.rows(entity).filter((r) => /^New (Badge|Title) - /.test(r.name)).length, 0, "the adopted placeholder was filled");
  });
}

test("review F1/F2: a malformed URL, an over-long uploaded URL or a padded name fails before badge.create; no placeholder", async () => {
  const run = async (data, up) => {
    const h = withImage(harness());
    if (up) h.uploader.upload = async () => ({ ufsUrl: up });
    const m = fixture("badge_create.json"); m.items[0].data = { ...m.items[0].data, ...data };
    let error;
    try { h.runner.plan(m, { jobId: "f" }); await h.runner.run("f"); error = h.journal.get("f").items[0].error; } catch (e) { error = e.message; }
    assert.equal(h.game.calls.filter((c) => c.path === "badge.create").length, 0, JSON.stringify(data));
    assert.equal(h.game.rows("badge").length, 0);
    return error;
  };
  assert.match(await run({ image: "https://[" }), /image: an @img ref or a URL/);
  assert.match(await run({}, "https://utfs.io/f/" + "x".repeat(180)), /at most 191/);
  assert.match(await run({ name: " Fixture Crest " }), /no leading or trailing whitespace/);
});

test("an edit keeps the live image and name: the fetch-merge re-sends the whole record", async () => {
  const h = harness();
  h.game.seed("badge", { id: "fxBadge00000000000001", name: "Fixture Crest", image: URL_UP, description: "old", createdAt: new Date(0), updatedAt: new Date(0) });
  h.runner.plan(fixture("badge_edit.json"), { jobId: "e1" });
  assert.deepEqual((await h.runner.run("e1")).counts, { VERIFIED: 1 });
  const upd = h.game.calls.find((c) => c.path === "badge.update");
  assert.deepEqual(upd.input, { id: "fxBadge00000000000001", data: { name: "Fixture Crest", image: URL_UP, description: "A test badge whose description an edit replaced." } });
});

// ------------------------------------------------------------------ offline gates
test("check_manifest.mjs and validate.py agree on every badge/title fixture", () => {
  const data = fileURLToPath(new URL("../../skills/building-tnr-content/data/", import.meta.url));
  const py = (f) => { try { return { code: 0, out: execFileSync("python3", ["../scripts/validate.py", "--strict", f], { cwd: data, encoding: "utf8" }) }; } catch (e) { return { code: e.status, out: String(e.stdout) + String(e.stderr) }; } };
  const forge = (f) => { try { return checkManifest(f).problems; } catch (e) { return [e.message]; } };
  for (const good of ["badge_create.json", "title_create.json", "badge_edit.json"]) {
    const f = join(FIX, good);
    assert.deepEqual(forge(f), [], good);
    const r = py(f);
    assert.equal(r.code, 0, good + "\n" + r.out);
  }
  const both = {
    "catalog_bad.json": [/unknown key .icon/, /image is required on a badge create/, /holds 500/, /archived is required on a title create/, /bonus/],
    "title_archived_reward.json": [/TITLE .?@title:fx_retired.? is archived in this manifest/],
  };
  for (const [bad, res] of Object.entries(both)) {
    const f = join(FIX, bad);
    const fp = forge(f).join("\n"), r = py(f);
    assert.notEqual(r.code, 0, bad);
    for (const re of res) { assert.match(fp, re, `forge ${bad}`); assert.match(r.out, re, `validate.py ${bad}`); }
  }
  assert.match(forge(join(FIX, "catalog_bad.json")).join("\n"), /unknown effect type "heal"/);
  const out = py(join(FIX, "catalog_bad.json")).out;
  assert.match(out, /'heal' is not a member of TitleEffectSchema/);
  // bounds are validate.py's (Forge checks key sets): power >= 0, at least one mastery type
  assert.match(out, /power=-1 below min 0/);
  assert.match(out, /needs at least one masteryTypes entry/);
});
