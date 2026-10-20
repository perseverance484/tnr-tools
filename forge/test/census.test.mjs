// Read-only item census (runner/census.mjs), against FakeGame's source-faithful item.getAll.
//
// What this file holds, in the brief's own terms
// (docs/handoffs/ELEMENTALDAMAGE_WEAPON_CENSUS_CAPTURE_IMPLEMENTATION_20261020.md sections 4-6):
//   - both hidden partitions, every page, explicit `hidden` on every list read;
//   - exact parsed-tag identity, with the server's string-search filter only a cross-check;
//   - two agreeing scans or no "complete"; malformed, shifted, repeated, wrong-type pages refused;
//   - one persist:"full" point read per target, accepted per point, STALE on updatedAt drift;
//   - 429 / reload resume without losing exported evidence or re-reading a done point;
//   - zero mutations, and the full-persistence allowlist unchanged.

import { test } from "node:test";
import assert from "node:assert/strict";
import { App } from "../src/ui/app.mjs";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";
import { FULL_PERSIST_PATHS, MAX_FULL_CAPTURE_BYTES } from "../src/storage/captures.mjs";
import { MUTATION_PATHS } from "../src/transport/procedures.mjs";
import { censusVerdict, jobOutcome } from "../src/storage/journal.mjs";
import { projectRow, normalizeCensus } from "../src/runner/census.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const KIND = "item.weapon.elementaldamage";
const CENSUS = (pageLimit = 2) => ({ _note: "test census", census: { kind: KIND, pageLimit } });

function harness({ game = new FakeGame(), storage = new MemoryStorage(), idb } = {}) {
  const d = composeForTest({ game, storage, ...(idb ? { idb } : {}) });
  const app = new App({ version: "forge test", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
  let exported = null;
  app.showExport = (t) => { exported = t; };
  return { ...d, app, storage, game, bundle: async (jobId) => { exported = null; await app.exportJob(jobId); return JSON.parse(exported); } };
}

const T0 = new Date("2026-10-01T00:00:00.000Z");
const ed = (extra = {}) => ({ type: "elementaldamage", power: 30, calculation: "formula", direction: "offence", ...extra });
let costSeq = 0;
function item(id, { itemType = "WEAPON", hidden = false, effects = [], cost, ...rest } = {}) {
  return { id, name: `Item ${id}`, itemType, hidden, rarity: "EPIC", cost: cost ?? (costSeq += 10), repsCost: 0, effects, updatedAt: T0, createdAt: T0, description: "d", ...rest };
}
/** The population every happy-path test starts from: 4 visible + 3 hidden WEAPONs, 2 non-weapons. */
function seed(game) {
  const rows = [
    item("w-formula-missing", { effects: [ed(), { type: "increasedamagetaken", power: 20 }] }), // Stormrender shape
    item("w-formula-good", { effects: [ed({ statTypes: ["None"], generalTypes: ["Highest"] })] }),
    item("w-plain", { effects: [{ type: "damage", power: 10, calculation: "formula", statTypes: ["Taijutsu"] }] }),
    // the word appears as a value, not as a type: the server's filter matches, the census must not
    item("w-coincidence", { effects: [{ type: "damage", power: 5, description: "elementaldamage" }] }),
    item("h-static", { hidden: true, effects: [ed({ calculation: "static" })] }),
    item("h-two", { hidden: true, effects: [ed({ statTypes: [] }), ed({ generalTypes: ["Strength"] })] }),
    item("h-none", { hidden: true, effects: [] }),
    item("c-other", { itemType: "CONSUMABLE", effects: [ed()] }),
    item("c-hidden-other", { itemType: "ARMOR", hidden: true, effects: [ed()] }),
  ];
  for (const r of rows) game.seed("item", r);
  return rows;
}
const TARGETS = ["h-static", "h-two", "w-formula-good", "w-formula-missing"];
const listCalls = (game) => game.calls.filter((c) => c.path === "item.getAll");
const getCalls = (game) => game.calls.filter((c) => c.path === "item.get");

// ---------------------------------------------------------------- the manifest contract
test("a census manifest parses alone, and its policy is part of its identity", () => {
  const m = parseManifest(CENSUS(100));
  assert.deepEqual(m.census, { kind: KIND, pageLimit: 100 });
  assert.equal(m.items.length, 0);
  assert.notEqual(parseManifest(CENSUS(50)).hash, m.hash, "pageLimit changes what the run does");
  assert.deepEqual(parseManifest({ census: { kind: KIND } }).census.pageLimit, 100, "default page size is the brief's conservative 100");
});

test("a census manifest refuses company: items, captures, suggest mode, bad kind or page size", () => {
  const refuse = (m, re) => assert.throws(() => parseManifest(m), (e) => e instanceof ManifestError && re.test(e.message));
  refuse({ census: { kind: KIND }, items: [{ entity: "item", slot: "edit", targetId: "x", name: "x", data: { name: "y" } }] }, /carries no items/);
  refuse({ census: { kind: KIND }, capture: { before: [{ proc: "item.get", input: { id: "x" } }] } }, /carries no items, captures/);
  refuse({ census: { kind: KIND }, mode: "suggest" }, /mode/);
  refuse({ census: { kind: "item.getAll" } }, /census.kind must be one of/);
  refuse({ census: { kind: KIND, pageLimit: 501 } }, /pageLimit/);
  refuse({ census: { kind: KIND, pageLimit: 0 } }, /pageLimit/);
  refuse({ census: { kind: KIND, filter: { hidden: false } } }, /only kind and pageLimit/);
  refuse({ census: "item" }, /must be an object/);
  assert.deepEqual(normalizeCensus({ kind: KIND, pageLimit: 500 }), { kind: KIND, pageLimit: 500 });
});

test("the full-persistence allowlist is unchanged: still point reads only, no list path", () => {
  assert.deepEqual([...FULL_PERSIST_PATHS], ["skillTree.get", "gameAsset.get", "jutsu.get", "item.get", "bloodline.get", "quests.get", "profile.getAi", "ai.getAiProfile"]);
  assert.throws(() => parseManifest({ capture: { before: [{ proc: "item.getAll", input: { limit: 100 }, persist: "full" }] } }), /only allowed for the audited content-record point reads/);
});

test("censusPage pages only the audited census list path", async () => {
  const h = harness();
  await assert.rejects(h.reader.censusPage("jutsu.getAll", { limit: 1 }), /censusPage is only for item.getAll/);
  await assert.rejects(h.reader.censusPage("item.update", {}), /censusPage is only for/);
});

test("the projection keeps exactly the allowlisted fields and normalizes Date to ISO", () => {
  const p = projectRow({ ...item("p1", { effects: [ed(), { power: 1 }] }), userId: "secret", ownerIds: ["u"] });
  assert.deepEqual(Object.keys(p).sort(), ["effectTypes", "effectsMalformed", "hidden", "id", "itemType", "name", "updatedAt"]);
  assert.equal(p.updatedAt, T0.toISOString());
  assert.deepEqual(p.effectTypes, ["elementaldamage", null]);
  assert.equal(p.effectsMalformed, true, "a member without a type is malformed even beside a real tag (review F1)");
  assert.equal(projectRow({ id: "x", effects: "[]" }).effectsMalformed, true);
  for (const fx of [[null], [{ power: 30 }], ["elementaldamage"], [{ type: "" }], [{ type: 7 }], [[{ type: "elementaldamage" }]]])
    assert.equal(projectRow({ id: "x", effects: fx }).effectsMalformed, true, JSON.stringify(fx));
  assert.equal(projectRow({ id: "x", effects: [] }).effectsMalformed, false);
  assert.equal(projectRow({ id: "x", effects: [{ type: "damage" }] }).effectsMalformed, false);
});

// ---------------------------------------------------------------- the happy path
test("census: both partitions, every page, exact tag; one full point read per target; zero mutations", async () => {
  const h = harness();
  const rows = seed(h.game);
  h.runner.plan(CENSUS(2), { jobId: "cz" });
  const s = await h.runner.run("cz");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success");

  // only the two public queries, never a mutation, never the cached path
  assert.deepEqual([...new Set(h.game.calls.map((c) => c.path))].sort(), ["item.get", "item.getAll"]);
  assert.ok(!h.game.calls.some((c) => MUTATION_PATHS.includes(c.path)));
  // every list read names its partition explicitly and the WEAPON type
  for (const c of listCalls(h.game)) {
    assert.equal(typeof c.input.hidden, "boolean", "an absent hidden would silently mean hidden:false");
    assert.equal(c.input.itemType, "WEAPON");
    assert.equal(c.input.limit, 2);
  }
  const unf = listCalls(h.game).filter((c) => !c.input.effect);
  // visible: 4 rows at limit 2 -> pages 0,1 full, page 2 empty terminator; hidden: 3 rows -> 0 full, 1 short
  assert.deepEqual(unf.map((c) => `${c.input.hidden}:${c.input.cursor}`), ["false:0", "false:1", "false:2", "true:0", "true:1", "false:0", "false:1", "false:2", "true:0", "true:1"], "two complete scans, cursors in order");
  assert.ok(listCalls(h.game).some((c) => c.input.effect?.[0] === "elementaldamage" && c.input.hidden === true), "filtered cross-check covers hidden too");

  const job = h.journal.get("cz");
  assert.equal(job.census.inventory, "COMPLETE");
  assert.deepEqual(job.census.counts, { "hidden:false": 4, "hidden:true": 3, total: 7, tagged: 4, malformed: 0 });
  assert.deepEqual(job.census.targets.map((t) => t.id), TARGETS);
  assert.deepEqual(job.census.crossCheck.filterOnly, ["w-coincidence"], "a string match that is not a tag is listed, not captured");
  assert.deepEqual(job.census.crossCheck.missedByFilter, []);
  assert.deepEqual(getCalls(h.game).map((c) => c.input.id), TARGETS, "exactly one point read per target, nothing else");
  assert.equal(censusVerdict(job), "COMPLETE");
  assert.ok(!("rows" in job.census), "the inventory rows live in IndexedDB, not the localStorage journal");

  const b = await h.bundle("cz");
  assert.equal(b.outcome, "success");
  assert.equal(b.census.verdict, "COMPLETE");
  assert.equal(b.census.rows.length, 7);
  for (const r of b.census.rows) assert.deepEqual(Object.keys(r).sort(), ["effectTypes", "effectsMalformed", "hidden", "id", "itemType", "name", "updatedAt"], "no list body field beyond the projection");
  assert.ok(!b.census.rows.some((r) => r.id.startsWith("c-")), "non-weapons never enter the inventory");
  const pts = b.captures.filter((c) => c.phase === "census");
  assert.equal(pts.length, 4);
  for (const c of pts) {
    assert.equal(c.proc, "item.get"); assert.equal(c.persist, "full"); assert.equal(c.persistOk, true);
    assert.equal(c.accepted, true); assert.equal(c.stale, false); assert.equal(c.rows, 1);
    const src = rows.find((r) => r.id === c.input.id);
    assert.deepEqual(c.data.effects, src.effects, "the exact effects array");
    assert.equal(c.data.cost, src.cost, "a full body, not the projection");
  }
  assert.equal(h.game.calls.filter((c) => c.path === "item.get").length, 4, "export never re-reads");
});

test("an empty partition and an exact-multiple page both terminate on nextCursor:null", async () => {
  const h = harness();
  h.game.seed("item", item("a", { effects: [ed()] }));
  h.game.seed("item", item("b"));
  h.runner.plan(CENSUS(2), { jobId: "edge" });
  const s = await h.runner.run("edge");
  assert.equal(s.outcome, "success");
  const scan1 = listCalls(h.game).slice(0, 3).map((c) => `${c.input.hidden}:${c.input.cursor}`);
  assert.deepEqual(scan1, ["false:0", "false:1", "true:0"], "2 rows at limit 2 needs the empty page; an empty hidden partition is one page");
  assert.deepEqual(h.journal.get("edge").census.counts, { "hidden:false": 2, "hidden:true": 0, total: 2, tagged: 1, malformed: 0 });
});

test("a clean zero-match census is COMPLETE with no point reads", async () => {
  const h = harness();
  h.game.seed("item", item("x", { effects: [{ type: "damage", power: 1 }] }));
  h.runner.plan(CENSUS(5), { jobId: "zero" });
  const s = await h.runner.run("zero");
  assert.equal(s.outcome, "success");
  assert.equal(getCalls(h.game).length, 0);
  const b = await h.bundle("zero");
  assert.equal(b.census.verdict, "COMPLETE");
  assert.equal(b.census.targets.length, 0);
});

test("a row whose effects cannot be parsed is captured as evidence, and the census is AMBIGUOUS, never COMPLETE", async () => {
  const h = harness();
  h.game.seed("item", item("m", { effects: "not-an-array" }));
  h.runner.plan(CENSUS(5), { jobId: "mal" });
  await h.runner.run("mal");
  const job = h.journal.get("mal");
  assert.deepEqual(job.census.targets, [{ id: "m", updatedAt: T0.toISOString(), reason: "effectsMalformed" }]);
  assert.equal(job.capturesCensus[0].persistOk, true, "its full body is kept: it is what the game holds");
  assert.equal(censusVerdict(job), "AMBIGUOUS");
  assert.equal(jobOutcome(job), "failed");
  assert.equal((await h.bundle("mal")).census.verdict, "AMBIGUOUS");
});

// Census review F1: a malformed MEMBER of an effects array used to count as well-formed, so the row
// fell out of the target set and a census could be COMPLETE without ever reading it.
for (const [label, fx] of [["null member", [null]], ["untyped member", [{ power: 30 }]], ["bare string member", ["elementaldamage"]],
  ["tag beside an untyped member", [ed(), { power: 1 }]]]) {
  test(`malformed effect member (${label}): the record is a target, its body is captured, the census is never COMPLETE`, async () => {
    const h = harness();
    h.game.seed("item", item("ok", { effects: [{ type: "damage", power: 1 }] }));
    h.game.seed("item", item("bad", { effects: fx }));
    h.runner.plan(CENSUS(5), { jobId: "mm" });
    const s = await h.runner.run("mm");
    const job = h.journal.get("mm");
    assert.deepEqual(job.census.targets, [{ id: "bad", updatedAt: T0.toISOString(), reason: "effectsMalformed" }]);
    assert.equal(job.census.counts.malformed, 1);
    assert.deepEqual(getCalls(h.game).map((c) => c.input.id), ["bad"], "the malformed record gets its full point read");
    assert.equal(job.capturesCensus[0].persistOk, true);
    assert.equal(censusVerdict(job), "AMBIGUOUS");
    assert.equal(s.outcome, "failed", "an ambiguous census is never success");
  });
}

// ---------------------------------------------------------------- Stage A refusals
const stageAFailure = async (hook, re, verdict = "FAILED") => {
  const h = harness();
  seed(h.game);
  h.game.onCall = hook;
  h.runner.plan(CENSUS(2), { jobId: "f" });
  const s = await h.runner.run("f");
  const job = h.journal.get("f");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "failed", "an incomplete inventory is never success");
  assert.equal(job.census.inventory, verdict);
  assert.match(job.census.problems.join("\n"), re);
  assert.equal(getCalls(h.game).length, 0, "no point read is sent from an untrustworthy inventory");
  assert.deepEqual(job.capturesCensus, []);
  const b = await h.bundle("f");
  assert.equal(b.outcome, "failed");
  assert.equal(b.census.verdict, verdict);
  return { h, job };
};
const ok = (data) => ({ ok: true, data });

test("an edit landing between the two scans is UNSTABLE, with the changed id named", async () => {
  let n = 0;
  const { job } = await stageAFailure((path, input, _, game) => {
    if (path === "item.getAll" && !input.effect && input.hidden === false && input.cursor === 0 && ++n === 2) game.tables.item.get("w-plain").updatedAt = new Date("2026-10-02T00:00:00Z");
  }, /two complete scans disagree/, "UNSTABLE");
  assert.deepEqual(job.census.diff.changed, ["w-plain"]);
});

test("a row inserted ahead of the cursor shifts the offset crawl and is refused as a repeat", async () => {
  await stageAFailure((path, input, _, game) => {
    if (path === "item.getAll" && input.hidden === false && input.cursor === 1 && !game.tables.item.has("new")) game.seed("item", item("new", { cost: -1 }));
  }, /repeated \(rows shifted under the crawl\)/);
});

test("a malformed page is refused", async () => {
  await stageAFailure((path, input) => (path === "item.getAll" && input.cursor === 1 ? ok({ rows: [] }) : undefined), /malformed page/);
});

test("a full page that claims to be the last, or a skipped cursor, is refused", async () => {
  await stageAFailure((path, input) => (path === "item.getAll" && input.cursor === 0 && !input.hidden ? ok({ data: [item("a1"), item("a2")], nextCursor: null }) : undefined), /nextCursor null after 2\/2 rows/);
  await stageAFailure((path, input) => (path === "item.getAll" && input.cursor === 0 && !input.hidden ? ok({ data: [item("a1"), item("a2")], nextCursor: 5 }) : undefined), /nextCursor 5/);
});

test("a row of the wrong type or the wrong partition is refused", async () => {
  await stageAFailure((path, input) => (path === "item.getAll" && input.cursor === 0 && !input.hidden ? ok({ data: [item("z", { itemType: "ARMOR" })], nextCursor: null }) : undefined), /is ARMOR, not WEAPON/);
  await stageAFailure((path, input) => (path === "item.getAll" && input.cursor === 0 && input.hidden ? ok({ data: [item("z")], nextCursor: null }) : undefined), /hidden:false in the hidden:true partition/);
});

test("a failed page read is refused, not skipped", async () => {
  await stageAFailure((path, input) => (path === "item.getAll" && input.hidden ? { ok: false, error: { code: "INTERNAL_SERVER_ERROR", message: "boom" } } : undefined), /read failed INTERNAL_SERVER_ERROR/);
});

test("a filtered cross-check that misses an exact hit fails the inventory", async () => {
  await stageAFailure((path, input) => (path === "item.getAll" && input.effect && input.hidden ? ok({ data: [], nextCursor: null }) : undefined), /cross-check: the tag-filtered crawl and the inventory disagree/);
});

// ---------------------------------------------------------------- Stage B acceptance
test("a record edited after the inventory is STALE: kept, but not accepted", async () => {
  const h = harness();
  seed(h.game);
  h.game.onCall = (path, input, _, game) => { if (path === "item.get" && input.id === "h-two") game.tables.item.get("h-two").updatedAt = new Date("2026-10-03T00:00:00Z"); };
  h.runner.plan(CENSUS(2), { jobId: "st" });
  const s = await h.runner.run("st");
  assert.equal(s.outcome, "failed");
  const job = h.journal.get("st");
  assert.equal(censusVerdict(job), "STALE");
  const p = job.capturesCensus.find((c) => c.input.id === "h-two");
  assert.equal(p.stale, true); assert.equal(p.accepted, false); assert.equal(p.persistOk, true, "the body the game gave is still evidence");
  assert.match(p.problems.join(), /STALE: updatedAt 2026-10-03T00:00:00.000Z != inventoried 2026-10-01T00:00:00.000Z; recapture required/);
  const b = await h.bundle("st");
  assert.equal(b.census.verdict, "STALE");
  assert.equal(b.captures.find((c) => c.input?.id === "h-two").data.updatedAt, "2026-10-03T00:00:00.000Z");
});

test("a body over the full-capture ceiling is a hard per-point failure, never truncated", async () => {
  const h = harness();
  h.game.seed("item", item("big", { effects: [ed()], description: "x".repeat(MAX_FULL_CAPTURE_BYTES) }));
  h.runner.plan(CENSUS(5), { jobId: "big" });
  const s = await h.runner.run("big");
  assert.equal(s.outcome, "failed");
  const [p] = h.journal.get("big").capturesCensus;
  assert.equal(p.persistOk, false); assert.equal(p.accepted, false);
  assert.match(p.problems.join(), /body not persisted: body is \d+ bytes, over the/);
  const b = await h.bundle("big");
  assert.ok(!("data" in b.captures[0]), "no shortened body presented as full");
  assert.equal(b.census.verdict, "FAILED");
});

test("a record deleted after the inventory (item.get answers null) is not accepted", async () => {
  const h = harness();
  seed(h.game);
  h.game.onCall = (path, input) => (path === "item.get" && input.id === "w-formula-good" ? ok(null) : undefined);
  h.runner.plan(CENSUS(2), { jobId: "gone" });
  await h.runner.run("gone");
  const p = h.journal.get("gone").capturesCensus.find((c) => c.input.id === "w-formula-good");
  assert.equal(p.accepted, false); assert.equal(p.rows, 0);
  assert.match(p.problems.join(), /record not found/);
});

test("a snapshot gone before export downgrades the census verdict instead of re-reading", async () => {
  const h = harness();
  seed(h.game);
  h.runner.plan(CENSUS(2), { jobId: "ev" });
  await h.runner.run("ev");
  const calls = h.game.calls.length;
  await h.cache.deleteSnapshot(h.journal.get("ev").census.inventoryKey);
  const b = await h.bundle("ev");
  assert.equal(b.census.verdict, "FAILED");
  assert.match(b.census.inventoryError, /is gone; it was not re-crawled/);
  assert.equal(b.outcome, "failed");
  assert.equal(h.game.calls.length, calls, "export issued no read");
});

// ---------------------------------------------------------------- budget, 429, resume
test("a 429 inside Stage A pauses with nothing journaled; resume crawls again from cursor 0", async () => {
  const h = harness();
  seed(h.game);
  let trip = true;
  h.game.onCall = (path, input) => (trip && path === "item.getAll" && input.hidden && input.cursor === 1 ? (trip = false, { ok: false, error: { code: "TOO_MANY_REQUESTS", message: "slow down", path } }) : undefined);
  h.runner.plan(CENSUS(2), { jobId: "rl" });
  const s = await h.runner.run("rl");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "TOO_MANY_REQUESTS"); assert.equal(s.pause.path, "item.getAll");
  assert.equal(h.journal.get("rl").census, undefined, "half an offset crawl is never journaled");
  assert.ok(h.budget.log.tripped(), "the trip is persisted by the existing budget");
  await assert.rejects(h.runner.run("rl").then((x) => { if (x.state === "PAUSED") throw new Error("still tripped"); }), /still tripped/, "no send while tripped");
  h.clock.set(s.pause.until + 1);
  const before = h.game.calls.length;
  const r = await h.runner.run("rl");
  assert.equal(r.outcome, "success");
  const first = h.game.calls.slice(before).find((c) => c.path === "item.getAll");
  assert.deepEqual([first.input.hidden, first.input.cursor], [false, 0]);
  assert.equal(censusVerdict(h.journal.get("rl")), "COMPLETE");
});

test("a pause inside Stage B, then a reload: done points are exported, never re-read, and the rest finish", async () => {
  const h = harness();
  seed(h.game);
  let n = 0;
  h.game.onCall = (path) => (path === "item.get" && ++n === 3 ? { ok: false, error: { code: "TOO_MANY_REQUESTS", message: "slow", path } } : undefined);
  h.runner.plan(CENSUS(2), { jobId: "rb" });
  const s = await h.runner.run("rb");
  assert.equal(s.state, "PAUSED");
  const partial = await h.bundle("rb");
  assert.equal(partial.census.verdict, "INCOMPLETE", "a paused census is never labelled complete");
  assert.notEqual(partial.outcome, "success");
  const done = partial.captures.filter((c) => c.phase === "census");
  assert.equal(done.length, 2);
  assert.ok(done.every((c) => c.persistOk === true && c.data), "the evidence already read is exportable now");

  // reload: a new tab over the same persisted storage and IndexedDB
  const h2 = harness({ game: h.game, storage: h.storage.crash(), idb: h.idb });
  h2.clock.set(s.pause.until + 1);
  h2.runner.attach("rb", CENSUS(2));
  const r = await h2.runner.resume("rb");
  assert.equal(r.outcome, "success");
  const ids = getCalls(h.game).map((c) => c.input.id);
  assert.deepEqual(ids, ["h-static", "h-two", "w-formula-good", "w-formula-good", "w-formula-missing"], "only the 429'd point is asked twice");
  const b = await h2.bundle("rb");
  assert.equal(b.census.verdict, "COMPLETE");
  assert.equal(b.captures.filter((c) => c.phase === "census").length, 4);
});

test("every census read goes through the per-path budget, never past its allowance", async () => {
  const h = harness();
  for (let i = 0; i < 70; i++) h.game.seed("item", item(`b${String(i).padStart(2, "0")}`, { effects: i % 2 ? [ed()] : [] }));
  const sends = [];
  h.game.onCall = (path) => { sends.push({ path, at: h.clock() }); };
  h.runner.plan(CENSUS(5), { jobId: "bud" });
  const s = await h.runner.run("bud");
  assert.equal(s.outcome, "success");
  assert.equal(h.journal.get("bud").census.targets.length, 35);
  for (const path of ["item.getAll", "item.get"]) {
    const ts = sends.filter((x) => x.path === path).map((x) => x.at);
    for (const t of ts) assert.ok(ts.filter((u) => u <= t && t - u < 60_000).length <= h.budget.allowance, `${path}: more than ${h.budget.allowance} in a 60 s window`);
  }
  assert.ok(h.budget.waits > 0, "the throttle actually held requests");
});

test("Pause after this item stops a census between point reads and resumes at the next one", async () => {
  const h = harness();
  seed(h.game);
  h.game.onCall = (path) => { if (path === "item.get") h.runner.requestPause(); };
  h.runner.plan(CENSUS(2), { jobId: "up" });
  const s = await h.runner.run("up");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "USER");
  assert.equal(h.journal.get("up").capturesCensusPartial.length, 1);
  h.game.onCall = null;
  const r = await h.runner.run("up");
  assert.equal(r.outcome, "success");
  assert.deepEqual(getCalls(h.game).map((c) => c.input.id), TARGETS);
});

// Census review F3: Pause used to be checked only between Stage B point reads, so the two full
// scans and the cross-check ran on, spending rate budget, after the operator pressed it.
for (const [label, at] of [["first scan", 1], ["second scan", 6], ["filtered cross-check", 11]]) {
  test(`Pause during Stage A (${label}) stops before the next page; nothing is journaled; resume restarts at cursor 0`, async () => {
    const h = harness();
    seed(h.game);
    let pages = 0;
    h.game.onCall = (path) => { if (path === "item.getAll" && ++pages === at) h.runner.requestPause(); };
    h.runner.plan(CENSUS(2), { jobId: "pa" });
    const s = await h.runner.run("pa");
    assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "USER");
    assert.match(s.pause.detail, /Stage A/);
    assert.equal(listCalls(h.game).length, at, "no page is read after the pause request");
    assert.equal(getCalls(h.game).length, 0);
    assert.equal(h.journal.get("pa").census, undefined, "a half-finished inventory is never journaled");
    h.game.onCall = null;
    const before = listCalls(h.game).length;
    const r = await h.runner.run("pa");
    assert.equal(r.outcome, "success");
    assert.equal(listCalls(h.game)[before].input.cursor, 0, "the resume crawls again from cursor 0");
    assert.equal(listCalls(h.game)[before].input.hidden, false);
    assert.deepEqual(getCalls(h.game).map((c) => c.input.id), TARGETS);
  });
}

test("Pause during Stage A of a zero-target census does not let it finish DONE", async () => {
  const h = harness();
  h.game.seed("item", item("x", { effects: [{ type: "damage", power: 1 }] }));
  h.game.onCall = (path) => { if (path === "item.getAll") h.runner.requestPause(); };
  h.runner.plan(CENSUS(5), { jobId: "pz" });
  const s = await h.runner.run("pz");
  assert.equal(s.state, "PAUSED");
  assert.equal(listCalls(h.game).length, 1);
});

// ---------------------------------------------------------------- the committed ledger fixture
// scripts/test_elementaldamage_census_ledger.py reads this bundle. It is produced HERE, by the
// shipped census code against FakeGame, so the ledger is tested against the real export shape and
// this test fails when that shape changes. Regenerate with UPDATE_CENSUS_FIXTURE=1.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
const FIXTURE = new URL("./fixtures/census/elementaldamage_bundle.json", import.meta.url);
test("the committed census ledger fixture is exactly what the census exports", async () => {
  costSeq = 0; // costs order the crawl; the fixture must not depend on which tests ran first
  const h = harness();
  const fx = (o) => ({ power: 30, rounds: 0, target: "INHERIT", direction: "offence", description: "placeholder", allowBloodlineDamageIncrease: true, allowBloodlineDamageDecrease: true, ...o });
  const rows = [
    // the known positive control, effects as captured in tnr_results_1792478135730.json
    item("cLXXf8RJv5l9B_gGsYN2a", { name: "Stormrender", effects: [fx({ type: "elementaldamage", calculation: "formula" }), fx({ type: "increasedamagetaken", calculation: "percentage", power: 20, rounds: 2 })] }),
    item("fx-missing-stats", { effects: [fx({ type: "elementaldamage", calculation: "formula", generalTypes: ["Highest"] })] }),
    item("fx-missing-gens", { effects: [fx({ type: "elementaldamage", calculation: "formula", statTypes: ["None"] })] }),
    item("fx-both-missing", { hidden: true, effects: [fx({ type: "elementaldamage", calculation: "formula", statTypes: [], allowBloodlineDamageIncrease: false })] }),
    item("fx-both-present", { effects: [fx({ type: "elementaldamage", calculation: "formula", statTypes: ["Ninjutsu"], generalTypes: ["Strength", "Speed"] }), fx({ type: "damage", calculation: "formula", statTypes: ["Ninjutsu"], generalTypes: ["Strength"] })] }),
    item("fx-static", { hidden: true, effects: [fx({ type: "elementaldamage", calculation: "static", power: 100 })] }),
    item("fx-two-tags", { effects: [fx({ type: "elementaldamage", calculation: "formula", statTypes: ["None"], generalTypes: ["Highest"] }), fx({ type: "elementaldamage", calculation: "formula" })] }),
    item("fx-ambiguous", { effects: [fx({ type: "elementaldamage", statTypes: "Highest" })] }),
    item("fx-damage-only", { effects: [fx({ type: "damage", calculation: "formula" })] }),
    item("fx-not-weapon", { itemType: "CONSUMABLE", effects: [fx({ type: "elementaldamage", calculation: "formula" })] }),
  ];
  for (const r of rows) h.game.seed("item", r);
  h.runner.plan(CENSUS(3), { jobId: "fixture", manifestPath: "push/132_elementaldamage_weapon_census.json", manifestNumber: 132 });
  assert.equal((await h.runner.run("fixture")).outcome, "success");
  const text = JSON.stringify(await h.bundle("fixture"), null, 1) + "\n";
  if (process.env.UPDATE_CENSUS_FIXTURE) { mkdirSync(new URL("./fixtures/census/", import.meta.url), { recursive: true }); writeFileSync(FIXTURE, text); }
  assert.equal(readFileSync(FIXTURE, "utf8"), text, "regenerate with UPDATE_CENSUS_FIXTURE=1 and review the diff");
});

test("the staged operator manifest push/132 is the census the brief asks for", () => {
  const m = parseManifest(readFileSync(new URL("../../push/132_elementaldamage_weapon_census.json", import.meta.url), "utf8"));
  assert.deepEqual(m.census, { kind: KIND, pageLimit: 100 });
  assert.equal(m.items.length + m.capture.before.length + m.capture.after.length, 0);
});
