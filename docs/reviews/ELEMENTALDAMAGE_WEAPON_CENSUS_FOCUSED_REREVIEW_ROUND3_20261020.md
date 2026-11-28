# ElementalDamage WEAPON census — independent round-3 focused re-review (2026-10-20)

**Lead:** Engineering Auditor; **support:** Release Auditor / operator-completeness lens.  
**Round-3 correction verdict:** **PASS** on both requested residual issues, R2-F2A and R2-F2B.  
**Overall integration verdict:** **HOLD — new F5 (P1) source-verified, reproduced offline: Stage A can still certify an incomplete dynamic-element weapon population after an edit between the second inventory scan and the filtered cross-check.**

| Field | Verified |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Fable implementation branch | `claude/elemental-damage-weapon-census-235ynv` |
| Frozen reviewed head | `8b5bf9d87ca46f84027c702bdff86a30338c7ddb` |
| Previous review target | `5b60f840f1a9e614f521ef2e4749967053759418` |
| Previous ChatGPT review | `chatgpt/review-elementaldamage-census-round2-20261020@e2fc3c20d927ff521523cd04af13f64c91935dda` |
| Current main | `02a288e966db27f427508734a6223e0e583b081a`; merge-base is exact main; branch 4 ahead / 0 behind |
| This round's diff | Only `scripts/elementaldamage_census_ledger.py`, `scripts/test_elementaldamage_census_ledger.py`, and implementation handoff (one commit) |
| Immutable Forge sources | `forge/src/runner/census.mjs` blob `c7296d48e5396e11d46ba145bc5cd417d3d15c54`; `forge_bundle.js` blob `549751e8e2c3f1ff4b81391d88d15fd5e4d0a906`, both identical to round 2 |
| Live requests / writes | **0 / 0**; no live game, credentials, browser or mutation |

## R2-F2A — CLOSED: independently verified Stage A evidence / COMPLETE

Inspected `scripts/elementaldamage_census_ledger.py:75-99,229-277,394-406` at the frozen head:

- The Python port of Forge `stableStringify`/FNV-1a 32-bit uses JS-compatible UTF-16 code units and sorted object keys. It checks its recomputed projection digest against `census.digest` and **both** scans, and checks scan/page row totals, tagged/malformed counts, cross-check membership/counts and empty inventory problems.
- `complete` now unconditionally requires `inventory == "COMPLETE"`, a matching ledger and bundle verdict of COMPLETE, and no validation errors. An inventory of `UNSTABLE` or `FAILED` cannot yield COMPLETE, even with an otherwise successful point-body set.
- Tests in `scripts/test_elementaldamage_census_ledger.py:267-349` cover the original inventory flips, 12 one-field mutations, projection corruption and an honest partial UNSTABLE bundle. The `reseal()` helper recomputes consistent fixture digests for targeted negative cases.
- Independently recomputed the shipped fixture's FNV from its 9 projection rows with the exact source JS algorithm: **`fnv1a32:7adbde6b`**, matching census and both scan digests. An extra independent Unicode/emoji JSON example produced matching Node and Python digests.

This closes the specific false-green ledger invariant identified in the previous review. Independent local execution of the full project suites was not available through the GitHub-only source connection.

## R2-F2B — CLOSED: malformed evidence beats candidate classification

Inspected `scripts/elementaldamage_census_ledger.py:362-376`: after capture problems, `reason == "effectsMalformed"` now selects MANUAL REVIEW **before** Stormrender, formula-candidate and control statuses, without losing individual effect classifications or the separate Stormrender staged marker. `scripts/test_elementaldamage_census_ledger.py` exercises a genuine `elementaldamage` formula member next to an untyped member, confirms `manualReview`, excludes it from `candidates`, and requires non-COMPLETE overall status. The previous classification-precedence defect is closed.

## NEW F5 — P1: post-scan exact tag appearance is misreported as harmless filterOnly

**Safety invariant:** a filtered cross-check that provides **positive evidence of a new exact `elementaldamage` tag** on an inventoried WEAPON must not allow a green COMPLETE census which fails to capture that weapon. The dual unfiltered scans only establish stability *during those scans*. A later filtered read must not contradict them silently.

**Relevant code:**
- `forge/src/runner/census.mjs:159-173` obtains two stable unfiltered scans, then the filtered `item.getAll` scan. The `exact` IDs are taken solely from the **earlier** projection.
- `:174-188` builds `filterOnly` using filtered **IDs** absent from the earlier `exact` list. The filtered scan already contains per-row `effectTypes`, but that richer evidence is never compared against the earlier row. The only blocking conditions are `missedByFilter` and `notInInventory`.
- `:189-199` then uses only the earlier projection to set `tagged` and Stage B `targets`, permitting inventory COMPLETE. `forge/src/storage/journal.mjs:84-95` can call a zero-target census COMPLETE.
- `scripts/elementaldamage_census_ledger.py:253-265` accepts `filterOnly` IDs as long as they are not tagged in the **earlier inventory**, and the filtered-row count balances; no filtered projection rows are exported for it to detect the contradiction later.

**Exact-source offline reproduction performed independently:**
Loaded the frozen `forge/src/runner/census.mjs` source (GitHub blob above) and executed its original `runInventory` in an isolated JS runtime with public-query procedure stubs, actual stableStringify/FNV implementations, and a deterministic read-only synthetic `item.getAll` page provider. No production requests.

1. Begin with one visible WEAPON, `id:"weapon-tag-added-after-scans"`, `effects:[{type:"damage"}]`, `updatedAt:17:00`.
2. Both unfiltered scans return this unchanged row, including empty hidden:true pages, and agree.
3. Immediately before the **first filtered cross-check page**, simulate an unrelated content editor changing the same weapon to `effects:[{type:"elementaldamage",calculation:"formula",power:30}]` with `updatedAt:17:01`.
4. The actual `runInventory` returns:
   - `inventory:"COMPLETE"`
   - `counts: {"hidden:false":1,"hidden:true":0,"total":1,"tagged":0,"malformed":0}`
   - `targets:[]` (no full-body reads)
   - `crossCheck: {"filteredRows":1,"filterOnly":["weapon-tag-added-after-scans"],"missedByFilter":[],"notInInventory":[]}`.
5. The game source at the adopted pin confirms the filter is broad JSON_SEARCH and `item.getAll` rows include `effects`; the filtered row demonstrably contains an exact `type:"elementaldamage"`, not a harmless description-only match. Nothing in Forge or the new ledger rejects the contradiction. This is a real **false-COMPLETE** path, conditional on a concurrent item edit at a specific point, not a claim it has occurred in production.

**Practical consequence:** a WEAPON that gains the dynamic tag while the census is running may be missing entirely from the full-body captures and downstream candidate ledger despite a green COMPLETE status. The operator cannot guarantee other content editors make no changes to production even when following the no-edit instructions.

**Smallest correction:** while processing filtered cross-check results, compare each returned row's projection to the original unfiltered inventory row with the same ID, at minimum `updatedAt` and exact `effectTypes`. Reject an unexpected change as **UNSTABLE/FAILED**, never harmless `filterOnly`. Preserve the valid case of unchanged non-tagged records appearing in JSON_SEARCH because another string field matches `"elementaldamage"`. Add a deterministic Forge regression test using `FakeGame.onCall` to edit an existing untagged WEAPON immediately before the filtered cross-check, then assert no COMPLETE, zero Stage B point reads and a named mismatch; keep a benign description-string filterOnly control test. No need to change the new F2 ledger logic if Forge stops this before claiming COMPLETE.

## Verification and boundaries

The author reports **679/679 Forge tests**, **38/38 total Python tests**, reproducible bundle/fixtures/dist, limits **427,610 / 432,000 raw**, **103,015 / 105,000 gzip**, clean release-pin/boundaries/imports, and validation 0/0 for both `push/131` and `push/132`. The reviewer verified source SHA boundaries, exact changed files, test assertions, contract/source identity and the fixture digest; **did not rerun** the complete local Forge/Python suites. No pull-request CI runs were returned for this frozen census head. The isolated JS reproduction of F5 is an additional independently executed synthetic code-path test, not a game request.

**Verdict:** R2-F2A and R2-F2B **CLOSED**. Recommend **HOLD** overall until F5 is corrected and returned at a new frozen exact SHA with the targeted regression plus full mandated gates. This finding can be repaired narrowly by Fable on its own implementation branch. Do not modify or merge this review branch as code. The director retains all live-game actions. Forge 0.9.0 is not released; push/132 has not been run. **Live requests/writes: 0/0; credentials none.**
