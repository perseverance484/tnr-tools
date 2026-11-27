# TNR current state — DRAFT as of 2026-11-27 (main@f0b5f0f)

Built from repository evidence only (git log on all fetched refs, results bundles' journals,
state/run_queue.json, state/skyglass_schedule.json, docs/rulings/2026-11.md, gh run/PR reads).
**Zero live reads.** Anything marked UNVERIFIED needs one connector read before anyone acts on it.
This replaces the claims in state/active-context.md (generated 2026-11-08), which are wrong in at
least ten places (see lane_b_state.md section 6).

## State in one line
Skyglass is live and weekly (Watch Log pages 1-3 published; the finale Mother of Echoes RELEASED
2026-11-14 by push/597). The Gobblefather Thanksgiving event went LIVE 2026-11-27 (main + genin
versions, ends 2026-12-03). Much of the live work since 2026-11-16 (Stolen Stores, Isonade, Short
Rations, the genin dungeon, Nettle Nova, rc335 caches, the residual-modifier fix) ran from
**unmerged claude/project-thread-* branches**, so main's queue, harvests and answers do not
reflect the live game.

## Time-sensitive today (Fri 2026-11-27)
- **Watch Log Fourth Page "Her Invitation"** (job 520, quest I_cEOGSfFuahaJlR3FnWC): its stated
  precondition (Mother of Echoes live) has been met since 11-14. The schedule still says
  published=false, so tonight's 6 PM CT weekly release would stop (scripts/skyglass_weekly.py
  stops when the page is not published). No commit or bundle on any ref shows 520 ran. UNVERIFIED live.

## Open items, by owner

### Director (decisions only)
1. Page 4 (520): publish for tonight, or skip/reschedule the weekend. (Rewards go was asked 11-08.)
2. Job 620, weapon variant text: it ran 2026-11-17 in the browser, INCOMPLETE (20 match, 1 diff,
   1 unresolved; tnr_results_1794936625194.json). Accept, or finish the last entry.
3. One Perfect Crop: launch-final ran 09-28/29 (push/54, then push/55 repair DONE success); the
   workstream still says BLOCKED. Next is the publish decision (still hidden?, UNVERIFIED).
4. Subaku Palace (503/504-505, parked since 11-07): retire or keep parked.
5. Driftline remainder (562): DL2 shipped in 611; decide the rest or retire the row.
6. Asset cleanup: approve the delete list once the inventory exists (per-record yes).
7. Merge policy for live content branches: which project-thread branches land on main
   (hlg3nc +101, g9d6ix, bxzz52 [forge change, CI red], 6ojemy, 9c4sh9, gcsyem, ua0lgy, kbi6r8,
   bkn9aw, f0jjus, ccr-8d5810e2).
8. Forge CI fix PR #123 (fable/ci-repair-20261114, green, open since 11-14): forge CI on main red
   since 11-13. Approve the merge after review.
9. Large-file history rewrite (preview GIFs, raw art): still undecided (the 11-09 rewrite covered
   only the real name).
10. Gobblefather follow-ups: one test fight per stage "on the director's say-so"
    (state/gobblefather/golive.md read-back checkboxes unticked).

### Claude (builder / runner)
1. Reconcile run_queue.json with what ran (rows 469-test, 510, 538, 545, 548, 549, 550, 593,
   597 should be done/superseded; duplicate ids 596 and 597; about 40 ran jobs have no row).
2. Land or record the branch-run live jobs on main: bundles plus queue rows for 335, 638-698.
   Renumber the colliding push numbers (627, 631, 632, 640, 641).
3. Verify by one live read whether the weekly routines ran on 11-20 (515 Wreck reopen,
   595 Lantern re-issue, 521/522 hides) and record last_run.
4. Job 621 FCF: re-scope (art at v24, waiting on the upstream area-tile PR draft) or close.
5. Afterburn report (Skyglass boss floor): open since 11-08, needs one live boss-floor read.
6. Asset-cleanup inventory (paused since 11-07).
7. answers/ refresh: frozen at 2026-08-30 data; name dedup is blind for Skyglass/MoE/Gobblefather.
8. state/ and push/ archive pass (lane_b_state.md sections 3-4).

### Duet
1. duet/moe-uploadthing (+55, last 11-16): MoE shipped from main. Confirm nothing on it is still
   needed (4 bundles, forge commits b935b18e/e077a73f/067b20b2), then archive the branch.
2. FCF upload (621) only if 621 survives re-scoping.

### ChatGPT (independent review)
1. PR #123 CI repair; PR #128 combat sim harness (claude/project-thread-f2r8sb);
   PR #126 claude/skyglass-update-6b5pk3 (content; check whether it is Lane B).
2. The forge change on claude/project-thread-bxzz52 (livePatch zeroInstantResidual; CI failure
   run 44384747222) before it reaches main.
3. AI player line: open fable/ai-player-ap4 and fable/ai-player-run2-followup handoffs.

## Rulings since the last digest (for orientation)
RUL-2026-11-08-136 (bundle budget 490k/119k), -137..-146 (skills, AI play, real-name rewrite,
staff reads), -147 (live play), -148/-149 (salvage, Teno Yuki names), -150..-167 (AI player line,
battle-art loops), -168/-169 (Gobblefather). ID collisions: -139, -148, -149 each used twice.

## What this draft could not verify
Live state of every item above (no live reads); claude.ai-side scheduled routines (not in repo);
whether the hlg3nc release state matches what is live; One Perfect Crop's current hidden flag.
