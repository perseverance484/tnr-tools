<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** FORGE NEXT PHASE 0 COMPLETE. main@77f02c30f7714eb8506ace8802904cb351a70d34 contains the integrated Phase 0 implementation, the READY/FROZEN Phase 1 contract and handoff, the selectively consolidated Forge Next planning/design record, and durable rulings for capture tiers, the research-read registry, and branch cleanup. Quest Studio remains an accepted future Phase-S source at 5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15 and is not integrated. No live TNR request or write was made in this session.

**Verified at close (exact runs):**
- main -> 77f02c30f7714eb8506ace8802904cb351a70d34 before closeout-state projection
- scrub run 35251493212 on main@77f02c30f7714eb8506ace8802904cb351a70d34 -> completed success
- Phase 0 canonical Forge CI run 35240352496 / job 105266889290 on 3130f9433810cca4f8eca78b80aeb4dc8eb7ddb0 -> completed success
- studie-tech/TheNinjaRPG main -> 1fd355ab92cec78148130e02c8d38834836c3181
- session_close projection contract reproduced locally; full lawmap/doctrine/packs/parity guard rerun was not possible because the ChatGPT container could not resolve github.com for a repository clone

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** forge_next_phase1: READY/FROZEN contract is on main at state/prompt_forge_next_phase1.md; implementation has not begun. Fable should create fable/forge-next-phase1 from fresh main, stay inside Phase 1, make zero live requests/writes, freeze an exact SHA, and return it for independent ChatGPT review.; branch_cleanup: Approved keep/delete plan is on main at docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md. Redundant refs remain until deleted through GitHub UI or an environment with explicit branch-ref deletion.; quest_studio_phase_s: Accepted implementation source chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15 is retained for later deliberate reconciliation/integration; do not merge it as cleanup.

**Open items, by owner:**
- dauntless: Optionally delete redundant Forge/Quest Studio branch refs exactly per docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md after confirming no active session is using them.; Hand the Phase 1 main-based implementation brief to Fable / Claude Code if its implementation session has not already started.
- claude: Create fable/forge-next-phase1 from fresh main and implement only state/prompt_forge_next_phase1.md.; Make zero live TNR requests/writes; reverify source facts and upstream head at implementation start; return an exact frozen SHA with tests/gates/bundle evidence.
- chatgpt: Independently review the frozen Phase 1 implementation SHA on a separate chatgpt/review-* branch without modifying Fable's branch.
- legacy_content_state: The prior 2026-09-08 mission/law queue was not reverified during this Forge session. The prior digest is archived before this closeout replacement; reopen the owning workstream/captures before acting on old live-action claims.

**Rulings open:** - Forge Next Phase 1 has no remaining director ruling blocker.
- Phase 2+ director choices remain deferred until the brief for the phase that actually needs them.
- Legacy law-provenance issues, including laws 19/23/37, remain outside this Forge closeout and must be reverified from their owning evidence/workstream before action.

**Next:** Start Forge Next Phase 1 from fresh main using state/prompt_forge_next_phase1.md; Fable implements, then ChatGPT independently reviews the frozen SHA. In parallel, dauntless may remove redundant branch refs per docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md. Do not start Phase 2 or integrate Quest Studio until the appropriate reviewed gate/director instruction.

Container quirks and cross-cutting laws live in the mounted instructions.
