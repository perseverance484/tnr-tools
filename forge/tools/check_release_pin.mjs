import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The public loader may self-update from main, but the executable bundle it names must stay
// immutable. Development branches therefore keep the last released @version/@require and mark the
// next package version with @x-release-pending. release_pin.yml promotes both together after merge.
const repo = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const REQUIRE_RE = /^\/\/ @require\s+(\S+)\s*$/m;
const VERSION_RE = /^\/\/ @version\s+(\S+)\s*$/m;
const UPDATE_RE = /^\/\/ @updateURL\s+(\S+)\s*$/m;
const DOWNLOAD_RE = /^\/\/ @downloadURL\s+(\S+)\s*$/m;
const MARKER_RE = /^\/\/ @x-unpinned-until-release\s+(\S+)\s*$/m;
const PENDING_RE = /^\/\/ @x-release-pending\s+(\S+)\s*$/m;
const JSDELIVR_RE = /^https:\/\/cdn\.jsdelivr\.net\/gh\/perseverance484\/tnr-tools@(.+)\/([A-Za-z0-9_.-]+\.js)$/;
const SHA_RE = /^[0-9a-f]{40}$/;
const UPDATE_URL = "https://raw.githubusercontent.com/perseverance484/tnr-tools/main/forge_loader_user.js";
const WORKFLOWS = [".github/workflows/release_pin.yml", "state/staged_workflows/release_pin.yml"];

const blocker = (text) => ({ level: "blocker", text });

export function checkReleasePin({ root = repo } = {}) {
  const problems = [];
  const add = (text) => problems.push(blocker(text));
  const loaderPath = join(root, "forge_loader_user.js");
  if (!existsSync(loaderPath)) return [blocker("forge_loader_user.js is missing")];

  const loader = readFileSync(loaderPath, "utf8");
  const req = REQUIRE_RE.exec(loader);
  let requirePinned = false;
  if (!req) {
    add("forge_loader_user.js has no @require line");
  } else {
    const url = JSDELIVR_RE.exec(req[1]);
    if (!url) {
      add(`forge_loader_user.js @require is not a jsDelivr URL for this repository: ${req[1]}`);
    } else {
      const [, ref, file] = url;
      if (file !== "forge_bundle.js") add(`forge_loader_user.js @require serves ${file}, not forge_bundle.js`);
      if (!SHA_RE.test(ref)) {
        const marker = MARKER_RE.exec(loader);
        if (!marker) add(`forge_loader_user.js @require floats on "${ref}" with no @x-unpinned-until-release marker`);
        else add(`forge_loader_user.js @require floats on "${ref}"; Forge self-update requires the last immutable release pin, not @x-unpinned-until-release`);
      } else {
        requirePinned = true;
        if (MARKER_RE.test(loader)) add("forge_loader_user.js is commit-pinned but still carries @x-unpinned-until-release");
      }
    }
  }

  const update = UPDATE_RE.exec(loader)?.[1];
  const download = DOWNLOAD_RE.exec(loader)?.[1];
  if (update !== UPDATE_URL) add(`forge_loader_user.js @updateURL must be ${UPDATE_URL}`);
  if (download !== UPDATE_URL) add(`forge_loader_user.js @downloadURL must be ${UPDATE_URL}`);

  const version = VERSION_RE.exec(loader)?.[1];
  const pending = PENDING_RE.exec(loader)?.[1];
  const packagePath = join(root, "forge", "package.json");
  if (!existsSync(packagePath)) add("forge/package.json is missing");
  else {
    const expected = JSON.parse(readFileSync(packagePath, "utf8")).version;
    if (!version) {
      add("forge_loader_user.js has no @version line");
    } else if (version !== expected) {
      if (!(requirePinned && pending === expected)) {
        add(`forge_loader_user.js @version ${version} != forge/package.json ${expected}`);
      }
    } else if (pending) {
      add(`forge_loader_user.js @x-release-pending ${pending} remains even though @version already equals forge/package.json ${expected}`);
    }
    if (pending && pending !== expected) {
      add(`forge_loader_user.js @x-release-pending ${pending} != forge/package.json ${expected}`);
    }
  }

  const workflowRel = WORKFLOWS.find((rel) => existsSync(join(root, rel)));
  if (!workflowRel) {
    add("release_pin.yml is missing");
  } else {
    const workflow = readFileSync(join(root, workflowRel), "utf8");
    for (const bundle of ["builder_bundle.js", "forge_bundle.js"]) {
      if (!workflow.includes(bundle)) add(`${workflowRel} does not cover ${bundle}`);
    }
    if (!workflow.includes("python3 .github/scripts/pin_release.py")) add(`${workflowRel} does not invoke pin_release.py`);
    if (/git diff --name-only|HEAD~1/.test(workflow)) {
      add(`${workflowRel} pins only the last commit's changed bundle; the latest run must pin both current loaders`);
    }
  }

  const scriptPath = join(root, ".github", "scripts", "pin_release.py");
  if (!existsSync(scriptPath)) {
    add("pin_release.py is missing");
  } else {
    const script = readFileSync(scriptPath, "utf8");
    if (/sys\.stdin/.test(script)) add("pin_release.py still selects targets from stdin; it must pin both current bundles on every run");
    if (!script.includes("@x-release-pending")) add("pin_release.py does not remove @x-release-pending during promotion");
  }
  return problems;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const problems = checkReleasePin();
  for (const problem of problems) console.error(`release-pin: ${problem.text}`);
  console.log(problems.length ? `${problems.length} blocker(s)` : "release pin ok");
  process.exit(problems.length ? 1 : 0);
}
