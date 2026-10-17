# Bloodright importer: independent-review response

The user supplied an independent review of PR #29 at
`d930c7a7a18d13a56206083f96b4a41c2a4dcb40`, dated 2026-10-08, with verdict
**READY WITH CONDITIONS**. Source: user-pasted review from
https://claude.ai/artifact/RjQvf6cRyYSYPxvx9WDWSH (the linked content itself was not accessible
from this environment). The review independently reported 546 passing tests, matching game
source and contract hashes, successful PR CI, and four lower-severity defects.

This response implements corrections on the same author-owned branch. It does not claim
independent verification of the corrected head. The new exact SHA is supplied with the PR
handoff for a focused verification pass. Game and design pins remain unchanged.

## Findings and changes

| Review finding | Disposition |
| --- | --- |
| R1, medium: a changed manifest can start over an unresolved same-bloodline job | Fixed. A shared persistent-journal guard checks SENT, ORPHANED and CONFIRMED obligations before preparation and planning, at Start, and in run/resume while holding the lease. Job provenance is stored with journal creation; scoped source IDs identify older jobs without metadata. The current job is exempt during resume. Other bloodlines and fully resolved jobs remain usable. |
| R2, low–medium: lost visibility fails items while later creates continue | Fixed. Empty own-target reads during fill or verification pause the whole job as VISIBILITY. The item retains its phase and entity ID. Restoring access resumes the same placeholder or readback; no retry create is sent. Applies to both skill records and one-phase folders. |
| R3, low: offset paging can silently skip a row during concurrent deletion | Mitigated mechanically and documented. Two complete fresh scans of both paths must agree in full; otherwise the result is refused without caching a partial inventory. This reproduces and detects the reported deletion case. The API still cannot provide an atomic snapshot under arbitrary concurrent edits. |
| R4, low: surrounding whitespace causes perpetual name drift | Fixed. Structural names and raw skill payload names with leading/trailing whitespace are refused. Existing folder names retain their server-compatible behavior. |
| Raw manifests can bypass the compiler envelope | Hardened. Skill/folder writes require valid scoped provenance and dedupNames:true; edits additionally require a preimage and matching explicit binding. Read-only captures stay available. Python manifest construction supports the prepared provenance envelope. |

The six initial regression probes failed against the reviewed implementation before fixes:
changed settings over an orphan; visibility lost during fill; visibility lost during readback;
deletion between offset pages; whitespace names; missing provenance/preimages/name checks.
Additional tests cover all three unresolved states, legacy journal metadata, other bloodlines,
already-queued jobs, and one-phase folder visibility loss. Existing tests continue to cover
recovery, parent verification, loader pins and repeat-import idempotence.

## Correction validation (2026-10-08)

| Check | Result |
| --- | --- |
| `npm --prefix forge test` (Node 24.19.0, full history) | 555 passed, zero failures/skips; 32 Bloodright tests. |
| `node forge/tools/derive_bloodright.mjs /workspace/TheNinjaRPG --check` | Byte-identical at game pin `1ccdaf078a58101872675e459c8e755b495d4c83`. |
| Forge `check_imports.mjs` / `check_boundaries.mjs` | Zero violations; legacy contract pin unchanged. |
| Forge `check_bundle_budget.mjs` | 375,119 / 386,000 raw bytes; 84,768 / 88,000 gzip bytes. |
| `node forge/build.mjs`, repeated | Identical SHA-256 `0bd1bd3c187a1a26c4c7addf7f391b4dd161e839f71e819f0e520ee03cf279da`. |
| Forge `npm run fixtures` | No fixture changes. |
| Forge `checkReleasePin()` | Clean; loader remains on 0.5.1. |
| Forge `npm audit --omit=dev --audit-level=high` | Zero vulnerabilities. |
| `factory.py --selftest` | 20/20. |
| `doctrinemap.py`, `render_doctrine.py --check`, `build_packs.py --check`, `catalog_sync.py --selftest` | Passed. |
| `lawmap.py` | Zero errors; five existing warnings (laws 16d, 18, 37, 61, 69). |
| `python3 .github/scripts/pack_skills.py`, repeated | Identical archives; updated content ZIP SHA-256 `c5dc72a4cdd688c648a80352e48cd0c39b7ca2eff9f5f7a863084d8c09dd14b9`. |
| `git diff --check` | Clean. |

For the focused independent pass, compare the new PR head against the reviewed
`d930c7a7a18d13a56206083f96b4a41c2a4dcb40`; inspect R1–R4 and the raw-manifest
guard, reproduce the regression probes, and verify generated bundle/ZIP fidelity.
The PR remains a draft. CI results and the exact frozen correction SHA are recorded in
the PR handoff, since this document is committed as part of that correction.

## Decisions retained for the user

No balance values, wording acceptance, folder visibility or release approval are inferred
from the review. The eleven missing node prices/durations remain unset; Hungry Pulse keeps
its evidenced 20 Silver / 99 rounds. Generated mechanical descriptions and the currently
visible existing folder remain previewable proposed behavior. The user was asked to confirm
these choices before the pilot.

The candidate keeps the existing proposed budget of 386,000 raw / 88,000 gzip bytes; this
correction does not raise it again. Approval of the increase over the pre-feature budget
remains a release decision explicitly requested from the user.

## Boundaries

No game requests or writes, live-session access, merge, release, refunds, deletions, or pilot
execution occurred in this correction pass. The published loader remains at 0.5.1, with
0.6.0 pending. A real browser/staff-session pilot and independent verification of these
corrections are still required. Paused jobs must be resolved explicitly; there is no automatic
cleanup, distributed lock, or server idempotency key.
