# Godstorm two-pyramid plan: verification notes

Prepared: 2026-09-15. Read with `docs/plans/GODSTORM_TWO_PYRAMID_RELEASE_PLAN.md` on this branch. This is a planning clarification, not a mutation manifest or approval of proposed scope details.

Repository evidence baseline: `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`. Captured game records are dated 2026-09-14. The recorded user scope remains two pyramids, no new keystone assets, reuse first, planning before execution, and chest/rewards open to Content Admin. See `docs/RULINGS.md#rul-2026-09-15-001--godstorm-two-pyramid-planning-scope`.

## Exact retained inventory

The retained graphs contain 122 objectives: 50 battles, 68 dialogs and four terminal nodes. Each pyramid contains 25 battles, 34 dialogs and two terminal nodes. The 68 dialogs are 50 pre-battle scenes, eight continue/withdraw choices, eight withdrawal payoffs and two full-clear victories.

The retained direct-opponent population is 18 AIs: 13 primary avatar fields have non-default images; five are default. All five defaults are Marrow enemies: Umbral Reaver, Hollow Lantern, Starless Monk, Nightveil Sentinel and Warden of the First Dark. Removing Dawnless excludes five unique keepers, not just its final boss. Twinned Reliquary and Loomwright must not remain in Marrow's backlog.

These are record-derived planning counts. They do not certify 50 playtested encounters or 13 pixel-approved avatar files. The local reproducibility gate in the main plan must join the captures programmatically and close auxiliary dependencies before implementation.

## Background clarification

The main plan's current-state table should not be read as four dedicated Godstorm backgrounds. Three records are dedicated Marrow plates; `StormCourtyard` is a captured **SkychainMonastery** asset being considered for reuse. It is not wired into the retained Stormcourt graph.

Existing Marrow assignments are exactly:
- `marrow vault 1`: `d1_1`, `d1_2`, `d1_boss`, `d1_choice`.
- `marrow vault 2`: `d1_3`, `d1_4`.
- `marrow vault 3`: `d1_cash`.

This leaves 27 Marrow and 34 Stormcourt dialog background assignments to fill: 61 total. All 68 placements, including the existing seven, still require a visual-fit review. Zero new background paintings is a reuse target, not a verified finding that the currently selected plates fit every scene.

The older asset catalog identifies `AbbotsBellDais`, `SummitShrine` and `SkychainOpening` as additional discovery candidates. Do not count them as accepted or current without checking the record and pixels. Reuse references or approved derivatives; do not modify a shared original used by other content.

The checked Logbook source selects a scene background from `gameAsset.image`, not `gameAsset.url`. An unrelated default `url` field therefore does not make the captured background image invalid. If objective and quest background references are empty, the client uses its engine fallback; it does not inherit the prior floor's custom image.

## Scene-character workload

The recommended keeper-only presentation needs ten keeper portrait assets/eligible records, one for each retained keeper. Nine already have primary avatar art to inspect as possible source material. The Warden of the First Dark can share one master between avatar and portrait. Extraction feasibility is not proven from the URLs.

Wire ten keeper dialogs to the corresponding portraits and 58 other dialogs to one verified blank character. Also set the verified blank as the main character fallback on both quests. The checked quest-update source requires either main characters or characters on every objective when publishing; populating only dialog characters does not satisfy the second route if battles/control nodes remain empty.

Four proposed base/Ascendant avatar reuses plus one unmatched Warden close five avatar assignments. Ten keeper portrait deliverables are a separate adaptation task. Do not add these to wiring operations and call the result a number of newly painted images. New source art is commissioned only after recovery, inspection, reuse/extraction trials and user approval.

## Reward and progression checks

Content Admin must approve the period, completion count and attempt policy together. In the additionally inspected source, `periodCapReached` compares current-period completions to `maxCompletes`. Consequently `retryDelay:"daily"` with `maxCompletes:100` is not a one-success-per-day configuration. Changing Marrow's delay string alone is not the complete proposed economy fix. Lifetime attempt behavior must also be checked for the relevant quest type.

The captured early withdrawals and full clears both end in `win_quest`, while the prerequisite check tests successful completion of Marrow, not completion of floor 5. The main plan's full-clear-only recommendation is not already implemented. Fable must identify a source-supported gate and its cost before it is approved. Allowing early-withdrawal unlocks is the lower-scope alternative; either choice needs explicit user approval and matching copy.

The chest remains an admin decision. Its current empty table, default icon and `destroyOnUse:true` are recorded, not accepted. A retained chest may require one icon assignment, preferably reused. Include existing player copies and all keeper inventory drop channels in the review. Do not claim that a later quest loss reverses ordinary combat gains or already granted loot without evidence, and do not introduce inventory clawbacks.

## Additional pinned source evidence

This pass additionally inspected `studie-tech/TheNinjaRPG@bdec2883748f029a0ecb93505adfdcbae6851fe9`:
- `app/src/layout/Logbook.tsx`, lines 360-425: scene source selection and fallback.
- `app/src/server/api/routers/quests.ts`, within lines 675-775: scene-character publication guard.
- `app/src/libs/quest.ts`, `postProcessRewards`, `periodCapReached` and `isAvailableUserQuests`: reward chance/quantity, period caps and successful-prerequisite semantics.

The main draft names a different source-review pin, `31996f1f9cb10dae246740afe273f164a2bb469b`. These pins are not interchangeable evidence of the deployed revision. Before implementation, reconcile the relevant source paths and current generated contracts; neither this note nor the draft adopts regenerated contracts or asserts the production deployment SHA.

Capture sources: `harvests/inbox/tnr_results_1789401726302.json` (quest graphs), `tnr_results_1789402842027.json` in the same directory (AI records, embedded kits, items and backgrounds), and `tnr_results_1789403623148.json` (AI profiles). Candidate-only catalog: `harvests/seed/43_INDEX_asset.json`, stamped 2026-08-24.

## Checks still open

No local clone, capture-normalization run, graph-derived shot-list generation, image-byte/pixel QC, automated content test suite, live gameplay or revised read-back was completed during this planning pass. Shared jutsu icons, effect assets, any actual summon dependencies and relevant alternate-avatar client paths remain a bounded inventory task, not an assumed zero-asset gap. The two-pyramid implementation, reward approval, active-run transition and publishing are not complete.

The next gate is approval of the proposed 25+25 structure/finale, unlock policy and reuse presentation, followed by reproducible inventory and pixel recovery. Chest/reward decisions can remain open while those tasks proceed; no unapproved reward placeholders may pass the final release gate.
