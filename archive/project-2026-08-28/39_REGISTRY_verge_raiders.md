> **STALE - archived 2026-08-28 (rollout Stage 1).** moved to building skill references/lines.md.
> Do not build from this file.

# The Verge: reusable border raider line

Four AIs covering the open-fight band, usable by any defense, ambush, patrol or escort-interception mission in any village. The Unsigned handle covert work; the Verge handle everything that arrives in the open and expects to be seen. Kits are entirely shared pool records, so nothing strands when a quest retires.

Naming grammar is deliberately unlike the Unsigned. The Unsigned take compound job names (Fleetfoot, Nightfoot); the Verge take blunt trade nouns, because they are a warband rather than an organisation and nobody in it is hiding what they do.

## Prowler, level 30

The probe. Sent ahead to touch a position and see what answers. Fights to learn rather than to win, blunts what it can reach, and withdraws with the information whether or not it wins.

**Kit**: Twin Shot (S06), Rapid Fire (S07), Quick Strike (S02), Weakening Strike (S27), Fighter's Poise (B37)

**Behaviour**: opens Fighter's Poise, works at range with Twin Shot and Rapid Fire, applies Weakening Strike to the hardest hitter, closes with Quick Strike only when already adjacent. Low individual threat, meant to be fought two or three at a time.

**Stat anchor [RATIFIED 2026-08-26]**: offence around 40,000, hp around 2,400, speed at or above band median. Fast and thin.

**Distance gates**: S06/S07/S27 range 5 gate 6; S02 range 3 gate 4; move fallback below.

## Breaker, level 45

Brought along to make a hole. Takes the gate, the shutter, or the wall, and does not care what it costs, because the band behind it only needs the hole to exist for a few seconds.

**Kit**: Bedrock Breaker (EE02), Shale Bolt (EE01), Heavy Strike (S01), Recoil Slam (B28), Stoneward (EE03)

**Element**: None. The kit is Earth-flavoured but the record carries no element, per the line ruling.

**Behaviour**: Stoneward on open, Shale Bolt at range, Bedrock Breaker the moment the player is inside range 3 (its moveprevent and stun are the signature: it pins you where it wants you), Recoil Slam as the reckless follow-up. Slow, heavy, and punishes a player who stands still.

**Stat anchor [RATIFIED 2026-08-26]**: offence around 62,000, hp around 4,200, speed below band median. Armor Light.

**Distance gates**: EE01 range 5 gate 6; EE02 and S01 range 3 gate 4; B28 range 5 gate 6.

## Warband Captain, level 60

The reason a Verge fight is harder than the sum of its parts. Does not out-damage the Breaker and is not meant to. Buffs the band, marks a target, and keeps the line standing.

**Kit**: Rallying Spiral (B31), Marking Volley (S33), Braced Strike (B26), Sundering Blow (S44), Warrior's Poise (B19), Second Wind (S35)

**Behaviour**: Rallying Spiral early and on refresh, since it is the whole point of the rung and it lifts every ally in range 3. Marking Volley on the player to raise incoming damage for the rest of the band, then Braced Strike and Sundering Blow. Second Wind below a health threshold. Kill priority should feel obvious: leave the Captain alive and the fight gets worse every round.

**Stat anchor [RATIFIED 2026-08-26]**: offence around 130,000, hp around 5,400, speed at band median. Armor Medium.

**Distance gates**: B31 range 3 gate 4; S33, B26, S44 range 5 gate 6.

## Verge Warlord, level 75 [SPECCED, not built]

The one who decides the border is worth crossing. Built when a mission needs an A rank confrontation rather than a raid.

**Proposed kit**: Sovereign Ascendance (B10), Worldbreaker Chorus (B17), Suppressing Roar (B30), Piercing Judgment (B33), Rallying Spiral (B31), Second Wind (S35)

## Why this line and not more Unsigned

Of the AIs at level 30 to 60, the reusable ones are almost all covert or creature records. A defense mission fighting Nightfoot reads wrong: the Unsigned are hired quiet professionals, and an outpost assault is neither quiet nor professional. Two lines with clearly different jobs also let a mission mean something by which one turns up.

## Art

One silhouette across all four so they read as one band: layered hide and scavenged plate that does not match, heavy cloth face wrap, fur at the shoulder, no insignia of any village. Rung shown through gear, not costume.

- Prowler: light, no plate, throwing gear at the belt, hood up
- Breaker: mismatched heavy plate on one side only, gauntlets, no visible blade
- Warband Captain: banded plate, a horn at the belt, a heavy blade across the back
- Warlord: full mismatched harness, cloak, helm carried rather than worn

One battle sprite each. Scene portraits only for the Captain and the Warlord, since those are the two that ever speak.

## Build order

1. Prowler and Breaker first, since Protect the Outpost needs both
2. Warband Captain, for the same mission's second wave
3. Warlord when a mission calls for it

## Rulings (2026-08-26)

1. **Stat anchors ratified** as written above.
2. **All four elementless.** `element: None` on every rung, including the Breaker, whose kit reads Earth without the record being typed. Keeps the line droppable into any mission and any village.
3. **No drops.** No band token, no chaining material.
4. **Warlord is not built.** Spec stays on the shelf until a mission asks for it.
