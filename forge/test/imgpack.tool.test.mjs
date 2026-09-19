// The pack AUTHORING tool, tested against this repository's own git history.
//
// The tool's one job is to make the binding true by construction: it reads bytes with
// `git cat-file blob <commit>:<path>`, so a pack can only ever name content the repository already
// holds at that commit. A tool that hashed the working tree would happily emit a pack for a file
// nobody has committed, and Forge would then refuse it on the operator's phone - which is the right
// failure in the wrong place. These tests hold the reading-from-git half and the four refusals.

import { test } from "node:test";
import assert from "node:assert/strict";
import { statSync, readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { buildPack, resolveCommit, blobAt, sha256Hex, splicePack, roundTrips, hasCommit, isShallow } from "../tools/make_image_pack.mjs";

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

test("--write preserves the repository's formatting, so the diff is the inserted block and nothing else", () => {
  // The defect this pins: writing at indent 2 turned a twelve-line addition to push/53 into 2,762
  // insertions and 2,717 deletions. Semantically identical, and useless to review.
  const manifest = {
    _note: "fixture",
    dedupNames: true,
    imgSizes: { "a.webp": 10, "b.webp": 20 },
    items: [{ entity: "asset", slot: "create", name: "A", srcId: "a", data: { name: "A", hidden: true, url: "@img:a.webp" } }],
  };
  const text = JSON.stringify(manifest, null, 1) + "\n";
  assert.equal(roundTrips(text), true, "a push/ manifest is written at one space");

  const pack = { ref: "a".repeat(40), files: { "a.webp": { path: "art/x/a.webp", sha256: "b".repeat(64), bytes: 10 } } };
  const out = splicePack(text, pack);

  // THE property, stated directly: strip the pack back out and the text is the original, byte for
  // byte. Nothing else was re-indented, reordered or re-escaped.
  const stripped = JSON.parse(out);
  delete stripped.imagePack;
  assert.equal(JSON.stringify(stripped, null, 1) + "\n", text,
    "splicing the pack changed something other than the pack");
  // and the addition really is small: the pack's own lines, not the whole file
  const addedLines = out.split("\n").length - text.split("\n").length;
  assert.ok(addedLines > 0 && addedLines < 20, `expected a small insertion, got ${addedLines} new lines`);

  // and the pack sits next to the ledger it must agree with
  const parsed = JSON.parse(out);
  assert.deepEqual(Object.keys(parsed), ["_note", "dedupNames", "imgSizes", "imagePack", "items"]);
  assert.deepEqual(parsed.imagePack, pack);
  assert.equal(roundTrips(out), true, "the result is itself a well-formed push/ manifest");

  // re-splicing is idempotent and does not stack a second pack or move imgSizes
  assert.equal(splicePack(out, pack), out);
});

test("push/53's COMMITTED pack matches the COMMITTED blobs, entry for entry", () => {
  // The guard that stops the pack drifting from the art. If anyone re-processes one of the eight
  // Godstorm images and forgets to regenerate the pack, this fails here rather than on the
  // operator's phone at Start. It reads the blob out of the commit the pack itself names, so it
  // also proves that commit still holds those paths.
  const manifestPath = join(REPO, "push", "53_godstorm_failed_items_repair.json");
  const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
  const pack = manifest.imagePack;
  if (!pack) return; // the pack is staged separately from the Forge feature; nothing to check yet

  assert.match(pack.ref, /^[0-9a-f]{40}$/, "a pack binds an immutable commit");
  if (!hasCommit(pack.ref)) {
    // A shallow clone cannot see the commit the pack names, which is a fact about the checkout and
    // not about the pack. CI fetches full history (.github/workflows/forge.yml) precisely so this
    // guard can do its job; anywhere else, say why it could not rather than reporting a mismatch.
    assert.ok(isShallow(), `commit ${pack.ref.slice(0, 12)} is missing from a COMPLETE clone; the pack names history this repository does not have`);
    console.log(`  (skipped: shallow clone, ${pack.ref.slice(0, 12)} not present; run git fetch --unshallow to check the pack)`);
    return;
  }
  const names = Object.keys(pack.files);
  assert.equal(names.length, 8, "the Godstorm repair binds eight images");
  for (const name of names) {
    const e = pack.files[name];
    const blob = blobAt(pack.ref, e.path);
    assert.equal(blob.length, e.bytes, `${name}: the committed blob is ${blob.length} bytes, the pack says ${e.bytes}`);
    assert.equal(sha256Hex(blob), e.sha256, `${name}: the committed blob's digest is not the one the pack names`);
    assert.equal(manifest.imgSizes[name], e.bytes, `${name}: imgSizes and the pack disagree`);
    // the bytes are a real WebP, not a renamed master
    assert.equal(blob.subarray(0, 4).toString("latin1"), "RIFF", `${name} is not a RIFF container`);
    assert.equal(blob.subarray(8, 12).toString("latin1"), "WEBP", `${name} is not a WebP`);
    assert.ok(blob.length <= 512 * 1024, `${name} is over the 512KB presign ceiling`);
  }
});
