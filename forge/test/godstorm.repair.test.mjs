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
import { existsSync } from "node:fs";
import { IDBFactory } from "fake-indexeddb";
import { listInput } from "../src/budget/reader.mjs";
import { deepEqualPayload } from "../src/runner/validate.mjs";
import { parseManifest } from "../src/runner/manifest.mjs";
import { imagePick, imagePicks, unusablePicks } from "../src/core/facts.mjs";
import { ForgeCore } from "../src/core/core.mjs";
import { FakeGame, rekey } from "./fakegame.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const RESULT = join(HERE, "..", "..", "harvests", "inbox", "tnr_results_1789829183863.json");
const REPAIR_53 = join(HERE, "..", "..", "push", "53_godstorm_failed_items_repair.json");

function harness({ game = new FakeGame(), storage = new MemoryStorage(), idb = new IDBFactory() } = {}) {
  return composeForTest({ game, storage, idb });
}

/** A DOM-less core over the fake game, serving one manifest text. */
function headlessCore(text) {
  const storage = new MemoryStorage();
  const clock = fakeClock();
  const d = composeForTest({ game: new FakeGame(), storage, idb: new IDBFactory(), clock });
  d.github = { list: async () => [], text: async () => text, put: async () => ({ sha: "s" }) };
  const notes = [];
  const core = new ForgeCore({ version: "test", storage, now: clock, ...d });
  core.subscribe((n) => notes.push(n));
  return { core, notes, storage, journal: d.journal };
}

// The eight images of the Godstorm repair, with the byte ledger of the processed .webp files the
// operator must pick. Taken from push/53 when it is in the tree (it is prepared on the planning
// branch), and otherwise reproduced here so the gate is tested in either checkout.
const GODSTORM_LEDGER = Object.freeze({
  "bg_godstorm_stormcourt_upper_court.webp": 379928,
  "bg_godstorm_stormcourt_binding_dais_active.webp": 283000,
  "bg_godstorm_stormcourt_binding_dais_released.webp": 256826,
  "ai_godstorm_marrow_starless_monk.webp": 207410,
  "ai_godstorm_marrow_hollow_lantern.webp": 196056,
  "ai_godstorm_marrow_umbral_reaver.webp": 161650,
  "ai_godstorm_marrow_nightveil_sentinel.webp": 115618,
  "ai_godstorm_marrow_warden_of_the_first_dark.webp": 238510,
});
function godstormRepairText() {
  if (existsSync(REPAIR_53)) {
    // WITHOUT its imagePack. This suite pins the MANUAL PICKER contract - the byte ledger that
    // catches a device file whose name is right and whose bytes are not (defect D). push/53 now also
    // binds those eight images to repository blobs, and a bound image deliberately cannot be
    // satisfied by a device file at all, so leaving the pack in would turn these tests into a second,
    // weaker copy of the pack gate instead of cover for the picker path that still exists for every
    // unbound image. The pack path has its own cover in test/imgpack.test.mjs, including an
    // end-to-end pass over this exact committed manifest and pack.
    const { imagePack, ...unpacked } = JSON.parse(readFileSync(REPAIR_53, "utf8"));
    return JSON.stringify(unpacked);
  }
  return JSON.stringify({
    imgSizes: GODSTORM_LEDGER,
    items: Object.keys(GODSTORM_LEDGER).map((f, i) => ({
      entity: "asset", slot: "create", name: `Godstorm image ${i}`, srcId: `gs_img_${i}`,
      data: { name: `Godstorm image ${i}`, hidden: true, type: "STATIC", url: `@img:${f}` },
    })),
  });
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

// ================================================================= defect B: manifest identity
//
// Manifests 50 and 51 differed only in `dedupNames` - one performing the live-name safety read
// before its creates, one not - and both hashed to d5164ee3, so Forge refused to open 51 on the
// grounds that job 50 was already open for "this manifest". The identity that decides whether two
// jobs are the same job must therefore cover execution policy, not only bodies.

const bodies = (extra = {}) => ({
  items: [{ entity: "jutsu", slot: "create", name: "A", srcId: "a", data: { name: "A", description: "d", hidden: true } }],
  ...extra,
});

test("B: two manifests differing only in dedupNames are one manifest by body and two by identity", () => {
  const dedup = parseManifest(bodies({ dedupNames: true }));
  const plain = parseManifest(bodies({ dedupNames: false }));
  assert.equal(dedup.bodyHash, plain.bodyHash, "this is the collision: the bodies are identical");
  assert.notEqual(dedup.hash, plain.hash, "and this is the fix: the runs are not");
});

test("B: every execution-affecting top-level key moves the identity; prose does not", () => {
  const base = parseManifest(bodies());
  const moves = {
    dedupNames: bodies({ dedupNames: true }),
    skipPreflight: bodies({ skipPreflight: true }),
    imgSizes: bodies({ imgSizes: { "a.webp": 10 } }),
  };
  for (const [key, m] of Object.entries(moves)) {
    assert.notEqual(parseManifest(m).hash, base.hash, `${key} changes what the run does`);
  }
  // readBack:false is refused outright on a manifest with items, so its identity is exercised on a
  // capture-only manifest, where it is legal.
  const capOnly = { items: [], capture: { after: [{ proc: "jutsu.getAllNames" }] } };
  assert.notEqual(parseManifest({ ...capOnly, readBack: false }).hash, parseManifest(capOnly).hash);
  // prose is not execution
  assert.equal(parseManifest(bodies({ _note: "a wholly different explanation" })).hash, base.hash);
});

test("B: identity is the behaviour, not its spelling", () => {
  const base = parseManifest(bodies()).hash;
  assert.equal(parseManifest(bodies({ dedupNames: false })).hash, base, "an explicit default is the default");
  assert.equal(parseManifest(bodies({ readBack: true, skipPreflight: false, imgSizes: {} })).hash, base);
});

test("B: a default-policy manifest keeps the identity it already had, so open jobs still attach", () => {
  const legacy = { items: [], capture: { after: [{ proc: "jutsu.getAllNames", input: {} }] } };
  const m = parseManifest(legacy);
  assert.equal(m.hash, "c359fd86", "the pre-policy hash of a default-policy manifest is unchanged");
  assert.equal(m.hash, m.bodyHash);
});

test("B: the committed Godstorm run's recorded hash is this manifest's BODY hash, and its identity has moved", () => {
  const text = readFileSync(join(HERE, "..", "..", "push", "52_godstorm_two_pyramid_final_update_v4.json"), "utf8");
  const m = parseManifest(text);
  const journalHash = JSON.parse(readFileSync(RESULT, "utf8")).journal.manifestHash;
  assert.equal(journalHash, "330fd853", "what the live run recorded");
  assert.equal(m.bodyHash, journalHash, "which is the body hash, reproduced exactly");
  assert.notEqual(m.hash, journalHash, "manifest 52 carries an imgSizes ledger, so its identity moves");
});

test("B: the incident itself - job 50 open, manifest 51 offered - now opens instead of being refused", () => {
  const h = harness();
  const fifty = parseManifest(bodies({ dedupNames: true }));
  const fiftyOne = parseManifest(bodies({ dedupNames: false }));
  h.journal.open({ jobId: "j50", manifestHash: fifty.hash, items: [{ entity: "jutsu", op: "create", name: "A", srcId: "a", payloadHash: "h" }] });
  // the same manifest is still refused: that guard is the point of the hash
  assert.throws(() => h.journal.open({ jobId: "j50b", manifestHash: fifty.hash, items: [{ entity: "jutsu", op: "create", name: "A", srcId: "a", payloadHash: "h" }] }),
    /an open job for this manifest already exists/);
  // a manifest that runs differently is a different manifest
  const ok = h.journal.open({ jobId: "j51", manifestHash: fiftyOne.hash, items: [{ entity: "jutsu", op: "create", name: "A", srcId: "a", payloadHash: "h" }] });
  assert.equal(ok.jobId, "j51");
});

test("B: attach refuses a policy-changed file, and names a pre-policy job for what it is", () => {
  const h = harness();
  const dedupText = JSON.stringify(bodies({ dedupNames: true }));
  const plainText = JSON.stringify(bodies({ dedupNames: false }));
  h.runner.plan(dedupText, { jobId: "att" });
  // same file: fine
  h.runner.attach("att", dedupText);
  // policy flipped under an open job: refused
  assert.throws(() => h.runner.attach("att", plainText), /manifest changed under job att/);

  // a job opened by a bundle that hashed bodies alone: the file still matches that body hash, and
  // the refusal must say so rather than accusing the operator of editing the manifest
  const legacyJob = h.journal.open({ jobId: "old", manifestHash: parseManifest(dedupText).bodyHash, items: [{ entity: "jutsu", op: "create", name: "A", srcId: "a", payloadHash: "h" }] });
  assert.ok(legacyJob);
  assert.throws(() => h.runner.attach("old", dedupText), /opened before manifest identity covered execution policy/);
  assert.throws(() => h.runner.attach("old", dedupText), /Export the job for evidence and start a fresh one/);
});

// ================================================================== defect D: the image picker
//
// The manifest asked for ai_godstorm_marrow_starless_monk.webp; the operator's device handed Forge
// 1000014259.png at 1709179 bytes; the picker showed "picked"; five avatar edits then failed one
// upload at a time inside a live run. The ledger binds the bytes (L17 exists because the Android
// picker renames files), so bytes are checked and a rename is reported.

const FILE = (name, size, type = "image/webp") => ({ name, size, type });
const LEDGER = { "ai_godstorm_marrow_starless_monk.webp": 207410 };
const PICK = "ai_godstorm_marrow_starless_monk.webp";

test("D: the exact Godstorm failure is refused at selection, with the bytes named", () => {
  const p = imagePick(PICK, FILE("1000014259.png", 1709179, "image/png"), LEDGER);
  assert.equal(p.ok, false);
  assert.equal(p.state, "refused");
  assert.match(p.problems.join(" | "), /1709179 bytes; the manifest ledger says .* is 207410/);
  assert.match(p.problems.join(" | "), /over the imageUploader ceiling of 524288/);
  assert.match(p.problems.join(" | "), /image\/png; .* is a webp/);
  assert.equal(p.picked.size, 1709179, "the physical bytes are carried, so a view can show them");
});

test("D: the exact processed WebP is accepted", () => {
  const p = imagePick(PICK, FILE(PICK, 207410), LEDGER);
  assert.equal(p.ok, true);
  assert.equal(p.state, "ready");
  assert.equal(p.renamed, false);
  assert.deepEqual(p.problems, []);
});

test("D: right name, wrong byte count is refused", () => {
  const p = imagePick(PICK, FILE(PICK, 207411), LEDGER);
  assert.equal(p.ok, false);
  assert.match(p.problems[0], /207411 bytes; the manifest ledger says/);
});

test("D: anything over the uploader ceiling is refused even if the ledger agrees with it", () => {
  const p = imagePick("big.webp", FILE("big.webp", 600000), { "big.webp": 600000 });
  assert.equal(p.ok, false);
  assert.match(p.problems.join(" "), /over the imageUploader ceiling of 524288/);
});

test("D: an unledgered image is refused rather than trusted", () => {
  const p = imagePick("nope.webp", FILE("nope.webp", 100), {});
  assert.equal(p.ok, false);
  assert.match(p.problems[0], /no imgSizes entry/);
});

test("D: a non-image, and an image of the wrong type, are refused", () => {
  assert.equal(imagePick(PICK, FILE(PICK, 207410, "application/pdf"), LEDGER).ok, false);
  assert.equal(imagePick(PICK, FILE(PICK, 207410, "image/png"), LEDGER).ok, false);
  // a browser that reports no type at all is not evidence of anything; the ledger still binds
  assert.equal(imagePick(PICK, FILE(PICK, 207410, ""), LEDGER).ok, true);
});

test("D: DOCUMENTED POLICY - a device-renamed file whose bytes match exactly is accepted, and said so", () => {
  // L17 (runner/lints.mjs) requires a byte entry for every @img ref precisely BECAUSE "the Android
  // picker matches a file by size when the name differs". Refusing on the name would break the
  // operator path the ledger was introduced to survive, so the bytes bind and the rename is
  // surfaced. If the reviewer wants the name to bind too, it is one condition here.
  const p = imagePick(PICK, FILE("image_1234.webp", 207410), LEDGER);
  assert.equal(p.ok, true);
  assert.equal(p.renamed, true, "and the view is told, so the operator sees what they actually picked");
});

test("D: an unpicked image is missing, not refused, and replacing a bad pick clears it", () => {
  const files = new Map();
  const first = imagePicks([PICK], files, LEDGER);
  assert.equal(first[0].state, "missing");
  assert.equal(first[0].picked, null);
  assert.equal(unusablePicks(first).length, 1);

  files.set(PICK, FILE("1000014259.png", 1709179, "image/png"));
  assert.equal(imagePicks([PICK], files, LEDGER)[0].state, "refused");

  files.set(PICK, FILE(PICK, 207410));
  const good = imagePicks([PICK], files, LEDGER);
  assert.equal(good[0].state, "ready");
  assert.deepEqual(unusablePicks(good), []);
});

test("D: the eight-image Godstorm repair cannot start with one wrong master PNG", async () => {
  const text = godstormRepairText();
  const { core, notes, journal } = headlessCore(text);
  await core.selectManifest({ name: "53.json", path: "push/53_godstorm_failed_items_repair.json", number: 53, text });
  assert.deepEqual(core.state.selected.problems, []);
  assert.equal(core.state.selected.images.length, 8);

  const sizes = core.state.selected.manifest.imgSizes;
  for (const name of core.state.selected.images) core.runner.files.set(name, FILE(name, sizes[name]));
  // ... and one of them is the original master, exactly as it was on the night
  core.runner.files.set("ai_godstorm_marrow_starless_monk.webp", FILE("1000014259.png", 1709179, "image/png"));

  await core.startJob();
  assert.equal(core.state.jobId, null, "no job was opened");
  assert.equal(journal.listJobs().length, 0, "and none was written to the journal");
  const bad = notes.filter((n) => n.level === "bad").map((n) => n.text).join(" | ");
  assert.match(bad, /image selection\(s\) do not match the manifest/);
  assert.match(bad, /Nothing was sent/);

  // fix the one file and the same job starts
  core.runner.files.set("ai_godstorm_marrow_starless_monk.webp", FILE("ai_godstorm_marrow_starless_monk.webp", sizes["ai_godstorm_marrow_starless_monk.webp"]));
  await core.selectManifest({ name: "53.json", path: "push/53_godstorm_failed_items_repair.json", number: 53, text });
  await core.startJob();
  assert.equal(journal.listJobs().length, 1, "the gate is a contract check, not a refusal to work");
});
