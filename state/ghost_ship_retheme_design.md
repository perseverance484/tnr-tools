# Ghost Ship retheme — design brief

**Status:** ACTIVE DESIGN / implementation not yet frozen  
**Lead:** ChatGPT / Content Designer  
**Implementation owner:** Fable / Claude Code after freeze  
**Live-game actor:** dauntless only  
**Evidence baseline:** main after the successful root/dependency/profile captures  
**Machine content source:** `state/ghost_ship_retheme_patch.json`

## Objective

Retheme the two live Ghost Ship profession quests away from literal ghost pirates and toward a TNR-native lost-shinobi-warship legend, while preserving the existing 57-node adventure graph, profession reward structure, combat tuning and AI behavior.

The Ghost Ship remains the public name because the vessel should not exist. It vanished decades ago and periodically reappears where no ship belongs, held aloft by a chakra-reactive crystal core and a hull-wide seal network.

## Core fiction

The vessel was an experimental shinobi warship built around a chakra-reactive **Skyglass Core**. Seal arrays through the keel distribute chakra, reduce effective weight and hold the ship aloft. The project and its crew vanished, leaving the ship as folklore.

The Core retains chakra impressions of the crew rather than literal souls. When the vessel reappears, the seal network reconstructs those impressions into temporary physical bodies. Player-facing UI uses short names; prose and art carry the echo/reconstruction explanation.

The White Crown was the Captain's command interface with the ship. It synchronized one shinobi with navigation, defensive seals, weapons and crew-impression systems. The strongest stored reconstruction is the Captain at full Crown synchronization.

## Scope

In scope:
- quest names, descriptions, success text and all 57 objective descriptions/choice labels for both Gather and Hunt;
- 11 direct Ghost Ship AI display names;
- 29 Ghost Ship-specific AI jutsu names/descriptions/battle text;
- Ghost Ship scene-asset display names and replacement-art direction;
- themed reward lore;
- White Crown reward-loop correction;
- top-level quest scene-background repair;
- AI loot-safety correction.

Out of scope:
- The Drowned Fleet battle pyramid;
- generic/shared combat jutsu used by the Captain or crew;
- balance changes beyond the explicitly approved loot corrections;
- publishing/unhiding;
- live execution by ChatGPT or Fable.

## Final short roster

| Live id | Current | Retheme |
|---|---|---|
| `texZaFi42S3EvJZBwQ8cd` | Ghostly Bosun | **Deck Warden** |
| `wTgO-Q32caSSd0is1QIS7` | Crate of Explosives | **Seal Charge** |
| `frc9LTxqQlM7mncG4VZGK` | Barrel of Explosives | **Core Canister** |
| `AQi-bHJ-5tHXtxrnc0P9E` | Ghostly Bilge Horror | **Core Horror** |
| `0PZU_FvlbM3ErYGlD5r56` | Ghostly Herald | **Oathkeeper** |
| `v7T9_XdGMfP46em0dPuBc` | Ghostly Navigator | **Wayfinder** |
| `2OXJEXoktxJcjqMkE851g` | Ghostly Quartermaster | **Arsenal Keeper** |
| `3V_gdHYaclMB1gTyOPAbV` | Ghostly Guardian | **Sentinel** |
| `d6g0mOM7RBSsYI1hrUVT9` | Ghostly First Mate | **First Blade** |
| `QY69h271Nx9uHrBeR6jwW` | Pirate King | **The Captain** |
| `fDU9jCPZtH7YHbdQPO9RF` | Ghostly Pirate King | **Crowned Captain** |

No exact collisions for these proposed names were present in the current repository AI-name catalog when checked.

## Quest identity

- `6Ri-W5TtUrEMWpyYlnf_F` -> **Ghost Ship (Gather)**
- `HckXVOf-qk6ESU9t5rxLh` -> **Ghost Ship (Hunt)**

The adventure remains structurally identical between professions. Gather/Hunt keep their profession-specific chest rewards and location fields.

Five endings remain:
1. hidden shore cache;
2. accessible hold supplies;
3. restricted vault;
4. direct Captain route;
5. oathbound Crowned Captain route.

## White Crown reward contract

Director-approved reward rule:
- **Fragment of the White Crown**: 20% AI drop from Crowned Captain only;
- remove the existing 10% `w_Co` quest-completion fragment roll from both quests;
- five fragments build **The White Crown**;
- The White Crown is not a direct AI drop;
- AI Heavy Armor and Cursed Dagger: 0% drop chance on both Captain AIs;
- explosive-prop Heavy Armor is already 0% and stays 0%;
- **Ghostly Sovereign's Diadem** is legacy debris, not the intended reward. Remove it from Crowned Captain attachments; leave the hidden standalone record otherwise untouched unless separately approved.

Captured White Crown mechanics remain unchanged:
- Legendary HEAD armor;
- 5% decreased damage taken;
- 20% increased damage given;
- 30-round effects;
- two imbue slots;
- craftable, tradable, PVE.

## Jutsu policy

The 29 Ghost Ship-specific jutsu keep their live ids and mechanics. Their names/descriptions/battle text change according to `state/ghost_ship_retheme_patch.json`.

Generic/shared jutsu such as Guarded Stance, Braced Stance, Counter Stance, Battle Trance, Death's Door, Death's Grasp, Worldbreaker Chorus, Cataclysm Detonation, Unraveling Strike, Second Wind and Stolen Form are not renamed as part of this retheme.

Because ids remain stable, captured AI profile rules can remain mechanically identical.

## Prose policy

`state/ghost_ship_retheme_patch.json` contains replacement text for all 57 objective ids. Implementation must:
- preserve every objective id, task, next/fail/reset edge and opponent block;
- preserve Gather/Hunt location/sector differences;
- preserve all profession chest reward arrays except the approved White Crown-fragment removal;
- use no em dash or en dash in player-facing text;
- reproduce the complete live quest record when editing.

The new prose explains the crew as Core reconstructions without repeating "Echo" or "Ghostly" in UI labels.

## Art direction

The ship is an ancient experimental shinobi warship, not a pirate vessel:
- dark timber reinforced by metal ribs and seal plates;
- glowing seal channels along the keel;
- visible Skyglass crystal structures and suspended seal rings;
- chakra-conductive rigging;
- large seal patterns on sails;
- air distortion beneath the hull;
- loose debris/crystal fragments affected by the lift field.

Crew presentation:
- shinobi field clothing, armor plates, utility harnesses, masks, weapons and seal tags;
- no tricorns, skull-and-crossbones, pirate coats or treasure-pageantry;
- reconstructed crew may show pale seal-script, fractured edges, double-images and incomplete sections resolving into chakra;
- the closer an impression is to the Captain's core memory, the more solid it appears;
- Crowned Captain is the most stable and visually authoritative reconstruction.

Existing asset ids should be reused where practical and their names/images updated, so quest wiring remains stable. The art task should audit each current image before deciding reuse vs regeneration.

## Scene identity

Directly wired scene assets become:
- Ghost Ship Deck;
- Ghost Ship Lower Hull;
- Ghost Ship Chart Room;
- Ghost Ship Hold;
- Ghost Ship Helm;
- Ghost Ship Cache Site;
- Oathkeeper Portrait;
- Captain Portrait;
- Crowned Captain Portrait.

The generic Blank Scene Character stays unchanged.

Both quests currently have an empty top-level `content.sceneBackground`. The final edit must set a deliberate global scene rather than reproducing the blank live state.

## Evidence

Fresh successful captures:
- `harvests/inbox/tnr_results_1790826101573.json` — both profession quests + Drowned Fleet comparison;
- `harvests/inbox/tnr_results_1790826836406.json` — direct Ghost Ship AI/assets/items;
- `harvests/inbox/tnr_results_1790828718767.json` — all 11 AI behavior profiles + intended White Crown record.

## Next production sequence

1. Director review of the exact machine patch and any final naming/lore adjustments.
2. Art audit/production in separate context-safe packets:
   - combat avatars/props;
   - scene backgrounds/portraits;
   - quest/item icons;
   - jutsu icons only where old visuals materially conflict.
3. Freeze a Fable implementation brief from the approved patch + accepted art.
4. Fable builds full-record edit manifest(s), preserving ids/mechanics and applying loot corrections.
5. ChatGPT independently reviews the exact frozen implementation SHA/manifest.
6. User alone executes hidden/live changes and returns readback.
7. Readback audit before any publish/final acceptance decision.

## Open content decision

`Dead Man's Draught` is the remaining overt pirate-era reward name. The patch proposes **Stillwater Tonic** with TNR-native restorative lore. This is not yet treated as director-approved until explicitly accepted or replaced.
