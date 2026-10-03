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
open/inspect the image itself. It is the primary presentation/style reference. If unavailable, use
the written rules below and flag the missing reference when exact matching matters.

This poster is **presentation authority only**. Never use its displayed skill text or numbers as
mechanical evidence.

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

## Presentation standard

- Prefer a **top-down progression**: Foundations → Hidden Arts → Advanced Arts, with obvious
  prerequisite arrows and generous vertical spacing. Preserve the real topology rather than forcing
  a fixed column count.
- Default to a **vertical 2:3 poster**.
- Integrate the supplied bloodline image into a large evocative hero treatment in the upper
  portion/background. Derive subject, motifs, palette, materials and supernatural effects from that
  exact image.
- Header convention: small **BLOODRIGHT** eyebrow, large bloodline name, then the Bloodright epithet
  as the second title line. Use thematic display effects without reducing legibility.
- **One tagline maximum.** Omit it if the composition does not need one.
- Use one compact rules/legend area near the top. Teal = self buffs, rose = enemy debuffs,
  amber = direct damage. Do not repeat role labels on every card.
- Use calm dark skill cards, restrained ornamental borders, selective glow and contained thematic
  vignettes/icons. Decoration stays away from arrows, names, costs and stat text.
- Keep full skill names, tier labels, costs and effect names readable. Do not number skill cards.
  Percentage-valued tags use `%`; flat Damage values do not.
- Mention eligibility scope **once**.
- Keep the bottom reference area lean. It may contain `Experimental design`, draft number, the
  single scope statement, silver-price status when undecided, and these static examples:
  - `Static bonuses: a 35% tag with +5% becomes 40%.`
  - `A 40 EP jutsu with +5 Damage becomes 45 EP.`
- Do **not** display source SHA, bloodline ID, `forked tree`, generic mechanic primers, generation
  provenance, duplicate scope copy, or common-tag explanations such as Reflect/Afterburn unless the
  user specifically requests them.
- Keep source SHA, hashes, generation id and reproducibility details in the generation log, not the
  player-facing poster.

## Naming and identity discipline

- Never invent or "improve" skill names during image generation. A renamed skill appears only after
  the user-approved rename is recorded in the design source that owns it.
- The exact bloodline image controls visual identity. Do not substitute a similarly named or related
  bloodline.
- Taiyo Kami or another approved poster may be a secondary reference, but the Ethereal Monarch
  poster above is the primary Bloodright presentation reference until the user replaces it.

## QA before delivery

Compare the generated poster against the pinned design and verify every skill name, tier, 1 BP cost,
effect name, numeric value, role color, prerequisite connection, 4 BP maximum and Advanced-Art
limit. Confirm the tree reads top-to-bottom at a glance. Correct generation errors before delivery.

The holy-grail poster is a visual standard, never a mechanical shortcut.
