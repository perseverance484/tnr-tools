<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** FORGE PRESENTATION STUDIO P0/P1 INTEGRATED AND RELEASED AS 0.5.1; P2 DESIGN DECISIONS SETTLED. main contains approved 5ac0e947196f88c695d0cdee7aabe75a2f0278b2 verbatim; loader @version 0.5.1 pins forge_bundle.js to 13b313d8eaf0687907178ceedc406a7154e0a473. The size pass took the bundle from 451,847/88,356 to 339,669/74,926 with the ratchet re-set to 354,000/78,000; the repository-side dossier/spec/registry/lint ship outside the runtime bundle and no Presentation Studio UI exists. Three independent review rounds closed F1-F7 and R1-R3 at 522 passing tests. The design contract at chatgpt/forge-presentation-studio-design@4532ef91 is ACCEPTED and four rulings are recorded (RUL-2026-09-20-001..004): decoration off, binaries uncommitted, Forge Next Phase 1 before P2. Checkpoint: docs/reviews/FORGE_PRESENTATION_STUDIO_P0_P1_CLOSEOUT.md. Zero live-game requests or writes all session; dauntless has not yet installed 0.5.1.

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
- Closeout integration verified independently before merge: presentation tree identical at approved 5ac0e94 and main (44a4e8eb); substituting the two 0.5.0 strings in the approved bundle reproduces the released bundle byte for byte; main's bundle blob equals the blob at the pinned commit 13b313d.
- state/status.json and state/active-context.md re-derived from state/digest.json in a scratch tree: both byte-identical to the committed projections, so they are generated rather than hand-edited.
- Doc guards on integrated main 566e4cd: doctrinemap 0 errors/0 warnings; doctrine projections current; packs and TOCs current; lawmap 0 errors / 5 pre-existing warnings.

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** forge_size_pass: COMPLETE / integrated at 05e7156 and released in Forge 0.5.1. Budget ratchet now 354000 raw/78000 gzip; measured 339669/74926.; godstorm_publication: The three new Stormcourt assets and the Stormcourt quest are live but HIDDEN, as doctrine requires. Publishing is a separate step that waits on the content admin's go-ahead and is dauntless's to perform.; forge_next_phase1: NEXT IMPLEMENTATION WORK per RUL-2026-09-20-004. READY/FROZEN contract remains on main at state/prompt_forge_next_phase1.md; implementation still has not begun.; branch_cleanup: Approved keep/delete plan remains on main at docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md. Redundant refs still present.; quest_studio_phase_s: Accepted source chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15 retained; not integrated.; forge_presentation_studio: P0/P1 COMPLETE / integrated and released in Forge 0.5.1. Design contract ACCEPTED (RUL-2026-09-20-001); decoration off, binaries uncommitted (RUL-2026-09-20-002/003). P2 renderer is QUEUED BEHIND Forge Next Phase 1 (RUL-2026-09-20-004); its brief is ChatGPT's to write and is unblocked. Art prerequisites still gate P2: source-archive resolution at 1bca57ee, the approved-derivative path, and MIME/dimensions - 5 of 23 registry entries have verified bytes today.

**Open items, by owner:**
- dauntless: Godstorm repair is complete and verified; nothing further is owed on it. The three new assets and the quest are live but hidden.; Publishing the Godstorm content is a separate step and waits on the content admin's go-ahead.; Optionally delete redundant branch refs per docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md.
- claude: P0 size pass and P1 dossier/spec/lint are integrated and released; no further R1-R3 correction remains.; After director acceptance of the design contract, prepare the concrete P2 brief including source-archive resolution, approved derivatives, MIME/dimensions and exact-art readiness. Keep renderer delivery separate from installed Android acceptance.; If any approved art/godstorm bytes change, regenerate the pack under its existing workflow; do not re-derive shipped art or alter historical captures.
- chatgpt: Design contract/Godstorm reference at chatgpt/forge-presentation-studio-design@4532ef917a1dfb40d00c554fd7f065e13216afc7 remains a proposal awaiting director acceptance before P2.; Continue design/review ownership; Fable retains implementation ownership. R1-R3 closure report is pinned at 939168b6045e2469ec2c9934429b2c61b4ef1a9a.
- legacy_content_state: The 2026-09-08 mission/law queue is still unreverified. lawmap.py reports 0 errors and 5 pre-existing classification warnings (laws 16d, 18, 37, 61, 69), which belong to the legacy law-provenance workstream and were deliberately not touched.

**Rulings open:** - Whether the pre-upload re-hash stays permanently, or identity alone suffices once the Forge size pass runs. Reviewer accepted it for now.
- Repository path prefix policy for packs (any safe repo-relative path vs an art/ allowlist) remains intentionally open; digest plus commit bind the bytes either way.
- Whether validate.py should learn the imagePack key by INVOKING the Node contract rather than duplicating it.
- Legacy law-provenance issues, including laws 19/23/37, remain outside this work and must be reverified from their owning evidence.
- Forge Next Phase 2+ director choices remain deferred until the brief for the phase that needs them. The Presentation Studio decisions are settled (RUL-2026-09-20-001..004).

**Next:** Forge Next Phase 1 is next: implement from the frozen contract at state/prompt_forge_next_phase1.md. Presentation Studio P0/P1 are integrated and released as 0.5.1; its P2 brief is unblocked but queued behind Phase 1, and its art prerequisites still gate the renderer. dauntless still has to install 0.5.1 and confirm the panel reads forge 0.5.1. Godstorm publishing remains a separate user-owned action on the content admin's go-ahead.

Container quirks and cross-cutting laws live in the mounted instructions.
