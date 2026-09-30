# Forge Next Phase 1 — integration verification (narrow re-check)

**Status:** FROZEN FOR NARROW VERIFICATION
**Date:** 2026-09-30
**Implementation owner:** Fable / Claude Code
**Independent reviewer:** ChatGPT
**Governing contract:** `state/prompt_forge_next_phase1.md` (unchanged)
**Authorized by:** `docs/reviews/FORGE_TWO_TARGET_INDEPENDENT_REVIEW_2026-09-30.md`. Target A (36dc359) and
Target B (57bcedd) were each PASS WITH NOTES. The approved order is: integrate B; merge fresh main into Phase 1 without
rebasing; return the new head for narrow verification. This handoff completes step 2.
**Live-game policy observed:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

## 1. Refs (review condition 2)

| field | value |
|---|---|
| repository | `perseverance484/tnr-tools` |
| branches | `fable/forge-next-phase1` and `claude/forge-next-phase1-uwhcn1`, same commit |
| **new frozen code/CI head** | `9b61ac333bcec65518ad2b6bb4de3ad47143644f` |
| merge parents | `0016994b61858c6409dfa9fcd920e5291f4bb6c4` (Phase 1 tip, doc-only above A) and `76ae8462f83587a6e9967f577f1b15a79d2e73a8` (fresh main) |
| fresh main | `76ae8462f83587a6e9967f577f1b15a79d2e73a8` |
| previously approved A | `36dc359ebdf503f56dca2bb16994a627c362f44c` (ancestor) |
| previously approved B | `57bceddb31bfaf97a9379e41e67dd501aa223aaa` (ancestor, via main) |

The commit that adds this document sits directly above `9b61ac3` and is **documentation only**. The CI
evidence in §4 is for `9b61ac3`.

### How B reached main (step 1)

`main` had moved to `06b66b0` (the automatic sentinel commit, `docs/DRIFT.md` and `state/schema_sentinel.json`) after B's base. The session
branch `ccr-d998b825-q58zf8` preserved the review verbatim (`7db79c5`, doc-only). It then merged `06b66b0`
(`76ae846`, parents `7db79c5` and `06b66b0`, no conflicts), and `main` was fast-forwarded to `76ae846`. B was not rebased,
so `57bcedd` is an ancestor of main. Main's Forge CI passed: run
[36751933280](https://github.com/perseverance484/tnr-tools/actions/runs/36751933280) on `76ae846`.

`76ae846` changes three paths relative to `06b66b0`: `forge/test/runner.test.mjs` (B's fix),
`docs/handoffs/FORGE_ARCHIVED_MANIFEST_54_TEST_FIX.md` and
`docs/reviews/FORGE_TWO_TARGET_INDEPENDENT_REVIEW_2026-09-30.md`.

## 2. Changed-path inventory (review condition 4)

**`9b61ac3` against frozen A (`36dc359`), restricted to `forge/`, `forge_bundle.js`, loaders and `.github/`:**

```
 forge/test/runner.test.mjs | 37 +++++++++++++++++++++++++++++++++++++
```

That is main's OPC attach-order test (`ce748f6`) with B's archive path. No runtime source,
admission or persistence policy, registry, source pin, generated contract, fixture, lockfile, package version, loader,
workflow or bundle change. The merge had **no conflicts**, so there are no new conflict resolutions to review.

**`9b61ac3` against fresh main (`76ae846`):** 35 files, +6,248 / −642. These are exactly the Phase 1 paths listed in
the reconciliation handoff (`forge/**`, `forge_bundle.js`, Phase 1 handoffs and reviews). No path outside `forge/`,
`forge_bundle.js`, `docs/handoffs/` and `docs/reviews/` differs.

Everything else the merge brought in from main (OPC, Wind Ruins, sentinel, results, state) is main's own
reviewed-or-routine history and is untouched by Phase 1.

## 3. Verification at `9b61ac3` (review condition 3)

From `forge/` in a clean worktree, Node v22.22.2, after `npm ci` (the lockfile is unchanged from A):

| command | result |
|---|---|
| `npm test` | **582 tests, 582 pass, 0 fail** |
| `npm audit --omit=dev --audit-level=high` | found 0 vulnerabilities |
| `node tools/check_imports.mjs` | 0 violations |
| `node tools/check_boundaries.mjs` | 0 violations |
| `npm run fixtures` + `git diff --exit-code -- test/fixtures` | clean |
| `npm run build` + `git diff --exit-code -- ../forge_bundle.js` | clean (bundle reproducible) |
| `node tools/derive_registry.mjs` + `git diff --exit-code -- RESEARCH_REGISTRY.md` | clean |
| `node tools/check_bundle_budget.mjs` | raw 368,514 / 380,000 (97.0%), gzip 82,479 / 85,000 (97.0%) |
| release pin check (`check_release_pin.mjs`, as CI runs it) | release pin clean (loader 0.5.1 at `13b313d8`, unchanged) |

**The test count is 582, up from A's 581:** the one added test is main's OPC attach-order test, now passing
through B's archive path. This matches the reviewer's stated expectation.

The local runs used Node 22; CI uses Node 24 (§4). The reviewer's no-network preload was not applied locally.
The suite's own transport is in-process, and no live host was contacted.

## 4. Canonical Forge CI at `9b61ac3`

Both pushes triggered the canonical `forge` workflow on the exact head `9b61ac3`. Both succeeded:

- **`fable/forge-next-phase1`**: run [36752088871](https://github.com/perseverance484/tnr-tools/actions/runs/36752088871),
  job `verify` (`110012986790`), conclusion **success**. Every step succeeded: npm ci, runtime audit, import direction,
  static boundaries, npm test, generated fixtures, checked bundle, bundle size budget, release pin state.
- **`claude/forge-next-phase1-uwhcn1`**: run [36752088125](https://github.com/perseverance484/tnr-tools/actions/runs/36752088125),
  conclusion **success**.

Neither run was a re-run. The commit carrying this document is documentation only and sits above the CI head.

## 5. Review notes carried forward

- **A-N1** (two cache slots for the unfiltered asset list): efficiency debt only; unchanged.
- **A-N2** (`99ec81e` intentionally over budget): unchanged; review and integrate the frozen pair and this head,
  not `99ec81e` alone.
- **A-N3** (`state/` still says Phase 1 has not begun): still true. It is to be reconciled through the
  `digest.json` → `session_close.py` projection at integration closeout, not hand-edited, and it must not trigger
  reimplementation.
- **B-N1** (`godstorm.repair.test.mjs:40` falls back to a stand-in because `push/53` is archived): open,
  pre-existing, and not addressed here. It needs a small separate follow-up.
- **B-N2** (`forge.yml` path filters omit `push/**` and `archive/spent-manifests/**`): open, pre-existing, and not
  addressed here. It needs a separate follow-up.
- The deferred user decisions (player-identifying battle-history projection; repo-safe name lists) remain
  deferred and untouched.

## 6. Live-game statement

- Live requests: **none.** Live writes: **none.** Credentials or session material: **none.**
- Not performed: installed Android userscript, real browser IndexedDB, Clerk session, production transport,
  export/share.

## 7. What explicitly has not begun

- Phase 1 has **not** been integrated into `main`. That is step 3, and it waits on this verification.
- No release: loader version and pin stay at 0.5.1 / `13b313d8`. The 0.5.2 release is a separate operator step.
- No `state/` edit, and Phase 2 has not begun. Presentation Studio P2 stays queued.

## 8. Freeze

`9b61ac333bcec65518ad2b6bb4de3ad47143644f` is frozen for narrow verification. Integrate Phase 1 into main only
after that verification returns.
