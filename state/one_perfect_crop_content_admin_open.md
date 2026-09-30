# One Perfect Crop — content-admin resolution

**Status:** RESOLVED for launch finalization  
**Resolved by:** dauntless / content admin  
**Resolution date:** 2026-09-24

## Launch-final decisions

| Field | Final decision | Implementation consequence |
|---|---|---|
| Event Ryo reward | None | Author no Ryo reward. |
| Event XP reward | None | Author no XP reward. |
| Event token / other standard reward currencies | None | Author no token/other standard-currency reward. |
| Cabbage Seed mechanical item | Skip | Do not create a Cabbage Seed item and do not grant one as a quest reward. The seed may remain in the ending prose as narrative flavor only. |
| Repeatability / attempts | 100 max attempts | Set `maxAttempts: 100`. |
| Maximum completions | 1 | Set `maxCompletes: 1`. |
| Cooldown | None | Do not author `retryDelay` or `attemptDelay`; leave both optional delay fields unset. |
| Eligibility | Disregard submitted Farming level 15 requirement | Author no Farming gate and no substitute eligibility gate. In particular, do not map it to character `requiredLevel: 15`. |

## Locked launch-final consequences

- The quest has **no mechanical reward package** beyond completion itself.
- No Cabbage Seed item is created or granted.
- The existing seed-packet / surviving-seed story beat may remain as prose flavor; it does not imply an inventory reward.
- `maxAttempts: 100`.
- `maxCompletes: 1`.
- No retry/attempt cooldown fields.
- No eligibility gate.
- No unique jutsu reward.
- Both battles remain one-enemy, scale-to-user PvE.
- Battle loss hard-fails the event.
- No authored retry branch inside the quest graph.
- Publishing/unhiding remains a separate user-owned action.

## Relationship to earlier open packet

This file previously tracked unresolved Ryo/XP/currency rewards, Cabbage Seed type/rarity/economics, repeatability and Farming-level eligibility. The 2026-09-24 director decisions above close all of those launch-final admin questions. Later implementation must copy these decisions exactly rather than reviving the superseded open requirements.
