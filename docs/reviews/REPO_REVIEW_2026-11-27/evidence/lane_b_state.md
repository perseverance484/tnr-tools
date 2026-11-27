# Lane B content, state & orientation — audit notes (main@f0b5f0f, 2026-11-27, read-only)

## 1. run_queue.json row-by-row (21 non-done rows)

Evidence source: results bundles' `journal.manifestPath/state/outcome` in harvests/inbox (main) and on branches; push/609 + push/611 `_note`/items; git log.

| id | queue status | actual (evidence) | action |
|---|---|---|---|
| 469-test | ready | MoE released 2026-11-14 by 597 (tnr_results_1794615376220.json DONE success 16/16). Practice test overtaken. | mark done/superseded |
| 477 | superseded | correct (by 597) | archive row |
| 503 / 504-505 | parked | director "Drop subaku palace art for now" | keep parked; director decision to retire |
| asset-cleanup | waiting | no commits since 11-07 inventory | keep, owner claude, needs director go list |
| 511 | retired | correct | archive row |
| 510 | waiting | Fire published + both Wreck Sighted copies unhidden + original hidden by push/611 (2026-11-14, bundle tnr_results_1794614869418 DONE failed 45/47; repaired by 612 DONE success) | mark superseded by 611 (verify Wreck Sighted rewrite part) |
| 515 | waiting (recurring) | no Friday-run commit or bundle for 2026-11-20 on any ref; Stolen Stores 6 PM release ran on branch hlg3nc (673). Weekly Wreck reopen unverified. | convert to a recurring routine row with last_run; needs a live read |
| 520 | waiting | precondition met (MoE live since 11-14). Schedule says page 4 published=false; releases tonight Fri 2026-11-27 6 PM CT (00:00Z 11-28) only if published. No commit/bundle anywhere shows it ran. | DIRECTOR DECISION today |
| 538 | waiting, manifest "(not written)" | charts unhidden + chart texts in push/609 (11-13, DONE failed 101/106, repaired 612) | mark done-by-609 |
| 548 | ready | "the Fire v6 (hidden)" text in 609; Fire published in 611 | mark superseded by 609/611 |
| 549 | ready | ran 2026-11-09 (tnr_results_1794259600259 DONE success) | mark done |
| 550 | waiting | ran 2026-11-09: commit 4914fcb0 "549/550 done ... live, verified" + tnr_results_1794259841147; the commit's run_queue diff only changed the trailing newline -> status edit LOST | mark done (lost-update bug) |
| 543 | superseded | correct (folded into 545) | archive row |
| 562 | parked | DL2 (Split Hold/Broken Stern charts+runs live) shipped in 611; Driftline remainder undecided | split: done part / parked part, director |
| 545 | waiting | executed inside push/611 ("545 salvage ladder") 2026-11-14 | mark done-by-611 |
| 593 | waiting | ran 2026-11-13 (tnr_results_1794601792898, _1794604795704 DONE success 76/76) | mark done |
| 597 (row 1) | waiting | ran 2026-11-14 00:16Z DONE success 16/16 | mark done; DUPLICATE id with row "597 grant quest" (done) |
| 596 | done x2 | two different jobs share id 596 | renumber one (596b) |
| 595 | waiting | depends on 545 live (it is) + Fridays; no evidence of 11-20 re-issue | recurring routine row; live read needed |
| 620 | waiting (director approval) | RAN 2026-11-17 in browser: tnr_results_1794936625194 INCOMPLETE 20 match / 1 diff / 1 unresolved | mark incomplete; finish 1 entry |
| 621 | waiting (Duet upload) | FCF went through v5..v24 art iterations, upstream PR draft; job never queued as manifest | re-scope: blocked on upstream PR |

Missing rows: 533-535, 539, 546-547, 551-559, 563-574, 582, 584-587, 594, 599-619 ran or were drafted on main without queue rows; 631/632 present.

## 2. Live jobs run from unmerged branches (not on main)
Run-lock claims on main since 11-14 cite job numbers with NO manifest on main:
335(rc335) 638 640 641 645 649 651-658 660 664-676 683 684 690 697 698.
Results bundles that exist only on branches (git diff --diff-filter=A main...origin/<b> -- harvests/inbox):
- claude/project-thread-hlg3nc: 40 bundles, +101 commits; Stolen Stores (Watch Log page 3 content) LIVE 2026-11-20/21 (673 go-live), Isonade boss v4..v11, Short Rations; its run_queue has 34 600-range rows main lacks; 650 still waiting.
- claude/project-thread-g9d6ix: 5 bundles; genin dungeon 660-664 hidden live build (660, 664 INCOMPLETE).
- claude/project-thread-bxzz52: 2 bundles; 640/641 residual-modifier fix LIVE (forge change too: CI failure 44384747222).
- claude/project-thread-6ojemy: 1 bundle; 690/691 shore crew hidden.
- claude/project-thread-9c4sh9: 684 Isonade style C wired (17 jutsu, 266 assets unhidden).
- claude/project-thread-gcsyem: 698 Nettle Nova live build, "queue row done" (on its branch only).
- claude/project-thread-ua0lgy: rc335 resource caches DONE.
- claude/project-thread-kbi6r8 (4), claude/project-thread-bkn9aw (1, 631 UT), ccr-8d5810e2-036hwx (1, "627" Skyglass charts 14/14), duet/moe-uploadthing (4), claude/ap-live-run-dauntless-goqgbz (1).
Push-number collisions: 627 (main White Tiger vs ccr-8d5810e2 Skyglass charts), 631 (main Gobblefather vs hlg3nc flooded_stores_stage1 vs f0jjus weapon_effect_targets), 632 (main Gobblefather genin vs hlg3nc stage2), 640/641 (bxzz52 residual fix vs hlg3nc), 509/511/512 (duet, known since 11-08).

## 3. state/ classification (full per-entry list: state_entries.tsv: last-touch, size, ref count)
ACTIVE / board (keep in state/): active-context.md, digest.json, status.json, run_queue.json, run_lock.json (move off main: see finding), skyglass_schedule.json, schema_sentinel.json, validate_exceptions/, player/ (pilot; heavy churn), gobblefather/, variant_text/ (620), fcf_upload/ (621), prompt_playing_tnr.md, prompt_ai_player_overhaul.md, mounted_instructions.txt (projection), staged_workflows/ (referenced by tests per REPO_SIMPLIFICATION_AUDIT debt #3), workstreams/, results/.
SPENT event state -> archive/state/<event>/ (each needs a ref-rewrite pass):
- ghost_ship_* (37 files, Oct 1-12): Skyglass shipped. BUT read by harness/ghost_ship_{consume,final,stage2,legacy_baseline,release_dryrun} tools/fixtures and push/344,358,361-366,89. Move together with harness/ghost_ship_* (or leave; do not move alone).
- one_perfect_crop_* (9 md) + plan_one_perfect_crop_finish.md + prompt_one_perfect_crop.md: workstream BLOCKED since 09-27 but push/54 ran 09-28 (DONE failed 3/5) and push/55 repair ran 09-29 DONE success; roadmap never updated. Close workstream first, then archive.
- headless_rider/ + 2 headless_rider_*_validate_exception.json (Oct 25-26, Halloween).
- tenth_name_* (6), prose_pass_* (2), fix_copies_converging.md, mission_hide_review.md, wave_workflow.md, bg_wiring_*, wiring_*.json, push16_misroute.json, thread_init_*.txt, prompt_report_clerk.txt, prompt_three_rounds_survivor.txt (Aug 30-31, 0-1 refs).
- moe_upload/ (3.1MB), moe_scale/, moe_etch_colours/, moe_* : MoE released 11-14 -> archive/state/mother_of_echoes/.
- rengoku/, rengoku_upload/, white_tiger/, whitetiger_upload/, recut_upload/, prompt_rengoku_624_626.md, prompt_white_tiger_627_629.md, prompt_strip_recut_630.md: jobs 624-630 done 11-18.
- skyglass_thread_boards_v2/v3.json, skyglass_thread_uploaded.json, salvager_trade/, driftline/ (partly), prompt_skyglass_handtest_20261113.md, prompt_skyglass_e2e_run.md: Nov 13 release done.
- schema_adoption_ledger_{85cecae,2af4b320,3314d122}.json: historical adoption evidence -> docs/reviews/schema_adoption/ (referenced by 1-2 docs each).
- prompt_* for completed Lane A briefs (builder_app_build, client_contract_audit, forge_full_capture, forge_protected_auth, forge_disappearing_overlay, forge_next_phase1, guide_studio, forge_bloodright_import, forge_dungeon_recipe, forge_suggest_create, validate_stale_rules, jutsu_icon_p1_tooling, qa_ticket_pipeline, art_generation_preflight_hydration, content_workstream_orchestration, tnr_art_reference_pack, bloodright_collection_icons, skill_overhaul, skill_research_program, early_game_sim) -> archive/briefs/ ONLY after checking each brief's task is closed (docs/handoffs / merged); CLAUDE.md says the brief is the build contract while active.
UNSURE (owner to say): skyglass_build/ (1.9MB, 20 refs), skyglass_design/ (1.3MB, 21 refs), skyglass_art/, crownhold/, skyglass_hunts/, skyglass_fx/, held/, ai_pool_battle_lines/, jutsu_icon_revert/, bloodright_reference_library/, art_backlog.md, art_produced.md, omen_text_live_kits.json — Skyglass is still running weekly; keep until the event closes.

## 4. push/ (464 files: 328 json, 131 py)
push/README.md: "Keep only manifests that are currently intended for operator use... Builder pickers list .json and .zip files from push/". Classification (push_spent.tsv): 214 RAN-ok (a DONE success bundle names it), 33 RAN-incomplete (most later repaired), 74 no bundle match (captures run pre-journal, generators' outputs, drafts), 8 queue-active (of which 549/593/597/620 actually ran).
Archive map: push/<N>_*.json with RAN-ok and N<600 -> archive/spent-manifests/push-2026-11/ (exclude files referenced by forge/test, harness, scripts: 00_forge_readonly_smoke, 02_one_perfect_crop_asset_probe, 03_tnr_art_style_reference_capture, 47_one_perfect_crop_core_manifest, 74_*, 90_ghost_ship_skyglass_release, 101_*). Keep *.gen.py generators for live recurring jobs (skyglass_wreck_window, skyglass_journal, salvager_*, mother_of_echoes (for reference), larry_bind) in push/ or move generators to push/gen/.

## 5. harvests/
inbox 548 bundles, 143MB: 2026-08 30 (18MB), 09 25 (4MB), 10 355 (109MB), 11 138 (18MB). 44 named in run_queue. No processed/pending marker exists; harvest.py has no ledger. Paths are referenced by forge/src (budget/reader, facts, runner), forge/test, harness fixtures, 62 push files, 45 state files -> do NOT move. Size reduction requires history rewrite (COMPACTION_RUNBOOK, director-only).
answers/ derived from getAllNames captures only (.github/scripts/build_answers.py CAPTURE_ENTITY); last regenerated 2026-10-23; hot.json newest source 2026-08-30. Connector-era runs produce no getAllNames captures, so names_quest/ai/item contain 0 Skyglass/MoE/Gobblefather rows; validate.py name-collision lint (_answers_names) runs blind for 3 months.

## 6. active-context.md / digest.json (generated 2026-11-08) — what is now wrong
1. "Mother of Echoes stays HIDDEN until the upstream clip-size revert" — WRONG: released 2026-11-14 (597 DONE success); clip size solved by per-effect animationScale (upstream 8bd670153, 593 ran).
2. "duet/moe-uploadthing ... reconcile into main" — moot: MoE shipped from main; branch now +55/-2421, last commit bot 11-16.
3. Forge CI "RED ... pending the director" on budget — budget raised to 490k/119k by RUL-2026-11-08-136; but forge CI on main is STILL red (last main forge runs 11-13/11-14 all failure; fix PR #123 fable/ci-repair-20261114 green, open since 11-14).
4. "Watch Log pages 3-4 drafts awaiting go" — page 3 published (518) and Stolen Stores page content released 11-20 (on branch hlg3nc); page 4 still unpublished, decision due today.
5. "Salvager's thread: browser image runs 509/511" — done (509 done, 511 retired), Fire published 11-14 (611).
6. Rulings open "Whether to rewrite git history ... Not proposed yet" — a rewrite happened 2026-11-09 (RUL-2026-11-09-144) for the real name; large-file rewrite still undecided.
7. Open by owner: duet items moot; chatgpt "review fable/forge-bundle-rebuild, fable/state-refresh" — state-refresh landed on main via 2146828e2 (branch spent); bundle-rebuild superseded by later forge releases (0.12.6/0.12.7).
8. Missing entirely: AI player line (merged 11-16, RUL-147..167), Gobblefather event (live 11-27), Rengoku/White Tiger animations (live 11-18), FCF art + upstream PR drafts, PvP planners PRs #125-#132, combat sim harness PR #128, Stolen Stores/Isonade/Short Rations/genin dungeon/Nettle Nova/rc335 branch work, variant text 620, Teno Yuki names.
9. "Verified at close" guard lines are 19 days old and report main@05982ffa.
10. Mechanism: digest is hand-written and rendered by session_close.py; session_open.py mutates digest.json (token_ledger) on every open. It has gone stale twice (10-17 -> 11-08, 11-08 -> now), each time discovered after ~3 weeks.

## 7. Rulings id collisions (docs/rulings/2026-11.md)
RUL-2026-11-08-139 and RUL-2026-11-09-139; RUL-2026-11-11-148 and RUL-2026-11-13-148; RUL-2026-11-11-149 and RUL-2026-11-13-149. (165 absent.) The sequence number is not unique across days.

## 8. Commit noise into state/ on main
Since 2026-11-08: 2309 commits on main, 1316 "run-lock:" (state/run_lock.json), 348 "player"/fight-log, 81 dauntless. Each run-lock commit triggers scrub + large-files + no-real-name workflows (gh run list -b main: 15 of last 15 runs are run-lock commits).
