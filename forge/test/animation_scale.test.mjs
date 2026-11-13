// Per-effect animation size after upstream 8bd670153 (2026-11-09, "Allow animation sizing per combat
// effect"). BaseAttributes gained animationScale (1x-3x, default 1), so every combat tag accepts it and
// the live jutsu.update schema lists it on all 96 tag variants. nested.json is pinned to 3314d122,
// which predates the key, so before this change a manifest that sized a clip was refused as an
// unknown key. The Mother of Echoes clips were drawn for 2.5 hex heights; this key is how they get it.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { Validator, EFFECT_POST_PIN_KEYS } from "../src/runner/validate.mjs";

const SCHEMAS = JSON.parse(readFileSync(new URL("../src/runner/fields.json", import.meta.url), "utf8"));
const NESTED = JSON.parse(readFileSync(new URL("../src/runner/nested.json", import.meta.url), "utf8"));

const tag = (extra = {}) => ({
  type: "damage", description: "d", power: 10, powerPerLevel: 0, calculation: "static", direction: "offence", target: "INHERIT",
  staticAssetPath: "", staticAnimation: "", appearAnimation: "clip", disappearAnimation: "", appearSfx: "", disappearSfx: "", rounds: 0,
  ...extra,
});

test("animationScale: accepted on a combat tag of a jutsu and an item", () => {
  const v = new Validator(SCHEMAS, NESTED);
  assert.deepEqual([...EFFECT_POST_PIN_KEYS], ["animationScale"]);
  for (const entity of ["jutsu", "item"]) assert.deepEqual(v.nestedProblems(entity, { effects: [tag({ animationScale: 2.5 })] }), []);
  // a non-damage tag shape too: the key comes from BaseAttributes, not from one tag
  const mark = { type: "increaseregeneration", description: "m", power: 1, powerPerLevel: 0, calculation: "static", direction: "offence",
    target: "INHERIT", friendlyFire: "FRIENDLY", staticAssetPath: "", staticAnimation: "mark", appearAnimation: "", disappearAnimation: "",
    appearSfx: "", disappearSfx: "", rounds: 1, animationScale: 1 };
  assert.deepEqual(v.nestedProblems("jutsu", { effects: [mark] }), []);
});

test("animationScale: the allowance opens nothing else", () => {
  const v = new Validator(SCHEMAS, NESTED);
  // a misspelling is still refused
  assert.match(v.nestedProblems("jutsu", { effects: [tag({ animationSize: 2.5 })] }).join(";"), /unknown key "animationSize"/);
  // title effects are TitleEffectSchema members, which do not spread BaseAttributes
  const title = { type: "increasemastery", masteryTypes: ["Ninjutsu"], power: 1 };
  assert.deepEqual(v.nestedProblems("title", { effects: [title] }), []);
  assert.match(v.nestedProblems("title", { effects: [{ ...title, animationScale: 2 }] }).join(";"), /unknown key "animationScale"/);
  // keys only, never bounds (validate.mjs nestedProblems): the server enforces 1..3
  assert.deepEqual(v.nestedProblems("jutsu", { effects: [tag({ animationScale: 9 })] }), []);
});

test("animationScale: without it the pinned set still refuses it (guards a re-pin that drops the list)", () => {
  const v = new Validator(SCHEMAS, NESTED);
  const pinned = v.nested.effects.damage;
  assert.equal(pinned.includes("animationScale"), false, "nested.json now carries animationScale: retire EFFECT_POST_PIN_KEYS");
});
