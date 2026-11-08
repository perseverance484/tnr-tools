<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** Skyglass event LIVE: the Watch Log (First Page, Second Page) and both Skyglass Wrecks run on a weekly Friday 6 PM Central release. Mother of Echoes (the finale) stays HIDDEN until the upstream clip-size revert (EFFECT_ANIMATION_HEX_RATIO 2.5). Its art was uploaded by Duet on branch duet/moe-uploadthing (not merged; see in_progress). Delivery changed 2026-11-06/07: agents write the live game through the director's TNR connector after gates and the director's go (RUL-2026-11-06-132), one runner at a time under the run lock (RUL-2026-11-07-133), routine in docs/workflows/OPERATING_MODEL.md (RUL-2026-11-07-135). What is waiting to run is state/run_queue.json, which is the live job board; this file is the orientation.

**Verified at close (exact runs):**
- doctrinemap -> 21 assertion(s), 18 referenced, 16 surface(s) scanned; 0 error(s), 0 warning(s) (main@05982ffa, 2026-11-08)
- render_doctrine.py --check -> all projections current (exit 0)
- build_packs.py --check -> all packs and TOCs current (exit 0)
- lawmap -> 93 laws, 93 matrix rows, 80 citations across 42 files; 0 errors, 5 warnings (pre-existing)
- forge CI on main -> RED since 595af9f6: forge_bundle.js not rebuilt after a forge/src change. Rebuild on fable/forge-bundle-rebuild (9944a8bc); bundle 482,780 raw is 780 bytes over the 482,000 budget, pending the director.
- validate.py --parity -> RED on bundles whose checks is null (TypeError), carried from 2026-10-13, not fixed.

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** mother_of_echoes: Final tuning (501) and art. Duet uploaded the art to the director's UploadThing and ran follow-ups on duet/moe-uploadthing (14 commits ahead, 86 behind main, unmerged; its push numbers 509/511/512 collide with different jobs on main). Next: reconcile that branch into main, then unhide (502), live test on practice quest 469, go-live (477) after the clip-size revert. run_queue rows 506/502 do not yet reflect Duet's upload.; skyglass_watch_log: Pages 1-2 live; pages 3 (Stolen Stores) and 4 (Her Invitation, needs Mother of Echoes live) created as drafts awaiting the director's go on rewards; rename of page 2 awaits the director's go on names (run_queue 517-520, 526).; skyglass_salvager_thread: 509/511 (main numbering) ready for a browser image run; 510 go-live waits on both and a director playtest.; subaku_palace: Art done and reviewed; parked by the director (503/504/505).; asset_cleanup: Delete unused director-made assets. Inventory started 2026-11-07, paused. gameAsset.delete has no reference check, so the inventory is the safety net.; afterburn_report: Players report enemies taking afterburn from round 1 on the Skyglass Wreck boss floor (battle NgHl3Qk6oHffHNE6CWfzk). Narrowed to a 50% afterburn on the opening wave only; not our content. Needs one read of a live boss-floor battle's effects to name the source.; repo_cleanup: Audit 2026-11-08 (see next): Forge CI, this refresh, RULINGS split, archiving spent manifests/state/docs, legacy builder files, branch pruning, large files.

**Open items, by owner:**
- director: Bundle budget: approve a raise (Forge CI is red until the bundle fits; the rebuilt bundle is 780 bytes over 482,000).; Go on Watch Log pages 3-4 rewards and the page names (517, 519, 526).; Salvager's thread: browser image runs 509/511 (main numbering) and the playtest before 510.; Mother of Echoes: go-live after the clip-size revert; decide how Duet's duet/moe-uploadthing work lands on main.
- duet: Reconcile duet/moe-uploadthing with main (rebase or merge, renumber its 509/511/512 to unused numbers, update run_queue 506/502).; Its Forge changes on that branch (b935b18e, e077a73f, 067b20b2) need independent review before they reach main; CI on b935b18e is red.; Claim the run lock as --holder duet, and commit under its own name, so its runs and commits are distinguishable from Claude's.
- claude: Repo cleanup steps 3-8 (RULINGS split, archive spent manifests/state/docs, legacy builder files, branch pruning, large files, history-rewrite decision).; Asset-cleanup inventory; afterburn report (needs a live boss-floor read).
- chatgpt: Review fable/forge-bundle-rebuild, fable/state-refresh, and Duet's Forge commits.

**Rulings open:** - Whether to rewrite git history to drop large preview GIFs and raw art (main force-push; breaks existing clones). Not proposed yet.
- Legacy law-provenance issues, including laws 19/23/37, remain outside current work and must be reverified from their owning evidence.

**Next:** Read state/run_queue.json for what is waiting to run. Lane A: repo cleanup per the 2026-11-08 audit (Forge CI first). Lane B: Skyglass weekly releases and Watch Log pages as the queue says; Mother of Echoes waits on the clip-size revert.

Container quirks and cross-cutting laws live in the mounted instructions.
