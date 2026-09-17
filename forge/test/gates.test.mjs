// The static gates, run as tests so a local `npm test` fails for the same reason CI does.
import { test } from "node:test";
import assert from "node:assert/strict";
import { checkBoundaries } from "../tools/check_boundaries.mjs";
import { measure, BUDGET } from "../tools/check_bundle_budget.mjs";

test("no layer outside transport issues a request, and no game host is hardcoded", () => {
  const { files, findings, pin } = checkBoundaries();
  assert.ok(files >= 30, `only ${files} modules scanned`);
  assert.match(pin, /^[0-9a-f]{40}$/, "generated contracts must agree on one source pin");
  assert.deepEqual(findings, [], "boundary violations:\n" + findings.join("\n"));
});

test("the checked bundle is inside its raw and gzip budget", () => {
  const { raw, gzip } = measure();
  assert.ok(raw <= BUDGET.raw, `raw bundle ${raw} exceeds budget ${BUDGET.raw}`);
  assert.ok(gzip <= BUDGET.gzip, `gzip bundle ${gzip} exceeds budget ${BUDGET.gzip}`);
  // A budget far above the measurement stops being a ratchet. Kept honest deliberately.
  assert.ok(raw > BUDGET.raw * 0.7, "raw budget has drifted far above the bundle; re-set it");
});
