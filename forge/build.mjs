#!/usr/bin/env node
// Bundle src/main.mjs into ../forge_bundle.js as a single IIFE the loader can @require.
// superjson and its two dependencies and the pinned field list are bundled in; nothing is fetched at runtime except
// the app's own API calls.
//
// The built text is then stripped of comments (tools/strip_comments.mjs) and PROVEN equivalent to
// the unstripped build before it is written: see the oracle below. The source keeps every comment;
// only the artifact the operator downloads is comment-free.
import { build, transform } from "esbuild";
import { readFileSync, writeFileSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { stripComments } from "./tools/strip_comments.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const out = join(here, "..", "forge_bundle.js");
const pkg = JSON.parse(readFileSync(join(here, "package.json"), "utf8"));
const banner = `// TNR forge bundle v${pkg.version} - full-page content builder, loaded via @require by forge_loader_user.js.
// Built from forge/src by forge/build.mjs (esbuild, IIFE). Do not edit by hand.
// Comments are stripped from this artifact by forge/tools/strip_comments.mjs and the strip is proven
// equivalent to the unstripped build at build time; every comment is still in forge/src.
// Entry: /forge (a providerless 404) arms the tab and hands off; Forge then mounts as an overlay on a
// real application route so ClerkProvider and the tRPC provider stay alive under it. Layers: storage, transport, budget, runner, reconcile, ui.
// Pinned engine facts: studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9.`;

// Built WITHOUT the banner: the banner is itself a comment and must survive the strip, so it is
// prepended afterwards rather than fed through it.
const built = await build({
  entryPoints: [join(here, "src", "main.mjs")],
  bundle: true,
  format: "iife",
  platform: "browser",
  target: ["firefox115"],
  minify: false,
  sourcemap: false,
  legalComments: "none",
  write: false,
  outfile: out,
  define: { "process.env.NODE_ENV": '"production"' },
});
const original = built.outputFiles[0].text;
const stripped = stripComments(original);

// THE ORACLE. esbuild's own parser decides whether the strip changed anything but comments and
// whitespace: minifyWhitespace removes comments and normalises layout, so two texts that differ
// only in comments normalise to the identical string. If they do not, the stripper mis-read
// something - a regex as a division, a comment marker inside a template - and the build stops
// rather than shipping a bundle nobody proved. This is what makes a hand-written tokenizer an
// acceptable thing to put between src/ and the operator's browser.
const norm = async (text) => (await transform(text, { minifyWhitespace: true, legalComments: "none" })).code;
const [a, b] = await Promise.all([norm(original), norm(stripped)]);
if (a !== b) {
  let i = 0;
  while (i < a.length && i < b.length && a[i] === b[i]) i++;
  throw new Error(
    "comment strip changed the program. First divergence at normalised offset " + i + ":\n" +
    "  unstripped: " + JSON.stringify(a.slice(Math.max(0, i - 80), i + 80)) + "\n" +
    "  stripped:   " + JSON.stringify(b.slice(Math.max(0, i - 80), i + 80)),
  );
}

const text = banner + "\n" + stripped;
if (/\.innerHTML\s*=/.test(text) || /\binnerHTML\s*[:=]/.test(text.replace(/\/\/[^\n]*/g, ""))) {
  // repo law: no innerHTML. Fail the build rather than ship it.
  const idx = text.search(/innerHTML/);
  throw new Error("innerHTML found in bundle near: " + text.slice(Math.max(0, idx - 120), idx + 60));
}
writeFileSync(out, text);
console.log(`wrote ${out} (${(statSync(out).size / 1024).toFixed(1)} KB)`);
