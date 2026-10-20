# TNR Premium Pet Artwork — Prompt and Evolution Direction

**Status:** DESIGN PROPOSAL — for TNR developer and director review; not deployed or approved as an implementation contract.  
**Prepared:** 2026-10-20  
**TNR game source inspected:** `studie-tech/TheNinjaRPG@19e2010f9cd3f9be26fff96cca0bf6dece322f11` (public source; *not* a live-database capture).  
**TNR Tools baseline:** `perseverance484/tnr-tools@e13bc9fa085b37bd84ab7736256da8d1ad2a4a99`.  
**Scope:** Generated **UserPet.avatar** artwork: generation prompts, per-species rank art direction, references, fidelity and acceptance. No combat rebalance, existing-pet alteration, content publishing or live-game operations.

## 1. The proposal in one minute

TNR should generate **one unique picture per individual pet at each requested rank**, not upload nine identical, fixed rank pictures per species. The player's chosen palette, distinctive marking and aura are persistent identity traits. An evolution uses the previously accepted image to preserve that individual while visibly changing its anatomy and silhouette.

Add a **premium pixel-art rendering contract** and editable **species × rank visual concepts**. The concepts describe a new physical design milestone for each species at each rank, *not* fixed colours or finished images. Keep the stored individual traits in control of colour, markings and restrained chakra accents. Use the approved Kitsune, Dragon and Phoenix artwork as **rendering-quality references**, not as universal species or pose templates. Optionally support a per-rank shape sketch later, but **never substitute that sketch for the previous individual pet image** without a tested multi-reference design.

This separates three concerns that the current long prompt tends to blend:

1. **What creature is this?** Species anatomy, body plan and recognizable features.
2. **Whose creature is this?** Its saved palette, marking, aura, facial/feature identity and previous approved picture.
3. **How powerful does this rank look?** Staff-authored, species-native changes in the actual silhouette and structure, rendered in consistent high-end TNR pixel art.

**Important count correction:** TNR currently has **10 ranks total**, meaning **one founder image plus nine evolutions**, not nine ranks total.

## 2. Verified behaviour and compatibility boundaries

These are source observations, not guesses about production data or proposed new rules.

| Area | Source-verified behaviour | Practical consequence |
|---|---|---|
| Identity | Saved pets carry `speciesId`, `paletteIndex`, `characteristicIndex`, `auraIndex`, `rank`, `artRank`, `avatar` and `avatarFacing`. | Do not replace unique saved traits with an entire species's fixed art. |
| Authored species | `PetSpecies.description` is staff-editable text, max 1,000 characters. There is **no rank-concept or rank-sketch field** in the inspected schema/editor. | The developer's suggested per-rank text is new functionality, not already available. |
| Ranks | `PET_RANKS` names ranks 1–10: Companion, Scout, Tracker, Guardian, Hunter, Warden, Sentinel, Mythic, Sovereign, Celestial. | Any per-rank art contract must support all 10 entries, including the base rank. |
| Trait selection | Species, palettes, markings and auras are separate catalogues. Their indices are persisted and the catalogues say to append entries, not reorder. | Style tuning must not change the catalogue indices or forced-colour choices. |
| Original and evolved generation | A new pet is prompted from species + saved traits; evolution supplies the previous accepted cutout as an image reference. A same-rank redraw retains maturity. | Preserve the established identity-reference path and rank-vs-`artRank` distinction. |
| Image request | `txt2imgNanoBanana` runs `google/nano-banana`, with a square request, `512×512` output bounds, background removal using `851-labs`. The current config exposes **one** `previousImg` field. | Initial release can improve text without introducing a second image dependency. Multiple source images require code/provider verification. |
| Actual export | Shared Nano Banana path resizes with Sharp and encodes `.webp({ quality: 70 })`. | **Potential fidelity risk**, not a visually proven defect: lossy re-encoding and resampling may soften pixel edges. Benchmark a pet-only lossless export path; do not globally change other image consumers. |
| Cutout and acceptance | Download/moderation, transparency, full-body and visual quality checks run before acceptance. A reviewer checks species, anatomy, previous identity and stronger evolution. The accepted right-facing sprite can be losslessly mirrored left. | Preserve review, transparency, identity, facing and failure behaviour. No shadow/ground patch in final sprite. |
| Attempts and state | Up to three player-triggered image attempts *per rank*; one in-request visual-quality correction can happen. A failed late evolution can keep the preceding image rather than erase it. | Do not experimentally spend real players' attempts or silently alter fallback policy. |
| Presentation | Pet profile displays the avatar in a `160×160` object-contained box; the same pet avatar enters combat state. | Judge shape and facial identity at small UI/battle sizes, not only zoomed-in originals. |

**Pinned source pointers (inspect at these SHAs when implementing):**

- [`app/drizzle/constants.ts#L676-L707`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/drizzle/constants.ts#L676-L707) — ranks, attempts and timeouts.
- [`app/drizzle/schema.ts#L2937-L3010`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/drizzle/schema.ts#L2937-L3010) — species and individual pet fields.
- [`app/src/libs/pets/catalogue.ts#L28-L95`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/src/libs/pets/catalogue.ts#L28-L95) — actual palettes, markings, auras and stable index warning.
- [`app/src/libs/pets/appearance.ts#L18-L174`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/src/libs/pets/appearance.ts#L18-L174) — full prompt and generator/corrective pipeline.
- [`app/src/libs/pets/quality.ts#L8-L102`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/src/libs/pets/quality.ts#L8-L102) — image-based acceptance.
- [`app/src/libs/replicate.ts#L266-L279`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/src/libs/replicate.ts#L266-L279) and [`#L345-L441`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/src/libs/replicate.ts#L345-L441) — source image handling, model prompt ordering, crop and output codec.
- [`app/src/validators/petSpecies.ts#L18-L70`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/src/validators/petSpecies.ts#L18-L70) and [`app/src/libs/petSpecies.ts#L112-L136`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/src/libs/petSpecies.ts#L112-L136) — staff authoring contract and current editor.
- [`app/src/server/api/routers/pets.ts#L725-L930`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/src/server/api/routers/pets.ts#L725-L930) — rank-up, reserved image attempts, accepted/failed states.
- [`app/src/layout/PetProfile.tsx#L734-L746`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/src/layout/PetProfile.tsx#L734-L746) — profile image size.
- [`app/tests/libs/pets/appearance.test.ts`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/tests/libs/pets/appearance.test.ts) — existing seam for prompt, cutout, identity, retry and facing tests.

**Different contracts:** The TNR Tools art spec's `AI_AVATAR` target describes `userData.avatar` and recommends a 640-square lossless WebP. The game's *automatic pet* path writes `UserPet.avatar` using a separate 512-bound provider flow. The approved reference artwork below is 640-square lossless and demonstrates style; that alone does **not** establish a new 640/450-KB server contract for pets. Preserve the game's actual pet-image constraints until implementation tests establish a safe alternative.

## 3. Premium pixel-art visual contract

### What to borrow from our approved examples

Three director-accepted, transparent, 640-square, lossless WebP art references have already been produced. Their names/hashes are given to make it possible to attach the **actual bytes** and prevent a stylistic reference from silently changing:

| Style exemplar | File and SHA-256 | Transferable qualities | **Do not** clone |
|---|---|---|---|
| Kitsune | `kitsune_ai_avatar.webp` — `4134df419936c55d896a755abd06090019e97dd01a87e62217753911a7854a69` | Precise fur layers, elegant head shape, high-definition pixel clusters, separated flowing tails, carefully controlled highlights. | Its red-white palette, ceremonial ornaments or large evolved tail display on every other pet. |
| Dragon | `dragon_ai_avatar.webp` — `bcd81c13621f9d96750c50d6d39f38d6bebfa756662ca6a9f387568d3ff7badc` | Dense readable scale plates, dramatic contour break-up, material highlights and bold dark-to-bright contrast. | **The Western winged anatomy**: the game's seeded Dragon describes a *long-scaled, whiskered, four-legged* creature. The sample is a **style-only reference**, not evidence of the species's canonical body plan. |
| Phoenix | `phoenix_ai_avatar.webp` — `94b916e912b376ec1e5039da83c614d13bd21fbf66705c38ccecab9b7f2c6142` | Clear avian anatomy, wings-as-primary silhouette, sharp layered feathers and fiery colours contained in feathers. | The sample's fire colours, aerial pose or wing structure on mammalian/fish/insect species. |

The seed descriptions are in [`0090_pet_companions.sql#L128-L133`](https://github.com/studie-tech/TheNinjaRPG/blob/19e2010f9cd3f9be26fff96cca0bf6dece322f11/app/drizzle/migrations/0090_pet_companions.sql#L128-L133). Seed text is historical identity evidence, **not a fresh production species capture**; the currently editable `PetSpecies.description` must win for an actual live record once captured.

**Style follows the reference's craftsmanship, not the reference's species, colour or pose.** No contact sheet as a conditioning image. Use an individual style reference only where the provider genuinely ingests its bytes and does not displace the mandatory previous-pet identity reference.

### Rendering instructions

- **Pixel discipline:** polished retro pixel art, crisp intentionally placed pixel clusters, solid contour readability, defined cel-shaded planes, no blurry painterly brushing or photography. Detailed *within* the silhouette, never a haze around it.
- **Premium finish:** refined feather/fur/scale material textures, consistent light direction, crisp specular highlights on the correct materials, controlled warm/cool shadow separation. Aim for a high-quality finished game asset, not rough pixel doodles.
- **Species-first shape:** a Phoenix reads from spread wings and long tail plumes; a Kitsune from fox head and distinct connected tails; a long-bodied whiskered Dragon from winding spine, leg placement and facial whiskers. No universal dragon-like flying wedge, generic horned beast or identical heroic stance.
- **Colour fidelity:** the saved palette controls the main hues and their placement. The chosen characteristic is visible, legible and stable. The selected aura is secondary; a premium result can use rich local contrast without turning every pet into a red-and-gold fire creature.
- **Contained effects:** chakra or flame motifs live on feathers, fur, scales or small attached trim. Do not add drifting smoke, free-floating particles, magic rings or broad exterior glows; these break cutouts and reduce readability.
- **Small-size legibility:** reserve detail for face, iconic limbs/wings/tails and one rank-specific silhouette milestone. Avoid tiny noise and excessive jewellery which disappear at the real display size.
- **Camera and framing:** retain TNR's elevated three-quarter viewpoint, normally left-facing, single complete subject, square composition, approximately 10% clean margin per side. A bird may be *flying* rather than standing; a fish may be swimming; an insect may hover. Body plan outranks a blanket 'planted paws' instruction.
- **Final alpha:** no background, floor, cast shadow, pedestal, border or text. The generator may temporarily use the existing uniform `#f0f0f0` staging field so the current background remover can cut out gaps between limbs/wings/tails, but that field is **not part of the delivered sprite**.

**Avoid a global pixel-art look that is simply 'more glow':** gold jewellery, fire, enormous wings, crown-shaped horns, celestial halos and magenta edges are not universal upgrades. The examples share craft quality, not a generic visual costume.

## 4. Proposed prompt assembly

### Order of authority

1. **Required:** correct species anatomy, body plan, one-head/one-body completeness and current record description.
2. **Required:** this exact pet's saved palette, marking, aura, facial identity and previous accepted appearance where available.
3. **Required:** requested rank's species-native *physical* upgrade and preserved earlier upgrades, not merely visual brightness.
4. **Required:** premium pixel-art rendering, camera/size and clean-cutout rules.
5. **Optional, subordinate:** staff-authored species/rank shape concept.
6. **Later optional, subordinate:** approved shape sketch — never a replacement for previous-pet identity.

Never send the player's free-form pet name to the image model. Existing code correctly excludes it. Staff-authored species text should be schema-bound, logged for review and treated as *descriptive data*, not a new system instruction.

### Copy-ready core template — founder

The subject appears first because the current Nano Banana wrapper expects an ordinary descriptive prompt, not a system-role message.

```text
Create ONE full-body [SPECIES] companion for The Ninja RPG.
Anatomy: [CURRENT_STAFF_AUTHORED_SPECIES_DESCRIPTION].
Recognizable body-plan anchors: [BODY_PLAN_AND_DISTINCTIVE_SPECIES_SILHOUETTE].
This is an individual adult creature, not a humanoid.

Individual appearance: [PALETTE_DESCRIPTION].
Keep the [CHARACTERISTIC_DESCRIPTION] unmistakably visible.
Selected chakra accent: [AURA_DESCRIPTION], applied as small, contained
surface markings or localized pixel highlights on the creature.

Rank [RANK] of 10 — [RANK_NAME].
Physical design milestone: [STAFF_AUTHORED_RANK_CONCEPT_OR_SAFE_DEFAULT].
Express maturity through species-native anatomy and silhouette,
not size inflation, camera zoom, excessive decoration or glow.

Premium high-definition retro pixel art for a finished combat sprite:
precise intentional pixel clusters, crisp linework, bold readable outline,
layered cel-shaded material planes, rich but controlled contrast,
sharp details in fur/feathers/scales as appropriate, one consistent
light direction and clear facial identity. Never smooth or painterly.

Elevated three-quarter view; face/muzzle/beak oriented toward image left
when anatomically practical. Use a species-appropriate [POSE].
Show the complete head, body, appendages, crest and tail in one square
composition with clean margins around all sides.

Render on perfectly uniform #f0f0f0 gray including gaps and holes for
background removal. No scene, platform, ground, cast shadow, text,
additional creature, extra limbs/heads, invented anatomy, floating magic,
outer aura cloud, blurred highlights, gradient haze or watermarks.
```

### Copy-ready evolution insertion (rank > 1)

Put this **after individual identity and before rendering**; pass the previous accepted pet avatar using the existing `previousImg` pathway:

```text
The attached previous-rank image is the SAME individual pet, not a style
sample to overwrite. Preserve its species, recognizable face, permanent
colour placement, unique markings and accessories, and the visual weight
of earlier native upgrades. New rank: [RANK] [RANK_NAME], previous art rank:
[ART_RANK]. At this rank make these new, clearly visible physical changes:
[RANK_CONCEPT]. Preserve [STABLE_ANATOMICAL_ANCHORS]. Do NOT use
[WRONG_SPECIES_OR_GENERIC_MORPHOLOGY].

Redraw a clean new full-body composition; do not trace the previous alpha
edge, copy the old gray cutout fringe, merely scale up the old sprite or
replace the animal with another species. Keep the same overall camera and
character identity while allowing a species-correct evolution pose.
All elements remain in frame with clean cutout gaps.
```

**Same-rank redraw:** explicit `RANK == ART_RANK` handling: **do not evolve, age, add armour, simplify or change saved traits**; only improve rendering/cutout/anatomy at the currently accepted rank. Preserve the existing distinction in `getPetAppearancePrompt`.

**Integration note:** Current `getPetAppearancePrompt` embeds `PET_ART_STYLE` in its returned text **and** supplies that same value as `preprompt`. On founders, the wrapper appends `preprompt` after the prompt, potentially repeating the style block. On image edits, `preprompt` is not used at all. Prefer building one canonical subject-first prompt shared by both paths, then passing empty/compatible wrapper guidance rather than duplicating a large style block. Preserve API shape and tests while refining this.

## 5. Staff-editable rank concepts: proposed data contract

**Fastest useful release:** an optional text field per species per rank; no fixed rank images. Existing descriptions and pet traits remain untouched.

Suggested logical record (illustrative; **not** an existing schema):

```json
{
  "speciesId": "existing-species-id",
  "rankVisualConcepts": {
    "1": "Lean but unmistakably adult foundation of this species; simple natural outer silhouette.",
    "2": "Develop more confident native stance and a visibly stronger core.",
    "3": "Develop the species' natural locomotor / striking anatomy.",
    "4": "Introduce a clearly new protective tier in native plumage, fur, scales or shell.",
    "5": "Strengthen native weapons or locomotion without adding new limb types.",
    "6": "Expand existing protective shapes into a larger, readable outer contour.",
    "7": "Develop the species-specific tail, wing fan, fin or rear-body display.",
    "8": "Add a strong native dorsal / back silhouette milestone.",
    "9": "Develop a distinguished head, mane, crest or front-shell silhouette.",
    "10": "Integrate previous motifs into a clearly sovereign full-body form without altering species identity."
  }
}
```

Those ten strings above are **generic placeholders**: the real value of this feature is replacing them with **authored, species-specific** descriptions. Avoid broadcasting "develop long claws", "heavy shoulder armour", "broad tail fan" and "planted stance" to every creature. Birds, aquatic pets, insects, serpents and shell creatures need different power grammar. Provide clear fallback to the *existing* `RANK_APPEARANCES` for missing entries until all desired species are authored. A missing field must never block existing pet generation.

**Implementation surface (developer-owned, separate code review):**

- Add a backwards-compatible optional JSON field on `PetSpecies` (e.g. `rankVisualConcepts`) with keys limited to supported rank numbers and bounded trimmed text lengths. Migrate/schema/validator/server and staff-only species editor together. Do not write rank concepts on `UserPet`; each individual's traits remain separate.
- Offer staff a collapsible **Rank 1–10 Appearance Direction** editor (text only first). Explain "body shape, silhouette milestone, anatomy to keep / avoid; never fixed palette". Preserve errors/drafts like the current species editor.
- Compose only **server-validated staff-authored text** with saved catalogue descriptions. No public user prompt input; no unverified URL or raw HTML interpreted as directives. Audit staff changes using the existing `petSpecies` action logging.
- Keep the rank concept snapshot deterministic *for that request*; if concepts are edited while a pet is mid-generation, the accepted artwork/traits are still guarded by its existing server lease.
- Test missing/malformed/migrated fields, old inactive species, same-rank redraw, rank 10 and compatibility of existing API calls. Empty concepts use old behaviour, not an empty/garbled prompt.

### Example: 10-step Kitsune direction (body shape only)

These are **illustrative editorial drafts**, **not approved canon** or instructions that every fox must have nine tails or red flames. Exact tail-count progression belongs to the game's content director.

| Rank | Species-native visual milestone |
|---|---|
| 1 Companion | Elegant adult fox, pointed ears, clear muzzle, several distinct connected bushy tails; minimal ornament. |
| 2 Scout | Slightly deeper chest, longer stride and confident alert ear posture; original tail structure stays recognizable. |
| 3 Tracker | Stronger forequarters and haunches, raised tail fan, forward tracking stance; no extra legs. |
| 4 Guardian | Two-layer fur mantle at shoulders and chest, projecting clearly beyond the previous outline. |
| 5 Hunter | More substantial natural paws and claws, athletic torso, sharper ready-to-spring stance. |
| 6 Warden | Broad swept cheek/shoulder ruff with distinct tiers, still soft fur rather than metal armour. |
| 7 Sentinel | Distinctly broader, layered tail fan with visible separation of every connected tail. |
| 8 Mythic | Raised flowing dorsal mane and high neck ruff integrated into the fox body. |
| 9 Sovereign | Refined crown-like ear/forehead fur structure, deeper commanding chest; familiar eyes/muzzle remain. |
| 10 Celestial | Grand layered chest/shoulder mane plus a second lower sweeping tail tier; coherent balanced whole-body fox silhouette. |

**Bird archetype:** For a Phoenix, evolve wing roots, primary feather layers, tail-plume architecture, breast strength and crest height. Wings stay the primary silhouette. **Do not** give a flying bird a dragon-like heavy stance or exterior wing-shaped spell effect.

**Dragon archetype:** Follow the current species description. In the shipped seed it is long-bodied, scaled, four-legged and whiskered. Evolve its spine arc, segmented scale plates, mane/whiskers, natural crest, jaws and leg support. **Do not** import wings from the winged style sample unless that species's *current authored identity* explicitly allows wings.

**Other body plans:** Quadrupeds grow through shoulders/haunches/paws; fish through fins and body contours; insects through thorax, wing cases/antennae; shelled creatures through shell profile and native appendages. No generic crown, horns, fur ruff, talons or armour applied across all species.

## 6. Practical complete examples

These are test prompts, using **real currently defined catalogue choices**. They do not add new player traits or prescribe a canonical palette for the species.

### Example A — new Kitsune, rank 1

```text
Generate ONE full-body adult Kitsune: a mythical fox with pointed ears, one
natural fox head, four native legs and several separate bushy tails attached
to the same body. Individually selected appearance: silver, slate and pale
blue; distinct pale tips on ears, limbs and tails; a subtle Spirit accent
drawn as fine pearl-toned markings on existing fur, not orbiting motes.
Rank 1 Companion: elegant lean adult foundation with clean, recognizable
fox anatomy, no large protective mantle or extreme crown. The tail fan
is readable but not a maximum-rank display. Premium finished TNR pixel art:
crisp deliberate pixel clusters, rich cool-shaded fur, clean contour,
precise three-step cel-shaded depth and luminous but contained highlights.
Natural alert three-quarter pose facing toward image left. All tails, ears
and paws inside a square composition with clean margins. Perfectly
uniform #f0f0f0 temporary background, also between tails/legs, for
cutout. No scenery, ground, shadow, another fox, humanoid body,
floating aura, blur, words or watermark.
```

### Example B — evolved Phoenix, rank 6 (with previous pet image)

```text
Redraw the SAME individual Phoenix from the supplied previous-rank image.
Keep its recognizable beak, eye character, crest, original selected colour
placement and distinctive markings. Rank 6 Warden: make its real wing-root
structure and overlapping primary/secondary feather layers substantially
more powerful and wider than the previous form, with strong chest and a
bolder swept crest. Preserve and expand already established tail plumes.
A Phoenix stays unmistakably AVIAN and may be airborne: do not invent
dragon legs, horns, fur, metal shoulder shields or a heavy standing beast.
Premium intricate pixel art: crisp feather-edge clusters, shadowed layered
wing planes, high local contrast, controlled highlights ON feather edges.
Three-quarter view, beak toward image left; entire wing and tail silhouette
inside generous square margins. No external smoke/flame cloud, ground
shadow, scenery or copy-pasted background. Uniform #f0f0f0 temporary
cutout field including all gaps.
```

### Example C — evolved long-bodied Dragon, rank 9 (with previous image)

```text
Redraw the SAME long-bodied, four-clawed-leg, whiskered Dragon shown in the
supplied previous-rank reference. Keep its individual selected palette,
facial design, eye colours and distinctive markings. Rank 9 Sovereign:
develop a visibly higher integrated head/neck crest, heavier scaled
supporting chest and a more commanding serpentine neck silhouette.
Preserve established segmented back scales and tail, with each native leg
connected. Follow this exact species' authored body plan: do not turn it
into a generic winged Western dragon just because a STYLE example had
wings. Premium TNR pixel art with finely resolved overlapping scales,
deliberate stepped shading, crisp linework and clean luminous highlights
within the animal. Elevated three-quarter coiled battle-ready pose, head
toward image left, full body contained in square safe margins. Flat
#f0f0f0 temporary backdrop in EVERY gap for clean cutout; no scene,
magic circle, smoke, floor, added heads or extra limbs.
```

The palettes/traits for B and C remain the **saved actual pet values**; the examples deliberately do not invent a player's selections.

## 7. Reference sketches: a later optional feature, not the MVP

A useful optional rank sketch conveys *body geometry* only: neutral silhouette, limb/wing count, contour changes, camera and proportion. It must not impose a colour palette, markings, aura or another player's pet identity.

**Current constraint:** `Txt2ImgConfig` exposes `previousImg?: string` and its implementation sets `image_input = [previousImg]`. The path as called by pets supplies one source image. The provider's ability to accept multiple references with consistent identity, provenance, aspect and cleanup is **not verified by this design review**. Do not silently replace the previous pet with a rank sketch.

If multi-reference support is built and tested, the priority is: **A = previous approved pet (identity)**, **B = optional approved shape sketch (geometry)**. Prove both are passed through real bytes, not a bare URL in text, and establish how the provider distinguishes their roles. Keep sketches staff-only and versioned; missing sketch is a normal text-only success path.

## 8. Fidelity and image-processing improvement

The current game's `txt2imgNanoBanana` performs:

```ts
sharp(sourceBuffer)
  .resize({ width: 512, height: 512, fit: "inside" })
  .webp({ quality: 70 })
```

This is efficient for general images but **not inherently ideal for high-contrast pixel art with hard alpha edges**. Pixel-art fidelity should be measured *after* model output, background removal and final export, not inferred from the prompt or a large chat preview.

**Suggested small, isolated investigation before any shared codec change:**

1. Use the *same offline/generated input image bytes* and cutout to compare the existing resample/lossy-70 output against pet-only `lossless WebP` and an appropriate pixel-edge-preserving resize option (e.g. nearest-neighbour), at the same final canvas and alpha. Do not assume nearest always wins: inspect detail loss and jaggies.
2. Compare on dark and light backgrounds and at the game's 160-square profile size and representative combat sprite size. Include the edges between separate Kitsune tails and Phoenix feathers and around Dragon whiskers.
3. Record output size, alpha bounds, background fragments, visual sharpness, additional server cost/latency and what would be changed in the real pet-only path.
4. Only then consider an explicit *pet-only* encode option on `txt2imgNanoBanana`, or a separate post-processing helper. Leave AI portraits and other image consumers unchanged unless separately assessed.

The inspected pet validator bounds downloads to 5 MiB and 1,048,576 pixels; that is **not proof** that every upload path will accept any lossless file of that size. Confirm the actual server upload route, CDN behavior and resource cost before setting a new byte policy. The TNR Tools `AI_AVATAR` 450-KB working ceiling should not be copied onto `UserPet.avatar` without evidence.

## 9. Acceptance and regression tests

### Offline/fixture-first acceptance suite (no live game)

Test at least one **founder, evolution and same-rank redraw** for each of the three shape classes (Kitsune, long-bodied Dragon, flying Phoenix), mixing palettes and characteristics rather than reproducing only the three premium samples.

**Required correctness:**

- One identifiable species-native animal, one connected body/head, natural limb/wing count and fully visible extremities, no geometry hallucinations.
- Exact saved palette/marking/aura remain identifiable across ranks; no blanket Ember palette and no player-name prompt injection.
- Rank-up visibly changes **anatomy and silhouette** compared with previous accepted image at identical framing, not just glow, jewellery or zoom. Earlier substantial structures aren't accidentally discarded.
- A Phoenix remains bird-shaped and may fly; a long-bodied Dragon retains authored anatomy; Kitsune tails are distinct and connected. No cross-species silhouette copying.
- Temporarily staged gray is completely removed, including interior gaps. Alpha/dark-background composite and small-size preview clean; no cast shadow/ground.
- Correct facing/review/mirror behavior; full square pose within appropriate margin without clipped tips.
- No degradation of existing moderated, leased, logged, bounded retry flow. No live requests/writes as part of fixture verification.

**Technical tests to extend (developer-owned):**

- `getPetAppearancePrompt`: founder vs redraw vs evolution, rank concepts present/missing, actual trait descriptions in output, no user's chosen name, no duplicated giant style preamble.
- Rank concept schema and server/editor round-trip: rank keys 1–10, lengths, empty defaults, species ID ownership, retired species; backward-compatible rows.
- Mocked `generatePetAppearance`: prior image passed only when present, 851-labs removal still active, provider prompt ordering correct, tests for failed moderation/visual review, allowed correction count, successful facing flip, save guards/leases and short attempts.
- Image processing: deterministic sample cutouts, dimensions, valid decoded WebP, transparency, no severe new halo/smoothing, realistic byte budget.
- Manual comparative 160-square and battle-size gallery, with side-by-side **current prompt** vs **new prompt** on the **same scenario and saved identities**. If concept+prompt yields worse consistency, revise instead of shipping by taste alone.

**Known existing safeguard to make visible:** After the single internal corrective pass, the code may waive only the subjective `evolutionStronger` quality flag while retaining all other visual checks and emitting a warning. Changing that is a **player-attempt / support-load policy decision**, not a mere art wording change. Measure weak-evolution occurrences first; director decides whether acceptance becomes stricter.

## 10. Suggested staged implementation and ownership

| Stage | Scope | Review gate |
|---|---|---|
| **P0 — prompt benchmark** | Pure prompt composition refactor; species-anatomy hierarchy, concise premium style block, species-native pose, eliminate duplicate founder style text. Compare existing vs proposed outputs *offline*, using saved examples and mocked provider tests. | Content/art director selects the visual target after identical-input comparisons; no shipped behaviour change yet. |
| **P1 — text rank concepts** | Staff-only optional species × rank concepts with schema/migration/editor/API/validation and safe fallback to old rank descriptors. | Fable/implementation review on an exact frozen SHA, schema migration/backward-compat and existing pet tests. |
| **P1b — pixel export fidelity** | Separately benchmark and, if warranted, add pet-only lossless/pixel-edge preservation in actual provider path; keep other content unaffected. | Byte/cost/dimension tests plus native dark/light composite and small-size visual approval. |
| **P2 — optional rank sketches** | Only after multiple image references are proven safe with the existing identity image. Sketch controls shape, not palettes. | Per-image reference provenance, fallback, tests for identity drift and removal/background fidelity. |

Do not silently select P2 as a prerequisite for P0/P1; **text concepts alone are useful**. Do not add nine fixed image fields or promise visually perfect generated evolutions in an untested provider. A more expressive prompt is a hypothesis to benchmark, not a guarantee.

**Owner responsibilities:** The project director owns art direction, acceptance and all live decisions; the TNR game's developers own game-code/schema/provider deployment; Fable is the normal implementation author in `tnr-tools` if local tooling or an independent prototype is commissioned; ChatGPT can review the exact resulting implementation. Do not treat access to public code as permission to modify or call production.

## 11. Decisions requested before implementation

1. **Premium look:** Confirm these three approved figures are the **quality/rendering standard** for companions, while each individual species keeps its own shape/palette and rank-appropriate complexity.
2. **First release:** Recommend **prompt refactor + staff-authored text rank concepts**, with **rank sketches deferred**.
3. **Style/engine distinction:** Permit pet-specific pixel-friendly encoding to be evaluated separately from prompt rewriting. No automatic 640-pixel or general upload-cap policy change is implied.
4. **Progression acceptance:** Preserve current fallback for weak but otherwise valid corrected evolutions unless an explicit support/attempt decision changes it.
5. **Content authorship:** Species × rank descriptions are authored/approved by Content; the player selects only the existing cosmetic variables.

**Status at handoff:** Source-read design proposal only. No new field, migration, prompt change, image provider call, live capture, live request or live write has been performed by this document.
