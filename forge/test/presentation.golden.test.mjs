// The Godstorm golden fixture (plan §8).
//
// Every assertion below is a fact the finished Godstorm event actually has, and every one of them
// is DERIVED from committed evidence by the tooling rather than written into a spec. That is the
// point of the fixture: the first poster's numbers were typed, so nothing could disagree with them.
// If the tooling ever starts reading these out of the presentation spec instead, the spec parser
// refuses the key and this file stops being reachable - see presentation.adversarial.test.mjs.
//
// ZERO LIVE REQUESTS. Everything here reads files under the repository and `git cat-file`.

import { test } from "node:test";
import assert from "node:assert/strict";
import { resolve, join } from "node:path";
import { buildFromSpecFile, summarize } from "../presentation/build.mjs";
import { STATUS } from "../presentation/assets.mjs";
import { REPO, PKG, MARROW, STORMCOURT } from "./presentation.scenario.mjs";

const built = buildFromSpecFile(join(PKG, "spec.json"), { root: REPO });
const { dossier, lint, spec } = built;

test("the Godstorm dossier builds from committed evidence with no fatal finding", () => {
  assert.deepEqual(lint.fatal, [], "fatal findings:\n" + lint.fatal.map((f) => f.code + ": " + f.message).join("\n"));
  assert.equal(dossier.schema, "tnr.presentation.dossier.v1");
  assert.match(dossier.hash, /^[0-9a-f]{64}$/);
});

test("two top-level structures, and they are Marrow Vaults and Stormcourt", () => {
  assert.deepEqual(dossier.subject.components, ["Marrow Vaults", "Stormcourt"]);
  assert.deepEqual(Object.keys(dossier.structure).sort(), [MARROW, STORMCOURT].sort());
  assert.equal(dossier.structure[MARROW].questType, "battlepyramid");
  assert.equal(dossier.structure[STORMCOURT].questType, "battlepyramid");
});

test("25 battles each, 50 in total", () => {
  assert.equal(dossier.structure[MARROW].counts.battles, 25);
  assert.equal(dossier.structure[STORMCOURT].counts.battles, 25);
  assert.equal(dossier.totals.battles, 50);
});

test("5 keeper fights each, 10 in total", () => {
  const marrow = dossier.encounters.find((e) => e.questId === MARROW);
  const storm = dossier.encounters.find((e) => e.questId === STORMCOURT);
  assert.equal(marrow.keepers, 5);
  assert.equal(storm.keepers, 5);
  assert.equal(dossier.totals.keepers, 10);
  assert.deepEqual(marrow.keeperObjectiveIds, ["b1_boss", "b2_boss", "b3_boss", "b4_boss", "b5_boss"]);
  assert.deepEqual(storm.keeperObjectiveIds, ["b6_boss", "b7_boss", "b8_boss", "b9_boss", "b10_boss"]);
});

test("the cadence is four ordinary fights then one keeper, five times, in both pyramids", () => {
  for (const [questId, ordinary] of [[MARROW, "recurring"], [STORMCOURT, "ascendant"]]) {
    const e = dossier.encounters.find((x) => x.questId === questId);
    assert.equal(e.cadence.exact, true, `${e.name}: the battle sequence must tile`);
    assert.deepEqual(e.cadence.unit, [{ role: ordinary, count: 4 }, { role: "keeper", count: 1 }]);
    assert.equal(e.cadence.repeats, 5);
    assert.equal(e.cadenceText, `4 ${ordinary} fights then 1 keeper fight, repeated 5 times`);
  }
});

test("18 distinct AI records, the complete current roster, every one named and role-annotated", () => {
  assert.equal(dossier.totals.distinctAi, 18);
  assert.equal(dossier.roster.length, 18);
  assert.equal(new Set(dossier.roster.map((e) => e.aiId)).size, 18);
  assert.deepEqual(dossier.roster.filter((e) => !e.resolved), [], "every roster entry must be named by a selected record");
  assert.deepEqual(dossier.roster.filter((e) => !e.role).map((e) => e.aiId), [], "every roster entry must carry a validated role");
  assert.equal(spec.roster.coverage, "all");

  // the roster the evidence yields, in the order a player meets them
  assert.deepEqual(dossier.roster.map((e) => e.name), [
    "Umbral Reaver", "Hollow Lantern", "Starless Monk", "Nightveil Sentinel", "Warden of the First Dark",
    "Keeper of Hushed Hours", "The Moth Tyrant", "Chained Chorister", "Warden of the Half Eclipse",
    "Hollow Lantern Ascendant", "Starless Monk Ascendant", "Nightveil Sentinel Ascendant", "Umbral Reaver Ascendant",
    "The Gloaming Judge", "Widow of the Waning Moon", "The Candlewright", "Herald of the Last Dusk",
    "Sovereign Echo of the Godstorm",
  ]);
  const roles = dossier.roster.reduce((n, e) => ({ ...n, [e.role]: (n[e.role] ?? 0) + 1 }), {});
  assert.deepEqual(roles, { recurring: 4, keeper: 9, ascendant: 4, finalBoss: 1 });
});

test("exact art coverage for all 18, with provenance, and five bound to verified repository bytes", () => {
  assert.equal(dossier.assets.coverage.total, 18);
  assert.equal(dossier.assets.coverage.missing, 0);
  assert.equal(dossier.assets.coverage.mismatch, 0);
  assert.equal(dossier.assets.coverage.historical, 0);
  // all eighteen resolve to CURRENT art
  assert.equal(dossier.assets.coverage.exactBytes + dossier.assets.coverage.exactRemote, 18);
  // and every one of them says where that claim comes from
  for (const e of dossier.assets.entries) {
    assert.ok(e.liveUrl, `${e.name}: no current art url`);
    assert.ok(e.provenance.record, `${e.name}: no provenance record`);
    assert.ok(e.provenance.capturedAt, `${e.name}: no capture timestamp`);
  }

  // The five Marrow recurring avatars were shipped from this repository, so their whole chain is
  // checkable offline: working tree == blob at the pack's commit == what was uploaded == what the
  // live record serves.
  const bound = dossier.assets.entries.filter((e) => e.repoPath);
  assert.equal(bound.length, 5);
  assert.equal(dossier.assets.coverage.exactBytes, 5);
  for (const e of bound) {
    assert.equal(e.status, STATUS.EXACT_BYTES, `${e.name}: ${e.notes.join("; ")}`);
    assert.equal(e.refVerified, true, `${e.name}: the working-tree file must equal the blob at the pack's commit`);
    assert.equal(e.ref, "10fb25704dff1bab8105cd83631e0d524193ef0d");
    assert.equal(e.sha256, e.declaredSha256);
    assert.equal(e.uploadedUrl, e.liveUrl, `${e.name}: the bound bytes must be what this entity currently serves`);
  }
  assert.deepEqual(bound.map((e) => e.name).sort(), [
    "Hollow Lantern", "Nightveil Sentinel", "Starless Monk", "Umbral Reaver", "Warden of the First Dark",
  ]);

  // The other thirteen are current and provenanced but not yet materialised, which is a P1 result,
  // not a P1 defect: this task makes zero live requests. The lint says so rather than a renderer
  // discovering it.
  assert.equal(dossier.assets.coverage.exactRemote, 13);
  assert.equal(lint.warnings.filter((f) => f.code === "asset-remote").length, 13);
});

test("the current full-clear rewards, and no intermediate cash-out or reward item anywhere", () => {
  const marrow = dossier.rewards[MARROW];
  const storm = dossier.rewards[STORMCOURT];

  assert.equal(marrow.fullClear.objectiveId, "d5_victory");
  assert.deepEqual(marrow.fullClear.reward, { money: 125000, tokens: 25, prestige: 10 });
  assert.equal(storm.fullClear.objectiveId, "d10_victory");
  assert.deepEqual(storm.fullClear.reward, { money: 250000, tokens: 150, prestige: 60 });

  for (const [name, r] of [["Marrow Vaults", marrow], ["Stormcourt", storm]]) {
    assert.deepEqual(r.intermediateCashOuts, [], `${name} must have zero intermediate cash-outs`);
    assert.deepEqual(r.rewardItems, [], `${name} must grant no reward item`);
    assert.deepEqual(r.unreachableRewardNodes, [], `${name} must carry no stranded reward node`);
    assert.equal(r.reachableRewardNodes.length, 1, `${name} must have exactly one reachable reward node`);
    assert.deepEqual(r.questLevelReward, {}, `${name} must carry no quest-level reward`);
    assert.equal(r.fullClear.reward.items, undefined);
  }
});

test("the top-level locations are the two pyramids, not the scene backgrounds", () => {
  assert.deepEqual(dossier.locations.map((l) => l.name), ["Marrow Vaults", "Stormcourt"]);
  assert.deepEqual(dossier.locations.map((l) => l.kind), ["component", "component"]);

  // The three Stormcourt backgrounds the old poster listed as locations are here, as scene art.
  const sceneKeys = dossier.sceneAssets.map((a) => a.key);
  for (const id of ["7xVJ55rsqarfRmPqLdv98", "L_ziMXaLeT9FSdyQ9hkDi", "_vK9jDEE0zyop_t23Ijgy"]) {
    assert.ok(sceneKeys.includes(`asset:${id}`), `scene background ${id} must be recorded as scene art`);
  }
  for (const a of dossier.sceneAssets) {
    assert.ok(["scene-background", "scene-character"].includes(a.kind));
    assert.ok(!dossier.locations.some((l) => l.key === a.key), `${a.key} must not also be a location`);
  }
});

test("every narrative source id resolves against the current quest dialogue", () => {
  assert.equal(dossier.narrative.length, 2);
  const marrow = dossier.narrative.find((b) => b.component === MARROW);
  const storm = dossier.narrative.find((b) => b.component === STORMCOURT);
  assert.deepEqual(marrow.sourceObjectives.map((o) => o.objectiveId), ["d1_1", "d4_1", "d5_victory"]);
  assert.deepEqual(storm.sourceObjectives.map((o) => o.objectiveId), ["d6_1", "d9_1", "d10_victory"]);
  for (const block of dossier.narrative) {
    for (const o of block.sourceObjectives) {
      const structure = dossier.structure[o.questId];
      assert.ok(structure.reachableIds.includes(o.objectiveId), `${o.objectiveId} must be a reachable node`);
      assert.equal(o.task, "dialog");
    }
  }
});

test("the hidden/unpublished state is carried as provenance, not silently dropped", () => {
  assert.equal(dossier.structure[MARROW].hidden, true);
  assert.equal(dossier.structure[STORMCOURT].hidden, true);
  assert.equal(lint.warnings.filter((f) => f.code === "hidden-subject").length, 2);
});

test("every hard fact points at the evidence record it came from", () => {
  const recordIds = new Set(dossier.sources.records.map((r) => r.id));
  assert.equal(recordIds.size, 6);
  for (const [path, record] of Object.entries(dossier.provenance)) {
    assert.ok(recordIds.has(record), `${path} points at unknown record ${record}`);
  }
  for (const key of [
    `structure.${MARROW}.counts.battles`,
    `structure.${STORMCOURT}.counts.battles`,
    `rewards.${MARROW}.fullClear`,
    `rewards.${STORMCOURT}.fullClear`,
    `encounters.${MARROW}.sequence`,
  ]) {
    assert.ok(dossier.provenance[key], `${key} must carry provenance`);
  }
  assert.equal(dossier.provenance[`rewards.${MARROW}.fullClear`], "marrow-quest");
  assert.equal(dossier.provenance[`rewards.${STORMCOURT}.fullClear`], "stormcourt-quest");
  // every source carries the file digest and a timestamp, so "which bytes" is answerable
  for (const r of dossier.sources.records) {
    assert.match(r.sha256, /^[0-9a-f]{64}$/);
    assert.ok(r.capturedAt || r.ref, `${r.id} must carry a capture time or an immutable ref`);
  }
});

test("the five replaced avatars use the 09-19 capture, not the 09-14 one that also names them", () => {
  // This is the freshness rule doing its job on real evidence: the older bundle is in the package
  // because it is the only source for thirteen AIs, and it must not supply the five it is stale for.
  for (const name of ["Umbral Reaver", "Hollow Lantern", "Starless Monk", "Nightveil Sentinel", "Warden of the First Dark"]) {
    const e = dossier.roster.find((r) => r.name === name);
    assert.equal(e.source, "ai-2026-09-19", `${name} must be read from the newest capture`);
  }
  const storm = dossier.roster.find((r) => r.name === "Sovereign Echo of the Godstorm");
  assert.equal(storm.source, "ai-2026-09-14");
});

test("the dossier is deterministic: the same evidence rebuilds to the same hash", () => {
  const again = buildFromSpecFile(join(PKG, "spec.json"), { root: resolve(REPO) });
  assert.equal(again.dossier.hash, dossier.hash);
});

test("the golden summary reads the way the poster is supposed to", () => {
  const text = summarize(dossier);
  for (const line of [
    "components: Marrow Vaults, Stormcourt",
    "Marrow Vaults: 25 battles, 5 keepers - 4 recurring fights then 1 keeper fight, repeated 5 times",
    "Stormcourt: 25 battles, 5 keepers - 4 ascendant fights then 1 keeper fight, repeated 5 times",
    "totals: 50 battles, 10 keepers, 18 distinct AI",
    "Marrow Vaults full clear (d5_victory): 125000 money / 25 tokens / 10 prestige; 0 intermediate cash-out(s), 0 reward item(s)",
    "Stormcourt full clear (d10_victory): 250000 money / 150 tokens / 60 prestige; 0 intermediate cash-out(s), 0 reward item(s)",
    "art: 5 exact-with-bytes, 13 exact-remote, 0 historical, 0 missing, 0 mismatched, of 18",
  ]) {
    assert.ok(text.includes(line), `summary is missing:\n  ${line}\ngot:\n${text}`);
  }
});
