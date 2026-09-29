<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** POTENCY DESIGN REVISION 2.1 RECORDED on chatgpt/potency-chakra-mandala-design-20260929. RUL-2026-09-29-002 supersedes the old progression and radial presentation: two 5-SP skills per school, +2.5% each, 30 Potency SP, +15% maximum overlap. Design graph has five categories and 64 schools including 16 Hidden Arts candidates and 15 retained Advanced Arts candidates. Hidden roster awaits dauntless review before imagery. RUL-2026-09-29-003 defers Absorb, Assimilation, Hollow Palm and Empty Vessel. Elemental healing/jutsu scope and a separate 30-SP cap remain implementation gaps. Live-game requests/writes 0/0. Unrelated operational entries below are inherited history and were not re-audited in this session.

**Verified at close (exact runs):**
- lawmap -> 93 laws, 93 matrix rows, 77 citations across 35 files; 0 errors, 5 warnings
- doctrine projections -> all projections current (exit 0)
- packs/TOCs -> all packs and TOCs current (exit 0)
- Live refs at bootstrap: main and merge-base 1601f072af839402395eeab1326b1228747e0009; assigned design branch 36bc4cc7aa79321e52f8e90584933d5c747497a7; upstream 9f01172038dbc412c837a7f97f7451eb87b6a234.
- Potency structural audit PASS: 64 unique schools, 64 affordable Majors, no dependency cycles, ten allocation assertions and four Special Element tradeoff comparisons. Graph digest and limits recorded in docs/design/POTENCY_V2_VALIDATION_2026-09-29.md.
- Potency workstream validates and renders. Repository-wide workstream validation remains incomplete because unrelated sparse-checkout artifacts are absent; automatic approval review rejected their out-of-scope fetch.
- Absorb is excluded from this design because it is absent from the pinned upstream PotencyTagTypes; Heal/Increase Heal lack elements; the purchase router has no dedicated Potency budget enforcement.
- Hidden/Advanced names and unlocks remain proposals; no images generated, no manifests authored, no upstream code changed. Live-game requests 0; writes 0; asset-CDN requests 0.
- Absorb amendment checked against branch input 664437382ba33a16023ad8e2feae12d90371336f; active graph has no Absorb selector, removed-school prerequisite or outgoing unlock. RUL-2026-09-29-003 recorded.

**Start ritual:** per the mounted instructions - clone, repo-local identity,
session_open.py (verify any new inbox bundle FIRST). No clone means no state.

**In progress:** forge_size_pass: COMPLETE / integrated at 05e7156 and released in Forge 0.5.1. Budget ratchet now 354000 raw/78000 gzip; measured 339669/74926.; godstorm_publication: The three new Stormcourt assets and the Stormcourt quest are live but HIDDEN, as doctrine requires. Publishing is a separate step that waits on the content admin's go-ahead and is dauntless's to perform.; forge_next_phase1: NEXT IMPLEMENTATION WORK per RUL-2026-09-20-004. READY/FROZEN contract remains on main at state/prompt_forge_next_phase1.md; implementation still has not begun.; branch_cleanup: Approved keep/delete plan remains on main at docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md. Redundant refs still present.; quest_studio_phase_s: Accepted source chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15 retained; not integrated.; forge_presentation_studio: P0/P1 COMPLETE / integrated and released in Forge 0.5.1. Design contract ACCEPTED (RUL-2026-09-20-001); decoration off, binaries uncommitted (RUL-2026-09-20-002/003). P2 renderer is QUEUED BEHIND Forge Next Phase 1 (RUL-2026-09-20-004); its brief is ChatGPT's to write and is unblocked. Art prerequisites still gate P2: source-archive resolution at 1bca57ee, the approved-derivative path, and MIME/dimensions - 5 of 23 registry entries have verified bytes today.; potency_skill_tree: DESIGN RECONCILED; 16 Hidden Arts candidates ready for user review. See docs/design/POTENCY_HIDDEN_ARTS_ROSTER_V2.md and state/workstreams/potency_skill_tree/roadmap.json. Final acceptance, artwork and implementation have not occurred.

**Open items, by owner:**
- dauntless: Godstorm repair is complete and verified; nothing further is owed on it. The three new assets and the quest are live but hidden.; Publishing the Godstorm content is a separate step and waits on the content admin's go-ahead.; Optionally delete redundant branch refs per docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md.; Review the 16 Hidden Arts names, selectors and unlocks, including four cross-discipline Special Element pairs. Boil/Metal/Sand mappings and final Advanced Arts choices remain open.
- claude: P0 size pass and P1 dossier/spec/lint are integrated and released; no further R1-R3 correction remains.; After director acceptance of the design contract, prepare the concrete P2 brief including source-archive resolution, approved derivatives, MIME/dimensions and exact-art readiness. Keep renderer delivery separate from installed Android acceptance.; If any approved art/godstorm bytes change, regenerate the pack under its existing workflow; do not re-derive shipped art or alter historical captures.
- chatgpt: Design contract/Godstorm reference at chatgpt/forge-presentation-studio-design@4532ef917a1dfb40d00c554fd7f065e13216afc7 remains a proposal awaiting director acceptance before P2.; Continue design/review ownership; Fable retains implementation ownership. R1-R3 closure report is pinned at 939168b6045e2469ec2c9934429b2c61b4ef1a9a.; Continue Potency design from its committed workstream; after roster review, inspect actual approved image references before producing a Hidden Arts showcase.
- legacy_content_state: The 2026-09-08 mission/law queue is still unreverified. lawmap.py reports 0 errors and 5 pre-existing classification warnings (laws 16d, 18, 37, 61, 69), which belong to the legacy law-provenance workstream and were deliberately not touched.

**Rulings open:** - Whether the pre-upload re-hash stays permanently, or identity alone suffices once the Forge size pass runs. Reviewer accepted it for now.
- Repository path prefix policy for packs (any safe repo-relative path vs an art/ allowlist) remains intentionally open; digest plus commit bind the bytes either way.
- Whether validate.py should learn the imagePack key by INVOKING the Node contract rather than duplicating it.
- Legacy law-provenance issues, including laws 19/23/37, remain outside this work and must be reverified from their owning evidence.
- Forge Next Phase 2+ director choices remain deferred until the brief for the phase that needs them. The Presentation Studio decisions are settled (RUL-2026-09-20-001..004).
- Potency: Hidden Arts candidate roster and gates; final Advanced Arts scope/names; provisional Boil/Metal/Sand topology. Progression is settled, not an open decision.

**Next:** Potency: review the full Hidden Arts roster with dauntless, then revise any names/effects/unlocks before image generation. Resume from state/workstreams/potency_skill_tree/roadmap.json. Unrelated inherited workstream queues were not re-ordered or re-verified.

Container quirks and cross-cutting laws live in the mounted instructions.
