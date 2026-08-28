# references/lines.md - reusable enemy lines

Design registries for the shared enemy lines, moved from project knowledge 2026-08-28.
Codes resolve via 32b_DATA_pool.json; the Forsworn registry rides the session bundle docs
until its wave closes, then joins this file.

---

# The Unsigned: reusable operative line

Four AIs covering the whole covert band, usable by any quest in any village. Kits are entirely shared pool records, so nothing strands when a quest retires. Names state the job in one word.

## Runner, level 40

The lookout and messenger. Carries the thing, watches the door, runs the moment it goes wrong. Fights only when cornered, and fights to break away rather than to win.

**Kit**: Fighter's Poise (B37), Veilstep (B09), Quick Strike (S02), Glancing Strike (S38), Gale Bolt (EA01)

**Behaviour**: opens with Veilstep to break contact, keeps at range with Gale Bolt, only closes with Quick Strike when the player is already adjacent. Low damage, high evasion feel. A player who lets a Runner escape should feel they lost something.

**Stat anchor**: offence around 59,000, hp around 3,000, speed at or above band median. Fast and thin.

## Nightfoot, level 55

Covert operations. Posted where something must not be interrupted, or sent where something must be taken quietly. The archive fight in Retrieve the Kage Documents is a Nightfoot.

**Kit**: Hushed Hours (B21), Numbing Shot (S08), Marking Volley (S33), Lunging Strike (S03), Braced Strike (B26)

**Behaviour**: opens Hushed Hours, marks with Marking Volley, stuns with Numbing Shot when the player closes, finishes with Braced Strike. Control first, damage second. Beatable but not a punching bag.

**Stat anchor**: offence around 53,000, hp around 2,600, speed at band median.

## Silencer, level 70

Removes the link between buyer and seller. Turns up after a mission has gone wrong for somebody else. Fights to end it fast.

**Kit**: Veilstrike (B24), Opening Strike (S04), Piercing Judgment (B33), Devouring Grasp (B05), Scorching Rend (B27)

**Behaviour**: Veilstrike opener for the stealth and buff, Opening Strike to apply vulnerability, then Piercing Judgment into the marked target. Burst shaped: dangerous in the first three rounds, fades if the player survives them.

**Stat anchor**: offence around 170,000, hp around 5,700, speed near band median.

## Shadowbroker, level 85

The one who takes the meeting. Does not fight unless negotiation has already failed, which makes it a natural A and S rank confrontation.

**Kit**: Apex Hunger (B18), Sovereign Fetters (B16), Hexweave (B13), Feast of Marrow (B15), Nullifying Wave (B32), Second Wind (S35)

**Behaviour**: Apex Hunger stance, Sovereign Fetters to lock, Hexweave to suppress healing, Feast of Marrow to drain, Nullifying Wave to strip player buffs, Second Wind when low. The only rung that answers what the player does rather than running a script.

**Stat anchor**: offence around 320,000, hp around 6,800, speed near band median.

The Shadowbroker is the one rung that could later earn a bespoke signature, once we see it in play.

## Art

Same silhouette across all four so they read as one organisation: dark layered garb, hood, face wrap covering below the eyes, no insignia of any village. Rung shown through gear, not costume:

- Runner: light, unarmoured, satchel across the body, no visible blade
- Nightfoot: forearm guards, short blade at the hip, tool pouches
- Silencer: mask fully up, two blades, wrapped forearms, darker palette
- Shadowbroker: long coat over the same garb, no visible weapon, hands empty

One battle sprite each. Scene portraits only for Nightfoot and Shadowbroker, since those are the two that appear in dialog.

## Build order

1. Nightfoot first, since Retrieve the Kage Documents needs it
2. Silencer, the next most reusable
3. Runner and Shadowbroker when a quest calls for them

## Decisions for you

1. Stat anchors above are band medians. Should operatives sit at median, or above it since they are professionals?
2. Element: leave all four elementless so they fit anywhere, or give each rung one element for variety?
3. Do they drop anything? A shared item, a note, a contract fragment that chains missions together.


---

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
