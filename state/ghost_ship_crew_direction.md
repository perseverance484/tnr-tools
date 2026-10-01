# Ghost Ship crew: recurring chakra echoes

**Status:** ACTIVE DIRECTION REVISION, requested by dauntless 2026-10-01 (RUL-2026-10-01-005). Complete summoned chakra echoes replace missing-body imagery. The particular aura/afterimage treatment below is a proposal awaiting visual-direction review.
**Lead:** Content Designer / Art Director, then Image Production.
**Sources:** `state/ghost_ship_retheme_design.md`, `state/ghost_ship_art_production.md`, the existing record/name map and shared-pool migration.

## What carries forward

The ship is a top-secret military project; its original personnel were all elite shinobi specialists. Retain their approved short names, duties, equipment distinctions and combat roles. Preserve the locked ship design, Skyglass palette, Captain/Crowned Captain identity relationship and reward names.

The vessel holds chakra resonances left by the original crew. Its unstable Skyglass system repeatedly summons complete chakra-made echoes from those stored patterns. The echoes man the helm, handle navigation, maintain the seal lattice and defend the vessel. They are recurring constructs with remembered personalities and habits, rather than injured survivors or revived bodies. The original crew's ultimate fate need not be settled by the art.

Proposed loop: the lattice gathers coherence, summons the crew, and the crew stabilize and pilot the ship; when coherence fails, echoes disperse and the ship slips out of stable space. The next manifestation summons them again. More faithful echoes can retain memories across manifestations, preserving the existing time, chart and unfinished-mission reveals. The tragedy is repeated duty and limited continuity of life.

## Proposed common visual treatment

- **Complete bodies:** intact arms, hands, faces, throats and torsos. Use a complete chakra form inside heavy armor. Body gaps, floating severed-looking parts and hollow anatomical openings are no longer visual markers.
- **Visible spectral identity:** cool desaturation across the whole figure, a narrow pale white-blue aura following the silhouette, and one slight offset contour or a few bounded chakra wisps. The effect must read at client size; it cannot depend only on tiny glowing scratches.
- **Preserve character readability:** retain near-black specialist clothing, recognizable faces and equipment. Convey an ethereal appearance through palette, light and controlled afterimages before attempting uniform transparency.
- **TNR execution:** clean pixel bands and crisp edge shapes, with the core figure readable. A broad blurred glow is not the proposed treatment. The user's aura request takes precedence over older prompt negatives for this workstream; do not carry a blanket “no aura” instruction into the next prompt. Existing chroma/soft-edge limits still need explicit QC, not assumptions about compliance.
- **Coherence hierarchy:** lesser echoes have a slightly wavering or displaced contour. The Captain is steady; Crowned Captain is the most coherent and authoritative, with the same recognizable identity. Power does not require bodily distortion.

This is a creative change to non-injurious subject matter, not a guarantee about any service's moderation outcome. No art-skill code or global spec has been changed.

## Roster application

| Character | Retained role / identity | Whole-echo treatment |
|---|---|---|
| Deck Warden | Boarding-security chief; approved armor, mask and hooked interception blade. | Restore the complete arm and sleeve. Give the whole operative a restrained chakra tint and close aura; retain the established asymmetry of the equipment. |
| Oathkeeper | Binding/access master; narrow silhouette, forearm bindings, oath gesture and rigid collar. | Complete human lower face and throat. The collar is worn equipment. Pale resonance traces and a close aura identify the summoned figure; his expression carries remembered grief. |
| Wayfinder | Spatial-seal navigator with a veiled head and compact sighting frame. | Complete figure with one slightly offset echo contour suggesting imperfect synchronization. |
| Arsenal Keeper | Weapons master with heavy gauntlets and a sealed armament case. | Closed, intact torso and armor; subdued chakra light follows figure and carried gear as one summoned impression. |
| Sentinel | Barrier master's impression in a heavy defensive frame. | A complete coherent chakra construct fills the frame. Inner seam-light and the surrounding aura replace empty joints or a missing occupant. |
| First Blade | Captain's combat specialist; lean armor and one long blade. | Intact duelist with a short delayed energy contour following the blade and sword arm. |
| The Captain | Project commander and primary Skyglass operator. | Full, recognizable figure with a steady, tightly controlled aura. |
| Crowned Captain | The same commander at highest command fidelity. | Clearest, most coherent echo; functional Skyglass Crown and precise light preserve authority without anatomical change. |
| Core Horror | Elite Core engineer whose stored resonance is unstable. | A complete operative overwhelmed by resonance: overlapping contours and a denser chakra field. Retire body/hull fusion. Exact effect remains to be tested, one readable central subject. |
| Seal Charge | Classified demolition device. | Existing compact seal-casket direction remains; this is hardware rather than a crew echo. |
| Core Canister | Chakra-containment hardware. | Existing tall reinforced crystal-vessel direction remains. |

## Current art and next test

- Quest icon remains **LOCKED**; its exact ship design still governs scenes.
- Deck Warden `_b` was explicitly approved under the preceding body-gap direction. Preserve its exact bytes and that approval history, but **HOLD it from the current delivery pack pending a whole-echo revision**. Use it only as an equipment/identity reference, not as a reference for missing anatomy.
- Oathkeeper `_b` was not accepted. It is **SUPERSEDED as a current candidate** by this direction request. Preserve its narrow uniform and gesture as possible design references, with a complete face/throat in the replacement.
- Proposed next test: **Deck Warden `_c`**, restoring the arm and establishing the common ethereal treatment. Settle this proposed visual treatment, then generate/process/show one replacement and obtain its visual lock before continuing.
- At client size, require elite specialist identity, complete anatomy and unmistakable chakra presence. Continue the bundled raw-QC, export, dark-composite and preflight workflow. Do not silently relax numeric checks or overwrite a previous filename.

## Content boundary

Keep the 11 record slots, 57-node graph, five endings, shared-pool kits, numeric tuning and reward contract. The machine patch remains the previous prose baseline and requires reconciliation before a Fable implementation freeze, especially Core Horror and bodily-reconstruction wording. Current work is direction development, not live-game changes. No retired bespoke jutsu art.
