# Godstorm art-reuse decisions

Updated: 2026-09-15. This is the task-specific asset acceptance/disposition record for Marrow Vaults and Stormcourt. Read alongside `GODSTORM_TWO_PYRAMID_RELEASE_PLAN.md` and `GODSTORM_STANDALONE_COPY_AND_SCENE_MAP.md`. It owns the operative asset exclusion below; `docs/RULINGS.md` preserves the director decision history.

## AR-001 — StormCourtyard rejected for Godstorm

**Status:** EXCLUDED_BY_DIRECTOR. No Godstorm use approved.

**Decision:** The user rejected StormCourtyard because it belongs to a different artwork/quest set. Do not use this asset as Stormcourt scenery, a donor image, or a style reference for the Godstorm release. Do not crop, recolor, rename or otherwise adapt it to evade the rejection.

**Identity:** `StormCourtyard`, gameAsset ID `cKHhHoboreP88iH5WjDe7`, captured folder `SkychainMonastery`. This exclusion concerns the scene background, not the retained Stormcourt quest listing image or the Court's enemy portraits.

**Supersedes:** The proposed S1 association in Draft 2 of `GODSTORM_STANDALONE_COPY_AND_SCENE_MAP.md` at `0ac6341748e32e86888e683ceccf17252666bbbc`, and the release plan's assumption that this shared-library candidate might fill the Court's environment needs. Those were unapproved proposals; they are now withdrawn, not waiting for another suitability test.

## Binding correction

All 26 proposed Stormcourt S1 bindings are void. Their effective planning value is **UNRESOLVED — no approved background ID**:

- `d6_1`, `d6_2`, `d6_3`, `d6_4`, `d6_boss`.
- `d7_1`, `d7_2`, `d7_3`, `d7_4`, `d7_boss`.
- `d8_1`, `d8_2`, `d8_3`, `d8_4`, `d8_boss`.
- `d9_1`, `d9_2`, `d9_3`, `d9_4`, `d9_boss`.
- `d10_1`, `d10_2`, `d10_3`, `d10_4`, `d10_boss`.
- `d10_victory`.

`S1` is not a usable runtime alias and must not resolve to the excluded asset in any build. The scene-map prose, graph, opponent order and character proposals are otherwise unchanged by this decision. Reuse other SkychainMonastery assets only through a new explicit direction decision, never as automatic substitutes for the rejected image.

## Corrected planning status

| Area | Current status |
| --- | --- |
| Marrow environments | Three recovered backgrounds; scene-fit/final acceptance status unchanged |
| Stormcourt environments | Zero approved backgrounds identified in the current recovered selection |
| Stormcourt scene assignments | 26 unresolved background selections; not 26 new paintings |
| New background commission count | Open; identify suitable Godstorm artwork or approve a new direction before setting the count |
| Core structure | Unchanged: Vaults below, Court above, two sequential 25-battle quests, no cash-out |
| Other recovered images | Not approved or rejected by this single-asset decision |

The previous zero-new-background target is not proof that the Court is covered. No new commission, replacement count, palette or completed visual set is approved here.

## Archive versus release selection

The recovery archive still contains 19 downloaded files as historical evidence. Keep its original bytes, hashes and capture index unchanged. One of those files is now excluded from the Godstorm review/production selection; 18 other recovered files remain available for their existing review process. Successful download/decoding does not confer art approval.

Display StormCourtyard only in a clearly marked rejected-reference/archive section, not among current Godstorm environment options. No game record or shared source artwork is deleted, renamed or modified. The asset remains valid for its original quest set; this is not a technical-invalidity claim.

## Evidence

- Director's instruction: Storm Courtyard is not approved because it belongs to a different artwork/quest set.
- Captured record: `harvests/inbox/tnr_results_1789402842027.json`, snapshot `24-mu1g8vqp::after::29`, `data.image`, at repository capture baseline `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`.
- Recovery archive: `art/godstorm_sources/capture-2026-09-14/index.json` on `chatgpt/godstorm-art-recovery`, verified at `f9bb4aafab2c83f764363a83b4c0abd58d69dc46` for AR-001.

AR-001 records an acceptance decision and its planning consequences. No art generation, new capture, game operation or engine/manifest validation was performed for that decision.

## AR-002 — Source inspection and Court direction proposal

**Status:** SOURCE_INSPECTION_COMPLETE / DIRECTION_PROPOSED. Not a new director ruling or asset acceptance.

The user authorized proceeding with direction based on Marrow backgrounds and retained Court character artwork. `GODSTORM_STORMCOURT_VISUAL_DIRECTION.md`, introduced at `77edd9a047fd5bfec050bd1f681499a3d90fb6b2`, records actual individual-source inspection, archive-integrity verification, exposure measurements, a proposed Court design and bounded production allocation.

Key results:
- Thirteen original images were individually inspected: three Marrow backgrounds, nine Stormcourt avatars and the Court listing image. The excluded StormCourtyard and earlier infographic artwork were not used as references.
- The proposed Court continues Marrow's dark masonry, arches, brass details and violet energy into a rain-exposed upper court. This is a proposed design, not a completed background.
- Recommended output allocation: two new masters (Upper Court for 20 dialogs, Binding Dais for five) plus one released-state derivative for the victory dialog. This remains unapproved; all 26 runtime bindings remain unresolved under AR-001. The derived finale state is conditional on acceptance of the binding-breaking ending.
- Pixel inspection shows Marrow plate 3 looking down a stairwell. Proposed correction: use it for the initial descent, and plate 2's part-open threshold for the final handoff. This is not an applied binding change.
- Marrow plates 2 and 3 need readability review against the current exposure guidance; recovered size is 500x333. No originals were altered or automatically rejected/replaced. The detailed report distinguishes diagnostics from repository art-preflight execution.

The current graph/encounter counts, rejected-asset decision, unresolved source-record/portrait IDs, reward decisions and live-operation boundaries are unchanged. The next asset would be a single Upper Court candidate after direction review, not an automatic three-image batch. Final art acceptance remains with dauntless.
