# Repository precision and simplification audit

Status: **READY FOR INDEPENDENT REVIEW**  
Implementation snapshot: `3a6abe6229192fba382c81c7e8cc8b33161e0ed7`  
Base: `main@991e32d4651a147e32d08474ea87f3ce80bc27f7`  
Branch: `chatgpt/repo-simplification-audit`

## Objective

Audit hand-written repository code for precision, concision, accidental complexity, duplicate mechanisms, and tests that protect impossible or tautological states. Rewrite where the simpler implementation preserves the repository's safety invariants. Do not weaken live-write safety merely to reduce line count.

No live-game requests, writes, cookies, credentials, or production actions were used.

## Review judgment

The Forge mutation journal, write-ahead transitions, crash recovery, ambiguous-response handling, reconciliation, read-back, and rate-limit tests are mostly necessary complexity. They model browser crashes, uncertain mutations, multi-tab execution, and production read failures that can happen. This audit did **not** collapse those state machines for aesthetic line-count reduction.

The largest avoidable complexity was instead in repository maintenance: independent writers racing on Git refs, filesystem-mtime source discovery, nondeterministic ZIP packaging, duplicate self-check implementations, pre-install workflow state that survived installation, and fixtures that encoded developer checkout paths and generator line numbers.

## Changes

### Repository writers

Added `.github/scripts/commit_generated.py` and routed generated-file writers through one repository-owned rebase/retry path. This replaces several ad hoc write-back mechanisms.

The motivating failure was observed on production `main`: `skillpack` completed its gates, then its push was rejected because `release-pin` advanced `main` first. On this branch, concurrent `answers` and `skillpack` runs both completed successfully using the shared writer path.

`relay.yml` rebuilds its merge against fresh remote state on retry rather than trying to push a stale merge. `answers.yml`, `skillpack.yml`, `regen_schemas.yml`, `scrub.yml`, and `release_pin.yml` were reduced around repository-owned scripts.

### Answer generation

`.github/scripts/build_answers.py` now reads the explicit canonical seed files under `harvests/seed/` rather than recursively guessing the newest source from filename patterns and filesystem mtimes. Hot inbox records remain a separate delta input.

Validation: the rewritten generator produced the five entity answer files plus `hot.json`; the workflow reported `no generated changes`. The simplified source selection therefore reproduced the existing answer layer byte-for-byte.

### Skill packaging

Added `.github/scripts/pack_skills.py`. ZIP timestamps and permissions are deterministic, and only Git-tracked files are packaged. This prevents checkout mtimes, `__pycache__`, and scratch files from changing distributable bytes.

Validation: the workflow built each ZIP twice in one run and verified identical SHA-256 values. The tracked-file correction then passed the full `skillpack` gate.

### Session and consistency tooling

`session_open.py` and `session_close.py` were simplified. A session-close self-test that appended text and then asserted the string differed was removed; it tested Python/file-string mechanics rather than a repository invariant.

`selfcheck_for_bundle.py` is now a compatibility wrapper around `selfcheck.py` instead of a second implementation. The prior `selfcheck.py` could append cross-module errors after printing its error list, producing a failing exit code without displaying the new error. The single implementation now reports what it counts.

Generated-contract provenance checking now compares source identity instead of assuming independently extracted contracts must share an extraction date. The existing 45c versus 45d/45g source mismatch remains visible; it was not simplified away.

The old long `idsWithNumberField` recovery explanation was removed because `schema_extract.py` now resolves that cross-module family directly. The regression invariant remains checked.

### Doctrine and pack renderers

Removed dead/repeated work in `render_doctrine.py` and `build_packs.py` while retaining deterministic rendered bytes. An initial rename of `MARK`/`BMARK` broke `doctrinemap.py`; CI caught it and the existing interface names were restored instead of propagating needless churn.

Validation after correction: doctrine map clean, doctrine projections current, packs/TOCs current.

### Release pinning

The old release-pin workflow combined `cancel-in-progress: true` with `git diff HEAD~1 HEAD` target selection. If a run for one bundle were cancelled by a later bundle commit, the latest run could pin only the later bundle and leave the first loader stale.

`.github/scripts/pin_release.py` now pins **both current bundle loaders on every release-pin run** to `GITHUB_SHA`. The latest successful run therefore converges both loaders to the repository state it contains regardless of which bundle triggered it.

`forge/tools/check_release_pin.mjs` was reduced around the installed workflow and rejects the old last-commit-only selection pattern. `state/staged_workflows/release_pin.yml` remains only as a compact compatibility mirror because existing test fixtures still exercise that path; the installed workflow is authoritative.

### Forge CI and fixtures

Added `.github/workflows/forge.yml` with read-only repository permissions. It runs:

1. `npm ci`
2. `npm audit --omit=dev --audit-level=high`
3. `npm test`
4. `npm run fixtures` followed by byte diff of `test/fixtures/envelope`
5. `npm run build` followed by byte diff of `forge_bundle.js`

The first fixture parity run exposed absolute checkout paths in tRPC stack strings. After path normalization, the next run exposed source line numbers from `tools/derive_envelope.mjs`. Both are incidental generator context, not the transport contract. The generator now canonicalizes its own file URL and its own stack locations to `:0:0`; dependency stack frames and protocol payloads remain intact. Five checked error fixtures were regenerated once to that stable representation.

## Verification evidence

Exact implementation snapshot `3a6abe6229192fba382c81c7e8cc8b33161e0ed7`:

- Forge Actions run `34306910241`: **success**.
  - `npm ci`: success.
  - runtime dependency audit: success.
  - `npm test`: success; the same suite reported 202/202 passing on the immediately preceding exact-code run and no test files changed afterward.
  - regenerated envelope fixtures: byte-identical.
  - fresh `forge_bundle.js`: byte-identical.
- Scrub run `34306910159`: **success**.
- Earlier branch `skillpack` validation: doctrine projections and packs/TOCs current; deterministic ZIPs reproduced on repeated builds.
- Earlier branch `answers` validation: simplified generator produced no answer-layer diff.

Plain `npm ci` reports three high-severity advisories in the development/test dependency graph. The production-only audit passes, so these are **not shipped runtime dependency vulnerabilities**. They remain dev-tool maintenance debt; do not use `npm audit fix --force` without reviewing the dependency changes.

## Deliberately not rewritten

- Forge's journal/reconciliation/crash state machine and adversarial tests: realistic production failure modes, not speculative edge cases.
- `forge/src/ui/dom.mjs::installCss()`: it can likely become a normal `<style>.textContent` path and lose the constructable-sheet/rule-splitting fallback. That is a production bundle change requiring a Forge version/release cycle; the readability gain did not justify expanding this audit into another deployed-bundle release.
- Generated contract source mismatch: `45c_DATA_constructors.json` and `45d_DATA_entity_schemas.json` / `45g_DATA_checks.json` do not currently share source provenance. This needs a source extraction + structural diff + adoption task, not suppression of the warning.

## Remaining non-blocking debt

1. `forge/package-lock.json` root metadata still identifies the package as `0.1.0` while `forge/package.json` is `0.2.0`. `npm ci` is reproducible and passes, but the metadata should be normalized during the next intentional dependency/lockfile refresh rather than hand-editing the lockfile.
2. The three high dev-tool advisories should be reviewed during that dependency refresh. Runtime audit is currently clean.
3. Other installed workflows still have historical copies under `state/staged_workflows/`. Retire them only after resolving every remaining reference; do not delete them blindly.
4. The Forge DOM stylesheet helper is a good future small refactor when a bundle version is already being cut.

## Independent review request

Fable should review the frozen handoff SHA containing this report, with `3a6abe6229192fba382c81c7e8cc8b33161e0ed7` as the executable implementation snapshot. Review primarily for:

- correctness of `commit_generated.py` under concurrent writers and conflicts;
- release-pin convergence when runs are cancelled/coalesced;
- determinism and contents of `pack_skills.py`;
- whether the answer generator's canonical seed routing loses any legitimate source class;
- fixture normalization being limited to non-contract local stack locations;
- whether any simplified workflow lost a required trigger, permission, or failure mode;
- any accidental weakening of self-check/provenance diagnostics.

Do not use live-game requests during review. A green GitHub branch is not authorization to operate the game.
