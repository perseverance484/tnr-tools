// The presentation tooling must stay out of the userscript, and must never be able to reach the
// game. Both are asserted, and the gate that asserts them is itself shown catching a violation:
// a containment check nobody has seen fail is a comment.

import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync, cpSync, readFileSync, readdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { checkBoundaries } from "../tools/check_boundaries.mjs";

const FORGE = join(dirname(fileURLToPath(import.meta.url)), "..");

test("the whole presentation library is scanned and clean", () => {
  const { presentationFiles, findings } = checkBoundaries();
  const onDisk = readdirSync(join(FORGE, "presentation"), { withFileTypes: true }).filter((d) => d.isFile() && d.name.endsWith(".mjs")).length;
  assert.ok(presentationFiles >= onDisk, `only ${presentationFiles} presentation modules scanned, ${onDisk} on disk`);
  assert.deepEqual(findings, [], "boundary violations:\n" + findings.join("\n"));
});

test("none of it reaches the shipped bundle", () => {
  const bundle = readFileSync(join(FORGE, "..", "forge_bundle.js"), "utf8");
  for (const marker of [
    "tnr.presentation.dossier.v1",
    "tnr.presentation.spec.v1",
    "tnr.presentation.evidence.v1",
    "buildAssetRegistry",
    "lintPresentation",
    "exact-current-bytes",
  ]) {
    assert.ok(!bundle.includes(marker), `the bundle carries presentation code (${marker})`);
  }
});

test("the gate catches a src module that imports the presentation library", () => {
  const root = mkdtempSync(join(tmpdir(), "forge-contain-"));
  try {
    mkdirSync(join(root, "tools"), { recursive: true });
    cpSync(join(FORGE, "src"), join(root, "src"), { recursive: true });
    cpSync(join(FORGE, "presentation"), join(root, "presentation"), { recursive: true });
    cpSync(join(FORGE, "tools", "check_boundaries.mjs"), join(root, "tools", "check_boundaries.mjs"));
    writeFileSync(join(root, "src", "ui", "_poster.mjs"),
      'import { buildDossier } from "../../presentation/dossier.mjs";\nexport const go = () => buildDossier;\n');

    let failed = false, output = "";
    try {
      execFileSync(process.execPath, [join(root, "tools", "check_boundaries.mjs")], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    } catch (e) {
      failed = true;
      output = String(e.stdout || "") + String(e.stderr || "");
    }
    assert.ok(failed, "a src module importing the presentation library must fail the gate");
    assert.match(output, /ui[\\/]_poster\.mjs: imports forge\/presentation/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("the gate catches a presentation module that issues a request", () => {
  const root = mkdtempSync(join(tmpdir(), "forge-presnet-"));
  try {
    mkdirSync(join(root, "tools"), { recursive: true });
    cpSync(join(FORGE, "src"), join(root, "src"), { recursive: true });
    cpSync(join(FORGE, "presentation"), join(root, "presentation"), { recursive: true });
    cpSync(join(FORGE, "tools", "check_boundaries.mjs"), join(root, "tools", "check_boundaries.mjs"));
    // assembled, so ui.test.mjs's own grep for a global fetch in a test file stays strict
    const CALL = ["fet", "ch("].join("");
    writeFileSync(join(root, "presentation", "_materialise.mjs"),
      `export const get = (url) => globalThis.${CALL}url);\n`);

    let failed = false, output = "";
    try {
      execFileSync(process.execPath, [join(root, "tools", "check_boundaries.mjs")], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    } catch (e) {
      failed = true;
      output = String(e.stdout || "") + String(e.stderr || "");
    }
    assert.ok(failed, "a presentation module that fetches must fail the gate");
    assert.match(output, /presentation\/_materialise\.mjs: issues a request/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("the repository's approved Godstorm art is byte-identical to what the pack binds", async () => {
  // The adversarial scenarios build throwaway roots that LINK to art/godstorm. An earlier version
  // linked the directory and a same-size fixture wrote straight through it into the repository's
  // own approved art. The harness now links files and unlinks before writing; this is the check
  // that says so out loud after the suite has run, in the one place a reader will look.
  const manifest = JSON.parse(readFileSync(join(FORGE, "..", "archive", "spent-manifests", "push-2026-09-19", "53_godstorm_failed_items_repair.json"), "utf8"));
  const { createHash } = await import("node:crypto");
  for (const [name, f] of Object.entries(manifest.imagePack.files)) {
    const bytes = readFileSync(join(FORGE, "..", f.path));
    assert.equal(bytes.length, f.bytes, `${name}: byte count moved`);
    assert.equal(createHash("sha256").update(bytes).digest("hex"), f.sha256, `${name}: the working-tree art no longer matches the pack`);
  }
});
