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
//
// RAISED for the Godstorm defects repair (docs/handoffs/GODSTORM_FORGE_DEFECTS_REPAIR_*). The four
// fixes - the per-procedure list-input table, the structural rules comparison, the manifest
// execution-policy identity and the image-pick contract - measured raw 424,642 / gzip 81,344,
// which put gzip 344 bytes over the old ceiling. That is ~4.9 KB raw of new code and its comments
// for four defects, not a structural regression, so the ratchet is stepped rather than the code
// squeezed to fit. Deliberate and reviewable, which is what the paragraph above asks for; a
// reviewer who disagrees should say so, because the next change inherits this headroom.
//
// RAISED for repo-backed image packs (docs/handoffs/FORGE_REPO_BACKED_IMAGE_PACKS.md). Measured by
// this tool at raw 447,540 / gzip 86,927, against 424,642 / 81,344 for the bundle on main: +22.4 KB
// raw, +5.5 KB gzip. That is three new modules and their reasoning - the manifest binding contract
// (runner/imgpack.mjs), the content-addressed asset store (storage/assets.mjs), the fetch/verify
// pass and the Start gate (core/imagepack.mjs) - plus the runner's content-keyed upload reuse and
// the provenance rows on the manifests screen. Roughly half of it is comment: these files carry the
// WHY of a provenance contract, and squeezing that out to hold a number would be the wrong trade.
// No new dependency and no new runtime code fetch; the digest is WebCrypto, from the browser.
// The ratchet is stepped to ~4% headroom, the same margin the Phase 0 freeze used, so ordinary
// change fits and a structural regression still trips it. A reviewer who wants the step smaller
// should say so, because the next change inherits this headroom.
export const BUDGET = { raw: 465_000, gzip: 90_000 };

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
