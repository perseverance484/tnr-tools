#!/usr/bin/env node
// Author a manifest's `imagePack` from files that are ALREADY COMMITTED to this repository.
//
// The binding a pack carries has to be true, and the only way to make that a property of the tool
// rather than a habit of whoever runs it is to read the bytes out of git itself. So this reads every
// blob with `git cat-file blob <ref>:<path>` at a resolved 40-hex commit - never from the working
// tree. A file that is staged, modified, untracked or absent at that commit cannot be bound, and the
// tool says which. That is the difference between "the pack names the file I have" and "the pack
// names a file this commit holds", and the second is the one an operator's Forge can verify.
//
// It also cross-checks the manifest's own `imgSizes` ledger (L17) and refuses to emit an entry that
// disagrees with it, because parseManifest refuses that manifest anyway and a tool that emits a
// manifest its own parser rejects is a trap.
//
// Usage:
//   node forge/tools/make_image_pack.mjs <manifest.json> --root <dir> [--ref <rev>] [--write]
//   node forge/tools/make_image_pack.mjs <manifest.json> --map <name>=<repo/path> [...] [--ref <rev>]
//
//   --root <dir>   look for each @img logical name at <dir>/<name>. The usual case: one art folder
//                  whose filenames are the manifest's @img names, character for character.
//   --map n=p      bind one logical name to an explicit repository path. Repeatable, and it wins
//                  over --root for that name.
//   --ref <rev>    the commit to bind to. Anything git can resolve (default HEAD); it is resolved to
//                  a 40-hex commit sha and THAT is what goes in the manifest.
//   --write        splice the pack into the manifest in place (2-space JSON, trailing newline).
//                  Without it, the pack is printed for inspection.
//
// Zero network, zero game requests. It reads git and one manifest file.

import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { pathProblem, extOf } from "../src/runner/imgpack.mjs";

const REPO = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const IMG_REF = /@img:([A-Za-z0-9_.\-]+)/g;

function git(args, { encoding = "utf8", quiet = false } = {}) {
  return execFileSync("git", ["-C", REPO, ...args], {
    encoding, maxBuffer: 64 * 1024 * 1024,
    // A missing blob is an expected outcome that this tool reports itself, so git's own "fatal:"
    // line is suppressed rather than interleaved with the refusals.
    stdio: quiet ? ["ignore", "pipe", "ignore"] : ["ignore", "pipe", "pipe"],
  });
}

/** Resolve any revision to the 40-hex commit a pack is allowed to name. */
export function resolveCommit(rev = "HEAD") {
  const sha = git(["rev-parse", `${rev}^{commit}`]).trim();
  if (!/^[0-9a-f]{40}$/.test(sha)) throw new Error(`${rev} did not resolve to a commit sha (got ${JSON.stringify(sha)})`);
  return sha;
}

/** The bytes a commit holds at a path, or a thrown error naming what is missing. */
export function blobAt(ref, path) {
  try {
    return git(["cat-file", "blob", `${ref}:${path}`], { encoding: "buffer", quiet: true });
  } catch {
    throw new Error(`${path} is not in commit ${ref.slice(0, 12)}. Commit the file first; a pack must bind bytes the repository already holds.`);
  }
}

export const sha256Hex = (buf) => createHash("sha256").update(buf).digest("hex");

/**
 * Build the pack. Pure apart from git and the manifest text it is handed.
 * @returns {{pack: object|null, problems: string[], notes: string[]}}
 */
export function buildPack(manifest, { ref, root = null, map = {} }) {
  const problems = [], notes = [];
  const imgSizes = (manifest.imgSizes && typeof manifest.imgSizes === "object") ? manifest.imgSizes : {};
  const names = [...new Set([...JSON.stringify(manifest.items ?? manifest.jutsu ?? []).matchAll(IMG_REF)].map((m) => m[1]))].sort();
  if (!names.length) return { pack: null, problems: ["this manifest has no @img references"], notes };

  const files = {};
  for (const name of names) {
    const path = map[name] ?? (root ? `${root.replace(/\/+$/, "")}/${name}` : null);
    if (!path) { problems.push(`${name}: no path (pass --root, or --map ${name}=<repo/path>)`); continue; }
    const bad = pathProblem(path);
    if (bad) { problems.push(`${name}: ${bad}`); continue; }
    if (extOf(path) !== extOf(name)) { problems.push(`${name}: ${path} is a ${extOf(path)}, but the @img name is a ${extOf(name)}`); continue; }
    let bytes;
    try { bytes = blobAt(ref, path); } catch (e) { problems.push(`${name}: ${e.message}`); continue; }
    const ledger = Object.prototype.hasOwnProperty.call(imgSizes, name) ? Number(imgSizes[name]) : null;
    if (ledger == null || !Number.isFinite(ledger)) {
      problems.push(`${name}: no imgSizes entry; add the byte ledger L17 requires (this file is ${bytes.length} bytes)`);
      continue;
    }
    if (ledger !== bytes.length) {
      problems.push(`${name}: ${path} at ${ref.slice(0, 12)} is ${bytes.length} bytes but imgSizes says ${ledger}. One of them is wrong; do not just take the file's number.`);
      continue;
    }
    files[name] = { path, sha256: sha256Hex(bytes), bytes: bytes.length };
    notes.push(`${name} <- ${path} @ ${ref.slice(0, 12)} (${bytes.length} bytes, sha256 ${files[name].sha256.slice(0, 16)}…)`);
  }
  if (problems.length) return { pack: null, problems, notes };
  return { pack: { ref, files }, problems, notes };
}

function parseArgs(argv) {
  const out = { manifest: null, root: null, ref: "HEAD", write: false, map: {} };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--root") out.root = argv[++i];
    else if (a === "--ref") out.ref = argv[++i];
    else if (a === "--write") out.write = true;
    else if (a === "--map") { const [k, ...v] = String(argv[++i]).split("="); out.map[k] = v.join("="); }
    else if (a.startsWith("--")) throw new Error(`unknown option ${a}`);
    else if (!out.manifest) out.manifest = a;
    else throw new Error(`unexpected argument ${a}`);
  }
  if (!out.manifest) throw new Error("usage: make_image_pack.mjs <manifest.json> --root <dir> [--ref <rev>] [--write]");
  return out;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = parseArgs(process.argv.slice(2));
  const ref = resolveCommit(args.ref);
  const text = readFileSync(args.manifest, "utf8");
  const manifest = JSON.parse(text);
  const { pack, problems, notes } = buildPack(manifest, { ref, root: args.root, map: args.map });
  for (const n of notes) console.log("  " + n);
  for (const p of problems) console.error("  REFUSED " + p);
  if (!pack) { console.error(`${problems.length} problem(s); no pack written`); process.exit(1); }
  console.log(`pack: ${Object.keys(pack.files).length} file(s) bound to ${ref}`);
  if (!args.write) { console.log(JSON.stringify({ imagePack: pack }, null, 2)); process.exit(0); }
  // Key order: imagePack sits next to imgSizes, which is the ledger it must agree with.
  const next = {};
  for (const k of Object.keys(manifest)) { next[k] = manifest[k]; if (k === "imgSizes") next.imagePack = pack; }
  if (!next.imagePack) next.imagePack = pack;
  writeFileSync(args.manifest, JSON.stringify(next, null, 2) + "\n");
  console.log(`wrote imagePack into ${relative(REPO, args.manifest) || args.manifest}`);
}
