<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** PRESENTATION STUDIO RE-REVIEW: P1 CHANGES REQUESTED (R1-R3); original witnesses addressed, F3 and F4/F5 partially open. P0 unchanged and passes. Verified main/base/merge-base eefefd1afd67111a90c332951a8dd9f83cb99cbd; frozen Fable head ac792ef1085c8350fda7bf79050d90ca0ce41879. Report docs/reviews/REVIEW_2026-09-20_forge_presentation_studio_p1_correction.md on chatgpt/review-forge-presentation-studio-p1-r2, based on that exact head. No implementation integration; live-game requests/writes ZERO. Design proposal remains at 4532ef917a1dfb40d00c554fd7f065e13216afc7, awaiting director acceptance.

**Verified at close (exact runs):**
- Refs: main/base/merge-base eefefd1afd67111a90c332951a8dd9f83cb99cbd; implementation remote/local ac792ef1085c8350fda7bf79050d90ca0ce41879; exactly P0 05e7156, P1 8830443, correction ac792ef.
- Correction diff: 17 presentation/package/test files. P0 runtime/build/tooling, lockfile, loader, bundle unchanged from 8830443.
- Forge npm test: 511 passed, 0 failed, 0 skipped. Runtime npm audit: 0 vulnerabilities. Node 24.19.0 / npm 11.9.0; offline lockfile install.
- Build and envelope/screens fixtures regenerated without drift. Import gate 40 modules/71 cross-layer imports and boundary gate 40 source/13 presentation modules: 0 violations. Release pin clean.
- Bundle 339669 raw / 74926 gzip; ratchet 354000 / 78000. Presentation code remains outside runtime bundle.
- 19 scratch probes completed. R1 duplicate/current+older quest selections pass with 3 components/75 battles; R2 tied name conflicts pass; R3 mixed-edge order mislabels full clear and cadence. Report contains durable recipes; scratch not committed.
- Godstorm default CLI: 0 fatal / 22 warnings, correct 2 pyramids/50 battles/18 AIs/10 keepers and current rewards. Strict exact-byte CLI: 18 fatal / 4 warnings, correctly incomplete for deterministic rendering.
- harvest.py verify harvests/inbox/tnr_results_1789842714086.json: verified, exit 0; 9 OK, no failed/unverified/skipped items. Committed read-back only, no live re-verification.
- Session guards: lawmap 0 errors / 5 pre-existing warnings; doctrine and packs current. Baseline parity adapter remains RED on checks:null (TypeError), outside correction; no green parity guard claimed.
- Live-game requests 0; live-game writes 0; asset-CDN requests 0. No implementation or Fable branch mutation.

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** forge_size_pass: P0 at 05e71564d693a8505f98df4400502abee7517a3c passes independent review and is unchanged by correction; not integrated. Bundle 339669 raw/74926 gzip; ratchet 354000/78000.; godstorm_publication: The three new Stormcourt assets and the Stormcourt quest are live but HIDDEN, as doctrine requires. Publishing is a separate step that waits on the content admin's go-ahead and is dauntless's to perform.; forge_next_phase1: READY/FROZEN contract remains on main at state/prompt_forge_next_phase1.md; implementation still has not begun.; branch_cleanup: Approved keep/delete plan remains on main at docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md. Redundant refs still present.; quest_studio_phase_s: Accepted source chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15 retained; not integrated.; forge_presentation_studio: P1 correction ac792ef1085c8350fda7bf79050d90ca0ce41879 needs R1-R3 fixes; see docs/reviews/REVIEW_2026-09-20_forge_presentation_studio_p1_correction.md. F1/F2/F6/F7 original defects closed. P2/P3 remain deferred pending foundation review and design acceptance.

**Open items, by owner:**
- dauntless: Godstorm repair is complete and verified; nothing further is owed on it. The three new assets and the quest are live but hidden.; Publishing the Godstorm content is a separate step and waits on the content admin's go-ahead.; Optionally delete redundant branch refs per docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md.
- claude: Correct R1 (duplicate quest selections), R2 (equal-time name conflicts), R3 (success-route order/rewards/cadence) on the Fable branch; preserve closed findings and golden facts. Return new frozen base/merge-base/head after rerunning gates. Do not begin P2 yet.; Include rooted-cycle handling in route corrections; narrative ordinary-word false positives are a nonblocking pre-UI refinement. Archive resolver/approved derivatives/MIME-dimensions remain explicit pre-renderer work.; If approved art/godstorm files change, regenerate the pack; do not change archived shipped evidence during this correction.
- chatgpt: Re-review source selection, dossier assembly, graph/encounter/reward consumers and affected tests when Fable returns a new frozen SHA. Deeper P0 review only if P0 changes.; Design contract/reference at chatgpt/forge-presentation-studio-design@4532ef917a1dfb40d00c554fd7f065e13216afc7 remains a proposal awaiting director acceptance before P2.
- legacy_content_state: The 2026-09-08 mission/law queue is still unreverified. lawmap.py reports 0 errors and 5 pre-existing classification warnings (laws 16d, 18, 37, 61, 69), which belong to the legacy law-provenance workstream and were deliberately not touched.

**Rulings open:** - Whether the pre-upload re-hash stays permanently, or identity alone suffices once the Forge size pass runs. Reviewer accepted it for now.
- Repository path prefix policy for packs (any safe repo-relative path vs an art/ allowlist) remains intentionally open; digest plus commit bind the bytes either way.
- Whether validate.py should learn the imagePack key by INVOKING the Node contract rather than duplicating it.
- Phase 2+ Forge director choices remain deferred until the brief for the phase that needs them.
- Legacy law-provenance issues, including laws 19/23/37, remain outside this work and must be reverified from their owning evidence.

**Next:** Fable closes R1-R3 and returns a new frozen P1 SHA. Do not integrate ac792ef or start P2. No director decision blocks these engineering corrections. This report branch is review evidence, not an integration candidate. Publishing remains user-owned.

Container quirks and cross-cutting laws live in the mounted instructions.
