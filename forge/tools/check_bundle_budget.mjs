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
// Headroom is ~4%: enough for ordinary change, small enough that a structural regression trips it.
export const BUDGET = { raw: 430_000, gzip: 81_000 };

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
