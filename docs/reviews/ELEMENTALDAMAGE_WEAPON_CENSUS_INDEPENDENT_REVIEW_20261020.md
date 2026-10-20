# ElementalDamage WEAPON census — independent Lane A review (2026-10-20)

**Lead:** Engineering Auditor; supporting lenses: Release Auditor, operator UX. **Verdict: HOLD — corrections before integration or operator census run.** This review is not a permission to contact the live game.

| Field | Verified review target |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Implementation branch | `claude/elemental-damage-weapon-census-235ynv` |
| Frozen head | `0dd1d43a2430995be97bb20ee5dbcddd0eedf434` |
| Implementation commit | `d2dc3532bb9431d510e08ff2e4c8bed954ad3aaa` |
| Main/base | `e13bc9fa085b37bd84ab7736256da8d1ad2a4a99` (2 ahead/0 behind) |
| Owning brief | `docs/handoffs/ELEMENTALDAMAGE_WEAPON_CENSUS_CAPTURE_IMPLEMENTATION_20261020.md`, `chatgpt/elementaldamage-weapon-census-handoff-20261020@38740f228958020ec183bbf0950e288e455c5698` |
| Game-source pin (read only) | `studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb` |
| Live-game requests/writes | **0/0**; credentials **none** |

## F1 — P1 confirmed code-path defect: malformed effect-array members can disappear from the census

**Invariant:** no weapon whose effect content cannot be classified should silently disappear from the audited denominator / possible-target set. The brief requires capture of ambiguous effects and fail-closed completeness.

**Evidence:** `forge/src/runner/census.mjs:71-80` treats `Array.isArray(effects)` as the entire `effectsMalformed` predicate, and maps an array member without a valid `type` to `null`. At `:182-185`, the target set contains only arrays that have an exact `elementaldamage` string or `effectsMalformed:true`. Thus an item whose effects are `[null]`, `[{power:30}]` or `["elementaldamage"]` is considered **not malformed**, is omitted from Stage B, and can leave `COMPLETE` unchanged if the two scans and JSON_SEARCH cross-check agree. The fixture test `forge/test/census.test.mjs:95-100` even expects a null entry in projected `effectTypes` without rejecting it; `:178-188` only exercises non-array effects.

**Consequence:** a complete verdict could incorrectly certify that all relevant WEAPON effect bodies were inspected, even though a malformed potential tag was skipped.

**Smallest correction:** treat any effect-array element without a well-formed string `type` as ambiguous/malformed. Include those weapon IDs in full point captures and prevent `COMPLETE` until ambiguity is resolved explicitly. Add adversarial tests for malformed *members*, not just a malformed top-level effects value.

## F2 — P1/P2 confirmed evidence-gate defect: ledger can certify an inconsistent tagged point as COMPLETE

**Invariant:** the offline candidate ledger must recompute acceptance from the exported projection and full-body point data; it must not trust Forge's `accepted` flag or the inventory target list.

**Evidence:** `scripts/elementaldamage_census_ledger.py:196-225` checks the capture's id, `WEAPON`, `effects` array, persistence, and `updatedAt`. It **does not independently check the captured body still contains an `elementaldamage` effect for a target classified as tagged** (`target.reason`), although the live Forge `acceptPoint` does (`forge/src/runner/census.mjs:198-211`). It also does not recompute each target's reason/updatedAt from its inventory row. A manipulated/inconsistent bundle with a tagged inventory row, `data.effects:[]`, unchanged `updatedAt`, `accepted:true`, and claimed `census.verdict:"COMPLETE"` passes these offline checks and can produce `ledger.status:"COMPLETE"` despite no qualifying effect in its full body. `scripts/test_elementaldamage_census_ledger.py` has no negative test for this counterexample.

**Consequence:** ledger's promised independent verification could falsely certify evidence that no longer supports the candidate population (also possible with accidental bundle corruption).

**Smallest correction:** independently compare `target.id/reason/updatedAt` with the projected inventory row; for every target that was tagged, verify the point's effects contain the exact tag; reject unexpected/duplicate/extra census point captures and inconsistent row/capture metadata. Add corrupted-bundle negative controls. If malformed inventory targets are allowed to become well-formed non-tag points, that must be an explicit documented classification, not an implicit acceptance.

## F3 — P2 operator-control defect: Pause is not honored during Stage A

**Invariant:** the operator can stop a potentially lengthy read-only census at a safe page boundary; Stage A can restart from zero on resume as deliberately designed.

**Evidence:** `runner.mjs:242` sets `pauseRequested`, but `runInventory()/scan()/crawl()` in `runner/census.mjs:90-188` never checks it. `runner.mjs:910-942` tests the pause only in the Stage B point-read loop (`:930-931`). A Pause request during the two full unfiltered scans or filtered cross-check continues sending item.getAll requests; a zero-target census can reach DONE with no pause honored. The Pause test `forge/test/census.test.mjs:369-380` covers only Stage B.

**Consequence:** on mobile the operator may think the job stopped when it keeps reading and spending rate-budget; for a large item population this is substantial friction, though no game mutation is possible.

**Smallest correction:** before each census page read, consult the runner's pause callback and throw the ordinary `Paused("USER")`; persist no half-scan; resume from cursor zero. Add a Stage-A pause/zero-target test.

## F4 — integration blocker: colliding RULING IDs and version lines in concurrent PR #76

**Confirmed cross-branch disagreement, not a reason to discard either user decision.**

- The census branch appends `RUL-2026-10-20-001` to `docs/RULINGS.md` for the director-approved Forge bundle ceiling of 432,000 raw / 105,000 gzip.
- Concurrent PR #76 (reviewed separately at frozen `503d98d`, tip `e48d3fb`) independently appends the **same ID** `RUL-2026-10-20-001` for the director-approved full generated-contract adoption at game-source `85cecae`.
- Both branches alter `forge/package.json`, `forge/src/main.mjs`, `forge_bundle.js`, `forge_loader_user.js`, `docs/RULINGS.md`, and packaged skill artifacts. The census 0.9.0 is based on pre-PR76 Forge 0.8.0, while PR #76 stages Forge 0.8.1 with newly re-derived `fields.json`/`nested.json`/45x contracts.

**Consequence:** merging the census branch independently or selecting one side of the RULINGS conflict would overwrite valid decision history or regress a reviewed Forge safety re-pin; installed loader and bundle versions can diverge.

**Correction/integration order:** first integrate the separately reviewed PR #76 through its normal release/pin process; then Fable rebases the census implementation on current `main`, preserves 0.8.1 contract and security changes, retains 0.9.0 as the prospective next release, renumbers the census size ruling to a new unique ID and updates every reference, updates the docs and ledger's stale 'PR #73 blocked' status (PR #76 supersedes #73), and re-runs complete build, budget, tests, fixture, manifest and skillpack gates. Return a new frozen head for focused re-review of F1–F4 and integration seams.

## What held up

- The checked pinned TNR source confirms public `item.getAll` with `{itemType,hidden,limit,cursor}`, offset pagination ordered by cost/repsCost/id and `nextCursor` behavior, and the public `item.get` point read; `itemDatabaseFilter` defaults omitted hidden to false and implements `effect` through broad JSON_SEARCH. The narrow dual-partition unfiltered scans plus *cross-check only* filtered scan are appropriate.
- `forge/src/budget/reader.mjs:152-159` uses the existing budget and allows only item.getAll as a census page. `forge/src/runner/manifest.mjs:80-91` makes a census standalone and refuses mutations/suggestions. The point bodies use the existing 512-KiB full-point persistence allowlist and immutable snapshots; list responses keep only a narrow projection.
- Stable rescans, explicit page-failure/duplicate-ID refusals, `updatedAt` drift handling and absence of automatic repair/suggest/edit operations are well designed. Tests cover per-path limits, 429, resume, missing/oversized snapshots, source-like pagination, and no mutations.
- The ledger differentiates missing/empty stat selectors from nonempty `["None"]`, classifies multiple dynamic tags independently, and marks Stormrender separately from new candidates. Candidate generation does not confer operator approval.

## Verification / boundaries

Code and pinned game-source files, operator workflow/brief, actual tests and generated fixture were read via the GitHub repository connector at frozen SHAs. The author reports `npm test` **667/667**, Python ledger tests **17/17**, bundle/fixture and skillpack reproducibility, `validate.py push/132` 0/0, and size budget 424,212/432,000 raw, 102,630/105,000 gzip. **No local npm or Python suite was independently executed** in this GitHub-connector review; there was no matching CI run returned for the census head. No production/browser/mobile checks were performed. Deployment of the pinned TNR source, hidden:true visibility, SuperJSON date handling, IndexedDB quota and mobile layout remain **unverified**, not implicit approvals.

**Verdict:** HOLD for census branch integration/operator run pending F1–F4 correction and new exact frozen SHA. The PR #76 round-two review is a separate PASS WITH NOTES; integrate that reviewed contract dependency first. Nothing in this report authorizes the director's census, suggestion, publishing or any live-game action. Review branch only; do not merge it as implementation.
