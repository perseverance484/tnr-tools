<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** FORGE PRESENTATION STUDIO P0/P1 INTEGRATED; FORGE 0.5.1 RELEASE PIN VERIFIED. main@42cbcb8a06a168e594e303c812a61b3d1a1cbeb3 contains approved 5ac0e947196f88c695d0cdee7aabe75a2f0278b2 verbatim; loader @version 0.5.1 pins forge_bundle.js to 13b313d8eaf0687907178ceedc406a7154e0a473. The size pass and repository-side dossier/spec/lint are complete; no Presentation Studio UI is released. docs/reviews/FORGE_PRESENTATION_STUDIO_P0_P1_CLOSEOUT.md. Next: accept the design contract and prepare the P2 brief with exact-art prerequisites. This checkpoint made zero live-game requests/writes; installed Android uptake was not tested.

**Verified at close (exact runs):**
- Live refs verified: main 42cbcb8a06a168e594e303c812a61b3d1a1cbeb3; Fable branch 13b313d8eaf0687907178ceedc406a7154e0a473; approved 5ac0e947196f88c695d0cdee7aabe75a2f0278b2 is a direct ancestor of main.
- History: eefefd1 -> 05e7156 -> 8830443 -> ac792ef -> 5ac0e94 -> 13b313d -> 42cbcb8. Approved implementation present verbatim.
- Release delta is version/pin-only in five files. Replacing two 0.5.0 strings with 0.5.1 in the approved Forge bundle produces the released bundle byte for byte.
- Presentation tree identical at approved/main: 44a4e8eb8c62455cde029ed3e8b07dd0f5adcf45. Main bundle equals immutable pin target; legacy builder bundle unchanged from its previous pin.
- Package/runtime/loader 0.5.1; loader @require at 13b313d8eaf0687907178ceedc406a7154e0a473; no pending marker; release-pin check clean.
- Release budget check: 339669 raw/74926 gzip, ceilings 354000/78000.
- Prior review 939168b6045e2469ec2c9934429b2c61b4ef1a9a at approved 5ac0e94: R1-R3 closed; 522 tests and 17 focused assertions passed; build/fixtures reproducible. Those full checks were not rerun for this version-only checkpoint.
- Session guards at release checkout: lawmap 0 errors/5 existing warnings; doctrine and packs current. Baseline parity adapter remains RED on checks:null; not changed or reported green.
- Live-game requests 0; live-game writes 0; asset-CDN requests 0. No installed Android session, CDN delivery, renderer, or export/share validation.

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** forge_size_pass: COMPLETE / integrated at 05e7156 and released in Forge 0.5.1. Budget ratchet now 354000 raw/78000 gzip; measured 339669/74926.; godstorm_publication: The three new Stormcourt assets and the Stormcourt quest are live but HIDDEN, as doctrine requires. Publishing is a separate step that waits on the content admin's go-ahead and is dauntless's to perform.; forge_next_phase1: READY/FROZEN contract remains on main at state/prompt_forge_next_phase1.md; implementation still has not begun.; branch_cleanup: Approved keep/delete plan remains on main at docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md. Redundant refs still present.; quest_studio_phase_s: Accepted source chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15 retained; not integrated.; forge_presentation_studio: P0/P1 COMPLETE / integrated, F1-F7 and R1-R3 closed. P2 renderer/UI not begun in this handoff; design proposal acceptance and exact-art/derivative/MIME-dimensions work remain next prerequisites.

**Open items, by owner:**
- dauntless: Godstorm repair is complete and verified; nothing further is owed on it. The three new assets and the quest are live but hidden.; Publishing the Godstorm content is a separate step and waits on the content admin's go-ahead.; Optionally delete redundant branch refs per docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md.
- claude: P0 size pass and P1 dossier/spec/lint are integrated and released; no further R1-R3 correction remains.; After director acceptance of the design contract, prepare the concrete P2 brief including source-archive resolution, approved derivatives, MIME/dimensions and exact-art readiness. Keep renderer delivery separate from installed Android acceptance.; If any approved art/godstorm bytes change, regenerate the pack under its existing workflow; do not re-derive shipped art or alter historical captures.
- chatgpt: Design contract/Godstorm reference at chatgpt/forge-presentation-studio-design@4532ef917a1dfb40d00c554fd7f065e13216afc7 remains a proposal awaiting director acceptance before P2.; Continue design/review ownership; Fable retains implementation ownership. R1-R3 closure report is pinned at 939168b6045e2469ec2c9934429b2c61b4ef1a9a.
- legacy_content_state: The 2026-09-08 mission/law queue is still unreverified. lawmap.py reports 0 errors and 5 pre-existing classification warnings (laws 16d, 18, 37, 61, 69), which belong to the legacy law-provenance workstream and were deliberately not touched.

**Rulings open:** - Whether the pre-upload re-hash stays permanently, or identity alone suffices once the Forge size pass runs. Reviewer accepted it for now.
- Repository path prefix policy for packs (any safe repo-relative path vs an art/ allowlist) remains intentionally open; digest plus commit bind the bytes either way.
- Whether validate.py should learn the imagePack key by INVOKING the Node contract rather than duplicating it.
- Phase 2+ Forge director choices remain deferred until the brief for the phase that needs them.
- Legacy law-provenance issues, including laws 19/23/37, remain outside this work and must be reverified from their owning evidence.

**Next:** P0/P1 are integrated and Forge 0.5.1 is pinned. Next design checkpoint: director acceptance of the durable design contract and the concrete P2 brief. Carry exact-art completion forward; do not imply a studio UI or Android export flow already ships. Godstorm publishing remains a separate user-owned action.

Container quirks and cross-cutting laws live in the mounted instructions.
