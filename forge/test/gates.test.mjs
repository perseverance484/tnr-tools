// The static gates, run as tests so a local `npm test` fails for the same reason CI does.
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, cpSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { checkBoundaries } from "../tools/check_boundaries.mjs";

const FORGE = join(dirname(fileURLToPath(import.meta.url)), "..");
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

test("the boundary gate catches a QUALIFIED fetch, not just a bare one", () => {
  // `globalThis.fetch("/api/...")` reaches the game from a forbidden layer without naming a host.
  // The first detector used a negative lookbehind that excluded anything after a dot, so this form
  // passed cleanly. Independent review F2.
  const root = mkdtempSync(join(tmpdir(), "forge-bound-"));
  try {
    mkdirSync(join(root, "tools"), { recursive: true });
    cpSync(join(FORGE, "src"), join(root, "src"), { recursive: true });
    cpSync(join(FORGE, "tools", "check_boundaries.mjs"), join(root, "tools", "check_boundaries.mjs"));
    // The token is assembled rather than written as a literal. ui.test.mjs greps every test file
    // for a global fetch call and cannot tell a call from a fixture string; keeping that guard
    // strict is worth more than the convenience of a literal here.
    const CALL = ["fet", "ch("].join("");
    writeFileSync(join(root, "src", "runner", "_net.mjs"), `export const go = () => globalThis.${CALL}"/api/trpc/jutsu.get");\n`);
    writeFileSync(join(root, "src", "core", "_net.mjs"), `export const go = () => window.${CALL}"/api/trpc/item.get");\n`);
    writeFileSync(join(root, "src", "storage", "_net.mjs"), `export const go = () => ${CALL}"/api/trpc/ai.get");\n`);

    let failed = false, output = "";
    try {
      execFileSync(process.execPath, [join(root, "tools", "check_boundaries.mjs")], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    } catch (e) {
      failed = true;
      output = String(e.stdout || "") + String(e.stderr || "");
    }
    assert.ok(failed, "a qualified fetch outside transport must fail the gate");
    for (const layer of ["runner", "core", "storage"]) {
      assert.match(output, new RegExp(`${layer}/_net\\.mjs: issues a request`));
    }
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("the injected fetchImpl seam is not mistaken for a request", () => {
  // compose() hands win.fetch.bind(win) to the transport layer. That is the seam working, not a
  // layer reaching for the network, and flagging it would make the gate unusable.
  const root = mkdtempSync(join(tmpdir(), "forge-seam-"));
  try {
    mkdirSync(join(root, "tools"), { recursive: true });
    cpSync(join(FORGE, "src"), join(root, "src"), { recursive: true });
    cpSync(join(FORGE, "tools", "check_boundaries.mjs"), join(root, "tools", "check_boundaries.mjs"));
    const BIND = ["fet", "ch.bind"].join("");
    writeFileSync(join(root, "src", "runner", "_seam.mjs"), `export const use = (fetchImpl) => fetchImpl("/x");\nexport const hand = (win) => win.${BIND}(win);\n`);
    execFileSync(process.execPath, [join(root, "tools", "check_boundaries.mjs")], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
