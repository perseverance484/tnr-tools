# Push staging

Keep only manifests that are currently intended for operator use in this directory.
Builder pickers list `.json` and `.zip` files from `push/`, so finished or superseded manifests must be archived after use.

The pre-cleanup push tree from 2026-09-09 is preserved under `archive/spent-manifests/push-2026-09-09/`.

`53_godstorm_failed_items_repair.json` was run and verified on 2026-09-19 (results
`harvests/inbox/tnr_results_1789842714086.json`, 9/9 VERIFIED) and is archived under
`archive/spent-manifests/push-2026-09-19/` with its outcome recorded there.

## 109–110 Bloodright kit-classification AI capture (stage 1, read-only)

`109_bloodright_classification_ai_capture_1.json` (24 reads) and `110_..._2.json` (23 reads):
`profile.getAllAiNames` plus `profile.getAi` with `persist:"full"` for the 46 AIs that equip a
Bloodright kit jutsu, per the 2026-10-12 census. Zero mutations. This is the before-image for the
unequip → edit → re-equip sequence in RUL-2026-10-18-003. Run both, then return the results bundles.
The unequip, convert and re-equip manifests are built from these results.
