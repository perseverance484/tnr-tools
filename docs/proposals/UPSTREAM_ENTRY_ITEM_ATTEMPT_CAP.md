# Upstream proposal: exempt paid-entry quests from the lifetime attempt cap

**For:** studie-tech/TheNinjaRPG maintainers. **From:** the TNR content team (Skyglass event). **Source pin:** 2af4b320.
**Status:** draft for the director to send (RUL-2026-10-29-039 item 6).

## Problem

Quest types in `QuestTypesWithMaxAttempts` (`drizzle/constants.ts:1097`) count every start, including restarts, in
`questHistory.previousAttempts` (`server/api/routers/quests.ts` ~3663/3720). That counter is never reset. Once it
reaches `maxAttempts`, the quest can't be started again (`libs/quest.ts` ~2484-2488), and `maxAttempts` is capped at 100
(`validators/objectives.ts:906`). `retryDelay` does not exempt the check.

For quests entered by spending `entryItems` (battlepyramid "chart" runs), the item is already the gate: every start
costs a dropped, tradeable item. The lifetime cap adds nothing there, and it breaks the content:
- A dedicated player hits 100 starts on a farmable chart run (about 450 Wreck clears for the most common chart).
- Every chart they find after that is a dead item.
- Failed runs and retries count too, so a player who loses often burns the cap faster.

## Proposed change (smallest compatible extension)

In the attempt check in `libs/quest.ts`, treat a quest whose `content.entryItems` is non-empty as exempt from the
lifetime attempt cap, the same way `ignorePreviousAttempts` already bypasses it:

```ts
const paidEntry = (questAndUserQuestInfo.content?.entryItems?.length ?? 0) > 0;
const eventAttemptsCheck =
  ignorePreviousAttempts ||
  paidEntry ||                       // each start already consumes an entry item
  !QuestTypesWithMaxAttempts.includes(questAndUserQuestInfo.questType) ||
  !questAndUserQuestInfo.previousAttempts ||
  questAndUserQuestInfo.previousAttempts < maxAttempts;
```

- `maxCompletes` and the per-period caps are unchanged.
- Quests without entry items behave exactly as today.
- **Test:** a battlepyramid quest with an entry item and `previousAttempts >= maxAttempts` can still be started.
  Without entry items it is still refused.

## Alternative

Raise `maxAttempts`' validator ceiling (100) for quests with entry items only. This is less clean: the cap still exists,
just higher.

## Why it matters

The Skyglass chart system (PoE-style maps) has players farm the Wreck for charts and spend them on isolated runs:
commons, hunts, rares, tainted runs, steeping, and S-rank profession hauls. Without the exemption, the most engaged
players are cut off from the content they've farmed charts for.
