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
| head (FROZEN) | see "Correction round 1" below |
| `main` observed at handoff | `4a506dff0af7dd499c8b580af4f0c14fdfc48c1c` |
| integration target | `main`, when the review passes. Not merged here. |

### Review rounds

| round | reviewed head | review | verdict |
|---|---|---|---|
| 1 | `c388ea65e0783f4e8ad0670949f23dfc420b205f` | `chatgpt/review-builder-app-readiness-c388ea6` @ `06392fbbe1d2893a98ff16ee4f430e9ee0218297`, `docs/reviews/BUILDER_APP_READINESS_C388EA6_REVIEW.md` | CHANGES REQUIRED: 2 blockers |
| 2 | this handoff's frozen head | pending | — |

Round 1 reviewed `c388ea6`, which is `5998db2` (the round-1 handoff commit) plus the automatic
skillpack rebuild the harvest.py change triggered. Both blockers are corrected below; nothing else
was touched.

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
| `npm test` | **202 tests, 202 pass, 0 fail** (199 at round 1; 168 at `4062268`) |
| `npm run build` | `wrote /home/user/tnr-tools/forge_bundle.js (342.2 KB)` |
| rebuild diff: `cp forge_bundle.js /tmp/b.js && npm run build && cmp /tmp/b.js ../forge_bundle.js` | identical — **deterministic**, and the checked-in bundle matches a fresh build |
| `npm run fixtures` then `diff -r` against the pre-run copy | **byte-identical**; no adapter fixture input changed |
| `node tools/derive_fields.mjs <pin> \| cmp - src/runner/fields.json` | **byte-identical** — `fields.json` reproduces from the pin |
| `node tools/derive_nested.mjs <pin> \| cmp - src/runner/nested.json` | **byte-identical** — `nested.json` reproduces from the pin |
| `node tools/derive_fields.mjs <game main 62af1b34> \| cmp - src/runner/fields.json` | **byte-identical** — the pin's field sets are production's today |
| `node tools/derive_nested.mjs <game main 62af1b34> \| cmp - src/runner/nested.json` | **byte-identical** — same for the nested key surface |
| `node tools/pin_relevance.mjs <pin> <game main 62af1b34>` | exit 1 with 3 flagged surfaces; each read individually; verdict below. The pin stays. |
| `node tools/check_release_pin.mjs` | 0 blockers, 1 pending install (the pre-integration workflow install) |
| `python3 skills/building-tnr-content/scripts/harvest.py verify <generated bundle>` | OK / FAIL / UNVERIFIED / ERROR for the four outcomes, `VERIFY FAILED`, **exit 1**; a clean bundle exits 0 |
| same, for a skipped orphan and for a pending write (round-2 regressions) | `UNVERIFIED`, **exit 1** — was exit 0 before the correction |
| same, over all 12 bundles in `harvests/inbox/` before and after both `harvest.py` changes | **no verdict changes** |
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
- Compared against the **actual current game `main`**, resolved fresh with `git ls-remote` at
  2026-09-09T01:44Z: `studie-tech/TheNinjaRPG@62af1b3405b10183b31f838c9a5f131d790460f1`. (Round 1
  compared only against this repository's sentinel snapshot `e02f8159`, which the review correctly
  called a different claim.)
- **Relevance verdict: nothing forge relies on changed.** `fields.json` and `nested.json`
  regenerated from a checkout of `62af1b34` are BYTE-IDENTICAL to the checked-in files — what the
  bundle validates against is what production's validators say today. Three of the 22 declared
  surfaces differ, all read: `root.ts` registers two new routers (`push`, `purchases`);
  `schema.ts` adds twelve device/purchase/store tables and their relations with no removals (no
  `userData` column moved, proved independently by the identical 157-key `ai` field set); and
  `constants.ts` is purely additive push/store/native constants plus one forum pagination constant
  (forge derives key sets and never enums, so a constant cannot make it reject what the server
  accepts). Everything else is byte-identical, including `trpc.ts`, all six content routers, all
  four validator files, the upload route, `proxy.ts`, `next.config.mjs`, `global-not-found.tsx` and
  `app/package.json`. Between the sentinel and current `main` the only changes at all are SEO,
  forum, comments and public-profile work. The pin is retained on that evidence; `docs/DRIFT.md`
  output was not adopted, and nothing was moved for being newer.
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

1. **Release-pin workflow install — not yet, and not by this handoff.**
   `state/staged_workflows/release_pin.yml` must be installed at
   `.github/workflows/release_pin.yml` (web UI; the PAT cannot push `.github/workflows/`, and no
   credential workaround was attempted) **before** the eventual `main` integration that changes
   `forge_bundle.js`, so that the integration commit itself triggers the immutable pin — installing
   it afterwards would not retroactively pin an already-landed bundle. It is a pre-integration user
   action after this correction passes review, not something to do now.
2. **The two manifest findings above** — edit those manifests, or accept that forge refuses them.
3. The first browser smoke test and any live job remain dauntless's, after review. No production
   mutation is authorised by this pass.

## Acceptance gate (brief §15)

1-9 are met in this tree on the evidence above. 10 (independent approval of the exact frozen SHA)
and 11 (the browser smoke and the first live manifest) are not, by construction.

## Correction round 1 (review of `c388ea6`)

Both findings accepted; neither rejected. Nothing else changed, no architecture moved, and forge's
own `jobOutcome()` semantics are untouched — the review is right that they were already correct.

### Finding 1 (HIGH, confirmed defect): a skipped or pending Forge write could still verify green

Reproduced first, through the real paths, before any code changed. A job whose only unresolved item
was an orphan resolved with `Runner.skip()` exported a bundle that `harvest.py verify` printed as
`SKIP … state=skipped` and exited **0** on ("verified"), while forge reported `outcome: unverified`
and the asset row the skip walked away from was still live. A bundle exported with a create still in
flight did the same.

Fixed in `skills/building-tnr-content/scripts/harvest.py::cmd_verify()`. A forge bundle (`cfg:
"forge"`, or entries carrying `forgeState`) now gets two rules no legacy bundle sees: a `skipped` or
`pending` entry is UNVERIFIED rather than a skip, and the bundle's own `outcome` must be `success`
before the gate exits 0 (a forge bundle with no `outcome` fails closed). Legacy semantics — where
those states meant a row the builder never attempted — are unchanged.

Regressions added in `forge/test/harvest.test.mjs`, all end to end through the real reconcile/skip
and export paths and the real `harvest.py`:

- an ambiguous create (two placeholder rows appeared while one create was in flight) reconciled to
  ORPHANED, resolved with the real `Runner.skip()`, exported: verify prints `UNVERIFIED Orphan`,
  says `VERIFY FAILED` and **exits 1**; the test also asserts the server row is still present;
- a job exported with its create still in flight: `UNVERIFIED Pending`, non-zero exit;
- a legacy-shaped bundle with a `pending` row: still `1 ok … 1 skipped`, **exit 0**;
- the same shape marked as forge with no `outcome`: **exit 1**;
- the round-1 clean forge bundle still exits 0.

Both new failing cases were confirmed red against the pre-fix `harvest.py` and green after.

### Finding 2 (BLOCKER, evidence gap): relevance proved against a sentinel, not production

Corrected by rerunning the whole gate against the actual game `main`, resolved fresh (not assumed
from the review): `62af1b3405b10183b31f838c9a5f131d790460f1` at 2026-09-09T01:44Z. Both derived
contracts regenerate byte-identically from a checkout of that head; three declared surfaces differ
and each was read individually (details in "Source / provenance" above and in
`docs/BUILDER_APP_NOTES.md`). `app/drizzle/constants.ts` was ADDED to the declared surfaces so that
an enum-list change is seen by the gate rather than sitting outside it — that is why the surface
count is 22, not 21. **The pin stays at `345d18ac`.** If game `main` advances before integration,
rerun `node tools/pin_relevance.mjs <pin-checkout> <new-head-checkout>`.

### Gates rerun for this correction

Every command in the Verification table above was rerun on the corrected tree; results as tabulated
(202 tests, deterministic bundle, byte-identical fixtures and both derived artifacts, unchanged
legacy harvest verdicts, `selfcheck.py` red identically to `main`).

### Wider scope

None. Two files changed for the fix (`harvest.py`, `forge/test/harvest.test.mjs`), one tool gained a
declared surface (`forge/tools/pin_relevance.mjs`), and the notes/handoff were updated. `forge_bundle.js`
is byte-identical to round 1 — no shipped client code changed in this correction, which is why a
narrow re-review is appropriate.

### Live-game statement for the correction

Zero live requests to `theninja-rpg.com`; zero game writes; no session cookie or credential of any
kind was used, requested or synthesised. The game source was read from a local checkout at two
commits and never executed. `git ls-remote` and a shallow fetch against `github.com` are the only
network calls, and they touch the public game REPOSITORY, never the game.

### Frozen head

Changing `skills/building-tnr-content/scripts/harvest.py` triggers an automatic skillpack rebuild
commit on this branch after the authored commits land, exactly as it did in round 1. The frozen SHA
for review is the remote branch head AFTER that auto-commit settles; it is recorded in the handoff
message accompanying this document and must be re-read from
`origin/claude/builder-app-production-readiness-kelsib` rather than assumed from an authored commit.
