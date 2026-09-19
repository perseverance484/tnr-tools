// Preparing a repo-backed image pack: fetch, verify, and hand back the exact bytes the manifest
// named. Talks to the GitHub client and the asset cache; never to the DOM, and — since the
// independent review of fbb4fb49 (F2) — never to the runner either.
//
// TWO PHASES, AND THE SPLIT IS THE SAFETY PROPERTY.
//
//   prepareImagePack()  fetches and verifies. It performs NO write to runner.files or
//                       runner.imgProvenance. Every verified image is returned as `staged` data.
//   commitImagePack()   installs staged data into the runner, synchronously, with no await inside
//                       it, so the clear-then-set is atomic with respect to anything else running.
//
// It used to be one phase, writing each image into the runner as it was verified. That is a
// selection race, and review F2 named it precisely: hold manifest A's repository fetch, select
// manifest B, then release A. A's writes land AFTER B's scope cleanup has already run, so a name B
// leaves to the manual picker inherits A's File and A's provenance — and because upload reuse for a
// provenanced image is keyed by content, the runner would then hand B the URL of A's picture. The
// caller's "is this still the selected manifest?" check came after the mutation, so it could only
// discard the RESULT, never the side effects. Now there are no side effects to discard: a stale pass
// simply never reaches its commit.
//
// WITHIN a fetch, the order still matters and is still written out:
//
//   1. cache, keyed by digest. A hit is the exact content the manifest asked for, because that is
//      what the key means (storage/assets.mjs).
//   2. verify, ALWAYS - cache hit and fresh fetch alike. Size first (cheap, and it catches a
//      truncated transfer), then SHA-256. A cached entry that fails its own key is corrupt: it is
//      deleted and refetched once, and a second failure is reported, never retried in a loop.
//   3. stage. Only a verified image becomes a File, and the File is carried in the staged record
//      together with the provenance that vouches for it, so the two can never be installed apart.
//
// Every failure is a REPORTED state, not a thrown error. One unreachable blob must not abort the
// preparation of the other seven, because the operator needs the whole picture before they decide
// what to do - and the gate in ForgeCore.startJob() refuses the job regardless of what this returns.

import { mimeOf, packWork, toHex, unboundNames } from "../runner/imgpack.mjs";

/** `File` when the host has one (browsers, node >= 20); a minimal stand-in otherwise. */
function makeFile(bytes, name, type) {
  const F = globalThis.File;
  if (typeof F === "function") return new F([bytes], name, { type });
  const B = globalThis.Blob;
  if (typeof B === "function") {
    const blob = new B([bytes], { type });
    // name/lastModified are what the uploader and the pick contract read off a File.
    return Object.defineProperties(blob, { name: { value: name }, lastModified: { value: 0 } });
  }
  throw new Error("this host has neither File nor Blob; repo-backed image packs need one to upload");
}

/**
 * Fetch and verify every bound image a manifest needs. Writes nothing.
 *
 * @param {object} ctx                 {github, assetCache, digest, now}
 * @param {object} o
 * @param {{ref: string, files: object}|null} o.pack   normalized pack from parseManifest
 * @param {string[]} o.names           the logical `@img` names the plan references
 * @param {boolean} [o.force]          ignore the cache and refetch from the repository
 * @returns {Promise<{ref, entries, unbound, ok, staged}>}
 *   entries: {name, path, ref, sha256, bytes, state, source, size, digest, error} - reportable, JSON
 *   staged:  [{name, file, prov}] - the verified images, for commitImagePack()
 */
export async function prepareImagePack({ github, assetCache, digest, now = () => Date.now() }, { pack, names = [], force = false } = {}) {
  const work = packWork(pack, names);
  const unbound = unboundNames(pack, names);
  const entries = [];
  const staged = [];
  for (const want of work) {
    const { entry, stage } = await one({ github, assetCache, digest, now }, want, force);
    entries.push(entry);
    if (stage) staged.push(stage);
  }
  return { ref: pack ? pack.ref : null, entries, unbound, ok: entries.length === staged.length, staged };
}

/**
 * Install a completed preparation. Synchronous and atomic: every bound name is cleared and every
 * verified name is set inside one turn, with no await in between, so no other pass can observe or
 * interleave with a half-installed pack.
 *
 * Clearing FIRST is what makes a failed image fail closed. A bound name whose bytes did not verify
 * is absent from `staged`, so it ends this call deleted - it cannot be left holding a file from an
 * earlier preparation, an earlier manifest, or the manual picker, and it therefore reads as
 * "missing" to both the byte-ledger gate and the pack gate.
 *
 * The verified File is stored ON the provenance record, not merely alongside it. Review F1: the gate
 * used to compare the provenance's digest and the current File's SIZE, which means a different file
 * of identical length swapped into runner.files after verification passed every check and was
 * uploaded - and then recorded in the content-keyed upload ledger under the CORRECT digest, so every
 * later job for those bytes would reuse the wrong URL. A File/Blob is immutable, so holding the
 * exact object is a complete answer to "are these still the bytes that were hashed".
 */
export function commitImagePack(runner, { pack, names = [], staged = [] } = {}) {
  for (const { name } of packWork(pack, names)) {
    runner.files.delete(name);
    runner.imgProvenance.delete(name);
  }
  for (const { name, file, prov } of staged) {
    runner.files.set(name, file);
    runner.imgProvenance.set(name, { ...prov, file });
  }
  return staged.length;
}

async function one(ctx, want, force) {
  const { github, assetCache, digest, now } = ctx;
  const base = { name: want.name, path: want.path, ref: want.ref, sha256: want.sha256, bytes: want.bytes };
  const fail = (o) => ({ entry: { ...base, source: null, size: null, digest: null, ...o }, stage: null });
  if (typeof digest !== "function") {
    return fail({ state: "error", error: "SHA-256 is not available in this context, so repo-backed bytes cannot be verified; Forge will not use them unverified" });
  }

  let cached = null;
  if (!force) {
    // A cache that cannot even be opened must not stop a preparation: go to the repository.
    try { cached = await assetCache.get(want.sha256); } catch { cached = null; }
  }

  // At most two attempts, and the second only ever happens because the FIRST came from the cache
  // and failed its own digest. A repository fetch that fails verification is not retried: the blob
  // at an immutable commit does not change between two requests, so a retry could only launder it.
  let source = cached ? "cache" : "repo";
  let bytes;
  for (let attempt = 0; attempt < 2; attempt++) {
    if (source === "cache") {
      bytes = cached.bytes;
    } else {
      try {
        bytes = await github.raw(want.path, want.ref);
      } catch (e) {
        return fail({ state: "error", source: "repo", error: `could not fetch ${want.path} at ${want.ref.slice(0, 12)}: ${(e && e.message) || e}` });
      }
    }
    const size = bytes.byteLength ?? bytes.length ?? 0;
    let hex = null;
    if (size === want.bytes) {
      try { hex = toHex(await digest(bytes)); }
      catch (e) {
        return fail({ state: "error", source, size, error: `could not compute SHA-256 for ${want.name}: ${(e && e.message) || e}` });
      }
    }
    if (size === want.bytes && hex === want.sha256) {
      if (source === "repo") {
        // Cache only verified bytes. A failure to cache is not a failure to verify: the image is
        // usable this run, and the next run fetches it again.
        try { await assetCache.put({ sha256: want.sha256, bytes, path: want.path, ref: want.ref }); }
        catch { /* the cache is an optimization; the digest is the contract */ }
      }
      let file;
      try { file = makeFile(bytes, want.name, mimeOf(want.name)); }
      catch (e) {
        // Reported like any other per-image failure: one host quirk must not abandon the rest.
        return fail({ state: "error", source, size, digest: hex, error: (e && e.message) || String(e) });
      }
      return {
        entry: { ...base, state: "ready", source, size, digest: hex, error: null },
        stage: { name: want.name, file, prov: { sha256: want.sha256, path: want.path, ref: want.ref, bytes: want.bytes, at: now() } },
      };
    }

    const why = size !== want.bytes
      ? `is ${size} bytes; the pack says ${want.bytes}`
      : `hashes to ${hex}; the pack says ${want.sha256}`;
    if (source === "cache") {
      // A content-addressed entry that does not match its own key is corrupt, not wrong. Drop it
      // and go to the repository once.
      try { await assetCache.delete(want.sha256); } catch { /* best effort */ }
      cached = null;
      source = "repo";
      continue;
    }
    return fail({ state: "refused", source, size, digest: hex,
      error: `${want.path} at ${want.ref.slice(0, 12)} ${why}. Nothing was uploaded and this image cannot be used; the manifest and the repository disagree about which file this is.` });
  }
  /* c8 ignore next */
  return fail({ state: "error", source, error: "verification did not settle" });
}

/**
 * Has every bound image been prepared and verified, right now? Read at the moment Start is tapped,
 * from the runner's own state rather than from whatever the preparation reported earlier, so a
 * stale report cannot open a job. Pure apart from reading the two maps it is handed.
 *
 * The File-IDENTITY check is the one review F1 required. Metadata plus a byte count is the exact
 * trust boundary this whole feature exists to leave behind: any file of the right length satisfies
 * it, which is how a 1.7 MB master rode into a live run in the first place. The object that was
 * hashed is the only thing that proves the bytes were hashed.
 *
 * @returns {string[]} one sentence per problem; empty means every bound image is the pack's.
 */
export function packGateProblems(pack, names, runner) {
  const problems = [];
  for (const want of packWork(pack, names)) {
    const prov = runner.imgProvenance.get(want.name) ?? null;
    const file = runner.files.get(want.name) ?? null;
    if (!prov || !file) {
      problems.push(`${want.name} is bound to ${want.path} at ${want.ref.slice(0, 12)} but has not been fetched and verified`);
      continue;
    }
    if (prov.sha256 !== want.sha256) {
      problems.push(`${want.name} was verified as ${prov.sha256.slice(0, 12)} but the manifest now binds ${want.sha256.slice(0, 12)}`);
      continue;
    }
    if (prov.ref !== want.ref || prov.path !== want.path) {
      problems.push(`${want.name} was fetched from ${prov.path} at ${prov.ref.slice(0, 12)}, not ${want.path} at ${want.ref.slice(0, 12)}`);
      continue;
    }
    if (!prov.file || file !== prov.file) {
      problems.push(`${want.name} is no longer holding the exact file that was verified against ${want.sha256.slice(0, 12)}; re-fetch it from the repository`);
      continue;
    }
    const size = Number(file.size);
    if (size !== want.bytes) {
      problems.push(`${want.name} is holding ${size} bytes, not the ${want.bytes} the pack names`);
    }
  }
  return problems;
}
