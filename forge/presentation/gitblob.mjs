// Read a file's bytes at an exact commit.
//
// The one place the presentation tooling shells out, kept on its own so assets.mjs stays a pure
// function of what it is handed and a test can present a working tree that disagrees with the
// commit. Same mechanism the image-pack drift guards and make_image_pack.mjs already use: a pack
// binds a blob at a commit, and `git cat-file` is what reads that blob.
//
// This is not a network call. `git cat-file` reads the local object database; a commit the clone
// does not contain returns null rather than fetching it (forge.yml checks out with fetch-depth 0
// for exactly this reason). A null is reported by the registry as "could not be checked", never
// as "checked and fine".

import { execFileSync } from "node:child_process";

/**
 * @param {string} gitRoot  repository working directory
 * @returns {(ref: string, path: string) => Buffer|null}
 */
export function gitBlobReader(gitRoot) {
  return (ref, path) => {
    if (!/^[0-9a-f]{40}$/.test(String(ref ?? ""))) return null;
    try {
      return execFileSync("git", ["-C", gitRoot, "cat-file", "-p", `${ref}:${path}`], {
        maxBuffer: 64 * 1024 * 1024,
        stdio: ["ignore", "pipe", "ignore"],
      });
    } catch {
      return null;
    }
  };
}
