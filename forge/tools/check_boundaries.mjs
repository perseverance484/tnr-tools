// Static boundary gate for Forge. Three properties, all checkable without running anything:
//
//   1. NETWORK CONFINEMENT. Only the transport layer and the GitHub client may issue a request.
//      A fetch appearing in the runner, the core, storage, budget, reconcile, the UI or a host
//      adapter means some layer learned to talk to the world directly, which defeats the
//      FakeClient substitution every behaviour test depends on.
//   2. NO HARDCODED GAME HOST. Forge runs as an overlay on the game's own origin and addresses it
//      with relative paths. A literal game hostname in src is how a build starts reaching a live
//      environment from a context that was never meant to.
//   3. GENERATED-CONTRACT PIN AGREEMENT. fields.json and nested.json are derived from one pinned
//      game-source commit. If they disagree, the app is validating against two different versions
//      of the contract and the provenance is a fiction.
//   4. PRESENTATION CONTAINMENT. forge/presentation/ is repository-side tooling and must stay out
//      of the userscript: nothing under src/ may import it, so it cannot reach the bundle by an
//      import edge, and nothing in it may issue a request, because a dossier is built from
//      committed evidence and a tool that can fetch is a tool that can be pointed at the game.
//      It may read src/ - reusing the runner's image-pack contract is the point of one owner per
//      contract - but never the other way round.
//
// The gate prints the population it scanned, so a clean result is a measurement rather than the
// absence of a finding.

import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join, dirname, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

const FORGE = join(dirname(fileURLToPath(import.meta.url)), "..");
const SRC = join(FORGE, "src");
const PRESENTATION = join(FORGE, "presentation");

// main.mjs is NOT here: composition INJECTS fetchImpl (win.fetch.bind(win)) and never issues a
// request itself, so allowlisting it only widened the gate for no behaviour. Removed on review.
const NETWORK_ALLOWED = ["transport", "github.mjs"];
const GAME_HOSTS = [/theninja-rpg\.com/i, /\bwww\.theninja\b/i];
// `fetchImpl` is the injected seam every layer is supposed to use; any other call is the smell.
// Both the bare form and the qualified one: the original pattern excluded anything preceded by a
// dot, so `globalThis.fetch("/api/...")` and `window.fetch(...)` sailed straight through it
// (independent review F2). `fetchImpl(` and `.fetch.bind(` are deliberately NOT matched — the
// first is the seam itself, the second is composition handing that seam over.
const FETCH_CALL = /(?:(?:globalThis|window|self|top|parent)\s*\.\s*)?(?<![.\w])fetch\s*\(|\.\s*fetch\s*\(/;

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true })
    .flatMap((d) => (d.isDirectory() ? walk(join(dir, d.name)) : [join(dir, d.name)]))
    .filter((f) => f.endsWith(".mjs"));
}

const strip = (t) => t.replace(/\/\/[^\n]*/g, "").replace(/\/\*[\s\S]*?\*\//g, "");

export function checkBoundaries() {
  const files = walk(SRC);
  const findings = [];

  for (const file of files) {
    const rel = relative(SRC, file);
    const top = rel.split(sep)[0];
    const code = strip(readFileSync(file, "utf8"));

    const mayNetwork = NETWORK_ALLOWED.includes(top) || NETWORK_ALLOWED.includes(rel);
    if (!mayNetwork && FETCH_CALL.test(code)) {
      findings.push(`${rel}: issues a request outside the transport layer`);
    }
    for (const host of GAME_HOSTS) {
      if (host.test(code)) findings.push(`${rel}: hardcodes a live game host`);
    }
  }

  // 4. presentation containment
  for (const file of files) {
    const rel = relative(SRC, file);
    const code = strip(readFileSync(file, "utf8"));
    if (/from\s*["'][^"']*\bpresentation\//.test(code) || /import\s*\(\s*["'][^"']*\bpresentation\//.test(code)) {
      findings.push(`${rel}: imports forge/presentation, which would pull repository-side tooling into the bundle`);
    }
  }
  // A tree with no presentation/ has nothing to contain, so an absent directory is zero files
  // rather than a crash - the gate is also run against synthetic roots that hold only src/ and
  // tools/. The count is returned, and presentation.boundary.test.mjs asserts it against what is
  // actually on disk, so "scanned nothing" cannot pass for "found nothing".
  const presentationFiles = existsSync(PRESENTATION) ? walk(PRESENTATION) : [];
  for (const file of presentationFiles) {
    const rel = relative(PRESENTATION, file);
    const code = strip(readFileSync(file, "utf8"));
    if (FETCH_CALL.test(code)) findings.push(`presentation/${rel}: issues a request; a dossier is built from committed evidence only`);
    for (const host of GAME_HOSTS) if (host.test(code)) findings.push(`presentation/${rel}: hardcodes a live game host`);
  }

  // pin agreement
  const pins = {};
  for (const name of ["fields.json", "nested.json"]) {
    const j = JSON.parse(readFileSync(join(SRC, "runner", name), "utf8"));
    pins[name] = (j._provenance || j._meta || {}).pin ?? null;
  }
  const distinct = [...new Set(Object.values(pins))];
  if (distinct.length !== 1 || !distinct[0]) {
    findings.push(`generated contracts disagree on their source pin: ${JSON.stringify(pins)}`);
  }

  return { files: files.length, presentationFiles: presentationFiles.length, pin: distinct[0] ?? null, findings };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const { files, presentationFiles, pin, findings } = checkBoundaries();
  console.log(`boundaries: ${files} src modules + ${presentationFiles} presentation modules scanned; generated-contract pin ${pin}`);
  for (const f of findings) console.error("  VIOLATION " + f);
  console.log(findings.length ? `${findings.length} violation(s)` : "0 violations");
  process.exit(findings.length ? 1 : 0);
}
