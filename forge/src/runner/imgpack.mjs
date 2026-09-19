// Repo-backed image packs: the manifest block that binds each `@img:<name>` to an IMMUTABLE
// repository blob, and the rules that make that binding trustworthy.
//
// WHY THIS EXISTS. Every `@img` reference used to be satisfied by whatever the operator's device
// handed to a file input. harvests/inbox/tnr_results_1789829183863.json is what that costs: five
// Marrow avatar edits ran to their uploads behind the right filenames carrying a 1.7 MB master PNG,
// and the run learned about it one ceiling refusal at a time. The byte ledger (`imgSizes`, L17) made
// that visible before Start; it still cannot say WHICH bytes were meant, because a size is not an
// identity. A pack says exactly which bytes: a repository path, a 40-hex commit, and the SHA-256 of
// the blob. Forge fetches those bytes and refuses to proceed unless the digest it computed equals
// the digest the manifest named.
//
// THE SHAPE, under a manifest's top level:
//
//   "imagePack": {
//     "ref": "<40-hex commit sha>",
//     "files": {
//       "ai_godstorm_marrow_starless_monk.webp": {
//         "path": "art/godstorm/ai_godstorm_marrow_starless_monk.webp",
//         "sha256": "<64 lowercase hex>",
//         "bytes": 207410
//       }
//     }
//   }
//
// FIVE RULES, all fail-closed at parse time so a malformed pack can never open a job:
//
//   1. `ref` is a 40-hex COMMIT sha. Not a branch, not a tag, not "main". A branch moves, and a
//      binding that can be changed after review is not provenance. This is the whole point of the
//      word "immutable" in the proposal, so it is a hard error rather than an advisory.
//   2. `path` is repository-relative and plain: named segments only, no leading slash, no "." or
//      "..", no backslash, no scheme. A pack is data that arrives with a manifest; it must not be
//      able to address anything but a file in this repository at that commit.
//   3. `sha256` is 64 lowercase hex. Verification compares against it byte for byte, and the
//      comparison is the only reason any of this is safe.
//   4. `bytes` MUST equal the manifest's own `imgSizes` entry for the same logical name. Two
//      ledgers that disagree about one file mean the manifest is internally contradictory, and
//      guessing which one is authoritative is exactly how the Godstorm run shipped the wrong file.
//      Refuse instead, and name both numbers.
//   5. The repository path's extension must match the logical name's extension. `@img` resolves by
//      exact filename (skills/producing-tnr-art), the extension decides the MIME the uploader
//      declares, and a .png blob bound to a .webp logical name is a mismatch worth failing on.
//
// A pack does NOT have to cover every `@img` in the manifest. Uncovered names fall back to the
// manual picker exactly as before - that is the "manual picker: fallback only" half of the proposal.
// Names the pack DOES cover are its own: the picker never offers to substitute a device file for a
// bound image, because a provenance that an operator can overwrite from a gallery is decoration.

/** The logical-name charset `@img:` itself accepts (refs.mjs / lints.mjs IMG_REF_RE). */
export const IMG_NAME_RE = /^[A-Za-z0-9_.\-]+$/;
export const COMMIT_RE = /^[0-9a-f]{40}$/;
export const SHA256_RE = /^[0-9a-f]{64}$/;
const SEGMENT_RE = /^[A-Za-z0-9._-]+$/;

/** The MIME a logical filename declares. Kept here because the pack decides the File it builds. */
export const EXT_MIME = Object.freeze({
  webp: "image/webp", png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif", avif: "image/avif",
});
export const extOf = (n) => { const m = /\.([A-Za-z0-9]+)$/.exec(String(n ?? "")); return m ? m[1].toLowerCase() : null; };
export const mimeOf = (n) => EXT_MIME[extOf(n)] ?? "application/octet-stream";

/** Lowercase hex for an ArrayBuffer/TypedArray. Pure; the digest itself is injected. */
export function toHex(buf) {
  const bytes = buf instanceof Uint8Array ? buf : new Uint8Array(buf);
  let out = "";
  for (let i = 0; i < bytes.length; i++) out += bytes[i].toString(16).padStart(2, "0");
  return out;
}

/** A repository path is plain and relative, or it is refused. Returns a reason, or null when ok. */
export function pathProblem(path) {
  if (typeof path !== "string" || !path) return "path must be a non-empty string";
  if (path.length > 255) return "path is longer than 255 characters";
  if (path.includes("\\")) return "path contains a backslash";
  if (/^[A-Za-z][A-Za-z0-9+.-]*:/.test(path)) return "path looks like a URL, not a repository path";
  if (path.startsWith("/")) return "path must be repository-relative (no leading slash)";
  const segments = path.split("/");
  for (const s of segments) {
    if (!s) return "path has an empty segment";
    if (s === "." || s === "..") return `path segment ${JSON.stringify(s)} is not allowed`;
    if (!SEGMENT_RE.test(s)) return `path segment ${JSON.stringify(s)} has characters outside [A-Za-z0-9._-]`;
  }
  return null;
}

/**
 * Normalize and validate a manifest's `imagePack`. Pure: no I/O, no digesting, no fetch.
 *
 * Returns `{pack, errors, warnings}`. `pack` is null when the manifest carries no pack OR when it
 * carries a broken one - a caller must treat a non-empty `errors` as fatal (parseManifest does),
 * because half a pack is worse than none.
 *
 * @param {any} raw            the manifest's `imagePack` value, whatever it is
 * @param {object} o
 * @param {object} o.imgSizes  the manifest's byte ledger, for rule 4
 * @param {string[]} o.names   every logical `@img` name the manifest actually references
 */
export function normalizeImagePack(raw, { imgSizes = {}, names = [] } = {}) {
  const errors = [], warnings = [];
  if (raw === undefined || raw === null) return { pack: null, errors, warnings };
  if (typeof raw !== "object" || Array.isArray(raw)) {
    errors.push("imagePack must be an object {ref, files}");
    return { pack: null, errors, warnings };
  }
  const ref = raw.ref;
  if (typeof ref !== "string" || !COMMIT_RE.test(ref)) {
    // Named rather than coerced: "main" is the mistake this rule exists to stop, so say so.
    errors.push(`imagePack.ref must be a 40-hex commit sha (an immutable commit, not a branch or tag), got ${JSON.stringify(ref)}`);
  }
  const rawFiles = raw.files;
  if (!rawFiles || typeof rawFiles !== "object" || Array.isArray(rawFiles)) {
    errors.push("imagePack.files must be an object keyed by the logical @img filename");
    return { pack: null, errors, warnings };
  }
  const referenced = new Set(names);
  const files = {};
  for (const name of Object.keys(rawFiles).sort()) {
    const where = `imagePack.files[${JSON.stringify(name)}]`;
    const e = rawFiles[name];
    if (!IMG_NAME_RE.test(name)) { errors.push(`${where}: ${JSON.stringify(name)} is not a legal @img filename`); continue; }
    if (!e || typeof e !== "object" || Array.isArray(e)) { errors.push(`${where} must be an object {path, sha256, bytes}`); continue; }
    const problem = pathProblem(e.path);
    if (problem) { errors.push(`${where}: ${problem}`); continue; }
    if (typeof e.sha256 !== "string" || !SHA256_RE.test(e.sha256)) {
      errors.push(`${where}.sha256 must be 64 lowercase hex characters, got ${JSON.stringify(e.sha256)}`);
      continue;
    }
    if (!Number.isInteger(e.bytes) || e.bytes <= 0) {
      errors.push(`${where}.bytes must be a positive integer, got ${JSON.stringify(e.bytes)}`);
      continue;
    }
    if (extOf(e.path) !== extOf(name)) {
      errors.push(`${where}: repository file is a ${extOf(e.path) ?? "(no extension)"} but the @img name is a ${extOf(name) ?? "(no extension)"}; @img resolves by exact filename and the extension decides the upload's MIME`);
      continue;
    }
    // Rule 4. The ledger L17 already demands is the one the Start gate checks the File against, so
    // a pack that disagrees with it would make one of the two checks a lie.
    const ledger = Object.prototype.hasOwnProperty.call(imgSizes, name) ? Number(imgSizes[name]) : null;
    if (ledger == null || !Number.isFinite(ledger)) {
      errors.push(`${where}: no imgSizes entry for ${name}; a pack entry must agree with the manifest byte ledger (L17)`);
      continue;
    }
    if (ledger !== e.bytes) {
      errors.push(`${where}.bytes is ${e.bytes} but imgSizes says ${name} is ${ledger}; the manifest contradicts itself about which file this is`);
      continue;
    }
    if (!referenced.has(name)) {
      // Harmless but never fetched, so it is reported rather than refused: a pack copied between
      // manifests is a reasonable thing to do, and a silent dead entry is not.
      warnings.push(`imagePack binds ${name}, which no @img reference in this manifest uses; it will not be fetched`);
    }
    files[name] = { path: e.path, sha256: e.sha256, bytes: e.bytes };
  }
  if (!Object.keys(files).length && !errors.length) errors.push("imagePack.files is empty; remove the key instead");
  if (errors.length) return { pack: null, errors, warnings };
  return { pack: { ref, files }, errors, warnings };
}

/** Does this pack bind this logical name? */
export function packBinds(pack, name) {
  return !!(pack && pack.files && Object.prototype.hasOwnProperty.call(pack.files, name));
}

/** The bound entries the manifest actually needs, in a stable order. */
export function packWork(pack, names) {
  if (!pack) return [];
  return [...new Set(names ?? [])].filter((n) => packBinds(pack, n)).sort()
    .map((name) => ({ name, ref: pack.ref, ...pack.files[name] }));
}

/** Logical names the pack does NOT bind: the manual picker's remaining territory. */
export function unboundNames(pack, names) {
  return [...new Set(names ?? [])].filter((n) => !packBinds(pack, n));
}
