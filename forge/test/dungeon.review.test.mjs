// Regressions for the independent review of the dungeon recipe (verdict REJECT on aef88c3e,
// findings F1-F6 and N1). Each test reconstructs a reviewer reproduction against the shipped
// wiring (composeForTest) and the in-process FakeGame. Socket-free; the extractor tests read a copy
// of the pinned game source and never run it.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, readFileSync, cpSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dungeonProblems, dungeonDiffs, CONTRACT } from "../src/dungeon/validate.mjs";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";
import { mergeForUpdate } from "../src/runner/recipes.mjs";
import { diffAsserted } from "../src/runner/validate.mjs";
import { SENDLOG_KEY } from "../src/budget/bucket.mjs";
import { TrpcClient } from "../src/transport/client.mjs";
import { CookieSession } from "../src/transport/session.mjs";
import { derive, PIN } from "../tools/derive_dungeon.mjs";
import { checkManifest } from "../tools/check_manifest.mjs";
import { FakeGame } from "./fakegame.mjs";
import { fakeClock } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const floor = (kind, ...aiIds) => ({ kind, waves: [{ aiIds }] });
function content(over = {}) {
  return {
    name: "Skyglass Wreck",
    description: "A downed warship on the tideline.",
    sector: 222, longitude: 12, latitude: 7,
    expiresAt: null, hidden: true, background: "ocean",
    tiers: [
      [floor("floor", "ai-1"), floor("floor", "ai-2"), floor("floor", "ai-3"), floor("floor", "ai-4"), floor("mini-boss", "ai-5")],
      [floor("floor", "ai-6"), floor("floor", "ai-7"), floor("floor", "ai-8"), floor("floor", "ai-9"), floor("boss", "ai-10")],
    ],
    rewards: { money: 5000, experience: 2000, drops: [{ type: "item", id: "chest-1", chance: 100, quantity: 1 }] },
    ...over,
  };
}
const harness = (opts = {}) => composeForTest(opts);
const saves = (game) => game.calls.filter((c) => c.path === "coop.dungeon.save");
const create = (data = content(), policy = {}) => ({ ...policy, items: [{ entity: "dungeon", slot: "create", name: data.name, srcId: "wreck", data }] });
const edit = (data, extra = {}, targetId = "dun-1") => ({ items: [{ entity: "dungeon", slot: "edit", name: "W", targetId, data, ...extra }] });
const edits = (n, label) => ({ items: Array.from({ length: n }, (_, i) => ({ entity: "dungeon", slot: "edit", name: `${label} ${i}`, targetId: `dun-${i}`, data: { name: `${label} ${i}` } })) });
const seedMany = (game, n) => { for (let i = 0; i < n; i++) game.seed("dungeon", { id: `dun-${i}`, content: content({ name: `Dungeon ${i}` }), updatedAt: new Date(0) }); };
/** A clock whose sleeps do not advance it: the reviewer's "fixed clock". */
const frozenClock = () => { const c = fakeClock(); c.tick = () => c(); return c; };

// ------------------------------------------------------------------ F1 budget and 429
test("F1: three sequential 30-edit jobs at a fixed clock send 30 saves, not 90; the budget counts every one", async () => {
  const game = new FakeGame(); seedMany(game, 30);
  const h = harness({ game, clock: frozenClock() });
  const results = [];
  for (const j of ["a", "b", "c"]) { h.runner.plan(edits(30, `Job ${j}`), { jobId: j }); results.push(await h.runner.run(j)); }
  assert.equal(saves(game).length, 30);
  assert.deepEqual(results.map((s) => s.counts.VERIFIED ?? 0), [30, 0, 0]);
  for (const s of results.slice(1)) {
    assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "TOO_MANY_REQUESTS");
    assert.ok(s.pause.until > h.clock(), "the pause carries the time the allowance frees up");
  }
  assert.equal(h.budget.status().paths["coop.dungeon.save"].used, 30);
  assert.ok(h.journal.get("b").items.every((it) => it.state === "PLANNED"), "nothing was marked SENT for a save that never left");
});

test("F1: with a running clock two 30-edit jobs wait rather than overspend; the server's sliding estimate never reaches its limit", async () => {
  const game = new FakeGame(); seedMany(game, 30);
  const h = harness({ game });
  const at = [];
  const handle = game.handle.bind(game);
  game.handle = (path, input) => { if (path === "coop.dungeon.save") at.push(h.clock()); return handle(path, input); };
  for (const j of ["a", "b"]) {
    h.runner.plan(edits(30, `Job ${j}`), { jobId: j });
    const s = await h.runner.run(j);
    assert.equal(s.counts.VERIFIED, 30, JSON.stringify(s.pause));
  }
  assert.equal(at.length, 60);
  for (const t of at) assert.ok(at.filter((u) => u <= t && t - u < 60_000).length <= 30, "at most the allowance in any 60 s");
  // slidingWindow(60, "60 s") as @upstash/ratelimit computes it (src/budget/bucket.mjs header)
  at.forEach((t, i) => {
    const w = 60_000, b = Math.floor(t / w), prior = at.slice(0, i);
    const prev = prior.filter((u) => Math.floor(u / w) === b - 1).length;
    const cur = prior.filter((u) => Math.floor(u / w) === b).length;
    assert.ok(Math.floor((1 - (t % w) / w) * prev) + cur < 60, `save ${i} would trip the server`);
  });
});

test("F1: the persisted send log survives a restart: a new tab cannot spend the same allowance again", async () => {
  const game = new FakeGame(); seedMany(game, 30);
  const clock = frozenClock();
  const h = harness({ game, clock });
  h.runner.plan(edits(30, "Before"), { jobId: "a" });
  assert.equal((await h.runner.run("a")).counts.VERIFIED, 30);
  const h2 = harness({ game, clock, storage: h.storage.crash(), idb: h.idb, tabId: "tab2" });
  h2.runner.plan(edits(1, "After"), { jobId: "b" });
  const s = await h2.runner.run("b");
  assert.equal(s.pause?.reason, "TOO_MANY_REQUESTS", JSON.stringify(s));
  assert.equal(saves(game).length, 30);
});

test("F1: a decoded 429 on coop.dungeon.save fails that item as a definite refusal, persists the trip and sends nothing after it", async () => {
  const game = new FakeGame({ limitPath: "coop.dungeon.save" }); seedMany(game, 3);
  const h = harness({ game });
  h.runner.plan(edits(3, "Limited"), { jobId: "l" });
  const s = await h.runner.run("l");
  assert.equal(saves(game).length, 1, "stopped at the first 429");
  assert.equal(s.state, "PAUSED"); assert.equal(s.pause.reason, "TOO_MANY_REQUESTS"); assert.ok(s.pause.until > h.clock());
  const items = h.journal.get("l").items;
  assert.equal(items[0].state, "FAILED"); assert.match(items[0].error, /TOO_MANY_REQUESTS.*not resent/);
  assert.deepEqual(items.slice(1).map((it) => it.state), ["PLANNED", "PLANNED"]);
  const trip = JSON.parse(h.storage.getItem(SENDLOG_KEY)).__tripped;
  assert.equal(trip.path, "coop.dungeon.save");

  // The same job, a new job and a new tab after a restart all honour the trip until it expires.
  game.limitPath = null;
  assert.equal((await h.runner.run("l")).pause.reason, "TOO_MANY_REQUESTS");
  const h2 = harness({ game, clock: h.clock, storage: h.storage.crash(), idb: h.idb, tabId: "tab2" });
  h2.runner.plan(edits(1, "Other"), { jobId: "o" });
  assert.equal((await h2.runner.run("o")).pause.reason, "TOO_MANY_REQUESTS");
  assert.equal(saves(game).length, 1, "nothing is sent while the trip holds");

  h.clock.set(trip.until);
  h2.runner.attach("l", edits(3, "Limited"));
  const after = await h2.runner.run("l");
  assert.equal(after.counts.VERIFIED, 2, JSON.stringify(after));
  assert.equal(h2.journal.get("l").items[0].state, "FAILED", "the refused save is never resent");
  assert.equal(saves(game).length, 3);
});

test("F1 cross-entity: a 429 on an unlimited mutation (jutsu.update) also stops the job, and spends no budget token", async () => {
  const game = new FakeGame({ limitPath: "jutsu.update" });
  for (const id of ["j1", "j2"]) game.seed("jutsu", { id, name: id });
  const h = harness({ game });
  h.runner.plan({ items: ["j1", "j2"].map((id) => ({ entity: "jutsu", slot: "edit", name: id, targetId: id, data: { description: "new" } })) }, { jobId: "j" });
  const s = await h.runner.run("j");
  assert.equal(game.calls.filter((c) => c.path === "jutsu.update").length, 1);
  assert.equal(s.pause.reason, "TOO_MANY_REQUESTS");
  assert.deepEqual(h.journal.get("j").items.map((it) => it.state), ["FAILED", "PLANNED"]);
  const log = JSON.parse(h.storage.getItem(SENDLOG_KEY));
  assert.equal(log.__tripped.path, "jutsu.update");
  assert.equal(log["jutsu.update"], undefined, "an unlimited path records no send");
});

test("F1: coop.dungeon.save is still sent as a POST mutation, and its 429 decodes as a definite error element", async () => {
  const fx = (n) => JSON.parse(readFileSync(new URL(`./fixtures/envelope/${n}.json`, import.meta.url), "utf8")).exchanges[0].response;
  const queue = [fx("mutation_create_ok"), fx("query_too_many_requests")];
  const calls = [];
  const fetchImpl = async (url, init) => { calls.push({ url, init }); const r = queue.shift(); return new Response(r.body, { status: r.status, headers: { "content-type": "application/json" } }); };
  const c = new TrpcClient(new CookieSession({ fetchImpl }));
  await c.call("coop.dungeon.save", { content: { name: "x" } });
  const r = await c.call("coop.dungeon.save", { content: { name: "x" } });
  assert.deepEqual(calls.map((x) => x.init.method), ["POST", "POST"]);
  assert.match(calls[0].url, /^\/api\/trpc\/coop\.dungeon\.save\?batch=1$/);
  assert.equal(r.ok, false); assert.equal(r.error.code, "TOO_MANY_REQUESTS");
});

// ------------------------------------------------------------------ F2 ambiguous creates
/** dedupNames read (call 1), pre-create snapshot (2), then the save is lost BEFORE it applies (3). */
async function lostCreate(data = content(), h = harness({ game: new FakeGame({ dropAt: 3 }) }), jobId = "lost") {
  h.runner.plan(create(data, { dedupNames: true }), { jobId });
  const s = await h.runner.run(jobId);
  assert.equal(s.pause.reason, "NETWORK", JSON.stringify(s));
  assert.equal(h.game.count("dungeon"), 0, "nothing applied");
  assert.equal(h.journal.get(jobId).items[0].state, "SENT");
  return h;
}
const foreignSave = (game, c) => assert.equal(game.handle("coop.dungeon.save", { content: c }).data.success, true);

test("F2: a foreign row identical to a lost create is a matching candidate, never adopted or verified by itself", async () => {
  const h = await lostCreate();
  foreignSave(h.game, content()); // another operator, same content
  const s = await h.runner.resume("lost");
  const it = h.journal.get("lost").items[0];
  assert.equal(it.state, "ORPHANED", JSON.stringify(s)); assert.equal(s.pause.reason, "ORPHANED");
  assert.deepEqual(it.candidates.map((c) => [c.name, c.matches, c.differs]), [["Skyglass Wreck", true, []]]);
  assert.match(it.error, /no idempotency key/);
  assert.equal(s.counts.VERIFIED, undefined);
  assert.equal(saves(h.game).length, 2, "the lost save and the foreign one; nothing resent");
});

test("F2: a foreign row that differs only where the plan relied on a default (quantity 100 vs the stored 1) does not match", async () => {
  const planned = content({ rewards: { money: 5000, experience: 2000, drops: [{ type: "item", id: "chest-1", chance: 100 }] } });
  const h = await lostCreate(planned);
  foreignSave(h.game, content({ rewards: { money: 5000, experience: 2000, drops: [{ type: "item", id: "chest-1", chance: 100, quantity: 100 }] } }));
  await h.runner.resume("lost");
  const it = h.journal.get("lost").items[0];
  assert.equal(it.state, "ORPHANED");
  assert.equal(it.candidates[0].matches, false); assert.deepEqual(it.candidates[0].differs, ["rewards"]);
  // the operator may still bind it; it is read back, shows the drift, and is never saved again
  h.runner.adopt("lost", 0, it.candidates[0].id);
  const s = await h.runner.run("lost");
  assert.equal(s.verify.drift, 1, JSON.stringify(s));
  assert.equal(saves(h.game).length, 2);
});

test("F2: several candidates are all listed with their evidence; binding one reads it back and sends nothing", async () => {
  const h = await lostCreate();
  foreignSave(h.game, content({ name: "Another Wreck" }));
  foreignSave(h.game, content());
  await h.runner.resume("lost");
  const it = h.journal.get("lost").items[0];
  assert.equal(it.state, "ORPHANED");
  assert.deepEqual(it.candidates.map((c) => [c.name, c.matches]), [["Another Wreck", false], ["Skyglass Wreck", true]]);
  h.runner.adopt("lost", 0, it.candidates[1].id);
  const s = await h.runner.run("lost");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.equal(saves(h.game).length, 3, "no create retry and no second save after binding");
});

test("F2: rows another job owns are never candidates", async () => {
  const h = await lostCreate();
  h.runner.plan(create(content({ name: "Owned Wreck" })), { jobId: "owner" });
  assert.equal((await h.runner.run("owner")).counts.VERIFIED, 1);
  await h.runner.resume("lost");
  const it = h.journal.get("lost").items[0];
  assert.equal(it.state, "ORPHANED");
  assert.deepEqual(it.candidates, [], "the journal-owned row is excluded");
});

// ------------------------------------------------------------------ F3 unknown live keys
test("F3: an unknown live key at any level is schema drift: the edit is refused and the row is untouched", async () => {
  const cases = {
    "top-level": (c) => { c.minLevel = 40; },
    "floor": (c) => { c.tiers[0][0].trap = true; },
    "wave": (c) => { c.tiers[1][4].waves[0].reinforce = 2; },
    "rewards": (c) => { c.rewards.ryo = 5; },
    "drop": (c) => { c.rewards.drops[0].bonus = 1; },
    "row-metadata name inside content": (c) => { c.id = "dun-1"; },
  };
  for (const [label, mutate] of Object.entries(cases)) {
    const game = new FakeGame();
    const c = content(); mutate(c);
    game.seed("dungeon", { id: "dun-1", content: structuredClone(c), updatedAt: new Date(0) });
    const h = harness({ game });
    h.runner.plan(edit({ name: "Renamed" }), { jobId: "d" });
    const s = await h.runner.run("d");
    assert.equal(s.counts.FAILED, 1, label);
    assert.match(h.journal.get("d").items[0].error, /schema drift/, label);
    assert.equal(saves(game).length, 0, label);
    assert.deepEqual(game.rows("dungeon")[0].content, c, `${label}: untouched`);
  }
});

test("F3: a malformed known live field is still refused before any save", async () => {
  const game = new FakeGame();
  game.seed("dungeon", { id: "dun-1", content: content({ sector: -5 }), updatedAt: new Date(0) });
  const h = harness({ game });
  h.runner.plan(edit({ name: "Renamed" }), { jobId: "m" });
  assert.equal((await h.runner.run("m")).counts.FAILED, 1);
  assert.match(h.journal.get("m").items[0].error, /sector/);
  assert.equal(saves(game).length, 0);
});

test("F3: an edit re-sends the live content whole, without the row's id or timestamp", () => {
  const live = { id: "d1", content: content({ structureAssetId: "asset-1", structureScale: 2 }), updatedAt: new Date(1) };
  const sent = mergeForUpdate("dungeon", live, { name: "Renamed" }, new Set(CONTRACT.contentFields));
  assert.deepEqual(sent, { ...live.content, name: "Renamed" });
  assert.deepEqual(dungeonProblems({ name: "Renamed" }, live), []);
  assert.match(dungeonProblems({ name: "Renamed" }, { id: "d1", updatedAt: new Date(1) }).join(), /no content object/);
});

// ------------------------------------------------------------------ F4 package snapshots
const PACKAGE = { name: "Wreck Haul", description: "Salvage", rewards: { reward_money: 100, reward_items: [] } };
const packageGame = () => { const game = new FakeGame(); game.packages = new Map([["pk-1", structuredClone(PACKAGE)]]); return game; };
const withPackage = (snapshot) => content({ rewards: { money: 0, experience: 0, tokens: 0, prestige: 0, drops: [{ type: "package", id: "pk-1", chance: 50, quantity: 1, ...(snapshot ? { package: snapshot } : {}) }] } });

test("F4: a create with a package drop gets the catalog snapshot from the server and verifies", async () => {
  const game = packageGame();
  const h = harness({ game });
  h.runner.plan(create(withPackage()), { jobId: "p" });
  const s = await h.runner.run("p");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.deepEqual(game.rows("dungeon")[0].content.rewards.drops[0].package, PACKAGE);
});

test("F4: a name-only edit of a package-bearing dungeon is refused with the refresh explanation, not 'omit it'", async () => {
  const game = packageGame();
  game.seed("dungeon", { id: "dun-1", content: withPackage(PACKAGE), updatedAt: new Date(0) });
  const h = harness({ game });
  h.runner.plan(edit({ name: "Renamed" }), { jobId: "e" });
  assert.equal((await h.runner.run("e")).counts.FAILED, 1);
  const error = h.journal.get("e").items[0].error;
  assert.match(error, /re-copies every package snapshot/); assert.match(error, /refreshPackages/);
  assert.doesNotMatch(error, /omit it/);
  assert.equal(saves(game).length, 0);
});

test("F4: with refreshPackages the edit saves once, sends no snapshot, and the read-back carries the catalog's CURRENT contents", async () => {
  const game = packageGame();
  game.seed("dungeon", { id: "dun-1", content: withPackage(PACKAGE), updatedAt: new Date(0) });
  game.packages.get("pk-1").rewards.reward_money = 999; // the catalog moved since the dungeon was saved
  const h = harness({ game });
  h.runner.plan(edit({ name: "Renamed" }, { refreshPackages: true }), { jobId: "r" });
  const s = await h.runner.run("r");
  assert.equal(s.counts.VERIFIED, 1, JSON.stringify(s));
  assert.equal(saves(game).length, 1);
  assert.ok(!("package" in saves(game)[0].input.content.rewards.drops[0]), "the inherited snapshot is not sent");
  assert.equal(game.rows("dungeon")[0].content.rewards.drops[0].package.rewards.reward_money, 999);
  assert.deepEqual(h.journal.get("r").items[0].packagesRefreshed, ["pk-1"]);
});

test("F4: a manifest-authored package payload is still refused, on create and on edit", () => {
  const live = { id: "d1", content: content(), updatedAt: new Date(0) };
  assert.match(dungeonProblems(withPackage({ name: "forged" }), null, { preCreate: true }).join(), /omit it/);
  assert.match(dungeonProblems({ rewards: withPackage({ name: "forged" }).rewards }, live, { refreshPackages: true }).join(), /omit it/);
});

test("F4: refreshPackages is accepted only as true on a dungeon edit", () => {
  assert.equal(parseManifest(edit({ name: "x" }, { refreshPackages: true })).items[0].refreshPackages, true);
  for (const m of [edit({ name: "x" }, { refreshPackages: false }), { items: [{ ...create().items[0], refreshPackages: true }] },
    { items: [{ entity: "jutsu", slot: "edit", name: "j", targetId: "j1", data: { description: "d" }, refreshPackages: true }] }]) {
    assert.throws(() => parseManifest(m), (e) => e instanceof ManifestError && /refreshPackages/.test(e.message));
  }
});

// ------------------------------------------------------------------ F5 normalization
test("F5: expiry instants compare across string and Date forms; null is never the epoch", () => {
  const same = (sent, live) => dungeonDiffs({ expiresAt: sent }, { expiresAt: live }).length === 0;
  assert.ok(same("2027-01-01", "2027-01-01T00:00:00.000Z"), "date-only");
  assert.ok(same("2027-01-01T01:00:00+01:00", "2027-01-01T00:00:00.000Z"), "offset");
  assert.ok(same("2027-01-01T00:00:00.000Z", "2027-01-01T00:00:00.000Z"), "canonical");
  assert.ok(same(new Date("2027-01-01T00:00:00Z"), "2027-01-01T00:00:00.000Z"), "Date vs JSON string");
  assert.ok(same("1970-01-01", "1970-01-01T00:00:00.000Z"), "epoch is an instant like any other");
  assert.ok(same(null, null));
  assert.ok(!same(null, "1970-01-01T00:00:00.000Z") && !same(null, new Date(0)) && !same("1970-01-01T00:00:00.000Z", null), "null is not the epoch");
  assert.ok(!same("2027-01-02", "2027-01-01T00:00:00.000Z"));
});

test("F5: invalid and zone-less dates are refused before send; a valid Date object is accepted", () => {
  for (const expiresAt of [new Date("nope"), "2027-01-01T00:00", "2027-13-01", "Jan 1 2027", 0, ""]) {
    assert.match(dungeonProblems(content({ expiresAt }), null, { preCreate: true }).join(), /expiresAt/, String(expiresAt));
  }
  assert.deepEqual(dungeonProblems(content({ expiresAt: new Date("2027-01-01T00:00:00Z") }), null, { preCreate: true }), []);
});

test("F5: a name with surrounding whitespace is refused (the server trims); the read-back compares trimmed", () => {
  assert.match(dungeonProblems(content({ name: " Skyglass Wreck " }), null, { preCreate: true }).join(), /whitespace/);
  assert.deepEqual(dungeonDiffs({ name: "Skyglass Wreck" }, { name: "Skyglass Wreck" }), []);
});

test("F5: an omitted default equals the stored default; a stored non-default is drift", () => {
  const drops = (extra) => [{ type: "item", id: "x", chance: 5, ...extra }];
  const stored = (q) => ({ rewards: { money: 0, experience: 0, tokens: 0, prestige: 0, drops: drops({ quantity: q }) } });
  assert.deepEqual(dungeonDiffs({ rewards: { drops: drops() } }, stored(1)), []);
  assert.deepEqual(dungeonDiffs({ rewards: { drops: drops() } }, stored(100)).map((d) => d.key), ["rewards"]);
  const c = content();
  const live = structuredClone(c); live.tiers[0][0].waves[0].delayRounds = 0; live.structureScale = 1; live.structureAssetId = "";
  assert.deepEqual(dungeonDiffs(c, live), []);
});

test("F5 end-to-end: offset, date-only and null expiries verify against the JSON the fake stores", async () => {
  for (const expiresAt of ["2027-01-01T01:00:00+01:00", "2027-01-01", null]) {
    const game = new FakeGame();
    const h = harness({ game });
    h.runner.plan(create(content({ expiresAt })), { jobId: "x" });
    const s = await h.runner.run("x");
    assert.equal(s.counts.VERIFIED, 1, `${expiresAt}: ${JSON.stringify(s.items[0].diffs)}`);
    assert.equal(game.rows("dungeon")[0].content.expiresAt, expiresAt === null ? null : "2027-01-01T00:00:00.000Z");
  }
});

test("F5 cross-entity: the other entities keep their comparison semantics", () => {
  assert.deepEqual(diffAsserted("item", { image: "" }, { image: null }), [], "'' and null");
  assert.deepEqual(diffAsserted("ai", { level: 10 }, { level: 10.4 }), [], "ai numeric tolerance");
  assert.deepEqual(diffAsserted("quest", { expiresAt: "2027-01-01T00:00:00.000Z" }, { expiresAt: new Date("2027-01-01T00:00:00Z") }), []);
  assert.equal(diffAsserted("jutsu", { name: "a" }, { name: "b" }).length, 1);
  assert.deepEqual(diffAsserted("jutsu", { effects: [{ type: "damage" }] }, { effects: [{ type: "damage", power: 1 }] }), [], "live-only nested keys stay one-sided");
});

// ------------------------------------------------------------------ F6 explicit null
const nulled = {
  delayRounds: () => { const c = content(); c.tiers[0][1].waves[0].delayRounds = null; return c; },
  quantity: () => { const c = content(); c.rewards.drops[0].quantity = null; return c; },
  drops: () => { const c = content(); c.rewards.drops = null; return c; },
};

test("F6: explicit null is not omission for delayRounds, quantity and drops", () => {
  for (const [k, make] of Object.entries(nulled)) assert.match(dungeonProblems(make(), null, { preCreate: true }).join(), /null is not accepted/, k);
  const omitted = content(); delete omitted.rewards.drops; delete omitted.rewards.money;
  assert.deepEqual(dungeonProblems(omitted, null, { preCreate: true }), [], "omitted still means the default");
});

test("F6: the fake game refuses the same nulls as a BAD_REQUEST, as zod's prefault does", () => {
  const game = new FakeGame();
  for (const [k, make] of Object.entries(nulled)) {
    const r = game.handle("coop.dungeon.save", { content: make() });
    assert.equal(r.ok, false, k); assert.equal(r.error.code, "BAD_REQUEST", k);
  }
  assert.equal(game.count("dungeon"), 0);
});

test("F6 bridge: check_manifest.mjs and validate.py refuse a null quantity; validate.py refuses refreshPackages on a create", () => {
  const dir = mkdtempSync(join(tmpdir(), "dungeon-review-"));
  const bad = join(dir, "null.json"), ack = join(dir, "ack.json");
  writeFileSync(bad, JSON.stringify(create(nulled.quantity())));
  writeFileSync(ack, JSON.stringify({ items: [{ ...create().items[0], refreshPackages: true }] }));
  assert.ok(checkManifest(bad).problems.some((p) => /quantity.*null is not accepted/.test(p)));
  const data = fileURLToPath(new URL("../../skills/building-tnr-content/data/", import.meta.url));
  const py = (f) => { try { execFileSync("python3", ["../scripts/validate.py", "--strict", f], { cwd: data, encoding: "utf8" }); return { code: 0, out: "" }; } catch (e) { return { code: e.status, out: String(e.stdout) + String(e.stderr) }; } };
  const b = py(bad);
  assert.notEqual(b.code, 0); assert.match(b.out, /null is not accepted/);
  const a = py(ack);
  assert.notEqual(a.code, 0); assert.match(a.out, /refreshPackages/);
});

// ------------------------------------------------------------------ N1 extractor
const GAME = process.env.TNR_GAME_CHECKOUT;
const SKIP = !GAME && "set TNR_GAME_CHECKOUT to a checkout at the pin";
const SOURCES = Object.keys(CONTRACT._meta.sources);
function sourceCopy() {
  const dir = mkdtempSync(join(tmpdir(), "dungeon-src-"));
  for (const p of SOURCES) cpSync(join(GAME, p), join(dir, p));
  return dir;
}

const ROOT_TS = "app/src/server/api/root.ts", COOP_TS = "app/src/server/api/routers/coop.ts";
/** A copy of the pinned sources with one exact, present-at-the-pin replacement in `file`. */
function mutated(file, from, to) {
  const dir = sourceCopy(), p = join(dir, file), s = readFileSync(p, "utf8");
  assert.equal(s.split(from).length, 2, `${JSON.stringify(from)} occurs exactly once in ${file} at the pin`);
  writeFileSync(p, s.replace(from, to));
  return dir;
}

test("N1: an unmodified copy of the pinned sources derives exactly the committed contract", { skip: SKIP }, () => {
  assert.equal(JSON.stringify(derive(sourceCopy()), null, 2) + "\n", readFileSync(new URL("../src/dungeon/contract.json", import.meta.url), "utf8"));
});

test("N1: the extractor refuses rebound bounds, spreads, computed keys and an unrecognised procedure kind", { skip: SKIP }, () => {
  const [validator, router] = SOURCES;
  const cases = [
    ["max waves rebound to a literal", validator, ".max(DUNGEON_MAX_WAVES)", ".max(1)", /dungeonFloorSchema\.waves: unrecognised/],
    ["floors per tier rebound", validator, ".length(DUNGEON_FLOORS_PER_TIER)", ".length(6)", /dungeonContentSchema\.tiers: unrecognised/],
    ["drop quantity max rebound", validator, ".max(DUNGEON_MAX_REWARD_QUANTITY)", ".max(7)", /dungeonDropSchema\.quantity: unrecognised/],
    ["content-object spread", validator, "    hidden: z.boolean().prefault(true),", "    hidden: z.boolean().prefault(true),\n    ...extraFields,", /unsupported member "\.\.\.extraFields,"/],
    ["computed key", validator, "    expiresAt: z.coerce.date().nullable(),", "    [\"expiresAt\"]: z.coerce.date().nullable(),", /unsupported member/],
    ["new field", validator, "    hidden: z.boolean().prefault(true),", "    hidden: z.boolean().prefault(true),\n    minLevel: z.number(),", /fields .* differ from the understood/],
    ["getAll as a subscription", router, "  getAll: protectedProcedure.query(", "  getAll: protectedProcedure.subscription(", /dungeon\.getAll: expected exactly one \.query\( or \.mutation\(/],
    ["save without its limiter", router, "  save: protectedProcedure\n    .use(ratelimitMiddleware)\n", "  save: protectedProcedure\n", /save input binding/],
  ];
  for (const [label, file, from, to, expected] of cases) {
    const dir = sourceCopy(), p = join(dir, file), s = readFileSync(p, "utf8");
    assert.ok(s.includes(from), `${label}: pattern present at the pin`);
    writeFileSync(p, s.replace(from, to));
    assert.throws(() => derive(dir), expected, label);
  }
});

test("procedure paths follow the router mount chain (coop.dungeon.*), derived from both router objects", { skip: SKIP }, () => {
  // Forge 0.9.0 called "dungeon.getAll"; the server answered NOT_FOUND because root.ts mounts
  // coopRouter at `coop` and coop.ts mounts dungeonRouter at `dungeon` (2026-10-25, push/263).
  assert.deepEqual(Object.keys(CONTRACT.procedures), ["coop.dungeon.getAll", "coop.dungeon.save"]);
  assert.ok(SOURCES.includes(ROOT_TS) && SOURCES.includes(COOP_TS), "both mount files are pinned sources");
  // The path is derived, not asserted: a renamed link changes the derived path (and so fails
  // derive_dungeon.mjs --check against the committed contract) instead of being matched by text.
  for (const [file, from, to, path] of [
    [ROOT_TS, "  coop: coopRouter,", "  party: coopRouter,", "party.dungeon"],
    [COOP_TS, "  dungeon: dungeonRouter,", "  dungeons: dungeonRouter,", "coop.dungeons"],
  ]) {
    const dir = mutated(file, from, to);
    assert.deepEqual(Object.keys(derive(dir).procedures), [`${path}.getAll`, `${path}.save`], to);
  }
});

test("review C1: the mount extractor refuses additional, duplicate, spread, computed and other unsupported bindings", { skip: SKIP }, () => {
  const R = "  coop: coopRouter,", C = "  dungeon: dungeonRouter,";
  const cases = [
    ["additional root alias", ROOT_TS, R, `${R}\n  party: coopRouter,`, /root\.ts: coopRouter is mounted twice \(coop, party\)/],
    ["additional coop alias", COOP_TS, C, `${C}\n  dungeons: dungeonRouter,`, /coop\.ts: dungeonRouter is mounted twice \(dungeon, dungeons\)/],
    ["identical duplicate root line", ROOT_TS, R, `${R}\n${R}`, /root\.ts: duplicate key coop/],
    ["duplicate root key, other router", ROOT_TS, R, `${R}\n  coop: questsRouter,`, /root\.ts: duplicate key coop/],
    ["identical duplicate coop line", COOP_TS, C, `${C}\n${C}`, /coop\.ts: duplicate key dungeon/],
    ["root spread after the mount", ROOT_TS, R, `${R}\n  ...overrides,`, /root\.ts: unsupported router member "\.\.\.overrides,"/],
    ["coop spread after the mount", COOP_TS, C, `${C}\n  ...{ dungeon: otherRouter },`, /coop\.ts: unsupported router member/],
    ["root computed member", ROOT_TS, R, '  ["coop"]: coopRouter,', /root\.ts: unsupported router member/],
    ["coop computed member", COOP_TS, C, "  [DUNGEON]: dungeonRouter,", /coop\.ts: unsupported router member/],
    ["quoted key", COOP_TS, C, '  "dungeon": dungeonRouter,', /coop\.ts: unsupported router member/],
    ["shorthand member", COOP_TS, C, "  dungeonRouter,", /coop\.ts: unsupported router member/],
    ["trailing comment", ROOT_TS, R, `${R} // co-op`, /root\.ts: unsupported router member/],
    ["inline router", ROOT_TS, R, "  coop: createTRPCRouter({ dungeon: dungeonRouter }),", /root\.ts: expected exactly one createTRPCRouter\( call, found 2/],
    ["second router in coop.ts", COOP_TS, "export const coopRouter", "export const otherRouter = createTRPCRouter({});\nexport const coopRouter", /coop\.ts: expected exactly one createTRPCRouter\( call, found 2/],
    ["mergeRouters", ROOT_TS, "export const appRouter", "const merged = mergeRouters();\nexport const appRouter", /root\.ts: mergeRouters/],
    ["binding with no import", ROOT_TS, R, "  coop: localCoopRouter,", /root\.ts: coop: localCoopRouter is not a named import/],
    ["aliased import", ROOT_TS, 'import { coopRouter } from "./routers/coop";', 'import { coopRouter as party } from "./routers/coop";', /root\.ts: coop: coopRouter is not a named import/],
    ["coop router renamed in its import", ROOT_TS, "  coop: coopRouter,", "  coop: partyRouter,", /root\.ts: coop: partyRouter is not a named import/],
    ["coop mount removed", ROOT_TS, `${R}\n`, "", /root\.ts: expected exactly one mount of app\/src\/server\/api\/routers\/coop, found 0/],
    ["dungeon router imported from elsewhere", COOP_TS, 'from "@/server/api/routers/dungeon"', 'from "@/server/api/routers/dungeonV2"', /coop\.ts: expected exactly one mount of app\/src\/server\/api\/routers\/dungeon, found 0/],
    ["dungeon also mounted at the root", ROOT_TS, R, `${R}\n  dungeon: dungeonRouter,`, /root\.ts: (dungeon: dungeonRouter is not a named import|dungeonRouter is referenced in root\.ts)/],
    ["dungeonRouter imported at the root", ROOT_TS, 'import { coopRouter } from "./routers/coop";', 'import { coopRouter } from "./routers/coop";\nimport { dungeonRouter } from "./routers/dungeon";', /dungeonRouter is referenced in root\.ts/],
    ["dungeon.ts exports a different router", "app/src/server/api/routers/dungeon.ts", "export const dungeonRouter = createTRPCRouter({", "export const dungeonRouterV2 = createTRPCRouter({", /dungeon\.ts: expected exactly one export const dungeonRouter/],
  ];
  for (const [label, file, from, to, expected] of cases) assert.throws(() => derive(mutated(file, from, to)), expected, label);
});

test("N1: the CLI keeps its exact-pin and dirty-file guards", { skip: SKIP }, () => {
  const tool = fileURLToPath(new URL("../tools/derive_dungeon.mjs", import.meta.url));
  const dir = mkdtempSync(join(tmpdir(), "dungeon-pin-"));
  const git = (...a) => execFileSync("git", ["-C", dir, "-c", "user.name=t", "-c", "user.email=t@t", ...a], { stdio: "pipe" });
  execFileSync("git", ["clone", "--quiet", "--shared", "--no-checkout", GAME, dir], { stdio: "pipe" });
  git("sparse-checkout", "set", "--no-cone", ...SOURCES.map((p) => "/" + p));
  git("checkout", "--quiet", PIN);
  const cli = () => { try { execFileSync(process.execPath, [tool, dir, "--check"], { stdio: "pipe", encoding: "utf8" }); return ""; } catch (e) { return String(e.stderr); } };
  assert.equal(cli(), "", "a clean checkout at the pin is current");
  writeFileSync(join(dir, SOURCES[0]), readFileSync(join(dir, SOURCES[0]), "utf8") + "\n// edited\n");
  assert.match(cli(), /dirty source file/);
  git("checkout", "--quiet", "--", SOURCES[0]);
  git("commit", "--quiet", "--allow-empty", "-m", "not the pin");
  assert.match(cli(), /expected audited/);
});
