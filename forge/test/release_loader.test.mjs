import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { checkReleasePin } from "../tools/check_release_pin.mjs";

const REPO = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const UPDATE_URL = "https://raw.githubusercontent.com/perseverance484/tnr-tools/main/forge_loader_user.js";
const LOADER = readFileSync(join(REPO, "forge_loader_user.js"), "utf8");
// Every version in this file is DERIVED. The staged-release fixtures used to hard-code 0.2.0 and
// 0.2.1; when the package moved to 0.3.0 the fixture stopped describing a legal staging and the
// test went red, and once a real @x-release-pending line existed in the loader the same fixture
// went green again for the wrong reason (its insert produced two pending markers and the checker
// read the real one). Deriving both ends means the fixture stays a legal staging at any version.
const PKG_VERSION = JSON.parse(readFileSync(join(REPO, "forge", "package.json"), "utf8")).version;
const OLDER_VERSION = "0.0.1";

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

/** The loader as a development branch stages it: last released @version, pending = the package. */
function stagedLoader({ version = OLDER_VERSION, pending = PKG_VERSION } = {}) {
  const withoutPending = LOADER.replace(/^\/\/ @x-release-pending\s+\S+\n/m, "");
  return withoutPending
    .replace(/^(\/\/ @version\s+)\S+$/m, `$1${version}`)
    .replace(/^(\/\/ @require\s+)/m, `// @x-release-pending ${pending}\n$1`);
}

test("release loader: current install has a stable self-update channel and immutable bundle", () => {
  assert.match(LOADER, new RegExp(`^// @updateURL\\s+${UPDATE_URL.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")}$`, "m"));
  assert.match(LOADER, new RegExp(`^// @downloadURL\\s+${UPDATE_URL.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")}$`, "m"));
  assert.match(LOADER, /^\/\/ @require\s+https:\/\/cdn\.jsdelivr\.net\/gh\/perseverance484\/tnr-tools@[0-9a-f]{40}\/forge_bundle\.js$/m);
  assert.deepEqual(checkReleasePin(), []);
});

test("release loader: exactly one @x-release-pending marker, naming the package version", () => {
  const markers = LOADER.match(/^\/\/ @x-release-pending\s+\S+$/gm) || [];
  assert.equal(markers.length, 1, "a second marker would shadow the real one from the checker");
  assert.equal(markers[0].split(/\s+/)[2], PKG_VERSION);
});

test("release loader: a future package may be staged without exposing the future loader version", () => {
  const root = fixtureRoot(stagedLoader());
  try {
    assert.deepEqual(checkReleasePin({ root }), []);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("release loader: a pending marker that disagrees with the package is a blocker", () => {
  const root = fixtureRoot(stagedLoader({ pending: "9.9.9" }));
  try {
    const text = checkReleasePin({ root }).map((problem) => problem.text).join("; ");
    assert.match(text, /@x-release-pending 9\.9\.9 != forge\/package\.json/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("release loader: pending staging never permits a moving bundle or a different update source", () => {
  const staged = stagedLoader()
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

// ---------------------------------------------------------------- 0.4.0 activation metadata
//
// The protected-auth repair moved WHERE forge runs, so the loader metadata that decides where the
// bundle is injected is now part of the contract and is asserted here rather than reviewed by eye.

test("release loader: @match covers the whole game origin, both hosts, so the carrier route is reachable", () => {
  const matches = (LOADER.match(/^\/\/ @match\s+(\S+)$/gm) || []).map((line) => line.split(/\s+/)[2]);
  assert.deepEqual(matches, ["*://www.theninja-rpg.com/*", "*://theninja-rpg.com/*"]);
  // The 0.3.0 loader matched /forge only. Production canonicalises www -> apex, and the app may
  // redirect a signed-in operator away from the carrier, so a path-scoped match cannot hold.
  assert.ok(!matches.some((m) => m.includes("/forge")), "a /forge-only match cannot reach the carrier");
});

test("release loader: still document-start, because the /forge entry has to be stopped before it renders", () => {
  assert.match(LOADER, /^\/\/ @run-at\s+document-start$/m);
});

test("release loader: the loader documents that an unarmed page is untouched", () => {
  // @match now covers every game page, so the promise that Forge is inert unless armed is a
  // user-visible contract and belongs in the file the operator installs.
  assert.match(LOADER, /has NOT been armed[\s\S]*does nothing at all/);
});

test("release loader: the operator entry point is still /forge", () => {
  assert.match(LOADER, /theninja-rpg\.com\/forge/);
});
