// The two Forge defects that failed 9 of the 28 writes in the committed Godstorm run
// (harvests/inbox/tnr_results_1789829183863.json, outcome "failed"), each pinned against the
// evidence that produced it.
//
//   1. gameAsset.getAllNames was called with NO input. Its source schema is
//      z.object({type?, folderPrefix?}) - members optional, object not - so zod refused the call
//      and the server answered BAD_REQUEST before the resolver ran. Both list callers died with
//      it: the pre-create reconciliation snapshot (3 Stormcourt SCENE_BACKGROUND creates,
//      "snapshot failed: gameAsset.getAllNames BAD_REQUEST") and, had the manifest reached it,
//      dedupNames. The Stormcourt quest update then failed on the @scene refs those creates were
//      supposed to fill, so one input bug cost 4 of the 9 failures.
//
//   2. The AI-profile read-back compared rules with JSON.stringify. The server re-emits a
//      validated document in schema key order, so all 18 corrections were reported as drift
//      (CONFIRMED, verdict "drift") although every recorded sent/live pair parses to the same
//      object. That is a false negative in the only check that says whether a write landed.
//
// The fake game now holds the source contract on both counts (test/fakegame.mjs): it refuses an
// asset name list with no object input, and it stores rules re-keyed the way zod re-emits them.
// With src reverted to its pre-fix state, 14 of the existing suite's tests fail alongside these.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { listInput } from "../src/budget/reader.mjs";
import { deepEqualPayload } from "../src/runner/validate.mjs";
import { FakeGame, rekey } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const RESULT = join(HERE, "..", "..", "harvests", "inbox", "tnr_results_1789829183863.json");

function harness({ game = new FakeGame(), storage = new MemoryStorage(), idb = new IDBFactory() } = {}) {
  return composeForTest({ game, storage, idb });
}

const asset = (name, srcId) => ({ entity: "asset", slot: "create", name, srcId, data: { name, hidden: true, type: "STATIC", url: "u" } });
const callsTo = (game, path) => game.calls.filter((c) => c.path === path);

// ------------------------------------------------------------------ 1: the list input contract

test("gameAsset.getAllNames is sent the object its schema requires; the inputless lists are not given one", () => {
  assert.deepEqual(listInput("gameAsset.getAllNames"), {}, "the one list with an .input() gets an object");
  for (const path of ["jutsu.getAllNames", "item.getAllNames", "bloodline.getAllNames", "quests.getAllNames", "profile.getAllAiNames"]) {
    assert.equal(listInput(path), undefined, `${path} declares no .input() at source; do not invent one`);
  }
});

test("the asset name list refuses an absent input, exactly as the live server did", async () => {
  const h = harness();
  // the defect, reproduced directly: what Forge used to put on the wire
  const [bad] = await h.client.batch([{ path: "gameAsset.getAllNames", input: undefined }]);
  assert.equal(bad.ok, false);
  assert.equal(bad.error.code, "BAD_REQUEST", "this is the error the three Stormcourt creates died on");
  // and what it puts on the wire now
  const good = await h.reader.list("gameAsset.getAllNames");
  assert.equal(good.ok, true);
  assert.deepEqual(callsTo(h.game, "gameAsset.getAllNames").at(-1).input, {});
});

test("a list read is cached under id '' only while it is the default, unfiltered one", async () => {
  const h = harness();
  h.game.seed("asset", { id: "a1", name: "Lantern", type: "STATIC", folder: "scenes" });
  h.game.seed("asset", { id: "a2", name: "Court", type: "SCENE_BACKGROUND", folder: "scenes" });

  await h.reader.list("gameAsset.getAllNames");
  const second = await h.reader.list("gameAsset.getAllNames");
  assert.equal(second.cached, true, "the default list is cacheable");
  assert.equal(callsTo(h.game, "gameAsset.getAllNames").length, 1);

  // an explicitly-passed default is the same request, so it still hits the cache
  const same = await h.reader.list("gameAsset.getAllNames", { input: {} });
  assert.equal(same.cached, true);
  assert.equal(callsTo(h.game, "gameAsset.getAllNames").length, 1);

  // a FILTER is a different question: never served from that slot, never written into it
  const filtered = await h.reader.list("gameAsset.getAllNames", { input: { type: "SCENE_BACKGROUND", folderPrefix: true } });
  assert.equal(filtered.cached, undefined);
  assert.deepEqual(filtered.data, [{ id: "a2", name: "scenes/Court" }]);
  const again = await h.reader.list("gameAsset.getAllNames");
  assert.equal(again.cached, true, "the filtered answer must not have overwritten the unfiltered slot");
  assert.equal(again.data.length, 2);
});

test("a list capture is called with the filter the manifest wrote, and records the input actually used", async () => {
  const h = harness();
  h.game.seed("asset", { id: "a1", name: "Lantern", type: "STATIC", folder: "props" });
  h.game.seed("asset", { id: "a2", name: "Court", type: "SCENE_BACKGROUND", folder: "scenes" });
  h.runner.plan({ items: [], capture: { before: [
    { proc: "gameAsset.getAllNames", input: { type: "SCENE_BACKGROUND", folderPrefix: true } },
    { proc: "gameAsset.getAllNames" },
  ] } }, { jobId: "cap" });
  await h.runner.run("cap");

  const sent = callsTo(h.game, "gameAsset.getAllNames").map((c) => c.input);
  assert.deepEqual(sent, [{ type: "SCENE_BACKGROUND", folderPrefix: true }, {}]);
  const [one, two] = h.journal.get("cap").capturesBefore;
  assert.deepEqual(one.input, { type: "SCENE_BACKGROUND", folderPrefix: true });
  assert.equal(one.rows, 1, "the filter was applied, so the bundle's row count means what it says");
  assert.deepEqual(two.input, {}, "the unfiltered read is stamped with the input it really used");
  assert.equal(two.rows, 2);
});

// ------------------------------------------------- 1b: the two callers that died on the defect

test("the pre-create snapshot of an asset create succeeds and the create lands", async () => {
  const h = harness();
  h.game.seed("asset", { id: "existing", name: "Elsewhere", type: "STATIC" });
  h.runner.plan({ items: [asset("Godstorm Stormcourt Upper Court", "godstorm_sc_upper")] }, { jobId: "snap" });
  const s = await h.runner.run("snap");

  assert.equal(s.items[0].state, "VERIFIED", s.items[0].error ?? "");
  assert.equal(h.game.count("asset"), 2);
  // the snapshot is taken BEFORE the create leaves, and it is the read that used to die here
  const names = h.game.calls.findIndex((c) => c.path === "gameAsset.getAllNames");
  const create = h.game.calls.findIndex((c) => c.path === "gameAsset.create");
  assert.ok(names >= 0 && names < create, "the pre-create snapshot read must precede the create");
  assert.deepEqual(h.game.calls[names].input, {});
  // (a finished job's snapshot is dropped by Reconciler.forget, so it is checked by its effect:
  // the create was allowed to run at all, which is what BAD_REQUEST prevented)
});

test("dedupNames over assets reads the live list and fails only the colliding item", async () => {
  const h = harness();
  h.game.seed("asset", { id: "live-1", name: "Godstorm Stormcourt Upper Court", type: "STATIC" });
  h.runner.plan({ dedupNames: true, items: [
    asset("Godstorm Stormcourt Upper Court", "godstorm_sc_upper"),
    asset("Godstorm Stormcourt Binding Dais Active", "godstorm_sc_dais_active"),
  ] }, { jobId: "dedup" });
  const s = await h.runner.run("dedup");

  assert.match(s.items[0].error, /LIVE NAME COLLISION "Godstorm Stormcourt Upper Court"/);
  assert.equal(s.items[1].state, "VERIFIED", s.items[1].error ?? "");
  assert.equal(h.game.count("asset"), 2, "one live row plus the one new row");
  for (const c of callsTo(h.game, "gameAsset.getAllNames")) assert.deepEqual(c.input, {}, "every list call carries the object");
});

test("dedupNames must not ask for folder-prefixed names: they would never match a manifest name", async () => {
  const h = harness();
  h.game.seed("asset", { id: "live-1", name: "Godstorm Stormcourt Upper Court", type: "SCENE_BACKGROUND", folder: "godstorm" });
  h.runner.plan({ dedupNames: true, items: [asset("Godstorm Stormcourt Upper Court", "godstorm_sc_upper")] }, { jobId: "pfx" });
  const s = await h.runner.run("pfx");
  assert.match(s.items[0].error, /LIVE NAME COLLISION/, "a folderPrefix'd list would have read 'godstorm/...' and missed this");
  assert.equal(h.game.count("asset"), 1, "no second row was minted");
});

// ------------------------------------------------------------- 2: the AI-profile read-back

const RULE = Object.freeze({
  action: { type: "use_highest_power_action", effect: "damage", target: "RANDOM_OPPONENT", description: "Use highest power action of given effect" },
  conditions: [{ type: "distance_lower_than", value: 2, target: "RANDOM_OPPONENT", description: "Distance lower than or equal given value" }],
});
const rulesManifest = (userId, rules) => ({ items: [{
  entity: "aiProfile", slot: "edit", targetId: userId, name: "Umbral Reaver AI profile safety",
  data: { rules, includeDefaultRules: false },
}] });
const AI = Object.freeze({ userId: "u1", username: "Umbral Reaver", isAi: true, level: 1, rank: "GENIN", aiProfileId: null, jutsus: [], items: [] });

test("an AI-profile write the server re-keys reads back as VERIFIED, not drift", async () => {
  const h = harness();
  h.game.seed("ai", { ...AI });
  h.runner.plan(rulesManifest("u1", [structuredClone(RULE)]), { jobId: "rk" });
  const s = await h.runner.run("rk");

  const stored = [...h.game.tables.aiProfile.values()][0];
  assert.notEqual(JSON.stringify(stored.rules), JSON.stringify([RULE]), "the fixture must really re-key, or this test proves nothing");
  assert.deepEqual(stored.rules, [RULE], "and it must only re-key: the document is unchanged");
  assert.equal(s.items[0].state, "VERIFIED", s.items[0].error ?? "");
  assert.equal(s.items[0].verify, "match");
  assert.deepEqual(s.items[0].diffs, []);
  assert.equal(s.outcome, "success");
});

test("real AI-profile drift is still drift: a changed value, a reordered array, a dropped key", async () => {
  const cases = {
    "a changed nested value": (r) => { r[0].conditions[0].value = 3; },
    "a changed action target": (r) => { r[0].action.target = "SELF"; },
    "a dropped nested key": (r) => { delete r[0].conditions[0].target; },
    "an added nested key": (r) => { r[0].conditions[0].extra = 1; },
    "a null where a value was": (r) => { r[0].conditions[0].value = null; },
  };
  for (const [what, mutate] of Object.entries(cases)) {
    const game = new FakeGame();
    game.seed("ai", { ...AI });
    const h = harness({ game });
    // the write lands, and then the stored document is not what was asserted
    const real = game.handle.bind(game);
    game.handle = (path, input) => {
      const out = real(path, input);
      if (path === "ai.updateAiProfile") { const p = game.tables.aiProfile.get(input.id); if (p) mutate(p.rules); }
      return out;
    };
    h.runner.plan(rulesManifest("u1", [structuredClone(RULE)]), { jobId: "d" });
    const s = await h.runner.run("d");
    assert.equal(s.items[0].verify, "drift", `${what} must be reported as drift`);
    assert.deepEqual(s.items[0].diffs.map((d) => d.key), ["rules"], what);
    assert.equal(s.outcome, "unverified", what);
  }
});

test("rule ORDER is meaning: two rules swapped read back as drift", async () => {
  const other = { action: { type: "end_turn", description: "End turn" }, conditions: [] };
  const game = new FakeGame();
  game.seed("ai", { ...AI });
  const h = harness({ game });
  const real = game.handle.bind(game);
  game.handle = (path, input) => {
    const out = real(path, input);
    if (path === "ai.updateAiProfile") { const p = game.tables.aiProfile.get(input.id); if (p) p.rules.reverse(); }
    return out;
  };
  h.runner.plan(rulesManifest("u1", [structuredClone(RULE), structuredClone(other)]), { jobId: "ord" });
  const s = await h.runner.run("ord");
  assert.equal(s.items[0].verify, "drift");
});

test("a resumed rules write that landed under a re-keyed read-back is confirmed, not orphaned", async () => {
  const h = harness();
  h.game.seed("ai", { ...AI });
  const pid = "p1";
  h.game.tables.aiProfile.set(pid, { id: pid, userId: "u1", rules: rekey(structuredClone([RULE])), includeDefaultRules: false });
  h.game.tables.ai.get("u1").aiProfileId = pid;

  const planned = rulesManifest("u1", [structuredClone(RULE)]);
  h.runner.plan(planned, { jobId: "res" });
  const job = h.journal.get("res");
  h.journal.transition("res", 0, "SENT", { phase: "rules", entityId: "u1", aiProfileId: pid });

  const out = await h.reconciler.resolveSent(h.journal.get("res"), h.journal.get("res").items[0], { planned: planned.items[0] });
  assert.equal(out.action, "confirm", out.note);
  assert.equal(out.landed, true);
  assert.equal(out.phase, "verify");
  assert.ok(job, "the job record exists");
});

// ---------------------------------------------------- 2b: the committed evidence, replayed

test("every 'drift' the committed Godstorm result recorded is a false one, and this comparison says so", () => {
  const bundle = JSON.parse(readFileSync(RESULT, "utf8"));
  const rulesDiffs = bundle.entries
    .filter((e) => e.entity === "aiProfile" && e.asserted)
    .flatMap((e) => e.asserted.fail.map((f) => ({ name: e.name, key: f.k, lines: f.d })));

  assert.equal(rulesDiffs.length, 18, "the bundle holds all 18 AI-profile 'drift' reports");
  for (const d of rulesDiffs) {
    assert.equal(d.key, "rules");
    assert.equal(d.lines.length, 1);
    const m = /^sent (.*)  live (.*)$/s.exec(d.lines[0]);
    assert.ok(m, `${d.name}: the recorded diff is a sent/live pair`);
    const [, sentText, liveText] = m;
    const sent = JSON.parse(sentText), live = JSON.parse(liveText);
    assert.notEqual(sentText, liveText, `${d.name}: the two payloads really did differ as TEXT`);
    assert.ok(deepEqualPayload(sent, live), `${d.name}: ... and are the same DOCUMENT, so this was never drift`);
  }
  // and the bundle's own verdicts are the symptom being fixed
  const verdicts = new Set(bundle.entries.filter((e) => e.entity === "aiProfile").map((e) => e.verdict));
  assert.deepEqual([...verdicts], ["drift"]);
});

// ---------------------------------------------------------------- the comparison itself

test("deepEqualPayload normalises key order and undefined-vs-missing, and nothing else", () => {
  const eq = (a, b, why) => assert.ok(deepEqualPayload(a, b), why);
  const ne = (a, b, why) => assert.ok(!deepEqualPayload(a, b), why);

  // the two normalisations
  eq({ a: 1, b: 2 }, { b: 2, a: 1 }, "key order is not meaning");
  eq({ a: { x: 1, y: 2 } }, { a: { y: 2, x: 1 } }, "nested key order is not meaning either");
  eq({ a: 1, b: undefined }, { a: 1 }, "a key carrying undefined is a key that is not there");
  eq({ a: 1 }, { a: 1, b: undefined }, "in both directions");
  eq([{ p: 1, q: undefined }], [{ q: undefined, p: 1 }], "inside arrays too");

  // strictness kept
  ne({ a: 1 }, { a: 1, b: null }, "null is a value the server stores, not an absence");
  ne({ a: 1, b: null }, { a: 1 }, "in both directions");
  ne({ a: 1 }, { a: "1" }, "1 is not \"1\"");
  ne({ a: 0 }, { a: false }, "0 is not false");
  ne([1, 2], [2, 1], "array order is meaning");
  ne([1, 2], [1, 2, 3], "length is meaning");
  ne({ a: [1] }, { a: 1 }, "an array is not its element");
  ne({ a: { x: 1 } }, { a: { x: 1, y: 2 } }, "an extra nested key is drift");
  ne({ a: { x: 1, y: 2 } }, { a: { x: 1 } }, "and so is a missing one");
  ne(null, {}, "null is not an object");
  ne(undefined, null, "undefined is not null");

  // scalars and dates
  eq([], []); eq({}, {}); eq(0, 0); eq("x", "x"); eq(null, null); eq(undefined, undefined);
  eq(new Date(5), new Date(5)); ne(new Date(5), new Date(6)); ne(new Date(5), 5);
  eq(NaN, NaN, "two unreadable numbers are not a drift report");
});
