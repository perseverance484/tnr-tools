# Repository precision and simplification audit

Status: **USER-DIRECTED INTEGRATION CANDIDATE**  
Base: `main@991e32d4651a147e32d08474ea87f3ce80bc27f7`  
Branch: `chatgpt/repo-simplification-audit`  
Corrected executable snapshot: `b9c57daf04ec39f71a7ed28285a343ea6467096d`

## Scope and judgment

This audit targeted hand-written repository code for accidental complexity, duplicate mechanisms, misleading tests, nondeterministic generation, and weak repository-maintenance invariants. It did **not** flatten Forge's journal, crash recovery, mutation ambiguity, reconciliation, or read-back state machines: those model realistic production failures.

No live-game request, write, cookie, credential, or production action was used.

## Simplifications and fixes

- Repository-generated commits use one repo-owned rebase/retry helper instead of several ad hoc write-back mechanisms.
- Answer generation reads explicit canonical seed files instead of filesystem-mtime heuristics; regeneration produced no answer-layer diff.
- Skill ZIPs are deterministic, contain only tracked runtime files, exclude archive-only art, and fail above 2 MiB.
- Duplicate self-check implementations were collapsed; counted errors are now always printed.
- Doctrine and pack renderers lost dead/repeated work while retaining byte-stable outputs.
- Release pinning converges both current loaders on every bundle-triggered run.
- Forge has read-only CI for runtime dependency audit, 202 tests, fixture parity, and bundle parity.
- tRPC fixtures no longer encode checkout paths or the fixture generator's own line numbers.
- Filtered `getAllNames` captures no longer become false absence evidence in catalogs.
- The dead `refresh_catalogs.py` INDEX emitter was removed; its CLI now describes what it actually writes.
- Generated contract provenance was reconciled across 45c/45d/45e/45f/45g to the same pinned source family.

## Contract provenance reconciliation

The earlier mismatch was real: 45c/45e/45f identified `studie-tech/TheNinjaRPG@bdec2883`, while 45d/45g still identified an older ZIP drop.

The branch re-extracted from exact upstream commit `bdec2883748f029a0ecb93505adfdcbae6851fe9` and proved before adoption:

- constructor invariants: 5 unions, 128 variants, 0 errors;
- structural diffs for 45c/45d/45e: 0 breaking changes and 0 additions;
- recursive semantic payload equality for 45d and 45g after removing `_provenance`;
- 45g hand-held law blocks unchanged;
- full selfcheck after adoption: factory 20/20, validator 16/16, 0 errors.

This closes the **internal provenance split only**. `bdec2883` is older than the Forge source pin `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` and older than the current upstream/sentinel source. The current 45d item-field differences reported by the sentinel are therefore a source-pin/currentness issue, not an extractor/provenance mismatch. No newer contract set was adopted in this audit.

## Independent Fable review and corrections

Fable independently reviewed `d35889d2034872046faf817f5f16bc904a8e7747` at `claude/builder-app-production-readiness-kelsib@e5d7ef447ac0512cfb09b3fe2c6dd46ccc7b70f3`. The durable review is `docs/reviews/REPO_SIMPLIFICATION_D35889D_REVIEW.md` on that branch.

The user then explicitly assigned ChatGPT the correction pass and immediate `main` integration. That means the corrected snapshot below does not receive a second Fable re-review before integration; the correction surface is instead mechanically re-gated in full.

### F1 — skill ZIP ruling fidelity — CLOSED

`.github/scripts/pack_skills.py` now excludes:

- `data/rank_icons/**`;
- `data/frames/**`;
- `*_raw.png`.

It also fails if any skill ZIP exceeds 2 MiB. The installed skillpack workflow remains deterministic and its staged historical copy is now a compatibility mirror, so following the old board pointer cannot reinstall the former nondeterministic implementation.

Skillpack run `34415837438`: **success**.

- `building-tnr-content.zip`: 382,021 bytes;
- `producing-tnr-art.zip`: 80,582 bytes;
- both repeated builds had identical SHA-256 values;
- doctrine/pack checks and `catalog_sync.py --selftest` passed.

### F2 — load-bearing rationale — CLOSED

Minimal rationale was restored without bringing back long historical comments:

- scrub step names the fail-closed `SCRUB_STRINGS` requirement;
- release-pin checker states why floating bundle URLs are unsafe;
- mixed tRPC fixture scenario states why shared HTTP status cannot determine per-item outcome;
- schema-sentinel step names state public/read-only fetch and signal-only/no-adoption behavior;
- missing selfcheck contracts now print an actionable `--generated`/sync hint.

### F3 — provenance wording — CLOSED

The audit now explicitly distinguishes **provenance reconciliation at `bdec2883`** from **contract currentness**. The sentinel/current-source adoption process remains separate and fail-closed.

### F4 — regenerate-after-rebase proposal — NOT REPRODUCED

A disposable Git repository reproduced the alleged race shape against the actual Git behavior used by `.github/scripts/commit_generated.py`:

- stale generated commit rebased over a newer commit changing the **same artifact**: rebase conflicts and aborts;
- stale generated commit rebased over a **disjoint** remote change: rebase succeeds and the artifact is preserved.

The claimed clean-rebase overwrite of a newer same-path generated artifact therefore was not reproduced. No regenerate-after-rebase loop was added without a failing case.

### F5 — Forge/harvest CI coupling — CLOSED

`.github/workflows/forge.yml` now triggers on `skills/building-tnr-content/scripts/harvest.py` for both push and pull request events.

Forge run `34415837435`: **success**.

- production dependency audit: 0 vulnerabilities;
- tests: 202/202 pass;
- regenerated envelope fixtures: byte-identical;
- fresh `forge_bundle.js`: byte-identical.

### F6 — informational notes

The remaining observations are not integration blockers. Historical staged workflows should be retired only when their remaining references are deliberately cleaned up; explicit answer-seed routing and release-pin mirror checking can be hardened later if a concrete failure case appears.

## Other verification evidence

Earlier successful branch evidence remains applicable:

- deterministic answer generation: no generated answer changes;
- concurrent generated writers: both writers completed after the shared retry rewrite;
- catalog filtered-list selftest: pass;
- contract exact-source probe `34339706768`: success;
- contract adoption `34339887245`: success;
- packaged contract propagation `34340007228`: success;
- correction scrub `34415837515`: success.

## Deliberately retained complexity

- Forge mutation journal/reconciliation/crash tests and state transitions;
- validators and content tools whose branching maps directly to game contracts;
- `forge/src/ui/dom.mjs::installCss()` until a real Forge bundle release justifies source/bundle churn.

## Remaining non-blocking debt

1. `forge/package-lock.json` root metadata still says 0.1.0 while `forge/package.json` is 0.2.0; normalize during an intentional lockfile/dependency refresh.
2. Plain `npm ci` reports three high dev-tool advisories; `npm audit --omit=dev --audit-level=high` is clean. Do not force-upgrade without reviewing toolchain impact.
3. Historical staged workflow copies still exist where current state/tests reference them. Retire them deliberately, not blindly.
4. `session_open.py` still does not run the full selfcheck. The former provenance blocker is gone; wiring it remains a separate startup/tooling change.
5. Current upstream contract drift remains signal-only until the repository's structural adoption process is intentionally run.
6. The Forge DOM stylesheet helper remains a future readability refactor when a bundle release is already being cut.

## Integration

Before integration, re-verify live `main`; automation may have advanced it. Merge normally so current sentinel/content history is preserved. Do not force-update `main`.

Nothing in this audit authorizes operating the live game.
