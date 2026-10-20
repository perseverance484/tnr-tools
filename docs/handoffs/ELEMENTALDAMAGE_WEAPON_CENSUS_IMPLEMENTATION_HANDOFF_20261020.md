# Implementation handoff — elementaldamage WEAPON census (Forge 0.9.0)

**Lane:** A (Forge code/tooling). The director's later census run and ledger are Lane B.
**Implementation owner:** Fable / Claude Code. **Independent reviewer:** ChatGPT.
**Status:** ROUND 2 CORRECTED, FROZEN FOR NARROW RE-REVIEW. Do not modify this branch during review.
**Round 1 review:** `chatgpt/review-elementaldamage-weapon-census-20261020@3a30a604` (`docs/reviews/ELEMENTALDAMAGE_WEAPON_CENSUS_INDEPENDENT_REVIEW_20261020.md`), HOLD on F1–F4; corrections below. Round-1 target was `0dd1d43a`.

## Round 2 corrections (2026-10-20)

Round-2 review: `chatgpt/review-elementaldamage-census-round2-20261020@e2fc3c20` (`docs/reviews/ELEMENTALDAMAGE_WEAPON_CENSUS_FOCUSED_REREVIEW_ROUND2_20261020.md`). F1, F3 and F4 were closed; F2 was partially closed, with two residual findings. Round-2 target was `5b60f840`; base still `main@02a288e9`. Ledger only: no Forge code changed in this round.

- **R2-F2A, incomplete or contradictory inventory certified COMPLETE.**
  - Ledger COMPLETE now requires `census.inventory == "COMPLETE"` unconditionally. When the inventory is not COMPLETE, the ledger's own verdict is the inventory state (UNSTABLE/FAILED, as Forge's `censusVerdict`), and the bundle verdict must equal it in every case.
  - A COMPLETE inventory must now prove itself against the exported projection. The ledger recomputes Forge's `fnv1a32(stableStringify(rows))` independently (Python port, verified to reproduce the fixture's `7adbde6b`) and checks it against `census.digest` and both scan digests. It also checks:
    - each scan's `rows`, and its page row totals, against the inventory size;
    - `counts.tagged` and `counts.malformed` against the rows;
    - that a cross-check is present, with empty `missedByFilter`/`notInInventory`, `filterOnly` naming only untagged inventory rows, and `filteredRows` = exact + filterOnly;
    - that `census.problems` is empty.
  - Honest UNSTABLE/FAILED bundles are not held to these checks and still produce a usable partial ledger (NOT COMPLETE, exit 1).
  - Tests: the reviewer's `inventory` flip (UNSTABLE and FAILED); 12 one-field mutations (digest, scan digest, scan rows, page rows, tagged, malformed, missedByFilter, notInInventory, filterOnly, filteredRows, missing cross-check, problems); an edited projection row; and the honest UNSTABLE partial ledger.
- **R2-F2B, mixed malformed records listed as candidates.** A target whose reason is `effectsMalformed` now gets MANUAL REVIEW before any Stormrender, candidate or control status. Its `classifications` still record the observed evidence (e.g. `formula / both missing`), and Stormrender keeps its staged marker. Test: a valid formula `elementaldamage` member beside an untyped member is in `manualReview`, not in `candidates`, and the status is NOT COMPLETE.
- Test harness: `reseal()` re-derives the digests and counts after a deliberate, consistent fixture edit, so each negative test hits the rule it names. The round-1 mixed-malformed test uses it.
- All 6 new round-2 test methods (17 cases with subtests) fail against the round-2 ledger and pass now.

## Round 1 corrections (2026-10-20)

The branch was **rebased onto `main@02a288e9`** (PR #76 merged as `d91c0878`, then the release-pin auto-commit that released Forge 0.8.1). The two census commits keep their content; the conflicts were resolved as below. The correction work was taken over by a second Claude Code session, at the director's direction; the original session was idle, so the branch still has one writer.

- **F1, malformed effect members (P1).** `projectRow` now marks a row `effectsMalformed` when `effects` is not an array **or any member** is not an object with a non-empty string `type`. `[null]`, `[{power:30}]`, `["elementaldamage"]`, `[{type:""}]` and a tag next to an untyped member all qualify. Such a row is a target and its full body is captured as evidence, whatever its shape (`acceptPoint` skips the array/tag checks for it). It can never make the census COMPLETE: `censusVerdict` returns a new **`AMBIGUOUS`** verdict once every body is in and any target is malformed. Precedence: INCOMPLETE > STALE > FAILED > AMBIGUOUS > COMPLETE. The bundle outcome is `failed`. Tests: projection member cases, and four end-to-end malformed-member runs (target, point read, AMBIGUOUS, outcome failed). The old "unparseable effects" test now expects AMBIGUOUS.
- **F2, offline ledger re-verification (P1/P2).** The ledger now recomputes, rather than trusts:
  - each row's `effectsMalformed` from its `effectTypes`;
  - the target set **and each target's `reason` and `updatedAt`** from the inventory rows;
  - for a tagged target, an exact `elementaldamage` member in the captured body (the reviewer's counterexample);
  - at the same `updatedAt`, the body's effect types against the projected ones (`item.getAll` and `item.get` both return the stored row);
  - its own verdict (`ledgerVerdict`, incl. AMBIGUOUS), which must equal the bundle's.

  It refuses duplicate targets and extra or duplicate point captures. It lists `ambiguous` ids, and malformed targets go to MANUAL REVIEW. Six corrupted-bundle negative controls were added; all six fail against the uncorrected ledger.
- **F3, Pause in Stage A (P2).** `runInventory` takes a `checkpoint` called before every page read of both scans and the cross-check. The runner's checkpoint throws the ordinary `Paused("USER")` and renews the lease. Nothing of a half inventory is journaled, and the resume crawls from cursor 0. Tests cover a pause in scan 1, scan 2, the cross-check and a zero-target census: no page is read after the request, nothing is journaled, and the resume starts at cursor 0.
- **F4, integration seams.**
  - The census size ruling is renumbered **RUL-2026-10-20-002**, and every reference was updated. PR #76's RUL-2026-10-20-001 is kept, and its status updated to integrated.
  - Forge: `package.json`/`main.mjs` 0.9.0 on top of the released 0.8.1. The loader keeps the released `@version 0.8.1`/`@require d91c0878` with `@x-release-pending 0.9.0`.
  - PR #76's `fields.json`/`nested.json` (85cecae) and all its tests and contracts are preserved. `forge_bundle.js` was rebuilt from the merged source. `dist/` was taken from `main` (the skillpack job rebuilds it).
  - The stale "PR #73 blocked" text in the ledger, workflow and this handoff now points at push/131 / PR #76.
  - The game-source citations stay at 6524d0f and were re-checked at 85cecae: `routers/item.ts`, `validators/item.ts`, `validators/combat.ts` and `libs/combat/elementalDamage.ts` are unchanged; `libs/combat/tags.ts` changed only in Clear/Cleanse.

## Repository / refs

| | |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Branch | `claude/elemental-damage-weapon-census-235ynv` (the session's assigned implementation branch) |
| Base | `main@02a288e9` after the round-1 rebase (originally `main@e13bc9fa`; the brief named `383ac0f4`) |
| Implementation commit | rebased `8992fbb3` (originally `d2dc3532`), plus the round-1 correction commit |
| Head | the commit that adds this file; its exact SHA is given in the handoff message |
| Integration target | `main` |
| Brief | `docs/handoffs/ELEMENTALDAMAGE_WEAPON_CENSUS_CAPTURE_IMPLEMENTATION_20261020.md` on `chatgpt/elementaldamage-weapon-census-handoff-20261020@38740f228958020ec183bbf0950e288e455c5698` (PR #74; not modified) |
| Game source | `studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb`, read over raw GitHub, never executed. Public source, not confirmed as the deployed production SHA. |

## Objective

An operator-run, read-only Forge census that finds every current WEAPON record with an `elementaldamage` effect (hidden and visible), captures each one's full body, and turns the results bundle into a deterministic, item-ID-keyed candidate ledger.

## Architecture (the brief left this to Fable)

A new manifest key, `census: {kind: "item.weapon.elementaldamage", pageLimit: 100}`, runs as an ordinary Forge job with no items. It uses the existing journal, lease, budget, pause/resume, snapshot store and export paths.

- **Stage A, inventory** (`runInventory`, `forge/src/runner/census.mjs`). Pages `item.getAll {itemType:"WEAPON", hidden:<false|true>, limit, cursor}` from cursor 0 to `nextCursor:null`, through the new `CachedReader.censusPage` (budgeted, never cached, `item.getAll` only). Every page must satisfy the source contract: `{data:[], nextCursor}`, at most `limit` rows, `nextCursor` null exactly on a short page and otherwise `cursor+1`, every row a WEAPON in the requested partition, no repeated id across the whole scan. The full crawl runs twice and the two projections must be byte-identical (`stableStringify`); otherwise the inventory is **UNSTABLE** and the changed/added/removed ids are recorded. A third crawl with `effect:["elementaldamage"]` is a cross-check only. An exact hit it misses, or a filtered row absent from the inventory, fails the inventory. String-only matches are listed as `filterOnly`.
  - Stage A is all-or-nothing. A 429 or network pause inside it journals nothing, and the resume crawls again from cursor 0.
  - Only a projection is kept: `id, name, itemType, hidden, updatedAt, effectTypes, effectsMalformed` (`projectRow`). It goes to the immutable `capture_snapshots` store under `<job>::census::inventory`. The journal keeps the summary, page provenance, counts, digest and target list. **`FULL_PERSIST_PATHS` is unchanged**, and no raw list body is stored or exported.
- **Stage B, point reads.** Targets are the rows whose parsed `effectTypes` include `elementaldamage`, plus any row whose `effects` was not an array (it cannot be ruled out). Each gets one `item.get` through the existing `_persistFull` snapshot path (512 KiB ceiling, never truncated) and `acceptPoint`: read ok, one row, body persisted, same id, WEAPON, effects array, tag still present, and `updatedAt` equal to Stage A's. Drift is **STALE**. Points are journaled one by one (`capturesCensusPartial`), so resume continues at the next target and never re-reads a finished one.
- **Verdict** (`censusVerdict`, `forge/src/storage/journal.mjs`). `COMPLETE` only when the inventory is COMPLETE and every target point is accepted with its body persisted. Otherwise the verdict is `UNSTABLE`, `FAILED`, `STALE` or `INCOMPLETE`. `jobOutcome` returns `failed` for anything but COMPLETE. The exported bundle's `outcome` also drops to `failed` if the inventory snapshot is gone at export; it is never re-crawled.
- **Export.** The bundle gains a `census` block (summary + verdict + projection rows from the snapshot). Census point captures appear in `captures` with `phase:"census"` and their full `data`. A paused census still exports the bodies it has read.
- **Ledger** (`scripts/elementaldamage_census_ledger.py`, stdlib only). Re-derives counts, the target set, scan termination and each point's acceptance from the bundle instead of trusting its verdict. Classifies each `elementaldamage` effect independently into the brief's seven classes and marks `cLXXf8RJv5l9B_gGsYN2a` **ALREADY STAGED / PR #73**. Records full original effects plus a sha256, provenance (bundle path/sha256, job, manifest hash, snapshot key, capture time, body sha256), controls, stale/missing/failed ids and zero-mutation evidence. Writes JSON and Markdown.

## Changed files

- New: `forge/src/runner/census.mjs`, `forge/test/census.test.mjs`, `forge/test/fixtures/census/elementaldamage_bundle.json`, `scripts/elementaldamage_census_ledger.py`, `scripts/test_elementaldamage_census_ledger.py`, `push/132_elementaldamage_weapon_census.json`, `docs/workflows/ELEMENTALDAMAGE_WEAPON_CENSUS.md`, this file.
- Forge: `budget/reader.mjs` (`censusPage`, `CENSUS_LIST_PATHS`), `runner/manifest.mjs` (census block, identity), `runner/runner.mjs` (`_census`), `storage/journal.mjs` (`allCaptures`, `censusVerdict`, `jobOutcome`), `core/results.mjs` (`resolveCensus`, census captures, bundle block), `core/core.mjs`, `core/facts.mjs` (`censusLine`), `ui/screens.mjs` (preflight card, Run census, verdict banner, folded list, read-only running text), `main.mjs` + `package.json` (0.9.0), `tools/check_manifest.mjs` (prints census), `tools/check_bundle_budget.mjs` (ceiling), `test/fakegame.mjs` (source-faithful `item.getAll`, `onCall` hook), `test/ui.test.mjs`.
- Built: `forge_bundle.js` (rebuilt), `forge_loader_user.js` (`@x-release-pending 0.9.0`; `@version`/`@require` still pinned to the released 0.8.0 bundle, per the release-pin workflow), `dist/building-tnr-content.zip` (rebuilt so the skillpack job has nothing to auto-commit over this SHA).
- Other: `skills/building-tnr-content/scripts/validate.py` (census manifests are noted, not "no items"), `push/README.md`, `docs/RULINGS.md` (RUL-2026-10-20-002).

## Verification (all run on the committed tree, socket-free)

Round-1 figures (pre-correction, pre-rebase) are kept below for history. The corrected head's results are in the round-2 handoff message.

| Command | Result |
| --- | --- |
| `cd forge && npm test` | 667 tests, 667 pass, 0 fail (base 640/640; +25 census, +1 UI, +1 manifest) |
| `cd forge && npm run build && git diff --exit-code -- ../forge_bundle.js` | reproducible (no diff) |
| `cd forge && npm run fixtures && git diff --exit-code -- test/fixtures` | reproducible |
| `node forge/tools/check_bundle_budget.mjs` | raw 424,212 / 432,000, gzip 102,630 / 105,000 (exit 0) |
| `node forge/tools/check_release_pin.mjs` | release pin ok |
| `node forge/tools/check_boundaries.mjs` / `check_imports.mjs` | 0 violations / 0 violations |
| `node forge/tools/check_manifest.mjs push/132_elementaldamage_weapon_census.json` | 0 pre-send problems (exit 0) |
| `python3 skills/building-tnr-content/scripts/validate.py push/132_elementaldamage_weapon_census.json` | 0 errors, 0 warnings |
| `python3 -m unittest scripts/test_elementaldamage_census_ledger.py` | 17 tests OK |
| `python3 scripts/elementaldamage_census_ledger.py forge/test/fixtures/census/elementaldamage_bundle.json --out-dir <tmp>` | COMPLETE, 8 dynamic weapons, 4 candidates, 2 controls, 1 manual, Stormrender staged (exit 0) |
| `build_packs.py --check` / `doctrinemap.py` / `render_doctrine.py --check` | current / 0 errors 0 warnings / current |
| `lawmap.py` | 0 errors, 5 warnings (16d, 18, 37, 61, 69; pre-existing) |
| `python3 .github/scripts/pack_skills.py && git diff --exit-code -- dist` | reproducible |

The baseline needed `git fetch --unshallow`: in a shallow clone, 14 pre-existing tests fail because they look up historical commits.

**Brief edge cases covered by `forge/test/census.test.mjs`:** mixed WEAPON/OTHER (CONSUMABLE, ARMOR, including a hidden one); visible and hidden partitions; more than one page; exact-multiple terminating empty page; empty partition; a description-string `elementaldamage` (filterOnly, not captured); `statTypes` absent/`[]`/`["None"]` and `generalTypes ["Highest"]` (ledger classification tests); multiple dynamic tags; non-formula tags; malformed effects; `updatedAt` drift between scans (UNSTABLE) and between stages (STALE); shifted/repeated rows; malformed page; bad `nextCursor` (null on a full page, skipped cursor); wrong type/partition rows; failed page; cross-check mismatch; over-ceiling body (`persistOk:false`); deleted record (`item.get` null); snapshot gone before export; 429 in Stage A (nothing journaled, restart at cursor 0) and in Stage B with a tab reload (done points exported, not re-read); user pause; per-path budget never above 30 in any 60 s window; zero-match COMPLETE; every list read carries an explicit boolean `hidden`; only `item.getAll`/`item.get` sent, no mutation path. The committed ledger fixture is regenerated and compared by the census test itself, so the Python ledger is tested against the real export shape.

## Deviations, debt and open points — please attack these

1. **Stage A is all-or-nothing.** A pause anywhere in the inventory costs the whole inventory. With `limit:100`, a few hundred WEAPONs is ~10–30 list reads. That seemed safer than resuming an offset crawl across a pause, but a very large population under repeated 429s would loop.
2. **Strictness.** Any page-contract violation, an unstable rescan or a cross-check mismatch blocks Stage B entirely. There is no "partial but labelled" mode. Operator response is a fresh run.
3. **The 32-bit digest** (`fnv1a32`) is a stability fingerprint used inside Forge. The ledger adds a sha256 over the canonical projection and over each captured body.
4. **The projection keeps `name`** (public item content) alongside the brief's id/type/hidden/updatedAt/effect-type list, so the ledger and run screen are readable.
5. **Malformed-effects rows are captured.** A WEAPON whose `effects` is not an array, or has any untyped member, goes to Stage B (`reason:"effectsMalformed"`); its body is captured as evidence and the census verdict is AMBIGUOUS, never COMPLETE (round-1 F1). Deliberate: it cannot be ruled out, and resolving it is an explicit operator step.
6. **Bundle ceiling raised** to 432,000 / 105,000 with the director's approval (RUL-2026-10-20-002, renumbered from a colliding -001). The census measured 424,212 / 102,630 against the 420,000 / 100,000 ceiling.
7. **The hidden partition is not proven live.** At source, `hidden:true` on public `item.getAll` is a plain `eq(item.hidden, true)` filter with no role check (`routers/item.ts:4452-4455`). Whether production behaves the same is not verified.
8. **The run-screen running text for capture-only jobs changed** from "All items sent; reading back…" (wrong for read-only jobs) to "Reading…; nothing is written."
9. **Resolved elsewhere:** PR #73's generated-contract blocker was fixed by PR #76 (Forge 0.8.1, contracts at 85cecae), which this branch now sits on. The census never depended on it.

## Live-game statement

- Live-game requests: **0**. Live-game writes: **0**. Credentials/session material: **none**.
- The game source was read as text from raw GitHub at the pinned SHA; it was not run.
- Not performed: any browser, Tampermonkey or live-Forge check, including real `item.getAll` pagination, superjson Date decoding of list rows, the hidden partition's live behaviour, mobile rendering of the new card and banner, and IndexedDB quota on the device.

## Not begun

- The director's census run (Lane B, `push/132`).
- Any ledger from live evidence; any candidate review; any repair, suggest or edit manifest for any weapon.
- Releasing Forge 0.9.0 (the loader stays pinned to the released 0.8.1 until the reviewed merge and `release_pin.yml`).
