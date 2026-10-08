# Workflow — Bloodright Poster Presentation

**Status:** user-approved presentation workflow for Bloodright showcase posters.

Bloodright posters are showcase/documentation deliverables, not in-game image assets. The final poster
may intentionally contain typography, cards, arrows, rules and other infographic structure.

## Standard structural SVG input

**Approved 2026-10-08:** use the [white Blood-Enchanted Eyes example](../design/bloodright/examples/blood_enchanted_eyes_structural.svg) as the default structural SVG format. Its [mechanical snapshot](../design/bloodright/examples/blood_enchanted_eyes_structural.json) makes every displayed value inspectable. The example is a layout standard; its BEE-specific numbers are not a universal balance template.

For structural SVG requests:

- Use a white background, plain neutral typography, grayscale card borders and blank illustration spaces.
- Do not draw artwork, motifs, decorative frames or a colored theme. The user passes the SVG to image generation and handles creative styling.
- Do not print path names, role headings such as Burst/Sustain/Guard/Pestilence, path numbers or skill numbers.
- Keep only the functional legend colors: cyan for self/ally buffs, pink for enemy debuffs and gold for direct damage. Match each effect dot to the shared legend.
- Put the Bloodright identifier, bloodline name, subtitle and rank near the top; place Rules on the left and the shared Legend and Scope on the right.
- Arrange tiers top-to-bottom with clear prerequisite arrows. Each card shows its tier, BP cost, blank image region, exact skill name and full effects.
- State scope once and keep reference notes brief. Omit path totals, Weight/Power Score figures, budget tables and implementation details.
- Preserve the current approved mechanics. The example uses four independent Foundation → Hidden Art → Advanced Art chains, 5 BP total and 1 BP per node; two Advanced Arts would require 6 BP. Adapt the topology and printed rules when another approved tree differs.
- Before delivery, inspect the rendered SVG and check all names, costs, values, prerequisites, legend dots and text fit against its mechanical source.

This is the default **SVG input** standard for future sessions. It does not require an image-generation step. The illustrated-poster references below apply when the user separately requests a finished poster.

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

Use three distinct references for three distinct jobs:

1. **Ethereal Monarch — Mandate of Heaven** controls **information presentation only**: hierarchy,
   grouping, top-down flow, spacing and what belongs on the poster.
2. **Taiyo Kami — Covenant of the Sun** is the primary **rendering/art-style reference**:
   persistent Library file `/TNR/Bloodright References/Taiyo_Kami_Rendering_Style_Reference.png`,
   SHA-256 `d6c575b8b11769ce69c6d117114ddc4cc057f631adc7c2d1d883b23bad020547`.
3. The **target bloodline image** controls subject identity, palette, motifs, atmosphere and thematic
   direction.

Before generation, open and visually inspect both persistent poster references and the exact target
bloodline image.

Taiyo Kami's role is to stabilize **rendering discipline**, not to make every poster solar or visually
identical. Preserve its polished stylized-anime/fantasy finish: crisp readable silhouettes, controlled
high-detail rendering, clean faces/anatomy, strong focal hierarchy, luminous effects with defined
edges, saturated-but-coherent color, and a finished illustrated quality rather than photorealism,
grimdark painterliness or faux pixel-art noise.

Everything theme-specific remains flexible:

- palette, typography treatment, card shape/material, frame language, ornament density, hero-art
  placement, environmental motifs and supernatural effects;
- whether the composition feels regal, ominous, organic, industrial, spectral, martial, serene, etc.;
- whether cards are dark or light, metallic or paper-like, ornate or restrained;
- how much the hero art dominates the poster.

Do not copy Taiyo Kami's fox, solar/fire motifs, orange-gold palette, shrine setting or exact frames
unless the target bloodline independently calls for them. Do not copy Ethereal Monarch's celestial
palace, regal typography or navy/gold language unless the target calls for them.

The invariant is **consistent rendering quality plus clear information hierarchy**, not aesthetic
sameness.

## Naming and identity discipline

- Never invent or "improve" skill names during image generation. A renamed skill appears only after
  the user-approved rename is recorded in the design source that owns it.
- The exact bloodline image controls visual identity. Do not substitute a similarly named or related
  bloodline.
- Ethereal Monarch remains the primary reference for **information presentation**.
- Taiyo Kami is the primary reference for **rendering/art style**.
- The exact target bloodline image remains the primary reference for **theme and identity**.

## QA before delivery

Compare the generated poster against the pinned design and verify every skill name, tier, 1 BP cost,
effect name, numeric value, role color, prerequisite connection, the source tree's BP maximum and
Advanced-Art limit. Confirm the tree reads top-to-bottom at a glance. Correct generation errors before delivery.

The holy-grail poster is an **information-presentation standard**, never a universal art-style
template and never a mechanical shortcut.
