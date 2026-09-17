// Mechanical import-direction gate.
//
// Required direction, one way only:
//
//     execution (runner, storage, transport, budget, reconcile, research)
//         ↓
//     core
//         ↓
//     ui / hosts
//
// An execution layer that imports a view cannot be driven by a second shell or a headless host; a
// core that imports a view is a core in name only. Both are easy to reintroduce by accident during
// a refactor and neither shows up as a failing behaviour test, so the direction is checked rather
// than trusted. The gate reports the whole population it scanned, so "zero violations" is a
// measurement and not an absence of evidence.

import { readdirSync, readFileSync } from "node:fs";
import { join, dirname, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

const SRC = join(dirname(fileURLToPath(import.meta.url)), "..", "src");

// `research` is the Phase 1 research-read registry: product/privacy admission and persistence tier,
// deliberately a layer of its own rather than a second opinion inside transport/. It sits in
// execution because that is what it governs, and because putting it here means a view that imports
// it is a violation like any other.
const EXECUTION = ["runner", "storage", "transport", "budget", "reconcile", "research"];
const VIEW = ["ui", "hosts"];

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true })
    .flatMap((d) => (d.isDirectory() ? walk(join(dir, d.name)) : [join(dir, d.name)]))
    .filter((f) => f.endsWith(".mjs"));
}

const layerOf = (file) => relative(SRC, file).split(sep)[0].replace(/\.mjs$/, "");

function importsOf(text) {
  const out = [];
  let m;
  // `import x from "y"` / `export { a } from "y"`
  const named = /(?:^|\n)\s*(?:import|export)[^;\n]*?from\s*["']([^"']+)["']/g;
  while ((m = named.exec(text))) out.push(m[1]);
  // `import "y"` — a side-effect import names no binding but creates the same edge, and a graph
  // that misses it will happily report zero violations while a view is being pulled into the
  // runner. Found by independent review (F2); the red test below injects this exact form.
  const sideEffect = /(?:^|\n)\s*import\s*["']([^"']+)["']\s*;?/g;
  while ((m = sideEffect.exec(text))) out.push(m[1]);
  // `import("y")` / `await import("y")`
  const dyn = /import\(\s*["']([^"']+)["']\s*\)/g;
  while ((m = dyn.exec(text))) out.push(m[1]);
  return out;
}

/** Resolve a relative specifier to its layer, or null when it leaves src/. */
function targetLayer(file, spec) {
  if (!spec.startsWith(".")) return null;
  const resolved = join(dirname(file), spec);
  const rel = relative(SRC, resolved);
  if (rel.startsWith("..")) return null;
  return rel.split(sep)[0].replace(/\.mjs$/, "");
}

export function checkImports() {
  const files = walk(SRC);
  const violations = [];
  let edges = 0;

  for (const file of files) {
    const from = layerOf(file);
    const text = readFileSync(file, "utf8");
    for (const spec of importsOf(text)) {
      const to = targetLayer(file, spec);
      if (!to || to === from) continue;
      edges++;
      const shown = relative(SRC, file);
      if (EXECUTION.includes(from) && VIEW.includes(to)) {
        violations.push(`${shown} (execution) imports ${spec} (${to}); execution must not know about a view`);
      } else if (from === "core" && VIEW.includes(to)) {
        violations.push(`${shown} (core) imports ${spec} (${to}); the core must not know about a view`);
      }
    }
  }

  return { files: files.length, edges, violations };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const { files, edges, violations } = checkImports();
  console.log(`import-direction: ${files} modules, ${edges} cross-layer imports scanned`);
  for (const v of violations) console.error("  VIOLATION " + v);
  console.log(violations.length ? `${violations.length} violation(s)` : "0 violations");
  process.exit(violations.length ? 1 : 0);
}
