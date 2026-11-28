# ElementalDamage WEAPON Census — focused independent re-review, round 2

**Date:** 2026-10-20  
**Lead:** Engineering Auditor · **Supporting lens:** Release Auditor  
**Verdict:** **HOLD — F1, F3 and F4 CLOSED; F2's original counterexample CLOSED, but its independent ledger completeness invariant is NOT fully closed.** Two small residual ledger corrections are needed before the census branch is recommended for integration or operator execution.

| Field | Verified |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Implementation branch | `claude/elemental-damage-weapon-census-235ynv` |
| Frozen round-2 target/head | `5b60f840f1a9e614f521ef2e4749967053759418` |
| Round-1 target (rebased away) | `0dd1d43a2430995be97bb20ee5dbcddd0eedf434` |
| Round-1 review | `chatgpt/review-elementaldamage-weapon-census-20261020@3a30a604399d3b179b17f7cc3e833e985f72afd6` |
| Current `main` | `02a288e966db27f427508734a6223e0e583b081a` — PR #76 merged, Forge 0.8.1 released |
| Branch relative to main | 3 commits ahead / 0 behind; merge-base `02a288e966db27f427508734a6223e0e583b081a` |
| Source pin | `studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb`; item router/validator, combat validator and elemental selection have same Git blobs at Forge pin `85cecaebf4ada2e265a18a1405f63c9637443275` |
| Live requests / writes | **0 / 0**; no credentials, no game execution |
| Reviewer execution | GitHub connector source/fixture/code-path verification only; no local repo clone, npm/Python tests, mobile browser or live checks |

## Round-1 corrections independently confirmed

**F1 — CLOSED (census inclusion / verdict).** `forge/src/runner/census.mjs:72-89` now marks effects malformed if the array itself is invalid **or any member** lacks a nonempty string type. `:194-197` adds that row to point-read targets, and `acceptPoint` retains its body as evidence. `forge/src/storage/journal.mjs:84-95` reports AMBIGUOUS (not COMPLETE) once all reads finish if any target was malformed. Forge tests in `forge/test/census.test.mjs:95-107,183-235` cover `[null]`, untyped objects, bare strings and a genuine tagged effect accompanied by an untyped member. The original silent-omission path no longer survives.

**F3 — CLOSED (Stage A operator Pause).** `forge/src/runner/census.mjs:99-107,129-160,171-172` invokes an optional checkpoint before *each* list page in scan 1, scan 2 and filtered cross-check. `forge/src/runner/runner.mjs:913-930` checks `pauseRequested` and throws `Paused("USER")`, renewing the lease otherwise, before inventory is journaled. `forge/test/census.test.mjs:407-448` covers all three phases and zero-target pause; resumption starts from cursor 0.

**F4 — CLOSED (integration).** The branch is based exactly on released `main@02a288e9` with the two rebased census commits and one correction commit. The contract regeneration from PR #76 remains on `main` (Forge fields/nested pinned to 85cecae); the 0.9.0 branch loader retains released `@version 0.8.1` and immutable `@require d91c0878...`, with `@x-release-pending 0.9.0`. `docs/RULINGS.md` preserves adoption `RUL-2026-10-20-001` and assigns the census bundle budget its unique `RUL-2026-10-20-002`; `forge/tools/check_bundle_budget.mjs` reflects 432,000/105,000. `push/131` remains suggestion-only and `push/132` is a census-only manifest. No new conflict with PR #76 was identified.

**F2 original negative test — CLOSED, but the broader gate is not.** `scripts/elementaldamage_census_ledger.py:185-201,216-273` now recomputes the expected target set/reasons/timestamps and demands a tagged point still contain the exact effect. It rejects duplicate or extra point reads, compares captured effect types with projection at equal `updatedAt`, and computes its own point verdict. The new negative tests `scripts/test_elementaldamage_census_ledger.py:178-251` cover the reviewer's original missing-tag counterexample and the added malformed-target case.

## Residual finding R2-F2A — P2 confirmed defect: incomplete/contradictory inventory can still become ledger COMPLETE

**Invariant:** the independent ledger must not certify a census whose **Stage A inventory** is not COMPLETE or whose recorded scan/projection evidence disagrees. The director must not be given a green ledger from untrustworthy inventory metadata.

**Reproduction from the committed green fixture (source-path replay):**
1. Start with `forge/test/fixtures/census/elementaldamage_bundle.json`, whose census is `inventory:"COMPLETE"`, `verdict:"COMPLETE"`, two matching scan digests, 9 projected weapons and 8 accepted point bodies.
2. Change **only** `bundle.census.inventory` to `"UNSTABLE"` (or `"FAILED"`), leaving the rest unchanged.
3. In `scripts/elementaldamage_census_ledger.py:202-215`, the only condition that checks scan agreement is now skipped because it is conditional on `inventory == "COMPLETE"`. `:323-331` computes `own="COMPLETE"` from point bodies and selects `complete = own == "COMPLETE" and verdict == "COMPLETE" and not errors`, **without requiring inventory COMPLETE**. Thus this inconsistent input is classified as `ledger.status:"COMPLETE"` by the inspected code path.

A second one-field counterexample changes only `bundle.census.digest` from `fnv1a32:7adbde6b` to any other string; `build_ledger` never compares that value with the scan digests or recomputes the projection fingerprint, so the same code path still certifies COMPLETE. `counts.tagged`, `counts.malformed`, scan row totals and `crossCheck.missedByFilter/notInInventory` are likewise not verified as completeness preconditions. These are not claims that Forge itself emits inconsistent bundles; they are the very inconsistent/corrupt exported-evidence class for which the **offline independent verifier** exists.

**Practical consequence:** a damaged or partially rewritten bundle could receive a green candidate ledger despite failing the exhaustive-inventory evidence gate. This is a P2 offline-certification defect, not a live-write or direct player-data corruption defect.

**Minimal correction:** require `census.inventory === "COMPLETE"` as an unconditional COMPLETE precondition. Check the Stage-A summary against the exported projection: scan fingerprints (and, preferably, independently recomputed FNV1a from canonical rows), scan and page counts, tagged/malformed counts, cross-check miss lists and `census.problems`. Match the ledger's own overall verdict to the exported verdict without exempting incomplete inventories. Test one-field mutations of a valid fixture: `inventory`, `digest`, `scans[i].rows`, `counts.tagged/malformed`, and nonempty cross-check miss list must all exit nonzero / never say COMPLETE. Preserve honest AMBIGUOUS/UNSTABLE/FAILED/INCOMPLETE evidence as usable *partial* ledgers.

## Residual finding R2-F2B — P2 needs refinement: mixed malformed rows enter candidate list rather than manual-review list

**Invariant:** a census target classified as `reason:"effectsMalformed"` remains explicitly manual/ambiguous in the ID-keyed ledger, even if another effect member looks like a formula-scaling candidate.

**Source-path counterexample:** a weapon stores `effects:[{type:"elementaldamage", calculation:"formula"}, {power:1}]`. Stage A correctly classifies this row `effectsMalformed` and the global verdict AMBIGUOUS. But `scripts/elementaldamage_census_ledger.py:290-308` assembles `classes = ["formula / both missing"]` from the valid elementaldamage member and tests for candidate classes at `:303` **before** testing `reason=="effectsMalformed"` at `:305`. It therefore labels this ambiguous target `CANDIDATE` rather than `MANUAL REVIEW`, contrary to the correction handoff's explicit malformed-target rule. The new ledger mixed-malformed negative control uses an ordinary damage member, so it misses this precedence case.

**Practical consequence:** a malformed record may appear in the director's candidate shortlist even while the overall census says AMBIGUOUS. The STOP gate still prevents automatic repairs, so this is lower severity, but it is avoidable operator confusion.

**Minimal correction:** prioritize `reason == "effectsMalformed"` before any candidate or control classification (while retaining Stormrender's separate staged marker). Add a ledger test for a valid dynamic elementaldamage member beside an untyped member and assert `manualReview` contains the ID, `candidates` does not, and global status is NOT COMPLETE.

## Remaining limits / next workflow step

The author reports **679/679 Forge tests**, **32/32 Python ledger tests**, 0-error manifest gates for push/131 and push/132, reproducible bundle/fixtures/dist, and budget **427,610/432,000 raw, 103,015/105,000 gzip**. I inspected the test implementations, frozen contracts, loader and ruling state. I **did not independently run** those suites; no pull-request CI result was returned for this branch head. Browser/mobile rendering, SuperJSON decoding, production hidden-partition behaviour and IndexedDB space remain unverified. They are not substituted with a production experiment.

**Verdict: HOLD.** F1/F3/F4 can receive a narrow closed finding in the next review. Fable owns the two residual ledger changes and their adversarial tests on the implementation branch. Return one new frozen SHA with Python tests, Forge tests, fixture/build/size/release-pin and both manifest gates. Do not merge this ChatGPT review branch as implementation. Do not run the game census #132 or any repair/suggestion. No live requests/writes authorized.
