// Capture persistence tiers and input-aware paged reads, end to end
// (state/prompt_forge_next_phase1.md §6 and §7, RUL-2026-09-17-001).
//
// The claim this file exists to hold: a body's TIER decides where it is allowed to end up, and no
// path through the product can move it somewhere wider. A local-only body is retained exactly and
// exported never; a projected body exports its declared fields and nothing beside them; a repo-safe
// body exports whole, as it always did. Every read is driven through FakeClient; nothing here
// contacts the game.
//
// The leak tests do not check "the bundle has no `data` key". They serialize the ENTIRE artefact —
// the bundle, the embedded journal, localStorage, and the object the export/clipboard path hands
// out — and look for the secret's own bytes, because the way a body leaks is by riding along
// somewhere nobody thought to look.

import { test } from "node:test";
import assert from "node:assert/strict";
import { App } from "../src/ui/app.mjs";
import { parseManifest } from "../src/runner/manifest.mjs";
import { snapshotKey, MAX_FULL_CAPTURE_BYTES, MAX_LOCAL_CAPTURE_BYTES, queryCaptureKey } from "../src/storage/captures.mjs";
import { canonicalKey, canonicalInput } from "../src/research/registry.mjs";
import { jobOutcome } from "../src/storage/journal.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

// A distinctive string that exists nowhere else, so a substring search over a whole artefact is a
// real leak test rather than a shape assertion.
const SECRET = "SECRET-PLAYER-NAME-b7f3a91c";

function harness({ game = new FakeGame(), storage = new MemoryStorage() } = {}) {
  const d = composeForTest({ game, storage });
  const committed = [];
  const app = new App({
    version: "forge test", storage, now: d.clock, ...d,
    github: { list: async () => [], text: async () => "", put: async (path, text, msg) => { committed.push({ path, text, msg }); return { sha: "deadbeef" }; } },
  });
  let exported = null;
  app.showExport = (t) => { exported = t; };
  return {
    ...d, app, storage, game, committed,
    bundle: async (jobId) => { exported = null; await app.exportJob(jobId); return JSON.parse(exported); },
    exportedText: () => exported,
  };
}

/** One battle whose history row and action log both carry the secret in a player-name position. */
function seedBattles(game, { battles = 1, actions = 3 } = {}) {
  for (let b = 0; b < battles; b++) {
    const battleId = `bat${b}`;
    game.seedBattle(
      {
        battleId, battleType: "COMBAT", createdAt: `2026-09-1${b}T00:00:00.000Z`,
        attackedId: `atk${b}`, defenderId: `def${b}`,
        attacker: { username: `${SECRET}-atk${b}`, userId: `atk${b}`, avatar: "https://utfs.io/f/a.webp" },
        defender: { username: `${SECRET}-def${b}`, userId: `def${b}`, avatar: "https://utfs.io/f/d.webp" },
      },
      Array.from({ length: actions }, (_, i) => ({ id: `${battleId}-a${i}`, battleId, userId: i % 2 ? "me" : "them", battleRound: actions - i, battleVersion: 1, description: `${SECRET} struck for ${i}`, basic: i === 0 })),
    );
  }
}

const runCaptures = async (h, jobId, after) => {
  h.runner.plan({ items: [], capture: { after } }, { jobId });
  return h.runner.run(jobId);
};

/** Everything an operator or a sync could carry out of the browser, as one string. */
function allExportSurfaces(h, bundle) {
  // Walked through the Storage API rather than a helper, so this is every key the journal, the
  // idmap and the settings actually hold - the places a body would end up if something serialized
  // it by accident.
  const local = {};
  for (let i = 0; i < h.storage.length; i++) { const k = h.storage.key(i); local[k] = h.storage.getItem(k); }
  assert.ok(Object.keys(local).length > 0, "the localStorage sweep must actually be looking at something");
  return JSON.stringify({
    bundle,
    exportedText: h.exportedText(),
    committed: h.committed,
    localStorage: local,
    journal: h.journal.listJobs().map((j) => h.journal.get(j.jobId)),
    // the verdict objects a screen or a diagnostic dump would render
    errors: bundle.captures.map((c) => ({ ...c, err: c.persistError })),
  });
}

// ---------------------------------------------------------------- local-only
test("local-only: the exact body is retained locally and reaches no export path at all", async () => {
  const h = harness();
  seedBattles(h.game, { battles: 2, actions: 4 });
  const s = await runCaptures(h, "loc", [
    { proc: "combat.getBattleHistory", input: { combatTypes: ["COMBAT"] }, persist: "local-only" },
  ]);
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success", "retaining a local-only body IS the job succeeding");

  // the exact body is in the immutable snapshot store, secret and all
  const snap = await h.cache.getSnapshot(snapshotKey("loc", "after", 0));
  assert.ok(snap, "the body must actually be retained; local-only is not a way of not keeping it");
  assert.equal(snap.tier, "local-only");
  assert.equal(snap.data.length, 2);
  assert.ok(JSON.stringify(snap.data).includes(SECRET), "the retained body is exact, not redacted");

  // ...and nowhere else
  const bundle = await h.bundle("loc");
  const [capture] = bundle.captures;
  assert.equal(capture.tier, "local-only");
  assert.equal(capture.persistOk, true, "the capture did what it promised");
  assert.equal(capture.localOnly, true);
  assert.ok(!("data" in capture), "a local-only capture never grows a body on export");
  assert.equal(capture.rows, 2, "the count is evidence; the rows are not");
  assert.ok(!allExportSurfaces(h, bundle).includes(SECRET),
    "the raw body must not appear in the bundle, the embedded journal, the export payload, the GitHub commit or localStorage");
});

test("local-only survives a GitHub sync without the body riding along", async () => {
  const h = harness();
  seedBattles(h.game, { battles: 1, actions: 2 });
  h.storage.setItem("tnr_bk_gh_v1", JSON.stringify({ on: true, pat: "ghp_fake", owner: "o", repo: "r", branch: "main" }));
  await runCaptures(h, "sync", [{ proc: "combat.getBattleEntries", input: { battleId: "bat0" }, persist: "local-only" }]);
  await h.app.exportJob("sync");
  assert.equal(h.committed.length, 1, "the bundle was committed");
  assert.ok(!h.committed[0].text.includes(SECRET), "and it carried no local-only body");
  assert.ok(h.committed[0].text.includes("local-only"), "it says which tier withheld it");
});

test("a local-only body over its own ceiling is an explicit failure, never truncated", async () => {
  const h = harness();
  h.game.seedBattle(
    { battleId: "big", battleType: "COMBAT", createdAt: "2026-09-10T00:00:00.000Z", attackedId: "a", defenderId: "d", attacker: {}, defender: {} },
    [{ id: "x", battleId: "big", userId: "me", battleRound: 1, battleVersion: 1, description: "x".repeat(MAX_LOCAL_CAPTURE_BYTES + 1) }]);
  const s = await runCaptures(h, "big", [{ proc: "combat.getBattleEntries", input: { battleId: "big" }, persist: "local-only" }]);
  assert.equal(jobOutcome(h.journal.get("big")), "failed");
  const bundle = await h.bundle("big");
  const [capture] = bundle.captures;
  assert.equal(capture.ok, true, "the READ succeeded; it is the persistence that did not");
  assert.equal(capture.persistOk, false);
  assert.match(capture.persistError, /over the \d+-byte local-only capture ceiling/);
  assert.match(capture.persistError, /NOT truncated/);
  assert.equal(await h.cache.getSnapshot(snapshotKey("big", "after", 0)), null, "nothing oversized was stored at all");
  // the two ceilings are different numbers for different reasons, and neither is the other's
  assert.notEqual(MAX_LOCAL_CAPTURE_BYTES, MAX_FULL_CAPTURE_BYTES);
});

// ---------------------------------------------------------------- projected
test("projected: only the declared LEAF fields export, including through an array", async () => {
  const h = harness();
  h.game.seed("quest", {
    id: "q1", name: "The Waystation", rank: "B", hidden: false,
    // each objective carries an undeclared field, which is how a projection leaks when a path is
    // allowed to stop on a structure: the element object would ship whole, this field included.
    content: { objectives: [{ id: "n1", type: "dialog", note: SECRET }], reward: { money: 0 }, note: SECRET },
    description: SECRET,
  });
  const fields = ["id", "name", "content.objectives.id", "content.objectives.type"];
  const s = await runCaptures(h, "proj", [
    { proc: "quests.get", input: { id: "q1" }, persist: "projected", projection: fields },
  ]);
  assert.equal(s.outcome, "success");
  const bundle = await h.bundle("proj");
  const [capture] = bundle.captures;
  assert.equal(capture.tier, "projected");
  assert.equal(capture.persistOk, true);
  assert.deepEqual(capture.projection, fields);
  assert.deepEqual(capture.data, { id: "q1", name: "The Waystation", content: { objectives: [{ id: "n1", type: "dialog" }] } },
    "exactly the declared leaves, nested exactly where they were, and nothing beside them");
  assert.ok(!("description" in capture.data) && !("rank" in capture.data) && !("hidden" in capture.data));
  assert.ok(!("reward" in capture.data.content) && !("note" in capture.data.content));
  assert.ok(!("note" in capture.data.content.objectives[0]), "an undeclared field inside a selected element must not ride along");
  assert.ok(!allExportSurfaces(h, bundle).includes(SECRET), "no undeclared field escapes by any route");
  // the RAW body still exists locally: projection narrows the export, not the evidence
  const snap = await h.cache.getSnapshot(snapshotKey("proj", "after", 0));
  assert.equal(snap.tier, "projected");
  assert.equal(snap.data.description, SECRET);
});

test("a declared field that is absent is a projection FAILURE, never a fallback to the full body", async () => {
  const h = harness();
  h.game.seed("quest", { id: "q2", name: "Loud Way", content: { objectives: [] }, description: SECRET });
  await runCaptures(h, "miss", [
    { proc: "quests.get", input: { id: "q2" }, persist: "projected", projection: ["id", "content.nowhere", "alsoMissing"] },
  ]);
  assert.equal(jobOutcome(h.journal.get("miss")), "failed");
  const bundle = await h.bundle("miss");
  const [capture] = bundle.captures;
  assert.equal(capture.ok, true);
  assert.equal(capture.persistOk, false);
  assert.match(capture.persistError, /projection failed: content\.nowhere, alsoMissing are absent/);
  assert.match(capture.persistError, /full body is NOT substituted and NOT exported/);
  assert.ok(!("data" in capture), "not the full body, and not a partial object either");
  assert.ok(!allExportSurfaces(h, bundle).includes(SECRET));
});

test("a wildcard, an index, a spread or a prototype walk is not a projection", () => {
  for (const field of ["*", "content.*", "content[0]", "", "a..b", "__proto__.polluted", "constructor.prototype", "a b", 7, null, {}]) {
    assert.throws(
      () => parseManifest({ items: [], capture: { after: [{ proc: "quests.get", input: { id: "q" }, persist: "projected", projection: [field] }] } }),
      /(is not a declared field path|is refused)/,
      JSON.stringify(field));
  }
  // and a projected capture with no declaration at all is refused rather than defaulted to "all"
  assert.throws(
    () => parseManifest({ items: [], capture: { after: [{ proc: "quests.get", input: { id: "q" }, persist: "projected" }] } }),
    /needs a "projection" \(or "select"\) list of field paths/);
});

test("a projection declared under a tier that cannot use it is an advisory, not a silent no-op", () => {
  // This is push/05's exact shape: a `select` list with no persist key. It stays runnable, and the
  // operator is told in a sentence that the projection is not being applied.
  const m = parseManifest({ items: [], capture: { after: [{ proc: "combat.getBattleHistory", input: { combatTypes: ["COMBAT"] }, select: ["battleId", "battleType"] }] } });
  assert.equal(m.capture.after[0].tier, null);
  assert.equal(m.capture.after[0].projection, null);
  assert.equal(m.warnings.length, 1);
  assert.match(m.warnings[0], /2-field projection is declared but persist is "summary", so NO projection is applied/);
});

// ---------------------------------------------------------------- repo-safe is unchanged
test("repo-safe still round-trips the exact body, and only for an approved path", async () => {
  const h = harness();
  const asset = { id: "a1", name: "Chase Alley Plate", type: "STATIC", image: "https://utfs.io/f/x.webp", hidden: false };
  h.game.seed("asset", asset);
  await runCaptures(h, "rs", [{ proc: "gameAsset.get", input: { id: "a1" }, persist: "repo-safe" }]);
  const bundle = await h.bundle("rs");
  assert.deepEqual(bundle.captures[0].data, asset, "the exact decoded body, as before tiers existed");
  assert.equal(bundle.captures[0].tier, "repo-safe");
  // an unapproved path cannot ask for it, under either spelling
  for (const persist of ["full", "repo-safe"]) {
    assert.throws(() => parseManifest({ items: [], capture: { after: [{ proc: "combat.getBattleEntries", input: { battleId: "b" }, persist }] } }),
      /the registry admits "local-only" for this path/);
  }
});

test("export can downgrade a tier but never widen one: the snapshot's own tier wins", async () => {
  const h = harness();
  seedBattles(h.game, { battles: 1, actions: 2 });
  await runCaptures(h, "tamper", [{ proc: "combat.getBattleEntries", input: { battleId: "bat0" }, persist: "local-only" }]);
  // Forge a journal entry claiming the body is repo-safe, exactly as a stale or edited journal
  // could. The snapshot still says local-only, and the narrower answer is the one that is used.
  const job = h.journal.get("tamper");
  h.journal.annotateJob("tamper", { capturesAfter: job.capturesAfter.map((c) => ({ ...c, tier: "repo-safe", persist: "full" })) });
  const bundle = await h.bundle("tamper");
  assert.equal(bundle.captures[0].tier, "local-only");
  assert.ok(!("data" in bundle.captures[0]));
  assert.ok(!allExportSurfaces(h, bundle).includes(SECRET));
});

test("a missing snapshot is an explicit non-success and is never re-read to fix the export", async () => {
  const h = harness();
  seedBattles(h.game, { battles: 1, actions: 2 });
  await runCaptures(h, "gone", [{ proc: "combat.getBattleEntries", input: { battleId: "bat0" }, persist: "local-only" }]);
  await h.cache.deleteSnapshot(snapshotKey("gone", "after", 0));
  const before = h.game.calls.length;
  const bundle = await h.bundle("gone");
  assert.equal(h.game.calls.length, before, "the export issued no read");
  assert.equal(bundle.captures[0].persistOk, false);
  assert.match(bundle.captures[0].persistError, /is gone, so the body cannot be exported without a second read; it was not re-read/);
});
