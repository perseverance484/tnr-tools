import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { checkReleasePin } from "../tools/check_release_pin.mjs";

const REPO = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const UPDATE_URL = "https://raw.githubusercontent.com/perseverance484/tnr-tools/main/forge_loader_user.js";

function fixtureRoot(loaderText) {
  const root = mkdtempSync(join(tmpdir(), "forge-loader-release-"));
  mkdirSync(join(root, "forge"), { recursive: true });
  mkdirSync(join(root, "state", "staged_workflows"), { recursive: true });
  mkdirSync(join(root, ".github", "scripts"), { recursive: true });
  writeFileSync(join(root, "forge_loader_user.js"), loaderText);
  writeFileSync(join(root, "forge", "package.json"), readFileSync(join(REPO, "forge", "package.json"), "utf8"));
  writeFileSync(join(root, "state", "staged_workflows", "release_pin.yml"), readFileSync(join(REPO, "state", "staged_workflows", "release_pin.yml"), "utf8"));
  writeFileSync(join(root, ".github", "scripts", "pin_release.py"), readFileSync(join(REPO, ".github", "scripts", "pin_release.py"), "utf8"));
  return root;
}

test("release loader: current install has a stable self-update channel and immutable bundle", () => {
  const loader = readFileSync(join(REPO, "forge_loader_user.js"), "utf8");
  assert.match(loader, new RegExp(`^// @updateURL\\s+${UPDATE_URL.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")}$`, "m"));
  assert.match(loader, new RegExp(`^// @downloadURL\\s+${UPDATE_URL.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")}$`, "m"));
  assert.match(loader, /^\/\/ @require\s+https:\/\/cdn\.jsdelivr\.net\/gh\/perseverance484\/tnr-tools@[0-9a-f]{40}\/forge_bundle\.js$/m);
  assert.deepEqual(checkReleasePin(), []);
});

test("release loader: a future package may be staged without exposing the future loader version", () => {
  const current = readFileSync(join(REPO, "forge_loader_user.js"), "utf8");
  const staged = current
    .replace(/^(\/\/ @version\s+)\S+$/m, "$10.2.0")
    .replace(/^(\/\/ @require\s+)/m, "// @x-release-pending 0.2.1\n$1");
  const root = fixtureRoot(staged);
  try {
    assert.deepEqual(checkReleasePin({ root }), []);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("release loader: pending staging never permits a moving bundle or a different update source", () => {
  const current = readFileSync(join(REPO, "forge_loader_user.js"), "utf8");
  const staged = current
    .replace(/^(\/\/ @version\s+)\S+$/m, "$10.2.0")
    .replace(/^(\/\/ @require\s+)/m, "// @x-release-pending 0.2.1\n$1")
    .replace(/tnr-tools@[0-9a-f]{40}\/forge_bundle\.js/, "tnr-tools@moving-branch/forge_bundle.js")
    .replace(UPDATE_URL, "https://example.invalid/forge_loader_user.js");
  const root = fixtureRoot(staged);
  try {
    const text = checkReleasePin({ root }).map((problem) => problem.text).join("; ");
    assert.match(text, /floats on "moving-branch"/);
    assert.match(text, /@updateURL must be/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
