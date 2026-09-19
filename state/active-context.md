<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** FORGE 0.5.0 RELEASED WITH REPO-BACKED IMAGE PACKS. main@4d88ad03ecc8e59f84d0760c8c34db461c5b466f carries the reviewed and approved implementation (dcaa1465) plus the automatic loader pin; a manifest may now bind each @img to an immutable repository blob (path + 40-hex commit + SHA-256), Forge fetches and verifies those bytes when the manifest is opened, and Start is refused unless every bound image is the exact verified file. Canonical Forge CI and release-pin are green on dcaa1465. The push/53 Godstorm repair is NOT yet packable: its eight processed .webp files are not in the repository and cannot be authored from anything that is. No live TNR request or write was made in this session.

**Verified at close (exact runs):**
- main 28bba70d0e14f74a768193881b592b92326f2867 -> fast-forward to dcaa1465eb0eb58001ced42ac4b3f60f2a12d6db -> release-pin auto-commit 4d88ad03ecc8e59f84d0760c8c34db461c5b466f
- canonical Forge CI run 35459192078 on dcaa1465eb0eb58001ced42ac4b3f60f2a12d6db -> completed success (the independently-run CI evidence both review rounds noted was missing for a frozen SHA)
- release-pin run 35459191920 on dcaa1465 -> completed success; loader @version 0.5.0, @require pinned to dcaa1465, @x-release-pending removed
- forge_loader_user.js @require target verified byte-identical to the committed forge_bundle.js via git cat-file | cmp
- forge npm test 416 pass / 0 fail on released main; check_imports 0 violations; check_boundaries 0 violations; check_release_pin ok; bundle 451,847 raw / 88,356 gzip inside 470,000 / 92,000
- doctrinemap.py 0 errors 0 warnings; render_doctrine.py --check all projections current; build_packs.py --check all packs and TOCs current; lawmap.py 0 errors, 5 pre-existing warnings
- validate.py on push/53_godstorm_failed_items_repair.json -> 0 errors, 9 warnings (pre-existing build-order and law-36 advisories)
- the eight Godstorm processed .webp files: 0 filename matches and 0 byte-count matches across the working tree and all 90 remote branches

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** godstorm_53_image_pack: BLOCKED ON FILES. push/53_godstorm_failed_items_repair.json is byte-unchanged and carries no imagePack. Its eight processed .webp files (byte counts already in the manifest's imgSizes) are absent from the working tree, from main, and from all 90 remote branches. chatgpt/godstorm-source-art-pack and chatgpt/godstorm-art-recovery hold only unprocessed originals - 13 lime-key avatar PNGs the manifest's _note explicitly forbids, three Marrow Vault backgrounds and stormcourtyard.jpg - with zero filename and zero byte-count matches. dauntless supplies the eight approved files; then commit them, run make_image_pack.mjs --write, re-run validate.py, and require Forge to show 8/8 verified.; forge_size_pass: Reviewer-requested and not begun: two bundle-budget raises inside one feature is the signal. Plan a Forge size/consolidation pass before the next substantial Forge feature.; forge_next_phase1: READY/FROZEN contract remains on main at state/prompt_forge_next_phase1.md; implementation still has not begun. Unaffected by this session.; branch_cleanup: Approved keep/delete plan remains on main at docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md. Redundant refs still present.; quest_studio_phase_s: Accepted source chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15 retained; not integrated.

**Open items, by owner:**
- dauntless: Update/reinstall the Forge loader and confirm the panel title shows 0.5.0 before trusting any smoke result; refreshing required resources alone does not update the loader.; Supply the eight approved processed Godstorm .webp files so the push/53 image pack can be generated.; After the pack is generated and validated, open push/53 in Forge and confirm all eight repo-backed images read verified before tapping Start.; Run the Godstorm repair. The play tap is the only act that touches the game; no agent performs it.; Optionally delete redundant branch refs per docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md.
- claude: On receipt of the eight .webp files: commit them to a durable art path, run make_image_pack.mjs --write against that commit, re-run validate.py from the skill data/ directory, and report the pack with its per-file digests.; Do not re-derive the eight files from the committed lime-key originals and do not rewrite imgSizes to match a re-processing.; Plan the Forge size pass before the next substantial Forge feature.
- chatgpt: No open item on image packs: correction round 1 returned APPROVED FOR INTEGRATION and both findings are CLOSED.; Optional: review the push/53 image pack once its eight blobs are committed and the pack is generated.
- legacy_content_state: The 2026-09-08 mission/law queue is still unreverified. lawmap.py reports 0 errors and 5 pre-existing classification warnings (laws 16d, 18, 37, 61, 69); these belong to the legacy law-provenance workstream and were deliberately not touched.

**Rulings open:** - Whether the pre-upload re-hash stays permanently, or identity alone suffices once the Forge size pass runs. Reviewer accepted it for now.
- Repository path prefix policy for packs (any safe repo-relative path vs an art/ allowlist) remains intentionally open; digest plus commit bind the bytes either way.
- Whether validate.py should learn the imagePack key by INVOKING the Node contract rather than duplicating it.
- Phase 2+ Forge director choices remain deferred until the brief for the phase that needs them.
- Legacy law-provenance issues, including laws 19/23/37, remain outside this work and must be reverified from their owning evidence.

**Next:** dauntless updates the Forge loader and confirms 0.5.0, then supplies the eight approved processed Godstorm .webp files. Claude then commits them, generates the push/53 imagePack from that commit with make_image_pack.mjs, re-runs validate.py, and hands the manifest back; dauntless confirms 8/8 verified in Forge and runs the repair. Plan the Forge size pass before the next substantial Forge feature. Do not start Forge Next Phase 2 or integrate Quest Studio.

Container quirks and cross-cutting laws live in the mounted instructions.
