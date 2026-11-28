# Isonade v8: every chain marker is a tag no player can put on Isonade (HIDDEN)

The director (2026-11-20 00:25Z, relayed): **"Key all five"**. This followed job 666, which keyed the Undertow on a
self marker no player could set. The same approach now covers Black Water Floods, Swell Rises (and the Tidal Bore),
Brine Brand, the Breaker and the Tide.

Job 667 (`push/667_isonade_v8_inert_markers.gen.py`). Rollback captures:
`state/stolen_stores_captures/isonade_v8_live_2026-11-20/`, read back on 2026-11-20 and identical to post-666.

## The problem

Each step of Isonade's rotation leaves a short self marker, and the next step's rule reads it with `has_effect`.
`has_effect` adds up every effect of that type on Isonade from any caster. So when a player puts the same type on
Isonade, the next step fires out of turn.

| Rule | Move | Old key | Player sources in the catalog (visible jutsu and items that land on an enemy) |
|---|---|---|---|
| 3 | Black Water Floods | seal | 18 jutsu, 2 items |
| 5 | Swell Rises | increasepoolcost | 16 jutsu, 5 items |
| 4 | Tidal Bore | increasepoolcost + robprevent | as above (robprevent: none) |
| 9 | Undertow | elementalseal 100 (job 666) | 1 jutsu at 80 (Heaven's Rupture Oath, cooldown 7) |
| 10 | Brine Brand | healprevent | 4 jutsu |
| 12 | Breaker | increasecooldown | 1 jutsu, 1 item |
| 13 | Tide Draws Back | fleeprevent | 1 jutsu (power 10) |

Source: harvest `tnr_results_1794368544997` (1,186 visible jutsu, 664 items, 50 bloodlines).

## The fix

Each marker becomes an out-of-combat tag type. They are kept at power 100, with the same rounds, SELF target,
"Isonade's rotation" text and animation fields as before. The rules read them at 100.

| Laid by | Old marker | New marker | Rule it calls |
|---|---|---|---|
| Barnacle Hide | fleeprevent 100 (2) | noncombatgainskill | 13 Tide |
| Tide Draws Back | increasecooldown 1 (2) | unlockitemvariant | 12 Breaker |
| Harpoon Line | healprevent 100 (2) | marriageslotincrease | 10 Brine Brand |
| Brine Brand | elementalseal 100 (2) | increaseregeneration | 9 Undertow |
| Omen: Black Water | seal 100 (2) | noncombatincreasereskins | 3 Black Water Floods |
| Swell Builds | increasepoolcost 100% Health (3) | repair | 5 Swell Rises; 4 Tidal Bore (with robprevent) |

Why these types (engine pin 3314d122):

- **No player can put one on Isonade.** None appears on any visible player jutsu or item aimed at an enemy. A few
  exist only as self-use consumables, which land on the user.
- **No player can take one off.** They are on neither the Clear list (isPositiveUserEffect) nor the Cleanse list
  (isNegativeUserEffect). So a player's Clear or Cleanse cannot cut a chain, and neither can Isonade's own Deep cleanse.
- **They do nothing in combat.** Combat has no handler for them, so they sit as timed effects that `has_effect` can read.
  The jutsu validator allows them. The only combat code that names one skips increaseregeneration for raid buffs.
- **They keep their power.** Prevent tags reset to 100 when they land, but these do not, so a threshold of 100 is
  reliable.

Unchanged: disarm (The Deep), weakness (the Harpoon after a hit) and robprevent (Swell Rises; positive, with no
player source).

The Omen: Black Water keeps its self seal and only gains the marker. Isonade's passives (stunprevent 100, "Old hull"
70% damage reduction) are realised as bloodline effects, and a seal blocks bloodline effects, so the omen's self seal is
what opens the Black Water burst window. Moving only the key keeps that window.

## Build (jobs 667 and 668, HIDDEN)

- **667** ran phase 10 (the six chain jutsu off Isonade) and five of the six edits (Barnacle Hide, Tide Draws Back,
  Harpoon Line, Brine Brand, Omen: Black Water), all verified. The Swell Builds edit was refused by the jutsu validator:
  every one of these tag types validates only with `direction: "offence"`, and the generator had kept the old
  increasepoolcost marker's "defence". Nothing was written for Swell Builds. The runner journaled the item FAILED and
  went on, so it was stopped before phase 30. No results bundle. Journal: `/mnt/project-files/tnr/isonade_build/v667_state`.
- The generator now sets `direction: "offence"` on every new tag (only Swell Builds changes).
- **668** (`push/668_isonade_v8_finish.gen.py`) re-sent phase 10, the corrected Swell Builds edit, the full live kit
  (phase 30) and the 20 rules (phase 40). DONE 4/4, bundle `harvests/inbox/tnr_results_1795135296365.json`.
- Read-back (`state/stolen_stores_captures/isonade_v8_live_2026-11-20/post668_getAi_isonade.json`): 18/18 equipped,
  each marker as in the table above at power 100, SELF; rules 3, 4, 5, 9, 10, 12 and 13 read them at 100.

Tooling note: a refused mutation is marked FAILED in the journal, but the runner carries on to later items. On a law-18
job that can leave an AI with its kit off. Here it was caught before phase 30 and nothing was left half-done.

## Sim (harness/combat_sim, pin 3314d122, 12 seeds)

| Variant | Win | dauntless HP left when won | Rounds |
|---|---|---|---|
| v8, no harass | 75% | 39.3% | 16 |
| v8, player seal / cooldown / elementalseal / pool cost / root / heal block harass | no chain move fires out of turn (0 strays) | | |
| live 666 rules, same harass | lost to the seal, cooldown, elementalseal and pool-cost harass | | |

v8 without harass is identical to live 666 without harass, so the rekey changes nothing for a player who leaves the
markers alone.

**Open for the director:** any player seal on Isonade switches off its hull DR (the same bloodline rule the omen uses).
In the sim a player who keeps Isonade sealed wins every seed. dauntless has no seal source (Danse Macabre no longer
carries one live), so this was not tested live.

## Live hidden test (battle SLdsDNxBf-XdfUUFwOvNP, 2026-11-20 00:43-00:46Z)

dauntless: PvE jutsu set with Crimson Surge in for Stunning Jab, PvE armour, Elite Smoke Bomb, Night's Testament in
HAND_2, pet Little Horror, full HP. Log: `/mnt/project-files/tnr/battle-logs/2026-11-20_isonade_v8_fivekeys_test_SLdsDNxBf-XdfUUFwOvNP.json`.

**Won round 10, dauntless 1,951 / 5,050 HP.**

- Player effects on Isonade tripped nothing: Dragon's Tomb root on R1 and R8, Crimson Surge pool cost (+76%) on R2.
- Rotation in order: Barnacle Hide R1, Tide R2, Breaker R3, Scour R4, Omen: Black Water R5 (at 69%), Floods R6,
  Harpoon R7, Omen: The Deep R8 (at 27%), Surfaces R9 after Night's Testament pierced the 4,000 shield, dead R10.
- Floods: 0 damage standing on the crate at E6. Isonade sealed R5-R7: Ember Blade 1,364, Storm Fist 2,710.
- Breaker R3: 4,199 + 500 shield (net about 2,650 after absorb). Not cleared: Tide's +200% stayed on. The two earlier
  runs that Cleared it took 2,349 and 557. Clear strips the buff but not the Tide marker, so the Breaker still comes.
- Arm Lash one-shot Little Horror (4,545) on R2, as in both earlier tests.
- Not reached: Brine Brand and the Undertow (The Deep took priority), Swell Builds and the Tidal Bore (Harpoon and
  The Deep outranked them), so the smoke bomb was not needed. The sim covers those keys.
- Not testable live: a player seal (dauntless has none) and elementalseal 80 twice (Undertow no longer reads
  elementalseal; dauntless does not own that jutsu).

Why the two earlier tests lost:
- 665 brand key (lost R9): the Undertow fired twice (2,284 and 899) because Brine's heal block outlasted its cooldown.
- 666 marker key (lost R18): played as a probe. Pet dead R1, Harpoon five times (3,535), Floods taken off the crate
  (2,643), Breaker 2,349.

Cleanup: dauntless repaired, Aetherion back in HAND_2, Stunning Jab back in slot 8 of the PvE set, loadouts soXek and
B-bCC, asleep in 177. No Full Potion left, so HP stays at 1,951 and regenerates while asleep. Lock released.
