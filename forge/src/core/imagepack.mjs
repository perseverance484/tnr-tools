// Preparing a repo-backed image pack: fetch, verify, cache, and hand the runner the exact bytes the
// manifest named. Talks to the GitHub client, the asset cache and the runner; never to the DOM.
//
// THE ORDER OF OPERATIONS IS THE SAFETY PROPERTY, so it is written out rather than implied:
//
//   1. clear. Before anything is fetched, whatever the runner is currently holding for a BOUND
//      logical name is removed. A bound name is the pack's, so a file left over from an earlier
//      preparation, an earlier manifest, or the manual picker must not be able to survive a failed
//      re-fetch and satisfy the Start gate with unverified provenance. Nothing about this feature
//      would be worth shipping if a stale File could outlive the binding that replaced it.
//   2. cache, keyed by digest. A hit is the exact content the manifest asked for, because that is
//      what the key means (storage/assets.mjs).
//   3. verify, ALWAYS - cache hit and fresh fetch alike. Size first (cheap, and it catches a
//      truncated transfer), then SHA-256. A cached entry that fails its own key is corrupt: it is
//      deleted and refetched once, and a second failure is reported, never retried in a loop.
//   4. only then does the File reach runner.files, together with the provenance the Start gate and
//      the run report read back. No verification, no File: the image reads as "missing" downstream,
//      which is exactly what blocks Start.
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
 * Prepare every bound image a manifest needs.
 *
 * @param {object} ctx                 {github, assetCache, digest, runner, now}
 * @param {object} o
 * @param {{ref: string, files: object}|null} o.pack   normalized pack from parseManifest
 * @param {string[]} o.names           the logical `@img` names the plan references
 * @param {boolean} [o.force]          ignore the cache and refetch from the repository
 * @returns {Promise<{ref: string|null, entries: Array, unbound: string[], ok: boolean}>}
 *   entries: {name, path, ref, sha256, bytes, state, source, size, digest, error}
 *   state:   "ready" | "refused" | "error"
 */
export async function prepareImagePack({ github, assetCache, digest, runner, now = () => Date.now() }, { pack, names = [], force = false } = {}) {
  const work = packWork(pack, names);
  const unbound = unboundNames(pack, names);
  // Step 1, for every bound name, before a single request.
  for (const { name } of work) {
    runner.files.delete(name);
    runner.imgProvenance.delete(name);
  }
  const entries = [];
  for (const want of work) entries.push(await one({ github, assetCache, digest, runner, now }, want, force));
  return { ref: pack ? pack.ref : null, entries, unbound, ok: entries.every((e) => e.state === "ready") };
}

async function one(ctx, want, force) {
  const { github, assetCache, digest, runner, now } = ctx;
  const base = { name: want.name, path: want.path, ref: want.ref, sha256: want.sha256, bytes: want.bytes };
  if (typeof digest !== "function") {
    return { ...base, state: "error", source: null, size: null, digest: null,
      error: "SHA-256 is not available in this context, so repo-backed bytes cannot be verified; Forge will not use them unverified" };
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
        return { ...base, state: "error", source: "repo", size: null, digest: null,
          error: `could not fetch ${want.path} at ${want.ref.slice(0, 12)}: ${(e && e.message) || e}` };
      }
    }
    const size = bytes.byteLength ?? bytes.length ?? 0;
    let hex = null;
    if (size === want.bytes) {
      try { hex = toHex(await digest(bytes)); }
      catch (e) {
        return { ...base, state: "error", source, size, digest: null,
          error: `could not compute SHA-256 for ${want.name}: ${(e && e.message) || e}` };
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
        return { ...base, state: "error", source, size, digest: hex, error: (e && e.message) || String(e) };
      }
      runner.files.set(want.name, file);
      runner.imgProvenance.set(want.name, { sha256: want.sha256, path: want.path, ref: want.ref, bytes: want.bytes, at: now() });
      return { ...base, state: "ready", source, size, digest: hex, error: null };
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
    return { ...base, state: "refused", source, size, digest: hex,
      error: `${want.path} at ${want.ref.slice(0, 12)} ${why}. Nothing was uploaded and this image cannot be used; the manifest and the repository disagree about which file this is.` };
  }
  /* c8 ignore next */
  return { ...base, state: "error", source, size: null, digest: null, error: "verification did not settle" };
}

/**
 * Has every bound image been prepared and verified, right now? Read at the moment Start is tapped,
 * from the runner's own state rather than from whatever the preparation reported earlier, so a
 * stale report cannot open a job. Pure apart from reading the two maps it is handed.
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
    const size = Number(file.size);
    if (size !== want.bytes) {
      problems.push(`${want.name} is holding ${size} bytes, not the ${want.bytes} the pack names`);
    }
  }
  return problems;
}
