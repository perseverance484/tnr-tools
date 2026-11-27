# Unmerged branch classification (origin/main@f0b5f0f, 2026-11-27)

Method: for each unmerged origin branch, diff merge-base..tip; a file is "landed" if its blob id exists anywhere in origin/main history (git rev-list --objects origin/main). "contained in" = tip is an ancestor of another unmerged branch. pre = last commit before the 2026-11-09 history rewrite (all branches were force-updated then; ids in old reviews/handoffs are pre-rewrite, see docs/reviews/HISTORY_REWRITE_2026-11-09_commit_map.txt).

Classes: A = content already on main; B = superseded/abandoned (delete, or harvest/tag first as noted); C = live work needing an owner decision.

Counts: A=17, B=215, C=38

Sub-buckets:

- A / all blobs already in main history: 1
- A / every file blob already exists in main h: 16
- B / abandoned/superseded: 72
- B / no merge base (2026-06 GitHub web upload: 1
- B / pre-Nov live-era manifests (numbers reus: 6
- B / review evidence branch-only: 70
- B / superseded: 55
- B / temp/CI scaffolding: 11
- C / Duet->Fable review: 1
- C / Duet/director: 1
- C / Fable: 2
- C / Fable/director: 7
- C / Fable/director (art direction): 1
- C / Lane B: 1
- C / Lane B thread with live-run records NOT : 7
- C / Lane B/A thread work not on main (.githu: 2
- C / Lane B/A thread work not on main (art/co: 1
- C / Lane B/A thread work not on main (art/is: 1
- C / Lane B/A thread work not on main (harnes: 1
- C / Lane B/A thread work not on main (player: 1
- C / Lane B/A thread work not on main (state/: 2
- C / Lane B/A thread work not on main (tools/: 1
- C / director: 1
- C / director (art direction): 1
- C / director/AI-player: 2
- C / director/ChatGPT: 1
- C / open PR#123: 1
- C / open PR#126: 1
- C / open PR#128: 1
- C / pilot/director: 1

| class | branch | last | ahead | landed files | unlanded files | rewrite | reason |
|---|---|---|---|---|---|---|---|
| A | ccr-9a2d53da-6kh6du | 2026-10-21 | 11 | 0 | 0 | pre | every file blob already exists in main history |
| A | chatgpt/collaboration-bootstrap | 2026-09-07 | 23 | 16 | 0 | pre | every file blob already exists in main history |
| A | chatgpt/forge-next-phase1-brief | 2026-09-17 | 1 | 1 | 0 | pre | every file blob already exists in main history |
| A | chatgpt/guide-studio-spec | 2026-09-13 | 6 | 2 | 0 | pre | every file blob already exists in main history |
| A | chatgpt/review-forge-next-phase0-integration | 2026-09-17 | 1 | 1 | 0 | pre | every file blob already exists in main history |
| A | chatgpt/review-jutsu-icon-alpha-20261016 | 2026-10-16 | 2 | 1 | 0 | pre | every file blob already exists in main history |
| A | chatgpt/review-opc-forge041-r2-20260916 | 2026-09-16 | 1 | 1 | 0 | pre | every file blob already exists in main history |
| A | chatgpt/taiyo-kami-capture-20261002 | 2026-10-02 | 3 | 1 | 0 | pre | every file blob already exists in main history |
| A | claude/one-perfect-crop-manifest-9wsry6 | 2026-09-16 | 1 | 1 | 0 | pre | every file blob already exists in main history |
| A | claude/project-thread-we4pm8 | 2026-11-27 | 2 | 4 | 0 | post | all blobs already in main history |
| A | duet/merge-live-patch-animation-scale | 2026-11-13 | 1 | 7 | 0 | post | every file blob already exists in main history |
| A | fable/badge-builder | 2026-10-29 | 1 | 1 | 0 | pre | every file blob already exists in main history |
| A | fable/branch-prune | 2026-11-08 | 1 | 1 | 0 | pre | every file blob already exists in main history |
| A | fable/large-file-guard | 2026-11-08 | 1 | 3 | 0 | pre | every file blob already exists in main history |
| A | fable/rewrite-probe | 2026-11-09 | 1 | 0 | 0 | post | every file blob already exists in main history |
| A | fable/skill-overhaul-brief | 2026-11-09 | 1 | 3 | 0 | post | every file blob already exists in main history |
| A | fable/state-refresh | 2026-11-08 | 1 | 4 | 0 | pre | every file blob already exists in main history |
| B | astra/guide-studio-staging-handoff | 2026-09-13 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | ccr-504cc1a9-bljl5m | 2026-10-20 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/aerathiel-guide-assets | 2026-09-12 | 15 | 0 | 19 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/aerathiel-jutsu-art-studio-20261019 | 2026-10-19 | 7 | 0 | 2 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/art-tempest-cleave-premium-refinement-20261024 | 2026-10-24 | 7 | 0 | 2 | pre | temp/CI scaffolding; delete |
| B | chatgpt/art-weapon-master-parity | 2026-10-06 | 8 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/ash-jutsu-prompt-desk-20261019 | 2026-10-20 | 11 | 0 | 4 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/aura-of-despair-art-lock-20261026 | 2026-10-26 | 2 | 0 | 2 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 1 |
| B | chatgpt/bakuhatsu-jutsu-art-studio-20261019 | 2026-10-20 | 53 | 1 | 11 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/bbe-final-export-closeout-20261017 | 2026-10-17 | 1 | 0 | 4 | pre | superseded: contained in chatgpt/review-bbe-final-closeout-pr41-20261017 |
| B | chatgpt/bbe-jutsu-art-studio-20261014 | 2026-10-14 | 6 | 0 | 7 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 1 |
| B | chatgpt/bbe-midnight-alloy-foundation-pilot-20261018 | 2026-10-18 | 185 | 0 | 58 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018,chatgpt/bee-bloodright-tier-studio-20261018; rulings only on branch: 3 |
| B | chatgpt/bbe-midnight-alloy-trio-20261018 | 2026-10-18 | 188 | 0 | 59 | pre | superseded: contained in chatgpt/bbe-pale-blue-source-correction-20261018,chatgpt/bee-bloodright-tier-studio-20261018,chatgpt/itojinsei-blackwire-finalization-20261018; rulings only on branch: 3 |
| B | chatgpt/bbe-pale-blue-source-correction-20261018 | 2026-10-18 | 196 | 0 | 61 | pre | superseded: contained in chatgpt/bee-bloodright-tier-studio-20261018,chatgpt/itojinsei-blackwire-finalization-20261018; rulings only on branch: 3 |
| B | chatgpt/bbe-tier-geometry-diagnosis-20261018 | 2026-10-18 | 183 | 0 | 57 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 3 |
| B | chatgpt/bee-bloodright-tier-studio-20261018 | 2026-10-18 | 205 | 0 | 64 | pre | superseded: contained in chatgpt/itojinsei-blackwire-finalization-20261018; rulings only on branch: 3 |
| B | chatgpt/bee-jutsu-art-studio-20261014 | 2026-10-17 | 79 | 0 | 11 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 2 |
| B | chatgpt/bloodline-jutsu-studio-zip-first-20261017 | 2026-10-17 | 15 | 0 | 9 | pre | superseded: contained in claude/bloodline-jutsu-icon-studio-3nmvc2 |
| B | chatgpt/bloodline-reskin-commerce-proposal-20261005 | 2026-10-05 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/bloodright-approved-original-sizepass-20261018 | 2026-10-18 | 182 | 0 | 56 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 3 |
| B | chatgpt/bloodright-factory-pilot-closeout-20261017 | 2026-10-17 | 24 | 0 | 11 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 3 |
| B | chatgpt/bloodright-icon-production-tracker-20261008 | 2026-10-08 | 6 | 0 | 3 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/bloodright-icon-studio-20261016 | 2026-10-16 | 11 | 0 | 8 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 1 |
| B | chatgpt/bloodright-pixelart-wave01-20261018 | 2026-10-18 | 175 | 0 | 55 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 3 |
| B | chatgpt/bloodright-planning-handoff-20261002 | 2026-10-02 | 4 | 0 | 13 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 2 |
| B | chatgpt/bloodright-reference-library-brief-20261016 | 2026-10-16 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/bloodright-remainder-factory-plan-20261017 | 2026-10-17 | 19 | 0 | 10 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 2 |
| B | chatgpt/bloodright-structural-priority-20261017 | 2026-10-17 | 3 | 0 | 3 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 1 |
| B | chatgpt/bloodright-wave02-art-closeout-20261017 | 2026-10-17 | 28 | 0 | 13 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 3 |
| B | chatgpt/bloodright-wave03-art-studio-20261017 | 2026-10-17 | 69 | 0 | 23 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 3 |
| B | chatgpt/bloodright-wave04-art-studio-20261017 | 2026-10-17 | 99 | 0 | 34 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 3 |
| B | chatgpt/bloodright-wave05-art-studio-20261017 | 2026-10-18 | 142 | 0 | 46 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 3 |
| B | chatgpt/bloodright-wave06-art-studio-20261018 | 2026-10-18 | 173 | 0 | 54 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 3 |
| B | chatgpt/builder-app-readiness-brief | 2026-09-08 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/crystal-essence-jutsu-art-studio-20261020 | 2026-10-21 | 54 | 0 | 20 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/elementaldamage-godstorm-capture-review-20261020 | 2026-10-20 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/elementaldamage-weapon-census-handoff-20261020 | 2026-10-20 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/ethereal-monarch-bloodright-art-qc-20261017 | 2026-10-17 | 13 | 0 | 9 | pre | superseded: contained in chatgpt/bbe-midnight-alloy-foundation-pilot-20261018,chatgpt/bbe-midnight-alloy-trio-20261018,chatgpt/bbe-pale-blue-source-correction-20261018; rulings only on branch: 1 |
| B | chatgpt/ethereal-rebirth-fox-ribbon-pass2-plan-20261024 | 2026-10-24 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/ethereal-rebirth-fox-ribbon-refinement-20261024 | 2026-10-24 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/forge-next-planning | 2026-09-12 | 32 | 6 | 20 | pre | superseded: contained in chatgpt/forge-quest-studio-final-fix,chatgpt/forge-quest-studio-foundation,chatgpt/forge-quest-studio-source-push-temp |
| B | chatgpt/forge-next-planning-workspace-temp | 2026-09-12 | 23 | 4 | 17 | pre | superseded: contained in chatgpt/forge-next-planning,chatgpt/forge-next-planning-workspace-temp2,chatgpt/forge-quest-studio-final-fix |
| B | chatgpt/forge-next-planning-workspace-temp2 | 2026-09-12 | 23 | 4 | 17 | pre | superseded: contained in chatgpt/forge-next-planning,chatgpt/forge-next-planning-workspace-temp,chatgpt/forge-quest-studio-final-fix |
| B | chatgpt/forge-next-unified-contract | 2026-09-16 | 3 | 0 | 3 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/forge-presentation-studio-design | 2026-09-19 | 1 | 0 | 5 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/forge-presentation-studio-plan | 2026-09-19 | 5 | 0 | 3 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/forge-quest-studio-final-fix | 2026-09-16 | 121 | 7 | 42 | pre | superseded: contained in chatgpt/forge-quest-studio-foundation,claude/quest-studio-final-review |
| B | chatgpt/forge-quest-studio-foundation | 2026-09-16 | 121 | 7 | 42 | pre | superseded: contained in chatgpt/forge-quest-studio-final-fix,claude/quest-studio-final-review |
| B | chatgpt/forge-quest-studio-source-push-temp | 2026-09-16 | 99 | 6 | 41 | pre | superseded: contained in chatgpt/forge-quest-studio-final-fix,chatgpt/forge-quest-studio-foundation,chatgpt/forge-quest-studio-source-push-temp2 |
| B | chatgpt/forge-quest-studio-source-push-temp2 | 2026-09-16 | 99 | 6 | 41 | pre | superseded: contained in chatgpt/forge-quest-studio-final-fix,chatgpt/forge-quest-studio-foundation,chatgpt/forge-quest-studio-source-push-temp |
| B | chatgpt/forge-quest-studio-source-push-work | 2026-09-16 | 114 | 6 | 42 | pre | superseded: contained in chatgpt/forge-quest-studio-final-fix,chatgpt/forge-quest-studio-foundation,claude/quest-studio-final-review |
| B | chatgpt/genin-battle-pyramids-plan-20261005 | 2026-10-06 | 8 | 0 | 2 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/ghost-ship-chest-icon-art-studio-20261020 | 2026-10-21 | 121 | 0 | 24 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 1 |
| B | chatgpt/ghost-ship-skyglass-art-20261001 | 2026-10-01 | 8 | 0 | 19 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 8 |
| B | chatgpt/godstorm-art-recovery | 2026-09-15 | 17 | 0 | 28 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 3 |
| B | chatgpt/godstorm-pyramid-final-audit | 2026-09-14 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/godstorm-pyramid-readiness | 2026-09-14 | 2 | 1 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/godstorm-source-art-pack | 2026-09-15 | 14 | 0 | 28 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 3 |
| B | chatgpt/godstorm-two-pyramid-plan | 2026-09-19 | 37 | 5 | 13 | pre | pre-Nov live-era manifests (numbers reused on main): 48_godstorm_current_manifest 49_godstorm_two_pyramid_final_update 50_godstorm_tw; archive tag then delete; rulings only on branch: 4 |
| B | chatgpt/godstorm-two-pyramid-release-plan-20260915 | 2026-09-15 | 2 | 0 | 2 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 1 |
| B | chatgpt/hellfire-harvest-art-approval-20261026 | 2026-10-26 | 2 | 0 | 2 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 1 |
| B | chatgpt/horizontal-item-progression-acquisition-20261004 | 2026-10-04 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/houkyuken-jutsu-art-studio-20261016 | 2026-10-16 | 27 | 0 | 12 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 3 |
| B | chatgpt/itojinsei-blackwire-finalization-20261018 | 2026-10-18 | 216 | 0 | 69 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 3 |
| B | chatgpt/jellyfish-beach-quest-20261004 | 2026-10-04 | 11 | 0 | 5 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/living-lineages-kitsune-workdesk-20261020 | 2026-10-20 | 70 | 0 | 21 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 5 |
| B | chatgpt/master-asset-processing-handoff-20261020 | 2026-10-20 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/night-parade-official-pack | 2026-09-12 | 2 | 0 | 2 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/one-perfect-crop-art-refs-20260911 | 2026-09-11 | 2 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/one-perfect-crop-scene-characters-20260923 | 2026-09-23 | 6 | 0 | 5 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/opc-art-final-validation-20260927 | 2026-09-27 | 1 | 0 | 1 | pre | temp/CI scaffolding; delete |
| B | chatgpt/opc-art-final-validation2-20260927 | 2026-09-27 | 1 | 0 | 1 | pre | temp/CI scaffolding; delete |
| B | chatgpt/opc-art-final-validation3-20260927 | 2026-09-27 | 1 | 0 | 1 | pre | temp/CI scaffolding; delete |
| B | chatgpt/opc-asset-repair-ci-20260929 | 2026-09-29 | 2 | 0 | 1 | pre | temp/CI scaffolding; delete |
| B | chatgpt/opc-launch-final-integration-check-20260928 | 2026-09-28 | 1 | 0 | 1 | pre | temp/CI scaffolding; delete |
| B | chatgpt/opc-launch-finalization-20260924 | 2026-09-27 | 2 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/opc-launch-finalization-ci-20260926 | 2026-09-27 | 7 | 0 | 1 | pre | temp/CI scaffolding; delete |
| B | chatgpt/opc-partial-failure-repair-brief-20260928 | 2026-09-28 | 4 | 0 | 4 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/opc-render-final-20260927 | 2026-09-27 | 2 | 2 | 1 | pre | temp/CI scaffolding; delete |
| B | chatgpt/opc-scene-asset-stage-20260927 | 2026-09-27 | 23 | 2 | 19 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/opc-scene-finalize-gen-20260927 | 2026-09-27 | 2 | 1 | 1 | pre | temp/CI scaffolding; delete |
| B | chatgpt/opc-scene-finalize-gen2-20260927 | 2026-09-27 | 2 | 1 | 1 | pre | temp/CI scaffolding; delete |
| B | chatgpt/potency-chakra-mandala-design-20260929 | 2026-09-29 | 6 | 0 | 12 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 3 |
| B | chatgpt/premium-pet-visual-prompt-proposal-20261020 | 2026-10-20 | 9 | 0 | 5 | pre | superseded: contained in chatgpt/living-lineages-kitsune-workdesk-20261020 |
| B | chatgpt/quest-workflow-skyglass-retrospective-20261012 | 2026-10-12 | 5 | 0 | 4 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 1 |
| B | chatgpt/qw0a-continuation-brief-20261014 | 2026-10-14 | 2 | 0 | 3 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/qw1-integration-checkpoint-20261014 | 2026-10-13 | 1 | 0 | 2 | pre | superseded: contained in chatgpt/qw0a-continuation-brief-20261014 |
| B | chatgpt/recipe-aligned-reward-caches-20261016 | 2026-10-16 | 9 | 0 | 5 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 1 |
| B | chatgpt/review-ai-player-ap1 | 2026-11-11 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-correction | 2026-11-11 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-live-rulings | 2026-11-11 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview10 | 2026-11-12 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview11-lane-a | 2026-11-12 | 1 | 0 | 4 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview12-lane-a | 2026-11-12 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview13-lane-a | 2026-11-12 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview2 | 2026-11-11 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview3 | 2026-11-11 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview4 | 2026-11-11 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview5 | 2026-11-11 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview6 | 2026-11-12 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview7 | 2026-11-12 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview8 | 2026-11-12 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview9 | 2026-11-12 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap1-rereview9-lane-a | 2026-11-12 | 1 | 0 | 6 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap2 | 2026-11-13 | 1 | 0 | 3 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap2-rereview1 | 2026-11-13 | 1 | 0 | 7 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-ap2-rereview2 | 2026-11-13 | 1 | 0 | 5 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-brain-split | 2026-11-12 | 1 | 0 | 3 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-hook-relay | 2026-11-13 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-hook-relay-rereview1 | 2026-11-13 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-hook-relay-rereview2 | 2026-11-13 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-hook-relay-rereview3 | 2026-11-13 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-preflight-rereview1-20261116 | 2026-11-15 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-preflight-rereview2-20261116 | 2026-11-15 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-preflight-rereview3-20261116 | 2026-11-15 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-relay-preflight-20261114 | 2026-11-13 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-relay-refusal-20261114 | 2026-11-14 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-relay-refusal-rereview1-20261115 | 2026-11-15 | 1 | 0 | 1 | post | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-ai-player-run2-followup-20261117 | 2026-11-17 | 10 | 0 | 30 | post | review evidence branch-only: harvest docs/reviews files to main, then delete; rulings only on branch: 1 |
| B | chatgpt/review-art-generation-preflight | 2026-09-11 | 7 | 0 | 15 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-bbe-final-closeout-pr41-20261017 | 2026-10-17 | 3 | 0 | 5 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-builder-app-4062268 | 2026-09-07 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-builder-app-readiness-5ffb735 | 2026-09-08 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-builder-app-readiness-c388ea6 | 2026-09-08 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-content-workstream-bootstrap | 2026-09-11 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-content-workstream-bootstrap-r2 | 2026-09-11 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-elementaldamage-census-round2-20261020 | 2026-10-20 | 4 | 1 | 28 | pre | pre-Nov live-era manifests (numbers reused on main): 132_elementaldamage_weapon_census ; archive tag then delete; rulings only on branch: 1 |
| B | chatgpt/review-elementaldamage-census-round3-20261020 | 2026-10-20 | 5 | 1 | 28 | pre | pre-Nov live-era manifests (numbers reused on main): 132_elementaldamage_weapon_census ; archive tag then delete; rulings only on branch: 1 |
| B | chatgpt/review-elementaldamage-weapon-census-20261020 | 2026-10-20 | 3 | 1 | 28 | pre | pre-Nov live-era manifests (numbers reused on main): 132_elementaldamage_weapon_census ; archive tag then delete; rulings only on branch: 1 |
| B | chatgpt/review-forge-carrier-disappears | 2026-09-12 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-full-capture | 2026-09-10 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-full-capture-r2 | 2026-09-10 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-next-phase0 | 2026-09-17 | 2 | 0 | 2 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-next-phase0-final | 2026-09-17 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-next-planning | 2026-09-13 | 48 | 2 | 68 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-next-planning-r2 | 2026-09-15 | 52 | 7 | 65 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-presentation-studio-p1 | 2026-09-19 | 1 | 0 | 4 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-presentation-studio-p1-r2 | 2026-09-19 | 1 | 0 | 4 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-presentation-studio-p1-r3 | 2026-09-19 | 1 | 0 | 4 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-protected-auth | 2026-09-10 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-protected-auth-r2 | 2026-09-10 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-forge-protected-auth-r3 | 2026-09-10 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-godstorm-forge-defects-repair | 2026-09-19 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-jutsu-art-20261005 | 2026-10-05 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-jutsu-art-corrections-20261006 | 2026-10-06 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-jutsu-icon-p1-20261019 | 2026-10-19 | 3 | 0 | 3 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-opc-core-manifest-20260916 | 2026-09-16 | 2 | 0 | 2 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-pr76-integration-20261020 | 2026-10-20 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-pr76-round2-20261020 | 2026-10-20 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-qw0a-extractor-20261014 | 2026-10-14 | 2 | 0 | 31 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-qw0a-extractor-corrections-20261014 | 2026-10-14 | 3 | 0 | 34 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-qw1-workstream-starter-20261012 | 2026-10-12 | 1 | 2 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-repo-backed-image-packs | 2026-09-19 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-repo-backed-image-packs-correction1 | 2026-09-19 | 1 | 0 | 1 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-resort-in-need-20261013 | 2026-10-13 | 9 | 0 | 2 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | chatgpt/review-silent-bastion-authoring-20261016 | 2026-10-16 | 70 | 13 | 124 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete; rulings only on branch: 15 |
| B | chatgpt/review-silent-bastion-authoring-r2-20261017 | 2026-10-17 | 70 | 19 | 123 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete; rulings only on branch: 15 |
| B | chatgpt/review-silent-bastion-c99-20261016 | 2026-10-16 | 42 | 3 | 82 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete; rulings only on branch: 2 |
| B | chatgpt/shinseina-ki-jutsu-art-studio-20261019 | 2026-10-19 | 18 | 0 | 5 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/silent-bastion-alt99-approval-20261016 | 2026-10-16 | 45 | 3 | 81 | pre | superseded: contained in chatgpt/review-silent-bastion-authoring-20261016,chatgpt/review-silent-bastion-authoring-r2-20261017,chatgpt/silent-bastion-caches-claude-handoff-20261016; rulings only on branch: 3 |
| B | chatgpt/silent-bastion-caches-claude-handoff-20261016 | 2026-10-16 | 63 | 3 | 88 | pre | superseded: contained in chatgpt/review-silent-bastion-authoring-20261016,chatgpt/review-silent-bastion-authoring-r2-20261017,claude/recipe-cache-native-proof-69za5u; rulings only on branch: 5 |
| B | chatgpt/silent-bastion-content-execution-plan-20261014 | 2026-10-14 | 25 | 1 | 31 | pre | superseded: contained in chatgpt/review-silent-bastion-authoring-20261016,chatgpt/review-silent-bastion-authoring-r2-20261017,chatgpt/review-silent-bastion-c99-20261016; rulings only on branch: 1 |
| B | chatgpt/silent-bastion-design-20261013 | 2026-10-13 | 20 | 0 | 7 | pre | superseded: contained in chatgpt/review-silent-bastion-authoring-20261016,chatgpt/review-silent-bastion-authoring-r2-20261017,chatgpt/review-silent-bastion-c99-20261016 |
| B | chatgpt/silent-bastion-node-budget-20261015 | 2026-10-15 | 38 | 1 | 35 | pre | superseded: contained in chatgpt/review-silent-bastion-authoring-20261016,chatgpt/review-silent-bastion-authoring-r2-20261017,chatgpt/review-silent-bastion-c99-20261016; rulings only on branch: 2 |
| B | chatgpt/tag-design-audit | 2026-09-20 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/task-first-restructure | 2026-10-06 | 1 | 7 | 67 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | chatgpt/vaporia-jutsu-art-studio-20261015 | 2026-10-16 | 19 | 0 | 14 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 2 |
| B | claude/ai-jutsu-reequip-validation-7ywxag | 2026-10-09 | 1 | 1 | 6 | pre | temp/CI scaffolding; delete |
| B | claude/art-generation-preflight-sq6j3n | 2026-09-11 | 6 | 0 | 14 | pre | superseded: contained in chatgpt/review-art-generation-preflight,fable/art-generation-preflight |
| B | claude/bloodline-jutsu-icon-studio-3nmvc2 | 2026-10-17 | 17 | 19 | 14 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | claude/builder-app-production-readiness-kelsib | 2026-09-09 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | claude/crafting-recipe-census-pln5za | 2026-10-13 | 23 | 8 | 26 | pre | pre-Nov live-era manifests (numbers reused on main): 99_crafting_caches_release ; archive tag then delete; rulings only on branch: 4 |
| B | claude/elemental-damage-weapon-census-235ynv | 2026-10-20 | 4 | 1 | 27 | pre | superseded: contained in chatgpt/review-elementaldamage-census-round3-20261020; rulings only on branch: 1 |
| B | claude/forge-next-phase1-uwhcn1 | 2026-09-30 | 16 | 0 | 36 | pre | superseded: contained in fable/forge-next-phase1 |
| B | claude/forge-next-planning-reconciled | 2026-09-17 | 52 | 10 | 61 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | claude/forge-next-planning-v3frzi | 2026-09-14 | 51 | 7 | 64 | pre | superseded: contained in chatgpt/review-forge-next-planning-r2,claude/forge-next-planning-reconciled |
| B | claude/forge-quest-studio-audit-j4jhcf | 2026-09-13 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | claude/handoff-format-standard | 2026-09-17 | 1 | 0 | 2 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | claude/quest-studio-final-review | 2026-09-17 | 122 | 8 | 42 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | claude/quest-studio-source-push-review | 2026-09-16 | 115 | 6 | 43 | pre | review evidence branch-only: harvest docs/reviews files to main, then delete |
| B | claude/recipe-cache-native-proof-69za5u | 2026-10-16 | 64 | 4 | 108 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 5 |
| B | claude/silent-bastion-authoring-69za5u | 2026-10-17 | 69 | 19 | 122 | pre | superseded: contained in chatgpt/review-silent-bastion-authoring-r2-20261017; rulings only on branch: 15 |
| B | claude/silent-bastion-budget-validation-69za5u | 2026-10-16 | 41 | 3 | 81 | pre | superseded: contained in chatgpt/review-silent-bastion-authoring-20261016,chatgpt/review-silent-bastion-authoring-r2-20261017,chatgpt/review-silent-bastion-c99-20261016; rulings only on branch: 2 |
| B | claude/silent-bastion-phase1-validation-9628h6 | 2026-10-14 | 24 | 1 | 30 | pre | superseded: contained in chatgpt/review-silent-bastion-authoring-20261016,chatgpt/review-silent-bastion-authoring-r2-20261017,chatgpt/review-silent-bastion-c99-20261016; rulings only on branch: 1 |
| B | claude/tnr-content-tickets-tcbi34 | 2026-10-21 | 4 | 0 | 6 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | client-contract-audit | 2026-09-03 | 1 | 0 | 2 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | client-contract-verification | 2026-09-03 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | content-146-frost-warden-direct | 2026-10-20 | 1 | 2 | 4 | pre | pre-Nov live-era manifests (numbers reused on main): 146_frost_warden_unequip 147_frost_warden_reequip_rank ; archive tag then delete |
| B | fable/ai-player-light-polls | 2026-11-13 | 3 | 0 | 13 | post | superseded: light reads dropped by RUL-2026-11-14-158 (on main) |
| B | fable/art-generation-preflight | 2026-09-11 | 6 | 0 | 14 | pre | superseded: contained in chatgpt/review-art-generation-preflight,claude/art-generation-preflight-sq6j3n |
| B | fable/bloodright-planning-20261003 | 2026-10-05 | 67 | 44 | 259 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 5 |
| B | fable/bloodright-reference-library-20261016 | 2026-10-17 | 7 | 0 | 7 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | fable/combat-fx-design-rules | 2026-11-17 | 2 | 0 | 6 | post | superseded: contained in fable/art-skill-duelyst; rulings only on branch: 1 |
| B | fable/contracts-107d7a8 | 2026-10-22 | 6 | 0 | 29 | pre | abandoned/superseded; harvest unique docs if wanted, then delete; rulings only on branch: 1 |
| B | fable/crowned-captain-sim | 2026-10-28 | 14 | 2 | 95 | pre | superseded: contained in fable/mother-of-echoes-act3,fable/mother-of-echoes-sim,fable/skyglass-final-sim |
| B | fable/duelyst-kit | 2026-11-18 | 6 | 0 | 6 | post | superseded: contained in fable/art-skill-duelyst |
| B | fable/forge-bundle-rebuild | 2026-11-08 | 2 | 2 | 1 | pre | superseded: RUL-2026-11-08-136 on main; only RULINGS.md text differs |
| B | fable/forge-next-phase1 | 2026-09-30 | 16 | 0 | 36 | pre | superseded: contained in claude/forge-next-phase1-uwhcn1 |
| B | fable/forge-suggest-create | 2026-10-25 | 1 | 0 | 11 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | fable/forge-suggest-scope-20261019 | 2026-10-19 | 1 | 0 | 1 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | fable/mother-of-echoes-act3 | 2026-11-05 | 108 | 10 | 653 | pre | superseded: contained in fable/mother-of-echoes-sim |
| B | fable/pixel-art-snap | 2026-10-24 | 3 | 0 | 5 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | fable/qw0a-extractor-fidelity-20261014 | 2026-10-14 | 3 | 0 | 29 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | fable/rulings-split | 2026-11-08 | 1 | 7 | 2 | pre | superseded: ledger split landed on main differently (docs/rulings/*.md + index) |
| B | fable/skyglass-art-bible-v04 | 2026-10-26 | 2 | 0 | 8 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | fable/skyglass-charts-sim | 2026-10-28 | 14 | 0 | 107 | pre | superseded: contained in fable/mother-of-echoes-act3,fable/mother-of-echoes-sim,fable/skyglass-final-sim |
| B | fable/skyglass-final-sim | 2026-10-30 | 54 | 6 | 162 | pre | superseded: contained in fable/mother-of-echoes-act3,fable/mother-of-echoes-sim,fable/skyglass-haul-fit |
| B | fable/skyglass-haul-fit | 2026-10-30 | 55 | 6 | 176 | pre | superseded: contained in fable/mother-of-echoes-act3,fable/mother-of-echoes-sim,fable/skyglass-kite-sim |
| B | fable/skyglass-haul-sim | 2026-10-29 | 25 | 0 | 121 | pre | superseded: contained in fable/mother-of-echoes-act3,fable/mother-of-echoes-sim,fable/skyglass-final-sim |
| B | fable/skyglass-hunts-sim | 2026-10-28 | 11 | 1 | 91 | pre | superseded: contained in fable/mother-of-echoes-act3,fable/mother-of-echoes-sim,fable/skyglass-final-sim |
| B | fable/skyglass-kite-sim | 2026-10-31 | 76 | 10 | 280 | pre | superseded: contained in fable/mother-of-echoes-act3,fable/mother-of-echoes-sim |
| B | fable/skyglass-wreck-sim | 2026-10-29 | 17 | 1 | 86 | pre | superseded: contained in fable/mother-of-echoes-act3,fable/mother-of-echoes-sim,fable/skyglass-final-sim |
| B | fable/validate-stale-rules | 2026-10-26 | 2 | 3 | 18 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | law-provenance | 2026-09-03 | 3 | 0 | 3 | pre | abandoned/superseded; harvest unique docs if wanted, then delete |
| B | perseverance484-patch-1 | 2026-06-30 | 11 | - | - | post | no merge base (2026-06 GitHub web upload); delete |
| C | ccr-8d5810e2-036hwx | 2026-11-17 | 3 | 0 | 3 | post | Lane B: push/627 Skyglass charts results 14/14 VERIFIED; 627 collides with main 627_white_tiger |
| C | chatgpt/ap6-simplification-clarification | 2026-11-12 | 1 | 0 | 4 | post | director/ChatGPT: AP6 ruling recorded only here as RUL-2026-11-12-153, which collides with main RUL-153 (ryo cap); rulings only on branch: 1 |
| C | chatgpt/premium-seichi-item-icon-overhaul-v10 | 2026-11-03 | 15 | 0 | 11 | pre | director (art direction): Premium Seichi V10.1 benchmark ruling only here as RUL-2026-11-03-111, collides with main RUL-111; rulings only on branch: 1 |
| C | claude/ap-live-run-dauntless-goqgbz | 2026-11-16 | 24 | 42 | 43 | post | Fable/director: AP live run logs + ops/ap_model_session |
| C | claude/project-thread-0vuxzt | 2026-11-23 | 3 | 0 | 28 | post | Lane B/A thread work not on main (player/tests(10);player/activities(7);data/player_allowlist.json(1);player/brain(1);player/calls.py() |
| C | claude/project-thread-3u4iz4 | 2026-11-23 | 4 | 0 | 3 | post | Lane B/A thread work not on main (harness/pvp_turn(3)) |
| C | claude/project-thread-6ojemy | 2026-11-20 | 1 | 0 | 9 | post | Lane B thread with live-run records NOT on main: harvest bundles=1, manifests: 690_shore_crew 691_short_rations_shore  |
| C | claude/project-thread-9c4sh9 | 2026-11-20 | 6 | 0 | 542 | post | Lane B/A thread work not on main (art/isonade_styleC(532);state/isonade_c_upload(7);.github/scripts(1);.github/workflows(1);state/run_) |
| C | claude/project-thread-bkn9aw | 2026-11-27 | 7 | 0 | 11 | post | Lane B thread with live-run records NOT on main: harvest bundles=1, manifests: 631_gobblefather_art_rewards_ut  |
| C | claude/project-thread-bqrptw | 2026-11-19 | 3 | 0 | 3 | post | Fable: repo copy of designing-tnr-pve-encounters skill (installed skill not in repo main) |
| C | claude/project-thread-bxzz52 | 2026-11-18 | 2 | 0 | 9 | post | Lane B thread with live-run records NOT on main: harvest bundles=2, manifests: 640_residual_modifier_fix 641_residual_modifier_fix_bloodline  |
| C | claude/project-thread-e98p9m | 2026-11-23 | 1 | 1 | 3 | post | Lane B/A thread work not on main (state/player(3)) |
| C | claude/project-thread-f0jjus | 2026-11-26 | 1 | 0 | 4 | post | Lane B thread with live-run records NOT on main: harvest bundles=0, manifests: 631_weapon_effect_targets  |
| C | claude/project-thread-f2r8sb | 2026-11-19 | 3 | 0 | 75 | post | open PR#128; review/merge via PR |
| C | claude/project-thread-fuqtpo | 2026-11-22 | 3 | 62 | 141 | post | Lane B/A thread work not on main (art/consumables_upgrade(140);.github/workflows(1)) |
| C | claude/project-thread-g9d6ix | 2026-11-18 | 1 | 0 | 13 | post | Lane B thread with live-run records NOT on main: harvest bundles=5, manifests: 660_genin_dungeon_pass_jutsu 661_genin_dungeon_rogues 662_genin_dungeon_reinforcements 663_genin_dungeon_captain 664_gen |
| C | claude/project-thread-gcsyem | 2026-11-21 | 4 | 1 | 39 | post | Lane B/A thread work not on main (state/nettle_nova_upload(24);state/nettle_nova_ship(12);.github/scripts(1);.github/workflows(1);stat) |
| C | claude/project-thread-hlg3nc | 2026-11-21 | 101 | 1 | 344 | post | Lane B thread with live-run records NOT on main: harvest bundles=40, manifests: 631_flooded_stores_stage1 632_flooded_stores_stage2 633_flooded_stores_stage3 634_flooded_stores_stage4 635_flooded_stor |
| C | claude/project-thread-kbi6r8 | 2026-11-18 | 7 | 11 | 3 | post | Lane B/A thread work not on main (.github/scripts(1);.github/workflows(1);state/rengoku_upload(1)) |
| C | claude/project-thread-kinzit | 2026-11-27 | 12 | 0 | 11 | post | Lane B/A thread work not on main (tools/fight-alert(9);.github/workflows(2)) |
| C | claude/project-thread-ua0lgy | 2026-11-21 | 5 | 1 | 15 | post | Lane B thread with live-run records NOT on main: harvest bundles=1, manifests: rc335_A2_create_caches_ut rc335_A_create_caches_ut rc335_B_unhide  |
| C | claude/project-thread-un0ofw | 2026-11-18 | 6 | 1 | 5 | post | Lane B/A thread work not on main (.github/workflows(2);.github/scripts(1);state/recut_upload(1);state/whitetiger_upload(1)) |
| C | claude/quest-cleanup-2026-11-07 | 2026-11-07 | 1 | 0 | 1 | pre | director: results bundle for live quest DELETES 2026-11-07 - must land in harvests/inbox per CLAUDE.md s6 |
| C | claude/skyglass-update-6b5pk3 | 2026-11-17 | 5 | 0 | 14 | post | open PR#126; review/merge via PR |
| C | duet/ai-player-ap1-live | 2026-11-11 | 1 | 0 | 4 | post | director/AI-player: AP1 live session log (state/player) only on branch |
| C | duet/ai-player-ap1-live2 | 2026-11-12 | 3 | 9 | 125 | post | director/AI-player: AP1 live test 2 report + 112 opponent kits/logs |
| C | duet/forge-mcp-fixes | 2026-11-08 | 4 | 0 | 8 | pre | Duet->Fable review: forge @jutsu-ref-in-AI-rules fix + mcp_run resend/skip; runner._rules on main still sends unresolved rules |
| C | duet/moe-uploadthing | 2026-11-16 | 55 | 956 | 227 | post | Duet/director: MoE art upload records (227 files incl. state/moe_upload) + 4 forge/src fixes not on main; push 509-512 collide with main numbering |
| C | fable/ai-player-ap4 | 2026-11-17 | 18 | 0 | 39 | post | Fable/director: AP4 move atlas, step 0 + handoff (39 files); rulings only on branch: 2 |
| C | fable/ai-player-run2-followup | 2026-11-17 | 14 | 0 | 36 | post | Fable/director: AP run-2 correction; 5 commits not in AP4; planner part landed via #125; rulings only on branch: 1 |
| C | fable/art-skill-duelyst | 2026-11-19 | 12 | 0 | 16 | post | Fable/director (art direction): producing-tnr-art Duelyst redesign; contains duelyst-kit and combat-fx-design-rules; rulings only on branch: 1 |
| C | fable/ci-repair-20261114 | 2026-11-14 | 3 | 3 | 24 | post | open PR#123; review/merge via PR |
| C | fable/early-game-sim | 2026-11-04 | 5 | 0 | 13 | pre | Fable/director: early-game levelling design docs (13 files); rulings only on branch: 1 |
| C | fable/mother-of-echoes-sim | 2026-11-06 | 115 | 10 | 735 | pre | Fable/director: 58 MB Skyglass+MoE sim harness and reports (tip of 10-branch chain); MoE shipped on main (597) without harness |
| C | fable/pilot-planner-fixes | 2026-11-11 | 3 | 17 | 66 | post | pilot/director: 2026-11-11 pilot session logs, post-mortems, opponent kits |
| C | fable/skill-overhaul-p2 | 2026-11-10 | 3 | 0 | 22 | post | Fable: designing-tnr-content P2 libraries; not on main |
| C | fable/skyglass-economy-model | 2026-11-02 | 2 | 0 | 19 | pre | Fable/director: economy model for RUL-2026-11-02-104/105 (19 files) |
| C | fable/skyglass-rule-cap | 2026-10-31 | 76 | 21 | 263 | pre | Fable/director: 1 commit not in MoE tip (RUL-2026-10-31-077 measurements) |


## Chains (only the tip needs a decision)

- fable/mother-of-echoes-sim contains: skyglass-wreck-sim, skyglass-haul-sim, skyglass-final-sim, skyglass-haul-fit, skyglass-kite-sim, crowned-captain-sim, skyglass-charts-sim, skyglass-hunts-sim, mother-of-echoes-act3. Not contained: skyglass-rule-cap (1 unique commit), skyglass-economy-model (independent).
- chatgpt/itojinsei-blackwire-finalization-20261018 contains 16 Bloodright/BBE art-studio branches (wave02..wave06, factory, sizepass, midnight-alloy, pale-blue, tier-studio, icon-studio, ethereal-monarch QC). Not contained: bee-jutsu-art-studio, bloodright-pixelart-wave01 (2), bloodline-jutsu-studio-zip-first, vaporia, houkyuken, bbe-jutsu-art-studio.
- fable/art-skill-duelyst contains fable/duelyst-kit and fable/combat-fx-design-rules.
- claude/silent-bastion-authoring-69za5u contains budget-validation and phase1-validation; recipe-cache-native-proof has 1 unique commit.
- claude/forge-next-phase1-uwhcn1 contains fable/forge-next-phase1; claude/art-generation-preflight-sq6j3n contains fable/art-generation-preflight.
- Full containment list: notes/contained.tsv (52 branches contained in another unmerged branch).

## Live-run records that exist only on branches

See notes/live_unlanded.tsv. main state/run_queue.json ends at job 632; branches hold manifests/results for 640-698 (Genin dungeon 660-664, Shore crew 690/691, residual modifier 640/641, Flooded/Stolen Stores 631-676/697 in its own numbering, rc335, Gobblefather UT, Isonade style C 683/684, Nettle Nova 698), plus claude/quest-cleanup-2026-11-07 (results bundle for live quest deletes). Push-number collisions: hlg3nc uses 631/632/640/641 (main 631/632 = Gobblefather; bxzz52 also uses 640/641); ccr-8d5810e2 uses 627 (main 627 = white tiger); duet/moe-uploadthing uses 509-512 (main 509 = skyglass thread).

## Ruling entries only on branches

notes/stranded_rulings_dedup.md: 66 distinct ruling headings (by id + title prefix) present on unmerged branches and absent from main docs/rulings; 12 reuse an id that main assigns to a different ruling. Example dangling reference: main docs/rulings/2026-10.md:2211 says it supersedes RUL-2026-10-16-010, an entry that exists only on chatgpt/review-silent-bastion-authoring-* branches. Heuristic: a reworded title on main would be a false positive; spot-check before acting.

## Review evidence only on branches

notes/review_docs_unlanded.txt: 112 docs/reviews paths (about 4.8 MB incl. evidence scripts) from 73 review branches are not in main history. Their paired *_HANDOFF.md files are on main (e.g. AI_PLAYER_AP1_REREVIEW*_HANDOFF.md), the *_REVIEW.md verdicts are not.

## Proposed standing branch-lifecycle rule (for DEVELOPMENT_WORKFLOW.md s17; needs director approval)

1. Names: `fable/<topic>`, `chatgpt/<topic>`, `chatgpt/review-<topic>-rN`, `duet/<topic>`, `coord/<topic>`. Session-generated names (`claude/project-thread-*`, `ccr-*`, `claude/*-xxxxxx`) are allowed only as throwaway session branches and must merge or die within 7 days.
2. Records never live only on a branch: results bundles (harvests/inbox), run_queue rows, push manifests that ran, and ruling entries land on main in the same session that produced them (OPERATING_MODEL s2 already says the runner commits these). Numbers (push/NNN, RUL ids) are reserved on main first.
3. Reviews land on main: `chatgpt/review-*` branches touch only docs/reviews/** and merge to main (fast path, no Lane A cycle); the branch is deleted on merge. The frozen SHA stays the audit target; the review file cites it.
4. GitHub setting: delete_branch_on_merge = true (currently false per `gh api repos/perseverance484/tnr-tools`).
5. TTL, enforced by a scheduled read-only report workflow that opens one issue/PR listing: merged branches (delete immediately), review branches >14 days, any other unmerged branch idle >30 days (owner: merge, archive as tag `archive/<branch>`, or delete). `builder-app` and branches named in an open audit are exempt.
6. Archive form: a lightweight tag `archive/<branch>` for anything with unique evidence not worth merging (keeps commits reachable, removes it from the branch list).
