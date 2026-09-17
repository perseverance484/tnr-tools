// Bundle size budget, raw and deterministic gzip.
//
// The budget is a ratchet, not a limit discovered after the fact: it is committed alongside the
// measurement it was set from, so a size regression fails CI on the commit that caused it instead
// of being noticed a release later. Deterministic gzip (-9, no timestamp) so the number is
// reproducible across runs and machines.
//
// Raising the budget is allowed and is meant to be a deliberate, reviewed edit of this file.

import { readFileSync, statSync } from "node:fs";
import { gzipSync } from "node:zlib";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const BUNDLE = join(dirname(fileURLToPath(import.meta.url)), "..", "..", "forge_bundle.js");

// Measured at the Phase 0 freeze by this tool: raw 413,323 / gzip 77,998. (zlib's gzipSync and the
// gzip(1) CLI differ by a few bytes of header; this tool's number is the one the budget tracks.)
// Fresh-main baseline before Phase 0 was raw 404,594, so the extraction cost ~8.7 KB raw for the
// core modules, the host adapter, the repo-text store and the runner emitter.
//
// PHASE 1 RAISE. Integrated Phase 0 shipped at raw 417,370 / gzip 79,294, ~97% of the 430,000 /
// 81,000 ceilings above. Phase 1 measures raw 446,372 / gzip 87,450: a delta of +29,002 raw and
// +8,156 gzip. Where it went, measured rather than estimated:
//
//   ~24.6 KB raw   src/research/registry.mjs, which is new. It holds fifteen audited rows with their
//                  source provenance and demand, the per-row input contracts that make a read
//                  validated-before-transport, the projection engine and the paging contract. Its
//                  comment density is 48%, in line with storage/captures.mjs at 50%, and the build
//                  does not minify - so the file is large because the registry is, not because the
//                  prose is unusual for this codebase.
//   ~4.4 KB raw    tier handling spread across reader, manifest, runner, results, journal and the
//                  two screens that report a tier.
//
// The new ceilings keep the SAME tightness Phase 0 ran at rather than buying comfortable room:
// 446,372 / 460,000 is 97.0% and 87,450 / 90,000 is 97.2%, against Phase 0's 97.1% and 97.9%. A
// structural regression still trips the gate on the commit that causes it, which is the whole point
// of a ratchet. This raise is isolated in its own commit so it can be reviewed as the policy change
// it is rather than as a line inside a feature.
//
// RE-REVIEW CORRECTION RAISE. The FN3-R1/FN4-R1/FN4-R2 corrections measure raw 453,086 / gzip 89,296
// against the 460,000 / 90,000 ceilings above: 98.5% and 99.2%. Passing, but 704 bytes of gzip
// headroom is a tripwire rather than a ratchet - the next one-line comment would fail CI on a gate
// that exists to catch STRUCTURAL regressions, and a control that cries wolf gets raised in a hurry
// by whoever is unblocking a build. Raised deliberately here instead, in its own commit.
//
// The delta is small and measured: +6,714 raw / +1,846 gzip over the previous correction pass, for
// the overlap check in validateProjection, the complete policy-facts derivation the registry
// revision is now taken over, and the capture-time policy stamp on summary and abandoned records.
//
// New ceilings restore the tightness Phase 0 and the first correction ran at: 453,086 / 466,000 is
// 97.2% and 89,296 / 92,000 is 97.1%, against Phase 0's 97.1% / 97.9%.
export const BUDGET = { raw: 466_000, gzip: 92_000 };

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
