// Adversarial scenarios for the presentation tooling.
//
// Every negative fixture is a MUTATION OF THE REAL GODSTORM EVIDENCE rather than a hand-written
// miniature. A miniature proves the code rejects what the test author imagined; a mutation proves
// it rejects the thing that actually went wrong, in the shape it actually has.
//
// The mutation never touches the repository. A scenario builds a throwaway root, symlinks the
// files it does not change (and each art FILE, never the directory - linking the directory once let
// a same-size fixture write straight through it into the repository's approved art), and writes the
// ones it does, unlinking first so a replacement replaces the link and not its target.
//
// SIMULATING A COMMITTED WORLD. The evidence package is now pinned: each record declares its
// sha256 and the loader checks the working file against the blob at `repoCommit`. A scenario that
// edits a record would therefore always fail on the source lock, never on the thing under test. So
// by default `files:` mutations are treated as COMMITTED - the declared digest is rewritten and the
// blob reader serves the mutated bytes for that commit. Testing the lock itself is what
// `uncommitted:` and `blobAtRef:` are for.

import { mkdtempSync, mkdirSync, symlinkSync, writeFileSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { createHash } from "node:crypto";
import { tmpdir } from "node:os";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { buildFromSpecFile } from "../presentation/build.mjs";
import { gitBlobReader } from "../presentation/gitblob.mjs";

export const REPO = resolve(join(dirname(fileURLToPath(import.meta.url)), "..", ".."));
export const PKG = join(REPO, "forge", "presentation", "packages", "godstorm");

/** The evidence files the Godstorm package selects, by the record id that selects them. */
export const SOURCES = {
  "marrow-quest": "harvests/inbox/tnr_results_1789829183863.json",
  "stormcourt-quest": "harvests/inbox/tnr_results_1789842714086.json",
  "ai-2026-09-19": "harvests/inbox/tnr_results_1789842714086.json",
  "ai-2026-09-14": "harvests/inbox/tnr_results_1789402842027.json",
  "assets-2026-09-14": "harvests/inbox/tnr_results_1789402842027.json",
  "pack-push53": "archive/spent-manifests/push-2026-09-19/53_godstorm_failed_items_repair.json",
  "uploads-push53": "harvests/inbox/tnr_results_1789842714086.json",
};

const readJson = (p) => JSON.parse(readFileSync(p, "utf8"));
const sha = (b) => createHash("sha256").update(b).digest("hex");

/**
 * Build the Godstorm dossier against a mutated copy of its own evidence.
 *
 * @param {object} o
 * @param {object} [o.files]   {repoRelativePath: (json) => json} - mutate a source AND treat the
 *   mutation as committed (declared digest rewritten, blob reader follows)
 * @param {object} [o.uncommitted] {repoRelativePath: (json) => json} - mutate the WORKING TREE only:
 *   the declared digest and the committed blob keep the real values, so the source lock should fire
 * @param {object} [o.extraFiles] {repoRelativePath: string|Buffer} - write a file over a link
 * @param {function} [o.spec]  (parsedSpec) => parsedSpec
 * @param {function} [o.evidence] (parsedPackage) => parsedPackage, applied AFTER digest rewriting
 * @param {function} [o.blobAtRef]  (ref, path, fallback) => Buffer|null
 * @param {boolean} [o.requireExactBytes]
 * @returns {{ok: true, built} | {ok: false, error: Error}}
 */
export function scenario({ files = {}, uncommitted = {}, extraFiles = {}, spec = (s) => s, evidence = (e) => e, blobAtRef, requireExactBytes = false } = {}) {
  const root = mkdtempSync(join(tmpdir(), "tnr-presentation-"));
  try {
    mkdirSync(join(root, "art", "godstorm"), { recursive: true });
    for (const f of readdirSync(join(REPO, "art", "godstorm"))) {
      symlinkSync(join(REPO, "art", "godstorm", f), join(root, "art", "godstorm", f));
    }

    const write = (rel, contents) => {
      const dest = join(root, rel);
      mkdirSync(dirname(dest), { recursive: true });
      rmSync(dest, { force: true });   // drops a symlink itself; never follows it
      writeFileSync(dest, contents);
    };

    // bytes the simulated commit holds, per path: the mutation for `files`, the real file otherwise
    const committed = new Map();
    const declared = new Map();
    for (const rel of new Set(Object.values(SOURCES))) {
      const real = readFileSync(join(REPO, rel));
      if (Object.prototype.hasOwnProperty.call(files, rel)) {
        const text = JSON.stringify(files[rel](JSON.parse(real.toString("utf8"))));
        write(rel, text);
        committed.set(rel, Buffer.from(text));
        declared.set(rel, sha(Buffer.from(text)));
      } else if (Object.prototype.hasOwnProperty.call(uncommitted, rel)) {
        // working tree diverges; the commit and the declared digest stay honest
        write(rel, JSON.stringify(uncommitted[rel](JSON.parse(real.toString("utf8")))));
        committed.set(rel, real);
        declared.set(rel, sha(real));
      } else {
        const dest = join(root, rel);
        mkdirSync(dirname(dest), { recursive: true });
        symlinkSync(join(REPO, rel), dest);
        committed.set(rel, real);
        declared.set(rel, sha(real));
      }
    }
    for (const [rel, contents] of Object.entries(extraFiles)) write(rel, contents);

    const pkg = readJson(join(PKG, "evidence.json"));
    for (const r of pkg.records) if (declared.has(r.path)) r.sha256 = declared.get(r.path);
    const repoCommit = pkg.repoCommit;

    const specDir = join(root, "spec");
    mkdirSync(specDir, { recursive: true });
    writeFileSync(join(specDir, "evidence.json"), JSON.stringify(evidence(pkg)));
    writeFileSync(join(specDir, "spec.json"), JSON.stringify(spec(readJson(join(PKG, "spec.json")))));

    // Art blobs live at the image pack's own commit and come from the REAL repository; evidence
    // blobs come from the simulated commit this scenario just built.
    const realGit = gitBlobReader(REPO);
    const fallback = (ref, path) => (ref === repoCommit && committed.has(path) ? committed.get(path) : realGit(ref, path));
    const reader = blobAtRef ? (ref, path) => blobAtRef(ref, path, fallback) : fallback;

    try {
      const built = buildFromSpecFile(join(specDir, "spec.json"), { root, gitRoot: REPO, blobAtRef: reader, requireExactBytes });
      return { ok: true, built, root };
    } catch (error) {
      return { ok: false, error, root };
    }
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

/** Fatal findings of one code. */
export const fatalsOf = (built, code) => built.lint.fatal.filter((f) => f.code === code);
/** Every fatal message joined, for a readable assertion failure. */
export const fatalText = (built) => built.lint.fatal.map((f) => `${f.code}: ${f.message}`).join("\n");
/** Every warning message joined. */
export const warnText = (built) => built.lint.warnings.map((f) => `${f.code}: ${f.message}`).join("\n");

/** Ids of the Godstorm AIs this suite names. */
export const AI = Object.freeze({
  umbralReaver: "9uDe65Qt90xnT-fM5vJZ7",
  hollowLantern: "IG5Mbfi_2lpUTnUU4_XhZ",
  starlessMonk: "qQ6jMh8w6aiyr4pevwDh-",
  nightveilSentinel: "YvinZCoMWiz0RY8ZBP5EW",
  wardenFirstDark: "oi4bHe3upEhLkI-ElJuMX",
  keeperHushedHours: "s6LjnqhSW85pIxYRM76Fw",
  mothTyrant: "jGHpkz2pgLu8loti6pZZi",
  chainedChorister: "QV1PwoQR9JImZL2_fcOsk",
  wardenHalfEclipse: "3XMsIV6Yv4jy-uaJAe52f",
  sovereignEcho: "i8oFdDcneF7YE-8VpQsu3",
});

export const MARROW = "2yvE9PUQqlD8lbYNfgX-b";
export const STORMCOURT = "OSADdXqostbyVliCxWk6k";
export const MARROW_CAPTURE_AT = "2026-09-19T14:46:23.568Z";

/** Rewrite the captured quest record for one quest inside a results bundle. */
export function editQuest(questId, edit) {
  return (bundle) => {
    for (const c of bundle.captures || []) {
      if (c.proc === "quests.get" && c.input && c.input.id === questId) c.data = edit(c.data);
    }
    return bundle;
  };
}

/** Remove the profile.getAi capture of one AI entirely. */
export function dropAiCapture(aiId) {
  return (bundle) => {
    bundle.captures = (bundle.captures || []).filter((c) => !(c.proc === "profile.getAi" && c.input && c.input.userId === aiId));
    return bundle;
  };
}

/** The capture of one AI, for a test that wants to read or damage it. */
export const aiCapture = (bundle, aiId) => (bundle.captures || []).find((c) => c.proc === "profile.getAi" && c.input && c.input.userId === aiId);
