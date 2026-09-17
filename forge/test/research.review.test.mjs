// Regressions for the Phase 1 independent review findings FN1-FN5.
//
// Each block reproduces the exact defect the reviewer demonstrated at `8f15416` and asserts the
// corrected behaviour. They are kept together and named after the findings so a future reader can
// tell what these particular assertions are defending, and so a re-review can run them directly.
//
// Nothing here contacts the game: bodies are synthetic, stores are in-memory, transport is injected.

import { test } from "node:test";
import assert from "node:assert/strict";
import { App } from "../src/ui/app.mjs";
import { materialize, resolveCaptures, buildBundle } from "../src/core/results.mjs";
import { parseManifest } from "../src/runner/manifest.mjs";
import { projectBody, REGISTRY_PIN, REGISTRY_REVISION, capturePolicy } from "../src/research/registry.mjs";
import { captureTier, isLegacyCapture, snapshotKey } from "../src/storage/captures.mjs";
import { jobOutcome, captureOk } from "../src/storage/journal.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const SECRET = "SECRET-REVIEW-4c81f0";

function harness({ game = new FakeGame(), storage = new MemoryStorage() } = {}) {
  const d = composeForTest({ game, storage });
  const app = new App({ version: "forge test", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
  let exported = null;
  app.showExport = (t) => { exported = t; };
  return { ...d, app, storage, game, bundle: async (jobId) => { exported = null; await app.exportJob(jobId); return JSON.parse(exported); } };
}

const build = (job, captures) => buildBundle({ version: "v", now: () => 0, storage: { getItem: () => null } }, job, captures);
function journalOf(capture) {
  const job = { jobId: "j", state: "DONE", items: [], capturesAfter: [capture] };
  return { job, patches: [], get: () => job, annotateJob(_id, patch) { this.patches.push(patch); Object.assign(job, patch); } };
}

// THE EXACT SHAPES runner.mjs and captures.mjs wrote at the Phase 1 base `77f02c3`, before tiers
// existed. Transcribed rather than produced, because the point of the test is the upgrade path: the
// code that wrote them is gone, and a record in an operator's browser is all that is left of it.
const BASE_CAPTURE = Object.freeze({
  phase: "after", proc: "quests.get", input: { id: "q1" }, ok: true, rows: 1, error: null,
  persist: "full", snapshotKey: "j::after::0", persistOk: true, persistError: null, bytes: 44,
});
const BASE_SNAPSHOT = Object.freeze({
  key: "j::after::0", jobId: "j", phase: "after", ordinal: 0, path: "quests.get", id: "q1",
  entity: "quest", input: { id: "q1" }, data: { id: "q1", name: "Exact prior body" },
  at: "2026-09-16T00:00:00.000Z", bytes: 44,
});

// ---------------------------------------------------------------- FN1
test("FN1: a Phase 0 full capture still resolves to its exact body after the upgrade", async () => {
  assert.equal(captureTier(BASE_CAPTURE), "repo-safe", "a pre-tier persist:full record is a repo-safe capture");
  assert.equal(isLegacyCapture(BASE_CAPTURE), true);
  const journal = journalOf({ ...BASE_CAPTURE });
  let lookups = 0;
  const captures = await resolveCaptures({ journal, cache: { getSnapshot: async () => { lookups++; return { ...BASE_SNAPSHOT }; } } }, "j");
  const bundle = build(journal.job, captures);
  assert.equal(lookups, 1, "the snapshot must actually be read; Phase 1 briefly never looked");
  assert.deepEqual(bundle.captures[0].data, BASE_SNAPSHOT.data, "the exact prior body, not an omission");
  assert.equal(bundle.captures[0].tier, "repo-safe");
  assert.equal(bundle.captures[0].persistOk, true);
  assert.equal(bundle.outcome, "success");
  assert.ok(journal.patches.length, "and the verdict is written back, as it is for a Phase 1 capture");
});

test("FN1: a Phase 0 capture whose body never landed stays a failure", () => {
  const failed = { ...BASE_CAPTURE, persistOk: false, persistError: "capture snapshot write failed: quota" };
  assert.equal(captureOk(failed), false);
  assert.equal(jobOutcome(journalOf(failed).job), "failed", "a capture-only job must not go green");
  assert.equal(jobOutcome({ state: "DONE", items: [{ state: "VERIFIED", verify: "match" }], capturesAfter: [failed] }),
    "unverified", "nor may a job that also wrote");
});

test("FN1: a missing or oversized Phase 0 snapshot is an explicit non-success, with no re-read", async () => {
  const gone = await materialize({ getSnapshot: async () => null }, { ...BASE_CAPTURE });
  assert.equal(gone.persistOk, false);
  assert.match(gone.persistError, /is gone, so the body cannot be exported without a second read/);
  assert.ok(!("data" in gone));
  const huge = await materialize({ getSnapshot: async () => ({ ...BASE_SNAPSHOT, bytes: 9_000_000 }) }, { ...BASE_CAPTURE });
  assert.equal(huge.persistOk, false);
  assert.match(huge.persistError, /over the \d+-byte repo-safe capture ceiling/);
  assert.ok(!("data" in huge));
});

test("FN1: the legacy mapping is narrow — it adopts nothing it does not recognise", async () => {
  // Only `persist: "full"` maps. An unknown persist value, or a record with neither key, is a
  // summary capture that kept no body, exactly as it was before tiers.
  for (const persist of [undefined, "summary", "fields", "FULL", true, 1]) {
    assert.equal(captureTier({ ok: true, persist }), null, `persist ${JSON.stringify(persist)} must not be adopted`);
  }
  // ...and a legacy record naming a path that is not repo-safe is refused rather than interpreted.
  const wrong = await materialize({ getSnapshot: async () => ({ ...BASE_SNAPSHOT, path: "combat.getBattleEntries" }) },
    { ...BASE_CAPTURE, proc: "combat.getBattleEntries" });
  assert.equal(wrong.persistOk, false);
  assert.match(wrong.persistError, /predates persistence tiers and names combat\.getBattleEntries, which is not an approved repo-safe path/);
  assert.ok(!("data" in wrong));
});

// ---------------------------------------------------------------- FN2
test("FN2: the projection retained with the body is authority; the journal may not redirect it", async () => {
  const snap = { key: "j::after::0", path: "quests.get", tier: "projected", projection: ["id"],
    data: { id: "q1", secret: SECRET }, at: "t", bytes: 40 };
  const base = { phase: "after", proc: "quests.get", input: { id: "q1" }, ok: true, rows: 1, error: null,
    persist: "projected", tier: "projected", projection: ["id"], snapshotKey: "j::after::0", persistOk: true, persistError: null };

  // agreeing journal: exports the declared field
  const good = await materialize({ getSnapshot: async () => snap }, { ...base });
  assert.deepEqual(good.data, { id: "q1" });

  // every way a stale or edited journal could try to redirect it
  for (const projection of [["secret"], ["id", "secret"], [], null, ["__proto__"], ["*"], ["id "]]) {
    const journal = journalOf({ ...base, projection });
    const bundle = build(journal.job, await resolveCaptures({ journal, cache: { getSnapshot: async () => snap } }, "j"));
    const [capture] = bundle.captures;
    assert.ok(!("data" in capture) || !JSON.stringify(capture.data).includes(SECRET),
      `journal projection ${JSON.stringify(projection)} must not export the undeclared field`);
    if (projection && projection.length) {
      assert.equal(capture.persistOk, false, `journal projection ${JSON.stringify(projection)} must be a non-success`);
      assert.match(capture.persistError, /the retained declaration is authority/);
    }
    assert.ok(!JSON.stringify(bundle).includes(SECRET), "and nothing leaks anywhere else in the bundle");
  }
});

test("FN2: a retained declaration is re-validated at the leak boundary, as a verdict not a throw", async () => {
  const bad = { key: "j::after::0", path: "quests.get", tier: "projected", projection: ["__proto__"],
    data: JSON.parse('{"id":"q1","__proto__":{"polluted":"YES"}}'), at: "t", bytes: 40 };
  const capture = { phase: "after", proc: "quests.get", input: { id: "q1" }, ok: true, rows: 1, error: null,
    persist: "projected", tier: "projected", projection: ["__proto__"], snapshotKey: "j::after::0", persistOk: true, persistError: null };
  const out = await materialize({ getSnapshot: async () => bad }, capture);
  assert.equal(out.persistOk, false, "an inadmissible retained declaration fails the export");
  assert.match(out.persistError, /is not admissible/);
  assert.ok(!("data" in out), "and applies nothing");
  // a snapshot with no declaration at all cannot fall back to anything
  const none = await materialize({ getSnapshot: async () => ({ ...bad, projection: null }) }, { ...capture, projection: null });
  assert.equal(none.persistOk, false);
  assert.match(none.persistError, /no projection was retained with this capture's body/);
  assert.ok(!("data" in none));
});

// ---------------------------------------------------------------- FN3
test("FN3: a declared path may not stop on a structure and ship the subtree", () => {
  const body = { id: "q1", content: { title: "Public", note: SECRET, nested: { hidden: SECRET }, objectives: [{ id: "n1", unseen: SECRET }] } };
  for (const fields of [["content"], ["content.nested"], ["content.objectives"]]) {
    const r = projectBody(body, fields);
    assert.equal(r.ok, false, `${fields[0]} is a structure and must not project as a field`);
    assert.deepEqual(r.missing, fields);
    assert.equal("data" in r, false, "and no partial object is emitted");
  }
  // the supported way to say it: name the leaves, including through an array
  const ok = projectBody(body, ["id", "content.title", "content.objectives.id"]);
  assert.deepEqual(ok.data, { id: "q1", content: { title: "Public", objectives: [{ id: "n1" }] } });
  assert.ok(!JSON.stringify(ok.data).includes(SECRET));
  // a list of scalars is a field, not a subtree, and is allowed
  assert.deepEqual(projectBody({ tags: ["a", "b"] }, ["tags"]).data, { tags: ["a", "b"] });
  // a field added to the record later cannot ride along, because it was never named
  const later = projectBody({ ...body, content: { ...body.content, objectives: [{ id: "n1", addedLater: SECRET }] } }, ["content.objectives.id"]);
  assert.deepEqual(later.data, { content: { objectives: [{ id: "n1" }] } });
  // descending through a scalar is a failure, not a silent drop
  assert.equal(projectBody({ id: "q1" }, ["id.deeper"]).ok, false);
});

test("FN3: a structured terminal is an honest capture failure end to end", async () => {
  const h = harness();
  h.game.seed("quest", { id: "q1", name: "N", content: { objectives: [{ id: "n1", note: SECRET }] } });
  h.runner.plan({ items: [], capture: { after: [
    { proc: "quests.get", input: { id: "q1" }, persist: "projected", projection: ["content.objectives"] },
  ] } }, { jobId: "struct" });
  await h.runner.run("struct");
  assert.equal(jobOutcome(h.journal.get("struct")), "failed");
  const bundle = await h.bundle("struct");
  assert.equal(bundle.captures[0].persistOk, false);
  assert.match(bundle.captures[0].persistError, /projection failed: content\.objectives/);
  assert.match(bundle.captures[0].persistError, /NOT substituted and NOT exported/);
  assert.ok(!JSON.stringify(bundle).includes(SECRET));
});

// ---------------------------------------------------------------- FN4
test("FN4: a capture retains the source pin and registry revision that admitted it", async () => {
  const h = harness();
  h.game.seedBattle({ battleId: "b1", battleType: "COMBAT", createdAt: "t", attackedId: "a", defenderId: "d", attacker: {}, defender: {} },
    [{ id: "x", battleId: "b1", userId: "me", battleRound: 1, battleVersion: 1 }]);
  h.runner.plan({ items: [], capture: { after: [{ proc: "combat.getBattleEntries", input: { battleId: "b1" }, persist: "local-only" }] } }, { jobId: "prov" });
  await h.runner.run("prov");

  const expected = capturePolicy("combat.getBattleEntries");
  assert.equal(expected.pin, REGISTRY_PIN);
  assert.equal(expected.registry, REGISTRY_REVISION);
  const entry = h.journal.get("prov").capturesAfter[0];
  assert.deepEqual(entry.policy, expected, "the journal entry names the contract that admitted the read");
  const snap = await h.cache.getSnapshot(snapshotKey("prov", "after", 0));
  assert.deepEqual(snap.policy, expected, "and so does the body, so the two cannot be separated");
  const bundle = await h.bundle("prov");
  assert.deepEqual(bundle.captures[0].policy, expected, "and the export carries it");
  assert.match(expected.source, /combat\.ts:\d+/);
});

test("FN4: export never fabricates provenance for a record that has none", async () => {
  // A Phase 0 capture predates the stamp. Materializing it under this build must show it as
  // carrying no policy identity rather than labelling it with today's registry.
  const out = await materialize({ getSnapshot: async () => ({ ...BASE_SNAPSHOT }) }, { ...BASE_CAPTURE });
  assert.equal(out.persistOk, true);
  assert.equal("policy" in out, false, "an old record must not be relabelled with the current policy");
  assert.ok(!JSON.stringify(out).includes(REGISTRY_REVISION));
});

test("FN4: the registry revision is a content identity, not a version string", async () => {
  // It is derived from the admission-relevant fields, so it cannot be left stale by a registry edit.
  assert.match(REGISTRY_REVISION, /^[0-9a-f]{8}$/);
  const { RESEARCH_READS } = await import("../src/research/registry.mjs");
  assert.notEqual(REGISTRY_REVISION, RESEARCH_READS["combat.getBattleEntries"].tier);
  // two different rows' policies differ in source but agree on pin and revision
  const a = capturePolicy("combat.getBattleEntries"), b = capturePolicy("quests.get");
  assert.equal(a.registry, b.registry);
  assert.notEqual(a.source, b.source);
  assert.notEqual(a.tier, b.tier);
});

// ---------------------------------------------------------------- FN5
test("FN5: a rate limit on a later page keeps the whole walk's per-page evidence", async () => {
  const h = harness({ game: new FakeGame() });
  h.game.seedBattle({ battleId: "b1", battleType: "COMBAT", createdAt: "t", attackedId: "a", defenderId: "d", attacker: {}, defender: {} },
    Array.from({ length: 10 }, (_, i) => ({ id: `x${i}`, battleId: "b1", userId: "me", battleRound: 10 - i, battleVersion: 1 })));
  // page 1 succeeds; page 2 is refused by the limiter
  let n = 0;
  const real = h.game.handle.bind(h.game);
  h.game.handle = (path, input) => {
    if (path === "combat.getBattleEntries" && ++n === 2) return { ok: false, error: { code: "TOO_MANY_REQUESTS", httpStatus: 429, message: "too fast", path, zodError: null } };
    return real(path, input);
  };
  h.runner.plan({ items: [], capture: { after: [
    { proc: "combat.getBattleEntries", input: { battleId: "b1", limit: 2 }, persist: "local-only", pages: 3 },
  ] } }, { jobId: "lim" });
  const s = await h.runner.run("lim");

  assert.equal(s.state, "PAUSED", "the rate-limit stop still holds");
  const job = h.journal.get("lim");
  assert.equal(job.pause.reason, "TOO_MANY_REQUESTS");
  assert.equal(jobOutcome(job), "open", "and it is not falsely classified complete");

  const [attempt] = job.capturesAfterAttempts;
  assert.ok(attempt, "the abandoned attempt must be journaled; Phase 1 lost it with the stack");
  assert.equal(attempt.abandoned, true);
  assert.equal(attempt.ok, false);
  assert.equal(attempt.complete, false);
  assert.equal(attempt.persistOk, false);
  assert.equal(attempt.pages.length, 2, "the page that succeeded and the page that tripped the limiter");
  assert.deepEqual(attempt.pages.map((p) => p.ok), [true, false]);
  assert.deepEqual(attempt.pages.map((p) => p.rows), [2, 0]);
  assert.equal(attempt.pages[1].error, "TOO_MANY_REQUESTS");
  assert.deepEqual(attempt.pages.map((p) => p.input.offset), [undefined, 2], "the exact inputs that were sent");
  assert.equal(job.capturesAfter, undefined, "the completed list is untouched, so resume re-reads this capture");

  // the evidence reaches an exported bundle rather than living only in the journal
  const bundle = await h.bundle("lim");
  const exported = bundle.captures.find((c) => c.abandoned);
  assert.ok(exported, "a paused job's bundle carries the attempt");
  assert.equal(exported.pages.length, 2);
  assert.match(exported.persistError, /stopped on a rate limit after 2 page\(s\)/);
});

test("FN5: a resumed attempt is a new record beside the abandoned one, never an overwrite", async () => {
  const h = harness();
  h.game.seedBattle({ battleId: "b1", battleType: "COMBAT", createdAt: "t", attackedId: "a", defenderId: "d", attacker: {}, defender: {} },
    Array.from({ length: 3 }, (_, i) => ({ id: `x${i}`, battleId: "b1", userId: "me", battleRound: 3 - i, battleVersion: 1 })));
  let fail = true;
  const real = h.game.handle.bind(h.game);
  h.game.handle = (path, input) => {
    if (path === "combat.getBattleEntries" && fail) { fail = false; return { ok: false, error: { code: "TOO_MANY_REQUESTS", httpStatus: 429, message: "too fast", path, zodError: null } }; }
    return real(path, input);
  };
  const manifest = { items: [], capture: { after: [{ proc: "combat.getBattleEntries", input: { battleId: "b1", limit: 2 }, persist: "local-only", pages: 2 }] } };
  h.runner.plan(manifest, { jobId: "again" });
  await h.runner.run("again");
  assert.equal(h.journal.get("again").capturesAfterAttempts.length, 1);

  // clear the tripped limiter the way waiting out the window would, then resume
  h.budget.log.clearTrip();
  await h.runner.run("again"); // the capture is read again from the start
  const job = h.journal.get("again");
  assert.equal(job.capturesAfterAttempts.length, 1, "the earlier attempt is preserved, not rewritten");
  assert.ok(Array.isArray(job.capturesAfter) && job.capturesAfter.length === 1, "and the resumed read is its own record");
  assert.equal(job.capturesAfter[0].abandoned, undefined);
});
