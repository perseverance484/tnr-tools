# Docs & authority audit notes (main@f0b5f0f, 2026-11-27, read-only)

## Gates (all read-only modes)
```
doctrinemap.py            -> 21 assertions, 0 errors, 0 warnings (exit 0)
render_doctrine.py --check-> all projections current (exit 0)
build_packs.py --check    -> all packs and TOCs current (exit 0)
lawmap.py .               -> 93 laws/93 rows/82 citations, 0 errors, 5 warnings (16d,18,37,61,69) (exit 0); same 5 'known' warnings recorded in PLAN_2026-08-30
rulings_index.py --check  -> 340 rulings; index current (exit 0)
```

## docs/ root classification
- 2026-11-16 127L docs/00_INDEX.md
- 2026-08-30 87L docs/10_LAWS_core.md
- 2026-11-08 1006L docs/BUILDER_APP_NOTES.md
- 2026-08-30 20L docs/COMPACTION_RUNBOOK.md
- 2026-09-07 349L docs/DEVELOPMENT_WORKFLOW.md
- 2026-11-09 213L docs/DOCTRINE.md
- 2026-11-27 298L docs/DRIFT.md
- 2026-10-24 211L docs/ENGINE_LAWS.md
- 2026-09-08 213L docs/HANDOFF_INVENTORY.md
- 2026-08-30 347L docs/PLAN_2026-08-30_stack_optimization.md
- 2026-09-03 196L docs/PLAN_2026-09-03_builder_app.md
- 2026-11-26 388L docs/RULINGS.md
- 2026-09-11 258L CHATGPT.md
- 2026-10-07 18L README.md
- 2026-09-03 106L EVENT_SHEET.md

Proposed disposition:
- 00_INDEX.md: KEEP, fix (wrong paths scripts/lawmap.py, scripts/session_open.py; PAT step; missing routes).
- DOCTRINE.md, ENGINE_LAWS.md, RULINGS.md, DEVELOPMENT_WORKFLOW.md: KEEP (DEVELOPMENT_WORKFLOW §13 stale vs RUL-132).
- 10_LAWS_core.md: MERGE into ENGINE_LAWS (cluster index citing law numbers only) or DOCTRINE; it restates laws 9-13, 28, 57-59, 61, 75-76 verbatim-ish, frozen 2026-08-30.
- DRIFT.md: KEEP path (written by .github/workflows/regen_schemas.yml) but route from 00_INDEX; 63 distinct days of drift commits, contracts last re-pinned 2026-10-29.
- HANDOFF_INVENTORY.md: ARCHIVE (self-labelled "DRAFT, uncommitted", 2026-09-08 ChatGPT takeover brief; only self-referenced).
- COMPACTION_RUNBOOK.md: KEEP until GIF/history-rewrite decision; then merge with HISTORY_REWRITE_2026-11-09 lessons into one history-surgery runbook (referenced by .github/scripts/build_answers.py and answers/INDEX.md).
- BUILDER_APP_NOTES.md: KEEP (cited by forge/src/runner/validate.mjs, takeover.mjs, state prompts); refresh header (cites dead branch claude/builder-app-production-readiness-kelsib, unmerged 4757 behind).
- PLAN_2026-08-30_stack_optimization.md: ARCHIVE (only referenced by HANDOFF_INVENTORY).
- PLAN_2026-09-03_builder_app.md: ARCHIVE with redirect stub or keep; referenced by forge_next + BUILDER_APP_NOTES + state/prompt_builder_app_build.md.
- README.md: REWRITE as start-here map ("Generated 2026-08-28", says "both Claude skills").
- CHATGPT.md: KEEP, fix §9 live-game boundary.
- EVENT_SHEET.md/.docx: KEEP (staff canvas, referenced by skills; docx built by build_event_sheet_docx.js).

## Rulings ledger anomalies
- 340 indexed; status counts: ACTIVE 330, SUPERSEDED 7, SHELVED 1 (RUL-2026-10-21-006), SUSPENDED 1 (RUL-2026-10-24-001), "?" 1 (RUL-2026-11-26-169, no Status line). Declared enum is ACTIVE/SUPERSEDED/DEFERRED.
- 56 index rows read "(superseded by ...)" yet Status ACTIVE: partial supersession (e.g. 168 superseded only items 21/24/25 by 169) is indistinguishable from full.
- Index lists RUL-2026-11-14-159 "superseded by 161, 162" though both say "Supersedes: none (it changes ... point 5/7)".
- Duplicate IDs in docs/rulings/2026-10.md: RUL-2026-10-25-002 (lines 2549, 2563), RUL-2026-10-26-001 (2806, 2842), RUL-2026-10-26-002 (2822, 2862). --check passes anyway.
- 2026-11.md format drift: 82 entries, 57 with Domain, 25 use "Decided by" instead; 81 Status.
- Pending law reconciliation: RUL-2026-10-26-008 (law 18 extends to AI-held items) -> ENGINE_LAWS law 18 still jutsu-only (ENGINE_LAWS last changed 2026-10-24). CLAUDE.md §6 and the never-list rely on law 18.
- RUL-2026-09-08-004 reconciliation sequence (laws 19/23/37...) still carried as rulings_open in state/status.json.

## Reviews/handoffs reference scan
Method: for each entry in docs/reviews and docs/handoffs, count files in state skills docs/00_INDEX.md docs/workflows docs/design docs/rulings scripts .github push/README.md forge player that mention its basename.
- handoffs: 101 entries, 61 unreferenced
- reviews: 85 entries, 54 unreferenced
- 33 AI_PLAYER_* files (580K) in docs/reviews are Fable Lane A *handoffs* (misfiled), each citing a ChatGPT review on an unmerged chatgpt/review-* branch ("evidence; not merged"); 73 of 76 chatgpt/review-* branches unmerged.
- handoffs categories: 24 ART_REQUEST, 34 *_PROMPT, 3 *_PROMPTS, 16 *_HANDOFF, 24 other (incl. .py/.json helpers, skill_overhaul/).
- Keep-forever: HISTORY_REWRITE_2026-11-09.md + _commit_map.txt (resolves every pre-rewrite SHA cited in docs).
Full table (refs, last-commit, size, path): docs_refs.tsv in this folder.

## Installed-vs-repo skill drift
- repo skills/: 3; installed synced TNR skills: 9 (shipping-tnr-content, simulating-tnr-combat, tnr-pvp-combat, tnr-replay-analysis, designing-tnr-pve-encounters, tnr-jutsu-engine exist only installed).
- diff -rq repo vs installed: building 38 diffs, designing 4, art 3. Installed building SKILL.md doctrine stamp @17d6a71 vs repo @b614200; installed adds a docs/combat-engine/tags routing paragraph not in repo; repo has EVENT_SHEET.md routing not installed.
