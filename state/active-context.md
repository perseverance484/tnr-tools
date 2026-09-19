<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** GODSTORM REPAIR RUN AND VERIFIED ON FORGE 0.5.0. main@72de3d3dc26db96d3e792c0191404301f36ebeb2. Results harvests/inbox/tnr_results_1789842714086.json: state DONE, outcome success, 9/9 VERIFIED with verdict match, 0 drift, 0 unverified, 0 failed, 0 skipped; harvest.py verify -> verified (exit 0); all six requested full captures persisted. First production use of a repo-backed image pack, and the binding was checked end to end AFTER the run: each of the eight URLs the live records now serve was fetched and hashed, and all eight digests equal the pack's exactly. push/53 is archived as spent. The live run was dauntless's; this session made no live TNR request or write.

**Verified at close (exact runs):**
- harvest.py verify harvests/inbox/tnr_results_1789842714086.json -> 'builder forge 0.5.0: 9 ok, 0 fail, 0 unverified, 0 skipped -> verified', exit 0
- bundle self-report: state DONE, outcome success, postflight match 9 / diff 0 / unverified 0 / failed 0 / skipped 0; 6 full captures all persistOk true
- the five live profile.getAi read-backs carry exactly the avatar URLs Forge recorded, per AI username
- all EIGHT live asset URLs fetched and hashed: HTTP 200, byte counts equal the ledger, SHA-256 equal the pack's digests, avatars taken from the LIVE read-backs rather than from what Forge sent
- hidden doctrine: the three new assets sent hidden true and 'hidden' is among the 9 asserted keys that read back as match; the quest's live read-back shows hidden true
- push/53 archived; forge npm test 418 pass / 0 fail with the three push/53 guards still resolving and checking the archived manifest
- main 28bba70 -> dcaa1465 -> 4d88ad03 -> 5aef6d59 -> 10fb2570 -> f52ca18f -> a2c52811 -> 72de3d33 (operator results commit) -> 72de3d3dc26db96d3e792c0191404301f36ebeb2
- canonical Forge CI run 35461146680 on a2c52811 success, 418 pass, skipped 0, with both pack drift guards actually running (52.7ms and 28.7ms)

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** forge_size_pass: Reviewer-requested and not begun: two bundle-budget raises inside one feature is the signal. Plan a Forge size/consolidation pass before the next substantial Forge feature.; godstorm_publication: The three new Stormcourt assets and the Stormcourt quest are live but HIDDEN, as doctrine requires. Publishing is a separate step that waits on the content admin's go-ahead and is dauntless's to perform.; forge_next_phase1: READY/FROZEN contract remains on main at state/prompt_forge_next_phase1.md; implementation still has not begun.; branch_cleanup: Approved keep/delete plan remains on main at docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md. Redundant refs still present.; quest_studio_phase_s: Accepted source chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15 retained; not integrated.

**Open items, by owner:**
- dauntless: Godstorm repair is complete and verified; nothing further is owed on it. The three new assets and the quest are live but hidden.; Publishing the Godstorm content is a separate step and waits on the content admin's go-ahead.; Optionally delete redundant branch refs per docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md.
- claude: Plan the Forge size pass before the next substantial Forge feature.; If any of the eight files under art/godstorm/ is ever re-processed, regenerate the pack; the drift guards fail until it is, and for an archived manifest a failure means the art no longer matches what shipped live.
- chatgpt: No open item: image packs approved and integrated, both findings CLOSED, and the first production run is verified.
- legacy_content_state: The 2026-09-08 mission/law queue is still unreverified. lawmap.py reports 0 errors and 5 pre-existing classification warnings (laws 16d, 18, 37, 61, 69), which belong to the legacy law-provenance workstream and were deliberately not touched.

**Rulings open:** - Whether the pre-upload re-hash stays permanently, or identity alone suffices once the Forge size pass runs. Reviewer accepted it for now.
- Repository path prefix policy for packs (any safe repo-relative path vs an art/ allowlist) remains intentionally open; digest plus commit bind the bytes either way.
- Whether validate.py should learn the imagePack key by INVOKING the Node contract rather than duplicating it.
- Phase 2+ Forge director choices remain deferred until the brief for the phase that needs them.
- Legacy law-provenance issues, including laws 19/23/37, remain outside this work and must be reverified from their owning evidence.

**Next:** Godstorm is done and verified; publishing it is a separate step on the content admin's go-ahead. Plan the Forge size pass before the next substantial Forge feature. Do not start Forge Next Phase 2 or integrate Quest Studio.

Container quirks and cross-cutting laws live in the mounted instructions.
