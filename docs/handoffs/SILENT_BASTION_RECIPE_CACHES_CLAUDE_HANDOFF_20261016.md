# Silent Bastion + Recipe-Aligned Caches — Claude Code handoff / ChatGPT closeout

**Status:** DIRECTOR-APPROVED DESIGN ALIGNMENT COMPLETE; OFFLINE IMPLEMENTATION/PROOF NEXT. This is not a production or publication handoff.

## Frozen input refs

| Field | Exact value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Main at preparation | `99e86dc549b86f1f4a5846c0e509fa6bc15b3463` |
| Bastion approved source | `chatgpt/silent-bastion-alt99-approval-20261016@c54a96883113979223d7989c1080ae25a480337e` |
| Cache approved source | `chatgpt/recipe-aligned-reward-caches-20261016@fb744e713873a99812b7c6e9ec8631769ef9ff9a` |
| Frozen Fable structural proof | `claude/silent-bastion-budget-validation-69za5u@74eeb328f05d4258056b0a1c531619ffcf852ce3` |
| Native graph tested against | `studie-tech/TheNinjaRPG@13d40c4c1509ecf44262aba1b5120266011ea786` |
| Later game source at preparation | `studie-tech/TheNinjaRPG@0651b039a466516a8fe24fc13b56f60dea11b7eb` |
| Integrated authoring handoff branch | `chatgpt/silent-bastion-caches-claude-handoff-20261016` (verify exact remote HEAD; delivery message provides freeze SHA) |
| Build contract | `state/prompt_silent_bastion_complete_authoring.md` — **rewritten to current four-division scope** |
| Immutable graph + hash pointer | `state/silent_bastion_approved_authoring_lock.json` → `harness/silent_bastion_condensed99/graphs/alt99_f4gate.json` |
| Separate reward proof contract | `docs/handoffs/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_PROOF_BRIEF_20261016.md` |
| Supporting reward design | `docs/design/RECIPE_ALIGNED_REWARD_CACHES_DISCOVERY_20261016.md`; `docs/design/RECIPE_ALIGNED_CACHE_PILOT_REVIEW_20261016.md`; `docs/design/RECIPE_ALIGNED_CACHE_CANDIDATE_POOLS_20261016.json` |

**Imported reward files:** The four reward source docs/JSON above were copied **byte-identically** from the reward-design frozen SHA into the integrated Bastion-based branch, then only their **current joint approval/B1 status** was annotated. Source IDs, recipe formulas, candidate weight tables and ingredient quantities were not finalized or rewritten. The reward `RUL-2026-10-16-001` was brought into the consolidated Rulings ledger, keeping the previously approved `RUL-2026-10-16-002`; `RUL-2026-10-16-003` records director acceptance of Beacon-at-start (supersedes first-fight wording).

## Current locked direction

- **Exactly 99 nodes**, native-tested `alt99_f4gate`; historical `state/silent_bastion_condensed99_candidate.json` FAILS C1 and **must not** be used as the authoring graph. Graph's embedded `directorApproval:NOT_SELECTED` is frozen *pre-decision* fixture metadata; RUL-002 and coordination lock are the current approval evidence.
- Four interior divisions: Experimental Armory, Skyglass Research, High Command, Command Sanctum; **no exterior garrison or Gatewarden**. 16 regular + 4 commander encounter slots, four three-choice terminal puzzles, 16–20 successful-route fights, 99 objective records and four player-facing floors (stable symbolic D2–D5 IDs).
- Medical Protocol sets boss-start HP/CP/SP **100%**, Combat Protocol gives **player-side** buff, Maintenance correct skips optional REG4 and wrong skips it with **player-side** alert. 50% replay on same-division loss; Arakane defeat hard-fails.
- **B1 CLOSED:** consume one Skyglass Signal Beacon **when the expedition starts**, never refunded (even before first battle), once per attempt and no additional charge on division retry. Refuse `startQuest` without Beacon. Player must be told before confirming entry.
- Completion grants a choice of **exactly one Bastion Arsenal Cache OR Bastion Research Cache**, offered at **quest-level** `rewardMode:"choose"`, `rewardPickCount:1` and `content.reward.reward_items`; neither cache belongs on `w.complete.reward_items`. Native Weighted Cache bundled single-recipe outcomes require a distinct post-claim item `noncombatconsumereward` effect and an offline feature-composition proof. This approval is category/pick policy only, not recipe acceptance.

## Fable single-session assignment (two own branches)

1. **Authoring branch:** from this integrated ChatGPT handoff head, complete the `state/prompt_silent_bastion_complete_authoring.md` scope: all 16 regular AI candidates, four complete commander profiles/kits, 4 puzzles, all 99 objective payloads, story, protocols, Beacon copy, art shotlist, candidate stats/economics, reproducible offline generator, validation and a director decision docket. Use **selected `alt99_f4gate` only**, preserve frozen proof source.
2. **Separate native reward proof branch:** run the full `docs/handoffs/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_PROOF_BRIEF_20261016.md` against a pinned current source using synthetic example ingredients/cache items. Prove one-of-two post-Pyramid claim, no direct dual reward or mid-run grant, weighted tier→single coherent entry opening, requestId receipt/idempotency, restart/failure isolation, and approved Beacon-at-start semantics. Keep technical proof branch separate until ChatGPT frozen-SHA review.
3. Return **two frozen exact SHAs** and reports/evidence, not a combined unreviewed push bundle. ChatGPT independently reviews both, director decides open values and release. Neither agent executes a game action.

## Open / blockers

- **NOT settled:** exact recipe list/yields/fractions/probabilities/roll counts, item rarity/tradability/art, Beacon drop source/rarity/rate, regular/commander numerical balance, Grand Marshal candidate AI, Arakane ultimate name/exact schema/stealth-counter reliability.
- **Arakane Combat Protocol:** desired `clearprevent` does not pass current quest-start buff whitelist; source-supported replacement requires director approval; mock `debuffprevent` is **not** automatically accepted.
- **F3:** XP/ryo can repeat through intentional recovery farming; report scenarios and seek director ruling before finalizing `scaleGains` or economy.
- **F4/F5:** hidden quest data and ending copy visible to public source API; story sequencing holds in intended UI, not confidentiality against data-mining.
- **Rulings collision:** older Bastion `RUL-2026-10-14-001` (Medical100) collides with `main`'s unrelated art ruling bearing the same ID. Preserve both decisions and reconcile IDs explicitly when integrating; do not overwrite one or infer that either is repealed.
- Source drift: initial topology proof pinned to `13d40c4`; authoring/proof must select and verify actual current source. No fabricated IDs or unsupported tags.

## Scope and evidence boundary

This ChatGPT session changed only **repository design, rulings, plans and handoff files** on its own integration-design branch. It **did not rerun** Fable's Bun/MySQL/native harness or validate a production manifest. The previous committed native evidence is consumed as source evidence; any current-source compatibility belongs to Fable. No engine changes, live requests, live writes, credentials, art production, hidden publication, or `main` merge.

**Next permitted step:** give Claude the exact integrated design handoff HEAD, read the rewritten prompt and separately pinned reward proof brief, use two own implementation/proof branches, and return two frozen exact SHA outputs for ChatGPT independent review.
