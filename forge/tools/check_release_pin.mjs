// The release path cannot silently float on a branch (readiness brief section 8).
//
//   node tools/check_release_pin.mjs        # exits 1 and prints every problem
//
// Also asserted by the test suite, so `npm test` fails on a regression here.
//
// What a floating @require costs: jsDelivr serves a branch ref from cache for about twelve hours
// and any later push changes what that URL returns, so the bytes running against the game are not
// necessarily the bytes that were reviewed. For a mutation client that is the difference between
// "audited" and "probably audited". The pinned form (@<40-hex sha>) is immutable and permanently
// cached, and a new bundle is a new URL, which is also what makes ViolentMonkey refetch.
//
// The one allowed exception is an explicit, greppable marker: while a release branch is still in
// review its loader may point at that branch IF it carries `// @x-unpinned-until-release <branch>`.
// release_pin.yml deletes that line when it writes the commit pin, so the exception cannot survive
// the release that makes it false.

import { readFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const REQUIRE_RE = /^\/\/ @require\s+(\S+)\s*$/m;
const VERSION_RE = /^\/\/ @version\s+(\S+)\s*$/m;
const MARKER_RE = /^\/\/ @x-unpinned-until-release\s+(\S+)\s*$/m;
const JSDELIVR_RE = /^https:\/\/cdn\.jsdelivr\.net\/gh\/perseverance484\/tnr-tools@(.+)\/([A-Za-z0-9_.-]+\.js)$/;
const SHA_RE = /^[0-9a-f]{40}$/;

/**
 * @returns {{level: "blocker"|"pending-install", text: string}[]}
 * "blocker" is something wrong in this tree. "pending-install" is the one thing Fable cannot do:
 * the PAT cannot push .github/workflows/, so installing a staged workflow is a dauntless action.
 * The test treats a blocker as a failure and a pending install as a fact to report, which keeps the
 * suite honest without leaving it permanently red for a reason outside this branch.
 */
export function checkReleasePin({ root = repo } = {}) {
  const problems = [];
  const add = (text, level = "blocker") => problems.push({ level, text });
  const loaderPath = join(root, "forge_loader_user.js");
  const loader = readFileSync(loaderPath, "utf8");

  const req = REQUIRE_RE.exec(loader);
  if (!req) return [{ level: "blocker", text: "forge_loader_user.js has no @require line" }];
  const url = JSDELIVR_RE.exec(req[1]);
  if (!url) {
    add(`forge_loader_user.js @require is not a jsDelivr URL for this repository: ${req[1]}`);
  } else {
    const [, ref, file] = url;
    if (file !== "forge_bundle.js") add(`forge_loader_user.js @require serves ${file}, not forge_bundle.js`);
    if (!SHA_RE.test(ref)) {
      const marker = MARKER_RE.exec(loader);
      if (!marker) {
        add(`forge_loader_user.js @require floats on "${ref}" with no @x-unpinned-until-release marker: ` + "a release must resolve an immutable commit, and an unpinned one must say so out loud");
      } else if (marker[1] !== ref) {
        add(`forge_loader_user.js marker says "${marker[1]}" but the @require serves "${ref}"`);
      }
    } else if (MARKER_RE.test(loader)) {
      add("forge_loader_user.js is commit-pinned but still carries @x-unpinned-until-release; remove the marker");
    }
  }

  const ver = VERSION_RE.exec(loader);
  const pkg = JSON.parse(readFileSync(join(root, "forge", "package.json"), "utf8"));
  if (!ver) add("forge_loader_user.js has no @version line");
  else if (ver[1] !== pkg.version) {
    add(`forge_loader_user.js @version ${ver[1]} != forge/package.json ${pkg.version}: ` + "ViolentMonkey refetches on a version rise, so a new bundle with an old version installs stale");
  }

  // The workflow that does the pinning must actually cover forge. Check the staged copy always, and
  // the installed one when it exists (they can differ: the PAT cannot push .github/workflows/).
  for (const rel of ["state/staged_workflows/release_pin.yml", ".github/workflows/release_pin.yml"]) {
    const p = join(root, rel);
    if (!existsSync(p)) {
      if (rel.startsWith("state/")) add(`${rel} is missing: the release-pin workflow must be staged`);
      continue;
    }
    const wf = readFileSync(p, "utf8");
    const covers = /paths:.*forge_bundle\.js/.test(wf) && /forge_loader_user\.js/.test(wf);
    if (!covers) {
      add(`${rel} does not pin forge: ` + (rel.startsWith(".github/") ? "install the staged copy (a dauntless action)" : "add forge_bundle.js to its paths filter"),
        rel.startsWith(".github/") ? "pending-install" : "blocker");
    }
  }
  return problems;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const problems = checkReleasePin();
  for (const p of problems) console.error(`release-pin [${p.level}]: ${p.text}`);
  const blockers = problems.filter((p) => p.level === "blocker").length;
  console.log(problems.length ? `${blockers} blocker(s), ${problems.length - blockers} pending install(s)` : "release pin ok");
  process.exit(problems.length ? 1 : 0);
}
