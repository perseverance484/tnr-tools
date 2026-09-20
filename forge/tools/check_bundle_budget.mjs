// Bundle size budget, raw and deterministic gzip.
//
// The budget is a ratchet, not a limit discovered after the fact: it is committed alongside the
// measurement it was set from, so a size regression fails CI on the commit that caused it instead
// of being noticed a release later. Deterministic gzip (-9, no timestamp) so the number is
// reproducible across runs and machines.
//
// Raising the budget is allowed and is meant to be a deliberate, reviewed edit of this file.
//
// ---- history -------------------------------------------------------------------------------
//
// Phase 0 freeze:            raw 413,323 / gzip 77,998   ceiling 430,000 / 81,000
// Godstorm defects repair:   raw 424,642 / gzip  81,344  ceiling stepped (gzip went 344 over)
// Repo-backed image packs:   raw 447,540 / gzip  86,927  ceiling stepped
// image-pack review F1/F2:   raw 451,847 / gzip  88,356  ceiling stepped AGAIN, to 470,000 / 92,000
//
// That second step inside one feature left the bundle at 96.1% raw and 96.0% gzip and is what the
// reviewer objected to: two raises for one feature is a signal, not a measurement. The standing
// question - whether Forge needed a size pass rather than another ceiling - was recorded as open
// and is now answered below.
//
// ---- the size pass (Forge Presentation Studio P0) --------------------------------------------
//
// Three changes, no behaviour change, measured by this tool:
//
//   1. nested.json stores its 165 allowed key sets as 53 distinct ones named by index instead of
//      165 literal arrays. Same contract, proven by digest against the pre-compaction content
//      (test/runner.test.mjs); the bundle stopped carrying the same twenty key names seventy-six
//      times.                                                   raw 451,847 -> 373,903  (gzip -255)
//   2. Comments are stripped from the ARTIFACT at build time and the strip is proven equivalent to
//      the unstripped build by esbuild's own parser (build.mjs). esbuild at minify:false drops
//      `//` comments but keeps every `/** */` block, so ~34 KB raw of JSDoc that nothing at runtime
//      reads was being shipped. forge/src keeps every word of it - this is the opposite of moving
//      explanatory comments out of the code to save bytes.       raw 373,903 -> 339,690  (gzip -13,175)
//   3. Dead exports removed (isRef, hasRefLiteral, POOL_META) and the results-bundle filename,
//      which existed twice, now has one owner.                   raw 339,690 -> 339,669
//
// Net: raw 451,847 -> 339,669 (-24.8%), gzip 88,356 -> 74,926 (-15.2%). The ceiling below is set
// from THAT measurement at the ~4% headroom the Phase 0 freeze used, so it is a ratchet against
// the reduced product rather than a ceiling raised to fit the old one.
//
// NOT taken, and deliberately left as a decision rather than made here: full esbuild minification
// measures raw 261,029 / gzip 61,525 on this build, and whitespace-only minification 301,678 /
// 67,770. Either would buy far more headroom than the pass above, and both make the shipped
// artifact unreadable. In a repository whose whole model is that the committed artifact can be
// audited, that is a product decision for the director and the reviewer, not a size fix.

import { readFileSync, statSync } from "node:fs";
import { gzipSync } from "node:zlib";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const BUNDLE = join(dirname(fileURLToPath(import.meta.url)), "..", "..", "forge_bundle.js");

export const BUDGET = { raw: 354_000, gzip: 78_000 };

export function measure() {
  const raw = statSync(BUNDLE).size;
  const gzip = gzipSync(readFileSync(BUNDLE), { level: 9 }).length;
  return { raw, gzip };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const { raw, gzip } = measure();
  const pct = (n, b) => ((n / b) * 100).toFixed(1);
  console.log(`bundle: raw ${raw} / ${BUDGET.raw} (${pct(raw, BUDGET.raw)}%)  gzip ${gzip} / ${BUDGET.gzip} (${pct(gzip, BUDGET.gzip)}%)`);
  const over = [];
  if (raw > BUDGET.raw) over.push(`raw ${raw} exceeds ${BUDGET.raw}`);
  if (gzip > BUDGET.gzip) over.push(`gzip ${gzip} exceeds ${BUDGET.gzip}`);
  for (const o of over) console.error("  OVER BUDGET " + o);
  process.exit(over.length ? 1 : 0);
}
