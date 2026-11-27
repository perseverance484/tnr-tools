# Lane A code & CI audit notes (main@f0b5f0f89, 2026-11-27)

## Gates run locally (read-only; player/dauntless suites run in a scratch copy at scratchpad/run)
| command | result |
|---|---|
| node forge/tools/check_imports.mjs | 0 violations (exit 0) |
| node forge/tools/check_boundaries.mjs | 0 violations, contract pin 3314d122 (exit 0) |
| node forge/tools/check_bundle_budget.mjs | raw 487360/490000 (99.5%), gzip 117767/119000 (99.0%) (exit 0) |
| check_release_pin (forge.yml inline) | release pin clean (exit 0) |
| npm test / npm run build (forge) | NOT RUN: no node_modules; npm ci would write into repo + network |
| python3 -m unittest discover -s player/tests (scratch copy) | Ran 675, OK (skipped=36; skips = scratch copy has no git history for pinned review SHAs) |
| pytest state/player/dauntless/tools/tests (scratch copy) | 46 passed |
| combat_map.py --check (scratch) | planner vs map @29cd91b5: agree |
| scripts/test_*.py (9 files, in repo, PYTHONDONTWRITEBYTECODE) | all OK: 6+43+10+40+6+4+10+51+13 = 183 tests |
| doctrinemap.py | 0 errors 0 warnings |
| render_doctrine.py --check | current |
| build_packs.py --check | current |
| catalog_sync.py --selftest | OK |
| design.py --selftest | 94 passed |
| rulings_index.py --check | 340 rulings, current |
| check_large_files.py | 17 over limit, 0 not allowed |
| check_no_real_name.py --selftest | 18 passed |
| lawmap.py --check | 0 errors, 5 warnings (16d/37/69 no citation; 18/61 reclass candidates) |
| selfcheck.py (default) | 1 error: 45d not found in repo root (needs --generated data) |
| selfcheck.py --generated data | 0 errors |
| validate.py --parity <newest inbox bundle> | TypeError: 'NoneType' object is not iterable (validate.py:215) |
Note: one `git merge-tree --write-tree` probe was run (writes loose tree objects only, no refs/worktree change).

## GitHub Actions (read-only via MCP)
- forge.yml on main: last success 2026-11-09 23:57 (run 42724600295, pre history rewrite). Every main run since (42739036770 .. 43544114757) failed in `npm test`, so the bundle-reproducibility, fixtures and budget steps have not executed on main since 11-09.
- Failure cause (run 44384747222 log): tests pin pre-rewrite SHAs: art blobs "at 10fb25704dff could not be read" (presentation.golden/adversarial), "imagePack ref a84807a is not on any pushed branch" (runner.test.mjs:363 staged-manifest compatibility over push/122_bloodright_collection_a.json).
- Fix exists: PR #123 fable/ci-repair-20261114 (d551bf131) forge CI success (runs 43556319045/43556294948), OPEN since 2026-11-14, now conflicts with main in .github/large-files-allowlist.txt and push/608_moe_etching_rehost.json.
- Last 60 runs on main: scrub/large-files/no-real-name only, all success, each triggered by run-lock commits.
- regen-schemas-sentinel: daily success, commits drift each day upstream moves.
- skillpack: last run 2026-11-19, success.
- relay.yml: total_count 0 runs ever.
- Node 20 deprecation warning on actions/checkout@v4, setup-node@v4.

## Commits on main by kind (since 2026-11-20)
runlock per day: 8, 67, 48, 59, 64, 52, 61, 53 vs other: 11, 38, 58, 20, 14, 18, 24, 21.
`player: jutsu engine` 126 commits since 11-20, all touching only state/player/dauntless/jutsu_training.md.
github-actions on main since 11-01: 22 sentinel, 13 skillpack, 8 loader pin.

## Bot commits on non-main branches (commit_generated.py pushes to whatever branch triggered)
22 duet/moe-uploadthing; 6 each claude/quest-studio-source-push-review, claude/quest-studio-final-review, chatgpt/premium-seichi-item-icon-overhaul-v10, chatgpt/forge-quest-studio-source-push-work, -temp2, -temp, chatgpt/forge-quest-studio-foundation, chatgpt/forge-quest-studio-final-fix; 5 fable/art-skill-duelyst; 3 fable/duelyst-kit; 3 claude/project-thread-hlg3nc; 2 claude/project-thread-un0ofw; 1 fable/skill-overhaul-p2; 1 fable/pixel-art-snap.

## Unmerged branch with live-run Forge code
origin/claude/project-thread-bxzz52: bf06a284f (forge/src/runner/livepatch.mjs +42, runner.mjs, test) + 75e7681d3 harvest bundles tnr_results_1795031980477/1795032609352 (builder "forge-mcp", at 2026-11-18T19:59Z). forge_bundle.js on branch has 0 occurrences of zeroInstantResidual (bundle not rebuilt). forge CI run 44384747222 failure. No run_queue row / ruling for 640/641 on main.

## Tests not in any CI workflow
player/tests (675), state/player/dauntless/tools/tests (46 pytest), scripts/test_*.py (183), guide-studio `npm run gate`, harness/* selftests, validate.py selftests.

## Root contract copies
32b/45c/45g at root byte-identical to skills/building-tnr-content/data (cmp). forge/src/runner/pool.mjs imports root 32b at build; builder_bundle.js fetches all three from raw main at load.

## Legacy / one-off code candidates
- harness/ghost_ship_{consume,final,legacy_baseline,release_dryrun,stage2}: 97 files, last touched 2026-10-11/12, event-specific, README says historical harnesses "still reproduce"; no references outside harness except content_workstream.py + inbox bundles.
- guide-studio/: 160 files, 3.4M, last commit 2026-09-13, "independent-review candidate, not a deployed service", corrections "await narrow independent re-review"; not routed by 00_INDEX, no CI.
- relay.yml: never run, no relay/* branches ever merged.
- scripts/ai_pool_reequip_readback.py (push/162-177 only, 0 refs), scripts/bloodright_classification_readback.py (push/109-110), scripts/bloodright_collection_package.py: job-specific.
- ops/ap_model_session/run2/LOSS_ANALYSIS.md: single doc in an otherwise empty ops/ tree.
- state/player/dauntless/tools: 41 py files, 11,382 lines of executable code (pilot.py 1043, planner2.py 1678, turn.py 1479) living under state/. player/ (3,710 lines + brain/activities) is "ported from the pilot"; pilot.py, restock.py, harvest.py still exist alongside player/activities/restock.py, harvest.py. pilot.py last edited 2026-11-22.
- builder_bundle.js v4.32 last changed 2026-09-03; J_MIGRATION_AND_RETIREMENT.md stage 5 (G-10 ruling) not taken; pin_release.py still pins both loaders.
