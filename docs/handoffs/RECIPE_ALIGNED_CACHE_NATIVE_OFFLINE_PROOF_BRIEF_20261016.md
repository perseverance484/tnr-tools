# Native Offline Proof — Silent Bastion One-of-Two Reward Cache Selection

> **CURRENT JOINT DESIGN STATUS — 2026-10-16.** Both `alt99_f4gate` (99 objectives; four interior divisions, RUL-2026-10-16-002) and the **Arsenal-or-Research, choose-exactly-one completion reward** pilot (RUL-2026-10-16-001) are director-approved **design directions**. Beacon B1 is now **SETTLED** by RUL-2026-10-16-003: debit one Beacon **at expedition start (`startQuest`)**, never refunded on abandonment/failure and no second payment for checkpoint retries. The executable reward choice and Weighted Cache open/receipt path still need Fable's **separate native offline proof**. Exact recipe choices, quantities, weights, rarity/tradability, reward economy, Arakane player Combat Protocol, art and publication are **not approved**. The operative Fable implementation contract is `state/prompt_silent_bastion_complete_authoring.md`; older superseded five-division/first-battle wording below is historical. Shared reward sources were adopted from `chatgpt/recipe-aligned-reward-caches-20261016@fb744e713873a99812b7c6e9ec8631769ef9ff9a` before scoped current-status edits. No live requests/writes.

**Status:** READY TECHNICAL PROOF BRIEF, NOT REWARD IMPLEMENTATION OR CONTENT ACCEPTANCE.  
**Owner:** Fable / Claude Code, sole writer on a **new Fable-owned branch**; ChatGPT independent reviewer of frozen SHA.  
**Director decisions already recorded:** `RUL-2026-10-16-001` (exactly two new Arsenal/Research recipe-aligned caches; select one after successful Pyramid completion), `RUL-2026-10-16-002` (select native-tested `alt99_f4gate` 99-node Bastion graph on separate ChatGPT Bastion branch).  
**Main reference:** `perseverance484/tnr-tools@99e86dc549b86f1f4a5846c0e509fa6bc15b3463`; reverify before work.  
**Game source:** `studie-tech/TheNinjaRPG@0651b039a466516a8fe24fc13b56f60dea11b7eb` as last verified at 2026-10-16; pin actual proof source, compare if newer.  
**No production requests:** zero calls to theninja-rpg.com / live endpoints, no credentials, no game writes; throwaway database/in-process only. Do **not** create a live-clickable `push/` manifest.

## Prerequisites and scope

Reconstruct project authorities (`state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, applicable source/design/role/contract files). Read:
- This design owner: `docs/design/RECIPE_ALIGNED_REWARD_CACHES_DISCOVERY_20261016.md`; comparison `docs/design/RECIPE_ALIGNED_CACHE_PILOT_REVIEW_20261016.md`; machine candidate `docs/design/RECIPE_ALIGNED_CACHE_CANDIDATE_POOLS_20261016.json`. These contain **unapproved** concrete recipe inclusion, probabilities and quantities; only use throwaway examples.
- Bastion acceptance: `chatgpt/silent-bastion-alt99-approval-20261016` `state/silent_bastion_design.md`, `state/prompt_silent_bastion_complete_authoring.md` and `RUL-2026-10-16-002`. Fable frozen native proof `claude/silent-bastion-budget-validation-69za5u@74eeb328f05d4258056b0a1c531619ffcf852ce3`, `harness/silent_bastion_condensed99/graphs/alt99_f4gate.json` and `docs/reviews/SILENT_BASTION_CONDENSED99_NATIVE_RESULTS.md`. The original 99-node candidate **failed** and is not allowed as the build source.
- Upstream `app/src/libs/quest.ts` `getReward`, `app/src/libs/rewardChoice.ts` `buildRewardChoiceCards`/`verifyRewardChoiceForSave`/`rewardFromChoiceCards`, `app/src/server/api/routers/quests.ts` `claimRewardChoice`/save/claim, `app/src/server/api/routers/item.ts` `item.consume`, `app/src/libs/weightedCache.ts`, `app/src/validators/{weightedCache,rewards,combat}.ts`; existing upstream tests `app/tests/libs/rewardChoice.test.ts`, `app/tests/server/api/quests.rewardChoiceSql.test.ts`, `app/tests/server/api/item.weightedCache.sql.test.ts`, `app/tests/server/api/quests.pyramidConsequences.test.ts`.

This is a **small cross-feature integration proof**, not a redesign of battlepyramid, builder, item schema, reward balancing or live quest.

## Positive path to demonstrate

1. Create a synthetic **hidden** `battlepyramid` quest in a throwaway DB, preserving isolated/entry/item requirements and valid graph semantics. Use the approved `alt99_f4gate` graph if feasible; if a smaller equivalent fixture is needed for speed, separately keep a regression confirming the selected graph.
2. Set **quest-level** `content.rewardMode:"choose"` and `content.rewardPickCount:1`. Put **exactly two distinct cache-item IDs** at `content.reward.reward_items`, each `number:100`, `quantity:1`. Put **no cache reward_items** on `w.complete` or any ordinary objective. Build synthetic `CONSUMABLE`, `destroyOnUse:true`, `preventBattleUsage:true` cache items with one `noncombatconsumereward` effect using `rewardMode:"weightedCache"`. Use scratch ordinary test ingredient items, not hidden, event-exclusive, reputation/bloodline or Ghost Ship rewards.
3. Save and validate the quest through real `quests.update`/schema pathways. Start, win battles and complete once via native routers; verify nothing is awarded before completion, no category is auto-granted, and a **frozen one-of-two item offer** is stored.
4. Claim Arsenal; prove exactly one Arsenal inventory item, zero Research. Replaying or parallel duplicate claims must not duplicate the cache. Repeat from a fresh attempt where the Research card is picked and assert the inverse.
5. Consume the chosen cache via real native `item.consume` with a requestId; verify one valid weighted **tier → uniform entry** selection awards all ingredient IDs/quantities together, no other recipe's materials, and a replay returns the stored receipt without debiting a second cache. Prove distinct request concurrency / grant rollback / invalid cache configuration defenses already present in the source tests.
6. Run losing/abandonment/recovery paths: no pending offer and zero new caches on failed attempts, no duplicate offer from recovery resets or battle starts, one successful completion = one offer. Verify the director-approved Beacon behavior (RUL-2026-10-16-003): consume **exactly one at `startQuest`**, never at first battle or retry, never refunded; reject a source drift rather than silently changing the approved timing.
7. Verify responsive/mobile-facing reward-choice content is present in the ordinary API view where available; a full interactive Android check is **not** part of offline proof. If the UI cannot expose the pick through the Battle Pyramid, label as **unverified/blocked**, not PASS.

## Negative controls and regression gates

- Force a cache item directly into a `win_quest.reward_items` in a *negative* fixture: demonstrate it **bypasses** one-of-two choice and/or grants directly, which is why it must never be used.
- Invalid tier/roll sums (not both 10,000), zero positive-tier entries, missing referenced ingredient, and forbidden item/bloodline/reputation rewards must fail before consuming.
- All rewards must remain player-owned; no rank-gated exclusive profession/material leakage via cache tables. The proof's synthetic ingredients do not constitute approval of the real proposed material sources.
- Confirm no extra graph objectives needed to claim the final reward; the selected `alt99_f4gate` topology stays 99, not 103 or a new ending.
- Distinguish **existing upstream unit/SQL passes** from **new Bastion × reward-choice × weighted-cache integration** passes. Do not assert source compatibility solely from a general feature being present.

## Pass/fail deliverable and ownership

Commit a concise `docs/reviews/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_RESULTS.md` (or equivalent task-owned proof result), minimal fixture/test harness and reproducibility instructions on the **Fable-owned branch**. Include exact source/test SHAs, actual commands and test counts, original/modified files, local grant/receipt traces, current-source differences, and what was **not** tested (production, UX, balance). Freeze the exact handoff SHA and send it to ChatGPT for independent review.

**PASS:** validated one-of-two end-of-Pyramid offer, both claim paths, exactly-once grant, coherent weighted bundle consumption, reset/failed-attempt isolation, and source-aligned validators. The resulting feature contract may be used *later* by normal Fable manifest construction **only after separate director approval** of candidate recipes/rates/items/presentation and other Silent Bastion gates.

**FAIL:** reproduce minimal defect and propose smallest source-supported workaround **without** changing source contracts/engine code or gameplay rules unless a subsequent director-approved Lane A brief authorizes that change. No live read/write under either outcome.
