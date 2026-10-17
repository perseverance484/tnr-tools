// Bloodright Jutsu Reference Library — pilot capture manifest gate
// (brief: chatgpt/bloodright-reference-library-brief-20261016@1b3b93b3ac939afc2fed1c63390fe68ed0d261d6).
//
// Holds, socket-free, that push/101 is a capture-only Forge job: it parses under Forge's own
// parser, plans zero items, asks for `persist: "full"` on exactly the six pinned BR-023 jutsu
// point reads plus one optional bloodline.get, issues no procedure other than those reads against
// an in-process fake game, and exports each record body (with its `image`) unmodified.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { App } from "../src/ui/app.mjs";
import { parseManifest, planOrder } from "../src/runner/manifest.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const MANIFEST = new URL("../../push/101_bloodright_reference_ethereal_monarch_pilot_capture.json", import.meta.url);

// Pinned roster: fable/bloodright-planning-20261003@7c1dfdd5e3ee163b90c22694dbb2de94ede08866,
// docs/design/bloodright/roster.json blob 64f6097cb65daccd636f98c8f35517941b67aebb, BR-023.
const BLOODLINE_ID = "IxhIoLEmznqdcnc_6MCN9";
const JUTSU_IDS = Object.freeze([
  "0_ip_8I2Dh_Ti2mYUcuAu",
  "Q3hmgslgYbbLHwwOZckT-",
  "AK8P4xmHSdbUOh2ywzb1l",
  "q7QKL0ETYGDEawoF_yzkS",
  "xPfjuu4WMe786wDVaizik",
  "nvMSommJJLlG5xwT7nQ6b",
]);

const raw = () => JSON.parse(readFileSync(MANIFEST, "utf8"));

test("push/101 parses as a zero-item capture-only manifest with seven full point reads", () => {
  const m = parseManifest(readFileSync(MANIFEST, "utf8"));
  assert.equal(m.items.length, 0);
  assert.equal(planOrder(m).length, 0, "nothing to create or update");
  assert.equal(m.capture.after.length, 0);
  assert.equal(m.fullCaptures, 7);
  assert.ok(m.capture.before.every((c) => c.persist === "full"));
});

test("push/101 reads exactly the pinned BR-023 membership, once each, plus one bloodline identity read", () => {
  const before = raw().capture.before;
  const jutsu = before.filter((c) => c.proc === "jutsu.get").map((c) => c.input.id);
  assert.deepEqual(jutsu, JUTSU_IDS, "exact roster IDs in roster order");
  assert.equal(new Set(jutsu).size, 6, "no duplicate reads");
  const other = before.filter((c) => c.proc !== "jutsu.get");
  assert.deepEqual(other, [{ proc: "bloodline.get", input: { id: BLOODLINE_ID }, persist: "full" }]);
  for (const c of before) assert.deepEqual(Object.keys(c.input), ["id"], "point reads carry only an id");
});

test("push/101 runs against a fake game with zero mutations and exports every image byte-for-byte", async () => {
  const game = new FakeGame();
  const storage = new MemoryStorage();
  const rows = JUTSU_IDS.map((id, i) => game.seed("jutsu", {
    id, name: `fixture ${i}`, bloodlineId: BLOODLINE_ID, jutsuType: i === 5 ? "SPECIAL" : "BLOODLINE",
    image: `https://ui0arpl8sm.ufs.sh/f/fixture-${i}`,
  }));
  game.seed("bloodline", { id: BLOODLINE_ID, name: "Ethereal Monarch", rank: "S", image: "https://ui0arpl8sm.ufs.sh/f/fixture-bl" });

  const d = composeForTest({ game, storage });
  const app = new App({ version: "forge test", storage, now: d.clock, ...d, github: { list: async () => [], text: async () => "", put: async () => ({}) } });
  let exported = null;
  app.showExport = (t) => { exported = t; };

  d.runner.plan(raw(), { jobId: "br023", manifestPath: "push/101_bloodright_reference_ethereal_monarch_pilot_capture.json" });
  const s = await d.runner.run("br023");
  assert.equal(s.state, "DONE");
  assert.equal(s.outcome, "success");

  const paths = game.calls.map((c) => c.path);
  assert.ok(paths.length > 0);
  assert.ok(paths.every((p) => p === "jutsu.get" || p === "bloodline.get"), `unexpected procedure(s): ${[...new Set(paths)]}`);

  await app.exportJob("br023");
  const bundle = JSON.parse(exported);
  const caps = bundle.captures;
  assert.equal(caps.length, 7);
  for (const c of caps) {
    assert.equal(c.ok, true);
    assert.equal(c.persistOk, true, `${c.proc} ${c.input.id}: ${c.persistError}`);
  }
  JUTSU_IDS.forEach((id, i) => {
    const c = caps.find((x) => x.proc === "jutsu.get" && x.input.id === id);
    assert.deepEqual(c.data, rows[i], `${id} body exported exactly as read`);
    assert.equal(c.data.image, rows[i].image);
    assert.equal(c.data.bloodlineId, BLOODLINE_ID);
  });
});
