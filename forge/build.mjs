#!/usr/bin/env node
// Bundle src/main.mjs into ../forge_bundle.js as a single IIFE the loader can @require.
// superjson and its two dependencies are bundled in; nothing is fetched at runtime except the
// 45d schema file and the app's own API calls.
import { build } from "esbuild";
import { readFileSync, writeFileSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const out = join(here, "..", "forge_bundle.js");
const pkg = JSON.parse(readFileSync(join(here, "package.json"), "utf8"));
const banner = `// TNR forge bundle v${pkg.version} - full-page content builder, loaded via @require by forge_loader_user.js.
// Built from forge/src by forge/build.mjs (esbuild, IIFE). Do not edit by hand.
// Host: any unmatched path on the game origin (/forge). Layers: storage, transport, budget, runner, reconcile, ui.
// Pinned engine facts: studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9.`;

await build({
  entryPoints: [join(here, "src", "main.mjs")],
  bundle: true,
  format: "iife",
  platform: "browser",
  target: ["firefox115"],
  minify: false,
  sourcemap: false,
  legalComments: "none",
  banner: { js: banner },
  outfile: out,
  define: { "process.env.NODE_ENV": '"production"' },
});
const text = readFileSync(out, "utf8");
if (/\.innerHTML\s*=/.test(text) || /\binnerHTML\s*[:=]/.test(text.replace(/\/\/[^\n]*/g, ""))) {
  // repo law: no innerHTML. Fail the build rather than ship it.
  const idx = text.search(/innerHTML/);
  throw new Error("innerHTML found in bundle near: " + text.slice(Math.max(0, idx - 120), idx + 60));
}
console.log(`wrote ${out} (${(statSync(out).size / 1024).toFixed(1)} KB)`);
