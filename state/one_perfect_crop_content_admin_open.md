# One Perfect Crop — content-admin open fields

**Purpose:** the quest design and implementation prep may continue, but these user/content-admin values are intentionally unresolved and must not be guessed into a runnable manifest.

## Required decisions before final manifest validation

| Field | Current requirement | Admin action |
|---|---|---|
| Event Ryo reward | Small / balance-owned | Supply exact value, including zero if intended. |
| Event XP reward | Small / balance-owned | Supply exact value, including zero if intended. |
| Event token / other standard reward currencies | Balance-owned | State which are used and exact values. |
| Cabbage Seed rarity | Unset | Select supported rarity. |
| Cabbage Seed item type | Reward is one `Cabbage Seed` | Select the supported functional item type that best represents a seed/flavor/material reward. |
| Cabbage Seed economic/value fields | Unset | Supply every required numeric/economic value for the chosen item type. |
| Repeatability | Submitted sheet says once `[BALANCE]` | Approve once-only or select supported repeat policy. |
| Eligibility | Submitted sheet says `Farming level 15` | Select an engine-supported gate or explicitly remove the mechanical gate. Do not silently substitute character level 15. |

## Eligibility warning

The current quest objective vocabulary documents profession counters for gathering, hunting, crafting and medical progression, but the current generated/reference surface does not establish a native farming progression gate. The phrase `Farming level 15` therefore remains a design requirement, not yet an implementation field.

Permissible resolution pattern:
1. content admin identifies a supported existing progression field that intentionally represents the requirement; or
2. content admin explicitly removes/substitutes the gate for this event.

Implementation must record which choice was made. Existing live values or schema defaults are not approval.

## Locked non-balance facts

- PASS reward item includes exactly `Cabbage Seed x1`.
- No unique jutsu reward.
- Both battles are customary/fair PvE, one enemy each, scale to user.
- Battle loss hard-fails the event.
- No authored retry branch.
- All new entities create hidden; publishing is a separate action.
