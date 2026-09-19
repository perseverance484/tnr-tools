# Review — Godstorm retained AI rule / jutsu safety

Date: 2026-09-19  
Scope: all 18 retained Marrow Vaults + Stormcourt AI records  
Result: **one repeated runtime-safety defect confirmed in all 18 captured authored profiles; target/range references otherwise reconcile cleanly. A bounded correction is specified below.**

## Evidence

- TNR Tools capture baseline: `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`.
- Quest graphs: `harvests/inbox/tnr_results_1789401726302.json`.
- Full AI records / embedded equipped jutsu definitions: `harvests/inbox/tnr_results_1789402842027.json`.
- AI profiles: `harvests/inbox/tnr_results_1789403623148.json`.
- Current game-source audit pin: `studie-tech/TheNinjaRPG@a670c9aaa741157dc66eacc949600ff2db0b48cd`.
- Source paths inspected: `app/src/validators/ai.ts`, `app/src/libs/combat/ai_v2.ts`, `app/src/libs/combat/actions.ts`.

The repository generated contracts currently trail this upstream pin, and current `main` itself carries an upstream-contract-drift sentinel commit. Runtime conclusions in this review therefore come from the current pinned game source plus the full saved captures, not from stale generated schemas alone.

## Runtime facts that matter

`performAIaction` resolves the AI-rule target independently of the selected jutsu. For `use_specific_jutsu`, `use_combo_action` and highest-power actions, the profile rule supplies the target coordinate. The jutsu's own `target` and `range` are still enforced later by combat action processing. A profile can therefore select an action successfully and then fail when the supplied coordinate is illegal for that action.

`availableUserActions` filters availability/cost/cooldown/status but does not limit the list to actions whose range reaches the current rule target. `performBattleAction` ultimately routes through `insertAction`; if the selected action cannot affect the selected tile, it returns false and `performBattleAction` throws `Action <name> no longer possible for <user>`.

Distance conditions in the AI profile are based on A* path length. The game's own default profile uses `distance_lower_than <= 2` for the adjacent highest-damage fallback and basic attack has range 1. That current engine pattern is the bounded fallback used for the correction below.

## Complete retained-AI audit

| AI | AI id | Captured profile | Specific/combo target match | Specific/combo range guards | Current fallback |
| --- | --- | --- | --- | --- | --- |
| Umbral Reaver | `9uDe65Qt90xnT-fM5vJZ7` | `muR-teDw81mr-16Gr9TLn` | PASS | PASS | **FIX** rule 4 |
| Hollow Lantern | `IG5Mbfi_2lpUTnUU4_XhZ` | `NyfJUsMqCBImEqMwl_Cfd` | PASS | PASS | **FIX** rule 3 |
| Starless Monk | `qQ6jMh8w6aiyr4pevwDh-` | `I6YfpRU-Rid8EBkFwBXra` | PASS | PASS | **FIX** rule 4 |
| Nightveil Sentinel | `YvinZCoMWiz0RY8ZBP5EW` | `AzVC76q7s98Ip9D_KZrQA` | PASS | PASS | **FIX** rule 4 |
| Warden of the First Dark | `oi4bHe3upEhLkI-ElJuMX` | `ODZUYqBF1MjvEpnc96gvc` | PASS | PASS | **FIX** rule 4 |
| Keeper of Hushed Hours | `s6LjnqhSW85pIxYRM76Fw` | `1Aw1W61zQKukzGs8KLZig` | PASS | PASS | **FIX** rule 3 |
| The Moth Tyrant | `jGHpkz2pgLu8loti6pZZi` | `G5Qti2x1kIl0bNw-viW1A` | PASS | PASS | **FIX** rule 3 |
| Chained Chorister | `QV1PwoQR9JImZL2_fcOsk` | `JKZ0osqzYdiQv00R-yOxr` | PASS | PASS | **FIX** rule 3 |
| Warden of the Half Eclipse | `3XMsIV6Yv4jy-uaJAe52f` | `k4iTMFZVIV1LksVL4QQZ7` | PASS | PASS | **FIX** rule 4 |
| Hollow Lantern Ascendant | `b8PGgZl8zNNr6UdWH9dBv` | `ZizkLReBsv70HbhI-lXXL` | PASS | PASS | **FIX** rule 3 |
| Starless Monk Ascendant | `JU2BgfdcWsBYGeHUgHMi_` | `fw0UV78pfIKUCPnAtd6po` | PASS | PASS | **FIX** rule 4 |
| Nightveil Sentinel Ascendant | `9yLEi0OoYxcIL0a2XYkWk` | `cMgDkb6qPzzsVgM1UnuiH` | PASS | PASS | **FIX** rule 4 |
| Umbral Reaver Ascendant | `k4qMHSTHHZBVsijP5FJ6E` | `tqI4rY5R1A0CweRMavxvF` | PASS | PASS | **FIX** rule 4 |
| The Gloaming Judge | `axTRSadaZbUepfT40-7cM` | `Ha60aj66Hz4yo-C7V4JH3` | PASS | PASS | **FIX** rule 4 |
| Widow of the Waning Moon | `HEjtNpXmuU4ShrOOPg8XK` | `2vpKOl94SuYxGsNHZnyWV` | PASS | PASS | **FIX** rule 3 |
| The Candlewright | `pln436P8g2ocUBCHavcdb` | `qwvUPKMr1n98leSKHs3i1` | PASS | PASS | **FIX** rule 3 |
| Herald of the Last Dusk | `aL1Gf1JmVaP8iWi2zHJoO` | `t_batIaeD6PEk4NkLIbrt` | PASS | PASS | **FIX** rule 4 |
| Sovereign Echo of the Godstorm | `i8oFdDcneF7YE-8VpQsu3` | `HbL9DwQlL42dvPoZE6itD` | PASS | PASS | **FIX** rule 3 |

### Target check

Every captured jutsu referenced by an authored specific/combo rule is equipped on that AI.

- Every referenced `SELF` jutsu is invoked with profile action target `SELF`.
- Every referenced `OTHER_USER` jutsu is invoked with `RANDOM_OPPONENT`.
- No authored combo mixes SELF and opponent jutsus under one combo target.
- No referenced combo/specific jutsu id is missing or unequipped.

Observed SELF actions are `Warrior's Poise`, `Compression Barrier`, and `Hushed Hours`; all are rule-targeted SELF. Offensive actions are rule-targeted RANDOM_OPPONENT.

### Range check

Every authored specific/combo offensive rule has an opponent-distance upper bound at or inside the minimum range of the jutsus that rule can select:

- Quick Strike: range 3, guarded at <=3.
- Opening Strike: range 4, guarded at <=4.
- All captured offensive combo members used here: range 5, guarded at <=5.

These guards are conservative under the engine's path-length distance representation and do not overreach the action's range.

## Confirmed repeated defect

Every retained profile ends its authored rules with an unconditional:

`use_highest_power_action(effect=damage, target=RANDOM_OPPONENT)`

The profiles also have a prior move-toward-opponent rule, but a checked move rule does not guarantee a move is produced. Movement may be unavailable or fail to produce a usable path/hex; when that happens the rule loop continues.

Because highest-power selection draws from available actions without a range-to-current-target filter, the unconditional fallback can select a damage action and hand it an opponent coordinate outside that action's range. Current combat processing then rejects the action and can throw. This is the exact failure class the director asked to eliminate.

## Correction

For each of the 18 profiles, preserve every existing authored rule and change only the final highest-damage fallback from no conditions to:

```json
{
  "conditions": [
    {
      "type": "distance_lower_than",
      "description": "Distance lower than or equal given value",
      "value": 2,
      "target": "RANDOM_OPPONENT"
    }
  ],
  "action": {
    "type": "use_highest_power_action",
    "effect": "damage",
    "target": "RANDOM_OPPONENT",
    "description": "Use highest power action of given effect"
  }
}
```

Why 2: this matches the current engine's own bounded highest-damage backup rule. It is safe for basic attack (range 1 under the engine's path-length distance convention) and therefore also safe for the longer-range offensive jutsus in these 18 kits.

The engine-owned default rules remain enabled. If an AI cannot move at longer distance, the corrected authored profile no longer forces an out-of-range attack; execution can continue through the engine fallbacks/end-turn path instead.

## Post-correction result

A programmatic second pass over the corrected 18 rule sets found:

- 18/18 profile records present;
- 0 missing/unequipped specific or combo references;
- 0 target mismatches;
- 0 offensive specific/combo rules with a guard beyond their jutsu range;
- 0 unbounded authored highest-damage rules;
- 0 remaining issues under this target/range audit.

This is a static/source audit, not a live battle playtest. No live request or game write was made.

## Manifest consequence

The current Godstorm manifest must include **18 `aiProfile` edit entries**, each targeted by the existing AI user id, preserving the captured rules and `includeDefaultRules:true` while applying only the bounded fallback condition above. No AI kit, stat, item, jutsu, image, or identity field is changed by these profile edits.
