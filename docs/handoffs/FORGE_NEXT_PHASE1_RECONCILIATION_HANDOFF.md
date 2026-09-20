# Forge Next Phase 1 — reconciliation with main (frozen combined SHA)

**Status:** FROZEN FOR INTEGRATION REVIEW OF THE SYNCHRONIZATION DELTA
**Date:** 2026-09-20
**Implementation owner:** Fable / Claude Code
**Independent reviewer:** ChatGPT
**Governing contract:** `state/prompt_forge_next_phase1.md` (unchanged)
**Authorized by:** `docs/reviews/FORGE_NEXT_PHASE1_CORRECTION2_REREVIEW.md` — PASS for `9133145`, next
permitted work: reconcile with fresh `main`, resolve overlapping surfaces, check upstream drift without
moving the pin, return a combined SHA with current gates and CI.
**Live-game policy observed:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

## 1. Refs

| field | value |
|---|---|
| repository | `perseverance484/tnr-tools` |
| branches | `fable/forge-next-phase1` and `claude/forge-next-phase1-uwhcn1`, same commit |
| **new frozen combined head** | `36dc359ebdf503f56dca2bb16994a627c362f44c` |
| merge commit | `99ec81e146755e7d6869e1e6bd86b37855bf90a6` — parents `c7bdd2d` (Phase 1 branch tip) and `18c6a25` (main) |
| last reviewed Phase 1 code | `9133145c1e626eb1611ac6a23302b58885c33fe6` (PASS) |
| `main` merged | `18c6a2554c1bf9231e00e46108a5a7faf66387aa` (Forge 0.5.1, Presentation Studio P0/P1, size pass) |
| original base | `77f02c30f7714eb8506ace8802904cb351a70d34` |

Two commits above the previous tip:

| SHA | commit |
|---|---|
| `99ec81e` | `merge: reconcile Phase 1 with main at 18c6a25` |
| `36dc359` | `build(forge): ratchet the bundle budget on the merged Phase 1 product` — the ceiling alone |

**Merge, not rebase.** A rebase would have orphaned every SHA the three handoffs and three reviews cite.
The merge keeps `8f15416`, `7bd8592` and `9133145` as ancestors, and gives one combined commit whose
resolution can be read directly: `git show 99ec81e` shows exactly what was decided at each conflict.

**The merge commit is red on one gate by design.** It leaves the budget at main's `354,000 / 78,000` so
the raise is measured against the merged product and reviewed on its own; `36dc359` is the green head.
The other eleven gates pass at both commits.

## 2. What the synchronization delta is

Eight paths conflicted. Every resolution keeps both sides' behaviour; none discards integrated work:

| file | resolution |
|---|---|
| `runner/manifest.mjs` | main's execution-policy identity (`manifestHash`/`bodyHash`/`isDefaultPolicy`) and `imagePack` normalization, plus the Phase 1 tier counts |
| `runner/runner.mjs` | main's image-pack provenance and upload path, plus the mode-dispatched capture loop; main's `capInput`/`sentInput` are superseded by the registry's canonical input and removed as dead code |
| `ui/screens.mjs` | both import groups |
| `test/fakegame.mjs` | main's filtered `gameAsset.getAllNames` answer and its BAD_REQUEST on a missing object, plus the combat rows |
| `test/screen_scenarios.mjs` | both scenario groups: main's pack verified/refused and Phase 1's research pair |
| `tools/check_boundaries.mjs` | main's property 4 (presentation containment) kept; the Phase 1 view boundary becomes property 5; registry-pin agreement kept |
| `tools/check_bundle_budget.mjs` | main's ceiling and history in the merge; ratcheted in `36dc359` |
| `forge_bundle.js` | rebuilt from the merged source |

Auto-merged without conflict and reviewed by hand: `budget/reader.mjs` (main's `listInput`/`sameInput`
beside the Phase 1 `query()`/`_page()`), `core/facts.mjs`, `core/core.mjs`, `main.mjs`, `build.mjs`
(main's comment strip and its esbuild oracle), `.github/workflows/forge.yml` (`fetch-depth: 0`),
`package.json` (0.5.1).

## 3. One semantic conflict, resolved by repository authority

`main` learned from a live failure — three Godstorm Stormcourt asset creates dying at their pre-create
name snapshot with `gameAsset.getAllNames BAD_REQUEST` (`harvests/inbox/tnr_results_1789829183863.json`,
repaired at `74083c1`) — that this procedure declares
`.input(z.object({ type: z.enum(GameAssetTypes).optional(), folderPrefix: z.boolean().optional() }))`:
members optional, **object required**, so `undefined` fails zod before the resolver runs.

The Phase 1 registry had transcribed that row as **input-free**. That was an audit error in the first
implementation: the row's transport facts (kind, auth, limiter) were audited, its input contract was
not. Left as it was, the registry would have reproduced the failure main had just fixed.

Resolved by reading the pinned source, not by taking the newer side: `asset.ts:50-57` at
`345d18ac` says exactly what main says, and is byte-identical at upstream `b78eadb9`. The row now
carries the audited contract (`type? ∈ GameAssetTypes`, `folderPrefix?: boolean`), so:

- "no filter" canonicalizes to `{}` and a manifest filter is validated before transport;
- `readMode("gameAsset.getAllNames")` is `query`, so a capture of it goes through the input-aware
  `reader.query()` path with a cache key that carries the filter;
- `reader.listInput(path)` — the shape the dedupNames and reconciler snapshot callers send — is now
  **derived from that row** (`canonicalInput(path, undefined) ?? undefined`) rather than kept as a
  second table, so the bare-list shape and the capture contract cannot disagree. Main's tests for
  it (`godstorm.repair.test.mjs`) pass unchanged;
- the five other name lists stay input-free, with a test that inventing an object for them is refused
  as firmly as omitting it for this one.

`REGISTRY_REVISION` moves `0657385d → 2b643a51` because the admission contract changed. No row was
added, removed or retiered; the transport table is byte-identical.

## 4. Upstream drift, checked at `b78eadb9` against the pin

`getBattleEntries`, `getBattleHistory`, `asset.getAllNames`, `BattleTypes`, `GameAssetTypes`, and the
`publicProcedure`/`protectedProcedure` builders are **identical** between `345d18ac` and `b78eadb9`.
The two admitted combat procedures remain at `combat.ts:382` and `:530`; the `.use(ratelimitMiddleware)`
sites shifted (`898→906, 960→967, 1410→1416, 1506→1511`) and still touch neither. **The source pin is
not moved**, and no adoption task is opened by this pass. `docs/DRIFT.md` and the sentinel
(`9e1dafc`, drift @`a670c9a`) were not consulted for admission and are untouched.

## 5. Verification — exact commands and results

From `forge/` on the merged tree, Node v22.22.2, after `npm ci`:

| command | result |
|---|---|
| `npm test` | **581 tests, 581 pass, 0 fail** (401 from Phase 1 + main's suites; +1 registry contract test) |
| `npm audit --omit=dev --audit-level=high` | found 0 vulnerabilities |
| `node tools/check_imports.mjs` | 41 modules, 78 cross-layer imports, **0 violations** |
| `node tools/check_boundaries.mjs` | 41 src + 13 presentation modules, pin `345d18ac…`, **0 violations** |
| `npm run fixtures` + `git diff --exit-code -- test/fixtures` | clean — all **16** screen fixtures reproducible (12 Phase 0, 2 research, 2 pack) |
| `npm run build` + `git diff --exit-code -- ../forge_bundle.js` | clean — bundle reproducible through main's comment strip and oracle |
| `node tools/derive_registry.mjs` + `git diff --exit-code -- RESEARCH_REGISTRY.md` | clean |
| `node tools/check_bundle_budget.mjs` | raw 368,514 / 380,000 (97.0%), gzip 82,479 / 85,000 (97.0%) |
| release pin check | clean (loader stays at released `13b313d8`; a release is the operator's step) |

**Canonical Forge CI: run `35518539978`, job `verify` (`106098496934`) — conclusion `success`** on
`36dc359`, all 15 steps. <https://github.com/perseverance484/tnr-tools/actions/runs/35518539978>

## 6. Bundle budget — and the documentation correction

main's size pass strips comments from the artifact, so Phase 1's cost on this build is its code alone:
main post-size-pass `339,669 / 74,926` → merged `368,514 / 82,479`, **+28,845 raw / +7,553 gzip**.
Ratchet `380,000 / 85,000` (97.0% / 97.0%), the same ~3% headroom the size pass set for itself. The two
earlier Phase 1 ceilings (`460,000/90,000`, `466,000/92,000`) are superseded and **not carried forward**,
as the re-review required.

The re-review's non-blocking correction is accepted: the previous handoff's "+6,714 raw / +1,846 gzip
over the previous correction pass" was cumulative from `8f15416`; the second correction's own increment
was **+1,086 raw / +333 gzip**. Corrected in `36dc359`'s message and budget comment; the frozen earlier
handoffs are left as written.

## 7. Known debt and what to attack

1. **The merge commit `99ec81e` is red on the budget gate alone**, by design; `36dc359` is green.
   Review the pair together.
2. **`gameAsset.getAllNames` has two cache slots**: the bare-list slot (`gameAsset.getAllNames:` via
   `reader.list()`, used by dedupNames/reconciler) and the query slot (`gameAsset.getAllNames?{}` via
   `reader.query()`, used by captures). Both are invalidated by a write to the entity and captures
   are always fresh, so nothing is wrong, but it is one request cached twice.
3. **Operational state on `main` still says Phase 1 "has not begun."** `state/` is a Lane B projection
   (`digest.json` → `session_close.py`), so it was **not** edited here; it needs reconciliation through
   that ritual when the workstream state is next updated, and must not cause this work to be done twice.
4. **`validate.py:201` is red on `main`'s session-open routine** (`set()` on an inbox bundle's
   `checks: null`), pre-existing and unrelated to the Forge gates. Not repaired here; not reported green.
5. Items from the earlier handoffs stand: the 32-bit FNV-1a revision is change detection, not a
   commitment; overlap refusal is one defensible policy; the two user-owned decisions (player-identifying
   projection on `combat.getBattleHistory`; repo-safe name lists) remain open and untouched.

## 8. Live-game statement

- Live requests: **none.** Live writes: **none.** Credentials or session material: **none.**
- The game source was read from read-only checkouts at `345d18ac` and `b78eadb9` — GitHub reads, not
  game requests.
- Browser checks not performed: unchanged — no real browser, IndexedDB, Clerk session, userscript run
  or transport. The merged image-pack screens are covered only by main's serialized fixtures.

## 9. What explicitly has not begun

Unchanged: Phase 2 visual shell, Phase 3 manifest UX, Quest Studio integration, Content Admin, Publish,
Project Workspace, Builder retirement, game-source pin adoption. Presentation Studio P2 stays queued
behind Forge Next per `18c6a25`'s ruling.

## 10. Freeze

`36dc359ebdf503f56dca2bb16994a627c362f44c` is frozen for review of the synchronization delta
(`git diff 18c6a25...36dc359` for Phase 1 on main; `git show 99ec81e` for the resolutions). Do not
integrate until that review returns. Phase 2 will not begin automatically.
