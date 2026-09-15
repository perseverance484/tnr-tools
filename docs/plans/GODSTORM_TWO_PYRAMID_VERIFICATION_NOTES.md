# Godstorm: verification notes after concept separation

Updated: 2026-09-15. Operative requirements belong to `docs/plans/GODSTORM_TWO_PYRAMID_RELEASE_PLAN.md`; decision history belongs to RUL-2026-09-15-002 in `docs/RULINGS.md`. These notes distinguish captured evidence from derived revision targets and unperformed checks.

Repository evidence baseline: `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`. Previous plan/notes: `11c55562f440e804a546163cb747a9fc8bc7e95c`. That version remains available as history; its cash-out delivery requirements are no longer operative.

## 1. Count reconciliation

The September 14 retained graphs have 122 objectives: 50 battles, 68 dialogs and four terminal nodes. The dialogs include eight continue/cash-out choices and eight cash-out payoffs. Removing those sixteen dialogs without adding replacements gives the minimal rewrite target:

- 106 objectives = 50 battles + 52 dialogs + four terminal nodes.
- Per pyramid: 53 objectives = 25 battles + 25 pre-battle dialogs + one victory dialog + two terminal nodes.
- One full-clear successful ending per pyramid; no early successful paid exit.

These are derived target counts, not results from a graph validator, payload implementation or fresh live read. Fable must reproduce the actual retained-ID inventory and validate the eight intermediate-keeper success reroutes before handoff. Preserve every pre-battle dialog gate.

The direct opponent population remains 18 AIs: 13 non-default primary avatars and five defaults. All five defaults are in Marrow: Umbral Reaver, Hollow Lantern, Starless Monk, Nightveil Sentinel and Warden of the First Dark. No enemy is removed merely because cash-out nodes are removed. Twinned Reliquary and Loomwright remain excluded with Crown.

## 2. Background and character arithmetic

Marrow had seven assigned dialog backgrounds in the capture. The proposed deletion removes TWO assigned nodes: `d1_choice` (plate 1) and `d1_cash` (plate 3). Five existing assignments survive:
- Plate 1: `d1_1`, `d1_2`, `d1_boss`.
- Plate 2: `d1_3`, `d1_4`.

Thus 26 - 5 = 21 Marrow background gaps; Stormcourt has 26 - 0 = 26 gaps; total target gap = 47. Do not report 46 by overlooking the removed choice node's existing background. All 52 retained scenes still require visual-fit review.

The third Marrow plate is not deleted. Its only captured use was the removed cash-out, so a suitable new retained placement should be assessed. `StormCourtyard` is a captured SkychainMonastery asset being considered for reuse, not dedicated Godstorm art. The older catalog's AbbotsBellDais, SummitShrine and SkychainOpening remain unverified candidates. Zero new paintings is a reuse target, not proven complete coverage.

Under the proposed keeper-focused art scope, ten keeper introductions use portraits and 42 other dialogs use one verified blank, with two main quest fallbacks. The previous 58-blank/68-dialog figures describe the old graph only. Nine existing keeper avatars are potential portrait sources, not proven extractable pixels or accepted scene-character files.

Five avatar assignments, ten keeper-portrait outputs, 47 missing background bindings and 52 character bindings are different work units. Do not total them as original illustrations.

## 3. Progression and reward implications

With no early successful exit, the retained Marrow prerequisite no longer needs an extra marker solely to distinguish new-run cash-out success from full clear. Validate that only the final battle/victory path can complete the revised quest. Preserve the prerequisite; a decision to make the two Godstorm locations separately accessible would be a separate scope change.

Historical successful completions and active trackers remain migration concerns. Do not revoke previous completions, reset player inventories or assume removal of nodes automatically fixes existing trackers. An operator-approved transition is required.

Content Admin now approves two full-clear packages, not ten alternative exit tiers. The old `Endless Night Chest` is Tower-branded and shared. Review its consumers, all enemy drop channels and existing player copies before choosing a neutral/Godstorm identity, safe rename, replacement or omission. No global item rename is authorized by the naming decision alone. Empty consumable content is not accepted release content.

Period, completion count and attempt rules must still be checked together. Prior source inspection found that daily with maxCompletes 100 is not one rewarded clear per day. No exact cadence or reward values were approved by structural acceptance.

## 4. Prior source evidence and unresolved version scope

Before this revision, review notes inspected `studie-tech/TheNinjaRPG@bdec2883748f029a0ecb93505adfdcbae6851fe9`:
- `app/src/layout/Logbook.tsx`, lines 360-425: scene references use gameAsset.image; objective/quest fallback selection.
- `app/src/server/api/routers/quests.ts`, within lines 675-775: scene-character publication guard; do not assume dialog-only population satisfies the every-objective route.
- `app/src/libs/quest.ts`, postProcessRewards, periodCapReached and isAvailableUserQuests: chance/quantity, completion periods and successful prerequisite semantics.

The earlier main draft also named source-review pin `31996f1f9cb10dae246740afe273f164a2bb469b`. Neither is proof of the deployed revision. This turn did not newly verify or reconcile those upstream files. Before building, recheck the relevant paths at the agreed implementation pin and reconcile current generated contracts. The routed quest reference also carries historical wording on defaults and caps that must not override source evidence without reconciliation. This decision revision changes no engine law or generated contract.

Capture sources: `harvests/inbox/tnr_results_1789401726302.json` (graphs), `harvests/inbox/tnr_results_1789402842027.json` (AIs, embedded kits, rewards/backgrounds), and `harvests/inbox/tnr_results_1789403623148.json` (profiles). Discovery catalog: `harvests/seed/43_INDEX_asset.json`, August 24.

## 5. Completed and unperformed checks

Completed in this turn: live GitHub main and planning-branch identification; planning/canonical-document review; committed graph/reference inspection; documentation revision and durable scope decision. No game requests or art generation.

Local Git access failed with DNS resolution; no clone, session guards, capture-normalization run, graph-derived shotlist, graph validator, art preflight, pixel inspection, actual engine simulation, live calibration or revised game readback was completed. Shared jutsu icons/effect assets, actual summons and alternate-avatar display paths still need their bounded inventory review.

Structural direction is now approved. Detached prose/storyboard drafting, source-image recovery, reproducible graph inventory and original-art reuse trials remain execution work. Their gates are in the current plan. Reward approval, corrected manifests, active-run handling and publishing remain unfinished.
