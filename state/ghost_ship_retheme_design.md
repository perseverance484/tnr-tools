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

The vessel was an experimental shinobi warship built around a chakra-reactive **Skyglass Core**. Seal arrays through the keel distributed chakra, reduced effective weight and allowed the ship to ignore terrain entirely. It was designed to cross mountains, walls and defended coastlines, appearing from directions ordinary military planning could not cover.

Official records say the project was destroyed decades ago. The Ghost Ship is called a ghost because it should not exist. It periodically materializes in the sky with no visible approach, follows fragments of old routes, then slips out of the world again.

The project failed through a preservation system that worked too well. During catastrophic damage, the Skyglass emergency lattice was ordered to preserve command continuity, preserve crew function and keep the vessel operational until its mission ended. The mission never reached a termination state.

The Core did not preserve living bodies. It preserved chakra impressions: combat habits, memories, personalities, routines and enough physical pattern to rebuild temporary bodies. When the ship reappears, it reconstructs its crew as afterimages from those stored patterns.

This is the TNR version of an immortality curse without literal undeath. The crew do not age because they are not biologically living. They remember food, warmth, sleep, shore leave and ordinary human pleasures, but the ship reconstructs them for duty rather than life. Some afterimages follow routine without fully understanding what happened. Higher-fidelity impressions know exactly how much time has passed and what they have become.

That condition also explains why the vessel was such a menace. A defender could be defeated and simply appear again the next time the Core rebuilt the ship. The crew could operate indefinitely without sleep or supplies, while the vessel itself could bypass the geography that normally protects settlements and strongholds.

The **Skyglass Crown** was the Captain's command interface with Skyglass. It synchronized one shinobi with navigation, defensive seals, weapons, lift systems and crew-impression control. The ordinary Captain is already one of the Core's most stable reconstructions. The oathbound route causes Skyglass to rebuild the highest-fidelity command imprint through the Skyglass Crown, producing the Crowned Captain, who remembers the final project orders and understands why the ship never stopped.

The broad tragedy can evoke the classic fantasy idea of immortality without mortal life, but the actual explanation, characters, reveals and dialogue remain original to TNR and rooted in forbidden shinobi engineering.

## Narrative reveal cadence

The story should be discovered rather than delivered as an opening exposition dump.

1. **Arrival:** the ship materializes without approach. Seal-light under the keel immediately establishes that this is an impossible piece of engineering, not a normal haunted vessel.
2. **Gangplank:** the Deck Warden has a young face and a uniform generations out of date. The first hint is that the crew did not simply survive normally.
3. **Lower hull:** the Core Horror shows that Skyglass can reconstruct a crew pattern incorrectly, using damaged timber, cable and leaked chakra to fill missing information.
4. **Parley:** the Oathkeeper recognizes the difference between the living and the crew. His answer to the time riddle makes clear that he knows decades have passed.
5. **Wayfinder:** charts contain decades of corrections, including settlements and routes that did not exist when the ship vanished. The Ghost Ship has been traveling for far longer than its official history allows.
6. **Arsenal Keeper:** food, medicine and stores remain untouched while inventory has been checked again and again. The crew remembers the need for supplies but no longer consumes them.
7. **First Blade:** one of the strongest crew impressions has spent decades waiting for something genuinely new to happen. His excitement at a living challenger makes the cost of endless reconstruction personal.
8. **The Captain:** the player learns that the ship did not simply survive destruction. Skyglass rejected the loss condition and kept executing its preservation orders.
9. **Crowned Captain:** the Skyglass Crown restores the deepest command memory. The final reveal is that the original mission never ended in the Core's logic, so vessel, Captain and crew are still being rebuilt to complete an order that no living shinobi remembers.

The three entry routes therefore show three different sides of the same mystery:
- direct assault shows the military machine still defending itself;
- hull infiltration shows the horror of damaged reconstruction;
- parley shows the remaining humanity of the afterimages.

The three interior routes continue that pattern:
- Wayfinder reveals impossible history;
- Arsenal Keeper reveals a life of endless routine without mortal need;
- the helm reveals the actual Skyglass failure and the Captain's role in it.

## Scope

In scope:
- quest names, descriptions, success text and all 57 objective descriptions/choice labels for both Gather and Hunt;
- 11 direct Ghost Ship AI display names;
- 29 Ghost Ship-specific AI jutsu names/descriptions/battle text;
- Ghost Ship scene-asset display names and replacement-art direction;
- themed reward lore;
- Skyglass Crown reward-loop correction;
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

## Skyglass Crown reward contract

Director-approved reward rule:
- **Fragment of the Skyglass Crown**: 20% AI drop from Crowned Captain only;
- remove the existing 10% `w_Co` quest-completion fragment roll from both quests;
- five fragments build **The Skyglass Crown**;
- The Skyglass Crown is not a direct AI drop;
- AI Heavy Armor and Cursed Dagger: 0% drop chance on both Captain AIs;
- explosive-prop Heavy Armor is already 0% and stays 0%;
- **Ghostly Sovereign's Diadem** is legacy debris, not the intended reward. Remove it from Crowned Captain attachments; leave the hidden standalone record otherwise untouched unless separately approved.

Captured Skyglass Crown mechanics remain unchanged:
- Legendary HEAD armor;
- 5% decreased damage taken;
- 20% increased damage given;
- 30-round effects;
- two imbue slots;
- craftable, tradable, PVE.

## Shared AI-pool migration

The earlier plan to retheme 29 bespoke Ghost Ship jutsu is **superseded**.

Ghost Ship combatants move onto the current shared AI jutsu pool according to `state/ghost_ship_shared_pool_migration.json`. Existing level, rank, stat ratios, stat/pool multipliers, regeneration and preferred-stat/general values remain unchanged for the initial migration. Combat identity comes from new shared-pool kits and rebuilt AI profiles.

Approved kit direction:
- Deck Warden: close-pressure shared standard kit.
- Core Horror: drain/control bruiser.
- Oathkeeper: technical duelist.
- Wayfinder: ranged control.
- Arsenal Keeper: heavy bruiser.
- Sentinel: earth defense/controller.
- First Blade: Air-pool skirmisher.
- The Captain: six-jutsu shared boss kit.
- Crowned Captain: six-jutsu Sovereign/command boss kit.

The two hazard props keep their delayed self-destruct behavior through one new **shared-pool** signature, **Core Rupture**, cloned mechanically from the captured legacy `Explosion!` record but created as a new shared record so unknown external consumers of the legacy jutsu are not silently renamed.

All 37 legacy-only jutsu found on the captured Ghost Ship roster become **retirement candidates**, not deletion targets. The retheme only unequips them. A later dependency audit must prove a record has no remaining consumers before deletion.

AI behavior profiles are rebuilt against the new kits with current range-gating doctrine. The operative exact kit/rule map is `state/ghost_ship_shared_pool_migration.json`.


## Prose policy

`state/ghost_ship_retheme_patch.json` contains replacement text for all 57 objective ids. Implementation must:
- preserve every objective id, task, next/fail/reset edge and opponent block;
- preserve Gather/Hunt location/sector differences;
- preserve all profession chest reward arrays except the approved Skyglass Crown-fragment removal;
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

## Crown naming

The live records keep their ids but are renamed:
- `ayiRmSjWs05lMPyL3G-1d`: **Fragment of the White Crown** -> **Fragment of the Skyglass Crown**
- `yTS9TSpr_QLnh_3zmEpGg`: **The White Crown** -> **The Skyglass Crown**

This makes the reward loop explicitly part of the forbidden-engineering story rather than leftover pirate mythology. The Crown remains the Captain's command interface with the Skyglass Core and keeps all captured mechanics unchanged.

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
- `harvests/inbox/tnr_results_1790828718767.json` — all 11 AI behavior profiles + intended Skyglass Crown record.

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

`Dead Man's Draught` is the remaining overt pirate-era reward name. The patch proposes **Stillwater Tonic** with TNR-native restorative lore. This remains open until explicitly accepted or replaced.

The shared-pool migration and Skyglass Crown naming are director-approved.
