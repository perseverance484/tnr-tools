# Implementation handoff — builder app (forge) production readiness

Per `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Implementation contract:
`state/prompt_builder_app_readiness.md` (branch `chatgpt/builder-app-readiness-brief`,
`b8f9dbf533dd51c119eb8d530e9c2fe3506e43b4`). Expect a **full relevant readiness review**, not a
narrow re-check: this pass is wider than the F4 correction.

## Repository / refs

| | |
|---|---|
| repository | `perseverance484/tnr-tools` |
| implementation branch | `claude/builder-app-production-readiness-kelsib` |
| base (prior implementation head) | `4062268f433ffd4d1f9b7b1e2678367ecad9119c` (`builder-app`) |
| merge-base with main | `4a506dff0af7dd499c8b580af4f0c14fdfc48c1c` |
| head (FROZEN) | see `HEAD_SHA` at the end of this file |
| `main` observed at handoff | `4a506dff0af7dd499c8b580af4f0c14fdfc48c1c` |
| integration target | `main`, when the review passes. Not merged here. |

**Branch deviation, stated plainly.** The brief says to work on `builder-app`. This session was
assigned `claude/builder-app-production-readiness-kelsib` and told never to push elsewhere, so the
branch was created FROM `builder-app` (not from `main`) and `main` was merged into it once, at the
start, in commit `00ce50b` — that merge is why the diff below also contains `main`'s own commits
(`push/46*`, the collaboration docs, the sentinel report). `builder-app` was not modified. Every
readiness commit is on top of `4062268`, so a reviewer can read this pass with
`git diff 4062268..HEAD -- forge/ forge_bundle.js forge_loader_user.js docs/BUILDER_APP_NOTES.md
state/staged_workflows/release_pin.yml skills/building-tnr-content/scripts/harvest.py`.

Verified before editing: every ref in brief section 0 still resolved to the value it names, and the
review evidence at `08382eebcffcbcc464c93d348f83598fc219dd76` was read first.

## Objective

Bring forge to the brief's definition of production-ready: close the surviving independent-review
blocker and the seven readiness blockers, prove the source pin still matches production-relevant
contracts, make the install immutable, and prove a result bundle is ingestible by the repository's
own harvest path — all without a single live request.

## Changed files, grouped by blocker

**P0-1, F4 (brief §3)** — `forge/src/transport/envelope.mjs`, `forge/test/adversarial.test.mjs`
(F4c, F4d).
`decodeElement()` accepted any truthy `el.error`, so `[{"error":{}}]` decoded to a normal `UNKNOWN`
verdict and an already-SENT mutation was marked FAILED. A per-index error is now held to the same
`isTrpcErrorBody()` adapter shape as a request-level one; anything else throws, the mutation batch
raises a `TransportError`, the item stays `SENT` and the job pauses at `UNDECODABLE_RESPONSE`. Query
sibling salvage unchanged. F4c fails against `4062268`.

**P0-2, honest terminal semantics (brief §4)** — `forge/src/storage/journal.mjs`,
`forge/src/runner/runner.mjs`, `forge/src/runner/manifest.mjs`, `forge/src/ui/{app,screens,styles}.mjs`,
tests R1-R5 plus a UI regression.
New job state `INCOMPLETE` (execution finished, something unresolved); `setJobState()` refuses `DONE`
while any item is non-terminal; `jobOutcome()` (`success|failed|unverified|open`) is what the toast,
the Run-screen banner and the exported bundle report. An `unread`/`drift` item stays resumable and a
resume can only re-read. `readBack:false` is refused by `parseManifest` on any manifest that writes
(it used to mint `VERIFIED{skipped}`); capture-only manifests are unaffected.

**P0-3, pool codes and lints (brief §5a)** — `forge/src/runner/pool.mjs` (new),
`forge/src/runner/lints.mjs` (new), `forge/src/runner/manifest.mjs`, `forge/src/runner/validate.mjs`,
tests K1-K6 plus a `push/` compatibility test.
Codes resolve at parse time — before any create, upload or update — from the repository's generated
`32b_DATA_pool.json`, bundled at build time. An unresolved code opens no job (TNR-01: a literal code
is dropped server-side and leaves an empty kit behind a green row). Laws 18 and 40 enforced; L03,
L04, L05, L07, L11, L12b, L13, L16, L17, L18 ported as errors and L06, L08, L10, L15 as advisories.
`skipPreflight` cannot disable any of them. L18's clear/copy half is deliberately NOT ported
(`docs/RULINGS.md`: law 19 contradicted at source).

**P0-4, dedupNames (brief §5b)** — `forge/src/runner/runner.mjs`, tests D1-D4.
Enforced before the first create through the budgeted cache-first reader; a collision fails the item
with no placeholder minted; a limited or failed name read pauses the job instead of being skipped.

**P0-5, nested unknown keys (brief §6)** — `forge/tools/derive_nested.mjs` (new),
`forge/src/runner/nested.json` (new, generated), `forge/src/runner/validate.mjs`,
`forge/src/main.mjs`, tests N1-N5.
Key sets per discriminator derived from the same pin; unknown nested keys and unknown `type`/`task`
refused pre-send; fails closed with no derived set. Key sets only, never bounds (`power: 400` is
still accepted, guarding against the `45g` mistake).

**P0-6, source relevance (brief §7)** — `forge/tools/pin_relevance.mjs` (new).
Evidence below. The pin stays at `345d18ac`.

**P0-7, release pin (brief §8)** — `state/staged_workflows/release_pin.yml`,
`forge_loader_user.js`, `forge/tools/check_release_pin.mjs` (new), tests in `ui.test.mjs`.

**P0-8, harvest compatibility (brief §9)** — `forge/src/ui/app.mjs`,
`skills/building-tnr-content/scripts/harvest.py` (the one change outside `forge/`),
`forge/test/harvest.test.mjs` (new).

**Also** — `forge/package.json` and `forge/src/main.mjs` version 0.1.3 → 0.2.0; `forge_bundle.js`
rebuilt; `docs/BUILDER_APP_NOTES.md` rewritten so its claims match the tree.

## Verification — exact commands and results

Run from `forge/` unless stated. Node v22.22.2, `npm ci` from the committed lockfile.

| command | result |
|---|---|
| `npm test` | **199 tests, 199 pass, 0 fail** (was 168 at `4062268`) |
| `npm run build` | `wrote /home/user/tnr-tools/forge_bundle.js (342.2 KB)` |
| rebuild diff: `cp forge_bundle.js /tmp/b.js && npm run build && cmp /tmp/b.js ../forge_bundle.js` | identical — **deterministic**, and the checked-in bundle matches a fresh build |
| `npm run fixtures` then `diff -r` against the pre-run copy | **byte-identical**; no adapter fixture input changed |
| `node tools/derive_fields.mjs <pin> \| cmp - src/runner/fields.json` | **byte-identical** — `fields.json` reproduces from the pin |
| `node tools/derive_nested.mjs <pin> \| cmp - src/runner/nested.json` | **byte-identical** — `nested.json` reproduces from the pin |
| `node tools/pin_relevance.mjs <pin> <sentinel>` | exit 1 with 2 flagged surfaces; both read; verdict below |
| `node tools/check_release_pin.mjs` | 0 blockers, 1 pending install (the dauntless workflow action) |
| `python3 skills/building-tnr-content/scripts/harvest.py verify <generated bundle>` | OK / FAIL / UNVERIFIED / ERROR for the four outcomes, `VERIFY FAILED`, **exit 1**; a clean bundle exits 0 |
| same, over all 12 bundles in `harvests/inbox/` before and after the `harvest.py` change | **no verdict changes** |
| `python3 .../doctrinemap.py` (repo root) | exit 0 — 21 assertions, 18 referenced, 0 errors, 0 warnings |
| `python3 .../render_doctrine.py --check` | exit 0 — all projections current |
| `python3 .../build_packs.py --check` | exit 0 — all packs and TOCs current |
| `python3 .../lawmap.py` | exit 0 — 93 laws, 93 matrix rows, 77 citations, 0 errors, 5 warnings (identical to the baseline in `state/status.json`) |
| `python3 .../selfcheck.py` | **exit 1, pre-existing** (TNR-03). Byte-identical output with this branch stashed, so this pass neither caused nor fixed it. |
| static: no socket in tests, no unexpected host in `src/` | asserted by a test, not just a grep: no test file may import a network module or call a global fetch, and `src/` may name only `api.github.com` and `cdn.jsdelivr.net` |

Every newly fixed defect has a regression that fails against `4062268` or an equivalent minimal
fixture: F4c (proved by stashing the source fix), R1-R5, K1-K6, D1-D4, N1-N5.

## Source / provenance

- Game source pin, unchanged: `studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`.
  Read from a local checkout; never executed.
- Compared against the sentinel upstream on `main`:
  `studie-tech/TheNinjaRPG@e02f815954c14eeb8c2fcbc4a589a506971e0ed7`.
- **Relevance verdict: nothing forge relies on changed.** Both derived contracts (`fields.json`,
  `nested.json`) are IDENTICAL between the two commits. Two of the 21 declared surfaces differ, both
  read: `app/src/server/api/root.ts` registers two new routers (`push`, `purchases`), and
  `app/drizzle/schema.ts` adds twelve device/purchase tables plus relations — no `userData` column
  moved, which the identical 157-key `ai` field set proves independently. `trpc.ts` (the limiter),
  all six content routers, all four validator files, the upload route, `proxy.ts`,
  `next.config.mjs`, `global-not-found.tsx` and `app/package.json` are byte-identical. The pin is
  retained on that evidence; `docs/DRIFT.md` output was not adopted.
- Generated/bundled artifacts: `forge_bundle.js` (from `forge/src` via `forge/build.mjs`),
  `src/runner/fields.json` (`tools/derive_fields.mjs`), `src/runner/nested.json`
  (`tools/derive_nested.mjs`), `test/fixtures/envelope/*` (`tools/derive_envelope.mjs`). All four
  regenerate byte-identically; none is intentionally stale.
- `32b_DATA_pool.json` is consumed (bundled), not regenerated. `45d`/`45g` remain unused by forge;
  the `45g.tag_power_max` bound is still gated out and still has a test.
- Package pins unchanged: superjson 2.2.6 bundled; `@trpc/*` 11.18.0, zod 4.4.3, uploadthing 7.7.4
  read for protocol only.

## Live-game statement

- Live requests to `theninja-rpg.com`: **none**.
- Game writes: **none**.
- Session cookies or credentials obtained, requested, synthesised or exposed: **none**.
- The game source was read from a local checkout and never run.
- Checks NOT performed, and which must not be treated as verified: Firefox Android +
  ViolentMonkey `document-start` timing on `/forge`; `window.stop()` against the real 404;
  `navigator.storage.persist()` prompt behaviour; Clerk session refresh/expiry during a long real
  job; real production cookie/auth continuity; real rate-limit clock skew. The code pauses or fails
  closed when those assumptions break — an argument from the code, not a measurement.

## Findings a reviewer should weigh

1. **Two committed manifests carry keys the live server drops.** Verified absent from the
   validators at the pin AND at `e02f8159`: five quest edits (`push/27, 30, 33, 34, 35`) re-assert
   `raidEndsAt`, `raidCaptureDeadline`, `raidGracePeriodEnd` (drizzle columns, not validator
   fields); `push/46` gives every `start_battle` objective an `image` the objective does not define.
   Forge refuses those manifests pre-send. Both are pinned by a test so they cannot be re-read as
   false positives. **Editing them is dauntless's call, not this pass's.**
2. **One change outside `forge/`:** `harvest.py verify` treated an entry with `state=error` as a
   SKIP, so a bundle holding a failed push could exit 0 as "verified". It is now an `ERROR` that
   fails the gate. Checked against every existing inbox bundle: no verdict changes. This widens the
   Lane A review surface by eight lines.
3. **`skipPreflight` no longer disables safety checks** in forge (it still does in the old builder).
   Every check fires only on data the entry carries, so a partial quest edit needs no bypass. A
   manifest relying on the bypass to smuggle a genuine violation past would now be refused.
4. **L13 on an `ai` create** is not required (no `hidden` column at the pin) and `hidden` is accepted
   and dropped rather than refused. That is a small softening of the unknown-key rule, argued in
   `validate.mjs`; attack it if you disagree.
5. **The pool code pattern was widened** to `[A-Z]{1,2}\d{1,2}`. The builder's `\d{2}` never matched
   A1-A3, so those neither resolved nor tripped the guard. A code-shaped string that is not in the
   pool now fails closed.

## Known debt / deviations / not begun

- Captures still ignore `select`/`scope`; consequence measured: `harvest.py index` lists a forge
  bundle's capture calls but has no rows, so `get`/`names`/`assets` answer nothing from one.
  Verification of writes does not depend on it.
- A capture-only manifest still cannot start a job (`journal.open()` refuses an empty item list).
  Pre-existing; untouched.
- Clock skew beyond a second or two remains a residual budget risk; the strict window and the 0.5
  margin absorb the rest.
- Clerk refresh on `/forge` remains inferred, mitigated by the SESSION pause, not solved.
- `selfcheck.py` remains red on `main` and here identically (TNR-03).
- Out of scope and not begun, per brief §12: the native shell, tab-eviction elimination, capture
  trimming, cosmetic redesign, any balance/reward/content change, automatic deletion, hidden game
  traffic for Clerk.

## Open decisions for dauntless

1. **Install `state/staged_workflows/release_pin.yml`** at `.github/workflows/release_pin.yml`
   through the GitHub web UI. This is the one action Fable cannot perform (the PAT cannot push
   `.github/workflows/`); no credential workaround was attempted. Until it lands, a push to `main`
   that changes `forge_bundle.js` does not pin the forge loader.
2. **The two manifest findings above** — edit those manifests, or accept that forge refuses them.
3. The first browser smoke test and any live job remain dauntless's, after review. No production
   mutation is authorised by this pass.

## Acceptance gate (brief §15)

1-9 are met in this tree on the evidence above. 10 (independent approval of the exact frozen SHA)
and 11 (the browser smoke and the first live manifest) are not, by construction.

HEAD_SHA: recorded in the handoff message accompanying this document; the branch head at the time
of writing is the tip of `claude/builder-app-production-readiness-kelsib` and is frozen until the
review returns.
