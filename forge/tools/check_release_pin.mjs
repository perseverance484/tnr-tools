import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// A floating @require can change after review; release loaders must pin immutable bundle commits.
const repo = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const REQUIRE_RE = /^\/\/ @require\s+(\S+)\s*$/m;
const VERSION_RE = /^\/\/ @version\s+(\S+)\s*$/m;
const MARKER_RE = /^\/\/ @x-unpinned-until-release\s+(\S+)\s*$/m;
const JSDELIVR_RE = /^https:\/\/cdn\.jsdelivr\.net\/gh\/perseverance484\/tnr-tools@(.+)\/([A-Za-z0-9_.-]+\.js)$/;
const SHA_RE = /^[0-9a-f]{40}$/;
const WORKFLOWS = [".github/workflows/release_pin.yml", "state/staged_workflows/release_pin.yml"];

const blocker = (text) => ({ level: "blocker", text });

export function checkReleasePin({ root = repo } = {}) {
  const problems = [];
  const add = (text) => problems.push(blocker(text));
  const loaderPath = join(root, "forge_loader_user.js");
  if (!existsSync(loaderPath)) return [blocker("forge_loader_user.js is missing")];

  const loader = readFileSync(loaderPath, "utf8");
  const req = REQUIRE_RE.exec(loader);
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
        else if (marker[1] !== ref) add(`forge_loader_user.js marker says "${marker[1]}" but the @require serves "${ref}"`);
      } else if (MARKER_RE.test(loader)) {
        add("forge_loader_user.js is commit-pinned but still carries @x-unpinned-until-release");
      }
    }
  }

  const version = VERSION_RE.exec(loader)?.[1];
  const packagePath = join(root, "forge", "package.json");
  if (!existsSync(packagePath)) add("forge/package.json is missing");
  else {
    const expected = JSON.parse(readFileSync(packagePath, "utf8")).version;
    if (!version) add("forge_loader_user.js has no @version line");
    else if (version !== expected) add(`forge_loader_user.js @version ${version} != forge/package.json ${expected}`);
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
  if (existsSync(scriptPath) && /sys\.stdin/.test(readFileSync(scriptPath, "utf8"))) {
    add("pin_release.py still selects targets from stdin; it must pin both current bundles on every run");
  }
  return problems;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const problems = checkReleasePin();
  for (const problem of problems) console.error(`release-pin: ${problem.text}`);
  console.log(problems.length ? `${problems.length} blocker(s)` : "release pin ok");
  process.exit(problems.length ? 1 : 0);
}
