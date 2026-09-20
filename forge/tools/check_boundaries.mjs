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
//      of the contract and the provenance is a fiction. The research registry declares the same pin,
//      because a registry row's source audit is only as good as the commit it was read at.
//   4. PRESENTATION CONTAINMENT. forge/presentation/ is repository-side tooling and must stay out
//      of the userscript: nothing under src/ may import it, so it cannot reach the bundle by an
//      import edge, and nothing in it may issue a request, because a dossier is built from
//      committed evidence and a tool that can fetch is a tool that can be pointed at the game.
//      It may read src/ - reusing the runner's image-pack contract is the point of one owner per
//      contract - but never the other way round.
//   5. THE VIEW REACHES NO RAW RESEARCH DATA. A screen renders state and invokes core actions. It
//      may not pull a response body out of capture storage, drive the budgeted reader, or hold a
//      transport client: all three route a read around ForgeCore, and the third also routes it
//      around the auth gate and the budget. Metadata listings (cache.list, cache.listSnapshots)
//      stay allowed - they return no `data` and the Captures screen is built on them.
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

// Property 5. Each entry is one way a view could get at raw research data or at the transport that
// produces it, matched on the member access rather than on a variable name, so renaming the handle
// does not evade it. `cache.get(` is in the list because it returns a cached response BODY; the
// listings beside it do not and are deliberately absent.
const VIEW = ["ui", "hosts"];
export const VIEW_FORBIDDEN = [
  [/\.\s*getSnapshot\s*\(/, "reads a capture snapshot body out of storage"],
  [/\.\s*getQuery\s*\(/, "reads a cached query body out of storage"],
  [/\.\s*putSnapshot\s*\(/, "writes a capture snapshot directly"],
  [/[Cc]ache\s*\.\s*(get|put|putQuery)\s*\(/, "reads or writes a cached response body directly"],
  [/\breader\s*\.\s*(get|getMany|list|query)\s*\(/, "drives the budgeted reader directly"],
  [/\bclient\s*\.\s*(batch|call)\s*\(/, "constructs a transport call directly"],
];

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
    if (VIEW.includes(top)) {
      for (const [re, what] of VIEW_FORBIDDEN) {
        if (re.test(code)) findings.push(`${rel}: ${what}; a screen goes through a ForgeCore action`);
      }
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
  // The research registry audits every row at a named commit. Read as text rather than imported so
  // the gate stays a static check over source, like the two above it.
  const reg = readFileSync(join(SRC, "research", "registry.mjs"), "utf8").match(/REGISTRY_PIN\s*=\s*"([0-9a-f]{40})"/);
  pins["research/registry.mjs"] = reg ? reg[1] : null;
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
