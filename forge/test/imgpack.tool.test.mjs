// The pack AUTHORING tool, tested against this repository's own git history.
//
// The tool's one job is to make the binding true by construction: it reads bytes with
// `git cat-file blob <commit>:<path>`, so a pack can only ever name content the repository already
// holds at that commit. A tool that hashed the working tree would happily emit a pack for a file
// nobody has committed, and Forge would then refuse it on the operator's phone - which is the right
// failure in the wrong place. These tests hold the reading-from-git half and the four refusals.

import { test } from "node:test";
import assert from "node:assert/strict";
import { statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { buildPack, resolveCommit, blobAt, sha256Hex } from "../tools/make_image_pack.mjs";

const REPO = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
// A committed image with a stable path, used as a stand-in for a processed art drop.
const ART_DIR = "art/style_refs/scene_backgrounds";
const ART_NAME = "drying_yard.webp";

const manifestFor = (name, bytes) => ({
  imgSizes: { [name]: bytes },
  items: [{ entity: "asset", slot: "create", name: "X", srcId: "x", data: { name: "X", hidden: true, type: "STATIC", url: `@img:${name}` } }],
});

test("the tool binds to a resolved 40-hex commit, never to the revision it was given", () => {
  const sha = resolveCommit("HEAD");
  assert.match(sha, /^[0-9a-f]{40}$/);
  assert.equal(resolveCommit(sha), sha, "an explicit commit resolves to itself");
});

test("the pack's digest is the digest of the COMMITTED blob, not of the working tree", () => {
  const ref = resolveCommit("HEAD");
  const path = `${ART_DIR}/${ART_NAME}`;
  const blob = blobAt(ref, path);
  const size = statSync(join(REPO, path)).size;
  assert.equal(blob.length, size, "this checkout is clean for the fixture file");

  const { pack, problems } = buildPack(manifestFor(ART_NAME, blob.length), { ref, root: ART_DIR });
  assert.deepEqual(problems, []);
  assert.equal(pack.ref, ref);
  assert.deepEqual(pack.files[ART_NAME], { path, sha256: sha256Hex(blob), bytes: blob.length });
  assert.match(pack.files[ART_NAME].sha256, /^[0-9a-f]{64}$/);
});

test("a file the commit does not hold is refused, and says to commit it first", () => {
  const ref = resolveCommit("HEAD");
  const { pack, problems } = buildPack(manifestFor("not_committed_anywhere.webp", 1234), { ref, root: ART_DIR });
  assert.equal(pack, null);
  assert.equal(problems.length, 1);
  assert.match(problems[0], /is not in commit [0-9a-f]{12}\. Commit the file first/);
});

test("a ledger that disagrees with the committed bytes is refused rather than silently corrected", () => {
  const ref = resolveCommit("HEAD");
  const real = blobAt(ref, `${ART_DIR}/${ART_NAME}`).length;
  const { pack, problems } = buildPack(manifestFor(ART_NAME, real + 1), { ref, root: ART_DIR });
  assert.equal(pack, null);
  assert.match(problems[0], new RegExp(`is ${real} bytes but imgSizes says ${real + 1}`));
  assert.match(problems[0], /do not just take the file's number/);

  // and no ledger entry at all names what L17 wants, with the real byte count to paste
  const noLedger = { ...manifestFor(ART_NAME, real), imgSizes: {} };
  const r2 = buildPack(noLedger, { ref, root: ART_DIR });
  assert.equal(r2.pack, null);
  assert.match(r2.problems[0], new RegExp(`no imgSizes entry.*this file is ${real} bytes`));
});

test("--map wins over --root, a traversing path is refused, and an extension swap is refused", () => {
  const ref = resolveCommit("HEAD");
  const real = blobAt(ref, `${ART_DIR}/${ART_NAME}`).length;
  const mapped = buildPack(manifestFor(ART_NAME, real), { ref, root: "art/nowhere", map: { [ART_NAME]: `${ART_DIR}/${ART_NAME}` } });
  assert.deepEqual(mapped.problems, []);
  assert.equal(mapped.pack.files[ART_NAME].path, `${ART_DIR}/${ART_NAME}`);

  const escaped = buildPack(manifestFor(ART_NAME, real), { ref, map: { [ART_NAME]: `../../${ART_NAME}` } });
  assert.equal(escaped.pack, null);
  assert.match(escaped.problems[0], /not allowed/);

  const swapped = buildPack(manifestFor("drying_yard.png", real), { ref, map: { "drying_yard.png": `${ART_DIR}/${ART_NAME}` } });
  assert.equal(swapped.pack, null);
  assert.match(swapped.problems[0], /is a webp, but the @img name is a png/);
});

test("a manifest with no @img reference is refused, not given an empty pack", () => {
  const ref = resolveCommit("HEAD");
  const { pack, problems } = buildPack({ items: [{ entity: "jutsu", slot: "create", name: "J", srcId: "j", data: { name: "J", hidden: true } }] }, { ref, root: ART_DIR });
  assert.equal(pack, null);
  assert.match(problems[0], /no @img references/);
});
