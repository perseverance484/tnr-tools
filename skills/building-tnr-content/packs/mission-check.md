<!-- RENDERED pack 'mission-check' from inspection.md@8838cef via build_packs.py - edit the sources, never this file -->
# Pack: mission-check

Read-only inspection packet. Load this for checking existing missions; build profiles and global handoffs are not required.

<!-- pack-trace: inspection.md @8838cef 'Mission check' -->
## Mission check

Use for "check the A rank missions" and equivalent inspection requests. Default
scope is a structural check of the latest eligible committed records. State that
scope and proceed. Building, balance review, player-facing prose and live refresh
are separate tasks that load their own sources when requested.

Run `python3 scripts/tnr.py missions check --rank A` (substitute the requested rank).
Use repeated `--id` options to restrict the population; IDs come from evidence,
never transcription or invention. `--json` includes per-record provenance,
coverage, excluded capture classes and unresolved records. No command here makes
a network request or modifies the repository. A query with stale generated inputs
rebuilds its view in memory, so it never waits for GitHub Actions.

Report the inspected population, capture times, findings and limitations. Each
record is an observation at its own timestamp. Rank filtering is not evidence of
a complete rank census. Unresolved records of unknown rank remain a coverage gap.
A missing record is unknown, not deleted. Published/visible records can legitimately
have `hidden: false`; the hidden-on-create rule applies to new delivery, not to an
inspection of existing records. No construction-profile comparison is implicit.

The check covers objective identities, duplicate IDs and explicit nextObjectiveId
targets. It does not certify balance, complete engine flow, current live state,
or complete population. Inspect the relevant raw record and quest reference when
explaining a finding. Do not infer mechanics from a record or design intent from a
capture. `docs/00_INDEX.md` owns precedence; `docs/DOCTRINE.md` owns shared rules.
User decisions, live-game operations and final acceptance remain the user's.

Without a checkout: resolve the requested GitHub ref to a commit once, then fetch
`answers/missions_A.md` at that exact commit. Use `answers/missions_A.json` for
deeper provenance when needed; it includes source hashes, timestamps and coverage.
Read specific raw evidence
at the same commit only when needed. These generated views are snapshots; do not
claim they were freshly executed or are current live game state. If the view is
missing or its integrity cannot be established, report that limitation and use a
checkout to derive it. Do not fall back to remembered mission facts.
