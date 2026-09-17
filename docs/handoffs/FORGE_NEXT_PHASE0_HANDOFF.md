# Forge Next Phase 0 — implementation handoff

**Status: COMPLETE and FROZEN.** ChatGPT performs the independent review before integration.
Phase 1 has not begun.

| | |
|---|---|
| Repository | `perseverance484/tnr-tools` |
| Implementation branch | `fable/forge-next-phase0` |
| Fresh-main base SHA | `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea` |
| Merge-base with `main` | `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea` (direct descendant; no merge, no rebase) |
| Frozen head SHA | `b364492` is this document's commit; the branch head is the single stamp commit that follows it and changes only this line. **Review the branch tip of `fable/forge-next-phase0`.** |
| Contract | `chatgpt/forge-next-unified-contract@efbdc2a4a2f35b12b425ba88a4d415f66f79f2c0` |
| Live game requests | **none** |
| Live game writes | **none** |
| Credentials used | the repository PAT, for clone and push only. No game credential, session or token was used or obtained. |

`main` was reverified at task start and was unchanged from the SHA the contract named
(`git rev-list --count b42c2afd..origin/main = 0`).

---

## 1. Commits

Each is independently reviewable and does one thing.

| SHA | Commit |
|---|---|
| `3b586b358ae7d2b4ee2f53bb5cfea32b58597a74` | `fix(test): release-pending marker is lifecycle state, not a constant` — **isolated baseline defect** |
| `0dd97a7880ce194d50b9c9cecb45ff916a36ae0c` | `docs: Phase 0 baseline, game-source drift measurement, and status` |
| `eb345ee8cc8d5592b132a34fad47873490e93597` | `test(forge): deterministic byte-identity fixtures for the five released screens` |
| `e78cc2525fead09d22a29e2c2c8b8c001021d544` | `harden(ui): h() refuses innerHTML/outerHTML/srcdoc/insertAdjacentHTML for every value type` |
| **`413835e32f85d562390c4ac94d861b080eb662cb`** | **`feat(runner): advisory structured progress emitter` — the runner-event commit** |
| `f86834edab67690f6c8cd067a8e3864d2028432b` | `refactor(forge): extract headless ForgeCore from the view layer` |
| `8fcffd6a11107a6fde22cc4a267f18fafadb6dcb` | `refactor(forge): isolate the userscript host and gate import direction` |
| `4434843cbe5be14dffba60adbb8be6ba995efb39` | `feat(storage): repository text gets its own IndexedDB, capture DB untouched` |
| `6306f5ce956304ba147ed4a714f343a4e980b8ff` | `ci(forge): canonical Node gate set (staged) + new gates, and rebuild the checked bundle` |

---

## 2. The baseline was red, and the defect is isolated

`main` failed `npm test` before any refactor: **310 tests, 309 pass, 1 fail.**

`forge/test/release_loader.test.mjs:47` required **exactly one** `@x-release-pending` marker, while
`forge/tools/check_release_pin.mjs:68` treats a *surviving* marker as a blocker once `@version`
equals `forge/package.json`. The marker is lifecycle state: `.github/scripts/pin_release.py:32`
strips it on promotion. Once 0.4.1 shipped, the two rules contradicted each other and the suite
went red.

Fixed in `3b586b3`, test-only, before any extraction, per the contract's instruction not to hide a
baseline fix inside the architecture work. The test now asserts *at most* one marker and that
whichever lifecycle state the loader is in is internally consistent and satisfies
`checkReleasePin()`.

**Anything currently gating on a green Forge suite on `main` is gating on a stale assumption.**

---

## 3. Objectives

| # | Objective | Status |
|---|---|---|
| 1 | orchestration behind an explicit headless core boundary | done — `forge/src/core/` |
| 2 | a non-DOM host drives a complete lifecycle | done — proven by `core.headless.test.mjs` |
| 3 | the userscript host consumes the same core through `compose()` | done |
| 4 | released screens deterministically byte-identical | done — 12 fixtures, unchanged throughout |
| 5 | execution layers preserved except the one additive runner hook | done — `413835e` |
| 6 | import direction mechanically enforced | done — `tools/check_imports.mjs` |
| 7 | repository text isolated from the capture DB | done — `tnr_forge_repo` v1 |
| 8 | bundle size, contract drift and no-live boundaries gated | done |
| 9 | one canonical Forge Node CI gate set | done, **staged not installed** — `state/staged_workflows/forge.yml` (see §6.8) |
| 10 | no visible Forge Next feature work | done — no screen, copy, class or route changed |

### Behavioural summary

The operator should notice nothing. `ui/app.mjs` went from 411 lines of mixed view and workflow to
a view that mounts, routes, renders banners and toasts, and subscribes to core notifications. Every
workflow decision — picker loading, manifest selection, auth gates, start/resume/drive, capture
materialization, results bundle — moved to `ForgeCore`, which emits facts (`level`, `text`,
payload) and never nodes. Screens call the same `app.*` methods as before; those are now forwarders.

### The one runner change — `413835e`

`Runner.on(fn)` subscribes; `_emit` is synchronous, never awaited, writes nothing to the journal,
performs no state transition, and sits only between awaits that already existed. Every subscriber
runs in `try/catch`. Events: `job:start`, `item:start`, `item:end`, `job:paused`, `job:end`.

`runner.events.test.mjs` runs the same job three ways — no subscriber, a passive subscriber, a
subscriber that throws on every event — and asserts **journal bytes, persisted storage, request
order and summary are identical across all three**. One axis is normalised: `FakeGame`'s entity-id
counter is module-global, so sequential runs mint different ids; each distinct id becomes a token by
order of first appearance. That is a harness property, is the only normalisation, and is stated in
the test.

---

## 4. Measurements

| | Baseline (fresh main) | Final (frozen) | Δ |
|---|---|---|---|
| Node / npm | v22.22.2 / 10.9.7 | same | — |
| `npm test` | 310 / **309 pass, 1 fail** | 332 / **332 pass, 0 fail, 0 cancelled, 0 skipped** | +22 tests |
| `npm test` after baseline fix | 310 / 310 pass | — | — |
| bundle raw | 404,594 B | **413,323 B** | **+8,729** |
| bundle gzip (tool) | 75,801 B (gzip(1)) · 76,843 B (zlib) | **77,998 B** (zlib) | **+1,155** vs zlib baseline |
| `npm audit --omit=dev --audit-level=high` | 0 vulnerabilities | 0 vulnerabilities | — |
| `npm audit` full headline | 3 high, all dev-only (`uploadthing`) | unchanged | — |
| import-direction violations | 0 (33 modules) | **0** (37 modules, 62 cross-layer imports) | — |

The +8.7 KB raw is the cost of `core/` (3 modules), the host adapter move, `repotext.mjs` and the
runner emitter. Budget set at raw 430,000 / gzip 81,000 — about 4% headroom, committed beside the
measurement it came from.

### Commands and results

```
main reverification            origin/main == b42c2afd, 0 commits since contract
npm ci                          rc=0
npm test                        332 tests / 332 pass / 0 fail / 0 cancelled / 0 skipped
npm run fixtures                rc=0
git diff --exit-code -- test/fixtures/envelope    clean
git diff --exit-code -- test/fixtures/screens     clean
npm run build                   rc=0
git diff --exit-code -- ../forge_bundle.js        clean
node tools/check_imports.mjs        37 modules, 62 cross-layer imports, 0 violations   exit 0
node tools/check_boundaries.mjs     37 modules, pin 345d18ac, 0 violations             exit 0
node tools/check_bundle_budget.mjs  raw 413323/430000 (96.1%)  gzip 77998/81000 (96.3%) exit 0
(the four steps above are the staged workflow's gates, run here by hand and under npm test;
 see §6.0 — they are not yet installed in CI)
python3 skills/building-tnr-content/scripts/doctrinemap.py          exit 0
python3 skills/building-tnr-content/scripts/render_doctrine.py --check  exit 0
python3 skills/building-tnr-content/scripts/build_packs.py --check      exit 0
python3 skills/building-tnr-content/scripts/lawmap.py .   93 laws / 93 rows / 77 citations, 0 errors, 5 pre-existing warnings
```

**Fixture status:** reproducible and clean. Envelope fixtures unchanged. All 12 screen fixtures
byte-identical from the moment they were created, through the core extraction, the host move and
the storage split.

**Generated artifact / build status:** `forge_bundle.js` rebuilds byte-identically from source and
is committed. It was found **stale** by the new reproducibility step — I had not rebuilt it after
the extraction commits. The gate caught it before the freeze; that is the gate doing its job, and it
is recorded here rather than quietly fixed.

---

## 5. Game-source drift — measured, nothing adopted

**Upstream head inspected:** `studie-tech/TheNinjaRPG@1fd355ab92cec78148130e02c8d38834836c3181`
(2026-09-16 17:58 +0200) — identical to the head observed when the contract was authored.

Two different pins exist in this repository and it is easy to assume one governs both:

| Artifact | Pin | Behind head |
|---|---|---|
| `forge/src/runner/fields.json` + `nested.json` | `345d18ac` (2026-08-31) | **154 commits** |
| `45c_DATA_constructors.json` `source_drop` | `bdec2883` (2026-08-29) | **243 commits** |

Forge-relevant drift since the Forge pin: 848 files changed upstream overall, 114 matching
router/tRPC/procedure/auth/session/schema/validator surfaces. Of the routers Forge calls —
`item.ts` **+120/−63**, `asset.ts` +20/−10, `bloodline.ts` +11/−14, `village.ts` +13/−12, `ai.ts`
+6/−5, `jutsu.ts` +5/−4; `app/drizzle/schema.ts` and `app/src/validators/` **+558/−9** across 9
files.

**All 43 procedures in `forge/src/transport/procedures.mjs` still exist at upstream head.** The
drift is in field shapes and validators, not in the procedure surface Forge addresses.

`fields.json` correctly describes its own pin and that pin has not moved, so the baseline is
truthful and **no adoption was necessary**. No pin moved, no contract regenerated, no auth semantics
or procedure shapes changed, no game source touched. The `item.ts` and validator deltas are real
standing debt for a separately scoped Lane A adoption task and should not be absorbed silently.

---

## 6. Known debt and deviations

0. **The consolidated CI workflow is STAGED, not installed — this needs an action from dauntless.**
   The container PAT cannot write `.github/workflows/`: a fine-grained token needs the separate
   Workflows scope, which this one deliberately does not have. The push was rejected outright
   (`refusing to allow a Personal Access Token to create or update workflow .github/workflows/forge.yml`).
   The consolidated gate set is therefore committed at **`state/staged_workflows/forge.yml`**, the
   convention this repository already uses for `release_pin.yml`, `scrub.yml`, `skillpack.yml`,
   `relay.yml` and `regen_schemas.yml`. `.github/workflows/forge.yml` on this branch is byte-identical
   to `main` and still runs the **old** gate set.

   **Until dauntless installs the staged file via the GitHub web UI, CI does not run the
   import-direction gate, the boundary gate, the bundle budget or the screen-fixture
   reproducibility check.** All four run locally under `npm test`, and all four pass here, so the
   protection exists in the suite; it is the CI enforcement that is pending. This is the same
   credential constraint recorded as F2 in the Quest Studio review, arriving from the other side.

1. **Generated-contract drift is unadopted**, as above. This is the largest open item.
2. **`derive_fields.mjs` / `derive_nested.mjs` cannot run in CI** — they need a game-source
   checkout. The boundary gate checks the weaker property that both files agree on one pin, which
   catches an accidental edit but not staleness against upstream.
3. **Screen fixtures cover 12 states, not every branch.** They cover all five screens across empty,
   loaded, selected, planned and finished. Orphan-decision, paused and rate-limited renders are not
   yet pinned; adding scenarios is cheap and is the right response to touching those paths.
4. **`ForgeCore` still receives the whole dependency bag** via `Object.assign`. It has no DOM
   dependency and the boundary is enforced, but the constructor is not yet an explicit contract.
5. **`repoCache` falls back to `this.cache`** when absent, so a harness that builds a core without
   `compose()` still works. Production always gets the separate database; the fallback is a
   compatibility seam worth removing once nothing needs it.
6. **The bundle budget is a ratchet at ~4% headroom.** Deliberate. It will need a reviewed raise
   during Phase 1, which is the intent.
7. **`npm audit` reports 3 high dev-only advisories** (`uploadthing`), unchanged from baseline and
   not converted into a Phase 0 blocker.

### Browser checks NOT performed

Everything here is Node and jsdom. **No real-browser verification was done and none was possible in
this environment**: no Firefox mobile, no ViolentMonkey, no device. Specifically unverified by
execution — the userscript loader install path, `/forge` entry takeover against the live site,
carrier hydration timing, overlay rendering and CSSOM install in a real browser, IndexedDB
behaviour under a real storage backend (including the new `tnr_forge_repo` database and the
rollback path), and `navigator.storage.persist()`.

The takeover move in `8fcffd6` is a pure file move with import updates and its existing suites pass,
but "the suites pass" is not the same as "it was opened on the device." That check belongs to the
operator before this reaches a release.

---

## 7. What has explicitly NOT begun

Quest Studio integration (the accepted Studio at `5ba636d8` was **not** cherry-picked, merged or
referenced by `forge.yml`; its constraints are carried forward as constraints only); Phase 1; the
visual-shell redesign; Content Admin; Builder retirement; any release movement; any adoption of
game-source drift. No ChatGPT branch was modified. The planning and Quest Studio branches were not
merged.

---

## 8. Summary

The extraction landed and the net held: twelve screen fixtures, created before any domain logic
moved, are byte-identical through the core extraction, the host isolation and the storage split. A
process with no DOM in it drives select → start → run → resolve → export and checks the committed
bundle's outcome, entries, verdicts and postflight.

Two findings are worth the reviewer's attention more than the refactor is. `main` was already red,
for a reason that had nothing to do with this work and everything to do with a test that encoded a
release as a constant. And the checked bundle was stale until the new reproducibility gate said so —
which is the argument for that gate, made by the gate itself, on its first run.
