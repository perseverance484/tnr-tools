// livePatch (livepatch.mjs): an edit whose effects are derived from the live record at send time.
// Built for job 593, the Mother of Echoes 2.5x pass, where the manifest cannot carry ~800 KB of
// effects through the connector relay.
import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";
import { parseManifest, planOrder, toJournalSpecs } from "../src/runner/manifest.mjs";
import { applyLivePatch, livePatchDiffs } from "../src/runner/livepatch.mjs";

const harness = () => composeForTest({ game: new FakeGame(), storage: new MemoryStorage(), idb: new IDBFactory(), tabId: "tab" });
const fx = (anim = {}, extra = {}) => ({
  type: "damage", description: "d", power: 10, powerPerLevel: 0, calculation: "static", direction: "offence", target: "INHERIT",
  staticAssetPath: "", staticAnimation: "", appearAnimation: "", disappearAnimation: "", appearSfx: "", disappearSfx: "", rounds: 0,
  ...anim, ...extra,
});
const jutsu = (id, effects, extra = {}) => ({ id, name: "Hold Still", description: "keep me", hidden: false, range: 4, cooldown: 3, effects, ...extra });
const patch = (extra = {}) => ({ animationScale: 2.5, assets: ["moe-a", "moe-b"], ...extra });
const edit = (id, livePatch, data = {}) => ({ items: [{ entity: "jutsu", slot: "edit", name: "Hold Still", targetId: id, data, livePatch }] });

test("livePatch: parse refuses a bad patch before a job opens", () => {
  assert.ok(parseManifest(edit("j", patch())).items[0].livePatch);
  const bad = [
    [patch({ animationScale: 4 }), /from 1 to 3/],
    [patch({ animationScale: "2.5" }), /from 1 to 3/],
    [patch({ assets: [] }), /at least one asset/],
    [patch({ size: 2 }), /does not know size/],
  ];
  for (const [p, re] of bad) assert.throws(() => parseManifest(edit("j", p)), re);
  assert.throws(() => parseManifest(edit("j", patch(), { effects: [] })), /do not also send data.effects/);
  assert.throws(() => parseManifest({ items: [{ entity: "quest", slot: "edit", name: "Q", targetId: "q", data: {}, livePatch: patch() }] }), /not quest/);
  assert.throws(() => parseManifest({ items: [{ entity: "jutsu", slot: "create", srcId: "s", name: "N", data: {}, livePatch: patch() }] }), /only for an edit/);
});

test("livePatch: is part of the item's identity hash; a manifest without one hashes as before", () => {
  const plain = toJournalSpecs(planOrder(parseManifest({ items: [{ entity: "jutsu", slot: "edit", name: "Hold Still", targetId: "j", data: {} }] })))[0].payloadHash;
  const a = toJournalSpecs(planOrder(parseManifest(edit("j", patch()))))[0].payloadHash;
  const b = toJournalSpecs(planOrder(parseManifest(edit("j", patch({ animationScale: 2 })))))[0].payloadHash;
  assert.notEqual(a, plain); assert.notEqual(a, b);
});

test("applyLivePatch: scales only effects that use a listed asset; counts mixed effects", () => {
  const live = { effects: [fx({ appearAnimation: "moe-a" }), fx({ staticAnimation: "stock" }), fx({ staticAnimation: "moe-b", disappearAnimation: "stock" }), fx()] };
  const r = applyLivePatch(patch(), live);
  assert.deepEqual(r.data.effects.map((e) => e.animationScale), [2.5, undefined, 2.5, undefined]);
  assert.deepEqual([r.targeted, r.changed, r.mixed], [2, 2, 1]);
  assert.equal(live.effects[0].animationScale, undefined, "the live row is not mutated");
  assert.equal(r.data.effects[1], live.effects[1], "untargeted effects pass through as live holds them");
  assert.equal(applyLivePatch(patch(), { effects: r.data.effects }).changed, 0);
  assert.deepEqual(livePatchDiffs(patch(), { effects: r.data.effects }), []);
  assert.equal(livePatchDiffs(patch(), live)[0].key, "effects.animationScale");
  assert.throws(() => applyLivePatch(patch(), { name: "x" }), /no effects array/);
  // targets gone is never a match (review P2-1)
  assert.equal(livePatchDiffs(patch(), { name: "x" }).length, 1);
  assert.equal(livePatchDiffs(patch(), { effects: [] }).length, 1);
  assert.equal(livePatchDiffs(patch(), { effects: [fx({ staticAnimation: "stock" })] }).length, 1);
});

test("livePatch: the runner sends the whole live record with the scale set, then verifies it", async () => {
  const h = harness();
  h.game.seed("jutsu", jutsu("j-1", [fx({ appearAnimation: "moe-a" }, { power: 77 }), fx({ staticAnimation: "stock" })]));
  h.runner.plan(edit("j-1", patch()), { jobId: "lp1" });
  const s = await h.runner.run("lp1");
  assert.equal(s.items[0].state, "VERIFIED", JSON.stringify(s.items[0]));
  const row = h.game.rows("jutsu")[0];
  assert.deepEqual(row.effects.map((e) => e.animationScale), [2.5, undefined]);
  assert.equal(row.effects[0].power, 77); assert.equal(row.description, "keep me"); assert.equal(row.range, 4);
  const sent = h.game.calls.filter((c) => c.path === "jutsu.update");
  assert.equal(sent.length, 1);
  assert.equal(sent[0].input.data.effects.length, 2, "the full effect list went out, built from live");
  assert.deepEqual(h.journal.get("lp1").items[0].livePatched, { targeted: 1, changed: 1, mixed: 0 });
});

test("livePatch: a record that already holds the scale gets an idempotent write and verifies", async () => {
  const h = harness();
  h.game.seed("jutsu", jutsu("j-2", [fx({ appearAnimation: "moe-a" }, { animationScale: 2.5 })]));
  h.runner.plan(edit("j-2", patch()), { jobId: "lp2" });
  const s = await h.runner.run("lp2");
  assert.equal(s.items[0].state, "VERIFIED");
  assert.equal(h.game.calls.filter((c) => c.path === "jutsu.update").length, 1);
  assert.deepEqual(h.journal.get("lp2").items[0].livePatched, { targeted: 1, changed: 0, mixed: 0 });
});

test("livePatch: other asserted keys still go out alongside the patch", async () => {
  const h = harness();
  h.game.seed("jutsu", jutsu("j-4", [fx({ appearAnimation: "moe-a" }, { animationScale: 2.5 })]));
  h.runner.plan(edit("j-4", patch(), { hidden: true }), { jobId: "lp4" });
  const s = await h.runner.run("lp4");
  assert.equal(s.items[0].state, "VERIFIED");
  assert.equal(h.game.rows("jutsu")[0].hidden, true);
  assert.equal(h.game.calls.filter((c) => c.path === "jutsu.update").length, 1);
});

test("livePatch: no effect using a listed asset FAILS the item without a send", async () => {
  const h = harness();
  h.game.seed("jutsu", jutsu("j-3", [fx({ staticAnimation: "stock" })]));
  h.runner.plan(edit("j-3", patch()), { jobId: "lp3" });
  const s = await h.runner.run("lp3");
  assert.equal(s.items[0].state, "FAILED"); assert.match(s.items[0].error, /no effect on the live record uses a listed asset/);
  assert.equal(h.game.calls.filter((c) => c.path === "jutsu.update").length, 0);
});

test("livePatch: reconciling a lost send confirms only when live holds the patch", async () => {
  const h = harness();
  h.game.seed("jutsu", jutsu("j-5", [fx({ appearAnimation: "moe-a" })]));
  const planned = { ...parseManifest(edit("j-5", patch())).items[0], deps: [] };
  const job = { jobId: "r", items: [] };
  const item = { idx: 0, entity: "jutsu", op: "update", state: "SENT", phase: "update", entityId: "j-5", targetId: "j-5" };
  const rec = h.reconciler;
  const before = await rec.resolveSent(job, item, { planned, lookup: () => undefined });
  assert.equal(before.action, "orphan"); assert.match(before.note, /effects.animationScale/);
  h.game.rows("jutsu")[0].effects[0].animationScale = 2.5;
  const after = await rec.resolveSent(job, item, { planned, lookup: () => undefined });
  assert.equal(after.action, "confirm"); assert.equal(after.landed, true);
});

test("livePatch: verify and reconcile report drift when the targets are gone (review P2-1)", async () => {
  const h = harness();
  h.game.seed("jutsu", jutsu("j-6", [fx({ appearAnimation: "moe-a" })]));
  const planned = { ...parseManifest(edit("j-6", patch())).items[0], deps: [] };
  const item = { idx: 0, entity: "jutsu", op: "update", state: "SENT", phase: "update", entityId: "j-6", targetId: "j-6" };
  for (const effects of [[], [fx({ staticAnimation: "stock" })]]) {
    h.game.rows("jutsu")[0].effects = effects;
    const r = await h.reconciler.resolveSent({ jobId: "r", items: [] }, item, { planned, lookup: () => undefined });
    assert.equal(r.action, "orphan");
  }
});

test("livePatch: suggest mode refuses it at parse (review P2-2)", () => {
  const m = { mode: "suggest", suggestion: { title: "Clip size pass", rationale: "Scale her clips to the size they were drawn for." }, ...edit("j", patch()) };
  assert.throws(() => parseManifest(m), /livePatch cannot be suggested/);
});

test("livePatch: ordinary verify after the targets were removed is drift, not a match (review P2-1)", async () => {
  const h = harness();
  h.game.seed("jutsu", jutsu("j-7", [fx({ appearAnimation: "moe-a" })]));
  const handle = h.game.handle.bind(h.game);
  // the update lands, then someone strips the clip before the read-back
  h.game.handle = (path, input) => {
    const out = handle(path, input);
    if (path === "jutsu.update") h.game.rows("jutsu")[0].effects = [fx({ staticAnimation: "stock" })];
    return out;
  };
  h.runner.plan(edit("j-7", patch()), { jobId: "lp7" });
  const s = await h.runner.run("lp7");
  assert.notEqual(s.items[0].state, "VERIFIED");
  assert.equal(h.journal.get("lp7").items[0].verify, "drift");
});
