# Silent Bastion — art shotlist and brief (CANDIDATE)

**Status: BRIEF ONLY.** No binaries are produced or committed (RUL-2026-09-20-003, binaries uncommitted). The director owns art direction and acceptance. Generation and processing follow `skills/producing-tnr-art` and the isolated art-studio protocol on main.

**Continuity rules:**

- The Bastion is the Skyglass Project's mountain HQ. Its palette is Skyglass blue-white crystal, mountain stone and military brass.
- The staff are **reconstructed chakra impressions**: luminous seams, slight translucency, flicker. They are **never undead**: no rot, no bones, no grave imagery.
- **Never show The Gatewarden or Garrison Marshal.** The Gatewarden is removed from this Pyramid, and earlier posters showing him are outdated.
- **No exterior defenders.** The gate shots are empty.
- **Protect the ending.** No art may depict the unknown issuer of the final order.

## 1. AI avatars — 20

| Slot | Name | Look (from design/regulars.json · commanders) |
| --- | --- | --- |
| D2.REG1 | Bastion Proving Proctor | Reconstructed armory proctor, faded Skyglass grey drill uniform, chakra-glow seams, clipboard of stamped trials, dual practice blades |
| D2.REG2 | Ordnance Quartermaster | Scorched apron over a Skyglass officer coat, satchels of glowing sealed tags, soot-dark gloves |
| D2.REG3 | Prototype Lancer Unit | Half-built lightning-lance automaton fused with a test pilot, exposed capacitor coils, serial plate 03 |
| D2.REG4 | Calibration Duelist | Calibration harness, chakra-measuring rings on both arms, wind-swept practice sword, apprentice insignia |
| D2.BOSS | Master of Arms | Forge-wall weapons master in heavy Skyglass armour; offensive combo identity; two drawn blades |
| D3.REG1 | Skyglass Archive Keeper | Archivist rendered in pale blue chakra light, Skyglass core ledger, translucent where the reconstruction is incomplete |
| D3.REG2 | Impression Containment Warden | Sealed containment suit, water-filled observation visor, chain of vat keys |
| D3.REG3 | Unstable Echo Subject | Failed reconstruction glitching between two silhouettes, shadow chakra leaking, tag "IX" |
| D3.REG4 | Failed Reconstruction Prototype | Hulking earth-bound prototype, crystal growths over a half-formed body, reconstruction rig bolted to its back |
| D3.BOSS | Replicant Zero | Scientist in a lab coat rebuilding his own hand from light; the first successful subject; calm and curious |
| D4.REG1 | Command Signal Adjutant | Relay headset, wind-banner semaphore flags, High Command rank stripes |
| D4.REG2 | High Command Staff Tactician | Campaign maps on a field desk, quill of chakra ink, aide's cord of the Grand Marshal |
| D4.REG3 | Honor Guard Commandant | Ceremonial stone-plated armour, tower shield with the High Command seal |
| D4.REG4 | Strategist's Aide-de-Camp | Sealed dispatch tubes crackling with lightning, reflective lacquered armour, aide's sash |
| D4.BOSS | The Grand Marshal ("The Second") | Senior officer in an unadorned greatcoat; thoughtful and severe; the deputy who could question orders |
| D5.REG1 | Sanctum Vanguard | Obsidian-and-ember Sanctum armour, fire-chakra gauntlets, banner of the Supreme Command |
| D5.REG2 | Directive Herald | Long ceremonial robes, a glowing directive scroll that rewrites itself, lightning-lit eyes |
| D5.REG3 | Last Watch Executor | Tattered night-watch cloak, twin wind glaives, mask stamped with an unreadable order |
| D5.REG4 | Order-Bearer of the Sanctum | Deep-water Sanctum regalia, sealed scroll case, blank unsigned command seal |
| D5.BOSS | Supreme Commander Arakane | Dignified, ruthlessly pragmatic commander at a summit window; command seal (Countermand) at his belt |

## 2. Scenes — backgrounds and characters

| Asset | Used by | Brief |
| --- | --- | --- |
| Bastion exterior gate | `d2.n.f1` | Snow-drifted parade ground and an open gate in a mountain wall; no people, no banners; dead silence |
| Experimental Armory | Division I dialogs | Lit weapon racks behind glass, trial range, forge wall |
| Skyglass Research — archive and vat halls | Division II dialogs | Crystal-core shelves, tall Skyglass lamp, specimen tanks |
| High Command | Division III dialogs | Map room, relay board, war-council table set for no one |
| Command Sanctum | Division IV dialogs | Obsidian and ember light, throne room with a summit window |
| Aftermath — signal room | `d.aftermath` | Relay board printing a new order onto the Supreme Commander's paper; **the issuer is not shown** |
| Scene characters | dialogs | Re-use the 20 avatars. A *visible* save needs `sceneCharacters` (C99 E7 note); the compiled candidate is hidden and leaves them empty |

## 3. Item and jutsu icons

| Asset | Status |
| --- | --- |
| Skyglass Signal Beacon (item icon) | New item; no committed capture found. A warm Skyglass signal lamp |
| Countermand (boss-only item) | Approved identity; icon optional (AI-only, never dropped: `dropChancePerc 0`) |
| Bastion Arsenal Cache / Bastion Research Cache | Names provisional; icons after the director approves the cache identities |
| The Last Directive (exclusive jutsu) | Approved name; icon in the BBE jutsu-icon register style |
| Extermination Order (exclusive jutsu) | **Name not approved**; icon waits for the name |
