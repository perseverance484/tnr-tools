# TNR Pets — Source-Seeded Species Roster & First Art Pilot

**Status:** Research roster and exploratory plan, NOT verified live catalogue or approved art.  
**Game evidence:** `studie-tech/TheNinjaRPG@19e2010f9cd3f9be26fff96cca0bf6dece322f11`, `app/drizzle/migrations/0090_pet_companions.sql` (read-only).  
**Tracked:** 2026-10-20. **Source insert rows:** 67 = 30 Common + 18 Uncommon + 9 Rare + 7 Epic + 3 Legendary.

## Evidence limits and availability

All 67 records were inserted by the game's `0090_pet_companions` migration, and `PetSpecies.isActive` defaults to `true`. Source search found no second `INSERT INTO PetSpecies` seed. **This is the full source-seeded roster, not proof that all 67 are currently active, unchanged or the entire live species population.** Staff can add/edit/retire species through `petSpecies.create/update`; `petSpecies.getAll` includes inactive species. The owner-facing daily list samples active species using rarity weights, so not every species appears for everyone every day. A current read-only `petSpecies.getAll` capture is needed for exact live availability. No live requests or writes were made to prepare this roster.

## Exact source-seeded identities

| Species ID | Species | Rarity | Seed appearance description |
| --- | --- | --- | --- |
| `pet-species-0` | Fox | RARE | A nimble fox with a bushy tail and pointed ears |
| `pet-species-1` | Wolf | EPIC | A compact wolf with thick fur and an alert muzzle |
| `pet-species-2` | Hound | RARE | A loyal shinobi hound with floppy ears |
| `pet-species-3` | Cat | COMMON | A graceful cat with expressive eyes and a long tail |
| `pet-species-4` | Lynx | RARE | A tuft-eared lynx with a short tail |
| `pet-species-5` | Tiger | EPIC | A small tiger with bold stripes and broad paws |
| `pet-species-6` | Leopard | EPIC | A lithe spotted leopard with a long tail |
| `pet-species-7` | Lion | EPIC | A proud young lion with a modest mane |
| `pet-species-8` | Panther | EPIC | A sleek panther with rounded ears |
| `pet-species-9` | Snow leopard | EPIC | A fluffy snow leopard with a thick tail |
| `pet-species-10` | Red panda | RARE | A red panda with rounded ears and a ringed tail |
| `pet-species-11` | Tanuki | UNCOMMON | A round tanuki with a friendly masked face |
| `pet-species-12` | Raccoon | COMMON | A clever raccoon with a striped tail |
| `pet-species-13` | Badger | UNCOMMON | A sturdy badger with a striped face |
| `pet-species-14` | Otter | UNCOMMON | A playful otter with webbed paws |
| `pet-species-15` | Ferret | COMMON | A slender ferret with a long flexible body |
| `pet-species-16` | Marten | COMMON | A woodland marten with a fluffy tail |
| `pet-species-17` | Weasel | COMMON | A quick little weasel with short legs |
| `pet-species-18` | Squirrel | COMMON | A woodland squirrel with a curled fluffy tail |
| `pet-species-19` | Chipmunk | COMMON | A tiny chipmunk with striped cheeks |
| `pet-species-20` | Rabbit | COMMON | A soft rabbit with long upright ears |
| `pet-species-21` | Hare | COMMON | A long-legged hare with very long ears |
| `pet-species-22` | Hedgehog | COMMON | A rounded hedgehog with soft stylized quills |
| `pet-species-23` | Porcupine | UNCOMMON | A small porcupine with a fan of stylized quills |
| `pet-species-24` | Mouse | COMMON | A little field mouse with round ears |
| `pet-species-25` | Rat | COMMON | A resourceful rat with a long curling tail |
| `pet-species-26` | Chinchilla | UNCOMMON | A fluffy chinchilla with large rounded ears |
| `pet-species-27` | Hamster | COMMON | A round hamster with plump cheeks |
| `pet-species-28` | Mole | COMMON | A velvety mole with broad digging paws |
| `pet-species-29` | Bat | UNCOMMON | A friendly bat with folded leathery wings |
| `pet-species-30` | Bear | EPIC | A sturdy bear cub with rounded ears |
| `pet-species-31` | Panda | RARE | A young panda with bold eye patches |
| `pet-species-32` | Deer | UNCOMMON | A young deer with delicate antlers |
| `pet-species-33` | Elk | UNCOMMON | A compact elk with branching antlers |
| `pet-species-34` | Goat | COMMON | A sure-footed goat with small curved horns |
| `pet-species-35` | Ram | UNCOMMON | A woolly ram with curled horns |
| `pet-species-36` | Boar | UNCOMMON | A young boar with small tusks and a bristled back |
| `pet-species-37` | Capybara | UNCOMMON | A calm capybara with a broad muzzle |
| `pet-species-38` | Owl | UNCOMMON | A watchful owl with broad folded wings |
| `pet-species-39` | Hawk | RARE | A compact hawk with a hooked beak |
| `pet-species-40` | Falcon | RARE | A swift falcon with pointed wings |
| `pet-species-41` | Raven | RARE | A clever raven with glossy feathers |
| `pet-species-42` | Crow | UNCOMMON | An alert crow with a compact silhouette |
| `pet-species-43` | Crane | UNCOMMON | A graceful crane with a long neck |
| `pet-species-44` | Heron | COMMON | A patient heron with long legs |
| `pet-species-45` | Kingfisher | COMMON | A bright kingfisher with a pointed beak |
| `pet-species-46` | Sparrow | COMMON | A small sparrow with a round body |
| `pet-species-47` | Peacock | UNCOMMON | A small peacock with a decorative tail fan |
| `pet-species-48` | Turtle | COMMON | A determined turtle with a patterned shell |
| `pet-species-49` | Tortoise | COMMON | A sturdy tortoise with a domed shell |
| `pet-species-50` | Gecko | COMMON | A nimble gecko with broad toes |
| `pet-species-51` | Chameleon | UNCOMMON | A chameleon with a curled tail and gentle eyes |
| `pet-species-52` | Iguana | COMMON | A small iguana with a decorative back crest |
| `pet-species-53` | Salamander | COMMON | A smooth salamander with a long tail |
| `pet-species-54` | Axolotl | UNCOMMON | A cheerful axolotl with feathery external gills |
| `pet-species-55` | Frog | COMMON | A springy frog with broad feet |
| `pet-species-56` | Toad | COMMON | A round toad with a textured back |
| `pet-species-57` | Snake | RARE | A little snake in a loose upright coil |
| `pet-species-58` | Moth | COMMON | A fluffy moth with broad patterned wings |
| `pet-species-59` | Butterfly | COMMON | A butterfly with large symmetrical wings |
| `pet-species-60` | Beetle | COMMON | A sturdy beetle with a polished shell |
| `pet-species-61` | Dragonfly | COMMON | A dragonfly with four delicate wings |
| `pet-species-62` | Mantis | UNCOMMON | A poised mantis with folded front limbs |
| `pet-species-63` | Crab | COMMON | A little crab with rounded claws |
| `pet-species-64` | Dragon | LEGENDARY | A dragon with a long scaled body, four clawed legs, swept horns and flowing whiskers |
| `pet-species-65` | Kitsune | LEGENDARY | A mythical fox spirit with pointed ears and a fan of multiple distinct bushy tails attached to one body |
| `pet-species-66` | Phoenix | LEGENDARY | A mythical phoenix bird with a swept feather crest, broad feathered wings and long flame-shaped tail plumes |

## First demonstration — only after director chooses a species

**A. Species base (1 image):** make a premium, clean, transparent, anatomically correct **Rank 1-compatible** species reference using the [approved art direction](PET_ART_REFERENCE_EVOLUTION_ONE_PAGE.md). Treat the earlier Kitsune/Dragon/Phoenix work as render-quality references only; a high-rank ornate design is not an automatic first-rank foundation. Director approves the base before any variants. Follow `docs/workflows/ART_PRODUCTION.md` and the correct generated-asset spec.

**B. Mock player pets (four images):** attach the EXACT accepted species base image bytes as the **only conditioning image** for each new individual. Each uses the same species identity and artwork quality, but different real catalogue inputs. Candidate test vectors below are **illustrative options**, not rolled live identities or captured player data; apply species-appropriate placement and optional accessories. Match the game exactly by obtaining descriptions from `app/src/libs/pets/catalogue.ts` at the same pinned source.

| Demo | Palette (index) | Characteristic (index) | Aura (index) | What it tests |
| --- | --- | --- | --- | --- |
| Player A | Ember (0) | Pale tips (10) | Wind (0) | Warm fur/feathers/scales without turning aura into fire. |
| Player B | Moonlit (1) | Crescent marking (1) | Moon (5) | Cool-toned identity and visible unique marking. |
| Player C | Jade (10) | Mismatched eyes (5) | Lightning (4) | Difficult noncanonical colour + eye identity and contained effect. |
| Player D | Obsidian (9) | Dappled accents (9) | Spirit (7) | Dark palette readability, localized marking and restrained aura. |

**C. Optional evolution proof (1 image):** take one approved individual (e.g. Player B), pass **that pet's own accepted avatar**, *not* the generic species base, plus a species-correct Rank 2 concept. Compare before/after side-by-side for visible advancement and identity preservation.

**Acceptance:** at a small display size (160px), all variants still read as the same species and premium pixel-art family; each clearly differs in the intended palette, characteristic and aura; complete species-native anatomy; no background, shadow, duplicate features or accidental colour/style clone. Final transparent art is raw until processed/QC'd; no asset is called production-valid without actual mechanical checks. This is a local exploration, **not** a call to the live `generateAppearance` mutation (which consumes real player attempts).

**Known source risks:** The live game uses one `previousImg` field and background-removal/quality review, which fits this demonstration; its shared Sharp export is lossy WebP quality 70, which can damage pixel fidelity. Test separately rather than changing the shared service during concept art production. The seeded Dragon is long-bodied, four-legged and whiskered, unlike our winged Dragon style exemplar; obey the CURRENT species identity when a fresh capture exists.

**Next gate:** Director selects one species and approves the species-base direction. All 67 species-base reference statuses are **NOT STARTED**; earlier approved examples are style/AI-avatar assets, not automatic species Rank 1 base approval.
