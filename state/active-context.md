# active-context.md - read this first, then the board

**State in one line:** migration ACCEPTED (zero-touch loop proven); law session landed
(lawmap.py, validators law-annotated, Phase 3 plan in 12b); source audit @bdec2883 landed
(extractor upgraded, 45c/45e/45f regenerated, SECTOR_TYPES corruption caught pre-adoption);
law 40 source-verified. ZERO game pushes these sessions. Closed 2026-08-30.

**Verified at close (exact runs, from data/):** validate.py on push/6_verify_and_fix.json ->
0 errors, 0 warnings; --parity vs harvests/inbox/tnr_results_1788053115846.json -> 16/16;
factory.py --selftest -> 20/20; lawmap.py -> 93 laws, 0 errors, 5 known warnings (the open
reclasses: 16d/37/69 unlocated, 18/61 coded-beyond-matrix).

**Start ritual next session:** git pull --rebase. Read state/status.json (board), then
docs/SOURCE_AUDIT_2026-08-30.md, then the Phase 3 + Source-audit sections at the tail of
skills/building-tnr-content/12b_LAWS_coverage.md. Re-run lawmap.py and the validate --parity
line above before trusting anything.

**What exists:** builder v4.27 live (root bundle; ⇩ Repo lists push/). scripts/lawmap.py
(law audit). schema_extract.py upgraded (derived cross-module refs incl. chained/.refine
-> min_items, file-local enums @file-qualified, POST_DOCS). 45c/45e/45f stamped
git:studie-tech/TheNinjaRPG@bdec2883; 45d/45g zero drift. push/6_verify_and_fix.json staged,
ON HOLD until Terr clears the editor crash.

**Open items, by owner:**
- dauntless: PAT Workflows RW (lands .github/workflows/regen_schemas.yml - copy in
  /mnt/user-data/outputs went stale with the container; re-emit from the migration bundle or
  ask for a rewrite, it is 20 lines). Phase 3 rulings in status.json rulings_open. Paste the mounted
  project instructions (delivered 2026-08-30) and delete 00_INDEX/10_LAWS from project
  knowledge - docs/ copies are canon. Relay the wedge source note (SOURCE_AUDIT
  wedge section) to Terr. Art queue: clerk portrait prompt at state/prompt_report_clerk.txt.
  Borrowed Awakening W4 closes ~Sep 5: hide the 5 cosmic jutsu.
- Terr: quest-edit crash fix; file 6 stays held until then.

**Laws that bite immediately:** validate.py and factory.py want cwd=data/ (they read 45c/45d/
45g from the working directory). Extraction owns CONTRACTS; capture-first owns LIVE STATE
(law 83). A push echo is not a read-back. Everything ships hidden:true. Always
git pull --rebase before push - the answers/skillpack workflows commit back.

**Failure modes to watch in yourself:** do not adopt a regenerated file without a structural
diff against the stamped one - the SECTOR_TYPES global/local collision would have shipped
silent corruption. Patch by exact-match with count==1 asserts, always. Userscript patches
need \U0001F4C4-style emoji escapes, not surrogate pairs. Test the RIGHT union member before
declaring a fix failed (SimpleObjective never had sectorType).
