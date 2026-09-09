# Repository simplification audit review — d35889d

## Target

- Repository: `perseverance484/tnr-tools`
- Reviewed branch: `chatgpt/repo-simplification-audit`
- Exact reviewed head: `d35889d2034872046faf817f5f16bc904a8e7747`
- Base: `main` @ `991e32d4651a147e32d08474ea87f3ce80bc27f7`
- Report under review: `docs/reviews/REPO_SIMPLIFICATION_AUDIT.md`
- Contract-reconciled snapshot named by that report: `e52dcc2536998dfc1e539a1d034317ae5f8dc154`
- Reviewer: Fable / Claude Code. Review only: nothing on `chatgpt/*` was modified.
- Mode: full relevant audit of `991e32d..d35889d`, executed in a throwaway worktree.

No live-game request, game write, session cookie, or credential was used. The game source was read
from local checkouts of `bdec2883`, `345d18ac` and `62af1b34` and was never executed.

## Verdict

**APPROVE WITH CHANGES.**

The engineering is sound. Several changes are genuine safety improvements, and the audit's central
claim — that the 45d/45g provenance was reconciled against the exact upstream commit rather than
suppressed — is true and independently verified below. One finding (F1) should be resolved, or
explicitly deferred by dauntless, before this lands on `main`. Nothing found here weakens live-write
safety, and Forge's mutation-safety surface is untouched.

## Claims reproduced and confirmed

Every row below was executed against `d35889d` in a clean worktree, not read off the report.

| claim | how it was checked | result |
|---|---|---|
| Forge source/tests unchanged by the audit | `git diff 5ffb735..d35889d -- forge/src forge/test` | only the five regenerated error fixtures differ |
| nothing in Forge changed after the audit's verified snapshot | `git diff 3a6abe6..d35889d -- forge/ forge_bundle.js forge_loader_user.js` | empty; the claim holds |
| Forge suite green | `cd forge && npm ci && npm test` | 202 tests, 202 pass |
| fixtures are now path-stable | `npm run fixtures` from a checkout at a **different absolute path**, then `diff -r` | byte-identical |
| bundle reproducible | `npm run build` then `cmp` | byte-identical |
| normalization limited to non-contract context | read the whole fixture delta | only `derive_envelope.mjs:85:15` → `:0:0` inside `data.stack`; `message`, `code`, `data.code`, `httpStatus`, `path`, `zodError` and all dependency frames untouched |
| 45d/45g changed only in provenance | recursive compare of `991e32d` vs `d35889d` excluding `_provenance` | identical for both, and for root `45g_DATA_checks.json` |
| the new provenance label is true | hashed the real bytes of every file in `_provenance.source_sha256_16` at `bdec2883748f029a0ecb93505adfdcbae6851fe9` | **9/9 match** |
| the idsWithNumberField invariant "remains checked" | simulated a regenerated 45c that lost the family, ran the branch's `selfcheck.py --generated` | 10 errors, exit 1 — the guard survives as `check_cross_module_refs()` |
| the factory selftest alone would not catch it | same simulation | factory selftest still 20/20, so the retained guard is doing the work |
| answer layer reproduces from canonical seeds | ran `build_answers.py --repo . --out answers` | zero diff against the committed `answers/` |
| deterministic ZIP loses nothing real | entry-set diff, old vs new `building-tnr-content.zip` | 73 → 72 entries; the only loss is one `__pycache__` entry; `SKILL.md` still at zip root |
| scrub gate still fail-closed | read the full step body | empty secret → fail, zero non-empty patterns → fail, any hit → fail; logic preserved exactly |
| catalog filtered-capture rule | read `full_name_listing()` + ran `catalog_sync.py --selftest` | filtered captures return `(kind, None)` and are skipped for absence; matches `harvest.py`'s own definition of "filtered" |
| release pin is immutable and correct | read the loader, resolved the pinned commit, hashed the bundle at it | `@require` is a 40-hex commit; `forge_bundle.js` there is byte-identical (`83b99fea…`) to the reviewed bundle |
| `emit_index` was dead | `git grep emit_index 991e32d` | one hit: the definition |
| repository gates | doctrinemap, `render_doctrine --check`, `build_packs --check`, lawmap | all exit 0 (lawmap 5 warnings, baseline) |

Release-pin convergence, which the report asked to be checked specifically: pinning **both** loaders
to `GITHUB_SHA` on every run is correct, because a later run's SHA necessarily contains the earlier
run's bundle, and the workflow triggers on the bundle paths themselves, so every bundle change
retriggers it. The residual cost is that a Forge-only bundle push now also rewrites
`builder_loader_user.js` to a new URL serving identical bytes — churn, not error.

## Finding 1 — MEDIUM — an approved ruling is stranded by the packaging rewrite

**Classification:** ruling fidelity / distribution size. Not a regression against installed behaviour.

### Evidence

`state/status.json` records, under `ruled_this_session`:

> SKILL ZIP SCOPE: archive-only art (`data/rank_icons/`, `data/frames/`, `*_raw.png`) is excluded
> from skill zips. Verified nothing in SKILL.md, scripts/ or references/ reads any of it.
> producing-tnr-art.zip 18.4MB -> 80KB. A 2MB per-zip CI size guard was added so the pattern list
> cannot rot silently.

`.github/scripts/pack_skills.py` packages every Git-tracked file under each skill directory and
implements neither the exclusion list nor the size guard. Measured on this branch:

```
producing-tnr-art.zip = 19,298,833 bytes
  13.38 MB  data/rank_icons
   5.83 MB  data/frames
```

— 99.5% of the archive is exactly the two directories the ruling excludes.

The ruling's vehicle, `state/staged_workflows/skillpack.yml`, still declares itself "REPLACES
`.github/workflows/skillpack.yml`", but installing it now would revert deterministic packaging, the
`catalog_sync --selftest` gate and the shared writer. So the ruling can no longer be landed as
written, and the audit's debt item 3 treats the staged workflows generically without noting that
this one carries an unimplemented decision.

### Practical consequence

Every `skills/**` change rewrites a 19MB binary in a repository that already ruled against blob
growth, and the "pattern list cannot rot silently" guard does not exist on any path that can now be
installed.

### Smallest robust correction

Implement the exclusion patterns and the 2MB per-ZIP guard inside `pack_skills.py` (the natural
home, and it makes the staged file retirable), or record explicitly in the audit and in
`state/status.json` that the ruling is consciously deferred. Either is fine; silently losing it is
not.

## Finding 2 — LOW/MEDIUM — concision was applied to load-bearing documentation

**Classification:** audit-trail erosion.

### Evidence

Removed from live artifacts, with no replacement in place:

- `scrub.yml`'s header: that the gate and the `SCRUB_STRINGS` secret must be installed together,
  that the old gate warned instead of failing, and the pointer to `scrub_check.py` with its pattern
  file kept outside the repo;
- `check_release_pin.mjs`'s header: why a floating `@require` is unsafe and what the marker means;
- `derive_envelope.mjs`'s per-scenario rationale, including "MIXED batches: the spec forbids
  inferring per-item outcome from HTTP status. Prove why." — the reason that fixture exists;
- workflow step names that stated the guarantee: "Privacy gate (fail-closed, multi-pattern)",
  "Record drift (baseline + DRIFT.md, never adopt)", "Fetch upstream source (public, read-only)";
- `selfcheck.py`'s actionable hint on a missing generated file ("The scripts read it from the
  working directory; copy the generated files in first") — now a bare "not found in `<dir>`".

Most of that text survives only in `state/staged_workflows/` copies, which the audit's own debt item
3 proposes to retire.

### Practical consequence

The behaviour is unchanged, but the reason for it is now recoverable only from history or from files
slated for deletion. In this repository the audit trail is part of the product: the same reasoning
that keeps Forge's comments citing source lines applies to the workflows that guard the repository.

### Smallest robust correction

Keep one line of "why" attached to each guarantee in the live artifact, and capture the operational
notes (secret coupling, local mirror) in `docs/` before retiring any staged copy.

## Finding 3 — LOW — "provenance reconciled" is not "contracts current"

**Classification:** precision of a closing statement.

### Evidence

The reconciled stamp is `git:studie-tech/TheNinjaRPG@bdec2883 (2026-08-29)` with
`extracted: 2026-09-09`. Commit dates from the public repository:

| commit | date | role |
|---|---|---|
| `bdec2883` | 2026-08-29 | new contract provenance |
| `345d18ac` | 2026-08-31 | the Forge pin |
| `62af1b34` | 2026-09-08 | game `main` at review time |

`farmYieldItemId` is absent from `combat.ts` at `bdec2883` and present at both later commits, which
is exactly why 45d carries 59 item fields where the Forge pin has 71, and why Forge derives its own
`fields.json` instead of consuming 45d. The reconciliation is correct **for `bdec2883`**; the
contracts are still two days behind the Forge pin and ten behind production.

### Practical consequence

The audit closes the mismatch and says it "should not be carried forward as review debt". True of
the *label*; a reader could take it as the contracts being current, and the known 45d gaps remain.

### Smallest robust correction

One line in the audit and in the selfcheck note: the reconciled contracts describe `bdec2883`, which
is behind both the Forge pin and current `main`, and the 45d field gaps are a pin difference rather
than an extraction fault.

## Finding 4 — LOW — `commit_generated.py` rebase-without-regenerate, concretely

**Classification:** the report's own flagged caveat, verified and narrowed.

Cross-workflow races are safe: skillpack losing to release-pin touches disjoint files. The residual
is intra-workflow ABA. Skillpack run A builds the ZIP from `skills@X`; run B builds it from
`skills@Y`; if A reaches its push after B has pushed, A rebases its X-derived ZIP onto B and
overwrites the Y-derived one. Nothing retriggers, because `dist/*` is not a trigger path, so `dist`
stays stale until the next `skills/**` change. `cancel-in-progress: true` narrows the window but
does not close it: a run already inside its push step completes.

### Smallest robust correction

After a successful rebase, re-run the generator (or diff the artifact against a fresh build) before
pushing. Skillpack already double-builds each ZIP for the determinism check, so the added cost is
negligible.

## Finding 5 — LOW — a CI trigger gap between Forge and the skill scripts

`.github/workflows/forge.yml` triggers on `forge/**`, the bundle and loader, and the release-pin
files. Forge's own suite **executes** `skills/building-tnr-content/scripts/harvest.py`
(`forge/test/harvest.test.mjs` spawns it three times), so a change to that script can break the
Forge tests without triggering the Forge workflow. This coupling was introduced by the readiness
pass, not by this audit, but this branch is where the Forge workflow was created.

### Smallest robust correction

Add `skills/building-tnr-content/scripts/harvest.py` to `forge.yml`'s `paths` filters.

## Finding 6 — informational

1. `check_release_pin.mjs` now inspects only the **first** workflow file that exists
   (`WORKFLOWS.find`), so the deliberately retained `state/staged_workflows/release_pin.yml` mirror
   is never verified; and `workflow.includes(bundle)` is weaker than the previous assertion that the
   bundle appears in the `paths:` filter — a mention in a comment would satisfy it.
2. `build_answers.py` silently ignores any file in `harvests/seed/` that is not one of the five
   routed names. The new explicit routing is the right call, but an unrouted seed drop should warn
   or fail rather than disappear.
3. The audit's "full generated-data selfcheck … 0 errors" is CI-context-specific: the workflow
   copies the generated contracts into the working directory first. A plain checkout still reports
   one error (`45d_DATA_entity_schemas.json not found in <root>`). Worth stating, since the sentence
   reads as if `selfcheck.py` is globally green.
4. `emit_index()` was genuinely dead, but the `4x_INDEX_*.json` files it targeted are live inputs to
   both `catalog_sync.py` and the new answer generator, and now have no in-repo regenerator at all.
   Worth one sentence so a future reader knows the capability was removed, not merely tidied.
5. Forge captures carry a row **count** rather than `data`, so `catalog_sync.py` skips a Forge
   bundle's captures entirely. That matches the boundary already documented in
   `docs/BUILDER_APP_NOTES.md`; no action, recorded for cross-surface clarity.

## Verified improvements

- **Contract provenance reconciliation.** Payloads semantically identical, all nine recorded source
  hashes match the real bytes at `bdec2883`, and the adoption did not lean on a vacuous
  `schema_diff.py` result for 45g. This is the strongest part of the branch.
- **`selfcheck.py` correctness.** The old implementation appended cross-module errors *after*
  printing its error list, so a late error changed the exit code invisibly. Fixed, and the
  cross-module guard is retained rather than dropped.
- **Catalog absence rule.** Treating a filtered `getAllNames` capture as authoritative absence
  contradicted the repository's own evidence rule and could have tombstoned real rows; the fix is
  correct and covered in both directions by the new selftest.
- **Deterministic packaging.** Fixed timestamps, tracked files only, and a double-build SHA check in
  CI. Checkout mtimes and scratch files can no longer move distributable bytes.
- **Fixture path stability.** Verified from a foreign path. The normalization is limited to the
  generator's own frame and the checkout prefix; dependency frames keep their line numbers, so a
  dependency bump would still show up.
- **Release pin.** Both loaders converge on the latest run, and the pinned URL demonstrably serves
  the exact reviewed bundle bytes.

## Not verified

Two of the report's evidence classes cannot be checked from the repository alone: the cited GitHub
Actions run IDs, and the observed push-race behaviour on production `main`. For the runs I verified
the tree they claim to cover instead (`3a6abe6..d35889d` touches nothing under `forge/`).

## Next permitted step

Resolve F1 (implement the exclusions and size guard in `pack_skills.py`, or record the ruling as
deferred), and take F2 and F5 as cheap follow-ups. F3, F4 and F6 are documentation and hardening
notes that do not need to block integration. A narrow re-check is appropriate afterwards: no
architecture or safety assumption changed.

Nothing in this review authorises operating the game. A green branch is not a live-write approval.
