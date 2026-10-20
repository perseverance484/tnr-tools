# Living Lineages — alternating evolution and growth by rank

**Status:** DIRECTOR-PROPOSED SYSTEM CHANGE; **not yet frozen as game design / evolution-stage ruling**. Date: 2026-10-20.  
**Lead:** Art Director; supporting lens: UI/UX / Image Production.  
**Source:** Director's latest description: "Each odd rank is an evolution, each even rank is a growth"; R1 baby base evolution; R2 juvenile base growth; R3 juvenile first evolution; R4 young adult growth; R5 young adult second evolution; R6 mature adult growth; R7 mature adult third evolution; R8 seasoned mature adult growth; R9 fully realized final form.

## Working principle: five forms, four growth steps

**Rank 1** establishes the pet's first **individualized base form** from the shared species reference and the player's selected cosmetic characteristics. **Even ranks** mature the *same evolved form* without requiring a new creature archetype. **Odd ranks 3/5/7/9** are form transitions that introduce/deepen inherited evolutionary traits. This reduces the generator's art-direction burden from nine unrelated forms to **five recognizable form designs, plus four age/growth progressions**.

| Rank | Actual TNR game label | Apparent age | Action | Visual form/state |
| ---: | --- | --- | --- | --- |
| 1 | Companion | Baby | **BASE EVOLUTION** | Species master + chosen palette/marking/aura => personal foundation; unique baby. |
| 2 | Scout | Juvenile | **GROWTH** | Matures the R1 **base form**; proportion, leg, muzzle/ruff growth. |
| 3 | Tracker | Juvenile | **EVOLUTION I** | New evolved form; add/deepen trait (e.g., tail + new markings). |
| 4 | Guardian | Young adult | **GROWTH** | Matures **Evolution I**; no new form requirement. |
| 5 | Hunter | Young adult | **EVOLUTION II** | Changes evolved silhouette and deepens inherited special traits; more tails where applicable. |
| 6 | Warden | Mature adult | **GROWTH** | Matures **Evolution II** without a separate new creature design. |
| 7 | Sentinel | Mature adult | **EVOLUTION III** | New advanced form; stronger unique physical marks/abilities/tail display. |
| 8 | Mythic | Seasoned adult | **GROWTH** | Matures **Evolution III**; age/physique, established form retained. |
| 9 | Sovereign | Fully realized | **FINAL EVOLUTION** | Apex personalized form, incorporating prior evolutionary traits. |

**Game labels** are source-verified at `studie-tech/TheNinjaRPG@19e2010f9cd3f9be26fff96cca0bf6dece322f11` / `app/drizzle/constants.ts`. These are **game rank names**; the age and evolutionary-stage labels above are **proposed art-system concepts** and do not claim existing game fields.

## Two reusable prompt operation types

- **EVOLVE (R1, R3, R5, R7, R9):** previous same-individual artwork + species evolution-stage concept + the player's persistent cosmetic selections + existing inherited evolution traits. R1 instead uses the one species master (no player-specific parent yet). Produce a new **form**, preserving species identity and previously inherited features.
- **GROW (R2, R4, R6, R8):** previous same-individual artwork + age/proportion growth description. Preserve the same evolved form and its cumulative marks/palette/aura; the change is physical maturity, not a fresh evolution concept.

**Implementation consequence:** To retain a new trait consistently, a future implementation needs a durable *per-pet evolutionary trait/appearance history* (trait identifier(s) or snapshot provenance) rather than hoping repeated image prompts independently remember it. Whether new traits are user-selected, deterministic from pet seed, randomly generated, or staff-authored is a director-owned design choice. This proposal does not commit a schema or authorize live generation.

## Unresolved before this becomes the operative final system

1. **Tail/trait timing:** The older director-approved art pilot used R1–9 tail counts `2,2,3,3,4,5,6,7,8`; that assigns new tail totals at **even R6 and R8**. If the new rule requires additions **only at odd EVOLVE ranks**, the exact numeric curve must be revised and approved. Do not silently mix incompatible systems. **Tentative invariance**: an even GROW rank carries the immediately preceding evolution form/trait count rather than introducing a new trait.
2. **Rank 9 vs Rank 10:** The pinned game includes **Rank 10 Celestial**, though the concept poster stops at R9 Sovereign. "Fully evolved final form" can mean **the final form shown in this demo**; it must not silently imply Rank 10 was removed or preempted. Whether Celestial is an apex growth/refinement, a prestige effect, or another outcome needs a separate decision.
3. **Mutation origin:** What exactly is a newly acquired trait at R3/R5/R7/R9, who selects it, and how is it stored/reproduced? Preserve player-selected palette/marking/aura as permanent identity, then explicitly track later-added traits.

**Authority conflict:** `docs/RULINGS.md` / RUL-2026-10-20-002 and the previously approved `LIVING_LINEAGES_KITSUNE_DEMONSTRATION_REGISTER_20261020.md` describe **Growth R1–4, metamorphoses R5/R7/R9**, with different tail milestones. The **newer director description** is authoritative as an *exploratory proposal for the V3 presentation*, but the previous approved roadmap is **not silently rewritten or declared superseded** before the director accepts the operative timing/tail decisions. This document explicitly surfaces the disagreement.

## V3 demonstration status and presentation boundaries

The director already approved a **V3 typographic simplification** of the full presentation: remove repeated per-image labels, keep one species + choices + examples, show shared R1–3 column concepts only once, and use larger typography with separate mobile-readable section crops. During drafting, the director proposed the alternating art system above. Hence **V3 is a reviewable proposed visualization of the newer cadence**; it does not change the already accepted V2 images, source SHA provenance or poster approvals.

**V3 files** were generated non-generatively and remain **conversation deliverables, not Git-pinned binary originals** before structural acceptance. `TNR_Living_Lineages_Kitsune_V3_Alternating_20261020_STRUCTURAL.svg` is a new editable SVG with 26 placeholder placements for 19 assets. `..._FILLED_REVIEW.svg` uses **only the prior presentation cutouts** from the verified V2 source ZIP; no image regeneration, painting or new production export. Structural/filled review geometry matches. The filled V3 has approximately **73 visible text elements** vs **138** in filled V2 (~47% fewer) while enlarging primary fonts.

**Presentation teaching logic:** Gold rank accents signify new evolutionary form and trait accumulation (R1/R3/R5/R7/R9), blue accents mean continued growth of that form (R2/R4/R6/R8). A grouped age track spans baby R1; juvenile R2–3; young adult R4–5; mature adult R6–7; seasoned adult R8; fully realized R9. A grouped form track spans R1–2 base form, R3–4 Evolution I, R5–6 Evolution II, R7–8 Evolution III, and R9 final form. All currently approved artwork stays identifiable as **illustrative**; imagery at R6/R8 still shows added tail complexity and does **not** prove strict compliance with an odd-only trait-unlock rule.

**Boundary:** The final poster, model's art generation behavior and TNR production generator are separate evidence/acceptance gates. No live-game operations, player generation attempts, credentials, uploads, or publishing were performed or authorized.
