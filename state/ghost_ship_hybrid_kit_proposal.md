# Ghost Ship / Skyglass — accepted hybrid jutsu test baseline

**2026-10-11 support decisions (RUL007/008):** Crowned Captain heals strictly below40%, Copies at IDG71 or higher and uses Reflect regularly. `state/ghost_ship_skyglass_crowned_support_behavior.md` owns this behavior and its test brief. Trigger values/boundaries are settled; exact ordering/selector implementation and measured balance remain open. The unchanged JSON remains the historical accepted membership/test input; its older support-activation question is superseded.

**Status:** DIRECTOR-ACCEPTED KIT BASELINE FOR OFFLINE TESTS under `RUL-2026-10-11-003`, accepting proposal commit `89fa921c839a9830fd66bb64aa267c470e8dd678`. All eleven memberships, substitutions, consolidations and both Sentinel assignments are accepted. Crowned support activation is directed by RUL007; final details and measured balance/parity remain open. This is not a combat freeze or Forge manifest. Converted names are used for readability; final presentation acceptance remains separate.

The historical filenames and JSON keys containing `proposal`/`proposed` are retained for stable references; their kit contents are now accepted by the ruling above.

**Owner:** ChatGPT designs/reviews; Fable implements offline tests and, after freeze, the manifest. Director owns balance and final acceptance. No live-game requests/writes.

## Accepted kit direction

Keep all five regular-Captain moves and ten of eleven Crowned-Captain moves. Replace redundant crew moves with existing shared records, keeping separate defensive/offensive stances. Reuse two approved retained techniques on Sentinel where global alternatives would introduce a stun or remove Health drain. Do not introduce new Clear, time-compression or pull mechanics merely because the superseded migration selected them.

| Enemy | Captured → accepted count | Accepted kit (not priority order) |
| --- | ---: | --- |
| Deck Warden | 8 → 7 | S02 Quick Strike; EW01 Tide Bolt; S07 Rapid Fire; S08 Numbing Shot; EE03 Stoneward; EW03 Springguard; EA03 Windlash Focus |
| Seal Charge | 1 → 1 | Core Rupture |
| Core Canister | 1 → 1 | Core Rupture |
| Core Horror | 8 → 7 | Rigging Snare; Hollow Timber; EE03 Stoneward; EW03 Springguard; EA03 Windlash Focus; S08 Numbing Shot; S06 Twin Shot |
| Oathkeeper | 8 → 6 | Rebounding Form; EE03 Stoneward; EA03 Windlash Focus; S04 Opening Strike; S07 Rapid Fire; S02 Quick Strike |
| Wayfinder | 8 → 6 | S03 Lunging Strike; S06 Twin Shot; S07 Rapid Fire; EE03 Stoneward; EW03 Springguard; EA03 Windlash Focus |
| Arsenal Keeper | 8 → 7 | Revocation Strike; S01 Heavy Strike; S06 Twin Shot; S08 Numbing Shot; EE03 Stoneward; EW03 Springguard; EA03 Windlash Focus |
| Sentinel | 9 → 7 | Rebounding Form; Rigging Snare; Hollow Timber; B39 Light Barrier; EE03 Stoneward; EW03 Springguard; S06 Twin Shot |
| First Blade | 8 → 7 | Remembered Form; EE03 Stoneward; EW03 Springguard; S08 Numbing Shot; EL04 Ion Lance; S04 Opening Strike; S07 Rapid Fire |
| The Captain | 5 → 5 | Unbroken Command; Remembered Form; Keelbind; B14 Cataclysm Detonation; B17 Worldbreaker Chorus |
| Crowned Captain | 11 → 11 | Unbroken Command; Suppression Writ; Final Command; Keelbind; Ruin Refrain; Rebounding Form; EA03 Windlash Focus; S31 Unraveling Strike; B14 Cataclysm Detonation; S35 Second Wind; B07 Stolen Form |

The accepted baseline uses **11 retained legacy IDs and 18 shared IDs**, with **75 → 65 equipped memberships** across the eleven AIs. All original retained and already-shared memberships survive. The other 26 legacy IDs become candidates for removal from these kits, not database deletion.

## Accepted tradeoffs and remaining behavior decision

1. **Sentinel shares Rigging Snare and Hollow Timber.** These are two new equipped memberships, explicitly accepted. Grasp of the Buried → Rigging Snare changes only the attack element from Sand to untyped among combat fields; Damage100, root1r, AP60/CD2/range4 remain. Sand-Choke → Hollow Timber keeps Damage100 and static250 drain from Health/Chakra/Stamina for2r, but changes Sand→Wood, range4→3 and CD3→2. No retained record is edited. This is closer to its original role than EE02 (adds guaranteed20AP stun, lengthens root and cooldown) and B15 (loses Health drain and changes potency/cadence). Do not silently substitute those mismatched alternatives.
2. **First Blade uses EL04 Ion Lance for pure Pierce.** Vault-Breaker is untyped Pierce100/CD3/range3; EL04 is Lightning Pierce60/CD6/range5. AP60 remains. No exact untyped pure-Pierce action exists in the reviewed global set; EA04 is Wind, and B33 adds IDT as well as Lightning. EL04 is accepted with those element/power/cadence changes. Its AI primary/secondary elements remain unchanged.
3. **Shared substitutes reduce ordinary power and alter cadence.** Most retired attacks have100EP; selected shared ordinary attacks have40–60EP. Guarded/Braced/Sharpened stances go30/35/30%→20/20/20%, with CD5→4 and2r preserved. First Blade Undertow loses40→10AP reduction; Thunderhead IDT20→15%. Fewer redundant attacks also means less cooldown coverage. These are not promises of equal fight difficulty.
4. **Crowned support activation and triggers are approved under RUL007/008.** S35 Second Wind heals strictly below40%, B07 Stolen Form Copies at IDG71+, and Rebounding Form enters regular rotation. Keep the dormant captured profile as a historical control and test the companion's exact ordering/selector candidate separately. Trigger values are closed; runtime validation and measured balance remain pending.
5. **Keep Wayfinder as ranged pressure for this migration.** The captured Redrawn Course has incomplete `increasecooldown` fields, with no proven active cooldown rider. Do not call pure Time Compression B08 an equivalent replacement. Adding real temporal control later is a separate design choice.

## Complete replacement map

Each captured equipped record appears once below. Repeated destinations mean consolidation into one equipped record, not duplicate equipment. Exact IDs and source pointers are in `state/ghost_ship_hybrid_kit_proposal.json`.

### Deck Warden

| Captured move | Accepted disposition |
| --- | --- |
| Guarded Stance | Replace / consolidate into EE03 Stoneward |
| Ghostly Knotted Lash | Replace / consolidate into EW01 Tide Bolt |
| Ghostly Grapeshot Volley | Replace / consolidate into S07 Rapid Fire |
| Braced Stance | Replace / consolidate into EW03 Springguard |
| Ghostly Boarding Hook | Replace / consolidate into S08 Numbing Shot |
| Sharpened Focus | Replace / consolidate into EA03 Windlash Focus |
| Ghostly Cutlass Slash | Replace / consolidate into S02 Quick Strike |
| Ghostly Chain Shot | Replace / consolidate into S07 Rapid Fire |

### Seal Charge

| Captured move | Accepted disposition |
| --- | --- |
| Explosion! | Retain as Core Rupture |

### Core Canister

| Captured move | Accepted disposition |
| --- | --- |
| Explosion! | Retain as Core Rupture |

### Core Horror

| Captured move | Accepted disposition |
| --- | --- |
| Guarded Stance | Replace / consolidate into EE03 Stoneward |
| Ghostly Rigging Snare | Retain as Rigging Snare |
| Ghostly Powder Flash | Replace / consolidate into S08 Numbing Shot |
| Braced Stance | Replace / consolidate into EW03 Springguard |
| Ghostly Strangling Weed | Retain as Hollow Timber |
| Sharpened Focus | Replace / consolidate into EA03 Windlash Focus |
| Ghostly Hull-Crush Coil | Replace / consolidate into S06 Twin Shot |
| Ghostly Tarred Harpoon | Replace / consolidate into S06 Twin Shot |

### Oathkeeper

| Captured move | Accepted disposition |
| --- | --- |
| Guarded Stance | Replace / consolidate into EE03 Stoneward |
| Ghostly Grapeshot Volley | Replace / consolidate into S07 Rapid Fire |
| Sharpened Focus | Replace / consolidate into EA03 Windlash Focus |
| Ghostly Cutlass Slash | Replace / consolidate into S02 Quick Strike |
| Ghostly Measured Verdict | Replace / consolidate into S04 Opening Strike |
| Counter Stance | Retain as Rebounding Form |
| Ghostly Chain Shot | Replace / consolidate into S07 Rapid Fire |
| Ghostly White-Fire Riposte | Replace / consolidate into S02 Quick Strike |

### Wayfinder

| Captured move | Accepted disposition |
| --- | --- |
| Guarded Stance | Replace / consolidate into EE03 Stoneward |
| Ghostly Grapeshot Volley | Replace / consolidate into S07 Rapid Fire |
| Ghostly Chart-Pin Barrage | Replace / consolidate into S06 Twin Shot |
| Braced Stance | Replace / consolidate into EW03 Springguard |
| Sharpened Focus | Replace / consolidate into EA03 Windlash Focus |
| Ghostly Tarred Harpoon | Replace / consolidate into S06 Twin Shot |
| Ghostly Chain Shot | Replace / consolidate into S03 Lunging Strike |
| Ghostly Redrawn Course | Replace / consolidate into S06 Twin Shot |

### Arsenal Keeper

| Captured move | Accepted disposition |
| --- | --- |
| Guarded Stance | Replace / consolidate into EE03 Stoneward |
| Ghostly Powder Flash | Replace / consolidate into S08 Numbing Shot |
| Ghostly Coin-Weight Maul | Replace / consolidate into S01 Heavy Strike |
| Braced Stance | Replace / consolidate into EW03 Springguard |
| Sharpened Focus | Replace / consolidate into EA03 Windlash Focus |
| Ghostly Cutlass Slash | Replace / consolidate into S01 Heavy Strike |
| Ghostly Tarred Harpoon | Replace / consolidate into S06 Twin Shot |
| Ghostly Crossed Out | Retain as Revocation Strike |

### Sentinel

| Captured move | Accepted disposition |
| --- | --- |
| Light Barrier | Keep B39 Light Barrier |
| Guarded Stance | Replace / consolidate into EE03 Stoneward |
| Ghostly Grasp of the Buried | Replace / consolidate into Rigging Snare |
| Ghostly Sand-Choke | Replace / consolidate into Hollow Timber |
| Ghostly Burial Tide | Replace / consolidate into S06 Twin Shot |
| Braced Stance | Replace / consolidate into EW03 Springguard |
| Ghostly Shore-Break | Replace / consolidate into S06 Twin Shot |
| Counter Stance | Retain as Rebounding Form |
| Ghostly Tidal Grave | Replace / consolidate into S06 Twin Shot |

### First Blade

| Captured move | Accepted disposition |
| --- | --- |
| Guarded Stance | Replace / consolidate into EE03 Stoneward |
| Ghostly Undertow Chain | Replace / consolidate into S08 Numbing Shot |
| Braced Stance | Replace / consolidate into EW03 Springguard |
| Ghostly Vault-Breaker | Replace / consolidate into EL04 Ion Lance |
| Battle Trance | Retain as Remembered Form |
| Ghostly Dead Reckoning | Replace / consolidate into S07 Rapid Fire |
| Ghostly Gale Cleaver | Replace / consolidate into S07 Rapid Fire |
| Ghostly Thunderhead Brand | Replace / consolidate into S04 Opening Strike |

### The Captain

| Captured move | Accepted disposition |
| --- | --- |
| Death's Door | Retain as Unbroken Command |
| Worldbreaker Chorus | Keep B17 Worldbreaker Chorus |
| Battle Trance | Retain as Remembered Form |
| Cataclysm Detonation | Keep B14 Cataclysm Detonation |
| Death's Grasp | Retain as Keelbind |

### Crowned Captain

| Captured move | Accepted disposition |
| --- | --- |
| Death's Door | Retain as Unbroken Command |
| Unraveling Strike | Keep S31 Unraveling Strike |
| Ghostly Deep Six | Retain as Suppression Writ |
| Ghostly Shipwreck Delusion | Retain as Ruin Refrain |
| Sharpened Focus | Replace / consolidate into EA03 Windlash Focus |
| Cataclysm Detonation | Keep B14 Cataclysm Detonation |
| Death's Grasp | Retain as Keelbind |
| Second Wind | Keep S35 Second Wind |
| Counter Stance | Retain as Rebounding Form |
| Stolen Form | Keep B07 Stolen Form |
| Ghostly Final Fathom | Retain as Final Command |

## Source and numerical interpretation

- Original full AI kits: `harvests/inbox/tnr_results_1790826836406.json`; profiles: `harvests/inbox/tnr_results_1790828718767.json`. Both are historical October1 evidence. Shared references resolve by pool code against all 82 full October9 records in `harvests/inbox/tnr_results_1791583362574.json`, not only the registry shorthand.
- Each entity carries exact AI/profile pointers and hashes; every original membership has an explicit disposition. Each selected shared record has an ID, full-record pointer/hash and AP/CD/range/method summary. No new jutsu fields or effects arrays are authored.
- Preserve raw stats, pool bases, rank, level, multipliers, regeneration, preferences, AI elements and all innate effect arrays. The crew often carry several large innate IDG entries, including duplicate99r entries and shorter entries. Do not deduplicate them or use an EP ratio as measured final-damage parity.
- EE03/EW03/EA03 names do not create elemental restrictions: their full stance effects have none. Standard S01/S02/S03/S04/S06/S07/S08 damage records omit `generalTypes`; do not normalize it. Their captured chakra/stamina costs remain0.05 each; selected elemental attacks/stances have their own captured costs, often zero. Read full records for all filters and defaults.
- S06 and S07 each contain one Damage tag despite their names. S08 is30% Stun application with10AP reduction for1r, not30AP. B39 has a500-health Shield tag for2r; its power100 is not its shield-health amount.
- The six already-shared IDs differ between October1 embedded records and October9 full records in `statClassification`/`elementClassification`, plus presence/absence of null requirement fields. The complete presence-sensitive field list is recorded in the JSON; absent and null are not silently equated. Their effects arrays match. Use the newer full records in fixtures, document the schema/metadata differences, and do not overwrite current shared records with an older embedded snapshot.
- Root/movement prevention, AP reduction, Clear and Drain are distinct behaviors. The eleven retained records stay mechanically unchanged, including their existing100AP Explosion exception, incomplete/omitted fields, and nested text. This proposal does not convert them to generic40/60AP defaults.
- Retirement means unequipping from these Ghost Ship kits. External consumers and fresh current captures must be checked before any eventual rename or separately authorized deletion.

## Regular Captain comparator and Fable test handoff

The accepted regular-Captain membership is exactly its captured five: Unbroken Command, Remembered Form, Keelbind, B14 Cataclysm Detonation and B17 Worldbreaker Chorus. Keep Level100/JONIN, stats3×, pools2.5×, regeneration60, Bukijutsu/Speed/Strength preferences, null primary/secondary elements and its complete innate effect array. AI Heavy Armor and Cursed Dagger were equipped:NONE; do not include their combat effects without fresh evidence. The old six-move B19/B14/B17/B05/S31/B33 comparator is superseded.

With kit acceptance recorded, Fable must apply these checks to work packageA of `state/prompt_ghost_ship_skyglass_stage2_feasibility.md`:

1. Resolve every selected code/ID to the cited full record. Preserve the eleven retained mechanical records, all original retained/shared memberships and the two explicitly accepted Sentinel additions; never substitute by a similar name.
2. Run both the captured profile baseline and candidate rebuilt rules against the same declared player fixtures. Separate changes caused by membership, corrected range gates, rule priority and newly activated support. Do not call equipped membership a working rotation.
3. Validate action affordability, cooldown coverage, attack/stance usage, idle/fallback turns and survival. Avoid serial40AP stance choices starving attacks. Most buffs activate after the cast round; a same-turn stance+attack is AP capacity, not proof of an immediate damage benefit.
4. Preserve all innate effects in the baseline. Measure real damage, control duration and pool pressure; do not compensate for lower shared EP by silently raising stats or adding IDG rows. Test different defense profiles because retained100EP actions and pooled40–60EP actions coexist.
5. Test the regular Captain's five-move cooldown gaps and ramp usage against Sealwright's approved seven. Report control lockout, win/loss, fight length, damage spikes, buff/shield uptime, Clear frequency and counterplay under the original Stage2 brief. Membership preservation does not establish parity.
6. Test Crowned Captain with the one Sharpened Focus→EA03 replacement and unchanged captured innate IDG60%99r/profile. Separately test proposals activating its dormant heal/copy/reflect support; do not bake activation into the comparator unnoticed.
7. Preserve hazard delayed-use thresholds (>2 and>6) and100AP self-destruct; prove pre-trigger waiting and delayed action behavior offline. Do not interpret display kit ordering as rules.
8. Derive SINGLE attack gates from full-record range+1; SELF and ALL normally take no range gate. Preserve Sealwright B32's separately director-approved distance6 condition and IDG71 threshold, plus regular S31. Its deliberate double Clear is unchanged.

Fable owns rule construction and in-process tests on a separate branch. This packet authorizes no upstream engine modification or full manifest. Current items follow the final-item revalidation brief under RUL006. Crowned support follows the RUL007 companion. Final kit balance, unresolved behavior details and test-driven tuning return to the director.

## Verification boundary

Offline referential checks cover eleven AIs, every historical equipped membership, all eleven retained IDs, all six already-shared IDs, and every selected full pool record. All original retained/shared memberships are preserved; the only new retained memberships are the two accepted Sentinel additions. No duplicate IDs within an accepted kit. This is design/source verification only: no combat execution, runtime validation, live request/write or final rule freeze.

Independent read-only review repeated the source/hash, membership, baseline and presence-sensitive drift checks and found no blocking mapping or preservation defects. This PASS is limited to the proposal's references and stated preservation; it does not approve balance, AI behavior or combat parity.
