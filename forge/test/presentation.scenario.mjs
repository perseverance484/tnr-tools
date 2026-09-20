// Adversarial scenarios for the presentation tooling.
//
// Every negative fixture in the plan is a MUTATION OF THE REAL GODSTORM EVIDENCE rather than a
// hand-written miniature. A miniature proves the code rejects what the test author imagined; a
// mutation proves it rejects the thing that actually went wrong, in the shape it actually has.
//
// The mutation never touches the repository. A scenario builds a throwaway root, symlinks the
// files it does not change (and the art directory, which is only ever read), and writes the ones
// it does. Nothing under harvests/, archive/ or art/ is opened for writing at any point.

import { mkdtempSync, mkdirSync, symlinkSync, writeFileSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { buildFromSpecFile } from "../presentation/build.mjs";

export const REPO = resolve(join(dirname(fileURLToPath(import.meta.url)), "..", ".."));
export const PKG = join(REPO, "forge", "presentation", "packages", "godstorm");

/** The evidence files the Godstorm package selects, by the record id that selects them. */
export const SOURCES = {
  "marrow-quest": "harvests/inbox/tnr_results_1789829183863.json",
  "stormcourt-quest": "harvests/inbox/tnr_results_1789842714086.json",
  "ai-2026-09-19": "harvests/inbox/tnr_results_1789842714086.json",
  "ai-2026-09-14": "harvests/inbox/tnr_results_1789402842027.json",
  "pack-push53": "archive/spent-manifests/push-2026-09-19/53_godstorm_failed_items_repair.json",
  "uploads-push53": "harvests/inbox/tnr_results_1789842714086.json",
};

const readJson = (p) => JSON.parse(readFileSync(p, "utf8"));

/**
 * Build the Godstorm dossier against a mutated copy of its own evidence.
 *
 * @param {object} o
 * @param {object} [o.files]   {repoRelativePath: (parsedJson) => parsedJson} - mutate a source
 * @param {object} [o.extraFiles] {repoRelativePath: string} - write a file that does not exist yet
 * @param {function} [o.spec]  (parsedSpec) => parsedSpec
 * @param {function} [o.evidence] (parsedPackage) => parsedPackage
 * @param {function} [o.blobAtRef]  override the commit-blob reader
 * @param {boolean} [o.requireExactBytes]
 * @returns {{ok: true, built} | {ok: false, error: Error}}
 */
export function scenario({ files = {}, extraFiles = {}, spec = (s) => s, evidence = (e) => e, blobAtRef, requireExactBytes = false } = {}) {
  const root = mkdtempSync(join(tmpdir(), "tnr-presentation-"));
  try {
    // NEVER symlink a DIRECTORY here. An earlier version linked art/godstorm wholesale and a
    // scenario that wrote a same-size replacement into it wrote straight through the link into the
    // repository's own approved art. Individual file links cannot do that, and `write()` below
    // removes the link before writing so a replacement replaces the LINK, not its target.
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

    const mutated = new Set(Object.keys(files));
    for (const rel of new Set(Object.values(SOURCES))) {
      const dest = join(root, rel);
      mkdirSync(dirname(dest), { recursive: true });
      if (mutated.has(rel)) write(rel, JSON.stringify(files[rel](readJson(join(REPO, rel)))));
      else symlinkSync(join(REPO, rel), dest);
    }
    for (const [rel, contents] of Object.entries(extraFiles)) write(rel, contents);

    const specDir = join(root, "spec");
    mkdirSync(specDir, { recursive: true });
    writeFileSync(join(specDir, "evidence.json"), JSON.stringify(evidence(readJson(join(PKG, "evidence.json")))));
    writeFileSync(join(specDir, "spec.json"), JSON.stringify(spec(readJson(join(PKG, "spec.json")))));

    try {
      const built = buildFromSpecFile(join(specDir, "spec.json"), {
        root,
        // the commit a pack names lives in the REAL repository; the throwaway root is not a clone
        gitRoot: REPO,
        blobAtRef,
        requireExactBytes,
      });
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

/** Ids of the eighteen Godstorm AIs, by the name the captures give them. */
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

/** Rewrite the captured quest record for one quest inside a results bundle. */
export function editQuest(questId, edit) {
  return (bundle) => {
    for (const c of bundle.captures || []) {
      if (c.proc === "quests.get" && c.input && c.input.id === questId) c.data = edit(c.data);
    }
    return bundle;
  };
}

/** Drop every AI record for one userId from a results bundle, wherever it is nested. */
export function dropAi(aiId) {
  const strip = (node) => {
    if (Array.isArray(node)) return node.map(strip);
    if (!node || typeof node !== "object") return node;
    if (node.userId === aiId && typeof node.avatar === "string") {
      const { avatar, username, ...rest } = node;
      void avatar; void username;
      return rest;
    }
    return Object.fromEntries(Object.entries(node).map(([k, v]) => [k, strip(v)]));
  };
  return strip;
}
