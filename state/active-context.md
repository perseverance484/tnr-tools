<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** FORGE 0.5.0 RELEASED AND push/53 IS BOUND. main@a2c528115bbd3f51270b396dbeb7cc72d02e0f39 carries the reviewed implementation, the automatic loader pin, the eight approved processed Godstorm .webp files at art/godstorm/, and push/53's imagePack binding all eight to commit 10fb25704dff1bab8105cd83631e0d524193ef0d by path and SHA-256. Forge CI is green on main and the two pack drift guards genuinely run there. validate.py on push/53: 0 errors. Everything up to the live run is done; the repair itself is dauntless's and has NOT been run. No live TNR request or write was made in this session.

**Verified at close (exact runs):**
- main 28bba70 -> dcaa1465 (reviewed implementation) -> 4d88ad03 (release-pin auto-commit) -> 5aef6d59 (state) -> 10fb2570 (art) -> f52ca18f (pack) -> a2c528115bbd3f51270b396dbeb7cc72d02e0f39 (CI history fix)
- canonical Forge CI: run 35459192078 on dcaa1465 success; run 35461146680 on a2c528115bbd3f51270b396dbeb7cc72d02e0f39 success (418 pass / 0 fail, skipped 0)
- the two pack drift guards RAN in CI rather than skipping: 'push/53 END TO END' 52.7ms and 'COMMITTED pack matches the COMMITTED blobs' 28.7ms in run 35461146680
- release-pin run 35459191920 success; loader @version 0.5.0, @require pinned to dcaa1465, @x-release-pending removed
- jsDelivr serves the pinned bundle: HTTP 200, 451,847 bytes, byte-identical to main's forge_bundle.js, banner reads v0.5.0
- the eight uploaded files verified before commit: names and bytes match push/53's imgSizes, SHA-256 matches the digest list shipped with them, valid RIFF/WEBP, all under the 524,288-byte ceiling
- make_image_pack.mjs re-derived the same eight digests from the committed git blobs; manifest 49 at bad3a2d9 ledgered the same eight files with identical byte counts
- validate.py on the packed push/53: 0 errors, 9 warnings (the same nine it carried before the pack)
- doctrinemap 0 errors 0 warnings; render_doctrine --check current; build_packs --check current; lawmap 0 errors, 5 pre-existing warnings
- shallow-clone behaviour verified against a real git clone --depth 1: guards skip with a diagnostic (41 pass) instead of failing (39 pass / 2 fail before the fix)

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** godstorm_53_run: READY FOR THE OPERATOR. Nothing is blocked. dauntless updates/reinstalls the Forge loader, confirms the panel title reads 0.5.0, opens push/53, confirms all eight repo-backed images read verified, then taps Start. The play tap is the only act that touches the game and no agent performs it.; forge_size_pass: Reviewer-requested and not begun: two bundle-budget raises inside one feature is the signal. Plan a Forge size/consolidation pass before the next substantial Forge feature.; forge_next_phase1: READY/FROZEN contract remains on main at state/prompt_forge_next_phase1.md; implementation still has not begun.; branch_cleanup: Approved keep/delete plan remains on main at docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md. Redundant refs still present.; quest_studio_phase_s: Accepted source chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15 retained; not integrated.

**Open items, by owner:**
- dauntless: Update/reinstall the Forge loader and confirm the panel title shows 0.5.0 before trusting any smoke result; refreshing required resources alone does not update the loader.; Open push/53 in Forge and confirm all eight repo-backed images read verified, then run the repair. The play tap is the only act that touches the game.; Optionally delete redundant branch refs per docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md.
- claude: On the results bundle from the repair: harvest and verify it, and do not treat a push echo as a read-back.; Plan the Forge size pass before the next substantial Forge feature.; If any of the eight art files is ever re-processed, regenerate the pack with make_image_pack.mjs; the two drift guards fail in CI until it is.
- chatgpt: No open item: correction round 1 returned APPROVED FOR INTEGRATION and both findings are CLOSED.; Optional: review the committed push/53 pack and the art commit.
- legacy_content_state: The 2026-09-08 mission/law queue is still unreverified. lawmap.py reports 0 errors and 5 pre-existing classification warnings (laws 16d, 18, 37, 61, 69); these belong to the legacy law-provenance workstream and were deliberately not touched.

**Rulings open:** - Whether the pre-upload re-hash stays permanently, or identity alone suffices once the Forge size pass runs. Reviewer accepted it for now.
- Repository path prefix policy for packs (any safe repo-relative path vs an art/ allowlist) remains intentionally open; digest plus commit bind the bytes either way.
- Whether validate.py should learn the imagePack key by INVOKING the Node contract rather than duplicating it.
- Phase 2+ Forge director choices remain deferred until the brief for the phase that needs them.
- Legacy law-provenance issues, including laws 19/23/37, remain outside this work and must be reverified from their owning evidence.

**Next:** dauntless updates the Forge loader, confirms 0.5.0, opens push/53, confirms 8/8 repo-backed images verified, and runs the repair. Claude then harvests and verifies the results bundle. Plan the Forge size pass before the next substantial Forge feature. Do not start Forge Next Phase 2 or integrate Quest Studio.

Container quirks and cross-cutting laws live in the mounted instructions.
