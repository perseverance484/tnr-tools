import { test } from "node:test";
import assert from "node:assert/strict";
import { Journal, JournalError, KEY_PREFIX, TERMINAL_ITEM_STATES, migrate, JOURNAL_VERSION } from "../src/storage/journal.mjs";
import { payloadHash, stableStringify } from "../src/storage/hash.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";

const specs = () => [
  { entity: "jutsu", op: "create", name: "A", srcId: "a", payloadHash: payloadHash({ name: "A" }) },
  { entity: "jutsu", op: "update", name: "B", targetId: "existing-id", payloadHash: payloadHash({ name: "B" }) },
  { entity: "asset", op: "create", name: "C", srcId: "c", payloadHash: payloadHash({ name: "C" }) },
];

function openJob(store, clock, id = "job1") {
  const j = new Journal(store, clock);
  j.open({ jobId: id, manifestPath: "push/99_x.json", manifestNumber: 99, manifestHash: "abc", items: specs() });
  return j;
}

test("hash: stable across key order, sensitive to value", () => {
  assert.equal(stableStringify({ b: 1, a: [2, { d: 3, c: 4 }] }), '{"a":[2,{"c":4,"d":3}],"b":1}');
  assert.equal(payloadHash({ x: 1, y: 2 }), payloadHash({ y: 2, x: 1 }));
  assert.notEqual(payloadHash({ x: 1 }), payloadHash({ x: 2 }));
  assert.equal(payloadHash(undefined), payloadHash(null));
});

test("open writes one key per job, derived listing has no separate index", () => {
  const s = new MemoryStorage(); const clock = fakeClock();
  const j = openJob(s, clock);
  assert.deepEqual(j.listJobIds(), ["job1"]);
  assert.equal(s.key(0), KEY_PREFIX + "job1");
  const job = j.get("job1");
  assert.equal(job.v, JOURNAL_VERSION);
  assert.equal(job.state, "RUNNING");
  assert.equal(job.items.length, 3);
  assert.equal(job.items[0].state, "PLANNED");
  assert.equal(job.items[0].phase, "create");
  assert.equal(job.items[1].phase, "update");
  assert.equal(job.items[1].entityId, "existing-id");
});

test("duplicate jobId refuses", () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  assert.throws(() => j.open({ jobId: "job1", items: specs() }), JournalError);
});

test("legal chain PLANNED -> SENT -> CONFIRMED -> SENT -> CONFIRMED -> VERIFIED (two-phase create)", () => {
  const s = new MemoryStorage(); const clock = fakeClock(); const j = openJob(s, clock);
  j.transition("job1", 0, "SENT");
  clock.tick();
  j.transition("job1", 0, "CONFIRMED", { entityId: "new-id-1", phase: "update" });
  clock.tick();
  j.transition("job1", 0, "SENT");
  clock.tick();
  j.transition("job1", 0, "CONFIRMED");
  j.transition("job1", 0, "VERIFIED");
  const it = j.get("job1").items[0];
  assert.equal(it.state, "VERIFIED");
  assert.equal(it.entityId, "new-id-1");
  assert.ok(it.sentAt && it.confirmedAt && it.verifiedAt);
});

test("THE INVARIANT: SENT can never go back to PLANNED", () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  j.transition("job1", 0, "SENT");
  assert.throws(() => j.transition("job1", 0, "PLANNED"), /illegal transition SENT -> PLANNED/);
  // and the failed attempt did not corrupt the record
  assert.equal(j.get("job1").items[0].state, "SENT");
});

test("terminal states accept nothing", () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  j.transition("job1", 1, "SENT"); j.transition("job1", 1, "CONFIRMED"); j.transition("job1", 1, "VERIFIED");
  for (const to of ["SENT", "PLANNED", "FAILED", "CONFIRMED"]) {
    assert.throws(() => j.transition("job1", 1, to), JournalError, "VERIFIED -> " + to);
  }
  j.transition("job1", 2, "FAILED", { error: "x" });
  assert.throws(() => j.transition("job1", 2, "SENT"), JournalError);
});

test("ORPHANED -> CONFIRMED is adoption; ORPHANED -> SENT is not allowed", () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  j.transition("job1", 2, "SENT");
  j.transition("job1", 2, "ORPHANED");
  assert.throws(() => j.transition("job1", 2, "SENT"), JournalError);
  j.transition("job1", 2, "CONFIRMED", { entityId: "adopted-id", phase: "update" });
  assert.equal(j.get("job1").items[2].entityId, "adopted-id");
});

test("withSent flushes SENT to disk BEFORE the thunk runs", async () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  let stateSeenInsideThunk = null;
  let writesBeforeThunk = null;
  const result = await j.withSent("job1", 0, async () => {
    // what is on disk at the moment the request would leave?
    stateSeenInsideThunk = JSON.parse(s.getItem(KEY_PREFIX + "job1")).items[0].state;
    writesBeforeThunk = s.log.length;
    return "response";
  });
  assert.equal(result, "response");
  assert.equal(stateSeenInsideThunk, "SENT");
  assert.equal(writesBeforeThunk, 2); // open + the SENT flush, nothing else in between
});

test("withSent: if the flush throws, the thunk never runs and nothing left", async () => {
  const s = new MemoryStorage({ quota: 4096 });
  const j = new Journal(s, fakeClock());
  j.open({ jobId: "j", items: [{ entity: "jutsu", op: "create", payloadHash: "0" }] });
  // now shrink quota so the next write fails
  s.quota = 10;
  let ran = false;
  await assert.rejects(() => j.withSent("j", 0, async () => { ran = true; }), /journal write failed/);
  assert.equal(ran, false);
  // the on-disk state is still PLANNED
  assert.equal(JSON.parse(s.getItem(KEY_PREFIX + "j")).items[0].state, "PLANNED");
});

test("CRASH before send: resume sees PLANNED, which is safe to send", async () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  const after = s.crash(); // evicted before any transition
  const j2 = new Journal(after, fakeClock());
  const r = j2.resumable();
  assert.equal(r.length, 1);
  assert.equal(r[0].items[0].state, "PLANNED");
  assert.deepEqual(j2.ambiguous("job1"), []);
});

test("CRASH after send, before response: resume sees SENT and it is ambiguous, not retried", async () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  let after = null;
  await j.withSent("job1", 0, async () => { after = s.crash(); /* evicted mid-flight */ });
  const j2 = new Journal(after, fakeClock());
  const amb = j2.ambiguous("job1");
  assert.equal(amb.length, 1);
  assert.equal(amb[0].idx, 0);
  assert.equal(amb[0].state, "SENT");
  // the only exits from SENT are CONFIRMED / ORPHANED / FAILED
  assert.throws(() => j2.transition("job1", 0, "PLANNED"), JournalError);
});

test("CRASH after response, before journal flush: journal still says SENT (the honest answer)", async () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  let after = null;
  await j.withSent("job1", 0, async () => "resp");
  // response arrived; runner is about to write CONFIRMED; eviction happens here
  after = s.crash();
  const j2 = new Journal(after, fakeClock());
  assert.equal(j2.get("job1").items[0].state, "SENT");
  assert.equal(j2.ambiguous("job1").length, 1);
});

test("CRASH mid two-phase create: create confirmed, update sent, eviction -> phase is recorded", async () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  await j.withSent("job1", 0, async () => {});
  j.transition("job1", 0, "CONFIRMED", { entityId: "id-1", phase: "update" });
  let after = null;
  await j.withSent("job1", 0, async () => { after = s.crash(); });
  const j2 = new Journal(after, fakeClock());
  const it = j2.get("job1").items[0];
  assert.equal(it.state, "SENT");
  assert.equal(it.phase, "update");
  assert.equal(it.entityId, "id-1"); // the id survived, so reconciliation knows which row
});

test("resumable excludes fully terminal jobs, includes PAUSED", () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  for (const i of [0, 1, 2]) { j.transition("job1", i, "FAILED"); }
  assert.deepEqual(j.resumable(), []);
  j.setJobState("job1", "PAUSED", { pause: { reason: "TOO_MANY_REQUESTS", path: "jutsu.get", until: 1 } });
  assert.equal(j.resumable().length, 1);
  assert.equal(j.get("job1").pause.path, "jutsu.get");
});

test("export is text and round-trips", () => {
  const s = new MemoryStorage(); const j = openJob(s, fakeClock());
  const text = j.exportText();
  const parsed = JSON.parse(text);
  assert.equal(parsed.version, JOURNAL_VERSION);
  assert.equal(parsed.jobs.length, 1);
  assert.equal(parsed.jobs[0].jobId, "job1");
});

test("migration: unknown future version throws, current passes through", () => {
  assert.throws(() => migrate({ v: 0 }), /no migration/);
  const job = { v: JOURNAL_VERSION, jobId: "x", items: [] };
  assert.equal(migrate(job), job);
});

test("corrupt record surfaces as JournalError, not a silent null", () => {
  const s = new MemoryStorage();
  s.setItem(KEY_PREFIX + "bad", "{not json");
  const j = new Journal(s, fakeClock());
  assert.throws(() => j.get("bad"), JournalError);
});

test("TERMINAL_ITEM_STATES is exactly VERIFIED, FAILED, SKIPPED", () => {
  assert.deepEqual([...TERMINAL_ITEM_STATES].sort(), ["FAILED", "SKIPPED", "VERIFIED"]);
});
