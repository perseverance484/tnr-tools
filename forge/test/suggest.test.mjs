// Suggest mode: edits go to the content review desk instead of being saved.
import test from "node:test";
import assert from "node:assert/strict";
import { parseManifest } from "../src/runner/manifest.mjs";
import { jobOutcome } from "../src/storage/journal.mjs";
import { runHeadline } from "../src/core/facts.mjs";
import { ForgeCore } from "../src/core/core.mjs";
import { composeForTest } from "./compose.mjs";
import { ReviewGame } from "./review.game.mjs";

const edit = (extra = {}) => ({ entity: "jutsu", slot: "edit", name: "Ember Step", targetId: "j1", data: { description: "Hotter now." }, ...extra });
const manifest = (items = [edit()], extra = {}) => ({ mode: "suggest", suggestion: { category: "BALANCE", title: "Ember tune", rationale: "Ember Step was underused in arena data." }, items, ...extra });

function setup() {
  const game = new ReviewGame();
  game.seed("jutsu", { id: "j1", name: "Ember Step", description: "Warm.", hidden: false, effects: [] });
  const d = composeForTest({ game });
  return { ...d, game };
}

test("suggest mode is for edits of supported records, with a title and rationale", () => {
  assert.ok(parseManifest(manifest()).policy.suggest);
  assert.throws(() => parseManifest(manifest([{ entity: "jutsu", slot: "create", name: "X", srcId: "x", data: { name: "X", hidden: true } }])), /only change existing records/);
  assert.throws(() => parseManifest(manifest(undefined, { suggestion: { title: "T1" } })), /title and rationale/);
  assert.throws(() => parseManifest(manifest(undefined, { suggestion: { title: "Ember", rationale: "long enough reason", category: "NOPE" } })), /category must be one of/);
  assert.throws(() => parseManifest({ ...manifest(), mode: "maybe" }), /mode must be/);
  // without mode the manifest is an ordinary write, and its identity is unchanged by the feature
  const plain = { items: [edit()] };
  assert.equal(parseManifest(plain).policy.suggest, undefined);
  assert.equal(parseManifest({ ...plain, mode: "write" }).hash, parseManifest(plain).hash);
});

test("an edit is sent for review, the record is untouched, and the suggestion's id is recorded", async () => {
  const d = setup();
  d.runner.plan(JSON.stringify(manifest()), { jobId: "s1", manifestPath: "push/s.json" });
  await d.runner.run("s1");
  assert.equal(d.game.rows("jutsu")[0].description, "Warm.", "nothing changed in the game");
  assert.equal(d.game.proposals.length, 1);
  const p = d.game.proposals[0];
  assert.deepEqual(Object.keys(p.after), ["description"]);
  assert.match(p.title, /^Ember tune · Ember Step \[\w+-1\]$/);
  const job = d.journal.get("s1");
  assert.equal(job.state, "DONE");
  assert.equal(job.items[0].verify, "suggested");
  assert.equal(job.items[0].suggestion.id, p.id);
  assert.equal(jobOutcome(job), "success");
  assert.match(runHeadline(job, { state: "DONE", counts: { VERIFIED: 1 }, verify: { match: 0, drift: 0, unread: 0 } }).text, /1 sent for review/);
  assert.ok(!d.game.calls.some((c) => c.path === "jutsu.update"), "never saved");
});

test("an edit the live record already holds is verified, not suggested", async () => {
  const d = setup();
  d.runner.plan(JSON.stringify(manifest([edit({ data: { description: "Warm." } })])), { jobId: "s2" });
  await d.runner.run("s2");
  const it = d.journal.get("s2").items[0];
  assert.equal(it.state, "VERIFIED"); assert.equal(it.verify, "match");
  assert.equal(d.game.proposals.length, 0);
});

test("a lost response is settled from the review queue on resume: found is not sent twice", async () => {
  const d = setup();
  d.game.dropCreateResponse = true;
  d.runner.plan(JSON.stringify(manifest()), { jobId: "s3" });
  await d.runner.run("s3");
  assert.equal(d.journal.get("s3").state, "PAUSED");
  await d.runner.resume("s3");
  assert.equal(d.game.proposals.length, 1, "the suggestion that landed was found, not resent");
  assert.equal(d.journal.get("s3").items[0].suggestion.id, d.game.proposals[0].id);
});

test("a suggestion that never landed is sent again on resume", async () => {
  const d = setup();
  d.game.dropCreateResponse = true;
  d.runner.plan(JSON.stringify(manifest()), { jobId: "s4" });
  await d.runner.run("s4");
  d.game.proposals.length = 0; // it never reached the desk
  await d.runner.resume("s4");
  assert.equal(d.game.proposals.length, 1);
  assert.equal(d.journal.get("s4").state, "DONE");
});

test("Check suggestions records each suggestion's current status", async () => {
  const d = setup();
  d.runner.plan(JSON.stringify(manifest()), { jobId: "s5" });
  await d.runner.run("s5");
  d.game.proposals[0].status = "REJECTED"; d.game.proposals[0].reviewNote = "too strong";
  const core = new ForgeCore({ ...d, version: "t", now: d.clock });
  await core.checkSuggestions("s5");
  const s = d.journal.get("s5").items[0].suggestion;
  assert.equal(s.status, "REJECTED"); assert.equal(s.note, "too strong");
});

test("review fixes: quests and AI fields the desk would drop are refused up front", () => {
  assert.throws(() => parseManifest(manifest([edit({ entity: "quest", targetId: "q1" })])), /quest cannot be suggested/);
  assert.throws(() => parseManifest(manifest([edit({ entity: "ai", targetId: "a1", data: { maxHealth: 10 } })])), /does not take maxHealth/);
  assert.throws(() => parseManifest(manifest([edit({ entity: "ai", targetId: "a1", data: { rules: [] } })])), /does not take rules/);
  assert.ok(parseManifest(manifest([edit({ entity: "ai", targetId: "a1", data: { level: 40 } })])).policy.suggest);
});

test("review fixes: an item with no store expiry sends it as the game's form does", async () => {
  const d = setup();
  d.game.seed("item", { id: "i1", name: "Inro", description: "Old.", hidden: false, effects: [], expireFromStoreAt: "" });
  d.game.tables.item.get("i1").expireFromStoreAt = null; // item.get returns the raw null
  d.runner.plan(JSON.stringify(manifest([edit({ entity: "item", name: "Inro", targetId: "i1", data: { description: "New." } })])), { jobId: "i" });
  await d.runner.run("i");
  const sent = d.game.calls.find((c) => c.path === "contentReview.create").input.data;
  assert.equal(sent.expireFromStoreAt, "");
});

test("review fixes: resume never resends a suggestion a reviewer already decided", async () => {
  const d = setup();
  d.game.dropCreateResponse = true;
  d.runner.plan(JSON.stringify(manifest()), { jobId: "r1" });
  await d.runner.run("r1");
  d.game.proposals[0].status = "REJECTED";
  await d.runner.resume("r1");
  assert.equal(d.game.proposals.length, 1);
  assert.equal(d.journal.get("r1").items[0].suggestion.status, "REJECTED");
});

test("review fixes: other people's and agent suggestions do not hide ours; an unsearchable queue is never resent", async () => {
  const d = setup();
  for (let i = 0; i < 400; i++) d.game.proposals.push({ id: `ag${i}`, source: "AGENT", title: "audit", status: "PENDING", targets: [{ entityType: "JUTSU", entityId: "j1" }] });
  d.runner.plan(JSON.stringify(manifest()), { jobId: "r2" });
  await d.runner.run("r2");
  assert.ok(d.journal.get("r2").items[0].suggestion.id, "found past 400 agent rows");

  const e = setup();
  for (let i = 0; i < 3001; i++) e.game.proposals.push({ id: `st${i}`, source: "STAFF", title: "other", status: "PENDING", targets: [{ entityType: "JUTSU", entityId: "x" }] });
  e.game.dropCreateResponse = true;
  e.runner.plan(JSON.stringify(manifest()), { jobId: "r3" });
  await e.runner.run("r3");
  await e.runner.resume("r3");
  assert.equal(e.game.proposals.filter((p) => p.title.startsWith("Ember tune")).length, 1, "not resent");
  assert.equal(e.journal.get("r3").state, "DONE");
});

test("review fixes: a failed queue read after a successful send pauses instead of failing", async () => {
  const d = setup();
  d.game.failQueue = 1;
  d.runner.plan(JSON.stringify(manifest()), { jobId: "r4" });
  await d.runner.run("r4");
  const job = d.journal.get("r4");
  assert.equal(job.state, "PAUSED"); assert.equal(job.items[0].state, "CONFIRMED");
  await d.runner.resume("r4");
  assert.equal(d.game.proposals.length, 1);
  assert.equal(d.journal.get("r4").items[0].suggestion.id, d.game.proposals[0].id);
});
