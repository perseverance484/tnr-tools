// The runner progress emitter is ADVISORY. This suite exists to prove that word, by running the
// same job three ways and comparing the evidence rather than the intent:
//
//   A  no subscriber at all        (the behaviour that shipped before this hook existed)
//   B  a passive recording subscriber
//   C  a subscriber that throws on every single event
//
// Journal bytes, request order and the returned summary must be identical across all three.
import { test } from "node:test";
import assert from "node:assert/strict";
import { IDBFactory } from "fake-indexeddb";
import { composeForTest } from "./compose.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { FakeGame } from "./fakegame.mjs";

const MANIFEST = JSON.stringify({
  items: [
    { entity: "jutsu", slot: "create", name: "Ev A", srcId: "ev-a", data: { name: "Ev A", hidden: true } },
    { entity: "jutsu", slot: "create", name: "Ev B", srcId: "ev-b", data: { name: "Ev B", hidden: true } },
  ],
});

async function runOnce(subscribe) {
  const storage = new MemoryStorage();
  const game = new FakeGame();
  const d = composeForTest({ game, storage, idb: new IDBFactory(), clock: fakeClock() });
  const sends = [];
  const inner = d.client.mutation ? d.client.mutation.bind(d.client) : null;
  if (inner) d.client.mutation = async (path, input) => { sends.push(path); return inner(path, input); };
  const innerQ = d.client.query ? d.client.query.bind(d.client) : null;
  if (innerQ) d.client.query = async (path, input) => { sends.push(path); return innerQ(path, input); };

  let off = null;
  if (subscribe) off = subscribe(d.runner);
  d.runner.plan(MANIFEST, { jobId: "ev-job", manifestPath: "push/ev.json", manifestNumber: 1 });
  const summary = await d.runner.run("ev-job");
  if (off) off();
  return {
    summary: normalizeIds(JSON.stringify(summary)),
    sends,
    journal: normalizeIds(JSON.stringify(d.journal.get("ev-job"))),
    storage: normalizeIds(JSON.stringify(storage.snapshot())),
  };
}

// FakeGame's entity-id counter is module-global, so three sequential runs mint different ids for
// the same work. That is a property of the harness, not of the subscriber, and it is the ONLY axis
// normalised here: each distinct generated id becomes a token by order of first appearance, so two
// runs that allocated ids in the same order compare equal and one that did not still fails.
function normalizeIds(text) {
  const seen = new Map();
  return text.replace(/fk\d{15,}/g, (id) => {
    if (!seen.has(id)) seen.set(id, `<id${seen.size + 1}>`);
    return seen.get(id);
  });
}

test("a throwing subscriber cannot change journal bytes, send order or the result", async () => {
  const seen = [];
  const bare = await runOnce(null);
  const passive = await runOnce((r) => r.on((e) => seen.push(e.type)));
  const hostile = await runOnce((r) => r.on(() => { throw new Error("subscriber exploded"); }));

  for (const [label, got] of [["passive", passive], ["hostile", hostile]]) {
    assert.deepEqual(got.sends, bare.sends, `${label}: request order changed`);
    assert.equal(got.journal, bare.journal, `${label}: journal bytes changed`);
    assert.equal(got.storage, bare.storage, `${label}: persisted storage changed`);
    assert.equal(got.summary, bare.summary, `${label}: summary changed`);
  }
  assert.ok(seen.length > 0, "the passive subscriber should have observed events");
});

test("events describe the job lifecycle and carry item identity", async () => {
  const events = [];
  await runOnce((r) => r.on((e) => events.push(e)));
  const types = events.map((e) => e.type);

  assert.equal(types[0], "job:start");
  assert.equal(types.at(-1), "job:end");
  assert.equal(types.filter((t) => t === "item:start").length, 2);
  assert.equal(types.filter((t) => t === "item:end").length, 2);

  const starts = events.filter((e) => e.type === "item:start");
  assert.deepEqual(starts.map((e) => e.idx), [0, 1]);
  assert.deepEqual(starts.map((e) => e.name), ["Ev A", "Ev B"]);
  for (const e of events) {
    assert.equal(e.jobId, "ev-job");
    assert.equal(typeof e.at, "number");
  }
});

test("unsubscribing stops delivery, and subscribing is not required", async () => {
  const storage = new MemoryStorage();
  const d = composeForTest({ game: new FakeGame(), storage, idb: new IDBFactory(), clock: fakeClock() });
  const seen = [];
  const off = d.runner.on((e) => seen.push(e.type));
  off();
  d.runner.plan(MANIFEST, { jobId: "ev-off", manifestPath: "push/ev.json", manifestNumber: 1 });
  await d.runner.run("ev-off");
  assert.deepEqual(seen, []);
  assert.throws(() => d.runner.on("not a function"), TypeError);
});
