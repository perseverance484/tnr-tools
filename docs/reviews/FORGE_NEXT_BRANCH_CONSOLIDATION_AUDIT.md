# Forge Next branch consolidation audit

**Date:** 2026-09-17  
**Basis:** current `main` `b0bae3bcd6e3d9cf76de48237892ac099fa7a60c` after Forge Next Phase 0 integration.  
**Purpose:** prevent planning/review branch drift without merging stale operational state or prematurely integrating accepted future code.

## Conclusion

Do **not** merge all stray Forge branches.

Several historical branches contain unique accepted planning/design evidence, while others contain stale `state/`, generated evidence, or Quest Studio implementation that is intentionally deferred to Phase S. A wholesale merge would combine incompatible snapshots and could reintroduce work that was deliberately excluded from Phase 0.

The safe cleanup model is:

1. selectively consolidate unique accepted documents onto a fresh `main`-based branch;
2. preserve the accepted Quest Studio implementation branch as a future integration source;
3. delete redundant aliases, temporary branches, superseded planning workspaces, and old review branches only after their unique durable evidence is represented on `main` or another explicitly retained canonical branch;
4. never merge an old review/audit branch merely to preserve its existence.

## Branch classes

### KEEP until selective planning consolidation lands

- `claude/forge-next-planning-reconciled` — accepted reconciled planning package at `ba51a28a99a7748e61de0c2768bd73ab9c65c856`. It owns unique `docs/forge_next/*` planning material not currently on `main`. **Do not merge wholesale**: it diverges from current operational state.
- `chatgpt/forge-next-planning` — retains accepted visual/design-direction material not all represented on `main`. Keep until the unique design sources are selectively copied/reconciled.
- `chatgpt/forge-next-unified-contract` — retains the Phase 0 implementation contract and verification records. Phase 0 code is integrated, but preserve this branch until the durable contract/review artifacts worth keeping are selectively copied.

### KEEP as future implementation source

- `chatgpt/forge-quest-studio-foundation` — accepted Quest Studio implementation at `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`. This is **not** stray historical work. It remains the reviewed source for the later Phase S integration slice.

Do not merge Quest Studio into `main` as part of branch cleanup.

### DELETE after evidence consolidation

These categories are redundant once their unique durable documents are represented elsewhere:

- `claude/forge-next-planning-v3frzi` — superseded by the reconciled planning package;
- `claude/forge-next-planning-workspace` and planning workspace temp branches — intermediate working history;
- completed `fable/forge-next-phase0` — implementation is already integrated to `main`; keep only until no active review/integration process still references the branch name;
- `chatgpt/review-forge-next-phase0*` — review-only branches; preserve final durable findings/clearance on `main` if desired, then delete branch refs;
- `chatgpt/forge-quest-studio-final-fix` — redundant alias if it points to the same accepted Quest Studio tree as `chatgpt/forge-quest-studio-foundation`;
- `chatgpt/forge-quest-studio-source-push-temp`, `...-temp2`, and `...-work` — superseded source-push work branches;
- older Quest Studio audit/review branches once the final accepted review evidence is durably represented.

### NEVER use as merge sources merely for cleanup

- review branches;
- audit branches;
- temporary/workspace branches;
- branches whose only unique difference is stale operational `state/`, captures/results, generated snapshots, or superseded planning text.

Branch deletion removes a ref; it does not erase commits already referenced by durable documents or integrated history. That is preferable to manufacturing merge commits whose only purpose is archival.

## What should be consolidated onto current main

A fresh `main`-based documentation consolidation should selectively preserve:

1. the accepted Forge Next program planning documents needed for future phases, especially the roadmap, architecture recommendation, risk register, user-decision register, and relevant visual/IA sources from `docs/forge_next/*`;
2. the approved Forge visual-direction source that future Phase 2 work depends on;
3. the Phase 0 implementation contract plus final integration clearance, where retaining those records materially improves reconstruction;
4. the final Quest Studio architecture/source-push ruling/review references needed to prepare Phase S — **documents only, not the deferred implementation**;
5. provenance headers naming the exact frozen source branches/SHAs from which historical planning documents were consolidated.

Do not copy stale operational state, old generated result snapshots, duplicate handoffs, or temporary evidence merely because they exist.

## Reconciliation rule for planning documents

The reconciled planning branch is historical design evidence, not current operational state. When copying it to `main`:

- retain the architecture/design intent;
- mark Phase 0 as completed/integrated rather than preserving stale "not yet begun" status prose;
- preserve Phase 1+ decision gates that remain genuinely open;
- retain accepted Quest Studio SHA/source-push facts;
- correct previously identified stale statements rather than silently carrying them forward;
- do not rewrite historical evidence matrices as though they were fresh measurements of current `main`.

## Current cleanup gate

Do not perform the destructive branch-deletion pass until:

- Phase 1 brief is frozen after K-06 and K-17;
- accepted future-phase planning sources needed by that brief are selectively consolidated;
- the accepted Quest Studio implementation branch is explicitly retained;
- a final keep/delete list is verified against live branch SHAs.

The current GitHub connector available to ChatGPT does not expose branch-ref deletion. After this consolidation lands, the director may delete the approved redundant branches in GitHub's Branches UI, or delegate deletion to an environment with explicit ref-deletion capability.
