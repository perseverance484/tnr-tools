# Skyglass pets: the ship's echoes

**Update (RUL-2026-10-29-047):** the event ships **one pet, the Little Horror**, from a once-per-player Wreck jar. The Deck Gull, Bilge Rat, Lantern Moth and Ship's Cat kits below are cut. They are kept here only as design history.

Five reward-only companions from the Echo Jar (RUL-2026-10-28-011; loot tables §5b). Story: the Skyglass Project
tested recall on the ship's animals first; their impressions were sealed in jars like Replicant Zero's.

**Status:** kits approved as proposed (RUL-2026-10-28-012). The catalogue was captured by push/345 (69 species, 4 PETS jutsu); the Little Horror's numbers are final (RUL-2026-10-31-068). The cut kits below were never finalised.

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
Legendary · Assault. **Numbers final (RUL-2026-10-31-068);** built by push/346 (`push/skyglass_pet.gen.py`), defaults by push/347. Effect rows are shaped exactly like the live legendary species' rows in the push/345 capture (`tnr_results_1793460185610.json`); the jutsu record is the Yamabiko's Rallying Echo with these numbers.
- `isActive: false` (reward-only; granted by The Little Horror's Jar). Description: `The Core tried to remember the ship's mascot. This is what came back: a small, damp thing with one tooth too many, and it has decided you are its crew.`
- Innate (ENEMIES) **Rot Bite:** enemies deal **10% less damage** (`decreasedamagegiven` 10%, 30 rounds, shaped like the Dragon's enemy-facing `increasedamagetaken` row; RUL-2026-10-31-070). An ENEMIES innate is applied once at battle start to every enemy (`libs/combat/pets.ts`). Pets fight only in quest battles (chart runs, the Haul), not the Wreck dungeon or PvP.
- Innate (SELF) **Hungry:** `increasedamagegiven` 20% for 30 rounds, shaped like the Kitsune's 30% row; applies to the owner and the pet.
- Signature (D) **Little Maw:** PETS, locked to the Little Horror; STUDENT / level 1; one opponent, range 4, cooldown 5, 60 AP, no pool costs. `damage` power 50 (formula, `generalTypes` [Highest], no `statTypes`, as Rallying Echo), then `increasedamagetaken` 10% for 1 round on the target. Animation: the Core Horror's maw strip, once uploaded (empty until then).
  - Description: `The Little Horror opens a mouth far too big for its body and bites, leaving the target easier to hurt for a round.`
  - Battle text: `%user opens a maw far too big for its body and bites down on %target.`
- Default loadout: Little Maw (push/347, after the director publishes it).
- **The Little Horror's Jar:** Legendary consumable, untradeable, `preventBattleUsage`, one `noncombatconsumereward` with `reward_pets` = the Little Horror; text `SKYGLASS_TEXT.md` `item:The Little Horror's Jar.description`.
- Art direction: small, oddly cute rot-and-skyglass creature, the Core's bad copy of the ship's mascot.
- Rank arc: oddly loyal blob with one tooth too many → towering skyglass rot-beast, still loyal.
- **`rankConcepts`** (canonical; director-approved, RUL-2026-10-31-064 item 6). Verbatim, ranks 1-10:
  1. Companion: `A palm-sized blob of dark, wet rot with big round eyes and one tooth too many, a tarnished brass bell on a frayed rope collar, sitting in a puddle of bilge water`
  2. Scout: `A small rot blob grown four stubby legs and a lopsided grin of too many teeth, flecks of cloudy skyglass in its skin, the brass bell on its rope collar`
  3. Tracker: `A dog-sized rot creature with a ragged rope-like tail and a wide toothy mouth, small barnacle clusters of cloudy skyglass along its back`
  4. Guardian: `A hound-sized rot beast with damp, timber-dark hide and a crest of cloudy skyglass shards down its spine, sitting like a loyal dog, bell at its neck`
  5. Hunter: `A lean rot beast on four powerful legs, ribs of old ship timber showing through, a maw that splits too wide, skyglass shards on its shoulders`
  6. Warden: `A large rot beast collared in scraps of rope and sailcloth, its mouth ringed with skyglass teeth, the brass bell now small against its throat`
  7. Sentinel: `A horse-sized rot beast whose back has grown a ridge of clear skyglass crystal, a second, smaller maw on its chest, eyes still big and devoted`
  8. Mythic: `A towering rot beast of wet timber and tar-black rope, rows of skyglass spines, a half-open maw in its chest, crouched protectively`
  9. Sovereign: `A huge skyglass rot-beast with a cracked ship's figurehead fused into its brow, barnacled rot armour, the old bell still on its rope collar`
  10. Celestial: `A colossal skyglass rot-beast, its body clouded crystal over dark rot, a maw full of crystal teeth, the tiny brass bell still at its neck, still loyal`
- Story: the Core tried to remember the ship's mascot; this is what came back.

## Pipeline (Lane A)
Pet species are built through the builder, not hand-entered (RUL-2026-10-28-012). Builder support for the pet-species
entity and the PETS jutsu `requiredPetSpeciesId` field is on `fable/pet-species-builder`, under independent review; the
Forge bundle budget was raised for it (RUL-2026-10-28-014). Galley Stores uses `reward_pet_experience`, which the pinned
source has (theninjarpg@2af4b320 `validators/rewards.ts`:54).

The jars and chests can't be built until the species ids exist.
