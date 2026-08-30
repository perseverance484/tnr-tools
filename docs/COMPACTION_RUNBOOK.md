# COMPACTION RUNBOOK - inbox history squashing (manual-only, ruling 5)

answers/ is a pure function of seed + inbox, so superseded inbox bundles carry
nothing derivable once folded into the seed. When .git growth actually bites
(clone time, not aesthetics), compact:

1. BETWEEN sessions only - no live container clone, no mid-work phone state.
2. Pick keep-N (default: newest 5 bundles stay verbatim).
3. Fold older bundles' rows into the seed catalogs (harvest.py stamp the
   result; the seed is the durable audit floor - nothing derivable is lost).
4. Safety tag first: `git tag pre-compact-YYYYMMDD && git push --tags`.
5. Interactive rebase squashing the superseded `results:`/`answers:` commits;
   `git push --force-with-lease` (never bare --force).
6. Every clone thereafter must re-clone (history diverged) - the session
   ritual's fresh clone absorbs this automatically.
7. Re-run build_answers + guards; verify answers byte-identical to
   pre-compaction output (pure-function check).

NEVER automated, never mid-session, never without the tag. Approved shape per
ruling 5 (2026-08-30); execution deferred until size actually bites.
