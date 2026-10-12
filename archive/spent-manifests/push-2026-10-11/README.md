# Spent manifests — 2026-10-11

Both are archived because they have been run: `push/README.md` requires it, and the builder and Forge pickers list `push/`. Findings: `docs/reviews/GHOST_SHIP_SKYGLASS_CAPTURES_85_86_2026-10-11.md`.

## 85_skyglass_legendary_sword_baseline_capture.json — RUN, SUCCESS

Read-only Legendary Sword baseline capture for the Skyglass Katana (Stage 2 gate C3).
**Result:** `harvests/inbox/tnr_results_1791727479372.json` (Forge 0.5.0, job `85-mv3wa2l9`, `2026-10-11T14:04:38Z`), state DONE, outcome success. `item.get` x3, all ok and `persistOk`, zero mutations.
Night's Testament, Chakra Sword and Masamune are all LEGENDARY WEAPON/SWORD. Baseline selection remains with dauntless.

## 86_ghost_ship_ai_post0056_recapture.json — RUN, SUCCESS

Read-only post-migration-0056 recapture of the eleven Ghost Ship AIs.
**Result:** `harvests/inbox/tnr_results_1791727613862.json` (Forge 0.5.0, job `86-mv3wcul9`, `2026-10-11T14:06:53Z`), state DONE, outcome success. `profile.getAi` x11 and `ai.getAiProfile` x11, all ok and `persistOk`, zero mutations.
Live offence, defence and masteries exactly equal the harness's 0056 AI-branch conversion. Profiles, innate effects and jutsu membership are unchanged. Embedded jutsu rows show schema-only drift, which stales the Oct 1 protected hashes; fresh hashes are in the review. Crowned Captain loot differs from Oct 1 (no Diadem; Fragment drop 10%; Dagger and Armor drops 0%).
