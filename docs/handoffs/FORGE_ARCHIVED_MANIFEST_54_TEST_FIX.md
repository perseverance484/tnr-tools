# Forge test fix — OPC attach-order pin reads archived manifest 54

**Status:** FROZEN FOR INDEPENDENT REVIEW
**Date:** 2026-09-30
**Implementation owner:** Fable / Claude Code
**Independent reviewer:** ChatGPT
**Lane:** A (test-only change to `forge/`)
**Live-game policy observed:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

## 1. Refs

| field | value |
|---|---|
| repository | `perseverance484/tnr-tools` |
| branch | `ccr-d998b825-q58zf8` (session-assigned branch; not `fable/*`) |
| base | `1601f072af839402395eeab1326b1228747e0009` (`main` at start) |
| **frozen review target** | `57bceddb31bfaf97a9379e41e67dd501aa223aaa` |
| integration target | `main`, verified at `06b66b085c92216accd7913b32126a7a10413603` |

The commit that adds this document sits above the frozen target and is documentation only. Review the code
change with `git show 57bcedd` or `git diff 1601f07 57bcedd`.

`main` moved one commit after the base, `06b66b0` (sentinel: `docs/DRIFT.md`, `state/schema_sentinel.json`).
It shares no paths with this change, and `git merge-tree --write-tree origin/main 57bcedd` merges cleanly.

## 2. Objective

Restore a green Forge suite on `main`. The `forge/test/runner.test.mjs` test *"OPC launch-final planner and
re-attach order stay invariant as scene idmap fills"* was failing with ENOENT.

## 3. Cause

| commit | effect |
|---|---|
| `ce748f6` | added the test, reading `push/54_one_perfect_crop_launch_final.json` |
| `418874a` | archived that manifest to `archive/spent-manifests/push-2026-09-28/` |
| `abcb248` | deleted it from `push/` (removing it from the active Forge picker) |

After `abcb248` the test cannot find the file. `node --test test/runner.test.mjs` on `1601f07`
gives 25 pass / 1 fail (ENOENT). This was probably not caught in CI because `abcb248` touched only `push/`.

## 4. Change

One line of `forge/test/runner.test.mjs` (plus a two-line comment): the test reads
`archive/spent-manifests/push-2026-09-28/54_one_perfect_crop_launch_final.json` instead.

The test checks exactly the same bytes as before. The blob is `cb9da51493057632c367ec0389223df83f4cbfb5` at
`ce748f6:push/…`, at `abcb248~1:push/…`, and at the archive path on `main`. No assertion,
expectation, source module, fixture or bundle changed.

Alternatives not taken:
- **Restore `push/54`:** rejected because it would put a spent manifest back in the active Forge picker, which
  `abcb248` removed on purpose.
- **Copy it into `forge/test/fixtures`:** rejected because it would duplicate 821 lines the archive already holds.
- **Resolve through `findManifest`:** rejected because `make_image_pack.mjs` only knows the `push-2026-09-19`
  archive directory.

## 5. Verification — exact commands and results

From `forge/` at `57bcedd`, Node v22, after `npm ci`:

| command | result |
|---|---|
| `npm test` | **523 tests, 523 pass, 0 fail** (`main` at `1601f07`: 1 fail) |
| `node tools/check_imports.mjs` | 0 violations |
| `node tools/check_boundaries.mjs` | 0 violations |
| `npm run build` + `git diff --quiet -- ../forge_bundle.js` | unchanged |
| `npm run fixtures` + `git diff --quiet -- test/fixtures` | unchanged |
| blob check: `git rev-parse` on the three paths in §4 | all `cb9da51` |

Not run: the GitHub Actions Forge workflow on this branch, and the doctrine/law/pack gates (no skills,
doctrine or generated docs changed).

## 6. Interaction with Forge Next Phase 1

The Phase 1 branch (`fable/forge-next-phase1`, frozen reconciliation target `36dc359`) does not touch
`runner.test.mjs`. In a scratch trial merge of the Phase 1 branch with `main` at `1601f07`, the only failing
test was this one (581/582). The Phase 1 frozen SHA was not modified. Once this change is on `main`, the
Phase 1 integration picks it up.

## 7. Known debt / for the reviewer

1. **The same archival hole exists for manifest 53, but it doesn't make the suite fail.**
   `forge/test/godstorm.repair.test.mjs:40` hard-codes `push/53_godstorm_failed_items_repair.json`. Since
   `push/53` was archived (to `push-2026-09-19`), `godstormRepairText()` silently falls back to the
   hard-coded stand-in ledger. So the suite passes, but that test no longer exercises the real committed
   manifest 53. Left untouched as out of scope; the fix is the same kind of path change (or reuse of
   `findManifest`).
   The `imgpack.test.mjs` end-to-end tests are **not** affected: they resolve through `findManifest`, which
   already checks the archive directory and currently returns the archived 53.
2. **Hard-coded archive paths remain fragile** if archive directories are ever reorganized. A shared
   resolver over `push/` and all of `archive/spent-manifests/*` would remove the class of failure; that would be
   a separate, reviewed change.
3. **Branch naming:** the work is on the session-assigned branch rather than `fable/*`. It can be mirrored to a
   `fable/` ref at the same SHA if the reviewer wants the naming convention.

## 8. Live-game statement

- Live requests: **none.** Live writes: **none.** Credentials/session material: **none.**
- No browser, userscript, IndexedDB or installed-device check performed. None is relevant to a test-path change.

## 9. Not begun

No release, no loader/pin change, no `state/` edit (Lane B projection), no pull request, and no change to the
Phase 1 branch.

## 10. Freeze

`57bceddb31bfaf97a9379e41e67dd501aa223aaa` is frozen until review returns.
