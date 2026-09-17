// Byte-identity guard for the five released Forge screens.
//
// Phase 0 moves orchestration out of the view layer. The contract is that the operator sees no
// change, and this is what makes that checkable rather than asserted: every scenario is rendered
// again here and compared byte for byte against the committed fixture. A diff means the rendered
// tree moved, which during an extraction is a defect until proven otherwise.
//
// To change a screen deliberately: change it, run `npm run fixtures`, and review the fixture diff
// as part of the change. Never regenerate to make a red extraction go green.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { installDom, renderScenarios } from "./screen_scenarios.mjs";

const DIR = join(dirname(fileURLToPath(import.meta.url)), "fixtures", "screens");

test("released screens render byte-identically to their committed fixtures", async () => {
  installDom();
  const scenarios = await renderScenarios();
  const committed = readdirSync(DIR).filter((f) => f.endsWith(".txt")).sort();

  assert.deepEqual(
    scenarios.map((s) => `${s.name}.txt`),
    committed,
    "scenario set and fixture set must match; run `npm run fixtures` after adding a scenario",
  );

  for (const { name, text } of scenarios) {
    const want = readFileSync(join(DIR, `${name}.txt`), "utf8");
    assert.equal(text, want, `screen fixture drift in ${name}; the rendered tree changed`);
  }
});

test("every released screen is covered by at least one fixture", async () => {
  const committed = readdirSync(DIR).filter((f) => f.endsWith(".txt"));
  for (const screen of ["jobs", "manifests", "run", "captures", "settings"]) {
    assert.ok(committed.some((f) => f.startsWith(screen + "_")), `no fixture covers the ${screen} screen`);
  }
});
