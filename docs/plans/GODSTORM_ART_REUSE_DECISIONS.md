# Godstorm art-reuse decisions

Updated: 2026-09-19. This is the task-specific asset acceptance/disposition record for Marrow Vaults and Stormcourt. Read alongside `GODSTORM_TWO_PYRAMID_RELEASE_PLAN.md` and `GODSTORM_STANDALONE_COPY_AND_SCENE_MAP.md`. It owns the operative asset exclusion below; `docs/RULINGS.md` preserves the director decision history.

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


## AR-003 — Upper Court accepted and production-exported

**Status:** ACCEPTED_BY_DIRECTOR / PRODUCTION_EXPORT COMPLETE LOCALLY. Runtime gameAsset creation and wiring are not complete.

**Decision:** The user accepted the generated Stormcourt Upper Court composition on 2026-09-18. Preserve that composition as the main Stormcourt environment for the first 20 retained Court dialogs, subject to final runtime asset creation/wiring through the normal implementation lane.

**Production filename:** `bg_godstorm_stormcourt_upper_court.webp`.

**Source candidate:** `stormlit_gothic_tribunal_courtyard.png`, generated at 1536x1024 and accepted before export.

**Production export evidence:**
- output: 1536x1024 RGB WebP;
- codec: lossy WebP, quality 85 / method 6, matching the current SCENE_BACKGROUND export mode;
- bytes: 379,928 (371.0 KB);
- SHA-256: `c0587d9fdeb8c4c75ecc6f5eaf0c08a0b783461299793c774f66f7aaab4f12b9`;
- aspect: 1.500000, within the current 3:2 target tolerance;
- minimum width: pass against 512px;
- working ceiling: pass against 460,800 bytes;
- hard cap: pass against 524,288 bytes;
- alpha: flattened / none;
- exposure diagnostic: median luminance 17, 54.28% of pixels below 20; inside the current background guidance rather than the reject band;
- lower-left reserve diagnostic: median luminance 12;
- client-size preview checked at 512x341 and composition remained readable with the lower-left overlay region usable.

The ChatGPT execution environment did not have a repository checkout, so the repository's `artpreflight.py` and `chroma.py` files were not executed as commands. The export and the relevant current preflight checks were applied directly from the scripts/spec read at main `015583ba581388ed53770cb3a2ce7ad899cad6e3`. Before repository handoff/live wiring, rerun the actual current repository art preflight in a checkout and require zero errors. This execution limitation does not change the accepted visual direction or the exact output hash above.

**Coverage intent:** Upper Court remains the planned background for Stormcourt dialogs `d6_1` through `d9_boss` (20 dialogs). Actual gameAsset ID and quest bindings do not yet exist.

**Next asset:** Binding Dais — active, using the accepted Upper Court as the primary Stormcourt environment reference. Do not batch-generate the released-state variant until the active dais is reviewed.

This acceptance does not approve rewards, the final binding-resolution prose, keeper portraits, missing Marrow avatars, publication, or live operation.


## AR-004 — Marrow background remap approved

**Status:** ACCEPTED_BY_DIRECTOR / MANIFEST-READY ASSIGNMENT. Runtime quest wiring is not complete.

The user approved the post-inspection Marrow remap on 2026-09-18.

Apply these two binding changes in the revised Marrow scene map:
- `d1_1`: use `M3` / `marrow vault 3` / gameAsset `IykL5XxwFF14BosCblZj8` for the initial descent into the lower vaults.
- `d5_victory`: use `M2` / `marrow vault 2` / gameAsset `oc0cXiMrcG_6kTUwNWRkn` for the part-open threshold at the Vaults-to-Court handoff.

All other proposed Marrow background allocations remain as previously specified unless separately changed. This supersedes Draft 2's `d1_1 = M1` and `d5_victory = M3` assignments. No source image is flipped, repainted or otherwise modified by this decision.

The three recovered Marrow plates remain legacy 500x333 source files and retain their previously documented resolution/readability caveats. Acceptance of this remap is a scene-fit decision, not a claim that those legacy files have passed the current production-art preflight.

## AR-005 — Binding Dais active accepted and production-exported

**Status:** ACCEPTED_BY_DIRECTOR / PRODUCTION EXPORT COMPLETE LOCALLY. Runtime gameAsset creation and wiring are not complete.

The user accepted the generated Binding Dais active composition on 2026-09-18 for the final five Stormcourt pre-victory dialogs.

**Production filename:** `bg_godstorm_stormcourt_binding_dais_active.webp`.

**Source candidate:** `wide_cinematic_atmospheric_gothic_fantasy_scene.png`, generated at 1536x1024 and accepted before export.

**Production export evidence, verified against the unchanged SCENE_BACKGROUND contract at current main `9e1dafc3ee5c8884ce90c3530de4afba364fad24`:**
- output: 1536x1024 RGB WebP;
- codec: lossy WebP, quality 85 / method 6;
- bytes: 283,000 (276.4 KB);
- SHA-256: `41ca12f9d21604151f754ded0df2211bed5b671dcc2dd7c954e53c5f17f36d70`;
- exact aspect: 3:2;
- minimum width 512: pass;
- working ceiling 460,800 bytes: pass;
- hard cap 524,288 bytes: pass;
- alpha: flattened / none;
- exposure diagnostic: median luminance 39; 23.07% of pixels below 20.

**Coverage:** `d10_1`, `d10_2`, `d10_3`, `d10_4`, `d10_boss`.

A 512x341 delivered-size preview was generated for review. Before repository handoff/live wiring, rerun the current repository `artpreflight.py` against the exact production bytes and require zero errors.

## AR-006 — Binding Dais released accepted and production-exported

**Status:** ACCEPTED_BY_DIRECTOR / PRODUCTION EXPORT COMPLETE LOCALLY. Runtime gameAsset creation and wiring are not complete.

The user accepted the released-state Binding Dais composition on 2026-09-18 as the post-victory state of the same Stormcourt location.

**Production filename:** `bg_godstorm_stormcourt_binding_dais_released.webp`.

**Source candidate:** `a_dramatic_cinematic_photorealistic_digital_pain.png`, generated at 1536x1024 and accepted before export.

**Production export evidence, verified against the unchanged SCENE_BACKGROUND contract at current main `9e1dafc3ee5c8884ce90c3530de4afba364fad24`:**
- output: 1536x1024 RGB WebP;
- codec: lossy WebP, quality 85 / method 6;
- bytes: 256,826 (250.8 KB);
- SHA-256: `97fc11d4ad1c24beeaffaf2e7f8a589715806dce6d17290d0fa253694fd3ef18`;
- exact aspect: 3:2;
- minimum width 512: pass;
- working ceiling 460,800 bytes: pass;
- hard cap 524,288 bytes: pass;
- alpha: flattened / none;
- exposure diagnostic: median luminance 44; 18.58% of pixels below 20.

**Coverage:** `d10_victory` only.

A 512x341 delivered-size preview was generated for review. Before repository handoff/live wiring, rerun the current repository `artpreflight.py` against the exact production bytes and require zero errors.

## Current accepted environment allocation

The operative accepted background plan is now:

| Quest area | Dialog coverage | Asset |
| --- | --- | --- |
| Marrow entry | `d1_1` | M3 / marrow vault 3 |
| Marrow retained non-entry scenes | per Draft 2 except the two remaps above | M1/M2 |
| Marrow victory handoff | `d5_victory` | M2 / marrow vault 2 |
| Stormcourt Upper Court | `d6_1` through `d9_boss` | new Upper Court production asset |
| Stormcourt Binding Dais active | `d10_1` through `d10_boss` | new active Dais production asset |
| Stormcourt Binding Dais released | `d10_victory` | new released Dais production asset |

The three new Stormcourt production files are accepted visual outputs, but they still need durable binary placement, current-repo art preflight, gameAsset creation, resulting runtime IDs and quest wiring before an executable mutation manifest can be frozen.

No change here approves the five missing Marrow AI avatars, keeper scene portraits, blank scene-character record, quest prose, rewards, balance changes, publication or any live operation.
