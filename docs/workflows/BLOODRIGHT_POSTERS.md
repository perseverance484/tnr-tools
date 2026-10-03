# Workflow — Bloodright Poster Presentation

**Status:** user-approved presentation workflow for Bloodright showcase posters.

Bloodright posters are showcase/documentation deliverables, not in-game image assets. The final poster
may intentionally contain typography, cards, arrows, rules and other infographic structure.

## Primary presentation reference

The user-approved **primary ("holy grail") Bloodright presentation reference** is:

- **Ethereal Monarch — Mandate of Heaven**, approved 2026-10-03;
- persistent Library file: `/TNR/Bloodright References/Ethereal_Monarch_Mandate_of_Heaven_Holy_Grail.png`;
- SHA-256: `8a6f5b0f8fbb50e1df4d6ae7a133117b888672c5713be4a1f29f155056bfff31`;
- canvas: 1024×1536, vertical 2:3;
- generation id: `c8f904d9-1cde-458b-9681-b84515e48990`.

Before generating any Bloodright poster, search the persistent Library for that exact filename and
open/inspect the image itself. It is the primary **information-presentation reference**: hierarchy,
flow, grouping, spacing and what information belongs on the poster. If unavailable, use the written
rules below and flag the missing reference when exact matching matters.

This poster is **not a visual-style lock**. Never use its celestial palette, typography treatment,
card materials, ornament, glow, hero composition or other theme-specific art direction as a required
template for another bloodline. It is also never mechanical evidence for skill text or numbers.

## Source authority

For each bloodline:

1. pin the exact design commit;
2. use the tree JSON as mechanical authority;
3. render and inspect the deterministic SVG as topology/layout evidence;
4. read the matching Markdown, validation and kit dossier;
5. inspect the exact bloodline image for visual identity;
6. preserve Fable's branch; poster work belongs in ChatGPT deliverables or a separate `chatgpt/*`
   branch.

When sources disagree, resolve the discrepancy before generation. Do not silently blend versions.

## Information-presentation standard

These are the parts of the Ethereal Monarch reference that should carry across Bloodright posters:

- Prefer a **top-down progression**: Foundations → Hidden Arts → Advanced Arts, with obvious
  prerequisite arrows and generous vertical spacing. Preserve the real topology rather than forcing
  a fixed column count.
- Default to a **vertical 2:3 poster** unless another delivery format is explicitly required.
- Preserve the Bloodright naming hierarchy: **BLOODRIGHT** identifier, bloodline name, then the
  Bloodright epithet/title. The typography and visual treatment of that hierarchy may change freely.
- Put the core purchase rules and one shared role legend near the top, before the tree. Teal = self
  buffs, rose = enemy debuffs, amber = direct damage. Do not repeat role labels on every card.
- Make tier hierarchy immediately readable. Every card must preserve the full skill name, tier,
  1 BP cost and full effect text. Do not number skill cards. Percentage-valued tags use `%`; flat
  Damage values do not.
- Keep prerequisite connections visually unmistakable and free of decorative interference.
- Mention eligibility scope **once**.
- **One tagline maximum.** Omit it entirely if it adds nothing.
- Keep the bottom reference area lean. It may contain `Experimental design`, draft number, the
  single scope statement, silver-price status when undecided, and these static examples:
  - `Static bonuses: a 35% tag with +5% becomes 40%.`
  - `A 40 EP jutsu with +5 Damage becomes 45 EP.`
- Do **not** display source SHA, bloodline ID, `forked tree`, generic mechanic primers, generation
  provenance, duplicate scope copy, or common-tag explanations such as Reflect/Afterburn unless the
  user specifically requests them.
- Keep source SHA, hashes, generation id and reproducibility details in the generation log, not the
  player-facing poster.

## Theme-driven visual direction

The **visual direction is bloodline-specific and may vary substantially** from the Ethereal Monarch
reference. Treat theme as a fresh art-direction problem for every bloodline.

- Use the exact bloodline image as identity evidence and derive an appropriate visual world from it.
- Palette, typography style, card shape/material, border language, ornament density, illustration
  style, hero-art placement, lighting, glow, texture, environmental motifs and supernatural effects
  are all flexible.
- Cards do not have to be dark, typography does not have to be celestial/regal, and ornament/glow
  does not have to resemble Ethereal Monarch.
- The hero image may dominate, recede, frame the tree, sit behind it or be handled another way if the
  theme benefits from a different composition.
- Secondary approved posters such as Taiyo Kami or Aerathiel may inform a particular theme, but no
  previous poster should override the chosen bloodline's own identity.
- The invariant is **information clarity and hierarchy**, not aesthetic sameness.

## Naming and identity discipline

- Never invent or "improve" skill names during image generation. A renamed skill appears only after
  the user-approved rename is recorded in the design source that owns it.
- The exact bloodline image controls visual identity. Do not substitute a similarly named or related
  bloodline.
- Ethereal Monarch remains the primary reference for **information presentation**, not for universal
  art style. Taiyo Kami, Aerathiel or another approved poster may be a useful secondary visual
  reference when it better suits the target bloodline's theme.

## QA before delivery

Compare the generated poster against the pinned design and verify every skill name, tier, 1 BP cost,
effect name, numeric value, role color, prerequisite connection, 4 BP maximum and Advanced-Art
limit. Confirm the tree reads top-to-bottom at a glance. Correct generation errors before delivery.

The holy-grail poster is an **information-presentation standard**, never a universal art-style
template and never a mechanical shortcut.
