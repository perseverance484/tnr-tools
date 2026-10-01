# Ghost Ship retheme — design brief

**Status:** ACTIVE DESIGN / implementation not yet frozen  
**Lead:** ChatGPT / Content Designer  
**Implementation owner:** Fable / Claude Code after freeze  
**Live-game actor:** dauntless only  
**Evidence baseline:** main after the successful root/dependency/profile captures  
**Machine content source:** `state/ghost_ship_retheme_patch.json` (previous prose baseline; not implementation-ready under the current revisions)

**Current revision, 2026-10-01:** RUL-2026-10-01-005 establishes complete chakra echoes; RUL-2026-10-01-006 fixes the post-mission attack, Skyglass critical incident, suppressed loss and fragmented memory continuity. RUL-2026-10-01-007 calls for a crystal-powered ship visualization and a simple narrative within existing roles. The lost-original-crew / failed-preservation-seal explanation in `state/ghost_ship_skyglass_mechanism.md` is a proposal. Reconcile the machine patch before implementation freeze. The locked ship, elite duties and names remain unchanged.

## Objective

Retheme the two live Ghost Ship profession quests away from literal ghost pirates and toward a TNR-native lost-shinobi-warship legend, while preserving the existing 57-node adventure graph, profession reward structure, combat tuning and AI behavior.

The Ghost Ship remains the public name because the vessel should not exist. It vanished decades ago and periodically reappears where no ship belongs, held aloft by a chakra-reactive crystal core and a hull-wide seal network.

## Core fiction

The vessel was an experimental shinobi warship built around a chakra-reactive **Skyglass Core**. Seal arrays through the keel distributed chakra, reduced effective weight and allowed the ship to ignore terrain entirely. It was designed to cross mountains, walls and defended coastlines, appearing from directions ordinary military planning could not cover.

The project was top secret. Every person aboard when it vanished was a high-level operative selected for a specialist military duty. Deck security, navigation, stores and engineering were elite assignments. Present-day reconstruction quality does not define the original operative's standing.

The ship was attacked after a mission and Skyglass went critical. Its military sponsors believed it destroyed and suppressed the project. The public legend contains sightings and contradictory rumors, not a complete account of classified engineering. The ship periodically materializes, follows fragments of old routes and disappears again.

Skyglass originally powered flight and sustained the crew's vitals. Its preservation function now continues beyond its intended limits, repeatedly forming complete chakra echoes from impressions ingrained in the ship. They pilot the vessel, maintain its arrays and perform their remembered duties. Their connection to the ship prevents ordinary independent lives ashore; the exact binding mechanism is proposed in the researched brief. The art need not settle the original people's ultimate fate.

Identity, training and habitual duty remain strong, while experiences between manifestations are sparse, disordered and hard to place. Some echoes recognize that decades have passed from changed geography, records or lingering impressions, yet cannot reliably distinguish one incarnation from another. Greater coherence does not grant a perfect elapsed-time count or uninterrupted memory. This supersedes that implication in the preceding draft.

The continuing emergency, rather than a necessarily unfinished combat objective, is the narrative focus. Proposed explanation: the originals perished, but a damaged preservation seal still forms their chakra echoes and leaves the ship intermittently absent from ordinary space. This fits a completed mission followed by an attack. Keep the cause brief; no external release-key quest, elaborate individual memory subplot or literal time travel is required. The precise mechanism and original crew's death await approval.

The vessel remains a military threat: it bypasses terrain, carries high-level operatives and can summon defenders again. The proposed explanation preserves the actual hull and stores between appearances, while only the crew constructs are re-formed. Its fiction does not add infinite healing, instant respawns or new mechanics to the shared AI kits.

The **Skyglass Crown** remains the Captain's command interface. The Captain is one of the most coherent echoes, and the oathbound route brings forth the most complete command impression. Proposed reveal: the Crown restores clarity about the critical incident and final preservation order, while his memory of the intervening manifestations remains fractured.

The broad tragedy can evoke the classic fantasy idea of immortality without mortal life, but the actual explanation, characters, reveals and dialogue remain original to TNR and rooted in forbidden shinobi engineering.

## Narrative reveal cadence

The story should be discovered rather than delivered as an opening exposition dump.

1. **Arrival:** the ship materializes without approach. Seal-light under the keel immediately establishes that this is an impossible piece of engineering, not a normal haunted vessel.
2. **Gangplank:** the Deck Warden is a complete, unaged operative in archaic specialist equipment whose chakra tint and spectral contour reveal his summoned nature.
3. **Lower hull:** the Core Horror shows an engineer's complete echo overwhelmed by unstable resonance, with overlapping contours and excessive chakra presence. This replaces the previous body/hull-fusion reveal.
4. **Parley:** the Oathkeeper recognizes the difference between the living and the crew. His response to the time riddle conveys awareness of elapsed years without a reliable count or sequence.
5. **Wayfinder:** continues navigating remembered routes. Charts serve their existing quest purpose; no handwriting mystery or personal memory investigation is needed.
6. **Arsenal Keeper:** guards the existing stores under remembered orders. Keep the military duty readable without adding a personal backstory.
7. **First Blade:** a powerful operative retains the feeling of long repetition without an exact memory of it. His excitement at a living challenger makes that loss personal.
8. **The Captain:** the player learns that the ship did not simply survive destruction. Skyglass rejected the loss condition and kept executing its preservation orders.
9. **Crowned Captain:** the Skyglass Crown restores the deepest command memory. The final reveal concerns the damaged preservation seal still calling the crew to duty after the critical incident. The original mission may already have finished; no new release mechanic is required.

The three entry routes therefore show three different sides of the same mystery:
- direct assault shows the military machine still defending itself;
- hull infiltration shows the danger of unstable resonance;
- parley shows the remaining humanity of the afterimages.

The three interior routes continue that pattern:
- Wayfinder reveals impossible history;
- Arsenal Keeper reveals a life of endless routine without mortal need;
- the helm reveals the actual Skyglass failure and the Captain's role in it.

## Scope

In scope:
- quest names, descriptions, success text and all 57 objective descriptions/choice labels for both Gather and Hunt;
- 11 direct Ghost Ship AI display names;
- shared AI-pool migration per `state/ghost_ship_shared_pool_migration.json`; the earlier bespoke jutsu retheme is superseded;
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

## Approved short names and record mapping

The names, slots and specialist duties below remain approved. Their visual presentation is under the complete-echo revision in `state/ghost_ship_crew_direction.md`; combat tuning and the shared kits are unchanged.

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
- elite personnel of a classified military project, with specialized fitted armor, protected seal instruments, masks and purpose-built weapons;
- no tricorns, skull-and-crossbones, pirate coats or treasure-pageantry;
- chakra nature must be visually central: complete figures with a cool spectral tint, controlled pale aura and optional displaced contour; bodily gaps and hollow anatomy are retired from the direction;
- the closer an impression is to the Captain's core memory, the steadier and more coherent its presentation;
- Crowned Captain is the most stable and visually authoritative reconstruction.

The exact ship design is locked by RUL-2026-10-01-002; `state/ghost_ship_art_production.md` points to its preserved source. Deck Warden `_b` was approved under the prior brief; preserve its bytes and approval history but hold it pending a complete-echo revision. Oathkeeper `_b` is superseded as a current candidate. See RUL-2026-10-01-005 and the crew brief for the current direction and proposed effect.

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
2. Art audit/production in separate context-safe packets, one image with QC and user acceptance at a time:
   - quest icon first, then Deck Warden avatar prototype;
   - remaining combat avatars/props;
   - scene portraits from locked identities and scene backgrounds;
   - Skyglass reward item icons as needed.
   No bespoke 29-jutsu icon set. See `state/ghost_ship_art_production.md` and `state/workstreams/ghost_ship_art/roadmap.json`.
3. Freeze a Fable implementation brief from the approved patch + accepted art.
4. Fable builds full-record edit manifest(s), preserving ids/mechanics and applying loot corrections.
5. ChatGPT independently reviews the exact frozen implementation SHA/manifest.
6. User alone executes hidden/live changes and returns readback.
7. Readback audit before any publish/final acceptance decision.

## Serum naming

Director-approved 2026-10-01: **Skyglass Serum** replaces `Dead Man's Draught`. The unaccepted Stillwater Tonic proposal is superseded. Preserve the existing item id and mechanics; use Skyglass Serum in art direction, planning and player-facing text. See RUL-2026-10-01-001.

The shared-pool migration and Skyglass Crown naming are director-approved.
