// Repo-backed image packs, end to end and adversarially.
//
// The feature's claim is narrow and checkable: the bytes Forge uploads for an `@img` reference are
// the bytes a named commit holds at a named path, and if they are not, nothing is uploaded. Every
// test below exists because some way of breaking that claim is cheap:
//
//   - a binding that can move          -> `ref` must be a 40-hex commit, never a branch;
//   - a path that escapes the repo      -> plain relative segments only;
//   - a cache that answers the wrong    -> the cache key IS the digest;
//     question
//   - a digest nobody checked           -> verified on every fetch AND every cache hit;
//   - a stale URL under the same name   -> upload reuse is keyed by content, not by filename;
//   - a picker that overrides provenance-> a bound image has no manual override, and the Start gate
//                                          re-reads the runner's own maps at the moment of the tap.
//
// The production shape under test is push/53 (the Godstorm repair): three Stormcourt backgrounds and
// five Marrow avatars, the same eight files whose manual selection cost nine live writes in
// harvests/inbox/tnr_results_1789829183863.json.

import { test } from "node:test";
import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { IDBFactory } from "fake-indexeddb";
import { parseManifest, ManifestError } from "../src/runner/manifest.mjs";
import { normalizeImagePack, packWork, pathProblem, toHex, unboundNames } from "../src/runner/imgpack.mjs";
import { prepareImagePack, commitImagePack, packGateProblems } from "../src/core/imagepack.mjs";
import { AssetCache, readAssetUploads, ASSET_UPLOADS_KEY } from "../src/storage/assets.mjs";
import { readIdmap, writeIdmap } from "../src/storage/compat.mjs";
import { ForgeCore } from "../src/core/core.mjs";
import { sha256 } from "../src/main.mjs";
import { FakeGame } from "./fakegame.mjs";
import { MemoryStorage, fakeClock } from "./shim.mjs";
import { composeForTest } from "./compose.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const REPAIR_53 = join(HERE, "..", "..", "push", "53_godstorm_failed_items_repair.json");
const COMMIT = "28bba70d0e14f74a768193881b592b92326f2867"; // a real 40-hex commit, used as a literal ref

// The eight Godstorm files and their processed-WebP byte counts, from push/53's own imgSizes.
const GODSTORM = Object.freeze({
  "bg_godstorm_stormcourt_upper_court.webp": 379928,
  "bg_godstorm_stormcourt_binding_dais_active.webp": 283000,
  "bg_godstorm_stormcourt_binding_dais_released.webp": 256826,
  "ai_godstorm_marrow_starless_monk.webp": 207410,
  "ai_godstorm_marrow_hollow_lantern.webp": 196056,
  "ai_godstorm_marrow_umbral_reaver.webp": 161650,
  "ai_godstorm_marrow_nightveil_sentinel.webp": 115618,
  "ai_godstorm_marrow_warden_of_the_first_dark.webp": 238510,
});

/** Deterministic bytes of an exact length, so a digest is reproducible across runs. */
function bytesOf(size, seed = 1) {
  const a = new Uint8Array(size);
  let x = (seed * 2654435761) >>> 0 || 1;
  for (let i = 0; i < size; i++) { x = (Math.imul(x, 1103515245) + 12345) >>> 0; a[i] = (x >>> 16) & 0xff; }
  return a.buffer;
}
const hexOf = async (bytes) => toHex(await sha256(bytes));

/** A fake repository: path@ref -> ArrayBuffer, with every raw() recorded. */
function fakeRepo(blobs = new Map(), { manifestText = "{}" } = {}) {
  const calls = [];
  return {
    blobs, calls,
    list: async () => [],
    text: async () => manifestText,
    put: async () => ({ sha: "s" }),
    raw: async (path, ref) => {
      calls.push({ path, ref });
      const key = `${ref}:${path}`;
      if (!blobs.has(key)) throw new Error(`fetch ${path}: HTTP 404`);
      const v = blobs.get(key);
      if (v instanceof Error) throw v;
      return v;
    },
  };
}

/** Build a pack (and the fake repo holding its blobs) for a set of logical names. */
async function packFor(names, { ref = COMMIT, dir = "art/godstorm", seed = 1, sizes = GODSTORM } = {}) {
  const files = {}; const blobs = new Map();
  let i = seed;
  for (const name of names) {
    const bytes = bytesOf(sizes[name], i++);
    const path = `${dir}/${name}`;
    files[name] = { path, sha256: await hexOf(bytes), bytes: sizes[name] };
    blobs.set(`${ref}:${path}`, bytes);
  }
  return { pack: { ref, files }, blobs };
}

/** A DOM-less core over the fake game, serving one manifest text and one fake repository. */
function headlessCore(text, github) {
  const storage = new MemoryStorage();
  const clock = fakeClock();
  const d = composeForTest({ game: new FakeGame(), storage, idb: new IDBFactory(), clock });
  d.github = github ?? fakeRepo(new Map(), { manifestText: text });
  const notes = [];
  const core = new ForgeCore({ version: "test", storage, now: clock, ...d });
  core.subscribe((n) => notes.push(n));
  return { core, notes, storage, journal: d.journal, github: d.github, clock };
}

/** An uploader that records what it was handed, so a test can prove WHICH bytes went out. */
function recordingUploader() {
  const uploads = [];
  return {
    uploads,
    async upload(file) {
      const buf = await file.arrayBuffer();
      const digest = await hexOf(buf);
      uploads.push({ name: file.name, size: file.size, type: file.type, digest });
      return { ufsUrl: `https://utfs.io/f/${digest.slice(0, 16)}`, key: digest.slice(0, 8), fileHash: digest };
    },
  };
}

/** A manifest of asset creates, one per image, in the shape push/53's backgrounds use. */
function manifestWith(names, pack, { sizes = GODSTORM } = {}) {
  const m = {
    _note: "repo-backed image pack fixture",
    imgSizes: Object.fromEntries(names.map((n) => [n, sizes[n]])),
    items: names.map((n, i) => ({
      entity: "asset", slot: "create", name: `Godstorm ${i}`, srcId: `gs_${i}`,
      data: { name: `Godstorm ${i}`, hidden: true, type: "STATIC", url: `@img:${n}` },
    })),
  };
  if (pack) m.imagePack = pack;
  return JSON.stringify(m);
}

// Deliberately WITHOUT `runner`: prepareImagePack() must not be able to write runner state, and
// handing it no runner is the cheapest structural proof that it does not try (review F2).
const ctxOf = (core) => ({ github: core.github, assetCache: core.assetCache, digest: core.digest, now: core.now });

/** Prepare, then commit — what ForgeCore does when the selection is still the current one. */
async function prepareAndCommit(core, { pack, names, force = false }) {
  const result = await prepareImagePack(ctxOf(core), { pack, names, force });
  commitImagePack(core.runner, { pack, names, staged: result.staged });
  return result;
}

// ================================================================== 1. the manifest contract

test("a well-formed pack parses, normalizes and reaches the manifest", async () => {
  const names = Object.keys(GODSTORM);
  const { pack } = await packFor(names);
  const m = parseManifest(manifestWith(names, pack));
  assert.equal(m.imagePack.ref, COMMIT);
  assert.deepEqual(Object.keys(m.imagePack.files).sort(), [...names].sort());
  assert.deepEqual(m.warnings, [], "a pack that binds exactly what the manifest references is silent");
  for (const n of names) {
    assert.match(m.imagePack.files[n].sha256, /^[0-9a-f]{64}$/);
    assert.equal(m.imagePack.files[n].bytes, GODSTORM[n]);
  }
});

test("ref must be an IMMUTABLE 40-hex commit: a branch, a tag and a short sha are all refused", async () => {
  const names = ["ai_godstorm_marrow_umbral_reaver.webp"];
  const { pack } = await packFor(names);
  for (const ref of ["main", "v1.2.0", COMMIT.slice(0, 7), COMMIT.toUpperCase(), "", null, 42]) {
    assert.throws(() => parseManifest(manifestWith(names, { ...pack, ref })),
      /imagePack\.ref must be a 40-hex commit sha/,
      `${JSON.stringify(ref)} must not be accepted as a binding`);
  }
  // and the one that is fine
  assert.equal(parseManifest(manifestWith(names, pack)).imagePack.ref, COMMIT);
});

test("a path must be repository-relative and plain; traversal, absolutes and URLs are refused", () => {
  assert.equal(pathProblem("art/godstorm/a.webp"), null);
  assert.match(pathProblem("../../etc/passwd"), /not allowed/);
  assert.match(pathProblem("art/../../x.webp"), /not allowed/);
  assert.match(pathProblem("/etc/passwd"), /repository-relative/);
  assert.match(pathProblem("https://evil.example/x.webp"), /looks like a URL/);
  assert.match(pathProblem("art\\godstorm\\a.webp"), /backslash/);
  assert.match(pathProblem("art//a.webp"), /empty segment/);
  assert.match(pathProblem("art/god storm/a.webp"), /outside \[A-Za-z0-9\._-\]/);
  assert.match(pathProblem(""), /non-empty/);
  assert.match(pathProblem("a/".repeat(200) + "x.webp"), /longer than 255/);
});

test("a malformed pack is a PARSE failure, so no job can be opened with one", async () => {
  const name = "ai_godstorm_marrow_umbral_reaver.webp";
  const { pack } = await packFor([name]);
  const good = pack.files[name];
  const cases = [
    [{ ...good, sha256: good.sha256.toUpperCase() }, /sha256 must be 64 lowercase hex/],
    [{ ...good, sha256: "deadbeef" }, /sha256 must be 64 lowercase hex/],
    [{ ...good, sha256: undefined }, /sha256 must be 64 lowercase hex/],
    [{ ...good, bytes: 0 }, /bytes must be a positive integer/],
    [{ ...good, bytes: 1.5 }, /bytes must be a positive integer/],
    [{ ...good, bytes: "161650" }, /bytes must be a positive integer/],
    [{ ...good, path: "art/godstorm/x.png" }, /repository file is a png but the @img name is a webp/],
    [{ ...good, path: undefined }, /path must be a non-empty string/],
    ["a string", /must be an object \{path, sha256, bytes\}/],
  ];
  for (const [entry, re] of cases) {
    assert.throws(() => parseManifest(manifestWith([name], { ref: COMMIT, files: { [name]: entry } })), re,
      `${JSON.stringify(entry)} must be refused`);
  }
  assert.throws(() => parseManifest(manifestWith([name], { ref: COMMIT, files: {} })), /imagePack\.files is empty/);
  assert.throws(() => parseManifest(manifestWith([name], { ref: COMMIT })), /imagePack\.files must be an object/);
  assert.throws(() => parseManifest(manifestWith([name], [pack])), /imagePack must be an object/);
});

test("a pack that disagrees with imgSizes about one file is refused, and both numbers are named", async () => {
  const name = "ai_godstorm_marrow_hollow_lantern.webp";
  const { pack } = await packFor([name]);
  const text = JSON.parse(manifestWith([name], pack));
  text.imagePack.files[name].bytes = GODSTORM[name] + 1;
  assert.throws(() => parseManifest(JSON.stringify(text)),
    new RegExp(`bytes is ${GODSTORM[name] + 1} but imgSizes says ${name.replace(/\./g, "\\.")} is ${GODSTORM[name]}`));

  // and a pack entry with no ledger entry at all: L17's ledger is what the Start gate checks the
  // File against, so a binding it cannot be cross-checked against is refused rather than trusted.
  const orphan = JSON.parse(manifestWith([name], pack));
  delete orphan.imgSizes[name];
  assert.throws(() => parseManifest(JSON.stringify(orphan)), /L17 @img:.* has no imgSizes byte entry/);
});

test("a pack entry nothing references is an advisory, not a refusal, and is never fetched", async () => {
  const used = "ai_godstorm_marrow_umbral_reaver.webp";
  const spare = "ai_godstorm_marrow_starless_monk.webp";
  const { pack, blobs } = await packFor([used, spare]);
  const text = JSON.parse(manifestWith([used], pack));
  text.imgSizes[spare] = GODSTORM[spare]; // ledgered, bound, but no @img uses it
  const m = parseManifest(JSON.stringify(text));
  assert.equal(m.warnings.length, 1);
  assert.match(m.warnings[0], /imagePack binds ai_godstorm_marrow_starless_monk\.webp, which no @img reference/);

  assert.deepEqual(packWork(m.imagePack, [used]).map((w) => w.name), [used], "only what is referenced is work");
  const { core } = headlessCore("{}", fakeRepo(blobs));
  const result = await prepareImagePack(ctxOf(core), { pack: m.imagePack, names: [used] });
  assert.equal(result.entries.length, 1);
  assert.deepEqual(core.github.calls.map((c) => c.path), [pack.files[used].path], "the unused binding is not fetched");
});

test("a pack need not cover every image: the rest stay the manual picker's", async () => {
  const bound = "bg_godstorm_stormcourt_upper_court.webp";
  const picked = "ai_godstorm_marrow_starless_monk.webp";
  const { pack } = await packFor([bound]);
  const m = parseManifest(manifestWith([bound, picked], pack));
  assert.deepEqual(unboundNames(m.imagePack, [bound, picked]), [picked]);
  assert.deepEqual(packWork(m.imagePack, [bound, picked]).map((w) => w.name), [bound]);
});

// ------------------------------------------------------------------ manifest identity

test("manifest identity covers the pack, and a manifest without one keeps the hash it already had", async () => {
  const names = ["bg_godstorm_stormcourt_upper_court.webp"];
  const { pack } = await packFor(names);
  const plain = manifestWith(names, null);
  const packed = manifestWith(names, pack);
  const hPlain = parseManifest(plain).hash;
  const hPacked = parseManifest(packed).hash;
  assert.notEqual(hPlain, hPacked, "two manifests that upload different bytes are not the same run");

  // A DIFFERENT pack over the same bodies is a different run too.
  const other = await packFor(names, { seed: 99 });
  assert.notEqual(parseManifest(manifestWith(names, other.pack)).hash, hPacked);

  // Re-spelling the same pack does not change identity: key order and a redundant field are not
  // execution, and an open job must survive a reformatted file.
  const respelled = JSON.parse(packed);
  respelled.imagePack = { files: { [names[0]]: { bytes: pack.files[names[0]].bytes, sha256: pack.files[names[0]].sha256, path: pack.files[names[0]].path } }, ref: pack.ref };
  assert.equal(parseManifest(JSON.stringify(respelled)).hash, hPacked);

  // The compatibility half: a pre-pack manifest carrying a NON-DEFAULT policy (dedupNames, as
  // push/53 does) must hash exactly as it did before packs existed, or its open jobs stop resuming.
  const dedup = JSON.parse(plain); dedup.dedupNames = true;
  const before = parseManifest(JSON.stringify(dedup));
  assert.deepEqual(Object.keys(before.policy).sort(), ["dedupNames", "imgSizes", "readBack", "skipPreflight"],
    "a manifest with no pack must not gain an imagePack key in its execution policy");
});

// ================================================================== 2. fetch, verify, cache

test("the happy path: bytes are fetched from the pinned commit, verified, cached and handed to the runner", async () => {
  const names = Object.keys(GODSTORM);
  const { pack, blobs } = await packFor(names);
  const { core } = headlessCore("{}", fakeRepo(blobs));
  const result = await prepareAndCommit(core, { pack, names });

  assert.equal(result.ok, true);
  assert.equal(result.ref, COMMIT);
  assert.equal(result.entries.length, 8);
  for (const e of result.entries) {
    assert.equal(e.state, "ready", e.error || "");
    assert.equal(e.source, "repo");
    assert.equal(e.digest, pack.files[e.name].sha256);
    assert.equal(e.size, GODSTORM[e.name]);
    const file = core.runner.files.get(e.name);
    assert.ok(file, `${e.name} must be loaded`);
    assert.equal(file.name, e.name, "the File carries the LOGICAL name, which is what @img resolves by");
    assert.equal(file.size, GODSTORM[e.name]);
    assert.equal(file.type, "image/webp");
    assert.equal(await hexOf(await file.arrayBuffer()), pack.files[e.name].sha256);
    const prov = core.runner.imgProvenance.get(e.name);
    assert.deepEqual({ ...prov, at: null, file: null }, {
      sha256: pack.files[e.name].sha256, path: pack.files[e.name].path, ref: COMMIT,
      bytes: GODSTORM[e.name], at: null, file: null,
    });
    assert.equal(prov.file, file, "provenance holds the EXACT verified File, which is what the gate binds");
  }
  assert.deepEqual(await core.assetCache.size(), { count: 8, bytes: Object.values(GODSTORM).reduce((a, b) => a + b, 0) });
  assert.equal(core.github.calls.length, 8, "one fetch per bound image, no more");
});

test("a second preparation is served from the content cache and issues no further request", async () => {
  const names = ["bg_godstorm_stormcourt_upper_court.webp", "ai_godstorm_marrow_umbral_reaver.webp"];
  const { pack, blobs } = await packFor(names);
  const { core } = headlessCore("{}", fakeRepo(blobs));
  await prepareAndCommit(core, { pack, names });
  assert.equal(core.github.calls.length, 2);

  const again = await prepareAndCommit(core, { pack, names });
  assert.equal(again.ok, true);
  assert.deepEqual(again.entries.map((e) => e.source), ["cache", "cache"]);
  assert.equal(core.github.calls.length, 2, "a cache hit must not go back to the repository");

  // ...and force goes back anyway, for an operator who wants the repository re-read.
  const forced = await prepareAndCommit(core, { pack, names, force: true });
  assert.deepEqual(forced.entries.map((e) => e.source), ["repo", "repo"]);
  assert.equal(core.github.calls.length, 4);
});

test("CACHE IDENTITY IS THE DIGEST: the same blob under a different name and path is one cached copy", async () => {
  // The property that makes the cache safe. A cache keyed by path, or by path@ref, or by logical
  // filename would answer a question nobody asked; keyed by digest, a hit IS the requested content.
  const a = "bg_godstorm_stormcourt_binding_dais_active.webp";
  const b = "bg_godstorm_stormcourt_binding_dais_released.webp";
  const bytes = bytesOf(GODSTORM[a], 7);
  const sha = await hexOf(bytes);
  const pack = { ref: COMMIT, files: {
    [a]: { path: `art/one/${a}`, sha256: sha, bytes: GODSTORM[a] },
    [b]: { path: `art/two/${b}`, sha256: sha, bytes: GODSTORM[a] },
  } };
  const blobs = new Map([[`${COMMIT}:art/one/${a}`, bytes], [`${COMMIT}:art/two/${b}`, bytes]]);
  const { core } = headlessCore("{}", fakeRepo(blobs));
  const result = await prepareAndCommit(core, { pack, names: [a, b] });
  assert.equal(result.ok, true);
  // packWork() sorts by logical name, so ...active is fetched and ...released hits its bytes.
  assert.deepEqual(result.entries.map((e) => [e.name, e.source]), [[a, "repo"], [b, "cache"]],
    "the second name is served from the first's cached bytes");
  assert.deepEqual(await core.assetCache.size(), { count: 1, bytes: GODSTORM[a] }, "one blob, one entry");
  assert.equal(core.github.calls.length, 1);
  // Both logical names are loaded, each with its OWN path recorded as provenance.
  assert.equal(core.runner.imgProvenance.get(a).path, `art/one/${a}`);
  assert.equal(core.runner.imgProvenance.get(b).path, `art/two/${b}`);
  assert.deepEqual(packGateProblems(pack, [a, b], core.runner), []);
});

test("a repository blob whose digest differs is REFUSED, named, not cached and not retried", async () => {
  const name = "ai_godstorm_marrow_nightveil_sentinel.webp";
  const { pack } = await packFor([name]);
  // same length, different content: only the digest can tell these apart
  const impostor = bytesOf(GODSTORM[name], 424242);
  const blobs = new Map([[`${COMMIT}:${pack.files[name].path}`, impostor]]);
  const { core } = headlessCore("{}", fakeRepo(blobs));
  const result = await prepareAndCommit(core, { pack, names: [name] });

  assert.equal(result.ok, false);
  const e = result.entries[0];
  assert.equal(e.state, "refused");
  assert.equal(e.digest, await hexOf(impostor));
  assert.match(e.error, /hashes to [0-9a-f]{64}; the pack says [0-9a-f]{64}/);
  assert.match(e.error, /Nothing was uploaded/);
  assert.equal(core.runner.files.has(name), false, "unverified bytes must never reach the runner");
  assert.equal(core.runner.imgProvenance.has(name), false);
  assert.deepEqual(await core.assetCache.size(), { count: 0, bytes: 0 }, "only verified bytes are cached");
  assert.equal(core.github.calls.length, 1, "a blob at an immutable commit does not change; do not retry it");
  assert.deepEqual(packGateProblems(pack, [name], core.runner).length, 1);
});

test("a size mismatch is refused before any digest is computed", async () => {
  const name = "ai_godstorm_marrow_hollow_lantern.webp";
  const { pack } = await packFor([name]);
  const truncated = bytesOf(GODSTORM[name] - 10, 1);
  const { core } = headlessCore("{}", fakeRepo(new Map([[`${COMMIT}:${pack.files[name].path}`, truncated]])));
  const e = (await prepareImagePack(ctxOf(core), { pack, names: [name] })).entries[0];
  assert.equal(e.state, "refused");
  assert.equal(e.digest, null, "there is no reason to hash a transfer that is the wrong length");
  assert.match(e.error, new RegExp(`is ${GODSTORM[name] - 10} bytes; the pack says ${GODSTORM[name]}`));
  assert.equal(core.runner.files.has(name), false);
});

test("a CORRUPT cache entry is dropped and refetched once; it is never trusted for matching its key", async () => {
  const name = "ai_godstorm_marrow_starless_monk.webp";
  const { pack, blobs } = await packFor([name]);
  const { core } = headlessCore("{}", fakeRepo(blobs));
  // Poison the store directly: right key, wrong bytes. Only re-verifying on read catches this.
  await core.assetCache.put({ sha256: pack.files[name].sha256, bytes: bytesOf(GODSTORM[name], 31337), path: "x", ref: COMMIT });
  const result = await prepareAndCommit(core, { pack, names: [name] });
  assert.equal(result.ok, true);
  assert.equal(result.entries[0].source, "repo", "the corrupt hit was dropped and the repository re-read");
  assert.equal(core.github.calls.length, 1);
  assert.equal(await hexOf(await core.runner.files.get(name).arrayBuffer()), pack.files[name].sha256);

  // and when the repository ALSO disagrees, the second failure is reported, not looped on
  const bad = new Map([[`${COMMIT}:${pack.files[name].path}`, bytesOf(GODSTORM[name], 5)]]);
  const c2 = headlessCore("{}", fakeRepo(bad)).core;
  await c2.assetCache.put({ sha256: pack.files[name].sha256, bytes: bytesOf(GODSTORM[name], 6), path: "x", ref: COMMIT });
  const r2 = await prepareAndCommit(c2, { pack, names: [name] });
  assert.equal(r2.entries[0].state, "refused");
  assert.equal(c2.github.calls.length, 1);
});

test("one unreachable blob is reported without abandoning the other seven", async () => {
  const names = Object.keys(GODSTORM);
  const { pack, blobs } = await packFor(names);
  const missing = "ai_godstorm_marrow_umbral_reaver.webp";
  blobs.delete(`${COMMIT}:${pack.files[missing].path}`);
  const { core } = headlessCore("{}", fakeRepo(blobs));
  const result = await prepareAndCommit(core, { pack, names });
  assert.equal(result.ok, false);
  const failed = result.entries.filter((e) => e.state !== "ready");
  assert.equal(failed.length, 1);
  assert.equal(failed[0].name, missing);
  assert.equal(failed[0].state, "error");
  assert.match(failed[0].error, /could not fetch art\/godstorm\/ai_godstorm_marrow_umbral_reaver\.webp at 28bba70d0e14: fetch .* HTTP 404/);
  assert.equal(core.runner.files.size, 7, "the other seven are prepared and usable");
});

test("with no digest available nothing is used, rather than used unverified", async () => {
  const name = "bg_godstorm_stormcourt_upper_court.webp";
  const { pack, blobs } = await packFor([name]);
  const { core } = headlessCore("{}", fakeRepo(blobs));
  const result = await prepareImagePack({ ...ctxOf(core), digest: null }, { pack, names: [name] });
  commitImagePack(core.runner, { pack, names: [name], staged: result.staged });
  assert.equal(result.entries[0].state, "error");
  assert.match(result.entries[0].error, /SHA-256 is not available/);
  assert.equal(core.runner.files.has(name), false);
  assert.equal(core.github.calls.length, 0, "there is no point fetching bytes that cannot be checked");
});

test("preparation CLEARS a bound name first, so a failure cannot leave a stale file satisfying the gate", async () => {
  const name = "bg_godstorm_stormcourt_binding_dais_active.webp";
  const { pack } = await packFor([name]);
  const { core } = headlessCore("{}", fakeRepo(new Map()));   // the blob is not there
  // whatever was loaded before - an earlier manifest, an earlier pack, a gallery pick
  core.runner.files.set(name, new File([bytesOf(GODSTORM[name], 2)], name, { type: "image/webp" }));
  core.runner.imgProvenance.set(name, { sha256: "0".repeat(64), path: "art/old.webp", ref: COMMIT, bytes: GODSTORM[name], file: core.runner.files.get(name) });

  const result = await prepareAndCommit(core, { pack, names: [name] });
  assert.equal(result.ok, false);
  assert.equal(core.runner.files.has(name), false, "the stale File must not survive a failed re-fetch");
  assert.equal(core.runner.imgProvenance.has(name), false);
  assert.equal(packGateProblems(pack, [name], core.runner).length, 1);
});

test("provenance is scoped to the OPEN manifest: a later selection cannot inherit an earlier pack's bytes", async () => {
  // The leak this closes. `@img` names are shared across manifests, and upload reuse for a bound
  // image is keyed by the digest recorded in imgProvenance. If selecting a manifest that does NOT
  // bind a name left the previous manifest's record in place, the runner would treat that name as
  // pack-backed and hand the new manifest the URL of the OLD picture.
  const name = "ai_godstorm_marrow_starless_monk.webp";
  const { pack, blobs } = await packFor([name]);
  const packedText = manifestWith([name], pack);
  const plainText = manifestWith([name], null);
  const github = fakeRepo(blobs, { manifestText: packedText });
  const { core } = headlessCore(packedText, github);

  await core.selectManifest({ name: "a.json", path: "push/a.json", number: 97, text: packedText });
  assert.equal(core.runner.imgProvenance.has(name), true);
  assert.equal(core.runner.files.has(name), true);

  // now open a manifest that references the same logical name but binds nothing
  await core.selectManifest({ name: "b.json", path: "push/b.json", number: 98, text: plainText });
  assert.equal(core.state.selected.pack, null);
  assert.equal(core.runner.imgProvenance.has(name), false, "the stale record must not survive");
  assert.equal(core.runner.files.has(name), false, "nor the File it vouched for; this one is now a manual pick");
});

test("two preparations do not race: the second is queued, not dropped", async () => {
  const names = ["bg_godstorm_stormcourt_upper_court.webp", "ai_godstorm_marrow_umbral_reaver.webp"];
  const { pack, blobs } = await packFor(names);
  const text = manifestWith(names, pack);
  const { core } = headlessCore(text, fakeRepo(blobs, { manifestText: text }));
  await core.selectManifest({ name: "x.json", path: "push/x.json", number: 99, text });
  assert.equal(core.github.calls.length, 2);

  const [a, b] = await Promise.all([core.prepareImages(true), core.prepareImages(true)]);
  assert.equal(a.ok, true, "the first forced re-fetch ran");
  assert.equal(b.ok, true, "and so did the second, rather than being silently skipped");
  assert.equal(core.github.calls.length, 6, "two forced passes over two images, serialized");
  assert.deepEqual(packGateProblems(pack, names, core.runner), []);
});

// ================================================================== 3. the Start gate

test("packGateProblems refuses provenance that no longer matches the pack", async () => {
  const name = "ai_godstorm_marrow_warden_of_the_first_dark.webp";
  const { pack, blobs } = await packFor([name]);
  const { core } = headlessCore("{}", fakeRepo(blobs));
  await prepareAndCommit(core, { pack, names: [name] });
  assert.deepEqual(packGateProblems(pack, [name], core.runner), []);

  // the manifest is re-selected under a pack naming DIFFERENT bytes; the loaded file is now wrong
  const other = await packFor([name], { seed: 555 });
  assert.match(packGateProblems(other.pack, [name], core.runner)[0], /was verified as [0-9a-f]{12} but the manifest now binds/);

  // a pack naming the same bytes at a different path/commit is also refused: provenance is the
  // path AND the commit, not only the digest
  const moved = { ref: "b".repeat(40), files: { [name]: { ...pack.files[name] } } };
  assert.match(packGateProblems(moved, [name], core.runner)[0],
    new RegExp(`was fetched from ${pack.files[name].path.replace(/\./g, "\\.")} at ${COMMIT.slice(0, 12)}, not .* at bbbbbbbbbbbb`));

  // and a File swapped out from under a still-valid provenance record. Identity is what catches it
  // now, so the refusal does not depend on the replacement being a different LENGTH.
  core.runner.files.set(name, new File([new Uint8Array(3)], name, { type: "image/webp" }));
  assert.match(packGateProblems(pack, [name], core.runner)[0], /is no longer holding the exact file that was verified/);
});

test("NO BYPASS: a manifest whose pack cannot be verified opens no job and sends nothing", async () => {
  const names = ["bg_godstorm_stormcourt_upper_court.webp", "ai_godstorm_marrow_starless_monk.webp"];
  const { pack, blobs } = await packFor(names);
  blobs.set(`${COMMIT}:${pack.files[names[1]].path}`, bytesOf(GODSTORM[names[1]], 999)); // right size, wrong file
  const text = manifestWith(names, pack);
  const { core, notes } = headlessCore(text, fakeRepo(blobs, { manifestText: text }));
  const game = core.client.game ?? null;

  await core.selectManifest({ name: "x.json", path: "push/x.json", number: 90, text });
  assert.deepEqual(core.state.selected.problems, []);
  assert.equal(core.state.selected.packResult.ok, false, "selection already knows");

  await core.startJob();
  assert.equal(core.state.jobId, null, "no job was opened");
  assert.deepEqual(core.journal.listJobs(), []);
  const said = notes.filter((n) => n.type === "message").map((n) => n.text).join(" | ");
  assert.match(said, /could not be verified|are not verified/);
  assert.match(said, /Nothing was sent|Nothing was uploaded/);
  if (game) assert.deepEqual(game.calls, [], "not one request left for the game");
});

test("NO BYPASS: a manual pick cannot stand in for a bound image, even with the right byte count", async () => {
  // The attack this closes: the byte ledger is satisfiable by any file of the right length, so
  // without a provenance gate an operator (or a bug) could pick a same-sized file for a bound name
  // and Start would go green on L17 alone.
  const name = "ai_godstorm_marrow_umbral_reaver.webp";
  const { pack } = await packFor([name]);
  const text = manifestWith([name], pack);
  const { core } = headlessCore(text, fakeRepo(new Map(), { manifestText: text })); // blob unreachable
  await core.selectManifest({ name: "x.json", path: "push/x.json", number: 91, text });

  // a device file of EXACTLY the ledgered length, named exactly right
  core.runner.files.set(name, new File([bytesOf(GODSTORM[name], 77)], name, { type: "image/webp" }));
  const { imagePicks, unusablePicks } = await import("../src/core/facts.mjs");
  assert.deepEqual(unusablePicks(imagePicks([name], core.runner.files, { [name]: GODSTORM[name] })), [],
    "the byte ledger alone is satisfied, which is exactly why it is not the only gate");

  await core.startJob();
  assert.equal(core.state.jobId, null, "the pack gate refuses what the ledger accepted");
  assert.match(packGateProblems(pack, [name], core.runner)[0], /has not been fetched and verified/);
});

test("the byte ledger still gates an UNBOUND image alongside the pack", async () => {
  const bound = "bg_godstorm_stormcourt_upper_court.webp";
  const picked = "ai_godstorm_marrow_starless_monk.webp";
  const { pack, blobs } = await packFor([bound]);
  const text = manifestWith([bound, picked], pack);
  const { core, notes } = headlessCore(text, fakeRepo(blobs, { manifestText: text }));
  await core.selectManifest({ name: "x.json", path: "push/x.json", number: 92, text });
  assert.equal(core.state.selected.packResult.ok, true);
  // the unbound one is picked, and it is the wrong file
  core.runner.files.set(picked, { name: "1000014259.png", size: 1709179, type: "image/png" });
  await core.startJob();
  assert.equal(core.state.jobId, null);
  assert.match(notes.filter((n) => n.type === "message").map((n) => n.text).join(" "), /do not match the manifest/);
});

// ------------------------------------------------------------------ F1: same-size swap

test("F1: a SAME-SIZE swap after verification is refused by the Start gate, and nothing is uploaded", async () => {
  // The case the feature exists for, and the one the first implementation let through: provenance
  // metadata still matched and the length still matched, so the gate passed and _resolved uploaded
  // the replacement - then recorded that upload under the CORRECT digest, poisoning the
  // content-keyed ledger for every later job that legitimately wants those bytes.
  const name = "ai_godstorm_marrow_starless_monk.webp";
  const { pack, blobs } = await packFor([name]);
  const text = manifestWith([name], pack);
  const { core, storage, notes } = headlessCore(text, fakeRepo(blobs, { manifestText: text }));
  const up = recordingUploader();
  core.runner.uploader = up;
  await core.selectManifest({ name: "x.json", path: "push/x.json", number: 120, text });
  assert.deepEqual(packGateProblems(pack, [name], core.runner), []);
  const verified = core.runner.files.get(name);

  // Different bytes. EXACTLY the expected length. Same MIME. Same filename.
  const impostor = new File([bytesOf(GODSTORM[name], 8675309)], name, { type: "image/webp" });
  assert.equal(impostor.size, GODSTORM[name], "the swap must be the same length or it proves nothing");
  assert.notEqual(await hexOf(await impostor.arrayBuffer()), pack.files[name].sha256);
  core.runner.files.set(name, impostor);

  // every SIZE-based check still passes, which is the whole point
  const { imagePicks, unusablePicks } = await import("../src/core/facts.mjs");
  assert.deepEqual(unusablePicks(imagePicks([name], core.runner.files, { [name]: GODSTORM[name] })), []);
  // ...and the pack gate does not
  assert.match(packGateProblems(pack, [name], core.runner)[0], /is no longer holding the exact file that was verified/);

  await core.startJob();
  assert.equal(core.state.jobId, null, "no job was opened");
  assert.deepEqual(core.journal.listJobs(), []);
  assert.equal(up.uploads.length, 0, "the replacement must not be uploaded");
  assert.equal(storage.getItem(ASSET_UPLOADS_KEY), null, "and the content ledger must be untouched");
  assert.match(notes.filter((n) => n.type === "message").map((n) => n.text).join(" "), /are not verified/);

  // the ORIGINAL verified File still starts cleanly: this is a refusal, not a wedge
  core.runner.files.set(name, verified);
  assert.deepEqual(packGateProblems(pack, [name], core.runner), []);
  await core.startJob();
  assert.ok(core.state.jobId, "the verified file still opens a job");
  assert.equal(up.uploads.length, 1);
  assert.equal(up.uploads[0].digest, pack.files[name].sha256);
  assert.deepEqual(Object.keys(readAssetUploads(storage)), [pack.files[name].sha256]);
});

test("F1: the runner refuses a same-size swap even when no preflight runs", async () => {
  // _preflight is CREATE-only (runner.mjs: `item.op === "create" && item.state === "PLANNED"`), so
  // for an EDIT - which is what push/53's five Marrow avatars are - _resolved is the only barrier the
  // bytes pass. It is therefore tested directly, at the boundary where the upload actually happens.
  const name = "ai_godstorm_marrow_umbral_reaver.webp";
  const { pack, blobs } = await packFor([name]);
  const text = manifestWith([name], pack);
  const { core, storage } = headlessCore(text, fakeRepo(blobs, { manifestText: text }));
  const up = recordingUploader();
  core.runner.uploader = up;
  await core.selectManifest({ name: "x.json", path: "push/x.json", number: 121, text });
  const prov = core.runner.imgProvenance.get(name);

  // (a) identity: a same-size impostor under a still-valid record
  core.runner.files.set(name, new File([bytesOf(GODSTORM[name], 31)], name, { type: "image/webp" }));
  await assert.rejects(() => core.runner._resolved({ avatar: `@img:${name}` }, null),
    /is not holding the exact file that was verified/);
  assert.equal(up.uploads.length, 0);
  assert.equal(storage.getItem(ASSET_UPLOADS_KEY), null);

  // (b) digest: a record whose own file is not the bytes it claims. Identity alone would accept
  //     this; the re-hash at the upload boundary is what refuses it.
  const wrong = new File([bytesOf(GODSTORM[name], 32)], name, { type: "image/webp" });
  core.runner.files.set(name, wrong);
  core.runner.imgProvenance.set(name, { ...prov, file: wrong });
  await assert.rejects(() => core.runner._resolved({ avatar: `@img:${name}` }, null),
    /hashes to [0-9a-f]{64} at the moment of upload; the pack says [0-9a-f]{64}\. Nothing was uploaded\./);
  assert.equal(up.uploads.length, 0);
  assert.equal(storage.getItem(ASSET_UPLOADS_KEY), null, "nothing may be recorded under a digest that was not uploaded");

  // (c) no digest wired at all: fail closed rather than upload unverified bytes
  core.runner.digest = null;
  await assert.rejects(() => core.runner._resolved({ avatar: `@img:${name}` }, null),
    /no digest is wired, so its bytes cannot be re-verified; nothing was uploaded/);
  assert.equal(up.uploads.length, 0);
});

// ------------------------------------------------------------------ F2: the selection race

test("F2: preparation alone writes nothing; only the commit installs", async () => {
  const name = "bg_godstorm_stormcourt_upper_court.webp";
  const { pack, blobs } = await packFor([name]);
  const { core } = headlessCore("{}", fakeRepo(blobs));
  const result = await prepareImagePack(ctxOf(core), { pack, names: [name] });
  assert.equal(result.ok, true);
  assert.equal(result.staged.length, 1);
  assert.equal(core.runner.files.size, 0, "a preparation must not touch the runner");
  assert.equal(core.runner.imgProvenance.size, 0);

  commitImagePack(core.runner, { pack, names: [name], staged: result.staged });
  assert.equal(core.runner.files.get(name), result.staged[0].file);
  assert.deepEqual(packGateProblems(pack, [name], core.runner), []);
});

test("F2: a fetch still in flight when the selection changes installs NOTHING into the new manifest", async () => {
  // The reviewer's repro. Manifest A binds shared.webp; manifest B references the same logical name
  // but leaves it to the manual picker. Hold A's repository fetch open, select B, then release A.
  const shared = "ai_godstorm_marrow_starless_monk.webp";
  const { pack, blobs } = await packFor([shared]);
  const aText = manifestWith([shared], pack);
  const bText = manifestWith([shared], null);

  let release;
  const held = new Promise((r) => { release = r; });
  const github = fakeRepo(blobs, { manifestText: aText });
  const rawReal = github.raw;
  github.raw = async (path, ref) => { await held; return rawReal(path, ref); };

  const { core, storage } = headlessCore(aText, github);
  const aPending = core.selectManifest({ name: "a.json", path: "push/a.json", number: 122, text: aText });
  await Promise.resolve();                      // A's fetch is now awaiting `held`
  assert.equal(core.runner.files.size, 0, "nothing is installed while the fetch is outstanding");

  await core.selectManifest({ name: "b.json", path: "push/b.json", number: 123, text: bText });
  assert.equal(core.state.selected.pack, null);

  release();                                    // A's fetch completes, far too late
  await aPending;
  await core._packChain;

  assert.equal(core.runner.imgProvenance.has(shared), false, "A's provenance must never appear under B");
  assert.equal(core.runner.files.has(shared), false, "nor A's File, which B left to the manual picker");
  assert.equal(core.state.selected.packResult, null, "and B's own state is untouched");

  // Start stays blocked until the operator supplies B's file, and then runs on THAT file
  const up = recordingUploader();
  core.runner.uploader = up;
  await core.startJob();
  assert.equal(core.state.jobId, null, "Start is blocked: B's image is simply not picked");
  const manual = new File([bytesOf(GODSTORM[shared], 4242)], shared, { type: "image/webp" });
  core.runner.files.set(shared, manual);
  await core.startJob();
  assert.ok(core.state.jobId);
  assert.equal(up.uploads.length, 1);
  assert.equal(up.uploads[0].digest, await hexOf(await manual.arrayBuffer()), "B uploaded B's file, not A's");
  assert.equal(storage.getItem(ASSET_UPLOADS_KEY), null, "an unbound image writes nothing to the content ledger");
});

test("F2: with OVERLAPPING packs the current selection always wins", async () => {
  // Same race, but B binds the shared name too - to different bytes. A's late pass must not install
  // its own File under a name B has bound, and B's own preparation must be what ends up loaded.
  const shared = "ai_godstorm_marrow_hollow_lantern.webp";
  const a = await packFor([shared], { dir: "art/a", seed: 11 });
  const b = await packFor([shared], { dir: "art/b", seed: 22 });
  assert.notEqual(a.pack.files[shared].sha256, b.pack.files[shared].sha256);
  const aText = manifestWith([shared], a.pack);
  const bText = manifestWith([shared], b.pack);

  const blobs = new Map([...a.blobs, ...b.blobs]);
  let release;
  const held = new Promise((r) => { release = r; });
  const github = fakeRepo(blobs, { manifestText: aText });
  const rawReal = github.raw;
  let first = true;
  github.raw = async (path, ref) => { if (first) { first = false; await held; } return rawReal(path, ref); };

  const { core } = headlessCore(aText, github);
  const aPending = core.selectManifest({ name: "a.json", path: "push/a.json", number: 124, text: aText });
  await Promise.resolve();
  const bPending = core.selectManifest({ name: "b.json", path: "push/b.json", number: 125, text: bText });
  release();
  await Promise.all([aPending, bPending]);
  await core._packChain;

  const prov = core.runner.imgProvenance.get(shared);
  assert.ok(prov, "B's own preparation installed");
  assert.equal(prov.sha256, b.pack.files[shared].sha256, "the bytes loaded are B's, not A's");
  assert.equal(prov.path, `art/b/${shared}`);
  assert.deepEqual(packGateProblems(b.pack, [shared], core.runner), []);
  assert.equal(packGateProblems(a.pack, [shared], core.runner).length, 1, "and they would not satisfy A");
});

// ================================================================== 4. upload identity

test("a pack-backed upload is recorded by CONTENT, and a re-run reuses it without uploading again", async () => {
  const names = ["bg_godstorm_stormcourt_upper_court.webp"];
  const { pack, blobs } = await packFor(names);
  const text = manifestWith(names, pack);
  const { core, storage } = headlessCore(text, fakeRepo(blobs, { manifestText: text }));
  const up = recordingUploader();
  core.runner.uploader = up;
  await core.selectManifest({ name: "x.json", path: "push/x.json", number: 93, text });
  await core.startJob();

  const job = core.journal.get(core.state.jobId);
  assert.equal(job.items.length, 1);
  assert.equal(up.uploads.length, 1);
  assert.equal(up.uploads[0].digest, pack.files[names[0]].sha256, "the bytes that went out are the bytes the pack named");
  assert.equal(up.uploads[0].name, names[0]);
  const bound = pack.files[names[0]];
  const ledger = readAssetUploads(storage);
  assert.deepEqual(Object.keys(ledger), [bound.sha256], "the content ledger is keyed by the digest, not the filename");
  assert.equal(ledger[bound.sha256].url, `https://utfs.io/f/${bound.sha256.slice(0, 16)}`);
  assert.equal(ledger[bound.sha256].path, bound.path);
  assert.equal(ledger[bound.sha256].ref, COMMIT);
  assert.equal(readIdmap(storage)[names[0]], ledger[bound.sha256].url, "resolveRefs still substitutes through the idmap");

  // a second job over the same pack: same content, so the recorded upload is reused
  await core.selectManifest({ name: "x2.json", path: "push/x2.json", number: 94, text });
  await core.startJob();
  assert.equal(up.uploads.length, 1, "the same bytes must not be uploaded twice");
});

test("A STALE NAME-KEYED IDMAP ENTRY CANNOT STAND IN FOR BOUND BYTES", async () => {
  // tnr_bk_idmap_v1 maps a FILENAME to an uploaded URL and is shared with the old builder. Two
  // different files have carried the same logical name across manifests, so for a pack-backed image
  // that map is not evidence: reusing its URL would ship the previous picture behind this
  // manifest's provenance, silently and with a green row. Content identity decides instead.
  const name = "ai_godstorm_marrow_starless_monk.webp";
  const { pack, blobs } = await packFor([name]);
  const text = manifestWith([name], pack);
  const { core, storage } = headlessCore(text, fakeRepo(blobs, { manifestText: text }));
  writeIdmap(storage, { [name]: "https://utfs.io/f/THE-OLD-WRONG-IMAGE" });
  const up = recordingUploader();
  core.runner.uploader = up;

  await core.selectManifest({ name: "x.json", path: "push/x.json", number: 95, text });
  await core.startJob();

  assert.equal(up.uploads.length, 1, "the bound bytes were uploaded rather than the stale URL reused");
  assert.equal(up.uploads[0].digest, pack.files[name].sha256);
  assert.notEqual(readIdmap(storage)[name], "https://utfs.io/f/THE-OLD-WRONG-IMAGE");
  const job = core.journal.get(core.state.jobId);
  assert.equal(job.items[0].state, "VERIFIED", JSON.stringify(job.items[0].error ?? ""));
});

test("an UNBOUND image keeps the historical idmap-by-name reuse exactly as it was", async () => {
  // Unchanged behaviour, stated as a test so the pack path cannot quietly take it over: for an image
  // the pack does not bind, an existing idmap entry under the filename still skips the upload. That
  // is the reuse the builder and Forge have always shared, and a picked image has no digest to key
  // anything else by. (The ledger gate still requires a File before Start, which is why one is set.)
  const name = "ai_godstorm_marrow_hollow_lantern.webp";
  const text = manifestWith([name], null);
  const { core, storage } = headlessCore(text, fakeRepo(new Map(), { manifestText: text }));
  writeIdmap(storage, { [name]: "https://utfs.io/f/ALREADY-UPLOADED" });
  const up = recordingUploader();
  core.runner.uploader = up;
  await core.selectManifest({ name: "x.json", path: "push/x.json", number: 96, text });
  core.runner.files.set(name, new File([bytesOf(GODSTORM[name], 4)], name, { type: "image/webp" }));
  await core.startJob();
  assert.equal(up.uploads.length, 0, "the name-keyed idmap still short-circuits an unbound image");
  const job = core.journal.get(core.state.jobId);
  assert.equal(job.items[0].state, "VERIFIED", JSON.stringify(job.items[0].error ?? ""));
  assert.equal(readIdmap(storage)[name], "https://utfs.io/f/ALREADY-UPLOADED");
  assert.equal(storage.getItem(ASSET_UPLOADS_KEY), null, "an unbound image writes nothing to the content ledger");
});

// ================================================================== 5. the production fixture

test("push/53: the eight Godstorm images bind to one commit, verify, and clear the Start gate", async () => {
  // The real manifest text when it is in the tree, with a pack spliced in over its OWN imgSizes.
  // This is the shape the first production pack has to satisfy: three Stormcourt backgrounds and
  // five Marrow avatars, the eight files whose manual selection cost nine live writes.
  if (!existsSync(REPAIR_53)) return; // the fixture is prepared on the planning branch
  const raw = JSON.parse(readFileSync(REPAIR_53, "utf8"));
  assert.deepEqual(Object.keys(raw.imgSizes).sort(), Object.keys(GODSTORM).sort(),
    "push/53's ledger has moved; re-derive this fixture rather than editing the expectation");
  const names = Object.keys(raw.imgSizes);
  const { pack, blobs } = await packFor(names, { sizes: raw.imgSizes });
  raw.imagePack = pack;
  const text = JSON.stringify(raw);

  const { core } = headlessCore(text, fakeRepo(blobs, { manifestText: text }));
  await core.selectManifest({ name: "53_godstorm_failed_items_repair.json", path: "push/53_godstorm_failed_items_repair.json", number: 53, text });
  const s = core.state.selected;
  assert.deepEqual(s.problems, [], "the packed manifest must still parse and validate clean");
  assert.equal(s.images.length, 8);
  assert.equal(s.packResult.ok, true, JSON.stringify((s.packResult.entries || []).filter((e) => e.state !== "ready")));
  assert.deepEqual(s.packResult.unbound, [], "every image of the repair is bound");
  assert.deepEqual(packGateProblems(s.pack, s.images, core.runner), []);
  // and the ledger gate agrees with the pack, because rule 4 made them agree at parse time
  const { imagePicks, unusablePicks } = await import("../src/core/facts.mjs");
  assert.deepEqual(unusablePicks(imagePicks(s.images, core.runner.files, s.manifest.imgSizes)), []);
  // three backgrounds and five avatars, named, so a reshaped fixture fails here
  assert.equal(s.images.filter((n) => n.startsWith("bg_")).length, 3);
  assert.equal(s.images.filter((n) => n.startsWith("ai_")).length, 5);
});

test("push/53 END TO END: its committed pack verifies 8/8 from the repository and clears the Start gate", async () => {
  // Not a synthetic pack over the real ledger this time - the REAL committed pack, with the bytes
  // fetched out of git at the commit the pack names. This is the closest a socket-free test gets to
  // what the operator will see when they open the repair in Forge.
  if (!existsSync(REPAIR_53)) return;
  const m = parseManifest(readFileSync(REPAIR_53, "utf8"));
  if (!m.imagePack) return; // the pack is staged separately from the Forge feature
  assert.equal(Object.keys(m.imgSizes).length, 8);
  assert.equal(Object.keys(m.imagePack.files).length, 8);

  const { execFileSync } = await import("node:child_process");
  const repo = join(HERE, "..", "..");
  const git = { raw: async (path, ref) => {
    const buf = execFileSync("git", ["-C", repo, "cat-file", "blob", `${ref}:${path}`],
      { encoding: "buffer", maxBuffer: 64 * 1024 * 1024, stdio: ["ignore", "pipe", "ignore"] });
    return buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
  } };

  const { core } = headlessCore("{}", git);
  const names = Object.keys(m.imagePack.files);
  const result = await prepareAndCommit(core, { pack: m.imagePack, names });
  const bad = result.entries.filter((e) => e.state !== "ready");
  assert.deepEqual(bad.map((e) => `${e.name}: ${e.error}`), [], "every bound image must verify from the repository");
  assert.equal(result.ok, true);
  assert.deepEqual(result.unbound, [], "the repair leaves no image to the manual picker");

  // both gates, together, exactly as startJob() reads them
  assert.deepEqual(packGateProblems(m.imagePack, names, core.runner), []);
  const { imagePicks, unusablePicks } = await import("../src/core/facts.mjs");
  assert.deepEqual(unusablePicks(imagePicks(names, core.runner.files, m.imgSizes)), []);

  // three backgrounds and five avatars, and each File carries the logical name @img resolves by
  assert.equal(names.filter((n) => n.startsWith("bg_")).length, 3);
  assert.equal(names.filter((n) => n.startsWith("ai_")).length, 5);
  for (const n of names) {
    const file = core.runner.files.get(n);
    assert.equal(file.name, n);
    assert.equal(await hexOf(await file.arrayBuffer()), m.imagePack.files[n].sha256);
  }
});
