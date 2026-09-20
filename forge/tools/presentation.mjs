// Build and lint a presentation dossier from the container, offline.
//
//   node tools/presentation.mjs presentation/packages/godstorm/spec.json
//   node tools/presentation.mjs presentation/packages/godstorm/spec.json --json > dossier.json
//   node tools/presentation.mjs presentation/packages/godstorm/spec.json --require-exact-bytes
//
// Exits 0 when the lint has no fatal finding, 1 otherwise. It NEVER opens a socket: every source
// is a committed file under the repository root, which is the whole point of an evidence package.

import { resolve, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { buildFromSpecFile, summarize } from "../presentation/build.mjs";
import { PresentationError } from "../presentation/errors.mjs";

const ROOT = resolve(join(dirname(fileURLToPath(import.meta.url)), "..", ".."));

const args = process.argv.slice(2);
const specArg = args.find((a) => !a.startsWith("--"));
if (!specArg) {
  console.error("usage: node tools/presentation.mjs <spec.json> [--json] [--require-exact-bytes]");
  process.exit(2);
}

let built;
try {
  built = buildFromSpecFile(resolve(specArg), {
    root: ROOT,
    requireExactBytes: args.includes("--require-exact-bytes"),
  });
} catch (e) {
  if (e instanceof PresentationError) {
    console.error("REFUSED: " + e.message);
    process.exit(1);
  }
  throw e;
}

const { dossier, lint } = built;
if (args.includes("--json")) {
  process.stdout.write(JSON.stringify(dossier, null, 1) + "\n");
} else {
  console.log(summarize(dossier));
  console.log("");
  for (const f of lint.findings) console.log(`  ${f.severity.toUpperCase().padEnd(5)} ${f.code}: ${f.message}`);
  console.log(`\n${lint.fatal.length} fatal, ${lint.warnings.length} warning(s)`);
}
process.exit(lint.fatal.length ? 1 : 0);
