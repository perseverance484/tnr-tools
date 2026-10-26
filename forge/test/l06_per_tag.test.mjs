// L06 per tag (RUL-2026-10-25-009, state/prompt_validate_stale_rules.md).
//
// L06 used to demand statTypes AND generalTypes on damage, pierce and wound. At the pinned game
// source (85cecaeb) WoundTag spreads IncludeGeneralsAndElements only (app/src/validators/combat.ts:760-762),
// so it has generalTypes and no statTypes, and Forge's nested key check refuses statTypes on a wound
// before the send. A correct wound therefore always tripped L06. The rule now takes each tag's
// statTypes/generalTypes requirement from the pinned key set in nested.json.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { parseManifest } from "../src/runner/manifest.mjs";
import { Validator, expandNested } from "../src/runner/validate.mjs";

const NESTED = JSON.parse(readFileSync(new URL("../src/runner/nested.json", import.meta.url), "utf8"));
const SCHEMAS = JSON.parse(readFileSync(new URL("../src/runner/fields.json", import.meta.url), "utf8"));
const STAT = ["Highest"], GEN = ["Highest"];
const jutsu = (effects) => ({ items: [{ entity: "jutsu", slot: "create", name: "J", srcId: "j", data: { name: "J", hidden: true, effects } }] });
const l06 = (effects) => parseManifest(jutsu(effects)).warnings.filter((w) => /L06/.test(w));

test("L06 per tag: the pinned key sets are what the rule reads", () => {
  const sets = expandNested(NESTED).effects;
  for (const t of ["damage", "pierce"]) {
    assert.ok(sets[t].includes("statTypes") && sets[t].includes("generalTypes"), t);
  }
  assert.ok(sets.wound.includes("generalTypes"), "wound has generalTypes");
  assert.ok(!sets.wound.includes("statTypes"), "wound has no statTypes at the pin");
});

test("L06 per tag: a wound with generalTypes and no statTypes is clean", () => {
  assert.deepEqual(l06([{ type: "damage", statTypes: STAT, generalTypes: GEN }, { type: "wound", generalTypes: GEN, calculation: "percentage" }]), []);
});

test("L06 per tag: a wound without generalTypes still warns, naming only generalTypes", () => {
  const w = l06([{ type: "damage", statTypes: STAT, generalTypes: GEN }, { type: "wound", calculation: "percentage" }]);
  assert.equal(w.length, 1);
  assert.match(w[0], /L06 wound missing generalTypes \(/);
  assert.doesNotMatch(w[0], /statTypes/);
});

test("L06 per tag: damage and pierce still need both keys", () => {
  for (const type of ["damage", "pierce"]) {
    assert.match(l06([{ type, generalTypes: GEN }]).join(";"), new RegExp(`L06 ${type} missing statTypes \\(`), type);
    assert.match(l06([{ type, statTypes: STAT }]).join(";"), new RegExp(`L06 ${type} missing generalTypes \\(`), type);
    assert.match(l06([{ type }]).join(";"), new RegExp(`L06 ${type} missing statTypes/generalTypes \\(`), type);
    assert.match(l06([{ type, statTypes: [], generalTypes: GEN }]).join(";"), new RegExp(`L06 ${type} missing statTypes \\(`), `${type} empty`);
    assert.deepEqual(l06([{ type, statTypes: STAT, generalTypes: GEN }]), [], type);
  }
});

test("L06 per tag: Forge's own key check still refuses statTypes on a wound", () => {
  // The lint no longer asks for the key, and the pre-send check still rejects it: the two now agree.
  const v = new Validator(SCHEMAS, NESTED);
  const p = v.problems("jutsu", { name: "J", effects: [{ type: "wound", statTypes: STAT, generalTypes: GEN }] }, null, { preCreate: true });
  assert.match(p.join(";"), /effects\[0\] \(wound\): unknown key "statTypes"/);
});

test("L06 per tag: push/261 (Lastlight) carries no L06 advisory", () => {
  const m = JSON.parse(readFileSync(new URL("../../push/261_lastlight_jutsu_create.json", import.meta.url), "utf8"));
  assert.deepEqual(parseManifest(m).warnings.filter((w) => /L06/.test(w)), []);
});
