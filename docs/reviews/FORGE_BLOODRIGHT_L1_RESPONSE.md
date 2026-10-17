# Bloodright follow-up: explicit saved-binding repair

The user supplied Claude Code's independent N1 verification on 2026-10-09 (review dated
2026-10-08). It closed N1 at PR #29 `27f859af97dbc9fa52b45e5d745169d6e9c47b95`
and confirmed PR #30 `ed982d5e3a317a5c004341a5af37005056b7f07c` retained the approved
pilot values. L1 remained: after a target was deleted, its saved binding could only be
removed by manually editing browser storage.

## Correction

The job screen now offers **Forget saved binding** for a FAILED or VERIFIED Bloodright
item whose recorded ID still matches the saved ID. Confirmation names the record and
explains replacement/duplicate risk. The operator must independently establish deletion
or choose an explicit replacement; invisibility alone is not proof of deletion.

The action requires a literal confirmation, persisted bloodline provenance, a resolved
item, and the expected saved ID. It refuses RUNNING jobs, local running work, any
SENT/ORPHANED/CONFIRMED job for the bloodline, another tab's active lease, and stale IDs.
It sends no game request and removes only that source key from the saved ID map.

Before removing the key, every existing job referencing it receives a `forgottenBindings`
audit entry. Those jobs refuse execution/resume as STALE_BINDINGS before restoring IDs
or sending requests. This includes already-queued jobs. Journal item evidence is preserved.
Explicitly invalidated Bloodright jobs no longer block a fresh job merely because its
manifest hash is identical. The ordinary duplicate-job and unresolved-write guards remain.
If invalidation cannot be persisted, the ID map is left intact. Selection is cleared after
success so the local UI requires a fresh preview.

The pilot README documents the workflow, including changing/removing explicit package
bindings, configuring a new folder when needed, and replacing a deleted `hiddenProbeId`.
Mark failed alone still retains all bindings. No automatic recreation or server deletion
was introduced. Historical jobs remain available for evidence export.

## Verification scope

New regressions cover deletion followed by a fresh create or explicit rebind, cancelled
confirmation, restored runners, invalidated old/queued jobs, identical manifest hashes,
all three unresolved states, active leases, stale IDs, storage failure, current-selection
clearing, UI cancellation/disabled controls, and export of the old ID. The fresh replacement
jobs verify successfully, and resuming the old jobs cannot restore or overwrite their IDs.

The initial probes reproduced the missing recovery method and the existing unreadable
binding failure before the implementation. The exact frozen correction heads and CI
results are recorded in the PR handoff; this document is author evidence, not an independent
verification of the correction.

Author checks (Node 24.19.0, full Git history):

- `npm test`: **563 passed**, zero failures/skips (38 Bloodright tests; four new tests overall).
- Import/boundary gates: zero violations; core action contract includes the new action.
- Repeated builds: SHA-256 `ca0cfaacf84025f899d3ea5808bcff89e46a9155e2f5f4bac73506d047b6496d`.
- Bundle budget: **381,299 raw / 86,120 gzip**, within unchanged proposed 386,000 / 88,000 limits.
- Fixtures regenerated without changes; release-pin check clean; skill ZIP unchanged.
- Pinned Bloodright contract derivation byte-identical; doctrine, projection and pack gates pass.
- `git diff --check`: clean.

## Boundaries

No main integration, release, game request or live staff/browser pilot occurred. Loader
0.5.1 remains unchanged with 0.6.0 pending. PR #30 retains all 12 nodes at 20 Silver and all
17 effects at 99 rounds. Description wording, existing-folder visibility and the proposed
386,000 / 88,000 bundle limits remain separate user decisions. Potency-tag expansion is
outside this correction. Game contract pin remains `1ccdaf078a58101872675e459c8e755b495d4c83`.
