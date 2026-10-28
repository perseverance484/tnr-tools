# Skyglass pets: the ship's echoes

Five reward-only companions from the Echo Jar (RUL-2026-10-28-011; loot tables §5b). Story: the Skyglass Project
tested recall on the ship's animals first; their impressions were sealed in jars like Replicant Zero's.

**Status:** kits proposed. The numbers are provisional until the live species and PETS jutsu catalogue is captured; nothing in this repo describes existing species yet.

## Rules every kit follows (engine)
- **Species record:**
  - `isActive: false`: reward-only.
  - Ability slots by rarity: 2 / 3 / 4 / 5 / 6.
  - Ability budget = pet rank + 1. Jutsu cost by rank: D 1 · C 2 · B 3 · A 4 · S 5.
- **Innate skill** (species `effects`):
  - `SELF`: applies to both the owner and the pet.
  - `ENEMIES`: triggers when either of them hits an enemy.
  - No COORDINATES targets.
- **Pet jutsu:**
  - `jutsuType PETS`, no element classification, no weapon.
  - Allowed effects: damage, elementaldamage, heal, shield, increase/decrease stat, increase/decrease damage given or taken, clear, cleanse and move.
  - **Signature jutsu** use `requiredPetSpeciesId`, so the species must exist before its jutsu. Build order: create the species → create the signature jutsu → edit the species defaults.
- **Default loadout:** the signature jutsu, plus existing published PETS jutsu chosen from the live catalogue once it is captured.
- **New content:** five signature jutsu, one per pet. The animations reuse the Skyglass boss FX where noted.

## Kits

### Deck Gull
Common · Support.
- Innate (SELF) **Lookout:** decreasedamagetaken 5%.
- Signature (D) **Gull's Cry:** one enemy, decreasedamagegiven 10% for 1 round.
- Art direction: grey-white sea gull with a faint cyan skyglass sheen at the wingtips; pixel art matching the event bible.
- Rank arc: scrappy deck gull → skyglass-feathered storm gull trailing pale light.
- Story: the gull that never stopped following the ship.

### Bilge Rat
Uncommon · Assault.
- Innate (ENEMIES) **Gnaw:** hit target, increasedamagetaken 5% for 1 round.
- Signature (C) **Bilge Swarm:** damage plus decreasestat (speed) on one enemy.
- Art direction: lean brown rat with a frayed rope collar and skyglass-glinting eyes.
- Rank arc: bilge rat → ghostly rat king crowned with knotted rope.
- Story: the hold was never empty.

### Lantern Moth
Rare · Healer.
- Innate (SELF) **Lastlight:** heal 2% per round.
- Signature (C) **Lantern Glow:** heal plus cleanse on owner or ally.
- Art direction: soft-furred moth whose wings carry a warm lantern glow against cyan skyglass dust.
- Rank arc: small moth circling a lantern → great moth whose wings hold the Lastlight.
- Story: drawn to the Lastlight; it remembers the way home.

### The Ship's Cat
Epic · Support.
- Innate (SELF) **Nine Lives:** decreasedamagetaken 10%, plus a small shield at battle start.
- Signature (B) **Landed on Its Feet:** cleanse plus shield on the owner.
- Art direction: sleek grey ship's cat with a skyglass bell and a white-tipped tail.
- Rank arc: wary ship's cat → serene nine-lives cat walking among faint crew ghosts.
- Story: the only one of the crew who ever walked off the wreck.

### Little Horror
Legendary · Assault.
- Innate (ENEMIES) **Rot Bite:** hit target, poison (small) for 2 rounds.
- Signature (B) **Little Maw:** damage plus increasedamagetaken 10% for 1 round. Animation: the Core Horror's maw strip.
- Art direction: small, oddly cute rot-and-skyglass creature, the Core's bad copy of the ship's mascot.
- Rank arc: oddly loyal blob with one tooth too many → towering skyglass rot-beast, still loyal.
- Story: the Core tried to remember the ship's mascot; this is what came back.

## Pipeline gap (Lane A)
The builder has no pet-species entity and no `requiredPetSpeciesId` jutsu field. `reward_pets` is in the constructors; `reward_pet_experience` (Galley Stores) is not, and must be confirmed against the pinned source.
- **Route 1:** the director enters the five species in the game's Manual from this sheet.
- **Route 2:** builder support is added on a `fable/*` branch, with source-pinned contract regeneration, then independent review.

The jars and chests can't be built until the species ids exist.
